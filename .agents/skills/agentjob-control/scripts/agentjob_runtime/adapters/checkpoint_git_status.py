"""Read-only Git-status checkpoint provider."""

from __future__ import annotations

from typing import Any, Mapping

from agentjob_runtime.adapters.repository_git import GitRepositoryProvider


class GitStatusCheckpointProvider:
    provider_id = "git_status"

    def __init__(self, project_root: str) -> None:
        self.repository = GitRepositoryProvider(project_root)

    def _receipt(self) -> dict[str, Any]:
        identity = self.repository.identity()
        status = self.repository.status()
        return {
            "provider": self.provider_id,
            "status": "pass",
            "revision": identity.revision,
            "evidence_ref": None,
            "claims": [],
            "changed_paths": list(status.changed_paths),
            "status_porcelain": status.porcelain,
            "process_evidence_only": True,
        }

    def inspect_before(self, job: Mapping[str, Any]) -> Mapping[str, Any]:
        return self._receipt()

    def capture_after(self, completion: Mapping[str, Any]) -> Mapping[str, Any]:
        return self._receipt()

    def __call__(self, specification: Mapping[str, Any], evidence: Any) -> Mapping[str, Any]:
        return self._receipt()
