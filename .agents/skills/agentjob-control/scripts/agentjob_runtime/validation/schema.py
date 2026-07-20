"""Dependency-free validator for the JSON Schema subset used by this package.

The repository intentionally avoids requiring ``jsonschema`` at runtime.  This
module implements only the Draft 2020-12 keywords present in the bundled
schemas.  Unsupported keywords are annotations, not silently interpreted as
security controls; schema authors must extend this module before depending on
additional validation behavior.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping


@dataclass(frozen=True, order=True)
class SchemaIssue:
    """One stable schema-validation finding."""

    path: str
    code: str
    message: str


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _json_identity(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class _SchemaValidator:
    def __init__(self) -> None:
        self._cache: dict[Path, Any] = {}

    def load(self, path: Path) -> Any:
        path = path.resolve()
        if path not in self._cache:
            self._cache[path] = json.loads(path.read_text(encoding="utf-8"))
        return self._cache[path]

    def resolve_ref(self, ref: str, current_path: Path) -> tuple[Any, Path]:
        file_part, marker, fragment = ref.partition("#")
        schema_path = (current_path.parent / file_part).resolve() if file_part else current_path
        value = self.load(schema_path)
        if marker and fragment:
            if not fragment.startswith("/"):
                raise ValueError(f"unsupported JSON pointer: {ref}")
            for raw_part in fragment[1:].split("/"):
                part = raw_part.replace("~1", "/").replace("~0", "~")
                if isinstance(value, list):
                    if not part.isdigit():
                        raise ValueError(
                            f"non-numeric array index in JSON pointer: {ref}"
                        )
                    value = value[int(part)]
                else:
                    value = value[part]
        return value, schema_path

    def validate(self, value: Any, schema: Any, schema_path: Path, path: str = "$") -> list[SchemaIssue]:
        if schema is True:
            return []
        if schema is False:
            return [SchemaIssue(path, "schema.false", "value is forbidden by schema")]
        if not isinstance(schema, Mapping):
            return [SchemaIssue(path, "schema.invalid", "schema node must be an object or boolean")]

        issues: list[SchemaIssue] = []

        if "$ref" in schema:
            target, target_path = self.resolve_ref(str(schema["$ref"]), schema_path)
            issues.extend(self.validate(value, target, target_path, path))

        for index, child in enumerate(schema.get("allOf", [])):
            issues.extend(self.validate(value, child, schema_path, path))

        if "anyOf" in schema:
            branches = [self.validate(value, child, schema_path, path) for child in schema["anyOf"]]
            if not any(not branch for branch in branches):
                issues.append(SchemaIssue(path, "schema.any_of", "value matches no anyOf branch"))

        if "oneOf" in schema:
            branches = [self.validate(value, child, schema_path, path) for child in schema["oneOf"]]
            match_count = sum(not branch for branch in branches)
            if match_count != 1:
                issues.append(
                    SchemaIssue(path, "schema.one_of", f"value matches {match_count} oneOf branches, expected 1")
                )

        if "not" in schema and not self.validate(value, schema["not"], schema_path, path):
            issues.append(SchemaIssue(path, "schema.not", "value matches a forbidden schema"))

        if "if" in schema:
            condition_matches = not self.validate(value, schema["if"], schema_path, path)
            branch = schema.get("then") if condition_matches else schema.get("else")
            if branch is not None:
                issues.extend(self.validate(value, branch, schema_path, path))

        expected_type = schema.get("type")
        if expected_type is not None:
            expected = [expected_type] if isinstance(expected_type, str) else list(expected_type)
            if not any(_type_matches(value, item) for item in expected):
                label = " or ".join(expected)
                issues.append(SchemaIssue(path, "type", f"expected {label}"))
                return sorted(set(issues))

        if "const" in schema and value != schema["const"]:
            issues.append(SchemaIssue(path, "const", f"expected constant {schema['const']!r}"))
        if "enum" in schema and value not in schema["enum"]:
            issues.append(SchemaIssue(path, "enum", f"value {value!r} is not allowed"))

        if isinstance(value, dict):
            required = schema.get("required", [])
            for key in required:
                if key not in value:
                    issues.append(SchemaIssue(f"{path}.{key}", "required", "required property is missing"))

            if "minProperties" in schema and len(value) < schema["minProperties"]:
                issues.append(SchemaIssue(path, "object.min_properties", "object has too few properties"))
            if "maxProperties" in schema and len(value) > schema["maxProperties"]:
                issues.append(SchemaIssue(path, "object.max_properties", "object has too many properties"))

            properties = schema.get("properties", {})
            patterns = schema.get("patternProperties", {})
            for key, child_value in value.items():
                child_path = f"{path}.{key}"
                matched = False
                if key in properties:
                    matched = True
                    issues.extend(self.validate(child_value, properties[key], schema_path, child_path))
                for pattern, child_schema in patterns.items():
                    if re.search(pattern, key):
                        matched = True
                        issues.extend(self.validate(child_value, child_schema, schema_path, child_path))
                if not matched:
                    additional = schema.get("additionalProperties", True)
                    if additional is False:
                        issues.append(SchemaIssue(child_path, "object.additional_property", "property is not allowed"))
                    elif isinstance(additional, (dict, bool)):
                        issues.extend(self.validate(child_value, additional, schema_path, child_path))

            if "propertyNames" in schema:
                for key in value:
                    issues.extend(self.validate(key, schema["propertyNames"], schema_path, f"{path}.<key>"))

            for key, dependencies in schema.get("dependentRequired", {}).items():
                if key in value:
                    for dependency in dependencies:
                        if dependency not in value:
                            issues.append(
                                SchemaIssue(f"{path}.{dependency}", "dependent_required", f"required when {key} is present")
                            )

        if isinstance(value, list):
            if "minItems" in schema and len(value) < schema["minItems"]:
                issues.append(SchemaIssue(path, "array.min_items", "array has too few items"))
            if "maxItems" in schema and len(value) > schema["maxItems"]:
                issues.append(SchemaIssue(path, "array.max_items", "array has too many items"))
            if schema.get("uniqueItems"):
                identities = [_json_identity(item) for item in value]
                if len(identities) != len(set(identities)):
                    issues.append(SchemaIssue(path, "array.unique_items", "array items must be unique"))
            if "items" in schema:
                for index, child_value in enumerate(value):
                    issues.extend(self.validate(child_value, schema["items"], schema_path, f"{path}[{index}]"))
            if "contains" in schema:
                matches = sum(not self.validate(item, schema["contains"], schema_path, path) for item in value)
                minimum = schema.get("minContains", 1)
                maximum = schema.get("maxContains")
                if matches < minimum or (maximum is not None and matches > maximum):
                    issues.append(SchemaIssue(path, "array.contains", "array contains constraint failed"))

        if isinstance(value, str):
            if "minLength" in schema and len(value) < schema["minLength"]:
                issues.append(SchemaIssue(path, "string.min_length", "string is too short"))
            if "maxLength" in schema and len(value) > schema["maxLength"]:
                issues.append(SchemaIssue(path, "string.max_length", "string is too long"))
            if "pattern" in schema and re.search(schema["pattern"], value) is None:
                issues.append(SchemaIssue(path, "string.pattern", "string does not match required pattern"))
            if schema.get("format") == "date-time":
                try:
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    issues.append(SchemaIssue(path, "string.date_time", "string is not an RFC 3339 timestamp"))

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in schema and value < schema["minimum"]:
                issues.append(SchemaIssue(path, "number.minimum", "number is below minimum"))
            if "maximum" in schema and value > schema["maximum"]:
                issues.append(SchemaIssue(path, "number.maximum", "number is above maximum"))
            if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
                issues.append(SchemaIssue(path, "number.exclusive_minimum", "number is not above exclusive minimum"))
            if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
                issues.append(SchemaIssue(path, "number.exclusive_maximum", "number is not below exclusive maximum"))

        return sorted(set(issues))


def validate_instance(instance: Any, schema_path: str | Path) -> list[SchemaIssue]:
    """Validate one JSON-compatible value against a bundled schema."""

    path = Path(schema_path).resolve()
    validator = _SchemaValidator()
    schema = validator.load(path)
    return validator.validate(instance, schema, path)


def validate_fragment(
    instance: Any, schema_path: str | Path, json_pointer: str
) -> list[SchemaIssue]:
    """Validate against a named definition within a schema file."""

    path = Path(schema_path).resolve()
    validator = _SchemaValidator()
    schema, resolved_path = validator.resolve_ref(f"#{json_pointer}", path)
    return validator.validate(instance, schema, resolved_path)


def format_issues(issues: Iterable[SchemaIssue]) -> str:
    """Render deterministic human-readable findings."""

    return "\n".join(f"{issue.code} {issue.path}: {issue.message}" for issue in sorted(issues))
