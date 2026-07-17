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

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "available": self.available,
            "automatic": self.automatic,
            "strategies": list(self.strategies),
            "operations": list(self.operations),
            "protocol_idempotency": self.protocol_idempotency,
            "reason_code": self.reason_code,
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
        self, *, prompt: str, envelope: Mapping[str, Any], idempotency_key: str
    ) -> ThreadCreateResult:
        result = self.delegate.create_thread(
            prompt=prompt,
            envelope=envelope,
            idempotency_key=idempotency_key,
        )
        response = copy.deepcopy(dict(result.response))
        response["provider_selection"] = self.selection.as_dict()
        return ThreadCreateResult(result.status, result.successor_thread_id, response)


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
