"""Direct semantic verification for one returned implementation-plan task."""

from __future__ import annotations

import copy
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from agentjob_runtime.errors import AgentJobControlError
from agentjob_runtime.path_security import alias_key, normalize_relative_path
from agentjob_runtime.records.canonical import canonical_json_bytes
from agentjob_runtime.security import contains_secret


_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_VALIDATOR_CLASSES = frozenset(
    {
        "schema_validation",
        "path_validation",
        "dependency_validation",
        "trace_validation",
        "process_validation",
        "control_validation",
        "command_validation",
        "claim_validation",
        "domain_validation",
        "human_authority",
    }
)
_VALIDATOR_STATUSES = frozenset(
    {"pass", "fail", "warning", "skipped", "indeterminate"}
)
_APPROVAL_STATUSES = frozenset(
    {
        "approved",
        "not_required",
        "missing",
        "rejected",
        "expired",
        "stale",
        "unknown",
    }
)
_PROTECTED_EFFECT_STATUSES = frozenset(
    {"not_attempted", "authorized", "completed", "blocked", "unknown"}
)
_DIRECT_VERIFIER_ID = "plan-task-direct-verifier"
_DIRECT_VERIFIER_REF = (
    "skills/agentjob-control/scripts/agentjob_runtime/plan/verify.py"
)


@dataclass(frozen=True)
class PlanTaskVerification:
    """Verified result and the existing lifecycle guard it requires."""

    disposition: str
    reason_code: str
    guard_reason: str | None
    findings: tuple[str, ...]
    result: Mapping[str, Any] = field(repr=False, compare=False)


def _valid_id(value: Any) -> bool:
    return (
        isinstance(value, str)
        and 3 <= len(value) <= 160
        and _ID_PATTERN.fullmatch(value) is not None
    )


def _normalize_evidence_path(
    value: Any,
    *,
    finding: str,
    findings: set[str],
) -> str | None:
    if not isinstance(value, str):
        findings.add(finding)
        return None
    try:
        return normalize_relative_path(
            value,
            label="plan task evidence path",
            allow_directory_rule=False,
        ).relative
    except AgentJobControlError:
        findings.add(finding)
        return None


def _normalize_changed_paths(
    value: Any,
    *,
    finding_prefix: str,
    findings: set[str],
) -> list[str]:
    if not isinstance(value, list):
        findings.add(f"{finding_prefix}.invalid_list")
        return []
    result: list[str] = []
    aliases: set[str] = set()
    for item in value:
        normalized = _normalize_evidence_path(
            item,
            finding=f"{finding_prefix}.invalid_path",
            findings=findings,
        )
        if normalized is None:
            continue
        identity = alias_key(
            normalize_relative_path(
                normalized,
                allow_directory_rule=False,
            )
        )
        if identity in aliases:
            findings.add(f"{finding_prefix}.duplicate_path")
            continue
        aliases.add(identity)
        result.append(normalized)
    return result


def _path_allowed(
    path: str,
    *,
    allowed_rules: Sequence[str],
    forbidden_rules: Sequence[str],
) -> bool:
    candidate = normalize_relative_path(
        path,
        label="observed changed path",
        allow_directory_rule=False,
    )

    def contains(rule_value: str) -> bool:
        rule = normalize_relative_path(
            rule_value,
            label="compiled authority path",
        )
        return candidate.base_relative == rule.base_relative or (
            rule.directory_rule
            and candidate.base_relative.startswith(
                rule.base_relative + "/"
            )
        )

    return any(contains(rule) for rule in allowed_rules) and not any(
        contains(rule) for rule in forbidden_rules
    )


def _string_list(
    value: Any,
    *,
    finding: str,
    findings: set[str],
) -> list[str]:
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        findings.add(finding)
        return []
    return list(value)


def _acceptance_results(
    value: Any,
    *,
    expected: Sequence[str],
    scope_findings: set[str],
    validation_findings: set[str],
) -> list[dict[str, Any]]:
    entries = value if isinstance(value, list) else []
    if not isinstance(value, list):
        validation_findings.add("acceptance.invalid_list")
    by_criterion: dict[str, list[Mapping[str, Any]]] = {}
    for item in entries:
        if not isinstance(item, Mapping):
            validation_findings.add("acceptance.invalid_entry")
            continue
        criterion = item.get("criterion")
        if not isinstance(criterion, str) or not criterion:
            validation_findings.add("acceptance.invalid_criterion")
            continue
        by_criterion.setdefault(criterion, []).append(item)
    expected_set = set(expected)
    if set(by_criterion) - expected_set:
        scope_findings.add("acceptance.out_of_scope_criterion")
    normalized: list[dict[str, Any]] = []
    for criterion in expected:
        candidates = by_criterion.get(criterion, [])
        if len(candidates) != 1:
            validation_findings.add(
                "acceptance.missing_or_duplicate_criterion"
            )
            normalized.append(
                {
                    "criterion": criterion,
                    "status": "fail",
                    "evidence_refs": [],
                }
            )
            continue
        candidate = candidates[0]
        status = candidate.get("status")
        refs_value = candidate.get("evidence_refs")
        refs_findings: set[str] = set()
        refs = [
            normalized_ref
            for ref in refs_value
            if (
                normalized_ref := _normalize_evidence_path(
                    ref,
                    finding="acceptance.invalid_evidence_ref",
                    findings=refs_findings,
                )
            )
            is not None
        ] if isinstance(refs_value, list) else []
        if not isinstance(refs_value, list) or len(set(refs)) != len(refs):
            refs_findings.add("acceptance.invalid_evidence_refs")
        if status not in {"pass", "fail", "indeterminate"}:
            status = "fail"
            validation_findings.add("acceptance.invalid_status")
        if refs_findings or status == "pass" and not refs:
            status = "fail"
            validation_findings.update(refs_findings)
            validation_findings.add("acceptance.pass_without_evidence")
        if status != "pass":
            validation_findings.add("acceptance.not_passed")
        normalized.append(
            {
                "criterion": criterion,
                "status": status,
                "evidence_refs": refs,
            }
        )
    return normalized


def _validator_results(
    value: Any,
    *,
    required: Mapping[str, Mapping[str, str]],
    validation_findings: set[str],
) -> list[dict[str, Any]]:
    entries = value if isinstance(value, list) else []
    if not isinstance(value, list):
        validation_findings.add("validator.invalid_list")
    normalized: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    for item in entries:
        if not isinstance(item, Mapping):
            validation_findings.add("validator.invalid_entry")
            continue
        validator_id = item.get("validator_id")
        validator_class = item.get("validator_class")
        status = item.get("status")
        if (
            not _valid_id(validator_id)
            or validator_class not in _VALIDATOR_CLASSES
            or status not in _VALIDATOR_STATUSES
        ):
            validation_findings.add("validator.invalid_entry")
            continue
        if validator_id == _DIRECT_VERIFIER_ID or validator_id in by_id:
            validation_findings.add("validator.duplicate_or_reserved_id")
            continue
        evidence_findings: set[str] = set()
        evidence_ref = item.get("evidence_ref")
        if evidence_ref is not None:
            evidence_ref = _normalize_evidence_path(
                evidence_ref,
                finding="validator.invalid_evidence_ref",
                findings=evidence_findings,
            )
        reason_code = item.get("reason_code")
        if reason_code is not None and not isinstance(reason_code, str):
            reason_code = "plan.validation_failed"
            evidence_findings.add("validator.invalid_reason_code")
        notes = _string_list(
            item.get("notes", []),
            finding="validator.invalid_notes",
            findings=evidence_findings,
        )
        validation_findings.update(evidence_findings)
        normalized_item = {
            "validator_id": validator_id,
            "validator_class": validator_class,
            "status": status,
            "reason_code": reason_code,
            "evidence_ref": evidence_ref,
            "notes": notes,
        }
        normalized.append(normalized_item)
        by_id[validator_id] = normalized_item
    for validator_id, specification in required.items():
        result = by_id.get(validator_id)
        if result is None:
            validation_findings.add("validator.required_missing")
            normalized.append(
                {
                    "validator_id": validator_id,
                    "validator_class": specification["validator_class"],
                    "status": "fail",
                    "reason_code": "plan.validation_failed",
                    "evidence_ref": None,
                    "notes": ["Required validator evidence is missing."],
                }
            )
            continue
        if (
            result["status"] != "pass"
            or result["validator_class"]
            != specification["validator_class"]
            or result["evidence_ref"]
            != specification["validation_ref"]
        ):
            validation_findings.add(
                "validator.required_result_mismatch"
            )
    if any(
        item["status"] in {"fail", "skipped", "indeterminate"}
        for item in normalized
    ):
        validation_findings.add("validator.nonpassing_result")
    return normalized


def _checkpoint(
    value: Any,
    *,
    expected: Mapping[str, Any],
    checkpoint_findings: set[str],
) -> dict[str, Any]:
    candidate = dict(value) if isinstance(value, Mapping) else {}
    if not isinstance(value, Mapping):
        checkpoint_findings.add("checkpoint.invalid_mapping")
    provider = candidate.get("provider")
    status = candidate.get("status")
    revision = candidate.get("revision")
    evidence_ref = candidate.get("evidence_ref")
    if not _valid_id(provider):
        provider = str(expected.get("provider") or "none")
        checkpoint_findings.add("checkpoint.invalid_provider")
    if status not in {"pass", "fail", "not_required", "unknown"}:
        status = "fail"
        checkpoint_findings.add("checkpoint.invalid_status")
    if revision is not None and not isinstance(revision, str):
        revision = None
        checkpoint_findings.add("checkpoint.invalid_revision")
    if evidence_ref is not None:
        evidence_ref = _normalize_evidence_path(
            evidence_ref,
            finding="checkpoint.invalid_evidence_ref",
            findings=checkpoint_findings,
        )
    expected_provider = expected.get("provider")
    required = expected.get("required") is True
    if provider != expected_provider:
        checkpoint_findings.add("checkpoint.provider_mismatch")
    if required and status != "pass":
        checkpoint_findings.add("checkpoint.required_not_passed")
    if not required and expected_provider == "none" and (
        status != "not_required"
        or revision is not None
        or evidence_ref is not None
    ):
        checkpoint_findings.add("checkpoint.not_required_mismatch")
    return {
        "provider": provider,
        "status": status,
        "revision": revision,
        "evidence_ref": evidence_ref,
    }


def _approvals_and_effects(
    direct: Mapping[str, Any],
    *,
    allowed_effects: set[str],
    allowed_approval_refs: set[str],
    human_findings: set[str],
    scope_findings: set[str],
    validation_findings: set[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    approvals: list[dict[str, Any]] = []
    approval_value = direct.get("approvals")
    if not isinstance(approval_value, list):
        validation_findings.add("approval.invalid_list")
    else:
        for item in approval_value:
            if (
                not isinstance(item, Mapping)
                or not isinstance(item.get("action"), str)
                or not item.get("action")
                or item.get("status") not in _APPROVAL_STATUSES
            ):
                validation_findings.add("approval.invalid_entry")
                continue
            evidence_ref = item.get("evidence_ref")
            if evidence_ref is not None:
                evidence_ref = _normalize_evidence_path(
                    evidence_ref,
                    finding="approval.invalid_evidence_ref",
                    findings=validation_findings,
                )
            approval_id = item.get("approval_id")
            if approval_id is not None and not _valid_id(approval_id):
                approval_id = None
                validation_findings.add("approval.invalid_id")
            normalized = {
                "approval_id": approval_id,
                "action": item["action"],
                "status": item["status"],
                "evidence_ref": evidence_ref,
            }
            approvals.append(normalized)
            if normalized["status"] in {
                "missing",
                "rejected",
                "expired",
                "stale",
                "unknown",
            }:
                human_findings.add("approval.unresolved")

    effects: list[dict[str, Any]] = []
    effect_value = direct.get("protected_effects")
    if not isinstance(effect_value, list):
        validation_findings.add("protected_effect.invalid_list")
    else:
        for item in effect_value:
            if (
                not isinstance(item, Mapping)
                or not isinstance(item.get("effect"), str)
                or not item.get("effect")
                or item.get("status") not in _PROTECTED_EFFECT_STATUSES
            ):
                validation_findings.add(
                    "protected_effect.invalid_entry"
                )
                continue
            evidence_ref = item.get("evidence_ref")
            if evidence_ref is not None:
                evidence_ref = _normalize_evidence_path(
                    evidence_ref,
                    finding="protected_effect.invalid_evidence_ref",
                    findings=validation_findings,
                )
            approval_id = item.get("approval_id")
            if approval_id is not None and not _valid_id(approval_id):
                approval_id = None
                validation_findings.add("protected_effect.invalid_approval")
            normalized = {
                "effect": item["effect"],
                "status": item["status"],
                "approval_id": approval_id,
                "evidence_ref": evidence_ref,
            }
            effects.append(normalized)
            if normalized["status"] in {"blocked", "unknown"}:
                human_findings.add("protected_effect.unresolved")
            if (
                normalized["status"] in {"authorized", "completed"}
                and normalized["effect"] not in allowed_effects
            ):
                scope_findings.add(
                    "protected_effect.outside_authority"
                )
            if (
                normalized["status"] in {"authorized", "completed"}
                and normalized["approval_id"] is None
            ):
                human_findings.add(
                    "protected_effect.approval_missing"
                )
            if (
                normalized["status"] in {"authorized", "completed"}
                and normalized["approval_id"] is not None
                and normalized["approval_id"] not in allowed_approval_refs
            ):
                scope_findings.add(
                    "protected_effect.approval_outside_authority"
                )
    return approvals, effects


def verify_plan_task_result(
    *,
    plan_record: Mapping[str, Any],
    task_definition: Mapping[str, Any],
    compiled_invocation: Mapping[str, Any],
    result: Mapping[str, Any],
    fingerprint_before: str,
    observed_repository_topology_before: Mapping[str, Any],
    direct_observation: Mapping[str, Any] | None,
    observation_findings: Sequence[str] = (),
) -> PlanTaskVerification:
    """Bind one known return to exact authority and direct observations."""

    value = copy.deepcopy(dict(result))
    invocation = copy.deepcopy(dict(compiled_invocation))
    direct = copy.deepcopy(dict(value["direct_evidence"]))
    observation = (
        copy.deepcopy(dict(direct_observation))
        if isinstance(direct_observation, Mapping)
        else {}
    )
    repository_findings = set(observation_findings)
    scope_findings: set[str] = set()
    human_findings: set[str] = set()
    checkpoint_findings: set[str] = set()
    validation_findings: set[str] = set()
    if not isinstance(direct_observation, Mapping):
        repository_findings.add("observation.invalid_mapping")
    try:
        serialized_observation = canonical_json_bytes(
            observation
        ).decode("utf-8")
    except (TypeError, ValueError):
        repository_findings.add("observation.not_canonical_json")
    else:
        if contains_secret(serialized_observation):
            repository_findings.add("observation.secret_detected")

    packet = invocation["authority_packet"]
    decision = packet["decision"]
    job = packet["agent_job"]
    task_id = str(invocation["task_id"])
    if value.get("task_id") != task_id:
        scope_findings.add("identity.task_mismatch")
    if value.get("decision_id") != decision["decision_id"]:
        scope_findings.add("identity.decision_mismatch")
    if value["agentjobs"] == 0:
        if value.get("agent_job_id") is not None:
            scope_findings.add("identity.unexecuted_agentjob_present")
        if value.get("completion_id") is not None:
            scope_findings.add("identity.unexecuted_completion_present")
        value["agent_job_id"] = None
        value["completion_id"] = None
    else:
        if value.get("agent_job_id") != job["job_id"]:
            scope_findings.add("identity.agentjob_mismatch")
        if value.get("completion_id") != f"AJC-{job['job_id']}":
            scope_findings.add("identity.completion_mismatch")
        value["zero_job_reason"] = None
    if value.get("handoff_id") is not None:
        scope_findings.add("identity.handoff_forbidden")
    if value.get("global_goal_evaluation") == "met":
        scope_findings.add("scope.global_completion_claim")

    repository = plan_record["repository_binding"]
    if value["starting_revision"] != repository["starting_revision"]:
        repository_findings.add("repository.starting_revision_mismatch")
    if value["pre_topology"] != observed_repository_topology_before:
        repository_findings.add("repository.pre_topology_mismatch")
    if observation.get("ending_revision") != value["ending_revision"]:
        repository_findings.add("repository.ending_revision_mismatch")
    if observation.get("fingerprint_after") != value["fingerprint_after"]:
        repository_findings.add("repository.fingerprint_mismatch")
    if observation.get("post_topology") != value["post_topology"]:
        repository_findings.add("repository.post_topology_mismatch")
    if not isinstance(fingerprint_before, str) or len(
        fingerprint_before
    ) != 64:
        repository_findings.add("repository.fingerprint_before_invalid")

    observed_paths = _normalize_changed_paths(
        observation.get("changed_paths"),
        finding_prefix="observation.changed_paths",
        findings=repository_findings,
    )
    reported_paths = _normalize_changed_paths(
        direct.get("changed_paths"),
        finding_prefix="evidence.changed_paths",
        findings=scope_findings,
    )
    if sorted(observed_paths) != sorted(reported_paths):
        repository_findings.add("repository.changed_paths_mismatch")
    authority = job["authority"]
    allowed_rules = [
        *authority["allowed_write_paths"],
        *authority["allowed_generated_paths"],
    ]
    for path in observed_paths:
        try:
            allowed = _path_allowed(
                path,
                allowed_rules=allowed_rules,
                forbidden_rules=authority["forbidden_paths"],
            )
        except AgentJobControlError:
            allowed = False
        if not allowed:
            scope_findings.add("scope.changed_path_not_allowed")
    other_task_ids = {
        str(item["task_id"])
        for item in plan_record["state"]["tasks"]
        if item["task_id"] != task_id
    }
    if any(
        other_task_id in path
        for path in observed_paths
        for other_task_id in other_task_ids
    ):
        scope_findings.add("scope.later_task_path")

    acceptance = _acceptance_results(
        direct.get("acceptance_results"),
        expected=task_definition["acceptance_criteria"],
        scope_findings=scope_findings,
        validation_findings=validation_findings,
    )
    required_validators: dict[str, dict[str, str]] = {}
    required_by_id = {
        item["validator_id"]: item
        for item in job["validators"]["required"]
    }
    for mapping in invocation["execution_mapping"]["validators"]:
        specification = required_by_id[mapping["validator_id"]]
        required_validators[mapping["validator_id"]] = {
            "validation_ref": mapping["validation_ref"],
            "validator_class": specification["validator_class"],
        }
    validators = _validator_results(
        direct.get("validator_results"),
        required=required_validators,
        validation_findings=validation_findings,
    )
    checkpoint = _checkpoint(
        direct.get("checkpoint"),
        expected=job["checkpoint"],
        checkpoint_findings=checkpoint_findings,
    )
    approvals, protected_effects = _approvals_and_effects(
        direct,
        allowed_effects=set(authority["external_effects"]),
        allowed_approval_refs=set(
            invocation["execution_mapping"].get(
                "external_effect_authority_refs", []
            )
        ),
        human_findings=human_findings,
        scope_findings=scope_findings,
        validation_findings=validation_findings,
    )
    warnings = _string_list(
        direct.get("warnings"),
        finding="evidence.invalid_warnings",
        findings=validation_findings,
    )
    indeterminate_checks = _string_list(
        direct.get("indeterminate_checks"),
        finding="evidence.invalid_indeterminate_checks",
        findings=validation_findings,
    )
    if indeterminate_checks:
        validation_findings.add("evidence.indeterminate_checks")
    if direct.get("plan_completion") is not None:
        scope_findings.add("scope.plan_completion_forbidden")
    coordinator = value.get("coordinator_action")
    if (
        isinstance(coordinator, Mapping)
        and coordinator.get("next_task_id") is not None
    ):
        scope_findings.add("scope.later_task_dispatch")
    if value.get("human_gate_outstanding") is True:
        human_findings.add("approval.outstanding_gate")
    if human_findings and not any(
        item["status"]
        in {"missing", "rejected", "expired", "stale", "unknown"}
        for item in approvals
    ):
        approvals.append(
            {
                "approval_id": None,
                "action": "Resolve the declared human gate.",
                "status": "missing",
                "evidence_ref": None,
            }
        )

    if repository_findings:
        disposition = "blocked"
        reason_code = "plan.repository_mismatch"
        guard_reason = "repository"
        terminal_reason = (
            "Direct task verification detected repository evidence mismatch."
        )
    elif scope_findings:
        disposition = "validation_failed"
        reason_code = "plan_task.scope_violation"
        guard_reason = "validation"
        terminal_reason = (
            "Direct task verification detected exact-task scope leakage."
        )
    elif human_findings:
        disposition = "human_gate_required"
        reason_code = "plan.human_gate_required"
        guard_reason = "human_gate"
        terminal_reason = (
            "Direct task verification detected unresolved human authority."
        )
    elif checkpoint_findings:
        disposition = "validation_failed"
        reason_code = "validation.checkpoint_failed"
        guard_reason = "checkpoint"
        terminal_reason = (
            "Direct task verification detected checkpoint failure."
        )
    elif validation_findings:
        disposition = "validation_failed"
        reason_code = "plan.validation_failed"
        guard_reason = "validation"
        terminal_reason = (
            "Direct task verification detected required evidence failure."
        )
    else:
        disposition = "task_complete"
        reason_code = str(value["reason_code"])
        guard_reason = None
        terminal_reason = None
        if not _valid_id(reason_code):
            disposition = "validation_failed"
            reason_code = "plan.validation_failed"
            guard_reason = "validation"
            terminal_reason = (
                "Direct task verification detected an invalid reason code."
            )
            validation_findings.add("result.invalid_reason_code")

    findings = tuple(
        sorted(
            repository_findings
            | scope_findings
            | human_findings
            | checkpoint_findings
            | validation_findings
        )
    )
    validators.append(
        {
            "validator_id": _DIRECT_VERIFIER_ID,
            "validator_class": "control_validation",
            "status": "pass" if not findings else "fail",
            "reason_code": None if not findings else reason_code,
            "evidence_ref": _DIRECT_VERIFIER_REF,
            "notes": list(findings),
        }
    )
    value["direct_evidence"] = {
        "changed_paths": observed_paths,
        "acceptance_results": acceptance,
        "validator_results": validators,
        "checkpoint": checkpoint,
        "approvals": approvals,
        "protected_effects": protected_effects,
        "warnings": warnings,
        "indeterminate_checks": indeterminate_checks,
        "plan_completion": None,
    }
    value["disposition"] = disposition
    value["reason_code"] = reason_code
    value["terminal_reason"] = terminal_reason
    value["recovery"] = {
        "status": "not_required",
        "action_ref": None,
    }
    value["replanning"] = {
        "status": "not_required",
        "action_ref": None,
    }
    value["coordinator_action"] = {
        "kind": (
            "dispatch_next_task"
            if disposition == "task_complete"
            else "protected_stop"
        ),
        "next_task_id": None,
    }
    return PlanTaskVerification(
        disposition,
        reason_code,
        guard_reason,
        findings,
        value,
    )
