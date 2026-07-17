"""Authorized zero-work reconciliation for goal relay crash windows."""

from __future__ import annotations

import copy
import secrets
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.initialize import _validate_completion_contract
from agentjob_runtime.goal.leases import DEFAULT_LEASE_SECONDS, require_active_lease
from agentjob_runtime.goal.model import (
    ABSORBING_TERMINALS,
    RECOVERABLE_TERMINALS,
    TERMINAL_PHASES,
    add_seconds,
    effective_completion_contract,
    effective_guards,
    parse_utc,
    transition_allowed,
    utc_now,
)
from agentjob_runtime.goal.receipts import finalize_receipt
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.records.canonical import content_sha256


RECOVERY_ENTRY_PHASES = {
    "successor_intent",
    "step_active",
    "step_verifying",
    "step_verified",
    "continuation_required",
}


def _require_authority(user_authorization: str, evidence: Mapping[str, Any]) -> None:
    if not isinstance(user_authorization, str) or not user_authorization.strip():
        raise RecordValidationError("recovery requires exact user authorization")
    if not isinstance(evidence, Mapping) or not evidence:
        raise RecordValidationError("recovery requires canonical evidence")


def begin_recovery(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    user_authorization: str,
    evidence: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    _require_authority(user_authorization, evidence)
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        prior_phase = record["state"]["phase"]
        if prior_phase in ABSORBING_TERMINALS:
            raise StateConflict(f"absorbing terminal cannot enter recovery: {prior_phase}")
        if prior_phase not in RECOVERABLE_TERMINALS and prior_phase not in RECOVERY_ENTRY_PHASES:
            raise StateConflict(f"phase is not recoverable: {prior_phase}")
        if prior_phase == "step_active" and not isinstance(evidence.get("terminal_holder_proof"), Mapping):
            raise RecordValidationError("active-step recovery requires terminal-holder proof")
        if (
            not transition_allowed(prior_phase, "recovery_pending", recovery=True)
            and prior_phase not in RECOVERY_ENTRY_PHASES
        ):
            raise StateConflict(f"unlisted recovery transition: {prior_phase} -> recovery_pending")
        prior_lease = record["state"].get("active_lease")
        generation = record["state"]["current_generation"]
        recovery_token = secrets.token_hex(24)
        mutation.replace_lease(
            generation=generation,
            holder_kind="continuation",
            holder_token=recovery_token,
            expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
        )
        record["state"]["phase"] = "recovery_pending"
        record["state"]["terminal_reason"] = None
        mutation.recovery(
            "begin",
            user_authorization=user_authorization,
            evidence={
                **copy.deepcopy(dict(evidence)),
                "prior_lease_transaction_id": prior_lease.get("transaction_id") if prior_lease else None,
            },
            prior_phase=prior_phase,
            resulting_phase="recovery_pending",
        )
    return store.load_goal(goal_id)


def adopt_successor(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    successor_thread_id: str,
    user_authorization: str,
    uniqueness_evidence: Mapping[str, Any],
    provider_id: str = "recovery-evidence",
    timestamp: str | None = None,
) -> dict[str, Any]:
    _require_authority(user_authorization, uniqueness_evidence)
    if (
        uniqueness_evidence.get("candidate_count") != 1
        or uniqueness_evidence.get("thread_id") != successor_thread_id
        or uniqueness_evidence.get("status") != "live"
    ):
        raise RecordValidationError("successor adoption requires proof of exactly one matching live successor")
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict("successor adoption requires recovery_pending")
        entry = record["generations"].get(str(generation))
        if entry is None:
            raise StateConflict("successor intent does not exist")
        if entry["invocation_consumed"] or entry["claimed_at"] is not None:
            raise StateConflict("a claimed or consumed generation cannot be adopted")
        if entry["successor_thread_id"] not in (None, successor_thread_id):
            raise StateConflict("a different successor is already recorded")
        prior_phase = record["state"]["phase"]
        entry["phase"] = "successor_created"
        entry["successor_thread_id"] = successor_thread_id
        entry["terminal_or_successor_outcome"] = "successor_created"
        record["state"]["phase"] = "successor_created"
        record["handoff"] = {
            "status": "successor_created",
            "generation": generation,
            "token": entry["handoff_token"],
            "idempotency_key": entry["idempotency_key"],
            "predecessor_thread_id": record["handoff"].get("predecessor_thread_id"),
            "successor_thread_id": successor_thread_id,
        }
        mutation.provider_receipt(
            generation=generation,
            provider_id=provider_id,
            idempotency_key=entry["idempotency_key"],
            provider_status="returned",
            returned_thread_id=successor_thread_id,
            response=uniqueness_evidence,
        )
        mutation.replace_lease(
            generation=generation,
            holder_kind="successor_reserved",
            holder_token=entry["handoff_token"],
            expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
        )
        mutation.recovery(
            "adopt",
            user_authorization=user_authorization,
            evidence=uniqueness_evidence,
            prior_phase=prior_phase,
            resulting_phase="successor_created",
        )
    return store.load_goal(goal_id)


def resume_relay(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    user_authorization: str,
    evidence: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    _require_authority(user_authorization, evidence)
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict("resume requires recovery_pending")
        require_active_lease(record, holder_kinds={"continuation"})
        if evidence.get("legal_route_available") is not True:
            raise RecordValidationError("resume requires canonical proof of a legal route")
        record["state"]["phase"] = "continuation_required"
        record["state"]["goal_evaluation"] = "unmet"
        mutation.recovery(
            "resume",
            user_authorization=user_authorization,
            evidence=evidence,
            prior_phase="recovery_pending",
            resulting_phase="continuation_required",
        )
    return store.load_goal(goal_id)


def amend_completion_contract(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    user_authorization: str,
    evidence: Mapping[str, Any],
    new_contract: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    _require_authority(user_authorization, evidence)
    validated = _validate_completion_contract(new_contract)
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict("contract amendment requires recovery_pending")
        prior = effective_completion_contract(record)
        amendment = {
            "kind": "completion_contract",
            "user_authorization": user_authorization,
            "created_at": now,
            "prior_effective_sha256": content_sha256(prior),
            "new_value": validated,
            "new_sha256": content_sha256(validated),
        }
        record["amendments"].append(amendment)
        mutation.amendment(amendment)
        mutation.recovery(
            "amend_contract",
            user_authorization=user_authorization,
            evidence=evidence,
            prior_phase="recovery_pending",
            resulting_phase="recovery_pending",
        )
    return store.load_goal(goal_id)


def amend_guards(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    user_authorization: str,
    evidence: Mapping[str, Any],
    new_guards: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    _require_authority(user_authorization, evidence)
    if not new_guards or not set(new_guards) <= {"max_continue_passes", "deadline_at"}:
        raise RecordValidationError("guard amendment may only extend pass count or deadline")
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict("guard amendment requires recovery_pending")
        prior = effective_guards(record)
        if "max_continue_passes" in new_guards:
            proposed = new_guards["max_continue_passes"]
            if not isinstance(proposed, int) or proposed <= prior["max_continue_passes"]:
                raise RecordValidationError("max_continue_passes may only increase")
        if "deadline_at" in new_guards:
            previous_deadline = prior.get("deadline_at", record["deadline_at"])
            if parse_utc(new_guards["deadline_at"]) <= parse_utc(previous_deadline):
                raise RecordValidationError("deadline_at may only move later")
        effective_new = copy.deepcopy(prior)
        effective_new.update(copy.deepcopy(dict(new_guards)))
        amendment = {
            "kind": "guards",
            "user_authorization": user_authorization,
            "created_at": now,
            "prior_effective_sha256": content_sha256(prior),
            "new_value": copy.deepcopy(dict(new_guards)),
            "new_sha256": content_sha256(effective_new),
        }
        record["amendments"].append(amendment)
        mutation.amendment(amendment)
        mutation.recovery(
            "amend_guards",
            user_authorization=user_authorization,
            evidence=evidence,
            prior_phase="recovery_pending",
            resulting_phase="recovery_pending",
        )
    return store.load_goal(goal_id)


def abandon_unconsumed(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    user_authorization: str,
    terminal_holder_proof: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    _require_authority(user_authorization, terminal_holder_proof)
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        entry = record["generations"].get(str(generation))
        if record["state"]["phase"] != "step_active" or entry is None:
            raise StateConflict("abandonment requires an active generation")
        if entry["invocation_consumed"]:
            raise StateConflict("consumed work cannot be abandoned as zero execution")
        prior_phase = record["state"]["phase"]
        entry["phase"] = "terminal_failed"
        record["state"]["phase"] = "terminal_failed"
        record["state"]["terminal_reason"] = "abandoned_unconsumed"
        finalize_receipt(
            mutation,
            generation=generation,
            invocation_count=0,
            decision="failed",
            evidence={
                "zero_job_reason": "holder proved terminal before invocation consumption",
                "goal_evaluation": "unmet",
                "progress_summary": "The unconsumed generation was abandoned through recovery.",
                "remaining_work": "A new generation requires explicit recovery and a legal route.",
            },
        )
        mutation.recovery(
            "abandon",
            user_authorization=user_authorization,
            evidence=terminal_holder_proof,
            prior_phase=prior_phase,
            resulting_phase="terminal_failed",
        )
        mutation.release_lease()
    return store.load_goal(goal_id)


def reconcile_consumed(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    user_authorization: str,
    terminal_holder_proof: Mapping[str, Any],
    canonical_evidence: Mapping[str, Any],
    returned_proven: bool,
    decision: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    _require_authority(user_authorization, terminal_holder_proof)
    if not isinstance(canonical_evidence, Mapping) or not canonical_evidence:
        raise RecordValidationError("consumed reconciliation requires canonical evidence")
    if decision not in TERMINAL_PHASES | {"continuation_required"}:
        raise RecordValidationError("invalid reconciliation decision")
    if decision == "continuation_required" and not returned_proven:
        raise StateConflict("unknown invocation cannot authorize automatic continuation")
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict("consumed reconciliation requires recovery_pending")
        entry = record["generations"].get(str(generation))
        if entry is None or not entry["invocation_consumed"]:
            raise StateConflict("generation was not consumed")
        if entry["finalized_receipt_hash"] is not None:
            raise StateConflict("generation already has a finalized receipt")
        prior_phase = record["state"]["phase"]
        entry["invocation_state"] = "returned" if returned_proven else "unknown"
        entry["after_fingerprint"] = canonical_evidence.get(
            "after_fingerprint", entry["after_fingerprint"] or entry["before_fingerprint"]
        )
        entry["fingerprint_status"] = canonical_evidence.get(
            "fingerprint_status", "new" if returned_proven else "unchanged"
        )
        record["state"]["goal_evaluation"] = canonical_evidence.get(
            "goal_evaluation", "unmet" if returned_proven else "indeterminate"
        )
        receipt_evidence = canonical_evidence.get("receipt_evidence")
        if not isinstance(receipt_evidence, Mapping):
            raise RecordValidationError("reconciliation requires complete receipt_evidence")
        mutation.recovery(
            "reconcile",
            user_authorization=user_authorization,
            evidence={
                "terminal_holder_proof": copy.deepcopy(dict(terminal_holder_proof)),
                "canonical_evidence": copy.deepcopy(dict(canonical_evidence)),
                "returned_proven": returned_proven,
            },
            prior_phase=prior_phase,
            resulting_phase=decision,
        )
        entry["phase"] = decision
        record["state"]["phase"] = decision
        if decision == "continuation_required":
            entry["pending_step_result"] = {
                "receipt_evidence": copy.deepcopy(dict(receipt_evidence)),
                "decision": decision,
            }
        else:
            record["state"]["terminal_reason"] = "reconciled_consumed_generation"
            finalize_receipt(
                mutation,
                generation=generation,
                invocation_count=1 if returned_proven else "unknown",
                decision="failed" if returned_proven else "unknown",
                evidence=receipt_evidence,
            )
            mutation.release_lease()
    return store.load_goal(goal_id)


def cancel_relay(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    user_authorization: str,
    evidence: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    _require_authority(user_authorization, evidence)
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict("cancellation requires recovery_pending")
        prior_phase = record["state"]["phase"]
        record["state"]["phase"] = "terminal_cancelled"
        record["state"]["terminal_reason"] = "cancelled"
        mutation.recovery(
            "cancel",
            user_authorization=user_authorization,
            evidence=evidence,
            prior_phase=prior_phase,
            resulting_phase="terminal_cancelled",
        )
        mutation.release_lease()
    return store.load_goal(goal_id)
