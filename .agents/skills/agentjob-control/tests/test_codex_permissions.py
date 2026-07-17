from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS, valid_job, valid_role
from agentjob_runtime.adapters.codex_permissions import (
    CodexRuntimeCapabilities,
    compile_codex_permissions,
)
from agentjob_runtime.errors import BootstrapRequired
from agentjob_runtime.execution.compiler import compile_authority


EXECUTION_CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


def runtime(**overrides):
    values = {
        "surface": "desktop",
        "working_directory": True,
        "writable_roots": True,
        "network_control": True,
        "approval_policy": True,
        "tool_allowlist": True,
        "required_skill_mentions": True,
        "command_budget": True,
        "fine_grained_path_exclusions": True,
    }
    values.update(overrides)
    return CodexRuntimeCapabilities(**values)


class CodexPermissionTests(unittest.TestCase):
    def authority(self, directory: str, *, nested_forbidden=False):
        root = Path(directory).resolve()
        (root / "src").mkdir()
        (root / "tests").mkdir()
        (root / "src/example.py").write_text("value = 1\n", encoding="utf-8")
        job = valid_job()
        if nested_forbidden:
            job["authority"]["allowed_write_paths"] = ["src/"]
            job["authority"]["forbidden_paths"] = ["src/private.txt"]
        role = valid_role()
        return compile_authority(
            project_root=root,
            job=job,
            execution_role=role,
            activated_record_ids={job["job_id"], role["execution_role_id"]},
            runtime_capabilities=EXECUTION_CAPABILITIES,
        )

    def test_mapping_preserves_exact_roots_network_tools_and_required_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            authority = self.authority(directory)
            plan = compile_codex_permissions(
                authority,
                capabilities=runtime(),
                required_skills=["continue"],
            )
            self.assertEqual(plan.status, "ready")
            self.assertEqual(
                plan.writable_roots,
                tuple(
                    item.absolute
                    for item in (*authority.allowed_write_paths, *authority.allowed_generated_paths)
                ),
            )
            self.assertEqual(plan.network, "disabled")
            self.assertEqual(plan.approval_policy, "deny_unlisted")
            self.assertEqual(plan.required_skills, ("continue",))
            self.assertEqual(plan.maximum_agentjobs, 1)
            self.assertTrue(plan.post_execution_path_validation_required)

    def test_mapping_never_invents_tools_or_writable_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            authority = self.authority(directory)
            plan = compile_codex_permissions(authority, capabilities=runtime())
            self.assertNotIn(authority.project_root, plan.writable_roots)
            self.assertEqual(
                set(plan.allowed_tools),
                {"filesystem.read", "filesystem.write", "terminal.command"},
            )

    def test_missing_mandatory_runtime_control_blocks_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            authority = self.authority(directory)
            with self.assertRaises(BootstrapRequired) as captured:
                compile_codex_permissions(
                    authority,
                    capabilities=runtime(network_control=False),
                )
            self.assertIn(
                "network_control",
                captured.exception.details["unsupported_restrictions"],
            )

    def test_coarse_path_exclusion_requires_local_enforcement_or_blocks_when_mandatory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            authority = self.authority(directory, nested_forbidden=True)
            plan = compile_codex_permissions(
                authority,
                capabilities=runtime(fine_grained_path_exclusions=False),
            )
            self.assertEqual(plan.status, "ready_with_local_enforcement")
            self.assertTrue(plan.requires_local_executor)
            self.assertIn("fine_grained_path_exclusions", plan.unsupported_restrictions)
            with self.assertRaises(BootstrapRequired):
                compile_codex_permissions(
                    authority,
                    capabilities=runtime(fine_grained_path_exclusions=False),
                    mandatory_runtime_restrictions=["fine_grained_path_exclusions"],
                )

    def test_missing_required_skill_or_tool_capability_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            authority = self.authority(directory)
            with self.assertRaises(BootstrapRequired):
                compile_codex_permissions(
                    authority,
                    capabilities=runtime(required_skill_mentions=False),
                    required_skills=["continue"],
                )
            with self.assertRaises(BootstrapRequired):
                compile_codex_permissions(
                    authority,
                    capabilities=runtime(available_tools=("filesystem.read",)),
                )


if __name__ == "__main__":
    unittest.main()
