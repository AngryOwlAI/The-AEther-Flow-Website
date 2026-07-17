"""Token-bound generation worker with one continue call and one successor."""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.fingerprinting.canonical import FingerprintResult
from agentjob_runtime.goal.decide import decide_and_reserve_successor, decide_generation
from agentjob_runtime.goal.execution import (
    claim_generation,
    guard_precheck,
    pre_execution_stop,
    consume_invocation,
    record_invocation_returned,
    record_invocation_unknown,
)
from agentjob_runtime.goal.launcher import (
    ThreadCreateResult,
    ThreadProvider,
    build_continuation_envelope,
    build_worker_prompt,
)
from agentjob_runtime.goal.model import fingerprint_status
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_dispatch_outcome, record_successor
from agentjob_runtime.goal.verify import verify_generation
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.validation.schema import format_issues, validate_instance


@dataclass
class WorkerBudget:
    continue_calls: int = 0
    successor_calls: int = 0

    def claim_continue(self) -> None:
        if self.continue_calls >= 1:
            raise StateConflict(
                "one generation cannot invoke continue twice",
                details={"reason_code": "worker.continue_limit"},
            )
        self.continue_calls += 1

    def claim_successor(self) -> None:
        if self.successor_calls >= 1:
            raise StateConflict(
                "one generation cannot create two successors",
                details={"reason_code": "worker.successor_limit"},
            )
        self.successor_calls += 1


@dataclass(frozen=True)
class WorkerSummary:
    status: str
    goal_id: str
    generation: int
    state_phase: str
    state_revision: int
    goal_evaluation: str
    continue_invocations: int | str
    agentjobs_executed: int | str
    successor_create_calls: int
    successor_generation: int | None
    successor_thread_id: str | None
    successor_envelope_sha256: str | None
    receipt_hash: str | None
    recovery_required: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_envelope(
    store: SQLiteGoalStore,
    *,
    envelope: Mapping[str, Any],
    envelope_sha256: str,
    expected_revision: int,
    current_thread_id: str,
) -> dict[str, Any]:
    if not isinstance(envelope, Mapping):
        raise RecordValidationError("normal worker mode requires a continuation envelope")
    value = copy.deepcopy(dict(envelope))
    schema = Path(__file__).resolve().parents[3] / "schemas" / "continuation-envelope.schema.json"
    issues = validate_instance(value, schema)
    if issues:
        raise RecordValidationError(
            "worker continuation envelope failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    if content_sha256(value) != envelope_sha256:
        raise StateConflict("worker envelope hash mismatch")
    record = store.load_goal(str(value["goal_id"]))
    if record["state"]["revision"] != expected_revision:
        raise StateConflict(
            "worker expected revision is stale",
            details={
                "expected_revision": expected_revision,
                "actual_revision": record["state"]["revision"],
            },
        )
    if record["state"]["phase"] != "successor_created":
        raise StateConflict("predecessor has not recorded a claimable successor")
    generation = int(value["generation"])
    entry = record["generations"].get(str(generation))
    handoff = record["handoff"]
    if entry is None:
        raise StateConflict("worker generation is not reserved")
    exact_matches = (
        value["goal_sha256"] == record["goal_sha256"]
        and value["completion_contract_sha256"]
        == record["completion_contract_sha256"]
        and value["repository_binding"] == record["repository_binding"]
        and generation == record["state"]["current_generation"]
        and value["handoff_token"] == entry["handoff_token"]
        and value["idempotency_key"] == entry["idempotency_key"]
        and handoff.get("successor_thread_id") == current_thread_id
        and entry.get("successor_thread_id") == current_thread_id
    )
    if not exact_matches:
        raise StateConflict("worker token, generation, thread, or goal identity mismatch")
    if value.get("predecessor_thread_id") == current_thread_id:
        raise StateConflict("a generation must run in a fresh successor discussion")
    return record


def _validate_continue_result(result: Mapping[str, Any]) -> list[str]:
    schema = Path(__file__).resolve().parents[3] / "schemas" / "continue-result.schema.json"
    issues = validate_instance(result, schema)
    return format_issues(issues).splitlines() if issues else []


def _result_stop_reason(
    result: Mapping[str, Any], direct_evidence: Mapping[str, Any]
) -> str | None:
    status = result.get("status")
    if status == "human_gate_required" or direct_evidence.get("human_gate_outstanding") is True:
        return "human_gate"
    if status == "bootstrap_required":
        return "capability"
    checkpoint = direct_evidence.get("checkpoint", {})
    if isinstance(checkpoint, Mapping) and checkpoint.get("status") == "fail":
        return "checkpoint"
    validators = direct_evidence.get("validator_results", [])
    if any(
        isinstance(item, Mapping) and item.get("status") == "fail"
        for item in validators
    ):
        return "validation"
    if status == "failed":
        reason = str(result.get("reason_code", ""))
        return "checkpoint" if "checkpoint" in reason else "validation"
    return None


def _summary(
    record: Mapping[str, Any],
    *,
    generation: int,
    status: str,
    budget: WorkerBudget,
    agentjobs_executed: int | str,
    successor_envelope_sha256: str | None = None,
    recovery_required: bool = False,
) -> WorkerSummary:
    original = record["generations"].get(str(generation), {})
    current_generation = int(record["state"]["current_generation"])
    current = record["generations"].get(str(current_generation), {})
    successor_generation = current_generation if current_generation > generation else None
    return WorkerSummary(
        status,
        str(record["goal_id"]),
        generation,
        str(record["state"]["phase"]),
        int(record["state"]["revision"]),
        str(record["state"]["goal_evaluation"]),
        "unknown" if recovery_required and budget.continue_calls else budget.continue_calls,
        agentjobs_executed,
        budget.successor_calls,
        successor_generation,
        str(current.get("successor_thread_id"))
        if successor_generation and current.get("successor_thread_id")
        else None,
        successor_envelope_sha256,
        str(original.get("finalized_receipt_hash"))
        if original.get("finalized_receipt_hash")
        else None,
        recovery_required,
    )


def run_goal_worker(
    store: SQLiteGoalStore,
    *,
    envelope: Mapping[str, Any],
    envelope_sha256: str,
    expected_revision: int,
    current_thread_id: str,
    continue_invoker: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    direct_evidence_provider: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    observations: Mapping[str, bool] | None = None,
    legal_route_available: bool,
    successor_provider: ThreadProvider | None = None,
    claim_token: str | None = None,
    successor_handoff_token: str | None = None,
    timestamp: str | None = None,
) -> WorkerSummary:
    """Consume one normal-mode generation and stop after one successor at most."""

    record = _validate_envelope(
        store,
        envelope=envelope,
        envelope_sha256=envelope_sha256,
        expected_revision=expected_revision,
        current_thread_id=current_thread_id,
    )
    goal_id = str(record["goal_id"])
    generation = int(envelope["generation"])
    budget = WorkerBudget()
    claimed = claim_generation(
        store,
        goal_id=goal_id,
        expected_revision=expected_revision,
        generation=generation,
        handoff_token=str(envelope["handoff_token"]),
        idempotency_key=str(envelope["idempotency_key"]),
        successor_thread_id=current_thread_id,
        claim_token=claim_token,
        timestamp=timestamp,
    )
    effective_claim_token = str(claimed["generations"][str(generation)]["lease_token"])
    stops = guard_precheck(claimed, timestamp=timestamp, observations=observations)
    if stops:
        stopped = pre_execution_stop(
            store,
            goal_id=goal_id,
            expected_revision=int(claimed["state"]["revision"]),
            generation=generation,
            claim_token=effective_claim_token,
            stop_reason=stops[0],
            timestamp=timestamp,
        )
        return _summary(
            stopped,
            generation=generation,
            status="pre_execution_stop",
            budget=budget,
            agentjobs_executed=0,
        )
    consumed = consume_invocation(
        store,
        goal_id=goal_id,
        expected_revision=int(claimed["state"]["revision"]),
        generation=generation,
        claim_token=effective_claim_token,
        observations=observations,
        timestamp=timestamp,
    )
    budget.claim_continue()
    try:
        raw_result = continue_invoker(copy.deepcopy(dict(envelope)))
        result = copy.deepcopy(dict(raw_result))
    except Exception as error:  # The consumed call boundary is now uncertain.
        unknown = record_invocation_unknown(
            store,
            goal_id=goal_id,
            expected_revision=int(consumed["state"]["revision"]),
            generation=generation,
            claim_token=effective_claim_token,
            diagnostic={
                "reason_code": "worker.continue_outcome_unknown",
                "exception_type": type(error).__name__,
            },
            timestamp=timestamp,
        )
        return _summary(
            unknown,
            generation=generation,
            status="invocation_unknown",
            budget=budget,
            agentjobs_executed="unknown",
            recovery_required=True,
        )
    result_findings = _validate_continue_result(result)
    if result_findings:
        unknown = record_invocation_unknown(
            store,
            goal_id=goal_id,
            expected_revision=int(consumed["state"]["revision"]),
            generation=generation,
            claim_token=effective_claim_token,
            diagnostic={
                "reason_code": "worker.continue_result_invalid",
                "findings": result_findings,
            },
            timestamp=timestamp,
        )
        return _summary(
            unknown,
            generation=generation,
            status="invocation_unknown",
            budget=budget,
            agentjobs_executed="unknown",
            recovery_required=True,
        )
    returned = record_invocation_returned(
        store,
        goal_id=goal_id,
        expected_revision=int(consumed["state"]["revision"]),
        generation=generation,
        claim_token=effective_claim_token,
        continue_result=result,
        timestamp=timestamp,
    )
    direct_evidence = copy.deepcopy(dict(direct_evidence_provider(result)))
    after_hash = str(result["repository_fingerprint_after"])
    after = FingerprintResult(
        {"continue_result_sha256": content_sha256(result)},
        after_hash,
        fingerprint_status(
            returned["state"]["canonical_fingerprint_history"], after_hash
        ),
    )
    verified = verify_generation(
        store,
        goal_id=goal_id,
        expected_revision=int(returned["state"]["revision"]),
        generation=generation,
        claim_token=effective_claim_token,
        continue_result=result,
        after_fingerprint=after,
        direct_evidence=direct_evidence,
        timestamp=timestamp,
    )
    stop_reason = _result_stop_reason(result, direct_evidence)
    if stop_reason is not None:
        final = decide_generation(
            store,
            goal_id=goal_id,
            expected_revision=int(verified["state"]["revision"]),
            generation=generation,
            claim_token=effective_claim_token,
            legal_route_available=False,
            explicit_stop_reason=stop_reason,
            timestamp=timestamp,
        )
        return _summary(
            final,
            generation=generation,
            status="terminal",
            budget=budget,
            agentjobs_executed=result["agent_jobs_executed"],
        )
    if (
        verified["state"]["goal_evaluation"] == "unmet"
        and legal_route_available
        and (successor_provider is None or successor_provider.available is not True)
    ):
        final = decide_generation(
            store,
            goal_id=goal_id,
            expected_revision=int(verified["state"]["revision"]),
            generation=generation,
            claim_token=effective_claim_token,
            legal_route_available=False,
            explicit_stop_reason="capability",
            timestamp=timestamp,
        )
        return _summary(
            final,
            generation=generation,
            status="terminal",
            budget=budget,
            agentjobs_executed=result["agent_jobs_executed"],
        )
    decided = decide_and_reserve_successor(
        store,
        goal_id=goal_id,
        expected_revision=int(verified["state"]["revision"]),
        generation=generation,
        claim_token=effective_claim_token,
        predecessor_thread_id=current_thread_id,
        handoff_token=successor_handoff_token,
        timestamp=timestamp,
    ) if legal_route_available else decide_generation(
        store,
        goal_id=goal_id,
        expected_revision=int(verified["state"]["revision"]),
        generation=generation,
        claim_token=effective_claim_token,
        legal_route_available=False,
        timestamp=timestamp,
    )
    if decided["state"]["phase"] != "successor_intent":
        return _summary(
            decided,
            generation=generation,
            status="terminal",
            budget=budget,
            agentjobs_executed=result["agent_jobs_executed"],
        )
    next_generation = int(decided["state"]["current_generation"])
    next_entry = decided["generations"][str(next_generation)]
    next_envelope = build_continuation_envelope(
        decided,
        predecessor_thread_id=current_thread_id,
        predecessor_handoff_id=result.get("handoff_id"),
        canonical_state={
            "fingerprint": result["repository_fingerprint_after"],
            "active_task_id": result.get("task_id"),
            "current_decision_id": result.get("decision_id"),
            "current_job_id": result.get("job_id"),
        },
        progress_summary=str(direct_evidence.get("progress_summary") or "One generation was verified."),
        remaining_work=str(direct_evidence.get("remaining_work") or "Continue the durable goal."),
    )
    next_envelope_hash = content_sha256(next_envelope)
    prompt = build_worker_prompt(
        next_envelope,
        project_root=str(decided["repository_binding"]["root"]),
        expected_revision=int(decided["state"]["revision"]) + 1,
    )
    budget.claim_successor()
    try:
        provider_result = successor_provider.create_thread(
            prompt=prompt,
            envelope=next_envelope,
            idempotency_key=str(next_entry["idempotency_key"]),
        )
    except Exception as error:  # Unknown provider outcome must never be retried here.
        provider_result = ThreadCreateResult(
            "ambiguous",
            None,
            {"reason_code": "provider.exception", "exception_type": type(error).__name__},
        )
    provider_status = provider_result.status
    successor_id = provider_result.successor_thread_id
    if provider_status == "returned" and successor_id == current_thread_id:
        provider_status = "duplicate"
        successor_id = None
        provider_result = ThreadCreateResult(
            "duplicate", None, {"reason_code": "provider.reused_predecessor_thread"}
        )
    if provider_status == "returned":
        final = record_successor(
            store,
            goal_id=goal_id,
            expected_revision=int(decided["state"]["revision"]),
            generation=next_generation,
            handoff_token=str(next_entry["handoff_token"]),
            successor_thread_id=str(successor_id),
            provider_id=str(successor_provider.provider_id),
            provider_response=provider_result.response,
            timestamp=timestamp,
        )
        status = "successor_dispatched"
    elif provider_status == "manual_pending":
        final = decided
        status = "manual_handoff_pending"
    else:
        final = record_dispatch_outcome(
            store,
            goal_id=goal_id,
            expected_revision=int(decided["state"]["revision"]),
            generation=next_generation,
            handoff_token=str(next_entry["handoff_token"]),
            provider_id=str(successor_provider.provider_id),
            outcome=provider_status,
            diagnostic=provider_result.response,
            timestamp=timestamp,
        )
        status = "successor_dispatch_failed"
    return _summary(
        final,
        generation=generation,
        status=status,
        budget=budget,
        agentjobs_executed=result["agent_jobs_executed"],
        successor_envelope_sha256=next_envelope_hash,
        recovery_required=provider_status == "ambiguous",
    )
