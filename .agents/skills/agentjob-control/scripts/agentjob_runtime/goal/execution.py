"""Atomic generation claim, guard precheck, and irreversible consumption."""

from __future__ import annotations

import copy
import secrets
from typing import Any, Mapping

from agentjob_runtime.errors import GuardStop, RecordValidationError, StateConflict
from agentjob_runtime.goal.leases import DEFAULT_LEASE_SECONDS, require_active_lease
from agentjob_runtime.goal.model import (
    GOAL_SCHEMA_VERSION,
    add_seconds,
    effective_guards,
    map_stop,
    parse_utc,
    utc_now,
)
from agentjob_runtime.goal.receipts import finalize_receipt
from agentjob_runtime.goal.resolution import (
    append_resolution,
    build_human_necessity_report,
    classify_resolution,
)
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


def claim_generation(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    handoff_token: str,
    idempotency_key: str,
    successor_thread_id: str,
    claim_token: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    now = timestamp or utc_now()
    token = claim_token or secrets.token_hex(24)
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        handoff = record["handoff"]
        if record["state"]["phase"] != "successor_created":
            raise StateConflict("generation is not claimable")
        if (
            generation != record["state"]["current_generation"]
            or handoff.get("generation") != generation
            or handoff.get("token") != handoff_token
            or handoff.get("idempotency_key") != idempotency_key
            or handoff.get("successor_thread_id") != successor_thread_id
        ):
            raise StateConflict("generation claim identity is stale or mismatched")
        entry = record["generations"].get(str(generation))
        if entry is None or entry["phase"] != "successor_created":
            raise StateConflict("generation is already claimed")
        if entry["invocation_consumed"] or entry["claimed_at"] is not None:
            raise StateConflict("generation is already claimed or consumed")
        require_active_lease(
            record,
            generation=generation,
            holder_token=handoff_token,
            holder_kinds={"successor_reserved"},
        )
        entry["phase"] = "step_active"
        entry["lease_token"] = token
        entry["claimed_at"] = now
        record["state"]["phase"] = "step_active"
        mutation.replace_lease(
            generation=generation,
            holder_kind="continuation",
            holder_token=token,
            expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
        )
        mutation.event(
            "generation_claimed",
            {
                "generation": generation,
                "idempotency_key": idempotency_key,
                "successor_thread_id": successor_thread_id,
            },
        )
    return store.load_goal(goal_id)


def guard_precheck(
    record: Mapping[str, Any],
    *,
    timestamp: str | None = None,
    observations: Mapping[str, bool] | None = None,
) -> list[str]:
    now = parse_utc(timestamp or utc_now())
    guards = effective_guards(record)
    stops: list[str] = []
    max_continue_passes = guards["max_continue_passes"]
    if (
        max_continue_passes is not None
        and record["state"]["passes_consumed"] >= max_continue_passes
    ):
        stops.append("pass_limit")
    deadline = guards.get("deadline_at", record["deadline_at"])
    if deadline is not None and now >= parse_utc(deadline):
        stops.append("deadline_limit")
    observations = dict(observations or {})
    mapped = {
        "human_gate_clear": "human_gate",
        "validation_clear": "validation",
        "checkpoint_clear": "checkpoint",
        "dirty_state_expected": "dirty_state",
        "capabilities_available": "capability",
        "repository_matches": "repository",
    }
    for key, reason in mapped.items():
        if key in observations and observations[key] is False:
            stops.append(reason)
    return stops


def consume_invocation(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    claim_token: str,
    observations: Mapping[str, bool] | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        entry = record["generations"].get(str(generation))
        if record["state"]["phase"] != "step_active" or entry is None:
            raise StateConflict("invocation consumption requires an active generation")
        require_active_lease(
            record,
            generation=generation,
            holder_token=claim_token,
            holder_kinds={"continuation"},
        )
        if entry["lease_token"] != claim_token:
            raise StateConflict("generation claim token mismatch")
        if entry["invocation_consumed"]:
            raise StateConflict("generation invocation was already consumed")
        stops = guard_precheck(record, timestamp=now, observations=observations)
        if stops:
            raise GuardStop(
                "goal guards prevent invocation consumption",
                details={"stop_reasons": stops},
            )
        entry["invocation_consumed"] = True
        entry["invocation_state"] = "authorized"
        entry["consumed_at"] = now
        record["state"]["passes_consumed"] += 1
        mutation.event("invocation_consumed", {"generation": generation})
    return store.load_goal(goal_id)


def record_invocation_returned(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    claim_token: str,
    continue_result: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    if not continue_result:
        raise RecordValidationError("direct structured continue result is required")
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        entry = record["generations"].get(str(generation))
        if record["state"]["phase"] != "step_active" or entry is None:
            raise StateConflict("returned invocation requires step_active")
        require_active_lease(record, generation=generation, holder_token=claim_token)
        if (
            not entry["invocation_consumed"]
            or entry["invocation_state"] != "authorized"
            or entry["lease_token"] != claim_token
        ):
            raise StateConflict("invocation was not consumed by this claim")
        entry["invocation_state"] = "returned"
        entry["returned_at"] = now
        entry["pending_step_result"] = {"continue_result": copy.deepcopy(dict(continue_result))}
        entry["phase"] = "step_verifying"
        record["state"]["phase"] = "step_verifying"
        mutation.event(
            "invocation_returned",
            {"generation": generation, "continue_result": copy.deepcopy(dict(continue_result))},
        )
    return store.load_goal(goal_id)


def record_invocation_unknown(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    claim_token: str,
    diagnostic: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    if not diagnostic:
        raise RecordValidationError("unknown invocation requires diagnostic evidence")
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        entry = record["generations"].get(str(generation))
        if record["state"]["phase"] != "step_active" or entry is None:
            raise StateConflict("unknown invocation requires step_active")
        require_active_lease(record, generation=generation, holder_token=claim_token)
        if not entry["invocation_consumed"] or entry["lease_token"] != claim_token:
            raise StateConflict("unknown invocation lacks a consumed matching claim")
        entry["invocation_state"] = "unknown"
        entry["pending_step_result"] = {"diagnostic": copy.deepcopy(dict(diagnostic))}
        if record.get("schema_version") == GOAL_SCHEMA_VERSION:
            disposition = classify_resolution(
                reason_code="worker.continue_outcome_unknown",
                status="unknown",
                evidence=diagnostic,
                history=record["resolution_history"],
                authority_refs=["goal-relay:at-most-once"],
                evidence_refs=[f"generation:{generation}:invocation"],
            )
            append_resolution(
                record,
                generation=generation,
                disposition=disposition,
                progress_dimensions=["canonical_evidence"],
            )
            entry["phase"] = "recovery_pending"
            record["state"]["phase"] = "recovery_pending"
            record["state"]["terminal_reason"] = None
        else:
            entry["phase"] = "terminal_awaiting_human"
            record["state"]["phase"] = "terminal_awaiting_human"
            record["state"]["terminal_reason"] = "invocation_outcome_uncertain"
        mutation.replace_lease(
            generation=generation,
            holder_kind="quarantined",
            holder_token=secrets.token_hex(24),
            expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
        )
        mutation.event(
            "invocation_unknown",
            {"generation": generation, "diagnostic": copy.deepcopy(dict(diagnostic))},
        )
    return store.load_goal(goal_id)


def pre_execution_stop(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    claim_token: str,
    stop_reason: str,
    evidence: Mapping[str, Any] | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    current = store.load_goal(goal_id)
    v3 = current.get("schema_version") == GOAL_SCHEMA_VERSION
    terminal = map_stop(
        stop_reason,
        schema_version=current.get("schema_version"),
    )
    if terminal == "terminal_complete":
        raise RecordValidationError("goal completion cannot be a pre-execution stop")
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        entry = record["generations"].get(str(generation))
        if record["state"]["phase"] != "step_active" or entry is None:
            raise StateConflict("pre-execution stop requires an active generation")
        require_active_lease(record, generation=generation, holder_token=claim_token)
        if entry["invocation_consumed"] or entry["lease_token"] != claim_token:
            raise StateConflict("pre-execution stop cannot follow consumption")
        disposition = None
        if v3:
            disposition = classify_resolution(
                reason_code=f"precheck.{stop_reason}",
                status=stop_reason,
                evidence=copy.deepcopy(dict(evidence or {})),
                history=record["resolution_history"],
                authority_refs=["goal-guards", "accepted-goal-authority"],
                evidence_refs=[f"generation:{generation}:precheck"],
                explicit_human_gate=stop_reason == "human_gate",
                policy_limit=stop_reason in {"pass_limit", "deadline_limit", "budget_limit"},
                integrity_incident=stop_reason in {"schema", "hash", "journal", "path"},
            )
            append_resolution(
                record,
                generation=generation,
                disposition=disposition,
                progress_dimensions=["blocker_resolution", "strategy"],
            )
        entry["phase"] = terminal
        record["state"]["phase"] = terminal
        record["state"]["terminal_reason"] = (
            stop_reason if terminal.startswith("terminal_") else None
        )
        supplied = {
            "zero_job_reason": f"pre-execution stop: {stop_reason}",
            "goal_evaluation": "indeterminate" if stop_reason in {"human_gate", "indeterminate"} else "unmet",
            "progress_summary": "No AgentJob executed because a protected pre-execution stop applied.",
            "remaining_work": "Resolve the protected stop through canonical authority or recovery.",
            **copy.deepcopy(dict(evidence or {})),
        }
        receipt_decision = (
            "continuation_required"
            if v3 and terminal in {"continuation_required", "recovery_pending"}
            else "policy_limit_reached"
            if v3 and terminal == "terminal_policy_limit"
            else "human_intervention_required"
            if v3 and terminal == "terminal_awaiting_human"
            else "integrity_incident"
            if v3 and terminal == "terminal_integrity_incident"
            else "guard_stop"
            if terminal == "terminal_guard_exhausted"
            else "protected_stop"
        )
        if v3 and terminal.startswith("terminal_"):
            report = build_human_necessity_report(
                goal_id=record["goal_id"],
                generation=generation,
                disposition=disposition,
                history=record["resolution_history"],
                required_human_authority_or_decision=(
                    "Resolve the accepted human gate."
                    if stop_reason == "human_gate"
                    else "Extend or cancel the accepted finite policy limit."
                    if terminal == "terminal_policy_limit"
                    else "Reconcile the canonical integrity incident."
                ),
                smallest_requested_user_action=(
                    "Provide the exact decision or authority identified by the active policy."
                ),
                resume_contract=(
                    "Resume the same goal and generation identity after the recorded gate is satisfied."
                ),
                policy_authority_refs=["goal-guards"]
                if stop_reason != "human_gate"
                else ["active-policy:human-gate"],
                evidence_refs=[f"generation:{generation}:precheck"],
                timestamp=now,
            )
            record["human_intervention"] = report
            entry["human_necessity_report_ref"] = report["report_id"]
        finalize_receipt(
            mutation,
            generation=generation,
            invocation_count=0,
            decision=receipt_decision,
            evidence=supplied,
        )
        if v3 and terminal.startswith("terminal_"):
            mutation.release_lease()
        elif not v3:
            mutation.release_lease()
    return store.load_goal(goal_id)
