"""Portable ProjectAdapter for the registered `.agents/control/` profile."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.adapters.protocols import (
    ADAPTER_CAPABILITY_VERSION,
    AdapterCapabilityReport,
    FeatureCapability,
    ValidationResult,
)
from agentjob_runtime.config import LoadedConfig, load_config, resolve_project_path
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.resolver import snapshot_from_store
from agentjob_runtime.errors import AgentJobControlError, RecordValidationError
from agentjob_runtime.records.canonical import content_sha256, load_structured
from agentjob_runtime.validation.schema import format_issues, validate_instance


CORE_FEATURES = (
    "task-records",
    "director-decisions",
    "agentjob-records",
    "execution-role-bindings",
    "completion-records",
    "handoffs",
    "immutable-activation",
    "supersession",
    "policy-catalog",
    "checkpoint-provider",
)


class FilesystemProjectAdapter:
    """Read portable control authority without making domain-specific claims."""

    adapter_id = "filesystem"
    version = "1.0.0"

    def __init__(
        self,
        project_root: str | Path,
        *,
        config_path: str | Path | None = None,
        provider_versions: Mapping[str, str] | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        self.config_path = config_path
        self.provider_versions = dict(provider_versions or {})

    def _load(self) -> LoadedConfig:
        return load_config(
            self.project_root,
            config_path=self.config_path,
            provider_versions=self.provider_versions,
        )

    @staticmethod
    def _feature(feature_id: str, available: bool, reason: str | None = None):
        return FeatureCapability(
            feature_id,
            "1.0.0",
            True,
            available,
            "native" if available else "unsupported",
            reason,
        )

    def discover(self, project_root: Path) -> AdapterCapabilityReport:
        root = Path(project_root).expanduser().resolve()
        try:
            loaded = load_config(
                root,
                config_path=self.config_path,
                provider_versions=self.provider_versions,
            )
            configured = loaded.data["control"]["adapter"] == self.adapter_id
            capabilities_ready = loaded.capabilities.status == "ready"
            available = configured and capabilities_ready
            reason = None
            if not configured:
                reason = "adapter.configuration_selects_other_provider"
            elif not capabilities_ready:
                reason = "adapter.required_provider_unavailable"
            roots = (loaded.control_root.relative_to(root).as_posix(),)
        except AgentJobControlError as error:
            available = False
            reason = error.code
            roots = (".agents/control",)
        features = tuple(self._feature(item, available, reason) for item in CORE_FEATURES)
        features += (
            FeatureCapability(
                "domain-truth-promotion",
                "1.0.0",
                False,
                False,
                "unsupported",
                "adapter.process_evidence_only",
            ),
        )
        return AdapterCapabilityReport(
            self.adapter_id,
            self.version,
            ADAPTER_CAPABILITY_VERSION,
            features,
            roots,
            ("domain-truth-promotion",),
            ("conformance_claims", "validate_decision", "validate_job"),
        )

    def _load_policies(self, loaded: LoadedConfig) -> list[dict[str, Any]]:
        schema = Path(__file__).resolve().parents[3] / "schemas" / "policy-pack.schema.json"
        policies: list[dict[str, Any]] = []
        for value in loaded.data["policy"]["packs"]:
            path = resolve_project_path(loaded.project_root, value, purpose="policy pack")
            if not path.is_file():
                raise RecordValidationError(f"policy pack is missing: {value}")
            policy = load_structured(path)
            if not isinstance(policy, dict):
                raise RecordValidationError(f"policy pack must be a mapping: {value}")
            issues = validate_instance(policy, schema)
            if issues:
                raise RecordValidationError(
                    f"policy pack failed validation: {value}",
                    details={"findings": format_issues(issues).splitlines()},
                )
            policies.append(policy)
        return policies

    def _load_role_catalogs(self, loaded: LoadedConfig) -> list[dict[str, Any]]:
        roles: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for value in loaded.data["roles"]["catalog"]:
            root = resolve_project_path(loaded.project_root, value, purpose="role catalog")
            if not root.exists():
                continue
            if not root.is_dir() or root.is_symlink():
                raise RecordValidationError(f"role catalog is not a safe directory: {value}")
            for path in sorted((*root.glob("*.json"), *root.glob("*.yaml"), *root.glob("*.yml"))):
                role = load_structured(path)
                if not isinstance(role, dict):
                    raise RecordValidationError(f"role catalog entry must be a mapping: {path}")
                role_id = str(role.get("role_id", ""))
                version = str(role.get("version", ""))
                if not role_id or not version:
                    raise RecordValidationError(f"role catalog entry lacks role_id or version: {path}")
                identity = (role_id, version)
                if identity in seen:
                    raise RecordValidationError(f"duplicate role catalog identity: {role_id}@{version}")
                seen.add(identity)
                roles.append(
                    {
                        **copy.deepcopy(role),
                        "source_ref": path.relative_to(loaded.project_root).as_posix(),
                    }
                )
        return roles

    def load_authoritative_state(self) -> Mapping[str, Any]:
        loaded = self._load()
        report = self.discover(self.project_root)
        report.require(CORE_FEATURES)
        store = FilesystemControlStore(self.project_root, loaded.control_root)
        grouped: dict[str, list[dict[str, Any]]] = {}
        for kind, path, record in store.iter_records():
            grouped.setdefault(kind, []).append(
                {
                    "path": store.relative(path),
                    "sha256": content_sha256(record),
                    "record": record,
                }
            )
        return {
            "adapter": report.as_dict(),
            "configuration": copy.deepcopy(loaded.data),
            "canonical_source_roots": list(report.canonical_source_roots),
            "records": grouped,
            "roles": self._load_role_catalogs(loaded),
            "policies": self._load_policies(loaded),
            "current": snapshot_from_store(store, capabilities=loaded.capabilities),
            "domain_truth": "not_evaluated",
        }

    def list_roles(self, snapshot: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
        roles = snapshot.get("roles", [])
        if not isinstance(roles, list):
            raise RecordValidationError("adapter snapshot roles must be a list")
        return tuple(copy.deepcopy(roles))

    def list_routes(self, snapshot: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
        current = snapshot.get("current", {})
        task = current.get("task") if isinstance(current, Mapping) else None
        if not isinstance(task, Mapping):
            return ()
        return tuple(
            {
                "route_id": f"role:{role['role_id']}",
                "role_id": role["role_id"],
                "role_version": role["version"],
                "status": "candidate",
                "selection_authority": "system_director_required",
                "task_id": task["task_id"],
            }
            for role in self.list_roles(snapshot)
        )

    @staticmethod
    def _validate_schema(record: Mapping[str, Any], schema_name: str) -> ValidationResult:
        schema = Path(__file__).resolve().parents[3] / "schemas" / schema_name
        issues = validate_instance(record, schema)
        if issues:
            return ValidationResult(
                "fail",
                "adapter.record_invalid",
                tuple(format_issues(issues).splitlines()),
            )
        return ValidationResult("pass", evidence={"schema": schema_name})

    def validate_decision(self, decision: Mapping[str, Any]) -> ValidationResult:
        return self._validate_schema(decision, "director-decision.schema.json")

    def validate_job(self, job: Mapping[str, Any]) -> ValidationResult:
        result = self._validate_schema(job, "agent-job.schema.json")
        if result.blocking:
            return result
        if job.get("authority", {}).get("network_access") is True:
            return ValidationResult(
                "fail",
                "adapter.generic_network_authority_denied",
                ("Portable filesystem policy defaults to no network authority.",),
            )
        return result

    def compute_domain_fingerprint(self) -> Mapping[str, Any]:
        snapshot = self.load_authoritative_state()
        record_hashes = sorted(
            item["sha256"]
            for records in snapshot["records"].values()
            for item in records
        )
        policy_hashes = sorted(content_sha256(item) for item in snapshot["policies"])
        role_hashes = sorted(content_sha256(item) for item in snapshot["roles"])
        return {
            "adapter_id": self.adapter_id,
            "adapter_version": self.version,
            "canonical_source_roots": snapshot["canonical_source_roots"],
            "record_hashes": record_hashes,
            "policy_hashes": policy_hashes,
            "role_hashes": role_hashes,
            "domain_truth": "not_evaluated",
        }

    def evaluate_completion(self, completion: Mapping[str, Any]) -> ValidationResult:
        result = self._validate_schema(completion, "completion.schema.json")
        if result.blocking:
            return result
        return ValidationResult(
            "pass",
            "adapter.process_completion_valid",
            evidence={
                "process_completion": "validated",
                "domain_truth": "indeterminate",
                "scientific_promotion_authority": False,
            },
        )

    def conformance_claims(self) -> Mapping[str, Mapping[str, Any]]:
        native = {
            "mode": "native",
            "status": "pass",
            "evidence": ["FilesystemControlStore", "activation manifests"],
        }
        return {
            feature: copy.deepcopy(native)
            for feature in (
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
        }
