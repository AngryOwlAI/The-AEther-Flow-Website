"""Explicitly approved Git commit checkpoint scoped to declared changed paths."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.adapters.repository_git import GitRepositoryProvider
from agentjob_runtime.errors import RecordValidationError, SecurityError


class GitCommitCheckpointProvider:
    provider_id = "git_commit"

    def __init__(
        self,
        project_root: str | Path,
        *,
        approval_ref: str | None,
        message: str,
        approved_paths: Sequence[str] | None = None,
        timeout_seconds: int = 30,
    ) -> None:
        self.repository = GitRepositoryProvider(project_root)
        self.root = self.repository.root
        self.approval_ref = approval_ref
        self.message = message
        self.approved_paths = tuple(approved_paths or ())
        self.timeout_seconds = timeout_seconds

    def _run(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment["GIT_OPTIONAL_LOCKS"] = "0"
        return subprocess.run(
            ["git", *arguments],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
            timeout=self.timeout_seconds,
            env=environment,
        )

    def inspect_before(self, job: Mapping[str, Any]) -> Mapping[str, Any]:
        identity = self.repository.identity()
        status = self.repository.status()
        return {
            "provider": self.provider_id,
            "status": "inspection_only",
            "revision": identity.revision,
            "evidence_ref": None,
            "claims": [],
            "changed_paths": list(status.changed_paths),
            "approval_present": bool(self.approval_ref),
            "process_evidence_only": True,
        }

    @staticmethod
    def _completion_paths(completion: Mapping[str, Any]) -> tuple[str, ...]:
        values = completion.get("changed_paths", ())
        if not isinstance(values, (list, tuple)):
            raise RecordValidationError("checkpoint completion changed_paths must be a list")
        return tuple(str(item) for item in values)

    def capture_after(self, completion: Mapping[str, Any]) -> Mapping[str, Any]:
        if not isinstance(self.approval_ref, str) or not self.approval_ref.strip():
            raise SecurityError(
                "Git commit checkpoint requires explicit approval",
                details={"reason_code": "checkpoint.git_commit_approval_required"},
            )
        if not self.message.strip():
            raise RecordValidationError("Git commit checkpoint message must be nonblank")
        paths = self._completion_paths(completion)
        if not paths:
            raise RecordValidationError("Git commit checkpoint requires declared changed paths")
        canonical = tuple(self.repository.canonicalize_path(item).relative for item in paths)
        if self.approved_paths:
            approved = {
                self.repository.canonicalize_path(item).relative
                for item in self.approved_paths
            }
            outside = sorted(set(canonical) - approved)
            if outside:
                raise SecurityError(
                    "checkpoint paths exceed explicit approval",
                    details={
                        "reason_code": "checkpoint.path_not_approved",
                        "paths": outside,
                    },
                )
        before = self.repository.identity().revision
        result = self._run("commit", "--only", "-m", self.message, "--", *canonical)
        if result.returncode != 0:
            return {
                "provider": self.provider_id,
                "status": "fail",
                "revision": before,
                "evidence_ref": None,
                "claims": [],
                "reason_code": "checkpoint.git_commit_failed",
                "exit_code": result.returncode,
                "stderr": result.stderr.strip(),
                "approved_paths": list(canonical),
                "approval_ref": self.approval_ref,
                "process_evidence_only": True,
            }
        after = self.repository.identity().revision
        return {
            "provider": self.provider_id,
            "status": "pass",
            "revision": after,
            "evidence_ref": None,
            "claims": [],
            "prior_revision": before,
            "approved_paths": list(canonical),
            "approval_ref": self.approval_ref,
            "process_evidence_only": True,
        }

    def __call__(self, specification: Mapping[str, Any], evidence: Any) -> Mapping[str, Any]:
        return self.capture_after({"changed_paths": list(evidence.changed_paths)})
