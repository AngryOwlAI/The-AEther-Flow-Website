# The Æther-Flow Website PRD System

**Document status:** Implementation handoff for local AI agent  
**Target project:** `AngryOwlAI/The-AEther-Flow`  
**Target output:** One master PRD plus eleven sub-PRDs for the public informative website  
**Prepared date:** 2026-06-29  
**Recommended repository location:** `PRDs/website-information-space/`  
**Primary source catalogue:** `aether_flow_project_components.md`  

---

## 0. Purpose of This Handoff

This document is a structured plan for creating a complete PRD system for the Æther-Flow public website. The website is intended to describe, explain, and promote the project while preserving the project’s scientific and workflow claim boundaries.

The local AI agent should use this document to create a set of PRDs that define the website information architecture, content system, source-authority rules, public-facing messaging, and implementation requirements.

The deliverable is not one monolithic PRD. The deliverable is a coordinated PRD family:

1. One master PRD that governs the whole website information space.
2. Eleven sub-PRDs, one for each major category in the project catalogue.
3. A PRD index or README that explains how the PRDs relate.
4. Clear dependency order, acceptance criteria, claim boundaries, and implementation phases.

---

## 1. Local AI Agent Operating Instructions

### 1.1 Recommended agent role

Use a documentation-oriented role for this task.

Preferred role:

- `Documentation Curator`

Acceptable supporting roles, only if the repository workflow requires them:

- `Project-System Director`, for routing documentation-system changes.
- `Project-Control Maintainer`, only if adding or modifying schemas, validators, or workflow rules.
- `Validator Engineer`, only if adding PRD validation scripts or documentation quality checks.

Do not use physics continuation roles for this PRD creation task unless explicitly directed by a human. This task creates product requirements for a website. It must not update scientific claims, ontology sources, exact-GR benchmark status, derivation milestones, or promotion gates.

### 1.2 Work boundaries

The local AI agent may create or edit:

- `PRDs/website-information-space/**/*.md`
- `PRDs/website-information-space/README.md`
- Optional index files or source maps inside the same PRD directory

The local AI agent must not edit, unless separately authorized:

- `ontology/`
- `ontology/tex/`
- `research_control/current_frontier.md`
- `research_control/program_state.yaml`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `.agents/roles/`
- `.agents/schemas/`
- `.codex/skills/`
- tracked publication outputs under `html/` or `github-facing/`

### 1.3 Scientific claim boundary

The PRD system may describe:

- the project as a dual physics and AI research program;
- the exact-GR benchmark as the current observable-scale effective benchmark;
- the GR derivation from Æther / Æther-flow ontology as open work;
- the AI agent system as governed, bounded, source-first, and human-scaffolded;
- current frontier state only as a dated snapshot from tracked sources.

The PRD system must not claim:

- GR has been derived from Æther / Æther-flow;
- the exact-GR benchmark has been promoted from first principles;
- matter coupling has been solved;
- Einstein equations have been derived from substrate structure;
- validators, generated docs, handoffs, registries, or local memory are scientific proof;
- a local negative result is global theory rejection unless tracked authority explicitly says so.

### 1.4 Current-frontier freshness rule

Do not hard-code active task IDs, latest handoff IDs, or current milestone details as permanent website content.

For `PRD-09`, require the website to treat current state as a dated snapshot. The website must refresh or verify frontier data from:

- `research_control/program_state.yaml`
- `research_control/current_frontier.md`
- latest relevant handoff under `research_control/handoffs/`
- `registries/DISTANCE_TO_GR_LEDGER.csv`

If these sources disagree, the PRD must instruct the implementation to display the more authoritative tracked source and label generated summaries as non-authoritative reader surfaces.

---

## 2. Required PRD File Tree

Create the following files:

```text
PRDs/
└── website-information-space/
    ├── README.md
    ├── PRD-00-master-website-information-space.md
    ├── PRD-01-high-level-components.md
    ├── PRD-02-physics-and-mathematical-components.md
    ├── PRD-03-research-control-and-agent-workflow.md
    ├── PRD-04-role-and-schema-components.md
    ├── PRD-05-memory-registry-and-retrieval-components.md
    ├── PRD-06-documentation-publication-and-website-components.md
    ├── PRD-07-tooling-skills-scripts-and-runtime-components.md
    ├── PRD-08-folder-and-repository-topology-components.md
    ├── PRD-09-current-research-frontier-for-website-use.md
    ├── PRD-10-website-positioning-guidance.md
    └── PRD-11-quick-source-map-for-site-builders.md
```

Optional supporting files:

```text
PRDs/website-information-space/
├── templates/
│   ├── sub-prd-template.md
│   ├── page-brief-template.md
│   └── claim-boundary-block.md
└── source-maps/
    ├── website-page-to-source-map.md
    └── prd-dependency-map.md
```

---

## 3. Recommended Creation Order

Do not create the PRDs in numerical category order. Create them in dependency order.

1. `README.md`
2. `PRD-00-master-website-information-space.md`
3. `PRD-10-website-positioning-guidance.md`
4. `PRD-05-memory-registry-and-retrieval-components.md`
5. `PRD-06-documentation-publication-and-website-components.md`
6. `PRD-01-high-level-components.md`
7. `PRD-02-physics-and-mathematical-components.md`
8. `PRD-09-current-research-frontier-for-website-use.md`
9. `PRD-03-research-control-and-agent-workflow.md`
10. `PRD-04-role-and-schema-components.md`
11. `PRD-07-tooling-skills-scripts-and-runtime-components.md`
12. `PRD-08-folder-and-repository-topology-components.md`
13. `PRD-11-quick-source-map-for-site-builders.md`

Reason: messaging, source authority, publication process, and claim boundaries must be established before technical website pages are specified. Otherwise the website may become visually polished but scientifically unsafe.

---

## 4. Shared Frontmatter for Every PRD

Every PRD file must begin with YAML frontmatter.

```yaml
---
prd_id: "PRD-XX"
title: "Replace with PRD title"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Replace with website area"
source_catalogue: "aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-29"
last_reviewed: "2026-06-29"
depends_on: []
blocks_claim_promotion: true
requires_human_gate: false
---
```

For `PRD-09`, set:

```yaml
freshness_sensitive: true
requires_current_frontier_refresh: true
```

For any PRD that defines public claim language, set:

```yaml
claim_boundary_required: true
```

---

## 5. Shared PRD Template

Every sub-PRD must use this structure.

```markdown
# PRD-XX: Title

## 1. Summary
## 2. Product Purpose
## 3. Source Authority
## 4. Audience and Reader Jobs
## 5. Scope
## 6. Non-Goals
## 7. Website Surfaces
## 8. Functional Requirements
## 9. Non-Functional Requirements
## 10. Claim Boundary
## 11. Content Requirements
## 12. UX and Navigation Requirements
## 13. Data, Source, and Provenance Requirements
## 14. User Stories
## 15. Acceptance Criteria
## 16. Dependencies
## 17. Risks and Mitigations
## 18. Validation Plan
## 19. Launch Priority
## 20. Open Questions
## 21. Definition of Done
```

The master PRD may use a broader structure, defined below.

---

## 6. Universal Claim-Boundary Block

Include this block, or a locally specialized form of it, in every PRD.

```markdown
## Claim Boundary

This PRD may specify website content that explains:

- the Æther / Æther-flow ontology as a research ontology;
- the exact-GR benchmark as the current observable-scale benchmark;
- the GR derivation burden as open;
- the AI research-agent workflow as governed, source-first, bounded, and human-scaffolded;
- current status only as a dated snapshot from tracked project sources.

This PRD must not authorize website content claiming:

- GR has been derived from Æther / Æther-flow;
- matter coupling has been solved;
- Einstein equations have been derived from source-side substrate structure;
- the benchmark has been promoted from first principles;
- validators, generated docs, registries, or handoffs are physics proof;
- local negative results are global theory rejection without tracked authority.
```

---

## 7. Master PRD Specification

### File

`PRD-00-master-website-information-space.md`

### Purpose

Define the complete product vision, structure, requirements, and governing rules for the Æther-Flow public website information space.

The master PRD must reference all eleven sub-PRDs and explain how they interlock.

### Required sections

```markdown
# PRD-00: Æther-Flow Website Information Space

## 1. Product Summary
## 2. Project Context
## 3. Website Mission
## 4. Source Authority Model
## 5. Product Goals
## 6. Non-Goals
## 7. Audiences and Reader Jobs
## 8. Website Information Architecture
## 9. Required Page Families
## 10. Cross-PRD Map
## 11. Claim Boundary Policy
## 12. Current-State Freshness Policy
## 13. Content Production Workflow
## 14. Design and UX Principles
## 15. Functional Requirements
## 16. Non-Functional Requirements
## 17. Accessibility Requirements
## 18. SEO and Discoverability Requirements
## 19. Metrics and Success Criteria
## 20. Launch Phases
## 21. Risks
## 22. Open Questions
## 23. Definition of Done
## 24. Sub-PRD Index
```

### Master product thesis

Use this as the baseline thesis:

> The Æther-Flow website is a source-backed public information space for a dual physics-and-AI research project. It explains an exact-GR-compatible interpretation of relativity, the open first-principles derivation burden from Æther / Æther-flow ontology, and the governed AI research-agent system that makes theoretical exploration auditable through roles, registries, validators, claim gates, memory, and handoffs.

### Required website top-level navigation

The master PRD must specify at least these top-level website sections:

1. Home
2. Physics Research
3. AI Research System
4. Research Operations
5. Source Authority
6. Library
7. Current Frontier
8. Contributor / Site Builder Guide

### Master acceptance criteria

The master PRD is complete when:

- it names all eleven sub-PRDs;
- it defines the site mission and non-goals;
- it defines the source-authority model;
- it defines the claim-boundary policy;
- it defines a current-frontier freshness policy;
- it defines reader audiences and page families;
- it defines launch phases and MVP scope;
- it prevents completed-GR-derivation claims;
- it gives the local implementation team a concrete website information architecture.

---

## 8. Sub-PRD Specifications

## PRD-01: High-Level Components

### File

`PRD-01-high-level-components.md`

### Purpose

Turn the project’s top-level identity into a clear first-read experience for general readers, physicists, AI researchers, reviewers, and contributors.

### Source basis

Use the catalogue category:

- `1. High-Level Components`

Use source anchors from the catalogue, especially:

- `README.md`
- `AGENTS.md`
- `research_control/README.md`
- `ontology/aether-and-aether-flow.md`
- `ontology/tex/`
- `registries/DISTANCE_TO_GR_LEDGER.csv`

### Required website surfaces

- Homepage hero
- Project overview page
- Dual-track project map
- Exact-GR benchmark summary card
- Open derivation burden summary card
- AI research-agent system summary card
- Trust and claim-boundary panel

### Functional requirements

The PRD must require the website to:

1. Explain the project in one precise sentence.
2. Present physics and AI research tracks as co-equal parts of the project.
3. Show that exact-GR benchmark adoption and first-principles derivation are different states.
4. Explain why the AI research-agent system matters even while the physics derivation remains open.
5. Provide reader paths for general readers, physicists, AI researchers, contributors, and site builders.

### Acceptance criteria

- A new reader can answer “what is this project?” within one minute.
- The homepage does not imply that GR has been derived.
- The page links to source authority before deep technical claims appear.
- The page includes a visible “what this project does not claim” element.

---

## PRD-02: Low-Level Physics and Mathematical Components

### File

`PRD-02-physics-and-mathematical-components.md`

### Purpose

Define the physics explainer system for ontology, exact-GR benchmark, derivation burdens, mathematical components, and proof boundaries.

### Source basis

Use the catalogue category:

- `2. Low-Level Physics and Mathematical Components`

Use source anchors from the catalogue, especially:

- `ontology/aether-and-aether-flow.md`
- `ontology/tex/aether_flow_foundations.tex`
- `ontology/tex/aether_flow_exact_closure_note.tex`
- `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`
- `ontology/tex/aether_flow_dynamics.tex`
- `ontology/tex/aether_flow_relativistic_recovery.tex`
- `ontology/tex/aether_flow_geometry.tex`
- `ontology/tex/aether_flow_consistency.tex`
- `research_control/design/gr_derivation_burden_map.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`

### Required website surfaces

- Ontology explainer
- Exact-GR benchmark boundary explainer
- GR derivation roadmap
- Physics glossary
- Flow-geometry visual dictionary
- Adoption versus derivation comparison table
- Current physics claim-status table
- “What remains open?” section

### Functional requirements

The PRD must require the website to explain:

1. Æther, Æther-flow, observed space, S-time, expansion, and gravity-language as ontology-level concepts.
2. Exact-GR benchmark package, including one operative metric and universal matter coupling at the benchmark level.
3. Einstein-Hilbert effective action as adopted effective benchmark structure, not substrate derivation.
4. Congruence geometry as a disciplined interpretive dictionary.
5. Source-side derivation milestones including source ontology, EqSrc, localization, response, `M_src`, `g_eff`, matter coupling, Einstein equations, and benchmark promotion.
6. Negative-result preservation and local freeze logic.

### Mandatory claim boundaries

This PRD must require physics pages to avoid claiming:

- independent low-energy non-GR signatures;
- completed matter coupling;
- completed Einstein-equation derivation;
- completed source-to-metric derivation;
- completed benchmark promotion.

### Acceptance criteria

- Every physics page has a claim-status panel.
- The exact-GR page clearly distinguishes benchmark adoption from derivation.
- The ontology page avoids naive ether-wind or three-dimensional medium framing.
- The mathematical roadmap identifies which burdens are upstream and downstream.
- Current status pages are dated snapshots, not permanent scientific claims.

---

## PRD-03: Low-Level Research-Control and Agent Workflow Components

### File

`PRD-03-research-control-and-agent-workflow.md`

### Purpose

Define how the website explains the governed AI research workflow: Director decisions, AgentJobs, execution-role records, completions, handoffs, validators, and Distance-to-GR updates.

### Source basis

Use the catalogue category:

- `3. Low-Level Research-Control and Agent Workflow Components`

Use source anchors from the catalogue, especially:

- `research_control/README.md`
- `research_control/program_state.yaml`
- `research_control/current_frontier.md`
- `research_control/tasks/`
- `research_control/templates/COMPLETION_TEMPLATE.yaml`
- `research_control/design/mathematical_decisiveness_completion_contract.md`
- `.codex/skills/continue-research/SKILL.md`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`
- `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`

### Required website surfaces

- Research-agent workflow page
- AgentJob lifecycle diagram
- Director decision explainer
- Completion and handoff explainer
- Distance-to-GR workflow panel
- Validator PASS limit explainer
- Parent-child synthesis explainer

### Functional requirements

The PRD must require the website to explain:

1. The one-job rule.
2. Director Decision Records.
3. AgentJob contracts.
4. Execution-role records.
5. Memory preflight.
6. Parent-child parallel synthesis for physics jobs.
7. Completion records.
8. Handoffs.
9. Distance-to-GR status matrix and delta.
10. The difference between operational validation and scientific proof.

### Acceptance criteria

- The workflow page includes a lifecycle diagram from current state to handoff.
- The page states that validator PASS does not equal scientific proof.
- The page explains why local failures are preserved without becoming global no-go claims.
- The page explains how bounded theoretical continuation prevents generic pause.

---

## PRD-04: Role and Schema Components

### File

`PRD-04-role-and-schema-components.md`

### Purpose

Define public-facing explanations for the project’s agent roles, schemas, authority limits, and human-gated promotion structures.

### Source basis

Use the catalogue category:

- `4. Role and Schema Components`

Use source anchors from the catalogue, especially:

- `.agents/roles/`
- `.agents/schemas/ROLE_SCHEMA.md`
- `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- `.agents/schemas/DOCUMENTATION_IMPACT_SCHEMA.md`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`

### Required website surfaces

- Role catalogue
- Role authority inspector
- Schema reference map
- “Who can make which claim?” matrix
- Human-gated role explainer

### Functional requirements

The PRD must require the website to document, at minimum:

- Director of Research
- Candidate Constructor
- Ontology Formalizer
- Refuter
- Smuggling Auditor
- Gate Chair
- Theoretical Continuation Selector
- Documentation Curator
- Memory-System Maintainer
- Process Integrity Auditor
- Project-Control Maintainer
- Project-System Director
- Validator Engineer
- Role Schema
- Director Decision Schema
- AgentJob Schema
- Execution Role Schema
- Documentation Impact Schema

### Acceptance criteria

- Every role page includes “can do,” “cannot do,” “outputs,” and “claim boundary.”
- The Gate Chair page states that protected scientific promotion requires explicit tracked human authority.
- The schema pages explain schemas as control contracts, not decorative documentation.
- No role is presented as having authority beyond its registered contract and task-local execution record.

---

## PRD-05: Memory, Registry, and Retrieval Components

### File

`PRD-05-memory-registry-and-retrieval-components.md`

### Purpose

Define website requirements for explaining the project’s source-first memory, registries, retrieval layers, generated derivatives, and provenance graph.

### Source basis

Use the catalogue category:

- `5. Memory, Registry, and Retrieval Components`

Use source anchors from the catalogue, especially:

- `registries/`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/PDF_DERIVATIVE_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `wiki/`
- `.local/content_semantics/`
- `.local/obsidian/`
- `.codex/skills/project-memory-system/SKILL.md`

### Required website surfaces

- Source authority explainer
- Registry explorer
- Memory-system explainer
- Provenance graph
- Generated derivative warning component
- Source versus derivative versus retrieval matrix

### Functional requirements

The PRD must require the website to explain:

1. TeX source authority for physics claims.
2. Markdown source authority for authored documentation and contracts.
3. PDF, HTML, GitHub-facing Markdown, and wiki pages as generated or reader-facing derivatives.
4. `.local/` as local retrieval/cache state.
5. CSV registries as provenance and workflow state.
6. Memory lookup as navigation, not authority.
7. Need to inspect canonical sources before using retrieved hits in claim text.

### Acceptance criteria

- Every website page has a source/provenance footer.
- Registry-driven dashboards include “not scientific proof” language.
- Generated surfaces are visibly labeled as noncanonical where appropriate.
- The source-authority page is linked from the homepage and technical sections.

---

## PRD-06: Documentation, Publication, and Website Components

### File

`PRD-06-documentation-publication-and-website-components.md`

### Purpose

Define the website content-production system, page templates, publication workflow, source specs, public explainers, and generated HTML/Markdown parity requirements.

### Source basis

Use the catalogue category:

- `6. Documentation, Publication, and Website Components`

Use source anchors from the catalogue, especially:

- `README.md`
- `CONTEXT.md`
- `markdown/publication-briefs/`
- `markdown/html-explainer-specs/`
- `github-facing/`
- `html/`
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `.agents/roles/research_ops/documentation-curator.v0.7.0.md`

### Required website surfaces

- Publication process explainer
- Page-type template library
- Source-spec template
- Publication-brief template
- GitHub Markdown and website parity guide
- Visual strategy catalogue
- Source-backed page footer design

### Functional requirements

The PRD must require the website content system to support:

1. Project overview pages.
2. Concept explainers.
3. Boundary explainers.
4. Status dashboards.
5. Role catalogues.
6. Registry/source maps.
7. Operator guides.
8. Site-builder guides.
9. Library and reading-path pages.

The PRD must also require every major page to declare:

- audience;
- reader job;
- source basis;
- claim boundary;
- visual strategy;
- acceptance criteria;
- freshness rule if applicable.

### Acceptance criteria

- Every planned page has a source basis and claim boundary.
- The publication process distinguishes reader surfaces from canonical authority.
- No tracked HTML or generated Markdown page is treated as independent scientific authority.
- The website system can reuse existing explainer content while preserving source hierarchy.

---

## PRD-07: Tooling, Skills, Scripts, and Runtime Components

### File

`PRD-07-tooling-skills-scripts-and-runtime-components.md`

### Purpose

Define technical website pages for operators, contributors, validators, skills, scripts, runtime requirements, and reproducibility.

### Source basis

Use the catalogue category:

- `7. Tooling, Skills, Scripts, and Runtime Components`

Use source anchors from the catalogue, especially:

- `.codex/skills/`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `scripts/research_control/`
- `scripts/project_control/`
- `Makefile`
- `requirements.txt`
- `tests/`
- `README.md`

### Required website surfaces

- Technical requirements page
- Skills catalogue
- Script catalogue
- Validator/operator workflow page
- Makefile command reference
- Runtime environment page
- Reproducibility guide

### Functional requirements

The PRD must require the website to explain:

1. Codex app harness role.
2. Continue-research skill.
3. Improve-project-system skill.
4. Project-memory-system skill.
5. HTML visual explainer workflow.
6. Visual explainer workflow.
7. User-modified-project skill.
8. Research-control scripts.
9. Project-control scripts.
10. Memory bootstrap and query tools.
11. Validators and tests.
12. Python runtime and PyMuPDF dependency.
13. Local cache boundary.

### Acceptance criteria

- Every command page says what the command validates and what it does not validate.
- Validator pages never imply proof, derivation, or claim promotion.
- Contributor paths show minimum setup, common validation, and where evidence is recorded.

---

## PRD-08: Folder and Repository Topology Components

### File

`PRD-08-folder-and-repository-topology-components.md`

### Purpose

Define how the website explains the repository’s folder structure, source lanes, derivative lanes, local caches, and authority topology.

### Source basis

Use the catalogue category:

- `8. Folder and Repository Topology Components`

Use source anchors from the catalogue, especially:

- `FOLDER_MAP.md`
- `.agents/`
- `.codex/`
- `ontology/`
- `legacy_ontology/`
- `research_control/`
- `registries/`
- `markdown/`
- `github-facing/`
- `html/`
- `wiki/`
- `scripts/`
- `tests/`
- `tex_shared/`
- `.local/`

### Required website surfaces

- Repository topology map
- Folder explorer
- Source-lane diagram
- “Where should I edit?” guide
- “Where should I read?” guide
- “Generated versus canonical” folder legend

### Functional requirements

The PRD must require the website to classify folders by authority:

- canonical scientific source;
- canonical documentation/control source;
- tracked control authority;
- generated derivative;
- generated local retrieval;
- tooling/runtime;
- archival;
- reserved/future lane.

### Acceptance criteria

- A contributor can identify where canonical edits belong.
- The website does not encourage hand-editing generated derivative outputs as authority.
- `.local/` is clearly labeled as ignored retrieval/cache state.
- The repo topology page links to source-authority and site-builder PRDs.

---

## PRD-09: Current Research Frontier for Website Use

### File

`PRD-09-current-research-frontier-for-website-use.md`

### Purpose

Define the live-status and research-frontier website layer without turning a moving snapshot into a stale permanent claim.

### Source basis

Use the catalogue category:

- `9. Current Research Frontier for Website Use`

Use source anchors from the catalogue, especially:

- `research_control/current_frontier.md`
- `research_control/program_state.yaml`
- latest relevant handoff under `research_control/handoffs/`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`

### Required website surfaces

- Current research frontier dashboard
- Current milestone card
- Active task and latest handoff card
- Distance-to-GR status table
- Blocked claims panel
- Next recommended action card
- Validation-status panel
- Freshness and source authority badge

### Functional requirements

The PRD must require the website to:

1. Treat all current-state data as dated snapshots.
2. Display the source and refresh date for frontier state.
3. Show blocked claims prominently.
4. Explain that validation PASS indicates operational consistency, not scientific proof.
5. Avoid permanent hard-coding of task IDs, handoff IDs, and transient routes.
6. Provide a stale-data warning if the frontier page has not been refreshed.

### Acceptance criteria

- The status page includes `last_source_refresh` or equivalent.
- The status page says it is not independent authority.
- The status system can be updated without rewriting core physics pages.
- Blocked claims are visible whenever progress status is shown.

---

## PRD-10: Website Positioning Guidance

### File

`PRD-10-website-positioning-guidance.md`

### Purpose

Define public messaging, homepage copy rules, approved vocabulary, forbidden claims, trust-building language, and audience-specific positioning.

### Source basis

Use the catalogue category:

- `10. Website Positioning Guidance`

Use source anchors from the catalogue, especially:

- `README.md`
- `AGENTS.md`
- `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`
- `ontology/tex/aether_flow_exact_closure_note.tex`
- `research_control/current_frontier.md`
- `research_control/design/gr_derivation_burden_map.md`
- `github-facing/claim-gates-explainer.md`
- `html/project-overview-explainer.html`

### Required website surfaces

- Messaging guide
- Homepage hero guidance
- Approved claims list
- Forbidden claims list
- Audience-specific pitch cards
- Trust and transparency copy block
- Copy QA checklist

### Required safe pitch

The PRD should include this baseline pitch:

> The Æther-Flow project is a dual physics and AI research program that presents an exact-GR-compatible interpretation of relativity while building a governed AI research-agent system for pursuing the still-open derivation from deeper substrate structure.

### Approved phrases

The PRD should approve phrasing such as:

- exact-GR benchmark
- GR-consistent interpretation
- open first-principles derivation burden
- source-backed research-control system
- human-scaffolded AI research-agent workflow
- governed theoretical research workflow
- claim-gated derivation program

### Forbidden phrases

The PRD must reject phrasing such as:

- GR has been derived
- Einstein equations derived from Æther
- matter coupling solved
- benchmark promoted from first principles
- new tested gravity prediction
- autonomous proof system
- validators prove the theory
- AI has solved relativity

### Acceptance criteria

- Homepage hero copy states dual mission, exact-GR status, and open derivation burden.
- Promotional copy does not overclaim scientific status.
- Every public-facing page has a claims-to-use and claims-to-avoid check.
- The site positions caution as credibility.

---

## PRD-11: Quick Source Map for Site Builders

### File

`PRD-11-quick-source-map-for-site-builders.md`

### Purpose

Give site builders, future agents, and documentation maintainers a clear map from website page types to repository source materials.

### Source basis

Use the catalogue category:

- `11. Quick Source Map for Site Builders`

Use source anchors from the catalogue, especially:

- `README.md`
- `AGENTS.md`
- `ontology/aether-and-aether-flow.md`
- `ontology/tex/*.tex`
- `research_control/README.md`
- `research_control/current_frontier.md`
- `.codex/skills/`
- `.agents/roles/`
- `.agents/schemas/`
- `github-facing/`
- `html/`
- `markdown/publication-briefs/`
- `markdown/html-explainer-specs/`
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`
- `Makefile`
- `requirements.txt`
- `scripts/`
- `tests/`

### Required website surfaces

- Site-builder guide
- Source bundle index
- Page-to-source mapping table
- “Build from these first” checklist
- Contributor handoff guide
- Staleness handling guide

### Functional requirements

The PRD must require source bundles for:

1. Project overview pages.
2. Physics pages.
3. AI research-agent pages.
4. Source-authority pages.
5. Current-frontier pages.
6. Operator/contributor pages.
7. Website publication pages.

### Acceptance criteria

- A site builder can identify the right source for any planned page.
- Every planned page type has a source bundle.
- Current-frontier content has a staleness and refresh policy.
- Site-builder docs preserve authority hierarchy.

---

## 9. Cross-PRD Dependency Map

| PRD | Depends On | Reason |
|---|---|---|
| PRD-00 | All sub-PRDs | Governs total website architecture. |
| PRD-01 | PRD-10, PRD-05 | Needs approved messaging and source authority. |
| PRD-02 | PRD-05, PRD-09, PRD-10 | Physics pages need provenance, live-status discipline, and claim limits. |
| PRD-03 | PRD-04, PRD-05, PRD-07 | Workflow pages need role, authority, registry, and tooling context. |
| PRD-04 | PRD-03, PRD-05 | Role authority depends on workflow and registries. |
| PRD-05 | PRD-08 | Registry and memory explanation benefits from folder topology. |
| PRD-06 | PRD-05, PRD-10 | Publication process needs source authority and messaging rules. |
| PRD-07 | PRD-03, PRD-05 | Tooling pages need workflow and validation boundaries. |
| PRD-08 | PRD-05, PRD-11 | Folder topology supports source mapping. |
| PRD-09 | PRD-05, PRD-10 | Current frontier needs source and claim-boundary discipline. |
| PRD-10 | PRD-00 | Messaging must align with master website mission. |
| PRD-11 | PRD-05, PRD-06, PRD-08 | Site-builder map depends on sources, publication process, and topology. |

---

## 10. MVP PRD Package

If the local AI agent is constrained to an MVP, create these first:

1. `README.md`
2. `PRD-00-master-website-information-space.md`
3. `PRD-10-website-positioning-guidance.md`
4. `PRD-05-memory-registry-and-retrieval-components.md`
5. `PRD-06-documentation-publication-and-website-components.md`
6. `PRD-01-high-level-components.md`
7. `PRD-02-physics-and-mathematical-components.md`
8. `PRD-09-current-research-frontier-for-website-use.md`

This MVP gives the website its public story, source-authority discipline, publication process, homepage requirements, physics explanation rules, and current-status safety rails.

Phase 2 can add:

- `PRD-03-research-control-and-agent-workflow.md`
- `PRD-04-role-and-schema-components.md`

Phase 3 can add:

- `PRD-07-tooling-skills-scripts-and-runtime-components.md`
- `PRD-08-folder-and-repository-topology-components.md`
- `PRD-11-quick-source-map-for-site-builders.md`

---

## 11. Website Page Families to Be Covered by PRDs

The PRD system must eventually support these page families.

| Page Family | Primary PRD | Secondary PRDs |
|---|---|---|
| Homepage | PRD-01 | PRD-00, PRD-10, PRD-05 |
| Project Overview | PRD-01 | PRD-10, PRD-05 |
| Ontology | PRD-02 | PRD-10, PRD-05 |
| Exact-GR Benchmark | PRD-02 | PRD-10, PRD-05 |
| Derivation Roadmap | PRD-02 | PRD-09, PRD-10 |
| Current Frontier | PRD-09 | PRD-02, PRD-05 |
| AI Research-Agent System | PRD-03 | PRD-04, PRD-07 |
| Roles and Schemas | PRD-04 | PRD-03, PRD-05 |
| Memory and Registries | PRD-05 | PRD-08 |
| Source Authority | PRD-05 | PRD-10 |
| Publications and Library | PRD-06 | PRD-05, PRD-11 |
| Tooling and Runtime | PRD-07 | PRD-03, PRD-05 |
| Repository Map | PRD-08 | PRD-05, PRD-11 |
| Site Builder Guide | PRD-11 | PRD-06, PRD-08 |

---

## 12. Page-Level Requirements for All Website Pages

Every website page specified by any PRD must include:

1. **Page purpose**  
   What job the page does for the reader.

2. **Audience**  
   General reader, physicist, AI researcher, reviewer, contributor, operator, or site builder.

3. **Source basis**  
   Specific repository files, registries, or catalogue sections.

4. **Claim status**  
   Adopted, benchmark, open, candidate, blocked, generated, derivative, or snapshot.

5. **Claim boundary**  
   What the page does not authorize the reader to infer.

6. **Navigation role**  
   Where the page sits in the website journey.

7. **Visual requirements**  
   Diagrams, cards, tables, timelines, matrices, source maps, or dashboards.

8. **Freshness rule**  
   Required for any page using active task, handoff, milestone, ledger, or current-frontier data.

9. **Acceptance criteria**  
   Concrete tests for completeness and accuracy.

10. **Source/provenance footer**  
   A visible footer stating whether the page is source-backed, generated, derivative, current snapshot, or non-authoritative.

---

## 13. Suggested Website Information Architecture

The PRD system should converge on this website structure.

```text
/
├── Home
├── Physics Research
│   ├── Ontology
│   ├── Exact-GR Benchmark
│   ├── Derivation Roadmap
│   ├── Flow Geometry
│   ├── Current Physics Claim Status
│   └── Open Burdens
├── AI Research System
│   ├── Research-Agent Workflow
│   ├── AgentJob Lifecycle
│   ├── Roles and Schemas
│   ├── Parent-Child Synthesis
│   └── Human-Gated Promotion
├── Research Operations
│   ├── Validators
│   ├── Handoffs
│   ├── Memory Preflight
│   ├── Project-System Improvement
│   └── Runtime Requirements
├── Source Authority
│   ├── Canonical Sources
│   ├── Registries
│   ├── Generated Derivatives
│   ├── Local Retrieval Layers
│   └── Claim Boundary Registry
├── Current Frontier
│   ├── Status Dashboard
│   ├── Distance-to-GR Ledger View
│   ├── Blocked Claims
│   └── Next Recommended Action
├── Library
│   ├── Explainers
│   ├── GitHub-Facing Docs
│   ├── HTML Explainables
│   ├── PDFs
│   └── Reading Paths
└── Site Builder Guide
    ├── Source Bundles
    ├── Page-to-Source Map
    ├── Publication Workflow
    └── Contributor Handoff
```

---

## 14. PRD Validation Checklist

Before marking the PRD system complete, the local AI agent must verify:

- [ ] `README.md` exists and indexes every PRD.
- [ ] `PRD-00` exists and references all eleven sub-PRDs.
- [ ] Every sub-PRD has the shared frontmatter.
- [ ] Every sub-PRD includes a source-authority section.
- [ ] Every sub-PRD includes a claim-boundary section.
- [ ] Every sub-PRD includes functional requirements.
- [ ] Every sub-PRD includes acceptance criteria.
- [ ] Every sub-PRD includes dependencies.
- [ ] `PRD-09` includes freshness rules.
- [ ] `PRD-10` includes approved and forbidden public claims.
- [ ] No PRD claims GR has been derived.
- [ ] No PRD claims benchmark promotion from first principles.
- [ ] No PRD treats generated docs as canonical authority.
- [ ] No PRD treats validators as scientific proof.
- [ ] The PRD set supports MVP and later phases.
- [ ] The PRD set is suitable as an implementation plan for website builders.

---

## 15. Agent Execution Phases

If the repository governance workflow requires one bounded job at a time, use these phases as separate packets.

### Phase 0: Source inspection and directory setup

Tasks:

1. Inspect the uploaded catalogue and source anchors.
2. Inspect existing `PRDs/` lane if present.
3. Create `PRDs/website-information-space/` if absent.
4. Create `README.md` skeleton and PRD file skeletons.
5. Do not write detailed PRD content yet if the local workflow restricts scope.

Expected output:

- PRD directory tree.
- PRD index skeleton.
- Handoff listing next phase.

### Phase 1: Master PRD and positioning rules

Tasks:

1. Write `PRD-00-master-website-information-space.md`.
2. Write `PRD-10-website-positioning-guidance.md`.
3. Add approved and forbidden claim language.
4. Add master IA and launch phases.

Expected output:

- Master website PRD.
- Positioning PRD.
- Updated PRD README.

### Phase 2: Source authority and publication process

Tasks:

1. Write `PRD-05-memory-registry-and-retrieval-components.md`.
2. Write `PRD-06-documentation-publication-and-website-components.md`.
3. Define source/provenance footer requirements.
4. Define generated-derivative warning requirements.

Expected output:

- Source authority PRD.
- Publication and website-components PRD.
- Updated cross-PRD dependency map.

### Phase 3: High-level website and physics pages

Tasks:

1. Write `PRD-01-high-level-components.md`.
2. Write `PRD-02-physics-and-mathematical-components.md`.
3. Define homepage and physics page requirements.
4. Add adoption-versus-derivation requirements.

Expected output:

- High-level components PRD.
- Physics and math PRD.
- Updated website page-family map.

### Phase 4: Current frontier and AI workflow pages

Tasks:

1. Write `PRD-09-current-research-frontier-for-website-use.md`.
2. Write `PRD-03-research-control-and-agent-workflow.md`.
3. Define freshness and stale-data behavior.
4. Define AgentJob and handoff lifecycle pages.

Expected output:

- Current frontier PRD.
- Research-control workflow PRD.
- Updated snapshot authority rules.

### Phase 5: Roles, tooling, topology, and site-builder guide

Tasks:

1. Write `PRD-04-role-and-schema-components.md`.
2. Write `PRD-07-tooling-skills-scripts-and-runtime-components.md`.
3. Write `PRD-08-folder-and-repository-topology-components.md`.
4. Write `PRD-11-quick-source-map-for-site-builders.md`.
5. Update `README.md` with final index and implementation sequencing.

Expected output:

- Remaining four PRDs.
- Completed PRD index.
- Cross-linked PRD system.

### Phase 6: Review and validation

Tasks:

1. Check all PRDs against the validation checklist.
2. Search for forbidden claims.
3. Verify every PRD has source basis and claim boundary.
4. Verify current-frontier status is freshness-sensitive.
5. Run available documentation validators if they exist and are applicable.
6. Produce final handoff summary.

Expected output:

- Completed PRD system.
- Validation checklist result.
- Handoff for website implementation.

---

## 16. Definition of Done for the PRD System

The PRD system is complete when:

1. The master PRD exists and defines the full website mission, IA, claim-boundary policy, and PRD map.
2. All eleven sub-PRDs exist and follow the shared template.
3. Every sub-PRD has specific source anchors from the catalogue.
4. Every sub-PRD has acceptance criteria.
5. Every sub-PRD has a claim-boundary section.
6. The website’s public story is ambitious but does not overclaim.
7. The exact-GR benchmark is distinguished from first-principles derivation.
8. The current-frontier page is specified as a dated snapshot.
9. Registry, memory, wiki, PDF, HTML, and `.local` layers are correctly classified.
10. Validators are described as operational checks, not scientific proof.
11. The PRD set gives future site builders a concrete source map.
12. The PRD README explains how to implement the site in phases.

---

## 17. Final Local AI Agent Prompt

Use this prompt when assigning the work to the local AI agent:

```text
You are working in the The-AEther-Flow repository as a Documentation Curator or equivalent documentation-focused local AI agent.

Create a complete PRD system for the public Æther-Flow website information space using the handoff file `aether_flow_website_prd_system.md` and the source catalogue `aether_flow_project_components.md`.

Create the PRD directory:

PRDs/website-information-space/

Create the following files:

- README.md
- PRD-00-master-website-information-space.md
- PRD-01-high-level-components.md
- PRD-02-physics-and-mathematical-components.md
- PRD-03-research-control-and-agent-workflow.md
- PRD-04-role-and-schema-components.md
- PRD-05-memory-registry-and-retrieval-components.md
- PRD-06-documentation-publication-and-website-components.md
- PRD-07-tooling-skills-scripts-and-runtime-components.md
- PRD-08-folder-and-repository-topology-components.md
- PRD-09-current-research-frontier-for-website-use.md
- PRD-10-website-positioning-guidance.md
- PRD-11-quick-source-map-for-site-builders.md

Follow the dependency order in the handoff file. Use the shared PRD template and frontmatter. Include source authority, claim boundaries, functional requirements, acceptance criteria, dependencies, validation plan, and definition of done in every PRD.

Do not edit ontology sources, research-control current state, role contracts, schemas, skills, registries, or generated website outputs unless separately authorized. Do not claim that GR has been derived, that matter coupling has been solved, that Einstein equations have been derived from substrate structure, or that the exact-GR benchmark has been promoted from first principles.

Treat current research frontier data as freshness-sensitive and source-backed snapshot material only.

When complete, provide a concise handoff summary listing created files, unresolved questions, validation performed, and recommended next website implementation phase.
```

---

## 18. Closing Note

This PRD system should make the website legible without making the science look more complete than it is. The correct public posture is disciplined ambition: exact-GR compatibility is real within the active benchmark, first-principles derivation remains open, and the AI research-agent system is valuable because it makes that open work auditable, bounded, and source-grounded.
