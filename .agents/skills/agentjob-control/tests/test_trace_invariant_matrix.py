from __future__ import annotations

import copy
import unittest

from _support import valid_goal_receipt, valid_policy, valid_record_set, valid_supersession
from agentjob_runtime.validation.cross_record import validate_record_set


ALL_INVARIANT_CODES = {
    "activation.active_job_missing",
    "activation.hash_mismatch",
    "activation.order_invalid",
    "activation.path_missing",
    "activation.record_id_conflict",
    "activation.record_reactivated",
    "completion.changed_path_forbidden",
    "completion.claim_broadened",
    "completion.command_undeclared",
    "completion.duplicate_for_job",
    "completion.job_missing",
    "completion.output_undeclared",
    "completion.trace_conflict",
    "completion.validator_failed_but_completed",
    "completion.validator_missing",
    "extension.namespace_undeclared",
    "extension.version_mismatch",
    "goal_receipt.duplicate_generation",
    "goal_receipt.duplicate_idempotency_key",
    "handoff.authority_grant_forbidden",
    "handoff.chain_missing",
    "handoff.predecessor_completion_missing",
    "handoff.predecessor_decision_missing",
    "handoff.predecessor_job_missing",
    "handoff.predecessor_task_missing",
    "record.duplicate_id",
    "record.missing_id",
    "supersession.cycle",
    "supersession.duplicate_old_job",
    "supersession.new_decision_missing",
    "supersession.new_job_missing",
    "supersession.old_decision_missing",
    "supersession.old_job_missing",
    "supersession.self_cycle",
    "trace.decision_job_missing",
    "trace.decision_task_missing",
    "trace.job_decision_conflict",
    "trace.job_decision_missing",
    "trace.job_role_cardinality",
    "trace.job_role_identity_conflict",
    "trace.job_task_missing",
    "trace.role_job_missing",
    "trace.role_task_conflict",
    "trace.task_decision_missing",
    "trace.task_job_missing",
}


def _codes(records, *, policies=(), strict_extensions=True):
    return {
        issue.code
        for issue in validate_record_set(
            records, policies=policies, strict_extensions=strict_extensions
        )
    }


def _add_replacement(records):
    decision = copy.deepcopy(records["decisions"][0])
    decision["decision_id"] = "DDR-20260717-002"
    decision["selected"]["agent_job_id"] = "AJ-TASK-20260717-001-002"
    decision["_path"] = ".agents/control/tasks/TASK-20260717-001/decision-2.yaml"
    job = copy.deepcopy(records["jobs"][0])
    job["job_id"] = "AJ-TASK-20260717-001-002"
    job["decision_id"] = decision["decision_id"]
    job["status"] = "superseded"
    job["_path"] = ".agents/control/tasks/TASK-20260717-001/job-2.yaml"
    role = copy.deepcopy(records["roles"][0])
    role["execution_role_id"] = "ER-AJ-TASK-20260717-001-002"
    role["job_id"] = job["job_id"]
    role["_path"] = ".agents/control/tasks/TASK-20260717-001/role-2.yaml"
    records["decisions"].append(decision)
    records["jobs"].append(job)
    records["roles"].append(role)


class TraceInvariantMatrixTests(unittest.TestCase):
    def test_valid_chain_is_the_positive_control(self) -> None:
        self.assertEqual(validate_record_set(valid_record_set()), [])

    def test_every_cross_record_invariant_has_a_negative_fixture(self) -> None:
        covered: set[str] = set()

        def run(name, mutate, expected, *, policies=(), strict_extensions=True):
            records = valid_record_set()
            mutate(records)
            found = _codes(
                records,
                policies=policies,
                strict_extensions=strict_extensions,
            )
            with self.subTest(name=name):
                self.assertTrue(set(expected) <= found, (expected, sorted(found)))
            covered.update(expected)

        run(
            "missing task pointers",
            lambda r: r["tasks"][0].update(
                current_decision_id="DDR-MISSING", current_job_id="AJ-MISSING"
            ),
            {"trace.task_decision_missing", "trace.task_job_missing"},
        )
        run(
            "decision orphans",
            lambda r: r["decisions"][0].update(
                task_id="TASK-MISSING",
                selected={**r["decisions"][0]["selected"], "agent_job_id": "AJ-MISSING"},
            ),
            {"trace.decision_task_missing", "trace.decision_job_missing"},
        )
        run(
            "job decision conflict and orphan",
            lambda r: r["jobs"][0].update(decision_id="DDR-MISSING"),
            {"trace.job_decision_conflict", "trace.job_decision_missing"},
        )
        run(
            "job task orphan",
            lambda r: r["jobs"][0].update(task_id="TASK-MISSING"),
            {"trace.job_task_missing"},
        )
        run(
            "role job orphan",
            lambda r: r["roles"][0].update(job_id="AJ-MISSING"),
            {"trace.role_job_missing", "trace.job_role_cardinality"},
        )
        run(
            "role task conflict",
            lambda r: r["roles"][0].update(task_id="TASK-MISSING"),
            {"trace.role_task_conflict"},
        )
        run(
            "role identity conflict",
            lambda r: r["roles"][0].update(role_id="different-role"),
            {"trace.job_role_identity_conflict"},
        )
        run(
            "missing role identifier",
            lambda r: r["roles"][0].pop("execution_role_id"),
            {"record.missing_id", "trace.job_role_cardinality"},
        )
        run(
            "duplicate role identifier",
            lambda r: r["roles"].append(copy.deepcopy(r["roles"][0])),
            {"record.duplicate_id"},
        )

        run(
            "active job lacks activation",
            lambda r: r.update(activations=[]),
            {"activation.active_job_missing"},
        )
        run(
            "activation path missing",
            lambda r: r["activations"][0]["records"][0].update(path="missing.json"),
            {"activation.path_missing"},
        )
        run(
            "activation record id conflict",
            lambda r: r["activations"][0]["records"][0].update(record_id="DDR-OTHER"),
            {"activation.record_id_conflict"},
        )
        run(
            "activation hash mismatch",
            lambda r: r["activations"][0]["records"][0].update(sha256="0" * 64),
            {"activation.hash_mismatch"},
        )
        run(
            "activation order invalid",
            lambda r: r["activations"][0]["records"][0].update(order=2),
            {"activation.order_invalid"},
        )

        def duplicate_activation(records):
            duplicate = copy.deepcopy(records["activations"][0])
            duplicate["activation_id"] = "ACT-20260717-002"
            records["activations"].append(duplicate)

        run(
            "record reactivated",
            duplicate_activation,
            {"activation.record_reactivated"},
        )

        def missing_supersession_targets(records):
            packet = valid_supersession()
            packet["old_decision_id"] = "DDR-OLD-MISSING"
            packet["old_job_id"] = "AJ-OLD-MISSING"
            records["supersessions"] = [packet]

        run(
            "supersession missing records",
            missing_supersession_targets,
            {
                "supersession.old_job_missing",
                "supersession.new_job_missing",
                "supersession.old_decision_missing",
                "supersession.new_decision_missing",
            },
        )

        def self_cycle(records):
            packet = valid_supersession()
            packet["replacement_job_id"] = packet["old_job_id"]
            records["supersessions"] = [packet]

        run("supersession self cycle", self_cycle, {"supersession.self_cycle"})

        def duplicate_old(records):
            _add_replacement(records)
            first = valid_supersession()
            second = copy.deepcopy(first)
            second["supersession_id"] = "SUPER-20260717-002"
            records["supersessions"] = [first, second]

        run(
            "duplicate superseded job",
            duplicate_old,
            {"supersession.duplicate_old_job"},
        )

        def cycle(records):
            _add_replacement(records)
            first = valid_supersession()
            second = copy.deepcopy(first)
            second.update(
                supersession_id="SUPER-20260717-002",
                old_decision_id=first["replacement_decision_id"],
                old_job_id=first["replacement_job_id"],
                replacement_decision_id=first["old_decision_id"],
                replacement_job_id=first["old_job_id"],
            )
            records["supersessions"] = [first, second]

        run("supersession cycle", cycle, {"supersession.cycle"})

        run(
            "completion job missing",
            lambda r: r["completions"][0].update(job_id="AJ-MISSING"),
            {"completion.job_missing"},
        )
        run(
            "completion trace conflict",
            lambda r: r["completions"][0].update(task_id="TASK-MISSING"),
            {"completion.trace_conflict"},
        )
        run(
            "completion path forbidden",
            lambda r: r["completions"][0]["changed_paths"].append("private/secret.txt"),
            {"completion.changed_path_forbidden"},
        )
        run(
            "completion output undeclared",
            lambda r: r["completions"][0]["outputs"].append(
                {"path": "other.txt", "kind": "generated_derivative", "sha256": "0" * 64}
            ),
            {"completion.output_undeclared"},
        )
        run(
            "completion command undeclared",
            lambda r: r["completions"][0]["command_results"].append(
                {"command_id": "other", "exit_code": 0, "status": "pass", "evidence_ref": None}
            ),
            {"completion.command_undeclared"},
        )
        run(
            "completion validator missing",
            lambda r: r["completions"][0].update(validator_results=[]),
            {"completion.validator_missing"},
        )
        run(
            "completion validator failed but completed",
            lambda r: r["completions"][0]["validator_results"][0].update(status="fail"),
            {"completion.validator_failed_but_completed"},
        )
        run(
            "completion claim broadened",
            lambda r: r["completions"][0]["claim_summary"]["allowed_conclusions"].append(
                "Everything is correct."
            ),
            {"completion.claim_broadened"},
        )

        def duplicate_completion(records):
            duplicate = copy.deepcopy(records["completions"][0])
            duplicate["completion_id"] = "AJC-AJ-TASK-20260717-001-002"
            records["completions"].append(duplicate)

        run(
            "duplicate completion",
            duplicate_completion,
            {"completion.duplicate_for_job"},
        )

        def missing_handoff_chain(records):
            predecessor = records["handoffs"][0]["predecessor"]
            predecessor.update(
                task_id="TASK-MISSING",
                decision_id="DDR-MISSING",
                job_id="AJ-MISSING",
                completion_id="AJC-MISSING",
            )
            records["handoffs"][0]["predecessor_handoff_ids"] = ["HANDOFF-MISSING"]
            records["handoffs"][0]["grants_execution_authority"] = True

        run(
            "handoff orphan and authority grant",
            missing_handoff_chain,
            {
                "handoff.predecessor_task_missing",
                "handoff.predecessor_decision_missing",
                "handoff.predecessor_job_missing",
                "handoff.predecessor_completion_missing",
                "handoff.chain_missing",
                "handoff.authority_grant_forbidden",
            },
        )

        def duplicate_receipts(records):
            first = valid_goal_receipt()
            second = copy.deepcopy(first)
            second["receipt_id"] = "RECEIPT-CG-2"
            records["goal_receipts"] = [first, second]

        run(
            "duplicate goal receipt identity",
            duplicate_receipts,
            {
                "goal_receipt.duplicate_generation",
                "goal_receipt.duplicate_idempotency_key",
            },
        )
        run(
            "undeclared extension",
            lambda r: r["tasks"][0].update(
                extensions={"demo": {"version": "1.0.0", "required": True, "data": {}}}
            ),
            {"extension.namespace_undeclared"},
        )
        policy = valid_policy()
        policy["extension_schemas"] = {
            "demo": {"version": "1.0.0", "schema_ref": "schemas/demo.schema.json"}
        }
        run(
            "extension version mismatch",
            lambda r: r["tasks"][0].update(
                extensions={"demo": {"version": "2.0.0", "required": True, "data": {}}}
            ),
            {"extension.version_mismatch"},
            policies=(policy,),
        )

        self.assertEqual(covered, ALL_INVARIANT_CODES)


if __name__ == "__main__":
    unittest.main()
