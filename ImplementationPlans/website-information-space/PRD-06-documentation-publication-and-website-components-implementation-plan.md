# Implementation Plan: PRD-06 Documentation, Publication, and Website Components

## Source PRD

- Source: `PRDs/website-information-space/PRD-06-documentation-publication-and-website-components.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines the website requirements for the documentation and publication system behind The Æther Flow Website. It covers publication workflow, source specs, publication briefs, generated GitHub-facing Markdown, tracked HTML explainers, page-type templates, library surfaces, parity checks, visual strategy, and source-backed page footer design.

The website needs a repeatable publication system because the project already contains multiple reader-facing output layers: Markdown source specs, publication briefs, GitHub-facing Markdown explainers, tracked HTML explainers, PDF derivatives, registry rows, and source-authority pages.

This sub implementation plan maps `PRD-06` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for publication, derivatives, library, and documentation workflow and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-06-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-06-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-06-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-06-Q-001 | Planning assumption | Should the first implementation expose a full publication workflow page, or | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-06-Q-002 | Planning assumption | Should source-spec and publication-brief templates be rendered as public | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-06-Q-003 | Planning assumption | Should the library organize first by reader journey, source type, topic, or | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-06-Q-004 | Planning assumption | What minimum browser QA evidence should be required when a publication page | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-06-REQ-001 | Define page-type requirements for project overview pages, concept | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-002 | Require every major planned page to declare audience, reader job, source | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-003 | Require a source-spec model for pages derived from `markdown/html-explainer-specs/`. | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-004 | Require a publication-brief model for reader job, document type, narrative | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-005 | Require GitHub-facing Markdown, tracked HTML, and website pages derived from | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-006 | Require tracked HTML explainers to remain generated noncanonical reader | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-007 | Require website page templates to foreground subject matter before process | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-008 | Require visual strategies to be page-specific and source-backed rather than | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-009 | Require a source-backed footer or equivalent provenance note on every major | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-REQ-010 | Require publication validation to distinguish structural compliance from | Publication, derivatives, library, and documentation workflow; future route surfaces `/resources/generated-derivatives/`, `/resources/publication-process/`, `/resources/library/`, `/resources/diagrams/`. | PRD-06-TASK-01, PRD-06-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-06-NFR-001 | Accuracy: Publication pages must preserve source hierarchy and claim | Shared page contract, source bundles, validation, and review closeout. | PRD-06-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-06-NFR-002 | Editorial quality: Pages should explain the project, not merely describe the | Shared page contract, source bundles, validation, and review closeout. | PRD-06-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-06-NFR-003 | Maintainability: Templates should reduce repeated decisions without forcing a | Shared page contract, source bundles, validation, and review closeout. | PRD-06-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-06-NFR-004 | Auditability: Each published page should point to its source spec, | Shared page contract, source bundles, validation, and review closeout. | PRD-06-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-06-NFR-005 | Portability: The publication process should support static website pages and | Shared page contract, source bundles, validation, and review closeout. | PRD-06-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-06-NFR-006 | Reversibility: A page can be revised by updating the source spec and brief, | Shared page contract, source bundles, validation, and review closeout. | PRD-06-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-06` requirements onto the greenfield route surfaces rather than the
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

- Every planned publication page has a source basis and claim boundary.
- The publication process distinguishes reader surfaces from canonical
- No tracked HTML, GitHub-facing Markdown, generated wiki, or publication page
- The website system can reuse existing explainer content while preserving
- Every major planned page declares audience, reader job, source basis, claim
- Page templates prioritize subject-first explanation over self-referential
- Publication validators are described as process and parity checks, not proof

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

`ImplementationPlans/website-information-space/PRD-06-documentation-publication-and-website-components-task-packets.md`

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

The Æther Flow Website. (2026). *Documentation, Publication, and Website Components* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
