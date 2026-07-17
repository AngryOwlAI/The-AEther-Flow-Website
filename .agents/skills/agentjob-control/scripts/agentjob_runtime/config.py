"""Strict target-project configuration loading and path resolution."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableMapping

from agentjob_runtime.capabilities import CapabilityReport, discover_capabilities
from agentjob_runtime.errors import BootstrapRequired, ConfigurationError, SecurityError
from agentjob_runtime.path_security import resolve_project_relative
from agentjob_runtime.records.canonical import load_structured
from agentjob_runtime.validation.schema import format_issues, validate_instance


ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
FORBIDDEN_STATE_ROOTS = ("skills", ".agents/skills", ".codex/skills", "plugins")


@dataclass(frozen=True)
class LoadedConfig:
    project_root: Path
    config_path: Path
    data: Mapping[str, Any]
    control_root: Path
    local_state_root: Path
    capabilities: CapabilityReport


def _walk_strings(value: Any, prefix: str = ""):
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else key
            yield from _walk_strings(item, path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_strings(item, f"{prefix}[{index}]")
    elif isinstance(value, str):
        yield prefix, value


def _get_mutable_path(data: MutableMapping[str, Any], dotted: str) -> tuple[MutableMapping[str, Any], str]:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", dotted):
        raise ConfigurationError(f"invalid environment-substitution field: {dotted}")
    parts = dotted.split(".")
    parent: MutableMapping[str, Any] = data
    for part in parts[:-1]:
        value = parent.get(part)
        if not isinstance(value, MutableMapping):
            raise ConfigurationError(f"environment-substitution field does not exist: {dotted}")
        parent = value
    return parent, parts[-1]


def _substitute_environment(
    data: MutableMapping[str, Any], environment: Mapping[str, str]
) -> None:
    allowed = set(data.get("security", {}).get("allow_environment_fields", []))
    for field, value in list(_walk_strings(data)):
        if ENV_PATTERN.search(value) and field not in allowed:
            raise ConfigurationError(
                f"environment substitution is not allowed in {field}",
                details={"reason_code": "config.environment_field_denied"},
            )
    for field in allowed:
        parent, key = _get_mutable_path(data, field)
        value = parent.get(key)
        if not isinstance(value, str):
            raise ConfigurationError(f"environment-substitution field is not a string: {field}")

        def replacement(match: re.Match[str]) -> str:
            name = match.group(1)
            if name not in environment:
                raise ConfigurationError(
                    f"required environment value is missing: {name}",
                    details={"reason_code": "config.environment_value_missing"},
                )
            return environment[name]

        parent[key] = ENV_PATTERN.sub(replacement, value)


def resolve_project_path(
    project_root: Path, value: str, *, purpose: str, reject_install_roots: bool = False
) -> Path:
    resolved, normalized = resolve_project_relative(
        project_root,
        value,
        label=purpose,
        allow_directory_rule=False,
    )
    relative = Path(*normalized.base_relative.split("/"))
    if reject_install_roots:
        normalized = relative.as_posix()
        if any(normalized == root or normalized.startswith(f"{root}/") for root in FORBIDDEN_STATE_ROOTS):
            raise SecurityError(
                f"{purpose} cannot be stored under an installed package: {value}",
                details={"reason_code": "path.mutable_state_in_install"},
            )
    return resolved


def load_config(
    project_root: str | Path,
    *,
    config_path: str | Path | None = None,
    environment: Mapping[str, str] | None = None,
    schema_path: str | Path | None = None,
    provider_versions: Mapping[str, str] | None = None,
) -> LoadedConfig:
    if project_root is None or not str(project_root).strip():
        raise ConfigurationError("an explicit project root is required")
    root = Path(project_root).expanduser().resolve()
    if not root.is_dir():
        raise ConfigurationError(f"project root is not a directory: {root}")
    path = Path(config_path) if config_path is not None else root / ".agents/control/config.yaml"
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise SecurityError("configuration path must remain within the project root") from error
    if not path.is_file():
        raise BootstrapRequired(
            f"control configuration is missing: {path}",
            details={"missing_capabilities": ["sys4ai.agentjob-control.v1"], "execution_performed": False},
        )
    loaded = load_structured(path)
    if not isinstance(loaded, dict):
        raise ConfigurationError("control configuration must be a mapping")
    data: MutableMapping[str, Any] = loaded
    _substitute_environment(data, environment or os.environ)
    if schema_path is None:
        schema_path = Path(__file__).resolve().parents[2] / "schemas" / "control-config.schema.json"
    issues = validate_instance(data, schema_path)
    if issues:
        raise ConfigurationError(
            "control configuration failed schema validation",
            details={"reason_code": "config.schema_invalid", "findings": format_issues(issues).splitlines()},
        )
    control_root = resolve_project_path(root, data["control"]["root"], purpose="control root")
    local_root = resolve_project_path(
        root,
        data["goal_relay"]["local_root"],
        purpose="local state root",
        reject_install_roots=True,
    )
    capabilities = discover_capabilities(data, provider_versions=provider_versions)
    return LoadedConfig(root, path, data, control_root, local_root, capabilities)
