"""Read-only project discovery, control validation, and before-state capture."""

from __future__ import annotations

import copy
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.capabilities import bootstrap_required_report
from agentjob_runtime.config import LoadedConfig, load_config, resolve_project_path
from agentjob_runtime.control.activation import _format_cross_issues, _record_set
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.indexes import INDEX_NAMES, build_indexes
from agentjob_runtime.control.resolver import BoundaryResult, resolve_store
from agentjob_runtime.errors import AgentJobControlError, BootstrapRequired, RecordValidationError
from agentjob_runtime.fingerprinting.canonical import FingerprintResult, build_fingerprint
from agentjob_runtime.records.canonical import content_sha256, load_structured, render_canonical_json
from agentjob_runtime.validation.cross_record import validate_record_set
from agentjob_runtime.validation.schema import format_issues, validate_instance


@dataclass(frozen=True)
class ContinuePreflight:
    status: str
    boundary: Mapping[str, Any]
    project_root: str
    configuration_path: str | None
    profile: str | None
    capabilities: Mapping[str, Any]
    repository: Mapping[str, Any]
    control: Mapping[str, Any]
    fingerprint: str | None
    fingerprint_payload: Mapping[str, Any] | None
    authority_surfaces: tuple[Mapping[str, Any], ...]
    pending_gates: tuple[str, ...]
    conflicts: tuple[str, ...]
    execution_performed: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _run_git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
        timeout=15,
    )
    if result.returncode != 0:
        raise RecordValidationError(
            f"Git repository inspection failed: {' '.join(arguments)}",
            details={"reason_code": "repository.git_inspection_failed", "stderr": result.stderr.strip()},
        )
    return result.stdout.rstrip("\n")


def capture_repository(root: Path, provider: str) -> dict[str, Any]:
    if provider == "git":
        repository_root = Path(_run_git(root, "rev-parse", "--show-toplevel")).resolve()
        common = Path(_run_git(root, "rev-parse", "--git-common-dir"))
        if not common.is_absolute():
            common = (root / common).resolve()
        branch = _run_git(root, "branch", "--show-current") or None
        return {
            "provider": "git",
            "root": str(repository_root),
            "worktree": str(repository_root),
            "git_common_dir": str(common),
            "branch": branch,
            "revision": _run_git(root, "rev-parse", "HEAD"),
            "status_porcelain": _run_git(root, "status", "--porcelain=v1", "--untracked-files=all"),
        }
    if provider == "filesystem_only":
        return {
            "provider": "filesystem_only",
            "root": str(root),
            "worktree": str(root),
            "git_common_dir": None,
            "branch": None,
            "revision": content_sha256(
                sorted(
                    path.relative_to(root).as_posix()
                    for path in root.rglob("*")
                    if path.is_file() and ".local" not in path.relative_to(root).parts
                )
            ),
            "status_porcelain": "",
        }
    raise RecordValidationError(
        f"repository provider requires an injected adapter snapshot: {provider}",
        details={"reason_code": "repository.provider_requires_adapter"},
    )


def _load_policies(loaded: LoadedConfig) -> tuple[list[dict[str, Any]], list[str]]:
    policies: list[dict[str, Any]] = []
    findings: list[str] = []
    schema = Path(__file__).resolve().parents[3] / "schemas" / "policy-pack.schema.json"
    for relative in loaded.data["policy"]["packs"]:
        path = resolve_project_path(loaded.project_root, relative, purpose="policy pack")
        if not path.is_file():
            findings.append(f"policy_missing:{relative}")
            continue
        value = load_structured(path)
        if not isinstance(value, dict):
            findings.append(f"policy_not_mapping:{relative}")
            continue
        issues = validate_instance(value, schema)
        if issues:
            findings.extend(f"policy_invalid:{relative}:{line}" for line in format_issues(issues).splitlines())
            continue
        policies.append(value)
    return policies, findings


def _index_drift(store: FilesystemControlStore) -> list[str]:
    if not store.root.exists():
        return []
    expected = build_indexes(store)
    drift: list[str] = []
    for kind, index in expected.items():
        path = store.indexes_root / INDEX_NAMES[kind]
        actual = path.read_text(encoding="utf-8") if path.is_file() else None
        if actual != render_canonical_json(index):
            drift.append(f"index_drift:{store.relative(path)}")
    return drift


def _authority_surfaces(store: FilesystemControlStore) -> tuple[dict[str, Any], ...]:
    surfaces = []
    for kind, path, record in store.iter_records():
        surfaces.append(
            {
                "record_type": kind,
                "path": store.relative(path),
                "record_id": next(
                    (
                        value
                        for key, value in record.items()
                        if key.endswith("_id") and key not in {"parent_task_id", "source_task_ref"} and value
                    ),
                    None,
                ),
                "sha256": content_sha256(record),
            }
        )
    return tuple(sorted(surfaces, key=lambda item: (item["record_type"], item["path"])))


def _bootstrap(root: Path, error: AgentJobControlError) -> ContinuePreflight:
    report = bootstrap_required_report()
    details = copy.deepcopy(error.details)
    missing = details.get("missing_capabilities") or report["missing_capabilities"]
    boundary = BoundaryResult(
        "bootstrap_required",
        "capability.missing_required",
        stop_conditions=tuple(missing),
    ).as_dict()
    return ContinuePreflight(
        "bootstrap_required",
        boundary,
        str(root),
        None,
        None,
        {"status": "bootstrap_required", "missing_capabilities": list(missing), "execution_performed": False},
        {},
        {},
        None,
        None,
        (),
        (),
        tuple(str(item) for item in missing),
    )


def run_preflight(
    project_root: str | Path,
    *,
    config_path: str | Path | None = None,
    task_id: str | None = None,
    repository_snapshot: Mapping[str, Any] | None = None,
    provider_versions: Mapping[str, str] | None = None,
) -> ContinuePreflight:
    """Capture and classify direct state without mutating project files."""

    root = Path(project_root).expanduser().resolve()
    try:
        loaded = load_config(
            root,
            config_path=config_path,
            provider_versions=provider_versions,
        )
    except BootstrapRequired as error:
        return _bootstrap(root, error)
    if loaded.capabilities.status != "ready":
        error = BootstrapRequired(
            "required capabilities are unavailable",
            details={"missing_capabilities": list(loaded.capabilities.missing_capabilities)},
        )
        return _bootstrap(root, error)
    store = FilesystemControlStore(root, loaded.control_root)
    policies, integrity = _load_policies(loaded)
    try:
        records = _record_set(store, [])
        issues = validate_record_set(
            records,
            policies=policies,
            strict_extensions=bool(loaded.data["policy"]["strict_extensions"]),
        )
        integrity.extend(item["code"] for item in _format_cross_issues(issues))
        integrity.extend(_index_drift(store))
        repository = copy.deepcopy(
            dict(repository_snapshot)
            if repository_snapshot is not None
            else capture_repository(root, str(loaded.data["repository"]["provider"]))
        )
    except AgentJobControlError as error:
        integrity.append(error.code)
        repository = copy.deepcopy(dict(repository_snapshot or {}))
    boundary = resolve_store(
        store,
        capabilities=loaded.capabilities,
        task_id=task_id,
        integrity_findings=tuple(integrity),
    )
    snapshot = {
        "config_hash": content_sha256(loaded.data),
        "task_id": boundary.task_id,
        "task_hash": None,
        "decision_id": boundary.decision_id,
        "decision_hash": None,
        "job_id": boundary.job_id,
        "job_hash": None,
        "role_hash": None,
        "completion_id": None,
        "completion_hash": None,
        "handoff_id": None,
        "handoff_hash": None,
    }
    for surface in _authority_surfaces(store):
        if surface["record_type"] == "task" and surface["record_id"] == boundary.task_id:
            snapshot["task_hash"] = surface["sha256"]
        elif surface["record_type"] == "director_decision" and surface["record_id"] == boundary.decision_id:
            snapshot["decision_hash"] = surface["sha256"]
        elif surface["record_type"] == "agent_job" and surface["record_id"] == boundary.job_id:
            snapshot["job_hash"] = surface["sha256"]
        elif surface["record_type"] == "execution_role" and surface["record_id"] == boundary.execution_role_id:
            snapshot["role_hash"] = surface["sha256"]
    validation = {
        "required_validator_ids": list(loaded.data["validation"]["pre_execution"]),
        "outcomes": [
            {"validator_id": "control-record-validator", "status": "fail" if integrity else "pass"}
        ],
    }
    checkpoint = {
        "provider": str(loaded.data["checkpoint"]["provider"]),
        "status": "not_required",
        "revision": repository.get("revision"),
    }
    fingerprint_result: FingerprintResult | None = None
    if repository:
        fingerprint_result = build_fingerprint(
            [],
            repository=repository,
            control=snapshot,
            resolver={"boundary": boundary.boundary, "reason_code": boundary.reason_code},
            validation=validation,
            checkpoint=checkpoint,
            adapter_extensions={},
        )
    pending_gates = (
        tuple(boundary.required_authority_surfaces)
        if boundary.boundary == "human_gate_required"
        else ()
    )
    return ContinuePreflight(
        boundary.boundary,
        boundary.as_dict(),
        str(root),
        str(loaded.config_path),
        str(loaded.data["control"]["profile"]),
        loaded.capabilities.as_dict(),
        repository,
        snapshot,
        fingerprint_result.fingerprint if fingerprint_result else None,
        fingerprint_result.payload if fingerprint_result else None,
        _authority_surfaces(store),
        pending_gates,
        tuple(integrity) + tuple(boundary.stop_conditions),
    )
