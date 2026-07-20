"""Legal implementation-plan lifecycle transitions and guard outcomes."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.model import parse_utc
from agentjob_runtime.plan.model import (
    ACTIVE_TASK_STATUSES,
    PROTECTED_STOP_TASK_STATUSES,
)


PLAN_PHASE_TRANSITIONS = frozenset(
    {
        ("initialized", "task_reserved"),
        ("initialized", "continuation_required"),
        ("continuation_required", "task_reserved"),
        ("continuation_required", "completion_candidate"),
        ("task_reserved", "task_active"),
        ("task_active", "task_verifying"),
        ("task_verifying", "continuation_required"),
        ("task_verifying", "completion_candidate"),
        ("completion_candidate", "terminal_complete"),
        ("recovery_pending", "continuation_required"),
        ("recovery_pending", "task_reserved"),
    }
)
TERMINAL_PLAN_PHASES = frozenset(
    {
        "terminal_complete",
        "terminal_blocked_no_runnable",
        "terminal_awaiting_human",
        "terminal_validation_failed",
        "terminal_capability_blocked",
        "terminal_corrupt_state",
        "terminal_cancelled",
    }
)
ACTIVE_PLAN_PHASES = frozenset(
    {"task_reserved", "task_active", "task_verifying"}
)
TASK_TRANSITIONS = frozenset(
    {
        ("pending", "reserved"),
        ("reserved", "active"),
        ("active", "verifying"),
        ("replan_required", "superseded"),
    }
)
RECEIPT_TASK_STATUSES = {
    "task_complete": "completed",
    "blocked": "blocked",
    "replan_required": "replan_required",
    "human_gate_required": "human_gate_required",
    "validation_failed": "validation_failed",
    "invocation_unknown": "invocation_unknown",
    "cancelled": "cancelled",
}


@dataclass(frozen=True)
class GuardOutcome:
    disposition: str
    plan_phase: str
    quarantine_lease: bool = False


GUARD_OUTCOMES = {
    "human_gate": GuardOutcome(
        "human_gate_required",
        "terminal_awaiting_human",
    ),
    "validation": GuardOutcome(
        "validation_failed",
        "terminal_validation_failed",
    ),
    "checkpoint": GuardOutcome(
        "validation_failed",
        "terminal_validation_failed",
    ),
    "capability": GuardOutcome(
        "blocked",
        "terminal_capability_blocked",
    ),
    "no_ready_task": GuardOutcome(
        "blocked",
        "terminal_blocked_no_runnable",
    ),
    "task_requires_replan": GuardOutcome(
        "replan_required",
        "continuation_required",
    ),
    "invocation_unknown": GuardOutcome(
        "invocation_unknown",
        "recovery_pending",
        True,
    ),
    "provider_ambiguous": GuardOutcome(
        "invocation_unknown",
        "recovery_pending",
        True,
    ),
    "provider_timeout": GuardOutcome(
        "invocation_unknown",
        "recovery_pending",
        True,
    ),
    "schema": GuardOutcome(
        "blocked",
        "terminal_corrupt_state",
    ),
    "hash": GuardOutcome(
        "blocked",
        "terminal_corrupt_state",
    ),
    "journal": GuardOutcome(
        "blocked",
        "terminal_corrupt_state",
    ),
    "repository": GuardOutcome(
        "blocked",
        "terminal_corrupt_state",
    ),
    "cancelled": GuardOutcome(
        "cancelled",
        "terminal_cancelled",
    ),
}


def holder_token_sha256(holder_token: str) -> str:
    if not isinstance(holder_token, str) or not holder_token:
        raise RecordValidationError("plan lease holder token must be nonblank")
    return hashlib.sha256(holder_token.encode("utf-8")).hexdigest()


def guard_outcome(reason: str) -> GuardOutcome:
    try:
        return GUARD_OUTCOMES[reason]
    except KeyError as error:
        raise RecordValidationError(
            f"unregistered plan guard reason: {reason!r}"
        ) from error


def _task(state: Mapping[str, Any], task_id: str) -> dict[str, Any]:
    try:
        return next(
            task
            for task in state["tasks"]
            if task["task_id"] == task_id
        )
    except StopIteration as error:
        raise RecordValidationError(
            f"plan task does not exist: {task_id}"
        ) from error


def _refresh_aggregates(state: dict[str, Any]) -> None:
    tasks = state["tasks"]
    state["current_generation"] = max(
        (task["generation"] or 0 for task in tasks),
        default=0,
    )
    state["counters"] = {
        "worker_discussions": sum(
            task["counters"]["worker_discussions"] for task in tasks
        ),
        "continue_invocations": sum(
            task["counters"]["continue_invocations"] for task in tasks
        ),
        "agentjobs": sum(task["counters"]["agentjobs"] for task in tasks),
        "provider_creates": sum(
            task["counters"]["provider_creates"] for task in tasks
        ),
        "successor_creates": sum(
            task["counters"]["successor_creates"] for task in tasks
        ),
        "tasks_completed": sum(
            task["status"] == "completed" for task in tasks
        ),
        "tasks_superseded": sum(
            task["status"] == "superseded" for task in tasks
        ),
        "protected_stops": sum(
            task["status"] in PROTECTED_STOP_TASK_STATUSES for task in tasks
        ),
    }


def reserve_task(
    record: dict[str, Any],
    *,
    task_id: str,
    generation: int,
    timestamp: str,
    successor_created: bool,
) -> None:
    parse_utc(timestamp)
    if type(generation) is not int or generation <= 0:
        raise RecordValidationError("plan task generation must be positive")
    if not isinstance(successor_created, bool):
        raise RecordValidationError(
            "successor_created must be an explicit boolean"
        )
    state = record["state"]
    if state["phase"] not in {
        "initialized",
        "continuation_required",
        "recovery_pending",
    }:
        raise StateConflict("plan is not ready to reserve a task")
    if state["active_task_id"] is not None or state["lease"] is not None:
        raise StateConflict("plan already has an active task or lease")
    if generation <= state["current_generation"]:
        raise StateConflict("plan task generation must advance monotonically")
    task = _task(state, task_id)
    if task["status"] != "pending":
        raise StateConflict("only a pending plan task can be reserved")
    task["status"] = "reserved"
    task["generation"] = generation
    task["counters"]["worker_discussions"] = 1
    task["counters"]["successor_creates"] = int(successor_created)
    task["updated_at"] = timestamp
    state["phase"] = "task_reserved"
    state["active_task_id"] = task_id
    state["terminal_reason"] = None
    state["evaluation"] = "unmet"
    _refresh_aggregates(state)


def activate_task(
    record: dict[str, Any],
    *,
    task_id: str,
    generation: int,
    fingerprint_before: str,
    timestamp: str,
) -> None:
    parse_utc(timestamp)
    state = record["state"]
    task = _task(state, task_id)
    if (
        state["phase"] != "task_reserved"
        or state["active_task_id"] != task_id
        or task["status"] != "reserved"
        or task["generation"] != generation
    ):
        raise StateConflict("plan task reservation identity does not match")
    if fingerprint_before != state["fingerprints"]["current"]:
        raise StateConflict(
            "plan task starting fingerprint differs from canonical state"
        )
    task["status"] = "active"
    task["fingerprint_before"] = fingerprint_before
    task["updated_at"] = timestamp
    state["phase"] = "task_active"


def consume_task_invocation(
    record: dict[str, Any],
    *,
    task_id: str,
    generation: int,
    timestamp: str,
) -> None:
    """Durably consume the one continue budget before the external call."""

    parse_utc(timestamp)
    state = record["state"]
    task = _task(state, task_id)
    if (
        state["phase"] != "task_active"
        or state["active_task_id"] != task_id
        or task["status"] != "active"
        or task["generation"] != generation
    ):
        raise StateConflict("active plan task identity does not match")
    if task["counters"]["continue_invocations"] != 0:
        raise StateConflict(
            "plan task continue invocation was already consumed"
        )
    task["counters"]["continue_invocations"] = 1
    task["updated_at"] = timestamp
    _refresh_aggregates(state)


def begin_task_verification(
    record: dict[str, Any],
    *,
    task_id: str,
    generation: int,
    fingerprint_after: str,
    continue_invocations: int,
    agentjobs: int,
    provider_creates: int,
    timestamp: str,
) -> None:
    parse_utc(timestamp)
    counts = {
        "continue_invocations": continue_invocations,
        "agentjobs": agentjobs,
        "provider_creates": provider_creates,
    }
    if any(type(value) is not int or value not in {0, 1} for value in counts.values()):
        raise RecordValidationError(
            "plan task execution cardinalities must be zero or one"
        )
    state = record["state"]
    task = _task(state, task_id)
    if (
        state["phase"] != "task_active"
        or state["active_task_id"] != task_id
        or task["status"] != "active"
        or task["generation"] != generation
    ):
        raise StateConflict("active plan task identity does not match")
    task["status"] = "verifying"
    task["fingerprint_after"] = fingerprint_after
    task["counters"].update(counts)
    task["updated_at"] = timestamp
    state["phase"] = "task_verifying"
    _refresh_aggregates(state)


def receipt_outcome(
    receipt: Mapping[str, Any],
    *,
    guard_reason: str | None,
) -> tuple[str, str, bool]:
    disposition = receipt.get("disposition")
    if disposition == "plan_complete":
        raise RecordValidationError(
            "plan completion is outside the task-lifecycle transition boundary"
        )
    try:
        task_status = RECEIPT_TASK_STATUSES[str(disposition)]
    except KeyError as error:
        raise RecordValidationError(
            f"unsupported plan task receipt disposition: {disposition!r}"
        ) from error
    if disposition == "task_complete":
        if guard_reason is not None:
            raise RecordValidationError(
                "completed task receipt cannot name a guard reason"
            )
        return task_status, "continuation_required", False
    if guard_reason is None:
        raise RecordValidationError(
            "protected task receipt requires a mapped guard reason"
        )
    outcome = guard_outcome(guard_reason)
    if outcome.disposition != disposition:
        raise RecordValidationError(
            "plan guard reason does not match receipt disposition"
        )
    return task_status, outcome.plan_phase, outcome.quarantine_lease


def apply_task_receipt(
    record: dict[str, Any],
    receipt: Mapping[str, Any],
    *,
    receipt_sha256: str,
    guard_reason: str | None,
    timestamp: str,
) -> bool:
    parse_utc(timestamp)
    state = record["state"]
    task_id = str(receipt["task_identity"]["task_id"])
    task = _task(state, task_id)
    generation = receipt["relay_identity"]["generation"]
    if (
        task["task_sha256"] != receipt["task_identity"]["task_sha256"]
        or record["plan_id"] != receipt["plan_identity"]["plan_id"]
        or receipt["plan_identity"]["plan_sha256"]
        not in {
            record["plan_sha256"],
            record["effective_plan_sha256"],
        }
        or task["generation"] != generation
    ):
        raise StateConflict("plan task receipt identity does not match active state")
    execution = receipt["execution"]
    if task["status"] not in ACTIVE_TASK_STATUSES:
        raise StateConflict("plan task is not eligible for finalization")
    repository = receipt["repository_evidence"]
    if (
        task["fingerprint_before"] is not None
        and task["fingerprint_before"] != repository["fingerprint_before"]
    ) or (
        task["fingerprint_after"] is not None
        and task["fingerprint_after"] != repository["fingerprint_after"]
    ):
        raise StateConflict(
            "plan task receipt fingerprints do not match active state"
        )
    task_status, plan_phase, quarantine = receipt_outcome(
        receipt,
        guard_reason=guard_reason,
    )
    counters = {
        "worker_discussions": execution["worker_discussions"],
        "provider_creates": execution["provider_create_calls"],
        "successor_creates": execution["successor_creates"],
        "same_task_successors": execution["same_task_successors"],
    }
    for name in ("continue_invocations", "agentjobs"):
        value = execution[name]
        if value != "unknown":
            counters[name] = value
    task.update(
        {
            "status": task_status,
            "counters": {**task["counters"], **counters},
            "receipt_link": {
                "receipt_id": receipt["receipt_id"],
                "receipt_sha256": receipt_sha256,
            },
            "fingerprint_before": repository["fingerprint_before"],
            "fingerprint_after": repository["fingerprint_after"],
            "terminal_reason": receipt["terminal_reason"],
            "updated_at": timestamp,
        }
    )
    state["phase"] = plan_phase
    state["active_task_id"] = task_id if quarantine else None
    state["evaluation"] = "indeterminate" if quarantine else "unmet"
    state["terminal_reason"] = receipt["terminal_reason"] if plan_phase in {
        "recovery_pending",
        *TERMINAL_PLAN_PHASES,
    } else None
    fingerprint_after = repository["fingerprint_after"]
    state["fingerprints"]["current"] = fingerprint_after
    if state["fingerprints"]["history"][-1] != fingerprint_after:
        state["fingerprints"]["history"].append(fingerprint_after)
    _refresh_aggregates(state)
    return quarantine


def validate_plan_transition(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> None:
    """Reject illegal lifecycle edges before a plan revision is persisted."""

    old_phase = str(before["phase"])
    new_phase = str(after["phase"])
    phase_edge = (old_phase, new_phase)
    allowed_phase_edge = (
        old_phase == new_phase
        or phase_edge in PLAN_PHASE_TRANSITIONS
        or (
            old_phase in {
                "initialized",
                "task_reserved",
                "task_active",
                "task_verifying",
                "continuation_required",
                "completion_candidate",
            }
            and new_phase in TERMINAL_PLAN_PHASES | {"recovery_pending"}
        )
    )
    if not allowed_phase_edge:
        raise StateConflict(
            f"illegal plan phase transition: {old_phase} -> {new_phase}"
        )

    before_tasks = {task["task_id"]: task for task in before["tasks"]}
    after_tasks = {task["task_id"]: task for task in after["tasks"]}
    if not set(before_tasks) <= set(after_tasks):
        raise StateConflict("plan transition cannot remove task identities")
    for task_id, prior in before_tasks.items():
        current = after_tasks[task_id]
        if current["task_sha256"] != prior["task_sha256"]:
            raise StateConflict("plan transition cannot change a task hash")
        edge = (prior["status"], current["status"])
        receipt_terminal = (
            prior["status"] in {"pending", "reserved", "active", "verifying"}
            and current["status"] in RECEIPT_TASK_STATUSES.values()
        )
        if not (
            prior["status"] == current["status"]
            or edge in TASK_TRANSITIONS
            or receipt_terminal
        ):
            raise StateConflict(
                f"illegal plan task transition for {task_id}: "
                f"{prior['status']} -> {current['status']}"
            )
        for name, old_value in prior["counters"].items():
            if current["counters"][name] < old_value:
                raise StateConflict("plan task counters cannot decrease")
    for task_id in set(after_tasks) - set(before_tasks):
        task = after_tasks[task_id]
        if (
            task["status"] != "pending"
            or task["generation"] is not None
            or task["receipt_link"] is not None
        ):
            raise StateConflict(
                "append-only replacement tasks must begin pending"
            )

    if after["current_generation"] < before["current_generation"]:
        raise StateConflict("plan generation cannot decrease")
    prior_history = list(before["fingerprints"]["history"])
    current_history = list(after["fingerprints"]["history"])
    if current_history[: len(prior_history)] != prior_history:
        raise StateConflict("plan fingerprint history is append-only")
    if old_phase in TERMINAL_PLAN_PHASES:
        raise StateConflict("terminal plan state is absorbing")

    active = [
        task
        for task in after["tasks"]
        if task["status"] in ACTIVE_TASK_STATUSES
    ]
    if new_phase in ACTIVE_PLAN_PHASES and len(active) != 1:
        raise StateConflict("active plan phase requires exactly one active task")
