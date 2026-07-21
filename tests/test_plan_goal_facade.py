from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from scripts.implementation_control.continue_plan_goal import build_parser
from scripts.implementation_control.plan_goal_adapter import STATE_RELATIVE
from test_plan_goal_adapter import make_project


REPO_ROOT = Path(__file__).resolve().parents[1]
FACADE = REPO_ROOT / "scripts/implementation_control/continue_plan_goal.py"


def run_facade(root: Path, *arguments: str):
    return subprocess.run(
        [
            str(REPO_ROOT / ".venv/bin/python"),
            str(FACADE),
            "--repo-root",
            str(root),
            *arguments,
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def test_status_is_canonical_read_only_json(tmp_path: Path):
    fixture = make_project(tmp_path, task_count=1)
    state_path = fixture.root / STATE_RELATIVE
    assert not state_path.exists()
    result = run_facade(fixture.root, "status")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "no_action"
    assert payload["effects"]["state_writes"] == 0
    assert payload["plan_control"]["plans"] == []
    assert not state_path.exists()
    assert result.stdout == json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ) + "\n"


def test_prepare_is_read_only_and_binds_all_acceptance_values(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    result = run_facade(
        fixture.root,
        "prepare",
        "--plan",
        fixture.plan_path.relative_to(fixture.root).as_posix(),
        "--binding",
        fixture.binding_path.relative_to(fixture.root).as_posix(),
        "--current-thread-id",
        "coordinator-thread-001",
        "--current-profile-evidence-ref",
        "host:coordinator-thread-001:max",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] == "acceptance_required"
    assert payload["reasoning_effort"] == "max"
    assert payload["plan_sha256"] in payload["acceptance_text"]
    assert (
        payload["binding_manifest_sha256"]
        in payload["acceptance_text"]
    )
    assert (
        payload["website_control_sha256"]
        in payload["acceptance_text"]
    )
    assert payload["authorization"]["fresh_local_codex_tasks"] is True
    assert payload["effects"]["state_writes"] == 0
    assert not (fixture.root / STATE_RELATIVE).exists()


def test_every_mutating_subcommand_requires_both_cas_arguments():
    parser = build_parser()
    mutating = (
        "activate",
        "adopt-worker",
        "worker-prepare",
        "worker-consume",
        "worker-fail",
        "worker-finalize",
        "worker-unknown",
        "reserve-next",
        "recover",
    )
    for command in mutating:
        subparser_action = next(
            action
            for action in parser._actions
            if action.dest == "command"
        )
        subparser = subparser_action.choices[command]
        required = {
            action.dest
            for action in subparser._actions
            if action.required
        }
        assert "expected_plan_revision" in required
        assert "expected_control_sha256" in required


def test_malformed_control_fails_closed_with_nonzero_json(tmp_path: Path):
    fixture = make_project(tmp_path, task_count=1)
    program = fixture.root / "implementation_control/program_state.yaml"
    program.write_text("status: [unsupported inline value]\n", encoding="utf-8")
    result = run_facade(fixture.root, "status")
    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "protected_stop"
    assert payload["reason_code"]
