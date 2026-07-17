import unittest

from _support import SCHEMA_ROOT, TS, cloned, fixture_cases, valid_record_set
from agentjob_runtime.validation.schema import validate_instance


class ActivationSchemaTests(unittest.TestCase):
    def test_activation_fixtures(self) -> None:
        base = valid_record_set()["activations"][0]
        for case in fixture_cases("activation"):
            record = cloned(base)
            record["packet_type"] = case["packet_type"]
            if "records" in case:
                record["records"] = case["records"]
            if "order" in case:
                record["records"][0]["order"] = case["order"]
            with self.subTest(case["name"]):
                issues = validate_instance(record, SCHEMA_ROOT / "activation.schema.json")
                self.assertEqual(not issues, case["valid"], issues)

    def test_supersession_preserves_old_and_replacement_references(self) -> None:
        record = {
            "schema_version": "sys4ai.supersession.v1",
            "supersession_id": "SUPER-1",
            "old_decision_id": "DDR-1",
            "old_job_id": "AJ-1",
            "reason": "The original state snapshot became stale.",
            "evidence_refs": [".agents/control/snapshots/current.json"],
            "prior_execution_status": "unexecuted",
            "working_evidence_handling": "No working evidence exists.",
            "replacement_decision_id": "DDR-2",
            "replacement_job_id": "AJ-2",
            "replacement_activation_id": "ACT-2",
            "claim_boundary_preserved": True,
            "created_at": TS,
            "extensions": {},
        }
        self.assertFalse(validate_instance(record, SCHEMA_ROOT / "supersession.schema.json"))
        del record["working_evidence_handling"]
        self.assertTrue(validate_instance(record, SCHEMA_ROOT / "supersession.schema.json"))


if __name__ == "__main__":
    unittest.main()
