from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_JOURNEY_FILES = tuple(
    sorted((REPO_ROOT / "src/pages").rglob("*.astro"))
    + sorted((REPO_ROOT / "src/components").rglob("*.astro"))
    + [
        REPO_ROOT / "src/layouts/BaseLayout.astro",
        REPO_ROOT / "src/lib/internalExplainers.ts",
        REPO_ROOT / "src/lib/siteContent.ts",
    ]
)
LEGACY_RESOURCES_HREF = re.compile(r'href(?:=|:)\s*["\']/resources(?:/|["\'])')
STALE_PRODUCT_LABELS = (
    'aria-label="Resources',
    'eyebrow="Resources',
    'label: "Library"',
    'label: "Resources"',
    'title="Library"',
    'title="Resources"',
    'title: "Library"',
    'title: "Resources"',
    '>Library</a>',
    '>Resources</a>',
)


def test_primary_internal_journeys_use_canonical_document_routes() -> None:
    findings = []
    for path in PUBLIC_JOURNEY_FILES:
        source = path.read_text(encoding="utf-8")
        if match := LEGACY_RESOURCES_HREF.search(source):
            findings.append(f"{path.relative_to(REPO_ROOT)}:{match.group(0)}")

    assert findings == []


def test_resources_and_library_are_not_public_product_labels() -> None:
    findings = []
    for path in PUBLIC_JOURNEY_FILES:
        source = path.read_text(encoding="utf-8")
        for label in STALE_PRODUCT_LABELS:
            if label in source:
                findings.append(f"{path.relative_to(REPO_ROOT)}:{label}")

    assert findings == []
