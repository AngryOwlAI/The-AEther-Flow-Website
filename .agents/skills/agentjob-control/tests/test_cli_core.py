import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _support import PACKAGE_ROOT, valid_config, valid_task
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.records.canonical import render_canonical_json


CLI = PACKAGE_ROOT / "scripts" / "agentjobctl.py"


class CoreCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(CLI), *map(str, arguments)],
            text=True,
            capture_output=True,
            check=False,
        )

    def prepared_project(self, directory: str):
        root = Path(directory).resolve()
        config_path = root / "config.json"
        config_path.write_text(render_canonical_json(valid_config()), encoding="utf-8")
        store = FilesystemControlStore(root, ".agents/control")
        task = valid_task()
        task["current_decision_id"] = None
        task["current_job_id"] = None
        store.create_task(task)
        return root, config_path, store

    def tree_bytes(self, root: Path):
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }

    def test_help_runs_without_project_state(self) -> None:
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("activate-packet", result.stdout)

    def test_status_and_fingerprint_are_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, config, _ = self.prepared_project(directory)
            before = self.tree_bytes(root)
            status = self.run_cli(
                "status", "--project-root", root, "--config", config, "--json"
            )
            fingerprint = self.run_cli(
                "fingerprint", "--project-root", root, "--config", config, "--json"
            )
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertEqual(fingerprint.returncode, 0, fingerprint.stderr)
            self.assertEqual(before, self.tree_bytes(root))
            self.assertEqual(json.loads(status.stdout)["resolver"]["boundary"], "director_decision_required")
            self.assertEqual(len(json.loads(fingerprint.stdout)["fingerprint"]), 64)

    def test_write_command_requires_root_and_revision(self) -> None:
        result = self.run_cli("complete", "--completion", "missing.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--project-root", result.stderr)

    def test_missing_configuration_returns_stable_bootstrap_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli("status", "--project-root", directory, "--json")
            self.assertEqual(result.returncode, 3)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["code"], "bootstrap.required")


if __name__ == "__main__":
    unittest.main()
