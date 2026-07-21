from __future__ import annotations

import copy
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from scripts.implementation_control import plan_goal_adapter as adapter_module
from scripts.implementation_control.continue_implementation import load_yaml
from scripts.implementation_control.plan_goal_adapter import (
    ADAPTER_CONFIG_RELATIVE,
    ADOPTION_SCHEMA_RELATIVE,
    BINDING_SCHEMA_RELATIVE,
    CONTROL_ACTIVATION_SCHEMA_RELATIVE,
    EXPECTED_LOCK_SHA256,
    LOCK_RELATIVE,
    PLAN_SCHEMA_ROOT_RELATIVE,
    PlanControlStore,
    RepositoryEvidence,
    WebsiteControlStore,
    WebsiteProjectAdapter,
    WebsitePlanAdapterError,
    WebsiteRepositoryProvider,
    WebsiteThreadExecutionProfileProvider,
    activate_plan,
    adopt_worker,
    compile_binding_director_route,
    content_sha256,
    load_plan_binding,
    prepare_plan,
    recover,
    render_yaml,
    resolve_effective_task_binding,
    reserve_next,
    validate_binding_manifest,
    worker_consume,
    worker_fail,
    worker_finalize,
    worker_prepare,
    worker_unknown,
)
from agentjob_runtime.adapters.protocols import (
    ControlStore,
    ProjectAdapter,
    RepositoryProvider,
    ThreadExecutionProfileProvider,
)
from scripts.implementation_control.validate_plan_goal import (
    ValidationReport,
    validate_repository_boundary,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = "2026-07-20T06:00:00Z"
GATES = (
    "public_claim_changes",
    "source_refresh_uncertainty",
    "broad_navigation_or_route_retirement",
    "shared_visual_systems",
    "public_downloadable_assets",
    "public_manifest_authority_records",
    "git_push",
    "cloudflare_deployment",
    "upstream_source_project_writes",
)


@dataclass(frozen=True)
class ProjectFixture:
    root: Path
    plan_path: Path
    binding_path: Path
    plan: dict[str, Any]
    binding: dict[str, Any]


def _run(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        list(arguments),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def make_project(tmp_path: Path, *, task_count: int = 2) -> ProjectFixture:
    root = tmp_path / "website"
    root.mkdir()
    shutil.copytree(
        REPO_ROOT / ".agents" / "skills",
        root / ".agents" / "skills",
    )
    for relative in (
        LOCK_RELATIVE,
        ADAPTER_CONFIG_RELATIVE,
        BINDING_SCHEMA_RELATIVE,
        CONTROL_ACTIVATION_SCHEMA_RELATIVE,
        ADOPTION_SCHEMA_RELATIVE,
    ):
        _copy_file(REPO_ROOT / relative, root / relative)
    program = {
        "schema_version": "0.1",
        "record_type": "implementation_program_state",
        "repository": "The-AEther-Flow-Website",
        "updated_utc": FIXED_TIME,
        "status": "inactive",
        "mode": "website_local_implementation_control",
        "authority_order": ["AGENTS.md"],
        "repository_boundary": {
            "website_repository": ".",
            "upstream_source_repository": (
                "/Volumes/P-SSD/AngryOwl/The-AEther-Flow"
            ),
            "upstream_write_status": "forbidden",
            "deployment_status": "not_authorized",
        },
        "active_task": {},
        "current_job": {},
        "latest_handoff": {},
        "required_validators": [],
        "next_recommended_action": {
            "task_packet": "none",
            "summary": "No active implementation packet.",
            "do_not_skip": "Open authority before execution.",
        },
    }
    program_path = root / "implementation_control/program_state.yaml"
    program_path.parent.mkdir(parents=True, exist_ok=True)
    program_path.write_bytes(render_yaml(program))
    (root / "package.json").write_text(
        json.dumps(
            {
                "name": "test-website",
                "private": True,
                "scripts": {"validate": "true"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / ".gitignore").write_text(
        ".local/sys4ai/\n", encoding="utf-8"
    )
    _run(root, "git", "init", "-b", "main")
    _run(root, "git", "config", "user.email", "tests@example.invalid")
    _run(root, "git", "config", "user.name", "Plan Adapter Tests")
    _run(root, "git", "add", ".")
    _run(root, "git", "commit", "-m", "fixture baseline")
    repository = WebsiteRepositoryProvider(root).observe()
    task_ids = [f"TASK-{index:03d}" for index in range(1, task_count + 1)]
    tasks = []
    for index, task_id in enumerate(task_ids, start=1):
        tasks.append(
            {
                "task_id": task_id,
                "task_sha256": str(index) * 64,
                "phase_id": "PHASE-01",
                "title": f"Task {index}",
                "objective": f"Implement bounded task {index}.",
                "depends_on": [] if index == 1 else [task_ids[index - 2]],
                "acceptance_criteria": [
                    f"Task {index} has direct completion evidence."
                ],
                "validation_refs": [f"evidence/task-{index}.txt"],
                "execution_budget": {
                    "one_task_per_discussion": True,
                    "max_continue_invocations": 1,
                    "max_agentjobs": 1,
                    "same_task_successors": 0,
                },
                "extensions": {},
            }
        )
    plan = {
        "schema_version": "sys4ai.implementation-plan.v2",
        "plan_id": "PLAN-WEBSITE-TEST-001",
        "title": "Website adapter test plan",
        "objective": "Execute the accepted website adapter test plan.",
        "acceptance": {
            "status": "accepted",
            "authority_ref": "test:accepted-plan",
            "accepted_at": FIXED_TIME,
            "policy_version": "TEST-POLICY-1",
        },
        "repository_binding": copy.deepcopy(dict(repository.binding)),
        "serial_execution": True,
        "required_scope": {
            "phase_ids": ["PHASE-01"],
            "task_ids": task_ids,
            "excluded_phase_ids": [],
            "excluded_task_ids": [],
        },
        "phases": [
            {
                "phase_id": "PHASE-01",
                "title": "Execute bounded tasks",
                "depends_on": [],
                "task_ids": task_ids,
                "acceptance_criteria": [
                    "Every required task has direct evidence."
                ],
                "extensions": {},
            }
        ],
        "tasks": tasks,
        "extensions": {},
    }
    task_bindings: dict[str, Any] = {}
    for index, task in enumerate(tasks, start=1):
        entry = {
            "task_id": task["task_id"],
            "task_sha256": task["task_sha256"],
            "packet_ids": {
                "task_id": f"WI-20990101-{index:03d}",
                "job_id": f"WJ-20990101-{index:03d}-A",
                "handoff_id": f"WH-20990101-{index:03d}",
                "completion_id": f"WJC-20990101-{index:03d}-A",
            },
            "objective": task["objective"],
            "acceptance_criteria": task["acceptance_criteria"],
            "validators": [
                {
                    "id": f"validator-task-{index}",
                    "command": task["validation_refs"][0],
                    "required": True,
                }
            ],
            "allowed_reads": ["package.json", "implementation_control/**"],
            "allowed_writes": [f"artifacts/task-{index}.txt"],
            "approval_gates": [
                {
                    "id": gate,
                    "status": (
                        "blocked"
                        if gate == "upstream_source_project_writes"
                        else "not_required"
                    ),
                    "reason": f"{gate} is outside this test packet.",
                }
                for gate in GATES
            ],
            "stop_conditions": [
                "Task identity, binding, topology, or control hash differs."
            ],
            "checkpoint_rights": {
                "stage": False,
                "commit": False,
                "branch": False,
                "worktree": False,
                "push": False,
                "deploy": False,
            },
            "execution_role": {
                "role_id": "website-plan-task-engineer",
                "role_version": "1.0.0",
                "responsibilities": [
                    "Execute only the mapped website packet."
                ],
                "may_not": ["Expand authority or select a successor."],
            },
            "authority_sha256": "",
        }
        entry["authority_sha256"] = content_sha256(
            {
                key: value
                for key, value in entry.items()
                if key != "authority_sha256"
            }
        )
        task_bindings[task["task_id"]] = entry
    binding = {
        "schema_version": "website.plan-binding.v1",
        "record_type": "implementation_plan_binding",
        "status": "non_executable",
        "plan_id": plan["plan_id"],
        "plan_sha256": content_sha256(plan),
        "binding_revision": 1,
        "tasks": task_bindings,
        "manifest_sha256": "",
    }
    binding["manifest_sha256"] = content_sha256(
        {
            key: value
            for key, value in binding.items()
            if key != "manifest_sha256"
        }
    )
    plan_path = root / "plans/accepted-plan.json"
    binding_path = (
        root
        / "implementation_control"
        / "plan_bindings"
        / f"{plan['plan_id']}.yaml"
    )
    plan_path.parent.mkdir(parents=True)
    binding_path.parent.mkdir(parents=True)
    plan_path.write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    binding_path.write_bytes(render_yaml(binding))
    assert EXPECTED_LOCK_SHA256 == hashlib_sha256(root / LOCK_RELATIVE)
    return ProjectFixture(root, plan_path, binding_path, plan, binding)


def hashlib_sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_fixture(fixture: ProjectFixture):
    return prepare_plan(
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        goal_text=None,
        reasoning_effort="max",
        current_thread_id="coordinator-thread-001",
        current_profile_evidence_ref="host:coordinator-thread-001:max",
        repo_root=fixture.root,
    )


def activate_fixture(fixture: ProjectFixture):
    prepared = prepare_fixture(fixture)
    result = activate_plan(
        prepared=prepared,
        acceptance_basis_sha256=prepared.acceptance_basis_sha256,
        acceptance_message="I accept the exact goal and reasoning effort.",
        acceptance_evidence_ref="conversation:test-acceptance",
        expected_plan_revision=0,
        expected_control_sha256=prepared.control.control_sha256,
        timestamp=FIXED_TIME,
    )
    return prepared, result


def write_completion(
    fixture: ProjectFixture,
    *,
    plan_task_id: str,
) -> None:
    entry = fixture.binding["tasks"][plan_task_id]
    ids = entry["packet_ids"]
    artifact = fixture.root / entry["allowed_writes"][0]
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("bounded result\n", encoding="utf-8")
    completion = {
        "schema_version": "0.1",
        "record_type": "implementation_completion",
        "completion_id": ids["completion_id"],
        "task_id": ids["task_id"],
        "job_id": ids["job_id"],
        "status": "completed",
        "completed_utc": "2026-07-20T06:05:00Z",
        "summary": "The mapped task is complete.",
        "changed_files": entry["allowed_writes"],
        "requirements_satisfied": entry["acceptance_criteria"],
        "validator_results": [
            {
                "id": validator["id"],
                "command": validator["command"],
                "status": "passed",
                "evidence": entry["allowed_writes"][0],
            }
            for validator in entry["validators"]
        ],
    }
    path = (
        fixture.root
        / "implementation_control"
        / "tasks"
        / ids["task_id"]
        / "jobs"
        / "completions"
        / f"{ids['completion_id']}.yaml"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(render_yaml(completion))
    task_path = (
        fixture.root
        / "implementation_control"
        / "tasks"
        / ids["task_id"]
        / "00_TASK.yaml"
    )
    job_path = (
        fixture.root
        / "implementation_control"
        / "tasks"
        / ids["task_id"]
        / "jobs"
        / f"{ids['job_id']}.yaml"
    )
    handoff_path = (
        fixture.root
        / "implementation_control"
        / "handoffs"
        / f"{ids['handoff_id']}.yaml"
    )
    for record_path in (task_path, job_path, handoff_path):
        record = load_yaml(record_path)
        record["status"] = "completed"
        record["updated_utc"] = "2026-07-20T06:05:00Z"
        record_path.write_bytes(render_yaml(record))
    program_path = fixture.root / "implementation_control/program_state.yaml"
    program = load_yaml(program_path)
    program["status"] = "inactive"
    program["updated_utc"] = "2026-07-20T06:05:00Z"
    program["active_task"]["status"] = "completed"
    program["current_job"] = {}
    program["latest_handoff"]["status"] = "completed"
    program["required_validators"] = []
    program["next_recommended_action"] = {
        "task_packet": "none",
        "summary": "The mapped website packet is complete.",
        "do_not_skip": "Only the coordinator may reserve a successor.",
    }
    program_path.write_bytes(render_yaml(program))


def test_complete_binding_and_authority_hashes_are_required(tmp_path: Path):
    fixture = make_project(tmp_path)
    loaded = load_plan_binding(
        fixture.plan,
        fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
    )
    assert set(loaded["tasks"]) == {"TASK-001", "TASK-002"}

    incomplete = copy.deepcopy(fixture.binding)
    incomplete["tasks"].pop("TASK-002")
    incomplete["manifest_sha256"] = content_sha256(
        {
            key: value
            for key, value in incomplete.items()
            if key != "manifest_sha256"
        }
    )
    with pytest.raises(
        WebsitePlanAdapterError, match="map every canonical task"
    ):
        validate_binding_manifest(
            fixture.plan,
            incomplete,
            schema_path=fixture.root / BINDING_SCHEMA_RELATIVE,
        )

    stale = copy.deepcopy(fixture.binding)
    stale["tasks"]["TASK-001"]["allowed_writes"].append("outside.txt")
    stale["manifest_sha256"] = content_sha256(
        {
            key: value
            for key, value in stale.items()
            if key != "manifest_sha256"
        }
    )
    with pytest.raises(
        WebsitePlanAdapterError, match="authority hash"
    ):
        validate_binding_manifest(
            fixture.plan,
            stale,
            schema_path=fixture.root / BINDING_SCHEMA_RELATIVE,
        )


def test_explicit_replacement_binding_hydrates_execution_without_changing_base(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    task = {
        "task_id": "TASK-REPLACEMENT-002",
        "task_sha256": "",
        "phase_id": "PHASE-01",
        "title": "Execute coupled replacement",
        "objective": "Execute one explicitly authorized replacement task.",
        "depends_on": ["TASK-001"],
        "acceptance_criteria": [
            "The replacement has direct completion evidence."
        ],
        "validation_refs": ["evidence/replacement.txt"],
        "execution_budget": {
            "one_task_per_discussion": True,
            "max_continue_invocations": 1,
            "max_agentjobs": 1,
            "same_task_successors": 0,
        },
        "extensions": {},
    }
    task["task_sha256"] = content_sha256(
        {
            key: value
            for key, value in task.items()
            if key != "task_sha256"
        }
    )
    entry = copy.deepcopy(fixture.binding["tasks"]["TASK-001"])
    entry.update(
        {
            "task_id": task["task_id"],
            "task_sha256": task["task_sha256"],
            "packet_ids": {
                "task_id": "WI-20990101-002",
                "job_id": "WJ-20990101-002-A",
                "handoff_id": "WH-20990101-002",
                "completion_id": "WJC-20990101-002-A",
            },
            "objective": task["objective"],
            "acceptance_criteria": task["acceptance_criteria"],
            "validators": [
                {
                    "id": "validator-replacement",
                    "command": task["validation_refs"][0],
                    "required": True,
                }
            ],
            "allowed_writes": ["artifacts/replacement.txt"],
        }
    )
    entry["authority_sha256"] = content_sha256(
        {
            key: value
            for key, value in entry.items()
            if key != "authority_sha256"
        }
    )
    supersession = {
        "supersession_id": "PTS-TEST-001",
        "replacement_tasks": [
            {
                "task_id": task["task_id"],
                "task_sha256": task["task_sha256"],
            }
        ],
    }
    supplement = {
        "schema_version": "website.plan-task-replacement-binding.v1",
        "record_type": "implementation_plan_task_replacement_binding",
        "status": "non_executable",
        "plan_id": fixture.plan["plan_id"],
        "plan_sha256": content_sha256(fixture.plan),
        "base_binding_manifest_sha256": fixture.binding[
            "manifest_sha256"
        ],
        "supersession_id": supersession["supersession_id"],
        "supersession_sha256": content_sha256(supersession),
        "plan_revision": 9,
        "task": entry,
        "hash_basis": "canonical_json_without_binding_content_sha256",
        "binding_content_sha256": "",
    }
    supplement["binding_content_sha256"] = content_sha256(
        {
            key: value
            for key, value in supplement.items()
            if key != "binding_content_sha256"
        }
    )
    session = {
        "replacement_binding_authorizations": {
            task["task_id"]: {
                "status": "approved",
                "approved_at": FIXED_TIME,
                "approval_ref": "conversation:replacement-approval",
                "authorized_plan_revision": 9,
                "authorized_website_control_sha256": "a" * 64,
                "task_authority_sha256": entry["authority_sha256"],
                "replacement_binding_content_sha256": supplement[
                    "binding_content_sha256"
                ],
                "compatibility_writes": [
                    "scripts/implementation_control/plan_goal_adapter.py"
                ],
                "external_effects_authorized": False,
                "replacement_binding": supplement,
                "task_definition": task,
            }
        }
    }

    class ReplacementStore:
        def load_task_definition(self, plan_id: str, task_id: str):
            assert plan_id == fixture.plan["plan_id"]
            assert task_id == task["task_id"]
            return {
                "task_id": task_id,
                "task_sha256": task["task_sha256"],
                "phase_id": task["phase_id"],
                "origin_kind": "replacement",
                "depends_on": task["depends_on"],
                "task_json": {
                    "task_id": task_id,
                    "task_sha256": task["task_sha256"],
                    "depends_on": task["depends_on"],
                    "one_task_per_discussion": True,
                    "max_continue_invocations": 1,
                    "max_agentjobs": 1,
                },
            }

        def list_supersessions(self, plan_id: str):
            assert plan_id == fixture.plan["plan_id"]
            return [supersession]

    plan_record = {
        "plan_id": fixture.plan["plan_id"],
        "plan_sha256": content_sha256(fixture.plan),
        "effective_plan_sha256": content_sha256(fixture.plan),
        "state": {"revision": 9},
    }
    resolved = resolve_effective_task_binding(
        store=ReplacementStore(),  # type: ignore[arg-type]
        plan_record=plan_record,
        session=session,
        base_binding=fixture.binding,
        task_id=task["task_id"],
        repo_root=fixture.root,
    )
    assert resolved["replacement"] is True
    assert resolved["task_definition"] == task
    assert resolved["entry"] == entry
    assert fixture.binding["tasks"] == {"TASK-001": fixture.binding["tasks"]["TASK-001"]}

    stale = copy.deepcopy(session)
    stale["replacement_binding_authorizations"][task["task_id"]][
        "replacement_binding"
    ]["task"]["allowed_writes"].append("outside.txt")
    with pytest.raises(
        WebsitePlanAdapterError, match="accepted bytes"
    ):
        resolve_effective_task_binding(
            store=ReplacementStore(),  # type: ignore[arg-type]
            plan_record=plan_record,
            session=stale,
            base_binding=fixture.binding,
            task_id=task["task_id"],
            repo_root=fixture.root,
        )


def test_control_cas_materializes_exactly_one_binding_projection(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    store = WebsiteControlStore(fixture.root)
    before = store.snapshot()
    staged = store.stage_packet(
        {
            "plan": fixture.plan,
            "binding": fixture.binding["tasks"]["TASK-001"],
            "binding_manifest_sha256": fixture.binding[
                "manifest_sha256"
            ],
            "timestamp": FIXED_TIME,
        }
    )
    activated = store.activate_packet(staged, before.control_sha256)
    assert activated["status"] == "activated"
    assert (
        store.resolve_current()["current_job"]["job_id"]
        == fixture.binding["tasks"]["TASK-001"]["packet_ids"]["job_id"]
    )
    assert not (fixture.root / ".agents/control").exists()
    with pytest.raises(
        WebsitePlanAdapterError, match="compare-and-swap"
    ):
        store.activate_packet(staged, before.control_sha256)


def test_yaml_renderer_round_trips_colon_in_list_scalar(tmp_path: Path):
    path = tmp_path / "record.yaml"
    value = {
        "requirements": [
            "npm run validate:provenance passes without exemptions."
        ]
    }
    payload = render_yaml(value)
    assert b"validate\\u003aprovenance" in payload
    path.write_bytes(payload)
    assert load_yaml(path) == value


def test_control_activation_rolls_back_unparseable_packet(tmp_path: Path):
    fixture = make_project(tmp_path, task_count=1)
    store = WebsiteControlStore(fixture.root)
    before = store.snapshot()
    staged = store.stage_packet(
        {
            "plan": fixture.plan,
            "binding": fixture.binding["tasks"]["TASK-001"],
            "binding_manifest_sha256": fixture.binding[
                "manifest_sha256"
            ],
            "timestamp": FIXED_TIME,
        }
    )
    task_path = (
        "implementation_control/tasks/"
        f"{fixture.binding['tasks']['TASK-001']['packet_ids']['task_id']}"
        "/00_TASK.yaml"
    )
    malformed = copy.deepcopy(staged)
    malformed["records"][task_path] = (
        b'schema_version: "0.1"\nrequirements:\n  - "bad: scalar"\n'
    )
    with pytest.raises(ValueError, match="unsupported key"):
        store.activate_packet(malformed, before.control_sha256)
    assert store.snapshot().control_sha256 == before.control_sha256
    assert not (fixture.root / task_path).exists()


def test_acceptance_changes_when_topology_changes(tmp_path: Path):
    fixture = make_project(tmp_path, task_count=1)
    first = prepare_fixture(fixture)
    _run(fixture.root, "git", "branch", "unexpected-local-branch")
    second = prepare_fixture(fixture)
    assert (
        first.repository.topology_sha256
        != second.repository.topology_sha256
    )
    assert (
        first.acceptance_basis_sha256
        != second.acceptance_basis_sha256
    )


def test_director_route_uses_binding_authority_not_plan_prose(tmp_path: Path):
    fixture = make_project(tmp_path, task_count=1)
    task = fixture.plan["tasks"][0]
    route = compile_binding_director_route(
        task, fixture.binding["tasks"][task["task_id"]]
    )
    assert route.job_spec["authority"]["allowed_write_paths"] == [
        "artifacts/task-1.txt"
    ]
    assert not (
        set(route.job_spec["authority"]["allowed_actions"])
        & {"repository-branch-create", "repository-worktree-create"}
    )


def test_director_route_uses_receipt_output_for_zero_write_task(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    task = fixture.plan["tasks"][0]
    entry = copy.deepcopy(fixture.binding["tasks"][task["task_id"]])
    entry["allowed_writes"] = []
    route = compile_binding_director_route(task, entry)
    completion_path = (
        "implementation_control/tasks/"
        f"{entry['packet_ids']['task_id']}/jobs/completions/"
        f"{entry['packet_ids']['completion_id']}.yaml"
    )
    assert route.job_spec["authority"]["allowed_write_paths"] == []
    assert route.job_spec["authority"]["allowed_generated_paths"] == [
        completion_path
    ]
    assert route.job_spec["expected_outputs"] == [
        {"path": completion_path, "kind": "receipt"}
    ]
    assert route.job_spec["policy_refs"] == [
        ".agents/implementation-plan-goal/adapter-config.json"
    ]


def test_required_imported_provider_protocols_are_bound(tmp_path: Path):
    fixture = make_project(tmp_path, task_count=1)
    assert isinstance(WebsiteControlStore(fixture.root), ControlStore)
    assert isinstance(WebsiteProjectAdapter(fixture.root), ProjectAdapter)
    assert isinstance(
        WebsiteRepositoryProvider(fixture.root),
        RepositoryProvider,
    )
    assert isinstance(
        WebsiteThreadExecutionProfileProvider(
            thread_id="coordinator-thread-001",
            reasoning_effort="max",
            evidence_ref="host:coordinator-thread-001:max",
        ),
        ThreadExecutionProfileProvider,
    )


def test_full_relay_adopts_before_prompt_consumes_once_and_is_coordinator_only(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=2)
    _, activation = activate_fixture(fixture)
    assert activation["plan_revision"] == 3
    assert (
        activation["task_create_request"]["token_bound_prompt_released"]
        is False
    )
    assert activation["agentjobs"] == 0

    adopted = adopt_worker(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=3,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        creation_status="returned",
        codex_task_id="worker-thread-001",
        effective_reasoning_effort="max",
        profile_evidence_ref="host:worker-thread-001:max",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:01:00Z",
    )
    assert adopted["plan_revision"] == 4
    assert adopted["token_bound_prompt_released"] is True
    assert "handoff_token" in adopted["worker_prompt"]

    claim = worker_prepare(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=4,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-001",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:02:00Z",
    )
    assert claim["plan_revision"] == 5
    consumed = worker_consume(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=5,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-001",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:03:00Z",
    )
    assert consumed["plan_revision"] == 6
    assert consumed["continue_invocations"] == 1
    with pytest.raises(WebsitePlanAdapterError):
        worker_consume(
            plan_id=fixture.plan["plan_id"],
            expected_plan_revision=6,
            expected_control_sha256=activation[
                "website_control_sha256"
            ],
            current_thread_id="worker-thread-001",
            plan_path=fixture.plan_path.relative_to(fixture.root),
            binding_path=fixture.binding_path.relative_to(fixture.root),
            repo_root=fixture.root,
        )

    write_completion(fixture, plan_task_id="TASK-001")
    completed_control_sha256 = WebsiteControlStore(
        fixture.root
    ).snapshot().control_sha256
    finalized = worker_finalize(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=6,
        expected_control_sha256=completed_control_sha256,
        current_thread_id="worker-thread-001",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:05:00Z",
    )
    assert finalized["schema_version"] == "sys4ai.plan-task-receipt.v2"
    assert finalized["plan_phase"] == "continuation_required"
    assert finalized["agentjobs"] == 1
    assert PlanControlStore(fixture.root).require_store().list_receipts(
        fixture.plan["plan_id"]
    )[0]["finalized"] is True
    boundary_report = ValidationReport()
    validate_repository_boundary(
        fixture.root,
        boundary_report,
        allow_active_packet=False,
    )
    assert boundary_report.errors == []

    with pytest.raises(
        WebsitePlanAdapterError, match="accepted coordinator"
    ):
        reserve_next(
            plan_id=fixture.plan["plan_id"],
            expected_plan_revision=finalized["plan_revision"],
            expected_control_sha256=completed_control_sha256,
            coordinator_thread_id="worker-thread-001",
            plan_path=fixture.plan_path.relative_to(fixture.root),
            binding_path=fixture.binding_path.relative_to(fixture.root),
            repo_root=fixture.root,
        )
    successor = reserve_next(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=finalized["plan_revision"],
        expected_control_sha256=completed_control_sha256,
        coordinator_thread_id="coordinator-thread-001",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:06:00Z",
    )
    assert successor["task_create_request"]["task_id"] == "TASK-002"
    assert successor["agentjobs"] == 0


def test_ambiguous_creation_is_not_retried_and_recovery_adopts_original(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    _, activation = activate_fixture(fixture)
    with pytest.raises(
        WebsitePlanAdapterError, match="not retried"
    ):
        adopt_worker(
            plan_id=fixture.plan["plan_id"],
            expected_plan_revision=3,
            expected_control_sha256=activation[
                "website_control_sha256"
            ],
            creation_status="ambiguous",
            codex_task_id=None,
            effective_reasoning_effort=None,
            profile_evidence_ref=None,
            repo_root=fixture.root,
        )
    recovery = recover(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=3,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        coordinator_thread_id="coordinator-thread-001",
        repo_root=fixture.root,
    )
    assert recovery["retry_task_creation"] is False
    assert recovery["adopt_original_task"] is True
    store = PlanControlStore(fixture.root).require_store()
    assert len(store.list_provider_intents(fixture.plan["plan_id"])) == 1


def test_reserve_next_is_read_only_no_action_after_final_task(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    _, activation = activate_fixture(fixture)
    adopted = adopt_worker(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=activation["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        creation_status="returned",
        codex_task_id="worker-thread-final",
        effective_reasoning_effort="max",
        profile_evidence_ref="host:worker-thread-final:max",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:01:00Z",
    )
    claim = worker_prepare(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=adopted["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-final",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:02:00Z",
    )
    consumed = worker_consume(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=claim["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-final",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:03:00Z",
    )
    write_completion(fixture, plan_task_id="TASK-001")
    completed_control_sha256 = WebsiteControlStore(
        fixture.root
    ).snapshot().control_sha256
    finalized = worker_finalize(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=consumed["plan_revision"],
        expected_control_sha256=completed_control_sha256,
        current_thread_id="worker-thread-final",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:05:00Z",
    )
    result = reserve_next(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=finalized["plan_revision"],
        expected_control_sha256=completed_control_sha256,
        coordinator_thread_id="coordinator-thread-001",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:06:00Z",
    )
    assert result["status"] == "no_action"
    assert result["reason_code"] == "plan.completion_candidate"
    assert result["plan_revision"] == finalized["plan_revision"]
    assert result["execution_performed"] is False


def test_partial_successor_activation_enters_recovery_without_duplication(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    fixture = make_project(tmp_path, task_count=2)
    _, activation = activate_fixture(fixture)
    adopted = adopt_worker(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=activation["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        creation_status="returned",
        codex_task_id="worker-thread-partial",
        effective_reasoning_effort="max",
        profile_evidence_ref="host:worker-thread-partial:max",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:01:00Z",
    )
    claim = worker_prepare(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=adopted["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-partial",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:02:00Z",
    )
    consumed = worker_consume(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=claim["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-partial",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:03:00Z",
    )
    write_completion(fixture, plan_task_id="TASK-001")
    completed_control_sha256 = WebsiteControlStore(
        fixture.root
    ).snapshot().control_sha256
    finalized = worker_finalize(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=consumed["plan_revision"],
        expected_control_sha256=completed_control_sha256,
        current_thread_id="worker-thread-partial",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:05:00Z",
    )

    def fail_activation(**_: Any) -> dict[str, Any]:
        raise OSError("injected website activation failure")

    monkeypatch.setattr(
        adapter_module,
        "_activate_reserved_packet",
        fail_activation,
    )
    with pytest.raises(OSError, match="injected website activation"):
        reserve_next(
            plan_id=fixture.plan["plan_id"],
            expected_plan_revision=finalized["plan_revision"],
            expected_control_sha256=completed_control_sha256,
            coordinator_thread_id="coordinator-thread-001",
            plan_path=fixture.plan_path.relative_to(fixture.root),
            binding_path=fixture.binding_path.relative_to(fixture.root),
            repo_root=fixture.root,
            timestamp="2026-07-20T06:06:00Z",
        )

    store = PlanControlStore(fixture.root).require_store()
    partial = store.load_plan(fixture.plan["plan_id"])
    assert partial["state"]["active_task_id"] == "TASK-002"
    assert partial["state"]["current_generation"] == 2
    assert len(store.list_provider_intents(fixture.plan["plan_id"])) == 1
    recovery = recover(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=partial["state"]["revision"],
        expected_control_sha256=completed_control_sha256,
        coordinator_thread_id="coordinator-thread-001",
        repo_root=fixture.root,
    )
    assert recovery["status"] == "recovery_required"
    assert recovery["reserved_task_id"] == "TASK-002"
    assert recovery["website_packet_activated"] is False
    assert recovery["retry_task_reservation"] is False
    assert recovery["duplicate_state_created"] is False


def test_unknown_consumed_result_is_quarantined_without_retry(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    _, activation = activate_fixture(fixture)
    adopt_worker(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=3,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        creation_status="returned",
        codex_task_id="worker-thread-unknown",
        effective_reasoning_effort="max",
        profile_evidence_ref="host:worker-thread-unknown:max",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:01:00Z",
    )
    worker_prepare(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=4,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-unknown",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:02:00Z",
    )
    consumed = worker_consume(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=5,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-unknown",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:03:00Z",
    )
    unknown = worker_unknown(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=consumed["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-unknown",
        reason_code="plan_worker.continue_outcome_unknown",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:04:00Z",
    )
    assert unknown["status"] == "invocation_unknown"
    assert unknown["retry_authorized"] is False
    assert unknown["recovery_required"] is True


def test_known_validator_failure_finalizes_without_retry_or_quarantine(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    _, activation = activate_fixture(fixture)
    adopt_worker(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=3,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        creation_status="returned",
        codex_task_id="worker-thread-failed",
        effective_reasoning_effort="max",
        profile_evidence_ref="host:worker-thread-failed:max",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:01:00Z",
    )
    worker_prepare(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=4,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-failed",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:02:00Z",
    )
    consumed = worker_consume(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=5,
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-failed",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        repo_root=fixture.root,
        timestamp="2026-07-20T06:03:00Z",
    )
    failed = worker_fail(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=consumed["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-failed",
        plan_path=fixture.plan_path.relative_to(fixture.root),
        binding_path=fixture.binding_path.relative_to(fixture.root),
        validator_results={"validator-task-1": "fail"},
        failure_summary="The required validator returned a known failure.",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:04:00Z",
    )
    assert failed["status"] == "task_finalized"
    assert failed["disposition"] == "validation_failed"
    assert failed["plan_phase"] == "terminal_validation_failed"
    assert WebsiteControlStore(fixture.root).snapshot().resolver[
        "status"
    ] == "no_action"
    receipt = PlanControlStore(fixture.root).require_store().list_receipts(
        fixture.plan["plan_id"]
    )[0]
    assert receipt["disposition"] == "validation_failed"
    assert receipt["execution"]["continue_invocations"] == 1
    assert receipt["execution"]["agentjobs"] == 1
    assert receipt["recovery"]["status"] == "not_required"


def test_repository_validation_uses_active_plan_binding_and_rejects_drift(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    _, activation = activate_fixture(fixture)
    adopted = adopt_worker(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=activation["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        creation_status="returned",
        codex_task_id="worker-thread-boundary",
        effective_reasoning_effort="max",
        profile_evidence_ref="host:worker-thread-boundary:max",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:01:00Z",
    )
    worker_prepare(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=adopted["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-boundary",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:02:00Z",
    )
    allowed = fixture.root / "artifacts/task-1.txt"
    allowed.parent.mkdir(parents=True)
    allowed.write_text("bound change\n", encoding="utf-8")

    report = ValidationReport()
    validate_repository_boundary(
        fixture.root,
        report,
        allow_active_packet=False,
    )
    assert report.errors == []
    _run(fixture.root, "git", "add", "artifacts/task-1.txt")
    staged_report = ValidationReport()
    validate_repository_boundary(
        fixture.root,
        staged_report,
        allow_active_packet=False,
    )
    assert any(
        "staged repository effects" in error
        for error in staged_report.errors
    )
    _run(fixture.root, "git", "reset", "--", "artifacts/task-1.txt")

    unrelated = fixture.root / "src/unrelated.ts"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("export const drift = true;\n", encoding="utf-8")
    drift_report = ValidationReport()
    validate_repository_boundary(
        fixture.root,
        drift_report,
        allow_active_packet=False,
    )
    assert any(
        "src/unrelated.ts" in error for error in drift_report.errors
    )
    unrelated.unlink()
    package = fixture.root / "package.json"
    package.write_text(
        package.read_text(encoding="utf-8") + "\n",
        encoding="utf-8",
    )
    tracked_drift_report = ValidationReport()
    validate_repository_boundary(
        fixture.root,
        tracked_drift_report,
        allow_active_packet=False,
    )
    assert any(
        "package.json" in error
        for error in tracked_drift_report.errors
    )


def test_repository_validation_rejects_open_intent_and_topology_change(
    tmp_path: Path,
):
    fixture = make_project(tmp_path, task_count=1)
    _, activation = activate_fixture(fixture)
    open_report = ValidationReport()
    validate_repository_boundary(
        fixture.root,
        open_report,
        allow_active_packet=True,
    )
    assert any(
        "unresolved provider intent" in error
        for error in open_report.errors
    )

    adopted = adopt_worker(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=activation["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        creation_status="returned",
        codex_task_id="worker-thread-topology",
        effective_reasoning_effort="max",
        profile_evidence_ref="host:worker-thread-topology:max",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:01:00Z",
    )
    worker_prepare(
        plan_id=fixture.plan["plan_id"],
        expected_plan_revision=adopted["plan_revision"],
        expected_control_sha256=activation[
            "website_control_sha256"
        ],
        current_thread_id="worker-thread-topology",
        repo_root=fixture.root,
        timestamp="2026-07-20T06:02:00Z",
    )
    _run(fixture.root, "git", "branch", "unauthorized-topology")
    topology_report = ValidationReport()
    validate_repository_boundary(
        fixture.root,
        topology_report,
        allow_active_packet=False,
    )
    assert any(
        "topology changed" in error
        for error in topology_report.errors
    )
