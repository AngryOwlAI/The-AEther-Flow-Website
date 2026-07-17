import copy
import tempfile
import unittest
from pathlib import Path

from _support import valid_completion, valid_decision, valid_handoff, valid_job, valid_role, valid_task
from agentjob_runtime.control.activation import activate_packet
from agentjob_runtime.control.completion import write_completion
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.handoff import write_handoff
from agentjob_runtime.errors import IntegrityError, RecordValidationError


class CompletionAndHandoffWriterTests(unittest.TestCase):
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

    def test_one_completion_and_one_handoff_finalize_with_revision_updates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, task = self.prepared_store(directory)
            completion_receipt = write_completion(
                store, valid_completion(), expected_revision=2, close_task=False
            )
            self.assertEqual(completion_receipt.task_revision, 3)
            handoff_receipt = write_handoff(store, valid_handoff(), expected_revision=3)
            self.assertEqual(handoff_receipt.task_revision, 4)
            self.assertFalse(handoff_receipt.grants_execution_authority)
            self.assertEqual(
                store.load_task(task["task_id"])["next_recommended_action"],
                valid_handoff()["next_action"]["objective"],
            )

    def test_duplicate_completion_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, _ = self.prepared_store(directory)
            write_completion(store, valid_completion(), expected_revision=2, close_task=False)
            with self.assertRaises(IntegrityError):
                write_completion(store, valid_completion(), expected_revision=3, close_task=False)

    def test_completion_outside_job_boundary_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, _ = self.prepared_store(directory)
            completion = valid_completion()
            completion["changed_paths"] = ["secrets/private.txt"]
            completion["outputs"] = []
            with self.assertRaises(RecordValidationError):
                write_completion(store, completion, expected_revision=2, close_task=False)

    def test_invalid_handoff_predecessor_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, _ = self.prepared_store(directory)
            write_completion(store, valid_completion(), expected_revision=2, close_task=False)
            handoff = valid_handoff()
            handoff["predecessor"]["completion_id"] = "AJC-MISSING"
            with self.assertRaises(RecordValidationError):
                write_handoff(store, handoff, expected_revision=3)

    def test_completion_can_close_task_without_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store, task = self.prepared_store(directory)
            receipt = write_completion(
                store,
                valid_completion(),
                expected_revision=2,
                close_task=True,
                next_recommended_action="No further action required.",
            )
            updated = store.load_task(task["task_id"])
            self.assertTrue(receipt.task_closed)
            self.assertEqual(updated["status"], "completed")
            self.assertEqual(updated["closure"]["completion_refs"], [valid_completion()["completion_id"]])


if __name__ == "__main__":
    unittest.main()
