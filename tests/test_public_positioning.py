from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOME_PAGE = REPO_ROOT / "src/pages/index.astro"
PHYSICS_PAGE = REPO_ROOT / "src/pages/physics/index.astro"
PHYSICS_ONTOLOGY_PAGE = REPO_ROOT / "src/pages/physics/ontology/index.astro"
PHYSICS_BENCHMARK_PAGE = REPO_ROOT / "src/pages/physics/exact-gr-benchmark/index.astro"
PHYSICS_DERIVATION_PAGE = REPO_ROOT / "src/pages/physics/derivation-roadmap/index.astro"
PHYSICS_FLOW_GEOMETRY_PAGE = REPO_ROOT / "src/pages/physics/flow-geometry/index.astro"
PHYSICS_CLAIM_STATUS_PAGE = REPO_ROOT / "src/pages/physics/claim-status/index.astro"
PROJECT_INTRODUCTION = REPO_ROOT / "src/components/ProjectIntroduction.astro"
ROUTE_MAP = REPO_ROOT / "public/files/manifests/page_route_map.json"

EXPECTED_STATE_ORDER = [
    "interpretive",
    "adopted-effective",
    "complete-effective",
    "open-foundational",
    "governed-method",
]


def load_public_statements() -> list[dict[str, object]]:
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


def route_record(route_path: str) -> dict[str, object]:
    route_map = json.loads(ROUTE_MAP.read_text(encoding="utf-8"))
    return next(route for route in route_map["routes"] if route["route_path"] == route_path)


def test_routes_consume_only_accepted_surface_statements() -> None:
    for path, surface in ((HOME_PAGE, "home"), (PHYSICS_PAGE, "physics")):
        source = path.read_text(encoding="utf-8")
        assert "resolvedPublicClaimLadder" in source
        assert 'statement.disposition === "accepted"' in source
        assert f'statement.surfaces.includes("{surface}")' in source
        assert ".exactWording" in source
        assert ".allowedQualification" in source

    statements = load_public_statements()
    for surface in ("home", "physics"):
        surface_statements = [
            item["statement"]
            for item in statements
            if surface in item["statement"]["surfaces"]
        ]
        assert len(surface_statements) == 6
        assert all(statement["disposition"] == "accepted" for statement in surface_statements)
        assert all(statement["allowedQualification"] for statement in surface_statements)


def test_routes_encode_the_authorized_positive_content_order() -> None:
    for path, prefix in ((HOME_PAGE, "home"), (PHYSICS_PAGE, "physics")):
        source = path.read_text(encoding="utf-8")
        sequence_start = source.index(f"const {prefix}PositioningSteps")
        sequence_end = source.index("] as const;", sequence_start)
        sequence = source[sequence_start:sequence_end]

        positions = [sequence.index(f'get("{state}")') for state in EXPECTED_STATE_ORDER]
        assert positions == sorted(positions)
        assert 'get("not-claimed")' in sequence

    physics = PHYSICS_PAGE.read_text(encoding="utf-8")
    rendered_sequence = physics.index("{physicsPositioningSteps.map")
    evidence = physics.index("<SourceAuthoritySection", rendered_sequence)
    route_navigation = physics.index("<ComprehensionBlocks", evidence)
    assert rendered_sequence < evidence < route_navigation


def test_home_introduction_and_requested_section_order_are_explicit() -> None:
    source = HOME_PAGE.read_text(encoding="utf-8")
    component = PROJECT_INTRODUCTION.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "exact benchmark for observable gravity" in source
    assert "human-accountable process" in source
    assert "remains an open research problem" in source
    assert "does not claim a verified new law of gravity" in source

    assert "ProjectIntroduction requires a nonempty paragraph." in component
    assert "data-project-introduction" in component
    assert "<p>{text}</p>" in component

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    status = source.index("<ProjectStatusStrip", introduction)
    positioning = source.index('aria-labelledby="home-positioning-title"', status)
    actions = source.index('class="home-action-row"', positioning)
    tracks = source.index('id="overview-paths"', actions)
    ontology = source.index('id="ontology-and-gr"', tracks)
    comprehension = source.index("<ComprehensionBlocks", ontology)
    capabilities = source.index('id="project-capabilities"', comprehension)
    source_authority = source.rindex("<SourceAuthoritySection")
    layout_end = source.index("</BaseLayout>", source_authority)

    assert (
        hero
        < introduction
        < status
        < positioning
        < actions
        < tracks
        < ontology
        < comprehension
        < capabilities
        < source_authority
        < layout_end
    )


def test_physics_overview_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = PHYSICS_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity as its exact observable benchmark" in source
    assert "remains an open research problem" in source
    assert "does not claim a verified new law of gravity" in source
    assert "helps readers distinguish the proposed ontology" in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    positioning = source.index('class="track-page-band public-positioning-sequence"', introduction)

    assert hero < introduction < positioning


def test_physics_ontology_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = PHYSICS_ONTOLOGY_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "proposed vocabulary" in source
    assert "do not supply the missing mathematical bridge" in source
    assert "derive general relativity" in source
    assert "establish an empirical prediction" in source
    assert "separates conceptual orientation" in source
    assert '<section class="greenfield-intro-panel" aria-label="Ontology introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_physics_benchmark_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = PHYSICS_BENCHMARK_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "conservative observable-scale reference" in source
    assert "one operative Lorentzian metric" in source
    assert "universal matter coupling" in source
    assert "no claimed empirical deviation from GR" in source
    assert "does not mean the proposed Æther / Æther-Flow ontology has derived it" in source
    assert "benchmark adoption, ontology compatibility" in source
    assert "effective-level result is not mistaken for foundational proof" in source
    assert '<section class="greenfield-intro-panel" aria-label="Exact-GR benchmark introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_physics_derivation_roadmap_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = PHYSICS_DERIVATION_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "open first-principles problem" in source
    assert "without inserting the target metric or benchmark behavior by hand" in source
    assert "source ontology, localization and response" in source
    assert "universal matter coupling, Einstein equations" in source
    assert "Distance-to-GR ledger record bounded statuses and evidence" in source
    assert "do not supply a completed derivation" in source
    assert "map of remaining work from proof" in source
    assert '<section class="greenfield-intro-panel" aria-label="Derivation roadmap introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_physics_flow_geometry_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = PHYSICS_FLOW_GEOMETRY_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "dictionary for reading the proposed Æther-Flow interpretation" in source
    assert "g is the adopted GR metric" in source
    assert "u is an admissible, generally non-unique observer field" in source
    assert "expansion, shear, rotation, and acceleration" in source
    assert "adds interpretation rather than a second gravitational law" in source
    assert "does not derive either the metric or a preferred flow" in source
    assert "derive matter coupling, recover Einstein equations, or promote the benchmark" in source
    assert '<section class="greenfield-intro-panel" aria-label="Flow geometry introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_physics_claim_status_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = PHYSICS_CLAIM_STATUS_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "exact GR remains the observable-scale benchmark" in source
    assert "first-principles derivation is still open" in source
    assert "four plain-language categories" in source
    assert "what the record supports saying" in source
    assert "what it does not support" in source
    assert "what remains open or protected by a human gate" in source
    assert "without proving a physical theory or promoting a scientific claim" in source
    assert "the page remains orientation only" in source
    assert '<section class="greenfield-intro-panel" aria-label="Physics claim-status introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_route_metadata_is_source_safe_and_route_local() -> None:
    home = HOME_PAGE.read_text(encoding="utf-8")
    physics = PHYSICS_PAGE.read_text(encoding="utf-8")

    assert 'title="The Æther Flow Project | Exact Closure and Open Foundations"' in home
    assert 'title="Physics Research | Exact Closure and Open Foundations"' in physics
    assert "description={`${homeCurrentResult.exactWording} ${homeOpenFoundation.exactWording}`}" in home
    assert "description={`${physicsCurrentResult.exactWording} ${physicsOpenFoundation.exactWording}`}" in physics


def test_route_bundles_and_authority_classifications_remain_fixed() -> None:
    expected_sources = [
        "ontology/tex/aether_flow_exact_closure_sequence_overview.tex",
        "ontology/tex/aether_flow_exact_closure_note.tex",
        "ontology/tex/aether_flow_exact_closure_flagship_article.tex",
    ]
    for route_path in ("/", "/physics/"):
        route = route_record(route_path)
        assert route["adaptation_type"] == "curated_synthesis"
        assert route["upstream_authority_status"] == "generated_noncanonical"
        assert route["website_publication_status"] == "published"
        for source_path in expected_sources:
            assert source_path in route["upstream_source_paths"]


def test_route_copy_omits_reviewed_forbidden_overreads() -> None:
    source = HOME_PAGE.read_text(encoding="utf-8") + PHYSICS_PAGE.read_text(encoding="utf-8")
    forbidden = {
        overread.casefold()
        for item in load_public_statements()
        for overread in item["statement"]["forbiddenOverreads"]
    }
    assert all(overread not in source.casefold() for overread in forbidden)
