from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import ActiveRelayError, RecordValidationError
from agentjob_runtime.goal.initialize import FIXED_GUARDS, initialize_goal
from agentjob_runtime.goal.model import goal_text_sha256
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


NOW = "2026-07-17T15:00:00Z"
DEADLINE = "2099-01-01T00:00:00Z"


def binding(root: Path) -> dict:
    return {
        "project_id": "example-project",
        "root": str(root),
        "worktree": str(root),
        "branch": "main",
        "git_common_dir": str(root / ".git"),
        "starting_revision": "abc123",
        "environment_mode": "local",
    }


def contract() -> dict:
    return {
        "interpretation": "All requested evidence exists.",
        "required_evidence": ["Focused tests pass."],
        "user_confirmed_when_ambiguous": True,
    }


class GoalInitializationTests(unittest.TestCase):
    def initialize(self, store: SQLiteGoalStore, root: Path, **overrides):
        values = {
            "goal_text": "  Preserve Unicode Ω and trailing space  \r\nsecond\rline ",
            "completion_contract": contract(),
            "guards": {"max_continue_passes": 3, "deadline_at": DEADLINE},
            "repository_binding": binding(root),
            "initial_fingerprint": "a" * 64,
            "authorization": {"fresh_recursive_threads_explicitly_requested": True},
            "goal_id": "CG-20260717T150000Z-abcdef12",
            "timestamp": NOW,
            "launcher_token": "l" * 48,
        }
        values.update(overrides)
        return initialize_goal(store, **values)

    def test_exact_text_hash_binding_and_fixed_guards_are_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / "state.sqlite3")
            record = self.initialize(store, root)
            self.assertEqual(record["goal_text"], "  Preserve Unicode Ω and trailing space  \nsecond\nline ")
            self.assertEqual(record["goal_sha256"], goal_text_sha256(record["goal_text"]))
            self.assertEqual(record["repository_binding"]["branch"], "main")
            for key, value in FIXED_GUARDS.items():
                self.assertEqual(record["guards"][key], value)
            self.assertEqual(store.load_goal(record["goal_id"]), record)

    def test_initialization_is_atomic_and_competing_relay_loses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / "state.sqlite3")
            first = self.initialize(store, root)
            with self.assertRaises(ActiveRelayError):
                self.initialize(
                    store,
                    root,
                    goal_id="CG-20260717T150001Z-abcdef13",
                    timestamp="2026-07-17T15:00:01Z",
                )
            self.assertEqual([row["goal_id"] for row in store.list_goals()], [first["goal_id"]])

    def test_invalid_input_or_secret_leaves_no_goal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / "state.sqlite3")
            with self.assertRaises(RecordValidationError):
                self.initialize(store, root, goal_text="token=sk-proj-abcdefghijklmnopqrstuvwxyz")
            self.assertEqual(store.list_goals(), [])

    def test_original_fields_are_database_immutable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            store = SQLiteGoalStore(root / "state.sqlite3")
            record = self.initialize(store, root)
            with store.connect() as connection, self.assertRaises(Exception):
                connection.execute(
                    "UPDATE goals SET goal_text='changed' WHERE goal_id=?", (record["goal_id"],)
                )


if __name__ == "__main__":
    unittest.main()
