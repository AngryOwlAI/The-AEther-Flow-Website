from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS, valid_config, valid_policy
from agentjob_runtime.adapters.conformance import (
    REQUIRED_CONFORMANCE_FEATURES,
    run_conformance,
)
from agentjob_runtime.adapters.project_filesystem import FilesystemProjectAdapter
from agentjob_runtime.records.canonical import render_canonical_json


class ClaimAdapter:
    adapter_id = "existing-fixture"
    version = "1.0.0"

    def __init__(self, claims):
        self.claims = claims

    def conformance_claims(self):
        return self.claims


def passing(mode="native"):
    return {"mode": mode, "status": "pass", "evidence": ["fixture-proof"]}


class ExistingControlConformanceTests(unittest.TestCase):
    def test_portable_filesystem_adapter_reports_complete_native_conformance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            config = valid_config()
            config["repository"]["provider"] = "filesystem_only"
            config["policy"]["packs"] = [".agents/control/policies/default.json"]
            config_path = root / "config.json"
            config_path.write_text(render_canonical_json(config), encoding="utf-8")
            policy = root / ".agents/control/policies/default.json"
            policy.parent.mkdir(parents=True)
            policy.write_text(render_canonical_json(valid_policy()), encoding="utf-8")
            report = run_conformance(
                FilesystemProjectAdapter(root, config_path=config_path)
            )
            self.assertEqual(report.status, "conformant")
            self.assertEqual(set(report.native_features), set(REQUIRED_CONFORMANCE_FEATURES))
            self.assertFalse(report.execution_performed)

    def test_absent_core_authority_record_is_a_blocking_gap(self) -> None:
        claims = {feature: passing() for feature in REQUIRED_CONFORMANCE_FEATURES}
        claims.pop("completion")
        report = run_conformance(ClaimAdapter(claims))
        self.assertEqual(report.status, "blocking_gaps")
        self.assertIn("completion", report.blocking_gaps)
        check = next(item for item in report.checks if item.feature_id == "completion")
        self.assertEqual(check.mode, "unsupported")
        self.assertEqual(check.reason_code, "conformance.mapping_absent")

    def test_report_distinguishes_native_emulated_and_unsupported(self) -> None:
        claims = {feature: passing() for feature in REQUIRED_CONFORMANCE_FEATURES}
        claims["handoff"] = passing("emulated")
        claims["recovery_evidence"] = {
            "mode": "unsupported",
            "status": "fail",
            "evidence": [],
            "reason_code": "fixture.no_recovery_record",
        }
        report = run_conformance(ClaimAdapter(claims))
        self.assertIn("handoff", report.emulated_features)
        self.assertIn("recovery_evidence", report.unsupported_features)
        self.assertIn("recovery_evidence", report.blocking_gaps)

    def test_cardinality_claim_and_path_boundaries_require_passing_evidence(self) -> None:
        for feature in ("one_job_cardinality", "claim_boundary", "path_boundary"):
            with self.subTest(feature=feature):
                claims = {item: passing() for item in REQUIRED_CONFORMANCE_FEATURES}
                claims[feature] = {"mode": "emulated", "status": "fail", "evidence": []}
                report = run_conformance(ClaimAdapter(claims))
                self.assertEqual(report.status, "blocking_gaps")
                self.assertIn(feature, report.blocking_gaps)


if __name__ == "__main__":
    unittest.main()
