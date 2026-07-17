from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, HASH_B, PACKAGE_ROOT, TS, valid_config
from agentjob_runtime.records.canonical import render_canonical_json


CLI = PACKAGE_ROOT / "scripts" / "agentjobctl.py"
GOAL_ID = "CG-20260717T150000Z-55667788"


class GoalCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(CLI), *map(str, arguments)],
            text=True,
            capture_output=True,
            check=False,
        )

    def write_json(self, root: Path, name: str, value):
        path = root / name
        path.write_text(render_canonical_json(value), encoding="utf-8")
        return path

    def prepared(self, directory: str):
        root = Path(directory).resolve()
        config = self.write_json(root, "config.json", valid_config())
        contract = self.write_json(
            root,
            "contract.json",
            {
                "interpretation": "The fixture is complete when its test passes.",
                "required_evidence": ["Tests pass."],
                "user_confirmed_when_ambiguous": True,
            },
        )
        guards = self.write_json(
            root,
            "guards.json",
            {"max_continue_passes": 3, "deadline_at": "2099-01-01T00:00:00Z"},
        )
        binding = self.write_json(
            root,
            "binding.json",
            {
                "project_id": "cli-fixture",
                "root": str(root),
                "worktree": str(root),
                "branch": "main",
                "git_common_dir": None,
                "starting_revision": "A",
                "environment_mode": "local",
            },
        )
        tokens = {}
        for name, character in (("launcher", "l"), ("handoff", "h"), ("claim", "c")):
            path = root / f"{name}.token"
            path.write_text(character * 48 + "\n", encoding="utf-8")
            tokens[name] = path
        return root, config, contract, guards, binding, tokens

    def initialize(self, root, config, contract, guards, binding, tokens):
        return self.run_cli(
            "goal",
            "initialize",
            "--project-root",
            root,
            "--config",
            config,
            "--goal-text",
            "Complete the CLI fixture.",
            "--completion-contract",
            contract,
            "--guards",
            guards,
            "--repository-binding",
            binding,
            "--initial-fingerprint",
            HASH_A,
            "--goal-id",
            GOAL_ID,
            "--launcher-token-file",
            tokens["launcher"],
            "--fresh-recursive-threads-explicitly-requested",
            "--timestamp",
            TS,
            "--json",
        )

    @staticmethod
    def tree_bytes(root: Path):
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }

    def test_goal_help_lists_public_and_advanced_operations(self) -> None:
        result = self.run_cli("goal", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in (
            "initialize",
            "status",
            "export",
            "reserve-successor",
            "record-successor",
            "claim",
            "consume",
            "returned",
            "unknown",
            "verify",
            "decide",
            "recover",
            "amend-contract",
            "amend-guards",
            "cancel",
        ):
            self.assertIn(name, result.stdout)
        self.assertIn("Advanced", result.stdout)

    def test_initialize_status_and_export_are_structured_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, config, contract, guards, binding, tokens = self.prepared(directory)
            initialized = self.initialize(root, config, contract, guards, binding, tokens)
            self.assertEqual(initialized.returncode, 0, initialized.stdout + initialized.stderr)
            payload = json.loads(initialized.stdout)
            self.assertEqual(payload["goal_id"], GOAL_ID)
            self.assertEqual(payload["revision"], 1)
            self.assertNotIn("l" * 48, initialized.stdout)
            before = self.tree_bytes(root)
            status = self.run_cli(
                "goal",
                "status",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--json",
            )
            export_one = self.run_cli(
                "goal",
                "export",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--json",
            )
            export_two = self.run_cli(
                "goal",
                "export",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--json",
            )
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertEqual(export_one.returncode, 0, export_one.stderr)
            self.assertEqual(export_one.stdout, export_two.stdout)
            self.assertEqual(before, self.tree_bytes(root))
            self.assertIn("<redacted>", export_one.stdout)
            self.assertNotIn("l" * 48, export_one.stdout)

    def test_full_internal_lifecycle_requires_revisions_and_phase_checks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, config, contract, guards, binding, tokens = self.prepared(directory)
            self.assertEqual(
                self.initialize(root, config, contract, guards, binding, tokens).returncode,
                0,
            )
            missing_revision = self.run_cli(
                "goal",
                "reserve-successor",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--holder-token-file",
                tokens["launcher"],
            )
            self.assertEqual(missing_revision.returncode, 2)
            misuse = self.run_cli(
                "goal",
                "consume",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--generation",
                1,
                "--expected-revision",
                1,
                "--claim-token-file",
                tokens["claim"],
                "--json",
            )
            self.assertEqual(misuse.returncode, 5)

            reserve = self.run_cli(
                "goal",
                "reserve-successor",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--expected-revision",
                1,
                "--holder-token-file",
                tokens["launcher"],
                "--handoff-token-file",
                tokens["handoff"],
                "--predecessor-thread-id",
                "thread-launcher",
                "--timestamp",
                TS,
                "--json",
            )
            self.assertEqual(reserve.returncode, 0, reserve.stdout + reserve.stderr)
            response = self.write_json(root, "provider.json", {"status": "created"})
            recorded = self.run_cli(
                "goal",
                "record-successor",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--generation",
                1,
                "--expected-revision",
                2,
                "--handoff-token-file",
                tokens["handoff"],
                "--successor-thread-id",
                "thread-generation-1",
                "--provider-id",
                "test-fake",
                "--provider-response",
                response,
                "--timestamp",
                TS,
                "--json",
            )
            self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
            claimed = self.run_cli(
                "goal",
                "claim",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--generation",
                1,
                "--expected-revision",
                3,
                "--handoff-token-file",
                tokens["handoff"],
                "--idempotency-key",
                f"{GOAL_ID}:1",
                "--successor-thread-id",
                "thread-generation-1",
                "--claim-token-file",
                tokens["claim"],
                "--timestamp",
                TS,
                "--json",
            )
            self.assertEqual(claimed.returncode, 0, claimed.stdout + claimed.stderr)
            consumed = self.run_cli(
                "goal",
                "consume",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--generation",
                1,
                "--expected-revision",
                4,
                "--claim-token-file",
                tokens["claim"],
                "--timestamp",
                TS,
                "--json",
            )
            self.assertEqual(consumed.returncode, 0, consumed.stdout + consumed.stderr)

            result_path = self.write_json(
                root,
                "continue-result.json",
                {
                    "schema_version": "sys4ai.continue-result.v1",
                    "status": "completed",
                    "boundary_entered": "existing_agent_job_ready",
                    "agent_jobs_executed": 1,
                    "task_id": "TASK-1",
                    "decision_id": "DDR-1",
                    "job_id": "AJ-1",
                    "completion_id": "AJC-1",
                    "handoff_id": None,
                    "progress_effect": "bounded_completion",
                    "global_goal_evaluation": "not_evaluated_here",
                    "repository_fingerprint_before": HASH_A,
                    "repository_fingerprint_after": HASH_B,
                    "validators": {
                        "required": 1,
                        "passed": 1,
                        "failed": 0,
                        "warning": 0,
                        "skipped": 0,
                    },
                    "next_recommended_action": "Evaluate the goal.",
                    "execution_performed": True,
                    "reason_code": "goal.checked",
                    "extensions": {},
                },
            )
            returned = self.run_cli(
                "goal",
                "returned",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--generation",
                1,
                "--expected-revision",
                5,
                "--claim-token-file",
                tokens["claim"],
                "--continue-result",
                result_path,
                "--timestamp",
                TS,
                "--json",
            )
            self.assertEqual(returned.returncode, 0, returned.stdout + returned.stderr)
            evidence_path = self.write_json(
                root,
                "direct-evidence.json",
                {
                    "completion_contract_results": [
                        {
                            "criterion": "Tests pass.",
                            "status": "pass",
                            "evidence_refs": ["tests/focused.json"],
                        }
                    ],
                    "checkpoint": {
                        "provider": "none",
                        "status": "not_required",
                        "revision": None,
                        "evidence_ref": None,
                    },
                    "validator_results": [
                        {
                            "validator_id": "focused",
                            "validator_class": "process_validation",
                            "status": "pass",
                            "reason_code": None,
                            "evidence_ref": None,
                            "notes": [],
                        }
                    ],
                    "progress_summary": "Direct evidence passed.",
                    "remaining_work": "None under the contract.",
                },
            )
            verified = self.run_cli(
                "goal",
                "verify",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--generation",
                1,
                "--expected-revision",
                6,
                "--claim-token-file",
                tokens["claim"],
                "--continue-result",
                result_path,
                "--direct-evidence",
                evidence_path,
                "--timestamp",
                TS,
                "--json",
            )
            self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
            decided = self.run_cli(
                "goal",
                "decide",
                "--project-root",
                root,
                "--config",
                config,
                "--goal-id",
                GOAL_ID,
                "--generation",
                1,
                "--expected-revision",
                7,
                "--claim-token-file",
                tokens["claim"],
                "--legal-route-available",
                "--timestamp",
                TS,
                "--json",
            )
            self.assertEqual(decided.returncode, 0, decided.stdout + decided.stderr)
            payload = json.loads(decided.stdout)
            self.assertEqual(payload["phase"], "terminal_complete")
            self.assertEqual(payload["revision"], 8)
            self.assertNotIn("c" * 48, decided.stdout)


if __name__ == "__main__":
    unittest.main()
