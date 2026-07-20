"""Minimal secret screening and deterministic redaction for durable evidence."""

from __future__ import annotations

import re
from typing import Any, Mapping, Sequence


REDACTION = "[REDACTED]"
SECRET_PATTERNS = (
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(
        r"(?i)\b(?:api[_ -]?key|access[_ -]?token|client[_ -]?secret|password)\s*[:=]\s*\S+"
    ),
)


def contains_secret(value: str) -> bool:
    return any(pattern.search(value) for pattern in SECRET_PATTERNS)


def redact_secrets(value: str) -> str:
    result = value
    for pattern in SECRET_PATTERNS:
        result = pattern.sub(REDACTION, result)
    return result


def redact_value(value: Any) -> Any:
    """Return a JSON-like value with detected string secrets replaced."""

    if isinstance(value, str):
        return redact_secrets(value)
    if isinstance(value, Mapping):
        return {str(key): redact_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return tuple(redact_value(item) for item in value)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [redact_value(item) for item in value]
    return value
