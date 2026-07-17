import unittest

from _support import SCHEMA_ROOT, fixture_cases
from agentjob_runtime.validation.schema import validate_fragment


class CommonSchemaTests(unittest.TestCase):
    def test_common_definition_fixtures(self) -> None:
        for case in fixture_cases("common"):
            with self.subTest(case["name"]):
                issues = validate_fragment(
                    case["value"], SCHEMA_ROOT / "common.schema.json", f"/$defs/{case['definition']}"
                )
                self.assertEqual(not issues, case["valid"], issues)

    def test_unknown_extension_namespace_shape_is_rejected(self) -> None:
        issues = validate_fragment(
            {"Bad Namespace": {"version": "1.0.0", "required": True, "data": {}}},
            SCHEMA_ROOT / "common.schema.json",
            "/$defs/extensions",
        )
        self.assertTrue(issues)


if __name__ == "__main__":
    unittest.main()
