from __future__ import annotations

from pathlib import Path

import quality_gate


def test_route_for_root_index() -> None:
    dist = Path("/tmp/site/dist")
    assert quality_gate.route_for_html(dist, dist / "index.html") == "/"


def test_url_path_to_dist_path_for_directory_route() -> None:
    dist = Path("/tmp/site/dist")
    assert quality_gate.url_path_to_dist_path(dist, "/documents/") == dist / "documents/index.html"


def test_internal_link_validator_reports_missing_target(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text('<a href="/missing/">Missing</a>', encoding="utf-8")

    errors = quality_gate.validate_internal_links(dist)

    assert any("broken href" in error for error in errors)


def test_document_source_authority_section_markup_fails(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    page = dist / "documents/diagrams/index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<section class="source-authority-section">Source authority</section>',
        encoding="utf-8",
    )

    errors = quality_gate.validate_no_document_source_authority_sections(dist)

    assert any("must not render dedicated Source authority sections" in error for error in errors)


def test_document_source_authority_prose_is_allowed(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    page = dist / "documents/diagrams/index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        "<main>Diagram prose can mention source authority without a dedicated notice.</main>",
        encoding="utf-8",
    )

    errors = quality_gate.validate_no_document_source_authority_sections(dist)

    assert errors == []


def test_document_collection_schema_is_required_for_research_not_diagrams(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    research_page = dist / "documents/research/index.html"
    diagrams_page = dist / "documents/diagrams/index.html"
    research_page.parent.mkdir(parents=True)
    diagrams_page.parent.mkdir(parents=True)
    research_page.write_text("<main>Missing collection schema</main>", encoding="utf-8")
    diagrams_page.write_text("<main>Greenfield diagram route</main>", encoding="utf-8")

    errors = quality_gate.validate_document_collection_schema(dist)

    assert any("/documents/research/" in error for error in errors)
    assert not any("/documents/diagrams/" in error for error in errors)


def test_document_greenfield_schema_is_required_for_diagrams(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    page = dist / "documents/diagrams/index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<body class="project-overview-page project-track-page documents-greenfield-page '
        'ai-greenfield-page">'
        '<section class="command-band overview-shell overview-command-hero">'
        '<svg class="track-map-svg physics-greenfield-svg"></svg>'
        '<h2 id="documents-diagrams-comprehension-title">Static diagram contract</h2>'
        '<h2 id="diagram-status-title">The gallery displays approved PNGs.</h2>'
        '<table class="greenfield-matrix"></table>'
        "</section></body>",
        encoding="utf-8",
    )

    errors = quality_gate.validate_document_greenfield_schema(dist)

    assert errors == []


def test_document_greenfield_schema_reports_missing_diagram_contract(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    page = dist / "documents/diagrams/index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<body class="project-overview-page project-track-page documents-greenfield-page '
        'ai-greenfield-page">'
        '<section class="command-band overview-shell overview-command-hero"></section>'
        "</body>",
        encoding="utf-8",
    )

    errors = quality_gate.validate_document_greenfield_schema(dist)

    assert any("missing document greenfield schema snippet" in error for error in errors)
