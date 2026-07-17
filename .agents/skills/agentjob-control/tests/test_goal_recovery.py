from __future__ import annotations

import tempfile
import unittest

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.decide import decide_generation
from agentjob_runtime.goal.execution import (
    claim_generation,
    consume_invocation,
    record_invocation_unknown,
)
from agentjob_runtime.goal.recovery import (
    abandon_unconsumed,
    adopt_successor,
    amend_guards,
    begin_recovery,
    cancel_relay,
    reconcile_consumed,
    resume_relay,
)
from agentjob_runtime.goal.successor import record_dispatch_outcome
from agentjob_runtime.goal.verify import verify_generation
from test_generation_execution import claimable
from test_goal_receipts import evidence, verifying
from test_successor_state import prepared


AUTH = "user-approved-recovery-2026-07-17"


def receipt_evidence(fingerprint: str, *, evaluation="indeterminate"):
    return {
        "revision_before": "A",
        "revision_after": "unknown",
        "fingerprint_after": fingerprint,
        "agent_job_id": None,
        "zero_job_reason": None,
        "task_id": None,
        "handoff_id": None,
        "checkpoint": {"provider": "none", "status": "unknown", "revision": None, "evidence_ref": None},
        "validator_results": [],
        "goal_evaluation": evaluation,
        "progress_summary": "Recovery could not prove a direct return.",
        "remaining_work": "Human reconciliation remains required.",
        "extensions": {},
    }


class GoalRecoveryTests(unittest.TestCase):
    def test_ambiguous_dispatch_adopts_one_uniquely_proven_successor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, reserved = prepared(directory)
            ambiguous = record_dispatch_outcome(
                store, goal_id=reserved["goal_id"], expected_revision=2, generation=1,
                handoff_token="h" * 48, provider_id="fake", outcome="ambiguous",
                diagnostic={"reason": "transport uncertainty"},
            )
            recovery = begin_recovery(
                store, goal_id=reserved["goal_id"], expected_revision=3,
                user_authorization=AUTH, evidence={"provider_status": "one live candidate"},
            )
            adopted = adopt_successor(
                store, goal_id=reserved["goal_id"], expected_revision=4, generation=1,
                successor_thread_id="recovered-thread", user_authorization=AUTH,
                uniqueness_evidence={"candidate_count": 1, "thread_id": "recovered-thread", "status": "live"},
            )
            self.assertEqual(adopted["state"]["phase"], "successor_created")
            self.assertEqual(adopted["handoff"]["successor_thread_id"], "recovered-thread")
            self.assertEqual(len(adopted["generations"]), 1)
            with self.assertRaises(StateConflict):
                adopt_successor(
                    store, goal_id=reserved["goal_id"], expected_revision=5, generation=1,
                    successor_thread_id="second", user_authorization=AUTH,
                    uniqueness_evidence={"candidate_count": 1, "thread_id": "second", "status": "live"},
                )

    def test_unconsumed_generation_can_be_abandoned_only_with_holder_proof(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, record = claimable(directory)
            claimed = claim_generation(
                store, goal_id=record["goal_id"], expected_revision=3, generation=1,
                handoff_token="h" * 48, idempotency_key=f"{record['goal_id']}:1",
                successor_thread_id="succ", claim_token="c" * 48,
            )
            with self.assertRaises(RecordValidationError):
                abandon_unconsumed(
                    store, goal_id=record["goal_id"], expected_revision=4, generation=1,
                    user_authorization=AUTH, terminal_holder_proof={},
                )
            abandoned = abandon_unconsumed(
                store, goal_id=record["goal_id"], expected_revision=4, generation=1,
                user_authorization=AUTH, terminal_holder_proof={"thread_status": "terminal"},
            )
            self.assertEqual(abandoned["state"]["passes_consumed"], 0)
            self.assertEqual(abandoned["state"]["phase"], "terminal_failed")
            self.assertIsNotNone(abandoned["generations"]["1"]["finalized_receipt_hash"])

    def test_consumed_unknown_is_finalized_unknown_and_never_rerun(self) -> None:
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
            uncertain = record_invocation_unknown(
                store, goal_id=record["goal_id"], expected_revision=5, generation=1,
                claim_token="c" * 48, diagnostic={"reason": "uncertain return"},
            )
            begin_recovery(
                store, goal_id=record["goal_id"], expected_revision=6,
                user_authorization=AUTH, evidence={"thread_status": "terminal"},
            )
            reconciled = reconcile_consumed(
                store, goal_id=record["goal_id"], expected_revision=7, generation=1,
                user_authorization=AUTH, terminal_holder_proof={"thread_status": "terminal"},
                canonical_evidence={
                    "after_fingerprint": uncertain["generations"]["1"]["before_fingerprint"],
                    "goal_evaluation": "indeterminate",
                    "receipt_evidence": receipt_evidence(
                        uncertain["generations"]["1"]["before_fingerprint"]
                    ),
                },
                returned_proven=False, decision="terminal_awaiting_human",
            )
            self.assertEqual(reconciled["generations"]["1"]["invocation_state"], "unknown")
            self.assertEqual(reconciled["state"]["passes_consumed"], 1)
            with self.assertRaises(StateConflict):
                consume_invocation(
                    store, goal_id=record["goal_id"], expected_revision=8, generation=1,
                    claim_token="c" * 48,
                )

    def test_guard_amendment_is_append_only_then_resume_requires_legal_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory, after_revision="A")
            verify_generation(
                store, goal_id=goal_id, expected_revision=6, generation=1,
                claim_token="c" * 48, continue_result=result,
                after_fingerprint=after, direct_evidence=evidence("fail"),
            )
            decide_generation(
                store, goal_id=goal_id, expected_revision=7, generation=1,
                claim_token="c" * 48, legal_route_available=True,
            )
            begin_recovery(
                store, goal_id=goal_id, expected_revision=8, user_authorization=AUTH,
                evidence={"new_evidence": "a different route now exists"},
            )
            amended = amend_guards(
                store, goal_id=goal_id, expected_revision=9, user_authorization=AUTH,
                evidence={"reason": "user extended relay"},
                new_guards={"max_continue_passes": 5, "deadline_at": "2099-01-02T00:00:00Z"},
            )
            self.assertEqual(amended["guards"]["max_continue_passes"], 3)
            self.assertEqual(amended["amendments"][-1]["new_value"]["max_continue_passes"], 5)
            with self.assertRaises(RecordValidationError):
                amend_guards(
                    store, goal_id=goal_id, expected_revision=10, user_authorization=AUTH,
                    evidence={"reason": "invalid weakening"},
                    new_guards={"max_continue_passes": 2},
                )
            resumed = resume_relay(
                store, goal_id=goal_id, expected_revision=10, user_authorization=AUTH,
                evidence={"legal_route_available": True, "route_ref": "TASK-2"},
            )
            self.assertEqual(resumed["state"]["phase"], "continuation_required")
            self.assertEqual(resumed["state"]["passes_consumed"], 1)
            self.assertGreaterEqual(
                store.query_one("SELECT COUNT(*) AS count FROM recovery_actions WHERE goal_id=?", (goal_id,))["count"],
                3,
            )

    def test_cancellation_is_immutable_and_absorbing_terminal_cannot_recover(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, reserved = prepared(directory)
            ambiguous = record_dispatch_outcome(
                store, goal_id=reserved["goal_id"], expected_revision=2, generation=1,
                handoff_token="h" * 48, provider_id="fake", outcome="ambiguous",
                diagnostic={"reason": "uncertain"},
            )
            begin_recovery(
                store, goal_id=reserved["goal_id"], expected_revision=3,
                user_authorization=AUTH, evidence={"thread_status": "terminal"},
            )
            cancelled = cancel_relay(
                store, goal_id=reserved["goal_id"], expected_revision=4,
                user_authorization=AUTH, evidence={"reason": "user cancelled"},
            )
            self.assertEqual(cancelled["state"]["phase"], "terminal_cancelled")
            with self.assertRaises(StateConflict):
                begin_recovery(
                    store, goal_id=reserved["goal_id"], expected_revision=5,
                    user_authorization=AUTH, evidence={"reason": "try again"},
                )


if __name__ == "__main__":
    unittest.main()
