import unittest

from _support import cloned, valid_decision, valid_job, valid_role, valid_task
from agentjob_runtime.control.resolver import resolve_snapshot


def base_snapshot():
    return {
        "configured": True,
        "capabilities_ready": True,
        "integrity_findings": (),
        "repository_match": True,
        "concurrent_conflict": False,
        "task": valid_task(),
        "decision": valid_decision(),
        "job": valid_job(),
        "role": valid_role(),
        "packet_activated": True,
        "state_snapshot_stale": False,
    }


class ContinuationBoundaryResolverTests(unittest.TestCase):
    def test_each_boundary_has_a_deterministic_fixture(self) -> None:
        cases = []
        snapshot = base_snapshot()
        snapshot["configured"] = False
        cases.append((snapshot, "bootstrap_required"))
        snapshot = base_snapshot()
        snapshot["task"] = None
        cases.append((snapshot, "no_action"))
        snapshot = base_snapshot()
        snapshot["job"] = None
        snapshot["decision"] = None
        snapshot["role"] = None
        cases.append((snapshot, "director_decision_required"))
        snapshot = base_snapshot()
        snapshot["task"]["requires_human_gate"] = True
        cases.append((snapshot, "human_gate_required"))
        snapshot = base_snapshot()
        cases.append((snapshot, "existing_agent_job_ready"))
        snapshot = base_snapshot()
        snapshot["integrity_findings"] = ("hash_mismatch",)
        cases.append((snapshot, "control_repair_required"))
        snapshot = base_snapshot()
        snapshot["repository_match"] = False
        cases.append((snapshot, "blocked"))

        for snapshot, expected in cases:
            with self.subTest(expected=expected):
                result = resolve_snapshot(snapshot)
                self.assertEqual(result.boundary, expected)
                self.assertFalse(result.execution_performed)

    def test_stale_packet_requires_a_new_decision_without_selecting_role(self) -> None:
        snapshot = base_snapshot()
        snapshot["state_snapshot_stale"] = True
        result = resolve_snapshot(snapshot)
        self.assertEqual(result.boundary, "director_decision_required")
        self.assertIsNone(result.execution_role_id)
        self.assertEqual(result.reason_code, "packet.stale_requires_supersession_decision")

    def test_existing_job_returns_only_its_bound_role(self) -> None:
        result = resolve_snapshot(base_snapshot())
        self.assertEqual(result.execution_role_id, "ER-AJ-TASK-20260717-001-001")
        self.assertIn("authority_ambiguity", result.stop_conditions)

    def test_terminal_task_and_terminal_job(self) -> None:
        snapshot = base_snapshot()
        snapshot["task"]["status"] = "completed"
        self.assertEqual(resolve_snapshot(snapshot).boundary, "no_action")
        snapshot = base_snapshot()
        snapshot["job"]["status"] = "completed"
        self.assertEqual(resolve_snapshot(snapshot).boundary, "director_decision_required")


if __name__ == "__main__":
    unittest.main()
