"""Pending activation handshake and immutable combined-acceptance receipts."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.execution.activation_profile import (
    DEFAULT_REASONING_EFFORT,
    DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
    record_manual_current_thread_profile as _record_manual_profile,
    request_current_thread_profile as _request_current_thread_profile,
)
from agentjob_runtime.goal.model import (
    canonical_goal_text,
    goal_text_sha256,
    repository_identity_hash,
    utc_now,
)
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


ACTIVATION_STATES = frozenset(
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
def _validate_completion_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "interpretation",
        "required_evidence",
        "user_confirmed_when_ambiguous",
    }
    if not isinstance(contract, Mapping) or set(contract) != required:
        raise RecordValidationError(
            "completion contract must contain interpretation, required_evidence, and user_confirmed_when_ambiguous"
        )
    if (
        not isinstance(contract["interpretation"], str)
        or not contract["interpretation"].strip()
    ):
        raise RecordValidationError("completion contract interpretation must be nonblank")
    evidence = contract["required_evidence"]
    if (
        not isinstance(evidence, list)
        or not evidence
        or any(not isinstance(item, str) or not item.strip() for item in evidence)
        or len(set(evidence)) != len(evidence)
    ):
        raise RecordValidationError(
            "completion contract requires unique nonblank evidence criteria"
        )
    if not isinstance(contract["user_confirmed_when_ambiguous"], bool):
        raise RecordValidationError(
            "user_confirmed_when_ambiguous must be Boolean"
        )
    return copy.deepcopy(dict(contract))


def _validate_repository_binding(binding: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "project_id",
        "root",
        "worktree",
        "branch",
        "git_common_dir",
        "starting_revision",
        "environment_mode",
    }
    if not isinstance(binding, Mapping) or set(binding) != required:
        raise RecordValidationError(
            "repository binding does not match the portable binding contract"
        )
    result = copy.deepcopy(dict(binding))
    for key in ("project_id", "starting_revision", "environment_mode"):
        if not isinstance(result[key], str) or not result[key].strip():
            raise RecordValidationError(
                f"repository binding {key} must be nonblank"
            )
    for key in ("root", "worktree"):
        path = Path(result[key])
        if not path.is_absolute():
            raise RecordValidationError(
                f"repository binding {key} must be an absolute identity path"
            )
        result[key] = str(path.resolve(strict=False))
    if result["git_common_dir"] is not None:
        common = Path(result["git_common_dir"])
        if not common.is_absolute():
            raise RecordValidationError(
                "git_common_dir must be an absolute identity path or null"
            )
        result["git_common_dir"] = str(common.resolve(strict=False))
    if result["branch"] is not None and (
        not isinstance(result["branch"], str) or not result["branch"].strip()
    ):
        raise RecordValidationError("branch must be nonblank or null")
    if result["environment_mode"] not in {"local", "remote", "container"}:
        raise RecordValidationError("unsupported repository environment mode")
    return result


def _schema(name: str) -> Path:
    return Path(__file__).resolve().parents[3] / "schemas" / name


def _validate_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(receipt))
    schema_name = (
        "goal-activation-receipt-v2.schema.json"
        if value.get("schema_version") == "sys4ai.goal-activation-receipt.v2"
        else "goal-activation-receipt.schema.json"
    )
    issues = validate_instance(value, _schema(schema_name))
    if issues:
        raise RecordValidationError(
            "goal activation receipt failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    if value["reasoning_effort"] != value["current_thread_requested_effort"]:
        raise RecordValidationError("accepted effort differs from the current-thread request")
    if value["reasoning_effort"] != value["current_thread_effective_effort"]:
        raise RecordValidationError("accepted effort was not verified on the current discussion")
    if value.get("schema_version") == "sys4ai.goal-activation-receipt.v2":
        expected = content_sha256(
            {
                key: item
                for key, item in value.items()
                if key != "receipt_content_sha256"
            }
        )
        if value["receipt_content_sha256"] != expected:
            raise RecordValidationError(
                "continuous goal activation receipt hash mismatch"
            )
    return value


def create_activation_proposal(
    *,
    goal_text: str,
    completion_contract: Mapping[str, Any],
    repository_binding: Mapping[str, Any],
    current_thread_id: str,
    provider_id: str,
    model_id: str | None = None,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    selection_source: str = "default",
    repository_topology_policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create noncanonical pending state; this function never writes a goal."""

    exact_goal = canonical_goal_text(goal_text)
    if not exact_goal.strip():
        raise RecordValidationError("activation goal must be nonblank")
    if contains_secret(exact_goal):
        raise RecordValidationError(
            "activation goal appears to contain a secret; redact it before persistence"
        )
    contract = _validate_completion_contract(completion_contract)
    if contains_secret(str(contract)):
        raise RecordValidationError(
            "activation completion contract appears to contain a secret"
        )
    binding = _validate_repository_binding(repository_binding)
    if not current_thread_id.strip() or not provider_id.strip():
        raise RecordValidationError("activation requires current thread and provider identity")
    if not isinstance(reasoning_effort, str) or not reasoning_effort.strip():
        raise RecordValidationError("reasoning_effort must be a nonblank exact literal")
    if selection_source not in {"default", "user_override"}:
        raise RecordValidationError("invalid reasoning-effort selection source")
    topology = copy.deepcopy(
        dict(repository_topology_policy or DEFAULT_REPOSITORY_TOPOLOGY_POLICY)
    )
    if topology != DEFAULT_REPOSITORY_TOPOLOGY_POLICY:
        raise RecordValidationError(
            "initial activation must reuse the bound checkout without topology authority"
        )
    return {
        "state": "draft",
        "goal_text": exact_goal,
        "goal_sha256": goal_text_sha256(exact_goal),
        "completion_contract": contract,
        "completion_contract_sha256": content_sha256(contract),
        "reasoning_effort": reasoning_effort,
        "selection_source": selection_source,
        "current_thread_id": current_thread_id,
        "current_thread_requested_effort": None,
        "current_thread_effective_effort": None,
        "current_thread_verification_status": "not_requested",
        "current_thread_evidence_ref": None,
        "provider_id": provider_id,
        "model_id": model_id,
        "repository_binding": binding,
        "repository_identity_sha256": repository_identity_hash(binding),
        "repository_topology_policy": topology,
        "repository_topology_policy_sha256": content_sha256(topology),
        "acceptance_invalidated": False,
    }


def request_current_thread_profile(
    proposal: Mapping[str, Any],
    *,
    provider: Any,
) -> dict[str, Any]:
    """Configure and verify the current discussion when the host supports it."""

    return _request_current_thread_profile(proposal, provider=provider)


def record_manual_current_thread_profile(
    proposal: Mapping[str, Any],
    *,
    effective_effort: str,
    evidence_ref: str,
) -> dict[str, Any]:
    """Record host/user attestation when no programmatic setter is exposed."""

    return _record_manual_profile(
        proposal,
        effective_effort=effective_effort,
        evidence_ref=evidence_ref,
    )


def revise_activation(
    proposal: Mapping[str, Any],
    *,
    goal_text: str | None = None,
    completion_contract: Mapping[str, Any] | None = None,
    reasoning_effort: str | None = None,
) -> dict[str, Any]:
    """Invalidate prior presentation while keeping a user effort override sticky."""

    value = copy.deepcopy(dict(proposal))
    changed_goal = goal_text is not None or completion_contract is not None
    changed_effort = reasoning_effort is not None
    if not changed_goal and not changed_effort:
        raise RecordValidationError("activation revision must change goal, contract, or effort")
    if goal_text is not None:
        value["goal_text"] = canonical_goal_text(goal_text)
        if not value["goal_text"].strip():
            raise RecordValidationError("revised goal must be nonblank")
        if contains_secret(value["goal_text"]):
            raise RecordValidationError(
                "revised goal appears to contain a secret"
            )
        value["goal_sha256"] = goal_text_sha256(value["goal_text"])
    if completion_contract is not None:
        value["completion_contract"] = _validate_completion_contract(completion_contract)
        if contains_secret(str(value["completion_contract"])):
            raise RecordValidationError(
                "revised completion contract appears to contain a secret"
            )
        value["completion_contract_sha256"] = content_sha256(
            value["completion_contract"]
        )
    if reasoning_effort is not None:
        if not isinstance(reasoning_effort, str) or not reasoning_effort.strip():
            raise RecordValidationError("revised reasoning effort must be nonblank")
        value["reasoning_effort"] = reasoning_effort
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


def render_combined_acceptance(proposal: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    value = copy.deepcopy(dict(proposal))
    if value.get("current_thread_verification_status") != "verified":
        raise StateConflict(
            "goal and effort cannot be presented as set before profile verification"
        )
    value["state"] = "presented"
    # A revision invalidates only the prior presentation. This freshly rendered
    # pair is now the sole combined-acceptance candidate.
    value["acceptance_invalidated"] = False
    text = (
        "I understand the goal as:\n\n"
        f"{value['goal_text']}\n\n"
        "The reasoning_effort for this discussion and every successor discussion\n"
        f"created by this goal relay is set to: {value['reasoning_effort']}.\n\n"
        "Do you accept both the goal and the reasoning_effort?"
    )
    return value, text


def accept_activation(
    proposal: Mapping[str, Any],
    *,
    acceptance_message: str,
    acceptance_evidence_ref: str,
    timestamp: str | None = None,
    activation_id: str | None = None,
    supersedes_activation_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    value = copy.deepcopy(dict(proposal))
    if value.get("state") != "presented":
        raise StateConflict("combined acceptance requires the latest presented values")
    if value.get("current_thread_verification_status") != "verified":
        raise StateConflict("combined acceptance requires verified current-thread effort")
    if not acceptance_message.strip() or not acceptance_evidence_ref.strip():
        raise RecordValidationError("combined acceptance requires exact host evidence")
    now = timestamp or utc_now()
    receipt = {
        "schema_version": "sys4ai.goal-activation-receipt.v1",
        "activation_id": activation_id
        or f"GAR-{hashlib.sha256((value['goal_sha256'] + now).encode()).hexdigest()[:24]}",
        "status": "accepted",
        "combined_acceptance": True,
        "accepted_goal_sha256": value["goal_sha256"],
        "accepted_completion_contract_sha256": value[
            "completion_contract_sha256"
        ],
        "reasoning_effort": value["reasoning_effort"],
        "selection_source": value["selection_source"],
        "current_thread_id": value["current_thread_id"],
        "current_thread_requested_effort": value["reasoning_effort"],
        "current_thread_effective_effort": value["current_thread_effective_effort"],
        "current_thread_verification_status": "verified",
        "current_thread_evidence_ref": value["current_thread_evidence_ref"],
        "provider_id": value["provider_id"],
        "model_id": value["model_id"],
        "repository_identity_sha256": value["repository_identity_sha256"],
        "repository_topology_policy_sha256": value[
            "repository_topology_policy_sha256"
        ],
        "acceptance_message_sha256": hashlib.sha256(
            acceptance_message.encode("utf-8")
        ).hexdigest(),
        "acceptance_evidence_ref": acceptance_evidence_ref,
        "accepted_at": now,
        "supersedes_activation_id": supersedes_activation_id,
        "finalized": True,
    }
    validated = _validate_receipt(receipt)
    value["state"] = "accepted"
    value["acceptance_invalidated"] = False
    return value, validated


def validate_activation_receipt(
    receipt: Mapping[str, Any],
    *,
    goal_text: str,
    completion_contract: Mapping[str, Any],
    repository_binding: Mapping[str, Any],
    repository_topology_policy: Mapping[str, Any],
) -> dict[str, Any]:
    value = _validate_receipt(receipt)
    expected = {
        "accepted_goal_sha256": goal_text_sha256(goal_text),
        "accepted_completion_contract_sha256": content_sha256(
            _validate_completion_contract(completion_contract)
        ),
        "repository_identity_sha256": repository_identity_hash(
            _validate_repository_binding(repository_binding)
        ),
        "repository_topology_policy_sha256": content_sha256(
            dict(repository_topology_policy)
        ),
    }
    mismatches = {
        key: {"expected": expected_value, "actual": value.get(key)}
        for key, expected_value in expected.items()
        if value.get(key) != expected_value
    }
    if mismatches:
        raise StateConflict(
            "activation receipt does not bind the values being initialized",
            details={"reason_code": "activation.binding_mismatch", "mismatches": mismatches},
        )
    return value


def execution_profile_from_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    value = _validate_receipt(receipt)
    return {
        "reasoning_effort": value["reasoning_effort"],
        "selection_source": value["selection_source"],
        "accepted_goal_sha256": value["accepted_goal_sha256"],
        "accepted_completion_contract_sha256": value[
            "accepted_completion_contract_sha256"
        ],
        "current_thread_id": value["current_thread_id"],
        "current_thread_requested_effort": value[
            "current_thread_requested_effort"
        ],
        "current_thread_effective_effort": value[
            "current_thread_effective_effort"
        ],
        "current_thread_verification_status": "verified",
        "current_thread_evidence_ref": value["current_thread_evidence_ref"],
        "successor_inheritance_required": True,
        "provider_id": value["provider_id"],
        "model_id": value["model_id"],
    }
