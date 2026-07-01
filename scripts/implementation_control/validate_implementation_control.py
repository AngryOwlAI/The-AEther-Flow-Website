#!/usr/bin/env python3
"""Validate website-local implementation-control records.

This validator is intentionally read-only. A passing result means the local
control records are structurally coherent; it does not grant source authority,
deployment approval, or public-claim approval.
"""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from implementation_control.continue_implementation import (  # noqa: E402
    ACTIVE_JOB_STATUSES,
    ALLOWED_GATE_STATUSES,
    NO_ACTION_STATUSES,
    ResolverError,
    SimpleYamlError,
    flatten_path_values,
    load_yaml,
    normalize_gates,
    safe_relative_path,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM_STATE_RELATIVE_PATH = Path("implementation_control/program_state.yaml")
CONTROL_ROOT_RELATIVE_PATH = Path("implementation_control")
TASKS_RELATIVE_PATH = CONTROL_ROOT_RELATIVE_PATH / "tasks"
HANDOFFS_RELATIVE_PATH = CONTROL_ROOT_RELATIVE_PATH / "handoffs"
UPSTREAM_SOURCE_REPOSITORY = "/Volumes/P-SSD/AngryOwl/The-AEther-Flow"

REQUIRED_HIGH_RISK_GATES = {
    "public_claim_changes",
    "source_refresh_uncertainty",
    "broad_navigation_or_route_retirement",
    "shared_visual_systems",
    "public_downloadable_assets",
    "public_manifest_authority_records",
    "git_push",
    "cloudflare_deployment",
    "upstream_source_project_writes",
}

PACKAGE_SCRIPT = "validate:implementation-control"
PACKAGE_COMMAND = "python3 scripts/implementation_control/validate_implementation_control.py"
CHECKPOINT_SCRIPT = "checkpoint:implementation"
CHECKPOINT_COMMAND = (
    "python3 scripts/implementation_control/checkpoint_implementation_transaction.py"
)

DOCUMENTED_STANDALONE_COMMANDS = {
    ".venv/bin/python -m pytest",
    "git diff --check",
    "python3 -m pytest",
}

RISKY_WRITE_RULES = (
    ("public_manifest_authority_records", "public/files/manifests"),
    ("public_downloadable_assets", "public/files"),
    ("public_downloadable_assets", "public/assets"),
    ("broad_navigation_or_route_retirement", "src/pages"),
    ("shared_visual_systems", "src/components"),
    ("shared_visual_systems", "src/layouts"),
    ("shared_visual_systems", "src/styles"),
    ("shared_visual_systems", "src/lib"),
)


@dataclass(frozen=True)
class RecordRef:
    label: str
    path: Path
    data: dict[str, Any]


def load_record(repo_root: Path, relative_path: Path, label: str, errors: list[str]) -> RecordRef:
    path = repo_root / relative_path
    if not path.is_file():
        errors.append(f"{label} is missing: {relative_path.as_posix()}")
        return RecordRef(label=label, path=relative_path, data={})
    try:
        data = load_yaml(path)
    except (ResolverError, SimpleYamlError) as exc:
        errors.append(str(exc))
        return RecordRef(label=label, path=relative_path, data={})
    return RecordRef(label=label, path=relative_path, data=data)


def require_directory(repo_root: Path, relative_path: Path, errors: list[str]) -> None:
    if not (repo_root / relative_path).is_dir():
        errors.append(f"required directory is missing: {relative_path.as_posix()}")


def require_mapping(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be a mapping")
        return {}
    return value


def require_record_type(
    record: dict[str, Any],
    *,
    expected: str,
    label: str,
    errors: list[str],
) -> None:
    if record.get("record_type") != expected:
        errors.append(f"{label}.record_type must be {expected!r}")
    if not record.get("schema_version"):
        errors.append(f"{label}.schema_version is required")
    if not record.get("status"):
        errors.append(f"{label}.status is required")


def safe_pointer_path(
    pointer: dict[str, Any],
    key: str,
    label: str,
    errors: list[str],
) -> Path | None:
    try:
        return safe_relative_path(pointer.get(key), f"{label}.{key}")
    except ResolverError as exc:
        errors.append(str(exc))
        return None


def load_package_scripts(repo_root: Path, errors: list[str]) -> dict[str, str]:
    package_path = repo_root / "package.json"
    if not package_path.is_file():
        errors.append("package.json is missing")
        return {}
    try:
        package_json = json.loads(package_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"package.json is malformed JSON: {exc}")
        return {}
    scripts = package_json.get("scripts")
    if not isinstance(scripts, dict):
        errors.append("package.json scripts must be a mapping")
        return {}
    return {str(key): str(value) for key, value in scripts.items()}


def validate_package_wiring(scripts: dict[str, str], errors: list[str]) -> None:
    command = scripts.get(PACKAGE_SCRIPT)
    if command != PACKAGE_COMMAND:
        errors.append(f"package.json scripts.{PACKAGE_SCRIPT} must be {PACKAGE_COMMAND!r}")

    checkpoint_command = scripts.get(CHECKPOINT_SCRIPT)
    if checkpoint_command != CHECKPOINT_COMMAND:
        errors.append(
            f"package.json scripts.{CHECKPOINT_SCRIPT} must be {CHECKPOINT_COMMAND!r}"
        )

    validate_command = scripts.get("validate", "")
    implementation_step = f"npm run {PACKAGE_SCRIPT}"
    build_step = "npm run build"
    if implementation_step not in validate_command:
        errors.append(
            "package.json scripts.validate must include "
            "npm run validate:implementation-control"
        )
        return
    if build_step not in validate_command:
        errors.append("package.json scripts.validate must include npm run build")
        return
    if validate_command.index(implementation_step) > validate_command.index(build_step):
        errors.append("validate:implementation-control must run before npm run build")
    provenance_step = "npm run validate:provenance"
    if (
        provenance_step in validate_command
        and validate_command.index(implementation_step) < validate_command.index(provenance_step)
    ):
        errors.append("validate:implementation-control must run after npm run validate:provenance")


def normalize_gate_map(raw_gates: Any, label: str, errors: list[str]) -> dict[str, str]:
    try:
        gates = normalize_gates(raw_gates, label)
    except ResolverError as exc:
        errors.append(str(exc))
        return {}

    gate_map: dict[str, str] = {}
    for gate in gates:
        gate_id = gate["id"]
        status = gate["status"]
        if status not in ALLOWED_GATE_STATUSES:
            errors.append(f"{label}.approval_gates.{gate_id}: unsupported status {status!r}")
        if gate_id in gate_map:
            errors.append(f"{label}.approval_gates.{gate_id}: duplicate gate")
        gate_map[gate_id] = status

    missing = sorted(REQUIRED_HIGH_RISK_GATES - gate_map.keys())
    if missing:
        errors.append(f"{label}.approval_gates missing required gates: {', '.join(missing)}")
    if gate_map.get("upstream_source_project_writes") != "blocked":
        errors.append(f"{label}.approval_gates.upstream_source_project_writes must be blocked")
    return gate_map


def path_values_from_allowed_writes(value: Any, label: str, errors: list[str]) -> list[str]:
    if value is None:
        errors.append(f"{label}.allowed_writes is required")
        return []
    if isinstance(value, dict):
        upstream_writes = value.get("upstream_source_repository")
        if flatten_path_values(upstream_writes):
            errors.append(
                f"{label}.allowed_writes must not declare upstream source repository writes"
            )
    return flatten_path_values(value)


def validate_allowed_write_path(write_path: str, label: str, errors: list[str]) -> Path | None:
    if not isinstance(write_path, str) or not write_path.strip():
        errors.append(f"{label}: allowed write path must be a nonempty string")
        return None
    if write_path.startswith(UPSTREAM_SOURCE_REPOSITORY):
        errors.append(f"{label}: upstream write path is forbidden: {write_path}")
    path = Path(write_path)
    if path.is_absolute():
        errors.append(f"{label}: allowed write path must be repo-relative: {write_path}")
        return None
    if ".." in path.parts:
        errors.append(f"{label}: allowed write path must not traverse upward: {write_path}")
    if write_path in {".", "./", "/", "~"}:
        errors.append(f"{label}: allowed write path is too broad: {write_path}")
    if any(part in {"", "."} for part in path.parts):
        errors.append(f"{label}: allowed write path contains an empty or current-directory segment")
    if path.parts and path.parts[0] in {"..", "~"}:
        errors.append(f"{label}: allowed write path must stay inside the repository: {write_path}")
    return path


def risky_gate_for_path(path: Path) -> str | None:
    normalized = path.as_posix()
    for gate_id, prefix in RISKY_WRITE_RULES:
        if normalized == prefix or normalized.startswith(f"{prefix}/"):
            return gate_id
    return None


def validate_allowed_writes(
    record: dict[str, Any],
    *,
    label: str,
    gate_map: dict[str, str],
    errors: list[str],
) -> None:
    for write_path in path_values_from_allowed_writes(record.get("allowed_writes"), label, errors):
        path = validate_allowed_write_path(write_path, label, errors)
        if path is None:
            continue
        required_gate = risky_gate_for_path(path)
        if required_gate and gate_map.get(required_gate) != "approved":
            errors.append(
                f"{label}: allowed write {write_path!r} requires approved gate {required_gate}"
            )


def command_references_existing_script(command: str, repo_root: Path) -> bool:
    try:
        parts = shlex.split(command)
    except ValueError:
        return False
    if len(parts) < 2:
        return False
    executable = parts[0]
    if executable not in {"python3", "python", ".venv/bin/python"}:
        return False
    script_path = Path(parts[1])
    return script_path.parts[:1] == ("scripts",) and (repo_root / script_path).is_file()


def is_known_validator_command(
    command: str,
    repo_root: Path,
    package_scripts: dict[str, str],
) -> bool:
    if command in DOCUMENTED_STANDALONE_COMMANDS:
        return True
    if command.startswith("manual inspection of "):
        return True
    if command_references_existing_script(command, repo_root):
        return True
    if command.startswith("npm run "):
        try:
            parts = shlex.split(command)
        except ValueError:
            return False
        if len(parts) >= 3 and parts[0] == "npm" and parts[1] == "run":
            return parts[2] in package_scripts
    return False


def validate_validator_items(
    items: Any,
    *,
    label: str,
    repo_root: Path,
    package_scripts: dict[str, str],
    require_required_flag: bool,
    errors: list[str],
) -> None:
    if not isinstance(items, list) or not items:
        errors.append(f"{label}.required_validators must be a nonempty list")
        return
    seen_ids: set[str] = set()
    for index, item in enumerate(items):
        item_label = f"{label}.required_validators[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_label} must be a mapping")
            continue
        validator_id = item.get("id")
        command = item.get("command")
        if not isinstance(validator_id, str) or not validator_id:
            errors.append(f"{item_label}.id must be a nonempty string")
        elif validator_id in seen_ids:
            errors.append(f"{item_label}.id is duplicated: {validator_id}")
        else:
            seen_ids.add(validator_id)
        if not isinstance(command, str) or not command:
            errors.append(f"{item_label}.command must be a nonempty string")
        elif not is_known_validator_command(command, repo_root, package_scripts):
            errors.append(f"{item_label}.command is not a known validator command: {command}")
        if require_required_flag and not isinstance(
            item.get("required", item.get("required_for_current_job")),
            bool,
        ):
            errors.append(
                f"{item_label} must declare required or required_for_current_job as boolean"
            )


def validate_all_yaml_is_parseable(repo_root: Path, errors: list[str]) -> None:
    control_root = repo_root / CONTROL_ROOT_RELATIVE_PATH
    if not control_root.is_dir():
        return
    for yaml_path in sorted(control_root.rglob("*.yaml")):
        try:
            data = load_yaml(yaml_path)
        except (ResolverError, SimpleYamlError) as exc:
            errors.append(str(exc))
            continue
        if not isinstance(data.get("record_type"), str):
            relative = yaml_path.relative_to(repo_root).as_posix()
            errors.append(f"{relative}: record_type is required")


def validate_completion_pointer(
    pointer: Any,
    *,
    label: str,
    repo_root: Path,
    expected_task_id: str,
    expected_job_id: str,
    errors: list[str],
) -> None:
    if pointer is None:
        return
    path_value: Any
    if isinstance(pointer, str):
        path_value = pointer
        completion_id = ""
    elif isinstance(pointer, dict):
        path_value = (
            pointer.get("path")
            or pointer.get("yaml_path")
            or pointer.get("completion_path")
        )
        completion_id = str(pointer.get("completion_id", ""))
    else:
        errors.append(f"{label} must be a path string or mapping")
        return

    try:
        relative_path = safe_relative_path(path_value, label)
    except ResolverError as exc:
        errors.append(str(exc))
        return
    completion = load_record(repo_root, relative_path, label, errors).data
    if not completion:
        return
    require_record_type(
        completion,
        expected="implementation_completion",
        label=label,
        errors=errors,
    )
    if completion_id and completion.get("completion_id") != completion_id:
        errors.append(f"{label}.completion_id does not match completion record")
    if completion.get("task_id") != expected_task_id:
        errors.append(f"{label}.task_id does not match active task")
    if expected_job_id and completion.get("job_id") != expected_job_id:
        errors.append(f"{label}.job_id does not match current job")


def collect_active_jobs(repo_root: Path, task_path: Path, errors: list[str]) -> list[RecordRef]:
    jobs_dir = repo_root / task_path.parent / "jobs"
    if not jobs_dir.is_dir():
        errors.append(f"jobs directory is missing: {(task_path.parent / 'jobs').as_posix()}")
        return []
    active_jobs: list[RecordRef] = []
    for job_path in sorted(jobs_dir.glob("*.yaml")):
        relative = job_path.relative_to(repo_root)
        record = load_record(repo_root, relative, f"job record {relative.as_posix()}", errors)
        status = str(record.data.get("status", ""))
        if status in ACTIVE_JOB_STATUSES:
            active_jobs.append(record)
    return active_jobs


def validate_implementation_control(repo_root: Path = REPO_ROOT) -> list[str]:
    repo_root = repo_root.resolve()
    errors: list[str] = []

    require_directory(repo_root, CONTROL_ROOT_RELATIVE_PATH, errors)
    require_directory(repo_root, TASKS_RELATIVE_PATH, errors)
    require_directory(repo_root, HANDOFFS_RELATIVE_PATH, errors)
    validate_all_yaml_is_parseable(repo_root, errors)

    package_scripts = load_package_scripts(repo_root, errors)
    validate_package_wiring(package_scripts, errors)

    program = load_record(
        repo_root,
        PROGRAM_STATE_RELATIVE_PATH,
        "implementation_control/program_state.yaml",
        errors,
    ).data
    if not program:
        return sorted(set(errors))

    require_record_type(
        program,
        expected="implementation_program_state",
        label="program_state",
        errors=errors,
    )

    repository_boundary = require_mapping(
        program.get("repository_boundary"),
        "program_state.repository_boundary",
        errors,
    )
    if repository_boundary.get("upstream_source_repository") != UPSTREAM_SOURCE_REPOSITORY:
        errors.append(
            "program_state.repository_boundary.upstream_source_repository must name "
            f"{UPSTREAM_SOURCE_REPOSITORY}"
        )
    if repository_boundary.get("upstream_write_status") != "forbidden":
        errors.append("program_state.repository_boundary.upstream_write_status must be forbidden")
    if repository_boundary.get("deployment_status") not in {"not_authorized", "not-authorized"}:
        errors.append("program_state.repository_boundary.deployment_status must be not_authorized")

    validate_validator_items(
        program.get("required_validators"),
        label="program_state",
        repo_root=repo_root,
        package_scripts=package_scripts,
        require_required_flag=True,
        errors=errors,
    )

    program_status = str(program.get("status", ""))
    if program_status in NO_ACTION_STATUSES:
        return sorted(set(errors))

    active_task_pointer = require_mapping(
        program.get("active_task"),
        "program_state.active_task",
        errors,
    )
    current_job_pointer = require_mapping(
        program.get("current_job"),
        "program_state.current_job",
        errors,
    )
    handoff_pointer = require_mapping(
        program.get("latest_handoff"),
        "program_state.latest_handoff",
        errors,
    )

    task_path = safe_pointer_path(active_task_pointer, "path", "program_state.active_task", errors)
    job_path = safe_pointer_path(current_job_pointer, "path", "program_state.current_job", errors)
    handoff_yaml_path = safe_pointer_path(
        handoff_pointer,
        "yaml_path",
        "program_state.latest_handoff",
        errors,
    )
    handoff_markdown_path = safe_pointer_path(
        handoff_pointer,
        "markdown_path",
        "program_state.latest_handoff",
        errors,
    )

    if task_path is None or job_path is None or handoff_yaml_path is None:
        return sorted(set(errors))

    task_record = load_record(repo_root, task_path, "active task record", errors).data
    job_record = load_record(repo_root, job_path, "current job record", errors).data
    handoff_record = load_record(repo_root, handoff_yaml_path, "latest handoff record", errors).data

    if handoff_markdown_path and not (repo_root / handoff_markdown_path).is_file():
        errors.append(
            f"latest handoff Markdown file is missing: {handoff_markdown_path.as_posix()}"
        )

    require_record_type(
        task_record,
        expected="implementation_task",
        label="active_task",
        errors=errors,
    )
    require_record_type(
        job_record,
        expected="implementation_job",
        label="current_job",
        errors=errors,
    )
    require_record_type(
        handoff_record,
        expected="implementation_handoff",
        label="latest_handoff",
        errors=errors,
    )

    task_id = str(task_record.get("task_id", ""))
    job_id = str(job_record.get("job_id", ""))
    if active_task_pointer.get("task_id") != task_id:
        errors.append("program_state.active_task.task_id does not match task record")
    if current_job_pointer.get("job_id") != job_id:
        errors.append("program_state.current_job.job_id does not match job record")
    if job_record.get("task_id") != task_id:
        errors.append("current_job.task_id does not match active task")
    if handoff_pointer.get("handoff_id") != handoff_record.get("handoff_id"):
        errors.append("program_state.latest_handoff.handoff_id does not match handoff record")
    if handoff_record.get("task_id") != task_id:
        errors.append("latest_handoff.task_id does not match active task")
    if handoff_record.get("job_id") != job_id:
        errors.append("latest_handoff.job_id does not match current job")

    active_jobs = collect_active_jobs(repo_root, task_path, errors)
    if len(active_jobs) != 1:
        job_ids = ", ".join(str(job.data.get("job_id", "")) for job in active_jobs) or "none"
        errors.append(
            f"expected exactly one active or pending job; found {len(active_jobs)}: {job_ids}"
        )
    elif active_jobs[0].data.get("job_id") != job_id:
        errors.append("program_state.current_job is not the single active or pending job")

    task_gate_map = normalize_gate_map(task_record.get("approval_gates"), "active_task", errors)
    job_gate_map = normalize_gate_map(job_record.get("approval_gates"), "current_job", errors)
    validate_allowed_writes(task_record, label="active_task", gate_map=task_gate_map, errors=errors)
    validate_allowed_writes(job_record, label="current_job", gate_map=job_gate_map, errors=errors)

    validate_validator_items(
        task_record.get("required_validators"),
        label="active_task",
        repo_root=repo_root,
        package_scripts=package_scripts,
        require_required_flag=True,
        errors=errors,
    )
    validate_validator_items(
        job_record.get("required_validators"),
        label="current_job",
        repo_root=repo_root,
        package_scripts=package_scripts,
        require_required_flag=True,
        errors=errors,
    )
    if "required_validators" in handoff_record:
        validate_validator_items(
            handoff_record.get("required_validators"),
            label="latest_handoff",
            repo_root=repo_root,
            package_scripts=package_scripts,
            require_required_flag=False,
            errors=errors,
        )

    validate_completion_pointer(
        program.get("latest_completion"),
        label="program_state.latest_completion",
        repo_root=repo_root,
        expected_task_id=task_id,
        expected_job_id=job_id,
        errors=errors,
    )
    validate_completion_pointer(
        task_record.get("completion_record"),
        label="active_task.completion_record",
        repo_root=repo_root,
        expected_task_id=task_id,
        expected_job_id=job_id,
        errors=errors,
    )
    validate_completion_pointer(
        job_record.get("completion_record"),
        label="current_job.completion_record",
        repo_root=repo_root,
        expected_task_id=task_id,
        expected_job_id=job_id,
        errors=errors,
    )
    validate_completion_pointer(
        handoff_record.get("completion_record"),
        label="latest_handoff.completion_record",
        repo_root=repo_root,
        expected_task_id=task_id,
        expected_job_id=job_id,
        errors=errors,
    )

    return sorted(set(errors))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root containing implementation_control/.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_implementation_control(args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Implementation-control validation passed. "
        "This is structural control validation only, not source authority or deployment approval."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
