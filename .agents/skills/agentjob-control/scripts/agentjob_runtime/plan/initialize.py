"""Atomic implementation-plan initialization from validated launcher evidence."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agentjob_runtime.errors import IntegrityError, RecordValidationError, StateConflict
from agentjob_runtime.plan.launcher import PlanLauncherPreflight
from agentjob_runtime.plan.normalize import (
    PLANNING_ADAPTER_ID,
    PlanNormalizationResult,
)
from agentjob_runtime.plan.sqlite_store import SQLitePlanStore
from agentjob_runtime.records.canonical import content_sha256


@dataclass(frozen=True)
class PlanInitializationResult:
    """Safe summary plus exact durable records from one initialization."""

    plan_record: Mapping[str, Any] = field(repr=False)
    normalization_report: Mapping[str, Any] = field(repr=False)
    activation_receipt: Mapping[str, Any] = field(repr=False)
    initialization_receipt: Mapping[str, Any] = field(repr=False)

    def as_dict(self) -> dict[str, Any]:
        plan = self.plan_record
        report = self.normalization_report
        activation = self.activation_receipt
        receipt = self.initialization_receipt
        return {
            "status": "initialized",
            "plan_id": plan["plan_id"],
            "plan_sha256": plan["plan_sha256"],
            "plan_revision": plan["state"]["revision"],
            "plan_phase": plan["state"]["phase"],
            "active_task_id": plan["state"]["active_task_id"],
            "plan_task_lease": plan["state"]["lease"],
            "normalization_report_id": report["report_id"],
            "normalization_report_sha256": report[
                "report_content_sha256"
            ],
            "activation_id": activation["activation_id"],
            "activation_receipt_sha256": content_sha256(activation),
            "reasoning_effort": activation["reasoning_effort"],
            "runtime_profile_version": plan["runtime_profile_version"],
            "initialization_receipt_id": receipt["receipt_id"],
            "initialization_receipt_sha256": receipt[
                "receipt_content_sha256"
            ],
            "outer_goal_revision": receipt["outer_goal_identity"][
                "revision_after"
            ],
            "initial_lease_authority": receipt["initial_lease"]["authority"],
            "state_writes": receipt["materialized"]["state_writes"],
            **copy.deepcopy(receipt["effect_counts"]),
            "next_boundary": receipt["next_boundary"],
        }


def _error(
    message: str,
    *,
    reason_code: str,
    **details: Any,
) -> RecordValidationError:
    return RecordValidationError(
        message,
        details={"reason_code": reason_code, **details},
    )


def _validate_inputs(
    store: SQLitePlanStore,
    preflight: PlanLauncherPreflight,
    normalization: PlanNormalizationResult,
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    if not isinstance(store, SQLitePlanStore):
        raise _error(
            "plan initialization requires the canonical SQLite plan store",
            reason_code="plan.validation_failed",
        )
    if (
        not isinstance(preflight, PlanLauncherPreflight)
        or preflight.status != "ready"
        or not preflight.sources
    ):
        raise _error(
            "plan initialization requires a ready launcher preflight",
            reason_code="plan.validation_failed",
        )
    preflight_effects = {
        "state_writes": preflight.state_writes,
        "provider_create_calls": preflight.provider_create_calls,
        "worker_discussions": preflight.worker_discussions,
        "agentjobs_executed": preflight.agentjobs_executed,
        "continue_invocations": preflight.continue_invocations,
        "task_reservations": preflight.task_reservations,
        "branch_creations": preflight.branch_creations,
        "worktree_creations": preflight.worktree_creations,
    }
    if any(value != 0 for value in preflight_effects.values()):
        raise _error(
            "launcher preflight contains an unexpected prior effect",
            reason_code="plan.validation_failed",
            effect_counts=preflight_effects,
        )
    if (
        not isinstance(normalization, PlanNormalizationResult)
        or not normalization.ready_for_initialization
        or normalization.planning_adapter_id != PLANNING_ADAPTER_ID
    ):
        raise _error(
            "plan initialization requires a canonical candidate normalization",
            reason_code="plan.validation_failed",
        )
    normalization_effects = {
        "state_writes": normalization.state_writes,
        "provider_create_calls": normalization.provider_create_calls,
        "worker_discussions": normalization.worker_discussions,
        "agentjobs_executed": normalization.agentjobs_executed,
        "continue_invocations": normalization.continue_invocations,
        "task_reservations": normalization.task_reservations,
        "branch_creations": normalization.branch_creations,
        "worktree_creations": normalization.worktree_creations,
    }
    if any(value != 0 for value in normalization_effects.values()):
        raise _error(
            "normalization result contains an unexpected prior effect",
            reason_code="plan.validation_failed",
            effect_counts=normalization_effects,
        )
    plan = normalization.candidate_plan
    report = normalization.normalization_report
    if not isinstance(plan, Mapping) or not isinstance(report, Mapping):
        raise _error(
            "candidate normalization omitted its plan or report",
            reason_code="plan.validation_failed",
        )
    if plan.get("repository_binding") != preflight.repository_binding:
        raise StateConflict(
            "candidate repository binding differs from launcher preflight",
            details={"reason_code": "plan.repository_mismatch"},
        )
    if (
        report.get("status") != "candidate"
        or report.get("finalized") is not True
        or report.get("plan_id") != plan.get("plan_id")
        or report.get("candidate_plan_sha256") != content_sha256(plan)
    ):
        raise StateConflict(
            "normalization report differs from its plan candidate",
            details={"reason_code": "plan.hash_mismatch"},
        )
    report_sources = report.get("sources")
    if (
        not isinstance(report_sources, list)
        or len(report_sources) != len(preflight.sources)
    ):
        raise StateConflict(
            "normalization report source set differs from launcher intake",
            details={"reason_code": "plan.hash_mismatch"},
        )
    for intake, source in zip(
        preflight.sources,
        report_sources,
        strict=True,
    ):
        if not isinstance(source, Mapping) or (
            source.get("immutable_ref") != intake.relative_path
            or source.get("source_sha256") != intake.source_sha256
            or source.get("media_type") != intake.media_type
            or source.get("authority") != intake.authority
            or source.get("precedence") != intake.precedence
        ):
            raise StateConflict(
                "normalization report source identity differs from launcher intake",
                details={
                    "reason_code": "plan.hash_mismatch",
                    "path": intake.relative_path,
                },
            )
    expected_state_path = (
        Path(preflight.project_root) / preflight.state_path
    ).resolve(strict=False)
    if expected_state_path != store.path.resolve(strict=False):
        raise StateConflict(
            "plan store path differs from launcher preflight",
            details={
                "reason_code": "plan.repository_mismatch",
                "state_path": preflight.state_path,
            },
        )
    return plan, report


def initialize_plan(
    store: SQLitePlanStore,
    *,
    preflight: PlanLauncherPreflight,
    normalization: PlanNormalizationResult,
    activation_receipt: Mapping[str, Any],
    activation_goal_text: str,
    repository_topology_policy: Mapping[str, Any],
    outer_goal_id: str,
    expected_outer_revision: int,
    outer_holder_token: str,
    timestamp: str | None = None,
) -> PlanInitializationResult:
    """Commit one plan profile, report, receipt, and outer link atomically."""

    plan, report = _validate_inputs(store, preflight, normalization)
    created, receipt = store.create_initialized_plan(
        plan=plan,
        normalization_report=report,
        activation_receipt=activation_receipt,
        activation_goal_text=activation_goal_text,
        repository_topology_policy=repository_topology_policy,
        outer_goal_id=outer_goal_id,
        expected_outer_revision=expected_outer_revision,
        outer_holder_token=outer_holder_token,
        timestamp=timestamp,
    )
    evidence = store.load_plan_initialization(created["plan_id"])
    if (
        evidence is None
        or evidence["normalization_report"] != report
        or evidence["activation_receipt_sha256"]
        != content_sha256(activation_receipt)
        or evidence["initialization_receipt"] != receipt
        or created["state"]["phase"] != "initialized"
        or created["state"]["active_task_id"] is not None
        or created["state"]["lease"] is not None
    ):
        raise IntegrityError(
            "durable plan initialization does not match its validated inputs"
        )
    return PlanInitializationResult(
        plan_record=copy.deepcopy(created),
        normalization_report=copy.deepcopy(report),
        activation_receipt=copy.deepcopy(dict(activation_receipt)),
        initialization_receipt=copy.deepcopy(receipt),
    )
