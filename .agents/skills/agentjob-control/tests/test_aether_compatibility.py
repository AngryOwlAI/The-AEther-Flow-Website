from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from _support import PACKAGE_ROOT, RUNTIME_SCRIPTS
from agentjob_runtime.adapters.conformance import run_conformance
from agentjob_runtime.compat.aether_adapter import (
    AetherProjectAdapter,
    CORE_REGISTRIES,
    SOURCE_BINDING_FILES,
)
from agentjob_runtime.compat.aether_shadow import run_shadow_comparison
from agentjob_runtime.records.canonical import load_structured
from agentjob_runtime.validation.schema import validate_instance


def write(path: Path, text: str = "fixture\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_aether_fixture(root: Path, *, sidecar_only: bool = False) -> AetherProjectAdapter:
    for relative in SOURCE_BINDING_FILES:
        if relative == "research_control/program_state.yaml":
            continue
        write(root / relative)
    for relative in ("research_control/tasks", "research_control/handoffs", ".agents/roles"):
        (root / relative).mkdir(parents=True, exist_ok=True)
    write(
        root / "research_control/program_state.yaml",
        'mode: "director_led_research_control"\n'
        'active_task_id: "RT-20260717-001"\n'
        'latest_handoff_id: "handoff-0001"\n'
        'current_status: "fixture_ready"\n'
        'next_recommended_action: "Run one bounded fixture packet."\n',
    )
    write(
        root / "research_control/tasks/RT-20260717-001/00_TASK.yaml",
        'task_id: "RT-20260717-001"\nstatus: "active"\nobjective: "Run one fixture."\n'
        'current_decision_id: "DDR-20260717-001"\ncurrent_job_id: "AJ-RT-20260717-001-001"\n'
        'requires_human_gate: false\nnext_recommended_action: "Run one bounded fixture packet."\n',
    )
    write(
        root / "research_control/tasks/RT-20260717-001/DDR-20260717-001.md",
        '---\ndecision_id: "DDR-20260717-001"\ntask_id: "RT-20260717-001"\n'
        'director_version: "director-of-research@0.3.0"\ndecision_type: "task_overlay"\n'
        'selected_role_id: "validator-engineer"\nselected_role_version: "0.2.0"\n'
        'agent_job_id: "AJ-RT-20260717-001-001"\nstatus: "active"\n'
        'supersedes_decision_id: ""\nrequires_human_gate: false\n'
        'role_fit_candidates:\n  - "validator-engineer@0.2.0|selected|fixture"\n---\n\n# Fixture\n',
    )
    job_path = "research_control/tasks/RT-20260717-001/jobs/AJ-RT-20260717-001-001.yaml"
    write(
        root / job_path,
        'job_id: "AJ-RT-20260717-001-001"\ntask_id: "RT-20260717-001"\n'
        'decision_id: "DDR-20260717-001"\nrole_id: "validator-engineer"\nrole_version: "0.2.0"\n'
        'status: "active"\nrequires_human_gate: false\nallowed_read_paths:\n  - "src/a.py"\n'
        'allowed_write_paths:\n  - "src/a.py"\nallowed_generated_paths:\n  - "output/a.json"\n'
        'forbidden_paths:\n  - "secrets/**"\nallowed_source_classes:\n  - "controlled"\n'
        'forbidden_source_classes:\n  - "secret"\napproved_commands:\n  - "python3 -m unittest"\n'
        'required_validators:\n  - "fixture"\nexpected_outputs:\n  - "src/a.py"\n'
        'claim_boundary: "CB-FIXTURE-001"\n',
    )
    role_path = "research_control/tasks/RT-20260717-001/roles/validator-engineer@0.2.0--RT-20260717-001.yaml"
    write(
        root / role_path,
        'execution_role_ref: "validator-engineer@0.2.0--RT-20260717-001"\n'
        'role_execution_kind: "registered_role"\ntask_id: "RT-20260717-001"\n'
        'agent_job_id: "AJ-RT-20260717-001-001"\nauthority_delta_summary: "none"\n'
        'allowed_write_paths:\n  - "src/a.py"\nrequires_human_gate: false\n'
        'expires_after: "AJ-RT-20260717-001-001"\n',
    )
    completion_path = "research_control/tasks/RT-20260717-001/jobs/completions/AJC-AJ-RT-20260717-001-001.yaml"
    write(
        root / completion_path,
        'completion_id: "AJC-AJ-RT-20260717-001-001"\njob_id: "AJ-RT-20260717-001-001"\n'
        'task_id: "RT-20260717-001"\ndecision_id: "DDR-20260717-001"\n'
        'status: "active"\nvalidation_status: "pending"\n',
    )
    write(
        root / "research_control/handoffs/handoff-0001.yaml",
        'handoff_id: "handoff-0001"\ntask_id: "RT-20260717-001"\n'
        'job_id: "AJ-RT-20260717-001-001"\nstatus: "completed"\n'
        'next_action: "Run one bounded fixture packet."\n',
    )
    write(root / "research_control/handoffs/handoff-0001.md", "# handoff fixture\n")

    write_csv(
        root / "registries/RESEARCH_TASK_REGISTRY.csv",
        ["task_id", "task_path", "current_decision_id", "current_job_id", "requires_human_gate", "status"],
        [{
            "task_id": "RT-20260717-001",
            "task_path": "research_control/tasks/RT-20260717-001/00_TASK.yaml",
            "current_decision_id": "DDR-20260717-001",
            "current_job_id": "AJ-RT-20260717-001-001",
            "requires_human_gate": "false",
            "status": "active",
        }],
    )
    write_csv(
        root / "registries/DIRECTOR_DECISION_REGISTRY.csv",
        ["decision_id", "task_id", "decision_path", "requires_human_gate", "status"],
        [{
            "decision_id": "DDR-20260717-001",
            "task_id": "RT-20260717-001",
            "decision_path": "research_control/tasks/RT-20260717-001/DDR-20260717-001.md",
            "requires_human_gate": "false",
            "status": "active",
        }],
    )
    jobs = [{
        "job_id": "AJ-RT-20260717-999-001" if sidecar_only else "AJ-RT-20260717-001-001",
        "task_id": "RT-20260717-999" if sidecar_only else "RT-20260717-001",
        "decision_id": "DDR-20260717-999" if sidecar_only else "DDR-20260717-001",
        "role_id": "validator-engineer",
        "role_version": "0.2.0",
        "job_path": job_path,
        "requires_human_gate": "false",
        "status": "active",
    }]
    write_csv(
        root / "registries/AGENT_JOB_REGISTRY.csv",
        ["job_id", "task_id", "decision_id", "role_id", "role_version", "job_path", "requires_human_gate", "status"],
        jobs,
    )
    write_csv(
        root / "registries/ROLE_EXECUTION_REGISTRY.csv",
        ["execution_role_ref", "task_id", "agent_job_id", "record_path", "status"],
        [{
            "execution_role_ref": "validator-engineer@0.2.0--RT-20260717-001",
            "task_id": "RT-20260717-001",
            "agent_job_id": "AJ-RT-20260717-001-001",
            "record_path": role_path,
            "status": "active",
        }],
    )
    write_csv(
        root / "registries/AGENT_ROLE_REGISTRY.csv",
        ["role_id", "version", "role_kind", "authority_level", "requires_human_gate", "role_contract_path", "status"],
        [{
            "role_id": "validator-engineer",
            "version": "0.2.0",
            "role_kind": "project_system_validation",
            "authority_level": "project_control",
            "requires_human_gate": "false",
            "role_contract_path": ".agents/roles/research_ops/validator-engineer.v0.2.0.md",
            "status": "active",
        }],
    )
    write_csv(root / "registries/CLAIM_BOUNDARY_REGISTRY.csv", ["claim_boundary_id", "status"], [])
    for name in CORE_REGISTRIES:
        path = root / "registries" / name
        if not path.exists():
            write_csv(path, ["id", "status"], [])
    return AetherProjectAdapter(root)


class AetherCompatibilityTests(unittest.TestCase):
    def test_adapter_manifest_policy_and_extensions_validate(self) -> None:
        pairs = [
            ("adapters/aether/aether-adapter.yaml", "project-adapter.schema.json"),
            ("policy-packs/aether-research.yaml", "policy-pack.schema.json"),
        ]
        for relative, schema in pairs:
            with self.subTest(relative=relative):
                value = load_structured(PACKAGE_ROOT / relative)
                self.assertEqual(
                    validate_instance(value, PACKAGE_ROOT / "schemas" / schema), []
                )
        policy = load_structured(PACKAGE_ROOT / "policy-packs/aether-research.yaml")
        gated = {
            row["action"] for row in policy["human_gate_rules"] if row["required"]
        }
        self.assertEqual(set(policy["protected_actions"]), gated)
        self.assertFalse(policy["claim_rules"]["scientific_promotion_authority"])

    def test_adapter_maps_matching_job_and_reports_conformance_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            adapter = build_aether_fixture(root)
            before = adapter.compute_domain_fingerprint()
            report = adapter.discover(root)
            self.assertEqual(report.status, "ready")
            self.assertFalse(report.execution_performed)
            state = adapter.load_authoritative_state()
            self.assertEqual(state["resolver"]["boundary"], "existing_agent_job_ready")
            self.assertEqual(state["resolver"]["active_task_id"], "RT-20260717-001")
            self.assertEqual(state["sidecar_jobs"], [])
            self.assertEqual(run_conformance(adapter).status, "conformant")
            self.assertEqual(before, adapter.compute_domain_fingerprint())

    def test_unrelated_active_sidecar_blocks_without_replacing_program_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            adapter = build_aether_fixture(Path(directory).resolve(), sidecar_only=True)
            resolver = adapter.resolve_boundary()
            self.assertEqual(resolver["boundary"], "blocked")
            self.assertEqual(resolver["active_task_id"], "RT-20260717-001")
            state = adapter.load_authoritative_state()
            self.assertEqual(state["sidecar_jobs"][0]["task_id"], "RT-20260717-999")

    def test_shadow_comparison_covers_route_authority_and_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            adapter = build_aether_fixture(root)
            legacy = adapter.resolve_boundary()
            legacy["checkpoint_required_after_execution"] = legacy["checkpoint_provider"][
                "required_after_execution"
            ]
            report = run_shadow_comparison(root, legacy_output=legacy)
            self.assertEqual(report["status"], "pass")
            self.assertTrue(report["source_unchanged"])
            self.assertEqual(report["defect_count"], 0)
            categories = {item["category"] for item in report["comparisons"]}
            self.assertTrue(
                {"routing", "task", "decision", "job", "roles", "paths", "validators", "gates", "checkpoint"}
                <= categories
            )

    def test_shims_are_thin_declarative_and_not_activated(self) -> None:
        mapping = load_structured(PACKAGE_ROOT / "compat/aether/shim-map.yaml")
        self.assertEqual(mapping["status"], "template_not_activated")
        self.assertEqual(len(mapping["shims"]), 3)
        for item in mapping["shims"]:
            text = (PACKAGE_ROOT.parent.parent / item["template_path"]).read_text(
                encoding="utf-8"
            )
            self.assertLess(len(text.splitlines()), 50)
            self.assertIn(f"name: {item['legacy_skill_id']}", text)
            self.assertIn(item["canonical_skill_id"], text)
            self.assertNotIn("## Procedure", text)


if __name__ == "__main__":
    unittest.main()
