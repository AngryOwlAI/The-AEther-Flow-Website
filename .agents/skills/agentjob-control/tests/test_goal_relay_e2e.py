from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, HASH_B, RUNTIME_SCRIPTS, TS
from agentjob_runtime.errors import StateConflict
from agentjob_runtime.goal.execution import (
    claim_generation,
    consume_invocation,
    record_invocation_returned,
)
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.launcher import ThreadCreateResult, launch_goal
from agentjob_runtime.goal.recovery import (
    abandon_unconsumed,
    begin_recovery,
    cancel_relay,
    reconcile_consumed,
)
from agentjob_runtime.goal.snapshots import regenerate_goal_snapshot
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import (
    InjectedSuccessorFault,
    record_successor,
    reserve_successor,
)
from agentjob_runtime.goal.worker import run_goal_worker
from agentjob_runtime.records.canonical import content_sha256


HASH_C = "c" * 64
AUTHORIZATION = "user-authorized-relay-recovery"
CAPABILITIES = {
    "agentjob_control": True,
    "goal_state": True,
    "continuation_envelope": True,
    "repository_provider": True,
    "thread_provider": True,
}
FIXTURES = Path(__file__).parent / "fixtures" / "relay" / "crash-windows.json"


class FakeThreadProvider:
    provider_id = "relay-fake"
    available = True

    def __init__(
        self,
        thread_id: str | None = None,
        *,
        status: str = "returned",
        raise_error: bool = False,
    ) -> None:
        self.thread_id = thread_id
        self.status = status
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
            raise RuntimeError("provider return boundary is unknown")
        return ThreadCreateResult(
            self.status,
            self.thread_id if self.status == "returned" else None,
            {"provider_request_id": f"relay-request-{len(self.calls)}"},
        )


class CountingContinue:
    def __init__(self, result: dict[str, object] | None = None, *, raise_error=False):
        self.result = result
        self.raise_error = raise_error
        self.calls = 0

    def __call__(self, envelope):
        self.calls += 1
        if self.raise_error:
            raise RuntimeError("continue outcome is uncertain")
        return copy.deepcopy(self.result)


class GoalRelayEndToEndTests(unittest.TestCase):
    maxDiff = None

    @staticmethod
    def binding(root: Path) -> dict[str, object]:
        return {
            "project_id": "neutral-relay-fixture",
            "root": str(root),
            "worktree": str(root),
            "branch": "main",
            "git_common_dir": None,
            "starting_revision": "A",
            "environment_mode": "local",
        }

    def launch(
        self,
        directory: str,
        *,
        provider: FakeThreadProvider | None = None,
        max_passes: int = 3,
        deadline: str = "2099-01-01T00:00:00Z",
    ):
        root = Path(directory).resolve()
        store = SQLiteGoalStore(root / ".local" / "state" / "goal.db")
        first_provider = provider or FakeThreadProvider("thread-generation-1")
        binding = self.binding(root)
        summary = launch_goal(
            store,
            goal_text="Complete the neutral relay fixture.",
            completion_contract={
                "interpretation": "The fixture is complete when its focused check passes.",
                "required_evidence": ["The focused check passes."],
                "user_confirmed_when_ambiguous": True,
            },
            guards={
                "max_continue_passes": max_passes,
                "deadline_at": deadline,
            },
            repository_binding=binding,
            repository_observation=dict(binding),
            initial_fingerprint=HASH_A,
            authorization={"fresh_recursive_threads_explicitly_requested": True},
            capabilities=CAPABILITIES,
            provider=first_provider,
            predecessor_thread_id="thread-launcher",
            canonical_state={
                "fingerprint": HASH_A,
                "active_task_id": None,
                "current_decision_id": None,
                "current_job_id": None,
            },
            progress_summary="The relay was initialized without project execution.",
            remaining_work="Execute one bounded generation.",
            goal_id="CG-20260717T150000Z-1234abcd",
            timestamp=TS,
            launcher_token="l" * 48,
            handoff_token="h" * 48,
        )
        envelope = (
            first_provider.calls[0]["envelope"] if first_provider.calls else None
        )
        return root, store, first_provider, summary, envelope

    @staticmethod
    def result(before: str, after: str, generation: int) -> dict[str, object]:
        return {
            "schema_version": "sys4ai.continue-result.v1",
            "status": "completed",
            "boundary_entered": "existing_agent_job_ready",
            "agent_jobs_executed": 1,
            "task_id": f"TASK-{generation}",
            "decision_id": f"DDR-{generation}",
            "job_id": f"AJ-{generation}",
            "completion_id": f"AJC-{generation}",
            "handoff_id": f"HANDOFF-{generation}",
            "progress_effect": "bounded_progress",
            "global_goal_evaluation": "not_evaluated_here",
            "repository_fingerprint_before": before,
            "repository_fingerprint_after": after,
            "validators": {
                "required": 1,
                "passed": 1,
                "failed": 0,
                "warning": 0,
                "skipped": 0,
            },
            "next_recommended_action": "Evaluate the durable completion contract.",
            "execution_performed": True,
            "reason_code": "goal.checked",
            "extensions": {},
        }

    @staticmethod
    def evidence(status: str) -> dict[str, object]:
        return {
            "completion_contract_results": [
                {
                    "criterion": "The focused check passes.",
                    "status": status,
                    "evidence_refs": ["tests/focused.json"] if status == "pass" else [],
                }
            ],
            "checkpoint": {
                "provider": "none",
                "status": "not_required",
                "revision": None,
                "evidence_ref": None,
            },
            "validator_results": [
                {
                    "validator_id": "focused",
                    "validator_class": "process_validation",
                    "status": "pass",
                    "reason_code": None,
                    "evidence_ref": None,
                    "notes": [],
                }
            ],
            "revision_before": "A",
            "revision_after": "B",
            "progress_summary": "Direct evidence for one generation was checked.",
            "remaining_work": "None." if status == "pass" else "Continue the legal route.",
        }

    @staticmethod
    def receipt_evidence(fingerprint: str, *, evaluation: str) -> dict[str, object]:
        return {
            "revision_before": "A",
            "revision_after": "B",
            "fingerprint_after": fingerprint,
            "agent_job_id": "AJ-recovered",
            "zero_job_reason": None,
            "task_id": "TASK-recovered",
            "handoff_id": "HANDOFF-recovered",
            "checkpoint": {
                "provider": "none",
                "status": "not_required",
                "revision": None,
                "evidence_ref": None,
            },
            "validator_results": [],
            "goal_evaluation": evaluation,
            "progress_summary": "Canonical recovery evidence was inspected.",
            "remaining_work": "Human review remains required.",
            "extensions": {},
        }

    def work_generation(
        self,
        store: SQLiteGoalStore,
        envelope: dict[str, object],
        *,
        thread_id: str,
        before: str,
        after: str,
        generation: int,
        criterion: str,
        provider: FakeThreadProvider | None = None,
        observations: dict[str, bool] | None = None,
        timestamp: str = TS,
        invoker: CountingContinue | None = None,
    ):
        continue_call = invoker or CountingContinue(
            self.result(before, after, generation)
        )
        summary = run_goal_worker(
            store,
            envelope=envelope,
            envelope_sha256=content_sha256(envelope),
            expected_revision=store.load_goal(str(envelope["goal_id"]))["state"]["revision"],
            current_thread_id=thread_id,
            continue_invoker=continue_call,
            direct_evidence_provider=lambda result: self.evidence(criterion),
            observations=observations,
            legal_route_available=True,
            successor_provider=provider,
            claim_token=(chr(98 + generation) * 48),
            successor_handoff_token=(chr(109 + generation) * 48),
            timestamp=timestamp,
        )
        return summary, continue_call

    @staticmethod
    def counts(store: SQLiteGoalStore) -> dict[str, int]:
        return {
            "receipts": int(
                store.query_one("SELECT COUNT(*) AS count FROM step_receipts")["count"]
            ),
            "providers": int(
                store.query_one("SELECT COUNT(*) AS count FROM provider_receipts")["count"]
            ),
            "generations": int(
                store.query_one("SELECT COUNT(*) AS count FROM generations")["count"]
            ),
        }

    def test_one_pass_completion_has_one_execution_and_one_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, envelope = self.launch(directory)
            summary, invoker = self.work_generation(
                store,
                envelope,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_B,
                generation=1,
                criterion="pass",
            )
            self.assertEqual(summary.state_phase, "terminal_complete")
            self.assertEqual(invoker.calls, 1)
            self.assertEqual(summary.successor_create_calls, 0)
            self.assertEqual(self.counts(store), {"receipts": 1, "providers": 1, "generations": 1})

    def test_multi_pass_progress_then_completion_is_exactly_once_per_generation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, first, _, envelope1 = self.launch(directory)
            second = FakeThreadProvider("thread-generation-2")
            summary1, invoker1 = self.work_generation(
                store,
                envelope1,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_B,
                generation=1,
                criterion="fail",
                provider=second,
            )
            envelope2 = second.calls[0]["envelope"]
            summary2, invoker2 = self.work_generation(
                store,
                envelope2,
                thread_id="thread-generation-2",
                before=HASH_B,
                after=HASH_C,
                generation=2,
                criterion="pass",
            )
            self.assertEqual(summary1.state_phase, "successor_created")
            self.assertEqual(summary2.state_phase, "terminal_complete")
            self.assertEqual((invoker1.calls, invoker2.calls), (1, 1))
            self.assertEqual((len(first.calls), len(second.calls)), (1, 1))
            self.assertEqual(self.counts(store), {"receipts": 2, "providers": 2, "generations": 2})

    def test_unchanged_and_repeated_states_stop_without_an_extra_successor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, envelope = self.launch(directory)
            summary, invoker = self.work_generation(
                store,
                envelope,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_A,
                generation=1,
                criterion="fail",
                provider=FakeThreadProvider("not-used"),
            )
            self.assertEqual(summary.state_phase, "terminal_no_progress")
            self.assertEqual(invoker.calls, 1)
            self.assertEqual(summary.successor_create_calls, 0)
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, envelope1 = self.launch(directory)
            second = FakeThreadProvider("thread-generation-2")
            self.work_generation(
                store,
                envelope1,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_B,
                generation=1,
                criterion="fail",
                provider=second,
            )
            unused = FakeThreadProvider("not-used")
            summary2, invoker2 = self.work_generation(
                store,
                second.calls[0]["envelope"],
                thread_id="thread-generation-2",
                before=HASH_B,
                after=HASH_A,
                generation=2,
                criterion="fail",
                provider=unused,
            )
            self.assertEqual(summary2.state_phase, "terminal_no_progress")
            self.assertEqual(invoker2.calls, 1)
            self.assertEqual(len(unused.calls), 0)
            self.assertEqual(self.counts(store)["generations"], 2)

    def test_human_gate_and_guard_exhaustion_execute_zero_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, envelope = self.launch(directory)
            summary, invoker = self.work_generation(
                store,
                envelope,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_B,
                generation=1,
                criterion="fail",
                observations={"human_gate_clear": False},
            )
            self.assertEqual(summary.state_phase, "terminal_awaiting_human")
            self.assertEqual(invoker.calls, 0)
            self.assertEqual(store.load_goal(summary.goal_id)["state"]["passes_consumed"], 0)
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, envelope = self.launch(directory, max_passes=1)
            summary, invoker = self.work_generation(
                store,
                envelope,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_B,
                generation=1,
                criterion="fail",
                provider=FakeThreadProvider("not-used"),
            )
            self.assertEqual(summary.state_phase, "terminal_guard_exhausted")
            self.assertEqual(invoker.calls, 1)
            self.assertEqual(store.load_goal(summary.goal_id)["state"]["passes_consumed"], 1)
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, envelope = self.launch(
                directory, deadline="2026-07-17T15:00:01Z"
            )
            summary, invoker = self.work_generation(
                store,
                envelope,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_B,
                generation=1,
                criterion="fail",
                timestamp="2026-07-17T15:00:01Z",
            )
            self.assertEqual(summary.state_phase, "terminal_guard_exhausted")
            self.assertEqual(invoker.calls, 0)

    def test_provider_failure_and_ambiguity_never_dispatch_twice(self) -> None:
        for status, expected_phase in (
            ("definitive_failure", "terminal_failed"),
            ("ambiguous", "terminal_handoff_ambiguous"),
        ):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                provider = FakeThreadProvider(status=status)
                _, store, _, summary, _ = self.launch(directory, provider=provider)
                self.assertEqual(len(provider.calls), 1)
                self.assertEqual(summary.state_phase, expected_phase)
                self.assertEqual(self.counts(store)["generations"], 1)

    def test_recovery_cancellation_after_ambiguous_dispatch_is_absorbing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            provider = FakeThreadProvider(status="ambiguous")
            _, store, _, summary, _ = self.launch(directory, provider=provider)
            recovery = begin_recovery(
                store,
                goal_id=summary.goal_id,
                expected_revision=summary.state_revision,
                user_authorization=AUTHORIZATION,
                evidence={"provider_status": "unable to prove a unique successor"},
                timestamp=TS,
            )
            cancelled = cancel_relay(
                store,
                goal_id=summary.goal_id,
                expected_revision=recovery["state"]["revision"],
                user_authorization=AUTHORIZATION,
                evidence={"reason": "operator cancelled the quarantined relay"},
                timestamp=TS,
            )
            self.assertEqual(cancelled["state"]["phase"], "terminal_cancelled")
            self.assertEqual(len(provider.calls), 1)
            with self.assertRaises(StateConflict):
                begin_recovery(
                    store,
                    goal_id=summary.goal_id,
                    expected_revision=cancelled["state"]["revision"],
                    user_authorization=AUTHORIZATION,
                    evidence={"reason": "must not reopen an absorbing terminal"},
                )

    def test_crash_fixture_catalog_covers_every_protocol_window(self) -> None:
        fixture = json.loads(FIXTURES.read_text(encoding="utf-8"))
        ids = {item["id"] for item in fixture["windows"]}
        self.assertEqual(
            ids,
            {
                "successor_intent_before_create",
                "create_before_successor_id_record",
                "successor_id_record_before_predecessor_exit",
                "claim_before_consumption",
                "consumption_before_continue_call",
                "continue_uncertain_return",
                "return_before_receipt",
                "receipt_before_successor_transfer",
                "state_commit_before_snapshot_render",
            },
        )
        self.assertEqual(len(fixture["windows"]), 9)

    def test_crash_after_successor_intent_requires_recovery_not_new_create(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manual = FakeThreadProvider(status="manual_pending")
            _, store, _, summary, _ = self.launch(directory, provider=manual)
            self.assertEqual(summary.state_phase, "successor_intent")
            record = store.load_goal(summary.goal_id)
            with self.assertRaises(StateConflict):
                reserve_successor(
                    store,
                    goal_id=summary.goal_id,
                    expected_revision=record["state"]["revision"],
                    current_holder_token=record["state"]["active_lease"]["holder_token"],
                    predecessor_thread_id="thread-launcher",
                )
            recovery = begin_recovery(
                store,
                goal_id=summary.goal_id,
                expected_revision=record["state"]["revision"],
                user_authorization=AUTHORIZATION,
                evidence={"provider_status": "no successor identity could be proven"},
                timestamp=TS,
            )
            cancelled = cancel_relay(
                store,
                goal_id=summary.goal_id,
                expected_revision=recovery["state"]["revision"],
                user_authorization=AUTHORIZATION,
                evidence={"reason": "cancel unresolved intent"},
                timestamp=TS,
            )
            self.assertEqual(cancelled["state"]["phase"], "terminal_cancelled")
            self.assertEqual(len(manual.calls), 1)
            self.assertEqual(self.counts(store)["generations"], 1)

    def test_crash_after_create_uses_record_only_idempotent_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / "state.sqlite3")
            binding = self.binding(root)
            initialized = initialize_goal(
                store,
                goal_text="Complete the neutral relay fixture.",
                completion_contract={
                    "interpretation": "Completion requires focused evidence.",
                    "required_evidence": ["The focused check passes."],
                    "user_confirmed_when_ambiguous": True,
                },
                guards={
                    "max_continue_passes": 3,
                    "deadline_at": "2099-01-01T00:00:00Z",
                },
                repository_binding=binding,
                initial_fingerprint=HASH_A,
                authorization={"fresh_recursive_threads_explicitly_requested": True},
                goal_id="CG-20260717T150000Z-1234abcd",
                timestamp=TS,
                launcher_token="l" * 48,
            )
            intent = reserve_successor(
                store,
                goal_id=initialized["goal_id"],
                expected_revision=initialized["state"]["revision"],
                current_holder_token="l" * 48,
                predecessor_thread_id="thread-launcher",
                handoff_token="h" * 48,
                timestamp=TS,
            )
            provider = FakeThreadProvider("thread-generation-1")
            created = provider.create_thread(
                prompt="retained exact prompt",
                envelope={"goal_id": initialized["goal_id"]},
                idempotency_key=intent["generations"]["1"]["idempotency_key"],
            )
            values = {
                "store": store,
                "goal_id": initialized["goal_id"],
                "expected_revision": intent["state"]["revision"],
                "generation": 1,
                "handoff_token": "h" * 48,
                "successor_thread_id": created.successor_thread_id,
                "provider_id": provider.provider_id,
                "provider_response": created.response,
                "timestamp": TS,
            }
            recorded = record_successor(**values)
            retried = record_successor(**values)
            self.assertEqual(recorded, retried)
            self.assertEqual(len(provider.calls), 1)
            self.assertEqual(self.counts(store)["providers"], 1)

    def test_crash_after_successor_id_allows_claim_without_predecessor_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, provider, summary, envelope = self.launch(directory)
            before_claim = store.load_goal(summary.goal_id)
            idempotent = record_successor(
                store,
                goal_id=summary.goal_id,
                expected_revision=before_claim["state"]["revision"],
                generation=1,
                handoff_token="h" * 48,
                successor_thread_id="thread-generation-1",
                provider_id=provider.provider_id,
                provider_response={"record_only": True},
                timestamp=TS,
            )
            self.assertEqual(idempotent["state"]["revision"], before_claim["state"]["revision"])
            claimed = claim_generation(
                store,
                goal_id=summary.goal_id,
                expected_revision=before_claim["state"]["revision"],
                generation=1,
                handoff_token=str(envelope["handoff_token"]),
                idempotency_key=str(envelope["idempotency_key"]),
                successor_thread_id="thread-generation-1",
                claim_token="c" * 48,
                timestamp=TS,
            )
            self.assertEqual(claimed["state"]["phase"], "step_active")
            self.assertEqual(len(provider.calls), 1)

    def test_crash_after_claim_can_finalize_zero_invocation_abandonment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, summary, envelope = self.launch(directory)
            claimed = claim_generation(
                store,
                goal_id=summary.goal_id,
                expected_revision=summary.state_revision,
                generation=1,
                handoff_token=str(envelope["handoff_token"]),
                idempotency_key=str(envelope["idempotency_key"]),
                successor_thread_id="thread-generation-1",
                claim_token="c" * 48,
                timestamp=TS,
            )
            abandoned = abandon_unconsumed(
                store,
                goal_id=summary.goal_id,
                expected_revision=claimed["state"]["revision"],
                generation=1,
                user_authorization=AUTHORIZATION,
                terminal_holder_proof={"thread_status": "terminal"},
                timestamp=TS,
            )
            self.assertEqual(abandoned["state"]["phase"], "terminal_failed")
            self.assertEqual(abandoned["state"]["passes_consumed"], 0)
            self.assertEqual(self.counts(store)["receipts"], 1)

    def test_crash_after_consumption_reconciles_unknown_without_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, summary, envelope = self.launch(directory)
            claimed = claim_generation(
                store,
                goal_id=summary.goal_id,
                expected_revision=summary.state_revision,
                generation=1,
                handoff_token=str(envelope["handoff_token"]),
                idempotency_key=str(envelope["idempotency_key"]),
                successor_thread_id="thread-generation-1",
                claim_token="c" * 48,
                timestamp=TS,
            )
            consumed = consume_invocation(
                store,
                goal_id=summary.goal_id,
                expected_revision=claimed["state"]["revision"],
                generation=1,
                claim_token="c" * 48,
                timestamp=TS,
            )
            recovery = begin_recovery(
                store,
                goal_id=summary.goal_id,
                expected_revision=consumed["state"]["revision"],
                user_authorization=AUTHORIZATION,
                evidence={"terminal_holder_proof": {"thread_status": "terminal"}},
                timestamp=TS,
            )
            reconciled = reconcile_consumed(
                store,
                goal_id=summary.goal_id,
                expected_revision=recovery["state"]["revision"],
                generation=1,
                user_authorization=AUTHORIZATION,
                terminal_holder_proof={"thread_status": "terminal"},
                canonical_evidence={
                    "after_fingerprint": HASH_A,
                    "goal_evaluation": "indeterminate",
                    "receipt_evidence": self.receipt_evidence(
                        HASH_A, evaluation="indeterminate"
                    ),
                },
                returned_proven=False,
                decision="terminal_awaiting_human",
                timestamp=TS,
            )
            self.assertEqual(reconciled["state"]["phase"], "terminal_awaiting_human")
            self.assertEqual(reconciled["generations"]["1"]["invocation_state"], "unknown")
            self.assertEqual(reconciled["state"]["passes_consumed"], 1)
            self.assertEqual(self.counts(store)["receipts"], 1)

    def test_crash_during_continue_records_unknown_and_quarantines(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, envelope = self.launch(directory)
            invoker = CountingContinue(raise_error=True)
            summary, _ = self.work_generation(
                store,
                envelope,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_B,
                generation=1,
                criterion="fail",
                invoker=invoker,
            )
            record = store.load_goal(summary.goal_id)
            self.assertEqual(summary.state_phase, "terminal_awaiting_human")
            self.assertEqual(invoker.calls, 1)
            self.assertTrue(summary.recovery_required)
            self.assertEqual(record["state"]["active_lease"]["holder_kind"], "quarantined")
            self.assertEqual(self.counts(store)["receipts"], 0)

    def test_crash_after_return_finalizes_existing_generation_without_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, summary, envelope = self.launch(directory)
            claimed = claim_generation(
                store,
                goal_id=summary.goal_id,
                expected_revision=summary.state_revision,
                generation=1,
                handoff_token=str(envelope["handoff_token"]),
                idempotency_key=str(envelope["idempotency_key"]),
                successor_thread_id="thread-generation-1",
                claim_token="c" * 48,
                timestamp=TS,
            )
            consumed = consume_invocation(
                store,
                goal_id=summary.goal_id,
                expected_revision=claimed["state"]["revision"],
                generation=1,
                claim_token="c" * 48,
                timestamp=TS,
            )
            result = self.result(HASH_A, HASH_B, 1)
            returned = record_invocation_returned(
                store,
                goal_id=summary.goal_id,
                expected_revision=consumed["state"]["revision"],
                generation=1,
                claim_token="c" * 48,
                continue_result=result,
                timestamp=TS,
            )
            recovery = begin_recovery(
                store,
                goal_id=summary.goal_id,
                expected_revision=returned["state"]["revision"],
                user_authorization=AUTHORIZATION,
                evidence={"thread_status": "terminal", "direct_return": True},
                timestamp=TS,
            )
            reconciled = reconcile_consumed(
                store,
                goal_id=summary.goal_id,
                expected_revision=recovery["state"]["revision"],
                generation=1,
                user_authorization=AUTHORIZATION,
                terminal_holder_proof={"thread_status": "terminal"},
                canonical_evidence={
                    "after_fingerprint": HASH_B,
                    "fingerprint_status": "new",
                    "goal_evaluation": "unmet",
                    "receipt_evidence": self.receipt_evidence(
                        HASH_B, evaluation="unmet"
                    ),
                },
                returned_proven=True,
                decision="terminal_failed",
                timestamp=TS,
            )
            self.assertEqual(reconciled["state"]["phase"], "terminal_failed")
            self.assertEqual(reconciled["generations"]["1"]["invocation_state"], "returned")
            self.assertEqual(self.counts(store)["receipts"], 1)

    def test_crash_during_receipt_and_transfer_rolls_back_then_commits_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, envelope = self.launch(directory)
            manual = FakeThreadProvider(status="manual_pending")
            summary, invoker = self.work_generation(
                store,
                envelope,
                thread_id="thread-generation-1",
                before=HASH_A,
                after=HASH_B,
                generation=1,
                criterion="fail",
                provider=manual,
            )
            intent = store.load_goal(summary.goal_id)
            generation = intent["state"]["current_generation"]
            entry = intent["generations"][str(generation)]
            values = {
                "store": store,
                "goal_id": summary.goal_id,
                "expected_revision": intent["state"]["revision"],
                "generation": generation,
                "handoff_token": entry["handoff_token"],
                "successor_thread_id": "thread-generation-2",
                "provider_id": "record-only-recovery",
                "provider_response": {"proof": "one retained provider result"},
                "timestamp": TS,
            }
            with self.assertRaises(InjectedSuccessorFault):
                record_successor(**values, fault_after="prior_receipt")
            rolled_back = store.load_goal(summary.goal_id)
            self.assertEqual(rolled_back["state"]["phase"], "successor_intent")
            self.assertIsNone(rolled_back["generations"]["1"]["finalized_receipt_hash"])
            self.assertEqual(self.counts(store)["receipts"], 0)
            committed = record_successor(**values)
            retried = record_successor(**values)
            self.assertEqual(committed, retried)
            self.assertEqual(invoker.calls, 1)
            self.assertEqual(len(manual.calls), 1)
            self.assertEqual(self.counts(store), {"receipts": 1, "providers": 2, "generations": 2})

    def test_snapshot_failure_retains_canonical_commit_and_regenerates_derivative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, store, _, summary, _ = self.launch(directory)
            failed = regenerate_goal_snapshot(
                store,
                goal_id=summary.goal_id,
                expected_revision=summary.state_revision,
                output_path=".local/state/goal-snapshot.md",
                inject_render_failure=True,
                timestamp=TS,
            )
            self.assertEqual(failed.status, "failed")
            retained = store.load_goal(summary.goal_id)
            self.assertEqual(retained["state"]["phase"], "successor_created")
            self.assertEqual(retained["state"]["revision"], summary.state_revision + 1)
            passed = regenerate_goal_snapshot(
                store,
                goal_id=summary.goal_id,
                expected_revision=retained["state"]["revision"],
                output_path=".local/state/goal-snapshot.md",
                timestamp=TS,
            )
            self.assertEqual(passed.status, "pass")
            payload = (root / passed.path).read_text(encoding="utf-8")
            self.assertIn("Durable goal relay snapshot", payload)
            self.assertNotIn("h" * 48, payload)
            self.assertNotIn("Complete the neutral relay fixture", payload)


if __name__ == "__main__":
    unittest.main()
