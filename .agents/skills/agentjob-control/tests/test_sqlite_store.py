from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import MigrationError
from agentjob_runtime.goal.sqlite_store import Migration, SQLiteGoalStore


class SQLiteStoreTests(unittest.TestCase):
    def test_schema_migrates_with_constraints_and_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SQLiteGoalStore(Path(directory) / "state.sqlite3")
            self.assertEqual(store.current_schema_version(), 1)
            self.assertEqual(store.integrity_check()["status"], "pass")
            tables = store.export_data()["tables"]
            for table in (
                "goals",
                "goal_amendments",
                "generations",
                "leases",
                "events",
                "step_receipts",
                "successor_intents",
                "provider_receipts",
                "recovery_actions",
            ):
                self.assertIn(table, tables)
            with store.connect() as connection:
                self.assertEqual(connection.execute("PRAGMA foreign_keys").fetchone()[0], 1)
                self.assertGreater(connection.execute("PRAGMA busy_timeout").fetchone()[0], 0)
                self.assertEqual(connection.execute("PRAGMA journal_mode").fetchone()[0], "wal")

    def test_duplicate_idempotency_keys_and_receipts_are_database_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SQLiteGoalStore(Path(directory) / "state.sqlite3")
            with store.connect() as connection:
                connection.execute("PRAGMA foreign_keys=OFF")
                base = (
                    "G", 1, "t", "same-key", "successor_intent", "l", 0,
                    "not_authorized", None, None, "a" * 64, None, None, None,
                    None, None, None, None,
                )
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute(
                        "INSERT INTO generations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        base,
                    )
                    connection.execute(
                        "INSERT INTO generations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ("H", 1, *base[2:]),
                    )
                connection.rollback()
                connection.execute(
                    "INSERT INTO step_receipts(goal_id, generation, receipt_kind, payload_json, receipt_hash, finalized_at) "
                    "VALUES ('G', 1, 'failed', '{}', ?, '2026-07-17T15:00:00Z')",
                    ("a" * 64,),
                )
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute(
                        "INSERT INTO step_receipts(goal_id, generation, receipt_kind, payload_json, receipt_hash, finalized_at) "
                        "VALUES ('G', 1, 'failed', '{}', ?, '2026-07-17T15:00:01Z')",
                        ("b" * 64,),
                    )

    def test_failed_migration_rolls_back_and_preserves_export(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SQLiteGoalStore(Path(directory) / "state.sqlite3")
            broken = Migration(2, "broken", "CREATE TABLE partial(id INTEGER); INVALID SQL;")
            with self.assertRaises(MigrationError) as caught:
                store.apply_migrations([broken])
            self.assertEqual(store.current_schema_version(), 1)
            self.assertEqual(store.integrity_check()["status"], "pass")
            self.assertFalse(
                store.query_one("SELECT name FROM sqlite_master WHERE name='partial'")
            )
            self.assertTrue(caught.exception.details["backup_paths"])
            self.assertTrue(Path(caught.exception.details["backup_paths"][0]).is_file())


if __name__ == "__main__":
    unittest.main()
