"""Deterministic receipt-backed scheduling for implementation-plan state."""

from __future__ import annotations

import heapq
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from agentjob_runtime.errors import (
    IntegrityError,
    RecordValidationError,
    SecurityError,
)
from agentjob_runtime.plan.model import (
    ACTIVE_TASK_STATUSES,
    PROTECTED_STOP_TASK_STATUSES,
)
from agentjob_runtime.records.canonical import (
    canonical_json_bytes,
    content_sha256,
)
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


SELECTOR_PROTOCOL_VERSION = "1.0.0"
SELECTION_POLICY = {
    "protocol": "sys4ai.plan-selection-policy.v1",
    "canonical_order_only": True,
    "one_active_task_maximum": 1,
    "terminal_dependency_statuses": ["completed", "superseded"],
    "receipt_required_for_terminal_dependency": True,
    "compare_and_swap_required": True,
    "state_mutation": False,
}
SELECTION_POLICY_SHA256 = content_sha256(SELECTION_POLICY)
NON_SCHEDULABLE_PHASES = frozenset(
    {
        "recovery_pending",
        "terminal_blocked_no_runnable",
        "terminal_awaiting_human",
        "terminal_validation_failed",
        "terminal_capability_blocked",
        "terminal_corrupt_state",
        "terminal_cancelled",
    }
)


@dataclass(frozen=True)
class SelectionResult:
    """One deterministic result over an exact canonical plan revision."""

    status: str
    reason_code: str
    proof: dict[str, Any]
    selected_task: dict[str, Any] | None
    ready_task_ids: tuple[str, ...]
    topological_task_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["ready_task_ids"] = list(self.ready_task_ids)
        value["topological_task_ids"] = list(self.topological_task_ids)
        return value


def _ordered_ids(
    task_ids: Sequence[str],
    definitions: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    return sorted(
        {str(task_id) for task_id in task_ids},
        key=lambda task_id: (
            int(definitions[task_id]["canonical_position"]),
            task_id,
        ),
    )


def effective_topological_order(
    *,
    definitions: Mapping[str, Mapping[str, Any]],
    effective_task_ids: Mapping[str, Sequence[str]],
) -> tuple[str, ...]:
    """Return the canonical-priority topological order of effective leaves."""

    if not definitions:
        raise RecordValidationError("plan scheduler requires at least one task")
    for task_id in definitions:
        leaves = effective_task_ids.get(task_id)
        if not leaves:
            raise IntegrityError(
                "plan task has no effective task leaf",
                details={"task_id": task_id},
            )
        if any(leaf not in definitions for leaf in leaves):
            raise IntegrityError(
                "plan task resolves to an unknown effective leaf",
                details={"task_id": task_id},
            )

    nodes = {
        leaf
        for task_id in definitions
        for leaf in effective_task_ids[task_id]
    }
    dependencies: dict[str, set[str]] = {task_id: set() for task_id in nodes}
    dependents: dict[str, set[str]] = {task_id: set() for task_id in nodes}
    for task_id in nodes:
        definition = definitions[task_id]
        for dependency_id in definition["depends_on"]:
            if dependency_id not in definitions:
                raise IntegrityError(
                    "plan task names an unknown dependency",
                    details={
                        "task_id": task_id,
                        "dependency_task_id": dependency_id,
                    },
                )
            for effective_dependency in effective_task_ids[dependency_id]:
                if effective_dependency == task_id:
                    raise IntegrityError(
                        "plan effective dependency graph has a cycle",
                        details={"task_id": task_id},
                    )
                dependencies[task_id].add(effective_dependency)
                dependents[effective_dependency].add(task_id)

    ready = [
        (
            int(definitions[task_id]["canonical_position"]),
            task_id,
        )
        for task_id, task_dependencies in dependencies.items()
        if not task_dependencies
    ]
    heapq.heapify(ready)
    remaining = {
        task_id: set(task_dependencies)
        for task_id, task_dependencies in dependencies.items()
    }
    ordered: list[str] = []
    while ready:
        _, task_id = heapq.heappop(ready)
        ordered.append(task_id)
        for dependent in sorted(
            dependents[task_id],
            key=lambda value: (
                int(definitions[value]["canonical_position"]),
                value,
            ),
        ):
            remaining[dependent].discard(task_id)
            if not remaining[dependent]:
                heapq.heappush(
                    ready,
                    (
                        int(definitions[dependent]["canonical_position"]),
                        dependent,
                    ),
                )
    if len(ordered) != len(nodes):
        raise IntegrityError("plan effective dependency graph has a cycle")
    return tuple(ordered)


def _proof_status(status: str) -> str:
    if status in {"active", "verifying"}:
        return "active"
    if status == "reserved":
        return "reserved"
    if status == "completed":
        return "completed"
    if status == "superseded":
        return "superseded"
    if status == "invocation_unknown":
        return "recovery_pending"
    if status in PROTECTED_STOP_TASK_STATUSES:
        return "blocked"
    return "pending"


def validate_selection_proof_snapshot(proof: Mapping[str, Any]) -> None:
    """Validate deterministic fields not expressible in the JSON schema."""

    if proof.get("selection_policy_sha256") != SELECTION_POLICY_SHA256:
        raise RecordValidationError("selection proof policy hash is unsupported")
    ordered = list(proof.get("ordered_tasks", []))
    positions = [item.get("canonical_position") for item in ordered]
    if (
        positions != sorted(positions)
        or len(set(positions)) != len(positions)
        or len({item.get("task_id") for item in ordered}) != len(ordered)
    ):
        raise RecordValidationError(
            "selection proof tasks are not in unique canonical order"
        )
    ready = [
        item
        for item in ordered
        if item.get("status") == "pending"
        and item.get("dependency_ready") is True
        and item.get("effective_task_ids") == [item.get("task_id")]
    ]
    if proof.get("outcome") == "selected":
        selected = proof.get("selected_task")
        if not ready or not isinstance(selected, Mapping) or any(
            selected.get(key) != ready[0].get(key)
            for key in ("task_id", "task_sha256", "canonical_position")
        ):
            raise RecordValidationError(
                "selection proof does not select the first ready task"
            )
    expected_id = "PSP-" + content_sha256(
        {
            "plan_id": proof.get("plan_id"),
            "plan_sha256": proof.get("plan_sha256"),
            "plan_revision": proof.get("plan_revision"),
            "prior_journal_sha256": proof.get("prior_journal_sha256"),
            "selection_policy_sha256": proof.get("selection_policy_sha256"),
            "supersession_graph_sha256": proof.get(
                "supersession_graph_sha256"
            ),
        }
    )[:24].upper()
    if proof.get("proof_id") != expected_id:
        raise RecordValidationError("selection proof ID is not deterministic")


def build_selection_result(
    *,
    record: Mapping[str, Any],
    definitions: Mapping[str, Mapping[str, Any]],
    effective_task_ids: Mapping[str, Sequence[str]],
    task_evidence: Mapping[str, Mapping[str, Any]],
    ready_task_ids: Sequence[str],
    supersession_graph_sha256: str,
    selection_schema_path: str | Path,
) -> SelectionResult:
    """Build one proof and result from a validated, revision-bound snapshot."""

    ordered_definitions = sorted(
        definitions.values(),
        key=lambda item: (
            int(item["canonical_position"]),
            str(item["task_id"]),
        ),
    )
    positions = [int(item["canonical_position"]) for item in ordered_definitions]
    if len(set(positions)) != len(positions):
        raise IntegrityError("plan scheduler found duplicate canonical positions")
    state_by_id = {
        str(item["task_id"]): item for item in record["state"]["tasks"]
    }
    if set(state_by_id) != set(definitions) or set(task_evidence) != set(
        definitions
    ):
        raise IntegrityError(
            "plan scheduler snapshot does not cover every task identity"
        )
    topological = effective_topological_order(
        definitions=definitions,
        effective_task_ids=effective_task_ids,
    )

    active_task_ids: list[str] = []
    ordered_tasks: list[dict[str, Any]] = []
    python_ready: list[str] = []
    for definition in ordered_definitions:
        task_id = str(definition["task_id"])
        lifecycle_status = str(state_by_id[task_id]["status"])
        if lifecycle_status in ACTIVE_TASK_STATUSES:
            active_task_ids.append(task_id)
        dependency_proofs: list[dict[str, Any]] = []
        dependency_ready = True
        for dependency_id in definition["depends_on"]:
            resolved = _ordered_ids(
                effective_task_ids[str(dependency_id)],
                definitions,
            )
            leaves = [task_evidence[item] for item in resolved]
            terminal = bool(leaves) and all(
                item.get("complete") is True for item in leaves
            )
            unknown = any(
                item.get("lifecycle_status") == "invocation_unknown"
                for item in leaves
            )
            dependency_ready = dependency_ready and terminal
            dependency_proofs.append(
                {
                    "task_id": str(dependency_id),
                    "effective_task_ids": resolved,
                    "status": (
                        "terminal"
                        if terminal
                        else "unknown"
                        if unknown
                        else "nonterminal"
                    ),
                    "receipt_sha256s": (
                        sorted(
                            str(item["receipt_sha256"])
                            for item in leaves
                            if item.get("receipt_sha256") is not None
                        )
                        if terminal
                        else []
                    ),
                }
            )
        snapshot = {
            "canonical_position": int(definition["canonical_position"]),
            "task_id": task_id,
            "task_sha256": str(definition["task_sha256"]),
            "effective_task_ids": _ordered_ids(
                effective_task_ids[task_id],
                definitions,
            ),
            "status": _proof_status(lifecycle_status),
            "dependencies": dependency_proofs,
            "dependency_ready": dependency_ready,
        }
        ordered_tasks.append(snapshot)
        if (
            snapshot["status"] == "pending"
            and snapshot["dependency_ready"]
            and snapshot["effective_task_ids"] == [task_id]
        ):
            python_ready.append(task_id)

    sql_ready = [str(task_id) for task_id in ready_task_ids]
    proof_ready = [] if active_task_ids else python_ready
    if proof_ready != sql_ready:
        raise IntegrityError(
            "plan ready-task view disagrees with canonical dependency proof",
            details={"proof_ready": proof_ready, "view_ready": sql_ready},
        )
    if len(active_task_ids) > 1:
        raise IntegrityError("plan scheduler found multiple active tasks")

    blocking_reasons: list[str] = []
    selected_task: dict[str, Any] | None = None
    if active_task_ids:
        status = "active_task_present"
        reason_code = "plan.active_task_present"
        proof_outcome = "blocked_no_runnable"
        blocking_reasons = ["selection.active_task_present"]
    elif record["state"]["phase"] in NON_SCHEDULABLE_PHASES:
        status = "blocked_no_runnable"
        reason_code = "plan.no_ready_task"
        proof_outcome = "blocked_no_runnable"
        blocking_reasons = ["selection.state_not_schedulable"]
    elif all(
        task_evidence[task_id].get("complete") is True
        for task_id in topological
    ):
        status = "completion_candidate"
        reason_code = "plan.completion_candidate"
        proof_outcome = "completion_candidate"
    elif sql_ready:
        status = "selected"
        reason_code = "plan.task_selected"
        proof_outcome = "selected"
        first = next(
            item for item in ordered_tasks if item["task_id"] == sql_ready[0]
        )
        selected_task = {
            "task_id": first["task_id"],
            "task_sha256": first["task_sha256"],
            "canonical_position": first["canonical_position"],
            "dependency_receipt_sha256s": sorted(
                {
                    receipt
                    for dependency in first["dependencies"]
                    for receipt in dependency["receipt_sha256s"]
                }
            ),
        }
    elif any(
        task_evidence[task_id].get("lifecycle_status") == "pending"
        for task_id in topological
    ):
        status = "blocked_no_runnable"
        reason_code = "plan.no_ready_task"
        proof_outcome = "no_ready_task"
        blocking_reasons = ["selection.dependencies_not_terminal"]
    else:
        status = "blocked_no_runnable"
        reason_code = "plan.no_ready_task"
        proof_outcome = "blocked_no_runnable"
        blocking_reasons = ["selection.no_runnable_task"]

    lease = record["state"].get("lease")
    lease_hash = (
        str(lease["holder_token_hash"])
        if isinstance(lease, Mapping)
        else content_sha256(None)
    )
    proof: dict[str, Any] = {
        "schema_version": "sys4ai.plan-selection-proof.v1",
        "proof_id": "PSP-PENDING",
        "plan_id": record["plan_id"],
        "plan_sha256": record["effective_plan_sha256"],
        "plan_revision": record["state"]["revision"],
        "prior_journal_sha256": record["journal"][-1]["event_hash"],
        "repository_fingerprint": record["repository_fingerprint"],
        "selector_protocol_version": SELECTOR_PROTOCOL_VERSION,
        "selection_policy_sha256": SELECTION_POLICY_SHA256,
        "supersession_graph_sha256": supersession_graph_sha256,
        "lease_token_sha256": lease_hash,
        "active_task_ids": active_task_ids,
        "ordered_tasks": ordered_tasks,
        "outcome": proof_outcome,
        "selected_task": selected_task,
        "blocking_reasons": blocking_reasons,
        "canonical_order_only": True,
        "revision_bound": True,
        "compare_and_swap_required": True,
        "hash_basis": "canonical_json_without_proof_content_sha256",
        "proof_content_sha256": "0" * 64,
        "finalized": True,
        "extensions": {},
    }
    proof["proof_id"] = "PSP-" + content_sha256(
        {
            "plan_id": proof["plan_id"],
            "plan_sha256": proof["plan_sha256"],
            "plan_revision": proof["plan_revision"],
            "prior_journal_sha256": proof["prior_journal_sha256"],
            "selection_policy_sha256": proof["selection_policy_sha256"],
            "supersession_graph_sha256": proof[
                "supersession_graph_sha256"
            ],
        }
    )[:24].upper()
    proof["proof_content_sha256"] = content_sha256(
        {
            key: value
            for key, value in proof.items()
            if key != "proof_content_sha256"
        }
    )
    issues = validate_instance(proof, selection_schema_path)
    if issues:
        raise RecordValidationError(
            "runtime selection proof failed canonical validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    validate_selection_proof_snapshot(proof)
    if contains_secret(canonical_json_bytes(proof).decode("utf-8")):
        raise SecurityError("selection proof appears to contain a secret")
    return SelectionResult(
        status=status,
        reason_code=reason_code,
        proof=proof,
        selected_task=selected_task,
        ready_task_ids=tuple(sql_ready),
        topological_task_ids=topological,
    )
