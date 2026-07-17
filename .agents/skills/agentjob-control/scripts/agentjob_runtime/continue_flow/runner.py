"""High-level zero-or-one-AgentJob continuation orchestration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from agentjob_runtime.config import load_config
from agentjob_runtime.continue_flow.director import (
    DirectorOutcome,
    DirectorRoute,
    resolve_director_packet,
)
from agentjob_runtime.continue_flow.finalize import (
    ContinueFinalization,
    HandoffPlan,
    finalize_execution,
    finalize_no_action,
)
from agentjob_runtime.continue_flow.preflight import ContinuePreflight, run_preflight
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.execution.compiler import compile_authority
from agentjob_runtime.execution.executor import (
    ExecutionContext,
    ExecutionEvidence,
    InvocationBudget,
    capture_file_state,
    execute_one_job,
)
from agentjob_runtime.execution.validation import (
    CheckpointProvider,
    PostExecutionReport,
    ValidatorAdapter,
    validate_execution,
)
from agentjob_runtime.goal.model import utc_now
from agentjob_runtime.records.canonical import content_sha256


@dataclass(frozen=True)
class ContinueInvocation:
    preflight: Mapping[str, Any]
    director: Mapping[str, Any] | None
    execution: Mapping[str, Any] | None
    validation: Mapping[str, Any] | None
    finalization: ContinueFinalization

    @property
    def result(self) -> Mapping[str, Any]:
        return self.finalization.result

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _preflight_fingerprint(preflight: ContinuePreflight) -> str:
    return preflight.fingerprint or content_sha256(preflight.as_dict())


def _protected_finalization(
    preflight: ContinuePreflight,
    *,
    boundary: str | None = None,
    reason_code: str | None = None,
    status: str | None = None,
    next_recommended_action: str | None = None,
) -> ContinueFinalization:
    value = preflight.boundary
    return finalize_no_action(
        boundary_entered=boundary or str(value["boundary"]),
        reason_code=reason_code or str(value["reason_code"]),
        repository_fingerprint=_preflight_fingerprint(preflight),
        status=status,
        task_id=str(value["task_id"]) if value.get("task_id") else None,
        decision_id=str(value["decision_id"]) if value.get("decision_id") else None,
        job_id=str(value["job_id"]) if value.get("job_id") else None,
        next_recommended_action=next_recommended_action,
    )


def run_continue(
    project_root: str | Path,
    *,
    config_path: str | Path | None = None,
    task_id: str | None = None,
    repository_snapshot: Mapping[str, Any] | None = None,
    provider_versions: Mapping[str, str] | None = None,
    routes: Sequence[DirectorRoute] = (),
    runtime_controls: Mapping[str, bool] | None = None,
    operation: Callable[[ExecutionContext], Any] | None = None,
    validator_adapters: Mapping[str, ValidatorAdapter] | None = None,
    checkpoint_provider: CheckpointProvider | None = None,
    proposed_claims: Sequence[str] = (),
    handoff_plan: HandoffPlan | None = None,
    close_task: bool = False,
    actor_ref: str = "continue:system-director",
    policy_refs: Sequence[str] = (".agents/control/policies/default.json",),
    policies: Sequence[Mapping[str, Any]] = (),
    timestamp: str | None = None,
) -> ContinueInvocation:
    """Resolve, execute, validate, and finalize at most one AgentJob."""

    started_at = timestamp or utc_now()
    preflight = run_preflight(
        project_root,
        config_path=config_path,
        task_id=task_id,
        repository_snapshot=repository_snapshot,
        provider_versions=provider_versions,
    )
    boundary = str(preflight.boundary["boundary"])
    if boundary not in {"existing_agent_job_ready", "director_decision_required"}:
        finalization = _protected_finalization(preflight)
        return ContinueInvocation(preflight.as_dict(), None, None, None, finalization)

    loaded = load_config(
        project_root,
        config_path=config_path,
        provider_versions=provider_versions,
    )
    store = FilesystemControlStore(loaded.project_root, loaded.control_root)
    expected_revision = None
    if preflight.boundary.get("task_id"):
        expected_revision = int(
            store.load_task(str(preflight.boundary["task_id"]))["revision"]
        )
    director: DirectorOutcome = resolve_director_packet(
        preflight,
        store=store,
        routes=routes,
        expected_revision=expected_revision,
        actor_ref=actor_ref,
        policy_refs=policy_refs,
        policies=policies,
        timestamp=started_at,
    )
    if director.status == "protected_stop":
        finalization = _protected_finalization(
            preflight,
            boundary=director.boundary,
            reason_code=director.reason_code,
            status="human_gate_required"
            if director.boundary == "human_gate_required"
            else "blocked",
        )
        return ContinueInvocation(
            preflight.as_dict(), director.as_dict(), None, None, finalization
        )
    if runtime_controls is None:
        finalization = _protected_finalization(
            preflight,
            reason_code="execution.runtime_controls_missing",
            status="blocked",
            next_recommended_action="Configure exact runtime enforcement controls.",
        )
        return ContinueInvocation(
            preflight.as_dict(), director.as_dict(), None, None, finalization
        )
    if operation is None:
        finalization = _protected_finalization(
            preflight,
            reason_code="execution.operation_adapter_missing",
            status="blocked",
            next_recommended_action="Supply the bounded AgentJob operation adapter.",
        )
        return ContinueInvocation(
            preflight.as_dict(), director.as_dict(), None, None, finalization
        )

    if director.job is None or director.execution_role is None:
        raise RuntimeError("Director returned no executable packet")
    authority = compile_authority(
        project_root=loaded.project_root,
        job=director.job,
        execution_role=director.execution_role,
        activated_record_ids=store.activated_record_ids(),
        runtime_capabilities=runtime_controls,
    )
    snapshot_ignored_roots = (loaded.data["goal_relay"]["local_root"],)
    _, expected_execution_fingerprint = capture_file_state(
        loaded.project_root,
        ignored_roots=snapshot_ignored_roots,
    )
    evidence: ExecutionEvidence = execute_one_job(
        authority=authority,
        store=store,
        operation=operation,
        budget=InvocationBudget(),
        expected_before_fingerprint=expected_execution_fingerprint,
        snapshot_ignored_roots=snapshot_ignored_roots,
    )
    validation: PostExecutionReport = validate_execution(
        authority=authority,
        evidence=evidence,
        validator_adapters=validator_adapters,
        checkpoint_provider=checkpoint_provider,
        proposed_claims=proposed_claims,
    )
    current_revision = int(store.load_task(authority.task_id)["revision"])
    finalization = finalize_execution(
        store=store,
        boundary_entered=boundary,
        authority=authority,
        evidence=evidence,
        validation=validation,
        expected_revision=current_revision,
        started_at=started_at,
        completed_at=timestamp,
        before_revision=str(preflight.repository.get("revision"))
        if preflight.repository.get("revision") is not None
        else None,
        after_revision=str(preflight.repository.get("revision"))
        if preflight.repository.get("revision") is not None
        else None,
        close_task=close_task,
        handoff_plan=handoff_plan,
        policies=policies,
    )
    return ContinueInvocation(
        preflight.as_dict(),
        director.as_dict(),
        evidence.as_dict(),
        validation.as_dict(),
        finalization,
    )
