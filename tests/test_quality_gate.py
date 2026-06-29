from __future__ import annotations

from pathlib import Path

import quality_gate


def test_route_for_root_index() -> None:
    dist = Path("/tmp/site/dist")
    assert quality_gate.route_for_html(dist, dist / "index.html") == "/"


def test_url_path_to_dist_path_for_directory_route() -> None:
    dist = Path("/tmp/site/dist")
    assert quality_gate.url_path_to_dist_path(dist, "/resources/") == dist / "resources/index.html"


def test_internal_link_validator_reports_missing_target(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text('<a href="/missing/">Missing</a>', encoding="utf-8")

    errors = quality_gate.validate_internal_links(dist)

    assert any("broken href" in error for error in errors)


def test_resource_source_authority_section_markup_fails(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    page = dist / "resources/diagrams/index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<section class="source-authority-section">Source authority</section>',
        encoding="utf-8",
    )

    errors = quality_gate.validate_no_resource_source_authority_sections(dist)

    assert any("must not render dedicated Source authority sections" in error for error in errors)


def test_resource_source_authority_prose_is_allowed(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    page = dist / "resources/diagrams/index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        "<main>Diagram prose can mention source authority without a dedicated notice.</main>",
        encoding="utf-8",
    )

    errors = quality_gate.validate_no_resource_source_authority_sections(dist)

    assert errors == []
