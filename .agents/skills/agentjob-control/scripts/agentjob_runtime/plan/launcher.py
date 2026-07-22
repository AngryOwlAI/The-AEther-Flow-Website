"""Implementation-plan launcher preflight, intake, and first-task reservation."""

from __future__ import annotations

import copy
import errno
import hashlib
import os
import secrets
import stat
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agentjob_runtime.config import resolve_project_path
from agentjob_runtime.errors import (
    IntegrityError,
    RecordValidationError,
    SecurityError,
    StateConflict,
)
from agentjob_runtime.goal.launcher import ThreadCreateResult, ThreadProvider
from agentjob_runtime.goal.leases import DEFAULT_LEASE_SECONDS
from agentjob_runtime.goal.model import add_seconds, parse_utc, utc_now
from agentjob_runtime.path_security import resolve_project_relative
from agentjob_runtime.plan.lifecycle import holder_token_sha256
from agentjob_runtime.plan.prompts import (
    build_plan_task_dependency_proof,
    build_plan_task_envelope,
    build_plan_task_worker_prompt,
)
from agentjob_runtime.plan.sqlite_store import SQLitePlanStore
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import contains_secret


REQUIRED_PLAN_LAUNCHER_CAPABILITIES = frozenset(
    {
        "agentjob_control",
        "plan_state",
        "repository_provider",
        "thread_provider",
        "thread_execution_profile",
        "repository_topology_enforcement",
    }
)
SOURCE_AUTHORITIES = frozenset(
    {
        "accepted",
        "supplemental",
        "advisory",
        "historical",
        "unknown",
    }
)
REPOSITORY_IDENTITY_FIELDS = (
    "project_id",
    "root",
    "worktree",
    "branch",
    "git_common_dir",
    "starting_revision",
    "environment_mode",
)
# Selection revision -> reservation -> provider intent -> provider outcome.
FIRST_TASK_CLAIM_REVISION_ADVANCE = 3


@dataclass(frozen=True)
class PlanSourceRequest:
    """One project-contained source and its externally established authority."""

    path: str
    authority: str
    precedence: int | None = None


@dataclass(frozen=True)
class PlanSourceIntake:
    """A bounded transient source read with a safe public metadata projection."""

    relative_path: str
    source_sha256: str
    size_bytes: int
    media_type: str
    authority: str
    precedence: int
    raw_bytes: bytes = field(repr=False, compare=False)
    text: str = field(repr=False, compare=False)

    def public_metadata(self) -> dict[str, Any]:
        return {
            "relative_path": self.relative_path,
            "source_sha256": self.source_sha256,
            "size_bytes": self.size_bytes,
            "media_type": self.media_type,
            "authority": self.authority,
            "precedence": self.precedence,
        }


@dataclass(frozen=True)
class PlanLauncherGuards:
    """Explicit resource and cardinality limits for one read-only preflight."""

    max_sources: int
    max_source_bytes: int
    max_total_source_bytes: int
    max_provider_creates: int = 1
    max_agentjobs: int = 0


@dataclass(frozen=True)
class PlanLauncherPreflight:
    """Safe preflight result; source payloads remain transient and non-public."""

    project_root: str
    local_state_root: str
    state_path: str
    provider_id: str
    sources: tuple[PlanSourceIntake, ...] = field(repr=False)
    repository_binding: Mapping[str, Any] = field(
        default_factory=dict,
        repr=False,
    )
    state_writes: int = 0
    provider_create_calls: int = 0
    worker_discussions: int = 0
    agentjobs_executed: int = 0
    continue_invocations: int = 0
    task_reservations: int = 0
    branch_creations: int = 0
    worktree_creations: int = 0
    status: str = "ready"

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "project_root": self.project_root,
            "local_state_root": self.local_state_root,
            "state_path": self.state_path,
            "provider_id": self.provider_id,
            "source_count": len(self.sources),
            "source_total_bytes": sum(item.size_bytes for item in self.sources),
            "sources": [item.public_metadata() for item in self.sources],
            "state_writes": self.state_writes,
            "provider_create_calls": self.provider_create_calls,
            "worker_discussions": self.worker_discussions,
            "agentjobs_executed": self.agentjobs_executed,
            "continue_invocations": self.continue_invocations,
            "task_reservations": self.task_reservations,
            "branch_creations": self.branch_creations,
            "worktree_creations": self.worktree_creations,
        }


@dataclass(frozen=True)
class PlanTaskReservationResult:
    """Safe summary plus private artifacts for one first-task reservation."""

    plan_record: Mapping[str, Any] = field(repr=False)
    outer_goal_record: Mapping[str, Any] = field(repr=False)
    selection_proof: Mapping[str, Any] = field(repr=False)
    task_definition: Mapping[str, Any] = field(repr=False)
    envelope: Mapping[str, Any] = field(repr=False)
    worker_prompt: str = field(repr=False)
    envelope_schema_path: Path = field(repr=False)
    expected_worker_revision: int
    selection_proof_sha256: str

    def as_dict(self) -> dict[str, Any]:
        plan = self.plan_record
        state = plan["state"]
        selected = self.selection_proof["selected_task"]
        dependency_proof = build_plan_task_dependency_proof(
            self.selection_proof,
            self.task_definition,
        )
        return {
            "status": "task_reserved",
            "plan_id": plan["plan_id"],
            "plan_sha256": plan["effective_plan_sha256"],
            "plan_revision": state["revision"],
            "outer_goal_revision": self.outer_goal_record["state"]["revision"],
            "plan_phase": state["phase"],
            "task_id": selected["task_id"],
            "task_sha256": selected["task_sha256"],
            "generation": self.envelope["generation"],
            "idempotency_key": self.envelope["idempotency_key"],
            "selection_proof_id": self.selection_proof["proof_id"],
            "selection_proof_sha256": self.selection_proof_sha256,
            "task_definition_sha256": content_sha256(self.task_definition),
            "dependency_proof_sha256": content_sha256(dependency_proof),
            "dependency_receipt_sha256s": copy.deepcopy(
                selected["dependency_receipt_sha256s"]
            ),
            "envelope_sha256": content_sha256(self.envelope),
            "expected_revision": self.expected_worker_revision,
            "worker_prompt_sha256": hashlib.sha256(
                self.worker_prompt.encode("utf-8")
            ).hexdigest(),
            "handoff_token_sha256": holder_token_sha256(
                str(self.envelope["handoff_token"])
            ),
            "plan_lease_transaction_id": state["lease"]["transaction_id"],
            "state_writes": 1,
            "worker_discussions": state["counters"]["worker_discussions"],
            "provider_create_calls": 0,
            "successor_creates": state["counters"]["successor_creates"],
            "same_task_successors": 0,
            "agentjobs_executed": 0,
            "continue_invocations": 0,
            "next_boundary": "persist_provider_intent",
        }


@dataclass(frozen=True)
class PlanTaskDispatchResult:
    """Redacted summary plus private evidence for one provider dispatch."""

    status: str
    plan_id: str
    task_id: str
    generation: int
    provider_id: str
    intent_id: str
    intent_sha256: str
    provider_response_sha256: str
    plan_revision: int
    outer_goal_revision: int
    successor_thread_id: str | None
    manual_handoff_path: str | None
    lease_holder_kind: str
    recovery_required: bool
    state_writes: int
    next_boundary: str
    plan_record: Mapping[str, Any] = field(repr=False, compare=False)
    outer_goal_record: Mapping[str, Any] = field(repr=False, compare=False)
    provider_intent: Mapping[str, Any] = field(repr=False, compare=False)
    provider_response: Mapping[str, Any] = field(repr=False, compare=False)
    provider_create_calls: int = 1
    agentjobs_executed: int = 0
    continue_invocations: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "plan_id": self.plan_id,
            "task_id": self.task_id,
            "generation": self.generation,
            "provider_id": self.provider_id,
            "intent_id": self.intent_id,
            "intent_sha256": self.intent_sha256,
            "provider_response_sha256": self.provider_response_sha256,
            "plan_revision": self.plan_revision,
            "outer_goal_revision": self.outer_goal_revision,
            "successor_thread_id": self.successor_thread_id,
            "manual_handoff_path": self.manual_handoff_path,
            "lease_holder_kind": self.lease_holder_kind,
            "recovery_required": self.recovery_required,
            "state_writes": self.state_writes,
            "provider_create_calls": self.provider_create_calls,
            "agentjobs_executed": self.agentjobs_executed,
            "continue_invocations": self.continue_invocations,
            "next_boundary": self.next_boundary,
        }


def _reason(
    message: str,
    *,
    reason_code: str,
    **details: Any,
) -> RecordValidationError:
    return RecordValidationError(
        message,
        details={"reason_code": reason_code, **details},
    )


def _validate_positive_integer(value: Any, *, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise _reason(
            f"{field_name} must be a positive integer",
            reason_code="plan.validation_failed",
            field=field_name,
        )
    return value


def _validate_guards(guards: PlanLauncherGuards) -> None:
    if not isinstance(guards, PlanLauncherGuards):
        raise _reason(
            "plan launcher guards must use the canonical guard type",
            reason_code="plan.validation_failed",
            field="guards",
        )
    _validate_positive_integer(guards.max_sources, field_name="max_sources")
    _validate_positive_integer(
        guards.max_source_bytes,
        field_name="max_source_bytes",
    )
    _validate_positive_integer(
        guards.max_total_source_bytes,
        field_name="max_total_source_bytes",
    )
    if (
        isinstance(guards.max_provider_creates, bool)
        or guards.max_provider_creates != 1
    ):
        raise _reason(
            "plan launcher must permit exactly one provider create at most",
            reason_code="plan.validation_failed",
            field="max_provider_creates",
        )
    if isinstance(guards.max_agentjobs, bool) or guards.max_agentjobs != 0:
        raise _reason(
            "plan launcher must execute zero AgentJobs",
            reason_code="plan.validation_failed",
            field="max_agentjobs",
        )


def _validate_capabilities(
    capabilities: Mapping[str, bool],
    provider: ThreadProvider,
) -> str:
    if not isinstance(capabilities, Mapping):
        raise _reason(
            "plan launcher capabilities must be a mapping",
            reason_code="plan_task.capability_missing",
            missing=sorted(REQUIRED_PLAN_LAUNCHER_CAPABILITIES),
        )
    missing = sorted(
        capability
        for capability in REQUIRED_PLAN_LAUNCHER_CAPABILITIES
        if capabilities.get(capability) is not True
    )
    if missing:
        raise _reason(
            "plan launcher capabilities are incomplete",
            reason_code="plan_task.capability_missing",
            missing=missing,
        )
    raw_provider_id = getattr(provider, "provider_id", None)
    if (
        getattr(provider, "available", False) is not True
        or not isinstance(raw_provider_id, str)
        or not raw_provider_id.strip()
    ):
        raise _reason(
            "selected ThreadProvider is unavailable",
            reason_code="plan_task.capability_missing",
            missing=["thread_provider"],
        )
    return raw_provider_id.strip()


def _validate_repository(
    project_root: str | Path,
    repository_binding: Mapping[str, Any],
    repository_observation: Mapping[str, Any],
) -> Path:
    if not isinstance(repository_binding, Mapping) or not isinstance(
        repository_observation,
        Mapping,
    ):
        raise _reason(
            "repository binding and observation must be mappings",
            reason_code="plan.repository_mismatch",
        )
    try:
        root = Path(project_root).expanduser().resolve(strict=True)
    except (OSError, TypeError) as error:
        raise _reason(
            "explicit project root is unavailable",
            reason_code="plan.repository_mismatch",
            field="root",
        ) from error
    for field_name in REPOSITORY_IDENTITY_FIELDS:
        if field_name not in repository_binding or field_name not in repository_observation:
            raise _reason(
                "repository identity is incomplete",
                reason_code="plan.repository_mismatch",
                field=field_name,
            )
        if repository_observation[field_name] != repository_binding[field_name]:
            raise _reason(
                "repository observation differs from the requested binding",
                reason_code="plan.repository_mismatch",
                field=field_name,
            )
    for field_name in (
        "project_id",
        "root",
        "worktree",
        "branch",
        "starting_revision",
        "environment_mode",
    ):
        value = repository_binding[field_name]
        if not isinstance(value, str) or not value.strip():
            raise _reason(
                "repository identity contains a blank field",
                reason_code="plan.repository_mismatch",
                field=field_name,
            )
    if repository_binding["environment_mode"] not in {"local", "worktree"}:
        raise _reason(
            "secure local source intake requires a local or worktree repository",
            reason_code="plan_task.capability_missing",
            missing=["local_repository_provider"],
        )
    for field_name in ("root", "worktree"):
        raw = str(repository_binding[field_name])
        try:
            observed_path = Path(raw).expanduser().resolve(strict=True)
        except OSError as error:
            raise _reason(
                f"repository {field_name} is unavailable",
                reason_code="plan.repository_mismatch",
                field=field_name,
            ) from error
        if observed_path != root or raw != str(observed_path):
            raise _reason(
                f"repository {field_name} differs from the explicit project root",
                reason_code="plan.repository_mismatch",
                field=field_name,
            )
    return root


def _validate_state_path(
    root: Path,
    local_state_root: str,
    state_path: str,
) -> tuple[Path, str, str]:
    if not isinstance(local_state_root, str) or not local_state_root.strip():
        raise _reason(
            "local state root must be a nonblank project-relative string",
            reason_code="plan.validation_failed",
            field="local_state_root",
        )
    if not isinstance(state_path, str) or not state_path.strip():
        raise _reason(
            "plan state path must be a nonblank project-relative string",
            reason_code="plan.validation_failed",
            field="state_path",
        )
    local_root = resolve_project_path(
        root,
        local_state_root,
        purpose="local state root",
        reject_install_roots=True,
    )
    local_relative = local_root.relative_to(root).as_posix()
    if local_root.exists() and not local_root.is_dir():
        raise _reason(
            "local state root is not a directory",
            reason_code="plan.validation_failed",
            path=local_relative,
        )
    resolved = resolve_project_path(
        root,
        state_path,
        purpose="plan state path",
        reject_install_roots=True,
    )
    relative = resolved.relative_to(root).as_posix()
    try:
        state_below_local = resolved.relative_to(local_root)
    except ValueError as error:
        raise SecurityError(
            "plan state path is outside the declared local state root",
            details={
                "reason_code": "path.mutable_state_outside_local_root",
                "path": relative,
                "local_state_root": local_relative,
            },
        ) from error
    if state_below_local == Path("."):
        raise _reason(
            "plan state path must name a file below the local state root",
            reason_code="plan.validation_failed",
            path=relative,
        )
    current = root
    parts = Path(relative).parts
    for part in parts[:-1]:
        current = current / part
        if current.exists() and not current.is_dir():
            raise _reason(
                "plan state path has a non-directory parent",
                reason_code="plan.validation_failed",
                path=relative,
            )
    if resolved.exists():
        info = resolved.stat()
        if not stat.S_ISREG(info.st_mode):
            raise _reason(
                "plan state path is not a regular file",
                reason_code="plan.validation_failed",
                path=relative,
            )
        if info.st_nlink != 1:
            raise SecurityError(
                "plan state path has an unsafe hard-link count",
                details={"reason_code": "path.hardlink", "path": relative},
            )
    return resolved, local_relative, relative


def _media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "application/json"
    if suffix in {".yaml", ".yml"}:
        return "application/yaml"
    if suffix in {".md", ".markdown"}:
        return "text/markdown"
    return "text/plain"


def _read_bounded_file(path: Path, relative: str, max_bytes: int) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        if error.errno == errno.ELOOP:
            raise SecurityError(
                "source path resolves through a symbolic link",
                details={"reason_code": "path.symlink", "path": relative},
            ) from error
        raise _reason(
            "source path cannot be opened as a regular file",
            reason_code="plan.validation_failed",
            path=relative,
        ) from error
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise _reason(
                "source path is not a regular file",
                reason_code="plan.validation_failed",
                path=relative,
            )
        if before.st_nlink != 1:
            raise SecurityError(
                "source path has an unsafe hard-link count",
                details={"reason_code": "path.hardlink", "path": relative},
            )
        if before.st_size == 0:
            raise _reason(
                "source path is empty",
                reason_code="plan.validation_failed",
                path=relative,
            )
        if before.st_size > max_bytes:
            raise _reason(
                "source exceeds the explicit byte limit",
                reason_code="plan.validation_failed",
                path=relative,
                size_bytes=before.st_size,
                max_source_bytes=max_bytes,
            )
        chunks: list[bytes] = []
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(descriptor, min(64 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    if len(raw) > max_bytes:
        raise _reason(
            "source exceeded the explicit byte limit while being read",
            reason_code="plan.validation_failed",
            path=relative,
            max_source_bytes=max_bytes,
        )
    before_identity = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    after_identity = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if before_identity != after_identity or after.st_size != len(raw):
        raise SecurityError(
            "source changed while it was being read",
            details={"reason_code": "security.source_changed", "path": relative},
        )
    return raw


def secure_read_plan_source(
    project_root: str | Path,
    request: PlanSourceRequest,
    *,
    max_bytes: int,
    default_precedence: int = 0,
) -> PlanSourceIntake:
    """Read one project-contained UTF-8 source without durable side effects."""

    limit = _validate_positive_integer(max_bytes, field_name="max_source_bytes")
    if not isinstance(request, PlanSourceRequest):
        raise _reason(
            "source request must use the canonical request type",
            reason_code="plan.validation_failed",
        )
    if not isinstance(request.path, str) or not request.path.strip():
        raise _reason(
            "source path must be a nonblank project-relative string",
            reason_code="plan.validation_failed",
        )
    if request.authority not in SOURCE_AUTHORITIES:
        raise _reason(
            "source authority is not recognized",
            reason_code="plan.authority_missing",
            path=request.path,
        )
    precedence = request.precedence
    if precedence is None:
        precedence = default_precedence
    if (
        isinstance(precedence, bool)
        or not isinstance(precedence, int)
        or precedence < 0
    ):
        raise _reason(
            "source precedence must be a non-negative integer",
            reason_code="plan.validation_failed",
            path=request.path,
        )
    path, normalized = resolve_project_relative(
        project_root,
        request.path,
        label="source path",
        allow_directory_rule=False,
    )
    raw = _read_bounded_file(path, normalized.relative, limit)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise _reason(
            "source must be valid UTF-8",
            reason_code="plan.validation_failed",
            path=normalized.relative,
        ) from error
    if contains_secret(text):
        raise SecurityError(
            "source appears to contain a secret",
            details={
                "reason_code": "security.secret_detected",
                "path": normalized.relative,
            },
        )
    return PlanSourceIntake(
        relative_path=normalized.relative,
        source_sha256=hashlib.sha256(raw).hexdigest(),
        size_bytes=len(raw),
        media_type=_media_type(path),
        authority=request.authority,
        precedence=precedence,
        raw_bytes=raw,
        text=text,
    )


def preflight_plan_launcher(
    *,
    project_root: str | Path,
    repository_binding: Mapping[str, Any],
    repository_observation: Mapping[str, Any],
    local_state_root: str,
    state_path: str,
    source_requests: Sequence[PlanSourceRequest],
    guards: PlanLauncherGuards,
    capabilities: Mapping[str, bool],
    provider: ThreadProvider,
) -> PlanLauncherPreflight:
    """Validate one plan launch boundary and perform no state or provider write."""

    _validate_guards(guards)
    provider_id = _validate_capabilities(capabilities, provider)
    root = _validate_repository(
        project_root,
        repository_binding,
        repository_observation,
    )
    state_resolved, local_state_relative, state_relative = _validate_state_path(
        root,
        local_state_root,
        state_path,
    )
    if isinstance(source_requests, (str, bytes)) or not isinstance(
        source_requests,
        Sequence,
    ):
        raise _reason(
            "source requests must be a bounded sequence",
            reason_code="plan.validation_failed",
        )
    requests = tuple(source_requests)
    if not requests:
        raise _reason(
            "plan launch requires at least one source",
            reason_code="plan.authority_missing",
        )
    if len(requests) > guards.max_sources:
        raise _reason(
            "source count exceeds the explicit launch guard",
            reason_code="plan.validation_failed",
            source_count=len(requests),
            max_sources=guards.max_sources,
        )
    if any(not isinstance(request, PlanSourceRequest) for request in requests):
        raise _reason(
            "source requests must use the canonical request type",
            reason_code="plan.validation_failed",
        )
    if not any(request.authority == "accepted" for request in requests):
        raise _reason(
            "plan launch requires at least one explicitly accepted source",
            reason_code="plan.authority_missing",
        )
    if len(requests) > 1 and any(request.precedence is None for request in requests):
        raise _reason(
            "multi-source launch requires explicit precedence for every source",
            reason_code="plan.validation_failed",
        )

    source_aliases: set[str] = set()
    state_alias = state_relative.casefold()
    sources: list[PlanSourceIntake] = []
    total_bytes = 0
    for request in requests:
        intake = secure_read_plan_source(
            root,
            request,
            max_bytes=guards.max_source_bytes,
        )
        alias = intake.relative_path.casefold()
        if alias == state_alias:
            raise SecurityError(
                "plan state path cannot also be a source",
                details={
                    "reason_code": "security.blocked",
                    "path": intake.relative_path,
                },
            )
        if alias in source_aliases:
            raise SecurityError(
                "source paths contain a portable alias",
                details={
                    "reason_code": "path.alias",
                    "path": intake.relative_path,
                },
            )
        source_aliases.add(alias)
        total_bytes += intake.size_bytes
        if total_bytes > guards.max_total_source_bytes:
            raise _reason(
                "aggregate source bytes exceed the explicit launch guard",
                reason_code="plan.validation_failed",
                source_total_bytes=total_bytes,
                max_total_source_bytes=guards.max_total_source_bytes,
            )
        sources.append(intake)

    return PlanLauncherPreflight(
        project_root=str(root),
        local_state_root=local_state_relative,
        state_path=state_resolved.relative_to(root).as_posix(),
        provider_id=provider_id,
        sources=tuple(sources),
        repository_binding=copy.deepcopy(dict(repository_binding)),
    )


def reserve_first_plan_task(
    store: SQLitePlanStore,
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_outer_revision: int,
    current_outer_holder_token: str | None,
    predecessor_thread_id: str | None,
    handoff_token: str | None = None,
    expires_at: str | None = None,
    timestamp: str | None = None,
) -> PlanTaskReservationResult:
    """Reserve one dependency-ready task and prepare its token-bound handoff."""

    if not isinstance(store, SQLitePlanStore):
        raise _reason(
            "first-task reservation requires the canonical SQLite plan store",
            reason_code="plan.validation_failed",
        )
    _validate_positive_integer(
        expected_plan_revision,
        field_name="expected_plan_revision",
    )
    _validate_positive_integer(
        expected_outer_revision,
        field_name="expected_outer_revision",
    )
    if (
        not isinstance(plan_id, str)
        or not plan_id.strip()
        or (
            current_outer_holder_token is not None
            and (
                not isinstance(current_outer_holder_token, str)
                or not current_outer_holder_token
            )
        )
    ):
        raise _reason(
            "plan and outer-holder identity must be nonblank",
            reason_code="plan.validation_failed",
        )
    now = timestamp or utc_now()
    record = store.load_plan(plan_id)
    state = record["state"]
    if state["revision"] != expected_plan_revision:
        raise StateConflict(
            "first-task reservation expected revision is stale",
            details={
                "expected_revision": expected_plan_revision,
                "actual_revision": state["revision"],
            },
        )
    if (
        state["phase"] not in {"initialized", "continuation_required"}
        or state["active_task_id"] is not None
        or state["lease"] is not None
    ):
        raise StateConflict(
            "task reservation requires a safe coordinator boundary"
        )
    selection = store.select_next_task(
        plan_id,
        expected_revision=expected_plan_revision,
    )
    if selection.status != "selected" or selection.selected_task is None:
        raise StateConflict(
            "plan does not have one dependency-ready task",
            details={
                "reason_code": selection.reason_code,
                "selection_status": selection.status,
            },
        )
    selected_task_id = str(selection.selected_task["task_id"])
    canonical_definition = store.load_task_definition(
        plan_id,
        selected_task_id,
    )
    task_definition = copy.deepcopy(
        dict(canonical_definition["task_json"])
    )
    if (
        task_definition.get("task_id") != selected_task_id
        or task_definition.get("task_sha256")
        != selection.selected_task["task_sha256"]
    ):
        raise IntegrityError(
            "selected task definition differs from canonical storage"
        )
    generation = int(state["current_generation"]) + 1
    effective_handoff_token = handoff_token or secrets.token_hex(24)
    envelope_schema_path = store.schema_root / (
        "plan-task-envelope-v2.schema.json"
        if record.get("runtime_profile_version") == 2
        else "plan-task-envelope.schema.json"
    )
    envelope = build_plan_task_envelope(
        record,
        selection_proof=selection.proof,
        task_definition=task_definition,
        generation=generation,
        handoff_token=effective_handoff_token,
        predecessor_thread_id=predecessor_thread_id,
        schema_path=envelope_schema_path,
    )
    build_plan_task_dependency_proof(
        selection.proof,
        task_definition,
    )
    expected_worker_revision = (
        expected_plan_revision + FIRST_TASK_CLAIM_REVISION_ADVANCE
    )
    worker_prompt = build_plan_task_worker_prompt(
        envelope,
        task_definition=task_definition,
        selection_proof=selection.proof,
        expected_revision=expected_worker_revision,
        schema_path=envelope_schema_path,
    )
    effective_expiry = expires_at or add_seconds(
        now,
        DEFAULT_LEASE_SECONDS,
    )
    with store.mutation(
        plan_id,
        expected_revision=expected_plan_revision,
        timestamp=now,
    ) as mutation:
        proof_sha256 = mutation.reserve_selected_task(
            selection.proof,
            generation=generation,
            successor_created=False,
            expected_outer_revision=expected_outer_revision,
            holder_kind="successor_reserved",
            holder_token=effective_handoff_token,
            expires_at=effective_expiry,
            current_outer_holder_token=current_outer_holder_token,
        )

    updated = store.load_plan(plan_id)
    outer = store.goal_store.load_goal(updated["outer_goal_id"])
    persisted_proof = store.selection_proof_for_revision(
        plan_id,
        expected_plan_revision,
    )
    task_state = next(
        item
        for item in updated["state"]["tasks"]
        if item["task_id"] == selected_task_id
    )
    plan_lease = updated["state"]["lease"]
    outer_lease = outer["state"].get("active_lease")
    if (
        updated["state"]["revision"] != expected_plan_revision + 1
        or outer["state"]["revision"] != expected_outer_revision + 1
        or updated["state"]["phase"] != "task_reserved"
        or updated["state"]["active_task_id"] != selected_task_id
        or task_state["status"] != "reserved"
        or task_state["generation"] != generation
        or not isinstance(plan_lease, Mapping)
        or plan_lease["holder_kind"] != "successor_reserved"
        or plan_lease["holder_token_hash"]
        != holder_token_sha256(effective_handoff_token)
        or not isinstance(outer_lease, Mapping)
        or outer_lease["holder_kind"] != "successor_reserved"
        or outer_lease["holder_token"] != effective_handoff_token
        or persisted_proof != selection.proof
        or content_sha256(persisted_proof) != proof_sha256
    ):
        raise IntegrityError(
            "first-task reservation does not match its canonical handoff"
        )
    return PlanTaskReservationResult(
        plan_record=copy.deepcopy(updated),
        outer_goal_record=copy.deepcopy(outer),
        selection_proof=copy.deepcopy(selection.proof),
        task_definition=copy.deepcopy(task_definition),
        envelope=copy.deepcopy(envelope),
        worker_prompt=worker_prompt,
        envelope_schema_path=envelope_schema_path,
        expected_worker_revision=expected_worker_revision,
        selection_proof_sha256=proof_sha256,
    )


def reserve_next_plan_task(
    store: SQLitePlanStore,
    *,
    plan_id: str,
    expected_plan_revision: int,
    expected_outer_revision: int,
    current_outer_holder_token: str | None,
    predecessor_thread_id: str | None,
    handoff_token: str | None = None,
    expires_at: str | None = None,
    timestamp: str | None = None,
) -> PlanTaskReservationResult:
    """Central successor path for first and all later plan-task workers."""

    return reserve_first_plan_task(
        store,
        plan_id=plan_id,
        expected_plan_revision=expected_plan_revision,
        expected_outer_revision=expected_outer_revision,
        current_outer_holder_token=current_outer_holder_token,
        predecessor_thread_id=predecessor_thread_id,
        handoff_token=handoff_token,
        expires_at=expires_at,
        timestamp=timestamp,
    )


def _valid_provider_identity(value: Any) -> bool:
    allowed = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789._:-"
    )
    return (
        isinstance(value, str)
        and 3 <= len(value) <= 160
        and value[0] in allowed[:62]
        and all(char in allowed for char in value)
    )


def _rehash_provider_intent(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop("intent_content_sha256", None)
    result["intent_content_sha256"] = content_sha256(result)
    return result


def _provider_response_digest(
    result: ThreadCreateResult,
) -> str:
    try:
        projection = {
            "status": result.status,
            "successor_thread_id": result.successor_thread_id,
            "response": copy.deepcopy(dict(result.response)),
        }
        return content_sha256(projection)
    except (TypeError, ValueError, RecursionError):
        return content_sha256(
            {
                "status": "unserializable_provider_response",
                "result_type": type(result.response).__name__,
            }
        )


def _provider_intent(
    reservation: PlanTaskReservationResult,
    *,
    provider_id: str,
    timestamp: str,
) -> dict[str, Any]:
    plan = reservation.plan_record
    state = plan["state"]
    envelope = reservation.envelope
    identity_sha256 = content_sha256(
        {
            "plan_id": plan["plan_id"],
            "task_id": envelope["task_id"],
            "generation": envelope["generation"],
            "provider_id": provider_id,
            "idempotency_key": envelope["idempotency_key"],
        }
    )
    profile_aware = (
        envelope.get("schema_version") == "sys4ai.plan-task-envelope.v2"
    )
    intent: dict[str, Any] = {
            "schema_version": (
                "sys4ai.plan-provider-intent.v2"
                if profile_aware
                else "sys4ai.plan-provider-intent.v1"
            ),
            "intent_id": f"PPI-{identity_sha256[:32]}",
            "plan_id": plan["plan_id"],
            "plan_sha256": plan["effective_plan_sha256"],
            "task_id": envelope["task_id"],
            "task_sha256": envelope["task_sha256"],
            "generation": envelope["generation"],
            "provider_id": provider_id,
            "idempotency_key": envelope["idempotency_key"],
            "handoff_token_sha256": holder_token_sha256(
                str(envelope["handoff_token"])
            ),
            "predecessor_thread_id": envelope["predecessor_thread_id"],
            "expected_revision": state["revision"],
            "repository_fingerprint": state["repository_fingerprint"],
            "created_at": timestamp,
            "status": "intent",
            "provider_create_budget": 1,
            "create_attempts": 0,
            "returned_thread_id": None,
            "provider_response_sha256": None,
            "conflicting_thread_ids": [],
            "retry_authorized": False,
            "recovery": {
                "status": "not_required",
                "reason": None,
                "evidence_refs": [],
            },
            "prior_journal_sha256": plan["journal"][-1]["event_hash"],
            "hash_basis": (
                "canonical_json_without_intent_content_sha256"
            ),
            "finalized": False,
            "extensions": {},
        }
    if profile_aware:
        profile = envelope["execution_profile"]
        intent.update(
            {
                "execution_profile_sha256": content_sha256(profile),
                "requested_reasoning_effort": profile[
                    "reasoning_effort"
                ],
                "effective_reasoning_effort": None,
                "profile_verification_status": "not_verified",
                "profile_evidence_ref": None,
                "environment_mode": "reuse_bound_checkout",
                "repository_binding_sha256": envelope[
                    "repository_binding_sha256"
                ],
                "observed_topology_sha256": None,
                "same_thread_profile_repair": {
                    "attempted": False,
                    "thread_id": None,
                    "evidence_ref": None,
                },
            }
        )
    return _rehash_provider_intent(intent)


def _validate_dispatch_reservation(
    store: SQLitePlanStore,
    reservation: PlanTaskReservationResult,
    provider: ThreadProvider,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str]:
    if not isinstance(store, SQLitePlanStore) or not isinstance(
        reservation,
        PlanTaskReservationResult,
    ):
        raise _reason(
            "plan dispatch requires canonical store and reservation types",
            reason_code="plan.validation_failed",
        )
    provider_id = getattr(provider, "provider_id", None)
    if (
        getattr(provider, "available", False) is not True
        or not _valid_provider_identity(provider_id)
    ):
        raise _reason(
            "selected ThreadProvider is unavailable or invalid",
            reason_code="plan_task.capability_missing",
            missing=["thread_provider"],
        )
    current_profile = reservation.plan_record.get("execution_profile")
    if isinstance(current_profile, Mapping):
        capabilities = (
            provider.capabilities()
            if callable(getattr(provider, "capabilities", None))
            else {}
        )
        required = {
            "can_create_with_reasoning_effort",
            "can_verify_effective_reasoning_effort",
            "can_reuse_bound_checkout",
        }
        missing = sorted(
            item for item in required if capabilities.get(item) is not True
        )
        supported = {
            str(item)
            for item in capabilities.get("supported_reasoning_efforts", ())
        }
        accepted = str(current_profile["reasoning_effort"])
        if missing:
            raise _reason(
                "ThreadProvider cannot preserve the accepted plan profile",
                reason_code="plan_task.profile_capability_missing",
                missing=missing,
            )
        if supported and accepted not in supported:
            raise _reason(
                "ThreadProvider does not support the accepted plan effort",
                reason_code="plan_task.reasoning_effort_unsupported",
                accepted=accepted,
                supported=sorted(supported),
            )
    plan_id = str(reservation.plan_record["plan_id"])
    current = store.load_plan(plan_id)
    outer = store.goal_store.load_goal(current["outer_goal_id"])
    if current != reservation.plan_record or outer != reservation.outer_goal_record:
        raise StateConflict(
            "plan dispatch reservation is stale or no longer canonical"
        )
    if store.integrity_check()["status"] != "pass":
        raise IntegrityError("plan dispatch store failed integrity preflight")
    state = current["state"]
    envelope = reservation.envelope
    task_id = str(envelope["task_id"])
    try:
        task = next(
            item
            for item in state["tasks"]
            if item["task_id"] == task_id
        )
    except StopIteration as error:
        raise IntegrityError(
            "reserved task is absent from canonical plan state"
        ) from error
    plan_lease = state.get("lease")
    outer_lease = outer["state"].get("active_lease")
    handoff_token = str(envelope["handoff_token"])
    expected_prompt = build_plan_task_worker_prompt(
        envelope,
        task_definition=reservation.task_definition,
        selection_proof=reservation.selection_proof,
        expected_revision=reservation.expected_worker_revision,
        schema_path=reservation.envelope_schema_path,
    )
    if (
        state["phase"] != "task_reserved"
        or state["active_task_id"] != task_id
        or task["status"] != "reserved"
        or task["generation"] != envelope["generation"]
        or task["task_sha256"] != envelope["task_sha256"]
        or task["counters"]["provider_creates"] != 0
        or task["counters"]["successor_creates"] != 0
        or envelope["plan_id"] != current["plan_id"]
        or envelope["plan_sha256"] != current["effective_plan_sha256"]
        or envelope["repository_binding"]
        != {
            key: current["repository_binding"][key]
            for key in envelope["repository_binding"]
        }
        or envelope["idempotency_key"]
        != f"{current['plan_id']}:{envelope['generation']}"
        or content_sha256(reservation.task_definition)
        != reservation.as_dict()["task_definition_sha256"]
        or content_sha256(reservation.selection_proof)
        != reservation.selection_proof_sha256
        or reservation.expected_worker_revision != state["revision"] + 2
        or expected_prompt != reservation.worker_prompt
        or not isinstance(plan_lease, Mapping)
        or plan_lease["holder_kind"] != "successor_reserved"
        or plan_lease["holder_token_hash"]
        != holder_token_sha256(handoff_token)
        or not isinstance(outer_lease, Mapping)
        or outer_lease["holder_kind"] != "successor_reserved"
        or outer_lease["holder_token"] != handoff_token
        or store.find_provider_intent(
            current["plan_id"],
            int(envelope["generation"]),
        )
        is not None
    ):
        raise StateConflict(
            "plan dispatch reservation identity or create budget differs"
        )
    return current, outer, task, str(provider_id)


def _validate_plan_created_profile(
    result: ThreadCreateResult,
    *,
    reservation: PlanTaskReservationResult,
    provider: ThreadProvider,
) -> ThreadCreateResult:
    """Verify or repair only the same unclaimed profile-aware successor."""

    envelope = reservation.envelope
    if envelope.get("schema_version") != "sys4ai.plan-task-envelope.v2":
        return result
    response = copy.deepcopy(dict(result.response))
    requested = str(envelope["execution_profile"]["reasoning_effort"])
    binding_hash = str(envelope["repository_binding_sha256"])
    base_matches = (
        response.get("requested_reasoning_effort") == requested
        and response.get("environment_mode") == "reuse_bound_checkout"
        and response.get("repository_binding_sha256") == binding_hash
    )
    if result.status == "manual_pending":
        if base_matches:
            return result
        return ThreadCreateResult(
            "ambiguous",
            None,
            {"reason_code": "provider.manual_profile_evidence_missing"},
        )
    if result.status != "returned":
        return result
    topology = response.get("repository_topology")
    binding = reservation.plan_record["repository_binding"]
    topology_matches = (
        isinstance(topology, Mapping)
        and topology.get("branch") == binding.get("branch")
        and topology.get("worktree") == binding.get("worktree")
        and all(
            topology.get(field) == binding.get(field)
            for field in ("root", "git_common_dir")
            if field in topology
        )
    )
    effective_matches = (
        response.get("effective_reasoning_effort") == requested
    )
    repair_record: dict[str, Any] = {
        "attempted": False,
        "thread_id": None,
        "evidence_ref": None,
    }
    if base_matches and topology_matches and not effective_matches:
        capabilities = (
            provider.capabilities()
            if callable(getattr(provider, "capabilities", None))
            else {}
        )
        repair = getattr(provider, "reconfigure_unclaimed_successor", None)
        read_profile = getattr(provider, "read_thread_profile", None)
        if (
            result.successor_thread_id
            and capabilities.get("can_reconfigure_unclaimed_successor")
            is True
            and callable(repair)
            and callable(read_profile)
        ):
            thread_id = str(result.successor_thread_id)
            repair_evidence = repair(
                thread_id,
                reasoning_effort=requested,
            )
            observed = read_profile(thread_id)
            repair_ref = (
                observed.get("evidence_ref")
                if isinstance(observed, Mapping)
                else None
            ) or (
                repair_evidence.get("evidence_ref")
                if isinstance(repair_evidence, Mapping)
                else None
            )
            repair_record = {
                "attempted": True,
                "thread_id": thread_id,
                "evidence_ref": str(
                    repair_ref
                    or (
                        "provider-repair:"
                        + content_sha256(
                            {
                                "thread_id": thread_id,
                                "effort": requested,
                            }
                        )
                    )
                ),
            }
            if (
                isinstance(observed, Mapping)
                and observed.get("reasoning_effort") == requested
            ):
                response["effective_reasoning_effort"] = requested
                response["profile_evidence_ref"] = repair_record[
                    "evidence_ref"
                ]
                response["same_thread_profile_repair"] = repair_record
                effective_matches = True
    if not (base_matches and topology_matches and effective_matches):
        return ThreadCreateResult(
            "ambiguous",
            result.successor_thread_id,
            {
                "reason_code": "provider.created_profile_unverified",
                "candidate_thread_id": result.successor_thread_id,
                "same_thread_profile_repair": repair_record,
            },
        )
    response.setdefault(
        "profile_evidence_ref",
        f"provider-response:{_provider_response_digest(result)}",
    )
    response.setdefault("same_thread_profile_repair", repair_record)
    response["observed_topology_sha256"] = content_sha256(dict(topology))
    return ThreadCreateResult(
        "returned",
        result.successor_thread_id,
        response,
    )


def _conflicting_thread_ids(
    result: ThreadCreateResult,
    *,
    predecessor_thread_id: str | None,
) -> list[str]:
    values: list[Any] = []
    if result.successor_thread_id is not None:
        values.append(result.successor_thread_id)
    raw = result.response.get("conflicting_thread_ids")
    if isinstance(raw, Sequence) and not isinstance(
        raw,
        (str, bytes, bytearray),
    ):
        values.extend(raw)
    return sorted(
        {
            value
            for value in values
            if _valid_provider_identity(value)
            and value != predecessor_thread_id
        }
    )


def _final_provider_intent(
    intent: Mapping[str, Any],
    result: ThreadCreateResult,
) -> tuple[dict[str, Any], str]:
    outcome = copy.deepcopy(dict(intent))
    response_sha256 = _provider_response_digest(result)
    predecessor = outcome["predecessor_thread_id"]
    returned_thread_id: str | None = None
    conflicts: list[str] = []
    recovery_reason: str | None = None
    if result.status == "returned":
        if (
            _valid_provider_identity(result.successor_thread_id)
            and result.successor_thread_id != predecessor
        ):
            status = "returned"
            returned_thread_id = result.successor_thread_id
        else:
            status = "ambiguous"
            recovery_reason = (
                "Provider did not prove one distinct fresh successor."
            )
    elif result.status == "definitive_failure":
        status = "failed"
    elif result.status == "duplicate":
        conflicts = _conflicting_thread_ids(
            result,
            predecessor_thread_id=predecessor,
        )
        if len(conflicts) >= 2:
            status = "duplicate"
            recovery_reason = (
                "Provider reported multiple conflicting successors."
            )
        else:
            status = "ambiguous"
            conflicts = []
            recovery_reason = (
                "Provider duplicate result lacked two distinct identities."
            )
    else:
        status = result.status
        recovery_reason = (
            f"Provider outcome requires protected recovery: {status}."
        )
    outcome.update(
        {
            "status": status,
            "create_attempts": 1,
            "returned_thread_id": returned_thread_id,
            "provider_response_sha256": response_sha256,
            "conflicting_thread_ids": conflicts,
            "recovery": {
                "status": (
                    "required"
                    if status in {"ambiguous", "timeout", "duplicate"}
                    else "not_required"
                ),
                "reason": recovery_reason,
                "evidence_refs": [],
            },
            "finalized": True,
        }
    )
    if outcome["schema_version"] == "sys4ai.plan-provider-intent.v2":
        response = dict(result.response)
        if status == "returned":
            outcome.update(
                {
                    "effective_reasoning_effort": response[
                        "effective_reasoning_effort"
                    ],
                    "profile_verification_status": "verified",
                    "profile_evidence_ref": response[
                        "profile_evidence_ref"
                    ],
                    "observed_topology_sha256": response[
                        "observed_topology_sha256"
                    ],
                    "same_thread_profile_repair": copy.deepcopy(
                        response["same_thread_profile_repair"]
                    ),
                }
            )
        else:
            repair = response.get("same_thread_profile_repair")
            outcome.update(
                {
                    "effective_reasoning_effort": None,
                    "profile_verification_status": (
                        "mismatch"
                        if response.get("reason_code")
                        == "provider.created_profile_unverified"
                        else "unavailable"
                    ),
                    "profile_evidence_ref": None,
                    "observed_topology_sha256": None,
                    "same_thread_profile_repair": copy.deepcopy(
                        repair
                        if isinstance(repair, Mapping)
                        else {
                            "attempted": False,
                            "thread_id": None,
                            "evidence_ref": None,
                        }
                    ),
                }
            )
    return _rehash_provider_intent(outcome), response_sha256


def dispatch_reserved_plan_task(
    store: SQLitePlanStore,
    *,
    reservation: PlanTaskReservationResult,
    provider: ThreadProvider,
    timestamp: str | None = None,
    expires_at: str | None = None,
    quarantine_token: str | None = None,
) -> PlanTaskDispatchResult:
    """Persist one intent, call one provider once, and record its outcome."""

    if quarantine_token is not None and (
        not isinstance(quarantine_token, str)
        or len(quarantine_token) < 32
    ):
        raise RecordValidationError(
            "plan quarantine token must contain at least 32 characters"
        )
    now = timestamp or utc_now()
    parse_utc(now)
    if expires_at is not None and parse_utc(expires_at) <= parse_utc(now):
        raise RecordValidationError(
            "plan dispatch lease expiry must be later than its timestamp"
        )
    plan, outer, _, provider_id = _validate_dispatch_reservation(
        store,
        reservation,
        provider,
    )
    intent = _provider_intent(
        reservation,
        provider_id=provider_id,
        timestamp=now,
    )
    plan_revision = int(plan["state"]["revision"])
    outer_revision = int(outer["state"]["revision"])
    with store.mutation(
        plan["plan_id"],
        expected_revision=plan_revision,
        timestamp=now,
    ) as mutation:
        intent_sha256 = mutation.add_provider_intent(intent)

    try:
        raw_result = provider.create_thread(
            prompt=reservation.worker_prompt,
            envelope=reservation.envelope,
            idempotency_key=str(
                reservation.envelope["idempotency_key"]
            ),
            execution_profile=copy.deepcopy(
                dict(
                    reservation.plan_record.get(
                        "execution_profile",
                        {},
                    )
                )
            ),
        )
        if not isinstance(raw_result, ThreadCreateResult):
            raw_result = ThreadCreateResult(
                "ambiguous",
                None,
                {
                    "status": "invalid_provider_result",
                    "result_type": type(raw_result).__name__,
                },
            )
        elif not isinstance(raw_result.response, Mapping):
            raw_result = ThreadCreateResult(
                "ambiguous",
                None,
                {
                    "status": "invalid_provider_response",
                    "response_type": type(raw_result.response).__name__,
                },
            )
    except Exception as error:
        raw_result = ThreadCreateResult(
            "ambiguous",
            None,
            {
                "status": "provider_exception",
                "exception_type": (
                    f"{type(error).__module__}.{type(error).__qualname__}"
                ),
            },
        )

    try:
        raw_result = _validate_plan_created_profile(
            raw_result,
            reservation=reservation,
            provider=provider,
        )
    except Exception as error:
        response = (
            copy.deepcopy(dict(raw_result.response))
            if isinstance(raw_result.response, Mapping)
            else {}
        )
        repair_attempted = (
            raw_result.status == "returned"
            and raw_result.successor_thread_id is not None
        )
        exception_type = (
            f"{type(error).__module__}.{type(error).__qualname__}"
        )
        response.update(
            {
                "status": "provider_profile_verification_exception",
                "reason_code": "provider.profile_verification_exception",
                "exception_type": exception_type,
                "same_thread_profile_repair": {
                    "attempted": repair_attempted,
                    "thread_id": (
                        raw_result.successor_thread_id
                        if repair_attempted
                        else None
                    ),
                    "evidence_ref": (
                        "provider-repair-verification-exception:"
                        + content_sha256(
                            {
                                "thread_id": raw_result.successor_thread_id,
                                "exception_type": exception_type,
                            }
                        )
                        if repair_attempted
                        else None
                    ),
                },
            }
        )
        raw_result = ThreadCreateResult(
            "ambiguous",
            raw_result.successor_thread_id,
            response,
        )
    response_sha256 = _provider_response_digest(raw_result)
    provider_response = raw_result.response
    if raw_result.status == "manual_pending":
        updated = store.load_plan(plan["plan_id"])
        updated_outer = store.goal_store.load_goal(
            updated["outer_goal_id"]
        )
        persisted = store.load_provider_intent(intent["intent_id"])
        manual_path = raw_result.response.get("receipt_path")
        if not isinstance(manual_path, str):
            manual_path = None
        if (
            updated["state"]["revision"] != plan_revision + 1
            or updated_outer != outer
            or persisted != intent
            or updated["state"]["lease"]["holder_kind"]
            != "successor_reserved"
            or store.integrity_check()["status"] != "pass"
        ):
            raise IntegrityError(
                "manual plan handoff differs from its open provider intent"
            )
        return PlanTaskDispatchResult(
            status="manual_handoff_pending",
            plan_id=plan["plan_id"],
            task_id=str(reservation.envelope["task_id"]),
            generation=int(reservation.envelope["generation"]),
            provider_id=provider_id,
            intent_id=intent["intent_id"],
            intent_sha256=intent_sha256,
            provider_response_sha256=response_sha256,
            plan_revision=updated["state"]["revision"],
            outer_goal_revision=updated_outer["state"]["revision"],
            successor_thread_id=None,
            manual_handoff_path=manual_path,
            lease_holder_kind="successor_reserved",
            recovery_required=False,
            state_writes=1,
            next_boundary="manual_adoption",
            plan_record=copy.deepcopy(updated),
            outer_goal_record=copy.deepcopy(updated_outer),
            provider_intent=copy.deepcopy(persisted),
            provider_response=provider_response,
        )

    outcome, response_sha256 = _final_provider_intent(
        intent,
        raw_result,
    )
    returned = outcome["status"] == "returned"
    handoff_token = str(reservation.envelope["handoff_token"])
    effective_holder_token = handoff_token
    holder_kind = "successor_reserved"
    if not returned:
        effective_holder_token = quarantine_token or secrets.token_hex(24)
        holder_kind = "quarantined"
    effective_expiry = expires_at or add_seconds(
        now,
        DEFAULT_LEASE_SECONDS,
    )
    with store.mutation(
        plan["plan_id"],
        expected_revision=plan_revision + 1,
        timestamp=now,
    ) as mutation:
        intent_sha256 = mutation.finalize_provider_intent(outcome)
        mutation.record_provider_dispatch(
            task_id=str(reservation.envelope["task_id"]),
            generation=int(reservation.envelope["generation"]),
            provider_status=str(outcome["status"]),
            successor_created=returned,
        )
        mutation.transfer_plan_lease(
            expected_outer_revision=outer_revision,
            current_holder_token=handoff_token,
            holder_kind=holder_kind,
            holder_token=effective_holder_token,
            expires_at=effective_expiry,
        )

    updated = store.load_plan(plan["plan_id"])
    updated_outer = store.goal_store.load_goal(updated["outer_goal_id"])
    persisted = store.load_provider_intent(intent["intent_id"])
    task = next(
        item
        for item in updated["state"]["tasks"]
        if item["task_id"] == reservation.envelope["task_id"]
    )
    outer_lease = updated_outer["state"].get("active_lease")
    if (
        updated["state"]["revision"] != plan_revision + 2
        or updated_outer["state"]["revision"] != outer_revision + 1
        or persisted != outcome
        or task["counters"]["provider_creates"] != 1
        or task["counters"]["successor_creates"] != int(returned)
        or updated["state"]["lease"]["holder_kind"] != holder_kind
        or not isinstance(outer_lease, Mapping)
        or outer_lease["holder_kind"]
        != (
            "successor_reserved"
            if returned
            else "quarantined"
        )
        or outer_lease["holder_token"] != effective_holder_token
        or (
            not returned
            and updated_outer["state"]["phase"] != "recovery_pending"
        )
        or store.integrity_check()["status"] != "pass"
    ):
        raise IntegrityError(
            "plan provider outcome differs from canonical dispatch evidence"
        )
    public_status = {
        "returned": "dispatched",
        "failed": "dispatch_failed",
        "ambiguous": "ambiguous",
        "timeout": "timeout",
        "duplicate": "duplicate",
    }[str(outcome["status"])]
    return PlanTaskDispatchResult(
        status=public_status,
        plan_id=plan["plan_id"],
        task_id=str(reservation.envelope["task_id"]),
        generation=int(reservation.envelope["generation"]),
        provider_id=provider_id,
        intent_id=intent["intent_id"],
        intent_sha256=intent_sha256,
        provider_response_sha256=response_sha256,
        plan_revision=updated["state"]["revision"],
        outer_goal_revision=updated_outer["state"]["revision"],
        successor_thread_id=outcome["returned_thread_id"],
        manual_handoff_path=None,
        lease_holder_kind=holder_kind,
        recovery_required=not returned,
        state_writes=2,
        next_boundary=(
            "worker_claim" if returned else "protected_recovery"
        ),
        plan_record=copy.deepcopy(updated),
        outer_goal_record=copy.deepcopy(updated_outer),
        provider_intent=copy.deepcopy(persisted),
        provider_response=provider_response,
    )
