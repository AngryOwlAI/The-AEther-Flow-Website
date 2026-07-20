"""Deterministic read-only validation and scheduling for plan-control records."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import validate_instance


TERMINAL_TASK_STATUSES = frozenset({"completed", "superseded"})
ACTIVE_TASK_STATUSES = frozenset({"reserved", "active", "verifying"})
BLOCKED_TASK_STATUSES = frozenset(
    {
        "blocked",
        "replan_required",
        "human_gate_required",
        "validation_failed",
        "invocation_unknown",
        "cancelled",
    }
)
NON_SCHEDULABLE_PHASES = frozenset(
    {
        "recovery_pending",
        "terminal_blocked_no_runnable",
        "terminal_awaiting_human",
        "terminal_validation_failed",
        "terminal_capability_blocked",
        "terminal_corrupt_state",
        "terminal_cancelled",
    }
)

SELECTION_POLICY = {
    "protocol": "sys4ai.plan-selection-policy.v1",
    "canonical_order_only": True,
    "one_active_task_maximum": 1,
    "terminal_dependency_statuses": sorted(TERMINAL_TASK_STATUSES),
    "receipt_required_for_terminal_dependency": True,
    "compare_and_swap_required": True,
    "state_mutation": False,
}
SELECTION_POLICY_SHA256 = content_sha256(SELECTION_POLICY)

REASON_CODES: dict[str, dict[str, str]] = {
    "amendment.chain_invalid": {
        "severity": "blocking",
        "description": "The amendment hash chain does not continue from the supplied base plan.",
    },
    "amendment.identity_mismatch": {
        "severity": "blocking",
        "description": "An amendment names a different plan identity.",
    },
    "amendment.sequence_invalid": {
        "severity": "blocking",
        "description": "Amendment sequence numbers are missing, duplicated, or non-contiguous.",
    },
    "diff.plan_identity_changed": {
        "severity": "blocking",
        "description": "Compared plans do not preserve immutable plan identity.",
    },
    "input.load_failed": {
        "severity": "blocking",
        "description": "A supplied record could not be loaded as JSON.",
    },
    "input.invalid": {
        "severity": "blocking",
        "description": "A supplied command argument or source record is invalid.",
    },
    "normalization.accepted_source_conflict": {
        "severity": "blocking",
        "description": "Equal-precedence accepted sources disagree on controlling content.",
    },
    "path.absolute_forbidden": {
        "severity": "blocking",
        "description": "A protected source path must be project-relative.",
    },
    "path.hardlink": {
        "severity": "blocking",
        "description": "A protected source has an unsafe hard-link count.",
    },
    "path.alias": {
        "severity": "blocking",
        "description": "A protected source path contains a non-canonical alias.",
    },
    "path.control_character": {
        "severity": "blocking",
        "description": "A protected source path contains a control character.",
    },
    "path.directory_rule_forbidden": {
        "severity": "blocking",
        "description": "A protected source file path cannot use directory-rule syntax.",
    },
    "path.glob_forbidden": {
        "severity": "blocking",
        "description": "A protected source file path cannot use a directory glob.",
    },
    "path.glob_unsupported": {
        "severity": "blocking",
        "description": "A protected source path contains unsupported glob syntax.",
    },
    "path.invalid": {
        "severity": "blocking",
        "description": "A protected source path is empty or contains NUL.",
    },
    "path.project_root_forbidden": {
        "severity": "blocking",
        "description": "A protected source path cannot name the project root.",
    },
    "path.symlink": {
        "severity": "blocking",
        "description": "A protected source path traverses a symbolic link.",
    },
    "path.traversal": {
        "severity": "blocking",
        "description": "A protected source path escapes or traverses its project root.",
    },
    "path.unicode_not_nfc": {
        "severity": "blocking",
        "description": "A protected source path is not NFC-normalized.",
    },
    "path.windows_alias": {
        "severity": "blocking",
        "description": "A protected source path has a Windows-specific alias.",
    },
    "path.windows_reserved": {
        "severity": "blocking",
        "description": "A protected source path contains a reserved Windows name.",
    },
    "phase.task_derivation_missing": {
        "severity": "blocking",
        "description": "A normalized phase has no derivable task.",
    },
    "phase.task_reference_invalid": {
        "severity": "blocking",
        "description": "A phase contains an invalid or unknown task reference.",
    },
    "plan.authority_missing": {
        "severity": "human_gate",
        "description": "No source is explicitly accepted plan authority.",
    },
    "plan.dependency_invalid": {
        "severity": "blocking",
        "description": "A normalized phase or task dependency is malformed.",
    },
    "plan.hash_mismatch": {
        "severity": "blocking",
        "description": "Plan-state effective hash does not match the supplied base and amendments.",
    },
    "plan.identity_mismatch": {
        "severity": "blocking",
        "description": "Related records name different plan identities.",
    },
    "plan.repository_binding_missing": {
        "severity": "human_gate",
        "description": "A canonical candidate has no explicit repository binding.",
    },
    "plan.phase_changed": {
        "severity": "warning",
        "description": "A phase definition changed between compared plans.",
    },
    "plan.task_added": {
        "severity": "warning",
        "description": "A task identity was added between compared plans.",
    },
    "plan.task_removed": {
        "severity": "blocking",
        "description": "A task identity was removed between compared plans.",
    },
    "plan.validation_failed": {
        "severity": "blocking",
        "description": "A normalized candidate fails canonical plan validation.",
    },
    "provider.identity_mismatch": {
        "severity": "blocking",
        "description": "A provider intent is not bound to the effective plan, task, or repository.",
    },
    "provider.predecessor_reused": {
        "severity": "blocking",
        "description": "A provider outcome reused the predecessor discussion identity.",
    },
    "receipt.hash_mismatch": {
        "severity": "blocking",
        "description": "A state receipt link does not match the exact supplied receipt bytes.",
    },
    "receipt.identity_mismatch": {
        "severity": "blocking",
        "description": "A task receipt is not bound to the expected plan or task identity.",
    },
    "receipt.missing": {
        "severity": "blocking",
        "description": "A terminal task does not have its linked receipt in the supplied record set.",
    },
    "receipt.execution_mismatch": {
        "severity": "blocking",
        "description": "Receipt relay, execution, or fingerprint evidence disagrees with task lifecycle state.",
    },
    "record.content_hash_mismatch": {
        "severity": "blocking",
        "description": "A finalized record content hash does not match canonical record content.",
    },
    "record.duplicate_identity": {
        "severity": "blocking",
        "description": "Two supplied records reuse one immutable record identity.",
    },
    "record.schema_invalid": {
        "severity": "blocking",
        "description": "A record fails its declared JSON schema.",
    },
    "record.schema_version_unknown": {
        "severity": "blocking",
        "description": "A record does not declare a supported schema version.",
    },
    "redaction.applied": {
        "severity": "info",
        "description": "Sensitive values were replaced by deterministic hashes in an output copy.",
    },
    "redaction.none": {
        "severity": "info",
        "description": "No sensitive values were found in the supplied record.",
    },
    "security.secret_detected": {
        "severity": "blocking",
        "description": "A protected source appears to contain a live secret.",
    },
    "selection.active_task_present": {
        "severity": "blocking",
        "description": "Serial scheduling cannot select another task while one task is active.",
    },
    "selection.dependencies_not_terminal": {
        "severity": "info",
        "description": "No pending task has terminal, receipt-backed effective dependencies.",
    },
    "selection.journal_hash_required": {
        "severity": "blocking",
        "description": "Revision-bound proof generation requires a valid prior journal hash.",
    },
    "selection.no_runnable_task": {
        "severity": "blocking",
        "description": "No active, pending, or completion-candidate task state is runnable.",
    },
    "selection.proof_invalid": {
        "severity": "blocking",
        "description": "Generated or supplied selection proof violates its record contract.",
    },
    "selection.state_not_schedulable": {
        "severity": "blocking",
        "description": "The current recovery or terminal state does not permit task selection.",
    },
    "state.active_task_mismatch": {
        "severity": "blocking",
        "description": "State active task, phase, lease, and lifecycle entries disagree.",
    },
    "state.counter_mismatch": {
        "severity": "blocking",
        "description": "Aggregate plan counters do not equal their task-lifecycle projections.",
    },
    "state.generation_mismatch": {
        "severity": "blocking",
        "description": "State generation does not match the active or latest task generation.",
    },
    "state.phase_mismatch": {
        "severity": "blocking",
        "description": "Plan phase does not agree with task lifecycle outcomes.",
    },
    "state.repository_fingerprint_mismatch": {
        "severity": "blocking",
        "description": "State or lease repository fingerprint differs from direct evidence.",
    },
    "state.task_missing": {
        "severity": "blocking",
        "description": "An immutable or superseding task has no lifecycle state.",
    },
    "state.task_unknown": {
        "severity": "blocking",
        "description": "Lifecycle state contains a task absent from plan or supersession authority.",
    },
    "supersession.identity_mismatch": {
        "severity": "blocking",
        "description": "A supersession does not bind the expected plan or original task.",
    },
    "supersession.replacement_invalid": {
        "severity": "blocking",
        "description": "A replacement task reuses an identity, position, or invalid dependency.",
    },
    "supersession.replacement_cycle": {
        "severity": "blocking",
        "description": "Replacement-task dependencies contain a cycle.",
    },
    "source.precedence_invalid": {
        "severity": "blocking",
        "description": "Source precedence is missing, malformed, or ambiguous.",
    },
    "task.duplicate_id": {
        "severity": "blocking",
        "description": "A normalized task identity is duplicated.",
    },
    "task.hash_drift": {
        "severity": "blocking",
        "description": "The same immutable task identity has different hashes across records.",
    },
    "task.phase_membership_conflict": {
        "severity": "blocking",
        "description": "A normalized task appears in more than one phase.",
    },
    "task.phase_reference_invalid": {
        "severity": "blocking",
        "description": "A normalized task names an unknown phase.",
    },
    "input.load": {
        "severity": "blocking",
        "description": "A legacy plan or envelope input could not be loaded.",
    },
    "phase.dependency_cycle": {
        "severity": "blocking",
        "description": "The immutable phase dependency graph contains a cycle.",
    },
    "phase.duplicate_id": {
        "severity": "blocking",
        "description": "An immutable phase identity is duplicated.",
    },
    "phase.self_dependency": {
        "severity": "blocking",
        "description": "An immutable phase depends on itself.",
    },
    "phase.unknown_dependency": {
        "severity": "blocking",
        "description": "An immutable phase names an unknown dependency.",
    },
    "phase.unknown_task": {
        "severity": "blocking",
        "description": "An immutable phase names an unknown task.",
    },
    "plan.completed_tasks_incomplete": {
        "severity": "blocking",
        "description": "A completed legacy plan retains nonterminal tasks.",
    },
    "plan.multiple_active_tasks": {
        "severity": "blocking",
        "description": "A serial legacy plan has more than one active task.",
    },
    "plan.phase_scope_overlap": {
        "severity": "blocking",
        "description": "Required and excluded immutable phase scopes overlap.",
    },
    "plan.required_phase_scope_mismatch": {
        "severity": "blocking",
        "description": "Required phase scope differs from canonical phase order.",
    },
    "plan.required_task_scope_mismatch": {
        "severity": "blocking",
        "description": "Required task scope differs from canonical task order.",
    },
    "plan.task_scope_overlap": {
        "severity": "blocking",
        "description": "Required and excluded immutable task scopes overlap.",
    },
    "task.completed_dependency_incomplete": {
        "severity": "blocking",
        "description": "A completed legacy task has a nonterminal dependency.",
    },
    "task.dependency_cycle": {
        "severity": "blocking",
        "description": "The immutable task dependency graph contains a cycle.",
    },
    "task.phase_membership_mismatch": {
        "severity": "blocking",
        "description": "An immutable task does not appear exactly once in its declared phase.",
    },
    "task.self_dependency": {
        "severity": "blocking",
        "description": "An immutable task depends on itself.",
    },
    "task.unknown_dependency": {
        "severity": "blocking",
        "description": "An immutable task names an unknown dependency.",
    },
    "task.unknown_phase": {
        "severity": "blocking",
        "description": "An immutable task names an unknown phase.",
    },
}


SCHEMA_PROFILES = {
    "sys4ai.implementation-plan.v1": ("implementation_plan", "implementation-plan.schema.json"),
    "sys4ai.implementation-plan.v2": ("implementation_plan", "implementation-plan.schema.json"),
    "sys4ai.implementation-plan-state.v1": (
        "implementation_plan_state",
        "implementation-plan-state.schema.json",
    ),
    "sys4ai.plan-task-envelope.v1": ("plan_task_envelope", "plan-task-envelope.schema.json"),
    "sys4ai.plan-task-envelope.v2": (
        "plan_task_envelope",
        "plan-task-envelope-v2.schema.json",
    ),
    "sys4ai.plan-task-receipt.v1": ("plan_task_receipt", "plan-task-receipt.schema.json"),
    "sys4ai.plan-task-receipt.v2": (
        "plan_task_receipt",
        "plan-task-receipt-v2.schema.json",
    ),
    "sys4ai.plan-activation-receipt.v1": (
        "plan_activation_receipt",
        "plan-activation-receipt.schema.json",
    ),
    "sys4ai.plan-execution-profile.v1": (
        "plan_execution_profile",
        "plan-execution-profile.schema.json",
    ),
    "sys4ai.plan-normalization-report.v1": (
        "normalization_report",
        "normalization-report.schema.json",
    ),
    "sys4ai.plan-amendment.v1": ("plan_amendment", "plan-amendment.schema.json"),
    "sys4ai.plan-task-supersession.v1": (
        "task_supersession",
        "plan-task-supersession.schema.json",
    ),
    "sys4ai.plan-provider-intent.v1": ("provider_intent", "provider-intent.schema.json"),
    "sys4ai.plan-provider-intent.v2": (
        "provider_intent",
        "provider-intent-v2.schema.json",
    ),
    "sys4ai.plan-selection-proof.v1": ("selection_proof", "selection-proof.schema.json"),
}

CONTENT_HASH_FIELDS = {
    "sys4ai.plan-task-receipt.v1": "receipt_content_sha256",
    "sys4ai.plan-task-receipt.v2": "receipt_content_sha256",
    "sys4ai.plan-activation-receipt.v1": "receipt_content_sha256",
    "sys4ai.plan-execution-profile.v1": "profile_content_sha256",
    "sys4ai.plan-normalization-report.v1": "report_content_sha256",
    "sys4ai.plan-amendment.v1": "amendment_content_sha256",
    "sys4ai.plan-task-supersession.v1": "supersession_content_sha256",
    "sys4ai.plan-provider-intent.v1": "intent_content_sha256",
    "sys4ai.plan-provider-intent.v2": "intent_content_sha256",
    "sys4ai.plan-selection-proof.v1": "proof_content_sha256",
}


def _finding(
    code: str,
    message: str,
    *,
    path: str = "$",
    record_type: str | None = None,
    severity: str | None = None,
) -> dict[str, Any]:
    catalog = REASON_CODES.get(code)
    if catalog is None:
        raise ValueError(f"uncatalogued planctl reason code: {code}")
    return {
        "code": code,
        "severity": severity or catalog["severity"],
        "message": message,
        "path": path,
        "record_type": record_type,
    }


def _deduplicate(findings: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    keyed = {
        (
            str(item.get("code")),
            str(item.get("path")),
            str(item.get("record_type")),
            str(item.get("message")),
        ): dict(item)
        for item in findings
    }
    return [keyed[key] for key in sorted(keyed)]


def record_profile(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return None
    declared = value.get("schema_version")
    profile = SCHEMA_PROFILES.get(str(declared))
    return profile[0] if profile else None


def validate_record(
    value: Any,
    *,
    skill_root: Path,
    plan_validator: Callable[[Any], list[str]] | None = None,
) -> tuple[str | None, list[dict[str, Any]]]:
    """Validate one supported record and return structured stable findings."""

    profile = record_profile(value)
    if profile is None:
        declared = value.get("schema_version") if isinstance(value, Mapping) else None
        return None, [
            _finding(
                "record.schema_version_unknown",
                f"Unsupported schema version: {declared!r}.",
                path="$.schema_version",
            )
        ]
    schema_name = SCHEMA_PROFILES[str(value["schema_version"])][1]
    issues = validate_instance(value, skill_root / "schemas" / schema_name)
    findings = [
        _finding(
            "record.schema_invalid",
            f"{issue.code}: {issue.message}",
            path=issue.path,
            record_type=profile,
        )
        for issue in issues
    ]
    if profile == "implementation_plan" and not issues and plan_validator is not None:
        findings.extend(
            _finding(
                "record.schema_invalid",
                message,
                record_type=profile,
            )
            for message in plan_validator(value)
        )
    content_hash_field = CONTENT_HASH_FIELDS.get(str(value["schema_version"]))
    if content_hash_field is not None and not issues:
        expected = content_sha256(
            {
                key: item
                for key, item in value.items()
                if key != content_hash_field
            }
        )
        if value.get(content_hash_field) != expected:
            findings.append(
                _finding(
                    "record.content_hash_mismatch",
                    f"{content_hash_field} does not match canonical record content.",
                    path=f"$.{content_hash_field}",
                    record_type=profile,
                )
            )
    return profile, _deduplicate(findings)


def _record_value(record: Mapping[str, Any]) -> Mapping[str, Any]:
    value = record.get("value")
    return value if isinstance(value, Mapping) else {}


def _raw_sha256(record: Mapping[str, Any]) -> str:
    return str(record.get("sha256") or "")


def _record_path(record: Mapping[str, Any]) -> str:
    return str(record.get("path") or "<memory>")


def _valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _task_definitions(
    plan: Mapping[str, Any],
    supersessions: Sequence[Mapping[str, Any]],
    findings: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]], str]:
    definitions: dict[str, dict[str, Any]] = {}
    replacement_map: dict[str, list[str]] = {}
    positions: dict[int, str] = {}
    for position, task in enumerate(plan.get("tasks", [])):
        if not isinstance(task, Mapping) or not isinstance(task.get("task_id"), str):
            continue
        task_id = str(task["task_id"])
        definitions[task_id] = {
            "task_id": task_id,
            "task_sha256": task.get("task_sha256"),
            "phase_id": task.get("phase_id"),
            "depends_on": list(task.get("depends_on", [])),
            "canonical_position": position,
            "source": "plan",
        }
        positions[position] = task_id

    graph_basis: list[dict[str, Any]] = []
    for wrapped in supersessions:
        record = _record_value(wrapped)
        original = record.get("original_task")
        replacements = record.get("replacement_tasks")
        if not isinstance(original, Mapping) or not isinstance(replacements, list):
            continue
        original_id = str(original.get("task_id"))
        original_definition = definitions.get(original_id)
        if (
            original_definition is None
            or original_definition["task_sha256"] != original.get("task_sha256")
        ):
            if (
                original_definition is not None
                and original_definition["task_sha256"] != original.get("task_sha256")
            ):
                findings.append(
                    _finding(
                        "task.hash_drift",
                        f"Supersession original task {original_id!r} has a different immutable hash.",
                        record_type="task_supersession",
                    )
                )
            findings.append(
                _finding(
                    "supersession.identity_mismatch",
                    f"Supersession {_record_path(wrapped)!r} does not bind original task {original_id!r}.",
                    record_type="task_supersession",
                )
            )
            continue
        replacement_ids: list[str] = []
        for replacement in replacements:
            if not isinstance(replacement, Mapping):
                continue
            task_id = str(replacement.get("task_id"))
            position = replacement.get("canonical_position")
            if (
                task_id in definitions
                or task_id == original_id
                or not isinstance(position, int)
                or position in positions
            ):
                findings.append(
                    _finding(
                        "supersession.replacement_invalid",
                        f"Replacement task {task_id!r} reuses an identity or canonical position.",
                        record_type="task_supersession",
                    )
                )
                continue
            definitions[task_id] = {
                "task_id": task_id,
                "task_sha256": replacement.get("task_sha256"),
                "phase_id": original_definition.get("phase_id"),
                "depends_on": list(replacement.get("depends_on", [])),
                "canonical_position": position,
                "source": "supersession",
            }
            positions[position] = task_id
            replacement_ids.append(task_id)
        if replacement_ids:
            replacement_graph_basis = [
                {
                    "task_id": replacement.get("task_id"),
                    "task_sha256": replacement.get("task_sha256"),
                    "depends_on": replacement.get("depends_on"),
                    "canonical_position": replacement.get("canonical_position"),
                }
                for replacement in replacements
                if isinstance(replacement, Mapping)
            ]
            if record.get("replacement_graph_sha256") != content_sha256(
                replacement_graph_basis
            ):
                findings.append(
                    _finding(
                        "supersession.replacement_invalid",
                        f"Supersession {_record_path(wrapped)!r} replacement graph hash does not match its tasks.",
                        record_type="task_supersession",
                    )
                )
            mapped_ids = {
                str(task_id)
                for mapping in record.get("acceptance_mapping", [])
                if isinstance(mapping, Mapping)
                for task_id in mapping.get("replacement_task_ids", [])
            }
            if not mapped_ids <= set(replacement_ids):
                findings.append(
                    _finding(
                        "supersession.replacement_invalid",
                        f"Supersession {_record_path(wrapped)!r} maps acceptance to an unknown replacement.",
                        record_type="task_supersession",
                    )
                )
            if original_id in replacement_map:
                findings.append(
                    _finding(
                        "record.duplicate_identity",
                        f"More than one supersession replaces task {original_id!r}.",
                        record_type="task_supersession",
                    )
                )
            replacement_map[original_id] = replacement_ids
            graph_basis.append(
                {
                    "original_task_id": original_id,
                    "replacement_task_ids": replacement_ids,
                    "replacement_graph_sha256": record.get("replacement_graph_sha256"),
                }
            )

    replacement_ids = {
        replacement_id
        for replacements in replacement_map.values()
        for replacement_id in replacements
    }
    for task_id in sorted(replacement_ids):
        definition = definitions[task_id]
        for dependency_id in definition["depends_on"]:
            if (
                dependency_id == task_id
                or dependency_id not in definitions
                or dependency_id in replacement_map
            ):
                findings.append(
                    _finding(
                        "supersession.replacement_invalid",
                        f"Replacement task {task_id!r} has invalid dependency {dependency_id!r}.",
                        record_type="task_supersession",
                    )
                )

    graph = {
        task_id: [
            str(dependency_id)
            for dependency_id in definition["depends_on"]
            if str(dependency_id) in replacement_ids
        ]
        for task_id, definition in definitions.items()
        if task_id in replacement_ids
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def has_cycle(task_id: str) -> bool:
        if task_id in visiting:
            return True
        if task_id in visited:
            return False
        visiting.add(task_id)
        if any(has_cycle(dependency_id) for dependency_id in graph[task_id]):
            return True
        visiting.remove(task_id)
        visited.add(task_id)
        return False

    if any(has_cycle(task_id) for task_id in sorted(graph)):
        findings.append(
            _finding(
                "supersession.replacement_cycle",
                "Replacement-task dependency graph contains a cycle.",
                record_type="task_supersession",
            )
        )
    return definitions, replacement_map, content_sha256(graph_basis)


def _structural_findings(
    records: Sequence[Mapping[str, Any]],
    *,
    skill_root: Path,
    expected_profile: str,
    plan_validator: Callable[[Any], list[str]] | None,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for wrapped in records:
        profile, record_findings = validate_record(
            wrapped.get("value"),
            skill_root=skill_root,
            plan_validator=plan_validator,
        )
        findings.extend(record_findings)
        if profile is not None and profile != expected_profile:
            findings.append(
                _finding(
                    "record.schema_version_unknown",
                    f"Expected {expected_profile}, found {profile} in {_record_path(wrapped)!r}.",
                    record_type=profile,
                )
            )
    return findings


def _duplicate_record_findings(
    records: Sequence[Mapping[str, Any]],
    *,
    identity_field: str,
    record_type: str,
) -> list[dict[str, Any]]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for wrapped in records:
        identity = str(_record_value(wrapped).get(identity_field))
        if identity in seen:
            duplicates.add(identity)
        seen.add(identity)
    return [
        _finding(
            "record.duplicate_identity",
            f"{record_type} identity {identity!r} is supplied more than once.",
            record_type=record_type,
        )
        for identity in sorted(duplicates)
    ]


def validate_control_set(
    *,
    plan: Mapping[str, Any],
    state: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
    amendments: Sequence[Mapping[str, Any]],
    supersessions: Sequence[Mapping[str, Any]],
    provider_intents: Sequence[Mapping[str, Any]],
    selection_proofs: Sequence[Mapping[str, Any]],
    skill_root: Path,
    plan_validator: Callable[[Any], list[str]] | None = None,
    repository_fingerprint: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Validate one complete offline plan-control view without changing it."""

    findings: list[dict[str, Any]] = []
    groups = (
        ([plan], "implementation_plan"),
        ([state], "implementation_plan_state"),
        (list(receipts), "plan_task_receipt"),
        (list(amendments), "plan_amendment"),
        (list(supersessions), "task_supersession"),
        (list(provider_intents), "provider_intent"),
        (list(selection_proofs), "selection_proof"),
    )
    for records, profile in groups:
        findings.extend(
            _structural_findings(
                records,
                skill_root=skill_root,
                expected_profile=profile,
                plan_validator=plan_validator,
            )
        )

    plan_value = _record_value(plan)
    if findings:
        return _deduplicate(findings), {
            "plan_id": plan_value.get("plan_id"),
            "base_plan_sha256": _raw_sha256(plan),
            "effective_plan_sha256": _raw_sha256(plan),
            "valid_plan_hashes": [_raw_sha256(plan)],
            "definitions": {},
            "replacement_map": {},
            "state_by_id": {},
            "receipt_hash_by_task": {},
            "supersession_graph_sha256": content_sha256([]),
            "record_counts": {
                "plans": 1,
                "states": 1,
                "receipts": len(receipts),
                "amendments": len(amendments),
                "supersessions": len(supersessions),
                "provider_intents": len(provider_intents),
                "selection_proofs": len(selection_proofs),
            },
        }

    for records, identity_field, record_type in (
        (amendments, "amendment_id", "plan_amendment"),
        (supersessions, "supersession_id", "task_supersession"),
        (provider_intents, "intent_id", "provider_intent"),
        (selection_proofs, "proof_id", "selection_proof"),
    ):
        findings.extend(
            _duplicate_record_findings(
                records,
                identity_field=identity_field,
                record_type=record_type,
            )
        )

    state_value = _record_value(state)
    plan_id = plan_value.get("plan_id")
    base_plan_sha256 = _raw_sha256(plan)
    valid_plan_hashes = [base_plan_sha256]
    effective_plan_sha256 = base_plan_sha256

    amendment_values = sorted(
        amendments,
        key=lambda wrapped: int(_record_value(wrapped).get("sequence", -1)),
    )
    sequences = [
        _record_value(wrapped).get("sequence") for wrapped in amendment_values
    ]
    if sequences and sequences != list(range(1, len(sequences) + 1)):
        findings.append(
            _finding(
                "amendment.sequence_invalid",
                f"Amendment sequences must be contiguous from 1, found {sequences!r}.",
                record_type="plan_amendment",
            )
        )
    for wrapped in amendment_values:
        record = _record_value(wrapped)
        if record.get("plan_id") != plan_id:
            findings.append(
                _finding(
                    "amendment.identity_mismatch",
                    f"Amendment {_record_path(wrapped)!r} names a different plan.",
                    record_type="plan_amendment",
                )
            )
        if record.get("prior_effective_plan_sha256") != effective_plan_sha256:
            findings.append(
                _finding(
                    "amendment.chain_invalid",
                    f"Amendment {_record_path(wrapped)!r} does not continue hash {effective_plan_sha256!r}.",
                    record_type="plan_amendment",
                )
            )
        if record.get("new_effective_plan_sha256") == record.get(
            "prior_effective_plan_sha256"
        ):
            findings.append(
                _finding(
                    "amendment.chain_invalid",
                    f"Amendment {_record_path(wrapped)!r} has no effective hash change.",
                    record_type="plan_amendment",
                )
            )
        new_hash = record.get("new_effective_plan_sha256")
        if isinstance(new_hash, str):
            effective_plan_sha256 = new_hash
            valid_plan_hashes.append(new_hash)

    if state_value.get("plan_id") != plan_id:
        findings.append(
            _finding(
                "plan.identity_mismatch",
                "Plan state names a different immutable plan identity.",
                path="$.plan_id",
                record_type="implementation_plan_state",
            )
        )
    if state_value.get("plan_sha256") != effective_plan_sha256:
        findings.append(
            _finding(
                "plan.hash_mismatch",
                f"Plan state hash {state_value.get('plan_sha256')!r} does not equal effective hash {effective_plan_sha256!r}.",
                path="$.plan_sha256",
                record_type="implementation_plan_state",
            )
        )
    if (
        repository_fingerprint is not None
        and state_value.get("repository_fingerprint") != repository_fingerprint
    ):
        findings.append(
            _finding(
                "state.repository_fingerprint_mismatch",
                "Plan state repository fingerprint differs from direct evidence.",
                path="$.repository_fingerprint",
                record_type="implementation_plan_state",
            )
        )
    state_fingerprints = state_value.get("fingerprints")
    if (
        isinstance(state_fingerprints, Mapping)
        and state_fingerprints.get("current")
        != state_value.get("repository_fingerprint")
    ):
        findings.append(
            _finding(
                "state.repository_fingerprint_mismatch",
                "State current fingerprint differs from repository fingerprint.",
                path="$.fingerprints.current",
                record_type="implementation_plan_state",
            )
        )

    for wrapped in supersessions:
        record = _record_value(wrapped)
        if (
            record.get("plan_id") != plan_id
            or record.get("plan_sha256") not in valid_plan_hashes
        ):
            findings.append(
                _finding(
                    "supersession.identity_mismatch",
                    f"Supersession {_record_path(wrapped)!r} is outside the effective plan history.",
                    record_type="task_supersession",
                )
            )
    definitions, replacement_map, supersession_graph_sha256 = _task_definitions(
        plan_value,
        supersessions,
        findings,
    )

    state_tasks = state_value.get("tasks")
    state_by_id: dict[str, Mapping[str, Any]] = {}
    if isinstance(state_tasks, list):
        for task in state_tasks:
            if not isinstance(task, Mapping) or not isinstance(task.get("task_id"), str):
                continue
            task_id = str(task["task_id"])
            if task_id in state_by_id:
                findings.append(
                    _finding(
                        "record.duplicate_identity",
                        f"Plan state repeats task {task_id!r}.",
                        path="$.tasks",
                        record_type="implementation_plan_state",
                    )
                )
            state_by_id[task_id] = task
    for task_id, definition in definitions.items():
        lifecycle = state_by_id.get(task_id)
        if lifecycle is None:
            findings.append(
                _finding(
                    "state.task_missing",
                    f"Task {task_id!r} has no lifecycle state.",
                    path="$.tasks",
                    record_type="implementation_plan_state",
                )
            )
            continue
        if lifecycle.get("task_sha256") != definition["task_sha256"]:
            findings.append(
                _finding(
                    "task.hash_drift",
                    f"Task {task_id!r} hash differs between immutable authority and state.",
                    path="$.tasks",
                    record_type="implementation_plan_state",
                )
            )
    for task_id in sorted(set(state_by_id) - set(definitions)):
        findings.append(
            _finding(
                "state.task_unknown",
                f"Lifecycle state contains unknown task {task_id!r}.",
                path="$.tasks",
                record_type="implementation_plan_state",
            )
        )
    for original_id in replacement_map:
        lifecycle = state_by_id.get(original_id)
        if lifecycle is not None and lifecycle.get("status") != "superseded":
            findings.append(
                _finding(
                    "supersession.identity_mismatch",
                    f"Superseded original task {original_id!r} is not terminal as superseded.",
                    path="$.tasks",
                    record_type="implementation_plan_state",
                )
            )

    state_phase = str(state_value.get("phase"))
    lifecycle_statuses = {
        str(task.get("status")) for task in state_by_id.values()
    }
    if state_phase in {"completion_candidate", "terminal_complete"} and not all(
        status in TERMINAL_TASK_STATUSES for status in lifecycle_statuses
    ):
        findings.append(
            _finding(
                "state.phase_mismatch",
                f"State phase {state_phase!r} requires every task to be terminal.",
                path="$.phase",
                record_type="implementation_plan_state",
            )
        )
    if (
        state_phase in NON_SCHEDULABLE_PHASES - {"recovery_pending"}
        and not lifecycle_statuses.intersection(BLOCKED_TASK_STATUSES)
    ):
        findings.append(
            _finding(
                "state.phase_mismatch",
                f"State phase {state_phase!r} has no protected-stop task lifecycle.",
                path="$.phase",
                record_type="implementation_plan_state",
            )
        )

    active_ids = [
        task_id
        for task_id, task in state_by_id.items()
        if task.get("status") in ACTIVE_TASK_STATUSES
    ]
    active_task_id = state_value.get("active_task_id")
    if active_ids != ([active_task_id] if active_task_id is not None else []):
        findings.append(
            _finding(
                "state.active_task_mismatch",
                f"active_task_id {active_task_id!r} disagrees with active lifecycle tasks {active_ids!r}.",
                path="$.active_task_id",
                record_type="implementation_plan_state",
            )
        )
    lease = state_value.get("lease")
    if isinstance(lease, Mapping):
        if (
            lease.get("task_id") != active_task_id
            or lease.get("generation") != state_value.get("current_generation")
            or lease.get("repository_fingerprint")
            != state_value.get("repository_fingerprint")
        ):
            findings.append(
                _finding(
                    "state.active_task_mismatch",
                    "Active lease does not match state task, generation, or repository.",
                    path="$.lease",
                    record_type="implementation_plan_state",
                )
            )
    if active_task_id is not None:
        active_lifecycle = state_by_id.get(str(active_task_id))
        expected_status = {
            "task_reserved": "reserved",
            "task_active": "active",
            "task_verifying": "verifying",
        }.get(str(state_value.get("phase")))
        if (
            active_lifecycle is None
            or active_lifecycle.get("generation")
            != state_value.get("current_generation")
            or (
                expected_status is not None
                and active_lifecycle.get("status") != expected_status
            )
        ):
            findings.append(
                _finding(
                    "state.generation_mismatch",
                    "Active task lifecycle does not match state phase and generation.",
                    path="$.current_generation",
                    record_type="implementation_plan_state",
                )
            )
    else:
        generations = [
            int(task["generation"])
            for task in state_by_id.values()
            if isinstance(task.get("generation"), int)
        ]
        expected_generation = max(generations, default=0)
        if state_value.get("current_generation") != expected_generation:
            findings.append(
                _finding(
                    "state.generation_mismatch",
                    f"State generation is {state_value.get('current_generation')!r}; latest task generation is {expected_generation}.",
                    path="$.current_generation",
                    record_type="implementation_plan_state",
                )
            )

    counters = state_value.get("counters")
    if isinstance(counters, Mapping):
        projections = {
            "worker_discussions": sum(
                int(task.get("counters", {}).get("worker_discussions", 0))
                for task in state_by_id.values()
            ),
            "continue_invocations": sum(
                int(task.get("counters", {}).get("continue_invocations", 0))
                for task in state_by_id.values()
            ),
            "agentjobs": sum(
                int(task.get("counters", {}).get("agentjobs", 0))
                for task in state_by_id.values()
            ),
            "provider_creates": sum(
                int(task.get("counters", {}).get("provider_creates", 0))
                for task in state_by_id.values()
            ),
            "successor_creates": sum(
                int(task.get("counters", {}).get("successor_creates", 0))
                for task in state_by_id.values()
            ),
            "tasks_completed": sum(
                task.get("status") == "completed" for task in state_by_id.values()
            ),
            "tasks_superseded": sum(
                task.get("status") == "superseded" for task in state_by_id.values()
            ),
            "protected_stops": sum(
                task.get("status") in BLOCKED_TASK_STATUSES
                for task in state_by_id.values()
            ),
        }
        for key, expected in projections.items():
            if counters.get(key) != expected:
                findings.append(
                    _finding(
                        "state.counter_mismatch",
                        f"Counter {key!r} is {counters.get(key)!r}; projected value is {expected}.",
                        path=f"$.counters.{key}",
                        record_type="implementation_plan_state",
                    )
                )

    receipt_by_id: dict[str, tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    receipt_hash_by_task: dict[str, str] = {}
    for wrapped in receipts:
        record = _record_value(wrapped)
        receipt_id = str(record.get("receipt_id"))
        if receipt_id in receipt_by_id:
            findings.append(
                _finding(
                    "record.duplicate_identity",
                    f"Receipt identity {receipt_id!r} is supplied more than once.",
                    record_type="plan_task_receipt",
                )
            )
        receipt_by_id[receipt_id] = (record, wrapped)
        plan_identity = record.get("plan_identity")
        task_identity = record.get("task_identity")
        if not isinstance(plan_identity, Mapping) or not isinstance(task_identity, Mapping):
            continue
        task_id = str(task_identity.get("task_id"))
        definition = definitions.get(task_id)
        if (
            plan_identity.get("plan_id") != plan_id
            or plan_identity.get("plan_sha256") not in valid_plan_hashes
            or definition is None
            or task_identity.get("task_sha256") != definition["task_sha256"]
        ):
            if (
                definition is not None
                and task_identity.get("task_sha256") != definition["task_sha256"]
            ):
                findings.append(
                    _finding(
                        "task.hash_drift",
                        f"Receipt {receipt_id!r} changes immutable task hash for {task_id!r}.",
                        record_type="plan_task_receipt",
                    )
                )
            findings.append(
                _finding(
                    "receipt.identity_mismatch",
                    f"Receipt {receipt_id!r} is not bound to the supplied plan/task history.",
                    record_type="plan_task_receipt",
                )
            )
        elif plan_identity.get("phase_id") != definition.get("phase_id"):
            findings.append(
                _finding(
                    "receipt.identity_mismatch",
                    f"Receipt {receipt_id!r} names the wrong phase for task {task_id!r}.",
                    record_type="plan_task_receipt",
                )
            )
        receipt_hash_by_task[task_id] = _raw_sha256(wrapped)

    for wrapped in supersessions:
        original = _record_value(wrapped).get("original_task", {})
        receipt_id = str(original.get("receipt_id"))
        supplied = receipt_by_id.get(receipt_id)
        if supplied is None:
            findings.append(
                _finding(
                    "receipt.missing",
                    f"Supersession {_record_path(wrapped)!r} links missing receipt {receipt_id!r}.",
                    record_type="task_supersession",
                )
            )
            continue
        receipt, receipt_wrapped = supplied
        task_identity = receipt.get("task_identity", {})
        if (
            original.get("receipt_sha256") != _raw_sha256(receipt_wrapped)
            or task_identity.get("task_id") != original.get("task_id")
            or task_identity.get("task_sha256") != original.get("task_sha256")
            or receipt.get("disposition") != "replan_required"
        ):
            findings.append(
                _finding(
                    "supersession.identity_mismatch",
                    f"Supersession {_record_path(wrapped)!r} is not bound to its exact replan receipt.",
                    record_type="task_supersession",
                )
            )

    disposition_by_state = {
        "completed": {"task_complete", "plan_complete"},
        "blocked": {"blocked"},
        "superseded": {"replan_required"},
        "replan_required": {"replan_required"},
        "human_gate_required": {"human_gate_required"},
        "validation_failed": {"validation_failed"},
        "invocation_unknown": {"invocation_unknown"},
        "cancelled": {"cancelled"},
    }
    for task_id, lifecycle in state_by_id.items():
        status = lifecycle.get("status")
        if status not in disposition_by_state:
            continue
        link = lifecycle.get("receipt_link")
        if not isinstance(link, Mapping):
            continue
        receipt_id = str(link.get("receipt_id"))
        supplied = receipt_by_id.get(receipt_id)
        if supplied is None:
            findings.append(
                _finding(
                    "receipt.missing",
                    f"Terminal task {task_id!r} links missing receipt {receipt_id!r}.",
                    path="$.tasks",
                    record_type="implementation_plan_state",
                )
            )
            continue
        receipt, wrapped = supplied
        if link.get("receipt_sha256") != _raw_sha256(wrapped):
            findings.append(
                _finding(
                    "receipt.hash_mismatch",
                    f"Task {task_id!r} receipt link does not match {_record_path(wrapped)!r}.",
                    path="$.tasks",
                    record_type="implementation_plan_state",
                )
            )
        task_identity = receipt.get("task_identity", {})
        if task_identity.get("task_id") != task_id:
            findings.append(
                _finding(
                    "receipt.identity_mismatch",
                    f"Task {task_id!r} links a receipt for {task_identity.get('task_id')!r}.",
                    path="$.tasks",
                    record_type="implementation_plan_state",
                )
            )
        if receipt.get("disposition") not in disposition_by_state[status]:
            findings.append(
                _finding(
                    "receipt.identity_mismatch",
                    f"Task state {status!r} disagrees with receipt disposition {receipt.get('disposition')!r}.",
                    path="$.tasks",
                    record_type="implementation_plan_state",
                )
            )
        relay_identity = receipt.get("relay_identity", {})
        execution = receipt.get("execution", {})
        lifecycle_counters = lifecycle.get("counters", {})
        expected_counters = {
            "worker_discussions": execution.get("worker_discussions"),
            "continue_invocations": execution.get("continue_invocations"),
            "agentjobs": execution.get("agentjobs"),
            "provider_creates": execution.get("provider_create_calls"),
            "successor_creates": execution.get("successor_creates"),
            "same_task_successors": execution.get("same_task_successors"),
        }
        repository_evidence = receipt.get("repository_evidence", {})
        if (
            relay_identity.get("generation") != lifecycle.get("generation")
            or any(
                lifecycle_counters.get(key) != expected
                for key, expected in expected_counters.items()
            )
            or repository_evidence.get("fingerprint_before")
            != lifecycle.get("fingerprint_before")
            or repository_evidence.get("fingerprint_after")
            != lifecycle.get("fingerprint_after")
        ):
            findings.append(
                _finding(
                    "receipt.execution_mismatch",
                    f"Receipt {receipt_id!r} execution evidence disagrees with lifecycle task {task_id!r}.",
                    path="$.tasks",
                    record_type="implementation_plan_state",
                )
            )

    for wrapped in provider_intents:
        record = _record_value(wrapped)
        task_id = str(record.get("task_id"))
        definition = definitions.get(task_id)
        if (
            record.get("plan_id") != plan_id
            or record.get("plan_sha256") not in valid_plan_hashes
            or definition is None
            or record.get("task_sha256") != definition["task_sha256"]
            or record.get("repository_fingerprint")
            != state_value.get("repository_fingerprint")
            or int(record.get("expected_revision", 0))
            > int(state_value.get("revision", 0))
            or int(record.get("generation", 0))
            > int(state_value.get("current_generation", 0)) + 1
        ):
            if (
                definition is not None
                and record.get("task_sha256") != definition["task_sha256"]
            ):
                findings.append(
                    _finding(
                        "task.hash_drift",
                        f"Provider intent for {task_id!r} changes its immutable task hash.",
                        record_type="provider_intent",
                    )
                )
            findings.append(
                _finding(
                    "provider.identity_mismatch",
                    f"Provider intent {_record_path(wrapped)!r} is not bound to effective state.",
                    record_type="provider_intent",
                )
            )
        if (
            record.get("returned_thread_id") is not None
            and record.get("returned_thread_id")
            == record.get("predecessor_thread_id")
        ):
            findings.append(
                _finding(
                    "provider.predecessor_reused",
                    f"Provider intent {_record_path(wrapped)!r} reused its predecessor discussion.",
                    record_type="provider_intent",
                )
            )

    for wrapped in selection_proofs:
        record = _record_value(wrapped)
        if (
            record.get("plan_id") != plan_id
            or record.get("plan_sha256") != effective_plan_sha256
            or record.get("plan_revision") != state_value.get("revision")
            or record.get("repository_fingerprint")
            != state_value.get("repository_fingerprint")
        ):
            findings.append(
                _finding(
                    "selection.proof_invalid",
                    f"Selection proof {_record_path(wrapped)!r} is not revision-bound to effective state.",
                    record_type="selection_proof",
                )
            )
            continue
        expected_proof, proof_findings = build_selection_proof(
            plan=plan_value,
            state=state_value,
            context={
                "effective_plan_sha256": effective_plan_sha256,
                "definitions": definitions,
                "replacement_map": replacement_map,
                "state_by_id": state_by_id,
                "supersession_graph_sha256": supersession_graph_sha256,
            },
            prior_journal_sha256=str(record.get("prior_journal_sha256")),
            skill_root=skill_root,
        )
        findings.extend(proof_findings)
        if expected_proof is None:
            continue
        proof_fields = (
            "proof_id",
            "selector_protocol_version",
            "selection_policy_sha256",
            "supersession_graph_sha256",
            "lease_token_sha256",
            "active_task_ids",
            "ordered_tasks",
            "outcome",
            "selected_task",
            "blocking_reasons",
            "canonical_order_only",
            "revision_bound",
            "compare_and_swap_required",
        )
        if any(record.get(field) != expected_proof.get(field) for field in proof_fields):
            for snapshot in record.get("ordered_tasks", []):
                if not isinstance(snapshot, Mapping):
                    continue
                definition = definitions.get(str(snapshot.get("task_id")))
                if (
                    definition is not None
                    and snapshot.get("task_sha256")
                    != definition.get("task_sha256")
                ):
                    findings.append(
                        _finding(
                            "task.hash_drift",
                            f"Selection proof changes immutable task hash for {snapshot.get('task_id')!r}.",
                            record_type="selection_proof",
                        )
                    )
            findings.append(
                _finding(
                    "selection.proof_invalid",
                    f"Selection proof {_record_path(wrapped)!r} does not reproduce deterministic scheduling evidence.",
                    record_type="selection_proof",
                )
            )

    context = {
        "plan_id": plan_id,
        "base_plan_sha256": base_plan_sha256,
        "effective_plan_sha256": effective_plan_sha256,
        "valid_plan_hashes": valid_plan_hashes,
        "definitions": definitions,
        "replacement_map": replacement_map,
        "state_by_id": state_by_id,
        "receipt_hash_by_task": receipt_hash_by_task,
        "supersession_graph_sha256": supersession_graph_sha256,
        "record_counts": {
            "plans": 1,
            "states": 1,
            "receipts": len(receipts),
            "amendments": len(amendments),
            "supersessions": len(supersessions),
            "provider_intents": len(provider_intents),
            "selection_proofs": len(selection_proofs),
        },
    }
    return _deduplicate(findings), context


def diff_plans(
    prior: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    prior_sha256: str,
    current_sha256: str,
) -> dict[str, Any]:
    """Return deterministic immutable-plan change and task-hash drift evidence."""

    findings: list[dict[str, Any]] = []
    changes: list[dict[str, Any]] = []
    if prior.get("plan_id") != current.get("plan_id"):
        findings.append(
            _finding(
                "diff.plan_identity_changed",
                f"Plan identity changed from {prior.get('plan_id')!r} to {current.get('plan_id')!r}.",
                path="$.plan_id",
                record_type="implementation_plan",
            )
        )
    prior_tasks = {
        str(task["task_id"]): task
        for task in prior.get("tasks", [])
        if isinstance(task, Mapping) and isinstance(task.get("task_id"), str)
    }
    current_tasks = {
        str(task["task_id"]): task
        for task in current.get("tasks", [])
        if isinstance(task, Mapping) and isinstance(task.get("task_id"), str)
    }
    for task_id in sorted(set(current_tasks) - set(prior_tasks)):
        changes.append(
            {
                "code": "plan.task_added",
                "identity": task_id,
                "before_sha256": None,
                "after_sha256": current_tasks[task_id].get("task_sha256"),
            }
        )
    for task_id in sorted(set(prior_tasks) - set(current_tasks)):
        changes.append(
            {
                "code": "plan.task_removed",
                "identity": task_id,
                "before_sha256": prior_tasks[task_id].get("task_sha256"),
                "after_sha256": None,
            }
        )
        findings.append(
            _finding(
                "plan.task_removed",
                f"Task {task_id!r} was removed rather than superseded.",
                path="$.tasks",
                record_type="implementation_plan",
            )
        )
    for task_id in sorted(set(prior_tasks) & set(current_tasks)):
        before = prior_tasks[task_id].get("task_sha256")
        after = current_tasks[task_id].get("task_sha256")
        if before != after:
            changes.append(
                {
                    "code": "task.hash_drift",
                    "identity": task_id,
                    "before_sha256": before,
                    "after_sha256": after,
                }
            )
            findings.append(
                _finding(
                    "task.hash_drift",
                    f"Immutable task {task_id!r} changed hash from {before!r} to {after!r}.",
                    path="$.tasks",
                    record_type="implementation_plan",
                )
            )
    prior_phases = {
        str(phase["phase_id"]): content_sha256(phase)
        for phase in prior.get("phases", [])
        if isinstance(phase, Mapping) and isinstance(phase.get("phase_id"), str)
    }
    current_phases = {
        str(phase["phase_id"]): content_sha256(phase)
        for phase in current.get("phases", [])
        if isinstance(phase, Mapping) and isinstance(phase.get("phase_id"), str)
    }
    for phase_id in sorted(set(prior_phases) | set(current_phases)):
        if prior_phases.get(phase_id) != current_phases.get(phase_id):
            changes.append(
                {
                    "code": "plan.phase_changed",
                    "identity": phase_id,
                    "before_sha256": prior_phases.get(phase_id),
                    "after_sha256": current_phases.get(phase_id),
                }
            )
    return {
        "status": (
            "identity_conflict"
            if any(item["code"] == "diff.plan_identity_changed" for item in findings)
            else "changed"
            if prior_sha256 != current_sha256 or changes
            else "unchanged"
        ),
        "prior_plan_sha256": prior_sha256,
        "current_plan_sha256": current_sha256,
        "changes": sorted(changes, key=lambda item: (item["code"], item["identity"])),
        "findings": _deduplicate(findings),
    }


def build_selection_proof(
    *,
    plan: Mapping[str, Any],
    state: Mapping[str, Any],
    context: Mapping[str, Any],
    prior_journal_sha256: str,
    skill_root: Path,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    """Build one deterministic advisory proof from an already-valid control set."""

    if not _valid_sha256(prior_journal_sha256):
        return None, [
            _finding(
                "selection.journal_hash_required",
                "A lowercase 64-character prior journal SHA-256 is required.",
                path="$.prior_journal_sha256",
                record_type="selection_proof",
            )
        ]
    definitions = context["definitions"]
    state_by_id = context["state_by_id"]
    replacement_map = context["replacement_map"]
    ordered_tasks: list[dict[str, Any]] = []
    ready: list[dict[str, Any]] = []
    active_task_ids: list[str] = []

    def effective_ids(task_id: str) -> list[str]:
        return list(replacement_map.get(task_id, [task_id]))

    for task_id, definition in sorted(
        definitions.items(),
        key=lambda item: (int(item[1]["canonical_position"]), item[0]),
    ):
        lifecycle = state_by_id[task_id]
        lifecycle_status = str(lifecycle["status"])
        if lifecycle_status in ACTIVE_TASK_STATUSES:
            active_task_ids.append(task_id)
        proof_status = (
            "active"
            if lifecycle_status in {"active", "verifying"}
            else "reserved"
            if lifecycle_status == "reserved"
            else "completed"
            if lifecycle_status == "completed"
            else "superseded"
            if lifecycle_status == "superseded"
            else "recovery_pending"
            if lifecycle_status == "invocation_unknown"
            else "blocked"
            if lifecycle_status in BLOCKED_TASK_STATUSES
            else "pending"
        )
        dependency_proofs: list[dict[str, Any]] = []
        dependency_ready = True
        for dependency_id in definition["depends_on"]:
            resolved = effective_ids(str(dependency_id))
            resolved_states = [state_by_id.get(item) for item in resolved]
            terminal = bool(resolved_states) and all(
                item is not None
                and item.get("status") in TERMINAL_TASK_STATUSES
                and isinstance(item.get("receipt_link"), Mapping)
                for item in resolved_states
            )
            dependency_ready = dependency_ready and terminal
            hashes = [
                str(item["receipt_link"]["receipt_sha256"])
                for item in resolved_states
                if item is not None and isinstance(item.get("receipt_link"), Mapping)
            ]
            dependency_proofs.append(
                {
                    "task_id": str(dependency_id),
                    "effective_task_ids": resolved,
                    "status": "terminal" if terminal else "nonterminal",
                    "receipt_sha256s": hashes if terminal else [],
                }
            )
        snapshot = {
            "canonical_position": int(definition["canonical_position"]),
            "task_id": task_id,
            "task_sha256": definition["task_sha256"],
            "effective_task_ids": effective_ids(task_id),
            "status": proof_status,
            "dependencies": dependency_proofs,
            "dependency_ready": dependency_ready,
        }
        ordered_tasks.append(snapshot)
        if proof_status == "pending" and dependency_ready:
            ready.append(snapshot)

    blocking_reasons: list[str] = []
    if active_task_ids:
        outcome = "blocked_no_runnable"
        selected_task = None
        blocking_reasons = ["selection.active_task_present"]
    elif state.get("phase") in NON_SCHEDULABLE_PHASES:
        outcome = "blocked_no_runnable"
        selected_task = None
        blocking_reasons = ["selection.state_not_schedulable"]
    elif ordered_tasks and all(
        item["status"] in {"completed", "superseded"} for item in ordered_tasks
    ):
        outcome = "completion_candidate"
        selected_task = None
    elif ready:
        outcome = "selected"
        first = ready[0]
        selected_task = {
            "task_id": first["task_id"],
            "task_sha256": first["task_sha256"],
            "canonical_position": first["canonical_position"],
            "dependency_receipt_sha256s": sorted(
                {
                    receipt
                    for dependency in first["dependencies"]
                    for receipt in dependency["receipt_sha256s"]
                }
            ),
        }
    elif any(item["status"] == "pending" for item in ordered_tasks):
        outcome = "no_ready_task"
        selected_task = None
        blocking_reasons = ["selection.dependencies_not_terminal"]
    else:
        outcome = "blocked_no_runnable"
        selected_task = None
        blocking_reasons = ["selection.no_runnable_task"]

    lease = state.get("lease")
    lease_hash = (
        lease.get("holder_token_hash")
        if isinstance(lease, Mapping)
        else content_sha256(None)
    )
    proof = {
        "schema_version": "sys4ai.plan-selection-proof.v1",
        "proof_id": "PSP-PENDING",
        "plan_id": plan["plan_id"],
        "plan_sha256": context["effective_plan_sha256"],
        "plan_revision": state["revision"],
        "prior_journal_sha256": prior_journal_sha256,
        "repository_fingerprint": state["repository_fingerprint"],
        "selector_protocol_version": "1.0.0",
        "selection_policy_sha256": SELECTION_POLICY_SHA256,
        "supersession_graph_sha256": context["supersession_graph_sha256"],
        "lease_token_sha256": lease_hash,
        "active_task_ids": active_task_ids,
        "ordered_tasks": ordered_tasks,
        "outcome": outcome,
        "selected_task": selected_task,
        "blocking_reasons": blocking_reasons,
        "canonical_order_only": True,
        "revision_bound": True,
        "compare_and_swap_required": True,
        "hash_basis": "canonical_json_without_proof_content_sha256",
        "proof_content_sha256": "0" * 64,
        "finalized": True,
        "extensions": {},
    }
    proof["proof_id"] = "PSP-" + content_sha256(
        {
            "plan_id": proof["plan_id"],
            "plan_sha256": proof["plan_sha256"],
            "plan_revision": proof["plan_revision"],
            "prior_journal_sha256": prior_journal_sha256,
            "selection_policy_sha256": SELECTION_POLICY_SHA256,
            "supersession_graph_sha256": proof["supersession_graph_sha256"],
        }
    )[:24].upper()
    proof["proof_content_sha256"] = content_sha256(
        {
            key: value
            for key, value in proof.items()
            if key != "proof_content_sha256"
        }
    )
    issues = validate_instance(proof, skill_root / "schemas" / "selection-proof.schema.json")
    findings = [
        _finding(
            "selection.proof_invalid",
            f"{issue.code}: {issue.message}",
            path=issue.path,
            record_type="selection_proof",
        )
        for issue in issues
    ]
    return (proof if not findings else None), _deduplicate(findings)


def _redaction_key(key: str) -> bool:
    lowered = key.lower()
    if "sha256" in lowered or lowered.endswith("_hash") or lowered == "hash":
        return False
    if lowered == "token" or lowered.endswith("_token"):
        return True
    return any(
        marker in lowered
        for marker in (
            "access_token",
            "api_key",
            "credential",
            "handoff_token",
            "lease_token",
            "password",
            "private_key",
            "provider_response",
            "secret",
            "goal_text",
        )
    )


def redact_record(value: Any) -> tuple[Any, list[str]]:
    """Return a deterministic redacted copy and JSON paths changed."""

    paths: list[str] = []

    def walk(item: Any, path: str, key: str | None = None) -> Any:
        sensitive = key is not None and _redaction_key(key)
        if sensitive and item is not None:
            paths.append(path)
            return {"redacted": True, "sha256": content_sha256(item)}
        if isinstance(item, Mapping):
            return {
                str(child_key): walk(
                    child_value,
                    f"{path}.{child_key}",
                    str(child_key),
                )
                for child_key, child_value in item.items()
            }
        if isinstance(item, list):
            return [
                walk(child, f"{path}[{index}]", key)
                for index, child in enumerate(item)
            ]
        if isinstance(item, str) and contains_secret(item):
            paths.append(path)
            return {"redacted": True, "sha256": hashlib.sha256(item.encode("utf-8")).hexdigest()}
        return item

    return walk(value, "$"), sorted(set(paths))
