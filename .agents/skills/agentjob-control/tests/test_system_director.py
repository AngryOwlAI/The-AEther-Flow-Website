from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from _support import (
    RUNTIME_SCRIPTS,
    valid_job,
    valid_policy,
    valid_role,
    valid_task,
)
from agentjob_runtime.continue_flow.director import DirectorRoute, resolve_director_packet
from agentjob_runtime.continue_flow.preflight import run_preflight
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.control.indexes import generate_indexes
from test_continue_preflight import ContinuePreflightTests, REPOSITORY


def route(route_id: str, priority: int = 10, **overrides) -> DirectorRoute:
    job = valid_job()
    role = valid_role()
    job_spec = {
        "objective": job["objective"],
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
        "source_refs": ["src/example.py"],
        "extensions": {},
    }
    role_spec = {
        "binding_type": role["binding_type"],
        "responsibilities": copy.deepcopy(role["responsibilities"]),
        "may_not": copy.deepcopy(role["may_not"]),
        "source_role_ref": role["source_role_ref"],
        "task_overlay": role["task_overlay"],
        "authority_delta": role["authority_delta"],
        "provisional_role": role["provisional_role"],
        "extensions": {},
    }
    values = {
        "route_id": route_id,
        "role_id": "software-engineer",
        "role_version": "1.0.0",
        "priority": priority,
        "rationale": f"{route_id} is a bounded legal route.",
        "job_spec": job_spec,
        "role_spec": role_spec,
    }
    values.update(overrides)
    return DirectorRoute(**values)


class SystemDirectorTests(unittest.TestCase):
    def prepared(self, directory: str):
        root = Path(directory).resolve()
        config = ContinuePreflightTests().configured(root)
        store = FilesystemControlStore(root, ".agents/control")
        task = valid_task()
        task["current_decision_id"] = None
        task["current_job_id"] = None
        task["next_recommended_action"] = "Select one legal route."
        store.create_task(task)
        generate_indexes(store)
        preflight = run_preflight(
            root,
            config_path=config,
            task_id=task["task_id"],
            repository_snapshot=REPOSITORY,
        )
        self.assertEqual(preflight.status, "director_decision_required")
        return root, config, store, task, preflight

    def test_multiple_candidates_activate_exactly_one_deliberative_packet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, config, store, task, preflight = self.prepared(directory)
            outcome = resolve_director_packet(
                preflight,
                store=store,
                routes=[route("broader", 20), route("narrower", 10)],
                expected_revision=1,
                policies=[valid_policy()],
                timestamp="2026-07-17T15:02:00Z",
            )
            self.assertEqual(outcome.status, "activated")
            self.assertEqual(outcome.decision["decision_mode"], "deliberative")
            self.assertEqual(outcome.decision["selected"]["route_id"], "narrower")
            jobs = [record for kind, _, record in store.iter_records() if kind == "agent_job"]
            self.assertEqual(len(jobs), 1)
            self.assertEqual(outcome.activation["task_revision"], 2)

            current = run_preflight(
                root,
                config_path=config,
                task_id=task["task_id"],
                repository_snapshot=REPOSITORY,
            )
            reused = resolve_director_packet(current, store=store)
            self.assertEqual(reused.status, "reused")
            self.assertEqual(reused.job["job_id"], outcome.job["job_id"])

    def test_single_policy_route_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, _, store, _, preflight = self.prepared(directory)
            outcome = resolve_director_packet(
                preflight,
                store=store,
                routes=[route("forced", forced_by_rule_id="policy.only-legal-route")],
                expected_revision=1,
                policies=[valid_policy()],
                timestamp="2026-07-17T15:02:00Z",
            )
            self.assertEqual(outcome.decision["decision_mode"], "deterministic")
            self.assertEqual(outcome.decision["rule_id"], "policy.only-legal-route")

    def test_human_gate_or_authority_expansion_stops_without_creating_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, _, store, _, preflight = self.prepared(directory)
            gated = resolve_director_packet(
                preflight,
                store=store,
                routes=[route("publish", requires_human_gate=True)],
                expected_revision=1,
            )
            self.assertEqual(gated.boundary, "human_gate_required")
            self.assertFalse(any(kind == "agent_job" for kind, _, _ in store.iter_records()))
        with tempfile.TemporaryDirectory() as directory:
            _, _, store, _, preflight = self.prepared(directory)
            blocked = resolve_director_packet(
                preflight,
                store=store,
                routes=[route("expand", authority_expansion=True)],
                expected_revision=1,
            )
            self.assertEqual(blocked.boundary, "blocked")
            self.assertFalse(any(kind == "agent_job" for kind, _, _ in store.iter_records()))

    def test_domain_truth_route_requires_declared_domain_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, _, store, _, preflight = self.prepared(directory)
            outcome = resolve_director_packet(
                preflight,
                store=store,
                routes=[route("research-claim", domain_truth_decision=True)],
                expected_revision=1,
            )
            self.assertEqual(outcome.reason_code, "director.no_legal_route")
            self.assertIn("domain truth", outcome.rejected_routes[0])


if __name__ == "__main__":
    unittest.main()
