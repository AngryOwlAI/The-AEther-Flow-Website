"""SQLite-backed goal state, transactional migrations, and normalized constraints."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import secrets
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Sequence

from agentjob_runtime.errors import (
    ActiveRelayError,
    IntegrityError,
    MigrationError,
    RecordNotFound,
    StateConflict,
)
from agentjob_runtime.goal.model import (
    append_journal,
    repository_identity_hash,
    utc_now,
    validate_goal_record,
)
from agentjob_runtime.records.canonical import canonical_json_bytes, content_sha256


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
    ) -> None:
        self.path = Path(database_path).expanduser().resolve(strict=False)
        self.read_only = read_only
        if not read_only:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.parent.is_symlink():
            raise IntegrityError("SQLite state directory may not be a symlink")
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
                f"{self.path.as_uri()}?mode=ro&immutable=1",
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

    def apply_migrations(self, migrations: Sequence[Migration] | None = None) -> list[Path]:
        planned = list(migrations or self.migrations())
        backups: list[Path] = []
        connection = self.connect()
        try:
            current = self.current_schema_version(connection)
            for migration in planned:
                if migration.version <= current:
                    if self._table_exists(connection, "schema_migrations"):
                        row = connection.execute(
                            "SELECT name, checksum FROM schema_migrations WHERE version=?",
                            (migration.version,),
                        ).fetchone()
                        if row and (row["name"] != migration.name or row["checksum"] != migration.checksum):
                            raise MigrationError(
                                f"migration {migration.version} does not match applied checksum"
                            )
                    continue
                if migration.version != current + 1:
                    raise MigrationError(
                        f"migration sequence gap: current={current}, next={migration.version}"
                    )
                if current:
                    backups.append(self.export_json(suffix=f"pre-migration-v{current}"))
                applied_at = utc_now()
                escaped_name = migration.name.replace("'", "''")
                escaped_checksum = migration.checksum
                escaped_applied = applied_at
                script = (
                    "BEGIN IMMEDIATE;\n"
                    + migration.sql
                    + "\nINSERT INTO schema_migrations(version, name, checksum, applied_at) "
                    + f"VALUES ({migration.version}, '{escaped_name}', '{escaped_checksum}', '{escaped_applied}');\n"
                    + "COMMIT;"
                )
                try:
                    connection.executescript(script)
                except sqlite3.Error as error:
                    try:
                        connection.execute("ROLLBACK")
                    except sqlite3.Error:
                        pass
                    raise MigrationError(
                        f"migration {migration.version} ({migration.name}) failed",
                        details={"database": str(self.path), "backup_paths": [str(path) for path in backups]},
                    ) from error
                current = migration.version
            return backups
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

    def create_goal(self, record: Mapping[str, Any]) -> dict[str, Any]:
        candidate = copy.deepcopy(dict(record))
        validate_goal_record(candidate)
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            self._insert_goal(connection, candidate)
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
            row = connection.execute("SELECT * FROM goals WHERE goal_id=?", (goal_id,)).fetchone()
            if row is None:
                raise RecordNotFound(f"goal does not exist: {goal_id}")
            if row["state_revision"] != expected_revision:
                raise StateConflict(
                    f"stale goal revision: expected {expected_revision}, found {row['state_revision']}",
                    details={"expected_revision": expected_revision, "actual_revision": row["state_revision"]},
                )
            record = json.loads(row["record_json"])
            validate_goal_record(record)
            self._validate_immutable_parity(row, record)
            self._validate_lease_parity(connection, record)
            mutation = GoalMutation(
                self,
                connection,
                record,
                expected_revision,
                len(record["journal"]),
                len(record["amendments"]),
                timestamp or utc_now(),
            )
            yield mutation
            record["state"]["revision"] = expected_revision + 1
            record["updated_at"] = mutation.timestamp
            validate_goal_record(record)
            self._sync_related(
                connection,
                record,
                mutation.original_journal_length,
                mutation.original_amendment_length,
            )
            self._insert_provider_receipts(connection, record["goal_id"], mutation.provider_receipts)
            self._insert_recovery_actions(connection, record["goal_id"], mutation.recovery_actions)
            cursor = connection.execute(
                """
                UPDATE goals SET record_json=?, updated_at=?, deadline_at=?, state_revision=?, phase=?,
                    current_generation=?, passes_consumed=?, goal_evaluation=?, last_fingerprint=?, terminal_reason=?
                WHERE goal_id=? AND state_revision=?
                """,
                (
                    canonical_json_bytes(record).decode("utf-8"),
                    record["updated_at"],
                    record["deadline_at"],
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
            self._validate_lease_parity(connection, record)
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

    def _insert_goal(self, connection: sqlite3.Connection, record: Mapping[str, Any]) -> None:
        connection.execute(
            """
            INSERT INTO goals(
                goal_id, schema_version, goal_text, goal_sha256, completion_contract_json,
                completion_contract_sha256, original_guards_json, repository_binding_json,
                repository_fingerprint, authorization_json, record_json, created_at, updated_at,
                deadline_at, state_revision, phase, current_generation, passes_consumed,
                goal_evaluation, last_fingerprint, terminal_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                record["deadline_at"],
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
        history = record["state"]["canonical_fingerprint_history"]
        for sequence, fingerprint in enumerate(history):
            row = connection.execute(
                "SELECT fingerprint FROM fingerprints WHERE goal_id=? AND sequence=?",
                (goal_id, sequence),
            ).fetchone()
            if row is None:
                classification = "initial" if sequence == 0 else record["generations"].get(
                    str(sequence), {}
                ).get("fingerprint_status", "new")
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
        )
        if existing is None:
            connection.execute(
                """
                INSERT INTO generations(
                    goal_id, generation, handoff_token, idempotency_key, phase, lease_token,
                    invocation_consumed, invocation_state, consumed_at, returned_at,
                    before_fingerprint, after_fingerprint, fingerprint_status,
                    pending_step_result_json, finalized_receipt_hash,
                    terminal_or_successor_outcome, claimed_at, successor_thread_id
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
                    *values[6:],
                ),
            )
        else:
            if tuple(existing) != immutable:
                raise IntegrityError("generation identity fields are immutable")
            connection.execute(
                """
                UPDATE generations SET
                    phase=?, lease_token=?, invocation_consumed=?, invocation_state=?,
                    consumed_at=?, returned_at=?, after_fingerprint=?, fingerprint_status=?,
                    pending_step_result_json=?, finalized_receipt_hash=?,
                    terminal_or_successor_outcome=?, claimed_at=?, successor_thread_id=?
                WHERE goal_id=? AND generation=?
                """,
                (*values, goal_id, generation["generation"]),
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
                or intent["successor_thread_id"] not in (None, generation["successor_thread_id"])
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
