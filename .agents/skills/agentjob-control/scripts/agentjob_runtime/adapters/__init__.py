"""Portable provider and project adapter implementations."""

from agentjob_runtime.adapters.thread_manual import (
    ManualThreadProvider,
    adopt_manual_plan_successor,
    adopt_manual_successor,
)

__all__ = [
    "ManualThreadProvider",
    "adopt_manual_plan_successor",
    "adopt_manual_successor",
]
