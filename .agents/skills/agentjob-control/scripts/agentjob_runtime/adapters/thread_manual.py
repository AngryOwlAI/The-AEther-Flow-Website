"""Project-local manual handoff ThreadProvider and explicit adoption."""

from __future__ import annotations

import copy
import hashlib
import os
import stat
import tempfile
from pathlib import Path
from typing import Any, Mapping

from agentjob_runtime.config import FORBIDDEN_STATE_ROOTS
from agentjob_runtime.errors import IntegrityError, RecordValidationError, SecurityError, StateConflict
from agentjob_runtime.goal.launcher import ThreadCreateResult
from agentjob_runtime.goal.model import utc_now
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore
from agentjob_runtime.goal.successor import record_successor
from agentjob_runtime.plan.launcher import _final_provider_intent
from agentjob_runtime.plan.lifecycle import holder_token_sha256
from agentjob_runtime.plan.sqlite_store import SQLitePlanStore
from agentjob_runtime.records.canonical import content_sha256, load_structured, render_canonical_json
from agentjob_runtime.validation.schema import format_issues, validate_instance


def _safe_root(project_root: Path, local_root: str | Path) -> Path:
    supplied = Path(local_root)
    if supplied.is_absolute() or ".." in supplied.parts:
        raise SecurityError("manual handoff root must be project-relative")
    root = (project_root / supplied).resolve(strict=False)
    try:
        relative = root.relative_to(project_root).as_posix()
    except ValueError as error:
        raise SecurityError("manual handoff root escapes the project") from error
    if any(relative == value or relative.startswith(f"{value}/") for value in FORBIDDEN_STATE_ROOTS):
        raise SecurityError("manual handoff state cannot live in an installed package")
    current = project_root
    for part in Path(relative).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise SecurityError("manual handoff root traverses a symlink")
    return root


def _assert_regular(path: Path) -> None:
    if path.is_symlink():
        raise SecurityError(f"manual handoff file cannot be a symlink: {path}")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise SecurityError(f"manual handoff file has an unsafe alias: {path}")


def _atomic_write(path: Path, payload: bytes, *, allow_identical: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.parent
    while current != current.parent:
        if current.is_symlink():
            raise SecurityError(f"manual handoff path traverses a symlink: {current}")
        current = current.parent
    if path.exists():
        _assert_regular(path)
        if allow_identical and path.read_bytes() == payload:
            return
        raise IntegrityError(f"manual handoff artifact already exists: {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
    finally:
        if temporary.exists():
            temporary.unlink()


def _validate_envelope(envelope: Mapping[str, Any]) -> dict[str, Any]:
    value = dict(envelope)
    version = value.get("schema_version")
    if version == "sys4ai.continuation-envelope.v1":
        schema = (
            Path(__file__).resolve().parents[3]
            / "schemas"
            / "continuation-envelope.schema.json"
        )
    elif version == "sys4ai.continuation-envelope.v2":
        schema = (
            Path(__file__).resolve().parents[3]
            / "schemas"
            / "continuation-envelope-v2.schema.json"
        )
    elif version == "sys4ai.continuation-envelope.v3":
        schema = (
            Path(__file__).resolve().parents[3]
            / "schemas"
            / "continuation-envelope-v3.schema.json"
        )
    elif version == "sys4ai.plan-task-envelope.v1":
        schema = (
            Path(__file__).resolve().parents[4]
            / "implementation-plan-goal"
            / "schemas"
            / "plan-task-envelope.schema.json"
        )
    elif version == "sys4ai.plan-task-envelope.v2":
        schema = (
            Path(__file__).resolve().parents[4]
            / "implementation-plan-goal"
            / "schemas"
            / "plan-task-envelope-v2.schema.json"
        )
    else:
        raise RecordValidationError(
            "manual handoff envelope profile is unsupported"
        )
    issues = validate_instance(value, schema)
    if issues:
        raise RecordValidationError(
            "manual handoff envelope failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    return value


class ManualThreadProvider:
    provider_id = "manual-handoff"
    available = True

    def __init__(
        self,
        project_root: str | Path,
        *,
        local_root: str | Path = ".local/sys4ai/continuation/manual",
        current_thread_id: str | None = None,
        timestamp: str | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        if not self.project_root.is_dir():
            raise RecordValidationError("manual handoff project root must exist")
        self.root = _safe_root(self.project_root, local_root)
        self.current_thread_id = current_thread_id
        self.timestamp = timestamp

    def capabilities(self) -> Mapping[str, Any]:
        return {
            "provider_id": self.provider_id,
            "available": True,
            "automatic": False,
            "strategies": ["manual_new_thread", "fresh_summary"],
            "operations": ["write_handoff", "explicit_adoption"],
            "protocol_idempotency": False,
            "supported_reasoning_efforts": [
                "minimal",
                "low",
                "medium",
                "high",
                "xhigh",
                "max",
            ],
            "can_configure_current_thread": False,
            "can_create_with_reasoning_effort": True,
            "can_verify_effective_reasoning_effort": True,
            "can_reconfigure_unclaimed_successor": False,
            "supported_environment_modes": ["reuse_bound_checkout"],
            "can_reuse_bound_checkout": True,
            "can_create_worktree": False,
            "can_query_by_idempotency_key": False,
            "can_wait_for_terminal": False,
            "can_resume_thread": False,
        }

    def _directory(self, envelope: Mapping[str, Any]) -> Path:
        identity = envelope.get("goal_id", envelope.get("plan_id"))
        if not isinstance(identity, str):
            raise RecordValidationError(
                "manual handoff envelope identity is missing"
            )
        generation = int(envelope["generation"])
        if any(
            char
            not in (
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "abcdefghijklmnopqrstuvwxyz"
                "0123456789._:-"
            )
            for char in identity
        ):
            raise SecurityError(
                "manual handoff identity is unsafe for storage"
            )
        return self.root / identity / f"generation-{generation}"

    def create_thread(
        self,
        *,
        prompt: str,
        envelope: Mapping[str, Any],
        idempotency_key: str,
        execution_profile: Mapping[str, Any],
    ) -> ThreadCreateResult:
        value = _validate_envelope(envelope)
        if idempotency_key != value["idempotency_key"]:
            raise StateConflict("manual handoff idempotency key differs from envelope")
        requested_effort = str(execution_profile["reasoning_effort"])
        if value.get("schema_version") in {
            "sys4ai.continuation-envelope.v2",
            "sys4ai.continuation-envelope.v3",
            "sys4ai.plan-task-envelope.v2",
        }:
            if (
                value["execution_profile"]["reasoning_effort"] != requested_effort
                or value["repository_topology_policy"]["environment_mode"]
                != "reuse_bound_checkout"
            ):
                raise StateConflict(
                    "manual handoff profile differs from the accepted envelope"
                )
        directory = self._directory(value)
        plan_profile = value["schema_version"] in {
            "sys4ai.plan-task-envelope.v1",
            "sys4ai.plan-task-envelope.v2",
        }
        envelope_path = directory / (
            "plan-task-envelope.json"
            if plan_profile
            else "continuation-envelope.json"
        )
        prompt_path = directory / "new-thread-prompt.txt"
        receipt_path = directory / "provider-receipt.json"
        envelope_payload = render_canonical_json(value).encode("utf-8")
        prompt_payload = prompt.encode("utf-8")
        common_receipt = {
            "provider_id": self.provider_id,
            "status": "manual_handoff_pending",
            "generation": value["generation"],
            "idempotency_key": idempotency_key,
            "handoff_token_sha256": hashlib.sha256(
                str(value["handoff_token"]).encode("utf-8")
            ).hexdigest(),
            "envelope_sha256": content_sha256(value),
            "predecessor_thread_id": value["predecessor_thread_id"],
            "provider_thread_id": self.current_thread_id,
            "envelope_path": (
                envelope_path.relative_to(self.project_root).as_posix()
            ),
            "prompt_path": (
                prompt_path.relative_to(self.project_root).as_posix()
            ),
            "created_at": self.timestamp or utc_now(),
            "requested_reasoning_effort": requested_effort,
            "environment_mode": "reuse_bound_checkout",
            "repository_binding_sha256": content_sha256(
                value["repository_binding"]
            ),
        }
        if value["schema_version"] == "sys4ai.plan-task-envelope.v2":
            common_receipt["repository_binding_sha256"] = value[
                "repository_binding_sha256"
            ]
        if plan_profile:
            receipt = {
                "schema_version": (
                    "sys4ai.plan-manual-thread-provider-receipt.v2"
                    if value["schema_version"]
                    == "sys4ai.plan-task-envelope.v2"
                    else "sys4ai.plan-manual-thread-provider-receipt.v1"
                ),
                **common_receipt,
                "plan_id": value["plan_id"],
                "plan_sha256": value["plan_sha256"],
                "task_id": value["task_id"],
                "task_sha256": value["task_sha256"],
            }
        else:
            receipt = {
                "schema_version": (
                    "sys4ai.manual-thread-provider-receipt.v1"
                ),
                **common_receipt,
                "goal_id": value["goal_id"],
            }
        receipt_payload = render_canonical_json(receipt).encode("utf-8")
        _atomic_write(envelope_path, envelope_payload, allow_identical=True)
        _atomic_write(prompt_path, prompt_payload, allow_identical=True)
        if receipt_path.exists():
            _assert_regular(receipt_path)
            existing = load_structured(receipt_path)
            if not isinstance(existing, Mapping):
                raise IntegrityError("manual provider receipt is not an object")
            comparable = dict(existing)
            comparable.pop("created_at", None)
            expected = dict(receipt)
            expected.pop("created_at", None)
            if comparable != expected:
                raise IntegrityError("manual provider receipt conflicts with existing intent")
        else:
            _atomic_write(receipt_path, receipt_payload)
        response = {
            "status": "manual_handoff_pending",
            "envelope_path": receipt["envelope_path"],
            "prompt_path": receipt["prompt_path"],
            "receipt_path": receipt_path.relative_to(self.project_root).as_posix(),
            "envelope_sha256": receipt["envelope_sha256"],
            "requested_reasoning_effort": requested_effort,
            "environment_mode": "reuse_bound_checkout",
            "repository_binding_sha256": receipt[
                "repository_binding_sha256"
            ],
        }
        return ThreadCreateResult("manual_pending", None, response)


def adopt_manual_successor(
    store: SQLiteGoalStore,
    *,
    project_root: str | Path,
    local_root: str | Path,
    goal_id: str,
    expected_revision: int,
    generation: int,
    handoff_token: str,
    envelope_sha256: str,
    successor_thread_id: str,
    effective_reasoning_effort: str | None = None,
    profile_evidence_ref: str | None = None,
    observed_repository_binding: Mapping[str, Any] | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Adopt one explicitly created fresh thread using the reserved identity."""

    root = Path(project_root).expanduser().resolve()
    manual_root = _safe_root(root, local_root)
    directory = manual_root / goal_id / f"generation-{generation}"
    envelope_path = directory / "continuation-envelope.json"
    receipt_path = directory / "provider-receipt.json"
    for path in (envelope_path, receipt_path):
        if not path.is_file():
            raise RecordValidationError(f"manual handoff artifact is missing: {path}")
        _assert_regular(path)
    envelope = _validate_envelope(load_structured(envelope_path))
    if envelope["schema_version"] not in {
        "sys4ai.continuation-envelope.v1",
        "sys4ai.continuation-envelope.v2",
        "sys4ai.continuation-envelope.v3",
    }:
        raise StateConflict(
            "generic manual adoption requires a continuation envelope"
        )
    receipt = load_structured(receipt_path)
    if not isinstance(receipt, Mapping):
        raise RecordValidationError("manual provider receipt must be an object")
    if (
        envelope["goal_id"] != goal_id
        or envelope["generation"] != generation
        or envelope["handoff_token"] != handoff_token
        or content_sha256(envelope) != envelope_sha256
        or receipt.get("envelope_sha256") != envelope_sha256
    ):
        raise StateConflict("manual adoption token, generation, goal, or envelope mismatch")
    forbidden_threads = {
        value
        for value in (
            envelope.get("predecessor_thread_id"),
            receipt.get("provider_thread_id"),
        )
        if value
    }
    if not successor_thread_id.strip() or successor_thread_id in forbidden_threads:
        raise StateConflict("manual adoption requires a distinct fresh successor thread")
    provider_response: dict[str, Any] = {
        "status": "manually_adopted",
        "receipt_path": receipt_path.relative_to(root).as_posix(),
        "envelope_sha256": envelope_sha256,
    }
    if envelope["schema_version"] in {
        "sys4ai.continuation-envelope.v2",
        "sys4ai.continuation-envelope.v3",
    }:
        requested = envelope["execution_profile"]["reasoning_effort"]
        observed_binding = copy.deepcopy(
            dict(observed_repository_binding or {})
        )
        if (
            effective_reasoning_effort != requested
            or not profile_evidence_ref
            or observed_binding != envelope["repository_binding"]
        ):
            raise StateConflict(
                "manual v2 adoption requires exact effort and bound-checkout attestation"
            )
        provider_response.update(
            {
                "requested_reasoning_effort": requested,
                "effective_reasoning_effort": effective_reasoning_effort,
                "profile_evidence_ref": profile_evidence_ref,
                "environment_mode": "reuse_bound_checkout",
                "repository_binding_sha256": content_sha256(observed_binding),
            }
        )
    record = record_successor(
        store,
        goal_id=goal_id,
        expected_revision=expected_revision,
        generation=generation,
        handoff_token=handoff_token,
        successor_thread_id=successor_thread_id,
        provider_id="manual-handoff",
        provider_response=provider_response,
        timestamp=timestamp,
    )
    successor_digest = hashlib.sha256(successor_thread_id.encode("utf-8")).hexdigest()[:16]
    adoption_path = directory / f"adoption-{successor_digest}.json"
    adoption = {
        "schema_version": "sys4ai.manual-thread-adoption.v1",
        "goal_id": goal_id,
        "generation": generation,
        "successor_thread_id": successor_thread_id,
        "envelope_sha256": envelope_sha256,
        "adopted_at": timestamp or utc_now(),
        "reasoning_effort": effective_reasoning_effort,
        "profile_evidence_ref": profile_evidence_ref,
    }
    if adoption_path.exists():
        _assert_regular(adoption_path)
        existing = load_structured(adoption_path)
        if not isinstance(existing, Mapping):
            raise IntegrityError("manual adoption receipt is not an object")
        comparable = dict(existing)
        comparable.pop("adopted_at", None)
        expected = dict(adoption)
        expected.pop("adopted_at", None)
        if comparable != expected:
            raise IntegrityError("manual adoption conflicts with existing receipt")
    else:
        _atomic_write(adoption_path, render_canonical_json(adoption).encode("utf-8"))
    return record


def adopt_manual_plan_successor(
    store: SQLitePlanStore,
    *,
    project_root: str | Path,
    local_root: str | Path,
    plan_id: str,
    expected_revision: int,
    generation: int,
    handoff_token: str,
    envelope_sha256: str,
    successor_thread_id: str,
    effective_reasoning_effort: str,
    profile_evidence_ref: str,
    observed_repository_binding: Mapping[str, Any],
    observed_repository_topology: Mapping[str, Any],
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Adopt one manual plan worker only after exact profile attestation."""

    root = Path(project_root).expanduser().resolve()
    manual_root = _safe_root(root, local_root)
    directory = manual_root / plan_id / f"generation-{generation}"
    envelope_path = directory / "plan-task-envelope.json"
    receipt_path = directory / "provider-receipt.json"
    for path in (envelope_path, receipt_path):
        if not path.is_file():
            raise RecordValidationError(
                f"manual plan handoff artifact is missing: {path}"
            )
        _assert_regular(path)
    envelope = _validate_envelope(load_structured(envelope_path))
    receipt = load_structured(receipt_path)
    if (
        envelope.get("schema_version") != "sys4ai.plan-task-envelope.v2"
        or not isinstance(receipt, Mapping)
        or envelope["plan_id"] != plan_id
        or envelope["generation"] != generation
        or envelope["handoff_token"] != handoff_token
        or content_sha256(envelope) != envelope_sha256
        or receipt.get("envelope_sha256") != envelope_sha256
    ):
        raise StateConflict(
            "manual plan adoption identity or envelope evidence mismatch"
        )
    record = store.load_plan(plan_id)
    intent = store.find_provider_intent(plan_id, generation)
    lease = record["state"].get("lease")
    requested = record["execution_profile"]["reasoning_effort"]
    binding = copy.deepcopy(dict(observed_repository_binding))
    topology = copy.deepcopy(dict(observed_repository_topology))
    if (
        record["state"]["revision"] != expected_revision
        or not isinstance(intent, Mapping)
        or intent["status"] != "intent"
        or intent["finalized"] is not False
        or not isinstance(lease, Mapping)
        or lease["holder_kind"] != "successor_reserved"
        or lease["holder_token_hash"]
        != holder_token_sha256(handoff_token)
        or effective_reasoning_effort != requested
        or not profile_evidence_ref.strip()
        or binding != record["repository_binding"]
        or receipt.get("requested_reasoning_effort") != requested
        or receipt.get("repository_binding_sha256")
        != record["repository_binding_sha256"]
        or topology.get("branch") != binding.get("branch")
        or topology.get("worktree") != binding.get("worktree")
        or any(
            topology.get(field) != binding.get(field)
            for field in ("root", "git_common_dir")
            if field in topology
        )
    ):
        raise StateConflict(
            "manual plan adoption requires exact effort and bound-checkout evidence"
        )
    forbidden = {
        value
        for value in (
            envelope.get("predecessor_thread_id"),
            receipt.get("provider_thread_id"),
        )
        if value
    }
    if (
        not successor_thread_id.strip()
        or successor_thread_id in forbidden
    ):
        raise StateConflict(
            "manual plan adoption requires a distinct fresh thread"
        )
    provider_result = ThreadCreateResult(
        "returned",
        successor_thread_id,
        {
            "status": "manually_adopted",
            "requested_reasoning_effort": requested,
            "effective_reasoning_effort": effective_reasoning_effort,
            "profile_evidence_ref": profile_evidence_ref,
            "environment_mode": "reuse_bound_checkout",
            "repository_binding_sha256": record[
                "repository_binding_sha256"
            ],
            "repository_topology": topology,
            "observed_topology_sha256": content_sha256(topology),
            "same_thread_profile_repair": {
                "attempted": False,
                "thread_id": None,
                "evidence_ref": None,
            },
        },
    )
    outcome, _ = _final_provider_intent(intent, provider_result)
    with store.mutation(
        plan_id,
        expected_revision=expected_revision,
        timestamp=timestamp,
    ) as mutation:
        mutation.finalize_provider_intent(outcome)
        mutation.record_provider_dispatch(
            task_id=str(envelope["task_id"]),
            generation=generation,
            provider_status="returned",
            successor_created=True,
        )
    updated = store.load_plan(plan_id)
    adoption = {
        "schema_version": "sys4ai.plan-manual-thread-adoption.v1",
        "plan_id": plan_id,
        "generation": generation,
        "successor_thread_id": successor_thread_id,
        "envelope_sha256": envelope_sha256,
        "reasoning_effort": effective_reasoning_effort,
        "profile_evidence_ref": profile_evidence_ref,
        "repository_binding_sha256": record[
            "repository_binding_sha256"
        ],
        "observed_topology_sha256": content_sha256(topology),
        "adopted_at": timestamp or utc_now(),
    }
    digest = hashlib.sha256(
        successor_thread_id.encode("utf-8")
    ).hexdigest()[:16]
    adoption_path = directory / f"adoption-{digest}.json"
    _atomic_write(
        adoption_path,
        render_canonical_json(adoption).encode("utf-8"),
        allow_identical=True,
    )
    return updated
