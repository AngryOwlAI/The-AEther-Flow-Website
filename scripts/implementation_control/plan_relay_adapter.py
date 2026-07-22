#!/usr/bin/env python3
"""Website control boundary for the plan-native recursive relay.

This module is the only default writer path for new implementation-plan runs.
It deliberately imports no ``agentjob_runtime.goal`` module. Legacy coordinator
operations remain isolated in :mod:`plan_goal_adapter` behind explicit legacy
commands.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_SCRIPTS = Path(__file__).resolve().parents[1]
VENDOR_SCRIPTS = REPO_ROOT / ".agents" / "skills" / "agentjob-control" / "scripts"
for import_root in (PROJECT_SCRIPTS, VENDOR_SCRIPTS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from implementation_control.continue_implementation import load_yaml, resolve_continue_context  # noqa: E402
from agentjob_runtime.errors import AgentJobControlError, RecordValidationError, StateConflict  # noqa: E402
from agentjob_runtime.plan.relay import (  # noqa: E402
    PROFILE,
    TOPOLOGY,
    RelayStore,
    build_acceptance_basis,
    validate_plan,
)
from agentjob_runtime.state_utils import canonical_json_bytes, content_sha256  # noqa: E402


CONFIG_RELATIVE = Path(".agents/implementation-plan-relay/adapter-config.json")
STATE_RELATIVE = Path(".local/sys4ai/implementation-plan-relay/state.sqlite3")
PROGRAM_STATE_RELATIVE = Path("implementation_control/program_state.yaml")


class WebsiteRelayAdapterError(RuntimeError):
    def __init__(self, message: str, *, reason_code: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.reason_code = reason_code
        self.details = dict(details or {})

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "protected_stop",
            "reason_code": self.reason_code,
            "message": str(self),
            "details": copy.deepcopy(self.details),
        }


def _protected(message: str, reason_code: str, **details: Any) -> WebsiteRelayAdapterError:
    return WebsiteRelayAdapterError(message, reason_code=reason_code, details=details)


def _load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise _protected(f"{label} is missing or unsafe", "relay.config_missing", path=str(path))
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise _protected(f"{label} is invalid", "relay.config_invalid", path=str(path)) from error
    if not isinstance(value, dict):
        raise _protected(f"{label} must be a JSON object", "relay.config_invalid", path=str(path))
    return value


def _git(repo_root: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        raise _protected(
            "website Git identity is unavailable",
            "relay.repository_identity_unavailable",
            command=["git", *arguments],
            stderr=process.stderr.strip(),
        )
    return process.stdout.strip()


def repository_binding(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    root = Path(repo_root).resolve(strict=True)
    binding = {
        "root": str(root),
        "git_common_dir": _git(root, "rev-parse", "--path-format=absolute", "--git-common-dir"),
        "worktree_git_dir": _git(root, "rev-parse", "--path-format=absolute", "--git-dir"),
        "head_commit": _git(root, "rev-parse", "HEAD"),
        "branch": _git(root, "branch", "--show-current") or "detached",
        "environment_mode": "reuse_bound_checkout",
    }
    return binding


def repository_fingerprint(repo_root: Path = REPO_ROOT) -> str:
    """Hash checkout identity, not task-generated dirty content."""

    return content_sha256(repository_binding(repo_root))


def _record_path_values(value: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in {"path", "yaml_path", "markdown_path"} and isinstance(item, str):
                paths.append(item)
            else:
                paths.extend(_record_path_values(item))
    elif isinstance(value, list):
        for item in value:
            paths.extend(_record_path_values(item))
    return paths


def website_control_snapshot(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    root = Path(repo_root).resolve(strict=True)
    program_path = root / PROGRAM_STATE_RELATIVE
    if not program_path.is_file() or program_path.is_symlink():
        raise _protected("website program state is unavailable", "relay.website_control_unavailable")
    program = load_yaml(program_path)
    selected: list[dict[str, str]] = []
    for relative in sorted(set(_record_path_values(program))):
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as error:
            raise _protected("website control pointer escapes the repository", "relay.website_control_path_escape", path=relative) from error
        if candidate.is_file() and not candidate.is_symlink():
            selected.append(
                {
                    "path": relative,
                    "sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
                }
            )
    try:
        resolver, exit_code = resolve_continue_context(root)
    except Exception as error:
        resolver, exit_code = {"status": "blocked", "error": type(error).__name__}, 2
    payload = {
        "schema_version": "website.plan-relay-control-cas.v1",
        "program_state_sha256": hashlib.sha256(program_path.read_bytes()).hexdigest(),
        "selected_records": selected,
        "repository_binding": repository_binding(root),
        "resolver": resolver,
        "resolver_exit_code": exit_code,
    }
    return {
        "website_control_sha256": content_sha256(payload),
        "payload": payload,
        "resolver": resolver,
        "resolver_exit_code": exit_code,
    }


def _config(repo_root: Path) -> dict[str, Any]:
    config = _load_json(repo_root / CONFIG_RELATIVE, "recursive relay adapter config")
    if (
        config.get("relay_topology") != TOPOLOGY
        or config.get("relay_profile") != PROFILE
        or config.get("persistent_coordinator") is not False
        or config.get("generic_outer_goal") is not False
    ):
        raise _protected("recursive relay adapter selects a mixed or legacy topology", "relay.profile_refused")
    return config


def _store(repo_root: Path) -> RelayStore:
    config = _config(repo_root)
    state_path = Path(str(config.get("state_path", STATE_RELATIVE.as_posix())))
    if state_path.is_absolute() or ".." in state_path.parts:
        raise _protected("relay state path escapes the website", "relay.state_path_invalid")
    return RelayStore(repo_root / state_path)


def _authority_manifest(
    config: Mapping[str, Any], control: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "schema_version": "website.plan-relay-authority-manifest.v1",
        "canonical_execution_authority": "implementation_control",
        "adapter_config_sha256": content_sha256(config),
        "website_control_sha256": control["website_control_sha256"],
        "plan_state_authorizes_website_effects": False,
    }


def _protected_effect_grants() -> dict[str, Any]:
    return {
        "schema_version": "website.plan-relay-protected-effect-grants.v1",
        "relay_state_write_authorized": True,
        "website_content_write_authorized": False,
        "stage_commit_push_deploy_authorized": False,
        "separate_implementation_control_packet_required": True,
    }


def _require_control(repo_root: Path, expected_control_sha256: str) -> dict[str, Any]:
    snapshot = website_control_snapshot(repo_root)
    if snapshot["website_control_sha256"] != expected_control_sha256:
        raise _protected(
            "website implementation control changed before relay mutation",
            "relay.website_control_drift",
            expected=expected_control_sha256,
            actual=snapshot["website_control_sha256"],
        )
    return snapshot


def _run_identity(store: RelayStore, run_id: str) -> dict[str, str]:
    summary = store.summarize(run_id)
    return {
        "repository_fingerprint": str(summary["repository_fingerprint"]),
        "control_fingerprint": str(summary["control_fingerprint"]),
    }


def prepare_relay(
    *,
    plan: Mapping[str, Any],
    launcher_thread_id: str,
    requested_effort: str,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    root = Path(repo_root).resolve(strict=True)
    config = _config(root)
    canonical = validate_plan(plan)
    control = website_control_snapshot(root)
    binding = repository_binding(root)
    repository_identity = content_sha256(binding)
    authority = _authority_manifest(config, control)
    grants = _protected_effect_grants()
    acceptance_basis = build_acceptance_basis(
        plan=canonical,
        repository_binding=binding,
        repository_fingerprint=repository_identity,
        control_fingerprint=control["website_control_sha256"],
        launcher_thread_id=launcher_thread_id,
        requested_effort=requested_effort,
        effective_effort=requested_effort,
        authority_manifest=authority,
        protected_effect_grants=grants,
    )
    return {
        "status": "prepared",
        "plan_id": canonical["plan_id"],
        "plan_sha256": content_sha256(canonical),
        "task_count": len(canonical["tasks"]),
        "relay_profile": PROFILE,
        "relay_topology": TOPOLOGY,
        "repository_binding": binding,
        "repository_fingerprint": repository_identity,
        "website_control_sha256": control["website_control_sha256"],
        "acceptance_basis": acceptance_basis,
        "acceptance_basis_sha256": content_sha256(acceptance_basis),
        "acceptance_required_fields": [
            "accepted=true",
            "acceptance_evidence_ref",
        ],
        "persistent_coordinator": False,
        "generic_outer_goal": False,
        "mutated": False,
    }


def launch_relay(
    *,
    plan: Mapping[str, Any],
    acceptance: Mapping[str, Any],
    expected_control_sha256: str,
    launcher_thread_id: str,
    requested_effort: str = "max",
    run_id: str | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    root = Path(repo_root).resolve(strict=True)
    control = _require_control(root, expected_control_sha256)
    config = _config(root)
    binding = repository_binding(root)
    repository_identity = content_sha256(binding)
    result = _store(root).launch(
        plan=plan,
        acceptance=acceptance,
        repository_binding=binding,
        repository_fingerprint=repository_identity,
        control_fingerprint=control["website_control_sha256"],
        launcher_thread_id=launcher_thread_id,
        requested_effort=requested_effort,
        effective_effort=requested_effort,
        authority_manifest=_authority_manifest(config, control),
        protected_effect_grants=_protected_effect_grants(),
        run_id=run_id,
    )
    return {
        **result,
        "website_control": {
            "sha256": control["website_control_sha256"],
            "canonical_execution_authority": "implementation_control",
        },
        "release_effects_authorized": False,
    }


def relay_status(*, run_id: str, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    root = Path(repo_root).resolve(strict=True)
    store = _store(root)
    summary = store.summarize(run_id)
    control = website_control_snapshot(root)
    return {
        **summary,
        "website_control": {
            "current_sha256": control["website_control_sha256"],
            "activation_sha256": summary["control_fingerprint"],
            "drifted_since_activation": control["website_control_sha256"] != summary["control_fingerprint"],
            "resolver": control["resolver"],
        },
        "authority_boundary": {
            "relay": "scheduling and evidence only",
            "website_control": "task/job/path/validator and protected-effect authority",
            "terminal_state_authorizes_release": False,
        },
    }


def relay_chain_projection(
    *, run_id: str, repo_root: Path = REPO_ROOT
) -> dict[str, Any]:
    """Return the passive, redacted cross-record chain projection."""

    root = Path(repo_root).resolve(strict=True)
    return _store(root).semantic_projection(run_id)


def _mutation(
    method: str,
    *,
    run_id: str,
    expected_control_sha256: str,
    repo_root: Path = REPO_ROOT,
    **arguments: Any,
) -> dict[str, Any]:
    root = Path(repo_root).resolve(strict=True)
    _require_control(root, expected_control_sha256)
    store = _store(root)
    identity = _run_identity(store, run_id)
    operation = getattr(store, method)
    return operation(run_id, **identity, **arguments)


def record_successor(**arguments: Any) -> dict[str, Any]:
    return _mutation("record_successor", **arguments)


def prepare_dispatch(**arguments: Any) -> dict[str, Any]:
    return _mutation("begin_dispatch", **arguments)


def record_dispatch_ambiguous(**arguments: Any) -> dict[str, Any]:
    return _mutation("mark_dispatch_ambiguous", **arguments)


def claim_generation(**arguments: Any) -> dict[str, Any]:
    return _mutation("claim_generation", **arguments)


def consume_generation(**arguments: Any) -> dict[str, Any]:
    return _mutation("consume_generation", **arguments)


def record_returned(**arguments: Any) -> dict[str, Any]:
    return _mutation("record_returned", **arguments)


def record_unknown(**arguments: Any) -> dict[str, Any]:
    return _mutation("record_unknown", **arguments)


def record_protected_stop(**arguments: Any) -> dict[str, Any]:
    return _mutation("record_protected_stop", **arguments)


def finalize_receipt(**arguments: Any) -> dict[str, Any]:
    return _mutation("finalize_receipt", **arguments)


def verify_and_decide(**arguments: Any) -> dict[str, Any]:
    return _mutation("verify_and_decide", **arguments)


def reserve_successor(**arguments: Any) -> dict[str, Any]:
    return _mutation("reserve_successor", **arguments)


def finalize_relay_plan(**arguments: Any) -> dict[str, Any]:
    result = _mutation("finalize_plan", **arguments)
    result["release_effects_authorized"] = False
    return result


def reconcile_dispatch(**arguments: Any) -> dict[str, Any]:
    return _mutation("reconcile_dispatch", **arguments)


def abandon_unconsumed(**arguments: Any) -> dict[str, Any]:
    return _mutation("abandon_unconsumed", **arguments)


def reconcile_consumed(**arguments: Any) -> dict[str, Any]:
    return _mutation("reconcile_consumed", **arguments)


def cancel_relay(**arguments: Any) -> dict[str, Any]:
    result = _mutation("cancel", **arguments)
    result["release_effects_authorized"] = False
    return result
