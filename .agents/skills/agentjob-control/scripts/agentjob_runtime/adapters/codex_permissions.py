"""Compile AgentJob authority into Codex runtime controls as defense in depth."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.errors import BootstrapRequired
from agentjob_runtime.execution.compiler import CompiledAuthority


ACTION_TO_TOOL = {
    "read_files": "filesystem.read",
    "edit_files": "filesystem.write",
    "run_local_commands": "terminal.command",
}


@dataclass(frozen=True)
class CodexRuntimeCapabilities:
    surface: str
    working_directory: bool
    writable_roots: bool
    network_control: bool
    approval_policy: bool
    tool_allowlist: bool
    required_skill_mentions: bool
    command_budget: bool
    fine_grained_path_exclusions: bool
    available_tools: tuple[str, ...] = (
        "filesystem.read",
        "filesystem.write",
        "terminal.command",
    )

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CodexPermissionPlan:
    status: str
    surface: str
    working_directory: str
    writable_roots: tuple[str, ...]
    network: str
    approval_policy: str
    allowed_tools: tuple[str, ...]
    required_skills: tuple[str, ...]
    maximum_agentjobs: int
    maximum_commands: int
    unsupported_restrictions: tuple[str, ...]
    requires_local_executor: bool
    post_execution_path_validation_required: bool = True
    execution_performed: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _nested_forbidden_paths(authority: CompiledAuthority) -> tuple[str, ...]:
    result: list[str] = []
    for forbidden in authority.forbidden_paths:
        target = Path(forbidden.absolute)
        if any(rule.contains(target) for rule in (*authority.allowed_write_paths, *authority.allowed_generated_paths)):
            result.append(forbidden.relative)
    return tuple(sorted(result))


def compile_codex_permissions(
    authority: CompiledAuthority,
    *,
    capabilities: CodexRuntimeCapabilities,
    required_skills: Sequence[str] = (),
    mandatory_runtime_restrictions: Sequence[str] = (),
) -> CodexPermissionPlan:
    """Return an equal-or-stricter mapping or block on mandatory gaps."""

    unsupported: list[str] = []
    mandatory = {
        "working_directory",
        "writable_roots",
        "network_control",
        "approval_policy",
        "tool_allowlist",
        *mandatory_runtime_restrictions,
    }
    if required_skills:
        mandatory.add("required_skill_mentions")
    capability_values = {
        "working_directory": capabilities.working_directory,
        "writable_roots": capabilities.writable_roots,
        "network_control": capabilities.network_control,
        "approval_policy": capabilities.approval_policy,
        "tool_allowlist": capabilities.tool_allowlist,
        "required_skill_mentions": capabilities.required_skill_mentions,
        "command_budget": capabilities.command_budget,
        "fine_grained_path_exclusions": capabilities.fine_grained_path_exclusions,
    }
    for restriction, available in capability_values.items():
        if not available:
            unsupported.append(restriction)
    nested_forbidden = _nested_forbidden_paths(authority)
    if nested_forbidden and not capabilities.fine_grained_path_exclusions:
        unsupported.append("fine_grained_path_exclusions")
    allowed_tools = tuple(
        sorted(
            ACTION_TO_TOOL[action]
            for action in authority.allowed_actions
            if action in ACTION_TO_TOOL
        )
    )
    missing_tools = sorted(set(allowed_tools) - set(capabilities.available_tools))
    if missing_tools:
        unsupported.append("required_tools_available")
        mandatory.add("required_tools_available")
    unsupported = sorted(set(unsupported))
    blocking = sorted(set(unsupported) & mandatory)
    if blocking:
        raise BootstrapRequired(
            "Codex runtime cannot enforce mandatory AgentJob restrictions",
            details={
                "reason_code": "codex_permissions.mandatory_restriction_unsupported",
                "surface": capabilities.surface,
                "unsupported_restrictions": blocking,
                "missing_tools": missing_tools,
                "nested_forbidden_paths": list(nested_forbidden),
            },
        )
    writable_roots = tuple(
        item.absolute
        for item in (*authority.allowed_write_paths, *authority.allowed_generated_paths)
    )
    project = Path(authority.project_root)
    for value in writable_roots:
        Path(value).relative_to(project)
    return CodexPermissionPlan(
        "ready" if not unsupported else "ready_with_local_enforcement",
        capabilities.surface,
        authority.project_root,
        writable_roots,
        "enabled" if authority.network_access else "disabled",
        "deny_unlisted",
        allowed_tools,
        tuple(required_skills),
        1,
        len(authority.commands),
        tuple(unsupported),
        bool(unsupported),
    )
