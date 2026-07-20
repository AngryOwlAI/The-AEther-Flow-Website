"""Profile-preserving plan successor recovery without duplicate creation."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from agentjob_runtime.errors import StateConflict
from agentjob_runtime.goal.model import add_seconds, parse_utc, utc_now
from agentjob_runtime.plan.lifecycle import holder_token_sha256
from agentjob_runtime.plan.sqlite_store import SQLitePlanStore
from agentjob_runtime.records.canonical import content_sha256


def adopt_quarantined_plan_successor(
    store: SQLitePlanStore,
    *,
    plan_id: str,
    expected_revision: int,
    expected_outer_revision: int,
    generation: int,
    quarantine_token: str,
    handoff_token: str,
    successor_thread_id: str,
    effective_reasoning_effort: str,
    profile_evidence_ref: str,
    observed_repository_binding: Mapping[str, Any],
    observed_repository_topology: Mapping[str, Any],
    timestamp: str | None = None,
    expires_at: str | None = None,
) -> dict[str, Any]:
    """Adopt one proven candidate while preserving the finalized intent."""

    now = timestamp or utc_now()
    parse_utc(now)
    record = store.load_plan(plan_id)
    outer = store.goal_store.load_goal(record["outer_goal_id"])
    intent = store.find_provider_intent(plan_id, generation)
    lease = record["state"].get("lease")
    profile = record.get("execution_profile")
    binding = copy.deepcopy(dict(observed_repository_binding))
    topology = copy.deepcopy(dict(observed_repository_topology))
    if (
        record["state"]["revision"] != expected_revision
        or outer["state"]["revision"] != expected_outer_revision
        or not isinstance(intent, Mapping)
        or intent["status"] not in {"ambiguous", "timeout", "duplicate"}
        or intent["finalized"] is not True
        or intent["create_attempts"] != 1
        or intent["retry_authorized"] is not False
        or not isinstance(lease, Mapping)
        or lease["holder_kind"] != "quarantined"
        or lease["holder_token_hash"]
        != holder_token_sha256(quarantine_token)
        or intent["handoff_token_sha256"]
        != holder_token_sha256(handoff_token)
        or not isinstance(profile, Mapping)
        or effective_reasoning_effort != profile["reasoning_effort"]
        or not profile_evidence_ref.strip()
        or binding != record["repository_binding"]
        or topology.get("branch") != binding.get("branch")
        or topology.get("worktree") != binding.get("worktree")
        or any(
            topology.get(field) != binding.get(field)
            for field in ("root", "git_common_dir")
            if field in topology
        )
        or not successor_thread_id.strip()
        or successor_thread_id == intent["predecessor_thread_id"]
    ):
        raise StateConflict(
            "quarantined plan adoption lacks exact profile or repository evidence"
        )
    topology_sha256 = content_sha256(topology)
    expiry = expires_at or add_seconds(now, 900)
    with store.mutation(
        plan_id,
        expected_revision=expected_revision,
        timestamp=now,
    ) as mutation:
        mutation.record_recovery_adoption(
            task_id=str(intent["task_id"]),
            generation=generation,
            successor_thread_id=successor_thread_id,
            effective_reasoning_effort=effective_reasoning_effort,
            profile_evidence_ref=profile_evidence_ref,
            observed_topology_sha256=topology_sha256,
        )
        mutation.transfer_plan_lease(
            expected_outer_revision=expected_outer_revision,
            current_holder_token=quarantine_token,
            holder_kind="successor_reserved",
            holder_token=handoff_token,
            expires_at=expiry,
        )
    updated = store.load_plan(plan_id)
    if store.load_provider_intent(intent["intent_id"]) != intent:
        raise StateConflict(
            "recovery adoption changed the original provider intent"
        )
    return updated
