"""Project-local manual handoff ThreadProvider and explicit adoption."""

from __future__ import annotations

import hashlib
import os
import stat
import tempfile
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.config import FORBIDDEN_STATE_ROOTS
from agentjob_runtime.errors import IntegrityError, RecordValidationError, SecurityError, StateConflict
from agentjob_runtime.goal.launcher import ThreadCreateResult
from agentjob_runtime.goal.model import utc_now
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_successor
from agentjob_runtime.records.canonical import content_sha256, load_structured, render_canonical_json
from agentjob_runtime.validation.schema import format_issues, validate_instance


def _safe_root(project_root: Path, local_root: str | Path) -> Path:
    supplied = Path(local_root)
    if supplied.is_absolute() or ".." in supplied.parts:
        raise SecurityError("manual handoff root must be project-relative")
    root = (project_root / supplied).resolve(strict=False)
    try:
        relative = root.relative_to(project_root).as_posix()
    except ValueError as error:
        raise SecurityError("manual handoff root escapes the project") from error
    if any(relative == value or relative.startswith(f"{value}/") for value in FORBIDDEN_STATE_ROOTS):
        raise SecurityError("manual handoff state cannot live in an installed package")
    current = project_root
    for part in Path(relative).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise SecurityError("manual handoff root traverses a symlink")
    return root


def _assert_regular(path: Path) -> None:
    if path.is_symlink():
        raise SecurityError(f"manual handoff file cannot be a symlink: {path}")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise SecurityError(f"manual handoff file has an unsafe alias: {path}")


def _atomic_write(path: Path, payload: bytes, *, allow_identical: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.parent
    while current != current.parent:
        if current.is_symlink():
            raise SecurityError(f"manual handoff path traverses a symlink: {current}")
        current = current.parent
    if path.exists():
        _assert_regular(path)
        if allow_identical and path.read_bytes() == payload:
            return
        raise IntegrityError(f"manual handoff artifact already exists: {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
    finally:
        if temporary.exists():
            temporary.unlink()


def _validate_envelope(envelope: Mapping[str, Any]) -> dict[str, Any]:
    value = dict(envelope)
    schema = Path(__file__).resolve().parents[3] / "schemas" / "continuation-envelope.schema.json"
    issues = validate_instance(value, schema)
    if issues:
        raise RecordValidationError(
            "manual handoff envelope failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    return value


class ManualThreadProvider:
    provider_id = "manual-handoff"
    available = True

    def __init__(
        self,
        project_root: str | Path,
        *,
        local_root: str | Path = ".local/sys4ai/continuation/manual",
        current_thread_id: str | None = None,
        timestamp: str | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        if not self.project_root.is_dir():
            raise RecordValidationError("manual handoff project root must exist")
        self.root = _safe_root(self.project_root, local_root)
        self.current_thread_id = current_thread_id
        self.timestamp = timestamp

    def capabilities(self) -> Mapping[str, Any]:
        return {
            "provider_id": self.provider_id,
            "available": True,
            "automatic": False,
            "strategies": ["manual_new_thread", "fresh_summary"],
            "operations": ["write_handoff", "explicit_adoption"],
            "protocol_idempotency": False,
        }

    def _directory(self, envelope: Mapping[str, Any]) -> Path:
        goal_id = str(envelope["goal_id"])
        generation = int(envelope["generation"])
        if any(char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._:-" for char in goal_id):
            raise SecurityError("manual handoff goal ID is unsafe for storage")
        return self.root / goal_id / f"generation-{generation}"

    def create_thread(
        self,
        *,
        prompt: str,
        envelope: Mapping[str, Any],
        idempotency_key: str,
    ) -> ThreadCreateResult:
        value = _validate_envelope(envelope)
        if idempotency_key != value["idempotency_key"]:
            raise StateConflict("manual handoff idempotency key differs from envelope")
        directory = self._directory(value)
        envelope_path = directory / "continuation-envelope.json"
        prompt_path = directory / "new-thread-prompt.txt"
        receipt_path = directory / "provider-receipt.json"
        envelope_payload = render_canonical_json(value).encode("utf-8")
        prompt_payload = prompt.encode("utf-8")
        receipt = {
            "schema_version": "sys4ai.manual-thread-provider-receipt.v1",
            "provider_id": self.provider_id,
            "status": "manual_handoff_pending",
            "goal_id": value["goal_id"],
            "generation": value["generation"],
            "idempotency_key": idempotency_key,
            "handoff_token_sha256": hashlib.sha256(
                str(value["handoff_token"]).encode("utf-8")
            ).hexdigest(),
            "envelope_sha256": content_sha256(value),
            "predecessor_thread_id": value["predecessor_thread_id"],
            "provider_thread_id": self.current_thread_id,
            "envelope_path": envelope_path.relative_to(self.project_root).as_posix(),
            "prompt_path": prompt_path.relative_to(self.project_root).as_posix(),
            "created_at": self.timestamp or utc_now(),
        }
        receipt_payload = render_canonical_json(receipt).encode("utf-8")
        _atomic_write(envelope_path, envelope_payload, allow_identical=True)
        _atomic_write(prompt_path, prompt_payload, allow_identical=True)
        if receipt_path.exists():
            _assert_regular(receipt_path)
            existing = load_structured(receipt_path)
            if not isinstance(existing, Mapping):
                raise IntegrityError("manual provider receipt is not an object")
            comparable = dict(existing)
            comparable.pop("created_at", None)
            expected = dict(receipt)
            expected.pop("created_at", None)
            if comparable != expected:
                raise IntegrityError("manual provider receipt conflicts with existing intent")
        else:
            _atomic_write(receipt_path, receipt_payload)
        response = {
            "status": "manual_handoff_pending",
            "envelope_path": receipt["envelope_path"],
            "prompt_path": receipt["prompt_path"],
            "receipt_path": receipt_path.relative_to(self.project_root).as_posix(),
            "envelope_sha256": receipt["envelope_sha256"],
        }
        return ThreadCreateResult("manual_pending", None, response)


def adopt_manual_successor(
    store: SQLiteGoalStore,
    *,
    project_root: str | Path,
    local_root: str | Path,
    goal_id: str,
    expected_revision: int,
    generation: int,
    handoff_token: str,
    envelope_sha256: str,
    successor_thread_id: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Adopt one explicitly created fresh thread using the reserved identity."""

    root = Path(project_root).expanduser().resolve()
    manual_root = _safe_root(root, local_root)
    directory = manual_root / goal_id / f"generation-{generation}"
    envelope_path = directory / "continuation-envelope.json"
    receipt_path = directory / "provider-receipt.json"
    for path in (envelope_path, receipt_path):
        if not path.is_file():
            raise RecordValidationError(f"manual handoff artifact is missing: {path}")
        _assert_regular(path)
    envelope = _validate_envelope(load_structured(envelope_path))
    receipt = load_structured(receipt_path)
    if not isinstance(receipt, Mapping):
        raise RecordValidationError("manual provider receipt must be an object")
    if (
        envelope["goal_id"] != goal_id
        or envelope["generation"] != generation
        or envelope["handoff_token"] != handoff_token
        or content_sha256(envelope) != envelope_sha256
        or receipt.get("envelope_sha256") != envelope_sha256
    ):
        raise StateConflict("manual adoption token, generation, goal, or envelope mismatch")
    forbidden_threads = {
        value
        for value in (
            envelope.get("predecessor_thread_id"),
            receipt.get("provider_thread_id"),
        )
        if value
    }
    if not successor_thread_id.strip() or successor_thread_id in forbidden_threads:
        raise StateConflict("manual adoption requires a distinct fresh successor thread")
    record = record_successor(
        store,
        goal_id=goal_id,
        expected_revision=expected_revision,
        generation=generation,
        handoff_token=handoff_token,
        successor_thread_id=successor_thread_id,
        provider_id="manual-handoff",
        provider_response={
            "status": "manually_adopted",
            "receipt_path": receipt_path.relative_to(root).as_posix(),
            "envelope_sha256": envelope_sha256,
        },
        timestamp=timestamp,
    )
    successor_digest = hashlib.sha256(successor_thread_id.encode("utf-8")).hexdigest()[:16]
    adoption_path = directory / f"adoption-{successor_digest}.json"
    adoption = {
        "schema_version": "sys4ai.manual-thread-adoption.v1",
        "goal_id": goal_id,
        "generation": generation,
        "successor_thread_id": successor_thread_id,
        "envelope_sha256": envelope_sha256,
        "adopted_at": timestamp or utc_now(),
    }
    if adoption_path.exists():
        _assert_regular(adoption_path)
        existing = load_structured(adoption_path)
        if not isinstance(existing, Mapping):
            raise IntegrityError("manual adoption receipt is not an object")
        comparable = dict(existing)
        comparable.pop("adopted_at", None)
        expected = dict(adoption)
        expected.pop("adopted_at", None)
        if comparable != expected:
            raise IntegrityError("manual adoption conflicts with existing receipt")
    else:
        _atomic_write(adoption_path, render_canonical_json(adoption).encode("utf-8"))
    return record
