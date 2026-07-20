"""Approved argv-only project command checkpoint provider."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.errors import RecordValidationError, SecurityError


class CommandCheckpointProvider:
    provider_id = "project_command"

    def __init__(
        self,
        project_root: str | Path,
        *,
        argv: Sequence[str],
        cwd: str = ".",
        environment: Mapping[str, str] | None = None,
        timeout_seconds: int = 60,
    ) -> None:
        self.root = Path(project_root).expanduser().resolve()
        if not self.root.is_dir():
            raise RecordValidationError(f"checkpoint root is not a directory: {self.root}")
        if not argv or any(not isinstance(item, str) or not item for item in argv):
            raise RecordValidationError("checkpoint argv must contain nonblank strings")
        supplied_cwd = Path(cwd)
        if supplied_cwd.is_absolute() or ".." in supplied_cwd.parts:
            raise SecurityError("checkpoint cwd must remain project-relative")
        self.cwd = (self.root / supplied_cwd).resolve(strict=False)
        try:
            self.cwd.relative_to(self.root)
        except ValueError as error:
            raise SecurityError("checkpoint cwd escapes project root") from error
        self.argv = tuple(argv)
        self.environment = dict(environment or {})
        self.timeout_seconds = timeout_seconds
        self.calls = 0

    def inspect_before(self, job: Mapping[str, Any]) -> Mapping[str, Any]:
        return {
            "provider": self.provider_id,
            "status": "inspection_only",
            "revision": None,
            "evidence_ref": None,
            "claims": [],
            "argv": list(self.argv),
            "cwd": self.cwd.relative_to(self.root).as_posix() or ".",
            "process_evidence_only": True,
        }

    def capture_after(self, completion: Mapping[str, Any]) -> Mapping[str, Any]:
        self.calls += 1
        environment = {"PATH": os.environ.get("PATH", "")}
        environment.update(self.environment)
        result = subprocess.run(
            list(self.argv),
            cwd=self.cwd,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
            timeout=self.timeout_seconds,
            shell=False,
        )
        return {
            "provider": self.provider_id,
            "status": "pass" if result.returncode == 0 else "fail",
            "revision": None,
            "evidence_ref": None,
            "claims": [],
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "argv": list(self.argv),
            "cwd": self.cwd.relative_to(self.root).as_posix() or ".",
            "process_evidence_only": True,
        }

    def __call__(self, specification: Mapping[str, Any], evidence: Any) -> Mapping[str, Any]:
        return self.capture_after({"job_id": getattr(evidence, "job_id", None)})
