"""Exact goal canonicalization and all-or-nothing relay initialization."""

from __future__ import annotations

import copy
import re
import secrets
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.activation import (
    DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
    execution_profile_from_receipt,
    validate_activation_receipt,
)
from agentjob_runtime.goal.model import (
    GOAL_SCHEMA_VERSION,
    add_seconds,
    append_journal,
    canonical_goal_text,
    contains_secret,
    goal_text_sha256,
    parse_utc,
    repository_identity_hash,
    utc_now,
)
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.records.canonical import content_sha256


FIXED_GUARDS: dict[str, Any] = {
    "max_repeated_state_fingerprints": 1,
    "max_live_continuations": 1,
    "handoff_ready_timeout_seconds": 60,
    "stop_on_human_gate": True,
    "stop_on_validation_failure": True,
    "stop_on_checkpoint_failure": True,
    "stop_on_unexpected_dirty_state": True,
    "stop_on_no_progress": True,
    "stop_on_repeated_state": True,
    "stop_on_capability_loss": True,
    "stop_on_repository_mismatch": True,
}
GOAL_ID_RE = re.compile(r"^CG-\d{8}T\d{6}Z-[a-f0-9]{8,64}$")


def _validate_completion_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    required = {"interpretation", "required_evidence", "user_confirmed_when_ambiguous"}
    if not isinstance(contract, Mapping) or set(contract) != required:
        raise RecordValidationError(
            "completion contract must contain interpretation, required_evidence, and user_confirmed_when_ambiguous"
        )
    if not isinstance(contract["interpretation"], str) or not contract["interpretation"].strip():
        raise RecordValidationError("completion contract interpretation must be nonblank")
    evidence = contract["required_evidence"]
    if (
        not isinstance(evidence, list)
        or not evidence
        or any(not isinstance(item, str) or not item.strip() for item in evidence)
        or len(set(evidence)) != len(evidence)
    ):
        raise RecordValidationError("completion contract requires unique nonblank evidence criteria")
    if not isinstance(contract["user_confirmed_when_ambiguous"], bool):
        raise RecordValidationError("user_confirmed_when_ambiguous must be Boolean")
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
        raise RecordValidationError("repository binding does not match the portable binding contract")
    result = copy.deepcopy(dict(binding))
    for key in ("project_id", "starting_revision", "environment_mode"):
        if not isinstance(result[key], str) or not result[key].strip():
            raise RecordValidationError(f"repository binding {key} must be nonblank")
    for key in ("root", "worktree"):
        path = Path(result[key])
        if not path.is_absolute():
            raise RecordValidationError(f"repository binding {key} must be an absolute identity path")
        result[key] = str(path.resolve(strict=False))
    if result["git_common_dir"] is not None:
        common = Path(result["git_common_dir"])
        if not common.is_absolute():
            raise RecordValidationError("git_common_dir must be an absolute identity path or null")
        result["git_common_dir"] = str(common.resolve(strict=False))
    if result["branch"] is not None and (
        not isinstance(result["branch"], str) or not result["branch"].strip()
    ):
        raise RecordValidationError("branch must be nonblank or null")
    if result["environment_mode"] not in {"local", "remote", "container"}:
        raise RecordValidationError("unsupported repository environment mode")
    return result


def _validate_guards(
    guards: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], str | None]:
    if guards is None:
        guards = {}
    if not isinstance(guards, Mapping):
        raise RecordValidationError("guards must be an object")
    allowed = {"max_continue_passes", "deadline_at", *FIXED_GUARDS}
    if not set(guards) <= allowed:
        raise RecordValidationError("unknown goal guard")
    max_continue_passes = guards.get("max_continue_passes")
    if max_continue_passes is not None and (
        isinstance(max_continue_passes, bool)
        or not isinstance(max_continue_passes, int)
        or max_continue_passes <= 0
    ):
        raise RecordValidationError("max_continue_passes must be a positive integer")
    deadline = guards.get("deadline_at")
    if deadline is not None:
        if not isinstance(deadline, str):
            raise RecordValidationError("deadline_at must be a UTC timestamp or null")
        parse_utc(deadline)
    effective = {**FIXED_GUARDS, "max_continue_passes": max_continue_passes}
    for key, fixed in FIXED_GUARDS.items():
        if key in guards and guards[key] != fixed:
            raise RecordValidationError(f"fixed guard {key} cannot be weakened or changed")
    return effective, deadline


def initialize_goal(
    store: SQLiteGoalStore,
    *,
    goal_text: str,
    completion_contract: Mapping[str, Any],
    guards: Mapping[str, Any] | None = None,
    repository_binding: Mapping[str, Any],
    initial_fingerprint: str,
    authorization: Mapping[str, Any],
    activation_receipt: Mapping[str, Any],
    runtime_binding: Mapping[str, Any] | None = None,
    repository_topology_policy: Mapping[str, Any] | None = None,
    supersession: Mapping[str, Any] | None = None,
    goal_id: str | None = None,
    timestamp: str | None = None,
    launcher_token: str | None = None,
) -> dict[str, Any]:
    """Initialize one accepted v3 goal and acquire its worktree lease atomically."""

    now = timestamp or utc_now()
    parse_utc(now)
    exact_goal = canonical_goal_text(goal_text)
    if not exact_goal.strip():
        raise RecordValidationError("goal_text must be nonblank")
    if contains_secret(exact_goal):
        raise RecordValidationError(
            "goal text appears to contain a secret; redact it before durable persistence"
        )
    contract = _validate_completion_contract(completion_contract)
    if contains_secret(str(contract)):
        raise RecordValidationError("completion contract appears to contain a secret")
    guard_values, deadline = _validate_guards(guards)
    if deadline is not None and parse_utc(deadline) <= parse_utc(now):
        raise RecordValidationError("deadline_at must be later than initialization")
    binding = _validate_repository_binding(repository_binding)
    topology = copy.deepcopy(
        dict(repository_topology_policy or DEFAULT_REPOSITORY_TOPOLOGY_POLICY)
    )
    if topology != DEFAULT_REPOSITORY_TOPOLOGY_POLICY:
        raise RecordValidationError(
            "new goals must reuse the current bound checkout without topology authority"
        )
    accepted = validate_activation_receipt(
        activation_receipt,
        goal_text=exact_goal,
        completion_contract=contract,
        repository_binding=binding,
        repository_topology_policy=topology,
    )
    execution_profile = execution_profile_from_receipt(accepted)
    runtime = copy.deepcopy(
        dict(
            runtime_binding
            or {
                "skill_versions": {
                    "agentjob-control": "0.3.0",
                    "continue": "0.3.0",
                    "continue-goal": "0.3.0",
                    "continue-implementing-goal": "0.3.0",
                },
                "capability_versions": [
                    "sys4ai.goal-relay-state.v3",
                    "sys4ai.continuation-envelope.v2",
                    "sys4ai.thread-provider.v2",
                ],
                "source_lock_ref": None,
                "provider_id": accepted["provider_id"],
            }
        )
    )
    if runtime.get("provider_id") != accepted["provider_id"]:
        raise RecordValidationError(
            "runtime binding provider differs from accepted activation provider"
        )
    if not re.fullmatch(r"[a-f0-9]{64}", initial_fingerprint):
        raise RecordValidationError("initial fingerprint must be a lowercase SHA-256 value")
    if dict(authorization) != {"fresh_recursive_threads_explicitly_requested": True}:
        raise RecordValidationError(
            "initialization requires explicit fresh recursive thread authorization"
        )
    candidate_id = goal_id or f"CG-{parse_utc(now).strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(8)}"
    if not GOAL_ID_RE.fullmatch(candidate_id):
        raise RecordValidationError("invalid goal_id")
    token = launcher_token or secrets.token_hex(24)
    transaction_id = secrets.token_hex(16)
    repository_fingerprint = repository_identity_hash(binding)
    lease = {
        "repository_fingerprint": repository_fingerprint,
        "goal_id": candidate_id,
        "generation": 0,
        "holder_kind": "launcher",
        "holder_token": token,
        "transaction_id": transaction_id,
        "acquired_at": now,
        "heartbeat_at": now,
        "expires_at": add_seconds(now, 300),
    }
    record: dict[str, Any] = {
        "schema_version": GOAL_SCHEMA_VERSION,
        "goal_id": candidate_id,
        "goal_text": exact_goal,
        "goal_sha256": goal_text_sha256(exact_goal),
        "completion_contract": contract,
        "completion_contract_sha256": content_sha256(contract),
        "amendments": [],
        "created_at": now,
        "deadline_at": deadline,
        "guards": guard_values,
        "repository_binding": binding,
        "authorization": {
            "fresh_recursive_threads_explicitly_requested": True,
            "activation_receipt_sha256": content_sha256(accepted),
        },
        "activation": accepted,
        "execution_profile": execution_profile,
        "runtime_binding": runtime,
        "repository_topology_policy": topology,
        "supersession": copy.deepcopy(dict(supersession))
        if supersession is not None
        else None,
        "resolution_history": [],
        "human_intervention": None,
        "completion_report": None,
        "state": {
            "revision": 1,
            "phase": "initialized",
            "current_generation": 0,
            "passes_consumed": 0,
            "active_lease": lease,
            "goal_evaluation": "unmet",
            "last_canonical_fingerprint": initial_fingerprint,
            "canonical_fingerprint_history": [initial_fingerprint],
            "terminal_reason": None,
        },
        "generations": {},
        "handoff": {
            "status": "none",
            "generation": 1,
            "token": None,
            "idempotency_key": None,
            "predecessor_thread_id": None,
            "successor_thread_id": None,
        },
        "journal": [],
        "updated_at": now,
        "extensions": {},
    }
    append_journal(
        record,
        "event",
        {
            "event_type": "initialized",
            "goal_id": candidate_id,
            "goal_sha256": record["goal_sha256"],
            "completion_contract_sha256": record["completion_contract_sha256"],
            "activation_receipt_sha256": record["authorization"][
                "activation_receipt_sha256"
            ],
            "reasoning_effort": execution_profile["reasoning_effort"],
            "repository_fingerprint": repository_fingerprint,
            "timestamp": now,
        },
    )
    return store.create_goal(record)


def supersede_legacy_goal(
    store: SQLiteGoalStore,
    *,
    predecessor_goal_id: str,
    expected_predecessor_revision: int,
    safe_boundary_evidence: Mapping[str, Any],
    goal_text: str,
    completion_contract: Mapping[str, Any],
    repository_binding: Mapping[str, Any],
    initial_fingerprint: str,
    authorization: Mapping[str, Any],
    activation_receipt: Mapping[str, Any],
    guards: Mapping[str, Any] | None = None,
    runtime_binding: Mapping[str, Any] | None = None,
    goal_id: str | None = None,
    timestamp: str | None = None,
    launcher_token: str | None = None,
) -> dict[str, Any]:
    """Create a v3 successor goal without rewriting its v1/v2 predecessor."""

    predecessor = store.load_goal(predecessor_goal_id)
    if predecessor.get("schema_version") not in {
        "sys4ai.continue-goal.v1",
        "sys4ai.continue-goal.v2",
    }:
        raise StateConflict("only a v1/v2 goal may be superseded into v3")
    if predecessor["state"]["revision"] != expected_predecessor_revision:
        raise StateConflict("legacy supersession expected revision is stale")
    if predecessor["state"].get("active_lease") is not None:
        raise StateConflict(
            "legacy supersession requires a released safe boundary"
        )
    if predecessor["goal_sha256"] != goal_text_sha256(goal_text):
        raise StateConflict(
            "legacy supersession must retain the exact accepted goal"
        )
    if predecessor["completion_contract_sha256"] != content_sha256(
        _validate_completion_contract(completion_contract)
    ):
        raise StateConflict(
            "legacy supersession must retain the exact completion contract"
        )
    if predecessor["repository_binding"] != _validate_repository_binding(
        repository_binding
    ):
        raise StateConflict(
            "legacy supersession cannot silently change repository binding"
        )
    unknown_consumption = any(
        generation.get("invocation_state") == "unknown"
        or (
            generation.get("invocation_consumed") is True
            and generation.get("finalized_receipt_hash") is None
        )
        for generation in predecessor["generations"].values()
    )
    unresolved_provider = (
        predecessor["handoff"].get("status") in {"intent", "ambiguous", "timeout"}
        or any(
            generation.get("terminal_or_successor_outcome")
            in {"ambiguous", "timeout"}
            for generation in predecessor["generations"].values()
        )
    )
    if unknown_consumption or unresolved_provider:
        raise StateConflict(
            "legacy supersession is unsafe while consumption or provider creation is unresolved"
        )
    evidence = copy.deepcopy(dict(safe_boundary_evidence))
    if (
        evidence.get("no_ambiguous_consumption") is not True
        or evidence.get("no_unresolved_provider_create") is not True
        or not isinstance(evidence.get("evidence_ref"), str)
        or not evidence["evidence_ref"].strip()
    ):
        raise RecordValidationError(
            "legacy supersession requires explicit safe-boundary evidence"
        )
    predecessor_hash = content_sha256(predecessor)
    now = timestamp or utc_now()
    result = initialize_goal(
        store,
        goal_text=goal_text,
        completion_contract=completion_contract,
        guards=guards,
        repository_binding=repository_binding,
        initial_fingerprint=initial_fingerprint,
        authorization=authorization,
        activation_receipt=activation_receipt,
        runtime_binding=runtime_binding,
        repository_topology_policy=DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
        supersession={
            "predecessor_goal_id": predecessor_goal_id,
            "predecessor_schema_version": predecessor["schema_version"],
            "predecessor_goal_sha256": predecessor["goal_sha256"],
            "predecessor_record_sha256": predecessor_hash,
            "predecessor_revision": predecessor["state"]["revision"],
            "safe_boundary_evidence_ref": evidence["evidence_ref"],
            "accepted_activation_id": activation_receipt["activation_id"],
            "superseded_at": now,
        },
        goal_id=goal_id,
        timestamp=now,
        launcher_token=launcher_token,
    )
    if content_sha256(store.load_goal(predecessor_goal_id)) != predecessor_hash:
        raise StateConflict("legacy predecessor changed during supersession")
    return result
