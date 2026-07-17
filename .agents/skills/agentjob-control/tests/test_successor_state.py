from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import StateConflict
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_dispatch_outcome, record_successor, reserve_successor


def prepared(directory: str):
    root = Path(directory).resolve()
    store = SQLiteGoalStore(root / "state.sqlite3")
    goal = initialize_goal(
        store,
        goal_text="Finish.",
        completion_contract={
            "interpretation": "Finish means verified.",
            "required_evidence": ["Evidence exists."],
            "user_confirmed_when_ambiguous": True,
        },
        guards={"max_continue_passes": 3, "deadline_at": "2099-01-01T00:00:00Z"},
        repository_binding={
            "project_id": "example", "root": str(root), "worktree": str(root),
            "branch": "main", "git_common_dir": str(root / ".git"),
            "starting_revision": "abc", "environment_mode": "local",
        },
        initial_fingerprint="a" * 64,
        authorization={"fresh_recursive_threads_explicitly_requested": True},
        goal_id="CG-20260717T150000Z-abcdef12",
        timestamp="2026-07-17T15:00:00Z",
        launcher_token="l" * 48,
    )
    reserved = reserve_successor(
        store,
        goal_id=goal["goal_id"],
        expected_revision=1,
        current_holder_token="l" * 48,
        predecessor_thread_id="thread-predecessor",
        handoff_token="h" * 48,
        timestamp="2026-07-17T15:00:01Z",
    )
    return store, reserved


class SuccessorStateTests(unittest.TestCase):
    def test_reservation_precedes_provider_record_and_key_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = prepared(directory)
            generation = record["generations"]["1"]
            self.assertEqual(generation["idempotency_key"], f"{record['goal_id']}:1")
            intent = store.query_one(
                "SELECT * FROM successor_intents WHERE goal_id=? AND generation=1",
                (record["goal_id"],),
            )
            self.assertEqual(intent["provider_state"], "intent")
            self.assertEqual(intent["predecessor_thread_id"], "thread-predecessor")

    def test_record_only_retry_is_idempotent_and_conflicting_identity_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, reserved = prepared(directory)
            values = dict(
                store=store,
                goal_id=reserved["goal_id"],
                expected_revision=2,
                generation=1,
                handoff_token="h" * 48,
                successor_thread_id="thread-successor",
                provider_id="test-fake",
                provider_response={"status": "created"},
                timestamp="2026-07-17T15:00:02Z",
            )
            recorded = record_successor(**values)
            retried = record_successor(**values)
            self.assertEqual(retried, recorded)
            self.assertEqual(
                store.query_one("SELECT COUNT(*) AS count FROM provider_receipts")["count"], 1
            )
            with self.assertRaises(StateConflict):
                record_successor(**{**values, "expected_revision": 3, "successor_thread_id": "other"})

    def test_ambiguous_provider_outcome_quarantines_without_new_intent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, reserved = prepared(directory)
            result = record_dispatch_outcome(
                store,
                goal_id=reserved["goal_id"],
                expected_revision=2,
                generation=1,
                handoff_token="h" * 48,
                provider_id="test-fake",
                outcome="ambiguous",
                diagnostic={"reason": "transport ended after submit"},
                timestamp="2026-07-17T15:00:02Z",
            )
            self.assertEqual(result["state"]["phase"], "terminal_handoff_ambiguous")
            self.assertEqual(result["state"]["active_lease"]["holder_kind"], "quarantined")
            self.assertEqual(len(result["generations"]), 1)


if __name__ == "__main__":
    unittest.main()
