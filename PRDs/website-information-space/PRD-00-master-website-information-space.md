---
prd_id: "PRD-00"
title: "AEther-Flow Website Information Space"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Master information architecture and requirements"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "README.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-00: AEther-Flow Website Information Space

## 1. Product Summary

The AEther-Flow Website is a source-backed public information space for a dual
physics and AI research project. It must explain an exact-GR-compatible
interpretation of relativity, the open first-principles derivation burden from
AEther / AEther-flow ontology, and the governed AI research-agent system that
makes theoretical exploration auditable through roles, registries, validators,
claim gates, memory, and handoffs.

The product is not a proof surface. It is a reader-facing explanation and
orientation layer that helps general readers, physicists, AI researchers,
reviewers, contributors, operators, and site builders understand what the
project claims, what remains open, and which repository sources support each
page.

## 2. Project Context

The upstream AEther Flow Project has two coupled tracks:

- A physics track that currently keeps observable-scale gravitational physics
  exactly aligned with ordinary general relativity while investigating whether
  the benchmark can be derived from deeper substrate structure.
- An AI research-agent track that uses bounded AgentJobs, role contracts,
  registries, validation, handoffs, memory, and human-gated promotion to make
  theoretical work auditable.

The website repository is the presentation layer. It may explain, organize, and
promote reviewed material, but canonical scientific, mathematical, governance,
and research-workflow authority remains in the upstream source project.

## 3. Website Mission

The website mission is to make the project legible without weakening its
discipline.

The site should:

- present the dual physics-and-AI program in a concise public narrative;
- explain the exact-GR benchmark and the adoption-versus-derivation boundary;
- make the open GR derivation burden visible rather than hidden;
- explain the research-control system as a practical governance system for
  speculative theoretical work;
- turn source authority, claim gates, validators, and handoffs into reader
  trust signals;
- provide internal-first reading paths, with source links available as
  provenance rather than the primary reader journey.

## 4. Source Authority Model

The master source-authority rule is:

Website pages are explanatory derivatives. The upstream project remains
authoritative for scientific, mathematical, governance, and research-workflow
claims.

The website information space should classify evidence this way:

| Layer | Website treatment |
| --- | --- |
| Registered TeX sources | Canonical physics authority for technical physics claims. |
| Research-control records | Canonical workflow and current-state authority when current. |
| Registries | Provenance, status, relationship, and validation-facing metadata. |
| PDFs and HTML explainers | Human-readable derivatives, not independent source authority. |
| GitHub-facing Markdown and wiki notes | Useful reader or retrieval surfaces, not claim promotion authority. |
| Local memory, semantic extracts, and caches | Navigation aids only. |
| Website PRDs | Requirements-planning artifacts, not claim authority. |

Every page family must declare source basis, claim status, claim boundary, and
freshness requirements where applicable.

## 5. Product Goals

1. Give readers a coherent first-visit understanding of the project.
2. Make exact-GR compatibility and open derivation status clear on physics
   pages.
3. Explain the AI research-agent system as bounded, source-first, and
   human-scaffolded.
4. Convert source authority and claim gates into visible trust architecture.
5. Provide a concrete information architecture for future route, content,
   library, dashboard, and site-builder work.
6. Keep GitHub and source links available as provenance while using internal
   website routes as the primary reading journey.
7. Support phased implementation without requiring all page families before the
   first useful release.

## 6. Non-Goals

The website must not:

- claim GR has been derived from AEther / AEther-flow;
- claim the exact-GR benchmark has been promoted from first principles;
- claim matter coupling or Einstein equations have been derived from substrate
  structure;
- present validators, generated documents, registries, handoffs, or local
  memory as scientific proof;
- publish active current-frontier data without a dated snapshot and source
  basis;
- mutate upstream source-project files;
- use PRDs as a substitute for source authority;
- make GitHub the primary reader path when an internal website route exists.

## 7. Audiences and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand the project thesis, exact-GR compatibility, and open derivation status without needing repository archaeology. |
| Physicist or technical reviewer | Inspect the physics claim boundary, exact benchmark, ontology framing, derivation roadmap, and missing promotion steps. |
| AI researcher | Understand the research-agent architecture, bounded autonomy, role authority, memory discipline, validation, and human gates. |
| Contributor | Find the correct source families, page families, and implementation constraints before proposing changes. |
| Operator | Understand validation, handoffs, current-state refresh, and checkpoint expectations. |
| Site builder | Map future website pages to source anchors, PRDs, manifests, and acceptance criteria. |

## 8. Website Information Architecture

The top-level website information architecture should include at least:

1. Home
2. Physics Research
3. AI Research System
4. Research Operations
5. Source Authority
6. Library
7. Current Frontier
8. Contributor / Site Builder Guide

The IA should converge on this route-family model:

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

Existing route families under project physics, AI research-agent system,
operations, source authority, and resources should be treated as prior art for
future implementation work.

## 9. Required Page Families

The PRD system must eventually support these page families:

| Page family | Primary PRD | Secondary PRDs |
| --- | --- | --- |
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

## 10. Cross-PRD Map

| PRD | Role in the system |
| --- | --- |
| PRD-01 | Defines high-level project explanation, dual-track framing, and primary reader journeys. |
| PRD-02 | Defines physics and mathematical page requirements, including exact-GR benchmark and open derivation boundaries. |
| PRD-03 | Defines research-control workflow pages and the difference between operational validation and proof. |
| PRD-04 | Defines role, schema, and authority-class pages. |
| PRD-05 | Defines memory, registry, retrieval, provenance, and generated-derivative boundaries. |
| PRD-06 | Defines documentation, publication, library, and website-component requirements. |
| PRD-07 | Defines tooling, skills, scripts, runtime, validator, and cache-boundary pages. |
| PRD-08 | Defines repository topology and folder-family orientation. |
| PRD-09 | Defines dated current-frontier pages and stale-data behavior. |
| PRD-10 | Defines positioning, safe public language, approved phrases, and forbidden phrases. |
| PRD-11 | Defines a quick source map for future site builders. |

Dependency rule: PRD-10 and PRD-05 should be written before most public-facing
content PRDs because messaging and source authority constrain the rest of the
system.

## 11. Claim Boundary Policy

This PRD may specify website content that explains:

- the AEther / AEther-flow ontology as a research ontology;
- the exact-GR benchmark as the current observable-scale benchmark;
- the GR derivation burden as open;
- the AI research-agent workflow as governed, source-first, bounded, and
  human-scaffolded;
- current status only as a dated snapshot from tracked project sources.

This PRD must not authorize website content claiming:

- GR has been derived from AEther / AEther-flow;
- matter coupling has been solved;
- Einstein equations have been derived from source-side substrate structure;
- the benchmark has been promoted from first principles;
- validators, generated docs, registries, or handoffs are physics proof;
- local negative results are global theory rejection without tracked authority.

## 12. Current-State Freshness Policy

Any page using active task, latest handoff, milestone, ledger, current frontier,
blocked claims, validator state, or next recommended action data must be treated
as freshness-sensitive.

Current-state pages must:

- display the source basis and refresh date;
- prefer tracked program state, latest relevant handoff, and Distance-to-GR
  ledger evidence over generated summaries when they disagree;
- label generated summaries as reader-facing derivatives;
- show blocked claims prominently;
- avoid permanent hard-coding of transient task IDs, handoff IDs, or current
  milestones unless they are part of a dated historical snapshot;
- include stale-data behavior when refresh evidence is missing or old.

## 13. Content Production Workflow

Future content production should follow this sequence:

1. Identify the page family and controlling PRD.
2. Identify source anchors and authority class.
3. Define claim status and forbidden inferences.
4. Draft reader-facing copy with internal-first navigation.
5. Add provenance links and source notes.
6. Validate route, manifest, content-source, link, layout, SVG, provenance, and
   implementation-control requirements as applicable.
7. Checkpoint locally through the active implementation-control packet.

Content that changes public scientific, mathematical, governance, or workflow
claims requires explicit live approval before implementation.

## 14. Design and UX Principles

The website should feel precise, source-backed, and readable. UX should support
fast orientation and progressively deeper inspection.

Design requirements:

- put the project identity and dual-track thesis in the first viewport on Home;
- use internal route cards and guided starts before source links;
- keep GitHub/source links available as provenance;
- treat caution as a trust feature, not as hidden disclaimer copy;
- separate public narrative, technical explanation, source authority, and
  current-state snapshot surfaces;
- make diagrams, matrices, timelines, and source maps serve explanation rather
  than decoration;
- avoid presenting generated reader surfaces as source authority.

## 15. Functional Requirements

1. The site must provide a Home route that introduces the dual physics-and-AI
   mission.
2. The site must provide physics research routes for ontology, exact-GR
   benchmark, derivation roadmap, and open burdens.
3. The site must provide AI research-system routes for workflow, AgentJob
   lifecycle, roles, schemas, memory, and bounded promotion.
4. The site must provide source-authority routes that explain canonical sources,
   registries, generated derivatives, and local retrieval layers.
5. The site must provide a current-frontier route family with dated snapshot
   semantics.
6. The site must provide a library or resources route family for explainers,
   documents, diagrams, reading paths, and reviewer packets.
7. The site must provide contributor and site-builder orientation.
8. Each page family must define source basis, claim status, claim boundary,
   navigation role, and acceptance criteria.
9. Public claims must use approved language and avoid forbidden claims.
10. PRDs must map future implementation work to validation gates and
    source-authority constraints.

## 16. Non-Functional Requirements

- Source authority: Pages must remain grounded in upstream source materials and
  website manifests where applicable.
- Maintainability: Future implementation packets should be small, reversible,
  and governed by live implementation-control records.
- Auditability: Readers and maintainers must be able to trace public claims to
  source anchors or provenance notes.
- Safety: The site must fail conservative on stale current-state data and
  public claim uncertainty.
- Performance: Static pages should remain buildable as Astro pages without
  adding unnecessary runtime services.
- Portability: PRDs should avoid brittle code snippets and file paths except
  when source maps or route requirements need explicit names.

## 17. Accessibility Requirements

Future page implementations should:

- use semantic headings and landmarks;
- keep diagrams accompanied by HTML labels, captions, and descriptions;
- avoid relying on color alone for claim status, risk, or freshness;
- provide readable tables or alternate summaries for matrices and source maps;
- keep keyboard navigation and focus states intact;
- preserve the repository SVG rule that visual SVG figures are animated and do
  not contain visible embedded text.

## 18. SEO and Discoverability Requirements

The website should make the project discoverable through precise, conservative
language:

- use "exact-GR benchmark," "open first-principles derivation," "AEther-flow
  ontology," "research-agent workflow," and "source-backed claim boundaries";
- avoid unsupported claims of new tested gravity predictions or completed GR
  derivation;
- provide page titles and descriptions that distinguish physics, AI workflow,
  source authority, and current frontier content;
- make library and guided-start pages useful for readers arriving from search,
  GitHub, or external AI systems.

## 19. Metrics and Success Criteria

Success is measured by readiness for implementation and reader clarity, not by
scientific promotion.

Minimum success criteria:

- every sub-PRD has a clear role in the information architecture;
- the master PRD prevents completed-derivation overclaims;
- the site IA gives readers internal paths to the project, physics, AI system,
  source authority, current frontier, and library;
- current-state material has freshness rules;
- implementation teams can derive route, content, provenance, and validation
  tasks from the PRD system.

## 20. Launch Phases

Phase 1: Master and positioning foundation.

- Create PRD-00 and PRD-10.
- Lock the site mission, safe pitch, approved phrases, and forbidden phrases.

Phase 2: Source authority and publication foundation.

- Create PRD-05 and PRD-06.
- Define source/provenance footers and generated-derivative warnings.

Phase 3: Public story and physics foundation.

- Create PRD-01, PRD-02, and PRD-09.
- Define homepage, physics pages, adoption-versus-derivation explanation, and
  current-frontier freshness behavior.

Phase 4: AI workflow, roles, tooling, topology, and site-builder support.

- Create PRD-03, PRD-04, PRD-07, PRD-08, and PRD-11.
- Complete role, schema, tooling, repository-map, and source-map support.

Phase 5: Review and implementation planning.

- Check the PRD validation checklist.
- Produce follow-on implementation plans and task packets.

## 21. Risks

| Risk | Mitigation |
| --- | --- |
| Public copy overstates physics status. | Use PRD-10 approved and forbidden language plus PRD-02 claim-boundary requirements. |
| Current-frontier content becomes stale. | Use dated snapshots, source-basis labels, and stale-data warnings from PRD-09. |
| Generated reader surfaces are treated as authority. | Use PRD-05 and PRD-06 to classify derivatives and require provenance notes. |
| Website IA becomes too broad for implementation. | Use phased launch scope and one bounded implementation packet at a time. |
| AI workflow pages sound like autonomous proof claims. | Use PRD-03 and PRD-04 to separate model/tool behavior, validation, human gates, and scientific proof. |
| Source links replace the reader journey. | Keep internal routes primary and use source/GitHub links as provenance. |

## 22. Open Questions

1. Which route family should be implemented first after the PRD system is
   complete: Home, Physics Research, Source Authority, or Current Frontier?
2. Should the current-frontier route use a generated static snapshot only, or a
   curator-generated package with explicit stale-data diagnostics?
3. Which diagrams are mandatory for the first public release: source authority,
   Distance-to-GR, AgentJob lifecycle, or full website IA?
4. Should contributor and site-builder guidance live under Resources,
   Operations, or a separate Site Builder Guide route family?

None of these questions blocks the master PRD. They should be resolved in
sub-PRDs or follow-on implementation plans.

## 23. Definition of Done

This master PRD is complete when:

- it names all eleven sub-PRDs;
- it defines the site mission and non-goals;
- it defines the source-authority model;
- it defines the claim-boundary policy;
- it defines the current-frontier freshness policy;
- it defines reader audiences and page families;
- it defines launch phases and MVP scope;
- it prevents completed-GR-derivation claims;
- it gives the local implementation team a concrete website information
  architecture.

The full PRD system is complete only after all eleven sub-PRDs exist, follow the
shared template, define source anchors and acceptance criteria, and pass the PRD
validation checklist.

## 24. Sub-PRD Index

| PRD | File | Status | Launch role |
| --- | --- | --- | --- |
| PRD-01 | `PRD-01-high-level-components.md` | complete | Public story and primary journeys. |
| PRD-02 | `PRD-02-physics-and-mathematical-components.md` | complete | Physics, benchmark, ontology, and derivation pages. |
| PRD-03 | `PRD-03-research-control-and-agent-workflow.md` | pending | AI workflow and research-control pages. |
| PRD-04 | `PRD-04-role-and-schema-components.md` | pending | Role and schema authority pages. |
| PRD-05 | `PRD-05-memory-registry-and-retrieval-components.md` | complete | Source authority, registries, memory, and provenance. |
| PRD-06 | `PRD-06-documentation-publication-and-website-components.md` | complete | Publication, library, and website-component requirements. |
| PRD-07 | `PRD-07-tooling-skills-scripts-and-runtime-components.md` | pending | Tooling, scripts, validators, runtime, and cache boundaries. |
| PRD-08 | `PRD-08-folder-and-repository-topology-components.md` | pending | Repository topology and folder-family orientation. |
| PRD-09 | `PRD-09-current-research-frontier-for-website-use.md` | pending | Dated current-state snapshots and stale-data behavior. |
| PRD-10 | `PRD-10-website-positioning-guidance.md` | complete | Safe public messaging and forbidden claims. |
| PRD-11 | `PRD-11-quick-source-map-for-site-builders.md` | pending | Source map for future page builders. |

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].

The AEther Flow Website. (2026). *Website Information-Space PRD Index*
[Product requirements index].
