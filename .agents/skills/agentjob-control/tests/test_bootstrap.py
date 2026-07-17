from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.bootstrap import bootstrap_project, doctor_project
from agentjob_runtime.config import load_config
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


class BootstrapTests(unittest.TestCase):
    @staticmethod
    def files(root: Path) -> dict[str, bytes]:
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }

    def test_dry_run_is_read_only_and_lists_portable_profile_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            before = self.files(root)
            report = bootstrap_project(root, dry_run=True)
            self.assertEqual(report.status, "dry_run")
            self.assertEqual(report.selected_profile, "portable_registered")
            self.assertIn(".agents/control/config.yaml", report.planned_files)
            self.assertIn(".local/sys4ai/continuation/state.sqlite3", report.planned_files)
            self.assertEqual(before, self.files(root))
            self.assertFalse(report.execution_performed)
            self.assertEqual(report.agent_jobs_executed, 0)

    def test_bootstrap_is_idempotent_creates_no_task_and_doctor_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            first = bootstrap_project(root)
            self.assertEqual(first.status, "initialized")
            loaded = load_config(root)
            self.assertEqual(loaded.data["control"]["profile"], "portable_registered")
            self.assertEqual(loaded.data["repository"]["provider"], "filesystem_only")
            self.assertIn(
                ".local/sys4ai/continuation/",
                (root / ".gitignore").read_text(encoding="utf-8").splitlines(),
            )
            store = SQLiteGoalStore(
                root / ".local/sys4ai/continuation/state.sqlite3",
                auto_migrate=False,
                read_only=True,
            )
            self.assertEqual(store.list_goals(), [])
            self.assertEqual(list((root / ".agents/control/tasks").iterdir()), [])
            before = self.files(root)
            second = bootstrap_project(root)
            self.assertEqual(second.status, "already_initialized")
            self.assertEqual(before, self.files(root))
            self.assertEqual(doctor_project(root).status, "pass")

    def test_git_project_selects_read_only_git_status_checkpoint_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            report = bootstrap_project(root)
            self.assertEqual(report.repository_provider, "git")
            loaded = load_config(root)
            self.assertEqual(loaded.data["checkpoint"]["provider"], "git_status")
            self.assertFalse(loaded.data["checkpoint"]["auto_commit"])
            self.assertEqual(doctor_project(root).status, "pass")

    def test_existing_unmapped_control_is_preserved_for_adapter_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            existing = root / ".agents/control/native-authority.txt"
            existing.parent.mkdir(parents=True)
            existing.write_text("retain exactly\n", encoding="utf-8")
            before = self.files(root)
            report = bootstrap_project(root)
            self.assertEqual(report.status, "existing_control_detected")
            self.assertEqual(report.selected_profile, "existing_control_adapter")
            self.assertEqual(before, self.files(root))
            self.assertEqual(existing.read_text(encoding="utf-8"), "retain exactly\n")

    def test_failure_returns_partial_rollback_evidence_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            collision = root / ".agents/control/roles/software-engineer.yaml"
            collision.parent.mkdir(parents=True)
            collision.write_text("user-owned\n", encoding="utf-8")
            report = bootstrap_project(root)
            self.assertEqual(report.status, "existing_control_detected")
            self.assertEqual(collision.read_text(encoding="utf-8"), "user-owned\n")
            self.assertIsNotNone(report.error)


if __name__ == "__main__":
    unittest.main()
