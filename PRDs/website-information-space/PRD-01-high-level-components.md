---
prd_id: "PRD-01"
title: "High-Level Components"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Homepage, project overview, dual-track framing, and primary reader journeys"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-10-website-positioning-guidance.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
  - "PRD-06-documentation-publication-and-website-components.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-01: High-Level Components

## 1. Summary

This PRD defines the high-level public explanation system for The AEther Flow
Website. It covers the homepage, project overview, dual-track project map,
exact-GR benchmark summary, open derivation burden summary, AI research-agent
system summary, trust and claim-boundary panel, and primary reader journeys.

The central product rule is that a new reader should understand the project
quickly without being invited to infer a completed derivation. The website
should present the physics and AI tracks as co-equal parts of one disciplined
research program: exact-GR-compatible physics plus a governed AI research
system for pursuing the still-open first-principles derivation.

## 2. Product Purpose

The high-level website layer exists to answer the first reader question:
"What is this project, and why should I trust its boundaries?"

This PRD gives future page builders the requirements for:

- a homepage hero that states the dual mission immediately;
- a project overview page that introduces the whole system;
- a dual-track project map;
- a clear adoption-versus-derivation explanation;
- summary cards for the exact-GR benchmark, open derivation burden, and AI
  research-agent system;
- reader paths for general readers, physicists, AI researchers, contributors,
  and site builders;
- a visible "what this project does not claim" trust panel.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, or research-workflow authority.

Source basis for implementation should include:

- `README.md`;
- `AGENTS.md`;
- `research_control/README.md`;
- `research_control/current_frontier.md`;
- `research_control/design/gr_derivation_burden_map.md`;
- `ontology/aether-and-aether-flow.md`;
- `ontology/tex/`;
- `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`;
- `ontology/tex/aether_flow_exact_closure_note.tex`;
- `registries/DISTANCE_TO_GR_LEDGER.csv`;
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`;
- `github-facing/project-overview-explainer.md`;
- `html/project-overview-explainer.html`;
- the website positioning, source-authority, and publication PRDs.

Implementation must verify public claim wording against upstream source
materials and current tracked project state before publishing new or revised
homepage or overview copy.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand the project in one minute: dual physics and AI mission, exact-GR compatibility, and open derivation status. |
| Physicist or reviewer | See the exact-GR benchmark, ontology framing, open derivation burden, and blocked inferences without marketing fog. |
| AI researcher | Understand the agent workflow as governed research infrastructure, not an autonomous proof machine. |
| Contributor | Find the right first sources, source-authority boundaries, and next reading path before proposing changes. |
| Operator | Know how homepage and overview copy should route to current-state, source-authority, and validation requirements. |
| Site builder | Derive route, card, panel, and navigation requirements for the first public information layer. |

## 5. Scope

In scope:

- homepage hero requirements;
- project overview requirements;
- dual-track project map requirements;
- exact-GR benchmark summary requirements;
- open derivation burden summary requirements;
- AI research-agent system summary requirements;
- trust and claim-boundary panel requirements;
- reader-path requirements for major audiences;
- internal-first navigation requirements.

Out of scope:

- implementing homepage or overview route changes;
- changing public route copy;
- refreshing current-frontier snapshots;
- changing generated explainers, PDFs, wiki, or `.local/` retrieval layers;
- mutating upstream source-project files;
- promoting scientific claims.

## 6. Non-Goals

This PRD must not:

- claim GR has been derived from AEther / AEther-flow;
- treat exact-GR benchmark adoption as first-principles derivation;
- present the AI research-agent system as autonomous proof;
- make GitHub or source files the primary reader journey when an internal
  website route exists;
- hide claim limitations in small disclaimers;
- force a single generic template onto every high-level page;
- require route implementation before the PRD family is complete.

## 7. Website Surfaces

Required surfaces:

- Homepage hero;
- Project overview page;
- Dual-track project map;
- Exact-GR benchmark summary card;
- Open derivation burden summary card;
- AI research-agent system summary card;
- Trust and claim-boundary panel.

Supporting surfaces:

- first-read guided path;
- audience-specific starts;
- source-authority route card;
- current-frontier route card;
- publication/library route card;
- contributor or site-builder route card;
- visible "what this project does not claim" element.

## 8. Functional Requirements

1. Explain the project in one precise sentence.
2. Present the physics and AI research tracks as co-equal parts of the project.
3. Show that exact-GR benchmark adoption and first-principles derivation are
   different states.
4. Explain why the AI research-agent system matters while the physics
   derivation remains open.
5. Provide reader paths for general readers, physicists, AI researchers,
   contributors, and site builders.
6. Require the homepage hero to state the dual mission, exact-GR status, and
   open derivation burden before deep technical content.
7. Require three first-level summary cards: the ontology or physics idea, the
   exact benchmark, and the research-agent system.
8. Require a visible trust panel explaining claims made, claims not made, and
   how claim promotion is gated.
9. Link to source-authority guidance before asking readers to evaluate deep
   technical claims.
10. Keep internal website routes primary and source links available as
    provenance.

## 9. Non-Functional Requirements

- Clarity: A new reader should answer "what is this project?" within one
  minute.
- Precision: The first screen must separate exact-GR compatibility from
  first-principles derivation.
- Balance: Physics and AI research-system material should appear as two parts
  of one program, not as a main topic plus an appendix.
- Auditability: High-level claims must point to source-authority and
  current-state paths.
- Maintainability: The overview model should survive later route or component
  redesigns.
- Safety: If source status is stale or uncertain, public copy must choose the
  weaker claim.

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

Additional first-read boundary:

High-level pages may be promotional, but they must make caution part of the
project identity. The strongest public story is disciplined ambition, not
completed proof.

## 11. Content Requirements

Baseline one-sentence explanation:

> The AEther Flow Project is a dual physics and AI research program that
> presents an exact-GR-compatible interpretation of relativity while building a
> governed AI research-agent system for pursuing the still-open derivation from
> deeper substrate structure.

Required homepage or overview content blocks:

| Block | Required message | Claim boundary |
| --- | --- | --- |
| Hero | Dual physics and AI mission, exact-GR compatibility, and open derivation burden. | Must not imply completed derivation. |
| Dual-track map | Physics track supplies the hard research problem; AI track supplies auditable workflow. | Must not demote either track to decoration. |
| Exact-GR benchmark card | Observable-scale benchmark remains ordinary GR through the accepted effective package. | Must not call this first-principles promotion. |
| Open derivation burden card | Source-side derivation work remains open and milestone-gated. | Must not imply the missing steps are solved. |
| AI research-agent card | Roles, AgentJobs, validators, memory, handoffs, and human gates make work auditable. | Must not call validators or agents proof. |
| Trust panel | Claims made, claims not made, and how source authority works. | Must link to source authority before deep claims. |

Required claims to use:

- exact-GR benchmark;
- GR-consistent interpretation;
- open first-principles derivation burden;
- dual physics and AI research program;
- source-backed research-control system;
- human-scaffolded AI research-agent workflow;
- claim-gated derivation program.

Required claims to avoid:

- GR has been derived;
- Einstein equations derived from AEther;
- matter coupling solved;
- benchmark promoted from first principles;
- new tested gravity prediction;
- autonomous proof system;
- validators prove the theory.

## 12. UX and Navigation Requirements

The first-read UX should:

- make Home the canonical first reader surface;
- show a concise project identity before dense technical or governance detail;
- give readers three immediate doors: physics idea, exact benchmark, and AI
  research system;
- include a visible route to source authority before technical deep dives;
- expose "what this project does not claim" as a normal trust feature;
- provide separate but connected reader paths for general readers, physicists,
  AI researchers, contributors, and site builders;
- keep source/GitHub links available as provenance rather than making them the
  primary journey.

Recommended primary reader paths:

| Reader | First path |
| --- | --- |
| General reader | Home to Project Overview to Reading Path or Library. |
| Physicist | Home to Exact-GR Benchmark to Derivation Roadmap to Source Authority. |
| AI researcher | Home to Research-Agent System to AgentJob Lifecycle to Roles and Schemas. |
| Contributor | Home to Source Authority to Site Builder Guide to Repository Map. |
| Site builder | Home to Site Builder Guide to Page-to-Source Map to PRD family. |

## 13. Data, Source, and Provenance Requirements

Every high-level page should declare:

- page purpose;
- primary audience;
- source basis;
- claim status;
- claim boundary;
- freshness rule if current-state data is shown;
- internal next route;
- source/provenance footer status.

Homepage and project overview pages should use source links as provenance, not
as the first required reading step. If current task, handoff, ledger, milestone,
or blocked-claim data appears, the page becomes freshness-sensitive and must
use PRD-09 rules.

## 14. User Stories

1. As a general reader, I want a precise one-sentence explanation, so that I
   can understand the project before seeing technical detail.
2. As a physicist, I want exact-GR benchmark status separated from open
   derivation status, so that I can evaluate the claim honestly.
3. As an AI researcher, I want the agent system explained as governance
   infrastructure, so that I can understand its value without treating it as
   proof.
4. As a contributor, I want guided starts and source-authority links, so that I
   can find the right source lane before proposing changes.
5. As an operator, I want high-level pages to expose claim boundaries, so that
   route updates do not create unsupported public claims.
6. As a site builder, I want card, panel, and reader-path requirements, so that
   the homepage and overview can be implemented consistently.

## 15. Acceptance Criteria

- A new reader can answer "what is this project?" within one minute.
- The homepage does not imply that GR has been derived.
- The overview separates exact-GR benchmark adoption from first-principles
  derivation.
- Physics and AI research tracks appear as co-equal parts of the project.
- The page links to source-authority guidance before deep technical claims
  appear.
- The page includes a visible "what this project does not claim" element.
- Reader paths exist for general readers, physicists, AI researchers,
  contributors, and site builders.
- High-level pages use approved positioning language and avoid forbidden
  claims from PRD-10.

## 16. Dependencies

- PRD-00 defines the master website mission and page-family map.
- PRD-10 defines safe public positioning, approved claims, and forbidden
  claims.
- PRD-05 defines source authority, generated derivative, memory, registry, and
  provenance boundaries.
- PRD-06 defines publication and library requirements that support high-level
  reader journeys.
- PRD-02 will define deeper physics and mathematical page requirements.
- PRD-09 will define current-frontier freshness behavior when high-level pages
  include active status data.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| The homepage sounds like a completed physics proof. | Require a visible open-derivation burden card and forbidden-claim QA. |
| The AI system looks like an unrelated tooling appendix. | Present physics and AI as co-equal tracks that meet at the derivation burden. |
| Caution feels like a weakness. | Treat claim boundaries and negative-result preservation as trust architecture. |
| Source links overwhelm new readers. | Use internal-first guided journeys with source links as provenance. |
| Current-state snippets become stale. | Use PRD-09 freshness rules or avoid live status on high-level pages. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Check first-viewport copy against PRD-10 approved and forbidden language.
2. Check that exact-GR benchmark language is not phrased as completed
   first-principles derivation.
3. Check that physics and AI tracks are both visible in the first reader
   journey.
4. Check that source-authority links or provenance notes appear before deep
   technical claims.
5. Check that current-state content, if present, has dated source basis and
   staleness behavior.
6. Run applicable content, provenance, route, build, browser, and
   implementation-control validators for implementation packets.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: MVP foundation.

This PRD should follow PRD-10, PRD-05, and PRD-06 because the public story needs
safe messaging, source authority, and publication process requirements before
high-level route implementation is specified.

## 20. Open Questions

1. Should the homepage include current-frontier status in the first release, or
   defer that to a dedicated current-frontier route until PRD-09 is complete?
2. Should the project overview be a separate route, a Home section, or both
   with different reader jobs?
3. What is the minimum first-release reader path: Home plus source authority,
   or Home plus project overview plus library?
4. Should the trust panel be a reusable component, a page section convention,
   or a manifest-driven block?

These questions do not block this PRD. They should be resolved in PRD-02,
PRD-09, PRD-11, or follow-on implementation plans.

## 21. Definition of Done

This PRD is complete when:

- it defines homepage and project overview requirements;
- it defines the dual-track project map;
- it defines exact-GR benchmark, open derivation burden, and AI research-agent
  summary requirements;
- it defines primary reader journeys;
- it requires visible claim-boundary and source-authority access;
- it prevents high-level public pages from implying completed GR derivation.

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].

The AEther Flow Website. (2026). *Website Positioning Guidance* [Product
requirements document].

The AEther Flow Website. (2026). *Memory, Registry, and Retrieval Components*
[Product requirements document].

The AEther Flow Website. (2026). *Documentation, Publication, and Website
Components* [Product requirements document].
