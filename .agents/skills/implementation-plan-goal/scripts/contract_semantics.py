"""Pure semantic checks for the Phase-02 plan control record contracts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any


def _duplicates(values: list[Any]) -> set[Any]:
    seen: set[Any] = set()
    duplicates: set[Any] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def _cycle_findings(replacements: list[Mapping[str, Any]]) -> list[str]:
    ids = {str(item["task_id"]) for item in replacements}
    graph = {
        str(item["task_id"]): [
            str(dep) for dep in item.get("depends_on", []) if str(dep) in ids
        ]
        for item in replacements
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> bool:
        if task_id in visiting:
            return True
        if task_id in visited:
            return False
        visiting.add(task_id)
        if any(visit(dep) for dep in graph[task_id]):
            return True
        visiting.remove(task_id)
        visited.add(task_id)
        return False

    return ["supersession.replacement_cycle"] if any(visit(item) for item in graph) else []


def _content_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def validate_contract_set(records: Mapping[str, Mapping[str, Any]]) -> list[str]:
    """Return stable semantic findings for one related five-record example set."""

    required = {
        "normalization_report",
        "plan_amendment",
        "task_supersession",
        "provider_intent",
        "selection_proof",
    }
    findings = [f"contracts.missing:{name}" for name in sorted(required - set(records))]
    if findings:
        return findings

    normalization = records["normalization_report"]
    amendment = records["plan_amendment"]
    supersession = records["task_supersession"]
    provider = records["provider_intent"]
    selection = records["selection_proof"]

    plan_ids = {
        str(record["plan_id"])
        for record in (normalization, amendment, supersession, provider, selection)
    }
    if len(plan_ids) != 1:
        findings.append("contracts.plan_id_mismatch")

    sources = list(normalization["sources"])
    if not any(item["authority"] == "accepted" for item in sources):
        findings.append("normalization.accepted_authority_missing")
    if any(item["source_class"] == "mixed_source" for item in sources) and len(sources) < 2:
        findings.append("normalization.mixed_source_cardinality")
    trace_keys = [
        (item["output_kind"], item["output_id"])
        for item in normalization["traceability"]
    ]
    if _duplicates(trace_keys):
        findings.append("normalization.duplicate_trace_target")

    if normalization["candidate_plan_sha256"] != amendment["prior_effective_plan_sha256"]:
        findings.append("amendment.prior_plan_hash_mismatch")
    if amendment["prior_effective_plan_sha256"] == amendment["new_effective_plan_sha256"]:
        findings.append("amendment.no_effect")
    operation_ids = [item["operation_id"] for item in amendment["operations"]]
    if _duplicates(operation_ids):
        findings.append("amendment.duplicate_operation_id")

    effective_hashes = {
        supersession["plan_sha256"],
        provider["plan_sha256"],
        selection["plan_sha256"],
    }
    if effective_hashes != {amendment["new_effective_plan_sha256"]}:
        findings.append("contracts.effective_plan_hash_mismatch")

    original_id = str(supersession["original_task"]["task_id"])
    replacements = list(supersession["replacement_tasks"])
    replacement_ids = [str(item["task_id"]) for item in replacements]
    if original_id in replacement_ids:
        findings.append("supersession.original_task_reused")
    if _duplicates(replacement_ids):
        findings.append("supersession.duplicate_replacement_task")
    findings.extend(_cycle_findings(replacements))
    mapped_ids = {
        str(task_id)
        for item in supersession["acceptance_mapping"]
        for task_id in item["replacement_task_ids"]
    }
    if not mapped_ids <= set(replacement_ids):
        findings.append("supersession.acceptance_unknown_replacement")

    if provider["returned_thread_id"] == provider["predecessor_thread_id"]:
        findings.append("provider.predecessor_reused")

    ordered = list(selection["ordered_tasks"])
    positions = [int(item["canonical_position"]) for item in ordered]
    if positions != sorted(positions) or _duplicates(positions):
        findings.append("selection.canonical_order_invalid")
    ready = [
        item
        for item in ordered
        if item["status"] == "pending" and item["dependency_ready"] is True
    ]
    selected = selection["selected_task"]
    if selection["outcome"] == "selected":
        if not ready:
            findings.append("selection.selected_without_ready_task")
        elif selected is None or any(
            selected[key] != ready[0][key]
            for key in ("task_id", "task_sha256", "canonical_position")
        ):
            findings.append("selection.not_first_ready_task")

    return sorted(set(findings))


def validate_profile_contract_set(
    records: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    """Validate one activation/profile/envelope/provider/receipt chain."""

    required = {
        "activation_receipt",
        "execution_profile",
        "task_envelope",
        "provider_intent",
        "task_receipt",
        "activation_transition",
    }
    findings = [
        f"profile_contracts.missing:{name}"
        for name in sorted(required - set(records))
    ]
    if findings:
        return findings

    activation = records["activation_receipt"]
    profile = records["execution_profile"]
    envelope = records["task_envelope"]
    provider = records["provider_intent"]
    receipt = records["task_receipt"]
    transition = records["activation_transition"]

    activation_sha256 = _content_sha256(activation)
    profile_sha256 = _content_sha256(profile)
    topology = envelope["repository_topology_policy"]
    topology_sha256 = _content_sha256(topology)

    if activation.get("current_thread_verification_status") != "verified":
        findings.append("activation.current_thread_not_verified")
    if activation.get("reasoning_effort") != activation.get(
        "current_thread_requested_effort"
    ) or activation.get("reasoning_effort") != activation.get(
        "current_thread_effective_effort"
    ):
        findings.append("activation.current_thread_effort_mismatch")
    if profile.get("activation_receipt_sha256") != activation_sha256:
        findings.append("profile.activation_receipt_mismatch")
    if profile.get("activation_id") != activation.get("activation_id"):
        findings.append("profile.activation_id_mismatch")
    if profile.get("accepted_goal_sha256") != activation.get(
        "exact_activation_goal_sha256"
    ):
        findings.append("profile.goal_hash_mismatch")
    if profile.get("accepted_plan_sha256") != activation.get(
        "accepted_plan_sha256"
    ):
        findings.append("profile.plan_hash_mismatch")
    if profile.get("reasoning_effort") != activation.get("reasoning_effort"):
        findings.append("profile.reasoning_effort_mismatch")
    if profile.get("successor_inheritance_required") is not True:
        findings.append("profile.successor_inheritance_missing")

    if envelope.get("activation_receipt_sha256") != activation_sha256:
        findings.append("envelope.activation_receipt_stale")
    if envelope.get("execution_profile") != profile:
        findings.append("envelope.profile_mismatch")
    if envelope.get("plan_id") != activation.get("plan_id"):
        findings.append("envelope.plan_id_mismatch")
    if envelope.get("plan_sha256") != activation.get("accepted_plan_sha256"):
        findings.append("envelope.plan_hash_mismatch")
    if int(envelope.get("generation", 0)) < int(
        profile.get("effective_from_generation", 1)
    ):
        findings.append("envelope.profile_not_yet_effective")
    if envelope.get("repository_binding_sha256") != profile.get(
        "repository_binding_sha256"
    ):
        findings.append("envelope.repository_binding_mismatch")
    if topology_sha256 != profile.get("repository_topology_policy_sha256"):
        findings.append("envelope.topology_policy_hash_mismatch")
    default_topology = {
        "environment_mode": "reuse_bound_checkout",
        "branch_creation_authorized": False,
        "worktree_creation_authorized": False,
        "binding_change_authorized": False,
        "authorization_ref": None,
    }
    if topology != default_topology:
        findings.append("topology.default_deny_mismatch")

    if provider.get("execution_profile_sha256") != profile_sha256:
        findings.append("provider.execution_profile_mismatch")
    if provider.get("requested_reasoning_effort") != profile.get(
        "reasoning_effort"
    ):
        findings.append("provider.requested_effort_mismatch")
    if provider.get("status") == "returned" and provider.get(
        "effective_reasoning_effort"
    ) != provider.get("requested_reasoning_effort"):
        findings.append("provider.effective_effort_mismatch")
    if provider.get("profile_verification_status") == "verified" and not provider.get(
        "profile_evidence_ref"
    ):
        findings.append("provider.verified_evidence_missing")
    for field in ("plan_id", "plan_sha256", "task_id", "task_sha256", "generation"):
        if provider.get(field) != envelope.get(field):
            findings.append(f"provider.{field}_mismatch")
    if provider.get("environment_mode") != "reuse_bound_checkout":
        findings.append("provider.environment_mode_mismatch")
    if provider.get("repository_binding_sha256") != envelope.get(
        "repository_binding_sha256"
    ):
        findings.append("provider.repository_binding_mismatch")

    profile_evidence = receipt["activation_profile_evidence"]
    topology_evidence = receipt["topology_evidence"]
    if profile_evidence.get("activation_receipt_sha256") != activation_sha256:
        findings.append("receipt.activation_receipt_mismatch")
    if profile_evidence.get("execution_profile_sha256") != profile_sha256:
        findings.append("receipt.execution_profile_mismatch")
    if profile_evidence.get("requested_reasoning_effort") != profile.get(
        "reasoning_effort"
    ) or profile_evidence.get("observed_effective_reasoning_effort") != profile.get(
        "reasoning_effort"
    ):
        findings.append("receipt.reasoning_effort_mismatch")
    if receipt["plan_identity"].get("plan_id") != envelope.get("plan_id"):
        findings.append("receipt.plan_id_mismatch")
    if receipt["plan_identity"].get("plan_sha256") != envelope.get("plan_sha256"):
        findings.append("receipt.plan_hash_mismatch")
    if receipt["task_identity"].get("task_id") != envelope.get("task_id"):
        findings.append("receipt.task_id_mismatch")
    if receipt["task_identity"].get("task_sha256") != envelope.get("task_sha256"):
        findings.append("receipt.task_hash_mismatch")
    if receipt["relay_identity"].get("generation") != envelope.get("generation"):
        findings.append("receipt.generation_mismatch")
    if topology_evidence.get("repository_binding_sha256") != envelope.get(
        "repository_binding_sha256"
    ):
        findings.append("receipt.repository_binding_mismatch")
    if topology_evidence.get(
        "repository_topology_policy_sha256"
    ) != topology_sha256:
        findings.append("receipt.topology_policy_mismatch")

    if (
        transition.get("prior_selection_source") == "user_override"
        and transition.get("event") == "goal_edit"
        and (
            transition.get("next_selection_source") != "user_override"
            or transition.get("next_reasoning_effort")
            != transition.get("prior_reasoning_effort")
        )
    ):
        findings.append("activation.user_override_not_sticky")
    if transition.get("accepted_presentation_sequence") != transition.get(
        "latest_presentation_sequence"
    ):
        findings.append("activation.stale_combined_acceptance")

    return sorted(set(findings))
