#!/usr/bin/env python3
"""Read-only plan normalization, offline control validation, and task selection."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = SKILL_ROOT.parent
SCRIPT_ROOT = Path(__file__).resolve().parent
AGENTJOB_SCRIPTS = SKILLS_ROOT / "agentjob-control" / "scripts"
if AGENTJOB_SCRIPTS.is_dir():
    sys.path.insert(0, str(AGENTJOB_SCRIPTS))
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

try:
    from agentjob_runtime.errors import RecordValidationError, SecurityError
    from agentjob_runtime.path_security import resolve_project_relative
    from agentjob_runtime.plan.model import (
        validate_implementation_plan as validate_runtime_plan,
    )
    from agentjob_runtime.records.canonical import content_sha256, load_structured
    from agentjob_runtime.security import contains_secret
    from agentjob_runtime.validation.schema import format_issues, validate_instance
    from offline_control import (
        REASON_CODES,
        build_selection_proof,
        diff_plans,
        redact_record,
        validate_control_set,
        validate_record,
    )
except ImportError as error:  # pragma: no cover - exercised by installed-package checks.
    raise SystemExit(
        "planctl requires the sibling agentjob-control package; "
        "install implementation-plan-goal through dependency resolution"
    ) from error


PLAN_SCHEMA = SKILL_ROOT / "schemas" / "implementation-plan.schema.json"
ENVELOPE_SCHEMA = SKILL_ROOT / "schemas" / "plan-task-envelope.schema.json"
ENVELOPE_SCHEMAS = {
    "sys4ai.plan-task-envelope.v1": ENVELOPE_SCHEMA,
    "sys4ai.plan-task-envelope.v2": (
        SKILL_ROOT / "schemas" / "plan-task-envelope-v2.schema.json"
    ),
}
NORMALIZATION_SCHEMA = SKILL_ROOT / "schemas" / "normalization-report.schema.json"
TERMINAL_TASK_STATUSES = frozenset({"completed", "superseded"})
SOURCE_CLASSES = (
    "structured_plan",
    "partial_plan",
    "task_list",
    "phase_outline",
    "requirements",
    "prose",
    "mixed_source",
)
SOURCE_AUTHORITIES = (
    "accepted",
    "supplemental",
    "advisory",
    "historical",
    "unknown",
)
CLASSIFICATION_RANK = {
    "structured_plan": 0,
    "partial_plan": 1,
    "task_list": 2,
    "phase_outline": 3,
    "requirements": 4,
    "prose": 5,
}
NORMALIZATION_CONTRACT = {
    "protocol": "sys4ai.plan-normalization-policy.v1",
    "classification_order": list(SOURCE_CLASSES),
    "preservation_before_synthesis": True,
    "dependency_inference_from_order": False,
    "generated_content_is_authority": False,
    "sizing_results": [
        "ready",
        "split_required",
        "blocked",
        "human_gate_required",
    ],
}
NORMALIZATION_CONTRACT_SHA256 = content_sha256(NORMALIZATION_CONTRACT)
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
PHASE_LINE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:phase|milestone)\s*(?:[-_:]|\d|\b)",
    re.IGNORECASE,
)
TASK_LINE = re.compile(
    r"^\s*(?:[-*+]\s+(?:\[[ xX]\]\s*)?|\d+[.)]\s+)\S+"
)
REQUIREMENT_LINE = re.compile(
    r"\b(?:must|shall|required?|requirement|acceptance criterion|user stor(?:y|ies))\b",
    re.IGNORECASE,
)


def _stable_id(prefix: str, *identity: Any) -> str:
    digest = content_sha256(list(identity))[:16].upper()
    return f"{prefix}-{digest}"


def _valid_id(value: Any) -> bool:
    return isinstance(value, str) and bool(ID_PATTERN.fullmatch(value))


def _as_nonempty_strings(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip() and item.strip() not in result:
            result.append(item.strip())
    return result


def _item_text(value: Any, *, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, Mapping):
        for key in ("title", "name", "objective", "description", "text", "goal"):
            item = value.get(key)
            if isinstance(item, str) and item.strip():
                return item.strip()
    return fallback


def _classify_text(text: str) -> tuple[str, list[str]]:
    lines = [line for line in text.splitlines() if line.strip()]
    phase_lines = [line for line in lines if PHASE_LINE.search(line)]
    task_lines = [line for line in lines if TASK_LINE.search(line)]
    requirement_lines = [line for line in lines if REQUIREMENT_LINE.search(line)]
    if len(phase_lines) >= 2:
        return (
            "phase_outline",
            ["Two or more explicit phase or milestone headings are present."],
        )
    if len(task_lines) >= 2:
        return (
            "task_list",
            ["Two or more explicit actionable list items are present."],
        )
    if len(requirement_lines) >= 2:
        return (
            "requirements",
            ["Two or more explicit requirement or acceptance statements are present."],
        )
    return (
        "prose",
        ["No reliable multi-task, phase, requirement, or canonical plan structure is present."],
    )


def classify_source(value: Any, *, text: str) -> tuple[str, list[str]]:
    """Classify one source from observable structure without assigning authority."""

    if isinstance(value, Mapping):
        if value.get("schema_version") in {
            "sys4ai.implementation-plan.v1",
            "sys4ai.implementation-plan.v2",
        } and not validate_plan(value):
            return (
                "structured_plan",
                ["The source is a valid canonical implementation plan with stable task boundaries."],
            )
        phases = value.get("phases")
        tasks = value.get("tasks")
        requirements = value.get("requirements")
        if isinstance(requirements, list) and requirements:
            return (
                "requirements",
                ["An explicit non-empty requirements collection is present without an accepted implementation sequence."],
            )
        if isinstance(phases, list) and phases and not (
            isinstance(tasks, list) and tasks
        ):
            return (
                "phase_outline",
                ["Ordered phase or milestone structure is present without an executable task set."],
            )
        plan_markers = {
            "schema_version",
            "plan_id",
            "title",
            "objective",
            "acceptance",
            "repository_binding",
            "required_scope",
            "phases",
        }.intersection(value)
        if isinstance(tasks, list) and tasks and not plan_markers:
            if len(tasks) >= 2:
                return (
                    "task_list",
                    ["Two or more actionable task entries are present without a reliable phase model."],
                )
            return (
                "prose",
                ["One isolated work item is present without accepted plan structure."],
            )
        if plan_markers and (
            isinstance(tasks, list) or isinstance(phases, list)
        ):
            return (
                "partial_plan",
                ["Recognizable plan structure is present but the canonical plan contract is incomplete."],
            )
        return _classify_text(text)
    if isinstance(value, list):
        if len(value) >= 2:
            return (
                "task_list",
                ["Two or more ordered actionable source items are present."],
            )
        return (
            "prose",
            ["The source contains fewer than two structured work items."],
        )
    return _classify_text(text)


def _read_source(
    source_root: Path,
    value: str,
    *,
    authority: str,
    precedence: int | None,
) -> dict[str, Any]:
    if precedence is not None and precedence < 0:
        raise RecordValidationError(
            "source precedence must be a non-negative integer",
            details={"reason_code": "source.precedence_invalid"},
        )
    path, normalized = resolve_project_relative(
        source_root,
        value,
        label="source path",
        allow_directory_rule=False,
    )
    if not path.is_file():
        raise RecordValidationError(f"source path is not a regular file: {normalized.relative}")
    if path.stat().st_nlink != 1:
        raise SecurityError(
            f"source path has an unsafe hard-link count: {normalized.relative}",
            details={"reason_code": "path.hardlink", "path": normalized.relative},
        )
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RecordValidationError(
            f"source must be valid UTF-8: {normalized.relative}"
        ) from error
    if contains_secret(text):
        raise SecurityError(
            f"source appears to contain a secret: {normalized.relative}",
            details={"reason_code": "security.secret_detected"},
        )
    suffix = path.suffix.lower()
    media_type = (
        "application/json"
        if suffix == ".json"
        else "application/yaml"
        if suffix in {".yaml", ".yml"}
        else "text/plain"
    )
    if suffix in {".json", ".yaml", ".yml"}:
        parsed = load_structured(path)
    else:
        parsed = text
    source_sha256 = hashlib.sha256(raw).hexdigest()
    source_class, evidence = classify_source(parsed, text=text)
    source_id = _stable_id(
        "SOURCE",
        normalized.relative,
        source_sha256,
    )
    return {
        "source_id": source_id,
        "source_sha256": source_sha256,
        "media_type": media_type,
        "source_class": source_class,
        "authority": authority,
        "precedence": precedence,
        "immutable_ref": normalized.relative,
        "classification_evidence": evidence,
        "_value": parsed,
    }


def _expand_option(
    values: list[Any] | None,
    count: int,
    *,
    default: Any,
    option: str,
) -> list[Any]:
    supplied = list(values or [])
    if not supplied:
        return [default for _ in range(count)]
    if len(supplied) == 1:
        return supplied * count
    if len(supplied) != count:
        raise RecordValidationError(
            f"{option} must be supplied once or exactly once per source"
        )
    return supplied


def classify_paths(
    paths: list[str],
    *,
    source_root: Path,
    authorities: list[str] | None = None,
    precedences: list[int] | None = None,
) -> dict[str, Any]:
    authority_values = _expand_option(
        authorities,
        len(paths),
        default="unknown",
        option="--authority",
    )
    precedence_values = _expand_option(
        precedences,
        len(paths),
        default=None,
        option="--precedence",
    )
    sources = [
        _read_source(
            source_root,
            path,
            authority=str(authority_values[index]),
            precedence=precedence_values[index],
        )
        for index, path in enumerate(paths)
    ]
    public_sources = [
        {key: value for key, value in source.items() if not key.startswith("_")}
        for source in sources
    ]
    return {
        "source_set_class": (
            "mixed_source" if len(public_sources) > 1 else public_sources[0]["source_class"]
        ),
        "sources": public_sources,
    }


def _finding(
    code: str,
    severity: str,
    message: str,
    source_ids: list[str],
) -> dict[str, Any]:
    if code not in REASON_CODES:
        raise ValueError(f"uncatalogued planctl reason code: {code}")
    return {
        "code": code,
        "severity": severity,
        "message": message,
        "source_ids": sorted(set(source_ids)),
    }


def _trace(
    output_kind: str,
    output_id: str,
    source_anchor: str,
    *,
    synthesized: bool,
) -> dict[str, Any]:
    return {
        "output_kind": output_kind,
        "output_id": output_id,
        "source_anchors": [source_anchor],
        "transformation": "synthesized" if synthesized else "canonicalized",
        "generated": synthesized,
    }


def _canonical_copy(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def _accepted_conflicts(sources: list[Mapping[str, Any]]) -> list[str]:
    if len(sources) < 2:
        return []
    conflicts: list[str] = []
    keys = (
        "plan_id",
        "title",
        "objective",
        "acceptance",
        "repository_binding",
        "required_scope",
    )
    for key in keys:
        values = {
            content_sha256(source["_value"][key])
            for source in sources
            if isinstance(source.get("_value"), Mapping)
            and source["_value"].get(key) not in (None, "", [], {})
        }
        if len(values) > 1:
            conflicts.append(key)

    tasks_by_id: dict[str, set[str]] = {}
    phases_by_id: dict[str, set[str]] = {}
    for source in sources:
        value = source.get("_value")
        if not isinstance(value, Mapping):
            continue
        if isinstance(value.get("tasks"), list):
            for task in value["tasks"]:
                if not isinstance(task, Mapping) or not _valid_id(task.get("task_id")):
                    continue
                tasks_by_id.setdefault(str(task["task_id"]), set()).add(
                    content_sha256(task)
                )
        if isinstance(value.get("phases"), list):
            for phase in value["phases"]:
                if not isinstance(phase, Mapping) or not _valid_id(
                    phase.get("phase_id")
                ):
                    continue
                phases_by_id.setdefault(str(phase["phase_id"]), set()).add(
                    content_sha256(phase)
                )
    conflicts.extend(
        f"task:{task_id}"
        for task_id, hashes in sorted(tasks_by_id.items())
        if len(hashes) > 1
    )
    conflicts.extend(
        f"phase:{phase_id}"
        for phase_id, hashes in sorted(phases_by_id.items())
        if len(hashes) > 1
    )
    for collection, identity_key in (("phases", "phase_id"), ("tasks", "task_id")):
        orders = {
            tuple(
                str(item.get(identity_key))
                if isinstance(item, Mapping) and _valid_id(item.get(identity_key))
                else content_sha256(item)
                for item in source["_value"][collection]
            )
            for source in sources
            if isinstance(source.get("_value"), Mapping)
            and isinstance(source["_value"].get(collection), list)
            and source["_value"][collection]
        }
        if len(orders) > 1:
            conflicts.append(f"{collection}_order_or_scope")
    return conflicts


def _dependency_ids(value: Any) -> tuple[list[str], bool]:
    if value is None:
        return [], False
    if not isinstance(value, list):
        return [], True
    result: list[str] = []
    invalid = False
    for item in value:
        if not _valid_id(item) or item in result:
            invalid = True
            continue
        result.append(str(item))
    return result, invalid


def _task_body(
    *,
    task_id: str,
    phase_id: str,
    title: str,
    objective: str,
    depends_on: list[str],
    acceptance_criteria: list[str],
    validation_refs: list[str],
) -> dict[str, Any]:
    body = {
        "task_id": task_id,
        "phase_id": phase_id,
        "title": title,
        "objective": objective,
        "depends_on": depends_on,
        "acceptance_criteria": acceptance_criteria,
        "validation_refs": validation_refs,
        "execution_budget": {
            "one_task_per_discussion": True,
            "max_continue_invocations": 1,
            "max_agentjobs": 1,
            "same_task_successors": 0,
        },
        "extensions": {},
    }
    return {
        "task_id": task_id,
        "task_sha256": content_sha256(body),
        **{key: value for key, value in body.items() if key != "task_id"},
    }


def _normalize_task(
    item: Any,
    *,
    index: int,
    phase_id: str,
    source: Mapping[str, Any],
    source_anchor: str,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    fallback = f"Task {index + 1}"
    title = _item_text(item, fallback=fallback)
    mapping = item if isinstance(item, Mapping) else {}
    objective = _item_text(
        mapping.get("objective") or mapping.get("description") or item,
        fallback=title,
    )
    supplied_id = mapping.get("task_id")
    task_id = (
        str(supplied_id)
        if _valid_id(supplied_id)
        else _stable_id("TASK", source["source_id"], source_anchor, title)
    )
    dependencies, dependencies_invalid = _dependency_ids(mapping.get("depends_on"))
    findings = (
        [
            _finding(
                "plan.dependency_invalid",
                "blocking",
                f"Task {task_id!r} has a malformed or duplicate dependency entry.",
                [source["source_id"]],
            )
        ]
        if dependencies_invalid
        else []
    )
    acceptance = (
        _as_nonempty_strings(mapping.get("acceptance_criteria"))
        or _as_nonempty_strings(mapping.get("acceptance"))
        or ["<ACCEPTANCE_CRITERION>"]
    )
    validation_refs = (
        _as_nonempty_strings(mapping.get("validation_refs"))
        or ["<VALIDATION_COMMAND>"]
    )
    explicit_outcomes = mapping.get("outcomes")
    tasks: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    if isinstance(explicit_outcomes, list) and len(explicit_outcomes) >= 2:
        replacement_ids = [
            _stable_id(
                "TASK",
                task_id,
                f"outcome:{outcome_index}",
                _item_text(outcome, fallback=f"Outcome {outcome_index + 1}"),
            )
            for outcome_index, outcome in enumerate(explicit_outcomes)
        ]
        for outcome_index, outcome in enumerate(explicit_outcomes):
            outcome_title = _item_text(
                outcome,
                fallback=f"{title} outcome {outcome_index + 1}",
            )
            outcome_mapping = outcome if isinstance(outcome, Mapping) else {}
            outcome_acceptance = (
                _as_nonempty_strings(outcome_mapping.get("acceptance_criteria"))
                or ["<ACCEPTANCE_CRITERION>"]
            )
            replacement = _task_body(
                task_id=replacement_ids[outcome_index],
                phase_id=phase_id,
                title=outcome_title,
                objective=_item_text(
                    outcome_mapping.get("objective") or outcome,
                    fallback=outcome_title,
                ),
                depends_on=dependencies,
                acceptance_criteria=outcome_acceptance,
                validation_refs=(
                    _as_nonempty_strings(outcome_mapping.get("validation_refs"))
                    or validation_refs
                ),
            )
            tasks.append(replacement)
            traces.append(
                _trace(
                    "task",
                    replacement["task_id"],
                    f"{source_anchor}/outcomes/{outcome_index}",
                    synthesized=True,
                )
            )
        sizing = [
            {
                "task_id": task_id,
                "result": "split_required",
                "evidence_refs": [source["immutable_ref"]],
                "replacement_task_ids": replacement_ids,
            }
        ]
        return tasks, traces, sizing, findings

    synthesized = any(
        (
            not _valid_id(supplied_id),
            not isinstance(mapping.get("objective"), str),
            not _as_nonempty_strings(mapping.get("acceptance_criteria")),
            not _as_nonempty_strings(mapping.get("validation_refs")),
        )
    )
    task = _task_body(
        task_id=task_id,
        phase_id=phase_id,
        title=title,
        objective=objective,
        depends_on=dependencies,
        acceptance_criteria=acceptance,
        validation_refs=validation_refs,
    )
    tasks.append(task)
    traces.append(
        _trace(
            "task",
            task_id,
            source_anchor,
            synthesized=synthesized,
        )
    )
    sizing = [
        {
            "task_id": task_id,
            "result": "ready",
            "evidence_refs": [source["immutable_ref"]],
            "replacement_task_ids": [],
        }
    ]
    return tasks, traces, sizing, findings


def _build_candidate(
    source: Mapping[str, Any],
    *,
    source_set_sha256: str,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    value = source["_value"]
    source_anchor = source["source_id"]
    findings: list[dict[str, Any]] = []
    if isinstance(value, Mapping) and value.get("schema_version") in {
        "sys4ai.implementation-plan.v1",
        "sys4ai.implementation-plan.v2",
    } and not validate_plan(value):
        candidate = _canonical_copy(value)
        traces = [
            _trace(
                "plan",
                str(candidate["plan_id"]),
                f"{source_anchor}#",
                synthesized=False,
            )
        ]
        for phase_index, phase in enumerate(candidate.get("phases", [])):
            traces.append(
                _trace(
                    "phase",
                    str(phase["phase_id"]),
                    f"{source_anchor}#/phases/{phase_index}",
                    synthesized=False,
                )
            )
        sizing = []
        for task_index, task in enumerate(candidate["tasks"]):
            traces.append(
                _trace(
                    "task",
                    str(task["task_id"]),
                    f"{source_anchor}#/tasks/{task_index}",
                    synthesized=False,
                )
            )
            sizing.append(
                {
                    "task_id": str(task["task_id"]),
                    "result": "ready",
                    "evidence_refs": [source["immutable_ref"]],
                    "replacement_task_ids": [],
                }
            )
        return candidate, traces, sizing, findings

    mapping = value if isinstance(value, Mapping) else {}
    acceptance = mapping.get("acceptance")
    repository_binding = mapping.get("repository_binding")
    if not isinstance(acceptance, Mapping) or acceptance.get("status") != "accepted":
        findings.append(
            _finding(
                "plan.authority_missing",
                "human_gate",
                "A canonical candidate requires preserved accepted plan authority.",
                [source["source_id"]],
            )
        )
    if not isinstance(repository_binding, Mapping):
        findings.append(
            _finding(
                "plan.repository_binding_missing",
                "human_gate",
                "A canonical candidate requires an explicit repository binding.",
                [source["source_id"]],
            )
        )
    if findings:
        plan_id = (
            str(mapping["plan_id"])
            if _valid_id(mapping.get("plan_id"))
            else _stable_id("PLAN", source_set_sha256)
        )
        placeholder_task = _stable_id("TASK", source_set_sha256, "deferred")
        return (
            None,
            [
                {
                    "output_kind": "plan",
                    "output_id": plan_id,
                    "source_anchors": [f"{source_anchor}#"],
                    "transformation": "deferred",
                    "generated": True,
                }
            ],
            [
                {
                    "task_id": placeholder_task,
                    "result": "human_gate_required",
                    "evidence_refs": [source["immutable_ref"]],
                    "replacement_task_ids": [],
                }
            ],
            findings,
        )

    plan_id = (
        str(mapping["plan_id"])
        if _valid_id(mapping.get("plan_id"))
        else _stable_id("PLAN", source_set_sha256)
    )
    title = _item_text(mapping.get("title"), fallback=f"Implementation plan {plan_id}")
    objective = _item_text(
        mapping.get("objective") or mapping.get("goal"),
        fallback=f"Deliver and verify {title}.",
    )
    raw_phases = mapping.get("phases")
    raw_tasks = mapping.get("tasks")
    requirement_route = isinstance(mapping.get("requirements"), list)
    if requirement_route:
        raw_tasks = mapping["requirements"]
    if isinstance(value, list):
        raw_tasks = value
    elif isinstance(value, str):
        raw_tasks = [value]

    phase_inputs = list(raw_phases) if isinstance(raw_phases, list) and raw_phases else []
    phase_outline_route = bool(phase_inputs) and not (
        isinstance(raw_tasks, list) and raw_tasks
    )
    phases: list[dict[str, Any]] = []
    phase_traces: list[dict[str, Any]] = []
    source_phase_task_ids: dict[str, list[str]] = {}
    if phase_inputs:
        for phase_index, phase_value in enumerate(phase_inputs):
            phase_mapping = phase_value if isinstance(phase_value, Mapping) else {}
            phase_title = _item_text(
                phase_value,
                fallback=f"Phase {phase_index + 1}",
            )
            supplied_phase_id = phase_mapping.get("phase_id")
            phase_id = (
                str(supplied_phase_id)
                if _valid_id(supplied_phase_id)
                else _stable_id(
                    "PHASE",
                    source["source_id"],
                    phase_index,
                    phase_title,
                )
            )
            phase_dependencies, phase_dependencies_invalid = _dependency_ids(
                phase_mapping.get("depends_on")
            )
            supplied_phase_tasks, phase_tasks_invalid = _dependency_ids(
                phase_mapping.get("task_ids")
            )
            if phase_dependencies_invalid:
                findings.append(
                    _finding(
                        "plan.dependency_invalid",
                        "blocking",
                        f"Phase {phase_id!r} has a malformed or duplicate dependency entry.",
                        [source["source_id"]],
                    )
                )
            if phase_tasks_invalid:
                findings.append(
                    _finding(
                        "phase.task_reference_invalid",
                        "blocking",
                        f"Phase {phase_id!r} has a malformed or duplicate task reference.",
                        [source["source_id"]],
                    )
                )
            source_phase_task_ids[phase_id] = supplied_phase_tasks
            phases.append(
                {
                    "phase_id": phase_id,
                    "title": phase_title,
                    "depends_on": phase_dependencies,
                    "task_ids": [],
                    "acceptance_criteria": (
                        _as_nonempty_strings(phase_mapping.get("acceptance_criteria"))
                        or ["<PHASE_ACCEPTANCE_CRITERION>"]
                    ),
                    "extensions": {},
                }
            )
            phase_traces.append(
                _trace(
                    "phase",
                    phase_id,
                    f"{source_anchor}#/phases/{phase_index}",
                    synthesized=(
                        not _valid_id(supplied_phase_id)
                        or not _as_nonempty_strings(
                            phase_mapping.get("acceptance_criteria")
                        )
                    ),
                )
            )
    else:
        phase_id = _stable_id("PHASE", source["source_id"], "default")
        phases.append(
            {
                "phase_id": phase_id,
                "title": "Execute and verify the accepted work",
                "depends_on": [],
                "task_ids": [],
                "acceptance_criteria": ["<PHASE_ACCEPTANCE_CRITERION>"],
                "extensions": {},
            }
        )
        phase_traces.append(
            _trace(
                "phase",
                phase_id,
                f"{source_anchor}#",
                synthesized=True,
            )
        )

    if phase_outline_route:
        raw_tasks = [
            {
                "title": f"Deliver {phase['title']}",
                "objective": _item_text(
                    phase_inputs[index],
                    fallback=f"Deliver and verify {phase['title']}.",
                ),
                "_phase_index": index,
            }
            for index, phase in enumerate(phases)
        ]
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raw_tasks = [
            {
                "title": title,
                "objective": objective,
            }
        ]

    tasks: list[dict[str, Any]] = []
    task_traces: list[dict[str, Any]] = []
    sizing: list[dict[str, Any]] = []
    for task_index, task_value in enumerate(raw_tasks):
        task_mapping = task_value if isinstance(task_value, Mapping) else {}
        phase_index = task_mapping.get("_phase_index")
        if not isinstance(phase_index, int) or not (0 <= phase_index < len(phases)):
            explicit_phase_id = task_mapping.get("phase_id")
            supplied_task_id = task_mapping.get("task_id")
            matching_phase_indexes = [
                index
                for index, phase in enumerate(phases)
                if _valid_id(supplied_task_id)
                and supplied_task_id
                in source_phase_task_ids.get(str(phase["phase_id"]), [])
            ]
            explicit_index = next(
                (
                    index
                    for index, phase in enumerate(phases)
                    if explicit_phase_id == phase["phase_id"]
                ),
                None,
            )
            if explicit_phase_id is not None and explicit_index is None:
                findings.append(
                    _finding(
                        "task.phase_reference_invalid",
                        "blocking",
                        f"Task {supplied_task_id!r} names an unknown phase {explicit_phase_id!r}.",
                        [source["source_id"]],
                    )
                )
            if len(matching_phase_indexes) > 1:
                findings.append(
                    _finding(
                        "task.phase_membership_conflict",
                        "blocking",
                        f"Task {supplied_task_id!r} appears in more than one source phase.",
                        [source["source_id"]],
                    )
                )
            phase_index = (
                explicit_index
                if explicit_index is not None
                else matching_phase_indexes[0]
                if len(matching_phase_indexes) == 1
                else 0
            )
        anchor_name = "requirements" if requirement_route else "tasks"
        normalized_tasks, traces, task_sizing, task_findings = _normalize_task(
            task_value,
            index=task_index,
            phase_id=phases[phase_index]["phase_id"],
            source=source,
            source_anchor=f"{source_anchor}#/{anchor_name}/{task_index}",
        )
        tasks.extend(normalized_tasks)
        task_traces.extend(traces)
        sizing.extend(task_sizing)
        findings.extend(task_findings)
        phases[phase_index]["task_ids"].extend(
            task["task_id"] for task in normalized_tasks
        )

    normalized_task_ids = {task["task_id"] for task in tasks}
    unknown_phase_task_ids = sorted(
        {
            task_id
            for task_ids in source_phase_task_ids.values()
            for task_id in task_ids
            if task_id not in normalized_task_ids
        }
    )
    if unknown_phase_task_ids:
        findings.append(
            _finding(
                "phase.task_reference_invalid",
                "blocking",
                f"Source phases reference unknown tasks: {unknown_phase_task_ids!r}.",
                [source["source_id"]],
            )
        )

    duplicate_ids = sorted(
        {
            task["task_id"]
            for task in tasks
            if sum(other["task_id"] == task["task_id"] for other in tasks) > 1
        }
    )
    if duplicate_ids:
        findings.append(
            _finding(
                "task.duplicate_id",
                "blocking",
                f"Accepted source repeats task identities: {duplicate_ids!r}.",
                [source["source_id"]],
            )
        )
    empty_phases = [phase["phase_id"] for phase in phases if not phase["task_ids"]]
    if empty_phases:
        findings.append(
            _finding(
                "phase.task_derivation_missing",
                "blocking",
                f"No task could be derived for phases: {empty_phases!r}.",
                [source["source_id"]],
            )
        )

    required_scope = mapping.get("required_scope")
    excluded_phase_ids = (
        _as_nonempty_strings(required_scope.get("excluded_phase_ids"))
        if isinstance(required_scope, Mapping)
        else []
    )
    excluded_task_ids = (
        _as_nonempty_strings(required_scope.get("excluded_task_ids"))
        if isinstance(required_scope, Mapping)
        else []
    )
    candidate = {
        "schema_version": "sys4ai.implementation-plan.v2",
        "plan_id": plan_id,
        "title": title,
        "objective": objective,
        "acceptance": _canonical_copy(acceptance),
        "repository_binding": _canonical_copy(repository_binding),
        "serial_execution": True,
        "required_scope": {
            "phase_ids": [phase["phase_id"] for phase in phases],
            "task_ids": [task["task_id"] for task in tasks],
            "excluded_phase_ids": excluded_phase_ids,
            "excluded_task_ids": excluded_task_ids,
        },
        "phases": phases,
        "tasks": tasks,
        "extensions": {},
    }
    plan_findings = validate_plan(candidate)
    if plan_findings:
        findings.append(
            _finding(
                "plan.validation_failed",
                "blocking",
                "The normalized candidate fails canonical validation: "
                + "; ".join(plan_findings),
                [source["source_id"]],
            )
        )
    traces = [
        _trace(
            "plan",
            plan_id,
            f"{source_anchor}#",
            synthesized=(
                not _valid_id(mapping.get("plan_id"))
                or not isinstance(mapping.get("objective"), str)
            ),
        ),
        *phase_traces,
        *task_traces,
    ]
    return candidate, traces, sizing, findings


def _normalization_report(
    *,
    sources: list[Mapping[str, Any]],
    source_set_sha256: str,
    plan_id: str,
    candidate: Mapping[str, Any] | None,
    findings: list[dict[str, Any]],
    traces: list[dict[str, Any]],
    sizing: list[dict[str, Any]],
    canonicalization_only: bool,
) -> dict[str, Any]:
    status = (
        "blocked"
        if any(item["severity"] == "blocking" for item in findings)
        else "human_gate_required"
        if any(item["severity"] == "human_gate" for item in findings)
        else "candidate"
    )
    candidate_hash = content_sha256(candidate) if candidate is not None and status == "candidate" else None
    public_sources = [
        {key: value for key, value in source.items() if not key.startswith("_")}
        for source in sources
    ]
    report = {
        "schema_version": "sys4ai.plan-normalization-report.v1",
        "report_id": _stable_id(
            "PNR",
            source_set_sha256,
            NORMALIZATION_CONTRACT_SHA256,
            candidate_hash,
            status,
        ),
        "plan_id": plan_id,
        "source_set_sha256": source_set_sha256,
        "normalization_contract_sha256": NORMALIZATION_CONTRACT_SHA256,
        "sources": public_sources,
        "candidate_plan_sha256": candidate_hash,
        "status": status,
        "findings": sorted(findings, key=lambda item: (item["code"], item["message"])),
        "traceability": traces,
        "task_sizing": sizing,
        "canonicalization_only": canonicalization_only and status == "candidate",
        "hash_basis": "canonical_json_without_report_content_sha256",
        "report_content_sha256": "0" * 64,
        "finalized": True,
        "extensions": {},
    }
    report["report_content_sha256"] = content_sha256(
        {key: value for key, value in report.items() if key != "report_content_sha256"}
    )
    issues = validate_instance(report, NORMALIZATION_SCHEMA)
    if issues:
        raise RecordValidationError(
            "normalizer produced an invalid normalization report: "
            + "; ".join(format_issues(issues).splitlines())
        )
    return report


def normalize_paths(
    paths: list[str],
    *,
    source_root: Path,
    authorities: list[str] | None = None,
    precedences: list[int] | None = None,
) -> dict[str, Any]:
    authority_values = _expand_option(
        authorities,
        len(paths),
        default="unknown",
        option="--authority",
    )
    if len(paths) > 1 and not precedences:
        raise RecordValidationError(
            "--precedence is required for every multi-source normalization"
        )
    precedence_values = _expand_option(
        precedences,
        len(paths),
        default=0,
        option="--precedence",
    )
    sources = [
        _read_source(
            source_root,
            path,
            authority=str(authority_values[index]),
            precedence=int(precedence_values[index]),
        )
        for index, path in enumerate(paths)
    ]
    public_sources = [
        {key: value for key, value in source.items() if not key.startswith("_")}
        for source in sources
    ]
    source_set_sha256 = content_sha256(public_sources)
    accepted = [source for source in sources if source["authority"] == "accepted"]
    findings: list[dict[str, Any]] = []
    if not accepted:
        findings.append(
            _finding(
                "plan.authority_missing",
                "human_gate",
                "No source is explicitly accepted plan authority.",
                [source["source_id"] for source in sources],
            )
        )
        controlling = min(
            sources,
            key=lambda source: (
                source["precedence"],
                CLASSIFICATION_RANK[source["source_class"]],
                source["immutable_ref"],
            ),
        )
    else:
        minimum_precedence = min(source["precedence"] for source in accepted)
        controlling_set = [
            source for source in accepted if source["precedence"] == minimum_precedence
        ]
        conflict_fields = _accepted_conflicts(controlling_set)
        if conflict_fields:
            findings.append(
                _finding(
                    "normalization.accepted_source_conflict",
                    "blocking",
                    "Equal-precedence accepted sources conflict on: "
                    + ", ".join(conflict_fields),
                    [source["source_id"] for source in controlling_set],
                )
            )
        controlling = min(
            controlling_set,
            key=lambda source: (
                CLASSIFICATION_RANK[source["source_class"]],
                source["immutable_ref"],
            ),
        )

    if findings:
        candidate = None
        plan_id = (
            str(controlling["_value"]["plan_id"])
            if isinstance(controlling["_value"], Mapping)
            and _valid_id(controlling["_value"].get("plan_id"))
            else _stable_id("PLAN", source_set_sha256)
        )
        placeholder_task = _stable_id("TASK", source_set_sha256, "blocked")
        traces = [
            {
                "output_kind": "plan",
                "output_id": plan_id,
                "source_anchors": [f"{controlling['source_id']}#"],
                "transformation": "deferred",
                "generated": True,
            }
        ]
        sizing = [
            {
                "task_id": placeholder_task,
                "result": (
                    "blocked"
                    if any(item["severity"] == "blocking" for item in findings)
                    else "human_gate_required"
                ),
                "evidence_refs": [source["immutable_ref"] for source in sources],
                "replacement_task_ids": [],
            }
        ]
        canonicalization_only = False
    else:
        candidate, traces, sizing, candidate_findings = _build_candidate(
            controlling,
            source_set_sha256=source_set_sha256,
        )
        findings.extend(candidate_findings)
        plan_id = (
            str(candidate["plan_id"])
            if candidate is not None
            else (
                str(controlling["_value"]["plan_id"])
                if isinstance(controlling["_value"], Mapping)
                and _valid_id(controlling["_value"].get("plan_id"))
                else _stable_id("PLAN", source_set_sha256)
            )
        )
        canonicalization_only = (
            candidate is not None
            and controlling["source_class"] == "structured_plan"
            and candidate == controlling["_value"]
        )
    report = _normalization_report(
        sources=sources,
        source_set_sha256=source_set_sha256,
        plan_id=plan_id,
        candidate=candidate,
        findings=findings,
        traces=traces,
        sizing=sizing,
        canonicalization_only=canonicalization_only,
    )
    return {
        "source_set_class": "mixed_source" if len(sources) > 1 else sources[0]["source_class"],
        "candidate_plan": candidate if report["status"] == "candidate" else None,
        "normalization_report": report,
    }


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_record(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": path.as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "value": json.loads(raw.decode("utf-8")),
    }


def validate_plan(plan: Any) -> list[str]:
    return validate_runtime_plan(plan, schema_path=PLAN_SCHEMA)


def select_next(plan: Mapping[str, Any]) -> dict[str, Any] | None:
    if plan.get("schema_version") == "sys4ai.implementation-plan.v2":
        return None
    tasks = plan["tasks"]
    if any(task["status"] == "in_progress" for task in tasks):
        return None
    by_id = {task["task_id"]: task for task in tasks}
    for position, task in enumerate(tasks):
        if task["status"] != "pending":
            continue
        dependencies = task["depends_on"]
        if all(by_id[item]["status"] in TERMINAL_TASK_STATUSES for item in dependencies):
            return {
                "task_id": task["task_id"],
                "task_sha256": task["task_sha256"],
                "canonical_position": position,
                "dependency_statuses": [
                    {"task_id": item, "status": by_id[item]["status"]}
                    for item in dependencies
                ],
            }
    return None


def _control_records(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "plan": _load_record(args.path),
        "state": _load_record(args.state),
        "receipts": [_load_record(path) for path in args.receipt],
        "amendments": [_load_record(path) for path in args.amendment],
        "supersessions": [_load_record(path) for path in args.supersession],
        "provider_intents": [
            _load_record(path) for path in args.provider_intent
        ],
        "selection_proofs": [
            _load_record(path) for path in args.selection_proof
        ],
    }


def _validate_control_records(
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    records = _control_records(args)
    findings, context = validate_control_set(
        **records,
        skill_root=SKILL_ROOT,
        plan_validator=validate_plan,
        repository_fingerprint=args.repository_fingerprint,
    )
    return findings, context, records


def _structured_plan_findings(
    findings: list[str],
    *,
    record_type: str = "implementation_plan",
) -> list[dict[str, Any]]:
    return [
        {
            "code": "record.schema_invalid",
            "severity": "blocking",
            "message": finding,
            "path": "$",
            "record_type": record_type,
        }
        for finding in findings
    ]


def _input_error(command: str, error: Exception) -> dict[str, Any]:
    return _result(
        command,
        "invalid",
        findings=[
            {
                "code": "input.load_failed",
                "severity": "blocking",
                "message": str(error),
                "path": "$",
                "record_type": None,
            }
        ],
    )


def _result(command: str, status: str, **values: Any) -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.planctl-result.v1",
        "command": command,
        "status": status,
        **values,
    }


def _emit(value: Mapping[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, sort_keys=True, separators=(",", ":")))
        return
    print(f"{value['command']}: {value['status']}")
    for finding in value.get("findings", []):
        print(
            f"- {finding['code']}: {finding['message']}"
            if isinstance(finding, Mapping)
            else f"- {finding}"
        )
    if value.get("selection") is not None:
        print(f"- selected: {value['selection']['task_id']}")
    for source in value.get("sources", []):
        print(f"- {source['immutable_ref']}: {source['source_class']}")
    if value.get("candidate_plan") is not None:
        print(f"- candidate: {value['candidate_plan']['plan_id']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "validate-envelope", "validate-record", "redact"):
        child = subparsers.add_parser(command)
        child.add_argument("path", type=Path)
        child.add_argument("--json", action="store_true")
    child = subparsers.add_parser("select-next")
    child.add_argument("path", type=Path)
    child.add_argument(
        "--state",
        type=Path,
        help="Separate v2 plan state for revision-bound offline selection.",
    )
    child.add_argument(
        "--prior-journal-sha256",
        help="Required journal head for v2 selection-proof generation.",
    )
    child.add_argument("--repository-fingerprint")
    for option in (
        "receipt",
        "amendment",
        "supersession",
        "provider-intent",
        "selection-proof",
    ):
        child.add_argument(f"--{option}", action="append", type=Path, default=[])
    child.add_argument("--json", action="store_true")
    child = subparsers.add_parser("validate-state")
    child.add_argument("path", type=Path, help="Immutable plan path.")
    child.add_argument("state", type=Path, help="Separate plan-state path.")
    child.add_argument("--repository-fingerprint")
    for option in (
        "receipt",
        "amendment",
        "supersession",
        "provider-intent",
        "selection-proof",
    ):
        child.add_argument(f"--{option}", action="append", type=Path, default=[])
    child.add_argument("--json", action="store_true")
    child = subparsers.add_parser("diff")
    child.add_argument("prior", type=Path)
    child.add_argument("current", type=Path)
    child.add_argument("--json", action="store_true")
    child = subparsers.add_parser("reason-codes")
    child.add_argument("--json", action="store_true")
    for command in ("classify", "normalize"):
        child = subparsers.add_parser(command)
        child.add_argument("paths", nargs="+")
        child.add_argument(
            "--source-root",
            type=Path,
            default=Path("."),
            help="Root used to resolve and contain project-relative source paths.",
        )
        child.add_argument(
            "--authority",
            action="append",
            choices=SOURCE_AUTHORITIES,
            help="Supply once for all sources or once per source.",
        )
        child.add_argument(
            "--precedence",
            action="append",
            type=int,
            help="Supply once for all sources or once per source; lower values control.",
        )
        child.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "reason-codes":
        result = _result(
            args.command,
            "catalogued",
            findings=[],
            reason_codes=[
                {"code": code, **REASON_CODES[code]}
                for code in sorted(REASON_CODES)
            ],
        )
        _emit(result, as_json=args.json)
        return 0

    if args.command == "redact":
        try:
            wrapped = _load_record(args.path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            result = _input_error(args.command, error)
            _emit(result, as_json=args.json)
            return 2
        redacted, redacted_paths = redact_record(wrapped["value"])
        reason_code = "redaction.applied" if redacted_paths else "redaction.none"
        result = _result(
            args.command,
            "redacted" if redacted_paths else "unchanged",
            findings=[],
            reason_code=reason_code,
            source_sha256=wrapped["sha256"],
            redacted_paths=redacted_paths,
            redacted_record=redacted,
        )
        _emit(result, as_json=args.json)
        return 0

    if args.command == "validate-record":
        try:
            wrapped = _load_record(args.path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            result = _input_error(args.command, error)
            _emit(result, as_json=args.json)
            return 2
        profile, findings = validate_record(
            wrapped["value"],
            skill_root=SKILL_ROOT,
            plan_validator=validate_plan,
        )
        result = _result(
            args.command,
            "valid" if not findings else "invalid",
            findings=findings,
            record_profile=profile,
            record_sha256=wrapped["sha256"],
        )
        _emit(result, as_json=args.json)
        return 0 if not findings else 1

    if args.command == "diff":
        try:
            prior = _load_record(args.prior)
            current = _load_record(args.current)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            result = _input_error(args.command, error)
            _emit(result, as_json=args.json)
            return 2
        plan_findings = [
            *_structured_plan_findings(validate_plan(prior["value"])),
            *_structured_plan_findings(validate_plan(current["value"])),
        ]
        if plan_findings:
            result = _result(
                args.command,
                "invalid",
                findings=plan_findings,
                changes=[],
            )
            _emit(result, as_json=args.json)
            return 1
        diff = diff_plans(
            prior["value"],
            current["value"],
            prior_sha256=prior["sha256"],
            current_sha256=current["sha256"],
        )
        result = _result(args.command, diff.pop("status"), **diff)
        _emit(result, as_json=args.json)
        return 1 if result["findings"] else 0

    if args.command == "validate-state":
        try:
            findings, context, _ = _validate_control_records(args)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            result = _input_error(args.command, error)
            _emit(result, as_json=args.json)
            return 2
        result = _result(
            args.command,
            "valid" if not findings else "invalid",
            findings=findings,
            plan_id=context["plan_id"],
            effective_plan_sha256=context["effective_plan_sha256"],
            supersession_graph_sha256=context["supersession_graph_sha256"],
            record_counts=context["record_counts"],
        )
        _emit(result, as_json=args.json)
        return 0 if not findings else 1

    if args.command == "select-next" and args.state is not None:
        try:
            findings, context, records = _validate_control_records(args)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            result = _input_error(args.command, error)
            _emit(result, as_json=args.json)
            return 2
        if findings:
            result = _result(
                args.command,
                "invalid",
                findings=findings,
                selection=None,
                selection_proof=None,
            )
            _emit(result, as_json=args.json)
            return 1
        proof, proof_findings = build_selection_proof(
            plan=records["plan"]["value"],
            state=records["state"]["value"],
            context=context,
            prior_journal_sha256=args.prior_journal_sha256 or "",
            skill_root=SKILL_ROOT,
        )
        if proof_findings or proof is None:
            result = _result(
                args.command,
                "invalid",
                findings=proof_findings,
                selection=None,
                selection_proof=None,
            )
            _emit(result, as_json=args.json)
            return 1
        result = _result(
            args.command,
            str(proof["outcome"]),
            findings=[],
            selection=proof["selected_task"],
            selection_proof=proof,
        )
        _emit(result, as_json=args.json)
        return 0

    if args.command in {"classify", "normalize"}:
        try:
            if args.command == "classify":
                classified = classify_paths(
                    args.paths,
                    source_root=args.source_root,
                    authorities=args.authority,
                    precedences=args.precedence,
                )
                result = _result(
                    args.command,
                    "classified",
                    findings=[],
                    **classified,
                )
                _emit(result, as_json=args.json)
                return 0
            normalized = normalize_paths(
                args.paths,
                source_root=args.source_root,
                authorities=args.authority,
                precedences=args.precedence,
            )
            report = normalized["normalization_report"]
            result = _result(
                args.command,
                str(report["status"]),
                findings=report["findings"],
                **normalized,
            )
            _emit(result, as_json=args.json)
            return 0 if report["status"] == "candidate" else 1
        except (OSError, RecordValidationError, SecurityError, ValueError) as error:
            reason_code = getattr(error, "details", {}).get(
                "reason_code",
                getattr(error, "code", "input.invalid"),
            )
            if reason_code not in REASON_CODES:
                reason_code = "input.invalid"
            result = _result(
                args.command,
                "invalid",
                findings=[
                    {
                        "code": reason_code,
                        "severity": "blocking",
                        "message": str(error),
                        "source_ids": [],
                    }
                ],
            )
            _emit(result, as_json=args.json)
            return 2

    try:
        value = _load_json(args.path)
    except (OSError, json.JSONDecodeError) as error:
        result = _result(args.command, "invalid", findings=[f"input.load $: {error}"])
        _emit(result, as_json=args.json)
        return 2

    if args.command == "validate-envelope":
        schema = (
            ENVELOPE_SCHEMAS.get(str(value.get("schema_version")))
            if isinstance(value, Mapping)
            else None
        )
        if schema is None:
            result = _result(
                args.command,
                "invalid",
                findings=[
                    "record.schema_version_unknown $.schema_version: "
                    "unsupported plan-task envelope version"
                ],
            )
            _emit(result, as_json=args.json)
            return 1
        issues = validate_instance(value, schema)
        findings = format_issues(issues).splitlines() if issues else []
        result = _result(
            args.command,
            "valid" if not findings else "invalid",
            findings=findings,
        )
        _emit(result, as_json=args.json)
        return 0 if not findings else 1

    findings = validate_plan(value)
    if findings:
        result = _result(args.command, "invalid", findings=findings)
        _emit(result, as_json=args.json)
        return 1
    if args.command == "validate":
        result = _result(args.command, "valid", findings=[])
    else:
        selection = select_next(value)
        state_required = value.get("schema_version") == "sys4ai.implementation-plan.v2"
        result = _result(
            args.command,
            (
                "state_required"
                if state_required
                else "selected"
                if selection is not None
                else "no_ready_task"
            ),
            findings=[],
            selection=selection,
        )
    _emit(result, as_json=args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
