"""Canonical generation receipt construction and one-time finalization."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.model import GOAL_SCHEMA_VERSION
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.validation.schema import format_issues, validate_instance


def finalize_receipt(
    mutation: Any,
    *,
    generation: int,
    invocation_count: int | str,
    decision: str,
    evidence: Mapping[str, Any],
    successor_thread_id: str | None = None,
) -> dict[str, Any]:
    """Validate and append the only finalized receipt for a generation."""

    record = mutation.record
    entry = record["generations"].get(str(generation))
    if entry is None:
        raise StateConflict("receipt generation does not exist")
    if entry.get("finalized_receipt_hash") is not None:
        raise StateConflict("generation receipt is already finalized")
    if invocation_count not in {0, 1, "unknown"}:
        raise RecordValidationError("invalid continue invocation count")
    expected_count = (
        1
        if entry["invocation_state"] == "returned"
        else "unknown"
        if entry["invocation_state"] == "unknown"
        else 0
    )
    if invocation_count != expected_count:
        raise StateConflict("receipt invocation count disagrees with generation invocation state")
    supplied = copy.deepcopy(dict(evidence))
    prior_hash = record["journal"][-1]["entry_hash"] if record["journal"] else None
    v3 = record.get("schema_version") == GOAL_SCHEMA_VERSION
    receipt: dict[str, Any] = {
        "schema_version": (
            "sys4ai.goal-step-receipt.v2"
            if v3
            else "sys4ai.goal-step-receipt.v1"
        ),
        "receipt_id": f"GSR-{record['goal_id']}-{generation}",
        "goal_id": record["goal_id"],
        "generation": generation,
        "handoff_token_hash": hashlib.sha256(entry["handoff_token"].encode("utf-8")).hexdigest(),
        "idempotency_key": entry["idempotency_key"],
        "predecessor_thread_id": supplied.pop(
            "predecessor_thread_id", record["handoff"].get("predecessor_thread_id")
        ),
        "successor_thread_id": successor_thread_id,
        "started_at": supplied.pop("started_at", entry.get("claimed_at") or mutation.timestamp),
        "finished_at": mutation.timestamp,
        "repository_binding": copy.deepcopy(record["repository_binding"]),
        "revision_before": supplied.pop(
            "revision_before", record["repository_binding"]["starting_revision"]
        ),
        "revision_after": supplied.pop(
            "revision_after", record["repository_binding"]["starting_revision"]
        ),
        "fingerprint_before": entry["before_fingerprint"],
        "fingerprint_after": supplied.pop(
            "fingerprint_after", entry.get("after_fingerprint") or entry["before_fingerprint"]
        ),
        "continue_invocation_count": invocation_count,
        "agent_job_id": supplied.pop("agent_job_id", None),
        "zero_job_reason": supplied.pop("zero_job_reason", None),
        "task_id": supplied.pop("task_id", None),
        "handoff_id": supplied.pop("handoff_id", None),
        "checkpoint": supplied.pop(
            "checkpoint",
            {"provider": "none", "status": "not_required", "revision": None, "evidence_ref": None},
        ),
        "validator_results": supplied.pop("validator_results", []),
        "goal_evaluation": supplied.pop("goal_evaluation", record["state"]["goal_evaluation"]),
        "progress_summary": supplied.pop("progress_summary", "Generation finalized."),
        "remaining_work": supplied.pop("remaining_work", "Reevaluate the durable goal."),
        "decision": decision,
        "journal_entry_hash": "0" * 64,
        "prior_journal_hash": prior_hash,
        "finalized": True,
        "extensions": supplied.pop("extensions", {}),
    }
    if v3:
        completion_results = supplied.pop(
            "completion_contract_results",
            [
                {
                    "criterion": criterion,
                    "status": "indeterminate",
                    "evidence_refs": [],
                }
                for criterion in record["completion_contract"][
                    "required_evidence"
                ]
            ],
        )
        mapped_decision = {
            "protected_stop": "human_intervention_required",
            "guard_stop": "policy_limit_reached",
            "failed": "integrity_incident",
        }.get(decision, decision)
        receipt.update(
            {
                "decision_id": supplied.pop("decision_id", None),
                "completion_id": supplied.pop("completion_id", None),
                "changed_paths": supplied.pop("changed_paths", []),
                "changed_path_source_ref": supplied.pop(
                    "changed_path_source_ref", None
                ),
                "output_refs": supplied.pop("output_refs", []),
                "completion_contract_results": completion_results,
                "decision": mapped_decision,
                "resolution_disposition": copy.deepcopy(
                    entry.get("resolution_disposition")
                ),
                "material_progress_dimensions": list(
                    entry.get("material_progress_dimensions", [])
                ),
                "requested_reasoning_effort": entry[
                    "requested_reasoning_effort"
                ],
                "effective_reasoning_effort": entry[
                    "effective_reasoning_effort"
                ]
                or entry["requested_reasoning_effort"],
                "skill_runtime_binding": copy.deepcopy(
                    record["runtime_binding"]
                ),
                "repository_topology_evidence": copy.deepcopy(
                    entry.get("observed_repository_topology") or {}
                ),
                "human_necessity_report_ref": entry.get(
                    "human_necessity_report_ref"
                ),
                "completion_report_ref": (
                    entry.get("completion_report_ref")
                    or (
                        f"GCR-{record['goal_id']}"
                        if mapped_decision == "terminal_complete"
                        else None
                    )
                ),
            }
        )
    if supplied:
        raise RecordValidationError(
            "unknown receipt evidence fields",
            details={"fields": sorted(supplied)},
        )
    receipt["journal_entry_hash"] = content_sha256(receipt)
    schema = (
        Path(__file__).resolve().parents[3]
        / "schemas"
        / (
            "goal-step-receipt-v2.schema.json"
            if v3
            else "goal-step-receipt.schema.json"
        )
    )
    issues = validate_instance(receipt, schema)
    if issues:
        raise RecordValidationError(
            "goal receipt failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    receipt_hash = mutation.receipt(receipt)
    entry["finalized_receipt_hash"] = receipt_hash
    entry["pending_step_result"] = None
    entry["terminal_or_successor_outcome"] = decision
    return receipt
