# Implementation Plan: PRD-05 Memory, Registry, and Retrieval Components

## Source PRD

- Source: `PRDs/website-information-space/PRD-05-memory-registry-and-retrieval-components.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines website requirements for explaining The Æther Flow Project's source-first memory model, registries, retrieval layers, generated derivatives, and provenance graph.

The website needs a public source-authority and provenance system because the project is complex, source-rich, and easy to overread. Readers should be able to see which materials are canonical, which are derivatives, which are local retrieval support, and which claims require upstream verification.

This sub implementation plan maps `PRD-05` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for source authority, registries, memory, retrieval, and provenance and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-05-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-05-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-05-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-05-Q-001 | Planning assumption | Should future route implementation include a full registry explorer in the | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-05-Q-002 | Planning assumption | Should source/provenance footers be a shared component, page-frontmatter | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-05-Q-003 | Planning assumption | Should retrieval freshness warnings appear in public pages, maintainer-only | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-05-REQ-001 | Explain TeX source authority for physics claims. | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-002 | Explain Markdown source authority for authored documentation, contracts, | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-003 | Label PDFs, HTML explainers, GitHub-facing Markdown, and wiki pages as | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-004 | Classify `.local/` as local retrieval/cache state. | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-005 | Explain CSV registries as provenance, relationship, validation, and workflow | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-006 | Explain memory lookup as navigation, not authority. | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-007 | Require canonical source inspection before using retrieved hits in claim | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-008 | Require registry-driven dashboards to include "not scientific proof" | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-009 | Require generated surfaces to be visibly labeled as noncanonical when they | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-REQ-010 | Require every website page to expose a source/provenance footer or | Source authority, registries, memory, retrieval, and provenance; future route surfaces `/resources/source-authority/`, `/resources/registries/`, `/resources/retrieval-layers/`. | PRD-05-TASK-01, PRD-05-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-05-NFR-001 | Accuracy: Authority classes must be explicit and conservative. | Shared page contract, source bundles, validation, and review closeout. | PRD-05-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-05-NFR-002 | Auditability: Readers should be able to trace major claims to source anchors. | Shared page contract, source bundles, validation, and review closeout. | PRD-05-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-05-NFR-003 | Maintainability: Source classifications should align with registries and | Shared page contract, source bundles, validation, and review closeout. | PRD-05-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-05-NFR-004 | Resilience: Retrieval freshness warnings must not be confused with canonical | Shared page contract, source bundles, validation, and review closeout. | PRD-05-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-05-NFR-005 | Usability: Provenance surfaces should help readers navigate without forcing | Shared page contract, source bundles, validation, and review closeout. | PRD-05-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-05-NFR-006 | Safety: Generated derivatives must not silently become claim authority. | Shared page contract, source bundles, validation, and review closeout. | PRD-05-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-05` requirements onto the greenfield route surfaces rather than the
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

- Every website page has a source/provenance footer or equivalent visible
- Registry-driven dashboards include "not scientific proof" language.
- Generated surfaces are visibly labeled as noncanonical where appropriate.
- The source-authority page is linked from the homepage and technical sections.
- Memory lookup is described as navigation, not authority.
- `.local/`, Obsidian, SQLite, semantic extracts, and generated wiki layers are
- Canonical source inspection is required before retrieved hits affect public

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

`ImplementationPlans/website-information-space/PRD-05-memory-registry-and-retrieval-components-task-packets.md`

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

The Æther Flow Website. (2026). *Memory, Registry, and Retrieval Components* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
