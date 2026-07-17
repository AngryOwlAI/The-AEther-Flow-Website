from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, HASH_B, TS
from agentjob_runtime.errors import StateConflict
from agentjob_runtime.goal.launcher import ThreadCreateResult, launch_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.worker import WorkerBudget, run_goal_worker
from agentjob_runtime.records.canonical import content_sha256


CAPABILITIES = {
    "agentjob_control": True,
    "goal_state": True,
    "continuation_envelope": True,
    "repository_provider": True,
    "thread_provider": True,
}


class FakeProvider:
    provider_id = "test-fake"
    available = True

    def __init__(self, thread_id, *, raise_error=False):
        self.thread_id = thread_id
        self.raise_error = raise_error
        self.calls = []

    def create_thread(self, *, prompt, envelope, idempotency_key):
        self.calls.append(
            {"prompt": prompt, "envelope": envelope, "idempotency_key": idempotency_key}
        )
        if self.raise_error:
            raise RuntimeError("ambiguous provider boundary")
        return ThreadCreateResult(
            "returned", self.thread_id, {"provider_request_id": f"request-{len(self.calls)}"}
        )


class CountingContinue:
    def __init__(self, result=None, *, raise_error=False):
        self.result = result
        self.raise_error = raise_error
        self.calls = 0

    def __call__(self, envelope):
        self.calls += 1
        if self.raise_error:
            raise RuntimeError("unknown continue outcome")
        return copy.deepcopy(self.result)


class GoalWorkerTests(unittest.TestCase):
    def launched(self, directory: str):
        root = Path(directory).resolve()
        store = SQLiteGoalStore(root / ".local/state/goal.db")
        binding = {
            "project_id": "worker-fixture",
            "root": str(root),
            "worktree": str(root),
            "branch": "main",
            "git_common_dir": None,
            "starting_revision": "A",
            "environment_mode": "local",
        }
        provider = FakeProvider("thread-generation-1")
        launch_goal(
            store,
            goal_text="Complete the bounded worker fixture.",
            completion_contract={
                "interpretation": "The fixture is complete when the criterion passes.",
                "required_evidence": ["Tests pass."],
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
            remaining_work="Execute one bounded generation.",
            goal_id="CG-20260717T150000Z-fedcba98",
            timestamp=TS,
            launcher_token="l" * 48,
            handoff_token="h" * 48,
        )
        envelope = provider.calls[0]["envelope"]
        return root, store, envelope

    @staticmethod
    def result(*, after=HASH_B, jobs=1, status=None):
        status = status or ("completed" if jobs else "no_action")
        return {
            "schema_version": "sys4ai.continue-result.v1",
            "status": status,
            "boundary_entered": "existing_agent_job_ready" if jobs else "no_action",
            "agent_jobs_executed": jobs,
            "task_id": "TASK-1" if jobs else None,
            "decision_id": "DDR-1" if jobs else None,
            "job_id": "AJ-1" if jobs else None,
            "completion_id": "AJC-1" if jobs else None,
            "handoff_id": "HANDOFF-1" if jobs else None,
            "progress_effect": "bounded_progress" if jobs else "none",
            "global_goal_evaluation": "not_evaluated_here",
            "repository_fingerprint_before": HASH_A,
            "repository_fingerprint_after": after,
            "validators": {
                "required": 1,
                "passed": 1,
                "failed": 0,
                "warning": 0,
                "skipped": 0,
            },
            "next_recommended_action": "Evaluate the durable goal.",
            "execution_performed": bool(jobs),
            "reason_code": "goal.checked",
            "extensions": {},
        }

    @staticmethod
    def evidence(criterion_status):
        return {
            "completion_contract_results": [
                {
                    "criterion": "Tests pass.",
                    "status": criterion_status,
                    "evidence_refs": ["tests/focused.json"]
                    if criterion_status == "pass"
                    else [],
                }
            ],
            "checkpoint": {
                "provider": "none",
                "status": "not_required",
                "revision": None,
                "evidence_ref": None,
            },
            "validator_results": [
                {
                    "validator_id": "focused",
                    "validator_class": "process_validation",
                    "status": "pass",
                    "reason_code": None,
                    "evidence_ref": None,
                    "notes": [],
                }
            ],
            "revision_before": "A",
            "revision_after": "B",
            "progress_summary": "Direct evidence was checked.",
            "remaining_work": "None." if criterion_status == "pass" else "Repair the remaining failure.",
        }

    def invoke(self, store, envelope, invoker, evidence_status, **overrides):
        values = {
            "envelope": envelope,
            "envelope_sha256": content_sha256(envelope),
            "expected_revision": 3,
            "current_thread_id": "thread-generation-1",
            "continue_invoker": invoker,
            "direct_evidence_provider": lambda result: self.evidence(evidence_status),
            "legal_route_available": True,
            "claim_token": "c" * 48,
            "successor_handoff_token": "n" * 48,
            "timestamp": TS,
        }
        values.update(overrides)
        return run_goal_worker(store, **values)

    def test_met_generation_invokes_continue_once_and_terminalizes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, envelope = self.launched(directory)
            invoker = CountingContinue(self.result())
            summary = self.invoke(store, envelope, invoker, "pass")
            self.assertEqual(invoker.calls, 1)
            self.assertEqual(summary.continue_invocations, 1)
            self.assertEqual(summary.agentjobs_executed, 1)
            self.assertEqual(summary.state_phase, "terminal_complete")
            self.assertEqual(summary.successor_create_calls, 0)
            self.assertIsNotNone(summary.receipt_hash)
            with self.assertRaises(StateConflict):
                self.invoke(store, envelope, invoker, "pass")
            self.assertEqual(invoker.calls, 1)

    def test_unmet_new_state_creates_exactly_one_successor_then_stops(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, envelope = self.launched(directory)
            invoker = CountingContinue(self.result())
            successor = FakeProvider("thread-generation-2")
            summary = self.invoke(
                store,
                envelope,
                invoker,
                "fail",
                successor_provider=successor,
            )
            self.assertEqual(invoker.calls, 1)
            self.assertEqual(len(successor.calls), 1)
            self.assertEqual(summary.successor_create_calls, 1)
            self.assertEqual(summary.successor_generation, 2)
            self.assertEqual(summary.successor_thread_id, "thread-generation-2")
            self.assertEqual(summary.state_phase, "successor_created")
            self.assertIsNotNone(summary.successor_envelope_sha256)
            self.assertIsNotNone(summary.receipt_hash)

    def test_pre_execution_guard_stop_consumes_no_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, envelope = self.launched(directory)
            invoker = CountingContinue(self.result())
            summary = self.invoke(
                store,
                envelope,
                invoker,
                "fail",
                observations={"human_gate_clear": False},
            )
            self.assertEqual(invoker.calls, 0)
            self.assertEqual(summary.continue_invocations, 0)
            self.assertEqual(summary.agentjobs_executed, 0)
            self.assertEqual(summary.state_phase, "terminal_awaiting_human")
            self.assertIsNotNone(summary.receipt_hash)

    def test_unknown_continue_outcome_is_never_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, envelope = self.launched(directory)
            invoker = CountingContinue(raise_error=True)
            summary = self.invoke(store, envelope, invoker, "fail")
            self.assertEqual(invoker.calls, 1)
            self.assertEqual(summary.continue_invocations, "unknown")
            self.assertEqual(summary.agentjobs_executed, "unknown")
            self.assertTrue(summary.recovery_required)
            self.assertEqual(summary.state_phase, "terminal_awaiting_human")
            with self.assertRaises(StateConflict):
                self.invoke(store, envelope, invoker, "fail")
            self.assertEqual(invoker.calls, 1)

    def test_invalid_token_or_thread_is_rejected_before_continue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, envelope = self.launched(directory)
            invalid = copy.deepcopy(envelope)
            invalid["handoff_token"] = "x" * 48
            invoker = CountingContinue(self.result())
            with self.assertRaises(StateConflict):
                self.invoke(store, invalid, invoker, "pass")
            self.assertEqual(invoker.calls, 0)
        with tempfile.TemporaryDirectory() as directory:
            _, store, envelope = self.launched(directory)
            invoker = CountingContinue(self.result())
            with self.assertRaises(StateConflict):
                self.invoke(
                    store,
                    envelope,
                    invoker,
                    "pass",
                    current_thread_id="thread-launcher",
                )
            self.assertEqual(invoker.calls, 0)

    def test_invalid_structured_result_becomes_unknown_not_a_retry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, envelope = self.launched(directory)
            invalid = self.result()
            invalid.pop("reason_code")
            invoker = CountingContinue(invalid)
            summary = self.invoke(store, envelope, invoker, "fail")
            self.assertEqual(invoker.calls, 1)
            self.assertTrue(summary.recovery_required)
            self.assertEqual(summary.state_phase, "terminal_awaiting_human")

    def test_ambiguous_successor_finalizes_prior_receipt_and_quarantines(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, envelope = self.launched(directory)
            invoker = CountingContinue(self.result())
            successor = FakeProvider("unused", raise_error=True)
            summary = self.invoke(
                store,
                envelope,
                invoker,
                "fail",
                successor_provider=successor,
            )
            self.assertEqual(len(successor.calls), 1)
            self.assertEqual(summary.state_phase, "terminal_handoff_ambiguous")
            self.assertTrue(summary.recovery_required)
            self.assertIsNotNone(summary.receipt_hash)

    def test_budget_guards_are_hard(self) -> None:
        budget = WorkerBudget()
        budget.claim_continue()
        with self.assertRaises(StateConflict):
            budget.claim_continue()
        budget.claim_successor()
        with self.assertRaises(StateConflict):
            budget.claim_successor()


if __name__ == "__main__":
    unittest.main()
