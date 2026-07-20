"""Strict, immutable reader for AEther ``continue-research-goal.v1`` records."""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import re
import stat
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import IntegrityError, RecordValidationError


SCHEMA_VERSION = "continue-research-goal.v1"
GOAL_ID_RE = re.compile(r"crg-[0-9]{8}T[0-9]{6}Z-[a-f0-9]+")
EXECUTION_PROFILES = {"acceptance_test", "production_profile"}
NONTERMINAL_PHASES = {
    "initialized",
    "successor_intent",
    "successor_created",
    "step_active",
    "step_verifying",
    "step_verified",
    "continuation_required",
    "recovery_pending",
}
TERMINAL_PHASES = {
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
PHASES = NONTERMINAL_PHASES | TERMINAL_PHASES
RECOVERABLE_TERMINALS = {
    "terminal_awaiting_human",
    "terminal_capability_blocked",
    "terminal_guard_exhausted",
    "terminal_no_progress",
    "terminal_validation_failed",
    "terminal_handoff_ambiguous",
    "terminal_handoff_timeout",
    "terminal_failed",
}
ABSORBING_TERMINALS = TERMINAL_PHASES - RECOVERABLE_TERMINALS
INVOCATION_STATES = {"not_authorized", "authorized", "returned", "unknown"}


class LegacyGoalReadOnlyError(IntegrityError):
    code = "aether.legacy_goal_read_only"


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _canonical_goal_text(value: str) -> str:
    if not isinstance(value, str):
        raise RecordValidationError("legacy goal text must be a string")
    return value.replace("\r\n", "\n").replace("\r", "\n")


def _goal_text_sha256(value: str) -> str:
    return hashlib.sha256(_canonical_goal_text(value).encode("utf-8")).hexdigest()


def _parse_utc(value: Any, field: str) -> dt.datetime:
    if not isinstance(value, str) or not value:
        raise RecordValidationError(f"legacy goal field {field} must be a UTC timestamp")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise RecordValidationError(f"legacy goal field {field} is not a timestamp") from error
    if parsed.tzinfo is None:
        raise RecordValidationError(f"legacy goal field {field} lacks timezone information")
    return parsed


def effective_completion_contract(record: Mapping[str, Any]) -> Mapping[str, Any]:
    value: Mapping[str, Any] = record["completion_contract"]
    for amendment in record.get("amendments", []):
        if amendment.get("kind") == "completion_contract":
            candidate = amendment.get("new_value")
            if not isinstance(candidate, Mapping):
                raise RecordValidationError("legacy completion-contract amendment is not a mapping")
            value = candidate
    return value


def render_legacy_goal(record: Mapping[str, Any]) -> str:
    """Reproduce the legacy helper's canonical Markdown serialization."""

    frontmatter = json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2)
    contract = json.dumps(effective_completion_contract(record), ensure_ascii=False, sort_keys=True, indent=2)
    lines = [
        "---",
        frontmatter,
        "---",
        "",
        "# Goal relay record",
        "",
        "## Completion contract",
        "",
        "```json",
        contract,
        "```",
        "",
        "## Step journal",
        "",
    ]
    journal = record.get("journal", [])
    if not journal:
        lines.append("_No journal entries._")
    else:
        for entry in journal:
            lines.extend(
                [
                    f"### {entry['sequence']}. {entry['kind']}",
                    "",
                    f"- Prior hash: `{entry['prior_hash'] or 'GENESIS'}`",
                    f"- Entry hash: `{entry['entry_hash']}`",
                    "",
                    "```json",
                    json.dumps(entry["payload"], ensure_ascii=False, sort_keys=True, indent=2),
                    "```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def parse_legacy_goal_text(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise RecordValidationError("legacy goal lacks the frontmatter opener")
    frontmatter, separator, body = text[4:].partition("\n---\n")
    if not separator:
        raise RecordValidationError("legacy goal lacks the frontmatter closer")
    try:
        value = json.loads(frontmatter)
    except json.JSONDecodeError as error:
        raise RecordValidationError("legacy goal frontmatter is not JSON") from error
    if not isinstance(value, dict):
        raise RecordValidationError("legacy goal frontmatter must be an object")
    return value, body


def _validate_journal(record: Mapping[str, Any]) -> dict[int, str]:
    journal = record.get("journal")
    if not isinstance(journal, list):
        raise RecordValidationError("legacy goal journal must be a list")
    prior: str | None = None
    receipts: dict[int, str] = {}
    for sequence, entry in enumerate(journal, start=1):
        if not isinstance(entry, Mapping):
            raise RecordValidationError("legacy goal journal entry must be an object")
        if entry.get("sequence") != sequence or entry.get("prior_hash") != prior:
            raise RecordValidationError("legacy journal sequence or prior hash mismatch")
        try:
            core = {key: entry[key] for key in ("kind", "payload", "prior_hash", "sequence")}
        except KeyError as error:
            raise RecordValidationError("legacy journal entry lacks a hash field") from error
        expected_hash = _sha256_json(core)
        if entry.get("entry_hash") != expected_hash:
            raise RecordValidationError("legacy journal entry hash mismatch")
        prior = expected_hash
        if entry["kind"] == "step_receipt":
            payload = entry.get("payload")
            generation = payload.get("generation") if isinstance(payload, Mapping) else None
            if not isinstance(generation, int) or generation in receipts:
                raise RecordValidationError("legacy goal has a duplicate or invalid generation receipt")
            receipts[generation] = expected_hash
    return receipts


def _validate_generations(record: Mapping[str, Any], receipts: Mapping[int, str]) -> None:
    generations = record.get("generations")
    if not isinstance(generations, Mapping):
        raise RecordValidationError("legacy goal generations must be an object")
    for key, generation in generations.items():
        try:
            number = int(key)
        except (TypeError, ValueError) as error:
            raise RecordValidationError("legacy generation keys must be decimal integers") from error
        if number <= 0 or not isinstance(generation, Mapping) or generation.get("generation") != number:
            raise RecordValidationError("legacy generation key and payload mismatch")
        if generation.get("invocation_state") not in INVOCATION_STATES:
            raise RecordValidationError("legacy generation invocation_state is invalid")
        if not isinstance(generation.get("invocation_consumed"), bool):
            raise RecordValidationError("legacy generation invocation_consumed must be Boolean")
        receipt_hash = generation.get("finalized_receipt_hash")
        if receipt_hash is not None and receipts.get(number) != receipt_hash:
            raise RecordValidationError("legacy finalized receipt hash does not match the journal")
        if receipt_hash is None and number in receipts:
            raise RecordValidationError("legacy journal receipt is not linked from its generation")


def _validate_amendments(record: Mapping[str, Any]) -> None:
    amendments = record.get("amendments")
    if not isinstance(amendments, list):
        raise RecordValidationError("legacy goal amendments must be a list")
    contract: Any = copy.deepcopy(record["completion_contract"])
    guards: Any = copy.deepcopy(record["guards"])
    for amendment in amendments:
        if not isinstance(amendment, Mapping):
            raise RecordValidationError("legacy goal amendment must be an object")
        kind = amendment.get("kind")
        if kind == "completion_contract":
            prior = _sha256_json(contract)
            contract = amendment.get("new_value")
            effective = contract
        elif kind == "guards":
            prior = _sha256_json(guards)
            delta = amendment.get("new_value")
            if not isinstance(delta, Mapping):
                raise RecordValidationError("legacy guard amendment must be an object")
            guards.update(copy.deepcopy(delta))
            effective = guards
        else:
            raise RecordValidationError("legacy goal amendment kind is invalid")
        if amendment.get("prior_effective_sha256") != prior:
            raise RecordValidationError("legacy amendment prior hash mismatch")
        if amendment.get("new_sha256") != _sha256_json(effective):
            raise RecordValidationError("legacy amendment new hash mismatch")
        if not amendment.get("user_authorization"):
            raise RecordValidationError("legacy amendment lacks exact user authorization")
        _parse_utc(amendment.get("created_at"), "amendments.created_at")


def validate_legacy_goal(
    record: Mapping[str, Any],
    *,
    expected_path: Path | None = None,
    rendered_text: str | None = None,
) -> None:
    required = {
        "schema_version",
        "goal_id",
        "goal_text",
        "goal_sha256",
        "completion_contract",
        "completion_contract_sha256",
        "amendments",
        "created_at",
        "deadline_at",
        "guards",
        "repository_binding",
        "authorization",
        "state",
        "generations",
        "handoff",
        "journal",
        "updated_at",
    }
    missing = sorted(required - set(record))
    if missing:
        raise RecordValidationError(f"legacy goal is missing fields: {', '.join(missing)}")
    if record["schema_version"] != SCHEMA_VERSION:
        raise RecordValidationError("legacy goal schema version is unsupported")
    goal_id = str(record["goal_id"])
    if not GOAL_ID_RE.fullmatch(goal_id):
        raise RecordValidationError("legacy goal_id is invalid")
    if expected_path is not None and expected_path.name != f"goal-{goal_id}.md":
        raise RecordValidationError("legacy goal filename does not match goal_id")
    goal_text = record["goal_text"]
    if goal_text != _canonical_goal_text(goal_text):
        raise RecordValidationError("legacy goal text has noncanonical line endings")
    if record["goal_sha256"] != _goal_text_sha256(goal_text):
        raise RecordValidationError("legacy goal text hash mismatch")
    if not isinstance(record["completion_contract"], Mapping):
        raise RecordValidationError("legacy completion contract must be an object")
    if record["completion_contract_sha256"] != _sha256_json(record["completion_contract"]):
        raise RecordValidationError("legacy completion-contract hash mismatch")
    created = _parse_utc(record["created_at"], "created_at")
    deadline = _parse_utc(record["deadline_at"], "deadline_at")
    _parse_utc(record["updated_at"], "updated_at")
    if deadline <= created:
        raise RecordValidationError("legacy deadline must be after creation")

    guards = record["guards"]
    if not isinstance(guards, Mapping):
        raise RecordValidationError("legacy guards must be an object")
    for key in (
        "max_continue_passes",
        "max_repeated_state_fingerprints",
        "max_live_continuations",
        "handoff_ready_timeout_seconds",
    ):
        if not isinstance(guards.get(key), int) or guards[key] <= 0:
            raise RecordValidationError(f"legacy guard {key} must be a positive integer")

    binding = record["repository_binding"]
    if not isinstance(binding, Mapping):
        raise RecordValidationError("legacy repository binding must be an object")
    for key in (
        "execution_profile",
        "root",
        "branch",
        "environment_mode",
        "git_common_dir",
        "starting_head",
    ):
        if not isinstance(binding.get(key), str) or not binding[key]:
            raise RecordValidationError(f"legacy repository binding field {key} is blank")
    if binding["execution_profile"] not in EXECUTION_PROFILES:
        raise RecordValidationError("legacy repository execution profile is unsupported")
    if binding["environment_mode"] != "local":
        raise RecordValidationError("legacy goal supports only local environment mode")
    if binding["branch"] == "main":
        raise RecordValidationError("legacy production relay cannot bind main")

    state = record["state"]
    if not isinstance(state, Mapping) or state.get("phase") not in PHASES:
        raise RecordValidationError("legacy goal phase is invalid")
    if not isinstance(state.get("revision"), int) or state["revision"] < 1:
        raise RecordValidationError("legacy goal revision must be positive")
    if not isinstance(state.get("current_generation"), int) or state["current_generation"] < 0:
        raise RecordValidationError("legacy current_generation must be nonnegative")
    if not isinstance(state.get("passes_consumed"), int) or state["passes_consumed"] < 0:
        raise RecordValidationError("legacy passes_consumed must be nonnegative")
    if state.get("goal_evaluation") not in {"unmet", "met", "indeterminate"}:
        raise RecordValidationError("legacy goal evaluation is invalid")
    if state["phase"] in ABSORBING_TERMINALS and state.get("active_lease") is not None:
        raise RecordValidationError("legacy absorbing terminal cannot retain a lease")

    receipts = _validate_journal(record)
    _validate_generations(record, receipts)
    _validate_amendments(record)
    if rendered_text is not None and render_legacy_goal(record) != rendered_text:
        raise RecordValidationError("legacy goal Markdown body or serialization drifted")


def export_legacy_goal(record: Mapping[str, Any], *, source_sha256: str | None = None) -> dict[str, Any]:
    """Create a derived portable view without changing the historical record."""

    state = record["state"]
    receipts = [
        {
            "generation": entry["payload"].get("generation"),
            "entry_hash": entry["entry_hash"],
            "payload": copy.deepcopy(entry["payload"]),
        }
        for entry in record["journal"]
        if entry.get("kind") == "step_receipt"
    ]
    return {
        "schema_version": "sys4ai.aether-legacy-goal-view.v1",
        "source_schema_version": record["schema_version"],
        "legacy_goal_id": record["goal_id"],
        "portable_goal_id": record["goal_id"],
        "read_only": True,
        "mutation_supported": False,
        "goal_text": record["goal_text"],
        "goal_sha256": record["goal_sha256"],
        "completion_contract": copy.deepcopy(effective_completion_contract(record)),
        "state": {
            "legacy_phase": state["phase"],
            "portable_status": (
                "terminal" if state["phase"] in TERMINAL_PHASES else "active"
            ),
            "revision": state["revision"],
            "current_generation": state["current_generation"],
            "passes_consumed": state["passes_consumed"],
            "goal_evaluation": state["goal_evaluation"],
            "terminal_reason": state.get("terminal_reason"),
        },
        "generation_receipts": receipts,
        "repository_binding": copy.deepcopy(record["repository_binding"]),
        "source_sha256": source_sha256,
        "authority_note": (
            "This is an export-only reader view. The historical legacy record remains "
            "the identity and evidence source and must not be rewritten."
        ),
    }


def read_legacy_goal(path: str | Path) -> dict[str, Any]:
    """Read, verify, and export one historical record without opening it for write."""

    candidate = Path(path).absolute()
    if candidate.is_symlink():
        raise IntegrityError("legacy goal path may not be a symlink")
    try:
        metadata = candidate.lstat()
    except FileNotFoundError as error:
        raise RecordValidationError("legacy goal file does not exist") from error
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
        raise IntegrityError("legacy goal must be one regular file with one hard link")
    before = candidate.read_bytes()
    try:
        text = before.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RecordValidationError("legacy goal is not UTF-8") from error
    record, _ = parse_legacy_goal_text(text)
    validate_legacy_goal(record, expected_path=candidate, rendered_text=text)
    after = candidate.read_bytes()
    if after != before:
        raise IntegrityError("legacy goal changed during the read-only operation")
    source_sha256 = hashlib.sha256(before).hexdigest()
    return {
        "legacy": True,
        "read_only": True,
        "record": record,
        "sha256": source_sha256,
        "portable_view": export_legacy_goal(record, source_sha256=source_sha256),
    }


def reject_legacy_write(*_args: Any, **_kwargs: Any) -> None:
    raise LegacyGoalReadOnlyError(
        "legacy AEther goal records are historical reader-only evidence",
        details={"reason_code": "aether.legacy_goal_read_only"},
    )
