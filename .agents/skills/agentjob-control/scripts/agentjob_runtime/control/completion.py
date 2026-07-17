"""Immutable completion writer for one bounded AgentJob."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from agentjob_runtime.control.activation import _format_cross_issues, _record_set
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.indexes import generate_indexes
from agentjob_runtime.errors import AgentJobControlError, IntegrityError, RecordValidationError, StateConflict
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.validation.cross_record import validate_record_set


class InjectedCompletionFault(AgentJobControlError):
    code = "completion.injected_fault"
    exit_code = 91


@dataclass(frozen=True)
class CompletionWriteReceipt:
    completion_id: str
    job_id: str
    task_id: str
    path: str
    sha256: str
    task_revision: int
    task_closed: bool
    indexes_status: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "completion_finalized",
            "completion_id": self.completion_id,
            "job_id": self.job_id,
            "task_id": self.task_id,
            "path": self.path,
            "sha256": self.sha256,
            "task_revision": self.task_revision,
            "task_closed": self.task_closed,
            "indexes_status": self.indexes_status,
        }


def _fault(fault_after: str | None, boundary: str) -> None:
    if fault_after == boundary:
        raise InjectedCompletionFault(
            f"injected fault after {boundary}", details={"boundary": boundary}
        )


def write_completion(
    store: FilesystemControlStore,
    completion: Mapping[str, Any],
    *,
    expected_revision: int,
    close_task: bool,
    next_recommended_action: str | None = None,
    policies: Sequence[Mapping[str, Any]] = (),
    fault_after: str | None = None,
) -> CompletionWriteReceipt:
    completion = copy.deepcopy(dict(completion))
    store.validate_record("completion", completion)
    task_id = str(completion["task_id"])
    completion_id = str(completion["completion_id"])
    job_id = str(completion["job_id"])
    path = store.record_path("completion", task_id, completion_id)

    with store.control_lock():
        task = store.load_task(task_id)
        if task.get("revision") != expected_revision:
            raise StateConflict(
                f"task revision conflict: expected {expected_revision}, found {task.get('revision')}",
                details={"expected_revision": expected_revision, "actual_revision": task.get("revision")},
            )
        existing_for_job = [
            record
            for kind, _, record in store.iter_records()
            if kind == "completion" and record.get("job_id") == job_id
        ]
        if existing_for_job:
            raise IntegrityError(
                f"AgentJob already has a finalized completion: {job_id}",
                details={"reason_code": "completion.duplicate_for_job"},
            )
        records = _record_set(store, [("completion", completion, store.relative(path))])
        issues = validate_record_set(records, policies=policies, strict_extensions=True)
        if issues:
            raise RecordValidationError(
                "completion failed cross-record validation",
                details={"reason_code": "completion.cross_record_invalid", "findings": _format_cross_issues(issues)},
            )
        store.write_immutable(path, completion)
        _fault(fault_after, "completion")
        if close_task:
            closure = copy.deepcopy(task["closure"])
            references = list(closure.get("completion_refs", []))
            references.append(completion_id)
            closure.update(
                {
                    "status": "closed",
                    "summary": completion.get("next_recommended_action") or completion.get("verdict"),
                    "completion_refs": references,
                    "no_execution_reason": None,
                }
            )
            updated = store.update_task_pointers(
                task_id,
                expected_revision=expected_revision,
                status="completed",
                closure=closure,
                next_recommended_action=next_recommended_action or "No further action required.",
            )
        else:
            updated = store.update_task_pointers(
                task_id,
                expected_revision=expected_revision,
                status="active",
                next_recommended_action=next_recommended_action
                or completion.get("next_recommended_action")
                or "Reevaluate the task.",
            )
        _fault(fault_after, "task_pointer")
        indexes = generate_indexes(store)
        _fault(fault_after, "indexes")
    return CompletionWriteReceipt(
        completion_id,
        job_id,
        task_id,
        store.relative(path),
        content_sha256(completion),
        int(updated["revision"]),
        close_task,
        indexes.status,
    )
