from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = PACKAGE_ROOT / "schemas"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "schema"
RUNTIME_SCRIPTS = PACKAGE_ROOT / "scripts"
if str(RUNTIME_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SCRIPTS))

from agentjob_runtime.validation.cross_record import canonical_sha256  # noqa: E402


TS = "2026-07-17T15:00:00Z"
HASH_A = "a" * 64
HASH_B = "b" * 64


def fixture_cases(group: str) -> list[dict[str, Any]]:
    return json.loads((FIXTURE_ROOT / group / "cases.json").read_text(encoding="utf-8"))


def valid_task() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.task.v1",
        "task_id": "TASK-20260717-001",
        "objective": "Make one bounded change.",
        "status": "active",
        "parent_task_id": None,
        "source_task_ref": None,
        "current_decision_id": "DDR-20260717-001",
        "current_job_id": "AJ-TASK-20260717-001-001",
        "requires_human_gate": False,
        "human_gate_refs": [],
        "created_at": TS,
        "updated_at": TS,
        "revision": 1,
        "closure": {
            "status": "open",
            "summary": None,
            "completion_refs": [],
            "no_execution_reason": None,
        },
        "next_recommended_action": "Execute the active job.",
        "extensions": {},
    }


def valid_decision() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.director-decision.v1",
        "decision_id": "DDR-20260717-001",
        "task_id": "TASK-20260717-001",
        "decision_authority": {
            "kind": "system_director",
            "actor_ref": "thread:test",
            "policy_refs": [".agents/control/policies/default.yaml"],
        },
        "decision_type": "create_job",
        "decision_mode": "deliberative",
        "status": "activated",
        "evidence": {
            "state_snapshot_ref": ".agents/control/snapshots/before.json",
            "state_snapshot_sha256": HASH_A,
            "handoff_refs": [],
            "source_refs": ["src/example.py"],
        },
        "candidates": [
            {
                "route_id": "bounded-change",
                "role_id": "software-engineer",
                "assessment": "accepted",
                "reason": "The role fits the bounded change.",
            },
            {
                "route_id": "broad-redesign",
                "role_id": "system-architect",
                "assessment": "rejected",
                "reason": "Evidence does not justify a redesign.",
            },
        ],
        "selected": {
            "route_id": "bounded-change",
            "role_id": "software-engineer",
            "role_version": "1.0.0",
            "agent_job_id": "AJ-TASK-20260717-001-001",
            "rationale": "The route is legal and minimal.",
        },
        "rejected_alternatives": ["Broad redesign exceeds the evidence."],
        "requires_human_gate": False,
        "human_gate_refs": [],
        "claim_boundary": {
            "allowed": ["The bounded fixture passes."],
            "forbidden": ["The entire target system is proven correct."],
        },
        "supersedes_decision_id": None,
        "rule_id": None,
        "rejected_illegal_routes": [],
        "created_at": TS,
        "activated_at": TS,
        "completed_at": None,
        "extensions": {},
    }


def valid_job() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.agent-job.v1",
        "job_id": "AJ-TASK-20260717-001-001",
        "task_id": "TASK-20260717-001",
        "decision_id": "DDR-20260717-001",
        "status": "active",
        "activated_at": TS,
        "objective": "Make one bounded change.",
        "role_binding": {
            "role_id": "software-engineer",
            "role_version": "1.0.0",
            "execution_role_ref": ".agents/control/tasks/TASK-20260717-001/execution-role.yaml",
        },
        "authority": {
            "allowed_read_paths": ["src/example.py", "tests/test_example.py"],
            "allowed_write_paths": ["src/example.py"],
            "allowed_generated_paths": [".local/results/example.json"],
            "forbidden_paths": [".agents/control/policies/private.yaml"],
            "allowed_actions": ["read_files", "edit_files", "run_local_commands"],
            "forbidden_actions": ["publish", "push", "merge", "access_secrets"],
            "network_access": False,
            "external_effects": [],
        },
        "source_policy": {
            "allowed_source_classes": ["controlled_source", "project_test"],
            "forbidden_source_classes": ["unverified_external_claim"],
        },
        "commands": {
            "approved": [
                {
                    "command_id": "focused-tests",
                    "argv": ["python3", "-m", "unittest", "tests.test_example"],
                    "cwd": "src",
                    "environment": {},
                    "network": False,
                    "shell": False,
                    "shell_policy_approval_ref": None,
                    "timeout_seconds": 60,
                }
            ]
        },
        "validators": {
            "required": [
                {
                    "validator_id": "changed-path-allowlist",
                    "validator_class": "path_validation",
                    "mode": "required",
                }
            ],
            "contextual": [],
        },
        "expected_outputs": [
            {"path": "src/example.py", "kind": "controlled_source_change"}
        ],
        "completion_contract": {
            "required_evidence": ["The focused fixture passes."],
            "goal_effect": {
                "type": "bounded_progress",
                "does_not_imply_global_goal_completion": True,
            },
        },
        "stop_conditions": ["authority_ambiguity", "validator_failure"],
        "checkpoint": {"provider": "git_status", "required": True, "auto_commit": False},
        "claim_boundary": {
            "allowed": ["The bounded fixture passes."],
            "forbidden": ["The entire target system is proven correct."],
        },
        "concurrency": {
            "policy": "exclusive_worktree",
            "lease_scope": "repository_worktree",
            "idempotency_key": "AJ-TASK-20260717-001-001",
        },
        "extensions": {},
    }


def valid_role() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.execution-role.v1",
        "execution_role_id": "ER-AJ-TASK-20260717-001-001",
        "job_id": "AJ-TASK-20260717-001-001",
        "task_id": "TASK-20260717-001",
        "binding_type": "registered_role",
        "role_id": "software-engineer",
        "role_version": "1.0.0",
        "responsibilities": ["Implement the bounded change."],
        "may_not": ["Broaden the job authority."],
        "source_role_ref": ".agents/control/roles/software-engineer.yaml",
        "task_overlay": None,
        "authority_delta": "No permission expansion.",
        "provisional_role": None,
        "requires_human_gate": False,
        "human_gate_refs": [],
        "expires_after": "AJ-TASK-20260717-001-001",
        "activated_at": TS,
        "extensions": {},
    }


def valid_completion() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.completion.v1",
        "completion_id": "AJC-AJ-TASK-20260717-001-001",
        "job_id": "AJ-TASK-20260717-001-001",
        "task_id": "TASK-20260717-001",
        "decision_id": "DDR-20260717-001",
        "started_at": TS,
        "completed_at": "2026-07-17T15:01:00Z",
        "status": "completed",
        "before": {"repository_fingerprint": HASH_A, "revision": "before"},
        "after": {"repository_fingerprint": HASH_B, "revision": "after"},
        "changed_paths": ["src/example.py"],
        "outputs": [
            {"path": "src/example.py", "kind": "controlled_source_change", "sha256": HASH_B}
        ],
        "command_results": [
            {"command_id": "focused-tests", "exit_code": 0, "status": "pass", "evidence_ref": None}
        ],
        "validator_results": [
            {
                "validator_id": "changed-path-allowlist",
                "validator_class": "path_validation",
                "status": "pass",
                "reason_code": None,
                "evidence_ref": None,
                "notes": [],
            }
        ],
        "verdict": "completed_within_claim_boundary",
        "uncertainty": {"status": "none_observed", "notes": []},
        "claim_summary": {
            "allowed_conclusions": ["The bounded fixture passes."],
            "forbidden_overread": ["This does not prove the entire target system correct."],
            "inherited_boundary_ref": "AJ-TASK-20260717-001-001",
        },
        "next_recommended_action": "Reevaluate the containing goal.",
        "extensions": {},
    }


def valid_handoff() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.handoff.v1",
        "handoff_id": "HANDOFF-20260717-001",
        "predecessor": {
            "task_id": "TASK-20260717-001",
            "decision_id": "DDR-20260717-001",
            "job_id": "AJ-TASK-20260717-001-001",
            "completion_id": "AJC-AJ-TASK-20260717-001-001",
        },
        "predecessor_handoff_ids": [],
        "summary": "The bounded change completed.",
        "progress": {"completed": ["Made the bounded change."], "remaining": ["Evaluate the next step."]},
        "next_action": {
            "objective": "Evaluate the next legal step.",
            "recommended_role": "system-director",
            "route_label": "goal-evaluation",
        },
        "constraints_to_preserve": ["A new job is required before execution."],
        "human_gates": [],
        "grants_execution_authority": False,
        "created_at": TS,
        "extensions": {},
    }


def valid_activation(decision: dict[str, Any], job: dict[str, Any], role: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.activation.v1",
        "activation_id": "ACT-20260717-001",
        "packet_type": "director_job_packet",
        "records": [
            {"order": 1, "path": decision["_path"], "record_id": decision["decision_id"], "record_type": "director_decision", "sha256": canonical_sha256({k: v for k, v in decision.items() if not k.startswith("_")})},
            {"order": 2, "path": job["_path"], "record_id": job["job_id"], "record_type": "agent_job", "sha256": canonical_sha256({k: v for k, v in job.items() if not k.startswith("_")})},
            {"order": 3, "path": role["_path"], "record_id": role["execution_role_id"], "record_type": "execution_role", "sha256": canonical_sha256({k: v for k, v in role.items() if not k.startswith("_")})},
        ],
        "activated_at": TS,
        "activation_revision": 1,
        "prior_control_revision": 0,
        "extensions": {},
    }


def valid_record_set() -> dict[str, list[dict[str, Any]]]:
    task = valid_task()
    decision = valid_decision()
    job = valid_job()
    role = valid_role()
    completion = valid_completion()
    handoff = valid_handoff()
    decision["_path"] = ".agents/control/tasks/TASK-20260717-001/decision.yaml"
    job["_path"] = ".agents/control/tasks/TASK-20260717-001/agent-job.yaml"
    role["_path"] = ".agents/control/tasks/TASK-20260717-001/execution-role.yaml"
    completion["_path"] = ".agents/control/tasks/TASK-20260717-001/completion.yaml"
    handoff["_path"] = ".agents/control/handoffs/HANDOFF-20260717-001.yaml"
    activation = valid_activation(decision, job, role)
    return {
        "tasks": [task],
        "decisions": [decision],
        "jobs": [job],
        "roles": [role],
        "completions": [completion],
        "handoffs": [handoff],
        "activations": [activation],
        "supersessions": [],
        "goal_receipts": [],
    }


def valid_goal() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.continue-goal.v1",
        "goal_id": "CG-20260717T150000Z-a1b2c3d4",
        "goal_text": "Complete the bounded fixture.",
        "goal_sha256": HASH_A,
        "completion_contract": {
            "interpretation": "Complete the fixture with passing evidence.",
            "required_evidence": ["The required fixture passes."],
            "user_confirmed_when_ambiguous": False,
        },
        "completion_contract_sha256": HASH_B,
        "amendments": [],
        "created_at": TS,
        "deadline_at": "2099-01-01T00:00:00Z",
        "guards": {
            "max_continue_passes": 12,
            "max_repeated_state_fingerprints": 1,
            "max_live_continuations": 1,
            "handoff_ready_timeout_seconds": 60,
            "stop_on_human_gate": True,
            "stop_on_validation_failure": True,
            "stop_on_checkpoint_failure": True,
            "stop_on_unexpected_dirty_state": True,
            "stop_on_no_progress": True,
            "stop_on_repeated_state": True,
            "stop_on_capability_loss": True,
            "stop_on_repository_mismatch": True,
        },
        "repository_binding": {
            "project_id": "neutral-fixture",
            "root": "/tmp/neutral-fixture",
            "worktree": "/tmp/neutral-fixture",
            "branch": "feature/fixture",
            "git_common_dir": "/tmp/neutral-fixture/.git",
            "starting_revision": "abc123",
            "environment_mode": "local",
        },
        "authorization": {"fresh_recursive_threads_explicitly_requested": True},
        "state": {
            "revision": 1,
            "phase": "initialized",
            "current_generation": 0,
            "passes_consumed": 0,
            "active_lease": None,
            "goal_evaluation": "unmet",
            "last_canonical_fingerprint": HASH_A,
            "canonical_fingerprint_history": [HASH_A],
            "terminal_reason": None,
        },
        "generations": {},
        "handoff": {
            "status": "none",
            "generation": 1,
            "token": None,
            "idempotency_key": None,
            "predecessor_thread_id": None,
            "successor_thread_id": None,
        },
        "journal": [],
        "updated_at": TS,
        "extensions": {},
    }


def valid_goal_receipt() -> dict[str, Any]:
    goal = valid_goal()
    return {
        "schema_version": "sys4ai.goal-step-receipt.v1",
        "receipt_id": "RECEIPT-CG-1",
        "goal_id": goal["goal_id"],
        "generation": 1,
        "handoff_token_hash": HASH_A,
        "idempotency_key": f"{goal['goal_id']}:1",
        "predecessor_thread_id": "thread-1",
        "successor_thread_id": None,
        "started_at": TS,
        "finished_at": "2026-07-17T15:01:00Z",
        "repository_binding": goal["repository_binding"],
        "revision_before": "abc123",
        "revision_after": "abc123",
        "fingerprint_before": HASH_A,
        "fingerprint_after": HASH_A,
        "continue_invocation_count": 0,
        "agent_job_id": None,
        "zero_job_reason": "A human gate is required.",
        "task_id": None,
        "handoff_id": None,
        "checkpoint": {
            "provider": "git-status",
            "status": "not_required",
            "revision": "abc123",
            "evidence_ref": None,
        },
        "validator_results": [],
        "goal_evaluation": "indeterminate",
        "progress_summary": "No execution occurred.",
        "remaining_work": "Obtain the protected approval.",
        "decision": "protected_stop",
        "journal_entry_hash": HASH_B,
        "prior_journal_hash": None,
        "finalized": True,
        "extensions": {},
    }


def valid_continuation_envelope() -> dict[str, Any]:
    goal = valid_goal()
    return {
        "schema_version": "sys4ai.continuation-envelope.v1",
        "goal_id": goal["goal_id"],
        "goal_sha256": goal["goal_sha256"],
        "completion_contract_sha256": goal["completion_contract_sha256"],
        "generation": 1,
        "handoff_token": "t" * 32,
        "idempotency_key": f"{goal['goal_id']}:1",
        "predecessor_thread_id": None,
        "predecessor_handoff_id": None,
        "repository_binding": goal["repository_binding"],
        "canonical_state": {
            "fingerprint": HASH_A,
            "active_task_id": None,
            "current_decision_id": None,
            "current_job_id": None,
        },
        "progress_summary": "The relay was initialized.",
        "remaining_work": "Execute one legal generation.",
        "required_skill": "continue-implementing-goal",
        "extensions": {},
    }


def valid_continue_result() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.continue-result.v1",
        "status": "no_action",
        "boundary_entered": "no_action",
        "agent_jobs_executed": 0,
        "task_id": None,
        "decision_id": None,
        "job_id": None,
        "completion_id": None,
        "handoff_id": None,
        "progress_effect": "none",
        "global_goal_evaluation": "not_evaluated_here",
        "repository_fingerprint_before": HASH_A,
        "repository_fingerprint_after": HASH_A,
        "validators": {"required": 1, "passed": 1, "failed": 0, "warning": 0, "skipped": 0},
        "next_recommended_action": None,
        "execution_performed": False,
        "reason_code": "no-action",
        "extensions": {},
    }


def valid_supersession() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.supersession.v1",
        "supersession_id": "SUPER-20260717-001",
        "old_decision_id": "DDR-20260717-001",
        "old_job_id": "AJ-TASK-20260717-001-001",
        "reason": "A newer bounded packet replaces stale authority.",
        "evidence_refs": [".agents/control/snapshots/newer.json"],
        "prior_execution_status": "unexecuted",
        "working_evidence_handling": "Preserve as non-authoritative historical evidence.",
        "replacement_decision_id": "DDR-20260717-002",
        "replacement_job_id": "AJ-TASK-20260717-001-002",
        "replacement_activation_id": "ACT-20260717-002",
        "claim_boundary_preserved": True,
        "created_at": TS,
        "extensions": {},
    }


def valid_policy() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.policy-pack.v1",
        "policy_id": "generic-software",
        "version": "1.0.0",
        "protocol_range": "^1.0.0",
        "namespace_owner": "sys4ai",
        "roles": ["software-engineer", "validator-engineer"],
        "protected_actions": ["public-release", "secret-access"],
        "human_gate_rules": [{"action": "public-release", "required": True}],
        "source_classes": ["controlled-source", "generated-derivative"],
        "validator_defaults": ["schema-validation", "path-allowlist"],
        "claim_rules": {"process_validation_does_not_imply_domain_truth": True},
        "extension_schemas": {},
        "extensions": {},
    }


def valid_adapter() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.project-adapter.v1",
        "adapter_id": "filesystem",
        "version": "1.0.0",
        "protocol_range": "^1.0.0",
        "profile": "portable_registered",
        "capabilities": ["task-records", "agentjob-records", "handoffs"],
        "canonical_source_roots": [".agents/control"],
        "record_mappings": {
            "task": "task.yaml",
            "director_decision": "decision.yaml",
            "agent_job": "agent-job.yaml",
            "execution_role": "execution-role.yaml",
            "completion": "completion.yaml",
            "handoff": "handoff.yaml",
        },
        "role_mappings": {"software-engineer": "software-engineer"},
        "validators": ["control-record-validator"],
        "checkpoint_provider": "git-status",
        "extension_schema_refs": [],
        "unsupported_features": [],
        "extensions": {},
    }


def valid_config() -> dict[str, Any]:
    return {
        "schema_version": "sys4ai.continuation-config.v1",
        "project": {"id": "neutral-fixture", "root": "project", "control_namespace": "default"},
        "runtime": {"harness": "codex", "surfaces": ["cli"]},
        "control": {
            "profile": "portable_registered",
            "root": ".agents/control",
            "adapter": "filesystem",
            "one_agentjob_per_continue": True,
            "immutable_after_activation": True,
            "supersession_required": True,
        },
        "goal_relay": {
            "state_backend": "sqlite",
            "local_root": ".local/sys4ai/continuation",
            "thread_provider": "manual-handoff",
            "thread_strategy": "fresh_summary",
            "native_goal_mirror": False,
            "at_most_once_consumption": True,
            "max_live_continuations": 1,
        },
        "repository": {
            "provider": "git",
            "default_branch_policy": "warn",
            "dirty_state_policy": "job_specific",
            "fingerprint_provider": "canonical-git-control",
        },
        "roles": {
            "catalog": [".agents/control/roles"],
            "allow_task_overlays": True,
            "allow_one_job_provisional_roles": True,
        },
        "policy": {"packs": [".agents/control/policies/default.yaml"], "strict_extensions": True},
        "validation": {
            "pre_execution": ["control-record-validator"],
            "post_write": ["changed-path-allowlist"],
        },
        "checkpoint": {"provider": "git_status", "auto_commit": False},
        "security": {
            "default_network_access": False,
            "reject_goal_secrets": True,
            "reject_symlink_state_paths": True,
            "reject_hardlink_aliases": True,
            "allow_environment_fields": [],
        },
        "human_gates": {"protected_actions": ["public-release", "secret-access"]},
    }


def cloned(value: Any) -> Any:
    return copy.deepcopy(value)
