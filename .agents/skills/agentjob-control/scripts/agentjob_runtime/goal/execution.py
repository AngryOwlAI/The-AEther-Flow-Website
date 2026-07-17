"""Atomic generation claim, guard precheck, and irreversible consumption."""

from __future__ import annotations

import copy
import secrets
from typing import Any, Mapping

from agentjob_runtime.errors import GuardStop, RecordValidationError, StateConflict
from agentjob_runtime.goal.leases import DEFAULT_LEASE_SECONDS, require_active_lease
from agentjob_runtime.goal.model import add_seconds, effective_guards, map_stop, parse_utc, utc_now
from agentjob_runtime.goal.receipts import finalize_receipt
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
    if record["state"]["passes_consumed"] >= guards["max_continue_passes"]:
        stops.append("pass_limit")
    if now >= parse_utc(guards.get("deadline_at", record["deadline_at"])):
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
    terminal = map_stop(stop_reason)
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
        entry["phase"] = terminal
        record["state"]["phase"] = terminal
        record["state"]["terminal_reason"] = stop_reason
        supplied = {
            "zero_job_reason": f"pre-execution stop: {stop_reason}",
            "goal_evaluation": "indeterminate" if stop_reason in {"human_gate", "indeterminate"} else "unmet",
            "progress_summary": "No AgentJob executed because a protected pre-execution stop applied.",
            "remaining_work": "Resolve the protected stop through canonical authority or recovery.",
            **copy.deepcopy(dict(evidence or {})),
        }
        finalize_receipt(
            mutation,
            generation=generation,
            invocation_count=0,
            decision="guard_stop" if terminal == "terminal_guard_exhausted" else "protected_stop",
            evidence=supplied,
        )
        mutation.release_lease()
    return store.load_goal(goal_id)
