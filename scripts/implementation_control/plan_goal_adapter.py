#!/usr/bin/env python3
"""Website authority adapter for the pinned implementation-plan relay.

The imported runtime owns plan scheduling, revisions, leases, provider intent,
and PlanTaskReceipt v2 records.  Website ``implementation_control/`` records
remain the only execution authority.  This module never instantiates the
imported generic ``.agents/control`` executor.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import secrets
import shlex
import stat
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_SCRIPTS = Path(__file__).resolve().parents[1]
VENDOR_SCRIPTS = (
    REPO_ROOT / ".agents" / "skills" / "agentjob-control" / "scripts"
)
PLANCTL_SCRIPTS = (
    REPO_ROOT / ".agents" / "skills" / "implementation-plan-goal" / "scripts"
)
for import_root in (PROJECT_SCRIPTS, VENDOR_SCRIPTS, PLANCTL_SCRIPTS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from implementation_control.continue_implementation import (  # noqa: E402
    NO_ACTION_STATUSES,
    load_yaml,
    resolve_continue_context,
)

from agentjob_runtime.adapters.conformance import run_conformance  # noqa: E402
from agentjob_runtime.adapters.protocols import (  # noqa: E402
    ADAPTER_CAPABILITY_VERSION,
    AdapterCapabilityReport,
    CanonicalPath,
    FeatureCapability,
    PathChange,
    RepositoryIdentity,
    RepositorySnapshot,
    RepositoryStatus,
    ValidationResult,
)
from agentjob_runtime.adapters.repository_git import (  # noqa: E402
    GitRepositoryProvider,
)
from agentjob_runtime.adapters.thread_manual import (  # noqa: E402
    ManualThreadProvider,
    adopt_manual_plan_successor,
)
from agentjob_runtime.continue_flow.director import DirectorRoute  # noqa: E402
from agentjob_runtime.errors import (  # noqa: E402
    AgentJobControlError,
    IntegrityError,
    RecordNotFound,
    RecordValidationError,
    StateConflict,
)
from agentjob_runtime.execution.activation_profile import (  # noqa: E402
    DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
)
from agentjob_runtime.goal.activation import (  # noqa: E402
    accept_activation as accept_goal_activation,
    create_activation_proposal as create_goal_activation_proposal,
    record_manual_current_thread_profile as record_goal_profile,
    render_combined_acceptance as render_goal_acceptance,
    request_current_thread_profile as request_goal_profile,
)
from agentjob_runtime.goal.initialize import initialize_goal  # noqa: E402
from agentjob_runtime.goal.model import (  # noqa: E402
    add_seconds,
    parse_utc,
    utc_now,
)
from agentjob_runtime.plan.activation import (  # noqa: E402
    accept_activation as accept_plan_activation,
    create_activation_proposal as create_plan_activation_proposal,
    record_manual_current_thread_profile as record_plan_profile,
    render_combined_acceptance as render_plan_acceptance,
    request_current_thread_profile as request_plan_profile,
)
from agentjob_runtime.plan.initialize import initialize_plan  # noqa: E402
from agentjob_runtime.plan.launcher import (  # noqa: E402
    PlanLauncherGuards,
    PlanSourceRequest,
    PlanTaskReservationResult,
    dispatch_reserved_plan_task,
    preflight_plan_launcher,
    reserve_first_plan_task,
    reserve_next_plan_task,
)
from agentjob_runtime.plan.model import require_implementation_plan  # noqa: E402
from agentjob_runtime.plan.normalize import (  # noqa: E402
    PrdToImplementationPlanAdapter,
    normalize_plan_preflight,
)
from agentjob_runtime.plan.prompts import (  # noqa: E402
    build_plan_task_dependency_proof,
)
from agentjob_runtime.plan.sqlite_store import SQLitePlanStore  # noqa: E402
from agentjob_runtime.plan.worker import (  # noqa: E402
    PlanTaskContinueInvocation,
    PlanWorkerPreclaim,
    _build_receipt,
    _unknown_continue_diagnostic,
    _unknown_continue_result,
    _validate_authority_record,
    claim_plan_task_generation,
    compile_plan_task_continue_invocation as compile_runtime_plan_task_invocation,
)
from agentjob_runtime.plan.verify import (  # noqa: E402
    verify_plan_task_result,
)
from agentjob_runtime.records.canonical import (  # noqa: E402
    canonical_json_bytes,
    content_sha256,
)
from agentjob_runtime.validation.schema import (  # noqa: E402
    format_issues,
    validate_instance,
)
from planctl import normalize_paths  # type: ignore[import-not-found] # noqa: E402


ADAPTER_CONFIG_RELATIVE = Path(
    ".agents/implementation-plan-goal/adapter-config.json"
)
PROVENANCE_RELATIVE = Path(
    ".agents/implementation-plan-goal/import-provenance.json"
)
CONFORMANCE_RELATIVE = Path(
    ".agents/implementation-plan-goal/adapter-conformance.json"
)
LOCK_RELATIVE = Path(
    ".agents/skill_registry/locks/implementation-plan-goal.lock.yaml"
)
PLAN_SCHEMA_ROOT_RELATIVE = Path(
    ".agents/skills/implementation-plan-goal/schemas"
)
STATE_RELATIVE = Path(
    ".local/sys4ai/implementation-plan-goal/state.sqlite3"
)
MANUAL_RELATIVE = Path(
    ".local/sys4ai/implementation-plan-goal/manual"
)
ADAPTER_RUNTIME_RELATIVE = Path(
    ".local/sys4ai/implementation-plan-goal/website-adapter"
)
CONTROL_ACTIVATION_RELATIVE = Path(
    ".local/sys4ai/implementation-plan-goal/control-activations"
)
ADOPTION_RELATIVE = Path(
    ".local/sys4ai/implementation-plan-goal/task-adoptions"
)
BINDING_ROOT_RELATIVE = Path("implementation_control/plan_bindings")
BINDING_SCHEMA_RELATIVE = Path(
    "implementation_control/schemas/plan-binding-v1.schema.json"
)
CONTROL_ACTIVATION_SCHEMA_RELATIVE = Path(
    "implementation_control/schemas/control-activation-receipt-v1.schema.json"
)
ADOPTION_SCHEMA_RELATIVE = Path(
    "implementation_control/schemas/codex-task-adoption-receipt-v1.schema.json"
)
PROGRAM_STATE_RELATIVE = Path("implementation_control/program_state.yaml")
EXPECTED_LOCK_SHA256 = (
    "a158c82edd140e0cfc637a780733a0a35241bfdb6083725e97e335441a6b7bb9"
)
EXPECTED_SKILLS = {
    "agentjob-control": (
        "0.3.0",
        "4fa0e93dc884e2c95ab3e0e01b3398c50aacacc91297574aabb456e1cc093c2d",
    ),
    "continue": (
        "0.3.0",
        "8ea81082ca76f77accaf4af2e839741b928817b6ff64761412fba71f0481294d",
    ),
    "continue-implementing-plan-task": (
        "0.1.0",
        "947c9d5b828746316d96874e253b772376978712e749ace48ef074fdbbcc7859",
    ),
    "implementation-plan-goal": (
        "0.1.0",
        "5c9320e736ae6314aaa794b57e488eb18488e73bc08031c6805493aa9a36ab76",
    ),
}
REQUIRED_HIGH_RISK_GATES = {
    "public_claim_changes",
    "source_refresh_uncertainty",
    "broad_navigation_or_route_retirement",
    "shared_visual_systems",
    "public_downloadable_assets",
    "public_manifest_authority_records",
    "git_push",
    "cloudflare_deployment",
    "upstream_source_project_writes",
}
NO_TOPOLOGY_ACTIONS = {
    "repository-branch-create",
    "repository-worktree-create",
    "repository-binding-change",
}


class WebsitePlanAdapterError(RuntimeError):
    """Protected adapter stop with one stable machine-readable reason."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.reason_code = reason_code
        self.details = dict(details or {})

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "protected_stop",
            "reason_code": self.reason_code,
            "message": str(self),
            "details": copy.deepcopy(self.details),
        }


def _protected(
    message: str,
    reason_code: str,
    **details: Any,
) -> WebsitePlanAdapterError:
    return WebsitePlanAdapterError(
        message,
        reason_code=reason_code,
        details=details,
    )


def canonical_json(value: Any) -> str:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _safe_relative_path(
    repo_root: Path,
    value: str | Path,
    *,
    label: str,
    must_exist: bool = False,
) -> tuple[Path, str]:
    supplied = Path(value)
    if supplied.is_absolute() or ".." in supplied.parts:
        raise _protected(
            f"{label} must remain project-relative",
            "security.path_escape",
            path=str(value),
        )
    root = repo_root.resolve(strict=True)
    resolved = (root / supplied).resolve(strict=must_exist)
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError as error:
        raise _protected(
            f"{label} escapes the website repository",
            "security.path_escape",
            path=str(value),
        ) from error
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise _protected(
                f"{label} traverses a symbolic link",
                "security.symlink",
                path=relative,
            )
    return resolved, relative


def _require_regular(path: Path, *, label: str) -> None:
    if not path.is_file() or path.is_symlink():
        raise _protected(
            f"{label} must be one regular unaliased file",
            "security.regular_file_required",
            path=str(path),
        )
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise _protected(
            f"{label} has an unsafe file identity",
            "security.regular_file_required",
            path=str(path),
        )


def _atomic_write(path: Path, payload: bytes, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_canonical_json(
    path: Path,
    value: Mapping[str, Any],
    *,
    append_only: bool = False,
) -> None:
    payload = canonical_json(value).encode("utf-8")
    if append_only and path.exists():
        _require_regular(path, label="append-only JSON artifact")
        if path.read_bytes() != payload:
            raise _protected(
                "append-only JSON artifact conflicts with existing bytes",
                "adapter.append_only_conflict",
                path=str(path),
            )
        return
    _atomic_write(path, payload)


def load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    _require_regular(path, label=label)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise _protected(
            f"{label} is not valid UTF-8 JSON",
            "adapter.invalid_json",
            path=str(path),
            error=type(error).__name__,
        ) from error
    if not isinstance(value, dict):
        raise _protected(
            f"{label} must contain one JSON object",
            "adapter.invalid_json",
            path=str(path),
        )
    return value


def load_adapter_config(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    value = load_json_object(
        repo_root / ADAPTER_CONFIG_RELATIVE,
        label="plan-goal adapter configuration",
    )
    if (
        value.get("canonical_execution_authority")
        != "implementation_control"
        or value.get("generic_executor_enabled") is not False
        or value.get("generic_control_root_enabled") is not False
        or value.get("plugin_distribution_enabled") is not False
        or value.get("state_path") != STATE_RELATIVE.as_posix()
    ):
        raise _protected(
            "plan-goal adapter configuration weakens the authority boundary",
            "adapter.configuration_invalid",
        )
    return value


def _git(repo_root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise _protected(
            f"git {' '.join(arguments)} failed",
            "plan.repository_mismatch",
            stderr=(completed.stderr or completed.stdout).strip(),
        )
    return completed.stdout.strip()


@dataclass(frozen=True)
class RepositoryEvidence:
    binding: Mapping[str, Any] = field(repr=False)
    topology: Mapping[str, Any] = field(repr=False)
    binding_sha256: str
    topology_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "binding": copy.deepcopy(dict(self.binding)),
            "topology": copy.deepcopy(dict(self.topology)),
            "binding_sha256": self.binding_sha256,
            "topology_sha256": self.topology_sha256,
        }


class WebsiteRepositoryProvider:
    """Read-only exact-checkout and default-deny topology provider."""

    provider_id = "website-git-repository"

    def __init__(self, repo_root: Path = REPO_ROOT) -> None:
        self.repo_root = Path(repo_root).resolve(strict=True)
        self._git_provider = GitRepositoryProvider(self.repo_root)

    def identity(self) -> RepositoryIdentity:
        """Return the imported provider's exact Git checkout identity."""

        identity = self._git_provider.identity()
        return RepositoryIdentity(
            self.provider_id,
            identity.root,
            identity.worktree,
            identity.common_dir,
            identity.branch,
            identity.revision,
            identity.detached,
        )

    def status(self) -> RepositoryStatus:
        """Return normalized read-only Git status evidence."""

        status = self._git_provider.status()
        return RepositoryStatus(
            self.provider_id,
            status.revision,
            status.porcelain,
            status.changed_paths,
            status.clean,
        )

    def snapshot(self) -> RepositorySnapshot:
        """Capture file hashes for direct before/after task evidence."""

        snapshot = self._git_provider.snapshot()
        return RepositorySnapshot(
            self.identity(),
            self.status(),
            copy.deepcopy(dict(snapshot.files)),
        )

    def changed_paths(
        self,
        before: RepositorySnapshot,
        after: RepositorySnapshot,
    ) -> Sequence[PathChange]:
        return self._git_provider.changed_paths(before, after)

    def canonicalize_path(self, value: str) -> CanonicalPath:
        return self._git_provider.canonicalize_path(value)

    def fingerprint_payload(self) -> Mapping[str, Any]:
        snapshot = self.snapshot()
        return {
            "identity": snapshot.identity.as_dict(),
            "status": snapshot.status.as_dict(),
            "files": copy.deepcopy(dict(snapshot.files)),
        }

    def observe(self) -> RepositoryEvidence:
        identity = self.identity()
        root = Path(identity.root).resolve(strict=True)
        if root != self.repo_root:
            raise _protected(
                "repository provider root differs from the requested checkout",
                "plan.repository_mismatch",
            )
        if identity.detached or not identity.branch:
            raise _protected(
                "detached checkout is not accepted without one-shot authority",
                "plan.repository_mismatch",
            )
        binding = {
            "project_id": "The-AEther-Flow-Website",
            "root": str(root),
            "worktree": identity.worktree,
            "branch": identity.branch,
            "starting_revision": identity.revision,
            "git_common_dir": identity.common_dir,
            "environment_mode": "local",
        }
        topology = {
            "root": str(root),
            "worktree": identity.worktree,
            "branch": identity.branch,
            "git_common_dir": identity.common_dir,
            "revision": identity.revision,
            "local_branches": sorted(
                line
                for line in _git(
                    root,
                    "for-each-ref",
                    "--format=%(refname:short)",
                    "refs/heads",
                ).splitlines()
                if line
            ),
            "registered_worktrees": sorted(
                line
                for line in _git(root, "worktree", "list", "--porcelain").splitlines()
                if line.startswith("worktree ")
            ),
            "worktree_bindings": [],
        }
        return RepositoryEvidence(
            binding=binding,
            topology=topology,
            binding_sha256=content_sha256(binding),
            topology_sha256=content_sha256(topology),
        )

    @staticmethod
    def require_same_checkout(
        accepted: RepositoryEvidence,
        observed: RepositoryEvidence,
    ) -> None:
        identity_fields = ("root", "worktree", "branch", "git_common_dir")
        if any(
            accepted.binding.get(key) != observed.binding.get(key)
            for key in identity_fields
        ):
            raise _protected(
                "repository topology drifted from the accepted checkout",
                "plan.repository_mismatch",
            )
        if (
            accepted.topology.get("local_branches")
            != observed.topology.get("local_branches")
            or accepted.topology.get("registered_worktrees")
            != observed.topology.get("registered_worktrees")
        ):
            raise _protected(
                "branch or worktree topology changed without one-shot authority",
                "plan.repository_topology_changed",
            )


def _pointer(value: Any, *keys: str) -> str | None:
    if isinstance(value, str) and value:
        return value
    if isinstance(value, Mapping):
        for key in keys:
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate:
                return candidate
    return None


def _safe_record_id(value: Any, *, label: str) -> str:
    allowed = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789._:-"
    )
    if (
        not isinstance(value, str)
        or not 3 <= len(value) <= 160
        or value[0] not in allowed[:62]
        or any(character not in allowed for character in value)
    ):
        raise _protected(
            f"{label} is not a safe record identity",
            "security.path_identity_invalid",
        )
    return value


@dataclass(frozen=True)
class WebsiteControlSnapshot:
    control_sha256: str
    payload: Mapping[str, Any] = field(repr=False)
    resolver: Mapping[str, Any] = field(repr=False)
    resolver_exit_code: int
    repository: RepositoryEvidence = field(repr=False)

    def as_dict(self) -> dict[str, Any]:
        return {
            "control_sha256": self.control_sha256,
            "resolver_status": self.resolver.get("status"),
            "resolver_exit_code": self.resolver_exit_code,
            "repository_binding_sha256": self.repository.binding_sha256,
            "repository_topology_sha256": self.repository.topology_sha256,
            "selected": copy.deepcopy(
                dict(self.payload.get("selected", {}))
            ),
        }


def _record_projection(
    repo_root: Path,
    relative: str | None,
    *,
    label: str,
) -> dict[str, Any] | None:
    if relative is None:
        return None
    path, normalized = _safe_relative_path(
        repo_root,
        relative,
        label=label,
        must_exist=True,
    )
    _require_regular(path, label=label)
    value = load_yaml(path)
    return {"path": normalized, "record": value}


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    raise TypeError(f"unsupported YAML scalar: {type(value).__name__}")


def _yaml_list_scalar(value: Any) -> str:
    rendered = _yaml_scalar(value)
    if isinstance(value, str):
        # The repository's deliberately small YAML reader identifies list
        # mappings before it parses quoted scalars.  Preserve literal colons
        # through JSON's equivalent escape so a scalar cannot be mistaken for
        # a mapping entry.
        return rendered.replace(":", "\\u003a")
    return rendered


def _yaml_lines(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if isinstance(value, Mapping):
        if not value:
            return [prefix + "{}"]
        lines: list[str] = []
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("YAML mapping keys must be strings")
            if isinstance(item, Mapping):
                if item:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(_yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: {{}}")
            elif isinstance(item, list):
                if item:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(_yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}: {_yaml_scalar(item)}")
        return lines
    if isinstance(value, list):
        if not value:
            return [prefix + "[]"]
        result: list[str] = []
        for item in value:
            if isinstance(item, Mapping):
                if not item:
                    result.append(prefix + "- {}")
                    continue
                first, *remaining = item.items()
                key, first_value = first
                if isinstance(first_value, (Mapping, list)):
                    result.append(f"{prefix}- {key}:")
                    result.extend(_yaml_lines(first_value, indent + 4))
                else:
                    result.append(
                        f"{prefix}- {key}: {_yaml_scalar(first_value)}"
                    )
                for nested_key, nested_value in remaining:
                    if isinstance(nested_value, (Mapping, list)):
                        if nested_value:
                            result.append(
                                f"{' ' * (indent + 2)}{nested_key}:"
                            )
                            result.extend(
                                _yaml_lines(nested_value, indent + 4)
                            )
                        else:
                            empty = "{}" if isinstance(nested_value, Mapping) else "[]"
                            result.append(
                                f"{' ' * (indent + 2)}{nested_key}: {empty}"
                            )
                    else:
                        result.append(
                            f"{' ' * (indent + 2)}{nested_key}: "
                            f"{_yaml_scalar(nested_value)}"
                        )
            elif isinstance(item, list):
                result.append(prefix + "-")
                result.extend(_yaml_lines(item, indent + 2))
            else:
                result.append(f"{prefix}- {_yaml_list_scalar(item)}")
        return result
    return [prefix + _yaml_scalar(value)]


def render_yaml(value: Mapping[str, Any]) -> bytes:
    return ("\n".join(_yaml_lines(value)) + "\n").encode("utf-8")


class WebsiteControlStore:
    """Emulated portable ControlStore over canonical website YAML records."""

    adapter_id = "the-aether-flow-website-implementation-control"
    version = "1.0.0"

    def __init__(
        self,
        repo_root: Path = REPO_ROOT,
        *,
        repository_provider: WebsiteRepositoryProvider | None = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve(strict=True)
        self.repository_provider = (
            repository_provider or WebsiteRepositoryProvider(self.repo_root)
        )

    def snapshot(self) -> WebsiteControlSnapshot:
        program_path = self.repo_root / PROGRAM_STATE_RELATIVE
        _require_regular(program_path, label="website program state")
        program = load_yaml(program_path)
        active = program.get("active_task")
        current = program.get("current_job")
        handoff = program.get("latest_handoff")
        selected = {
            "task": _record_projection(
                self.repo_root,
                _pointer(active, "path"),
                label="selected website task",
            ),
            "job": _record_projection(
                self.repo_root,
                _pointer(current, "path"),
                label="selected website job",
            ),
            "handoff": _record_projection(
                self.repo_root,
                _pointer(handoff, "yaml_path", "path"),
                label="selected website handoff",
            ),
        }
        repository = self.repository_provider.observe()
        try:
            resolver, exit_code = resolve_continue_context(self.repo_root)
        except Exception as error:
            resolver = {
                "status": "blocked",
                "reason_code": "website.control_malformed",
                "error": type(error).__name__,
            }
            exit_code = 2
        payload = {
            "schema_version": "website.control-cas.v1",
            "program_state": {
                "path": PROGRAM_STATE_RELATIVE.as_posix(),
                "record": program,
            },
            "selected": selected,
            "repository_identity": copy.deepcopy(dict(repository.binding)),
        }
        return WebsiteControlSnapshot(
            control_sha256=content_sha256(payload),
            payload=payload,
            resolver=resolver,
            resolver_exit_code=exit_code,
            repository=repository,
        )

    def resolve_current(self) -> Mapping[str, Any]:
        snapshot = self.snapshot()
        return {
            **copy.deepcopy(dict(snapshot.resolver)),
            "website_control_sha256": snapshot.control_sha256,
        }

    def conformance_claims(self) -> Mapping[str, Mapping[str, Any]]:
        report = load_json_object(
            self.repo_root / CONFORMANCE_RELATIVE,
            label="website adapter conformance",
        )
        return {
            str(item["feature_id"]): {
                "mode": item["mode"],
                "status": item["status"],
                "evidence": item["evidence"],
            }
            for item in report.get("checks", [])
            if isinstance(item, Mapping) and item.get("feature_id")
        }

    @staticmethod
    def _gate_map(entry: Mapping[str, Any]) -> dict[str, Any]:
        return {
            str(item["id"]): {
                "status": str(item["status"]),
                "reason": str(item["reason"]),
            }
            for item in entry["approval_gates"]
        }

    def stage_packet(
        self,
        packet: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Build one exact website packet only from a validated binding."""

        entry = copy.deepcopy(dict(packet["binding"]))
        plan = copy.deepcopy(dict(packet["plan"]))
        now = str(packet.get("timestamp") or utc_now())
        parse_utc(now)
        ids = copy.deepcopy(dict(entry["packet_ids"]))
        task_id = str(ids["task_id"])
        job_id = str(ids["job_id"])
        handoff_id = str(ids["handoff_id"])
        task_path = Path(
            f"implementation_control/tasks/{task_id}/00_TASK.yaml"
        )
        job_path = Path(
            f"implementation_control/tasks/{task_id}/jobs/{job_id}.yaml"
        )
        handoff_path = Path(
            f"implementation_control/handoffs/{handoff_id}.yaml"
        )
        handoff_markdown_path = Path(
            f"implementation_control/handoffs/{handoff_id}.md"
        )
        gates = self._gate_map(entry)
        task_record = {
            "schema_version": "0.1",
            "record_type": "implementation_task",
            "task_id": task_id,
            "title": entry["objective"],
            "created_utc": now,
            "updated_utc": now,
            "status": "active",
            "source_context": {
                "plan_id": plan["plan_id"],
                "plan_sha256": content_sha256(plan),
                "plan_task_id": entry["task_id"],
                "plan_task_sha256": entry["task_sha256"],
                "binding_manifest_sha256": packet[
                    "binding_manifest_sha256"
                ],
                "authority_sha256": entry["authority_sha256"],
                "implementation_authority": "implementation_control only",
            },
            "goal": entry["objective"],
            "requirements": list(entry["acceptance_criteria"]),
            "scope": {
                "in_scope": list(entry["allowed_writes"]),
                "out_of_scope": [
                    "Any path, task, claim, or effect absent from this exact binding."
                ],
            },
            "allowed_reads": {
                "website_repository": list(entry["allowed_reads"])
            },
            "allowed_writes": {
                "website_repository": list(entry["allowed_writes"]),
                "upstream_source_repository": [],
            },
            "approval_gates": gates,
            "required_validators": list(entry["validators"]),
            "stop_conditions": list(entry["stop_conditions"]),
            "checkpoint_expectations": {
                "automated_checkpoint_command_available": bool(
                    entry["checkpoint_rights"]["commit"]
                ),
                "staging_allowed_by_this_job": bool(
                    entry["checkpoint_rights"]["stage"]
                ),
                "commit_allowed_by_this_job": bool(
                    entry["checkpoint_rights"]["commit"]
                ),
                "branch_allowed_by_this_job": bool(
                    entry["checkpoint_rights"]["branch"]
                ),
                "worktree_allowed_by_this_job": bool(
                    entry["checkpoint_rights"]["worktree"]
                ),
                "push_allowed_by_this_job": bool(
                    entry["checkpoint_rights"]["push"]
                ),
                "deploy_allowed_by_this_job": bool(
                    entry["checkpoint_rights"]["deploy"]
                ),
            },
            "execution_role": copy.deepcopy(entry["execution_role"]),
            "handoff": {
                "latest_handoff_id": handoff_id,
                "yaml_path": handoff_path.as_posix(),
                "markdown_path": handoff_markdown_path.as_posix(),
            },
            "next_recommended_action": {
                "task_packet": entry["task_id"],
                "summary": entry["objective"],
                "do_not_skip": "Do not broaden the hash-bound website packet.",
            },
        }
        job_record = {
            "schema_version": "0.1",
            "record_type": "implementation_job",
            "job_id": job_id,
            "task_id": task_id,
            "title": entry["objective"],
            "created_utc": now,
            "updated_utc": now,
            "status": "active",
            "objective": entry["objective"],
            "plan_binding": copy.deepcopy(task_record["source_context"]),
            "execution_boundary": {
                "invocation_limit": "one mapped website job",
                "implementation_authority": "implementation_control only",
                "generic_executor_status": "forbidden",
            },
            "allowed_reads": list(entry["allowed_reads"]),
            "allowed_writes": list(entry["allowed_writes"]),
            "required_outputs": list(entry["acceptance_criteria"]),
            "approval_gates": [
                {
                    "id": gate_id,
                    "status": value["status"],
                    "trigger": value["reason"],
                }
                for gate_id, value in gates.items()
            ],
            "required_validators": list(entry["validators"]),
            "stop_conditions": list(entry["stop_conditions"]),
            "checkpoint": {
                "staging_allowed": bool(entry["checkpoint_rights"]["stage"]),
                "commit_allowed": bool(entry["checkpoint_rights"]["commit"]),
                "branch_allowed": bool(entry["checkpoint_rights"]["branch"]),
                "worktree_allowed": bool(
                    entry["checkpoint_rights"]["worktree"]
                ),
                "push_allowed": bool(entry["checkpoint_rights"]["push"]),
                "deploy_allowed": bool(entry["checkpoint_rights"]["deploy"]),
            },
            "execution_role": copy.deepcopy(entry["execution_role"]),
            "next_recommended_action": {
                "task_packet": entry["task_id"],
                "summary": entry["objective"],
                "do_not_skip": "Execute only this mapped packet.",
            },
        }
        handoff_record = {
            "schema_version": "0.1",
            "record_type": "implementation_handoff",
            "handoff_id": handoff_id,
            "created_utc": now,
            "updated_utc": now,
            "status": "active",
            "task_id": task_id,
            "job_id": job_id,
            "summary": (
                f"Plan task {entry['task_id']} is mapped to one active "
                "website implementation packet."
            ),
            "plan_binding": copy.deepcopy(task_record["source_context"]),
            "current_state": [
                "The imported plan scheduler selected exactly one task.",
                "The website packet remains sole execution authority.",
                "The worker may invoke local continue once.",
            ],
            "next_recommended_action": {
                "task_packet": entry["task_id"],
                "summary": entry["objective"],
                "do_not_skip": "Do not select a successor in the worker.",
            },
            "stop_before": list(entry["stop_conditions"]),
        }
        program_record = {
            "schema_version": "0.1",
            "record_type": "implementation_program_state",
            "repository": "The-AEther-Flow-Website",
            "updated_utc": now,
            "status": "active",
            "mode": "website_local_implementation_control",
            "authority_order": [
                "AGENTS.md",
                PROGRAM_STATE_RELATIVE.as_posix(),
                task_path.as_posix(),
                job_path.as_posix(),
                handoff_path.as_posix(),
                "current_git_state_and_validator_output",
            ],
            "repository_boundary": {
                "website_repository": ".",
                "upstream_source_repository": (
                    "/Volumes/P-SSD/AngryOwl/The-AEther-Flow"
                ),
                "upstream_write_status": "forbidden",
                "deployment_status": (
                    "authorized"
                    if entry["checkpoint_rights"]["deploy"]
                    else "not_authorized"
                ),
            },
            "active_task": {
                "task_id": task_id,
                "title": entry["objective"],
                "status": "active",
                "path": task_path.as_posix(),
                "planning_context": copy.deepcopy(
                    task_record["source_context"]
                ),
            },
            "current_job": {
                "job_id": job_id,
                "status": "active",
                "path": job_path.as_posix(),
            },
            "latest_handoff": {
                "handoff_id": handoff_id,
                "status": "active",
                "yaml_path": handoff_path.as_posix(),
                "markdown_path": handoff_markdown_path.as_posix(),
            },
            "required_validators": [
                {
                    "id": item["id"],
                    "command": item["command"],
                    "required_for_current_job": item["required"],
                }
                for item in entry["validators"]
            ],
            "next_recommended_action": {
                "task_packet": entry["task_id"],
                "summary": entry["objective"],
                "do_not_skip": "Execute only the mapped website job.",
            },
            "implementation_status": {
                "status": "plan_task_active",
                "plan_id": plan["plan_id"],
                "plan_task_id": entry["task_id"],
                "plan_task_sha256": entry["task_sha256"],
                "binding_manifest_sha256": packet[
                    "binding_manifest_sha256"
                ],
                "authority_sha256": entry["authority_sha256"],
            },
        }
        markdown = (
            f"# Handoff {handoff_id}\n\n"
            f"Plan task `{entry['task_id']}` maps to website task "
            f"`{task_id}` and job `{job_id}`.\n\n"
            "This handoff is continuity evidence only. It grants no authority "
            "beyond the hash-bound YAML packet.\n"
        ).encode("utf-8")
        records = {
            PROGRAM_STATE_RELATIVE.as_posix(): render_yaml(program_record),
            task_path.as_posix(): render_yaml(task_record),
            job_path.as_posix(): render_yaml(job_record),
            handoff_path.as_posix(): render_yaml(handoff_record),
            handoff_markdown_path.as_posix(): markdown,
        }
        return {
            "records": records,
            "task_id": task_id,
            "job_id": job_id,
            "handoff_id": handoff_id,
            "plan_task_id": entry["task_id"],
            "plan_task_sha256": entry["task_sha256"],
            "authority_sha256": entry["authority_sha256"],
            "binding_manifest_sha256": packet[
                "binding_manifest_sha256"
            ],
            "timestamp": now,
        }

    def activate_packet(
        self,
        staged: Mapping[str, Any],
        expected_revision: str,
    ) -> dict[str, Any]:
        """CAS-activate exactly one staged packet with rollback on write error."""

        before = self.snapshot()
        if before.control_sha256 != expected_revision:
            raise _protected(
                "website control compare-and-swap conflict",
                "website.control_hash_conflict",
                expected=expected_revision,
                actual=before.control_sha256,
            )
        records = staged.get("records")
        if not isinstance(records, Mapping) or len(records) != 5:
            raise _protected(
                "staged website packet is incomplete",
                "website.packet_invalid",
            )
        backups: dict[Path, bytes | None] = {}
        written: list[Path] = []
        try:
            for relative, payload in records.items():
                if not isinstance(relative, str) or not isinstance(
                    payload, bytes
                ):
                    raise _protected(
                        "staged website record bytes are invalid",
                        "website.packet_invalid",
                    )
                path, _ = _safe_relative_path(
                    self.repo_root,
                    relative,
                    label="staged website record",
                )
                backups[path] = path.read_bytes() if path.exists() else None
                _atomic_write(path, payload, mode=0o644)
                written.append(path)
            after = self.snapshot()
        except Exception:
            for path in reversed(written):
                original = backups[path]
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    _atomic_write(path, original, mode=0o644)
            raise
        selected = after.payload["selected"]
        task_record = selected.get("task", {}).get("record", {})
        job_record = selected.get("job", {}).get("record", {})
        handoff_record = selected.get("handoff", {}).get("record", {})
        if (
            task_record.get("task_id") != staged["task_id"]
            or job_record.get("job_id") != staged["job_id"]
            or handoff_record.get("handoff_id") != staged["handoff_id"]
            or after.resolver_exit_code != 0
            or after.resolver.get("status") != "ready"
        ):
            for path in reversed(written):
                original = backups[path]
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    _atomic_write(path, original, mode=0o644)
            raise _protected(
                "materialized website packet did not resolve as one ready job",
                "website.packet_activation_failed",
            )
        basis = {
            "schema_version": "website.control-activation-receipt.v1",
            "receipt_id": (
                "WCAR-"
                + content_sha256(
                    {
                        "plan_task_id": staged["plan_task_id"],
                        "before": before.control_sha256,
                        "after": after.control_sha256,
                    }
                )[:24]
            ),
            "plan_id": task_record["source_context"]["plan_id"],
            "task_id": staged["plan_task_id"],
            "task_sha256": staged["plan_task_sha256"],
            "binding_manifest_sha256": staged[
                "binding_manifest_sha256"
            ],
            "authority_sha256": staged["authority_sha256"],
            "website_control_sha256_before": before.control_sha256,
            "website_control_sha256_after": after.control_sha256,
            "repository_identity_sha256": after.repository.binding_sha256,
            "activated_paths": sorted(records),
            "activated_at": staged["timestamp"],
            "receipt_content_sha256": "",
            "finalized": True,
        }
        basis["receipt_content_sha256"] = content_sha256(
            {
                key: value
                for key, value in basis.items()
                if key != "receipt_content_sha256"
            }
        )
        schema = self.repo_root / CONTROL_ACTIVATION_SCHEMA_RELATIVE
        findings = validate_instance(basis, schema)
        if findings:
            raise _protected(
                "website control activation receipt failed validation",
                "website.activation_receipt_invalid",
                findings=format_issues(findings).splitlines(),
            )
        path = (
            self.repo_root
            / CONTROL_ACTIVATION_RELATIVE
            / str(basis["plan_id"])
            / f"{basis['task_id']}.json"
        )
        write_canonical_json(path, basis, append_only=True)
        return {
            "status": "activated",
            "website_control_sha256_before": before.control_sha256,
            "website_control_sha256_after": after.control_sha256,
            "receipt": basis,
            "receipt_path": path.relative_to(self.repo_root).as_posix(),
        }

    def _write_records_with_cas(
        self,
        records: Mapping[str, bytes],
        *,
        expected_control_sha256: str,
    ) -> tuple[WebsiteControlSnapshot, WebsiteControlSnapshot]:
        before = self.snapshot()
        if before.control_sha256 != expected_control_sha256:
            raise _protected(
                "website control compare-and-swap conflict",
                "website.control_hash_conflict",
                expected=expected_control_sha256,
                actual=before.control_sha256,
            )
        backups: dict[Path, bytes | None] = {}
        written: list[Path] = []
        try:
            for relative, payload in records.items():
                if not isinstance(relative, str) or not isinstance(
                    payload, bytes
                ):
                    raise _protected(
                        "website control mutation is malformed",
                        "website.packet_invalid",
                    )
                path, _ = _safe_relative_path(
                    self.repo_root,
                    relative,
                    label="website control mutation",
                )
                backups[path] = path.read_bytes() if path.exists() else None
                _atomic_write(path, payload, mode=0o644)
                written.append(path)
        except Exception:
            for path in reversed(written):
                original = backups[path]
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    _atomic_write(path, original, mode=0o644)
            raise
        try:
            after = self.snapshot()
        except Exception:
            for path in reversed(written):
                original = backups[path]
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    _atomic_write(path, original, mode=0o644)
            raise
        return before, after

    def supersede_packet(self, request: Mapping[str, Any]) -> dict[str, Any]:
        """Close one selected packet while retaining historical provenance."""

        expected = str(request.get("expected_control_sha256", ""))
        timestamp = str(request.get("timestamp") or utc_now())
        parse_utc(timestamp)
        before = self.snapshot()
        if before.resolver.get("status") == "no_action":
            return {
                "status": "no_action",
                "website_control_sha256": before.control_sha256,
                "execution_performed": False,
            }
        selected = before.payload["selected"]
        required = ("task", "job", "handoff")
        if any(not isinstance(selected.get(key), Mapping) for key in required):
            raise _protected(
                "selected website packet is incomplete",
                "website.packet_invalid",
            )
        program = copy.deepcopy(
            dict(before.payload["program_state"]["record"])
        )
        records: dict[str, bytes] = {}
        for key in required:
            projection = selected[key]
            record = copy.deepcopy(dict(projection["record"]))
            record["status"] = "superseded"
            record["updated_utc"] = timestamp
            records[str(projection["path"])] = render_yaml(record)
        program["status"] = "inactive"
        program["updated_utc"] = timestamp
        if isinstance(program.get("active_task"), Mapping):
            program["active_task"]["status"] = "superseded"
        program["current_job"] = {}
        if isinstance(program.get("latest_handoff"), Mapping):
            program["latest_handoff"]["status"] = "superseded"
        program["required_validators"] = []
        program["next_recommended_action"] = {
            "task_packet": "none",
            "summary": "Open a fresh bounded packet before execution.",
            "do_not_skip": "Historical pointers grant no authority.",
        }
        records[PROGRAM_STATE_RELATIVE.as_posix()] = render_yaml(program)
        _, after = self._write_records_with_cas(
            records,
            expected_control_sha256=expected,
        )
        if after.resolver.get("status") != "no_action":
            raise _protected(
                "superseded website packet did not reach no-action state",
                "website.packet_activation_failed",
            )
        return {
            "status": "superseded",
            "website_control_sha256_before": before.control_sha256,
            "website_control_sha256_after": after.control_sha256,
        }

    def load_task(self, task_id: str) -> Mapping[str, Any]:
        identity = _safe_record_id(task_id, label="website task ID")
        path = (
            self.repo_root
            / "implementation_control"
            / "tasks"
            / identity
            / "00_TASK.yaml"
        )
        _require_regular(path, label="website task")
        value = load_yaml(path)
        if value.get("task_id") != identity:
            raise _protected(
                "website task identity differs from its path",
                "website.packet_invalid",
            )
        return value

    def write_completion(
        self,
        request: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Append one website completion through an explicit control CAS."""

        expected = str(request.get("expected_control_sha256", ""))
        value = request.get("record")
        if not isinstance(value, Mapping):
            raise _protected(
                "website completion request lacks one record",
                "website.packet_invalid",
            )
        completion = copy.deepcopy(dict(value))
        completion_id = _safe_record_id(
            completion.get("completion_id"),
            label="website completion ID",
        )
        task_id = _safe_record_id(
            completion.get("task_id"),
            label="website task ID",
        )
        if (
            completion.get("record_type") != "implementation_completion"
            or completion.get("status") not in {"complete", "completed"}
        ):
            raise _protected(
                "website completion record is not final",
                "website.packet_invalid",
            )
        relative = (
            f"implementation_control/tasks/{task_id}/jobs/completions/"
            f"{completion_id}.yaml"
        )
        path = self.repo_root / relative
        if path.exists():
            raise _protected(
                "website completion record already exists",
                "website.append_only_conflict",
            )
        before, after = self._write_records_with_cas(
            {relative: render_yaml(completion)},
            expected_control_sha256=expected,
        )
        return {
            "status": "written",
            "path": relative,
            "website_control_sha256_before": before.control_sha256,
            "website_control_sha256_after": after.control_sha256,
        }

    def write_handoff(self, request: Mapping[str, Any]) -> dict[str, Any]:
        """Write one exact YAML handoff through an explicit control CAS."""

        expected = str(request.get("expected_control_sha256", ""))
        value = request.get("record")
        if not isinstance(value, Mapping):
            raise _protected(
                "website handoff request lacks one record",
                "website.packet_invalid",
            )
        handoff = copy.deepcopy(dict(value))
        handoff_id = _safe_record_id(
            handoff.get("handoff_id"),
            label="website handoff ID",
        )
        if handoff.get("record_type") != "implementation_handoff":
            raise _protected(
                "website handoff record type is invalid",
                "website.packet_invalid",
            )
        relative = f"implementation_control/handoffs/{handoff_id}.yaml"
        before, after = self._write_records_with_cas(
            {relative: render_yaml(handoff)},
            expected_control_sha256=expected,
        )
        return {
            "status": "written",
            "path": relative,
            "website_control_sha256_before": before.control_sha256,
            "website_control_sha256_after": after.control_sha256,
        }

    def regenerate_indexes(self) -> dict[str, Any]:
        """Report the website control system's no-index contract."""

        snapshot = self.snapshot()
        return {
            "status": "not_required",
            "website_control_sha256": snapshot.control_sha256,
            "execution_performed": False,
        }


class WebsiteProjectAdapter:
    """ProjectAdapter view over website-native control authority."""

    adapter_id = "the-aether-flow-website"
    version = "1.0.0"
    _FEATURES = (
        "task-records",
        "director-decisions",
        "agentjob-records",
        "execution-role-bindings",
        "completion-records",
        "handoffs",
        "immutable-activation",
        "supersession",
        "one-job-cardinality",
        "claim-boundary",
        "path-boundary",
        "recovery-evidence",
    )

    def __init__(self, project_root: Path = REPO_ROOT) -> None:
        self.project_root = Path(project_root).resolve(strict=True)
        self.control_store = WebsiteControlStore(self.project_root)

    def discover(self, project_root: Path) -> AdapterCapabilityReport:
        root = Path(project_root).resolve(strict=True)
        available = root == self.project_root
        if available:
            load_adapter_config(root)
            _require_regular(
                root / PROGRAM_STATE_RELATIVE,
                label="website program state",
            )
        features = tuple(
            FeatureCapability(
                feature_id,
                "1.0.0",
                True,
                available,
                "emulated" if available else "unsupported",
                None if available else "adapter.project_root_mismatch",
            )
            for feature_id in self._FEATURES
        )
        return AdapterCapabilityReport(
            self.adapter_id,
            self.version,
            ADAPTER_CAPABILITY_VERSION,
            features,
            ("implementation_control",),
            ("domain-truth-promotion",),
            (
                "conformance_claims",
                "validate_decision",
                "validate_job",
                "evaluate_completion",
            ),
        )

    def load_authoritative_state(self) -> Mapping[str, Any]:
        snapshot = self.control_store.snapshot()
        return {
            "adapter": self.discover(self.project_root).as_dict(),
            "configuration": load_adapter_config(self.project_root),
            "canonical_source_roots": ["implementation_control"],
            "control": copy.deepcopy(dict(snapshot.payload)),
            "resolver": copy.deepcopy(dict(snapshot.resolver)),
            "domain_truth": "not_evaluated",
        }

    def list_roles(
        self,
        snapshot: Mapping[str, Any],
    ) -> Sequence[Mapping[str, Any]]:
        selected = snapshot.get("control", {}).get("selected", {})
        task = (
            selected.get("task", {}).get("record")
            if isinstance(selected, Mapping)
            else None
        )
        role = task.get("execution_role") if isinstance(task, Mapping) else None
        if not isinstance(role, Mapping):
            return ()
        return (
            {
                **copy.deepcopy(dict(role)),
                "source_ref": selected["task"]["path"],
            },
        )

    def list_routes(
        self,
        snapshot: Mapping[str, Any],
    ) -> Sequence[Mapping[str, Any]]:
        selected = snapshot.get("control", {}).get("selected", {})
        task = (
            selected.get("task", {}).get("record")
            if isinstance(selected, Mapping)
            else None
        )
        roles = self.list_roles(snapshot)
        if not isinstance(task, Mapping) or len(roles) != 1:
            return ()
        role = roles[0]
        return (
            {
                "route_id": f"website-binding:{task['task_id']}",
                "role_id": role["role_id"],
                "role_version": role["role_version"],
                "status": "selected",
                "selection_authority": "validated_plan_binding",
                "task_id": task["task_id"],
            },
        )

    def _validate_imported_record(
        self,
        value: Mapping[str, Any],
        schema_name: str,
    ) -> ValidationResult:
        schema = (
            self.project_root
            / ".agents"
            / "skills"
            / "agentjob-control"
            / "schemas"
            / schema_name
        )
        findings = validate_instance(value, schema)
        if findings:
            return ValidationResult(
                "fail",
                "adapter.record_invalid",
                tuple(format_issues(findings).splitlines()),
            )
        return ValidationResult(
            "pass",
            evidence={"schema": schema_name},
        )

    def validate_decision(
        self,
        decision: Mapping[str, Any],
    ) -> ValidationResult:
        return self._validate_imported_record(
            decision,
            "director-decision.schema.json",
        )

    def validate_job(
        self,
        job: Mapping[str, Any],
    ) -> ValidationResult:
        result = self._validate_imported_record(
            job,
            "agent-job.schema.json",
        )
        if result.blocking:
            return result
        if job.get("authority", {}).get("network_access") is True:
            return ValidationResult(
                "fail",
                "adapter.network_authority_denied",
                ("Website plan jobs default to no network authority.",),
            )
        return result

    def compute_domain_fingerprint(self) -> Mapping[str, Any]:
        snapshot = self.control_store.snapshot()
        return {
            "adapter_id": self.adapter_id,
            "adapter_version": self.version,
            "canonical_source_roots": ["implementation_control"],
            "control_sha256": snapshot.control_sha256,
            "repository_binding_sha256": (
                snapshot.repository.binding_sha256
            ),
            "repository_topology_sha256": (
                snapshot.repository.topology_sha256
            ),
            "domain_truth": "not_evaluated",
        }

    def evaluate_completion(
        self,
        completion: Mapping[str, Any],
    ) -> ValidationResult:
        if (
            completion.get("record_type") != "implementation_completion"
            or completion.get("status") not in {"complete", "completed"}
            or not isinstance(completion.get("validator_results"), list)
        ):
            return ValidationResult(
                "fail",
                "adapter.process_completion_invalid",
                ("Website completion lacks final validator evidence.",),
            )
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
        return self.control_store.conformance_claims()


class WebsiteThreadExecutionProfileProvider:
    """Explicit manual profile attestation for one exact Codex task."""

    provider_id = "manual-handoff"

    def __init__(
        self,
        *,
        thread_id: str,
        reasoning_effort: str,
        evidence_ref: str,
    ) -> None:
        if not all(
            isinstance(value, str) and value.strip()
            for value in (thread_id, reasoning_effort, evidence_ref)
        ):
            raise _protected(
                "thread profile attestation is incomplete",
                "thread.profile_evidence_missing",
            )
        self.thread_id = thread_id
        self.reasoning_effort = reasoning_effort
        self.evidence_ref = evidence_ref

    def capabilities(self) -> Mapping[str, Any]:
        return {
            "provider_id": self.provider_id,
            "available": True,
            "automatic": False,
            "can_configure_current_thread": False,
            "can_verify_effective_reasoning_effort": True,
            "can_reconfigure_unclaimed_successor": False,
            "supported_reasoning_efforts": [
                "minimal",
                "low",
                "medium",
                "high",
                "xhigh",
                "max",
            ],
        }

    def configure_current_thread(
        self,
        thread_id: str,
        *,
        reasoning_effort: str,
    ) -> Mapping[str, Any]:
        if (
            thread_id != self.thread_id
            or reasoning_effort != self.reasoning_effort
        ):
            raise _protected(
                "current thread profile differs from explicit attestation",
                "thread.profile_mismatch",
            )
        return self.read_thread_profile(thread_id)

    def read_thread_profile(self, thread_id: str) -> Mapping[str, Any]:
        if thread_id != self.thread_id:
            raise _protected(
                "profile evidence belongs to a different Codex task",
                "thread.profile_mismatch",
            )
        return {
            "status": "verified",
            "thread_id": self.thread_id,
            "effective_reasoning_effort": self.reasoning_effort,
            "evidence_ref": self.evidence_ref,
            "provider_id": self.provider_id,
        }

    def reconfigure_unclaimed_successor(
        self,
        thread_id: str,
        *,
        reasoning_effort: str,
    ) -> Mapping[str, Any]:
        raise _protected(
            "manual profile evidence cannot reconfigure a Codex task",
            "thread.reconfiguration_unsupported",
            thread_id=thread_id,
            reasoning_effort=reasoning_effort,
        )


def _task_authority_basis(entry: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in entry.items()
        if key != "authority_sha256"
    }


def _validate_task_binding_entry(
    task_id: str,
    task: Mapping[str, Any],
    entry: Mapping[str, Any],
) -> None:
    """Validate one task binding without granting manifest authority."""

    validator_ids = [str(item["id"]) for item in entry["validators"]]
    validator_commands = [
        str(item["command"]) for item in entry["validators"]
    ]
    gates = {str(item["id"]): item for item in entry["approval_gates"]}
    if (
        entry["task_id"] != task_id
        or entry["task_sha256"] != task["task_sha256"]
        or entry["objective"] != task["objective"]
        or entry["acceptance_criteria"] != task["acceptance_criteria"]
        or validator_commands != task["validation_refs"]
    ):
        raise _protected(
            "plan binding task projection differs from canonical task identity",
            "plan.binding_task_mismatch",
            task_id=task_id,
        )
    if (
        len(set(validator_ids)) != len(validator_ids)
        or not all(item["required"] is True for item in entry["validators"])
    ):
        raise _protected(
            "canonical plan validators must remain unique and required",
            "plan.binding_validator_mismatch",
            task_id=task_id,
        )
    for kind in ("allowed_reads", "allowed_writes"):
        for path_rule in entry[kind]:
            supplied = Path(str(path_rule).removesuffix("/**"))
            if (
                supplied.is_absolute()
                or ".." in supplied.parts
                or str(path_rule) in {"", ".", "*", "**"}
            ):
                raise _protected(
                    "plan binding contains an unsafe authority path",
                    "plan.binding_path_invalid",
                    task_id=task_id,
                    authority_field=kind,
                    path=path_rule,
                )
    if (
        set(gates) != REQUIRED_HIGH_RISK_GATES
        or gates["upstream_source_project_writes"]["status"]
        != "blocked"
    ):
        raise _protected(
            "plan binding lacks the complete website high-risk gate map",
            "plan.binding_gate_mismatch",
            task_id=task_id,
        )
    rights = entry["checkpoint_rights"]
    if rights["branch"] or rights["worktree"]:
        raise _protected(
            "binding cannot grant Git topology authority",
            "plan.topology_authority_required",
            task_id=task_id,
        )
    if entry["authority_sha256"] != content_sha256(
        _task_authority_basis(entry)
    ):
        raise _protected(
            "plan binding task authority hash is invalid",
            "plan.binding_authority_hash_mismatch",
            task_id=task_id,
        )


def validate_binding_manifest(
    plan: Mapping[str, Any],
    binding: Mapping[str, Any],
    *,
    schema_path: Path,
) -> dict[str, Any]:
    """Require a complete exact task-to-packet map before acceptance."""

    value = copy.deepcopy(dict(binding))
    findings = validate_instance(value, schema_path)
    if findings:
        raise _protected(
            "plan binding failed schema validation",
            "plan.binding_invalid",
            findings=format_issues(findings).splitlines(),
        )
    plan_hash = content_sha256(plan)
    if (
        value["plan_id"] != plan["plan_id"]
        or value["plan_sha256"] != plan_hash
    ):
        raise _protected(
            "plan binding identity differs from canonical plan bytes",
            "plan.binding_hash_mismatch",
        )
    expected_tasks = {
        str(item["task_id"]): copy.deepcopy(dict(item))
        for item in plan["tasks"]
    }
    if set(value["tasks"]) != set(expected_tasks):
        raise _protected(
            "plan binding must map every canonical task exactly once",
            "plan.binding_incomplete",
            expected=sorted(expected_tasks),
            actual=sorted(value["tasks"]),
        )
    packet_ids: set[str] = set()
    for task_id, task in expected_tasks.items():
        entry = value["tasks"][task_id]
        _validate_task_binding_entry(task_id, task, entry)
        for packet_id in entry["packet_ids"].values():
            if packet_id in packet_ids:
                raise _protected(
                    "website packet IDs must be unique across a binding",
                    "plan.binding_packet_identity_conflict",
                    packet_id=packet_id,
                )
            packet_ids.add(str(packet_id))
    expected_manifest_hash = content_sha256(
        {
            key: item
            for key, item in value.items()
            if key != "manifest_sha256"
        }
    )
    if value["manifest_sha256"] != expected_manifest_hash:
        raise _protected(
            "plan binding manifest hash is invalid",
            "plan.binding_hash_mismatch",
        )
    return value


def load_project_plan(
    path: str | Path,
    *,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    resolved, relative = _safe_relative_path(
        repo_root,
        path,
        label="canonical plan",
        must_exist=True,
    )
    value = load_json_object(resolved, label="canonical plan")
    if value.get("schema_version") != "sys4ai.implementation-plan.v2":
        raise _protected(
            "only a separately accepted canonical v2 plan may execute",
            "plan.legacy_read_only",
            path=relative,
        )
    try:
        return require_implementation_plan(
            value,
            schema_path=(
                repo_root
                / PLAN_SCHEMA_ROOT_RELATIVE
                / "implementation-plan.schema.json"
            ),
        )
    except AgentJobControlError as error:
        raise _protected(
            "canonical plan failed imported runtime validation",
            "plan.validation_failed",
            details=getattr(error, "details", {}),
        ) from error


def load_plan_binding(
    plan: Mapping[str, Any],
    path: str | Path | None = None,
    *,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    relative = (
        Path(path)
        if path is not None
        else BINDING_ROOT_RELATIVE / f"{plan['plan_id']}.yaml"
    )
    resolved, _ = _safe_relative_path(
        repo_root,
        relative,
        label="plan binding",
        must_exist=True,
    )
    _require_regular(resolved, label="plan binding")
    return validate_binding_manifest(
        plan,
        load_yaml(resolved),
        schema_path=repo_root / BINDING_SCHEMA_RELATIVE,
    )


def _require_replacement_binding_authorization(
    *,
    store: SQLitePlanStore,
    plan_record: Mapping[str, Any],
    session: Mapping[str, Any],
    base_binding: Mapping[str, Any],
    task_id: str,
    repo_root: Path,
) -> dict[str, Any]:
    authorizations = session.get("replacement_binding_authorizations")
    authorization = (
        authorizations.get(task_id)
        if isinstance(authorizations, Mapping)
        else None
    )
    if not isinstance(authorization, Mapping):
        raise _protected(
            "replacement plan task lacks explicit binding authorization",
            "plan.binding_authorization_missing",
            task_id=task_id,
        )
    required_authorization_fields = {
        "status",
        "approved_at",
        "approval_ref",
        "authorized_plan_revision",
        "authorized_website_control_sha256",
        "task_authority_sha256",
        "replacement_binding_content_sha256",
        "compatibility_writes",
        "external_effects_authorized",
        "replacement_binding",
        "task_definition",
    }
    if set(authorization) != required_authorization_fields:
        raise _protected(
            "replacement binding authorization fields are not exact",
            "plan.binding_authorization_invalid",
            task_id=task_id,
        )
    try:
        parse_utc(str(authorization["approved_at"]))
    except (TypeError, ValueError) as error:
        raise _protected(
            "replacement binding approval timestamp is invalid",
            "plan.binding_authorization_invalid",
            task_id=task_id,
        ) from error
    compatibility_writes = authorization["compatibility_writes"]
    if (
        authorization["status"] != "approved"
        or not isinstance(authorization["approval_ref"], str)
        or not authorization["approval_ref"].strip()
        or isinstance(authorization["authorized_plan_revision"], bool)
        or not isinstance(authorization["authorized_plan_revision"], int)
        or authorization["authorized_plan_revision"] < 0
        or authorization["authorized_plan_revision"]
        > int(plan_record["state"]["revision"])
        or authorization["external_effects_authorized"] is not False
        or not isinstance(compatibility_writes, list)
        or not compatibility_writes
        or len(set(compatibility_writes)) != len(compatibility_writes)
        or any(
            not isinstance(path, str)
            or Path(path.removesuffix("/**")).is_absolute()
            or ".." in Path(path.removesuffix("/**")).parts
            or path in {"", ".", "*", "**"}
            for path in compatibility_writes
        )
    ):
        raise _protected(
            "replacement binding authorization is not an approved bounded delta",
            "plan.binding_authorization_invalid",
            task_id=task_id,
        )

    supplement = authorization["replacement_binding"]
    task = authorization["task_definition"]
    if not isinstance(supplement, Mapping) or not isinstance(task, Mapping):
        raise _protected(
            "replacement binding evidence is malformed",
            "plan.binding_authorization_invalid",
            task_id=task_id,
        )
    required_supplement_fields = {
        "schema_version",
        "record_type",
        "status",
        "plan_id",
        "plan_sha256",
        "base_binding_manifest_sha256",
        "supersession_id",
        "supersession_sha256",
        "plan_revision",
        "task",
        "hash_basis",
        "binding_content_sha256",
    }
    if (
        set(supplement) != required_supplement_fields
        or supplement["schema_version"]
        != "website.plan-task-replacement-binding.v1"
        or supplement["record_type"]
        != "implementation_plan_task_replacement_binding"
        or supplement["status"] != "non_executable"
        or supplement["plan_id"] != plan_record["plan_id"]
        or supplement["plan_sha256"]
        not in {
            plan_record["plan_sha256"],
            plan_record["effective_plan_sha256"],
        }
        or supplement["base_binding_manifest_sha256"]
        != base_binding["manifest_sha256"]
        or supplement["plan_revision"]
        != authorization["authorized_plan_revision"]
        or supplement["hash_basis"]
        != "canonical_json_without_binding_content_sha256"
        or supplement["binding_content_sha256"]
        != authorization["replacement_binding_content_sha256"]
        or supplement["binding_content_sha256"]
        != content_sha256(
            {
                key: copy.deepcopy(value)
                for key, value in supplement.items()
                if key != "binding_content_sha256"
            }
        )
    ):
        raise _protected(
            "replacement binding content differs from accepted bytes",
            "plan.binding_hash_mismatch",
            task_id=task_id,
        )

    entry = supplement["task"]
    expected_task_fields = {
        "task_id",
        "task_sha256",
        "phase_id",
        "title",
        "objective",
        "depends_on",
        "acceptance_criteria",
        "validation_refs",
        "execution_budget",
        "extensions",
    }
    if (
        set(task) != expected_task_fields
        or task["task_id"] != task_id
        or task["task_sha256"]
        != content_sha256(
            {
                key: copy.deepcopy(value)
                for key, value in task.items()
                if key != "task_sha256"
            }
        )
        or not isinstance(entry, Mapping)
    ):
        raise _protected(
            "replacement task definition does not match its accepted hash",
            "plan.binding_task_mismatch",
            task_id=task_id,
        )
    wrapper = {
        "schema_version": "website.plan-binding.v1",
        "record_type": "implementation_plan_binding",
        "status": "non_executable",
        "plan_id": plan_record["plan_id"],
        "plan_sha256": plan_record["plan_sha256"],
        "binding_revision": 1,
        "tasks": {task_id: copy.deepcopy(dict(entry))},
        "manifest_sha256": "0" * 64,
    }
    wrapper["manifest_sha256"] = content_sha256(
        {
            key: copy.deepcopy(value)
            for key, value in wrapper.items()
            if key != "manifest_sha256"
        }
    )
    findings = validate_instance(
        wrapper, repo_root / BINDING_SCHEMA_RELATIVE
    )
    if findings:
        raise _protected(
            "replacement task binding failed schema validation",
            "plan.binding_invalid",
            task_id=task_id,
            findings=format_issues(findings).splitlines(),
        )
    _validate_task_binding_entry(task_id, task, entry)
    if (
        entry["authority_sha256"]
        != authorization["task_authority_sha256"]
    ):
        raise _protected(
            "replacement task authority differs from accepted bytes",
            "plan.binding_authority_hash_mismatch",
            task_id=task_id,
        )

    runtime_definition = store.load_task_definition(
        str(plan_record["plan_id"]), task_id
    )
    runtime_task = runtime_definition.get("task_json", {})
    budget = task["execution_budget"]
    if (
        runtime_definition.get("origin_kind") != "replacement"
        or runtime_definition.get("task_sha256") != task["task_sha256"]
        or runtime_definition.get("phase_id") != task["phase_id"]
        or runtime_definition.get("depends_on") != task["depends_on"]
        or runtime_task.get("one_task_per_discussion")
        != budget["one_task_per_discussion"]
        or runtime_task.get("max_continue_invocations")
        != budget["max_continue_invocations"]
        or runtime_task.get("max_agentjobs") != budget["max_agentjobs"]
        or budget.get("same_task_successors") != 0
    ):
        raise _protected(
            "replacement binding differs from canonical scheduling identity",
            "plan_task.identity_mismatch",
            task_id=task_id,
        )
    supersession = next(
        (
            item
            for item in store.list_supersessions(
                str(plan_record["plan_id"])
            )
            if item["supersession_id"] == supplement["supersession_id"]
        ),
        None,
    )
    replacement_ids = {
        item["task_id"]
        for item in supersession.get("replacement_tasks", [])
    } if isinstance(supersession, Mapping) else set()
    if (
        not isinstance(supersession, Mapping)
        or content_sha256(supersession)
        != supplement["supersession_sha256"]
        or task_id not in replacement_ids
    ):
        raise _protected(
            "replacement binding lacks its exact append-only supersession",
            "plan.binding_authorization_invalid",
            task_id=task_id,
        )
    occupied_packet_ids = {
        str(packet_id)
        for value in base_binding["tasks"].values()
        for packet_id in value["packet_ids"].values()
    }
    if occupied_packet_ids.intersection(
        str(value) for value in entry["packet_ids"].values()
    ):
        raise _protected(
            "replacement binding reuses a canonical website packet ID",
            "plan.binding_packet_identity_conflict",
            task_id=task_id,
        )
    return {
        "entry": copy.deepcopy(dict(entry)),
        "task_definition": copy.deepcopy(dict(task)),
        "binding_manifest_sha256": supplement[
            "binding_content_sha256"
        ],
        "authorized_website_control_sha256": authorization[
            "authorized_website_control_sha256"
        ],
        "compatibility_writes": copy.deepcopy(compatibility_writes),
        "replacement": True,
    }


def resolve_effective_task_binding(
    *,
    store: SQLitePlanStore,
    plan_record: Mapping[str, Any],
    session: Mapping[str, Any],
    base_binding: Mapping[str, Any],
    task_id: str,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Resolve a canonical or explicitly authorized replacement binding."""

    entry = base_binding["tasks"].get(task_id)
    if isinstance(entry, Mapping):
        runtime_definition = store.load_task_definition(
            str(plan_record["plan_id"]), task_id
        )
        return {
            "entry": copy.deepcopy(dict(entry)),
            "task_definition": copy.deepcopy(
                dict(runtime_definition["task_json"])
            ),
            "binding_manifest_sha256": base_binding[
                "manifest_sha256"
            ],
            "authorized_website_control_sha256": None,
            "compatibility_writes": [],
            "replacement": False,
        }
    return _require_replacement_binding_authorization(
        store=store,
        plan_record=plan_record,
        session=session,
        base_binding=base_binding,
        task_id=task_id,
        repo_root=repo_root,
    )


def directory_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for current_root, directory_names, file_names in os.walk(
        path, followlinks=False
    ):
        directory_names[:] = sorted(
            name
            for name in directory_names
            if name not in {".DS_Store", "__pycache__", ".pytest_cache"}
        )
        current = Path(current_root)
        for directory_name in directory_names:
            if (current / directory_name).is_symlink():
                raise _protected(
                    "installed skill contains a directory symlink",
                    "installation.symlink_present",
                )
        for file_name in sorted(file_names):
            if (
                file_name == ".DS_Store"
                or file_name.endswith((".pyc", ".pyo"))
            ):
                continue
            item = current / file_name
            if item.is_symlink():
                raise _protected(
                    "installed skill contains a file symlink",
                    "installation.symlink_present",
                )
            if not item.is_file():
                continue
            relative = item.relative_to(path).as_posix().encode("utf-8")
            digest.update(len(relative).to_bytes(8, "big"))
            digest.update(relative)
            content = item.read_bytes()
            digest.update(len(content).to_bytes(8, "big"))
            digest.update(content)
    return digest.hexdigest()


def verify_installed_bundle(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    lock = repo_root / LOCK_RELATIVE
    if not lock.is_file() or file_sha256(lock) != EXPECTED_LOCK_SHA256:
        raise _protected(
            "installed bundle lock differs from the source pin",
            "installation.lock_mismatch",
        )
    observed: dict[str, Any] = {}
    for skill_id, (version, expected_hash) in EXPECTED_SKILLS.items():
        root = repo_root / ".agents" / "skills" / skill_id
        if not root.is_dir():
            raise _protected(
                "installed skill is missing",
                "installation.skill_missing",
                skill_id=skill_id,
            )
        caches = [
            item.relative_to(root).as_posix()
            for item in root.rglob("*")
            if (
                item.name in {"__pycache__", ".pytest_cache"}
                or item.suffix in {".pyc", ".pyo"}
                or item.name == ".local"
            )
        ]
        if caches:
            raise _protected(
                "installed skill contains mutable or cache data",
                "installation.mutable_data_present",
                skill_id=skill_id,
                paths=sorted(caches),
            )
        actual_hash = directory_sha256(root)
        if actual_hash != expected_hash:
            raise _protected(
                "installed skill hash differs from the pinned package",
                "installation.skill_hash_mismatch",
                skill_id=skill_id,
                expected=expected_hash,
                actual=actual_hash,
            )
        observed[skill_id] = {
            "version": version,
            "source_sha256": actual_hash,
        }
    return {
        "status": "pass",
        "lock_sha256": EXPECTED_LOCK_SHA256,
        "packages": observed,
        "plugin_distribution_enabled": False,
    }


@dataclass(frozen=True)
class PreparedPlan:
    plan: Mapping[str, Any] = field(repr=False)
    binding: Mapping[str, Any] = field(repr=False)
    repository: RepositoryEvidence = field(repr=False)
    control: WebsiteControlSnapshot = field(repr=False)
    launcher_preflight: Any = field(repr=False)
    normalization: Any = field(repr=False)
    plan_proposal: Mapping[str, Any] = field(repr=False)
    goal_proposal: Mapping[str, Any] = field(repr=False)
    completion_contract: Mapping[str, Any] = field(repr=False)
    acceptance_basis: Mapping[str, Any] = field(repr=False)
    acceptance_text: str

    @property
    def acceptance_basis_sha256(self) -> str:
        return content_sha256(self.acceptance_basis)

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "acceptance_required",
            "plan_id": self.plan["plan_id"],
            "plan_sha256": content_sha256(self.plan),
            "binding_manifest_sha256": self.binding["manifest_sha256"],
            "reasoning_effort": self.acceptance_basis[
                "reasoning_effort"
            ],
            "website_control_sha256": self.control.control_sha256,
            "repository_binding_sha256": self.repository.binding_sha256,
            "repository_topology_sha256": self.repository.topology_sha256,
            "acceptance_basis_sha256": self.acceptance_basis_sha256,
            "acceptance_text_sha256": hashlib.sha256(
                self.acceptance_text.encode("utf-8")
            ).hexdigest(),
            "acceptance_text": self.acceptance_text,
            "authorization": copy.deepcopy(
                dict(self.acceptance_basis["authorization"])
            ),
            "effects": {
                "state_writes": 0,
                "provider_create_calls": 0,
                "worker_discussions": 0,
                "agentjobs": 0,
                "continue_invocations": 0,
            },
        }


def _completion_contract(plan: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "interpretation": (
            "Complete every required canonical plan task serially through "
            "its exact website implementation-control binding."
        ),
        "required_evidence": [
            "Every required task has one finalized PlanTaskReceipt v2.",
            "Every mapped website packet has direct completion and validator evidence.",
            "No unauthorized topology or external effect occurred.",
        ],
        "user_confirmed_when_ambiguous": True,
    }


def prepare_plan(
    *,
    plan_path: str | Path,
    binding_path: str | Path | None,
    goal_text: str | None,
    reasoning_effort: str,
    current_thread_id: str,
    current_profile_evidence_ref: str,
    repo_root: Path = REPO_ROOT,
) -> PreparedPlan:
    """Read-only complete preflight and exact combined-acceptance rendering."""

    verify_installed_bundle(repo_root)
    plan = load_project_plan(plan_path, repo_root=repo_root)
    binding = load_plan_binding(
        plan,
        binding_path,
        repo_root=repo_root,
    )
    exact_goal = goal_text if goal_text is not None else str(plan["objective"])
    if exact_goal != plan["objective"]:
        raise _protected(
            "activation goal must exactly match the accepted plan objective",
            "plan_activation.amendment_required",
        )
    repository = WebsiteRepositoryProvider(repo_root).observe()
    if dict(plan["repository_binding"]) != dict(repository.binding):
        raise _protected(
            "canonical plan repository binding differs from the live checkout",
            "plan.repository_mismatch",
            accepted_sha256=content_sha256(plan["repository_binding"]),
            observed_sha256=repository.binding_sha256,
        )
    project_adapter = WebsiteProjectAdapter(repo_root)
    project_capabilities = project_adapter.discover(repo_root)
    project_capabilities.require(project_adapter._FEATURES)
    profile_provider = WebsiteThreadExecutionProfileProvider(
        thread_id=current_thread_id,
        reasoning_effort=reasoning_effort,
        evidence_ref=current_profile_evidence_ref,
    )
    profile_provider.configure_current_thread(
        current_thread_id,
        reasoning_effort=reasoning_effort,
    )
    control = WebsiteControlStore(repo_root).snapshot()
    provider = ManualThreadProvider(
        repo_root,
        local_root=MANUAL_RELATIVE,
        current_thread_id=current_thread_id,
    )
    plan_relative = _safe_relative_path(
        repo_root,
        plan_path,
        label="canonical plan",
        must_exist=True,
    )[1]
    launcher = preflight_plan_launcher(
        project_root=repo_root,
        repository_binding=repository.binding,
        repository_observation=repository.binding,
        local_state_root=STATE_RELATIVE.parent.as_posix(),
        state_path=STATE_RELATIVE.as_posix(),
        source_requests=(
            PlanSourceRequest(plan_relative, "accepted", 0),
        ),
        guards=PlanLauncherGuards(
            max_sources=1,
            max_source_bytes=8 * 1024 * 1024,
            max_total_source_bytes=8 * 1024 * 1024,
            max_provider_creates=1,
            max_agentjobs=0,
        ),
        capabilities={
            "agentjob_control": True,
            "plan_state": True,
            "repository_provider": True,
            "thread_provider": True,
            "thread_execution_profile": True,
            "repository_topology_enforcement": True,
        },
        provider=provider,
    )
    normalization = normalize_plan_preflight(
        launcher,
        planning_adapter=PrdToImplementationPlanAdapter(normalize_paths),
        plan_schema_path=(
            repo_root
            / PLAN_SCHEMA_ROOT_RELATIVE
            / "implementation-plan.schema.json"
        ),
        normalization_report_schema_path=(
            repo_root
            / PLAN_SCHEMA_ROOT_RELATIVE
            / "normalization-report.schema.json"
        ),
    )
    if (
        not normalization.ready_for_initialization
        or normalization.candidate_plan != plan
    ):
        raise _protected(
            "canonical plan was not preserved by imported normalization",
            "plan.normalization_mismatch",
        )
    plan_proposal = create_plan_activation_proposal(
        goal_text=exact_goal,
        plan_id=str(plan["plan_id"]),
        accepted_plan_sha256=content_sha256(plan),
        plan_objective=str(plan["objective"]),
        repository_binding=repository.binding,
        current_thread_id=current_thread_id,
        provider_id=provider.provider_id,
        reasoning_effort=reasoning_effort,
        selection_source=(
            "default" if reasoning_effort == "max" else "user_override"
        ),
        repository_topology_policy=DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
    )
    plan_proposal = request_plan_profile(
        plan_proposal,
        provider=provider,
    )
    plan_proposal = record_plan_profile(
        plan_proposal,
        effective_effort=reasoning_effort,
        evidence_ref=current_profile_evidence_ref,
    )
    plan_proposal, plan_acceptance_text = render_plan_acceptance(
        plan_proposal
    )
    completion_contract = _completion_contract(plan)
    goal_proposal = create_goal_activation_proposal(
        goal_text=exact_goal,
        completion_contract=completion_contract,
        repository_binding=repository.binding,
        current_thread_id=current_thread_id,
        provider_id=provider.provider_id,
        reasoning_effort=reasoning_effort,
        selection_source=(
            "default" if reasoning_effort == "max" else "user_override"
        ),
        repository_topology_policy=DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
    )
    goal_proposal = request_goal_profile(
        goal_proposal,
        provider=provider,
    )
    goal_proposal = record_goal_profile(
        goal_proposal,
        effective_effort=reasoning_effort,
        evidence_ref=current_profile_evidence_ref,
    )
    goal_proposal, _ = render_goal_acceptance(goal_proposal)
    acceptance_basis = {
        "schema_version": "website.plan-combined-acceptance.v1",
        "goal_text": exact_goal,
        "goal_sha256": hashlib.sha256(
            exact_goal.encode("utf-8")
        ).hexdigest(),
        "reasoning_effort": reasoning_effort,
        "plan_id": plan["plan_id"],
        "plan_sha256": content_sha256(plan),
        "binding_manifest_sha256": binding["manifest_sha256"],
        "binding_revision": binding["binding_revision"],
        "website_control_sha256": control.control_sha256,
        "repository_binding": copy.deepcopy(dict(repository.binding)),
        "repository_binding_sha256": repository.binding_sha256,
        "repository_topology": copy.deepcopy(dict(repository.topology)),
        "repository_topology_sha256": repository.topology_sha256,
        "current_thread_id": current_thread_id,
        "current_profile_evidence_ref": current_profile_evidence_ref,
        "installation_lock_sha256": EXPECTED_LOCK_SHA256,
        "authorization": {
            "fresh_local_codex_tasks": True,
            "reuse_existing_checkout": True,
            "branch_creation": False,
            "worktree_creation": False,
            "generic_executor": False,
            "public_or_remote_effects": False,
        },
    }
    acceptance_text = (
        plan_acceptance_text
        + "\n\nWebsite binding:\n"
        + f"- plan SHA-256: {acceptance_basis['plan_sha256']}\n"
        + "- binding manifest SHA-256: "
        + f"{acceptance_basis['binding_manifest_sha256']}\n"
        + "- website control SHA-256: "
        + f"{acceptance_basis['website_control_sha256']}\n"
        + "- repository binding SHA-256: "
        + f"{acceptance_basis['repository_binding_sha256']}\n"
        + "- repository topology SHA-256: "
        + f"{acceptance_basis['repository_topology_sha256']}\n"
        + "- authorization: create fresh local Codex tasks in this exact "
        "checkout; no branch, worktree, generic executor, public, or remote "
        "effect authority.\n\n"
        + "Accepting this presentation accepts all values above together."
    )
    return PreparedPlan(
        plan=plan,
        binding=binding,
        repository=repository,
        control=control,
        launcher_preflight=launcher,
        normalization=normalization,
        plan_proposal=plan_proposal,
        goal_proposal=goal_proposal,
        completion_contract=completion_contract,
        acceptance_basis=acceptance_basis,
        acceptance_text=acceptance_text,
    )


class PlanControlStore:
    """Project-local PlanControlStore over the imported SQLite v5 runtime."""

    def __init__(
        self,
        repo_root: Path = REPO_ROOT,
        *,
        read_only: bool = False,
    ) -> None:
        self.repo_root = Path(repo_root).resolve(strict=True)
        self.path = self.repo_root / STATE_RELATIVE
        self.read_only = read_only
        if read_only and not self.path.is_file():
            self.store: SQLitePlanStore | None = None
        else:
            self.store = SQLitePlanStore(
                self.path,
                schema_root=self.repo_root / PLAN_SCHEMA_ROOT_RELATIVE,
                read_only=read_only,
                auto_migrate=not read_only,
            )

    def require_store(self) -> SQLitePlanStore:
        if self.store is None:
            raise _protected(
                "plan store is not initialized",
                "plan.not_initialized",
            )
        return self.store

    def assert_revision(self, plan_id: str, expected_revision: int) -> None:
        if isinstance(expected_revision, bool) or expected_revision < 0:
            raise _protected(
                "expected plan revision must be a non-negative integer",
                "plan.revision_conflict",
            )
        store = self.require_store()
        try:
            record = store.load_plan(plan_id)
        except RecordNotFound:
            if expected_revision == 0:
                return
            raise _protected(
                "expected plan does not exist",
                "plan.revision_conflict",
                expected=expected_revision,
                actual=None,
            )
        actual = int(record["state"]["revision"])
        if actual != expected_revision:
            raise _protected(
                "plan revision compare-and-swap conflict",
                "plan.revision_conflict",
                expected=expected_revision,
                actual=actual,
            )

    def session_path(self, plan_id: str) -> Path:
        if not plan_id or any(
            character
            not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._:-"
            for character in plan_id
        ):
            raise _protected(
                "plan ID is unsafe for adapter session storage",
                "security.path_identity_invalid",
            )
        return (
            self.repo_root
            / ADAPTER_RUNTIME_RELATIVE
            / "sessions"
            / f"{plan_id}.json"
        )

    def load_session(self, plan_id: str) -> dict[str, Any] | None:
        path = self.session_path(plan_id)
        if not path.is_file():
            return None
        return load_json_object(path, label="plan adapter session")

    def write_session(
        self,
        plan_id: str,
        value: Mapping[str, Any],
        *,
        expected_adapter_revision: int | None,
    ) -> dict[str, Any]:
        if self.read_only:
            raise _protected(
                "read-only plan store cannot write adapter state",
                "adapter.read_only",
            )
        current = self.load_session(plan_id)
        actual = int(current["adapter_revision"]) if current else 0
        if (
            expected_adapter_revision is not None
            and actual != expected_adapter_revision
        ):
            raise _protected(
                "adapter session compare-and-swap conflict",
                "adapter.revision_conflict",
                expected=expected_adapter_revision,
                actual=actual,
            )
        result = copy.deepcopy(dict(value))
        result["schema_version"] = "website.plan-adapter-session.v1"
        result["plan_id"] = plan_id
        result["adapter_revision"] = actual + 1
        result["updated_at"] = utc_timestamp()
        write_canonical_json(self.session_path(plan_id), result)
        return result

    def status(self, plan_id: str | None = None) -> dict[str, Any]:
        if self.store is None:
            return {
                "status": "not_initialized",
                "state_path": STATE_RELATIVE.as_posix(),
                "plans": [],
            }
        plans = self.store.list_plans()
        selected = (
            [item for item in plans if item["plan_id"] == plan_id]
            if plan_id
            else plans
        )
        result = []
        for item in selected:
            plan = self.store.load_plan(item["plan_id"])
            result.append(
                {
                    **item,
                    "provider_intents": len(
                        self.store.list_provider_intents(item["plan_id"])
                    ),
                    "receipts": len(
                        self.store.list_receipts(item["plan_id"])
                    ),
                    "plan_lease": copy.deepcopy(plan["state"].get("lease")),
                    "session": self.load_session(item["plan_id"]),
                }
            )
        return {
            "status": "initialized",
            "state_path": STATE_RELATIVE.as_posix(),
            "integrity": self.store.integrity_check(),
            "plans": result,
        }


def _goal_id(timestamp: str, acceptance_sha256: str) -> str:
    moment = parse_utc(timestamp)
    return (
        f"CG-{moment.strftime('%Y%m%dT%H%M%SZ')}-"
        f"{acceptance_sha256[:16]}"
    )


def _reservation_session(
    reservation: PlanTaskReservationResult,
) -> dict[str, Any]:
    dependency = build_plan_task_dependency_proof(
        reservation.selection_proof,
        reservation.task_definition,
    )
    return {
        "summary": reservation.as_dict(),
        "selection_proof": copy.deepcopy(
            dict(reservation.selection_proof)
        ),
        "task_definition": copy.deepcopy(
            dict(reservation.task_definition)
        ),
        "dependency_proof": dependency,
        "envelope": copy.deepcopy(dict(reservation.envelope)),
        "worker_prompt_sha256": hashlib.sha256(
            reservation.worker_prompt.encode("utf-8")
        ).hexdigest(),
    }


def _task_create_request(
    session: Mapping[str, Any],
    *,
    repo_root: Path,
) -> dict[str, Any]:
    reservation = session["reservation"]
    summary = reservation["summary"]
    return {
        "status": "task_creation_required",
        "create_attempt_budget": 1,
        "retry_on_ambiguous": False,
        "reuse_existing_checkout": True,
        "project_root": str(repo_root),
        "reasoning_effort": session["reasoning_effort"],
        "idempotency_key": summary["idempotency_key"],
        "plan_id": summary["plan_id"],
        "task_id": summary["task_id"],
        "generation": summary["generation"],
        "envelope_sha256": summary["envelope_sha256"],
        "initial_message": (
            "Reserve this fresh implementation-plan worker task. Do not "
            "claim or consume the plan task until the coordinator adopts "
            "this task ID and sends the token-bound activation prompt."
        ),
        "token_bound_prompt_released": False,
    }


def _reserve_task(
    *,
    plan_store: PlanControlStore,
    prepared: PreparedPlan,
    expected_plan_revision: int,
    expected_outer_revision: int,
    outer_holder_token: str | None,
    predecessor_thread_id: str,
    first_task: bool,
    timestamp: str,
) -> PlanTaskReservationResult:
    store = plan_store.require_store()
    reserve = reserve_first_plan_task if first_task else reserve_next_plan_task
    reservation_store = store
    record = store.load_plan(str(prepared.plan["plan_id"]))
    selection = store.select_next_task(
        str(prepared.plan["plan_id"]),
        expected_revision=expected_plan_revision,
    )
    selected_task_id = (
        str(selection.selected_task["task_id"])
        if selection.status == "selected"
        and selection.selected_task is not None
        else None
    )
    immutable_task_ids = {
        str(item["task_id"]) for item in record["plan"]["tasks"]
    }
    if selected_task_id is not None and selected_task_id not in immutable_task_ids:
        runtime_definition = store.load_task_definition(
            record["plan_id"], selected_task_id
        )
        entry = prepared.binding["tasks"].get(selected_task_id)
        if (
            runtime_definition.get("origin_kind") != "replacement"
            or not isinstance(entry, Mapping)
            or entry.get("task_sha256")
            != runtime_definition.get("task_sha256")
        ):
            raise _protected(
                "replacement reservation lacks exact runtime and binding identity",
                "plan_task.identity_mismatch",
                task_id=selected_task_id,
            )
        replacement_task = copy.deepcopy(
            dict(runtime_definition["task_json"])
        )
        reservation_store = copy.copy(store)

        def load_plan_with_replacement(plan_id: str) -> dict[str, Any]:
            value = store.load_plan(plan_id)
            value["plan"]["tasks"].append(
                copy.deepcopy(replacement_task)
            )
            return value

        reservation_store.load_plan = load_plan_with_replacement  # type: ignore[method-assign]
    reserved = reserve(
        reservation_store,
        plan_id=str(prepared.plan["plan_id"]),
        expected_plan_revision=expected_plan_revision,
        expected_outer_revision=expected_outer_revision,
        current_outer_holder_token=outer_holder_token,
        predecessor_thread_id=predecessor_thread_id,
        timestamp=timestamp,
    )
    if reservation_store is store:
        return reserved
    return PlanTaskReservationResult(
        plan_record=copy.deepcopy(
            store.load_plan(str(prepared.plan["plan_id"]))
        ),
        outer_goal_record=copy.deepcopy(reserved.outer_goal_record),
        selection_proof=copy.deepcopy(reserved.selection_proof),
        task_definition=copy.deepcopy(reserved.task_definition),
        envelope=copy.deepcopy(reserved.envelope),
        worker_prompt=reserved.worker_prompt,
        envelope_schema_path=reserved.envelope_schema_path,
        expected_worker_revision=reserved.expected_worker_revision,
        selection_proof_sha256=reserved.selection_proof_sha256,
    )


def _activate_reserved_packet(
    *,
    reservation: PlanTaskReservationResult,
    prepared: PreparedPlan,
    expected_control_sha256: str,
    timestamp: str,
) -> dict[str, Any]:
    selected_task_id = str(reservation.envelope["task_id"])
    binding_entry = prepared.binding["tasks"].get(selected_task_id)
    if not isinstance(binding_entry, Mapping):
        raise _protected(
            "selected plan task lacks one exact website binding",
            "plan.binding_incomplete",
            task_id=selected_task_id,
        )
    control_store = WebsiteControlStore(prepared.control.repository.binding["root"])
    staged = control_store.stage_packet(
        {
            "plan": prepared.plan,
            "binding": binding_entry,
            "binding_manifest_sha256": prepared.binding[
                "manifest_sha256"
            ],
            "timestamp": timestamp,
        }
    )
    return control_store.activate_packet(
        staged,
        expected_control_sha256,
    )


def activate_plan(
    *,
    prepared: PreparedPlan,
    acceptance_basis_sha256: str,
    acceptance_message: str,
    acceptance_evidence_ref: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Initialize, reserve, materialize, and open exactly one manual intent."""

    now = timestamp or utc_now()
    parse_utc(now)
    if (
        acceptance_basis_sha256 != prepared.acceptance_basis_sha256
        or expected_control_sha256 != prepared.control.control_sha256
    ):
        raise _protected(
            "combined acceptance or website control evidence is stale",
            "activation.acceptance_invalidated",
        )
    if not acceptance_message.strip() or not acceptance_evidence_ref.strip():
        raise _protected(
            "activation requires exact combined-acceptance evidence",
            "activation.acceptance_missing",
        )
    plan_id = str(prepared.plan["plan_id"])
    controls = PlanControlStore(
        Path(prepared.repository.binding["root"]),
        read_only=False,
    )
    controls.assert_revision(plan_id, expected_plan_revision)
    if expected_plan_revision != 0:
        raise _protected(
            "activate is only valid before plan initialization; use recover",
            "plan.revision_conflict",
            expected=0,
            actual=expected_plan_revision,
        )
    _, goal_activation = accept_goal_activation(
        prepared.goal_proposal,
        acceptance_message=acceptance_message,
        acceptance_evidence_ref=acceptance_evidence_ref,
        timestamp=now,
    )
    _, plan_activation = accept_plan_activation(
        prepared.plan_proposal,
        acceptance_message=acceptance_message,
        acceptance_evidence_ref=acceptance_evidence_ref,
        timestamp=now,
    )
    launcher_token = secrets.token_hex(24)
    goal = initialize_goal(
        controls.require_store().goal_store,
        goal_text=str(prepared.plan["objective"]),
        completion_contract=prepared.completion_contract,
        repository_binding=prepared.repository.binding,
        initial_fingerprint=prepared.control.control_sha256,
        authorization={
            "fresh_recursive_threads_explicitly_requested": True
        },
        activation_receipt=goal_activation,
        runtime_binding={
            "skill_versions": {
                skill: version
                for skill, (version, _) in EXPECTED_SKILLS.items()
            },
            "capability_versions": [
                "sys4ai.implementation-plan-goal.runtime.v1",
                "sys4ai.plan-store.sqlite.v5",
                "sys4ai.plan-task-receipt.v2",
            ],
            "source_lock_ref": LOCK_RELATIVE.as_posix(),
            "provider_id": "manual-handoff",
        },
        repository_topology_policy=DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
        goal_id=_goal_id(now, acceptance_basis_sha256),
        timestamp=now,
        launcher_token=launcher_token,
    )
    initialized = initialize_plan(
        controls.require_store(),
        preflight=prepared.launcher_preflight,
        normalization=prepared.normalization,
        activation_receipt=plan_activation,
        activation_goal_text=str(prepared.plan["objective"]),
        repository_topology_policy=DEFAULT_REPOSITORY_TOPOLOGY_POLICY,
        outer_goal_id=str(goal["goal_id"]),
        expected_outer_revision=int(goal["state"]["revision"]),
        outer_holder_token=launcher_token,
        timestamp=now,
    )
    plan_record = initialized.plan_record
    outer = controls.require_store().goal_store.load_goal(
        plan_record["outer_goal_id"]
    )
    session = controls.write_session(
        plan_id,
        {
            "status": "activation_in_progress",
            "acceptance_basis_sha256": acceptance_basis_sha256,
            "acceptance_message_sha256": hashlib.sha256(
                acceptance_message.encode("utf-8")
            ).hexdigest(),
            "binding_manifest_sha256": prepared.binding[
                "manifest_sha256"
            ],
            "coordinator_thread_id": prepared.acceptance_basis[
                "current_thread_id"
            ],
            "reasoning_effort": prepared.acceptance_basis[
                "reasoning_effort"
            ],
            "repository_binding": copy.deepcopy(
                dict(prepared.repository.binding)
            ),
            "repository_topology": copy.deepcopy(
                dict(prepared.repository.topology)
            ),
            "website_control_sha256_before": expected_control_sha256,
            "goal_id": goal["goal_id"],
            "reservation": None,
            "control_activation": None,
            "worker": None,
            "last_error": None,
        },
        expected_adapter_revision=0,
    )
    try:
        reservation = _reserve_task(
            plan_store=controls,
            prepared=prepared,
            expected_plan_revision=int(plan_record["state"]["revision"]),
            expected_outer_revision=int(outer["state"]["revision"]),
            outer_holder_token=launcher_token,
            predecessor_thread_id=str(
                prepared.acceptance_basis["current_thread_id"]
            ),
            first_task=True,
            timestamp=now,
        )
        session = controls.write_session(
            plan_id,
            {
                **session,
                "status": "task_reserved",
                "reservation": _reservation_session(reservation),
                "last_error": None,
            },
            expected_adapter_revision=session["adapter_revision"],
        )
        control_activation = _activate_reserved_packet(
            reservation=reservation,
            prepared=prepared,
            expected_control_sha256=expected_control_sha256,
            timestamp=now,
        )
        session = controls.write_session(
            plan_id,
            {
                **session,
                "status": "website_packet_activated",
                "control_activation": control_activation,
                "website_control_sha256": control_activation[
                    "website_control_sha256_after"
                ],
                "last_error": None,
            },
            expected_adapter_revision=session["adapter_revision"],
        )
        provider = ManualThreadProvider(
            prepared.repository.binding["root"],
            local_root=MANUAL_RELATIVE,
            current_thread_id=str(
                prepared.acceptance_basis["current_thread_id"]
            ),
            timestamp=now,
        )
        dispatch = dispatch_reserved_plan_task(
            controls.require_store(),
            reservation=reservation,
            provider=provider,
            timestamp=now,
        )
        if dispatch.status != "manual_handoff_pending":
            raise _protected(
                "manual dispatch did not preserve an open adoption intent",
                "provider.dispatch_unexpected",
                status=dispatch.status,
            )
        session = controls.write_session(
            plan_id,
            {
                **session,
                "status": "awaiting_task_creation",
                "provider_intent_id": dispatch.intent_id,
                "provider_intent_sha256": dispatch.intent_sha256,
                "last_error": None,
            },
            expected_adapter_revision=session["adapter_revision"],
        )
    except Exception as error:
        controls.write_session(
            plan_id,
            {
                **session,
                "status": "recovery_required",
                "last_error": {
                    "type": type(error).__name__,
                    "message": str(error),
                },
            },
            expected_adapter_revision=session["adapter_revision"],
        )
        raise
    current = controls.require_store().load_plan(plan_id)
    return {
        "status": "awaiting_task_creation",
        "plan_id": plan_id,
        "plan_revision": current["state"]["revision"],
        "outer_goal_revision": dispatch.outer_goal_revision,
        "website_control_sha256": session["website_control_sha256"],
        "task_create_request": _task_create_request(
            session,
            repo_root=prepared.repository.binding["root"],
        ),
        "provider_intent_id": dispatch.intent_id,
        "provider_intent_status": "intent",
        "agentjobs": 0,
        "continue_invocations": 0,
    }


def _require_mutation_cas(
    *,
    controls: PlanControlStore,
    control_store: WebsiteControlStore,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
) -> tuple[dict[str, Any], WebsiteControlSnapshot]:
    controls.assert_revision(plan_id, expected_plan_revision)
    snapshot = control_store.snapshot()
    if snapshot.control_sha256 != expected_control_sha256:
        raise _protected(
            "website control compare-and-swap conflict",
            "website.control_hash_conflict",
            expected=expected_control_sha256,
            actual=snapshot.control_sha256,
        )
    session = controls.load_session(plan_id)
    if session is None:
        raise _protected(
            "plan adapter session is missing",
            "adapter.session_missing",
        )
    accepted_binding = session.get("repository_binding")
    accepted_topology = session.get("repository_topology")
    if (
        accepted_binding != snapshot.repository.binding
        or any(
            accepted_topology.get(key) != snapshot.repository.topology.get(key)
            for key in (
                "root",
                "worktree",
                "branch",
                "git_common_dir",
                "local_branches",
                "registered_worktrees",
            )
        )
    ):
        raise _protected(
            "repository binding or topology drifted after acceptance",
            "plan.repository_topology_changed",
        )
    return session, snapshot


def adopt_worker(
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    creation_status: str,
    codex_task_id: str | None,
    effective_reasoning_effort: str | None,
    profile_evidence_ref: str | None,
    repo_root: Path = REPO_ROOT,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Adopt the one returned task before releasing its token-bound prompt."""

    now = timestamp or utc_now()
    controls = PlanControlStore(repo_root)
    session, snapshot = _require_mutation_cas(
        controls=controls,
        control_store=WebsiteControlStore(repo_root),
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_control_sha256=expected_control_sha256,
    )
    if creation_status != "returned":
        updated = controls.write_session(
            plan_id,
            {
                **session,
                "status": "recovery_required",
                "ambiguous_task_creation": True,
                "last_error": {
                    "reason_code": "provider.create_ambiguous",
                    "retry_authorized": False,
                },
            },
            expected_adapter_revision=session["adapter_revision"],
        )
        raise _protected(
            "ambiguous task creation is not retried; adopt the original task through recovery",
            "provider.create_ambiguous",
            retry_authorized=False,
            adapter_revision=updated["adapter_revision"],
        )
    if not all(
        isinstance(value, str) and value.strip()
        for value in (
            codex_task_id,
            effective_reasoning_effort,
            profile_evidence_ref,
        )
    ):
        raise _protected(
            "returned task adoption requires task and profile evidence",
            "provider.adoption_evidence_missing",
        )
    reservation = session.get("reservation")
    if not isinstance(reservation, Mapping):
        raise _protected(
            "manual reservation evidence is missing",
            "provider.adoption_evidence_missing",
        )
    envelope = reservation["envelope"]
    plan = controls.require_store().load_plan(plan_id)
    requested_effort = str(
        plan["execution_profile"]["reasoning_effort"]
    )
    profile_provider = WebsiteThreadExecutionProfileProvider(
        thread_id=str(codex_task_id),
        reasoning_effort=str(effective_reasoning_effort),
        evidence_ref=str(profile_evidence_ref),
    )
    profile = profile_provider.read_thread_profile(str(codex_task_id))
    if profile["effective_reasoning_effort"] != requested_effort:
        raise _protected(
            "returned task reasoning effort differs from acceptance",
            "thread.profile_mismatch",
            expected=requested_effort,
            actual=profile["effective_reasoning_effort"],
        )
    adopted = adopt_manual_plan_successor(
        controls.require_store(),
        project_root=repo_root,
        local_root=MANUAL_RELATIVE,
        plan_id=plan_id,
        expected_revision=expected_plan_revision,
        generation=int(envelope["generation"]),
        handoff_token=str(envelope["handoff_token"]),
        envelope_sha256=content_sha256(envelope),
        successor_thread_id=str(codex_task_id),
        effective_reasoning_effort=str(effective_reasoning_effort),
        profile_evidence_ref=str(profile_evidence_ref),
        observed_repository_binding=snapshot.repository.binding,
        observed_repository_topology=snapshot.repository.topology,
        timestamp=now,
    )
    adoption = {
        "schema_version": "website.codex-task-adoption-receipt.v1",
        "receipt_id": (
            "WCTA-"
            + content_sha256(
                {
                    "plan_id": plan_id,
                    "generation": envelope["generation"],
                    "codex_task_id": codex_task_id,
                }
            )[:24]
        ),
        "plan_id": plan_id,
        "task_id": envelope["task_id"],
        "generation": envelope["generation"],
        "codex_task_id": codex_task_id,
        "envelope_sha256": content_sha256(envelope),
        "requested_reasoning_effort": requested_effort,
        "effective_reasoning_effort": effective_reasoning_effort,
        "profile_evidence_ref": profile_evidence_ref,
        "repository_binding_sha256": snapshot.repository.binding_sha256,
        "repository_topology_sha256": snapshot.repository.topology_sha256,
        "prompt_release_authorized": True,
        "adopted_at": now,
        "receipt_content_sha256": "",
        "finalized": True,
    }
    adoption["receipt_content_sha256"] = content_sha256(
        {
            key: value
            for key, value in adoption.items()
            if key != "receipt_content_sha256"
        }
    )
    findings = validate_instance(
        adoption,
        repo_root / ADOPTION_SCHEMA_RELATIVE,
    )
    if findings:
        raise _protected(
            "Codex task adoption receipt failed validation",
            "provider.adoption_receipt_invalid",
            findings=format_issues(findings).splitlines(),
        )
    adoption_path = (
        repo_root
        / ADOPTION_RELATIVE
        / plan_id
        / f"generation-{envelope['generation']}.json"
    )
    write_canonical_json(adoption_path, adoption, append_only=True)
    prompt_path = (
        repo_root
        / MANUAL_RELATIVE
        / plan_id
        / f"generation-{envelope['generation']}"
        / "new-thread-prompt.txt"
    )
    _require_regular(prompt_path, label="token-bound worker prompt")
    prompt = prompt_path.read_text(encoding="utf-8")
    updated_session = controls.write_session(
        plan_id,
        {
            **session,
            "status": "worker_adopted",
            "ambiguous_task_creation": False,
            "worker": {
                "codex_task_id": codex_task_id,
                "effective_reasoning_effort": effective_reasoning_effort,
                "profile_evidence_ref": profile_evidence_ref,
                "adoption_receipt": adoption,
                "prompt_released": True,
            },
            "last_error": None,
        },
        expected_adapter_revision=session["adapter_revision"],
    )
    return {
        "status": "worker_adopted",
        "plan_id": plan_id,
        "plan_revision": adopted["state"]["revision"],
        "website_control_sha256": snapshot.control_sha256,
        "adoption_receipt_sha256": content_sha256(adoption),
        "adoption_receipt_path": adoption_path.relative_to(
            repo_root
        ).as_posix(),
        "token_bound_prompt_released": True,
        "worker_prompt": prompt,
        "adapter_revision": updated_session["adapter_revision"],
    }


def _worker_entry(
    controls: PlanControlStore,
    session: Mapping[str, Any],
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    reservation = session.get("reservation")
    if not isinstance(reservation, Mapping):
        raise _protected(
            "worker reservation evidence is missing",
            "plan_task.identity_mismatch",
        )
    return (
        copy.deepcopy(dict(reservation["envelope"])),
        copy.deepcopy(dict(reservation["selection_proof"])),
        copy.deepcopy(dict(reservation["task_definition"])),
        copy.deepcopy(dict(reservation["dependency_proof"])),
    )


def worker_prepare(
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    current_thread_id: str,
    repo_root: Path = REPO_ROOT,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Validate all worker evidence and atomically claim one generation."""

    now = timestamp or utc_now()
    controls = PlanControlStore(repo_root)
    session, snapshot = _require_mutation_cas(
        controls=controls,
        control_store=WebsiteControlStore(repo_root),
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_control_sha256=expected_control_sha256,
    )
    worker = session.get("worker")
    if (
        not isinstance(worker, Mapping)
        or worker.get("codex_task_id") != current_thread_id
        or worker.get("adoption_receipt", {}).get(
            "prompt_release_authorized"
        )
        is not True
    ):
        raise _protected(
            "worker identity was not adopted before claim",
            "plan_task.identity_mismatch",
        )
    envelope, selection, definition, dependency = _worker_entry(
        controls, session
    )
    worker_token = secrets.token_hex(24)
    plan = controls.require_store().load_plan(plan_id)
    outer = controls.require_store().goal_store.load_goal(
        plan["outer_goal_id"]
    )
    claim = claim_plan_task_generation(
        controls.require_store(),
        envelope=envelope,
        envelope_sha256=content_sha256(envelope),
        selection_proof_sha256=content_sha256(selection),
        selected_task_definition=definition,
        task_definition_sha256=content_sha256(definition),
        dependency_proof=dependency,
        dependency_proof_sha256=content_sha256(dependency),
        expected_revision=expected_plan_revision,
        expected_outer_revision=int(outer["state"]["revision"]),
        current_thread_id=current_thread_id,
        worker_token=worker_token,
        observed_execution_profile={
            "effective_reasoning_effort": worker[
                "effective_reasoning_effort"
            ],
            "evidence_ref": worker["profile_evidence_ref"],
        },
        observed_repository_binding=snapshot.repository.binding,
        observed_repository_topology=snapshot.repository.topology,
        timestamp=now,
    )
    updated_session = controls.write_session(
        plan_id,
        {
            **session,
            "status": "worker_claimed",
            "worker": {
                **worker,
                "worker_token": worker_token,
                "preclaim": asdict(claim.preclaim),
                "claim_receipt_sha256": claim.claim_receipt_sha256,
                "claim_receipt": copy.deepcopy(
                    dict(claim.claim_receipt)
                ),
                "outer_goal_revision_before_claim": int(
                    outer["state"]["revision"]
                ),
            },
        },
        expected_adapter_revision=session["adapter_revision"],
    )
    return {
        **claim.as_dict(),
        "website_control_sha256": snapshot.control_sha256,
        "adapter_revision": updated_session["adapter_revision"],
        "continue_invocations": 0,
        "agentjobs": 0,
        "next_boundary": "worker-consume",
    }


def compile_binding_director_route(
    task_definition: Mapping[str, Any],
    binding: Mapping[str, Any],
) -> DirectorRoute:
    """Compile one DirectorRoute exclusively from the hash-bound mapping."""

    task = copy.deepcopy(dict(task_definition))
    entry = copy.deepcopy(dict(binding))
    packet_ids = entry["packet_ids"]
    task_authority_ref = (
        "implementation_control/tasks/"
        f"{packet_ids['task_id']}/00_TASK.yaml"
    )
    validators = [
        {
            "validator_id": str(item["id"]),
            "validator_class": "command_validation",
            "mode": "required",
        }
        for item in entry["validators"]
    ]
    commands = [
        {
            "command_id": str(item["id"]),
            "argv": shlex.split(str(item["command"])),
            "cwd": "./",
            "environment": {},
            "network": False,
            "shell": False,
            "shell_policy_approval_ref": None,
            "timeout_seconds": 1800,
        }
        for item in entry["validators"]
    ]
    controlled_outputs = [
        {"path": path, "kind": "controlled_source_change"}
        for path in entry["allowed_writes"]
    ]
    generated_paths: list[str] = []
    if not controlled_outputs:
        completion_path = (
            "implementation_control/tasks/"
            f"{packet_ids['task_id']}/jobs/completions/"
            f"{packet_ids['completion_id']}.yaml"
        )
        generated_paths.append(completion_path)
        controlled_outputs.append(
            {"path": completion_path, "kind": "receipt"}
        )
    rights = entry["checkpoint_rights"]
    forbidden_actions = [
        "publish",
        "push",
        "merge",
        "access_secrets",
        "repository-branch-create",
        "repository-worktree-create",
        "repository-binding-change",
    ]
    return DirectorRoute(
        route_id=f"website-binding:{task['task_id']}",
        role_id=str(entry["execution_role"]["role_id"]),
        role_version=str(entry["execution_role"]["role_version"]),
        priority=1,
        rationale=(
            "Execute only the exact hash-bound website implementation packet."
        ),
        job_spec={
            "actor_ref": "website:implementation-plan-goal-adapter",
            "policy_refs": [ADAPTER_CONFIG_RELATIVE.as_posix()],
            "source_refs": [task_authority_ref],
            "objective": task["objective"],
            "authority": {
                "allowed_read_paths": list(entry["allowed_reads"]),
                "allowed_write_paths": list(entry["allowed_writes"]),
                "allowed_generated_paths": generated_paths,
                "forbidden_paths": [".git/**", ".local/**"],
                "allowed_actions": [
                    "read_files",
                    "edit_files",
                    "run_local_commands",
                ],
                "forbidden_actions": forbidden_actions,
                "network_access": False,
                "external_effects": [],
            },
            "source_policy": {
                "allowed_source_classes": [
                    "controlled_source",
                    "repository_evidence",
                ],
                "forbidden_source_classes": [
                    "unverified_external_claim"
                ],
            },
            "commands": {"approved": commands},
            "validators": {
                "required": validators,
                "contextual": [],
            },
            "expected_outputs": controlled_outputs,
            "completion_contract": {
                "required_evidence": list(
                    task["acceptance_criteria"]
                ),
                "goal_effect": {
                    "type": "bounded_completion",
                    "does_not_imply_global_goal_completion": True,
                },
            },
            "stop_conditions": list(entry["stop_conditions"]),
            "checkpoint": {
                "provider": (
                    "website-checkpoint"
                    if rights["commit"]
                    else "none"
                ),
                "required": bool(rights["commit"]),
                "auto_commit": False,
            },
            "claim_boundary": {
                "allowed": list(task["acceptance_criteria"]),
                "forbidden": [
                    "Any other plan task is complete.",
                    "The global plan goal is complete.",
                ],
            },
            "extensions": {
                "website_implementation_control": {
                    "version": "1.0.0",
                    "required": True,
                    "data": {
                        "packet_ids": copy.deepcopy(
                            entry["packet_ids"]
                        ),
                        "authority_sha256": entry["authority_sha256"],
                    },
                }
            },
        },
        role_spec={
            "binding_type": "registered_role",
            "responsibilities": list(
                entry["execution_role"]["responsibilities"]
            ),
            "may_not": list(entry["execution_role"]["may_not"]),
            "source_role_ref": None,
            "task_overlay": None,
            "authority_delta": "No permission expansion.",
            "provisional_role": None,
            "extensions": {},
        },
    )


def compile_binding_plan_task_invocation(
    *,
    preclaim: PlanWorkerPreclaim,
    plan_record: Mapping[str, Any],
    envelope: Mapping[str, Any],
    selected_task_definition: Mapping[str, Any],
    resolved_task_id: str,
    director_route: DirectorRoute,
    timestamp: str,
) -> PlanTaskContinueInvocation:
    """Compile command validators without treating commands as path evidence."""

    task = copy.deepcopy(dict(selected_task_definition))
    original_validation_refs = list(task.get("validation_refs", []))
    required_validators = list(
        director_route.job_spec.get("validators", {}).get("required", [])
    )
    source_refs = list(director_route.job_spec.get("source_refs", []))
    if (
        len(source_refs) != 1
        or len(original_validation_refs) != len(required_validators)
    ):
        raise RecordValidationError(
            "website task compiler requires one task authority source and "
            "one validation reference per validator",
            details={"reason_code": "plan_task.authority_packet_invalid"},
        )

    # The generic compiler historically reused validation_refs as the
    # DirectorDecision pathList.  Give that validation stage bounded relative
    # placeholders, then restore the canonical validation metadata and replace
    # the decision evidence with the actual website task authority record.
    task["validation_refs"] = [
        f"{source_refs[0]}.validator-{index}"
        for index in range(len(required_validators))
    ]
    compiled = compile_runtime_plan_task_invocation(
        preclaim=preclaim,
        plan_record=plan_record,
        envelope=envelope,
        selected_task_definition=task,
        resolved_task_id=resolved_task_id,
        director_route=director_route,
        timestamp=timestamp,
    )
    invocation = compiled.as_dict()
    invocation["authority_packet"]["decision"]["evidence"][
        "source_refs"
    ] = source_refs
    invocation["task_binding"]["validation_refs"] = (
        original_validation_refs
    )
    for validation_ref, mapping in zip(
        original_validation_refs,
        invocation["execution_mapping"]["validators"],
        strict=True,
    ):
        mapping["validation_ref"] = validation_ref
    _validate_authority_record(
        invocation["authority_packet"]["decision"],
        schema_name="director-decision.schema.json",
    )
    invocation["invocation_content_sha256"] = content_sha256(
        {
            key: value
            for key, value in invocation.items()
            if key != "invocation_content_sha256"
        }
    )
    return PlanTaskContinueInvocation(
        preclaim.plan_id,
        preclaim.task_id,
        preclaim.generation,
        content_sha256(invocation),
        invocation,
    )


def worker_consume(
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    current_thread_id: str,
    plan_path: str | Path,
    binding_path: str | Path | None,
    repo_root: Path = REPO_ROOT,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Consume once immediately before resolving the local continue boundary."""

    now = timestamp or utc_now()
    controls = PlanControlStore(repo_root)
    session, snapshot = _require_mutation_cas(
        controls=controls,
        control_store=WebsiteControlStore(repo_root),
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_control_sha256=expected_control_sha256,
    )
    worker = session.get("worker")
    if (
        session.get("status") != "worker_claimed"
        or not isinstance(worker, Mapping)
        or worker.get("codex_task_id") != current_thread_id
        or not isinstance(worker.get("preclaim"), Mapping)
    ):
        raise _protected(
            "worker is not at the single-consumption boundary",
            "plan_task.identity_mismatch",
        )
    plan_source = load_project_plan(plan_path, repo_root=repo_root)
    if plan_source["plan_id"] != plan_id:
        raise _protected(
            "worker plan source identity differs from adopted plan",
            "plan_task.identity_mismatch",
        )
    binding = load_plan_binding(
        plan_source,
        binding_path,
        repo_root=repo_root,
    )
    if binding["manifest_sha256"] != session["binding_manifest_sha256"]:
        raise _protected(
            "binding changed after combined acceptance",
            "activation.acceptance_invalidated",
        )
    envelope, _, definition, _ = _worker_entry(controls, session)
    record = controls.require_store().load_plan(plan_id)
    resolved_binding = resolve_effective_task_binding(
        store=controls.require_store(),
        plan_record=record,
        session=session,
        base_binding=binding,
        task_id=str(envelope["task_id"]),
        repo_root=repo_root,
    )
    active_binding_sha256 = session.get(
        "active_binding_manifest_sha256",
        session["binding_manifest_sha256"],
    )
    if (
        active_binding_sha256
        != resolved_binding["binding_manifest_sha256"]
    ):
        raise _protected(
            "active task binding differs from the reserved authority",
            "activation.acceptance_invalidated",
        )
    entry = resolved_binding["entry"]
    execution_definition = resolved_binding["task_definition"]
    preclaim = PlanWorkerPreclaim(**dict(worker["preclaim"]))
    compiled = compile_binding_plan_task_invocation(
        preclaim=preclaim,
        plan_record=record,
        envelope=envelope,
        selected_task_definition=execution_definition,
        resolved_task_id=str(envelope["task_id"]),
        director_route=compile_binding_director_route(
            execution_definition, entry
        ),
        timestamp=now,
    )
    with controls.require_store().mutation(
        plan_id,
        expected_revision=expected_plan_revision,
        timestamp=now,
    ) as mutation:
        mutation.consume_task_invocation(
            task_id=str(envelope["task_id"]),
            generation=int(envelope["generation"]),
        )
    resolver, exit_code = resolve_continue_context(repo_root)
    packet_ids = entry["packet_ids"]
    if (
        exit_code != 0
        or resolver.get("status") != "ready"
        or resolver.get("active_task", {}).get("task_id")
        != packet_ids["task_id"]
        or resolver.get("current_job", {}).get("job_id")
        != packet_ids["job_id"]
    ):
        controls.write_session(
            plan_id,
            {
                **session,
                "status": "invocation_unknown",
                "worker": {
                    **worker,
                    "compiled_invocation": compiled.as_dict(),
                    "consumed": True,
                },
                "last_error": {
                    "reason_code": "website.continue_boundary_mismatch"
                },
            },
            expected_adapter_revision=session["adapter_revision"],
        )
        raise _protected(
            "consumed website continue boundary is uncertain",
            "plan_worker.continue_outcome_unknown",
            retry_authorized=False,
        )
    updated = controls.write_session(
        plan_id,
        {
            **session,
            "status": "invocation_consumed",
            "worker": {
                **worker,
                "compiled_invocation": compiled.as_dict(),
                "compiled_invocation_sha256": compiled.invocation_sha256,
                "consumed": True,
                "continue_resolver": copy.deepcopy(dict(resolver)),
            },
            "last_error": None,
        },
        expected_adapter_revision=session["adapter_revision"],
    )
    current = controls.require_store().load_plan(plan_id)
    return {
        "status": "invocation_consumed",
        "plan_id": plan_id,
        "task_id": envelope["task_id"],
        "generation": envelope["generation"],
        "plan_revision": current["state"]["revision"],
        "website_control_sha256": snapshot.control_sha256,
        "continue_command": "npm run continue:implementation",
        "continue_context": resolver,
        "compiled_invocation": compiled.as_dict(),
        "continue_invocations": 1,
        "agentjobs": 0,
        "adapter_revision": updated["adapter_revision"],
        "next_boundary": "execute at most one mapped website job, then worker-finalize",
    }


def _path_allowed(path: str, rules: Sequence[str]) -> bool:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        return False
    for rule in rules:
        base = rule[:-3] if rule.endswith("/**") else rule
        if path == base or path.startswith(base.rstrip("/") + "/"):
            return True
    return False


def _load_completion(
    repo_root: Path,
    entry: Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    ids = entry["packet_ids"]
    relative = (
        f"implementation_control/tasks/{ids['task_id']}/jobs/"
        f"completions/{ids['completion_id']}.yaml"
    )
    path = repo_root / relative
    _require_regular(path, label="website implementation completion")
    value = load_yaml(path)
    if (
        value.get("record_type") != "implementation_completion"
        or value.get("completion_id") != ids["completion_id"]
        or value.get("task_id") != ids["task_id"]
        or value.get("job_id") != ids["job_id"]
        or value.get("status") not in {"complete", "completed"}
    ):
        raise _protected(
            "website completion does not prove the mapped packet",
            "plan.validation_failed",
        )
    return value, relative


def _direct_website_result(
    *,
    plan_record: Mapping[str, Any],
    task_definition: Mapping[str, Any],
    entry: Mapping[str, Any],
    compiled: Mapping[str, Any],
    snapshot: WebsiteControlSnapshot,
    completion: Mapping[str, Any],
    completion_path: str,
    timestamp: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    ids = entry["packet_ids"]
    root = Path(snapshot.repository.binding["root"])
    authority_paths = {
        "task": (
            root
            / "implementation_control"
            / "tasks"
            / ids["task_id"]
            / "00_TASK.yaml"
        ),
        "job": (
            root
            / "implementation_control"
            / "tasks"
            / ids["task_id"]
            / "jobs"
            / f"{ids['job_id']}.yaml"
        ),
        "handoff": (
            root
            / "implementation_control"
            / "handoffs"
            / f"{ids['handoff_id']}.yaml"
        ),
    }
    authority_records: dict[str, dict[str, Any]] = {}
    for kind, path in authority_paths.items():
        _require_regular(path, label=f"website {kind} completion evidence")
        authority_records[kind] = load_yaml(path)
    program = snapshot.payload["program_state"]["record"]
    if (
        snapshot.resolver_exit_code != 0
        or snapshot.resolver.get("status") != "no_action"
        or program.get("status") not in NO_ACTION_STATUSES
        or authority_records["task"].get("task_id") != ids["task_id"]
        or authority_records["task"].get("status")
        not in {"complete", "completed"}
        or authority_records["job"].get("job_id") != ids["job_id"]
        or authority_records["job"].get("status")
        not in {"complete", "completed"}
        or authority_records["handoff"].get("handoff_id")
        != ids["handoff_id"]
        or authority_records["handoff"].get("status")
        not in {"complete", "completed"}
    ):
        raise _protected(
            "website control does not directly prove packet completion",
            "plan.validation_failed",
        )
    source_context = authority_records["task"].get("source_context", {})
    if (
        source_context.get("plan_task_id") != task_definition["task_id"]
        or source_context.get("plan_task_sha256")
        != task_definition["task_sha256"]
        or source_context.get("authority_sha256")
        != entry["authority_sha256"]
    ):
        raise _protected(
            "website completion authority differs from the selected binding",
            "plan_task.identity_mismatch",
        )
    changed = [
        str(path) for path in completion.get("changed_files", [])
    ]
    if any(
        not _path_allowed(path, entry["allowed_writes"])
        for path in changed
    ):
        raise _protected(
            "website completion names a changed path outside binding authority",
            "plan_task.scope_violation",
        )
    validator_by_id = {
        str(item.get("id")): item
        for item in completion.get("validator_results", [])
        if isinstance(item, Mapping) and item.get("id")
    }
    missing = [
        item["id"]
        for item in entry["validators"]
        if (
            item["required"]
            and (
                item["id"] not in validator_by_id
                or str(
                    validator_by_id[item["id"]].get("status", "")
                ).lower()
                not in {"pass", "passed", "complete", "completed"}
                or validator_by_id[item["id"]].get("command")
                != item["command"]
            )
        )
    ]
    if missing:
        raise _protected(
            "website completion lacks passing required validator evidence",
            "plan.validation_failed",
            validators=missing,
        )
    acceptance_results = completion.get("acceptance_results")
    requirements_satisfied = completion.get("requirements_satisfied")
    if isinstance(acceptance_results, list):
        acceptance_by_criterion = {
            str(item.get("criterion")): item
            for item in acceptance_results
            if isinstance(item, Mapping) and item.get("criterion")
        }
        acceptance_ok = all(
            criterion in acceptance_by_criterion
            and str(
                acceptance_by_criterion[criterion].get("status", "")
            ).lower()
            in {"pass", "passed", "complete", "completed"}
            for criterion in task_definition["acceptance_criteria"]
        )
    else:
        acceptance_ok = (
            isinstance(requirements_satisfied, list)
            and set(task_definition["acceptance_criteria"])
            <= {str(item) for item in requirements_satisfied}
        )
    if not acceptance_ok:
        raise _protected(
            "website completion lacks direct acceptance-criterion evidence",
            "plan.validation_failed",
        )
    project_completion = WebsiteProjectAdapter(root).evaluate_completion(
        completion
    )
    if project_completion.blocking:
        raise _protected(
            "website completion failed project-adapter validation",
            "plan.validation_failed",
            findings=list(project_completion.findings),
        )
    checkpoint_required = bool(entry["checkpoint_rights"]["commit"])
    direct = {
        "changed_paths": changed,
        "acceptance_results": [
            {
                "criterion": criterion,
                "status": "pass",
                "evidence_refs": [completion_path],
            }
            for criterion in task_definition["acceptance_criteria"]
        ],
        "validator_results": [
            {
                "validator_id": item["id"],
                "validator_class": "command_validation",
                "status": "pass",
                "reason_code": None,
                "evidence_ref": completion_path,
                "notes": [item["command"]],
            }
            for item in entry["validators"]
        ],
        "checkpoint": {
            "provider": (
                "website-checkpoint" if checkpoint_required else "none"
            ),
            "status": "pass" if checkpoint_required else "not_required",
            "revision": (
                snapshot.repository.binding["starting_revision"]
                if checkpoint_required
                else None
            ),
            "evidence_ref": (
                completion_path if checkpoint_required else None
            ),
        },
        "approvals": [
            {
                "approval_id": None,
                "action": item["id"],
                "status": (
                    "approved"
                    if item["status"] == "approved"
                    else "not_required"
                ),
                "evidence_ref": None,
            }
            for item in entry["approval_gates"]
        ],
        "protected_effects": [],
        "warnings": [],
        "indeterminate_checks": [],
        "plan_completion": None,
    }
    packet = compiled["authority_packet"]
    result = {
        "starting_revision": plan_record["repository_binding"][
            "starting_revision"
        ],
        "ending_revision": snapshot.repository.binding[
            "starting_revision"
        ],
        "fingerprint_after": snapshot.control_sha256,
        "agentjobs": 1,
        "agent_job_id": packet["agent_job"]["job_id"],
        "completion_id": f"AJC-{packet['agent_job']['job_id']}",
        "task_id": task_definition["task_id"],
        "decision_id": packet["decision"]["decision_id"],
        "handoff_id": None,
        "global_goal_evaluation": "not_evaluated_here",
        "zero_job_reason": None,
        "direct_evidence": direct,
        "disposition": "task_complete",
        "reason_code": "website.task_complete",
        "terminal_reason": None,
        "recovery": {"status": "not_required", "action_ref": None},
        "replanning": {"status": "not_required", "action_ref": None},
        "coordinator_action": {
            "kind": "dispatch_next_task",
            "next_task_id": None,
        },
        "pre_topology": copy.deepcopy(
            dict(snapshot.repository.topology)
        ),
        "post_topology": copy.deepcopy(
            dict(snapshot.repository.topology)
        ),
        "finished_at": timestamp,
    }
    observation = {
        "ending_revision": result["ending_revision"],
        "fingerprint_after": result["fingerprint_after"],
        "post_topology": result["post_topology"],
        "changed_paths": changed,
    }
    return result, observation


def worker_finalize(
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    current_thread_id: str,
    plan_path: str | Path,
    binding_path: str | Path | None,
    repo_root: Path = REPO_ROOT,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Finalize PlanTaskReceipt v2 only from direct website completion evidence."""

    now = timestamp or utc_now()
    controls = PlanControlStore(repo_root)
    session, snapshot = _require_mutation_cas(
        controls=controls,
        control_store=WebsiteControlStore(repo_root),
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_control_sha256=expected_control_sha256,
    )
    worker = session.get("worker")
    if (
        session.get("status") != "invocation_consumed"
        or not isinstance(worker, Mapping)
        or worker.get("codex_task_id") != current_thread_id
        or worker.get("consumed") is not True
    ):
        raise _protected(
            "worker is not eligible for direct finalization",
            "plan_task.identity_mismatch",
        )
    plan_source = load_project_plan(plan_path, repo_root=repo_root)
    binding = load_plan_binding(
        plan_source,
        binding_path,
        repo_root=repo_root,
    )
    if binding["manifest_sha256"] != session["binding_manifest_sha256"]:
        raise _protected(
            "binding changed after acceptance",
            "activation.acceptance_invalidated",
        )
    envelope, _, definition, _ = _worker_entry(controls, session)
    record = controls.require_store().load_plan(plan_id)
    resolved_binding = resolve_effective_task_binding(
        store=controls.require_store(),
        plan_record=record,
        session=session,
        base_binding=binding,
        task_id=str(envelope["task_id"]),
        repo_root=repo_root,
    )
    active_binding_sha256 = session.get(
        "active_binding_manifest_sha256",
        session["binding_manifest_sha256"],
    )
    if (
        active_binding_sha256
        != resolved_binding["binding_manifest_sha256"]
    ):
        raise _protected(
            "active task binding differs from the finalized authority",
            "activation.acceptance_invalidated",
        )
    entry = resolved_binding["entry"]
    execution_definition = resolved_binding["task_definition"]
    completion, completion_path = _load_completion(repo_root, entry)
    result, _ = _direct_website_result(
        plan_record=record,
        task_definition=execution_definition,
        entry=entry,
        compiled=worker["compiled_invocation"],
        snapshot=snapshot,
        completion=completion,
        completion_path=completion_path,
        timestamp=now,
    )
    with controls.require_store().mutation(
        plan_id,
        expected_revision=expected_plan_revision,
        timestamp=now,
    ) as mutation:
        mutation.begin_task_verification(
            task_id=str(envelope["task_id"]),
            generation=int(envelope["generation"]),
            fingerprint_after=snapshot.control_sha256,
            continue_invocations=1,
            agentjobs=1,
            provider_creates=1,
        )
    verifying = controls.require_store().load_plan(plan_id)
    intent = controls.require_store().find_provider_intent(
        plan_id, int(envelope["generation"])
    )
    preclaim = PlanWorkerPreclaim(**dict(worker["preclaim"]))
    receipt = _build_receipt(
        record=verifying,
        task_definition=controls.require_store().load_task_definition(
            plan_id, str(envelope["task_id"])
        ),
        envelope=envelope,
        intent=intent,
        preclaim=preclaim,
        prior_journal_sha256=verifying["journal"][-1]["event_hash"],
        fingerprint_before=str(
            worker["claim_receipt"]["fingerprint_before"]
        ),
        result=result,
        started_at=str(worker["claim_receipt"]["claimed_at"]),
        finished_at=now,
    )
    outer = controls.require_store().goal_store.load_goal(
        verifying["outer_goal_id"]
    )
    with controls.require_store().mutation(
        plan_id,
        expected_revision=int(verifying["state"]["revision"]),
        timestamp=now,
    ) as mutation:
        _, quarantined = mutation.finalize_task(
            receipt, guard_reason=None
        )
        if quarantined:
            raise IntegrityError(
                "successful website completion unexpectedly quarantined"
            )
        mutation.release_plan_lease(
            expected_outer_revision=int(outer["state"]["revision"]),
            holder_token=str(worker["worker_token"]),
        )
    final = controls.require_store().load_plan(plan_id)
    updated = controls.write_session(
        plan_id,
        {
            **session,
            "status": "task_finalized",
            "worker": {
                **worker,
                "receipt_id": receipt["receipt_id"],
                "receipt_sha256": content_sha256(receipt),
                "finalized": True,
            },
            "last_error": None,
        },
        expected_adapter_revision=session["adapter_revision"],
    )
    return {
        "status": "task_finalized",
        "plan_id": plan_id,
        "task_id": envelope["task_id"],
        "generation": envelope["generation"],
        "plan_revision": final["state"]["revision"],
        "plan_phase": final["state"]["phase"],
        "receipt_id": receipt["receipt_id"],
        "receipt_sha256": content_sha256(receipt),
        "schema_version": receipt["schema_version"],
        "website_control_sha256": snapshot.control_sha256,
        "continue_invocations": 1,
        "agentjobs": 1,
        "adapter_revision": updated["adapter_revision"],
        "next_boundary": "coordinator reserve-next",
    }


def worker_fail(
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    current_thread_id: str,
    plan_path: str | Path,
    binding_path: str | Path | None,
    validator_results: Mapping[str, str],
    failure_summary: str,
    repo_root: Path = REPO_ROOT,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Finalize one known validator failure without retry or false success."""

    now = timestamp or utc_now()
    summary = failure_summary.strip()
    if not summary or len(summary) > 1000 or "\n" in summary:
        raise _protected(
            "validator failure summary must be one bounded line",
            "plan.validation_failed",
        )
    controls = PlanControlStore(repo_root)
    session, snapshot = _require_mutation_cas(
        controls=controls,
        control_store=WebsiteControlStore(repo_root),
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_control_sha256=expected_control_sha256,
    )
    worker = session.get("worker")
    if (
        session.get("status") != "invocation_consumed"
        or not isinstance(worker, Mapping)
        or worker.get("codex_task_id") != current_thread_id
        or worker.get("consumed") is not True
    ):
        raise _protected(
            "worker is not eligible for known-failure finalization",
            "plan_task.identity_mismatch",
        )
    plan_source = load_project_plan(plan_path, repo_root=repo_root)
    binding = load_plan_binding(
        plan_source,
        binding_path,
        repo_root=repo_root,
    )
    if binding["manifest_sha256"] != session["binding_manifest_sha256"]:
        raise _protected(
            "binding changed after acceptance",
            "activation.acceptance_invalidated",
        )
    envelope, _, _, _ = _worker_entry(controls, session)
    record = controls.require_store().load_plan(plan_id)
    resolved_binding = resolve_effective_task_binding(
        store=controls.require_store(),
        plan_record=record,
        session=session,
        base_binding=binding,
        task_id=str(envelope["task_id"]),
        repo_root=repo_root,
    )
    active_binding_sha256 = session.get(
        "active_binding_manifest_sha256",
        session["binding_manifest_sha256"],
    )
    if (
        active_binding_sha256
        != resolved_binding["binding_manifest_sha256"]
    ):
        raise _protected(
            "active task binding differs from the finalized authority",
            "activation.acceptance_invalidated",
        )
    entry = resolved_binding["entry"]
    execution_definition = resolved_binding["task_definition"]
    expected_validators = {
        str(item["id"]): str(item["command"])
        for item in entry["validators"]
        if item["required"]
    }
    normalized_results = {
        str(validator_id): str(status).lower()
        for validator_id, status in validator_results.items()
    }
    if (
        set(normalized_results) != set(expected_validators)
        or any(
            status not in {"pass", "fail"}
            for status in normalized_results.values()
        )
        or "fail" not in normalized_results.values()
    ):
        raise _protected(
            "known-failure finalization requires one exact result for every required validator and at least one failure",
            "plan.validation_failed",
            expected_validator_ids=sorted(expected_validators),
        )

    compiled = worker["compiled_invocation"]
    packet = compiled["authority_packet"]
    agent_job = packet["agent_job"]
    direct = {
        "changed_paths": [],
        "acceptance_results": [
            {
                "criterion": criterion,
                "status": "fail",
                "evidence_refs": [],
            }
            for criterion in execution_definition["acceptance_criteria"]
        ],
        "validator_results": [
            {
                "validator_id": validator_id,
                "validator_class": "command_validation",
                "status": status,
                "reason_code": (
                    "plan.validation_failed" if status == "fail" else None
                ),
                "evidence_ref": expected_validators[validator_id],
                "notes": [
                    expected_validators[validator_id],
                    *([summary] if status == "fail" else []),
                ],
            }
            for validator_id, status in normalized_results.items()
        ],
        "checkpoint": {
            "provider": "none",
            "status": "not_required",
            "revision": None,
            "evidence_ref": None,
        },
        "approvals": [
            {
                "approval_id": None,
                "action": item["id"],
                "status": (
                    "approved"
                    if item["status"] == "approved"
                    else "not_required"
                ),
                "evidence_ref": None,
            }
            for item in entry["approval_gates"]
        ],
        "protected_effects": [],
        "warnings": [],
        "indeterminate_checks": [],
        "plan_completion": None,
    }
    result = {
        "starting_revision": record["repository_binding"][
            "starting_revision"
        ],
        "ending_revision": snapshot.repository.binding[
            "starting_revision"
        ],
        "fingerprint_after": snapshot.control_sha256,
        "agentjobs": 1,
        "agent_job_id": agent_job["job_id"],
        "completion_id": f"AJC-{agent_job['job_id']}",
        "task_id": execution_definition["task_id"],
        "decision_id": packet["decision"]["decision_id"],
        "handoff_id": None,
        "global_goal_evaluation": "not_evaluated_here",
        "zero_job_reason": None,
        "direct_evidence": direct,
        "disposition": "validation_failed",
        "reason_code": "plan.validation_failed",
        "terminal_reason": summary,
        "recovery": {"status": "not_required", "action_ref": None},
        "replanning": {"status": "not_required", "action_ref": None},
        "coordinator_action": {
            "kind": "protected_stop",
            "next_task_id": None,
        },
        "pre_topology": copy.deepcopy(
            dict(snapshot.repository.topology)
        ),
        "post_topology": copy.deepcopy(
            dict(snapshot.repository.topology)
        ),
        "finished_at": now,
    }
    verification = verify_plan_task_result(
        plan_record=record,
        task_definition=execution_definition,
        compiled_invocation=compiled,
        result=result,
        fingerprint_before=str(
            worker["claim_receipt"]["fingerprint_before"]
        ),
        observed_repository_topology_before=snapshot.repository.topology,
        direct_observation={
            "ending_revision": result["ending_revision"],
            "fingerprint_after": result["fingerprint_after"],
            "post_topology": result["post_topology"],
            "changed_paths": [],
        },
    )
    if (
        verification.disposition != "validation_failed"
        or verification.guard_reason != "validation"
    ):
        raise IntegrityError(
            "known validator failure did not produce the validation guard"
        )
    result = copy.deepcopy(dict(verification.result))
    with controls.require_store().mutation(
        plan_id,
        expected_revision=expected_plan_revision,
        timestamp=now,
    ) as mutation:
        mutation.begin_task_verification(
            task_id=str(envelope["task_id"]),
            generation=int(envelope["generation"]),
            fingerprint_after=snapshot.control_sha256,
            continue_invocations=1,
            agentjobs=1,
            provider_creates=1,
        )
    verifying = controls.require_store().load_plan(plan_id)
    intent = controls.require_store().find_provider_intent(
        plan_id, int(envelope["generation"])
    )
    receipt = _build_receipt(
        record=verifying,
        task_definition=controls.require_store().load_task_definition(
            plan_id, str(envelope["task_id"])
        ),
        envelope=envelope,
        intent=intent,
        preclaim=PlanWorkerPreclaim(**dict(worker["preclaim"])),
        prior_journal_sha256=verifying["journal"][-1]["event_hash"],
        fingerprint_before=str(
            worker["claim_receipt"]["fingerprint_before"]
        ),
        result=result,
        started_at=str(worker["claim_receipt"]["claimed_at"]),
        finished_at=now,
    )
    outer = controls.require_store().goal_store.load_goal(
        verifying["outer_goal_id"]
    )
    with controls.require_store().mutation(
        plan_id,
        expected_revision=int(verifying["state"]["revision"]),
        timestamp=now,
    ) as mutation:
        _, quarantined = mutation.finalize_task(
            receipt, guard_reason="validation"
        )
        if quarantined:
            raise IntegrityError(
                "known validator failure unexpectedly quarantined"
            )
        mutation.release_plan_lease(
            expected_outer_revision=int(outer["state"]["revision"]),
            holder_token=str(worker["worker_token"]),
        )
    control_result = WebsiteControlStore(repo_root).supersede_packet(
        {
            "expected_control_sha256": snapshot.control_sha256,
            "timestamp": now,
        }
    )
    final = controls.require_store().load_plan(plan_id)
    updated = controls.write_session(
        plan_id,
        {
            **session,
            "status": "task_finalized",
            "website_control_sha256": control_result[
                "website_control_sha256_after"
            ],
            "worker": {
                **worker,
                "receipt_id": receipt["receipt_id"],
                "receipt_sha256": content_sha256(receipt),
                "finalized": True,
            },
            "last_error": {
                "reason_code": "plan.validation_failed",
                "message": summary,
            },
        },
        expected_adapter_revision=session["adapter_revision"],
    )
    return {
        "status": "task_finalized",
        "disposition": "validation_failed",
        "plan_id": plan_id,
        "task_id": envelope["task_id"],
        "generation": envelope["generation"],
        "plan_revision": final["state"]["revision"],
        "plan_phase": final["state"]["phase"],
        "receipt_id": receipt["receipt_id"],
        "receipt_sha256": content_sha256(receipt),
        "schema_version": receipt["schema_version"],
        "website_control_sha256": control_result[
            "website_control_sha256_after"
        ],
        "continue_invocations": 1,
        "agentjobs": 1,
        "adapter_revision": updated["adapter_revision"],
        "next_boundary": "coordinator terminal review",
    }


def worker_unknown(
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    current_thread_id: str,
    reason_code: str,
    repo_root: Path = REPO_ROOT,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Quarantine one already-consumed uncertain invocation without rerun."""

    now = timestamp or utc_now()
    controls = PlanControlStore(repo_root)
    session, snapshot = _require_mutation_cas(
        controls=controls,
        control_store=WebsiteControlStore(repo_root),
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_control_sha256=expected_control_sha256,
    )
    worker = session.get("worker")
    if (
        session.get("status")
        not in {"invocation_consumed", "invocation_unknown"}
        or not isinstance(worker, Mapping)
        or worker.get("codex_task_id") != current_thread_id
        or worker.get("consumed") is not True
    ):
        raise _protected(
            "only one consumed adopted worker may enter unknown quarantine",
            "plan_task.identity_mismatch",
        )
    envelope, _, definition, _ = _worker_entry(controls, session)
    record = controls.require_store().load_plan(plan_id)
    diagnostic = _unknown_continue_diagnostic(
        reason_code=reason_code,
        failure_stage="website_continue_result",
    )
    result = _unknown_continue_result(
        record=record,
        fingerprint_before=str(
            worker["claim_receipt"]["fingerprint_before"]
        ),
        observed_repository_topology=snapshot.repository.topology,
        diagnostic=diagnostic,
    )
    with controls.require_store().mutation(
        plan_id,
        expected_revision=expected_plan_revision,
        timestamp=now,
    ) as mutation:
        mutation.event(
            "task_invocation_unknown",
            {
                "task_id": envelope["task_id"],
                "generation": envelope["generation"],
                "diagnostic": diagnostic,
            },
        )
    verifying = controls.require_store().load_plan(plan_id)
    intent = controls.require_store().find_provider_intent(
        plan_id, int(envelope["generation"])
    )
    receipt = _build_receipt(
        record=verifying,
        task_definition=definition,
        envelope=envelope,
        intent=intent,
        preclaim=PlanWorkerPreclaim(**dict(worker["preclaim"])),
        prior_journal_sha256=verifying["journal"][-1]["event_hash"],
        fingerprint_before=str(
            worker["claim_receipt"]["fingerprint_before"]
        ),
        result=result,
        started_at=str(worker["claim_receipt"]["claimed_at"]),
        finished_at=now,
    )
    outer = controls.require_store().goal_store.load_goal(
        verifying["outer_goal_id"]
    )
    quarantine_token = secrets.token_hex(24)
    with controls.require_store().mutation(
        plan_id,
        expected_revision=int(verifying["state"]["revision"]),
        timestamp=now,
    ) as mutation:
        _, quarantined = mutation.finalize_task(
            receipt, guard_reason="invocation_unknown"
        )
        if not quarantined:
            raise IntegrityError(
                "unknown website invocation was not quarantined"
            )
        mutation.quarantine_plan_lease(
            expected_outer_revision=int(outer["state"]["revision"]),
            current_holder_token=str(worker["worker_token"]),
            holder_token=quarantine_token,
            expires_at=add_seconds(now, 900),
        )
    final = controls.require_store().load_plan(plan_id)
    updated = controls.write_session(
        plan_id,
        {
            **session,
            "status": "invocation_unknown",
            "worker": {
                **worker,
                "receipt_id": receipt["receipt_id"],
                "receipt_sha256": content_sha256(receipt),
                "unknown": True,
                "retry_authorized": False,
            },
            "last_error": diagnostic,
        },
        expected_adapter_revision=session["adapter_revision"],
    )
    return {
        "status": "invocation_unknown",
        "plan_id": plan_id,
        "task_id": envelope["task_id"],
        "plan_revision": final["state"]["revision"],
        "receipt_sha256": content_sha256(receipt),
        "recovery_required": True,
        "retry_authorized": False,
        "adapter_revision": updated["adapter_revision"],
    }


def reserve_next(
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    coordinator_thread_id: str,
    plan_path: str | Path,
    binding_path: str | Path | None,
    repo_root: Path = REPO_ROOT,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Coordinator-only successor reservation after a finalized receipt."""

    now = timestamp or utc_now()
    controls = PlanControlStore(repo_root)
    session, snapshot = _require_mutation_cas(
        controls=controls,
        control_store=WebsiteControlStore(repo_root),
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_control_sha256=expected_control_sha256,
    )
    if (
        coordinator_thread_id != session.get("coordinator_thread_id")
        or session.get("status") != "task_finalized"
    ):
        raise _protected(
            "only the accepted coordinator may reserve a successor after receipt finalization",
            "plan.coordinator_only",
        )
    plan_source = load_project_plan(plan_path, repo_root=repo_root)
    binding = load_plan_binding(
        plan_source,
        binding_path,
        repo_root=repo_root,
    )
    if binding["manifest_sha256"] != session["binding_manifest_sha256"]:
        raise _protected(
            "binding changed after acceptance",
            "activation.acceptance_invalidated",
        )
    record = controls.require_store().load_plan(plan_id)
    selection = controls.require_store().select_next_task(
        plan_id,
        expected_revision=expected_plan_revision,
    )
    if selection.status == "completion_candidate":
        return {
            "status": "no_action",
            "reason_code": "plan.completion_candidate",
            "plan_id": plan_id,
            "plan_revision": expected_plan_revision,
            "website_control_sha256": snapshot.control_sha256,
            "execution_performed": False,
            "provider_create_calls": 0,
            "agentjobs": 0,
            "continue_invocations": 0,
        }
    selected_task_id = str(selection.selected_task["task_id"])
    resolved_binding = resolve_effective_task_binding(
        store=controls.require_store(),
        plan_record=record,
        session=session,
        base_binding=binding,
        task_id=selected_task_id,
        repo_root=repo_root,
    )
    if (
        resolved_binding["replacement"]
        and resolved_binding["authorized_website_control_sha256"]
        != snapshot.control_sha256
    ):
        raise _protected(
            "replacement binding authorization is stale at reservation",
            "activation.acceptance_invalidated",
            task_id=selected_task_id,
            expected=resolved_binding[
                "authorized_website_control_sha256"
            ],
            actual=snapshot.control_sha256,
        )
    if (
        record["state"]["phase"] != "continuation_required"
        or record["state"]["active_task_id"] is not None
        or record["state"]["lease"] is not None
    ):
        raise _protected(
            "successor reservation requires one finalized safe coordinator boundary",
            "plan.successor_not_ready",
        )
    effective_binding = {
        **copy.deepcopy(dict(binding)),
        "tasks": {
            **copy.deepcopy(dict(binding["tasks"])),
            selected_task_id: copy.deepcopy(
                dict(resolved_binding["entry"])
            ),
        },
        "manifest_sha256": resolved_binding[
            "binding_manifest_sha256"
        ],
    }
    outer = controls.require_store().goal_store.load_goal(
        record["outer_goal_id"]
    )
    prepared = PreparedPlan(
        plan=plan_source,
        binding=effective_binding,
        repository=snapshot.repository,
        control=snapshot,
        launcher_preflight=None,
        normalization=None,
        plan_proposal={},
        goal_proposal={},
        completion_contract={},
        acceptance_basis={
            "current_thread_id": coordinator_thread_id,
            "reasoning_effort": session["reasoning_effort"],
        },
        acceptance_text="",
    )
    session = controls.write_session(
        plan_id,
        {
            **session,
            "status": "successor_activation_in_progress",
            "last_error": None,
        },
        expected_adapter_revision=session["adapter_revision"],
    )
    try:
        reservation = _reserve_task(
            plan_store=controls,
            prepared=prepared,
            expected_plan_revision=expected_plan_revision,
            expected_outer_revision=int(outer["state"]["revision"]),
            outer_holder_token=None,
            predecessor_thread_id=coordinator_thread_id,
            first_task=False,
            timestamp=now,
        )
        session = controls.write_session(
            plan_id,
            {
                **session,
                "status": "task_reserved",
                "reservation": _reservation_session(reservation),
                "control_activation": None,
                "website_control_sha256": expected_control_sha256,
                "active_binding_manifest_sha256": resolved_binding[
                    "binding_manifest_sha256"
                ],
                "worker": None,
                "last_error": None,
            },
            expected_adapter_revision=session["adapter_revision"],
        )
        activation = _activate_reserved_packet(
            reservation=reservation,
            prepared=prepared,
            expected_control_sha256=expected_control_sha256,
            timestamp=now,
        )
        session = controls.write_session(
            plan_id,
            {
                **session,
                "status": "website_packet_activated",
                "control_activation": activation,
                "website_control_sha256": activation[
                    "website_control_sha256_after"
                ],
                "last_error": None,
            },
            expected_adapter_revision=session["adapter_revision"],
        )
        provider = ManualThreadProvider(
            repo_root,
            local_root=MANUAL_RELATIVE,
            current_thread_id=coordinator_thread_id,
            timestamp=now,
        )
        dispatch = dispatch_reserved_plan_task(
            controls.require_store(),
            reservation=reservation,
            provider=provider,
            timestamp=now,
        )
        if dispatch.status != "manual_handoff_pending":
            raise _protected(
                "successor dispatch did not preserve one manual adoption intent",
                "provider.dispatch_unexpected",
            )
        updated = controls.write_session(
            plan_id,
            {
                **session,
                "status": "awaiting_task_creation",
                "provider_intent_id": dispatch.intent_id,
                "provider_intent_sha256": dispatch.intent_sha256,
                "last_error": None,
            },
            expected_adapter_revision=session["adapter_revision"],
        )
    except Exception as error:
        controls.write_session(
            plan_id,
            {
                **session,
                "status": "recovery_required",
                "last_error": {
                    "type": type(error).__name__,
                    "message": str(error),
                },
            },
            expected_adapter_revision=session["adapter_revision"],
        )
        raise
    current = controls.require_store().load_plan(plan_id)
    return {
        "status": "awaiting_task_creation",
        "plan_id": plan_id,
        "plan_revision": current["state"]["revision"],
        "website_control_sha256": updated["website_control_sha256"],
        "task_create_request": _task_create_request(
            updated, repo_root=repo_root
        ),
        "agentjobs": 0,
        "continue_invocations": 0,
    }


def recover(
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_control_sha256: str,
    coordinator_thread_id: str,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Inspect and safely resume without duplicating task or execution state."""

    controls = PlanControlStore(repo_root)
    session, snapshot = _require_mutation_cas(
        controls=controls,
        control_store=WebsiteControlStore(repo_root),
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_control_sha256=expected_control_sha256,
    )
    if coordinator_thread_id != session.get("coordinator_thread_id"):
        raise _protected(
            "protected recovery is coordinator-only",
            "plan.coordinator_only",
        )
    record = controls.require_store().load_plan(plan_id)
    intent = (
        controls.require_store().find_provider_intent(
            plan_id, int(record["state"]["current_generation"])
        )
        if record["state"]["current_generation"]
        else None
    )
    if session.get("ambiguous_task_creation") is True:
        return {
            "status": "manual_adoption_required",
            "plan_id": plan_id,
            "plan_revision": expected_plan_revision,
            "retry_task_creation": False,
            "adopt_original_task": True,
            "task_create_request": _task_create_request(
                session, repo_root=repo_root
            ),
        }
    if isinstance(intent, Mapping) and intent.get("status") == "intent":
        return {
            "status": "manual_adoption_required",
            "plan_id": plan_id,
            "plan_revision": expected_plan_revision,
            "retry_task_creation": False,
            "task_create_request": _task_create_request(
                session, repo_root=repo_root
            ),
        }
    if session.get("status") == "recovery_required":
        reservation = session.get("reservation")
        return {
            "status": "recovery_required",
            "plan_id": plan_id,
            "plan_revision": expected_plan_revision,
            "website_control_sha256": snapshot.control_sha256,
            "reserved_task_id": (
                reservation.get("summary", {}).get("task_id")
                if isinstance(reservation, Mapping)
                else None
            ),
            "website_packet_activated": isinstance(
                session.get("control_activation"),
                Mapping,
            ),
            "retry_task_creation": False,
            "retry_task_reservation": False,
            "duplicate_state_created": False,
            "next_action": "inspect and reconcile the recorded partial boundary",
        }
    if session.get("status") == "invocation_unknown":
        return {
            "status": "recovery_required",
            "plan_id": plan_id,
            "plan_revision": expected_plan_revision,
            "retry_task_execution": False,
            "quarantined": True,
        }
    return {
        "status": "recovery_inspected",
        "plan_id": plan_id,
        "plan_revision": expected_plan_revision,
        "plan_phase": record["state"]["phase"],
        "website_control_sha256": snapshot.control_sha256,
        "duplicate_state_created": False,
        "next_action": (
            "reserve-next"
            if record["state"]["phase"] == "continuation_required"
            else "worker-finalize"
            if session.get("status") == "invocation_consumed"
            else "inspect protected state"
        ),
    }


def status(
    *,
    plan_id: str | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Read-only combined website and imported plan status."""

    control = WebsiteControlStore(repo_root).snapshot()
    if (
        control.resolver_exit_code != 0
        or control.resolver.get("status") not in {"ready", "no_action"}
    ):
        raise _protected(
            "website implementation control is malformed or blocked",
            str(
                control.resolver.get("reason_code")
                or "website.control_blocked"
            ),
            resolver=copy.deepcopy(dict(control.resolver)),
        )
    plans = PlanControlStore(repo_root, read_only=True).status(plan_id)
    return {
        "status": (
            "no_action"
            if control.resolver.get("status") == "no_action"
            and not plans["plans"]
            else "ready"
        ),
        "website_control": control.as_dict(),
        "plan_control": plans,
        "effects": {
            "state_writes": 0,
            "provider_create_calls": 0,
            "worker_discussions": 0,
            "agentjobs": 0,
            "continue_invocations": 0,
        },
    }


__all__ = [
    "ADAPTER_CONFIG_RELATIVE",
    "ADAPTER_RUNTIME_RELATIVE",
    "ADOPTION_RELATIVE",
    "BINDING_ROOT_RELATIVE",
    "CONTROL_ACTIVATION_RELATIVE",
    "EXPECTED_LOCK_SHA256",
    "EXPECTED_SKILLS",
    "LOCK_RELATIVE",
    "MANUAL_RELATIVE",
    "PLAN_SCHEMA_ROOT_RELATIVE",
    "PROVENANCE_RELATIVE",
    "STATE_RELATIVE",
    "PlanControlStore",
    "PreparedPlan",
    "WebsiteControlSnapshot",
    "WebsiteControlStore",
    "WebsiteProjectAdapter",
    "WebsitePlanAdapterError",
    "WebsiteRepositoryProvider",
    "WebsiteThreadExecutionProfileProvider",
    "activate_plan",
    "adopt_worker",
    "canonical_json",
    "compile_binding_director_route",
    "directory_sha256",
    "file_sha256",
    "load_adapter_config",
    "load_plan_binding",
    "load_project_plan",
    "prepare_plan",
    "recover",
    "render_yaml",
    "reserve_next",
    "run_conformance",
    "status",
    "validate_binding_manifest",
    "verify_installed_bundle",
    "worker_consume",
    "worker_fail",
    "worker_finalize",
    "worker_prepare",
    "worker_unknown",
]
