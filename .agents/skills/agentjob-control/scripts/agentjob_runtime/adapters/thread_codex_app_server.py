"""Codex App Server ThreadProvider over a configured documented transport."""

from __future__ import annotations

import hashlib
import re
from typing import Any, Mapping, Protocol

from agentjob_runtime.errors import RecordValidationError
from agentjob_runtime.goal.launcher import ThreadCreateResult
from agentjob_runtime.records.canonical import content_sha256


SECRET_KEY = re.compile(r"(?:secret|token|password|private.?key|credential|authorization)", re.I)
SECRET_VALUE = re.compile(r"(?:sk-[A-Za-z0-9_-]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")


class AppServerTransport(Protocol):
    def request(
        self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: int
    ) -> Mapping[str, Any]: ...


def _redact(value: Any, *, key: str = "") -> Any:
    if SECRET_KEY.search(key):
        return "<redacted>"
    if isinstance(value, Mapping):
        return {str(item): _redact(data, key=str(item)) for item, data in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, str) and SECRET_VALUE.search(value):
        return "<redacted>"
    return value


class CodexAppServerThreadProvider:
    provider_id = "codex-app-server"

    def __init__(
        self,
        transport: AppServerTransport,
        *,
        strategy: str = "fresh_summary",
        timeout_seconds: int = 30,
    ) -> None:
        if strategy not in {"fresh_summary", "fork_history"}:
            raise RecordValidationError(f"unsupported App Server thread strategy: {strategy}")
        self.transport = transport
        self.strategy = strategy
        self.timeout_seconds = timeout_seconds
        self._capabilities: dict[str, Any] | None = None

    def capabilities(self) -> Mapping[str, Any]:
        if self._capabilities is None:
            try:
                raw = self.transport.request(
                    "capabilities", {}, timeout_seconds=self.timeout_seconds
                )
                operations = tuple(str(item) for item in raw.get("operations", ()))
                strategies = []
                if "thread.start" in operations:
                    strategies.append("fresh_summary")
                if "thread.fork" in operations:
                    strategies.append("fork_history")
                required_operation = (
                    "thread.start" if self.strategy == "fresh_summary" else "thread.fork"
                )
                supported_efforts = [
                    str(item)
                    for item in raw.get("supported_reasoning_efforts", ())
                ]
                supported_environments = [
                    str(item)
                    for item in raw.get("supported_environment_modes", ())
                ]
                can_create_profile = (
                    raw.get("can_create_with_reasoning_effort") is True
                )
                if self.strategy == "fork_history":
                    can_create_profile = (
                        raw.get("can_fork_with_reasoning_effort") is True
                    )
                available = (
                    raw.get("available") is True
                    and required_operation in operations
                    and can_create_profile
                    and "reuse_bound_checkout" in supported_environments
                )
                self._capabilities = {
                    "provider_id": self.provider_id,
                    "available": available,
                    "automatic": True,
                    "strategies": strategies,
                    "operations": list(operations),
                    "protocol_idempotency": False,
                    "supported_reasoning_efforts": supported_efforts,
                    "can_configure_current_thread": (
                        "thread.configure" in operations
                        and "thread.profile" in operations
                    ),
                    "can_create_with_reasoning_effort": can_create_profile,
                    "can_verify_effective_reasoning_effort": (
                        raw.get("can_verify_effective_reasoning_effort") is True
                    ),
                    "can_reconfigure_unclaimed_successor": (
                        "thread.configure" in operations
                    ),
                    "supported_environment_modes": supported_environments,
                    "can_reuse_bound_checkout": (
                        "reuse_bound_checkout" in supported_environments
                    ),
                    "can_create_worktree": (
                        "provider_managed_worktree" in supported_environments
                    ),
                    "can_query_by_idempotency_key": (
                        "thread.query_by_idempotency_key" in operations
                    ),
                    "reason_code": None
                    if available
                    else "provider.required_operation_unavailable",
                }
            except Exception as error:
                self._capabilities = {
                    "provider_id": self.provider_id,
                    "available": False,
                    "automatic": True,
                    "strategies": [],
                    "operations": [],
                    "protocol_idempotency": False,
                    "supported_reasoning_efforts": [],
                    "can_configure_current_thread": False,
                    "can_create_with_reasoning_effort": False,
                    "can_verify_effective_reasoning_effort": False,
                    "can_reconfigure_unclaimed_successor": False,
                    "supported_environment_modes": [],
                    "can_reuse_bound_checkout": False,
                    "can_create_worktree": False,
                    "can_query_by_idempotency_key": False,
                    "reason_code": f"provider.capability_error.{type(error).__name__}",
                }
        return dict(self._capabilities)

    @property
    def available(self) -> bool:
        return self.capabilities()["available"] is True

    def _request_evidence(
        self,
        *,
        operation: str,
        prompt: str,
        envelope: Mapping[str, Any],
        idempotency_key: str,
        response: Mapping[str, Any],
        execution_profile: Mapping[str, Any],
    ) -> dict[str, Any]:
        safe_response = _redact(response)
        response_effort = (
            safe_response.get("thinking", {}).get("effort")
            if isinstance(safe_response.get("thinking"), Mapping)
            else safe_response.get("thinking")
        )
        response_environment = safe_response.get("environment")
        response_environment_mode = (
            response_environment.get("mode")
            if isinstance(response_environment, Mapping)
            else response_environment
        )
        return {
            "operation": operation,
            "strategy": self.strategy,
            "request_sha256": content_sha256(
                {
                    "operation": operation,
                    "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
                    "envelope_sha256": content_sha256(envelope),
                    "idempotency_key": idempotency_key,
                }
            ),
            "provider_request_id": safe_response.get("request_id")
            if isinstance(safe_response, Mapping)
            else None,
            "transport_status": safe_response.get("status")
            if isinstance(safe_response, Mapping)
            else None,
            "diagnostic": safe_response.get("diagnostic")
            if isinstance(safe_response, Mapping)
            else None,
            "protocol_idempotency_external": False,
            "requested_reasoning_effort": execution_profile["reasoning_effort"],
            "effective_reasoning_effort": response_effort,
            "environment_mode": response_environment_mode,
            "repository_binding_sha256": safe_response.get(
                "repository_binding_sha256"
            ),
        }

    def create_thread(
        self,
        *,
        prompt: str,
        envelope: Mapping[str, Any],
        idempotency_key: str,
        execution_profile: Mapping[str, Any],
    ) -> ThreadCreateResult:
        capabilities = self.capabilities()
        effort = str(execution_profile["reasoning_effort"])
        if (
            capabilities.get("can_create_with_reasoning_effort") is not True
            or effort
            not in tuple(
                str(item)
                for item in capabilities.get("supported_reasoning_efforts", ())
            )
            or capabilities.get("can_reuse_bound_checkout") is not True
        ):
            raise RecordValidationError(
                "Codex provider cannot preserve the accepted execution profile"
            )
        operation = "thread.start" if self.strategy == "fresh_summary" else "thread.fork"
        payload: dict[str, Any] = {
            "prompt": prompt,
            "thinking": {"effort": effort},
            "environment": {
                "mode": "reuse_bound_checkout",
                "repository_binding": dict(envelope["repository_binding"]),
            },
            "metadata": {
                "continuation_envelope": dict(envelope),
                "idempotency_key": idempotency_key,
                "strategy": self.strategy,
            },
        }
        if self.strategy == "fork_history":
            predecessor = envelope.get("predecessor_thread_id")
            if not predecessor:
                raise RecordValidationError("fork-history strategy requires predecessor_thread_id")
            payload["thread_id"] = predecessor
        try:
            response = self.transport.request(
                operation, payload, timeout_seconds=self.timeout_seconds
            )
        except TimeoutError:
            return ThreadCreateResult(
                "timeout",
                None,
                {
                    "operation": operation,
                    "strategy": self.strategy,
                    "reason_code": "provider.timeout",
                    "protocol_idempotency_external": False,
                },
            )
        except Exception as error:
            return ThreadCreateResult(
                "ambiguous",
                None,
                {
                    "operation": operation,
                    "strategy": self.strategy,
                    "reason_code": "provider.ambiguous_exception",
                    "exception_type": type(error).__name__,
                    "protocol_idempotency_external": False,
                },
            )
        if not isinstance(response, Mapping):
            return ThreadCreateResult(
                "ambiguous",
                None,
                {"operation": operation, "reason_code": "provider.invalid_response"},
            )
        status = str(response.get("status") or ("returned" if response.get("thread_id") else "ambiguous"))
        if status not in {
            "returned",
            "definitive_failure",
            "ambiguous",
            "timeout",
            "duplicate",
        }:
            status = "ambiguous"
        thread_id = str(response["thread_id"]) if status == "returned" and response.get("thread_id") else None
        if status == "returned" and not thread_id:
            status = "ambiguous"
        evidence = self._request_evidence(
            operation=operation,
            prompt=prompt,
            envelope=envelope,
            idempotency_key=idempotency_key,
            response=response,
            execution_profile=execution_profile,
        )
        return ThreadCreateResult(status, thread_id, evidence)

    def configure_current_thread(
        self,
        thread_id: str,
        *,
        reasoning_effort: str,
    ) -> Mapping[str, Any]:
        if self.capabilities().get("can_configure_current_thread") is not True:
            raise RecordValidationError(
                "Codex host cannot configure the current discussion programmatically"
            )
        response = self.transport.request(
            "thread.configure",
            {"thread_id": thread_id, "thinking": {"effort": reasoning_effort}},
            timeout_seconds=self.timeout_seconds,
        )
        return {
            "thread_id": str(response.get("thread_id") or thread_id),
            "reasoning_effort": (
                response.get("thinking", {}).get("effort")
                if isinstance(response.get("thinking"), Mapping)
                else response.get("thinking")
            ),
            "evidence_ref": _redact(response.get("request_id"))
            or f"codex-app-server:thread.configure:{thread_id}",
        }

    def read_thread_profile(self, thread_id: str) -> Mapping[str, Any]:
        response = self.transport.request(
            "thread.profile",
            {"thread_id": thread_id},
            timeout_seconds=self.timeout_seconds,
        )
        return {
            "thread_id": str(response.get("thread_id") or thread_id),
            "reasoning_effort": (
                response.get("thinking", {}).get("effort")
                if isinstance(response.get("thinking"), Mapping)
                else response.get("thinking")
            ),
            "model_id": response.get("model"),
            "evidence_ref": _redact(response.get("request_id"))
            or f"codex-app-server:thread.profile:{thread_id}",
        }

    def reconfigure_unclaimed_successor(
        self,
        thread_id: str,
        *,
        reasoning_effort: str,
    ) -> Mapping[str, Any]:
        return self.configure_current_thread(
            thread_id,
            reasoning_effort=reasoning_effort,
        )

    def query_by_idempotency_key(
        self, idempotency_key: str
    ) -> Mapping[str, Any]:
        if self.capabilities().get("can_query_by_idempotency_key") is not True:
            raise RecordValidationError(
                "Codex host cannot query dispatch by idempotency key"
            )
        response = self.transport.request(
            "thread.query_by_idempotency_key",
            {"idempotency_key": idempotency_key},
            timeout_seconds=self.timeout_seconds,
        )
        return _redact(response)

    def read_thread(self, thread_id: str) -> Mapping[str, Any]:
        response = self.transport.request(
            "thread.read", {"thread_id": thread_id}, timeout_seconds=self.timeout_seconds
        )
        return {
            "thread_id": str(response.get("thread_id") or thread_id),
            "status": str(response.get("status") or "unknown"),
            "terminal": response.get("terminal") is True,
            "updated_at": response.get("updated_at"),
        }

    def resume_thread(self, thread_id: str, prompt: str) -> Mapping[str, Any]:
        response = self.transport.request(
            "thread.resume",
            {"thread_id": thread_id, "prompt": prompt},
            timeout_seconds=self.timeout_seconds,
        )
        return {
            "thread_id": str(response.get("thread_id") or thread_id),
            "status": str(response.get("status") or "unknown"),
            "request_id": _redact(response.get("request_id")),
        }

    def confirm_terminal(self, thread_id: str) -> bool:
        return self.read_thread(thread_id)["terminal"] is True
