# AEther-Flow Ontology Vocabulary System Analysis

## Purpose

This analysis supports PG-007: rewriting
`/project/physics/ontology/` as a public-first ontology vocabulary and
source-boundary page. The page should help non-specialists understand the
project's core vocabulary while preserving the distinction between ontology,
mathematical derivation, benchmark compatibility, empirical prediction, and
registered source authority.

## Scope And Authority

This document is website-maintained explanatory analysis. It is not source
authority and cannot promote ontology, edit registered TeX, adopt a source
law, derive `MetricData(E)`, define or adopt `g_eff`, derive matter coupling,
derive Einstein equations, promote a benchmark, or complete the GR derivation.

The source basis was inspected at upstream commit
`4d249ba24ead51445e496a74b2f6072149bc7609`. Registered TeX files under
`ontology/tex/` carry scientific source authority for ontology and benchmark
material. PDFs are generated human-readable derivatives. Markdown in
`ontology/` may explain context but does not supersede registered TeX.

## Evidence Reviewed

- `github-facing/aether-flow-ontology-explainer.md`
  - Generated noncanonical public ontology explainer.
- `ontology/aether-and-aether-flow.md`
  - Ontology-adjacent explanatory Markdown defining the public vocabulary.
- `ontology/README.md`
  - Folder authority boundary: TeX authority, PDF derivatives, explanatory
    Markdown, and live versus legacy lane.
- `registries/TEX_SOURCE_REGISTRY.csv`
  - Registered ontology TeX source metadata and canonical/legacy status.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
  - Claim-boundary guardrails against promotion and derivation overreads.
- `ImplementationPlans/sitewide_page_revamp_task_packets.md`
  - PG-007 implementation and validation requirements.

## System Context

The ontology lane answers a "what is the model about?" question. It names
`AEther`, `AEther-flow`, observed three-dimensional space, `S-time`, observed
expansion, and gravity-as-reorganization language. The source note explicitly
frames this as ontology, not a completed first-principles substrate derivation
of gravity.

The route must therefore start with public vocabulary and then move to
specialist source status. That ordering matters. If source status appears
first, general readers can miss the basic terms. If vocabulary appears without
source status, readers can overread conceptual language as accepted physics.

## Vocabulary Layer

Safe public definitions:

- `AEther`: the proposed deeper four-dimensional substrate of reality.
- `AEther-flow`: intrinsic ordered motion of that substrate.
- Observed three-dimensional space: the local observer-accessible slice or
  appearance of the deeper substrate.
- `S-time`: the experienced order of change involving matter, light, and
  `AEther-flow`.
- Observed expansion: the three-dimensional appearance of deeper
  four-dimensional ordered motion.
- Gravity-as-reorganization: a heuristic ontology interpretation in which
  matter locally reorganizes surrounding `AEther-flow`.

Boundary: none of these definitions, by themselves, supplies the equation-level
observer-response law, same-metric matter theorem, nonmetric mode control, or
Einsteinian closure needed for stronger derivation claims.

## Specialist Source Layer

The specialist layer should name the source basis without making the public
page a source substitute:

- `ontology/tex/*.tex` files are current canonical ontology package sources in
  `registries/TEX_SOURCE_REGISTRY.csv`.
- `ontology/pdfs/*.pdf` files are generated human-readable derivatives.
- `legacy_ontology/` is archival and noncanonical.
- `ontology/aether-and-aether-flow.md` is explanatory Markdown.
- Generated GitHub-facing explainers are noncanonical reader surfaces.
- Claim-boundary registry rows prevent public summaries, validators, files,
  derivatives, or source metadata from becoming physics proof.

## Page Contract

The rewritten route should:

- Put public vocabulary first.
- Include observed expansion as a first-class term.
- Treat gravity-as-reorganization as heuristic ontology language, not an
  equation-level result.
- Put source status after the public vocabulary.
- Cross-link internally to ontology documents, exact-GR benchmark,
  Distance-to-GR, current state, and claim-boundary pages.
- Preserve the statement that ontology vocabulary is not a completed GR
  derivation.

The rewritten route should not:

- Present AEther as an ordinary three-dimensional medium.
- Present AEther-flow as a detectable wind or fluid in observed space.
- Treat compatibility with exact GR as a first-principles derivation.
- Claim empirical predictions from ontology vocabulary alone.
- Treat PDFs as independent authority over registered TeX.

## Risks

- Public simplification could make ontology sound like accepted scientific
  theory rather than current project ontology.
- Technical source-status language could overwhelm first-time readers.
- Exact-closure or benchmark terms could be read as derivation closure unless
  the page repeats the open-derivation boundary.

## Recommendation

The logical next step is a two-layer route:

1. Public vocabulary cards: AEther, AEther-flow, observed space, `S-time`,
   observed expansion, gravity-as-reorganization.
2. Source status cards: registered TeX, PDF derivatives, explanatory Markdown,
   generated derivatives, claim boundaries, and open derivation burden.

An improvement will be a later side-by-side "term / common overread / safe
phrasing" table, but the first rewrite should stay compact and readable.

## References

The AEther Flow. (n.d.-a). *AEther-flow ontology explainer*
[`github-facing/aether-flow-ontology-explainer.md`].

The AEther Flow. (n.d.-b). *Æther and Æther-flow*
[`ontology/aether-and-aether-flow.md`].

The AEther Flow. (n.d.-c). *Ontology sources and derivatives*
[`ontology/README.md`].

The AEther Flow. (n.d.-d). *TeX source registry*
[`registries/TEX_SOURCE_REGISTRY.csv`].

The AEther Flow. (n.d.-e). *Claim boundary registry*
[`registries/CLAIM_BOUNDARY_REGISTRY.csv`].

The AEther Flow Website. (2026). *Sitewide page revamp task packets*
[`ImplementationPlans/sitewide_page_revamp_task_packets.md`].
