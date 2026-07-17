import unittest

from _support import SCHEMA_ROOT, cloned, fixture_cases, valid_job
from agentjob_runtime.validation.schema import validate_instance


class AgentJobSchemaTests(unittest.TestCase):
    def test_authority_scenarios_and_negative_fixtures(self) -> None:
        for case in fixture_cases("agent-job"):
            record = cloned(valid_job())
            record["authority"]["allowed_write_paths"] = case.get(
                "write_paths", record["authority"]["allowed_write_paths"]
            )
            record["authority"]["allowed_actions"] = case.get(
                "actions", record["authority"]["allowed_actions"]
            )
            if case.get("drop"):
                del record[case["drop"]]
            with self.subTest(case["name"]):
                issues = validate_instance(record, SCHEMA_ROOT / "agent-job.schema.json")
                self.assertEqual(not issues, case["valid"], issues)

    def test_structured_command_is_required(self) -> None:
        record = valid_job()
        record["commands"]["approved"][0] = "python -m unittest"
        self.assertTrue(validate_instance(record, SCHEMA_ROOT / "agent-job.schema.json"))

    def test_shell_mode_requires_policy_approval(self) -> None:
        record = valid_job()
        record["commands"]["approved"][0]["shell"] = True
        self.assertTrue(validate_instance(record, SCHEMA_ROOT / "agent-job.schema.json"))
        record["commands"]["approved"][0]["shell_policy_approval_ref"] = "APPROVAL-1"
        self.assertFalse(validate_instance(record, SCHEMA_ROOT / "agent-job.schema.json"))

    def test_core_contains_no_aether_physics_fields(self) -> None:
        text = (SCHEMA_ROOT / "agent-job.schema.json").read_text(encoding="utf-8").lower()
        for forbidden in ["distance_to_gr", "ontology-law", "gate chair", "physics"]:
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
