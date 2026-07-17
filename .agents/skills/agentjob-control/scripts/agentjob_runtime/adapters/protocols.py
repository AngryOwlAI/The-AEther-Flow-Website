"""Typed, inspectable adapter contracts for portable governed continuation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable

from agentjob_runtime.errors import BootstrapRequired, RecordValidationError


ADAPTER_CAPABILITY_VERSION = "1.0.0"
FEATURE_MODES = {"native", "emulated", "unsupported"}


@dataclass(frozen=True)
class FeatureCapability:
    feature_id: str
    version: str
    required: bool
    available: bool
    mode: str = "native"
    reason_code: str | None = None

    def __post_init__(self) -> None:
        if self.mode not in FEATURE_MODES:
            raise ValueError(f"unsupported feature mode: {self.mode}")
        if self.mode == "unsupported" and self.available:
            raise ValueError("an unsupported feature cannot be available")


@dataclass(frozen=True)
class AdapterCapabilityReport:
    adapter_id: str
    adapter_version: str
    capability_version: str
    features: tuple[FeatureCapability, ...]
    canonical_source_roots: tuple[str, ...]
    unsupported_features: tuple[str, ...] = ()
    conformance_hooks: tuple[str, ...] = ()
    execution_performed: bool = False

    @property
    def missing_required(self) -> tuple[str, ...]:
        return tuple(
            item.feature_id
            for item in self.features
            if item.required and not item.available
        )

    @property
    def status(self) -> str:
        return "ready" if not self.missing_required else "capability_mismatch"

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "adapter_id": self.adapter_id,
            "adapter_version": self.adapter_version,
            "capability_version": self.capability_version,
            "missing_required": list(self.missing_required),
            "canonical_source_roots": list(self.canonical_source_roots),
            "unsupported_features": list(self.unsupported_features),
            "conformance_hooks": list(self.conformance_hooks),
            "execution_performed": self.execution_performed,
            "features": [asdict(item) for item in self.features],
        }

    def require(self, feature_ids: Sequence[str]) -> None:
        by_id = {item.feature_id: item for item in self.features}
        missing = sorted(
            feature_id
            for feature_id in feature_ids
            if feature_id not in by_id or not by_id[feature_id].available
        )
        if missing:
            raise BootstrapRequired(
                "adapter lacks required capabilities",
                details={
                    "reason_code": "adapter.capability_mismatch",
                    "adapter_id": self.adapter_id,
                    "missing_capabilities": missing,
                    "report": self.as_dict(),
                },
            )


@dataclass(frozen=True)
class ValidationResult:
    status: str
    reason_code: str | None = None
    findings: tuple[str, ...] = ()
    evidence: Mapping[str, Any] | None = None

    @property
    def blocking(self) -> bool:
        return self.status in {"fail", "unsupported"}

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryIdentity:
    provider: str
    root: str
    worktree: str
    common_dir: str | None
    branch: str | None
    revision: str
    detached: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryStatus:
    provider: str
    revision: str
    porcelain: str
    changed_paths: tuple[str, ...]
    clean: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositorySnapshot:
    identity: RepositoryIdentity
    status: RepositoryStatus
    files: Mapping[str, str]


@dataclass(frozen=True)
class PathChange:
    path: str
    status: str
    before_sha256: str | None
    after_sha256: str | None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CanonicalPath:
    supplied: str
    relative: str
    absolute: str
    comparison_key: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@runtime_checkable
class ProjectAdapter(Protocol):
    adapter_id: str
    version: str

    def discover(self, project_root: Path) -> AdapterCapabilityReport: ...

    def load_authoritative_state(self) -> Mapping[str, Any]: ...

    def list_roles(self, snapshot: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]: ...

    def list_routes(self, snapshot: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]: ...

    def validate_decision(self, decision: Mapping[str, Any]) -> ValidationResult: ...

    def validate_job(self, job: Mapping[str, Any]) -> ValidationResult: ...

    def compute_domain_fingerprint(self) -> Mapping[str, Any]: ...

    def evaluate_completion(self, completion: Mapping[str, Any]) -> ValidationResult: ...

    def conformance_claims(self) -> Mapping[str, Mapping[str, Any]]: ...


@runtime_checkable
class ControlStore(Protocol):
    def stage_packet(self, packet: Mapping[str, Any]) -> Any: ...

    def activate_packet(self, staged: Any, expected_revision: int) -> Any: ...

    def supersede_packet(self, request: Mapping[str, Any]) -> Any: ...

    def load_task(self, task_id: str) -> Mapping[str, Any]: ...

    def resolve_current(self) -> Mapping[str, Any]: ...

    def write_completion(self, completion: Mapping[str, Any]) -> Any: ...

    def write_handoff(self, handoff: Mapping[str, Any]) -> Any: ...

    def regenerate_indexes(self) -> Any: ...


@runtime_checkable
class ThreadProvider(Protocol):
    provider_id: str

    def capabilities(self) -> Mapping[str, Any]: ...

    def create_successor(
        self, envelope: Mapping[str, Any], idempotency_key: str
    ) -> Mapping[str, Any]: ...

    def read_thread(self, thread_id: str) -> Mapping[str, Any]: ...

    def confirm_terminal(self, thread_id: str) -> bool: ...


@runtime_checkable
class NativeGoalProvider(Protocol):
    provider_id: str

    def set_mirror(self, thread_id: str, summary: Mapping[str, Any]) -> Mapping[str, Any]: ...

    def get_mirror(self, thread_id: str) -> Mapping[str, Any] | None: ...

    def clear_mirror(self, thread_id: str) -> Mapping[str, Any]: ...


@runtime_checkable
class RepositoryProvider(Protocol):
    provider_id: str

    def identity(self) -> RepositoryIdentity: ...

    def status(self) -> RepositoryStatus: ...

    def snapshot(self) -> RepositorySnapshot: ...

    def changed_paths(
        self, before: RepositorySnapshot, after: RepositorySnapshot
    ) -> Sequence[PathChange]: ...

    def canonicalize_path(self, value: str) -> CanonicalPath: ...

    def fingerprint_payload(self) -> Mapping[str, Any]: ...


@runtime_checkable
class CheckpointProvider(Protocol):
    provider_id: str

    def inspect_before(self, job: Mapping[str, Any]) -> Mapping[str, Any]: ...

    def capture_after(self, completion: Mapping[str, Any]) -> Mapping[str, Any]: ...


@runtime_checkable
class ContextProvider(Protocol):
    provider_id: str

    def available(self) -> bool: ...

    def search(self, query: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]: ...


@runtime_checkable
class PolicyPackLoader(Protocol):
    loader_id: str

    def load_policy(self, source: str | Path) -> Mapping[str, Any]: ...

    def validate_policy(self, policy: Mapping[str, Any]) -> ValidationResult: ...


def validate_authority_extensions(
    extensions: Mapping[str, Any], *, declared_namespaces: Sequence[str]
) -> None:
    """Reject undeclared or malformed authority-affecting extensions."""

    declared = set(declared_namespaces)
    undeclared = sorted(set(extensions) - declared)
    if undeclared:
        raise RecordValidationError(
            "authority extension namespace is undeclared",
            details={
                "reason_code": "adapter.extension_namespace_undeclared",
                "namespaces": undeclared,
            },
        )
    for namespace, value in extensions.items():
        if not isinstance(value, Mapping) or set(value) != {"version", "required", "data"}:
            raise RecordValidationError(
                f"authority extension has an invalid envelope: {namespace}",
                details={"reason_code": "adapter.extension_envelope_invalid"},
            )
        if not isinstance(value["required"], bool) or not isinstance(value["data"], Mapping):
            raise RecordValidationError(
                f"authority extension has invalid typed fields: {namespace}",
                details={"reason_code": "adapter.extension_envelope_invalid"},
            )
