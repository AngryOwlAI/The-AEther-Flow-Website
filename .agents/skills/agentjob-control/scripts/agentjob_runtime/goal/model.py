"""Shared goal-state vocabulary, canonicalization, and record validation."""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import re
from pathlib import Path
from typing import Any, Iterable, Mapping, MutableMapping

from agentjob_runtime.errors import RecordValidationError
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


GOAL_SCHEMA_VERSION_V1 = "sys4ai.continue-goal.v1"
GOAL_SCHEMA_VERSION_V2 = "sys4ai.continue-goal.v2"
GOAL_SCHEMA_VERSION = "sys4ai.continue-goal.v3"
GOAL_SCHEMA_FILES = {
    GOAL_SCHEMA_VERSION_V1: "goal-state.schema.json",
    GOAL_SCHEMA_VERSION_V2: "goal-state-v2.schema.json",
    GOAL_SCHEMA_VERSION: "goal-state-v3.schema.json",
}
LEASE_SCHEMA_VERSION = "sys4ai.continue-goal-worktree-lease.v1"

NONTERMINAL_PHASES = frozenset(
    {
        "initialized",
        "successor_intent",
        "successor_created",
        "step_active",
        "step_verifying",
        "step_verified",
        "continuation_required",
        "recovery_pending",
    }
)
TERMINAL_PHASES = frozenset(
    {
        "terminal_complete",
        "terminal_awaiting_human",
        "terminal_capability_blocked",
        "terminal_guard_exhausted",
        "terminal_no_progress",
        "terminal_validation_failed",
        "terminal_handoff_ambiguous",
        "terminal_handoff_timeout",
        "terminal_duplicate_detected",
        "terminal_corrupt_state",
        "terminal_failed",
        "terminal_cancelled",
    }
)
V3_TERMINAL_PHASES = frozenset(
    {
        "terminal_complete",
        "terminal_awaiting_human",
        "terminal_policy_limit",
        "terminal_integrity_incident",
        "terminal_cancelled",
    }
)
ALL_TERMINAL_PHASES = frozenset(TERMINAL_PHASES | V3_TERMINAL_PHASES)
RECOVERABLE_TERMINALS = frozenset(
    TERMINAL_PHASES
    - {
        "terminal_complete",
        "terminal_duplicate_detected",
        "terminal_corrupt_state",
        "terminal_cancelled",
    }
)
ABSORBING_TERMINALS = frozenset(TERMINAL_PHASES - RECOVERABLE_TERMINALS)
PHASES = frozenset(NONTERMINAL_PHASES | ALL_TERMINAL_PHASES)
INVOCATION_STATES = frozenset({"not_authorized", "authorized", "returned", "unknown"})
HOLDER_KINDS = frozenset({"launcher", "continuation", "successor_reserved", "quarantined"})

STOP_PHASES = {
    "goal_met": "terminal_complete",
    "human_gate": "terminal_awaiting_human",
    "indeterminate": "terminal_awaiting_human",
    "capability": "terminal_capability_blocked",
    "pass_limit": "terminal_guard_exhausted",
    "deadline_limit": "terminal_guard_exhausted",
    "repetition_limit": "terminal_guard_exhausted",
    "budget_limit": "terminal_guard_exhausted",
    "no_action": "terminal_no_progress",
    "no_progress": "terminal_no_progress",
    "repeated_state": "terminal_no_progress",
    "validation": "terminal_validation_failed",
    "checkpoint": "terminal_validation_failed",
    "dirty_state": "terminal_validation_failed",
    "ambiguous_dispatch": "terminal_handoff_ambiguous",
    "handoff_timeout": "terminal_handoff_timeout",
    "duplicate": "terminal_duplicate_detected",
    "schema": "terminal_corrupt_state",
    "hash": "terminal_corrupt_state",
    "journal": "terminal_corrupt_state",
    "path": "terminal_corrupt_state",
    "repository": "terminal_failed",
    "interrupted": "terminal_failed",
    "execution": "terminal_failed",
    "dispatch_failed": "terminal_failed",
    "cancelled": "terminal_cancelled",
}
V3_STOP_PHASES = {
    "goal_met": "terminal_complete",
    "human_gate": "terminal_awaiting_human",
    "pass_limit": "terminal_policy_limit",
    "deadline_limit": "terminal_policy_limit",
    "budget_limit": "terminal_policy_limit",
    "duplicate": "terminal_integrity_incident",
    "schema": "terminal_integrity_incident",
    "hash": "terminal_integrity_incident",
    "journal": "terminal_integrity_incident",
    "path": "terminal_integrity_incident",
    "cancelled": "terminal_cancelled",
    "ambiguous_dispatch": "recovery_pending",
    "handoff_timeout": "recovery_pending",
    "indeterminate": "continuation_required",
    "capability": "continuation_required",
    "repetition_limit": "continuation_required",
    "no_action": "continuation_required",
    "no_progress": "continuation_required",
    "repeated_state": "continuation_required",
    "validation": "continuation_required",
    "checkpoint": "continuation_required",
    "dirty_state": "continuation_required",
    "repository": "continuation_required",
    "interrupted": "recovery_pending",
    "execution": "continuation_required",
    "dispatch_failed": "continuation_required",
}

NORMAL_TRANSITIONS = frozenset(
    {
        ("initialized", "successor_intent"),
        ("successor_intent", "successor_created"),
        ("successor_intent", "terminal_failed"),
        ("successor_intent", "terminal_handoff_ambiguous"),
        ("successor_intent", "terminal_duplicate_detected"),
        ("successor_intent", "terminal_handoff_timeout"),
        ("successor_created", "step_active"),
        ("step_active", "step_active"),
        ("step_active", "step_verifying"),
        ("step_active", "terminal_awaiting_human"),
        ("step_verifying", "step_verified"),
        ("step_verified", "terminal_complete"),
        ("step_verified", "continuation_required"),
        ("continuation_required", "successor_intent"),
    }
    | {("step_active", terminal) for terminal in ALL_TERMINAL_PHASES - {"terminal_complete"}}
    | {("step_verified", terminal) for terminal in ALL_TERMINAL_PHASES - {"terminal_complete"}}
)
V3_NORMAL_TRANSITIONS = frozenset(
    {
        ("initialized", "successor_intent"),
        ("successor_intent", "successor_created"),
        ("successor_intent", "continuation_required"),
        ("successor_intent", "recovery_pending"),
        ("successor_intent", "terminal_integrity_incident"),
        ("successor_created", "step_active"),
        ("step_active", "step_active"),
        ("step_active", "step_verifying"),
        ("step_active", "continuation_required"),
        ("step_active", "recovery_pending"),
        ("step_active", "terminal_awaiting_human"),
        ("step_active", "terminal_policy_limit"),
        ("step_active", "terminal_integrity_incident"),
        ("step_active", "terminal_cancelled"),
        ("step_verifying", "step_verified"),
        ("step_verified", "terminal_complete"),
        ("step_verified", "continuation_required"),
        ("step_verified", "recovery_pending"),
        ("step_verified", "terminal_awaiting_human"),
        ("step_verified", "terminal_policy_limit"),
        ("step_verified", "terminal_integrity_incident"),
        ("step_verified", "terminal_cancelled"),
        ("continuation_required", "successor_intent"),
        ("recovery_pending", "successor_created"),
        ("recovery_pending", "successor_intent"),
        ("recovery_pending", "continuation_required"),
        ("recovery_pending", "terminal_awaiting_human"),
        ("recovery_pending", "terminal_integrity_incident"),
        ("recovery_pending", "terminal_cancelled"),
    }
)

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def parse_utc(value: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as error:
        raise RecordValidationError(f"invalid UTC timestamp: {value!r}") from error
    if parsed.tzinfo is None:
        raise RecordValidationError(f"timestamp lacks timezone: {value!r}")
    return parsed.astimezone(dt.timezone.utc)


def add_seconds(value: str, seconds: int) -> str:
    return (
        (parse_utc(value) + dt.timedelta(seconds=seconds))
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def canonical_goal_text(value: str) -> str:
    if not isinstance(value, str):
        raise RecordValidationError("goal_text must be a string")
    return value.replace("\r\n", "\n").replace("\r", "\n")


def goal_text_sha256(value: str) -> str:
    return hashlib.sha256(canonical_goal_text(value).encode("utf-8")).hexdigest()


def canonical_fingerprint(payload: Mapping[str, Any]) -> str:
    if not isinstance(payload, Mapping):
        raise RecordValidationError("fingerprint payload must be an object")
    return content_sha256(dict(payload))


def fingerprint_status(history: Iterable[str], candidate: str) -> str:
    values = list(history)
    if values and values[-1] == candidate:
        return "unchanged"
    if candidate in values:
        return "repeated"
    return "new"


def map_stop(reason: str, *, schema_version: str | None = None) -> str:
    mapping = V3_STOP_PHASES if schema_version == GOAL_SCHEMA_VERSION else STOP_PHASES
    try:
        return mapping[reason]
    except KeyError as error:
        raise RecordValidationError(f"unregistered stop reason: {reason!r}") from error


def repository_identity_hash(binding: Mapping[str, Any]) -> str:
    return content_sha256(
        {
            "project_id": binding.get("project_id"),
            "root": binding.get("root"),
            "worktree": binding.get("worktree"),
            "git_common_dir": binding.get("git_common_dir"),
        }
    )


def effective_completion_contract(record: Mapping[str, Any]) -> Mapping[str, Any]:
    value: Mapping[str, Any] = record["completion_contract"]
    for amendment in record.get("amendments", []):
        if amendment.get("kind") == "completion_contract":
            value = amendment["new_value"]
    return value


def effective_guards(record: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(record["guards"])
    for amendment in record.get("amendments", []):
        if amendment.get("kind") == "guards":
            value.update(copy.deepcopy(amendment["new_value"]))
    return value


def append_journal(
    record: MutableMapping[str, Any],
    kind: str,
    payload: Mapping[str, Any],
) -> str:
    if kind not in {"event", "step_receipt", "recovery", "amendment"}:
        raise RecordValidationError(f"invalid journal kind: {kind}")
    journal = record.setdefault("journal", [])
    prior_hash = journal[-1]["entry_hash"] if journal else None
    core = {
        "sequence": len(journal) + 1,
        "kind": kind,
        "payload": copy.deepcopy(dict(payload)),
        "prior_hash": prior_hash,
    }
    entry_hash = content_sha256(core)
    journal.append({**core, "entry_hash": entry_hash})
    return entry_hash


def validate_goal_record(record: Mapping[str, Any]) -> None:
    schema_version = record.get("schema_version")
    try:
        schema_name = GOAL_SCHEMA_FILES[schema_version]
    except (KeyError, TypeError) as error:
        raise RecordValidationError(
            f"unsupported goal schema version: {schema_version!r}"
        ) from error
    schema = Path(__file__).resolve().parents[3] / "schemas" / schema_name
    issues = validate_instance(record, schema)
    if issues:
        raise RecordValidationError(
            "goal record failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    if record["goal_text"] != canonical_goal_text(record["goal_text"]):
        raise RecordValidationError("goal text contains noncanonical line endings")
    if record["goal_sha256"] != goal_text_sha256(record["goal_text"]):
        raise RecordValidationError("goal text hash mismatch")
    if record["completion_contract_sha256"] != content_sha256(record["completion_contract"]):
        raise RecordValidationError("original completion contract hash mismatch")
    if record["state"]["last_canonical_fingerprint"] != record["state"][
        "canonical_fingerprint_history"
    ][-1]:
        raise RecordValidationError("last fingerprint does not match fingerprint history")
    terminal_phases = (
        V3_TERMINAL_PHASES
        if schema_version == GOAL_SCHEMA_VERSION
        else TERMINAL_PHASES
    )
    absorbing = (
        V3_TERMINAL_PHASES
        if schema_version == GOAL_SCHEMA_VERSION
        else ABSORBING_TERMINALS
    )
    if record["state"]["phase"] in absorbing and record["state"]["active_lease"]:
        raise RecordValidationError("absorbing terminal cannot retain a lease")
    if schema_version == GOAL_SCHEMA_VERSION:
        activation = record["activation"]
        profile = record["execution_profile"]
        if record["authorization"]["activation_receipt_sha256"] != content_sha256(
            activation
        ):
            raise RecordValidationError("activation receipt hash mismatch")
        if (
            activation["accepted_goal_sha256"] != record["goal_sha256"]
            or activation["accepted_completion_contract_sha256"]
            != record["completion_contract_sha256"]
            or profile["accepted_goal_sha256"] != record["goal_sha256"]
            or profile["accepted_completion_contract_sha256"]
            != record["completion_contract_sha256"]
            or profile["reasoning_effort"] != activation["reasoning_effort"]
            or profile["current_thread_effective_effort"]
            != profile["reasoning_effort"]
        ):
            raise RecordValidationError(
                "activation, execution profile, and immutable goal identity disagree"
            )
        topology = record["repository_topology_policy"]
        if topology["environment_mode"] != "reuse_bound_checkout":
            raise RecordValidationError("v3 goals must reuse the bound checkout")
        for key in (
            "branch_creation_authorized",
            "worktree_creation_authorized",
            "binding_change_authorized",
        ):
            if topology[key] and not topology["authorization_ref"]:
                raise RecordValidationError(
                    "repository topology authority requires an exact authorization reference"
                )
        phase = record["state"]["phase"]
        if phase == "terminal_complete":
            report = record["completion_report"]
            if (
                report is None
                or record["state"]["goal_evaluation"] != "met"
                or report["goal_id"] != record["goal_id"]
                or report["goal_sha256"] != record["goal_sha256"]
            ):
                raise RecordValidationError(
                    "terminal_complete requires a bound validated completion report"
                )
        elif phase in terminal_phases:
            human = record["human_intervention"]
            if (
                human is None
                or human["goal_id"] != record["goal_id"]
                or human["human_intervention_required"] is not True
            ):
                raise RecordValidationError(
                    "v3 non-success terminal requires a human-necessity report"
                )
        strategy_keys: set[tuple[str, str]] = set()
        for disposition in record["resolution_history"]:
            selected = disposition.get("selected_strategy_id")
            if not selected:
                continue
            key = (str(disposition["blocker_signature"]), str(selected))
            if key in strategy_keys:
                raise RecordValidationError(
                    "the same strategy cannot repeat against one blocker signature"
                )
            strategy_keys.add(key)
    effective_contract: Mapping[str, Any] = record["completion_contract"]
    effective_guard_values = copy.deepcopy(record["guards"])
    for amendment in record["amendments"]:
        if amendment["kind"] == "completion_contract":
            prior = content_sha256(effective_contract)
            effective_contract = amendment["new_value"]
            effective_new: Mapping[str, Any] = effective_contract
        else:
            prior = content_sha256(effective_guard_values)
            effective_guard_values.update(copy.deepcopy(amendment["new_value"]))
            effective_new = effective_guard_values
        if amendment["prior_effective_sha256"] != prior:
            raise RecordValidationError("amendment prior-effective hash mismatch")
        if amendment["new_sha256"] != content_sha256(effective_new):
            raise RecordValidationError("amendment new-effective hash mismatch")
    prior_hash = None
    receipts: set[int] = set()
    for sequence, entry in enumerate(record["journal"], 1):
        if entry["sequence"] != sequence or entry["prior_hash"] != prior_hash:
            raise RecordValidationError("journal sequence or prior hash mismatch")
        core = {key: entry[key] for key in ("sequence", "kind", "payload", "prior_hash")}
        if entry["entry_hash"] != content_sha256(core):
            raise RecordValidationError("journal entry hash mismatch")
        prior_hash = entry["entry_hash"]
        if entry["kind"] == "step_receipt":
            generation = entry["payload"].get("generation")
            if not isinstance(generation, int) or generation in receipts:
                raise RecordValidationError("generation has duplicate or invalid receipt")
            receipts.add(generation)
    for key, generation in record["generations"].items():
        if str(generation["generation"]) != key:
            raise RecordValidationError("generation key and payload mismatch")
        receipt_hash = generation.get("finalized_receipt_hash")
        journal_hash = next(
            (
                entry["entry_hash"]
                for entry in record["journal"]
                if entry["kind"] == "step_receipt"
                and entry["payload"].get("generation") == generation["generation"]
            ),
            None,
        )
        if receipt_hash != journal_hash:
            raise RecordValidationError("generation receipt link mismatch")
        if schema_version == GOAL_SCHEMA_VERSION:
            if generation["requested_reasoning_effort"] != record[
                "execution_profile"
            ]["reasoning_effort"]:
                raise RecordValidationError(
                    "generation requested effort differs from accepted profile"
                )
            if (
                generation["effective_reasoning_effort"] is not None
                and generation["effective_reasoning_effort"]
                != generation["requested_reasoning_effort"]
            ):
                raise RecordValidationError(
                    "generation effective effort differs from accepted profile"
                )


def transition_allowed(
    old_phase: str,
    new_phase: str,
    *,
    recovery: bool = False,
    schema_version: str | None = None,
) -> bool:
    if schema_version == GOAL_SCHEMA_VERSION:
        return (old_phase, new_phase) in V3_NORMAL_TRANSITIONS
    if recovery:
        return (
            old_phase in RECOVERABLE_TERMINALS and new_phase == "recovery_pending"
        ) or (
            old_phase == "recovery_pending"
            and new_phase
            in {
                "successor_created",
                "successor_intent",
                "continuation_required",
                *TERMINAL_PHASES,
            }
        )
    return (old_phase, new_phase) in NORMAL_TRANSITIONS
