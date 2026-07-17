#!/usr/bin/env python3
"""Measure governed-continuation control operations without changing semantics."""

from __future__ import annotations

import argparse
import json
import platform
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable


PACKAGE = Path(__file__).resolve().parents[1]
SCRIPTS = PACKAGE / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agentjob_runtime.capabilities import CapabilityReport  # noqa: E402
from agentjob_runtime.control.filesystem_store import FilesystemControlStore  # noqa: E402
from agentjob_runtime.control.indexes import generate_indexes  # noqa: E402
from agentjob_runtime.control.resolver import resolve_store  # noqa: E402
from agentjob_runtime.fingerprinting.canonical import build_fingerprint  # noqa: E402
from agentjob_runtime.goal.initialize import initialize_goal  # noqa: E402
from agentjob_runtime.goal.receipts import finalize_receipt  # noqa: E402
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore  # noqa: E402
from agentjob_runtime.records.canonical import content_sha256  # noqa: E402


TS = "2026-07-17T15:00:00Z"
BUDGETS_SECONDS = {
    "status_scan": 8.0,
    "resolve": 8.0,
    "fingerprint": 3.0,
    "index_regeneration": 20.0,
    "goal_export": 20.0,
    "database_compaction": 30.0,
}


def _task(index: int) -> dict[str, Any]:
    task_id = f"TASK-BENCH-{index:06d}"
    return {
        "schema_version": "sys4ai.task.v1",
        "task_id": task_id,
        "objective": f"Benchmark task {index}.",
        "status": "active",
        "parent_task_id": None,
        "source_task_ref": None,
        "current_decision_id": None,
        "current_job_id": None,
        "requires_human_gate": False,
        "human_gate_refs": [],
        "created_at": TS,
        "updated_at": TS,
        "revision": 1,
        "closure": {
            "status": "open",
            "summary": None,
            "completion_refs": [],
            "no_execution_reason": None,
        },
        "next_recommended_action": "Await a bounded Director decision.",
        "extensions": {},
    }


def _measure(operation: Callable[[], Any]) -> tuple[Any, float]:
    started = time.perf_counter()
    value = operation()
    return value, time.perf_counter() - started


def _initialize_receipt_history(store: SQLiteGoalStore, root: Path, count: int) -> str:
    goal = initialize_goal(
        store,
        goal_text="Preserve a large evidence history.",
        completion_contract={
            "interpretation": "Every synthetic receipt remains readable.",
            "required_evidence": ["Receipt history is retained."],
            "user_confirmed_when_ambiguous": True,
        },
        guards={"max_continue_passes": count + 1, "deadline_at": "2099-01-01T00:00:00Z"},
        repository_binding={
            "project_id": "performance-fixture",
            "root": str(root),
            "worktree": str(root),
            "branch": "benchmark",
            "git_common_dir": str(root / ".git"),
            "starting_revision": "benchmark-start",
            "environment_mode": "local",
        },
        initial_fingerprint="a" * 64,
        authorization={"fresh_recursive_threads_explicitly_requested": True},
        goal_id="CG-20260717T150000Z-bbbbbbbb",
        timestamp=TS,
        launcher_token="l" * 48,
    )
    with store.mutation(goal["goal_id"], expected_revision=1, timestamp=TS) as mutation:
        record = mutation.record
        for generation in range(1, count + 1):
            token = f"handoff-{generation:08d}-" + "h" * 32
            record["generations"][str(generation)] = {
                "generation": generation,
                "handoff_token": token,
                "idempotency_key": f"{goal['goal_id']}:{generation}",
                "phase": "terminal_awaiting_human",
                "lease_token": token,
                "invocation_consumed": False,
                "invocation_state": "not_authorized",
                "consumed_at": None,
                "returned_at": None,
                "before_fingerprint": "a" * 64,
                "after_fingerprint": None,
                "fingerprint_status": None,
                "pending_step_result": None,
                "finalized_receipt_hash": None,
                "terminal_or_successor_outcome": None,
                "claimed_at": None,
                "successor_thread_id": None,
            }
            finalize_receipt(
                mutation,
                generation=generation,
                invocation_count=0,
                decision="protected_stop",
                evidence={
                    "zero_job_reason": "Synthetic performance fixture; no execution occurred.",
                    "goal_evaluation": "indeterminate",
                    "progress_summary": f"Receipt {generation} retained.",
                    "remaining_work": "No benchmark work is authorized.",
                },
            )
        record["state"]["current_generation"] = count
        record["state"]["phase"] = "terminal_cancelled"
        record["state"]["terminal_reason"] = "performance_fixture_complete"
        record["handoff"] = {
            "status": "none",
            "generation": count + 1,
            "token": None,
            "idempotency_key": None,
            "predecessor_thread_id": None,
            "successor_thread_id": None,
        }
        mutation.release_lease()
    return goal["goal_id"]


def run_benchmark(root: Path, count: int) -> dict[str, Any]:
    control = FilesystemControlStore(root, ".agents/control")
    task_hashes: list[str] = []
    fixture_started = time.perf_counter()
    for index in range(1, count + 1):
        task = _task(index)
        control.create_task(task)
        task_hashes.append(content_sha256(task))
    sqlite = SQLiteGoalStore(root / ".local/state.sqlite3")
    goal_id = _initialize_receipt_history(sqlite, root, count)
    fixture_seconds = time.perf_counter() - fixture_started

    record_count, status_seconds = _measure(lambda: sum(1 for _ in control.iter_records()))
    boundary, resolve_seconds = _measure(
        lambda: resolve_store(
            control,
            capabilities=CapabilityReport("ready", ()),
            task_id="TASK-BENCH-000001",
        )
    )
    fingerprint, fingerprint_seconds = _measure(
        lambda: build_fingerprint(
            [],
            repository={
                "provider": "filesystem_only",
                "root": "<BENCHMARK_ROOT>",
                "worktree": "<BENCHMARK_ROOT>",
                "git_common_dir": None,
                "branch": None,
                "revision": None,
                "status_porcelain": "",
            },
            control={"task_count": count, "task_hashes": task_hashes},
            resolver={"boundary": boundary.boundary, "reason_code": boundary.reason_code},
            validation={"required_validator_ids": [], "outcomes": []},
            checkpoint={"provider": "none", "status": "not_required", "revision": None},
            adapter_extensions={},
        )
    )
    index_receipt, index_seconds = _measure(lambda: generate_indexes(control))
    export_path, export_seconds = _measure(lambda: sqlite.export_json(suffix="benchmark"))

    before_export = sqlite.export_data()
    before_hash = content_sha256(before_export)
    before_counts = {name: len(rows) for name, rows in before_export["tables"].items()}
    database_bytes_before = sqlite.path.stat().st_size

    def compact() -> None:
        connection = sqlite.connect()
        try:
            connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            connection.execute("VACUUM")
        finally:
            connection.close()

    _, compact_seconds = _measure(compact)
    after_export = sqlite.export_data()
    after_hash = content_sha256(after_export)
    after_counts = {name: len(rows) for name, rows in after_export["tables"].items()}
    database_bytes_after = sqlite.path.stat().st_size

    metrics = {
        "status_scan": status_seconds,
        "resolve": resolve_seconds,
        "fingerprint": fingerprint_seconds,
        "index_regeneration": index_seconds,
        "goal_export": export_seconds,
        "database_compaction": compact_seconds,
    }
    budget_results = {
        name: {
            "seconds": round(value, 6),
            "budget_seconds": BUDGETS_SECONDS[name],
            "status": "pass" if value <= BUDGETS_SECONDS[name] else "fail",
        }
        for name, value in metrics.items()
    }
    semantics_preserved = before_hash == after_hash and before_counts == after_counts
    return {
        "schema_version": "sys4ai.governed-continuation-benchmark.v1",
        "status": "pass"
        if all(item["status"] == "pass" for item in budget_results.values())
        and semantics_preserved
        else "fail",
        "records_requested": count,
        "control_records_observed": record_count,
        "goal_receipts_observed": after_counts.get("step_receipts", 0),
        "goal_events_observed": after_counts.get("events", 0),
        "fixture_build_seconds": round(fixture_seconds, 6),
        "metrics": budget_results,
        "semantic_checks": {
            "resolver_boundary": boundary.boundary,
            "fingerprint": fingerprint.fingerprint,
            "index_status": index_receipt.status,
            "export_bytes": export_path.stat().st_size,
            "compaction_preserved_export_hash": before_hash == after_hash,
            "compaction_preserved_row_counts": before_counts == after_counts,
            "database_bytes_before": database_bytes_before,
            "database_bytes_after": database_bytes_after,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "implementation": platform.python_implementation(),
        },
        "execution_performed": False,
        "project_mutation_performed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=int, default=2000)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.records < 1000:
        parser.error("--records must be at least 1000 for the release scale benchmark")
    if args.workspace:
        args.workspace.mkdir(parents=True, exist_ok=True)
        report = run_benchmark(args.workspace.resolve(), args.records)
    else:
        with tempfile.TemporaryDirectory(prefix="governed-continuation-benchmark-") as directory:
            report = run_benchmark(Path(directory).resolve(), args.records)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
