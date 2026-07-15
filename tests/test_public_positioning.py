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
PHYSICS_OPEN_BURDENS_PAGE = REPO_ROOT / "src/pages/physics/open-burdens/index.astro"
AI_RESEARCH_SYSTEM_PAGE = REPO_ROOT / "src/pages/ai-research-system/index.astro"
AI_RESEARCH_SYSTEM_CURRENT_STATE_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/current-state/index.astro"
)
AI_RESEARCH_SYSTEM_WORKFLOW_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/workflow/index.astro"
)
AI_RESEARCH_SYSTEM_AGENTJOB_LIFECYCLE_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/agentjob-lifecycle/index.astro"
)
AI_RESEARCH_SYSTEM_ROLES_AND_SCHEMAS_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/roles-and-schemas/index.astro"
)
AI_RESEARCH_SYSTEM_HUMAN_GATED_PROMOTION_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/human-gated-promotion/index.astro"
)
AI_RESEARCH_SYSTEM_VALIDATORS_AND_HANDOFFS_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/validators-and-handoffs/index.astro"
)
AI_RESEARCH_SYSTEM_MEMORY_PREFLIGHT_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/memory-preflight/index.astro"
)
AI_RESEARCH_SYSTEM_PROJECT_SYSTEM_IMPROVEMENT_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/project-system-improvement/index.astro"
)
AI_RESEARCH_SYSTEM_RUNTIME_REQUIREMENTS_PAGE = (
    REPO_ROOT / "src/pages/ai-research-system/runtime-requirements/index.astro"
)
RESOURCES_PAGE = REPO_ROOT / "src/pages/resources/index.astro"
RESOURCES_SOURCE_AUTHORITY_PAGE = REPO_ROOT / "src/pages/resources/source-authority/index.astro"
RESOURCES_REGISTRY_EXPLORER_PAGE = REPO_ROOT / "src/pages/resources/registries/index.astro"
RESOURCES_GENERATED_DERIVATIVES_PAGE = (
    REPO_ROOT / "src/pages/resources/generated-derivatives/index.astro"
)
RESOURCES_LOCAL_RETRIEVAL_LAYERS_PAGE = (
    REPO_ROOT / "src/pages/resources/retrieval-layers/index.astro"
)
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


def test_physics_open_burdens_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = PHYSICS_OPEN_BURDENS_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "exact GR remains the observable-scale benchmark" in source
    assert "first-principles derivation is still open" in source
    assert "missing links as separate obligations" in source
    assert "source structure and metric construction" in source
    assert "matter coupling, Einstein equations, benchmark promotion, and protected human review" in source
    assert "they are not a percentage score" in source
    assert "scoped evidence for one step does not solve the steps after it" in source
    assert "without treating one blocked route as a rejection of the entire research program" in source
    assert "the page remains orientation only" in source
    assert '<section class="greenfield-intro-panel" aria-label="Open burdens introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_ai_research_system_overview_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "small, inspectable unit" in source
    assert "one AgentJob to named roles and allowed actions" in source
    assert "completion and handoff evidence" in source
    assert "protected decisions left to a human Director" in source
    assert "who may act, what evidence is required" in source
    assert "does not by itself prove a physics claim" in source
    assert "expand the authority granted by source records" in source
    assert '<section class="greenfield-intro-panel" aria-label="AI Research System introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_ai_research_system_current_state_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_CURRENT_STATE_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles derivation is still open" in source
    assert "bounded tasks, AgentJobs, validator results, completion records, and handoffs" in source
    assert "one checked-in, dated snapshot" in source
    assert "rather than a live dashboard or permanent statement" in source
    assert "old, missing, or contradicted by higher-authority records" in source
    assert "proves a physics claim" in source
    assert "authorizes source refresh" in source
    assert "expands role or source authority" in source
    assert '<section class="greenfield-intro-panel" aria-label="AI current-state introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_ai_research_system_workflow_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_WORKFLOW_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "starting from tracked state" in source
    assert "using memory only to locate sources" in source
    assert "recording a Director decision" in source
    assert "binding one AgentJob to named roles, allowed files" in source
    assert "what happened and what remains uncertain" in source
    assert "later work as a separate packet" in source
    assert "how authority narrows at each step" in source
    assert "independently proves a physics claim" in source
    assert "expands the job" in source
    assert "replaces a protected human decision" in source
    assert '<section class="greenfield-intro-panel" aria-label="Workflow introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_agentjob_lifecycle_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_AGENTJOB_LIFECYCLE_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "one AgentJob is a single-use contract" in source
    assert "allowed reads and writes, forbidden paths, expected outputs" in source
    assert "claim limits, and stop conditions" in source
    assert "A Director decision chooses the route" in source
    assert "execution-role record binds the role to that one job" in source
    assert "separate handoff and new packet" in source
    assert "none independently proves a physics claim" in source
    assert "promotes the proposed ontology" in source
    assert "authorizes upstream changes" in source
    assert "becomes reusable permission" in source
    assert '<section class="greenfield-intro-panel" aria-label="AgentJob lifecycle introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_roles_and_schemas_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_ROLES_AND_SCHEMAS_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "schemas—required field definitions for control records" in source
    assert "registered role is only a stable template" in source
    assert "task-local execution-role record binds it to one AgentJob" in source
    assert "one-job task overlay" in source
    assert "provisional role that expires with its job" in source
    assert "distinguish a label from live permission" in source
    assert "no role, schema, registry row, validator PASS, or website page" in source
    assert "independently proves a physics claim" in source
    assert "human-gated Gate Chair path" in source
    assert "requires explicit tracked approval" in source
    assert '<section class="greenfield-intro-panel" aria-label="Roles and schemas introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_human_gated_promotion_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_HUMAN_GATED_PROMOTION_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "candidate calculations, audits, refutations, documentation" in source
    assert "Canonical ontology adoption, benchmark promotion, scientific claim closure" in source
    assert "Gate Chair verdict require the explicit tracked human approval" in source
    assert "role registry does not activate that authority" in source
    assert "validator PASS, completion, handoff, commit, or public page" in source
    assert "cannot substitute for the required person and approval record" in source
    assert "evidence can accumulate below that boundary" in source
    assert "protected verdict remains separate" in source
    assert "Publication acceptance and deployment are also separate owner decisions" in source
    assert "none independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology" in source
    assert "authorizes protected execution" in source
    assert '<section class="greenfield-intro-panel" aria-label="Human-gated promotion introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_validators_and_handoffs_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_VALIDATORS_AND_HANDOFFS_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "bounded, inspectable transactions" in source
    assert "allowed work, expected outputs, checks, claim limits, and stop conditions" in source
    assert "one named question about the state actually checked" in source
    assert "nothing automatically about unmodified surfaces, future changes, or scientific truth" in source
    assert "completion closes one job" in source
    assert "handoff transfers that durable state and recommends a separate next packet" in source
    assert "program state points to the current job" in source
    assert "local checkpoint seals the allowed transaction" in source
    assert "Screenshot review can expose overflow, missing headings, broken navigation" in source
    assert "cannot make a website page source authority" in source
    assert "no validator PASS, completion, handoff, registry row, screenshot, commit, or webpage" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology" in source
    assert "expands role authority" in source
    assert "silently continues a closed job" in source
    assert '<section class="greenfield-intro-panel" aria-label="Validators and handoffs introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_memory_preflight_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_MEMORY_PREFLIGHT_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "memory preflight before bounded work" in source
    assert "source objects, registry rows, prior tasks, handoffs" in source
    assert "retrieval layers are fresh enough for navigation" in source
    assert "targeted lookup" in source
    assert "tracked source file and its registry row" in source
    assert "query, returned canonical object IDs, inspected paths, hashes, and authority note" in source
    assert "Registered TeX carries physics and derivational claims" in source
    assert "registered Markdown and tracked control records carry their scoped project authority" in source
    assert "registries carry provenance, relationships, status, and memory metadata" in source
    assert "Generated wiki notes, semantic extracts, Obsidian mirrors, SQLite indexes" in source
    assert "they remain downstream retrieval support" in source
    assert "the tracked source wins" in source
    assert "stale retrieval warning calls for maintenance or direct source inspection" in source
    assert "No memory hit, freshness report, registry row, generated derivative, receipt, AI output, or website page" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology" in source
    assert "expands authority" in source
    assert "replaces direct canonical inspection" in source
    assert '<section class="greenfield-intro-panel" aria-label="Memory preflight introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_project_system_improvement_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_PROJECT_SYSTEM_IMPROVEMENT_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "keeps research and maintenance separate" in source
    assert "Project-System Improvement repairs the machinery around that work" in source
    assert "documentation, validators, schemas, memory retrieval, routing, trigger logic" in source
    assert "without continuing the science by implication" in source
    assert "current working-tree diff, a registered open signal, a repeated workflow problem" in source
    assert "source-bridged project-improvement sidecar" in source
    assert "tracked source files and registry rows must be inspected" in source
    assert "classifier describes the issue as documentation drift, a validator gap, routing ambiguity" in source
    assert "advisory resolver ranks the candidate" in source
    assert "one bounded AgentJob with an explicit write-path allowlist and claim boundary" in source
    assert "documentation-impact receipt records affected source surfaces" in source
    assert "generated derivatives, classifier reason codes, and required validators" in source
    assert "signal closes only with matching PASS completion evidence or a documented rejection decision" in source
    assert "sidecar is a separate maintenance input and never replaces the normal research handoff" in source
    assert "resolver recommendation alone neither authorizes nor blocks checkpointing" in source
    assert "registered role or descriptive perspective does not activate authority" in source
    assert "no diff, classifier, resolver, sidecar, signal, registry row" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology or a benchmark" in source
    assert "grants role authority" in source
    assert "expands an allowlist" in source
    assert "authorizes research continuation" in source
    assert '<section class="greenfield-intro-panel" aria-label="Project-system improvement introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_runtime_requirements_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = AI_RESEARCH_SYSTEM_RUNTIME_REQUIREMENTS_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "tool being installed answers only whether an operation can run" in source
    assert "not whether anyone is authorized to run it" in source
    assert "Git, a shell, an editor, and a browser support read-only inspection" in source
    assert "Codex app, repository skills, and tracked control records support governed work" in source
    assert "Python virtual environment, declared dependencies, scripts, and tests" in source
    assert "Node.js, npm, Astro, and Playwright support static builds and browser review" in source
    assert "local retrieval layers support navigation" in source
    assert "TeX or PDF tooling is used only when registered derivatives are explicitly in scope" in source
    assert "tracked source, current task and job, role or skill contract" in source
    assert "write-path allowlist, claim boundary, and applicable human gates" in source
    assert "result remains limited to the named surface it checked" in source
    assert "`npm run build` compiles the website routes but does not deploy them" in source
    assert "implementation-control validation checks record structure but not source authority" in source
    assert "Python tests provide evidence about tested behavior but not untested behavior or physics" in source
    assert "screenshots show rendered layout rather than truth" in source
    assert "Missing or failing runtime support becomes a bounded maintenance signal" in source
    assert "not a scientific verdict" in source
    assert "Memory indexes, Obsidian mirrors, SQLite databases, and `.local` caches" in source
    assert "tracked files and registries remain authority" in source
    assert "No installed runtime, dependency, skill, script, Makefile target" in source
    assert "validator PASS, screenshot, cache, AI output, or website page" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology or a benchmark" in source
    assert "grants role or source-edit authority" in source
    assert "bypasses an AgentJob allowlist" in source
    assert "deploys the site" in source
    assert "refreshes sources" in source
    assert "authorizes an upstream mutation" in source
    assert '<section class="greenfield-intro-panel" aria-label="Runtime requirements introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_resources_overview_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = RESOURCES_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "public map for reading evidence around both tracks" in source
    assert "Start with the internal route that matches the question" in source
    assert "Registered TeX carries scoped physics and derivational claims" in source
    assert "registered Markdown and tracked control records carry guidance and workflow authority" in source
    assert "registries record provenance, relationships, hashes, routing, and status" in source
    assert "without replacing the source files they describe" in source
    assert "Generated pages, PDFs, diagrams, and downloads help people read the project" in source
    assert "semantic extracts, Obsidian mirrors, SQLite indexes, and local caches help them find material" in source
    assert "the source and record win" in source
    assert "path, type, byte count, hash, status, and source reference" in source
    assert "a hash identifies file contents rather than scientific correctness" in source
    assert "Publication briefs define the reader and acceptance criteria" in source
    assert "source specifications bind public outputs to inspected evidence" in source
    assert "bounded publication quality rather than source authority" in source
    assert "No route card, manifest row, download, hash, registry entry, generated derivative" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology or a benchmark" in source
    assert "grants workflow authority" in source
    assert "replaces human review" in source
    assert '<section class="greenfield-intro-panel" aria-label="Resources overview introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_resources_source_authority_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = RESOURCES_SOURCE_AUTHORITY_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "Source authority is the trust rule shared by both tracks" in source
    assert "not which page is clearest" in source
    assert "which tracked material is allowed to define the status of the claim" in source
    assert "Registered TeX carries scoped physics and derivational claims" in source
    assert "Registered Markdown carries front-door guidance" in source
    assert "Current research-control records and registries carry task authority" in source
    assert "without replacing the source files they describe" in source
    assert "Generated Markdown, HTML pages, PDFs, diagrams, wiki notes" in source
    assert "semantic extracts, Obsidian mirrors, SQLite indexes, memory results, and local caches" in source
    assert "website PRDs define page requirements rather than canonical project claims" in source
    assert "names the claim class, identifies its owner, inspects the source file" in source
    assert "resolves any disagreement in favor of the source" in source
    assert "preserves exact qualifiers" in source
    assert "contextual copy and provenance metadata rather than a separate Source authority component section" in source
    assert "the source wins and the derivative needs repair" in source
    assert "No registry row, generated explainer, diagram, PDF, memory hit, validator PASS" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology or a benchmark" in source
    assert "expands an AgentJob or role's authority" in source
    assert "overrides a human gate" in source
    assert "replaces direct source inspection" in source
    assert "SourceAuthoritySection" not in source
    assert '<section class="greenfield-intro-panel" aria-label="Resources source authority introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_resources_registry_explorer_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = RESOURCES_REGISTRY_EXPLORER_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "tracked maps to the material and decisions behind both tracks" in source
    assert "owner, path, status, date, hash, relationship, or limit" in source
    assert "do not replace the file or decision record they describe" in source
    assert "Source registries point to registered TeX" in source
    assert "registered Markdown for authored guidance" in source
    assert "Derivative registries connect PDFs, HTML explainers, GitHub-facing Markdown" in source
    assert "publication and relationship registries connect briefs, specifications, sources, and outputs" in source
    assert "Workflow registries record bounded AgentJobs, Director decisions, roles, tasks" in source
    assert "cannot widen an allowlist, expand a role" in source
    assert "Claim-boundary rows record allowed wording, forbidden overreads, and required gates" in source
    assert "Distance-to-GR ledger records named open burdens and evidence paths" in source
    assert "neither the boundary metadata nor a burden label executes a gate" in source
    assert "find the relevant row, open the owner it names" in source
    assert "check the recorded status, date, source commit, or freshness boundary" in source
    assert "what the row supports and what it cannot prove" in source
    assert "neither establishes scientific correctness" in source
    assert "contextual copy, tables, and provenance rather than a separate Source authority component section" in source
    assert "No registry row, dashboard, hash, approval status, generated derivative" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology or a benchmark" in source
    assert "expands workflow authority" in source
    assert "overrides a human gate" in source
    assert "replaces direct source inspection" in source
    assert "SourceAuthoritySection" not in source
    assert '<section class="greenfield-intro-panel" aria-label="Resources registries introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_resources_generated_derivatives_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = RESOURCES_GENERATED_DERIVATIVES_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "reader-facing copy, explanation, or visual presentation made from tracked material" in source
    assert "without becoming the owner of the claims it presents" in source
    assert "GitHub-facing Markdown supports repository and AI-assisted reading" in source
    assert "tracked HTML supports visual no-network reading" in source
    assert "PDFs and document copies support inspection and download" in source
    assert "generated wiki pages and object browsers support discovery" in source
    assert "diagrams and public assets support comprehension" in source
    assert "remains downstream from its registered source, registry row, or governed control record" in source
    assert "canonical source or registry supplies the claim basis" in source
    assert "source specification binds the intended output" in source
    assert "publication brief defines the reader job, visual strategy, acceptance criteria" in source
    assert "deterministic checks plus desktop, mobile, or before-and-after review evidence" in source
    assert "parity requires the same source basis, authority boundary, and core claims" in source
    assert "rather than identical section order" in source
    assert "a hash identifies particular file contents, not scientific correctness" in source
    assert "publication approval records a bounded reader-surface decision rather than physics authority" in source
    assert "find the source basis, inspect the named source" in source
    assert "The source wins, and the derivative needs repair" in source
    assert "contextual copy, tables, and provenance rather than a separate Source authority component section" in source
    assert "No generated Markdown, HTML page, PDF, document copy, wiki note, diagram" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology or a benchmark" in source
    assert "expands workflow authority" in source
    assert "overrides a human gate" in source
    assert "replaces direct source inspection" in source
    assert "SourceAuthoritySection" not in source
    assert '<section class="greenfield-intro-panel" aria-label="Generated derivatives introduction">' not in source

    hero = source.index('className="overview-shell overview-command-hero"')
    introduction = source.index("<ProjectIntroduction", hero)
    comprehension = source.index("<ComprehensionBlocks", introduction)

    assert hero < introduction < comprehension


def test_resources_local_retrieval_layers_has_a_general_public_project_introduction_after_the_hero() -> None:
    source = RESOURCES_LOCAL_RETRIEVAL_LAYERS_PAGE.read_text(encoding="utf-8")

    assert 'import ProjectIntroduction from "../../../components/ProjectIntroduction.astro"' in source
    assert source.count("<ProjectIntroduction") == 1
    assert "two-part research program about foundational physics" in source
    assert "governed, human-accountable AI research system" in source
    assert "general relativity remains the exact benchmark for observable gravity" in source
    assert "first-principles substrate derivation is still open" in source
    assert "search and navigation aids" in source
    assert "without becoming the owner of the claims they find" in source
    assert "Memory lookup can recall candidate paths" in source
    assert "semantic extracts can surface related passages" in source
    assert "generated wiki pages and Obsidian mirrors" in source
    assert "SQLite or other local indexes" in source
    assert "ignored local caches can hold previews, screenshots, logs" in source
    assert "stale, partial, generated, or local-only" in source
    assert "begins with a precise question, uses retrieval to find a candidate" in source
    assert "identifies the tracked file, registry row, task, completion, handoff" in source
    assert "inspects that owner in context" in source
    assert "Registered TeX carries scoped physics and derivational claims" in source
    assert "registered Markdown and tracked control records carry their own" in source
    assert "registries record provenance, relationships, paths, hashes, and status" in source
    assert "repairs navigation support rather than creating committed evidence" in source
    assert "the tracked source and current governed record win" in source
    assert "an older memory must be rechecked" in source
    assert "a partial extract must be expanded to its surrounding source" in source
    assert "a generated mirror must route the reader back to its owner" in source
    assert "a local cache must remain local rather than being cited as public evidence" in source
    assert "contextual copy, tables, and provenance rather than a separate Source authority component section" in source
    assert "No memory hit, semantic extract, wiki or Obsidian mirror, SQLite index, local cache" in source
    assert "independently proves a physics claim" in source
    assert "completes the open first-principles derivation" in source
    assert "promotes the proposed ontology or a benchmark" in source
    assert "expands workflow authority" in source
    assert "overrides a human gate" in source
    assert "replaces direct source inspection" in source
    assert "SourceAuthoritySection" not in source
    assert '<section class="greenfield-intro-panel" aria-label="Retrieval layers introduction">' not in source

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
