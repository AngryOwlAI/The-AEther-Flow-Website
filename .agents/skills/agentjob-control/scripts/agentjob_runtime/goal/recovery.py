"""Authorized zero-work reconciliation for goal relay crash windows."""

from __future__ import annotations

import copy
import secrets
from typing import Any, Mapping, Protocol

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.initialize import _validate_completion_contract
from agentjob_runtime.goal.leases import DEFAULT_LEASE_SECONDS, require_active_lease
from agentjob_runtime.goal.model import (
    ABSORBING_TERMINALS,
    GOAL_SCHEMA_VERSION,
    PROFILED_GOAL_SCHEMA_VERSIONS,
    RECOVERABLE_TERMINALS,
    TERMINAL_PHASES,
    V3_TERMINAL_PHASES,
    add_seconds,
    effective_completion_contract,
    effective_guards,
    parse_utc,
    transition_allowed,
    utc_now,
)
from agentjob_runtime.goal.receipts import finalize_receipt
from agentjob_runtime.goal.resolution import (
    append_resolution,
    build_human_necessity_report,
    classify_resolution,
)
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.records.canonical import content_sha256


RECOVERY_ENTRY_PHASES = {
    "successor_intent",
    "step_active",
    "step_verifying",
    "step_verified",
    "continuation_required",
}


class QueryableThreadProvider(Protocol):
    provider_id: str

    def capabilities(self) -> Mapping[str, Any]: ...

    def query_by_idempotency_key(
        self, idempotency_key: str
    ) -> Mapping[str, Any]: ...


def _require_authority(
    user_authorization: str | None,
    evidence: Mapping[str, Any],
    *,
    allow_deterministic_reconciliation: bool = False,
) -> str:
    if not isinstance(evidence, Mapping) or not evidence:
        raise RecordValidationError("recovery requires canonical evidence")
    if isinstance(user_authorization, str) and user_authorization.strip():
        return user_authorization
    if (
        allow_deterministic_reconciliation
        and evidence.get("within_existing_authority") is True
        and evidence.get("deterministic_reconciliation") is True
    ):
        return "runtime:deterministic-reconciliation-within-existing-authority"
    raise RecordValidationError("authority-changing recovery requires exact user authorization")


def begin_recovery(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    user_authorization: str | None = None,
    evidence: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    authorization = _require_authority(
        user_authorization,
        evidence,
        allow_deterministic_reconciliation=True,
    )
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
            not transition_allowed(
                prior_phase,
                "recovery_pending",
                recovery=True,
                schema_version=record.get("schema_version"),
            )
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
            user_authorization=authorization,
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
    user_authorization: str | None = None,
    uniqueness_evidence: Mapping[str, Any],
    provider_id: str = "recovery-evidence",
    timestamp: str | None = None,
) -> dict[str, Any]:
    authorization = _require_authority(
        user_authorization,
        uniqueness_evidence,
        allow_deterministic_reconciliation=True,
    )
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
        if record.get("schema_version") in PROFILED_GOAL_SCHEMA_VERSIONS:
            effort = record["execution_profile"]["reasoning_effort"]
            binding_hash = content_sha256(record["repository_binding"])
            if (
                uniqueness_evidence.get("effective_reasoning_effort") != effort
                or uniqueness_evidence.get("environment_mode")
                != "reuse_bound_checkout"
                or uniqueness_evidence.get("repository_binding_sha256")
                != binding_hash
            ):
                raise RecordValidationError(
                    "adopted successor lacks exact execution-profile evidence"
                )
            entry["effective_reasoning_effort"] = effort
            entry["profile_evidence"] = copy.deepcopy(
                dict(uniqueness_evidence)
            )
            entry["observed_repository_topology"] = {
                "environment_mode": "reuse_bound_checkout",
                "repository_binding_sha256": binding_hash,
                **copy.deepcopy(
                    dict(
                        uniqueness_evidence.get("repository_topology") or {}
                    )
                ),
            }
            disposition = classify_resolution(
                reason_code="provider.unique_successor_adopted",
                status="reconciled",
                evidence=uniqueness_evidence,
                history=record["resolution_history"],
                authority_refs=["thread-provider.v2"],
                evidence_refs=[f"provider-intent:{entry['idempotency_key']}"],
            )
            append_resolution(
                record,
                generation=generation,
                disposition=disposition,
                progress_dimensions=["provider_reconciliation"],
            )
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
            user_authorization=authorization,
            evidence=uniqueness_evidence,
            prior_phase=prior_phase,
            resulting_phase="successor_created",
        )
    return store.load_goal(goal_id)


def _terminalize_provider_query(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    provider_id: str,
    query_evidence: Mapping[str, Any],
    integrity_incident: bool,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Persist an irreducible provider ambiguity without issuing another create."""

    now = timestamp or utc_now()
    terminal = (
        "terminal_integrity_incident"
        if integrity_incident
        else "terminal_awaiting_human"
    )
    reason_code = (
        "provider.multiple_successors"
        if integrity_incident
        else "provider.zero_versus_one_unknown"
    )
    with store.mutation(
        goal_id, expected_revision=expected_revision, timestamp=now
    ) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict(
                "provider-query reconciliation requires recovery_pending"
            )
        entry = record["generations"].get(str(generation))
        if entry is None or entry["invocation_consumed"]:
            raise StateConflict(
                "provider-query reconciliation requires one unconsumed intent"
            )
        disposition = classify_resolution(
            reason_code=reason_code,
            status="integrity_incident" if integrity_incident else "unknown",
            evidence=query_evidence,
            history=record["resolution_history"],
            authority_refs=["thread-provider.v2"],
            evidence_refs=[f"provider-intent:{entry['idempotency_key']}"],
            legal_route_available=False,
            integrity_incident=integrity_incident,
        )
        append_resolution(
            record,
            generation=generation,
            disposition=disposition,
            progress_dimensions=["provider_reconciliation"],
        )
        entry["phase"] = terminal
        entry["terminal_or_successor_outcome"] = (
            "duplicate" if integrity_incident else "ambiguous"
        )
        record["state"]["phase"] = terminal
        record["state"]["terminal_reason"] = reason_code
        record["handoff"]["status"] = (
            "failed" if integrity_incident else "ambiguous"
        )
        human = build_human_necessity_report(
            goal_id=goal_id,
            generation=generation,
            disposition=disposition,
            history=record["resolution_history"],
            required_human_authority_or_decision=(
                "Select the one canonical successor identity."
                if integrity_incident
                else "Determine whether the ambiguous provider create produced a successor."
            ),
            smallest_requested_user_action=(
                "Identify the canonical successor or cancel the relay."
            ),
            resume_contract=(
                "Resume only by reconciling this existing idempotency key; never issue a second create."
            ),
            policy_authority_refs=["thread-provider.v2:successor-uniqueness"],
            evidence_refs=[f"provider-intent:{entry['idempotency_key']}"],
            timestamp=now,
        )
        record["human_intervention"] = human
        entry["human_necessity_report_ref"] = human["report_id"]
        mutation.provider_receipt(
            generation=generation,
            provider_id=provider_id,
            idempotency_key=entry["idempotency_key"],
            provider_status="duplicate" if integrity_incident else "ambiguous",
            returned_thread_id=None,
            response=query_evidence,
        )
        mutation.recovery(
            "provider_query_incident"
            if integrity_incident
            else "provider_query_unresolved",
            user_authorization=(
                "runtime:deterministic-reconciliation-within-existing-authority"
            ),
            evidence=query_evidence,
            prior_phase="recovery_pending",
            resulting_phase=terminal,
        )
        mutation.release_lease()
    return store.load_goal(goal_id)


def reconcile_ambiguous_provider_create(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    provider: QueryableThreadProvider,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Query one ambiguous create by idempotency key and never create again."""

    record = store.load_goal(goal_id)
    if record["state"]["revision"] != expected_revision:
        raise StateConflict("provider reconciliation expected revision is stale")
    if record["state"]["phase"] != "recovery_pending":
        raise StateConflict("provider reconciliation requires recovery_pending")
    entry = record["generations"].get(str(generation))
    if (
        entry is None
        or entry["invocation_consumed"]
        or entry["successor_thread_id"] is not None
        or entry["terminal_or_successor_outcome"] not in {"ambiguous", "timeout"}
    ):
        raise StateConflict(
            "provider reconciliation requires one ambiguous unconsumed create intent"
        )
    capabilities = (
        provider.capabilities()
        if callable(getattr(provider, "capabilities", None))
        else {}
    )
    if (
        capabilities.get("can_query_by_idempotency_key") is not True
        or not callable(getattr(provider, "query_by_idempotency_key", None))
    ):
        return _terminalize_provider_query(
            store,
            goal_id=goal_id,
            expected_revision=expected_revision,
            generation=generation,
            provider_id=f"{provider.provider_id}:query",
            query_evidence={
                "query_status": "unsupported",
                "candidate_count": "unknown",
                "idempotency_key": entry["idempotency_key"],
            },
            integrity_incident=False,
            timestamp=timestamp,
        )
    try:
        raw = provider.query_by_idempotency_key(entry["idempotency_key"])
        query = copy.deepcopy(dict(raw))
    except Exception as error:
        query = {
            "query_status": "unknown",
            "candidate_count": "unknown",
            "exception_type": type(error).__name__,
        }
    candidates_value = query.get("candidates", ())
    candidates = (
        [copy.deepcopy(dict(item)) for item in candidates_value]
        if isinstance(candidates_value, (list, tuple))
        and all(isinstance(item, Mapping) for item in candidates_value)
        else []
    )
    live = [
        item
        for item in candidates
        if item.get("status") == "live"
        and isinstance(item.get("thread_id"), str)
        and item["thread_id"].strip()
    ]
    evidence = {
        **query,
        "idempotency_key": entry["idempotency_key"],
        "candidate_count": len(live),
        "within_existing_authority": True,
        "deterministic_reconciliation": True,
    }
    if len(live) == 1:
        candidate = live[0]
        uniqueness = {
            **evidence,
            **candidate,
            "candidate_count": 1,
            "thread_id": candidate["thread_id"],
            "status": "live",
        }
        return adopt_successor(
            store,
            goal_id=goal_id,
            expected_revision=expected_revision,
            generation=generation,
            successor_thread_id=str(candidate["thread_id"]),
            uniqueness_evidence=uniqueness,
            provider_id=f"{provider.provider_id}:query",
            timestamp=timestamp,
        )
    if len(live) > 1:
        return _terminalize_provider_query(
            store,
            goal_id=goal_id,
            expected_revision=expected_revision,
            generation=generation,
            provider_id=f"{provider.provider_id}:query",
            query_evidence=evidence,
            integrity_incident=True,
            timestamp=timestamp,
        )
    if query.get("definitive_none") is True:
        now = timestamp or utc_now()
        with store.mutation(
            goal_id, expected_revision=expected_revision, timestamp=now
        ) as mutation:
            current = mutation.record
            current_entry = current["generations"][str(generation)]
            disposition = classify_resolution(
                reason_code="provider.definitive_no_successor",
                status="reconciled",
                evidence=evidence,
                history=current["resolution_history"],
                authority_refs=["thread-provider.v2"],
                evidence_refs=[
                    f"provider-intent:{current_entry['idempotency_key']}"
                ],
            )
            append_resolution(
                current,
                generation=generation,
                disposition=disposition,
                progress_dimensions=["provider_reconciliation"],
            )
            mutation.provider_receipt(
                generation=generation,
                provider_id=f"{provider.provider_id}:query",
                idempotency_key=current_entry["idempotency_key"],
                provider_status="returned",
                returned_thread_id=None,
                response=evidence,
            )
            mutation.recovery(
                "provider_query_definitive_none",
                user_authorization=(
                    "runtime:deterministic-reconciliation-within-existing-authority"
                ),
                evidence=evidence,
                prior_phase="recovery_pending",
                resulting_phase="recovery_pending",
            )
        return store.load_goal(goal_id)
    return _terminalize_provider_query(
        store,
        goal_id=goal_id,
        expected_revision=expected_revision,
        generation=generation,
        provider_id=f"{provider.provider_id}:query",
        query_evidence=evidence,
        integrity_incident=False,
        timestamp=timestamp,
    )


def resume_relay(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    user_authorization: str | None = None,
    evidence: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    authorization = _require_authority(
        user_authorization,
        evidence,
        allow_deterministic_reconciliation=True,
    )
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
            user_authorization=authorization,
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
    authorization = _require_authority(user_authorization, evidence)
    validated = _validate_completion_contract(new_contract)
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict("contract amendment requires recovery_pending")
        prior = effective_completion_contract(record)
        amendment = {
            "kind": "completion_contract",
            "user_authorization": authorization,
            "created_at": now,
            "prior_effective_sha256": content_sha256(prior),
            "new_value": validated,
            "new_sha256": content_sha256(validated),
        }
        record["amendments"].append(amendment)
        mutation.amendment(amendment)
        mutation.recovery(
            "amend_contract",
            user_authorization=authorization,
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
    authorization = _require_authority(user_authorization, evidence)
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
            previous_passes = prior["max_continue_passes"]
            if (
                previous_passes is None
                or isinstance(proposed, bool)
                or not isinstance(proposed, int)
                or proposed <= previous_passes
            ):
                raise RecordValidationError("max_continue_passes may only increase")
        if "deadline_at" in new_guards:
            previous_deadline = prior.get("deadline_at", record["deadline_at"])
            proposed_deadline = new_guards["deadline_at"]
            if (
                previous_deadline is None
                or not isinstance(proposed_deadline, str)
                or parse_utc(proposed_deadline) <= parse_utc(previous_deadline)
            ):
                raise RecordValidationError("deadline_at may only move later")
        effective_new = copy.deepcopy(prior)
        effective_new.update(copy.deepcopy(dict(new_guards)))
        amendment = {
            "kind": "guards",
            "user_authorization": authorization,
            "created_at": now,
            "prior_effective_sha256": content_sha256(prior),
            "new_value": copy.deepcopy(dict(new_guards)),
            "new_sha256": content_sha256(effective_new),
        }
        record["amendments"].append(amendment)
        mutation.amendment(amendment)
        mutation.recovery(
            "amend_guards",
            user_authorization=authorization,
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
    authorization = _require_authority(
        user_authorization, terminal_holder_proof
    )
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        entry = record["generations"].get(str(generation))
        if record["state"]["phase"] != "step_active" or entry is None:
            raise StateConflict("abandonment requires an active generation")
        if entry["invocation_consumed"]:
            raise StateConflict("consumed work cannot be abandoned as zero execution")
        prior_phase = record["state"]["phase"]
        profiled = record.get("schema_version") in PROFILED_GOAL_SCHEMA_VERSIONS
        resulting_phase = (
            "recovery_pending" if profiled else "terminal_failed"
        )
        entry["phase"] = resulting_phase
        record["state"]["phase"] = resulting_phase
        record["state"]["terminal_reason"] = (
            None if profiled else "abandoned_unconsumed"
        )
        if profiled:
            disposition = classify_resolution(
                reason_code="recovery.unconsumed_generation_abandoned",
                status="recovery_pending",
                evidence=terminal_holder_proof,
                history=record["resolution_history"],
                authority_refs=["goal-relay:at-most-once"],
                evidence_refs=[f"generation:{generation}:terminal-holder"],
            )
            append_resolution(
                record,
                generation=generation,
                disposition=disposition,
                progress_dimensions=[
                    "blocker_resolution",
                    "canonical_evidence",
                ],
            )
        finalize_receipt(
            mutation,
            generation=generation,
            invocation_count=0,
            decision="unknown" if profiled else "failed",
            evidence={
                "zero_job_reason": "holder proved terminal before invocation consumption",
                "goal_evaluation": "unmet",
                "progress_summary": "The unconsumed generation was abandoned through recovery.",
                "remaining_work": (
                    "Prove a legal route, then resume the same immutable goal."
                    if profiled
                    else "A new generation requires explicit recovery and a legal route."
                ),
            },
        )
        mutation.recovery(
            "abandon",
            user_authorization=authorization,
            evidence=terminal_holder_proof,
            prior_phase=prior_phase,
            resulting_phase=resulting_phase,
        )
        if profiled:
            mutation.replace_lease(
                generation=generation,
                holder_kind="continuation",
                holder_token=secrets.token_hex(24),
                expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
            )
        else:
            mutation.release_lease()
    return store.load_goal(goal_id)


def reconcile_consumed(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    user_authorization: str | None = None,
    terminal_holder_proof: Mapping[str, Any],
    canonical_evidence: Mapping[str, Any],
    returned_proven: bool,
    decision: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    combined_reconciliation_evidence = {
        **copy.deepcopy(dict(terminal_holder_proof)),
        "within_existing_authority": canonical_evidence.get(
            "within_existing_authority"
        ),
        "deterministic_reconciliation": canonical_evidence.get(
            "deterministic_reconciliation"
        ),
    }
    authorization = _require_authority(
        user_authorization,
        combined_reconciliation_evidence,
        allow_deterministic_reconciliation=True,
    )
    if not isinstance(canonical_evidence, Mapping) or not canonical_evidence:
        raise RecordValidationError("consumed reconciliation requires canonical evidence")
    if decision not in TERMINAL_PHASES | V3_TERMINAL_PHASES | {"continuation_required"}:
        raise RecordValidationError("invalid reconciliation decision")
    if decision == "continuation_required" and not returned_proven:
        raise StateConflict("unknown invocation cannot authorize automatic continuation")
    if (
        decision == "terminal_complete"
        and (
            not returned_proven
            or canonical_evidence.get("goal_evaluation") != "met"
        )
    ):
        raise StateConflict(
            "reconciled completion requires uniquely reconstructed canonical met evidence"
        )
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
            user_authorization=authorization,
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
            if record.get("schema_version") in PROFILED_GOAL_SCHEMA_VERSIONS:
                if decision not in V3_TERMINAL_PHASES:
                    raise RecordValidationError(
                        "goal v3 reconciliation requires a v3 terminal phase"
                    )
                disposition = classify_resolution(
                    reason_code="recovery.consumed_invocation_unreconstructable"
                    if not returned_proven
                    else "recovery.reconstructed_terminal",
                    status="unknown" if not returned_proven else decision,
                    evidence=canonical_evidence,
                    history=record["resolution_history"],
                    authority_refs=["goal-relay:at-most-once"],
                    evidence_refs=[f"generation:{generation}:recovery"],
                    legal_route_available=False,
                    integrity_incident=decision
                    == "terminal_integrity_incident",
                    policy_limit=decision == "terminal_policy_limit",
                    cancelled=decision == "terminal_cancelled",
                    goal_reached=decision == "terminal_complete",
                )
                append_resolution(
                    record,
                    generation=generation,
                    disposition=disposition,
                    progress_dimensions=["canonical_evidence"],
                )
                if decision != "terminal_complete":
                    human = build_human_necessity_report(
                        goal_id=record["goal_id"],
                        generation=generation,
                        disposition=disposition,
                        history=record["resolution_history"],
                        required_human_authority_or_decision=(
                            "Resolve the irreducible consumed-invocation uncertainty."
                        ),
                        smallest_requested_user_action=(
                            "Confirm the canonical outcome of the consumed invocation."
                        ),
                        resume_contract=(
                            "Resume only by reconciling this same consumed generation; never rerun it."
                        ),
                        policy_authority_refs=["goal-relay:at-most-once"],
                        evidence_refs=[f"generation:{generation}:recovery"],
                        timestamp=now,
                    )
                    record["human_intervention"] = human
                    entry["human_necessity_report_ref"] = human["report_id"]
            finalize_receipt(
                mutation,
                generation=generation,
                invocation_count=1 if returned_proven else "unknown",
                decision=(
                    "terminal_complete"
                    if decision == "terminal_complete"
                    else "policy_limit_reached"
                    if decision == "terminal_policy_limit"
                    else "integrity_incident"
                    if decision == "terminal_integrity_incident"
                    else "cancelled"
                    if decision == "terminal_cancelled"
                    else "unknown"
                )
                if record.get("schema_version") in PROFILED_GOAL_SCHEMA_VERSIONS
                else "failed"
                if returned_proven
                else "unknown",
                evidence=receipt_evidence,
            )
            if (
                record.get("schema_version") in PROFILED_GOAL_SCHEMA_VERSIONS
                and decision == "terminal_complete"
            ):
                from agentjob_runtime.goal.completion_report import (
                    build_completion_report,
                )

                completion = build_completion_report(record, completed_at=now)
                record["completion_report"] = completion
                entry["completion_report_ref"] = completion["report_id"]
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
    authorization = _require_authority(user_authorization, evidence)
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        if record["state"]["phase"] != "recovery_pending":
            raise StateConflict("cancellation requires recovery_pending")
        prior_phase = record["state"]["phase"]
        generation = int(record["state"]["current_generation"])
        record["state"]["phase"] = "terminal_cancelled"
        record["state"]["terminal_reason"] = "cancelled"
        if record.get("schema_version") in PROFILED_GOAL_SCHEMA_VERSIONS:
            if generation < 1 or str(generation) not in record["generations"]:
                raise StateConflict(
                    "v3 cancellation requires an existing relay generation"
                )
            disposition = classify_resolution(
                reason_code="goal.cancelled",
                status="cancelled",
                evidence=evidence,
                history=record["resolution_history"],
                authority_refs=["user-cancellation"],
                evidence_refs=[f"goal:{goal_id}:cancellation"],
                cancelled=True,
            )
            append_resolution(
                record,
                generation=generation,
                disposition=disposition,
                progress_dimensions=[],
            )
            human = build_human_necessity_report(
                goal_id=goal_id,
                generation=generation,
                disposition=disposition,
                history=record["resolution_history"],
                required_human_authority_or_decision=(
                    "The user explicitly cancelled the relay."
                ),
                smallest_requested_user_action=(
                    "Create a newly accepted goal to resume cancelled work."
                ),
                resume_contract=(
                    "This cancelled goal is immutable; any resumption requires a new accepted goal."
                ),
                policy_authority_refs=["user-cancellation"],
                evidence_refs=[f"goal:{goal_id}:cancellation"],
                timestamp=now,
            )
            record["human_intervention"] = human
            record["generations"][str(generation)][
                "human_necessity_report_ref"
            ] = human["report_id"]
        mutation.recovery(
            "cancel",
            user_authorization=authorization,
            evidence=evidence,
            prior_phase=prior_phase,
            resulting_phase="terminal_cancelled",
        )
        mutation.release_lease()
    return store.load_goal(goal_id)
