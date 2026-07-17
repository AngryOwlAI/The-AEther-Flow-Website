from __future__ import annotations

import copy
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from _support import valid_job, valid_role
from agentjob_runtime.errors import RecordValidationError, SecurityError
from agentjob_runtime.execution.compiler import compile_authority
from agentjob_runtime.execution.executor import MAX_CAPTURE_BYTES, ExecutionContext


CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


def command(command_id: str, code: str, *, timeout: int = 10, environment=None, shell=False, network=False):
    return {
        "command_id": command_id,
        "argv": [sys.executable, "-c", code],
        "cwd": "src",
        "environment": dict(environment or {}),
        "network": network,
        "shell": shell,
        "shell_policy_approval_ref": "APPROVAL-SHELL-001" if shell else None,
        "timeout_seconds": timeout,
    }


class CommandSecurityTests(unittest.TestCase):
    def prepared(self, directory: str, commands, *, capabilities=None):
        root = Path(directory).resolve()
        (root / "src").mkdir()
        (root / "tests").mkdir()
        (root / "src/example.py").write_text("value = 1\n", encoding="utf-8")
        job = valid_job()
        job["commands"]["approved"] = list(commands)
        role = valid_role()
        authority = compile_authority(
            project_root=root,
            job=job,
            execution_role=role,
            activated_record_ids={job["job_id"], role["execution_role_id"]},
            runtime_capabilities=capabilities or CAPABILITIES,
        )
        return root, job, role, authority

    def test_shell_metacharacters_in_argv_remain_literal_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            marker = root / "shell-injection.txt"
            payload = f"; touch {marker}"
            cmd = {
                **command("literal-argument", "import sys; print(sys.argv[1])"),
                "argv": [sys.executable, "-c", "import sys; print(sys.argv[1])", payload],
            }
            _, _, _, authority = self.prepared(directory, [cmd])
            evidence = ExecutionContext(authority).run_command("literal-argument")
            self.assertEqual(evidence.status, "pass")
            self.assertEqual(evidence.stdout.strip(), payload)
            self.assertFalse(marker.exists())

    def test_parent_environment_is_not_inherited_and_only_declared_values_exist(self) -> None:
        code = "import os; print(os.environ.get('PARENT_SECRET', 'missing')); print(os.environ['DECLARED'])"
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ, {"PARENT_SECRET": "must-not-leak"}, clear=False
        ):
            _, _, _, authority = self.prepared(
                directory,
                [command("environment", code, environment={"DECLARED": "present"})],
            )
            evidence = ExecutionContext(authority).run_command("environment")
            self.assertEqual(evidence.stdout.splitlines(), ["missing", "present"])

    def test_command_cwd_escape_and_embedded_secrets_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "src").mkdir()
            (root / "tests").mkdir()
            job = valid_job()
            role = valid_role()
            for cwd in ("../outside", "..\\outside", "C:\\outside"):
                candidate = copy.deepcopy(job)
                candidate["commands"]["approved"][0]["cwd"] = cwd
                with self.subTest(cwd=cwd), self.assertRaises((RecordValidationError, SecurityError)):
                    compile_authority(
                        project_root=root,
                        job=candidate,
                        execution_role=role,
                        activated_record_ids={candidate["job_id"], role["execution_role_id"]},
                        runtime_capabilities=CAPABILITIES,
                    )
            secret_job = copy.deepcopy(job)
            secret_job["commands"]["approved"][0]["environment"] = {
                "TOKEN": "sk-proj-abcdefghijklmnopqrstuvwxyz"
            }
            with self.assertRaises(SecurityError) as caught:
                compile_authority(
                    project_root=root,
                    job=secret_job,
                    execution_role=role,
                    activated_record_ids={secret_job["job_id"], role["execution_role_id"]},
                    runtime_capabilities=CAPABILITIES,
                )
            self.assertEqual(caught.exception.details["reason_code"], "execution.command_secret_detected")

    def test_network_authority_and_enforcement_capability_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "src").mkdir()
            (root / "tests").mkdir()
            job = valid_job()
            role = valid_role()
            job["commands"]["approved"][0]["network"] = True
            with self.assertRaises(SecurityError):
                compile_authority(
                    project_root=root,
                    job=job,
                    execution_role=role,
                    activated_record_ids={job["job_id"], role["execution_role_id"]},
                    runtime_capabilities=CAPABILITIES,
                )
            job["commands"]["approved"][0]["network"] = False
            capabilities = {**CAPABILITIES, "network_control": False}
            with self.assertRaises(SecurityError) as caught:
                compile_authority(
                    project_root=root,
                    job=job,
                    execution_role=role,
                    activated_record_ids={job["job_id"], role["execution_role_id"]},
                    runtime_capabilities=capabilities,
                )
            self.assertIn("network_control", caught.exception.details["missing_controls"])

    def test_timeout_output_limit_and_secret_redaction_are_durable_evidence_controls(self) -> None:
        commands = [
            command("timeout", "import time; time.sleep(2)", timeout=1),
            command("large-output", f"print('x' * {MAX_CAPTURE_BYTES * 2})"),
            command(
                "redaction",
                "print('sk-' + 'proj-' + 'a' * 28); print('password' + '=' + 'super-secret')",
            ),
        ]
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, authority = self.prepared(directory, commands)
            context = ExecutionContext(authority)
            timeout = context.run_command("timeout")
            self.assertEqual(timeout.status, "timeout")
            self.assertEqual(timeout.exit_code, 124)
            large = context.run_command("large-output")
            self.assertTrue(large.stdout_truncated)
            self.assertLessEqual(len(large.stdout.encode("utf-8")), MAX_CAPTURE_BYTES)
            redacted = context.run_command("redaction")
            self.assertNotIn("sk-proj-", redacted.stdout)
            self.assertNotIn("super-secret", redacted.stdout)
            self.assertGreaterEqual(redacted.stdout.count("[REDACTED]"), 2)

    def test_shell_mode_requires_declared_capability_and_a_separate_adapter(self) -> None:
        shell_command = command("shell", "print('not executed')", shell=True)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(SecurityError) as caught:
                self.prepared(
                    directory,
                    [shell_command],
                    capabilities={**CAPABILITIES, "shell_execution": False},
                )
            self.assertIn("shell_execution", caught.exception.details["missing_controls"])
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, authority = self.prepared(directory, [shell_command])
            with self.assertRaises(SecurityError) as caught:
                ExecutionContext(authority).run_command("shell")
            self.assertEqual(caught.exception.details["reason_code"], "execution.shell_adapter_required")


if __name__ == "__main__":
    unittest.main()
