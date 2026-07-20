"""Deterministic plan completion evidence with profile history."""

from __future__ import annotations

from typing import Any

from agentjob_runtime.plan.sqlite_store import SQLitePlanStore
from agentjob_runtime.records.canonical import content_sha256


def build_plan_completion_report(
    store: SQLitePlanStore,
    *,
    plan_id: str,
) -> dict[str, Any]:
    """Project accepted profiles and per-generation provider evidence."""

    record = store.load_plan(plan_id)
    activations = store.list_activation_receipts(plan_id)
    intents = store.list_provider_intents(plan_id)
    receipts = store.list_receipts(plan_id)
    generations = [
        {
            "generation": intent["generation"],
            "task_id": intent["task_id"],
            "provider_id": intent["provider_id"],
            "thread_id": intent["returned_thread_id"],
            "requested_reasoning_effort": intent.get(
                "requested_reasoning_effort"
            ),
            "effective_reasoning_effort": intent.get(
                "effective_reasoning_effort"
            ),
            "profile_verification_status": intent.get(
                "profile_verification_status",
                "historical_profile_not_recorded",
            ),
            "profile_evidence_ref": intent.get("profile_evidence_ref"),
            "repository_binding_sha256": intent.get(
                "repository_binding_sha256"
            ),
        }
        for intent in intents
    ]
    accepted_profiles = [
        {
            "activation_id": receipt["activation_id"],
            "activation_receipt_sha256": content_sha256(receipt),
            "reasoning_effort": receipt["reasoning_effort"],
            "effective_from_generation": receipt[
                "effective_from_generation"
            ],
            "superseded_activation_id": receipt[
                "superseded_activation_id"
            ],
        }
        for receipt in activations
    ]
    tasks_complete = all(
        task["status"] in {"completed", "superseded"}
        for task in record["state"]["tasks"]
    )
    profile_conformant = all(
        item["requested_reasoning_effort"]
        == item["effective_reasoning_effort"]
        and item["profile_verification_status"] == "verified"
        for item in generations
    )
    topology_conformant = all(
        receipt.get("schema_version") != "sys4ai.plan-task-receipt.v2"
        or (
            receipt["topology_evidence"]["unapproved_change_detected"]
            is False
            and receipt["topology_evidence"][
                "repository_binding_sha256"
            ]
            == record["repository_binding_sha256"]
        )
        for receipt in receipts
    )
    report: dict[str, Any] = {
        "schema_version": "sys4ai.plan-completion-report.v1",
        "plan_id": record["plan_id"],
        "plan_sha256": record["effective_plan_sha256"],
        "status": (
            "complete"
            if tasks_complete
            and profile_conformant
            and topology_conformant
            else "incomplete"
        ),
        "accepted_profiles": accepted_profiles,
        "generation_profile_evidence": generations,
        "task_receipt_sha256s": [
            content_sha256(receipt) for receipt in receipts
        ],
        "profile_conformant": profile_conformant,
        "topology_conformant": topology_conformant,
        "tasks_complete": tasks_complete,
        "report_content_sha256": "",
    }
    report["report_content_sha256"] = content_sha256(
        {
            key: value
            for key, value in report.items()
            if key != "report_content_sha256"
        }
    )
    return report
