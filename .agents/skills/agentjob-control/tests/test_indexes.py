import tempfile
import unittest
from pathlib import Path

from _support import valid_decision, valid_job, valid_role, valid_task
from agentjob_runtime.control.activation import activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.indexes import generate_indexes
from agentjob_runtime.errors import IntegrityError


class DerivedIndexTests(unittest.TestCase):
    def activated_store(self, directory: str):
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
        return store

    def test_regeneration_is_deterministic_and_check_only_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.activated_store(directory)
            first = {path.name: path.read_bytes() for path in store.indexes_root.glob("*.json")}
            for path in store.indexes_root.glob("*.json"):
                path.unlink()
            receipt = generate_indexes(store)
            second = {path.name: path.read_bytes() for path in store.indexes_root.glob("*.json")}
            self.assertEqual(first, second)
            self.assertEqual(receipt.status, "pass")
            target = store.indexes_root / "AGENT_JOB_INDEX.json"
            target.write_text("{}\n", encoding="utf-8")
            check = generate_indexes(store, check=True)
            self.assertEqual(check.status, "drift")
            self.assertIn(store.relative(target), check.drifted)

    def test_duplicate_canonical_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.activated_store(directory)
            duplicate = valid_job()
            duplicate["status"] = "completed"
            duplicate["activated_at"] = None
            store.write_immutable(store.task_directory(duplicate["task_id"]) / "duplicate.json", duplicate)
            with self.assertRaises(IntegrityError):
                generate_indexes(store)

    def test_index_content_cannot_validate_an_invalid_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = self.activated_store(directory)
            index = store.indexes_root / "AGENT_JOB_INDEX.json"
            index.write_text('{"invented": "authority"}\n', encoding="utf-8")
            job_path = store.record_path("agent_job", "TASK-20260717-001", "AJ-TASK-20260717-001-001")
            self.assertEqual(store.read(job_path)["authority"]["network_access"], False)


if __name__ == "__main__":
    unittest.main()
