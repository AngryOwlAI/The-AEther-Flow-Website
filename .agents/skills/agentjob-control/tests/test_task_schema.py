import unittest

from _support import SCHEMA_ROOT, cloned, fixture_cases, valid_task
from agentjob_runtime.validation.schema import validate_instance


class TaskSchemaTests(unittest.TestCase):
    def test_task_status_and_closure_fixtures(self) -> None:
        for case in fixture_cases("task"):
            record = cloned(valid_task())
            record["status"] = case["status"]
            record["closure"]["status"] = case["closure_status"]
            if "completion_refs" in case:
                record["closure"]["completion_refs"] = case["completion_refs"]
            if "no_execution_reason" in case:
                record["closure"]["no_execution_reason"] = case["no_execution_reason"]
            with self.subTest(case["name"]):
                issues = validate_instance(record, SCHEMA_ROOT / "task.schema.json")
                self.assertEqual(not issues, case["valid"], issues)

    def test_domain_field_must_be_namespaced(self) -> None:
        record = valid_task()
        record["physics_route"] = "not-portable"
        self.assertTrue(validate_instance(record, SCHEMA_ROOT / "task.schema.json"))


if __name__ == "__main__":
    unittest.main()
