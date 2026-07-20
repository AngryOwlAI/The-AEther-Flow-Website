"""Read-only compatibility surfaces for project-bound legacy control systems."""

from agentjob_runtime.compat.aether_adapter import AetherProjectAdapter
from agentjob_runtime.compat.aether_goal_v1 import (
    LegacyGoalReadOnlyError,
    export_legacy_goal,
    read_legacy_goal,
)

__all__ = [
    "AetherProjectAdapter",
    "LegacyGoalReadOnlyError",
    "export_legacy_goal",
    "read_legacy_goal",
]
