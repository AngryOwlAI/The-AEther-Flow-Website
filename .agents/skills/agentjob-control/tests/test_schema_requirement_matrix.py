from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, Mapping

from _support import (
    SCHEMA_ROOT,
    valid_activation,
    valid_adapter,
    valid_completion,
    valid_config,
    valid_continuation_envelope,
    valid_continue_result,
    valid_decision,
    valid_goal,
    valid_goal_receipt,
    valid_handoff,
    valid_job,
    valid_policy,
    valid_role,
    valid_supersession,
    valid_task,
)
from agentjob_runtime.validation.schema import _SchemaValidator, validate_fragment, validate_instance


def _activation() -> dict[str, Any]:
    decision = valid_decision()
    job = valid_job()
    role = valid_role()
    decision["_path"] = ".agents/control/tasks/TASK-20260717-001/decision.json"
    job["_path"] = ".agents/control/tasks/TASK-20260717-001/job.json"
    role["_path"] = ".agents/control/tasks/TASK-20260717-001/role.json"
    return valid_activation(decision, job, role)


SCHEMA_FIXTURES = {
    "activation.schema.json": _activation,
    "agent-job.schema.json": valid_job,
    "completion.schema.json": valid_completion,
    "continuation-envelope.schema.json": valid_continuation_envelope,
    "continue-result.schema.json": valid_continue_result,
    "control-config.schema.json": valid_config,
    "director-decision.schema.json": valid_decision,
    "execution-role.schema.json": valid_role,
    "goal-state.schema.json": valid_goal,
    "goal-step-receipt.schema.json": valid_goal_receipt,
    "handoff.schema.json": valid_handoff,
    "policy-pack.schema.json": valid_policy,
    "project-adapter.schema.json": valid_adapter,
    "supersession.schema.json": valid_supersession,
    "task.schema.json": valid_task,
}


def _resolve_ref(ref: str, current_path: Path) -> tuple[Mapping[str, Any], Path]:
    file_part, marker, fragment = ref.partition("#")
    schema_path = (current_path.parent / file_part).resolve() if file_part else current_path
    value: Any = json.loads(schema_path.read_text(encoding="utf-8"))
    if marker and fragment:
        for raw_part in fragment.removeprefix("/").split("/"):
            part = raw_part.replace("~1", "/").replace("~0", "~")
            value = value[part]
    return value, schema_path


def _walk_active_schema(
    instance: Any,
    schema: Mapping[str, Any],
    schema_path: Path,
    path: tuple[str | int, ...] = (),
):
    validator = _SchemaValidator()
    if "$ref" in schema:
        target, target_path = _resolve_ref(str(schema["$ref"]), schema_path)
        yield from _walk_active_schema(instance, target, target_path, path)
    for child in schema.get("allOf", []):
        yield from _walk_active_schema(instance, child, schema_path, path)
    for keyword in ("anyOf", "oneOf"):
        for child in schema.get(keyword, []):
            if not validator.validate(instance, child, schema_path):
                yield from _walk_active_schema(instance, child, schema_path, path)
    if "if" in schema:
        branch = "then" if not validator.validate(instance, schema["if"], schema_path) else "else"
        if branch in schema:
            yield from _walk_active_schema(instance, schema[branch], schema_path, path)
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key in instance:
                yield "required", path, key
        for key, child in schema.get("properties", {}).items():
            if key in instance:
                yield from _walk_active_schema(instance[key], child, schema_path, (*path, key))
    if isinstance(instance, list) and "items" in schema:
        for index, value in enumerate(instance):
            yield from _walk_active_schema(value, schema["items"], schema_path, (*path, index))
    if "enum" in schema:
        yield "enum", path, tuple(schema["enum"])


def _parent(value: Any, path: tuple[str | int, ...]) -> Any:
    current = value
    for part in path:
        current = current[part]
    return current


class SchemaRequirementMatrixTests(unittest.TestCase):
    def test_every_schema_baseline_is_valid(self) -> None:
        for name, factory in SCHEMA_FIXTURES.items():
            with self.subTest(schema=name):
                self.assertFalse(validate_instance(factory(), SCHEMA_ROOT / name))

    def test_every_active_required_field_has_missing_and_wrong_shape_coverage(self) -> None:
        for name, factory in SCHEMA_FIXTURES.items():
            schema_path = SCHEMA_ROOT / name
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            baseline = factory()
            cases = {
                (path, key)
                for kind, path, key in _walk_active_schema(baseline, schema, schema_path)
                if kind == "required"
            }
            self.assertTrue(cases, name)
            for path, key in sorted(cases, key=repr):
                with self.subTest(schema=name, path=path, field=key, defect="missing"):
                    candidate = copy.deepcopy(baseline)
                    del _parent(candidate, path)[key]
                    self.assertTrue(validate_instance(candidate, schema_path))
                with self.subTest(schema=name, path=path, field=key, defect="wrong-shape"):
                    candidate = copy.deepcopy(baseline)
                    current = _parent(candidate, path)[key]
                    _parent(candidate, path)[key] = [] if isinstance(current, dict) else {}
                    self.assertTrue(validate_instance(candidate, schema_path))

    def test_every_active_controlled_enum_rejects_an_unknown_value(self) -> None:
        for name, factory in SCHEMA_FIXTURES.items():
            schema_path = SCHEMA_ROOT / name
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            baseline = factory()
            cases = {
                (path, choices)
                for kind, path, choices in _walk_active_schema(baseline, schema, schema_path)
                if kind == "enum" and path
            }
            for path, choices in sorted(cases, key=repr):
                with self.subTest(schema=name, path=path, choices=choices):
                    candidate = copy.deepcopy(baseline)
                    parent = _parent(candidate, path[:-1])
                    parent[path[-1]] = "__unsupported_enum_value__"
                    self.assertTrue(validate_instance(candidate, schema_path))

    def test_common_fragment_required_fields_and_enums_are_negative_tested(self) -> None:
        fragments = {
            "command": valid_job()["commands"]["approved"][0],
            "validationResult": valid_completion()["validator_results"][0],
            "claimBoundary": valid_job()["claim_boundary"],
            "humanGateRef": {"gate_id": "GATE-001", "status": "approved", "approval_ref": "APPROVAL-001"},
            "extensionValue": {"version": "1.0.0", "required": False, "data": {}},
        }
        common = json.loads((SCHEMA_ROOT / "common.schema.json").read_text(encoding="utf-8"))
        for definition, baseline in fragments.items():
            schema = common["$defs"][definition]
            self.assertFalse(validate_fragment(baseline, SCHEMA_ROOT / "common.schema.json", f"/$defs/{definition}"))
            for key in schema.get("required", []):
                with self.subTest(definition=definition, field=key):
                    candidate = copy.deepcopy(baseline)
                    del candidate[key]
                    self.assertTrue(validate_fragment(candidate, SCHEMA_ROOT / "common.schema.json", f"/$defs/{definition}"))
            for key, child in schema.get("properties", {}).items():
                if "enum" in child:
                    candidate = copy.deepcopy(baseline)
                    candidate[key] = "__unsupported_enum_value__"
                    self.assertTrue(validate_fragment(candidate, SCHEMA_ROOT / "common.schema.json", f"/$defs/{definition}"))

    def test_invalid_ids_duplicates_extensions_and_protocol_versions_fail(self) -> None:
        task = valid_task()
        task["task_id"] = "bad id"
        self.assertTrue(validate_instance(task, SCHEMA_ROOT / "task.schema.json"))
        job = valid_job()
        job["authority"]["allowed_write_paths"].append(job["authority"]["allowed_write_paths"][0])
        self.assertTrue(validate_instance(job, SCHEMA_ROOT / "agent-job.schema.json"))
        task = valid_task()
        task["extensions"] = {"invalid namespace": {"version": "1.0.0", "required": False, "data": {}}}
        self.assertTrue(validate_instance(task, SCHEMA_ROOT / "task.schema.json"))
        for name, factory in SCHEMA_FIXTURES.items():
            candidate = factory()
            candidate["schema_version"] = "sys4ai.unsupported.v999"
            with self.subTest(schema=name):
                self.assertTrue(validate_instance(candidate, SCHEMA_ROOT / name))


if __name__ == "__main__":
    unittest.main()
