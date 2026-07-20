"""Timestamp-free canonical fingerprints and repeated-state detection."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.model import canonical_fingerprint, fingerprint_status


EXCLUDED_KEYS = frozenset(
    {
        "timestamp",
        "created_at",
        "updated_at",
        "checked_at",
        "thread_title",
        "assistant_prose",
        "logs",
        "telemetry",
        "usage_metrics",
        "relay_state",
        "lock_files",
        "temporary_files",
        "cache_identity",
        "handoff_token",
        "holder_token",
    }
)


@dataclass(frozen=True)
class FingerprintResult:
    payload: Mapping[str, Any]
    fingerprint: str
    classification: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "payload": copy.deepcopy(dict(self.payload)),
            "fingerprint": self.fingerprint,
            "classification": self.classification,
        }


def _sanitize(value: Any, *, reject_excluded: bool, path: str = "$") -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise RecordValidationError(f"{path}: fingerprint keys must be strings")
            normalized = key.lower().replace("-", "_")
            if normalized in EXCLUDED_KEYS or normalized.endswith("_timestamp"):
                if reject_excluded:
                    raise RecordValidationError(
                        f"{path}.{key}: adapter fingerprint contains nondeterministic or excluded data"
                    )
                continue
            result[key] = _sanitize(
                item,
                reject_excluded=reject_excluded,
                path=f"{path}.{key}",
            )
        return result
    if isinstance(value, list):
        return [
            _sanitize(item, reject_excluded=reject_excluded, path=f"{path}[{index}]")
            for index, item in enumerate(value)
        ]
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise RecordValidationError(f"{path}: unsupported fingerprint value {type(value).__name__}")


def build_payload(
    *,
    repository: Mapping[str, Any],
    control: Mapping[str, Any],
    resolver: Mapping[str, Any],
    validation: Mapping[str, Any],
    checkpoint: Mapping[str, Any],
    adapter_extensions: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the generic canonical payload while excluding telemetry and timestamps."""

    required = {
        "repository": repository,
        "control": control,
        "resolver": resolver,
        "validation": validation,
        "checkpoint": checkpoint,
    }
    for name, value in required.items():
        if not isinstance(value, Mapping):
            raise RecordValidationError(f"fingerprint {name} must be an object")
    repository_value = copy.deepcopy(dict(repository))
    if isinstance(repository_value.get("status_porcelain"), str):
        repository_value["status_porcelain"] = repository_value["status_porcelain"].replace(
            "\r\n", "\n"
        ).replace("\r", "\n")
    payload = {
        "repository": _sanitize(repository_value, reject_excluded=False),
        "control": _sanitize(control, reject_excluded=False),
        "resolver": _sanitize(resolver, reject_excluded=False),
        "validation": _sanitize(validation, reject_excluded=False),
        "checkpoint": _sanitize(checkpoint, reject_excluded=False),
        "adapter_extensions": _sanitize(
            adapter_extensions or {},
            reject_excluded=True,
            path="$.adapter_extensions",
        ),
    }
    return payload


def build_fingerprint(
    history: list[str] | tuple[str, ...],
    **payload_parts: Mapping[str, Any],
) -> FingerprintResult:
    payload = build_payload(**payload_parts)
    fingerprint = canonical_fingerprint(payload)
    return FingerprintResult(payload, fingerprint, fingerprint_status(history, fingerprint))


def apply_fingerprint(mutation: Any, *, generation: int, result: FingerprintResult) -> None:
    record = mutation.record
    if record["state"]["phase"] != "step_verifying":
        raise StateConflict("after fingerprint requires step_verifying")
    entry = record["generations"].get(str(generation))
    if entry is None or entry["invocation_state"] != "returned":
        raise StateConflict("after fingerprint requires a returned generation")
    history = record["state"]["canonical_fingerprint_history"]
    expected = fingerprint_status(history, result.fingerprint)
    if expected != result.classification:
        raise StateConflict("fingerprint classification does not match canonical history")
    entry["after_fingerprint"] = result.fingerprint
    entry["fingerprint_status"] = result.classification
    record["state"]["last_canonical_fingerprint"] = result.fingerprint
    history.append(result.fingerprint)
    mutation.event(
        "fingerprint_captured",
        {
            "generation": generation,
            "fingerprint": result.fingerprint,
            "classification": result.classification,
        },
    )
