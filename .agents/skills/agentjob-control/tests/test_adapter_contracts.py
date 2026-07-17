from __future__ import annotations

import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.adapters.protocols import (
    ADAPTER_CAPABILITY_VERSION,
    AdapterCapabilityReport,
    FeatureCapability,
    ProjectAdapter,
    ValidationResult,
    validate_authority_extensions,
)
from agentjob_runtime.errors import BootstrapRequired, RecordValidationError


class InspectableAdapter:
    adapter_id = "fixture-adapter"
    version = "1.0.0"

    def __init__(self) -> None:
        self.work_calls = 0

    def discover(self, project_root: Path) -> AdapterCapabilityReport:
        return AdapterCapabilityReport(
            self.adapter_id,
            self.version,
            ADAPTER_CAPABILITY_VERSION,
            (
                FeatureCapability("task-records", "1.0.0", True, True),
                FeatureCapability(
                    "native-goal-mirror",
                    "1.0.0",
                    False,
                    False,
                    "unsupported",
                    "fixture.not_implemented",
                ),
            ),
            (".agents/control",),
            ("native-goal-mirror",),
            ("conformance_claims",),
        )

    def load_authoritative_state(self):
        return {}

    def list_roles(self, snapshot):
        return []

    def list_routes(self, snapshot):
        return []

    def validate_decision(self, decision):
        return ValidationResult("pass")

    def validate_job(self, job):
        return ValidationResult("pass")

    def compute_domain_fingerprint(self):
        return {}

    def evaluate_completion(self, completion):
        return ValidationResult("indeterminate")

    def conformance_claims(self):
        return {}


class AdapterContractTests(unittest.TestCase):
    def test_discovery_is_inspectable_and_executes_no_project_work(self) -> None:
        adapter = InspectableAdapter()
        self.assertIsInstance(adapter, ProjectAdapter)
        report = adapter.discover(Path("/project"))
        self.assertEqual(report.status, "ready")
        self.assertFalse(report.execution_performed)
        self.assertEqual(adapter.work_calls, 0)
        self.assertEqual(report.as_dict()["unsupported_features"], ["native-goal-mirror"])

    def test_required_capability_mismatch_is_machine_readable_and_blocking(self) -> None:
        report = AdapterCapabilityReport(
            "fixture",
            "1.0.0",
            ADAPTER_CAPABILITY_VERSION,
            (
                FeatureCapability(
                    "completion-records",
                    "1.0.0",
                    True,
                    False,
                    "unsupported",
                    "fixture.missing_completion",
                ),
            ),
            (".agents/control",),
        )
        with self.assertRaises(BootstrapRequired) as captured:
            report.require(["completion-records"])
        self.assertEqual(
            captured.exception.details["reason_code"], "adapter.capability_mismatch"
        )
        self.assertEqual(
            captured.exception.details["missing_capabilities"], ["completion-records"]
        )

    def test_authority_extensions_require_declared_standard_envelopes(self) -> None:
        validate_authority_extensions(
            {
                "fixture": {
                    "version": "1.0.0",
                    "required": False,
                    "data": {"evidence": "bounded"},
                }
            },
            declared_namespaces=["fixture"],
        )
        with self.assertRaises(RecordValidationError):
            validate_authority_extensions(
                {"undeclared": {"version": "1.0.0", "required": False, "data": {}}},
                declared_namespaces=[],
            )
        with self.assertRaises(RecordValidationError):
            validate_authority_extensions(
                {"fixture": {"required": False, "data": {}}},
                declared_namespaces=["fixture"],
            )


if __name__ == "__main__":
    unittest.main()
