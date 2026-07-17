"""Safe filesystem store for tracked portable control records."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping, MutableMapping

from agentjob_runtime.errors import IntegrityError, RecordNotFound, RecordValidationError, SecurityError, StateConflict
from agentjob_runtime.records.canonical import load_structured, render_canonical_json
from agentjob_runtime.validation.schema import format_issues, validate_instance


SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{1,159}$")
SCHEMA_FILES = {
    "task": "task.schema.json",
    "director_decision": "director-decision.schema.json",
    "agent_job": "agent-job.schema.json",
    "execution_role": "execution-role.schema.json",
    "completion": "completion.schema.json",
    "handoff": "handoff.schema.json",
    "activation": "activation.schema.json",
    "supersession": "supersession.schema.json",
}
SCHEMA_VERSIONS = {
    "sys4ai.task.v1": "task",
    "sys4ai.director-decision.v1": "director_decision",
    "sys4ai.agent-job.v1": "agent_job",
    "sys4ai.execution-role.v1": "execution_role",
    "sys4ai.completion.v1": "completion",
    "sys4ai.handoff.v1": "handoff",
    "sys4ai.activation.v1": "activation",
    "sys4ai.supersession.v1": "supersession",
}


@dataclass(frozen=True)
class WriteReceipt:
    relative_path: str
    bytes_written: int
    created: bool


def _safe_identifier(value: str, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID.fullmatch(value):
        raise SecurityError(
            f"invalid {label}: {value!r}", details={"reason_code": "path.identifier_invalid"}
        )
    return value


class FilesystemControlStore:
    """Store canonical records under one project-declared control root."""

    def __init__(self, project_root: str | Path, control_root: str | Path) -> None:
        self.project_root = Path(project_root).resolve()
        root = Path(control_root)
        self.root = root.resolve() if root.is_absolute() else (self.project_root / root).resolve()
        try:
            self.root.relative_to(self.project_root)
        except ValueError as error:
            raise SecurityError("control root must remain within the project root") from error
        self.schema_root = Path(__file__).resolve().parents[3] / "schemas"

    @property
    def staging_root(self) -> Path:
        return self.root / ".staging"

    @property
    def indexes_root(self) -> Path:
        return self.root / "indexes"

    def initialize_layout(self) -> None:
        for path in [self.root, self.root / "tasks", self.root / "handoffs", self.indexes_root, self.staging_root]:
            self._ensure_directory(path)

    def _ensure_directory(self, path: Path) -> None:
        safe = self._resolve_within_root(path)
        current = self.root
        if self.root.exists() and self.root.is_symlink():
            raise SecurityError(f"control root cannot be a symlink: {self.root}")
        if not self.root.exists():
            self.root.mkdir(parents=True, mode=0o700)
        relative = safe.relative_to(self.root)
        for part in relative.parts:
            current = current / part
            if current.exists():
                if current.is_symlink() or not current.is_dir():
                    raise SecurityError(f"control directory component is unsafe: {current}")
            else:
                current.mkdir(mode=0o700)
        try:
            os.chmod(safe, 0o700)
        except OSError:
            pass

    def _resolve_within_root(self, value: str | Path) -> Path:
        path = Path(value)
        candidate = path.resolve(strict=False) if path.is_absolute() else (self.root / path).resolve(strict=False)
        try:
            candidate.relative_to(self.root)
        except ValueError as error:
            raise SecurityError(
                f"control path escapes root: {value}", details={"reason_code": "path.traversal"}
            ) from error
        return candidate

    def _assert_safe_existing(self, path: Path, *, expect_file: bool = True) -> None:
        current = self.root
        for part in path.relative_to(self.root).parts:
            current = current / part
            if current.is_symlink():
                raise SecurityError(
                    f"control path traverses symlink: {current}", details={"reason_code": "path.symlink"}
                )
        if not path.exists():
            raise RecordNotFound(f"record does not exist: {path}")
        info = path.stat()
        if expect_file and not stat.S_ISREG(info.st_mode):
            raise SecurityError(f"record is not a regular file: {path}")
        if expect_file and info.st_nlink != 1:
            raise SecurityError(
                f"record has a hard-link alias: {path}", details={"reason_code": "path.hardlink"}
            )

    def relative(self, path: str | Path) -> str:
        resolved = self._resolve_within_root(path)
        return resolved.relative_to(self.project_root).as_posix()

    def task_directory(self, task_id: str) -> Path:
        return self.root / "tasks" / _safe_identifier(task_id, "task id")

    def task_path(self, task_id: str) -> Path:
        return self.task_directory(task_id) / "task.json"

    def record_path(self, kind: str, task_id: str, record_id: str) -> Path:
        task_root = self.task_directory(task_id)
        record_id = _safe_identifier(record_id, f"{kind} id")
        mapping = {
            "director_decision": task_root / "decisions" / f"{record_id}.json",
            "agent_job": task_root / "jobs" / f"{record_id}.json",
            "execution_role": task_root / "roles" / f"{record_id}.json",
            "completion": task_root / "completions" / f"{record_id}.json",
            "activation": task_root / "activations" / f"{record_id}.json",
            "supersession": task_root / "supersessions" / f"{record_id}.json",
            "handoff": self.root / "handoffs" / f"{record_id}.json",
        }
        if kind not in mapping:
            raise ValueError(f"unsupported record kind: {kind}")
        return mapping[kind]

    def validate_record(self, kind: str, record: Mapping[str, Any]) -> None:
        schema_name = SCHEMA_FILES[kind]
        issues = validate_instance(record, self.schema_root / schema_name)
        if issues:
            raise RecordValidationError(
                f"{kind} record failed schema validation",
                details={"reason_code": "record.schema_invalid", "findings": format_issues(issues).splitlines()},
            )

    def read(self, path: str | Path) -> dict[str, Any]:
        resolved = self._resolve_within_root(path)
        self._assert_safe_existing(resolved)
        value = load_structured(resolved)
        if not isinstance(value, dict):
            raise RecordValidationError(f"record must be a mapping: {resolved}")
        return value

    def _atomic_write(self, path: Path, payload: bytes) -> None:
        path = self._resolve_within_root(path)
        self._ensure_directory(path.parent)
        if path.exists() and path.is_symlink():
            raise SecurityError(f"refusing to replace symlink: {path}")
        temporary = path.parent / f".{path.name}.{uuid.uuid4().hex}.tmp"
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, "wb", closefd=True) as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
            try:
                descriptor_dir = os.open(path.parent, os.O_RDONLY)
                try:
                    os.fsync(descriptor_dir)
                finally:
                    os.close(descriptor_dir)
            except OSError:
                pass
            try:
                os.chmod(path, 0o600)
            except OSError:
                pass
        finally:
            if temporary.exists():
                temporary.unlink()

    def write_immutable(
        self, path: str | Path, record: Mapping[str, Any], *, allow_identical: bool = False
    ) -> WriteReceipt:
        resolved = self._resolve_within_root(path)
        payload = render_canonical_json(record).encode("utf-8")
        if resolved.exists():
            self._assert_safe_existing(resolved)
            existing = resolved.read_bytes()
            if allow_identical and existing == payload:
                return WriteReceipt(self.relative(resolved), len(payload), False)
            raise IntegrityError(
                f"immutable record already exists: {resolved}",
                details={"reason_code": "record.immutable_exists"},
            )
        self._atomic_write(resolved, payload)
        return WriteReceipt(self.relative(resolved), len(payload), True)

    def write_mutable(self, path: str | Path, record: Mapping[str, Any]) -> WriteReceipt:
        resolved = self._resolve_within_root(path)
        payload = render_canonical_json(record).encode("utf-8")
        created = not resolved.exists()
        if resolved.exists():
            self._assert_safe_existing(resolved)
        self._atomic_write(resolved, payload)
        return WriteReceipt(self.relative(resolved), len(payload), created)

    def create_task(self, record: Mapping[str, Any]) -> WriteReceipt:
        self.initialize_layout()
        self.validate_record("task", record)
        return self.write_immutable(self.task_path(str(record["task_id"])), record)

    def load_task(self, task_id: str) -> dict[str, Any]:
        record = self.read(self.task_path(task_id))
        self.validate_record("task", record)
        return record

    def update_task_pointers(
        self,
        task_id: str,
        *,
        expected_revision: int,
        decision_id: str | None = None,
        job_id: str | None = None,
        status: str | None = None,
        closure: Mapping[str, Any] | None = None,
        next_recommended_action: str | None = None,
    ) -> dict[str, Any]:
        task = self.load_task(task_id)
        actual = task.get("revision")
        if actual != expected_revision:
            raise StateConflict(
                f"task revision conflict: expected {expected_revision}, found {actual}",
                details={"expected_revision": expected_revision, "actual_revision": actual},
            )
        if decision_id is not None:
            task["current_decision_id"] = decision_id
        if job_id is not None:
            task["current_job_id"] = job_id
        if status is not None:
            task["status"] = status
        if closure is not None:
            task["closure"] = dict(closure)
        if next_recommended_action is not None:
            task["next_recommended_action"] = next_recommended_action
        task["revision"] = expected_revision + 1
        task["updated_at"] = task.get("updated_at")
        self.validate_record("task", task)
        self.write_mutable(self.task_path(task_id), task)
        return task

    def create_staging_directory(self, packet_id: str) -> Path:
        self.initialize_layout()
        packet_id = _safe_identifier(packet_id, "packet id")
        path = self.staging_root / f"{packet_id}-{uuid.uuid4().hex}"
        self._ensure_directory(path)
        return path

    def remove_staging_directory(self, path: str | Path) -> None:
        resolved = self._resolve_within_root(path)
        if resolved.parent != self.staging_root or not resolved.name:
            raise SecurityError("only a direct staging directory may be removed")
        if resolved.exists():
            if resolved.is_symlink() or not resolved.is_dir():
                raise SecurityError(f"unsafe staging path: {resolved}")
            shutil.rmtree(resolved)

    @contextmanager
    def control_lock(self) -> Iterator[None]:
        self.initialize_layout()
        lock = self.root / ".control.lock"
        try:
            descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as error:
            raise StateConflict(
                "another conforming control writer holds the lock",
                details={"reason_code": "state.control_lock_held"},
            ) from error
        try:
            os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
            os.fsync(descriptor)
            yield
        finally:
            os.close(descriptor)
            try:
                lock.unlink()
            except FileNotFoundError:
                pass

    def iter_records(self) -> Iterator[tuple[str, Path, dict[str, Any]]]:
        if not self.root.exists():
            return
        for path in sorted(self.root.rglob("*.json")):
            relative = path.relative_to(self.root)
            if relative.parts and relative.parts[0] in {".staging", "indexes"}:
                continue
            record = self.read(path)
            kind = SCHEMA_VERSIONS.get(record.get("schema_version"))
            if kind:
                yield kind, path, record

    def activated_record_ids(self) -> set[str]:
        result: set[str] = set()
        for kind, _, record in self.iter_records():
            if kind == "activation":
                result.update(str(item["record_id"]) for item in record.get("records", []))
        return result
