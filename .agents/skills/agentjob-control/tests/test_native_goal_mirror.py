from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, RUNTIME_SCRIPTS, TS, valid_goal
from agentjob_runtime.adapters.native_goal_codex import (
    CodexNativeGoalProvider,
    build_goal_mirror,
)
from agentjob_runtime.errors import RecordValidationError
from agentjob_runtime.goal.initialize import initialize_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


class FakeMirrorTransport:
    def __init__(self, *, raise_error=False):
        self.values = {}
        self.raise_error = raise_error
        self.calls = []

    def set(self, thread_id, mirror):
        self.calls.append(("set", thread_id))
        if self.raise_error:
            raise RuntimeError("mirror unavailable")
        self.values[thread_id] = copy.deepcopy(mirror)
        return {"status": "set"}

    def get(self, thread_id):
        self.calls.append(("get", thread_id))
        if self.raise_error:
            raise RuntimeError("mirror unavailable")
        return copy.deepcopy(self.values.get(thread_id))

    def clear(self, thread_id):
        self.calls.append(("clear", thread_id))
        self.values.pop(thread_id, None)
        return {"status": "cleared"}


class NativeGoalMirrorTests(unittest.TestCase):
    def test_set_read_clear_records_receipts_without_tokens(self) -> None:
        record = valid_goal()
        record["handoff"]["token"] = "h" * 48
        receipts = []
        transport = FakeMirrorTransport()
        provider = CodexNativeGoalProvider(
            transport, receipt_sink=receipts.append, timestamp=TS
        )
        mirror = build_goal_mirror(
            record,
            canonical_ref=".local/sys4ai/continuation/state.sqlite3",
            concise_summary="Complete the bounded fixture.",
            timestamp=TS,
        )
        set_receipt = provider.set_mirror("thread-1", mirror)
        current = provider.inspect_mirror("thread-1", canonical_record=record)
        clear = provider.clear_mirror("thread-1")
        self.assertEqual(set_receipt.status, "pass")
        self.assertEqual(current.status, "current")
        self.assertEqual(clear.status, "pass")
        self.assertEqual(len(receipts), 2)
        self.assertNotIn("h" * 48, str(mirror))
        self.assertNotIn("h" * 48, str(receipts))
        self.assertFalse(mirror["may_mark_complete"])

    def test_stale_mirror_cannot_override_canonical_phase(self) -> None:
        record = valid_goal()
        transport = FakeMirrorTransport()
        provider = CodexNativeGoalProvider(transport, timestamp=TS)
        mirror = build_goal_mirror(
            record,
            canonical_ref="state.sqlite3",
            concise_summary="Bounded relay.",
            timestamp=TS,
        )
        mirror["phase"] = "terminal_complete"
        transport.values["thread-1"] = mirror
        read = provider.inspect_mirror("thread-1", canonical_record=record)
        self.assertEqual(read.status, "stale")
        self.assertTrue(read.stale)
        self.assertEqual(record["state"]["phase"], "initialized")
        self.assertFalse(read.may_mark_complete)

    def test_provider_failure_or_disabled_mirror_does_not_corrupt_goal_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / "goal.db")
            goal = initialize_goal(
                store,
                goal_text="Finish the mirror fixture.",
                completion_contract={
                    "interpretation": "Finish when evidence passes.",
                    "required_evidence": ["Evidence passes."],
                    "user_confirmed_when_ambiguous": True,
                },
                guards={
                    "max_continue_passes": 2,
                    "deadline_at": "2099-01-01T00:00:00Z",
                },
                repository_binding={
                    "project_id": "mirror-fixture",
                    "root": str(root),
                    "worktree": str(root),
                    "branch": "main",
                    "git_common_dir": None,
                    "starting_revision": "A",
                    "environment_mode": "local",
                },
                initial_fingerprint=HASH_A,
                authorization={"fresh_recursive_threads_explicitly_requested": True},
                timestamp=TS,
                launcher_token="l" * 48,
            )
            before = store.load_goal(goal["goal_id"])
            mirror = build_goal_mirror(
                before,
                canonical_ref="goal.db",
                concise_summary="Mirror fixture.",
                timestamp=TS,
            )
            failed = CodexNativeGoalProvider(
                FakeMirrorTransport(raise_error=True), timestamp=TS
            ).set_mirror("thread-1", mirror)
            disabled = CodexNativeGoalProvider(None, enabled=False, timestamp=TS).set_mirror(
                "thread-1", mirror
            )
            self.assertEqual(failed.status, "fail")
            self.assertEqual(disabled.status, "unavailable")
            self.assertEqual(store.load_goal(goal["goal_id"]), before)

    def test_secret_like_summary_and_authority_shape_are_rejected(self) -> None:
        record = valid_goal()
        with self.assertRaises(RecordValidationError):
            build_goal_mirror(
                record,
                canonical_ref="state.sqlite3",
                concise_summary="Use sk-secretvalue123456789 to finish.",
            )
        mirror = build_goal_mirror(
            record,
            canonical_ref="state.sqlite3",
            concise_summary="Bounded relay.",
            timestamp=TS,
        )
        mirror["may_mark_complete"] = True
        with self.assertRaises(RecordValidationError):
            CodexNativeGoalProvider(FakeMirrorTransport()).set_mirror("thread-1", mirror)


if __name__ == "__main__":
    unittest.main()
