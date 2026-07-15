from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPONENT = REPO_ROOT / "src/components/ProjectStatusStrip.astro"
HOME_PAGE = REPO_ROOT / "src/pages/index.astro"
GLOBAL_CSS = REPO_ROOT / "src/styles/global.css"

EXPECTED_STATES = [
    ("exact-closure", "Exact closure", "Completed effective statement", "complete"),
    ("observable-dynamics", "Observable dynamics", "Exactly GR by adoption", "adopted"),
    ("ontology", "Ontology", "Retained interpretive structure", "interpretive"),
    ("first-principles-derivation", "First-principles derivation", "Open", "open"),
    ("new-low-energy-signature", "New low-energy signature", "Not claimed", "not-claimed"),
]


def load_claim_ladder() -> list[dict[str, object]]:
    script = r"""
import { createServer } from "vite";

const server = await createServer({
  root: process.cwd(),
  server: { middlewareMode: true },
  appType: "custom",
  logLevel: "silent",
});

try {
  const module = await server.ssrLoadModule("/src/lib/publicClaimLadder.ts");
  process.stdout.write(JSON.stringify(module.resolvedPublicClaimLadder));
} finally {
  await server.close();
}
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_home_maps_exactly_five_statuses_in_authorized_order() -> None:
    source = HOME_PAGE.read_text(encoding="utf-8")
    start = source.index("const homeStatusItems")
    end = source.index("] as const;", start)
    status_source = source[start:end]

    positions = []
    for item_id, label, value, semantic in EXPECTED_STATES:
        assert f'id: "{item_id}"' in status_source
        assert f'label: "{label}"' in status_source
        assert f'value: "{value}"' in status_source
        assert f'semantic: "{semantic}"' in status_source
        positions.append(status_source.index(f'id: "{item_id}"'))
    assert positions == sorted(positions)


def test_home_consumes_accepted_claim_ladder_entries_and_places_strip_after_hero() -> None:
    source = HOME_PAGE.read_text(encoding="utf-8")
    ladder = load_claim_ladder()
    expected_claim_states = [
        "complete-effective",
        "adopted-effective",
        "interpretive",
        "open-foundational",
        "not-claimed",
    ]

    assert "resolvedPublicClaimLadder" in source
    assert 'statement.disposition === "accepted"' in source
    for state in expected_claim_states:
        statement = next(item["statement"] for item in ladder if item["state"] == state)
        assert statement["disposition"] == "accepted"
        assert "home" in statement["surfaces"]

    hero = source.index('className="overview-shell overview-command-hero"')
    strip = source.index("<ProjectStatusStrip", hero)
    positioning = source.index('aria-labelledby="home-positioning-title"', strip)
    assert hero < strip < positioning


def test_component_uses_explicit_text_and_non_color_semantics() -> None:
    source = COMPONENT.read_text(encoding="utf-8")

    assert "items.length !== expectedSemantics.length" in source
    assert '<ol class="project-status-strip-list">' in source
    assert "project-status-name" in source
    assert "project-status-value" in source
    assert "project-status-row" in source
    assert "project-status-shape-label" in source
    assert "project-status-context" in source
    assert "project-status-qualification" in source
    assert "Five states, explained." in source
    assert "what the project has completed, adopted, proposed" in source
    assert "Complete within the stated scope" in source
    assert "Used as the observable benchmark" in source
    assert "Proposed interpretation" in source
    assert "Not completed" in source
    assert "Outside the project's current claims" in source
    assert "aria-describedby" not in source
    assert "<svg" not in source


def test_status_strip_is_a_visible_responsive_list_without_card_boxes() -> None:
    css = GLOBAL_CSS.read_text(encoding="utf-8")
    start = css.index(".project-status-strip {")
    end = css.index(".home-intro-panel {", start)
    component_css = css[start:end]
    item_start = component_css.index(".project-status-strip-item {")
    item_end = component_css.index(".project-status-row", item_start)
    item_css = component_css[item_start:item_end]
    context_start = component_css.index(".project-status-context,")
    context_end = component_css.index(".project-status-context {", context_start)
    context_css = component_css[context_start:context_end]

    assert "list-style: decimal;" in component_css
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" not in component_css
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" not in component_css
    assert "border-top: 1px solid var(--overview-white-line);" in item_css
    assert "display: grid;" not in item_css
    assert "background:" not in item_css
    assert "min-width: 0;" in component_css
    assert 'data-status-semantic="open"' in component_css
    assert "border-style: dashed;" in component_css
    assert 'data-status-semantic="not-claimed"' in component_css
    assert "display: none" not in component_css
    assert "overflow-x" not in component_css
    assert "position: absolute" not in context_css
    assert "clip-path" not in context_css
    assert ".project-status-copy {\n    grid-template-columns: minmax(0, 1fr);" in css


def test_status_strip_omits_reviewed_forbidden_overreads() -> None:
    source = (
        COMPONENT.read_text(encoding="utf-8")
        + HOME_PAGE.read_text(encoding="utf-8")
    ).casefold()
    forbidden = {
        overread.casefold()
        for item in load_claim_ladder()
        for overread in item["statement"]["forbiddenOverreads"]
    }
    assert all(overread not in source for overread in forbidden)
