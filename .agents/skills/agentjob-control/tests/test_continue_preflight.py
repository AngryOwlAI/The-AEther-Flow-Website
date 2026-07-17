from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS, valid_config, valid_policy
from agentjob_runtime.continue_flow.preflight import run_preflight
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.indexes import generate_indexes
from agentjob_runtime.records.canonical import render_canonical_json


REPOSITORY = {
    "provider": "test_fake",
    "root": "/project",
    "worktree": "/project",
    "git_common_dir": None,
    "branch": "main",
    "revision": "abc123",
    "status_porcelain": "",
}


class ContinuePreflightTests(unittest.TestCase):
    def files(self, root: Path):
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }

    def configured(self, root: Path) -> Path:
        config = valid_config()
        config["repository"]["provider"] = "test_fake"
        config["policy"]["packs"] = [".agents/control/policies/default.json"]
        config_path = root / "config.json"
        config_path.write_text(render_canonical_json(config), encoding="utf-8")
        policy_path = root / ".agents/control/policies/default.json"
        policy_path.parent.mkdir(parents=True)
        policy_path.write_text(render_canonical_json(valid_policy()), encoding="utf-8")
        generate_indexes(FilesystemControlStore(root, ".agents/control"))
        return config_path

    def test_missing_configuration_returns_bootstrap_without_creating_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            before = self.files(root)
            result = run_preflight(root)
            self.assertEqual(result.status, "bootstrap_required")
            self.assertEqual(result.boundary["boundary"], "bootstrap_required")
            self.assertFalse(result.execution_performed)
            self.assertEqual(before, self.files(root))

    def test_configured_no_action_preflight_is_read_only_and_fingerprinted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = self.configured(root)
            before = self.files(root)
            result = run_preflight(
                root,
                config_path=config,
                repository_snapshot=REPOSITORY,
            )
            self.assertEqual(result.status, "no_action")
            self.assertEqual(result.boundary["reason_code"], "task.none_active")
            self.assertEqual(len(result.fingerprint), 64)
            self.assertFalse(result.execution_performed)
            self.assertEqual(before, self.files(root))

    def test_missing_required_provider_is_bootstrap_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = self.configured(root)
            result = run_preflight(
                root,
                config_path=config,
                repository_snapshot=REPOSITORY,
                provider_versions={"repository:test_fake": "2.0.0"},
            )
            self.assertEqual(result.status, "bootstrap_required")
            self.assertIn(
                "sys4ai.repository-provider.v1",
                result.capabilities["missing_capabilities"],
            )

    def test_missing_policy_is_reported_as_control_repair_not_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = valid_config()
            config["repository"]["provider"] = "test_fake"
            config["policy"]["packs"] = ["missing-policy.json"]
            config_path = root / "config.json"
            config_path.write_text(render_canonical_json(config), encoding="utf-8")
            result = run_preflight(
                root,
                config_path=config_path,
                repository_snapshot=REPOSITORY,
            )
            self.assertEqual(result.status, "control_repair_required")
            self.assertIn("policy_missing:missing-policy.json", result.conflicts)
            self.assertFalse(result.execution_performed)


if __name__ == "__main__":
    unittest.main()
