"""Non-authoritative Codex native Goal mirror adapter."""

from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import asdict, dataclass
from typing import Any, Callable, Mapping, Protocol

from agentjob_runtime.errors import RecordValidationError
from agentjob_runtime.goal.model import utc_now
from agentjob_runtime.records.canonical import content_sha256


SECRET_KEY = re.compile(r"(?:secret|token|password|private.?key|credential|authorization)", re.I)
SECRET_VALUE = re.compile(r"(?:sk-[A-Za-z0-9_-]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")


class NativeGoalTransport(Protocol):
    def set(self, thread_id: str, mirror: Mapping[str, Any]) -> Mapping[str, Any]: ...

    def get(self, thread_id: str) -> Mapping[str, Any] | None: ...

    def clear(self, thread_id: str) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class MirrorReceipt:
    provider_id: str
    operation: str
    status: str
    thread_id: str
    goal_id: str | None
    canonical_revision: int | None
    request_sha256: str | None
    reason_code: str | None
    created_at: str
    authority_effect: str = "mirror_only"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MirrorRead:
    status: str
    mirror: Mapping[str, Any] | None
    stale: bool
    reason_code: str | None
    authority_effect: str = "mirror_only"
    may_mark_complete: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _contains_secret(value: Any, *, key: str = "") -> bool:
    if SECRET_KEY.search(key):
        return True
    if isinstance(value, Mapping):
        return any(_contains_secret(item, key=str(name)) for name, item in value.items())
    if isinstance(value, (list, tuple)):
        return any(_contains_secret(item) for item in value)
    return isinstance(value, str) and SECRET_VALUE.search(value) is not None


def build_goal_mirror(
    record: Mapping[str, Any],
    *,
    canonical_ref: str,
    concise_summary: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    if not concise_summary.strip() or len(concise_summary) > 280:
        raise RecordValidationError("goal mirror summary must contain 1 to 280 characters")
    mirror = {
        "schema_version": "sys4ai.goal-mirror.v1",
        "goal_id": record["goal_id"],
        "goal_sha256": record["goal_sha256"],
        "concise_summary": concise_summary,
        "generation": record["state"]["current_generation"],
        "phase": record["state"]["phase"],
        "canonical_revision": record["state"]["revision"],
        "canonical_ref": canonical_ref,
        "authority_effect": "mirror_only",
        "may_mark_complete": False,
        "updated_at": timestamp or utc_now(),
    }
    if _contains_secret(mirror):
        raise RecordValidationError("goal mirror contains secret-like content")
    return mirror


class CodexNativeGoalProvider:
    provider_id = "codex-native-goal"

    def __init__(
        self,
        transport: NativeGoalTransport | None,
        *,
        enabled: bool = True,
        receipt_sink: Callable[[Mapping[str, Any]], None] | None = None,
        timestamp: str | None = None,
    ) -> None:
        self.transport = transport
        self.enabled = enabled
        self.receipt_sink = receipt_sink
        self.timestamp = timestamp

    @property
    def available(self) -> bool:
        return self.enabled and self.transport is not None

    def capabilities(self) -> Mapping[str, Any]:
        return {
            "provider_id": self.provider_id,
            "available": self.available,
            "mirror_only": True,
            "operations": ["set", "get", "clear"] if self.available else [],
        }

    def _receipt(
        self,
        *,
        operation: str,
        status: str,
        thread_id: str,
        mirror: Mapping[str, Any] | None,
        reason_code: str | None = None,
    ) -> MirrorReceipt:
        receipt = MirrorReceipt(
            self.provider_id,
            operation,
            status,
            thread_id,
            str(mirror["goal_id"]) if mirror else None,
            int(mirror["canonical_revision"]) if mirror else None,
            content_sha256(mirror) if mirror else None,
            reason_code,
            self.timestamp or utc_now(),
        )
        if self.receipt_sink is not None:
            self.receipt_sink(receipt.as_dict())
        return receipt

    @staticmethod
    def _validate_mirror(mirror: Mapping[str, Any]) -> dict[str, Any]:
        value = copy.deepcopy(dict(mirror))
        required = {
            "schema_version",
            "goal_id",
            "goal_sha256",
            "concise_summary",
            "generation",
            "phase",
            "canonical_revision",
            "canonical_ref",
            "authority_effect",
            "may_mark_complete",
            "updated_at",
        }
        if set(value) != required:
            raise RecordValidationError("goal mirror has an invalid exact shape")
        if (
            value["schema_version"] != "sys4ai.goal-mirror.v1"
            or value["authority_effect"] != "mirror_only"
            or value["may_mark_complete"] is not False
        ):
            raise RecordValidationError("goal mirror attempts to claim authority")
        if _contains_secret(value):
            raise RecordValidationError("goal mirror contains secret-like content")
        return value

    def set_mirror(self, thread_id: str, summary: Mapping[str, Any]) -> MirrorReceipt:
        mirror = self._validate_mirror(summary)
        if not self.available:
            return self._receipt(
                operation="set",
                status="unavailable",
                thread_id=thread_id,
                mirror=mirror,
                reason_code="mirror.provider_unavailable",
            )
        try:
            response = self.transport.set(thread_id, mirror)
            status = "pass" if response.get("status") in {"pass", "set", "ok"} else "fail"
            reason = None if status == "pass" else "mirror.provider_rejected"
        except Exception as error:
            status = "fail"
            reason = f"mirror.provider_error.{type(error).__name__}"
        return self._receipt(
            operation="set",
            status=status,
            thread_id=thread_id,
            mirror=mirror,
            reason_code=reason,
        )

    def inspect_mirror(
        self, thread_id: str, *, canonical_record: Mapping[str, Any]
    ) -> MirrorRead:
        if not self.available:
            return MirrorRead("unavailable", None, False, "mirror.provider_unavailable")
        try:
            raw = self.transport.get(thread_id)
        except Exception as error:
            return MirrorRead(
                "unavailable",
                None,
                False,
                f"mirror.provider_error.{type(error).__name__}",
            )
        if raw is None:
            return MirrorRead("missing", None, False, "mirror.not_found")
        try:
            mirror = self._validate_mirror(raw)
        except RecordValidationError:
            return MirrorRead("invalid", None, True, "mirror.invalid")
        stale = any(
            (
                mirror["goal_id"] != canonical_record["goal_id"],
                mirror["goal_sha256"] != canonical_record["goal_sha256"],
                mirror["canonical_revision"] != canonical_record["state"]["revision"],
                mirror["generation"] != canonical_record["state"]["current_generation"],
                mirror["phase"] != canonical_record["state"]["phase"],
            )
        )
        return MirrorRead(
            "stale" if stale else "current",
            mirror,
            stale,
            "mirror.stale" if stale else None,
        )

    def get_mirror(self, thread_id: str) -> Mapping[str, Any] | None:
        if not self.available:
            return None
        try:
            value = self.transport.get(thread_id)
            return self._validate_mirror(value) if value is not None else None
        except Exception:
            return None

    def clear_mirror(self, thread_id: str) -> MirrorReceipt:
        if not self.available:
            return self._receipt(
                operation="clear",
                status="unavailable",
                thread_id=thread_id,
                mirror=None,
                reason_code="mirror.provider_unavailable",
            )
        try:
            response = self.transport.clear(thread_id)
            status = "pass" if response.get("status") in {"pass", "cleared", "ok"} else "fail"
            reason = None if status == "pass" else "mirror.provider_rejected"
        except Exception as error:
            status = "fail"
            reason = f"mirror.provider_error.{type(error).__name__}"
        return self._receipt(
            operation="clear",
            status=status,
            thread_id=thread_id,
            mirror=None,
            reason_code=reason,
        )
