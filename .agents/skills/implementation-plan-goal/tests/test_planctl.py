from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "planctl.py"
PLAN_FIXTURE = SKILL_ROOT / "templates" / "canonical-plan-template.json"
STATE_SCHEMA = SKILL_ROOT / "schemas" / "implementation-plan-state.schema.json"
RECEIPT_SCHEMA = SKILL_ROOT / "schemas" / "plan-task-receipt.schema.json"
CONTRACT_SCHEMAS = {
    "normalization_report": SKILL_ROOT / "schemas" / "normalization-report.schema.json",
    "plan_amendment": SKILL_ROOT / "schemas" / "plan-amendment.schema.json",
    "task_supersession": SKILL_ROOT / "schemas" / "plan-task-supersession.schema.json",
    "provider_intent": SKILL_ROOT / "schemas" / "provider-intent.schema.json",
    "selection_proof": SKILL_ROOT / "schemas" / "selection-proof.schema.json",
}
ACTIVE_STATE_FIXTURE = (
    SKILL_ROOT / "templates" / "implementation-plan-state-template.json"
)
RECEIPT_FIXTURE = SKILL_ROOT / "templates" / "plan-task-receipt-template.json"
COMPLETED_STATE_FIXTURE = (
    SKILL_ROOT / "examples" / "implementation-plan-state.completed.example.json"
)
RECEIPT_OUTCOME_FIXTURES = (
    SKILL_ROOT / "examples" / "plan-task-receipt-outcomes.example.json"
)
ENVELOPE_FIXTURE = SKILL_ROOT / "examples" / "plan-task-envelope.example.json"
CONTROL_CONTRACT_FIXTURES = (
    SKILL_ROOT / "examples" / "plan-control-contracts.example.json"
)
NORMALIZATION_SOURCE = (
    SKILL_ROOT / "examples" / "normalization-partial-source.example.json"
)
NORMALIZATION_GOLDEN = (
    SKILL_ROOT / "examples" / "planctl-normalization-golden.example.json"
)


def load_planctl():
    spec = importlib.util.spec_from_file_location("planctl_seed", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load planctl")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PlanCtlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.planctl = load_planctl()
        cls.plan = json.loads(PLAN_FIXTURE.read_text(encoding="utf-8"))
        cls.active_state = json.loads(
            ACTIVE_STATE_FIXTURE.read_text(encoding="utf-8")
        )
        cls.completed_state = json.loads(
            COMPLETED_STATE_FIXTURE.read_text(encoding="utf-8")
        )
        cls.receipt = json.loads(RECEIPT_FIXTURE.read_text(encoding="utf-8"))
        cls.receipt_outcomes = json.loads(
            RECEIPT_OUTCOME_FIXTURES.read_text(encoding="utf-8")
        )
        cls.control_contracts = json.loads(
            CONTROL_CONTRACT_FIXTURES.read_text(encoding="utf-8")
        )
        semantics_spec = importlib.util.spec_from_file_location(
            "plan_contract_semantics",
            SKILL_ROOT / "scripts" / "contract_semantics.py",
        )
        if semantics_spec is None or semantics_spec.loader is None:
            raise RuntimeError("cannot load contract semantics")
        cls.contract_semantics = importlib.util.module_from_spec(semantics_spec)
        semantics_spec.loader.exec_module(cls.contract_semantics)

    def run_cli(self, command: str, path: Path) -> tuple[int, dict]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), command, str(path), "--json"],
            check=False,
            capture_output=True,
            text=True,
        )
        return result.returncode, json.loads(result.stdout)

    def run_arguments(self, *arguments: object) -> tuple[int, dict, str]:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                *(str(argument) for argument in arguments),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        return result.returncode, json.loads(result.stdout), result.stdout

    def run_source_cli(
        self,
        command: str,
        paths: list[Path | str],
        *options: str,
    ) -> tuple[int, dict]:
        arguments = []
        for path in paths:
            candidate = Path(path)
            arguments.append(
                candidate.relative_to(REPOSITORY_ROOT).as_posix()
                if candidate.is_absolute()
                else candidate.as_posix()
            )
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                command,
                *arguments,
                "--source-root",
                str(REPOSITORY_ROOT),
                *options,
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=REPOSITORY_ROOT,
        )
        return result.returncode, json.loads(result.stdout)

    def write_plan(self, plan: dict) -> Path:
        temporary = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            encoding="utf-8",
            delete=False,
        )
        with temporary:
            json.dump(plan, temporary)
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        return Path(temporary.name)

    def finalized_record(self, record: dict) -> dict:
        value = json.loads(json.dumps(record))
        content_fields = {
            "sys4ai.plan-task-receipt.v1": "receipt_content_sha256",
            "sys4ai.plan-normalization-report.v1": "report_content_sha256",
            "sys4ai.plan-amendment.v1": "amendment_content_sha256",
            "sys4ai.plan-task-supersession.v1": "supersession_content_sha256",
            "sys4ai.plan-provider-intent.v1": "intent_content_sha256",
            "sys4ai.plan-selection-proof.v1": "proof_content_sha256",
        }
        field = content_fields.get(value["schema_version"])
        if field is not None:
            value[field] = self.planctl.content_sha256(
                {key: item for key, item in value.items() if key != field}
            )
        return value

    def initialized_state(self) -> dict:
        state = json.loads(json.dumps(self.active_state))
        plan_sha256 = hashlib.sha256(PLAN_FIXTURE.read_bytes()).hexdigest()
        repository_fingerprint = "c" * 64
        state.update(
            {
                "plan_sha256": plan_sha256,
                "repository_fingerprint": repository_fingerprint,
                "revision": 1,
                "phase": "initialized",
                "current_generation": 0,
                "active_task_id": None,
                "counters": {
                    "worker_discussions": 0,
                    "continue_invocations": 0,
                    "agentjobs": 0,
                    "provider_creates": 0,
                    "successor_creates": 0,
                    "tasks_completed": 0,
                    "tasks_superseded": 0,
                    "protected_stops": 0,
                },
                "lease": None,
                "evaluation": "unmet",
                "fingerprints": {
                    "initial": repository_fingerprint,
                    "current": repository_fingerprint,
                    "history": [repository_fingerprint],
                },
                "terminal_reason": None,
                "updated_at": "2026-01-01T00:00:00Z",
            }
        )
        for task, definition in zip(state["tasks"], self.plan["tasks"], strict=True):
            task.update(
                {
                    "task_id": definition["task_id"],
                    "task_sha256": definition["task_sha256"],
                    "status": "pending",
                    "generation": None,
                    "counters": {
                        "worker_discussions": 0,
                        "continue_invocations": 0,
                        "agentjobs": 0,
                        "provider_creates": 0,
                        "successor_creates": 0,
                        "same_task_successors": 0,
                    },
                    "receipt_link": None,
                    "fingerprint_before": None,
                    "fingerprint_after": None,
                    "terminal_reason": None,
                    "updated_at": "2026-01-01T00:00:00Z",
                    "extensions": {},
                }
            )
        return state

    def bound_receipt(
        self,
        *,
        task_id: str = "TASK-001",
        task_sha256: str = "1" * 64,
        phase_id: str = "PHASE-01",
        disposition: str = "task_complete",
    ) -> dict:
        receipt = json.loads(json.dumps(self.receipt))
        receipt["plan_identity"].update(
            {
                "plan_id": self.plan["plan_id"],
                "plan_sha256": hashlib.sha256(PLAN_FIXTURE.read_bytes()).hexdigest(),
                "phase_id": phase_id,
            }
        )
        receipt["task_identity"] = {
            "task_id": task_id,
            "task_sha256": task_sha256,
        }
        receipt["relay_identity"]["generation"] = 1
        receipt["repository_evidence"]["fingerprint_before"] = "4" * 64
        receipt["repository_evidence"]["fingerprint_after"] = "5" * 64
        receipt["execution"].update(
            {
                "outcome": "zero_job",
                "worker_discussions": 1,
                "continue_invocations": 1,
                "agentjobs": 0,
                "agent_job_id": None,
                "provider_create_calls": 0,
                "successor_creates": 0,
                "same_task_successors": 0,
                "zero_job_reason": "The bounded task required no AgentJob.",
            }
        )
        receipt["disposition"] = disposition
        receipt["terminal_reason"] = (
            "The task requires append-only replacement task identities."
            if disposition == "replan_required"
            else None
        )
        receipt["replanning"]["status"] = (
            "required" if disposition == "replan_required" else "not_required"
        )
        receipt["coordinator_action"] = {
            "kind": (
                "await_replan"
                if disposition == "replan_required"
                else "dispatch_next_task"
            ),
            "next_task_id": (
                None if disposition == "replan_required" else "TASK-002"
            ),
        }
        return self.finalized_record(receipt)

    def state_with_receipt(
        self,
        receipt: dict,
        receipt_path: Path,
        *,
        lifecycle_status: str = "completed",
    ) -> dict:
        state = self.initialized_state()
        task = state["tasks"][0]
        task.update(
            {
                "status": lifecycle_status,
                "generation": 1,
                "counters": {
                    "worker_discussions": 1,
                    "continue_invocations": 1,
                    "agentjobs": 0,
                    "provider_creates": 0,
                    "successor_creates": 0,
                    "same_task_successors": 0,
                },
                "receipt_link": {
                    "receipt_id": receipt["receipt_id"],
                    "receipt_sha256": hashlib.sha256(
                        receipt_path.read_bytes()
                    ).hexdigest(),
                },
                "fingerprint_before": receipt["repository_evidence"][
                    "fingerprint_before"
                ],
                "fingerprint_after": receipt["repository_evidence"][
                    "fingerprint_after"
                ],
                "terminal_reason": (
                    "The task was replaced by append-only successor task identities."
                    if lifecycle_status == "superseded"
                    else None
                ),
                "updated_at": "2026-01-01T00:05:00Z",
            }
        )
        state.update(
            {
                "phase": "continuation_required",
                "current_generation": 1,
                "counters": {
                    "worker_discussions": 1,
                    "continue_invocations": 1,
                    "agentjobs": 0,
                    "provider_creates": 0,
                    "successor_creates": 0,
                    "tasks_completed": int(lifecycle_status == "completed"),
                    "tasks_superseded": int(lifecycle_status == "superseded"),
                    "protected_stops": 0,
                },
                "fingerprints": {
                    "initial": "4" * 64,
                    "current": state["repository_fingerprint"],
                    "history": [
                        "4" * 64,
                        "5" * 64,
                        state["repository_fingerprint"],
                    ],
                },
                "updated_at": "2026-01-01T00:05:00Z",
            }
        )
        return state

    def valid_supersession(self, receipt: dict, receipt_path: Path) -> dict:
        supersession = json.loads(
            json.dumps(self.control_contracts["task_supersession"])
        )
        supersession.update(
            {
                "plan_id": self.plan["plan_id"],
                "plan_sha256": hashlib.sha256(
                    PLAN_FIXTURE.read_bytes()
                ).hexdigest(),
            }
        )
        supersession["original_task"].update(
            {
                "task_id": "TASK-001",
                "task_sha256": "1" * 64,
                "generation": 1,
                "receipt_id": receipt["receipt_id"],
                "receipt_sha256": hashlib.sha256(
                    receipt_path.read_bytes()
                ).hexdigest(),
            }
        )
        supersession["replacement_tasks"] = [
            {
                "task_id": "TASK-001A",
                "task_sha256": "a" * 64,
                "depends_on": [],
                "canonical_position": 3,
                "one_task_per_discussion": True,
                "max_continue_invocations": 1,
                "max_agentjobs": 1,
            },
            {
                "task_id": "TASK-001B",
                "task_sha256": "b" * 64,
                "depends_on": ["TASK-001A"],
                "canonical_position": 4,
                "one_task_per_discussion": True,
                "max_continue_invocations": 1,
                "max_agentjobs": 1,
            },
        ]
        supersession["replacement_graph_sha256"] = self.planctl.content_sha256(
            [
                {
                    "task_id": replacement["task_id"],
                    "task_sha256": replacement["task_sha256"],
                    "depends_on": replacement["depends_on"],
                    "canonical_position": replacement["canonical_position"],
                }
                for replacement in supersession["replacement_tasks"]
            ]
        )
        supersession["acceptance_mapping"] = [
            {
                "criterion_id": "ACCEPT-001",
                "replacement_task_ids": ["TASK-001A"],
                "shared_gate_ref": None,
            },
            {
                "criterion_id": "ACCEPT-002",
                "replacement_task_ids": ["TASK-001B"],
                "shared_gate_ref": None,
            },
        ]
        return self.finalized_record(supersession)

    @staticmethod
    def pending_lifecycle(task_id: str, task_sha256: str) -> dict:
        return {
            "task_id": task_id,
            "task_sha256": task_sha256,
            "status": "pending",
            "generation": None,
            "counters": {
                "worker_discussions": 0,
                "continue_invocations": 0,
                "agentjobs": 0,
                "provider_creates": 0,
                "successor_creates": 0,
                "same_task_successors": 0,
            },
            "receipt_link": None,
            "fingerprint_before": None,
            "fingerprint_after": None,
            "terminal_reason": None,
            "updated_at": "2026-01-01T00:05:00Z",
            "extensions": {},
        }

    @staticmethod
    def legacy_plan() -> dict:
        return {
            "schema_version": "sys4ai.implementation-plan.v1",
            "plan_id": "PLAN-LEGACY-001",
            "title": "Legacy read-compatible fixture",
            "status": "active",
            "serial_execution": True,
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "task_sha256": "1" * 64,
                    "title": "Completed prerequisite",
                    "status": "completed",
                    "depends_on": [],
                    "extensions": {},
                },
                {
                    "task_id": "TASK-002",
                    "task_sha256": "2" * 64,
                    "title": "Pending task",
                    "status": "pending",
                    "depends_on": ["TASK-001"],
                    "extensions": {},
                },
            ],
            "extensions": {},
        }

    def test_valid_immutable_fixture_requires_separate_state_for_selection(self) -> None:
        code, validation = self.run_cli("validate", PLAN_FIXTURE)
        self.assertEqual(code, 0)
        self.assertEqual(validation["status"], "valid")

        code, selection = self.run_cli("select-next", PLAN_FIXTURE)
        self.assertEqual(code, 0)
        self.assertEqual(selection["status"], "state_required")
        self.assertIsNone(selection["selection"])

    def test_v1_fixture_remains_read_compatible(self) -> None:
        path = self.write_plan(self.legacy_plan())
        code, validation = self.run_cli("validate", path)
        self.assertEqual(code, 0)
        self.assertEqual(validation["status"], "valid")
        code, selection = self.run_cli("select-next", path)
        self.assertEqual(code, 0)
        self.assertEqual(selection["status"], "selected")
        self.assertEqual(selection["selection"]["task_id"], "TASK-002")

    def test_schema_rejects_unknown_critical_and_mutable_fields(self) -> None:
        plan = json.loads(json.dumps(self.plan))
        plan["unexpected"] = True
        code, result = self.run_cli("validate", self.write_plan(plan))
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "invalid")

        plan = json.loads(json.dumps(self.plan))
        plan["status"] = "active"
        plan["tasks"][0]["status"] = "pending"
        code, result = self.run_cli("validate", self.write_plan(plan))
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "invalid")

        plan = json.loads(json.dumps(self.plan))
        plan["extensions"]["unknown.required"] = {"required": True}
        code, result = self.run_cli("validate", self.write_plan(plan))
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "invalid")

    def test_semantics_reject_unknown_dependency_and_cycle(self) -> None:
        plan = self.legacy_plan()
        plan["tasks"][0]["status"] = "pending"
        plan["tasks"][0]["depends_on"] = ["TASK-002", "TASK-404"]
        code, result = self.run_cli("validate", self.write_plan(plan))
        self.assertEqual(code, 1)
        self.assertTrue(
            any("task.unknown_dependency" in item for item in result["findings"])
        )
        self.assertTrue(
            any("task.dependency_cycle" in item for item in result["findings"])
        )

    def test_no_ready_task_is_read_only_success(self) -> None:
        plan = self.legacy_plan()
        plan["tasks"][1]["status"] = "blocked"
        code, result = self.run_cli("select-next", self.write_plan(plan))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "no_ready_task")
        self.assertIsNone(result["selection"])

    def test_active_task_blocks_second_selection(self) -> None:
        plan = self.legacy_plan()
        plan["tasks"][1]["status"] = "in_progress"
        code, result = self.run_cli("select-next", self.write_plan(plan))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "no_ready_task")
        self.assertIsNone(result["selection"])

        plan["tasks"].append(
            {
                "task_id": "TASK-003",
                "task_sha256": "3" * 64,
                "title": "Second active task",
                "status": "in_progress",
                "depends_on": ["TASK-001"],
                "extensions": {},
            }
        )
        code, result = self.run_cli("validate", self.write_plan(plan))
        self.assertEqual(code, 1)
        self.assertTrue(
            any("plan.multiple_active_tasks" in item for item in result["findings"])
        )

    def test_v2_rejects_scope_and_phase_membership_mismatch(self) -> None:
        plan = json.loads(json.dumps(self.plan))
        plan["required_scope"]["task_ids"].reverse()
        plan["phases"][0]["task_ids"] = ["TASK-002"]
        code, result = self.run_cli("validate", self.write_plan(plan))
        self.assertEqual(code, 1)
        self.assertTrue(
            any("plan.required_task_scope_mismatch" in item for item in result["findings"])
        )
        self.assertTrue(
            any("task.phase_membership_mismatch" in item for item in result["findings"])
        )

    def test_v2_freezes_one_task_execution_budget(self) -> None:
        for field, value in (
            ("one_task_per_discussion", False),
            ("max_continue_invocations", 2),
            ("max_agentjobs", 2),
            ("same_task_successors", 1),
        ):
            with self.subTest(field=field):
                plan = json.loads(json.dumps(self.plan))
                plan["tasks"][0]["execution_budget"][field] = value
                code, result = self.run_cli("validate", self.write_plan(plan))
                self.assertEqual(code, 1)
                self.assertEqual(result["status"], "invalid")

    def test_envelope_fixture_validates_and_cardinality_is_constant(self) -> None:
        code, result = self.run_cli("validate-envelope", ENVELOPE_FIXTURE)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

        envelope = json.loads(ENVELOPE_FIXTURE.read_text(encoding="utf-8"))
        envelope["max_agentjobs"] = 2
        code, result = self.run_cli(
            "validate-envelope",
            self.write_plan(envelope),
        )
        self.assertEqual(code, 1)
        self.assertTrue(any("const" in item for item in result["findings"]))

    def validate_state(self, state: dict) -> list:
        return self.planctl.validate_instance(state, STATE_SCHEMA)

    def validate_receipt(self, receipt: dict) -> list:
        return self.planctl.validate_instance(receipt, RECEIPT_SCHEMA)

    def validate_contract(self, name: str, record: dict) -> list:
        return self.planctl.validate_instance(record, CONTRACT_SCHEMAS[name])

    def receipt_for_case(self, case: dict) -> dict:
        receipt = json.loads(json.dumps(self.receipt))
        execution = receipt["execution"]
        execution["outcome"] = case["execution_outcome"]
        execution["continue_invocations"] = case["continue_invocations"]
        execution["agentjobs"] = case["agentjobs"]
        receipt["disposition"] = case["disposition"]
        receipt["terminal_reason"] = (
            f"Protected outcome: {case['case_id']}."
            if case["terminal_reason_required"]
            else None
        )
        receipt["recovery"]["status"] = case["recovery_status"]
        receipt["replanning"]["status"] = case["replanning_status"]
        receipt["coordinator_action"]["kind"] = case["coordinator_action"]
        receipt["coordinator_action"]["next_task_id"] = (
            "TASK-EXAMPLE-002"
            if case["coordinator_action"] == "dispatch_next_task"
            else None
        )
        receipt["direct_evidence"]["approvals"][0]["status"] = (
            "missing" if case["disposition"] == "human_gate_required" else "not_required"
        )
        receipt["direct_evidence"]["validator_results"][0]["status"] = (
            "fail" if case["disposition"] == "validation_failed" else "pass"
        )
        if execution["outcome"] == "one_job":
            execution["agent_job_id"] = "AJ-EXAMPLE-001"
            execution["zero_job_reason"] = None
        elif execution["outcome"] == "unknown":
            execution["agent_job_id"] = None
            execution["zero_job_reason"] = "The consumed invocation outcome is unknown."
        else:
            execution["agent_job_id"] = None
            execution["zero_job_reason"] = "No AgentJob was executed."
        receipt["direct_evidence"]["plan_completion"] = (
            {
                "task_receipts": [
                    {
                        "receipt_id": "PTR-EXAMPLE-001",
                        "receipt_sha256": "9" * 64,
                    }
                ],
                "phase_gate_receipts": [
                    {
                        "receipt_id": "PGR-EXAMPLE-001",
                        "receipt_sha256": "a" * 64,
                    }
                ],
                "final_validator_refs": [
                    "implementation_plans/example/final-validation.md"
                ],
                "completion_contract_status": "pass",
            }
            if case["disposition"] == "plan_complete"
            else None
        )
        return receipt

    def test_plan_state_active_and_completed_fixtures_validate(self) -> None:
        self.assertEqual(self.validate_state(self.active_state), [])
        self.assertEqual(self.validate_state(self.completed_state), [])

    def test_plan_state_rejects_multiple_active_tasks(self) -> None:
        state = json.loads(json.dumps(self.active_state))
        state["tasks"][2]["status"] = "reserved"
        state["tasks"][2]["generation"] = 3
        state["tasks"][2]["counters"]["provider_creates"] = 1
        self.assertTrue(self.validate_state(state))

    def test_plan_state_active_phase_requires_identity_and_lease(self) -> None:
        for field, value in (("active_task_id", None), ("lease", None)):
            with self.subTest(field=field):
                state = json.loads(json.dumps(self.active_state))
                state[field] = value
                self.assertTrue(self.validate_state(state))

        state = json.loads(json.dumps(self.active_state))
        state["tasks"][1]["generation"] = None
        self.assertTrue(self.validate_state(state))

        state = json.loads(json.dumps(self.active_state))
        state["tasks"][1]["status"] = "reserved"
        self.assertTrue(self.validate_state(state))

    def test_plan_state_rejects_task_cardinality_overflow(self) -> None:
        for field, value in (
            ("worker_discussions", 2),
            ("continue_invocations", 2),
            ("agentjobs", 2),
            ("provider_creates", 2),
            ("successor_creates", 2),
            ("same_task_successors", 1),
        ):
            with self.subTest(field=field):
                state = json.loads(json.dumps(self.active_state))
                state["tasks"][1]["counters"][field] = value
                self.assertTrue(self.validate_state(state))

    def test_plan_state_terminal_task_requires_receipt_and_stop_reason(self) -> None:
        state = json.loads(json.dumps(self.completed_state))
        state["tasks"][0]["receipt_link"] = None
        self.assertTrue(self.validate_state(state))

        state = json.loads(json.dumps(self.completed_state))
        state["tasks"][0]["status"] = "validation_failed"
        state["tasks"][0]["terminal_reason"] = None
        self.assertTrue(self.validate_state(state))

    def test_plan_state_terminal_plan_requires_closed_met_state(self) -> None:
        for field, value in (
            ("active_task_id", "TASK-003"),
            ("lease", self.active_state["lease"]),
            ("evaluation", "unmet"),
            ("terminal_reason", None),
        ):
            with self.subTest(field=field):
                state = json.loads(json.dumps(self.completed_state))
                state[field] = value
                self.assertTrue(self.validate_state(state))

    def test_plan_state_rejects_invalid_fingerprint_and_unknown_field(self) -> None:
        state = json.loads(json.dumps(self.active_state))
        state["fingerprints"]["current"] = "not-a-sha256"
        self.assertTrue(self.validate_state(state))

        state = json.loads(json.dumps(self.active_state))
        state["unexpected"] = True
        self.assertTrue(self.validate_state(state))

    def test_plan_task_receipt_template_and_all_outcome_fixtures_validate(self) -> None:
        self.assertEqual(self.receipt_outcomes["base_fixture"], RECEIPT_FIXTURE.relative_to(SKILL_ROOT).as_posix())
        self.assertEqual(self.validate_receipt(self.receipt), [])
        cases = self.receipt_outcomes["cases"]
        self.assertEqual(
            [case["case_id"] for case in cases],
            [
                "zero-job",
                "one-job",
                "blocked",
                "replan",
                "human-gated",
                "validation-failed",
                "unknown",
                "cancelled",
                "task-complete",
                "plan-complete",
            ],
        )
        for case in cases:
            with self.subTest(case=case["case_id"]):
                self.assertEqual(self.validate_receipt(self.receipt_for_case(case)), [])

    def test_plan_task_receipt_enforces_identity_hashes_and_cardinality(self) -> None:
        for path, value in (
            (("plan_identity", "plan_sha256"), "not-a-hash"),
            (("task_identity", "task_sha256"), "not-a-hash"),
            (("relay_identity", "handoff_token_sha256"), "not-a-hash"),
            (("execution", "worker_discussions"), 2),
            (("execution", "provider_create_calls"), 2),
            (("execution", "successor_creates"), 2),
            (("execution", "same_task_successors"), 1),
        ):
            with self.subTest(path=path):
                receipt = json.loads(json.dumps(self.receipt))
                receipt[path[0]][path[1]] = value
                self.assertTrue(self.validate_receipt(receipt))

    def test_plan_task_receipt_enforces_zero_one_and_unknown_execution_shapes(self) -> None:
        receipt = json.loads(json.dumps(self.receipt))
        receipt["execution"]["agentjobs"] = 1
        self.assertTrue(self.validate_receipt(receipt))

        one_job = self.receipt_for_case(self.receipt_outcomes["cases"][1])
        one_job["execution"]["agent_job_id"] = None
        self.assertTrue(self.validate_receipt(one_job))

        unknown = self.receipt_for_case(self.receipt_outcomes["cases"][6])
        unknown["execution"]["continue_invocations"] = 1
        self.assertTrue(self.validate_receipt(unknown))

    def test_plan_task_receipt_enforces_disposition_specific_evidence(self) -> None:
        for case_id in ("blocked", "human-gated", "validation-failed", "cancelled"):
            case = next(
                item for item in self.receipt_outcomes["cases"]
                if item["case_id"] == case_id
            )
            receipt = self.receipt_for_case(case)
            receipt["terminal_reason"] = None
            self.assertTrue(self.validate_receipt(receipt))

        replan = self.receipt_for_case(self.receipt_outcomes["cases"][3])
        replan["replanning"]["status"] = "not_required"
        self.assertTrue(self.validate_receipt(replan))

        unknown = self.receipt_for_case(self.receipt_outcomes["cases"][6])
        unknown["recovery"]["status"] = "not_required"
        self.assertTrue(self.validate_receipt(unknown))

    def test_plan_task_receipt_enforces_completion_and_plan_completion_evidence(self) -> None:
        receipt = json.loads(json.dumps(self.receipt))
        receipt["direct_evidence"]["acceptance_results"][0]["status"] = "fail"
        receipt["direct_evidence"]["acceptance_results"][0]["evidence_refs"] = []
        self.assertTrue(self.validate_receipt(receipt))

        plan_complete = self.receipt_for_case(self.receipt_outcomes["cases"][9])
        plan_complete["direct_evidence"]["plan_completion"] = None
        self.assertTrue(self.validate_receipt(plan_complete))

        plan_complete = self.receipt_for_case(self.receipt_outcomes["cases"][9])
        plan_complete["coordinator_action"]["kind"] = "dispatch_next_task"
        plan_complete["coordinator_action"]["next_task_id"] = "TASK-EXAMPLE-002"
        self.assertTrue(self.validate_receipt(plan_complete))

    def test_plan_task_receipt_rejects_unsafe_paths_unknown_fields_and_live_tokens(self) -> None:
        receipt = json.loads(json.dumps(self.receipt))
        receipt["direct_evidence"]["changed_paths"] = ["../outside"]
        self.assertTrue(self.validate_receipt(receipt))

        receipt = json.loads(json.dumps(self.receipt))
        receipt["handoff_token"] = "forbidden-live-token"
        self.assertTrue(self.validate_receipt(receipt))

    def test_phase_02_control_contract_examples_validate(self) -> None:
        self.assertEqual(set(self.control_contracts), set(CONTRACT_SCHEMAS))
        for name, record in self.control_contracts.items():
            with self.subTest(contract=name):
                self.assertEqual(self.validate_contract(name, record), [])
        self.assertEqual(
            self.contract_semantics.validate_contract_set(self.control_contracts),
            [],
        )

    def test_normalization_contract_enforces_traceability_and_sizing(self) -> None:
        report = json.loads(json.dumps(self.control_contracts["normalization_report"]))
        report["traceability"][0]["transformation"] = "synthesized"
        report["traceability"][0]["generated"] = False
        self.assertTrue(self.validate_contract("normalization_report", report))

        report = json.loads(json.dumps(self.control_contracts["normalization_report"]))
        report["task_sizing"][0]["result"] = "split_required"
        self.assertTrue(self.validate_contract("normalization_report", report))

    def test_amendment_contract_preserves_identity_history_and_authority(self) -> None:
        for field, value in (
            ("plan_identity_unchanged", False),
            ("prior_receipts_preserved", False),
            ("consumed_invocations_preserved", False),
        ):
            amendment = json.loads(json.dumps(self.control_contracts["plan_amendment"]))
            amendment[field] = value
            self.assertTrue(self.validate_contract("plan_amendment", amendment))

        amendment = json.loads(json.dumps(self.control_contracts["plan_amendment"]))
        amendment["operations"][0]["protected_effects_added"] = True
        self.assertTrue(self.validate_contract("plan_amendment", amendment))

    def test_supersession_contract_enforces_new_ids_and_one_task_budgets(self) -> None:
        supersession = json.loads(json.dumps(self.control_contracts["task_supersession"]))
        supersession["replacement_tasks"][0]["max_continue_invocations"] = 2
        self.assertTrue(self.validate_contract("task_supersession", supersession))

        supersession = json.loads(json.dumps(self.control_contracts["task_supersession"]))
        supersession["replacement_tasks"][0]["task_id"] = supersession["original_task"]["task_id"]
        findings = self.contract_semantics.validate_contract_set(
            {**self.control_contracts, "task_supersession": supersession}
        )
        self.assertIn("supersession.original_task_reused", findings)

    def test_provider_intent_contract_quarantines_uncertain_and_duplicate_outcomes(self) -> None:
        provider = json.loads(json.dumps(self.control_contracts["provider_intent"]))
        provider["retry_authorized"] = True
        self.assertTrue(self.validate_contract("provider_intent", provider))

        provider = json.loads(json.dumps(self.control_contracts["provider_intent"]))
        provider["recovery"]["status"] = "not_required"
        self.assertTrue(self.validate_contract("provider_intent", provider))

        provider = json.loads(json.dumps(self.control_contracts["provider_intent"]))
        provider["status"] = "duplicate"
        provider["conflicting_thread_ids"] = ["THREAD-ONLY-ONE"]
        self.assertTrue(self.validate_contract("provider_intent", provider))

    def test_selection_proof_is_revision_bound_and_first_ready_only(self) -> None:
        proof = json.loads(json.dumps(self.control_contracts["selection_proof"]))
        proof["active_task_ids"] = ["TASK-ACTIVE-001"]
        self.assertTrue(self.validate_contract("selection_proof", proof))

        proof = json.loads(json.dumps(self.control_contracts["selection_proof"]))
        proof["ordered_tasks"].insert(
            0,
            {
                "canonical_position": 0,
                "task_id": "TASK-EARLIER-READY",
                "task_sha256": "2323232323232323232323232323232323232323232323232323232323232323",
                "effective_task_ids": ["TASK-EARLIER-READY"],
                "status": "pending",
                "dependencies": [],
                "dependency_ready": True,
            },
        )
        findings = self.contract_semantics.validate_contract_set(
            {**self.control_contracts, "selection_proof": proof}
        )
        self.assertIn("selection.not_first_ready_task", findings)

    def test_validate_record_covers_every_profile_and_content_hash(self) -> None:
        records = [
            ("implementation_plan", self.plan),
            ("implementation_plan_state", self.initialized_state()),
            (
                "plan_task_envelope",
                json.loads(ENVELOPE_FIXTURE.read_text(encoding="utf-8")),
            ),
            ("plan_task_receipt", self.bound_receipt()),
            (
                "normalization_report",
                self.finalized_record(
                    self.control_contracts["normalization_report"]
                ),
            ),
            (
                "plan_amendment",
                self.finalized_record(self.control_contracts["plan_amendment"]),
            ),
            (
                "task_supersession",
                self.finalized_record(
                    self.control_contracts["task_supersession"]
                ),
            ),
            (
                "provider_intent",
                self.finalized_record(self.control_contracts["provider_intent"]),
            ),
            (
                "selection_proof",
                self.finalized_record(self.control_contracts["selection_proof"]),
            ),
        ]
        for expected_profile, record in records:
            with self.subTest(profile=expected_profile):
                code, result, _ = self.run_arguments(
                    "validate-record",
                    self.write_plan(record),
                )
                self.assertEqual(code, 0)
                self.assertEqual(result["status"], "valid")
                self.assertEqual(result["record_profile"], expected_profile)
                self.assertEqual(result["findings"], [])

        receipt = self.bound_receipt()
        receipt["receipt_content_sha256"] = "0" * 64
        code, result, _ = self.run_arguments(
            "validate-record",
            self.write_plan(receipt),
        )
        self.assertEqual(code, 1)
        self.assertEqual(
            [finding["code"] for finding in result["findings"]],
            ["record.content_hash_mismatch"],
        )

    def test_validate_state_checks_hashes_counters_and_repository_evidence(self) -> None:
        state = self.initialized_state()
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(state),
            "--repository-fingerprint",
            state["repository_fingerprint"],
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["record_counts"]["states"], 1)

        drifted = json.loads(json.dumps(state))
        drifted["tasks"][0]["task_sha256"] = "9" * 64
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(drifted),
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "task.hash_drift",
            {finding["code"] for finding in result["findings"]},
        )

        inconsistent = json.loads(json.dumps(state))
        inconsistent["counters"]["continue_invocations"] = 1
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(inconsistent),
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "state.counter_mismatch",
            {finding["code"] for finding in result["findings"]},
        )

        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(state),
            "--repository-fingerprint",
            "d" * 64,
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "state.repository_fingerprint_mismatch",
            {finding["code"] for finding in result["findings"]},
        )

    def test_state_aware_selection_is_deterministic_revision_bound_and_read_only(self) -> None:
        state = self.initialized_state()
        state_path = self.write_plan(state)
        arguments = (
            "select-next",
            PLAN_FIXTURE,
            "--state",
            state_path,
            "--prior-journal-sha256",
            "a" * 64,
        )
        first_code, first, _ = self.run_arguments(*arguments)
        second_code, second, _ = self.run_arguments(*arguments)
        self.assertEqual(first_code, 0)
        self.assertEqual(second_code, 0)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "selected")
        self.assertEqual(first["selection"]["task_id"], "TASK-001")
        self.assertEqual(first["selection_proof"]["plan_revision"], state["revision"])
        self.assertEqual(
            json.loads(state_path.read_text(encoding="utf-8")),
            state,
        )

        proof_path = self.write_plan(first["selection_proof"])
        code, result, _ = self.run_arguments("validate-record", proof_path)
        self.assertEqual(code, 0)
        self.assertEqual(result["record_profile"], "selection_proof")
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            state_path,
            "--selection-proof",
            proof_path,
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

        invalid_proof = json.loads(json.dumps(first["selection_proof"]))
        invalid_proof["ordered_tasks"][0]["task_sha256"] = "9" * 64
        invalid_proof = self.finalized_record(invalid_proof)
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            state_path,
            "--selection-proof",
            self.write_plan(invalid_proof),
        )
        self.assertEqual(code, 1)
        self.assertTrue(
            {"selection.proof_invalid", "task.hash_drift"}
            <= {finding["code"] for finding in result["findings"]}
        )

    def test_state_aware_selection_blocks_when_one_task_is_reserved(self) -> None:
        state = self.initialized_state()
        task = state["tasks"][0]
        task["status"] = "reserved"
        task["generation"] = 1
        task["counters"]["provider_creates"] = 1
        state["phase"] = "task_reserved"
        state["current_generation"] = 1
        state["active_task_id"] = task["task_id"]
        state["counters"]["provider_creates"] = 1
        state["lease"] = json.loads(json.dumps(self.active_state["lease"]))
        state["lease"].update(
            {
                "generation": 1,
                "task_id": task["task_id"],
                "repository_fingerprint": state["repository_fingerprint"],
            }
        )
        code, result, _ = self.run_arguments(
            "select-next",
            PLAN_FIXTURE,
            "--state",
            self.write_plan(state),
            "--prior-journal-sha256",
            "a" * 64,
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "blocked_no_runnable")
        self.assertIsNone(result["selection"])
        self.assertEqual(
            result["selection_proof"]["blocking_reasons"],
            ["selection.active_task_present"],
        )

        recovery = self.initialized_state()
        recovery["phase"] = "recovery_pending"
        recovery["terminal_reason"] = "Provider identity requires explicit recovery."
        code, result, _ = self.run_arguments(
            "select-next",
            PLAN_FIXTURE,
            "--state",
            self.write_plan(recovery),
            "--prior-journal-sha256",
            "a" * 64,
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "blocked_no_runnable")
        self.assertEqual(
            result["selection_proof"]["blocking_reasons"],
            ["selection.state_not_schedulable"],
        )

    def test_receipt_links_execution_and_dependency_selection_are_validated(self) -> None:
        receipt = self.bound_receipt()
        receipt_path = self.write_plan(receipt)
        state = self.state_with_receipt(receipt, receipt_path)
        state_path = self.write_plan(state)
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            state_path,
            "--receipt",
            receipt_path,
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

        code, result, _ = self.run_arguments(
            "select-next",
            PLAN_FIXTURE,
            "--state",
            state_path,
            "--receipt",
            receipt_path,
            "--prior-journal-sha256",
            "b" * 64,
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["selection"]["task_id"], "TASK-002")
        self.assertEqual(
            result["selection"]["dependency_receipt_sha256s"],
            [hashlib.sha256(receipt_path.read_bytes()).hexdigest()],
        )

        mismatched_receipt = json.loads(json.dumps(receipt))
        mismatched_receipt["execution"]["provider_create_calls"] = 1
        mismatched_receipt = self.finalized_record(mismatched_receipt)
        mismatched_path = self.write_plan(mismatched_receipt)
        mismatched_state = self.state_with_receipt(
            mismatched_receipt,
            mismatched_path,
        )
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(mismatched_state),
            "--receipt",
            mismatched_path,
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "receipt.execution_mismatch",
            {finding["code"] for finding in result["findings"]},
        )

    def test_amendment_chain_advances_only_the_effective_plan_hash(self) -> None:
        amendment = json.loads(
            json.dumps(self.control_contracts["plan_amendment"])
        )
        base_hash = hashlib.sha256(PLAN_FIXTURE.read_bytes()).hexdigest()
        effective_hash = "6" * 64
        amendment.update(
            {
                "plan_id": self.plan["plan_id"],
                "prior_effective_plan_sha256": base_hash,
                "new_effective_plan_sha256": effective_hash,
            }
        )
        amendment = self.finalized_record(amendment)
        state = self.initialized_state()
        state["plan_sha256"] = effective_hash
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(state),
            "--amendment",
            self.write_plan(amendment),
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["effective_plan_sha256"], effective_hash)

        broken = json.loads(json.dumps(amendment))
        broken["prior_effective_plan_sha256"] = "9" * 64
        broken = self.finalized_record(broken)
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(state),
            "--amendment",
            self.write_plan(broken),
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "amendment.chain_invalid",
            {finding["code"] for finding in result["findings"]},
        )

    def test_supersession_preserves_original_receipt_and_selects_new_identity(self) -> None:
        receipt = self.bound_receipt(disposition="replan_required")
        receipt_path = self.write_plan(receipt)
        supersession = self.valid_supersession(receipt, receipt_path)
        supersession_path = self.write_plan(supersession)
        state = self.state_with_receipt(
            receipt,
            receipt_path,
            lifecycle_status="superseded",
        )
        state["tasks"].extend(
            [
                self.pending_lifecycle("TASK-001A", "a" * 64),
                self.pending_lifecycle("TASK-001B", "b" * 64),
            ]
        )
        state_path = self.write_plan(state)
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            state_path,
            "--receipt",
            receipt_path,
            "--supersession",
            supersession_path,
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

        code, result, _ = self.run_arguments(
            "select-next",
            PLAN_FIXTURE,
            "--state",
            state_path,
            "--receipt",
            receipt_path,
            "--supersession",
            supersession_path,
            "--prior-journal-sha256",
            "c" * 64,
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["selection"]["task_id"], "TASK-001A")

        cyclic = json.loads(json.dumps(supersession))
        cyclic["replacement_tasks"][0]["depends_on"] = ["TASK-001B"]
        cyclic["replacement_graph_sha256"] = self.planctl.content_sha256(
            [
                {
                    "task_id": replacement["task_id"],
                    "task_sha256": replacement["task_sha256"],
                    "depends_on": replacement["depends_on"],
                    "canonical_position": replacement["canonical_position"],
                }
                for replacement in cyclic["replacement_tasks"]
            ]
        )
        cyclic = self.finalized_record(cyclic)
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            state_path,
            "--receipt",
            receipt_path,
            "--supersession",
            self.write_plan(cyclic),
        )
        self.assertEqual(code, 1)
        self.assertIn(
            "supersession.replacement_cycle",
            {finding["code"] for finding in result["findings"]},
        )

    def test_provider_intent_is_bound_to_plan_task_and_repository(self) -> None:
        state = self.initialized_state()
        provider = json.loads(
            json.dumps(self.control_contracts["provider_intent"])
        )
        provider.update(
            {
                "plan_id": self.plan["plan_id"],
                "plan_sha256": state["plan_sha256"],
                "task_id": "TASK-001",
                "task_sha256": "1" * 64,
                "generation": 1,
                "expected_revision": state["revision"],
                "repository_fingerprint": state["repository_fingerprint"],
                "status": "intent",
                "create_attempts": 0,
                "returned_thread_id": None,
                "provider_response_sha256": None,
                "conflicting_thread_ids": [],
                "finalized": False,
                "recovery": {
                    "status": "not_required",
                    "reason": None,
                    "evidence_refs": [],
                },
            }
        )
        provider = self.finalized_record(provider)
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(state),
            "--provider-intent",
            self.write_plan(provider),
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

        drifted = json.loads(json.dumps(provider))
        drifted["task_sha256"] = "9" * 64
        drifted = self.finalized_record(drifted)
        code, result, _ = self.run_arguments(
            "validate-state",
            PLAN_FIXTURE,
            self.write_plan(state),
            "--provider-intent",
            self.write_plan(drifted),
        )
        self.assertEqual(code, 1)
        self.assertTrue(
            {"provider.identity_mismatch", "task.hash_drift"}
            <= {finding["code"] for finding in result["findings"]}
        )

    def test_plan_diff_redaction_and_reason_catalog_are_stable(self) -> None:
        code, result, _ = self.run_arguments(
            "diff",
            PLAN_FIXTURE,
            PLAN_FIXTURE,
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "unchanged")
        self.assertEqual(result["changes"], [])

        changed = json.loads(json.dumps(self.plan))
        changed["tasks"][0]["task_sha256"] = "9" * 64
        code, result, _ = self.run_arguments(
            "diff",
            PLAN_FIXTURE,
            self.write_plan(changed),
        )
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "changed")
        self.assertIn(
            "task.hash_drift",
            {finding["code"] for finding in result["findings"]},
        )

        sensitive = {
            "handoff_token": "live-handoff-token-value-that-must-not-escape",
            "nested": {
                "api_key": "sk-proj-abcdefghijklmnopqrstuvwxyz1234567890"
            },
            "safe_sha256": "a" * 64,
        }
        sensitive_path = self.write_plan(sensitive)
        first_code, first, first_stdout = self.run_arguments(
            "redact",
            sensitive_path,
        )
        second_code, second, second_stdout = self.run_arguments(
            "redact",
            sensitive_path,
        )
        self.assertEqual(first_code, 0)
        self.assertEqual(second_code, 0)
        self.assertEqual(first, second)
        self.assertEqual(first_stdout, second_stdout)
        self.assertNotIn(sensitive["handoff_token"], first_stdout)
        self.assertNotIn(sensitive["nested"]["api_key"], first_stdout)
        self.assertEqual(
            first["redacted_paths"],
            ["$.handoff_token", "$.nested.api_key"],
        )
        self.assertEqual(
            json.loads(sensitive_path.read_text(encoding="utf-8")),
            sensitive,
        )

        first_code, first, _ = self.run_arguments("reason-codes")
        second_code, second, _ = self.run_arguments("reason-codes")
        self.assertEqual(first_code, 0)
        self.assertEqual(second_code, 0)
        self.assertEqual(first, second)
        codes = [item["code"] for item in first["reason_codes"]]
        self.assertEqual(codes, sorted(codes))
        self.assertEqual(len(codes), len(set(codes)))
        self.assertTrue(
            {
                "plan.authority_missing",
                "record.content_hash_mismatch",
                "selection.proof_invalid",
                "task.hash_drift",
            }
            <= set(codes)
        )

    def test_source_classifier_covers_all_seven_routes_with_explanations(self) -> None:
        cases = [
            ("structured_plan", self.plan),
            (
                "partial_plan",
                {
                    "plan_id": "PLAN-PARTIAL-001",
                    "title": "Partial plan",
                    "tasks": [{"title": "One incomplete task"}],
                },
            ),
            ("task_list", ["Implement the behavior", "Verify the behavior"]),
            (
                "phase_outline",
                {
                    "phases": [
                        {"title": "Establish the baseline"},
                        {"title": "Deliver the change"},
                    ]
                },
            ),
            (
                "requirements",
                {
                    "requirements": [
                        "The implementation must be deterministic.",
                        "The result must be directly verified.",
                    ]
                },
            ),
            ("prose", "Please improve the bounded widget behavior."),
        ]
        for expected, value in cases:
            with self.subTest(expected=expected):
                text = value if isinstance(value, str) else json.dumps(value)
                source_class, evidence = self.planctl.classify_source(
                    value,
                    text=text,
                )
                self.assertEqual(source_class, expected)
                self.assertTrue(evidence)

        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as directory:
            root = Path(directory)
            first = root / "tasks.json"
            second = root / "requirements.json"
            first.write_text(
                json.dumps(["Implement the behavior", "Verify the behavior"]),
                encoding="utf-8",
            )
            second.write_text(
                json.dumps(
                    {
                        "requirements": [
                            "The implementation must be bounded.",
                            "The result must be verified.",
                        ]
                    }
                ),
                encoding="utf-8",
            )
            code, result = self.run_source_cli("classify", [first, second])
        self.assertEqual(code, 0)
        self.assertEqual(result["source_set_class"], "mixed_source")
        self.assertEqual(
            [source["source_class"] for source in result["sources"]],
            ["task_list", "requirements"],
        )

    def test_normalize_matches_exact_golden_output_and_is_repeatable(self) -> None:
        options = ("--authority", "accepted", "--precedence", "0")
        first_code, first = self.run_source_cli(
            "normalize",
            [NORMALIZATION_SOURCE],
            *options,
        )
        second_code, second = self.run_source_cli(
            "normalize",
            [NORMALIZATION_SOURCE],
            *options,
        )
        expected = json.loads(NORMALIZATION_GOLDEN.read_text(encoding="utf-8"))
        self.assertEqual(first_code, 0)
        self.assertEqual(second_code, 0)
        self.assertEqual(first, expected)
        self.assertEqual(second, expected)
        self.assertEqual(
            self.planctl.validate_plan(first["candidate_plan"]),
            [],
        )
        self.assertEqual(
            self.planctl.validate_instance(
                first["normalization_report"],
                SKILL_ROOT / "schemas" / "normalization-report.schema.json",
            ),
            [],
        )

    def test_normalize_preserves_a_valid_structured_plan_without_synthesis(self) -> None:
        code, result = self.run_source_cli(
            "normalize",
            [PLAN_FIXTURE],
            "--authority",
            "accepted",
            "--precedence",
            "0",
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "candidate")
        self.assertEqual(result["candidate_plan"], self.plan)
        self.assertTrue(result["normalization_report"]["canonicalization_only"])
        self.assertTrue(
            all(
                trace["generated"] is False
                for trace in result["normalization_report"]["traceability"]
            )
        )

    def test_normalize_derives_tasks_from_accepted_requirements(self) -> None:
        source = {
            "title": "Requirements-derived plan",
            "objective": "Implement two accepted requirements.",
            "acceptance": self.plan["acceptance"],
            "repository_binding": self.plan["repository_binding"],
            "requirements": [
                "The implementation must preserve accepted source wording.",
                "The result must record direct validation evidence.",
            ],
        }
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as directory:
            path = Path(directory) / "requirements.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            code, result = self.run_source_cli(
                "normalize",
                [path],
                "--authority",
                "accepted",
                "--precedence",
                "0",
            )
        self.assertEqual(code, 0)
        self.assertEqual(result["source_set_class"], "requirements")
        self.assertEqual(len(result["candidate_plan"]["phases"]), 1)
        self.assertEqual(len(result["candidate_plan"]["tasks"]), 2)
        self.assertEqual(
            [item["result"] for item in result["normalization_report"]["task_sizing"]],
            ["ready", "ready"],
        )

    def test_normalize_requires_authority_and_explicit_multi_source_precedence(self) -> None:
        code, result = self.run_source_cli("normalize", [NORMALIZATION_SOURCE])
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "human_gate_required")
        self.assertIsNone(result["candidate_plan"])
        self.assertTrue(
            any(
                finding["code"] == "plan.authority_missing"
                for finding in result["findings"]
            )
        )

        code, result = self.run_source_cli(
            "normalize",
            [NORMALIZATION_SOURCE, PLAN_FIXTURE],
            "--authority",
            "accepted",
        )
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(
            any("--precedence is required" in finding["message"] for finding in result["findings"])
        )

    def test_normalize_obeys_explicit_multi_source_authority_and_precedence(self) -> None:
        supplemental = {
            "requirements": [
                "The implementation must preserve the accepted plan.",
                "The result must remain read-only.",
            ]
        }
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as directory:
            path = Path(directory) / "supplemental.json"
            path.write_text(json.dumps(supplemental), encoding="utf-8")
            code, result = self.run_source_cli(
                "normalize",
                [path, PLAN_FIXTURE],
                "--authority",
                "supplemental",
                "--authority",
                "accepted",
                "--precedence",
                "5",
                "--precedence",
                "0",
            )
        self.assertEqual(code, 0)
        self.assertEqual(result["source_set_class"], "mixed_source")
        self.assertEqual(result["candidate_plan"], self.plan)
        self.assertEqual(
            [source["authority"] for source in result["normalization_report"]["sources"]],
            ["supplemental", "accepted"],
        )

    def test_normalize_blocks_malformed_dependencies_and_phase_membership(self) -> None:
        source = {
            "title": "Malformed accepted source",
            "objective": "Demonstrate fail-closed normalization.",
            "acceptance": self.plan["acceptance"],
            "repository_binding": self.plan["repository_binding"],
            "phases": [
                {
                    "phase_id": "PHASE-ONE",
                    "title": "Only phase",
                    "task_ids": ["TASK-UNKNOWN"],
                }
            ],
            "tasks": [
                {
                    "task_id": "TASK-ONE",
                    "title": "Bounded task",
                    "depends_on": "TASK-NOT-A-LIST",
                }
            ],
        }
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as directory:
            path = Path(directory) / "malformed.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            code, result = self.run_source_cli(
                "normalize",
                [path],
                "--authority",
                "accepted",
            )
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "blocked")
        self.assertIsNone(result["candidate_plan"])
        self.assertEqual(
            {
                finding["code"]
                for finding in result["findings"]
            },
            {"phase.task_reference_invalid", "plan.dependency_invalid"},
        )

    def test_normalize_blocks_equal_precedence_accepted_conflicts(self) -> None:
        base = {
            "plan_id": "PLAN-CONFLICT-001",
            "objective": "Deliver one accepted outcome.",
            "acceptance": self.plan["acceptance"],
            "repository_binding": self.plan["repository_binding"],
            "tasks": [{"title": "Implement the accepted outcome"}],
        }
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as directory:
            root = Path(directory)
            first = root / "first.json"
            second = root / "second.json"
            first.write_text(
                json.dumps({**base, "title": "First accepted title"}),
                encoding="utf-8",
            )
            second.write_text(
                json.dumps({**base, "title": "Conflicting accepted title"}),
                encoding="utf-8",
            )
            code, result = self.run_source_cli(
                "normalize",
                [first, second],
                "--authority",
                "accepted",
                "--precedence",
                "0",
            )
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "blocked")
        self.assertIsNone(result["candidate_plan"])
        self.assertTrue(
            any(
                finding["code"] == "normalization.accepted_source_conflict"
                for finding in result["findings"]
            )
        )

    def test_classification_and_normalization_reject_unsafe_sources(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "classify",
                str(NORMALIZATION_SOURCE),
                "--source-root",
                str(REPOSITORY_ROOT),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=REPOSITORY_ROOT,
        )
        body = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(body["findings"][0]["code"], "path.absolute_forbidden")

        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as directory:
            source = Path(directory) / "secret.txt"
            source.write_text(
                "api_key=abcdefghijklmnopqrstuvwxyz123456",
                encoding="utf-8",
            )
            code, body = self.run_source_cli("classify", [source])
        self.assertEqual(code, 2)
        self.assertEqual(body["status"], "invalid")
        self.assertEqual(body["findings"][0]["code"], "security.secret_detected")
        self.assertIn("appears to contain a secret", body["findings"][0]["message"])


if __name__ == "__main__":
    unittest.main()
