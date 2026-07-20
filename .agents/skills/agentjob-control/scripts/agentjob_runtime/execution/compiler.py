"""Compile activated AgentJob authority without performing side effects."""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.errors import RecordValidationError, SecurityError, StateConflict
from agentjob_runtime.path_security import alias_key, resolve_project_relative
from agentjob_runtime.execution.repository_topology import (
    capture_git_topology_if_present,
    classify_topology_command,
    topology_command_target,
    validate_topology_authorization,
)
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


@dataclass(frozen=True)
class CompiledPath:
    relative: str
    absolute: str
    directory_rule: bool

    def contains(self, candidate: Path) -> bool:
        target = Path(self.absolute)
        return candidate == target or self.directory_rule and target in candidate.parents


@dataclass(frozen=True)
class CompiledCommand:
    command_id: str
    argv: tuple[str, ...]
    cwd: str
    environment: Mapping[str, str]
    network: bool
    shell: bool
    timeout_seconds: int
    repository_topology_action: str | None = None
    repository_topology_authorization: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class CompiledAuthority:
    project_root: str
    task_id: str
    decision_id: str
    job_id: str
    execution_role_id: str
    role_id: str
    source_job_sha256: str
    source_role_sha256: str
    allowed_read_paths: tuple[CompiledPath, ...]
    allowed_write_paths: tuple[CompiledPath, ...]
    allowed_generated_paths: tuple[CompiledPath, ...]
    forbidden_paths: tuple[CompiledPath, ...]
    allowed_actions: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    commands: tuple[CompiledCommand, ...]
    network_access: bool
    external_effects: tuple[str, ...]
    expected_outputs: tuple[Mapping[str, Any], ...]
    required_validators: tuple[Mapping[str, Any], ...]
    contextual_validators: tuple[Mapping[str, Any], ...]
    completion_contract: Mapping[str, Any]
    checkpoint: Mapping[str, Any]
    claim_boundary: Mapping[str, Any]
    stop_conditions: tuple[str, ...]
    sandbox_hints: Mapping[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_record(record: Mapping[str, Any], schema_name: str) -> None:
    schema = Path(__file__).resolve().parents[3] / "schemas" / schema_name
    issues = validate_instance(record, schema)
    if issues:
        raise RecordValidationError(
            f"runtime authority source failed {schema_name}",
            details={"findings": format_issues(issues).splitlines()},
        )


def _compile_paths(root: Path, values: Sequence[str], label: str) -> tuple[CompiledPath, ...]:
    result: list[CompiledPath] = []
    canonical_seen: set[str] = set()
    for value in values:
        candidate, normalized = resolve_project_relative(root, value, label=f"{label} path")
        canonical = alias_key(normalized)
        if canonical in canonical_seen:
            raise SecurityError(
                f"{label} contains a portable path alias: {value}",
                details={"reason_code": "path.alias", "path": value},
            )
        canonical_seen.add(canonical)
        result.append(
            CompiledPath(
                normalized.relative,
                str(candidate),
                normalized.directory_rule,
            )
        )
    return tuple(result)


def _required_runtime_controls(job: Mapping[str, Any]) -> set[str]:
    controls = {"read_path_enforcement", "write_path_enforcement", "environment_enforcement"}
    if job["commands"]["approved"]:
        controls.add("command_enforcement")
        controls.add("repository_topology_enforcement")
    controls.add("network_control")
    if job["authority"]["external_effects"]:
        controls.add("external_effect_enforcement")
    if any(command["shell"] for command in job["commands"]["approved"]):
        controls.add("shell_execution")
    return controls


def compile_authority(
    *,
    project_root: str | Path,
    job: Mapping[str, Any],
    execution_role: Mapping[str, Any],
    activated_record_ids: set[str] | frozenset[str],
    runtime_capabilities: Mapping[str, bool],
) -> CompiledAuthority:
    """Return an immutable execution plan no broader than the activated records."""

    job = copy.deepcopy(dict(job))
    role = copy.deepcopy(dict(execution_role))
    _validate_record(job, "agent-job.schema.json")
    _validate_record(role, "execution-role.schema.json")
    if job["status"] != "active":
        raise StateConflict("only an active AgentJob can be compiled")
    if job["job_id"] not in activated_record_ids or role["execution_role_id"] not in activated_record_ids:
        raise StateConflict("job or execution role lacks activation authority")
    if role["job_id"] != job["job_id"] or role["task_id"] != job["task_id"]:
        raise StateConflict("execution role does not bind the compiled AgentJob")
    if role["role_id"] != job["role_binding"]["role_id"]:
        raise StateConflict("execution role identity differs from AgentJob role binding")
    overlay = role.get("task_overlay")
    if isinstance(overlay, Mapping) and overlay.get("expanded_permissions"):
        raise SecurityError("execution-role overlay may not expand activated AgentJob authority")
    missing = sorted(
        control
        for control in _required_runtime_controls(job)
        if runtime_capabilities.get(control) is not True
    )
    if missing:
        raise SecurityError(
            "required runtime controls are unavailable",
            details={"reason_code": "execution.required_control_unavailable", "missing_controls": missing},
        )
    root = Path(project_root).expanduser().resolve()
    if not root.is_dir():
        raise RecordValidationError(f"project root is not a directory: {root}")
    authority = job["authority"]
    allowed_actions = tuple(authority["allowed_actions"])
    forbidden_actions = tuple(authority["forbidden_actions"])
    overlap = sorted(set(allowed_actions) & set(forbidden_actions))
    if overlap:
        raise SecurityError(
            "AgentJob allows and forbids the same action",
            details={"actions": overlap},
        )
    if job["commands"]["approved"] and "run_local_commands" not in allowed_actions:
        raise SecurityError("approved commands require run_local_commands authority")
    read_paths = _compile_paths(root, authority["allowed_read_paths"], "read")
    write_paths = _compile_paths(root, authority["allowed_write_paths"], "write")
    generated_paths = _compile_paths(root, authority["allowed_generated_paths"], "generated")
    forbidden_paths = _compile_paths(root, authority["forbidden_paths"], "forbidden")
    compiled_commands: list[CompiledCommand] = []
    command_ids: set[str] = set()
    topology_extension = job.get("extensions", {}).get(
        "sys4ai.repository-topology-authorizations"
    )
    topology_data = (
        topology_extension.get("data")
        if isinstance(topology_extension, Mapping)
        else {}
    )
    topology_authorizations = (
        topology_data.get("authorizations", {})
        if isinstance(topology_data, Mapping)
        else {}
    )
    if not isinstance(topology_authorizations, Mapping):
        raise SecurityError(
            "repository topology authorizations must be keyed by command ID"
        )
    for command in job["commands"]["approved"]:
        if command["command_id"] in command_ids:
            raise SecurityError("approved command IDs must be unique")
        command_ids.add(command["command_id"])
        cwd_path, cwd_normalized = resolve_project_relative(
            root,
            command["cwd"],
            label="command cwd",
            allow_directory_rule=False,
            allow_project_root=True,
        )
        if any(contains_secret(str(item)) for item in command["argv"]) or any(
            contains_secret(str(item)) for item in command["environment"].values()
        ):
            raise SecurityError(
                "approved command embeds a detected secret",
                details={"reason_code": "execution.command_secret_detected", "command_id": command["command_id"]},
            )
        if command["network"] and not authority["network_access"]:
            raise SecurityError("command requests network outside AgentJob network authority")
        topology_action = classify_topology_command(command["argv"])
        topology_authorization = None
        if topology_action is not None:
            topology_target = topology_command_target(command["argv"])
            if topology_target is None:
                raise SecurityError(
                    "repository topology command target cannot be bound exactly",
                    details={
                        "reason_code": (
                            "execution.repository_topology_target_ambiguous"
                        ),
                        "command_id": command["command_id"],
                        "action": topology_action,
                    },
                )
            if topology_action not in allowed_actions:
                raise SecurityError(
                    "repository topology command lacks the exact protected action",
                    details={
                        "reason_code": "execution.repository_topology_not_authorized",
                        "command_id": command["command_id"],
                        "action": topology_action,
                    },
                )
            candidate = topology_authorizations.get(command["command_id"])
            if not isinstance(candidate, Mapping):
                raise SecurityError(
                    "repository topology command lacks a one-shot user authorization",
                    details={
                        "reason_code": "execution.repository_topology_authorization_missing",
                        "command_id": command["command_id"],
                        "action": topology_action,
                    },
                )
            topology_authorization = validate_topology_authorization(
                candidate,
                action=topology_action,
                command_id=command["command_id"],
                starting_revision=str(
                    (
                        capture_git_topology_if_present(root)
                        or {"revision": candidate.get("starting_revision")}
                    )["revision"]
                ),
                requested_name_or_path=topology_target,
            )
        compiled_commands.append(
            CompiledCommand(
                command["command_id"],
                tuple(command["argv"]),
                str(cwd_path),
                copy.deepcopy(command["environment"]),
                bool(command["network"]),
                bool(command["shell"]),
                int(command["timeout_seconds"]),
                topology_action,
                topology_authorization,
            )
        )
    for output in job["expected_outputs"]:
        output_path = _compile_paths(root, [output["path"]], "expected output")[0]
        if not any(
            rule.contains(Path(output_path.absolute))
            for rule in (*write_paths, *generated_paths)
        ):
            raise SecurityError(
                f"expected output is outside compiled write authority: {output['path']}"
            )
    return CompiledAuthority(
        str(root),
        str(job["task_id"]),
        str(job["decision_id"]),
        str(job["job_id"]),
        str(role["execution_role_id"]),
        str(role["role_id"]),
        content_sha256(job),
        content_sha256(role),
        read_paths,
        write_paths,
        generated_paths,
        forbidden_paths,
        allowed_actions,
        forbidden_actions,
        tuple(compiled_commands),
        bool(authority["network_access"]),
        tuple(authority["external_effects"]),
        tuple(copy.deepcopy(job["expected_outputs"])),
        tuple(copy.deepcopy(job["validators"]["required"])),
        tuple(copy.deepcopy(job["validators"]["contextual"])),
        copy.deepcopy(job["completion_contract"]),
        copy.deepcopy(job["checkpoint"]),
        copy.deepcopy(job["claim_boundary"]),
        tuple(job["stop_conditions"]),
        {
            "working_directory": str(root),
            "writable_roots": [item.absolute for item in (*write_paths, *generated_paths)],
            "network": "enabled" if authority["network_access"] else "disabled",
            "approval_mode": "deny_unlisted",
            "maximum_agentjobs": 1,
        },
    )
