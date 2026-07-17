from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

from _support import valid_decision, valid_job, valid_role, valid_task
from agentjob_runtime.control.activation import activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import SecurityError, StateConflict
from agentjob_runtime.execution.compiler import compile_authority
from agentjob_runtime.execution.executor import InvocationBudget, capture_file_state, execute_one_job


CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


class OneJobExecutorTests(unittest.TestCase):
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
        decision = valid_decision()
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
            decision=decision,
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
        return root, store, job, role, authority

    def test_executes_one_job_and_returns_direct_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, store, _, _, authority = self.prepared(directory)
            budget = InvocationBudget()

            def operation(context):
                current = context.read_text("src/example.py")
                context.write_text("src/example.py", current.replace("1", "2"))
                return context.run_command("focused-tests").status

            evidence = execute_one_job(
                authority=authority,
                store=store,
                operation=operation,
                budget=budget,
            )
            self.assertEqual((root / "src/example.py").read_text(encoding="utf-8"), "value = 2\n")
            self.assertEqual(evidence.changed_paths, ("src/example.py",))
            self.assertEqual(evidence.command_results[0].status, "pass")
            self.assertEqual(evidence.operation_result, "pass")
            self.assertEqual(budget.attempted_job_ids, [authority.job_id])

    def test_second_attempt_is_blocked_by_hard_budget(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, authority = self.prepared(directory)
            budget = InvocationBudget()
            execute_one_job(
                authority=authority,
                store=store,
                operation=lambda context: None,
                budget=budget,
            )
            with self.assertRaises(StateConflict) as caught:
                execute_one_job(
                    authority=authority,
                    store=store,
                    operation=lambda context: None,
                    budget=budget,
                )
            self.assertEqual(caught.exception.details["reason_code"], "execution.one_job_limit")

    def test_unapproved_path_and_command_are_blocked_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, store, _, _, authority = self.prepared(directory)
            with self.assertRaises(SecurityError) as path_error:
                execute_one_job(
                    authority=authority,
                    store=store,
                    operation=lambda context: context.write_text("outside.txt", "blocked"),
                    budget=InvocationBudget(),
                )
            self.assertEqual(path_error.exception.details["reason_code"], "execution.write_not_allowed")
            with self.assertRaises(SecurityError) as command_error:
                execute_one_job(
                    authority=authority,
                    store=store,
                    operation=lambda context: context.run_command("not-approved"),
                    budget=InvocationBudget(),
                )
            self.assertEqual(command_error.exception.details["reason_code"], "execution.command_not_allowed")

    def test_stale_repository_or_control_authority_stops_before_operation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, store, job, _, authority = self.prepared(directory)
            _, fingerprint = capture_file_state(root)
            (root / "src/example.py").write_text("changed concurrently\n", encoding="utf-8")
            called = False

            def operation(context):
                nonlocal called
                called = True

            with self.assertRaises(StateConflict) as stale:
                execute_one_job(
                    authority=authority,
                    store=store,
                    operation=operation,
                    budget=InvocationBudget(),
                    expected_before_fingerprint=fingerprint,
                )
            self.assertFalse(called)
            self.assertEqual(stale.exception.details["reason_code"], "execution.stale_state_snapshot")

            task = store.load_task(job["task_id"])
            task["current_job_id"] = "AJ-OTHER-0001"
            store.write_mutable(store.task_path(job["task_id"]), task)
            with self.assertRaises(StateConflict) as changed:
                execute_one_job(
                    authority=authority,
                    store=store,
                    operation=operation,
                    budget=InvocationBudget(),
                )
            self.assertEqual(changed.exception.details["reason_code"], "execution.task_pointer_changed")

    def test_symlink_alias_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root, store, job, role, _ = self.prepared(directory)
            (Path(outside) / "secret.txt").write_text("secret\n", encoding="utf-8")
            (root / "src/link.txt").symlink_to(Path(outside) / "secret.txt")
            job = copy.deepcopy(job)
            job["authority"]["allowed_read_paths"].append("src/link.txt")
            # A newly broadened, unactivated record cannot compile against current hashes.
            with self.assertRaises(SecurityError):
                compile_authority(
                    project_root=root,
                    job=job,
                    execution_role=role,
                    activated_record_ids=store.activated_record_ids(),
                    runtime_capabilities=CAPABILITIES,
                )


if __name__ == "__main__":
    unittest.main()
