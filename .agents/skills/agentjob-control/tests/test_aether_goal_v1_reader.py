from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from _support import PACKAGE_ROOT, RUNTIME_SCRIPTS
from agentjob_runtime.compat.aether_goal_v1 import (
    LegacyGoalReadOnlyError,
    read_legacy_goal,
    reject_legacy_write,
    render_legacy_goal,
)
from agentjob_runtime.errors import RecordValidationError


FIXTURE = PACKAGE_ROOT / "tests/fixtures/aether/legacy-goal-v1.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def sha256_json(value) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class AetherGoalV1ReaderTests(unittest.TestCase):
    def write_goal(self, root: Path, record: dict, *, name: str | None = None) -> Path:
        path = root / (name or f"goal-{record['goal_id']}.md")
        path.write_text(render_legacy_goal(record), encoding="utf-8")
        return path

    def test_golden_record_validates_exports_and_remains_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record = load_fixture()
            path = self.write_goal(Path(directory), record)
            before = path.read_bytes()
            result = read_legacy_goal(path)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(result["record"]["goal_id"], record["goal_id"])
            view = result["portable_view"]
            self.assertTrue(view["read_only"])
            self.assertFalse(view["mutation_supported"])
            self.assertEqual(view["legacy_goal_id"], view["portable_goal_id"])
            self.assertEqual(view["state"]["legacy_phase"], "terminal_complete")
            self.assertEqual(len(view["generation_receipts"]), 1)

    def test_hash_filename_and_serialization_drift_fail_closed(self) -> None:
        scenarios = []
        bad_hash = load_fixture()
        bad_hash["goal_sha256"] = "0" * 64
        scenarios.append((bad_hash, None))
        scenarios.append((load_fixture(), "goal-crg-20260717T150000Z-deadbeef.md"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index, (record, name) in enumerate(scenarios):
                with self.subTest(index=index):
                    path = self.write_goal(root, record, name=name)
                    with self.assertRaises(RecordValidationError):
                        read_legacy_goal(path)
                    path.unlink()
            record = load_fixture()
            path = self.write_goal(root, record)
            path.write_text(path.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
            with self.assertRaises(RecordValidationError):
                read_legacy_goal(path)

    def test_duplicate_generation_receipt_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record = copy.deepcopy(load_fixture())
            second = {
                "kind": "step_receipt",
                "payload": {"generation": 1, "invocation_count": 1, "status": "duplicate"},
                "prior_hash": record["journal"][0]["entry_hash"],
                "sequence": 2,
            }
            second["entry_hash"] = sha256_json(second)
            record["journal"].append(second)
            path = self.write_goal(Path(directory), record)
            with self.assertRaises(RecordValidationError):
                read_legacy_goal(path)

    def test_write_api_is_explicitly_unavailable(self) -> None:
        with self.assertRaises(LegacyGoalReadOnlyError):
            reject_legacy_write({"goal_id": "crg-example"})


if __name__ == "__main__":
    unittest.main()
