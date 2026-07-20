"""Deterministic derived indexes for portable control records."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import IntegrityError, RecordValidationError
from agentjob_runtime.records.canonical import content_sha256, render_canonical_json


INDEX_NAMES = {
    "task": "TASK_INDEX.json",
    "director_decision": "DIRECTOR_DECISION_INDEX.json",
    "agent_job": "AGENT_JOB_INDEX.json",
    "execution_role": "EXECUTION_ROLE_INDEX.json",
    "completion": "COMPLETION_INDEX.json",
    "handoff": "HANDOFF_INDEX.json",
    "activation": "ACTIVATION_INDEX.json",
    "supersession": "SUPERSESSION_INDEX.json",
}
ID_FIELDS = {
    "task": "task_id",
    "director_decision": "decision_id",
    "agent_job": "job_id",
    "execution_role": "execution_role_id",
    "completion": "completion_id",
    "handoff": "handoff_id",
    "activation": "activation_id",
    "supersession": "supersession_id",
}


@dataclass(frozen=True)
class IndexReceipt:
    status: str
    paths: tuple[str, ...]
    drifted: tuple[str, ...]


def build_indexes(store: FilesystemControlStore) -> dict[str, dict[str, Any]]:
    activated = store.activated_record_ids()
    grouped: dict[str, list[dict[str, Any]]] = {kind: [] for kind in INDEX_NAMES}
    seen: dict[tuple[str, str], str] = {}
    for kind, path, record in store.iter_records():
        store.validate_record(kind, record)
        record_id = str(record[ID_FIELDS[kind]])
        key = (kind, record_id)
        if key in seen:
            raise IntegrityError(
                f"duplicate {kind} identifier: {record_id}",
                details={"reason_code": "index.duplicate_id", "paths": [seen[key], store.relative(path)]},
            )
        seen[key] = store.relative(path)
        is_activated = kind in {"task", "activation", "completion", "handoff", "supersession"} or record_id in activated
        if kind == "agent_job" and record.get("status") == "active" and not is_activated:
            raise IntegrityError(
                f"active job lacks activation: {record_id}",
                details={"reason_code": "activation.active_job_missing"},
            )
        grouped[kind].append(
            {
                "record_id": record_id,
                "source_path": store.relative(path),
                "sha256": content_sha256(record),
                "status": record.get("status"),
                "task_id": record.get("task_id"),
                "activated": is_activated,
            }
        )
    return {
        kind: {
            "schema_version": "sys4ai.derived-index.v1",
            "record_type": kind,
            "records": sorted(rows, key=lambda item: (item["record_id"], item["source_path"])),
        }
        for kind, rows in grouped.items()
    }


def generate_indexes(
    store: FilesystemControlStore, *, check: bool = False, export_csv: bool = False
) -> IndexReceipt:
    store.initialize_layout()
    indexes = build_indexes(store)
    written: list[str] = []
    drifted: list[str] = []
    for kind, index in indexes.items():
        path = store.indexes_root / INDEX_NAMES[kind]
        expected = render_canonical_json(index)
        relative = store.relative(path)
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual != expected:
            drifted.append(relative)
            if not check:
                store.write_mutable(path, index)
        written.append(relative)
        if export_csv and not check:
            output = io.StringIO(newline="")
            writer = csv.DictWriter(
                output,
                fieldnames=["record_id", "source_path", "sha256", "status", "task_id", "activated"],
            )
            writer.writeheader()
            writer.writerows(index["records"])
            csv_path = path.with_suffix(".csv")
            store._atomic_write(csv_path, output.getvalue().encode("utf-8"))
            written.append(store.relative(csv_path))
    return IndexReceipt("drift" if drifted and check else "pass", tuple(written), tuple(drifted))
