from __future__ import annotations

import copy
import stat
import sys
from argparse import Namespace
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
FACADE_SCRIPTS = REPO_ROOT / "scripts/implementation_control"
VENDOR_SCRIPTS = REPO_ROOT / ".agents/skills/agentjob-control/scripts"
for import_root in (FACADE_SCRIPTS, VENDOR_SCRIPTS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

import continue_goal as facade  # noqa: E402
import goal_relay_adapter as adapter  # noqa: E402
from agentjob_runtime.adapters.thread_manual import ManualThreadProvider  # noqa: E402
from agentjob_runtime.errors import StateConflict  # noqa: E402
from agentjob_runtime.goal.launcher import (  # noqa: E402
    ThreadCreateResult,
    launch_goal,
)
from agentjob_runtime.goal.execution import (  # noqa: E402
    claim_generation,
    consume_invocation,
)
from agentjob_runtime.goal.recovery import begin_recovery  # noqa: E402
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore  # noqa: E402
from agentjob_runtime.goal.worker import run_goal_worker  # noqa: E402
from agentjob_runtime.records.canonical import content_sha256  # noqa: E402


TS = "2026-07-17T20:00:00Z"
HASH_A = "a" * 64
HASH_B = "b" * 64
CAPABILITIES = {
    "agentjob_control": True,
    "goal_state": True,
    "continuation_envelope": True,
    "repository_provider": True,
    "thread_provider": True,
}


class FakeTaskProvider:
    provider_id = "website-fixture-provider"
    available = True

    def __init__(
        self,
        task_id: str | None,
        *,
        raise_error: bool = False,
    ) -> None:
        self.task_id = task_id
        self.raise_error = raise_error
        self.calls: list[dict[str, object]] = []

    def create_thread(self, *, prompt, envelope, idempotency_key):
        self.calls.append(
            {
                "prompt": prompt,
                "envelope": copy.deepcopy(envelope),
                "idempotency_key": idempotency_key,
            }
        )
        if self.raise_error:
            raise RuntimeError("task creation outcome is ambiguous")
        return ThreadCreateResult(
            "returned",
            self.task_id,
            {"provider_request_id": f"request-{len(self.calls)}"},
        )


class CountingContinue:
    def __init__(
        self,
        result: dict[str, object] | None,
        *,
        raise_error: bool = False,
    ) -> None:
        self.result = result
        self.raise_error = raise_error
        self.calls = 0

    def __call__(self, envelope):
        self.calls += 1
        if self.raise_error:
            raise RuntimeError("continue return boundary is ambiguous")
        return copy.deepcopy(self.result)


def repository_binding(root: Path) -> dict[str, object]:
    return {
        "project_id": "website-relay-fixture",
        "root": str(root),
        "worktree": str(root),
        "branch": "main",
        "git_common_dir": str(root / ".git"),
        "starting_revision": "fixture-A",
        "environment_mode": "local",
    }


def launch_inputs(root: Path) -> dict[str, object]:
    binding = repository_binding(root)
    return {
        "goal_text": "Complete the disposable website relay fixture.",
        "completion_contract": {
            "interpretation": (
                "The fixture is complete when its exact focused criterion passes."
            ),
            "required_evidence": ["The focused fixture passes."],
            "user_confirmed_when_ambiguous": True,
        },
        "guards": {
            "max_continue_passes": 3,
            "deadline_at": "2099-01-01T00:00:00Z",
        },
        "repository_binding": binding,
        "repository_observation": dict(binding),
        "initial_fingerprint": HASH_A,
        "authorization": {
            "fresh_recursive_threads_explicitly_requested": True
        },
        "capabilities": CAPABILITIES,
        "predecessor_thread_id": "task-launcher",
        "canonical_state": {
            "fingerprint": HASH_A,
            "active_task_id": "WI-FIXTURE-001",
            "current_decision_id": None,
            "current_job_id": "WJ-FIXTURE-001-A",
        },
        "progress_summary": "The fixture goal was reserved without project work.",
        "remaining_work": "Execute one bounded fixture generation.",
        "goal_id": "CG-20260717T200000Z-a1b2c3d4",
        "timestamp": TS,
        "launcher_token": "l" * 48,
        "handoff_token": "h" * 48,
    }


def continue_result() -> dict[str, object]:
    return {
        "schema_version": "sys4ai.continue-result.v1",
        "status": "completed",
        "boundary_entered": "existing_agent_job_ready",
        "agent_jobs_executed": 1,
        "task_id": "WI-FIXTURE-001",
        "decision_id": None,
        "job_id": "WJ-FIXTURE-001-A",
        "completion_id": "WJC-FIXTURE-001-A",
        "handoff_id": "WH-FIXTURE-001",
        "progress_effect": "bounded_completion",
        "global_goal_evaluation": "not_evaluated_here",
        "repository_fingerprint_before": HASH_A,
        "repository_fingerprint_after": HASH_B,
        "validators": {
            "required": 1,
            "passed": 1,
            "failed": 0,
            "warning": 0,
            "skipped": 0,
        },
        "next_recommended_action": "Evaluate the durable fixture contract.",
        "execution_performed": True,
        "reason_code": "website.fixture_completed",
        "extensions": {},
    }


def direct_evidence(criterion_status: str) -> dict[str, object]:
    return {
        "completion_contract_results": [
            {
                "criterion": "The focused fixture passes.",
                "status": criterion_status,
                "evidence_refs": (
                    ["tests/test_goal_relay_facade.py"]
                    if criterion_status == "pass"
                    else []
                ),
            }
        ],
        "checkpoint": {
            "provider": "website-checkpoint",
            "status": "pass",
            "revision": "fixture-B",
            "evidence_ref": "fixture-completion.yaml",
        },
        "validator_results": [
            {
                "validator_id": "focused",
                "validator_class": "process_validation",
                "status": "pass",
                "reason_code": None,
                "evidence_ref": "tests/test_goal_relay_facade.py",
                "notes": [],
            }
        ],
        "revision_before": "fixture-A",
        "revision_after": "fixture-B",
        "progress_summary": "One bounded website fixture generation was verified.",
        "remaining_work": (
            "No fixture work remains."
            if criterion_status == "pass"
            else "One lawful fixture generation remains."
        ),
        "human_gate_outstanding": False,
        "extensions": {},
    }


def launched_goal(
    root: Path,
    provider: FakeTaskProvider,
) -> tuple[SQLiteGoalStore, dict[str, object]]:
    store = SQLiteGoalStore(root / ".local/state/goal-state.sqlite3")
    launch_goal(store, provider=provider, **launch_inputs(root))
    envelope = provider.calls[0]["envelope"]
    assert isinstance(envelope, dict)
    return store, envelope


def test_disposable_relay_executes_one_job_and_creates_at_most_one_successor(
    tmp_path: Path,
) -> None:
    first_provider = FakeTaskProvider("task-generation-1")
    store, envelope = launched_goal(tmp_path, first_provider)
    invoker = CountingContinue(continue_result())
    successor_provider = FakeTaskProvider("task-generation-2")
    summary = run_goal_worker(
        store,
        envelope=envelope,
        envelope_sha256=content_sha256(envelope),
        expected_revision=store.load_goal(str(envelope["goal_id"]))["state"][
            "revision"
        ],
        current_thread_id="task-generation-1",
        continue_invoker=invoker,
        direct_evidence_provider=lambda result: direct_evidence("fail"),
        legal_route_available=True,
        successor_provider=successor_provider,
        claim_token="c" * 48,
        successor_handoff_token="n" * 48,
        timestamp=TS,
    )
    assert invoker.calls == 1
    assert summary.agentjobs_executed == 1
    assert summary.continue_invocations == 1
    assert summary.successor_create_calls == 1
    assert len(first_provider.calls) == 1
    assert len(successor_provider.calls) == 1
    assert summary.successor_thread_id == "task-generation-2"

    with pytest.raises(StateConflict):
        run_goal_worker(
            store,
            envelope=envelope,
            envelope_sha256=content_sha256(envelope),
            expected_revision=store.load_goal(str(envelope["goal_id"]))["state"][
                "revision"
            ],
            current_thread_id="task-generation-1",
            continue_invoker=invoker,
            direct_evidence_provider=lambda result: direct_evidence("fail"),
            legal_route_available=True,
            successor_provider=successor_provider,
            claim_token="d" * 48,
            successor_handoff_token="o" * 48,
            timestamp=TS,
        )
    assert invoker.calls == 1
    assert len(successor_provider.calls) == 1


def test_exact_completion_contract_terminalizes_without_successor(
    tmp_path: Path,
) -> None:
    first_provider = FakeTaskProvider("task-generation-1")
    store, envelope = launched_goal(tmp_path, first_provider)
    invoker = CountingContinue(continue_result())
    unused_successor = FakeTaskProvider("must-not-be-created")
    summary = run_goal_worker(
        store,
        envelope=envelope,
        envelope_sha256=content_sha256(envelope),
        expected_revision=store.load_goal(str(envelope["goal_id"]))["state"][
            "revision"
        ],
        current_thread_id="task-generation-1",
        continue_invoker=invoker,
        direct_evidence_provider=lambda result: direct_evidence("pass"),
        legal_route_available=True,
        successor_provider=unused_successor,
        claim_token="c" * 48,
        successor_handoff_token="n" * 48,
        timestamp=TS,
    )
    assert summary.state_phase == "terminal_complete"
    assert summary.goal_evaluation == "met"
    assert summary.continue_invocations == 1
    assert summary.successor_create_calls == 0
    assert unused_successor.calls == []


def test_unknown_continue_outcome_is_consumed_once_and_requires_recovery(
    tmp_path: Path,
) -> None:
    provider = FakeTaskProvider("task-generation-1")
    store, envelope = launched_goal(tmp_path, provider)
    invoker = CountingContinue(None, raise_error=True)
    summary = run_goal_worker(
        store,
        envelope=envelope,
        envelope_sha256=content_sha256(envelope),
        expected_revision=store.load_goal(str(envelope["goal_id"]))["state"][
            "revision"
        ],
        current_thread_id="task-generation-1",
        continue_invoker=invoker,
        direct_evidence_provider=lambda result: direct_evidence("fail"),
        legal_route_available=True,
        claim_token="c" * 48,
        timestamp=TS,
    )
    assert invoker.calls == 1
    assert summary.continue_invocations == "unknown"
    assert summary.agentjobs_executed == "unknown"
    assert summary.recovery_required is True
    with pytest.raises(StateConflict):
        run_goal_worker(
            store,
            envelope=envelope,
            envelope_sha256=content_sha256(envelope),
            expected_revision=store.load_goal(str(envelope["goal_id"]))["state"][
                "revision"
            ],
            current_thread_id="task-generation-1",
            continue_invoker=invoker,
            direct_evidence_provider=lambda result: direct_evidence("fail"),
            legal_route_available=True,
            claim_token="d" * 48,
            timestamp=TS,
        )
    assert invoker.calls == 1


def test_ambiguous_task_provider_enters_recovery_without_retry(
    tmp_path: Path,
) -> None:
    provider = FakeTaskProvider(None, raise_error=True)
    store = SQLiteGoalStore(tmp_path / ".local/state/goal-state.sqlite3")
    summary = launch_goal(store, provider=provider, **launch_inputs(tmp_path))
    assert summary.status == "ambiguous"
    assert summary.state_phase == "terminal_handoff_ambiguous"
    assert len(provider.calls) == 1

    recovered = begin_recovery(
        store,
        goal_id=summary.goal_id,
        expected_revision=summary.state_revision,
        user_authorization="user-authorized-fixture-recovery",
        evidence={"provider_status": "creation outcome remains unknown"},
        timestamp=TS,
    )
    assert recovered["state"]["phase"] == "recovery_pending"
    assert len(provider.calls) == 1


def test_manual_provider_retains_protected_handoff_without_execution(
    tmp_path: Path,
) -> None:
    store = SQLiteGoalStore(tmp_path / ".local/state/goal-state.sqlite3")
    provider = ManualThreadProvider(
        tmp_path,
        local_root=".local/sys4ai/continuation/manual",
        current_thread_id="task-launcher",
        timestamp=TS,
    )
    summary = launch_goal(store, provider=provider, **launch_inputs(tmp_path))
    assert summary.status == "manual_handoff_pending"
    assert summary.agentjobs_executed == 0
    assert summary.continue_invocations == 0
    assert summary.provider_create_calls == 1
    directory = (
        tmp_path
        / ".local/sys4ai/continuation/manual"
        / summary.goal_id
        / "generation-1"
    )
    for name in (
        "continuation-envelope.json",
        "new-thread-prompt.txt",
        "provider-receipt.json",
    ):
        path = directory / name
        assert path.is_file()
        assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_repository_or_canonical_mismatch_blocks_before_consumption(
    tmp_path: Path,
) -> None:
    git = {
        "project_root": str(tmp_path),
        "worktree": str(tmp_path),
        "git_common_dir": str(tmp_path / ".git"),
        "head": "1" * 40,
        "branch": "main",
        "status": [],
    }
    website = adapter.WebsiteSnapshot(
        repo_root=tmp_path,
        resolver={"status": "ready"},
        resolver_exit_code=0,
        git=git,
        record_paths={},
        record_hashes={},
        record_metadata={},
        fingerprint=HASH_A,
        source_authority={},
    )
    envelope = {
        "repository_binding": facade.repository_binding(website),
        "canonical_state": {"fingerprint": HASH_A},
    }
    assert facade._repository_matches_envelope(website, envelope) is True

    wrong_fingerprint = copy.deepcopy(envelope)
    wrong_fingerprint["canonical_state"]["fingerprint"] = HASH_B
    assert facade._repository_matches_envelope(website, wrong_fingerprint) is False
    wrong_repository = copy.deepcopy(envelope)
    wrong_repository["repository_binding"]["branch"] = "other"
    assert facade._repository_matches_envelope(website, wrong_repository) is False


def test_structured_unknown_result_enters_recovery_without_successor(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(facade, "REPO_ROOT", tmp_path)
    store = SQLiteGoalStore(tmp_path / facade.STATE_DB_RELATIVE)
    provider = FakeTaskProvider("task-generation-1")
    launch_goal(store, provider=provider, **launch_inputs(tmp_path))
    envelope = provider.calls[0]["envelope"]
    assert isinstance(envelope, dict)
    goal_id = str(envelope["goal_id"])
    current = store.load_goal(goal_id)
    claimed = claim_generation(
        store,
        goal_id=goal_id,
        expected_revision=int(current["state"]["revision"]),
        generation=1,
        handoff_token=str(envelope["handoff_token"]),
        idempotency_key=str(envelope["idempotency_key"]),
        successor_thread_id="task-generation-1",
        claim_token="c" * 48,
        timestamp=TS,
    )
    consumed = consume_invocation(
        store,
        goal_id=goal_id,
        expected_revision=int(claimed["state"]["revision"]),
        generation=1,
        claim_token="c" * 48,
        observations={
            "human_gate_clear": True,
            "validation_clear": True,
            "checkpoint_clear": True,
            "dirty_state_expected": True,
            "capabilities_available": True,
            "repository_matches": True,
        },
        timestamp=TS,
    )
    git = {
        "project_root": str(tmp_path),
        "worktree": str(tmp_path),
        "git_common_dir": str(tmp_path / ".git"),
        "head": "1" * 40,
        "branch": "main",
        "status": [],
    }
    website = adapter.WebsiteSnapshot(
        repo_root=tmp_path,
        resolver={"status": "ready"},
        resolver_exit_code=0,
        git=git,
        record_paths={},
        record_hashes={},
        record_metadata={},
        fingerprint=HASH_B,
        source_authority={},
    )
    facade.write_protected_json(
        facade._invocation_path(goal_id, 1),
        {
            "schema_version": "sys4ai.website-worker-invocation.v1",
            "goal_id": goal_id,
            "generation": 1,
            "current_task_id": "task-generation-1",
            "claim_token": "c" * 48,
            "envelope_path": "fixture-envelope.json",
            "envelope_sha256": content_sha256(envelope),
            "activation_receipt_path": "fixture-activation.json",
            "state_revision": int(consumed["state"]["revision"]),
            "before_snapshot": website.as_dict(),
        },
    )
    unknown = continue_result()
    unknown.update(
        {
            "status": "unknown",
            "agent_jobs_executed": "unknown",
            "progress_effect": "unknown",
            "repository_fingerprint_before": HASH_A,
            "repository_fingerprint_after": HASH_B,
            "reason_code": "website.fixture_outcome_unknown",
        }
    )
    monkeypatch.setattr(facade, "capture_snapshot", lambda root: website)
    monkeypatch.setattr(
        facade,
        "build_continue_result",
        lambda before, after, execution_attempted: unknown,
    )
    outcome = facade.worker_finalize(
        Namespace(
            goal_id=goal_id,
            generation=1,
            current_task_id="task-generation-1",
            contract_results=None,
            legal_route_available=True,
        )
    )
    final = store.load_goal(goal_id)
    assert outcome["status"] == "recovery_required"
    assert outcome["successor"] is None
    assert final["generations"]["1"]["invocation_state"] == "unknown"
    assert final["state"]["phase"] == "terminal_awaiting_human"
    assert len(final["generations"]) == 1
