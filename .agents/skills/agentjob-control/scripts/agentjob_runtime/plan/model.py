"""Plan-profile canonicalization, state validation, and journal primitives."""

from __future__ import annotations

import copy
import hashlib
import re
from collections.abc import Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import Any

from agentjob_runtime.errors import RecordValidationError, SecurityError
from agentjob_runtime.goal.model import parse_utc
from agentjob_runtime.records.canonical import canonical_json_bytes, content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


PLAN_SCHEMA_VERSION_V1 = "sys4ai.implementation-plan.v1"
PLAN_SCHEMA_VERSION = "sys4ai.implementation-plan.v2"
PLAN_STATE_SCHEMA_VERSION = "sys4ai.implementation-plan-state.v1"
PLAN_RECORD_BASE_KEYS = frozenset(
    {
        "plan_id",
        "outer_goal_id",
        "plan_sha256",
        "effective_plan_sha256",
        "repository_binding",
        "repository_fingerprint",
        "plan",
        "state",
        "journal",
        "created_at",
        "updated_at",
    }
)
PLAN_RUNTIME_PROFILE_KEYS = frozenset(
    {
        "runtime_profile_version",
        "activation_sequence",
        "activation_receipt_sha256",
        "execution_profile",
        "repository_topology_policy",
        "activation_goal_text",
        "activation_goal_sha256",
        "profile_effective_from_generation",
        "repository_binding_sha256",
    }
)
PLAN_RECORD_KEYS = PLAN_RECORD_BASE_KEYS | PLAN_RUNTIME_PROFILE_KEYS
ACTIVE_TASK_STATUSES = frozenset({"reserved", "active", "verifying"})
TERMINAL_TASK_STATUSES = frozenset({"completed", "superseded"})
PROTECTED_STOP_TASK_STATUSES = frozenset(
    {
        "blocked",
        "replan_required",
        "human_gate_required",
        "validation_failed",
        "invocation_unknown",
        "cancelled",
    }
)
PLAN_JOURNAL_KINDS = frozenset(
    {
        "event",
        "task_receipt",
        "phase_gate_receipt",
        "plan_completion_receipt",
        "provider_intent",
        "selection_proof",
        "amendment",
        "supersession",
        "recovery",
    }
)
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


def _immutable_v2_findings(
    plan: Mapping[str, Any], tasks_by_id: Mapping[str, Mapping[str, Any]]
) -> list[str]:
    findings: list[str] = []
    phases = plan.get("phases")
    if not isinstance(phases, list):
        return findings

    phases_by_id: dict[str, Mapping[str, Any]] = {}
    for index, phase in enumerate(phases):
        if not isinstance(phase, Mapping) or not isinstance(phase.get("phase_id"), str):
            continue
        phase_id = str(phase["phase_id"])
        if phase_id in phases_by_id:
            findings.append(
                f"phase.duplicate_id $.phases[{index}]: duplicate phase_id {phase_id!r}"
            )
        else:
            phases_by_id[phase_id] = phase

    required_scope = plan.get("required_scope")
    if isinstance(required_scope, Mapping):
        phase_ids = list(phases_by_id)
        task_ids = list(tasks_by_id)
        if required_scope.get("phase_ids") != phase_ids:
            findings.append(
                "plan.required_phase_scope_mismatch $.required_scope.phase_ids: "
                "required phase IDs must equal canonical phase order"
            )
        if required_scope.get("task_ids") != task_ids:
            findings.append(
                "plan.required_task_scope_mismatch $.required_scope.task_ids: "
                "required task IDs must equal canonical task order"
            )
        excluded_phases = set(required_scope.get("excluded_phase_ids", []))
        excluded_tasks = set(required_scope.get("excluded_task_ids", []))
        if excluded_phases.intersection(phase_ids):
            findings.append(
                "plan.phase_scope_overlap $.required_scope: "
                "required and excluded phase IDs must be disjoint"
            )
        if excluded_tasks.intersection(task_ids):
            findings.append(
                "plan.task_scope_overlap $.required_scope: "
                "required and excluded task IDs must be disjoint"
            )

    phase_graph: dict[str, list[str]] = {}
    memberships: dict[str, list[str]] = {task_id: [] for task_id in tasks_by_id}
    for phase_id, phase in phases_by_id.items():
        phase_graph[phase_id] = []
        for dependency in phase.get("depends_on", []):
            if dependency == phase_id:
                findings.append(
                    f"phase.self_dependency $.phases: {phase_id!r} depends on itself"
                )
            elif dependency not in phases_by_id:
                findings.append(
                    "phase.unknown_dependency $.phases: "
                    f"{phase_id!r} depends on unknown phase {dependency!r}"
                )
            else:
                phase_graph[phase_id].append(str(dependency))
        for task_id in phase.get("task_ids", []):
            if task_id not in tasks_by_id:
                findings.append(
                    "phase.unknown_task $.phases: "
                    f"{phase_id!r} references unknown task {task_id!r}"
                )
            else:
                memberships[str(task_id)].append(phase_id)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit_phase(phase_id: str) -> None:
        if phase_id in visiting:
            findings.append(
                f"phase.dependency_cycle $.phases: cycle includes {phase_id!r}"
            )
            return
        if phase_id in visited:
            return
        visiting.add(phase_id)
        for dependency in phase_graph.get(phase_id, []):
            visit_phase(dependency)
        visiting.remove(phase_id)
        visited.add(phase_id)

    for phase_id in phase_graph:
        visit_phase(phase_id)

    for task_id, task in tasks_by_id.items():
        declared_phase = task.get("phase_id")
        if declared_phase not in phases_by_id:
            findings.append(
                f"task.unknown_phase $.tasks: {task_id!r} names unknown phase {declared_phase!r}"
            )
        if memberships[task_id] != [declared_phase]:
            findings.append(
                "task.phase_membership_mismatch $.tasks: "
                f"{task_id!r} must appear exactly once in phase {declared_phase!r}"
            )
    return findings


def _semantic_findings(plan: Mapping[str, Any]) -> list[str]:
    tasks = plan.get("tasks")
    if not isinstance(tasks, list):
        return []
    findings: list[str] = []
    by_id: dict[str, Mapping[str, Any]] = {}
    for index, task in enumerate(tasks):
        if not isinstance(task, Mapping) or not isinstance(task.get("task_id"), str):
            continue
        task_id = str(task["task_id"])
        if task_id in by_id:
            findings.append(
                f"task.duplicate_id $.tasks[{index}]: duplicate task_id {task_id!r}"
            )
        else:
            by_id[task_id] = task
    active = [
        task_id for task_id, task in by_id.items() if task.get("status") == "in_progress"
    ]
    if len(active) > 1:
        findings.append(
            "plan.multiple_active_tasks $.tasks: "
            f"serial plan has multiple in_progress tasks {active!r}"
        )

    graph: dict[str, list[str]] = {}
    for task_id, task in by_id.items():
        dependencies = task.get("depends_on")
        if not isinstance(dependencies, list):
            continue
        graph[task_id] = []
        for dependency in dependencies:
            if not isinstance(dependency, str):
                continue
            if dependency == task_id:
                findings.append(
                    f"task.self_dependency $.tasks: {task_id!r} depends on itself"
                )
            elif dependency not in by_id:
                findings.append(
                    f"task.unknown_dependency $.tasks: {task_id!r} "
                    f"depends on unknown task {dependency!r}"
                )
            else:
                graph[task_id].append(dependency)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            findings.append(f"task.dependency_cycle $.tasks: cycle includes {task_id!r}")
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in graph.get(task_id, []):
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in graph:
        visit(task_id)

    for task_id, task in by_id.items():
        if task.get("status") != "completed":
            continue
        for dependency in graph.get(task_id, []):
            if by_id[dependency].get("status") not in TERMINAL_TASK_STATUSES:
                findings.append(
                    "task.completed_dependency_incomplete $.tasks: "
                    f"{task_id!r} is completed before dependency {dependency!r}"
                )
    if plan.get("status") == "completed":
        incomplete = [
            task_id
            for task_id, task in by_id.items()
            if task.get("status") not in TERMINAL_TASK_STATUSES
        ]
        if incomplete:
            findings.append(
                "plan.completed_tasks_incomplete $.status: "
                f"completed plan has nonterminal tasks {incomplete!r}"
            )
    if plan.get("schema_version") == PLAN_SCHEMA_VERSION:
        findings.extend(_immutable_v2_findings(plan, by_id))
    return sorted(set(findings))


def validate_implementation_plan(
    plan: Any,
    *,
    schema_path: str | Path,
) -> list[str]:
    """Return deterministic structural and semantic plan findings."""

    issues = validate_instance(plan, schema_path)
    findings = format_issues(issues).splitlines() if issues else []
    if not issues and isinstance(plan, Mapping):
        findings.extend(_semantic_findings(plan))
    return sorted(set(findings))


def require_implementation_plan(
    plan: Mapping[str, Any],
    *,
    schema_path: str | Path,
) -> dict[str, Any]:
    candidate = copy.deepcopy(dict(plan))
    findings = validate_implementation_plan(candidate, schema_path=schema_path)
    if findings:
        raise RecordValidationError(
            "implementation plan failed canonical validation",
            details={"findings": findings},
        )
    if contains_secret(canonical_json_bytes(candidate).decode("utf-8")):
        raise SecurityError(
            "implementation plan appears to contain a secret; redact it before persistence"
        )
    return candidate


def _raise_state_findings(findings: Sequence[str]) -> None:
    if findings:
        raise RecordValidationError(
            "implementation-plan state failed canonical validation",
            details={"findings": sorted(set(findings))},
        )


def validate_plan_state(
    state: Mapping[str, Any],
    *,
    plan: Mapping[str, Any],
    schema_path: str | Path,
    repository_fingerprint: str | None = None,
    additional_tasks: Sequence[Mapping[str, Any]] = (),
) -> None:
    """Validate exact plan/state identity and aggregate canonical parity."""

    issues = validate_instance(state, schema_path)
    findings = format_issues(issues).splitlines() if issues else []
    if issues:
        _raise_state_findings(findings)

    plan_sha256 = content_sha256(plan)
    if state["plan_id"] != plan["plan_id"]:
        findings.append("state.plan_identity_mismatch")
    if state["plan_sha256"] != plan_sha256:
        findings.append("state.plan_hash_mismatch")
    if (
        repository_fingerprint is not None
        and state["repository_fingerprint"] != repository_fingerprint
    ):
        findings.append("state.repository_fingerprint_mismatch")

    plan_tasks = [
        {
            "task_id": item["task_id"],
            "task_sha256": item["task_sha256"],
            "canonical_position": position,
        }
        for position, item in enumerate(plan["tasks"])
    ]
    plan_tasks.extend(copy.deepcopy(dict(item)) for item in additional_tasks)
    task_ids = [item.get("task_id") for item in plan_tasks]
    task_positions = [item.get("canonical_position") for item in plan_tasks]
    if (
        any(
            not isinstance(item.get("task_id"), str)
            or not SHA256_RE.fullmatch(str(item.get("task_sha256")))
            or not isinstance(item.get("canonical_position"), int)
            or int(item["canonical_position"]) < 0
            for item in plan_tasks
        )
        or len(set(task_ids)) != len(task_ids)
        or len(set(task_positions)) != len(task_positions)
    ):
        findings.append("state.additional_task_definition_invalid")
        _raise_state_findings(findings)
    plan_tasks.sort(
        key=lambda item: (
            int(item.get("canonical_position", -1)),
            str(item.get("task_id", "")),
        )
    )
    state_tasks = list(state["tasks"])
    plan_identities = [
        (item["task_id"], item["task_sha256"]) for item in plan_tasks
    ]
    state_identities = [
        (item["task_id"], item["task_sha256"]) for item in state_tasks
    ]
    if state_identities != plan_identities:
        findings.append("state.task_identity_or_order_mismatch")

    task_counter_names = (
        "worker_discussions",
        "continue_invocations",
        "agentjobs",
        "provider_creates",
        "successor_creates",
    )
    for name in task_counter_names:
        if state["counters"][name] != sum(
            item["counters"][name] for item in state_tasks
        ):
            findings.append(f"state.counter_mismatch:{name}")
    if state["counters"]["tasks_completed"] != sum(
        item["status"] == "completed" for item in state_tasks
    ):
        findings.append("state.counter_mismatch:tasks_completed")
    if state["counters"]["tasks_superseded"] != sum(
        item["status"] == "superseded" for item in state_tasks
    ):
        findings.append("state.counter_mismatch:tasks_superseded")
    if state["counters"]["protected_stops"] != sum(
        item["status"] in PROTECTED_STOP_TASK_STATUSES for item in state_tasks
    ):
        findings.append("state.counter_mismatch:protected_stops")

    generations = [
        int(item["generation"])
        for item in state_tasks
        if item["generation"] is not None
    ]
    if state["current_generation"] != max(generations, default=0):
        findings.append("state.current_generation_mismatch")

    active = [item for item in state_tasks if item["status"] in ACTIVE_TASK_STATUSES]
    if active:
        item = active[0]
        expected_phase = {
            "reserved": "task_reserved",
            "active": "task_active",
            "verifying": "task_verifying",
        }[item["status"]]
        lease = state["lease"]
        if state["active_task_id"] != item["task_id"]:
            findings.append("state.active_task_identity_mismatch")
        if state["phase"] != expected_phase:
            findings.append("state.active_task_phase_mismatch")
        if (
            not isinstance(lease, Mapping)
            or lease.get("task_id") != item["task_id"]
            or lease.get("generation") != item["generation"]
            or lease.get("repository_fingerprint")
            != state["repository_fingerprint"]
        ):
            findings.append("state.active_task_lease_mismatch")

    fingerprints = state["fingerprints"]
    if fingerprints["history"][0] != fingerprints["initial"]:
        findings.append("state.initial_fingerprint_mismatch")
    if fingerprints["history"][-1] != fingerprints["current"]:
        findings.append("state.current_fingerprint_mismatch")

    if contains_secret(canonical_json_bytes(state).decode("utf-8")):
        findings.append("state.secret_detected")
    _raise_state_findings(findings)


def append_plan_journal(
    journal: list[dict[str, Any]],
    kind: str,
    payload: Mapping[str, Any],
) -> str:
    if kind not in PLAN_JOURNAL_KINDS:
        raise RecordValidationError(f"invalid plan journal kind: {kind!r}")
    body = copy.deepcopy(dict(payload))
    if contains_secret(canonical_json_bytes(body).decode("utf-8")):
        raise SecurityError("plan journal payload appears to contain a secret")
    prior_hash = journal[-1]["event_hash"] if journal else None
    core = {
        "sequence": len(journal) + 1,
        "kind": kind,
        "payload": body,
        "prior_hash": prior_hash,
    }
    event_hash = content_sha256(core)
    journal.append({**core, "event_hash": event_hash})
    return event_hash


def validate_plan_journal(journal: Sequence[Mapping[str, Any]]) -> str | None:
    prior_hash: str | None = None
    for sequence, entry in enumerate(journal, 1):
        if entry.get("sequence") != sequence:
            raise RecordValidationError("plan journal sequence is not contiguous")
        if entry.get("kind") not in PLAN_JOURNAL_KINDS:
            raise RecordValidationError("plan journal kind is invalid")
        if entry.get("prior_hash") != prior_hash:
            raise RecordValidationError("plan journal prior hash is invalid")
        payload = entry.get("payload")
        if not isinstance(payload, Mapping):
            raise RecordValidationError("plan journal payload must be an object")
        core = {
            "sequence": sequence,
            "kind": entry["kind"],
            "payload": dict(payload),
            "prior_hash": prior_hash,
        }
        if entry.get("event_hash") != content_sha256(core):
            raise RecordValidationError("plan journal event hash is invalid")
        prior_hash = str(entry["event_hash"])
    return prior_hash


def build_initial_plan_record(
    *,
    plan: Mapping[str, Any],
    outer_goal_id: str,
    repository_fingerprint: str,
    initial_fingerprint: str,
    timestamp: str,
    plan_schema_path: str | Path,
    state_schema_path: str | Path,
    runtime_profile_version: int = 1,
    activation_sequence: int = 0,
    activation_receipt_sha256: str | None = None,
    execution_profile: Mapping[str, Any] | None = None,
    repository_topology_policy: Mapping[str, Any] | None = None,
    activation_goal_text: str | None = None,
    activation_goal_sha256: str | None = None,
    profile_effective_from_generation: int | None = None,
    repository_binding_sha256: str | None = None,
) -> dict[str, Any]:
    canonical_plan = require_implementation_plan(plan, schema_path=plan_schema_path)
    if canonical_plan["schema_version"] != PLAN_SCHEMA_VERSION:
        raise RecordValidationError(
            "new durable plan state requires immutable implementation-plan v2; "
            "v1 remains reader-compatible only"
        )
    if not isinstance(outer_goal_id, str) or not outer_goal_id:
        raise RecordValidationError("outer_goal_id must be nonblank")
    for label, value in (
        ("repository_fingerprint", repository_fingerprint),
        ("initial_fingerprint", initial_fingerprint),
    ):
        if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
            raise RecordValidationError(f"{label} must be a lowercase SHA-256 value")
    parse_utc(timestamp)

    plan_sha256 = content_sha256(canonical_plan)
    task_states = [
        {
            "task_id": task["task_id"],
            "task_sha256": task["task_sha256"],
            "status": "pending",
            "generation": None,
            "counters": {
                "worker_discussions": 0,
                "continue_invocations": 0,
                "agentjobs": 0,
                "provider_creates": 0,
                "successor_creates": 0,
                "same_task_successors": 0,
            },
            "receipt_link": None,
            "fingerprint_before": None,
            "fingerprint_after": None,
            "terminal_reason": None,
            "updated_at": timestamp,
            "extensions": {},
        }
        for task in canonical_plan["tasks"]
    ]
    state = {
        "schema_version": PLAN_STATE_SCHEMA_VERSION,
        "plan_id": canonical_plan["plan_id"],
        "plan_sha256": plan_sha256,
        "repository_fingerprint": repository_fingerprint,
        "revision": 1,
        "phase": "initialized",
        "current_generation": 0,
        "active_task_id": None,
        "counters": {
            "worker_discussions": 0,
            "continue_invocations": 0,
            "agentjobs": 0,
            "provider_creates": 0,
            "successor_creates": 0,
            "tasks_completed": 0,
            "tasks_superseded": 0,
            "protected_stops": 0,
        },
        "lease": None,
        "evaluation": "unmet",
        "fingerprints": {
            "initial": initial_fingerprint,
            "current": initial_fingerprint,
            "history": [initial_fingerprint],
        },
        "terminal_reason": None,
        "tasks": task_states,
        "updated_at": timestamp,
        "extensions": {},
    }
    validate_plan_state(
        state,
        plan=canonical_plan,
        schema_path=state_schema_path,
        repository_fingerprint=repository_fingerprint,
    )
    journal: list[dict[str, Any]] = []
    append_plan_journal(
        journal,
        "event",
        {
            "event_type": "plan_initialized",
            "plan_id": canonical_plan["plan_id"],
            "plan_sha256": plan_sha256,
            "outer_goal_id": outer_goal_id,
            "repository_fingerprint": repository_fingerprint,
            "timestamp": timestamp,
        },
    )
    record = {
        "plan_id": canonical_plan["plan_id"],
        "outer_goal_id": outer_goal_id,
        "plan_sha256": plan_sha256,
        "effective_plan_sha256": plan_sha256,
        "repository_binding": copy.deepcopy(canonical_plan["repository_binding"]),
        "repository_fingerprint": repository_fingerprint,
        "plan": canonical_plan,
        "state": state,
        "journal": journal,
        "runtime_profile_version": runtime_profile_version,
        "activation_sequence": activation_sequence,
        "activation_receipt_sha256": activation_receipt_sha256,
        "execution_profile": (
            copy.deepcopy(dict(execution_profile))
            if execution_profile is not None
            else None
        ),
        "repository_topology_policy": (
            copy.deepcopy(dict(repository_topology_policy))
            if repository_topology_policy is not None
            else None
        ),
        "activation_goal_text": activation_goal_text,
        "activation_goal_sha256": activation_goal_sha256,
        "profile_effective_from_generation": (
            profile_effective_from_generation
        ),
        "repository_binding_sha256": repository_binding_sha256,
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    validate_runtime_plan_record(
        record,
        plan_schema_path=plan_schema_path,
        state_schema_path=state_schema_path,
    )
    return record


def validate_runtime_plan_record(
    record: Mapping[str, Any],
    *,
    plan_schema_path: str | Path,
    state_schema_path: str | Path,
    additional_tasks: Sequence[Mapping[str, Any]] = (),
) -> None:
    if set(record) != PLAN_RECORD_KEYS:
        raise RecordValidationError(
            "runtime plan record fields do not match the canonical contract",
            details={
                "missing": sorted(PLAN_RECORD_KEYS - set(record)),
                "unexpected": sorted(set(record) - PLAN_RECORD_KEYS),
            },
        )
    plan = require_implementation_plan(record["plan"], schema_path=plan_schema_path)
    if record["plan_id"] != plan["plan_id"]:
        raise RecordValidationError("runtime plan ID does not match plan bytes")
    plan_sha256 = content_sha256(plan)
    if record["plan_sha256"] != plan_sha256:
        raise RecordValidationError("runtime plan hash does not match plan bytes")
    if not SHA256_RE.fullmatch(str(record["effective_plan_sha256"])):
        raise RecordValidationError("effective plan hash is invalid")
    if record["repository_binding"] != plan.get("repository_binding"):
        raise RecordValidationError("runtime repository binding does not match plan bytes")
    if not SHA256_RE.fullmatch(str(record["repository_fingerprint"])):
        raise RecordValidationError("runtime repository fingerprint is invalid")
    runtime_profile_version = record["runtime_profile_version"]
    if runtime_profile_version not in {1, 2}:
        raise RecordValidationError(
            "runtime plan profile version must be 1 or 2"
        )
    profile_fields = {
        "activation_receipt_sha256": record["activation_receipt_sha256"],
        "execution_profile": record["execution_profile"],
        "repository_topology_policy": record[
            "repository_topology_policy"
        ],
        "activation_goal_text": record["activation_goal_text"],
        "activation_goal_sha256": record["activation_goal_sha256"],
        "profile_effective_from_generation": record[
            "profile_effective_from_generation"
        ],
        "repository_binding_sha256": record[
            "repository_binding_sha256"
        ],
    }
    if runtime_profile_version == 1:
        if record["activation_sequence"] != 0 or any(
            value is not None for value in profile_fields.values()
        ):
            raise RecordValidationError(
                "legacy runtime plan profile fields must remain empty"
            )
    else:
        if (
            isinstance(record["activation_sequence"], bool)
            or not isinstance(record["activation_sequence"], int)
            or record["activation_sequence"] < 1
            or any(value is None for value in profile_fields.values())
        ):
            raise RecordValidationError(
                "runtime plan profile v2 fields are incomplete"
            )
        for field_name in (
            "activation_receipt_sha256",
            "activation_goal_sha256",
            "repository_binding_sha256",
        ):
            if not SHA256_RE.fullmatch(str(record[field_name])):
                raise RecordValidationError(
                    f"runtime plan {field_name} is invalid"
                )
        goal_text = record["activation_goal_text"]
        if (
            not isinstance(goal_text, str)
            or not goal_text.strip()
            or goal_text != goal_text.strip()
            or hashlib.sha256(goal_text.encode("utf-8")).hexdigest()
            != record["activation_goal_sha256"]
        ):
            raise RecordValidationError(
                "runtime plan activation goal text/hash is invalid"
            )
        if (
            record["repository_binding_sha256"]
            != content_sha256(record["repository_binding"])
        ):
            raise RecordValidationError(
                "runtime plan repository-binding hash is invalid"
            )
        profile = record["execution_profile"]
        topology = record["repository_topology_policy"]
        if not isinstance(profile, Mapping) or not isinstance(
            topology, Mapping
        ):
            raise RecordValidationError(
                "runtime plan profile and topology policy must be objects"
            )
        expected_profile_hash = content_sha256(
            {
                key: value
                for key, value in profile.items()
                if key != "profile_content_sha256"
            }
        )
        if (
            profile.get("schema_version")
            != "sys4ai.plan-execution-profile.v1"
            or profile.get("profile_content_sha256")
            != expected_profile_hash
            or profile.get("activation_receipt_sha256")
            != record["activation_receipt_sha256"]
            or profile.get("accepted_goal_sha256")
            != record["activation_goal_sha256"]
            or profile.get("accepted_plan_sha256")
            != record["effective_plan_sha256"]
            or profile.get("repository_binding_sha256")
            != record["repository_binding_sha256"]
            or profile.get("current_thread_verification_status")
            != "verified"
            or profile.get("successor_inheritance_required") is not True
            or profile.get("effective_from_generation")
            != record["profile_effective_from_generation"]
            or topology.get("environment_mode")
            != "reuse_bound_checkout"
            or profile.get("repository_topology_policy_sha256")
            != content_sha256(topology)
        ):
            raise RecordValidationError(
                "runtime plan execution-profile bindings are inconsistent"
            )
        effective_generation = record[
            "profile_effective_from_generation"
        ]
        if (
            isinstance(effective_generation, bool)
            or not isinstance(effective_generation, int)
            or effective_generation < 1
        ):
            raise RecordValidationError(
                "runtime plan profile generation is invalid"
            )
    validate_plan_state(
        record["state"],
        plan=plan,
        schema_path=state_schema_path,
        repository_fingerprint=str(record["repository_fingerprint"]),
        additional_tasks=additional_tasks,
    )
    if record["state"]["revision"] < 1:
        raise RecordValidationError("runtime plan revision must be positive")
    parse_utc(str(record["created_at"]))
    parse_utc(str(record["updated_at"]))
    if record["state"]["updated_at"] != record["updated_at"]:
        raise RecordValidationError("runtime plan and state timestamps differ")
    if not isinstance(record["outer_goal_id"], str) or not record["outer_goal_id"]:
        raise RecordValidationError("runtime outer goal ID is invalid")
    journal = record["journal"]
    if not isinstance(journal, list) or not journal:
        raise RecordValidationError("runtime plan requires an initialization journal entry")
    validate_plan_journal(journal)
    initial = journal[0]
    expected_initial = {
        "event_type": "plan_initialized",
        "plan_id": record["plan_id"],
        "plan_sha256": record["plan_sha256"],
        "outer_goal_id": record["outer_goal_id"],
        "repository_fingerprint": record["repository_fingerprint"],
        "timestamp": record["created_at"],
    }
    if (
        initial["kind"] != "event"
        or initial["payload"] != expected_initial
        or initial["prior_hash"] is not None
    ):
        raise RecordValidationError("runtime plan initialization journal entry is invalid")
