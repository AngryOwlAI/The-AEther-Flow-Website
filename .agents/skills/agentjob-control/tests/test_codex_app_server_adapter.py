from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, RUNTIME_SCRIPTS, TS
from agentjob_runtime.adapters.thread_codex_app_server import CodexAppServerThreadProvider
from agentjob_runtime.goal.launcher import launch_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


class FakeTransport:
    def __init__(self, responses=None, *, exception=None):
        self.responses = dict(responses or {})
        self.exception = exception
        self.calls = []

    def request(self, operation, payload, *, timeout_seconds):
        self.calls.append(
            {"operation": operation, "payload": payload, "timeout_seconds": timeout_seconds}
        )
        if operation != "capabilities" and self.exception:
            raise self.exception
        if operation == "capabilities":
            return {
                "available": True,
                "operations": ["thread.start", "thread.read", "thread.resume", "thread.fork"],
            }
        return self.responses.get(
            operation,
            {"status": "returned", "thread_id": "thread-created", "request_id": "REQ-1"},
        )


def envelope(predecessor="thread-predecessor"):
    return {
        "goal_id": "CG-1",
        "generation": 1,
        "predecessor_thread_id": predecessor,
        "handoff_token": "h" * 48,
    }


class CodexAppServerAdapterTests(unittest.TestCase):
    def test_capability_discovery_and_fresh_summary_create_are_cached(self) -> None:
        transport = FakeTransport()
        provider = CodexAppServerThreadProvider(transport)
        self.assertTrue(provider.available)
        self.assertTrue(provider.available)
        result = provider.create_thread(
            prompt="bounded summary",
            envelope=envelope(),
            idempotency_key="CG-1:1",
        )
        self.assertEqual(result.status, "returned")
        self.assertEqual(result.successor_thread_id, "thread-created")
        self.assertEqual([item["operation"] for item in transport.calls], ["capabilities", "thread.start"])
        self.assertFalse(result.response["protocol_idempotency_external"])

    def test_fork_history_translates_to_one_fork_request(self) -> None:
        transport = FakeTransport()
        provider = CodexAppServerThreadProvider(transport, strategy="fork_history")
        result = provider.create_thread(
            prompt="fork bounded history",
            envelope=envelope("thread-parent"),
            idempotency_key="CG-1:1",
        )
        self.assertEqual(result.status, "returned")
        call = transport.calls[-1]
        self.assertEqual(call["operation"], "thread.fork")
        self.assertEqual(call["payload"]["thread_id"], "thread-parent")

    def test_timeout_and_ambiguous_exception_make_one_create_call(self) -> None:
        for error, status in ((TimeoutError(), "timeout"), (RuntimeError("uncertain"), "ambiguous")):
            with self.subTest(status=status):
                transport = FakeTransport(exception=error)
                provider = CodexAppServerThreadProvider(transport)
                result = provider.create_thread(
                    prompt="one request",
                    envelope=envelope(),
                    idempotency_key="CG-1:1",
                )
                self.assertEqual(result.status, status)
                self.assertEqual(
                    [item["operation"] for item in transport.calls].count("thread.start"), 1
                )

    def test_recorded_evidence_redacts_provider_secrets_and_prompt_content(self) -> None:
        transport = FakeTransport(
            {
                "thread.start": {
                    "status": "returned",
                    "thread_id": "thread-created",
                    "request_id": "REQ-1",
                    "api_token": "sk-secretvalue123456789",
                    "diagnostic": "safe",
                }
            }
        )
        provider = CodexAppServerThreadProvider(transport)
        result = provider.create_thread(
            prompt="contains sk-secretvalue123456789 only in transport request",
            envelope=envelope(),
            idempotency_key="CG-1:1",
        )
        self.assertNotIn("sk-secretvalue", str(result.response))
        self.assertNotIn("contains", str(result.response))

    def test_launcher_persists_returned_id_before_stopping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / ".local/state/goal.db")
            transport = FakeTransport()
            provider = CodexAppServerThreadProvider(transport)
            binding = {
                "project_id": "app-server-fixture",
                "root": str(root),
                "worktree": str(root),
                "branch": "main",
                "git_common_dir": None,
                "starting_revision": "A",
                "environment_mode": "local",
            }
            summary = launch_goal(
                store,
                goal_text="Complete the app server fixture.",
                completion_contract={
                    "interpretation": "Complete when focused evidence passes.",
                    "required_evidence": ["Focused evidence passes."],
                    "user_confirmed_when_ambiguous": True,
                },
                guards={
                    "max_continue_passes": 2,
                    "deadline_at": "2099-01-01T00:00:00Z",
                },
                repository_binding=binding,
                repository_observation=dict(binding),
                initial_fingerprint=HASH_A,
                authorization={"fresh_recursive_threads_explicitly_requested": True},
                capabilities={
                    "agentjob_control": True,
                    "goal_state": True,
                    "continuation_envelope": True,
                    "repository_provider": True,
                    "thread_provider": True,
                },
                provider=provider,
                predecessor_thread_id="thread-launcher",
                canonical_state={"fingerprint": HASH_A},
                progress_summary="Initialized.",
                remaining_work="Run one generation.",
                timestamp=TS,
                launcher_token="l" * 48,
                handoff_token="h" * 48,
            )
            record = store.load_goal(summary.goal_id)
            self.assertEqual(summary.state_phase, "successor_created")
            self.assertEqual(record["handoff"]["successor_thread_id"], "thread-created")
            self.assertEqual(summary.agentjobs_executed, 0)

    def test_read_resume_and_terminal_checks_return_minimal_evidence(self) -> None:
        transport = FakeTransport(
            {
                "thread.read": {
                    "thread_id": "thread-1",
                    "status": "completed",
                    "terminal": True,
                    "messages": ["private history"],
                },
                "thread.resume": {
                    "thread_id": "thread-1",
                    "status": "resumed",
                    "request_id": "REQ-2",
                },
            }
        )
        provider = CodexAppServerThreadProvider(transport)
        read = provider.read_thread("thread-1")
        self.assertNotIn("messages", read)
        self.assertTrue(provider.confirm_terminal("thread-1"))
        self.assertEqual(provider.resume_thread("thread-1", "continue")["status"], "resumed")


if __name__ == "__main__":
    unittest.main()
