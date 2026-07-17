from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.adapters.checkpoint_command import CommandCheckpointProvider
from agentjob_runtime.adapters.checkpoint_git_commit import GitCommitCheckpointProvider
from agentjob_runtime.adapters.checkpoint_git_status import GitStatusCheckpointProvider
from agentjob_runtime.adapters.checkpoint_none import NoneCheckpointProvider
from agentjob_runtime.errors import SecurityError


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


class CheckpointProviderTests(unittest.TestCase):
    def git_project(self, root: Path) -> None:
        git(root, "init", "-q")
        git(root, "config", "user.name", "Fixture")
        git(root, "config", "user.email", "fixture@example.invalid")
        (root / "allowed.txt").write_text("one\n", encoding="utf-8")
        (root / "unrelated.txt").write_text("one\n", encoding="utf-8")
        git(root, "add", "allowed.txt", "unrelated.txt")
        git(root, "commit", "-qm", "initial")

    def test_none_and_git_status_providers_never_commit(self) -> None:
        self.assertEqual(NoneCheckpointProvider().capture_after({})["status"], "not_required")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            self.git_project(root)
            (root / "allowed.txt").write_text("two\n", encoding="utf-8")
            before = git(root, "rev-parse", "HEAD")
            receipt = GitStatusCheckpointProvider(str(root)).capture_after({})
            self.assertEqual(receipt["status"], "pass")
            self.assertIn("allowed.txt", receipt["changed_paths"])
            self.assertEqual(git(root, "rev-parse", "HEAD"), before)
            self.assertTrue(receipt["process_evidence_only"])

    def test_git_commit_requires_approval_and_does_not_stage_unrelated_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            self.git_project(root)
            (root / "allowed.txt").write_text("two\n", encoding="utf-8")
            (root / "unrelated.txt").write_text("two\n", encoding="utf-8")
            denied = GitCommitCheckpointProvider(
                root,
                approval_ref=None,
                message="checkpoint allowed path",
                approved_paths=["allowed.txt"],
            )
            with self.assertRaises(SecurityError):
                denied.capture_after({"changed_paths": ["allowed.txt"]})
            provider = GitCommitCheckpointProvider(
                root,
                approval_ref="APPROVAL-1",
                message="checkpoint allowed path",
                approved_paths=["allowed.txt"],
            )
            receipt = provider.capture_after({"changed_paths": ["allowed.txt"]})
            self.assertEqual(receipt["status"], "pass")
            self.assertEqual(git(root, "show", "--pretty=", "--name-only", "HEAD"), "allowed.txt")
            self.assertIn("unrelated.txt", git(root, "status", "--porcelain=v1"))
            self.assertNotIn("unrelated.txt", git(root, "diff", "--cached", "--name-only"))

    def test_command_provider_uses_fixed_argv_and_captures_failure_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            provider = CommandCheckpointProvider(
                directory,
                argv=[sys.executable, "-c", "print('checkpoint-ok')"],
            )
            receipt = provider(
                {"provider": "project_command", "argv": ["must", "not", "override"]},
                SimpleNamespace(job_id="AJ-1"),
            )
            self.assertEqual(receipt["status"], "pass")
            self.assertIn("checkpoint-ok", receipt["stdout"])
            self.assertEqual(provider.calls, 1)
            failing = CommandCheckpointProvider(
                directory,
                argv=[sys.executable, "-c", "raise SystemExit(3)"],
            )
            failed = failing.capture_after({})
            self.assertEqual(failed["status"], "fail")
            self.assertEqual(failed["exit_code"], 3)


if __name__ == "__main__":
    unittest.main()
