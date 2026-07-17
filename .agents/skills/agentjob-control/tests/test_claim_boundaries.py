from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, valid_job, valid_role
from agentjob_runtime.continue_flow.director import DirectorRoute, _route_legality
from agentjob_runtime.execution.compiler import compile_authority
from agentjob_runtime.execution.executor import ExecutionEvidence
from agentjob_runtime.execution.validation import validate_execution
from agentjob_runtime.records.canonical import load_structured
from agentjob_runtime.validation.schema import validate_instance


CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}
PACKAGE = Path(__file__).resolve().parents[1]


class ClaimBoundaryTests(unittest.TestCase):
    def authority(self, directory: str, *, allowed, forbidden, domain_validator=False):
        root = Path(directory).resolve()
        (root / "src").mkdir()
        (root / "tests").mkdir()
        (root / "src/example.py").write_text("value = 1\n", encoding="utf-8")
        job = valid_job()
        job["commands"]["approved"] = []
        job["expected_outputs"] = [
            {"path": "src/example.py", "kind": "generated_derivative"}
        ]
        job["checkpoint"] = {"provider": "none", "required": False, "auto_commit": False}
        job["claim_boundary"] = {"allowed": list(allowed), "forbidden": list(forbidden)}
        job["validators"] = {
            "required": [
                {
                    "validator_id": "claim-boundary-linter",
                    "validator_class": "claim_validation",
                    "mode": "required",
                }
            ],
            "contextual": [],
        }
        if domain_validator:
            job["validators"]["required"].append(
                {
                    "validator_id": "domain-review",
                    "validator_class": "domain_validation",
                    "mode": "required",
                }
            )
        role = valid_role()
        authority = compile_authority(
            project_root=root,
            job=job,
            execution_role=role,
            activated_record_ids={job["job_id"], role["execution_role_id"]},
            runtime_capabilities=CAPABILITIES,
        )
        evidence = ExecutionEvidence(
            "executed",
            authority.task_id,
            authority.decision_id,
            authority.job_id,
            authority.execution_role_id,
            HASH_A,
            HASH_A,
            {"src/example.py": HASH_A},
            {"src/example.py": HASH_A},
            (),
            (),
            (),
            None,
        )
        return authority, evidence

    def test_allowed_language_is_exact_and_forbidden_or_paraphrased_claims_fail(self) -> None:
        allowed = "The bounded literature scan completed."
        forbidden = "The research hypothesis is scientifically established."
        with tempfile.TemporaryDirectory() as directory:
            authority, evidence = self.authority(
                directory, allowed=[allowed], forbidden=[forbidden]
            )
            accepted = validate_execution(
                authority=authority, evidence=evidence, proposed_claims=[allowed]
            )
            self.assertEqual(accepted.status, "passed")
            for claim in (forbidden, "The bounded literature scan is complete."):
                with self.subTest(claim=claim):
                    report = validate_execution(
                        authority=authority, evidence=evidence, proposed_claims=[claim]
                    )
                    self.assertEqual(report.status, "validation_failed")
                    result = next(
                        item
                        for item in report.validator_results
                        if item["validator_id"] == "claim-boundary-linter"
                    )
                    self.assertEqual(result["status"], "fail")

    def test_generated_derivative_cannot_promote_itself_to_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            authority, evidence = self.authority(
                directory,
                allowed=["The generated comparison report exists."],
                forbidden=["The generated comparison report is canonical authority."],
            )
            report = validate_execution(
                authority=authority,
                evidence=evidence,
                proposed_claims=["The generated comparison report is canonical authority."],
            )
            self.assertEqual(report.status, "validation_failed")

    def test_process_pass_does_not_promote_domain_truth(self) -> None:
        process_claim = "The declared process checks passed."
        domain_claim = "The scientific model is true."
        with tempfile.TemporaryDirectory() as directory:
            authority, evidence = self.authority(
                directory,
                allowed=[process_claim],
                forbidden=[domain_claim],
                domain_validator=True,
            )
            report = validate_execution(
                authority=authority,
                evidence=evidence,
                validator_adapters={"domain-review": lambda *_: {"status": "pass"}},
                proposed_claims=[domain_claim],
            )
            self.assertEqual(report.status, "validation_failed")
            self.assertFalse(report.domain_indeterminate)

    def test_neutral_research_example_retains_domain_indeterminacy(self) -> None:
        process_claim = "The bounded literature scan completed."
        with tempfile.TemporaryDirectory() as directory:
            authority, evidence = self.authority(
                directory,
                allowed=[process_claim],
                forbidden=["The hypothesis is established."],
                domain_validator=True,
            )
            report = validate_execution(
                authority=authority,
                evidence=evidence,
                validator_adapters={
                    "domain-review": lambda *_: {
                        "status": "indeterminate",
                        "reason_code": "research.insufficient_evidence",
                        "notes": ["The scan is process evidence, not domain truth."],
                    }
                },
                proposed_claims=[process_claim],
            )
            self.assertEqual(report.status, "domain_indeterminate")
            self.assertTrue(report.domain_indeterminate)

    def test_missing_human_or_domain_authority_blocks_director_route(self) -> None:
        base = valid_job()
        role = valid_role()
        route = DirectorRoute(
            "protected",
            "software-engineer",
            "1.0.0",
            1,
            "Protected route.",
            base,
            role,
            requires_human_gate=True,
        )
        allowed, reason = _route_legality(route)
        self.assertFalse(allowed)
        self.assertIn("human gate", reason)
        domain_route = copy.copy(route)
        domain_route = DirectorRoute(
            **{
                **domain_route.__dict__,
                "requires_human_gate": False,
                "domain_truth_decision": True,
                "domain_authority_ref": None,
            }
        )
        allowed, reason = _route_legality(domain_route)
        self.assertFalse(allowed)
        self.assertIn("domain authority", reason)

    def test_policy_extension_ownership_and_aether_physics_rules_are_separate(self) -> None:
        generic = load_structured(PACKAGE / "policy-packs/generic-software.yaml")
        aether = load_structured(PACKAGE / "policy-packs/aether-research.yaml")
        policy_schema = PACKAGE / "schemas/policy-pack.schema.json"
        self.assertFalse(validate_instance(generic, policy_schema))
        self.assertFalse(validate_instance(aether, policy_schema))
        self.assertFalse(generic["claim_rules"]["scientific_promotion_authority"])
        self.assertNotIn("aether.physics-completion", generic["extension_schemas"])
        declaration = aether["extension_schemas"]["aether.physics-completion"]
        self.assertEqual(declaration["owner"], "aether-flow")

        schema = PACKAGE / declaration["schema_ref"]
        neutral = {
            "status": "process-complete-domain-indeterminate",
            "scientific_claims_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "forbidden_conclusion_summary": ["No completed derivation is claimed."],
            "source_schema_ref": ".agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md",
        }
        self.assertFalse(validate_instance(neutral, schema))
        promoted = {**neutral, "physics_promotion_authorized": True}
        self.assertTrue(validate_instance(promoted, schema))
        promoted["promotion_authority_path"] = ".agents/approvals/GATE-001.yaml"
        self.assertFalse(validate_instance(promoted, schema))


if __name__ == "__main__":
    unittest.main()
