import unittest

from _support import SCHEMA_ROOT, cloned, fixture_cases, valid_handoff
from agentjob_runtime.validation.schema import validate_instance


class HandoffSchemaTests(unittest.TestCase):
    def test_handoff_never_grants_execution_authority(self) -> None:
        for case in fixture_cases("handoff"):
            record = cloned(valid_handoff())
            record["grants_execution_authority"] = case["grants_execution_authority"]
            with self.subTest(case["name"]):
                issues = validate_instance(record, SCHEMA_ROOT / "handoff.schema.json")
                self.assertEqual(not issues, case["valid"], issues)


if __name__ == "__main__":
    unittest.main()
