from __future__ import annotations

import tempfile
import threading
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import GuardStop, StateConflict
from agentjob_runtime.goal.execution import (
    claim_generation,
    consume_invocation,
    pre_execution_stop,
    record_invocation_returned,
    record_invocation_unknown,
)
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_successor, reserve_successor


def claimable(directory: str):
    root = Path(directory).resolve()
    store = SQLiteGoalStore(root / "state.sqlite3")
    goal = initialize_goal(
        store,
        goal_text="Finish.",
        completion_contract={
            "interpretation": "Verified finish.", "required_evidence": ["Tests pass."],
            "user_confirmed_when_ambiguous": True,
        },
        guards={"max_continue_passes": 2, "deadline_at": "2099-01-01T00:00:00Z"},
        repository_binding={
            "project_id": "example", "root": str(root), "worktree": str(root),
            "branch": "main", "git_common_dir": str(root / ".git"),
            "starting_revision": "abc", "environment_mode": "local",
        },
        initial_fingerprint="a" * 64,
        authorization={"fresh_recursive_threads_explicitly_requested": True},
        goal_id="CG-20260717T150000Z-abcdef12", timestamp="2026-07-17T15:00:00Z",
        launcher_token="l" * 48,
    )
    reserved = reserve_successor(
        store, goal_id=goal["goal_id"], expected_revision=1,
        current_holder_token="l" * 48, predecessor_thread_id="pred",
        handoff_token="h" * 48, timestamp="2026-07-17T15:00:01Z",
    )
    created = record_successor(
        store, goal_id=goal["goal_id"], expected_revision=2, generation=1,
        handoff_token="h" * 48, successor_thread_id="succ", provider_id="fake",
        provider_response={"status": "created"}, timestamp="2026-07-17T15:00:02Z",
    )
    return store, created


class GenerationExecutionTests(unittest.TestCase):
    def test_competing_claims_have_one_winner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = claimable(directory)
            barrier = threading.Barrier(2)
            outcomes: list[str] = []

            def claim(token: str):
                barrier.wait()
                try:
                    claim_generation(
                        store, goal_id=record["goal_id"], expected_revision=3, generation=1,
                        handoff_token="h" * 48, idempotency_key=f"{record['goal_id']}:1",
                        successor_thread_id="succ", claim_token=token,
                    )
                    outcomes.append("won")
                except StateConflict:
                    outcomes.append("lost")

            threads = [threading.Thread(target=claim, args=(c * 48,)) for c in ("x", "y")]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertCountEqual(outcomes, ["won", "lost"])

    def test_consumption_is_irreversible_and_pass_count_increments_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = claimable(directory)
            claimed = claim_generation(
                store, goal_id=record["goal_id"], expected_revision=3, generation=1,
                handoff_token="h" * 48, idempotency_key=f"{record['goal_id']}:1",
                successor_thread_id="succ", claim_token="c" * 48,
                timestamp="2026-07-17T15:00:03Z",
            )
            consumed = consume_invocation(
                store, goal_id=record["goal_id"], expected_revision=4, generation=1,
                claim_token="c" * 48, timestamp="2026-07-17T15:00:04Z",
            )
            self.assertEqual(consumed["state"]["passes_consumed"], 1)
            with self.assertRaises(StateConflict):
                consume_invocation(
                    store, goal_id=record["goal_id"], expected_revision=5, generation=1,
                    claim_token="c" * 48,
                )
            self.assertEqual(store.load_goal(record["goal_id"])["state"]["passes_consumed"], 1)

    def test_guard_stop_does_not_consume_and_zero_receipt_is_finalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = claimable(directory)
            claim_generation(
                store, goal_id=record["goal_id"], expected_revision=3, generation=1,
                handoff_token="h" * 48, idempotency_key=f"{record['goal_id']}:1",
                successor_thread_id="succ", claim_token="c" * 48,
                timestamp="2026-07-17T15:00:03Z",
            )
            with self.assertRaises(GuardStop):
                consume_invocation(
                    store, goal_id=record["goal_id"], expected_revision=4, generation=1,
                    claim_token="c" * 48, observations={"human_gate_clear": False},
                    timestamp="2026-07-17T15:00:04Z",
                )
            stopped = pre_execution_stop(
                store, goal_id=record["goal_id"], expected_revision=4, generation=1,
                claim_token="c" * 48, stop_reason="human_gate",
                timestamp="2026-07-17T15:00:05Z",
            )
            self.assertEqual(stopped["state"]["passes_consumed"], 0)
            receipt = store.query_one("SELECT * FROM step_receipts WHERE goal_id=?", (record["goal_id"],))
            self.assertIsNotNone(receipt)

    def test_unknown_invocation_cannot_be_returned_or_reconsumed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = claimable(directory)
            claim_generation(
                store, goal_id=record["goal_id"], expected_revision=3, generation=1,
                handoff_token="h" * 48, idempotency_key=f"{record['goal_id']}:1",
                successor_thread_id="succ", claim_token="c" * 48,
            )
            consume_invocation(
                store, goal_id=record["goal_id"], expected_revision=4, generation=1,
                claim_token="c" * 48,
            )
            unknown = record_invocation_unknown(
                store, goal_id=record["goal_id"], expected_revision=5, generation=1,
                claim_token="c" * 48, diagnostic={"reason": "uncertain boundary"},
            )
            self.assertEqual(unknown["generations"]["1"]["invocation_state"], "unknown")
            with self.assertRaises(StateConflict):
                record_invocation_returned(
                    store, goal_id=record["goal_id"], expected_revision=6, generation=1,
                    claim_token="c" * 48, continue_result={"status": "completed"},
                )


if __name__ == "__main__":
    unittest.main()
