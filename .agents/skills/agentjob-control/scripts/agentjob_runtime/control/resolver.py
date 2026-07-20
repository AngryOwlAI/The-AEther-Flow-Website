"""Deterministic continuation-boundary resolver.

The resolver classifies validated state. It never selects a new route or role;
that remains the System Director phase when the returned boundary requires it.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from agentjob_runtime.capabilities import CapabilityReport
from agentjob_runtime.control.filesystem_store import FilesystemControlStore


BOUNDARIES = {
    "bootstrap_required",
    "existing_agent_job_ready",
    "director_decision_required",
    "human_gate_required",
    "no_action",
    "blocked",
    "control_repair_required",
}


@dataclass(frozen=True)
class BoundaryResult:
    boundary: str
    reason_code: str
    task_id: str | None = None
    decision_id: str | None = None
    job_id: str | None = None
    execution_role_id: str | None = None
    execution_performed: bool = False
    required_authority_surfaces: tuple[str, ...] = ()
    stop_conditions: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def resolve_snapshot(snapshot: Mapping[str, Any]) -> BoundaryResult:
    """Classify one already-inspected state snapshot."""

    if not snapshot.get("configured", False) or not snapshot.get("capabilities_ready", False):
        return BoundaryResult(
            "bootstrap_required",
            "capability.missing_required",
            stop_conditions=("missing_required_capability",),
        )
    integrity_findings = tuple(snapshot.get("integrity_findings", ()))
    if integrity_findings:
        return BoundaryResult(
            "control_repair_required",
            "control.integrity_findings",
            task_id=snapshot.get("task_id"),
            required_authority_surfaces=("validated control-repair AgentJob",),
            stop_conditions=integrity_findings,
        )
    if snapshot.get("repository_match") is False:
        return BoundaryResult(
            "blocked",
            "repository.binding_mismatch",
            task_id=snapshot.get("task_id"),
            stop_conditions=("repository_binding_mismatch",),
        )
    if snapshot.get("concurrent_conflict"):
        return BoundaryResult(
            "blocked",
            "control.concurrent_conflict",
            task_id=snapshot.get("task_id"),
            stop_conditions=("concurrent_control_change",),
        )

    task = snapshot.get("task")
    if task is None:
        return BoundaryResult("no_action", "task.none_active")
    task_id = task.get("task_id")
    if task.get("requires_human_gate") or task.get("status") == "human_gated":
        return BoundaryResult(
            "human_gate_required",
            "task.human_gate_required",
            task_id=task_id,
            required_authority_surfaces=("exact human-gate approval",),
            stop_conditions=("human_gate_required",),
        )
    if task.get("status") in {"completed", "cancelled", "superseded"}:
        return BoundaryResult("no_action", "task.terminal", task_id=task_id)
    if task.get("status") == "blocked" and not task.get("current_job_id"):
        return BoundaryResult(
            "blocked",
            "task.blocked_without_route",
            task_id=task_id,
            stop_conditions=("blocked_task",),
        )

    job = snapshot.get("job")
    decision = snapshot.get("decision")
    role = snapshot.get("role")
    completion = snapshot.get("completion")
    if job is None:
        return BoundaryResult(
            "director_decision_required",
            "job.none_current",
            task_id=task_id,
            required_authority_surfaces=("Director Decision Record", "AgentJob", "execution-role binding"),
        )
    if decision is None or role is None or not snapshot.get("packet_activated", False):
        return BoundaryResult(
            "control_repair_required",
            "packet.incomplete_or_unactivated",
            task_id=task_id,
            decision_id=decision.get("decision_id") if isinstance(decision, Mapping) else None,
            job_id=job.get("job_id"),
            stop_conditions=("invalid_control_packet",),
        )
    if snapshot.get("state_snapshot_stale"):
        return BoundaryResult(
            "director_decision_required",
            "packet.stale_requires_supersession_decision",
            task_id=task_id,
            decision_id=decision.get("decision_id"),
            job_id=job.get("job_id"),
            required_authority_surfaces=("superseding Director Decision Record",),
        )
    if isinstance(completion, Mapping) and completion.get("job_id") == job.get("job_id"):
        return BoundaryResult(
            "director_decision_required",
            "job.completion_recorded_requires_next_decision",
            task_id=task_id,
            decision_id=decision.get("decision_id"),
            job_id=job.get("job_id"),
            required_authority_surfaces=("new Director Decision Record",),
            stop_conditions=("completed_job_cannot_be_reexecuted",),
        )
    if job.get("status") in {"active", "draft"}:
        return BoundaryResult(
            "existing_agent_job_ready",
            "job.activated_and_ready",
            task_id=task_id,
            decision_id=decision.get("decision_id"),
            job_id=job.get("job_id"),
            execution_role_id=role.get("execution_role_id"),
            required_authority_surfaces=(
                "activated decision",
                "activated AgentJob",
                "execution-role binding",
                "project policy",
            ),
            stop_conditions=tuple(job.get("stop_conditions", ())),
        )
    if job.get("status") in {"completed", "blocked", "failed", "cancelled", "superseded"}:
        return BoundaryResult(
            "director_decision_required",
            "job.terminal_requires_next_decision",
            task_id=task_id,
            decision_id=decision.get("decision_id"),
            job_id=job.get("job_id"),
        )
    return BoundaryResult(
        "blocked",
        "job.status_unknown",
        task_id=task_id,
        decision_id=decision.get("decision_id"),
        job_id=job.get("job_id"),
        stop_conditions=("unknown_job_status",),
    )


def snapshot_from_store(
    store: FilesystemControlStore,
    *,
    capabilities: CapabilityReport,
    task_id: str | None = None,
    integrity_findings: Sequence[str] = (),
    repository_match: bool = True,
    state_snapshot_stale: bool = False,
    concurrent_conflict: bool = False,
) -> dict[str, Any]:
    records: dict[str, dict[str, Mapping[str, Any]]] = {
        "task": {},
        "director_decision": {},
        "agent_job": {},
        "execution_role": {},
        "completion": {},
    }
    id_fields = {
        "task": "task_id",
        "director_decision": "decision_id",
        "agent_job": "job_id",
        "execution_role": "execution_role_id",
        "completion": "completion_id",
    }
    for kind, _, record in store.iter_records():
        if kind in records:
            records[kind][str(record[id_fields[kind]])] = record

    if task_id is None:
        candidates = [
            record
            for record in records["task"].values()
            if record.get("status") in {"active", "blocked", "human_gated"}
        ]
        task = candidates[0] if len(candidates) == 1 else None
        if len(candidates) > 1:
            integrity_findings = tuple(integrity_findings) + ("multiple_active_tasks",)
    else:
        task = records["task"].get(task_id)
    decision = None
    job = None
    role = None
    completion = None
    if task:
        decision = records["director_decision"].get(str(task.get("current_decision_id")))
        job = records["agent_job"].get(str(task.get("current_job_id")))
        if job:
            matches = [item for item in records["execution_role"].values() if item.get("job_id") == job.get("job_id")]
            role = matches[0] if len(matches) == 1 else None
            if len(matches) > 1:
                integrity_findings = tuple(integrity_findings) + ("multiple_execution_roles",)
            completions = [
                item
                for item in records["completion"].values()
                if item.get("job_id") == job.get("job_id")
            ]
            completion = completions[0] if len(completions) == 1 else None
            if len(completions) > 1:
                integrity_findings = tuple(integrity_findings) + ("multiple_job_completions",)
    activated = store.activated_record_ids()
    packet_activated = bool(
        job
        and decision
        and role
        and {str(job.get("job_id")), str(decision.get("decision_id")), str(role.get("execution_role_id"))}.issubset(activated)
    )
    return {
        "configured": True,
        "capabilities_ready": capabilities.status == "ready",
        "integrity_findings": tuple(integrity_findings),
        "repository_match": repository_match,
        "concurrent_conflict": concurrent_conflict,
        "task": task,
        "task_id": task.get("task_id") if task else task_id,
        "decision": decision,
        "job": job,
        "role": role,
        "completion": completion,
        "packet_activated": packet_activated,
        "state_snapshot_stale": state_snapshot_stale,
    }


def resolve_store(
    store: FilesystemControlStore,
    *,
    capabilities: CapabilityReport,
    task_id: str | None = None,
    **snapshot_options: Any,
) -> BoundaryResult:
    return resolve_snapshot(
        snapshot_from_store(store, capabilities=capabilities, task_id=task_id, **snapshot_options)
    )
