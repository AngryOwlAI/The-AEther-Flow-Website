"""Human-readable, hash-linked compatibility backend for durable goal state."""

from __future__ import annotations

import copy
import json
import os
import secrets
import stat
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping

from agentjob_runtime.errors import ActiveRelayError, IntegrityError, RecordNotFound, StateConflict
from agentjob_runtime.goal.locking import CrossPlatformFileLock, LockBackend
from agentjob_runtime.goal.model import (
    LEASE_SCHEMA_VERSION,
    append_journal,
    goal_text_sha256,
    repository_identity_hash,
    utc_now,
    validate_goal_record,
)
from agentjob_runtime.records.canonical import canonical_json_bytes


def render_goal(record: Mapping[str, Any]) -> str:
    frontmatter = json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2)
    return (
        "---\n"
        + frontmatter
        + "\n---\n\n"
        + "# Durable goal relay snapshot\n\n"
        + f"- Goal: `{record['goal_id']}`\n"
        + f"- Revision: `{record['state']['revision']}`\n"
        + f"- Phase: `{record['state']['phase']}`\n"
        + f"- Journal entries: `{len(record['journal'])}`\n"
    )


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        raise IntegrityError("goal file lacks a frontmatter opener")
    frontmatter, separator, _ = text[4:].partition("\n---\n")
    if not separator:
        raise IntegrityError("goal file lacks a frontmatter closer")
    try:
        value = json.loads(frontmatter)
    except json.JSONDecodeError as error:
        raise IntegrityError("goal frontmatter is not valid deterministic JSON") from error
    if not isinstance(value, dict):
        raise IntegrityError("goal frontmatter must be an object")
    return value


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _exclusive_write(path: Path, data: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)
    _fsync_directory(path.parent)


def _atomic_write(path: Path, data: bytes) -> None:
    temporary = path.with_name(f"{path.name}.{secrets.token_hex(8)}.tmp")
    try:
        _exclusive_write(temporary, data)
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


@dataclass
class FileGoalMutation:
    record: dict[str, Any]
    timestamp: str

    def event(self, event_type: str, payload: Mapping[str, Any] | None = None) -> str:
        body = {"event_type": event_type, **copy.deepcopy(dict(payload or {}))}
        body.setdefault("timestamp", self.timestamp)
        return append_journal(self.record, "event", body)

    def recovery(
        self,
        action: str,
        *,
        user_authorization: str,
        evidence: Mapping[str, Any],
        prior_phase: str,
        resulting_phase: str,
    ) -> str:
        return append_journal(
            self.record,
            "recovery",
            {
                "recovery_action": action,
                "user_authorization": user_authorization,
                "evidence": copy.deepcopy(dict(evidence)),
                "prior_phase": prior_phase,
                "resulting_phase": resulting_phase,
                "timestamp": self.timestamp,
            },
        )

    def amendment(self, amendment: Mapping[str, Any]) -> str:
        return append_journal(self.record, "amendment", amendment)

    def receipt(self, payload: Mapping[str, Any]) -> str:
        return append_journal(self.record, "step_receipt", payload)

    def provider_receipt(
        self,
        *,
        generation: int,
        provider_id: str,
        idempotency_key: str,
        provider_status: str,
        returned_thread_id: str | None,
        response: Mapping[str, Any],
    ) -> None:
        for entry in self.record["journal"]:
            payload = entry["payload"]
            if (
                entry["kind"] == "event"
                and payload.get("event_type") == "provider_receipt"
                and payload.get("provider_id") == provider_id
                and payload.get("idempotency_key") == idempotency_key
            ):
                raise StateConflict("provider receipt already exists for this idempotency key")
        self.event(
            "provider_receipt",
            {
                "generation": generation,
                "provider_id": provider_id,
                "idempotency_key": idempotency_key,
                "provider_status": provider_status,
                "returned_thread_id": returned_thread_id,
                "response": copy.deepcopy(dict(response)),
            },
        )

    def replace_lease(
        self,
        *,
        generation: int,
        holder_kind: str,
        holder_token: str,
        expires_at: str,
    ) -> dict[str, Any]:
        prior = self.record["state"].get("active_lease")
        lease = {
            "repository_fingerprint": repository_identity_hash(self.record["repository_binding"]),
            "goal_id": self.record["goal_id"],
            "generation": generation,
            "holder_kind": holder_kind,
            "holder_token": holder_token,
            "transaction_id": secrets.token_hex(16),
            "acquired_at": prior["acquired_at"] if prior else self.timestamp,
            "heartbeat_at": self.timestamp,
            "expires_at": expires_at,
        }
        self.record["state"]["active_lease"] = lease
        return lease

    def release_lease(self) -> None:
        self.record["state"]["active_lease"] = None

    def heartbeat(self, *, expires_at: str) -> None:
        lease = self.record["state"].get("active_lease")
        if lease is None:
            raise StateConflict("goal has no active lease")
        lease["heartbeat_at"] = self.timestamp
        lease["expires_at"] = expires_at


class FileJournalGoalStore:
    """Compatibility store with the same mutation interface as SQLiteGoalStore."""

    def __init__(
        self,
        root: str | Path,
        *,
        lock_backend: LockBackend = "auto",
        lock_timeout_seconds: float = 5.0,
    ) -> None:
        supplied = Path(root).expanduser().absolute()
        supplied.mkdir(parents=True, exist_ok=True)
        if supplied.is_symlink():
            raise IntegrityError("file-journal root may not be a symlink")
        self.root = supplied.resolve()
        self.lock_backend = lock_backend
        self.lock_timeout_seconds = lock_timeout_seconds
        self.global_lease_path = self.root / "worktree-lease.json"
        self.lock_path = self.root / ".goal-journal.lock"

    def _lock(self) -> CrossPlatformFileLock:
        return CrossPlatformFileLock(
            self.lock_path,
            backend=self.lock_backend,
            timeout_seconds=self.lock_timeout_seconds,
        )

    def _path(self, goal_id: str, *, must_exist: bool = True) -> Path:
        if not goal_id or any(character in goal_id for character in ("/", "\\", os.sep)):
            raise IntegrityError("goal ID cannot contain path separators")
        path = self.root / f"goal-{goal_id}.md"
        if path.parent != self.root:
            raise IntegrityError("goal path must be a direct child of the journal root")
        if must_exist:
            try:
                metadata = path.lstat()
            except FileNotFoundError as error:
                raise RecordNotFound(f"goal does not exist: {goal_id}") from error
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                raise IntegrityError("goal path must be a regular non-symlink file")
            if metadata.st_nlink != 1:
                raise IntegrityError("goal file must have exactly one hard link")
            if path.resolve().parent != self.root:
                raise IntegrityError("goal path escapes the journal root")
        return path

    def _read_global_lease(self) -> dict[str, Any] | None:
        if not self.global_lease_path.exists():
            return None
        metadata = self.global_lease_path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise IntegrityError("global lease must be one regular non-symlink file")
        try:
            value = json.loads(self.global_lease_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise IntegrityError("global lease is unreadable or corrupt") from error
        if value.pop("schema_version", None) != LEASE_SCHEMA_VERSION:
            raise IntegrityError("global lease schema is unsupported")
        return value

    def _write_global_lease(self, lease: Mapping[str, Any] | None) -> None:
        if lease is None:
            try:
                self.global_lease_path.unlink()
            except FileNotFoundError:
                return
            _fsync_directory(self.root)
            return
        payload = {"schema_version": LEASE_SCHEMA_VERSION, **copy.deepcopy(dict(lease))}
        _atomic_write(self.global_lease_path, canonical_json_bytes(payload) + b"\n")

    @staticmethod
    def _validate_lease_parity(record: Mapping[str, Any], global_lease: Mapping[str, Any] | None) -> None:
        lease = record["state"].get("active_lease")
        if lease is None and global_lease is None:
            return
        if lease is None and global_lease is not None and global_lease.get("goal_id") != record["goal_id"]:
            return
        if lease is None or global_lease is None:
            raise IntegrityError(
                "goal/global lease mismatch requires quarantine and explicit recovery",
                details={"recovery_required": True},
            )
        if lease != global_lease:
            raise IntegrityError(
                "goal/global lease identity mismatch requires quarantine and explicit recovery",
                details={"recovery_required": True},
            )

    def _load_unlocked(self, goal_id: str) -> dict[str, Any]:
        path = self._path(goal_id)
        text = path.read_text(encoding="utf-8")
        record = parse_frontmatter(text)
        validate_goal_record(record)
        if path.name != f"goal-{record['goal_id']}.md":
            raise IntegrityError("goal filename and embedded identity disagree")
        if text != render_goal(record):
            raise IntegrityError("rendered snapshot drift detected")
        self._validate_lease_parity(record, self._read_global_lease())
        return record

    def load_goal(self, goal_id: str) -> dict[str, Any]:
        with self._lock():
            return self._load_unlocked(goal_id)

    def list_goals(self) -> list[dict[str, Any]]:
        with self._lock():
            rows = []
            for path in sorted(self.root.glob("goal-*.md")):
                record = self._load_unlocked(path.name[5:-3])
                rows.append(
                    {
                        "goal_id": record["goal_id"],
                        "revision": record["state"]["revision"],
                        "phase": record["state"]["phase"],
                        "current_generation": record["state"]["current_generation"],
                        "passes_consumed": record["state"]["passes_consumed"],
                    }
                )
            return rows

    def create_goal(self, record: Mapping[str, Any]) -> dict[str, Any]:
        candidate = copy.deepcopy(dict(record))
        validate_goal_record(candidate)
        path = self._path(candidate["goal_id"], must_exist=False)
        with self._lock():
            if path.exists():
                raise StateConflict("goal ID already exists")
            global_lease = self._read_global_lease()
            if global_lease is not None:
                raise ActiveRelayError("another relay owns the repository worktree")
            for existing in self.root.glob("goal-*.md"):
                value = parse_frontmatter(existing.read_text(encoding="utf-8"))
                if value["state"].get("active_lease") is not None:
                    raise ActiveRelayError("an unreconciled per-goal lease exists")
            try:
                _exclusive_write(path, render_goal(candidate).encode("utf-8"))
                self._write_global_lease(candidate["state"].get("active_lease"))
            except Exception:
                if path.exists() and self.global_lease_path.exists() is False:
                    path.unlink()
                raise
            return copy.deepcopy(candidate)

    @contextmanager
    def mutation(
        self,
        goal_id: str,
        *,
        expected_revision: int,
        timestamp: str | None = None,
    ) -> Iterator[FileGoalMutation]:
        with self._lock():
            record = self._load_unlocked(goal_id)
            actual = record["state"]["revision"]
            if actual != expected_revision:
                raise StateConflict(
                    f"stale goal revision: expected {expected_revision}, found {actual}",
                    details={"expected_revision": expected_revision, "actual_revision": actual},
                )
            mutation = FileGoalMutation(record, timestamp or utc_now())
            yield mutation
            record["state"]["revision"] = expected_revision + 1
            record["updated_at"] = mutation.timestamp
            validate_goal_record(record)
            path = self._path(goal_id)
            _atomic_write(path, render_goal(record).encode("utf-8"))
            self._write_global_lease(record["state"].get("active_lease"))
            self._validate_lease_parity(record, self._read_global_lease())

    def read_legacy_aether(self, path: str | Path) -> dict[str, Any]:
        """Read a strict historical record through the compatibility reader."""

        from agentjob_runtime.compat.aether_goal_v1 import read_legacy_goal

        candidate = Path(path).absolute()
        if candidate.parent.resolve() != self.root:
            raise IntegrityError("legacy goal must be a direct child of the goal store")
        return read_legacy_goal(candidate)
