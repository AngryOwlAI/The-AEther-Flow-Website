"""Immutable non-authoritative handoff writer."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from agentjob_runtime.control.activation import _format_cross_issues, _record_set
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.indexes import generate_indexes
from agentjob_runtime.errors import AgentJobControlError, RecordValidationError, StateConflict
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.validation.cross_record import validate_record_set


class InjectedHandoffFault(AgentJobControlError):
    code = "handoff.injected_fault"
    exit_code = 92


@dataclass(frozen=True)
class HandoffWriteReceipt:
    handoff_id: str
    task_id: str
    path: str
    sha256: str
    task_revision: int
    grants_execution_authority: bool
    indexes_status: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "handoff_finalized",
            "handoff_id": self.handoff_id,
            "task_id": self.task_id,
            "path": self.path,
            "sha256": self.sha256,
            "task_revision": self.task_revision,
            "grants_execution_authority": self.grants_execution_authority,
            "indexes_status": self.indexes_status,
        }


def write_handoff(
    store: FilesystemControlStore,
    handoff: Mapping[str, Any],
    *,
    expected_revision: int,
    policies: Sequence[Mapping[str, Any]] = (),
    fault_after: str | None = None,
) -> HandoffWriteReceipt:
    handoff = copy.deepcopy(dict(handoff))
    store.validate_record("handoff", handoff)
    handoff_id = str(handoff["handoff_id"])
    task_id = str(handoff["predecessor"]["task_id"])
    path = store.record_path("handoff", task_id, handoff_id)
    with store.control_lock():
        task = store.load_task(task_id)
        if task.get("revision") != expected_revision:
            raise StateConflict(
                f"task revision conflict: expected {expected_revision}, found {task.get('revision')}",
                details={"expected_revision": expected_revision, "actual_revision": task.get("revision")},
            )
        records = _record_set(store, [("handoff", handoff, store.relative(path))])
        issues = validate_record_set(records, policies=policies, strict_extensions=True)
        if issues:
            raise RecordValidationError(
                "handoff failed cross-record validation",
                details={"reason_code": "handoff.cross_record_invalid", "findings": _format_cross_issues(issues)},
            )
        store.write_immutable(path, handoff)
        if fault_after == "handoff":
            raise InjectedHandoffFault("injected fault after handoff")
        updated = store.update_task_pointers(
            task_id,
            expected_revision=expected_revision,
            next_recommended_action=str(handoff["next_action"]["objective"]),
        )
        if fault_after == "task_pointer":
            raise InjectedHandoffFault("injected fault after task pointer")
        indexes = generate_indexes(store)
    return HandoffWriteReceipt(
        handoff_id,
        task_id,
        store.relative(path),
        content_sha256(handoff),
        int(updated["revision"]),
        False,
        indexes.status,
    )
