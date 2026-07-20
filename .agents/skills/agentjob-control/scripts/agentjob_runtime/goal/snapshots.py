"""Regenerable redacted human snapshots for canonical SQLite goal state."""

from __future__ import annotations

import os
import stat
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.config import resolve_project_path
from agentjob_runtime.errors import SecurityError, StateConflict
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


@dataclass(frozen=True)
class SnapshotReceipt:
    status: str
    goal_id: str
    source_revision: int
    resulting_revision: int
    path: str
    reason_code: str | None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def render_redacted_snapshot(record: Mapping[str, Any]) -> str:
    """Render stable operator context without tokens, goal prose, or provider payloads."""

    return (
        "# Durable goal relay snapshot\n\n"
        f"- Goal ID: `{record['goal_id']}`\n"
        f"- Goal SHA-256: `{record['goal_sha256']}`\n"
        f"- Completion contract SHA-256: `{record['completion_contract_sha256']}`\n"
        f"- Revision: `{record['state']['revision']}`\n"
        f"- Phase: `{record['state']['phase']}`\n"
        f"- Current generation: `{record['state']['current_generation']}`\n"
        f"- Passes consumed: `{record['state']['passes_consumed']}`\n"
        f"- Goal evaluation: `{record['state']['goal_evaluation']}`\n"
        f"- Journal entries: `{len(record['journal'])}`\n"
    )


def _write_snapshot(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.is_symlink():
            raise SecurityError("goal snapshot cannot replace a symlink")
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise SecurityError("goal snapshot target has an unsafe alias")
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


def regenerate_goal_snapshot(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    output_path: str,
    inject_render_failure: bool = False,
    timestamp: str | None = None,
) -> SnapshotReceipt:
    """Render a derivative; record a failure without changing canonical goal facts."""

    record = store.load_goal(goal_id)
    if record["state"]["revision"] != expected_revision:
        raise StateConflict("snapshot source revision changed")
    root = Path(record["repository_binding"]["root"])
    path = resolve_project_path(
        root,
        output_path,
        purpose="goal snapshot",
        reject_install_roots=True,
    )
    try:
        if inject_render_failure:
            raise OSError("injected snapshot render failure")
        _write_snapshot(path, render_redacted_snapshot(record).encode("utf-8"))
    except OSError as error:
        with store.mutation(
            goal_id,
            expected_revision=expected_revision,
            timestamp=timestamp,
        ) as mutation:
            mutation.event(
                "snapshot_render_failed",
                {
                    "path": path.relative_to(root).as_posix(),
                    "error_type": type(error).__name__,
                },
            )
        failed = store.load_goal(goal_id)
        return SnapshotReceipt(
            "failed",
            goal_id,
            expected_revision,
            int(failed["state"]["revision"]),
            path.relative_to(root).as_posix(),
            "snapshot.render_failed",
        )
    return SnapshotReceipt(
        "pass",
        goal_id,
        expected_revision,
        expected_revision,
        path.relative_to(root).as_posix(),
        None,
    )
