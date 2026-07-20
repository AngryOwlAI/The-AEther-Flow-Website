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
    canonical_json,
    prepare_plan,
    recover,
    reserve_next,
    status,
    worker_consume,
    worker_finalize,
    worker_prepare,
    worker_unknown,
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Coordinate one accepted canonical plan through website "
            "implementation control."
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

    prepare_parser = subparsers.add_parser("prepare")
    _add_prepare_fields(prepare_parser)

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

    worker_prepare_parser = subparsers.add_parser("worker-prepare")
    _add_mutation_cas(worker_prepare_parser)
    worker_prepare_parser.add_argument("--plan-id", required=True)
    worker_prepare_parser.add_argument(
        "--current-thread-id", required=True
    )
    worker_prepare_parser.add_argument("--timestamp")

    worker_consume_parser = subparsers.add_parser("worker-consume")
    _add_mutation_cas(worker_consume_parser)
    _add_plan_source(worker_consume_parser)
    worker_consume_parser.add_argument("--plan-id", required=True)
    worker_consume_parser.add_argument(
        "--current-thread-id", required=True
    )
    worker_consume_parser.add_argument("--timestamp")

    worker_finalize_parser = subparsers.add_parser("worker-finalize")
    _add_mutation_cas(worker_finalize_parser)
    _add_plan_source(worker_finalize_parser)
    worker_finalize_parser.add_argument("--plan-id", required=True)
    worker_finalize_parser.add_argument(
        "--current-thread-id", required=True
    )
    worker_finalize_parser.add_argument("--timestamp")

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

    next_parser = subparsers.add_parser("reserve-next")
    _add_mutation_cas(next_parser)
    _add_plan_source(next_parser)
    next_parser.add_argument("--plan-id", required=True)
    next_parser.add_argument(
        "--coordinator-thread-id", required=True
    )
    next_parser.add_argument("--timestamp")

    recover_parser = subparsers.add_parser("recover")
    _add_mutation_cas(recover_parser)
    recover_parser.add_argument("--plan-id", required=True)
    recover_parser.add_argument(
        "--coordinator-thread-id", required=True
    )
    return parser


def _repo_root(arguments: argparse.Namespace) -> Path:
    return Path(arguments.repo_root).expanduser().resolve(strict=True)


def dispatch(arguments: argparse.Namespace) -> dict[str, Any]:
    root = _repo_root(arguments)
    command = arguments.command
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
    if isinstance(error, WebsitePlanAdapterError):
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
    except (WebsitePlanAdapterError, AgentJobControlError) as error:
        sys.stdout.write(canonical_json(_error_payload(error)))
        return 2
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        sys.stdout.write(canonical_json(_error_payload(error)))
        return 2
    sys.stdout.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
