import tempfile
import unittest
from pathlib import Path

from _support import valid_decision, valid_job, valid_role, valid_task
from agentjob_runtime.control.activation import InjectedActivationFault, activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import StateConflict


class PacketActivationTests(unittest.TestCase):
    def make_store(self, directory: str):
        root = Path(directory).resolve()
        store = FilesystemControlStore(root, ".agents/control")
        task = valid_task()
        task["current_decision_id"] = None
        task["current_job_id"] = None
        store.create_task(task)
        return store, task

    def test_packet_becomes_authoritative_only_with_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, task = self.make_store(directory)
            receipt = activate_packet(
                store,
                task_id=task["task_id"],
                decision=valid_decision(),
                job=valid_job(),
                execution_role=valid_role(),
                expected_revision=1,
            )
            self.assertIn(receipt.job_id, store.activated_record_ids())
            self.assertTrue((store.project_root / receipt.activation_path).is_file())
            updated = store.load_task(task["task_id"])
            self.assertEqual(updated["revision"], 2)
            self.assertEqual(updated["current_job_id"], receipt.job_id)

    def test_fault_before_manifest_leaves_no_execution_authority(self) -> None:
        for boundary in ["staged", "director_decision", "agent_job", "execution_role"]:
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as directory:
                store, task = self.make_store(directory)
                with self.assertRaises(InjectedActivationFault):
                    activate_packet(
                        store,
                        task_id=task["task_id"],
                        decision=valid_decision(),
                        job=valid_job(),
                        execution_role=valid_role(),
                        expected_revision=1,
                        fault_after=boundary,
                    )
                self.assertNotIn(valid_job()["job_id"], store.activated_record_ids())
                self.assertEqual(store.load_task(task["task_id"])["revision"], 1)

    def test_revision_conflict_writes_no_packet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, task = self.make_store(directory)
            store.update_task_pointers(task["task_id"], expected_revision=1, status="blocked")
            with self.assertRaises(StateConflict):
                activate_packet(
                    store,
                    task_id=task["task_id"],
                    decision=valid_decision(),
                    job=valid_job(),
                    execution_role=valid_role(),
                    expected_revision=1,
                )
            self.assertEqual(store.activated_record_ids(), set())


if __name__ == "__main__":
    unittest.main()
