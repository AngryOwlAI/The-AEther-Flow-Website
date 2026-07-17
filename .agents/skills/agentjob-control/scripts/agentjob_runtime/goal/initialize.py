"""Exact goal canonicalization and all-or-nothing relay initialization."""

from __future__ import annotations

import copy
import re
import secrets
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError
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


def _validate_guards(guards: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    if not isinstance(guards, Mapping):
        raise RecordValidationError("guards must be an object")
    allowed = {"max_continue_passes", "deadline_at", *FIXED_GUARDS}
    if not set(guards) <= allowed:
        raise RecordValidationError("unknown goal guard")
    if not isinstance(guards.get("max_continue_passes"), int) or guards["max_continue_passes"] <= 0:
        raise RecordValidationError("max_continue_passes must be a positive integer")
    deadline = guards.get("deadline_at")
    if not isinstance(deadline, str):
        raise RecordValidationError("deadline_at is required")
    parse_utc(deadline)
    effective = {**FIXED_GUARDS, "max_continue_passes": guards["max_continue_passes"]}
    for key, fixed in FIXED_GUARDS.items():
        if key in guards and guards[key] != fixed:
            raise RecordValidationError(f"fixed guard {key} cannot be weakened or changed")
    return effective, deadline


def initialize_goal(
    store: SQLiteGoalStore,
    *,
    goal_text: str,
    completion_contract: Mapping[str, Any],
    guards: Mapping[str, Any],
    repository_binding: Mapping[str, Any],
    initial_fingerprint: str,
    authorization: Mapping[str, Any],
    goal_id: str | None = None,
    timestamp: str | None = None,
    launcher_token: str | None = None,
) -> dict[str, Any]:
    """Initialize one immutable goal and acquire its worktree lease atomically."""

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
    if parse_utc(deadline) <= parse_utc(now):
        raise RecordValidationError("deadline_at must be later than initialization")
    binding = _validate_repository_binding(repository_binding)
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
        "authorization": {"fresh_recursive_threads_explicitly_requested": True},
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
            "repository_fingerprint": repository_fingerprint,
            "timestamp": now,
        },
    )
    return store.create_goal(record)
