from __future__ import annotations

import unittest

from _support import RUNTIME_SCRIPTS  # noqa: F401
from agentjob_runtime.goal.model import (
    ABSORBING_TERMINALS,
    NORMAL_TRANSITIONS,
    PHASES,
    RECOVERABLE_TERMINALS,
    STOP_PHASES,
    TERMINAL_PHASES,
    map_stop,
    transition_allowed,
)


class GoalStateMachineTests(unittest.TestCase):
    def test_every_declared_normal_transition_is_allowed(self) -> None:
        for old_phase, new_phase in sorted(NORMAL_TRANSITIONS):
            with self.subTest(old=old_phase, new=new_phase):
                self.assertTrue(transition_allowed(old_phase, new_phase))

    def test_every_unlisted_normal_transition_is_rejected(self) -> None:
        for old_phase in sorted(PHASES):
            for new_phase in sorted(PHASES):
                with self.subTest(old=old_phase, new=new_phase):
                    self.assertEqual(
                        transition_allowed(old_phase, new_phase),
                        (old_phase, new_phase) in NORMAL_TRANSITIONS,
                    )

    def test_recovery_transition_matrix_is_exhaustive(self) -> None:
        recovery_targets = {
            "successor_created",
            "successor_intent",
            "continuation_required",
            *TERMINAL_PHASES,
        }
        for old_phase in sorted(PHASES):
            for new_phase in sorted(PHASES):
                expected = (
                    old_phase in RECOVERABLE_TERMINALS and new_phase == "recovery_pending"
                ) or (old_phase == "recovery_pending" and new_phase in recovery_targets)
                with self.subTest(old=old_phase, new=new_phase):
                    self.assertEqual(
                        transition_allowed(old_phase, new_phase, recovery=True), expected
                    )

    def test_absorbing_terminals_cannot_resume_or_recover(self) -> None:
        for terminal in sorted(ABSORBING_TERMINALS):
            for target in sorted(PHASES):
                with self.subTest(terminal=terminal, target=target):
                    self.assertFalse(transition_allowed(terminal, target))
                    self.assertFalse(transition_allowed(terminal, target, recovery=True))

    def test_every_registered_stop_reason_maps_to_a_terminal(self) -> None:
        for reason, terminal in sorted(STOP_PHASES.items()):
            with self.subTest(reason=reason):
                self.assertEqual(map_stop(reason), terminal)
                self.assertIn(terminal, TERMINAL_PHASES)


if __name__ == "__main__":
    unittest.main()
