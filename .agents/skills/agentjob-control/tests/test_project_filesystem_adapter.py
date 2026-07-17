from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import (
    RUNTIME_SCRIPTS,
    valid_completion,
    valid_config,
    valid_decision,
    valid_job,
    valid_policy,
)
from agentjob_runtime.adapters.project_filesystem import FilesystemProjectAdapter
from agentjob_runtime.records.canonical import render_canonical_json


class ProjectFilesystemAdapterTests(unittest.TestCase):
    def configured(self, root: Path) -> Path:
        config = valid_config()
        config["repository"]["provider"] = "filesystem_only"
        config["policy"]["packs"] = [".agents/control/policies/default.json"]
        config_path = root / "config.json"
        config_path.write_text(render_canonical_json(config), encoding="utf-8")
        policy = root / ".agents/control/policies/default.json"
        policy.parent.mkdir(parents=True)
        policy.write_text(render_canonical_json(valid_policy()), encoding="utf-8")
        role = root / ".agents/control/roles/software-engineer.json"
        role.parent.mkdir(parents=True)
        role.write_text(
            render_canonical_json(
                {
                    "role_id": "software-engineer",
                    "version": "1.0.0",
                    "responsibilities": ["Implement one bounded AgentJob."],
                    "may_not": ["Expand activated authority."],
                }
            ),
            encoding="utf-8",
        )
        return config_path

    def test_neutral_project_discovers_and_loads_without_custom_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = self.configured(root)
            adapter = FilesystemProjectAdapter(root, config_path=config)
            report = adapter.discover(root)
            self.assertEqual(report.status, "ready")
            self.assertFalse(report.execution_performed)
            snapshot = adapter.load_authoritative_state()
            self.assertEqual(snapshot["domain_truth"], "not_evaluated")
            self.assertEqual(snapshot["current"]["task"], None)
            self.assertEqual(adapter.list_roles(snapshot)[0]["role_id"], "software-engineer")
            self.assertEqual(adapter.list_routes(snapshot), ())

    def test_routes_are_candidates_and_never_self_authorizing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = self.configured(root)
            adapter = FilesystemProjectAdapter(root, config_path=config)
            snapshot = dict(adapter.load_authoritative_state())
            snapshot["current"] = {
                **snapshot["current"],
                "task": {"task_id": "TASK-1"},
            }
            route = adapter.list_routes(snapshot)[0]
            self.assertEqual(route["status"], "candidate")
            self.assertEqual(route["selection_authority"], "system_director_required")

    def test_schema_validation_and_completion_keep_domain_truth_indeterminate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = self.configured(root)
            adapter = FilesystemProjectAdapter(root, config_path=config)
            self.assertEqual(adapter.validate_decision(valid_decision()).status, "pass")
            self.assertEqual(adapter.validate_job(valid_job()).status, "pass")
            completion = adapter.evaluate_completion(valid_completion())
            self.assertEqual(completion.status, "pass")
            self.assertEqual(completion.evidence["domain_truth"], "indeterminate")
            self.assertFalse(completion.evidence["scientific_promotion_authority"])

    def test_domain_fingerprint_uses_canonical_hashes_not_local_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = self.configured(root)
            adapter = FilesystemProjectAdapter(root, config_path=config)
            before = adapter.compute_domain_fingerprint()
            cache = root / ".local/cache/result.json"
            cache.parent.mkdir(parents=True)
            cache.write_text('{"stale": true}\n', encoding="utf-8")
            after = adapter.compute_domain_fingerprint()
            self.assertEqual(before, after)
            self.assertEqual(after["domain_truth"], "not_evaluated")


if __name__ == "__main__":
    unittest.main()
