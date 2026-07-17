from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from _support import valid_decision, valid_job, valid_role, valid_task
from agentjob_runtime.control.activation import activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.execution.compiler import compile_authority
from agentjob_runtime.execution.executor import InvocationBudget, execute_one_job
from agentjob_runtime.execution.validation import validate_execution


CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


class PostExecutionValidationTests(unittest.TestCase):
    def prepared(self, directory: str, *, domain_validator: bool = False):
        root = Path(directory).resolve()
        (root / "src").mkdir()
        (root / "tests").mkdir()
        (root / "src/example.py").write_text("value = 1\n", encoding="utf-8")
        (root / "tests/test_example.py").write_text("fixture = True\n", encoding="utf-8")
        store = FilesystemControlStore(root, ".agents/control")
        task = valid_task()
        task["current_decision_id"] = None
        task["current_job_id"] = None
        store.create_task(task)
        job = valid_job()
        job["commands"]["approved"][0] = {
            "command_id": "focused-tests",
            "argv": [sys.executable, "-c", "print('verified')"],
            "cwd": "src",
            "environment": {},
            "network": False,
            "shell": False,
            "shell_policy_approval_ref": None,
            "timeout_seconds": 10,
        }
        if domain_validator:
            job["validators"]["required"].append(
                {
                    "validator_id": "domain-check",
                    "validator_class": "domain_validation",
                    "mode": "required",
                }
            )
        role = valid_role()
        activate_packet(
            store,
            task_id=task["task_id"],
            decision=valid_decision(),
            job=job,
            execution_role=role,
            expected_revision=1,
        )
        authority = compile_authority(
            project_root=root,
            job=job,
            execution_role=role,
            activated_record_ids=store.activated_record_ids(),
            runtime_capabilities=CAPABILITIES,
        )
        return root, store, authority

    @staticmethod
    def operation(context):
        context.write_text("src/example.py", "value = 2\n")
        context.run_command("focused-tests")

    @staticmethod
    def checkpoint(specification, evidence):
        return {
            "provider": specification["provider"],
            "status": "pass",
            "revision": evidence.after_fingerprint,
            "evidence_ref": None,
            "claims": ["The bounded fixture passes."],
        }

    def test_validates_paths_outputs_commands_claims_and_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, authority = self.prepared(directory)
            evidence = execute_one_job(
                authority=authority,
                store=store,
                operation=self.operation,
                budget=InvocationBudget(),
            )
            report = validate_execution(
                authority=authority,
                evidence=evidence,
                checkpoint_provider=self.checkpoint,
                proposed_claims=["The bounded fixture passes."],
            )
            self.assertTrue(report.successful)
            self.assertEqual(report.outputs[0]["sha256"], evidence.after_files["src/example.py"])
            self.assertEqual(report.checkpoint["status"], "pass")

    def test_unapproved_direct_write_fails_post_execution_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, store, authority = self.prepared(directory)

            def bypassing_operation(context):
                self.operation(context)
                (root / "outside.txt").write_text("not approved\n", encoding="utf-8")

            evidence = execute_one_job(
                authority=authority,
                store=store,
                operation=bypassing_operation,
                budget=InvocationBudget(),
            )
            report = validate_execution(
                authority=authority,
                evidence=evidence,
                checkpoint_provider=self.checkpoint,
                proposed_claims=["The bounded fixture passes."],
            )
            self.assertEqual(report.status, "validation_failed")
            path_result = next(
                item for item in report.validator_results if item["validator_id"] == "changed-path-allowlist"
            )
            self.assertEqual(path_result["status"], "fail")

    def test_missing_output_and_command_prevent_success(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, authority = self.prepared(directory)
            evidence = execute_one_job(
                authority=authority,
                store=store,
                operation=lambda context: None,
                budget=InvocationBudget(),
            )
            report = validate_execution(
                authority=authority,
                evidence=evidence,
                checkpoint_provider=self.checkpoint,
                proposed_claims=["The bounded fixture passes."],
            )
            self.assertEqual(report.status, "validation_failed")
            self.assertFalse(report.successful)

    def test_domain_indeterminacy_is_not_process_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, authority = self.prepared(directory, domain_validator=True)
            evidence = execute_one_job(
                authority=authority,
                store=store,
                operation=self.operation,
                budget=InvocationBudget(),
            )
            report = validate_execution(
                authority=authority,
                evidence=evidence,
                validator_adapters={
                    "domain-check": lambda authority, evidence: {
                        "status": "indeterminate",
                        "reason_code": "domain.insufficient_evidence",
                        "notes": ["Process completion does not establish domain truth."],
                    }
                },
                checkpoint_provider=self.checkpoint,
                proposed_claims=["The bounded fixture passes."],
            )
            self.assertEqual(report.status, "domain_indeterminate")
            self.assertTrue(report.domain_indeterminate)

    def test_checkpoint_cannot_broaden_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, authority = self.prepared(directory)
            evidence = execute_one_job(
                authority=authority,
                store=store,
                operation=self.operation,
                budget=InvocationBudget(),
            )

            def broad_checkpoint(specification, evidence):
                value = self.checkpoint(specification, evidence)
                value["claims"] = ["The entire target system is proven correct."]
                return value

            report = validate_execution(
                authority=authority,
                evidence=evidence,
                checkpoint_provider=broad_checkpoint,
                proposed_claims=["The bounded fixture passes."],
            )
            self.assertEqual(report.status, "checkpoint_failed")
            self.assertFalse(report.successful)


if __name__ == "__main__":
    unittest.main()
