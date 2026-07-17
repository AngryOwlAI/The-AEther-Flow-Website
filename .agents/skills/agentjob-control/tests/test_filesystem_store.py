import os
import tempfile
import unittest
from pathlib import Path

from _support import valid_task
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import SecurityError, StateConflict


class FilesystemControlStoreTests(unittest.TestCase):
    def make_store(self, directory: str):
        root = Path(directory).resolve()
        store = FilesystemControlStore(root, ".agents/control")
        store.initialize_layout()
        return store

    def test_task_write_read_and_compare_and_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.make_store(directory)
            task = valid_task()
            task["current_decision_id"] = None
            task["current_job_id"] = None
            store.create_task(task)
            self.assertEqual(store.load_task(task["task_id"]), task)
            updated = store.update_task_pointers(
                task["task_id"], expected_revision=1, status="blocked", next_recommended_action="Repair state."
            )
            self.assertEqual(updated["revision"], 2)
            with self.assertRaises(StateConflict):
                store.update_task_pointers(task["task_id"], expected_revision=1, status="active")

    def test_staging_is_separate_and_non_authoritative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.make_store(directory)
            staging = store.create_staging_directory("ACT-TEST")
            store.write_immutable(staging / "draft.json", {"draft": True})
            self.assertEqual(store.activated_record_ids(), set())
            store.remove_staging_directory(staging)
            self.assertFalse(staging.exists())

    def test_traversal_and_symlink_writes_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.make_store(directory)
            with self.assertRaises(SecurityError):
                store.write_immutable("../../escape.json", {"bad": True})
            outside = Path(directory) / "outside"
            outside.mkdir()
            link = store.root / "tasks" / "linked"
            link.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(SecurityError):
                store.write_immutable(link / "record.json", {"bad": True})

    def test_hard_link_alias_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.make_store(directory)
            path = store.root / "tasks" / "source.json"
            store.write_immutable(path, {"value": 1})
            alias = store.root / "tasks" / "alias.json"
            os.link(path, alias)
            with self.assertRaises(SecurityError):
                store.read(path)


if __name__ == "__main__":
    unittest.main()
