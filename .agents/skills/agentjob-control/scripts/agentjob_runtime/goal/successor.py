"""One-intent, one-identity successor reservation and provider recording."""

from __future__ import annotations

import copy
import secrets
from typing import Any, Mapping

from agentjob_runtime.errors import AgentJobControlError, RecordValidationError, StateConflict
from agentjob_runtime.goal.leases import DEFAULT_LEASE_SECONDS, require_active_lease
from agentjob_runtime.goal.model import add_seconds, map_stop, parse_utc, utc_now
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.verify import finalize_verified_receipt


RESERVABLE_PHASES = {"initialized", "continuation_required", "recovery_pending"}


class InjectedSuccessorFault(AgentJobControlError):
    code = "successor.injected_fault"
    exit_code = 93


def reserve_successor(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    current_holder_token: str,
    predecessor_thread_id: str | None,
    handoff_token: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    now = timestamp or utc_now()
    parse_utc(now)
    token = handoff_token or secrets.token_hex(24)
    if len(token) < 32:
        raise RecordValidationError("handoff token must contain at least 32 characters")
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        prior_phase = record["state"]["phase"]
        if prior_phase not in RESERVABLE_PHASES:
            raise StateConflict(f"cannot reserve a successor from {prior_phase}")
        require_active_lease(record, holder_token=current_holder_token)
        generation = record["state"]["current_generation"] + 1
        key = str(generation)
        if key in record["generations"]:
            raise StateConflict("successor generation already exists")
        idempotency_key = f"{goal_id}:{generation}"
        record["generations"][key] = {
            "generation": generation,
            "handoff_token": token,
            "idempotency_key": idempotency_key,
            "phase": "successor_intent",
            "lease_token": token,
            "invocation_consumed": False,
            "invocation_state": "not_authorized",
            "consumed_at": None,
            "returned_at": None,
            "before_fingerprint": record["state"]["last_canonical_fingerprint"],
            "after_fingerprint": None,
            "pending_step_result": None,
            "finalized_receipt_hash": None,
            "terminal_or_successor_outcome": None,
            "claimed_at": None,
            "successor_thread_id": None,
        }
        record["state"]["phase"] = "successor_intent"
        record["state"]["current_generation"] = generation
        record["handoff"] = {
            "status": "intent",
            "generation": generation,
            "token": token,
            "idempotency_key": idempotency_key,
            "predecessor_thread_id": predecessor_thread_id,
            "successor_thread_id": None,
        }
        mutation.replace_lease(
            generation=generation,
            holder_kind="successor_reserved",
            holder_token=token,
            expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
        )
        mutation.event(
            "successor_intent",
            {
                "generation": generation,
                "handoff_token": token,
                "idempotency_key": idempotency_key,
                "predecessor_thread_id": predecessor_thread_id,
            },
        )
    return store.load_goal(goal_id)


def record_successor(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    handoff_token: str,
    successor_thread_id: str,
    provider_id: str,
    provider_response: Mapping[str, Any],
    timestamp: str | None = None,
    fault_after: str | None = None,
) -> dict[str, Any]:
    if not successor_thread_id.strip() or not provider_id.strip():
        raise RecordValidationError("successor and provider IDs must be nonblank")
    current = store.load_goal(goal_id)
    handoff = current["handoff"]
    if (
        current["state"]["phase"] == "successor_created"
        and handoff.get("generation") == generation
        and handoff.get("token") == handoff_token
        and handoff.get("successor_thread_id") == successor_thread_id
    ):
        return current
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        handoff = record["handoff"]
        if record["state"]["phase"] != "successor_intent":
            raise StateConflict("successor identity can be recorded only from successor_intent")
        if handoff.get("generation") != generation or handoff.get("token") != handoff_token:
            raise StateConflict("successor handoff identity mismatch")
        entry = record["generations"].get(str(generation))
        if entry is None:
            raise StateConflict("successor generation does not exist")
        if entry["successor_thread_id"] not in (None, successor_thread_id):
            raise StateConflict("a different successor identity is already recorded")
        entry["phase"] = "successor_created"
        entry["successor_thread_id"] = successor_thread_id
        entry["terminal_or_successor_outcome"] = "successor_created"
        handoff["status"] = "successor_created"
        handoff["successor_thread_id"] = successor_thread_id
        record["state"]["phase"] = "successor_created"
        prior_generation = generation - 1
        if prior_generation > 0:
            prior = record["generations"][str(prior_generation)]
            if (
                prior.get("pending_step_result") is not None
                and prior.get("finalized_receipt_hash") is None
            ):
                finalize_verified_receipt(
                    mutation,
                    generation=prior_generation,
                    decision="continuation_required",
                    successor_thread_id=successor_thread_id,
                )
                if fault_after == "prior_receipt":
                    raise InjectedSuccessorFault("injected fault after prior receipt")
        mutation.provider_receipt(
            generation=generation,
            provider_id=provider_id,
            idempotency_key=entry["idempotency_key"],
            provider_status="returned",
            returned_thread_id=successor_thread_id,
            response=provider_response,
        )
        if fault_after == "provider_receipt":
            raise InjectedSuccessorFault("injected fault after provider receipt")
        mutation.replace_lease(
            generation=generation,
            holder_kind="successor_reserved",
            holder_token=handoff_token,
            expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
        )
        if fault_after == "lease_transfer":
            raise InjectedSuccessorFault("injected fault after lease transfer")
        mutation.event(
            "successor_created",
            {
                "generation": generation,
                "idempotency_key": entry["idempotency_key"],
                "provider_id": provider_id,
                "successor_thread_id": successor_thread_id,
            },
        )
    return store.load_goal(goal_id)


def record_dispatch_outcome(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    handoff_token: str,
    provider_id: str,
    outcome: str,
    diagnostic: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    reason_by_outcome = {
        "definitive_failure": "dispatch_failed",
        "ambiguous": "ambiguous_dispatch",
        "timeout": "handoff_timeout",
        "duplicate": "duplicate",
    }
    if outcome not in reason_by_outcome:
        raise RecordValidationError("unsupported provider dispatch outcome")
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        handoff = record["handoff"]
        if record["state"]["phase"] != "successor_intent":
            raise StateConflict("dispatch outcome requires successor_intent")
        if handoff.get("generation") != generation or handoff.get("token") != handoff_token:
            raise StateConflict("dispatch outcome handoff identity mismatch")
        entry = record["generations"][str(generation)]
        terminal = map_stop(reason_by_outcome[outcome])
        entry["phase"] = terminal
        entry["terminal_or_successor_outcome"] = (
            "failed" if outcome == "definitive_failure" else outcome
        )
        prior_generation = generation - 1
        if prior_generation > 0:
            prior = record["generations"].get(str(prior_generation))
            if (
                prior is not None
                and prior.get("pending_step_result") is not None
                and prior.get("finalized_receipt_hash") is None
            ):
                finalize_verified_receipt(
                    mutation,
                    generation=prior_generation,
                    decision="unknown"
                    if outcome in {"ambiguous", "timeout"}
                    else "failed",
                )
        handoff["status"] = "failed" if outcome in {"definitive_failure", "duplicate"} else outcome
        record["state"]["phase"] = terminal
        record["state"]["terminal_reason"] = reason_by_outcome[outcome]
        mutation.provider_receipt(
            generation=generation,
            provider_id=provider_id,
            idempotency_key=entry["idempotency_key"],
            provider_status=outcome,
            returned_thread_id=None,
            response=diagnostic,
        )
        mutation.event(
            "dispatch_outcome",
            {"generation": generation, "outcome": outcome, "diagnostic": copy.deepcopy(dict(diagnostic))},
        )
        if outcome == "ambiguous":
            mutation.replace_lease(
                generation=generation,
                holder_kind="quarantined",
                holder_token=secrets.token_hex(24),
                expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
            )
        else:
            mutation.release_lease()
    return store.load_goal(goal_id)
