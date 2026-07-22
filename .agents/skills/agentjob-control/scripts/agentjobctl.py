#!/usr/bin/env python3
"""Portable AgentJob control command-line interface."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
import stat
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime import PACKAGE_VERSION, PROTOCOL_VERSION
from agentjob_runtime.adapters.thread_auto import (
    inspect_thread_provider,
    select_thread_provider,
)
from agentjob_runtime.adapters.thread_manual import ManualThreadProvider
from agentjob_runtime.config import LoadedConfig, load_config, resolve_project_path
from agentjob_runtime.control.activation import _format_cross_issues, _record_set, activate_packet
from agentjob_runtime.control.completion import write_completion
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.handoff import write_handoff
from agentjob_runtime.control.indexes import generate_indexes
from agentjob_runtime.control.resolver import resolve_store
from agentjob_runtime.control.supersession import supersede_packet
from agentjob_runtime.errors import (
    AgentJobControlError,
    BootstrapRequired,
    RecordNotFound,
    RecordValidationError,
    SecurityError,
    StateConflict,
)
from agentjob_runtime.fingerprinting.canonical import FingerprintResult
from agentjob_runtime.goal.decide import decide_generation
from agentjob_runtime.goal.completion_report import render_completion_markdown
from agentjob_runtime.goal.continuous import (
    accept_and_run as accept_and_run_goal,
    advance_once as advance_goal_once,
    preparation_from_mapping as goal_preparation_from_mapping,
    prepare_goal_activation,
)
from agentjob_runtime.goal.execution import (
    claim_generation,
    consume_invocation,
    record_invocation_returned,
    record_invocation_unknown,
)
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.model import fingerprint_status
from agentjob_runtime.goal.recovery import (
    abandon_unconsumed,
    adopt_successor,
    amend_completion_contract,
    amend_guards,
    begin_recovery,
    cancel_relay,
    reconcile_consumed,
    resume_relay,
)
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_successor, reserve_successor
from agentjob_runtime.goal.verify import verify_generation
from agentjob_runtime.plan.initialize import initialize_plan
from agentjob_runtime.plan.continuous import (
    ContinuousPreparation,
    accept_continuous_activation,
    advance_once as advance_plan_once,
    answer_and_resume,
    prepare_continuous_activation,
    run_to_goal as run_plan_to_goal,
    validate_execution_authority,
    validate_question_batch,
)
from agentjob_runtime.plan.launcher import (
    PlanLauncherGuards,
    PlanSourceRequest,
    dispatch_reserved_plan_task,
    preflight_plan_launcher,
    reserve_first_plan_task,
)
from agentjob_runtime.plan.normalize import (
    PrdToImplementationPlanAdapter,
    normalize_plan_preflight,
)
from agentjob_runtime.plan.sqlite_store import SQLitePlanStore
from agentjob_runtime.records.canonical import content_sha256, load_structured
from agentjob_runtime.validation.cross_record import validate_record_set


SECRET_KEY = re.compile(r"(?:secret|token|password|private.?key|authorization|credential)", re.I)
SECRET_VALUE = re.compile(r"(?:sk-[A-Za-z0-9_-]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")


def redact(value: Any, *, key: str = "") -> Any:
    if SECRET_KEY.search(key):
        return "<redacted>"
    if isinstance(value, Mapping):
        return {item_key: redact(item, key=str(item_key)) for item_key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return [redact(item) for item in value]
    if isinstance(value, str) and SECRET_VALUE.search(value):
        return "<redacted>"
    return value


def emit(value: Mapping[str, Any], *, as_json: bool) -> None:
    safe = redact(value)
    if as_json:
        print(json.dumps(safe, sort_keys=True, ensure_ascii=False))
        return
    status = safe.get("status", "unknown")
    code = safe.get("code") or safe.get("reason_code")
    print(f"status: {status}" + (f" ({code})" if code else ""))
    for key, item in safe.items():
        if key in {"status", "code", "reason_code"}:
            continue
        if isinstance(item, (dict, list)):
            print(f"{key}: {json.dumps(item, sort_keys=True, ensure_ascii=False)}")
        else:
            print(f"{key}: {item}")


def context(args: argparse.Namespace, *, require_ready: bool = False) -> tuple[LoadedConfig, FilesystemControlStore]:
    loaded = load_config(args.project_root, config_path=args.config)
    if require_ready and loaded.capabilities.status != "ready":
        raise BootstrapRequired(
            "required project capabilities are unavailable",
            details=loaded.capabilities.as_dict(),
        )
    store = FilesystemControlStore(loaded.project_root, loaded.control_root)
    return loaded, store


def load_mapping(path: str) -> dict[str, Any]:
    value = load_structured(path)
    if not isinstance(value, dict):
        raise RecordValidationError(f"record file must contain a mapping: {path}")
    return value


def load_policies(loaded: LoadedConfig) -> list[dict[str, Any]]:
    policies: list[dict[str, Any]] = []
    for relative in loaded.data["policy"]["packs"]:
        path = loaded.project_root / relative
        if path.is_file():
            policies.append(load_mapping(str(path)))
    return policies


def command_doctor(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args)
    findings: list[dict[str, str]] = []
    if not store.root.exists():
        findings.append({"severity": "warning", "code": "control.root_missing", "message": str(store.root)})
    else:
        try:
            drift = generate_indexes(store, check=True)
            for path in drift.drifted:
                findings.append({"severity": "warning", "code": "index.drift", "message": path})
        except AgentJobControlError as error:
            findings.append({"severity": "failure", "code": error.code, "message": str(error)})
    for capability in loaded.capabilities.capabilities:
        if not capability.available:
            findings.append(
                {
                    "severity": "failure" if capability.required else "warning",
                    "code": capability.reason_code or "capability.unavailable",
                    "message": f"{capability.capability_id}: {capability.provider}",
                }
            )
    hard_failures = [item for item in findings if item["severity"] == "failure"]
    return {
        "status": "pass" if not hard_failures else "fail",
        "protocol_version": PROTOCOL_VERSION,
        "package_version": PACKAGE_VERSION,
        "profile": loaded.data["control"]["profile"],
        "capabilities": loaded.capabilities.as_dict(),
        "control_root": str(store.root),
        "local_state_root": str(loaded.local_state_root),
        "findings": findings,
        "execution_performed": False,
    }


def command_validate(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args)
    schema_counts: dict[str, int] = {}
    for kind, _, record in store.iter_records():
        store.validate_record(kind, record)
        schema_counts[kind] = schema_counts.get(kind, 0) + 1
    records = _record_set(store, [])
    issues = validate_record_set(
        records,
        policies=load_policies(loaded),
        strict_extensions=bool(loaded.data["policy"]["strict_extensions"]),
    )
    if issues:
        raise RecordValidationError(
            "control records failed cross-record validation",
            details={"findings": _format_cross_issues(issues)},
        )
    return {
        "status": "pass",
        "schema_counts": schema_counts,
        "cross_record_findings": [],
        "execution_performed": False,
    }


def command_resolve(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args)
    result = resolve_store(store, capabilities=loaded.capabilities, task_id=args.task_id)
    return {"status": "pass", **result.as_dict()}


def command_status(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args)
    boundary = resolve_store(store, capabilities=loaded.capabilities, task_id=args.task_id)
    records = list(store.iter_records())
    latest: dict[str, Any] = {}
    id_fields = {
        "task": "task_id",
        "director_decision": "decision_id",
        "agent_job": "job_id",
        "execution_role": "execution_role_id",
        "completion": "completion_id",
        "handoff": "handoff_id",
    }
    for kind, _, record in records:
        if kind in id_fields:
            latest[kind] = record.get(id_fields[kind])
    return {
        "status": "ready" if loaded.capabilities.status == "ready" else "bootstrap_required",
        "protocol_version": PROTOCOL_VERSION,
        "profile": loaded.data["control"]["profile"],
        "capabilities": loaded.capabilities.as_dict(),
        "latest_records": latest,
        "resolver": boundary.as_dict(),
        "repository_binding": {"project_root": str(loaded.project_root)},
        "execution_performed": False,
    }


def command_fingerprint(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args)
    record_rows = [
        {
            "kind": kind,
            "path": store.relative(path),
            "sha256": content_sha256(record),
        }
        for kind, path, record in store.iter_records()
    ]
    boundary = resolve_store(store, capabilities=loaded.capabilities, task_id=args.task_id)
    payload = {
        "project_root": str(loaded.project_root),
        "config_sha256": content_sha256(loaded.data),
        "records": sorted(record_rows, key=lambda item: (item["kind"], item["path"])),
        "resolver": {"boundary": boundary.boundary, "reason_code": boundary.reason_code},
    }
    return {"status": "pass", "fingerprint": content_sha256(payload), "payload": payload, "execution_performed": False}


def command_activate(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args, require_ready=True)
    receipt = activate_packet(
        store,
        task_id=args.task_id,
        decision=load_mapping(args.decision),
        job=load_mapping(args.job),
        execution_role=load_mapping(args.role),
        expected_revision=args.expected_revision,
        policies=load_policies(loaded),
    )
    return receipt.as_dict()


def command_supersede(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args, require_ready=True)
    receipt = supersede_packet(
        store,
        task_id=args.task_id,
        old_decision_id=args.old_decision_id,
        old_job_id=args.old_job_id,
        replacement_decision=load_mapping(args.decision),
        replacement_job=load_mapping(args.job),
        replacement_role=load_mapping(args.role),
        reason=args.reason,
        evidence_refs=args.evidence_ref,
        prior_execution_status=args.prior_execution_status,
        working_evidence_handling=args.working_evidence_handling,
        expected_revision=args.expected_revision,
        created_at=args.created_at,
        policies=load_policies(loaded),
    )
    return receipt.as_dict()


def command_complete(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args, require_ready=True)
    receipt = write_completion(
        store,
        load_mapping(args.completion),
        expected_revision=args.expected_revision,
        close_task=args.close_task,
        next_recommended_action=args.next_action,
        policies=load_policies(loaded),
    )
    return receipt.as_dict()


def command_handoff(args: argparse.Namespace) -> dict[str, Any]:
    loaded, store = context(args, require_ready=True)
    receipt = write_handoff(
        store,
        load_mapping(args.handoff),
        expected_revision=args.expected_revision,
        policies=load_policies(loaded),
    )
    return receipt.as_dict()


def _goal_store(args: argparse.Namespace, *, read_only: bool = False) -> tuple[LoadedConfig, SQLiteGoalStore]:
    try:
        loaded = load_config(args.project_root, config_path=args.config)
    except BootstrapRequired:
        if not getattr(args, "state_db", None):
            raise
        root = Path(args.project_root).expanduser().resolve()
        supplied = Path(args.state_db)
        path = (
            supplied.expanduser().resolve()
            if supplied.is_absolute()
            else (root / supplied).resolve()
        )
        try:
            path.relative_to(root)
        except ValueError as error:
            raise SecurityError(
                "goal state database must remain inside the explicit project root"
            ) from error
        if read_only and not path.is_file():
            raise RecordNotFound(f"goal state database does not exist: {path}")
        return None, SQLiteGoalStore(
            path,
            auto_migrate=not read_only,
            read_only=read_only,
        )
    if loaded.data["goal_relay"]["state_backend"] != "sqlite":
        raise BootstrapRequired(
            "goal CLI currently requires the configured SQLite state backend",
            details={"missing_capabilities": ["sys4ai.goal-relay-state.sqlite.v1"]},
        )
    if getattr(args, "state_db", None):
        path = resolve_project_path(
            loaded.project_root,
            args.state_db,
            purpose="goal state database",
            reject_install_roots=True,
        )
    else:
        path = loaded.local_state_root / "goal-state.sqlite3"
    if read_only and not path.is_file():
        raise RecordNotFound(f"goal state database does not exist: {path}")
    return loaded, SQLiteGoalStore(
        path,
        auto_migrate=not read_only,
        read_only=read_only,
    )


def _goal_summary(record: Mapping[str, Any]) -> dict[str, Any]:
    lease = record["state"].get("active_lease")
    generations = [
        {
            "generation": entry["generation"],
            "phase": entry["phase"],
            "invocation_state": entry["invocation_state"],
            "invocation_consumed": entry["invocation_consumed"],
            "successor_thread_id": entry["successor_thread_id"],
            "receipt_finalized": entry["finalized_receipt_hash"] is not None,
        }
        for _, entry in sorted(record["generations"].items(), key=lambda item: int(item[0]))
    ]
    result = {
        "status": "pass",
        "goal_id": record["goal_id"],
        "goal_sha256": record["goal_sha256"],
        "completion_contract_sha256": record["completion_contract_sha256"],
        "revision": record["state"]["revision"],
        "phase": record["state"]["phase"],
        "current_generation": record["state"]["current_generation"],
        "passes_consumed": record["state"]["passes_consumed"],
        "goal_evaluation": record["state"]["goal_evaluation"],
        "terminal_reason": record["state"]["terminal_reason"],
        "lease_holder_kind": lease["holder_kind"] if lease else None,
        "generations": generations,
        "execution_performed": False,
    }
    if record.get("schema_version") in {
        "sys4ai.continue-goal.v3",
        "sys4ai.continue-goal.v4",
    }:
        result.update(
            {
                "reasoning_effort": record["execution_profile"][
                    "reasoning_effort"
                ],
                "repository_environment_mode": record[
                    "repository_topology_policy"
                ]["environment_mode"],
                "human_necessity_report_id": (
                    record["human_intervention"]["report_id"]
                    if record.get("human_intervention")
                    else None
                ),
                "completion_report_id": (
                    record["completion_report"]["report_id"]
                    if record.get("completion_report")
                    else None
                ),
            }
        )
    if record.get("schema_version") == "sys4ai.continue-goal.v4":
        granted_ids = {
            item["grant_id"]
            for item in record["question_response"]["grants"]
            if item["granted"] is True
        }
        consumed_ids = {
            item["grant_id"] for item in record["grant_consumptions"]
        }
        result.update(
            {
                "coordinator_status": record["coordinator"]["status"],
                "coordinator_thread_id": record["coordinator"]["thread_id"],
                "current_worker_thread_id": record["coordinator"][
                    "current_worker_thread_id"
                ],
                "question_batch_id": record["question_batch"]["batch_id"],
                "execution_authority_id": record["execution_authority"][
                    "authority_id"
                ],
                "available_grant_ids": [
                    item["grant_id"]
                    for item in record["execution_authority"]["requested_grants"]
                    if item["grant_id"] in granted_ids
                    and item["grant_id"] not in consumed_ids
                ],
                "continue_required": False,
            }
        )
    return result


def _read_text_argument(args: argparse.Namespace) -> str:
    if bool(args.goal_text) == bool(args.goal_text_file):
        raise RecordValidationError("provide exactly one of --goal-text or --goal-text-file")
    if args.goal_text_file:
        return Path(args.goal_text_file).read_text(encoding="utf-8")
    return str(args.goal_text)


def _read_secret_file(path_value: str) -> str:
    path = Path(path_value).expanduser().resolve()
    if not path.is_file() or path.is_symlink():
        raise SecurityError("token file must be one regular non-symlink file")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise SecurityError("token file has an unsafe alias")
    value = path.read_text(encoding="utf-8").strip()
    if len(value) < 32:
        raise RecordValidationError("token file must contain at least 32 characters")
    return value


def command_goal_initialize(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = initialize_goal(
        store,
        goal_text=_read_text_argument(args),
        completion_contract=load_mapping(args.completion_contract),
        guards=load_structured(args.guards) if args.guards else None,
        repository_binding=load_mapping(args.repository_binding),
        initial_fingerprint=args.initial_fingerprint,
        authorization={
            "fresh_recursive_threads_explicitly_requested": bool(
                args.fresh_recursive_threads_explicitly_requested
            )
        },
        activation_receipt=load_mapping(args.activation_receipt),
        runtime_binding=load_mapping(args.runtime_binding)
        if args.runtime_binding
        else None,
        repository_topology_policy=load_mapping(
            args.repository_topology_policy
        )
        if args.repository_topology_policy
        else None,
        goal_id=args.goal_id,
        timestamp=args.timestamp,
        launcher_token=_read_secret_file(args.launcher_token_file)
        if args.launcher_token_file
        else None,
    )
    return _goal_summary(record)


def command_goal_status(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args, read_only=True)
    if args.goal_id:
        return _goal_summary(store.load_goal(args.goal_id))
    return {"status": "pass", "goals": store.list_goals(), "execution_performed": False}


def command_goal_export(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args, read_only=True)
    records = (
        [store.load_goal(args.goal_id)]
        if args.goal_id
        else [store.load_goal(item["goal_id"]) for item in store.list_goals()]
    )
    return {
        "status": "pass",
        "schema_version": "sys4ai.goal-export.v1",
        "goals": records,
        "execution_performed": False,
    }


def command_goal_completion_summary(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args, read_only=True)
    record = store.load_goal(args.goal_id)
    report = record.get("completion_report")
    if not isinstance(report, Mapping):
        raise RecordNotFound(
            f"goal has no canonical completion report: {args.goal_id}"
        )
    return {
        "status": "pass",
        "goal_id": args.goal_id,
        "completion_report": dict(report),
        "markdown": render_completion_markdown(report),
        "execution_performed": False,
    }


def command_goal_reserve(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = reserve_successor(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        current_holder_token=_read_secret_file(args.holder_token_file),
        predecessor_thread_id=args.predecessor_thread_id,
        handoff_token=_read_secret_file(args.handoff_token_file)
        if args.handoff_token_file
        else None,
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_record_successor(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = record_successor(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        handoff_token=_read_secret_file(args.handoff_token_file),
        successor_thread_id=args.successor_thread_id,
        provider_id=args.provider_id,
        provider_response=load_mapping(args.provider_response),
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_claim(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = claim_generation(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        handoff_token=_read_secret_file(args.handoff_token_file),
        idempotency_key=args.idempotency_key,
        successor_thread_id=args.successor_thread_id,
        claim_token=_read_secret_file(args.claim_token_file)
        if args.claim_token_file
        else None,
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_consume(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = consume_invocation(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        claim_token=_read_secret_file(args.claim_token_file),
        observations=load_mapping(args.observations) if args.observations else None,
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_returned(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = record_invocation_returned(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        claim_token=_read_secret_file(args.claim_token_file),
        continue_result=load_mapping(args.continue_result),
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_unknown(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = record_invocation_unknown(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        claim_token=_read_secret_file(args.claim_token_file),
        diagnostic=load_mapping(args.diagnostic),
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_verify(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    result = load_mapping(args.continue_result)
    current = store.load_goal(args.goal_id)
    after_hash = str(result["repository_fingerprint_after"])
    after = FingerprintResult(
        {"continue_result_sha256": content_sha256(result)},
        after_hash,
        fingerprint_status(current["state"]["canonical_fingerprint_history"], after_hash),
    )
    record = verify_generation(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        claim_token=_read_secret_file(args.claim_token_file),
        continue_result=result,
        after_fingerprint=after,
        direct_evidence=load_mapping(args.direct_evidence),
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_decide(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = decide_generation(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        claim_token=_read_secret_file(args.claim_token_file),
        legal_route_available=args.legal_route_available,
        explicit_stop_reason=args.explicit_stop_reason,
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_recover(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    evidence = load_mapping(args.evidence)
    common = {
        "store": store,
        "goal_id": args.goal_id,
        "expected_revision": args.expected_revision,
        "user_authorization": args.user_authorization,
        "timestamp": args.timestamp,
    }
    if args.action == "begin":
        record = begin_recovery(evidence=evidence, **common)
    elif args.action == "adopt":
        if args.generation is None or not args.successor_thread_id:
            raise RecordValidationError("recovery adopt requires generation and successor thread ID")
        record = adopt_successor(
            generation=args.generation,
            successor_thread_id=args.successor_thread_id,
            uniqueness_evidence=evidence,
            **common,
        )
    elif args.action == "resume":
        record = resume_relay(evidence=evidence, **common)
    elif args.action == "abandon":
        if args.generation is None:
            raise RecordValidationError("recovery abandon requires generation")
        record = abandon_unconsumed(
            generation=args.generation,
            terminal_holder_proof=evidence,
            **common,
        )
    else:
        if args.generation is None or not args.canonical_evidence or not args.decision:
            raise RecordValidationError(
                "recovery reconcile requires generation, canonical evidence, and decision"
            )
        record = reconcile_consumed(
            generation=args.generation,
            terminal_holder_proof=evidence,
            canonical_evidence=load_mapping(args.canonical_evidence),
            returned_proven=args.returned_proven,
            decision=args.decision,
            **common,
        )
    return _goal_summary(record)


def command_goal_amend_contract(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = amend_completion_contract(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        user_authorization=args.user_authorization,
        evidence=load_mapping(args.evidence),
        new_contract=load_mapping(args.completion_contract),
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_amend_guards(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = amend_guards(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        user_authorization=args.user_authorization,
        evidence=load_mapping(args.evidence),
        new_guards=load_mapping(args.guards),
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def command_goal_cancel(args: argparse.Namespace) -> dict[str, Any]:
    _, store = _goal_store(args)
    record = cancel_relay(
        store,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        user_authorization=args.user_authorization,
        evidence=load_mapping(args.evidence),
        timestamp=args.timestamp,
    )
    return _goal_summary(record)


def _protected_project_file(
    project_root: str | Path,
    path_value: str,
    *,
    purpose: str,
    require_private_mode: bool = False,
) -> Path:
    root = Path(project_root).expanduser().resolve()
    if not root.is_dir():
        raise RecordValidationError(
            "plan-goal project root must be an existing directory",
            details={"reason_code": "plan.repository_mismatch"},
        )
    path = resolve_project_path(root, path_value, purpose=purpose)
    if not path.is_file() or path.is_symlink():
        raise SecurityError(
            f"{purpose} must be one project-contained regular non-symlink file",
            details={"reason_code": "security.blocked", "path": path_value},
        )
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise SecurityError(
            f"{purpose} has an unsafe filesystem alias",
            details={"reason_code": "path.hardlink", "path": path_value},
        )
    if (
        require_private_mode
        and sys.platform != "win32"
        and stat.S_IMODE(info.st_mode) & 0o077
    ):
        raise SecurityError(
            f"{purpose} must not grant group or other permissions",
            details={
                "reason_code": "security.file_permissions",
                "path": path_value,
                "mode": oct(stat.S_IMODE(info.st_mode)),
            },
        )
    return path


def _load_protected_mapping(
    project_root: str | Path,
    path_value: str,
    *,
    purpose: str,
) -> dict[str, Any]:
    path = _protected_project_file(
        project_root,
        path_value,
        purpose=purpose,
    )
    value = load_structured(path)
    if not isinstance(value, dict):
        raise RecordValidationError(
            f"{purpose} must contain one mapping",
            details={"reason_code": "plan.validation_failed", "path": path_value},
        )
    return value


def _read_protected_text(
    project_root: str | Path,
    path_value: str,
    *,
    purpose: str,
) -> str:
    path = _protected_project_file(
        project_root,
        path_value,
        purpose=purpose,
    )
    value = path.read_text(encoding="utf-8").strip()
    if not value:
        raise RecordValidationError(
            f"{purpose} must contain nonblank UTF-8 text",
            details={"reason_code": "plan.validation_failed", "path": path_value},
        )
    return value


def _read_protected_secret(
    project_root: str | Path,
    path_value: str,
    *,
    purpose: str,
) -> str:
    path = _protected_project_file(
        project_root,
        path_value,
        purpose=purpose,
        require_private_mode=True,
    )
    value = path.read_text(encoding="utf-8").strip()
    if len(value) < 32:
        raise RecordValidationError(
            f"{purpose} must contain at least 32 characters",
            details={"reason_code": "plan.validation_failed", "path": path_value},
        )
    return value


def _implementation_plan_skill_root() -> Path:
    root = Path(__file__).resolve().parents[2] / "implementation-plan-goal"
    required = (
        root / "scripts" / "planctl.py",
        root / "schemas" / "implementation-plan.schema.json",
        root / "schemas" / "normalization-report.schema.json",
    )
    missing = [
        path.relative_to(root).as_posix()
        for path in required
        if not path.is_file()
    ]
    if missing:
        raise BootstrapRequired(
            "plan-goal initialize requires its installed implementation-plan-goal dependency",
            details={
                "reason_code": "plan_task.capability_missing",
                "missing": missing,
                "execution_performed": False,
            },
        )
    return root


def _load_plan_normalizer(plan_skill_root: Path):
    script = plan_skill_root / "scripts" / "planctl.py"
    spec = importlib.util.spec_from_file_location(
        "_sys4ai_implementation_plan_goal_planctl",
        script,
    )
    if spec is None or spec.loader is None:
        raise BootstrapRequired(
            "plan-goal normalizer module is unavailable",
            details={
                "reason_code": "plan_task.capability_missing",
                "missing": ["prd-to-implementation-plan"],
                "execution_performed": False,
            },
        )
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ImportError as error:
        raise BootstrapRequired(
            "plan-goal normalizer dependencies are unavailable",
            details={
                "reason_code": "plan_task.capability_missing",
                "missing": ["prd-to-implementation-plan"],
                "execution_performed": False,
            },
        ) from error
    normalizer = getattr(module, "normalize_paths", None)
    if not callable(normalizer):
        raise BootstrapRequired(
            "plan-goal normalizer callable is unavailable",
            details={
                "reason_code": "plan_task.capability_missing",
                "missing": ["prd-to-implementation-plan"],
                "execution_performed": False,
            },
        )
    return normalizer


def _plan_source_requests(
    project_root: str | Path,
    manifest_path: str,
) -> tuple[PlanSourceRequest, ...]:
    manifest = _load_protected_mapping(
        project_root,
        manifest_path,
        purpose="plan source manifest",
    )
    entries = manifest.get("sources")
    if not isinstance(entries, list) or not entries:
        raise RecordValidationError(
            "plan source manifest requires a nonempty sources list",
            details={"reason_code": "plan.authority_missing"},
        )
    requests: list[PlanSourceRequest] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            raise RecordValidationError(
                "plan source manifest entries must be mappings",
                details={
                    "reason_code": "plan.validation_failed",
                    "source_index": index,
                },
            )
        path = entry.get("path")
        authority = entry.get("authority")
        precedence = entry.get("precedence")
        if (
            not isinstance(path, str)
            or not path.strip()
            or not isinstance(authority, str)
            or not authority.strip()
            or (
                precedence is not None
                and (
                    isinstance(precedence, bool)
                    or not isinstance(precedence, int)
                )
            )
        ):
            raise RecordValidationError(
                "plan source manifest contains an invalid source declaration",
                details={
                    "reason_code": "plan.validation_failed",
                    "source_index": index,
                },
            )
        requests.append(
            PlanSourceRequest(
                path=path,
                authority=authority,
                precedence=precedence,
            )
        )
    return tuple(requests)


def _plan_dispatch_reason_code(status: str) -> str:
    return {
        "dispatched": "plan.worker_dispatched",
        "manual_handoff_pending": "plan.manual_handoff_pending",
        "dispatch_failed": "plan.provider_failed",
        "ambiguous": "plan.provider_ambiguous",
        "timeout": "plan.provider_timeout",
        "duplicate": "plan.provider_duplicate",
    }.get(status, "plan.launcher_completed")


def _plan_state_path(args: argparse.Namespace) -> tuple[Path, Path]:
    root = Path(args.project_root).expanduser().resolve()
    if not root.is_dir():
        raise RecordValidationError(
            "plan-goal project root must be an existing directory",
            details={"reason_code": "plan.repository_mismatch"},
        )
    state_path = resolve_project_path(
        root,
        args.state_db,
        purpose="plan-goal state database",
        reject_install_roots=True,
    )
    return root, state_path


def _load_project_thread_provider(
    project_root: Path,
    adapter_path: str,
) -> Any:
    path = _protected_project_file(
        project_root,
        adapter_path,
        purpose="ThreadProvider adapter",
    )
    spec = importlib.util.spec_from_file_location(
        "_sys4ai_project_thread_provider",
        path,
    )
    if spec is None or spec.loader is None:
        raise BootstrapRequired(
            "configured ThreadProvider adapter cannot be loaded",
            details={"reason_code": "thread_provider.adapter_unavailable"},
        )
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise BootstrapRequired(
            "configured ThreadProvider adapter failed to load",
            details={
                "reason_code": "thread_provider.adapter_unavailable",
                "error_type": type(exc).__name__,
            },
        ) from exc
    factory = getattr(module, "build_thread_provider", None)
    if not callable(factory):
        raise BootstrapRequired(
            "ThreadProvider adapter must expose build_thread_provider(project_root=...)",
            details={"reason_code": "thread_provider.adapter_unavailable"},
        )
    provider = factory(project_root=project_root)
    inspect_thread_provider(provider)
    return provider


def _continuous_provider(args: argparse.Namespace, root: Path) -> Any:
    provider = _load_project_thread_provider(root, args.provider_adapter)
    selected = select_thread_provider(
        configured_provider=str(provider.provider_id),
        strategy=args.thread_strategy,
        providers=[provider],
        require_continuous=True,
    )
    return selected


def _load_goal_setup_adapter(project_root: Path, adapter_path: str) -> Any:
    path = _protected_project_file(
        project_root,
        adapter_path,
        purpose="goal setup adapter",
    )
    spec = importlib.util.spec_from_file_location(
        "_sys4ai_project_goal_setup_adapter",
        path,
    )
    if spec is None or spec.loader is None:
        raise BootstrapRequired(
            "configured goal setup adapter cannot be loaded",
            details={"reason_code": "goal.setup_adapter_unavailable"},
        )
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise BootstrapRequired(
            "configured goal setup adapter failed to load",
            details={
                "reason_code": "goal.setup_adapter_unavailable",
                "error_type": type(exc).__name__,
            },
        ) from exc
    required = (
        "apply_goal_setup",
        "observe_goal_repository",
        "fingerprint_goal_repository",
    )
    missing = [name for name in required if not callable(getattr(module, name, None))]
    if missing:
        raise BootstrapRequired(
            "goal setup adapter lacks required callables",
            details={
                "reason_code": "goal.setup_adapter_unavailable",
                "missing": missing,
            },
        )
    return module


def command_goal_prepare(args: argparse.Namespace) -> dict[str, Any]:
    """Perform the complete read-only v4 intake and emit one prompt."""

    root = Path(args.project_root).expanduser().resolve()
    if not root.is_dir():
        raise RecordValidationError("goal project root must be an existing directory")
    proposal = _load_protected_mapping(
        root,
        args.proposal,
        purpose="verified goal activation proposal",
    )
    completion_contract = _load_protected_mapping(
        root,
        args.completion_contract,
        purpose="goal completion contract",
    )
    repository_binding = _load_protected_mapping(
        root,
        args.repository_binding,
        purpose="goal repository binding",
    )
    repository_observation = _load_protected_mapping(
        root,
        args.repository_observation,
        purpose="goal repository observation",
    )
    provider_capabilities = _load_protected_mapping(
        root,
        args.provider_capabilities,
        purpose="ThreadProvider capability report",
    )
    intake_inventory = _load_protected_mapping(
        root,
        args.intake_inventory,
        purpose="complete goal intake inventory",
    )
    question_manifest = (
        _load_protected_mapping(
            root,
            args.questions,
            purpose="declared goal questions",
        )
        if args.questions
        else {"questions": []}
    )
    grant_manifest = (
        _load_protected_mapping(
            root,
            args.grants,
            purpose="declared protected goal actions",
        )
        if args.grants
        else {"grants": []}
    )
    questions = question_manifest.get("questions")
    grants = grant_manifest.get("grants")
    if not isinstance(questions, list) or not isinstance(grants, list):
        raise RecordValidationError(
            "question and grant manifests must contain list values"
        )
    preparation = prepare_goal_activation(
        proposal,
        completion_contract=completion_contract,
        repository_binding=repository_binding,
        repository_observation=repository_observation,
        initial_fingerprint=args.initial_fingerprint,
        provider_capabilities=provider_capabilities,
        intake_inventory=intake_inventory,
        questions=questions,
        requested_grants=grants,
        timestamp=args.timestamp,
    )
    return preparation.as_dict()


def command_goal_accept_and_run(args: argparse.Namespace) -> dict[str, Any]:
    """Accept the complete v4 intake once and remain active to canonical met."""

    root = Path(args.project_root).expanduser().resolve()
    preparation = goal_preparation_from_mapping(
        _load_protected_mapping(
            root,
            args.preparation,
            purpose="continuous goal preparation",
        )
    )
    provider = _continuous_provider(args, root)
    response_input = (
        _load_protected_mapping(
            root,
            args.response,
            purpose="consolidated goal response",
        )
        if args.response
        else {"answers": {}, "grants": {}}
    )
    answers = response_input.get("answers", {})
    grants = response_input.get("grants", {})
    if not isinstance(answers, Mapping) or not isinstance(grants, Mapping):
        raise RecordValidationError(
            "consolidated response requires answers and grants mappings"
        )
    acceptance_message = (
        _read_protected_text(
            root,
            args.acceptance_message_file,
            purpose="combined goal acceptance message",
        )
        if args.acceptance_message_file
        else args.acceptance_message
    )
    setup_executor = None
    repository_observer = None
    fingerprint_provider = None
    if args.setup_adapter:
        adapter = _load_goal_setup_adapter(root, args.setup_adapter)
        setup_executor = lambda grant: adapter.apply_goal_setup(
            project_root=root,
            grant=grant,
        )
        repository_observer = lambda: adapter.observe_goal_repository(
            project_root=root
        )
        fingerprint_provider = lambda: adapter.fingerprint_goal_repository(
            project_root=root
        )
    else:
        if not args.repository_observation or not args.initial_fingerprint:
            raise RecordValidationError(
                "accept-and-run requires live --repository-observation and "
                "--initial-fingerprint when no setup adapter is used"
            )
        live_observation = _load_protected_mapping(
            root,
            args.repository_observation,
            purpose="live goal repository observation",
        )
        repository_observer = lambda: copy.deepcopy(live_observation)
        fingerprint_provider = lambda: str(args.initial_fingerprint)
    _, store = _goal_store(args)
    return accept_and_run_goal(
        store,
        preparation=preparation,
        acceptance_message=str(acceptance_message),
        acceptance_evidence_ref=args.acceptance_evidence_ref,
        answers=answers,
        grants=grants,
        provider=provider,
        setup_executor=setup_executor,
        repository_observer=repository_observer,
        fingerprint_provider=fingerprint_provider,
        guards=load_structured(args.guards) if args.guards else None,
        runtime_binding=(
            _load_protected_mapping(
                root,
                args.runtime_binding,
                purpose="goal runtime binding",
            )
            if args.runtime_binding
            else None
        ),
        goal_id=args.goal_id,
        timestamp=args.timestamp,
    )


def command_goal_advance(args: argparse.Namespace) -> dict[str, Any]:
    """Run one idempotent internal v4 coordinator boundary."""

    root = Path(args.project_root).expanduser().resolve()
    provider = _continuous_provider(args, root)
    _, store = _goal_store(args)
    return advance_goal_once(
        store,
        goal_id=args.goal_id,
        provider=provider,
        timestamp=args.timestamp,
    ).as_dict()


def _preparation_from_mapping(value: Mapping[str, Any]) -> ContinuousPreparation:
    required = {
        "proposal",
        "plan",
        "question_batch",
        "execution_authority",
        "prompt",
        "status",
    }
    if set(value) != required:
        raise RecordValidationError(
            "continuous preparation has missing or unknown fields"
        )
    batch = validate_question_batch(value["question_batch"])
    authority = validate_execution_authority(value["execution_authority"])
    if (
        value["status"] not in {"confirmation_required", "suspended_safeguard"}
        or not isinstance(value["prompt"], str)
        or not value["prompt"].strip()
        or value["proposal"].get("state") != "presented"
        or value["proposal"].get("accepted_plan_sha256")
        != batch["accepted_plan_sha256"]
        or authority["accepted_plan_sha256"]
        != batch["accepted_plan_sha256"]
        or authority["accepted_plan_revision"]
        != batch["accepted_plan_revision"]
    ):
        raise RecordValidationError(
            "continuous preparation bindings are inconsistent"
        )
    return ContinuousPreparation(
        proposal=copy.deepcopy(dict(value["proposal"])),
        plan=copy.deepcopy(dict(value["plan"])),
        question_batch=batch,
        execution_authority=authority,
        prompt=str(value["prompt"]),
        status=str(value["status"]),
    )


def command_plan_goal_prepare(args: argparse.Namespace) -> dict[str, Any]:
    """Run deterministic read-only intake and return one complete prompt."""

    root = Path(args.project_root).expanduser().resolve()
    plan_skill_root = _implementation_plan_skill_root()
    proposal = _load_protected_mapping(
        root,
        args.proposal,
        purpose="verified plan activation proposal",
    )
    plan = _load_protected_mapping(
        root,
        args.plan,
        purpose="accepted implementation plan",
    )
    repository_observation = _load_protected_mapping(
        root,
        args.repository_observation,
        purpose="plan repository observation",
    )
    capabilities = _load_protected_mapping(
        root,
        args.provider_capabilities,
        purpose="ThreadProvider capability report",
    )
    effects_record = (
        _load_protected_mapping(
            root,
            args.effects,
            purpose="declared protected effects",
        )
        if args.effects
        else {"effects": []}
    )
    questions_record = (
        _load_protected_mapping(
            root,
            args.questions,
            purpose="declared plan questions",
        )
        if args.questions
        else {"questions": []}
    )
    effects = effects_record.get("effects")
    questions = questions_record.get("questions")
    if not isinstance(effects, list) or not isinstance(questions, list):
        raise RecordValidationError(
            "effects and questions manifests must contain list values"
        )
    preparation = prepare_continuous_activation(
        proposal,
        plan=plan,
        plan_schema_path=(
            plan_skill_root / "schemas" / "implementation-plan.schema.json"
        ),
        repository_observation=repository_observation,
        provider_capabilities=capabilities,
        plan_revision=args.plan_revision,
        requested_effects=effects,
        questions=questions,
        timestamp=args.timestamp,
    )
    return preparation.as_dict()


def command_plan_goal_accept_and_run(args: argparse.Namespace) -> dict[str, Any]:
    """Atomically accept prepared authority, initialize, and enter the loop."""

    root, state_path = _plan_state_path(args)
    plan_skill_root = _implementation_plan_skill_root()
    preparation = _preparation_from_mapping(
        _load_protected_mapping(
            root,
            args.preparation,
            purpose="continuous plan preparation",
        )
    )
    if preparation.status != "confirmation_required":
        raise BootstrapRequired(
            "continuous preparation safeguards are not resolved",
            details={
                "reason_code": "plan.continuous_safeguard",
                "safeguards": preparation.question_batch["safeguards"],
            },
        )
    provider = _continuous_provider(args, root)
    if provider.provider_id != preparation.proposal["provider_id"]:
        raise StateConflict(
            "live ThreadProvider differs from the confirmed preparation"
        )
    response_input = (
        _load_protected_mapping(
            root,
            args.response,
            purpose="consolidated plan response",
        )
        if args.response
        else {"answers": {}, "grants": {}}
    )
    answers = response_input.get("answers", {})
    grants = response_input.get("grants", {})
    if not isinstance(answers, Mapping) or not isinstance(grants, Mapping):
        raise RecordValidationError(
            "consolidated response requires answers and grants mappings"
        )
    acceptance_message = (
        _read_protected_text(
            root,
            args.acceptance_message_file,
            purpose="combined acceptance message",
        )
        if args.acceptance_message_file
        else args.acceptance_message
    )
    _, activation_receipt, question_response = accept_continuous_activation(
        preparation,
        acceptance_message=acceptance_message,
        acceptance_evidence_ref=args.acceptance_evidence_ref,
        answers=answers,
        grants=grants,
        timestamp=args.timestamp,
        activation_id=args.activation_id,
    )
    report = _load_protected_mapping(
        root,
        args.normalization_report,
        purpose="plan normalization report",
    )
    topology = _load_protected_mapping(
        root,
        args.repository_topology_policy,
        purpose="plan repository topology policy",
    )
    outer_holder_token = _read_protected_secret(
        root,
        args.outer_holder_token_file,
        purpose="outer goal holder token",
    )
    store = SQLitePlanStore(
        state_path,
        schema_root=plan_skill_root / "schemas",
    )
    created, initialization_receipt = store.create_initialized_plan(
        plan=preparation.plan,
        normalization_report=report,
        activation_receipt=activation_receipt,
        activation_goal_text=preparation.proposal["goal_text"],
        repository_topology_policy=topology,
        outer_goal_id=args.outer_goal_id,
        expected_outer_revision=args.expected_outer_revision,
        outer_holder_token=outer_holder_token,
        question_batch=preparation.question_batch,
        execution_authority=preparation.execution_authority,
        question_response=question_response,
        timestamp=args.timestamp,
    )
    result = run_plan_to_goal(
        store,
        plan_id=created["plan_id"],
        provider=provider,
        current_outer_holder_token=outer_holder_token,
    )
    return {
        "schema_version": "sys4ai.plan-goal-continuous-launch.v1",
        **result.as_dict(),
        "activation_receipt_sha256": content_sha256(activation_receipt),
        "question_batch_sha256": content_sha256(
            preparation.question_batch
        ),
        "execution_authority_sha256": content_sha256(
            preparation.execution_authority
        ),
        "initialization_receipt_sha256": initialization_receipt[
            "receipt_content_sha256"
        ],
        "continue_required": False,
    }


def command_plan_goal_advance(args: argparse.Namespace) -> dict[str, Any]:
    root, state_path = _plan_state_path(args)
    provider = _continuous_provider(args, root)
    token = (
        _read_protected_secret(
            root,
            args.outer_holder_token_file,
            purpose="outer goal holder token",
        )
        if args.outer_holder_token_file
        else None
    )
    store = SQLitePlanStore(
        state_path,
        schema_root=_implementation_plan_skill_root() / "schemas",
    )
    return advance_plan_once(
        store,
        plan_id=args.plan_id,
        provider=provider,
        current_outer_holder_token=token,
        timestamp=args.timestamp,
    ).as_dict()


def command_plan_goal_answer(args: argparse.Namespace) -> dict[str, Any]:
    root, state_path = _plan_state_path(args)
    provider = _continuous_provider(args, root)
    response_input = _load_protected_mapping(
        root,
        args.response,
        purpose="consolidated plan response",
    )
    answers = response_input.get("answers", {})
    grants = response_input.get("grants", {})
    if not isinstance(answers, Mapping) or not isinstance(grants, Mapping):
        raise RecordValidationError(
            "consolidated response requires answers and grants mappings"
        )
    store = SQLitePlanStore(
        state_path,
        schema_root=_implementation_plan_skill_root() / "schemas",
    )
    state = store.load_continuous_state(args.plan_id)
    if state["pending_question_batch_sha256"] is None:
        raise StateConflict("plan has no pending consolidated question batch")
    batch = store.load_question_batch(
        args.plan_id,
        batch_sha256=state["pending_question_batch_sha256"],
    )
    authority = store.load_execution_authority(args.plan_id)
    return answer_and_resume(
        store,
        plan_id=args.plan_id,
        question_batch=batch,
        execution_authority=authority,
        answers=answers,
        grants=grants,
        provider=provider,
        timestamp=args.timestamp,
    )


def command_plan_goal_status(args: argparse.Namespace) -> dict[str, Any]:
    _, state_path = _plan_state_path(args)
    store = SQLitePlanStore(
        state_path,
        schema_root=_implementation_plan_skill_root() / "schemas",
        read_only=True,
        auto_migrate=False,
    )
    record = store.load_plan(args.plan_id)
    try:
        continuous = store.load_continuous_state(args.plan_id)
    except RecordNotFound:
        return {
            "schema_version": "sys4ai.plan-goal-status.v2",
            "status": "legacy_manual",
            "reason_code": "plan.legacy_state",
            "plan_id": args.plan_id,
            "plan_revision": record["state"]["revision"],
            "plan_phase": record["state"]["phase"],
            "continue_required": True,
        }
    pending_batch = (
        store.load_question_batch(
            args.plan_id,
            batch_sha256=continuous["pending_question_batch_sha256"],
        )
        if continuous["pending_question_batch_sha256"] is not None
        else None
    )
    return {
        "schema_version": "sys4ai.plan-goal-status.v2",
        "status": continuous["status"],
        "reason_code": f"plan.{continuous['status']}",
        "plan_id": args.plan_id,
        "plan_revision": record["state"]["revision"],
        "plan_phase": record["state"]["phase"],
        "continuous_revision": continuous["revision"],
        "generation": record["state"]["current_generation"],
        "current_worker_thread_id": continuous["current_worker_thread_id"],
        "pending_questions": (
            [item["prompt"] for item in pending_batch["questions"]]
            if pending_batch is not None
            else []
        ),
        "completion_report_sha256": continuous[
            "completion_report_sha256"
        ],
        "continue_required": False,
    }


def command_plan_goal_initialize(args: argparse.Namespace) -> dict[str, Any]:
    """Compatibility alias: prepare v2, or run the explicit legacy manual form."""

    if getattr(args, "proposal", None) is not None:
        missing = [
            name
            for name in (
                "plan",
                "repository_observation",
                "provider_capabilities",
            )
            if getattr(args, name, None) is None
        ]
        if missing:
            raise RecordValidationError(
                "initialize preparation alias is missing required inputs",
                details={"missing": missing},
            )
        return command_plan_goal_prepare(args)

    legacy_required = (
        "state_db",
        "sources",
        "goal_text_file",
        "activation_receipt",
        "repository_binding",
        "repository_observation",
        "repository_topology_policy",
        "outer_goal_id",
        "expected_outer_revision",
        "outer_holder_token_file",
        "predecessor_thread_id",
    )
    missing = [
        name for name in legacy_required if getattr(args, name, None) is None
    ]
    if missing:
        raise RecordValidationError(
            "legacy manual initialize is missing required inputs",
            details={"missing": missing},
        )

    root = Path(args.project_root).expanduser().resolve()
    plan_skill_root = _implementation_plan_skill_root()
    repository_binding = _load_protected_mapping(
        root,
        args.repository_binding,
        purpose="plan repository binding",
    )
    repository_observation = _load_protected_mapping(
        root,
        args.repository_observation,
        purpose="plan repository observation",
    )
    activation_receipt = _load_protected_mapping(
        root,
        args.activation_receipt,
        purpose="plan activation receipt",
    )
    topology_policy = _load_protected_mapping(
        root,
        args.repository_topology_policy,
        purpose="plan repository topology policy",
    )
    source_requests = _plan_source_requests(root, args.sources)
    activation_goal = _read_protected_text(
        root,
        args.goal_text_file,
        purpose="plan activation goal",
    )
    outer_holder_token = _read_protected_secret(
        root,
        args.outer_holder_token_file,
        purpose="outer goal holder token",
    )
    provider = ManualThreadProvider(
        root,
        local_root=args.manual_handoff_root,
        current_thread_id=args.predecessor_thread_id,
        timestamp=args.timestamp,
    )
    preflight = preflight_plan_launcher(
        project_root=root,
        repository_binding=repository_binding,
        repository_observation=repository_observation,
        local_state_root=args.local_state_root,
        state_path=args.state_db,
        source_requests=source_requests,
        guards=PlanLauncherGuards(
            max_sources=args.max_sources,
            max_source_bytes=args.max_source_bytes,
            max_total_source_bytes=args.max_total_source_bytes,
        ),
        capabilities={
            "agentjob_control": True,
            "plan_state": True,
            "repository_provider": True,
            "thread_provider": True,
            "thread_execution_profile": True,
            "repository_topology_enforcement": True,
        },
        provider=provider,
    )
    normalization = normalize_plan_preflight(
        preflight,
        planning_adapter=PrdToImplementationPlanAdapter(
            _load_plan_normalizer(plan_skill_root)
        ),
        plan_schema_path=(
            plan_skill_root / "schemas" / "implementation-plan.schema.json"
        ),
        normalization_report_schema_path=(
            plan_skill_root / "schemas" / "normalization-report.schema.json"
        ),
    )
    state_path = root / preflight.state_path
    store = SQLitePlanStore(
        state_path,
        schema_root=plan_skill_root / "schemas",
    )
    initialized = initialize_plan(
        store,
        preflight=preflight,
        normalization=normalization,
        activation_receipt=activation_receipt,
        activation_goal_text=activation_goal,
        repository_topology_policy=topology_policy,
        outer_goal_id=args.outer_goal_id,
        expected_outer_revision=args.expected_outer_revision,
        outer_holder_token=outer_holder_token,
        timestamp=args.timestamp,
    )
    initialized_summary = initialized.as_dict()
    reservation = reserve_first_plan_task(
        store,
        plan_id=str(initialized.plan_record["plan_id"]),
        expected_plan_revision=int(
            initialized.plan_record["state"]["revision"]
        ),
        expected_outer_revision=int(
            initialized_summary["outer_goal_revision"]
        ),
        current_outer_holder_token=outer_holder_token,
        predecessor_thread_id=args.predecessor_thread_id,
        timestamp=args.timestamp,
    )
    reservation_summary = reservation.as_dict()
    dispatch = dispatch_reserved_plan_task(
        store,
        reservation=reservation,
        provider=provider,
        timestamp=args.timestamp,
    )
    dispatch_summary = dispatch.as_dict()
    task_state = next(
        item
        for item in dispatch.plan_record["state"]["tasks"]
        if item["task_id"] == dispatch.task_id
    )
    manual_handoffs = int(dispatch.status == "manual_handoff_pending")
    return {
        "schema_version": "sys4ai.plan-goal-launcher-summary.v1",
        "status": dispatch.status,
        "reason_code": _plan_dispatch_reason_code(dispatch.status),
        "plan_id": dispatch.plan_id,
        "plan_sha256": dispatch.plan_record["effective_plan_sha256"],
        "plan_phase": dispatch.plan_record["state"]["phase"],
        "plan_revision": dispatch.plan_revision,
        "outer_goal_id": dispatch.plan_record["outer_goal_id"],
        "outer_goal_revision": dispatch.outer_goal_revision,
        "source_count": len(preflight.sources),
        "source_set_class": normalization.source_set_class,
        "source_set_sha256": normalization.normalization_report[
            "source_set_sha256"
        ],
        "normalization_report_id": normalization.normalization_report[
            "report_id"
        ],
        "normalization_report_sha256": normalization.normalization_report[
            "report_content_sha256"
        ],
        "activation_id": activation_receipt["activation_id"],
        "activation_receipt_sha256": content_sha256(activation_receipt),
        "reasoning_effort": initialized.plan_record["execution_profile"][
            "reasoning_effort"
        ],
        "repository_binding_sha256": content_sha256(repository_binding),
        "task_id": dispatch.task_id,
        "task_sha256": task_state["task_sha256"],
        "task_status": task_state["status"],
        "generation": dispatch.generation,
        "selection_proof_sha256": reservation.selection_proof_sha256,
        "envelope_sha256": reservation_summary["envelope_sha256"],
        "worker_prompt_sha256": reservation_summary[
            "worker_prompt_sha256"
        ],
        "expected_worker_revision": reservation.expected_worker_revision,
        "provider_id": dispatch.provider_id,
        "provider_status": dispatch.status,
        "provider_intent_id": dispatch.intent_id,
        "provider_intent_sha256": dispatch.intent_sha256,
        "provider_response_sha256": dispatch.provider_response_sha256,
        "successor_thread_id": dispatch.successor_thread_id,
        "manual_handoff_path": dispatch.manual_handoff_path,
        "lease_holder_kind": dispatch.lease_holder_kind,
        "recovery_required": dispatch.recovery_required,
        "effect_counts": {
            "state_writes": (
                int(initialized_summary["state_writes"])
                + int(reservation_summary["state_writes"])
                + int(dispatch_summary["state_writes"])
            ),
            "task_reservations": 1,
            "provider_create_calls": dispatch.provider_create_calls,
            "worker_discussions": dispatch.plan_record["state"][
                "counters"
            ]["worker_discussions"],
            "successor_creates": dispatch.plan_record["state"][
                "counters"
            ]["successor_creates"],
            "manual_handoffs": manual_handoffs,
            "same_task_successors": 0,
            "agentjobs_executed": dispatch.agentjobs_executed,
            "continue_invocations": dispatch.continue_invocations,
            "branch_creations": 0,
            "worktree_creations": 0,
        },
        "next_boundary": dispatch.next_boundary,
        "launcher_effects_performed": True,
        "execution_performed": False,
    }


def add_common(subparser: argparse.ArgumentParser, *, write: bool = False) -> None:
    subparser.add_argument("--project-root", required=True, help="Explicit target project root.")
    subparser.add_argument("--config", help="Project-relative or absolute config path inside project root.")
    subparser.add_argument("--json", action="store_true", help="Emit one machine-readable JSON object.")
    if write:
        subparser.add_argument("--expected-revision", required=True, type=int)


def add_goal_common(subparser: argparse.ArgumentParser, *, write: bool = False) -> None:
    add_common(subparser, write=write)
    subparser.add_argument(
        "--state-db",
        help="Optional project-relative SQLite state path; defaults to configured local state.",
    )
    subparser.add_argument("--timestamp", help="Advanced deterministic UTC timestamp override.")


def add_goal_identity(subparser: argparse.ArgumentParser, *, generation: bool = False) -> None:
    subparser.add_argument("--goal-id", required=True)
    if generation:
        subparser.add_argument("--generation", required=True, type=int)


def add_plan_continuous_provider(
    subparser: argparse.ArgumentParser,
) -> None:
    subparser.add_argument(
        "--provider-adapter",
        required=True,
        help=(
            "Project-relative Python adapter exposing "
            "build_thread_provider(project_root=...)."
        ),
    )
    subparser.add_argument(
        "--thread-strategy",
        choices=["fresh_summary", "fork_history"],
        default="fresh_summary",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and operate portable AgentJob control records.",
        epilog=(
            "Examples:\n"
            "  agentjobctl.py doctor --project-root <PROJECT_ROOT> --json\n"
            "  agentjobctl.py resolve --project-root <PROJECT_ROOT> --task-id <TASK_ID>\n"
            "  agentjobctl.py activate-packet --project-root <PROJECT_ROOT> --task-id <TASK_ID> "
            "--expected-revision 1 --decision decision.json --job job.json --role role.json"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {PACKAGE_VERSION} protocol {PROTOCOL_VERSION}")
    commands = parser.add_subparsers(dest="command", required=True)
    handlers = {
        "doctor": command_doctor,
        "status": command_status,
        "resolve": command_resolve,
        "validate": command_validate,
        "fingerprint": command_fingerprint,
    }
    for name, handler in handlers.items():
        subparser = commands.add_parser(name)
        add_common(subparser)
        if name in {"status", "resolve", "fingerprint"}:
            subparser.add_argument("--task-id")
        subparser.set_defaults(handler=handler)

    activate = commands.add_parser("activate-packet")
    add_common(activate, write=True)
    activate.add_argument("--task-id", required=True)
    activate.add_argument("--decision", required=True)
    activate.add_argument("--job", required=True)
    activate.add_argument("--role", required=True)
    activate.set_defaults(handler=command_activate)

    supersede = commands.add_parser("supersede")
    add_common(supersede, write=True)
    supersede.add_argument("--task-id", required=True)
    supersede.add_argument("--old-decision-id", required=True)
    supersede.add_argument("--old-job-id", required=True)
    supersede.add_argument("--decision", required=True)
    supersede.add_argument("--job", required=True)
    supersede.add_argument("--role", required=True)
    supersede.add_argument("--reason", required=True)
    supersede.add_argument("--evidence-ref", action="append", required=True)
    supersede.add_argument(
        "--prior-execution-status",
        required=True,
        choices=["unexecuted", "partially_executed", "completed", "failed", "ambiguous"],
    )
    supersede.add_argument("--working-evidence-handling", required=True)
    supersede.add_argument("--created-at", required=True)
    supersede.set_defaults(handler=command_supersede)

    complete = commands.add_parser("complete")
    add_common(complete, write=True)
    complete.add_argument("--completion", required=True)
    complete.add_argument("--close-task", action="store_true")
    complete.add_argument("--next-action")
    complete.set_defaults(handler=command_complete)

    handoff = commands.add_parser("handoff")
    add_common(handoff, write=True)
    handoff.add_argument("--handoff", required=True)
    handoff.set_defaults(handler=command_handoff)

    plan_goal = commands.add_parser(
        "plan-goal",
        help="Implementation-plan relay launcher operations.",
    )
    plan_goal_commands = plan_goal.add_subparsers(
        dest="plan_goal_command",
        required=True,
    )
    plan_prepare = plan_goal_commands.add_parser(
        "prepare",
        help="Read-only intake and one consolidated activation prompt.",
    )
    plan_prepare.add_argument("--project-root", required=True)
    plan_prepare.add_argument("--proposal", required=True)
    plan_prepare.add_argument("--plan", required=True)
    plan_prepare.add_argument("--plan-revision", type=int, default=1)
    plan_prepare.add_argument("--repository-observation", required=True)
    plan_prepare.add_argument("--provider-capabilities", required=True)
    plan_prepare.add_argument("--effects")
    plan_prepare.add_argument("--questions")
    plan_prepare.add_argument("--timestamp")
    plan_prepare.add_argument("--json", action="store_true")
    plan_prepare.set_defaults(handler=command_plan_goal_prepare)

    plan_accept = plan_goal_commands.add_parser(
        "accept-and-run",
        help="Record one combined acceptance and enter continuous execution.",
    )
    plan_accept.add_argument("--project-root", required=True)
    plan_accept.add_argument("--state-db", required=True)
    plan_accept.add_argument("--preparation", required=True)
    plan_accept.add_argument("--normalization-report", required=True)
    plan_accept.add_argument("--repository-topology-policy", required=True)
    plan_accept.add_argument("--outer-goal-id", required=True)
    plan_accept.add_argument(
        "--expected-outer-revision", required=True, type=int
    )
    plan_accept.add_argument("--outer-holder-token-file", required=True)
    acceptance = plan_accept.add_mutually_exclusive_group(required=True)
    acceptance.add_argument("--acceptance-message")
    acceptance.add_argument("--acceptance-message-file")
    plan_accept.add_argument("--acceptance-evidence-ref", required=True)
    plan_accept.add_argument("--activation-id")
    plan_accept.add_argument("--response")
    plan_accept.add_argument("--timestamp")
    plan_accept.add_argument("--json", action="store_true")
    add_plan_continuous_provider(plan_accept)
    plan_accept.set_defaults(handler=command_plan_goal_accept_and_run)

    plan_advance = plan_goal_commands.add_parser(
        "advance",
        help="Internal idempotent continuous coordinator step.",
    )
    plan_advance.add_argument("--project-root", required=True)
    plan_advance.add_argument("--state-db", required=True)
    plan_advance.add_argument("--plan-id", required=True)
    plan_advance.add_argument("--outer-holder-token-file")
    plan_advance.add_argument("--timestamp")
    plan_advance.add_argument("--json", action="store_true")
    add_plan_continuous_provider(plan_advance)
    plan_advance.set_defaults(handler=command_plan_goal_advance)

    plan_answer = plan_goal_commands.add_parser(
        "answer",
        help="Record one complete answer batch and resume automatically.",
    )
    plan_answer.add_argument("--project-root", required=True)
    plan_answer.add_argument("--state-db", required=True)
    plan_answer.add_argument("--plan-id", required=True)
    plan_answer.add_argument("--response", required=True)
    plan_answer.add_argument("--timestamp")
    plan_answer.add_argument("--json", action="store_true")
    add_plan_continuous_provider(plan_answer)
    plan_answer.set_defaults(handler=command_plan_goal_answer)

    plan_status = plan_goal_commands.add_parser(
        "status",
        help="Report canonical continuous, waiting, safeguard, or completion state.",
    )
    plan_status.add_argument("--project-root", required=True)
    plan_status.add_argument("--state-db", required=True)
    plan_status.add_argument("--plan-id", required=True)
    plan_status.add_argument("--json", action="store_true")
    plan_status.set_defaults(handler=command_plan_goal_status)

    plan_initialize = plan_goal_commands.add_parser(
        "initialize",
        help=(
            "Compatibility entry: route --proposal input to read-only preparation; "
            "the legacy full form remains an explicit manual degraded mode."
        ),
    )
    plan_initialize.add_argument(
        "--project-root",
        required=True,
        help="Explicit target project root.",
    )
    plan_initialize.add_argument(
        "--state-db",
        required=False,
        help="Project-relative shared outer-goal and plan SQLite state path.",
    )
    plan_initialize.add_argument(
        "--proposal",
        help="Project-relative verified activation proposal; selects v2 preparation.",
    )
    plan_initialize.add_argument(
        "--plan",
        help="Project-relative accepted implementation plan for v2 preparation.",
    )
    plan_initialize.add_argument("--plan-revision", type=int, default=1)
    plan_initialize.add_argument(
        "--provider-capabilities",
        help="Project-relative continuous ThreadProvider capability report.",
    )
    plan_initialize.add_argument(
        "--effects",
        help="Optional project-relative declared protected-effects manifest.",
    )
    plan_initialize.add_argument(
        "--questions",
        help="Optional project-relative declared plan-questions manifest.",
    )
    plan_initialize.add_argument(
        "--local-state-root",
        default=".local/sys4ai",
        help="Project-relative mutable-state root containing --state-db.",
    )
    plan_initialize.add_argument(
        "--sources",
        required=False,
        help="Project-relative JSON/YAML source manifest with path, authority, and precedence.",
    )
    plan_initialize.add_argument(
        "--goal-text-file",
        required=False,
        help="Project-relative exact accepted activation-goal text file.",
    )
    plan_initialize.add_argument(
        "--activation-receipt",
        required=False,
        help="Project-relative combined goal-and-effort acceptance receipt.",
    )
    plan_initialize.add_argument(
        "--repository-binding",
        required=False,
        help="Project-relative accepted repository-binding record.",
    )
    plan_initialize.add_argument(
        "--repository-observation",
        required=False,
        help="Project-relative current RepositoryProvider observation.",
    )
    plan_initialize.add_argument(
        "--repository-topology-policy",
        required=False,
        help="Project-relative accepted repository-topology policy.",
    )
    plan_initialize.add_argument("--outer-goal-id", required=False)
    plan_initialize.add_argument(
        "--expected-outer-revision",
        required=False,
        type=int,
    )
    plan_initialize.add_argument(
        "--outer-holder-token-file",
        required=False,
        help="Project-relative private file; group/other permissions are rejected.",
    )
    plan_initialize.add_argument(
        "--predecessor-thread-id",
        required=False,
    )
    plan_initialize.add_argument(
        "--manual-handoff-root",
        default=".local/sys4ai/continuation/manual",
        help="Project-relative protected manual-provider artifact root.",
    )
    plan_initialize.add_argument("--max-sources", type=int, default=8)
    plan_initialize.add_argument(
        "--max-source-bytes",
        type=int,
        default=4 * 1024 * 1024,
    )
    plan_initialize.add_argument(
        "--max-total-source-bytes",
        type=int,
        default=16 * 1024 * 1024,
    )
    plan_initialize.add_argument(
        "--timestamp",
        help="Advanced deterministic UTC timestamp override.",
    )
    plan_initialize.add_argument(
        "--json",
        action="store_true",
        help="Emit one redacted machine-readable launcher summary.",
    )
    plan_initialize.set_defaults(handler=command_plan_goal_initialize)

    goal = commands.add_parser(
        "goal",
        help="One-confirmation continuous goals plus advanced compatibility operations.",
    )
    goal_commands = goal.add_subparsers(dest="goal_command", required=True)

    goal_prepare = goal_commands.add_parser(
        "prepare",
        help="Read-only complete intake and one consolidated v4 confirmation prompt.",
    )
    goal_prepare.add_argument("--project-root", required=True)
    goal_prepare.add_argument("--proposal", required=True)
    goal_prepare.add_argument("--completion-contract", required=True)
    goal_prepare.add_argument("--repository-binding", required=True)
    goal_prepare.add_argument("--repository-observation", required=True)
    goal_prepare.add_argument("--initial-fingerprint", required=True)
    goal_prepare.add_argument("--provider-capabilities", required=True)
    goal_prepare.add_argument("--intake-inventory", required=True)
    goal_prepare.add_argument("--questions")
    goal_prepare.add_argument("--grants")
    goal_prepare.add_argument("--timestamp")
    goal_prepare.add_argument("--json", action="store_true")
    goal_prepare.set_defaults(handler=command_goal_prepare)

    goal_accept = goal_commands.add_parser(
        "accept-and-run",
        help="Record one complete response, initialize v4, and stay active until met.",
    )
    add_goal_common(goal_accept)
    goal_accept.add_argument("--preparation", required=True)
    goal_accept.add_argument("--response")
    goal_accept.add_argument("--repository-observation")
    goal_accept.add_argument("--initial-fingerprint")
    goal_accept.add_argument(
        "--setup-adapter",
        help=(
            "Project-relative adapter for accepted setup effects and live "
            "post-setup repository revalidation."
        ),
    )
    acceptance = goal_accept.add_mutually_exclusive_group(required=True)
    acceptance.add_argument("--acceptance-message")
    acceptance.add_argument("--acceptance-message-file")
    goal_accept.add_argument("--acceptance-evidence-ref", required=True)
    goal_accept.add_argument("--guards")
    goal_accept.add_argument("--runtime-binding")
    goal_accept.add_argument("--goal-id")
    add_plan_continuous_provider(goal_accept)
    goal_accept.set_defaults(handler=command_goal_accept_and_run)

    goal_advance = goal_commands.add_parser(
        "advance",
        help="Internal idempotent v4 coordinator resumption boundary.",
    )
    add_goal_common(goal_advance)
    add_goal_identity(goal_advance)
    add_plan_continuous_provider(goal_advance)
    goal_advance.set_defaults(handler=command_goal_advance)

    initialize = goal_commands.add_parser("initialize", help="Initialize one exact durable goal.")
    add_goal_common(initialize)
    initialize.add_argument("--goal-text")
    initialize.add_argument("--goal-text-file")
    initialize.add_argument("--completion-contract", required=True)
    initialize.add_argument(
        "--activation-receipt",
        required=True,
        help="Combined goal-and-effort acceptance receipt.",
    )
    initialize.add_argument(
        "--guards",
        help="Optional JSON/YAML pass and deadline limits; omitted means unlimited.",
    )
    initialize.add_argument("--repository-binding", required=True)
    initialize.add_argument("--runtime-binding")
    initialize.add_argument("--repository-topology-policy")
    initialize.add_argument("--initial-fingerprint", required=True)
    initialize.add_argument("--goal-id")
    initialize.add_argument("--launcher-token-file")
    initialize.add_argument(
        "--fresh-recursive-threads-explicitly-requested",
        action="store_true",
        required=True,
    )
    initialize.set_defaults(handler=command_goal_initialize)

    goal_status = goal_commands.add_parser("status", help="Read goal summaries without mutation.")
    add_goal_common(goal_status)
    goal_status.add_argument("--goal-id")
    goal_status.set_defaults(handler=command_goal_status)

    goal_export = goal_commands.add_parser("export", help="Emit deterministic redacted goal records.")
    add_goal_common(goal_export)
    goal_export.add_argument("--goal-id")
    goal_export.set_defaults(handler=command_goal_export)

    completion_summary = goal_commands.add_parser(
        "completion-summary",
        help="Read the canonical goal-completion report.",
    )
    add_goal_common(completion_summary)
    add_goal_identity(completion_summary)
    completion_summary.add_argument(
        "--markdown",
        action="store_true",
        help="Render the authoritative user-facing completion summary.",
    )
    completion_summary.set_defaults(handler=command_goal_completion_summary)

    reserve = goal_commands.add_parser(
        "reserve-successor", help="Advanced: reserve one successor intent."
    )
    add_goal_common(reserve, write=True)
    add_goal_identity(reserve)
    reserve.add_argument("--holder-token-file", required=True)
    reserve.add_argument("--handoff-token-file")
    reserve.add_argument("--predecessor-thread-id")
    reserve.set_defaults(handler=command_goal_reserve)

    record = goal_commands.add_parser(
        "record-successor", help="Advanced: record one provider-returned successor identity."
    )
    add_goal_common(record, write=True)
    add_goal_identity(record, generation=True)
    record.add_argument("--handoff-token-file", required=True)
    record.add_argument("--successor-thread-id", required=True)
    record.add_argument("--provider-id", required=True)
    record.add_argument("--provider-response", required=True)
    record.set_defaults(handler=command_goal_record_successor)

    claim = goal_commands.add_parser("claim", help="Advanced internal generation claim.")
    add_goal_common(claim, write=True)
    add_goal_identity(claim, generation=True)
    claim.add_argument("--handoff-token-file", required=True)
    claim.add_argument("--idempotency-key", required=True)
    claim.add_argument("--successor-thread-id", required=True)
    claim.add_argument("--claim-token-file")
    claim.set_defaults(handler=command_goal_claim)

    consume = goal_commands.add_parser("consume", help="Advanced irreversible invocation consumption.")
    add_goal_common(consume, write=True)
    add_goal_identity(consume, generation=True)
    consume.add_argument("--claim-token-file", required=True)
    consume.add_argument("--observations")
    consume.set_defaults(handler=command_goal_consume)

    returned = goal_commands.add_parser("returned", help="Advanced direct-return recording.")
    add_goal_common(returned, write=True)
    add_goal_identity(returned, generation=True)
    returned.add_argument("--claim-token-file", required=True)
    returned.add_argument("--continue-result", required=True)
    returned.set_defaults(handler=command_goal_returned)

    unknown = goal_commands.add_parser("unknown", help="Advanced unknown-outcome quarantine.")
    add_goal_common(unknown, write=True)
    add_goal_identity(unknown, generation=True)
    unknown.add_argument("--claim-token-file", required=True)
    unknown.add_argument("--diagnostic", required=True)
    unknown.set_defaults(handler=command_goal_unknown)

    verify = goal_commands.add_parser("verify", help="Advanced canonical generation verification.")
    add_goal_common(verify, write=True)
    add_goal_identity(verify, generation=True)
    verify.add_argument("--claim-token-file", required=True)
    verify.add_argument("--continue-result", required=True)
    verify.add_argument("--direct-evidence", required=True)
    verify.set_defaults(handler=command_goal_verify)

    decide = goal_commands.add_parser("decide", help="Advanced terminal or continuation decision.")
    add_goal_common(decide, write=True)
    add_goal_identity(decide, generation=True)
    decide.add_argument("--claim-token-file", required=True)
    decide.add_argument("--legal-route-available", action="store_true")
    decide.add_argument("--explicit-stop-reason")
    decide.set_defaults(handler=command_goal_decide)

    recover = goal_commands.add_parser("recover", help="Explicit evidence-backed recovery action.")
    add_goal_common(recover, write=True)
    add_goal_identity(recover)
    recover.add_argument(
        "--action", required=True, choices=["begin", "adopt", "resume", "abandon", "reconcile"]
    )
    recover.add_argument(
        "--user-authorization",
        help="Required for authority changes; deterministic existing-authority reconciliation may omit it.",
    )
    recover.add_argument("--evidence", required=True)
    recover.add_argument("--generation", type=int)
    recover.add_argument("--successor-thread-id")
    recover.add_argument("--canonical-evidence")
    recover.add_argument("--returned-proven", action="store_true")
    recover.add_argument("--decision")
    recover.set_defaults(handler=command_goal_recover)

    amend_contract = goal_commands.add_parser(
        "amend-contract", help="Append one authorized completion-contract amendment."
    )
    add_goal_common(amend_contract, write=True)
    add_goal_identity(amend_contract)
    amend_contract.add_argument("--user-authorization", required=True)
    amend_contract.add_argument("--evidence", required=True)
    amend_contract.add_argument("--completion-contract", required=True)
    amend_contract.set_defaults(handler=command_goal_amend_contract)

    amend_guard_values = goal_commands.add_parser(
        "amend-guards", help="Append one authorized finite-guard extension."
    )
    add_goal_common(amend_guard_values, write=True)
    add_goal_identity(amend_guard_values)
    amend_guard_values.add_argument("--user-authorization", required=True)
    amend_guard_values.add_argument("--evidence", required=True)
    amend_guard_values.add_argument("--guards", required=True)
    amend_guard_values.set_defaults(handler=command_goal_amend_guards)

    cancel = goal_commands.add_parser("cancel", help="Cancel a relay from recovery_pending.")
    add_goal_common(cancel, write=True)
    add_goal_identity(cancel)
    cancel.add_argument("--user-authorization", required=True)
    cancel.add_argument("--evidence", required=True)
    cancel.set_defaults(handler=command_goal_cancel)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
        if (
            getattr(args, "goal_command", None) == "completion-summary"
            and getattr(args, "markdown", False)
        ):
            print(result["markdown"], end="")
            return 0
        emit(result, as_json=args.json)
        return 0
    except AgentJobControlError as error:
        emit(error.as_dict(), as_json=getattr(args, "json", False))
        return error.exit_code
    except (OSError, ValueError) as error:
        wrapped = AgentJobControlError(str(error), details={"reason_code": "cli.unexpected_input"})
        emit(wrapped.as_dict(), as_json=getattr(args, "json", False))
        return wrapped.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
