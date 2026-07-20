"""Typed error hierarchy and stable exit codes."""

from __future__ import annotations

from typing import Any, Mapping


class AgentJobControlError(RuntimeError):
    code = "agentjob_control.error"
    exit_code = 1

    def __init__(self, message: str, *, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = dict(details or {})

    def as_dict(self) -> dict[str, Any]:
        return {"status": "error", "code": self.code, "message": str(self), "details": self.details}


class ConfigurationError(AgentJobControlError):
    code = "config.invalid"
    exit_code = 2


class BootstrapRequired(AgentJobControlError):
    code = "bootstrap.required"
    exit_code = 3


class RecordValidationError(AgentJobControlError):
    code = "record.invalid"
    exit_code = 4


class StateConflict(AgentJobControlError):
    code = "state.revision_conflict"
    exit_code = 5


class IntegrityError(AgentJobControlError):
    code = "integrity.failed"
    exit_code = 6


class SecurityError(AgentJobControlError):
    code = "security.blocked"
    exit_code = 7


class RecordNotFound(AgentJobControlError):
    code = "record.not_found"
    exit_code = 8


class ActiveRelayError(StateConflict):
    code = "goal.active_relay"


class GuardStop(StateConflict):
    code = "goal.guard_stop"


class MigrationError(IntegrityError):
    code = "state.migration_failed"
