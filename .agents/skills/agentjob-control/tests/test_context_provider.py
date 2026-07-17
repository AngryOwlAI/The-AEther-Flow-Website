from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.adapters.context import (
    ContextQuery,
    context_fingerprint_payload,
    inspect_context,
)


class FakeContextProvider:
    provider_id = "fixture-context"

    def __init__(self, hits=(), *, available=True, raise_error=False):
        self.hits = list(hits)
        self.is_available = available
        self.raise_error = raise_error
        self.calls = 0

    def available(self):
        return self.is_available

    def search(self, query):
        self.calls += 1
        if self.raise_error:
            raise RuntimeError("cache offline")
        return list(self.hits)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ContextProviderTests(unittest.TestCase):
    def test_influential_hit_requires_direct_canonical_source_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / "docs/canonical.md"
            source.parent.mkdir(parents=True)
            source.write_text("Canonical authority.\n", encoding="utf-8")
            provider = FakeContextProvider(
                [
                    {
                        "hit_id": "HIT-1",
                        "summary": "A navigation hint.",
                        "canonical_ref": "docs/canonical.md",
                        "canonical_sha256": digest(source),
                        "cache_id": "CACHE-99",
                        "influences_routing": True,
                        "stale": False,
                    }
                ]
            )
            report = inspect_context(
                root,
                provider=provider,
                query=ContextQuery("authority", "route-navigation"),
                required=True,
            )
            self.assertEqual(report.status, "ready")
            self.assertTrue(report.hits[0].canonical_verified)
            self.assertEqual(report.authority_effect, "navigation_only")
            self.assertFalse(report.may_select_job)
            self.assertFalse(report.may_complete_job)

    def test_stale_or_hash_mismatched_cache_cannot_influence_routing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / "canonical.txt"
            source.write_text("current\n", encoding="utf-8")
            provider = FakeContextProvider(
                [
                    {
                        "hit_id": "STALE",
                        "summary": "Old hint.",
                        "canonical_ref": "canonical.txt",
                        "canonical_sha256": "a" * 64,
                        "cache_id": "CACHE-STALE",
                        "influences_routing": True,
                        "stale": True,
                    }
                ]
            )
            required = inspect_context(
                root,
                provider=provider,
                query=ContextQuery("old", "route-navigation"),
                required=True,
            )
            self.assertTrue(required.blocking)
            self.assertEqual(required.reason_code, "context.influential_source_unverified")
            optional = inspect_context(
                root,
                provider=provider,
                query=ContextQuery("old", "route-navigation"),
                required=False,
            )
            self.assertEqual(optional.status, "ready_with_warnings")
            self.assertFalse(optional.control_state_mutated)

    def test_missing_or_failed_optional_provider_does_not_corrupt_control_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            optional = inspect_context(
                root,
                provider=None,
                query=ContextQuery("anything", "navigation"),
            )
            self.assertEqual(optional.status, "optional_unavailable")
            self.assertFalse(optional.control_state_mutated)
            failed = inspect_context(
                root,
                provider=FakeContextProvider(raise_error=True),
                query=ContextQuery("anything", "navigation"),
            )
            self.assertEqual(failed.status, "optional_unavailable")
            required = inspect_context(
                root,
                provider=None,
                query=ContextQuery("anything", "navigation"),
                required=True,
            )
            self.assertTrue(required.blocking)

    def test_cache_ids_are_excluded_from_fingerprint_without_explicit_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / "canonical.txt"
            source.write_text("current\n", encoding="utf-8")
            report = inspect_context(
                root,
                provider=FakeContextProvider(
                    [
                        {
                            "hit_id": "HIT-1",
                            "summary": "Hint.",
                            "canonical_ref": "canonical.txt",
                            "canonical_sha256": digest(source),
                            "cache_id": "CACHE-1",
                            "influences_routing": False,
                        }
                    ]
                ),
                query=ContextQuery("hint", "navigation"),
            )
            self.assertEqual(context_fingerprint_payload(report), {})
            canonical = context_fingerprint_payload(
                report, policy_declares_context_canonical=True
            )
            self.assertNotIn("cache_ids", canonical)
            promoted = context_fingerprint_payload(
                report,
                policy_declares_context_canonical=True,
                policy_declares_cache_ids_canonical=True,
            )
            self.assertEqual(promoted["cache_ids"], ["CACHE-1"])


if __name__ == "__main__":
    unittest.main()
