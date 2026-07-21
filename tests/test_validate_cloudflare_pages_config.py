from __future__ import annotations

from pathlib import Path

import validate_cloudflare_pages_config as validator

REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_RESOURCE_REDIRECTS = [
    ("/resources/", "/documents/", "301"),
    ("/resources/library/", "/documents/", "301"),
    ("/resources/documents/", "/documents/research/", "301"),
    ("/resources/diagrams/", "/documents/diagrams/", "301"),
    (
        "/resources/source-authority/",
        "/documents/governance/source-authority/",
        "301",
    ),
    ("/resources/registries/", "/documents/governance/registries/", "301"),
    ("/resources/generated-derivatives/", "/documents/derivatives/", "301"),
    (
        "/resources/retrieval-layers/",
        "/documents/governance/retrieval-layers/",
        "301",
    ),
    (
        "/resources/publication-process/",
        "/documents/governance/publication-process/",
        "301",
    ),
    ("/resources/reading-paths/", "/documents/reading-paths/", "301"),
    (
        "/resources/repository-map/",
        "/documents/governance/repository-map/",
        "301",
    ),
    (
        "/resources/site-builder-guide/",
        "/documents/governance/site-builder-guide/",
        "301",
    ),
    ("/resources/guided-starts/", "/documents/reading-paths/", "301"),
    (
        "/resources/guided-starts/general-public/",
        "/documents/reading-paths/general-public/",
        "301",
    ),
    ("/resources/reviewer-packet/", "/documents/reviewer-packet/", "301"),
]

EXPECTED_LEGACY_REDIRECTS = {
    "/diagrams": ("/documents/diagrams/", "301"),
    "/equations": ("/documents/research/", "301"),
    "/downloads": ("/documents/", "301"),
    "/project/operations/publication-process/": (
        "/documents/governance/publication-process/",
        "301",
    ),
    "/project/source-authority/publication-and-provenance-system/": (
        "/documents/governance/publication-process/",
        "301",
    ),
    "/project/source-authority/": (
        "/documents/governance/source-authority/",
        "301",
    ),
    "/research": ("/documents/governance/publication-process/", "302"),
    "/research/map/": (
        "/documents/governance/publication-process/",
        "301",
    ),
}


def test_current_cloudflare_pages_config_validates() -> None:
    header_errors = validator.validate_headers(REPO_ROOT / "public/_headers")
    redirect_errors = validator.validate_redirects(REPO_ROOT / "public/_redirects")

    assert header_errors == []
    assert redirect_errors == []


def test_project_overview_redirects_to_home() -> None:
    redirects = [line for _, line in validator.meaningful_lines(REPO_ROOT / "public/_redirects")]

    assert "/project/overview/ / 301" in redirects
    assert "/overview / 301" in redirects


def test_retired_resources_routes_redirect_directly_to_documents() -> None:
    redirects = [
        tuple(line.split())
        for _, line in validator.meaningful_lines(REPO_ROOT / "public/_redirects")
    ]
    resource_redirects = [
        rule for rule in redirects if rule[0].startswith("/resources")
    ]
    redirect_sources = {rule[0] for rule in redirects}

    assert resource_redirects == EXPECTED_RESOURCE_REDIRECTS
    assert all(
        destination not in redirect_sources
        for _, destination, _ in resource_redirects
    )


def test_legacy_aliases_redirect_directly_to_documents() -> None:
    redirects = {
        fields[0]: (fields[1], fields[2] if len(fields) == 3 else "302")
        for _, line in validator.meaningful_lines(REPO_ROOT / "public/_redirects")
        if (fields := line.split())
    }

    assert {
        source: redirects[source] for source in EXPECTED_LEGACY_REDIRECTS
    } == EXPECTED_LEGACY_REDIRECTS
    assert all(
        destination not in redirects
        for destination, _ in EXPECTED_LEGACY_REDIRECTS.values()
    )


def test_redirect_validator_rejects_invalid_status(tmp_path: Path) -> None:
    redirects = tmp_path / "_redirects"
    redirects.write_text("/old /new 999\n", encoding="utf-8")

    errors = validator.validate_redirects(redirects)

    assert any("unsupported redirect status" in error for error in errors)
