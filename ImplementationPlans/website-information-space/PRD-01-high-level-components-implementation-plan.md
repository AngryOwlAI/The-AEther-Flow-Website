# Implementation Plan: PRD-01 High-Level Components

## Source PRD

- Source: `PRDs/website-information-space/PRD-01-high-level-components.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines the high-level public explanation system for The Æther Flow Website. It covers the homepage, project overview, dual-track project map, exact-GR benchmark summary, open derivation burden summary, AI research-agent system summary, trust and claim-boundary panel, and primary reader journeys.

The high-level website layer exists to answer the first reader question: "What is this project, and why should I trust its boundaries?"

This sub implementation plan maps `PRD-01` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for home, overview, dual-track framing, and reader journeys and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/`, `/resources/reading-paths/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-01-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-01-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-01-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-01-Q-001 | Planning assumption | Should the homepage include current-frontier status in the first release, or | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-01-Q-002 | Planning assumption | Should the project overview be a separate route, a Home section, or both | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-01-Q-003 | Planning assumption | What is the minimum first-release reader path: Home plus source authority, | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-01-Q-004 | Planning assumption | Should the trust panel be a reusable component, a page section convention, | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-01-REQ-001 | Explain the project in one precise sentence. | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-002 | Present the physics and AI research tracks as co-equal parts of the project. | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-003 | Show that exact-GR benchmark adoption and first-principles derivation are | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-004 | Explain why the AI research-agent system matters while the physics | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-005 | Provide reader paths for general readers, physicists, AI researchers, | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-006 | Require the homepage hero to state the dual mission, exact-GR status, and | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-007 | Require three first-level summary cards: the ontology or physics idea, the | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-008 | Require a visible trust panel explaining claims made, claims not made, and | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-009 | Link to source-authority guidance before asking readers to evaluate deep | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-REQ-010 | Keep internal website routes primary and source links available as | Home, overview, dual-track framing, and reader journeys; future route surfaces `/`, `/resources/reading-paths/`. | PRD-01-TASK-01, PRD-01-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-01-NFR-001 | Clarity: A new reader should answer "what is this project?" within one | Shared page contract, source bundles, validation, and review closeout. | PRD-01-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-01-NFR-002 | Precision: The first screen must separate exact-GR compatibility from | Shared page contract, source bundles, validation, and review closeout. | PRD-01-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-01-NFR-003 | Balance: Physics and AI research-system material should appear as two parts | Shared page contract, source bundles, validation, and review closeout. | PRD-01-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-01-NFR-004 | Auditability: High-level claims must point to source-authority and | Shared page contract, source bundles, validation, and review closeout. | PRD-01-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-01-NFR-005 | Maintainability: The overview model should survive later route or component | Shared page contract, source bundles, validation, and review closeout. | PRD-01-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-01-NFR-006 | Safety: If source status is stale or uncertain, public copy must choose the | Shared page contract, source bundles, validation, and review closeout. | PRD-01-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-01` requirements onto the greenfield route surfaces rather than the
   older route tree.
3. Require future route packets to inspect source bundles before public copy is
   written.
4. Use narrative bands, evidence rails, status dossiers, matrices, tables,
   timelines, glossaries, or diagrams according to the information type.
5. Preserve internal-first navigation and use GitHub or source links as
   provenance rather than primary reader journeys.

## Implementation Phases

1. Planning packet: create this sub implementation plan and task-packet set.
2. Source-bundle packet: inspect or create the source bundle for the affected
   future route family.
3. Route packet: implement the affected greenfield route surfaces in bounded
   vertical slices.
4. Validation packet: run page-specific validators, browser QA, provenance
   checks, and owner review.
5. Retirement packet: only after replacements validate, update manifests,
   redirects, and old-route retirement under a separate authorized packet.

## Future Acceptance Criteria

- A new reader can answer "what is this project?" within one minute.
- The homepage does not imply that GR has been derived.
- The overview separates exact-GR benchmark adoption from first-principles
- Physics and AI research tracks appear as co-equal parts of the project.
- The page links to source-authority guidance before deep technical claims
- The page includes a visible "what this project does not claim" element.
- Reader paths exist for general readers, physicists, AI researchers,
- High-level pages use approved positioning language and avoid forbidden

## Validation Plan

- Planning packet validation:
  - `git diff --check`
  - `npm run validate:implementation-control`
  - `.venv/bin/python -m pytest`
- Future public route validation:
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:layout`
  - `npm run validate:provenance`
  - `npm run validate:comprehension`
  - `npm run build`
  - desktop and mobile browser QA for changed routes
- Add `npm run validate:svg` and `npm run validate:manifests` when SVGs,
  diagrams, public assets, or public manifests change.

## Security, Privacy, And Reliability Notes

- Do not mutate upstream source-project files.
- Do not strengthen scientific, mathematical, governance, or workflow claims
  beyond tracked source authority.
- Do not publish or refresh public assets, manifests, generated derivatives,
  source snapshots, or retrieval layers from this planning packet.
- Treat stale current-state evidence as a blocker for public current-state copy.
- Keep owner review separate from automated validation.

## Rollout And Rollback Plan

- Rollout: use this plan as input to later implementation-control packets.
- Migration: future public route work should build replacement surfaces before
  old route retirement.
- Rollback: revert the packet commit for planning-only changes; future public
  route rollback must follow the canonical greenfield rebuild plan.
- Deployment: out of scope until owner review and a separate deployment workflow
  authorize it.

## Out Of Scope

- Public route implementation.
- Public copy changes.
- Public assets and public manifests.
- Source snapshot or source bundle dataset refreshes.
- Generated HTML, Markdown, wiki, PDF, diagram, or retrieval-layer refreshes.
- Upstream source-project writes.
- Git push or Cloudflare deployment.

## Codex Task Packets

Task packets for future implementation work are in:

`ImplementationPlans/website-information-space/PRD-01-high-level-components-task-packets.md`

## Final Review Checklist

- [x] Source PRD is identified.
- [x] Requirements are mapped to implementation areas and future task IDs.
- [x] Canonical greenfield rebuild constraints are preserved.
- [x] Display-spelling rule is preserved.
- [x] Source Authority Boundary is preserved.
- [x] Validation commands are discovered from the repository.
- [x] Product questions are separated from implementation decisions.
- [x] The plan avoids direct public route implementation.

## References

The Æther Flow Website. (2026). *High-Level Components* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
