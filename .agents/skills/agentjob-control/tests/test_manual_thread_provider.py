from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, TS
from agentjob_runtime.adapters.thread_manual import (
    ManualThreadProvider,
    adopt_manual_successor,
)
from agentjob_runtime.errors import SecurityError, StateConflict
from agentjob_runtime.goal.launcher import launch_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


CAPABILITIES = {
    "agentjob_control": True,
    "goal_state": True,
    "continuation_envelope": True,
    "repository_provider": True,
    "thread_provider": True,
}


class ManualThreadProviderTests(unittest.TestCase):
    def launch(self, root: Path):
        store = SQLiteGoalStore(root / ".local/state/goal.db")
        binding = {
            "project_id": "manual-fixture",
            "root": str(root),
            "worktree": str(root),
            "branch": "main",
            "git_common_dir": None,
            "starting_revision": "A",
            "environment_mode": "local",
        }
        provider = ManualThreadProvider(
            root,
            local_root=".local/manual",
            current_thread_id="thread-launcher",
            timestamp=TS,
        )
        summary = launch_goal(
            store,
            goal_text="Complete the manual handoff fixture.",
            completion_contract={
                "interpretation": "The fixture is complete when its check passes.",
                "required_evidence": ["The fixture check passes."],
                "user_confirmed_when_ambiguous": True,
            },
            guards={
                "max_continue_passes": 3,
                "deadline_at": "2099-01-01T00:00:00Z",
            },
            repository_binding=binding,
            repository_observation=dict(binding),
            initial_fingerprint=HASH_A,
            authorization={"fresh_recursive_threads_explicitly_requested": True},
            capabilities=CAPABILITIES,
            provider=provider,
            predecessor_thread_id="thread-launcher",
            canonical_state={
                "fingerprint": HASH_A,
                "active_task_id": None,
                "current_decision_id": None,
                "current_job_id": None,
            },
            progress_summary="The relay was initialized.",
            remaining_work="Open a fresh thread and adopt generation 1.",
            goal_id="CG-20260717T150000Z-11223344",
            timestamp=TS,
            launcher_token="l" * 48,
            handoff_token="h" * 48,
        )
        return store, provider, summary

    def test_manual_launch_writes_exact_artifacts_without_app_server(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store, _, summary = self.launch(root)
            self.assertEqual(summary.status, "manual_handoff_pending")
            self.assertEqual(summary.state_phase, "successor_intent")
            self.assertEqual(summary.state_revision, 2)
            self.assertIsNone(summary.successor_thread_id)
            envelope_path = root / summary.manual_handoff_path
            prompt_path = envelope_path.parent / "new-thread-prompt.txt"
            receipt_path = envelope_path.parent / "provider-receipt.json"
            self.assertTrue(envelope_path.is_file())
            self.assertTrue(prompt_path.is_file())
            self.assertTrue(receipt_path.is_file())
            self.assertIn("continue-implementing-goal", prompt_path.read_text(encoding="utf-8"))
            self.assertIn("expected_revision: 3", prompt_path.read_text(encoding="utf-8"))
            self.assertNotIn("h" * 48, receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(store.load_goal(summary.goal_id)["state"]["phase"], "successor_intent")

    def test_explicit_adoption_requires_token_generation_and_fresh_thread(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store, _, summary = self.launch(root)
            with self.assertRaises(StateConflict):
                adopt_manual_successor(
                    store,
                    project_root=root,
                    local_root=".local/manual",
                    goal_id=summary.goal_id,
                    expected_revision=2,
                    generation=1,
                    handoff_token="x" * 48,
                    envelope_sha256=summary.envelope_sha256,
                    successor_thread_id="thread-generation-1",
                    timestamp=TS,
                )
            with self.assertRaises(StateConflict):
                adopt_manual_successor(
                    store,
                    project_root=root,
                    local_root=".local/manual",
                    goal_id=summary.goal_id,
                    expected_revision=2,
                    generation=1,
                    handoff_token="h" * 48,
                    envelope_sha256=summary.envelope_sha256,
                    successor_thread_id="thread-launcher",
                    timestamp=TS,
                )
            adopted = adopt_manual_successor(
                store,
                project_root=root,
                local_root=".local/manual",
                goal_id=summary.goal_id,
                expected_revision=2,
                generation=1,
                handoff_token="h" * 48,
                envelope_sha256=summary.envelope_sha256,
                successor_thread_id="thread-generation-1",
                timestamp=TS,
            )
            self.assertEqual(adopted["state"]["phase"], "successor_created")
            self.assertEqual(adopted["state"]["revision"], 3)
            self.assertEqual(adopted["handoff"]["successor_thread_id"], "thread-generation-1")
            self.assertEqual(adopted["state"]["active_lease"]["holder_kind"], "successor_reserved")

    def test_adoption_is_idempotent_for_same_identity_and_rejects_second_successor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store, _, summary = self.launch(root)
            arguments = {
                "project_root": root,
                "local_root": ".local/manual",
                "goal_id": summary.goal_id,
                "expected_revision": 2,
                "generation": 1,
                "handoff_token": "h" * 48,
                "envelope_sha256": summary.envelope_sha256,
                "successor_thread_id": "thread-generation-1",
                "timestamp": TS,
            }
            first = adopt_manual_successor(store, **arguments)
            second = adopt_manual_successor(store, **arguments)
            self.assertEqual(first["state"]["revision"], second["state"]["revision"])
            with self.assertRaises(StateConflict):
                adopt_manual_successor(
                    store,
                    **{**arguments, "successor_thread_id": "thread-generation-other"},
                )

    def test_manual_state_root_rejects_installed_or_symlink_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with self.assertRaises(SecurityError):
                ManualThreadProvider(root, local_root="skills/manual")
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory).resolve()
            (root / ".local").mkdir()
            (root / ".local/manual").symlink_to(Path(outside))
            with self.assertRaises(SecurityError):
                ManualThreadProvider(root, local_root=".local/manual")


if __name__ == "__main__":
    unittest.main()
