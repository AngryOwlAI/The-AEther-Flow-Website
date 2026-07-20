"""Immutable completion, optional handoff, and continue-result finalization."""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.control.completion import CompletionWriteReceipt, write_completion
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.handoff import HandoffWriteReceipt, write_handoff
from agentjob_runtime.control.indexes import generate_indexes
from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.execution.compiler import CompiledAuthority
from agentjob_runtime.execution.executor import ExecutionEvidence, capture_file_state
from agentjob_runtime.execution.validation import PostExecutionReport
from agentjob_runtime.goal.model import utc_now
from agentjob_runtime.goal.resolution import (
    classify_resolution,
    normal_continuation_disposition,
)
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.validation.schema import format_issues, validate_instance


@dataclass(frozen=True)
class HandoffPlan:
    summary: str
    completed: tuple[str, ...]
    remaining: tuple[str, ...]
    next_objective: str
    recommended_role: str
    route_label: str
    constraints_to_preserve: tuple[str, ...]
    predecessor_handoff_ids: tuple[str, ...] = ()
    human_gates: tuple[Mapping[str, Any], ...] = ()
    handoff_id: str | None = None


@dataclass(frozen=True)
class ContinueFinalization:
    result: Mapping[str, Any]
    completion: Mapping[str, Any] | None
    completion_sha256: str | None
    completion_receipt: Mapping[str, Any] | None
    handoff: Mapping[str, Any] | None
    handoff_sha256: str | None
    handoff_receipt: Mapping[str, Any] | None
    indexes_status: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_result(result: Mapping[str, Any]) -> None:
    schema_name = (
        "continue-result-v2.schema.json"
        if result.get("schema_version") == "sys4ai.continue-result.v2"
        else "continue-result.schema.json"
    )
    schema = Path(__file__).resolve().parents[3] / "schemas" / schema_name
    issues = validate_instance(result, schema)
    if issues:
        raise RecordValidationError(
            "continue result failed schema validation",
            details={
                "reason_code": "continue.result_invalid",
                "findings": format_issues(issues).splitlines(),
            },
        )


def _validator_counts(
    authority: CompiledAuthority, report: PostExecutionReport
) -> dict[str, int]:
    required_ids = {str(item["validator_id"]) for item in authority.required_validators}
    declared_ids = required_ids | {
        str(item["validator_id"]) for item in authority.contextual_validators
    }
    required_ids.update(
        {
            "changed-path-allowlist",
            "command-evidence-validator",
            "claim-boundary-linter",
        }
        - declared_ids
    )
    statuses = [str(item["status"]) for item in report.validator_results]
    return {
        "required": len(required_ids),
        "passed": statuses.count("pass"),
        "failed": statuses.count("fail") + statuses.count("indeterminate"),
        "warning": statuses.count("warning"),
        "skipped": statuses.count("skipped"),
    }


def _build_completion(
    *,
    authority: CompiledAuthority,
    evidence: ExecutionEvidence,
    report: PostExecutionReport,
    started_at: str,
    completed_at: str,
    before_revision: str | None,
    after_revision: str | None,
    next_recommended_action: str | None,
) -> dict[str, Any]:
    domain_warning = report.status == "domain_indeterminate"
    failed = report.status in {"validation_failed", "checkpoint_failed"}
    return {
        "schema_version": "sys4ai.completion.v1",
        "completion_id": f"AJC-{authority.job_id}",
        "job_id": authority.job_id,
        "task_id": authority.task_id,
        "decision_id": authority.decision_id,
        "started_at": started_at,
        "completed_at": completed_at,
        "status": "failed" if failed else "completed_with_warnings" if domain_warning else "completed",
        "before": {
            "repository_fingerprint": evidence.before_fingerprint,
            "revision": before_revision,
        },
        "after": {
            "repository_fingerprint": evidence.after_fingerprint,
            "revision": after_revision,
        },
        "changed_paths": list(evidence.changed_paths),
        "outputs": [copy.deepcopy(dict(item)) for item in report.outputs],
        "command_results": [copy.deepcopy(dict(item)) for item in report.command_results],
        "validator_results": [copy.deepcopy(dict(item)) for item in report.validator_results],
        "verdict": "failed_within_claim_boundary" if failed else "completed_within_claim_boundary",
        "uncertainty": {
            "status": "material" if failed else "bounded" if domain_warning else "none_observed",
            "notes": [
                "Domain truth remains indeterminate despite completed process validation."
            ]
            if domain_warning
            else ["Required post-execution validation or checkpoint evidence did not pass."]
            if failed
            else [],
        },
        "claim_summary": {
            "allowed_conclusions": [] if failed else list(report.proposed_claims),
            "forbidden_overread": list(authority.claim_boundary["forbidden"]),
            "inherited_boundary_ref": authority.job_id,
        },
        "next_recommended_action": next_recommended_action,
        "extensions": {},
    }


def _build_handoff(
    *,
    plan: HandoffPlan,
    authority: CompiledAuthority,
    completion_id: str,
    timestamp: str,
) -> dict[str, Any]:
    if not plan.summary.strip() or not plan.next_objective.strip():
        raise RecordValidationError("handoff summary and next objective must be non-empty")
    if not plan.constraints_to_preserve:
        raise RecordValidationError("handoff must preserve at least one constraint")
    return {
        "schema_version": "sys4ai.handoff.v1",
        "handoff_id": plan.handoff_id or f"HANDOFF-{completion_id}",
        "predecessor": {
            "task_id": authority.task_id,
            "decision_id": authority.decision_id,
            "job_id": authority.job_id,
            "completion_id": completion_id,
        },
        "predecessor_handoff_ids": list(plan.predecessor_handoff_ids),
        "summary": plan.summary,
        "progress": {
            "completed": list(plan.completed),
            "remaining": list(plan.remaining),
        },
        "next_action": {
            "objective": plan.next_objective,
            "recommended_role": plan.recommended_role,
            "route_label": plan.route_label,
        },
        "constraints_to_preserve": list(plan.constraints_to_preserve),
        "human_gates": [copy.deepcopy(dict(item)) for item in plan.human_gates],
        "grants_execution_authority": False,
        "created_at": timestamp,
        "extensions": {},
    }


def finalize_no_action(
    *,
    boundary_entered: str,
    reason_code: str,
    repository_fingerprint: str,
    status: str | None = None,
    task_id: str | None = None,
    decision_id: str | None = None,
    job_id: str | None = None,
    next_recommended_action: str | None = None,
    resolution_history: Sequence[Mapping[str, Any]] = (),
    authority_refs: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
) -> ContinueFinalization:
    """Return a validated read-only result without creating control evidence."""

    mapped_status = status or {
        "bootstrap_required": "bootstrap_required",
        "human_gate_required": "human_gate_required",
        "no_action": "no_action",
        "blocked": "blocked",
        "control_repair_required": "control_repair_required",
        "director_decision_required": "blocked",
        "existing_agent_job_ready": "blocked",
    }.get(boundary_entered, "unknown")
    disposition = classify_resolution(
        reason_code=reason_code,
        status=mapped_status,
        evidence={
            "boundary_entered": boundary_entered,
            "task_id": task_id,
            "decision_id": decision_id,
            "job_id": job_id,
        },
        history=resolution_history,
        authority_refs=authority_refs,
        evidence_refs=evidence_refs,
        explicit_human_gate=mapped_status == "human_gate_required",
        policy_limit=mapped_status == "policy_limit_reached",
        integrity_incident=mapped_status == "integrity_incident",
    )
    routed_status = mapped_status
    if disposition["machine_resolvable"]:
        routed_status = {
            "provider_recovery": "recovery_routed",
            "evidence_gathering": "evidence_gathering_routed",
        }.get(disposition["resolution_type"], "repair_routed")
    repair_route = (
        {
            "strategy_id": disposition["selected_strategy_id"],
            "authority_refs": list(disposition["authority_refs"]),
            "requires_agentjob": disposition["resolution_type"]
            in {"project_repair", "control_repair"},
            "execute_in_successor": False,
        }
        if disposition["machine_resolvable"]
        else None
    )
    result = {
        "schema_version": "sys4ai.continue-result.v2",
        "status": routed_status,
        "boundary_entered": boundary_entered,
        "agent_jobs_executed": 0,
        "task_id": task_id,
        "decision_id": decision_id,
        "job_id": job_id,
        "completion_id": None,
        "handoff_id": None,
        "progress_effect": "none",
        "global_goal_evaluation": "not_evaluated_here",
        "repository_fingerprint_before": repository_fingerprint,
        "repository_fingerprint_after": repository_fingerprint,
        "validators": {
            "required": 0,
            "passed": 0,
            "failed": 0,
            "warning": 0,
            "skipped": 0,
        },
        "next_recommended_action": next_recommended_action,
        "execution_performed": False,
        "reason_code": reason_code,
        "resolution_disposition": disposition,
        "repair_route": repair_route,
        "extensions": {},
    }
    _validate_result(result)
    return ContinueFinalization(result, None, None, None, None, None, None, "not_run")


def finalize_execution(
    *,
    store: FilesystemControlStore,
    boundary_entered: str,
    authority: CompiledAuthority,
    evidence: ExecutionEvidence,
    validation: PostExecutionReport,
    expected_revision: int,
    started_at: str,
    completed_at: str | None = None,
    before_revision: str | None = None,
    after_revision: str | None = None,
    close_task: bool = False,
    handoff_plan: HandoffPlan | None = None,
    next_recommended_action: str | None = "Reevaluate the containing goal.",
    policies: Sequence[Mapping[str, Any]] = (),
) -> ContinueFinalization:
    """Finalize exactly one successfully validated execution transaction."""

    if validation.job_id != authority.job_id or evidence.job_id != authority.job_id:
        raise StateConflict("finalization evidence does not bind the compiled AgentJob")
    allowed_statuses = {
        "passed",
        "domain_indeterminate",
        "validation_failed",
        "checkpoint_failed",
    }
    if validation.status not in allowed_statuses:
        raise StateConflict("unsupported post-execution finalization status")
    failed = validation.status in {"validation_failed", "checkpoint_failed"}
    if failed and (close_task or handoff_plan is not None):
        raise StateConflict("failed validation cannot close a task or authorize a handoff")
    if close_task and handoff_plan is not None:
        raise StateConflict("a closed task cannot simultaneously require a successor handoff")
    timestamp = completed_at or utc_now()
    completion = _build_completion(
        authority=authority,
        evidence=evidence,
        report=validation,
        started_at=started_at,
        completed_at=timestamp,
        before_revision=before_revision,
        after_revision=after_revision,
        next_recommended_action=next_recommended_action,
    )
    completion_receipt: CompletionWriteReceipt = write_completion(
        store,
        completion,
        expected_revision=expected_revision,
        close_task=close_task,
        next_recommended_action=next_recommended_action,
        policies=policies,
    )
    handoff = None
    handoff_receipt: HandoffWriteReceipt | None = None
    if handoff_plan is not None:
        handoff = _build_handoff(
            plan=handoff_plan,
            authority=authority,
            completion_id=str(completion["completion_id"]),
            timestamp=timestamp,
        )
        handoff_receipt = write_handoff(
            store,
            handoff,
            expected_revision=completion_receipt.task_revision,
            policies=policies,
        )
    index_receipt = generate_indexes(store)
    _, final_fingerprint = capture_file_state(authority.project_root)
    progress_effect = (
        "blocked_evidence"
        if failed
        else str(authority.completion_contract["goal_effect"]["type"])
    )
    if failed:
        disposition = classify_resolution(
            reason_code=str(validation.reason_code or "continue.validation_failed"),
            status="failed",
            evidence={
                "job_id": authority.job_id,
                "validation_status": validation.status,
            },
            authority_refs=[authority.job_id],
            evidence_refs=[
                f"completion:{completion['completion_id']}"
            ],
        )
    elif validation.status == "domain_indeterminate":
        disposition = classify_resolution(
            reason_code="continue.domain_indeterminate",
            status="completed_with_warnings",
            evidence={"completion_id": completion["completion_id"]},
            authority_refs=[authority.job_id],
            evidence_refs=[
                f"completion:{completion['completion_id']}"
            ],
        )
    else:
        disposition = normal_continuation_disposition(
            reason_code="continue.one_job_completed",
            evidence={"completion_id": completion["completion_id"]},
            authority_refs=[authority.job_id],
            evidence_refs=[
                f"completion:{completion['completion_id']}"
            ],
        )
    result = {
        "schema_version": "sys4ai.continue-result.v2",
        "status": "repair_routed"
        if failed
        else "evidence_gathering_routed"
        if validation.status == "domain_indeterminate"
        else "completed",
        "boundary_entered": boundary_entered,
        "agent_jobs_executed": 1,
        "task_id": authority.task_id,
        "decision_id": authority.decision_id,
        "job_id": authority.job_id,
        "completion_id": completion["completion_id"],
        "handoff_id": handoff["handoff_id"] if handoff else None,
        "progress_effect": progress_effect,
        "global_goal_evaluation": "indeterminate"
        if validation.status == "domain_indeterminate"
        else "not_evaluated_here",
        "repository_fingerprint_before": evidence.before_fingerprint,
        "repository_fingerprint_after": final_fingerprint,
        "validators": _validator_counts(authority, validation),
        "next_recommended_action": next_recommended_action,
        "execution_performed": True,
        "reason_code": validation.reason_code
        if failed
        else "continue.domain_indeterminate"
        if validation.status == "domain_indeterminate"
        else "continue.one_job_completed",
        "resolution_disposition": disposition,
        "repair_route": (
            {
                "strategy_id": disposition["selected_strategy_id"],
                "authority_refs": list(disposition["authority_refs"]),
                "requires_agentjob": True,
                "execute_in_successor": True,
            }
            if failed
            else {
                "strategy_id": disposition["selected_strategy_id"],
                "authority_refs": list(disposition["authority_refs"]),
                "requires_agentjob": False,
                "execute_in_successor": True,
            }
            if validation.status == "domain_indeterminate"
            else None
        ),
        "extensions": {},
    }
    _validate_result(result)
    completion_hash = content_sha256(completion)
    if completion_hash != completion_receipt.sha256:
        raise StateConflict("canonical completion hash differs from write receipt")
    handoff_hash = content_sha256(handoff) if handoff is not None else None
    if handoff_receipt is not None and handoff_hash != handoff_receipt.sha256:
        raise StateConflict("canonical handoff hash differs from write receipt")
    return ContinueFinalization(
        result,
        completion,
        completion_hash,
        completion_receipt.as_dict(),
        handoff,
        handoff_hash,
        handoff_receipt.as_dict() if handoff_receipt else None,
        index_receipt.status,
    )
