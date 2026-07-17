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
                available = raw.get("available") is True and required_operation in operations
                self._capabilities = {
                    "provider_id": self.provider_id,
                    "available": available,
                    "automatic": True,
                    "strategies": strategies,
                    "operations": list(operations),
                    "protocol_idempotency": False,
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
    ) -> dict[str, Any]:
        safe_response = _redact(response)
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
        }

    def create_thread(
        self,
        *,
        prompt: str,
        envelope: Mapping[str, Any],
        idempotency_key: str,
    ) -> ThreadCreateResult:
        operation = "thread.start" if self.strategy == "fresh_summary" else "thread.fork"
        payload: dict[str, Any] = {
            "prompt": prompt,
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
        )
        return ThreadCreateResult(status, thread_id, evidence)

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
