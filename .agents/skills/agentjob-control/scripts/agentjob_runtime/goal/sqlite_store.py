"""SQLite-backed goal state, transactional migrations, and normalized constraints."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import secrets
import sqlite3
import stat
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Sequence

from agentjob_runtime.errors import (
    ActiveRelayError,
    IntegrityError,
    MigrationError,
    RecordNotFound,
    RecordValidationError,
    StateConflict,
)
from agentjob_runtime.goal.model import (
    append_journal,
    effective_guards,
    repository_identity_hash,
    utc_now,
    validate_goal_record,
)
from agentjob_runtime.goal.locking import CrossPlatformFileLock, LockBackend
from agentjob_runtime.records.canonical import canonical_json_bytes, content_sha256


SQL_UNLIMITED_DEADLINE = "__SYS4AI_UNLIMITED__"
CURRENT_SQLITE_SCHEMA_VERSION = 7
# Compatibility alias for callers that imported the former goal-store name.
DEFAULT_SCHEMA_VERSION = CURRENT_SQLITE_SCHEMA_VERSION
MIGRATION_BACKUP_SCHEMA_VERSION = "sys4ai.sqlite-migration-backup.v1"
CREATE_SCHEMA_OBJECT = re.compile(
    r"^\s*CREATE\s+(?:UNIQUE\s+)?"
    r"(TABLE|INDEX|VIEW|TRIGGER)\s+"
    r"(?:IF\s+NOT\s+EXISTS\s+)?"
    r"(?:[\"`\[])?([A-Za-z_][A-Za-z0-9_]*)",
    re.IGNORECASE | re.MULTILINE,
)


def _deadline_projections(record: Mapping[str, Any]) -> tuple[str, str | None]:
    effective = effective_guards(record).get("deadline_at", record["deadline_at"])
    return (
        record["deadline_at"]
        if record["deadline_at"] is not None
        else SQL_UNLIMITED_DEADLINE,
        effective,
    )


@dataclass(frozen=True)
class Migration:
    version: int
    name: str
    sql: str

    @property
    def checksum(self) -> str:
        return hashlib.sha256(self.sql.encode("utf-8")).hexdigest()


@dataclass
class GoalMutation:
    store: "SQLiteGoalStore"
    connection: sqlite3.Connection
    record: dict[str, Any]
    original_revision: int
    original_journal_length: int
    original_amendment_length: int
    timestamp: str
    provider_receipts: list[dict[str, Any]] = field(default_factory=list)
    recovery_actions: list[dict[str, Any]] = field(default_factory=list)

    def event(self, event_type: str, payload: Mapping[str, Any] | None = None) -> str:
        body = {"event_type": event_type, **copy.deepcopy(dict(payload or {}))}
        body.setdefault("timestamp", self.timestamp)
        return append_journal(self.record, "event", body)

    def recovery(
        self,
        action: str,
        *,
        user_authorization: str,
        evidence: Mapping[str, Any],
        prior_phase: str,
        resulting_phase: str,
    ) -> str:
        payload = {
            "recovery_action": action,
            "user_authorization": user_authorization,
            "evidence": copy.deepcopy(dict(evidence)),
            "prior_phase": prior_phase,
            "resulting_phase": resulting_phase,
            "timestamp": self.timestamp,
        }
        entry_hash = append_journal(self.record, "recovery", payload)
        self.recovery_actions.append({**payload, "action_hash": entry_hash})
        return entry_hash

    def amendment(self, amendment: Mapping[str, Any]) -> str:
        return append_journal(self.record, "amendment", amendment)

    def receipt(self, payload: Mapping[str, Any]) -> str:
        return append_journal(self.record, "step_receipt", payload)

    def provider_receipt(
        self,
        *,
        generation: int,
        provider_id: str,
        idempotency_key: str,
        provider_status: str,
        returned_thread_id: str | None,
        response: Mapping[str, Any],
    ) -> None:
        self.provider_receipts.append(
            {
                "generation": generation,
                "provider_id": provider_id,
                "idempotency_key": idempotency_key,
                "provider_status": provider_status,
                "returned_thread_id": returned_thread_id,
                "response": copy.deepcopy(dict(response)),
                "created_at": self.timestamp,
            }
        )

    def replace_lease(
        self,
        *,
        generation: int,
        holder_kind: str,
        holder_token: str,
        expires_at: str,
    ) -> dict[str, Any]:
        binding_hash = repository_identity_hash(self.record["repository_binding"])
        prior = self.record["state"].get("active_lease")
        acquired_at = prior["acquired_at"] if prior else self.timestamp
        transaction_id = secrets.token_hex(16)
        lease = {
            "repository_fingerprint": binding_hash,
            "goal_id": self.record["goal_id"],
            "generation": generation,
            "holder_kind": holder_kind,
            "holder_token": holder_token,
            "transaction_id": transaction_id,
            "acquired_at": acquired_at,
            "heartbeat_at": self.timestamp,
            "expires_at": expires_at,
        }
        self.connection.execute(
            "UPDATE leases SET lease_state='released', released_at=? "
            "WHERE goal_id=? AND lease_state='active'",
            (self.timestamp, self.record["goal_id"]),
        )
        try:
            self.connection.execute(
                """
                INSERT INTO leases(
                    repository_fingerprint, goal_id, generation, holder_kind,
                    holder_token, transaction_id, acquired_at, heartbeat_at,
                    expires_at, lease_state, released_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', NULL)
                """,
                (
                    binding_hash,
                    self.record["goal_id"],
                    generation,
                    holder_kind,
                    holder_token,
                    transaction_id,
                    acquired_at,
                    self.timestamp,
                    expires_at,
                ),
            )
        except sqlite3.IntegrityError as error:
            raise ActiveRelayError(
                "another goal relay owns the repository worktree",
                details={"repository_fingerprint": binding_hash},
            ) from error
        self.record["state"]["active_lease"] = lease
        return lease

    def release_lease(self) -> None:
        self.connection.execute(
            "UPDATE leases SET lease_state='released', released_at=? "
            "WHERE goal_id=? AND lease_state='active'",
            (self.timestamp, self.record["goal_id"]),
        )
        self.record["state"]["active_lease"] = None

    def heartbeat(self, *, expires_at: str) -> None:
        lease = self.record["state"].get("active_lease")
        if lease is None:
            raise StateConflict("goal has no active lease")
        lease["heartbeat_at"] = self.timestamp
        lease["expires_at"] = expires_at
        self.connection.execute(
            "UPDATE leases SET heartbeat_at=?, expires_at=? "
            "WHERE transaction_id=? AND lease_state='active'",
            (self.timestamp, expires_at, lease["transaction_id"]),
        )


class SQLiteGoalStore:
    """Canonical default backend for durable goal relay state."""

    def __init__(
        self,
        database_path: str | Path,
        *,
        busy_timeout_ms: int = 5000,
        auto_migrate: bool = True,
        read_only: bool = False,
        target_schema_version: int = DEFAULT_SCHEMA_VERSION,
        lock_backend: LockBackend = "auto",
        lock_timeout_seconds: float = 5.0,
    ) -> None:
        supplied = Path(database_path).expanduser().absolute()
        if supplied.is_symlink() or supplied.parent.is_symlink():
            raise IntegrityError("SQLite state database may not be a symlink")
        self.path = supplied.resolve(strict=False)
        self.read_only = read_only
        if not isinstance(target_schema_version, int) or target_schema_version <= 0:
            raise ValueError("target_schema_version must be a positive integer")
        self.target_schema_version = target_schema_version
        self.lock_backend = lock_backend
        self.lock_timeout_seconds = lock_timeout_seconds
        if not read_only:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.parent.is_symlink():
            raise IntegrityError("SQLite state directory may not be a symlink")
        if self.path.exists():
            metadata = self.path.lstat()
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise IntegrityError(
                    "SQLite state database must be one regular non-symlink file"
                )
        self.busy_timeout_ms = busy_timeout_ms
        if auto_migrate:
            if read_only:
                raise ValueError("a read-only SQLite store cannot apply migrations")
            self.apply_migrations()

    @property
    def migration_directory(self) -> Path:
        return Path(__file__).resolve().parent / "migrations"

    def migrations(self) -> list[Migration]:
        result: list[Migration] = []
        for path in sorted(self.migration_directory.glob("[0-9][0-9][0-9]_*.sql")):
            version_text, _, name = path.stem.partition("_")
            result.append(Migration(int(version_text), name, path.read_text(encoding="utf-8")))
        return result

    def connect(self) -> sqlite3.Connection:
        if self.read_only:
            connection = sqlite3.connect(
                f"{self.path.as_uri()}?mode=ro",
                uri=True,
                timeout=self.busy_timeout_ms / 1000,
            )
        else:
            connection = sqlite3.connect(self.path, timeout=self.busy_timeout_ms / 1000)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute(f"PRAGMA busy_timeout={int(self.busy_timeout_ms)}")
        if self.read_only:
            connection.execute("PRAGMA query_only=ON")
        else:
            connection.execute("PRAGMA synchronous=FULL")
            connection.execute("PRAGMA journal_mode=WAL")
        return connection

    @staticmethod
    def _table_exists(connection: sqlite3.Connection, name: str) -> bool:
        row = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
        ).fetchone()
        return row is not None

    def current_schema_version(self, connection: sqlite3.Connection | None = None) -> int:
        own = connection is None
        connection = connection or self.connect()
        try:
            if not self._table_exists(connection, "schema_migrations"):
                return 0
            row = connection.execute("SELECT COALESCE(MAX(version), 0) FROM schema_migrations").fetchone()
            return int(row[0])
        finally:
            if own:
                connection.close()

    @property
    def migration_lock_path(self) -> Path:
        return self.path.with_name(f".{self.path.name}.migration.lock")

    @property
    def migration_backup_root(self) -> Path:
        return self.path.with_name(f".{self.path.name}.migration-backups")

    def _migration_lock(self) -> CrossPlatformFileLock:
        if self.migration_lock_path.exists():
            metadata = self.migration_lock_path.lstat()
            if (
                not stat.S_ISREG(metadata.st_mode)
                or stat.S_ISLNK(metadata.st_mode)
                or metadata.st_nlink != 1
            ):
                raise IntegrityError(
                    "migration lock must be one regular non-symlink file"
                )
        return CrossPlatformFileLock(
            self.migration_lock_path,
            backend=self.lock_backend,
            timeout_seconds=self.lock_timeout_seconds,
        )

    @staticmethod
    def _migration_map(migrations: Sequence[Migration]) -> dict[int, Migration]:
        result: dict[int, Migration] = {}
        for migration in migrations:
            if migration.version in result:
                raise MigrationError(
                    f"duplicate migration version: {migration.version}"
                )
            result[migration.version] = migration
        return result

    def _known_migrations(
        self, planned: Sequence[Migration]
    ) -> dict[int, Migration]:
        known = self._migration_map(self.migrations())
        for version, migration in self._migration_map(planned).items():
            canonical = known.get(version)
            if canonical is not None and (
                canonical.name != migration.name
                or canonical.checksum != migration.checksum
            ):
                raise MigrationError(
                    f"planned migration {version} conflicts with canonical bytes",
                    details={
                        "version": version,
                        "canonical_name": canonical.name,
                        "canonical_checksum": canonical.checksum,
                        "planned_name": migration.name,
                        "planned_checksum": migration.checksum,
                    },
                )
            known[version] = migration
        return known

    def _validate_migration_history(
        self,
        connection: sqlite3.Connection,
        *,
        known: Mapping[int, Migration],
        writer_target: int,
    ) -> list[dict[str, Any]]:
        if not self._table_exists(connection, "schema_migrations"):
            return []
        rows = [
            dict(row)
            for row in connection.execute(
                "SELECT version, name, checksum, applied_at "
                "FROM schema_migrations ORDER BY version"
            )
        ]
        versions = [int(row["version"]) for row in rows]
        if versions != list(range(1, len(versions) + 1)):
            raise MigrationError(
                "applied migration history is not contiguous",
                details={"applied_versions": versions},
            )
        for row in rows:
            version = int(row["version"])
            if version > writer_target:
                raise MigrationError(
                    "database schema is newer than the configured writer target",
                    details={
                        "database_version": versions[-1],
                        "writer_target": writer_target,
                    },
                )
            expected = known.get(version)
            if expected is None:
                raise MigrationError(
                    f"applied migration {version} is unknown to this writer"
                )
            if (
                row["name"] != expected.name
                or row["checksum"] != expected.checksum
            ):
                raise MigrationError(
                    f"migration {version} does not match applied checksum",
                    details={
                        "version": version,
                        "expected_name": expected.name,
                        "expected_checksum": expected.checksum,
                        "actual_name": row["name"],
                        "actual_checksum": row["checksum"],
                    },
                )
        return rows

    @staticmethod
    def _declared_schema_objects(
        migrations: Sequence[Migration],
    ) -> dict[str, str]:
        objects: dict[str, str] = {}
        for migration in migrations:
            for match in CREATE_SCHEMA_OBJECT.finditer(migration.sql):
                object_type, name = match.groups()
                objects[name] = object_type.lower()
        return objects

    def _validate_schema_objects(
        self,
        connection: sqlite3.Connection,
        *,
        migrations: Sequence[Migration],
    ) -> None:
        expected = self._declared_schema_objects(migrations)
        actual = {
            row["name"]: row["type"]
            for row in connection.execute(
                "SELECT type, name FROM sqlite_master "
                "WHERE type IN ('table', 'index', 'view', 'trigger')"
            )
        }
        missing = [
            {"name": name, "type": object_type}
            for name, object_type in sorted(expected.items())
            if actual.get(name) != object_type
        ]
        if missing:
            raise MigrationError(
                "database schema objects disagree with applied migrations",
                details={"missing_or_mismatched_objects": missing},
            )
        if len(migrations) >= 2:
            goal_columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(goals)")
            }
            if "effective_deadline_at" not in goal_columns:
                raise MigrationError(
                    "database schema version 2 lacks effective_deadline_at"
                )
        if len(migrations) >= 4:
            generation_columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(generations)")
            }
            required = {
                "requested_reasoning_effort",
                "effective_reasoning_effort",
                "profile_evidence_json",
                "environment_mode",
                "observed_repository_topology_json",
                "resolution_disposition_json",
                "repair_strategy_id",
                "strategy_attempt",
                "material_progress_dimensions_json",
                "human_necessity_report_ref",
                "completion_report_ref",
            }
            if not required <= generation_columns:
                raise MigrationError(
                    "database schema version 4 lacks goal v3 generation columns"
                )
        if len(migrations) >= 5:
            plan_columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(plans)")
            }
            required_plan_columns = {
                "runtime_profile_version",
                "activation_sequence",
                "activation_receipt_sha256",
                "execution_profile_json",
                "topology_policy_json",
                "activation_goal_text",
                "activation_goal_sha256",
                "profile_effective_from_generation",
                "repository_binding_sha256",
            }
            if not required_plan_columns <= plan_columns:
                raise MigrationError(
                    "database schema version 5 lacks plan profile columns"
                )
            provider_columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(plan_provider_intents)"
                )
            }
            required_provider_columns = {
                "execution_profile_sha256",
                "requested_reasoning_effort",
                "effective_reasoning_effort",
                "profile_verification_status",
                "profile_evidence_ref",
                "environment_mode",
                "repository_binding_sha256",
                "observed_topology_sha256",
                "same_thread_profile_repair_json",
            }
            if not required_provider_columns <= provider_columns:
                raise MigrationError(
                    "database schema version 5 lacks plan provider profile columns"
                )
            if not self._table_exists(connection, "plan_activation_receipts"):
                raise MigrationError(
                    "database schema version 5 lacks plan activation receipts"
                )
        if len(migrations) >= 6:
            required_tables = {
                "plan_question_batches",
                "plan_execution_authorities",
                "plan_question_responses",
                "plan_continuous_states",
                "plan_coordinator_wakeups",
                "plan_completion_reports",
            }
            missing_tables = sorted(
                table
                for table in required_tables
                if not self._table_exists(connection, table)
            )
            if missing_tables:
                raise MigrationError(
                    "database schema version 6 lacks continuous plan tables",
                    details={"missing_tables": missing_tables},
                )
        if len(migrations) >= 7:
            required_tables = {
                "goal_question_batches",
                "goal_execution_authorities",
                "goal_question_responses",
                "goal_grant_consumptions",
                "goal_coordinator_states",
            }
            missing_tables = sorted(
                table
                for table in required_tables
                if not self._table_exists(connection, table)
            )
            if missing_tables:
                raise MigrationError(
                    "database schema version 7 lacks continuous goal tables",
                    details={"missing_tables": missing_tables},
                )

    def _validate_goal_parity(self, connection: sqlite3.Connection) -> None:
        if not self._table_exists(connection, "goals"):
            return
        for row in connection.execute("SELECT * FROM goals ORDER BY goal_id"):
            try:
                record = json.loads(row["record_json"])
                validate_goal_record(record)
                self._validate_immutable_parity(row, record)
                self._validate_deadline_parity(row, record)
                self._validate_lease_parity(connection, record)
            except (
                KeyError,
                TypeError,
                ValueError,
                json.JSONDecodeError,
                RecordValidationError,
            ) as error:
                raise IntegrityError(
                    f"canonical goal parity failed for {row['goal_id']}"
                ) from error

    @staticmethod
    def _check_rows(connection: sqlite3.Connection, pragma: str) -> list[Any]:
        return [
            row[0] if len(row) == 1 else dict(row)
            for row in connection.execute(pragma)
        ]

    def _migration_preflight(
        self,
        connection: sqlite3.Connection,
        *,
        known: Mapping[int, Migration],
        writer_target: int,
    ) -> dict[str, Any]:
        history = self._validate_migration_history(
            connection,
            known=known,
            writer_target=writer_target,
        )
        current = int(history[-1]["version"]) if history else 0
        quick = self._check_rows(connection, "PRAGMA quick_check")
        integrity = self._check_rows(connection, "PRAGMA integrity_check")
        foreign_keys = self._check_rows(connection, "PRAGMA foreign_key_check")
        if quick != ["ok"] or integrity != ["ok"] or foreign_keys:
            raise MigrationError(
                "database failed pre-migration integrity checks",
                details={
                    "quick_check": quick,
                    "integrity_check": integrity,
                    "foreign_key_check": foreign_keys,
                },
            )
        applied = [known[version] for version in range(1, current + 1)]
        self._validate_schema_objects(connection, migrations=applied)
        self._validate_goal_parity(connection)
        marker = content_sha256(
            {
                "schema_migrations": history,
                "goals": [
                    {
                        "goal_id": row["goal_id"],
                        "state_revision": row["state_revision"],
                        "updated_at": row["updated_at"],
                        "record_sha256": hashlib.sha256(
                            row["record_json"].encode("utf-8")
                        ).hexdigest(),
                    }
                    for row in connection.execute(
                        "SELECT goal_id, state_revision, updated_at, record_json "
                        "FROM goals ORDER BY goal_id"
                    )
                ]
                if self._table_exists(connection, "goals")
                else [],
            }
        )
        return {
            "schema_version": current,
            "migration_history_sha256": content_sha256(history),
            "source_marker_sha256": marker,
            "quick_check": quick,
            "integrity_check": integrity,
            "foreign_key_findings": foreign_keys,
            "canonical_goal_parity": "pass",
        }

    @staticmethod
    def _fsync_file(path: Path) -> None:
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    @staticmethod
    def _fsync_directory(path: Path) -> None:
        try:
            descriptor = os.open(path, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(descriptor)
        except OSError:
            pass
        finally:
            os.close(descriptor)

    @staticmethod
    def _atomic_private_write(path: Path, payload: bytes) -> None:
        if path.exists() or path.is_symlink():
            raise IntegrityError(f"refusing to replace migration artifact: {path}")
        temporary = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        try:
            try:
                with os.fdopen(descriptor, "wb", closefd=False) as handle:
                    handle.write(payload)
                    handle.flush()
                    os.fsync(handle.fileno())
            finally:
                os.close(descriptor)
            try:
                os.link(temporary, path)
            except FileExistsError as error:
                raise IntegrityError(
                    f"refusing to replace migration artifact: {path}"
                ) from error
        finally:
            temporary.unlink(missing_ok=True)
        os.chmod(path, 0o600)

    def _prepare_backup_root(self) -> Path:
        root = self.migration_backup_root
        if root.exists():
            metadata = root.lstat()
            if not stat.S_ISDIR(metadata.st_mode) or root.is_symlink():
                raise IntegrityError(
                    "migration backup root must be a non-symlink directory"
                )
        else:
            root.mkdir(mode=0o700)
        try:
            os.chmod(root, 0o700)
        except OSError:
            pass
        if root.resolve().parent != self.path.parent:
            raise IntegrityError("migration backup root escapes the state directory")
        return root

    @staticmethod
    def _file_evidence(path: Path, root: Path) -> dict[str, Any]:
        metadata = path.stat()
        return {
            "path": path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "size": metadata.st_size,
            "mode": f"{stat.S_IMODE(metadata.st_mode):04o}",
        }

    def _create_migration_backup(
        self,
        *,
        guard_connection: sqlite3.Connection,
        migration: Migration,
        preflight: Mapping[str, Any],
        timestamp: str,
    ) -> Path:
        root = self._prepare_backup_root()
        token = secrets.token_hex(8)
        stem = (
            f"{self.path.name}.pre-migration-v{preflight['schema_version']}"
            f"-to-v{migration.version}-{token}"
        )
        database_path = root / f"{stem}.sqlite3"
        export_path = root / f"{stem}.json"
        manifest_path = root / f"{stem}.manifest.json"
        temporary_database = root / f".{stem}.{secrets.token_hex(8)}.tmp"
        descriptor = os.open(
            temporary_database,
            os.O_RDWR | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        os.close(descriptor)
        try:
            source = sqlite3.connect(
                f"{self.path.as_uri()}?mode=ro",
                uri=True,
                timeout=self.busy_timeout_ms / 1000,
            )
            source.row_factory = sqlite3.Row
            destination = sqlite3.connect(temporary_database)
            destination.row_factory = sqlite3.Row
            try:
                source.execute("PRAGMA query_only=ON")
                source.execute("BEGIN")
                source.backup(destination)
                export_payload = (
                    json.dumps(
                        self.export_data(source),
                        ensure_ascii=False,
                        sort_keys=True,
                        indent=2,
                    ).encode("utf-8")
                    + b"\n"
                )
                backup_integrity = self._check_rows(
                    destination, "PRAGMA integrity_check"
                )
                backup_foreign_keys = self._check_rows(
                    destination, "PRAGMA foreign_key_check"
                )
                if backup_integrity != ["ok"] or backup_foreign_keys:
                    raise MigrationError(
                        "online migration backup failed integrity validation",
                        details={
                            "integrity_check": backup_integrity,
                            "foreign_key_check": backup_foreign_keys,
                        },
                    )
                destination.commit()
            finally:
                destination.close()
                source.close()
            self._fsync_file(temporary_database)
            try:
                os.link(temporary_database, database_path)
            except FileExistsError as error:
                raise IntegrityError(
                    f"refusing to replace migration artifact: {database_path}"
                ) from error
        finally:
            temporary_database.unlink(missing_ok=True)
        os.chmod(database_path, 0o600)
        self._atomic_private_write(export_path, export_payload)
        source_metadata = self.path.stat()
        manifest = {
            "schema_version": MIGRATION_BACKUP_SCHEMA_VERSION,
            "source_database": {
                "path": str(self.path),
                "device": source_metadata.st_dev,
                "inode": source_metadata.st_ino,
                "size": source_metadata.st_size,
                "mode": f"{stat.S_IMODE(source_metadata.st_mode):04o}",
            },
            "from_version": preflight["schema_version"],
            "to_version": migration.version,
            "migration": {
                "name": migration.name,
                "checksum": migration.checksum,
            },
            "created_at": timestamp,
            "preflight": dict(preflight),
            "backup_database": self._file_evidence(database_path, root),
            "json_export": self._file_evidence(export_path, root),
        }
        self._atomic_private_write(
            manifest_path,
            canonical_json_bytes(manifest) + b"\n",
        )
        self._fsync_directory(root)
        marker_after = self._migration_preflight(
            guard_connection,
            known=self._known_migrations([migration]),
            writer_target=migration.version,
        )["source_marker_sha256"]
        if marker_after != preflight["source_marker_sha256"]:
            raise MigrationError(
                "source database changed after the migration backup",
                details={"backup_manifest": str(manifest_path)},
            )
        return manifest_path

    @staticmethod
    def _execute_migration_sql(
        connection: sqlite3.Connection, migration: Migration
    ) -> None:
        transaction_tokens = re.compile(
            r"^\s*(?:BEGIN|COMMIT|ROLLBACK|END\s+TRANSACTION|"
            r"VACUUM|ATTACH|DETACH)\b",
            re.IGNORECASE,
        )
        pending = ""
        for line in migration.sql.splitlines(keepends=True):
            pending += line
            if not sqlite3.complete_statement(pending):
                continue
            statement = pending.strip()
            pending = ""
            has_sql = statement and any(
                value.strip() and not value.lstrip().startswith("--")
                for value in statement.splitlines()
            )
            if not has_sql:
                continue
            executable = "\n".join(
                value
                for value in statement.splitlines()
                if not value.lstrip().startswith("--")
            )
            if transaction_tokens.match(executable):
                raise MigrationError(
                    f"migration {migration.version} contains forbidden "
                    "transaction control"
                )
            connection.execute(statement)
        if pending.strip() and any(
            value.strip() and not value.lstrip().startswith("--")
            for value in pending.splitlines()
        ):
            raise MigrationError(
                f"migration {migration.version} ends with incomplete SQL"
            )

    def apply_migrations(self, migrations: Sequence[Migration] | None = None) -> list[Path]:
        available = self.migrations()
        available_versions = [migration.version for migration in available]
        if available_versions != list(range(1, len(available_versions) + 1)):
            raise MigrationError(
                "canonical migration sequence is not contiguous",
                details={"available_versions": available_versions},
            )
        if migrations is None:
            if self.target_schema_version not in available_versions:
                raise MigrationError(
                    "configured schema target has no matching migration",
                    details={
                        "writer_target": self.target_schema_version,
                        "available_versions": available_versions,
                    },
                )
            planned = [
                migration
                for migration in available
                if migration.version <= self.target_schema_version
            ]
            writer_target = self.target_schema_version
        else:
            planned = list(migrations)
            writer_target = (
                max((migration.version for migration in planned), default=0)
                or self.target_schema_version
            )
        planned.sort(key=lambda migration: migration.version)
        known = self._known_migrations(planned)
        backups: list[Path] = []
        with self._migration_lock():
            connection = self.connect()
            try:
                current_history = self._validate_migration_history(
                    connection,
                    known=known,
                    writer_target=writer_target,
                )
                current = (
                    int(current_history[-1]["version"])
                    if current_history
                    else 0
                )
                applied = [
                    known[version] for version in range(1, current + 1)
                ]
                self._validate_schema_objects(
                    connection,
                    migrations=applied,
                )
                pending_migrations = [
                    migration
                    for migration in planned
                    if migration.version > current
                ]
                if not pending_migrations:
                    if current != writer_target:
                        raise MigrationError(
                            "database schema does not match configured "
                            "writer target",
                            details={
                                "database_version": current,
                                "writer_target": writer_target,
                            },
                        )
                    return backups
                for migration in pending_migrations:
                    if migration.version != current + 1:
                        raise MigrationError(
                            "migration sequence gap: "
                            f"current={current}, next={migration.version}"
                        )
                    backup_for_migration: Path | None = None
                    applied_at = utc_now()
                    connection.execute("BEGIN IMMEDIATE")
                    preflight = self._migration_preflight(
                        connection,
                        known=known,
                        writer_target=writer_target,
                    )
                    if preflight["schema_version"] != current:
                        raise MigrationError(
                            "source schema changed before migration"
                        )
                    if current:
                        backup_for_migration = self._create_migration_backup(
                            guard_connection=connection,
                            migration=migration,
                            preflight=preflight,
                            timestamp=applied_at,
                        )
                        backups.append(backup_for_migration)
                    try:
                        self._execute_migration_sql(connection, migration)
                        connection.execute(
                            "INSERT INTO schema_migrations"
                            "(version, name, checksum, applied_at) "
                            "VALUES (?, ?, ?, ?)",
                            (
                                migration.version,
                                migration.name,
                                migration.checksum,
                                applied_at,
                            ),
                        )
                        pending = self._migration_preflight(
                            connection,
                            known=known,
                            writer_target=writer_target,
                        )
                        if pending["schema_version"] != migration.version:
                            raise MigrationError(
                                "migration row and schema version disagree"
                            )
                        connection.commit()
                    except Exception:
                        connection.rollback()
                        raise
                    current = migration.version
                    connection.execute("PRAGMA wal_checkpoint(FULL)")
                    self._fsync_file(self.path)
                    wal_path = self.path.with_name(f"{self.path.name}-wal")
                    if wal_path.exists():
                        self._fsync_file(wal_path)
                    self._fsync_directory(self.path.parent)
                    postflight = self._migration_preflight(
                        connection,
                        known=known,
                        writer_target=writer_target,
                    )
                    if postflight["schema_version"] != current:
                        raise MigrationError(
                            "post-migration schema version parity failed"
                        )
                final_history = self._validate_migration_history(
                    connection,
                    known=known,
                    writer_target=writer_target,
                )
                final_version = (
                    int(final_history[-1]["version"])
                    if final_history
                    else 0
                )
                final_applied = [
                    known[version]
                    for version in range(1, final_version + 1)
                ]
                self._validate_schema_objects(
                    connection,
                    migrations=final_applied,
                )
                if final_version != writer_target:
                    raise MigrationError(
                        "database schema does not match configured writer target",
                        details={
                            "database_version": final_version,
                            "writer_target": writer_target,
                        },
                    )
                return backups
            except sqlite3.Error as error:
                try:
                    connection.rollback()
                except sqlite3.Error:
                    pass
                raise MigrationError(
                    "SQLite migration failed",
                    details={
                        "database": str(self.path),
                        "backup_paths": [str(path) for path in backups],
                    },
                ) from error
            except (IntegrityError, MigrationError) as error:
                try:
                    connection.rollback()
                except sqlite3.Error:
                    pass
                details = dict(error.details)
                details.setdefault("database", str(self.path))
                details.setdefault(
                    "backup_paths", [str(path) for path in backups]
                )
                raise MigrationError(str(error), details=details) from error
            finally:
                connection.close()

    def export_data(self, connection: sqlite3.Connection | None = None) -> dict[str, Any]:
        own = connection is None
        connection = connection or self.connect()
        try:
            tables = [
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
                )
            ]
            return {
                "schema_version": self.current_schema_version(connection),
                "tables": {
                    table: [dict(row) for row in connection.execute(f'SELECT * FROM "{table}" ORDER BY rowid')]
                    for table in tables
                },
            }
        finally:
            if own:
                connection.close()

    def export_json(self, *, suffix: str = "export") -> Path:
        output = self.path.with_name(f"{self.path.name}.{suffix}.json")
        temporary = output.with_name(f"{output.name}.{secrets.token_hex(8)}.tmp")
        data = json.dumps(self.export_data(), ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, "wb", closefd=False) as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        finally:
            os.close(descriptor)
        os.replace(temporary, output)
        return output

    def restore_export_data(
        self,
        export: Mapping[str, Any],
    ) -> None:
        """Restore one full-store export into an otherwise empty current store."""

        if self.read_only:
            raise StateConflict("read-only SQLite store cannot restore an export")
        if (
            not isinstance(export, Mapping)
            or set(export) != {"schema_version", "tables"}
            or export.get("schema_version") != self.target_schema_version
            or not isinstance(export.get("tables"), Mapping)
        ):
            raise RecordValidationError(
                "SQLite export does not match the current store schema"
            )
        supplied_tables = dict(export["tables"])
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            actual_tables = {
                str(row["name"])
                for row in connection.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
            }
            if set(supplied_tables) != actual_tables:
                raise RecordValidationError(
                    "SQLite export table set differs from the current schema",
                    details={
                        "missing": sorted(actual_tables - set(supplied_tables)),
                        "unexpected": sorted(
                            set(supplied_tables) - actual_tables
                        ),
                    },
                )
            expected_history = [
                {
                    "version": row["version"],
                    "name": row["name"],
                    "checksum": row["checksum"],
                }
                for row in connection.execute(
                    "SELECT version, name, checksum "
                    "FROM schema_migrations ORDER BY version"
                )
            ]
            supplied_history = [
                {
                    "version": row.get("version"),
                    "name": row.get("name"),
                    "checksum": row.get("checksum"),
                }
                for row in supplied_tables["schema_migrations"]
                if isinstance(row, Mapping)
            ]
            if supplied_history != expected_history:
                raise RecordValidationError(
                    "SQLite export migration history differs from this writer"
                )
            nonempty = {
                table: int(
                    connection.execute(
                        f'SELECT COUNT(*) FROM "{table}"'
                    ).fetchone()[0]
                )
                for table in sorted(actual_tables - {"schema_migrations"})
                if connection.execute(
                    f'SELECT COUNT(*) FROM "{table}"'
                ).fetchone()[0]
            }
            if nonempty:
                raise StateConflict(
                    "SQLite export restore requires an empty destination",
                    details={"nonempty_tables": nonempty},
                )
            connection.execute("PRAGMA defer_foreign_keys=ON")
            for table in sorted(actual_tables - {"schema_migrations"}):
                rows = supplied_tables[table]
                if not isinstance(rows, list):
                    raise RecordValidationError(
                        f"SQLite export table {table} is not a row list"
                    )
                declared_columns = [
                    str(row["name"])
                    for row in connection.execute(
                        f'PRAGMA table_info("{table}")'
                    )
                ]
                for row in rows:
                    if not isinstance(row, Mapping) or (
                        set(row) - set(declared_columns)
                    ):
                        raise RecordValidationError(
                            f"SQLite export row for {table} is malformed"
                        )
                    columns = [
                        column
                        for column in declared_columns
                        if column in row
                    ]
                    if not columns:
                        raise RecordValidationError(
                            f"SQLite export row for {table} has no columns"
                        )
                    placeholders = ", ".join("?" for _ in columns)
                    column_sql = ", ".join(
                        f'"{column}"' for column in columns
                    )
                    connection.execute(
                        f'INSERT INTO "{table}" ({column_sql}) '
                        f"VALUES ({placeholders})",
                        tuple(row[column] for column in columns),
                    )
            foreign_keys = [
                dict(row)
                for row in connection.execute("PRAGMA foreign_key_check")
            ]
            integrity = [
                row[0]
                for row in connection.execute("PRAGMA integrity_check")
            ]
            if foreign_keys or integrity != ["ok"]:
                raise IntegrityError(
                    "restored SQLite export failed integrity checks",
                    details={
                        "foreign_key_findings": foreign_keys,
                        "integrity_check": integrity,
                    },
                )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def integrity_check(self) -> dict[str, Any]:
        connection = self.connect()
        try:
            rows = [row[0] for row in connection.execute("PRAGMA integrity_check")]
            foreign_keys = [dict(row) for row in connection.execute("PRAGMA foreign_key_check")]
            return {
                "status": "pass" if rows == ["ok"] and not foreign_keys else "fail",
                "integrity": rows,
                "foreign_key_findings": foreign_keys,
                "schema_version": self.current_schema_version(connection),
            }
        finally:
            connection.close()

    def load_goal(self, goal_id: str) -> dict[str, Any]:
        connection = self.connect()
        try:
            row = connection.execute("SELECT * FROM goals WHERE goal_id=?", (goal_id,)).fetchone()
            if row is None:
                raise RecordNotFound(f"goal does not exist: {goal_id}")
            record = json.loads(row["record_json"])
            validate_goal_record(record)
            self._validate_immutable_parity(row, record)
            self._validate_deadline_parity(row, record)
            self._validate_lease_parity(connection, record)
            return record
        finally:
            connection.close()

    def list_goals(self) -> list[dict[str, Any]]:
        connection = self.connect()
        try:
            return [
                {
                    "goal_id": row["goal_id"],
                    "revision": row["state_revision"],
                    "phase": row["phase"],
                    "current_generation": row["current_generation"],
                    "passes_consumed": row["passes_consumed"],
                }
                for row in connection.execute(
                    "SELECT goal_id, state_revision, phase, current_generation, passes_consumed "
                    "FROM goals ORDER BY created_at, goal_id"
                )
            ]
        finally:
            connection.close()

    def register_topology_authorization(
        self,
        authorization: Mapping[str, Any],
        *,
        goal_id: str | None = None,
    ) -> dict[str, Any]:
        """Persist one exact, unconsumed repository-topology directive."""

        if self.read_only:
            raise StateConflict("read-only goal store cannot register authorization")
        from agentjob_runtime.execution.repository_topology import (
            validate_topology_authorization,
        )

        value = copy.deepcopy(dict(authorization))
        value = validate_topology_authorization(
            value,
            action=str(value.get("action", "")),
            command_id=str(value.get("command_id", "")),
            starting_revision=str(value.get("starting_revision", "")),
            requested_name_or_path=str(
                value.get("requested_name_or_path", "")
            ),
            require_unconsumed=True,
        )
        digest = content_sha256(value)
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            if goal_id is not None:
                exists = connection.execute(
                    "SELECT 1 FROM goals WHERE goal_id=?", (goal_id,)
                ).fetchone()
                if exists is None:
                    raise RecordNotFound(f"goal not found: {goal_id}")
            connection.execute(
                """
                INSERT INTO repository_topology_authorizations(
                    authorization_id, goal_id, action, command_id,
                    authorization_json, authorization_sha256, consumed,
                    authorized_at, consumed_at
                ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, NULL)
                """,
                (
                    value["authorization_id"],
                    goal_id,
                    value["action"],
                    value["command_id"],
                    canonical_json_bytes(value).decode("utf-8"),
                    digest,
                    value["authorized_at"],
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise StateConflict(
                "repository topology authorization identity already exists"
            ) from error
        finally:
            connection.close()
        return value

    def load_topology_authorization(
        self, authorization_id: str
    ) -> dict[str, Any]:
        connection = self.connect()
        try:
            row = connection.execute(
                """
                SELECT authorization_json
                FROM repository_topology_authorizations
                WHERE authorization_id=?
                """,
                (authorization_id,),
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            raise RecordNotFound(
                f"repository topology authorization not found: {authorization_id}"
            )
        return json.loads(row["authorization_json"])

    def consume_topology_authorization(
        self,
        authorization_id: str,
        *,
        action: str,
        command_id: str,
        starting_revision: str,
        requested_name_or_path: str,
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        """Atomically consume a registered directive using exact-operation CAS."""

        if self.read_only:
            raise StateConflict("read-only goal store cannot consume authorization")
        from agentjob_runtime.execution.repository_topology import (
            consume_topology_authorization,
            validate_topology_authorization,
        )

        consumed_at = timestamp or utc_now()
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                """
                SELECT authorization_json, authorization_sha256, consumed
                FROM repository_topology_authorizations
                WHERE authorization_id=?
                """,
                (authorization_id,),
            ).fetchone()
            if row is None:
                raise RecordNotFound(
                    f"repository topology authorization not found: {authorization_id}"
                )
            value = validate_topology_authorization(
                json.loads(row["authorization_json"]),
                action=action,
                command_id=command_id,
                starting_revision=starting_revision,
                requested_name_or_path=requested_name_or_path,
                require_unconsumed=True,
            )
            if int(row["consumed"]) != 0:
                raise StateConflict(
                    "repository topology authorization was already consumed"
                )
            consumed = consume_topology_authorization(value)
            new_digest = content_sha256(consumed)
            cursor = connection.execute(
                """
                UPDATE repository_topology_authorizations
                SET authorization_json=?, authorization_sha256=?,
                    consumed=1, consumed_at=?
                WHERE authorization_id=? AND consumed=0
                  AND authorization_sha256=?
                """,
                (
                    canonical_json_bytes(consumed).decode("utf-8"),
                    new_digest,
                    consumed_at,
                    authorization_id,
                    row["authorization_sha256"],
                ),
            )
            if cursor.rowcount != 1:
                raise StateConflict(
                    "repository topology authorization changed before consumption"
                )
            connection.commit()
            return consumed
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def consume_compiled_topology_authorization(
        self,
        authorization: Mapping[str, Any],
        *,
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        """Consume the exact compiled receipt through the durable CAS store."""

        value = dict(authorization)
        return self.consume_topology_authorization(
            str(value.get("authorization_id", "")),
            action=str(value.get("action", "")),
            command_id=str(value.get("command_id", "")),
            starting_revision=str(value.get("starting_revision", "")),
            requested_name_or_path=str(
                value.get("requested_name_or_path", "")
            ),
            timestamp=timestamp,
        )

    def create_goal(self, record: Mapping[str, Any]) -> dict[str, Any]:
        candidate = copy.deepcopy(dict(record))
        validate_goal_record(candidate)
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            self._insert_goal(connection, candidate)
            row = connection.execute(
                "SELECT * FROM goals WHERE goal_id=?", (candidate["goal_id"],)
            ).fetchone()
            self._validate_deadline_parity(row, candidate)
            self._sync_related(connection, candidate, 0, 0)
            lease = candidate["state"].get("active_lease")
            if lease:
                self._insert_initial_lease(connection, lease)
            connection.commit()
            return copy.deepcopy(candidate)
        except sqlite3.IntegrityError as error:
            connection.rollback()
            message = str(error).lower()
            if "one_active_lease" in message or "leases.repository_fingerprint" in message:
                raise ActiveRelayError("another relay owns the repository worktree") from error
            raise StateConflict(
                "goal initialization conflicts with existing state",
                details={"database_error": str(error)},
            ) from error
        except sqlite3.OperationalError as error:
            connection.rollback()
            if "locked" in str(error).lower() or "busy" in str(error).lower():
                raise StateConflict(
                    "SQLite goal state is busy with another conforming writer",
                    details={"reason_code": "state.sqlite_busy", "database_error": str(error)},
                ) from error
            raise
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @contextmanager
    def mutation(
        self,
        goal_id: str,
        *,
        expected_revision: int,
        timestamp: str | None = None,
    ) -> Iterator[GoalMutation]:
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            mutation = self._prepare_mutation(
                connection,
                goal_id,
                expected_revision=expected_revision,
                timestamp=timestamp or utc_now(),
            )
            yield mutation
            self._finalize_mutation(connection, mutation)
            connection.commit()
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise StateConflict(
                "goal state constraint rejected the transition",
                details={"database_error": str(error)},
            ) from error
        except sqlite3.OperationalError as error:
            connection.rollback()
            if "locked" in str(error).lower() or "busy" in str(error).lower():
                raise StateConflict(
                    "SQLite goal state is busy with another conforming writer",
                    details={"reason_code": "state.sqlite_busy", "database_error": str(error)},
                ) from error
            raise
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _prepare_mutation(
        self,
        connection: sqlite3.Connection,
        goal_id: str,
        *,
        expected_revision: int,
        timestamp: str,
    ) -> GoalMutation:
        """Load one revision-checked goal mutation on the caller's transaction."""

        row = connection.execute(
            "SELECT * FROM goals WHERE goal_id=?",
            (goal_id,),
        ).fetchone()
        if row is None:
            raise RecordNotFound(f"goal does not exist: {goal_id}")
        if row["state_revision"] != expected_revision:
            raise StateConflict(
                f"stale goal revision: expected {expected_revision}, "
                f"found {row['state_revision']}",
                details={
                    "expected_revision": expected_revision,
                    "actual_revision": row["state_revision"],
                },
            )
        record = json.loads(row["record_json"])
        validate_goal_record(record)
        self._validate_immutable_parity(row, record)
        self._validate_deadline_parity(row, record)
        self._validate_lease_parity(connection, record)
        return GoalMutation(
            self,
            connection,
            record,
            expected_revision,
            len(record["journal"]),
            len(record["amendments"]),
            timestamp,
        )

    def _finalize_mutation(
        self,
        connection: sqlite3.Connection,
        mutation: GoalMutation,
    ) -> None:
        """Persist a prepared goal mutation without committing its transaction."""

        record = mutation.record
        expected_revision = mutation.original_revision
        record["state"]["revision"] = expected_revision + 1
        record["updated_at"] = mutation.timestamp
        validate_goal_record(record)
        self._sync_related(
            connection,
            record,
            mutation.original_journal_length,
            mutation.original_amendment_length,
        )
        self._insert_provider_receipts(
            connection,
            record["goal_id"],
            mutation.provider_receipts,
        )
        self._insert_recovery_actions(
            connection,
            record["goal_id"],
            mutation.recovery_actions,
        )
        cursor = connection.execute(
            """
            UPDATE goals SET record_json=?, updated_at=?, deadline_at=?,
                effective_deadline_at=?, state_revision=?, phase=?, current_generation=?,
                passes_consumed=?, goal_evaluation=?, last_fingerprint=?, terminal_reason=?
            WHERE goal_id=? AND state_revision=?
            """,
            (
                canonical_json_bytes(record).decode("utf-8"),
                record["updated_at"],
                *_deadline_projections(record),
                record["state"]["revision"],
                record["state"]["phase"],
                record["state"]["current_generation"],
                record["state"]["passes_consumed"],
                record["state"]["goal_evaluation"],
                record["state"]["last_canonical_fingerprint"],
                record["state"]["terminal_reason"],
                record["goal_id"],
                expected_revision,
            ),
        )
        if cursor.rowcount != 1:
            raise StateConflict("goal revision changed during transaction")
        updated_row = connection.execute(
            "SELECT * FROM goals WHERE goal_id=?",
            (record["goal_id"],),
        ).fetchone()
        self._validate_deadline_parity(updated_row, record)
        self._validate_lease_parity(connection, record)

    def _insert_goal(self, connection: sqlite3.Connection, record: Mapping[str, Any]) -> None:
        connection.execute(
            """
            INSERT INTO goals(
                goal_id, schema_version, goal_text, goal_sha256, completion_contract_json,
                completion_contract_sha256, original_guards_json, repository_binding_json,
                repository_fingerprint, authorization_json, record_json, created_at, updated_at,
                deadline_at, effective_deadline_at, state_revision, phase, current_generation, passes_consumed,
                goal_evaluation, last_fingerprint, terminal_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["goal_id"],
                record["schema_version"],
                record["goal_text"],
                record["goal_sha256"],
                canonical_json_bytes(record["completion_contract"]).decode("utf-8"),
                record["completion_contract_sha256"],
                canonical_json_bytes(record["guards"]).decode("utf-8"),
                canonical_json_bytes(record["repository_binding"]).decode("utf-8"),
                repository_identity_hash(record["repository_binding"]),
                canonical_json_bytes(record["authorization"]).decode("utf-8"),
                canonical_json_bytes(record).decode("utf-8"),
                record["created_at"],
                record["updated_at"],
                *_deadline_projections(record),
                record["state"]["revision"],
                record["state"]["phase"],
                record["state"]["current_generation"],
                record["state"]["passes_consumed"],
                record["state"]["goal_evaluation"],
                record["state"]["last_canonical_fingerprint"],
                record["state"]["terminal_reason"],
            ),
        )

    @staticmethod
    def _insert_initial_lease(connection: sqlite3.Connection, lease: Mapping[str, Any]) -> None:
        connection.execute(
            """
            INSERT INTO leases(
                repository_fingerprint, goal_id, generation, holder_kind, holder_token,
                transaction_id, acquired_at, heartbeat_at, expires_at, lease_state
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
            """,
            tuple(
                lease[key]
                for key in (
                    "repository_fingerprint",
                    "goal_id",
                    "generation",
                    "holder_kind",
                    "holder_token",
                    "transaction_id",
                    "acquired_at",
                    "heartbeat_at",
                    "expires_at",
                )
            ),
        )

    def _sync_related(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        original_journal_length: int,
        original_amendment_length: int,
    ) -> None:
        goal_id = record["goal_id"]
        for sequence, amendment in enumerate(
            record["amendments"][original_amendment_length:], original_amendment_length + 1
        ):
            connection.execute(
                """
                INSERT INTO goal_amendments(
                    goal_id, sequence, kind, user_authorization, prior_effective_sha256,
                    new_value_json, new_sha256, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    goal_id,
                    sequence,
                    amendment["kind"],
                    amendment["user_authorization"],
                    amendment["prior_effective_sha256"],
                    canonical_json_bytes(amendment["new_value"]).decode("utf-8"),
                    amendment["new_sha256"],
                    amendment["created_at"],
                ),
            )
        for generation in record["generations"].values():
            handoff = (
                record["handoff"]
                if record["handoff"].get("generation") == generation["generation"]
                else {}
            )
            self._sync_generation(connection, goal_id, generation, record["updated_at"], handoff)
        self._sync_v3_records(connection, record)
        self._sync_v4_records(connection, record)
        history = record["state"]["canonical_fingerprint_history"]
        for sequence, fingerprint in enumerate(history):
            row = connection.execute(
                "SELECT fingerprint FROM fingerprints WHERE goal_id=? AND sequence=?",
                (goal_id, sequence),
            ).fetchone()
            if row is None:
                classification = (
                    "initial"
                    if sequence == 0
                    else next(
                        (
                            str(generation["fingerprint_status"])
                            for generation in record[
                                "generations"
                            ].values()
                            if generation.get("after_fingerprint")
                            == fingerprint
                            and generation.get("fingerprint_status")
                            is not None
                        ),
                        "new",
                    )
                )
                connection.execute(
                    "INSERT INTO fingerprints(goal_id, sequence, fingerprint, classification, payload_json) "
                    "VALUES (?, ?, ?, ?, NULL)",
                    (goal_id, sequence, fingerprint, classification),
                )
            elif row["fingerprint"] != fingerprint:
                raise IntegrityError("fingerprint history is immutable")
        for entry in record["journal"][original_journal_length:]:
            timestamp = str(entry["payload"].get("timestamp", record["updated_at"]))
            connection.execute(
                """
                INSERT INTO events(goal_id, sequence, kind, payload_json, prior_hash, event_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    goal_id,
                    entry["sequence"],
                    entry["kind"],
                    canonical_json_bytes(entry["payload"]).decode("utf-8"),
                    entry["prior_hash"],
                    entry["entry_hash"],
                    timestamp,
                ),
            )
            if entry["kind"] == "step_receipt":
                payload = entry["payload"]
                connection.execute(
                    """
                    INSERT INTO step_receipts(
                        goal_id, generation, receipt_kind, payload_json, receipt_hash, finalized_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        goal_id,
                        payload["generation"],
                        payload["decision"],
                        canonical_json_bytes(payload).decode("utf-8"),
                        entry["entry_hash"],
                        payload["finished_at"],
                    ),
                )

    @staticmethod
    def _sync_generation(
        connection: sqlite3.Connection,
        goal_id: str,
        generation: Mapping[str, Any],
        updated_at: str,
        handoff: Mapping[str, Any],
    ) -> None:
        existing = connection.execute(
            "SELECT handoff_token, idempotency_key, before_fingerprint FROM generations "
            "WHERE goal_id=? AND generation=?",
            (goal_id, generation["generation"]),
        ).fetchone()
        immutable = (
            generation["handoff_token"],
            generation["idempotency_key"],
            generation["before_fingerprint"],
        )
        values = (
            generation["phase"],
            generation["lease_token"],
            int(generation["invocation_consumed"]),
            generation["invocation_state"],
            generation["consumed_at"],
            generation["returned_at"],
            generation["after_fingerprint"],
            generation.get("fingerprint_status"),
            json.dumps(generation["pending_step_result"], sort_keys=True, ensure_ascii=False)
            if generation["pending_step_result"] is not None
            else None,
            generation["finalized_receipt_hash"],
            generation["terminal_or_successor_outcome"],
            generation["claimed_at"],
            generation["successor_thread_id"],
            generation.get("requested_reasoning_effort"),
            generation.get("effective_reasoning_effort"),
            canonical_json_bytes(generation["profile_evidence"]).decode("utf-8")
            if generation.get("profile_evidence") is not None
            else None,
            generation.get("environment_mode"),
            canonical_json_bytes(
                generation["observed_repository_topology"]
            ).decode("utf-8")
            if generation.get("observed_repository_topology") is not None
            else None,
            canonical_json_bytes(generation["resolution_disposition"]).decode(
                "utf-8"
            )
            if generation.get("resolution_disposition") is not None
            else None,
            generation.get("repair_strategy_id"),
            int(generation.get("strategy_attempt", 0)),
            canonical_json_bytes(
                generation.get("material_progress_dimensions", [])
            ).decode("utf-8")
            if "material_progress_dimensions" in generation
            else None,
            generation.get("human_necessity_report_ref"),
            generation.get("completion_report_ref"),
        )
        generation_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(generations)")
        }
        v3_columns_available = (
            "requested_reasoning_effort" in generation_columns
        )
        if existing is None:
            if v3_columns_available:
                connection.execute(
                    """
                    INSERT INTO generations(
                        goal_id, generation, handoff_token, idempotency_key, phase, lease_token,
                        invocation_consumed, invocation_state, consumed_at, returned_at,
                        before_fingerprint, after_fingerprint, fingerprint_status,
                        pending_step_result_json, finalized_receipt_hash,
                        terminal_or_successor_outcome, claimed_at, successor_thread_id,
                        requested_reasoning_effort, effective_reasoning_effort,
                        profile_evidence_json, environment_mode,
                        observed_repository_topology_json, resolution_disposition_json,
                        repair_strategy_id, strategy_attempt,
                        material_progress_dimensions_json, human_necessity_report_ref,
                        completion_report_ref
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        goal_id,
                        generation["generation"],
                        *immutable[:2],
                        values[0],
                        values[1],
                        values[2],
                        values[3],
                        values[4],
                        values[5],
                        immutable[2],
                        *values[6:],
                    ),
                )
            else:
                connection.execute(
                    """
                    INSERT INTO generations(
                        goal_id, generation, handoff_token, idempotency_key,
                        phase, lease_token, invocation_consumed,
                        invocation_state, consumed_at, returned_at,
                        before_fingerprint, after_fingerprint,
                        fingerprint_status, pending_step_result_json,
                        finalized_receipt_hash, terminal_or_successor_outcome,
                        claimed_at, successor_thread_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        goal_id,
                        generation["generation"],
                        *immutable[:2],
                        values[0],
                        values[1],
                        values[2],
                        values[3],
                        values[4],
                        values[5],
                        immutable[2],
                        *values[6:13],
                    ),
                )
        else:
            if tuple(existing) != immutable:
                raise IntegrityError("generation identity fields are immutable")
            if v3_columns_available:
                connection.execute(
                    """
                    UPDATE generations SET
                        phase=?, lease_token=?, invocation_consumed=?, invocation_state=?,
                        consumed_at=?, returned_at=?, after_fingerprint=?, fingerprint_status=?,
                        pending_step_result_json=?, finalized_receipt_hash=?,
                        terminal_or_successor_outcome=?, claimed_at=?, successor_thread_id=?,
                        requested_reasoning_effort=?, effective_reasoning_effort=?,
                        profile_evidence_json=?, environment_mode=?,
                        observed_repository_topology_json=?, resolution_disposition_json=?,
                        repair_strategy_id=?, strategy_attempt=?,
                        material_progress_dimensions_json=?,
                        human_necessity_report_ref=?, completion_report_ref=?
                    WHERE goal_id=? AND generation=?
                    """,
                    (*values, goal_id, generation["generation"]),
                )
            else:
                connection.execute(
                    """
                    UPDATE generations SET
                        phase=?, lease_token=?, invocation_consumed=?,
                        invocation_state=?, consumed_at=?, returned_at=?,
                        after_fingerprint=?, fingerprint_status=?,
                        pending_step_result_json=?, finalized_receipt_hash=?,
                        terminal_or_successor_outcome=?, claimed_at=?,
                        successor_thread_id=?
                    WHERE goal_id=? AND generation=?
                    """,
                    (*values[:13], goal_id, generation["generation"]),
                )
        intent = connection.execute(
            "SELECT handoff_token, idempotency_key, successor_thread_id FROM successor_intents "
            "WHERE goal_id=? AND generation=?",
            (goal_id, generation["generation"]),
        ).fetchone()
        provider_state = "returned" if generation["successor_thread_id"] else "intent"
        if generation["terminal_or_successor_outcome"] in {
            "ambiguous",
            "failed",
            "timeout",
            "duplicate",
        }:
            provider_state = generation["terminal_or_successor_outcome"]
        if intent is None:
            connection.execute(
                """
                INSERT INTO successor_intents(
                    goal_id, generation, handoff_token, idempotency_key,
                    predecessor_thread_id, successor_thread_id, provider_state, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    goal_id,
                    generation["generation"],
                    generation["handoff_token"],
                    generation["idempotency_key"],
                    handoff.get("predecessor_thread_id"),
                    generation["successor_thread_id"],
                    provider_state,
                    updated_at,
                    updated_at,
                ),
            )
        else:
            if (
                intent["handoff_token"] != generation["handoff_token"]
                or intent["idempotency_key"] != generation["idempotency_key"]
                or intent["successor_thread_id"]
                not in (None, generation["successor_thread_id"])
            ):
                raise IntegrityError("successor intent identity is immutable")
            connection.execute(
                "UPDATE successor_intents SET successor_thread_id=?, provider_state=?, updated_at=? "
                "WHERE goal_id=? AND generation=?",
                (
                    generation["successor_thread_id"],
                    provider_state,
                    updated_at,
                    goal_id,
                    generation["generation"],
                ),
            )

    @staticmethod
    def _sync_v3_records(
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> None:
        if record.get("schema_version") not in {
            "sys4ai.continue-goal.v3",
            "sys4ai.continue-goal.v4",
        }:
            return
        goal_id = str(record["goal_id"])
        activation = record["activation"]
        activation_hash = content_sha256(activation)
        existing_activation = connection.execute(
            "SELECT receipt_sha256 FROM goal_activation_receipts WHERE goal_id=?",
            (goal_id,),
        ).fetchone()
        if existing_activation is None:
            connection.execute(
                """
                INSERT INTO goal_activation_receipts(
                    goal_id, activation_id, receipt_json, receipt_sha256, accepted_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    goal_id,
                    activation["activation_id"],
                    canonical_json_bytes(activation).decode("utf-8"),
                    activation_hash,
                    activation["accepted_at"],
                ),
            )
        elif existing_activation["receipt_sha256"] != activation_hash:
            raise IntegrityError("activation receipt is immutable")

        for sequence, disposition in enumerate(
            record["resolution_history"], 1
        ):
            disposition_hash = content_sha256(disposition)
            existing = connection.execute(
                "SELECT disposition_sha256 FROM goal_resolution_strategies "
                "WHERE goal_id=? AND sequence=?",
                (goal_id, sequence),
            ).fetchone()
            generation = next(
                (
                    int(key)
                    for key, item in record["generations"].items()
                    if item.get("resolution_disposition") == disposition
                ),
                int(record["state"]["current_generation"]),
            )
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO goal_resolution_strategies(
                        goal_id, sequence, generation, blocker_signature,
                        strategy_id, attempt, disposition_json, disposition_sha256
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        goal_id,
                        sequence,
                        generation,
                        disposition["blocker_signature"],
                        disposition["selected_strategy_id"],
                        disposition["strategy_attempt"],
                        canonical_json_bytes(disposition).decode("utf-8"),
                        disposition_hash,
                    ),
                )
            elif existing["disposition_sha256"] != disposition_hash:
                raise IntegrityError("resolution history is immutable")

        human = record.get("human_intervention")
        if human is not None:
            human_hash = content_sha256(human)
            existing = connection.execute(
                "SELECT report_sha256 FROM goal_human_necessity_reports WHERE goal_id=?",
                (goal_id,),
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO goal_human_necessity_reports(
                        goal_id, report_id, report_json, report_sha256, created_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        goal_id,
                        human["report_id"],
                        canonical_json_bytes(human).decode("utf-8"),
                        human_hash,
                        human["created_at"],
                    ),
                )
            elif existing["report_sha256"] != human_hash:
                raise IntegrityError("human-necessity report is immutable")

        completion = record.get("completion_report")
        if completion is not None:
            completion_hash = content_sha256(completion)
            existing = connection.execute(
                "SELECT report_sha256 FROM goal_completion_reports WHERE goal_id=?",
                (goal_id,),
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO goal_completion_reports(
                        goal_id, report_id, report_json, report_sha256, completed_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        goal_id,
                        completion["report_id"],
                        canonical_json_bytes(completion).decode("utf-8"),
                        completion_hash,
                        completion["completed_at"],
                    ),
                )
            elif existing["report_sha256"] != completion_hash:
                raise IntegrityError("goal completion report is immutable")

    @staticmethod
    def _sync_v4_records(
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> None:
        if record.get("schema_version") != "sys4ai.continue-goal.v4":
            return
        goal_id = str(record["goal_id"])
        immutable_records = (
            (
                "goal_question_batches",
                "batch_id",
                record["question_batch"]["batch_id"],
                "batch_json",
                record["question_batch"],
                "batch_sha256",
                content_sha256(record["question_batch"]),
                "created_at",
                record["question_batch"]["created_at"],
            ),
            (
                "goal_execution_authorities",
                "authority_id",
                record["execution_authority"]["authority_id"],
                "authority_json",
                record["execution_authority"],
                "authority_sha256",
                content_sha256(record["execution_authority"]),
                "created_at",
                record["execution_authority"]["created_at"],
            ),
            (
                "goal_question_responses",
                "response_id",
                record["question_response"]["response_id"],
                "response_json",
                record["question_response"],
                "response_sha256",
                content_sha256(record["question_response"]),
                "answered_at",
                record["question_response"]["answered_at"],
            ),
        )
        for (
            table,
            id_column,
            record_id,
            json_column,
            value,
            hash_column,
            digest,
            time_column,
            timestamp,
        ) in immutable_records:
            existing = connection.execute(
                f"SELECT {hash_column} FROM {table} WHERE {id_column}=?",
                (record_id,),
            ).fetchone()
            if existing is None:
                columns = [
                    id_column,
                    "goal_id",
                    json_column,
                    hash_column,
                    time_column,
                ]
                values: list[Any] = [
                    record_id,
                    goal_id,
                    canonical_json_bytes(value).decode("utf-8"),
                    digest,
                    timestamp,
                ]
                if table == "goal_question_responses":
                    columns.insert(2, "batch_id")
                    values.insert(2, record["question_response"]["batch_id"])
                connection.execute(
                    f"INSERT INTO {table}({', '.join(columns)}) "
                    f"VALUES ({', '.join('?' for _ in columns)})",
                    tuple(values),
                )
            elif existing[hash_column] != digest:
                raise IntegrityError(f"{table} immutable record changed")
        for consumption in record["grant_consumptions"]:
            digest = content_sha256(consumption)
            existing = connection.execute(
                "SELECT consumption_sha256 FROM goal_grant_consumptions "
                "WHERE consumption_id=?",
                (consumption["consumption_id"],),
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO goal_grant_consumptions(
                        consumption_id, goal_id, generation, grant_id,
                        action_sha256, consumption_json, consumption_sha256,
                        consumed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        consumption["consumption_id"],
                        goal_id,
                        consumption["generation"],
                        consumption["grant_id"],
                        consumption["action_sha256"],
                        canonical_json_bytes(consumption).decode("utf-8"),
                        digest,
                        consumption["consumed_at"],
                    ),
                )
            elif existing["consumption_sha256"] != digest:
                raise IntegrityError("goal grant consumption changed")
        coordinator = record["coordinator"]
        existing_coordinator = connection.execute(
            "SELECT coordinator_thread_id FROM goal_coordinator_states "
            "WHERE goal_id=?",
            (goal_id,),
        ).fetchone()
        if existing_coordinator is not None and (
            existing_coordinator["coordinator_thread_id"]
            != coordinator["thread_id"]
        ):
            raise IntegrityError("goal coordinator identity is immutable")
        connection.execute(
            """
            INSERT INTO goal_coordinator_states(
                goal_id, coordinator_thread_id, status, state_json, updated_at
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(goal_id) DO UPDATE SET
                status=excluded.status,
                state_json=excluded.state_json,
                updated_at=excluded.updated_at
            """,
            (
                goal_id,
                coordinator["thread_id"],
                coordinator["status"],
                canonical_json_bytes(coordinator).decode("utf-8"),
                coordinator["updated_at"],
            ),
        )
    @staticmethod
    def _insert_provider_receipts(
        connection: sqlite3.Connection,
        goal_id: str,
        receipts: Sequence[Mapping[str, Any]],
    ) -> None:
        for receipt in receipts:
            connection.execute(
                """
                INSERT INTO provider_receipts(
                    goal_id, generation, provider_id, idempotency_key, provider_status,
                    returned_thread_id, response_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    goal_id,
                    receipt["generation"],
                    receipt["provider_id"],
                    receipt["idempotency_key"],
                    receipt["provider_status"],
                    receipt["returned_thread_id"],
                    canonical_json_bytes(receipt["response"]).decode("utf-8"),
                    receipt["created_at"],
                ),
            )

    @staticmethod
    def _insert_recovery_actions(
        connection: sqlite3.Connection,
        goal_id: str,
        actions: Sequence[Mapping[str, Any]],
    ) -> None:
        current = connection.execute(
            "SELECT COUNT(*) FROM recovery_actions WHERE goal_id=?", (goal_id,)
        ).fetchone()[0]
        for offset, action in enumerate(actions, 1):
            connection.execute(
                """
                INSERT INTO recovery_actions(
                    goal_id, sequence, action, user_authorization, evidence_json,
                    prior_phase, resulting_phase, action_hash, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    goal_id,
                    current + offset,
                    action["recovery_action"],
                    action["user_authorization"],
                    canonical_json_bytes(action["evidence"]).decode("utf-8"),
                    action["prior_phase"],
                    action["resulting_phase"],
                    action["action_hash"],
                    action["timestamp"],
                ),
            )

    @staticmethod
    def _validate_immutable_parity(row: sqlite3.Row, record: Mapping[str, Any]) -> None:
        expected = {
            "goal_text": record["goal_text"],
            "goal_sha256": record["goal_sha256"],
            "completion_contract_json": canonical_json_bytes(record["completion_contract"]).decode("utf-8"),
            "completion_contract_sha256": record["completion_contract_sha256"],
            "original_guards_json": canonical_json_bytes(record["guards"]).decode("utf-8"),
            "repository_binding_json": canonical_json_bytes(record["repository_binding"]).decode("utf-8"),
            "repository_fingerprint": repository_identity_hash(record["repository_binding"]),
            "authorization_json": canonical_json_bytes(record["authorization"]).decode("utf-8"),
            "created_at": record["created_at"],
        }
        for key, value in expected.items():
            if row[key] != value:
                raise IntegrityError(f"normalized immutable goal field disagrees with record: {key}")

    @staticmethod
    def _validate_deadline_parity(row: sqlite3.Row, record: Mapping[str, Any]) -> None:
        legacy, effective = _deadline_projections(record)
        if row["deadline_at"] != legacy:
            raise IntegrityError("normalized legacy deadline disagrees with record")
        if "effective_deadline_at" in row.keys() and row["effective_deadline_at"] != effective:
            raise IntegrityError("normalized effective deadline disagrees with record")

    @staticmethod
    def _validate_lease_parity(
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> None:
        row = connection.execute(
            "SELECT * FROM leases WHERE goal_id=? AND lease_state='active'",
            (record["goal_id"],),
        ).fetchone()
        lease = record["state"].get("active_lease")
        if lease is None and row is None:
            return
        if lease is None or row is None:
            raise IntegrityError("goal and database lease state disagree")
        for key in (
            "repository_fingerprint",
            "goal_id",
            "generation",
            "holder_kind",
            "holder_token",
            "transaction_id",
            "acquired_at",
            "heartbeat_at",
            "expires_at",
        ):
            if lease[key] != row[key]:
                raise IntegrityError(f"goal and database lease disagree on {key}")

    def query_one(self, sql: str, parameters: Sequence[Any] = ()) -> dict[str, Any] | None:
        connection = self.connect()
        try:
            row = connection.execute(sql, parameters).fetchone()
            return dict(row) if row else None
        finally:
            connection.close()

    def with_connection(self, operation: Callable[[sqlite3.Connection], Any]) -> Any:
        connection = self.connect()
        try:
            return operation(connection)
        finally:
            connection.close()
