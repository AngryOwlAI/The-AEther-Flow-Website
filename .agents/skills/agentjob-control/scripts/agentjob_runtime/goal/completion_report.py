"""Build, validate, persist, and render authoritative goal completion reports."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.goal.model import effective_completion_contract, utc_now
from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.validation.schema import format_issues, validate_instance


def _schema() -> Path:
    return (
        Path(__file__).resolve().parents[3]
        / "schemas"
        / "goal-completion-report.schema.json"
    )


def _step_receipts(record: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        copy.deepcopy(dict(entry["payload"]))
        for entry in record.get("journal", ())
        if entry.get("kind") == "step_receipt"
    ]


def _deduplicate_strings(values: Sequence[Any]) -> list[str]:
    return list(dict.fromkeys(str(item) for item in values if str(item).strip()))


def _extension_values(
    extensions: Sequence[Mapping[str, Any]], key: str
) -> list[Any]:
    values: list[Any] = []
    for extension_set in extensions:
        for extension in extension_set.values():
            if not isinstance(extension, Mapping):
                continue
            data = extension.get("data")
            if not isinstance(data, Mapping):
                continue
            supplied = data.get(key, ())
            if isinstance(supplied, (list, tuple)):
                values.extend(supplied)
    return values


def _validate_completion_report(report: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(report))
    issues = validate_instance(value, _schema())
    if issues:
        raise RecordValidationError(
            "goal completion report failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    expected = content_sha256(
        {key: data for key, data in value.items() if key != "final_report_sha256"}
    )
    if value["final_report_sha256"] != expected:
        raise RecordValidationError("goal completion report hash mismatch")
    if value["goal_reached"] is not True or value["canonical_evaluation"] != "met":
        raise RecordValidationError("completion report requires canonical met evidence")
    return value


def build_completion_report(
    record: Mapping[str, Any],
    *,
    completed_at: str | None = None,
    warnings: Sequence[str] = (),
    uncertainty: Sequence[str] = (),
    forbidden_overread: Sequence[str] = (),
    unverified_optional_matters: Sequence[str] = (),
) -> dict[str, Any]:
    """Derive the report only from canonical goal records and finalized receipts."""

    if record.get("schema_version") != "sys4ai.continue-goal.v3":
        raise StateConflict("authoritative completion reports require goal state v3")
    if record["state"]["goal_evaluation"] != "met":
        raise StateConflict("goal completion report requires canonical met evaluation")
    receipts = _step_receipts(record)
    if not receipts:
        raise StateConflict("goal completion report requires finalized generation receipts")
    criteria = [
        copy.deepcopy(dict(result))
        for receipt in receipts
        for result in receipt.get("completion_contract_results", ())
    ]
    expected_criteria = set(effective_completion_contract(record)["required_evidence"])
    latest_by_criterion: dict[str, dict[str, Any]] = {}
    for item in criteria:
        latest_by_criterion[str(item.get("criterion"))] = item
    if set(latest_by_criterion) != expected_criteria or any(
        item.get("status") != "pass" for item in latest_by_criterion.values()
    ):
        raise StateConflict(
            "completion report criteria do not prove the effective contract is met"
        )
    generation_ledger: list[dict[str, Any]] = []
    for key, generation in sorted(
        record["generations"].items(), key=lambda item: int(item[0])
    ):
        receipt = next(
            (
                item
                for item in receipts
                if int(item.get("generation", -1)) == int(key)
            ),
            None,
        )
        generation_ledger.append(
            {
                "generation": generation["generation"],
                "discussion_id": generation.get("successor_thread_id"),
                "task_id": receipt.get("task_id") if receipt else None,
                "decision_id": receipt.get("decision_id") if receipt else None,
                "agent_job_id": receipt.get("agent_job_id") if receipt else None,
                "completion_id": receipt.get("completion_id") if receipt else None,
                "handoff_id": receipt.get("handoff_id") if receipt else None,
                "continue_invocation_count": receipt.get(
                    "continue_invocation_count"
                )
                if receipt
                else "unknown",
                "repair_strategy_id": generation.get("repair_strategy_id"),
                "requested_reasoning_effort": generation.get(
                    "requested_reasoning_effort"
                ),
                "effective_reasoning_effort": generation.get(
                    "effective_reasoning_effort"
                ),
                "receipt_hash": generation.get("finalized_receipt_hash"),
            }
        )
    changed_paths = _deduplicate_strings(
        [
            path
            for receipt in receipts
            for path in receipt.get("changed_paths", ())
        ]
    )
    outputs = [
        copy.deepcopy(dict(output))
        for receipt in receipts
        for output in receipt.get("output_refs", ())
    ]
    receipt_extensions = [
        copy.deepcopy(dict(receipt.get("extensions") or {}))
        for receipt in receipts
    ]
    validators = [
        copy.deepcopy(dict(result))
        for receipt in receipts
        for result in receipt.get("validator_results", ())
    ]
    checkpoints = [
        copy.deepcopy(dict(receipt["checkpoint"]))
        for receipt in receipts
        if isinstance(receipt.get("checkpoint"), Mapping)
    ]
    runtime = copy.deepcopy(dict(record["runtime_binding"]))
    profile = copy.deepcopy(dict(record["execution_profile"]))
    report: dict[str, Any] = {
        "schema_version": "sys4ai.goal-completion-report.v1",
        "report_id": f"GCR-{record['goal_id']}",
        "goal_id": record["goal_id"],
        "goal_text": record["goal_text"],
        "goal_sha256": record["goal_sha256"],
        "completion_contract": copy.deepcopy(effective_completion_contract(record)),
        "completion_contract_sha256": content_sha256(
            effective_completion_contract(record)
        ),
        "accepted_reasoning_effort": profile["reasoning_effort"],
        "goal_reached": True,
        "canonical_evaluation": "met",
        "terminal_phase": "terminal_complete",
        "completed_at": completed_at or utc_now(),
        "skill_runtime_ledger": {
            "skills": [
                {"skill_id": skill_id, "version": version}
                for skill_id, version in sorted(runtime["skill_versions"].items())
            ],
            "runtime_capabilities": list(runtime["capability_versions"]),
            "source_lock_ref": runtime.get("source_lock_ref"),
            "provider_id": runtime["provider_id"],
            "model_id": profile["model_id"],
        },
        "generation_ledger": generation_ledger,
        "work_performed": {
            "claim_summaries": _deduplicate_strings(
                [receipt.get("progress_summary", "") for receipt in receipts]
            ),
            "changed_paths": changed_paths,
            "changed_path_source_refs": _deduplicate_strings(
                [
                    receipt.get("changed_path_source_ref", "")
                    for receipt in receipts
                ]
            ),
            "outputs": outputs,
            "generated_derivatives": [
                output
                for output in outputs
                if output.get("kind")
                in {"generated_evidence", "generated_derivative"}
            ],
            "external_effects": [
                output
                for output in outputs
                if output.get("kind") == "external_effect"
            ],
        },
        "verification": {
            "completion_criteria": [
                latest_by_criterion[criterion]
                for criterion in effective_completion_contract(record)[
                    "required_evidence"
                ]
            ],
            "validator_results": validators,
            "checkpoints": checkpoints,
            "final_repository": {
                "binding": copy.deepcopy(record["repository_binding"]),
                "fingerprint": record["state"]["last_canonical_fingerprint"],
                "topology_policy": copy.deepcopy(
                    record["repository_topology_policy"]
                ),
            },
            "reasoning_profile_evidence": {
                "reasoning_effort": profile["reasoning_effort"],
                "current_thread_evidence_ref": profile[
                    "current_thread_evidence_ref"
                ],
                "generation_evidence": [
                    {
                        "generation": item["generation"],
                        "requested": item["requested_reasoning_effort"],
                        "effective": item["effective_reasoning_effort"],
                    }
                    for item in generation_ledger
                ],
            },
        },
        "repair_and_recovery": copy.deepcopy(
            list(record.get("resolution_history", ()))
        ),
        "limitations": {
            "warnings": _deduplicate_strings(
                [
                    *warnings,
                    *_extension_values(receipt_extensions, "warnings"),
                ]
            ),
            "uncertainty": _deduplicate_strings(
                [
                    *uncertainty,
                    *_extension_values(receipt_extensions, "uncertainty"),
                ]
            ),
            "forbidden_overread": _deduplicate_strings(
                [
                    *forbidden_overread,
                    *_extension_values(
                        receipt_extensions, "forbidden_overread"
                    ),
                ]
            ),
            "unverified_optional_matters": _deduplicate_strings(
                [
                    *unverified_optional_matters,
                    *_extension_values(
                        receipt_extensions,
                        "unverified_optional_matters",
                    ),
                ]
            ),
        },
        "final_report_sha256": "0" * 64,
        "finalized": True,
    }
    report["final_report_sha256"] = content_sha256(
        {
            key: value
            for key, value in report.items()
            if key != "final_report_sha256"
        }
    )
    return _validate_completion_report(report)


def render_completion_markdown(report: Mapping[str, Any]) -> str:
    value = _validate_completion_report(report)
    work = value["work_performed"]
    verification = value["verification"]
    lines = [
        "Goal reached: YES",
        "",
        "Goal:",
        value["goal_text"],
        "",
        "Result:",
        "The goal was reached.",
        "",
        "Summary:",
    ]
    summaries = work["claim_summaries"]
    lines.extend(f"- {item}" for item in summaries)
    lines.extend(
        [
            f"- Generations: {len(value['generation_ledger'])}",
            f"- Changed paths: {len(work['changed_paths'])}",
            f"- Outputs: {len(work['outputs'])}",
            f"- Completion criteria passed: {len(verification['completion_criteria'])}",
            "",
            "No further continuation is required for this goal.",
            "",
        ]
    )
    return "\n".join(lines)


def render_continuing_summary(
    *,
    successor_thread_id: str,
    next_authorized_work: str,
) -> str:
    return (
        "Goal reached: NO\n"
        "Relay status: CONTINUING\n"
        f"Successor discussion: {successor_thread_id}\n"
        f"Next authorized work: {next_authorized_work}\n"
    )


def render_human_summary(report: Mapping[str, Any]) -> str:
    issues = validate_instance(report, Path(__file__).resolve().parents[3] / "schemas" / "human-necessity-report.schema.json")
    if issues:
        raise RecordValidationError(
            "human summary requires a valid human-necessity report",
            details={"findings": format_issues(issues).splitlines()},
        )
    attempted = ", ".join(
        item["strategy_id"] for item in report["automated_strategies_attempted"]
    ) or "None; active policy declares this action human-owned."
    return (
        "Goal reached: NO\n"
        "Human intervention required: YES\n"
        f"Reason: {report['reason_code']}\n"
        f"Automated actions attempted: {attempted}\n"
        "Why automation cannot continue: "
        f"{report['why_no_machine_route_remains']}\n"
        f"Required user action: {report['smallest_requested_user_action']}\n"
    )
