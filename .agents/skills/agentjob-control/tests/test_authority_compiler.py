from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS, valid_job, valid_role
from agentjob_runtime.errors import SecurityError, StateConflict
from agentjob_runtime.execution.compiler import compile_authority


CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


class AuthorityCompilerTests(unittest.TestCase):
    def prepared(self, directory: str):
        root = Path(directory).resolve()
        (root / "src").mkdir()
        (root / "tests").mkdir()
        (root / "src/example.py").write_text("value = 1\n", encoding="utf-8")
        job = valid_job()
        role = valid_role()
        activated = {job["job_id"], role["execution_role_id"]}
        return root, job, role, activated

    def test_compilation_is_read_only_and_preserves_exact_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, job, role, activated = self.prepared(directory)
            before = {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}
            plan = compile_authority(
                project_root=root,
                job=job,
                execution_role=role,
                activated_record_ids=activated,
                runtime_capabilities=CAPABILITIES,
            )
            self.assertEqual(
                [item.relative for item in plan.allowed_write_paths],
                job["authority"]["allowed_write_paths"],
            )
            self.assertEqual(plan.commands[0].argv, tuple(job["commands"]["approved"][0]["argv"]))
            self.assertEqual(plan.commands[0].environment, {})
            after = {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}
            self.assertEqual(before, after)

    def test_missing_required_control_stops_compilation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, job, role, activated = self.prepared(directory)
            capabilities = {**CAPABILITIES, "network_control": False}
            with self.assertRaises(SecurityError) as caught:
                compile_authority(
                    project_root=root,
                    job=job,
                    execution_role=role,
                    activated_record_ids=activated,
                    runtime_capabilities=capabilities,
                )
            self.assertIn("network_control", caught.exception.details["missing_controls"])

    def test_unactivated_or_expanding_role_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, job, role, activated = self.prepared(directory)
            with self.assertRaises(StateConflict):
                compile_authority(
                    project_root=root,
                    job=job,
                    execution_role=role,
                    activated_record_ids={job["job_id"]},
                    runtime_capabilities=CAPABILITIES,
                )
            role["binding_type"] = "task_overlay"
            role["task_overlay"] = {
                "added_constraints": [],
                "removed_permissions": [],
                "expanded_permissions": ["write:anywhere"],
                "justification": "Not allowed.",
            }
            with self.assertRaises(SecurityError):
                compile_authority(
                    project_root=root,
                    job=job,
                    execution_role=role,
                    activated_record_ids=activated,
                    runtime_capabilities=CAPABILITIES,
                )

    def test_command_network_and_expected_output_cannot_exceed_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, job, role, activated = self.prepared(directory)
            job["commands"]["approved"][0]["network"] = True
            with self.assertRaises(SecurityError):
                compile_authority(
                    project_root=root,
                    job=job,
                    execution_role=role,
                    activated_record_ids=activated,
                    runtime_capabilities=CAPABILITIES,
                )
            job = valid_job()
            job["expected_outputs"][0]["path"] = "outside.txt"
            with self.assertRaises(SecurityError):
                compile_authority(
                    project_root=root,
                    job=job,
                    execution_role=role,
                    activated_record_ids=activated,
                    runtime_capabilities=CAPABILITIES,
                )


if __name__ == "__main__":
    unittest.main()
