# Implementation Plan: PRD-04 Role and Schema Components

## Source PRD

- Source: `PRDs/website-information-space/PRD-04-role-and-schema-components.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines how The Æther Flow Website should explain project roles, role authority, execution-role records, and schema contracts. It covers the role catalogue, role authority inspector, schema reference map, "who can make which claim?" matrix, and human-gated role explainer required by the website PRD system.

The Æther Flow Project uses named roles and schemas to keep research work bounded, auditable, and hard to overread. Readers need a clear map of which roles route work, construct draft/control artifacts, audit hidden imports, repair project-control systems, or require explicit human approval.

This sub implementation plan maps `PRD-04` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for roles, schemas, authority classes, and human-gated promotion and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-04-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-04-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-04-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-04-Q-001 | Planning assumption | Should role metadata be rendered from registry data at build time or kept as | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-04-Q-002 | Planning assumption | Should the authority inspector be a standalone route, a reusable component, | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-04-Q-003 | Planning assumption | Should role detail pages include recent execution examples, or should | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-04-Q-004 | Planning assumption | Should schema pages show full required-field tables or reader-first summaries | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-04-REQ-001 | Provide a role catalogue that includes, at minimum, Director of Research, | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-002 | Provide a schema reference map that includes Role Schema, Director Decision | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-003 | For every role page, include the same four reader questions: "can do," | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-004 | Resolve active role versions from `AGENT_ROLE_REGISTRY.csv` and label | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-005 | Explain that registered role contracts are stable templates, while | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-006 | Explain `registered_role`, `task_overlay`, and `one_job_provisional_role` | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-007 | Explain that a task overlay may narrow, constrain, or task-bind a role, but | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-008 | Explain that one-job provisional roles expire after their owning AgentJob | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-009 | Explain that schemas are control contracts with required fields, | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-010 | Explain that AgentJobs are bounded executable contracts and immutable after | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-011 | Explain that Director Decision Records preserve routing reasoning and | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-012 | Explain that documentation-impact records account for project-system | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-013 | Explain that the Gate Chair is defined but paused; execution and any | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-014 | Explain that physics roles may produce draft/control outputs, audits, | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-015 | Explain that project-control roles can modify allowed control or tooling | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-016 | Explain that registries support provenance, validation, and historical | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-017 | Provide a claim-authority matrix that separates routing authority, | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-REQ-018 | Provide links from role/schema pages to PRD-03 workflow concepts, PRD-05 | Roles, schemas, authority classes, and human-gated promotion; future route surfaces `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`. | PRD-04-TASK-01, PRD-04-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-04-NFR-001 | Accuracy: Role and schema pages must be generated or reviewed against active | Shared page contract, source bundles, validation, and review closeout. | PRD-04-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-04-NFR-002 | Version awareness: The UI must distinguish active, superseded, historical, | Shared page contract, source bundles, validation, and review closeout. | PRD-04-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-04-NFR-003 | Auditability: Every authority claim should map to a source role contract, | Shared page contract, source bundles, validation, and review closeout. | PRD-04-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-04-NFR-004 | Safety: Claim-boundary language must be adjacent to authority language. | Shared page contract, source bundles, validation, and review closeout. | PRD-04-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-04-NFR-005 | Maintainability: Pages should describe stable artifact classes and active | Shared page contract, source bundles, validation, and review closeout. | PRD-04-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-04-NFR-006 | Comprehension: Readers should see the authority model before low-level | Shared page contract, source bundles, validation, and review closeout. | PRD-04-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-04-NFR-007 | Reversibility: Future role or schema changes should update the catalogue | Shared page contract, source bundles, validation, and review closeout. | PRD-04-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-04` requirements onto the greenfield route surfaces rather than the
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

- The role catalogue includes all required roles from this PRD.
- Every role page includes "can do," "cannot do," "outputs," and "claim
- The Gate Chair page states that protected scientific promotion requires
- Schema pages explain schemas as control contracts, not decorative
- No role is presented as having authority beyond its registered contract and
- Active role versions are resolved from `AGENT_ROLE_REGISTRY.csv` or clearly
- Superseded role versions are not presented as current defaults.
- The claim-authority matrix states that roles, registries, validators, and
- Execution-role pages distinguish registered roles, task overlays, and
- Current examples follow PRD-09 freshness and stale-data rules.

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

`ImplementationPlans/website-information-space/PRD-04-role-and-schema-components-task-packets.md`

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

The Æther Flow Website. (2026). *Role and Schema Components* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
