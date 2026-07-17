from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from _support import PACKAGE_ROOT, RUNTIME_SCRIPTS
from agentjob_runtime.errors import IntegrityError, StateConflict
from agentjob_runtime.fingerprinting.canonical import build_fingerprint
from agentjob_runtime.goal.decide import decide_generation
from agentjob_runtime.goal.execution import (
    claim_generation,
    consume_invocation,
    record_invocation_returned,
)
from agentjob_runtime.goal.file_journal_store import FileJournalGoalStore, render_goal
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.locking import CrossPlatformFileLock
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_successor, reserve_successor
from agentjob_runtime.goal.verify import verify_generation
from test_goal_receipts import continue_result, evidence, fingerprint_parts


class FileJournalStoreTests(unittest.TestCase):
    def initialize(self, store, root: Path):
        initial = build_fingerprint([], **fingerprint_parts("A"))
        goal = initialize_goal(
            store,
            goal_text="Portable file-backed goal.",
            completion_contract={
                "interpretation": "Canonical evidence proves completion.",
                "required_evidence": ["Tests pass."],
                "user_confirmed_when_ambiguous": True,
            },
            guards={"max_continue_passes": 2, "deadline_at": "2099-01-01T00:00:00Z"},
            repository_binding={
                "project_id": "example", "root": str(root), "worktree": str(root),
                "branch": "main", "git_common_dir": str(root / ".git"),
                "starting_revision": "A", "environment_mode": "local",
            },
            initial_fingerprint=initial.fingerprint,
            authorization={"fresh_recursive_threads_explicitly_requested": True},
            goal_id="CG-20260717T150000Z-abcdef12",
            timestamp="2026-07-17T15:00:00Z",
            launcher_token="l" * 48,
        )
        return goal, initial

    def run_contract(self, store, root: Path):
        goal, initial = self.initialize(store, root)
        reserve_successor(
            store, goal_id=goal["goal_id"], expected_revision=1,
            current_holder_token="l" * 48, predecessor_thread_id="pred",
            handoff_token="h" * 48,
        )
        record_successor(
            store, goal_id=goal["goal_id"], expected_revision=2, generation=1,
            handoff_token="h" * 48, successor_thread_id="succ", provider_id="fake",
            provider_response={"status": "created"},
        )
        claim_generation(
            store, goal_id=goal["goal_id"], expected_revision=3, generation=1,
            handoff_token="h" * 48, idempotency_key=f"{goal['goal_id']}:1",
            successor_thread_id="succ", claim_token="c" * 48,
        )
        consume_invocation(
            store, goal_id=goal["goal_id"], expected_revision=4, generation=1,
            claim_token="c" * 48,
        )
        after = build_fingerprint([initial.fingerprint], **fingerprint_parts("B"))
        result = continue_result(initial.fingerprint, after.fingerprint)
        record_invocation_returned(
            store, goal_id=goal["goal_id"], expected_revision=5, generation=1,
            claim_token="c" * 48, continue_result=result,
        )
        verify_generation(
            store, goal_id=goal["goal_id"], expected_revision=6, generation=1,
            claim_token="c" * 48, continue_result=result,
            after_fingerprint=after, direct_evidence=evidence("pass"),
        )
        return decide_generation(
            store, goal_id=goal["goal_id"], expected_revision=7, generation=1,
            claim_token="c" * 48, legal_route_available=False,
        )

    def test_file_and_sqlite_backends_pass_same_state_machine_contract(self) -> None:
        for backend in ("sqlite", "file"):
            with self.subTest(backend=backend), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                store = (
                    SQLiteGoalStore(root / "state.sqlite3")
                    if backend == "sqlite"
                    else FileJournalGoalStore(root / "goals", lock_backend="directory")
                )
                terminal = self.run_contract(store, root)
                self.assertEqual(terminal["state"]["phase"], "terminal_complete")
                self.assertEqual(terminal["state"]["passes_consumed"], 1)
                self.assertIsNotNone(terminal["generations"]["1"]["finalized_receipt_hash"])

    def test_rendering_is_deterministic_and_hash_linked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = FileJournalGoalStore(root / "goals", lock_backend="directory")
            goal, _ = self.initialize(store, root)
            path = store.root / f"goal-{goal['goal_id']}.md"
            before = path.read_bytes()
            loaded = store.load_goal(goal["goal_id"])
            self.assertEqual(before, render_goal(loaded).encode("utf-8"))
            self.assertEqual(loaded["journal"][0]["prior_hash"], None)

    def test_directory_lock_reports_contention_without_stealing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lock_path = Path(directory) / "state.lock"
            with CrossPlatformFileLock(lock_path, backend="directory"):
                with self.assertRaises(StateConflict):
                    with CrossPlatformFileLock(
                        lock_path, backend="directory", timeout_seconds=0.02
                    ):
                        pass
                self.assertTrue(lock_path.with_name("state.lock.lockdir").is_dir())

    def test_auto_lock_selects_and_operates_a_supported_platform_backend(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lock = CrossPlatformFileLock(Path(directory) / "auto.lock", backend="auto")
            self.assertIn(lock.backend, {"posix", "windows", "directory"})
            with lock:
                self.assertTrue((Path(directory) / "auto.lock").exists() or lock.backend == "directory")

    def test_symlink_hardlink_and_lease_mismatch_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = FileJournalGoalStore(root / "goals", lock_backend="directory")
            goal, _ = self.initialize(store, root)
            path = store.root / f"goal-{goal['goal_id']}.md"
            alias = store.root / "alias.md"
            os.link(path, alias)
            with self.assertRaises(IntegrityError):
                store.load_goal(goal["goal_id"])
            alias.unlink()
            lease = json.loads(store.global_lease_path.read_text(encoding="utf-8"))
            lease["holder_token"] = "tampered"
            store.global_lease_path.write_text(json.dumps(lease) + "\n", encoding="utf-8")
            with self.assertRaises(IntegrityError) as caught:
                store.load_goal(goal["goal_id"])
            self.assertTrue(caught.exception.details["recovery_required"])

    def test_legacy_aether_record_is_read_without_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = FileJournalGoalStore(root / "goals", lock_backend="directory")
            record = json.loads(
                (PACKAGE_ROOT / "tests/fixtures/aether/legacy-goal-v1.json").read_text(
                    encoding="utf-8"
                )
            )
            path = store.root / f"goal-{record['goal_id']}.md"
            from agentjob_runtime.compat.aether_goal_v1 import render_legacy_goal

            path.write_text(render_legacy_goal(record), encoding="utf-8")
            before = path.read_bytes()
            loaded = store.read_legacy_aether(path)
            self.assertTrue(loaded["legacy"])
            self.assertTrue(loaded["read_only"])
            self.assertEqual(before, path.read_bytes())


if __name__ == "__main__":
    unittest.main()
