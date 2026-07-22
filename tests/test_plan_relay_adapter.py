from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from implementation_control.plan_relay_adapter import (
    RecordValidationError,
    WebsiteRelayAdapterError,
    claim_generation,
    consume_generation,
    finalize_receipt,
    finalize_relay_plan,
    launch_relay,
    prepare_dispatch,
    prepare_relay,
    record_protected_stop,
    record_returned,
    record_successor,
    relay_chain_projection,
    relay_status,
    verify_and_decide,
    website_control_snapshot,
)


CONFIG = {
    "schema_version": "website.implementation-plan-relay-adapter.v1",
    "relay_profile": "recursive_chain_v1",
    "relay_topology": "recursive_chain_v1",
    "state_path": ".local/sys4ai/implementation-plan-relay/state.sqlite3",
    "persistent_coordinator": False,
    "generic_outer_goal": False,
}


def _run(root: Path, *command: str) -> str:
    process = subprocess.run(command, cwd=root, check=True, capture_output=True, text=True)
    return process.stdout.strip()


@pytest.fixture()
def relay_project(tmp_path: Path) -> Path:
    (tmp_path / ".agents/implementation-plan-relay").mkdir(parents=True)
    (tmp_path / ".agents/implementation-plan-relay/adapter-config.json").write_text(
        json.dumps(CONFIG, indent=2) + "\n", encoding="utf-8"
    )
    (tmp_path / "implementation_control").mkdir()
    (tmp_path / "implementation_control/program_state.yaml").write_text(
        "schema_version: 0.1\nstatus: initialized\nactive_task: null\ncurrent_job: null\nlatest_handoff: null\n",
        encoding="utf-8",
    )
    _run(tmp_path, "git", "init")
    _run(tmp_path, "git", "config", "user.email", "relay@example.invalid")
    _run(tmp_path, "git", "config", "user.name", "Relay Test")
    _run(tmp_path, "git", "add", ".")
    _run(tmp_path, "git", "commit", "-m", "fixture")
    return tmp_path


def _plan() -> dict:
    return {"plan_id": "P-ONE", "tasks": [{"task_id": "A", "depends_on": []}]}


def _prepare(root: Path) -> dict:
    return prepare_relay(
        plan=_plan(),
        launcher_thread_id="launcher",
        requested_effort="max",
        repo_root=root,
    )


def _acceptance(prepared: dict, evidence: str = "test:combined-acceptance") -> dict:
    return {
        **prepared["acceptance_basis"],
        "accepted": True,
        "acceptance_evidence_ref": evidence,
    }


def test_recursive_launch_creates_no_outer_goal_and_reports_control_boundary(relay_project: Path) -> None:
    prepared = _prepare(relay_project)
    launched = launch_relay(
        plan=_plan(),
        acceptance=_acceptance(prepared),
        expected_control_sha256=prepared["website_control_sha256"],
        launcher_thread_id="launcher",
        run_id="RUN-ONE",
        repo_root=relay_project,
    )
    assert launched["maximum_agentjobs"] == 0
    assert launched["release_effects_authorized"] is False
    state = relay_project / ".local/sys4ai/implementation-plan-relay/state.sqlite3"
    assert state.is_file()
    assert not (relay_project / ".local/sys4ai/implementation-plan-goal/state.sqlite3").exists()
    summary = relay_status(run_id="RUN-ONE", repo_root=relay_project)
    assert summary["relay_topology"] == "recursive_chain_v1"
    assert summary["authority_boundary"]["terminal_state_authorizes_release"] is False


def test_stale_recursive_acceptance_fails_before_state_initialization(
    relay_project: Path,
) -> None:
    prepared = _prepare(relay_project)
    stale = _acceptance(prepared, "test:stale-acceptance")
    stale["launcher_thread_id"] = "another-thread"
    with pytest.raises(RecordValidationError) as error:
        launch_relay(
            plan=_plan(),
            acceptance=stale,
            expected_control_sha256=prepared["website_control_sha256"],
            launcher_thread_id="launcher",
            run_id="RUN-STALE",
            repo_root=relay_project,
        )
    assert error.value.details["reason_code"] == "relay.acceptance_stale"
    assert not (
        relay_project / ".local/sys4ai/implementation-plan-relay/state.sqlite3"
    ).exists()


def test_every_recursive_mutation_rejects_website_control_drift(relay_project: Path) -> None:
    prepared = _prepare(relay_project)
    launched = launch_relay(
        plan=_plan(), acceptance=_acceptance(prepared),
        expected_control_sha256=prepared["website_control_sha256"],
        launcher_thread_id="launcher", run_id="RUN-ONE", repo_root=relay_project,
    )
    (relay_project / "implementation_control/program_state.yaml").write_text(
        "schema_version: 0.1\nstatus: changed\nactive_task: null\ncurrent_job: null\nlatest_handoff: null\n",
        encoding="utf-8",
    )
    with pytest.raises(WebsiteRelayAdapterError, match="changed") as error:
        prepare_dispatch(
            run_id="RUN-ONE", generation=1, expected_revision=1,
            expected_control_sha256=prepared["website_control_sha256"],
            owner_token=launched["handoff_token"], current_thread_id="launcher",
            repo_root=relay_project,
        )
    assert error.value.reason_code == "relay.website_control_drift"


def test_one_task_wrapper_finalizes_and_never_grants_release(relay_project: Path) -> None:
    prepared = _prepare(relay_project)
    control = prepared["website_control_sha256"]
    launched = launch_relay(
        plan=_plan(), acceptance=_acceptance(prepared), expected_control_sha256=control,
        launcher_thread_id="launcher", run_id="RUN-ONE", repo_root=relay_project,
    )
    token = launched["handoff_token"]
    started = prepare_dispatch(
        run_id="RUN-ONE", generation=1, expected_revision=1,
        expected_control_sha256=control, owner_token=token,
        current_thread_id="launcher", repo_root=relay_project,
    )
    recorded = record_successor(
        run_id="RUN-ONE", generation=1, expected_revision=started["revision"],
        expected_control_sha256=control, owner_token=token,
        current_thread_id="launcher", child_thread_id="worker-A",
        provider_response={"thread_id": "worker-A", "manual": True},
        effective_effort="max", repo_root=relay_project,
    )
    token = recorded["handoff_token"]
    claimed = claim_generation(
        run_id="RUN-ONE", generation=1, expected_revision=recorded["revision"],
        expected_control_sha256=control, current_thread_id="worker-A",
        handoff_token=token, effective_effort="max", repo_root=relay_project,
    )
    consumed = consume_generation(
        run_id="RUN-ONE", generation=1, expected_revision=claimed["revision"],
        expected_control_sha256=control, current_thread_id="worker-A",
        handoff_token=token, repo_root=relay_project,
    )
    returned = record_returned(
        run_id="RUN-ONE", generation=1, expected_revision=consumed["revision"],
        expected_control_sha256=control, current_thread_id="worker-A",
        handoff_token=token, result={"direct": True}, repo_root=relay_project,
    )
    receipt = finalize_receipt(
        run_id="RUN-ONE", generation=1, expected_revision=returned["revision"],
        expected_control_sha256=control, current_thread_id="worker-A",
        handoff_token=token, disposition="completed", evidence={"validator": "pass"},
        repo_root=relay_project,
    )
    decision = verify_and_decide(
        run_id="RUN-ONE", generation=1, expected_revision=receipt["revision"],
        expected_control_sha256=control, current_thread_id="worker-A",
        handoff_token=token, repo_root=relay_project,
    )
    finalized = finalize_relay_plan(
        run_id="RUN-ONE", expected_revision=receipt["revision"],
        expected_control_sha256=control, current_thread_id="worker-A",
        handoff_token=token, report=decision["completion_report"], repo_root=relay_project,
    )
    assert finalized["status"] == "plan_complete"
    assert finalized["release_effects_authorized"] is False
    assert relay_status(run_id="RUN-ONE", repo_root=relay_project)["lease"]["released"] is True


def test_mixed_or_legacy_default_profile_fails_closed(relay_project: Path) -> None:
    config = dict(CONFIG)
    config["relay_topology"] = "coordinator_v2_legacy"
    (relay_project / ".agents/implementation-plan-relay/adapter-config.json").write_text(
        json.dumps(config), encoding="utf-8"
    )
    with pytest.raises(WebsiteRelayAdapterError) as error:
        _prepare(relay_project)
    assert error.value.reason_code == "relay.profile_refused"


def test_status_is_passive(relay_project: Path) -> None:
    prepared = _prepare(relay_project)
    launch_relay(
        plan=_plan(), acceptance=_acceptance(prepared),
        expected_control_sha256=prepared["website_control_sha256"],
        launcher_thread_id="launcher", run_id="RUN-ONE", repo_root=relay_project,
    )
    before = relay_status(run_id="RUN-ONE", repo_root=relay_project)["revision"]
    for _ in range(3):
        relay_status(run_id="RUN-ONE", repo_root=relay_project)
    after = relay_status(run_id="RUN-ONE", repo_root=relay_project)["revision"]
    assert before == after


def test_protected_stop_is_pre_call_and_chain_projection_is_redacted(
    relay_project: Path,
) -> None:
    prepared = _prepare(relay_project)
    launched = launch_relay(
        plan=_plan(),
        acceptance=_acceptance(prepared),
        expected_control_sha256=prepared["website_control_sha256"],
        launcher_thread_id="launcher",
        run_id="RUN-ONE",
        repo_root=relay_project,
    )
    stopped = record_protected_stop(
        run_id="RUN-ONE",
        generation=1,
        expected_revision=1,
        expected_control_sha256=prepared["website_control_sha256"],
        current_thread_id="launcher",
        handoff_token=launched["handoff_token"],
        disposition="capability_blocked",
        reason_code="provider.capability_missing",
        evidence={"missing": ["create_thread"]},
        repo_root=relay_project,
    )
    assert stopped["status"] == "capability_blocked"
    assert stopped["child_created"] is False
    projection = relay_chain_projection(
        run_id="RUN-ONE", repo_root=relay_project
    )
    assert projection["schema_version"] == "sys4ai.plan-relay-chain.v1"
    assert projection["generations"][0]["invocation_count"] == 0
    assert '"handoff_token":' not in json.dumps(projection)
