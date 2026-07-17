from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.adapters.repository_filesystem import FilesystemRepositoryProvider
from agentjob_runtime.adapters.repository_git import GitRepositoryProvider
from agentjob_runtime.errors import RecordValidationError, SecurityError


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


class RepositoryProviderTests(unittest.TestCase):
    def git_project(self, root: Path) -> None:
        git(root, "init", "-q")
        git(root, "config", "user.name", "Fixture")
        git(root, "config", "user.email", "fixture@example.invalid")
        (root / "tracked.txt").write_text("one\n", encoding="utf-8")
        git(root, "add", "tracked.txt")
        git(root, "commit", "-qm", "initial")

    def test_filesystem_provider_detects_added_modified_and_deleted_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "modified.txt").write_text("before\n", encoding="utf-8")
            (root / "deleted.txt").write_text("delete\n", encoding="utf-8")
            provider = FilesystemRepositoryProvider(root)
            before = provider.snapshot()
            (root / "modified.txt").write_text("after\n", encoding="utf-8")
            (root / "deleted.txt").unlink()
            (root / "added.txt").write_text("add\n", encoding="utf-8")
            after = provider.snapshot()
            changes = {item.path: item.status for item in provider.changed_paths(before, after)}
            self.assertEqual(
                changes,
                {"added.txt": "added", "deleted.txt": "deleted", "modified.txt": "modified"},
            )
            self.assertTrue(provider.status().clean)

    def test_git_provider_is_read_only_and_normalizes_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            self.git_project(root)
            provider = GitRepositoryProvider(root)
            before_git = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in (root / ".git").rglob("*")
                if path.is_file()
            }
            before = provider.snapshot()
            (root / "tracked.txt").write_text("two\n", encoding="utf-8")
            (root / "space name.txt").write_text("new\n", encoding="utf-8")
            after = provider.snapshot()
            status = provider.status()
            self.assertEqual(tuple(sorted(status.changed_paths)), status.changed_paths)
            self.assertIn("tracked.txt", status.changed_paths)
            self.assertIn("space name.txt", status.changed_paths)
            changes = {item.path: item.status for item in provider.changed_paths(before, after)}
            self.assertEqual(changes["tracked.txt"], "modified")
            self.assertEqual(changes["space name.txt"], "added")
            provider.identity()
            after_git = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in (root / ".git").rglob("*")
                if path.is_file()
            }
            self.assertEqual(before_git, after_git)

    def test_detached_head_and_repository_mismatch_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            self.git_project(root)
            git(root, "checkout", "--detach", "-q")
            provider = GitRepositoryProvider(root)
            identity = provider.identity()
            self.assertTrue(identity.detached)
            self.assertIsNone(identity.branch)
            mismatch = provider.matches({"provider": "git", "revision": "different"})
            self.assertEqual(mismatch.status, "fail")
            self.assertEqual(mismatch.reason_code, "repository.identity_mismatch")

    def test_no_git_and_cross_platform_path_behavior_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with self.assertRaises(RecordValidationError):
                GitRepositoryProvider(root)
            provider = FilesystemRepositoryProvider(root, case_sensitive=False)
            first = provider.canonicalize_path("Docs/Guide.md")
            second = provider.canonicalize_path("docs\\guide.md")
            self.assertEqual(first.comparison_key, second.comparison_key)
            with self.assertRaises(SecurityError):
                provider.canonicalize_path("C:\\outside\\file.txt")
            with self.assertRaises(SecurityError):
                provider.canonicalize_path("../outside.txt")


if __name__ == "__main__":
    unittest.main()
