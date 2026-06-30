# Implementation Plan: PRD-11 Quick Source Map for Site Builders

## Source PRD

- Source: `PRDs/website-information-space/PRD-11-quick-source-map-for-site-builders.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines the quick source map future site builders, implementation agents, and documentation maintainers should use when turning The Æther Flow Project into public website pages. It covers the site-builder guide, source bundle index, page-to-source mapping table, "Build from these first" checklist, contributor handoff guide, and staleness handling guide.

The website PRD family now defines the public story, physics pages, research-agent workflow pages, source-authority surfaces, publication process, tooling, and repository topology. A site builder still needs a compact operational map that answers one practical question: "For this page type, what do I inspect first, what may I reuse, and what must I not infer?"

This sub implementation plan maps `PRD-11` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for source map, page-to-source checklist, and site-builder handoff and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-11-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-11-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-11-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-11-Q-001 | Planning assumption | Should source bundles be implemented as static Markdown tables, a small | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-11-Q-002 | Planning assumption | Should route implementation packets require a machine-readable | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-11-Q-003 | Planning assumption | Should general readers see the site-builder guide, or should it live under a | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-11-Q-004 | Planning assumption | Should current-frontier pages block rendering when stale, or render with a | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-11-REQ-001 | Define a source-bundle schema for every planned page family. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-002 | Require every source bundle to identify primary authority sources, | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-003 | Provide source bundles for project overview pages. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-004 | Provide source bundles for physics pages. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-005 | Provide source bundles for AI research-agent pages. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-006 | Provide source bundles for source-authority pages. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-007 | Provide source bundles for current-frontier pages. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-008 | Provide source bundles for operator and contributor pages. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-009 | Provide source bundles for website publication pages. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-010 | Require source-first inspection before derivative reuse. | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-011 | Require generated GitHub-facing Markdown and tracked HTML to be labeled as | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-012 | Require current-frontier content to include source precedence, inspection | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-013 | Require page implementation handoffs to name inspected source files, | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-014 | Require source-bundle pages to keep internal website routes primary while | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-015 | Require source-map implementation to avoid copying long source excerpts, | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-016 | Require a "do not build from this alone" warning for local memory, wiki, | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-017 | Require all source bundles to state whether human-gated promotion is | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-018 | Require a review readiness checklist before any future route packet uses a | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-REQ-019 | Require the final PRD-family review to verify that PRD-11 aligns with | Source map, page-to-source checklist, and site-builder handoff; future route surfaces `/resources/site-builder-guide/`, `/resources/reading-paths/`, `/resources/repository-map/`. | PRD-11-TASK-01, PRD-11-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-11-NFR-001 | Accuracy: Source bundles must be checked against current upstream files and | Shared page contract, source bundles, validation, and review closeout. | PRD-11-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-11-NFR-002 | Maintainability: The source map should be compact enough to keep current and | Shared page contract, source bundles, validation, and review closeout. | PRD-11-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-11-NFR-003 | Safety: The guide must discourage claims built from derivatives, retrieval | Shared page contract, source bundles, validation, and review closeout. | PRD-11-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-11-NFR-004 | Traceability: Every bundle must point to source anchors and relevant PRDs. | Shared page contract, source bundles, validation, and review closeout. | PRD-11-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-11-NFR-005 | Freshness: Current-state and current-frontier bundles must include an | Shared page contract, source bundles, validation, and review closeout. | PRD-11-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-11-NFR-006 | Usability: Site builders should be able to select a page type without | Shared page contract, source bundles, validation, and review closeout. | PRD-11-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-11-NFR-007 | Reversibility: If a source bundle is wrong or stale, future implementation | Shared page contract, source bundles, validation, and review closeout. | PRD-11-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-11` requirements onto the greenfield route surfaces rather than the
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

- A site builder can identify the right source for any planned page type.
- Every planned page family has a source bundle.
- Current-frontier content has a staleness and refresh policy.
- Site-builder docs preserve authority hierarchy.
- Generated derivatives are labeled as seed material, not canonical authority.
- Every source bundle includes forbidden inferences.
- Every source bundle points to relevant PRDs.
- The build-first checklist requires source inspection before derivative reuse.
- Contributor handoffs require source paths, inspection date, PRD references,
- The final PRD-family review can verify that all eleven sub-PRDs now exist and

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

`ImplementationPlans/website-information-space/PRD-11-quick-source-map-for-site-builders-task-packets.md`

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

The Æther Flow Website. (2026). *Quick Source Map for Site Builders* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
