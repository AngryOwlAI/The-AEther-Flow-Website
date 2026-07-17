import json
import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import RecordValidationError
from agentjob_runtime.records.canonical import (
    DuplicateKeyError,
    canonical_goal_text,
    content_sha256,
    goal_text_sha256,
    load_structured,
    render_canonical_json,
)


class CanonicalSerializationTests(unittest.TestCase):
    def test_equivalent_yaml_and_json_hash_identically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "record.json"
            yaml_path = root / "record.yaml"
            json_path.write_text('{"b": true, "a": 1}\n', encoding="utf-8")
            yaml_path.write_text("a: 1\nb: true\n", encoding="utf-8")
            json_record = load_structured(json_path)
            yaml_record = load_structured(yaml_path)
            self.assertEqual(json_record, yaml_record)
            self.assertEqual(content_sha256(json_record), content_sha256(yaml_record))
            self.assertEqual(
                content_sha256(json_record),
                "d918e8d1a9eb1f54b583326cad9950c771474b5c8ac1072bb0f2a0ad148d6de5",
            )

    def test_duplicate_keys_are_rejected_in_json_and_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "duplicate.json"
            yaml_path = root / "duplicate.yaml"
            json_path.write_text('{"a": 1, "a": 2}', encoding="utf-8")
            yaml_path.write_text("a: 1\na: 2\n", encoding="utf-8")
            with self.assertRaises(DuplicateKeyError):
                load_structured(json_path)
            with self.assertRaises(DuplicateKeyError):
                load_structured(yaml_path)

    def test_material_changes_and_extension_maps_change_hash(self) -> None:
        base = {
            "unicode": "Æther",
            "text": "line one\nline two",
            "enabled": True,
            "count": 1,
            "items": [1, False, None],
            "extensions": {"example": {"version": "1.0.0", "required": False, "data": {}}},
        }
        changed = json.loads(json.dumps(base))
        changed["count"] = 2
        self.assertNotEqual(content_sha256(base), content_sha256(changed))
        self.assertEqual(render_canonical_json(base), render_canonical_json(json.loads(render_canonical_json(base))))

    def test_goal_text_only_normalizes_line_endings(self) -> None:
        self.assertEqual(canonical_goal_text("  A\r\nB\r"), "  A\nB\n")
        self.assertEqual(goal_text_sha256("A\r\nB"), goal_text_sha256("A\nB"))
        self.assertNotEqual(goal_text_sha256(" A\nB"), goal_text_sha256("A\nB"))
        self.assertNotEqual(goal_text_sha256("A\nB\n"), goal_text_sha256("A\nB"))

    def test_non_finite_numbers_are_rejected(self) -> None:
        with self.assertRaises(RecordValidationError):
            content_sha256({"bad": float("nan")})


if __name__ == "__main__":
    unittest.main()
