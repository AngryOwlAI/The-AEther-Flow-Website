# Implementation Plan: PRD-02 Physics and Mathematical Components

## Source PRD

- Source: `PRDs/website-information-space/PRD-02-physics-and-mathematical-components.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines the website requirements for explaining the physics and mathematical side of The Æther Flow Project. It covers the Æther / Æther-flow ontology, exact-GR benchmark, adoption-versus-derivation boundary, flow-geometry dictionary, GR derivation roadmap, current claim-status tables, negative-result preservation, and "what remains open" explanations.

Physics pages need to make the project technically legible without turning interpretive and roadmap material into proof. A reader should understand:

This sub implementation plan maps `PRD-02` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for physics, mathematics, exact-gr benchmark, and open burdens and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-02-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-02-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-02-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-02-Q-001 | Planning assumption | Should the first physics implementation include a full derivation-roadmap | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-02-Q-002 | Planning assumption | Which equations should be rendered directly on the website, and which should | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-02-Q-003 | Planning assumption | Should the flow-geometry dictionary be visual, tabular, or both? | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-02-Q-004 | Planning assumption | Should current claim-status tables live in physics pages, current-frontier | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-02-REQ-001 | Explain Æther, Æther-flow, observed space, S-time, expansion, and gravity | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-002 | Explain the exact-GR benchmark package, including one operative metric and | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-003 | Explain the Einstein-Hilbert effective action as adopted effective benchmark | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-004 | Explain congruence geometry as a disciplined interpretive dictionary. | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-005 | Explain source-side derivation milestones including source ontology, EqSrc, | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-006 | Explain negative-result preservation, obstruction records, and local freeze | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-007 | Require every physics page to expose a claim-status panel. | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-008 | Require every physics page to declare canonical source basis and derivative | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-009 | Require exact-GR pages to separate observer-facing benchmark claims from | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-REQ-010 | Require current-status physics pages to use dated snapshot and PRD-09 | Physics, mathematics, exact-GR benchmark, and open burdens; future route surfaces `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-02-TASK-01, PRD-02-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-02-NFR-001 | Scientific caution: Pages must use weaker language when source state is | Shared page contract, source bundles, validation, and review closeout. | PRD-02-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-02-NFR-002 | Mathematical clarity: Pages should define symbols, domains, assumptions, and | Shared page contract, source bundles, validation, and review closeout. | PRD-02-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-02-NFR-003 | Dimensional discipline: Any future displayed equation should include context | Shared page contract, source bundles, validation, and review closeout. | PRD-02-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-02-NFR-004 | Source traceability: Technical claims should link to registered TeX sources | Shared page contract, source bundles, validation, and review closeout. | PRD-02-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-02-NFR-005 | Reader comprehension: Physics explanations should proceed from ontology to | Shared page contract, source bundles, validation, and review closeout. | PRD-02-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-02-NFR-006 | Reversibility: Page requirements should allow future correction if upstream | Shared page contract, source bundles, validation, and review closeout. | PRD-02-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-02` requirements onto the greenfield route surfaces rather than the
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

- Every physics page has a claim-status panel.
- The exact-GR page clearly distinguishes benchmark adoption from derivation.
- The ontology page avoids naive ether-wind or three-dimensional medium
- The mathematical roadmap identifies which burdens are upstream and downstream.
- Current status pages are dated snapshots, not permanent scientific claims.
- The physics glossary defines key ontology, benchmark, geometry, and
- Adoption-versus-derivation language appears before deep technical claims.
- Pages do not claim matter coupling, Einstein-equation derivation,

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

`ImplementationPlans/website-information-space/PRD-02-physics-and-mathematical-components-task-packets.md`

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

The Æther Flow Website. (2026). *Physics and Mathematical Components* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
