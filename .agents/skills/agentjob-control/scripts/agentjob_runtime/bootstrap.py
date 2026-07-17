"""Idempotent portable-profile bootstrap and read-only project doctor."""

from __future__ import annotations

import hashlib
import os
import re
import stat
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime import PROTOCOL_VERSION
from agentjob_runtime.adapters.project_filesystem import FilesystemProjectAdapter
from agentjob_runtime.adapters.repository_filesystem import FilesystemRepositoryProvider
from agentjob_runtime.adapters.repository_git import GitRepositoryProvider
from agentjob_runtime.config import load_config, resolve_project_path
from agentjob_runtime.errors import AgentJobControlError, IntegrityError, SecurityError, StateConflict
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.records.canonical import (
    content_sha256,
    load_structured,
    render_canonical_json,
)
from agentjob_runtime.validation.schema import format_issues, validate_instance


LOCAL_STATE_LINE = ".local/sys4ai/continuation/"
ROLE_DEFINITIONS = {
    "system-analyst": (
        "Inspect canonical project state and define bounded evidence needs.",
        "Grant execution authority or infer domain truth.",
    ),
    "system-engineer": (
        "Maintain control structure, interfaces, and portable governance.",
        "Bypass activated AgentJob boundaries.",
    ),
    "software-engineer": (
        "Implement one activated bounded AgentJob.",
        "Expand paths, actions, commands, or claims beyond activation.",
    ),
    "validator-engineer": (
        "Validate direct process evidence and report uncertainty.",
        "Treat process validation as domain truth.",
    ),
    "system-architect": (
        "Evaluate architecture only when canonical evidence requires it.",
        "Replace a local fix with an unapproved redesign.",
    ),
}


@dataclass(frozen=True)
class DoctorReport:
    status: str
    profile: str | None
    repository_provider: str | None
    control_root: str | None
    local_state_root: str | None
    findings: tuple[Mapping[str, str], ...]
    capabilities: Mapping[str, Any]
    sqlite: Mapping[str, Any] | None
    execution_performed: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BootstrapReport:
    status: str
    selected_profile: str
    repository_provider: str
    planned_files: tuple[str, ...]
    created_files: tuple[str, ...]
    existing_files: tuple[str, ...]
    created_directories: tuple[str, ...]
    rollback_manifest: str | None
    doctor: Mapping[str, Any] | None
    error: Mapping[str, Any] | None
    execution_performed: bool = False
    agent_jobs_executed: int = 0

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _project_id(root: Path) -> str:
    value = re.sub(r"[^A-Za-z0-9._:-]+", "-", root.name).strip("-.")
    if len(value) < 3:
        value = f"project-{value or 'root'}"
    return value[:160]


def _config_yaml(project_id: str, repository_provider: str) -> str:
    checkpoint = "git_status" if repository_provider == "git" else "none"
    return f"""schema_version: sys4ai.continuation-config.v1
project:
  id: {project_id}
  root: project
  control_namespace: default
runtime:
  harness: codex
  surfaces: [desktop, cli, ide]
control:
  profile: portable_registered
  root: .agents/control
  adapter: filesystem
  one_agentjob_per_continue: true
  immutable_after_activation: true
  supersession_required: true
goal_relay:
  state_backend: sqlite
  local_root: .local/sys4ai/continuation
  thread_provider: manual-handoff
  thread_strategy: fresh_summary
  native_goal_mirror: false
  at_most_once_consumption: true
  max_live_continuations: 1
repository:
  provider: {repository_provider}
  default_branch_policy: warn
  dirty_state_policy: job_specific
  fingerprint_provider: canonical-repository-control
roles:
  catalog: [.agents/control/roles]
  allow_task_overlays: true
  allow_one_job_provisional_roles: true
policy:
  packs: [.agents/control/policies/default.yaml]
  strict_extensions: true
validation:
  pre_execution: [control-record-validator, active-lease-validator, repository-binding-validator]
  post_write: [changed-path-allowlist, command-evidence-validator, claim-boundary-linter]
checkpoint:
  provider: {checkpoint}
  auto_commit: false
security:
  default_network_access: false
  reject_goal_secrets: true
  reject_symlink_state_paths: true
  reject_hardlink_aliases: true
  allow_environment_fields: []
human_gates:
  protected_actions: [public-release, production-deployment, secret-access, policy-change, irreversible-external-action]
"""


def _role_yaml(role_id: str, responsibility: str, prohibition: str) -> str:
    return f"""role_id: {role_id}
version: 1.0.0
responsibilities:
  - {responsibility}
may_not:
  - {prohibition}
authority_effect: role-candidate-only
"""


def _schema_lock_yaml(schema_root: Path) -> str:
    hashes = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(schema_root.glob("*.json"))
    }
    return (
        "schema_version: sys4ai.schemas-lock.v1\n"
        f"protocol_version: {PROTOCOL_VERSION}\n"
        "adapter_id: filesystem\n"
        "adapter_version: 1.0.0\n"
        f"schema_bundle_sha256: {content_sha256(hashes)}\n"
    )


def _program_state_yaml() -> str:
    return """schema_version: sys4ai.program-state.v1
status: initialized
current_task_id: null
current_decision_id: null
current_job_id: null
execution_performed: false
"""


def _assert_safe_parent(root: Path, path: Path) -> None:
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise SecurityError("bootstrap path escapes project root") from error
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if current.exists() and current.is_symlink():
            raise SecurityError(f"bootstrap path traverses a symlink: {current}")


def _ensure_directory(root: Path, path: Path) -> bool:
    _assert_safe_parent(root, path / "sentinel")
    if path.exists():
        if path.is_symlink() or not path.is_dir():
            raise SecurityError(f"bootstrap directory path is unsafe: {path}")
        return False
    path.mkdir(parents=True, mode=0o700)
    return True


def _write_identical_or_create(root: Path, path: Path, payload: bytes) -> bool:
    _assert_safe_parent(root, path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.is_symlink() or not path.is_file():
            raise SecurityError(f"bootstrap file path is unsafe: {path}")
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise SecurityError(f"bootstrap file has an unsafe alias: {path}")
        if path.read_bytes() == payload:
            return False
        raise StateConflict(
            f"bootstrap refuses to overwrite a different existing file: {path}",
            details={"reason_code": "bootstrap.file_conflict"},
        )
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return True


def _append_gitignore(root: Path) -> tuple[bool, bool]:
    path = root / ".gitignore"
    if path.exists():
        if path.is_symlink() or not path.is_file() or path.stat().st_nlink != 1:
            raise SecurityError("bootstrap refuses unsafe .gitignore")
        text = path.read_text(encoding="utf-8")
    else:
        text = ""
    if LOCAL_STATE_LINE in text.splitlines():
        return False, path.exists()
    prefix = text
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    created = _write_identical_or_create(
        root, path, f"{prefix}{LOCAL_STATE_LINE}\n".encode("utf-8")
    ) if not path.exists() else False
    if path.exists() and not created:
        payload = f"{prefix}{LOCAL_STATE_LINE}\n".encode("utf-8")
        _assert_safe_parent(root, path)
        descriptor, temporary_name = tempfile.mkstemp(prefix=".gitignore.", dir=root)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()
    return True, not text


def _detect_repository(root: Path) -> str:
    try:
        GitRepositoryProvider(root)
        return "git"
    except AgentJobControlError:
        FilesystemRepositoryProvider(root)
        return "filesystem_only"


def _finding(severity: str, code: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "message": message}


def doctor_project(
    project_root: str | Path, *, config_path: str | Path | None = None
) -> DoctorReport:
    """Inspect every configured profile without creating or repairing state."""

    root = Path(project_root).expanduser().resolve()
    findings: list[dict[str, str]] = []
    try:
        loaded = load_config(root, config_path=config_path)
    except AgentJobControlError as error:
        return DoctorReport(
            "fail",
            None,
            None,
            None,
            None,
            (_finding("failure", error.code, str(error)),),
            {},
            None,
        )
    for capability in loaded.capabilities.capabilities:
        if not capability.available:
            findings.append(
                _finding(
                    "failure" if capability.required else "warning",
                    capability.reason_code or "capability.unavailable",
                    f"{capability.capability_id}: {capability.provider}",
                )
            )
    for name in ("roles", "policies", "tasks", "handoffs", "indexes"):
        path = loaded.control_root / name
        if not path.is_dir():
            findings.append(_finding("failure", "bootstrap.directory_missing", str(path)))
    schema = Path(__file__).resolve().parents[2] / "schemas" / "policy-pack.schema.json"
    for relative in loaded.data["policy"]["packs"]:
        try:
            path = resolve_project_path(root, relative, purpose="doctor policy pack")
            policy = load_structured(path)
            issues = validate_instance(policy, schema)
            if issues:
                findings.append(
                    _finding(
                        "failure",
                        "policy.invalid",
                        format_issues(issues),
                    )
                )
        except (AgentJobControlError, OSError) as error:
            findings.append(_finding("failure", "policy.unreadable", str(error)))
    if loaded.data["control"]["profile"] == "portable_registered":
        lock = loaded.control_root / "schemas.lock.yaml"
        if not lock.is_file():
            findings.append(_finding("failure", "bootstrap.schema_lock_missing", str(lock)))
    sqlite_report: Mapping[str, Any] | None = None
    if loaded.data["goal_relay"]["state_backend"] == "sqlite":
        database = loaded.local_state_root / "state.sqlite3"
        if not database.is_file():
            findings.append(_finding("failure", "state.sqlite_missing", str(database)))
        else:
            try:
                sqlite_report = SQLiteGoalStore(
                    database, auto_migrate=False, read_only=True
                ).integrity_check()
                if sqlite_report["status"] != "pass":
                    findings.append(
                        _finding("failure", "state.sqlite_integrity_failed", str(database))
                    )
            except (AgentJobControlError, OSError) as error:
                findings.append(_finding("failure", "state.sqlite_unreadable", str(error)))
    try:
        if loaded.data["control"]["adapter"] == "filesystem":
            report = FilesystemProjectAdapter(
                root, config_path=loaded.config_path
            ).discover(root)
            if report.status != "ready":
                findings.append(
                    _finding("failure", "adapter.capability_mismatch", str(report.missing_required))
                )
    except AgentJobControlError as error:
        findings.append(_finding("failure", error.code, str(error)))
    status = "pass" if not any(item["severity"] == "failure" for item in findings) else "fail"
    return DoctorReport(
        status,
        str(loaded.data["control"]["profile"]),
        str(loaded.data["repository"]["provider"]),
        str(loaded.control_root),
        str(loaded.local_state_root),
        tuple(findings),
        loaded.capabilities.as_dict(),
        sqlite_report,
    )


def bootstrap_project(
    project_root: str | Path,
    *,
    dry_run: bool = False,
) -> BootstrapReport:
    """Create a portable registered profile and no task or AgentJob."""

    root = Path(project_root).expanduser().resolve()
    if not root.is_dir():
        raise IntegrityError(f"project root is not a directory: {root}")
    control = root / ".agents/control"
    config = control / "config.yaml"
    repository_provider = _detect_repository(root)
    if config.is_file():
        doctor = doctor_project(root, config_path=config)
        return BootstrapReport(
            "already_initialized" if doctor.status == "pass" else "existing_configuration_invalid",
            "portable_registered",
            repository_provider,
            (),
            (),
            (config.relative_to(root).as_posix(),),
            (),
            None,
            doctor.as_dict(),
            None,
        )
    if control.exists() and any(control.iterdir()):
        return BootstrapReport(
            "existing_control_detected",
            "existing_control_adapter",
            repository_provider,
            (".agents/control/config.yaml",),
            (),
            tuple(
                path.relative_to(root).as_posix()
                for path in sorted(control.rglob("*"))
                if path.is_file()
            ),
            (),
            None,
            None,
            {
                "code": "bootstrap.existing_control_requires_mapping",
                "message": "Existing control evidence requires an explicit adapter mapping.",
            },
        )
    package = Path(__file__).resolve().parents[2]
    schema_root = package / "schemas"
    policy_source = package / "policy-packs" / "generic-software.yaml"
    files: dict[Path, bytes] = {
        config: _config_yaml(_project_id(root), repository_provider).encode("utf-8"),
        control / "program-state.yaml": _program_state_yaml().encode("utf-8"),
        control / "policies/default.yaml": policy_source.read_bytes(),
        control / "schemas.lock.yaml": _schema_lock_yaml(schema_root).encode("utf-8"),
    }
    for role_id, (responsibility, prohibition) in ROLE_DEFINITIONS.items():
        files[control / f"roles/{role_id}.yaml"] = _role_yaml(
            role_id, responsibility, prohibition
        ).encode("utf-8")
    directories = tuple(
        control / name for name in ("roles", "policies", "tasks", "handoffs", "indexes")
    ) + (
        root / ".local/sys4ai/continuation/snapshots",
        root / ".local/sys4ai/continuation/logs",
    )
    database = root / ".local/sys4ai/continuation/state.sqlite3"
    rollback = root / ".local/sys4ai/continuation/bootstrap-rollback.json"
    planned = tuple(
        sorted(
            [path.relative_to(root).as_posix() for path in files]
            + [database.relative_to(root).as_posix(), rollback.relative_to(root).as_posix(), ".gitignore"]
        )
    )
    if dry_run:
        return BootstrapReport(
            "dry_run",
            "portable_registered",
            repository_provider,
            planned,
            (),
            (),
            (),
            rollback.relative_to(root).as_posix(),
            None,
            None,
        )
    created_files: list[str] = []
    existing_files: list[str] = []
    created_directories: list[str] = []
    appended_gitignore = False
    try:
        for directory in directories:
            if _ensure_directory(root, directory):
                created_directories.append(directory.relative_to(root).as_posix())
        for path, payload in files.items():
            relative = path.relative_to(root).as_posix()
            if _write_identical_or_create(root, path, payload):
                created_files.append(relative)
            else:
                existing_files.append(relative)
        appended_gitignore, gitignore_created = _append_gitignore(root)
        if gitignore_created:
            created_files.append(".gitignore")
        elif not appended_gitignore:
            existing_files.append(".gitignore")
        database_existed = database.exists()
        state = SQLiteGoalStore(database)
        sqlite_report = state.integrity_check()
        if sqlite_report["status"] != "pass":
            raise IntegrityError("new SQLite state failed integrity check")
        if not database_existed:
            created_files.append(database.relative_to(root).as_posix())
        rollback_record = {
            "schema_version": "sys4ai.bootstrap-rollback.v1",
            "project_root": str(root),
            "created_files": sorted(created_files),
            "created_directories": sorted(created_directories, reverse=True),
            "gitignore_appended_lines": [LOCAL_STATE_LINE] if appended_gitignore else [],
            "preserve_preexisting_files": True,
            "execution_performed": False,
        }
        if _write_identical_or_create(
            root, rollback, render_canonical_json(rollback_record).encode("utf-8")
        ):
            created_files.append(rollback.relative_to(root).as_posix())
        doctor = doctor_project(root, config_path=config)
        return BootstrapReport(
            "initialized" if doctor.status == "pass" else "initialized_with_findings",
            "portable_registered",
            repository_provider,
            planned,
            tuple(sorted(created_files)),
            tuple(sorted(existing_files)),
            tuple(sorted(created_directories)),
            rollback.relative_to(root).as_posix(),
            doctor.as_dict(),
            None,
        )
    except (AgentJobControlError, OSError) as error:
        partial_record = {
            "schema_version": "sys4ai.bootstrap-rollback.v1",
            "project_root": str(root),
            "created_files": sorted(created_files),
            "created_directories": sorted(created_directories, reverse=True),
            "gitignore_appended_lines": [LOCAL_STATE_LINE] if appended_gitignore else [],
            "preserve_preexisting_files": True,
            "partial_failure": True,
            "error_code": getattr(error, "code", "bootstrap.io_failure"),
            "execution_performed": False,
        }
        rollback_path: str | None = None
        try:
            rollback.parent.mkdir(parents=True, exist_ok=True)
            if not rollback.exists():
                _write_identical_or_create(
                    root, rollback, render_canonical_json(partial_record).encode("utf-8")
                )
                rollback_path = rollback.relative_to(root).as_posix()
        except Exception:
            rollback_path = None
        return BootstrapReport(
            "partial_failure",
            "portable_registered",
            repository_provider,
            planned,
            tuple(sorted(created_files)),
            tuple(sorted(existing_files)),
            tuple(sorted(created_directories)),
            rollback_path,
            None,
            {
                "code": getattr(error, "code", "bootstrap.io_failure"),
                "message": str(error),
            },
        )
