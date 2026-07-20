"""Post-execution validation and checkpoint orchestration."""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass
from typing import Any, Callable, Mapping, Sequence

from agentjob_runtime.execution.compiler import CompiledAuthority, CompiledPath
from agentjob_runtime.execution.executor import ExecutionEvidence
from agentjob_runtime.errors import SecurityError
from agentjob_runtime.path_security import resolve_project_relative


ValidatorAdapter = Callable[[CompiledAuthority, ExecutionEvidence], Mapping[str, Any]]
CheckpointProvider = Callable[[Mapping[str, Any], ExecutionEvidence], Mapping[str, Any]]


@dataclass(frozen=True)
class PostExecutionReport:
    status: str
    reason_code: str
    job_id: str
    changed_paths: tuple[str, ...]
    outputs: tuple[Mapping[str, Any], ...]
    command_results: tuple[Mapping[str, Any], ...]
    validator_results: tuple[Mapping[str, Any], ...]
    checkpoint: Mapping[str, Any]
    proposed_claims: tuple[str, ...]
    domain_indeterminate: bool
    execution_performed: bool = True

    @property
    def successful(self) -> bool:
        return self.status == "passed"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path_is_allowed(
    authority: CompiledAuthority, relative: str, rules: Sequence[CompiledPath]
) -> bool:
    try:
        candidate, _ = resolve_project_relative(
            authority.project_root,
            relative,
            label="validation path",
            allow_directory_rule=False,
        )
    except SecurityError:
        return False
    if any(rule.contains(candidate) for rule in authority.forbidden_paths):
        return False
    return any(rule.contains(candidate) for rule in rules)


def _validation_result(
    validator_id: str,
    validator_class: str,
    status: str,
    *,
    reason_code: str | None = None,
    evidence_ref: str | None = None,
    notes: Sequence[str] = (),
) -> dict[str, Any]:
    return {
        "validator_id": validator_id,
        "validator_class": validator_class,
        "status": status,
        "reason_code": reason_code,
        "evidence_ref": evidence_ref,
        "notes": list(notes),
    }


def _changed_path_result(
    authority: CompiledAuthority, evidence: ExecutionEvidence
) -> dict[str, Any]:
    allowed = (*authority.allowed_write_paths, *authority.allowed_generated_paths)
    unexpected = [
        path for path in evidence.changed_paths if not _path_is_allowed(authority, path, allowed)
    ]
    return _validation_result(
        "changed-path-allowlist",
        "path_validation",
        "fail" if unexpected else "pass",
        reason_code="validation.changed_path_not_allowed" if unexpected else None,
        notes=[f"Unapproved changed path: {path}" for path in unexpected],
    )


def _command_result(
    authority: CompiledAuthority, evidence: ExecutionEvidence
) -> dict[str, Any]:
    actual = {item.command_id: item for item in evidence.command_results}
    approved = {item.command_id for item in authority.commands}
    unexpected = sorted(set(actual) - approved)
    missing = sorted(approved - set(actual))
    failed = sorted(
        command_id
        for command_id, item in actual.items()
        if command_id in approved and item.status != "pass"
    )
    notes = [f"Unapproved command result: {item}" for item in unexpected]
    notes.extend(f"Approved command was not run: {item}" for item in missing)
    notes.extend(f"Approved command did not pass: {item}" for item in failed)
    return _validation_result(
        "command-evidence-validator",
        "command_validation",
        "fail" if notes else "pass",
        reason_code="validation.command_evidence_invalid" if notes else None,
        notes=notes,
    )


def _claim_result(
    authority: CompiledAuthority, proposed_claims: Sequence[str]
) -> dict[str, Any]:
    allowed = set(authority.claim_boundary["allowed"])
    forbidden = set(authority.claim_boundary["forbidden"])
    overreach = sorted(set(proposed_claims) - allowed)
    explicit_forbidden = sorted(set(proposed_claims) & forbidden)
    notes = [f"Claim lacks exact boundary authority: {item}" for item in overreach]
    notes.extend(f"Claim is explicitly forbidden: {item}" for item in explicit_forbidden)
    return _validation_result(
        "claim-boundary-linter",
        "claim_validation",
        "fail" if notes else "pass",
        reason_code="validation.claim_boundary_exceeded" if notes else None,
        notes=notes,
    )


def _normalize_adapter_result(
    specification: Mapping[str, Any], value: Mapping[str, Any]
) -> dict[str, Any]:
    status = str(value.get("status", "indeterminate"))
    if status not in {"pass", "fail", "warning", "skipped", "indeterminate"}:
        status = "fail"
    return _validation_result(
        str(specification["validator_id"]),
        str(specification["validator_class"]),
        status,
        reason_code=str(value["reason_code"]) if value.get("reason_code") else None,
        evidence_ref=str(value["evidence_ref"]) if value.get("evidence_ref") else None,
        notes=tuple(str(item) for item in value.get("notes", ())),
    )


def _run_adapter(
    specification: Mapping[str, Any],
    adapter: ValidatorAdapter | None,
    authority: CompiledAuthority,
    evidence: ExecutionEvidence,
) -> dict[str, Any]:
    if adapter is None:
        return _validation_result(
            str(specification["validator_id"]),
            str(specification["validator_class"]),
            "fail" if specification["mode"] == "required" else "skipped",
            reason_code="validation.required_adapter_missing"
            if specification["mode"] == "required"
            else "validation.contextual_adapter_missing",
            notes=["No validator adapter was configured."],
        )
    try:
        value = adapter(authority, evidence)
    except Exception as error:  # A validator boundary must fail closed.
        return _validation_result(
            str(specification["validator_id"]),
            str(specification["validator_class"]),
            "fail",
            reason_code="validation.adapter_error",
            notes=[f"Validator adapter raised {type(error).__name__}."],
        )
    return _normalize_adapter_result(specification, value)


def _outputs(
    authority: CompiledAuthority, evidence: ExecutionEvidence
) -> tuple[tuple[dict[str, Any], ...], list[str]]:
    results: list[dict[str, Any]] = []
    findings: list[str] = []
    for expected in authority.expected_outputs:
        path = str(expected["path"])
        kind = str(expected["kind"])
        digest = evidence.after_files.get(path)
        if kind != "external_effect" and digest is None:
            findings.append(f"Expected output is missing: {path}")
        if kind == "controlled_source_change" and path not in evidence.changed_paths:
            findings.append(f"Expected controlled source did not change: {path}")
        results.append({"path": path, "kind": kind, "sha256": digest})
    return tuple(results), findings


def _checkpoint(
    authority: CompiledAuthority,
    evidence: ExecutionEvidence,
    provider: CheckpointProvider | None,
) -> tuple[dict[str, Any], list[str]]:
    specification = copy.deepcopy(dict(authority.checkpoint))
    if specification["provider"] == "none" and not specification["required"]:
        return {
            "provider": "none",
            "status": "not_required",
            "revision": None,
            "evidence_ref": None,
            "claims": [],
        }, []
    if provider is None:
        return {
            "provider": specification["provider"],
            "status": "fail",
            "revision": None,
            "evidence_ref": None,
            "claims": [],
        }, ["Required checkpoint provider is unavailable."]
    try:
        checkpoint = copy.deepcopy(dict(provider(specification, evidence)))
    except Exception as error:  # A checkpoint boundary must fail closed.
        return {
            "provider": specification["provider"],
            "status": "fail",
            "revision": None,
            "evidence_ref": None,
            "claims": [],
        }, [f"Checkpoint provider raised {type(error).__name__}."]
    checkpoint.setdefault("provider", specification["provider"])
    checkpoint.setdefault("status", "fail")
    checkpoint.setdefault("revision", None)
    checkpoint.setdefault("evidence_ref", None)
    checkpoint.setdefault("claims", [])
    findings = []
    if checkpoint["provider"] != specification["provider"]:
        findings.append("Checkpoint provider identity differs from AgentJob authority.")
    if checkpoint["status"] not in {"pass", "not_required"}:
        findings.append("Checkpoint provider did not report success.")
    allowed = set(authority.claim_boundary["allowed"])
    for claim in checkpoint.get("claims", []):
        if claim not in allowed:
            findings.append(f"Checkpoint claim lacks exact boundary authority: {claim}")
    return checkpoint, findings


def validate_execution(
    *,
    authority: CompiledAuthority,
    evidence: ExecutionEvidence,
    validator_adapters: Mapping[str, ValidatorAdapter] | None = None,
    checkpoint_provider: CheckpointProvider | None = None,
    proposed_claims: Sequence[str] = (),
) -> PostExecutionReport:
    """Validate direct evidence without finalizing a completion record."""

    if evidence.job_id != authority.job_id or not evidence.execution_performed:
        raise ValueError("execution evidence does not identify the compiled AgentJob")
    adapters = dict(validator_adapters or {})
    path_result = _changed_path_result(authority, evidence)
    command_result = _command_result(authority, evidence)
    claim_result = _claim_result(authority, proposed_claims)
    builtins = {
        "changed-path-allowlist": path_result,
        "command-evidence-validator": command_result,
        "claim-boundary-linter": claim_result,
    }
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    required_ids: set[str] = set()
    for specification in (*authority.required_validators, *authority.contextual_validators):
        validator_id = str(specification["validator_id"])
        if specification["mode"] == "required":
            required_ids.add(validator_id)
        result = copy.deepcopy(builtins.get(validator_id))
        if result is None:
            result = _run_adapter(
                specification,
                adapters.get(validator_id),
                authority,
                evidence,
            )
        results.append(result)
        seen.add(validator_id)
    for validator_id, result in builtins.items():
        if validator_id not in seen:
            results.append(copy.deepcopy(result))
            required_ids.add(validator_id)
    outputs, output_findings = _outputs(authority, evidence)
    checkpoint, checkpoint_findings = _checkpoint(authority, evidence, checkpoint_provider)
    required_failures = [
        item
        for item in results
        if item["validator_id"] in required_ids and item["status"] in {"fail", "skipped"}
    ]
    domain_indeterminate = any(
        item["validator_class"] == "domain_validation"
        and item["validator_id"] in required_ids
        and item["status"] == "indeterminate"
        for item in results
    )
    command_results = tuple(
        {
            "command_id": item.command_id,
            "exit_code": item.exit_code,
            "status": "pass" if item.status == "pass" else "fail",
            "evidence_ref": None,
        }
        for item in evidence.command_results
    )
    if checkpoint_findings:
        status = "checkpoint_failed"
        reason_code = "validation.checkpoint_failed"
    elif output_findings or required_failures:
        status = "validation_failed"
        reason_code = "validation.required_check_failed"
    elif domain_indeterminate:
        status = "domain_indeterminate"
        reason_code = "validation.domain_indeterminate"
    else:
        status = "passed"
        reason_code = "validation.passed"
    if output_findings:
        results.append(
            _validation_result(
                "expected-output-validator",
                "process_validation",
                "fail",
                reason_code="validation.expected_output_invalid",
                notes=output_findings,
            )
        )
    if checkpoint_findings:
        results.append(
            _validation_result(
                "checkpoint-validator",
                "process_validation",
                "fail",
                reason_code="validation.checkpoint_failed",
                notes=checkpoint_findings,
            )
        )
    return PostExecutionReport(
        status,
        reason_code,
        authority.job_id,
        evidence.changed_paths,
        outputs,
        command_results,
        tuple(results),
        checkpoint,
        tuple(proposed_claims),
        domain_indeterminate,
    )
