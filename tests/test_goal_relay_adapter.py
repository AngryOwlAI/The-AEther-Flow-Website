from __future__ import annotations

import copy
import stat
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_SCRIPTS = REPO_ROOT / "scripts/implementation_control"
VENDOR_SCRIPTS = REPO_ROOT / ".agents/skills/agentjob-control/scripts"
for import_root in (ADAPTER_SCRIPTS, VENDOR_SCRIPTS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

import goal_relay_adapter as adapter  # noqa: E402
from agentjob_runtime.validation.schema import validate_instance  # noqa: E402


HASH_A = "a" * 64
HASH_B = "b" * 64


def snapshot(
    root: Path,
    *,
    status: str = "ready",
    checkpoint_allowed: bool = True,
    exit_code: int = 0,
    fingerprint: str = HASH_A,
    task_id: str = "WI-FIXTURE-001",
    job_id: str = "WJ-FIXTURE-001-A",
    completion_id: str | None = None,
) -> adapter.WebsiteSnapshot:
    completion_path = "completion.yaml" if completion_id else None
    record_paths = {
        "program_state": "implementation_control/program_state.yaml",
        "task": "task.yaml",
        "job": "job.yaml",
        "handoff": "handoff.yaml",
        "handoff_markdown": "handoff.md",
        "completion": completion_path,
    }
    metadata = {
        "task": {
            "path": "task.yaml",
            "record_id": task_id,
            "record_type": "implementation_task",
            "status": "active",
        },
        "job": {
            "path": "job.yaml",
            "record_id": job_id,
            "record_type": "implementation_job",
            "status": "active",
        },
        "handoff": {
            "path": "handoff.yaml",
            "record_id": "WH-FIXTURE-001",
            "record_type": "implementation_handoff",
            "status": "current",
        },
    }
    if completion_id:
        metadata["completion"] = {
            "path": completion_path,
            "record_id": completion_id,
            "record_type": "implementation_completion",
            "status": "completed",
        }
    resolver = {
        "status": status,
        "active_task": {"task_id": task_id, "path": "task.yaml"},
        "current_job": {"job_id": job_id, "path": "job.yaml"},
        "latest_handoff": {
            "handoff_id": "WH-FIXTURE-001",
            "yaml_path": "handoff.yaml",
            "markdown_path": "handoff.md",
        },
        "allowed_paths": {
            "reads": ["src/fixture.py"],
            "writes": ["src/fixture.py"],
        },
        "approval_gates": {"aggregate_status": status},
        "boundary": {
            "source_authority": "upstream remains authoritative",
            "forbidden": ["public claim promotion"],
        },
        "checkpoint": {
            "staging_allowed_by_this_job": checkpoint_allowed,
            "push_allowed": False,
            "deploy_allowed": False,
        },
        "required_validators": [
            {"id": "focused", "command": "pytest", "required": True}
        ],
        "stop_conditions": ["scope change"],
        "next_recommended_action": {"summary": "Run one bounded fixture job."},
    }
    git = {
        "project_root": str(root),
        "worktree": str(root),
        "git_common_dir": str(root / ".git"),
        "head": "1" * 40,
        "branch": "main",
        "status": [],
    }
    return adapter.WebsiteSnapshot(
        repo_root=root,
        resolver=resolver,
        resolver_exit_code=exit_code,
        git=git,
        record_paths=record_paths,
        record_hashes={
            "program_state": "1" * 64,
            "task": "2" * 64,
            "job": "3" * 64,
            "handoff": "4" * 64,
            **({"completion": "5" * 64} if completion_id else {}),
        },
        record_metadata=metadata,
        fingerprint=fingerprint,
        source_authority={
            "boundary": resolver["boundary"],
            "task_source_context": {
                "accepted_source_commit": "57438af555214bc0785dcb390ee6254f580b8a62"
            },
            "handoff_source_authority_boundary": {
                "public_claim_promotion": "forbidden"
            },
        },
    )


@pytest.mark.parametrize(
    ("status", "checkpoint_allowed", "exit_code", "expected", "reason"),
    [
        (
            "ready",
            True,
            0,
            "no_action",
            "website.execution_not_attempted",
        ),
        (
            "approval_required",
            True,
            0,
            "human_gate_required",
            "website.approval_required",
        ),
        (
            "blocked",
            True,
            1,
            "control_repair_required",
            "website.control_repair_required",
        ),
        ("no_action", True, 0, "no_action", "website.no_action"),
        (
            "ready",
            False,
            0,
            "human_gate_required",
            "website.checkpoint_authority_required",
        ),
    ],
)
def test_pre_execution_boundaries_emit_zero_job_results(
    tmp_path: Path,
    status: str,
    checkpoint_allowed: bool,
    exit_code: int,
    expected: str,
    reason: str,
) -> None:
    before = snapshot(
        tmp_path,
        status=status,
        checkpoint_allowed=checkpoint_allowed,
        exit_code=exit_code,
    )
    result = adapter.build_continue_result(before)
    assert result["status"] == expected
    assert result["reason_code"] == reason
    assert result["agent_jobs_executed"] == 0
    assert result["execution_performed"] is False


def test_source_authority_and_job_scope_are_preserved_in_result(
    tmp_path: Path,
) -> None:
    before = snapshot(tmp_path)
    result = adapter.build_continue_result(before)
    extension = result["extensions"][adapter.ADAPTER_EXTENSION]["data"]
    assert extension["implementation_authority"] == "implementation_control"
    assert extension["allowed_paths"] == before.resolver["allowed_paths"]
    assert extension["approval_gates"] == before.resolver["approval_gates"]
    assert extension["source_authority"] == before.source_authority
    assert extension["checkpoint"]["status"] == "unknown"


def test_exact_checkpointed_completion_maps_and_validates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    before = snapshot(tmp_path)
    after = snapshot(
        tmp_path,
        fingerprint=HASH_B,
        completion_id="WJC-FIXTURE-001-A",
    )
    completion = {
        "summary": "The bounded fixture completed.",
        "validator_results": [
            {
                "id": "focused",
                "status": "passed",
                "evidence": "One focused test passed.",
            }
        ],
    }
    monkeypatch.setattr(adapter, "_completion_record", lambda value: completion)
    monkeypatch.setattr(
        adapter,
        "checkpoint_evidence",
        lambda value: {
            "provider": "website-checkpoint",
            "status": "pass",
            "revision": value.git["head"],
            "evidence_ref": value.record_paths["completion"],
        },
    )

    result = adapter.build_continue_result(
        before,
        after,
        execution_attempted=True,
    )
    assert result["status"] == "completed"
    assert result["agent_jobs_executed"] == 1
    assert result["completion_id"] == "WJC-FIXTURE-001-A"
    assert result["validators"] == {
        "required": 1,
        "passed": 1,
        "failed": 0,
        "warning": 0,
        "skipped": 0,
    }
    schema = (
        REPO_ROOT
        / ".agents/skills/agentjob-control/schemas/continue-result.schema.json"
    )
    assert validate_instance(result, schema) == []

    criteria = [
        {
            "criterion": "The focused adapter test passes.",
            "status": "pass",
            "evidence_refs": ["tests/test_goal_relay_adapter.py"],
        }
    ]
    evidence = adapter.build_direct_evidence(
        result,
        after,
        completion_contract_results=criteria,
    )
    assert evidence["completion_contract_results"] == criteria
    assert evidence["checkpoint"]["status"] == "pass"
    assert evidence["human_gate_outstanding"] is False
    assert evidence["extensions"][adapter.ADAPTER_EXTENSION]["data"][
        "source_authority"
    ] == after.source_authority


def test_active_task_or_job_change_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    before = snapshot(tmp_path)
    after = snapshot(
        tmp_path,
        fingerprint=HASH_B,
        job_id="WJ-FIXTURE-002-A",
        completion_id="WJC-FIXTURE-002-A",
    )
    monkeypatch.setattr(adapter, "_completion_record", lambda value: {})
    monkeypatch.setattr(
        adapter,
        "checkpoint_evidence",
        lambda value: {
            "provider": "website-checkpoint",
            "status": "pass",
            "revision": value.git["head"],
            "evidence_ref": value.record_paths["completion"],
        },
    )
    result = adapter.build_continue_result(
        before,
        after,
        execution_attempted=True,
    )
    assert result["status"] == "unknown"
    assert result["boundary_entered"] == "control_repair_required"
    assert result["agent_jobs_executed"] == "unknown"
    assert result["reason_code"] == "website.active_boundary_changed"


def test_activation_receipt_is_append_only_and_blocks_mismatch(
    tmp_path: Path,
) -> None:
    before = snapshot(tmp_path)
    path = adapter.write_activation_receipt(
        before,
        goal_id="CG-FIXTURE-001",
        generation=1,
        envelope_sha256="e" * 64,
    )
    receipt = adapter.read_protected_json(path)
    adapter.verify_activation_receipt(before, receipt)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600

    with pytest.raises(adapter.GoalRelayAdapterError, match="already exists"):
        adapter.write_activation_receipt(
            before,
            goal_id="CG-FIXTURE-001",
            generation=1,
            envelope_sha256="e" * 64,
        )
    changed = replace(before, fingerprint=HASH_B)
    with pytest.raises(adapter.GoalRelayAdapterError, match="differs"):
        adapter.verify_activation_receipt(changed, receipt)


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def test_fingerprint_ignores_relay_state_but_tracks_control_changes(
    tmp_path: Path,
) -> None:
    _git(tmp_path, "init", "-b", "main")
    control = tmp_path / "implementation_control/program_state.yaml"
    control.parent.mkdir(parents=True)
    control.write_text(
        'record_type: "implementation_program_state"\nstatus: "active"\n',
        encoding="utf-8",
    )
    (tmp_path / "tracked.txt").write_text("baseline\n", encoding="utf-8")
    _git(tmp_path, "add", "implementation_control/program_state.yaml", "tracked.txt")
    _git(
        tmp_path,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-m",
        "fixture",
    )
    resolver = {
        "status": "ready",
        "active_task": None,
        "current_job": None,
        "latest_handoff": None,
        "allowed_paths": {},
        "approval_gates": {},
        "boundary": {},
        "checkpoint": {},
        "required_validators": [],
        "stop_conditions": [],
        "next_recommended_action": None,
    }
    paths = {
        "program_state": "implementation_control/program_state.yaml",
        "task": None,
        "job": None,
        "handoff": None,
        "handoff_markdown": None,
        "completion": None,
    }
    initial, _, _ = adapter.compute_canonical_fingerprint(
        tmp_path,
        resolver=resolver,
        record_paths=paths,
    )
    local = tmp_path / ".local/sys4ai/continuation"
    local.mkdir(parents=True)
    (local / "goal-state.sqlite3").write_text("relay mutation\n", encoding="utf-8")
    relay_changed, _, _ = adapter.compute_canonical_fingerprint(
        tmp_path,
        resolver=resolver,
        record_paths=paths,
    )
    assert relay_changed == initial

    control.write_text(
        'record_type: "implementation_program_state"\nstatus: "blocked"\n',
        encoding="utf-8",
    )
    control_changed, _, _ = adapter.compute_canonical_fingerprint(
        tmp_path,
        resolver=resolver,
        record_paths=paths,
    )
    assert control_changed != initial


def test_active_completion_pointer_must_match_current_task_and_job(
    tmp_path: Path,
) -> None:
    control_root = tmp_path / "implementation_control"
    control_root.mkdir()
    (control_root / "program_state.yaml").write_text(
        "\n".join(
            [
                'record_type: "implementation_program_state"',
                "completion_record:",
                '  path: "old-completion.yaml"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "task.yaml").write_text(
        'record_type: "implementation_task"\ntask_id: "WI-CURRENT-001"\n',
        encoding="utf-8",
    )
    (tmp_path / "job.yaml").write_text(
        (
            'record_type: "implementation_job"\n'
            'task_id: "WI-CURRENT-001"\n'
            'job_id: "WJ-CURRENT-001-A"\n'
        ),
        encoding="utf-8",
    )
    (tmp_path / "handoff.yaml").write_text(
        'record_type: "implementation_handoff"\n',
        encoding="utf-8",
    )
    (tmp_path / "old-completion.yaml").write_text(
        (
            'record_type: "implementation_completion"\n'
            'task_id: "WI-OLD-001"\n'
            'job_id: "WJ-OLD-001-A"\n'
        ),
        encoding="utf-8",
    )
    resolver = {
        "active_task": {
            "task_id": "WI-CURRENT-001",
            "path": "task.yaml",
        },
        "current_job": {
            "job_id": "WJ-CURRENT-001-A",
            "path": "job.yaml",
        },
        "latest_handoff": {
            "yaml_path": "handoff.yaml",
            "markdown_path": "",
        },
    }
    paths = adapter.active_record_paths(tmp_path, resolver)
    assert paths["completion"] is None

    (tmp_path / "current-completion.yaml").write_text(
        (
            'record_type: "implementation_completion"\n'
            'task_id: "WI-CURRENT-001"\n'
            'job_id: "WJ-CURRENT-001-A"\n'
        ),
        encoding="utf-8",
    )
    (tmp_path / "job.yaml").write_text(
        (
            'record_type: "implementation_job"\n'
            'task_id: "WI-CURRENT-001"\n'
            'job_id: "WJ-CURRENT-001-A"\n'
            "completion_record:\n"
            '  path: "current-completion.yaml"\n'
        ),
        encoding="utf-8",
    )
    paths = adapter.active_record_paths(tmp_path, resolver)
    assert paths["completion"] == "current-completion.yaml"
