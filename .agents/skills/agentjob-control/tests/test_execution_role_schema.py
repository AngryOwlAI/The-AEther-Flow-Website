import unittest

from _support import SCHEMA_ROOT, cloned, fixture_cases, valid_role
from agentjob_runtime.validation.schema import validate_instance


class ExecutionRoleSchemaTests(unittest.TestCase):
    def test_binding_type_fixtures(self) -> None:
        for case in fixture_cases("execution-role"):
            record = cloned(valid_role())
            record["binding_type"] = case["binding_type"]
            if case["binding_type"] == "task_overlay" and not case.get("omit_overlay"):
                record["task_overlay"] = {
                    "added_constraints": ["No network."],
                    "removed_permissions": ["external_research"],
                    "expanded_permissions": [],
                    "justification": "The job is local-only.",
                }
            if case["binding_type"] == "one_job_provisional_role":
                record["source_role_ref"] = None
                record["provisional_role"] = {
                    "justification": "No registered role fits exactly.",
                    "reusable": case.get("reusable", False),
                    "registration_prohibited_by_completion": True,
                }
            with self.subTest(case["name"]):
                issues = validate_instance(record, SCHEMA_ROOT / "execution-role.schema.json")
                self.assertEqual(not issues, case["valid"], issues)

    def test_one_job_expiration_is_required(self) -> None:
        record = valid_role()
        del record["expires_after"]
        self.assertTrue(validate_instance(record, SCHEMA_ROOT / "execution-role.schema.json"))


if __name__ == "__main__":
    unittest.main()
