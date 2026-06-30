---
prd_index_id: "WIS-PRD-INDEX"
title: "Website Information-Space PRD Index"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
prd_system_plan: "ImplementationPlans/aether_flow_website_prd_system.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# Website Information-Space PRD Index

## Purpose

This directory contains the PRD family for the public information space of The
AEther Flow Website. The PRDs define how the website should explain, organize,
and promote The AEther Flow Project while preserving source authority and claim
boundaries.

The PRD family is based on two planning inputs:

- the project components catalogue;
- the website PRD-system handoff plan.

The PRDs are requirements-planning artifacts. They do not create scientific,
mathematical, governance, or research-workflow authority.

## Current Progress

| Artifact | Status | Notes |
| --- | --- | --- |
| `README.md` | complete | Index packet checkpointed before the master PRD packet. |
| `PRD-00-master-website-information-space.md` | complete | Defines the website mission, source-authority model, information architecture, launch phases, and sub-PRD map. |
| `PRD-10-website-positioning-guidance.md` | complete | Defines safe public positioning, approved phrasing, forbidden claims, homepage guidance, audience pitches, and copy QA. |
| `PRD-05-memory-registry-and-retrieval-components.md` | complete | Defines source authority, registry, generated derivative, memory, retrieval, provenance, and source/provenance footer requirements. |
| Remaining sub-PRDs | pending | Create one bounded packet at a time in dependency order. |

## Source Authority Boundary

Website PRDs may specify reader-facing explanations, routes, content models,
source maps, acceptance criteria, and validation expectations. They must not
authorize website content that silently strengthens upstream claims.

The PRD system may describe:

- the project as a dual physics and AI research program;
- the exact-GR benchmark as the current observable-scale benchmark;
- first-principles GR derivation from the AEther / AEther-flow ontology as open
  work;
- the AI research-agent system as governed, bounded, source-first, and
  human-scaffolded;
- current research status only as a dated snapshot from tracked project
  sources.

The PRD system must not claim:

- GR has been derived from AEther / AEther-flow;
- matter coupling has been solved;
- Einstein equations have been derived from source-side substrate structure;
- the exact-GR benchmark has been promoted from first principles;
- validators, generated documents, registries, handoffs, or local memory are
  physics proof;
- local negative results are global theory rejection without tracked authority.

## Required PRD Files

The target PRD family contains one index, one master PRD, and eleven sub-PRDs:

| Order | File | Purpose |
| --- | --- | --- |
| 1 | `README.md` | Index, dependency order, shared boundaries, and execution map. |
| 2 | `PRD-00-master-website-information-space.md` | Whole-site information-space vision, IA, goals, launch phases, and cross-PRD map. |
| 3 | `PRD-10-website-positioning-guidance.md` | Safe public positioning, approved phrases, forbidden phrases, and homepage messaging boundaries. |
| 4 | `PRD-05-memory-registry-and-retrieval-components.md` | Source authority, registries, generated derivatives, memory, and retrieval requirements. |
| 5 | `PRD-06-documentation-publication-and-website-components.md` | Publication workflow, documentation layers, library surfaces, and provenance expectations. |
| 6 | `PRD-01-high-level-components.md` | High-level project explanation, dual-track framing, and primary reader journeys. |
| 7 | `PRD-02-physics-and-mathematical-components.md` | Physics and mathematics pages, exact-GR benchmark boundary, and open derivation milestones. |
| 8 | `PRD-09-current-research-frontier-for-website-use.md` | Dated current-state snapshot requirements and stale-data behavior. |
| 9 | `PRD-03-research-control-and-agent-workflow.md` | Research-control workflow, AgentJobs, handoffs, validation, and proof-boundary requirements. |
| 10 | `PRD-04-role-and-schema-components.md` | Role catalogue, schemas, authority classes, and human-gated promotion requirements. |
| 11 | `PRD-07-tooling-skills-scripts-and-runtime-components.md` | Tooling, skills, scripts, validators, runtime, and local-cache boundaries. |
| 12 | `PRD-08-folder-and-repository-topology-components.md` | Repository topology, folder families, reader-facing source map, and site-builder orientation. |
| 13 | `PRD-11-quick-source-map-for-site-builders.md` | Concise source map for future page builders and implementation agents. |

## Dependency Order

The PRDs should be created in dependency order, not numerical order:

1. Create the index.
2. Define the master information-space contract.
3. Lock public positioning and forbidden-claim language.
4. Define source authority, memory, registry, and publication boundaries.
5. Specify high-level and physics-facing page families.
6. Specify current-frontier and AI workflow pages.
7. Specify roles, tooling, topology, and site-builder support.
8. Review the whole set against the validation checklist.

Reasoning: the website must establish messaging, source authority, publication
process, and claim boundaries before detailed technical or physics page
requirements are written.

## Shared PRD Requirements

Every detailed PRD in this directory should include:

- YAML frontmatter with PRD ID, status, owner role, source catalogue, source
  authority class, dates, dependency list, and claim-boundary flags.
- Summary, product purpose, source authority, audience, scope, non-goals,
  website surfaces, functional requirements, non-functional requirements, claim
  boundary, content requirements, UX and navigation requirements, provenance
  requirements, user stories, acceptance criteria, dependencies, risks,
  validation plan, launch priority, open questions, and definition of done.
- Specific source anchors from the catalogue.
- Explicit accepted and forbidden claim language when public messaging is in
  scope.
- A validation plan that distinguishes operational checks from scientific
  proof.

## MVP Package

The minimum useful PRD package is:

1. `README.md`
2. `PRD-00-master-website-information-space.md`
3. `PRD-10-website-positioning-guidance.md`
4. `PRD-05-memory-registry-and-retrieval-components.md`
5. `PRD-06-documentation-publication-and-website-components.md`
6. `PRD-01-high-level-components.md`
7. `PRD-02-physics-and-mathematical-components.md`
8. `PRD-09-current-research-frontier-for-website-use.md`

The remaining PRDs complete the implementation support surface for roles,
tooling, repository topology, and site builders.

## Execution Phases

Phase 0: Create this index and establish the directory.

Phase 1: Create the master PRD and website positioning PRD.

Phase 2: Create source-authority, memory, registry, documentation, and
publication PRDs.

Phase 3: Create high-level project and physics/mathematics PRDs.

Phase 4: Create current-frontier and research-control workflow PRDs.

Phase 5: Create role/schema, tooling/runtime, topology, and source-map PRDs.

Phase 6: Review all PRDs against the validation checklist and produce a final
handoff.

## Validation Checklist

Before the PRD family is treated as ready for implementation planning:

- All required PRD files exist.
- Every PRD has a source basis and claim-boundary section.
- Forbidden claim language is absent.
- The exact-GR benchmark is separated from first-principles derivation.
- Current-frontier requirements are freshness-sensitive.
- Generated derivatives, memory, wiki, PDF, HTML, registries, and local caches
  are correctly classified.
- Validators are described as operational checks, not scientific proof.
- Public route and implementation requirements remain internal-first and
  source-provenance aware.

## Next Packet

The next bounded implementation-control packet should create
`PRD-00-master-website-information-space.md`. It should not create additional
sub-PRDs in the same packet unless fresh live control records authorize a wider
scope.

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].
