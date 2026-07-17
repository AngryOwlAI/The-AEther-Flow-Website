#!/usr/bin/env python3
"""Portable AgentJob control command-line interface."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime import PACKAGE_VERSION, PROTOCOL_VERSION
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
)
from agentjob_runtime.fingerprinting.canonical import FingerprintResult
from agentjob_runtime.goal.decide import decide_generation
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
    loaded = load_config(args.project_root, config_path=args.config)
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
    return {
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
        guards=load_mapping(args.guards),
        repository_binding=load_mapping(args.repository_binding),
        initial_fingerprint=args.initial_fingerprint,
        authorization={
            "fresh_recursive_threads_explicitly_requested": bool(
                args.fresh_recursive_threads_explicitly_requested
            )
        },
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

    goal = commands.add_parser(
        "goal",
        help="Durable goal relay operations; mutation subcommands are advanced and revision-checked.",
    )
    goal_commands = goal.add_subparsers(dest="goal_command", required=True)

    initialize = goal_commands.add_parser("initialize", help="Initialize one exact durable goal.")
    add_goal_common(initialize)
    initialize.add_argument("--goal-text")
    initialize.add_argument("--goal-text-file")
    initialize.add_argument("--completion-contract", required=True)
    initialize.add_argument("--guards", required=True)
    initialize.add_argument("--repository-binding", required=True)
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
    recover.add_argument("--user-authorization", required=True)
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
