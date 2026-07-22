from __future__ import annotations

import json
from pathlib import Path

import pytest

from implementation_control import validate_implementation_control as validator

REPO_ROOT = Path(__file__).resolve().parents[1]

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


def replace_top_level_list_with_empty(path: Path, key: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start = next(index for index, line in enumerate(lines) if line == f"{key}:\n")
    end = start + 1
    while end < len(lines) and (lines[end].startswith(" ") or not lines[end].strip()):
        end += 1
    lines[start:end] = [f"{key}: []\n"]
    path.write_text("".join(lines), encoding="utf-8")


def gate_statuses(overrides: dict[str, str] | None = None) -> dict[str, str]:
    gates = {gate_id: "not_required" for gate_id in HIGH_RISK_GATES}
    gates["upstream_source_project_writes"] = "blocked"
    if overrides:
        gates.update(overrides)
    return gates


def gate_mapping(gates: dict[str, str]) -> str:
    lines: list[str] = []
    for gate_id, status in gates.items():
        lines.extend(
            [
                f"  {gate_id}:",
                f'    status: "{status}"',
                f'    reason: "Fixture gate {gate_id}."',
            ]
        )
    return "\n".join(lines)


def gate_list(gates: dict[str, str]) -> str:
    lines: list[str] = []
    for gate_id, status in gates.items():
        lines.extend(
            [
                f'  - id: "{gate_id}"',
                f'    status: "{status}"',
                f'    trigger: "Fixture gate {gate_id}."',
            ]
        )
    return "\n".join(lines)


def write_package_json(
    repo_root: Path,
    *,
    validate_script: str | None = None,
    include_validator_script: bool = True,
    include_checkpoint_script: bool = True,
) -> None:
    scripts = {
        "validate:content": "python3 scripts/validate_content_sources.py",
        "validate:provenance": "python3 scripts/validate_page_provenance.py",
        "build": "astro build",
        "validate": validate_script
        or (
            "npm run validate:content && npm run validate:provenance && "
            "npm run validate:implementation-control && npm run build"
        ),
    }
    if include_validator_script:
        scripts["validate:implementation-control"] = (
            "python3 scripts/implementation_control/validate_implementation_control.py"
        )
    if include_checkpoint_script:
        scripts["checkpoint:implementation"] = (
            "python3 scripts/implementation_control/checkpoint_implementation_transaction.py"
        )
    write_text(repo_root / "package.json", json.dumps({"scripts": scripts}, indent=2))


def write_valid_control_fixture(
    repo_root: Path,
    *,
    task_gate_overrides: dict[str, str] | None = None,
    job_gate_overrides: dict[str, str] | None = None,
    job_write: str = "scripts/implementation_control/validate_implementation_control.py",
    validator_command: str = "npm run validate:implementation-control",
    include_job_gate: str | None = None,
) -> None:
    write_package_json(repo_root)
    task_gates = gate_statuses(task_gate_overrides)
    job_gates = gate_statuses(job_gate_overrides)
    if include_job_gate is not None:
        job_gates = {key: value for key, value in job_gates.items() if key != include_job_gate}

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
  title: "Validator fixture"
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
  - id: "implementation-control"
    command: "{validator_command}"
    required_for_current_job: true
next_recommended_action:
  task_packet: "Task 3"
  summary: "Validate fixture."
""".lstrip(),
    )
    write_text(
        repo_root / "implementation_control/tasks/WI-TEST-001/00_TASK.yaml",
        f"""
schema_version: "0.1"
record_type: "implementation_task"
task_id: "WI-TEST-001"
title: "Validator fixture"
status: "active"
allowed_reads:
  website_repository:
    - "implementation_control/program_state.yaml"
  upstream_source_repository: []
allowed_writes:
  website_repository:
    - "scripts/implementation_control/validate_implementation_control.py"
    - "tests/test_validate_implementation_control.py"
  upstream_source_repository: []
approval_gates:
{gate_mapping(task_gates)}
required_validators:
  - id: "implementation-control"
    command: "{validator_command}"
    required: true
stop_conditions:
  - "Validation fails."
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
title: "Add validator"
status: "active"
execution_boundary:
  upstream_write_status: "forbidden"
allowed_reads:
  - "implementation_control/program_state.yaml"
allowed_writes:
  - "{job_write}"
approval_gates:
{gate_list(job_gates)}
required_validators:
  - id: "implementation-control"
    command: "{validator_command}"
    required: true
stop_conditions:
  - "Validation fails."
checkpoint_expectations:
  automated_checkpoint_command_available: false
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
  - id: "implementation-control"
    command: "{validator_command}"
    status: "passed"
next_recommended_action:
  task_packet: "Task 3"
  summary: "Validate fixture."
""".lstrip(),
    )
    write_text(repo_root / "implementation_control/handoffs/WH-TEST-001.md", "# WH-TEST-001\n")


def test_current_implementation_control_records_validate() -> None:
    assert validator.validate_implementation_control(REPO_ROOT) == []


def test_valid_fixture_passes(tmp_path: Path) -> None:
    write_valid_control_fixture(tmp_path)

    assert validator.validate_implementation_control(tmp_path) == []


def test_upstream_write_path_fails_closed(tmp_path: Path) -> None:
    write_valid_control_fixture(
        tmp_path,
        job_write="/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/program_state.yaml",
    )

    errors = validator.validate_implementation_control(tmp_path)

    assert any("upstream write path is forbidden" in error for error in errors)
    assert any("allowed write path must be repo-relative" in error for error in errors)


def test_high_risk_gate_is_required(tmp_path: Path) -> None:
    write_valid_control_fixture(tmp_path, include_job_gate="public_manifest_authority_records")

    errors = validator.validate_implementation_control(tmp_path)

    assert any(
        "missing required gates: public_manifest_authority_records" in error for error in errors
    )


def test_public_manifest_write_requires_approved_gate(tmp_path: Path) -> None:
    write_valid_control_fixture(
        tmp_path,
        job_write="public/files/manifests/source_manifest.json",
    )

    errors = validator.validate_implementation_control(tmp_path)

    assert any(
        "requires approved gate public_manifest_authority_records" in error for error in errors
    )


def test_public_manifest_write_passes_with_approved_gate(tmp_path: Path) -> None:
    write_valid_control_fixture(
        tmp_path,
        job_write="public/files/manifests/source_manifest.json",
        job_gate_overrides={"public_manifest_authority_records": "approved"},
    )

    assert validator.validate_implementation_control(tmp_path) == []


def test_unknown_required_validator_command_fails(tmp_path: Path) -> None:
    write_valid_control_fixture(tmp_path, validator_command="do-the-secret-check")

    errors = validator.validate_implementation_control(tmp_path)

    assert any("not a known validator command" in error for error in errors)


@pytest.mark.parametrize(
    "validator_command",
    [
        "/usr/bin/env AETHER_FLOW_SOURCE_COMMIT=c6aa66b9 npm run validate",
        "AETHER_FLOW_SOURCE_ROOT=/tmp/source npm run validate:content -- --strict",
        (
            "/usr/bin/env PYTHONDONTWRITEBYTECODE=1 "
            "python3 scripts/check_fixture.py --check"
        ),
        (
            "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest "
            "-p no:cacheprovider tests/test_fixture.py -q"
        ),
        "/usr/bin/env REVIEW_MODE=local manual inspection of rendered routes",
        "/usr/bin/env GIT_OPTIONAL_LOCKS=0 git diff --check -- tests",
    ],
)
def test_known_argument_bearing_or_environment_wrapped_validator_passes(
    tmp_path: Path,
    validator_command: str,
) -> None:
    write_valid_control_fixture(tmp_path, validator_command=validator_command)
    write_text(tmp_path / "scripts/check_fixture.py", "# Fixture validator.\n")

    assert validator.validate_implementation_control(tmp_path) == []


@pytest.mark.parametrize(
    "validator_command",
    [
        "/usr/bin/env SAFE_MODE=1 do-the-secret-check",
        "/usr/bin/env SAFE_MODE=1 npm run unknown-validator",
        "/usr/bin/env",
        "/usr/bin/env --",
        "/usr/bin/env -S 'npm run validate'",
        "BROKEN-NAME=1 npm run validate",
        "/usr/bin/env SAFE_MODE=1 npm run validate && do-the-secret-check",
    ],
)
def test_malformed_or_unknown_environment_wrapped_validator_fails(
    tmp_path: Path,
    validator_command: str,
) -> None:
    write_valid_control_fixture(tmp_path, validator_command=validator_command)

    errors = validator.validate_implementation_control(tmp_path)

    assert any("not a known validator command" in error for error in errors)


def test_inactive_program_allows_empty_required_validators(tmp_path: Path) -> None:
    write_valid_control_fixture(tmp_path)
    program_path = tmp_path / "implementation_control/program_state.yaml"
    program_text = program_path.read_text(encoding="utf-8").replace(
        'status: "active"',
        'status: "inactive"',
        1,
    )
    program_path.write_text(program_text, encoding="utf-8")
    replace_top_level_list_with_empty(program_path, "required_validators")

    assert validator.validate_implementation_control(tmp_path) == []


@pytest.mark.parametrize(
    ("relative_path", "record_label"),
    [
        ("implementation_control/program_state.yaml", "program_state"),
        ("implementation_control/tasks/WI-TEST-001/00_TASK.yaml", "active_task"),
        (
            "implementation_control/tasks/WI-TEST-001/jobs/WJ-TEST-001-A.yaml",
            "current_job",
        ),
    ],
)
def test_active_records_require_nonempty_required_validators(
    tmp_path: Path,
    relative_path: str,
    record_label: str,
) -> None:
    write_valid_control_fixture(tmp_path)
    replace_top_level_list_with_empty(tmp_path / relative_path, "required_validators")

    errors = validator.validate_implementation_control(tmp_path)

    assert (
        f"{record_label}.required_validators must be a nonempty list" in errors
    )


def test_package_wiring_must_include_validator_before_build(tmp_path: Path) -> None:
    write_valid_control_fixture(tmp_path)
    write_package_json(
        tmp_path,
        validate_script=(
            "npm run validate:content && npm run validate:provenance && "
            "npm run build && npm run validate:implementation-control"
        ),
    )

    errors = validator.validate_implementation_control(tmp_path)

    assert any("must run before npm run build" in error for error in errors)


def test_package_wiring_must_include_checkpoint_script(tmp_path: Path) -> None:
    write_valid_control_fixture(tmp_path)
    write_package_json(tmp_path, include_checkpoint_script=False)

    errors = validator.validate_implementation_control(tmp_path)

    assert any("scripts.checkpoint:implementation must be" in error for error in errors)
