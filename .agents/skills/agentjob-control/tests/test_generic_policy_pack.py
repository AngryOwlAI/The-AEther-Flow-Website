from __future__ import annotations

import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.records.canonical import load_structured
from agentjob_runtime.validation.schema import validate_instance


PACKAGE = Path(__file__).resolve().parents[1]
POLICY = PACKAGE / "policy-packs" / "generic-software.yaml"


class GenericPolicyPackTests(unittest.TestCase):
    def test_pack_validates_and_contains_portable_default_roles(self) -> None:
        policy = load_structured(POLICY)
        issues = validate_instance(policy, PACKAGE / "schemas" / "policy-pack.schema.json")
        self.assertEqual(issues, [])
        self.assertEqual(
            set(policy["roles"]),
            {
                "system-analyst",
                "system-engineer",
                "software-engineer",
                "validator-engineer",
                "system-architect",
            },
        )
        extension = policy["extensions"]["sys4ai.generic-software"]["data"]
        self.assertTrue(extension["suitable_for_software"])
        self.assertTrue(extension["suitable_for_documentation"])

    def test_every_protected_action_requires_a_human_gate(self) -> None:
        policy = load_structured(POLICY)
        gated = {
            item["action"]
            for item in policy["human_gate_rules"]
            if item["required"] is True
        }
        self.assertEqual(set(policy["protected_actions"]), gated)
        self.assertIn("secret-access", gated)
        self.assertIn("irreversible-external-action", gated)

    def test_claim_and_route_defaults_are_conservative_and_not_scientific_authority(self) -> None:
        policy = load_structured(POLICY)
        rules = policy["claim_rules"]
        self.assertTrue(rules["process_validation_does_not_imply_domain_truth"])
        self.assertFalse(rules["scientific_promotion_authority"])
        self.assertEqual(rules["default_route_policy"], "conservative")
        self.assertEqual(
            rules["conservative_route_candidates"],
            ["existing-bounded-job", "director-review", "control-repair"],
        )
        self.assertFalse(
            policy["extensions"]["sys4ai.generic-software"]["data"][
                "automatic_release_authority"
            ]
        )


if __name__ == "__main__":
    unittest.main()
