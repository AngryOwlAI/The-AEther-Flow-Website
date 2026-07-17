"""Deterministic recursive and terminal decisions for verified generations."""

from __future__ import annotations

from typing import Any

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.execution import guard_precheck
from agentjob_runtime.goal.leases import require_active_lease
from agentjob_runtime.goal.model import (
    ABSORBING_TERMINALS,
    RECOVERABLE_TERMINALS,
    TERMINAL_PHASES,
    map_stop,
    transition_allowed,
    utc_now,
)
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import reserve_successor
from agentjob_runtime.goal.verify import finalize_verified_receipt


def select_decision(
    record: dict[str, Any],
    *,
    generation: int,
    legal_route_available: bool,
    timestamp: str | None = None,
    explicit_stop_reason: str | None = None,
) -> tuple[str, str | None]:
    entry = record["generations"].get(str(generation))
    if entry is None or record["state"]["phase"] != "step_verified":
        raise StateConflict("decision selection requires a verified generation")
    evaluation = record["state"]["goal_evaluation"]
    if explicit_stop_reason is not None:
        terminal = map_stop(explicit_stop_reason)
        if terminal == "terminal_complete" and evaluation != "met":
            raise StateConflict("goal completion requires canonical met evidence")
        if terminal != "terminal_complete" and evaluation == "met":
            raise StateConflict("a canonically met goal must use terminal_complete")
        return terminal, explicit_stop_reason
    if evaluation == "met":
        return "terminal_complete", "goal_met"
    if evaluation == "indeterminate":
        return "terminal_awaiting_human", "indeterminate"
    if entry.get("fingerprint_status") in {"unchanged", "repeated"}:
        return "terminal_no_progress", "repeated_state"
    stops = guard_precheck(record, timestamp=timestamp)
    if stops:
        return map_stop(stops[0]), stops[0]
    if legal_route_available:
        return "continuation_required", None
    return "terminal_no_progress", "no_action"


def decide_generation(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    claim_token: str,
    legal_route_available: bool,
    explicit_stop_reason: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        entry = record["generations"].get(str(generation))
        if entry is None or record["state"]["phase"] != "step_verified":
            raise StateConflict("generation decision requires step_verified")
        require_active_lease(record, generation=generation, holder_token=claim_token)
        if entry["lease_token"] != claim_token:
            raise StateConflict("decision claim token mismatch")
        decision, reason = select_decision(
            record,
            generation=generation,
            legal_route_available=legal_route_available,
            timestamp=now,
            explicit_stop_reason=explicit_stop_reason,
        )
        if not transition_allowed("step_verified", decision):
            raise StateConflict(f"unlisted normal transition: step_verified -> {decision}")
        entry["phase"] = decision
        record["state"]["phase"] = decision
        if decision == "continuation_required":
            pending = entry.get("pending_step_result")
            if not isinstance(pending, dict):
                raise StateConflict("recursive decision requires pending verified evidence")
            pending["decision"] = decision
            mutation.event("continuation_required", {"generation": generation})
        else:
            record["state"]["terminal_reason"] = reason or decision
            receipt_decision = (
                "terminal_complete"
                if decision == "terminal_complete"
                else "cancelled"
                if decision == "terminal_cancelled"
                else "guard_stop"
                if decision == "terminal_guard_exhausted"
                else "protected_stop"
                if decision in {"terminal_awaiting_human", "terminal_capability_blocked"}
                else "failed"
            )
            finalize_verified_receipt(
                mutation,
                generation=generation,
                decision=receipt_decision,
            )
            mutation.event(
                "generation_terminal",
                {"generation": generation, "terminal_phase": decision, "reason": reason},
            )
            mutation.release_lease()
    return store.load_goal(goal_id)


def decide_and_reserve_successor(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    claim_token: str,
    predecessor_thread_id: str | None,
    handoff_token: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    decided = decide_generation(
        store,
        goal_id=goal_id,
        expected_revision=expected_revision,
        generation=generation,
        claim_token=claim_token,
        legal_route_available=True,
        timestamp=timestamp,
    )
    if decided["state"]["phase"] != "continuation_required":
        return decided
    return reserve_successor(
        store,
        goal_id=goal_id,
        expected_revision=decided["state"]["revision"],
        current_holder_token=claim_token,
        predecessor_thread_id=predecessor_thread_id,
        handoff_token=handoff_token,
        timestamp=timestamp,
    )


def terminal_classification(phase: str) -> str:
    if phase in ABSORBING_TERMINALS:
        return "absorbing"
    if phase in RECOVERABLE_TERMINALS:
        return "recoverable"
    if phase in TERMINAL_PHASES:
        raise AssertionError("terminal phase classification is incomplete")
    raise RecordValidationError(f"not a terminal phase: {phase}")
