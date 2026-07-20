"""Read-only repository provider for projects without Git."""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.adapters.protocols import (
    CanonicalPath,
    PathChange,
    RepositoryIdentity,
    RepositorySnapshot,
    RepositoryStatus,
    ValidationResult,
)
from agentjob_runtime.errors import RecordValidationError, SecurityError
from agentjob_runtime.records.canonical import content_sha256


WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")


def _canonicalize(root: Path, value: str, *, case_sensitive: bool) -> CanonicalPath:
    if not isinstance(value, str) or not value.strip():
        raise SecurityError("repository path must be a nonblank relative path")
    if Path(value).is_absolute() or WINDOWS_ABSOLUTE.match(value) or value.startswith("\\\\"):
        raise SecurityError("repository path must be relative")
    supplied = Path(value.replace("\\", "/"))
    if ".." in supplied.parts:
        raise SecurityError("repository path cannot traverse outside the root")
    candidate = (root / supplied).resolve(strict=False)
    try:
        relative = candidate.relative_to(root)
    except ValueError as error:
        raise SecurityError("repository path resolves outside the root") from error
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise SecurityError(f"repository path traverses a symlink: {current}")
    normalized = relative.as_posix()
    key = normalized if case_sensitive else normalized.casefold()
    return CanonicalPath(value, normalized, str(candidate), key)


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compare_snapshots(
    before: RepositorySnapshot, after: RepositorySnapshot
) -> tuple[PathChange, ...]:
    paths = sorted(set(before.files) | set(after.files))
    changes: list[PathChange] = []
    for path in paths:
        prior = before.files.get(path)
        current = after.files.get(path)
        if prior == current:
            continue
        status = "added" if prior is None else "deleted" if current is None else "modified"
        changes.append(PathChange(path, status, prior, current))
    return tuple(changes)


class FilesystemRepositoryProvider:
    provider_id = "filesystem_only"

    def __init__(
        self,
        project_root: str | Path,
        *,
        excluded_roots: Sequence[str] = (".git", ".local"),
        case_sensitive: bool | None = None,
    ) -> None:
        self.root = Path(project_root).expanduser().resolve()
        if not self.root.is_dir():
            raise RecordValidationError(f"repository root is not a directory: {self.root}")
        self.excluded_roots = tuple(excluded_roots)
        self.case_sensitive = os.name != "nt" if case_sensitive is None else case_sensitive

    def canonicalize_path(self, value: str) -> CanonicalPath:
        return _canonicalize(self.root, value, case_sensitive=self.case_sensitive)

    def _files(self) -> dict[str, str]:
        files: dict[str, str] = {}
        for path in sorted(self.root.rglob("*")):
            relative = path.relative_to(self.root)
            if relative.parts and relative.parts[0] in self.excluded_roots:
                continue
            if path.is_symlink():
                raise SecurityError(f"repository snapshot refuses symlink content: {path}")
            if path.is_file():
                canonical = self.canonicalize_path(relative.as_posix())
                files[canonical.relative] = _file_hash(path)
        return files

    def identity(self) -> RepositoryIdentity:
        files = self._files()
        return RepositoryIdentity(
            self.provider_id,
            str(self.root),
            str(self.root),
            None,
            None,
            content_sha256(files),
            False,
        )

    def status(self) -> RepositoryStatus:
        identity = self.identity()
        return RepositoryStatus(self.provider_id, identity.revision, "", (), True)

    def snapshot(self) -> RepositorySnapshot:
        files = self._files()
        identity = RepositoryIdentity(
            self.provider_id,
            str(self.root),
            str(self.root),
            None,
            None,
            content_sha256(files),
            False,
        )
        return RepositorySnapshot(
            identity,
            RepositoryStatus(self.provider_id, identity.revision, "", (), True),
            files,
        )

    def changed_paths(
        self, before: RepositorySnapshot, after: RepositorySnapshot
    ) -> Sequence[PathChange]:
        return compare_snapshots(before, after)

    def fingerprint_payload(self) -> Mapping[str, Any]:
        snapshot = self.snapshot()
        return {
            "identity": snapshot.identity.as_dict(),
            "status": snapshot.status.as_dict(),
            "files": dict(snapshot.files),
        }

    def matches(self, expected: Mapping[str, Any]) -> ValidationResult:
        actual = self.identity().as_dict()
        mismatches = tuple(
            key
            for key in ("provider", "root", "worktree", "branch", "revision")
            if key in expected and expected[key] != actual.get(key)
        )
        return ValidationResult(
            "fail" if mismatches else "pass",
            "repository.identity_mismatch" if mismatches else None,
            tuple(f"Repository identity differs at {key}." for key in mismatches),
            {"actual": actual, "expected": dict(expected)},
        )
