from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from _support import PACKAGE_ROOT, TS, valid_config, valid_job, valid_policy, valid_role, valid_task
from agentjob_runtime.continue_flow.director import DirectorRoute, resolve_director_packet
from agentjob_runtime.continue_flow.preflight import run_preflight
from agentjob_runtime.continue_flow.runner import run_continue
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.indexes import generate_indexes
from agentjob_runtime.execution.executor import capture_file_state
from agentjob_runtime.records.canonical import render_canonical_json


EXAMPLES = PACKAGE_ROOT.parents[1] / "examples" / "governed-continuation"
CONTROLS = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


class ContinueEndToEndTests(unittest.TestCase):
    def configured(self, root: Path, fixture_name: str):
        shutil.copytree(EXAMPLES / fixture_name, root, dirs_exist_ok=True)
        metadata = json.loads((root / "fixture.json").read_text(encoding="utf-8"))
        config = valid_config()
        config["project"]["id"] = metadata["fixture_id"]
        config["repository"]["provider"] = "test_fake"
        config["policy"]["packs"] = [".agents/control/policies/default.json"]
        config_path = root / "config.json"
        config_path.write_text(render_canonical_json(config), encoding="utf-8")
        policy_path = root / ".agents/control/policies/default.json"
        policy_path.parent.mkdir(parents=True, exist_ok=True)
        policy_path.write_text(render_canonical_json(valid_policy()), encoding="utf-8")
        store = FilesystemControlStore(root, ".agents/control")
        generate_indexes(store)
        repository = {
            "provider": "test_fake",
            "root": str(root),
            "worktree": str(root),
            "git_common_dir": None,
            "branch": "main",
            "revision": "fixture-revision-1",
            "status_porcelain": "",
        }
        return metadata, config_path, store, repository

    def task(self, store: FilesystemControlStore, *, gated: bool = False):
        task = valid_task()
        task["current_decision_id"] = None
        task["current_job_id"] = None
        task["next_recommended_action"] = "Select one bounded route."
        if gated:
            task["status"] = "human_gated"
            task["requires_human_gate"] = True
            task["human_gate_refs"] = [
                {"gate_id": "GATE-PUBLIC-RELEASE", "status": "required", "approval_ref": None}
            ]
        store.create_task(task)
        generate_indexes(store)
        return task

    def route(self, metadata, *, domain_validator: bool = False):
        job = valid_job()
        role = valid_role()
        job["authority"]["allowed_read_paths"] = list(metadata["read_paths"])
        job["authority"]["allowed_write_paths"] = [metadata["write_path"]]
        job["authority"]["allowed_generated_paths"] = [
            ".local/results/fixture.json"
        ]
        job["commands"]["approved"] = [
            {
                "command_id": "fixture-check",
                "argv": [sys.executable, "-c", "print('fixture verified')"],
                "cwd": metadata["command_cwd"],
                "environment": {},
                "network": False,
                "shell": False,
                "shell_policy_approval_ref": None,
                "timeout_seconds": 10,
            }
        ]
        job["expected_outputs"] = [
            {"path": metadata["write_path"], "kind": "controlled_source_change"}
        ]
        job["claim_boundary"] = {
            "allowed": [metadata["allowed_claim"]],
            "forbidden": [metadata["forbidden_claim"]],
        }
        job["completion_contract"] = {
            "required_evidence": [metadata["allowed_claim"]],
            "goal_effect": {
                "type": "bounded_progress",
                "does_not_imply_global_goal_completion": True,
            },
        }
        if domain_validator:
            job["validators"]["required"].append(
                {
                    "validator_id": "domain-check",
                    "validator_class": "domain_validation",
                    "mode": "required",
                }
            )
        job_spec = {
            "objective": f"Advance {metadata['fixture_id']} once.",
            "authority": copy.deepcopy(job["authority"]),
            "source_policy": copy.deepcopy(job["source_policy"]),
            "commands": copy.deepcopy(job["commands"]),
            "validators": copy.deepcopy(job["validators"]),
            "expected_outputs": copy.deepcopy(job["expected_outputs"]),
            "completion_contract": copy.deepcopy(job["completion_contract"]),
            "stop_conditions": copy.deepcopy(job["stop_conditions"]),
            "checkpoint": copy.deepcopy(job["checkpoint"]),
            "claim_boundary": copy.deepcopy(job["claim_boundary"]),
            "concurrency": copy.deepcopy(job["concurrency"]),
            "source_refs": list(metadata["read_paths"]),
            "extensions": {},
        }
        role_spec = {
            "binding_type": role["binding_type"],
            "responsibilities": ["Perform the declared fixture transaction."],
            "may_not": ["Broaden the activated authority."],
            "source_role_ref": role["source_role_ref"],
            "task_overlay": None,
            "authority_delta": "No permission expansion.",
            "provisional_role": None,
            "extensions": {},
        }
        return DirectorRoute(
            route_id=f"route-{metadata['fixture_id']}",
            role_id="software-engineer",
            role_version="1.0.0",
            priority=10,
            rationale="The route is bounded by the neutral fixture.",
            job_spec=job_spec,
            role_spec=role_spec,
        )

    @staticmethod
    def checkpoint(claim):
        def provider(specification, evidence):
            return {
                "provider": specification["provider"],
                "status": "pass",
                "revision": evidence.after_fingerprint,
                "evidence_ref": None,
                "claims": [claim],
            }

        return provider

    @staticmethod
    def operation(metadata, replacement):
        def perform(context):
            context.read_text(metadata["read_paths"][0])
            context.write_text(metadata["write_path"], replacement)
            context.run_command("fixture-check")

        return perform

    def invoke(
        self,
        root,
        metadata,
        config_path,
        repository,
        task,
        route,
        operation,
        **overrides,
    ):
        values = {
            "config_path": config_path,
            "task_id": task["task_id"],
            "repository_snapshot": repository,
            "routes": [route],
            "runtime_controls": CONTROLS,
            "operation": operation,
            "checkpoint_provider": self.checkpoint(metadata["allowed_claim"]),
            "proposed_claims": [metadata["allowed_claim"]],
            "policies": [valid_policy()],
            "timestamp": TS,
        }
        values.update(overrides)
        return run_continue(root, **values)

    def test_new_decision_executes_exactly_one_software_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            metadata, config, store, repository = self.configured(
                root, "minimal-software-project"
            )
            task = self.task(store)
            outcome = self.invoke(
                root,
                metadata,
                config,
                repository,
                task,
                self.route(metadata),
                self.operation(metadata, "value=2\n"),
            )
            self.assertEqual(outcome.result["boundary_entered"], "director_decision_required")
            self.assertEqual(outcome.result["agent_jobs_executed"], 1)
            self.assertEqual((root / "src/value.txt").read_text(encoding="utf-8"), "value=2\n")
            jobs = [record for kind, _, record in store.iter_records() if kind == "agent_job"]
            self.assertEqual(len(jobs), 1)

    def test_existing_activated_job_is_reused_without_duplicate_packet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            metadata, config, store, repository = self.configured(
                root, "minimal-software-project"
            )
            task = self.task(store)
            preflight = run_preflight(
                root,
                config_path=config,
                task_id=task["task_id"],
                repository_snapshot=repository,
            )
            resolve_director_packet(
                preflight,
                store=store,
                routes=[self.route(metadata)],
                expected_revision=1,
                policies=[valid_policy()],
                timestamp=TS,
            )
            outcome = self.invoke(
                root,
                metadata,
                config,
                repository,
                task,
                self.route(metadata),
                self.operation(metadata, "value=2\n"),
            )
            self.assertEqual(outcome.result["boundary_entered"], "existing_agent_job_ready")
            self.assertEqual(outcome.director["status"], "reused")
            decisions = [record for kind, _, record in store.iter_records() if kind == "director_decision"]
            self.assertEqual(len(decisions), 1)

    def test_execution_fingerprint_excludes_configured_goal_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            metadata, config, store, repository = self.configured(
                root, "minimal-software-project"
            )
            task = self.task(store)
            route = self.route(metadata)
            preflight = run_preflight(
                root,
                config_path=config,
                task_id=task["task_id"],
                repository_snapshot=repository,
            )
            resolve_director_packet(
                preflight,
                store=store,
                routes=[route],
                expected_revision=1,
                policies=[valid_policy()],
                timestamp=TS,
            )
            local_state = root / ".local/sys4ai/continuation/relay-state.json"
            local_state.parent.mkdir(parents=True, exist_ok=True)
            local_state.write_text('{"phase":"claimed"}\n', encoding="utf-8")
            _, expected_before = capture_file_state(
                root,
                ignored_roots=[".local/sys4ai/continuation"],
            )

            def operation(context):
                local_state.write_text('{"phase":"returned"}\n', encoding="utf-8")
                context.read_text(metadata["read_paths"][0])
                context.write_text(metadata["write_path"], "value=2\n")
                context.run_command("fixture-check")

            outcome = self.invoke(
                root,
                metadata,
                config,
                repository,
                task,
                route,
                operation,
            )
            self.assertEqual(outcome.result["status"], "completed")
            self.assertEqual(outcome.execution["before_fingerprint"], expected_before)
            self.assertNotIn(
                ".local/sys4ai/continuation/relay-state.json",
                outcome.execution["changed_paths"],
            )

    def test_human_gate_and_no_action_execute_zero_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            metadata, config, store, repository = self.configured(
                root, "minimal-software-project"
            )
            task = self.task(store, gated=True)
            called = False

            def operation(context):
                nonlocal called
                called = True

            gated = self.invoke(
                root,
                metadata,
                config,
                repository,
                task,
                self.route(metadata),
                operation,
            )
            self.assertEqual(gated.result["status"], "human_gate_required")
            self.assertEqual(gated.result["agent_jobs_executed"], 0)
            self.assertFalse(called)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            _, config, _, repository = self.configured(root, "minimal-software-project")
            no_action = run_continue(
                root,
                config_path=config,
                repository_snapshot=repository,
            )
            self.assertEqual(no_action.result["status"], "no_action")
            self.assertEqual(no_action.result["agent_jobs_executed"], 0)

    def test_validation_failure_is_failed_evidence_not_success(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            metadata, config, store, repository = self.configured(
                root, "minimal-software-project"
            )
            task = self.task(store)
            outcome = self.invoke(
                root,
                metadata,
                config,
                repository,
                task,
                self.route(metadata),
                lambda context: context.run_command("fixture-check"),
            )
            self.assertEqual(outcome.result["status"], "failed")
            self.assertEqual(outcome.result["agent_jobs_executed"], 1)
            self.assertEqual(outcome.finalization.completion["status"], "failed")
            self.assertEqual(
                outcome.finalization.completion["claim_summary"]["allowed_conclusions"], []
            )

    def test_documentation_fixture_preserves_source_derivative_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            metadata, config, store, repository = self.configured(
                root, "documentation-project"
            )
            task = self.task(store)
            replacement = "# Guide\n\nPortable controls require explicit authority before execution.\n"
            outcome = self.invoke(
                root,
                metadata,
                config,
                repository,
                task,
                self.route(metadata),
                self.operation(metadata, replacement),
            )
            self.assertEqual(outcome.result["status"], "completed")
            self.assertEqual((root / "docs/guide.md").read_text(encoding="utf-8"), replacement)
            self.assertIn("canonical/source.md", outcome.execution["accessed_paths"])

    def test_research_fixture_does_not_promote_process_completion_to_truth(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            metadata, config, store, repository = self.configured(
                root, "research-note-project"
            )
            task = self.task(store)
            replacement = (
                "# Research Note\n\nSource: sources/observation.md. "
                "No domain conclusion is asserted.\n"
            )
            outcome = self.invoke(
                root,
                metadata,
                config,
                repository,
                task,
                self.route(metadata, domain_validator=True),
                self.operation(metadata, replacement),
                validator_adapters={
                    "domain-check": lambda authority, evidence: {
                        "status": "indeterminate",
                        "reason_code": "domain.insufficient_evidence",
                        "notes": ["The process check does not establish the hypothesis."],
                    }
                },
            )
            self.assertEqual(outcome.result["status"], "completed_with_warnings")
            self.assertEqual(outcome.result["global_goal_evaluation"], "indeterminate")
            completion = outcome.finalization.completion
            self.assertEqual(
                completion["claim_summary"]["allowed_conclusions"],
                [metadata["allowed_claim"]],
            )
            self.assertIn(
                metadata["forbidden_claim"],
                completion["claim_summary"]["forbidden_overread"],
            )


if __name__ == "__main__":
    unittest.main()
