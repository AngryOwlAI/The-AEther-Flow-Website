from __future__ import annotations

import copy
import multiprocessing as mp
import sqlite3
import tempfile
import unittest
from pathlib import Path

from _support import TS, valid_decision, valid_job, valid_role, valid_task
from agentjob_runtime.control.activation import activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import ActiveRelayError, StateConflict
from agentjob_runtime.goal.execution import claim_generation
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_successor
from test_generation_execution import claimable
from test_goal_leases import initialized
from test_successor_state import prepared


def _binding(root: str, common: str) -> dict:
    return {
        "project_id": Path(root).name,
        "root": root,
        "worktree": root,
        "branch": "main",
        "git_common_dir": common,
        "starting_revision": "abc123",
        "environment_mode": "local",
    }


def _initialize_worker(database, root, common, goal_id, token, start, results):
    start.wait(10)
    try:
        store = SQLiteGoalStore(database, auto_migrate=False)
        value = initialize_goal(
            store,
            goal_text=f"Finish {goal_id}.",
            completion_contract={
                "interpretation": "Finish the bounded work.",
                "required_evidence": ["Tests pass."],
                "user_confirmed_when_ambiguous": True,
            },
            guards={"max_continue_passes": 3, "deadline_at": "2099-01-01T00:00:00Z"},
            repository_binding=_binding(root, common),
            initial_fingerprint="a" * 64,
            authorization={"fresh_recursive_threads_explicitly_requested": True},
            goal_id=goal_id,
            timestamp=TS,
            launcher_token=token,
        )
        results.put(("won", value["goal_id"]))
    except (ActiveRelayError, StateConflict) as error:
        results.put(("lost", getattr(error, "code", type(error).__name__)))
    except Exception as error:
        results.put(("error", f"{type(error).__name__}: {error}"))


def _claim_worker(database, goal_id, token, start, results):
    start.wait(10)
    try:
        store = SQLiteGoalStore(database, auto_migrate=False)
        value = claim_generation(
            store,
            goal_id=goal_id,
            expected_revision=3,
            generation=1,
            handoff_token="h" * 48,
            idempotency_key=f"{goal_id}:1",
            successor_thread_id="succ",
            claim_token=token,
        )
        results.put(("won", value["state"]["revision"]))
    except StateConflict as error:
        results.put(("lost", error.code))
    except Exception as error:
        results.put(("error", f"{type(error).__name__}: {error}"))


def _successor_worker(database, goal_id, start, results):
    start.wait(10)
    try:
        store = SQLiteGoalStore(database, auto_migrate=False)
        value = record_successor(
            store,
            goal_id=goal_id,
            expected_revision=2,
            generation=1,
            handoff_token="h" * 48,
            successor_thread_id="successor",
            provider_id="test-fake",
            provider_response={"status": "created"},
        )
        results.put(("ok", value["state"]["revision"]))
    except StateConflict as error:
        results.put(("lost", error.code))
    except Exception as error:
        results.put(("error", f"{type(error).__name__}: {error}"))


def _packet(serial: int):
    decision = copy.deepcopy(valid_decision())
    job = copy.deepcopy(valid_job())
    role = copy.deepcopy(valid_role())
    decision_id = f"DDR-20260717-{serial:03d}"
    job_id = f"AJ-TASK-20260717-001-{serial:03d}"
    role_id = f"ER-{job_id}"
    decision["decision_id"] = decision_id
    decision["selected"]["agent_job_id"] = job_id
    job["job_id"] = job_id
    job["decision_id"] = decision_id
    job["concurrency"]["idempotency_key"] = job_id
    job["role_binding"]["execution_role_ref"] = (
        f".agents/control/tasks/TASK-20260717-001/roles/{role_id}.json"
    )
    role["execution_role_id"] = role_id
    role["job_id"] = job_id
    role["expires_after"] = job_id
    return decision, job, role


def _activation_worker(root, serial, start, results):
    start.wait(10)
    try:
        store = FilesystemControlStore(root, ".agents/control")
        decision, job, role = _packet(serial)
        receipt = activate_packet(
            store,
            task_id="TASK-20260717-001",
            decision=decision,
            job=job,
            execution_role=role,
            expected_revision=1,
        )
        results.put(("won", receipt.job_id))
    except StateConflict as error:
        results.put(("lost", error.code))
    except Exception as error:
        results.put(("error", f"{type(error).__name__}: {error}"))


def _hold_sqlite(database, ready, release):
    connection = sqlite3.connect(database, timeout=5)
    connection.execute("BEGIN IMMEDIATE")
    ready.set()
    release.wait(30)
    connection.rollback()
    connection.close()


def _hold_control_lock(root, ready, release):
    store = FilesystemControlStore(root, ".agents/control")
    with store.control_lock():
        ready.set()
        release.wait(30)


class MultiprocessConcurrencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.context = mp.get_context("spawn")

    def run_competitors(self, target, args_list):
        start = self.context.Event()
        results = self.context.Queue()
        processes = [
            self.context.Process(target=target, args=(*args, start, results))
            for args in args_list
        ]
        for process in processes:
            process.start()
        start.set()
        values = [results.get(timeout=15) for _ in processes]
        for process in processes:
            process.join(15)
            if process.is_alive():
                process.terminate()
                process.join(5)
            self.assertEqual(process.exitcode, 0)
        self.assertFalse(any(status == "error" for status, _ in values), values)
        return values

    def test_competing_initializers_in_one_worktree_have_exactly_one_winner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = str(Path(directory).resolve())
            database = str(Path(root) / "state.sqlite3")
            SQLiteGoalStore(database)
            values = self.run_competitors(
                _initialize_worker,
                [
                    (database, root, str(Path(root) / ".git"), "CG-20260717T150000Z-aaaa0001", "a" * 48),
                    (database, root, str(Path(root) / ".git"), "CG-20260717T150000Z-bbbb0002", "b" * 48),
                ],
            )
            self.assertCountEqual([status for status, _ in values], ["won", "lost"])
            self.assertEqual(len(SQLiteGoalStore(database, auto_migrate=False).list_goals()), 1)

    def test_different_worktrees_sharing_git_common_dir_follow_worktree_lease_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            worktree_a = base / "worktree-a"
            worktree_b = base / "worktree-b"
            worktree_a.mkdir()
            worktree_b.mkdir()
            common = str(base / "repository.git")
            database = str(base / "state.sqlite3")
            SQLiteGoalStore(database)
            values = self.run_competitors(
                _initialize_worker,
                [
                    (database, str(worktree_a), common, "CG-20260717T150000Z-aaaa0001", "a" * 48),
                    (database, str(worktree_b), common, "CG-20260717T150000Z-bbbb0002", "b" * 48),
                ],
            )
            self.assertEqual([status for status, _ in values].count("won"), 2)
            self.assertEqual(len(SQLiteGoalStore(database, auto_migrate=False).list_goals()), 2)

    def test_competing_claims_have_one_winner_and_no_partial_loser_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = claimable(directory)
            values = self.run_competitors(
                _claim_worker,
                [
                    (str(store.path), record["goal_id"], "x" * 48),
                    (str(store.path), record["goal_id"], "y" * 48),
                ],
            )
            self.assertCountEqual([status for status, _ in values], ["won", "lost"])
            final = store.load_goal(record["goal_id"])
            self.assertEqual(final["state"]["revision"], 4)
            self.assertEqual(final["state"]["phase"], "step_active")

    def test_competing_record_only_successor_writes_are_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, reserved = prepared(directory)
            values = self.run_competitors(
                _successor_worker,
                [
                    (str(store.path), reserved["goal_id"]),
                    (str(store.path), reserved["goal_id"]),
                ],
            )
            self.assertCountEqual([status for status, _ in values], ["ok", "lost"])
            self.assertEqual(
                store.query_one("SELECT COUNT(*) AS count FROM provider_receipts")["count"], 1
            )
            self.assertEqual(store.load_goal(reserved["goal_id"])["state"]["revision"], 3)
            replay = record_successor(
                store,
                goal_id=reserved["goal_id"],
                expected_revision=2,
                generation=1,
                handoff_token="h" * 48,
                successor_thread_id="successor",
                provider_id="test-fake",
                provider_response={"status": "created"},
            )
            self.assertEqual(replay["state"]["revision"], 3)

    def test_competing_task_activations_have_one_revision_winner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = FilesystemControlStore(root, ".agents/control")
            task = valid_task()
            task["current_decision_id"] = None
            task["current_job_id"] = None
            store.create_task(task)
            values = self.run_competitors(
                _activation_worker,
                [(str(root), 11), (str(root), 12)],
            )
            self.assertCountEqual([status for status, _ in values], ["won", "lost"])
            self.assertEqual(store.load_task(task["task_id"])["revision"], 2)
            self.assertEqual(
                sum(1 for kind, _, _ in store.iter_records() if kind == "activation"), 1
            )

    def test_busy_timeout_is_a_protocol_conflict_and_killed_sqlite_writer_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = initialized(directory)
            ready = self.context.Event()
            release = self.context.Event()
            holder = self.context.Process(target=_hold_sqlite, args=(str(store.path), ready, release))
            holder.start()
            self.assertTrue(ready.wait(10))
            busy_store = SQLiteGoalStore(
                store.path, auto_migrate=False, busy_timeout_ms=50
            )
            with self.assertRaises(StateConflict) as caught:
                with busy_store.mutation(record["goal_id"], expected_revision=1):
                    pass
            self.assertEqual(caught.exception.details["reason_code"], "state.sqlite_busy")
            self.assertEqual(store.load_goal(record["goal_id"])["state"]["revision"], 1)
            holder.terminate()
            holder.join(10)
            self.assertIsNotNone(holder.exitcode)
            with store.mutation(record["goal_id"], expected_revision=1) as mutation:
                mutation.event("post_termination", {"result": "lock released by SQLite"})
            self.assertEqual(store.load_goal(record["goal_id"])["state"]["revision"], 2)

    def test_killed_directory_lock_is_not_stolen_and_requires_explicit_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = FilesystemControlStore(root, ".agents/control")
            task = valid_task()
            task["current_decision_id"] = None
            task["current_job_id"] = None
            store.create_task(task)
            ready = self.context.Event()
            release = self.context.Event()
            holder = self.context.Process(target=_hold_control_lock, args=(str(root), ready, release))
            holder.start()
            self.assertTrue(ready.wait(10))
            holder.terminate()
            holder.join(10)
            decision, job, role = _packet(21)
            with self.assertRaises(StateConflict) as caught:
                activate_packet(
                    store,
                    task_id=task["task_id"],
                    decision=decision,
                    job=job,
                    execution_role=role,
                    expected_revision=1,
                )
            self.assertEqual(caught.exception.details["reason_code"], "state.control_lock_held")
            self.assertEqual(store.load_task(task["task_id"])["revision"], 1)
            lock = store.root / ".control.lock"
            self.assertTrue(lock.is_file())
            lock.unlink()
            receipt = activate_packet(
                store,
                task_id=task["task_id"],
                decision=decision,
                job=job,
                execution_role=role,
                expected_revision=1,
            )
            self.assertEqual(receipt.task_revision, 2)


if __name__ == "__main__":
    unittest.main()
