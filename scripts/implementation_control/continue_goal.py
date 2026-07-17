#!/usr/bin/env python3
"""Project facade for the experimental governed continuation relay.

The CLI intentionally separates reservation, activation, one bounded website
continuation, and recovery. It cannot create a Codex task by itself; a project
skill must use the host task tools or preserve the protected manual handoff.
"""

from __future__ import annotations

import argparse
import copy
import json
import secrets
import sys
from pathlib import Path
from typing import Any, Mapping

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[2]
VENDOR_SCRIPTS = REPO_ROOT / ".agents/skills/agentjob-control/scripts"
if str(VENDOR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(VENDOR_SCRIPTS))

from agentjob_runtime.adapters.thread_manual import (  # noqa: E402
    ManualThreadProvider,
    adopt_manual_successor,
)
from agentjob_runtime.errors import AgentJobControlError, StateConflict  # noqa: E402
from agentjob_runtime.fingerprinting.canonical import FingerprintResult  # noqa: E402
from agentjob_runtime.goal.decide import (  # noqa: E402
    decide_and_reserve_successor,
    decide_generation,
)
from agentjob_runtime.goal.execution import (  # noqa: E402
    claim_generation,
    consume_invocation,
    guard_precheck,
    pre_execution_stop,
    record_invocation_returned,
    record_invocation_unknown,
)
from agentjob_runtime.goal.launcher import (  # noqa: E402
    build_continuation_envelope,
    build_worker_prompt,
    launch_goal,
)
from agentjob_runtime.goal.model import fingerprint_status  # noqa: E402
from agentjob_runtime.goal.recovery import (  # noqa: E402
    begin_recovery,
    cancel_relay,
)
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore  # noqa: E402
from agentjob_runtime.goal.verify import verify_generation  # noqa: E402
from agentjob_runtime.goal.worker import (  # noqa: E402
    _result_stop_reason,
    _validate_continue_result,
    _validate_envelope,
)
from agentjob_runtime.records.canonical import (  # noqa: E402
    content_sha256,
    load_structured,
)

from goal_relay_adapter import (  # noqa: E402
    GoalRelayAdapterError,
    LOCAL_STATE_RELATIVE,
    WebsiteSnapshot,
    activation_receipt_path,
    build_continue_result,
    build_direct_evidence,
    capture_snapshot,
    checkpoint_is_authorized,
    pre_execution_block,
    read_protected_json,
    repository_binding,
    verify_activation_receipt,
    write_activation_receipt,
    write_protected_json,
)


STATE_DB_RELATIVE = LOCAL_STATE_RELATIVE / "goal-state.sqlite3"
MANUAL_ROOT_RELATIVE = LOCAL_STATE_RELATIVE / "manual"
INVOCATION_ROOT_RELATIVE = LOCAL_STATE_RELATIVE / "invocations"
OUTCOME_ROOT_RELATIVE = LOCAL_STATE_RELATIVE / "outcomes"
DELIVERY_ROOT_RELATIVE = LOCAL_STATE_RELATIVE / "delivery-recovery"
CAPABILITIES = {
    "agentjob_control": True,
    "goal_state": True,
    "continuation_envelope": True,
    "repository_provider": True,
    "thread_provider": True,
}


def _json_file(path: str | Path) -> Any:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    return value


def _mapping_file(path: str | Path) -> dict[str, Any]:
    value = _json_file(path)
    if not isinstance(value, dict):
        raise GoalRelayAdapterError(f"expected one JSON object: {path}")
    return value


def _goal_text(args: argparse.Namespace) -> str:
    if bool(args.goal_text) == bool(args.goal_file):
        raise GoalRelayAdapterError(
            "provide exactly one of --goal-text or --goal-file"
        )
    if args.goal_file:
        return Path(args.goal_file).read_text(encoding="utf-8")
    return str(args.goal_text)


def _store(*, read_only: bool = False) -> SQLiteGoalStore:
    path = REPO_ROOT / STATE_DB_RELATIVE
    return SQLiteGoalStore(
        path,
        auto_migrate=not read_only,
        read_only=read_only,
    )


def _goal_summary(record: Mapping[str, Any]) -> dict[str, Any]:
    lease = record["state"].get("active_lease")
    return {
        "goal_id": record["goal_id"],
        "revision": record["state"]["revision"],
        "phase": record["state"]["phase"],
        "current_generation": record["state"]["current_generation"],
        "passes_consumed": record["state"]["passes_consumed"],
        "goal_evaluation": record["state"]["goal_evaluation"],
        "terminal_reason": record["state"]["terminal_reason"],
        "lease_holder_kind": lease["holder_kind"] if lease else None,
        "generations": [
            {
                "generation": entry["generation"],
                "phase": entry["phase"],
                "invocation_state": entry["invocation_state"],
                "invocation_consumed": entry["invocation_consumed"],
                "successor_thread_id": entry["successor_thread_id"],
                "receipt_finalized": entry["finalized_receipt_hash"] is not None,
            }
            for _, entry in sorted(
                record["generations"].items(), key=lambda item: int(item[0])
            )
        ],
    }


def _manual_directory(goal_id: str, generation: int) -> Path:
    return (
        REPO_ROOT
        / MANUAL_ROOT_RELATIVE
        / goal_id
        / f"generation-{generation}"
    )


def _manual_artifacts(goal_id: str, generation: int) -> dict[str, str]:
    directory = _manual_directory(goal_id, generation)
    return {
        "envelope_path": str(
            (directory / "continuation-envelope.json").relative_to(REPO_ROOT)
        ),
        "activation_prompt_path": str(
            (directory / "new-thread-prompt.txt").relative_to(REPO_ROOT)
        ),
        "provider_receipt_path": str(
            (directory / "provider-receipt.json").relative_to(REPO_ROOT)
        ),
    }


def _reservation_prompt(goal_id: str, generation: int) -> str:
    return (
        "Reserve this fresh Codex task for governed continuation only. "
        f"Goal {goal_id}, generation {generation}. "
        "Do not execute project work, invoke a skill, or alter files. "
        "Wait for the token-bound activation message from the predecessor."
    )


def _snapshot_from_dict(value: Mapping[str, Any]) -> WebsiteSnapshot:
    return WebsiteSnapshot(
        repo_root=REPO_ROOT,
        resolver=copy.deepcopy(dict(value["resolver"])),
        resolver_exit_code=int(value["resolver_exit_code"]),
        git=copy.deepcopy(dict(value["git"])),
        record_paths=copy.deepcopy(dict(value["record_paths"])),
        record_hashes=copy.deepcopy(dict(value["record_hashes"])),
        record_metadata=copy.deepcopy(dict(value["record_metadata"])),
        fingerprint=str(value["fingerprint"]),
        source_authority=copy.deepcopy(dict(value["source_authority"])),
    )


def _invocation_path(goal_id: str, generation: int) -> Path:
    return (
        REPO_ROOT
        / INVOCATION_ROOT_RELATIVE
        / goal_id
        / f"generation-{generation}.json"
    )


def _outcome_path(goal_id: str, generation: int, kind: str) -> Path:
    return (
        REPO_ROOT
        / OUTCOME_ROOT_RELATIVE
        / goal_id
        / f"generation-{generation}-{kind}.json"
    )


def _load_envelope(path: str | Path) -> dict[str, Any]:
    value = load_structured(path)
    if not isinstance(value, dict):
        raise GoalRelayAdapterError("continuation envelope must be a JSON object")
    return value


def _repository_matches_envelope(
    snapshot: WebsiteSnapshot,
    envelope: Mapping[str, Any],
) -> bool:
    binding = envelope.get("repository_binding")
    if not isinstance(binding, Mapping):
        return False
    current = repository_binding(snapshot)
    for key in ("project_id", "root", "worktree", "branch", "git_common_dir"):
        if binding.get(key) != current.get(key):
            return False
    canonical_state = envelope.get("canonical_state")
    return bool(
        isinstance(canonical_state, Mapping)
        and canonical_state.get("fingerprint") == snapshot.fingerprint
    )


def command_launch(args: argparse.Namespace) -> dict[str, Any]:
    store = _store()
    if args.phase == "reserve":
        snapshot = capture_snapshot(REPO_ROOT)
        blocked, reason = pre_execution_block(snapshot)
        if blocked:
            return {
                "status": blocked,
                "reason_code": reason,
                "execution_performed": False,
                "agent_jobs_executed": 0,
            }
        contract = _mapping_file(args.completion_contract)
        guards = _mapping_file(args.guards)
        provider = ManualThreadProvider(
            REPO_ROOT,
            local_root=MANUAL_ROOT_RELATIVE,
            current_thread_id=args.predecessor_task_id,
        )
        binding = repository_binding(snapshot)
        summary = launch_goal(
            store,
            goal_text=_goal_text(args),
            completion_contract=contract,
            guards=guards,
            repository_binding=binding,
            repository_observation=dict(binding),
            initial_fingerprint=snapshot.fingerprint,
            authorization={"fresh_recursive_threads_explicitly_requested": True},
            capabilities=CAPABILITIES,
            provider=provider,
            predecessor_thread_id=args.predecessor_task_id,
            predecessor_handoff_id=(
                snapshot.record_metadata.get("handoff", {}).get("record_id")
            ),
            canonical_state={
                "fingerprint": snapshot.fingerprint,
                "active_task_id": snapshot.record_metadata.get("task", {}).get(
                    "record_id"
                ),
                "current_decision_id": None,
                "current_job_id": snapshot.record_metadata.get("job", {}).get(
                    "record_id"
                ),
            },
            progress_summary="The goal was reserved without executing project work.",
            remaining_work=str(
                snapshot.resolver.get("next_recommended_action", {}).get("summary")
                or "Execute one bounded website continuation."
            ),
            goal_id=args.goal_id,
        )
        result = summary.as_dict()
        result.update(_manual_artifacts(summary.goal_id, summary.generation))
        result.update(
            {
                "reservation_prompt": _reservation_prompt(
                    summary.goal_id, summary.generation
                ),
                "next_action": (
                    "Create exactly one fresh Codex task with reservation_prompt, "
                    "then run launch --phase adopt with the returned task ID."
                ),
            }
        )
        return result

    envelope_path = _manual_directory(args.goal_id, args.generation) / (
        "continuation-envelope.json"
    )
    envelope = _load_envelope(envelope_path)
    record = adopt_manual_successor(
        store,
        project_root=REPO_ROOT,
        local_root=MANUAL_ROOT_RELATIVE,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        handoff_token=str(envelope["handoff_token"]),
        envelope_sha256=str(args.envelope_sha256),
        successor_thread_id=args.adopt_task_id,
    )
    return {
        "status": "successor_recorded",
        **_goal_summary(record),
        **_manual_artifacts(args.goal_id, args.generation),
        "next_action": (
            "Send the exact activation_prompt_path contents to the recorded fresh "
            "task once, then stop this predecessor."
        ),
    }


def command_status(args: argparse.Namespace) -> dict[str, Any]:
    path = REPO_ROOT / STATE_DB_RELATIVE
    snapshot = capture_snapshot(REPO_ROOT)
    if not path.is_file():
        return {
            "status": "no_goal_state",
            "website": snapshot.as_dict(),
            "execution_performed": False,
        }
    store = _store(read_only=True)
    if args.goal_id:
        goals = [_goal_summary(store.load_goal(args.goal_id))]
    else:
        goals = [
            _goal_summary(store.load_goal(item["goal_id"]))
            for item in store.list_goals()
        ]
    return {
        "status": "pass",
        "goals": goals,
        "website": snapshot.as_dict(),
        "execution_performed": False,
    }


def _prepare_observations(
    snapshot: WebsiteSnapshot,
    envelope: Mapping[str, Any],
) -> dict[str, bool]:
    blocked, _ = pre_execution_block(snapshot)
    return {
        "human_gate_clear": blocked != "human_gate_required",
        "validation_clear": snapshot.resolver.get("status") == "ready",
        "checkpoint_clear": checkpoint_is_authorized(snapshot),
        "dirty_state_expected": True,
        "capabilities_available": True,
        "repository_matches": _repository_matches_envelope(snapshot, envelope),
    }


def worker_prepare(args: argparse.Namespace) -> dict[str, Any]:
    store = _store()
    envelope = _load_envelope(args.envelope)
    envelope_hash = content_sha256(envelope)
    if args.envelope_sha256 and args.envelope_sha256 != envelope_hash:
        raise StateConflict("worker envelope hash differs from supplied hash")
    _validate_envelope(
        store,
        envelope=envelope,
        envelope_sha256=envelope_hash,
        expected_revision=args.expected_revision,
        current_thread_id=args.current_task_id,
    )
    snapshot = capture_snapshot(REPO_ROOT)
    if not _repository_matches_envelope(snapshot, envelope):
        raise GoalRelayAdapterError(
            "repository or canonical website fingerprint differs from the envelope"
        )
    goal_id = str(envelope["goal_id"])
    generation = int(envelope["generation"])
    receipt_path = write_activation_receipt(
        snapshot,
        goal_id=goal_id,
        generation=generation,
        envelope_sha256=envelope_hash,
    )
    claim_token = secrets.token_hex(24)
    claimed = claim_generation(
        store,
        goal_id=goal_id,
        expected_revision=args.expected_revision,
        generation=generation,
        handoff_token=str(envelope["handoff_token"]),
        idempotency_key=str(envelope["idempotency_key"]),
        successor_thread_id=args.current_task_id,
        claim_token=claim_token,
    )
    observations = _prepare_observations(snapshot, envelope)
    stops = guard_precheck(claimed, observations=observations)
    if stops:
        stopped = pre_execution_stop(
            store,
            goal_id=goal_id,
            expected_revision=int(claimed["state"]["revision"]),
            generation=generation,
            claim_token=claim_token,
            stop_reason=stops[0],
            evidence={
                "activation_receipt": str(receipt_path.relative_to(REPO_ROOT))
            },
        )
        result = build_continue_result(snapshot)
        write_protected_json(
            _outcome_path(goal_id, generation, "pre-execution-stop"),
            {
                "schema_version": "sys4ai.website-worker-outcome.v1",
                "status": "pre_execution_stop",
                "stop_reason": stops[0],
                "continue_result": result,
                "goal": _goal_summary(stopped),
            },
        )
        return {
            "status": "pre_execution_stop",
            "stop_reason": stops[0],
            "continue_invocations": 0,
            "agent_jobs_executed": 0,
            "goal": _goal_summary(stopped),
            "continue_result": result,
        }

    current = capture_snapshot(REPO_ROOT)
    receipt = read_protected_json(receipt_path)
    verify_activation_receipt(current, receipt)
    consumed = consume_invocation(
        store,
        goal_id=goal_id,
        expected_revision=int(claimed["state"]["revision"]),
        generation=generation,
        claim_token=claim_token,
        observations=observations,
    )
    invocation_path = _invocation_path(goal_id, generation)
    write_protected_json(
        invocation_path,
        {
            "schema_version": "sys4ai.website-worker-invocation.v1",
            "goal_id": goal_id,
            "generation": generation,
            "current_task_id": args.current_task_id,
            "claim_token": claim_token,
            "envelope_path": str(Path(args.envelope).resolve()),
            "envelope_sha256": envelope_hash,
            "activation_receipt_path": str(receipt_path.relative_to(REPO_ROOT)),
            "state_revision": int(consumed["state"]["revision"]),
            "before_snapshot": snapshot.as_dict(),
        },
    )
    return {
        "status": "continue_authorized",
        "goal_id": goal_id,
        "generation": generation,
        "invocation_record": str(invocation_path.relative_to(REPO_ROOT)),
        "continue_invocations_authorized": 1,
        "next_action": (
            "Invoke the project-local continue skill exactly once. After it returns "
            "and its bounded packet is complete, run worker --phase finalize."
        ),
    }


def _contract_results(path: str | Path) -> list[dict[str, Any]]:
    value = _json_file(path)
    if isinstance(value, Mapping):
        value = value.get("completion_contract_results")
    if not isinstance(value, list) or not all(
        isinstance(item, dict) for item in value
    ):
        raise GoalRelayAdapterError(
            "completion contract results must be a JSON list of objects"
        )
    return [dict(item) for item in value]


def _finalize_successor_intent(
    record: Mapping[str, Any],
    *,
    current_task_id: str,
    result: Mapping[str, Any],
    direct_evidence: Mapping[str, Any],
) -> dict[str, Any]:
    generation = int(record["state"]["current_generation"])
    entry = record["generations"][str(generation)]
    envelope = build_continuation_envelope(
        record,
        predecessor_thread_id=current_task_id,
        predecessor_handoff_id=result.get("handoff_id"),
        canonical_state={
            "fingerprint": result["repository_fingerprint_after"],
            "active_task_id": result.get("task_id"),
            "current_decision_id": result.get("decision_id"),
            "current_job_id": result.get("job_id"),
        },
        progress_summary=str(direct_evidence["progress_summary"]),
        remaining_work=str(direct_evidence["remaining_work"]),
    )
    prompt = build_worker_prompt(
        envelope,
        project_root=str(REPO_ROOT),
        expected_revision=int(record["state"]["revision"]) + 1,
    )
    provider = ManualThreadProvider(
        REPO_ROOT,
        local_root=MANUAL_ROOT_RELATIVE,
        current_thread_id=current_task_id,
    )
    provider_result = provider.create_thread(
        prompt=prompt,
        envelope=envelope,
        idempotency_key=str(entry["idempotency_key"]),
    )
    if provider_result.status != "manual_pending":
        raise GoalRelayAdapterError("manual successor reservation was not retained")
    return {
        "goal_id": record["goal_id"],
        "generation": generation,
        "envelope_sha256": content_sha256(envelope),
        **_manual_artifacts(str(record["goal_id"]), generation),
        "reservation_prompt": _reservation_prompt(
            str(record["goal_id"]), generation
        ),
    }


def worker_finalize(args: argparse.Namespace) -> dict[str, Any]:
    invocation = read_protected_json(
        _invocation_path(args.goal_id, args.generation)
    )
    if invocation.get("current_task_id") != args.current_task_id:
        raise StateConflict("finalizer task does not match consumed generation")
    store = _store()
    before = _snapshot_from_dict(invocation["before_snapshot"])
    after = capture_snapshot(REPO_ROOT)
    result = build_continue_result(
        before,
        after,
        execution_attempted=True,
    )
    findings = _validate_continue_result(result)
    if findings:
        raise GoalRelayAdapterError(
            "website continue result failed portable schema validation: "
            + "; ".join(findings)
        )
    claim_token = str(invocation["claim_token"])
    if (
        result.get("status") == "unknown"
        or result.get("agent_jobs_executed") == "unknown"
    ):
        uncertain = record_invocation_unknown(
            store,
            goal_id=args.goal_id,
            expected_revision=int(invocation["state_revision"]),
            generation=args.generation,
            claim_token=claim_token,
            diagnostic={
                "reason_code": str(result.get("reason_code")),
                "continue_result": result,
            },
        )
        outcome = {
            "schema_version": "sys4ai.website-worker-outcome.v1",
            "status": "recovery_required",
            "continue_result": result,
            "goal": _goal_summary(uncertain),
            "successor": None,
            "next_action": (
                "Inspect recovery evidence and do not invoke continue again for "
                "this consumed generation."
            ),
        }
        write_protected_json(
            _outcome_path(args.goal_id, args.generation, "final"),
            outcome,
        )
        return outcome
    returned = record_invocation_returned(
        store,
        goal_id=args.goal_id,
        expected_revision=int(invocation["state_revision"]),
        generation=args.generation,
        claim_token=claim_token,
        continue_result=result,
    )
    direct_evidence = build_direct_evidence(
        result,
        after,
        completion_contract_results=_contract_results(args.contract_results),
    )
    after_fingerprint = FingerprintResult(
        {"continue_result_sha256": content_sha256(result)},
        after.fingerprint,
        fingerprint_status(
            returned["state"]["canonical_fingerprint_history"],
            after.fingerprint,
        ),
    )
    verified = verify_generation(
        store,
        goal_id=args.goal_id,
        expected_revision=int(returned["state"]["revision"]),
        generation=args.generation,
        claim_token=claim_token,
        continue_result=result,
        after_fingerprint=after_fingerprint,
        direct_evidence=direct_evidence,
    )
    stop_reason = _result_stop_reason(result, direct_evidence)
    if (
        stop_reason is None
        and verified["state"]["goal_evaluation"] == "unmet"
    ):
        if result["status"] in {"blocked", "control_repair_required"}:
            stop_reason = "validation"
        elif result["status"] == "no_action":
            stop_reason = "no_action"
    if stop_reason:
        final = decide_generation(
            store,
            goal_id=args.goal_id,
            expected_revision=int(verified["state"]["revision"]),
            generation=args.generation,
            claim_token=claim_token,
            legal_route_available=False,
            explicit_stop_reason=stop_reason,
        )
        successor = None
    elif (
        verified["state"]["goal_evaluation"] == "unmet"
        and args.legal_route_available
    ):
        final = decide_and_reserve_successor(
            store,
            goal_id=args.goal_id,
            expected_revision=int(verified["state"]["revision"]),
            generation=args.generation,
            claim_token=claim_token,
            predecessor_thread_id=args.current_task_id,
        )
        successor = _finalize_successor_intent(
            final,
            current_task_id=args.current_task_id,
            result=result,
            direct_evidence=direct_evidence,
        )
    else:
        final = decide_generation(
            store,
            goal_id=args.goal_id,
            expected_revision=int(verified["state"]["revision"]),
            generation=args.generation,
            claim_token=claim_token,
            legal_route_available=False,
        )
        successor = None
    outcome = {
        "schema_version": "sys4ai.website-worker-outcome.v1",
        "status": (
            "manual_successor_pending"
            if successor
            else "terminal"
        ),
        "continue_result": result,
        "direct_evidence": direct_evidence,
        "goal": _goal_summary(final),
        "successor": successor,
    }
    write_protected_json(
        _outcome_path(args.goal_id, args.generation, "final"),
        outcome,
    )
    return outcome


def worker_unknown(args: argparse.Namespace) -> dict[str, Any]:
    invocation = read_protected_json(
        _invocation_path(args.goal_id, args.generation)
    )
    if invocation.get("current_task_id") != args.current_task_id:
        raise StateConflict("unknown-outcome reporter task does not match generation")
    store = _store()
    record = record_invocation_unknown(
        store,
        goal_id=args.goal_id,
        expected_revision=int(invocation["state_revision"]),
        generation=args.generation,
        claim_token=str(invocation["claim_token"]),
        diagnostic={
            "reason_code": "website.continue_outcome_ambiguous",
            "evidence": args.diagnostic,
        },
    )
    return {
        "status": "recovery_required",
        "continue_invocations": "unknown",
        "agent_jobs_executed": "unknown",
        "goal": _goal_summary(record),
        "next_action": "Use recover inspect and do not invoke continue again.",
    }


def worker_adopt_successor(args: argparse.Namespace) -> dict[str, Any]:
    store = _store()
    envelope_path = _manual_directory(args.goal_id, args.generation) / (
        "continuation-envelope.json"
    )
    envelope = _load_envelope(envelope_path)
    record = adopt_manual_successor(
        store,
        project_root=REPO_ROOT,
        local_root=MANUAL_ROOT_RELATIVE,
        goal_id=args.goal_id,
        expected_revision=args.expected_revision,
        generation=args.generation,
        handoff_token=str(envelope["handoff_token"]),
        envelope_sha256=args.envelope_sha256,
        successor_thread_id=args.adopt_task_id,
    )
    return {
        "status": "successor_recorded",
        "goal": _goal_summary(record),
        **_manual_artifacts(args.goal_id, args.generation),
        "next_action": (
            "Send activation_prompt_path to the fresh task once and stop this "
            "predecessor immediately."
        ),
    }


def command_worker(args: argparse.Namespace) -> dict[str, Any]:
    if args.phase == "prepare":
        return worker_prepare(args)
    if args.phase == "finalize":
        return worker_finalize(args)
    if args.phase == "unknown":
        return worker_unknown(args)
    return worker_adopt_successor(args)


def command_recover(args: argparse.Namespace) -> dict[str, Any]:
    store = _store(read_only=args.action == "inspect")
    record = store.load_goal(args.goal_id)
    if args.action == "inspect":
        delivery_root = REPO_ROOT / DELIVERY_ROOT_RELATIVE / args.goal_id
        receipts = (
            [
                str(path.relative_to(REPO_ROOT))
                for path in sorted(delivery_root.glob("*.json"))
            ]
            if delivery_root.is_dir()
            else []
        )
        return {
            "status": "recovery_inspection",
            "goal": _goal_summary(record),
            "delivery_recovery_receipts": receipts,
            "execution_performed": False,
        }
    if args.action == "delivery-unknown":
        path = (
            REPO_ROOT
            / DELIVERY_ROOT_RELATIVE
            / args.goal_id
            / f"generation-{args.generation}.json"
        )
        write_protected_json(
            path,
            {
                "schema_version": "sys4ai.website-delivery-recovery.v1",
                "goal_id": args.goal_id,
                "generation": args.generation,
                "status": "activation_delivery_unknown",
                "task_id": args.task_id,
                "evidence": args.diagnostic,
                "retry_allowed": False,
            },
        )
        return {
            "status": "recovery_required",
            "receipt_path": str(path.relative_to(REPO_ROOT)),
            "retry_allowed": False,
        }
    evidence = _mapping_file(args.evidence)
    if args.action == "begin":
        updated = begin_recovery(
            store,
            goal_id=args.goal_id,
            expected_revision=args.expected_revision,
            user_authorization=args.authorization,
            evidence=evidence,
        )
    else:
        updated = cancel_relay(
            store,
            goal_id=args.goal_id,
            expected_revision=args.expected_revision,
            user_authorization=args.authorization,
            evidence=evidence,
        )
    return {
        "status": f"recovery_{args.action}",
        "goal": _goal_summary(updated),
        "execution_performed": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    launch = subparsers.add_parser("launch")
    launch.add_argument("--phase", choices=("reserve", "adopt"), default="reserve")
    launch.add_argument("--goal-text")
    launch.add_argument("--goal-file")
    launch.add_argument("--completion-contract")
    launch.add_argument("--guards")
    launch.add_argument("--predecessor-task-id")
    launch.add_argument("--goal-id")
    launch.add_argument("--generation", type=int)
    launch.add_argument("--expected-revision", type=int)
    launch.add_argument("--envelope-sha256")
    launch.add_argument("--adopt-task-id")

    status = subparsers.add_parser("status")
    status.add_argument("--goal-id")

    worker = subparsers.add_parser("worker")
    worker.add_argument(
        "--phase",
        choices=("prepare", "finalize", "unknown", "adopt-successor"),
        required=True,
    )
    worker.add_argument("--envelope")
    worker.add_argument("--envelope-sha256")
    worker.add_argument("--expected-revision", type=int)
    worker.add_argument("--current-task-id")
    worker.add_argument("--goal-id")
    worker.add_argument("--generation", type=int)
    worker.add_argument("--contract-results")
    worker.add_argument("--legal-route-available", action="store_true")
    worker.add_argument("--diagnostic")
    worker.add_argument("--adopt-task-id")

    recover = subparsers.add_parser("recover")
    recover.add_argument(
        "--action",
        choices=("inspect", "begin", "cancel", "delivery-unknown"),
        default="inspect",
    )
    recover.add_argument("--goal-id", required=True)
    recover.add_argument("--generation", type=int)
    recover.add_argument("--expected-revision", type=int)
    recover.add_argument("--authorization")
    recover.add_argument("--evidence")
    recover.add_argument("--task-id")
    recover.add_argument("--diagnostic")

    return parser


def _require_args(args: argparse.Namespace) -> None:
    if args.command == "launch":
        if args.phase == "reserve":
            required = (
                "completion_contract",
                "guards",
                "predecessor_task_id",
            )
        else:
            required = (
                "goal_id",
                "generation",
                "expected_revision",
                "envelope_sha256",
                "adopt_task_id",
            )
    elif args.command == "worker":
        by_phase = {
            "prepare": (
                "envelope",
                "expected_revision",
                "current_task_id",
            ),
            "finalize": (
                "goal_id",
                "generation",
                "current_task_id",
                "contract_results",
            ),
            "unknown": (
                "goal_id",
                "generation",
                "current_task_id",
                "diagnostic",
            ),
            "adopt-successor": (
                "goal_id",
                "generation",
                "expected_revision",
                "envelope_sha256",
                "adopt_task_id",
            ),
        }
        required = by_phase[args.phase]
    elif args.command == "recover" and args.action != "inspect":
        required = (
            ("goal_id", "generation", "task_id", "diagnostic")
            if args.action == "delivery-unknown"
            else ("goal_id", "expected_revision", "authorization", "evidence")
        )
    else:
        required = ()
    missing = [name for name in required if getattr(args, name, None) in (None, "")]
    if missing:
        raise GoalRelayAdapterError(
            "missing required arguments: " + ", ".join(f"--{name.replace('_', '-')}" for name in missing)
        )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        _require_args(args)
        if args.command == "launch":
            result = command_launch(args)
        elif args.command == "status":
            result = command_status(args)
        elif args.command == "worker":
            result = command_worker(args)
        else:
            result = command_recover(args)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (
        AgentJobControlError,
        GoalRelayAdapterError,
        json.JSONDecodeError,
        OSError,
        ValueError,
    ) as error:
        reason = getattr(error, "code", "website.goal_relay_blocked")
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "reason_code": reason,
                    "message": str(error),
                    "execution_performed": False,
                },
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
