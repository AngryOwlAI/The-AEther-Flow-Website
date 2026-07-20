"""Plan-specific combined activation and accepted execution profiles."""

from __future__ import annotations

import copy
import hashlib
import re
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.execution.activation_profile import (
    DEFAULT_REASONING_EFFORT,
    DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
    canonical_text,
    profile_sha256,
    record_manual_current_thread_profile,
    render_combined_acceptance as _render_combined_acceptance,
    request_current_thread_profile,
    text_sha256,
    validate_effort,
    validate_evidence_ref,
    validate_repository_binding,
    validate_topology_policy,
)
from agentjob_runtime.goal.model import utc_now
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
PLAN_ACTIVATION_STATES = frozenset(
    {
        "draft",
        "current_thread_profile_requested",
        "current_thread_profile_verified",
        "presented",
        "revised_goal",
        "revised_effort",
        "revised_both",
        "accepted",
        "initialized",
    }
)
PLAN_BINDING_ENVIRONMENT_MODES = frozenset({"local", "worktree", "remote"})


def _schema(name: str) -> Path:
    return (
        Path(__file__).resolve().parents[4]
        / "implementation-plan-goal"
        / "schemas"
        / name
    )


def _require_sha256(value: str, *, field: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise RecordValidationError(f"{field} must be a lowercase SHA-256")
    return value


def _validate_id(value: str, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecordValidationError(f"{field} must be nonblank")
    if contains_secret(value):
        raise RecordValidationError(f"{field} appears to contain a secret")
    return value


def _validate_consistency_attestation(
    value: Mapping[str, Any],
    *,
    activation_goal_sha256: str,
    plan_objective_sha256: str,
    accepted_plan_sha256: str,
) -> dict[str, Any]:
    required = {
        "status",
        "scope_unchanged",
        "activation_goal_sha256",
        "plan_objective_sha256",
        "accepted_plan_sha256",
        "evidence_ref",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise RecordValidationError(
            "goal/plan consistency attestation has missing or unknown fields"
        )
    result = copy.deepcopy(dict(value))
    if result["status"] != "consistent" or result["scope_unchanged"] is not True:
        raise StateConflict(
            "activation goal conflicts with accepted plan scope",
            details={"reason_code": "plan_activation.scope_conflict"},
        )
    expected = {
        "activation_goal_sha256": activation_goal_sha256,
        "plan_objective_sha256": plan_objective_sha256,
        "accepted_plan_sha256": accepted_plan_sha256,
    }
    mismatches = {
        key: {"expected": expected_value, "actual": result.get(key)}
        for key, expected_value in expected.items()
        if result.get(key) != expected_value
    }
    if mismatches:
        raise StateConflict(
            "goal/plan consistency attestation is stale or mismatched",
            details={
                "reason_code": "plan_activation.consistency_evidence_mismatch",
                "mismatches": mismatches,
            },
        )
    validate_evidence_ref(
        result["evidence_ref"],
        field="goal/plan consistency evidence",
    )
    return result


def validate_goal_plan_consistency(
    *,
    goal_text: str,
    plan_objective: str,
    accepted_plan_sha256: str,
    consistency_attestation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Require exact objective equality or explicit hash-bound unchanged scope."""

    goal = canonical_text(goal_text, field="activation goal")
    objective = canonical_text(plan_objective, field="accepted plan objective")
    plan_hash = _require_sha256(
        accepted_plan_sha256,
        field="accepted_plan_sha256",
    )
    goal_hash = text_sha256(goal, field="activation goal")
    objective_hash = text_sha256(objective, field="accepted plan objective")
    if goal == objective:
        return {
            "status": "exact_objective_match",
            "scope_unchanged": True,
            "activation_goal_sha256": goal_hash,
            "plan_objective_sha256": objective_hash,
            "accepted_plan_sha256": plan_hash,
            "evidence_ref": None,
        }
    if consistency_attestation is None:
        raise StateConflict(
            "activation goal conflicts with or extends the accepted plan objective",
            details={
                "reason_code": "plan_activation.amendment_required",
                "activation_goal_sha256": goal_hash,
                "plan_objective_sha256": objective_hash,
            },
        )
    attestation = _validate_consistency_attestation(
        consistency_attestation,
        activation_goal_sha256=goal_hash,
        plan_objective_sha256=objective_hash,
        accepted_plan_sha256=plan_hash,
    )
    return {
        **attestation,
        "status": "attested_scope_unchanged",
    }


def create_activation_proposal(
    *,
    goal_text: str,
    plan_id: str,
    accepted_plan_sha256: str,
    plan_objective: str,
    repository_binding: Mapping[str, Any],
    current_thread_id: str,
    provider_id: str,
    model_id: str | None = None,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    selection_source: str = "default",
    repository_topology_policy: Mapping[str, Any] | None = None,
    consistency_attestation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a noncanonical in-memory proposal with zero plan effects."""

    exact_goal = canonical_text(goal_text, field="activation goal")
    objective = canonical_text(
        plan_objective,
        field="accepted plan objective",
    )
    selected_effort = validate_effort(reasoning_effort)
    if selection_source not in {"default", "user_override"}:
        raise RecordValidationError("invalid reasoning-effort selection source")
    if selection_source == "default" and selected_effort != DEFAULT_REASONING_EFFORT:
        raise RecordValidationError("default plan activation effort must be exactly max")
    binding = validate_repository_binding(
        repository_binding,
        allowed_environment_modes=PLAN_BINDING_ENVIRONMENT_MODES,
    )
    topology = validate_topology_policy(
        repository_topology_policy or DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
        require_default_deny=True,
    )
    plan_hash = _require_sha256(
        accepted_plan_sha256,
        field="accepted_plan_sha256",
    )
    consistency = validate_goal_plan_consistency(
        goal_text=exact_goal,
        plan_objective=objective,
        accepted_plan_sha256=plan_hash,
        consistency_attestation=consistency_attestation,
    )
    return {
        "state": "draft",
        "goal_text": exact_goal,
        "goal_sha256": text_sha256(exact_goal, field="activation goal"),
        "plan_id": _validate_id(plan_id, field="plan_id"),
        "accepted_plan_sha256": plan_hash,
        "plan_objective": objective,
        "plan_objective_sha256": text_sha256(
            objective,
            field="accepted plan objective",
        ),
        "goal_plan_consistency": consistency,
        "reasoning_effort": selected_effort,
        "selection_source": selection_source,
        "current_thread_id": _validate_id(
            current_thread_id,
            field="current_thread_id",
        ),
        "current_thread_requested_effort": None,
        "current_thread_effective_effort": None,
        "current_thread_verification_status": "not_requested",
        "current_thread_evidence_ref": None,
        "provider_id": _validate_id(provider_id, field="provider_id"),
        "model_id": (
            _validate_id(model_id, field="model_id")
            if model_id is not None
            else None
        ),
        "repository_binding": binding,
        "repository_binding_sha256": content_sha256(binding),
        "repository_topology_policy": topology,
        "repository_topology_policy_sha256": content_sha256(topology),
        "acceptance_invalidated": False,
        "presentation_sequence": 0,
    }


def revise_activation(
    proposal: Mapping[str, Any],
    *,
    goal_text: str | None = None,
    reasoning_effort: str | None = None,
    consistency_attestation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Invalidate presentation while retaining prior user effort overrides."""

    value = copy.deepcopy(dict(proposal))
    changed_goal = goal_text is not None
    changed_effort = reasoning_effort is not None
    if not changed_goal and not changed_effort:
        raise RecordValidationError("activation revision must change goal or effort")
    if goal_text is not None:
        value["goal_text"] = canonical_text(
            goal_text,
            field="revised activation goal",
        )
        value["goal_sha256"] = text_sha256(
            value["goal_text"],
            field="revised activation goal",
        )
        value["goal_plan_consistency"] = validate_goal_plan_consistency(
            goal_text=value["goal_text"],
            plan_objective=value["plan_objective"],
            accepted_plan_sha256=value["accepted_plan_sha256"],
            consistency_attestation=consistency_attestation,
        )
    if reasoning_effort is not None:
        value["reasoning_effort"] = validate_effort(
            reasoning_effort,
            field="revised reasoning_effort",
        )
        value["selection_source"] = "user_override"
        value["current_thread_requested_effort"] = None
        value["current_thread_effective_effort"] = None
        value["current_thread_verification_status"] = "not_requested"
        value["current_thread_evidence_ref"] = None
    value["state"] = (
        "revised_both"
        if changed_goal and changed_effort
        else "revised_goal"
        if changed_goal
        else "revised_effort"
    )
    value["acceptance_invalidated"] = True
    return value


def render_combined_acceptance(
    proposal: Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    value, text = _render_combined_acceptance(
        proposal,
        goal_heading="implementation-plan goal",
        relay_name="implementation-plan relay",
    )
    value["presentation_sequence"] = int(
        proposal.get("presentation_sequence", 0)
    ) + 1
    # The prior presentation remains invalid, while this newly rendered
    # presentation becomes the sole acceptance candidate.
    value["acceptance_invalidated"] = False
    return value, text


def _validate_activation_receipt_record(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    value = copy.deepcopy(dict(receipt))
    issues = validate_instance(
        value,
        _schema("plan-activation-receipt.schema.json"),
    )
    if issues:
        raise RecordValidationError(
            "plan activation receipt failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    expected_hash = profile_sha256(
        value,
        hash_field="receipt_content_sha256",
    )
    if value["receipt_content_sha256"] != expected_hash:
        raise RecordValidationError(
            "plan activation receipt content hash is invalid"
        )
    if value["reasoning_effort"] != value["current_thread_requested_effort"]:
        raise RecordValidationError(
            "accepted effort differs from the current-thread request"
        )
    if value["reasoning_effort"] != value["current_thread_effective_effort"]:
        raise RecordValidationError(
            "accepted effort was not verified on the current discussion"
        )
    return value


def accept_activation(
    proposal: Mapping[str, Any],
    *,
    acceptance_message: str,
    acceptance_evidence_ref: str,
    effective_from_generation: int = 1,
    timestamp: str | None = None,
    activation_id: str | None = None,
    superseded_activation_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    value = copy.deepcopy(dict(proposal))
    if value.get("state") != "presented":
        raise StateConflict(
            "combined acceptance requires the latest presented values"
        )
    if value.get("acceptance_invalidated") is True:
        raise StateConflict("stale combined acceptance cannot be reused")
    if value.get("current_thread_verification_status") != "verified":
        raise StateConflict(
            "combined acceptance requires verified current-thread effort"
        )
    if (
        value.get("current_thread_requested_effort")
        != value.get("reasoning_effort")
        or value.get("current_thread_effective_effort")
        != value.get("reasoning_effort")
    ):
        raise StateConflict(
            "combined acceptance profile differs from current-thread evidence"
        )
    exact_acceptance = canonical_text(
        acceptance_message,
        field="combined acceptance message",
    )
    evidence = validate_evidence_ref(
        acceptance_evidence_ref,
        field="combined acceptance evidence",
    )
    if not isinstance(effective_from_generation, int) or (
        effective_from_generation < 1
    ):
        raise RecordValidationError(
            "effective_from_generation must be a positive integer"
        )
    now = timestamp or utc_now()
    receipt_id = activation_id or (
        "PAR-"
        + hashlib.sha256(
            (
                value["plan_id"]
                + value["goal_sha256"]
                + str(value["presentation_sequence"])
                + now
            ).encode("utf-8")
        ).hexdigest()[:24]
    )
    receipt = {
        "schema_version": "sys4ai.plan-activation-receipt.v1",
        "activation_id": receipt_id,
        "status": "accepted",
        "combined_acceptance": True,
        "plan_id": value["plan_id"],
        "accepted_plan_sha256": value["accepted_plan_sha256"],
        "exact_activation_goal_sha256": value["goal_sha256"],
        "reasoning_effort": value["reasoning_effort"],
        "selection_source": value["selection_source"],
        "current_thread_id": value["current_thread_id"],
        "current_thread_requested_effort": value["reasoning_effort"],
        "current_thread_effective_effort": value[
            "current_thread_effective_effort"
        ],
        "current_thread_verification_status": "verified",
        "current_thread_evidence_ref": value["current_thread_evidence_ref"],
        "provider_id": value["provider_id"],
        "model_id": value["model_id"],
        "repository_identity_sha256": value["repository_binding_sha256"],
        "repository_topology_policy_sha256": value[
            "repository_topology_policy_sha256"
        ],
        "acceptance_message_sha256": hashlib.sha256(
            exact_acceptance.encode("utf-8")
        ).hexdigest(),
        "acceptance_evidence_ref": evidence,
        "effective_from_generation": effective_from_generation,
        "superseded_activation_id": superseded_activation_id,
        "accepted_at": now,
        "hash_basis": "canonical_json_without_receipt_content_sha256",
        "receipt_content_sha256": "",
        "finalized": True,
    }
    receipt["receipt_content_sha256"] = profile_sha256(
        receipt,
        hash_field="receipt_content_sha256",
    )
    validated = _validate_activation_receipt_record(receipt)
    value["state"] = "accepted"
    value["acceptance_invalidated"] = False
    return value, validated


def validate_activation_receipt(
    receipt: Mapping[str, Any],
    *,
    plan_id: str,
    accepted_plan_sha256: str,
    goal_text: str,
    repository_binding: Mapping[str, Any],
    repository_topology_policy: Mapping[str, Any],
) -> dict[str, Any]:
    value = _validate_activation_receipt_record(receipt)
    binding = validate_repository_binding(
        repository_binding,
        allowed_environment_modes=PLAN_BINDING_ENVIRONMENT_MODES,
    )
    topology = validate_topology_policy(
        repository_topology_policy,
        require_default_deny=False,
    )
    expected = {
        "plan_id": _validate_id(plan_id, field="plan_id"),
        "accepted_plan_sha256": _require_sha256(
            accepted_plan_sha256,
            field="accepted_plan_sha256",
        ),
        "exact_activation_goal_sha256": text_sha256(
            goal_text,
            field="activation goal",
        ),
        "repository_identity_sha256": content_sha256(binding),
        "repository_topology_policy_sha256": content_sha256(topology),
    }
    mismatches = {
        key: {"expected": expected_value, "actual": value.get(key)}
        for key, expected_value in expected.items()
        if value.get(key) != expected_value
    }
    if mismatches:
        raise StateConflict(
            "plan activation receipt does not bind the initialization values",
            details={
                "reason_code": "plan_activation.binding_mismatch",
                "mismatches": mismatches,
            },
        )
    return value


def execution_profile_from_receipt(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    value = _validate_activation_receipt_record(receipt)
    profile = {
        "schema_version": "sys4ai.plan-execution-profile.v1",
        "activation_id": value["activation_id"],
        "activation_receipt_sha256": content_sha256(value),
        "reasoning_effort": value["reasoning_effort"],
        "selection_source": value["selection_source"],
        "accepted_goal_sha256": value["exact_activation_goal_sha256"],
        "accepted_plan_sha256": value["accepted_plan_sha256"],
        "current_thread_id": value["current_thread_id"],
        "current_thread_requested_effort": value[
            "current_thread_requested_effort"
        ],
        "current_thread_effective_effort": value[
            "current_thread_effective_effort"
        ],
        "current_thread_verification_status": "verified",
        "current_thread_evidence_ref": value[
            "current_thread_evidence_ref"
        ],
        "successor_inheritance_required": True,
        "provider_id": value["provider_id"],
        "model_id": value["model_id"],
        "effective_from_generation": value["effective_from_generation"],
        "repository_binding_sha256": value[
            "repository_identity_sha256"
        ],
        "repository_topology_policy_sha256": value[
            "repository_topology_policy_sha256"
        ],
        "hash_basis": "canonical_json_without_profile_content_sha256",
        "profile_content_sha256": "",
        "finalized": True,
    }
    profile["profile_content_sha256"] = profile_sha256(
        profile,
        hash_field="profile_content_sha256",
    )
    return validate_execution_profile(profile)


def validate_execution_profile(
    profile: Mapping[str, Any],
) -> dict[str, Any]:
    value = copy.deepcopy(dict(profile))
    issues = validate_instance(
        value,
        _schema("plan-execution-profile.schema.json"),
    )
    if issues:
        raise RecordValidationError(
            "plan execution profile failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    expected_hash = profile_sha256(
        value,
        hash_field="profile_content_sha256",
    )
    if value["profile_content_sha256"] != expected_hash:
        raise RecordValidationError("plan execution profile content hash is invalid")
    if value["reasoning_effort"] not in {
        value["current_thread_requested_effort"],
        value["current_thread_effective_effort"],
    } or (
        value["current_thread_requested_effort"]
        != value["current_thread_effective_effort"]
    ):
        raise RecordValidationError(
            "plan execution profile current-thread evidence is inconsistent"
        )
    return value
