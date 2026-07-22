"""Deterministic recursive and terminal decisions for verified generations."""

from __future__ import annotations

from typing import Any

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.execution import guard_precheck
from agentjob_runtime.goal.leases import require_active_lease
from agentjob_runtime.goal.model import (
    ABSORBING_TERMINALS,
    GOAL_SCHEMA_VERSION,
    GOAL_SCHEMA_VERSION_V4,
    PROFILED_GOAL_SCHEMA_VERSIONS,
    RECOVERABLE_TERMINALS,
    TERMINAL_PHASES,
    V3_TERMINAL_PHASES,
    map_stop,
    transition_allowed,
    utc_now,
)
from agentjob_runtime.goal.completion_report import build_completion_report
from agentjob_runtime.goal.resolution import (
    append_resolution,
    build_human_necessity_report,
    classify_resolution,
    normal_continuation_disposition,
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
    profiled = record.get("schema_version") in PROFILED_GOAL_SCHEMA_VERSIONS
    if explicit_stop_reason is not None:
        terminal = map_stop(
            explicit_stop_reason,
            schema_version=record.get("schema_version"),
        )
        if terminal == "terminal_complete" and evaluation != "met":
            raise StateConflict("goal completion requires canonical met evidence")
        if terminal != "terminal_complete" and evaluation == "met":
            raise StateConflict("a canonically met goal must use terminal_complete")
        return terminal, explicit_stop_reason
    if evaluation == "met":
        return "terminal_complete", "goal_met"
    if profiled:
        stops = guard_precheck(record, timestamp=timestamp)
        if stops:
            return (
                map_stop(stops[0], schema_version=record.get("schema_version")),
                stops[0],
            )
        disposition = entry.get("resolution_disposition")
        if isinstance(disposition, dict) and disposition.get("requires_human") is True:
            return (
                "terminal_integrity_incident"
                if disposition.get("classification")
                == "integrity_incident_requires_owner"
                else "terminal_policy_limit"
                if disposition.get("classification") == "policy_limit_requires_user"
                else "terminal_cancelled"
                if disposition.get("classification") == "cancelled"
                else "terminal_awaiting_human",
                str(disposition.get("reason_code") or "human_intervention_required"),
            )
        if legal_route_available:
            return "continuation_required", None
        return "terminal_awaiting_human", "no_distinct_lawful_strategy"
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
        profiled = record.get("schema_version") in PROFILED_GOAL_SCHEMA_VERSIONS
        v4 = record.get("schema_version") == GOAL_SCHEMA_VERSION_V4
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
        if not transition_allowed(
            "step_verified",
            decision,
            schema_version=record.get("schema_version"),
        ):
            raise StateConflict(f"unlisted normal transition: step_verified -> {decision}")
        disposition = entry.get("resolution_disposition") if profiled else None
        if profiled:
            if decision == "terminal_complete":
                disposition = classify_resolution(
                    reason_code="goal.met",
                    status="met",
                    evidence={
                        "generation": generation,
                        "fingerprint": entry.get("after_fingerprint"),
                    },
                    authority_refs=["completion-contract"],
                    evidence_refs=[f"generation:{generation}:verified"],
                    goal_reached=True,
                )
            elif decision == "continuation_required":
                if not isinstance(disposition, dict):
                    disposition = normal_continuation_disposition(
                        reason_code=reason or "goal.unmet",
                        evidence={
                            "generation": generation,
                            "fingerprint_status": entry.get("fingerprint_status"),
                        },
                        authority_refs=["accepted-goal-authority"],
                        evidence_refs=[f"generation:{generation}:verified"],
                    )
            elif not isinstance(disposition, dict) or disposition.get(
                "requires_human"
            ) is not True:
                disposition = classify_resolution(
                    reason_code=reason or "goal.human_intervention_required",
                    status=decision,
                    evidence={
                        "generation": generation,
                        "fingerprint_status": entry.get("fingerprint_status"),
                    },
                    history=record["resolution_history"],
                    authority_refs=["accepted-goal-authority"],
                    evidence_refs=[f"generation:{generation}:verified"],
                    legal_route_available=False,
                    explicit_human_gate=decision == "terminal_awaiting_human"
                    and reason == "human_gate",
                    policy_limit=decision == "terminal_policy_limit",
                    integrity_incident=decision == "terminal_integrity_incident",
                    cancelled=decision == "terminal_cancelled",
                )
            if not any(item == disposition for item in record["resolution_history"]):
                append_resolution(
                    record,
                    generation=generation,
                    disposition=disposition,
                    progress_dimensions=entry.get(
                        "material_progress_dimensions", []
                    ),
                )
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
                else "policy_limit_reached"
                if decision == "terminal_policy_limit"
                else "integrity_incident"
                if decision == "terminal_integrity_incident"
                else "human_intervention_required"
                if profiled
                else "guard_stop"
                if decision == "terminal_guard_exhausted"
                else "protected_stop"
                if decision in {"terminal_awaiting_human", "terminal_capability_blocked"}
                else "failed"
            )
            if profiled and decision != "terminal_complete":
                human = build_human_necessity_report(
                    goal_id=record["goal_id"],
                    generation=generation,
                    disposition=disposition,
                    history=record["resolution_history"],
                    required_human_authority_or_decision=(
                        "Extend or cancel the accepted finite policy limit."
                        if decision == "terminal_policy_limit"
                        else "Resolve the canonical integrity incident."
                        if decision == "terminal_integrity_incident"
                        else "Confirm or supersede the explicit cancellation."
                        if decision == "terminal_cancelled"
                        else "Choose or authorize the smallest remaining lawful route."
                    ),
                    smallest_requested_user_action=(
                        "Provide the exact authority or decision named in this report."
                    ),
                    resume_contract=(
                        "Resume the same immutable goal after satisfying the recorded requirement."
                    ),
                    policy_authority_refs=(
                        ["goal-guards"]
                        if decision == "terminal_policy_limit"
                        else ["canonical-integrity"]
                        if decision == "terminal_integrity_incident"
                        else ["user-cancellation"]
                        if decision == "terminal_cancelled"
                        else ["accepted-goal-policy"]
                    ),
                    evidence_refs=[f"generation:{generation}:verified"],
                    timestamp=now,
                )
                record["human_intervention"] = human
                entry["human_necessity_report_ref"] = human["report_id"]
            finalize_verified_receipt(
                mutation,
                generation=generation,
                decision=receipt_decision,
            )
            if v4:
                record["coordinator"]["status"] = (
                    "goal_reached"
                    if decision == "terminal_complete"
                    else "cancelled"
                    if decision == "terminal_cancelled"
                    else "suspended_safeguard"
                )
                record["coordinator"]["current_worker_thread_id"] = None
                record["coordinator"]["last_worker_receipt_sha256"] = entry[
                    "finalized_receipt_hash"
                ]
                record["coordinator"]["updated_at"] = now
            if profiled and decision == "terminal_complete":
                report = build_completion_report(record, completed_at=now)
                record["completion_report"] = report
                entry["completion_report_ref"] = report["report_id"]
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
    if phase in V3_TERMINAL_PHASES:
        return "absorbing"
    if phase in ABSORBING_TERMINALS:
        return "absorbing"
    if phase in RECOVERABLE_TERMINALS:
        return "recoverable"
    if phase in TERMINAL_PHASES:
        raise AssertionError("terminal phase classification is incomplete")
    raise RecordValidationError(f"not a terminal phase: {phase}")
