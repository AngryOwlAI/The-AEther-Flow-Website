from __future__ import annotations

import tempfile
import threading
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import StateConflict
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.leases import heartbeat_lease, lease_diagnostics, transfer_lease
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


NOW = "2026-07-17T15:00:00Z"


def initialized(directory: str):
    root = Path(directory).resolve()
    store = SQLiteGoalStore(root / "state.sqlite3")
    record = initialize_goal(
        store,
        goal_text="Finish the bounded work.",
        completion_contract={
            "interpretation": "The bounded work is proved complete.",
            "required_evidence": ["Tests pass."],
            "user_confirmed_when_ambiguous": True,
        },
        guards={"max_continue_passes": 3, "deadline_at": "2099-01-01T00:00:00Z"},
        repository_binding={
            "project_id": "example-project",
            "root": str(root),
            "worktree": str(root),
            "branch": "main",
            "git_common_dir": str(root / ".git"),
            "starting_revision": "abc123",
            "environment_mode": "local",
        },
        initial_fingerprint="a" * 64,
        authorization={"fresh_recursive_threads_explicitly_requested": True},
        goal_id="CG-20260717T150000Z-abcdef12",
        timestamp=NOW,
        launcher_token="l" * 48,
    )
    return store, record


class GoalLeaseTests(unittest.TestCase):
    def test_transfer_and_heartbeat_require_revision_and_holder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = initialized(directory)
            transferred = transfer_lease(
                store,
                goal_id=record["goal_id"],
                expected_revision=1,
                current_holder_token="l" * 48,
                generation=1,
                holder_kind="successor_reserved",
                holder_token="s" * 48,
                timestamp="2026-07-17T15:00:01Z",
            )
            self.assertEqual(transferred["state"]["revision"], 2)
            with self.assertRaises(StateConflict):
                heartbeat_lease(
                    store,
                    goal_id=record["goal_id"],
                    expected_revision=1,
                    holder_token="s" * 48,
                )
            unchanged = store.load_goal(record["goal_id"])
            self.assertEqual(unchanged["state"]["revision"], 2)
            heartbeat = heartbeat_lease(
                store,
                goal_id=record["goal_id"],
                expected_revision=2,
                holder_token="s" * 48,
                timestamp="2026-07-17T15:01:00Z",
            )
            self.assertEqual(heartbeat["state"]["active_lease"]["heartbeat_at"], "2026-07-17T15:01:00Z")

    def test_expiry_is_diagnostic_and_does_not_authorize_stealing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = initialized(directory)
            diagnostic = lease_diagnostics(
                store, record["goal_id"], timestamp="2026-07-17T16:00:00Z"
            )
            self.assertTrue(diagnostic["expired"])
            self.assertFalse(diagnostic["steal_authorized"])
            with self.assertRaises(StateConflict):
                transfer_lease(
                    store,
                    goal_id=record["goal_id"],
                    expected_revision=1,
                    current_holder_token="wrong-token",
                    generation=1,
                    holder_kind="continuation",
                )

    def test_competing_revision_checked_transfers_have_one_winner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = initialized(directory)
            barrier = threading.Barrier(2)
            outcomes: list[str] = []

            def compete(token: str) -> None:
                barrier.wait()
                try:
                    transfer_lease(
                        store,
                        goal_id=record["goal_id"],
                        expected_revision=1,
                        current_holder_token="l" * 48,
                        generation=1,
                        holder_kind="successor_reserved",
                        holder_token=token,
                    )
                    outcomes.append("won")
                except StateConflict:
                    outcomes.append("lost")

            threads = [threading.Thread(target=compete, args=(character * 48,)) for character in ("x", "y")]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertCountEqual(outcomes, ["won", "lost"])
            self.assertEqual(store.load_goal(record["goal_id"])["state"]["revision"], 2)


if __name__ == "__main__":
    unittest.main()
