"""No-checkpoint provider for policies that require only an explicit receipt."""

from __future__ import annotations

from typing import Any, Mapping


class NoneCheckpointProvider:
    provider_id = "none"

    @staticmethod
    def _receipt() -> dict[str, Any]:
        return {
            "provider": "none",
            "status": "not_required",
            "revision": None,
            "evidence_ref": None,
            "claims": [],
            "process_evidence_only": True,
        }

    def inspect_before(self, job: Mapping[str, Any]) -> Mapping[str, Any]:
        return self._receipt()

    def capture_after(self, completion: Mapping[str, Any]) -> Mapping[str, Any]:
        return self._receipt()

    def __call__(self, specification: Mapping[str, Any], evidence: Any) -> Mapping[str, Any]:
        return self._receipt()
