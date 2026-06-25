# Dual-Project Public Overview PRD

## Problem Statement

The current website needs a public-facing overview that explains, describes, and promotes the Æther Flow project for a general audience. The page must not read as an internal publication-layer scaffold, a software-only dashboard, or a physics-only technical page.

The core communication problem is that Æther Flow is a dual project. One track is a physics research program exploring an Æther-flow interpretation of relativity. The other track is an AI research-agent system used to plan, check, preserve, and review the research work. A general reader should understand both tracks without needing to be a physicist, systems engineer, or contributor.

The page must also preserve the Source Authority Boundary. Website copy can explain reviewed source material, but it must not silently strengthen physics, mathematics, governance, or research-workflow claims. The project is dynamic and expected to change as the upstream source repository changes, so the website must be designed to keep up with future source updates.

## Solution

Create a production-ready public overview experience for Æther Flow that introduces the project as:

> The Æther Flow is a research program with two connected tracks: one explores a physics interpretation, and the other develops the AI research-agent system used to pursue it.

The overview should prioritize public comprehension and restrained promotion. It should use a visually rich, banner-inspired dark cosmic-laboratory direction with electric cyan, orange/gold, ivory text, thin amber outlines, and animated SVG field/workflow motifs. The default page should remain readable and clear. Denser technical diagrams and heavier animation should appear only after a deliberate "More detail" action.

The current UI prototype compares three information-architecture hypotheses:

1. Variant A: Dual-track program first.
2. Variant B: Public reader journey first.
3. Variant C: Trust and claim-status first.

The production implementation should either choose one variant or deliberately remix the strongest parts after review.

## User Stories

1. As a general public reader, I want to quickly understand what Æther Flow is, so that I can decide whether to keep reading.
2. As a general public reader, I want the project introduced as both physics research and an AI research-agent system, so that I do not mistake it for only one of those projects.
3. As a curious non-specialist, I want a simple first layer and optional deeper detail, so that I can choose how technical the page becomes.
4. As a physics-interested reader, I want a clear path to PDFs, ontology material, the Exact-GR benchmark, and the open GR-derivation problem, so that I can inspect the research track.
5. As a software- or systems-interested reader, I want a clear path to the AI research-agent system, source project, roles, claim gates, and memory/registry concepts, so that I can inspect how the project operates.
6. As a reader evaluating credibility, I want visible claim-status and source-authority language, so that I can distinguish explanation from proof.
7. As a reader encountering speculative physics claims, I want the page to state that a first-principles derivation of GR from the ontology is not currently presented as complete, so that the project does not overclaim.
8. As a returning reader, I want the website to communicate that the project is alive and changes over time, so that I know current source state matters.
9. As a mobile reader, I want the overview, animations, controls, and detail panels to fit without overlap, so that the page remains usable on small screens.
10. As a motion-sensitive reader, I want reduced-motion behavior respected, so that animated presentation does not block access.
11. As the project owner, I want the visible public brand to use "Æther Flow" while technical-safe surfaces use "AEther Flow," so that identity and tooling stability both hold.
12. As the project owner, I want visually impressive animation that supports the concept, so that the website feels alive without hiding the source-boundary discipline.

## Implementation Decisions

- Primary audience: the general public.
- Secondary audiences: physics-interested readers who may continue to PDFs and technical material; software/system readers who may continue to the source repository.
- Public brand convention: visible site branding should use "Æther Flow"; technical-safe filenames, URLs, metadata aliases, and repository names should use "AEther Flow."
- Hero direction: title "Æther Flow"; subtitle describing a dual physics-and-AI research program exploring an Æther-flow interpretation of relativity and the research-agent system built to pursue it.
- Primary action: "Understand the project."
- Secondary actions: "Explore physics research" and "Explore the AI research system."
- Track structure: Physics Research and AI Research-Agent System should be equal first-class paths.
- Physics path content: ontology, Exact-GR benchmark, open GR-derivation problem, and no-go/obstruction record.
- AI path content: AI research-agent workflow, role contracts and governed skills, claim gates/review/refutation discipline, and source-first memory/wiki/registries.
- Public wording for the AI side: use "AI research-agent system" and define it as the structured AI-assisted workflow used to plan, check, preserve, and review research work.
- Claim limitation placement: visible but not dominant. Put it near the physics path or trust/status panel, not as the hero headline.
- Dynamic project treatment: include a "Living project" or "Current state" panel explaining that the website should be refreshed from reviewed project outputs, PDFs, source records, and documentation updates.
- Visual direction: use the supplied banner as visual inspiration, not as a direct hero image. The production design should translate it into responsive SVG/CSS motion.
- Animation boundary: use SVG for decorative and explanatory animation; use CSS-first motion plus small vanilla JavaScript for light interaction; avoid new production dependencies unless explicitly approved.
- Progressive disclosure: default content stays clear; "More detail" panels can contain denser diagrams, heavier animation, and more technical language.
- Link behavior: use real links for existing website resources and the GitHub/source project. Mark missing future pages as planned rather than linking to fake routes.
- Prototype handling: the current overview prototype is a decision artifact. After selecting or remixing a variant, remove prototype-only labels and switcher behavior before production release unless a development-only mechanism is approved.

## Testing Decisions

- Validate that the overview route renders with one clear `h1`, accessible headings, meaningful links, and no text overlap on desktop or mobile.
- Verify all three prototype variants during the decision phase: direct URL entry with `?variant=A`, `?variant=B`, and `?variant=C`; switcher next/previous controls; left/right arrow key cycling.
- Verify "More detail" panels open and reveal the correct track-specific richer diagrams and text.
- Verify reduced-motion handling for animated SVG/CSS effects.
- Verify that public CTAs go to real targets or clearly marked planned targets.
- Run the repository validation chain before signoff.
- Run the project-explainer frontend audit against the built static output.
- Run existing tests and lint for repository tooling.
- Use browser QA on `127.0.0.1` for desktop and mobile screenshots, with artifacts stored under the existing Playwright output location.
- Do not test animation internals as implementation detail; test observable behavior, accessibility, non-overlap, and route/interaction correctness.

## Source Authority and Provenance

- The upstream source repository remains authoritative for scientific, mathematical, governance, and research-workflow claims.
- Website copy may explain reviewed source material, organize reader paths, and promote the project, but it must not create or strengthen claims.
- Physics wording must preserve the open-derivation boundary unless the upstream source state changes.
- AI-system wording must distinguish workflow/methodology claims from physics proof.
- New public claims, downloadable artifacts, diagrams, or technical pages require source provenance before production release.
- The source project front door supports the dual-track framing: physics research track plus AI research-agent track.
- Existing source reader paths include project overview, physics-frame explainers, research-agent workflow explainers, source authority pages, and generated HTML/Markdown public surfaces.

References:

- AEther-Flow Project. (2026). `README.md` [Project front door and dual-track research program summary].
- The AEther Flow Website. (2026). `CONTEXT.md` [Source Authority Boundary and website vocabulary].
- The AEther Flow Website. (2026). `README.md` [Website workspace purpose, validation entry points, and source repository boundary].
- The AEther Flow Website. (2026). `src/pages/project/overview.astro` [Current throwaway UI prototype for overview information architecture].

## Out of Scope

- Automatic push-based synchronization from the source repository into website content and manifests.
- Full production conversion of every source explainer page.
- Backend services, live dashboards, simulations, proof validation, or AI runtime integration.
- New production dependencies for animation or interaction.
- Treating the website repository as authoritative for physics or AI research-control claims.
- Using the supplied banner bitmap as the production hero image.
- Shipping the prototype switcher as a public production feature.

## Further Notes

- The logical next step is to review Variants A, B, and C in the browser and choose the production information architecture.
- A likely production remix is: Variant A's equal dual-track structure, Variant B's public reader actions, and Variant C's trust/status framing placed below the hero rather than first.
- A later PRD should define the source-to-website update workflow once the project is ready to keep website content synchronized with upstream source pushes.
- If the final overview introduces new source-backed pages for the physics track or AI research-agent track, those pages should each receive their own source provenance requirements and browser QA scope.
