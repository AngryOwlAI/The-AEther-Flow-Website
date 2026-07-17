"""One-AgentJob execution through default-deny local interfaces."""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence, TypeVar

from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import IntegrityError, SecurityError, StateConflict
from agentjob_runtime.execution.compiler import CompiledAuthority, CompiledCommand, CompiledPath
from agentjob_runtime.path_security import resolve_project_relative
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import redact_secrets, redact_value


MAX_CAPTURE_BYTES = 64 * 1024
T = TypeVar("T")


@dataclass
class InvocationBudget:
    """Invocation-local cardinality guard; one attempt consumes the budget."""

    maximum_agentjobs: int = 1
    attempted_job_ids: list[str] = field(default_factory=list)

    def claim(self, job_id: str) -> None:
        if self.maximum_agentjobs != 1:
            raise StateConflict(
                "the portable continue runtime requires a one-AgentJob budget",
                details={"reason_code": "execution.invalid_job_budget"},
            )
        if self.attempted_job_ids:
            raise StateConflict(
                "a second AgentJob attempt is forbidden in one invocation",
                details={
                    "reason_code": "execution.one_job_limit",
                    "attempted_job_ids": [*self.attempted_job_ids, job_id],
                },
            )
        self.attempted_job_ids.append(job_id)


@dataclass(frozen=True)
class CommandEvidence:
    command_id: str
    argv: tuple[str, ...]
    cwd: str
    exit_code: int
    status: str
    stdout: str
    stderr: str
    stdout_truncated: bool
    stderr_truncated: bool


@dataclass(frozen=True)
class ExecutionEvidence:
    status: str
    task_id: str
    decision_id: str
    job_id: str
    execution_role_id: str
    before_fingerprint: str
    after_fingerprint: str
    before_files: Mapping[str, str]
    after_files: Mapping[str, str]
    changed_paths: tuple[str, ...]
    accessed_paths: tuple[str, ...]
    command_results: tuple[CommandEvidence, ...]
    operation_result: Any
    execution_performed: bool = True

    def as_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _iter_snapshot_files(root: Path, ignored_roots: Sequence[Path]) -> list[Path]:
    ignored = tuple(path.resolve(strict=False) for path in ignored_roots)
    result: list[Path] = []
    for path in root.rglob("*"):
        if ".git" in path.relative_to(root).parts:
            continue
        resolved = path.resolve(strict=False)
        if any(resolved == item or item in resolved.parents for item in ignored):
            continue
        if path.is_symlink():
            relative = path.relative_to(root).as_posix()
            raise SecurityError(
                f"repository snapshot encountered a symlink: {relative}",
                details={"reason_code": "path.symlink", "path": relative},
            )
        if path.is_file():
            info = path.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                relative = path.relative_to(root).as_posix()
                raise SecurityError(
                    f"repository snapshot encountered an unsafe file alias: {relative}",
                    details={"reason_code": "path.hardlink", "path": relative},
                )
            result.append(path)
    return sorted(result)


def capture_file_state(
    project_root: str | Path,
    *,
    ignored_roots: Sequence[str | Path] = (),
) -> tuple[dict[str, str], str]:
    """Hash regular project files deterministically, excluding Git internals."""

    root = Path(project_root).expanduser().resolve()
    ignored = [
        value.resolve(strict=False) if isinstance(value, Path) and value.is_absolute() else
        (root / value).resolve(strict=False) if not Path(value).is_absolute() else Path(value).resolve(strict=False)
        for value in ignored_roots
    ]
    files = {
        path.relative_to(root).as_posix(): _file_sha256(path)
        for path in _iter_snapshot_files(root, ignored)
    }
    return files, content_sha256(files)


def _truncate(value: str, limit: int) -> tuple[str, bool]:
    encoded = value.encode("utf-8", errors="replace")
    if len(encoded) <= limit:
        return value, False
    return encoded[:limit].decode("utf-8", errors="replace"), True


def _subprocess_text(value: str | bytes | None) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def _changed_paths(before: Mapping[str, str], after: Mapping[str, str]) -> tuple[str, ...]:
    return tuple(
        sorted(
            path
            for path in set(before) | set(after)
            if before.get(path) != after.get(path)
        )
    )


def _record_by_id(
    store: FilesystemControlStore, kind: str, identifier: str, id_field: str
) -> Mapping[str, Any]:
    matches = [
        record
        for record_kind, _, record in store.iter_records()
        if record_kind == kind and record.get(id_field) == identifier
    ]
    if len(matches) != 1:
        raise StateConflict(
            f"activated {kind} record is missing or ambiguous: {identifier}",
            details={"reason_code": "execution.control_record_changed"},
        )
    return matches[0]


def _revalidate_authority(store: FilesystemControlStore, authority: CompiledAuthority) -> None:
    activated = store.activated_record_ids()
    required = {authority.job_id, authority.execution_role_id, authority.decision_id}
    if not required.issubset(activated):
        raise StateConflict(
            "compiled packet is no longer fully activated",
            details={"reason_code": "execution.activation_changed", "missing": sorted(required - activated)},
        )
    task = store.load_task(authority.task_id)
    if task.get("current_job_id") != authority.job_id or task.get("current_decision_id") != authority.decision_id:
        raise StateConflict(
            "task pointers changed after authority compilation",
            details={"reason_code": "execution.task_pointer_changed"},
        )
    job = _record_by_id(store, "agent_job", authority.job_id, "job_id")
    role = _record_by_id(store, "execution_role", authority.execution_role_id, "execution_role_id")
    if content_sha256(job) != authority.source_job_sha256 or content_sha256(role) != authority.source_role_sha256:
        raise IntegrityError(
            "compiled authority source hash changed before execution",
            details={"reason_code": "execution.authority_hash_changed"},
        )
    if job.get("status") != "active":
        raise StateConflict(
            "AgentJob is no longer active",
            details={"reason_code": "execution.job_not_active"},
        )


class ExecutionContext:
    """The only supported project I/O surface for a one-job operation."""

    def __init__(self, authority: CompiledAuthority) -> None:
        self.authority = authority
        self.root = Path(authority.project_root)
        self._accessed: set[str] = set()
        self._commands: list[CommandEvidence] = []

    @property
    def accessed_paths(self) -> tuple[str, ...]:
        return tuple(sorted(self._accessed))

    @property
    def command_results(self) -> tuple[CommandEvidence, ...]:
        return tuple(self._commands)

    def _candidate(self, value: str | Path) -> tuple[Path, str]:
        resolved, normalized = resolve_project_relative(
            self.root,
            value,
            label="execution path",
            allow_directory_rule=False,
        )
        relative = normalized.base_relative
        if resolved.exists() and resolved.is_file() and resolved.stat().st_nlink != 1:
            raise SecurityError(
                f"path request targets a hard-link alias: {value}",
                details={"reason_code": "path.hardlink", "path": relative},
            )
        if any(rule.contains(resolved) for rule in self.authority.forbidden_paths):
            raise SecurityError(
                f"path request is explicitly forbidden: {relative}",
                details={"reason_code": "execution.path_forbidden", "path": relative},
            )
        return resolved, relative

    @staticmethod
    def _permitted(candidate: Path, rules: Sequence[CompiledPath]) -> bool:
        return any(rule.contains(candidate) for rule in rules)

    def read_bytes(self, path: str | Path) -> bytes:
        candidate, relative = self._candidate(path)
        if "read_files" not in self.authority.allowed_actions or not self._permitted(
            candidate, self.authority.allowed_read_paths
        ):
            raise SecurityError(
                f"read is outside AgentJob authority: {relative}",
                details={"reason_code": "execution.read_not_allowed", "path": relative},
            )
        if not candidate.is_file():
            raise SecurityError(
                f"approved read target is not a regular file: {relative}",
                details={"reason_code": "execution.read_target_invalid", "path": relative},
            )
        self._accessed.add(relative)
        return candidate.read_bytes()

    def read_text(self, path: str | Path, *, encoding: str = "utf-8") -> str:
        return self.read_bytes(path).decode(encoding)

    def write_bytes(self, path: str | Path, payload: bytes) -> None:
        candidate, relative = self._candidate(path)
        writable = (*self.authority.allowed_write_paths, *self.authority.allowed_generated_paths)
        if "edit_files" not in self.authority.allowed_actions or not self._permitted(candidate, writable):
            raise SecurityError(
                f"write is outside AgentJob authority: {relative}",
                details={"reason_code": "execution.write_not_allowed", "path": relative},
            )
        candidate.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{candidate.name}.", dir=candidate.parent)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, candidate)
        finally:
            if temporary.exists():
                temporary.unlink()
        self._accessed.add(relative)

    def write_text(self, path: str | Path, value: str, *, encoding: str = "utf-8") -> None:
        self.write_bytes(path, value.encode(encoding))

    def run_command(self, command_id: str) -> CommandEvidence:
        if "run_local_commands" not in self.authority.allowed_actions:
            raise SecurityError(
                "local commands are not authorized",
                details={"reason_code": "execution.command_not_allowed", "command_id": command_id},
            )
        matches = [item for item in self.authority.commands if item.command_id == command_id]
        if len(matches) != 1:
            raise SecurityError(
                f"command is not approved: {command_id}",
                details={"reason_code": "execution.command_not_allowed", "command_id": command_id},
            )
        command: CompiledCommand = matches[0]
        if command.shell:
            raise SecurityError(
                "the portable local executor does not interpolate shell commands",
                details={"reason_code": "execution.shell_adapter_required", "command_id": command_id},
            )
        try:
            completed = subprocess.run(
                list(command.argv),
                cwd=command.cwd,
                env=dict(command.environment),
                text=True,
                capture_output=True,
                check=False,
                timeout=command.timeout_seconds,
            )
            stdout, stdout_truncated = _truncate(
                redact_secrets(completed.stdout), MAX_CAPTURE_BYTES
            )
            stderr, stderr_truncated = _truncate(
                redact_secrets(completed.stderr), MAX_CAPTURE_BYTES
            )
            evidence = CommandEvidence(
                command.command_id,
                tuple(redact_secrets(item) for item in command.argv),
                command.cwd,
                int(completed.returncode),
                "pass" if completed.returncode == 0 else "fail",
                stdout,
                stderr,
                stdout_truncated,
                stderr_truncated,
            )
        except subprocess.TimeoutExpired as error:
            stdout, stdout_truncated = _truncate(
                redact_secrets(_subprocess_text(error.stdout)), MAX_CAPTURE_BYTES
            )
            stderr, stderr_truncated = _truncate(
                redact_secrets(_subprocess_text(error.stderr)), MAX_CAPTURE_BYTES
            )
            evidence = CommandEvidence(
                command.command_id,
                tuple(redact_secrets(item) for item in command.argv),
                command.cwd,
                124,
                "timeout",
                stdout,
                stderr,
                stdout_truncated,
                stderr_truncated,
            )
        self._commands.append(evidence)
        return evidence

    def request_external_effect(self, effect_id: str, adapter: Callable[[], T]) -> T:
        if effect_id not in self.authority.external_effects:
            raise SecurityError(
                f"external effect is not authorized: {effect_id}",
                details={"reason_code": "execution.external_effect_not_allowed", "effect_id": effect_id},
            )
        return adapter()


def execute_one_job(
    *,
    authority: CompiledAuthority,
    store: FilesystemControlStore,
    operation: Callable[[ExecutionContext], T],
    budget: InvocationBudget,
    expected_before_fingerprint: str | None = None,
    snapshot_ignored_roots: Sequence[str | Path] = (),
) -> ExecutionEvidence:
    """Execute one operation after revalidating all compiled control authority."""

    _revalidate_authority(store, authority)
    before, before_fingerprint = capture_file_state(
        authority.project_root, ignored_roots=snapshot_ignored_roots
    )
    if expected_before_fingerprint is not None and before_fingerprint != expected_before_fingerprint:
        raise StateConflict(
            "repository state changed after preflight",
            details={
                "reason_code": "execution.stale_state_snapshot",
                "expected_fingerprint": expected_before_fingerprint,
                "actual_fingerprint": before_fingerprint,
            },
        )
    budget.claim(authority.job_id)
    context = ExecutionContext(authority)
    result = operation(context)
    after, after_fingerprint = capture_file_state(
        authority.project_root, ignored_roots=snapshot_ignored_roots
    )
    return ExecutionEvidence(
        "executed",
        authority.task_id,
        authority.decision_id,
        authority.job_id,
        authority.execution_role_id,
        before_fingerprint,
        after_fingerprint,
        before,
        after,
        _changed_paths(before, after),
        context.accessed_paths,
        context.command_results,
        result,
    )
