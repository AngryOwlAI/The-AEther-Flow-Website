---
prd_id: "PRD-02"
title: "Physics and Mathematical Components"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Physics ontology, exact-GR benchmark, derivation roadmap, mathematical components, and proof boundaries"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-01-high-level-components.md"
  - "PRD-10-website-positioning-guidance.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
  - "PRD-09-current-research-frontier-for-website-use.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-02: Physics and Mathematical Components

## 1. Summary

This PRD defines the website requirements for explaining the physics and
mathematical side of The AEther Flow Project. It covers the AEther /
AEther-flow ontology, exact-GR benchmark, adoption-versus-derivation boundary,
flow-geometry dictionary, GR derivation roadmap, current claim-status tables,
negative-result preservation, and "what remains open" explanations.

The central product rule is that physics pages must be ambitious and precise.
They may explain the project's exact-GR-compatible benchmark and ontology-first
interpretation, but they must not imply that source-side derivation, matter
coupling, Einstein equations, or benchmark promotion are complete.

## 2. Product Purpose

Physics pages need to make the project technically legible without turning
interpretive and roadmap material into proof. A reader should understand:

- what the AEther / AEther-flow ontology proposes;
- what the exact-GR benchmark adopts at the effective level;
- which mathematical structures belong to the benchmark;
- which source-side derivation burdens remain open;
- why negative results and local freezes are useful evidence rather than global
  rejection;
- where to inspect canonical source authority before trusting a technical
  claim.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, or research-workflow authority.

Source basis for implementation should include:

- `ontology/aether-and-aether-flow.md`;
- `ontology/tex/aether_flow_foundations.tex`;
- `ontology/tex/aether_flow_exact_closure_note.tex`;
- `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`;
- `ontology/tex/aether_flow_dynamics.tex`;
- `ontology/tex/aether_flow_relativistic_recovery.tex`;
- `ontology/tex/aether_flow_geometry.tex`;
- `ontology/tex/aether_flow_consistency.tex`;
- `research_control/design/gr_derivation_burden_map.md`;
- `research_control/current_frontier.md`;
- `registries/DISTANCE_TO_GR_LEDGER.csv`;
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`;
- the website positioning, source-authority, high-level, and current-frontier
  PRDs.

Registered TeX sources carry source authority for technical physics claims.
Generated PDFs, HTML explainers, GitHub-facing Markdown, website PRDs, and
local retrieval layers are reader aids unless a higher-authority record says
otherwise.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand the physics idea without imagining a naive ether wind or a completed GR derivation. |
| Physicist or reviewer | Inspect exact-GR benchmark assumptions, mathematical components, and open derivation burdens clearly. |
| AI researcher | See why the physics problem is hard enough to need governed research-agent workflows. |
| Contributor | Know which physics claims require TeX-source verification and which pages are only explanatory. |
| Operator | Distinguish benchmark adoption, source-side evidence, current frontier status, obstruction, and human-gated promotion. |
| Site builder | Build physics pages with claim-status panels, source footers, and conservative mathematical language. |

## 5. Scope

In scope:

- ontology explainer requirements;
- exact-GR benchmark boundary requirements;
- GR derivation roadmap requirements;
- physics glossary requirements;
- flow-geometry visual dictionary requirements;
- adoption-versus-derivation comparison requirements;
- current physics claim-status table requirements;
- "what remains open?" requirements;
- negative-result and local-freeze explanation requirements.

Out of scope:

- changing ontology or TeX sources;
- refreshing current-frontier snapshots;
- updating Distance-to-GR ledgers or claim-boundary registries;
- implementing public routes or generated diagrams;
- promoting any scientific claim;
- deriving new equations or proposing new physics.

## 6. Non-Goals

This PRD must not:

- claim independent low-energy non-GR signatures;
- claim completed matter coupling;
- claim completed Einstein-equation derivation;
- claim completed source-to-metric derivation;
- claim benchmark promotion from first principles;
- treat `g_eff`, `MetricData(E)`, or similar guarded objects as adopted unless
  current source authority says so;
- treat a local obstruction or freeze as global theory rejection;
- make validators, registries, generated explainers, or PRDs scientific proof.

## 7. Website Surfaces

Required surfaces:

- Ontology explainer;
- Exact-GR benchmark boundary explainer;
- GR derivation roadmap;
- Physics glossary;
- Flow-geometry visual dictionary;
- Adoption versus derivation comparison table;
- Current physics claim-status table;
- "What remains open?" section.

Supporting surfaces:

- exact-closure source card;
- one-operative-metric card;
- universal matter-coupling benchmark card;
- flow-geometry `(g, u)` dictionary card;
- Distance-to-GR burden map card;
- blocked-claims panel;
- negative-result and local-freeze panel.

## 8. Functional Requirements

1. Explain AEther, AEther-flow, observed space, S-time, expansion, and gravity
   language as ontology-level concepts.
2. Explain the exact-GR benchmark package, including one operative metric and
   universal matter coupling at the benchmark level.
3. Explain the Einstein-Hilbert effective action as adopted effective benchmark
   structure, not substrate derivation.
4. Explain congruence geometry as a disciplined interpretive dictionary.
5. Explain source-side derivation milestones including source ontology, EqSrc,
   localization, response, `M_src`, `g_eff`, matter coupling, Einstein
   equations, and benchmark promotion.
6. Explain negative-result preservation, obstruction records, and local freeze
   logic.
7. Require every physics page to expose a claim-status panel.
8. Require every physics page to declare canonical source basis and derivative
   status.
9. Require exact-GR pages to separate observer-facing benchmark claims from
   source-side derivation claims.
10. Require current-status physics pages to use dated snapshot and PRD-09
    freshness rules.

## 9. Non-Functional Requirements

- Scientific caution: Pages must use weaker language when source state is
  uncertain or freshness evidence is missing.
- Mathematical clarity: Pages should define symbols, domains, assumptions, and
  status before using equations as public evidence.
- Dimensional discipline: Any future displayed equation should include context
  sufficient to prevent category or unit confusion.
- Source traceability: Technical claims should link to registered TeX sources
  or source-authority explanations.
- Reader comprehension: Physics explanations should proceed from ontology to
  benchmark to derivation roadmap, not from low-level notation first.
- Reversibility: Page requirements should allow future correction if upstream
  source authority changes.

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

Additional physics boundary:

The website may describe exact-GR benchmark adoption as a real effective-level
benchmark. It must not describe that adoption as source-side recovery of GR.

## 11. Content Requirements

The adoption-versus-derivation table must include at least:

| Topic | Adopted effective benchmark | Open source-side derivation |
| --- | --- | --- |
| Metric | One operative Lorentzian metric for observer-facing physics. | Source-to-metric construction or `g_eff` promotion remains guarded. |
| Matter coupling | Universal matter coupling is part of the benchmark package. | Deriving matter coupling from substrate structure remains open. |
| Field equations | Einstein equations hold in the adopted exact-GR benchmark. | Deriving field equations from source-side dynamics remains open. |
| Predictions | Low-energy gravitational predictions remain ordinary GR. | Independent non-GR signatures are not claimed by the active benchmark. |
| Ontology | AEther / AEther-flow supplies an interpretive research ontology. | Ontology must produce source-side laws before derivation claims. |
| Promotion | Benchmark is the current effective target and reversion floor. | First-principles benchmark promotion remains human-gated and blocked until prerequisites close. |

The physics glossary must cover:

- AEther;
- AEther-flow;
- observed space;
- S-time;
- exact-GR benchmark;
- exact closure;
- one operative metric;
- universal matter coupling;
- flow geometry;
- congruence;
- observer rest-space projector;
- expansion, shear, vorticity, and acceleration;
- source-side derivation;
- Distance-to-GR burden;
- local obstruction;
- local freeze.

Required copy fragments:

- "Exact-GR benchmark adoption is not first-principles derivation."
- "The active benchmark inherits GR behavior at observable scale."
- "The ontology is a research ontology, not a completed equation-level
  derivation."
- "Matter coupling, Einstein-equation derivation, and benchmark promotion
  remain guarded downstream burdens."
- "Distance-to-GR is a burden map and status ledger, not a percentage-complete
  meter."

## 12. UX and Navigation Requirements

Physics navigation should:

- begin with a short physics orientation before equations;
- route readers from ontology to exact-GR benchmark to derivation roadmap;
- show adoption-versus-derivation before dense technical claims;
- include source-authority access on every technical page;
- expose blocked claims as normal trust information;
- keep current-status widgets separate from stable explanation unless PRD-09
  freshness requirements are satisfied.

Recommended physics reader path:

| Reader | First path |
| --- | --- |
| General reader | Ontology explainer to exact-GR benchmark boundary to "what remains open." |
| Physicist | Exact-GR benchmark boundary to flow-geometry dictionary to derivation roadmap. |
| AI researcher | Derivation roadmap to obstruction/freeze logic to research-agent workflow. |
| Contributor | Source authority to physics glossary to source map. |
| Site builder | PRD-02 to PRD-05 to PRD-09 before implementing current-status physics pages. |

## 13. Data, Source, and Provenance Requirements

Every physics page should declare:

- canonical source basis;
- equation or concept status;
- claim status;
- claim boundary;
- freshness rule, if current-state data is shown;
- whether the page is explanatory, derivative, current snapshot, or source
  authority;
- source/provenance footer status.

Physics claim-status labels should include:

- adopted benchmark;
- ontology concept;
- interpretive dictionary;
- open derivation burden;
- scoped evidence;
- blocked downstream claim;
- local obstruction;
- local freeze;
- human-gated promotion.

Current frontier, Distance-to-GR, burden-map, and blocked-claim content should
be treated as dated snapshots. Stable physics explanation should be separated
from time-sensitive status reporting.

## 14. User Stories

1. As a general reader, I want ontology language explained without naive ether
   imagery, so that I can understand the concept safely.
2. As a physicist, I want the exact-GR benchmark separated from source-side
   derivation, so that I can evaluate what has been adopted and what remains
   open.
3. As an AI researcher, I want the derivation burden map explained, so that I
   can understand why the agent workflow matters.
4. As a contributor, I want canonical physics source links, so that I can verify
   technical claims before editing pages.
5. As an operator, I want claim-status panels, so that public physics pages do
   not overread current frontier evidence.
6. As a site builder, I want page templates for ontology, benchmark, roadmap,
   glossary, and status tables, so that physics routes can be implemented
   consistently.

## 15. Acceptance Criteria

- Every physics page has a claim-status panel.
- The exact-GR page clearly distinguishes benchmark adoption from derivation.
- The ontology page avoids naive ether-wind or three-dimensional medium
  framing.
- The mathematical roadmap identifies which burdens are upstream and downstream.
- Current status pages are dated snapshots, not permanent scientific claims.
- The physics glossary defines key ontology, benchmark, geometry, and
  derivation terms.
- Adoption-versus-derivation language appears before deep technical claims.
- Pages do not claim matter coupling, Einstein-equation derivation,
  source-to-metric derivation, or benchmark promotion as complete.

## 16. Dependencies

- PRD-00 defines the master information architecture and source-authority
  policy.
- PRD-01 defines first-reader and high-level route requirements.
- PRD-10 defines approved physics positioning and forbidden claims.
- PRD-05 defines canonical source, derivative, registry, memory, and provenance
  requirements.
- PRD-09 will define dated current-frontier and stale-data behavior.
- PRD-11 will define concise source bundles for site builders.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Readers infer completed GR derivation from exact-GR compatibility. | Put adoption-versus-derivation tables before technical deep dives. |
| Ontology language sounds like a mechanical three-dimensional ether. | Require ontology pages to reject ether-wind and observed-space-container framing. |
| Current frontier snippets become stale. | Use dated snapshots and PRD-09 freshness behavior. |
| Mathematical notation implies more authority than the source permits. | Require source basis, equation status, and claim-status labels near equations. |
| Negative results look like global theory rejection. | Explain scoped obstruction and local-freeze semantics. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Check every physics page for claim-status panel and source/provenance footer.
2. Search for forbidden claims: completed derivation, solved matter coupling,
   derived Einstein equations, promoted benchmark, independent low-energy
   non-GR signature, and autonomous proof.
3. Check ontology pages for naive ether-wind, preferred-frame, or
   three-dimensional medium wording.
4. Check exact-GR pages for adoption-versus-derivation separation.
5. Check current-status pages for dated snapshot, source basis, and stale-data
   behavior.
6. Run applicable content, provenance, route, build, browser, and
   implementation-control validators for implementation packets.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: MVP foundation.

This PRD should follow PRD-01 because the high-level story must exist before
deep physics pages. It should precede PRD-09 implementation use because current
frontier pages need physics claim-status discipline before publishing live or
dated status material.

## 20. Open Questions

1. Should the first physics implementation include a full derivation-roadmap
   page, or should it start with ontology plus exact-GR benchmark boundary?
2. Which equations should be rendered directly on the website, and which should
   remain linked through TeX/PDF source materials?
3. Should the flow-geometry dictionary be visual, tabular, or both?
4. Should current claim-status tables live in physics pages, current-frontier
   pages, or both with different freshness rules?

These questions do not block this PRD. They should be resolved in PRD-09,
PRD-11, or follow-on implementation plans.

## 21. Definition of Done

This PRD is complete when:

- it defines ontology, exact-GR benchmark, derivation-roadmap, glossary,
  flow-geometry, claim-status, and open-burden requirements;
- it separates adopted effective benchmark structure from source-side
  derivation;
- it requires claim-status panels and source/provenance notes for physics
  pages;
- it prevents completed matter-coupling, Einstein-equation derivation,
  source-to-metric derivation, and benchmark-promotion overclaims;
- it gives future physics pages a testable requirements contract.

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].

The AEther Flow Website. (2026). *High-Level Components* [Product requirements
document].

The AEther Flow Website. (2026). *Website Positioning Guidance* [Product
requirements document].

The AEther Flow Website. (2026). *Memory, Registry, and Retrieval Components*
[Product requirements document].
