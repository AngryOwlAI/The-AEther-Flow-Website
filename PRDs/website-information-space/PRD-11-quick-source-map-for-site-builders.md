---
prd_id: "PRD-11"
title: "Quick Source Map for Site Builders"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Site-builder guide, source bundle index, page-to-source mapping table, build-first checklist, contributor handoff guide, and staleness handling guide"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
  - "PRD-06-documentation-publication-and-website-components.md"
  - "PRD-08-folder-and-repository-topology-components.md"
  - "PRD-10-website-positioning-guidance.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-11: Quick Source Map for Site Builders

## 1. Summary

This PRD defines the quick source map future site builders, implementation
agents, and documentation maintainers should use when turning The AEther Flow
Project into public website pages. It covers the site-builder guide, source
bundle index, page-to-source mapping table, "Build from these first"
checklist, contributor handoff guide, and staleness handling guide.

The central product rule is that every planned page type must have a source
bundle before implementation starts. A source bundle identifies the primary
authority files, supporting source files, derivative seed material, relevant
PRDs, freshness policy, and forbidden inferences for that page family.

## 2. Product Purpose

The website PRD family now defines the public story, physics pages,
research-agent workflow pages, source-authority surfaces, publication process,
tooling, and repository topology. A site builder still needs a compact
operational map that answers one practical question: "For this page type, what
do I inspect first, what may I reuse, and what must I not infer?"

The website should help site builders:

- begin with the correct authority sources before using derivatives;
- pair page families with the right source bundles;
- avoid using generated HTML, GitHub-facing Markdown, wiki notes, local memory,
  or screenshots as source authority;
- apply PRD-09 freshness rules to current-frontier content;
- preserve the claim boundaries from PRD-05, PRD-06, PRD-08, and PRD-10;
- hand off implementation packets with enough provenance for reviewers to
  verify the page without reconstructing the repository.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, routing, publication, page-build, or
claim-promotion authority.

Source basis for implementation should include:

- `README.md`;
- `AGENTS.md`;
- `ontology/aether-and-aether-flow.md`;
- `ontology/tex/*.tex`;
- `registries/TEX_SOURCE_REGISTRY.csv`;
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`;
- `research_control/README.md`;
- `research_control/current_frontier.md`;
- `.codex/skills/`;
- `.agents/roles/`;
- `.agents/schemas/`;
- `github-facing/`;
- `html/`;
- `markdown/publication-briefs/`;
- `markdown/html-explainer-specs/`;
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`;
- `Makefile`;
- `requirements.txt`;
- `scripts/`;
- `tests/`;
- PRD-05, PRD-06, PRD-08, PRD-09, and PRD-10.

Site-builder pages may use generated derivatives as reader-friendly seed
material, but source bundles must point back to canonical or control sources
for claim-bearing copy. When source and derivative disagree, the builder must
inspect the source, registry, and current tracked control record.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| Site builder | Select the correct source bundle for a planned page before writing or implementing it. |
| Implementation agent | Know which files to inspect, which files may seed copy, and which files are out of authority. |
| Documentation maintainer | Prepare handoffs that include source basis, derivative use, freshness status, and validation expectations. |
| Reviewer | Verify that a proposed page maps to the right sources and avoids forbidden inferences. |
| Contributor | Understand where to begin when proposing a page, guide, dashboard, or publication-derived route. |
| General reader | Benefit from pages that are internally navigable and source-backed rather than repository archaeology. |

## 5. Scope

In scope:

- site-builder guide requirements;
- source bundle index requirements;
- page-to-source mapping table requirements;
- "Build from these first" checklist requirements;
- contributor handoff guide requirements;
- staleness handling guide requirements;
- source-bundle schema requirements;
- validation expectations for future page implementation packets.

Out of scope:

- implementing public routes;
- changing page navigation;
- changing public assets or manifests;
- refreshing source snapshots;
- regenerating HTML, GitHub-facing Markdown, PDFs, wiki notes, Obsidian, or
  `.local/` retrieval layers;
- editing upstream source files, registries, role contracts, schema contracts,
  skills, scripts, tests, or control records;
- promoting scientific, mathematical, governance, or research-workflow claims;
- pushing or deploying.

## 6. Non-Goals

This PRD must not:

- make source-map convenience a substitute for source inspection;
- treat reviewed GitHub-facing Markdown or tracked HTML as canonical authority;
- allow current-frontier content without a freshness policy;
- encourage route implementation before the PRD-family review is complete;
- hide uncertainty when source basis, claim status, or page family is unclear;
- imply that validators, tests, registries, generated derivatives, or local
  memory prove scientific claims;
- turn site-builder guidance into an unrestricted write authorization.

## 7. Website Surfaces

Required surfaces:

- Site-builder guide;
- Source bundle index;
- Page-to-source mapping table;
- "Build from these first" checklist;
- Contributor handoff guide;
- Staleness handling guide.

Supporting surfaces:

- source-bundle detail cards;
- page-family selector;
- source-versus-seed legend;
- forbidden-inference checklist;
- implementation handoff template;
- review readiness checklist;
- source freshness badge model.

## 8. Functional Requirements

1. Define a source-bundle schema for every planned page family.
2. Require every source bundle to identify primary authority sources,
   supporting sources, derivative seed material, relevant PRDs, freshness
   policy, validation expectations, and forbidden inferences.
3. Provide source bundles for project overview pages.
4. Provide source bundles for physics pages.
5. Provide source bundles for AI research-agent pages.
6. Provide source bundles for source-authority pages.
7. Provide source bundles for current-frontier pages.
8. Provide source bundles for operator and contributor pages.
9. Provide source bundles for website publication pages.
10. Require source-first inspection before derivative reuse.
11. Require generated GitHub-facing Markdown and tracked HTML to be labeled as
    reader-facing seed material, not canonical authority.
12. Require current-frontier content to include source precedence, inspection
    date, staleness behavior, and refresh trigger.
13. Require page implementation handoffs to name inspected source files,
    derivative seeds used, relevant PRDs, claim boundaries, validation
    commands, and any skipped checks.
14. Require source-bundle pages to keep internal website routes primary while
    preserving source and GitHub links as provenance.
15. Require source-map implementation to avoid copying long source excerpts,
    generated registry tables, or stale file inventories into public pages.
16. Require a "do not build from this alone" warning for local memory, wiki,
    PDFs, generated HTML, GitHub-facing Markdown, screenshots, and validator
    output.
17. Require all source bundles to state whether human-gated promotion is
    relevant before a claim can change status.
18. Require a review readiness checklist before any future route packet uses a
    source bundle.
19. Require the final PRD-family review to verify that PRD-11 aligns with
    PRD-05 source authority, PRD-06 publication process, PRD-08 topology, and
    PRD-09 freshness rules.

## 9. Non-Functional Requirements

- Accuracy: Source bundles must be checked against current upstream files and
  registries before route implementation.
- Maintainability: The source map should be compact enough to keep current and
  specific enough to prevent authority drift.
- Safety: The guide must discourage claims built from derivatives, retrieval
  layers, or validator output alone.
- Traceability: Every bundle must point to source anchors and relevant PRDs.
- Freshness: Current-state and current-frontier bundles must include an
  inspection date and a refresh policy.
- Usability: Site builders should be able to select a page type without
  knowing the repository layout first.
- Reversibility: If a source bundle is wrong or stale, future implementation
  packets should be able to update the bundle without rewriting the entire PRD
  family.

## 10. Claim Boundary

This PRD may specify website content that explains:

- which source materials support planned page families;
- how source bundles map page types to upstream evidence;
- which generated derivatives can seed reader-facing copy;
- which freshness rules apply to current-frontier content;
- which validation checks should accompany future implementation packets.

This PRD must not authorize website content claiming:

- GR has been derived from AEther / AEther-flow;
- matter coupling, stress-energy semantics, Einstein equations, or exact-GR
  benchmark promotion have been completed;
- generated explainers, PDFs, wiki notes, screenshots, local memory,
  registries, validators, tests, PRDs, or source maps are scientific proof;
- a site-builder source bundle changes canonical source authority;
- derivative seed material may override source, registry, or control state.

## 11. Content Requirements

Every source bundle must use this structure:

```text
Page family:
Reader job:
Primary authority sources:
Supporting sources:
Derivative seed material:
Relevant PRDs:
Freshness policy:
Validation expectations:
Forbidden inferences:
Handoff requirements:
```

The source bundle index must include at least:

| Page family | Primary authority sources | Derivative seeds | Required PRDs |
| --- | --- | --- | --- |
| Project overview pages | `README.md`, `AGENTS.md`, `research_control/README.md`, publication process notes | `github-facing/project-overview-explainer.md`, `html/project-overview-explainer.html`, project overview brief/spec | PRD-01, PRD-05, PRD-06, PRD-10 |
| Physics pages | `ontology/aether-and-aether-flow.md`, `ontology/tex/*.tex`, `registries/TEX_SOURCE_REGISTRY.csv`, `registries/CLAIM_BOUNDARY_REGISTRY.csv` | physics GitHub-facing explainers, tracked HTML explainers, publication briefs, source specs | PRD-02, PRD-05, PRD-09, PRD-10 |
| AI research-agent pages | `research_control/README.md`, `.agents/roles/`, `.agents/schemas/`, `.codex/skills/`, task and registry sources | workflow, lifecycle, role, parent-child, and roles/skills explainers | PRD-03, PRD-04, PRD-05, PRD-07 |
| Source-authority pages | `AGENTS.md`, `registries/`, `FOLDER_MAP.md`, source and derivative registries | source-authority, memory-system, and repository-topology explainers | PRD-05, PRD-06, PRD-08 |
| Current-frontier pages | `research_control/current_frontier.md`, `research_control/program_state.yaml`, latest handoff, `registries/DISTANCE_TO_GR_LEDGER.csv` | dated current-state cards and reviewed explanatory derivatives only after source check | PRD-09, PRD-05, PRD-10 |
| Operator/contributor pages | `README.md`, `Makefile`, `requirements.txt`, `scripts/`, `tests/`, `.codex/skills/` | technical requirements, validator workflow, project-system improvement explainers | PRD-07, PRD-03, PRD-04, PRD-05 |
| Website publication pages | `markdown/publication-briefs/`, `markdown/html-explainer-specs/`, `registries/PUBLICATION_BRIEF_REGISTRY.csv` | `github-facing/`, `html/`, publication QA evidence | PRD-06, PRD-05, PRD-08, PRD-11 |

The "Build from these first" checklist must require:

1. identify the page family;
2. inspect the relevant PRD bundle;
3. inspect primary authority sources;
4. inspect supporting sources and registries;
5. choose derivative seed material only after source inspection;
6. write the claim boundary before the page draft;
7. write the freshness policy before using current-frontier content;
8. record source paths and inspection date in the implementation handoff;
9. run applicable validators for the implementation packet;
10. avoid push, deploy, route, asset, or manifest changes unless separately
    authorized by live control records.

The staleness guide must state:

- current-frontier content is freshness-sensitive;
- source precedence must be visible;
- stale current-frontier data should block or warn on publication depending on
  route severity;
- generated snapshots are not independent authority;
- current-state pages must identify the source inspection date and refresh
  trigger;
- PRD-09 governs detailed stale-data behavior.

## 12. UX and Navigation Requirements

The site-builder guide should:

- begin with a short source-authority warning;
- offer a page-family selector before source tables;
- show primary authority sources before derivative seeds;
- include a compact "build from these first" checklist near the top;
- let builders expand source-bundle detail cards only when needed;
- link to PRD-05, PRD-06, PRD-08, PRD-09, and PRD-10 for deeper rules;
- keep internal website routes primary and source/GitHub links as provenance;
- avoid showing internal process metadata as the primary public reader journey.

Recommended reader path:

| Reader | First path |
| --- | --- |
| Site builder | Page-family selector to source bundle card. |
| Implementation agent | Build-first checklist to handoff requirements. |
| Documentation maintainer | Publication bundle to contributor handoff guide. |
| Reviewer | Source bundle card to forbidden-inference checklist. |
| Contributor | Site-builder guide to source-authority and repository-topology pages. |

## 13. Data, Source, and Provenance Requirements

Future source-map pages should declare:

- page family;
- source bundle version or inspection date;
- primary authority source paths;
- supporting source paths;
- derivative seed paths;
- required PRDs;
- source freshness status;
- claim-boundary status;
- validators expected for implementation;
- route, asset, manifest, snapshot, or deployment gates that would require
  separate authorization;
- reviewer handoff requirements.

The source bundle index should be implementable as a structured dataset that
future route packets can validate. It should not embed full source text,
private local cache content, screenshots as evidence, or generated registry
tables as if they were canonical source.

## 14. User Stories

1. As a site builder, I want to select a page family and get the correct source
   bundle, so that I can start from authority rather than search results.
2. As an implementation agent, I want primary sources and derivative seeds
   separated, so that I do not write public claims from generated material
   alone.
3. As a reviewer, I want forbidden inferences listed per page family, so that I
   can detect overclaiming quickly.
4. As a documentation maintainer, I want a contributor handoff guide, so that
   future page work includes inspected sources, PRDs, freshness, and validation
   evidence.
5. As a contributor, I want a build-first checklist, so that I understand the
   safe order of inspection before proposing route work.
6. As a reader, I want pages built from source bundles, so that the website
   reads coherently without hiding provenance.

## 15. Acceptance Criteria

- A site builder can identify the right source for any planned page type.
- Every planned page family has a source bundle.
- Current-frontier content has a staleness and refresh policy.
- Site-builder docs preserve authority hierarchy.
- Generated derivatives are labeled as seed material, not canonical authority.
- Every source bundle includes forbidden inferences.
- Every source bundle points to relevant PRDs.
- The build-first checklist requires source inspection before derivative reuse.
- Contributor handoffs require source paths, inspection date, PRD references,
  claim boundaries, and validation expectations.
- The final PRD-family review can verify that all eleven sub-PRDs now exist and
  that PRD-11 aligns with the validation checklist.

## 16. Dependencies

- PRD-00 defines the master website information architecture and final PRD-set
  readiness criteria.
- PRD-05 defines source authority, registries, retrieval, and derivative
  boundaries.
- PRD-06 defines publication briefs, source specs, and generated reader
  surfaces.
- PRD-07 defines operator, validator, runtime, and local-cache boundaries.
- PRD-08 defines folder topology and edit/read policies.
- PRD-09 defines current-frontier freshness and stale-data behavior.
- PRD-10 defines safe public positioning and forbidden claim language.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Builders use derivative explainers as source authority. | Put primary authority sources before derivative seeds in every bundle. |
| Current-state pages drift from tracked frontier state. | Require PRD-09 staleness policy, inspection date, source precedence, and refresh triggers. |
| Source bundles become too broad to use. | Keep bundles page-family scoped and require only primary, supporting, derivative, PRD, freshness, and forbidden-inference fields. |
| Source-map tables become stale inventories. | Require live source inspection before route implementation and avoid copying long generated tables. |
| Operator pages accidentally imply tooling proves science. | Link to PRD-07 and repeat validator-as-operational-evidence language. |
| Physics pages overclaim derivation status. | Require PRD-02, PRD-09, and PRD-10 claim checks plus source inspection. |
| The PRD family is treated as complete before review. | Keep final PRD-family review as the next packet after PRD-11 checkpoint. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Confirm the page family and source bundle.
2. Inspect primary authority sources listed by the source bundle.
3. Inspect supporting sources and registries.
4. Confirm derivative seed material is treated as reader-facing support only.
5. Apply PRD-09 freshness checks for current-frontier content.
6. Apply PRD-10 forbidden-claim checks for public copy.
7. Confirm PRD-05, PRD-06, and PRD-08 classifications for source, derivative,
   local retrieval, and folder topology.
8. Confirm implementation handoff records source paths, inspection date,
   relevant PRDs, claim boundaries, validators, and skipped checks.
9. Run applicable route, content, provenance, build, browser, and
   implementation-control validators for implementation packets.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: implementation support foundation.

This PRD should be the last detailed sub-PRD because it depends on source
authority, publication process, repository topology, current-frontier rules,
and safe public positioning. After this PRD is checkpointed, the logical next
packet is a final PRD-family review against the index validation checklist.

## 20. Open Questions

1. Should source bundles be implemented as static Markdown tables, a small
   structured dataset, or generated from a reviewed source-bundle manifest?
2. Should route implementation packets require a machine-readable
   source-bundle receipt, or is a human-readable handoff sufficient at first?
3. Should general readers see the site-builder guide, or should it live under a
   contributor/operator route family?
4. Should current-frontier pages block rendering when stale, or render with a
   visible stale-data warning and no current-status claims?

These questions do not block this PRD. They should be resolved during the final
PRD-family review or future route implementation planning.

## 21. Definition of Done

This PRD is complete when:

- it defines site-builder guide, source bundle index, page-to-source mapping
  table, build-first checklist, contributor handoff guide, and staleness
  handling guide requirements;
- it provides source bundles for project overview, physics, AI research-agent,
  source-authority, current-frontier, operator/contributor, and website
  publication page families;
- it separates primary authority sources from derivative seed material;
- it requires current-frontier freshness and refresh policy;
- it requires contributor handoffs with source paths, inspection dates, PRD
  references, claim boundaries, and validation expectations;
- it preserves the authority hierarchy defined by PRD-05, PRD-06, PRD-08,
  PRD-09, and PRD-10.

## References

The AEther Flow Project. (2026). *Current research frontier* [Generated
control snapshot].

The AEther Flow Project. (2026). *Project README* [Repository overview].

The AEther Flow Project. (2026). *Publication brief registry* [CSV registry].

The AEther Flow Project. (2026). *Research control README* [Control
documentation].

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].
