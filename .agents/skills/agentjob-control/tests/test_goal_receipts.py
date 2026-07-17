from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.fingerprinting.canonical import build_fingerprint
from agentjob_runtime.goal.execution import (
    claim_generation,
    consume_invocation,
    record_invocation_returned,
)
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_successor, reserve_successor
from agentjob_runtime.goal.verify import verify_generation


def fingerprint_parts(revision: str):
    return {
        "repository": {
            "provider": "git", "root": "/project", "worktree": "/project",
            "git_common_dir": "/project/.git", "branch": "main", "revision": revision,
            "status_porcelain": "",
        },
        "control": {"config_hash": "a" * 64, "task_id": "TASK-1"},
        "resolver": {"boundary": "no_action", "reason_code": "goal.checked"},
        "validation": {"required_validator_ids": ["focused"], "outcomes": ["pass"]},
        "checkpoint": {"provider": "none", "status": "not_required", "revision": revision},
        "adapter_extensions": {},
    }


def continue_result(before: str, after: str, *, jobs=0):
    return {
        "schema_version": "sys4ai.continue-result.v1",
        "status": "no_action" if jobs == 0 else "completed",
        "boundary_entered": "no_action" if jobs == 0 else "existing_agent_job_ready",
        "agent_jobs_executed": jobs,
        "task_id": None if jobs == 0 else "TASK-1",
        "decision_id": None if jobs == 0 else "DDR-1",
        "job_id": None if jobs == 0 else "AJ-1",
        "completion_id": None if jobs == 0 else "AJC-1",
        "handoff_id": None,
        "progress_effect": "none" if jobs == 0 else "bounded_completion",
        "global_goal_evaluation": "not_evaluated_here",
        "repository_fingerprint_before": before,
        "repository_fingerprint_after": after,
        "validators": {"required": 1, "passed": 1, "failed": 0, "warning": 0, "skipped": 0},
        "next_recommended_action": "Evaluate the durable goal.",
        "execution_performed": jobs == 1,
        "reason_code": "goal.checked",
        "extensions": {},
    }


def evidence(status="pass"):
    return {
        "completion_contract_results": [
            {"criterion": "Tests pass.", "status": status, "evidence_refs": ["tests/focused.json"]}
        ],
        "checkpoint": {"provider": "none", "status": "not_required", "revision": None, "evidence_ref": None},
        "validator_results": [
            {"validator_id": "focused", "validator_class": "process_validation", "status": "pass", "reason_code": None, "evidence_ref": None, "notes": []}
        ],
        "progress_summary": "Direct evidence was checked.",
        "remaining_work": "None under the contract." if status == "pass" else "Repair failures.",
    }


def verifying(directory: str, after_revision: str = "B"):
    root = Path(directory).resolve()
    store = SQLiteGoalStore(root / "state.sqlite3")
    initial = build_fingerprint([], **fingerprint_parts("A"))
    goal = initialize_goal(
        store, goal_text="Finish.",
        completion_contract={"interpretation": "Verified finish.", "required_evidence": ["Tests pass."], "user_confirmed_when_ambiguous": True},
        guards={"max_continue_passes": 3, "deadline_at": "2099-01-01T00:00:00Z"},
        repository_binding={"project_id": "example", "root": str(root), "worktree": str(root), "branch": "main", "git_common_dir": str(root / ".git"), "starting_revision": "A", "environment_mode": "local"},
        initial_fingerprint=initial.fingerprint,
        authorization={"fresh_recursive_threads_explicitly_requested": True},
        goal_id="CG-20260717T150000Z-abcdef12", timestamp="2026-07-17T15:00:00Z", launcher_token="l" * 48,
    )
    reserve_successor(store, goal_id=goal["goal_id"], expected_revision=1, current_holder_token="l" * 48, predecessor_thread_id="pred", handoff_token="h" * 48)
    record_successor(store, goal_id=goal["goal_id"], expected_revision=2, generation=1, handoff_token="h" * 48, successor_thread_id="succ", provider_id="fake", provider_response={"status": "created"})
    claim_generation(store, goal_id=goal["goal_id"], expected_revision=3, generation=1, handoff_token="h" * 48, idempotency_key=f"{goal['goal_id']}:1", successor_thread_id="succ", claim_token="c" * 48)
    consume_invocation(store, goal_id=goal["goal_id"], expected_revision=4, generation=1, claim_token="c" * 48)
    after = build_fingerprint([initial.fingerprint], **fingerprint_parts(after_revision))
    result = continue_result(initial.fingerprint, after.fingerprint)
    record_invocation_returned(store, goal_id=goal["goal_id"], expected_revision=5, generation=1, claim_token="c" * 48, continue_result=result)
    return store, goal["goal_id"], result, after


class GoalReceiptTests(unittest.TestCase):
    def test_direct_evidence_evaluates_goal_and_persists_pending_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory)
            verified = verify_generation(
                store, goal_id=goal_id, expected_revision=6, generation=1,
                claim_token="c" * 48, continue_result=result, after_fingerprint=after,
                direct_evidence=evidence(),
            )
            self.assertEqual(verified["state"]["goal_evaluation"], "met")
            self.assertEqual(verified["state"]["phase"], "step_verified")
            self.assertIsNotNone(verified["generations"]["1"]["pending_step_result"])
            self.assertIsNone(store.query_one("SELECT * FROM step_receipts WHERE goal_id=?", (goal_id,)))

    def test_worker_prose_without_contract_evidence_cannot_satisfy_goal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory)
            prose_only = evidence()
            prose_only.pop("completion_contract_results")
            prose_only["progress_summary"] = "Everything is definitely complete."
            with self.assertRaises(RecordValidationError):
                verify_generation(
                    store, goal_id=goal_id, expected_revision=6, generation=1,
                    claim_token="c" * 48, continue_result=result,
                    after_fingerprint=after, direct_evidence=prose_only,
                )

    def test_continue_result_must_match_direct_fingerprints(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory)
            mismatched = copy.deepcopy(result)
            mismatched["repository_fingerprint_after"] = "f" * 64
            with self.assertRaises(StateConflict):
                verify_generation(
                    store, goal_id=goal_id, expected_revision=6, generation=1,
                    claim_token="c" * 48, continue_result=mismatched,
                    after_fingerprint=after, direct_evidence=evidence(),
                )


if __name__ == "__main__":
    unittest.main()
