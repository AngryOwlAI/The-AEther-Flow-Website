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


def test_resource_support_schema_is_required_for_documents_not_diagrams(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    documents_page = dist / "resources/documents/index.html"
    diagrams_page = dist / "resources/diagrams/index.html"
    documents_page.parent.mkdir(parents=True)
    diagrams_page.parent.mkdir(parents=True)
    documents_page.write_text("<main>Missing support schema</main>", encoding="utf-8")
    diagrams_page.write_text("<main>Greenfield diagram route</main>", encoding="utf-8")

    errors = quality_gate.validate_resource_support_schema(dist)

    assert any("/resources/documents/" in error for error in errors)
    assert not any("/resources/diagrams/" in error for error in errors)


def test_resource_greenfield_schema_is_required_for_diagrams(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    page = dist / "resources/diagrams/index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<body class="project-overview-page project-track-page resources-greenfield-page '
        'ai-greenfield-page">'
        '<section class="command-band overview-shell overview-command-hero">'
        '<svg class="track-map-svg physics-greenfield-svg"></svg>'
        '<h2 id="resources-diagrams-comprehension-title">Static diagram contract</h2>'
        '<h2 id="diagram-status-title">The gallery displays approved PNGs.</h2>'
        '<div class="diagram-gallery-list"></div>'
        "</section></body>",
        encoding="utf-8",
    )

    errors = quality_gate.validate_resource_greenfield_schema(dist)

    assert errors == []


def test_resource_greenfield_schema_reports_missing_diagram_contract(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    page = dist / "resources/diagrams/index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<body class="project-overview-page project-track-page resources-greenfield-page '
        'ai-greenfield-page">'
        '<section class="command-band overview-shell overview-command-hero"></section>'
        "</body>",
        encoding="utf-8",
    )

    errors = quality_gate.validate_resource_greenfield_schema(dist)

    assert any("missing resource greenfield schema snippet" in error for error in errors)
