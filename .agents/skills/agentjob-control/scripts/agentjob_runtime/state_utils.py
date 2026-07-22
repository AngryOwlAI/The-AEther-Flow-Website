"""Neutral deterministic state utilities shared by goal and plan runtimes."""

from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import json
import os
import sqlite3
import tempfile
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

from agentjob_runtime.errors import IntegrityError, RecordValidationError


UTC = dt.timezone.utc


def utc_now() -> str:
    """Return a canonical second-precision UTC timestamp."""

    return dt.datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> dt.datetime:
    """Parse a timezone-aware RFC 3339 timestamp and normalize it to UTC."""

    if not isinstance(value, str) or not value:
        raise RecordValidationError("timestamp must be a nonblank RFC 3339 string")
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = dt.datetime.fromisoformat(candidate)
    except ValueError as error:
        raise RecordValidationError("timestamp is not valid RFC 3339") from error
    if parsed.tzinfo is None:
        raise RecordValidationError("timestamp must include a timezone")
    return parsed.astimezone(UTC)


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize strict canonical JSON used by authoritative hashes."""

    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise RecordValidationError("value is not canonical-JSON serializable") from error


def content_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def bytes_sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_private_parent(path: str | Path) -> Path:
    target = Path(path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with contextlib.suppress(OSError):
        target.parent.chmod(0o700)
    return target


def connect_sqlite(path: str | Path, *, read_only: bool = False) -> sqlite3.Connection:
    target = Path(path).resolve()
    if read_only:
        connection = sqlite3.connect(f"file:{target}?mode=ro", uri=True, timeout=10.0)
    else:
        target = require_private_parent(target)
        connection = sqlite3.connect(target, timeout=10.0)
        with contextlib.suppress(OSError):
            target.chmod(0o600)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    if not read_only:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
    return connection


@contextlib.contextmanager
def immediate_transaction(connection: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    connection.execute("BEGIN IMMEDIATE")
    try:
        yield connection
        connection.commit()
    except BaseException:
        connection.rollback()
        raise


def sqlite_backup(source: str | Path, destination: str | Path) -> dict[str, Any]:
    source_path = Path(source).resolve()
    destination_path = require_private_parent(destination)
    if destination_path.exists():
        raise IntegrityError("backup destination already exists")
    with connect_sqlite(source_path, read_only=True) as source_connection:
        with sqlite3.connect(destination_path) as destination_connection:
            source_connection.backup(destination_connection)
    with contextlib.suppress(OSError):
        destination_path.chmod(0o600)
    return {
        "source": str(source_path),
        "destination": str(destination_path),
        "source_sha256": file_sha256(source_path),
        "backup_sha256": file_sha256(destination_path),
    }


def atomic_write(path: str | Path, payload: bytes) -> None:
    target = require_private_parent(path)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        with contextlib.suppress(FileNotFoundError):
            Path(temporary).unlink()


def canonical_export_hash(records: Mapping[str, Any]) -> str:
    return content_sha256(dict(records))

