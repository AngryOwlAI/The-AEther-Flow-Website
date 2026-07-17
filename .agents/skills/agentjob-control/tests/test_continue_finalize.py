from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from _support import TS, valid_decision, valid_job, valid_role, valid_task
from agentjob_runtime.continue_flow.finalize import (
    HandoffPlan,
    finalize_execution,
    finalize_no_action,
)
from agentjob_runtime.control.activation import activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import StateConflict
from agentjob_runtime.execution.compiler import compile_authority
from agentjob_runtime.execution.executor import InvocationBudget, execute_one_job
from agentjob_runtime.execution.validation import PostExecutionReport, validate_execution


CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


class ContinueFinalizeTests(unittest.TestCase):
    def prepared(self, directory: str):
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

        def operation(context):
            context.write_text("src/example.py", "value = 2\n")
            context.run_command("focused-tests")

        evidence = execute_one_job(
            authority=authority,
            store=store,
            operation=operation,
            budget=InvocationBudget(),
        )
        report = validate_execution(
            authority=authority,
            evidence=evidence,
            checkpoint_provider=lambda specification, evidence: {
                "provider": "git_status",
                "status": "pass",
                "revision": evidence.after_fingerprint,
                "evidence_ref": None,
                "claims": ["The bounded fixture passes."],
            },
            proposed_claims=["The bounded fixture passes."],
        )
        return root, store, authority, evidence, report

    def test_finalizes_canonical_completion_handoff_indexes_and_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, authority, evidence, report = self.prepared(directory)
            outcome = finalize_execution(
                store=store,
                boundary_entered="existing_agent_job_ready",
                authority=authority,
                evidence=evidence,
                validation=report,
                expected_revision=2,
                started_at=TS,
                completed_at="2026-07-17T15:01:00Z",
                handoff_plan=HandoffPlan(
                    "The bounded change completed.",
                    ("Made the bounded change.",),
                    ("Evaluate the next step.",),
                    "Evaluate the next legal step.",
                    "system-director",
                    "goal-evaluation",
                    ("A new job is required before execution.",),
                ),
            )
            self.assertEqual(outcome.result["agent_jobs_executed"], 1)
            self.assertEqual(
                outcome.result["completion_id"], outcome.completion["completion_id"]
            )
            self.assertEqual(
                outcome.completion_receipt["sha256"], outcome.completion_sha256
            )
            self.assertEqual(outcome.handoff_receipt["sha256"], outcome.handoff_sha256)
            self.assertFalse(outcome.handoff["grants_execution_authority"])
            self.assertEqual(store.load_task(authority.task_id)["revision"], 4)

    def test_failed_validation_creates_only_failed_bounded_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, authority, evidence, report = self.prepared(directory)
            failed = PostExecutionReport(
                "validation_failed",
                "validation.required_check_failed",
                report.job_id,
                report.changed_paths,
                report.outputs,
                report.command_results,
                report.validator_results,
                report.checkpoint,
                report.proposed_claims,
                False,
            )
            outcome = finalize_execution(
                store=store,
                boundary_entered="existing_agent_job_ready",
                authority=authority,
                evidence=evidence,
                validation=failed,
                expected_revision=2,
                started_at=TS,
            )
            completions = [
                record
                for kind, _, record in store.iter_records()
                if kind == "completion"
            ]
            self.assertEqual(len(completions), 1)
            self.assertEqual(completions[0]["status"], "failed")
            self.assertEqual(completions[0]["claim_summary"]["allowed_conclusions"], [])
            self.assertEqual(outcome.result["status"], "failed")
            self.assertEqual(outcome.result["progress_effect"], "blocked_evidence")

    def test_no_action_is_read_only_and_creates_no_fake_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / "marker.txt"
            marker.write_text("stable\n", encoding="utf-8")
            before = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            outcome = finalize_no_action(
                boundary_entered="no_action",
                reason_code="task.none_active",
                repository_fingerprint="a" * 64,
                next_recommended_action="No action is required.",
            )
            after = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(before, after)
            self.assertEqual(outcome.result["agent_jobs_executed"], 0)
            self.assertIsNone(outcome.result["completion_id"])


if __name__ == "__main__":
    unittest.main()
