"""Strict structured parsing and deterministic protocol serialization."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError


class DuplicateKeyError(RecordValidationError):
    code = "record.duplicate_key"


class _DuplicateRejectingDecoder(json.JSONDecoder):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, object_pairs_hook=self._pairs, **kwargs)

    @staticmethod
    def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise DuplicateKeyError(f"duplicate JSON key: {key}")
            result[key] = value
        return result


def _strip_yaml_comment(line: str) -> str:
    quote: str | None = None
    escaped = False
    for index, character in enumerate(line):
        if escaped:
            escaped = False
            continue
        if quote and character == "\\":
            escaped = True
            continue
        if quote:
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
        elif character == "#":
            return line[:index]
    return line


def _split_inline(value: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    quote: str | None = None
    depth = 0
    for character in value:
        if quote:
            current.append(character)
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
            current.append(character)
        elif character in "[{":
            depth += 1
            current.append(character)
        elif character in "]}":
            depth -= 1
            current.append(character)
        elif character == "," and depth == 0:
            items.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    items.append("".join(current).strip())
    return items


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [_parse_scalar(item) for item in _split_inline(inner)]
    if value.startswith("{") and value.endswith("}"):
        inner = value[1:-1].strip()
        if not inner:
            return {}
        result: dict[str, Any] = {}
        for item in _split_inline(inner):
            key, separator, remainder = item.partition(":")
            if not separator:
                raise RecordValidationError(f"invalid inline YAML mapping item: {item}")
            normalized_key = str(_parse_scalar(key.strip()))
            if normalized_key in result:
                raise DuplicateKeyError(f"duplicate YAML key: {normalized_key}")
            result[normalized_key] = _parse_scalar(remainder)
        return result
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        if value.startswith('"'):
            return json.loads(value)
        return value[1:-1].replace("''", "'")
    if re.fullmatch(r"-?[0-9]+", value):
        return int(value)
    if re.fullmatch(r"-?(?:[0-9]+\\.[0-9]*|[0-9]*\\.[0-9]+)(?:[eE][+-]?[0-9]+)?", value):
        number = float(value)
        if not math.isfinite(number):
            raise RecordValidationError("non-finite YAML number is not allowed")
        return number
    return value


def parse_yaml_subset(text: str, *, source: str = "<yaml>") -> Any:
    """Parse the portable, dependency-free YAML subset used by templates.

    Anchors, aliases, merge keys, tags, block scalars, tabs, and duplicate keys
    are rejected. JSON remains the recommended canonical machine format.
    """

    if re.search(r"(^|\s)[&*!][A-Za-z0-9_-]+", text):
        raise RecordValidationError(f"{source}: YAML anchors, aliases, or tags are unsupported")
    lines: list[tuple[int, int, str]] = []
    for number, raw in enumerate(text.splitlines(), 1):
        leading = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in leading:
            raise RecordValidationError(f"{source}:{number}: tabs are not allowed")
        line = _strip_yaml_comment(raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        content = line[indent:]
        if content.endswith("|") or content.endswith(">"):
            raise RecordValidationError(f"{source}:{number}: block scalars are unsupported")
        lines.append((number, indent, content))
    if not lines:
        return None

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(lines):
            return {}, index
        number, actual, content = lines[index]
        if actual != indent:
            raise RecordValidationError(f"{source}:{number}: unexpected indentation {actual}")
        return parse_sequence(index, indent) if content.startswith("- ") else parse_mapping(index, indent)

    def parse_mapping(index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(lines):
            number, actual, content = lines[index]
            if actual < indent:
                break
            if actual > indent:
                raise RecordValidationError(f"{source}:{number}: unexpected indentation {actual}")
            if content.startswith("- "):
                break
            key, separator, remainder = content.partition(":")
            key = key.strip()
            if not separator or not key:
                raise RecordValidationError(f"{source}:{number}: expected key: value")
            if key in result:
                raise DuplicateKeyError(f"{source}:{number}: duplicate YAML key: {key}")
            remainder = remainder.strip()
            index += 1
            if remainder:
                result[key] = _parse_scalar(remainder)
            elif index < len(lines) and lines[index][1] > actual:
                result[key], index = parse_block(index, lines[index][1])
            else:
                result[key] = {}
        return result, index

    def parse_sequence(index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(lines):
            number, actual, content = lines[index]
            if actual < indent:
                break
            if actual > indent:
                raise RecordValidationError(f"{source}:{number}: unexpected indentation {actual}")
            if not content.startswith("- "):
                break
            item = content[2:].strip()
            index += 1
            if not item:
                if index < len(lines) and lines[index][1] > actual:
                    value, index = parse_block(index, lines[index][1])
                else:
                    value = None
                result.append(value)
                continue
            key, separator, remainder = item.partition(":")
            if separator and re.fullmatch(r"[A-Za-z0-9_.-]+", key.strip()):
                item_map: dict[str, Any] = {key.strip(): _parse_scalar(remainder) if remainder.strip() else {}}
                if index < len(lines) and lines[index][1] > actual:
                    nested, index = parse_block(index, lines[index][1])
                    if not isinstance(nested, dict):
                        raise RecordValidationError(f"{source}:{number}: sequence mapping expects keys")
                    for nested_key, nested_value in nested.items():
                        if nested_key in item_map:
                            raise DuplicateKeyError(f"{source}:{number}: duplicate YAML key: {nested_key}")
                        item_map[nested_key] = nested_value
                result.append(item_map)
            else:
                result.append(_parse_scalar(item))
        return result, index

    value, next_index = parse_block(0, lines[0][1])
    if next_index != len(lines):
        raise RecordValidationError(f"{source}:{lines[next_index][0]}: trailing YAML content")
    return value


def load_structured(path: str | Path) -> Any:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        try:
            return json.loads(text, cls=_DuplicateRejectingDecoder)
        except json.JSONDecodeError as error:
            raise RecordValidationError(f"{path}:{error.lineno}: invalid JSON: {error.msg}") from error
    if path.suffix.lower() in {".yaml", ".yml"}:
        return parse_yaml_subset(text, source=str(path))
    raise RecordValidationError(f"unsupported structured file type: {path.suffix}")


def normalize_json_value(value: Any, *, path: str = "$") -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RecordValidationError(f"{path}: non-finite number is not allowed")
        return value
    if isinstance(value, list):
        return [normalize_json_value(item, path=f"{path}[{index}]") for index, item in enumerate(value)]
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise RecordValidationError(f"{path}: object keys must be strings")
            result[key] = normalize_json_value(item, path=f"{path}.{key}")
        return result
    raise RecordValidationError(f"{path}: unsupported value type {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    normalized = normalize_json_value(value)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def render_canonical_json(value: Any) -> str:
    normalized = normalize_json_value(value)
    return json.dumps(normalized, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


def content_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def canonical_goal_text(value: str) -> str:
    if not isinstance(value, str):
        raise RecordValidationError("goal text must be a string")
    return value.replace("\r\n", "\n").replace("\r", "\n")


def goal_text_sha256(value: str) -> str:
    return hashlib.sha256(canonical_goal_text(value).encode("utf-8")).hexdigest()
