"""Byte-preserving read-only projection of legacy coordinator databases."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from agentjob_runtime.errors import IntegrityError, RecordValidationError, StateConflict
from agentjob_runtime.state_utils import canonical_json_bytes, connect_sqlite, content_sha256, file_sha256


SUPPORTED_SCHEMA_VERSIONS = frozenset({3, 4, 5, 6, 7})


def inspect_legacy_database(path: str | Path) -> dict[str, Any]:
    """Return a read-only audit projection and prove the file stayed unchanged."""

    source = Path(path).resolve()
    before = file_sha256(source)
    with connect_sqlite(source, read_only=True) as connection:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
        }
        if "schema_migrations" in tables:
            versions = [
                int(row[0])
                for row in connection.execute(
                    "SELECT version FROM schema_migrations ORDER BY version"
                )
            ]
            schema_version = max(versions) if versions else 0
        elif "schema_metadata" in tables:
            raw = connection.execute("SELECT schema_version FROM schema_metadata LIMIT 1").fetchone()
            try:
                schema_version = int(str(raw[0]).rsplit(".", 1)[-1]) if raw else 0
            except ValueError:
                schema_version = 0
        else:
            schema_version = 3 if "plans" in tables else 0
        if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
            raise RecordValidationError(
                "legacy database schema family is unsupported",
                details={"schema_version": schema_version},
            )
        counts = {
            table: int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            for table in sorted(tables)
            if table in {
                "goals",
                "plans",
                "plan_task_receipts",
                "plan_provider_intents",
                "plan_leases",
                "plan_journal",
                "journal",
            }
        }
    after = file_sha256(source)
    if before != after:
        raise IntegrityError("read-only legacy inspection changed database bytes")
    projection = {
        "schema_version": "sys4ai.plan-relay-legacy-projection.v1",
        "legacy_schema_version": schema_version,
        "profile": "coordinator_v2_legacy",
        "writer_enabled": False,
        "database_sha256": before,
        "table_counts": counts,
    }
    projection["projection_sha256"] = content_sha256(projection)
    return projection


def export_legacy_database(path: str | Path) -> dict[str, Any]:
    projection = inspect_legacy_database(path)
    return {
        "status": "legacy_exported_read_only",
        "projection": projection,
        "canonical_json_sha256": content_sha256(projection),
    }


def refuse_legacy_mutation(profile: str) -> None:
    if profile != "recursive_chain_v1":
        raise StateConflict(
            "recursive writer refuses legacy coordinator records",
            details={"reason_code": "relay.cross_topology_write_refused", "profile": profile},
        )


def refuse_recursive_legacy_writer(profile: str) -> None:
    if profile == "recursive_chain_v1":
        raise StateConflict(
            "legacy writer refuses recursive relay records",
            details={"reason_code": "relay.cross_topology_write_refused", "profile": profile},
        )

