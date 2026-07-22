#!/usr/bin/env python3
"""Crash-auditable CLI for the plan-native recursive relay."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "skills" / "agentjob-control" / "scripts"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from agentjob_runtime.errors import AgentJobControlError, RecordValidationError  # noqa: E402
from agentjob_runtime.plan.relay import (  # noqa: E402
    PROFILE,
    TOPOLOGY,
    RelayStore,
    build_successor_prompt,
    validate_plan,
)
from agentjob_runtime.state_utils import canonical_json_bytes, content_sha256  # noqa: E402
from agentjob_runtime.validation.schema import format_issues, validate_instance  # noqa: E402


SCHEMAS = Path(__file__).resolve().parents[1] / "schemas"
SCHEMA_BY_VERSION = {
    "sys4ai.plan-relay-run.v1": "plan-relay-run-v1.schema.json",
    "sys4ai.plan-relay-generation.v1": "plan-relay-generation-v1.schema.json",
    "sys4ai.plan-task-envelope.v3": "plan-task-envelope-v3.schema.json",
    "sys4ai.plan-task-receipt.v3": "plan-task-receipt-v3.schema.json",
    "sys4ai.plan-dispatch-intent.v3": "plan-dispatch-intent-v3.schema.json",
    "sys4ai.plan-relay-lease.v1": "plan-relay-lease-v1.schema.json",
    "sys4ai.plan-completion-report.v2": "plan-completion-report-v2.schema.json",
    "sys4ai.codex-goal-mirror.v1": "codex-goal-mirror-v1.schema.json",
}


def _load(path: str) -> Any:
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _emit(value: Any) -> None:
    sys.stdout.buffer.write(canonical_json_bytes(value) + b"\n")


def _request(args: argparse.Namespace) -> dict[str, Any]:
    value = _load(args.request)
    if not isinstance(value, dict):
        raise RecordValidationError("--request must contain one JSON object")
    return value


def _raw_token_fields(value: Any, path: str = "$") -> list[str]:
    forbidden = {"handoff_token", "lease_token", "raw_token", "access_token"}
    findings: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            child_path = f"{path}.{key}"
            if key in forbidden:
                findings.append(child_path)
            findings.extend(_raw_token_fields(item, child_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(_raw_token_fields(item, f"{path}[{index}]"))
    return findings


def validate_record(value: dict[str, Any]) -> dict[str, Any]:
    version = value.get("schema_version")
    if version not in SCHEMA_BY_VERSION:
        raise RecordValidationError(
            "record schema_version is unsupported",
            details={"reason_code": "relay.schema_version_unsupported"},
        )
    issues = validate_instance(value, SCHEMAS / SCHEMA_BY_VERSION[str(version)])
    if issues:
        raise RecordValidationError(
            "relay record failed schema validation",
            details={
                "reason_code": "relay.schema_invalid",
                "findings": format_issues(issues).splitlines(),
            },
        )
    present = sorted(_raw_token_fields(value))
    if present:
        raise RecordValidationError(
            "durable relay record contains a raw token field",
            details={"reason_code": "relay.raw_token_forbidden", "paths": present},
        )
    return {
        "status": "valid",
        "schema_version": version,
        "content_sha256": content_sha256(value),
    }


def validate_chain(value: dict[str, Any]) -> dict[str, Any]:
    """Validate one complete cross-record relay projection."""

    if value.get("schema_version") != "sys4ai.plan-relay-chain.v1":
        raise RecordValidationError(
            "relay chain schema_version is unsupported",
            details={"reason_code": "relay.chain_schema_unsupported"},
        )
    allowed_keys = {
        "schema_version",
        "run",
        "generations",
        "envelopes",
        "intents",
        "receipts",
        "lease",
        "completion_report",
        "goal_mirror",
        "projection_content_sha256",
    }
    if set(value) != allowed_keys:
        raise RecordValidationError(
            "relay chain fields are incomplete or unknown",
            details={
                "reason_code": "relay.chain_fields_invalid",
                "missing": sorted(allowed_keys - set(value)),
                "unknown": sorted(set(value) - allowed_keys),
            },
        )
    expected_projection_hash = value.get("projection_content_sha256")
    projection_basis = dict(value)
    projection_basis.pop("projection_content_sha256", None)
    if expected_projection_hash != content_sha256(projection_basis):
        raise RecordValidationError(
            "relay chain projection hash is invalid",
            details={"reason_code": "relay.chain_hash_mismatch"},
        )
    raw_token_paths = _raw_token_fields(value)
    if raw_token_paths:
        raise RecordValidationError(
            "relay chain contains a raw token field",
            details={
                "reason_code": "relay.raw_token_forbidden",
                "paths": sorted(raw_token_paths),
            },
        )
    run = value.get("run")
    generations = value.get("generations")
    envelopes = value.get("envelopes")
    intents = value.get("intents")
    receipts = value.get("receipts")
    lease = value.get("lease")
    completion = value.get("completion_report")
    mirror = value.get("goal_mirror")
    if (
        not isinstance(run, dict)
        or not isinstance(generations, list)
        or not generations
        or not isinstance(envelopes, list)
        or not isinstance(intents, list)
        or not isinstance(receipts, list)
        or not isinstance(lease, dict)
        or (completion is not None and not isinstance(completion, dict))
        or (mirror is not None and not isinstance(mirror, dict))
    ):
        raise RecordValidationError(
            "relay chain record collections are invalid",
            details={"reason_code": "relay.chain_collections_invalid"},
        )
    validate_record(run)
    validate_record(lease)
    for record in [*generations, *envelopes, *intents, *receipts]:
        if not isinstance(record, dict):
            raise RecordValidationError(
                "relay chain collection contains a non-object",
                details={"reason_code": "relay.chain_record_not_object"},
            )
        validate_record(record)
    if completion is not None:
        validate_record(completion)
    if mirror is not None:
        validate_record(mirror)

    findings: list[dict[str, Any]] = []
    run_id = run["run_id"]
    plan_id = run["plan_id"]
    active_statuses = {"dispatch_pending", "reserved", "claimed", "consumed", "returned"}
    active = 0
    seen_tasks: set[str] = set()
    by_generation: dict[int, dict[str, Any]] = {}
    for index, item in enumerate(generations, 1):
        by_generation[index] = item
        if item.get("generation") != index:
            findings.append({"reason_code": "relay.generation_sequence_mismatch", "generation": index})
        if item.get("run_id") != run_id:
            findings.append({"reason_code": "relay.run_identity_mismatch", "generation": index})
        task_id = item.get("task_id")
        if task_id in seen_tasks:
            findings.append({"reason_code": "relay.same_task_successor", "generation": index})
        if isinstance(task_id, str):
            seen_tasks.add(task_id)
        if item.get("status") in active_statuses:
            active += 1
        if index == 1:
            if (
                item.get("predecessor_thread_id") != run["launcher_thread_id"]
                or item.get("predecessor_receipt_sha256") is not None
            ):
                findings.append(
                    {
                        "reason_code": "relay.launcher_predecessor_mismatch",
                        "generation": index,
                    }
                )
        else:
            prior = generations[index - 2]
            if item.get("predecessor_thread_id") != prior.get("worker_thread_id"):
                findings.append({"reason_code": "relay.predecessor_thread_mismatch", "generation": index})
            if item.get("predecessor_receipt_sha256") != prior.get("receipt_sha256"):
                findings.append({"reason_code": "relay.predecessor_receipt_mismatch", "generation": index})
            if prior.get("successor_generation") != index:
                findings.append({"reason_code": "relay.successor_link_mismatch", "generation": index})
        if int(item.get("invocation_count", 0)) > 1:
            findings.append({"reason_code": "relay.invocation_cardinality_exceeded", "generation": index})
    if run["current_generation"] != len(generations):
        findings.append({"reason_code": "relay.current_generation_mismatch"})
    if active > 1:
        findings.append({"reason_code": "relay.multiple_active_generations", "count": active})

    if len(envelopes) != len(generations):
        findings.append({"reason_code": "relay.envelope_cardinality_mismatch"})
    if len(intents) != len(generations):
        findings.append({"reason_code": "relay.intent_cardinality_mismatch"})
    envelope_by_generation = {
        int(item["generation"]): item for item in envelopes
    }
    intent_by_generation = {int(item["generation"]): item for item in intents}
    if len(envelope_by_generation) != len(envelopes):
        findings.append({"reason_code": "relay.duplicate_envelope_generation"})
    if len(intent_by_generation) != len(intents):
        findings.append({"reason_code": "relay.duplicate_intent_generation"})
    for generation, item in by_generation.items():
        envelope = envelope_by_generation.get(generation)
        intent = intent_by_generation.get(generation)
        if envelope is not None:
            expected_envelope_identity = (
                envelope.get("run_id") == run_id
                and envelope.get("plan_id") == plan_id
                and envelope.get("plan_sha256") == run["plan_sha256"]
                and envelope.get("generation") == generation
                and envelope.get("task_id") == item["task_id"]
                and envelope.get("task_sha256") == item["task_sha256"]
                and envelope.get("predecessor_thread_id")
                == item["predecessor_thread_id"]
                and envelope.get("predecessor_receipt_sha256")
                == item["predecessor_receipt_sha256"]
                and envelope.get("repository_fingerprint")
                == run["repository_fingerprint"]
                and envelope.get("control_fingerprint")
                == run["control_fingerprint"]
                and envelope.get("relay_profile") == run["relay_profile"]
                and envelope.get("relay_topology") == run["relay_topology"]
                and envelope.get("requested_effort") == item["requested_effort"]
                and envelope.get("handoff_token_sha256")
                == item["handoff_token_sha256"]
                and content_sha256(envelope) == item["envelope_sha256"]
            )
            if not expected_envelope_identity:
                findings.append(
                    {
                        "reason_code": "relay.envelope_identity_mismatch",
                        "generation": generation,
                    }
                )
        if intent is not None:
            if (
                intent.get("run_id") != run_id
                or intent.get("generation") != generation
                or intent.get("requested_effort") != item["requested_effort"]
                or intent.get("create_budget") != 1
            ):
                findings.append(
                    {
                        "reason_code": "relay.intent_identity_mismatch",
                        "generation": generation,
                    }
                )
            if intent.get("status") == "recorded" and (
                intent.get("child_thread_id") != item.get("worker_thread_id")
                or intent.get("provider_response_sha256") is None
            ):
                findings.append(
                    {
                        "reason_code": "relay.recorded_child_mismatch",
                        "generation": generation,
                    }
                )

    receipt_by_generation = {
        int(item["generation"]): item for item in receipts
    }
    if len(receipt_by_generation) != len(receipts):
        findings.append({"reason_code": "relay.duplicate_receipt_generation"})
    for generation, item in by_generation.items():
        receipt = receipt_by_generation.get(generation)
        if receipt is None:
            if item.get("receipt_sha256") is not None:
                findings.append(
                    {
                        "reason_code": "relay.receipt_projection_missing",
                        "generation": generation,
                    }
                )
            continue
        if (
            receipt.get("run_id") != run_id
            or receipt.get("plan_id") != plan_id
            or receipt.get("plan_sha256") != run["plan_sha256"]
            or receipt.get("task_id") != item["task_id"]
            or receipt.get("task_sha256") != item["task_sha256"]
            or receipt.get("worker_thread_id") != item["worker_thread_id"]
            or receipt.get("repository_fingerprint")
            != run["repository_fingerprint"]
            or receipt.get("control_fingerprint") != run["control_fingerprint"]
            or receipt.get("relay_profile") != run["relay_profile"]
            or receipt.get("relay_topology") != run["relay_topology"]
            or content_sha256(receipt) != item.get("receipt_sha256")
        ):
            findings.append(
                {
                    "reason_code": "relay.receipt_identity_mismatch",
                    "generation": generation,
                }
            )

    if (
        lease.get("run_id") != run_id
        or lease.get("repository_fingerprint") != run["repository_fingerprint"]
        or lease.get("steal_authorized") is not False
    ):
        findings.append({"reason_code": "relay.lease_identity_mismatch"})
    if mirror is not None and (
        mirror.get("run_id") != run_id
        or mirror.get("may_mark_complete") is not False
    ):
        findings.append({"reason_code": "relay.goal_mirror_authority_mismatch"})

    if completion is None:
        if run.get("completion_report_sha256") is not None:
            findings.append({"reason_code": "relay.completion_report_missing"})
    else:
        terminal_proof_valid = (
            completion.get("run_id") == run_id
            and completion.get("plan_id") == plan_id
            and completion.get("plan_sha256") == run["plan_sha256"]
            and completion.get("repository_fingerprint")
            == run["repository_fingerprint"]
            and completion.get("control_fingerprint")
            == run["control_fingerprint"]
            and completion.get("relay_profile") == run["relay_profile"]
            and completion.get("relay_topology") == run["relay_topology"]
            and completion.get("receipt_count") == len(receipts)
            and completion.get("missing_task_ids") == []
            and completion.get("open_intent_count") == 0
            and completion.get("terminal_proof") is True
        )
        if not terminal_proof_valid:
            findings.append({"reason_code": "relay.terminal_proof_incomplete"})
        if run.get("completion_report_sha256") not in {
            None,
            content_sha256(completion),
        }:
            findings.append({"reason_code": "relay.completion_report_hash_mismatch"})
    if run["status"] == "plan_complete" and (
        completion is None
        or run.get("completion_report_sha256") != content_sha256(completion)
        or lease.get("released_at") is None
    ):
        findings.append({"reason_code": "relay.terminal_state_incomplete"})
    if findings:
        raise RecordValidationError("relay chain failed semantic validation", details={"findings": findings})
    return {
        "status": "valid",
        "generation_count": len(generations),
        "receipt_count": len(receipts),
        "active_generation_count": active,
        "terminal": run["status"] == "plan_complete",
        "projection_content_sha256": expected_projection_hash,
    }


def _preflight() -> dict[str, Any]:
    if sys.version_info < (3, 11):
        raise RecordValidationError(
            "plan-native relay requires Python >=3.11",
            details={"reason_code": "relay.python_unsupported", "current": sys.version.split()[0]},
        )
    resolved = str(Path(sys.executable).resolve())
    configured = os.environ.get("SYS4AI_RELAY_PYTHON")
    if configured is not None and str(Path(configured).resolve()) != resolved:
        raise RecordValidationError(
            "nested relay interpreter differs from the parent runtime",
            details={"reason_code": "relay.interpreter_mismatch", "current": resolved, "expected": configured},
        )
    return {"status": "compatible", "python": resolved, "version": sys.version.split()[0], "requires_python": ">=3.11"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan-native recursive relay; no coordinator or generic outer goal.",
        epilog="Ambiguous create: reconcile-dispatch. Consumed unknown: reconcile-consumed; never rerun blindly.",
    )
    parser.add_argument("--database", default=".local/sys4ai/implementation-plan-relay/state.sqlite3")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("runtime-preflight")
    sub.add_parser("bootstrap")
    prepare = sub.add_parser("prepare", help="read-only plan classification")
    prepare.add_argument("plan")
    launch = sub.add_parser("launch", aliases=["activate-relay"])
    launch.add_argument("--request", required=True)
    for name in (
        "prepare-dispatch",
        "record-dispatch-ambiguous",
        "record-successor",
        "adopt-successor",
        "claim-generation",
        "consume-generation",
        "record-returned",
        "record-unknown",
        "record-protected-stop",
        "verify-and-decide",
        "reserve-successor",
        "finalize-plan",
        "reconcile-dispatch",
        "abandon-unconsumed",
        "reconcile-consumed",
        "cancel",
    ):
        command = sub.add_parser(name)
        command.add_argument("--request", required=True, help="canonical JSON request with CAS and identity evidence")
    summary = sub.add_parser("summarize", help="strictly read-only status")
    summary.add_argument("run_id")
    projection = sub.add_parser(
        "project-chain",
        help="strictly read-only schema-valid cross-record projection",
    )
    projection.add_argument("run_id")
    export = sub.add_parser("export", help="strictly read-only canonical export")
    export.add_argument("run_id")
    journal = sub.add_parser("verify-journal")
    journal.add_argument("run_id")
    record = sub.add_parser("validate-record")
    record.add_argument("path")
    chain = sub.add_parser("validate-chain")
    chain.add_argument("path")
    prompt = sub.add_parser("build-successor-prompt")
    prompt.add_argument("--request", required=True)
    sub.add_parser("legacy-status", help="read-only legacy boundary; never a writer")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = RelayStore(args.database)
    try:
        _preflight()
        command = args.command
        if command == "runtime-preflight":
            result = _preflight()
        elif command == "bootstrap":
            result = store.bootstrap()
        elif command == "prepare":
            plan = validate_plan(_load(args.plan))
            result = {
                "status": "prepared",
                "plan_id": plan["plan_id"],
                "plan_sha256": content_sha256(plan),
                "task_count": len(plan["tasks"]),
                "relay_profile": PROFILE,
                "relay_topology": TOPOLOGY,
                "mutated": False,
            }
        elif command in {"launch", "activate-relay"}:
            result = store.launch(**_request(args))
        elif command in {"record-successor", "adopt-successor"}:
            result = store.record_successor(**_request(args))
        elif command == "prepare-dispatch":
            result = store.begin_dispatch(**_request(args))
        elif command == "record-dispatch-ambiguous":
            result = store.mark_dispatch_ambiguous(**_request(args))
        elif command == "claim-generation":
            result = store.claim_generation(**_request(args))
        elif command == "consume-generation":
            result = store.consume_generation(**_request(args))
        elif command == "record-returned":
            result = store.record_returned(**_request(args))
        elif command == "record-unknown":
            result = store.record_unknown(**_request(args))
        elif command == "record-protected-stop":
            result = store.record_protected_stop(**_request(args))
        elif command == "verify-and-decide":
            result = store.verify_and_decide(**_request(args))
        elif command == "reserve-successor":
            result = store.reserve_successor(**_request(args))
        elif command == "finalize-plan":
            result = store.finalize_plan(**_request(args))
        elif command == "reconcile-dispatch":
            result = store.reconcile_dispatch(**_request(args))
        elif command == "abandon-unconsumed":
            result = store.abandon_unconsumed(**_request(args))
        elif command == "reconcile-consumed":
            result = store.reconcile_consumed(**_request(args))
        elif command == "summarize":
            result = store.summarize(args.run_id)
        elif command == "project-chain":
            result = store.semantic_projection(args.run_id)
            validate_chain(result)
        elif command == "cancel":
            result = store.cancel(**_request(args))
        elif command == "export":
            result = store.export(args.run_id)
        elif command == "verify-journal":
            result = store.verify_journal(args.run_id)
        elif command == "validate-record":
            result = validate_record(_load(args.path))
        elif command == "validate-chain":
            result = validate_chain(_load(args.path))
        elif command == "build-successor-prompt":
            result = {"status": "built", "prompt": build_successor_prompt(**_request(args))}
        elif command == "legacy-status":
            result = {
                "status": "legacy_reader_only",
                "writer_enabled": False,
                "required_selector_for_historical_mutation": "coordinator_v2_legacy",
            }
        else:  # pragma: no cover
            raise AssertionError(command)
        _emit(result)
        return 0
    except AgentJobControlError as error:
        _emit(error.as_dict())
        return error.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
