"""Cross-record conformance checks for the portable control protocol."""

from __future__ import annotations

import fnmatch
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True, order=True)
class ConformanceIssue:
    """One stable semantic finding that cannot be expressed by one schema."""

    code: str
    record_id: str
    field: str
    message: str


ID_FIELDS = {
    "tasks": "task_id",
    "decisions": "decision_id",
    "jobs": "job_id",
    "roles": "execution_role_id",
    "completions": "completion_id",
    "handoffs": "handoff_id",
    "activations": "activation_id",
    "supersessions": "supersession_id",
    "goal_receipts": "receipt_id",
}


def canonical_json_bytes(value: Any) -> bytes:
    """Return the normalized JSON bytes used by activation hashes."""

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _record_payload(record: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if not key.startswith("_")}


def _path_allowed(path: str, patterns: Sequence[str]) -> bool:
    return any(path == pattern or fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def _add(
    issues: list[ConformanceIssue],
    code: str,
    record_id: str | None,
    field: str,
    message: str,
) -> None:
    issues.append(ConformanceIssue(code, record_id or "<missing-id>", field, message))


def _index_records(
    records: Mapping[str, Sequence[Mapping[str, Any]]], issues: list[ConformanceIssue]
) -> dict[str, dict[str, Mapping[str, Any]]]:
    indexes: dict[str, dict[str, Mapping[str, Any]]] = {}
    for kind, id_field in ID_FIELDS.items():
        index: dict[str, Mapping[str, Any]] = {}
        for record in records.get(kind, []):
            record_id = record.get(id_field)
            if not isinstance(record_id, str):
                _add(issues, "record.missing_id", None, id_field, f"{kind} record lacks {id_field}")
                continue
            if record_id in index:
                _add(issues, "record.duplicate_id", record_id, id_field, f"duplicate {kind} identifier")
            else:
                index[record_id] = record
        indexes[kind] = index
    return indexes


def _validate_primary_chain(
    indexes: Mapping[str, Mapping[str, Mapping[str, Any]]], issues: list[ConformanceIssue]
) -> None:
    tasks = indexes["tasks"]
    decisions = indexes["decisions"]
    jobs = indexes["jobs"]
    roles = indexes["roles"]

    for task_id, task in tasks.items():
        decision_id = task.get("current_decision_id")
        job_id = task.get("current_job_id")
        if decision_id is not None and decision_id not in decisions:
            _add(issues, "trace.task_decision_missing", task_id, "current_decision_id", str(decision_id))
        if job_id is not None and job_id not in jobs:
            _add(issues, "trace.task_job_missing", task_id, "current_job_id", str(job_id))

    for decision_id, decision in decisions.items():
        task_id = decision.get("task_id")
        if task_id not in tasks:
            _add(issues, "trace.decision_task_missing", decision_id, "task_id", str(task_id))
        selected = decision.get("selected", {})
        job_id = selected.get("agent_job_id") if isinstance(selected, Mapping) else None
        if job_id is not None:
            job = jobs.get(job_id)
            if job is None:
                _add(issues, "trace.decision_job_missing", decision_id, "selected.agent_job_id", str(job_id))
            elif job.get("decision_id") != decision_id:
                _add(issues, "trace.job_decision_conflict", job_id, "decision_id", "job does not point to selecting decision")

    active_roles_by_job: dict[str, list[str]] = {}
    for role_id, role in roles.items():
        job_id = role.get("job_id")
        job = jobs.get(str(job_id))
        if job is None:
            _add(issues, "trace.role_job_missing", role_id, "job_id", str(job_id))
            continue
        if role.get("task_id") != job.get("task_id"):
            _add(issues, "trace.role_task_conflict", role_id, "task_id", "role and job task IDs differ")
        active_roles_by_job.setdefault(str(job_id), []).append(role_id)

    for job_id, job in jobs.items():
        task_id = job.get("task_id")
        decision_id = job.get("decision_id")
        if task_id not in tasks:
            _add(issues, "trace.job_task_missing", job_id, "task_id", str(task_id))
        if decision_id not in decisions:
            _add(issues, "trace.job_decision_missing", job_id, "decision_id", str(decision_id))
        role_ids = active_roles_by_job.get(job_id, [])
        if len(role_ids) != 1:
            _add(issues, "trace.job_role_cardinality", job_id, "role_binding", f"expected one role, found {len(role_ids)}")
        elif job.get("role_binding", {}).get("role_id") != roles[role_ids[0]].get("role_id"):
            _add(issues, "trace.job_role_identity_conflict", job_id, "role_binding.role_id", "job and execution-role IDs differ")


def _validate_activation_hashes(
    indexes: Mapping[str, Mapping[str, Mapping[str, Any]]], issues: list[ConformanceIssue]
) -> None:
    by_path: dict[str, tuple[str, Mapping[str, Any]]] = {}
    for kind in ["tasks", "decisions", "jobs", "roles", "completions", "handoffs", "supersessions"]:
        for record_id, record in indexes[kind].items():
            source_path = record.get("_path")
            if isinstance(source_path, str):
                by_path[source_path] = (record_id, record)

    activated_ids: set[str] = set()
    for activation_id, activation in indexes["activations"].items():
        orders: list[int] = []
        for entry in activation.get("records", []):
            if not isinstance(entry, Mapping):
                continue
            record_id = entry.get("record_id")
            path = entry.get("path")
            orders.append(entry.get("order", -1))
            if record_id in activated_ids:
                _add(issues, "activation.record_reactivated", activation_id, "records", str(record_id))
            activated_ids.add(str(record_id))
            found = by_path.get(str(path))
            if found is None:
                _add(issues, "activation.path_missing", activation_id, "records.path", str(path))
                continue
            found_id, record = found
            if found_id != record_id:
                _add(issues, "activation.record_id_conflict", activation_id, "records.record_id", f"{record_id} != {found_id}")
            actual_hash = canonical_sha256(_record_payload(record))
            if actual_hash != entry.get("sha256"):
                _add(issues, "activation.hash_mismatch", activation_id, "records.sha256", str(record_id))
        if orders != list(range(1, len(orders) + 1)):
            _add(issues, "activation.order_invalid", activation_id, "records.order", "activation order must be contiguous from 1")

    for job_id, job in indexes["jobs"].items():
        if job.get("status") == "active" and job_id not in activated_ids:
            _add(issues, "activation.active_job_missing", job_id, "status", "active job has no activation manifest")


def _validate_supersession(
    indexes: Mapping[str, Mapping[str, Mapping[str, Any]]], issues: list[ConformanceIssue]
) -> None:
    jobs = indexes["jobs"]
    decisions = indexes["decisions"]
    graph: dict[str, str] = {}
    superseded_old: set[str] = set()
    for packet_id, packet in indexes["supersessions"].items():
        old_job = str(packet.get("old_job_id"))
        new_job = str(packet.get("replacement_job_id"))
        if old_job not in jobs:
            _add(issues, "supersession.old_job_missing", packet_id, "old_job_id", old_job)
        if new_job not in jobs:
            _add(issues, "supersession.new_job_missing", packet_id, "replacement_job_id", new_job)
        if packet.get("old_decision_id") not in decisions:
            _add(issues, "supersession.old_decision_missing", packet_id, "old_decision_id", str(packet.get("old_decision_id")))
        if packet.get("replacement_decision_id") not in decisions:
            _add(issues, "supersession.new_decision_missing", packet_id, "replacement_decision_id", str(packet.get("replacement_decision_id")))
        if old_job == new_job:
            _add(issues, "supersession.self_cycle", packet_id, "replacement_job_id", new_job)
        if old_job in superseded_old:
            _add(issues, "supersession.duplicate_old_job", packet_id, "old_job_id", old_job)
        superseded_old.add(old_job)
        graph[old_job] = new_job

    for start in graph:
        seen: set[str] = set()
        current = start
        while current in graph:
            if current in seen:
                _add(issues, "supersession.cycle", start, "replacement_job_id", current)
                break
            seen.add(current)
            current = graph[current]


def _validate_completions(
    indexes: Mapping[str, Mapping[str, Mapping[str, Any]]], issues: list[ConformanceIssue]
) -> None:
    jobs = indexes["jobs"]
    completion_by_job: dict[str, list[str]] = {}
    for completion_id, completion in indexes["completions"].items():
        job_id = str(completion.get("job_id"))
        completion_by_job.setdefault(job_id, []).append(completion_id)
        job = jobs.get(job_id)
        if job is None:
            _add(issues, "completion.job_missing", completion_id, "job_id", job_id)
            continue
        if completion.get("task_id") != job.get("task_id") or completion.get("decision_id") != job.get("decision_id"):
            _add(issues, "completion.trace_conflict", completion_id, "task_id", "completion trace differs from job")

        authority = job.get("authority", {})
        writable = list(authority.get("allowed_write_paths", [])) + list(authority.get("allowed_generated_paths", []))
        for path in completion.get("changed_paths", []):
            if not _path_allowed(path, writable):
                _add(issues, "completion.changed_path_forbidden", completion_id, "changed_paths", path)

        expected = {item.get("path") for item in job.get("expected_outputs", []) if isinstance(item, Mapping)}
        for output in completion.get("outputs", []):
            path = output.get("path") if isinstance(output, Mapping) else None
            if path not in expected:
                _add(issues, "completion.output_undeclared", completion_id, "outputs", str(path))

        approved_commands = {
            item.get("command_id")
            for item in job.get("commands", {}).get("approved", [])
            if isinstance(item, Mapping)
        }
        for result in completion.get("command_results", []):
            command_id = result.get("command_id") if isinstance(result, Mapping) else None
            if command_id not in approved_commands:
                _add(issues, "completion.command_undeclared", completion_id, "command_results", str(command_id))

        required_validators = {
            item.get("validator_id")
            for item in job.get("validators", {}).get("required", [])
            if isinstance(item, Mapping)
        }
        result_by_id = {
            item.get("validator_id"): item
            for item in completion.get("validator_results", [])
            if isinstance(item, Mapping)
        }
        for validator_id in required_validators:
            if validator_id not in result_by_id:
                _add(issues, "completion.validator_missing", completion_id, "validator_results", str(validator_id))
            elif completion.get("status") in {"completed", "completed_with_warnings"} and result_by_id[validator_id].get("status") == "fail":
                _add(issues, "completion.validator_failed_but_completed", completion_id, "validator_results", str(validator_id))

        allowed_claims = set(job.get("claim_boundary", {}).get("allowed", []))
        for conclusion in completion.get("claim_summary", {}).get("allowed_conclusions", []):
            if conclusion not in allowed_claims:
                _add(issues, "completion.claim_broadened", completion_id, "claim_summary.allowed_conclusions", conclusion)

    for job_id, completion_ids in completion_by_job.items():
        if len(completion_ids) > 1:
            _add(issues, "completion.duplicate_for_job", job_id, "completion_id", ",".join(sorted(completion_ids)))


def _validate_handoffs(
    indexes: Mapping[str, Mapping[str, Mapping[str, Any]]], issues: list[ConformanceIssue]
) -> None:
    for handoff_id, handoff in indexes["handoffs"].items():
        predecessor = handoff.get("predecessor", {})
        checks = [
            ("task_id", "tasks", "handoff.predecessor_task_missing"),
            ("decision_id", "decisions", "handoff.predecessor_decision_missing"),
            ("job_id", "jobs", "handoff.predecessor_job_missing"),
            ("completion_id", "completions", "handoff.predecessor_completion_missing"),
        ]
        for field, kind, code in checks:
            value = predecessor.get(field) if isinstance(predecessor, Mapping) else None
            if value not in indexes[kind]:
                _add(issues, code, handoff_id, f"predecessor.{field}", str(value))
        for predecessor_id in handoff.get("predecessor_handoff_ids", []):
            if predecessor_id not in indexes["handoffs"]:
                _add(issues, "handoff.chain_missing", handoff_id, "predecessor_handoff_ids", str(predecessor_id))
        if handoff.get("grants_execution_authority") is not False:
            _add(issues, "handoff.authority_grant_forbidden", handoff_id, "grants_execution_authority", "handoff cannot authorize execution")


def _validate_goal_receipts(
    indexes: Mapping[str, Mapping[str, Mapping[str, Any]]], issues: list[ConformanceIssue]
) -> None:
    unique: dict[tuple[str, int], str] = {}
    idempotency: dict[str, str] = {}
    for receipt_id, receipt in indexes["goal_receipts"].items():
        key = (str(receipt.get("goal_id")), int(receipt.get("generation", -1)))
        if key in unique:
            _add(issues, "goal_receipt.duplicate_generation", receipt_id, "generation", unique[key])
        unique[key] = receipt_id
        idem = str(receipt.get("idempotency_key"))
        if idem in idempotency:
            _add(issues, "goal_receipt.duplicate_idempotency_key", receipt_id, "idempotency_key", idempotency[idem])
        idempotency[idem] = receipt_id


def _validate_extensions(
    records: Mapping[str, Sequence[Mapping[str, Any]]],
    policies: Sequence[Mapping[str, Any]],
    strict_extensions: bool,
    issues: list[ConformanceIssue],
) -> None:
    declared: dict[str, Mapping[str, Any]] = {}
    for policy in policies:
        for namespace, declaration in policy.get("extension_schemas", {}).items():
            declared[namespace] = declaration
    if not strict_extensions:
        return
    for kind, values in records.items():
        id_field = ID_FIELDS.get(kind)
        for record in values:
            record_id = str(record.get(id_field, "<missing-id>")) if id_field else "<record>"
            for namespace, extension in record.get("extensions", {}).items():
                declaration = declared.get(namespace)
                if declaration is None:
                    _add(issues, "extension.namespace_undeclared", record_id, f"extensions.{namespace}", "strict mode requires a policy declaration")
                    continue
                if isinstance(extension, Mapping) and extension.get("version") != declaration.get("version"):
                    _add(issues, "extension.version_mismatch", record_id, f"extensions.{namespace}.version", str(extension.get("version")))


def validate_record_set(
    records: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    policies: Sequence[Mapping[str, Any]] = (),
    strict_extensions: bool = True,
) -> list[ConformanceIssue]:
    """Validate portable semantics spanning multiple immutable records.

    ``_path`` metadata may be attached to a record for activation-path lookup;
    keys beginning with ``_`` are excluded from canonical record hashing.
    """

    issues: list[ConformanceIssue] = []
    indexes = _index_records(records, issues)
    _validate_primary_chain(indexes, issues)
    _validate_activation_hashes(indexes, issues)
    _validate_supersession(indexes, issues)
    _validate_completions(indexes, issues)
    _validate_handoffs(indexes, issues)
    _validate_goal_receipts(indexes, issues)
    _validate_extensions(records, policies, strict_extensions, issues)
    return sorted(set(issues))
