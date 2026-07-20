"""Bounded System Director selection and one-packet activation."""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from agentjob_runtime.continue_flow.preflight import ContinuePreflight
from agentjob_runtime.control.activation import ActivationReceipt, activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.execution.repository_topology import (
    PROTECTED_TOPOLOGY_ACTIONS,
    classify_topology_command,
)
from agentjob_runtime.goal.model import utc_now


@dataclass(frozen=True)
class DirectorRoute:
    route_id: str
    role_id: str
    role_version: str
    priority: int
    rationale: str
    job_spec: Mapping[str, Any]
    role_spec: Mapping[str, Any]
    forced_by_rule_id: str | None = None
    requires_human_gate: bool = False
    human_gate_refs: tuple[Mapping[str, Any], ...] = ()
    authority_expansion: bool = False
    domain_truth_decision: bool = False
    domain_authority_ref: str | None = None


@dataclass(frozen=True)
class RepairRouteDeclaration:
    """A target-declared, authority-bounded automated repair process."""

    repair_id: str
    supported_reason_codes: tuple[str, ...]
    route: DirectorRoute
    provider_or_command: str
    required_authority: tuple[str, ...]
    input_schema_ref: str
    output_schema_ref: str
    idempotency_behavior: str
    validators: tuple[str, ...]
    rollback_or_recovery: str
    consumes_agentjob: bool
    changes_project_state: bool

    def __post_init__(self) -> None:
        if (
            not self.repair_id.strip()
            or not self.supported_reason_codes
            or not self.provider_or_command.strip()
            or not self.required_authority
            or not self.input_schema_ref.strip()
            or not self.output_schema_ref.strip()
            or not self.idempotency_behavior.strip()
            or not self.validators
            or not self.rollback_or_recovery.strip()
        ):
            raise RecordValidationError(
                "repair declarations require complete, inspectable metadata"
            )
        legal, reason = _route_legality(self.route)
        if not legal:
            raise RecordValidationError(
                f"repair declaration is not legal inside existing authority: {reason}"
            )
        authority = self.route.job_spec.get("authority", {})
        allowed_actions = set(authority.get("allowed_actions", ()))
        if set(self.required_authority) - allowed_actions:
            raise RecordValidationError(
                "repair required authority exceeds the declared AgentJob authority"
            )
        if allowed_actions & PROTECTED_TOPOLOGY_ACTIONS:
            raise RecordValidationError(
                "repair declarations cannot include repository-topology authority"
            )
        for command in self.route.job_spec.get("commands", {}).get(
            "approved", ()
        ):
            if classify_topology_command(command.get("argv", ())) is not None:
                raise RecordValidationError(
                    "repair declarations cannot create branches or worktrees"
                )


@dataclass(frozen=True)
class DirectorOutcome:
    status: str
    boundary: str
    reason_code: str
    task_id: str | None
    decision: Mapping[str, Any] | None = None
    job: Mapping[str, Any] | None = None
    execution_role: Mapping[str, Any] | None = None
    activation: Mapping[str, Any] | None = None
    rejected_routes: tuple[str, ...] = ()
    execution_performed: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _records_for_task(
    store: FilesystemControlStore, task_id: str
) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None]:
    task = store.load_task(task_id)
    decision = None
    job = None
    role = None
    for kind, _, record in store.iter_records():
        if kind == "director_decision" and record.get("decision_id") == task.get("current_decision_id"):
            decision = record
        elif kind == "agent_job" and record.get("job_id") == task.get("current_job_id"):
            job = record
    if job:
        matches = [
            record
            for kind, _, record in store.iter_records()
            if kind == "execution_role" and record.get("job_id") == job.get("job_id")
        ]
        role = matches[0] if len(matches) == 1 else None
    return task, decision, job, role


def _route_legality(route: DirectorRoute) -> tuple[bool, str]:
    if route.requires_human_gate:
        return False, "human gate is required"
    if route.authority_expansion:
        return False, "route would expand authority beyond current policy"
    if route.domain_truth_decision and not route.domain_authority_ref:
        return False, "route would decide domain truth without declared domain authority"
    if route.job_spec.get("authority", {}).get("external_effects") and not route.job_spec.get(
        "external_effect_authority_refs"
    ):
        return False, "external effects lack exact authority references"
    return True, route.rationale


def _reason_supported(reason_code: str, declared: str) -> bool:
    return declared == reason_code or (
        declared.endswith(".*")
        and reason_code.startswith(declared[:-1])
    )


def declared_repair_routes(
    preflight: ContinuePreflight,
    declarations: Sequence[RepairRouteDeclaration],
) -> tuple[DirectorRoute, ...]:
    """Return only declared routes that support this exact machine boundary."""

    reason_code = str(preflight.boundary["reason_code"])
    result: list[DirectorRoute] = []
    for declaration in declarations:
        if not any(
            _reason_supported(reason_code, supported)
            for supported in declaration.supported_reason_codes
        ):
            continue
        if declaration.consumes_agentjob is not True:
            continue
        result.append(declaration.route)
    return tuple(result)


def _select_route(routes: Sequence[DirectorRoute]) -> tuple[DirectorRoute | None, str, list[tuple[DirectorRoute, str]]]:
    assessed = [(route, *_route_legality(route)) for route in routes]
    legal = [route for route, allowed, _ in assessed if allowed]
    blocked = [(route, reason) for route, allowed, reason in assessed if not allowed]
    if not legal:
        return None, "protected", blocked
    forced = [route for route in legal if route.forced_by_rule_id]
    if len(forced) > 1:
        raise StateConflict("multiple policy-forced Director routes conflict")
    if forced:
        selected = forced[0]
        mode = "deterministic"
    elif len(legal) == 1:
        selected = legal[0]
        mode = "deterministic"
    else:
        selected = sorted(
            legal,
            key=lambda route: (
                route.priority,
                len(route.job_spec.get("authority", {}).get("allowed_write_paths", [])),
                len(route.job_spec.get("authority", {}).get("allowed_actions", [])),
                route.route_id,
            ),
        )[0]
        mode = "deliberative"
    return selected, mode, blocked


def _build_packet(
    *,
    task: Mapping[str, Any],
    selected: DirectorRoute,
    routes: Sequence[DirectorRoute],
    mode: str,
    blocked: Sequence[tuple[DirectorRoute, str]],
    preflight: ContinuePreflight,
    store: FilesystemControlStore,
    expected_revision: int,
    actor_ref: str,
    policy_refs: Sequence[str],
    timestamp: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    task_id = str(task["task_id"])
    serial = expected_revision + 1
    decision_id = f"DDR-{task_id}-{serial}"
    job_id = f"AJ-{task_id}-{serial}"
    role_id = f"ER-{job_id}"
    job_spec = copy.deepcopy(dict(selected.job_spec))
    role_spec = copy.deepcopy(dict(selected.role_spec))
    role_path = store.relative(store.record_path("execution_role", task_id, role_id))
    rejected = [route for route in routes if route.route_id != selected.route_id]
    assessments = []
    blocked_by_id = {route.route_id: reason for route, reason in blocked}
    for route in routes:
        assessments.append(
            {
                "route_id": route.route_id,
                "role_id": route.role_id,
                "assessment": "accepted"
                if route.route_id == selected.route_id
                else "blocked"
                if route.route_id in blocked_by_id
                else "rejected",
                "reason": selected.rationale
                if route.route_id == selected.route_id
                else blocked_by_id.get(route.route_id, "A narrower or higher-priority legal route was selected."),
            }
        )
    rejected_alternatives = [
        f"{route.route_id}: {blocked_by_id.get(route.route_id, 'not selected by deliberative ranking')}"
        for route in rejected
    ]
    if mode == "deliberative" and not rejected_alternatives:
        raise RecordValidationError("deliberative decisions require a rejected alternative")
    rejected_illegal = [f"{route.route_id}: {reason}" for route, reason in blocked]
    if mode == "deterministic" and not rejected_illegal:
        rejected_illegal = ["No alternative route satisfied the deterministic selection rule."]
    decision = {
        "schema_version": "sys4ai.director-decision.v1",
        "decision_id": decision_id,
        "task_id": task_id,
        "decision_authority": {
            "kind": "system_director",
            "actor_ref": actor_ref,
            "policy_refs": list(policy_refs),
        },
        "decision_type": "create_job",
        "decision_mode": mode,
        "status": "activated",
        "evidence": {
            "state_snapshot_ref": f"preflight-snapshot-{preflight.fingerprint}.json",
            "state_snapshot_sha256": str(preflight.fingerprint),
            "handoff_refs": [],
            "source_refs": list(job_spec.pop("source_refs", [])),
        },
        "candidates": assessments,
        "selected": {
            "route_id": selected.route_id,
            "role_id": selected.role_id,
            "role_version": selected.role_version,
            "agent_job_id": job_id,
            "rationale": selected.rationale,
        },
        "rejected_alternatives": rejected_alternatives,
        "requires_human_gate": False,
        "human_gate_refs": [],
        "claim_boundary": copy.deepcopy(job_spec["claim_boundary"]),
        "supersedes_decision_id": None,
        "rule_id": selected.forced_by_rule_id
        or (f"single-legal-route:{selected.route_id}" if mode == "deterministic" else None),
        "rejected_illegal_routes": rejected_illegal,
        "created_at": timestamp,
        "activated_at": timestamp,
        "completed_at": None,
        "extensions": {},
    }
    job = {
        "schema_version": "sys4ai.agent-job.v1",
        "job_id": job_id,
        "task_id": task_id,
        "decision_id": decision_id,
        "status": "active",
        "activated_at": timestamp,
        "objective": str(job_spec["objective"]),
        "role_binding": {
            "role_id": selected.role_id,
            "role_version": selected.role_version,
            "execution_role_ref": role_path,
        },
        "authority": copy.deepcopy(job_spec["authority"]),
        "source_policy": copy.deepcopy(job_spec["source_policy"]),
        "commands": copy.deepcopy(job_spec["commands"]),
        "validators": copy.deepcopy(job_spec["validators"]),
        "expected_outputs": copy.deepcopy(job_spec["expected_outputs"]),
        "completion_contract": copy.deepcopy(job_spec["completion_contract"]),
        "stop_conditions": copy.deepcopy(job_spec["stop_conditions"]),
        "checkpoint": copy.deepcopy(job_spec["checkpoint"]),
        "claim_boundary": copy.deepcopy(job_spec["claim_boundary"]),
        "concurrency": {
            "policy": job_spec.get("concurrency", {}).get("policy", "exclusive_worktree"),
            "lease_scope": job_spec.get("concurrency", {}).get(
                "lease_scope", "repository_worktree"
            ),
            "idempotency_key": job_id,
        },
        "extensions": copy.deepcopy(job_spec.get("extensions", {})),
    }
    role = {
        "schema_version": "sys4ai.execution-role.v1",
        "execution_role_id": role_id,
        "job_id": job_id,
        "task_id": task_id,
        "binding_type": role_spec.get("binding_type", "registered_role"),
        "role_id": selected.role_id,
        "role_version": selected.role_version,
        "responsibilities": copy.deepcopy(role_spec["responsibilities"]),
        "may_not": copy.deepcopy(role_spec["may_not"]),
        "source_role_ref": role_spec.get("source_role_ref"),
        "task_overlay": copy.deepcopy(role_spec.get("task_overlay")),
        "authority_delta": str(role_spec.get("authority_delta", "No permission expansion.")),
        "provisional_role": copy.deepcopy(role_spec.get("provisional_role")),
        "requires_human_gate": False,
        "human_gate_refs": [],
        "expires_after": job_id,
        "activated_at": timestamp,
        "extensions": copy.deepcopy(role_spec.get("extensions", {})),
    }
    return decision, job, role


def resolve_director_packet(
    preflight: ContinuePreflight,
    *,
    store: FilesystemControlStore,
    routes: Sequence[DirectorRoute] = (),
    repair_routes: Sequence[RepairRouteDeclaration] = (),
    expected_revision: int | None = None,
    actor_ref: str = "continue:system-director",
    policy_refs: Sequence[str] = (".agents/control/policies/default.json",),
    policies: Sequence[Mapping[str, Any]] = (),
    timestamp: str | None = None,
) -> DirectorOutcome:
    boundary = str(preflight.boundary["boundary"])
    task_id = preflight.boundary.get("task_id")
    if boundary == "existing_agent_job_ready":
        if not task_id:
            raise StateConflict("ready boundary lacks task identity")
        _, decision, job, role = _records_for_task(store, str(task_id))
        if not all((decision, job, role)):
            raise StateConflict("ready boundary packet disappeared before reuse")
        return DirectorOutcome(
            "reused",
            boundary,
            "job.activated_and_ready",
            str(task_id),
            decision,
            job,
            role,
        )
    machine_boundary = boundary in {
        "bootstrap_required",
        "no_action",
        "blocked",
        "control_repair_required",
    }
    if machine_boundary:
        routes = declared_repair_routes(preflight, repair_routes)
    elif boundary != "director_decision_required":
        return DirectorOutcome(
            "protected_stop",
            boundary,
            str(preflight.boundary["reason_code"]),
            str(task_id) if task_id else None,
        )
    if not task_id or expected_revision is None:
        if machine_boundary:
            return DirectorOutcome(
                "protected_stop",
                boundary,
                "director.repair_requires_existing_task_authority",
                str(task_id) if task_id else None,
            )
        raise RecordValidationError(
            "new Director packet requires task ID and expected revision"
        )
    if not routes:
        return DirectorOutcome(
            "protected_stop",
            boundary,
            "director.no_declared_repair_route"
            if machine_boundary
            else "director.no_candidate_route",
            str(task_id),
        )
    selected, mode, blocked = _select_route(routes)
    if selected is None:
        reason = (
            "director.human_gate_required"
            if any(route.requires_human_gate for route, _ in blocked)
            else "director.no_legal_route"
        )
        return DirectorOutcome(
            "protected_stop",
            "human_gate_required" if "human_gate" in reason else "blocked",
            reason,
            str(task_id),
            rejected_routes=tuple(f"{route.route_id}: {why}" for route, why in blocked),
        )
    task = store.load_task(str(task_id))
    if task["revision"] != expected_revision:
        raise StateConflict(
            f"task revision changed before Director activation: {task['revision']}"
        )
    now = timestamp or utc_now()
    decision, job, role = _build_packet(
        task=task,
        selected=selected,
        routes=routes,
        mode=mode,
        blocked=blocked,
        preflight=preflight,
        store=store,
        expected_revision=expected_revision,
        actor_ref=actor_ref,
        policy_refs=policy_refs,
        timestamp=now,
    )
    receipt: ActivationReceipt = activate_packet(
        store,
        task_id=str(task_id),
        decision=decision,
        job=job,
        execution_role=role,
        expected_revision=expected_revision,
        policies=policies,
    )
    return DirectorOutcome(
        "activated",
        boundary,
        "director.repair_packet_activated"
        if machine_boundary
        else "director.one_packet_activated",
        str(task_id),
        decision,
        job,
        role,
        receipt.as_dict(),
        tuple(f"{route.route_id}: {why}" for route, why in blocked),
    )
