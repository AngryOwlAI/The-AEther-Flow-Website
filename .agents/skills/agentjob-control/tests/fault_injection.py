"""Deterministic observations shared by crash-window tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from agentjob_runtime.bootstrap import doctor_project
from agentjob_runtime.capabilities import CapabilityReport
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.resolver import resolve_store
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


@dataclass(frozen=True)
class ControlObservation:
    doctor_status: str
    boundary: str
    reason_code: str
    task_revision: int
    activated_ids: tuple[str, ...]
    record_counts: Mapping[str, int]


@dataclass(frozen=True)
class GoalObservation:
    integrity_status: str
    revision: int
    phase: str
    journal_entries: int
    provider_receipts: int
    step_receipts: int


def observe_control(
    project_root,
    store: FilesystemControlStore,
    task_id: str,
) -> ControlObservation:
    counts: dict[str, int] = {}
    for kind, _, _ in store.iter_records():
        counts[kind] = counts.get(kind, 0) + 1
    boundary = resolve_store(
        store,
        capabilities=CapabilityReport("ready", ()),
        task_id=task_id,
    )
    return ControlObservation(
        doctor_project(project_root).status,
        boundary.boundary,
        boundary.reason_code,
        int(store.load_task(task_id)["revision"]),
        tuple(sorted(store.activated_record_ids())),
        counts,
    )


def observe_goal(store: SQLiteGoalStore, goal_id: str) -> GoalObservation:
    record = store.load_goal(goal_id)
    return GoalObservation(
        str(store.integrity_check()["status"]),
        int(record["state"]["revision"]),
        str(record["state"]["phase"]),
        len(record["journal"]),
        int(store.query_one("SELECT COUNT(*) AS count FROM provider_receipts")["count"]),
        int(store.query_one("SELECT COUNT(*) AS count FROM step_receipts")["count"]),
    )
