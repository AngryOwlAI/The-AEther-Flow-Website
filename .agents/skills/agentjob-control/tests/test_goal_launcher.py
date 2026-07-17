from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, TS
from agentjob_runtime.errors import RecordValidationError
from agentjob_runtime.goal.launcher import ThreadCreateResult, launch_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.records.canonical import content_sha256


CAPABILITIES = {
    "agentjob_control": True,
    "goal_state": True,
    "continuation_envelope": True,
    "repository_provider": True,
    "thread_provider": True,
}


class FakeThreadProvider:
    provider_id = "test-fake"
    available = True

    def __init__(self, result=None, *, raise_error=False):
        self.result = result or ThreadCreateResult(
            "returned", "thread-generation-1", {"provider_request_id": "request-1"}
        )
        self.raise_error = raise_error
        self.calls = []

    def create_thread(self, *, prompt, envelope, idempotency_key):
        self.calls.append(
            {"prompt": prompt, "envelope": envelope, "idempotency_key": idempotency_key}
        )
        if self.raise_error:
            raise RuntimeError("unknown provider boundary")
        return self.result


class GoalLauncherTests(unittest.TestCase):
    def inputs(self, root: Path):
        binding = {
            "project_id": "launcher-fixture",
            "root": str(root),
            "worktree": str(root),
            "branch": "main",
            "git_common_dir": None,
            "starting_revision": "abc123",
            "environment_mode": "local",
        }
        return {
            "goal_text": "Complete the bounded launcher fixture.",
            "completion_contract": {
                "interpretation": "The fixture is complete when its required check passes.",
                "required_evidence": ["The required fixture check passes."],
                "user_confirmed_when_ambiguous": False,
            },
            "guards": {
                "max_continue_passes": 4,
                "deadline_at": "2099-01-01T00:00:00Z",
            },
            "repository_binding": binding,
            "repository_observation": dict(binding),
            "initial_fingerprint": HASH_A,
            "authorization": {"fresh_recursive_threads_explicitly_requested": True},
            "capabilities": CAPABILITIES,
            "predecessor_thread_id": "thread-launcher",
            "canonical_state": {
                "fingerprint": HASH_A,
                "active_task_id": None,
                "current_decision_id": None,
                "current_job_id": None,
            },
            "progress_summary": "The goal was initialized; project work has not started.",
            "remaining_work": "Run a bounded continuation and evaluate the contract.",
            "goal_id": "CG-20260717T150000Z-a1b2c3d4",
            "timestamp": TS,
            "launcher_token": "l" * 48,
            "handoff_token": "h" * 48,
        }

    def test_success_dispatches_exactly_once_and_executes_no_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / ".local/state/goal.db")
            provider = FakeThreadProvider()
            summary = launch_goal(store, provider=provider, **self.inputs(root))
            self.assertEqual(summary.status, "dispatched")
            self.assertEqual(summary.provider_create_calls, 1)
            self.assertEqual(len(provider.calls), 1)
            self.assertEqual(summary.agentjobs_executed, 0)
            self.assertEqual(summary.continue_invocations, 0)
            self.assertEqual(summary.state_revision, 3)
            self.assertEqual(summary.state_phase, "successor_created")
            self.assertEqual(summary.lease_holder_kind, "successor_reserved")
            envelope = provider.calls[0]["envelope"]
            self.assertEqual(summary.envelope_sha256, content_sha256(envelope))
            self.assertIn("expected_revision: 3", provider.calls[0]["prompt"])
            self.assertNotIn("h" * 48, str(summary.as_dict()))
            record = store.load_goal(summary.goal_id)
            self.assertEqual(
                record["handoff"]["successor_thread_id"], "thread-generation-1"
            )

    def test_missing_capability_or_repository_mismatch_prevents_initialization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / ".local/state/goal.db")
            provider = FakeThreadProvider()
            values = self.inputs(root)
            values["capabilities"] = {**CAPABILITIES, "thread_provider": False}
            with self.assertRaises(RecordValidationError):
                launch_goal(store, provider=provider, **values)
            self.assertEqual(store.list_goals(), [])
            self.assertEqual(provider.calls, [])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / ".local/state/goal.db")
            provider = FakeThreadProvider()
            values = self.inputs(root)
            values["repository_observation"]["starting_revision"] = "different"
            with self.assertRaises(RecordValidationError):
                launch_goal(store, provider=provider, **values)
            self.assertEqual(store.list_goals(), [])

    def test_secret_validation_happens_before_provider_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / ".local/state/goal.db")
            provider = FakeThreadProvider()
            values = self.inputs(root)
            values["goal_text"] = "Use api_key=super-secret-value-1234567890 to finish."
            with self.assertRaises(RecordValidationError):
                launch_goal(store, provider=provider, **values)
            self.assertEqual(provider.calls, [])
            self.assertEqual(store.list_goals(), [])

    def test_ambiguous_provider_exception_is_recorded_once_and_quarantined(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / ".local/state/goal.db")
            provider = FakeThreadProvider(raise_error=True)
            summary = launch_goal(store, provider=provider, **self.inputs(root))
            self.assertEqual(len(provider.calls), 1)
            self.assertEqual(summary.status, "ambiguous")
            self.assertEqual(summary.state_phase, "terminal_handoff_ambiguous")
            self.assertEqual(summary.lease_holder_kind, "quarantined")

    def test_predecessor_reuse_is_duplicate_not_a_generation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / ".local/state/goal.db")
            provider = FakeThreadProvider(
                ThreadCreateResult("returned", "thread-launcher", {"request": "same-thread"})
            )
            summary = launch_goal(store, provider=provider, **self.inputs(root))
            self.assertEqual(summary.status, "duplicate")
            self.assertEqual(summary.state_phase, "terminal_duplicate_detected")
            self.assertEqual(summary.agentjobs_executed, 0)


if __name__ == "__main__":
    unittest.main()
