import copy
import tempfile
import unittest
from pathlib import Path

from _support import TS, valid_decision, valid_job, valid_role, valid_task
from agentjob_runtime.control.activation import activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.supersession import supersede_packet
from agentjob_runtime.errors import RecordValidationError


class SupersessionTests(unittest.TestCase):
    def prepared_store(self, directory: str):
        root = Path(directory).resolve()
        store = FilesystemControlStore(root, ".agents/control")
        task = valid_task()
        task["current_decision_id"] = None
        task["current_job_id"] = None
        store.create_task(task)
        activate_packet(
            store,
            task_id=task["task_id"],
            decision=valid_decision(),
            job=valid_job(),
            execution_role=valid_role(),
            expected_revision=1,
        )
        return store, task

    def replacement_packet(self):
        decision = copy.deepcopy(valid_decision())
        job = copy.deepcopy(valid_job())
        role = copy.deepcopy(valid_role())
        decision["decision_id"] = "DDR-20260717-002"
        decision["decision_type"] = "supersede_job"
        decision["supersedes_decision_id"] = "DDR-20260717-001"
        decision["selected"]["agent_job_id"] = "AJ-TASK-20260717-001-002"
        job["job_id"] = "AJ-TASK-20260717-001-002"
        job["decision_id"] = decision["decision_id"]
        job["concurrency"]["idempotency_key"] = job["job_id"]
        job["role_binding"]["execution_role_ref"] = ".agents/control/tasks/TASK-20260717-001/roles/ER-AJ-TASK-20260717-001-002.json"
        role["execution_role_id"] = "ER-AJ-TASK-20260717-001-002"
        role["job_id"] = job["job_id"]
        role["expires_after"] = job["job_id"]
        return decision, job, role

    def test_supersession_preserves_old_bytes_and_updates_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, task = self.prepared_store(directory)
            decision, job, role = self.replacement_packet()
            old_decision_path = store.record_path("director_decision", task["task_id"], "DDR-20260717-001")
            old_job_path = store.record_path("agent_job", task["task_id"], "AJ-TASK-20260717-001-001")
            before = (old_decision_path.read_bytes(), old_job_path.read_bytes())
            receipt = supersede_packet(
                store,
                task_id=task["task_id"],
                old_decision_id="DDR-20260717-001",
                old_job_id="AJ-TASK-20260717-001-001",
                replacement_decision=decision,
                replacement_job=job,
                replacement_role=role,
                reason="The prior state snapshot became stale.",
                evidence_refs=[".agents/control/snapshots/current.json"],
                prior_execution_status="unexecuted",
                working_evidence_handling="No working evidence exists.",
                expected_revision=2,
                created_at=TS,
            )
            self.assertEqual(before, (old_decision_path.read_bytes(), old_job_path.read_bytes()))
            self.assertEqual(store.load_task(task["task_id"])["current_job_id"], job["job_id"])
            self.assertIn(receipt.supersession_id, store.activated_record_ids())

    def test_missing_reason_or_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, task = self.prepared_store(directory)
            decision, job, role = self.replacement_packet()
            with self.assertRaises(RecordValidationError):
                supersede_packet(
                    store,
                    task_id=task["task_id"],
                    old_decision_id="DDR-20260717-001",
                    old_job_id="AJ-TASK-20260717-001-001",
                    replacement_decision=decision,
                    replacement_job=job,
                    replacement_role=role,
                    reason="",
                    evidence_refs=[],
                    prior_execution_status="unexecuted",
                    working_evidence_handling="None.",
                    expected_revision=2,
                    created_at=TS,
                )


if __name__ == "__main__":
    unittest.main()
