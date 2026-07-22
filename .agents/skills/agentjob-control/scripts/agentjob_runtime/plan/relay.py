"""Plan-native recursive discussion relay.

This module is intentionally independent from the generic-goal runtime. New
recursive runs have one SQLite authority, one transferable repository lease,
one task per generation, and no coordinator wake/resume path.
"""

from __future__ import annotations

import copy
import hashlib
import json
import secrets
import sqlite3
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from agentjob_runtime.errors import IntegrityError, RecordNotFound, RecordValidationError, StateConflict
from agentjob_runtime.state_utils import (
    canonical_json_bytes,
    connect_sqlite,
    content_sha256,
    file_sha256,
    immediate_transaction,
    parse_utc,
    sqlite_backup,
    utc_now,
)


SCHEMA_VERSION = "sys4ai.implementation-plan-relay.sqlite.v1"
PROFILE = "recursive_chain_v1"
TOPOLOGY = "recursive_chain_v1"
ACCEPTANCE_SCHEMA = "sys4ai.plan-relay-acceptance.v1"
EXPORT_SCHEMA = "sys4ai.implementation-plan-relay.export.v1"
TERMINAL_RUN_STATUSES = frozenset({"plan_complete", "cancelled"})
PROTECTED_RUN_STATUSES = frozenset(
    {
        "human_gate",
        "integrity_stop",
        "validation_failed",
        "capability_blocked",
        "invocation_unknown",
    }
)
ACTIVE_GENERATION_STATUSES = frozenset(
    {
        "dispatch_pending",
        "reserved",
        "claimed",
        "consumed",
        "returned",
        "receipt_finalized",
        "successor_reserved",
    }
)


class RelayConflict(StateConflict):
    code = "plan_relay.state_conflict"


class RelayIntegrityError(IntegrityError):
    code = "plan_relay.integrity_failed"


def _require_nonblank(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecordValidationError(f"{field} must be a nonblank string")
    return value


def _token_sha256(token: str) -> str:
    _require_nonblank(token, "token")
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _json(value: Any) -> str:
    return canonical_json_bytes(value).decode("utf-8")


def _loads(value: str | None) -> Any:
    return None if value is None else json.loads(value)


def _row(row: sqlite3.Row | None, label: str) -> sqlite3.Row:
    if row is None:
        raise RecordNotFound(f"{label} was not found")
    return row


def _task_hash(task: Mapping[str, Any]) -> str:
    basis = copy.deepcopy(dict(task))
    supplied = task.get("task_sha256")
    basis.pop("task_sha256", None)
    calculated = content_sha256(basis)
    if supplied is None:
        return calculated
    if not isinstance(supplied, str) or len(supplied) != 64 or supplied != calculated:
        raise RecordValidationError(
            "task_sha256 does not match the canonical task body",
            details={
                "reason_code": "relay.task_hash_mismatch",
                "task_id": task.get("task_id"),
                "expected": calculated,
                "actual": supplied,
            },
        )
    return supplied


def validate_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(dict(plan))
    plan_id = _require_nonblank(candidate.get("plan_id"), "plan_id")
    tasks = candidate.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise RecordValidationError("plan.tasks must be a nonempty array")
    known: set[str] = set()
    for index, task in enumerate(tasks):
        if not isinstance(task, Mapping):
            raise RecordValidationError(f"plan.tasks[{index}] must be an object")
        task_id = _require_nonblank(task.get("task_id"), f"plan.tasks[{index}].task_id")
        if task_id in known:
            raise RecordValidationError(f"duplicate task_id: {task_id}")
        known.add(task_id)
        _task_hash(task)
        dependencies = task.get("depends_on", [])
        if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
            raise RecordValidationError(f"task {task_id} dependencies must be string IDs")
    for task in tasks:
        task_id = str(task["task_id"])
        dependencies = list(task.get("depends_on", []))
        if task_id in dependencies:
            raise RecordValidationError(f"task {task_id} depends on itself")
        unknown = sorted(set(dependencies) - known)
        if unknown:
            raise RecordValidationError(f"task {task_id} has unknown dependencies: {unknown}")
    visiting: set[str] = set()
    visited: set[str] = set()
    by_id = {str(task["task_id"]): task for task in tasks}

    def visit(task_id: str) -> None:
        if task_id in visiting:
            raise RecordValidationError(f"task dependency cycle includes {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in by_id[task_id].get("depends_on", []):
            visit(str(dependency))
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in by_id:
        visit(task_id)
    _require_nonblank(plan_id, "plan_id")
    canonical_json_bytes(candidate)
    return candidate


def _effective_plan_revision(plan: Mapping[str, Any]) -> int:
    value = plan.get("effective_plan_revision", plan.get("revision", 1))
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise RecordValidationError(
            "effective plan revision must be a positive integer",
            details={"reason_code": "relay.plan_revision_invalid"},
        )
    return value


def build_acceptance_basis(
    *,
    plan: Mapping[str, Any],
    repository_binding: Mapping[str, Any],
    repository_fingerprint: str,
    control_fingerprint: str,
    launcher_thread_id: str,
    requested_effort: str,
    effective_effort: str,
    authority_manifest: Mapping[str, Any],
    protected_effect_grants: Mapping[str, Any],
    profile: str = PROFILE,
    topology: str = TOPOLOGY,
) -> dict[str, Any]:
    """Build the immutable values that an acceptance must bind exactly."""

    canonical_plan = validate_plan(plan)
    canonical_json_bytes(repository_binding)
    canonical_json_bytes(authority_manifest)
    canonical_json_bytes(protected_effect_grants)
    repository_identity = _require_nonblank(
        repository_fingerprint, "repository_fingerprint"
    )
    control_identity = _require_nonblank(
        control_fingerprint, "control_fingerprint"
    )
    launcher_identity = _require_nonblank(
        launcher_thread_id, "launcher_thread_id"
    )
    requested = _require_nonblank(requested_effort, "requested_effort")
    effective = _require_nonblank(effective_effort, "effective_effort")
    if profile != PROFILE or topology != TOPOLOGY:
        raise RecordValidationError(
            "acceptance basis selects a legacy or mixed relay profile",
            details={"reason_code": "relay.profile_refused"},
        )
    graph = [
        {
            "task_id": str(task["task_id"]),
            "task_sha256": _task_hash(task),
            "depends_on": [str(item) for item in task.get("depends_on", [])],
        }
        for task in canonical_plan["tasks"]
    ]
    objective = canonical_plan.get("objective", "")
    if not isinstance(objective, str):
        raise RecordValidationError(
            "plan objective must be a string when present",
            details={"reason_code": "relay.objective_invalid"},
        )
    reasoning_profile = {
        "requested_effort": requested,
        "effective_effort": effective,
    }
    return {
        "schema_version": ACCEPTANCE_SCHEMA,
        "plan_id": str(canonical_plan["plan_id"]),
        "plan_sha256": content_sha256(canonical_plan),
        "accepted_objective_sha256": content_sha256(
            {"plan_id": canonical_plan["plan_id"], "objective": objective}
        ),
        "effective_plan_revision": _effective_plan_revision(canonical_plan),
        "task_graph_sha256": content_sha256(graph),
        "repository_binding_sha256": content_sha256(repository_binding),
        "repository_fingerprint": repository_identity,
        "control_fingerprint": control_identity,
        "launcher_thread_id": launcher_identity,
        "requested_effort": requested,
        "effective_effort": effective,
        "reasoning_profile_sha256": content_sha256(reasoning_profile),
        "authority_manifest_sha256": content_sha256(authority_manifest),
        "protected_effect_grants_sha256": content_sha256(
            protected_effect_grants
        ),
        "relay_profile": profile,
        "relay_topology": topology,
    }


def validate_acceptance(
    acceptance: Mapping[str, Any],
    *,
    basis: Mapping[str, Any],
) -> dict[str, Any]:
    """Reject incomplete, stale, or differently scoped combined acceptance."""

    if not isinstance(acceptance, Mapping):
        raise RecordValidationError(
            "relay acceptance must be an object",
            details={"reason_code": "relay.acceptance_stale"},
        )
    candidate = copy.deepcopy(dict(acceptance))
    expected_keys = set(basis) | {"accepted", "acceptance_evidence_ref"}
    mismatches: list[str] = []
    if set(candidate) != expected_keys:
        mismatches.extend(sorted(expected_keys ^ set(candidate)))
    if candidate.get("accepted") is not True:
        mismatches.append("accepted")
    try:
        _require_nonblank(
            candidate.get("acceptance_evidence_ref"),
            "acceptance_evidence_ref",
        )
    except RecordValidationError:
        mismatches.append("acceptance_evidence_ref")
    for field, expected in basis.items():
        if candidate.get(field) != expected:
            mismatches.append(field)
    if mismatches:
        raise RecordValidationError(
            "combined relay acceptance is missing, stale, or identity-mismatched",
            details={
                "reason_code": "relay.acceptance_stale",
                "fields": sorted(set(mismatches)),
            },
        )
    canonical_json_bytes(candidate)
    return candidate


class RelayStore:
    """Transactional authority for one or more recursive relay runs."""

    def __init__(self, database_path: str | Path):
        self.path = Path(database_path).resolve()
        self.migration_path = Path(__file__).with_name("migrations") / "001_plan_native_relay.sql"

    def bootstrap(self) -> dict[str, Any]:
        existed = self.path.exists()
        with connect_sqlite(self.path) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            if not tables:
                sql = self.migration_path.read_text(encoding="utf-8")
                connection.executescript(sql)
                timestamp = utc_now()
                connection.execute(
                    "INSERT INTO schema_metadata(singleton, schema_version, relay_profile, created_at) VALUES(1, ?, ?, ?)",
                    (SCHEMA_VERSION, PROFILE, timestamp),
                )
                connection.commit()
            metadata = _row(
                connection.execute("SELECT * FROM schema_metadata WHERE singleton=1").fetchone(),
                "relay schema metadata",
            )
            if metadata["schema_version"] != SCHEMA_VERSION or metadata["relay_profile"] != PROFILE:
                raise RelayIntegrityError("database profile/schema is not the recursive relay profile")
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            foreign = connection.execute("PRAGMA foreign_key_check").fetchall()
            if integrity != "ok" or foreign:
                raise RelayIntegrityError(
                    "relay database integrity check failed",
                    details={"integrity_check": integrity, "foreign_key_issues": [tuple(row) for row in foreign]},
                )
        return {
            "status": "existing" if existed else "created",
            "database": str(self.path),
            "schema_version": SCHEMA_VERSION,
            "relay_profile": PROFILE,
            "sha256": file_sha256(self.path),
        }

    def backup(self, destination: str | Path) -> dict[str, Any]:
        self.bootstrap()
        return sqlite_backup(self.path, destination)

    @staticmethod
    def _journal(
        connection: sqlite3.Connection,
        run_id: str,
        kind: str,
        payload: Mapping[str, Any],
        timestamp: str,
    ) -> str:
        prior = connection.execute(
            "SELECT sequence, entry_sha256 FROM relay_journal WHERE run_id=? ORDER BY sequence DESC LIMIT 1",
            (run_id,),
        ).fetchone()
        sequence = 1 if prior is None else int(prior["sequence"]) + 1
        prior_hash = None if prior is None else str(prior["entry_sha256"])
        body = copy.deepcopy(dict(payload))
        payload_hash = content_sha256(body)
        entry = {
            "run_id": run_id,
            "sequence": sequence,
            "kind": kind,
            "payload_sha256": payload_hash,
            "prior_entry_sha256": prior_hash,
            "created_at": timestamp,
        }
        entry_hash = content_sha256(entry)
        connection.execute(
            "INSERT INTO relay_journal(run_id, sequence, kind, payload_json, payload_sha256, prior_entry_sha256, entry_sha256, created_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
            (run_id, sequence, kind, _json(body), payload_hash, prior_hash, entry_hash, timestamp),
        )
        return entry_hash

    @staticmethod
    def _run(connection: sqlite3.Connection, run_id: str) -> sqlite3.Row:
        return _row(connection.execute("SELECT * FROM relay_runs WHERE run_id=?", (run_id,)).fetchone(), "relay run")

    @staticmethod
    def _generation(connection: sqlite3.Connection, run_id: str, generation: int) -> sqlite3.Row:
        return _row(
            connection.execute(
                "SELECT * FROM relay_generations WHERE run_id=? AND generation=?",
                (run_id, generation),
            ).fetchone(),
            "relay generation",
        )

    @staticmethod
    def _check_expected(
        run: sqlite3.Row,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        profile: str = PROFILE,
        topology: str = TOPOLOGY,
    ) -> None:
        mismatches: list[str] = []
        if int(run["revision"]) != expected_revision:
            mismatches.append("revision")
        if run["repository_fingerprint"] != repository_fingerprint:
            mismatches.append("repository_fingerprint")
        if run["control_fingerprint"] != control_fingerprint:
            mismatches.append("control_fingerprint")
        if run["relay_profile"] != profile:
            mismatches.append("relay_profile")
        if run["relay_topology"] != topology:
            mismatches.append("relay_topology")
        if mismatches:
            raise RelayConflict(
                "relay compare-and-swap evidence mismatch",
                details={"reason_code": "relay.identity_or_revision_mismatch", "fields": mismatches},
            )

    @staticmethod
    def _check_lease(
        connection: sqlite3.Connection,
        run_id: str,
        token: str,
        *,
        thread_id: str | None = None,
    ) -> sqlite3.Row:
        lease = _row(
            connection.execute(
                "SELECT * FROM relay_leases WHERE run_id=? AND released_at IS NULL", (run_id,)
            ).fetchone(),
            "active relay lease",
        )
        if lease["holder_token_sha256"] != _token_sha256(token):
            raise RelayConflict("relay lease token mismatch", details={"reason_code": "relay.lease_token_mismatch"})
        if thread_id is not None and lease["holder_thread_id"] != thread_id:
            raise RelayConflict("current discussion does not own the relay lease", details={"reason_code": "relay.lease_owner_mismatch"})
        return lease

    @staticmethod
    def _completed_tasks(connection: sqlite3.Connection, run_id: str) -> set[str]:
        rows = connection.execute(
            "SELECT receipt_json FROM task_receipts WHERE run_id=? ORDER BY generation", (run_id,)
        ).fetchall()
        completed: set[str] = set()
        for row in rows:
            receipt = json.loads(row["receipt_json"])
            if receipt.get("disposition") in {"completed", "superseded"}:
                completed.add(str(receipt["task_id"]))
        return completed

    @staticmethod
    def _select_next(plan: Mapping[str, Any], completed: set[str]) -> Mapping[str, Any] | None:
        for task in plan["tasks"]:
            task_id = str(task["task_id"])
            if task_id in completed:
                continue
            if all(str(item) in completed for item in task.get("depends_on", [])):
                return task
        return None

    @staticmethod
    def _envelope(
        *,
        run_id: str,
        plan_id: str,
        plan_sha256: str,
        task: Mapping[str, Any],
        generation: int,
        predecessor_thread_id: str,
        predecessor_receipt_sha256: str | None,
        repository_binding: Mapping[str, Any],
        repository_fingerprint: str,
        control_fingerprint: str,
        requested_effort: str,
        token_sha256: str,
    ) -> dict[str, Any]:
        return {
            "schema_version": "sys4ai.plan-task-envelope.v3",
            "run_id": run_id,
            "plan_id": plan_id,
            "plan_sha256": plan_sha256,
            "task_id": str(task["task_id"]),
            "task_sha256": _task_hash(task),
            "generation": generation,
            "predecessor_thread_id": predecessor_thread_id,
            "predecessor_receipt_sha256": predecessor_receipt_sha256,
            "repository_binding": copy.deepcopy(dict(repository_binding)),
            "repository_fingerprint": repository_fingerprint,
            "control_fingerprint": control_fingerprint,
            "relay_profile": PROFILE,
            "relay_topology": TOPOLOGY,
            "requested_effort": requested_effort,
            "handoff_token_sha256": token_sha256,
            "cardinality": {
                "tasks": 1,
                "continue_invocations": 1,
                "agentjobs": 1,
                "next_task_successors": 1,
                "same_task_successors": 0,
            },
        }

    def launch(
        self,
        *,
        plan: Mapping[str, Any],
        acceptance: Mapping[str, Any],
        repository_binding: Mapping[str, Any],
        repository_fingerprint: str,
        control_fingerprint: str,
        launcher_thread_id: str,
        requested_effort: str,
        effective_effort: str,
        authority_manifest: Mapping[str, Any],
        protected_effect_grants: Mapping[str, Any],
        run_id: str | None = None,
        lease_expires_at: str = "9999-12-31T23:59:59Z",
    ) -> dict[str, Any]:
        canonical_plan = validate_plan(plan)
        canonical_json_bytes(repository_binding)
        _require_nonblank(repository_fingerprint, "repository_fingerprint")
        _require_nonblank(control_fingerprint, "control_fingerprint")
        _require_nonblank(launcher_thread_id, "launcher_thread_id")
        _require_nonblank(requested_effort, "requested_effort")
        _require_nonblank(effective_effort, "effective_effort")
        parse_utc(lease_expires_at)
        plan_sha = content_sha256(canonical_plan)
        acceptance_basis = build_acceptance_basis(
            plan=canonical_plan,
            repository_binding=repository_binding,
            repository_fingerprint=repository_fingerprint,
            control_fingerprint=control_fingerprint,
            launcher_thread_id=launcher_thread_id,
            requested_effort=requested_effort,
            effective_effort=effective_effort,
            authority_manifest=authority_manifest,
            protected_effect_grants=protected_effect_grants,
        )
        canonical_acceptance = validate_acceptance(
            acceptance, basis=acceptance_basis
        )
        run_id = run_id or f"RLY-{plan_sha[:20]}"
        first = self._select_next(canonical_plan, set())
        if first is None:
            raise RelayConflict(
                "accepted plan has no ready task and is not a launchable completion",
                details={"reason_code": "relay.no_ready_not_complete"},
            )
        # No relay database or reservation exists until every acceptance and
        # identity check above has succeeded.
        self.bootstrap()
        token = secrets.token_urlsafe(32)
        token_hash = _token_sha256(token)
        timestamp = utc_now()
        binding_hash = content_sha256(repository_binding)
        envelope = self._envelope(
            run_id=run_id,
            plan_id=str(canonical_plan["plan_id"]),
            plan_sha256=plan_sha,
            task=first,
            generation=1,
            predecessor_thread_id=launcher_thread_id,
            predecessor_receipt_sha256=None,
            repository_binding=repository_binding,
            repository_fingerprint=repository_fingerprint,
            control_fingerprint=control_fingerprint,
            requested_effort=requested_effort,
            token_sha256=token_hash,
        )
        envelope_hash = content_sha256(envelope)
        intent_id = f"INT-{content_sha256({'run_id': run_id, 'generation': 1})[:24]}"
        idempotency_key = f"{run_id}:1"
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            if connection.execute("SELECT 1 FROM relay_runs WHERE run_id=?", (run_id,)).fetchone():
                raise RelayConflict("relay run already exists", details={"reason_code": "relay.run_exists"})
            connection.execute(
                "INSERT INTO relay_runs(run_id,plan_id,plan_sha256,plan_json,acceptance_sha256,repository_binding_json,repository_binding_sha256,repository_fingerprint,control_fingerprint,relay_profile,relay_topology,launcher_thread_id,requested_effort,revision,status,current_generation,completion_report_sha256,cancellation_reason,created_at,updated_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'active', 1, NULL, NULL, ?, ?)",
                (
                    run_id,
                    canonical_plan["plan_id"],
                    plan_sha,
                    _json(canonical_plan),
                    content_sha256(canonical_acceptance),
                    _json(repository_binding),
                    binding_hash,
                    repository_fingerprint,
                    control_fingerprint,
                    PROFILE,
                    TOPOLOGY,
                    launcher_thread_id,
                    requested_effort,
                    timestamp,
                    timestamp,
                ),
            )
            connection.execute(
                "INSERT INTO relay_generations(run_id,generation,task_id,task_sha256,predecessor_thread_id,predecessor_receipt_sha256,worker_thread_id,requested_effort,effective_effort,status,handoff_token_sha256,envelope_sha256,invocation_count,result_json,result_sha256,receipt_sha256,successor_generation,created_at,updated_at) VALUES(?,1,?,?,?,NULL,NULL,?,NULL,'dispatch_pending',?,?,0,NULL,NULL,NULL,NULL,?,?)",
                (run_id, first["task_id"], _task_hash(first), launcher_thread_id, requested_effort, token_hash, envelope_hash, timestamp, timestamp),
            )
            connection.execute(
                "INSERT INTO task_envelopes VALUES(?,?,?,?)",
                (run_id, 1, _json(envelope), envelope_hash),
            )
            connection.execute(
                "INSERT INTO dispatch_intents VALUES(?,?,1,?,1,0,'pending',?,NULL,NULL,NULL,?,?)",
                (intent_id, run_id, idempotency_key, requested_effort, timestamp, timestamp),
            )
            connection.execute(
                "INSERT INTO relay_leases VALUES(?,?, 'launcher', 1, ?, ?, ?, ?, NULL)",
                (run_id, repository_fingerprint, launcher_thread_id, token_hash, timestamp, lease_expires_at),
            )
            self._journal(
                connection,
                run_id,
                "relay_launched",
                {
                    "generation": 1,
                    "task_id": first["task_id"],
                    "envelope_sha256": envelope_hash,
                    "intent_id": intent_id,
                    "zero_agentjobs": True,
                },
                timestamp,
            )
        return {
            "status": "dispatch_pending",
            "run_id": run_id,
            "revision": 1,
            "generation": 1,
            "intent_id": intent_id,
            "idempotency_key": idempotency_key,
            "envelope": envelope,
            "envelope_sha256": envelope_hash,
            "acceptance_sha256": content_sha256(canonical_acceptance),
            "handoff_token": token,
            "maximum_agentjobs": 0,
            "next_safe_action": "prepare-dispatch",
        }

    def begin_dispatch(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        owner_token: str,
        current_thread_id: str,
    ) -> dict[str, Any]:
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            self._check_lease(connection, run_id, owner_token, thread_id=current_thread_id)
            intent = _row(connection.execute("SELECT * FROM dispatch_intents WHERE run_id=? AND generation=?", (run_id, generation)).fetchone(), "dispatch intent")
            if intent["status"] in {"creating", "ambiguous", "returned"} and int(intent["attempt_count"]) == 1:
                return {"status": "already_creating", "intent_id": intent["intent_id"], "revision": expected_revision}
            if intent["status"] != "pending" or int(intent["attempt_count"]) != 0:
                raise RelayConflict("dispatch create budget is not available", details={"reason_code": "relay.create_budget_exhausted"})
            connection.execute("UPDATE dispatch_intents SET status='creating', attempt_count=1, updated_at=? WHERE intent_id=?", (timestamp, intent["intent_id"]))
            new_revision = expected_revision + 1
            connection.execute("UPDATE relay_runs SET revision=?,updated_at=? WHERE run_id=?", (new_revision, timestamp, run_id))
            self._journal(connection, run_id, "dispatch_attempt_started", {"generation": generation, "intent_id": intent["intent_id"], "attempt_count": 1}, timestamp)
        return {"status": "creating", "intent_id": intent["intent_id"], "idempotency_key": intent["idempotency_key"], "revision": new_revision}

    def record_successor(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        owner_token: str,
        current_thread_id: str,
        child_thread_id: str,
        provider_response: Mapping[str, Any],
        effective_effort: str,
        child_token: str | None = None,
    ) -> dict[str, Any]:
        _require_nonblank(child_thread_id, "child_thread_id")
        _require_nonblank(effective_effort, "effective_effort")
        response_hash = content_sha256(provider_response)
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            self._check_lease(connection, run_id, owner_token, thread_id=current_thread_id)
            intent = _row(connection.execute("SELECT * FROM dispatch_intents WHERE run_id=? AND generation=?", (run_id, generation)).fetchone(), "dispatch intent")
            generation_row = self._generation(connection, run_id, generation)
            if intent["status"] == "recorded":
                if intent["child_thread_id"] == child_thread_id and intent["provider_response_sha256"] == response_hash:
                    return {"status": "already_recorded", "child_thread_id": child_thread_id, "revision": expected_revision}
                raise RelayConflict("a different successor is already recorded", details={"reason_code": "relay.different_child_conflict"})
            if int(intent["attempt_count"]) != 1 or intent["status"] not in {"creating", "returned", "ambiguous"}:
                raise RelayConflict("successor cannot be recorded for this intent state", details={"reason_code": "relay.intent_not_recordable"})
            if effective_effort != generation_row["requested_effort"]:
                raise RelayConflict("successor effective effort differs from the accepted effort", details={"reason_code": "relay.effort_mismatch"})
            new_token = child_token or owner_token
            new_token_hash = _token_sha256(new_token)
            if new_token_hash != generation_row["handoff_token_sha256"]:
                raise RelayConflict(
                    "recorded child token differs from the immutable envelope",
                    details={"reason_code": "relay.handoff_token_mismatch"},
                )
            connection.execute(
                "UPDATE dispatch_intents SET status='recorded',child_thread_id=?,provider_response_json=?,provider_response_sha256=?,updated_at=? WHERE intent_id=?",
                (child_thread_id, _json(provider_response), response_hash, timestamp, intent["intent_id"]),
            )
            connection.execute(
                "UPDATE relay_generations SET worker_thread_id=?,effective_effort=?,status='reserved',handoff_token_sha256=?,updated_at=? WHERE run_id=? AND generation=?",
                (child_thread_id, effective_effort, new_token_hash, timestamp, run_id, generation),
            )
            connection.execute(
                "UPDATE relay_leases SET holder_kind='worker',holder_generation=?,holder_thread_id=?,holder_token_sha256=?,heartbeat_at=? WHERE run_id=? AND released_at IS NULL",
                (generation, child_thread_id, new_token_hash, timestamp, run_id),
            )
            new_revision = expected_revision + 1
            connection.execute("UPDATE relay_runs SET revision=?,updated_at=? WHERE run_id=?", (new_revision, timestamp, run_id))
            self._journal(connection, run_id, "successor_recorded", {"generation": generation, "intent_id": intent["intent_id"], "child_thread_id": child_thread_id, "provider_response_sha256": response_hash}, timestamp)
        return {"status": "successor_created", "child_thread_id": child_thread_id, "handoff_token": new_token, "revision": new_revision}

    def mark_dispatch_ambiguous(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        owner_token: str,
        current_thread_id: str,
        evidence: Mapping[str, Any],
    ) -> dict[str, Any]:
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            self._check_lease(connection, run_id, owner_token, thread_id=current_thread_id)
            intent = _row(connection.execute("SELECT * FROM dispatch_intents WHERE run_id=? AND generation=?", (run_id, generation)).fetchone(), "dispatch intent")
            if int(intent["attempt_count"]) != 1 or intent["status"] not in {"creating", "ambiguous"}:
                raise RelayConflict("dispatch is not at an ambiguous create boundary")
            connection.execute("UPDATE dispatch_intents SET status='ambiguous',provider_response_json=?,provider_response_sha256=?,updated_at=? WHERE intent_id=?", (_json(evidence), content_sha256(evidence), timestamp, intent["intent_id"]))
            new_revision = expected_revision + 1
            connection.execute("UPDATE relay_runs SET revision=?,updated_at=? WHERE run_id=?", (new_revision, timestamp, run_id))
            self._journal(connection, run_id, "dispatch_ambiguous", {"generation": generation, "intent_id": intent["intent_id"], "evidence_sha256": content_sha256(evidence)}, timestamp)
        return {"status": "ambiguous", "revision": new_revision, "next_safe_action": "reconcile-dispatch"}

    def reconcile_dispatch(
        self,
        run_id: str,
        generation: int,
        *,
        matches: Sequence[Mapping[str, Any]],
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        owner_token: str,
        current_thread_id: str,
    ) -> dict[str, Any]:
        exact = [dict(item) for item in matches]
        if len(exact) == 1:
            child = exact[0]
            return self.record_successor(
                run_id,
                generation,
                expected_revision=expected_revision,
                repository_fingerprint=repository_fingerprint,
                control_fingerprint=control_fingerprint,
                owner_token=owner_token,
                current_thread_id=current_thread_id,
                child_thread_id=_require_nonblank(child.get("thread_id"), "thread_id"),
                provider_response={"reconciled": True, "match": child},
                effective_effort=_require_nonblank(child.get("effective_effort"), "effective_effort"),
            )
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            self._check_lease(connection, run_id, owner_token, thread_id=current_thread_id)
            intent = _row(connection.execute("SELECT * FROM dispatch_intents WHERE run_id=? AND generation=?", (run_id, generation)).fetchone(), "dispatch intent")
            if intent["status"] != "ambiguous":
                raise RelayConflict("only an ambiguous intent can enter reconciliation gate")
            reason = "relay.dispatch_zero_matches" if not exact else "relay.dispatch_multiple_matches"
            connection.execute("UPDATE dispatch_intents SET status='human_gate',provider_response_json=?,provider_response_sha256=?,updated_at=? WHERE intent_id=?", (_json({"matches": exact}), content_sha256({"matches": exact}), timestamp, intent["intent_id"]))
            connection.execute("UPDATE relay_generations SET status='human_gate',updated_at=? WHERE run_id=? AND generation=?", (timestamp, run_id, generation))
            connection.execute("UPDATE relay_runs SET status='human_gate',revision=?,updated_at=? WHERE run_id=?", (expected_revision + 1, timestamp, run_id))
            connection.execute("UPDATE relay_leases SET holder_kind='quarantined',heartbeat_at=? WHERE run_id=? AND released_at IS NULL", (timestamp, run_id))
            self._journal(connection, run_id, "dispatch_human_gate", {"generation": generation, "reason_code": reason, "match_count": len(exact)}, timestamp)
        return {"status": "human_gate", "reason_code": reason, "revision": expected_revision + 1, "child_created": False}

    def claim_generation(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
        effective_effort: str,
    ) -> dict[str, Any]:
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            generation_row = self._generation(connection, run_id, generation)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            if generation_row["status"] == "claimed" and generation_row["worker_thread_id"] == current_thread_id:
                return {"status": "already_claimed", "revision": expected_revision}
            if generation_row["status"] != "reserved" or generation_row["worker_thread_id"] != current_thread_id:
                raise RelayConflict("generation is not reserved for the current discussion", details={"reason_code": "relay.claim_identity_mismatch"})
            if generation_row["effective_effort"] != effective_effort or generation_row["requested_effort"] != effective_effort:
                raise RelayConflict("current discussion effort differs from envelope", details={"reason_code": "relay.effort_mismatch"})
            if generation > 1:
                prior = self._generation(connection, run_id, generation - 1)
                if generation_row["predecessor_thread_id"] != prior["worker_thread_id"] or generation_row["predecessor_receipt_sha256"] != prior["receipt_sha256"]:
                    raise RelayConflict("predecessor handoff is not recorded", details={"reason_code": "relay.predecessor_handoff_missing"})
            connection.execute("UPDATE relay_generations SET status='claimed',updated_at=? WHERE run_id=? AND generation=?", (timestamp, run_id, generation))
            new_revision = expected_revision + 1
            connection.execute("UPDATE relay_runs SET revision=?,updated_at=? WHERE run_id=?", (new_revision, timestamp, run_id))
            self._journal(connection, run_id, "generation_claimed", {"generation": generation, "worker_thread_id": current_thread_id}, timestamp)
        return {"status": "claimed", "revision": new_revision, "generation": generation}

    def consume_generation(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
    ) -> dict[str, Any]:
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            generation_row = self._generation(connection, run_id, generation)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            if generation_row["status"] != "claimed" or int(generation_row["invocation_count"]) != 0:
                raise RelayConflict("generation cannot be consumed again", details={"reason_code": "relay.duplicate_consume"})
            connection.execute("UPDATE relay_generations SET status='consumed',invocation_count=1,updated_at=? WHERE run_id=? AND generation=?", (timestamp, run_id, generation))
            new_revision = expected_revision + 1
            connection.execute("UPDATE relay_runs SET revision=?,updated_at=? WHERE run_id=?", (new_revision, timestamp, run_id))
            self._journal(connection, run_id, "generation_consumed", {"generation": generation, "worker_thread_id": current_thread_id, "maximum_continue_invocations": 1}, timestamp)
        return {"status": "consumed", "revision": new_revision, "generation": generation, "continue_budget_remaining": 0}

    def record_returned(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
        result: Mapping[str, Any],
    ) -> dict[str, Any]:
        timestamp = utc_now()
        result_hash = content_sha256(result)
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            row = self._generation(connection, run_id, generation)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            if row["status"] == "returned" and row["result_sha256"] == result_hash:
                return {"status": "already_returned", "revision": expected_revision, "result_sha256": result_hash}
            if row["status"] != "consumed" or int(row["invocation_count"]) != 1:
                raise RelayConflict("direct return requires one consumed invocation", details={"reason_code": "relay.return_without_consume"})
            connection.execute("UPDATE relay_generations SET status='returned',result_json=?,result_sha256=?,updated_at=? WHERE run_id=? AND generation=?", (_json(result), result_hash, timestamp, run_id, generation))
            new_revision = expected_revision + 1
            connection.execute("UPDATE relay_runs SET revision=?,updated_at=? WHERE run_id=?", (new_revision, timestamp, run_id))
            self._journal(connection, run_id, "generation_returned", {"generation": generation, "result_sha256": result_hash}, timestamp)
        return {"status": "returned", "revision": new_revision, "result_sha256": result_hash}

    def record_unknown(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
        evidence: Mapping[str, Any],
    ) -> dict[str, Any]:
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            row = self._generation(connection, run_id, generation)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            if row["status"] != "consumed" or int(row["invocation_count"]) != 1:
                raise RelayConflict("unknown outcome requires consumed work")
            connection.execute("UPDATE relay_generations SET status='invocation_unknown',result_json=?,result_sha256=?,updated_at=? WHERE run_id=? AND generation=?", (_json(evidence), content_sha256(evidence), timestamp, run_id, generation))
            connection.execute("UPDATE relay_runs SET status='invocation_unknown',revision=?,updated_at=? WHERE run_id=?", (expected_revision + 1, timestamp, run_id))
            connection.execute("UPDATE relay_leases SET holder_kind='quarantined',heartbeat_at=? WHERE run_id=? AND released_at IS NULL", (timestamp, run_id))
            self._journal(connection, run_id, "invocation_unknown", {"generation": generation, "evidence_sha256": content_sha256(evidence), "automatic_rerun_authorized": False}, timestamp)
        return {"status": "invocation_unknown", "revision": expected_revision + 1, "child_created": False, "automatic_rerun_authorized": False}

    def finalize_receipt(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
        disposition: str,
        evidence: Mapping[str, Any],
    ) -> dict[str, Any]:
        if disposition not in {"completed", "superseded", "validation_failed", "human_gate", "cancelled"}:
            raise RecordValidationError("receipt disposition is unsupported")
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            row = self._generation(connection, run_id, generation)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            if row["receipt_sha256"] is not None:
                existing = _row(connection.execute("SELECT * FROM task_receipts WHERE run_id=? AND generation=?", (run_id, generation)).fetchone(), "task receipt")
                return {"status": "already_finalized", "revision": expected_revision, "receipt_sha256": existing["receipt_sha256"]}
            if row["status"] != "returned" or row["result_sha256"] is None:
                raise RelayConflict("receipt requires direct returned evidence", details={"reason_code": "relay.receipt_without_return"})
            receipt = {
                "schema_version": "sys4ai.plan-task-receipt.v3",
                "receipt_id": f"RCP-{content_sha256({'run_id': run_id, 'generation': generation})[:24]}",
                "run_id": run_id,
                "plan_id": run["plan_id"],
                "plan_sha256": run["plan_sha256"],
                "generation": generation,
                "task_id": row["task_id"],
                "task_sha256": row["task_sha256"],
                "worker_thread_id": current_thread_id,
                "result_sha256": row["result_sha256"],
                "disposition": disposition,
                "evidence": copy.deepcopy(dict(evidence)),
                "repository_fingerprint": repository_fingerprint,
                "control_fingerprint": control_fingerprint,
                "relay_profile": PROFILE,
                "relay_topology": TOPOLOGY,
                "invocation_count": 1,
                "successor_count": 0,
                "created_at": timestamp,
            }
            receipt_hash = content_sha256(receipt)
            connection.execute("INSERT INTO task_receipts VALUES(?,?,?,?,?,?)", (receipt["receipt_id"], run_id, generation, _json(receipt), receipt_hash, timestamp))
            next_status = "receipt_finalized" if disposition in {"completed", "superseded"} else disposition
            connection.execute("UPDATE relay_generations SET status=?,receipt_sha256=?,updated_at=? WHERE run_id=? AND generation=?", (next_status, receipt_hash, timestamp, run_id, generation))
            run_status = "active" if next_status == "receipt_finalized" else next_status
            connection.execute("UPDATE relay_runs SET status=?,revision=?,updated_at=? WHERE run_id=?", (run_status, expected_revision + 1, timestamp, run_id))
            if next_status != "receipt_finalized":
                connection.execute("UPDATE relay_leases SET holder_kind='quarantined',heartbeat_at=? WHERE run_id=? AND released_at IS NULL", (timestamp, run_id))
            self._journal(connection, run_id, "task_receipt_finalized", {"generation": generation, "receipt_sha256": receipt_hash, "disposition": disposition}, timestamp)
        return {"status": next_status, "revision": expected_revision + 1, "receipt": receipt, "receipt_sha256": receipt_hash}

    def record_protected_stop(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
        disposition: str,
        reason_code: str,
        evidence: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Persist a no-child protected stop before executor consumption."""

        allowed = {
            "human_gate",
            "integrity_stop",
            "validation_failed",
            "capability_blocked",
        }
        if disposition not in allowed:
            raise RecordValidationError("protected-stop disposition is unsupported")
        _require_nonblank(reason_code, "reason_code")
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(
                run,
                expected_revision=expected_revision,
                repository_fingerprint=repository_fingerprint,
                control_fingerprint=control_fingerprint,
            )
            row = self._generation(connection, run_id, generation)
            self._check_lease(
                connection,
                run_id,
                handoff_token,
                thread_id=current_thread_id,
            )
            if row["status"] in {
                "consumed",
                "returned",
                "invocation_unknown",
                "receipt_finalized",
                "successor_reserved",
                "cancelled",
            } or int(row["invocation_count"]) != 0:
                raise RelayConflict(
                    "a consumed or completed generation cannot become a pre-call protected stop",
                    details={"reason_code": "relay.protected_stop_after_consume"},
                )
            intent = _row(
                connection.execute(
                    "SELECT * FROM dispatch_intents WHERE run_id=? AND generation=?",
                    (run_id, generation),
                ).fetchone(),
                "dispatch intent",
            )
            intent_status = str(intent["status"])
            attempt_count = int(intent["attempt_count"])
            if intent_status == "pending" and attempt_count == 0:
                intent_status = (
                    "human_gate"
                    if disposition == "human_gate"
                    else "failed_before_create"
                )
                connection.execute(
                    "UPDATE dispatch_intents SET status=?,provider_response_json=?,"
                    "provider_response_sha256=?,updated_at=? WHERE intent_id=?",
                    (
                        intent_status,
                        _json(evidence),
                        content_sha256(evidence),
                        timestamp,
                        intent["intent_id"],
                    ),
                )
            elif intent_status == "creating" and attempt_count == 1:
                if evidence.get("effect_not_attempted") is not True:
                    raise RelayConflict(
                        "an uncertain create must be recorded and reconciled before a protected stop",
                        details={
                            "reason_code": "relay.create_outcome_requires_reconciliation"
                        },
                    )
                intent_status = "failed_before_create"
                connection.execute(
                    "UPDATE dispatch_intents SET status='failed_before_create',"
                    "provider_response_json=?,provider_response_sha256=?,updated_at=? "
                    "WHERE intent_id=?",
                    (
                        _json(evidence),
                        content_sha256(evidence),
                        timestamp,
                        intent["intent_id"],
                    ),
                )
            elif intent_status == "ambiguous":
                raise RelayConflict(
                    "an ambiguous create requires idempotency reconciliation",
                    details={
                        "reason_code": "relay.create_outcome_requires_reconciliation"
                    },
                )
            connection.execute(
                "UPDATE relay_generations SET status=?,updated_at=? "
                "WHERE run_id=? AND generation=?",
                (disposition, timestamp, run_id, generation),
            )
            connection.execute(
                "UPDATE relay_runs SET status=?,revision=?,updated_at=? WHERE run_id=?",
                (disposition, expected_revision + 1, timestamp, run_id),
            )
            connection.execute(
                "UPDATE relay_leases SET holder_kind='quarantined',heartbeat_at=? "
                "WHERE run_id=? AND released_at IS NULL",
                (timestamp, run_id),
            )
            self._journal(
                connection,
                run_id,
                "relay_protected_stop",
                {
                    "generation": generation,
                    "disposition": disposition,
                    "reason_code": reason_code,
                    "evidence_sha256": content_sha256(evidence),
                    "child_created": False,
                    "intent_status": intent_status,
                },
                timestamp,
            )
        return {
            "status": disposition,
            "reason_code": reason_code,
            "revision": expected_revision + 1,
            "child_created": False,
            "automatic_rerun_authorized": False,
            "intent_status": intent_status,
        }

    def verify_and_decide(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
    ) -> dict[str, Any]:
        with connect_sqlite(self.path, read_only=True) as connection:
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            row = self._generation(connection, run_id, generation)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            if row["status"] != "receipt_finalized" or row["receipt_sha256"] is None:
                raise RelayConflict("decision requires one finalized successful receipt")
            plan = json.loads(run["plan_json"])
            completed = self._completed_tasks(connection, run_id)
            next_task = self._select_next(plan, completed)
            all_complete = len(completed) == len(plan["tasks"])
            if all_complete:
                return {
                    "status": "plan_completion_candidate",
                    "decision": "plan_complete",
                    "revision": expected_revision,
                    "completion_report": self.build_completion_report(run_id),
                    "next_safe_action": "finalize-plan",
                }
            if next_task is None:
                return {
                    "status": "protected",
                    "decision": "no_ready_blocked",
                    "revision": expected_revision,
                    "child_created": False,
                    "next_safe_action": "human-gate-or-replan",
                }
            return {
                "status": "successor_candidate",
                "decision": "safe_next_task",
                "revision": expected_revision,
                "task_id": next_task["task_id"],
                "next_safe_action": "reserve-successor",
            }

    def reserve_successor(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
    ) -> dict[str, Any]:
        timestamp = utc_now()
        token = secrets.token_urlsafe(32)
        token_hash = _token_sha256(token)
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            row = self._generation(connection, run_id, generation)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            if row["successor_generation"] is not None:
                successor = self._generation(connection, run_id, int(row["successor_generation"]))
                if successor["task_id"] == row["task_id"]:
                    raise RelayIntegrityError("same-task successor exists")
                return {"status": "already_reserved", "generation": int(row["successor_generation"]), "revision": expected_revision}
            if row["status"] != "receipt_finalized" or row["receipt_sha256"] is None:
                raise RelayConflict("successor reservation requires a finalized receipt")
            plan = json.loads(run["plan_json"])
            completed = self._completed_tasks(connection, run_id)
            next_task = self._select_next(plan, completed)
            if next_task is None:
                raise RelayConflict("no dependency-ready successor exists", details={"reason_code": "relay.no_ready_not_complete"})
            if str(next_task["task_id"]) == row["task_id"]:
                raise RelayConflict("same-task automatic successor is forbidden")
            next_generation = generation + 1
            envelope = self._envelope(
                run_id=run_id,
                plan_id=run["plan_id"],
                plan_sha256=run["plan_sha256"],
                task=next_task,
                generation=next_generation,
                predecessor_thread_id=current_thread_id,
                predecessor_receipt_sha256=row["receipt_sha256"],
                repository_binding=json.loads(run["repository_binding_json"]),
                repository_fingerprint=repository_fingerprint,
                control_fingerprint=control_fingerprint,
                requested_effort=run["requested_effort"],
                token_sha256=token_hash,
            )
            envelope_hash = content_sha256(envelope)
            intent_id = f"INT-{content_sha256({'run_id': run_id, 'generation': next_generation})[:24]}"
            connection.execute("UPDATE relay_generations SET status='successor_reserved',successor_generation=?,updated_at=? WHERE run_id=? AND generation=?", (next_generation, timestamp, run_id, generation))
            connection.execute(
                "INSERT INTO relay_generations(run_id,generation,task_id,task_sha256,predecessor_thread_id,predecessor_receipt_sha256,worker_thread_id,requested_effort,effective_effort,status,handoff_token_sha256,envelope_sha256,invocation_count,result_json,result_sha256,receipt_sha256,successor_generation,created_at,updated_at) VALUES(?,?,?,?,?,?,NULL,?,NULL,'dispatch_pending',?,?,0,NULL,NULL,NULL,NULL,?,?)",
                (run_id, next_generation, next_task["task_id"], _task_hash(next_task), current_thread_id, row["receipt_sha256"], run["requested_effort"], token_hash, envelope_hash, timestamp, timestamp),
            )
            connection.execute("INSERT INTO task_envelopes VALUES(?,?,?,?)", (run_id, next_generation, _json(envelope), envelope_hash))
            connection.execute("INSERT INTO dispatch_intents VALUES(?,?,?, ?,1,0,'pending',?,NULL,NULL,NULL,?,?)", (intent_id, run_id, next_generation, f"{run_id}:{next_generation}", run["requested_effort"], timestamp, timestamp))
            connection.execute("UPDATE relay_leases SET holder_kind='successor_reserved',holder_generation=?,holder_thread_id=?,holder_token_sha256=?,heartbeat_at=? WHERE run_id=? AND released_at IS NULL", (next_generation, current_thread_id, token_hash, timestamp, run_id))
            new_revision = expected_revision + 1
            connection.execute("UPDATE relay_runs SET current_generation=?,revision=?,updated_at=? WHERE run_id=?", (next_generation, new_revision, timestamp, run_id))
            self._journal(connection, run_id, "successor_reserved", {"generation": next_generation, "task_id": next_task["task_id"], "predecessor_thread_id": current_thread_id, "predecessor_receipt_sha256": row["receipt_sha256"], "intent_id": intent_id}, timestamp)
        return {"status": "dispatch_pending", "generation": next_generation, "revision": new_revision, "intent_id": intent_id, "envelope": envelope, "handoff_token": token, "next_safe_action": "prepare-dispatch"}

    def build_completion_report(self, run_id: str) -> dict[str, Any]:
        with connect_sqlite(self.path, read_only=True) as connection:
            run = self._run(connection, run_id)
            plan = json.loads(run["plan_json"])
            receipts = [json.loads(row["receipt_json"]) for row in connection.execute("SELECT receipt_json FROM task_receipts WHERE run_id=? ORDER BY generation", (run_id,))]
            completed = {str(receipt["task_id"]) for receipt in receipts if receipt.get("disposition") in {"completed", "superseded"}}
            missing = [str(task["task_id"]) for task in plan["tasks"] if str(task["task_id"]) not in completed]
            open_intents = connection.execute("SELECT COUNT(*) FROM dispatch_intents WHERE run_id=? AND status NOT IN ('recorded','failed_before_create','human_gate')", (run_id,)).fetchone()[0]
            report = {
                "schema_version": "sys4ai.plan-completion-report.v2",
                "run_id": run_id,
                "plan_id": run["plan_id"],
                "plan_sha256": run["plan_sha256"],
                "repository_fingerprint": run["repository_fingerprint"],
                "control_fingerprint": run["control_fingerprint"],
                "relay_profile": PROFILE,
                "relay_topology": TOPOLOGY,
                "task_count": len(plan["tasks"]),
                "receipt_count": len(receipts),
                "completed_task_ids": sorted(completed),
                "missing_task_ids": missing,
                "open_intent_count": int(open_intents),
                "terminal_proof": not missing and len(receipts) == len(plan["tasks"]),
                "receipt_sha256s": [content_sha256(receipt) for receipt in receipts],
            }
            report["report_content_sha256"] = content_sha256(report)
            return report

    def finalize_plan(
        self,
        run_id: str,
        *,
        report: Mapping[str, Any],
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
    ) -> dict[str, Any]:
        timestamp = utc_now()
        supplied = copy.deepcopy(dict(report))
        supplied_hash = supplied.pop("report_content_sha256", None)
        if supplied_hash != content_sha256(supplied):
            raise RecordValidationError("completion report content hash is invalid")
        supplied["report_content_sha256"] = supplied_hash
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            if run["status"] == "plan_complete":
                existing = _row(connection.execute("SELECT * FROM completion_reports WHERE run_id=?", (run_id,)).fetchone(), "completion report")
                if existing["report_sha256"] == content_sha256(supplied):
                    return {"status": "already_terminal", "revision": int(run["revision"]), "report_sha256": existing["report_sha256"]}
                raise RelayConflict("run is already terminal with a different report")
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            expected = self.build_completion_report(run_id)
            if supplied != expected or supplied.get("terminal_proof") is not True or supplied.get("missing_task_ids") or supplied.get("open_intent_count") != 0:
                raise RelayConflict("completion report does not prove complete canonical state", details={"reason_code": "relay.terminal_proof_incomplete"})
            current = self._generation(connection, run_id, int(run["current_generation"]))
            if current["status"] != "receipt_finalized" or current["receipt_sha256"] is None:
                raise RelayConflict("terminal generation has no finalized receipt")
            report_hash = content_sha256(supplied)
            connection.execute(
                "INSERT INTO completion_reports VALUES(?,?,?,?)",
                (run_id, _json(supplied), report_hash, timestamp),
            )
            new_revision = expected_revision + 1
            connection.execute("UPDATE relay_runs SET status='plan_complete',completion_report_sha256=?,revision=?,updated_at=? WHERE run_id=?", (report_hash, new_revision, timestamp, run_id))
            connection.execute("UPDATE relay_leases SET released_at=?,heartbeat_at=? WHERE run_id=? AND released_at IS NULL", (timestamp, timestamp, run_id))
            self._journal(connection, run_id, "plan_completed", {"report_sha256": report_hash, "terminal_generation": int(run["current_generation"]), "lease_released": True}, timestamp)
        return {"status": "plan_complete", "revision": new_revision, "report_sha256": report_hash, "child_created": False, "lease_released": True}

    def abandon_unconsumed(
        self,
        run_id: str,
        generation: int,
        *,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
        proof: Mapping[str, Any],
    ) -> dict[str, Any]:
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            row = self._generation(connection, run_id, generation)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            if row["status"] != "claimed" or int(row["invocation_count"]) != 0:
                raise RelayConflict("only directly proven unconsumed claims may be abandoned")
            connection.execute("UPDATE relay_generations SET status='reserved',updated_at=? WHERE run_id=? AND generation=?", (timestamp, run_id, generation))
            connection.execute("UPDATE relay_runs SET revision=?,updated_at=? WHERE run_id=?", (expected_revision + 1, timestamp, run_id))
            self._journal(connection, run_id, "unconsumed_claim_released", {"generation": generation, "proof_sha256": content_sha256(proof)}, timestamp)
        return {"status": "reserved", "revision": expected_revision + 1, "automatic_rerun_authorized": False}

    def reconcile_consumed(
        self,
        run_id: str,
        generation: int,
        *,
        direct_result: Mapping[str, Any] | None,
        **identity: Any,
    ) -> dict[str, Any]:
        if direct_result is None:
            return self.record_unknown(run_id, generation, evidence={"reason_code": "relay.consumed_return_unproven"}, **identity)
        return self.record_returned(run_id, generation, result=direct_result, **identity)

    def cancel(
        self,
        run_id: str,
        *,
        reason: str,
        authority_reference: str,
        expected_revision: int,
        repository_fingerprint: str,
        control_fingerprint: str,
        current_thread_id: str,
        handoff_token: str,
    ) -> dict[str, Any]:
        _require_nonblank(reason, "reason")
        _require_nonblank(authority_reference, "authority_reference")
        timestamp = utc_now()
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            run = self._run(connection, run_id)
            if run["status"] == "cancelled":
                return {"status": "already_cancelled", "revision": int(run["revision"])}
            self._check_expected(run, expected_revision=expected_revision, repository_fingerprint=repository_fingerprint, control_fingerprint=control_fingerprint)
            self._check_lease(connection, run_id, handoff_token, thread_id=current_thread_id)
            connection.execute("UPDATE relay_runs SET status='cancelled',cancellation_reason=?,revision=?,updated_at=? WHERE run_id=?", (reason, expected_revision + 1, timestamp, run_id))
            connection.execute("UPDATE relay_generations SET status='cancelled',updated_at=? WHERE run_id=? AND generation=?", (timestamp, run_id, int(run["current_generation"])))
            connection.execute("UPDATE relay_leases SET released_at=?,heartbeat_at=? WHERE run_id=? AND released_at IS NULL", (timestamp, timestamp, run_id))
            self._journal(connection, run_id, "relay_cancelled", {"reason": reason, "authority_reference": authority_reference, "child_created": False}, timestamp)
        return {"status": "cancelled", "revision": expected_revision + 1, "child_created": False, "lease_released": True}

    def summarize(self, run_id: str) -> dict[str, Any]:
        with connect_sqlite(self.path, read_only=True) as connection:
            run = self._run(connection, run_id)
            generations = []
            for row in connection.execute("SELECT * FROM relay_generations WHERE run_id=? ORDER BY generation", (run_id,)):
                intent = connection.execute("SELECT * FROM dispatch_intents WHERE run_id=? AND generation=?", (run_id, row["generation"])).fetchone()
                generations.append(
                    {
                        "generation": int(row["generation"]),
                        "task_id": row["task_id"],
                        "status": row["status"],
                        "predecessor_thread_id": row["predecessor_thread_id"],
                        "predecessor_receipt_sha256": row["predecessor_receipt_sha256"],
                        "worker_thread_id": row["worker_thread_id"],
                        "intent_id": None if intent is None else intent["intent_id"],
                        "intent_status": None if intent is None else intent["status"],
                        "receipt_sha256": row["receipt_sha256"],
                        "successor_generation": row["successor_generation"],
                        "invocation_count": int(row["invocation_count"]),
                    }
                )
            lease = connection.execute("SELECT * FROM relay_leases WHERE run_id=?", (run_id,)).fetchone()
            journal_count = connection.execute("SELECT COUNT(*) FROM relay_journal WHERE run_id=?", (run_id,)).fetchone()[0]
            status = str(run["status"])
            next_action = {
                "active": "inspect-current-generation",
                "human_gate": "human-reconciliation-required",
                "integrity_stop": "integrity-review-required",
                "validation_failed": "repair-or-replan",
                "capability_blocked": "supply-capability-or-human-authority",
                "invocation_unknown": "reconcile-consumed",
                "cancelled": "none",
                "plan_complete": "none",
            }[status]
            return {
                "schema_version": "sys4ai.plan-relay-summary.v1",
                "run_id": run_id,
                "plan_id": run["plan_id"],
                "status": status,
                "revision": int(run["revision"]),
                "relay_profile": run["relay_profile"],
                "relay_topology": run["relay_topology"],
                "launcher_thread_id": run["launcher_thread_id"],
                "repository_fingerprint": run["repository_fingerprint"],
                "control_fingerprint": run["control_fingerprint"],
                "current_generation": int(run["current_generation"]),
                "generations": generations,
                "lease": None if lease is None else {
                    "holder_kind": lease["holder_kind"],
                    "holder_generation": lease["holder_generation"],
                    "holder_thread_id": lease["holder_thread_id"],
                    "expires_at": lease["expires_at"],
                    "expired": utc_now() >= lease["expires_at"],
                    "released": lease["released_at"] is not None,
                    "steal_authorized": False,
                },
                "completion_report_sha256": run["completion_report_sha256"],
                "journal_count": int(journal_count),
                "next_safe_action": next_action,
                "evidence_classification": {
                    "stored_identity_and_state": "direct",
                    "generation_and_intent_chain": "direct",
                    "worker_thread_id": (
                        "unknown"
                        if generations[-1]["worker_thread_id"] is None
                        else "direct"
                    ),
                    "lease_expired": "inferred",
                    "next_safe_action": "inferred",
                },
            }

    def semantic_projection(self, run_id: str) -> dict[str, Any]:
        """Project independently schema-valid records for cross-record checks.

        The projection is read-only, omits provider response bodies and task
        result bodies, and contains token hashes only.  It is deliberately
        separate from the lossless database export used for backup/restore.
        """

        with connect_sqlite(self.path, read_only=True) as connection:
            run = self._run(connection, run_id)
            run_record = {
                "schema_version": "sys4ai.plan-relay-run.v1",
                "run_id": run["run_id"],
                "plan_id": run["plan_id"],
                "plan_sha256": run["plan_sha256"],
                "acceptance_sha256": run["acceptance_sha256"],
                "repository_binding_sha256": run[
                    "repository_binding_sha256"
                ],
                "repository_fingerprint": run["repository_fingerprint"],
                "control_fingerprint": run["control_fingerprint"],
                "relay_profile": run["relay_profile"],
                "relay_topology": run["relay_topology"],
                "launcher_thread_id": run["launcher_thread_id"],
                "requested_effort": run["requested_effort"],
                "revision": int(run["revision"]),
                "status": run["status"],
                "current_generation": int(run["current_generation"]),
                "completion_report_sha256": run[
                    "completion_report_sha256"
                ],
            }
            generations: list[dict[str, Any]] = []
            envelopes: list[dict[str, Any]] = []
            intents: list[dict[str, Any]] = []
            receipts: list[dict[str, Any]] = []
            for generation in connection.execute(
                "SELECT * FROM relay_generations WHERE run_id=? "
                "ORDER BY generation",
                (run_id,),
            ):
                generations.append(
                    {
                        "schema_version": "sys4ai.plan-relay-generation.v1",
                        "run_id": generation["run_id"],
                        "generation": int(generation["generation"]),
                        "task_id": generation["task_id"],
                        "task_sha256": generation["task_sha256"],
                        "predecessor_thread_id": generation[
                            "predecessor_thread_id"
                        ],
                        "predecessor_receipt_sha256": generation[
                            "predecessor_receipt_sha256"
                        ],
                        "worker_thread_id": generation["worker_thread_id"],
                        "requested_effort": generation["requested_effort"],
                        "effective_effort": generation["effective_effort"],
                        "status": generation["status"],
                        "handoff_token_sha256": generation[
                            "handoff_token_sha256"
                        ],
                        "envelope_sha256": generation["envelope_sha256"],
                        "invocation_count": int(generation["invocation_count"]),
                        "receipt_sha256": generation["receipt_sha256"],
                        "successor_generation": generation[
                            "successor_generation"
                        ],
                    }
                )
                envelope = _row(
                    connection.execute(
                        "SELECT envelope_json FROM task_envelopes "
                        "WHERE run_id=? AND generation=?",
                        (run_id, generation["generation"]),
                    ).fetchone(),
                    "task envelope",
                )
                envelopes.append(json.loads(envelope["envelope_json"]))
                intent = _row(
                    connection.execute(
                        "SELECT * FROM dispatch_intents "
                        "WHERE run_id=? AND generation=?",
                        (run_id, generation["generation"]),
                    ).fetchone(),
                    "dispatch intent",
                )
                intents.append(
                    {
                        "schema_version": "sys4ai.plan-dispatch-intent.v3",
                        "intent_id": intent["intent_id"],
                        "run_id": intent["run_id"],
                        "generation": int(intent["generation"]),
                        "idempotency_key": intent["idempotency_key"],
                        "create_budget": int(intent["create_budget"]),
                        "attempt_count": int(intent["attempt_count"]),
                        "status": intent["status"],
                        "requested_effort": intent["requested_effort"],
                        "child_thread_id": intent["child_thread_id"],
                        "provider_response_sha256": intent[
                            "provider_response_sha256"
                        ],
                    }
                )
            for receipt in connection.execute(
                "SELECT receipt_json FROM task_receipts WHERE run_id=? "
                "ORDER BY generation",
                (run_id,),
            ):
                receipts.append(json.loads(receipt["receipt_json"]))
            lease = _row(
                connection.execute(
                    "SELECT * FROM relay_leases WHERE run_id=?",
                    (run_id,),
                ).fetchone(),
                "relay lease",
            )
            lease_record = {
                "schema_version": "sys4ai.plan-relay-lease.v1",
                "run_id": lease["run_id"],
                "repository_fingerprint": lease["repository_fingerprint"],
                "holder_kind": lease["holder_kind"],
                "holder_generation": lease["holder_generation"],
                "holder_thread_id": lease["holder_thread_id"],
                "holder_token_sha256": lease["holder_token_sha256"],
                "heartbeat_at": lease["heartbeat_at"],
                "expires_at": lease["expires_at"],
                "released_at": lease["released_at"],
                "steal_authorized": False,
            }
            completion_row = connection.execute(
                "SELECT report_json FROM completion_reports WHERE run_id=?",
                (run_id,),
            ).fetchone()
            mirror_row = connection.execute(
                "SELECT * FROM goal_mirrors WHERE run_id=?",
                (run_id,),
            ).fetchone()
            mirror_record = None
            if mirror_row is not None:
                mirror_record = {
                    "schema_version": "sys4ai.codex-goal-mirror.v1",
                    "run_id": mirror_row["run_id"],
                    "mirror_id": mirror_row["mirror_id"],
                    "may_mark_complete": False,
                    "projection": json.loads(mirror_row["projection_json"]),
                    "projection_sha256": mirror_row["projection_sha256"],
                    "last_error": mirror_row["last_error"],
                    "updated_at": mirror_row["updated_at"],
                }
            value = {
                "schema_version": "sys4ai.plan-relay-chain.v1",
                "run": run_record,
                "generations": generations,
                "envelopes": envelopes,
                "intents": intents,
                "receipts": receipts,
                "lease": lease_record,
                "completion_report": (
                    None
                    if completion_row is None
                    else json.loads(completion_row["report_json"])
                ),
                "goal_mirror": mirror_record,
            }
            value["projection_content_sha256"] = content_sha256(value)
            return value

    def verify_journal(self, run_id: str) -> dict[str, Any]:
        with connect_sqlite(self.path, read_only=True) as connection:
            self._run(connection, run_id)
            prior: str | None = None
            count = 0
            for row in connection.execute("SELECT * FROM relay_journal WHERE run_id=? ORDER BY sequence", (run_id,)):
                count += 1
                if int(row["sequence"]) != count or row["prior_entry_sha256"] != prior:
                    raise RelayIntegrityError("relay journal sequence or prior hash is invalid")
                payload = json.loads(row["payload_json"])
                if content_sha256(payload) != row["payload_sha256"]:
                    raise RelayIntegrityError("relay journal payload hash is invalid")
                expected = content_sha256({
                    "run_id": run_id,
                    "sequence": count,
                    "kind": row["kind"],
                    "payload_sha256": row["payload_sha256"],
                    "prior_entry_sha256": prior,
                    "created_at": row["created_at"],
                })
                if expected != row["entry_sha256"]:
                    raise RelayIntegrityError("relay journal entry hash is invalid")
                prior = expected
            return {"status": "valid", "run_id": run_id, "entry_count": count, "head_sha256": prior}

    def export(self, run_id: str) -> dict[str, Any]:
        with connect_sqlite(self.path, read_only=True) as connection:
            run = self._run(connection, run_id)
            tables = {}
            for table in (
                "relay_runs",
                "relay_generations",
                "task_envelopes",
                "dispatch_intents",
                "task_receipts",
                "relay_leases",
                "completion_reports",
                "goal_mirrors",
                "relay_journal",
            ):
                rows = connection.execute(f"SELECT * FROM {table} WHERE run_id=? ORDER BY rowid", (run_id,)).fetchall()
                tables[table] = [{key: row[key] for key in row.keys()} for row in rows]
            value = {
                "schema_version": EXPORT_SCHEMA,
                "relay_schema_version": SCHEMA_VERSION,
                "run_id": run_id,
                "relay_profile": run["relay_profile"],
                "tables": tables,
            }
            value["export_content_sha256"] = content_sha256(value)
            return value

    def import_export(self, value: Mapping[str, Any]) -> dict[str, Any]:
        """Import one verified recursive export into an empty recursive store."""

        candidate = copy.deepcopy(dict(value))
        supplied_hash = candidate.pop("export_content_sha256", None)
        if supplied_hash != content_sha256(candidate):
            raise RelayIntegrityError("relay export content hash is invalid")
        candidate["export_content_sha256"] = supplied_hash
        if (
            candidate.get("schema_version") != EXPORT_SCHEMA
            or candidate.get("relay_schema_version") != SCHEMA_VERSION
            or candidate.get("relay_profile") != PROFILE
            or not isinstance(candidate.get("tables"), Mapping)
        ):
            raise RecordValidationError("relay export profile/schema is unsupported")
        self.bootstrap()
        table_order = (
            "relay_runs",
            "relay_generations",
            "task_envelopes",
            "dispatch_intents",
            "task_receipts",
            "relay_leases",
            "completion_reports",
            "goal_mirrors",
            "relay_journal",
        )
        tables = candidate["tables"]
        if set(tables) != set(table_order):
            raise RecordValidationError("relay export table set is incomplete or unknown")
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            if connection.execute("SELECT COUNT(*) FROM relay_runs").fetchone()[0]:
                raise RelayConflict("relay import target is not empty")
            for table in table_order:
                rows = tables[table]
                if not isinstance(rows, list):
                    raise RecordValidationError(f"relay export table {table} is not an array")
                for row in rows:
                    if not isinstance(row, Mapping) or not row:
                        raise RecordValidationError(f"relay export table {table} contains an invalid row")
                    columns = list(row)
                    placeholders = ",".join("?" for _ in columns)
                    names = ",".join(columns)
                    connection.execute(
                        f"INSERT INTO {table}({names}) VALUES({placeholders})",
                        tuple(row[column] for column in columns),
                    )
        imported = self.export(str(candidate["run_id"]))
        if imported["export_content_sha256"] != supplied_hash:
            raise RelayIntegrityError("relay import canonical hash differs from source")
        return {
            "status": "imported",
            "run_id": candidate["run_id"],
            "export_content_sha256": supplied_hash,
        }

    def project_goal_mirror(
        self,
        run_id: str,
        *,
        mirror_id: str,
        projection: Mapping[str, Any],
        last_error: str | None = None,
    ) -> dict[str, Any]:
        """Write an advisory UI projection that can never mark completion."""

        _require_nonblank(mirror_id, "mirror_id")
        body = copy.deepcopy(dict(projection))
        timestamp = utc_now()
        projection_hash = content_sha256(body)
        with connect_sqlite(self.path) as connection, immediate_transaction(connection):
            self._run(connection, run_id)
            connection.execute(
                "INSERT INTO goal_mirrors(run_id,mirror_id,may_mark_complete,projection_json,projection_sha256,last_error,updated_at) VALUES(?,?,0,?,?,?,?) "
                "ON CONFLICT(run_id) DO UPDATE SET mirror_id=excluded.mirror_id,may_mark_complete=0,projection_json=excluded.projection_json,projection_sha256=excluded.projection_sha256,last_error=excluded.last_error,updated_at=excluded.updated_at",
                (run_id, mirror_id, _json(body), projection_hash, last_error, timestamp),
            )
        return {
            "status": "advisory_projected" if last_error is None else "advisory_failed",
            "run_id": run_id,
            "mirror_id": mirror_id,
            "may_mark_complete": False,
            "projection_sha256": projection_hash,
            "canonical_state_mutated": False,
        }


def build_successor_prompt(
    *,
    project_root: str,
    database_path: str,
    run_id: str,
    generation: int,
    expected_revision: int,
    current_thread_id: str,
    handoff_token: str,
) -> str:
    """Build the deliberately minimal token-bearing successor prompt."""

    for value, field in (
        (project_root, "project_root"),
        (database_path, "database_path"),
        (run_id, "run_id"),
        (current_thread_id, "current_thread_id"),
        (handoff_token, "handoff_token"),
    ):
        _require_nonblank(value, field)
    return (
        "Invoke the installed continue-implementation-plan-relay skill once.\n"
        f"project_root: {project_root}\n"
        f"relay_database: {database_path}\n"
        f"run_id: {run_id}\n"
        f"generation: {generation}\n"
        f"expected_revision: {expected_revision}\n"
        f"expected_current_thread_id: {current_thread_id}\n"
        f"handoff_token: {handoff_token}\n"
        "Wait read-only until successor_created is recorded, then validate, claim, consume, execute exactly one task, and stop after recording at most one successor.\n"
    )
