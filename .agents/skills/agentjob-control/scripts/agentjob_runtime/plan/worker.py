"""Profile-aware bounded implementation-plan task worker."""

from __future__ import annotations

import copy
import secrets
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from agentjob_runtime.continue_flow.director import (
    DirectorRoute,
    _route_legality,
)
from agentjob_runtime.errors import (
    AgentJobControlError,
    IntegrityError,
    RecordValidationError,
    StateConflict,
)
from agentjob_runtime.execution.repository_topology import (
    assert_topology_transition,
)
from agentjob_runtime.goal.model import add_seconds, parse_utc, utc_now
from agentjob_runtime.plan.lifecycle import holder_token_sha256
from agentjob_runtime.plan.prompts import (
    PLAN_TASK_REPOSITORY_FIELDS,
    build_plan_task_dependency_proof,
)
from agentjob_runtime.plan.sqlite_store import SQLitePlanStore
from agentjob_runtime.plan.verify import verify_plan_task_result
from agentjob_runtime.records.canonical import (
    canonical_json_bytes,
    content_sha256,
)
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import (
    format_issues,
    validate_instance,
)


@dataclass(frozen=True)
class PlanWorkerPreclaim:
    """Immutable evidence established before any task mutation."""

    plan_id: str
    task_id: str
    generation: int
    plan_revision: int
    outer_goal_revision: int
    current_thread_id: str
    reasoning_effort: str
    provider_id: str
    provider_evidence_ref: str
    pre_task_topology_sha256: str
    predecessor_thread_id: str | None
    envelope_sha256: str
    selection_proof_sha256: str
    task_definition_sha256: str
    dependency_proof_sha256: str
    provider_intent_sha256: str
    repository_binding_sha256: str


@dataclass(frozen=True)
class PlanTaskClaimResult:
    """Structured, non-secret evidence for one atomic task-generation claim."""

    status: str
    plan_id: str
    task_id: str
    generation: int
    plan_revision: int
    outer_goal_revision: int
    claim_receipt_sha256: str
    preclaim: PlanWorkerPreclaim = field(repr=False, compare=False)
    claim_receipt: Mapping[str, Any] = field(repr=False, compare=False)
    plan_record: Mapping[str, Any] = field(repr=False, compare=False)
    outer_goal_record: Mapping[str, Any] = field(
        repr=False,
        compare=False,
    )

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "plan_id": self.plan_id,
            "task_id": self.task_id,
            "generation": self.generation,
            "plan_revision": self.plan_revision,
            "outer_goal_revision": self.outer_goal_revision,
            "claim_receipt_sha256": self.claim_receipt_sha256,
            "claim_receipt": copy.deepcopy(dict(self.claim_receipt)),
        }


@dataclass(frozen=True)
class PlanTaskContinueInvocation:
    """Token-free exact-task input for one canonical continue call."""

    plan_id: str
    task_id: str
    generation: int
    invocation_sha256: str
    invocation: Mapping[str, Any] = field(repr=False, compare=False)

    def as_dict(self) -> dict[str, Any]:
        return copy.deepcopy(dict(self.invocation))


@dataclass(frozen=True)
class PlanWorkerSummary:
    status: str
    plan_id: str
    task_id: str
    generation: int
    plan_revision: int
    outer_goal_revision: int
    continue_invocations: int | str
    agentjobs: int | str
    receipt_sha256: str
    recovery_required: bool
    coordinator_wakeup_status: str | None = None
    coordinator_wakeup_sha256: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_topology_binding(
    topology: Mapping[str, Any],
    binding: Mapping[str, Any],
) -> None:
    if (
        topology.get("branch") != binding.get("branch")
        or topology.get("worktree") != binding.get("worktree")
        or any(
            topology.get(field) != binding.get(field)
            for field in ("root", "git_common_dir")
            if field in topology
        )
    ):
        raise StateConflict(
            "worker refuses a claim in a mismatched repository topology",
            details={"reason_code": "plan_worker.repository_topology_mismatch"},
        )


def _preclaim_conflict(
    message: str,
    *,
    reason_code: str = "plan_task.identity_mismatch",
) -> StateConflict:
    return StateConflict(message, details={"reason_code": reason_code})


def validate_plan_worker_preclaim(
    store: SQLitePlanStore,
    *,
    envelope: Mapping[str, Any],
    envelope_sha256: str,
    selection_proof_sha256: str,
    selected_task_definition: Mapping[str, Any],
    task_definition_sha256: str,
    dependency_proof: Mapping[str, Any],
    dependency_proof_sha256: str,
    expected_revision: int,
    current_thread_id: str,
    observed_execution_profile: Mapping[str, Any],
    observed_repository_binding: Mapping[str, Any],
    observed_repository_topology: Mapping[str, Any],
) -> PlanWorkerPreclaim:
    """Validate all profile and topology evidence before task claim."""

    value = copy.deepcopy(dict(envelope))
    version = value.get("schema_version")
    schema = store.schema_root / (
        "plan-task-envelope-v2.schema.json"
        if version == "sys4ai.plan-task-envelope.v2"
        else "plan-task-envelope.schema.json"
    )
    issues = validate_instance(value, schema)
    if issues:
        raise RecordValidationError(
            "plan worker envelope failed canonical validation",
            details={
                "reason_code": "plan_task.envelope_invalid",
                "findings": format_issues(issues).splitlines(),
            },
        )
    if content_sha256(value) != envelope_sha256:
        raise _preclaim_conflict("plan worker envelope hash mismatch")
    record = store.load_plan(str(value["plan_id"]))
    if record.get("runtime_profile_version") == 2 and version != (
        "sys4ai.plan-task-envelope.v2"
    ):
        raise _preclaim_conflict(
            "legacy envelope is readable but cannot enter the profile-aware writer",
            reason_code="plan_task.envelope_invalid",
        )
    if version != "sys4ai.plan-task-envelope.v2":
        raise _preclaim_conflict(
            "new plan worker writes require a profile-aware v2 envelope",
            reason_code="plan_task.envelope_invalid",
        )
    if (
        not isinstance(selected_task_definition, Mapping)
        or not isinstance(dependency_proof, Mapping)
        or not isinstance(current_thread_id, str)
        or not current_thread_id.strip()
    ):
        raise _preclaim_conflict(
            "plan worker entry artifacts or current thread are invalid"
        )
    definition = copy.deepcopy(dict(selected_task_definition))
    dependency = copy.deepcopy(dict(dependency_proof))
    state = record["state"]
    if state["revision"] != expected_revision:
        raise StateConflict(
            "plan worker expected revision is stale",
            details={
                "reason_code": "plan.revision_conflict",
                "expected_revision": expected_revision,
                "actual_revision": state["revision"],
            },
        )
    task_id = str(value["task_id"])
    task = next(
        (
            item
            for item in state["tasks"]
            if item["task_id"] == task_id
        ),
        None,
    )
    generation = int(value["generation"])
    lease = state.get("lease")
    intent = store.find_provider_intent(record["plan_id"], generation)
    canonical_definition = store.load_task_definition(
        record["plan_id"],
        task_id,
    )
    canonical_task_json = copy.deepcopy(
        dict(canonical_definition["task_json"])
    )
    proof_revision = dependency.get("plan_revision")
    if (
        isinstance(proof_revision, bool)
        or not isinstance(proof_revision, int)
        or proof_revision < 0
    ):
        raise _preclaim_conflict(
            "plan worker dependency proof revision is invalid",
            reason_code="plan.dependency_invalid",
        )
    persisted_proof = store.selection_proof_for_revision(
        record["plan_id"],
        proof_revision,
    )
    if persisted_proof is None:
        raise _preclaim_conflict(
            "plan worker selection proof is absent",
            reason_code="plan.dependency_invalid",
        )
    expected_dependency = build_plan_task_dependency_proof(
        persisted_proof,
        canonical_definition,
    )
    profile = record["execution_profile"]
    accepted_effort = str(profile["reasoning_effort"])
    observed_effort = observed_execution_profile.get(
        "effective_reasoning_effort",
        observed_execution_profile.get("reasoning_effort"),
    )
    evidence_ref = observed_execution_profile.get("evidence_ref")
    topology_sha256 = content_sha256(
        dict(observed_repository_topology)
    )
    recovery_events = [
        entry
        for entry in record["journal"]
        if entry["kind"] == "event"
        and entry["payload"].get("event_type")
        == "provider_recovery_adopted"
        and entry["payload"].get("generation") == generation
        and entry["payload"].get("task_id") == task_id
        and entry["payload"].get("successor_thread_id_sha256")
        == content_sha256({"thread_id": current_thread_id})
        and entry["payload"].get("observed_topology_sha256")
        == topology_sha256
    ]
    normal_provider_match = (
        isinstance(intent, Mapping)
        and intent["status"] == "returned"
        and intent["returned_thread_id"] == current_thread_id
        and intent["requested_reasoning_effort"] == accepted_effort
        and intent["effective_reasoning_effort"] == accepted_effort
        and intent["profile_verification_status"] == "verified"
        and isinstance(intent["observed_topology_sha256"], str)
        and len(intent["observed_topology_sha256"]) == 64
    )
    recovery_provider_match = (
        isinstance(intent, Mapping)
        and intent["status"] in {"ambiguous", "timeout", "duplicate"}
        and len(recovery_events) == 1
        and recovery_events[0]["payload"].get(
            "effective_reasoning_effort"
        )
        == accepted_effort
        and recovery_events[0]["payload"].get("profile_evidence_ref")
        == evidence_ref
    )
    provider_revision_match = (
        normal_provider_match
        and expected_revision == intent["expected_revision"] + 2
    ) or (
        recovery_provider_match
        and expected_revision == intent["expected_revision"] + 3
    )
    projected_binding = {
        field_name: copy.deepcopy(
            record["repository_binding"].get(field_name)
        )
        for field_name in PLAN_TASK_REPOSITORY_FIELDS
    }
    expected_task_counters = {
        "worker_discussions": 1,
        "continue_invocations": 0,
        "agentjobs": 0,
        "provider_creates": 1,
        "successor_creates": 1,
        "same_task_successors": 0,
    }
    token_sha256 = holder_token_sha256(str(value["handoff_token"]))
    canonical_idempotency_key = f"{record['plan_id']}:{generation}"
    proof_content_sha256 = content_sha256(persisted_proof)
    definition_content_sha256 = content_sha256(canonical_task_json)
    dependency_content_sha256 = content_sha256(expected_dependency)
    exact = (
        state["phase"] == "task_reserved"
        and state["current_generation"] == generation
        and state["active_task_id"] == task_id
        and isinstance(task, Mapping)
        and task["status"] == "reserved"
        and task["generation"] == generation
        and task["task_sha256"] == value["task_sha256"]
        and task["counters"] == expected_task_counters
        and task["receipt_link"] is None
        and task["fingerprint_before"] is None
        and task["fingerprint_after"] is None
        and task["terminal_reason"] is None
        and isinstance(lease, Mapping)
        and lease["holder_kind"] == "successor_reserved"
        and lease["holder_token_hash"] == token_sha256
        and lease["generation"] == generation
        and lease["task_id"] == task_id
        and lease["repository_fingerprint"]
        == state["repository_fingerprint"]
        and value["plan_id"] == record["plan_id"]
        and value["plan_sha256"] == record["effective_plan_sha256"]
        and value["idempotency_key"] == canonical_idempotency_key
        and value["predecessor_thread_id"] != current_thread_id
        and value["repository_binding"] == projected_binding
        and value["activation_receipt_sha256"]
        == record["activation_receipt_sha256"]
        and value["execution_profile"] == profile
        and value["repository_topology_policy"]
        == record["repository_topology_policy"]
        and value["repository_binding_sha256"]
        == record["repository_binding_sha256"]
        and value["activation_sequence"] == record["activation_sequence"]
        and observed_repository_binding == record["repository_binding"]
        and definition == canonical_task_json
        and task_definition_sha256 == definition_content_sha256
        and dependency == expected_dependency
        and dependency_proof_sha256 == dependency_content_sha256
        and selection_proof_sha256 == proof_content_sha256
        and dependency["selection_proof_sha256"]
        == proof_content_sha256
        and dependency["selected_task"]["task_id"] == task_id
        and dependency["selected_task"]["task_sha256"]
        == value["task_sha256"]
        and dependency["dependency_ready"] is True
        and observed_effort == accepted_effort
        and isinstance(evidence_ref, str)
        and bool(evidence_ref.strip())
        and isinstance(intent, Mapping)
        and intent["schema_version"] == "sys4ai.plan-provider-intent.v2"
        and intent["finalized"] is True
        and intent["plan_id"] == record["plan_id"]
        and intent["plan_sha256"] == record["effective_plan_sha256"]
        and intent["task_id"] == task_id
        and intent["task_sha256"] == value["task_sha256"]
        and intent["generation"] == generation
        and intent["idempotency_key"] == canonical_idempotency_key
        and intent["handoff_token_sha256"] == token_sha256
        and intent["predecessor_thread_id"]
        == value["predecessor_thread_id"]
        and intent["expected_revision"] == proof_revision + 1
        and provider_revision_match
        and intent["repository_fingerprint"]
        == state["repository_fingerprint"]
        and intent["provider_create_budget"] == 1
        and intent["create_attempts"] == 1
        and intent["retry_authorized"] is False
        and (normal_provider_match or recovery_provider_match)
        and intent["execution_profile_sha256"] == content_sha256(profile)
        and intent["repository_binding_sha256"]
        == record["repository_binding_sha256"]
        and intent["environment_mode"] == "reuse_bound_checkout"
    )
    if not exact:
        reason_code = (
            "plan_task.thread_mismatch"
            if isinstance(intent, Mapping)
            and (
                (
                    intent.get("status") == "returned"
                    and intent.get("returned_thread_id")
                    != current_thread_id
                )
                or value.get("predecessor_thread_id")
                == current_thread_id
            )
            else "plan_task.identity_mismatch"
        )
        raise _preclaim_conflict(
            "plan worker profile, provider, thread, or canonical identity mismatch",
            reason_code=reason_code,
        )
    _validate_topology_binding(
        observed_repository_topology,
        record["repository_binding"],
    )
    outer = store.goal_store.load_goal(record["outer_goal_id"])
    return PlanWorkerPreclaim(
        plan_id=record["plan_id"],
        task_id=task_id,
        generation=generation,
        plan_revision=state["revision"],
        outer_goal_revision=outer["state"]["revision"],
        current_thread_id=current_thread_id,
        reasoning_effort=accepted_effort,
        provider_id=str(intent["provider_id"]),
        provider_evidence_ref=str(
            intent["profile_evidence_ref"]
            if normal_provider_match
            else evidence_ref
        ),
        pre_task_topology_sha256=topology_sha256,
        predecessor_thread_id=value["predecessor_thread_id"],
        envelope_sha256=envelope_sha256,
        selection_proof_sha256=proof_content_sha256,
        task_definition_sha256=definition_content_sha256,
        dependency_proof_sha256=dependency_content_sha256,
        provider_intent_sha256=content_sha256(intent),
        repository_binding_sha256=record[
            "repository_binding_sha256"
        ],
    )


def _build_claim_receipt(
    *,
    preclaim: PlanWorkerPreclaim,
    record: Mapping[str, Any],
    envelope: Mapping[str, Any],
    lease: Mapping[str, Any],
    worker_token: str,
    fingerprint_before: str,
    timestamp: str,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "schema_version": "sys4ai.plan-task-claim-receipt.v1",
        "plan_id": preclaim.plan_id,
        "plan_sha256": record["effective_plan_sha256"],
        "task_id": preclaim.task_id,
        "task_sha256": envelope["task_sha256"],
        "generation": preclaim.generation,
        "envelope_sha256": preclaim.envelope_sha256,
        "selection_proof_sha256": preclaim.selection_proof_sha256,
        "task_definition_sha256": preclaim.task_definition_sha256,
        "dependency_proof_sha256": preclaim.dependency_proof_sha256,
        "provider_intent_sha256": preclaim.provider_intent_sha256,
        "idempotency_key": envelope["idempotency_key"],
        "predecessor_thread_id": preclaim.predecessor_thread_id,
        "worker_thread_id": preclaim.current_thread_id,
        "plan_revision_before": preclaim.plan_revision,
        "plan_revision_after": preclaim.plan_revision + 1,
        "outer_goal_revision_before": preclaim.outer_goal_revision,
        "outer_goal_revision_after": preclaim.outer_goal_revision + 1,
        "repository_binding_sha256": (
            preclaim.repository_binding_sha256
        ),
        "pre_task_topology_sha256": (
            preclaim.pre_task_topology_sha256
        ),
        "fingerprint_before": fingerprint_before,
        "lease_transaction_id": lease["transaction_id"],
        "worker_token_sha256": holder_token_sha256(worker_token),
        "counts_at_claim": {
            "worker_discussions": 1,
            "continue_invocations": 0,
            "agentjobs": 0,
            "provider_creates": 1,
            "successor_creates": 1,
            "same_task_successors": 0,
        },
        "claimed_at": timestamp,
        "hash_basis": (
            "canonical_json_without_claim_content_sha256"
        ),
        "claim_content_sha256": "",
        "finalized": True,
    }
    receipt["claim_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in receipt.items()
            if key != "claim_content_sha256"
        }
    )
    return receipt


def claim_plan_task_generation(
    store: SQLitePlanStore,
    *,
    envelope: Mapping[str, Any],
    envelope_sha256: str,
    selection_proof_sha256: str,
    selected_task_definition: Mapping[str, Any],
    task_definition_sha256: str,
    dependency_proof: Mapping[str, Any],
    dependency_proof_sha256: str,
    expected_revision: int,
    expected_outer_revision: int,
    current_thread_id: str,
    worker_token: str,
    observed_execution_profile: Mapping[str, Any],
    observed_repository_binding: Mapping[str, Any],
    observed_repository_topology: Mapping[str, Any],
    timestamp: str | None = None,
    expires_at: str | None = None,
) -> PlanTaskClaimResult:
    """Validate and atomically claim one exact unconsumed task generation."""

    if not isinstance(worker_token, str) or len(worker_token) < 32:
        raise RecordValidationError(
            "plan worker token must contain at least 32 characters",
            details={"reason_code": "plan_task.identity_mismatch"},
        )
    now = timestamp or utc_now()
    parse_utc(now)
    preclaim = validate_plan_worker_preclaim(
        store,
        envelope=envelope,
        envelope_sha256=envelope_sha256,
        selection_proof_sha256=selection_proof_sha256,
        selected_task_definition=selected_task_definition,
        task_definition_sha256=task_definition_sha256,
        dependency_proof=dependency_proof,
        dependency_proof_sha256=dependency_proof_sha256,
        expected_revision=expected_revision,
        current_thread_id=current_thread_id,
        observed_execution_profile=observed_execution_profile,
        observed_repository_binding=observed_repository_binding,
        observed_repository_topology=observed_repository_topology,
    )
    if preclaim.outer_goal_revision != expected_outer_revision:
        raise StateConflict(
            "plan worker outer-goal revision is stale",
            details={
                "reason_code": "plan.revision_conflict",
                "expected_revision": expected_outer_revision,
                "actual_revision": preclaim.outer_goal_revision,
            },
        )
    expiry = expires_at or add_seconds(now, 900)
    record = store.load_plan(preclaim.plan_id)
    fingerprint_before = record["state"]["fingerprints"]["current"]
    with store.mutation(
        preclaim.plan_id,
        expected_revision=preclaim.plan_revision,
        timestamp=now,
    ) as mutation:
        mutation.activate_task(
            task_id=preclaim.task_id,
            generation=preclaim.generation,
            fingerprint_before=fingerprint_before,
        )
        lease = mutation.transfer_plan_lease(
            expected_outer_revision=expected_outer_revision,
            current_holder_token=str(envelope["handoff_token"]),
            holder_kind="worker",
            holder_token=worker_token,
            expires_at=expiry,
        )
        claim_receipt = _build_claim_receipt(
            preclaim=preclaim,
            record=record,
            envelope=envelope,
            lease=lease,
            worker_token=worker_token,
            fingerprint_before=fingerprint_before,
            timestamp=now,
        )
        mutation.event(
            "task_generation_claimed",
            {"claim_receipt": claim_receipt},
        )

    claimed = store.load_plan(preclaim.plan_id)
    outer = store.goal_store.load_goal(claimed["outer_goal_id"])
    task = next(
        item
        for item in claimed["state"]["tasks"]
        if item["task_id"] == preclaim.task_id
    )
    persisted_claims = [
        entry["payload"]["claim_receipt"]
        for entry in claimed["journal"]
        if entry["kind"] == "event"
        and entry["payload"].get("event_type")
        == "task_generation_claimed"
        and entry["payload"].get("claim_receipt", {}).get("generation")
        == preclaim.generation
        and entry["payload"].get("claim_receipt", {}).get("task_id")
        == preclaim.task_id
    ]
    expected_counts = claim_receipt["counts_at_claim"]
    state_lease = claimed["state"].get("lease")
    outer_lease = outer["state"].get("active_lease")
    persisted_intent = store.find_provider_intent(
        preclaim.plan_id,
        preclaim.generation,
    )
    if (
        claimed["state"]["revision"] != preclaim.plan_revision + 1
        or outer["state"]["revision"]
        != preclaim.outer_goal_revision + 1
        or claimed["state"]["phase"] != "task_active"
        or claimed["state"]["active_task_id"] != preclaim.task_id
        or task["status"] != "active"
        or task["generation"] != preclaim.generation
        or task["fingerprint_before"] != fingerprint_before
        or task["fingerprint_after"] is not None
        or task["receipt_link"] is not None
        or task["counters"] != expected_counts
        or not isinstance(state_lease, Mapping)
        or state_lease["holder_kind"] != "worker"
        or state_lease["generation"] != preclaim.generation
        or state_lease["task_id"] != preclaim.task_id
        or state_lease["holder_token_hash"]
        != holder_token_sha256(worker_token)
        or state_lease["transaction_id"]
        != claim_receipt["lease_transaction_id"]
        or not isinstance(outer_lease, Mapping)
        or outer_lease["holder_kind"] != "continuation"
        or outer_lease["holder_token"] != worker_token
        or len(persisted_claims) != 1
        or persisted_claims[0] != claim_receipt
        or claim_receipt["claim_content_sha256"]
        != content_sha256(
            {
                key: item
                for key, item in claim_receipt.items()
                if key != "claim_content_sha256"
            }
        )
        or not isinstance(persisted_intent, Mapping)
        or content_sha256(persisted_intent)
        != preclaim.provider_intent_sha256
        or store.integrity_check()["status"] != "pass"
    ):
        raise IntegrityError(
            "plan task claim differs from its canonical atomic receipt"
        )
    return PlanTaskClaimResult(
        status="claimed",
        plan_id=preclaim.plan_id,
        task_id=preclaim.task_id,
        generation=preclaim.generation,
        plan_revision=claimed["state"]["revision"],
        outer_goal_revision=outer["state"]["revision"],
        claim_receipt_sha256=content_sha256(claim_receipt),
        preclaim=preclaim,
        claim_receipt=copy.deepcopy(claim_receipt),
        plan_record=copy.deepcopy(claimed),
        outer_goal_record=copy.deepcopy(outer),
    )


def _authority_packet_invalid(
    message: str,
    *,
    reason_code: str = "plan_task.scope_violation",
) -> StateConflict:
    return StateConflict(message, details={"reason_code": reason_code})


def _validate_authority_record(
    value: Mapping[str, Any],
    *,
    schema_name: str,
) -> None:
    schema = Path(__file__).resolve().parents[3] / "schemas" / schema_name
    issues = validate_instance(value, schema)
    if issues:
        raise RecordValidationError(
            "plan-task authority packet failed canonical validation",
            details={
                "reason_code": "plan_task.authority_packet_invalid",
                "record_schema": schema_name,
                "findings": format_issues(issues).splitlines(),
            },
        )


def _continuous_execution_authority_evidence(
    store: SQLitePlanStore,
    *,
    plan_id: str,
    task_id: str,
    director_route: DirectorRoute,
) -> dict[str, Any]:
    """Bind a continuous worker route to exact, currently granted effects."""

    record = store.load_plan(plan_id)
    authority = store.load_execution_authority(plan_id)
    if (
        authority["plan_id"] != plan_id
        or authority["accepted_plan_sha256"]
        != record["effective_plan_sha256"]
    ):
        raise StateConflict(
            "continuous execution authority no longer matches the accepted plan",
            details={"reason_code": "plan.acceptance_invalidated"},
        )

    requested_by_id = {
        str(item["effect_id"]): copy.deepcopy(dict(item))
        for item in authority["requested_effects"]
    }
    responses = store.load_question_responses(plan_id)
    latest_grants: dict[str, bool] = {}
    for response in responses:
        for grant in response["grants"]:
            effect_id = str(grant["effect_id"])
            if effect_id not in requested_by_id:
                raise IntegrityError(
                    "a persisted response refers to an unknown protected effect",
                    details={
                        "reason_code": "plan.protected_effect_unknown",
                        "effect_id": effect_id,
                    },
                )
            latest_grants[effect_id] = grant["granted"] is True
    granted_effect_ids = {
        effect_id
        for effect_id, granted in latest_grants.items()
        if granted
    }

    task_effects = {
        effect_id: item
        for effect_id, item in requested_by_id.items()
        if not item["affected_task_ids"]
        or task_id in item["affected_task_ids"]
    }
    authority_block = director_route.job_spec.get("authority")
    if not isinstance(authority_block, Mapping):
        raise StateConflict(
            "continuous worker route lacks a declared authority block",
            details={"reason_code": "plan.protected_effect_unapproved"},
        )
    route_effects = authority_block.get("external_effects")
    route_refs = director_route.job_spec.get(
        "external_effect_authority_refs", []
    )
    if (
        not isinstance(route_effects, list)
        or any(
            not isinstance(item, str) or not item.strip()
            for item in route_effects
        )
        or len(route_effects) != len(set(route_effects))
        or not isinstance(route_refs, list)
        or any(
            not isinstance(item, str) or not item.strip()
            for item in route_refs
        )
        or len(route_refs) != len(set(route_refs))
    ):
        raise StateConflict(
            "continuous worker route has malformed protected-effect bindings",
            details={"reason_code": "plan.protected_effect_unapproved"},
        )

    matched_effect_ids: list[str] = []
    for description in route_effects:
        matches = [
            effect_id
            for effect_id, item in task_effects.items()
            if item["description"] == description
        ]
        if len(matches) != 1:
            raise StateConflict(
                "continuous worker route does not name one exact accepted effect",
                details={
                    "reason_code": "plan.protected_effect_unapproved",
                    "effect": description,
                    "matching_effect_ids": sorted(matches),
                },
            )
        matched_effect_ids.append(matches[0])

    if set(route_refs) != set(matched_effect_ids):
        raise StateConflict(
            "continuous worker route authority references do not match its effects",
            details={
                "reason_code": "plan.protected_effect_unapproved",
                "expected_effect_ids": sorted(matched_effect_ids),
                "observed_effect_ids": sorted(route_refs),
            },
        )
    ungranted = sorted(set(matched_effect_ids) - granted_effect_ids)
    if ungranted:
        raise StateConflict(
            "continuous worker route requests a protected effect without its grant",
            details={
                "reason_code": "plan.protected_effect_unapproved",
                "ungranted_effect_ids": ungranted,
            },
        )

    return {
        "authority_record_sha256": content_sha256(authority),
        "authority_content_sha256": authority["authority_content_sha256"],
        "response_record_sha256s": [
            content_sha256(response) for response in responses
        ],
        "granted_effect_ids": sorted(granted_effect_ids),
        "task_effect_ids": sorted(task_effects),
        "route_effect_ids": sorted(matched_effect_ids),
    }


def compile_plan_task_continue_invocation(
    *,
    preclaim: PlanWorkerPreclaim,
    plan_record: Mapping[str, Any],
    envelope: Mapping[str, Any],
    selected_task_definition: Mapping[str, Any],
    resolved_task_id: str,
    director_route: DirectorRoute,
    timestamp: str,
    continuous_authority_evidence: Mapping[str, Any] | None = None,
) -> PlanTaskContinueInvocation:
    """Compile one exact-task, token-free continuation authority packet."""

    parse_utc(timestamp)
    record = copy.deepcopy(dict(plan_record))
    value = copy.deepcopy(dict(envelope))
    if not isinstance(selected_task_definition, Mapping):
        raise RecordValidationError(
            "plan-task compiler requires one canonical task definition",
            details={"reason_code": "plan_task.authority_packet_invalid"},
        )
    definition = copy.deepcopy(dict(selected_task_definition))
    task = copy.deepcopy(definition)
    state = record.get("state")
    if (
        not isinstance(resolved_task_id, str)
        or not resolved_task_id.strip()
        or not isinstance(state, Mapping)
        or record.get("plan_id") != preclaim.plan_id
        or record.get("effective_plan_sha256") != value.get("plan_sha256")
        or state.get("phase") != "task_active"
        or state.get("active_task_id") != preclaim.task_id
        or resolved_task_id != preclaim.task_id
        or value.get("task_id") != preclaim.task_id
        or definition.get("task_id") != preclaim.task_id
        or definition.get("task_sha256") != value.get("task_sha256")
        or int(value.get("generation", -1)) != preclaim.generation
    ):
        raise _authority_packet_invalid(
            "plan-task compiler refuses resolver substitution or identity drift"
        )
    budget = task.get("execution_budget")
    if (
        not isinstance(budget, Mapping)
        or budget
        != {
            "one_task_per_discussion": True,
            "max_continue_invocations": 1,
            "max_agentjobs": 1,
            "same_task_successors": 0,
        }
        or value.get("one_task_per_discussion") is not True
        or value.get("max_continue_invocations") != 1
        or value.get("max_agentjobs") != 1
    ):
        raise _authority_packet_invalid(
            "plan-task compiler requires the frozen one-task execution budget"
        )
    if not isinstance(director_route, DirectorRoute):
        raise RecordValidationError(
            "plan-task compiler requires one declared DirectorRoute",
            details={"reason_code": "plan_task.authority_packet_invalid"},
        )
    if not isinstance(
        director_route.job_spec, Mapping
    ) or not isinstance(director_route.role_spec, Mapping):
        raise RecordValidationError(
            "plan-task Director route requires mapping job and role specs",
            details={"reason_code": "plan_task.authority_packet_invalid"},
        )
    legal, route_reason = _route_legality(director_route)
    if not legal:
        reason_code = (
            "plan.human_gate_required"
            if director_route.requires_human_gate
            else "plan_task.scope_violation"
        )
        raise _authority_packet_invalid(
            f"plan-task Director route is not executable: {route_reason}",
            reason_code=reason_code,
        )
    if director_route.human_gate_refs:
        raise _authority_packet_invalid(
            "plan-task executable route retains unresolved human-gate references",
            reason_code="plan.human_gate_required",
        )
    job_spec = copy.deepcopy(dict(director_route.job_spec))
    role_spec = copy.deepcopy(dict(director_route.role_spec))
    required_job_fields = {
        "objective",
        "authority",
        "source_policy",
        "commands",
        "validators",
        "expected_outputs",
        "completion_contract",
        "stop_conditions",
        "checkpoint",
        "claim_boundary",
    }
    required_role_fields = {"responsibilities", "may_not"}
    if (
        required_job_fields - set(job_spec)
        or required_role_fields - set(role_spec)
    ):
        raise RecordValidationError(
            "plan-task Director route lacks required AgentJob or role fields",
            details={"reason_code": "plan_task.authority_packet_invalid"},
        )
    acceptance = list(task.get("acceptance_criteria", []))
    validation_refs = list(task.get("validation_refs", []))
    required_validators = list(
        job_spec.get("validators", {}).get("required", [])
    )
    if (
        not acceptance
        or not validation_refs
        or job_spec.get("objective") != task.get("objective")
        or job_spec.get("claim_boundary", {}).get("allowed") != acceptance
        or job_spec.get("completion_contract", {}).get(
            "required_evidence"
        )
        != acceptance
        or len(required_validators) != len(validation_refs)
    ):
        raise _authority_packet_invalid(
            "plan-task route objective, claims, evidence, or validators "
            "differ from the canonical task"
        )
    overlay = role_spec.get("task_overlay")
    if isinstance(overlay, Mapping) and overlay.get(
        "expanded_permissions"
    ):
        raise _authority_packet_invalid(
            "plan-task execution-role overlay may not expand authority"
        )
    binding_basis = {
        "plan_id": preclaim.plan_id,
        "plan_sha256": record["effective_plan_sha256"],
        "task_id": preclaim.task_id,
        "task_sha256": value["task_sha256"],
        "generation": preclaim.generation,
        "envelope_sha256": preclaim.envelope_sha256,
        "task_definition_sha256": preclaim.task_definition_sha256,
        "dependency_proof_sha256": preclaim.dependency_proof_sha256,
        "resolver_task_id": resolved_task_id,
        "director_route": {
            "route_id": director_route.route_id,
            "role_id": director_route.role_id,
            "role_version": director_route.role_version,
            "priority": director_route.priority,
            "rationale": director_route.rationale,
            "job_spec": job_spec,
            "role_spec": role_spec,
            "forced_by_rule_id": director_route.forced_by_rule_id,
            "requires_human_gate": director_route.requires_human_gate,
            "human_gate_refs": list(director_route.human_gate_refs),
            "authority_expansion": director_route.authority_expansion,
            "domain_truth_decision": (
                director_route.domain_truth_decision
            ),
            "domain_authority_ref": (
                director_route.domain_authority_ref
            ),
        },
    }
    if continuous_authority_evidence is not None:
        binding_basis["continuous_authority_evidence"] = copy.deepcopy(
            dict(continuous_authority_evidence)
        )
    if contains_secret(
        canonical_json_bytes(binding_basis).decode("utf-8")
    ):
        raise RecordValidationError(
            "plan-task authority packet appears to contain a secret",
            details={"reason_code": "security.secret_detected"},
        )
    binding_sha256 = content_sha256(binding_basis)
    suffix = binding_sha256[:16]
    decision_id = f"DDR-{preclaim.task_id}-{suffix}"
    job_id = f"AJ-{preclaim.task_id}-{suffix}"
    execution_role_id = f"ER-{preclaim.task_id}-{suffix}"
    role_ref = (
        f"roles/{preclaim.task_id}/{execution_role_id}.json"
    )
    policy_refs = list(
        job_spec.get(
            "policy_refs",
            [".agents/control/policies/default.json"],
        )
    )
    actor_ref = str(
        job_spec.get(
            "actor_ref",
            "continue-implementing-plan-task:compiler",
        )
    )
    decision = {
        "schema_version": "sys4ai.director-decision.v1",
        "decision_id": decision_id,
        "task_id": preclaim.task_id,
        "decision_authority": {
            "kind": "system_director",
            "actor_ref": actor_ref,
            "policy_refs": policy_refs,
        },
        "decision_type": "create_job",
        "decision_mode": "deterministic",
        "status": "activated",
        "evidence": {
            "state_snapshot_ref": (
                f"evidence/plan-task-claims/{binding_sha256}.json"
            ),
            "state_snapshot_sha256": binding_sha256,
            "handoff_refs": [],
            "source_refs": validation_refs,
        },
        "candidates": [
            {
                "route_id": director_route.route_id,
                "role_id": director_route.role_id,
                "assessment": "accepted",
                "reason": director_route.rationale,
            }
        ],
        "selected": {
            "route_id": director_route.route_id,
            "role_id": director_route.role_id,
            "role_version": director_route.role_version,
            "agent_job_id": job_id,
            "rationale": director_route.rationale,
        },
        "rejected_alternatives": [],
        "requires_human_gate": False,
        "human_gate_refs": [],
        "claim_boundary": copy.deepcopy(job_spec["claim_boundary"]),
        "supersedes_decision_id": None,
        "rule_id": (
            director_route.forced_by_rule_id
            or f"plan-task-exact:{preclaim.task_id}"
        ),
        "rejected_illegal_routes": [
            "Resolver substitution and additional routes are forbidden."
        ],
        "created_at": timestamp,
        "activated_at": timestamp,
        "completed_at": None,
        "extensions": {},
    }
    job = {
        "schema_version": "sys4ai.agent-job.v1",
        "job_id": job_id,
        "task_id": preclaim.task_id,
        "decision_id": decision_id,
        "status": "active",
        "activated_at": timestamp,
        "objective": task["objective"],
        "role_binding": {
            "role_id": director_route.role_id,
            "role_version": director_route.role_version,
            "execution_role_ref": role_ref,
        },
        "authority": copy.deepcopy(job_spec["authority"]),
        "source_policy": copy.deepcopy(job_spec["source_policy"]),
        "commands": copy.deepcopy(job_spec["commands"]),
        "validators": copy.deepcopy(job_spec["validators"]),
        "expected_outputs": copy.deepcopy(
            job_spec["expected_outputs"]
        ),
        "completion_contract": copy.deepcopy(
            job_spec["completion_contract"]
        ),
        "stop_conditions": copy.deepcopy(
            job_spec["stop_conditions"]
        ),
        "checkpoint": copy.deepcopy(job_spec["checkpoint"]),
        "claim_boundary": copy.deepcopy(job_spec["claim_boundary"]),
        "concurrency": {
            "policy": "exclusive_task",
            "lease_scope": (
                f"{preclaim.plan_id}:{preclaim.task_id}:"
                f"{preclaim.generation}"
            ),
            "idempotency_key": value["idempotency_key"],
        },
        "extensions": copy.deepcopy(job_spec.get("extensions", {})),
    }
    role = {
        "schema_version": "sys4ai.execution-role.v1",
        "execution_role_id": execution_role_id,
        "job_id": job_id,
        "task_id": preclaim.task_id,
        "binding_type": role_spec.get(
            "binding_type",
            "registered_role",
        ),
        "role_id": director_route.role_id,
        "role_version": director_route.role_version,
        "responsibilities": copy.deepcopy(
            role_spec["responsibilities"]
        ),
        "may_not": copy.deepcopy(role_spec["may_not"]),
        "source_role_ref": role_spec.get("source_role_ref"),
        "task_overlay": copy.deepcopy(role_spec.get("task_overlay")),
        "authority_delta": str(
            role_spec.get(
                "authority_delta",
                "No permission expansion.",
            )
        ),
        "provisional_role": copy.deepcopy(
            role_spec.get("provisional_role")
        ),
        "requires_human_gate": False,
        "human_gate_refs": [],
        "expires_after": job_id,
        "activated_at": timestamp,
        "extensions": copy.deepcopy(role_spec.get("extensions", {})),
    }
    _validate_authority_record(
        decision,
        schema_name="director-decision.schema.json",
    )
    _validate_authority_record(
        job,
        schema_name="agent-job.schema.json",
    )
    _validate_authority_record(
        role,
        schema_name="execution-role.schema.json",
    )
    invocation: dict[str, Any] = {
        "schema_version": "sys4ai.plan-task-continue-invocation.v1",
        "mode": "normal",
        "project_root": record["repository_binding"]["root"],
        "task_id": preclaim.task_id,
        "plan_binding": {
            "plan_id": preclaim.plan_id,
            "plan_sha256": record["effective_plan_sha256"],
            "generation": preclaim.generation,
            "envelope_sha256": preclaim.envelope_sha256,
            "task_definition_sha256": (
                preclaim.task_definition_sha256
            ),
            "dependency_proof_sha256": (
                preclaim.dependency_proof_sha256
            ),
        },
        "task_binding": {
            "task_id": preclaim.task_id,
            "task_sha256": value["task_sha256"],
            "phase_id": task["phase_id"],
            "objective": task["objective"],
            "acceptance_criteria": acceptance,
            "validation_refs": validation_refs,
        },
        "resolver_binding": {
            "requested_task_id": preclaim.task_id,
            "observed_task_id": resolved_task_id,
            "substitution_allowed": False,
        },
        "authority_packet": {
            "decision": decision,
            "agent_job": job,
            "execution_role": role,
        },
        "execution_mapping": {
            "allowed_read_paths": copy.deepcopy(
                job["authority"]["allowed_read_paths"]
            ),
            "allowed_write_paths": copy.deepcopy(
                job["authority"]["allowed_write_paths"]
            ),
            "allowed_generated_paths": copy.deepcopy(
                job["authority"]["allowed_generated_paths"]
            ),
            "forbidden_paths": copy.deepcopy(
                job["authority"]["forbidden_paths"]
            ),
            "allowed_actions": copy.deepcopy(
                job["authority"]["allowed_actions"]
            ),
            "forbidden_actions": copy.deepcopy(
                job["authority"]["forbidden_actions"]
            ),
            "approved_command_ids": [
                command["command_id"]
                for command in job["commands"]["approved"]
            ],
            "tool_policy": {
                "allowed_actions": copy.deepcopy(
                    job["authority"]["allowed_actions"]
                ),
                "forbidden_actions": copy.deepcopy(
                    job["authority"]["forbidden_actions"]
                ),
                "approved_commands": copy.deepcopy(
                    job["commands"]["approved"]
                ),
            },
            "network_access": job["authority"]["network_access"],
            "external_effects": copy.deepcopy(
                job["authority"]["external_effects"]
            ),
            "external_effect_authority_refs": copy.deepcopy(
                job_spec.get("external_effect_authority_refs", [])
            ),
            "validators": [
                {
                    "validation_ref": validation_ref,
                    "validator_id": validator["validator_id"],
                }
                for validation_ref, validator in zip(
                    validation_refs,
                    required_validators,
                    strict=True,
                )
            ],
            "checkpoint": copy.deepcopy(job["checkpoint"]),
            "human_gates": {
                "required": False,
                "refs": [],
            },
        },
        "cardinality": {
            "worker_discussions": 1,
            "max_continue_invocations": 1,
            "max_agentjobs": 1,
            "same_task_successors": 0,
            "candidate_routes": 1,
        },
        "invocation_content_sha256": "",
    }
    if continuous_authority_evidence is not None:
        invocation["execution_mapping"][
            "continuous_authority_evidence"
        ] = copy.deepcopy(dict(continuous_authority_evidence))
    invocation["invocation_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in invocation.items()
            if key != "invocation_content_sha256"
        }
    )
    if contains_secret(
        canonical_json_bytes(invocation).decode("utf-8")
    ):
        raise RecordValidationError(
            "compiled plan-task invocation appears to contain a secret",
            details={"reason_code": "security.secret_detected"},
        )
    return PlanTaskContinueInvocation(
        preclaim.plan_id,
        preclaim.task_id,
        preclaim.generation,
        content_sha256(invocation),
        copy.deepcopy(invocation),
    )


def _default_direct_evidence(
    *,
    status: str,
    evidence_ref: str,
) -> dict[str, Any]:
    return {
        "changed_paths": [],
        "acceptance_results": [
            {
                "criterion": "The bounded plan task outcome is directly evidenced.",
                "status": status,
                "evidence_refs": [evidence_ref],
            }
        ],
        "validator_results": [],
        "checkpoint": {
            "provider": "none",
            "status": "not_required",
            "revision": None,
            "evidence_ref": None,
        },
        "approvals": [],
        "protected_effects": [],
        "warnings": [],
        "indeterminate_checks": (
            [] if status == "pass" else ["continue outcome is unknown"]
        ),
        "plan_completion": None,
    }


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _validate_plan_continue_result(
    result: Mapping[str, Any],
    *,
    repository_binding: Mapping[str, Any],
) -> list[str]:
    """Return stable structural findings for one consumed continue result."""

    required = {
        "starting_revision",
        "ending_revision",
        "fingerprint_after",
        "agentjobs",
        "direct_evidence",
        "reason_code",
        "pre_topology",
        "post_topology",
    }
    findings = [
        f"result.missing:{field_name}"
        for field_name in sorted(required - set(result))
    ]
    for field_name in ("starting_revision", "ending_revision", "reason_code"):
        value = result.get(field_name)
        if not isinstance(value, str) or not value.strip():
            findings.append(f"result.invalid_nonempty_string:{field_name}")
    if not _is_sha256(result.get("fingerprint_after")):
        findings.append("result.invalid_sha256:fingerprint_after")
    agentjobs = result.get("agentjobs")
    if type(agentjobs) is not int or agentjobs not in {0, 1}:
        findings.append("result.invalid_cardinality:agentjobs")
    elif agentjobs == 0:
        reason = result.get("zero_job_reason")
        if not isinstance(reason, str) or not reason.strip():
            findings.append("result.missing_zero_job_reason")
    else:
        job_id = result.get("agent_job_id")
        if not isinstance(job_id, str) or not job_id.strip():
            findings.append("result.missing_agent_job_id")
    if not isinstance(result.get("direct_evidence"), Mapping):
        findings.append("result.invalid_mapping:direct_evidence")
    pre_topology = result.get("pre_topology")
    post_topology = result.get("post_topology")
    if not isinstance(pre_topology, Mapping):
        findings.append("result.invalid_mapping:pre_topology")
    if not isinstance(post_topology, Mapping):
        findings.append("result.invalid_mapping:post_topology")
    if isinstance(pre_topology, Mapping) and isinstance(
        post_topology,
        Mapping,
    ):
        try:
            assert_topology_transition(pre_topology, post_topology)
            _validate_topology_binding(
                post_topology,
                repository_binding,
            )
        except AgentJobControlError:
            findings.append("result.invalid_repository_topology")
    finished_at = result.get("finished_at")
    if finished_at is not None:
        try:
            parse_utc(str(finished_at))
        except (TypeError, ValueError):
            findings.append("result.invalid_timestamp:finished_at")
    try:
        serialized = canonical_json_bytes(result).decode("utf-8")
    except (TypeError, ValueError):
        findings.append("result.not_canonical_json")
    else:
        if contains_secret(serialized):
            findings.append("result.secret_detected")
    return sorted(set(findings))


def _unknown_continue_diagnostic(
    *,
    reason_code: str,
    failure_stage: str,
    exception_type: str | None = None,
    findings: list[str] | None = None,
) -> dict[str, Any]:
    diagnostic: dict[str, Any] = {
        "schema_version": "sys4ai.plan-task-invocation-unknown.v1",
        "reason_code": reason_code,
        "failure_stage": failure_stage,
        "continue_invocations": 1,
        "agentjobs": "unknown",
        "retry_authorized": False,
        "raw_result_persisted": False,
        "findings": sorted(set(findings or [])),
    }
    if exception_type is not None:
        diagnostic["exception_type"] = exception_type
    return diagnostic


def _unknown_continue_result(
    *,
    record: Mapping[str, Any],
    fingerprint_before: str,
    observed_repository_topology: Mapping[str, Any],
    diagnostic: Mapping[str, Any],
) -> dict[str, Any]:
    diagnostic_sha256 = content_sha256(diagnostic)
    return {
        "starting_revision": record["repository_binding"][
            "starting_revision"
        ],
        "ending_revision": record["repository_binding"][
            "starting_revision"
        ],
        "fingerprint_after": fingerprint_before,
        "agentjobs": "unknown",
        "agent_job_id": None,
        "zero_job_reason": "The consumed continue outcome is unknown.",
        "direct_evidence": _default_direct_evidence(
            status="indeterminate",
            evidence_ref=(
                "journal:task_invocation_unknown:"
                + diagnostic_sha256
            ),
        ),
        "disposition": "invocation_unknown",
        "reason_code": str(diagnostic["reason_code"]),
        "terminal_reason": "The consumed continue outcome is unknown.",
        "recovery": {"status": "required", "action_ref": None},
        "replanning": {
            "status": "not_required",
            "action_ref": None,
        },
        "coordinator_action": {
            "kind": "await_recovery",
            "next_task_id": None,
        },
        "pre_topology": copy.deepcopy(
            dict(observed_repository_topology)
        ),
        "post_topology": copy.deepcopy(
            dict(observed_repository_topology)
        ),
    }


def _build_receipt(
    *,
    record: Mapping[str, Any],
    task_definition: Mapping[str, Any],
    envelope: Mapping[str, Any],
    intent: Mapping[str, Any],
    preclaim: PlanWorkerPreclaim,
    prior_journal_sha256: str,
    fingerprint_before: str,
    result: Mapping[str, Any],
    started_at: str,
    finished_at: str,
) -> dict[str, Any]:
    post_topology = copy.deepcopy(dict(result["post_topology"]))
    assert_topology_transition(
        copy.deepcopy(dict(result["pre_topology"])),
        post_topology,
    )
    post_topology_sha256 = content_sha256(post_topology)
    agentjobs = result["agentjobs"]
    execution_outcome = (
        "unknown"
        if agentjobs == "unknown"
        else "one_job"
        if agentjobs == 1
        else "zero_job"
    )
    disposition = str(result.get("disposition", "task_complete"))
    receipt_id = (
        "PTR-"
        + content_sha256(
            {
                "plan_id": record["plan_id"],
                "task_id": preclaim.task_id,
                "generation": preclaim.generation,
                "thread_id": preclaim.current_thread_id,
            }
        )[:32]
    )
    receipt: dict[str, Any] = {
        "schema_version": "sys4ai.plan-task-receipt.v2",
        "receipt_id": receipt_id,
        "plan_identity": {
            "plan_id": record["plan_id"],
            "plan_sha256": record["effective_plan_sha256"],
            "phase_id": task_definition["phase_id"],
        },
        "task_identity": {
            "task_id": preclaim.task_id,
            "task_sha256": envelope["task_sha256"],
        },
        "relay_identity": {
            "generation": preclaim.generation,
            "predecessor_thread_id": envelope["predecessor_thread_id"],
            "worker_thread_id": preclaim.current_thread_id,
            "envelope_sha256": content_sha256(envelope),
            "idempotency_key": envelope["idempotency_key"],
            "handoff_token_sha256": holder_token_sha256(
                str(envelope["handoff_token"])
            ),
        },
        "activation_profile_evidence": {
            "activation_receipt_sha256": record[
                "activation_receipt_sha256"
            ],
            "execution_profile_sha256": content_sha256(
                record["execution_profile"]
            ),
            "requested_reasoning_effort": preclaim.reasoning_effort,
            "observed_effective_reasoning_effort": preclaim.reasoning_effort,
            "provider_id": preclaim.provider_id,
            "thread_id": preclaim.current_thread_id,
            "provider_evidence_ref": preclaim.provider_evidence_ref,
            "profile_checked_before_claim": True,
            "canonical_profile_match": True,
        },
        "topology_evidence": {
            "environment_mode": "reuse_bound_checkout",
            "repository_binding_sha256": record[
                "repository_binding_sha256"
            ],
            "repository_topology_policy_sha256": content_sha256(
                record["repository_topology_policy"]
            ),
            "pre_task_topology_sha256": preclaim.pre_task_topology_sha256,
            "post_task_topology_sha256": post_topology_sha256,
            "topology_checked_before_claim": True,
            "unapproved_change_detected": False,
            "authorization_ref": None,
        },
        "started_at": started_at,
        "finished_at": finished_at,
        "repository_evidence": {
            "starting_revision": result["starting_revision"],
            "ending_revision": result["ending_revision"],
            "fingerprint_before": fingerprint_before,
            "fingerprint_after": result["fingerprint_after"],
        },
        "execution": {
            "outcome": execution_outcome,
            "worker_discussions": 1,
            "continue_invocations": (
                "unknown" if execution_outcome == "unknown" else 1
            ),
            "agentjobs": agentjobs,
            "agent_job_id": result.get("agent_job_id"),
            "provider_create_calls": 1,
            "successor_creates": 1,
            "same_task_successors": 0,
            "zero_job_reason": result.get("zero_job_reason"),
        },
        "direct_evidence": copy.deepcopy(dict(result["direct_evidence"])),
        "disposition": disposition,
        "reason_code": str(result["reason_code"]),
        "terminal_reason": result.get("terminal_reason"),
        "recovery": copy.deepcopy(
            dict(
                result.get(
                    "recovery",
                    {"status": "not_required", "action_ref": None},
                )
            )
        ),
        "replanning": copy.deepcopy(
            dict(
                result.get(
                    "replanning",
                    {"status": "not_required", "action_ref": None},
                )
            )
        ),
        "coordinator_action": copy.deepcopy(
            dict(
                result.get(
                    "coordinator_action",
                    {
                        "kind": (
                            "await_recovery"
                            if disposition == "invocation_unknown"
                            else "dispatch_next_task"
                        ),
                        "next_task_id": None,
                    },
                )
            )
        ),
        "journal": {
            "prior_hash": prior_journal_sha256,
            "entry_hash": content_sha256(
                {
                    "prior_hash": prior_journal_sha256,
                    "receipt_id": receipt_id,
                }
            ),
        },
        "hash_basis": "canonical_json_without_receipt_content_sha256",
        "receipt_content_sha256": "",
        "finalized": True,
        "extensions": {},
    }
    receipt["receipt_content_sha256"] = content_sha256(
        {
            key: value
            for key, value in receipt.items()
            if key != "receipt_content_sha256"
        }
    )
    return receipt


def run_plan_task_worker(
    store: SQLitePlanStore,
    *,
    envelope: Mapping[str, Any],
    envelope_sha256: str,
    selection_proof_sha256: str,
    selected_task_definition: Mapping[str, Any],
    task_definition_sha256: str,
    dependency_proof: Mapping[str, Any],
    dependency_proof_sha256: str,
    expected_revision: int,
    expected_outer_revision: int,
    current_thread_id: str,
    worker_token: str,
    observed_execution_profile: Mapping[str, Any],
    observed_repository_binding: Mapping[str, Any],
    observed_repository_topology: Mapping[str, Any],
    resolved_task_id: str,
    director_route: DirectorRoute,
    continue_invoker: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    direct_observation_provider: Callable[
        [Mapping[str, Any]], Mapping[str, Any]
    ],
    timestamp: str | None = None,
    expires_at: str | None = None,
    quarantine_token: str | None = None,
    coordinator_provider: Any | None = None,
    coordinator_thread_id: str | None = None,
) -> PlanWorkerSummary:
    """Claim, consume, invoke, verify, and finalize exactly one plan task."""

    now = timestamp or utc_now()
    parse_utc(now)
    if (coordinator_provider is None) != (coordinator_thread_id is None):
        raise RecordValidationError(
            "coordinator provider and thread identity must be supplied together"
        )
    continuous_authority_evidence: dict[str, Any] | None = None
    if coordinator_provider is not None:
        capabilities = coordinator_provider.capabilities()
        if (
            not isinstance(capabilities, Mapping)
            or capabilities.get("automatic") is not True
            or capabilities.get("can_resume_thread") is not True
        ):
            raise RecordValidationError(
                "continuous worker requires an automatic coordinator-resume capability"
            )
        continuous_state = store.load_continuous_state(str(envelope["plan_id"]))
        if continuous_state["coordinator_thread_id"] != coordinator_thread_id:
            raise StateConflict(
                "worker coordinator identity differs from canonical continuous state"
            )
        continuous_authority_evidence = (
            _continuous_execution_authority_evidence(
                store,
                plan_id=str(envelope["plan_id"]),
                task_id=str(envelope["task_id"]),
                director_route=director_route,
            )
        )
    expiry = expires_at or add_seconds(now, 900)
    claim = claim_plan_task_generation(
        store,
        envelope=envelope,
        envelope_sha256=envelope_sha256,
        selection_proof_sha256=selection_proof_sha256,
        selected_task_definition=selected_task_definition,
        task_definition_sha256=task_definition_sha256,
        dependency_proof=dependency_proof,
        dependency_proof_sha256=dependency_proof_sha256,
        expected_revision=expected_revision,
        expected_outer_revision=expected_outer_revision,
        current_thread_id=current_thread_id,
        worker_token=worker_token,
        observed_execution_profile=observed_execution_profile,
        observed_repository_binding=observed_repository_binding,
        observed_repository_topology=observed_repository_topology,
        timestamp=now,
        expires_at=expiry,
    )
    preclaim = claim.preclaim
    record = claim.plan_record
    claimed = claim.plan_record
    fingerprint_before = str(
        claim.claim_receipt["fingerprint_before"]
    )
    compiled_invocation = compile_plan_task_continue_invocation(
        preclaim=preclaim,
        plan_record=claimed,
        envelope=envelope,
        selected_task_definition=selected_task_definition,
        resolved_task_id=resolved_task_id,
        director_route=director_route,
        timestamp=now,
        continuous_authority_evidence=continuous_authority_evidence,
    )
    with store.mutation(
        preclaim.plan_id,
        expected_revision=claimed["state"]["revision"],
        timestamp=now,
    ) as mutation:
        mutation.consume_task_invocation(
            task_id=preclaim.task_id,
            generation=preclaim.generation,
        )
    consumed = store.load_plan(preclaim.plan_id)
    unknown_diagnostic: dict[str, Any] | None = None
    verification = None
    try:
        raw_result = continue_invoker(compiled_invocation.as_dict())
    except Exception as error:
        unknown_diagnostic = _unknown_continue_diagnostic(
            reason_code="plan_worker.continue_outcome_unknown",
            failure_stage="continue_call",
            exception_type=type(error).__name__,
        )
    else:
        if not isinstance(raw_result, Mapping):
            findings = ["result.invalid_mapping"]
            result = {}
        else:
            try:
                result = copy.deepcopy(dict(raw_result))
                findings = _validate_plan_continue_result(
                    result,
                    repository_binding=record["repository_binding"],
                )
            except Exception as error:
                findings = ["result.validation_failed_closed"]
                result = {}
                unknown_diagnostic = _unknown_continue_diagnostic(
                    reason_code="plan_worker.continue_result_invalid",
                    failure_stage="continue_result_validation",
                    exception_type=type(error).__name__,
                    findings=findings,
                )
        if findings and unknown_diagnostic is None:
            unknown_diagnostic = _unknown_continue_diagnostic(
                reason_code="plan_worker.continue_result_invalid",
                failure_stage="continue_result_validation",
                findings=findings,
            )
    unknown = unknown_diagnostic is not None
    if unknown:
        result = _unknown_continue_result(
            record=record,
            fingerprint_before=fingerprint_before,
            observed_repository_topology=observed_repository_topology,
            diagnostic=unknown_diagnostic,
        )
        with store.mutation(
            preclaim.plan_id,
            expected_revision=consumed["state"]["revision"],
            timestamp=now,
        ) as mutation:
            mutation.event(
                "task_invocation_unknown",
                {
                    "task_id": preclaim.task_id,
                    "generation": preclaim.generation,
                    "diagnostic": unknown_diagnostic,
                },
            )
        verifying = store.load_plan(preclaim.plan_id)
    if not unknown:
        observation_findings: list[str] = []
        try:
            direct_observation = direct_observation_provider(result)
        except Exception as error:
            direct_observation = {}
            observation_findings.append(
                "observation.provider_error:"
                + type(error).__name__
            )
        verification = verify_plan_task_result(
            plan_record=record,
            task_definition=selected_task_definition,
            compiled_invocation=compiled_invocation.as_dict(),
            result=result,
            fingerprint_before=fingerprint_before,
            observed_repository_topology_before=(
                observed_repository_topology
            ),
            direct_observation=direct_observation,
            observation_findings=observation_findings,
        )
        result = copy.deepcopy(dict(verification.result))
        with store.mutation(
            preclaim.plan_id,
            expected_revision=consumed["state"]["revision"],
            timestamp=now,
        ) as mutation:
            mutation.begin_task_verification(
                task_id=preclaim.task_id,
                generation=preclaim.generation,
                fingerprint_after=str(result["fingerprint_after"]),
                continue_invocations=1,
                agentjobs=int(result["agentjobs"]),
                provider_creates=1,
            )
        verifying = store.load_plan(preclaim.plan_id)
    intent = store.find_provider_intent(
        preclaim.plan_id,
        preclaim.generation,
    )
    receipt = _build_receipt(
        record=verifying,
        task_definition=store.load_task_definition(
            preclaim.plan_id,
            preclaim.task_id,
        ),
        envelope=envelope,
        intent=intent,
        preclaim=preclaim,
        prior_journal_sha256=verifying["journal"][-1]["event_hash"],
        fingerprint_before=fingerprint_before,
        result=result,
        started_at=now,
        finished_at=str(result.get("finished_at", now)),
    )
    final_revision = verifying["state"]["revision"]
    quarantine = unknown
    effective_quarantine_token = quarantine_token or secrets.token_hex(24)
    with store.mutation(
        preclaim.plan_id,
        expected_revision=final_revision,
        timestamp=now,
    ) as mutation:
        _, receipt_quarantine = mutation.finalize_task(
            receipt,
            guard_reason=(
                "invocation_unknown"
                if unknown
                else verification.guard_reason
            ),
        )
        if receipt_quarantine != quarantine:
            raise StateConflict("plan worker receipt quarantine mismatch")
        if quarantine:
            mutation.quarantine_plan_lease(
                expected_outer_revision=expected_outer_revision + 1,
                current_holder_token=worker_token,
                holder_token=effective_quarantine_token,
                expires_at=expiry,
            )
        else:
            mutation.release_plan_lease(
                expected_outer_revision=expected_outer_revision + 1,
                holder_token=worker_token,
            )
    final = store.load_plan(preclaim.plan_id)
    outer = store.goal_store.load_goal(final["outer_goal_id"])
    wakeup_status: str | None = None
    wakeup_sha256: str | None = None
    if coordinator_provider is not None and coordinator_thread_id is not None:
        if final.get("activation_goal_text") is None:
            raise IntegrityError(
                "continuous coordinator wakeup requires a profile-aware plan"
            )
        from agentjob_runtime.plan.continuous import notify_coordinator

        wakeup = notify_coordinator(
            store,
            plan_id=preclaim.plan_id,
            generation=preclaim.generation,
            worker_thread_id=current_thread_id,
            task_receipt_sha256=content_sha256(receipt),
            provider=coordinator_provider,
            timestamp=now,
        )
        wakeup_status = str(wakeup["status"])
        wakeup_sha256 = content_sha256(wakeup)
    return PlanWorkerSummary(
        (
            "invocation_unknown"
            if unknown
            else verification.disposition
        ),
        preclaim.plan_id,
        preclaim.task_id,
        preclaim.generation,
        final["state"]["revision"],
        outer["state"]["revision"],
        "unknown" if unknown else 1,
        result["agentjobs"],
        content_sha256(receipt),
        quarantine,
        wakeup_status,
        wakeup_sha256,
    )
