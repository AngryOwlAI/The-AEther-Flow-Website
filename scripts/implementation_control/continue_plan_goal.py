#!/usr/bin/env python3
"""Canonical-JSON façade for the website implementation-plan relay."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from implementation_control.plan_goal_adapter import (  # noqa: E402
    REPO_ROOT,
    WebsitePlanAdapterError,
    activate_plan,
    adopt_worker,
    bootstrap_website_packet,
    canonical_json,
    complete_bootstrap_website_packet,
    finalize_plan,
    prepare_plan,
    prepare_plan_finalization,
    recover,
    reserve_next,
    status,
    worker_consume,
    worker_fail,
    worker_finalize,
    worker_prepare,
    worker_unknown,
)
from implementation_control.plan_relay_adapter import (  # noqa: E402
    WebsiteRelayAdapterError,
    abandon_unconsumed,
    cancel_relay,
    claim_generation,
    consume_generation,
    finalize_receipt,
    finalize_relay_plan,
    launch_relay,
    prepare_relay,
    prepare_dispatch,
    reconcile_consumed,
    reconcile_dispatch,
    record_dispatch_ambiguous,
    record_protected_stop,
    record_returned,
    record_successor,
    record_unknown,
    relay_chain_projection,
    relay_status,
    reserve_successor,
    verify_and_decide,
)

try:  # noqa: E402
    from agentjob_runtime.errors import AgentJobControlError
except ImportError:  # Installation validation reports this more specifically.
    AgentJobControlError = RuntimeError  # type: ignore[assignment,misc]


def _add_plan_source(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--plan", required=True)
    parser.add_argument("--binding")


def _add_prepare_fields(parser: argparse.ArgumentParser) -> None:
    _add_plan_source(parser)
    parser.add_argument("--goal")
    parser.add_argument("--reasoning-effort", default="max")
    parser.add_argument("--current-thread-id", required=True)
    parser.add_argument(
        "--current-profile-evidence-ref",
        required=True,
    )


def _add_mutation_cas(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--expected-plan-revision",
        required=True,
        type=int,
    )
    parser.add_argument(
        "--expected-control-sha256",
        required=True,
    )


def _add_legacy_profile(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--legacy-profile",
        choices=("coordinator_v2_legacy",),
        required=True,
        help="Explicit selector required for a legacy coordinator mutation.",
    )


def _add_control_cas(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--expected-control-sha256",
        required=True,
    )


def _load_json_object(path: str, *, label: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise WebsiteRelayAdapterError(
            f"{label} must be one JSON object",
            reason_code="relay.request_invalid",
        )
    return value


def _add_relay_mutation(parser: argparse.ArgumentParser, *, generation: bool = True) -> None:
    parser.add_argument("--run-id", required=True)
    if generation:
        parser.add_argument("--generation", required=True, type=int)
    _add_mutation_cas(parser)
    parser.add_argument("--current-thread-id", required=True)
    parser.add_argument("--handoff-token", required=True)


def _relay_common(arguments: argparse.Namespace) -> dict[str, Any]:
    return {
        "run_id": arguments.run_id,
        "generation": arguments.generation,
        "expected_revision": arguments.expected_plan_revision,
        "expected_control_sha256": arguments.expected_control_sha256,
        "current_thread_id": arguments.current_thread_id,
        "handoff_token": arguments.handoff_token,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the plan-native recursive relay; legacy coordinator commands "
            "are explicitly named and never selected by default."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=str(REPO_ROOT),
        help="Website repository root.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--plan-id")

    summary_parser = subparsers.add_parser(
        "summarize", help="read-only recursive chain and website-control status"
    )
    summary_parser.add_argument("--run-id", required=True)

    projection_parser = subparsers.add_parser(
        "project-chain", help="read-only redacted recursive chain projection"
    )
    projection_parser.add_argument("--run-id", required=True)

    relay_prepare_parser = subparsers.add_parser("relay-prepare")
    relay_prepare_parser.add_argument("--plan", required=True)
    relay_prepare_parser.add_argument("--launcher-thread-id", required=True)
    relay_prepare_parser.add_argument("--reasoning-effort", default="max")

    launch_parser = subparsers.add_parser("launch", aliases=["activate-relay"])
    launch_parser.add_argument("--plan", required=True)
    launch_parser.add_argument("--acceptance", required=True)
    launch_parser.add_argument("--expected-control-sha256", required=True)
    launch_parser.add_argument("--launcher-thread-id", required=True)
    launch_parser.add_argument("--reasoning-effort", default="max")
    launch_parser.add_argument("--run-id")

    record_parser = subparsers.add_parser("record-successor", aliases=["adopt-successor"])
    _add_relay_mutation(record_parser)
    record_parser.add_argument("--child-thread-id", required=True)
    record_parser.add_argument("--provider-response", required=True)
    record_parser.add_argument("--effective-reasoning-effort", required=True)

    dispatch_parser = subparsers.add_parser("prepare-dispatch")
    _add_relay_mutation(dispatch_parser)

    ambiguous_dispatch_parser = subparsers.add_parser(
        "record-dispatch-ambiguous"
    )
    _add_relay_mutation(ambiguous_dispatch_parser)
    ambiguous_dispatch_parser.add_argument("--evidence", required=True)

    claim_parser = subparsers.add_parser("claim-generation")
    _add_relay_mutation(claim_parser)
    claim_parser.add_argument("--effective-reasoning-effort", required=True)

    consume_parser = subparsers.add_parser("consume-generation")
    _add_relay_mutation(consume_parser)

    returned_parser = subparsers.add_parser("record-returned")
    _add_relay_mutation(returned_parser)
    returned_parser.add_argument("--result", required=True)

    unknown_parser = subparsers.add_parser("record-unknown")
    _add_relay_mutation(unknown_parser)
    unknown_parser.add_argument("--evidence", required=True)

    protected_stop_parser = subparsers.add_parser(
        "record-protected-stop"
    )
    _add_relay_mutation(protected_stop_parser)
    protected_stop_parser.add_argument(
        "--disposition",
        choices=(
            "human_gate",
            "integrity_stop",
            "validation_failed",
            "capability_blocked",
        ),
        required=True,
    )
    protected_stop_parser.add_argument("--reason-code", required=True)
    protected_stop_parser.add_argument("--evidence", required=True)

    receipt_parser = subparsers.add_parser("finalize-receipt")
    _add_relay_mutation(receipt_parser)
    receipt_parser.add_argument(
        "--disposition",
        choices=("completed", "superseded", "validation_failed", "human_gate", "cancelled"),
        required=True,
    )
    receipt_parser.add_argument("--evidence", required=True)

    decide_parser = subparsers.add_parser("verify-and-decide")
    _add_relay_mutation(decide_parser)

    successor_parser = subparsers.add_parser("reserve-successor")
    _add_relay_mutation(successor_parser)

    relay_finalize_parser = subparsers.add_parser("finalize-plan")
    _add_relay_mutation(relay_finalize_parser, generation=False)
    relay_finalize_parser.add_argument("--completion-report", required=True)

    reconcile_dispatch_parser = subparsers.add_parser("reconcile-dispatch")
    _add_relay_mutation(reconcile_dispatch_parser)
    reconcile_dispatch_parser.add_argument("--matches", required=True)

    abandon_parser = subparsers.add_parser("abandon-unconsumed")
    _add_relay_mutation(abandon_parser)
    abandon_parser.add_argument("--proof", required=True)

    reconcile_consumed_parser = subparsers.add_parser("reconcile-consumed")
    _add_relay_mutation(reconcile_consumed_parser)
    reconcile_consumed_parser.add_argument("--direct-result")

    cancel_parser = subparsers.add_parser("cancel")
    _add_relay_mutation(cancel_parser, generation=False)
    cancel_parser.add_argument("--reason", required=True)
    cancel_parser.add_argument("--authority-reference", required=True)

    prepare_parser = subparsers.add_parser("prepare")
    _add_prepare_fields(prepare_parser)

    bootstrap_parser = subparsers.add_parser(
        "bootstrap-website-packet"
    )
    _add_plan_source(bootstrap_parser)
    _add_control_cas(bootstrap_parser)
    bootstrap_parser.add_argument("--task-id", required=True)
    bootstrap_parser.add_argument(
        "--authorization-message", required=True
    )
    bootstrap_parser.add_argument(
        "--authorization-evidence-ref", required=True
    )
    bootstrap_parser.add_argument("--timestamp")

    complete_bootstrap_parser = subparsers.add_parser(
        "complete-bootstrap-website-packet"
    )
    _add_plan_source(complete_bootstrap_parser)
    _add_control_cas(complete_bootstrap_parser)
    complete_bootstrap_parser.add_argument("--task-id", required=True)
    complete_bootstrap_parser.add_argument(
        "--authorization-evidence-ref", required=True
    )
    complete_bootstrap_parser.add_argument(
        "--validator-result",
        action="append",
        required=True,
        help="Required validator result in ID=pass form.",
    )
    complete_bootstrap_parser.add_argument(
        "--changed-file", action="append", required=True
    )
    complete_bootstrap_parser.add_argument(
        "--completion-summary", required=True
    )
    complete_bootstrap_parser.add_argument("--timestamp")

    prepare_finalize_parser = subparsers.add_parser(
        "prepare-finalize-plan"
    )
    _add_mutation_cas(prepare_finalize_parser)
    prepare_finalize_parser.add_argument("--plan-id", required=True)
    prepare_finalize_parser.add_argument(
        "--current-holder-thread-id", required=True
    )
    prepare_finalize_parser.add_argument("--timestamp")
    _add_legacy_profile(prepare_finalize_parser)

    finalize_parser = subparsers.add_parser("legacy-finalize-plan")
    _add_mutation_cas(finalize_parser)
    finalize_parser.add_argument("--plan-id", required=True)
    finalize_parser.add_argument(
        "--current-holder-thread-id", required=True
    )
    finalize_parser.add_argument(
        "--completion-report", required=True
    )
    finalize_parser.add_argument(
        "--completion-report-sha256", required=True
    )
    finalize_parser.add_argument("--timestamp")
    _add_legacy_profile(finalize_parser)

    activate_parser = subparsers.add_parser("activate")
    _add_prepare_fields(activate_parser)
    _add_mutation_cas(activate_parser)
    activate_parser.add_argument(
        "--acceptance-basis-sha256",
        required=True,
    )
    activate_parser.add_argument(
        "--acceptance-message",
        required=True,
    )
    activate_parser.add_argument(
        "--acceptance-evidence-ref",
        required=True,
    )
    activate_parser.add_argument("--timestamp")
    _add_legacy_profile(activate_parser)

    adopt_parser = subparsers.add_parser("adopt-worker")
    _add_mutation_cas(adopt_parser)
    adopt_parser.add_argument("--plan-id", required=True)
    adopt_parser.add_argument(
        "--creation-status",
        choices=("returned", "ambiguous", "timeout", "failed"),
        required=True,
    )
    adopt_parser.add_argument("--codex-task-id")
    adopt_parser.add_argument("--effective-reasoning-effort")
    adopt_parser.add_argument("--profile-evidence-ref")
    adopt_parser.add_argument("--timestamp")
    _add_legacy_profile(adopt_parser)

    worker_prepare_parser = subparsers.add_parser("worker-prepare")
    _add_mutation_cas(worker_prepare_parser)
    worker_prepare_parser.add_argument("--plan-id", required=True)
    worker_prepare_parser.add_argument(
        "--current-thread-id", required=True
    )
    worker_prepare_parser.add_argument("--timestamp")
    _add_legacy_profile(worker_prepare_parser)

    worker_consume_parser = subparsers.add_parser("worker-consume")
    _add_mutation_cas(worker_consume_parser)
    _add_plan_source(worker_consume_parser)
    worker_consume_parser.add_argument("--plan-id", required=True)
    worker_consume_parser.add_argument(
        "--current-thread-id", required=True
    )
    worker_consume_parser.add_argument("--timestamp")
    _add_legacy_profile(worker_consume_parser)

    worker_finalize_parser = subparsers.add_parser("worker-finalize")
    _add_mutation_cas(worker_finalize_parser)
    _add_plan_source(worker_finalize_parser)
    worker_finalize_parser.add_argument("--plan-id", required=True)
    worker_finalize_parser.add_argument(
        "--current-thread-id", required=True
    )
    worker_finalize_parser.add_argument("--timestamp")
    _add_legacy_profile(worker_finalize_parser)

    worker_fail_parser = subparsers.add_parser("worker-fail")
    _add_mutation_cas(worker_fail_parser)
    _add_plan_source(worker_fail_parser)
    worker_fail_parser.add_argument("--plan-id", required=True)
    worker_fail_parser.add_argument(
        "--current-thread-id", required=True
    )
    worker_fail_parser.add_argument(
        "--validator-result",
        action="append",
        required=True,
        help="Required validator result in ID=pass or ID=fail form.",
    )
    worker_fail_parser.add_argument("--failure-summary", required=True)
    worker_fail_parser.add_argument("--timestamp")
    _add_legacy_profile(worker_fail_parser)

    worker_unknown_parser = subparsers.add_parser("worker-unknown")
    _add_mutation_cas(worker_unknown_parser)
    worker_unknown_parser.add_argument("--plan-id", required=True)
    worker_unknown_parser.add_argument(
        "--current-thread-id", required=True
    )
    worker_unknown_parser.add_argument(
        "--reason-code",
        default="plan_worker.continue_outcome_unknown",
    )
    worker_unknown_parser.add_argument("--timestamp")
    _add_legacy_profile(worker_unknown_parser)

    next_parser = subparsers.add_parser("reserve-next")
    _add_mutation_cas(next_parser)
    _add_plan_source(next_parser)
    next_parser.add_argument("--plan-id", required=True)
    next_parser.add_argument(
        "--coordinator-thread-id", required=True
    )
    next_parser.add_argument("--timestamp")
    _add_legacy_profile(next_parser)

    recover_parser = subparsers.add_parser("recover")
    _add_mutation_cas(recover_parser)
    recover_parser.add_argument("--plan-id", required=True)
    recover_parser.add_argument(
        "--coordinator-thread-id", required=True
    )
    _add_legacy_profile(recover_parser)
    return parser


def _repo_root(arguments: argparse.Namespace) -> Path:
    return Path(arguments.repo_root).expanduser().resolve(strict=True)


def dispatch(arguments: argparse.Namespace) -> dict[str, Any]:
    root = _repo_root(arguments)
    command = arguments.command
    if command == "summarize":
        return relay_status(run_id=arguments.run_id, repo_root=root)
    if command == "project-chain":
        return relay_chain_projection(
            run_id=arguments.run_id, repo_root=root
        )
    if command == "relay-prepare":
        return prepare_relay(
            plan=_load_json_object(arguments.plan, label="plan"),
            launcher_thread_id=arguments.launcher_thread_id,
            requested_effort=arguments.reasoning_effort,
            repo_root=root,
        )
    if command in {"launch", "activate-relay"}:
        return launch_relay(
            plan=_load_json_object(arguments.plan, label="plan"),
            acceptance=_load_json_object(arguments.acceptance, label="acceptance"),
            expected_control_sha256=arguments.expected_control_sha256,
            launcher_thread_id=arguments.launcher_thread_id,
            requested_effort=arguments.reasoning_effort,
            run_id=arguments.run_id,
            repo_root=root,
        )
    if command in {"record-successor", "adopt-successor"}:
        common = _relay_common(arguments)
        common["owner_token"] = common.pop("handoff_token")
        return record_successor(
            **common,
            child_thread_id=arguments.child_thread_id,
            provider_response=_load_json_object(
                arguments.provider_response, label="provider response"
            ),
            effective_effort=arguments.effective_reasoning_effort,
            repo_root=root,
        )
    if command == "prepare-dispatch":
        common = _relay_common(arguments)
        common["owner_token"] = common.pop("handoff_token")
        return prepare_dispatch(**common, repo_root=root)
    if command == "record-dispatch-ambiguous":
        common = _relay_common(arguments)
        common["owner_token"] = common.pop("handoff_token")
        return record_dispatch_ambiguous(
            **common,
            evidence=_load_json_object(
                arguments.evidence, label="ambiguous dispatch evidence"
            ),
            repo_root=root,
        )
    if command == "claim-generation":
        return claim_generation(
            **_relay_common(arguments),
            effective_effort=arguments.effective_reasoning_effort,
            repo_root=root,
        )
    if command == "consume-generation":
        return consume_generation(**_relay_common(arguments), repo_root=root)
    if command == "record-returned":
        return record_returned(
            **_relay_common(arguments),
            result=_load_json_object(arguments.result, label="task result"),
            repo_root=root,
        )
    if command == "record-unknown":
        return record_unknown(
            **_relay_common(arguments),
            evidence=_load_json_object(arguments.evidence, label="unknown evidence"),
            repo_root=root,
        )
    if command == "record-protected-stop":
        return record_protected_stop(
            **_relay_common(arguments),
            disposition=arguments.disposition,
            reason_code=arguments.reason_code,
            evidence=_load_json_object(
                arguments.evidence, label="protected-stop evidence"
            ),
            repo_root=root,
        )
    if command == "finalize-receipt":
        return finalize_receipt(
            **_relay_common(arguments),
            disposition=arguments.disposition,
            evidence=_load_json_object(arguments.evidence, label="receipt evidence"),
            repo_root=root,
        )
    if command == "verify-and-decide":
        return verify_and_decide(**_relay_common(arguments), repo_root=root)
    if command == "reserve-successor":
        return reserve_successor(**_relay_common(arguments), repo_root=root)
    if command == "finalize-plan":
        return finalize_relay_plan(
            run_id=arguments.run_id,
            expected_revision=arguments.expected_plan_revision,
            expected_control_sha256=arguments.expected_control_sha256,
            current_thread_id=arguments.current_thread_id,
            handoff_token=arguments.handoff_token,
            report=_load_json_object(
                arguments.completion_report, label="completion report"
            ),
            repo_root=root,
        )
    if command == "reconcile-dispatch":
        matches = json.loads(Path(arguments.matches).read_text(encoding="utf-8"))
        if not isinstance(matches, list) or any(not isinstance(item, dict) for item in matches):
            raise WebsiteRelayAdapterError(
                "dispatch matches must be one JSON array of objects",
                reason_code="relay.request_invalid",
            )
        common = _relay_common(arguments)
        common["owner_token"] = common.pop("handoff_token")
        return reconcile_dispatch(**common, matches=matches, repo_root=root)
    if command == "abandon-unconsumed":
        return abandon_unconsumed(
            **_relay_common(arguments),
            proof=_load_json_object(arguments.proof, label="non-consumption proof"),
            repo_root=root,
        )
    if command == "reconcile-consumed":
        result = (
            None
            if arguments.direct_result is None
            else _load_json_object(arguments.direct_result, label="direct result")
        )
        return reconcile_consumed(
            **_relay_common(arguments), direct_result=result, repo_root=root
        )
    if command == "cancel":
        return cancel_relay(
            run_id=arguments.run_id,
            expected_revision=arguments.expected_plan_revision,
            expected_control_sha256=arguments.expected_control_sha256,
            current_thread_id=arguments.current_thread_id,
            handoff_token=arguments.handoff_token,
            reason=arguments.reason,
            authority_reference=arguments.authority_reference,
            repo_root=root,
        )
    if command == "status":
        return status(plan_id=arguments.plan_id, repo_root=root)
    if command == "prepare":
        return prepare_plan(
            plan_path=arguments.plan,
            binding_path=arguments.binding,
            goal_text=arguments.goal,
            reasoning_effort=arguments.reasoning_effort,
            current_thread_id=arguments.current_thread_id,
            current_profile_evidence_ref=(
                arguments.current_profile_evidence_ref
            ),
            repo_root=root,
        ).as_dict()
    if command == "bootstrap-website-packet":
        return bootstrap_website_packet(
            plan_path=arguments.plan,
            binding_path=arguments.binding,
            task_id=arguments.task_id,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            authorization_message=arguments.authorization_message,
            authorization_evidence_ref=(
                arguments.authorization_evidence_ref
            ),
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "complete-bootstrap-website-packet":
        validator_results: dict[str, str] = {}
        for item in arguments.validator_result:
            validator_id, separator, validator_status = item.rpartition("=")
            if not separator or validator_id in validator_results:
                raise WebsitePlanAdapterError(
                    "validator results must use unique ID=STATUS values",
                    reason_code="plan.validation_failed",
                )
            validator_results[validator_id] = validator_status
        return complete_bootstrap_website_packet(
            plan_path=arguments.plan,
            binding_path=arguments.binding,
            task_id=arguments.task_id,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            authorization_evidence_ref=(
                arguments.authorization_evidence_ref
            ),
            validator_results=validator_results,
            changed_files=arguments.changed_file,
            completion_summary=arguments.completion_summary,
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "prepare-finalize-plan":
        return prepare_plan_finalization(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            current_holder_thread_id=(
                arguments.current_holder_thread_id
            ),
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "legacy-finalize-plan":
        return finalize_plan(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            current_holder_thread_id=(
                arguments.current_holder_thread_id
            ),
            completion_report_path=arguments.completion_report,
            expected_completion_report_sha256=(
                arguments.completion_report_sha256
            ),
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "activate":
        prepared = prepare_plan(
            plan_path=arguments.plan,
            binding_path=arguments.binding,
            goal_text=arguments.goal,
            reasoning_effort=arguments.reasoning_effort,
            current_thread_id=arguments.current_thread_id,
            current_profile_evidence_ref=(
                arguments.current_profile_evidence_ref
            ),
            repo_root=root,
        )
        return activate_plan(
            prepared=prepared,
            acceptance_basis_sha256=(
                arguments.acceptance_basis_sha256
            ),
            acceptance_message=arguments.acceptance_message,
            acceptance_evidence_ref=(
                arguments.acceptance_evidence_ref
            ),
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            timestamp=arguments.timestamp,
        )
    if command == "adopt-worker":
        return adopt_worker(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            creation_status=arguments.creation_status,
            codex_task_id=arguments.codex_task_id,
            effective_reasoning_effort=(
                arguments.effective_reasoning_effort
            ),
            profile_evidence_ref=arguments.profile_evidence_ref,
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "worker-prepare":
        return worker_prepare(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            current_thread_id=arguments.current_thread_id,
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "worker-consume":
        return worker_consume(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            current_thread_id=arguments.current_thread_id,
            plan_path=arguments.plan,
            binding_path=arguments.binding,
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "worker-finalize":
        return worker_finalize(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            current_thread_id=arguments.current_thread_id,
            plan_path=arguments.plan,
            binding_path=arguments.binding,
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "worker-fail":
        validator_results: dict[str, str] = {}
        for item in arguments.validator_result:
            validator_id, separator, validator_status = item.rpartition("=")
            if not separator or validator_id in validator_results:
                raise WebsitePlanAdapterError(
                    "validator results must use unique ID=STATUS values",
                    reason_code="plan.validation_failed",
                )
            validator_results[validator_id] = validator_status
        return worker_fail(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            current_thread_id=arguments.current_thread_id,
            plan_path=arguments.plan,
            binding_path=arguments.binding,
            validator_results=validator_results,
            failure_summary=arguments.failure_summary,
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "worker-unknown":
        return worker_unknown(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            current_thread_id=arguments.current_thread_id,
            reason_code=arguments.reason_code,
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "reserve-next":
        return reserve_next(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            coordinator_thread_id=arguments.coordinator_thread_id,
            plan_path=arguments.plan,
            binding_path=arguments.binding,
            repo_root=root,
            timestamp=arguments.timestamp,
        )
    if command == "recover":
        return recover(
            plan_id=arguments.plan_id,
            expected_plan_revision=arguments.expected_plan_revision,
            expected_control_sha256=(
                arguments.expected_control_sha256
            ),
            coordinator_thread_id=arguments.coordinator_thread_id,
            repo_root=root,
        )
    raise AssertionError(f"unhandled command: {command}")


def _error_payload(error: Exception) -> dict[str, Any]:
    if isinstance(error, (WebsitePlanAdapterError, WebsiteRelayAdapterError)):
        return error.as_dict()
    details = getattr(error, "details", {})
    reason_code = (
        details.get("reason_code")
        if isinstance(details, dict)
        else None
    )
    return {
        "status": "protected_stop",
        "reason_code": reason_code or "plan.adapter_error",
        "message": str(error),
        "details": details if isinstance(details, dict) else {},
    }


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        result = dispatch(arguments)
    except (WebsitePlanAdapterError, WebsiteRelayAdapterError, AgentJobControlError) as error:
        sys.stdout.write(canonical_json(_error_payload(error)))
        return 2
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        sys.stdout.write(canonical_json(_error_payload(error)))
        return 2
    sys.stdout.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
