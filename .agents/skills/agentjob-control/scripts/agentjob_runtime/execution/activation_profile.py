"""Protocol-neutral execution-profile activation primitives."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import contains_secret


DEFAULT_REASONING_EFFORT = "max"
DEFAULT_REPOSITORY_TOPOLOGY_POLICY: dict[str, Any] = {
    "environment_mode": "reuse_bound_checkout",
    "branch_creation_authorized": False,
    "worktree_creation_authorized": False,
    "binding_change_authorized": False,
    "authorization_ref": None,
}


def canonical_text(value: str, *, field: str) -> str:
    if not isinstance(value, str):
        raise RecordValidationError(f"{field} must be a string")
    result = value.replace("\r\n", "\n").replace("\r", "\n")
    if not result.strip():
        raise RecordValidationError(f"{field} must be nonblank")
    if contains_secret(result):
        raise RecordValidationError(
            f"{field} appears to contain a secret; redact it before activation"
        )
    return result


def text_sha256(value: str, *, field: str) -> str:
    return hashlib.sha256(
        canonical_text(value, field=field).encode("utf-8")
    ).hexdigest()


def validate_effort(value: str, *, field: str = "reasoning_effort") -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecordValidationError(f"{field} must be a nonblank exact literal")
    if contains_secret(value):
        raise RecordValidationError(f"{field} appears to contain a secret")
    return value


def validate_evidence_ref(value: str, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecordValidationError(f"{field} must be nonblank")
    if contains_secret(value):
        raise RecordValidationError(f"{field} appears to contain a secret")
    return value


def validate_repository_binding(
    binding: Mapping[str, Any],
    *,
    allowed_environment_modes: frozenset[str],
) -> dict[str, Any]:
    if not isinstance(binding, Mapping):
        raise RecordValidationError("repository binding must be an object")
    required = {
        "root",
        "worktree",
        "branch",
        "starting_revision",
        "environment_mode",
    }
    optional = {"project_id", "git_common_dir"}
    if not required <= set(binding) or set(binding) - required - optional:
        raise RecordValidationError(
            "repository binding does not match the portable execution-profile contract"
        )
    result = copy.deepcopy(dict(binding))
    for key in ("root", "worktree"):
        path = Path(result[key])
        if not path.is_absolute():
            raise RecordValidationError(
                f"repository binding {key} must be an absolute identity path"
            )
        result[key] = str(path.resolve(strict=False))
    for key in ("starting_revision", "environment_mode"):
        if not isinstance(result[key], str) or not result[key].strip():
            raise RecordValidationError(
                f"repository binding {key} must be nonblank"
            )
    if result["environment_mode"] not in allowed_environment_modes:
        raise RecordValidationError("unsupported repository environment mode")
    for key in ("branch", "project_id"):
        if key in result and result[key] is not None and (
            not isinstance(result[key], str) or not result[key].strip()
        ):
            raise RecordValidationError(
                f"repository binding {key} must be nonblank or null"
            )
    if result.get("git_common_dir") is not None:
        common = Path(result["git_common_dir"])
        if not common.is_absolute():
            raise RecordValidationError(
                "repository binding git_common_dir must be absolute or null"
            )
        result["git_common_dir"] = str(common.resolve(strict=False))
    return result


def validate_topology_policy(
    policy: Mapping[str, Any],
    *,
    require_default_deny: bool,
) -> dict[str, Any]:
    if not isinstance(policy, Mapping):
        raise RecordValidationError("repository topology policy must be an object")
    result = copy.deepcopy(dict(policy))
    if set(result) != set(DEFAULT_REPOSITORY_TOPOLOGY_POLICY):
        raise RecordValidationError(
            "repository topology policy has missing or unknown fields"
        )
    if result["environment_mode"] != "reuse_bound_checkout":
        raise RecordValidationError(
            "implementation-plan relays must reuse the bound checkout"
        )
    authority_fields = (
        "branch_creation_authorized",
        "worktree_creation_authorized",
        "binding_change_authorized",
    )
    if any(not isinstance(result[field], bool) for field in authority_fields):
        raise RecordValidationError("topology authority flags must be Boolean")
    authorized = any(result[field] for field in authority_fields)
    if authorized:
        validate_evidence_ref(
            result["authorization_ref"],
            field="repository topology authorization_ref",
        )
    elif result["authorization_ref"] is not None:
        raise RecordValidationError(
            "default-deny topology policy cannot carry an authorization reference"
        )
    if require_default_deny and result != DEFAULT_REPOSITORY_TOPOLOGY_POLICY:
        raise RecordValidationError(
            "initial activation must reuse the bound checkout without topology authority"
        )
    return result


def request_current_thread_profile(
    proposal: Mapping[str, Any],
    *,
    provider: Any,
) -> dict[str, Any]:
    """Configure and verify the selected profile without canonical state writes."""

    value = copy.deepcopy(dict(proposal))
    effort = validate_effort(str(value["reasoning_effort"]))
    capabilities = provider.capabilities()
    if not isinstance(capabilities, Mapping):
        raise RecordValidationError("thread provider capabilities must be an object")
    supported = tuple(
        str(item)
        for item in capabilities.get("supported_reasoning_efforts", ())
    )
    if supported and effort not in supported:
        raise RecordValidationError(
            "selected reasoning effort is unsupported by the provider/model",
            details={
                "reason_code": "activation.reasoning_effort_unsupported",
                "requested": effort,
                "supported": list(supported),
            },
        )
    value["state"] = "current_thread_profile_requested"
    value["current_thread_requested_effort"] = effort
    value["current_thread_effective_effort"] = None
    value["current_thread_verification_status"] = "pending"
    value["current_thread_evidence_ref"] = None
    if capabilities.get("can_configure_current_thread") is not True:
        return value
    configure = getattr(provider, "configure_current_thread", None)
    read_profile = getattr(provider, "read_thread_profile", None)
    if not callable(configure) or not callable(read_profile):
        raise RecordValidationError(
            "provider advertises current-thread configuration without required operations"
        )
    configure_result = configure(
        str(value["current_thread_id"]),
        reasoning_effort=effort,
    )
    observed = read_profile(str(value["current_thread_id"]))
    if not isinstance(observed, Mapping):
        raise RecordValidationError("thread profile observation must be an object")
    effective = observed.get("reasoning_effort")
    if effective != effort:
        raise StateConflict(
            "provider did not verify the selected current-thread reasoning effort",
            details={
                "reason_code": "activation.current_thread_profile_mismatch",
                "requested": effort,
                "effective": effective,
            },
        )
    configure_evidence = (
        configure_result.get("evidence_ref")
        if isinstance(configure_result, Mapping)
        else None
    )
    evidence = str(
        observed.get("evidence_ref")
        or configure_evidence
        or f"provider:{value['provider_id']}:thread:{value['current_thread_id']}"
    )
    value["state"] = "current_thread_profile_verified"
    value["current_thread_effective_effort"] = effort
    value["current_thread_verification_status"] = "verified"
    value["current_thread_evidence_ref"] = validate_evidence_ref(
        evidence,
        field="current thread profile evidence",
    )
    return value


def record_manual_current_thread_profile(
    proposal: Mapping[str, Any],
    *,
    effective_effort: str,
    evidence_ref: str,
) -> dict[str, Any]:
    value = copy.deepcopy(dict(proposal))
    if value.get("state") != "current_thread_profile_requested":
        raise StateConflict(
            "manual profile confirmation requires a pending profile request"
        )
    effective = validate_effort(
        effective_effort,
        field="manual effective reasoning effort",
    )
    if effective != value["reasoning_effort"]:
        raise StateConflict(
            "manual profile confirmation differs from the proposed effort"
        )
    value["state"] = "current_thread_profile_verified"
    value["current_thread_effective_effort"] = effective
    value["current_thread_verification_status"] = "verified"
    value["current_thread_evidence_ref"] = validate_evidence_ref(
        evidence_ref,
        field="manual profile evidence",
    )
    return value


def render_combined_acceptance(
    proposal: Mapping[str, Any],
    *,
    goal_heading: str,
    relay_name: str,
) -> tuple[dict[str, Any], str]:
    value = copy.deepcopy(dict(proposal))
    if value.get("current_thread_verification_status") != "verified":
        raise StateConflict(
            "goal and effort cannot be presented as set before profile verification"
        )
    if value.get("current_thread_requested_effort") != value.get(
        "reasoning_effort"
    ) or value.get("current_thread_effective_effort") != value.get(
        "reasoning_effort"
    ):
        raise StateConflict(
            "current-thread requested and effective effort must match the proposal"
        )
    value["state"] = "presented"
    text = (
        f"I understand the {goal_heading} as:\n\n"
        f"{value['goal_text']}\n\n"
        "The reasoning_effort for this discussion and every future discussion\n"
        f"created by this {relay_name} is set to: {value['reasoning_effort']}.\n\n"
        "Do you accept both the goal and the reasoning_effort?"
    )
    return value, text


def profile_sha256(value: Mapping[str, Any], *, hash_field: str) -> str:
    return content_sha256(
        {key: item for key, item in value.items() if key != hash_field}
    )
