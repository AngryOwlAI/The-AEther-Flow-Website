"""Semantic conformance reporting for adapters over existing control systems."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from agentjob_runtime.adapters.protocols import FEATURE_MODES


REQUIRED_CONFORMANCE_FEATURES = (
    "task",
    "director_decision",
    "agent_job",
    "execution_role",
    "completion",
    "handoff",
    "immutability",
    "supersession",
    "one_job_cardinality",
    "claim_boundary",
    "path_boundary",
    "recovery_evidence",
)


@dataclass(frozen=True)
class ConformanceCheck:
    feature_id: str
    mode: str
    status: str
    evidence: tuple[str, ...]
    blocking: bool
    reason_code: str | None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConformanceReport:
    adapter_id: str
    adapter_version: str
    status: str
    checks: tuple[ConformanceCheck, ...]
    execution_performed: bool = False

    @property
    def blocking_gaps(self) -> tuple[str, ...]:
        return tuple(item.feature_id for item in self.checks if item.blocking)

    @property
    def native_features(self) -> tuple[str, ...]:
        return tuple(item.feature_id for item in self.checks if item.mode == "native")

    @property
    def emulated_features(self) -> tuple[str, ...]:
        return tuple(item.feature_id for item in self.checks if item.mode == "emulated")

    @property
    def unsupported_features(self) -> tuple[str, ...]:
        return tuple(item.feature_id for item in self.checks if item.mode == "unsupported")

    def as_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "adapter_version": self.adapter_version,
            "status": self.status,
            "execution_performed": self.execution_performed,
            "blocking_gaps": list(self.blocking_gaps),
            "native_features": list(self.native_features),
            "emulated_features": list(self.emulated_features),
            "unsupported_features": list(self.unsupported_features),
            "checks": [item.as_dict() for item in self.checks],
        }


def _check(feature_id: str, claim: Mapping[str, Any] | None) -> ConformanceCheck:
    if not isinstance(claim, Mapping):
        return ConformanceCheck(
            feature_id,
            "unsupported",
            "fail",
            (),
            True,
            "conformance.mapping_absent",
        )
    mode = str(claim.get("mode", "unsupported"))
    if mode not in FEATURE_MODES:
        mode = "unsupported"
    status = str(claim.get("status", "fail"))
    evidence_value = claim.get("evidence", ())
    evidence = (
        tuple(str(item) for item in evidence_value)
        if isinstance(evidence_value, (list, tuple))
        else ()
    )
    reason = str(claim["reason_code"]) if claim.get("reason_code") else None
    blocking = mode == "unsupported" or status != "pass" or not evidence
    if blocking and reason is None:
        reason = (
            "conformance.evidence_absent"
            if not evidence
            else "conformance.semantic_check_failed"
        )
    return ConformanceCheck(feature_id, mode, status, evidence, blocking, reason)


def run_conformance(adapter: Any) -> ConformanceReport:
    """Inspect adapter claims; never execute a task or repair missing authority."""

    claims = adapter.conformance_claims()
    checks = tuple(
        _check(feature_id, claims.get(feature_id) if isinstance(claims, Mapping) else None)
        for feature_id in REQUIRED_CONFORMANCE_FEATURES
    )
    status = "conformant" if not any(item.blocking for item in checks) else "blocking_gaps"
    return ConformanceReport(
        str(getattr(adapter, "adapter_id", "unknown")),
        str(getattr(adapter, "version", "unknown")),
        status,
        checks,
    )
