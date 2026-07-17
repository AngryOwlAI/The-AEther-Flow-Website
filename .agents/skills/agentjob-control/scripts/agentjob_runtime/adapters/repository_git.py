"""Read-only Git repository provider with deterministic status normalization."""

from __future__ import annotations

import os
import subprocess
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
from agentjob_runtime.adapters.repository_filesystem import (
    _canonicalize,
    _file_hash,
    compare_snapshots,
)
from agentjob_runtime.errors import RecordValidationError, SecurityError


class GitRepositoryProvider:
    provider_id = "git"

    def __init__(
        self,
        project_root: str | Path,
        *,
        case_sensitive: bool | None = None,
        timeout_seconds: int = 15,
    ) -> None:
        requested = Path(project_root).expanduser().resolve()
        if not requested.is_dir():
            raise RecordValidationError(f"repository root is not a directory: {requested}")
        self.timeout_seconds = timeout_seconds
        self.case_sensitive = os.name != "nt" if case_sensitive is None else case_sensitive
        root = self._run_from(requested, "rev-parse", "--show-toplevel")
        self.root = Path(root).resolve()

    def _run_from(
        self, cwd: Path, *arguments: str, allow_failure: bool = False
    ) -> str:
        environment = dict(os.environ)
        environment["GIT_OPTIONAL_LOCKS"] = "0"
        result = subprocess.run(
            ["git", *arguments],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            timeout=self.timeout_seconds,
            env=environment,
        )
        if result.returncode != 0 and not allow_failure:
            raise RecordValidationError(
                f"Git inspection failed: {' '.join(arguments)}",
                details={
                    "reason_code": "repository.git_inspection_failed",
                    "exit_code": result.returncode,
                    "stderr": result.stderr.strip(),
                },
            )
        return result.stdout.rstrip("\n") if result.returncode == 0 else ""

    def _run(self, *arguments: str, allow_failure: bool = False) -> str:
        return self._run_from(self.root, *arguments, allow_failure=allow_failure)

    def canonicalize_path(self, value: str) -> CanonicalPath:
        return _canonicalize(self.root, value, case_sensitive=self.case_sensitive)

    def identity(self) -> RepositoryIdentity:
        common_value = self._run("rev-parse", "--git-common-dir")
        common = Path(common_value)
        if not common.is_absolute():
            common = (self.root / common).resolve()
        branch = self._run("branch", "--show-current") or None
        revision = self._run("rev-parse", "--verify", "HEAD", allow_failure=True) or "UNBORN"
        return RepositoryIdentity(
            self.provider_id,
            str(self.root),
            str(self.root),
            str(common),
            branch,
            revision,
            branch is None and revision != "UNBORN",
        )

    @staticmethod
    def _status_path(line: str) -> str:
        value = line[3:] if len(line) >= 3 else line
        if " -> " in value:
            value = value.rsplit(" -> ", 1)[1]
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        return value.replace("\\", "/")

    def status(self) -> RepositoryStatus:
        identity = self.identity()
        lines = sorted(
            line
            for line in self._run(
                "status", "--porcelain=v1", "--untracked-files=all"
            ).splitlines()
            if line
        )
        normalized = "\n".join(lines)
        paths = tuple(sorted({self._status_path(line) for line in lines}))
        return RepositoryStatus(
            self.provider_id,
            identity.revision,
            normalized,
            paths,
            not lines,
        )

    def _files(self) -> dict[str, str]:
        output = self._run(
            "ls-files", "-co", "--exclude-standard", "-z"
        )
        files: dict[str, str] = {}
        for value in sorted(item for item in output.split("\0") if item):
            canonical = self.canonicalize_path(value)
            path = Path(canonical.absolute)
            if path.is_symlink():
                raise SecurityError(f"repository snapshot refuses symlink content: {path}")
            if path.is_file():
                files[canonical.relative] = _file_hash(path)
        return files

    def snapshot(self) -> RepositorySnapshot:
        return RepositorySnapshot(self.identity(), self.status(), self._files())

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
        aliases = {"git_common_dir": "common_dir"}
        mismatches: list[str] = []
        for requested, actual_key in (
            ("provider", "provider"),
            ("root", "root"),
            ("worktree", "worktree"),
            ("git_common_dir", "common_dir"),
            ("branch", "branch"),
            ("revision", "revision"),
        ):
            if requested in expected and expected[requested] != actual.get(actual_key):
                mismatches.append(requested)
        return ValidationResult(
            "fail" if mismatches else "pass",
            "repository.identity_mismatch" if mismatches else None,
            tuple(f"Repository identity differs at {item}." for item in mismatches),
            {"actual": actual, "expected": dict(expected), "aliases": aliases},
        )
