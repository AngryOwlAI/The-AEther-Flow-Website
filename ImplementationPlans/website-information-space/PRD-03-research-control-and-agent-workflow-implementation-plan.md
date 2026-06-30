# Implementation Plan: PRD-03 Research-Control and Agent Workflow

## Source PRD

- Source: `PRDs/website-information-space/PRD-03-research-control-and-agent-workflow.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines how The Æther Flow Website should explain the governed AI research-control workflow. It covers Director decisions, AgentJob contracts, execution-role records, the one-job rule, memory preflight, parent-child parallel synthesis, completion records, handoffs, validators, Distance-to-GR status updates, and the boundary between operational validation and scientific proof.

The Æther Flow Project uses a controlled research-agent system because the research program is speculative, mathematically delicate, and easy to overread. The website should make that system understandable without exposing readers to raw control files first.

This sub implementation plan maps `PRD-03` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for research-control workflow, agentjobs, handoffs, validators, and distance-to-gr and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-03-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-03-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-03-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-03-Q-001 | Planning assumption | Should the first public workflow page include a full AgentJob schema table or | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-03-Q-002 | Planning assumption | Should parent-child synthesis be shown in the main lifecycle diagram or in a | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-03-Q-003 | Planning assumption | Should example control records be pulled from a dated snapshot bundle or | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-03-Q-004 | Planning assumption | Should the validation panel group research-control, documentation-impact, | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-03-REQ-001 | Explain the one-job rule: a continuation invocation may set up or execute at | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-002 | Explain Director Decision Records as auditable routing records with | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-003 | Explain AgentJob contracts as immutable executable YAML contracts for one | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-004 | Explain execution-role records as task-local authority contracts that bind an | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-005 | Explain memory preflight as navigation and source-inspection support, not as | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-006 | Explain parent-child parallel synthesis for physics jobs as internal | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-007 | Explain completion records as receipts for outputs, validators, memory | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-008 | Explain handoffs as durable state-transfer records that preserve result, | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-009 | Explain Distance-to-GR status matrix and delta as progress accounting for | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-010 | Explain that validator PASS means operational consistency, not scientific | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-011 | Explain local failures, obstructions, and freezes as preserved routing | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-012 | Explain bounded theoretical continuation as the alternative to generic | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-REQ-013 | Explain that protected promotion, benchmark closure, canonical ontology | Research-control workflow, AgentJobs, handoffs, validators, and Distance-to-GR; future route surfaces `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/validators-and-handoffs/`. | PRD-03-TASK-01, PRD-03-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-03-NFR-001 | Auditability: Every workflow explanation should map to a named control | Shared page contract, source bundles, validation, and review closeout. | PRD-03-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-03-NFR-002 | Safety: Claim-boundary language must be adjacent to workflow power language. | Shared page contract, source bundles, validation, and review closeout. | PRD-03-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-03-NFR-003 | Maintainability: Pages should describe stable artifact classes rather than | Shared page contract, source bundles, validation, and review closeout. | PRD-03-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-03-NFR-004 | Comprehension: Diagrams should show lifecycle and authority flow before | Shared page contract, source bundles, validation, and review closeout. | PRD-03-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-03-NFR-005 | Security and integrity: Pages should avoid suggesting that users bypass | Shared page contract, source bundles, validation, and review closeout. | PRD-03-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-03-NFR-006 | Reversibility: Future changes to roles or schemas should update workflow | Shared page contract, source bundles, validation, and review closeout. | PRD-03-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-03` requirements onto the greenfield route surfaces rather than the
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

- The workflow page includes a lifecycle diagram from current state to handoff.
- The page states that validator PASS does not equal scientific proof.
- The page explains why local failures are preserved without becoming global
- The page explains how bounded theoretical continuation prevents generic
- The page explains the one-job rule.
- The page explains Director Decision Records, AgentJobs, execution-role
- The page distinguishes workflow authority from physics claim authority.
- The page links current-state examples to PRD-09 freshness rules rather than

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

`ImplementationPlans/website-information-space/PRD-03-research-control-and-agent-workflow-task-packets.md`

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

The Æther Flow Website. (2026). *Research-Control and Agent Workflow* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
