"""Revision-checked worktree lease operations."""

from __future__ import annotations

import copy
import secrets
from typing import Any

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.model import HOLDER_KINDS, add_seconds, parse_utc, utc_now
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


DEFAULT_LEASE_SECONDS = 300


def require_active_lease(
    record: dict[str, Any],
    *,
    generation: int | None = None,
    holder_token: str | None = None,
    holder_kinds: set[str] | None = None,
) -> dict[str, Any]:
    lease = record["state"].get("active_lease")
    if lease is None:
        raise StateConflict("goal has no active lease")
    if generation is not None and lease["generation"] != generation:
        raise StateConflict("lease generation mismatch")
    if holder_token is not None and lease["holder_token"] != holder_token:
        raise StateConflict("lease holder token mismatch")
    if holder_kinds is not None and lease["holder_kind"] not in holder_kinds:
        raise StateConflict("lease holder kind mismatch")
    return lease


def transfer_lease(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    current_holder_token: str,
    generation: int,
    holder_kind: str,
    holder_token: str | None = None,
    timestamp: str | None = None,
    lease_seconds: int = DEFAULT_LEASE_SECONDS,
) -> dict[str, Any]:
    if holder_kind not in HOLDER_KINDS:
        raise RecordValidationError(f"invalid lease holder kind: {holder_kind}")
    if not isinstance(lease_seconds, int) or lease_seconds <= 0:
        raise RecordValidationError("lease_seconds must be a positive integer")
    now = timestamp or utc_now()
    parse_utc(now)
    next_token = holder_token or secrets.token_hex(24)
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        prior = require_active_lease(mutation.record, holder_token=current_holder_token)
        mutation.replace_lease(
            generation=generation,
            holder_kind=holder_kind,
            holder_token=next_token,
            expires_at=add_seconds(now, lease_seconds),
        )
        mutation.event(
            "lease_transferred",
            {
                "generation": generation,
                "prior_holder_kind": prior["holder_kind"],
                "holder_kind": holder_kind,
                "transaction_id": mutation.record["state"]["active_lease"]["transaction_id"],
            },
        )
    return store.load_goal(goal_id)


def heartbeat_lease(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    holder_token: str,
    timestamp: str | None = None,
    lease_seconds: int = DEFAULT_LEASE_SECONDS,
) -> dict[str, Any]:
    if not isinstance(lease_seconds, int) or lease_seconds <= 0:
        raise RecordValidationError("lease_seconds must be a positive integer")
    now = timestamp or utc_now()
    parse_utc(now)
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        lease = require_active_lease(mutation.record, holder_token=holder_token)
        mutation.heartbeat(expires_at=add_seconds(now, lease_seconds))
        mutation.event(
            "lease_heartbeat",
            {"generation": lease["generation"], "transaction_id": lease["transaction_id"]},
        )
    return store.load_goal(goal_id)


def quarantine_lease(
    store: SQLiteGoalStore,
    *,
    goal_id: str,
    expected_revision: int,
    current_holder_token: str,
    reason: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    if not reason.strip():
        raise RecordValidationError("quarantine reason must be nonblank")
    now = timestamp or utc_now()
    with store.mutation(goal_id, expected_revision=expected_revision, timestamp=now) as mutation:
        prior = require_active_lease(mutation.record, holder_token=current_holder_token)
        quarantine_token = secrets.token_hex(24)
        mutation.replace_lease(
            generation=prior["generation"],
            holder_kind="quarantined",
            holder_token=quarantine_token,
            expires_at=add_seconds(now, DEFAULT_LEASE_SECONDS),
        )
        mutation.record["state"]["phase"] = "recovery_pending"
        mutation.record["state"]["terminal_reason"] = reason
        mutation.event(
            "lease_quarantined",
            {"generation": prior["generation"], "reason": reason},
        )
    return store.load_goal(goal_id)


def lease_diagnostics(
    store: SQLiteGoalStore,
    goal_id: str,
    *,
    timestamp: str | None = None,
) -> dict[str, Any]:
    record = store.load_goal(goal_id)
    lease = record["state"].get("active_lease")
    if lease is None:
        return {"status": "released", "expired": False, "steal_authorized": False, "lease": None}
    now = parse_utc(timestamp or utc_now())
    return {
        "status": "quarantined" if lease["holder_kind"] == "quarantined" else "active",
        "expired": now >= parse_utc(lease["expires_at"]),
        "steal_authorized": False,
        "lease": copy.deepcopy(lease),
    }
