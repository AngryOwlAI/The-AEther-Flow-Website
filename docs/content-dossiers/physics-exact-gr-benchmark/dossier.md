# Exact-GR Benchmark Content Dossier

Status: Task 9 physics dossier.
Human review status: pending maintainer review.

## Route and reader job

- Public route: `/project/physics/exact-gr-benchmark/`
- Reader job: keep benchmark adoption, ontology compatibility, derivation, and
  benchmark promotion separate.
- Primary audience: readers evaluating exact-GR claims.
- Maintainer owner: website maintainer.
- Review status: implemented for mechanical audit; maintainer acceptance still
  required.

## Current page summary

The page already states the conservative exact-GR benchmark boundary. The
remediation adds a static ladder diagram and safe/unsafe comprehension blocks
so readers do not treat benchmark compatibility as derivation.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/exact-gr-benchmark-boundary-explainer.md` | generated noncanonical reader surface | Benchmark matrix, forbidden conclusions, and safe summary. |
| `registries/TEX_SOURCE_REGISTRY.csv` | registry | Registered TeX status and canonical/derivative distinctions. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | registry | Forbidden benchmark-promotion claims. |
| `research_control/design/gr_derivation_burden_map.md` | control note | Source-side derivation burden chain. |

## Source-derived topic outline

1. Explain ordinary-GR observable-scale benchmark.
2. Separate adoption, compatibility, derivation, and promotion.
3. State forbidden conclusions.
4. Provide safe and unsafe summary.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Adoption | Ordinary GR behavior used as benchmark. | Not source derivation. |
| Compatibility | Ontology held beside benchmark. | Weaker than derivation. |
| Promotion | Protected source-authority change. | Generated pages cannot issue it. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Observable-scale behavior remains ordinary GR.
- Substrate derivation remains open.
- Benchmark promotion remains gated.

### Forbidden implications

- Do not claim g_eff, matter coupling, or Einstein equations are derived.
- Do not claim empirical deviation from ordinary GR at benchmark boundary.
- Do not make public pages, PDFs, or generated derivatives scientific
  authority.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Benchmark boundary page. |
| Plain summary | Yes | Conservative benchmark answer. |
| Mechanism steps | Yes | Read answer, avoid derivation inference, reserve gates. |
| Term group | Yes | Adoption, compatibility, promotion. |
| Source basis | Optional | Existing SourceNotice covers refs. |
| Boundary block | Yes | No empirical deviation, no source-to-metric claim. |
| Diagram | Yes | Static boundary ladder. |
| Equation walkthrough | No | No equation walkthrough required for this route. |
| Safe/unsafe summary | Yes | High overclaim-risk route. |
| Related internal routes | Yes | Existing links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-exact-gr-benchmark/diagrams/benchmark-boundary-ladder.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-benchmark-boundary-ladder.png` |
| Manifest id | `comprehension_physics_benchmark_boundary_ladder` |
| Alt text | Diagram showing benchmark adoption, ontology compatibility, source-side derivation, and human-gated benchmark promotion as separate claim states. |
| Caption | Static comprehension diagram: benchmark adoption is not the same as derivation or promotion. |
| Nearby prose requirement | State that public pages are boundary maps, not proof. |
| Review status | pending maintainer review |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: AEther Flow keeps ordinary GR as an exact operational benchmark
while the substrate derivation remains open and claim-gated.

## Unsafe summary

Unsafe summary: The public page, ontology note, or a generated derivative
proves GR from AEther-flow.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead:
  `/project/physics/exact-gr-benchmark/`.
- Reason a new route is or is not justified: existing route owns benchmark
  boundary explanation.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [ ] Mobile layout and desktop layout were reviewed.
- [ ] Human review note is recorded under `docs/quality/`.

## References

AEther-Flow Project. (2026).
`github-facing/exact-gr-benchmark-boundary-explainer.md` [Generated
noncanonical reader surface].
