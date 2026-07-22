"""Continuous implementation-plan intake, authority, and coordination."""

from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from agentjob_runtime.errors import (
    BootstrapRequired,
    IntegrityError,
    RecordValidationError,
    StateConflict,
)
from agentjob_runtime.goal.model import parse_utc, utc_now
from agentjob_runtime.goal.resolution import classify_resolution
from agentjob_runtime.plan.activation import (
    accept_activation,
    render_combined_acceptance,
)
from agentjob_runtime.plan.completion_report import build_plan_completion_report
from agentjob_runtime.plan.launcher import (
    dispatch_reserved_plan_task,
    reserve_next_plan_task,
)
from agentjob_runtime.plan.model import require_implementation_plan
from agentjob_runtime.records.canonical import canonical_json_bytes, content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


DEFAULT_LOCAL_ACTIONS = (
    "read_plan_and_repository",
    "edit_plan_scoped_files",
    "run_declared_tests",
    "run_declared_builds",
    "regenerate_declared_derivatives",
    "perform_safe_plan_repairs",
)
EXCLUDED_EFFECT_KINDS = (
    "commit",
    "branch_or_worktree",
    "dependency_installation",
    "network_or_external_system",
    "destructive_operation",
    "publication_or_deployment",
)
CONTINUOUS_TERMINALS = frozenset({"goal_reached", "cancelled"})
PLACEHOLDER_RE = re.compile(r"<[A-Z][A-Z0-9_:-]*>")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
REPAIR_SUFFIX_RE = re.compile(r"(?:-R[1-9][0-9]*-[1-9][0-9]*)+$")


def _schema(name: str) -> Path:
    return (
        Path(__file__).resolve().parents[4]
        / "implementation-plan-goal"
        / "schemas"
        / name
    )


def _validated_record(
    value: Mapping[str, Any],
    *,
    schema_name: str,
    hash_field: str | None = None,
    label: str,
) -> dict[str, Any]:
    candidate = copy.deepcopy(dict(value))
    issues = validate_instance(candidate, _schema(schema_name))
    if issues:
        raise RecordValidationError(
            f"{label} failed canonical validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    if hash_field is not None:
        expected = content_sha256(
            {
                key: item
                for key, item in candidate.items()
                if key != hash_field
            }
        )
        if candidate.get(hash_field) != expected:
            raise RecordValidationError(f"{label} content hash is invalid")
    if contains_secret(canonical_json_bytes(candidate).decode("utf-8")):
        raise RecordValidationError(f"{label} appears to contain a secret")
    return candidate


def validate_question_batch(value: Mapping[str, Any]) -> dict[str, Any]:
    return _validated_record(
        value,
        schema_name="plan-question-batch.schema.json",
        hash_field="batch_content_sha256",
        label="plan question batch",
    )


def validate_execution_authority(value: Mapping[str, Any]) -> dict[str, Any]:
    return _validated_record(
        value,
        schema_name="plan-execution-authority.schema.json",
        hash_field="authority_content_sha256",
        label="plan execution authority",
    )


def validate_question_response(value: Mapping[str, Any]) -> dict[str, Any]:
    return _validated_record(
        value,
        schema_name="plan-question-response.schema.json",
        hash_field="response_content_sha256",
        label="plan question response",
    )


def validate_continuous_state(value: Mapping[str, Any]) -> dict[str, Any]:
    result = _validated_record(
        value,
        schema_name="implementation-plan-state-v2.schema.json",
        label="continuous implementation-plan state",
    )
    status = result["status"]
    worker = result["current_worker_thread_id"]
    pending_batch = result["pending_question_batch_sha256"]
    completion = result["completion_report_sha256"]
    if status == "worker_active" and worker is None:
        raise RecordValidationError(
            "worker-active continuous state requires one worker identity"
        )
    if status in {"active", "awaiting_user_input", "goal_reached", "cancelled"} and (
        worker is not None
    ):
        raise RecordValidationError(
            "continuous state retains a worker outside an active worker boundary"
        )
    if status == "awaiting_user_input" and pending_batch is None:
        raise RecordValidationError(
            "awaiting-user-input state requires one complete pending batch"
        )
    if status == "goal_reached" and completion is None:
        raise RecordValidationError(
            "goal-reached state requires a canonical completion report"
        )
    if status != "goal_reached" and completion is not None:
        raise RecordValidationError(
            "only goal-reached state may bind a completion report"
        )
    return result


def validate_coordinator_wakeup(value: Mapping[str, Any]) -> dict[str, Any]:
    result = _validated_record(
        value,
        schema_name="plan-coordinator-wakeup.schema.json",
        hash_field="wakeup_content_sha256",
        label="plan coordinator wakeup",
    )
    if (result["status"] == "delivered") != (
        result["provider_response_sha256"] is not None
    ):
        raise RecordValidationError(
            "delivered wakeup status and provider evidence must agree"
        )
    return result


def _stable_id(prefix: str, value: Mapping[str, Any]) -> str:
    return prefix + content_sha256(value)[:24].upper()


def _validate_id(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or ID_RE.fullmatch(value) is None:
        raise RecordValidationError(f"{field} must be one portable identifier")
    return value


def _task_ids(value: Any, *, known: set[str]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise RecordValidationError("affected_task_ids must be a sequence")
    result = sorted({_validate_id(item, field="task_id") for item in value})
    unknown = sorted(set(result) - known)
    if unknown:
        raise RecordValidationError(
            "intake entry names an unknown plan task",
            details={"unknown_task_ids": unknown},
        )
    return result


def _placeholder_questions(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    for task in plan["tasks"]:
        task_id = str(task["task_id"])
        values = [
            ("objective", task.get("objective")),
            *(
                (f"acceptance_criteria[{index}]", item)
                for index, item in enumerate(task.get("acceptance_criteria", []))
            ),
            *(
                (f"validation_refs[{index}]", item)
                for index, item in enumerate(task.get("validation_refs", []))
            ),
        ]
        for field, item in values:
            if not isinstance(item, str):
                continue
            placeholders = sorted(set(PLACEHOLDER_RE.findall(item)))
            for placeholder in placeholders:
                basis = {
                    "task_id": task_id,
                    "field": field,
                    "placeholder": placeholder,
                }
                questions.append(
                    {
                        "question_id": _stable_id("PQ-", basis),
                        "category": "information",
                        "prompt": (
                            f"For task {task_id}, what value should replace "
                            f"{placeholder} in {field}?"
                        ),
                        "required": True,
                        "affected_task_ids": [task_id],
                        "effect_id": None,
                    }
                )
    return questions


def _normalize_supplied_questions(
    supplied: Sequence[Mapping[str, Any]],
    *,
    known_tasks: set[str],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for raw in supplied:
        item = copy.deepcopy(dict(raw))
        prompt = item.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise RecordValidationError("intake question prompt must be nonblank")
        affected_task_ids = _task_ids(
            item.get("affected_task_ids"),
            known=known_tasks,
        )
        question_id = item.get("question_id") or _stable_id(
            "PQ-",
            {
                "category": item.get("category", "information"),
                "prompt": prompt.strip(),
                "affected_task_ids": affected_task_ids,
            },
        )
        category = item.get("category", "information")
        if category not in {"information", "authorization", "human_decision"}:
            raise RecordValidationError("intake question category is invalid")
        effect_id = item.get("effect_id")
        if effect_id is not None:
            effect_id = _validate_id(effect_id, field="effect_id")
        result.append(
            {
                "question_id": _validate_id(question_id, field="question_id"),
                "category": category,
                "prompt": prompt.strip(),
                "required": item.get("required", True) is True,
                "affected_task_ids": affected_task_ids,
                "effect_id": effect_id,
            }
        )
    return result


def _normalize_effects(
    supplied: Sequence[Mapping[str, Any]],
    *,
    known_tasks: set[str],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for raw in supplied:
        item = copy.deepcopy(dict(raw))
        kind = item.get("kind")
        if kind not in EXCLUDED_EFFECT_KINDS:
            raise RecordValidationError(
                "protected effect kind is not declared by the portable contract"
            )
        description = item.get("description")
        if not isinstance(description, str) or not description.strip():
            raise RecordValidationError(
                "protected effect description must be nonblank"
            )
        affected_task_ids = _task_ids(
            item.get("affected_task_ids"),
            known=known_tasks,
        )
        effect_id = item.get("effect_id") or _stable_id(
            "PE-",
            {
                "kind": kind,
                "description": description.strip(),
                "affected_task_ids": affected_task_ids,
            },
        )
        result.append(
            {
                "effect_id": _validate_id(effect_id, field="effect_id"),
                "kind": kind,
                "description": description.strip(),
                "required": item.get("required", True) is True,
                "affected_task_ids": affected_task_ids,
            }
        )
    return result


def _repository_safeguards(
    plan: Mapping[str, Any],
    observation: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    if observation is None:
        return [
            {
                "reason_code": "plan.repository_observation_missing",
                "message": (
                    "A current repository observation is required before execution."
                ),
                "affected_task_ids": [],
            }
        ]
    binding = plan["repository_binding"]
    aliases = {"starting_revision": ("starting_revision", "revision")}
    mismatches: list[str] = []
    for key in ("root", "worktree", "branch", "starting_revision", "git_common_dir"):
        observed = next(
            (
                observation.get(alias)
                for alias in aliases.get(key, (key,))
                if observation.get(alias) is not None
            ),
            None,
        )
        if observed != binding.get(key):
            mismatches.append(key)
    if not mismatches:
        return []
    return [
        {
            "reason_code": "plan.repository_identity_mismatch",
            "message": (
                "The current repository does not match the accepted binding for: "
                + ", ".join(sorted(mismatches))
                + "."
            ),
            "affected_task_ids": [],
        }
    ]


def _provider_safeguards(
    capabilities: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    required = {
        "available": True,
        "automatic": True,
        "can_configure_current_thread": True,
        "can_create_with_reasoning_effort": True,
        "can_verify_effective_reasoning_effort": True,
        "can_reuse_bound_checkout": True,
        "can_wait_for_terminal": True,
        "can_resume_thread": True,
    }
    supplied = dict(capabilities or {})
    missing = sorted(
        key for key, expected in required.items() if supplied.get(key) is not expected
    )
    supported = supplied.get("supported_reasoning_efforts", [])
    if not isinstance(supported, Sequence) or "max" not in supported:
        missing.append("supported_reasoning_efforts:max")
    if not missing:
        return []
    return [
        {
            "reason_code": "plan.continuous_provider_unavailable",
            "message": (
                "Continuous execution requires an automatic ThreadProvider with "
                "verified max effort, terminal waiting, and coordinator resumption; "
                "missing: "
                + ", ".join(missing)
                + "."
            ),
            "affected_task_ids": [],
        }
    ]


@dataclass(frozen=True)
class ContinuousPreparation:
    proposal: dict[str, Any]
    plan: dict[str, Any]
    question_batch: dict[str, Any]
    execution_authority: dict[str, Any]
    prompt: str
    status: str

    def as_dict(self) -> dict[str, Any]:
        return copy.deepcopy(asdict(self))


def prepare_continuous_activation(
    proposal: Mapping[str, Any],
    *,
    plan: Mapping[str, Any],
    plan_schema_path: str | Path,
    repository_observation: Mapping[str, Any] | None,
    provider_capabilities: Mapping[str, Any] | None,
    plan_revision: int = 1,
    requested_effects: Sequence[Mapping[str, Any]] = (),
    questions: Sequence[Mapping[str, Any]] = (),
    timestamp: str | None = None,
) -> ContinuousPreparation:
    """Inspect the complete plan and render one consolidated activation prompt."""

    canonical_plan = require_implementation_plan(
        plan,
        schema_path=plan_schema_path,
    )
    if canonical_plan.get("schema_version") != "sys4ai.implementation-plan.v2":
        raise StateConflict(
            "continuous activation requires an immutable implementation-plan v2; "
            "legacy v1 remains readable in explicit manual mode",
            details={"reason_code": "plan.continuous_v2_required"},
        )
    plan_sha256 = content_sha256(canonical_plan)
    if (
        isinstance(plan_revision, bool)
        or not isinstance(plan_revision, int)
        or plan_revision < 1
    ):
        raise RecordValidationError("plan_revision must be a positive integer")
    if (
        proposal.get("plan_id") != canonical_plan["plan_id"]
        or proposal.get("accepted_plan_sha256") != plan_sha256
        or proposal.get("reasoning_effort") != "max"
    ):
        raise StateConflict(
            "continuous intake does not match the accepted plan and max profile",
            details={"reason_code": "plan_activation.binding_mismatch"},
        )
    now = timestamp or utc_now()
    parse_utc(now)
    known_tasks = {str(item["task_id"]) for item in canonical_plan["tasks"]}
    effects = _normalize_effects(requested_effects, known_tasks=known_tasks)
    all_questions = [
        *_placeholder_questions(canonical_plan),
        *_normalize_supplied_questions(questions, known_tasks=known_tasks),
    ]
    all_questions.extend(
        {
            "question_id": _stable_id(
                "PQ-",
                {"effect_id": effect["effect_id"], "kind": effect["kind"]},
            ),
            "category": "authorization",
            "prompt": (
                "The accepted plan requires this protected action: "
                + effect["description"]
                + " Authorize this exact action?"
            ),
            "required": effect["required"],
            "affected_task_ids": effect["affected_task_ids"],
            "effect_id": effect["effect_id"],
        }
        for effect in effects
    )
    by_question_id: dict[str, dict[str, Any]] = {}
    for item in all_questions:
        existing = by_question_id.get(item["question_id"])
        if existing is not None and existing != item:
            raise RecordValidationError(
                "consolidated questions have a conflicting question_id"
            )
        by_question_id[item["question_id"]] = item
    ordered_questions = [by_question_id[key] for key in sorted(by_question_id)]
    effect_by_id: dict[str, dict[str, Any]] = {}
    for effect in effects:
        existing = effect_by_id.get(effect["effect_id"])
        if existing is not None and existing != effect:
            raise RecordValidationError(
                "protected effects have a conflicting effect_id"
            )
        effect_by_id[effect["effect_id"]] = effect
    ordered_effects = [effect_by_id[key] for key in sorted(effect_by_id)]
    safeguards = [
        *_repository_safeguards(canonical_plan, repository_observation),
        *_provider_safeguards(provider_capabilities),
    ]
    safeguards.sort(key=lambda item: (item["reason_code"], item["message"]))
    batch_basis = {
        "plan_id": canonical_plan["plan_id"],
        "accepted_plan_sha256": plan_sha256,
        "accepted_plan_revision": plan_revision,
        "questions": ordered_questions,
        "safeguards": safeguards,
    }
    question_batch = {
        "schema_version": "sys4ai.plan-question-batch.v1",
        "batch_id": _stable_id("PQB-", batch_basis),
        **batch_basis,
        "created_at": now,
        "hash_basis": "canonical_json_without_batch_content_sha256",
        "batch_content_sha256": "",
        "finalized": True,
    }
    question_batch["batch_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in question_batch.items()
            if key != "batch_content_sha256"
        }
    )
    question_batch = validate_question_batch(question_batch)
    authority_basis = {
        "plan_id": canonical_plan["plan_id"],
        "accepted_plan_sha256": plan_sha256,
        "accepted_plan_revision": plan_revision,
        "bound_checkout_only": True,
        "default_local_actions": list(DEFAULT_LOCAL_ACTIONS),
        "excluded_effect_kinds": list(EXCLUDED_EFFECT_KINDS),
        "requested_effects": ordered_effects,
    }
    authority = {
        "schema_version": "sys4ai.plan-execution-authority.v1",
        "authority_id": _stable_id("PEA-", authority_basis),
        **authority_basis,
        "created_at": now,
        "hash_basis": "canonical_json_without_authority_content_sha256",
        "authority_content_sha256": "",
        "finalized": True,
    }
    authority["authority_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in authority.items()
            if key != "authority_content_sha256"
        }
    )
    authority = validate_execution_authority(authority)
    presented, prompt = render_combined_acceptance(proposal)
    if ordered_questions:
        prompt += "\n\nBefore I start, please answer all of these in one reply:\n"
        prompt += "\n".join(
            f"{index}. {item['prompt']}"
            for index, item in enumerate(ordered_questions, start=1)
        )
    if safeguards:
        prompt += "\n\nI cannot start safely until these items are resolved:\n"
        prompt += "\n".join(
            f"- {item['message']}" for item in safeguards
        )
    return ContinuousPreparation(
        proposal=presented,
        plan=canonical_plan,
        question_batch=question_batch,
        execution_authority=authority,
        prompt=prompt,
        status=("suspended_safeguard" if safeguards else "confirmation_required"),
    )


def build_question_response(
    question_batch: Mapping[str, Any],
    execution_authority: Mapping[str, Any],
    *,
    answers: Mapping[str, str] | None = None,
    grants: Mapping[str, bool] | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    batch = validate_question_batch(question_batch)
    authority = validate_execution_authority(execution_authority)
    if (
        batch["plan_id"] != authority["plan_id"]
        or batch["accepted_plan_sha256"] != authority["accepted_plan_sha256"]
        or batch["accepted_plan_revision"]
        != authority["accepted_plan_revision"]
    ):
        raise StateConflict("question batch and execution authority disagree")
    supplied_answers = dict(answers or {})
    supplied_grants = dict(grants or {})
    required_questions = {
        item["question_id"]
        for item in batch["questions"]
        if item["required"] is True and item["category"] != "authorization"
    }
    missing_answers = sorted(required_questions - set(supplied_answers))
    required_effects = {
        item["effect_id"]
        for item in authority["requested_effects"]
        if item["required"] is True
    }
    missing_grants = sorted(
        effect_id
        for effect_id in required_effects
        if supplied_grants.get(effect_id) is not True
    )
    if missing_answers or missing_grants:
        raise StateConflict(
            "all unresolved questions and exact grants must be submitted together",
            details={
                "unanswered_question_ids": missing_answers,
                "unresolved_questions": [
                    item["prompt"]
                    for item in batch["questions"]
                    if item["question_id"] in missing_answers
                ],
                "ungranted_effect_ids": missing_grants,
                "unresolved_authorizations": [
                    item["description"]
                    for item in authority["requested_effects"]
                    if item["effect_id"] in missing_grants
                ],
            },
        )
    unknown_answers = sorted(
        set(supplied_answers)
        - {item["question_id"] for item in batch["questions"]}
    )
    if unknown_answers:
        raise RecordValidationError(
            "question response contains unknown question IDs",
            details={"unknown_question_ids": unknown_answers},
        )
    normalized_answers = []
    for question_id in sorted(supplied_answers):
        answer = supplied_answers[question_id]
        if not isinstance(answer, str) or not answer.strip():
            raise RecordValidationError("question answers must be nonblank text")
        normalized_answers.append(
            {"question_id": question_id, "answer": answer.strip()}
        )
    unknown_grants = sorted(
        set(supplied_grants)
        - {item["effect_id"] for item in authority["requested_effects"]}
    )
    if unknown_grants:
        raise RecordValidationError(
            "question response contains unknown effect IDs",
            details={"unknown_effect_ids": unknown_grants},
        )
    normalized_grants = [
        {"effect_id": effect_id, "granted": supplied_grants[effect_id] is True}
        for effect_id in sorted(supplied_grants)
    ]
    now = timestamp or utc_now()
    parse_utc(now)
    response_basis = {
        "batch_id": batch["batch_id"],
        "batch_content_sha256": content_sha256(batch),
        "answers": normalized_answers,
        "grants": normalized_grants,
        "answered_at": now,
    }
    response = {
        "schema_version": "sys4ai.plan-question-response.v1",
        "response_id": _stable_id("PQR-", response_basis),
        **response_basis,
        "hash_basis": "canonical_json_without_response_content_sha256",
        "response_content_sha256": "",
        "finalized": True,
    }
    response["response_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in response.items()
            if key != "response_content_sha256"
        }
    )
    return validate_question_response(response)


def accept_continuous_activation(
    preparation: ContinuousPreparation,
    *,
    acceptance_message: str,
    acceptance_evidence_ref: str,
    answers: Mapping[str, str] | None = None,
    grants: Mapping[str, bool] | None = None,
    timestamp: str | None = None,
    activation_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Accept goal, max effort, questions, and exact grants in one operation."""

    if preparation.question_batch["safeguards"]:
        raise BootstrapRequired(
            "continuous activation safeguards must be resolved before acceptance",
            details={
                "reason_code": "plan.continuous_safeguard",
                "safeguards": preparation.question_batch["safeguards"],
            },
        )
    if preparation.proposal.get("reasoning_effort") != "max":
        raise StateConflict("continuous implementation-plan execution requires max")
    response = build_question_response(
        preparation.question_batch,
        preparation.execution_authority,
        answers=answers,
        grants=grants,
        timestamp=timestamp,
    )
    accepted, receipt_v1 = accept_activation(
        preparation.proposal,
        acceptance_message=acceptance_message,
        acceptance_evidence_ref=acceptance_evidence_ref,
        timestamp=timestamp,
        activation_id=activation_id,
    )
    receipt_v2 = {
        **receipt_v1,
        "schema_version": "sys4ai.plan-activation-receipt.v2",
        "continuous_execution": True,
        "accepted_plan_revision": preparation.question_batch[
            "accepted_plan_revision"
        ],
        "question_batch_sha256": content_sha256(preparation.question_batch),
        "execution_authority_sha256": content_sha256(
            preparation.execution_authority
        ),
        "question_response_sha256": content_sha256(response),
        "receipt_content_sha256": "",
    }
    receipt_v2["receipt_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in receipt_v2.items()
            if key != "receipt_content_sha256"
        }
    )
    receipt_v2 = _validated_record(
        receipt_v2,
        schema_name="plan-activation-receipt-v2.schema.json",
        hash_field="receipt_content_sha256",
        label="continuous plan activation receipt",
    )
    return accepted, receipt_v2, response


def build_continuous_state(
    plan_record: Mapping[str, Any],
    *,
    activation_receipt: Mapping[str, Any],
    question_batch: Mapping[str, Any],
    execution_authority: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    batch = validate_question_batch(question_batch)
    authority = validate_execution_authority(execution_authority)
    if activation_receipt.get("schema_version") != (
        "sys4ai.plan-activation-receipt.v2"
    ):
        raise RecordValidationError(
            "continuous state requires an activation receipt v2"
        )
    if (
        batch["plan_id"] != plan_record["plan_id"]
        or batch["accepted_plan_sha256"] != plan_record["plan_sha256"]
        or authority["plan_id"] != batch["plan_id"]
        or authority["accepted_plan_sha256"]
        != batch["accepted_plan_sha256"]
        or authority["accepted_plan_revision"]
        != batch["accepted_plan_revision"]
        or activation_receipt.get("accepted_plan_revision")
        != batch["accepted_plan_revision"]
        or activation_receipt.get("question_batch_sha256")
        != content_sha256(batch)
        or activation_receipt.get("execution_authority_sha256")
        != content_sha256(authority)
    ):
        raise StateConflict(
            "continuous state inputs do not share one accepted plan revision"
        )
    now = timestamp or utc_now()
    parse_utc(now)
    state = plan_record["state"]
    value = {
        "schema_version": "sys4ai.implementation-plan-state.v2",
        "plan_id": plan_record["plan_id"],
        "plan_sha256": plan_record["effective_plan_sha256"],
        "revision": 1,
        "status": "active",
        "coordinator_thread_id": activation_receipt["current_thread_id"],
        "current_worker_thread_id": None,
        "current_generation": state["current_generation"],
        "base_plan_revision": state["revision"],
        "base_state_sha256": content_sha256(state),
        "activation_receipt_sha256": content_sha256(activation_receipt),
        "question_batch_sha256": content_sha256(batch),
        "execution_authority_sha256": content_sha256(authority),
        "pending_question_batch_sha256": None,
        "last_worker_receipt_sha256": None,
        "completion_report_sha256": None,
        "repair_history": [],
        "wakeup": {"status": "idle", "wakeup_id": None},
        "updated_at": now,
        "extensions": {},
    }
    return validate_continuous_state(value)


def transition_continuous_state(
    state: Mapping[str, Any],
    *,
    status: str,
    base_plan_record: Mapping[str, Any],
    timestamp: str | None = None,
    current_worker_thread_id: str | None = None,
    pending_question_batch_sha256: str | None = None,
    last_worker_receipt_sha256: str | None = None,
    completion_report_sha256: str | None = None,
    wakeup: Mapping[str, Any] | None = None,
    repair_history: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    value = copy.deepcopy(dict(state))
    if value["status"] in CONTINUOUS_TERMINALS and status != value["status"]:
        raise StateConflict("continuous terminal state is immutable")
    base_phase = base_plan_record["state"]["phase"]
    if status == "goal_reached" and (
        base_phase != "terminal_complete" or completion_report_sha256 is None
    ):
        raise IntegrityError(
            "goal-reached transition requires terminal plan completion evidence"
        )
    if status == "cancelled" and base_phase != "terminal_cancelled":
        raise IntegrityError(
            "cancelled transition requires canonical plan cancellation"
        )
    value.update(
        {
            "plan_sha256": base_plan_record["effective_plan_sha256"],
            "revision": int(value["revision"]) + 1,
            "status": status,
            "current_worker_thread_id": current_worker_thread_id,
            "current_generation": base_plan_record["state"]["current_generation"],
            "base_plan_revision": base_plan_record["state"]["revision"],
            "base_state_sha256": content_sha256(base_plan_record["state"]),
            "pending_question_batch_sha256": pending_question_batch_sha256,
            "last_worker_receipt_sha256": last_worker_receipt_sha256,
            "completion_report_sha256": completion_report_sha256,
            "updated_at": timestamp or utc_now(),
        }
    )
    if wakeup is not None:
        value["wakeup"] = copy.deepcopy(dict(wakeup))
    if repair_history is not None:
        value["repair_history"] = [copy.deepcopy(dict(item)) for item in repair_history]
    return validate_continuous_state(value)


@dataclass(frozen=True)
class ContinuousAdvanceResult:
    status: str
    reason_code: str
    plan_id: str
    plan_revision: int
    continuous_revision: int
    generation: int
    task_id: str | None = None
    worker_thread_id: str | None = None
    resolution: dict[str, Any] | None = None
    completion_report_sha256: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return copy.deepcopy(asdict(self))


def _active_task(record: Mapping[str, Any]) -> Mapping[str, Any] | None:
    task_id = record["state"].get("active_task_id")
    return next(
        (item for item in record["state"]["tasks"] if item["task_id"] == task_id),
        None,
    )


PROTECTED_REPAIR_TASK_STATUSES = frozenset(
    {"blocked", "replan_required", "human_gate_required", "validation_failed"}
)


def _protected_task(record: Mapping[str, Any]) -> Mapping[str, Any] | None:
    active = _active_task(record)
    if isinstance(active, Mapping) and active.get("status") == "invocation_unknown":
        return active
    return next(
        (
            item
            for item in record["state"]["tasks"]
            if item.get("status") in PROTECTED_REPAIR_TASK_STATUSES
        ),
        None,
    )


def _logical_repair_task_id(task_id: str) -> str:
    """Keep one blocker identity across append-only replacement attempts."""

    return REPAIR_SUFFIX_RE.sub("", task_id)


def _classifier_history(
    history: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "blocker_signature": item["blocker_signature"],
            "selected_strategy_id": item["strategy_id"],
        }
        for item in history
    ]


def _protected_resolution(
    record: Mapping[str, Any],
    *,
    history: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    phase = str(record["state"]["phase"])
    task = _protected_task(record)
    task_status = str(task.get("status")) if isinstance(task, Mapping) else ""
    task_id = str(task.get("task_id")) if isinstance(task, Mapping) else ""
    reason = {
        "replan_required": "plan_task.task_requires_replan",
        "blocked": "plan.blocked_no_runnable",
        "human_gate_required": "plan.human_gate_required",
        "validation_failed": "plan.validation_failed",
        "invocation_unknown": "plan.provider_ambiguous",
    }.get(
        task_status,
        {
            "terminal_capability_blocked": "plan.capability_blocked",
            "terminal_corrupt_state": "plan.integrity_failed",
            "terminal_blocked_no_runnable": "plan.blocked_no_runnable",
            "terminal_awaiting_human": "plan.human_gate_required",
            "terminal_validation_failed": "plan.validation_failed",
            "recovery_pending": "plan.recovery_pending",
        }.get(phase, "plan.machine_repair"),
    )
    explicit_human = phase == "terminal_awaiting_human" or task_status == (
        "human_gate_required"
    )
    integrity = phase == "terminal_corrupt_state" or task_status == (
        "invocation_unknown"
    )
    cancelled = phase == "terminal_cancelled"
    return classify_resolution(
        reason_code=reason,
        status=phase,
        evidence={
            "plan_id": record["plan_id"],
            "logical_task_id": (
                _logical_repair_task_id(task_id) if task_id else None
            ),
            "task_status": task_status,
        },
        history=_classifier_history(history),
        authority_refs=["plan-execution-authority"],
        evidence_refs=[record["journal"][-1]["event_hash"]],
        legal_route_available=not explicit_human and not integrity and not cancelled,
        explicit_human_gate=explicit_human,
        integrity_incident=integrity,
        cancelled=cancelled,
    )


def _late_question_batch(
    record: Mapping[str, Any],
    resolution: Mapping[str, Any],
    *,
    accepted_plan_sha256: str,
    accepted_plan_revision: int,
    timestamp: str,
) -> dict[str, Any]:
    prompt = str(
        resolution.get("human_reason")
        or "Please provide the smallest decision or authority needed to resume."
    )
    basis = {
        "plan_id": record["plan_id"],
        "accepted_plan_sha256": accepted_plan_sha256,
        "accepted_plan_revision": accepted_plan_revision,
        "questions": [
            {
                "question_id": _stable_id(
                    "PQ-",
                    {
                        "blocker_signature": resolution["blocker_signature"],
                        "prompt": prompt,
                    },
                ),
                "category": "human_decision",
                "prompt": prompt,
                "required": True,
                "affected_task_ids": (
                    [str(_protected_task(record)["task_id"])]
                    if _protected_task(record) is not None
                    else []
                ),
                "effect_id": None,
            }
        ],
        "safeguards": [],
    }
    batch = {
        "schema_version": "sys4ai.plan-question-batch.v1",
        "batch_id": _stable_id("PQB-", basis),
        **basis,
        "created_at": timestamp,
        "hash_basis": "canonical_json_without_batch_content_sha256",
        "batch_content_sha256": "",
        "finalized": True,
    }
    batch["batch_content_sha256"] = content_sha256(
        {key: item for key, item in batch.items() if key != "batch_content_sha256"}
    )
    return validate_question_batch(batch)


def _apply_machine_repair(
    store: Any,
    *,
    state: Mapping[str, Any],
    record: Mapping[str, Any],
    resolution: Mapping[str, Any],
    timestamp: str,
    repair_executor: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None,
) -> tuple[str, dict[str, Any]]:
    """Apply one distinct strategy and append a replacement when task-bound."""

    executor_status = "succeeded"
    if repair_executor is not None:
        repair_result = repair_executor(resolution)
        executor_status = (
            "succeeded"
            if repair_result.get("status") == "succeeded"
            else "failed"
        )
    if executor_status != "succeeded":
        return "failed", store.load_plan(record["plan_id"])

    current = store.load_plan(record["plan_id"])
    task = _protected_task(current)
    if isinstance(task, Mapping) and task.get("status") == "invocation_unknown":
        return "failed", current
    if isinstance(task, Mapping) and task.get("status") in (
        PROTECTED_REPAIR_TASK_STATUSES
    ):
        repaired = store.supersede_protected_task(
            record["plan_id"],
            expected_revision=current["state"]["revision"],
            reason_code=str(resolution["reason_code"]),
            reason=(
                "Continuous coordinator applied distinct repair strategy "
                f"{resolution['selected_strategy_id']} before retrying the "
                "accepted task as an append-only replacement."
            ),
            authorization_ref=(
                "sqlite/plan_execution_authorities/"
                + str(state["execution_authority_sha256"])
            ),
            evidence_ref=(
                "sqlite/plan_repairs/"
                + str(resolution["blocker_signature"])
                + ".json"
            ),
            timestamp=timestamp,
        )
        resumed = store.resume_repaired_plan(
            record["plan_id"],
            expected_revision=repaired["state"]["revision"],
            evidence_ref=(
                "sqlite/plan_repairs/"
                + str(resolution["blocker_signature"])
                + ".json"
            ),
            timestamp=timestamp,
        )
        return "succeeded", resumed
    if current["state"]["phase"] == "recovery_pending" and any(
        item["status"] == "pending" for item in current["state"]["tasks"]
    ):
        resumed = store.resume_repaired_plan(
            record["plan_id"],
            expected_revision=current["state"]["revision"],
            evidence_ref=(
                "sqlite/plan_repairs/"
                + str(resolution["blocker_signature"])
                + ".json"
            ),
            timestamp=timestamp,
        )
        return "succeeded", resumed
    return (
        ("succeeded", current)
        if repair_executor is not None
        else ("failed", current)
    )


def _handle_resolution(
    store: Any,
    *,
    state: Mapping[str, Any],
    record: Mapping[str, Any],
    resolution: Mapping[str, Any],
    timestamp: str,
    repair_executor: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None,
) -> ContinuousAdvanceResult:
    if resolution["requires_human"] is True:
        accepted_batch = store.load_question_batch(
            record["plan_id"],
            batch_sha256=state["question_batch_sha256"],
        )
        batch = _late_question_batch(
            record,
            resolution,
            accepted_plan_sha256=accepted_batch["accepted_plan_sha256"],
            accepted_plan_revision=accepted_batch["accepted_plan_revision"],
            timestamp=timestamp,
        )
        store.persist_question_batch(record["plan_id"], batch)
        updated = transition_continuous_state(
            state,
            status=(
                "suspended_safeguard"
                if resolution["classification"]
                == "integrity_incident_requires_owner"
                else "awaiting_user_input"
            ),
            base_plan_record=record,
            timestamp=timestamp,
            pending_question_batch_sha256=content_sha256(batch),
            repair_history=state["repair_history"],
        )
        store.update_continuous_state(state["revision"], updated)
        return ContinuousAdvanceResult(
            updated["status"],
            str(resolution["reason_code"]),
            record["plan_id"],
            record["state"]["revision"],
            updated["revision"],
            record["state"]["current_generation"],
            resolution=dict(resolution),
        )

    outcome, repaired_record = _apply_machine_repair(
        store,
        state=state,
        record=record,
        resolution=resolution,
        timestamp=timestamp,
        repair_executor=repair_executor,
    )
    history = list(state["repair_history"])
    history.append(
        {
            "blocker_signature": resolution["blocker_signature"],
            "strategy_id": str(resolution["selected_strategy_id"]),
            "attempt": int(resolution["strategy_attempt"]),
            "outcome": outcome,
            "evidence_refs": list(resolution.get("evidence_refs", [])),
        }
    )
    updated = transition_continuous_state(
        state,
        status="active",
        base_plan_record=repaired_record,
        timestamp=timestamp,
        repair_history=history,
    )
    store.update_continuous_state(state["revision"], updated)
    return ContinuousAdvanceResult(
        "repair_applied",
        str(resolution["reason_code"]),
        record["plan_id"],
        repaired_record["state"]["revision"],
        updated["revision"],
        repaired_record["state"]["current_generation"],
        resolution=dict(resolution),
    )


def advance_once(
    store: Any,
    *,
    plan_id: str,
    provider: Any,
    current_outer_holder_token: str | None = None,
    timestamp: str | None = None,
    repair_executor: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None = None,
) -> ContinuousAdvanceResult:
    """Advance one idempotent coordinator boundary without requiring `continue`."""

    now = timestamp or utc_now()
    state = store.load_continuous_state(plan_id)
    record = store.load_plan(plan_id)
    if state["status"] in CONTINUOUS_TERMINALS:
        return ContinuousAdvanceResult(
            state["status"],
            "plan.goal_reached" if state["status"] == "goal_reached" else "plan.cancelled",
            plan_id,
            record["state"]["revision"],
            state["revision"],
            record["state"]["current_generation"],
            completion_report_sha256=state["completion_report_sha256"],
        )
    if state["status"] in {"awaiting_user_input", "suspended_safeguard"}:
        return ContinuousAdvanceResult(
            state["status"],
            (
                "plan.awaiting_user_input"
                if state["status"] == "awaiting_user_input"
                else "plan.suspended_safeguard"
            ),
            plan_id,
            record["state"]["revision"],
            state["revision"],
            record["state"]["current_generation"],
        )
    phase = record["state"]["phase"]
    if phase == "terminal_complete":
        report = store.load_plan_completion_report(plan_id)
        updated = transition_continuous_state(
            state,
            status="goal_reached",
            base_plan_record=record,
            timestamp=now,
            completion_report_sha256=content_sha256(report),
        )
        store.update_continuous_state(state["revision"], updated)
        return ContinuousAdvanceResult(
            "goal_reached",
            "plan.goal_reached",
            plan_id,
            record["state"]["revision"],
            updated["revision"],
            record["state"]["current_generation"],
            completion_report_sha256=content_sha256(report),
        )
    if phase == "terminal_cancelled":
        updated = transition_continuous_state(
            state,
            status="cancelled",
            base_plan_record=record,
            timestamp=now,
        )
        store.update_continuous_state(state["revision"], updated)
        return ContinuousAdvanceResult(
            "cancelled",
            "plan.cancelled",
            plan_id,
            record["state"]["revision"],
            updated["revision"],
            record["state"]["current_generation"],
        )
    if phase in {
        "recovery_pending",
        "terminal_blocked_no_runnable",
        "terminal_awaiting_human",
        "terminal_validation_failed",
        "terminal_capability_blocked",
        "terminal_corrupt_state",
    }:
        resolution = _protected_resolution(
            record,
            history=state["repair_history"],
        )
        return _handle_resolution(
            store,
            state=state,
            record=record,
            resolution=resolution,
            timestamp=now,
            repair_executor=repair_executor,
        )
    if phase in {"initialized", "continuation_required", "completion_candidate"}:
        selection = store.select_next_task(
            plan_id,
            expected_revision=record["state"]["revision"],
        )
        if selection.status == "completion_candidate":
            report = build_plan_completion_report(store, plan_id=plan_id)
            if report["status"] != "complete":
                raise IntegrityError(
                    "completion candidate lacks canonical completion evidence"
                )
            completed = store.finalize_plan_completion(
                plan_id,
                expected_revision=record["state"]["revision"],
                report=report,
                timestamp=now,
            )
            updated = transition_continuous_state(
                state,
                status="goal_reached",
                base_plan_record=completed,
                timestamp=now,
                completion_report_sha256=content_sha256(report),
            )
            store.update_continuous_state(state["revision"], updated)
            return ContinuousAdvanceResult(
                "goal_reached",
                "plan.goal_reached",
                plan_id,
                completed["state"]["revision"],
                updated["revision"],
                completed["state"]["current_generation"],
                completion_report_sha256=content_sha256(report),
            )
        if selection.status != "selected":
            resolution = classify_resolution(
                reason_code=selection.reason_code,
                status=selection.status,
                evidence={
                    "plan_id": plan_id,
                    "outcome": selection.proof["outcome"],
                    "blocking_reasons": selection.proof["blocking_reasons"],
                    "blocked_task_ids": [
                        item["task_id"]
                        for item in selection.proof["ordered_tasks"]
                        if item["status"] == "blocked"
                    ],
                },
                history=_classifier_history(state["repair_history"]),
                authority_refs=["plan-execution-authority"],
                evidence_refs=[record["journal"][-1]["event_hash"]],
                legal_route_available=True,
            )
            return _handle_resolution(
                store,
                state=state,
                record=record,
                resolution=resolution,
                timestamp=now,
                repair_executor=repair_executor,
            )
        outer = store.goal_store.load_goal(record["outer_goal_id"])
        active_outer_lease = outer["state"].get("active_lease")
        if active_outer_lease is not None and current_outer_holder_token is None:
            raise StateConflict(
                "initial continuous advance requires the current outer holder token"
            )
        reservation = reserve_next_plan_task(
            store,
            plan_id=plan_id,
            expected_plan_revision=record["state"]["revision"],
            expected_outer_revision=outer["state"]["revision"],
            current_outer_holder_token=current_outer_holder_token,
            predecessor_thread_id=state["coordinator_thread_id"],
            timestamp=now,
        )
        dispatch = dispatch_reserved_plan_task(
            store,
            reservation=reservation,
            provider=provider,
            timestamp=now,
        )
        if dispatch.status != "dispatched" or dispatch.successor_thread_id is None:
            reason_code = (
                "plan.provider_dispatch_failed"
                if dispatch.status == "dispatch_failed"
                else "plan.provider_dispatch_ambiguous"
            )
            suspended = transition_continuous_state(
                state,
                status="suspended_safeguard",
                base_plan_record=dispatch.plan_record,
                timestamp=now,
                current_worker_thread_id=dispatch.successor_thread_id,
            )
            store.update_continuous_state(state["revision"], suspended)
            return ContinuousAdvanceResult(
                "suspended_safeguard",
                reason_code,
                plan_id,
                dispatch.plan_record["state"]["revision"],
                suspended["revision"],
                dispatch.generation,
                task_id=dispatch.task_id,
                worker_thread_id=dispatch.successor_thread_id,
                resolution={
                    "provider_status": dispatch.status,
                    "provider_id": dispatch.provider_id,
                    "intent_id": dispatch.intent_id,
                    "provider_response_sha256": (
                        dispatch.provider_response_sha256
                    ),
                    "recovery_required": dispatch.recovery_required,
                },
            )
        updated_record = dispatch.plan_record
        updated = transition_continuous_state(
            state,
            status="worker_active",
            base_plan_record=updated_record,
            timestamp=now,
            current_worker_thread_id=dispatch.successor_thread_id,
        )
        store.update_continuous_state(state["revision"], updated)
        return ContinuousAdvanceResult(
            "worker_dispatched",
            "plan.worker_dispatched",
            plan_id,
            updated_record["state"]["revision"],
            updated["revision"],
            dispatch.generation,
            task_id=dispatch.task_id,
            worker_thread_id=dispatch.successor_thread_id,
        )
    task = _active_task(record)
    worker_thread_id = state.get("current_worker_thread_id")
    if worker_thread_id is None:
        intent = store.find_provider_intent(
            plan_id,
            record["state"]["current_generation"],
        )
        worker_thread_id = intent.get("returned_thread_id")
    return ContinuousAdvanceResult(
        "worker_active",
        "plan.worker_active",
        plan_id,
        record["state"]["revision"],
        state["revision"],
        record["state"]["current_generation"],
        task_id=str(task["task_id"]) if isinstance(task, Mapping) else None,
        worker_thread_id=worker_thread_id,
    )


def run_to_goal(
    store: Any,
    *,
    plan_id: str,
    provider: Any,
    current_outer_holder_token: str | None = None,
    worker_driver: Callable[[ContinuousAdvanceResult], None] | None = None,
    repair_executor: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None = None,
) -> ContinuousAdvanceResult:
    """Drive until completion, cancellation, or a genuine nonterminal user gate."""

    outer_token = current_outer_holder_token
    terminal_observation: tuple[str, int, int] | None = None
    while True:
        result = advance_once(
            store,
            plan_id=plan_id,
            provider=provider,
            current_outer_holder_token=outer_token,
            repair_executor=repair_executor,
        )
        outer_token = None
        if result.status in {"worker_dispatched", "worker_active"}:
            if result.status == "worker_dispatched" and worker_driver is not None:
                worker_driver(result)
                continue
            wait = getattr(provider, "wait_for_terminal", None)
            if not callable(wait) or result.worker_thread_id is None:
                record = store.load_plan(plan_id)
                state = store.load_continuous_state(plan_id)
                suspended = transition_continuous_state(
                    state,
                    status="suspended_safeguard",
                    base_plan_record=record,
                    current_worker_thread_id=result.worker_thread_id,
                )
                store.update_continuous_state(state["revision"], suspended)
                return ContinuousAdvanceResult(
                    "suspended_safeguard",
                    "plan.provider_wait_unavailable",
                    plan_id,
                    record["state"]["revision"],
                    suspended["revision"],
                    record["state"]["current_generation"],
                    task_id=result.task_id,
                    worker_thread_id=result.worker_thread_id,
                )
            observation_key = (
                result.worker_thread_id,
                result.plan_revision,
                result.continuous_revision,
            )
            if terminal_observation == observation_key:
                record = store.load_plan(plan_id)
                state = store.load_continuous_state(plan_id)
                suspended = transition_continuous_state(
                    state,
                    status="suspended_safeguard",
                    base_plan_record=record,
                    current_worker_thread_id=result.worker_thread_id,
                )
                store.update_continuous_state(state["revision"], suspended)
                return ContinuousAdvanceResult(
                    "suspended_safeguard",
                    "plan.terminal_worker_receipt_missing",
                    plan_id,
                    record["state"]["revision"],
                    suspended["revision"],
                    record["state"]["current_generation"],
                    task_id=result.task_id,
                    worker_thread_id=result.worker_thread_id,
                )
            try:
                observed = wait(result.worker_thread_id)
            except Exception as exc:
                record = store.load_plan(plan_id)
                state = store.load_continuous_state(plan_id)
                suspended = transition_continuous_state(
                    state,
                    status="suspended_safeguard",
                    base_plan_record=record,
                    current_worker_thread_id=result.worker_thread_id,
                )
                store.update_continuous_state(state["revision"], suspended)
                return ContinuousAdvanceResult(
                    "suspended_safeguard",
                    "plan.provider_wait_ambiguous",
                    plan_id,
                    record["state"]["revision"],
                    suspended["revision"],
                    record["state"]["current_generation"],
                    task_id=result.task_id,
                    worker_thread_id=result.worker_thread_id,
                    resolution={"error_type": type(exc).__name__},
                )
            if not isinstance(observed, Mapping) or observed.get("terminal") is not True:
                return ContinuousAdvanceResult(
                    "worker_active",
                    "plan.worker_active",
                    result.plan_id,
                    result.plan_revision,
                    result.continuous_revision,
                    result.generation,
                    task_id=result.task_id,
                    worker_thread_id=result.worker_thread_id,
                )
            terminal_observation = observation_key
            continue
        if result.status == "repair_applied":
            terminal_observation = None
            continue
        if result.status in {
            "goal_reached",
            "cancelled",
            "awaiting_user_input",
            "suspended_safeguard",
            "repair_required",
        }:
            return result


def answer_and_resume(
    store: Any,
    *,
    plan_id: str,
    question_batch: Mapping[str, Any],
    execution_authority: Mapping[str, Any],
    answers: Mapping[str, str],
    grants: Mapping[str, bool] | None,
    provider: Any,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Persist one complete answer batch and make that answer the resume signal."""

    now = timestamp or utc_now()
    state = store.load_continuous_state(plan_id)
    if state["status"] != "awaiting_user_input":
        raise StateConflict("plan is not awaiting consolidated user input")
    batch = validate_question_batch(question_batch)
    authority = validate_execution_authority(execution_authority)
    if state["pending_question_batch_sha256"] != content_sha256(batch):
        raise StateConflict("answer batch does not match the pending question batch")
    if state["execution_authority_sha256"] != content_sha256(authority):
        raise StateConflict("answer authority differs from the accepted manifest")
    response = build_question_response(
        batch,
        authority,
        answers=answers,
        grants=grants,
        timestamp=now,
    )
    store.persist_question_response(plan_id, response)
    record = store.load_plan(plan_id)
    task = _protected_task(record)
    if isinstance(task, Mapping) and task.get("status") in (
        PROTECTED_REPAIR_TASK_STATUSES
    ):
        repaired = store.supersede_protected_task(
            plan_id,
            expected_revision=record["state"]["revision"],
            reason_code=(
                "plan.human_gate_required"
                if task.get("status") == "human_gate_required"
                else "plan.machine_repair"
            ),
            reason=(
                "The consolidated user response resolved the protected task "
                "boundary; execution continues through an append-only replacement."
            ),
            authorization_ref=(
                "sqlite/plan_question_responses/"
                + str(response["response_content_sha256"])
            ),
            evidence_ref=(
                "sqlite/plan_question_batches/"
                + str(batch["batch_content_sha256"])
            ),
            timestamp=now,
        )
        record = store.resume_repaired_plan(
            plan_id,
            expected_revision=repaired["state"]["revision"],
            evidence_ref=(
                "sqlite/plan_question_responses/"
                + str(response["response_content_sha256"])
            ),
            timestamp=now,
        )
    elif record["state"]["phase"] != "continuation_required":
        raise StateConflict(
            "answered plan boundary is not safe for automatic resumption"
        )
    updated = transition_continuous_state(
        state,
        status="active",
        base_plan_record=record,
        timestamp=now,
    )
    store.update_continuous_state(state["revision"], updated)
    resume = getattr(provider, "resume_thread", None)
    try:
        if not callable(resume):
            raise BootstrapRequired(
                "automatic answer resumption requires ThreadProvider.resume_thread",
                details={"reason_code": "plan.continuous_provider_unavailable"},
            )
        provider_response = resume(
            state["coordinator_thread_id"],
            "The consolidated implementation-plan questions were answered. "
            "Resume the same active coordinator automatically from canonical state.",
        )
    except Exception:
        suspended = transition_continuous_state(
            updated,
            status="suspended_safeguard",
            base_plan_record=record,
            timestamp=now,
        )
        store.update_continuous_state(updated["revision"], suspended)
        return {
            "schema_version": "sys4ai.plan-answer-and-resume-summary.v1",
            "status": "suspended_safeguard",
            "reason_code": "plan.provider_resume_ambiguous",
            "plan_id": plan_id,
            "continuous_revision": suspended["revision"],
            "question_response_sha256": content_sha256(response),
            "provider_response_sha256": None,
            "continue_required": False,
        }
    return {
        "schema_version": "sys4ai.plan-answer-and-resume-summary.v1",
        "status": "active",
        "reason_code": "plan.answer_resumed",
        "plan_id": plan_id,
        "continuous_revision": updated["revision"],
        "question_response_sha256": content_sha256(response),
        "provider_response_sha256": content_sha256(provider_response),
        "continue_required": False,
    }


def notify_coordinator(
    store: Any,
    *,
    plan_id: str,
    generation: int,
    worker_thread_id: str,
    task_receipt_sha256: str,
    provider: Any,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Persist and deliver one idempotent worker-to-coordinator wakeup."""

    now = timestamp or utc_now()
    state = store.load_continuous_state(plan_id)
    basis = {
        "plan_id": plan_id,
        "generation": generation,
        "worker_thread_id": worker_thread_id,
        "coordinator_thread_id": state["coordinator_thread_id"],
        "task_receipt_sha256": task_receipt_sha256,
    }
    wakeup = {
        "schema_version": "sys4ai.plan-coordinator-wakeup.v1",
        "wakeup_id": _stable_id("PCW-", basis),
        **basis,
        "idempotency_key": _stable_id("PCWK-", basis),
        "status": "pending",
        "provider_response_sha256": None,
        "created_at": now,
        "updated_at": now,
        "hash_basis": "canonical_json_without_wakeup_content_sha256",
        "wakeup_content_sha256": "",
        "finalized": True,
    }
    wakeup["wakeup_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in wakeup.items()
            if key != "wakeup_content_sha256"
        }
    )
    wakeup = validate_coordinator_wakeup(wakeup)
    persisted = store.persist_coordinator_wakeup(wakeup)
    if persisted["status"] in {"delivered", "ambiguous"}:
        return persisted
    resume = getattr(provider, "resume_thread", None)
    try:
        if not callable(resume):
            raise BootstrapRequired(
                "worker completion cannot wake the coordinator automatically",
                details={"reason_code": "plan.continuous_provider_unavailable"},
            )
        response = resume(
            state["coordinator_thread_id"],
            "A plan worker finalized its canonical receipt. Advance the same "
            "implementation-plan coordinator automatically; do not ask for continue.",
        )
    except Exception:
        ambiguous = store.finalize_coordinator_wakeup(
            wakeup["wakeup_id"],
            status="ambiguous",
            provider_response_sha256=None,
            timestamp=now,
        )
        fresh_state = store.load_continuous_state(plan_id)
        fresh_record = store.load_plan(plan_id)
        if (
            fresh_state["status"] not in CONTINUOUS_TERMINALS
            and fresh_state["current_generation"] == generation
            and fresh_state.get("current_worker_thread_id") == worker_thread_id
        ):
            suspended = transition_continuous_state(
                fresh_state,
                status="suspended_safeguard",
                base_plan_record=fresh_record,
                timestamp=now,
                current_worker_thread_id=worker_thread_id,
                last_worker_receipt_sha256=task_receipt_sha256,
                wakeup={"status": "ambiguous", "wakeup_id": wakeup["wakeup_id"]},
            )
            store.update_continuous_state(fresh_state["revision"], suspended)
        return ambiguous
    return store.finalize_coordinator_wakeup(
        wakeup["wakeup_id"],
        status="delivered",
        provider_response_sha256=content_sha256(response),
        timestamp=now,
    )
