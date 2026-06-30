---
prd_id: "PRD-08"
title: "Folder and Repository Topology Components"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Repository topology map, folder explorer, source-lane diagram, edit/read guides, and generated-versus-canonical folder legend"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
  - "PRD-06-documentation-publication-and-website-components.md"
  - "PRD-07-tooling-skills-scripts-and-runtime-components.md"
  - "PRD-10-website-positioning-guidance.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-08: Folder and Repository Topology Components

## 1. Summary

This PRD defines how The AEther Flow Website should explain the repository
topology of The AEther Flow Project. It covers the repository topology map,
folder explorer, source-lane diagram, "Where should I edit?" guide, "Where
should I read?" guide, and generated-versus-canonical folder legend.

The central product rule is that folder pages must classify every important
repository lane by purpose, authority class, edit policy, website use, and
source/derivative/cache status. Readers should be able to tell where canonical
edits belong, which folders are generated derivatives, which folders are local
retrieval support, and which folders exist for tooling or control rather than
scientific source authority.

## 2. Product Purpose

The AEther Flow Project is easier to misunderstand than a normal repository
because it contains scientific source material, research-control state,
registries, generated reader surfaces, role and schema contracts, workflow
skills, deterministic tooling, archival material, and ignored local retrieval
caches in the same tree.

The website should help readers understand:

- which folders carry canonical scientific source material;
- which folders carry canonical documentation or control material;
- which folders are tracked control authority;
- which folders are generated derivatives;
- which folders are local retrieval or QA support;
- which folders contain tooling, tests, runtime helpers, or support material;
- which folders are archival or reserved lanes;
- where contributors should edit source material;
- where readers should read explanatory derivatives;
- where site builders should find website seed material without treating it as
  stronger authority than the upstream sources permit.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, routing, folder-classification,
publication, or claim-promotion authority.

Source basis for implementation should include:

- `FOLDER_MAP.md`;
- `.agents/`;
- `.codex/`;
- `ontology/`;
- `legacy_ontology/`;
- `research_control/`;
- `registries/`;
- `markdown/`;
- `github-facing/`;
- `html/`;
- `wiki/`;
- `scripts/`;
- `tests/`;
- `tex_shared/`;
- `.local/`;
- `README.md`;
- `AGENTS.md`;
- `CONTEXT.md`;
- PRD-05, PRD-06, PRD-07, and PRD-11 when the topology page links to memory,
  publication, tooling, or site-builder concepts.

`FOLDER_MAP.md` is useful topology evidence, but it is generated and explicitly
not canonical authority. Folder pages should use it as an orientation and
cross-check surface, then point readers back to tracked source files,
registries, control records, role contracts, schemas, source specs, and
publication briefs as applicable.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand why the project has source, generated, control, tooling, archival, and local retrieval lanes. |
| Contributor | Identify where canonical edits belong and which generated outputs should not be hand-edited as authority. |
| Operator | Navigate control records, registries, validators, and generated surfaces without crossing write boundaries. |
| AI researcher | Inspect how repository topology supports a governed research-agent system. |
| Site builder | Locate source-backed website seed material while preserving claim and authority boundaries. |
| Reviewer | Check whether a proposed page cites the right source lane and labels derivative or local material correctly. |

## 5. Scope

In scope:

- repository topology map requirements;
- folder explorer requirements;
- source-lane diagram requirements;
- "Where should I edit?" guide requirements;
- "Where should I read?" guide requirements;
- generated-versus-canonical folder legend requirements;
- folder authority-class taxonomy;
- folder edit-policy requirements;
- website-use requirements for each folder family;
- cross-links to source authority, publication, tooling, and site-builder
  PRDs.

Out of scope:

- changing the upstream folder structure;
- editing upstream source files, registries, generated derivatives, or local
  caches;
- refreshing `FOLDER_MAP.md`, source snapshots, memory, wiki, Obsidian,
  semantic extracts, PDF derivatives, GitHub-facing Markdown, or HTML
  explainers;
- implementing public routes in this packet;
- adding new validators, scripts, tests, skills, or dependencies;
- changing public website navigation;
- promoting or weakening any scientific, mathematical, governance, or
  research-workflow claim;
- pushing or deploying.

## 6. Non-Goals

This PRD must not:

- treat `FOLDER_MAP.md` as canonical source authority;
- imply that a generated derivative folder is the correct place to make
  canonical scientific, mathematical, governance, or documentation edits;
- imply that `.local/` files are committed evidence or source authority;
- present wiki, Obsidian, semantic extract, PDF, HTML, or GitHub-facing
  derivatives as independent proof or claim-promotion mechanisms;
- collapse scientific source authority, control authority, generated
  derivatives, and retrieval support into one undifferentiated "documentation"
  category;
- encourage manual edits to generated folders when source specs, registries,
  or governed workflows are the correct route;
- imply that repository topology alone grants write permission.

## 7. Website Surfaces

Required surfaces:

- Repository topology map;
- Folder explorer;
- Source-lane diagram;
- "Where should I edit?" guide;
- "Where should I read?" guide;
- "Generated versus canonical" folder legend.

Supporting surfaces:

- folder authority-class matrix;
- folder detail cards;
- edit-policy table;
- source-to-derivative flow diagram;
- local retrieval and QA boundary explainer;
- site-builder source-orientation panel;
- folder relationship map connected to PRD-05, PRD-06, PRD-07, and PRD-11.

## 8. Functional Requirements

1. Classify every required folder into one or more reader-facing authority
   classes: canonical scientific source, canonical documentation/control
   source, tracked control authority, generated derivative, generated local
   retrieval, tooling/runtime, archival, or reserved/future lane.
2. For every folder entry, provide purpose, authority class, edit policy,
   website use, source/derivative/cache class, source anchors, and
   validator/refresh notes.
3. Explain `.agents/` as control authority for role contracts, schemas,
   permitted agent behavior, authority levels, and execution structures.
4. Explain `.codex/` as tooling for repo-local skills, prompts, and current
   Codex app workflow procedures.
5. Explain `ontology/` as the active canonical scientific source lane for the
   ontology, registered TeX sources, and related source materials, while
   labeling generated PDFs as derivatives.
6. Explain `legacy_ontology/` as archival source material retained for
   comparison, not the active authority lane.
7. Explain `research_control/` as the tracked control spine for program state,
   current frontier, approvals, tasks, AgentJobs, completions, handoffs,
   templates, and design records.
8. Explain `registries/` as the machine-checkable ledger layer for source
   files, derivatives, roles, jobs, decisions, claims, relationships, memory,
   and improvement signals.
9. Explain `markdown/` as canonical Markdown source material for publication
   briefs, HTML explainer specs, and other source-backed documentation.
10. Explain `github-facing/` as generated source-backed Markdown for
    repository browsing and external AI orientation, not canonical authority.
11. Explain `html/` as tracked generated standalone HTML explainers backed by
    source specs and publication briefs.
12. Explain `wiki/` as generated object notes and indexes for navigation and
    memory, with edits routed back to source files and registries.
13. Explain `scripts/` as deterministic tooling for project-control,
    research-control, validation, rendering, checkpoint, metrics, and
    publication/documentation audit work.
14. Explain `tests/` as focused reliability checks for project-system and
    memory tooling, not proof of scientific claims.
15. Explain `tex_shared/` as shared TeX support used by ontology or manuscript
    sources without creating independent physics claims.
16. Explain `.local/` as ignored local retrieval, semantic extraction,
    Obsidian, memory index, preview, render QA, PDF QA, and local HTML state.
17. Explain that generated derivatives and local retrieval layers can guide
    reading or verification but cannot override tracked source authority.
18. Provide a "Where should I edit?" guide that sends source changes to
    canonical sources, source specs, registries, control records, role/schema
    contracts, or governed workflows rather than generated outputs.
19. Provide a "Where should I read?" guide that allows human-readable
    derivatives while showing their provenance and non-authority boundaries.
20. Provide a site-builder orientation that identifies website seed material:
    `github-facing/`, `html/`, `markdown/publication-briefs/`,
    `markdown/html-explainer-specs/`, `registries/`,
    `research_control/current_frontier.md`, and the relevant PRDs.
21. Provide a stale-topology warning that tells implementers to re-check the
    live upstream tree and `FOLDER_MAP.md` before building public pages from
    this PRD.

## 9. Non-Functional Requirements

- Accuracy: Folder pages must be reviewed against current upstream folders,
  `FOLDER_MAP.md`, README project map, and relevant registries before public
  implementation.
- Boundary clarity: Source, control, generated, local, tooling, archival, and
  reserved lanes must be visually and textually distinct.
- Maintainability: The folder explorer should use stable classifications and
  source anchors rather than copying long generated folder-map tables.
- Safety: Edit guides must discourage hand-editing generated derivatives and
  local caches as authority.
- Traceability: Folder entries must point to source anchors and related PRDs.
- Freshness: Public topology pages must show an inspection date or refresh
  expectation because the upstream repository can change.
- Accessibility: Diagrams must not require color alone to communicate source,
  derivative, local, or control categories.

## 10. Claim Boundary

This PRD may specify website content that explains:

- repository folder families;
- authority classes and edit policies;
- source, derivative, cache, tooling, archival, and reserved lanes;
- where contributors should edit;
- where readers may read;
- how website builders should find source-backed material;
- why generated and local layers support navigation rather than authority.

This PRD must not authorize website content claiming:

- folder classification proves physics claims;
- generated folder-map rows, registries, wiki notes, PDFs, HTML explainers, or
  local caches are scientific proof;
- generated outputs can be edited directly to change canonical source claims;
- `.local/` data is committed evidence;
- archival ontology material supersedes the active ontology lane;
- tooling or tests promote `M_src`, `g_eff`, exact-GR benchmark status,
  matter coupling, Einstein equations, or first-principles derivation status.

## 11. Content Requirements

The folder explorer must include at least:

| Folder | Authority class | Edit policy | Website use |
| --- | --- | --- | --- |
| `.agents/` | Tracked control authority | Edit only through governed role/schema/project-control work. | Explain roles, schemas, execution boundaries, and claim authority. |
| `.codex/` | Tooling/runtime | Edit only through project-control or skill-maintenance packets. | Explain current workflow skills, prompts, and Codex harness procedures. |
| `ontology/` | Canonical scientific source plus generated PDFs | Edit source Markdown/TeX through governed source workflows; treat PDFs as derivatives. | Explain ontology, exact-GR benchmark sources, and source-to-PDF relationship. |
| `legacy_ontology/` | Archival source and derivative lane | Do not treat as active source unless a tracked source says so. | Explain historical comparison and archival status. |
| `research_control/` | Tracked control authority | Edit through Director decisions, AgentJobs, allowlists, validators, completions, and handoffs. | Explain current frontier, tasks, approvals, workflow state, and evidence receipts. |
| `registries/` | CSV authority and metadata ledger | Edit only through governed workflows with validation and receipts. | Explain provenance, source/derivative ledgers, role/task/job rows, and source maps. |
| `markdown/` | Canonical documentation/control source | Edit source specs and briefs through documentation-curator or governed workflows. | Explain publication briefs, HTML specs, and website seed source material. |
| `github-facing/` | Generated source-backed Markdown derivative | Regenerate from source-backed publication process; do not treat as canonical authority. | Provide reader-friendly source-backed orientation and website seed content. |
| `html/` | Tracked generated HTML derivative | Regenerate through governed HTML explainer workflow. | Provide closest existing analogue for public website explainers. |
| `wiki/` | Generated derivative and navigation layer | Regenerate from source objects and registries; do not edit as authority. | Support object browsing, relationship maps, and retrieval orientation. |
| `scripts/` | Tooling/runtime | Edit through project-control or validator/tooling work with tests. | Explain deterministic enforcement, validation, rendering, and checkpoint tooling. |
| `tests/` | Tooling/runtime reliability checks | Edit with relevant code changes; passing tests are operational evidence only. | Explain reliability coverage and test limitations. |
| `tex_shared/` | Source-support lane | Edit when shared TeX support changes are governed and validated. | Explain shared frontmatter/includes without independent physics claims. |
| `.local/` | Local retrieval and QA cache | Never treat as source authority; may be refreshed or cleaned locally. | Explain semantic extracts, Obsidian vault, memory indexes, previews, and QA caches. |

The authority-class legend must define:

| Class | Meaning | Reader warning |
| --- | --- | --- |
| canonical scientific source | Source material that may carry active scientific or mathematical claims when registered and governed. | Derivatives help reading but do not replace the source. |
| canonical documentation/control source | Source material for documentation, publication briefs, source specs, instructions, or governed workflow records. | Website copy must not silently strengthen it. |
| tracked control authority | Tasks, schemas, roles, approvals, program state, registries, validators, completions, and handoffs. | Controls workflow authority, not scientific truth by itself. |
| generated derivative | Human or agent-readable output generated from source material. | Read for orientation; edit sources and regenerate. |
| generated local retrieval | Ignored local semantic, Obsidian, memory, preview, or QA state. | Use for search and review; do not cite as authority. |
| tooling/runtime | Skills, scripts, tests, prompts, dependencies, and operator helpers. | Validates or automates workflow behavior, not physics proof. |
| archival | Historical source snapshots retained for comparison. | Do not treat as the active authority lane unless explicitly promoted. |
| reserved/future lane | Placeholder or support area without active registered authority. | Avoid building claims from it until source authority exists. |

The "Where should I edit?" guide must include:

- physics or mathematical claims: active registered source material such as
  ontology Markdown/TeX and associated registries, through governed workflows;
- role or schema behavior: `.agents/` and related registries, through
  project-control workflows;
- research workflow state: `research_control/` records and registries, through
  bounded AgentJobs;
- publication source specs: `markdown/publication-briefs/` and
  `markdown/html-explainer-specs/`;
- generated reader surfaces: edit the source spec or brief, then regenerate;
- local retrieval state: refresh or clean locally, but do not cite as source
  authority;
- website requirements: PRDs in the website repository, with upstream source
  links as provenance.

The "Where should I read?" guide must include:

- source-first paths for claims and governance;
- generated HTML and GitHub-facing pages for reader-friendly summaries;
- wiki and `.local/` layers for navigation and retrieval only;
- registries for source, derivative, role, task, job, relationship, and
  provenance lookups;
- current-frontier and handoff records for dated workflow state.

## 12. UX and Navigation Requirements

Topology navigation should:

- begin with a source-authority warning before folder details;
- group folders into source, control, generated, local, tooling, archival, and
  reserved lanes;
- expose edit and read policies side by side;
- show source-to-derivative flows from source specs and registries to
  GitHub-facing, HTML, PDF, wiki, and local retrieval layers;
- link memory and registry concepts back to PRD-05;
- link publication and generated derivative concepts back to PRD-06;
- link tooling/runtime folders back to PRD-07;
- link site-builder quick lookup forward to PRD-11;
- keep internal website routes primary while preserving source links as
  provenance;
- avoid implying that folder browsing is enough to make a source-authority
  decision.

Recommended reader path:

| Reader | First path |
| --- | --- |
| General reader | Generated-versus-canonical legend to repository topology map. |
| Contributor | "Where should I edit?" guide to folder explorer. |
| Operator | Control authority lane to registries, research-control, scripts, and validators. |
| AI researcher | Source-lane diagram to role/tool/control topology. |
| Site builder | Website seed material panel to PRD-11. |
| Reviewer | Folder detail card to source anchors and provenance records. |

## 13. Data, Source, and Provenance Requirements

Future topology pages should declare, for each folder:

- folder path;
- short purpose;
- authority class;
- source/derivative/cache/tooling/archival/reserved class;
- edit policy;
- website use;
- primary source anchors;
- related registry, if any;
- generated-from relationship, if any;
- refresh or validation expectation;
- whether the folder may be cited as claim authority;
- related PRDs.

Folder data should be implementable as a small structured dataset rather than
hard-coded prose scattered across pages. The dataset should be reviewed against
the current upstream tree before route implementation and should carry an
inspection date.

## 14. User Stories

1. As a contributor, I want to know where canonical edits belong, so that I do
   not hand-edit generated derivatives as if they were authority.
2. As a general reader, I want a simple folder legend, so that I can understand
   why source, generated, local, and control folders are different.
3. As an operator, I want edit policies for control and registry folders, so
   that I preserve AgentJob, validation, completion, and checkpoint discipline.
4. As a site builder, I want a source-lane map, so that future pages cite source
   anchors rather than copying stale generated summaries.
5. As an AI researcher, I want to see how roles, skills, scripts, registries,
   and control records connect, so that I can evaluate the agent-system
   architecture.
6. As a reviewer, I want generated and local layers clearly marked, so that I
   can detect authority drift before public copy ships.

## 15. Acceptance Criteria

- The repository topology map distinguishes source, control, generated, local,
  tooling, archival, and reserved lanes.
- The folder explorer includes purpose, authority class, edit policy, website
  use, source/derivative/cache class, source anchors, and refresh or validation
  notes for every required folder.
- Contributors can identify where canonical edits belong.
- The website does not encourage hand-editing generated derivative outputs as
  authority.
- `.local/` is labeled ignored, local, non-authoritative retrieval or QA state.
- `FOLDER_MAP.md` is labeled generated and noncanonical.
- `github-facing/`, `html/`, `wiki/`, `ontology/pdfs/`, and generated local
  layers are labeled derivatives or retrieval support as applicable.
- `ontology/tex/` and relevant source materials are separated from generated
  PDFs.
- `legacy_ontology/` is clearly archival and not the active authority lane.
- Topology pages link to PRD-05, PRD-06, PRD-07, and PRD-11 where memory,
  publication, tooling, and site-builder source mapping are involved.

## 16. Dependencies

- PRD-00 defines the master source-authority model and website information
  architecture.
- PRD-05 defines memory, registry, generated derivative, retrieval, and
  provenance boundaries.
- PRD-06 defines publication workflow, source specs, library surfaces, and
  generated reader surfaces.
- PRD-07 defines tooling, skills, scripts, validators, runtime, and cache
  boundaries.
- PRD-09 supplies freshness-sensitive examples for current-state topology
  references.
- PRD-10 defines safe public language and forbidden claims.
- PRD-11 will define a concise source map for future site builders.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Generated folders are mistaken for source authority. | Put generated-versus-canonical labels on every folder card and diagram. |
| `.local/` retrieval state is treated as evidence. | Require local-cache warnings and forbid citation as authority. |
| `FOLDER_MAP.md` is treated as canonical. | State that it is generated orientation and require source/registry cross-checking. |
| Folder topology drifts after page implementation. | Require an inspection date and re-check against live upstream folders before launch. |
| Contributors edit reader derivatives instead of source specs. | Provide "Where should I edit?" routing and source-to-derivative flows. |
| Site builders overuse GitHub-facing derivatives as source. | Require source anchors and PRD-11 quick-source-map linkage. |
| Archival ontology material is mistaken for active ontology. | Label `legacy_ontology/` as archival and compare-only unless promoted by tracked authority. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Re-check the current upstream tree and `FOLDER_MAP.md`.
2. Confirm folder classifications against source registries where available.
3. Confirm generated derivative labels against PRD-05 and PRD-06.
4. Confirm tooling/runtime labels against PRD-07.
5. Confirm site-builder source-map language against PRD-11 after it exists.
6. Search rendered copy for generated-as-authority, cache-as-authority,
   registry-as-proof, validator-as-proof, and archival-as-active-authority
   language.
7. Confirm all diagrams communicate category and edit policy without relying
   on color alone.
8. Run applicable route, content, provenance, build, browser, and
   implementation-control validators for implementation packets.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: implementation support foundation.

This PRD should follow PRD-05, PRD-06, and PRD-07 because topology pages depend
on source/provenance, publication, generated-derivative, tooling, and cache
boundaries. It should precede PRD-11 because the quick source map for site
builders needs a stable folder-classification model.

## 20. Open Questions

1. Should the public folder explorer be manually curated from a small dataset,
   or generated from a reviewed topology manifest that is refreshed from
   upstream evidence?
2. Should folder cards show registry row counts, or would that create
   unnecessary drift and maintenance burden?
3. Should local retrieval lanes be visible to general readers, or should they
   appear only on contributor/operator pages?
4. Should the source-lane diagram include reserved lanes such as `assets/`,
   `manuscripts/`, `reviews/`, and `output/`, or keep the first public version
   limited to required PRD-08 folders?

These questions do not block this PRD. They should be resolved during PRD-11
or future route implementation planning.

## 21. Definition of Done

This PRD is complete when:

- it defines repository topology map, folder explorer, source-lane diagram,
  edit guide, read guide, and generated-versus-canonical legend requirements;
- it covers all required topology components from the PRD-system plan;
- it requires every folder entry to include purpose, authority class, edit
  policy, website use, source/derivative/cache class, source anchors, and
  refresh or validation notes;
- it labels generated derivative and local retrieval folders as
  non-authoritative;
- it keeps canonical source edits routed to source material, registries,
  control records, or governed workflows;
- it gives future site-builder pages a testable folder-classification model
  without creating new source authority.

## References

The AEther Flow Project. (2026). *Folder map* [Generated repository topology
map].

The AEther Flow Project. (2026). *Project README* [Repository overview and
project map].

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].
