---
prd_id: "PRD-10"
title: "Website Positioning Guidance"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Public positioning and copy guidance"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-10: Website Positioning Guidance

## 1. Summary

This PRD defines the public messaging system for The AEther Flow Website. It
specifies safe positioning, homepage copy rules, approved vocabulary,
forbidden claims, audience-specific pitch cards, trust-building language, and a
copy QA checklist.

The central positioning rule is ambitious but conservative: the website may
promote the project as a dual physics-and-AI research program with an exact-GR
benchmark and governed AI research workflow, but it must keep first-principles
derivation from AEther / AEther-flow ontology explicitly open.

## 2. Product Purpose

The positioning system exists so every public page can speak with one coherent
voice:

- clear enough for a first-time reader;
- precise enough for a technical reviewer;
- promotional enough to explain why the project matters;
- restrained enough to preserve source authority and blocked-claim boundaries.

The website should treat caution as credibility. It should make the current
limits legible rather than burying them as disclaimers.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not authorize scientific,
mathematical, governance, or research-workflow claims.

Source basis for implementation should include:

- `README.md`;
- `AGENTS.md`;
- `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`;
- `ontology/tex/aether_flow_exact_closure_note.tex`;
- `research_control/current_frontier.md`;
- `research_control/design/gr_derivation_burden_map.md`;
- `github-facing/claim-gates-explainer.md`;
- `html/project-overview-explainer.html`;
- the website information-space master PRD.

When source materials disagree or current-state evidence appears stale,
implementation must defer to the higher-authority tracked source records named
by the live workflow rather than strengthening website copy.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand the project in one sentence without mistaking the open derivation program for a completed proof. |
| Physicist or reviewer | See exact-GR compatibility, open derivation burden, and blocked claims stated plainly. |
| AI researcher | Understand the agent system as governed research infrastructure, not an autonomous proof oracle. |
| Contributor | Learn which phrases are safe to reuse and which claims require source authority. |
| Site builder | Apply a repeatable copy QA checklist before publishing new public pages. |

## 5. Scope

In scope:

- safe one-sentence pitch;
- approved vocabulary;
- forbidden phrases and implied claims;
- homepage hero guidance;
- audience-specific pitch cards;
- trust and transparency copy block;
- copy QA checklist;
- requirements for public page copy review.

Out of scope for this PRD:

- detailed physics derivations;
- new route implementation;
- visual design implementation;
- source refresh or current-state publication;
- promotion of any scientific claim beyond tracked authority.

## 6. Non-Goals

This PRD must not:

- make the website sound less ambitious by erasing the physics or AI vision;
- make the website sound more certain by claiming completed derivation;
- use vague inspirational copy where claim-status language is required;
- present the AI workflow as autonomous scientific proof;
- treat exact-GR benchmark adoption as first-principles promotion;
- create public copy outside implementation-control approval.

## 7. Website Surfaces

This PRD governs copy requirements for:

- messaging guide;
- homepage hero guidance;
- approved claims list;
- forbidden claims list;
- audience-specific pitch cards;
- trust and transparency block;
- copy QA checklist;
- future homepage, overview, physics, AI workflow, source-authority, current
  frontier, library, and site-builder pages.

## 8. Functional Requirements

1. Provide the baseline safe pitch for first-viewport and overview use.
2. Define approved phrases that can be reused across public pages.
3. Define forbidden phrases that must be blocked during copy review.
4. Require homepage hero copy to state the dual mission, exact-GR status, and
   open derivation burden.
5. Require audience-specific pitch variants for general readers, physicists,
   AI researchers, contributors, and site builders.
6. Require a trust-and-transparency block explaining what the project claims,
   what it does not claim, and how claims are gated.
7. Require every public page to check claims-to-use and claims-to-avoid before
   publication.
8. Require copy to distinguish operational validation from scientific proof.
9. Require source/provenance links to support claims without replacing the
   internal website reading path.

## 9. Non-Functional Requirements

- Precision: Copy must use explicit claim-status language.
- Consistency: Shared pages should use the same approved vocabulary for the
  same concept.
- Reversibility: Copy guidance should remain usable before and after route
  implementation.
- Maintainability: Forbidden phrases should be searchable in review.
- Safety: When uncertain, copy must choose the weaker claim.
- Reader trust: Caution should be presented as part of the project's operating
  discipline.

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

## 11. Content Requirements

Baseline safe pitch:

> The AEther-Flow project is a dual physics and AI research program that
> presents an exact-GR-compatible interpretation of relativity while building a
> governed AI research-agent system for pursuing the still-open derivation from
> deeper substrate structure.

Approved phrases:

- exact-GR benchmark;
- GR-consistent interpretation;
- open first-principles derivation burden;
- source-backed research-control system;
- human-scaffolded AI research-agent workflow;
- governed theoretical research workflow;
- claim-gated derivation program;
- dated current-state snapshot;
- source authority boundary;
- operational validation, not scientific proof.

Forbidden phrases:

- GR has been derived;
- Einstein equations derived from AEther;
- matter coupling solved;
- benchmark promoted from first principles;
- new tested gravity prediction;
- autonomous proof system;
- validators prove the theory;
- AI has solved relativity;
- completed theory of gravity;
- source memory proves the claim.

Audience-specific pitch requirements:

- General reader: emphasize the dual mission and exact-GR-compatible benchmark.
- Physicist: emphasize exact-GR recovery, the open derivation burden, and the
  claim gate.
- AI researcher: emphasize bounded roles, validators, memory discipline, and
  human-gated promotion.
- Contributor: emphasize source authority, provenance, and implementation
  boundaries.
- Site builder: emphasize page-to-source mapping, copy QA, and internal-first
  reader journeys.

## 12. UX and Navigation Requirements

Homepage hero guidance:

- first sentence states dual mission;
- second layer states exact-GR benchmark status and open derivation burden;
- primary cards should route to "The Ontology," "The Exact Benchmark," and
  "The Research-Agent System";
- trust/transparency content should appear early enough that readers do not
  need to hunt for claim limits;
- provenance links should support the journey but not replace internal routes.

Navigation guidance:

- position physics pages and AI workflow pages as co-equal branches;
- keep Source Authority visible as a confidence-building route family;
- route Current Frontier through dated snapshot language;
- use Library and Site Builder surfaces for readers who want source depth or
  implementation context.

## 13. Data, Source, and Provenance Requirements

Copy that makes a public claim must name or link an appropriate source basis.
The implementation should prefer:

- registered TeX sources for technical physics claims;
- research-control records and handoffs for current-state workflow claims;
- registries for source relationships and provenance;
- publication briefs, reviewed explainers, and generated derivatives as reader
  support rather than source authority.

Current-state claims require dated snapshot language and must defer to PRD-09
freshness rules when that PRD is created.

## 14. User Stories

1. As a general reader, I want a one-sentence explanation of the project, so
   that I can understand the thesis before reading technical pages.
2. As a physicist, I want copy to distinguish exact-GR adoption from derivation,
   so that I can evaluate the claim status accurately.
3. As an AI researcher, I want the agent system positioned as governed
   workflow, so that I do not mistake it for autonomous proof generation.
4. As a contributor, I want approved and forbidden phrase lists, so that I can
   draft pages without overclaiming.
5. As a reviewer, I want trust and transparency copy, so that blocked claims are
   visible rather than hidden.
6. As a site builder, I want a copy QA checklist, so that each public page can
   be reviewed consistently.

## 15. Acceptance Criteria

- Homepage hero copy states dual mission, exact-GR status, and open derivation
  burden.
- Promotional copy does not overclaim scientific status.
- Every public-facing page has a claims-to-use and claims-to-avoid check.
- The site positions caution as credibility.
- Approved phrases appear in the copy guidance.
- Forbidden phrases are listed as blocked unless tracked authority changes.
- AI-system copy avoids autonomous-proof framing.
- Validator and handoff language is framed as operational evidence, not
  scientific proof.

## 16. Dependencies

- PRD-00 defines the master mission, source-authority model, IA, and launch
  phases.
- PRD-05 will define source authority, memory, registry, and retrieval
  boundaries in detail.
- PRD-06 will define publication and website-component requirements.
- PRD-01 and PRD-02 depend on this PRD for homepage and physics copy safety.
- PRD-09 depends on this PRD for current-frontier claim-boundary language.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Copy sounds too cautious to be compelling. | Use the safe pitch: ambitious program, exact benchmark, open derivation, governed AI workflow. |
| Copy overstates physics status. | Require forbidden-phrase search and source-authority review before publication. |
| AI workflow is framed as an oracle. | Use "human-scaffolded," "bounded," "claim-gated," and "operational validation." |
| Readers miss the claim boundary. | Put trust/transparency copy near core public journeys, not only in footers. |
| Source links become the primary journey. | Prefer internal route cards and use source links as provenance. |

## 18. Validation Plan

Before implementing public copy from this PRD:

1. Search for forbidden phrases and close variants.
2. Confirm approved phrases are used consistently for recurring concepts.
3. Confirm each public claim has source basis or provenance support.
4. Confirm current-state copy has a dated snapshot and freshness rule.
5. Confirm validators and handoffs are described as operational checks only.
6. Run the relevant website validators for the implementation packet.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: MVP foundation.

This PRD should be created immediately after PRD-00 because it constrains all
public-facing page copy. It should precede PRD-01 homepage requirements,
PRD-02 physics page requirements, PRD-06 publication requirements, and PRD-09
current-frontier requirements.

## 20. Open Questions

1. Should the homepage use the safe pitch verbatim, or should it use a shorter
   first-viewport version with the safe pitch in supporting copy?
2. Should copy QA be enforced by a future validator, a checklist, or both?
3. Which route should own the trust/transparency block: Home, Source Authority,
   Current Frontier, or all three?

These questions do not block this PRD. They should be resolved in follow-on
implementation plans or route-specific PRDs.

## 21. Definition of Done

This PRD is complete when:

- it includes the safe baseline pitch;
- it defines approved and forbidden language;
- it specifies homepage hero guidance;
- it specifies audience-specific positioning;
- it defines trust and transparency copy requirements;
- it includes a copy QA checklist;
- it preserves the source-authority and claim-boundary model from PRD-00;
- it gives future page PRDs a reusable messaging contract.

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].
