#!/usr/bin/env python3
"""Read-only validation for the website implementation-plan integration."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

sys.dont_write_bytecode = True

SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from implementation_control.continue_implementation import load_yaml  # noqa: E402
from implementation_control.plan_goal_adapter import (  # noqa: E402
    ADAPTER_CONFIG_RELATIVE,
    ADAPTER_RUNTIME_RELATIVE,
    ADOPTION_RELATIVE,
    BINDING_ROOT_RELATIVE,
    BINDING_SCHEMA_RELATIVE,
    CONFORMANCE_RELATIVE,
    CONTROL_ACTIVATION_RELATIVE,
    CONTROL_ACTIVATION_SCHEMA_RELATIVE,
    EXPECTED_LOCK_SHA256,
    EXPECTED_SKILLS,
    LOCK_RELATIVE,
    MANUAL_RELATIVE,
    PLAN_SCHEMA_ROOT_RELATIVE,
    PROGRAM_STATE_RELATIVE,
    PROVENANCE_RELATIVE,
    REPO_ROOT,
    STATE_RELATIVE,
    PlanControlStore,
    WebsiteControlStore,
    WebsiteProjectAdapter,
    WebsiteRepositoryProvider,
    WebsiteThreadExecutionProfileProvider,
    canonical_json,
    content_sha256,
    load_adapter_config,
    load_json_object,
    load_plan_binding,
    resolve_effective_task_binding,
    run_conformance,
    status,
    verify_installed_bundle,
)
from agentjob_runtime.adapters.protocols import (  # noqa: E402
    ControlStore,
    ProjectAdapter,
    RepositoryProvider,
    ThreadExecutionProfileProvider,
)


SOURCE_REPOSITORY = "/Volumes/P-SSD/AngryOwl/skills-Sys4AI"
SOURCE_COMMIT = "5309fabc665b8c6665a24b9edb42b4ceda82227d"
INSTALL_RECEIPT_RELATIVE = Path(
    ".agents/skill_registry/INSTALL_RECEIPTS/"
    "bundle-implementation-plan-goal-d379c6badd2e43d39ee6a8a457b75b1d.json"
)
REGISTRY_RELATIVE = Path(".agents/skill_registry/SKILL_REGISTRY.yaml")
FRONT_DOORS = {
    "implementation-plan-goal": "user_workflow",
    "continue": "relay_callable",
    "continue-implementing-plan-task": "internal_component",
    "agentjob-control": "support_provider",
}
REQUIRED_SCHEMAS = (
    BINDING_SCHEMA_RELATIVE,
    CONTROL_ACTIVATION_SCHEMA_RELATIVE,
    Path(
        "implementation_control/schemas/"
        "codex-task-adoption-receipt-v1.schema.json"
    ),
)
PACKAGE_SCRIPTS = {
    "plan-goal": (
        "PYTHONDONTWRITEBYTECODE=1 python3 "
        "scripts/implementation_control/continue_plan_goal.py"
    ),
    "validate:plan-goal": (
        "PYTHONDONTWRITEBYTECODE=1 python3 "
        "scripts/implementation_control/validate_plan_goal.py"
    ),
    "test:plan-goal": (
        "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest "
        "-p no:cacheprovider tests/test_plan_goal_adapter.py "
        "tests/test_plan_goal_facade.py "
        "tests/test_plan_goal_installation.py "
        ".agents/skills/implementation-plan-goal/tests"
    ),
}
ACTIVE_TASK_STATUSES = {"reserved", "active"}
TERMINAL_TASK_STATUSES = {"completed", "superseded"}
PROTECTED_TASK_STATUSES = {
    "blocked",
    "replan_required",
    "human_gate_required",
    "validation_failed",
    "invocation_unknown",
    "cancelled",
}
RECEIPT_TASK_STATUSES = TERMINAL_TASK_STATUSES | PROTECTED_TASK_STATUSES
TERMINAL_PLAN_PHASES = {
    "terminal_complete",
    "terminal_blocked_no_runnable",
    "terminal_awaiting_human",
    "terminal_validation_failed",
    "terminal_capability_blocked",
    "terminal_corrupt_state",
    "terminal_cancelled",
}


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    checks: dict[str, Any] = field(default_factory=dict)

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "pass" if not self.errors else "fail",
            "errors": sorted(set(self.errors)),
            "checks": self.checks,
            "execution_performed": False,
        }


def _run(
    repo_root: Path,
    *arguments: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(arguments),
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )


def _git_paths(repo_root: Path, *arguments: str) -> set[str]:
    result = _run(repo_root, "git", *arguments)
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "Git path query failed")
    return {path for path in result.stdout.split("\0") if path}


def _path_allowed(path: str, rules: set[str]) -> bool:
    return any(
        path == rule
        or (
            rule.endswith("/**")
            and path.startswith(rule[:-3].rstrip("/") + "/")
        )
        for rule in rules
    )


def _packet_paths(entry: Mapping[str, Any]) -> set[str]:
    identifiers = entry["packet_ids"]
    task_root = (
        f"implementation_control/tasks/{identifiers['task_id']}"
    )
    return {
        f"{task_root}/00_TASK.yaml",
        f"{task_root}/jobs/{identifiers['job_id']}.yaml",
        (
            f"{task_root}/jobs/completions/"
            f"{identifiers['completion_id']}.yaml"
        ),
        f"implementation_control/handoffs/{identifiers['handoff_id']}.md",
        f"implementation_control/handoffs/{identifiers['handoff_id']}.yaml",
    }


def _selected_control_plan_id(control: Any) -> str | None:
    if control.resolver.get("status") != "ready":
        return None
    selected = control.payload.get("selected")
    if not isinstance(selected, Mapping):
        return None
    plan_ids: set[str] = set()
    for record_name, binding_name in (
        ("task", "source_context"),
        ("job", "plan_binding"),
        ("handoff", "plan_binding"),
    ):
        projection = selected.get(record_name)
        record = (
            projection.get("record")
            if isinstance(projection, Mapping)
            else None
        )
        binding = (
            record.get(binding_name)
            if isinstance(record, Mapping)
            else None
        )
        plan_id = (
            binding.get("plan_id")
            if isinstance(binding, Mapping)
            else None
        )
        if isinstance(plan_id, str) and plan_id:
            plan_ids.add(plan_id)
    return next(iter(plan_ids)) if len(plan_ids) == 1 else None


def _validate_plan_changes(
    repo_root: Path,
    report: ValidationReport,
    *,
    plan_summary: Mapping[str, Any],
    changed_paths: set[str],
    head_revision: str,
) -> set[str]:
    plan_id = str(plan_summary["plan_id"])
    controls = PlanControlStore(repo_root, read_only=True)
    store = controls.require_store()
    record = store.load_plan(plan_id)
    session = plan_summary.get("session")
    if not isinstance(session, Mapping):
        report.errors.append(f"plan adapter session is missing: {plan_id}")
        return set()
    binding_path = BINDING_ROOT_RELATIVE / f"{plan_id}.yaml"
    try:
        binding = load_plan_binding(
            record["plan"],
            binding_path,
            repo_root=repo_root,
        )
    except Exception as error:
        report.errors.append(f"plan binding is invalid: {plan_id}: {error}")
        return set()
    report.require(
        binding["manifest_sha256"]
        == session.get("binding_manifest_sha256"),
        f"plan binding differs from accepted session: {plan_id}",
    )
    plan_phase = str(record["state"].get("phase", ""))
    if plan_phase not in TERMINAL_PLAN_PHASES:
        accepted_binding = record["repository_binding"]
        report.require(
            head_revision == accepted_binding["starting_revision"],
            f"website HEAD differs from accepted plan binding: {plan_id}",
        )
        observed = WebsiteRepositoryProvider(repo_root).observe()
        report.require(
            observed.binding == accepted_binding
            and observed.topology == session.get("repository_topology"),
            f"repository binding or topology changed: {plan_id}",
        )
    intents = store.list_provider_intents(plan_id)
    unresolved_intents = [
        item["intent_id"]
        for item in intents
        if (
            item.get("status") != "returned"
            or item.get("finalized") is not True
            or item.get("recovery", {}).get("status") != "not_required"
        )
    ]
    report.require(
        not unresolved_intents,
        "unresolved provider intent remains: "
        + ", ".join(unresolved_intents),
    )

    allowed = {
        PROGRAM_STATE_RELATIVE.as_posix(),
        binding_path.as_posix(),
    }
    resolved_bindings: dict[str, Mapping[str, Any]] = {}
    replacement_authorizations = session.get(
        "replacement_binding_authorizations", {}
    )
    if not isinstance(replacement_authorizations, Mapping):
        report.errors.append(
            f"replacement binding authorizations are malformed: {plan_id}"
        )
        return allowed
    for replacement_task_id in replacement_authorizations:
        try:
            resolved = resolve_effective_task_binding(
                store=store,
                plan_record=record,
                session=session,
                base_binding=binding,
                task_id=str(replacement_task_id),
                repo_root=repo_root,
            )
        except Exception as error:
            report.errors.append(
                "replacement binding authorization is invalid: "
                f"{plan_id}:{replacement_task_id}: {error}"
            )
            continue
        resolved_bindings[str(replacement_task_id)] = resolved
        allowed.update(str(path) for path in resolved["compatibility_writes"])
    for path in changed_paths:
        if not path.endswith(".json"):
            continue
        try:
            candidate = load_json_object(
                repo_root / path,
                label="canonical plan candidate",
            )
        except Exception:
            continue
        if (
            candidate.get("plan_id") == plan_id
            and content_sha256(candidate) == record["plan_sha256"]
        ):
            allowed.add(path)

    activation = session.get("control_activation", {})
    activation_receipt = (
        activation.get("receipt", {})
        if isinstance(activation, Mapping)
        else {}
    )
    activation_task_id = activation_receipt.get("task_id")
    try:
        activation_binding = (
            resolved_bindings.get(str(activation_task_id))
            or resolve_effective_task_binding(
                store=store,
                plan_record=record,
                session=session,
                base_binding=binding,
                task_id=str(activation_task_id),
                repo_root=repo_root,
            )
        )
        activation_binding_sha256 = activation_binding[
            "binding_manifest_sha256"
        ]
    except Exception as error:
        report.errors.append(
            f"website control activation binding is invalid: {plan_id}: {error}"
        )
        activation_binding_sha256 = None
    report.require(
        activation_receipt.get("finalized") is True
        and activation_receipt.get("plan_id") == plan_id
        and activation_receipt.get("binding_manifest_sha256")
        == activation_binding_sha256,
        f"website control activation receipt is invalid: {plan_id}",
    )
    allowed.update(
        str(path)
        for path in activation_receipt.get("activated_paths", [])
    )

    receipts = {
        str(item["task_identity"]["task_id"]): item
        for item in store.list_receipts(plan_id)
    }
    active_tasks: list[Mapping[str, Any]] = []
    for lifecycle in record["state"]["tasks"]:
        task_id = str(lifecycle["task_id"])
        task_status = str(lifecycle["status"])
        if task_status not in ACTIVE_TASK_STATUSES | RECEIPT_TASK_STATUSES:
            continue
        try:
            resolved = (
                resolved_bindings.get(task_id)
                or resolve_effective_task_binding(
                    store=store,
                    plan_record=record,
                    session=session,
                    base_binding=binding,
                    task_id=task_id,
                    repo_root=repo_root,
                )
            )
        except Exception as error:
            report.errors.append(
                f"effective task binding is invalid: {plan_id}:{task_id}: {error}"
            )
            continue
        resolved_bindings[task_id] = resolved
        entry = resolved["entry"]
        allowed.update(_packet_paths(entry))
        if task_status in ACTIVE_TASK_STATUSES:
            active_tasks.append(lifecycle)
            allowed.update(str(path) for path in entry["allowed_writes"])
            continue
        receipt = receipts.get(task_id, {})
        report.require(
            receipt.get("finalized") is True
            and receipt.get("task_identity", {}).get("task_sha256")
            == lifecycle["task_sha256"]
            and receipt.get("topology_evidence", {}).get(
                "repository_binding_sha256"
            )
            == record["repository_binding_sha256"],
            f"terminal task receipt is invalid: {plan_id}:{task_id}",
        )
        allowed.update(
            str(path)
            for path in receipt.get("direct_evidence", {}).get(
                "changed_paths", []
            )
        )

    lease = record["state"].get("lease")
    control = WebsiteControlStore(repo_root).snapshot()
    if active_tasks:
        worker = session.get("worker")
        token = (
            worker.get("worker_token")
            if isinstance(worker, Mapping)
            else None
        )
        active = active_tasks[0]
        report.require(
            len(active_tasks) == 1
            and session.get("status")
            in {"worker_claimed", "invocation_consumed"}
            and isinstance(token, str)
            and isinstance(lease, Mapping)
            and lease.get("holder_kind") == "worker"
            and lease.get("task_id") == active["task_id"]
            and lease.get("generation") == active["generation"]
            and lease.get("holder_token_hash")
            == hashlib.sha256(token.encode("utf-8")).hexdigest(),
            f"active plan lease or worker evidence is invalid: {plan_id}",
        )
        entry = resolved_bindings[str(active["task_id"])]["entry"]
        identifiers = entry["packet_ids"]
        if control.resolver.get("status") == "ready":
            selected = control.payload["selected"]
            task = (selected.get("task") or {}).get("record", {})
            job = (selected.get("job") or {}).get("record", {})
            handoff = (selected.get("handoff") or {}).get("record", {})
            control_matches = (
                task.get("task_id") == identifiers["task_id"]
                and job.get("job_id") == identifiers["job_id"]
                and handoff.get("handoff_id")
                == identifiers["handoff_id"]
            )
        else:
            completion_path = next(
                path
                for path in _packet_paths(entry)
                if "/completions/" in path
            )
            try:
                completion = load_yaml(repo_root / completion_path)
            except Exception:
                completion = {}
            control_matches = (
                control.resolver.get("status") == "no_action"
                and completion.get("completion_id")
                == identifiers["completion_id"]
                and completion.get("task_id") == identifiers["task_id"]
                and completion.get("job_id") == identifiers["job_id"]
                and completion.get("status")
                in {"complete", "completed"}
            )
        report.require(
            control_matches,
            f"website control differs from active plan task: {plan_id}",
        )
    else:
        report.require(
            lease is None,
            f"orphaned plan lease remains: {plan_id}",
        )
        control_status = control.resolver.get("status")
        selected_control_plan_id = _selected_control_plan_id(control)
        report.require(
            control_status == "no_action"
            or (
                control_status == "ready"
                and selected_control_plan_id is not None
                and selected_control_plan_id != plan_id
            ),
            f"terminal plan retains executable website control: {plan_id}",
        )
    return allowed


def validate_source_and_install(
    repo_root: Path,
    report: ValidationReport,
) -> None:
    provenance_path = repo_root / PROVENANCE_RELATIVE
    try:
        provenance = load_json_object(
            provenance_path,
            label="import provenance",
        )
    except Exception as error:
        report.errors.append(f"import provenance is invalid: {error}")
        return
    report.require(
        provenance.get("source_repository") == SOURCE_REPOSITORY,
        "import provenance source repository is not exact",
    )
    report.require(
        provenance.get("source_commit") == SOURCE_COMMIT,
        "import provenance source commit is not exact",
    )
    report.require(
        provenance.get("source_access_method") == "git archive"
        and provenance.get("source_working_tree_used") is False,
        "import provenance must prove git-archive-only source access",
    )
    report.require(
        provenance.get("lock_sha256") == EXPECTED_LOCK_SHA256,
        "import provenance lock hash is not exact",
    )
    report.require(
        provenance.get("bootstrap_requested") is False
        and provenance.get("python_package_install_requested") is False,
        "import provenance must forbid bootstrap and Python installation",
    )
    report.require(
        provenance.get("plugin_distribution_enabled") is False,
        "plugin distribution must remain disabled",
    )
    try:
        installed = verify_installed_bundle(repo_root)
    except Exception as error:
        report.errors.append(f"installed bundle validation failed: {error}")
    else:
        report.checks["installed_bundle"] = installed
    receipt_path = repo_root / INSTALL_RECEIPT_RELATIVE
    try:
        receipt = load_json_object(
            receipt_path,
            label="installer receipt",
        )
    except Exception as error:
        report.errors.append(f"installer receipt is invalid: {error}")
        return
    report.require(
        receipt.get("status") == "installed"
        and receipt.get("mode") == "apply",
        "installer receipt must record one successful apply",
    )
    report.require(
        receipt.get("source_lock_sha256") == EXPECTED_LOCK_SHA256,
        "installer receipt lock hash is not exact",
    )
    report.require(
        receipt.get("bootstrap_requested") is False
        and receipt.get("python_install_requested") is False,
        "installer receipt requested bootstrap or Python installation",
    )
    report.require(
        receipt.get("recommended_plugins") == [],
        "installer receipt must declare no plugin recommendation",
    )
    actions = receipt.get("actions")
    report.require(
        isinstance(actions, list)
        and len(actions) == 4
        and {item.get("skill_id") for item in actions} == set(EXPECTED_SKILLS)
        and all(item.get("action") == "install" for item in actions),
        "installer receipt must contain exactly four install actions",
    )
    registry_path = repo_root / REGISTRY_RELATIVE
    try:
        registry = load_yaml(registry_path)
    except Exception as error:
        report.errors.append(f"installed skill registry is invalid: {error}")
        return
    registry_entries = {
        str(item.get("skill_id")): item
        for item in registry.get("skills", [])
        if isinstance(item, Mapping)
    }
    report.require(
        set(registry_entries) == set(EXPECTED_SKILLS),
        "installed skill registry must contain exactly four pinned skills",
    )
    for skill_id, (version, source_hash) in EXPECTED_SKILLS.items():
        entry = registry_entries.get(skill_id, {})
        report.require(
            entry.get("version") == version
            and entry.get("source_sha256") == source_hash,
            f"installed skill registry mismatch: {skill_id}",
        )
        report.require(
            entry.get("installation_source", {}).get(
                "distributed_via_plugin"
            )
            is None,
            f"installed skill unexpectedly uses plugin distribution: {skill_id}",
        )


def validate_adapter_contracts(
    repo_root: Path,
    report: ValidationReport,
) -> None:
    try:
        config = load_adapter_config(repo_root)
    except Exception as error:
        report.errors.append(f"adapter configuration is invalid: {error}")
        return
    report.require(
        config.get("conformance_mode") == "emulated",
        "website ControlStore conformance mode must be emulated",
    )
    report.require(
        config.get("canonical_execution_authority")
        == "implementation_control",
        "website implementation_control must remain sole authority",
    )
    report.require(
        config.get("state_path") == STATE_RELATIVE.as_posix(),
        "mutable plan state path is not exact",
    )
    report.require(
        config.get("manual_provider_root") == MANUAL_RELATIVE.as_posix(),
        "manual provider root is outside the plan local state root",
    )
    report.require(
        config.get("adapter_runtime_root")
        == ADAPTER_RUNTIME_RELATIVE.as_posix()
        and config.get("activation_receipt_root")
        == CONTROL_ACTIVATION_RELATIVE.as_posix()
        and config.get("adoption_receipt_root")
        == ADOPTION_RELATIVE.as_posix(),
        "adapter mutable roots are not exact",
    )
    report.require(
        config.get("generic_executor_enabled") is False
        and config.get("generic_control_root_enabled") is False,
        "generic .agents/control execution must be disabled",
    )
    report.require(
        config.get("providers")
        == {
            "project": "WebsiteProjectAdapter",
            "repository": "WebsiteRepositoryProvider",
            "thread": "ManualThreadProvider",
            "thread_execution_profile": (
                "WebsiteThreadExecutionProfileProvider"
            ),
            "control": "WebsiteControlStore",
            "plan_control": "PlanControlStore",
        },
        "adapter provider bindings are incomplete or ambiguous",
    )
    control_provider = WebsiteControlStore(repo_root)
    project_provider = WebsiteProjectAdapter(repo_root)
    repository_provider = WebsiteRepositoryProvider(repo_root)
    profile_provider = WebsiteThreadExecutionProfileProvider(
        thread_id="validator-thread",
        reasoning_effort="max",
        evidence_ref="validator:manual-profile-attestation",
    )
    report.require(
        isinstance(control_provider, ControlStore)
        and isinstance(project_provider, ProjectAdapter)
        and isinstance(repository_provider, RepositoryProvider)
        and isinstance(
            profile_provider,
            ThreadExecutionProfileProvider,
        ),
        "website adapters do not satisfy imported provider protocols",
    )
    report.require(
        project_provider.discover(repo_root).status == "ready",
        "website ProjectAdapter capability discovery is not ready",
    )
    try:
        conformance = run_conformance(project_provider)
    except Exception as error:
        report.errors.append(f"adapter conformance failed: {error}")
    else:
        report.require(
            conformance.status == "conformant"
            and conformance.execution_performed is False,
            "adapter conformance has blocking gaps",
        )
        report.checks["conformance"] = conformance.as_dict()
    for relative in REQUIRED_SCHEMAS:
        path = repo_root / relative
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            report.errors.append(f"interface schema is invalid: {relative}: {error}")
            continue
        report.require(
            isinstance(value, dict)
            and value.get("$schema")
            == "https://json-schema.org/draft/2020-12/schema",
            f"interface schema lacks draft identity: {relative}",
        )
    adapter_source = (
        repo_root
        / "scripts/implementation_control/plan_goal_adapter.py"
    ).read_text(encoding="utf-8")
    report.require(
        "FilesystemControlStore(" not in adapter_source
        and "run_continue(" not in adapter_source,
        "website adapter must not instantiate the generic executor",
    )
    report.require(
        "compile_plan_task_continue_invocation" in adapter_source
        and "resolve_continue_context" in adapter_source,
        "website adapter does not compile DirectorRoute into local continue",
    )


def validate_front_doors_and_package(
    repo_root: Path,
    report: ValidationReport,
) -> None:
    for skill_id, entrypoint_class in FRONT_DOORS.items():
        skill = repo_root / ".codex" / "skills" / skill_id / "SKILL.md"
        policy = (
            repo_root
            / ".codex"
            / "skills"
            / skill_id
            / "agents"
            / "openai.yaml"
        )
        report.require(skill.is_file(), f"Codex front door is missing: {skill_id}")
        report.require(
            policy.is_file(),
            f"Codex front-door policy is missing: {skill_id}",
        )
        if policy.is_file():
            report.require(
                f'entrypoint_class: "{entrypoint_class}"'
                in policy.read_text(encoding="utf-8"),
                f"Codex front-door class mismatch: {skill_id}",
            )
    index = (repo_root / ".codex/skills/README.md").read_text(
        encoding="utf-8"
    )
    notices = (
        repo_root / ".codex/skills/THIRD_PARTY_NOTICES.md"
    ).read_text(encoding="utf-8")
    for skill_id in FRONT_DOORS:
        report.require(
            f"`{skill_id}/`" in index,
            f"Codex skill index omits {skill_id}",
        )
    report.require(
        SOURCE_COMMIT in notices and EXPECTED_LOCK_SHA256 in notices,
        "third-party notices omit exact source provenance",
    )
    package_path = repo_root / "package.json"
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        report.errors.append(f"package.json is invalid: {error}")
        return
    scripts = package.get("scripts", {})
    for name, command in PACKAGE_SCRIPTS.items():
        report.require(
            scripts.get(name) == command,
            f"package script {name} is not exact",
        )
    validate = str(scripts.get("validate", ""))
    for step in (
        "npm run validate:implementation-control",
        "npm run validate:plan-goal",
        "npm run test:plan-goal",
        "npm run build",
    ):
        report.require(step in validate, f"npm run validate omits {step}")
    if all(step in validate for step in ("npm run validate:plan-goal", "npm run test:plan-goal", "npm run build")):
        report.require(
            validate.index("npm run validate:plan-goal")
            < validate.index("npm run test:plan-goal")
            < validate.index("npm run build"),
            "plan validation and tests must run before build",
        )
    ignore = (repo_root / ".gitignore").read_text(encoding="utf-8")
    report.require(
        ".local/sys4ai/" in ignore,
        "mutable plan runtime root is not ignored",
    )


def validate_repository_boundary(
    repo_root: Path,
    report: ValidationReport,
    *,
    allow_active_packet: bool,
) -> None:
    head = _run(repo_root, "git", "rev-parse", "HEAD")
    report.require(head.returncode == 0, "website HEAD cannot be resolved")
    head_revision = head.stdout.strip()
    tracked = _run(repo_root, "git", "ls-files", "-z")
    tracked_paths = tracked.stdout.split("\0") if tracked.returncode == 0 else []
    forbidden_tracked = [
        path
        for path in tracked_paths
        if (
            path.startswith(".local/sys4ai/")
            or path.startswith(".agents/control/")
            or "/__pycache__/" in path
            or path.endswith((".pyc", ".pyo"))
            or "/.pytest_cache/" in path
        )
    ]
    report.require(
        not forbidden_tracked,
        "forbidden mutable, cache, or parallel-control paths are tracked: "
        + ", ".join(forbidden_tracked),
    )
    report.require(
        not (repo_root / ".agents/control").exists(),
        "parallel .agents/control authority tree exists",
    )
    program = load_yaml(repo_root / "implementation_control/program_state.yaml")
    state_result = status(repo_root=repo_root)
    plans = state_result["plan_control"]["plans"]
    try:
        changed_paths = _git_paths(
            repo_root,
            "diff",
            "--name-only",
            "--no-renames",
            "-z",
            head_revision,
            "--",
        ) | _git_paths(
            repo_root,
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
        )
        staged_paths = _git_paths(
            repo_root,
            "diff",
            "--cached",
            "--name-only",
            "-z",
            "--",
        )
    except ValueError as error:
        report.errors.append(str(error))
        changed_paths = set()
        staged_paths = set()
    report.require(
        not staged_paths,
        "staged repository effects are not authorized: "
        + ", ".join(sorted(staged_paths)),
    )
    allowed_paths: set[str] = set()
    for plan in plans:
        allowed_paths.update(
            _validate_plan_changes(
                repo_root,
                report,
                plan_summary=plan,
                changed_paths=changed_paths,
                head_revision=head_revision,
            )
        )
    unexpected_paths = sorted(
        path
        for path in changed_paths
        if not _path_allowed(path, allowed_paths)
    )
    report.require(
        not unexpected_paths,
        "repository drift is outside accepted plan control: "
        + ", ".join(unexpected_paths),
    )
    if not plans:
        report.require(
            program.get("status") == "inactive"
            and program.get("current_job") in ({}, None),
            "inactive repository retains executable website control",
        )
    report.checks["final_state"] = {
        "program_status": program.get("status"),
        "current_job": program.get("current_job"),
        "live_plan_count": len(plans),
        "accepted_changed_paths": sorted(changed_paths),
        "allow_active_packet": allow_active_packet,
        "status_effects": state_result["effects"],
    }


def run_validation(
    repo_root: Path = REPO_ROOT,
    *,
    allow_active_packet: bool = False,
) -> ValidationReport:
    report = ValidationReport()
    validate_source_and_install(repo_root, report)
    validate_adapter_contracts(repo_root, report)
    validate_front_doors_and_package(repo_root, report)
    validate_repository_boundary(
        repo_root,
        report,
        allow_active_packet=allow_active_packet,
    )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument(
        "--allow-active-packet",
        action="store_true",
        help="Development-only structural check before control closeout.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    root = Path(arguments.repo_root).expanduser().resolve(strict=True)
    result = run_validation(
        root,
        allow_active_packet=arguments.allow_active_packet,
    ).as_dict()
    sys.stdout.write(canonical_json(result))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
