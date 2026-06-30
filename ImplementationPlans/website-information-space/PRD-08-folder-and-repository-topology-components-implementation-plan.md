# Implementation Plan: PRD-08 Folder and Repository Topology Components

## Source PRD

- Source: `PRDs/website-information-space/PRD-08-folder-and-repository-topology-components.md`
- Master plan: `ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`
- Canonical rebuild plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

This PRD defines how The Æther Flow Website should explain the repository topology of The Æther Flow Project. It covers the repository topology map, folder explorer, source-lane diagram, "Where should I edit?" guide, "Where should I read?" guide, and generated-versus-canonical folder legend.

The Æther Flow Project is easier to misunderstand than a normal repository because it contains scientific source material, research-control state, registries, generated reader surfaces, role and schema contracts, workflow skills, deterministic tooling, archival material, and ignored local retrieval caches in the same tree.

This sub implementation plan maps `PRD-08` into the canonical greenfield rebuild
without implementing public routes in this packet. The plan constrains future
route packets for repository topology, folder families, and generated-versus-canonical boundaries and preserves the Source Authority Boundary.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, and Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` where available.
- Canonical implementation direction: the sitewide greenfield rebuild controls
  route model, page grammar, owner review, and old-route retirement sequencing.
- Relevant future route surfaces: `/resources/repository-map/`, `/resources/site-builder-guide/`.
- Repository rules: upstream source files and governed task records remain
  authoritative for scientific, mathematical, governance, and research-workflow
  claims. Website plans and pages are explanatory derivatives.
- Display-spelling rule: use `Æther` in reader-facing text and reserve `aether`
  for links, slugs, file naming, package names, repository paths, and other
  machine-facing identifiers.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| PRD-08-ASM-001 | Planning assumption | This packet creates planning outputs only. | The active implementation-control scope forbids public routes, assets, manifests, source refreshes, push, deploy, and upstream writes. | Public route implementation. |
| PRD-08-ASM-002 | Planning assumption | The greenfield route model is canonical for this PRD. | The master implementation plan and active control packet require the sitewide rebuild plan as the governing route and page grammar source. | Route packet design. |
| PRD-08-ASM-003 | Planning assumption | Source bundles will be created or inspected before claim-bearing copy is written. | The PRD family treats source authority and provenance as gating constraints. | Public copy implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| PRD-08-Q-001 | Planning assumption | Should the public folder explorer be manually curated from a small dataset, | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-08-Q-002 | Planning assumption | Should folder cards show registry row counts, or would that create | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-08-Q-003 | Planning assumption | Should local retrieval lanes be visible to general readers, or should they | Resolve before public route implementation if it affects copy, source, or route behavior. |
| PRD-08-Q-004 | Planning assumption | Should the source-lane diagram include reserved lanes such as `assets/`, | Resolve before public route implementation if it affects copy, source, or route behavior. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| PRD-08-REQ-001 | Classify every required folder into one or more reader-facing authority | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-002 | For every folder entry, provide purpose, authority class, edit policy, | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-003 | Explain `.agents/` as control authority for role contracts, schemas, | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-004 | Explain `.codex/` as tooling for repo-local skills, prompts, and current | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-005 | Explain `ontology/` as the active canonical scientific source lane for the | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-006 | Explain `legacy_ontology/` as archival source material retained for | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-007 | Explain `research_control/` as the tracked control spine for program state, | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-008 | Explain `registries/` as the machine-checkable ledger layer for source | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-009 | Explain `markdown/` as canonical Markdown source material for publication | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-010 | Explain `github-facing/` as generated source-backed Markdown for | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-011 | Explain `html/` as tracked generated standalone HTML explainers backed by | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-012 | Explain `wiki/` as generated object notes and indexes for navigation and | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-013 | Explain `scripts/` as deterministic tooling for project-control, | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-014 | Explain `tests/` as focused reliability checks for project-system and | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-015 | Explain `tex_shared/` as shared TeX support used by ontology or manuscript | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-016 | Explain `.local/` as ignored local retrieval, semantic extraction, | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-017 | Explain that generated derivatives and local retrieval layers can guide | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-018 | Provide a "Where should I edit?" guide that sends source changes to | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-019 | Provide a "Where should I read?" guide that allows human-readable | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-020 | Provide a site-builder orientation that identifies website seed material: | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-REQ-021 | Provide a stale-topology warning that tells implementers to re-check the | Repository topology, folder families, and generated-versus-canonical boundaries; future route surfaces `/resources/repository-map/`, `/resources/site-builder-guide/`. | PRD-08-TASK-01, PRD-08-TASK-02 | Planning checks now; future route packet uses content, links, layout, provenance, build, and browser QA. |
| PRD-08-NFR-001 | Accuracy: Folder pages must be reviewed against current upstream folders, | Shared page contract, source bundles, validation, and review closeout. | PRD-08-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-08-NFR-002 | Boundary clarity: Source, control, generated, local, tooling, archival, and | Shared page contract, source bundles, validation, and review closeout. | PRD-08-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-08-NFR-003 | Maintainability: The folder explorer should use stable classifications and | Shared page contract, source bundles, validation, and review closeout. | PRD-08-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-08-NFR-004 | Safety: Edit guides must discourage hand-editing generated derivatives and | Shared page contract, source bundles, validation, and review closeout. | PRD-08-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-08-NFR-005 | Traceability: Folder entries must point to source anchors and related PRDs. | Shared page contract, source bundles, validation, and review closeout. | PRD-08-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-08-NFR-006 | Freshness: Public topology pages must show an inspection date or refresh | Shared page contract, source bundles, validation, and review closeout. | PRD-08-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |
| PRD-08-NFR-007 | Accessibility: Diagrams must not require color alone to communicate source, | Shared page contract, source bundles, validation, and review closeout. | PRD-08-TASK-03 | Planning checks now; future implementation uses the canonical greenfield validation profile. |

## Proposed Technical Approach

1. Keep this packet planning-only and use it to constrain future implementation
   packets.
2. Map `PRD-08` requirements onto the greenfield route surfaces rather than the
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

- The repository topology map distinguishes source, control, generated, local,
- The folder explorer includes purpose, authority class, edit policy, website
- Contributors can identify where canonical edits belong.
- The website does not encourage hand-editing generated derivative outputs as
- `.local/` is labeled ignored, local, non-authoritative retrieval or QA state.
- `FOLDER_MAP.md` is labeled generated and noncanonical.
- `github-facing/`, `html/`, `wiki/`, `ontology/pdfs/`, and generated local
- `ontology/tex/` and relevant source materials are separated from generated
- `legacy_ontology/` is clearly archival and not the active authority lane.
- Topology pages link to PRD-05, PRD-06, PRD-07, and PRD-11 where memory,

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

`ImplementationPlans/website-information-space/PRD-08-folder-and-repository-topology-components-task-packets.md`

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

The Æther Flow Website. (2026). *Folder and Repository Topology Components* [Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family Validation Review* [Requirements-readiness review].
