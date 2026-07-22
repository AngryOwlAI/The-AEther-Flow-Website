"""One-confirmation intake, authority, and uninterrupted goal coordination."""

from __future__ import annotations

import copy
import hashlib
import re
import secrets
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from agentjob_runtime.errors import (
    BootstrapRequired,
    IntegrityError,
    RecordValidationError,
    StateConflict,
)
from agentjob_runtime.goal.activation import (
    _validate_receipt,
    accept_activation,
    render_combined_acceptance,
)
from agentjob_runtime.goal.model import (
    GOAL_SCHEMA_VERSION_V4,
    canonical_goal_text,
    goal_text_sha256,
    parse_utc,
    repository_identity_hash,
    utc_now,
)
from agentjob_runtime.records.canonical import canonical_json_bytes, content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


DEFAULT_LOCAL_ACTIONS = (
    "read_goal_and_repository",
    "edit_goal_scoped_files",
    "run_goal_scoped_tests",
    "run_goal_scoped_builds",
    "regenerate_goal_scoped_derivatives",
    "perform_safe_goal_repairs",
)
FORBIDDEN_ACTION_CLASSES = (
    "commit",
    "dependency_installation",
    "network_or_external_system",
    "destructive_operation",
    "branch_or_worktree",
    "push_or_merge",
    "publication",
    "deployment",
)
SETUP_ACTION_CLASSES = frozenset({"branch_or_worktree"})
INVENTORY_SURFACES = (
    "tasks",
    "policies",
    "commands",
    "checkpoints",
    "adapters",
)
PLACEHOLDER_RE = re.compile(r"<[A-Z][A-Z0-9_:-]*>")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")


def _schema(name: str) -> Path:
    return Path(__file__).resolve().parents[3] / "schemas" / name


def _validated_record(
    value: Mapping[str, Any],
    *,
    schema_name: str,
    hash_field: str | None,
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
            {key: item for key, item in candidate.items() if key != hash_field}
        )
        if candidate.get(hash_field) != expected:
            raise RecordValidationError(f"{label} content hash is invalid")
    if contains_secret(canonical_json_bytes(candidate).decode("utf-8")):
        raise RecordValidationError(f"{label} appears to contain a secret")
    return candidate


def validate_question_batch(value: Mapping[str, Any]) -> dict[str, Any]:
    return _validated_record(
        value,
        schema_name="goal-question-batch.schema.json",
        hash_field="batch_content_sha256",
        label="goal question batch",
    )


def validate_question_response(value: Mapping[str, Any]) -> dict[str, Any]:
    return _validated_record(
        value,
        schema_name="goal-question-response.schema.json",
        hash_field="response_content_sha256",
        label="goal question response",
    )


def validate_execution_authority(value: Mapping[str, Any]) -> dict[str, Any]:
    result = _validated_record(
        value,
        schema_name="goal-execution-authority.schema.json",
        hash_field="authority_content_sha256",
        label="goal execution authority",
    )
    if tuple(result["default_local_actions"]) != DEFAULT_LOCAL_ACTIONS:
        raise RecordValidationError(
            "goal execution authority changed the default local action contract"
        )
    if tuple(result["forbidden_action_classes"]) != FORBIDDEN_ACTION_CLASSES:
        raise RecordValidationError(
            "goal execution authority changed the protected action contract"
        )
    seen: set[str] = set()
    for grant in result["requested_grants"]:
        if grant["grant_id"] in seen:
            raise RecordValidationError("execution authority repeats a grant ID")
        seen.add(grant["grant_id"])
        expected = content_sha256(
            {
                key: grant[key]
                for key in (
                    "action_class",
                    "operation",
                    "target",
                    "description",
                    "phase",
                )
            }
        )
        if grant["action_sha256"] != expected:
            raise RecordValidationError(
                "protected grant action hash differs from its exact action"
            )
        if (
            grant["action_class"] in SETUP_ACTION_CLASSES
            and grant["phase"] != "setup"
        ):
            raise RecordValidationError(
                "repository topology grants must be consumed during pre-loop setup"
            )
    return result


def validate_grant_consumption(value: Mapping[str, Any]) -> dict[str, Any]:
    return _validated_record(
        value,
        schema_name="goal-grant-consumption.schema.json",
        hash_field="consumption_content_sha256",
        label="goal grant consumption",
    )


def _stable_id(prefix: str, value: Mapping[str, Any]) -> str:
    return prefix + content_sha256(value)[:24].upper()


def _portable_id(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or ID_RE.fullmatch(value) is None:
        raise RecordValidationError(f"{field} must be one portable identifier")
    return value


def _canonical_completion_contract(value: Mapping[str, Any]) -> dict[str, Any]:
    from agentjob_runtime.goal.initialize import _validate_completion_contract

    return _validate_completion_contract(value)


def _canonical_repository_binding(value: Mapping[str, Any]) -> dict[str, Any]:
    from agentjob_runtime.goal.initialize import _validate_repository_binding

    return _validate_repository_binding(value)


def _normalize_inventory(value: Mapping[str, Any] | None) -> dict[str, Any]:
    raw = copy.deepcopy(dict(value or {}))
    surfaces_value = raw.get("surfaces", {})
    surfaces = dict(surfaces_value) if isinstance(surfaces_value, Mapping) else {}
    normalized_surfaces: dict[str, list[str]] = {}
    for name in INVENTORY_SURFACES:
        items = surfaces.get(name, [])
        if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
            raise RecordValidationError(f"intake inventory {name} must be a list")
        normalized = sorted({str(item).strip() for item in items if str(item).strip()})
        normalized_surfaces[name] = normalized
    return {
        "inventory_complete": raw.get("inventory_complete") is True,
        "scope_classification": str(raw.get("scope_classification") or "open"),
        "surfaces": normalized_surfaces,
        "protected_actions": copy.deepcopy(raw.get("protected_actions", [])),
        "questions": copy.deepcopy(raw.get("questions", [])),
        "evidence_refs": sorted(
            {
                str(item).strip()
                for item in raw.get("evidence_refs", [])
                if str(item).strip()
            }
        ),
    }


def _normalize_questions(
    supplied: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for raw in supplied:
        item = copy.deepcopy(dict(raw))
        prompt = item.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise RecordValidationError("intake question prompt must be nonblank")
        category = item.get("category", "information")
        if category not in {"information", "human_decision"}:
            raise RecordValidationError(
                "non-grant intake question category is invalid"
            )
        basis = {"category": category, "prompt": prompt.strip()}
        question_id = _portable_id(
            item.get("question_id") or _stable_id("GQ-", basis),
            field="question_id",
        )
        normalized = {
            "question_id": question_id,
            "category": category,
            "prompt": prompt.strip(),
            "required": item.get("required", True) is True,
            "grant_id": None,
        }
        existing = result.get(question_id)
        if existing is not None and existing != normalized:
            raise RecordValidationError("intake question ID is ambiguous")
        result[question_id] = normalized
    return [result[key] for key in sorted(result)]


def _normalize_grants(
    supplied: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for raw in supplied:
        item = copy.deepcopy(dict(raw))
        action_class = item.get("action_class", item.get("kind"))
        if action_class not in FORBIDDEN_ACTION_CLASSES:
            raise RecordValidationError(
                "protected action class is not declared by the portable contract"
            )
        description = item.get("description")
        operation = item.get("operation")
        target = item.get("target")
        for field, value in (
            ("description", description),
            ("operation", operation),
            ("target", target),
        ):
            if not isinstance(value, str) or not value.strip():
                raise RecordValidationError(
                    f"protected action {field} must be nonblank"
                )
        phase = item.get(
            "phase",
            "setup" if action_class in SETUP_ACTION_CLASSES else "runtime",
        )
        if phase not in {"setup", "runtime"}:
            raise RecordValidationError("protected action phase is invalid")
        basis = {
            "action_class": action_class,
            "operation": operation.strip(),
            "target": target.strip(),
            "description": description.strip(),
            "phase": phase,
        }
        action_sha256 = content_sha256(basis)
        grant_id = _portable_id(
            item.get("grant_id") or _stable_id("GG-", basis),
            field="grant_id",
        )
        normalized = {
            "grant_id": grant_id,
            **basis,
            "required": item.get("required", True) is True,
            "action_sha256": action_sha256,
        }
        existing = result.get(grant_id)
        if existing is not None and existing != normalized:
            raise RecordValidationError("protected grant ID is ambiguous")
        result[grant_id] = normalized
    return [result[key] for key in sorted(result)]


def _placeholder_questions(
    goal_text: str,
    completion_contract: Mapping[str, Any],
) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    values = [
        ("goal", goal_text),
        ("completion interpretation", completion_contract["interpretation"]),
        *(
            (f"completion criterion {index}", criterion)
            for index, criterion in enumerate(
                completion_contract["required_evidence"], start=1
            )
        ),
    ]
    for field, value in values:
        for placeholder in sorted(set(PLACEHOLDER_RE.findall(str(value)))):
            prompt = f"What exact value should replace {placeholder} in the {field}?"
            basis = {"field": field, "placeholder": placeholder}
            questions.append(
                {
                    "question_id": _stable_id("GQ-", basis),
                    "category": "information",
                    "prompt": prompt,
                    "required": True,
                    "grant_id": None,
                }
            )
    return questions


def _repository_safeguards(
    binding: Mapping[str, Any],
    observation: Mapping[str, Any] | None,
) -> list[dict[str, str]]:
    if observation is None:
        return [
            {
                "reason_code": "goal.repository_observation_missing",
                "message": "A current repository observation is required before execution.",
            }
        ]
    aliases = {"starting_revision": ("starting_revision", "revision")}
    mismatches: list[str] = []
    for key in (
        "project_id",
        "root",
        "worktree",
        "branch",
        "git_common_dir",
        "starting_revision",
        "environment_mode",
    ):
        observed = next(
            (
                observation.get(alias)
                for alias in aliases.get(key, (key,))
                if alias in observation
            ),
            None,
        )
        if observed != binding.get(key):
            mismatches.append(key)
    return (
        []
        if not mismatches
        else [
            {
                "reason_code": "goal.repository_identity_mismatch",
                "message": (
                    "The current repository differs from the proposed binding at: "
                    + ", ".join(sorted(mismatches))
                    + "."
                ),
            }
        ]
    )


def _provider_safeguards(
    provider_id: str,
    capabilities: Mapping[str, Any] | None,
) -> list[dict[str, str]]:
    supplied = dict(capabilities or {})
    required = {
        "available": True,
        "automatic": True,
        "can_configure_current_thread": True,
        "can_create_with_reasoning_effort": True,
        "can_verify_effective_reasoning_effort": True,
        "can_reuse_bound_checkout": True,
        "can_query_by_idempotency_key": True,
        "can_wait_for_terminal": True,
        "can_resume_thread": True,
    }
    missing = sorted(
        key for key, expected in required.items() if supplied.get(key) is not expected
    )
    supported = supplied.get("supported_reasoning_efforts", [])
    if not isinstance(supported, Sequence) or "max" not in supported:
        missing.append("supported_reasoning_efforts:max")
    if supplied.get("provider_id", provider_id) != provider_id:
        missing.append("provider_id")
    if not missing:
        return []
    return [
        {
            "reason_code": "goal.continuous_provider_unavailable",
            "message": (
                "Uninterrupted execution requires one automatic provider with "
                "verified max effort, bound-checkout reuse, idempotency lookup, "
                "terminal waiting, and coordinator resumption; missing: "
                + ", ".join(missing)
                + "."
            ),
        }
    ]


@dataclass(frozen=True)
class GoalPreparation:
    proposal: dict[str, Any]
    completion_contract: dict[str, Any]
    repository_binding: dict[str, Any]
    repository_observation: dict[str, Any]
    initial_fingerprint: str
    provider_capabilities: dict[str, Any]
    intake_inventory: dict[str, Any]
    question_batch: dict[str, Any]
    execution_authority: dict[str, Any]
    prompt: str
    status: str

    def as_dict(self) -> dict[str, Any]:
        return copy.deepcopy(asdict(self))


def prepare_goal_activation(
    proposal: Mapping[str, Any],
    *,
    completion_contract: Mapping[str, Any],
    repository_binding: Mapping[str, Any],
    repository_observation: Mapping[str, Any] | None,
    initial_fingerprint: str,
    provider_capabilities: Mapping[str, Any] | None,
    intake_inventory: Mapping[str, Any] | None,
    questions: Sequence[Mapping[str, Any]] = (),
    requested_grants: Sequence[Mapping[str, Any]] = (),
    timestamp: str | None = None,
) -> GoalPreparation:
    """Perform deterministic read-only intake and render one complete prompt."""

    pending = copy.deepcopy(dict(proposal))
    exact_goal = canonical_goal_text(str(pending.get("goal_text", "")))
    contract = _canonical_completion_contract(completion_contract)
    binding = _canonical_repository_binding(repository_binding)
    observation = copy.deepcopy(dict(repository_observation or {}))
    capabilities = copy.deepcopy(dict(provider_capabilities or {}))
    inventory = _normalize_inventory(intake_inventory)
    if pending.get("reasoning_effort") != "max":
        raise StateConflict(
            "uninterrupted goal activation requires reasoning_effort: max",
            details={"reason_code": "goal.max_required"},
        )
    if pending.get("current_thread_verification_status") != "verified" or (
        pending.get("current_thread_effective_effort") != "max"
    ):
        raise StateConflict(
            "the coordinator must be configured and verified at max before presentation",
            details={"reason_code": "goal.max_unverified"},
        )
    if (
        pending.get("goal_sha256") != goal_text_sha256(exact_goal)
        or pending.get("completion_contract_sha256") != content_sha256(contract)
        or pending.get("repository_binding") != binding
        or pending.get("repository_identity_sha256")
        != repository_identity_hash(binding)
    ):
        raise StateConflict(
            "activation proposal differs from the exact intake goal, contract, or repository",
            details={"reason_code": "goal.intake_binding_mismatch"},
        )
    if not re.fullmatch(r"[a-f0-9]{64}", initial_fingerprint):
        raise RecordValidationError(
            "initial_fingerprint must be a lowercase SHA-256 value"
        )
    now = timestamp or utc_now()
    parse_utc(now)
    inventory_questions = inventory["questions"]
    if not isinstance(inventory_questions, Sequence) or isinstance(
        inventory_questions, (str, bytes)
    ):
        raise RecordValidationError("intake inventory questions must be a list")
    all_questions = [
        *_placeholder_questions(exact_goal, contract),
        *_normalize_questions(
            [
                *(
                    item
                    for item in inventory_questions
                    if isinstance(item, Mapping)
                ),
                *questions,
            ]
        ),
    ]
    inventory_actions = inventory["protected_actions"]
    if not isinstance(inventory_actions, Sequence) or isinstance(
        inventory_actions, (str, bytes)
    ):
        raise RecordValidationError(
            "intake inventory protected_actions must be a list"
        )
    grants = _normalize_grants(
        [
            *(item for item in inventory_actions if isinstance(item, Mapping)),
            *requested_grants,
        ]
    )
    question_map = {item["question_id"]: item for item in all_questions}
    for grant in grants:
        basis = {"grant_id": grant["grant_id"], "action_sha256": grant["action_sha256"]}
        question = {
            "question_id": _stable_id("GQ-", basis),
            "category": "authorization",
            "prompt": (
                f"Authorize this exact {grant['action_class']} action: "
                f"{grant['description']} Operation: {grant['operation']}. "
                f"Target: {grant['target']}."
            ),
            "required": grant["required"],
            "grant_id": grant["grant_id"],
        }
        question_map[question["question_id"]] = question
    ordered_questions = [question_map[key] for key in sorted(question_map)]
    safeguards = [
        *_repository_safeguards(binding, repository_observation),
        *_provider_safeguards(str(pending["provider_id"]), capabilities),
    ]
    if inventory["inventory_complete"] is not True:
        safeguards.append(
            {
                "reason_code": "goal.intake_inventory_incomplete",
                "message": (
                    "The project intake did not prove that discoverable tasks, policies, "
                    "commands, checkpoints, adapters, and protected effects were inspected."
                ),
            }
        )
    if inventory["scope_classification"] != "closed":
        safeguards.append(
            {
                "reason_code": "goal.execution_scope_open",
                "message": (
                    "The execution scope is still open-ended and cannot be classified safely."
                ),
            }
        )
    safeguards.sort(key=lambda item: (item["reason_code"], item["message"]))
    batch_basis = {
        "goal_sha256": goal_text_sha256(exact_goal),
        "completion_contract_sha256": content_sha256(contract),
        "repository_binding_sha256": content_sha256(binding),
        "repository_observation_sha256": content_sha256(observation),
        "initial_fingerprint": initial_fingerprint,
        "provider_id": str(pending["provider_id"]),
        "provider_capabilities_sha256": content_sha256(capabilities),
        "intake_inventory_sha256": content_sha256(inventory),
        "questions": ordered_questions,
        "safeguards": safeguards,
    }
    batch = {
        "schema_version": "sys4ai.goal-question-batch.v1",
        "batch_id": _stable_id("GQB-", batch_basis),
        **batch_basis,
        "created_at": now,
        "hash_basis": "canonical_json_without_batch_content_sha256",
        "batch_content_sha256": "",
        "finalized": True,
    }
    batch["batch_content_sha256"] = content_sha256(
        {key: item for key, item in batch.items() if key != "batch_content_sha256"}
    )
    batch = validate_question_batch(batch)
    authority_basis = {
        "goal_sha256": goal_text_sha256(exact_goal),
        "completion_contract_sha256": content_sha256(contract),
        "repository_binding_sha256": content_sha256(binding),
        "question_batch_sha256": content_sha256(batch),
        "bound_checkout_only": True,
        "default_local_actions": list(DEFAULT_LOCAL_ACTIONS),
        "forbidden_action_classes": list(FORBIDDEN_ACTION_CLASSES),
        "requested_grants": grants,
    }
    authority = {
        "schema_version": "sys4ai.goal-execution-authority.v1",
        "authority_id": _stable_id("GEA-", authority_basis),
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
    presented, prompt = render_combined_acceptance(pending)
    if ordered_questions:
        prompt += "\n\nPlease answer or authorize every item below in the same reply:\n"
        prompt += "\n".join(
            f"{index}. {item['prompt']}"
            for index, item in enumerate(ordered_questions, start=1)
        )
    if safeguards:
        prompt += "\n\nI cannot start until these admission defects are resolved:\n"
        prompt += "\n".join(f"- {item['message']}" for item in safeguards)
    return GoalPreparation(
        proposal=presented,
        completion_contract=contract,
        repository_binding=binding,
        repository_observation=observation,
        initial_fingerprint=initial_fingerprint,
        provider_capabilities=capabilities,
        intake_inventory=inventory,
        question_batch=batch,
        execution_authority=authority,
        prompt=prompt,
        status="suspended_safeguard" if safeguards else "confirmation_required",
    )


def preparation_from_mapping(value: Mapping[str, Any]) -> GoalPreparation:
    raw = copy.deepcopy(dict(value))
    required = {field.name for field in GoalPreparation.__dataclass_fields__.values()}
    if set(raw) != required:
        raise RecordValidationError(
            "continuous goal preparation fields are incomplete or unknown",
            details={
                "missing": sorted(required - set(raw)),
                "unknown": sorted(set(raw) - required),
            },
        )
    raw["question_batch"] = validate_question_batch(raw["question_batch"])
    raw["execution_authority"] = validate_execution_authority(
        raw["execution_authority"]
    )
    return GoalPreparation(**raw)


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
    if authority["question_batch_sha256"] != content_sha256(batch):
        raise StateConflict("question batch and execution authority disagree")
    supplied_answers = dict(answers or {})
    supplied_grants = dict(grants or {})
    question_ids = {
        item["question_id"]
        for item in batch["questions"]
        if item["category"] != "authorization"
    }
    required_questions = {
        item["question_id"]
        for item in batch["questions"]
        if item["required"] is True and item["category"] != "authorization"
    }
    missing_answers = sorted(required_questions - set(supplied_answers))
    grant_ids = {item["grant_id"] for item in authority["requested_grants"]}
    required_grants = {
        item["grant_id"]
        for item in authority["requested_grants"]
        if item["required"] is True
    }
    missing_grants = sorted(
        grant_id
        for grant_id in required_grants
        if supplied_grants.get(grant_id) is not True
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
                "ungranted_grant_ids": missing_grants,
                "unresolved_authorizations": [
                    item["description"]
                    for item in authority["requested_grants"]
                    if item["grant_id"] in missing_grants
                ],
            },
        )
    if set(supplied_answers) - question_ids:
        raise RecordValidationError("question response contains unknown question IDs")
    if set(supplied_grants) - grant_ids:
        raise RecordValidationError("question response contains unknown grant IDs")
    normalized_answers = []
    for question_id in sorted(supplied_answers):
        answer = supplied_answers[question_id]
        if not isinstance(answer, str) or not answer.strip():
            raise RecordValidationError("question answers must be nonblank text")
        normalized_answers.append(
            {"question_id": question_id, "answer": answer.strip()}
        )
    normalized_grants = [
        {"grant_id": grant_id, "granted": supplied_grants[grant_id] is True}
        for grant_id in sorted(supplied_grants)
    ]
    now = timestamp or utc_now()
    parse_utc(now)
    basis = {
        "batch_id": batch["batch_id"],
        "batch_content_sha256": content_sha256(batch),
        "answers": normalized_answers,
        "grants": normalized_grants,
        "answered_at": now,
    }
    response = {
        "schema_version": "sys4ai.goal-question-response.v1",
        "response_id": _stable_id("GQR-", basis),
        **basis,
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


def accept_goal_activation(
    preparation: GoalPreparation,
    *,
    acceptance_message: str,
    acceptance_evidence_ref: str,
    answers: Mapping[str, str] | None = None,
    grants: Mapping[str, bool] | None = None,
    activation_initial_fingerprint: str | None = None,
    activation_repository_binding: Mapping[str, Any] | None = None,
    activation_repository_observation: Mapping[str, Any] | None = None,
    timestamp: str | None = None,
    activation_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Bind the one user response to every accepted intake input."""

    if preparation.status != "confirmation_required" or preparation.question_batch[
        "safeguards"
    ]:
        raise BootstrapRequired(
            "continuous goal admission defects must be resolved before acceptance",
            details={
                "reason_code": "goal.continuous_safeguard",
                "safeguards": preparation.question_batch["safeguards"],
            },
        )
    if preparation.proposal.get("reasoning_effort") != "max":
        raise StateConflict("continuous goal execution requires max")
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
    activation_fingerprint = (
        activation_initial_fingerprint or preparation.initial_fingerprint
    )
    final_binding = _canonical_repository_binding(
        activation_repository_binding or preparation.repository_binding
    )
    final_observation = copy.deepcopy(
        dict(
            activation_repository_observation
            or preparation.repository_observation
        )
    )
    repository_safeguards = _repository_safeguards(
        final_binding, final_observation
    )
    if repository_safeguards:
        raise StateConflict(
            "repository identity changed outside the accepted setup result",
            details={
                "reason_code": "goal.post_setup_repository_mismatch",
                "safeguards": repository_safeguards,
            },
        )
    if not re.fullmatch(r"[a-f0-9]{64}", activation_fingerprint):
        raise RecordValidationError(
            "activation initial fingerprint must be a lowercase SHA-256 value"
        )
    receipt_v2 = {
        **receipt_v1,
        "schema_version": "sys4ai.goal-activation-receipt.v2",
        "continuous_execution": True,
        "repository_identity_sha256": repository_identity_hash(final_binding),
        "intake_repository_binding_sha256": content_sha256(
            preparation.repository_binding
        ),
        "repository_binding_sha256": content_sha256(final_binding),
        "repository_observation_sha256": content_sha256(final_observation),
        "intake_initial_fingerprint": preparation.initial_fingerprint,
        "activation_initial_fingerprint": activation_fingerprint,
        "intake_inventory_sha256": content_sha256(
            preparation.intake_inventory
        ),
        "question_batch_sha256": content_sha256(
            preparation.question_batch
        ),
        "question_response_sha256": content_sha256(response),
        "execution_authority_sha256": content_sha256(
            preparation.execution_authority
        ),
        "hash_basis": "canonical_json_without_receipt_content_sha256",
        "receipt_content_sha256": "",
    }
    receipt_v2["receipt_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in receipt_v2.items()
            if key != "receipt_content_sha256"
        }
    )
    receipt_v2 = _validate_receipt(receipt_v2)
    return accepted, receipt_v2, response


def validate_continuous_activation_bundle(
    value: Mapping[str, Any],
    *,
    activation_receipt: Mapping[str, Any],
    goal_text: str,
    completion_contract: Mapping[str, Any],
    repository_binding: Mapping[str, Any],
    initial_fingerprint: str,
) -> dict[str, Any]:
    bundle = copy.deepcopy(dict(value))
    batch = validate_question_batch(bundle.get("question_batch", {}))
    response = validate_question_response(bundle.get("question_response", {}))
    authority = validate_execution_authority(
        bundle.get("execution_authority", {})
    )
    receipt = _validate_receipt(activation_receipt)
    if receipt.get("schema_version") != "sys4ai.goal-activation-receipt.v2":
        raise StateConflict("continuous goal initialization requires activation receipt v2")
    exact_goal_hash = goal_text_sha256(goal_text)
    contract_hash = content_sha256(
        _canonical_completion_contract(completion_contract)
    )
    binding = _canonical_repository_binding(repository_binding)
    expected = {
        "accepted_goal_sha256": exact_goal_hash,
        "accepted_completion_contract_sha256": contract_hash,
        "repository_identity_sha256": repository_identity_hash(binding),
        "repository_binding_sha256": content_sha256(binding),
        "question_batch_sha256": content_sha256(batch),
        "question_response_sha256": content_sha256(response),
        "execution_authority_sha256": content_sha256(authority),
        "activation_initial_fingerprint": initial_fingerprint,
    }
    mismatches = {
        field: {"expected": expected_value, "actual": receipt.get(field)}
        for field, expected_value in expected.items()
        if receipt.get(field) != expected_value
    }
    if mismatches:
        raise StateConflict(
            "continuous activation does not bind the initialized values",
            details={"reason_code": "goal.activation_binding_mismatch", "mismatches": mismatches},
        )
    if (
        batch["goal_sha256"] != exact_goal_hash
        or batch["completion_contract_sha256"] != contract_hash
        or batch["repository_binding_sha256"]
        != receipt["intake_repository_binding_sha256"]
        or authority["goal_sha256"] != exact_goal_hash
        or authority["completion_contract_sha256"] != contract_hash
        or authority["repository_binding_sha256"]
        != receipt["intake_repository_binding_sha256"]
        or authority["question_batch_sha256"] != content_sha256(batch)
        or response["batch_id"] != batch["batch_id"]
        or response["batch_content_sha256"] != content_sha256(batch)
    ):
        raise StateConflict("continuous intake records disagree")
    granted = {
        item["grant_id"] for item in response["grants"] if item["granted"] is True
    }
    missing = sorted(
        item["grant_id"]
        for item in authority["requested_grants"]
        if item["required"] is True and item["grant_id"] not in granted
    )
    if missing:
        raise StateConflict(
            "continuous activation is missing required exact grants",
            details={"missing_grant_ids": missing},
        )
    return {
        "activation_receipt": receipt,
        "question_batch": batch,
        "question_response": response,
        "execution_authority": authority,
        "setup_consumptions": copy.deepcopy(bundle.get("setup_consumptions", [])),
    }


def _granted_ids(record: Mapping[str, Any]) -> set[str]:
    return {
        item["grant_id"]
        for item in record["question_response"]["grants"]
        if item["granted"] is True
    }


def available_grant_ids(record: Mapping[str, Any]) -> list[str]:
    if record.get("schema_version") != GOAL_SCHEMA_VERSION_V4:
        return []
    consumed = {item["grant_id"] for item in record["grant_consumptions"]}
    return sorted(_granted_ids(record) - consumed)


def build_grant_consumption_record(
    *,
    goal_id: str,
    generation: int,
    grant: Mapping[str, Any],
    authority: Mapping[str, Any],
    evidence_ref: str,
    timestamp: str,
) -> dict[str, Any]:
    validated_authority = validate_execution_authority(authority)
    exact_grant = next(
        (
            item
            for item in validated_authority["requested_grants"]
            if item["grant_id"] == grant.get("grant_id")
        ),
        None,
    )
    if exact_grant is None or dict(grant) != exact_grant:
        raise StateConflict("grant consumption does not match exact accepted authority")
    basis = {
        "goal_id": goal_id,
        "generation": generation,
        "grant_id": exact_grant["grant_id"],
        "authority_content_sha256": validated_authority[
            "authority_content_sha256"
        ],
        "action_sha256": exact_grant["action_sha256"],
        "evidence_ref": evidence_ref,
        "consumed_at": timestamp,
    }
    consumption = {
        "schema_version": "sys4ai.goal-grant-consumption.v1",
        "consumption_id": _stable_id("GGC-", basis),
        **basis,
        "hash_basis": "canonical_json_without_consumption_content_sha256",
        "consumption_content_sha256": "",
        "finalized": True,
    }
    consumption["consumption_content_sha256"] = content_sha256(
        {
            key: item
            for key, item in consumption.items()
            if key != "consumption_content_sha256"
        }
    )
    return validate_grant_consumption(consumption)


def consume_execution_grant(
    store: Any,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    action: Mapping[str, Any],
    evidence_ref: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Atomically consume the one exact accepted grant and no other action."""

    supplied = copy.deepcopy(dict(action))
    required = {
        "grant_id",
        "action_class",
        "operation",
        "target",
        "description",
        "action_sha256",
    }
    if set(supplied) != required:
        raise RecordValidationError(
            "protected action request is incomplete or contains unknown fields"
        )
    if not evidence_ref.strip():
        raise RecordValidationError("grant consumption requires canonical evidence")
    now = timestamp or utc_now()
    with store.mutation(
        goal_id, expected_revision=expected_revision, timestamp=now
    ) as mutation:
        record = mutation.record
        if record.get("schema_version") != GOAL_SCHEMA_VERSION_V4:
            raise StateConflict("one-shot execution grants require goal state v4")
        grant = next(
            (
                item
                for item in record["execution_authority"]["requested_grants"]
                if item["grant_id"] == supplied["grant_id"]
            ),
            None,
        )
        if grant is None or grant["grant_id"] not in _granted_ids(record):
            raise StateConflict(
                "protected action was not granted by the accepted intake",
                details={"reason_code": "goal.undisclosed_protected_action"},
            )
        if any(
            item["grant_id"] == grant["grant_id"]
            for item in record["grant_consumptions"]
        ):
            raise StateConflict(
                "protected grant has already been consumed",
                details={"reason_code": "goal.grant_already_consumed"},
            )
        exact = {
            key: grant[key]
            for key in (
                "grant_id",
                "action_class",
                "operation",
                "target",
                "description",
                "action_sha256",
            )
        }
        if supplied != exact:
            raise StateConflict(
                "protected grant cannot authorize a different action",
                details={"reason_code": "goal.grant_action_mismatch"},
            )
        consumption = build_grant_consumption_record(
            goal_id=goal_id,
            generation=generation,
            grant=grant,
            authority=record["execution_authority"],
            evidence_ref=evidence_ref,
            timestamp=now,
        )
        record["grant_consumptions"].append(consumption)
        mutation.event(
            "execution_grant_consumed",
            {
                "generation": generation,
                "grant_id": grant["grant_id"],
                "action_sha256": grant["action_sha256"],
                "consumption_content_sha256": consumption[
                    "consumption_content_sha256"
                ],
            },
        )
    return store.load_goal(goal_id)


def route_protected_action(
    store: Any,
    *,
    goal_id: str,
    expected_revision: int,
    generation: int,
    action: Mapping[str, Any],
    preauthorized: bool,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Replace a protected-stop disposition with its lawful v4 continuation."""

    from agentjob_runtime.goal.resolution import (
        append_resolution,
        classify_resolution,
        normal_continuation_disposition,
    )

    now = timestamp or utc_now()
    supplied = copy.deepcopy(dict(action))
    with store.mutation(
        goal_id, expected_revision=expected_revision, timestamp=now
    ) as mutation:
        record = mutation.record
        if (
            record.get("schema_version") != GOAL_SCHEMA_VERSION_V4
            or record["state"]["phase"] != "step_verified"
        ):
            raise StateConflict(
                "protected-action routing requires one verified v4 generation"
            )
        if preauthorized:
            disposition = normal_continuation_disposition(
                reason_code="goal.preauthorized_protected_action",
                evidence={
                    "grant_id": supplied.get("grant_id"),
                    "action_sha256": supplied.get("action_sha256"),
                },
                authority_refs=[
                    "goal-execution-authority:"
                    + record["execution_authority"]["authority_id"]
                ],
                evidence_refs=[f"generation:{generation}:grant-consumption"],
            )
        else:
            disposition = classify_resolution(
                reason_code="goal.undisclosed_protected_action",
                status="route_around",
                evidence={
                    "action_class": supplied.get("action_class"),
                    "operation": supplied.get("operation"),
                    "target": supplied.get("target"),
                    "action_sha256": supplied.get("action_sha256"),
                },
                history=record["resolution_history"],
                authority_refs=["accepted-goal-default-local-actions"],
                evidence_refs=[f"generation:{generation}:protected-action-request"],
                legal_route_available=True,
            )
        append_resolution(
            record,
            generation=generation,
            disposition=disposition,
            progress_dimensions=["blocker_resolution", "strategy"],
        )
        mutation.event(
            "protected_action_routed",
            {
                "generation": generation,
                "preauthorized": preauthorized,
                "action_sha256": supplied.get("action_sha256"),
                "strategy_id": disposition.get("selected_strategy_id"),
            },
        )
    return store.load_goal(goal_id)


@dataclass(frozen=True)
class CoordinatorAdvance:
    status: str
    reason_code: str
    goal_id: str
    goal_revision: int
    generation: int
    worker_thread_id: str | None = None
    completion_report_sha256: str | None = None
    provider_create_calls: int = 0
    continue_required: bool = False

    def as_dict(self) -> dict[str, Any]:
        return copy.deepcopy(asdict(self))


def accept_and_run(
    store: Any,
    *,
    preparation: GoalPreparation,
    acceptance_message: str,
    acceptance_evidence_ref: str,
    answers: Mapping[str, str] | None,
    grants: Mapping[str, bool] | None,
    provider: Any,
    setup_executor: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None = None,
    repository_observer: Callable[[], Mapping[str, Any]] | None = None,
    fingerprint_provider: Callable[[], str] | None = None,
    worker_driver: Callable[[CoordinatorAdvance], None] | None = None,
    guards: Mapping[str, Any] | None = None,
    runtime_binding: Mapping[str, Any] | None = None,
    goal_id: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Accept once, apply accepted setup, initialize v4, and stay active."""

    from agentjob_runtime.goal.initialize import initialize_goal

    if preparation.status != "confirmation_required":
        raise BootstrapRequired(
            "continuous goal preparation is not ready for acceptance",
            details={"reason_code": "goal.continuous_safeguard"},
        )
    live_capabilities = (
        dict(provider.capabilities())
        if callable(getattr(provider, "capabilities", None))
        else {}
    )
    safeguards = _provider_safeguards(
        str(getattr(provider, "provider_id", "")), live_capabilities
    )
    if safeguards or getattr(provider, "provider_id", None) != preparation.proposal[
        "provider_id"
    ]:
        raise BootstrapRequired(
            "the live automatic provider differs from the accepted intake",
            details={
                "reason_code": "goal.continuous_provider_changed",
                "safeguards": safeguards,
            },
        )
    if content_sha256(live_capabilities) != content_sha256(
        preparation.provider_capabilities
    ):
        raise StateConflict(
            "ThreadProvider capabilities changed after presentation; replace the combined intake",
            details={"reason_code": "goal.intake_invalidated"},
        )
    now = timestamp or utc_now()
    parse_utc(now)
    # Validate the complete answer before any setup effect or durable state.
    response_preview = build_question_response(
        preparation.question_batch,
        preparation.execution_authority,
        answers=answers,
        grants=grants,
        timestamp=now,
    )
    granted_ids = {
        item["grant_id"]
        for item in response_preview["grants"]
        if item["granted"] is True
    }
    candidate_goal_id = goal_id or (
        f"CG-{parse_utc(now).strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(8)}"
    )
    final_binding = copy.deepcopy(preparation.repository_binding)
    final_observation = copy.deepcopy(preparation.repository_observation)
    final_fingerprint = preparation.initial_fingerprint
    setup_evidence: list[tuple[dict[str, Any], str]] = []
    setup_grants = [
        item
        for item in preparation.execution_authority["requested_grants"]
        if item["phase"] == "setup" and item["grant_id"] in granted_ids
    ]
    if setup_grants and setup_executor is None:
        raise BootstrapRequired(
            "accepted pre-loop setup requires the configured project setup adapter",
            details={
                "reason_code": "goal.setup_adapter_unavailable",
                "grant_ids": [item["grant_id"] for item in setup_grants],
            },
        )
    for grant in setup_grants:
        outcome = copy.deepcopy(dict(setup_executor(copy.deepcopy(grant))))
        if outcome.get("status") != "applied" or not isinstance(
            outcome.get("evidence_ref"), str
        ) or not outcome["evidence_ref"].strip():
            raise StateConflict(
                "authorized setup did not produce an applied canonical receipt",
                details={
                    "reason_code": "goal.setup_failed",
                    "grant_id": grant["grant_id"],
                },
            )
        if isinstance(outcome.get("repository_binding"), Mapping):
            final_binding = _canonical_repository_binding(
                outcome["repository_binding"]
            )
        if isinstance(outcome.get("repository_observation"), Mapping):
            final_observation = copy.deepcopy(
                dict(outcome["repository_observation"])
            )
        if isinstance(outcome.get("initial_fingerprint"), str):
            final_fingerprint = outcome["initial_fingerprint"]
        setup_evidence.append((copy.deepcopy(grant), outcome["evidence_ref"]))
    if repository_observer is not None:
        final_observation = copy.deepcopy(dict(repository_observer()))
    if fingerprint_provider is not None:
        final_fingerprint = str(fingerprint_provider())
    if not setup_evidence and (
        final_binding != preparation.repository_binding
        or final_observation != preparation.repository_observation
        or final_fingerprint != preparation.initial_fingerprint
    ):
        raise StateConflict(
            "the repository changed after presentation without an accepted setup grant",
            details={"reason_code": "goal.intake_invalidated"},
        )
    if _repository_safeguards(final_binding, final_observation):
        raise StateConflict(
            "post-setup repository identity failed revalidation",
            details={"reason_code": "goal.post_setup_repository_mismatch"},
        )
    if not re.fullmatch(r"[a-f0-9]{64}", final_fingerprint):
        raise RecordValidationError(
            "post-setup initial fingerprint must be a lowercase SHA-256 value"
        )
    _, activation, response = accept_goal_activation(
        preparation,
        acceptance_message=acceptance_message,
        acceptance_evidence_ref=acceptance_evidence_ref,
        answers=answers,
        grants=grants,
        activation_initial_fingerprint=final_fingerprint,
        activation_repository_binding=final_binding,
        activation_repository_observation=final_observation,
        timestamp=now,
    )
    if response != response_preview:
        raise IntegrityError("the accepted response changed during setup")
    setup_consumptions = [
        build_grant_consumption_record(
            goal_id=candidate_goal_id,
            generation=0,
            grant=grant,
            authority=preparation.execution_authority,
            evidence_ref=evidence_ref,
            timestamp=now,
        )
        for grant, evidence_ref in setup_evidence
    ]
    created = initialize_goal(
        store,
        goal_text=preparation.proposal["goal_text"],
        completion_contract=preparation.completion_contract,
        guards=guards,
        repository_binding=final_binding,
        initial_fingerprint=final_fingerprint,
        authorization={"fresh_recursive_threads_explicitly_requested": True},
        activation_receipt=activation,
        runtime_binding=runtime_binding,
        continuous_context={
            "question_batch": preparation.question_batch,
            "question_response": response,
            "execution_authority": preparation.execution_authority,
            "setup_consumptions": setup_consumptions,
        },
        goal_id=candidate_goal_id,
        timestamp=now,
    )
    result = run_to_goal(
        store,
        goal_id=created["goal_id"],
        provider=provider,
        worker_driver=worker_driver,
    )
    return {
        "schema_version": "sys4ai.goal-accept-and-run-summary.v1",
        **result.as_dict(),
        "activation_receipt_sha256": content_sha256(activation),
        "question_batch_sha256": content_sha256(
            preparation.question_batch
        ),
        "question_response_sha256": content_sha256(response),
        "execution_authority_sha256": content_sha256(
            preparation.execution_authority
        ),
        "setup_grants_consumed": [
            item["grant_id"] for item in setup_consumptions
        ],
        "continue_required": False,
    }


def _set_coordinator(
    store: Any,
    record: Mapping[str, Any],
    *,
    status: str,
    worker_thread_id: str | None,
    last_worker_receipt_sha256: str | None = None,
    wakeup: Mapping[str, Any] | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    if record.get("schema_version") != GOAL_SCHEMA_VERSION_V4:
        raise StateConflict("continuous coordination requires goal state v4")
    now = timestamp or utc_now()
    with store.mutation(
        str(record["goal_id"]),
        expected_revision=int(record["state"]["revision"]),
        timestamp=now,
    ) as mutation:
        current = mutation.record["coordinator"]
        current["status"] = status
        current["current_worker_thread_id"] = worker_thread_id
        if last_worker_receipt_sha256 is not None:
            current["last_worker_receipt_sha256"] = last_worker_receipt_sha256
        if wakeup is not None:
            current["wakeup"] = copy.deepcopy(dict(wakeup))
        current["updated_at"] = now
        mutation.event(
            "coordinator_state",
            {
                "status": status,
                "worker_thread_id": worker_thread_id,
                "wakeup": copy.deepcopy(dict(current["wakeup"])),
            },
        )
    return store.load_goal(str(record["goal_id"]))


def _dispatch_current_intent(
    store: Any,
    *,
    record: Mapping[str, Any],
    provider: Any,
    predecessor_thread_id: str | None,
    canonical_state: Mapping[str, Any] | None = None,
    timestamp: str | None = None,
) -> CoordinatorAdvance:
    from agentjob_runtime.goal.launcher import (
        ThreadCreateResult,
        _validate_created_profile,
        build_continuation_envelope,
        build_worker_prompt,
    )
    from agentjob_runtime.goal.successor import (
        record_dispatch_outcome,
        record_successor,
        reserve_successor,
    )

    current = copy.deepcopy(dict(record))
    if current["state"]["phase"] in {"initialized", "continuation_required"}:
        lease = current["state"].get("active_lease")
        if not isinstance(lease, Mapping):
            raise IntegrityError("coordinator cannot reserve without the active lease")
        current = reserve_successor(
            store,
            goal_id=current["goal_id"],
            expected_revision=current["state"]["revision"],
            current_holder_token=lease["holder_token"],
            predecessor_thread_id=predecessor_thread_id,
            timestamp=timestamp,
        )
    if current["state"]["phase"] != "successor_intent":
        raise StateConflict("dispatch requires one canonical successor intent")
    generation = int(current["state"]["current_generation"])
    entry = current["generations"][str(generation)]
    envelope = build_continuation_envelope(
        current,
        predecessor_thread_id=predecessor_thread_id,
        predecessor_handoff_id=None,
        canonical_state=canonical_state
        or {
            "fingerprint": current["state"]["last_canonical_fingerprint"],
            "active_task_id": None,
            "current_decision_id": None,
            "current_job_id": None,
        },
        progress_summary="The uninterrupted goal coordinator admitted the next generation.",
        remaining_work="Continue until canonical evidence marks the exact goal met.",
    )
    prompt = build_worker_prompt(
        envelope,
        project_root=str(current["repository_binding"]["root"]),
        expected_revision=int(current["state"]["revision"]) + 1,
    )
    try:
        result = provider.create_thread(
            prompt=prompt,
            envelope=envelope,
            idempotency_key=entry["idempotency_key"],
            execution_profile=current["execution_profile"],
        )
    except Exception as error:
        result = ThreadCreateResult(
            "ambiguous",
            None,
            {
                "reason_code": "provider.exception",
                "exception_type": type(error).__name__,
            },
        )
    result = _validate_created_profile(
        result,
        execution_profile=current["execution_profile"],
        repository_binding=current["repository_binding"],
        provider=provider,
    )
    status = result.status
    thread_id = result.successor_thread_id
    if status == "returned" and thread_id == predecessor_thread_id:
        status = "duplicate"
        thread_id = None
        result = ThreadCreateResult(
            "duplicate", None, {"reason_code": "provider.reused_predecessor_thread"}
        )
    if status == "returned":
        final = record_successor(
            store,
            goal_id=current["goal_id"],
            expected_revision=current["state"]["revision"],
            generation=generation,
            handoff_token=entry["handoff_token"],
            successor_thread_id=str(thread_id),
            provider_id=str(provider.provider_id),
            provider_response=result.response,
            timestamp=timestamp,
        )
        final = _set_coordinator(
            store,
            final,
            status="worker_active",
            worker_thread_id=str(thread_id),
            timestamp=timestamp,
        )
        return CoordinatorAdvance(
            "worker_dispatched",
            "goal.worker_dispatched",
            str(final["goal_id"]),
            int(final["state"]["revision"]),
            generation,
            str(thread_id),
            provider_create_calls=1,
        )
    final = record_dispatch_outcome(
        store,
        goal_id=current["goal_id"],
        expected_revision=current["state"]["revision"],
        generation=generation,
        handoff_token=entry["handoff_token"],
        provider_id=str(provider.provider_id),
        outcome=status,
        diagnostic=result.response,
        timestamp=timestamp,
    )
    final = _set_coordinator(
        store,
        final,
        status="suspended_safeguard"
        if status == "duplicate"
        else "active",
        worker_thread_id=thread_id,
        timestamp=timestamp,
    )
    return CoordinatorAdvance(
        "suspended_safeguard" if status == "duplicate" else "provider_recovery",
        "goal.provider_duplicate"
        if status == "duplicate"
        else "goal.provider_dispatch_ambiguous",
        str(final["goal_id"]),
        int(final["state"]["revision"]),
        generation,
        thread_id,
        provider_create_calls=1,
    )


def advance_once(
    store: Any,
    *,
    goal_id: str,
    provider: Any,
    timestamp: str | None = None,
) -> CoordinatorAdvance:
    """Advance one idempotent coordinator boundary from canonical v4 state."""

    from agentjob_runtime.goal.recovery import reconcile_ambiguous_provider_create

    record = store.load_goal(goal_id)
    if record.get("schema_version") != GOAL_SCHEMA_VERSION_V4:
        raise StateConflict(
            "uninterrupted coordination rejects legacy or manual goal state"
        )
    phase = record["state"]["phase"]
    generation = int(record["state"]["current_generation"])
    if phase == "terminal_complete":
        report = record.get("completion_report")
        if (
            record["state"]["goal_evaluation"] != "met"
            or not isinstance(report, Mapping)
        ):
            raise IntegrityError(
                "terminal completion lacks canonical met evidence and report"
            )
        return CoordinatorAdvance(
            "goal_reached",
            "goal.met",
            goal_id,
            int(record["state"]["revision"]),
            generation,
            completion_report_sha256=content_sha256(report),
        )
    if phase == "terminal_cancelled":
        return CoordinatorAdvance(
            "cancelled",
            "goal.cancelled",
            goal_id,
            int(record["state"]["revision"]),
            generation,
        )
    if phase in {
        "terminal_awaiting_human",
        "terminal_policy_limit",
        "terminal_integrity_incident",
    }:
        return CoordinatorAdvance(
            "suspended_safeguard",
            str(record["state"].get("terminal_reason") or "goal.hard_safeguard"),
            goal_id,
            int(record["state"]["revision"]),
            generation,
        )
    if phase == "recovery_pending":
        entry = record["generations"].get(str(generation), {})
        if entry.get("terminal_or_successor_outcome") in {"ambiguous", "timeout"}:
            reconciled = reconcile_ambiguous_provider_create(
                store,
                goal_id=goal_id,
                expected_revision=record["state"]["revision"],
                generation=generation,
                provider=provider,
                timestamp=timestamp,
            )
            if reconciled["state"]["phase"] == "successor_created":
                reconciled = _set_coordinator(
                    store,
                    reconciled,
                    status="worker_active",
                    worker_thread_id=reconciled["generations"][str(generation)][
                        "successor_thread_id"
                    ],
                    timestamp=timestamp,
                )
                return CoordinatorAdvance(
                    "worker_active",
                    "goal.provider_unique_successor_adopted",
                    goal_id,
                    int(reconciled["state"]["revision"]),
                    generation,
                    reconciled["generations"][str(generation)][
                        "successor_thread_id"
                    ],
                )
            return CoordinatorAdvance(
                "suspended_safeguard",
                str(
                    reconciled["state"].get("terminal_reason")
                    or "goal.provider_reconciliation_unresolved"
                ),
                goal_id,
                int(reconciled["state"]["revision"]),
                generation,
            )
        return CoordinatorAdvance(
            "suspended_safeguard",
            "goal.consumed_outcome_recovery_required",
            goal_id,
            int(record["state"]["revision"]),
            generation,
        )
    if phase in {"initialized", "continuation_required", "successor_intent"}:
        predecessor = record["coordinator"].get("current_worker_thread_id") or record[
            "coordinator"
        ]["thread_id"]
        return _dispatch_current_intent(
            store,
            record=record,
            provider=provider,
            predecessor_thread_id=predecessor,
            timestamp=timestamp,
        )
    if phase in {"successor_created", "step_active", "step_verifying", "step_verified"}:
        entry = record["generations"].get(str(generation), {})
        worker = entry.get("successor_thread_id") or record["coordinator"].get(
            "current_worker_thread_id"
        )
        return CoordinatorAdvance(
            "worker_active",
            "goal.worker_active",
            goal_id,
            int(record["state"]["revision"]),
            generation,
            worker,
        )
    raise IntegrityError(f"unhandled v4 goal phase: {phase}")


def run_to_goal(
    store: Any,
    *,
    goal_id: str,
    provider: Any,
    worker_driver: Callable[[CoordinatorAdvance], None] | None = None,
) -> CoordinatorAdvance:
    """Remain active until canonical success or one lawful hard safeguard."""

    last_observation: tuple[str, int] | None = None
    while True:
        result = advance_once(store, goal_id=goal_id, provider=provider)
        if result.status in {
            "goal_reached",
            "cancelled",
            "suspended_safeguard",
        }:
            return result
        if result.status == "provider_recovery":
            continue
        if result.status in {"worker_dispatched", "worker_active"}:
            if worker_driver is not None:
                worker_driver(result)
                continue
            wait = getattr(provider, "wait_for_terminal", None)
            if not callable(wait) or result.worker_thread_id is None:
                record = store.load_goal(goal_id)
                _set_coordinator(
                    store,
                    record,
                    status="suspended_safeguard",
                    worker_thread_id=result.worker_thread_id,
                )
                return CoordinatorAdvance(
                    "suspended_safeguard",
                    "goal.provider_wait_unavailable",
                    goal_id,
                    int(record["state"]["revision"]) + 1,
                    result.generation,
                    result.worker_thread_id,
                )
            try:
                observed = wait(result.worker_thread_id)
            except Exception as error:
                record = store.load_goal(goal_id)
                fresh = _set_coordinator(
                    store,
                    record,
                    status="suspended_safeguard",
                    worker_thread_id=result.worker_thread_id,
                    wakeup={
                        "status": "ambiguous",
                        "wakeup_id": _stable_id(
                            "GCW-",
                            {
                                "goal_id": goal_id,
                                "generation": result.generation,
                                "worker_thread_id": result.worker_thread_id,
                            },
                        ),
                    },
                )
                resume = getattr(provider, "resume_thread", None)
                if callable(resume):
                    try:
                        resume(
                            fresh["coordinator"]["thread_id"],
                            "Resume the same interrupted goal coordinator from canonical "
                            "v4 state. Do not ask the user to say continue.",
                        )
                    except Exception:
                        pass
                return CoordinatorAdvance(
                    "suspended_safeguard",
                    f"goal.provider_wait_ambiguous.{type(error).__name__}",
                    goal_id,
                    int(fresh["state"]["revision"]),
                    result.generation,
                    result.worker_thread_id,
                )
            if not isinstance(observed, Mapping):
                raise IntegrityError("ThreadProvider wait returned non-object evidence")
            if observed.get("terminal") is not True:
                continue
            key = (result.worker_thread_id, result.goal_revision)
            if last_observation == key:
                record = store.load_goal(goal_id)
                if record["state"]["revision"] == result.goal_revision:
                    fresh = _set_coordinator(
                        store,
                        record,
                        status="suspended_safeguard",
                        worker_thread_id=result.worker_thread_id,
                    )
                    return CoordinatorAdvance(
                        "suspended_safeguard",
                        "goal.terminal_worker_receipt_missing",
                        goal_id,
                        int(fresh["state"]["revision"]),
                        result.generation,
                        result.worker_thread_id,
                    )
            last_observation = key
            continue


def notify_coordinator(
    store: Any,
    *,
    goal_id: str,
    generation: int,
    worker_thread_id: str,
    step_receipt_sha256: str,
    provider: Any,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Persist and deliver an idempotent worker-to-coordinator wakeup."""

    record = store.load_goal(goal_id)
    if record.get("schema_version") != GOAL_SCHEMA_VERSION_V4:
        return {"status": "legacy_no_wakeup", "goal_id": goal_id}
    now = timestamp or utc_now()
    basis = {
        "goal_id": goal_id,
        "generation": generation,
        "worker_thread_id": worker_thread_id,
        "coordinator_thread_id": record["coordinator"]["thread_id"],
        "step_receipt_sha256": step_receipt_sha256,
    }
    wakeup_id = _stable_id("GCW-", basis)
    pending = _set_coordinator(
        store,
        record,
        status=record["coordinator"]["status"],
        worker_thread_id=record["coordinator"].get("current_worker_thread_id"),
        last_worker_receipt_sha256=step_receipt_sha256,
        wakeup={"status": "pending", "wakeup_id": wakeup_id},
        timestamp=now,
    )
    resume = getattr(provider, "resume_thread", None)
    try:
        if not callable(resume):
            raise BootstrapRequired(
                "continuous provider cannot resume the coordinator",
                details={"reason_code": "goal.continuous_provider_unavailable"},
            )
        response = resume(
            pending["coordinator"]["thread_id"],
            "A goal worker finalized canonical state. Resume this same v4 "
            "coordinator automatically and continue until the goal is met. "
            "Do not ask the user to say continue.",
        )
    except Exception:
        final = _set_coordinator(
            store,
            pending,
            status="suspended_safeguard",
            worker_thread_id=pending["coordinator"].get(
                "current_worker_thread_id"
            ),
            wakeup={"status": "ambiguous", "wakeup_id": wakeup_id},
            timestamp=now,
        )
        return {
            "schema_version": "sys4ai.goal-coordinator-wakeup-summary.v1",
            "status": "ambiguous",
            "goal_id": goal_id,
            "wakeup_id": wakeup_id,
            "goal_revision": final["state"]["revision"],
        }
    final = _set_coordinator(
        store,
        pending,
        status=pending["coordinator"]["status"],
        worker_thread_id=pending["coordinator"].get("current_worker_thread_id"),
        wakeup={"status": "delivered", "wakeup_id": wakeup_id},
        timestamp=now,
    )
    return {
        "schema_version": "sys4ai.goal-coordinator-wakeup-summary.v1",
        "status": "delivered",
        "goal_id": goal_id,
        "wakeup_id": wakeup_id,
        "provider_response_sha256": content_sha256(response),
        "goal_revision": final["state"]["revision"],
    }
