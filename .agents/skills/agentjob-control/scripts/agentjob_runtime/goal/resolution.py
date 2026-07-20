"""Strategy-aware resolution classification and human-necessity proof."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.model import utc_now
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.validation.schema import format_issues, validate_instance


STRATEGIES: dict[str, tuple[str, ...]] = {
    "validation": (
        "repair-validation-defect",
        "repair-underlying-work",
        "rerun-original-validator",
    ),
    "checkpoint": (
        "repair-checkpoint-input",
        "repair-underlying-work",
        "rerun-original-checkpoint",
    ),
    "control": (
        "repair-control-index-drift",
        "normalize-control-packet",
        "regenerate-canonical-derivative",
    ),
    "bootstrap": (
        "inspect-bound-goal-runtime",
        "inspect-configured-adapters",
        "run-capability-doctor",
    ),
    "capability": (
        "run-capability-doctor",
        "run-configured-capability-repair",
        "use-declared-provider-fallback",
    ),
    "no_action": (
        "reevaluate-goal-criteria",
        "select-earliest-legal-task",
        "materialize-bounded-task",
    ),
    "indeterminate": (
        "gather-missing-canonical-evidence",
        "rerun-declared-evaluator",
        "run-independent-validation",
    ),
    "dirty_state": (
        "classify-dirty-state-ownership",
        "route-nonoverlapping-work",
        "gather-ownership-evidence",
    ),
    "repository": (
        "reread-bound-repository-identity",
        "reattach-bound-checkout",
        "revalidate-repository-binding",
    ),
    "repeated_state": (
        "reorient-control-evidence",
        "reorient-task-route",
        "reorient-provider-state",
    ),
    "provider": (
        "query-provider-idempotency-key",
        "adopt-unique-provider-result",
        "reconcile-reserved-successor",
    ),
    "stale_revision": (
        "reread-canonical-revision",
        "resume-existing-unclaimed-worker",
    ),
}


def _schema(name: str) -> Path:
    return Path(__file__).resolve().parents[3] / "schemas" / name


def validate_disposition(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    issues = validate_instance(result, _schema("resolution-disposition.schema.json"))
    if issues:
        raise RecordValidationError(
            "resolution disposition failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    return result


def _family(reason_code: str, status: str | None) -> str:
    joined = f"{status or ''} {reason_code}".lower()
    if "checkpoint" in joined:
        return "checkpoint"
    if "validation" in joined or "validator" in joined:
        return "validation"
    if "control" in joined or "index" in joined or "derivative" in joined:
        return "control"
    if "bootstrap" in joined:
        return "bootstrap"
    if "capability" in joined or "provider_unavailable" in joined:
        return "capability"
    if "no_action" in joined or "no.action" in joined:
        return "no_action"
    if "indeterminate" in joined or "evidence" in joined:
        return "indeterminate"
    if "dirty" in joined:
        return "dirty_state"
    if "repository" in joined or "worktree" in joined or "binding" in joined:
        return "repository"
    if "repeat" in joined or "no_progress" in joined:
        return "repeated_state"
    if "provider" in joined or "dispatch" in joined or "handoff" in joined:
        return "provider"
    if "stale" in joined or "revision" in joined:
        return "stale_revision"
    return "no_action"


def _attempted(
    history: Sequence[Mapping[str, Any]], blocker_signature: str
) -> set[str]:
    return {
        str(item["selected_strategy_id"])
        for item in history
        if item.get("blocker_signature") == blocker_signature
        and item.get("selected_strategy_id")
    }


def _candidate_strategies(
    family: str,
    reason_code: str,
) -> list[str]:
    candidates = list(STRATEGIES[family])
    normalized = reason_code.lower()
    preferred = (
        "regenerate-canonical-derivative"
        if family == "control" and "derivative" in normalized
        else "normalize-control-packet"
        if family == "control"
        and any(token in normalized for token in ("packet", "incomplete", "stale"))
        else None
    )
    if preferred is not None:
        candidates.remove(preferred)
        candidates.insert(0, preferred)
    return candidates


def classify_resolution(
    *,
    reason_code: str,
    status: str | None = None,
    evidence: Mapping[str, Any] | None = None,
    history: Sequence[Mapping[str, Any]] = (),
    authority_refs: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
    legal_route_available: bool = True,
    explicit_human_gate: bool = False,
    protected_topology_action: bool = False,
    policy_limit: bool = False,
    integrity_incident: bool = False,
    cancelled: bool = False,
    goal_reached: bool = False,
) -> dict[str, Any]:
    """Return one validated disposition; machine routes are preferred by default."""

    if not reason_code:
        raise RecordValidationError("resolution requires a stable reason code")
    supplied_evidence = copy.deepcopy(dict(evidence or {}))
    blocker_signature = content_sha256(
        {"reason_code": reason_code, "status": status, "evidence": supplied_evidence}
    )
    common = {
        "schema_version": "sys4ai.resolution-disposition.v1",
        "reason_code": reason_code,
        "blocker_signature": blocker_signature,
        "authority_refs": list(authority_refs),
        "evidence_refs": list(evidence_refs),
    }
    if goal_reached:
        return validate_disposition(
            {
                **common,
                "classification": "goal_reached",
                "machine_resolvable": False,
                "resolution_type": "none",
                "candidate_strategy_ids": [],
                "selected_strategy_id": None,
                "strategy_attempt": 0,
                "requires_successor": False,
                "requires_human": False,
                "human_reason": None,
            }
        )
    if cancelled:
        classification, resolution_type, human_reason = (
            "cancelled",
            "cancellation",
            "The user explicitly cancelled the goal.",
        )
    elif integrity_incident:
        classification, resolution_type, human_reason = (
            "integrity_incident_requires_owner",
            "integrity_incident",
            "Canonical integrity or successor uniqueness requires owner authority.",
        )
    elif policy_limit:
        classification, resolution_type, human_reason = (
            "policy_limit_requires_user",
            "policy_limit",
            "Only the user may extend or cancel the accepted finite policy limit.",
        )
    elif explicit_human_gate or protected_topology_action:
        classification, resolution_type, human_reason = (
            "human_authority_required",
            "human_decision",
            "The requested action is explicitly human-owned by active policy.",
        )
    else:
        classification = resolution_type = human_reason = ""
    if classification:
        return validate_disposition(
            {
                **common,
                "classification": classification,
                "machine_resolvable": False,
                "resolution_type": resolution_type,
                "candidate_strategy_ids": [],
                "selected_strategy_id": None,
                "strategy_attempt": 0,
                "requires_successor": False,
                "requires_human": True,
                "human_reason": human_reason,
            }
        )

    family = _family(reason_code, status)
    candidates = [
        *_candidate_strategies(family, reason_code),
        "reorient-after-two-failures",
    ]
    attempted = _attempted(history, blocker_signature)
    selected = (
        "reorient-after-two-failures"
        if len(attempted) >= 2
        and "reorient-after-two-failures" not in attempted
        else next(
            (
                item
                for item in candidates
                if item not in attempted
                and item != "reorient-after-two-failures"
            ),
            None,
        )
    )
    if selected is None or not legal_route_available:
        return validate_disposition(
            {
                **common,
                "classification": "human_choice_required",
                "machine_resolvable": False,
                "resolution_type": "human_decision",
                "candidate_strategy_ids": candidates,
                "selected_strategy_id": None,
                "strategy_attempt": 0,
                "requires_successor": False,
                "requires_human": True,
                "human_reason": (
                    "No distinct lawful automated strategy remains."
                    if selected is None
                    else "The candidate strategy is outside the active goal authority."
                ),
            }
        )
    classification = {
        "control": "machine_control_repair",
        "bootstrap": "machine_control_repair",
        "provider": "machine_provider_recovery",
        "stale_revision": "refresh_and_retry_same_identity",
        "indeterminate": "machine_evidence_gathering",
    }.get(family, "machine_project_repair")
    resolution_type = {
        "machine_control_repair": "control_repair",
        "machine_provider_recovery": "provider_recovery",
        "refresh_and_retry_same_identity": "identity_refresh",
        "machine_evidence_gathering": "evidence_gathering",
    }.get(classification, "project_repair")
    return validate_disposition(
        {
            **common,
            "classification": classification,
            "machine_resolvable": True,
            "resolution_type": resolution_type,
            "candidate_strategy_ids": candidates,
            "selected_strategy_id": selected,
            "strategy_attempt": len(attempted) + 1,
            "requires_successor": True,
            "requires_human": False,
            "human_reason": None,
        }
    )


def normal_continuation_disposition(
    *,
    reason_code: str,
    evidence: Mapping[str, Any] | None = None,
    authority_refs: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
) -> dict[str, Any]:
    blocker_signature = content_sha256(
        {
            "reason_code": reason_code,
            "evidence": copy.deepcopy(dict(evidence or {})),
        }
    )
    return validate_disposition(
        {
            "schema_version": "sys4ai.resolution-disposition.v1",
            "classification": "normal_continuation",
            "reason_code": reason_code,
            "blocker_signature": blocker_signature,
            "machine_resolvable": True,
            "resolution_type": "continue",
            "candidate_strategy_ids": ["reevaluate-goal-after-bounded-job"],
            "selected_strategy_id": "reevaluate-goal-after-bounded-job",
            "strategy_attempt": 1,
            "authority_refs": list(authority_refs),
            "evidence_refs": list(evidence_refs),
            "requires_successor": True,
            "requires_human": False,
            "human_reason": None,
        }
    )


def material_progress_dimensions(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> list[str]:
    dimensions = {
        "repository_fingerprint": ("repository_fingerprint",),
        "control_store_revision": ("control_revision",),
        "task_lifecycle": ("task_id", "decision_id", "job_id"),
        "canonical_evidence": ("evidence_refs",),
        "blocker_resolution": ("resolved_blocker_codes",),
        "validator_checkpoint": ("validator_status", "checkpoint_status"),
        "provider_reconciliation": ("provider_state",),
        "completion_criteria": ("completion_status",),
        "strategy": ("selected_strategy_id",),
    }
    return [
        name
        for name, keys in dimensions.items()
        if any(before.get(key) != after.get(key) for key in keys)
    ]


def append_resolution(
    record: dict[str, Any],
    *,
    generation: int,
    disposition: Mapping[str, Any],
    progress_dimensions: Sequence[str] = (),
) -> None:
    value = validate_disposition(disposition)
    entry = record["generations"].get(str(generation))
    if entry is None:
        raise StateConflict("resolution generation does not exist")
    record.setdefault("resolution_history", []).append(copy.deepcopy(value))
    entry["resolution_disposition"] = copy.deepcopy(value)
    entry["repair_strategy_id"] = value["selected_strategy_id"]
    entry["strategy_attempt"] = value["strategy_attempt"]
    entry["material_progress_dimensions"] = list(progress_dimensions)


def build_human_necessity_report(
    *,
    goal_id: str,
    generation: int,
    disposition: Mapping[str, Any],
    history: Sequence[Mapping[str, Any]],
    required_human_authority_or_decision: str,
    smallest_requested_user_action: str,
    resume_contract: str,
    policy_authority_refs: Sequence[str],
    evidence_refs: Sequence[str],
    why_no_machine_route_remains: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    value = validate_disposition(disposition)
    if value["requires_human"] is not True:
        raise StateConflict("human-necessity proof requires a human disposition")
    attempted = [
        {
            "strategy_id": str(item["selected_strategy_id"]),
            "outcome": "exhausted",
            "evidence_refs": list(item.get("evidence_refs", [])),
        }
        for item in history
        if item.get("selected_strategy_id")
        and item.get("blocker_signature") == value["blocker_signature"]
    ]
    report = {
        "schema_version": "sys4ai.human-necessity-report.v1",
        "report_id": f"HNR-{goal_id}-{generation}",
        "goal_id": goal_id,
        "generation": generation,
        "human_intervention_required": True,
        "reason_code": value["reason_code"],
        "required_human_authority_or_decision": required_human_authority_or_decision,
        "automated_strategies_attempted": attempted,
        "remaining_machine_routes": [],
        "why_no_machine_route_remains": why_no_machine_route_remains
        or str(value["human_reason"]),
        "smallest_requested_user_action": smallest_requested_user_action,
        "resume_contract": resume_contract,
        "policy_authority_refs": list(policy_authority_refs),
        "evidence_refs": list(evidence_refs),
        "created_at": timestamp or utc_now(),
        "finalized": True,
    }
    issues = validate_instance(report, _schema("human-necessity-report.schema.json"))
    if issues:
        raise RecordValidationError(
            "human-necessity report failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    if not attempted and not policy_authority_refs:
        raise RecordValidationError(
            "an inherent human gate requires the policy declaring it human-owned"
        )
    return report
