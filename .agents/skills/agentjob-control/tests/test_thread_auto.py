from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.adapters.thread_auto import select_thread_provider
from agentjob_runtime.adapters.thread_manual import ManualThreadProvider
from agentjob_runtime.errors import BootstrapRequired
from agentjob_runtime.goal.launcher import ThreadCreateResult


class FakeAutomaticProvider:
    available = True

    def __init__(self, provider_id="external-controller", *, available=True):
        self.provider_id = provider_id
        self.available = available
        self.calls = 0

    def capabilities(self):
        return {
            "provider_id": self.provider_id,
            "available": self.available,
            "automatic": True,
            "strategies": ["fresh_summary", "fork_history"],
            "operations": ["start", "read", "fork"],
            "protocol_idempotency": False,
        }

    def create_thread(self, *, prompt, envelope, idempotency_key):
        self.calls += 1
        return ThreadCreateResult("returned", "thread-automatic", {"request": "one"})


class ThreadAutoTests(unittest.TestCase):
    def test_explicit_available_provider_wins_and_selection_is_in_receipt(self) -> None:
        provider = FakeAutomaticProvider()
        selected = select_thread_provider(
            configured_provider=provider.provider_id,
            strategy="fresh_summary",
            providers=[provider],
        )
        result = selected.create_thread(
            prompt="prompt", envelope={}, idempotency_key="goal:1"
        )
        self.assertEqual(selected.provider_id, provider.provider_id)
        self.assertFalse(selected.selection.fallback_used)
        self.assertEqual(result.response["provider_selection"]["mode"], "automatic")
        self.assertEqual(provider.calls, 1)

    def test_auto_selection_is_deterministic_by_declared_provider_order(self) -> None:
        first = FakeAutomaticProvider("first")
        second = FakeAutomaticProvider("second")
        selected = select_thread_provider(
            configured_provider="auto",
            strategy="fresh_summary",
            providers=[first, second],
        )
        self.assertEqual(selected.provider_id, "first")

    def test_unavailable_provider_falls_back_to_manual_without_same_thread_recursion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manual = ManualThreadProvider(
                Path(directory), current_thread_id="thread-current"
            )
            selected = select_thread_provider(
                configured_provider="missing-automatic",
                strategy="fresh_summary",
                providers=[FakeAutomaticProvider(available=False)],
                manual_provider=manual,
            )
            self.assertEqual(selected.provider_id, "manual-handoff")
            self.assertTrue(selected.selection.fallback_used)
            self.assertEqual(selected.selection.mode, "manual")

    def test_missing_safe_or_required_automatic_provider_blocks(self) -> None:
        with self.assertRaises(BootstrapRequired):
            select_thread_provider(
                configured_provider="auto",
                strategy="fresh_summary",
                providers=[FakeAutomaticProvider(available=False)],
            )
        with tempfile.TemporaryDirectory() as directory:
            manual = ManualThreadProvider(Path(directory))
            with self.assertRaises(BootstrapRequired):
                select_thread_provider(
                    configured_provider="auto",
                    strategy="fresh_summary",
                    providers=[],
                    manual_provider=manual,
                    require_automatic=True,
                )


if __name__ == "__main__":
    unittest.main()
