"""Canonical plan-task envelope and bounded worker-prompt construction."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.plan.scheduler import validate_selection_proof_snapshot
from agentjob_runtime.records.canonical import (
    canonical_json_bytes,
    content_sha256,
    render_canonical_json,
)
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


PLAN_TASK_REPOSITORY_FIELDS = (
    "root",
    "worktree",
    "branch",
    "starting_revision",
    "environment_mode",
)


def _positive_integer(value: Any, *, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise RecordValidationError(f"{field_name} must be a positive integer")
    return value


def _validate_plan_task_envelope(
    envelope: Mapping[str, Any],
    *,
    schema_path: str | Path,
) -> dict[str, Any]:
    value = copy.deepcopy(dict(envelope))
    issues = validate_instance(value, schema_path)
    if issues:
        raise RecordValidationError(
            "plan-task envelope failed canonical validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    return value


def _selected_task_snapshot(
    selection_proof: Mapping[str, Any],
    task_definition: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    proof = copy.deepcopy(dict(selection_proof))
    definition = copy.deepcopy(dict(task_definition))
    validate_selection_proof_snapshot(proof)
    selected = proof.get("selected_task")
    if proof.get("outcome") != "selected" or not isinstance(selected, Mapping):
        raise StateConflict("plan-task prompt requires one selected task")
    if (
        definition.get("task_id") != selected.get("task_id")
        or definition.get("task_sha256") != selected.get("task_sha256")
    ):
        raise StateConflict(
            "selected task definition differs from the selection proof"
        )
    snapshots = [
        item
        for item in proof.get("ordered_tasks", [])
        if isinstance(item, Mapping)
        and item.get("task_id") == selected.get("task_id")
    ]
    if len(snapshots) != 1:
        raise StateConflict(
            "selection proof does not contain exactly one selected-task snapshot"
        )
    snapshot = copy.deepcopy(dict(snapshots[0]))
    if (
        snapshot.get("task_sha256") != selected.get("task_sha256")
        or snapshot.get("status") != "pending"
        or snapshot.get("dependency_ready") is not True
        or not isinstance(snapshot.get("dependencies"), list)
    ):
        raise StateConflict(
            "selection proof does not establish a dependency-ready pending task"
        )
    return proof, snapshot


def build_plan_task_dependency_proof(
    selection_proof: Mapping[str, Any],
    task_definition: Mapping[str, Any],
) -> dict[str, Any]:
    """Return the bounded provider projection of one canonical selection proof."""

    proof, snapshot = _selected_task_snapshot(
        selection_proof,
        task_definition,
    )
    dependency_proof = {
        "selection_proof_id": proof["proof_id"],
        "selection_proof_sha256": content_sha256(proof),
        "plan_revision": proof["plan_revision"],
        "prior_journal_sha256": proof["prior_journal_sha256"],
        "selected_task": copy.deepcopy(proof["selected_task"]),
        "dependencies": copy.deepcopy(snapshot["dependencies"]),
        "dependency_ready": True,
    }
    if contains_secret(
        canonical_json_bytes(dependency_proof).decode("utf-8")
    ):
        raise RecordValidationError(
            "plan-task dependency proof appears to contain a secret"
        )
    return dependency_proof


def build_plan_task_envelope(
    plan_record: Mapping[str, Any],
    *,
    selection_proof: Mapping[str, Any],
    task_definition: Mapping[str, Any],
    generation: int,
    handoff_token: str,
    predecessor_thread_id: str | None,
    schema_path: str | Path,
) -> dict[str, Any]:
    """Build one independently validated envelope for the selected task."""

    generation = _positive_integer(generation, field_name="generation")
    if not isinstance(handoff_token, str) or len(handoff_token) < 32:
        raise RecordValidationError(
            "plan-task handoff token must contain at least 32 characters"
        )
    if predecessor_thread_id is not None and (
        not isinstance(predecessor_thread_id, str)
        or not predecessor_thread_id.strip()
    ):
        raise RecordValidationError(
            "predecessor_thread_id must be null or a nonblank string"
        )
    record = copy.deepcopy(dict(plan_record))
    proof, _ = _selected_task_snapshot(selection_proof, task_definition)
    selected = proof["selected_task"]
    state = record.get("state")
    repository_binding = record.get("repository_binding")
    if not isinstance(state, Mapping) or not isinstance(
        repository_binding,
        Mapping,
    ):
        raise RecordValidationError(
            "plan-task envelope requires a canonical runtime plan record"
        )
    if (
        record.get("plan_id") != proof.get("plan_id")
        or record.get("effective_plan_sha256") != proof.get("plan_sha256")
        or record.get("repository_fingerprint")
        != proof.get("repository_fingerprint")
        or state.get("revision") != proof.get("plan_revision")
        or generation != int(state.get("current_generation", -1)) + 1
    ):
        raise StateConflict(
            "plan-task envelope identity differs from canonical selection state"
        )
    projected_binding = {
        field: copy.deepcopy(repository_binding.get(field))
        for field in PLAN_TASK_REPOSITORY_FIELDS
    }
    profile_aware = record.get("runtime_profile_version") == 2
    envelope: dict[str, Any] = {
        "schema_version": (
            "sys4ai.plan-task-envelope.v2"
            if profile_aware
            else "sys4ai.plan-task-envelope.v1"
        ),
        "plan_id": record["plan_id"],
        "plan_sha256": record["effective_plan_sha256"],
        "task_id": selected["task_id"],
        "task_sha256": selected["task_sha256"],
        "generation": generation,
        "handoff_token": handoff_token,
        "idempotency_key": f"{record['plan_id']}:{generation}",
        "predecessor_thread_id": predecessor_thread_id,
        "repository_binding": projected_binding,
        "one_task_per_discussion": True,
        "max_continue_invocations": 1,
        "max_agentjobs": 1,
        "required_skill": "continue-implementing-plan-task",
        "extensions": {},
    }
    if profile_aware:
        execution_profile = record.get("execution_profile")
        topology_policy = record.get("repository_topology_policy")
        if (
            not isinstance(execution_profile, Mapping)
            or not isinstance(topology_policy, Mapping)
            or record.get("activation_receipt_sha256") is None
            or record.get("repository_binding_sha256") is None
            or record.get("activation_sequence") is None
            or generation
            < int(execution_profile.get("effective_from_generation", 0))
        ):
            raise StateConflict(
                "profile-aware plan lacks an effective canonical task profile"
            )
        if record["repository_binding_sha256"] != content_sha256(
            record["repository_binding"]
        ):
            raise StateConflict(
                "profile-aware plan repository binding hash has drifted"
            )
        envelope.update(
            {
                "activation_receipt_sha256": record[
                    "activation_receipt_sha256"
                ],
                "execution_profile": copy.deepcopy(
                    dict(execution_profile)
                ),
                "repository_topology_policy": copy.deepcopy(
                    dict(topology_policy)
                ),
                "repository_binding_sha256": record[
                    "repository_binding_sha256"
                ],
                "activation_sequence": record["activation_sequence"],
            }
        )
    return _validate_plan_task_envelope(envelope, schema_path=schema_path)


def build_plan_task_worker_prompt(
    envelope: Mapping[str, Any],
    *,
    task_definition: Mapping[str, Any],
    selection_proof: Mapping[str, Any],
    expected_revision: int,
    schema_path: str | Path,
) -> str:
    """Render the minimum token-bearing prompt for one future worker claim."""

    expected_revision = _positive_integer(
        expected_revision,
        field_name="expected_revision",
    )
    value = _validate_plan_task_envelope(envelope, schema_path=schema_path)
    definition = copy.deepcopy(dict(task_definition))
    proof, _ = _selected_task_snapshot(selection_proof, definition)
    if (
        value["plan_id"] != proof["plan_id"]
        or value["plan_sha256"] != proof["plan_sha256"]
        or value["task_id"] != proof["selected_task"]["task_id"]
        or value["task_sha256"] != proof["selected_task"]["task_sha256"]
        or expected_revision <= proof["plan_revision"]
    ):
        raise StateConflict(
            "plan-task worker prompt identity or expected revision is stale"
        )
    dependency_proof = build_plan_task_dependency_proof(proof, definition)
    return (
        "Invoke the installed continue-implementing-plan-task skill in normal mode.\n"
        "Wait for the plan coordinator to record this worker before claiming the task.\n"
        + (
            "Authoritative accepted reasoning_effort: "
            f"{value['execution_profile']['reasoning_effort']}\n"
            "Authoritative environment_mode: reuse_bound_checkout\n"
            if value["schema_version"] == "sys4ai.plan-task-envelope.v2"
            else ""
        )
        +
        f"project_root: {value['repository_binding']['root']}\n"
        f"expected_revision: {expected_revision}\n"
        f"envelope_sha256: {content_sha256(value)}\n"
        f"selection_proof_sha256: {content_sha256(proof)}\n"
        f"task_definition_sha256: {content_sha256(definition)}\n"
        f"dependency_proof_sha256: {content_sha256(dependency_proof)}\n"
        "plan_task_envelope:\n"
        + render_canonical_json(value)
        + "selected_task_definition:\n"
        + render_canonical_json(definition)
        + "dependency_proof:\n"
        + render_canonical_json(dependency_proof)
    )
