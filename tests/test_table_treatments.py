from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OVERFLOW_TABLE = REPO_ROOT / "src/components/OverflowTable.astro"
TERM_CARD_GRID = REPO_ROOT / "src/components/TermCardGrid.astro"
ONTOLOGY_ROUTE = REPO_ROOT / "src/pages/physics/ontology/index.astro"


def test_term_card_grid_is_one_labeled_semantic_list() -> None:
    source = TERM_CARD_GRID.read_text(encoding="utf-8")

    assert '<ul class:list={["term-card-grid", className]} aria-label={ariaLabel}>' in source
    assert '<li class="term-card-grid__item">' in source
    assert '<article class="term-card">' in source
    assert '<h3>{item.term}</h3>' in source
    assert '<dl class="term-card__fields">' in source
    assert "<dt>{field.label}</dt>" in source
    assert "<dd>{field.value}</dd>" in source
    assert "desktop" not in source.casefold()
    assert "mobile" not in source.casefold()


def test_overflow_table_exposes_instruction_focus_and_edge_state() -> None:
    source = OVERFLOW_TABLE.read_text(encoding="utf-8")

    assert "data-overflow-table" in source
    assert "Scroll table horizontally when it overflows." in source
    assert 'role="region"' in source
    assert 'tabindex="0"' in source
    assert "aria-label={label}" in source
    assert "aria-describedby={instructionId}" in source
    assert "data-overflow-table-start-cue" in source
    assert "data-overflow-table-end-cue" in source
    assert 'viewport.addEventListener("scroll", syncState' in source
    assert "new ResizeObserver(syncState)" in source
    assert "viewport.scrollWidth > viewport.clientWidth + 1" in source
    assert "table.getBoundingClientRect().right <= viewport.getBoundingClientRect().right + 1" in source
    assert "viewport.tabIndex = overflows ? 0 : -1" in source
    assert "instruction.hidden = !overflows" in source


def test_ontology_pilot_uses_cards_and_retains_comparison_table_semantics() -> None:
    source = ONTOLOGY_ROUTE.read_text(encoding="utf-8")

    assert 'import OverflowTable from "../../../components/OverflowTable.astro";' in source
    assert 'import TermCardGrid from "../../../components/TermCardGrid.astro";' in source

    vocabulary_start = source.index('id="ontology-vocabulary"')
    boundary_start = source.index('aria-labelledby="ontology-boundary-title"')
    vocabulary = source[vocabulary_start:boundary_start]
    boundary_end = source.index("<CommandBand", boundary_start)
    boundary = source[boundary_start:boundary_end]

    assert "<TermCardGrid" in vocabulary
    assert "items={vocabularyRows.map" in vocabulary
    assert 'label: "Meaning here"' in vocabulary
    assert 'label: "Boundary"' in vocabulary
    assert "<table" not in vocabulary

    assert "<OverflowTable" in boundary
    assert 'label="Ontology claim boundary comparison"' in boundary
    assert '<table class="greenfield-matrix">' in boundary
    assert '<th scope="col">Layer</th>' in boundary
    assert '<th scope="row">{row.layer}</th>' in boundary

    source_authority = source.rindex("<SourceAuthoritySection")
    layout_close = source.rindex("</BaseLayout>")
    assert boundary_start < source_authority < layout_close
