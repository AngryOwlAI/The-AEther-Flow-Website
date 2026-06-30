from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from implementation_control import checkpoint_implementation_transaction as checkpoint

HIGH_RISK_GATES = [
    "public_claim_changes",
    "source_refresh_uncertainty",
    "broad_navigation_or_route_retirement",
    "shared_visual_systems",
    "public_downloadable_assets",
    "public_manifest_authority_records",
    "git_push",
    "cloudflare_deployment",
    "upstream_source_project_writes",
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", repo_root.as_posix(), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def require_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    result = run_git(repo_root, *args)
    assert result.returncode == 0, result.stderr or result.stdout
    return result


def gate_mapping() -> str:
    lines: list[str] = []
    for gate_id in HIGH_RISK_GATES:
        status = "blocked" if gate_id == "upstream_source_project_writes" else "not_required"
        lines.extend(
            [
                f"  {gate_id}:",
                f'    status: "{status}"',
                f'    reason: "Fixture gate {gate_id}."',
            ]
        )
    return "\n".join(lines)


def gate_list() -> str:
    lines: list[str] = []
    for gate_id in HIGH_RISK_GATES:
        status = "blocked" if gate_id == "upstream_source_project_writes" else "not_required"
        lines.extend(
            [
                f'  - id: "{gate_id}"',
                f'    status: "{status}"',
                f'    trigger: "Fixture gate {gate_id}."',
            ]
        )
    return "\n".join(lines)


def write_package_json(repo_root: Path) -> None:
    write_text(
        repo_root / "package.json",
        json.dumps(
            {
                "scripts": {
                    "build": "astro build",
                    "validate:content": "python3 scripts/validate_content_sources.py",
                    "validate:provenance": "python3 scripts/validate_page_provenance.py",
                    "validate:implementation-control": (
                        "python3 scripts/implementation_control/"
                        "validate_implementation_control.py"
                    ),
                    "checkpoint:implementation": (
                        "python3 scripts/implementation_control/"
                        "checkpoint_implementation_transaction.py"
                    ),
                    "validate": (
                        "npm run validate:content && npm run validate:provenance && "
                        "npm run validate:implementation-control && npm run build"
                    ),
                }
            },
            indent=2,
        )
        + "\n",
    )


def write_control_fixture(
    repo_root: Path,
    *,
    include_completion_pointer: bool = True,
    validator_command: str = "python3 scripts/pass_validator.py",
) -> None:
    completion_pointer = ""
    task_completion = ""
    if include_completion_pointer:
        completion_pointer = """
completion_record:
  completion_id: "WJC-TEST-001"
  path: "implementation_control/tasks/WI-TEST-001/jobs/completions/WJC-TEST-001.yaml"
""".rstrip()
        task_completion = completion_pointer

    write_package_json(repo_root)
    write_text(
        repo_root / "scripts/pass_validator.py",
        "raise SystemExit(0)\n",
    )
    write_text(
        repo_root / "implementation_control/program_state.yaml",
        f"""
schema_version: "0.1"
record_type: "implementation_program_state"
repository: "The-AEther-Flow-Website"
updated_utc: "2026-06-29T23:30:00Z"
status: "active"
mode: "website_local_implementation_control"
repository_boundary:
  website_repository: "."
  upstream_source_repository: "/Volumes/P-SSD/AngryOwl/The-AEther-Flow"
  upstream_write_status: "forbidden"
  public_claim_authority: "upstream_source_project_only"
  deployment_status: "not_authorized"
active_task:
  task_id: "WI-TEST-001"
  title: "Checkpoint fixture"
  status: "active"
  path: "implementation_control/tasks/WI-TEST-001/00_TASK.yaml"
current_job:
  job_id: "WJ-TEST-001-A"
  status: "active"
  path: "implementation_control/tasks/WI-TEST-001/jobs/WJ-TEST-001-A.yaml"
latest_handoff:
  handoff_id: "WH-TEST-001"
  status: "active"
  yaml_path: "implementation_control/handoffs/WH-TEST-001.yaml"
  markdown_path: "implementation_control/handoffs/WH-TEST-001.md"
required_validators:
  - id: "fixture-validator"
    command: "{validator_command}"
    required_for_current_job: true
next_recommended_action:
  task_packet: "Task fixture"
  summary: "Validate fixture."
""".lstrip(),
    )
    write_text(
        repo_root / "implementation_control/tasks/WI-TEST-001/00_TASK.yaml",
        f"""
schema_version: "0.1"
record_type: "implementation_task"
task_id: "WI-TEST-001"
title: "Checkpoint fixture"
status: "active"
allowed_reads:
  website_repository:
    - "implementation_control/program_state.yaml"
  upstream_source_repository: []
allowed_writes:
  website_repository:
    - "allowed/"
  upstream_source_repository: []
approval_gates:
{gate_mapping()}
required_validators:
  - id: "fixture-validator"
    command: "{validator_command}"
    required: true
stop_conditions:
  - "Validation fails."
checkpoint_expectations:
  automated_checkpoint_command_available: true
{task_completion}
""".lstrip(),
    )
    write_text(
        repo_root / "implementation_control/tasks/WI-TEST-001/jobs/WJ-TEST-001-A.yaml",
        f"""
schema_version: "0.1"
record_type: "implementation_job"
job_id: "WJ-TEST-001-A"
task_id: "WI-TEST-001"
title: "Checkpoint fixture job"
status: "active"
execution_boundary:
  upstream_write_status: "forbidden"
allowed_reads:
  - "implementation_control/program_state.yaml"
allowed_writes:
  - "allowed/"
approval_gates:
{gate_list()}
required_validators:
  - id: "fixture-validator"
    command: "{validator_command}"
    required: true
stop_conditions:
  - "Validation fails."
checkpoint_expectations:
  automated_checkpoint_command_available: true
{completion_pointer}
""".lstrip(),
    )
    write_text(
        repo_root / "implementation_control/handoffs/WH-TEST-001.yaml",
        f"""
schema_version: "0.1"
record_type: "implementation_handoff"
handoff_id: "WH-TEST-001"
status: "active"
task_id: "WI-TEST-001"
job_id: "WJ-TEST-001-A"
required_validators:
  - id: "fixture-validator"
    command: "{validator_command}"
    status: "passed"
next_recommended_action:
  task_packet: "Task fixture"
  summary: "Validate fixture."
""".lstrip(),
    )
    write_text(repo_root / "implementation_control/handoffs/WH-TEST-001.md", "# WH-TEST-001\n")
    if include_completion_pointer:
        write_text(
            repo_root
            / "implementation_control/tasks/WI-TEST-001/jobs/completions/WJC-TEST-001.yaml",
            f"""
schema_version: "0.1"
record_type: "implementation_completion"
completion_id: "WJC-TEST-001"
task_id: "WI-TEST-001"
job_id: "WJ-TEST-001-A"
status: "completed"
summary: "Commit the allowed fixture output"
changed_files:
  - "allowed/output.txt"
validator_results:
  - id: "fixture-validator"
    command: "{validator_command}"
    status: "passed"
""".lstrip(),
        )


def setup_repo(
    repo_root: Path,
    *,
    include_completion_pointer: bool = True,
    validator_command: str = "python3 scripts/pass_validator.py",
) -> None:
    write_control_fixture(
        repo_root,
        include_completion_pointer=include_completion_pointer,
        validator_command=validator_command,
    )
    write_text(repo_root / "allowed/output.txt", "before\n")
    require_git(repo_root, "init")
    require_git(repo_root, "config", "user.email", "checkpoint@example.test")
    require_git(repo_root, "config", "user.name", "Checkpoint Test")
    require_git(repo_root, "add", ".")
    require_git(repo_root, "commit", "-m", "Baseline fixture")
    write_text(repo_root / "allowed/output.txt", "after\n")


def commit_count(repo_root: Path) -> int:
    result = require_git(repo_root, "rev-list", "--count", "HEAD")
    return int(result.stdout.strip())


def porcelain(repo_root: Path) -> str:
    return require_git(repo_root, "status", "--porcelain=v1", "-uall").stdout


def test_checkpoint_commits_allowed_paths_and_preserves_unrelated_dirty(
    tmp_path: Path,
) -> None:
    setup_repo(tmp_path)
    write_text(tmp_path / "notes/unrelated.txt", "leave me alone\n")

    receipt, exit_code = checkpoint.checkpoint_transaction(tmp_path)

    assert exit_code == 0
    assert receipt["status"] == "committed"
    assert len(receipt["commit_hash"]) == 40
    assert receipt["staged_paths"] == ["allowed/output.txt"]
    assert receipt["ignored_unrelated_paths"] == ["notes/unrelated.txt"]
    assert commit_count(tmp_path) == 2
    assert porcelain(tmp_path).strip() == "?? notes/unrelated.txt"
    assert require_git(tmp_path, "show", "--name-only", "--format=", "HEAD").stdout.strip() == (
        "allowed/output.txt"
    )


def test_checkpoint_refuses_missing_completion_record(tmp_path: Path) -> None:
    setup_repo(tmp_path, include_completion_pointer=False)

    with pytest.raises(checkpoint.CheckpointError, match="completion record is required"):
        checkpoint.checkpoint_transaction(tmp_path)

    assert commit_count(tmp_path) == 1


def test_checkpoint_runs_validators_before_staging(tmp_path: Path) -> None:
    setup_repo(tmp_path, validator_command="python3 scripts/fail_validator.py")
    write_text(tmp_path / "scripts/fail_validator.py", "raise SystemExit(7)\n")
    require_git(tmp_path, "add", "scripts/fail_validator.py")
    require_git(tmp_path, "commit", "-m", "Add failing validator")

    with pytest.raises(checkpoint.CheckpointError, match="required validator failed"):
        checkpoint.checkpoint_transaction(tmp_path)

    assert commit_count(tmp_path) == 2
    assert "allowed/output.txt" not in require_git(
        tmp_path,
        "diff",
        "--cached",
        "--name-only",
    ).stdout


def test_checkpoint_blocks_ambiguous_dirty_overlap(tmp_path: Path) -> None:
    setup_repo(tmp_path)
    write_text(tmp_path / "allowed/unlisted.txt", "ambiguous\n")

    with pytest.raises(checkpoint.CheckpointError, match="overlaps the active allowed write"):
        checkpoint.checkpoint_transaction(tmp_path)

    assert commit_count(tmp_path) == 1


def test_checkpoint_blocks_unrelated_staged_file(tmp_path: Path) -> None:
    setup_repo(tmp_path)
    write_text(tmp_path / "notes/staged.txt", "staged unrelated\n")
    require_git(tmp_path, "add", "notes/staged.txt")

    with pytest.raises(checkpoint.CheckpointError, match="unrelated staged path"):
        checkpoint.checkpoint_transaction(tmp_path)

    assert commit_count(tmp_path) == 1


def test_checkpoint_dry_run_does_not_commit(tmp_path: Path) -> None:
    setup_repo(tmp_path)

    receipt, exit_code = checkpoint.checkpoint_transaction(tmp_path, dry_run=True)

    assert exit_code == 0
    assert receipt["status"] == "dry_run"
    assert receipt["staged_paths"] == []
    assert commit_count(tmp_path) == 1
