from __future__ import annotations

import copy
import os
import tempfile
import unittest
from pathlib import Path

from _support import valid_config, valid_job, valid_role
from agentjob_runtime.config import load_config
from agentjob_runtime.errors import RecordValidationError, SecurityError
from agentjob_runtime.execution.compiler import compile_authority
from agentjob_runtime.execution.executor import ExecutionContext
from agentjob_runtime.records.canonical import render_canonical_json


CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


class PathSecurityTests(unittest.TestCase):
    def prepared(self, directory: str):
        root = Path(directory).resolve()
        (root / "src").mkdir()
        (root / "tests").mkdir()
        (root / "src/example.py").write_text("value = 1\n", encoding="utf-8")
        (root / "tests/test_example.py").write_text("fixture = True\n", encoding="utf-8")
        return root, valid_job(), valid_role()

    def compile(self, root: Path, job, role=None):
        role = role or valid_role()
        return compile_authority(
            project_root=root,
            job=job,
            execution_role=role,
            activated_record_ids={job["job_id"], role["execution_role_id"]},
            runtime_capabilities=CAPABILITIES,
        )

    def test_posix_and_windows_traversal_and_absolute_aliases_are_blocked(self) -> None:
        values = ["../secret", "..\\secret", "/etc/passwd", "C:\\Windows\\system.ini", "\\\\server\\share"]
        with tempfile.TemporaryDirectory() as directory:
            root, baseline, role = self.prepared(directory)
            for value in values:
                job = copy.deepcopy(baseline)
                job["authority"]["allowed_read_paths"] = [value]
                with self.subTest(path=value), self.assertRaises((RecordValidationError, SecurityError)):
                    self.compile(root, job, role)

    def test_windows_separators_normalize_and_aliases_collide_portably(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, job, role = self.prepared(directory)
            job["authority"]["allowed_read_paths"] = ["src\\example.py"]
            authority = self.compile(root, job, role)
            self.assertEqual(authority.allowed_read_paths[0].relative, "src/example.py")
            job["authority"]["allowed_read_paths"] = ["src/example.py", "src\\example.py"]
            with self.assertRaises(SecurityError) as caught:
                self.compile(root, job, role)
            self.assertEqual(caught.exception.details["reason_code"], "path.alias")

    def test_case_collisions_reserved_names_and_trimmed_components_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, baseline, role = self.prepared(directory)
            job = copy.deepcopy(baseline)
            job["authority"]["allowed_read_paths"] = ["src/Example.py", "src/example.py"]
            with self.assertRaises(SecurityError):
                self.compile(root, job, role)
            for value in ("CON", "aux.txt", "src/name.", "src/name ", "src/file.txt:stream"):
                job = copy.deepcopy(baseline)
                job["authority"]["allowed_read_paths"] = [value]
                with self.subTest(path=value), self.assertRaises(SecurityError):
                    self.compile(root, job, role)

    def test_unicode_requires_nfc_and_canonical_unicode_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, baseline, role = self.prepared(directory)
            nfc = "src/caf\u00e9.txt"
            (root / nfc).write_text("ok\n", encoding="utf-8")
            job = copy.deepcopy(baseline)
            job["authority"]["allowed_read_paths"] = [nfc]
            self.assertEqual(self.compile(root, job, role).allowed_read_paths[0].relative, nfc)
            job["authority"]["allowed_read_paths"] = ["src/cafe\u0301.txt"]
            with self.assertRaises(SecurityError) as caught:
                self.compile(root, job, role)
            self.assertEqual(caught.exception.details["reason_code"], "path.unicode_not_nfc")

    def test_only_explicit_directory_rules_are_recursive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, baseline, role = self.prepared(directory)
            for unsupported in ("src/*.py", "src/**/example.py", "src/?x"):
                job = copy.deepcopy(baseline)
                job["authority"]["allowed_read_paths"] = [unsupported]
                with self.subTest(path=unsupported), self.assertRaises(SecurityError):
                    self.compile(root, job, role)

            job = copy.deepcopy(baseline)
            job["authority"]["allowed_write_paths"] = ["out/**"]
            job["authority"]["allowed_generated_paths"] = []
            job["expected_outputs"] = [
                {"path": "out/nested/result.txt", "kind": "controlled_source_change"}
            ]
            authority = self.compile(root, job, role)
            context = ExecutionContext(authority)
            context.write_text("out/nested/result.txt", "ok\n")
            self.assertTrue((root / "out/nested/result.txt").is_file())
            with self.assertRaises(SecurityError):
                context.write_text("outside/result.txt", "blocked\n")

    def test_symlink_escape_and_hardlink_alias_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root, baseline, role = self.prepared(directory)
            target = Path(outside) / "secret.txt"
            target.write_text("secret\n", encoding="utf-8")
            (root / "src/link.txt").symlink_to(target)
            job = copy.deepcopy(baseline)
            job["authority"]["allowed_read_paths"] = ["src/link.txt"]
            with self.assertRaises(SecurityError) as caught:
                self.compile(root, job, role)
            self.assertEqual(caught.exception.details["reason_code"], "path.symlink")

            alias = root / "src/hardlink.txt"
            try:
                os.link(root / "src/example.py", alias)
            except OSError as error:
                self.skipTest(f"hard links unavailable: {error}")
            job = copy.deepcopy(baseline)
            job["authority"]["allowed_read_paths"] = ["src/hardlink.txt"]
            authority = self.compile(root, job, role)
            with self.assertRaises(SecurityError) as hardlink:
                ExecutionContext(authority).read_text("src/hardlink.txt")
            self.assertEqual(hardlink.exception.details["reason_code"], "path.hardlink")

    def test_nested_forbidden_directory_overrides_allowed_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, job, role = self.prepared(directory)
            job["authority"]["allowed_write_paths"] = ["src/**"]
            job["authority"]["forbidden_paths"] = ["src/private/**"]
            authority = self.compile(root, job, role)
            context = ExecutionContext(authority)
            with self.assertRaises(SecurityError) as caught:
                context.write_text("src/private/value.txt", "blocked\n")
            self.assertEqual(caught.exception.details["reason_code"], "execution.path_forbidden")

    def test_mutable_state_cannot_hide_under_skill_or_plugin_paths_with_windows_spelling(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for value in ("skills\\agentjob-control\\runtime", ".agents\\skills\\runtime", "plugins\\runtime"):
                config = valid_config()
                config["goal_relay"]["local_root"] = value
                path = root / "config.json"
                path.write_text(render_canonical_json(config), encoding="utf-8")
                with self.subTest(path=value), self.assertRaises(SecurityError) as caught:
                    load_config(root, config_path=path)
                self.assertEqual(caught.exception.details["reason_code"], "path.mutable_state_in_install")


if __name__ == "__main__":
    unittest.main()
