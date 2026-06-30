#!/usr/bin/env python3
"""Validate and locally commit one completed implementation-control packet."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from implementation_control.continue_implementation import (  # noqa: E402
    ResolverError,
    flatten_path_values,
    load_yaml,
    resolve_continue_context,
    safe_relative_path,
)
from implementation_control.validate_implementation_control import (  # noqa: E402
    validate_implementation_control,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPLETION_PATH_KEYS = (
    "changed_files",
    "changed_paths",
    "files_changed",
    "repo_relative_changed_files",
)
COMPLETION_VALIDATOR_KEYS = (
    "validator_results",
    "validation_results",
    "validators",
    "validators_run",
)
COMPLETION_READY_STATUSES = {
    "complete",
    "completed",
    "ready_for_checkpoint",
    "ready_to_checkpoint",
}
MANUAL_COMMAND_PREFIX = "manual inspection of "


class CheckpointError(RuntimeError):
    """Raised when a checkpoint would be unsafe or incomplete."""


@dataclass(frozen=True)
class CommandResult:
    command: str
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class DirtyEntry:
    index_status: str
    worktree_status: str
    paths: tuple[str, ...]

    @property
    def is_staged(self) -> bool:
        return self.index_status not in {" ", "?"}


def stable_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def run_command(
    command: list[str],
    *,
    repo_root: Path,
) -> CommandResult:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    return CommandResult(
        command=shlex.join(command),
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def run_git(repo_root: Path, *args: str) -> CommandResult:
    return run_command(["git", "-C", repo_root.as_posix(), *args], repo_root=repo_root)


def require_git_success(result: CommandResult) -> None:
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        raise CheckpointError(f"{result.command} failed: {details}")


def load_relative_yaml(repo_root: Path, relative_path: str, label: str) -> dict[str, Any]:
    path = safe_relative_path(relative_path, label)
    record_path = repo_root / path
    if not record_path.is_file():
        raise CheckpointError(f"{label} is missing: {path.as_posix()}")
    data = load_yaml(record_path)
    if not isinstance(data, dict):
        raise CheckpointError(f"{label} must be a mapping: {path.as_posix()}")
    return data


def path_from_pointer(pointer: Any) -> str:
    if isinstance(pointer, str):
        return pointer
    if isinstance(pointer, dict):
        for key in ("path", "yaml_path", "completion_path"):
            value = pointer.get(key)
            if isinstance(value, str) and value:
                return value
    return ""


def find_completion_pointer(records: list[tuple[str, dict[str, Any]]]) -> tuple[str, str]:
    for label, record in records:
        key = "latest_completion" if label == "program_state" else "completion_record"
        value = record.get(key)
        path = path_from_pointer(value)
        if path:
            return label, path
    raise CheckpointError(
        "completion record is required before checkpointing; "
        "write the active job completion record first"
    )


def extract_completion_paths(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        paths: list[str] = []
        for item in value:
            paths.extend(extract_completion_paths(item))
        return paths
    if isinstance(value, dict):
        paths: list[str] = []
        for key in ("path", "file", "relative_path", "repo_relative_path"):
            item = value.get(key)
            if isinstance(item, str):
                paths.append(item)
        for key in ("paths", "files", "changed_files", "changed_paths"):
            paths.extend(extract_completion_paths(value.get(key)))
        return paths
    return []


def completion_changed_paths(completion: dict[str, Any]) -> list[Path]:
    paths: list[str] = []
    for key in COMPLETION_PATH_KEYS:
        paths.extend(extract_completion_paths(completion.get(key)))
    if not paths:
        raise CheckpointError("completion record must list changed files")

    normalized: list[Path] = []
    for index, path_value in enumerate(paths):
        try:
            normalized.append(safe_relative_path(path_value, f"completion.changed_files[{index}]"))
        except ResolverError as exc:
            raise CheckpointError(str(exc)) from exc
    return sorted(set(normalized), key=lambda item: item.as_posix())


def completion_validator_records(completion: dict[str, Any]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for key in COMPLETION_VALIDATOR_KEYS:
        value = completion.get(key)
        if not isinstance(value, list):
            continue
        for item in value:
            if not isinstance(item, dict):
                continue
            records.append(
                {
                    "command": str(item.get("command", "")),
                    "id": str(item.get("id", "")),
                    "status": str(item.get("status", "")),
                }
            )
    return records


def require_manual_validator_evidence(
    validator: dict[str, Any],
    completion: dict[str, Any],
) -> dict[str, str]:
    validator_id = str(validator.get("id", ""))
    command = str(validator.get("command", ""))
    for record in completion_validator_records(completion):
        if validator_id and record["id"] and record["id"] != validator_id:
            continue
        if command and record["command"] and record["command"] != command:
            continue
        if record["status"] in {"pass", "passed", "complete", "completed"}:
            return {
                "command": command,
                "id": validator_id,
                "mode": "completion-evidence",
                "status": record["status"],
            }
    raise CheckpointError(
        f"manual validator {validator_id or command!r} requires passed evidence "
        "in the completion record"
    )


def required_validators(
    job_record: dict[str, Any],
    task_record: dict[str, Any],
    program_state: dict[str, Any],
) -> list[dict[str, Any]]:
    for record in (job_record, task_record, program_state):
        validators = record.get("required_validators")
        if isinstance(validators, list) and validators:
            return [
                item
                for item in validators
                if isinstance(item, dict)
                and bool(item.get("required", item.get("required_for_current_job", False)))
            ]
    return []


def run_required_validators(
    *,
    repo_root: Path,
    validators: list[dict[str, Any]],
    completion: dict[str, Any],
    dry_run: bool,
) -> list[dict[str, str]]:
    if not validators:
        raise CheckpointError("active job must declare at least one required validator")

    receipts: list[dict[str, str]] = []
    for validator in validators:
        command = str(validator.get("command", ""))
        validator_id = str(validator.get("id", ""))
        if not command:
            raise CheckpointError(f"required validator {validator_id!r} has no command")
        if command.startswith(MANUAL_COMMAND_PREFIX):
            receipts.append(require_manual_validator_evidence(validator, completion))
            continue
        try:
            parts = shlex.split(command)
        except ValueError as exc:
            raise CheckpointError(f"validator command cannot be parsed: {command}") from exc
        if dry_run:
            receipts.append(
                {
                    "command": command,
                    "id": validator_id,
                    "mode": "dry-run",
                    "status": "not-run",
                }
            )
            continue
        result = run_command(parts, repo_root=repo_root)
        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip()
            raise CheckpointError(
                f"required validator failed ({validator_id or command}): {details}"
            )
        receipts.append(
            {
                "command": command,
                "id": validator_id,
                "mode": "executed",
                "status": "passed",
            }
        )
    return receipts


def path_is_within(candidate: Path, scope: Path) -> bool:
    if candidate == scope:
        return True
    return candidate.as_posix().startswith(f"{scope.as_posix().rstrip('/')}/")


def path_matches_any_scope(candidate: Path, scopes: list[Path]) -> bool:
    return any(path_is_within(candidate, scope) for scope in scopes)


def parse_porcelain_status(output: str) -> list[DirtyEntry]:
    entries: list[DirtyEntry] = []
    for raw_line in output.splitlines():
        if not raw_line:
            continue
        if len(raw_line) < 4:
            raise CheckpointError(f"unrecognized git status line: {raw_line!r}")
        index_status = raw_line[0]
        worktree_status = raw_line[1]
        path_text = raw_line[3:]
        if " -> " in path_text:
            paths = tuple(path_text.split(" -> ", 1))
        else:
            paths = (path_text,)
        entries.append(
            DirtyEntry(
                index_status=index_status,
                worktree_status=worktree_status,
                paths=paths,
            )
        )
    return entries


def inspect_dirty_state(
    *,
    dirty_entries: list[DirtyEntry],
    allowed_scopes: list[Path],
    packet_paths: list[Path],
) -> tuple[list[str], list[str]]:
    packet_path_set = {path.as_posix() for path in packet_paths}
    ignored: list[str] = []
    errors: list[str] = []
    packet_dirty: set[str] = set()

    for entry in dirty_entries:
        for path_text in entry.paths:
            try:
                path = safe_relative_path(path_text, f"git status path {path_text!r}")
            except ResolverError as exc:
                errors.append(str(exc))
                continue
            path_label = path.as_posix()
            if path_label in packet_path_set:
                packet_dirty.add(path_label)
                continue
            if path_matches_any_scope(path, allowed_scopes):
                errors.append(
                    "dirty path overlaps the active allowed write scope but is not "
                    f"listed by the completion record: {path_label}"
                )
                continue
            if entry.is_staged:
                errors.append(
                    "unrelated staged path would be included in git commit: "
                    f"{path_label}"
                )
                continue
            ignored.append(path_label)

    missing_dirty = sorted(packet_path_set - packet_dirty)
    if missing_dirty:
        errors.append(
            "completion-listed path has no dirty git entry: " + ", ".join(missing_dirty)
        )
    return sorted(set(ignored)), sorted(set(errors))


def commit_message(
    *,
    task_record: dict[str, Any],
    job_record: dict[str, Any],
    completion: dict[str, Any],
) -> str:
    job_id = str(job_record.get("job_id", "implementation-job"))
    task_id = str(task_record.get("task_id", "implementation-task"))
    completion_id = str(completion.get("completion_id", "implementation-completion"))
    summary = str(
        completion.get("summary")
        or completion.get("title")
        or job_record.get("title")
        or task_record.get("title")
        or "implementation packet"
    )
    summary = " ".join(summary.split())
    subject = f"Checkpoint {job_id}: {summary}"
    if len(subject) > 72:
        subject = subject[:69].rstrip() + "..."
    return "\n".join(
        [
            subject,
            "",
            f"Task: {task_id}",
            f"Job: {job_id}",
            f"Completion: {completion_id}",
        ]
    )


def checkpoint_transaction(
    repo_root: Path = REPO_ROOT,
    *,
    dry_run: bool = False,
    control_validator: Callable[[Path], list[str]] = validate_implementation_control,
) -> tuple[dict[str, Any], int]:
    repo_root = repo_root.resolve()

    git_check = run_git(repo_root, "rev-parse", "--is-inside-work-tree")
    if git_check.returncode != 0 or git_check.stdout.strip() != "true":
        raise CheckpointError(f"{repo_root.as_posix()} is not a Git working tree")

    control_errors = control_validator(repo_root)
    if control_errors:
        raise CheckpointError(
            "implementation-control validation failed before checkpoint:\n"
            + "\n".join(f"- {error}" for error in control_errors)
        )

    context, exit_code = resolve_continue_context(repo_root)
    if exit_code != 0:
        errors = context.get("errors", [])
        raise CheckpointError(
            "continue implementation resolver is blocked: "
            + "; ".join(str(error) for error in errors)
        )
    if context.get("status") != "ready":
        raise CheckpointError(f"active implementation state is not ready: {context.get('status')}")

    program_state = load_relative_yaml(
        repo_root,
        str(context.get("program_state_path", "")),
        "program_state",
    )
    task_record = load_relative_yaml(
        repo_root,
        str(context.get("active_task", {}).get("path", "")),
        "active_task",
    )
    job_record = load_relative_yaml(
        repo_root,
        str(context.get("current_job", {}).get("path", "")),
        "current_job",
    )
    handoff_path = str(context.get("latest_handoff", {}).get("yaml_path", ""))
    handoff_record = load_relative_yaml(repo_root, handoff_path, "latest_handoff")

    pointer_source, completion_path = find_completion_pointer(
        [
            ("current_job", job_record),
            ("active_task", task_record),
            ("latest_handoff", handoff_record),
            ("program_state", program_state),
        ]
    )
    completion = load_relative_yaml(repo_root, completion_path, "completion_record")
    if completion.get("record_type") != "implementation_completion":
        raise CheckpointError("completion_record.record_type must be implementation_completion")
    if str(completion.get("task_id", "")) != str(task_record.get("task_id", "")):
        raise CheckpointError("completion_record.task_id does not match active task")
    if str(completion.get("job_id", "")) != str(job_record.get("job_id", "")):
        raise CheckpointError("completion_record.job_id does not match current job")
    completion_status = str(completion.get("status", ""))
    if completion_status not in COMPLETION_READY_STATUSES:
        raise CheckpointError(
            "completion_record.status must be one of "
            f"{', '.join(sorted(COMPLETION_READY_STATUSES))}; found {completion_status!r}"
        )

    packet_paths = completion_changed_paths(completion)
    allowed_scopes = [
        safe_relative_path(path, "allowed_writes")
        for path in sorted(
            set(
                flatten_path_values(task_record.get("allowed_writes"))
                + flatten_path_values(job_record.get("allowed_writes"))
            )
        )
    ]
    for path in packet_paths:
        if not path_matches_any_scope(path, allowed_scopes):
            raise CheckpointError(
                "completion-listed path is not allowed by the active task/job: "
                f"{path.as_posix()}"
            )

    validator_receipts = run_required_validators(
        repo_root=repo_root,
        validators=required_validators(job_record, task_record, program_state),
        completion=completion,
        dry_run=dry_run,
    )

    status_result = run_git(repo_root, "status", "--porcelain=v1", "-uall")
    require_git_success(status_result)
    ignored_paths, dirty_errors = inspect_dirty_state(
        dirty_entries=parse_porcelain_status(status_result.stdout),
        allowed_scopes=allowed_scopes,
        packet_paths=packet_paths,
    )
    if dirty_errors:
        raise CheckpointError(
            "unsafe dirty state:\n" + "\n".join(f"- {error}" for error in dirty_errors)
        )

    staged_paths = [path.as_posix() for path in packet_paths]
    if not staged_paths:
        raise CheckpointError("no packet paths are available to stage")

    if dry_run:
        return (
            {
                "commit_hash": "",
                "completion_path": completion_path,
                "dry_run": True,
                "ignored_unrelated_paths": ignored_paths,
                "packet_paths": staged_paths,
                "pointer_source": pointer_source,
                "staged_paths": [],
                "status": "dry_run",
                "validators": validator_receipts,
            },
            0,
        )

    add_result = run_git(repo_root, "add", "--", *staged_paths)
    require_git_success(add_result)
    commit_result = run_git(
        repo_root,
        "commit",
        "-m",
        commit_message(task_record=task_record, job_record=job_record, completion=completion),
    )
    require_git_success(commit_result)
    hash_result = run_git(repo_root, "rev-parse", "HEAD")
    require_git_success(hash_result)
    commit_hash = hash_result.stdout.strip()

    return (
        {
            "commit_hash": commit_hash,
            "completion_path": completion_path,
            "dry_run": False,
            "ignored_unrelated_paths": ignored_paths,
            "packet_paths": staged_paths,
            "pointer_source": pointer_source,
            "staged_paths": staged_paths,
            "status": "committed",
            "validators": validator_receipts,
        },
        0,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root containing implementation_control/.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report the checkpoint without staging or committing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        payload, exit_code = checkpoint_transaction(args.repo_root, dry_run=args.dry_run)
    except CheckpointError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(stable_json(payload), end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
