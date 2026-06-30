---
prd_id: "PRD-05"
title: "Memory, Registry, and Retrieval Components"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Source authority, registries, memory, retrieval, and provenance"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-10-website-positioning-guidance.md"
  - "PRD-08-folder-and-repository-topology-components.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-05: Memory, Registry, and Retrieval Components

## 1. Summary

This PRD defines website requirements for explaining The AEther Flow Project's
source-first memory model, registries, retrieval layers, generated derivatives,
and provenance graph.

The central product rule is that source authority and retrieval convenience are
different things. Registries and canonical sources can support claims; local
memory, generated wiki pages, semantic extracts, Obsidian mirrors, SQLite
indexes, PDFs, HTML explainers, and GitHub-facing Markdown can help readers and
agents navigate, but they do not independently promote scientific or workflow
claims.

## 2. Product Purpose

The website needs a public source-authority and provenance system because the
project is complex, source-rich, and easy to overread. Readers should be able
to see which materials are canonical, which are derivatives, which are local
retrieval support, and which claims require upstream verification.

This PRD gives future page builders the requirements for:

- a source authority explainer;
- a registry explorer;
- a memory-system explainer;
- a provenance graph;
- generated-derivative warnings;
- source versus derivative versus retrieval matrices;
- source/provenance footers on website pages.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, or research-workflow authority.

Source basis for implementation should include:

- `registries/`;
- `registries/TEX_SOURCE_REGISTRY.csv`;
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`;
- `registries/PDF_DERIVATIVE_REGISTRY.csv`;
- `registries/HTML_EXPLAINER_REGISTRY.csv`;
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`;
- `registries/DISTANCE_TO_GR_LEDGER.csv`;
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`;
- `wiki/`;
- `.local/content_semantics/`;
- `.local/obsidian/`;
- `.codex/skills/project-memory-system/SKILL.md`;
- the website master PRD and positioning PRD.

Implementation must verify authoritative claim text against canonical sources
or registry-backed records, not against retrieval hits alone.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand why some website pages are source-backed while others are reader aids or navigation surfaces. |
| Physicist or reviewer | Identify canonical physics sources before evaluating technical claims. |
| AI researcher | Understand how memory and retrieval help navigation without replacing source inspection. |
| Contributor | Learn which registry or source lane must be updated for each kind of content change. |
| Operator | Distinguish validator, registry, current-state, derivative, and retrieval evidence during packet execution. |
| Site builder | Map page claims to canonical sources, registries, derivatives, and provenance footers. |

## 5. Scope

In scope:

- source authority explainer requirements;
- registry explorer requirements;
- memory-system explainer requirements;
- provenance graph requirements;
- source/provenance footer requirements;
- generated-derivative warning requirements;
- source versus derivative versus retrieval matrix requirements;
- copy rules that prevent retrieval or generated artifacts from being treated
  as proof.

Out of scope:

- implementing registry dashboards or public pages;
- refreshing upstream source snapshots;
- mutating upstream source-project files;
- changing generated `.local/` retrieval artifacts;
- changing public manifests;
- promoting scientific claims.

## 6. Non-Goals

This PRD must not:

- treat local memory search as source authority;
- treat Obsidian, SQLite, semantic extracts, or generated wiki pages as
  canonical evidence;
- treat PDFs, HTML explainers, or GitHub-facing Markdown as stronger than their
  registered source materials;
- require website users to leave the site for every source explanation;
- turn registry dashboards into scientific proof claims;
- create a public current-state dashboard without PRD-09 freshness rules.

## 7. Website Surfaces

Required surfaces:

- Source authority explainer;
- Registry explorer;
- Memory-system explainer;
- Provenance graph;
- Generated derivative warning component;
- Source versus derivative versus retrieval matrix.

Supporting surfaces:

- source/provenance footer on every public page;
- source cards for canonical TeX, Markdown, registry, derivative, and retrieval
  categories;
- glossary entries for canonical source, generated derivative, retrieval layer,
  current snapshot, and requirements-planning artifact.

## 8. Functional Requirements

1. Explain TeX source authority for physics claims.
2. Explain Markdown source authority for authored documentation, contracts,
   role definitions, schema descriptions, publication briefs, and source specs.
3. Label PDFs, HTML explainers, GitHub-facing Markdown, and wiki pages as
   generated or reader-facing derivatives where appropriate.
4. Classify `.local/` as local retrieval/cache state.
5. Explain CSV registries as provenance, relationship, validation, and workflow
   state.
6. Explain memory lookup as navigation, not authority.
7. Require canonical source inspection before using retrieved hits in claim
   text.
8. Require registry-driven dashboards to include "not scientific proof"
   language.
9. Require generated surfaces to be visibly labeled as noncanonical when they
   are not the source of authority.
10. Require every website page to expose a source/provenance footer or
    equivalent visible provenance note.

## 9. Non-Functional Requirements

- Accuracy: Authority classes must be explicit and conservative.
- Auditability: Readers should be able to trace major claims to source anchors.
- Maintainability: Source classifications should align with registries and
  folder topology rather than page-local guesswork.
- Resilience: Retrieval freshness warnings must not be confused with canonical
  source failure unless a source validator says so.
- Usability: Provenance surfaces should help readers navigate without forcing
  them into repository archaeology.
- Safety: Generated derivatives must not silently become claim authority.

## 10. Claim Boundary

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

Additional authority boundary:

Memory hits, generated derivatives, and retrieval layers may locate candidate
sources. They do not independently authorize public claims.

## 11. Content Requirements

The source-versus-derivative-versus-retrieval matrix must include at least:

| Category | Examples | Website label | Claim use |
| --- | --- | --- | --- |
| Canonical physics source | registered TeX sources | canonical physics authority | Use for technical physics claims after source inspection. |
| Canonical documentation source | registered Markdown sources | authored source authority | Use for workflow, role, schema, and publication-process claims. |
| Registry | CSV source, derivative, role, task, ledger, and relationship registries | provenance and workflow state | Use for traceability, status, and relationship claims. |
| Generated derivative | PDFs, HTML explainers, GitHub-facing Markdown, generated wiki pages | reader-facing derivative | Use for reading support; verify claims upstream. |
| Local retrieval layer | semantic extracts, Obsidian mirrors, SQLite index, `.local/` caches | retrieval support | Use for navigation only. |
| Website PRD | PRD files in this directory | requirements-planning artifact | Use for implementation requirements, not source authority. |

Required copy fragments:

- "Memory lookup is a navigation aid, not claim authority."
- "Generated derivatives help readers inspect the project, but registered
  sources and tracked control records remain authoritative."
- "Registry dashboards show provenance and status; they do not prove physics
  claims."
- "When source and derivative disagree, inspect the canonical source and
  current tracked control record."

## 12. UX and Navigation Requirements

The source-authority UX should:

- use a clear visual hierarchy from canonical source to derivative to retrieval
  support;
- provide route cards for canonical sources, registries, generated derivatives,
  retrieval layers, and site-builder source maps;
- make source/provenance footers short enough to read but specific enough to
  support audit;
- include warning states for stale or generated material without making the
  site feel broken;
- keep internal website routes primary and source links available as
  provenance.

The registry explorer UX should:

- allow readers to understand what each registry does before seeing rows;
- surface claim-boundary notes before detailed tables;
- distinguish source registries from derivative registries and workflow
  registries.

## 13. Data, Source, and Provenance Requirements

Website implementations based on this PRD should treat:

- TeX source registries as the strongest physics source lane;
- Markdown source registries as authored documentation and contract source
  lanes;
- derivative registries as generated-output tracking;
- relationship registries as provenance graph edges;
- AgentJob, Director Decision, role-execution, and research-task registries as
  workflow state;
- Distance-to-GR and claim-boundary registries as claim-status and burden-map
  evidence;
- local semantic, Obsidian, SQLite, and `.local/` layers as retrieval support.

Every public page should declare one of these provenance statuses:

- source-backed;
- generated derivative;
- current snapshot;
- requirements-planning;
- retrieval support;
- mixed, with explicit source-basis details.

## 14. User Stories

1. As a reader, I want to know which source supports a page, so that I can
   judge whether I am reading authority, a derivative, or a guide.
2. As a physicist, I want physics claims linked back to registered TeX sources,
   so that I can inspect the actual claim-bearing text.
3. As an AI researcher, I want memory and retrieval explained as navigation, so
   that I do not mistake search results for source verification.
4. As a contributor, I want registry categories explained, so that I can update
   the correct source or derivative lane.
5. As an operator, I want retrieval freshness warnings separated from canonical
   source failures, so that I can route maintenance work correctly.
6. As a site builder, I want source/provenance footer requirements, so that
   every public page has an audit trail.

## 15. Acceptance Criteria

- Every website page has a source/provenance footer or equivalent visible
  provenance note.
- Registry-driven dashboards include "not scientific proof" language.
- Generated surfaces are visibly labeled as noncanonical where appropriate.
- The source-authority page is linked from the homepage and technical sections.
- Memory lookup is described as navigation, not authority.
- `.local/`, Obsidian, SQLite, semantic extracts, and generated wiki layers are
  classified as retrieval or generated support rather than source authority.
- Canonical source inspection is required before retrieved hits affect public
  claim text.

## 16. Dependencies

- PRD-00 defines the master source-authority model and page-family map.
- PRD-10 defines safe public phrasing and forbidden overclaims.
- PRD-08 will define folder and repository topology in more detail.
- PRD-06 depends on this PRD for publication, derivative, and library
  provenance requirements.
- PRD-01, PRD-02, PRD-03, PRD-04, PRD-07, PRD-09, and PRD-11 depend on this PRD
  for source, registry, retrieval, and provenance discipline.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Readers treat polished generated pages as canonical sources. | Add visible derivative labels and source/provenance footers. |
| Site builders cite memory hits directly in public claims. | Require canonical source inspection before retrieved hits affect claim text. |
| Registry dashboards look like proof dashboards. | Include "provenance/status, not scientific proof" language near dashboards. |
| Retrieval freshness warnings derail unrelated packets. | Explain retrieval warnings as navigation-layer issues unless canonical validators fail. |
| Source links overwhelm general readers. | Keep internal explanations primary and source links available as provenance. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Check that each page declares provenance status.
2. Check that technical physics claims cite canonical source lanes.
3. Check that generated derivatives are labeled as derivatives.
4. Check that retrieval surfaces are labeled as retrieval support.
5. Search page copy for phrasing that treats validators, generated docs,
   registries, or memory hits as proof.
6. Run applicable content, provenance, implementation-control, and build
   validators for the implementation packet.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: MVP foundation.

This PRD should follow PRD-00 and PRD-10 because source authority and retrieval
discipline constrain homepage, physics, publication, current-frontier, AI
workflow, role, tooling, topology, and site-builder requirements.

## 20. Open Questions

1. Should future route implementation include a full registry explorer in the
   MVP, or only a source-authority explainer and lightweight registry cards?
2. Should source/provenance footers be a shared component, page-frontmatter
   convention, manifest-driven block, or all three?
3. Should retrieval freshness warnings appear in public pages, maintainer-only
   pages, or build/curator reports?

These questions do not block this PRD. They should be resolved in PRD-06,
PRD-08, PRD-11, or follow-on implementation plans.

## 21. Definition of Done

This PRD is complete when:

- it explains TeX, Markdown, registry, derivative, and retrieval authority
  classes;
- it requires source/provenance footers for public pages;
- it defines generated-derivative warning requirements;
- it defines memory lookup as navigation, not authority;
- it defines the need to inspect canonical sources before public claim use;
- it gives future source-authority, registry, memory, and provenance pages a
  testable requirements contract.

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].

The AEther Flow Website. (2026). *Website Positioning Guidance* [Product
requirements document].
