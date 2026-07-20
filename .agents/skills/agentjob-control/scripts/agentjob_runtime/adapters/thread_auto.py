"""Deterministic ThreadProvider capability selection with manual fallback."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from agentjob_runtime.errors import BootstrapRequired, RecordValidationError
from agentjob_runtime.goal.launcher import ThreadCreateResult


@dataclass(frozen=True)
class ThreadProviderReport:
    provider_id: str
    available: bool
    automatic: bool
    strategies: tuple[str, ...]
    operations: tuple[str, ...]
    protocol_idempotency: bool
    reason_code: str | None = None
    supported_reasoning_efforts: tuple[str, ...] = ()
    can_configure_current_thread: bool = False
    can_create_with_reasoning_effort: bool = False
    can_verify_effective_reasoning_effort: bool = False
    can_reconfigure_unclaimed_successor: bool = False
    supported_environment_modes: tuple[str, ...] = ()
    can_reuse_bound_checkout: bool = False
    can_create_worktree: bool = False
    can_query_by_idempotency_key: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "available": self.available,
            "automatic": self.automatic,
            "strategies": list(self.strategies),
            "operations": list(self.operations),
            "protocol_idempotency": self.protocol_idempotency,
            "reason_code": self.reason_code,
            "supported_reasoning_efforts": list(
                self.supported_reasoning_efforts
            ),
            "can_configure_current_thread": self.can_configure_current_thread,
            "can_create_with_reasoning_effort": self.can_create_with_reasoning_effort,
            "can_verify_effective_reasoning_effort": self.can_verify_effective_reasoning_effort,
            "can_reconfigure_unclaimed_successor": self.can_reconfigure_unclaimed_successor,
            "supported_environment_modes": list(self.supported_environment_modes),
            "can_reuse_bound_checkout": self.can_reuse_bound_checkout,
            "can_create_worktree": self.can_create_worktree,
            "can_query_by_idempotency_key": self.can_query_by_idempotency_key,
        }


@dataclass(frozen=True)
class ThreadSelectionReport:
    configured_provider: str
    selected_provider: str
    strategy: str
    mode: str
    fallback_used: bool
    providers: tuple[ThreadProviderReport, ...]
    execution_performed: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "configured_provider": self.configured_provider,
            "selected_provider": self.selected_provider,
            "strategy": self.strategy,
            "mode": self.mode,
            "fallback_used": self.fallback_used,
            "providers": [item.as_dict() for item in self.providers],
            "execution_performed": self.execution_performed,
        }


def inspect_thread_provider(provider: Any) -> ThreadProviderReport:
    provider_id = str(getattr(provider, "provider_id", ""))
    if not provider_id:
        raise RecordValidationError("ThreadProvider must declare a provider_id")
    try:
        raw = provider.capabilities() if callable(getattr(provider, "capabilities", None)) else {}
    except Exception as error:
        return ThreadProviderReport(
            provider_id,
            False,
            False,
            (),
            (),
            False,
            f"provider.capability_error.{type(error).__name__}",
        )
    capabilities = dict(raw) if isinstance(raw, Mapping) else {}
    available = capabilities.get("available", getattr(provider, "available", False)) is True
    automatic = capabilities.get("automatic", provider_id != "manual-handoff") is True
    strategies = tuple(str(item) for item in capabilities.get("strategies", ("fresh_summary",)))
    operations = tuple(str(item) for item in capabilities.get("operations", ("create",)))
    return ThreadProviderReport(
        provider_id,
        available,
        automatic,
        strategies,
        operations,
        capabilities.get("protocol_idempotency") is True,
        None if available else str(capabilities.get("reason_code") or "provider.unavailable"),
        tuple(
            str(item)
            for item in capabilities.get("supported_reasoning_efforts", ())
        ),
        capabilities.get("can_configure_current_thread") is True,
        capabilities.get("can_create_with_reasoning_effort") is True,
        capabilities.get("can_verify_effective_reasoning_effort") is True,
        capabilities.get("can_reconfigure_unclaimed_successor") is True,
        tuple(
            str(item)
            for item in capabilities.get("supported_environment_modes", ())
        ),
        capabilities.get("can_reuse_bound_checkout") is True,
        capabilities.get("can_create_worktree") is True,
        capabilities.get("can_query_by_idempotency_key") is True,
    )


class SelectedThreadProvider:
    """Delegate provider calls while retaining selection evidence in receipts."""

    def __init__(self, provider: Any, report: ThreadSelectionReport) -> None:
        self.delegate = provider
        self.selection = report
        self.provider_id = str(provider.provider_id)
        self.available = True

    def capabilities(self) -> Mapping[str, Any]:
        selected = next(
            item for item in self.selection.providers if item.provider_id == self.provider_id
        )
        return selected.as_dict()

    def create_thread(
        self,
        *,
        prompt: str,
        envelope: Mapping[str, Any],
        idempotency_key: str,
        execution_profile: Mapping[str, Any],
    ) -> ThreadCreateResult:
        result = self.delegate.create_thread(
            prompt=prompt,
            envelope=envelope,
            idempotency_key=idempotency_key,
            execution_profile=execution_profile,
        )
        response = copy.deepcopy(dict(result.response))
        response["provider_selection"] = self.selection.as_dict()
        return ThreadCreateResult(result.status, result.successor_thread_id, response)

    def configure_current_thread(
        self, thread_id: str, *, reasoning_effort: str
    ) -> Mapping[str, Any]:
        return self.delegate.configure_current_thread(
            thread_id, reasoning_effort=reasoning_effort
        )

    def read_thread_profile(self, thread_id: str) -> Mapping[str, Any]:
        return self.delegate.read_thread_profile(thread_id)

    def reconfigure_unclaimed_successor(
        self, thread_id: str, *, reasoning_effort: str
    ) -> Mapping[str, Any]:
        return self.delegate.reconfigure_unclaimed_successor(
            thread_id, reasoning_effort=reasoning_effort
        )

    def query_by_idempotency_key(
        self, idempotency_key: str
    ) -> Mapping[str, Any]:
        return self.delegate.query_by_idempotency_key(idempotency_key)


def select_thread_provider(
    *,
    configured_provider: str,
    strategy: str,
    providers: Sequence[Any],
    manual_provider: Any | None = None,
    require_automatic: bool = False,
) -> SelectedThreadProvider:
    """Select only from an explicit ordered provider list; never infer host tools."""

    if strategy not in {"fresh_summary", "fork_history", "manual_new_thread"}:
        raise RecordValidationError(f"unsupported thread strategy: {strategy}")
    candidates = list(providers)
    if manual_provider is not None and all(
        getattr(item, "provider_id", None) != getattr(manual_provider, "provider_id", None)
        for item in candidates
    ):
        candidates.append(manual_provider)
    reports = tuple(inspect_thread_provider(item) for item in candidates)
    by_id = {report.provider_id: (provider, report) for provider, report in zip(candidates, reports)}
    selected: tuple[Any, ThreadProviderReport] | None = None
    fallback = False
    if configured_provider != "auto":
        candidate = by_id.get(configured_provider)
        if candidate and candidate[1].available and strategy in candidate[1].strategies:
            selected = candidate
        else:
            fallback = True
    else:
        selected = next(
            (
                (provider, report)
                for provider, report in zip(candidates, reports)
                if report.available
                and report.automatic
                and strategy in report.strategies
            ),
            None,
        )
        fallback = selected is None
    if selected is None and manual_provider is not None:
        manual = by_id.get(str(manual_provider.provider_id))
        if manual and manual[1].available and strategy in manual[1].strategies:
            selected = manual
    if selected is None:
        raise BootstrapRequired(
            "no safe ThreadProvider is available",
            details={
                "reason_code": "thread_provider.safe_provider_unavailable",
                "configured_provider": configured_provider,
                "strategy": strategy,
                "providers": [item.as_dict() for item in reports],
            },
        )
    provider, provider_report = selected
    if (
        provider_report.can_create_with_reasoning_effort is not True
        or provider_report.can_verify_effective_reasoning_effort is not True
        or provider_report.can_reuse_bound_checkout is not True
    ):
        raise BootstrapRequired(
            "selected ThreadProvider cannot preserve the accepted execution profile",
            details={
                "reason_code": "thread_provider.execution_profile_unavailable",
                "selected_provider": provider_report.provider_id,
                "strategy": strategy,
            },
        )
    if strategy == "fork_history" and (
        "fork_history" not in provider_report.strategies
        or provider_report.can_create_with_reasoning_effort is not True
    ):
        raise BootstrapRequired(
            "fork_history cannot guarantee the accepted initial effort",
            details={
                "reason_code": "thread_provider.fork_profile_unavailable",
                "selected_provider": provider_report.provider_id,
            },
        )
    if require_automatic and not provider_report.automatic:
        raise BootstrapRequired(
            "automatic recursion was required but only manual handoff is available",
            details={
                "reason_code": "thread_provider.automatic_unavailable",
                "selected_provider": provider_report.provider_id,
            },
        )
    report = ThreadSelectionReport(
        configured_provider,
        provider_report.provider_id,
        strategy,
        "automatic" if provider_report.automatic else "manual",
        fallback or configured_provider != provider_report.provider_id,
        reports,
    )
    return SelectedThreadProvider(provider, report)
