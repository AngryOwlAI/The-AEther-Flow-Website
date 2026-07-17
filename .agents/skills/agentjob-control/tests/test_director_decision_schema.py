import unittest

from _support import SCHEMA_ROOT, cloned, fixture_cases, valid_decision
from agentjob_runtime.validation.schema import validate_instance


class DirectorDecisionSchemaTests(unittest.TestCase):
    def test_decision_mode_and_type_fixtures(self) -> None:
        for case in fixture_cases("director-decision"):
            record = cloned(valid_decision())
            record["decision_type"] = case["decision_type"]
            record["decision_mode"] = case["decision_mode"]
            if case["decision_mode"] == "deterministic":
                record["rule_id"] = "explicit-policy-rule"
                record["rejected_illegal_routes"] = ["Mutating activated records is illegal."]
            if case.get("drop_rejections"):
                record["rejected_alternatives"] = []
            with self.subTest(case["name"]):
                issues = validate_instance(record, SCHEMA_ROOT / "director-decision.schema.json")
                self.assertEqual(not issues, case["valid"], issues)

    def test_claim_boundary_is_required(self) -> None:
        record = valid_decision()
        del record["claim_boundary"]
        self.assertTrue(validate_instance(record, SCHEMA_ROOT / "director-decision.schema.json"))


if __name__ == "__main__":
    unittest.main()
