import copy
import unittest

from _support import valid_goal_receipt, valid_record_set
from agentjob_runtime.validation.cross_record import validate_record_set


class CrossRecordValidationTests(unittest.TestCase):
    def reason_codes(self, records, **kwargs):
        return {issue.code for issue in validate_record_set(records, **kwargs)}

    def test_valid_record_chain_has_no_findings(self) -> None:
        self.assertEqual(validate_record_set(valid_record_set()), [])

    def test_orphan_duplicate_stale_and_conflicting_records(self) -> None:
        records = valid_record_set()
        records["tasks"][0]["current_job_id"] = "AJ-MISSING"
        records["roles"].append(copy.deepcopy(records["roles"][0]))
        records["activations"][0]["records"][1]["sha256"] = "0" * 64
        codes = self.reason_codes(records)
        self.assertIn("trace.task_job_missing", codes)
        self.assertIn("record.duplicate_id", codes)
        self.assertIn("activation.hash_mismatch", codes)

    def test_completion_is_checked_against_job_boundary(self) -> None:
        records = valid_record_set()
        completion = records["completions"][0]
        completion["changed_paths"].append("secrets/private.txt")
        completion["command_results"].append(
            {"command_id": "undeclared", "exit_code": 0, "status": "pass", "evidence_ref": None}
        )
        completion["claim_summary"]["allowed_conclusions"].append("Everything is correct.")
        codes = self.reason_codes(records)
        self.assertIn("completion.changed_path_forbidden", codes)
        self.assertIn("completion.command_undeclared", codes)
        self.assertIn("completion.claim_broadened", codes)

    def test_handoff_is_recommendation_not_authority(self) -> None:
        records = valid_record_set()
        records["handoffs"][0]["grants_execution_authority"] = True
        self.assertIn("handoff.authority_grant_forbidden", self.reason_codes(records))

    def test_goal_receipt_generation_and_idempotency_are_unique(self) -> None:
        records = valid_record_set()
        receipt = valid_goal_receipt()
        duplicate = copy.deepcopy(receipt)
        duplicate["receipt_id"] = "RECEIPT-CG-1-DUPLICATE"
        records["goal_receipts"] = [receipt, duplicate]
        codes = self.reason_codes(records)
        self.assertIn("goal_receipt.duplicate_generation", codes)
        self.assertIn("goal_receipt.duplicate_idempotency_key", codes)

    def test_unknown_extension_is_blocking_in_strict_mode(self) -> None:
        records = valid_record_set()
        records["tasks"][0]["extensions"] = {
            "unregistered": {"version": "1.0.0", "required": True, "data": {}}
        }
        self.assertIn("extension.namespace_undeclared", self.reason_codes(records))
        self.assertNotIn(
            "extension.namespace_undeclared",
            self.reason_codes(records, strict_extensions=False),
        )

    def test_supersession_cycle_is_detected(self) -> None:
        records = valid_record_set()
        old_job = records["jobs"][0]
        old_decision = records["decisions"][0]
        new_job = copy.deepcopy(old_job)
        new_job["job_id"] = "AJ-TASK-20260717-001-002"
        new_job["decision_id"] = "DDR-20260717-002"
        new_job["status"] = "superseded"
        new_decision = copy.deepcopy(old_decision)
        new_decision["decision_id"] = "DDR-20260717-002"
        new_decision["selected"]["agent_job_id"] = new_job["job_id"]
        new_decision["status"] = "superseded"
        records["jobs"].append(new_job)
        records["decisions"].append(new_decision)
        records["supersessions"] = [
            {
                "supersession_id": "SUPER-1",
                "old_job_id": old_job["job_id"],
                "replacement_job_id": new_job["job_id"],
                "old_decision_id": old_decision["decision_id"],
                "replacement_decision_id": new_decision["decision_id"],
            },
            {
                "supersession_id": "SUPER-2",
                "old_job_id": new_job["job_id"],
                "replacement_job_id": old_job["job_id"],
                "old_decision_id": new_decision["decision_id"],
                "replacement_decision_id": old_decision["decision_id"],
            },
        ]
        self.assertIn("supersession.cycle", self.reason_codes(records))


if __name__ == "__main__":
    unittest.main()
