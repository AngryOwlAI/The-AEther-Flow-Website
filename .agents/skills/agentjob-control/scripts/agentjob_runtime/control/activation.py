"""Validation-first activation of one immutable decision/job/role packet."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from agentjob_runtime.control.filesystem_store import FilesystemControlStore, SCHEMA_VERSIONS
from agentjob_runtime.control.indexes import generate_indexes
from agentjob_runtime.errors import AgentJobControlError, RecordValidationError, StateConflict
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.validation.cross_record import ConformanceIssue, validate_record_set


class InjectedActivationFault(AgentJobControlError):
    code = "activation.injected_fault"
    exit_code = 90


@dataclass(frozen=True)
class ActivationReceipt:
    activation_id: str
    task_id: str
    decision_id: str
    job_id: str
    execution_role_id: str
    activation_path: str
    task_revision: int
    record_hashes: Mapping[str, str]
    indexes_status: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "activated",
            "activation_id": self.activation_id,
            "task_id": self.task_id,
            "decision_id": self.decision_id,
            "job_id": self.job_id,
            "execution_role_id": self.execution_role_id,
            "activation_path": self.activation_path,
            "task_revision": self.task_revision,
            "record_hashes": dict(self.record_hashes),
            "indexes_status": self.indexes_status,
        }


PLURAL_KIND = {
    "task": "tasks",
    "director_decision": "decisions",
    "agent_job": "jobs",
    "execution_role": "roles",
    "completion": "completions",
    "handoff": "handoffs",
    "activation": "activations",
    "supersession": "supersessions",
}
ID_FIELD = {
    "task": "task_id",
    "director_decision": "decision_id",
    "agent_job": "job_id",
    "execution_role": "execution_role_id",
    "completion": "completion_id",
    "handoff": "handoff_id",
    "activation": "activation_id",
    "supersession": "supersession_id",
}


def _raise_fault(fault_after: str | None, boundary: str) -> None:
    if fault_after == boundary:
        raise InjectedActivationFault(
            f"injected fault after {boundary}", details={"boundary": boundary}
        )


def _record_set(
    store: FilesystemControlStore,
    additions: Sequence[tuple[str, Mapping[str, Any], str]],
) -> dict[str, list[dict[str, Any]]]:
    records: dict[str, list[dict[str, Any]]] = {
        "tasks": [],
        "decisions": [],
        "jobs": [],
        "roles": [],
        "completions": [],
        "handoffs": [],
        "activations": [],
        "supersessions": [],
        "goal_receipts": [],
    }
    keyed: dict[tuple[str, str], dict[str, Any]] = {}
    for kind, path, record in store.iter_records():
        plural = PLURAL_KIND[kind]
        value = copy.deepcopy(record)
        value["_path"] = store.relative(path)
        keyed[(plural, str(record[ID_FIELD[kind]]))] = value
    for kind, record, relative_path in additions:
        plural = PLURAL_KIND[kind]
        value = copy.deepcopy(dict(record))
        value["_path"] = relative_path
        keyed[(plural, str(record[ID_FIELD[kind]]))] = value
    for (plural, _), value in sorted(keyed.items()):
        records[plural].append(value)
    return records


def _format_cross_issues(issues: Sequence[ConformanceIssue]) -> list[dict[str, str]]:
    return [
        {"code": issue.code, "record_id": issue.record_id, "field": issue.field, "message": issue.message}
        for issue in issues
    ]


def activate_packet(
    store: FilesystemControlStore,
    *,
    task_id: str,
    decision: Mapping[str, Any],
    job: Mapping[str, Any],
    execution_role: Mapping[str, Any],
    expected_revision: int,
    activation_id: str | None = None,
    packet_type: str = "director_job_packet",
    additional_records: Sequence[tuple[str, Mapping[str, Any]]] = (),
    policies: Sequence[Mapping[str, Any]] = (),
    fault_after: str | None = None,
) -> ActivationReceipt:
    """Activate one packet; the activation manifest is the authority boundary."""

    decision = copy.deepcopy(dict(decision))
    job = copy.deepcopy(dict(job))
    execution_role = copy.deepcopy(dict(execution_role))
    if decision.get("task_id") != task_id or job.get("task_id") != task_id or execution_role.get("task_id") != task_id:
        raise RecordValidationError("packet task IDs do not match the requested task")
    if decision.get("selected", {}).get("agent_job_id") != job.get("job_id"):
        raise RecordValidationError("decision does not select the supplied AgentJob")
    if job.get("decision_id") != decision.get("decision_id"):
        raise RecordValidationError("AgentJob does not reference the supplied decision")
    if execution_role.get("job_id") != job.get("job_id"):
        raise RecordValidationError("execution-role binding does not reference the supplied AgentJob")
    if job.get("role_binding", {}).get("role_id") != execution_role.get("role_id"):
        raise RecordValidationError("AgentJob and execution-role role IDs differ")

    store.validate_record("director_decision", decision)
    store.validate_record("agent_job", job)
    store.validate_record("execution_role", execution_role)
    for kind, record in additional_records:
        store.validate_record(kind, record)

    activation_id = activation_id or f"ACT-{job['job_id']}"
    decision_path = store.record_path("director_decision", task_id, str(decision["decision_id"]))
    job_path = store.record_path("agent_job", task_id, str(job["job_id"]))
    role_path = store.record_path("execution_role", task_id, str(execution_role["execution_role_id"]))
    activation_path = store.record_path("activation", task_id, activation_id)
    final_records: list[tuple[str, Mapping[str, Any], Any]] = [
        ("director_decision", decision, decision_path),
        ("agent_job", job, job_path),
        ("execution_role", execution_role, role_path),
    ]
    for kind, record in additional_records:
        record_id = str(record[ID_FIELD[kind]])
        final_records.append((kind, copy.deepcopy(dict(record)), store.record_path(kind, task_id, record_id)))

    activation = {
        "schema_version": "sys4ai.activation.v1",
        "activation_id": activation_id,
        "packet_type": packet_type,
        "records": [
            {
                "order": index,
                "path": store.relative(path),
                "record_id": str(record[ID_FIELD[kind]]),
                "record_type": kind,
                "sha256": content_sha256(record),
            }
            for index, (kind, record, path) in enumerate(final_records, 1)
        ],
        "activated_at": str(decision.get("activated_at") or job.get("activated_at")),
        "activation_revision": expected_revision + 1,
        "prior_control_revision": expected_revision,
        "extensions": {},
    }
    store.validate_record("activation", activation)

    additions_for_validation = [
        (kind, record, store.relative(path)) for kind, record, path in final_records
    ] + [("activation", activation, store.relative(activation_path))]

    with store.control_lock():
        task = store.load_task(task_id)
        if task.get("revision") != expected_revision:
            raise StateConflict(
                f"task revision conflict: expected {expected_revision}, found {task.get('revision')}",
                details={"expected_revision": expected_revision, "actual_revision": task.get("revision")},
            )
        records = _record_set(store, additions_for_validation)
        issues = validate_record_set(records, policies=policies, strict_extensions=True)
        if issues:
            raise RecordValidationError(
                "packet failed cross-record validation",
                details={"reason_code": "activation.cross_record_invalid", "findings": _format_cross_issues(issues)},
            )

        staging = store.create_staging_directory(activation_id)
        for kind, record, _ in final_records:
            stage_path = staging / f"{kind}-{record[ID_FIELD[kind]]}.json"
            store.write_immutable(stage_path, record)
        store.write_immutable(staging / "activation.json", activation)
        _raise_fault(fault_after, "staged")

        for kind, record, path in final_records:
            store.write_immutable(path, record, allow_identical=True)
            _raise_fault(fault_after, kind)

        store.write_immutable(activation_path, activation, allow_identical=True)
        _raise_fault(fault_after, "manifest")
        task = store.update_task_pointers(
            task_id,
            expected_revision=expected_revision,
            decision_id=str(decision["decision_id"]),
            job_id=str(job["job_id"]),
            status="active",
            next_recommended_action=f"Execute AgentJob {job['job_id']}.",
        )
        _raise_fault(fault_after, "task_pointer")
        index_receipt = generate_indexes(store)
        _raise_fault(fault_after, "indexes")
        store.remove_staging_directory(staging)

    return ActivationReceipt(
        activation_id=activation_id,
        task_id=task_id,
        decision_id=str(decision["decision_id"]),
        job_id=str(job["job_id"]),
        execution_role_id=str(execution_role["execution_role_id"]),
        activation_path=store.relative(activation_path),
        task_revision=int(task["revision"]),
        record_hashes={str(record[ID_FIELD[kind]]): content_sha256(record) for kind, record, _ in final_records},
        indexes_status=index_receipt.status,
    )
