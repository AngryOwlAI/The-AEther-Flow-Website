from __future__ import annotations

import json
from pathlib import Path

from implementation_control import continue_implementation as resolver


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_ready_fixture(
    repo_root: Path,
    *,
    gate_status: str = "not_required",
    job_status: str = "active",
    job_write: str = "scripts/implementation_control/continue_implementation.py",
    extra_active_job: bool = False,
) -> None:
    write_text(
        repo_root / "implementation_control/program_state.yaml",
        """
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
  title: "Resolver fixture"
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
  - id: "pytest"
    command: "python3 -m pytest"
    required_for_current_job: true
next_recommended_action:
  task_packet: "Task 3: Add Implementation-Control Validator"
  summary: "Add fail-closed validation for implementation-control records."
  do_not_skip: "Do not checkpoint or deploy before validation exists."
""".lstrip(),
    )
    write_text(
        repo_root / "implementation_control/tasks/WI-TEST-001/00_TASK.yaml",
        """
schema_version: "0.1"
record_type: "implementation_task"
task_id: "WI-TEST-001"
title: "Resolver fixture"
status: "active"
allowed_reads:
  website_repository:
    - "implementation_control/program_state.yaml"
  upstream_source_repository: []
allowed_writes:
  website_repository:
    - "scripts/implementation_control/continue_implementation.py"
  upstream_source_repository: []
approval_gates:
  public_claim_changes:
    status: "not_required"
    reason: "No public claim edits are in scope."
  upstream_source_project_writes:
    status: "blocked"
    reason: "The website control system cannot write upstream."
required_validators:
  - id: "pytest"
    command: "python3 -m pytest"
    required: true
stop_conditions:
  - "Required validation fails."
checkpoint_expectations:
  automated_checkpoint_command_available: false
""".lstrip(),
    )
    write_text(
        repo_root / "implementation_control/tasks/WI-TEST-001/jobs/WJ-TEST-001-A.yaml",
        f"""
schema_version: "0.1"
record_type: "implementation_job"
job_id: "WJ-TEST-001-A"
task_id: "WI-TEST-001"
title: "Add resolver"
status: "{job_status}"
execution_boundary:
  upstream_write_status: "forbidden"
allowed_reads:
  - "implementation_control/program_state.yaml"
allowed_writes:
  - "{job_write}"
approval_gates:
  - id: "public_claim_changes"
    status: "{gate_status}"
    trigger: "Any public scientific or governance claim edit."
  - id: "upstream_source_project_writes"
    status: "blocked"
    trigger: "Any write to the upstream source project."
required_validators:
  - id: "pytest"
    command: "python3 -m pytest"
    required: true
stop_conditions:
  - "The resolver would need to write files."
checkpoint_expectations:
  automated_checkpoint_command_available: false
next_recommended_action:
  task_packet: "Task 3: Add Implementation-Control Validator"
  summary: "Add fail-closed validation for implementation-control records."
""".lstrip(),
    )
    write_text(
        repo_root / "implementation_control/handoffs/WH-TEST-001.yaml",
        """
schema_version: "0.1"
record_type: "implementation_handoff"
handoff_id: "WH-TEST-001"
status: "active"
task_id: "WI-TEST-001"
job_id: "WJ-TEST-001-A"
next_recommended_action:
  task_packet: "Task 3: Add Implementation-Control Validator"
  summary: "Add fail-closed validation for implementation-control records."
""".lstrip(),
    )
    write_text(repo_root / "implementation_control/handoffs/WH-TEST-001.md", "# WH-TEST-001\n")
    if extra_active_job:
        write_text(
            repo_root / "implementation_control/tasks/WI-TEST-001/jobs/WJ-TEST-001-B.yaml",
            """
schema_version: "0.1"
record_type: "implementation_job"
job_id: "WJ-TEST-001-B"
task_id: "WI-TEST-001"
title: "Second active job"
status: "active"
""".lstrip(),
        )


def test_ready_state_reports_one_active_job(tmp_path: Path) -> None:
    write_ready_fixture(tmp_path)

    payload, exit_code = resolver.resolve_continue_context(tmp_path)

    assert exit_code == 0
    assert payload["status"] == "ready"
    assert payload["resolver"]["read_only"] is True
    assert payload["active_task"]["task_id"] == "WI-TEST-001"
    assert payload["current_job"]["job_id"] == "WJ-TEST-001-A"
    assert payload["latest_handoff"]["handoff_id"] == "WH-TEST-001"
    assert payload["next_recommended_action"]["task_packet"].startswith("Task 3")
    assert payload["active_jobs"] == [
        {
            "job_id": "WJ-TEST-001-A",
            "path": "implementation_control/tasks/WI-TEST-001/jobs/WJ-TEST-001-A.yaml",
            "status": "active",
        }
    ]
    assert json.loads(resolver.stable_json(payload))["status"] == "ready"


def test_summary_mode_uses_resolved_state(tmp_path: Path) -> None:
    write_ready_fixture(tmp_path)
    payload, _ = resolver.resolve_continue_context(tmp_path)

    summary = resolver.format_summary(payload)

    assert "Status: ready" in summary
    assert "Current job: WJ-TEST-001-A" in summary
    assert "Next recommended action: Task 3" in summary


def test_missing_program_state_blocks_closed(tmp_path: Path) -> None:
    payload, exit_code = resolver.resolve_continue_context(tmp_path)

    assert exit_code == 1
    assert payload["status"] == "blocked"
    assert any("program_state.yaml is missing" in error for error in payload["errors"])


def test_malformed_program_state_blocks_closed(tmp_path: Path) -> None:
    program_state = tmp_path / "implementation_control/program_state.yaml"
    write_text(program_state, "- not-a-map\n")

    payload, exit_code = resolver.resolve_continue_context(tmp_path)

    assert program_state.is_file()
    assert exit_code == 1
    assert payload["status"] == "blocked"
    assert any("top-level YAML value must be a mapping" in error for error in payload["errors"])


def test_required_approval_gate_reports_approval_required(tmp_path: Path) -> None:
    write_ready_fixture(tmp_path, gate_status="required")

    payload, exit_code = resolver.resolve_continue_context(tmp_path)

    assert exit_code == 0
    assert payload["status"] == "approval_required"
    assert payload["approval_gates"]["required"] == ["public_claim_changes"]


def test_no_action_state_is_not_an_error(tmp_path: Path) -> None:
    write_text(
        tmp_path / "implementation_control/program_state.yaml",
        """
schema_version: "0.1"
record_type: "implementation_program_state"
repository: "The-AEther-Flow-Website"
status: "completed"
repository_boundary:
  website_repository: "."
  upstream_source_repository: "/Volumes/P-SSD/AngryOwl/The-AEther-Flow"
  upstream_write_status: "forbidden"
  deployment_status: "not_authorized"
next_recommended_action:
  task_packet: ""
  summary: ""
""".lstrip(),
    )

    payload, exit_code = resolver.resolve_continue_context(tmp_path)

    assert exit_code == 0
    assert payload["status"] == "no_action"
    assert payload["errors"] == []


def test_no_action_state_ignores_superseded_historical_pointers(tmp_path: Path) -> None:
    write_text(
        tmp_path / "implementation_control/program_state.yaml",
        """
schema_version: "0.1"
record_type: "implementation_program_state"
repository: "The-AEther-Flow-Website"
status: "inactive"
repository_boundary:
  website_repository: "."
  upstream_source_repository: "/Volumes/P-SSD/AngryOwl/The-AEther-Flow"
  upstream_write_status: "forbidden"
  deployment_status: "not_authorized"
active_task:
  task_id: "WI-HISTORICAL-001"
  status: "superseded"
  path: "implementation_control/tasks/WI-HISTORICAL-001/00_TASK.yaml"
current_job:
  job_id: "WJ-HISTORICAL-001-A"
  status: "superseded"
  path: "implementation_control/tasks/WI-HISTORICAL-001/jobs/WJ-HISTORICAL-001-A.yaml"
latest_handoff:
  handoff_id: "WH-HISTORICAL-001"
  status: "superseded"
  yaml_path: "implementation_control/handoffs/WH-HISTORICAL-001.yaml"
next_recommended_action:
  task_packet: "none"
  summary: "Open a new bounded packet before implementation."
""".lstrip(),
    )

    payload, exit_code = resolver.resolve_continue_context(tmp_path)

    assert exit_code == 0
    assert payload["status"] == "no_action"
    assert payload["errors"] == []
    assert payload["active_task"] == {}
    assert payload["current_job"] == {}
    assert payload["latest_handoff"] == {}


def test_upstream_or_absolute_write_path_blocks(tmp_path: Path) -> None:
    write_ready_fixture(
        tmp_path,
        job_write="/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/program_state.yaml",
    )

    payload, exit_code = resolver.resolve_continue_context(tmp_path)

    assert exit_code == 1
    assert payload["status"] == "blocked"
    assert any("allowed write path must be repo-relative" in error for error in payload["errors"])


def test_more_than_one_active_job_blocks(tmp_path: Path) -> None:
    write_ready_fixture(tmp_path, extra_active_job=True)

    payload, exit_code = resolver.resolve_continue_context(tmp_path)

    assert exit_code == 1
    assert payload["status"] == "blocked"
    assert any("more than one active or pending job" in error for error in payload["errors"])
