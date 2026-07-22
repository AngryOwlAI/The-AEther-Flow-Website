"""Fresh-discussion provider boundary for the plan-native relay."""

from __future__ import annotations

import copy
import hashlib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any, Protocol

from agentjob_runtime.errors import RecordValidationError, StateConflict
from agentjob_runtime.plan.relay import RelayStore


@dataclass(frozen=True)
class RelayProviderCapabilities:
    create_thread: bool
    read_thread: bool
    query_by_idempotency_key: bool
    current_thread_identity: bool
    same_project_evidence: bool
    bound_checkout_evidence: bool
    requested_and_effective_effort: bool
    wait_for_terminal: bool = False
    resume_thread: bool = False
    mode: str = "automatic"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def automatic_ready(self) -> bool:
        return all(
            (
                self.create_thread,
                self.read_thread,
                self.query_by_idempotency_key,
                self.current_thread_identity,
                self.same_project_evidence,
                self.bound_checkout_evidence,
                self.requested_and_effective_effort,
            )
        ) and self.mode == "automatic"


class RelayThreadProvider(Protocol):
    def capabilities(self) -> RelayProviderCapabilities: ...

    def create_thread(
        self,
        *,
        project_id: str,
        checkout_id: str,
        requested_effort: str,
        idempotency_key: str,
        prompt: str,
    ) -> Mapping[str, Any]: ...

    def query_by_idempotency_key(self, key: str) -> Sequence[Mapping[str, Any]]: ...


class ProviderCreateNotAttempted(RuntimeError):
    """Provider proof that failure occurred before any external create effect."""


class CallbackRelayThreadProvider:
    """Concrete provider adapter over injected create/query API callables."""

    def __init__(
        self,
        *,
        create: Callable[..., Mapping[str, Any]],
        query: Callable[[str], Sequence[Mapping[str, Any]]],
        capability_report: RelayProviderCapabilities | None = None,
    ) -> None:
        self._create = create
        self._query = query
        self._capabilities = capability_report or RelayProviderCapabilities(
            create_thread=True,
            read_thread=True,
            query_by_idempotency_key=True,
            current_thread_identity=True,
            same_project_evidence=True,
            bound_checkout_evidence=True,
            requested_and_effective_effort=True,
        )

    def capabilities(self) -> RelayProviderCapabilities:
        return self._capabilities

    def create_thread(self, **kwargs: Any) -> Mapping[str, Any]:
        return copy.deepcopy(dict(self._create(**kwargs)))

    def query_by_idempotency_key(self, key: str) -> Sequence[Mapping[str, Any]]:
        return [copy.deepcopy(dict(item)) for item in self._query(key)]


class ManualRelayThreadProvider:
    """Truthful degraded transport; it never claims an automatic create."""

    def capabilities(self) -> RelayProviderCapabilities:
        return RelayProviderCapabilities(
            create_thread=False,
            read_thread=False,
            query_by_idempotency_key=False,
            current_thread_identity=False,
            same_project_evidence=False,
            bound_checkout_evidence=False,
            requested_and_effective_effort=False,
            mode="degraded_manual",
        )

    def create_thread(self, **kwargs: Any) -> Mapping[str, Any]:
        raise StateConflict("automatic provider create is unavailable in degraded_manual mode")

    def query_by_idempotency_key(self, key: str) -> Sequence[Mapping[str, Any]]:
        raise StateConflict("automatic provider query is unavailable in degraded_manual mode")


def _verify_response(
    response: Mapping[str, Any],
    *,
    project_id: str,
    checkout_id: str,
    requested_effort: str,
    idempotency_key: str,
) -> dict[str, Any]:
    value = copy.deepcopy(dict(response))
    required = {
        "thread_id": str,
        "project_id": str,
        "checkout_id": str,
        "requested_effort": str,
        "effective_effort": str,
        "idempotency_key": str,
    }
    for field, expected_type in required.items():
        if not isinstance(value.get(field), expected_type) or not value[field]:
            raise RecordValidationError(f"provider response lacks nonblank {field}")
    mismatches = []
    for field, expected in (
        ("project_id", project_id),
        ("checkout_id", checkout_id),
        ("requested_effort", requested_effort),
        ("effective_effort", requested_effort),
        ("idempotency_key", idempotency_key),
    ):
        if value[field] != expected:
            mismatches.append(field)
    if mismatches:
        raise StateConflict(
            "provider response identity differs from the committed intent",
            details={"reason_code": "relay.provider_identity_mismatch", "fields": mismatches},
        )
    return value


def dispatch_generation(
    store: RelayStore,
    provider: RelayThreadProvider,
    *,
    run_id: str,
    generation: int,
    expected_revision: int,
    repository_fingerprint: str,
    control_fingerprint: str,
    owner_token: str,
    current_thread_id: str,
    project_id: str,
    checkout_id: str,
    requested_effort: str,
    prompt: str,
) -> dict[str, Any]:
    """Perform the sole provider create between two explicit state commits."""

    capabilities = provider.capabilities()
    if not capabilities.automatic_ready:
        return {
            "status": "degraded_manual",
            "automatic_continuity": False,
            "capabilities": capabilities.as_dict(),
            "handoff_packet": {
                "run_id": run_id,
                "generation": generation,
                "project_id": project_id,
                "checkout_id": checkout_id,
                "requested_effort": requested_effort,
                "prompt_sha256": hashlib.sha256(
                    prompt.encode("utf-8")
                ).hexdigest(),
                "raw_prompt_included": False,
                "raw_token_included": False,
            },
            "next_safe_action": "adopt-successor-after-human-verification",
        }
    started = store.begin_dispatch(
        run_id,
        generation,
        expected_revision=expected_revision,
        repository_fingerprint=repository_fingerprint,
        control_fingerprint=control_fingerprint,
        owner_token=owner_token,
        current_thread_id=current_thread_id,
    )
    if started["status"] == "already_creating":
        return {
            **started,
            "next_safe_action": "reconcile-dispatch",
            "provider_create_called": False,
        }
    try:
        raw = provider.create_thread(
            project_id=project_id,
            checkout_id=checkout_id,
            requested_effort=requested_effort,
            idempotency_key=started["idempotency_key"],
            prompt=prompt,
        )
    except ProviderCreateNotAttempted as error:
        return store.record_protected_stop(
            run_id,
            generation,
            expected_revision=started["revision"],
            repository_fingerprint=repository_fingerprint,
            control_fingerprint=control_fingerprint,
            current_thread_id=current_thread_id,
            handoff_token=owner_token,
            disposition="capability_blocked",
            reason_code="relay.provider_create_not_attempted",
            evidence={
                "provider_exception_type": type(error).__name__,
                "boundary": "before_create",
                "effect_not_attempted": True,
            },
        )
    except BaseException as error:
        return store.mark_dispatch_ambiguous(
            run_id,
            generation,
            expected_revision=started["revision"],
            repository_fingerprint=repository_fingerprint,
            control_fingerprint=control_fingerprint,
            owner_token=owner_token,
            current_thread_id=current_thread_id,
            evidence={"provider_exception_type": type(error).__name__, "boundary": "create_outcome_unknown"},
        )
    response = _verify_response(
        raw,
        project_id=project_id,
        checkout_id=checkout_id,
        requested_effort=requested_effort,
        idempotency_key=started["idempotency_key"],
    )
    return store.record_successor(
        run_id,
        generation,
        expected_revision=started["revision"],
        repository_fingerprint=repository_fingerprint,
        control_fingerprint=control_fingerprint,
        owner_token=owner_token,
        current_thread_id=current_thread_id,
        child_thread_id=response["thread_id"],
        provider_response=response,
        effective_effort=response["effective_effort"],
    )


def reconcile_generation_dispatch(
    store: RelayStore,
    provider: RelayThreadProvider,
    *,
    idempotency_key: str,
    project_id: str,
    checkout_id: str,
    requested_effort: str,
    **store_arguments: Any,
) -> dict[str, Any]:
    capabilities = provider.capabilities()
    if not capabilities.query_by_idempotency_key:
        return {
            "status": "human_gate",
            "reason_code": "relay.provider_query_capability_missing",
            "child_created": False,
        }
    raw_matches = provider.query_by_idempotency_key(idempotency_key)
    matches = [
        _verify_response(
            item,
            project_id=project_id,
            checkout_id=checkout_id,
            requested_effort=requested_effort,
            idempotency_key=idempotency_key,
        )
        for item in raw_matches
    ]
    return store.reconcile_dispatch(matches=matches, **store_arguments)
