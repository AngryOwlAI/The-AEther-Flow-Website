"""Capability discovery with fail-closed bootstrap reporting."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from agentjob_runtime import (
    CAPABILITY_AGENTJOB_CONTROL,
    CAPABILITY_CONTINUATION_ENVELOPE,
    CAPABILITY_CONTROL_RECORDS,
    CAPABILITY_GOAL_RELAY_STATE,
    CAPABILITY_GOAL_RELAY_STATE_READER_V1,
)


@dataclass(frozen=True)
class Capability:
    capability_id: str
    provider: str
    version: str
    required: bool
    available: bool
    reason_code: str | None = None


@dataclass(frozen=True)
class CapabilityReport:
    status: str
    capabilities: tuple[Capability, ...]
    execution_performed: bool = False

    @property
    def missing_capabilities(self) -> tuple[str, ...]:
        return tuple(
            item.capability_id for item in self.capabilities if item.required and not item.available
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "missing_capabilities": list(self.missing_capabilities),
            "execution_performed": self.execution_performed,
            "capabilities": [asdict(item) for item in self.capabilities],
        }


BUILTIN_PROVIDERS = {
    "control": {"filesystem": "1.0.0"},
    "repository": {"git": "1.0.0", "filesystem_only": "1.0.0", "test_fake": "1.0.0"},
    "state": {"sqlite": "2.0.0", "file_journal": "2.0.0"},
    "checkpoint": {
        "none": "1.0.0",
        "git_status": "1.0.0",
        "git_commit": "1.0.0",
        "project_command": "1.0.0",
        "external_system": "1.0.0",
    },
    "thread": {"manual-handoff": "1.0.0", "manual_handoff": "1.0.0", "test-fake": "1.0.0"},
}


def _major(version: str) -> str:
    return version.split(".", 1)[0]


def discover_capabilities(
    config: Mapping[str, Any],
    *,
    provider_versions: Mapping[str, str] | None = None,
) -> CapabilityReport:
    overrides = dict(provider_versions or {})
    requested = [
        (CAPABILITY_AGENTJOB_CONTROL, "agentjob-control", "1.0.0", True, True, None),
        (CAPABILITY_CONTROL_RECORDS, str(config["control"]["adapter"]), "1.0.0", True, None, "control"),
        (CAPABILITY_GOAL_RELAY_STATE, str(config["goal_relay"]["state_backend"]), "2.0.0", True, None, "state"),
        (
            CAPABILITY_GOAL_RELAY_STATE_READER_V1,
            str(config["goal_relay"]["state_backend"]),
            "1.0.0",
            False,
            True,
            None,
        ),
        (CAPABILITY_CONTINUATION_ENVELOPE, str(config["goal_relay"]["thread_provider"]), "1.0.0", False, None, "thread"),
        ("sys4ai.repository-provider.v1", str(config["repository"]["provider"]), "1.0.0", True, None, "repository"),
        ("sys4ai.checkpoint-provider.v1", str(config["checkpoint"]["provider"]), "1.0.0", True, None, "checkpoint"),
    ]
    results: list[Capability] = []
    for capability_id, provider, expected, required, fixed_available, group in requested:
        if fixed_available is not None:
            results.append(Capability(capability_id, provider, expected, required, fixed_available))
            continue
        version = overrides.get(f"{group}:{provider}") or BUILTIN_PROVIDERS.get(str(group), {}).get(provider)
        if version is None:
            results.append(
                Capability(capability_id, provider, expected, required, False, "capability.provider_unavailable")
            )
        elif _major(version) != _major(expected):
            results.append(
                Capability(capability_id, provider, version, required, False, "capability.unsupported_version")
            )
        else:
            results.append(Capability(capability_id, provider, version, required, True))
    status = "ready" if all(not item.required or item.available for item in results) else "bootstrap_required"
    return CapabilityReport(status, tuple(results))


def bootstrap_required_report() -> dict[str, Any]:
    return {
        "status": "bootstrap_required",
        "missing_capabilities": [CAPABILITY_AGENTJOB_CONTROL],
        "execution_performed": False,
        "recommended_action": {
            "command": "python <AGENTJOB_CONTROL_PATH>/scripts/agentjobctl.py init --project-root <PROJECT_ROOT>"
        },
    }
