"""Goal launcher orchestration with one first-generation dispatch."""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol

from agentjob_runtime.errors import RecordValidationError, SecurityError
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import (
    record_dispatch_outcome,
    record_successor,
    reserve_successor,
)
from agentjob_runtime.records.canonical import content_sha256, render_canonical_json
from agentjob_runtime.validation.schema import format_issues, validate_instance


REQUIRED_CAPABILITIES = frozenset(
    {
        "agentjob_control",
        "goal_state",
        "continuation_envelope",
        "repository_provider",
        "thread_provider",
    }
)
PROVIDER_STATUSES = frozenset(
    {
        "returned",
        "manual_pending",
        "definitive_failure",
        "ambiguous",
        "timeout",
        "duplicate",
    }
)


@dataclass(frozen=True)
class ThreadCreateResult:
    status: str
    successor_thread_id: str | None
    response: Mapping[str, Any]

    def __post_init__(self) -> None:
        if self.status not in PROVIDER_STATUSES:
            raise RecordValidationError(f"unsupported ThreadProvider status: {self.status}")
        if self.status == "returned" and not self.successor_thread_id:
            raise RecordValidationError("returned ThreadProvider result requires a thread ID")


class ThreadProvider(Protocol):
    provider_id: str
    available: bool

    def create_thread(
        self,
        *,
        prompt: str,
        envelope: Mapping[str, Any],
        idempotency_key: str,
    ) -> ThreadCreateResult: ...


@dataclass(frozen=True)
class LauncherSummary:
    status: str
    goal_id: str
    generation: int
    envelope_sha256: str
    provider_id: str
    provider_create_calls: int
    successor_thread_id: str | None
    manual_handoff_path: str | None
    state_phase: str
    state_revision: int
    lease_holder_kind: str | None
    agentjobs_executed: int = 0
    continue_invocations: int = 0

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_preflight(
    *,
    store: SQLiteGoalStore,
    repository_binding: Mapping[str, Any],
    repository_observation: Mapping[str, Any],
    capabilities: Mapping[str, bool],
    provider: ThreadProvider,
) -> None:
    missing = sorted(
        capability
        for capability in REQUIRED_CAPABILITIES
        if capabilities.get(capability) is not True
    )
    if missing:
        raise RecordValidationError(
            "goal launcher capabilities are incomplete",
            details={"reason_code": "launcher.capability_missing", "missing": missing},
        )
    if provider.available is not True or not str(provider.provider_id).strip():
        raise RecordValidationError(
            "selected ThreadProvider is unavailable",
            details={"reason_code": "launcher.thread_provider_unavailable"},
        )
    for key in (
        "project_id",
        "root",
        "worktree",
        "branch",
        "git_common_dir",
        "starting_revision",
        "environment_mode",
    ):
        if repository_observation.get(key) != repository_binding.get(key):
            raise RecordValidationError(
                f"repository observation differs from requested binding at {key}",
                details={"reason_code": "launcher.repository_mismatch", "field": key},
            )
    root = Path(str(repository_binding["root"])).expanduser().resolve()
    worktree = Path(str(repository_binding["worktree"])).expanduser().resolve()
    if not root.is_dir() or not worktree.is_dir():
        raise RecordValidationError("repository root and worktree must exist")
    try:
        store.path.relative_to(root)
    except ValueError as error:
        raise SecurityError(
            "goal state database must remain inside the bound project root",
            details={"reason_code": "launcher.state_outside_project"},
        ) from error
    integrity = store.integrity_check()
    if integrity["status"] != "pass":
        raise RecordValidationError(
            "goal state backend failed integrity preflight",
            details={"reason_code": "launcher.state_integrity_failed", "integrity": integrity},
        )


def build_continuation_envelope(
    record: Mapping[str, Any],
    *,
    predecessor_thread_id: str | None,
    predecessor_handoff_id: str | None,
    canonical_state: Mapping[str, Any],
    progress_summary: str,
    remaining_work: str,
) -> dict[str, Any]:
    generation = int(record["state"]["current_generation"])
    entry = record["generations"][str(generation)]
    envelope = {
        "schema_version": "sys4ai.continuation-envelope.v1",
        "goal_id": record["goal_id"],
        "goal_sha256": record["goal_sha256"],
        "completion_contract_sha256": record["completion_contract_sha256"],
        "generation": generation,
        "handoff_token": entry["handoff_token"],
        "idempotency_key": entry["idempotency_key"],
        "predecessor_thread_id": predecessor_thread_id,
        "predecessor_handoff_id": predecessor_handoff_id,
        "repository_binding": copy.deepcopy(record["repository_binding"]),
        "canonical_state": {
            "fingerprint": canonical_state.get(
                "fingerprint", record["state"]["last_canonical_fingerprint"]
            ),
            "active_task_id": canonical_state.get("active_task_id"),
            "current_decision_id": canonical_state.get("current_decision_id"),
            "current_job_id": canonical_state.get("current_job_id"),
        },
        "progress_summary": progress_summary,
        "remaining_work": remaining_work,
        "required_skill": "continue-implementing-goal",
        "extensions": {},
    }
    schema = Path(__file__).resolve().parents[3] / "schemas" / "continuation-envelope.schema.json"
    issues = validate_instance(envelope, schema)
    if issues:
        raise RecordValidationError(
            "continuation envelope failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    return envelope


def build_worker_prompt(
    envelope: Mapping[str, Any],
    *,
    project_root: str,
    expected_revision: int,
) -> str:
    envelope_hash = content_sha256(envelope)
    return (
        "Invoke the installed continue-implementing-goal skill in normal mode.\n"
        "Wait for the predecessor to record this successor before claiming the generation.\n"
        f"project_root: {project_root}\n"
        f"expected_revision: {expected_revision}\n"
        f"envelope_sha256: {envelope_hash}\n"
        "continuation_envelope:\n"
        + render_canonical_json(envelope)
    )


def launch_goal(
    store: SQLiteGoalStore,
    *,
    goal_text: str,
    completion_contract: Mapping[str, Any],
    guards: Mapping[str, Any],
    repository_binding: Mapping[str, Any],
    repository_observation: Mapping[str, Any],
    initial_fingerprint: str,
    authorization: Mapping[str, Any],
    capabilities: Mapping[str, bool],
    provider: ThreadProvider,
    predecessor_thread_id: str | None,
    canonical_state: Mapping[str, Any],
    progress_summary: str,
    remaining_work: str,
    predecessor_handoff_id: str | None = None,
    goal_id: str | None = None,
    timestamp: str | None = None,
    launcher_token: str | None = None,
    handoff_token: str | None = None,
) -> LauncherSummary:
    """Initialize and dispatch generation 1, then stop without project work."""

    _validate_preflight(
        store=store,
        repository_binding=repository_binding,
        repository_observation=repository_observation,
        capabilities=capabilities,
        provider=provider,
    )
    initialized = initialize_goal(
        store,
        goal_text=goal_text,
        completion_contract=completion_contract,
        guards=guards,
        repository_binding=repository_binding,
        initial_fingerprint=initial_fingerprint,
        authorization=authorization,
        goal_id=goal_id,
        timestamp=timestamp,
        launcher_token=launcher_token,
    )
    current_lease = initialized["state"]["active_lease"]
    reserved = reserve_successor(
        store,
        goal_id=initialized["goal_id"],
        expected_revision=initialized["state"]["revision"],
        current_holder_token=current_lease["holder_token"],
        predecessor_thread_id=predecessor_thread_id,
        handoff_token=handoff_token,
        timestamp=timestamp,
    )
    envelope = build_continuation_envelope(
        reserved,
        predecessor_thread_id=predecessor_thread_id,
        predecessor_handoff_id=predecessor_handoff_id,
        canonical_state=canonical_state,
        progress_summary=progress_summary,
        remaining_work=remaining_work,
    )
    envelope_hash = content_sha256(envelope)
    generation = int(reserved["state"]["current_generation"])
    entry = reserved["generations"][str(generation)]
    prompt = build_worker_prompt(
        envelope,
        project_root=str(repository_binding["root"]),
        expected_revision=int(reserved["state"]["revision"]) + 1,
    )
    try:
        provider_result = provider.create_thread(
            prompt=prompt,
            envelope=envelope,
            idempotency_key=str(entry["idempotency_key"]),
        )
    except Exception as error:  # Provider call ambiguity must be retained, never retried.
        provider_result = ThreadCreateResult(
            "ambiguous",
            None,
            {"reason_code": "provider.exception", "exception_type": type(error).__name__},
        )
    status = provider_result.status
    thread_id = provider_result.successor_thread_id
    if status == "returned" and thread_id == predecessor_thread_id:
        status = "duplicate"
        thread_id = None
        provider_result = ThreadCreateResult(
            status,
            None,
            {"reason_code": "provider.reused_predecessor_thread"},
        )
    if status == "returned":
        final = record_successor(
            store,
            goal_id=reserved["goal_id"],
            expected_revision=reserved["state"]["revision"],
            generation=generation,
            handoff_token=str(entry["handoff_token"]),
            successor_thread_id=str(thread_id),
            provider_id=str(provider.provider_id),
            provider_response=provider_result.response,
            timestamp=timestamp,
        )
        summary_status = "dispatched"
    elif status == "manual_pending":
        final = reserved
        summary_status = "manual_handoff_pending"
    else:
        final = record_dispatch_outcome(
            store,
            goal_id=reserved["goal_id"],
            expected_revision=reserved["state"]["revision"],
            generation=generation,
            handoff_token=str(entry["handoff_token"]),
            provider_id=str(provider.provider_id),
            outcome=status,
            diagnostic=provider_result.response,
            timestamp=timestamp,
        )
        summary_status = "dispatch_failed" if status == "definitive_failure" else status
    lease = final["state"].get("active_lease")
    manual_path = provider_result.response.get("envelope_path") if status == "manual_pending" else None
    return LauncherSummary(
        summary_status,
        str(final["goal_id"]),
        generation,
        envelope_hash,
        str(provider.provider_id),
        1,
        str(thread_id) if thread_id else None,
        str(manual_path) if manual_path else None,
        str(final["state"]["phase"]),
        int(final["state"]["revision"]),
        str(lease["holder_kind"]) if lease else None,
    )
