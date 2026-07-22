from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from scripts.implementation_control.continue_plan_goal import build_parser
from scripts.implementation_control.plan_goal_adapter import STATE_RELATIVE
from test_plan_goal_adapter import complete_only_plan_task, make_project


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
        "record-successor",
        "prepare-dispatch",
        "record-dispatch-ambiguous",
        "claim-generation",
        "consume-generation",
        "record-returned",
        "record-unknown",
        "record-protected-stop",
        "finalize-receipt",
        "verify-and-decide",
        "reserve-successor",
        "reconcile-dispatch",
        "abandon-unconsumed",
        "reconcile-consumed",
        "cancel",
        "activate",
        "adopt-worker",
        "worker-prepare",
        "worker-consume",
        "worker-fail",
        "worker-finalize",
        "worker-unknown",
        "reserve-next",
        "recover",
        "finalize-plan",
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


def test_prepare_finalize_plan_requires_both_cas_arguments():
    parser = build_parser()
    subparser_action = next(
        action for action in parser._actions if action.dest == "command"
    )
    subparser = subparser_action.choices["prepare-finalize-plan"]
    required = {
        action.dest for action in subparser._actions if action.required
    }
    assert "expected_plan_revision" in required
    assert "expected_control_sha256" in required
    assert "legacy_profile" in required


def test_every_legacy_mutation_requires_explicit_profile_selector():
    parser = build_parser()
    subparser_action = next(
        action for action in parser._actions if action.dest == "command"
    )
    for command in (
        "prepare-finalize-plan",
        "legacy-finalize-plan",
        "activate",
        "adopt-worker",
        "worker-prepare",
        "worker-consume",
        "worker-fail",
        "worker-finalize",
        "worker-unknown",
        "reserve-next",
        "recover",
    ):
        required = {
            action.dest
            for action in subparser_action.choices[command]._actions
            if action.required
        }
        assert "legacy_profile" in required


def test_standalone_mutations_require_control_cas_without_plan_revision():
    parser = build_parser()
    subparser_action = next(
        action for action in parser._actions if action.dest == "command"
    )
    for command in (
        "bootstrap-website-packet",
        "complete-bootstrap-website-packet",
    ):
        subparser = subparser_action.choices[command]
        required = {
            action.dest
            for action in subparser._actions
            if action.required
        }
        assert "expected_control_sha256" in required
        assert "expected_plan_revision" not in required


def test_facade_bootstraps_and_completes_one_standalone_packet(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    status_result = run_facade(fixture.root, "status")
    control_hash = json.loads(status_result.stdout)["website_control"][
        "control_sha256"
    ]
    common = (
        "--plan",
        fixture.plan_path.relative_to(fixture.root).as_posix(),
        "--binding",
        fixture.binding_path.relative_to(fixture.root).as_posix(),
        "--task-id",
        "TASK-001",
    )
    activation = run_facade(
        fixture.root,
        "bootstrap-website-packet",
        *common,
        "--expected-control-sha256",
        control_hash,
        "--authorization-message",
        "Authorize this exact standalone packet.",
        "--authorization-evidence-ref",
        "test:accepted-plan",
        "--timestamp",
        "2026-07-20T06:00:00Z",
    )
    assert activation.returncode == 0, activation.stdout + activation.stderr
    activated = json.loads(activation.stdout)
    artifact_relative = fixture.binding["tasks"]["TASK-001"][
        "allowed_writes"
    ][0]
    artifact = fixture.root / artifact_relative
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("bounded result\n", encoding="utf-8")

    completion = run_facade(
        fixture.root,
        "complete-bootstrap-website-packet",
        *common,
        "--expected-control-sha256",
        activated["website_control_sha256_after"],
        "--authorization-evidence-ref",
        "test:accepted-plan",
        "--validator-result",
        "validator-task-1=pass",
        "--changed-file",
        artifact_relative,
        "--completion-summary",
        "The exact standalone packet is complete.",
        "--timestamp",
        "2026-07-20T06:05:00Z",
    )
    assert completion.returncode == 0, completion.stdout + completion.stderr
    assert json.loads(completion.stdout)["status"] == "completed"


def test_facade_prepares_and_finalizes_legacy_completion(tmp_path: Path):
    fixture = make_project(tmp_path, task_count=1)
    finalized_task, control_sha256 = complete_only_plan_task(fixture)
    common = (
        "--plan-id",
        fixture.plan["plan_id"],
        "--expected-plan-revision",
        str(finalized_task["plan_revision"]),
        "--expected-control-sha256",
        control_sha256,
        "--current-holder-thread-id",
        "coordinator-thread-001",
    )
    prepared_result = run_facade(
        fixture.root,
        "prepare-finalize-plan",
        *common,
        "--legacy-profile",
        "coordinator_v2_legacy",
        "--timestamp",
        "2026-07-20T06:06:00Z",
    )
    assert prepared_result.returncode == 0, (
        prepared_result.stdout + prepared_result.stderr
    )
    prepared = json.loads(prepared_result.stdout)
    report_path = fixture.root / "reports/legacy-completion.json"
    report_path.parent.mkdir(parents=True)
    report_path.write_text(
        json.dumps(prepared["completion_report"], sort_keys=True) + "\n",
        encoding="utf-8",
    )
    finalized_result = run_facade(
        fixture.root,
        "legacy-finalize-plan",
        *common,
        "--legacy-profile",
        "coordinator_v2_legacy",
        "--completion-report",
        report_path.relative_to(fixture.root).as_posix(),
        "--completion-report-sha256",
        prepared["completion_report_sha256"],
        "--timestamp",
        "2026-07-20T06:07:00Z",
    )
    assert finalized_result.returncode == 0, (
        finalized_result.stdout + finalized_result.stderr
    )
    assert json.loads(finalized_result.stdout)["status"] == (
        "terminal_complete"
    )


def test_malformed_control_fails_closed_with_nonzero_json(tmp_path: Path):
    fixture = make_project(tmp_path, task_count=1)
    program = fixture.root / "implementation_control/program_state.yaml"
    program.write_text("status: [unsupported inline value]\n", encoding="utf-8")
    result = run_facade(fixture.root, "status")
    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "protected_stop"
    assert payload["reason_code"]
