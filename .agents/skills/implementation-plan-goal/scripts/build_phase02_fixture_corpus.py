#!/usr/bin/env python3
"""Build or verify the deterministic PHASE-02 fixture corpus."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = SKILL_ROOT.parent
AGENTJOB_SCRIPTS = SKILLS_ROOT / "agentjob-control" / "scripts"
if str(AGENTJOB_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AGENTJOB_SCRIPTS))

from agentjob_runtime.records.canonical import content_sha256


CORPUS_ROOT = SKILL_ROOT / "tests" / "fixtures" / "phase-02"
MATRIX_NAME = "coverage-matrix.json"
PLAN_PATH = SKILL_ROOT / "templates" / "canonical-plan-template.json"
STATE_TEMPLATE = (
    SKILL_ROOT / "templates" / "implementation-plan-state-template.json"
)
RECEIPT_TEMPLATE = SKILL_ROOT / "templates" / "plan-task-receipt-template.json"
RECEIPT_V2_TEMPLATE = (
    SKILL_ROOT / "templates" / "plan-task-receipt-v2-template.json"
)
ENVELOPE_EXAMPLE = SKILL_ROOT / "examples" / "plan-task-envelope.example.json"
ENVELOPE_V2_EXAMPLE = (
    SKILL_ROOT / "examples" / "plan-task-envelope-v2.example.json"
)
ACTIVATION_RECEIPT_EXAMPLE = (
    SKILL_ROOT / "examples" / "plan-activation-receipt.example.json"
)
EXECUTION_PROFILE_EXAMPLE = (
    SKILL_ROOT / "examples" / "plan-execution-profile.example.json"
)
PROVIDER_V2_EXAMPLE = (
    SKILL_ROOT / "examples" / "provider-intent-v2.example.json"
)
CONTROL_EXAMPLES = (
    SKILL_ROOT / "examples" / "plan-control-contracts.example.json"
)
RECEIPT_OUTCOMES = (
    SKILL_ROOT / "examples" / "plan-task-receipt-outcomes.example.json"
)

SOURCE_CLASSES = (
    "structured_plan",
    "partial_plan",
    "task_list",
    "phase_outline",
    "requirements",
    "prose",
    "mixed_source",
)
PLAN_PHASES = (
    "initialized",
    "task_reserved",
    "task_active",
    "task_verifying",
    "continuation_required",
    "completion_candidate",
    "recovery_pending",
    "terminal_complete",
    "terminal_blocked_no_runnable",
    "terminal_awaiting_human",
    "terminal_validation_failed",
    "terminal_capability_blocked",
    "terminal_corrupt_state",
    "terminal_cancelled",
)
TASK_STATUSES = (
    "pending",
    "reserved",
    "active",
    "verifying",
    "completed",
    "blocked",
    "superseded",
    "replan_required",
    "human_gate_required",
    "validation_failed",
    "invocation_unknown",
    "cancelled",
)
RECEIPT_DISPOSITIONS = (
    "blocked",
    "replan_required",
    "human_gate_required",
    "validation_failed",
    "invocation_unknown",
    "cancelled",
    "task_complete",
    "plan_complete",
)
RECEIPT_EXECUTION_OUTCOMES = ("zero_job", "one_job", "unknown")
PROVIDER_OUTCOMES = (
    "intent",
    "returned",
    "failed",
    "ambiguous",
    "timeout",
    "duplicate",
)
SUPERSESSION_TERMINAL_STATUSES = (
    "replan_required",
    "blocked",
    "validation_failed",
    "human_gate_required",
)
SUPERSESSION_REASON_CODES = (
    "plan_task.task_requires_replan",
    "plan_task.scope_violation",
    "plan.validation_failed",
    "plan.human_gate_required",
)
AMENDMENT_EFFECTS = ("add", "replace", "remove", "narrow")
NORMALIZATION_STATUSES = ("candidate", "blocked", "human_gate_required")
SELECTION_OUTCOMES = (
    "selected",
    "no_ready_task",
    "blocked_no_runnable",
    "completion_candidate",
    "invalid",
)
SCHEMA_VERSIONS = (
    "sys4ai.implementation-plan.v1",
    "sys4ai.implementation-plan.v2",
    "sys4ai.implementation-plan-state.v1",
    "sys4ai.plan-task-envelope.v1",
    "sys4ai.plan-task-envelope.v2",
    "sys4ai.plan-task-receipt.v1",
    "sys4ai.plan-task-receipt.v2",
    "sys4ai.plan-activation-receipt.v1",
    "sys4ai.plan-execution-profile.v1",
    "sys4ai.plan-normalization-report.v1",
    "sys4ai.plan-amendment.v1",
    "sys4ai.plan-task-supersession.v1",
    "sys4ai.plan-provider-intent.v1",
    "sys4ai.plan-provider-intent.v2",
    "sys4ai.plan-selection-proof.v1",
)
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


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _clone(value: Any) -> Any:
    return copy.deepcopy(value)


def _finalize(record: Mapping[str, Any]) -> dict[str, Any]:
    value = _clone(dict(record))
    field = CONTENT_HASH_FIELDS.get(str(value.get("schema_version")))
    if field is not None:
        value[field] = content_sha256(
            {key: item for key, item in value.items() if key != field}
        )
    return value


def _legacy_plan() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.implementation-plan.v1",
        "plan_id": "PLAN-PHASE02-LEGACY",
        "title": "Legacy read-compatible Phase 2 fixture",
        "status": "active",
        "serial_execution": True,
        "tasks": [
            {
                "task_id": "TASK-001",
                "task_sha256": "1" * 64,
                "title": "Completed prerequisite",
                "status": "completed",
                "depends_on": [],
                "extensions": {},
            },
            {
                "task_id": "TASK-002",
                "task_sha256": "2" * 64,
                "title": "Pending bounded task",
                "status": "pending",
                "depends_on": ["TASK-001"],
                "extensions": {},
            },
        ],
        "extensions": {},
    }


def _pending_task(definition: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "task_id": definition["task_id"],
        "task_sha256": definition["task_sha256"],
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
        "updated_at": "2026-01-01T00:00:00Z",
        "extensions": {},
    }


def _base_state(plan: Mapping[str, Any]) -> dict[str, Any]:
    initial = "a" * 64
    return {
        "schema_version": "sys4ai.implementation-plan-state.v1",
        "plan_id": plan["plan_id"],
        "plan_sha256": _sha256_bytes(PLAN_PATH.read_bytes()),
        "repository_fingerprint": initial,
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
            "initial": initial,
            "current": initial,
            "history": [initial],
        },
        "terminal_reason": None,
        "tasks": [_pending_task(item) for item in plan["tasks"]],
        "updated_at": "2026-01-01T00:00:00Z",
        "extensions": {},
    }


def _mark_task(
    state: dict[str, Any],
    index: int,
    status: str,
    *,
    generation: int | None = None,
) -> None:
    task = state["tasks"][index]
    task["status"] = status
    if status == "pending":
        return
    task_generation = generation or index + 1
    task["generation"] = task_generation
    task["counters"].update(
        {
            "worker_discussions": 1,
            "continue_invocations": int(status not in {"reserved", "blocked", "human_gate_required", "cancelled"}),
            "agentjobs": int(status in {"verifying", "completed"}),
            "provider_creates": 1,
            "successor_creates": int(status == "completed"),
        }
    )
    if status in {"active", "verifying"}:
        task["fingerprint_before"] = chr(96 + task_generation) * 64
    if status in {
        "completed",
        "blocked",
        "superseded",
        "replan_required",
        "human_gate_required",
        "validation_failed",
        "invocation_unknown",
        "cancelled",
    }:
        task["receipt_link"] = {
            "receipt_id": f"PTR-PHASE02-{task_generation:03d}",
            "receipt_sha256": f"{task_generation % 10}" * 64,
        }
        task["fingerprint_before"] = chr(96 + task_generation) * 64
        task["fingerprint_after"] = chr(97 + task_generation) * 64
        task["terminal_reason"] = (
            None
            if status == "completed"
            else f"Synthetic fixture terminal state: {status}."
        )
    task["updated_at"] = f"2026-01-01T00:{task_generation:02d}:00Z"


def _lease(
    state: Mapping[str, Any],
    *,
    holder_kind: str,
) -> dict[str, Any]:
    task_id = str(state["active_task_id"])
    generation = int(state["current_generation"])
    return {
        "generation": generation,
        "task_id": task_id,
        "holder_kind": holder_kind,
        "holder_token_hash": "d" * 64,
        "transaction_id": f"TX-PHASE02-{generation:03d}",
        "repository_fingerprint": state["repository_fingerprint"],
        "acquired_at": "2026-01-01T00:01:00Z",
        "heartbeat_at": "2026-01-01T00:02:00Z",
        "expires_at": "2026-01-01T00:07:00Z",
    }


def _sync_state(state: dict[str, Any]) -> None:
    counters = state["counters"]
    task_counters = [item["counters"] for item in state["tasks"]]
    for field in (
        "worker_discussions",
        "continue_invocations",
        "agentjobs",
        "provider_creates",
        "successor_creates",
    ):
        counters[field] = sum(int(item[field]) for item in task_counters)
    counters["tasks_completed"] = sum(
        item["status"] == "completed" for item in state["tasks"]
    )
    counters["tasks_superseded"] = sum(
        item["status"] == "superseded" for item in state["tasks"]
    )
    counters["protected_stops"] = sum(
        item["status"]
        in {
            "blocked",
            "replan_required",
            "human_gate_required",
            "validation_failed",
            "invocation_unknown",
            "cancelled",
        }
        for item in state["tasks"]
    )
    generations = [
        int(item["generation"])
        for item in state["tasks"]
        if item["generation"] is not None
    ]
    state["current_generation"] = max(generations, default=0)
    current = "b" * 64 if generations else "a" * 64
    state["repository_fingerprint"] = current
    state["fingerprints"]["current"] = current
    state["fingerprints"]["history"] = (
        ["a" * 64] if current == "a" * 64 else ["a" * 64, current]
    )
    state["updated_at"] = (
        "2026-01-01T00:00:00Z"
        if not generations
        else "2026-01-01T00:20:00Z"
    )


def _state_phase_case(plan: Mapping[str, Any], phase: str) -> dict[str, Any]:
    state = _base_state(plan)
    state["phase"] = phase
    if phase == "task_reserved":
        _mark_task(state, 0, "reserved")
        _sync_state(state)
        state["active_task_id"] = state["tasks"][0]["task_id"]
        state["lease"] = _lease(state, holder_kind="successor_reserved")
    elif phase == "task_active":
        _mark_task(state, 0, "active")
        _sync_state(state)
        state["active_task_id"] = state["tasks"][0]["task_id"]
        state["lease"] = _lease(state, holder_kind="worker")
    elif phase == "task_verifying":
        _mark_task(state, 0, "verifying")
        _sync_state(state)
        state["active_task_id"] = state["tasks"][0]["task_id"]
        state["lease"] = _lease(state, holder_kind="worker")
    elif phase == "continuation_required":
        _mark_task(state, 0, "completed")
        _sync_state(state)
    elif phase == "completion_candidate":
        for index in range(len(state["tasks"])):
            _mark_task(state, index, "completed")
        _sync_state(state)
    elif phase == "recovery_pending":
        _mark_task(state, 0, "invocation_unknown")
        _sync_state(state)
        state["evaluation"] = "indeterminate"
        state["terminal_reason"] = "Synthetic provider or invocation recovery is required."
    elif phase == "terminal_complete":
        for index in range(len(state["tasks"])):
            _mark_task(state, index, "completed")
        _sync_state(state)
        state["evaluation"] = "met"
        state["terminal_reason"] = "All synthetic plan tasks and gates are complete."
    elif phase == "terminal_blocked_no_runnable":
        _mark_task(state, 0, "blocked")
        _sync_state(state)
        state["terminal_reason"] = "No synthetic dependency-ready task remains."
    elif phase == "terminal_awaiting_human":
        _mark_task(state, 0, "human_gate_required")
        _sync_state(state)
        state["terminal_reason"] = "Synthetic human authority is required."
    elif phase == "terminal_validation_failed":
        _mark_task(state, 0, "validation_failed")
        _sync_state(state)
        state["terminal_reason"] = "Synthetic validation evidence failed."
    elif phase == "terminal_capability_blocked":
        _mark_task(state, 0, "blocked")
        _sync_state(state)
        state["terminal_reason"] = "A synthetic required capability is unavailable."
    elif phase == "terminal_corrupt_state":
        state["evaluation"] = "indeterminate"
        state["terminal_reason"] = "Synthetic state corruption was detected."
    elif phase == "terminal_cancelled":
        _mark_task(state, 0, "cancelled")
        _sync_state(state)
        state["terminal_reason"] = "The synthetic plan was explicitly cancelled."
    return state


def _state_task_status_case(
    plan: Mapping[str, Any],
    status: str,
) -> dict[str, Any]:
    phase_by_status = {
        "pending": "initialized",
        "reserved": "task_reserved",
        "active": "task_active",
        "verifying": "task_verifying",
        "completed": "continuation_required",
        "blocked": "terminal_blocked_no_runnable",
        "human_gate_required": "terminal_awaiting_human",
        "validation_failed": "terminal_validation_failed",
        "invocation_unknown": "recovery_pending",
        "cancelled": "terminal_cancelled",
    }
    if status in phase_by_status:
        return _state_phase_case(plan, phase_by_status[status])
    state = _base_state(plan)
    state["phase"] = "continuation_required"
    _mark_task(state, 0, status)
    _sync_state(state)
    return state


def _receipt_case(
    template: Mapping[str, Any],
    case: Mapping[str, Any],
) -> dict[str, Any]:
    receipt = _clone(dict(template))
    case_id = str(case["case_id"])
    receipt["receipt_id"] = f"PTR-PHASE02-{case_id.upper()}"
    execution = receipt["execution"]
    execution["outcome"] = case["execution_outcome"]
    execution["continue_invocations"] = case["continue_invocations"]
    execution["agentjobs"] = case["agentjobs"]
    receipt["disposition"] = case["disposition"]
    receipt["reason_code"] = f"fixture.{case_id}"
    receipt["terminal_reason"] = (
        f"Synthetic protected fixture outcome: {case_id}."
        if case["terminal_reason_required"]
        else None
    )
    receipt["recovery"]["status"] = case["recovery_status"]
    receipt["replanning"]["status"] = case["replanning_status"]
    receipt["coordinator_action"]["kind"] = case["coordinator_action"]
    receipt["coordinator_action"]["next_task_id"] = (
        "TASK-EXAMPLE-002"
        if case["coordinator_action"] == "dispatch_next_task"
        else None
    )
    receipt["direct_evidence"]["approvals"][0]["status"] = (
        "missing"
        if case["disposition"] == "human_gate_required"
        else "not_required"
    )
    receipt["direct_evidence"]["validator_results"][0]["status"] = (
        "fail" if case["disposition"] == "validation_failed" else "pass"
    )
    if execution["outcome"] == "one_job":
        execution["agent_job_id"] = "AJ-PHASE02-001"
        execution["zero_job_reason"] = None
    elif execution["outcome"] == "unknown":
        execution["agent_job_id"] = None
        execution["zero_job_reason"] = (
            "The synthetic consumed invocation outcome is unknown."
        )
    else:
        execution["agent_job_id"] = None
        execution["zero_job_reason"] = "No AgentJob was executed."
    receipt["direct_evidence"]["plan_completion"] = (
        {
            "task_receipts": [
                {
                    "receipt_id": receipt["receipt_id"],
                    "receipt_sha256": "9" * 64,
                }
            ],
            "phase_gate_receipts": [
                {
                    "receipt_id": "PGR-PHASE02-001",
                    "receipt_sha256": "a" * 64,
                }
            ],
            "final_validator_refs": [
                "tests/fixtures/phase-02/coverage-matrix.json"
            ],
            "completion_contract_status": "pass",
        }
        if case["disposition"] == "plan_complete"
        else None
    )
    return _finalize(receipt)


def _normalization_case(
    base: Mapping[str, Any],
    status: str,
) -> dict[str, Any]:
    record = _clone(dict(base))
    record["status"] = status
    if status != "candidate":
        record["candidate_plan_sha256"] = None
        record["canonicalization_only"] = False
        record["findings"] = [
            {
                "code": f"fixture.{status}",
                "severity": (
                    "human_gate" if status == "human_gate_required" else "blocking"
                ),
                "message": f"Synthetic normalization outcome: {status}.",
                "source_ids": [record["sources"][0]["source_id"]],
            }
        ]
    return _finalize(record)


def _amendment_case(
    base: Mapping[str, Any],
    effect: str,
) -> dict[str, Any]:
    record = _clone(dict(base))
    operation = record["operations"][0]
    operation["effect"] = effect
    operation["narrows_authority"] = effect == "narrow"
    if effect == "add":
        operation["prior_value_sha256"] = None
        operation["new_value_sha256"] = "7" * 64
    elif effect == "remove":
        operation["prior_value_sha256"] = "7" * 64
        operation["new_value_sha256"] = None
    else:
        operation["prior_value_sha256"] = "7" * 64
        operation["new_value_sha256"] = "8" * 64
    return _finalize(record)


def _supersession_case(
    base: Mapping[str, Any],
    terminal_status: str,
    reason_code: str,
) -> dict[str, Any]:
    record = _clone(dict(base))
    record["original_task"]["terminal_status"] = terminal_status
    record["reason_code"] = reason_code
    record["reason"] = (
        f"Synthetic append-only supersession path for {terminal_status}."
    )
    return _finalize(record)


def _provider_case(
    base: Mapping[str, Any],
    status: str,
) -> dict[str, Any]:
    record = _clone(dict(base))
    record["status"] = status
    record["conflicting_thread_ids"] = []
    record["returned_thread_id"] = None
    record["provider_response_sha256"] = None
    record["recovery"] = {
        "status": "not_required",
        "reason": None,
        "evidence_refs": [],
    }
    if status == "intent":
        record["create_attempts"] = 0
        record["finalized"] = False
    elif status == "returned":
        record["create_attempts"] = 1
        record["returned_thread_id"] = "THREAD-SUCCESSOR-001"
        record["provider_response_sha256"] = "a" * 64
        record["finalized"] = True
    elif status == "failed":
        record["create_attempts"] = 1
        record["provider_response_sha256"] = "b" * 64
        record["finalized"] = True
    else:
        record["create_attempts"] = 1
        record["provider_response_sha256"] = "c" * 64
        record["finalized"] = True
        record["recovery"] = {
            "status": "required",
            "reason": f"Synthetic provider outcome requires recovery: {status}.",
            "evidence_refs": ["evidence/provider-query.md"],
        }
        if status == "duplicate":
            record["conflicting_thread_ids"] = [
                "THREAD-CONFLICT-001",
                "THREAD-CONFLICT-002",
            ]
    return _finalize(record)


def _profile_provider_returned(base: Mapping[str, Any]) -> dict[str, Any]:
    record = _clone(dict(base))
    record.update(
        {
            "status": "returned",
            "create_attempts": 1,
            "returned_thread_id": "thread-worker-example",
            "provider_response_sha256": "a" * 64,
            "effective_reasoning_effort": record[
                "requested_reasoning_effort"
            ],
            "profile_verification_status": "verified",
            "profile_evidence_ref": "evidence/worker-thread-profile.md",
            "observed_topology_sha256": "b" * 64,
            "finalized": True,
        }
    )
    return _finalize(record)


def _activation_transition_case() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.plan-activation-transition-fixture.v1",
        "prior_selection_source": "user_override",
        "prior_reasoning_effort": "high",
        "event": "goal_edit",
        "next_selection_source": "user_override",
        "next_reasoning_effort": "high",
        "latest_presentation_sequence": 2,
        "accepted_presentation_sequence": 2,
    }


def _selection_case(
    base: Mapping[str, Any],
    outcome: str,
) -> dict[str, Any]:
    record = _clone(dict(base))
    record["outcome"] = outcome
    if outcome == "selected":
        return _finalize(record)
    record["selected_task"] = None
    record["blocking_reasons"] = []
    record["active_task_ids"] = []
    task = record["ordered_tasks"][0]
    task["dependency_ready"] = False
    if outcome == "no_ready_task":
        task["status"] = "blocked"
    elif outcome == "blocked_no_runnable":
        task["status"] = "active"
        record["active_task_ids"] = [task["task_id"]]
        record["blocking_reasons"] = ["selection.active_task_present"]
    elif outcome == "completion_candidate":
        task["status"] = "completed"
    else:
        task["status"] = "recovery_pending"
        record["blocking_reasons"] = ["selection.state_not_schedulable"]
    return _finalize(record)


def build_corpus() -> tuple[dict[str, bytes], dict[str, Any]]:
    """Return generated relative-path bytes and the coverage matrix."""

    plan = _load(PLAN_PATH)
    receipt_template = _load(RECEIPT_TEMPLATE)
    receipt_v2_template = _load(RECEIPT_V2_TEMPLATE)
    envelope = _load(ENVELOPE_EXAMPLE)
    envelope_v2 = _load(ENVELOPE_V2_EXAMPLE)
    activation_receipt = _load(ACTIVATION_RECEIPT_EXAMPLE)
    execution_profile = _load(EXECUTION_PROFILE_EXAMPLE)
    provider_v2 = _profile_provider_returned(_load(PROVIDER_V2_EXAMPLE))
    activation_transition = _activation_transition_case()
    controls = _load(CONTROL_EXAMPLES)
    receipt_outcomes = _load(RECEIPT_OUTCOMES)["cases"]

    files: dict[str, bytes] = {}
    values: dict[str, Any] = {}
    source_cases: list[dict[str, Any]] = []
    positive_cases: list[dict[str, Any]] = []
    schema_negative_cases: list[dict[str, Any]] = []
    semantic_negative_cases: list[dict[str, Any]] = []
    profile_semantic_negative_cases: list[dict[str, Any]] = []

    def add_text(path: str, text: str) -> None:
        files[path] = text.encode("utf-8")

    def add_json(path: str, value: Any) -> None:
        if path in files:
            raise ValueError(f"duplicate generated fixture path: {path}")
        values[path] = _clone(value)
        files[path] = _json_bytes(value)

    def add_positive(
        case_id: str,
        path: str,
        value: Any,
        profile: str,
        **dimensions: str,
    ) -> None:
        add_json(path, value)
        positive_cases.append(
            {
                "case_id": case_id,
                "path": path,
                "record_profile": profile,
                "dimensions": dict(sorted(dimensions.items())),
            }
        )

    source_values = {
        "sources/structured-plan.json": plan,
        "sources/partial-plan.json": {
            "plan_id": "PLAN-PARTIAL-PHASE02",
            "title": "Partial plan fixture",
            "tasks": [{"title": "One incomplete task"}],
        },
        "sources/task-list.json": [
            "Implement the bounded behavior",
            "Verify the bounded behavior",
        ],
        "sources/phase-outline.json": {
            "phases": [
                {"title": "Establish the baseline"},
                {"title": "Deliver the bounded change"},
            ]
        },
        "sources/requirements.json": {
            "requirements": [
                "The implementation must be deterministic.",
                "The result must be directly verified.",
            ]
        },
        "sources/mixed-task-list.json": [
            "Implement the bounded behavior",
            "Verify the bounded behavior",
        ],
        "sources/mixed-requirements.json": {
            "requirements": [
                "The implementation must remain serial.",
                "The result must preserve exact task identity.",
            ]
        },
    }
    for path, value in source_values.items():
        add_json(path, value)
    add_text(
        "sources/prose.txt",
        "Improve the bounded widget behavior while preserving existing scope.\n",
    )
    source_cases.extend(
        [
            {
                "case_id": "source-structured-plan",
                "source_class": "structured_plan",
                "paths": ["sources/structured-plan.json"],
            },
            {
                "case_id": "source-partial-plan",
                "source_class": "partial_plan",
                "paths": ["sources/partial-plan.json"],
            },
            {
                "case_id": "source-task-list",
                "source_class": "task_list",
                "paths": ["sources/task-list.json"],
            },
            {
                "case_id": "source-phase-outline",
                "source_class": "phase_outline",
                "paths": ["sources/phase-outline.json"],
            },
            {
                "case_id": "source-requirements",
                "source_class": "requirements",
                "paths": ["sources/requirements.json"],
            },
            {
                "case_id": "source-prose",
                "source_class": "prose",
                "paths": ["sources/prose.txt"],
            },
            {
                "case_id": "source-mixed",
                "source_class": "mixed_source",
                "paths": [
                    "sources/mixed-task-list.json",
                    "sources/mixed-requirements.json",
                ],
            },
        ]
    )

    add_positive(
        "plan-v1",
        "records/positive/implementation-plan-v1.json",
        _legacy_plan(),
        "implementation_plan",
        schema_version="sys4ai.implementation-plan.v1",
    )
    add_positive(
        "plan-v2",
        "records/positive/implementation-plan-v2.json",
        plan,
        "implementation_plan",
        schema_version="sys4ai.implementation-plan.v2",
    )

    phase_paths: dict[str, str] = {}
    for phase in PLAN_PHASES:
        path = f"records/positive/state-phase-{phase}.json"
        phase_paths[phase] = path
        add_positive(
            f"state-phase-{phase}",
            path,
            _state_phase_case(plan, phase),
            "implementation_plan_state",
            plan_phase=phase,
        )
    for status in ("superseded", "replan_required"):
        add_positive(
            f"state-task-status-{status}",
            f"records/positive/state-task-status-{status}.json",
            _state_task_status_case(plan, status),
            "implementation_plan_state",
            task_status=status,
        )

    add_positive(
        "plan-task-envelope",
        "records/positive/plan-task-envelope.json",
        envelope,
        "plan_task_envelope",
        schema_version="sys4ai.plan-task-envelope.v1",
    )
    activation_path = "records/positive/plan-activation-receipt.json"
    add_positive(
        "plan-activation-receipt",
        activation_path,
        activation_receipt,
        "plan_activation_receipt",
        schema_version="sys4ai.plan-activation-receipt.v1",
    )
    profile_path = "records/positive/plan-execution-profile.json"
    add_positive(
        "plan-execution-profile",
        profile_path,
        execution_profile,
        "plan_execution_profile",
        schema_version="sys4ai.plan-execution-profile.v1",
    )
    envelope_v2_path = "records/positive/plan-task-envelope-v2.json"
    add_positive(
        "plan-task-envelope-v2",
        envelope_v2_path,
        envelope_v2,
        "plan_task_envelope",
        schema_version="sys4ai.plan-task-envelope.v2",
    )
    receipt_v2_path = "records/positive/plan-task-receipt-v2.json"
    add_positive(
        "plan-task-receipt-v2",
        receipt_v2_path,
        receipt_v2_template,
        "plan_task_receipt",
        schema_version="sys4ai.plan-task-receipt.v2",
    )
    provider_v2_path = "records/positive/provider-v2-returned.json"
    add_positive(
        "provider-v2-returned",
        provider_v2_path,
        provider_v2,
        "provider_intent",
        schema_version="sys4ai.plan-provider-intent.v2",
    )
    transition_path = "records/positive/activation-transition.json"
    add_json(transition_path, activation_transition)

    receipt_paths: dict[str, str] = {}
    for case in receipt_outcomes:
        case_id = str(case["case_id"])
        path = f"records/positive/receipt-{case_id}.json"
        receipt_paths[case_id] = path
        add_positive(
            f"receipt-{case_id}",
            path,
            _receipt_case(receipt_template, case),
            "plan_task_receipt",
            receipt_disposition=str(case["disposition"]),
            receipt_execution_outcome=str(case["execution_outcome"]),
        )

    normalization_paths: dict[str, str] = {}
    for status in NORMALIZATION_STATUSES:
        path = f"records/positive/normalization-{status}.json"
        normalization_paths[status] = path
        add_positive(
            f"normalization-{status}",
            path,
            _normalization_case(controls["normalization_report"], status),
            "normalization_report",
            normalization_status=status,
        )

    amendment_paths: dict[str, str] = {}
    for effect in AMENDMENT_EFFECTS:
        path = f"records/positive/amendment-{effect}.json"
        amendment_paths[effect] = path
        add_positive(
            f"amendment-{effect}",
            path,
            _amendment_case(controls["plan_amendment"], effect),
            "plan_amendment",
            amendment_effect=effect,
        )

    supersession_paths: dict[str, str] = {}
    for terminal_status, reason_code in zip(
        SUPERSESSION_TERMINAL_STATUSES,
        SUPERSESSION_REASON_CODES,
        strict=True,
    ):
        path = f"records/positive/supersession-{terminal_status}.json"
        supersession_paths[terminal_status] = path
        add_positive(
            f"supersession-{terminal_status}",
            path,
            _supersession_case(
                controls["task_supersession"],
                terminal_status,
                reason_code,
            ),
            "task_supersession",
            supersession_terminal_status=terminal_status,
            supersession_reason_code=reason_code,
        )

    provider_paths: dict[str, str] = {}
    for status in PROVIDER_OUTCOMES:
        path = f"records/positive/provider-{status}.json"
        provider_paths[status] = path
        add_positive(
            f"provider-{status}",
            path,
            _provider_case(controls["provider_intent"], status),
            "provider_intent",
            provider_outcome=status,
        )

    selection_paths: dict[str, str] = {}
    for outcome in SELECTION_OUTCOMES:
        path = f"records/positive/selection-{outcome}.json"
        selection_paths[outcome] = path
        add_positive(
            f"selection-{outcome}",
            path,
            _selection_case(controls["selection_proof"], outcome),
            "selection_proof",
            selection_outcome=outcome,
        )

    def schema_negative(
        case_id: str,
        base_path: str,
        value: Any,
        fault_path: str,
        expected_reason_codes: Sequence[str],
    ) -> None:
        path = f"records/negative/schema/{case_id}.json"
        add_json(path, value)
        schema_negative_cases.append(
            {
                "case_id": case_id,
                "path": path,
                "base_path": base_path,
                "fault_path": fault_path,
                "expected_reason_codes": list(expected_reason_codes),
            }
        )

    base = _clone(values["records/positive/implementation-plan-v2.json"])
    base["unexpected"] = True
    schema_negative(
        "plan-unknown-field",
        "records/positive/implementation-plan-v2.json",
        base,
        "$.unexpected",
        ["record.schema_invalid"],
    )

    active_state_path = phase_paths["task_active"]
    base = _clone(values[active_state_path])
    base["tasks"][2]["status"] = "active"
    schema_negative(
        "state-second-active-task",
        active_state_path,
        base,
        "$.tasks[2].status",
        ["record.schema_invalid"],
    )

    envelope_path = "records/positive/plan-task-envelope.json"
    base = _clone(values[envelope_path])
    base["max_agentjobs"] = 2
    schema_negative(
        "envelope-second-agentjob",
        envelope_path,
        base,
        "$.max_agentjobs",
        ["record.schema_invalid"],
    )

    receipt_path = receipt_paths["task-complete"]
    base = _clone(values[receipt_path])
    base["execution"]["same_task_successors"] = 1
    schema_negative(
        "receipt-same-task-successor",
        receipt_path,
        base,
        "$.execution.same_task_successors",
        ["record.schema_invalid"],
    )

    base = _clone(values[receipt_path])
    base["reason_code"] = "fixture.changed-without-rehash"
    schema_negative(
        "receipt-stale-content-hash",
        receipt_path,
        base,
        "$.reason_code",
        ["record.content_hash_mismatch"],
    )

    base = _clone(values[receipt_path])
    base["direct_evidence"]["changed_paths"][0] = "../outside"
    schema_negative(
        "receipt-unsafe-path",
        receipt_path,
        base,
        "$.direct_evidence.changed_paths[0]",
        ["record.schema_invalid"],
    )

    normalization_path = normalization_paths["candidate"]
    base = _clone(values[normalization_path])
    base["traceability"][0]["generated"] = True
    schema_negative(
        "normalization-generated-flag",
        normalization_path,
        base,
        "$.traceability[0].generated",
        ["record.schema_invalid"],
    )

    amendment_path = amendment_paths["add"]
    base = _clone(values[amendment_path])
    base["operations"][0]["protected_effects_added"] = True
    schema_negative(
        "amendment-protected-effect",
        amendment_path,
        base,
        "$.operations[0].protected_effects_added",
        ["record.schema_invalid"],
    )

    supersession_path = supersession_paths["replan_required"]
    base = _clone(values[supersession_path])
    base["original_redispatch_forbidden"] = False
    schema_negative(
        "supersession-original-redispatch",
        supersession_path,
        base,
        "$.original_redispatch_forbidden",
        ["record.schema_invalid"],
    )

    provider_path = provider_paths["ambiguous"]
    base = _clone(values[provider_path])
    base["retry_authorized"] = True
    schema_negative(
        "provider-retry-authorized",
        provider_path,
        base,
        "$.retry_authorized",
        ["record.schema_invalid"],
    )

    selection_path = selection_paths["selected"]
    base = _clone(values[selection_path])
    base["revision_bound"] = False
    schema_negative(
        "selection-not-revision-bound",
        selection_path,
        base,
        "$.revision_bound",
        ["record.schema_invalid"],
    )

    base = _clone(values[activation_path])
    base["current_thread_verification_status"] = "pending"
    schema_negative(
        "activation-current-thread-unverified",
        activation_path,
        base,
        "$.current_thread_verification_status",
        ["record.schema_invalid"],
    )

    base = _clone(values[profile_path])
    base["successor_inheritance_required"] = False
    schema_negative(
        "profile-successor-inheritance-missing",
        profile_path,
        base,
        "$.successor_inheritance_required",
        ["record.schema_invalid"],
    )

    base = _clone(values[provider_v2_path])
    base["profile_evidence_ref"] = None
    schema_negative(
        "provider-v2-verified-without-evidence",
        provider_v2_path,
        base,
        "$.profile_evidence_ref",
        ["record.schema_invalid"],
    )

    base = _clone(values[envelope_v2_path])
    base["repository_topology_policy"]["branch_creation_authorized"] = True
    schema_negative(
        "envelope-v2-branch-authority-default",
        envelope_v2_path,
        base,
        "$.repository_topology_policy.branch_creation_authorized",
        ["record.schema_invalid"],
    )

    base = _clone(values[envelope_v2_path])
    base["repository_topology_policy"]["worktree_creation_authorized"] = True
    schema_negative(
        "envelope-v2-worktree-authority-default",
        envelope_v2_path,
        base,
        "$.repository_topology_policy.worktree_creation_authorized",
        ["record.schema_invalid"],
    )

    contract_set = {
        "normalization_report": normalization_path,
        "plan_amendment": amendment_path,
        "task_supersession": supersession_path,
        "provider_intent": provider_path,
        "selection_proof": selection_path,
    }
    profile_contract_set = {
        "activation_receipt": activation_path,
        "execution_profile": profile_path,
        "task_envelope": envelope_v2_path,
        "provider_intent": provider_v2_path,
        "task_receipt": receipt_v2_path,
        "activation_transition": transition_path,
    }

    def semantic_negative(
        case_id: str,
        record_key: str,
        base_path: str,
        value: Any,
        fault_path: str,
        expected_reason_codes: Sequence[str],
    ) -> None:
        path = f"records/negative/semantic/{case_id}.json"
        add_json(path, value)
        semantic_negative_cases.append(
            {
                "case_id": case_id,
                "record_key": record_key,
                "path": path,
                "base_path": base_path,
                "fault_path": fault_path,
                "expected_reason_codes": list(expected_reason_codes),
            }
        )

    base = _clone(values[normalization_path])
    base["sources"][0]["authority"] = "supplemental"
    semantic_negative(
        "normalization-accepted-authority-missing",
        "normalization_report",
        normalization_path,
        base,
        "$.sources[0].authority",
        ["normalization.accepted_authority_missing"],
    )

    base = _clone(values[amendment_path])
    base["new_effective_plan_sha256"] = base["prior_effective_plan_sha256"]
    semantic_negative(
        "amendment-no-effect",
        "plan_amendment",
        amendment_path,
        base,
        "$.new_effective_plan_sha256",
        ["amendment.no_effect"],
    )

    base = _clone(values[supersession_path])
    base["replacement_tasks"][0]["task_id"] = base["original_task"]["task_id"]
    semantic_negative(
        "supersession-original-task-reused",
        "task_supersession",
        supersession_path,
        base,
        "$.replacement_tasks[0].task_id",
        ["supersession.original_task_reused"],
    )

    base = _clone(values[supersession_path])
    base["replacement_tasks"][0]["depends_on"] = [
        base["replacement_tasks"][1]["task_id"]
    ]
    semantic_negative(
        "supersession-replacement-cycle",
        "task_supersession",
        supersession_path,
        base,
        "$.replacement_tasks[0].depends_on",
        ["supersession.replacement_cycle"],
    )

    base = _clone(values[provider_path])
    base["returned_thread_id"] = base["predecessor_thread_id"]
    semantic_negative(
        "provider-predecessor-reused",
        "provider_intent",
        provider_path,
        base,
        "$.returned_thread_id",
        ["provider.predecessor_reused"],
    )

    base = _clone(values[selection_path])
    base["selected_task"]["task_id"] = "TASK-NOT-FIRST-READY"
    semantic_negative(
        "selection-not-first-ready",
        "selection_proof",
        selection_path,
        base,
        "$.selected_task.task_id",
        ["selection.not_first_ready_task"],
    )

    base = _clone(values[provider_path])
    base["plan_id"] = "PLAN-DIFFERENT-001"
    semantic_negative(
        "contract-plan-identity-mismatch",
        "provider_intent",
        provider_path,
        base,
        "$.plan_id",
        ["contracts.plan_id_mismatch"],
    )

    def profile_semantic_negative(
        case_id: str,
        record_key: str,
        base_path: str,
        value: Any,
        fault_path: str,
        expected_reason_codes: Sequence[str],
    ) -> None:
        path = f"records/negative/semantic-profile/{case_id}.json"
        add_json(path, value)
        profile_semantic_negative_cases.append(
            {
                "case_id": case_id,
                "record_key": record_key,
                "path": path,
                "base_path": base_path,
                "fault_path": fault_path,
                "expected_reason_codes": list(expected_reason_codes),
            }
        )

    base = _clone(values[profile_path])
    base["accepted_plan_sha256"] = "b" * 64
    profile_semantic_negative(
        "profile-plan-hash-mismatch",
        "execution_profile",
        profile_path,
        base,
        "$.accepted_plan_sha256",
        ["profile.plan_hash_mismatch"],
    )

    base = _clone(values[profile_path])
    base["accepted_goal_sha256"] = "b" * 64
    profile_semantic_negative(
        "profile-goal-hash-mismatch",
        "execution_profile",
        profile_path,
        base,
        "$.accepted_goal_sha256",
        ["profile.goal_hash_mismatch"],
    )

    base = _clone(values[envelope_v2_path])
    base["activation_receipt_sha256"] = "f" * 64
    profile_semantic_negative(
        "envelope-stale-activation-receipt",
        "task_envelope",
        envelope_v2_path,
        base,
        "$.activation_receipt_sha256",
        ["envelope.activation_receipt_stale"],
    )

    base = _clone(values[provider_v2_path])
    base["effective_reasoning_effort"] = "high"
    profile_semantic_negative(
        "provider-requested-effective-mismatch",
        "provider_intent",
        provider_v2_path,
        base,
        "$.effective_reasoning_effort",
        ["provider.effective_effort_mismatch"],
    )

    base = _clone(values[envelope_v2_path])
    base["execution_profile"]["reasoning_effort"] = "high"
    profile_semantic_negative(
        "envelope-profile-mismatch",
        "task_envelope",
        envelope_v2_path,
        base,
        "$.execution_profile.reasoning_effort",
        ["envelope.profile_mismatch"],
    )

    base = _clone(values[receipt_v2_path])
    base["activation_profile_evidence"]["execution_profile_sha256"] = "f" * 64
    profile_semantic_negative(
        "receipt-profile-mismatch",
        "task_receipt",
        receipt_v2_path,
        base,
        "$.activation_profile_evidence.execution_profile_sha256",
        ["receipt.execution_profile_mismatch"],
    )

    base = _clone(values[transition_path])
    base["next_reasoning_effort"] = "max"
    profile_semantic_negative(
        "activation-user-override-reset",
        "activation_transition",
        transition_path,
        base,
        "$.next_reasoning_effort",
        ["activation.user_override_not_sticky"],
    )

    base = _clone(values[transition_path])
    base["accepted_presentation_sequence"] = 1
    profile_semantic_negative(
        "activation-stale-combined-acceptance",
        "activation_transition",
        transition_path,
        base,
        "$.accepted_presentation_sequence",
        ["activation.stale_combined_acceptance"],
    )

    file_entries = [
        {"path": path, "sha256": _sha256_bytes(value)}
        for path, value in sorted(files.items())
    ]
    matrix = {
        "schema_version": "sys4ai.phase02-fixture-coverage.v1",
        "corpus_root": "tests/fixtures/phase-02",
        "generated_by": "scripts/build_phase02_fixture_corpus.py",
        "coverage": {
            "schema_versions": list(SCHEMA_VERSIONS),
            "source_classes": list(SOURCE_CLASSES),
            "plan_phases": list(PLAN_PHASES),
            "task_statuses": list(TASK_STATUSES),
            "receipt_dispositions": list(RECEIPT_DISPOSITIONS),
            "receipt_execution_outcomes": list(RECEIPT_EXECUTION_OUTCOMES),
            "provider_outcomes": list(PROVIDER_OUTCOMES),
            "supersession_terminal_statuses": list(
                SUPERSESSION_TERMINAL_STATUSES
            ),
            "supersession_reason_codes": list(SUPERSESSION_REASON_CODES),
            "amendment_effects": list(AMENDMENT_EFFECTS),
            "normalization_statuses": list(NORMALIZATION_STATUSES),
            "selection_outcomes": list(SELECTION_OUTCOMES),
        },
        "source_cases": source_cases,
        "positive_record_cases": positive_cases,
        "schema_negative_cases": schema_negative_cases,
        "semantic_contract_set": contract_set,
        "semantic_negative_cases": semantic_negative_cases,
        "profile_semantic_contract_set": profile_contract_set,
        "profile_semantic_negative_cases": profile_semantic_negative_cases,
        "files": file_entries,
        "corpus_sha256": content_sha256(file_entries),
        "summary": {
            "generated_files": len(file_entries),
            "source_cases": len(source_cases),
            "positive_record_cases": len(positive_cases),
            "schema_negative_cases": len(schema_negative_cases),
            "semantic_negative_cases": len(semantic_negative_cases),
            "profile_semantic_negative_cases": len(
                profile_semantic_negative_cases
            ),
        },
    }
    return files, matrix


def _expected_outputs() -> dict[str, bytes]:
    files, matrix = build_corpus()
    return {**files, MATRIX_NAME: _json_bytes(matrix)}


def _safe_output_path(relative: str) -> Path:
    target = (CORPUS_ROOT / relative).resolve()
    if not target.is_relative_to(CORPUS_ROOT.resolve()):
        raise ValueError(f"generated fixture path escapes corpus root: {relative}")
    return target


def write_corpus() -> dict[str, Any]:
    outputs = _expected_outputs()
    for relative, value in outputs.items():
        target = _safe_output_path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value)
    return {
        "status": "written",
        "corpus_root": str(CORPUS_ROOT),
        "file_count": len(outputs),
        "write_performed": True,
    }


def check_corpus() -> tuple[int, dict[str, Any]]:
    outputs = _expected_outputs()
    missing: list[str] = []
    drifted: list[str] = []
    for relative, expected in outputs.items():
        target = _safe_output_path(relative)
        if not target.is_file():
            missing.append(relative)
        elif target.read_bytes() != expected:
            drifted.append(relative)
    expected_paths = set(outputs)
    actual_paths = {
        path.relative_to(CORPUS_ROOT).as_posix()
        for path in CORPUS_ROOT.rglob("*")
        if path.is_file()
        and path.name not in {"README.md", ".DS_Store"}
        and "__pycache__" not in path.parts
    } if CORPUS_ROOT.is_dir() else set()
    extra = sorted(actual_paths - expected_paths)
    result = {
        "status": "valid" if not (missing or drifted or extra) else "invalid",
        "corpus_root": str(CORPUS_ROOT),
        "expected_file_count": len(outputs),
        "missing": sorted(missing),
        "drifted": sorted(drifted),
        "extra": extra,
        "write_performed": False,
    }
    return (0 if result["status"] == "valid" else 1), result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build or verify deterministic PHASE-02 plan fixtures."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--check",
        action="store_true",
        help="Verify tracked corpus bytes without writing.",
    )
    mode.add_argument(
        "--write",
        action="store_true",
        help="Write only the tracked test-fixture corpus.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.write:
        result = write_corpus()
        code = 0
    else:
        code, result = check_corpus()
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(
            f"{result['status']}: {result.get('file_count', result.get('expected_file_count'))} files"
        )
        for key in ("missing", "drifted", "extra"):
            for item in result.get(key, []):
                print(f"{key}: {item}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
