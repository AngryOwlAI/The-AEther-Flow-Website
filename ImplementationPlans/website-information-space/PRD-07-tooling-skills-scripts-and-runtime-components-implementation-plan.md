# Implementation Plan: PRD-07 Tooling, Skills, Scripts, and Runtime Components

## Source PRD

- Source: `PRDs/website-information-space/PRD-07-tooling-skills-scripts-and-runtime-components.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines how The Æther Flow Website should explain the tooling, skills, scripts, validators, runtime requirements, reproducibility workflow, and local-cache boundary used by The Æther Flow Project. It covers technical requirements pages, skills catalogues, script catalogues, validator/operator workflow pages, Makefile command references, runtime environment pages, and reproducibility guides.

The Æther Flow Project is unusually tooling-rich because it is both a physics research project and an AI research-agent system. Readers need a clear, bounded explanation of how operators reproduce the project state, run validators, inspect source-backed memory, understand repo-local skills, and avoid overclaiming from green checks.

This sub implementation plan maps `PRD-07` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for tooling, skills, scripts, validators, runtime, and reproducibility and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-07-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-07-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-07-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-07-Q-001 | Planning assumption | Should command references be generated from source command metadata or kept | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-07-Q-002 | Planning assumption | Should the contributor path include a single "safe read-only" command set | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-07-Q-003 | Planning assumption | Should validator pages include recent example failures, or should examples | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-07-Q-004 | Planning assumption | Should runtime pages distinguish website repo requirements from upstream | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-07-REQ-001 | Explain the Codex app harness as the current governed AI-agent execution | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-002 | Explain that future harness replacement would need to preserve tracked | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-003 | Explain the `continue-research` skill as the research-control continuation | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-004 | Explain the `improve-project-system` skill as the project-system repair | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-005 | Explain the `project-memory-system` skill as the owner of memory, registry, | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-006 | Explain the `html-visual-explainer` workflow as the governed tracked-HTML | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-007 | Explain the `visual-explainer` skill as local visual documentation support, | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-008 | Explain the `user-modified-project` skill as the router for human-made | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-009 | Explain Markdown, Obsidian, TeX, PDF, and ontology-support skills as | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-010 | Explain research-control scripts, including continuation, latest-handoff | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-011 | Explain project-control scripts, including change classification, | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-012 | Explain memory bootstrap and query tools, including bootstrap refresh, | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-013 | Explain validators and tests as deterministic reliability checks, not | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-014 | Explain Makefile targets as operator convenience wrappers around existing | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-015 | Explain the Python runtime requirement, including `.venv`, Python 3.12.13 | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-016 | Explain diagram and screenshot tooling requirements only where governed | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-017 | Explain `.local/` as ignored local retrieval, vault, preview, semantic, | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-018 | For every command page, state what the command validates or changes and | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-019 | For contributor paths, show minimum setup, common validation commands, and | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-REQ-020 | For operator paths, identify which workflows require a completion record, | Tooling, skills, scripts, validators, runtime, and reproducibility; future route surfaces `/ai-research-system/runtime-requirements/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/validators-and-handoffs/`. | PRD-07-TASK-01, PRD-07-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-07-NFR-001 | Accuracy: Tooling pages must be reviewed against current source skills, | Shared page contract, source bundles, validation, and review closeout. | PRD-07-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-07-NFR-002 | Safety: Validator and test pages must place non-proof language next to | Shared page contract, source bundles, validation, and review closeout. | PRD-07-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-07-NFR-003 | Reproducibility: Command pages should include preconditions, expected | Shared page contract, source bundles, validation, and review closeout. | PRD-07-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-07-NFR-004 | Maintainability: Pages should describe command families and source locations | Shared page contract, source bundles, validation, and review closeout. | PRD-07-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-07-NFR-005 | Boundary clarity: Source, derivative, retrieval, QA, and cache artifacts | Shared page contract, source bundles, validation, and review closeout. | PRD-07-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-07-NFR-006 | Security and integrity: Pages must not encourage manual edits to generated | Shared page contract, source bundles, validation, and review closeout. | PRD-07-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-07-NFR-007 | Portability: Runtime pages should distinguish documented current setup from | Shared page contract, source bundles, validation, and review closeout. | PRD-07-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-07` requirements onto the greenfield route surfaces rather than the
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

- The technical requirements page explains Codex app, Python `.venv`,
- The skills catalogue includes the required skills and states each skill's
- The script catalogue distinguishes research-control, project-control, memory,
- Every command page says what the command validates and what it does not
- Validator pages never imply proof, derivation, source-law adoption, benchmark
- Contributor paths show minimum setup, common validation, and where evidence
- The Makefile reference describes each target as a wrapper over source
- The runtime page distinguishes current documented setup from future possible
- The local-cache page states that `.local/`, Obsidian, semantic extracts, and
- Tooling pages link to PRD-03, PRD-04, PRD-05, PRD-08, and PRD-11 where their

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

`ImplementationPlans/website-information-space/PRD-07-tooling-skills-scripts-and-runtime-components-task-packets.md`

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

The Æther Flow Website. (2026). *Tooling, Skills, Scripts, and Runtime Components* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
