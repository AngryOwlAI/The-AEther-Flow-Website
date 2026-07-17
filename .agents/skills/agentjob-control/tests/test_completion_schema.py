import unittest

from _support import SCHEMA_ROOT, cloned, fixture_cases, valid_completion
from agentjob_runtime.validation.schema import validate_instance


class CompletionSchemaTests(unittest.TestCase):
    def test_completion_fixtures(self) -> None:
        for case in fixture_cases("completion"):
            record = cloned(valid_completion())
            record["status"] = case.get("status", record["status"])
            if "verdict" in case:
                record["verdict"] = case["verdict"]
            if "changed_paths" in case:
                record["changed_paths"] = case["changed_paths"]
                record["outputs"] = []
            if case.get("drop_overread"):
                record["claim_summary"]["forbidden_overread"] = []
                record["claim_summary"]["inherited_boundary_ref"] = None
            with self.subTest(case["name"]):
                issues = validate_instance(record, SCHEMA_ROOT / "completion.schema.json")
                self.assertEqual(not issues, case["valid"], issues)


if __name__ == "__main__":
    unittest.main()
