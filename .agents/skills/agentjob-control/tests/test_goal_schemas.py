import unittest

from _support import (
    SCHEMA_ROOT,
    cloned,
    fixture_cases,
    valid_adapter,
    valid_config,
    valid_goal,
    valid_goal_receipt,
    valid_policy,
)
from agentjob_runtime.validation.schema import validate_instance


class GoalAndExtensionSchemaTests(unittest.TestCase):
    def test_all_terminal_states_and_forbidden_goal_amendment(self) -> None:
        for case in fixture_cases("goal"):
            record = cloned(valid_goal())
            record["state"]["phase"] = case.get("phase", "initialized")
            if "amendment_kind" in case:
                record["amendments"] = [
                    {
                        "kind": case["amendment_kind"],
                        "user_authorization": "Authorized test amendment.",
                        "created_at": "2026-07-17T15:01:00Z",
                        "prior_effective_sha256": "a" * 64,
                        "new_value": {"goal_text": "Changed"},
                        "new_sha256": "b" * 64,
                    }
                ]
            with self.subTest(case["name"]):
                issues = validate_instance(record, SCHEMA_ROOT / "goal-state.schema.json")
                self.assertEqual(not issues, case["valid"], issues)

    def test_consumed_generation_cannot_be_not_authorized(self) -> None:
        record = valid_goal()
        record["generations"]["1"] = {
            "generation": 1,
            "handoff_token": "t" * 32,
            "idempotency_key": f"{record['goal_id']}:1",
            "phase": "step_active",
            "lease_token": "lease-token",
            "invocation_consumed": True,
            "invocation_state": "not_authorized",
            "consumed_at": None,
            "returned_at": None,
            "before_fingerprint": "a" * 64,
            "after_fingerprint": None,
            "pending_step_result": None,
            "finalized_receipt_hash": None,
            "terminal_or_successor_outcome": None,
            "claimed_at": "2026-07-17T15:00:00Z",
            "successor_thread_id": None,
        }
        self.assertTrue(validate_instance(record, SCHEMA_ROOT / "goal-state.schema.json"))

    def test_receipt_count_zero_one_and_unknown(self) -> None:
        for count in [0, 1, "unknown"]:
            receipt = valid_goal_receipt()
            receipt["continue_invocation_count"] = count
            if count == 1:
                receipt["agent_job_id"] = "AJ-TASK-20260717-001-001"
                receipt["zero_job_reason"] = None
            elif count == "unknown":
                receipt["zero_job_reason"] = "The external call boundary is ambiguous."
            with self.subTest(count=count):
                self.assertFalse(
                    validate_instance(receipt, SCHEMA_ROOT / "goal-step-receipt.schema.json")
                )

    def test_policy_adapter_and_strict_config(self) -> None:
        for value, name in [
            (valid_policy(), "policy-pack.schema.json"),
            (valid_adapter(), "project-adapter.schema.json"),
            (valid_config(), "control-config.schema.json"),
        ]:
            with self.subTest(name=name):
                self.assertFalse(validate_instance(value, SCHEMA_ROOT / name))
        config = valid_config()
        config["unguarded_fallback"] = True
        self.assertTrue(validate_instance(config, SCHEMA_ROOT / "control-config.schema.json"))

    def test_continuation_envelope_and_continue_result(self) -> None:
        goal = valid_goal()
        envelope = {
            "schema_version": "sys4ai.continuation-envelope.v1",
            "goal_id": goal["goal_id"],
            "goal_sha256": goal["goal_sha256"],
            "completion_contract_sha256": goal["completion_contract_sha256"],
            "generation": 1,
            "handoff_token": "t" * 32,
            "idempotency_key": f"{goal['goal_id']}:1",
            "predecessor_thread_id": None,
            "predecessor_handoff_id": None,
            "repository_binding": goal["repository_binding"],
            "canonical_state": {
                "fingerprint": "a" * 64,
                "active_task_id": None,
                "current_decision_id": None,
                "current_job_id": None,
            },
            "progress_summary": "The relay was initialized.",
            "remaining_work": "Execute one legal generation.",
            "required_skill": "continue-implementing-goal",
            "extensions": {},
        }
        self.assertFalse(
            validate_instance(envelope, SCHEMA_ROOT / "continuation-envelope.schema.json")
        )
        envelope["required_skill"] = "continue"
        self.assertTrue(
            validate_instance(envelope, SCHEMA_ROOT / "continuation-envelope.schema.json")
        )

        result = {
            "schema_version": "sys4ai.continue-result.v1",
            "status": "no_action",
            "boundary_entered": "no_action",
            "agent_jobs_executed": 0,
            "task_id": None,
            "decision_id": None,
            "job_id": None,
            "completion_id": None,
            "handoff_id": None,
            "progress_effect": "none",
            "global_goal_evaluation": "not_evaluated_here",
            "repository_fingerprint_before": "a" * 64,
            "repository_fingerprint_after": "a" * 64,
            "validators": {"required": 1, "passed": 1, "failed": 0, "warning": 0, "skipped": 0},
            "next_recommended_action": None,
            "execution_performed": False,
            "reason_code": "no-action",
            "extensions": {},
        }
        self.assertFalse(validate_instance(result, SCHEMA_ROOT / "continue-result.schema.json"))
        result["agent_jobs_executed"] = 1
        self.assertTrue(validate_instance(result, SCHEMA_ROOT / "continue-result.schema.json"))


if __name__ == "__main__":
    unittest.main()
