# Implementation Plan: PRD-09 Current Research Frontier for Website Use

## Source PRD

- Source: `PRDs/website-information-space/PRD-09-current-research-frontier-for-website-use.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines how The Æther Flow Website should present current research frontier status without converting a moving control snapshot into stale permanent website truth.

Readers need a concise way to understand what the project is working on now, what remains blocked, and which source records govern that status. Without a frontier layer, readers must inspect control files directly. With an unsafe frontier layer, readers may overread a task, handoff, validation pass, or generated summary as scientific proof.

This sub implementation plan maps `PRD-09` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for current-frontier snapshots, blocked claims, and stale-data behavior and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-09-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-09-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-09-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-09-Q-001 | Planning assumption | What freshness threshold should the first public implementation use: | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-09-Q-002 | Planning assumption | Should stale current-frontier widgets hide transient IDs or display them with | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-09-Q-003 | Planning assumption | Should the first dashboard import from generated Markdown, a derived JSON | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-09-Q-004 | Planning assumption | Should source-disagreement failures block a build, block a release, or render | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-09-REQ-001 | Treat all current-state data as a dated snapshot. | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-002 | Display `last_source_refresh` or an equivalent timestamp on every current | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-003 | Display source basis and source-authority class near the dashboard title. | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-004 | Display the active task ID and latest handoff ID only as snapshot data. | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-005 | Display the current milestone and current burden as snapshot data. | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-006 | Display the next recommended action as routing context, not as website | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-007 | Show blocked claims prominently whenever progress status is shown. | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-008 | Explain that validation PASS indicates operational consistency, not | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-009 | Avoid permanent hard-coding of active task IDs, handoff IDs, route labels, | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-010 | Provide a stale-data warning if the dashboard has not been refreshed within | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-011 | Provide a stronger warning if required source files are missing, | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-012 | Keep current frontier pages updateable without rewriting core physics, | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-013 | Preserve source links as provenance while keeping the reader journey | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-REQ-014 | Require snapshot regeneration or verification before any release that | Current-frontier snapshots, blocked claims, and stale-data behavior; future route surfaces `/ai-research-system/current-state/`, `/physics/claim-status/`, `/physics/open-burdens/`. | PRD-09-TASK-01, PRD-09-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-09-NFR-001 | Freshness: Current-state pages must make age and source basis visible. | Shared page contract, source bundles, validation, and review closeout. | PRD-09-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-09-NFR-002 | Stability: Stable physics pages must not depend on transient active task | Shared page contract, source bundles, validation, and review closeout. | PRD-09-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-09-NFR-003 | Safety: Blocked-claim language must appear before or beside progress | Shared page contract, source bundles, validation, and review closeout. | PRD-09-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-09-NFR-004 | Maintainability: Frontier data should be supplied through a small data | Shared page contract, source bundles, validation, and review closeout. | PRD-09-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-09-NFR-005 | Auditability: Each visible current-state field should map back to a source | Shared page contract, source bundles, validation, and review closeout. | PRD-09-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-09-NFR-006 | Reversibility: A stale or contradictory snapshot should fail closed into a | Shared page contract, source bundles, validation, and review closeout. | PRD-09-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-09-NFR-007 | Accessibility: Snapshot tables and warning badges must use readable text, | Shared page contract, source bundles, validation, and review closeout. | PRD-09-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-09` requirements onto the greenfield route surfaces rather than the
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

- The status page includes `last_source_refresh` or an equivalent visible
- The status page says it is not independent source authority.
- The status system can be updated without rewriting core physics pages.
- Blocked claims are visible whenever progress status is shown.
- Validation status is described as operational consistency, not scientific
- Active task ID, handoff ID, current milestone, and next route are rendered as
- Stale, missing-source, and source-disagreement states have explicit warning
- Distance-to-GR rows expose control, mathematical, physical, promotion, and
- Implementation can fail closed when freshness or source precedence cannot be

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

`ImplementationPlans/website-information-space/PRD-09-current-research-frontier-for-website-use-task-packets.md`

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

The Æther Flow Website. (2026). *Current Research Frontier for Website Use* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
