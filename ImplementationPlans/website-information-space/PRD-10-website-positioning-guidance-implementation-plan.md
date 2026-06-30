# Implementation Plan: PRD-10 Website Positioning Guidance

## Source PRD

- Source: `PRDs/website-information-space/PRD-10-website-positioning-guidance.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines the public messaging system for The Æther Flow Website. It specifies safe positioning, homepage copy rules, approved vocabulary, forbidden claims, audience-specific pitch cards, trust-building language, and a copy QA checklist.

The positioning system exists so every public page can speak with one coherent voice:

This sub implementation plan maps `PRD-10` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for positioning and public-language and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/`, `/physics/`, `/ai-research-system/`, `/resources/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.
- Discovered validation commands: `git diff --check`,
  `npm run validate:implementation-control`, `.venv/bin/python -m pytest`,
  `npm run validate:content`, `npm run validate:links`,
  `npm run validate:layout`, `npm run validate:provenance`,
  `npm run validate:comprehension`, `npm run validate:svg`,
  `npm run validate:manifests`, `npm run build`, `npm run validate`, and
  `npm run quality`.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-10-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-10-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-10-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-10-Q-001 | Planning assumption | Should the homepage use the safe pitch verbatim, or should it use a shorter | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-10-Q-002 | Planning assumption | Should copy QA be enforced by a future validator, a checklist, or both? | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-10-Q-003 | Planning assumption | Which route should own the trust/transparency block: Home, Source Authority, | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-10-REQ-001 | Provide the baseline safe pitch for first-viewport and overview use. | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-REQ-002 | Define approved phrases that can be reused across public pages. | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-REQ-003 | Define forbidden phrases that must be blocked during copy review. | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-REQ-004 | Require homepage hero copy to state the dual mission, exact-GR status, and | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-REQ-005 | Require audience-specific pitch variants for general readers, physicists, | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-REQ-006 | Require a trust-and-transparency block explaining what the project claims, | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-REQ-007 | Require every public page to check claims-to-use and claims-to-avoid before | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-REQ-008 | Require copy to distinguish operational validation from scientific proof. | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-REQ-009 | Require source/provenance links to support claims without replacing the | Positioning and public-language; future route surfaces `/`, `/physics/`, `/ai-research-system/`, `/resources/`. | PRD-10-TASK-01, PRD-10-TASK-02 | Planning packet checks now; future route packet uses content, links, layout, provenance, build, and browser QA as applicable. |
| PRD-10-NFR-001 | Precision: Copy must use explicit claim-status language. | Shared page contract, source bundles, validation, and review closeout. | PRD-10-TASK-03 | Planning packet checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-10-NFR-002 | Consistency: Shared pages should use the same approved vocabulary for the | Shared page contract, source bundles, validation, and review closeout. | PRD-10-TASK-03 | Planning packet checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-10-NFR-003 | Reversibility: Copy guidance should remain usable before and after route | Shared page contract, source bundles, validation, and review closeout. | PRD-10-TASK-03 | Planning packet checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-10-NFR-004 | Maintainability: Forbidden phrases should be searchable in review. | Shared page contract, source bundles, validation, and review closeout. | PRD-10-TASK-03 | Planning packet checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-10-NFR-005 | Safety: When uncertain, copy must choose the weaker claim. | Shared page contract, source bundles, validation, and review closeout. | PRD-10-TASK-03 | Planning packet checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-10-NFR-006 | Reader trust: Caution should be presented as part of the project's operating | Shared page contract, source bundles, validation, and review closeout. | PRD-10-TASK-03 | Planning packet checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-10` requirements onto the greenfield route surfaces rather than the
   older route tree.
3. Require future route packets to inspect source bundles before public copy is
   written.
4. Use narrative bands, evidence rails, status dossiers, matrices, tables,
   timelines, glossaries, or diagrams according to the information type.
5. Preserve internal-first navigation and use GitHub or source links as
   provenance rather than primary reader journeys.
6. Require future closeouts to name validators, browser QA, source-bundle
   evidence, and owner-review status where public routes change.

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

- Homepage hero copy states dual mission, exact-GR status, and open derivation
- Promotional copy does not overclaim scientific status.
- Every public-facing page has a claims-to-use and claims-to-avoid check.
- The site positions caution as credibility.
- Approved phrases appear in the copy guidance.
- Forbidden phrases are listed as blocked unless tracked authority changes.
- AI-system copy avoids autonomous-proof framing.
- Validator and handoff language is framed as operational evidence, not

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
- Add source-refresh or snapshot checks only under fresh authorization.

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

`ImplementationPlans/website-information-space/PRD-10-website-positioning-guidance-task-packets.md`

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

The Æther Flow Website. (2026). *Website Positioning Guidance* [Product requirements
document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation
plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family
Validation Review* [Requirements-readiness review].
