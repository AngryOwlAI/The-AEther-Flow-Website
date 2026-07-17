from __future__ import annotations

import tempfile
import unittest

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import StateConflict
from agentjob_runtime.goal.decide import (
    decide_and_reserve_successor,
    decide_generation,
    terminal_classification,
)
from agentjob_runtime.goal.model import ABSORBING_TERMINALS, RECOVERABLE_TERMINALS, STOP_PHASES
from agentjob_runtime.goal.successor import record_successor
from agentjob_runtime.goal.verify import verify_generation
from test_goal_receipts import evidence, verifying


class GoalDecisionTests(unittest.TestCase):
    def test_met_goal_terminalizes_with_exactly_one_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory)
            verify_generation(
                store, goal_id=goal_id, expected_revision=6, generation=1,
                claim_token="c" * 48, continue_result=result,
                after_fingerprint=after, direct_evidence=evidence("pass"),
            )
            terminal = decide_generation(
                store, goal_id=goal_id, expected_revision=7, generation=1,
                claim_token="c" * 48, legal_route_available=True,
            )
            self.assertEqual(terminal["state"]["phase"], "terminal_complete")
            self.assertIsNone(terminal["state"]["active_lease"])
            self.assertEqual(
                store.query_one("SELECT COUNT(*) AS count FROM step_receipts WHERE goal_id=?", (goal_id,))["count"],
                1,
            )
            with self.assertRaises(StateConflict):
                decide_generation(
                    store, goal_id=goal_id, expected_revision=8, generation=1,
                    claim_token="c" * 48, legal_route_available=False,
                )

    def test_unmet_new_state_reserves_one_successor_and_finalizes_after_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory)
            verify_generation(
                store, goal_id=goal_id, expected_revision=6, generation=1,
                claim_token="c" * 48, continue_result=result,
                after_fingerprint=after, direct_evidence=evidence("fail"),
            )
            reserved = decide_and_reserve_successor(
                store, goal_id=goal_id, expected_revision=7, generation=1,
                claim_token="c" * 48, predecessor_thread_id="succ",
                handoff_token="n" * 48,
            )
            self.assertEqual(reserved["state"]["phase"], "successor_intent")
            self.assertEqual(set(reserved["generations"]), {"1", "2"})
            self.assertIsNone(reserved["generations"]["1"]["finalized_receipt_hash"])
            created = record_successor(
                store, goal_id=goal_id, expected_revision=9, generation=2,
                handoff_token="n" * 48, successor_thread_id="succ-2",
                provider_id="fake", provider_response={"status": "created"},
            )
            self.assertIsNotNone(created["generations"]["1"]["finalized_receipt_hash"])
            self.assertEqual(
                store.query_one("SELECT COUNT(*) AS count FROM step_receipts WHERE goal_id=?", (goal_id,))["count"],
                1,
            )

    def test_unchanged_state_and_indeterminate_evidence_never_map_to_success(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory, after_revision="A")
            verify_generation(
                store, goal_id=goal_id, expected_revision=6, generation=1,
                claim_token="c" * 48, continue_result=result,
                after_fingerprint=after, direct_evidence=evidence("fail"),
            )
            stopped = decide_generation(
                store, goal_id=goal_id, expected_revision=7, generation=1,
                claim_token="c" * 48, legal_route_available=True,
            )
            self.assertEqual(stopped["state"]["phase"], "terminal_no_progress")
        with tempfile.TemporaryDirectory() as directory:
            store, goal_id, result, after = verifying(directory)
            verify_generation(
                store, goal_id=goal_id, expected_revision=6, generation=1,
                claim_token="c" * 48, continue_result=result,
                after_fingerprint=after, direct_evidence=evidence("indeterminate"),
            )
            stopped = decide_generation(
                store, goal_id=goal_id, expected_revision=7, generation=1,
                claim_token="c" * 48, legal_route_available=True,
            )
            self.assertEqual(stopped["state"]["phase"], "terminal_awaiting_human")

    def test_stop_mapping_and_terminal_partition_are_complete(self) -> None:
        self.assertNotIn("terminal_complete", {phase for reason, phase in STOP_PHASES.items() if reason != "goal_met"})
        for phase in ABSORBING_TERMINALS:
            self.assertEqual(terminal_classification(phase), "absorbing")
        for phase in RECOVERABLE_TERMINALS:
            self.assertEqual(terminal_classification(phase), "recoverable")
        self.assertFalse(ABSORBING_TERMINALS & RECOVERABLE_TERMINALS)


if __name__ == "__main__":
    unittest.main()
