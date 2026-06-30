#!/usr/bin/env python3
"""Resolve the next website-local implementation boundary.

The resolver is intentionally read-only. It reports live implementation-control
state and fails closed when required control records are missing or malformed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM_STATE_RELATIVE_PATH = Path("implementation_control/program_state.yaml")
ACTIVE_JOB_STATUSES = {"active", "pending"}
NO_ACTION_STATUSES = {"complete", "completed", "closed", "inactive", "none"}
ALLOWED_GATE_STATUSES = {"not_required", "required", "approved", "blocked"}
KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


class ResolverError(ValueError):
    """Raised when implementation-control state cannot be resolved safely."""


class SimpleYamlError(ValueError):
    """Raised when the local YAML subset parser cannot parse a record."""


@dataclass(frozen=True)
class YamlLine:
    number: int
    indent: int
    text: str


def stable_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def clean_yaml_lines(text: str, path: Path) -> list[YamlLine]:
    lines: list[YamlLine] = []
    for number, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line:
            raise SimpleYamlError(f"{path}:{number}: tabs are not supported")
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        lines.append(YamlLine(number=number, indent=indent, text=raw_line.strip()))
    return lines


def split_key_value(text: str, path: Path, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise SimpleYamlError(f"{path}:{line_number}: expected 'key: value'")
    key, value = text.split(":", 1)
    key = key.strip()
    if not KEY_RE.match(key):
        raise SimpleYamlError(f"{path}:{line_number}: unsupported key {key!r}")
    return key, value.strip()


def parse_scalar(value: str) -> Any:
    if value == "":
        return None
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if re.fullmatch(r"-?[0-9]+", value):
        try:
            return int(value)
        except ValueError:
            return value
    return value


def parse_block(lines: list[YamlLine], index: int, indent: int, path: Path) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    if lines[index].indent < indent:
        return {}, index
    if lines[index].indent != indent:
        raise SimpleYamlError(
            f"{path}:{lines[index].number}: unexpected indentation "
            f"{lines[index].indent}; expected {indent}"
        )
    if lines[index].text.startswith("- "):
        return parse_list(lines, index, indent, path)
    return parse_map(lines, index, indent, path)


def parse_map(
    lines: list[YamlLine],
    index: int,
    indent: int,
    path: Path,
) -> tuple[dict[str, Any], int]:
    data: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise SimpleYamlError(
                f"{path}:{line.number}: unexpected indentation {line.indent}; expected {indent}"
            )
        if line.text.startswith("- "):
            break
        key, raw_value = split_key_value(line.text, path, line.number)
        if key in data:
            raise SimpleYamlError(f"{path}:{line.number}: duplicate key {key!r}")
        index += 1
        if raw_value:
            data[key] = parse_scalar(raw_value)
            continue
        if index < len(lines) and lines[index].indent > indent:
            value, index = parse_block(lines, index, lines[index].indent, path)
            data[key] = value
        else:
            data[key] = None
    return data, index


def parse_list(lines: list[YamlLine], index: int, indent: int, path: Path) -> tuple[list[Any], int]:
    data: list[Any] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise SimpleYamlError(
                f"{path}:{line.number}: unexpected indentation {line.indent}; expected {indent}"
            )
        if not line.text.startswith("- "):
            break
        item_text = line.text[2:].strip()
        index += 1
        if not item_text:
            if index >= len(lines) or lines[index].indent <= indent:
                data.append(None)
                continue
            value, index = parse_block(lines, index, lines[index].indent, path)
            data.append(value)
            continue
        if ":" in item_text:
            key, raw_value = split_key_value(item_text, path, line.number)
            item: dict[str, Any] = {key: parse_scalar(raw_value)}
            if index < len(lines) and lines[index].indent > indent:
                nested, index = parse_block(lines, index, lines[index].indent, path)
                if not isinstance(nested, dict):
                    raise SimpleYamlError(
                        f"{path}:{lines[index - 1].number}: list item mapping expected"
                    )
                overlap = set(item).intersection(nested)
                if overlap:
                    duplicate = sorted(overlap)[0]
                    raise SimpleYamlError(
                        f"{path}:{line.number}: duplicate list item key {duplicate!r}"
                    )
                item.update(nested)
            data.append(item)
            continue
        data.append(parse_scalar(item_text))
    return data, index


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ResolverError(f"{relative_label(path)} is missing") from exc
    lines = clean_yaml_lines(text, path)
    if not lines:
        raise ResolverError(f"{relative_label(path)} is empty")
    data, index = parse_block(lines, 0, lines[0].indent, path)
    if index != len(lines):
        line = lines[index]
        raise SimpleYamlError(f"{path}:{line.number}: unparsed content")
    if not isinstance(data, dict):
        raise ResolverError(f"{relative_label(path)}: top-level YAML value must be a mapping")
    return data


def relative_label(path: Path, repo_root: Path | None = None) -> str:
    base = (repo_root or REPO_ROOT).resolve()
    try:
        return path.resolve().relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def as_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ResolverError(f"{label} must be a mapping")
    return value


def as_list(value: Any, label: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ResolverError(f"{label} must be a list")
    return value


def optional_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def optional_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def safe_relative_path(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ResolverError(f"{label} must be a nonempty relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ResolverError(f"{label} must stay inside the website repository: {value!r}")
    return path


def read_record(repo_root: Path, relative_path: Path, label: str) -> dict[str, Any]:
    path = repo_root / relative_path
    if not path.is_file():
        raise ResolverError(f"{label} is missing: {relative_path.as_posix()}")
    try:
        return load_yaml(path)
    except SimpleYamlError as exc:
        raise ResolverError(str(exc)) from exc


def normalize_gates(raw_gates: Any, source: str) -> list[dict[str, str]]:
    gates: list[dict[str, str]] = []
    if raw_gates is None:
        return gates
    if isinstance(raw_gates, dict):
        for gate_id in sorted(raw_gates):
            gate_payload = raw_gates[gate_id]
            if isinstance(gate_payload, dict):
                status = str(gate_payload.get("status", ""))
                reason = str(gate_payload.get("reason", gate_payload.get("trigger", "")))
            else:
                status = str(gate_payload)
                reason = ""
            gates.append(
                {
                    "id": str(gate_id),
                    "status": status,
                    "reason": reason,
                    "source": source,
                }
            )
        return gates
    if isinstance(raw_gates, list):
        for index, item in enumerate(raw_gates):
            if not isinstance(item, dict):
                raise ResolverError(f"{source}.approval_gates[{index}] must be a mapping")
            gate_id = str(item.get("id", ""))
            if not gate_id:
                raise ResolverError(f"{source}.approval_gates[{index}] must declare id")
            gates.append(
                {
                    "id": gate_id,
                    "status": str(item.get("status", "")),
                    "reason": str(item.get("reason", item.get("trigger", ""))),
                    "source": source,
                }
            )
        return gates
    raise ResolverError(f"{source}.approval_gates must be a mapping or list")


def summarize_approval_gates(gates: list[dict[str, str]]) -> dict[str, Any]:
    invalid = [
        gate["id"]
        for gate in gates
        if gate.get("status") not in ALLOWED_GATE_STATUSES
    ]
    required = [gate["id"] for gate in gates if gate.get("status") == "required"]
    approved = [gate["id"] for gate in gates if gate.get("status") == "approved"]
    blocked = [gate["id"] for gate in gates if gate.get("status") == "blocked"]
    not_required = [gate["id"] for gate in gates if gate.get("status") == "not_required"]
    if invalid:
        aggregate_status = "invalid"
    elif required:
        aggregate_status = "approval_required"
    else:
        aggregate_status = "ready"
    return {
        "aggregate_status": aggregate_status,
        "approved": sorted(set(approved)),
        "blocked": sorted(set(blocked)),
        "gates": gates,
        "invalid": sorted(set(invalid)),
        "not_required": sorted(set(not_required)),
        "required": sorted(set(required)),
    }


def flatten_path_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        paths: list[str] = []
        for item in value:
            paths.extend(flatten_path_values(item))
        return paths
    if isinstance(value, dict):
        paths = []
        for nested_value in value.values():
            paths.extend(flatten_path_values(nested_value))
        return paths
    return []


def validate_write_boundaries(
    write_paths: list[str],
    *,
    upstream_root: str,
    label: str,
) -> list[str]:
    errors: list[str] = []
    for write_path in write_paths:
        path = Path(write_path)
        if path.is_absolute():
            errors.append(f"{label}: allowed write path must be repo-relative: {write_path}")
            continue
        if ".." in path.parts:
            errors.append(f"{label}: allowed write path must not traverse upward: {write_path}")
        if upstream_root and write_path.startswith(upstream_root):
            errors.append(f"{label}: upstream write path is forbidden: {write_path}")
    return errors


def validator_summary(records: list[Any]) -> list[dict[str, Any]]:
    validators: list[dict[str, Any]] = []
    for item in records:
        if not isinstance(item, dict):
            continue
        validators.append(
            {
                "command": str(item.get("command", "")),
                "id": str(item.get("id", "")),
                "required": bool(item.get("required", item.get("required_for_current_job", False))),
                "status": str(item.get("status", "")) if item.get("status") is not None else "",
            }
        )
    return validators


def next_action_summary(value: Any) -> dict[str, str]:
    if isinstance(value, dict):
        return {
            "do_not_skip": str(value.get("do_not_skip", "")),
            "summary": str(value.get("summary", "")),
            "task_packet": str(value.get("task_packet", "")),
        }
    if isinstance(value, str):
        return {"do_not_skip": "", "summary": value, "task_packet": value}
    return {"do_not_skip": "", "summary": "", "task_packet": ""}


def collect_active_jobs(repo_root: Path, task_relative_path: Path) -> list[dict[str, str]]:
    jobs_dir = repo_root / task_relative_path.parent / "jobs"
    if not jobs_dir.is_dir():
        return []
    active_jobs: list[dict[str, str]] = []
    for job_path in sorted(jobs_dir.glob("*.yaml")):
        try:
            record = load_yaml(job_path)
        except (ResolverError, SimpleYamlError):
            continue
        status = str(record.get("status", ""))
        if status in ACTIVE_JOB_STATUSES:
            active_jobs.append(
                {
                    "job_id": str(record.get("job_id", "")),
                    "path": relative_label(job_path, repo_root),
                    "status": status,
                }
            )
    return active_jobs


def blocked_payload(repo_root: Path, errors: list[str]) -> dict[str, Any]:
    return {
        "active_task": {},
        "allowed_paths": {"reads": [], "writes": []},
        "approval_gates": {
            "aggregate_status": "blocked",
            "approved": [],
            "blocked": [],
            "gates": [],
            "invalid": [],
            "not_required": [],
            "required": [],
        },
        "boundary": {
            "deployment_status": "unknown",
            "mode": "website_local_implementation_control",
            "read_only": True,
            "upstream_write_status": "unknown",
        },
        "checkpoint": {},
        "current_job": {},
        "errors": errors,
        "latest_handoff": {},
        "next_recommended_action": {},
        "program_state_path": PROGRAM_STATE_RELATIVE_PATH.as_posix(),
        "repository": {"root": repo_root.as_posix()},
        "required_validators": [],
        "resolver": {
            "command": "continue_implementation",
            "read_only": True,
            "schema_version": "0.1",
        },
        "status": "blocked",
        "stop_conditions": [],
    }


def resolve_continue_context(repo_root: Path = REPO_ROOT) -> tuple[dict[str, Any], int]:
    repo_root = repo_root.resolve()
    errors: list[str] = []
    program_state_path = repo_root / PROGRAM_STATE_RELATIVE_PATH
    try:
        program_state = load_yaml(program_state_path)
    except (ResolverError, SimpleYamlError) as exc:
        return blocked_payload(repo_root, [str(exc)]), 1

    repository_boundary = optional_mapping(program_state.get("repository_boundary"))
    upstream_root = str(repository_boundary.get("upstream_source_repository", ""))
    active_task_pointer = optional_mapping(program_state.get("active_task"))
    current_job_pointer = optional_mapping(program_state.get("current_job"))
    handoff_pointer = optional_mapping(program_state.get("latest_handoff"))

    program_status = str(program_state.get("status", ""))
    if (
        program_status in NO_ACTION_STATUSES
        and not active_task_pointer
        and not current_job_pointer
        and not handoff_pointer
    ):
        payload = blocked_payload(repo_root, [])
        payload["status"] = "no_action"
        payload["errors"] = []
        payload["boundary"]["upstream_write_status"] = str(
            repository_boundary.get("upstream_write_status", "unknown")
        )
        payload["boundary"]["deployment_status"] = str(
            repository_boundary.get("deployment_status", "unknown")
        )
        payload["next_recommended_action"] = next_action_summary(
            program_state.get("next_recommended_action")
        )
        return payload, 0

    task_relative_path: Path | None = None
    job_relative_path: Path | None = None
    handoff_relative_path: Path | None = None
    markdown_handoff_relative_path: Path | None = None
    task_record: dict[str, Any] = {}
    job_record: dict[str, Any] = {}
    handoff_record: dict[str, Any] = {}

    try:
        if not active_task_pointer:
            raise ResolverError("active_task must be present unless program status is no-action")
        task_relative_path = safe_relative_path(active_task_pointer.get("path"), "active_task.path")
        task_record = read_record(repo_root, task_relative_path, "active task record")
        if str(task_record.get("task_id", "")) != str(active_task_pointer.get("task_id", "")):
            errors.append("active_task.task_id does not match task record")

        if current_job_pointer:
            job_relative_path = safe_relative_path(
                current_job_pointer.get("path"),
                "current_job.path",
            )
            job_record = read_record(repo_root, job_relative_path, "current job record")
            if str(job_record.get("job_id", "")) != str(current_job_pointer.get("job_id", "")):
                errors.append("current_job.job_id does not match job record")
            if str(job_record.get("task_id", "")) != str(task_record.get("task_id", "")):
                errors.append("current job task_id does not match active task")

        if handoff_pointer:
            handoff_relative_path = safe_relative_path(
                handoff_pointer.get("yaml_path"), "latest_handoff.yaml_path"
            )
            handoff_record = read_record(repo_root, handoff_relative_path, "latest handoff record")
            markdown_path_value = handoff_pointer.get("markdown_path")
            if markdown_path_value:
                markdown_handoff_relative_path = safe_relative_path(
                    markdown_path_value,
                    "latest_handoff.markdown_path",
                )
                if not (repo_root / markdown_handoff_relative_path).is_file():
                    errors.append(
                        "latest handoff Markdown file is missing: "
                        f"{markdown_handoff_relative_path.as_posix()}"
                    )
            if str(handoff_record.get("handoff_id", "")) != str(
                handoff_pointer.get("handoff_id", "")
            ):
                errors.append("latest_handoff.handoff_id does not match handoff record")
    except (ResolverError, SimpleYamlError) as exc:
        errors.append(str(exc))

    if task_relative_path is not None:
        active_jobs = collect_active_jobs(repo_root, task_relative_path)
        if len(active_jobs) > 1:
            job_ids = ", ".join(job["job_id"] for job in active_jobs)
            errors.append(f"more than one active or pending job is present: {job_ids}")
    else:
        active_jobs = []

    if repository_boundary.get("upstream_write_status") != "forbidden":
        errors.append("repository_boundary.upstream_write_status must be forbidden")

    task_allowed_writes = flatten_path_values(task_record.get("allowed_writes"))
    job_allowed_writes = flatten_path_values(job_record.get("allowed_writes"))
    errors.extend(
        validate_write_boundaries(
            task_allowed_writes,
            upstream_root=upstream_root,
            label="active task",
        )
    )
    errors.extend(
        validate_write_boundaries(
            job_allowed_writes,
            upstream_root=upstream_root,
            label="current job",
        )
    )

    task_upstream_writes = optional_mapping(task_record.get("allowed_writes")).get(
        "upstream_source_repository"
    )
    if optional_list(task_upstream_writes):
        errors.append("active task declares upstream source repository writes")

    gates = normalize_gates(task_record.get("approval_gates"), "active_task")
    gates.extend(normalize_gates(job_record.get("approval_gates"), "current_job"))
    approval_gates = summarize_approval_gates(gates)
    for invalid_gate_id in approval_gates["invalid"]:
        errors.append(f"approval gate has invalid status: {invalid_gate_id}")

    required_validators = validator_summary(
        optional_list(job_record.get("required_validators"))
        or optional_list(task_record.get("required_validators"))
        or optional_list(program_state.get("required_validators"))
    )

    if errors:
        return blocked_payload(repo_root, sorted(set(errors))), 1

    current_job_status = str(job_record.get("status", current_job_pointer.get("status", "")))
    if not job_record or current_job_status in NO_ACTION_STATUSES:
        status = "no_action"
    elif approval_gates["aggregate_status"] == "approval_required":
        status = "approval_required"
    else:
        status = "ready"

    task_id = str(task_record.get("task_id", active_task_pointer.get("task_id", "")))
    job_id = str(job_record.get("job_id", current_job_pointer.get("job_id", "")))
    latest_handoff_id = str(handoff_record.get("handoff_id", handoff_pointer.get("handoff_id", "")))
    task_allowed_reads = flatten_path_values(task_record.get("allowed_reads"))
    job_allowed_reads = flatten_path_values(job_record.get("allowed_reads"))

    payload: dict[str, Any] = {
        "active_task": {
            "path": task_relative_path.as_posix() if task_relative_path else "",
            "status": str(task_record.get("status", active_task_pointer.get("status", ""))),
            "task_id": task_id,
            "title": str(task_record.get("title", active_task_pointer.get("title", ""))),
        },
        "active_jobs": active_jobs,
        "allowed_paths": {
            "reads": sorted(set(task_allowed_reads + job_allowed_reads)),
            "task_reads": task_allowed_reads,
            "task_writes": task_allowed_writes,
            "writes": sorted(set(task_allowed_writes + job_allowed_writes)),
            "job_reads": job_allowed_reads,
            "job_writes": job_allowed_writes,
        },
        "approval_gates": approval_gates,
        "boundary": {
            "deployment_status": str(repository_boundary.get("deployment_status", "unknown")),
            "mode": str(program_state.get("mode", "website_local_implementation_control")),
            "public_claim_authority": str(
                repository_boundary.get("public_claim_authority", "unknown")
            ),
            "read_only": True,
            "upstream_source_repository": upstream_root,
            "upstream_write_status": str(
                repository_boundary.get("upstream_write_status", "unknown")
            ),
            "website_repository": str(repository_boundary.get("website_repository", ".")),
        },
        "checkpoint": optional_mapping(job_record.get("checkpoint_expectations"))
        or optional_mapping(task_record.get("checkpoint_expectations")),
        "current_job": {
            "job_id": job_id,
            "path": job_relative_path.as_posix() if job_relative_path else "",
            "status": current_job_status,
            "title": str(job_record.get("title", current_job_pointer.get("title", ""))),
        },
        "errors": [],
        "latest_handoff": {
            "handoff_id": latest_handoff_id,
            "markdown_path": markdown_handoff_relative_path.as_posix()
            if markdown_handoff_relative_path
            else str(handoff_pointer.get("markdown_path", "")),
            "status": str(handoff_record.get("status", handoff_pointer.get("status", ""))),
            "yaml_path": handoff_relative_path.as_posix() if handoff_relative_path else "",
        },
        "next_recommended_action": next_action_summary(
            job_record.get("next_recommended_action")
            or handoff_record.get("next_recommended_action")
            or program_state.get("next_recommended_action")
        ),
        "program_state_path": PROGRAM_STATE_RELATIVE_PATH.as_posix(),
        "repository": {
            "name": str(program_state.get("repository", "")),
            "root": repo_root.as_posix(),
        },
        "required_validators": required_validators,
        "resolver": {
            "command": "continue_implementation",
            "read_only": True,
            "schema_version": "0.1",
        },
        "status": status,
        "stop_conditions": optional_list(job_record.get("stop_conditions"))
        or optional_list(task_record.get("stop_conditions")),
    }
    return payload, 0


def format_summary(payload: dict[str, Any]) -> str:
    status = str(payload.get("status", "unknown"))
    boundary = optional_mapping(payload.get("boundary"))
    active_task = optional_mapping(payload.get("active_task"))
    current_job = optional_mapping(payload.get("current_job"))
    latest_handoff = optional_mapping(payload.get("latest_handoff"))
    next_action = optional_mapping(payload.get("next_recommended_action"))
    approval_gates = optional_mapping(payload.get("approval_gates"))
    validators = optional_list(payload.get("required_validators"))
    allowed_paths = optional_mapping(payload.get("allowed_paths"))
    checkpoint = optional_mapping(payload.get("checkpoint"))

    lines = [
        f"Status: {status}",
        (
            "Boundary: website-local; upstream writes "
            f"{boundary.get('upstream_write_status', 'unknown')}; deployment "
            f"{boundary.get('deployment_status', 'unknown')}"
        ),
    ]
    if active_task:
        lines.append(
            "Active task: "
            f"{active_task.get('task_id', '')} "
            f"({active_task.get('status', '')}) - {active_task.get('title', '')}"
        )
    if current_job:
        lines.append(
            "Current job: "
            f"{current_job.get('job_id', '')} "
            f"({current_job.get('status', '')}) - {current_job.get('title', '')}"
        )
    if latest_handoff:
        lines.append(
            "Latest handoff: "
            f"{latest_handoff.get('handoff_id', '')} at {latest_handoff.get('yaml_path', '')}"
        )
    if next_action:
        lines.append(
            "Next recommended action: "
            f"{next_action.get('task_packet', '')} - {next_action.get('summary', '')}"
        )

    required_gates = approval_gates.get("required", [])
    blocked_gates = approval_gates.get("blocked", [])
    lines.append(
        "Approval gates: "
        f"{approval_gates.get('aggregate_status', 'unknown')}; "
        f"required={', '.join(required_gates) if required_gates else 'none'}; "
        f"blocked={', '.join(blocked_gates) if blocked_gates else 'none'}"
    )
    if validators:
        validator_text = "; ".join(
            f"{item.get('id', '')}: {item.get('command', '')}" for item in validators
        )
        lines.append(f"Required validators: {validator_text}")
    lines.append(
        "Allowed writes: "
        f"{len(optional_list(allowed_paths.get('writes')))} repo-relative path(s)"
    )
    lines.append(
        "Checkpoint: "
        f"automated={checkpoint.get('automated_checkpoint_command_available', False)}"
    )

    errors = optional_list(payload.get("errors"))
    if errors:
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in errors)
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve the next website-local implementation packet."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root containing implementation_control/.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a concise human-readable summary instead of JSON.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload, exit_code = resolve_continue_context(args.repo_root)
    if args.summary:
        print(format_summary(payload), end="")
    else:
        print(stable_json(payload), end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
