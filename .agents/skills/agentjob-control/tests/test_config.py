import tempfile
import unittest
from pathlib import Path

from _support import cloned, valid_config
from agentjob_runtime.config import load_config
from agentjob_runtime.errors import BootstrapRequired, ConfigurationError, SecurityError
from agentjob_runtime.records.canonical import render_canonical_json


class ConfigurationTests(unittest.TestCase):
    def write_config(self, root: Path, value) -> Path:
        path = root / "config.json"
        path.write_text(render_canonical_json(value), encoding="utf-8")
        return path

    def test_missing_configuration_returns_bootstrap_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(BootstrapRequired) as raised:
                load_config(directory)
            self.assertFalse(raised.exception.details["execution_performed"])

    def test_valid_configuration_discovers_required_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self.write_config(root, valid_config())
            loaded = load_config(root, config_path=path)
            self.assertEqual(loaded.capabilities.status, "ready")
            self.assertEqual(loaded.control_root, (root / ".agents/control").resolve())
            self.assertEqual(
                loaded.local_state_root, (root / ".local/sys4ai/continuation").resolve()
            )

    def test_unknown_or_unsupported_provider_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = valid_config()
            config["control"]["adapter"] = "unknown-adapter"
            path = self.write_config(root, config)
            loaded = load_config(root, config_path=path)
            self.assertEqual(loaded.capabilities.status, "bootstrap_required")
            self.assertIn("sys4ai.control-records.v1", loaded.capabilities.missing_capabilities)

            config["control"]["adapter"] = "filesystem"
            path = self.write_config(root, config)
            loaded = load_config(
                root,
                config_path=path,
                provider_versions={"control:filesystem": "2.0.0"},
            )
            finding = next(
                item for item in loaded.capabilities.capabilities if item.capability_id == "sys4ai.control-records.v1"
            )
            self.assertEqual(finding.reason_code, "capability.unsupported_version")

    def test_core_invariants_cannot_be_weakened(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = valid_config()
            config["control"]["one_agentjob_per_continue"] = False
            with self.assertRaises(ConfigurationError):
                load_config(root, config_path=self.write_config(root, config))

    def test_environment_substitution_is_allowlisted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = valid_config()
            config["project"]["id"] = "${PROJECT_ID}"
            config["security"]["allow_environment_fields"] = ["project.id"]
            loaded = load_config(
                root,
                config_path=self.write_config(root, config),
                environment={"PROJECT_ID": "fixture-project"},
            )
            self.assertEqual(loaded.data["project"]["id"], "fixture-project")

            denied = cloned(config)
            denied["security"]["allow_environment_fields"] = []
            with self.assertRaises(ConfigurationError):
                load_config(
                    root,
                    config_path=self.write_config(root, denied),
                    environment={"PROJECT_ID": "fixture-project"},
                )

    def test_mutable_state_cannot_live_in_installed_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = valid_config()
            config["goal_relay"]["local_root"] = "skills/agentjob-control/runtime"
            with self.assertRaises(SecurityError):
                load_config(root, config_path=self.write_config(root, config))


if __name__ == "__main__":
    unittest.main()
