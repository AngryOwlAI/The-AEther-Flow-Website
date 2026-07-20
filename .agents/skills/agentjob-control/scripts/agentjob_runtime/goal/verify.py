"""Direct goal verification and pending/final generation receipt evidence."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.fingerprinting.canonical import FingerprintResult, apply_fingerprint
from agentjob_runtime.goal.leases import require_active_lease
from agentjob_runtime.goal.model import (
    GOAL_SCHEMA_VERSION,
    effective_completion_contract,
    utc_now,
)
from agentjob_runtime.goal.receipts import finalize_receipt
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.validation.schema import format_issues, validate_instance


def _validate_continue_result(value: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RecordValidationError("structured continue result must be an object")
    result = copy.deepcopy(dict(value))
    schema_name = (
        "continue-result-v2.schema.json"
        if result.get("schema_version") == "sys4ai.continue-result.v2"
        else "continue-result.schema.json"
    )
    schema = Path(__file__).resolve().parents[3] / "schemas" / schema_name
    issues = validate_instance(result, schema)
    if issues:
        raise RecordValidationError(
            "structured continue result failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    return result


def evaluate_goal(
    record: Mapping[str, Any],
    *,
    direct_evidence: Mapping[str, Any],
) -> str:
    """Evaluate the effective completion contract only from structured canonical evidence."""

    contract = effective_completion_contract(record)
    results = direct_evidence.get("completion_contract_results")
    if not isinstance(results, list):
        raise RecordValidationError(
            "direct completion-contract results are required; worker prose is not canonical evidence"
        )
    expected = contract["required_evidence"]
    by_criterion: dict[str, Mapping[str, Any]] = {}
    for result in results:
        if not isinstance(result, Mapping) or result.get("criterion") in by_criterion:
            raise RecordValidationError("completion-contract results must be unique objects")
        by_criterion[str(result.get("criterion"))] = result
    if set(by_criterion) != set(expected):
        raise RecordValidationError("completion-contract results do not cover the effective contract exactly")
    statuses: list[str] = []
    for criterion in expected:
        result = by_criterion[criterion]
        status = result.get("status")
        refs = result.get("evidence_refs")
        if status not in {"pass", "fail", "indeterminate"}:
            raise RecordValidationError("completion criterion has an invalid status")
        if status == "pass" and (
            not isinstance(refs, list)
            or not refs
            or any(not isinstance(ref, str) or not ref.strip() for ref in refs)
        ):
            raise RecordValidationError("a passing completion criterion requires canonical evidence references")
        statuses.append(status)
    validators = direct_evidence.get("validator_results", [])
    if not isinstance(validators, list):
        raise RecordValidationError("validator_results must be a list")
    validator_statuses = {result.get("status") for result in validators if isinstance(result, Mapping)}
    checkpoint = direct_evidence.get("checkpoint")
    if not isinstance(checkpoint, Mapping):
        raise RecordValidationError("direct checkpoint evidence is required")
    checkpoint_status = checkpoint.get("status")
    if direct_evidence.get("human_gate_outstanding") is True:
        return "indeterminate"
    if "indeterminate" in statuses or "indeterminate" in validator_statuses or checkpoint_status == "unknown":
        return "indeterminate"
    if (
        statuses
        and all(status == "pass" for status in statuses)
        and not validator_statuses.intersection({"fail", "indeterminate", "skipped"})
        and checkpoint_status in {"pass", "not_required"}
    ):
        return "met"
    return "unmet"


def verify_generation(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    claim_token: str,
    continue_result: Mapping[str, Any],
    after_fingerprint: FingerprintResult,
    direct_evidence: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    result = _validate_continue_result(continue_result)
    evidence = copy.deepcopy(dict(direct_evidence))
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        record = mutation.record
        entry = record["generations"].get(str(generation))
        if record["state"]["phase"] != "step_verifying" or entry is None:
            raise StateConflict("goal verification requires step_verifying")
        require_active_lease(record, generation=generation, holder_token=claim_token)
        if entry["invocation_state"] != "returned" or entry["lease_token"] != claim_token:
            raise StateConflict("verification lacks the returned matching invocation")
        if result != entry.get("pending_step_result", {}).get("continue_result"):
            raise StateConflict("continue result differs from the directly recorded return")
        if result["repository_fingerprint_before"] != entry["before_fingerprint"]:
            raise StateConflict("continue result before fingerprint disagrees with generation state")
        if result["repository_fingerprint_after"] != after_fingerprint.fingerprint:
            raise StateConflict("continue result after fingerprint disagrees with direct fingerprint")
        evaluation = evaluate_goal(record, direct_evidence=evidence)
        apply_fingerprint(mutation, generation=generation, result=after_fingerprint)
        agent_job_id = result["job_id"] if result["agent_jobs_executed"] == 1 else None
        zero_job_reason = None
        if agent_job_id is None:
            zero_job_reason = str(
                evidence.get("zero_job_reason")
                or result.get("reason_code")
                or "continue returned without an AgentJob"
            )
        receipt_evidence = {
            "revision_before": evidence.get(
                "revision_before", record["repository_binding"]["starting_revision"]
            ),
            "revision_after": evidence.get(
                "revision_after", record["repository_binding"]["starting_revision"]
            ),
            "fingerprint_after": after_fingerprint.fingerprint,
            "agent_job_id": agent_job_id,
            "zero_job_reason": zero_job_reason,
            "task_id": result["task_id"],
            "decision_id": result["decision_id"],
            "completion_id": result["completion_id"],
            "handoff_id": result["handoff_id"],
            "changed_paths": copy.deepcopy(evidence.get("changed_paths", [])),
            "changed_path_source_ref": evidence.get(
                "changed_path_source_ref"
            ),
            "output_refs": copy.deepcopy(evidence.get("output_refs", [])),
            "checkpoint": copy.deepcopy(evidence["checkpoint"]),
            "validator_results": copy.deepcopy(evidence.get("validator_results", [])),
            "completion_contract_results": copy.deepcopy(
                evidence["completion_contract_results"]
            ),
            "goal_evaluation": evaluation,
            "progress_summary": str(evidence.get("progress_summary") or "Canonical state was verified."),
            "remaining_work": str(evidence.get("remaining_work") or "Reevaluate the durable goal."),
            "extensions": copy.deepcopy(evidence.get("extensions", {})),
        }
        entry["pending_step_result"] = {
            "continue_result": result,
            "completion_contract_results": copy.deepcopy(evidence["completion_contract_results"]),
            "receipt_evidence": receipt_evidence,
            "goal_evaluation": evaluation,
            "fingerprint_status": after_fingerprint.classification,
            "resolution_disposition": copy.deepcopy(
                result.get("resolution_disposition")
            ),
        }
        if (
            record.get("schema_version") == GOAL_SCHEMA_VERSION
            and result.get("resolution_disposition") is not None
        ):
            entry["resolution_disposition"] = copy.deepcopy(
                result["resolution_disposition"]
            )
            entry["repair_strategy_id"] = result["resolution_disposition"].get(
                "selected_strategy_id"
            )
            entry["strategy_attempt"] = int(
                result["resolution_disposition"].get("strategy_attempt", 0)
            )
        if (
            record.get("schema_version") == GOAL_SCHEMA_VERSION
            and "material_progress_dimensions" in evidence
        ):
            entry["material_progress_dimensions"] = list(
                evidence["material_progress_dimensions"]
            )
        entry["phase"] = "step_verified"
        record["state"]["phase"] = "step_verified"
        record["state"]["goal_evaluation"] = evaluation
        mutation.event(
            "step_verified",
            {
                "generation": generation,
                "goal_evaluation": evaluation,
                "fingerprint": after_fingerprint.fingerprint,
                "fingerprint_status": after_fingerprint.classification,
            },
        )
    return store.load_goal(goal_id)


def finalize_verified_receipt(
    mutation: Any,
    *,
    generation: int,
    decision: str,
    successor_thread_id: str | None = None,
) -> dict[str, Any]:
    entry = mutation.record["generations"].get(str(generation))
    pending = entry.get("pending_step_result") if entry else None
    if not isinstance(pending, Mapping) or not isinstance(pending.get("receipt_evidence"), Mapping):
        raise StateConflict("generation has no verified pending receipt")
    return finalize_receipt(
        mutation,
        generation=generation,
        invocation_count=1,
        decision=decision,
        evidence=pending["receipt_evidence"],
        successor_thread_id=successor_thread_id,
    )
