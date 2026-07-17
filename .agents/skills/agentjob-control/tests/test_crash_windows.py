from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from _support import TS, valid_completion, valid_decision, valid_handoff, valid_job, valid_role, valid_task
from agentjob_runtime.bootstrap import bootstrap_project
from agentjob_runtime.control.activation import InjectedActivationFault, activate_packet
from agentjob_runtime.control.completion import InjectedCompletionFault, write_completion
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.handoff import InjectedHandoffFault, write_handoff
from agentjob_runtime.errors import IntegrityError, StateConflict
from agentjob_runtime.goal.decide import decide_generation
from agentjob_runtime.goal.file_journal_store import FileJournalGoalStore
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.successor import InjectedSuccessorFault, record_successor, reserve_successor
from agentjob_runtime.goal.verify import verify_generation
from fault_injection import observe_control, observe_goal
from test_goal_leases import initialized
from test_goal_receipts import evidence, verifying
from test_successor_state import prepared


class CrashWindowTests(unittest.TestCase):
    def bootstrapped_store(self, directory: str):
        root = Path(directory).resolve()
        self.assertIn(bootstrap_project(root).status, {"initialized", "initialized_with_findings"})
        store = FilesystemControlStore(root, ".agents/control")
        task = valid_task()
        task["current_decision_id"] = None
        task["current_job_id"] = None
        store.create_task(task)
        return root, store, task

    @staticmethod
    def activate(store, task, *, fault_after=None):
        return activate_packet(
            store,
            task_id=task["task_id"],
            decision=valid_decision(),
            job=valid_job(),
            execution_role=valid_role(),
            expected_revision=1,
            fault_after=fault_after,
        )

    def test_all_activation_fault_boundaries_are_inspectable_and_never_duplicate_authority(self) -> None:
        before_manifest = {"staged", "director_decision", "agent_job", "execution_role"}
        retryable = {*before_manifest, "manifest"}
        for boundary in (
            "staged",
            "director_decision",
            "agent_job",
            "execution_role",
            "manifest",
            "task_pointer",
            "indexes",
        ):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as directory:
                root, store, task = self.bootstrapped_store(directory)
                with self.assertRaises(InjectedActivationFault):
                    self.activate(store, task, fault_after=boundary)
                observed = observe_control(root, store, task["task_id"])
                self.assertEqual(observed.doctor_status, "pass")
                if boundary in before_manifest:
                    self.assertNotIn(valid_job()["job_id"], observed.activated_ids)
                    self.assertEqual(observed.task_revision, 1)
                else:
                    self.assertIn(valid_job()["job_id"], observed.activated_ids)
                if boundary in retryable:
                    self.activate(store, task)
                else:
                    self.assertEqual(observed.task_revision, 2)
                    self.assertEqual(observed.boundary, "existing_agent_job_ready")
                    with self.assertRaises(StateConflict):
                        self.activate(store, task)
                final = observe_control(root, store, task["task_id"])
                self.assertEqual(final.record_counts.get("activation"), 1)
                self.assertEqual(final.record_counts.get("agent_job"), 1)
                self.assertEqual(final.boundary, "existing_agent_job_ready")

    def test_completion_faults_leave_one_completion_and_never_reoffer_the_job(self) -> None:
        for boundary in ("completion", "task_pointer", "indexes"):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as directory:
                root, store, task = self.bootstrapped_store(directory)
                self.activate(store, task)
                with self.assertRaises(InjectedCompletionFault):
                    write_completion(
                        store,
                        valid_completion(),
                        expected_revision=2,
                        close_task=False,
                        fault_after=boundary,
                    )
                observed = observe_control(root, store, task["task_id"])
                self.assertEqual(observed.doctor_status, "pass")
                self.assertEqual(observed.record_counts.get("completion"), 1)
                self.assertEqual(observed.boundary, "director_decision_required")
                self.assertEqual(
                    observed.reason_code, "job.completion_recorded_requires_next_decision"
                )
                with self.assertRaises((IntegrityError, StateConflict)):
                    write_completion(
                        store,
                        valid_completion(),
                        expected_revision=observed.task_revision,
                        close_task=False,
                    )

    def test_handoff_faults_preserve_non_authoritative_evidence_without_duplication(self) -> None:
        for boundary in ("handoff", "task_pointer"):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as directory:
                root, store, task = self.bootstrapped_store(directory)
                self.activate(store, task)
                write_completion(store, valid_completion(), expected_revision=2, close_task=False)
                with self.assertRaises(InjectedHandoffFault):
                    write_handoff(
                        store,
                        valid_handoff(),
                        expected_revision=3,
                        fault_after=boundary,
                    )
                observed = observe_control(root, store, task["task_id"])
                self.assertEqual(observed.doctor_status, "pass")
                self.assertEqual(observed.record_counts.get("handoff"), 1)
                self.assertEqual(observed.boundary, "director_decision_required")
                with self.assertRaises(IntegrityError):
                    write_handoff(
                        store,
                        valid_handoff(),
                        expected_revision=observed.task_revision,
                    )

    def test_provider_and_lease_faults_roll_back_then_record_only_retry_succeeds_once(self) -> None:
        for boundary in ("provider_receipt", "lease_transfer"):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as directory:
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
                with self.assertRaises(InjectedSuccessorFault):
                    record_successor(**values, fault_after=boundary)
                observed = observe_goal(store, reserved["goal_id"])
                self.assertEqual(observed.integrity_status, "pass")
                self.assertEqual(observed.revision, 2)
                self.assertEqual(observed.phase, "successor_intent")
                self.assertEqual(observed.provider_receipts, 0)
                record_successor(**values)
                final = observe_goal(store, reserved["goal_id"])
                self.assertEqual(final.provider_receipts, 1)
                self.assertEqual(final.phase, "successor_created")

    def test_prior_receipt_fault_rolls_back_both_receipt_and_successor_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory)
            verify_generation(
                store,
                goal_id=goal_id,
                expected_revision=6,
                generation=1,
                claim_token="c" * 48,
                continue_result=result,
                after_fingerprint=after,
                direct_evidence=evidence("fail"),
            )
            decide_generation(
                store,
                goal_id=goal_id,
                expected_revision=7,
                generation=1,
                claim_token="c" * 48,
                legal_route_available=True,
            )
            reserve_successor(
                store,
                goal_id=goal_id,
                expected_revision=8,
                current_holder_token="c" * 48,
                predecessor_thread_id="succ",
                handoff_token="n" * 48,
            )
            values = dict(
                store=store,
                goal_id=goal_id,
                expected_revision=9,
                generation=2,
                handoff_token="n" * 48,
                successor_thread_id="successor-2",
                provider_id="test-fake",
                provider_response={"status": "created"},
            )
            with self.assertRaises(InjectedSuccessorFault):
                record_successor(**values, fault_after="prior_receipt")
            observed = observe_goal(store, goal_id)
            self.assertEqual(observed.revision, 9)
            self.assertEqual(observed.step_receipts, 0)
            self.assertEqual(observed.provider_receipts, 1)
            record_successor(**values)
            final = observe_goal(store, goal_id)
            self.assertEqual(final.step_receipts, 1)
            self.assertEqual(final.provider_receipts, 2)

    def test_sqlite_mutation_exception_rolls_back_revision_and_journal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = initialized(directory)
            before = observe_goal(store, record["goal_id"])
            with self.assertRaises(RuntimeError):
                with store.mutation(record["goal_id"], expected_revision=1) as mutation:
                    mutation.event("will_rollback", {"evidence": "injected"})
                    mutation.record["state"]["phase"] = "successor_intent"
                    raise RuntimeError("injected transaction failure")
            after = observe_goal(store, record["goal_id"])
            self.assertEqual(after, before)

    def test_atomic_replace_failure_keeps_prior_files_and_removes_temporary_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = FilesystemControlStore(root, ".agents/control")
            task = valid_task()
            store.create_task(task)
            before = store.task_path(task["task_id"]).read_bytes()
            with patch(
                "agentjob_runtime.control.filesystem_store.os.replace",
                side_effect=OSError("injected replace failure"),
            ):
                with self.assertRaises(OSError):
                    store.update_task_pointers(task["task_id"], expected_revision=1, status="blocked")
            self.assertEqual(store.task_path(task["task_id"]).read_bytes(), before)
            self.assertFalse(list(store.task_path(task["task_id"]).parent.glob("*.tmp")))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            journal = FileJournalGoalStore(root / "journal")
            goal = initialize_goal(
                journal,
                goal_text="Preserve atomic state.",
                completion_contract={
                    "interpretation": "The mutation remains atomic.",
                    "required_evidence": ["State is readable."],
                    "user_confirmed_when_ambiguous": True,
                },
                guards={"max_continue_passes": 2, "deadline_at": "2099-01-01T00:00:00Z"},
                repository_binding={
                    "project_id": "atomic-fixture",
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
                timestamp=TS,
                launcher_token="l" * 48,
            )
            before = copy.deepcopy(goal)
            with patch(
                "agentjob_runtime.goal.file_journal_store.os.replace",
                side_effect=OSError("injected replace failure"),
            ):
                with self.assertRaises(OSError):
                    with journal.mutation(goal["goal_id"], expected_revision=1) as mutation:
                        mutation.event("will_rollback", {"evidence": "injected"})
            self.assertEqual(journal.load_goal(goal["goal_id"]), before)
            self.assertFalse(list((root / "journal").glob("*.tmp")))


if __name__ == "__main__":
    unittest.main()
