"""Transactional SQLite store for canonical implementation-plan state."""

from __future__ import annotations

import copy
import json
import secrets
import sqlite3
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agentjob_runtime.errors import (
    IntegrityError,
    RecordNotFound,
    RecordValidationError,
    SecurityError,
    StateConflict,
)
from agentjob_runtime.goal.model import parse_utc, utc_now
from agentjob_runtime.goal.sqlite_store import (
    CURRENT_SQLITE_SCHEMA_VERSION,
    GoalMutation,
    SQLiteGoalStore,
)
from agentjob_runtime.plan.lifecycle import (
    activate_task,
    apply_task_receipt,
    begin_task_verification,
    consume_task_invocation,
    holder_token_sha256,
    receipt_outcome,
    reserve_task,
    validate_plan_transition,
)
from agentjob_runtime.plan.model import (
    append_plan_journal,
    build_initial_plan_record,
    validate_runtime_plan_record,
)
from agentjob_runtime.plan.scheduler import (
    SelectionResult,
    build_selection_result,
    validate_selection_proof_snapshot,
)
from agentjob_runtime.records.canonical import canonical_json_bytes, content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


PLAN_SCHEMA_VERSION = CURRENT_SQLITE_SCHEMA_VERSION
PLAN_EXPORT_SCHEMA_VERSION = "sys4ai.plan-store-export.v2"
PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION_V1 = (
    "sys4ai.plan-initialization-receipt.v1"
)
PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION = (
    "sys4ai.plan-initialization-receipt.v2"
)
OUTER_HOLDER_KINDS = {
    "coordinator": "launcher",
    "successor_reserved": "successor_reserved",
    "worker": "continuation",
    "quarantined": "quarantined",
}


@dataclass
class PlanMutation:
    """One revision-checked plan-row mutation inside an active transaction."""

    record: dict[str, Any]
    timestamp: str
    _connection: sqlite3.Connection = field(repr=False)
    _store: "SQLitePlanStore" = field(repr=False)
    expected_revision: int
    _outer_mutation: GoalMutation | None = field(
        default=None,
        init=False,
        repr=False,
    )

    def journal(
        self,
        kind: str,
        payload: Mapping[str, Any] | None = None,
    ) -> str:
        body = copy.deepcopy(dict(payload or {}))
        if "timestamp" in body and body["timestamp"] != self.timestamp:
            raise RecordValidationError(
                "plan event payload cannot replace the mutation timestamp"
            )
        body["timestamp"] = self.timestamp
        return append_plan_journal(self.record["journal"], kind, body)

    def event(
        self,
        event_type: str,
        payload: Mapping[str, Any] | None = None,
    ) -> str:
        if not isinstance(event_type, str) or not event_type.strip():
            raise RecordValidationError("plan event_type must be nonblank")
        body = copy.deepcopy(dict(payload or {}))
        if "event_type" in body and body["event_type"] != event_type:
            raise RecordValidationError("plan event payload cannot replace event_type")
        body["event_type"] = event_type
        return self.journal("event", body)

    def add_task_receipt(self, receipt: Mapping[str, Any]) -> str:
        receipt_sha256 = self._store._insert_task_receipt(
            self._connection,
            self.record,
            receipt,
        )
        value = dict(receipt)
        self.journal(
            "task_receipt",
            {
                "receipt_id": value["receipt_id"],
                "receipt_sha256": receipt_sha256,
                "task_id": value["task_identity"]["task_id"],
                "generation": value["relay_identity"]["generation"],
                "disposition": value["disposition"],
            },
        )
        return receipt_sha256

    def reserve_selected_task(
        self,
        proof: Mapping[str, Any],
        *,
        generation: int,
        successor_created: bool,
        expected_outer_revision: int,
        holder_kind: str,
        holder_token: str,
        expires_at: str,
        current_outer_holder_token: str | None = None,
    ) -> str:
        expected = self._store._selection_result(
            self._connection,
            self.record,
        )
        candidate = self._store._require_selection_proof(proof)
        if expected.status != "selected" or expected.selected_task is None:
            raise StateConflict("plan revision has no selectable task")
        if candidate != expected.proof:
            raise StateConflict(
                "selection proof differs from the current canonical snapshot"
            )
        proof_sha256 = self._store._insert_selection_proof(
            self._connection,
            self.record,
            candidate,
            timestamp=self.timestamp,
        )
        self.journal(
            "selection_proof",
            {
                "proof_id": candidate["proof_id"],
                "proof_sha256": proof_sha256,
                "plan_revision": candidate["plan_revision"],
                "outcome": candidate["outcome"],
                "selected_task_id": candidate["selected_task"]["task_id"],
            },
        )
        self.reserve_task(
            task_id=candidate["selected_task"]["task_id"],
            generation=generation,
            successor_created=successor_created,
        )
        self.acquire_plan_lease(
            expected_outer_revision=expected_outer_revision,
            holder_kind=holder_kind,
            holder_token=holder_token,
            expires_at=expires_at,
            current_outer_holder_token=current_outer_holder_token,
        )
        return proof_sha256

    def add_supersession(self, supersession: Mapping[str, Any]) -> str:
        supersession_sha256 = self._store._insert_supersession(
            self._connection,
            self.record,
            supersession,
            timestamp=self.timestamp,
        )
        value = dict(supersession)
        self.journal(
            "supersession",
            {
                "supersession_id": value["supersession_id"],
                "supersession_sha256": supersession_sha256,
                "original_task_id": value["original_task"]["task_id"],
                "replacement_task_ids": [
                    item["task_id"] for item in value["replacement_tasks"]
                ],
            },
        )
        return supersession_sha256

    def add_provider_intent(self, intent: Mapping[str, Any]) -> str:
        intent_sha256 = self._store._insert_provider_intent(
            self._connection,
            self.record,
            intent,
            expected_revision=self.expected_revision,
            timestamp=self.timestamp,
        )
        value = dict(intent)
        self.journal(
            "provider_intent",
            {
                "intent_id": value["intent_id"],
                "intent_sha256": intent_sha256,
                "task_id": value["task_id"],
                "generation": value["generation"],
                "status": value["status"],
            },
        )
        return intent_sha256

    def finalize_provider_intent(self, intent: Mapping[str, Any]) -> str:
        intent_sha256 = self._store._finalize_provider_intent(
            self._connection,
            self.record,
            intent,
            timestamp=self.timestamp,
        )
        value = dict(intent)
        self.journal(
            "provider_intent",
            {
                "intent_id": value["intent_id"],
                "intent_sha256": intent_sha256,
                "task_id": value["task_id"],
                "generation": value["generation"],
                "status": value["status"],
            },
        )
        return intent_sha256

    def record_provider_dispatch(
        self,
        *,
        task_id: str,
        generation: int,
        provider_status: str,
        successor_created: bool,
    ) -> None:
        """Record the single provider effect for one reserved task."""

        if provider_status not in {
            "returned",
            "failed",
            "ambiguous",
            "timeout",
            "duplicate",
        }:
            raise RecordValidationError(
                "plan provider dispatch status is invalid"
            )
        if not isinstance(successor_created, bool):
            raise RecordValidationError(
                "successor_created must be an explicit boolean"
            )
        state = self.record["state"]
        try:
            task = next(
                item
                for item in state["tasks"]
                if item["task_id"] == task_id
            )
        except StopIteration as error:
            raise RecordValidationError(
                f"plan task does not exist: {task_id}"
            ) from error
        if (
            state["phase"] != "task_reserved"
            or state["active_task_id"] != task_id
            or task["status"] != "reserved"
            or task["generation"] != generation
        ):
            raise StateConflict(
                "provider dispatch does not match the reserved task"
            )
        if (
            task["counters"]["provider_creates"] != 0
            or task["counters"]["successor_creates"] != 0
        ):
            raise StateConflict(
                "reserved task provider effect was already recorded"
            )
        expected_successor = provider_status == "returned"
        if successor_created != expected_successor:
            raise RecordValidationError(
                "provider status and successor-created evidence disagree"
            )
        task["counters"]["provider_creates"] = 1
        task["counters"]["successor_creates"] = int(successor_created)
        task["updated_at"] = self.timestamp
        state["counters"]["provider_creates"] = sum(
            item["counters"]["provider_creates"]
            for item in state["tasks"]
        )
        state["counters"]["successor_creates"] = sum(
            item["counters"]["successor_creates"]
            for item in state["tasks"]
        )
        self.event(
            "provider_dispatch_recorded",
            {
                "task_id": task_id,
                "generation": generation,
                "provider_status": provider_status,
                "provider_creates": 1,
                "successor_creates": int(successor_created),
            },
        )

    def record_recovery_adoption(
        self,
        *,
        task_id: str,
        generation: int,
        successor_thread_id: str,
        effective_reasoning_effort: str,
        profile_evidence_ref: str,
        observed_topology_sha256: str,
    ) -> None:
        """Record an adopted candidate without another provider create."""

        state = self.record["state"]
        task = next(
            (
                item
                for item in state["tasks"]
                if item["task_id"] == task_id
            ),
            None,
        )
        if (
            state["phase"] != "task_reserved"
            or state["active_task_id"] != task_id
            or not isinstance(task, Mapping)
            or task["status"] != "reserved"
            or task["generation"] != generation
            or task["counters"]["provider_creates"] != 1
            or task["counters"]["successor_creates"] != 0
            or state.get("lease", {}).get("holder_kind") != "quarantined"
        ):
            raise StateConflict(
                "plan recovery adoption does not match quarantined state"
            )
        task["counters"]["successor_creates"] = 1
        task["updated_at"] = self.timestamp
        state["counters"]["successor_creates"] = sum(
            item["counters"]["successor_creates"]
            for item in state["tasks"]
        )
        self.event(
            "provider_recovery_adopted",
            {
                "task_id": task_id,
                "generation": generation,
                "successor_thread_id_sha256": content_sha256(
                    {"thread_id": successor_thread_id}
                ),
                "effective_reasoning_effort": effective_reasoning_effort,
                "profile_evidence_ref": profile_evidence_ref,
                "observed_topology_sha256": observed_topology_sha256,
                "provider_creates": 1,
                "successor_creates": 1,
            },
        )

    def reserve_task(
        self,
        *,
        task_id: str,
        generation: int,
        successor_created: bool,
    ) -> None:
        reserve_task(
            self.record,
            task_id=task_id,
            generation=generation,
            timestamp=self.timestamp,
            successor_created=successor_created,
        )
        self.event(
            "task_reserved",
            {
                "task_id": task_id,
                "generation": generation,
                "successor_created": successor_created,
            },
        )

    def activate_task(
        self,
        *,
        task_id: str,
        generation: int,
        fingerprint_before: str,
    ) -> None:
        activate_task(
            self.record,
            task_id=task_id,
            generation=generation,
            fingerprint_before=fingerprint_before,
            timestamp=self.timestamp,
        )
        self.event(
            "task_activated",
            {
                "task_id": task_id,
                "generation": generation,
                "fingerprint_before": fingerprint_before,
            },
        )

    def begin_task_verification(
        self,
        *,
        task_id: str,
        generation: int,
        fingerprint_after: str,
        continue_invocations: int,
        agentjobs: int,
        provider_creates: int,
    ) -> None:
        begin_task_verification(
            self.record,
            task_id=task_id,
            generation=generation,
            fingerprint_after=fingerprint_after,
            continue_invocations=continue_invocations,
            agentjobs=agentjobs,
            provider_creates=provider_creates,
            timestamp=self.timestamp,
        )
        self.event(
            "task_verifying",
            {
                "task_id": task_id,
                "generation": generation,
                "fingerprint_after": fingerprint_after,
            },
        )

    def consume_task_invocation(
        self,
        *,
        task_id: str,
        generation: int,
    ) -> None:
        consume_task_invocation(
            self.record,
            task_id=task_id,
            generation=generation,
            timestamp=self.timestamp,
        )
        self.event(
            "task_invocation_consumed",
            {
                "task_id": task_id,
                "generation": generation,
                "continue_invocations": 1,
            },
        )

    def finalize_task(
        self,
        receipt: Mapping[str, Any],
        *,
        guard_reason: str | None = None,
    ) -> tuple[str, bool]:
        _, _, quarantine = receipt_outcome(
            receipt,
            guard_reason=guard_reason,
        )
        receipt_sha256 = self.add_task_receipt(receipt)
        apply_task_receipt(
            self.record,
            receipt,
            receipt_sha256=receipt_sha256,
            guard_reason=guard_reason,
            timestamp=self.timestamp,
        )
        self.event(
            "task_finalized",
            {
                "task_id": receipt["task_identity"]["task_id"],
                "generation": receipt["relay_identity"]["generation"],
                "receipt_id": receipt["receipt_id"],
                "receipt_sha256": receipt_sha256,
                "disposition": receipt["disposition"],
                "guard_reason": guard_reason,
                "lease_disposition": "quarantine" if quarantine else "release",
            },
        )
        return receipt_sha256, quarantine

    def acquire_plan_lease(
        self,
        *,
        expected_outer_revision: int,
        holder_kind: str,
        holder_token: str,
        expires_at: str,
        current_outer_holder_token: str | None = None,
    ) -> dict[str, Any]:
        return self._store._acquire_plan_lease(
            self,
            expected_outer_revision=expected_outer_revision,
            holder_kind=holder_kind,
            holder_token=holder_token,
            expires_at=expires_at,
            current_outer_holder_token=current_outer_holder_token,
        )

    def transfer_plan_lease(
        self,
        *,
        expected_outer_revision: int,
        current_holder_token: str,
        holder_kind: str,
        holder_token: str,
        expires_at: str,
    ) -> dict[str, Any]:
        return self._store._transfer_plan_lease(
            self,
            expected_outer_revision=expected_outer_revision,
            current_holder_token=current_holder_token,
            holder_kind=holder_kind,
            holder_token=holder_token,
            expires_at=expires_at,
        )

    def quarantine_plan_lease(
        self,
        *,
        expected_outer_revision: int,
        current_holder_token: str,
        holder_token: str,
        expires_at: str,
    ) -> dict[str, Any]:
        return self.transfer_plan_lease(
            expected_outer_revision=expected_outer_revision,
            current_holder_token=current_holder_token,
            holder_kind="quarantined",
            holder_token=holder_token,
            expires_at=expires_at,
        )

    def release_plan_lease(
        self,
        *,
        expected_outer_revision: int,
        holder_token: str,
    ) -> None:
        self._store._release_plan_lease(
            self,
            expected_outer_revision=expected_outer_revision,
            holder_token=holder_token,
        )


class SQLitePlanStore:
    """Plan-profile writer over the shared generic goal-state database."""

    def __init__(
        self,
        database_path: str | Path,
        *,
        schema_root: str | Path,
        busy_timeout_ms: int = 5000,
        auto_migrate: bool = True,
        read_only: bool = False,
    ) -> None:
        self.schema_root = Path(schema_root).expanduser().resolve(strict=True)
        if not self.schema_root.is_dir():
            raise RecordValidationError("plan schema root must be a directory")
        self.plan_schema_path = self.schema_root / "implementation-plan.schema.json"
        self.state_schema_path = (
            self.schema_root / "implementation-plan-state.schema.json"
        )
        self.normalization_report_schema_path = (
            self.schema_root / "normalization-report.schema.json"
        )
        self.receipt_schema_path = self.schema_root / "plan-task-receipt.schema.json"
        self.receipt_v2_schema_path = (
            self.schema_root / "plan-task-receipt-v2.schema.json"
        )
        self.supersession_schema_path = (
            self.schema_root / "plan-task-supersession.schema.json"
        )
        self.provider_intent_schema_path = (
            self.schema_root / "provider-intent.schema.json"
        )
        self.provider_intent_v2_schema_path = (
            self.schema_root / "provider-intent-v2.schema.json"
        )
        self.activation_receipt_schema_path = (
            self.schema_root / "plan-activation-receipt.schema.json"
        )
        self.execution_profile_schema_path = (
            self.schema_root / "plan-execution-profile.schema.json"
        )
        self.topology_policy_schema_path = (
            self.schema_root / "repository-topology-policy.schema.json"
        )
        self.selection_proof_schema_path = (
            self.schema_root / "selection-proof.schema.json"
        )
        required_schemas = (
            self.plan_schema_path,
            self.state_schema_path,
            self.normalization_report_schema_path,
            self.receipt_schema_path,
            self.receipt_v2_schema_path,
            self.supersession_schema_path,
            self.provider_intent_schema_path,
            self.provider_intent_v2_schema_path,
            self.activation_receipt_schema_path,
            self.execution_profile_schema_path,
            self.topology_policy_schema_path,
            self.selection_proof_schema_path,
        )
        if any(not path.is_file() for path in required_schemas):
            raise RecordValidationError(
                "plan schema root is missing a required plan-profile schema"
            )
        self.goal_store = SQLiteGoalStore(
            database_path,
            busy_timeout_ms=busy_timeout_ms,
            auto_migrate=auto_migrate,
            read_only=read_only,
            target_schema_version=PLAN_SCHEMA_VERSION,
        )
        self.path = self.goal_store.path
        self.read_only = read_only
        actual_version = self.goal_store.current_schema_version()
        self.database_schema_version = actual_version
        allowed_versions = (
            {3, 4, PLAN_SCHEMA_VERSION}
            if read_only and not auto_migrate
            else {PLAN_SCHEMA_VERSION}
        )
        if actual_version not in allowed_versions:
            raise IntegrityError(
                "plan store schema version is not supported by this access mode",
                details={
                    "database_version": actual_version,
                    "supported_versions": sorted(allowed_versions),
                },
            )

    def _require_profile_record(
        self,
        value: Mapping[str, Any],
        *,
        schema_path: Path,
        content_hash_field: str,
        label: str,
    ) -> dict[str, Any]:
        candidate = copy.deepcopy(dict(value))
        issues = validate_instance(candidate, schema_path)
        if issues:
            raise RecordValidationError(
                f"{label} failed canonical validation",
                details={"findings": format_issues(issues).splitlines()},
            )
        expected_hash = content_sha256(
            {
                key: item
                for key, item in candidate.items()
                if key != content_hash_field
            }
        )
        if candidate.get(content_hash_field) != expected_hash:
            raise RecordValidationError(
                f"{label} content hash does not match canonical bytes"
            )
        if contains_secret(canonical_json_bytes(candidate).decode("utf-8")):
            raise SecurityError(
                f"{label} appears to contain a secret; redact it before persistence"
            )
        return candidate

    def _require_task_receipt(
        self,
        value: Mapping[str, Any],
    ) -> dict[str, Any]:
        schema_path = (
            self.receipt_v2_schema_path
            if value.get("schema_version") == "sys4ai.plan-task-receipt.v2"
            else self.receipt_schema_path
        )
        return self._require_profile_record(
            value,
            schema_path=schema_path,
            content_hash_field="receipt_content_sha256",
            label="plan task receipt",
        )

    def _require_activation_receipt(
        self,
        value: Mapping[str, Any],
    ) -> dict[str, Any]:
        return self._require_profile_record(
            value,
            schema_path=self.activation_receipt_schema_path,
            content_hash_field="receipt_content_sha256",
            label="plan activation receipt",
        )

    def _require_execution_profile(
        self,
        value: Mapping[str, Any],
    ) -> dict[str, Any]:
        return self._require_profile_record(
            value,
            schema_path=self.execution_profile_schema_path,
            content_hash_field="profile_content_sha256",
            label="plan execution profile",
        )

    def _require_topology_policy(
        self,
        value: Mapping[str, Any],
        *,
        require_default_deny: bool,
    ) -> dict[str, Any]:
        policy = copy.deepcopy(dict(value))
        issues = validate_instance(policy, self.topology_policy_schema_path)
        if issues:
            raise RecordValidationError(
                "repository topology policy failed canonical validation",
                details={"findings": format_issues(issues).splitlines()},
            )
        if require_default_deny and policy != {
            "environment_mode": "reuse_bound_checkout",
            "branch_creation_authorized": False,
            "worktree_creation_authorized": False,
            "binding_change_authorized": False,
            "authorization_ref": None,
        }:
            raise RecordValidationError(
                "new plan initialization requires default-deny bound-checkout reuse"
            )
        if contains_secret(canonical_json_bytes(policy).decode("utf-8")):
            raise SecurityError(
                "repository topology policy appears to contain a secret"
            )
        return policy

    def _require_normalization_report(
        self,
        value: Mapping[str, Any],
    ) -> dict[str, Any]:
        report = self._require_profile_record(
            value,
            schema_path=self.normalization_report_schema_path,
            content_hash_field="report_content_sha256",
            label="plan normalization report",
        )
        if report["status"] != "candidate" or report["finalized"] is not True:
            raise RecordValidationError(
                "durable plan initialization requires a finalized candidate report"
            )
        return report

    @staticmethod
    def _require_initialization_receipt(
        value: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(value, Mapping):
            raise RecordValidationError(
                "plan initialization receipt must be an object"
            )
        receipt = copy.deepcopy(dict(value))
        expected_keys = {
            "schema_version",
            "receipt_id",
            "status",
            "plan_identity",
            "normalization_identity",
            "outer_goal_identity",
            "repository_fingerprint",
            "initial_fingerprint",
            "initial_lease",
            "materialized",
            "effect_counts",
            "prior_journal_sha256",
            "next_boundary",
            "finalized_at",
            "finalized",
            "receipt_content_sha256",
        }
        version = receipt.get("schema_version")
        if version == PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION:
            expected_keys.add("activation_identity")
        elif version != PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION_V1:
            raise RecordValidationError(
                "plan initialization receipt schema version is unsupported"
            )
        if set(receipt) != expected_keys:
            raise RecordValidationError(
                "plan initialization receipt fields do not match the canonical contract"
            )
        expected_nested = {
            "plan_identity": {"plan_id", "plan_sha256"},
            "normalization_identity": {
                "report_id",
                "report_content_sha256",
                "source_set_sha256",
            },
            "outer_goal_identity": {
                "goal_id",
                "revision_before",
                "revision_after",
            },
            "initial_lease": {
                "authority",
                "generation",
                "holder_kind",
                "holder_token_sha256",
                "transaction_id",
                "expires_at",
            },
            "materialized": {
                "phase_count",
                "task_count",
                "plan_revision",
                "state_writes",
            },
            "effect_counts": {
                "provider_create_calls",
                "agentjobs_executed",
                "continue_invocations",
            },
        }
        if version == PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION:
            expected_nested["activation_identity"] = {
                "activation_id",
                "activation_receipt_sha256",
                "execution_profile_sha256",
                "repository_topology_policy_sha256",
                "activation_goal_sha256",
                "effective_from_generation",
            }
            expected_nested["effect_counts"] = {
                "provider_create_calls",
                "worker_discussions",
                "agentjobs_executed",
                "continue_invocations",
                "task_reservations",
                "branch_creations",
                "worktree_creations",
            }
        for field_name, keys in expected_nested.items():
            item = receipt.get(field_name)
            if not isinstance(item, Mapping) or set(item) != keys:
                raise RecordValidationError(
                    f"plan initialization receipt {field_name} is malformed"
                )
        if (
            receipt["status"] != "initialized"
            or receipt["finalized"] is not True
            or receipt["next_boundary"] != "reserve_first_task"
            or receipt["initial_lease"]["authority"] != "outer_worktree"
            or receipt["initial_lease"]["holder_kind"]
            not in {"launcher", "continuation"}
        ):
            raise RecordValidationError(
                "plan initialization receipt lifecycle fields are invalid"
            )
        expected_effects = (
            {
                "provider_create_calls": 0,
                "worker_discussions": 0,
                "agentjobs_executed": 0,
                "continue_invocations": 0,
                "task_reservations": 0,
                "branch_creations": 0,
                "worktree_creations": 0,
            }
            if version == PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION
            else {
                "provider_create_calls": 0,
                "agentjobs_executed": 0,
                "continue_invocations": 0,
            }
        )
        if receipt["effect_counts"] != expected_effects:
            raise RecordValidationError(
                "plan initialization receipt contains an unexpected effect"
            )
        if (
            receipt["materialized"]["plan_revision"] != 1
            or receipt["materialized"]["state_writes"] != 1
            or receipt["materialized"]["phase_count"] < 1
            or receipt["materialized"]["task_count"] < 1
        ):
            raise RecordValidationError(
                "plan initialization receipt materialization counts are invalid"
            )
        outer_identity = receipt["outer_goal_identity"]
        if (
            isinstance(outer_identity["revision_before"], bool)
            or not isinstance(outer_identity["revision_before"], int)
            or outer_identity["revision_after"]
            != outer_identity["revision_before"] + 1
        ):
            raise RecordValidationError(
                "plan initialization receipt outer revisions are invalid"
            )
        for field_name in (
            "repository_fingerprint",
            "initial_fingerprint",
            "prior_journal_sha256",
            "receipt_content_sha256",
        ):
            candidate = receipt.get(field_name)
            if (
                not isinstance(candidate, str)
                or len(candidate) != 64
                or any(character not in "0123456789abcdef" for character in candidate)
            ):
                raise RecordValidationError(
                    f"plan initialization receipt {field_name} is invalid"
                )
        token_hash = receipt["initial_lease"]["holder_token_sha256"]
        if (
            not isinstance(token_hash, str)
            or len(token_hash) != 64
            or any(character not in "0123456789abcdef" for character in token_hash)
        ):
            raise RecordValidationError(
                "plan initialization receipt holder-token hash is invalid"
            )
        parse_utc(str(receipt["initial_lease"]["expires_at"]))
        parse_utc(str(receipt["finalized_at"]))
        if version == PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION:
            activation = receipt["activation_identity"]
            for field_name in (
                "activation_receipt_sha256",
                "execution_profile_sha256",
                "repository_topology_policy_sha256",
                "activation_goal_sha256",
            ):
                candidate = activation[field_name]
                if (
                    not isinstance(candidate, str)
                    or len(candidate) != 64
                    or any(
                        character not in "0123456789abcdef"
                        for character in candidate
                    )
                ):
                    raise RecordValidationError(
                        "plan initialization receipt activation identity "
                        f"{field_name} is invalid"
                    )
            if (
                not isinstance(activation["activation_id"], str)
                or not activation["activation_id"].strip()
                or activation["effective_from_generation"] != 1
            ):
                raise RecordValidationError(
                    "plan initialization receipt activation identity is invalid"
                )
        expected_hash = content_sha256(
            {
                key: item
                for key, item in receipt.items()
                if key != "receipt_content_sha256"
            }
        )
        if receipt["receipt_content_sha256"] != expected_hash:
            raise RecordValidationError(
                "plan initialization receipt content hash does not match "
                "canonical bytes"
            )
        if contains_secret(canonical_json_bytes(receipt).decode("utf-8")):
            raise SecurityError(
                "plan initialization receipt appears to contain a secret"
            )
        return receipt

    def _require_supersession(
        self,
        value: Mapping[str, Any],
    ) -> dict[str, Any]:
        return self._require_profile_record(
            value,
            schema_path=self.supersession_schema_path,
            content_hash_field="supersession_content_sha256",
            label="plan task supersession",
        )

    def _require_provider_intent(
        self,
        value: Mapping[str, Any],
    ) -> dict[str, Any]:
        schema_path = (
            self.provider_intent_v2_schema_path
            if value.get("schema_version") == "sys4ai.plan-provider-intent.v2"
            else self.provider_intent_schema_path
        )
        return self._require_profile_record(
            value,
            schema_path=schema_path,
            content_hash_field="intent_content_sha256",
            label="plan provider intent",
        )

    def _require_selection_proof(
        self,
        value: Mapping[str, Any],
    ) -> dict[str, Any]:
        proof = self._require_profile_record(
            value,
            schema_path=self.selection_proof_schema_path,
            content_hash_field="proof_content_sha256",
            label="plan selection proof",
        )
        validate_selection_proof_snapshot(proof)
        return proof

    def connect(self) -> sqlite3.Connection:
        return self.goal_store.connect()

    def _outer_mutation(
        self,
        mutation: PlanMutation,
        *,
        expected_outer_revision: int,
    ) -> GoalMutation:
        current = mutation._outer_mutation
        if current is not None:
            if current.original_revision != expected_outer_revision:
                raise StateConflict(
                    "outer goal revision changed within the plan transaction"
                )
            return current
        current = self.goal_store._prepare_mutation(
            mutation._connection,
            mutation.record["outer_goal_id"],
            expected_revision=expected_outer_revision,
            timestamp=mutation.timestamp,
        )
        if current.record["repository_binding"] != mutation.record[
            "repository_binding"
        ]:
            raise StateConflict(
                "plan repository binding differs from its outer goal"
            )
        mutation._outer_mutation = current
        return current

    @staticmethod
    def _active_plan_lease(
        connection: sqlite3.Connection,
        plan_id: str,
    ) -> sqlite3.Row | None:
        return connection.execute(
            "SELECT * FROM plan_leases "
            "WHERE plan_id=? AND lease_state='active'",
            (plan_id,),
        ).fetchone()

    def _require_active_plan_lease(
        self,
        mutation: PlanMutation,
        outer: GoalMutation,
        *,
        holder_token: str,
    ) -> sqlite3.Row:
        state_lease = mutation.record["state"]["lease"]
        row = self._active_plan_lease(
            mutation._connection,
            mutation.record["plan_id"],
        )
        outer_lease = outer.record["state"].get("active_lease")
        token_hash = holder_token_sha256(holder_token)
        if state_lease is None or row is None or outer_lease is None:
            raise StateConflict("plan does not have a complete active lease")
        if (
            state_lease["holder_token_hash"] != token_hash
            or row["holder_token_sha256"] != token_hash
            or outer_lease["holder_token"] != holder_token
            or state_lease["transaction_id"] != row["transaction_id"]
            or row["outer_lease_transaction_id"]
            != outer_lease["transaction_id"]
            or OUTER_HOLDER_KINDS[state_lease["holder_kind"]]
            != outer_lease["holder_kind"]
        ):
            raise StateConflict("plan lease holder identity does not match")
        return row

    @staticmethod
    def _require_lease_expiry(timestamp: str, expires_at: str) -> None:
        if parse_utc(expires_at) <= parse_utc(timestamp):
            raise RecordValidationError(
                "plan lease expiration must be later than acquisition"
            )

    def _insert_plan_lease(
        self,
        mutation: PlanMutation,
        *,
        outer_lease: Mapping[str, Any],
        holder_kind: str,
        holder_token: str,
    ) -> dict[str, Any]:
        state = mutation.record["state"]
        task_id = state["active_task_id"]
        if task_id is None:
            raise StateConflict("plan lease requires an active task identity")
        task = next(
            (
                item
                for item in state["tasks"]
                if item["task_id"] == task_id
            ),
            None,
        )
        if task is None or task["generation"] is None:
            raise StateConflict("plan lease task generation is unavailable")
        transaction_id = secrets.token_hex(16)
        token_hash = holder_token_sha256(holder_token)
        lease = {
            "generation": task["generation"],
            "task_id": task_id,
            "holder_kind": holder_kind,
            "holder_token_hash": token_hash,
            "transaction_id": transaction_id,
            "repository_fingerprint": mutation.record[
                "repository_fingerprint"
            ],
            "acquired_at": outer_lease["acquired_at"],
            "heartbeat_at": outer_lease["heartbeat_at"],
            "expires_at": outer_lease["expires_at"],
        }
        mutation._connection.execute(
            """
            INSERT INTO plan_leases(
                plan_id, task_id, generation, holder_kind,
                holder_token_sha256, transaction_id,
                outer_lease_transaction_id, repository_fingerprint,
                acquired_at, heartbeat_at, expires_at,
                lease_state, released_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', NULL)
            """,
            (
                mutation.record["plan_id"],
                task_id,
                task["generation"],
                holder_kind,
                token_hash,
                transaction_id,
                outer_lease["transaction_id"],
                mutation.record["repository_fingerprint"],
                outer_lease["acquired_at"],
                outer_lease["heartbeat_at"],
                outer_lease["expires_at"],
            ),
        )
        state["lease"] = lease
        return lease

    def _acquire_plan_lease(
        self,
        mutation: PlanMutation,
        *,
        expected_outer_revision: int,
        holder_kind: str,
        holder_token: str,
        expires_at: str,
        current_outer_holder_token: str | None,
    ) -> dict[str, Any]:
        if holder_kind not in {
            "coordinator",
            "successor_reserved",
            "worker",
        }:
            raise RecordValidationError(
                "initial plan lease holder kind is invalid"
            )
        self._require_lease_expiry(mutation.timestamp, expires_at)
        outer = self._outer_mutation(
            mutation,
            expected_outer_revision=expected_outer_revision,
        )
        if (
            mutation.record["state"]["lease"] is not None
            or self._active_plan_lease(
                mutation._connection,
                mutation.record["plan_id"],
            )
            is not None
        ):
            raise StateConflict("plan already has an active lease")
        outer_prior = outer.record["state"].get("active_lease")
        if outer_prior is None and current_outer_holder_token is not None:
            raise StateConflict("outer goal does not have the claimed lease")
        allowed_outer_generations = {
            mutation.record["state"]["current_generation"],
            mutation.record["state"]["current_generation"] - 1,
        }
        if outer_prior is not None and (
            current_outer_holder_token is None
            or outer_prior["holder_token"] != current_outer_holder_token
            or outer_prior["generation"] not in allowed_outer_generations
        ):
            raise StateConflict(
                "outer goal lease identity does not permit plan acquisition"
            )
        outer_lease = outer.replace_lease(
            generation=mutation.record["state"]["current_generation"],
            holder_kind=OUTER_HOLDER_KINDS[holder_kind],
            holder_token=holder_token,
            expires_at=expires_at,
        )
        lease = self._insert_plan_lease(
            mutation,
            outer_lease=outer_lease,
            holder_kind=holder_kind,
            holder_token=holder_token,
        )
        payload = {
            "plan_id": mutation.record["plan_id"],
            "task_id": lease["task_id"],
            "generation": lease["generation"],
            "holder_kind": holder_kind,
            "plan_lease_transaction_id": lease["transaction_id"],
            "outer_lease_transaction_id": outer_lease["transaction_id"],
        }
        outer.event("plan_lease_acquired", payload)
        mutation.event("plan_lease_acquired", payload)
        return copy.deepcopy(lease)

    def _transfer_plan_lease(
        self,
        mutation: PlanMutation,
        *,
        expected_outer_revision: int,
        current_holder_token: str,
        holder_kind: str,
        holder_token: str,
        expires_at: str,
    ) -> dict[str, Any]:
        if holder_kind not in OUTER_HOLDER_KINDS:
            raise RecordValidationError("plan lease holder kind is invalid")
        self._require_lease_expiry(mutation.timestamp, expires_at)
        outer = self._outer_mutation(
            mutation,
            expected_outer_revision=expected_outer_revision,
        )
        prior = self._require_active_plan_lease(
            mutation,
            outer,
            holder_token=current_holder_token,
        )
        mutation._connection.execute(
            "UPDATE plan_leases SET lease_state='released', released_at=? "
            "WHERE lease_id=? AND lease_state='active'",
            (mutation.timestamp, prior["lease_id"]),
        )
        outer_lease = outer.replace_lease(
            generation=mutation.record["state"]["current_generation"],
            holder_kind=OUTER_HOLDER_KINDS[holder_kind],
            holder_token=holder_token,
            expires_at=expires_at,
        )
        lease = self._insert_plan_lease(
            mutation,
            outer_lease=outer_lease,
            holder_kind=holder_kind,
            holder_token=holder_token,
        )
        event_type = (
            "plan_lease_quarantined"
            if holder_kind == "quarantined"
            else "plan_lease_transferred"
        )
        if holder_kind == "quarantined":
            outer.record["state"]["phase"] = "recovery_pending"
            outer.record["state"]["terminal_reason"] = (
                mutation.record["state"]["terminal_reason"]
                or "Plan lease quarantined for protected recovery."
            )
        elif prior["holder_kind"] == "quarantined":
            outer.record["state"]["phase"] = "successor_created"
            outer.record["state"]["terminal_reason"] = None
        payload = {
            "plan_id": mutation.record["plan_id"],
            "task_id": lease["task_id"],
            "generation": lease["generation"],
            "holder_kind": holder_kind,
            "prior_plan_lease_transaction_id": prior["transaction_id"],
            "plan_lease_transaction_id": lease["transaction_id"],
            "outer_lease_transaction_id": outer_lease["transaction_id"],
        }
        outer.event(event_type, payload)
        mutation.event(event_type, payload)
        return copy.deepcopy(lease)

    def _release_plan_lease(
        self,
        mutation: PlanMutation,
        *,
        expected_outer_revision: int,
        holder_token: str,
    ) -> None:
        outer = self._outer_mutation(
            mutation,
            expected_outer_revision=expected_outer_revision,
        )
        prior = self._require_active_plan_lease(
            mutation,
            outer,
            holder_token=holder_token,
        )
        mutation._connection.execute(
            "UPDATE plan_leases SET lease_state='released', released_at=? "
            "WHERE lease_id=? AND lease_state='active'",
            (mutation.timestamp, prior["lease_id"]),
        )
        outer.release_lease()
        mutation.record["state"]["lease"] = None
        payload = {
            "plan_id": mutation.record["plan_id"],
            "task_id": prior["task_id"],
            "generation": prior["generation"],
            "plan_lease_transaction_id": prior["transaction_id"],
            "outer_lease_transaction_id": prior[
                "outer_lease_transaction_id"
            ],
        }
        outer.event("plan_lease_released", payload)
        mutation.event("plan_lease_released", payload)

    def integrity_check(self) -> dict[str, Any]:
        result = self.goal_store.integrity_check()
        if result["status"] != "pass":
            return result
        try:
            for item in self.list_plans():
                self.load_plan(item["plan_id"])
        except (IntegrityError, RecordValidationError):
            result["status"] = "fail"
            result["plan_parity"] = "fail"
        else:
            result["plan_parity"] = "pass"
        return result

    @staticmethod
    def _parse_canonical_json(value: str, *, label: str) -> Any:
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise IntegrityError(f"{label} is not valid JSON") from error
        if canonical_json_bytes(parsed).decode("utf-8") != value:
            raise IntegrityError(f"{label} is not canonical JSON")
        return parsed

    @classmethod
    def _parse_canonical_object(
        cls,
        value: str,
        *,
        label: str,
    ) -> dict[str, Any]:
        parsed = cls._parse_canonical_json(value, label=label)
        if not isinstance(parsed, dict):
            raise IntegrityError(f"{label} must be a JSON object")
        return parsed

    @staticmethod
    def _base_definitions(record: Mapping[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "task_id": str(task["task_id"]),
                "task_sha256": str(task["task_sha256"]),
                "phase_id": str(task["phase_id"]),
                "canonical_position": position,
                "origin_kind": "canonical",
                "task_json": copy.deepcopy(dict(task)),
                "depends_on": list(task["depends_on"]),
            }
            for position, task in enumerate(record["plan"]["tasks"])
        ]

    @staticmethod
    def _assert_rows(
        connection: sqlite3.Connection,
        *,
        query: str,
        parameters: tuple[Any, ...],
        columns: tuple[str, ...],
        expected: list[tuple[Any, ...]],
        label: str,
    ) -> None:
        actual = [
            tuple(row[column] for column in columns)
            for row in connection.execute(query, parameters)
        ]
        if actual != expected:
            raise IntegrityError(
                f"plan normalized child projection mismatch: {label}",
                details={
                    "label": label,
                    "expected_count": len(expected),
                    "actual_count": len(actual),
                },
            )

    @staticmethod
    def _result_projection(values: list[str]) -> str:
        if not values:
            return "not_applicable"
        if "fail" in values:
            return "fail"
        if any(value in {"indeterminate", "skipped"} for value in values):
            return "indeterminate"
        if all(value == "pass" for value in values):
            return "pass"
        return "indeterminate"

    def _receipt_projection(
        self,
        receipt: Mapping[str, Any],
    ) -> dict[str, Any]:
        direct = receipt["direct_evidence"]
        return {
            "acceptance_status": self._result_projection(
                [str(item["status"]) for item in direct["acceptance_results"]]
            ),
            "validator_status": self._result_projection(
                [str(item["status"]) for item in direct["validator_results"]]
            ),
            "checkpoint_status": str(direct["checkpoint"]["status"]),
        }

    def _validate_v2_receipt_profile(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        receipt: Mapping[str, Any],
    ) -> None:
        if receipt.get("schema_version") != "sys4ai.plan-task-receipt.v2":
            return
        generation = int(receipt["relay_identity"]["generation"])
        history = self._activation_history(
            connection,
            str(record["plan_id"]),
        )
        applicable = [
            item
            for item in history
            if int(item["effective_from_generation"]) <= generation
        ]
        if not applicable:
            raise RecordValidationError(
                "profile-aware task receipt has no applicable activation"
            )
        activation = applicable[-1]
        from agentjob_runtime.plan.activation import (
            execution_profile_from_receipt,
        )

        profile = execution_profile_from_receipt(activation)
        profile_evidence = receipt["activation_profile_evidence"]
        topology_evidence = receipt["topology_evidence"]
        intent_row = connection.execute(
            "SELECT record_json FROM plan_provider_intents "
            "WHERE plan_id=? AND generation=?",
            (record["plan_id"], generation),
        ).fetchone()
        if intent_row is None:
            raise RecordValidationError(
                "profile-aware task receipt lacks provider evidence"
            )
        intent = self._require_provider_intent(
            self._parse_canonical_object(
                str(intent_row["record_json"]),
                label="task receipt provider intent",
            )
        )
        thread_id = receipt["relay_identity"]["worker_thread_id"]
        recovery_matches = [
            entry
            for entry in record["journal"]
            if entry["kind"] == "event"
            and entry["payload"].get("event_type")
            == "provider_recovery_adopted"
            and entry["payload"].get("generation") == generation
            and entry["payload"].get("successor_thread_id_sha256")
            == content_sha256({"thread_id": thread_id})
        ]
        provider_match = (
            intent["status"] == "returned"
            and intent["returned_thread_id"] == thread_id
            and intent["profile_evidence_ref"]
            == profile_evidence["provider_evidence_ref"]
        ) or (
            intent["status"] in {"ambiguous", "timeout", "duplicate"}
            and len(recovery_matches) == 1
            and recovery_matches[0]["payload"].get(
                "profile_evidence_ref"
            )
            == profile_evidence["provider_evidence_ref"]
        )
        if (
            record.get("runtime_profile_version") != 2
            or profile_evidence["activation_receipt_sha256"]
            != content_sha256(activation)
            or profile_evidence["execution_profile_sha256"]
            != content_sha256(profile)
            or profile_evidence["requested_reasoning_effort"]
            != profile["reasoning_effort"]
            or profile_evidence["observed_effective_reasoning_effort"]
            != profile["reasoning_effort"]
            or profile_evidence["provider_id"] != intent["provider_id"]
            or profile_evidence["thread_id"] != thread_id
            or not provider_match
            or topology_evidence["repository_binding_sha256"]
            != record["repository_binding_sha256"]
            or topology_evidence["repository_topology_policy_sha256"]
            != content_sha256(record["repository_topology_policy"])
            or receipt["execution"]["provider_create_calls"] != 1
            or receipt["execution"]["successor_creates"] != 1
        ):
            raise RecordValidationError(
                "plan task receipt profile or topology evidence is not canonical"
            )

    def _load_receipt_records(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        definitions: Mapping[str, Mapping[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        by_task: dict[str, dict[str, Any]] = {}
        valid_plan_hashes = {
            str(record["plan_sha256"]),
            str(record["effective_plan_sha256"]),
        }
        for row in connection.execute(
            "SELECT * FROM plan_receipts WHERE plan_id=? "
            "ORDER BY finalized_at, receipt_id",
            (record["plan_id"],),
        ):
            receipt = self._require_task_receipt(
                self._parse_canonical_object(
                    str(row["record_json"]),
                    label=f"plan receipt {row['receipt_id']}",
                )
            )
            receipt_sha256 = content_sha256(receipt)
            plan_identity = receipt["plan_identity"]
            task_identity = receipt["task_identity"]
            relay_identity = receipt["relay_identity"]
            task_id = str(task_identity["task_id"])
            definition = definitions.get(task_id)
            projection = self._receipt_projection(receipt)
            self._validate_v2_receipt_profile(
                connection,
                record,
                receipt,
            )
            if (
                row["receipt_kind"] != "task"
                or row["receipt_id"] != receipt["receipt_id"]
                or row["task_id"] != task_id
                or row["phase_id"] is not None
                or row["generation"] != relay_identity["generation"]
                or row["disposition"] != receipt["disposition"]
                or row["reason_code"] != receipt["reason_code"]
                or row["acceptance_status"] != projection["acceptance_status"]
                or row["validator_status"] != projection["validator_status"]
                or row["checkpoint_status"] != projection["checkpoint_status"]
                or row["receipt_sha256"] != receipt_sha256
                or row["finalized"] != 1
                or row["finalized_at"] != receipt["finished_at"]
                or plan_identity["plan_id"] != record["plan_id"]
                or plan_identity["plan_sha256"] not in valid_plan_hashes
                or definition is None
                or task_identity["task_sha256"] != definition["task_sha256"]
                or plan_identity["phase_id"] != definition["phase_id"]
            ):
                raise IntegrityError(
                    "plan receipt canonical/normalized identity mismatch",
                    details={"receipt_id": receipt["receipt_id"]},
                )
            if task_id in by_task:
                raise IntegrityError("plan has duplicate task receipt identity")
            by_task[task_id] = {
                "record": receipt,
                "receipt_sha256": receipt_sha256,
            }
        return by_task

    def _replacement_definitions(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        definitions = {
            item["task_id"]: item for item in self._base_definitions(record)
        }
        positions = {
            int(item["canonical_position"]): item["task_id"]
            for item in definitions.values()
        }
        pending = list(
            connection.execute(
                "SELECT rowid AS insertion_order, * FROM plan_supersessions "
                "WHERE plan_id=? ORDER BY insertion_order",
                (record["plan_id"],),
            )
        )
        replacement_definitions: list[dict[str, Any]] = []
        supersession_records: list[dict[str, Any]] = []
        valid_plan_hashes = {
            str(record["plan_sha256"]),
            str(record["effective_plan_sha256"]),
        }
        disposition_by_terminal = {
            "replan_required": "replan_required",
            "blocked": "blocked",
            "validation_failed": "validation_failed",
            "human_gate_required": "human_gate_required",
        }
        while pending:
            progressed = False
            for row in list(pending):
                supersession = self._require_supersession(
                    self._parse_canonical_object(
                        str(row["record_json"]),
                        label=f"plan supersession {row['supersession_id']}",
                    )
                )
                original = supersession["original_task"]
                original_id = str(original["task_id"])
                original_definition = definitions.get(original_id)
                if original_definition is None:
                    continue
                pending.remove(row)
                progressed = True
                supersession_sha256 = content_sha256(supersession)
                if (
                    row["supersession_id"] != supersession["supersession_id"]
                    or row["plan_id"] != supersession["plan_id"]
                    or row["original_task_id"] != original_id
                    or row["original_task_sha256"] != original["task_sha256"]
                    or row["original_receipt_id"] != original["receipt_id"]
                    or row["replacement_graph_sha256"]
                    != supersession["replacement_graph_sha256"]
                    or row["reason_code"] != supersession["reason_code"]
                    or row["supersession_sha256"] != supersession_sha256
                    or row["finalized"] != 1
                ):
                    raise IntegrityError(
                        "plan supersession canonical/normalized identity mismatch",
                        details={"supersession_id": supersession["supersession_id"]},
                    )
                if (
                    supersession["plan_id"] != record["plan_id"]
                    or supersession["plan_sha256"] not in valid_plan_hashes
                    or original["task_sha256"]
                    != original_definition["task_sha256"]
                ):
                    raise IntegrityError("plan supersession authority mismatch")
                receipt_row = connection.execute(
                    "SELECT record_json, receipt_sha256, task_id FROM plan_receipts "
                    "WHERE receipt_id=? AND plan_id=?",
                    (original["receipt_id"], record["plan_id"]),
                ).fetchone()
                if receipt_row is None:
                    raise IntegrityError("plan supersession original receipt is missing")
                receipt = self._require_task_receipt(
                    self._parse_canonical_object(
                        str(receipt_row["record_json"]),
                        label="supersession original receipt",
                    )
                )
                if (
                    receipt_row["receipt_sha256"] != original["receipt_sha256"]
                    or receipt_row["task_id"] != original_id
                    or receipt["task_identity"]["task_sha256"]
                    != original["task_sha256"]
                    or receipt["relay_identity"]["generation"]
                    != original["generation"]
                    or receipt["disposition"]
                    != disposition_by_terminal[original["terminal_status"]]
                ):
                    raise IntegrityError(
                        "plan supersession does not preserve its exact original receipt"
                    )
                replacements = list(supersession["replacement_tasks"])
                graph_basis = [
                    {
                        "task_id": item["task_id"],
                        "task_sha256": item["task_sha256"],
                        "depends_on": item["depends_on"],
                        "canonical_position": item["canonical_position"],
                    }
                    for item in replacements
                ]
                if supersession["replacement_graph_sha256"] != content_sha256(
                    graph_basis
                ):
                    raise IntegrityError("plan supersession replacement graph hash mismatch")
                replacement_ids = [str(item["task_id"]) for item in replacements]
                if (
                    len(set(replacement_ids)) != len(replacement_ids)
                    or original_id in replacement_ids
                    or any(task_id in definitions for task_id in replacement_ids)
                ):
                    raise IntegrityError(
                        "plan supersession replacement task identity is duplicated"
                    )
                replacement_id_set = set(replacement_ids)
                allowed_dependencies = set(definitions) | replacement_id_set
                for item in replacements:
                    task_id = str(item["task_id"])
                    position = int(item["canonical_position"])
                    dependencies = [str(value) for value in item["depends_on"]]
                    if (
                        position in positions
                        or task_id in dependencies
                        or any(value not in allowed_dependencies for value in dependencies)
                    ):
                        raise IntegrityError(
                            "plan supersession replacement definition is invalid"
                        )
                    definition = {
                        "task_id": task_id,
                        "task_sha256": str(item["task_sha256"]),
                        "phase_id": original_definition["phase_id"],
                        "canonical_position": position,
                        "origin_kind": "replacement",
                        "task_json": copy.deepcopy(dict(item)),
                        "depends_on": dependencies,
                    }
                    definitions[task_id] = definition
                    positions[position] = task_id
                    replacement_definitions.append(definition)
                mapped_ids = {
                    str(task_id)
                    for mapping in supersession["acceptance_mapping"]
                    for task_id in mapping["replacement_task_ids"]
                }
                if not mapped_ids <= replacement_id_set:
                    raise IntegrityError(
                        "plan supersession acceptance mapping names an unknown replacement"
                    )
                expected_replacements = [
                    (
                        supersession["supersession_id"],
                        record["plan_id"],
                        item["task_id"],
                        position,
                    )
                    for position, item in enumerate(replacements)
                ]
                self._assert_rows(
                    connection,
                    query=(
                        "SELECT supersession_id, plan_id, replacement_task_id, "
                        "replacement_position FROM plan_supersession_replacements "
                        "WHERE supersession_id=? ORDER BY replacement_position"
                    ),
                    parameters=(supersession["supersession_id"],),
                    columns=(
                        "supersession_id",
                        "plan_id",
                        "replacement_task_id",
                        "replacement_position",
                    ),
                    expected=expected_replacements,
                    label="supersession replacements",
                )
                expected_acceptance = sorted(
                    (
                        supersession["supersession_id"],
                        mapping["criterion_id"],
                        task_id,
                        mapping["shared_gate_ref"],
                    )
                    for mapping in supersession["acceptance_mapping"]
                    for task_id in mapping["replacement_task_ids"]
                )
                self._assert_rows(
                    connection,
                    query=(
                        "SELECT supersession_id, criterion_id, replacement_task_id, "
                        "shared_gate_ref FROM plan_supersession_acceptance "
                        "WHERE supersession_id=? "
                        "ORDER BY criterion_id, replacement_task_id"
                    ),
                    parameters=(supersession["supersession_id"],),
                    columns=(
                        "supersession_id",
                        "criterion_id",
                        "replacement_task_id",
                        "shared_gate_ref",
                    ),
                    expected=expected_acceptance,
                    label="supersession acceptance",
                )
                supersession_records.append(supersession)
            if not progressed:
                raise IntegrityError(
                    "plan supersession chain names an unknown original task"
                )
        replacement_graph = {
            item["task_id"]: [
                dependency
                for dependency in item["depends_on"]
                if dependency in {entry["task_id"] for entry in replacement_definitions}
            ]
            for item in replacement_definitions
        }
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(task_id: str) -> None:
            if task_id in visiting:
                raise IntegrityError("plan supersession replacement graph has a cycle")
            if task_id in visited:
                return
            visiting.add(task_id)
            for dependency in replacement_graph.get(task_id, []):
                visit(dependency)
            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in sorted(replacement_graph):
            visit(task_id)
        return replacement_definitions, supersession_records

    def _load_provider_intents(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        definitions: Mapping[str, Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        valid_plan_hashes = {
            str(record["plan_sha256"]),
            str(record["effective_plan_sha256"]),
        }
        activation_history = self._activation_history(
            connection,
            str(record["plan_id"]),
        )
        from agentjob_runtime.plan.activation import (
            execution_profile_from_receipt,
        )
        for row in connection.execute(
            "SELECT * FROM plan_provider_intents WHERE plan_id=? "
            "ORDER BY generation, intent_id",
            (record["plan_id"],),
        ):
            intent = self._require_provider_intent(
                self._parse_canonical_object(
                    str(row["record_json"]),
                    label=f"plan provider intent {row['intent_id']}",
                )
            )
            intent_sha256 = content_sha256(intent)
            task_id = str(intent["task_id"])
            definition = definitions.get(task_id)
            applicable_activations = [
                item
                for item in activation_history
                if int(item["effective_from_generation"])
                <= int(intent["generation"])
            ]
            applicable_profile = (
                execution_profile_from_receipt(
                    applicable_activations[-1]
                )
                if applicable_activations
                else None
            )
            if (
                row["intent_id"] != intent["intent_id"]
                or row["task_id"] != task_id
                or row["task_sha256"] != intent["task_sha256"]
                or row["generation"] != intent["generation"]
                or row["provider_id"] != intent["provider_id"]
                or row["idempotency_key"] != intent["idempotency_key"]
                or row["handoff_token_sha256"] != intent["handoff_token_sha256"]
                or row["predecessor_thread_id"]
                != intent["predecessor_thread_id"]
                or row["expected_revision"] != intent["expected_revision"]
                or row["repository_fingerprint"]
                != intent["repository_fingerprint"]
                or row["status"] != intent["status"]
                or row["provider_create_budget"]
                != intent["provider_create_budget"]
                or row["create_attempts"] != intent["create_attempts"]
                or row["returned_thread_id"] != intent["returned_thread_id"]
                or row["provider_response_sha256"]
                != intent["provider_response_sha256"]
                or row["retry_authorized"] != int(intent["retry_authorized"])
                or row["intent_sha256"] != intent_sha256
                or row["finalized"] != int(intent["finalized"])
                or row["created_at"] != intent["created_at"]
                or intent["plan_id"] != record["plan_id"]
                or intent["plan_sha256"] not in valid_plan_hashes
                or definition is None
                or intent["task_sha256"] != definition["task_sha256"]
                or intent["repository_fingerprint"]
                != record["state"]["repository_fingerprint"]
                or intent["expected_revision"] > record["state"]["revision"]
                or intent["generation"] > record["state"]["current_generation"] + 1
                or (
                    intent["returned_thread_id"] is not None
                    and intent["returned_thread_id"]
                    == intent["predecessor_thread_id"]
                )
                or (
                    intent["schema_version"]
                    == "sys4ai.plan-provider-intent.v2"
                    and (
                        record.get("runtime_profile_version") != 2
                        or not isinstance(applicable_profile, Mapping)
                        or intent["execution_profile_sha256"]
                        != content_sha256(applicable_profile)
                        or intent["requested_reasoning_effort"]
                        != applicable_profile["reasoning_effort"]
                        or intent["repository_binding_sha256"]
                        != record["repository_binding_sha256"]
                        or row["execution_profile_sha256"]
                        != intent["execution_profile_sha256"]
                        or row["requested_reasoning_effort"]
                        != intent["requested_reasoning_effort"]
                        or row["effective_reasoning_effort"]
                        != intent["effective_reasoning_effort"]
                        or row["profile_verification_status"]
                        != intent["profile_verification_status"]
                        or row["profile_evidence_ref"]
                        != intent["profile_evidence_ref"]
                        or row["environment_mode"]
                        != intent["environment_mode"]
                        or row["repository_binding_sha256"]
                        != intent["repository_binding_sha256"]
                        or row["observed_topology_sha256"]
                        != intent["observed_topology_sha256"]
                        or self._parse_canonical_object(
                            str(row["same_thread_profile_repair_json"]),
                            label="same-thread profile repair",
                        )
                        != intent["same_thread_profile_repair"]
                    )
                )
            ):
                raise IntegrityError(
                    "plan provider intent canonical/normalized identity mismatch",
                    details={"intent_id": intent["intent_id"]},
                )
            result.append(intent)
        return result

    def _load_selection_proofs(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        definitions: Mapping[str, Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        valid_plan_hashes = {
            str(record["plan_sha256"]),
            str(record["effective_plan_sha256"]),
        }
        receipt_hashes = {
            str(row["receipt_sha256"])
            for row in connection.execute(
                "SELECT receipt_sha256 FROM plan_receipts WHERE plan_id=?",
                (record["plan_id"],),
            )
        }
        for row in connection.execute(
            "SELECT * FROM plan_selection_proofs WHERE plan_id=? "
            "ORDER BY plan_revision, proof_id",
            (record["plan_id"],),
        ):
            proof = self._require_selection_proof(
                self._parse_canonical_object(
                    str(row["record_json"]),
                    label=f"plan selection proof {row['proof_id']}",
                )
            )
            proof_sha256 = content_sha256(proof)
            selected = proof["selected_task"]
            selected_task_id = (
                str(selected["task_id"])
                if isinstance(selected, Mapping)
                else None
            )
            if (
                row["proof_id"] != proof["proof_id"]
                or row["plan_id"] != proof["plan_id"]
                or row["plan_revision"] != proof["plan_revision"]
                or row["outcome"] != proof["outcome"]
                or row["selected_task_id"] != selected_task_id
                or row["proof_sha256"] != proof_sha256
                or row["finalized"] != int(proof["finalized"])
                or proof["plan_id"] != record["plan_id"]
                or proof["plan_sha256"] not in valid_plan_hashes
                or proof["repository_fingerprint"]
                != record["repository_fingerprint"]
                or proof["plan_revision"] >= record["state"]["revision"]
                or proof["outcome"] != "selected"
            ):
                raise IntegrityError(
                    "plan selection proof canonical/normalized identity mismatch",
                    details={"proof_id": proof["proof_id"]},
                )
            for snapshot in proof["ordered_tasks"]:
                definition = definitions.get(str(snapshot["task_id"]))
                if (
                    definition is None
                    or snapshot["task_sha256"]
                    != definition["task_sha256"]
                    or snapshot["canonical_position"]
                    != definition["canonical_position"]
                    or any(
                        effective_id not in definitions
                        for effective_id in snapshot["effective_task_ids"]
                    )
                ):
                    raise IntegrityError(
                        "plan selection proof task snapshot has drifted",
                        details={"proof_id": proof["proof_id"]},
                    )
                for dependency in snapshot["dependencies"]:
                    hashes = set(dependency["receipt_sha256s"])
                    if (
                        any(
                            task_id not in definitions
                            for task_id in dependency[
                                "effective_task_ids"
                            ]
                        )
                        or not hashes <= receipt_hashes
                        or (
                            dependency["status"] != "terminal"
                            and hashes
                        )
                    ):
                        raise IntegrityError(
                            "plan selection proof dependency evidence has drifted",
                            details={"proof_id": proof["proof_id"]},
                        )
            journal_matches = [
                entry
                for entry in record["journal"]
                if entry["kind"] == "selection_proof"
                and entry["payload"].get("proof_id") == proof["proof_id"]
            ]
            if (
                len(journal_matches) != 1
                or journal_matches[0]["prior_hash"]
                != proof["prior_journal_sha256"]
                or journal_matches[0]["payload"].get("proof_sha256")
                != proof_sha256
                or journal_matches[0]["payload"].get("plan_revision")
                != proof["plan_revision"]
                or journal_matches[0]["payload"].get("outcome")
                != proof["outcome"]
                or journal_matches[0]["payload"].get("selected_task_id")
                != selected_task_id
                or row["created_at"]
                != journal_matches[0]["payload"].get("timestamp")
            ):
                raise IntegrityError(
                    "plan selection proof journal linkage mismatch",
                    details={"proof_id": proof["proof_id"]},
                )
            result.append(proof)
        return result

    @staticmethod
    def _task_state_values(
        plan_id: str,
        task: Mapping[str, Any],
    ) -> tuple[Any, ...]:
        link = task["receipt_link"]
        return (
            plan_id,
            task["task_id"],
            task["task_sha256"],
            task["status"],
            task["generation"],
            task["counters"]["worker_discussions"],
            task["counters"]["continue_invocations"],
            task["counters"]["agentjobs"],
            task["counters"]["provider_creates"],
            task["counters"]["successor_creates"],
            task["counters"]["same_task_successors"],
            link["receipt_id"] if link is not None else None,
            link["receipt_sha256"] if link is not None else None,
            task["fingerprint_before"],
            task["fingerprint_after"],
            task["terminal_reason"],
            canonical_json_bytes(task).decode("utf-8"),
            task["updated_at"],
        )

    def _sync_task_states(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        definitions: Mapping[str, Mapping[str, Any]],
    ) -> None:
        state_tasks = list(record["state"]["tasks"])
        if {str(item["task_id"]) for item in state_tasks} != set(definitions):
            raise RecordValidationError(
                "canonical plan state does not contain every persisted task definition"
            )
        existing = {
            str(row["task_id"])
            for row in connection.execute(
                "SELECT task_id FROM plan_task_states WHERE plan_id=?",
                (record["plan_id"],),
            )
        }
        if not existing <= set(definitions):
            raise IntegrityError("plan task-state table contains an unknown task")
        for task in state_tasks:
            definition = definitions[str(task["task_id"])]
            if task["task_sha256"] != definition["task_sha256"]:
                raise RecordValidationError(
                    "canonical plan task-state hash differs from its definition"
                )
            values = self._task_state_values(str(record["plan_id"]), task)
            connection.execute(
                """
                INSERT INTO plan_task_states(
                    plan_id, task_id, task_sha256, lifecycle_status, generation,
                    worker_discussions, continue_invocations, agentjobs,
                    provider_creates, successor_creates, same_task_successors,
                    receipt_id, receipt_sha256, fingerprint_before,
                    fingerprint_after, terminal_reason, lifecycle_json, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(plan_id, task_id) DO UPDATE SET
                    task_sha256=excluded.task_sha256,
                    lifecycle_status=excluded.lifecycle_status,
                    generation=excluded.generation,
                    worker_discussions=excluded.worker_discussions,
                    continue_invocations=excluded.continue_invocations,
                    agentjobs=excluded.agentjobs,
                    provider_creates=excluded.provider_creates,
                    successor_creates=excluded.successor_creates,
                    same_task_successors=excluded.same_task_successors,
                    receipt_id=excluded.receipt_id,
                    receipt_sha256=excluded.receipt_sha256,
                    fingerprint_before=excluded.fingerprint_before,
                    fingerprint_after=excluded.fingerprint_after,
                    terminal_reason=excluded.terminal_reason,
                    lifecycle_json=excluded.lifecycle_json,
                    updated_at=excluded.updated_at
                """,
                values,
            )

    def _validate_child_parity(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        replacement_definitions: list[dict[str, Any]],
    ) -> None:
        plan_id = str(record["plan_id"])
        phases = list(record["plan"]["phases"])
        expected_phases = [
            (
                plan_id,
                phase["phase_id"],
                position,
                content_sha256(phase),
                canonical_json_bytes(phase).decode("utf-8"),
            )
            for position, phase in enumerate(phases)
        ]
        self._assert_rows(
            connection,
            query=(
                "SELECT plan_id, phase_id, canonical_position, phase_sha256, "
                "phase_json FROM plan_phases WHERE plan_id=? "
                "ORDER BY canonical_position, phase_id"
            ),
            parameters=(plan_id,),
            columns=(
                "plan_id",
                "phase_id",
                "canonical_position",
                "phase_sha256",
                "phase_json",
            ),
            expected=expected_phases,
            label="phases",
        )
        expected_phase_dependencies = [
            (plan_id, phase["phase_id"], dependency, dependency_position)
            for phase in phases
            for dependency_position, dependency in enumerate(phase["depends_on"])
        ]
        self._assert_rows(
            connection,
            query=(
                "SELECT dependency.plan_id, dependency.phase_id, "
                "dependency.depends_on_phase_id, dependency.dependency_position "
                "FROM plan_phase_dependencies AS dependency "
                "JOIN plan_phases AS phase ON phase.plan_id=dependency.plan_id "
                "AND phase.phase_id=dependency.phase_id "
                "WHERE dependency.plan_id=? "
                "ORDER BY phase.canonical_position, dependency.dependency_position"
            ),
            parameters=(plan_id,),
            columns=(
                "plan_id",
                "phase_id",
                "depends_on_phase_id",
                "dependency_position",
            ),
            expected=expected_phase_dependencies,
            label="phase dependencies",
        )
        all_definitions = self._base_definitions(record) + replacement_definitions
        all_definitions.sort(
            key=lambda item: (item["canonical_position"], item["task_id"])
        )
        definitions = {item["task_id"]: item for item in all_definitions}
        expected_tasks = [
            (
                plan_id,
                item["task_id"],
                item["task_sha256"],
                item["phase_id"],
                item["canonical_position"],
                item["origin_kind"],
                canonical_json_bytes(item["task_json"]).decode("utf-8"),
            )
            for item in all_definitions
        ]
        self._assert_rows(
            connection,
            query=(
                "SELECT plan_id, task_id, task_sha256, phase_id, "
                "canonical_position, origin_kind, task_json FROM plan_tasks "
                "WHERE plan_id=? ORDER BY canonical_position, task_id"
            ),
            parameters=(plan_id,),
            columns=(
                "plan_id",
                "task_id",
                "task_sha256",
                "phase_id",
                "canonical_position",
                "origin_kind",
                "task_json",
            ),
            expected=expected_tasks,
            label="tasks",
        )
        expected_task_dependencies = [
            (plan_id, item["task_id"], dependency, dependency_position)
            for item in all_definitions
            for dependency_position, dependency in enumerate(item["depends_on"])
        ]
        self._assert_rows(
            connection,
            query=(
                "SELECT dependency.plan_id, dependency.task_id, "
                "dependency.depends_on_task_id, dependency.dependency_position "
                "FROM plan_task_dependencies AS dependency "
                "JOIN plan_tasks AS task ON task.plan_id=dependency.plan_id "
                "AND task.task_id=dependency.task_id "
                "WHERE dependency.plan_id=? "
                "ORDER BY task.canonical_position, dependency.dependency_position"
            ),
            parameters=(plan_id,),
            columns=(
                "plan_id",
                "task_id",
                "depends_on_task_id",
                "dependency_position",
            ),
            expected=expected_task_dependencies,
            label="task dependencies",
        )
        state_by_id = {
            str(item["task_id"]): item for item in record["state"]["tasks"]
        }
        expected_task_states = [
            self._task_state_values(plan_id, state_by_id[item["task_id"]])
            for item in all_definitions
        ]
        self._assert_rows(
            connection,
            query=(
                "SELECT state.plan_id, state.task_id, state.task_sha256, "
                "state.lifecycle_status, state.generation, "
                "state.worker_discussions, state.continue_invocations, "
                "state.agentjobs, state.provider_creates, "
                "state.successor_creates, state.same_task_successors, "
                "state.receipt_id, state.receipt_sha256, "
                "state.fingerprint_before, state.fingerprint_after, "
                "state.terminal_reason, state.lifecycle_json, state.updated_at "
                "FROM plan_task_states AS state "
                "JOIN plan_tasks AS task ON task.plan_id=state.plan_id "
                "AND task.task_id=state.task_id "
                "WHERE state.plan_id=? ORDER BY task.canonical_position, task.task_id"
            ),
            parameters=(plan_id,),
            columns=(
                "plan_id",
                "task_id",
                "task_sha256",
                "lifecycle_status",
                "generation",
                "worker_discussions",
                "continue_invocations",
                "agentjobs",
                "provider_creates",
                "successor_creates",
                "same_task_successors",
                "receipt_id",
                "receipt_sha256",
                "fingerprint_before",
                "fingerprint_after",
                "terminal_reason",
                "lifecycle_json",
                "updated_at",
            ),
            expected=expected_task_states,
            label="task states",
        )
        receipts = self._load_receipt_records(connection, record, definitions)
        disposition_by_status = {
            "completed": {"task_complete"},
            "blocked": {"blocked"},
            "superseded": {"replan_required"},
            "replan_required": {"replan_required"},
            "human_gate_required": {"human_gate_required"},
            "validation_failed": {"validation_failed"},
            "invocation_unknown": {"invocation_unknown"},
            "cancelled": {"cancelled"},
        }
        for task_id, receipt_entry in receipts.items():
            if state_by_id[task_id]["status"] not in disposition_by_status:
                raise IntegrityError(
                    "plan receipt exists for a nonterminal task",
                    details={"task_id": task_id},
                )
            receipt = receipt_entry["record"]
            task = state_by_id[task_id]
            link = task["receipt_link"]
            execution = receipt["execution"]
            repository = receipt["repository_evidence"]
            expected_counters = {
                "worker_discussions": execution["worker_discussions"],
                "provider_creates": execution["provider_create_calls"],
                "successor_creates": execution["successor_creates"],
                "same_task_successors": execution["same_task_successors"],
            }
            if execution["continue_invocations"] != "unknown":
                expected_counters["continue_invocations"] = execution[
                    "continue_invocations"
                ]
            if execution["agentjobs"] != "unknown":
                expected_counters["agentjobs"] = execution["agentjobs"]
            if (
                link is None
                or link["receipt_id"] != receipt["receipt_id"]
                or link["receipt_sha256"] != receipt_entry["receipt_sha256"]
                or receipt["disposition"]
                not in disposition_by_status[task["status"]]
                or receipt["relay_identity"]["generation"] != task["generation"]
                or any(
                    task["counters"][key] != value
                    for key, value in expected_counters.items()
                )
                or repository["fingerprint_before"]
                != task["fingerprint_before"]
                or repository["fingerprint_after"] != task["fingerprint_after"]
            ):
                raise IntegrityError(
                    "plan task receipt disagrees with canonical task state",
                    details={"task_id": task_id},
                )
        for task_id, task in state_by_id.items():
            if task["status"] in disposition_by_status and task_id not in receipts:
                raise IntegrityError(
                    "terminal plan task is missing its immutable receipt",
                    details={"task_id": task_id},
                )
        self._load_provider_intents(connection, record, definitions)
        self._load_selection_proofs(connection, record, definitions)

    def _validate_plan_lease_parity(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> None:
        rows = list(
            connection.execute(
                "SELECT * FROM plan_leases WHERE plan_id=? ORDER BY lease_id",
                (record["plan_id"],),
            )
        )
        creation_events = {
            entry["payload"]["plan_lease_transaction_id"]: entry
            for entry in record["journal"]
            if entry["kind"] == "event"
            and entry["payload"].get("event_type")
            in {
                "plan_lease_acquired",
                "plan_lease_transferred",
                "plan_lease_quarantined",
            }
        }
        if len(creation_events) != len(rows):
            raise IntegrityError(
                "plan lease rows and append-only creation events disagree"
            )
        for row in rows:
            event = creation_events.get(row["transaction_id"])
            if event is None:
                raise IntegrityError(
                    "plan lease lacks its append-only creation event"
                )
            payload = event["payload"]
            expected_event = {
                "plan_id": record["plan_id"],
                "task_id": row["task_id"],
                "generation": row["generation"],
                "holder_kind": row["holder_kind"],
                "plan_lease_transaction_id": row["transaction_id"],
                "outer_lease_transaction_id": row[
                    "outer_lease_transaction_id"
                ],
            }
            if any(
                payload.get(field_name) != value
                for field_name, value in expected_event.items()
            ):
                raise IntegrityError(
                    "plan lease creation event identity disagrees with its row"
                )
            outer_row = connection.execute(
                "SELECT * FROM leases WHERE transaction_id=?",
                (row["outer_lease_transaction_id"],),
            ).fetchone()
            if (
                outer_row is None
                or outer_row["goal_id"] != record["outer_goal_id"]
                or outer_row["generation"] != row["generation"]
                or outer_row["holder_kind"]
                != OUTER_HOLDER_KINDS[row["holder_kind"]]
                or holder_token_sha256(outer_row["holder_token"])
                != row["holder_token_sha256"]
                or outer_row["acquired_at"] != row["acquired_at"]
                or outer_row["heartbeat_at"] != row["heartbeat_at"]
                or outer_row["expires_at"] != row["expires_at"]
                or outer_row["lease_state"] != row["lease_state"]
                or outer_row["released_at"] != row["released_at"]
            ):
                raise IntegrityError(
                    "plan lease history and outer-goal lease disagree"
                )
            closing_events = [
                entry
                for entry in record["journal"]
                if entry["kind"] == "event"
                and (
                    (
                        entry["payload"].get("event_type")
                        in {
                            "plan_lease_transferred",
                            "plan_lease_quarantined",
                        }
                        and entry["payload"].get(
                            "prior_plan_lease_transaction_id"
                        )
                        == row["transaction_id"]
                    )
                    or (
                        entry["payload"].get("event_type")
                        == "plan_lease_released"
                        and entry["payload"].get(
                            "plan_lease_transaction_id"
                        )
                        == row["transaction_id"]
                    )
                )
            ]
            if row["lease_state"] == "released":
                if (
                    len(closing_events) != 1
                    or row["released_at"]
                    != closing_events[0]["payload"]["timestamp"]
                ):
                    raise IntegrityError(
                        "released plan lease lacks one append-only closing event"
                    )
            elif closing_events or row["released_at"] is not None:
                raise IntegrityError(
                    "active plan lease has a closing event or release timestamp"
                )

        active_rows = [row for row in rows if row["lease_state"] == "active"]
        lease = record["state"]["lease"]
        if lease is None and not active_rows:
            return
        if lease is None or len(active_rows) != 1:
            raise IntegrityError(
                "canonical plan and normalized lease state disagree"
            )
        row = active_rows[0]
        expected = {
            "plan_id": record["plan_id"],
            "task_id": lease["task_id"],
            "generation": lease["generation"],
            "holder_kind": lease["holder_kind"],
            "holder_token_sha256": lease["holder_token_hash"],
            "transaction_id": lease["transaction_id"],
            "repository_fingerprint": lease["repository_fingerprint"],
            "acquired_at": lease["acquired_at"],
            "heartbeat_at": lease["heartbeat_at"],
            "expires_at": lease["expires_at"],
        }
        for field_name, value in expected.items():
            if row[field_name] != value:
                raise IntegrityError(
                    f"plan and normalized lease disagree on {field_name}"
                )
        outer_goal = connection.execute(
            "SELECT record_json FROM goals WHERE goal_id=?",
            (record["outer_goal_id"],),
        ).fetchone()
        if outer_goal is None:
            raise IntegrityError("plan lease outer goal does not exist")
        outer_record = json.loads(str(outer_goal["record_json"]))
        self.goal_store._validate_lease_parity(connection, outer_record)
        outer_lease = outer_record["state"].get("active_lease")
        if (
            outer_lease is None
            or outer_row["goal_id"] != record["outer_goal_id"]
            or outer_lease["transaction_id"]
            != row["outer_lease_transaction_id"]
            or outer_lease["generation"] != lease["generation"]
            or outer_lease["holder_kind"]
            != OUTER_HOLDER_KINDS[lease["holder_kind"]]
            or holder_token_sha256(outer_lease["holder_token"])
            != lease["holder_token_hash"]
            or outer_lease["acquired_at"] != lease["acquired_at"]
            or outer_lease["heartbeat_at"] != lease["heartbeat_at"]
            or outer_lease["expires_at"] != lease["expires_at"]
        ):
            raise IntegrityError(
                "plan lease and outer-goal lease identity disagree"
            )

    def _insert_base_children(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> None:
        plan_id = str(record["plan_id"])
        for position, phase in enumerate(record["plan"]["phases"]):
            connection.execute(
                """
                INSERT INTO plan_phases(
                    plan_id, phase_id, canonical_position, phase_sha256, phase_json
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    plan_id,
                    phase["phase_id"],
                    position,
                    content_sha256(phase),
                    canonical_json_bytes(phase).decode("utf-8"),
                ),
            )
        for phase in record["plan"]["phases"]:
            for dependency_position, dependency in enumerate(phase["depends_on"]):
                connection.execute(
                    """
                    INSERT INTO plan_phase_dependencies(
                        plan_id, phase_id, depends_on_phase_id, dependency_position
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (
                        plan_id,
                        phase["phase_id"],
                        dependency,
                        dependency_position,
                    ),
                )
        definitions = self._base_definitions(record)
        for item in definitions:
            connection.execute(
                """
                INSERT INTO plan_tasks(
                    plan_id, task_id, task_sha256, phase_id, canonical_position,
                    origin_kind, task_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    plan_id,
                    item["task_id"],
                    item["task_sha256"],
                    item["phase_id"],
                    item["canonical_position"],
                    item["origin_kind"],
                    canonical_json_bytes(item["task_json"]).decode("utf-8"),
                ),
            )
        for item in definitions:
            for dependency_position, dependency in enumerate(item["depends_on"]):
                connection.execute(
                    """
                    INSERT INTO plan_task_dependencies(
                        plan_id, task_id, depends_on_task_id, dependency_position
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (
                        plan_id,
                        item["task_id"],
                        dependency,
                        dependency_position,
                    ),
                )
        self._sync_task_states(
            connection,
            record,
            {item["task_id"]: item for item in definitions},
        )

    def _events(
        self,
        connection: sqlite3.Connection,
        plan_id: str,
    ) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for row in connection.execute(
            "SELECT sequence, kind, payload_json, prior_hash, event_hash, created_at "
            "FROM plan_events WHERE plan_id=? ORDER BY sequence",
            (plan_id,),
        ):
            payload = self._parse_canonical_object(
                str(row["payload_json"]),
                label=f"plan event {row['sequence']} payload",
            )
            if payload.get("timestamp") != row["created_at"]:
                raise IntegrityError("plan event timestamp projection mismatch")
            result.append(
                {
                    "sequence": int(row["sequence"]),
                    "kind": str(row["kind"]),
                    "payload": payload,
                    "prior_hash": row["prior_hash"],
                    "event_hash": str(row["event_hash"]),
                }
            )
        return result

    def _activation_history(
        self,
        connection: sqlite3.Connection,
        plan_id: str,
    ) -> list[dict[str, Any]]:
        if self.database_schema_version < 5:
            return []
        history: list[dict[str, Any]] = []
        prior_activation_id: str | None = None
        for expected_sequence, row in enumerate(
            connection.execute(
                "SELECT * FROM plan_activation_receipts "
                "WHERE plan_id=? ORDER BY activation_sequence",
                (plan_id,),
            ),
            1,
        ):
            receipt = self._require_activation_receipt(
                self._parse_canonical_object(
                    str(row["receipt_json"]),
                    label=f"plan activation receipt {row['activation_id']}",
                )
            )
            receipt_sha256 = content_sha256(receipt)
            if (
                row["activation_id"] != receipt["activation_id"]
                or row["plan_id"] != receipt["plan_id"]
                or row["activation_sequence"] != expected_sequence
                or row["receipt_sha256"] != receipt_sha256
                or row["effective_from_generation"]
                != receipt["effective_from_generation"]
                or row["superseded_activation_id"]
                != receipt["superseded_activation_id"]
                or row["accepted_at"] != receipt["accepted_at"]
                or receipt["plan_id"] != plan_id
                or receipt["superseded_activation_id"]
                != prior_activation_id
            ):
                raise IntegrityError(
                    "plan activation receipt canonical/normalized mismatch",
                    details={"activation_id": receipt["activation_id"]},
                )
            history.append(receipt)
            prior_activation_id = str(receipt["activation_id"])
        return history

    def _validate_activation_history(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> None:
        history = self._activation_history(
            connection,
            str(record["plan_id"]),
        )
        if record["runtime_profile_version"] == 1:
            if history:
                raise IntegrityError(
                    "legacy plan row unexpectedly has activation history"
                )
            return
        if (
            len(history) != record["activation_sequence"]
            or not history
        ):
            raise IntegrityError(
                "plan activation history cardinality does not match profile"
            )
        current = history[-1]
        profile = record["execution_profile"]
        if (
            content_sha256(current)
            != record["activation_receipt_sha256"]
            or current["activation_id"] != profile["activation_id"]
            or current["accepted_plan_sha256"]
            != record["effective_plan_sha256"]
            or current["exact_activation_goal_sha256"]
            != record["activation_goal_sha256"]
            or current["effective_from_generation"]
            != record["profile_effective_from_generation"]
            or current["repository_identity_sha256"]
            != record["repository_binding_sha256"]
            or current["repository_topology_policy_sha256"]
            != content_sha256(record["repository_topology_policy"])
        ):
            raise IntegrityError(
                "current activation receipt does not match plan profile state"
            )

    def _record_from_row(
        self,
        connection: sqlite3.Connection,
        row: sqlite3.Row,
    ) -> dict[str, Any]:
        plan = self._parse_canonical_object(str(row["plan_json"]), label="plan_json")
        state = self._parse_canonical_object(str(row["state_json"]), label="state_json")
        binding = self._parse_canonical_object(
            str(row["repository_binding_json"]),
            label="repository_binding_json",
        )
        row_keys = set(row.keys())
        runtime_profile_version = (
            int(row["runtime_profile_version"])
            if "runtime_profile_version" in row_keys
            else 1
        )
        execution_profile = (
            self._parse_canonical_object(
                str(row["execution_profile_json"]),
                label="execution_profile_json",
            )
            if "execution_profile_json" in row_keys
            and row["execution_profile_json"] is not None
            else None
        )
        topology_policy = (
            self._parse_canonical_object(
                str(row["topology_policy_json"]),
                label="topology_policy_json",
            )
            if "topology_policy_json" in row_keys
            and row["topology_policy_json"] is not None
            else None
        )
        return {
            "plan_id": str(row["plan_id"]),
            "outer_goal_id": str(row["outer_goal_id"]),
            "plan_sha256": str(row["plan_sha256"]),
            "effective_plan_sha256": str(row["effective_plan_sha256"]),
            "repository_binding": binding,
            "repository_fingerprint": str(row["repository_fingerprint"]),
            "plan": plan,
            "state": state,
            "journal": self._events(connection, str(row["plan_id"])),
            "runtime_profile_version": runtime_profile_version,
            "activation_sequence": (
                int(row["activation_sequence"])
                if "activation_sequence" in row_keys
                else 0
            ),
            "activation_receipt_sha256": (
                row["activation_receipt_sha256"]
                if "activation_receipt_sha256" in row_keys
                else None
            ),
            "execution_profile": execution_profile,
            "repository_topology_policy": topology_policy,
            "activation_goal_text": (
                row["activation_goal_text"]
                if "activation_goal_text" in row_keys
                else None
            ),
            "activation_goal_sha256": (
                row["activation_goal_sha256"]
                if "activation_goal_sha256" in row_keys
                else None
            ),
            "profile_effective_from_generation": (
                row["profile_effective_from_generation"]
                if "profile_effective_from_generation" in row_keys
                else None
            ),
            "repository_binding_sha256": (
                row["repository_binding_sha256"]
                if "repository_binding_sha256" in row_keys
                else None
            ),
            "created_at": str(row["created_at"]),
            "updated_at": str(row["updated_at"]),
        }

    def _validate_row_parity(
        self,
        connection: sqlite3.Connection,
        row: sqlite3.Row,
        record: Mapping[str, Any],
    ) -> None:
        replacement_definitions, _ = self._replacement_definitions(
            connection,
            record,
        )
        validate_runtime_plan_record(
            record,
            plan_schema_path=self.plan_schema_path,
            state_schema_path=self.state_schema_path,
            additional_tasks=replacement_definitions,
        )
        state = record["state"]
        expected = {
            "plan_id": record["plan_id"],
            "outer_goal_id": record["outer_goal_id"],
            "plan_schema_version": record["plan"]["schema_version"],
            "state_schema_version": state["schema_version"],
            "plan_sha256": record["plan_sha256"],
            "effective_plan_sha256": record["effective_plan_sha256"],
            "repository_binding_json": canonical_json_bytes(
                record["repository_binding"]
            ).decode("utf-8"),
            "repository_fingerprint": record["repository_fingerprint"],
            "plan_json": canonical_json_bytes(record["plan"]).decode("utf-8"),
            "state_json": canonical_json_bytes(state).decode("utf-8"),
            "state_revision": state["revision"],
            "phase": state["phase"],
            "current_generation": state["current_generation"],
            "active_task_id": state["active_task_id"],
            "evaluation": state["evaluation"],
            "initial_fingerprint": state["fingerprints"]["initial"],
            "current_fingerprint": state["fingerprints"]["current"],
            "journal_head_sha256": record["journal"][-1]["event_hash"],
            "terminal_reason": state["terminal_reason"],
            "created_at": record["created_at"],
            "updated_at": record["updated_at"],
        }
        if "runtime_profile_version" in set(row.keys()):
            expected.update(
                {
                    "runtime_profile_version": record[
                        "runtime_profile_version"
                    ],
                    "activation_sequence": record["activation_sequence"],
                    "activation_receipt_sha256": record[
                        "activation_receipt_sha256"
                    ],
                    "execution_profile_json": (
                        canonical_json_bytes(
                            record["execution_profile"]
                        ).decode("utf-8")
                        if record["execution_profile"] is not None
                        else None
                    ),
                    "topology_policy_json": (
                        canonical_json_bytes(
                            record["repository_topology_policy"]
                        ).decode("utf-8")
                        if record["repository_topology_policy"] is not None
                        else None
                    ),
                    "activation_goal_text": record[
                        "activation_goal_text"
                    ],
                    "activation_goal_sha256": record[
                        "activation_goal_sha256"
                    ],
                    "profile_effective_from_generation": record[
                        "profile_effective_from_generation"
                    ],
                    "repository_binding_sha256": record[
                        "repository_binding_sha256"
                    ],
                }
            )
        for key, value in expected.items():
            if row[key] != value:
                raise IntegrityError(
                    f"plan normalized projection mismatch: {key}",
                    details={"plan_id": record["plan_id"], "field": key},
                )
        self._validate_child_parity(
            connection,
            record,
            replacement_definitions,
        )
        self._validate_plan_lease_parity(connection, record)
        self._validate_activation_history(connection, record)

    def _load_plan(
        self,
        connection: sqlite3.Connection,
        plan_id: str,
    ) -> dict[str, Any]:
        row = connection.execute(
            "SELECT * FROM plans WHERE plan_id=?",
            (plan_id,),
        ).fetchone()
        if row is None:
            raise RecordNotFound(f"plan does not exist: {plan_id}")
        record = self._record_from_row(connection, row)
        self._validate_row_parity(connection, row, record)
        return record

    def load_plan(self, plan_id: str) -> dict[str, Any]:
        connection = self.connect()
        try:
            return self._load_plan(connection, plan_id)
        finally:
            connection.close()

    def load_task_definition(
        self,
        plan_id: str,
        task_id: str,
    ) -> dict[str, Any]:
        """Load one effective base or append-only replacement definition."""

        connection = self.connect()
        try:
            record = self._load_plan(connection, plan_id)
            definition = self._definitions(connection, record).get(task_id)
            if definition is None:
                raise RecordNotFound(
                    f"plan task definition does not exist: {plan_id}/{task_id}"
                )
            return copy.deepcopy(definition)
        finally:
            connection.close()

    def list_plans(self) -> list[dict[str, Any]]:
        connection = self.connect()
        try:
            result: list[dict[str, Any]] = []
            plan_ids = [
                str(row["plan_id"])
                for row in connection.execute(
                    "SELECT plan_id FROM plans ORDER BY created_at, plan_id"
                )
            ]
            for plan_id in plan_ids:
                record = self._load_plan(connection, plan_id)
                result.append(
                    {
                        "plan_id": plan_id,
                        "outer_goal_id": record["outer_goal_id"],
                        "plan_sha256": record["plan_sha256"],
                        "effective_plan_sha256": record["effective_plan_sha256"],
                        "revision": record["state"]["revision"],
                        "phase": record["state"]["phase"],
                        "current_generation": record["state"]["current_generation"],
                        "active_task_id": record["state"]["active_task_id"],
                        "evaluation": record["state"]["evaluation"],
                        "runtime_profile_version": record[
                            "runtime_profile_version"
                        ],
                        "activation_sequence": record[
                            "activation_sequence"
                        ],
                        "reasoning_effort": (
                            record["execution_profile"][
                                "reasoning_effort"
                            ]
                            if record["execution_profile"] is not None
                            else None
                        ),
                    }
                )
            return result
        finally:
            connection.close()

    def export_plan(self, plan_id: str) -> dict[str, Any]:
        return {
            "schema_version": PLAN_EXPORT_SCHEMA_VERSION,
            "record": self.load_plan(plan_id),
            "activation_receipts": self.list_activation_receipts(plan_id),
        }

    def export_plans(self) -> dict[str, Any]:
        return {
            "schema_version": PLAN_EXPORT_SCHEMA_VERSION,
            "records": [
                self.export_plan(item["plan_id"])
                for item in self.list_plans()
            ],
        }

    def _insert_events(
        self,
        connection: sqlite3.Connection,
        plan_id: str,
        entries: list[Mapping[str, Any]],
    ) -> None:
        for entry in entries:
            timestamp = str(entry["payload"].get("timestamp"))
            connection.execute(
                """
                INSERT INTO plan_events(
                    plan_id, sequence, kind, payload_json, prior_hash,
                    event_hash, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    plan_id,
                    entry["sequence"],
                    entry["kind"],
                    canonical_json_bytes(entry["payload"]).decode("utf-8"),
                    entry["prior_hash"],
                    entry["event_hash"],
                    timestamp,
                ),
            )

    def _insert_activation_receipt(
        self,
        connection: sqlite3.Connection,
        receipt: Mapping[str, Any],
        *,
        activation_sequence: int,
    ) -> str:
        value = self._require_activation_receipt(receipt)
        receipt_sha256 = content_sha256(value)
        connection.execute(
            """
            INSERT INTO plan_activation_receipts(
                activation_id, plan_id, activation_sequence,
                receipt_json, receipt_sha256,
                effective_from_generation, superseded_activation_id,
                accepted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                value["activation_id"],
                value["plan_id"],
                activation_sequence,
                canonical_json_bytes(value).decode("utf-8"),
                receipt_sha256,
                value["effective_from_generation"],
                value["superseded_activation_id"],
                value["accepted_at"],
            ),
        )
        return receipt_sha256

    @staticmethod
    def _insert_plan_row(
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> None:
        state = record["state"]
        connection.execute(
            """
            INSERT INTO plans(
                plan_id, outer_goal_id, plan_schema_version,
                state_schema_version, plan_sha256, effective_plan_sha256,
                repository_binding_json, repository_fingerprint, plan_json,
                state_json, state_revision, phase, current_generation,
                active_task_id, evaluation, initial_fingerprint,
                current_fingerprint, journal_head_sha256, terminal_reason,
                runtime_profile_version, activation_sequence,
                activation_receipt_sha256, execution_profile_json,
                topology_policy_json, activation_goal_text,
                activation_goal_sha256, profile_effective_from_generation,
                repository_binding_sha256, created_at, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                record["plan_id"],
                record["outer_goal_id"],
                record["plan"]["schema_version"],
                state["schema_version"],
                record["plan_sha256"],
                record["effective_plan_sha256"],
                canonical_json_bytes(record["repository_binding"]).decode("utf-8"),
                record["repository_fingerprint"],
                canonical_json_bytes(record["plan"]).decode("utf-8"),
                canonical_json_bytes(state).decode("utf-8"),
                state["revision"],
                state["phase"],
                state["current_generation"],
                state["active_task_id"],
                state["evaluation"],
                state["fingerprints"]["initial"],
                state["fingerprints"]["current"],
                record["journal"][-1]["event_hash"],
                state["terminal_reason"],
                record["runtime_profile_version"],
                record["activation_sequence"],
                record["activation_receipt_sha256"],
                (
                    canonical_json_bytes(
                        record["execution_profile"]
                    ).decode("utf-8")
                    if record["execution_profile"] is not None
                    else None
                ),
                (
                    canonical_json_bytes(
                        record["repository_topology_policy"]
                    ).decode("utf-8")
                    if record["repository_topology_policy"] is not None
                    else None
                ),
                record["activation_goal_text"],
                record["activation_goal_sha256"],
                record["profile_effective_from_generation"],
                record["repository_binding_sha256"],
                record["created_at"],
                record["updated_at"],
            ),
        )

    def _initialization_evidence(
        self,
        record: Mapping[str, Any],
    ) -> dict[str, Any] | None:
        report_entries = [
            entry
            for entry in record["journal"]
            if entry["kind"] == "event"
            and entry["payload"].get("event_type")
            == "normalization_report_persisted"
        ]
        receipt_entries = [
            entry
            for entry in record["journal"]
            if entry["kind"] == "event"
            and entry["payload"].get("event_type")
            == "plan_initialization_finalized"
        ]
        if not report_entries and not receipt_entries:
            return None
        if len(report_entries) != 1 or len(receipt_entries) != 1:
            raise IntegrityError(
                "plan initialization evidence cardinality is invalid"
            )
        report_entry = report_entries[0]
        receipt_entry = receipt_entries[0]
        report_payload = report_entry["payload"]
        receipt_payload = receipt_entry["payload"]
        report = self._require_normalization_report(
            report_payload.get("normalization_report", {})
        )
        receipt = self._require_initialization_receipt(
            receipt_payload.get("initialization_receipt", {})
        )
        if (
            report_entry["sequence"] + 1 != receipt_entry["sequence"]
            or receipt_entry["prior_hash"] != report_entry["event_hash"]
            or receipt["prior_journal_sha256"] != report_entry["event_hash"]
            or report_payload.get("plan_id") != record["plan_id"]
            or report_payload.get("report_id") != report["report_id"]
            or report_payload.get("report_content_sha256")
            != report["report_content_sha256"]
            or receipt_payload.get("plan_id") != record["plan_id"]
            or receipt_payload.get("receipt_id") != receipt["receipt_id"]
            or receipt_payload.get("receipt_content_sha256")
            != receipt["receipt_content_sha256"]
            or receipt["plan_identity"]
            != {
                "plan_id": record["plan_id"],
                "plan_sha256": record["plan_sha256"],
            }
            or receipt["normalization_identity"]
            != {
                "report_id": report["report_id"],
                "report_content_sha256": report["report_content_sha256"],
                "source_set_sha256": report["source_set_sha256"],
            }
            or report["plan_id"] != record["plan_id"]
            or report["candidate_plan_sha256"] != record["plan_sha256"]
            or receipt["repository_fingerprint"]
            != record["repository_fingerprint"]
            or receipt["initial_fingerprint"]
            != record["state"]["fingerprints"]["initial"]
            or receipt["materialized"]["phase_count"]
            != len(record["plan"]["phases"])
            or receipt["materialized"]["task_count"]
            != len(record["plan"]["tasks"])
        ):
            raise IntegrityError(
                "plan initialization evidence does not match canonical plan state"
            )
        result = {
            "normalization_report": report,
            "initialization_receipt": receipt,
        }
        if (
            receipt["schema_version"]
            == PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION
        ):
            history = [
                entry
                for entry in record["journal"]
                if entry["kind"] == "event"
                and entry["payload"].get("event_type")
                == "plan_activation_persisted"
            ]
            if len(history) != 1:
                raise IntegrityError(
                    "plan initialization activation evidence cardinality is invalid"
                )
            activation = receipt["activation_identity"]
            profile = record["execution_profile"]
            if (
                history[0]["sequence"] + 1 != report_entry["sequence"]
                or history[0]["payload"].get("activation_id")
                != activation["activation_id"]
                or history[0]["payload"].get(
                    "activation_receipt_sha256"
                )
                != activation["activation_receipt_sha256"]
                or activation["activation_receipt_sha256"]
                != record["activation_receipt_sha256"]
                or activation["execution_profile_sha256"]
                != profile["profile_content_sha256"]
                or activation["repository_topology_policy_sha256"]
                != content_sha256(record["repository_topology_policy"])
                or activation["activation_goal_sha256"]
                != record["activation_goal_sha256"]
                or activation["effective_from_generation"] != 1
            ):
                raise IntegrityError(
                    "plan initialization activation evidence does not match "
                    "canonical profile state"
                )
            result.update(
                {
                    "activation_receipt_sha256": record[
                        "activation_receipt_sha256"
                    ],
                    "execution_profile": copy.deepcopy(profile),
                    "repository_topology_policy": copy.deepcopy(
                        record["repository_topology_policy"]
                    ),
                    "activation_goal_text": record[
                        "activation_goal_text"
                    ],
                }
            )
        return result

    def create_initialized_plan(
        self,
        *,
        plan: Mapping[str, Any],
        normalization_report: Mapping[str, Any],
        activation_receipt: Mapping[str, Any],
        activation_goal_text: str,
        repository_topology_policy: Mapping[str, Any],
        outer_goal_id: str,
        expected_outer_revision: int,
        outer_holder_token: str,
        timestamp: str | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Atomically bind one finalized plan profile to its outer goal lease."""

        if self.read_only:
            raise StateConflict(
                "read-only plan store cannot initialize a plan profile"
            )
        if (
            isinstance(expected_outer_revision, bool)
            or not isinstance(expected_outer_revision, int)
            or expected_outer_revision < 1
        ):
            raise RecordValidationError(
                "expected_outer_revision must be a positive integer"
            )
        if (
            not isinstance(outer_holder_token, str)
            or not outer_holder_token
        ):
            raise RecordValidationError("outer_holder_token must be nonblank")
        now = timestamp or utc_now()
        parse_utc(now)
        report = self._require_normalization_report(normalization_report)
        topology = self._require_topology_policy(
            repository_topology_policy,
            require_default_deny=True,
        )
        if (
            not isinstance(activation_goal_text, str)
            or not activation_goal_text.strip()
            or activation_goal_text != activation_goal_text.strip()
        ):
            raise RecordValidationError(
                "activation_goal_text must be exact, nonblank canonical text"
            )
        from agentjob_runtime.plan.activation import (
            execution_profile_from_receipt,
            validate_activation_receipt,
        )

        canonical_plan = copy.deepcopy(dict(plan))
        plan_sha256 = content_sha256(canonical_plan)
        accepted_activation = validate_activation_receipt(
            activation_receipt,
            plan_id=str(canonical_plan.get("plan_id", "")),
            accepted_plan_sha256=plan_sha256,
            goal_text=activation_goal_text,
            repository_binding=canonical_plan.get("repository_binding", {}),
            repository_topology_policy=topology,
        )
        if (
            accepted_activation["effective_from_generation"] != 1
            or accepted_activation["superseded_activation_id"] is not None
        ):
            raise RecordValidationError(
                "initial plan activation must begin at generation 1 "
                "without a predecessor"
            )
        execution_profile = self._require_execution_profile(
            execution_profile_from_receipt(accepted_activation)
        )
        activation_receipt_sha256 = content_sha256(accepted_activation)
        if (
            execution_profile["activation_receipt_sha256"]
            != activation_receipt_sha256
        ):
            raise IntegrityError(
                "activation receipt and execution-profile hashes differ"
            )
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            outer = self.goal_store._prepare_mutation(
                connection,
                outer_goal_id,
                expected_revision=expected_outer_revision,
                timestamp=now,
            )
            lease = outer.record["state"].get("active_lease")
            if lease is None:
                raise StateConflict(
                    "outer goal does not have an active initialization lease"
                )
            if lease["holder_token"] != outer_holder_token:
                raise StateConflict(
                    "outer initialization lease holder identity does not match"
                )
            if lease["holder_kind"] not in {"launcher", "continuation"}:
                raise StateConflict(
                    "outer lease holder kind cannot initialize plan state"
                )
            if parse_utc(lease["expires_at"]) <= parse_utc(now):
                raise StateConflict("outer initialization lease has expired")
            record = build_initial_plan_record(
                plan=canonical_plan,
                outer_goal_id=outer_goal_id,
                repository_fingerprint=lease["repository_fingerprint"],
                initial_fingerprint=outer.record["state"][
                    "last_canonical_fingerprint"
                ],
                timestamp=now,
                plan_schema_path=self.plan_schema_path,
                state_schema_path=self.state_schema_path,
                runtime_profile_version=2,
                activation_sequence=1,
                activation_receipt_sha256=activation_receipt_sha256,
                execution_profile=execution_profile,
                repository_topology_policy=topology,
                activation_goal_text=activation_goal_text,
                activation_goal_sha256=accepted_activation[
                    "exact_activation_goal_sha256"
                ],
                profile_effective_from_generation=1,
                repository_binding_sha256=accepted_activation[
                    "repository_identity_sha256"
                ],
            )
            if record["repository_binding"] != outer.record[
                "repository_binding"
            ]:
                raise StateConflict(
                    "plan repository binding does not match the outer goal"
                )
            if (
                report["plan_id"] != record["plan_id"]
                or report["candidate_plan_sha256"] != record["plan_sha256"]
            ):
                raise StateConflict(
                    "normalization report differs from the plan candidate"
                )
            append_plan_journal(
                record["journal"],
                "event",
                {
                    "event_type": "plan_activation_persisted",
                    "plan_id": record["plan_id"],
                    "activation_id": accepted_activation[
                        "activation_id"
                    ],
                    "activation_receipt_sha256": (
                        activation_receipt_sha256
                    ),
                    "execution_profile_sha256": execution_profile[
                        "profile_content_sha256"
                    ],
                    "effective_from_generation": 1,
                    "timestamp": now,
                },
            )
            report_event_hash = append_plan_journal(
                record["journal"],
                "event",
                {
                    "event_type": "normalization_report_persisted",
                    "plan_id": record["plan_id"],
                    "report_id": report["report_id"],
                    "report_content_sha256": report[
                        "report_content_sha256"
                    ],
                    "normalization_report": report,
                    "timestamp": now,
                },
            )
            receipt: dict[str, Any] = {
                "schema_version": PLAN_INITIALIZATION_RECEIPT_SCHEMA_VERSION,
                "receipt_id": f"PIR-{record['plan_id']}",
                "status": "initialized",
                "plan_identity": {
                    "plan_id": record["plan_id"],
                    "plan_sha256": record["plan_sha256"],
                },
                "normalization_identity": {
                    "report_id": report["report_id"],
                    "report_content_sha256": report[
                        "report_content_sha256"
                    ],
                    "source_set_sha256": report["source_set_sha256"],
                },
                "activation_identity": {
                    "activation_id": accepted_activation["activation_id"],
                    "activation_receipt_sha256": (
                        activation_receipt_sha256
                    ),
                    "execution_profile_sha256": execution_profile[
                        "profile_content_sha256"
                    ],
                    "repository_topology_policy_sha256": content_sha256(
                        topology
                    ),
                    "activation_goal_sha256": accepted_activation[
                        "exact_activation_goal_sha256"
                    ],
                    "effective_from_generation": 1,
                },
                "outer_goal_identity": {
                    "goal_id": outer_goal_id,
                    "revision_before": expected_outer_revision,
                    "revision_after": expected_outer_revision + 1,
                },
                "repository_fingerprint": record[
                    "repository_fingerprint"
                ],
                "initial_fingerprint": record["state"]["fingerprints"][
                    "initial"
                ],
                "initial_lease": {
                    "authority": "outer_worktree",
                    "generation": lease["generation"],
                    "holder_kind": lease["holder_kind"],
                    "holder_token_sha256": holder_token_sha256(
                        outer_holder_token
                    ),
                    "transaction_id": lease["transaction_id"],
                    "expires_at": lease["expires_at"],
                },
                "materialized": {
                    "phase_count": len(record["plan"]["phases"]),
                    "task_count": len(record["plan"]["tasks"]),
                    "plan_revision": record["state"]["revision"],
                    "state_writes": 1,
                },
                "effect_counts": {
                    "provider_create_calls": 0,
                    "worker_discussions": 0,
                    "agentjobs_executed": 0,
                    "continue_invocations": 0,
                    "task_reservations": 0,
                    "branch_creations": 0,
                    "worktree_creations": 0,
                },
                "prior_journal_sha256": report_event_hash,
                "next_boundary": "reserve_first_task",
                "finalized_at": now,
                "finalized": True,
                "receipt_content_sha256": "",
            }
            receipt["receipt_content_sha256"] = content_sha256(
                {
                    key: item
                    for key, item in receipt.items()
                    if key != "receipt_content_sha256"
                }
            )
            receipt = self._require_initialization_receipt(receipt)
            append_plan_journal(
                record["journal"],
                "event",
                {
                    "event_type": "plan_initialization_finalized",
                    "plan_id": record["plan_id"],
                    "receipt_id": receipt["receipt_id"],
                    "receipt_content_sha256": receipt[
                        "receipt_content_sha256"
                    ],
                    "initialization_receipt": receipt,
                    "timestamp": now,
                },
            )
            validate_runtime_plan_record(
                record,
                plan_schema_path=self.plan_schema_path,
                state_schema_path=self.state_schema_path,
            )
            outer.event(
                "plan_profile_initialized",
                {
                    "plan_id": record["plan_id"],
                    "plan_sha256": record["plan_sha256"],
                    "normalization_report_id": report["report_id"],
                    "normalization_report_sha256": report[
                        "report_content_sha256"
                    ],
                    "initialization_receipt_id": receipt["receipt_id"],
                    "initialization_receipt_sha256": receipt[
                        "receipt_content_sha256"
                    ],
                    "activation_id": accepted_activation[
                        "activation_id"
                    ],
                    "activation_receipt_sha256": (
                        activation_receipt_sha256
                    ),
                    "reasoning_effort": execution_profile[
                        "reasoning_effort"
                    ],
                    "initial_lease_transaction_id": lease["transaction_id"],
                },
            )
            self._insert_plan_row(connection, record)
            persisted_activation_sha256 = self._insert_activation_receipt(
                connection,
                accepted_activation,
                activation_sequence=1,
            )
            if persisted_activation_sha256 != activation_receipt_sha256:
                raise IntegrityError(
                    "persisted activation receipt hash changed"
                )
            self._insert_base_children(connection, record)
            self._insert_events(
                connection,
                record["plan_id"],
                record["journal"],
            )
            self.goal_store._finalize_mutation(connection, outer)
            row = connection.execute(
                "SELECT * FROM plans WHERE plan_id=?",
                (record["plan_id"],),
            ).fetchone()
            created = self._record_from_row(connection, row)
            self._validate_row_parity(connection, row, created)
            evidence = self._initialization_evidence(created)
            if (
                evidence is None
                or evidence["initialization_receipt"] != receipt
            ):
                raise IntegrityError(
                    "plan initialization receipt was not durably recovered"
                )
            connection.commit()
            return created, receipt
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise StateConflict(
                "plan initialization conflicts with existing state",
                details={"database_error": str(error)},
            ) from error
        except sqlite3.OperationalError as error:
            connection.rollback()
            if "locked" in str(error).lower() or "busy" in str(error).lower():
                raise StateConflict(
                    "SQLite plan state is busy with another conforming writer",
                    details={"reason_code": "state.sqlite_busy"},
                ) from error
            raise
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def create_plan(
        self,
        *,
        plan: Mapping[str, Any],
        outer_goal_id: str,
        repository_fingerprint: str,
        initial_fingerprint: str,
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        if self.read_only:
            raise StateConflict("read-only plan store cannot create a plan")
        record = build_initial_plan_record(
            plan=plan,
            outer_goal_id=outer_goal_id,
            repository_fingerprint=repository_fingerprint,
            initial_fingerprint=initial_fingerprint,
            timestamp=timestamp or utc_now(),
            plan_schema_path=self.plan_schema_path,
            state_schema_path=self.state_schema_path,
        )
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            goal = connection.execute(
                "SELECT repository_binding_json FROM goals WHERE goal_id=?",
                (outer_goal_id,),
            ).fetchone()
            if goal is None:
                raise RecordNotFound(f"outer goal does not exist: {outer_goal_id}")
            outer_binding = self._parse_canonical_object(
                str(goal["repository_binding_json"]),
                label="outer goal repository binding",
            )
            if outer_binding != record["repository_binding"]:
                raise StateConflict(
                    "plan repository binding does not match the outer goal"
                )
            self._insert_plan_row(connection, record)
            self._insert_base_children(connection, record)
            self._insert_events(connection, record["plan_id"], record["journal"])
            row = connection.execute(
                "SELECT * FROM plans WHERE plan_id=?",
                (record["plan_id"],),
            ).fetchone()
            created = self._record_from_row(connection, row)
            self._validate_row_parity(connection, row, created)
            connection.commit()
            return created
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise StateConflict(
                "plan initialization conflicts with existing state",
                details={"database_error": str(error)},
            ) from error
        except sqlite3.OperationalError as error:
            connection.rollback()
            if "locked" in str(error).lower() or "busy" in str(error).lower():
                raise StateConflict(
                    "SQLite plan state is busy with another conforming writer",
                    details={"reason_code": "state.sqlite_busy"},
                ) from error
            raise
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def load_plan_initialization(
        self,
        plan_id: str,
    ) -> dict[str, Any] | None:
        connection = self.connect()
        try:
            record = self._load_plan(connection, plan_id)
            return self._initialization_evidence(record)
        finally:
            connection.close()

    def list_activation_receipts(
        self,
        plan_id: str,
    ) -> list[dict[str, Any]]:
        connection = self.connect()
        try:
            self._load_plan(connection, plan_id)
            return copy.deepcopy(
                self._activation_history(connection, plan_id)
            )
        finally:
            connection.close()

    def upgrade_execution_profile(
        self,
        plan_id: str,
        *,
        expected_revision: int,
        activation_receipt: Mapping[str, Any],
        activation_goal_text: str,
        repository_topology_policy: Mapping[str, Any],
        coordinator_holder_token: str,
        observed_repository_binding: Mapping[str, Any],
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        """Apply one accepted profile only at a verified coordinator boundary."""

        if self.read_only:
            raise StateConflict(
                "read-only plan store cannot upgrade an execution profile"
            )
        if (
            isinstance(expected_revision, bool)
            or not isinstance(expected_revision, int)
            or expected_revision < 1
        ):
            raise RecordValidationError(
                "expected_revision must be a positive integer"
            )
        if (
            not isinstance(coordinator_holder_token, str)
            or not coordinator_holder_token
        ):
            raise RecordValidationError(
                "coordinator_holder_token must be nonblank"
            )
        if (
            not isinstance(activation_goal_text, str)
            or not activation_goal_text.strip()
            or activation_goal_text != activation_goal_text.strip()
        ):
            raise RecordValidationError(
                "activation_goal_text must be exact canonical text"
            )
        now = timestamp or utc_now()
        parse_utc(now)
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM plans WHERE plan_id=?",
                (plan_id,),
            ).fetchone()
            if row is None:
                raise RecordNotFound(f"plan does not exist: {plan_id}")
            if int(row["state_revision"]) != expected_revision:
                raise StateConflict(
                    "plan revision changed before profile acceptance"
                )
            record = self._record_from_row(connection, row)
            self._validate_row_parity(connection, row, record)
            state = record["state"]
            unsafe_statuses = {
                str(task["task_id"]): str(task["status"])
                for task in state["tasks"]
                if task["status"]
                in {
                    "reserved",
                    "active",
                    "verifying",
                    "invocation_unknown",
                }
            }
            if unsafe_statuses:
                raise StateConflict(
                    "plan profile upgrade requires a safe task boundary",
                    details={
                        "reason_code": "plan_profile.unsafe_task_boundary",
                        "tasks": unsafe_statuses,
                    },
                )
            open_intent = connection.execute(
                "SELECT intent_id FROM plan_provider_intents "
                "WHERE plan_id=? AND status='intent' AND finalized=0",
                (plan_id,),
            ).fetchone()
            if open_intent is not None:
                raise StateConflict(
                    "plan profile upgrade is denied while provider intent is open",
                    details={
                        "reason_code": "plan_profile.open_provider_intent",
                        "intent_id": open_intent["intent_id"],
                    },
                )
            plan_lease = state.get("lease")
            if plan_lease is None:
                outer_row = connection.execute(
                    "SELECT record_json FROM goals WHERE goal_id=?",
                    (record["outer_goal_id"],),
                ).fetchone()
                outer = (
                    json.loads(str(outer_row["record_json"]))
                    if outer_row is not None
                    else {}
                )
                outer_lease = outer.get("state", {}).get("active_lease")
                initial_coordinator_boundary = (
                    state["current_generation"] == 0
                    and state["phase"] == "initialized"
                    and isinstance(outer_lease, Mapping)
                    and outer_lease.get("holder_kind")
                    in {"launcher", "continuation"}
                    and outer_lease.get("holder_token")
                    == coordinator_holder_token
                )
                lease_free_coordinator_boundary = (
                    state["current_generation"] > 0
                    and state["phase"] == "continuation_required"
                    and state["active_task_id"] is None
                    and outer_lease is None
                )
                if not (
                    initial_coordinator_boundary
                    or lease_free_coordinator_boundary
                ):
                    raise StateConflict(
                        "plan lease is not held at the coordinator boundary",
                        details={
                            "reason_code": "plan_profile.coordinator_required"
                        },
                    )
            elif (
                plan_lease.get("holder_kind") != "coordinator"
                or plan_lease.get("holder_token_hash")
                != holder_token_sha256(coordinator_holder_token)
            ):
                raise StateConflict(
                    "plan lease is not held by the accepting coordinator",
                    details={
                        "reason_code": "plan_profile.coordinator_required"
                    },
                )
            observed_binding = copy.deepcopy(
                dict(observed_repository_binding)
            )
            if observed_binding != record["repository_binding"]:
                raise StateConflict(
                    "repository binding changed before profile acceptance",
                    details={
                        "reason_code": "plan_profile.repository_binding_changed"
                    },
                )
            topology = self._require_topology_policy(
                repository_topology_policy,
                require_default_deny=(
                    record["runtime_profile_version"] == 1
                ),
            )
            if (
                record["runtime_profile_version"] == 2
                and topology != record["repository_topology_policy"]
            ):
                raise StateConflict(
                    "reasoning-profile acceptance cannot change topology policy",
                    details={
                        "reason_code": "plan_profile.topology_change_requires_authority"
                    },
                )
            from agentjob_runtime.plan.activation import (
                execution_profile_from_receipt,
                validate_activation_receipt,
            )

            accepted = validate_activation_receipt(
                activation_receipt,
                plan_id=record["plan_id"],
                accepted_plan_sha256=record["effective_plan_sha256"],
                goal_text=activation_goal_text,
                repository_binding=record["repository_binding"],
                repository_topology_policy=topology,
            )
            next_generation = int(state["current_generation"]) + 1
            prior_activation_id = (
                record["execution_profile"]["activation_id"]
                if record["runtime_profile_version"] == 2
                else None
            )
            if (
                accepted["effective_from_generation"] != next_generation
                or accepted["superseded_activation_id"]
                != prior_activation_id
            ):
                raise StateConflict(
                    "accepted profile has a stale generation or predecessor",
                    details={
                        "reason_code": "plan_profile.stale_acceptance",
                        "expected_effective_from_generation": next_generation,
                        "expected_superseded_activation_id": (
                            prior_activation_id
                        ),
                    },
                )
            profile = self._require_execution_profile(
                execution_profile_from_receipt(accepted)
            )
            next_sequence = int(record["activation_sequence"]) + 1
            receipt_sha256 = self._insert_activation_receipt(
                connection,
                accepted,
                activation_sequence=next_sequence,
            )
            record.update(
                {
                    "runtime_profile_version": 2,
                    "activation_sequence": next_sequence,
                    "activation_receipt_sha256": receipt_sha256,
                    "execution_profile": profile,
                    "repository_topology_policy": topology,
                    "activation_goal_text": activation_goal_text,
                    "activation_goal_sha256": accepted[
                        "exact_activation_goal_sha256"
                    ],
                    "profile_effective_from_generation": next_generation,
                    "repository_binding_sha256": content_sha256(
                        record["repository_binding"]
                    ),
                }
            )
            original_journal_length = len(record["journal"])
            append_plan_journal(
                record["journal"],
                "event",
                {
                    "event_type": "plan_execution_profile_superseded",
                    "plan_id": plan_id,
                    "activation_id": accepted["activation_id"],
                    "superseded_activation_id": prior_activation_id,
                    "activation_receipt_sha256": receipt_sha256,
                    "reasoning_effort": profile["reasoning_effort"],
                    "effective_from_generation": next_generation,
                    "coordinator_holder_token_sha256": (
                        holder_token_sha256(coordinator_holder_token)
                    ),
                    "timestamp": now,
                },
            )
            state["revision"] = expected_revision + 1
            state["updated_at"] = now
            record["updated_at"] = now
            replacements, _ = self._replacement_definitions(
                connection,
                record,
            )
            validate_runtime_plan_record(
                record,
                plan_schema_path=self.plan_schema_path,
                state_schema_path=self.state_schema_path,
                additional_tasks=replacements,
            )
            self._insert_events(
                connection,
                plan_id,
                record["journal"][original_journal_length:],
            )
            cursor = connection.execute(
                """
                UPDATE plans SET
                    state_json=?, state_revision=?, journal_head_sha256=?,
                    runtime_profile_version=2, activation_sequence=?,
                    activation_receipt_sha256=?,
                    execution_profile_json=?, topology_policy_json=?,
                    activation_goal_text=?, activation_goal_sha256=?,
                    profile_effective_from_generation=?,
                    repository_binding_sha256=?, updated_at=?
                WHERE plan_id=? AND state_revision=?
                """,
                (
                    canonical_json_bytes(state).decode("utf-8"),
                    state["revision"],
                    record["journal"][-1]["event_hash"],
                    next_sequence,
                    receipt_sha256,
                    canonical_json_bytes(profile).decode("utf-8"),
                    canonical_json_bytes(topology).decode("utf-8"),
                    activation_goal_text,
                    accepted["exact_activation_goal_sha256"],
                    next_generation,
                    record["repository_binding_sha256"],
                    now,
                    plan_id,
                    expected_revision,
                ),
            )
            if cursor.rowcount != 1:
                raise StateConflict(
                    "plan revision changed during profile upgrade"
                )
            updated_row = connection.execute(
                "SELECT * FROM plans WHERE plan_id=?",
                (plan_id,),
            ).fetchone()
            updated = self._record_from_row(connection, updated_row)
            self._validate_row_parity(
                connection,
                updated_row,
                updated,
            )
            connection.commit()
            return updated
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise StateConflict(
                "plan profile persistence rejected the accepted transition",
                details={"database_error": str(error)},
            ) from error
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def load_receipt(self, receipt_id: str) -> dict[str, Any]:
        connection = self.connect()
        try:
            row = connection.execute(
                "SELECT plan_id, record_json FROM plan_receipts WHERE receipt_id=?",
                (receipt_id,),
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            raise RecordNotFound(f"plan receipt does not exist: {receipt_id}")
        self.load_plan(str(row["plan_id"]))
        return self._require_task_receipt(
            self._parse_canonical_object(
                str(row["record_json"]),
                label=f"plan receipt {receipt_id}",
            )
        )

    def find_task_receipt(
        self,
        plan_id: str,
        task_id: str,
    ) -> dict[str, Any] | None:
        self.load_plan(plan_id)
        connection = self.connect()
        try:
            row = connection.execute(
                "SELECT record_json FROM plan_receipts "
                "WHERE plan_id=? AND task_id=? AND receipt_kind='task'",
                (plan_id, task_id),
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            return None
        return self._require_task_receipt(
            self._parse_canonical_object(
                str(row["record_json"]),
                label=f"plan receipt for task {task_id}",
            )
        )

    def list_receipts(self, plan_id: str) -> list[dict[str, Any]]:
        self.load_plan(plan_id)
        connection = self.connect()
        try:
            rows = list(
                connection.execute(
                    "SELECT record_json FROM plan_receipts WHERE plan_id=? "
                    "ORDER BY finalized_at, receipt_id",
                    (plan_id,),
                )
            )
        finally:
            connection.close()
        return [
            self._require_task_receipt(
                self._parse_canonical_object(
                    str(row["record_json"]),
                    label="plan receipt",
                )
            )
            for row in rows
        ]

    def load_provider_intent(self, intent_id: str) -> dict[str, Any]:
        connection = self.connect()
        try:
            row = connection.execute(
                "SELECT plan_id, record_json FROM plan_provider_intents "
                "WHERE intent_id=?",
                (intent_id,),
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            raise RecordNotFound(
                f"plan provider intent does not exist: {intent_id}"
            )
        self.load_plan(str(row["plan_id"]))
        return self._require_provider_intent(
            self._parse_canonical_object(
                str(row["record_json"]),
                label=f"plan provider intent {intent_id}",
            )
        )

    def find_provider_intent(
        self,
        plan_id: str,
        generation: int,
    ) -> dict[str, Any] | None:
        self.load_plan(plan_id)
        connection = self.connect()
        try:
            row = connection.execute(
                "SELECT record_json FROM plan_provider_intents "
                "WHERE plan_id=? AND generation=?",
                (plan_id, generation),
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            return None
        return self._require_provider_intent(
            self._parse_canonical_object(
                str(row["record_json"]),
                label=f"plan provider intent generation {generation}",
            )
        )

    def list_provider_intents(
        self,
        plan_id: str,
    ) -> list[dict[str, Any]]:
        """Return canonical provider evidence in generation order."""

        self.load_plan(plan_id)
        connection = self.connect()
        try:
            rows = list(
                connection.execute(
                    "SELECT record_json FROM plan_provider_intents "
                    "WHERE plan_id=? ORDER BY generation, intent_id",
                    (plan_id,),
                )
            )
        finally:
            connection.close()
        return [
            self._require_provider_intent(
                self._parse_canonical_object(
                    str(row["record_json"]),
                    label="plan provider intent",
                )
            )
            for row in rows
        ]

    def list_supersessions(self, plan_id: str) -> list[dict[str, Any]]:
        self.load_plan(plan_id)
        connection = self.connect()
        try:
            rows = list(
                connection.execute(
                    "SELECT record_json FROM plan_supersessions WHERE plan_id=? "
                    "ORDER BY created_at, supersession_id",
                    (plan_id,),
                )
            )
        finally:
            connection.close()
        return [
            self._require_supersession(
                self._parse_canonical_object(
                    str(row["record_json"]),
                    label="plan supersession",
                )
            )
            for row in rows
        ]

    def _selection_result(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> SelectionResult:
        replacements, supersessions = self._replacement_definitions(
            connection,
            record,
        )
        definitions = {
            item["task_id"]: item
            for item in self._base_definitions(record) + replacements
        }
        effective_task_ids: dict[str, list[str]] = {
            task_id: [] for task_id in definitions
        }
        for row in connection.execute(
            """
            SELECT effective.root_task_id, effective.effective_task_id
            FROM plan_effective_task_leaves_v1 AS effective
            JOIN plan_tasks AS root
              ON root.plan_id=effective.plan_id
             AND root.task_id=effective.root_task_id
            JOIN plan_tasks AS leaf
              ON leaf.plan_id=effective.plan_id
             AND leaf.task_id=effective.effective_task_id
            WHERE effective.plan_id=?
            ORDER BY root.canonical_position, root.task_id,
                     leaf.canonical_position, leaf.task_id
            """,
            (record["plan_id"],),
        ):
            effective_task_ids[str(row["root_task_id"])].append(
                str(row["effective_task_id"])
            )

        task_evidence: dict[str, dict[str, Any]] = {}
        for row in connection.execute(
            """
            SELECT state.task_id, state.lifecycle_status,
                   receipt.receipt_id, receipt.receipt_sha256,
                   receipt.disposition, receipt.acceptance_status,
                   receipt.validator_status, receipt.checkpoint_status
            FROM plan_task_states AS state
            JOIN plan_tasks AS task
              ON task.plan_id=state.plan_id
             AND task.task_id=state.task_id
            LEFT JOIN plan_receipts AS receipt
              ON receipt.plan_id=state.plan_id
             AND receipt.task_id=state.task_id
             AND receipt.receipt_kind='task'
             AND receipt.finalized=1
            WHERE state.plan_id=?
            ORDER BY task.canonical_position, task.task_id
            """,
            (record["plan_id"],),
        ):
            complete = (
                row["lifecycle_status"] == "completed"
                and row["disposition"] == "task_complete"
                and row["acceptance_status"] == "pass"
                and row["validator_status"] == "pass"
                and row["checkpoint_status"] in {"pass", "not_required"}
            )
            task_evidence[str(row["task_id"])] = {
                "lifecycle_status": row["lifecycle_status"],
                "receipt_id": row["receipt_id"],
                "receipt_sha256": row["receipt_sha256"],
                "complete": complete,
            }

        ready_task_ids = [
            str(row["task_id"])
            for row in connection.execute(
                "SELECT task_id FROM plan_ready_tasks_v1 "
                "WHERE plan_id=? ORDER BY canonical_position, task_id",
                (record["plan_id"],),
            )
        ]
        supersession_graph_sha256 = content_sha256(
            [
                {
                    "original_task_id": item["original_task"]["task_id"],
                    "replacement_task_ids": [
                        replacement["task_id"]
                        for replacement in item["replacement_tasks"]
                    ],
                    "replacement_graph_sha256": item[
                        "replacement_graph_sha256"
                    ],
                }
                for item in supersessions
            ]
        )
        return build_selection_result(
            record=record,
            definitions=definitions,
            effective_task_ids=effective_task_ids,
            task_evidence=task_evidence,
            ready_task_ids=ready_task_ids,
            supersession_graph_sha256=supersession_graph_sha256,
            selection_schema_path=self.selection_proof_schema_path,
        )

    def select_next_task(
        self,
        plan_id: str,
        *,
        expected_revision: int | None = None,
    ) -> SelectionResult:
        """Return one deterministic proof without mutating plan state."""

        connection = self.connect()
        try:
            connection.execute("BEGIN")
            record = self._load_plan(connection, plan_id)
            revision = int(record["state"]["revision"])
            if (
                expected_revision is not None
                and revision != expected_revision
            ):
                raise StateConflict(
                    f"stale plan revision: expected {expected_revision}, "
                    f"found {revision}",
                    details={
                        "expected_revision": expected_revision,
                        "actual_revision": revision,
                    },
                )
            result = self._selection_result(connection, record)
            connection.commit()
            return result
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def selection_proof_for_revision(
        self,
        plan_id: str,
        plan_revision: int,
    ) -> dict[str, Any] | None:
        self.load_plan(plan_id)
        connection = self.connect()
        try:
            row = connection.execute(
                "SELECT record_json FROM plan_selection_proofs "
                "WHERE plan_id=? AND plan_revision=?",
                (plan_id, plan_revision),
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            return None
        return self._require_selection_proof(
            self._parse_canonical_object(
                str(row["record_json"]),
                label=f"plan selection proof revision {plan_revision}",
            )
        )

    def dependency_completion(
        self,
        plan_id: str,
        task_id: str,
    ) -> dict[str, Any]:
        self.load_plan(plan_id)
        connection = self.connect()
        try:
            task_row = connection.execute(
                "SELECT task_id FROM plan_tasks WHERE plan_id=? AND task_id=?",
                (plan_id, task_id),
            ).fetchone()
            if task_row is None:
                raise RecordNotFound(f"plan task does not exist: {task_id}")
            roots = [
                str(row["depends_on_task_id"])
                for row in connection.execute(
                    "SELECT depends_on_task_id FROM plan_task_dependencies "
                    "WHERE plan_id=? AND task_id=? ORDER BY dependency_position",
                    (plan_id, task_id),
                )
            ]
            dependencies: list[dict[str, Any]] = []
            for root_task_id in roots:
                leaves: list[dict[str, Any]] = []
                for row in connection.execute(
                    """
                    SELECT effective.effective_task_id, task.task_sha256,
                           state.lifecycle_status, receipt.receipt_id,
                           receipt.receipt_sha256, receipt.disposition,
                           receipt.acceptance_status, receipt.validator_status,
                           receipt.checkpoint_status
                    FROM plan_effective_task_leaves_v1 AS effective
                    JOIN plan_tasks AS task
                      ON task.plan_id=effective.plan_id
                     AND task.task_id=effective.effective_task_id
                    LEFT JOIN plan_task_states AS state
                      ON state.plan_id=effective.plan_id
                     AND state.task_id=effective.effective_task_id
                    LEFT JOIN plan_receipts AS receipt
                      ON receipt.plan_id=effective.plan_id
                     AND receipt.task_id=effective.effective_task_id
                     AND receipt.receipt_kind='task'
                     AND receipt.finalized=1
                    WHERE effective.plan_id=? AND effective.root_task_id=?
                    ORDER BY task.canonical_position, task.task_id
                    """,
                    (plan_id, root_task_id),
                ):
                    complete = (
                        row["lifecycle_status"] == "completed"
                        and row["disposition"] == "task_complete"
                        and row["acceptance_status"] == "pass"
                        and row["validator_status"] == "pass"
                        and row["checkpoint_status"] in {"pass", "not_required"}
                    )
                    leaves.append(
                        {
                            "task_id": str(row["effective_task_id"]),
                            "task_sha256": str(row["task_sha256"]),
                            "lifecycle_status": row["lifecycle_status"],
                            "receipt_id": row["receipt_id"],
                            "receipt_sha256": row["receipt_sha256"],
                            "complete": complete,
                        }
                    )
                if not leaves:
                    raise IntegrityError(
                        "plan dependency has no effective task leaf",
                        details={
                            "task_id": task_id,
                            "dependency_task_id": root_task_id,
                        },
                    )
                dependencies.append(
                    {
                        "task_id": root_task_id,
                        "effective_leaves": leaves,
                        "complete": all(item["complete"] for item in leaves),
                    }
                )
        finally:
            connection.close()
        return {
            "plan_id": plan_id,
            "task_id": task_id,
            "dependencies": dependencies,
            "all_complete": all(item["complete"] for item in dependencies),
        }

    def _definitions(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
    ) -> dict[str, dict[str, Any]]:
        replacements, _ = self._replacement_definitions(connection, record)
        return {
            item["task_id"]: item
            for item in self._base_definitions(record) + replacements
        }

    def _insert_selection_proof(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        value: Mapping[str, Any],
        *,
        timestamp: str,
    ) -> str:
        proof = self._require_selection_proof(value)
        selected = proof["selected_task"]
        if (
            proof["outcome"] != "selected"
            or not isinstance(selected, Mapping)
            or proof["plan_id"] != record["plan_id"]
            or proof["plan_sha256"]
            != record["effective_plan_sha256"]
            or proof["plan_revision"] != record["state"]["revision"]
            or proof["prior_journal_sha256"]
            != record["journal"][-1]["event_hash"]
            or proof["repository_fingerprint"]
            != record["repository_fingerprint"]
        ):
            raise StateConflict(
                "selection proof is not bound to the current plan revision"
            )
        definitions = self._definitions(connection, record)
        definition = definitions.get(str(selected["task_id"]))
        if (
            definition is None
            or selected["task_sha256"] != definition["task_sha256"]
            or selected["canonical_position"]
            != definition["canonical_position"]
        ):
            raise StateConflict(
                "selection proof task identity differs from canonical state"
            )
        proof_sha256 = content_sha256(proof)
        connection.execute(
            """
            INSERT INTO plan_selection_proofs(
                proof_id, plan_id, plan_revision, outcome,
                selected_task_id, record_json, proof_sha256,
                finalized, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
            """,
            (
                proof["proof_id"],
                record["plan_id"],
                proof["plan_revision"],
                proof["outcome"],
                selected["task_id"],
                canonical_json_bytes(proof).decode("utf-8"),
                proof_sha256,
                timestamp,
            ),
        )
        return proof_sha256

    def _insert_task_receipt(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        value: Mapping[str, Any],
    ) -> str:
        receipt = self._require_task_receipt(value)
        if receipt["disposition"] == "plan_complete":
            raise RecordValidationError(
                "plan-complete persistence requires the later completion boundary"
            )
        definitions = self._definitions(connection, record)
        plan_identity = receipt["plan_identity"]
        task_identity = receipt["task_identity"]
        relay_identity = receipt["relay_identity"]
        task_id = str(task_identity["task_id"])
        definition = definitions.get(task_id)
        if (
            definition is None
            or plan_identity["plan_id"] != record["plan_id"]
            or plan_identity["plan_sha256"]
            not in {record["plan_sha256"], record["effective_plan_sha256"]}
            or plan_identity["phase_id"] != definition["phase_id"]
            or task_identity["task_sha256"] != definition["task_sha256"]
            or receipt["journal"]["prior_hash"]
            != record["journal"][-1]["event_hash"]
        ):
            raise RecordValidationError(
                "plan task receipt is not bound to current canonical state"
            )
        projection = self._receipt_projection(receipt)
        self._validate_v2_receipt_profile(
            connection,
            record,
            receipt,
        )
        receipt_sha256 = content_sha256(receipt)
        connection.execute(
            """
            INSERT INTO plan_receipts(
                receipt_id, plan_id, receipt_kind, task_id, phase_id,
                generation, disposition, reason_code, acceptance_status,
                validator_status, checkpoint_status, record_json,
                receipt_sha256, finalized, finalized_at
            ) VALUES (?, ?, 'task', ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
            """,
            (
                receipt["receipt_id"],
                record["plan_id"],
                task_id,
                relay_identity["generation"],
                receipt["disposition"],
                receipt["reason_code"],
                projection["acceptance_status"],
                projection["validator_status"],
                projection["checkpoint_status"],
                canonical_json_bytes(receipt).decode("utf-8"),
                receipt_sha256,
                receipt["finished_at"],
            ),
        )
        return receipt_sha256

    def _insert_supersession(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        value: Mapping[str, Any],
        *,
        timestamp: str,
    ) -> str:
        supersession = self._require_supersession(value)
        definitions = self._definitions(connection, record)
        original = supersession["original_task"]
        original_id = str(original["task_id"])
        original_definition = definitions.get(original_id)
        if (
            original_definition is None
            or supersession["plan_id"] != record["plan_id"]
            or supersession["plan_sha256"]
            not in {record["plan_sha256"], record["effective_plan_sha256"]}
            or original["task_sha256"] != original_definition["task_sha256"]
            or supersession["prior_journal_sha256"]
            != record["journal"][-1]["event_hash"]
        ):
            raise RecordValidationError(
                "plan supersession is not bound to current canonical state"
            )
        receipt_row = connection.execute(
            "SELECT record_json, receipt_sha256, task_id FROM plan_receipts "
            "WHERE receipt_id=? AND plan_id=?",
            (original["receipt_id"], record["plan_id"]),
        ).fetchone()
        if receipt_row is None:
            raise RecordValidationError(
                "plan supersession requires the exact original task receipt"
            )
        receipt = self._require_task_receipt(
            self._parse_canonical_object(
                str(receipt_row["record_json"]),
                label="supersession original receipt",
            )
        )
        disposition_by_terminal = {
            "replan_required": "replan_required",
            "blocked": "blocked",
            "validation_failed": "validation_failed",
            "human_gate_required": "human_gate_required",
        }
        if (
            receipt_row["receipt_sha256"] != original["receipt_sha256"]
            or receipt_row["task_id"] != original_id
            or receipt["task_identity"]["task_sha256"]
            != original["task_sha256"]
            or receipt["relay_identity"]["generation"] != original["generation"]
            or receipt["disposition"]
            != disposition_by_terminal[original["terminal_status"]]
        ):
            raise RecordValidationError(
                "plan supersession original receipt identity is invalid"
            )
        replacements = list(supersession["replacement_tasks"])
        graph_basis = [
            {
                "task_id": item["task_id"],
                "task_sha256": item["task_sha256"],
                "depends_on": item["depends_on"],
                "canonical_position": item["canonical_position"],
            }
            for item in replacements
        ]
        if supersession["replacement_graph_sha256"] != content_sha256(graph_basis):
            raise RecordValidationError(
                "plan supersession replacement graph hash is invalid"
            )
        replacement_ids = [str(item["task_id"]) for item in replacements]
        replacement_id_set = set(replacement_ids)
        occupied_positions = {
            int(item["canonical_position"]) for item in definitions.values()
        }
        allowed_dependencies = set(definitions) | replacement_id_set
        if (
            len(replacement_id_set) != len(replacement_ids)
            or original_id in replacement_id_set
            or replacement_id_set.intersection(definitions)
            or len(
                {
                    int(item["canonical_position"])
                    for item in replacements
                }
            )
            != len(replacements)
        ):
            raise RecordValidationError(
                "plan supersession replacement identities are duplicated"
            )
        graph: dict[str, list[str]] = {}
        for item in replacements:
            task_id = str(item["task_id"])
            dependencies = [str(value) for value in item["depends_on"]]
            if (
                int(item["canonical_position"]) in occupied_positions
                or task_id in dependencies
                or any(value not in allowed_dependencies for value in dependencies)
            ):
                raise RecordValidationError(
                    "plan supersession replacement definition is invalid"
                )
            graph[task_id] = [
                dependency
                for dependency in dependencies
                if dependency in replacement_id_set
            ]
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(task_id: str) -> None:
            if task_id in visiting:
                raise RecordValidationError(
                    "plan supersession replacement dependency cycle"
                )
            if task_id in visited:
                return
            visiting.add(task_id)
            for dependency in graph[task_id]:
                visit(dependency)
            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in sorted(graph):
            visit(task_id)
        mapped_ids = {
            str(task_id)
            for mapping in supersession["acceptance_mapping"]
            for task_id in mapping["replacement_task_ids"]
        }
        if not mapped_ids <= replacement_id_set:
            raise RecordValidationError(
                "plan supersession acceptance mapping is invalid"
            )
        supersession_sha256 = content_sha256(supersession)
        connection.execute(
            """
            INSERT INTO plan_supersessions(
                supersession_id, plan_id, original_task_id,
                original_task_sha256, original_receipt_id,
                replacement_graph_sha256, reason_code, record_json,
                supersession_sha256, finalized, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
            """,
            (
                supersession["supersession_id"],
                record["plan_id"],
                original_id,
                original["task_sha256"],
                original["receipt_id"],
                supersession["replacement_graph_sha256"],
                supersession["reason_code"],
                canonical_json_bytes(supersession).decode("utf-8"),
                supersession_sha256,
                timestamp,
            ),
        )
        for item in replacements:
            connection.execute(
                """
                INSERT INTO plan_tasks(
                    plan_id, task_id, task_sha256, phase_id,
                    canonical_position, origin_kind, task_json
                ) VALUES (?, ?, ?, ?, ?, 'replacement', ?)
                """,
                (
                    record["plan_id"],
                    item["task_id"],
                    item["task_sha256"],
                    original_definition["phase_id"],
                    item["canonical_position"],
                    canonical_json_bytes(item).decode("utf-8"),
                ),
            )
        for item in replacements:
            for dependency_position, dependency in enumerate(item["depends_on"]):
                connection.execute(
                    """
                    INSERT INTO plan_task_dependencies(
                        plan_id, task_id, depends_on_task_id, dependency_position
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (
                        record["plan_id"],
                        item["task_id"],
                        dependency,
                        dependency_position,
                    ),
                )
        for replacement_position, item in enumerate(replacements):
            connection.execute(
                """
                INSERT INTO plan_supersession_replacements(
                    supersession_id, plan_id, replacement_task_id,
                    replacement_position
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    supersession["supersession_id"],
                    record["plan_id"],
                    item["task_id"],
                    replacement_position,
                ),
            )
        for mapping in supersession["acceptance_mapping"]:
            for replacement_task_id in mapping["replacement_task_ids"]:
                connection.execute(
                    """
                    INSERT INTO plan_supersession_acceptance(
                        supersession_id, criterion_id, replacement_task_id,
                        shared_gate_ref
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (
                        supersession["supersession_id"],
                        mapping["criterion_id"],
                        replacement_task_id,
                        mapping["shared_gate_ref"],
                    ),
                )
        return supersession_sha256

    def _insert_provider_intent(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        value: Mapping[str, Any],
        *,
        expected_revision: int,
        timestamp: str,
    ) -> str:
        intent = self._require_provider_intent(value)
        definitions = self._definitions(connection, record)
        definition = definitions.get(str(intent["task_id"]))
        if (
            intent["status"] != "intent"
            or intent["finalized"]
            or intent["plan_id"] != record["plan_id"]
            or intent["plan_sha256"]
            not in {record["plan_sha256"], record["effective_plan_sha256"]}
            or definition is None
            or intent["task_sha256"] != definition["task_sha256"]
            or intent["expected_revision"] != expected_revision
            or intent["repository_fingerprint"]
            != record["state"]["repository_fingerprint"]
            or intent["created_at"] != timestamp
            or intent["prior_journal_sha256"]
            != record["journal"][-1]["event_hash"]
            or (
                intent["schema_version"]
                == "sys4ai.plan-provider-intent.v2"
                and (
                    record.get("runtime_profile_version") != 2
                    or intent["execution_profile_sha256"]
                    != content_sha256(record["execution_profile"])
                    or intent["requested_reasoning_effort"]
                    != record["execution_profile"]["reasoning_effort"]
                    or intent["repository_binding_sha256"]
                    != record["repository_binding_sha256"]
                    or intent["generation"]
                    < record["execution_profile"][
                        "effective_from_generation"
                    ]
                )
            )
        ):
            raise RecordValidationError(
                "plan provider intent is not bound to current canonical state"
            )
        intent_sha256 = content_sha256(intent)
        connection.execute(
            """
            INSERT INTO plan_provider_intents(
                intent_id, plan_id, task_id, task_sha256, generation,
                provider_id, idempotency_key, handoff_token_sha256,
                predecessor_thread_id, expected_revision,
                repository_fingerprint, status, provider_create_budget,
                create_attempts, returned_thread_id, provider_response_sha256,
                retry_authorized, record_json, intent_sha256, finalized,
                created_at, updated_at, execution_profile_sha256,
                requested_reasoning_effort, effective_reasoning_effort,
                profile_verification_status, profile_evidence_ref,
                environment_mode, repository_binding_sha256,
                observed_topology_sha256, same_thread_profile_repair_json
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                intent["intent_id"],
                record["plan_id"],
                intent["task_id"],
                intent["task_sha256"],
                intent["generation"],
                intent["provider_id"],
                intent["idempotency_key"],
                intent["handoff_token_sha256"],
                intent["predecessor_thread_id"],
                intent["expected_revision"],
                intent["repository_fingerprint"],
                intent["status"],
                intent["provider_create_budget"],
                intent["create_attempts"],
                intent["returned_thread_id"],
                intent["provider_response_sha256"],
                int(intent["retry_authorized"]),
                canonical_json_bytes(intent).decode("utf-8"),
                intent_sha256,
                int(intent["finalized"]),
                intent["created_at"],
                timestamp,
                intent.get("execution_profile_sha256"),
                intent.get("requested_reasoning_effort"),
                intent.get("effective_reasoning_effort"),
                intent.get("profile_verification_status"),
                intent.get("profile_evidence_ref"),
                intent.get("environment_mode"),
                intent.get("repository_binding_sha256"),
                intent.get("observed_topology_sha256"),
                (
                    canonical_json_bytes(
                        intent["same_thread_profile_repair"]
                    ).decode("utf-8")
                    if intent.get("same_thread_profile_repair") is not None
                    else None
                ),
            ),
        )
        return intent_sha256

    def _finalize_provider_intent(
        self,
        connection: sqlite3.Connection,
        record: Mapping[str, Any],
        value: Mapping[str, Any],
        *,
        timestamp: str,
    ) -> str:
        intent = self._require_provider_intent(value)
        row = connection.execute(
            "SELECT * FROM plan_provider_intents WHERE intent_id=? AND plan_id=?",
            (intent["intent_id"], record["plan_id"]),
        ).fetchone()
        if row is None:
            raise RecordNotFound(
                f"plan provider intent does not exist: {intent['intent_id']}"
            )
        prior = self._require_provider_intent(
            self._parse_canonical_object(
                str(row["record_json"]),
                label="existing plan provider intent",
            )
        )
        immutable_fields = (
            "schema_version",
            "intent_id",
            "plan_id",
            "plan_sha256",
            "task_id",
            "task_sha256",
            "generation",
            "provider_id",
            "idempotency_key",
            "handoff_token_sha256",
            "predecessor_thread_id",
            "expected_revision",
            "repository_fingerprint",
            "created_at",
            "provider_create_budget",
            "retry_authorized",
            "prior_journal_sha256",
            "hash_basis",
            "extensions",
        )
        if prior["schema_version"] == "sys4ai.plan-provider-intent.v2":
            immutable_fields += (
                "execution_profile_sha256",
                "requested_reasoning_effort",
                "environment_mode",
                "repository_binding_sha256",
            )
        if (
            prior["status"] != "intent"
            or prior["finalized"]
            or intent["status"] == "intent"
            or not intent["finalized"]
            or any(intent[field] != prior[field] for field in immutable_fields)
            or (
                intent["returned_thread_id"] is not None
                and intent["returned_thread_id"]
                == intent["predecessor_thread_id"]
            )
        ):
            raise RecordValidationError(
                "plan provider outcome is not an identity-preserving finalization"
            )
        intent_sha256 = content_sha256(intent)
        connection.execute(
            """
            UPDATE plan_provider_intents SET
                status=?, create_attempts=?, returned_thread_id=?,
                provider_response_sha256=?, record_json=?, intent_sha256=?,
                finalized=1, updated_at=?,
                effective_reasoning_effort=?,
                profile_verification_status=?, profile_evidence_ref=?,
                observed_topology_sha256=?,
                same_thread_profile_repair_json=?
            WHERE intent_id=? AND plan_id=? AND finalized=0 AND status='intent'
            """,
            (
                intent["status"],
                intent["create_attempts"],
                intent["returned_thread_id"],
                intent["provider_response_sha256"],
                canonical_json_bytes(intent).decode("utf-8"),
                intent_sha256,
                timestamp,
                intent.get("effective_reasoning_effort"),
                intent.get("profile_verification_status"),
                intent.get("profile_evidence_ref"),
                intent.get("observed_topology_sha256"),
                (
                    canonical_json_bytes(
                        intent["same_thread_profile_repair"]
                    ).decode("utf-8")
                    if intent.get("same_thread_profile_repair") is not None
                    else None
                ),
                intent["intent_id"],
                record["plan_id"],
            ),
        )
        if connection.execute("SELECT changes()").fetchone()[0] != 1:
            raise StateConflict("plan provider intent was already finalized")
        return intent_sha256

    @contextmanager
    def mutation(
        self,
        plan_id: str,
        *,
        expected_revision: int,
        timestamp: str | None = None,
    ) -> Iterator[PlanMutation]:
        if self.read_only:
            raise StateConflict("read-only plan store cannot mutate a plan")
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM plans WHERE plan_id=?",
                (plan_id,),
            ).fetchone()
            if row is None:
                raise RecordNotFound(f"plan does not exist: {plan_id}")
            if row["state_revision"] != expected_revision:
                raise StateConflict(
                    f"stale plan revision: expected {expected_revision}, "
                    f"found {row['state_revision']}",
                    details={
                        "expected_revision": expected_revision,
                        "actual_revision": row["state_revision"],
                    },
                )
            record = self._record_from_row(connection, row)
            self._validate_row_parity(connection, row, record)
            original_state = copy.deepcopy(record["state"])
            original_journal_length = len(record["journal"])
            immutable = {
                key: copy.deepcopy(record[key])
                for key in (
                    "plan_id",
                    "outer_goal_id",
                    "plan_sha256",
                    "effective_plan_sha256",
                    "repository_binding",
                    "repository_fingerprint",
                    "plan",
                    "runtime_profile_version",
                    "activation_sequence",
                    "activation_receipt_sha256",
                    "execution_profile",
                    "repository_topology_policy",
                    "activation_goal_text",
                    "activation_goal_sha256",
                    "profile_effective_from_generation",
                    "repository_binding_sha256",
                    "created_at",
                )
            }
            mutation = PlanMutation(
                record,
                timestamp or utc_now(),
                connection,
                self,
                expected_revision,
            )
            yield mutation
            if len(record["journal"]) <= original_journal_length:
                raise RecordValidationError(
                    "plan mutation requires at least one append-only journal event"
                )
            if any(record[key] != value for key, value in immutable.items()):
                raise RecordValidationError(
                    "plan mutation attempted to change immutable plan identity"
                )
            validate_plan_transition(original_state, record["state"])
            record["state"]["revision"] = expected_revision + 1
            record["state"]["updated_at"] = mutation.timestamp
            record["updated_at"] = mutation.timestamp
            replacement_definitions, _ = self._replacement_definitions(
                connection,
                record,
            )
            validate_runtime_plan_record(
                record,
                plan_schema_path=self.plan_schema_path,
                state_schema_path=self.state_schema_path,
                additional_tasks=replacement_definitions,
            )
            self._insert_events(
                connection,
                plan_id,
                record["journal"][original_journal_length:],
            )
            state = record["state"]
            cursor = connection.execute(
                """
                UPDATE plans SET
                    state_json=?, state_revision=?, phase=?,
                    current_generation=?, active_task_id=?, evaluation=?,
                    current_fingerprint=?, journal_head_sha256=?,
                    terminal_reason=?, updated_at=?
                WHERE plan_id=? AND state_revision=?
                """,
                (
                    canonical_json_bytes(state).decode("utf-8"),
                    state["revision"],
                    state["phase"],
                    state["current_generation"],
                    state["active_task_id"],
                    state["evaluation"],
                    state["fingerprints"]["current"],
                    record["journal"][-1]["event_hash"],
                    state["terminal_reason"],
                    record["updated_at"],
                    plan_id,
                    expected_revision,
                ),
            )
            if cursor.rowcount != 1:
                raise StateConflict("plan revision changed during transaction")
            definitions = self._base_definitions(record) + replacement_definitions
            self._sync_task_states(
                connection,
                record,
                {item["task_id"]: item for item in definitions},
            )
            if mutation._outer_mutation is not None:
                self.goal_store._finalize_mutation(
                    connection,
                    mutation._outer_mutation,
                )
            updated_row = connection.execute(
                "SELECT * FROM plans WHERE plan_id=?",
                (plan_id,),
            ).fetchone()
            updated = self._record_from_row(connection, updated_row)
            self._validate_row_parity(connection, updated_row, updated)
            connection.commit()
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise StateConflict(
                "plan state constraint rejected the transition",
                details={"database_error": str(error)},
            ) from error
        except sqlite3.OperationalError as error:
            connection.rollback()
            if "locked" in str(error).lower() or "busy" in str(error).lower():
                raise StateConflict(
                    "SQLite plan state is busy with another conforming writer",
                    details={"reason_code": "state.sqlite_busy"},
                ) from error
            raise
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
