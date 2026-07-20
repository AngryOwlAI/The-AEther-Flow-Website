"""Supersede future packet authority without rewriting prior evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from agentjob_runtime.control.activation import ActivationReceipt, activate_packet
from agentjob_runtime.control.filesystem_store import FilesystemControlStore
from agentjob_runtime.errors import IntegrityError, RecordValidationError
from agentjob_runtime.records.canonical import content_sha256


@dataclass(frozen=True)
class SupersessionReceipt:
    supersession_id: str
    old_decision_id: str
    old_job_id: str
    replacement_decision_id: str
    replacement_job_id: str
    prior_hashes: Mapping[str, str]
    replacement_activation: ActivationReceipt

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "superseded",
            "supersession_id": self.supersession_id,
            "old_decision_id": self.old_decision_id,
            "old_job_id": self.old_job_id,
            "replacement_decision_id": self.replacement_decision_id,
            "replacement_job_id": self.replacement_job_id,
            "prior_hashes": dict(self.prior_hashes),
            "replacement_activation": self.replacement_activation.as_dict(),
        }


def supersede_packet(
    store: FilesystemControlStore,
    *,
    task_id: str,
    old_decision_id: str,
    old_job_id: str,
    replacement_decision: Mapping[str, Any],
    replacement_job: Mapping[str, Any],
    replacement_role: Mapping[str, Any],
    reason: str,
    evidence_refs: Sequence[str],
    prior_execution_status: str,
    working_evidence_handling: str,
    expected_revision: int,
    created_at: str,
    policies: Sequence[Mapping[str, Any]] = (),
    fault_after: str | None = None,
) -> SupersessionReceipt:
    if not reason.strip() or not evidence_refs or not working_evidence_handling.strip():
        raise RecordValidationError("supersession requires reason, evidence, and evidence handling")
    old_decision_path = store.record_path("director_decision", task_id, old_decision_id)
    old_job_path = store.record_path("agent_job", task_id, old_job_id)
    old_decision = store.read(old_decision_path)
    old_job = store.read(old_job_path)
    activated = store.activated_record_ids()
    if old_decision_id not in activated or old_job_id not in activated:
        raise IntegrityError(
            "the prior packet is not activated",
            details={"reason_code": "supersession.prior_not_activated"},
        )
    before_hashes = {
        old_decision_id: content_sha256(old_decision),
        old_job_id: content_sha256(old_job),
    }

    if replacement_decision.get("decision_type") != "supersede_job":
        raise RecordValidationError("replacement decision_type must be supersede_job")
    if replacement_decision.get("supersedes_decision_id") != old_decision_id:
        raise RecordValidationError("replacement decision must reference the prior decision")
    if replacement_job.get("job_id") == old_job_id:
        raise RecordValidationError("replacement AgentJob must use a new ID")

    supersession_id = f"SUPER-{replacement_job['job_id']}"
    activation_id = f"ACT-{replacement_job['job_id']}"
    packet = {
        "schema_version": "sys4ai.supersession.v1",
        "supersession_id": supersession_id,
        "old_decision_id": old_decision_id,
        "old_job_id": old_job_id,
        "reason": reason,
        "evidence_refs": list(evidence_refs),
        "prior_execution_status": prior_execution_status,
        "working_evidence_handling": working_evidence_handling,
        "replacement_decision_id": replacement_decision["decision_id"],
        "replacement_job_id": replacement_job["job_id"],
        "replacement_activation_id": activation_id,
        "claim_boundary_preserved": True,
        "created_at": created_at,
        "extensions": {},
    }
    store.validate_record("supersession", packet)
    activation = activate_packet(
        store,
        task_id=task_id,
        decision=replacement_decision,
        job=replacement_job,
        execution_role=replacement_role,
        expected_revision=expected_revision,
        activation_id=activation_id,
        packet_type="supersession_packet",
        additional_records=[("supersession", packet)],
        policies=policies,
        fault_after=fault_after,
    )
    after_hashes = {
        old_decision_id: content_sha256(store.read(old_decision_path)),
        old_job_id: content_sha256(store.read(old_job_path)),
    }
    if before_hashes != after_hashes:
        raise IntegrityError(
            "prior packet bytes changed during supersession",
            details={"reason_code": "supersession.prior_mutated"},
        )
    return SupersessionReceipt(
        supersession_id,
        old_decision_id,
        old_job_id,
        str(replacement_decision["decision_id"]),
        str(replacement_job["job_id"]),
        before_hashes,
        activation,
    )
