"""Optional navigation-only context provider boundary."""

from __future__ import annotations

import copy
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.config import resolve_project_path
from agentjob_runtime.errors import RecordValidationError


@dataclass(frozen=True)
class ContextQuery:
    text: str
    purpose: str
    max_results: int = 10

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ContextHit:
    hit_id: str
    provider_id: str
    summary: str
    canonical_ref: str | None
    canonical_sha256: str | None
    cache_id: str | None
    influences_routing: bool
    stale: bool
    canonical_verified: bool
    rejection_reason: str | None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ContextInspection:
    status: str
    provider_id: str | None
    required: bool
    hits: tuple[ContextHit, ...]
    warnings: tuple[str, ...]
    reason_code: str | None
    authority_effect: str = "navigation_only"
    may_select_job: bool = False
    may_complete_job: bool = False
    control_state_mutated: bool = False

    @property
    def blocking(self) -> bool:
        return self.status == "blocked"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_context(
    project_root: str | Path,
    *,
    provider: Any | None,
    query: ContextQuery,
    required: bool = False,
) -> ContextInspection:
    """Inspect context hints and verify influential hits against canonical files."""

    root = Path(project_root).expanduser().resolve()
    if provider is None:
        return ContextInspection(
            "blocked" if required else "optional_unavailable",
            None,
            required,
            (),
            ("No context provider is configured.",),
            "context.required_provider_unavailable"
            if required
            else "context.optional_provider_unavailable",
        )
    provider_id = str(getattr(provider, "provider_id", "unknown"))
    try:
        available = provider.available()
    except Exception:
        available = False
    if available is not True:
        return ContextInspection(
            "blocked" if required else "optional_unavailable",
            provider_id,
            required,
            (),
            ("Configured context provider is unavailable.",),
            "context.required_provider_unavailable"
            if required
            else "context.optional_provider_unavailable",
        )
    try:
        raw_hits = provider.search(query.as_dict())
    except Exception as error:
        return ContextInspection(
            "blocked" if required else "optional_unavailable",
            provider_id,
            required,
            (),
            (f"Context provider raised {type(error).__name__}.",),
            "context.required_provider_failed"
            if required
            else "context.optional_provider_failed",
        )
    if not isinstance(raw_hits, Sequence) or isinstance(raw_hits, (str, bytes)):
        raise RecordValidationError("context provider search must return a sequence")
    hits: list[ContextHit] = []
    warnings: list[str] = []
    influential_unverified = False
    for index, raw in enumerate(raw_hits[: query.max_results]):
        if not isinstance(raw, Mapping):
            raise RecordValidationError("context hits must be mappings")
        hit_id = str(raw.get("hit_id") or f"hit-{index + 1}")
        summary = str(raw.get("summary") or "")
        canonical_ref = str(raw["canonical_ref"]) if raw.get("canonical_ref") else None
        expected_hash = (
            str(raw["canonical_sha256"]) if raw.get("canonical_sha256") else None
        )
        cache_id = str(raw["cache_id"]) if raw.get("cache_id") else None
        influential = raw.get("influences_routing") is True
        stale = raw.get("stale") is True
        verified = False
        rejection: str | None = None
        if stale:
            rejection = "context.stale_cache_hit"
        elif canonical_ref is None or expected_hash is None:
            rejection = "context.canonical_reference_missing"
        else:
            try:
                source = resolve_project_path(
                    root, canonical_ref, purpose="context canonical source"
                )
                verified = source.is_file() and _sha256(source) == expected_hash
                if not verified:
                    rejection = "context.canonical_hash_mismatch"
            except Exception:
                rejection = "context.canonical_reference_invalid"
        if rejection:
            warnings.append(f"{hit_id}:{rejection}")
        if influential and not verified:
            influential_unverified = True
        hits.append(
            ContextHit(
                hit_id,
                provider_id,
                summary,
                canonical_ref,
                expected_hash,
                cache_id,
                influential,
                stale,
                verified,
                rejection,
            )
        )
    if influential_unverified and required:
        status = "blocked"
        reason = "context.influential_source_unverified"
    elif warnings:
        status = "ready_with_warnings"
        reason = "context.unverified_hits_ignored"
    else:
        status = "ready"
        reason = None
    return ContextInspection(
        status,
        provider_id,
        required,
        tuple(hits),
        tuple(warnings),
        reason,
    )


def context_fingerprint_payload(
    inspection: ContextInspection,
    *,
    policy_declares_context_canonical: bool = False,
    policy_declares_cache_ids_canonical: bool = False,
) -> Mapping[str, Any]:
    """Exclude context by default; include only explicitly promoted evidence."""

    if not policy_declares_context_canonical:
        return {}
    verified = [item for item in inspection.hits if item.canonical_verified]
    payload: dict[str, Any] = {
        "canonical_sources": [
            {"canonical_ref": item.canonical_ref, "canonical_sha256": item.canonical_sha256}
            for item in verified
        ]
    }
    if policy_declares_cache_ids_canonical:
        payload["cache_ids"] = [item.cache_id for item in verified if item.cache_id]
    return copy.deepcopy(payload)
