# Physics Track Content Dossier

Status: Task 9 physics dossier.
Human review status: pending maintainer review.

## Route and reader job

- Public route: `/project/physics/`
- Reader job: understand the physics route family as a layered status model
  before selecting ontology, benchmark, roadmap, current-state, or claim-gate
  pages.
- Primary audience: readers evaluating AEther Flow physics status.
- Maintainer owner: website maintainer.
- Review status: implemented for mechanical audit; maintainer acceptance still
  required.

## Current page summary

The page already separates ontology, exact-GR benchmark, open burden, and
negative-result control. The remediation adds dossier-backed comprehension
blocks and a static Mermaid-authored diagram to make those separations explicit
before the route grid.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/aether-flow-physics-program-explainer.md` | generated noncanonical reader surface | Five-layer status model, safe/unsafe summary, and source-boundary language. |
| `ontology/aether-and-aether-flow.md` | ontology-adjacent explanatory source | Ontology vocabulary and open derivation boundary. |
| `research_control/design/gr_derivation_burden_map.md` | control note | Required milestone chain and burden status categories. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | registry | Forbidden claim and gate patterns. |

## Source-derived topic outline

1. Physics track as ontology, benchmark, burden, negative-result, and gate
   layers.
2. Internal route choices by reader question.
3. Source authority and claim boundaries.
4. Safe and unsafe summaries.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Exact-GR benchmark | Observable-scale public benchmark remains ordinary GR. | Not a source-side substrate derivation. |
| Derivation burden | Required source-side bridge to metric, coupling, equations, and promotion. | Open until source authority and gates close it. |
| Scoped obstruction | A route-local failure under stated assumptions. | Not global theory rejection. |

## Claim boundaries and forbidden implications

### Claim boundaries

- The page is public orientation only.
- Ontology, benchmark, derivation burden, negative-result records, and gates
  must stay distinct.
- Validator success is bounded repository evidence, not physics proof.

### Forbidden implications

- Do not claim completed GR derivation.
- Do not claim benchmark promotion or Gate Chair closure.
- Do not inflate scoped obstruction into global theory rejection.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Physics track as layered status model. |
| Plain summary | Yes | Conservative public interpretation. |
| Mechanism steps | Yes | Name layer, check source status, preserve open burdens. |
| Term group | Yes | Benchmark, burden, scoped obstruction. |
| Source basis | Optional | Existing SourceNotice handles primary refs. |
| Boundary block | Yes | No derivation, no validator proof. |
| Diagram | Yes | Static status-layer map. |
| Equation walkthrough | No | No equation walkthrough required for this route. |
| Safe/unsafe summary | Yes | High overclaim-risk route. |
| Related internal routes | Yes | Existing route grid and links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-track/diagrams/status-layer-map.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-track-status-map.png` |
| Manifest id | `comprehension_physics_track_status_map` |
| Alt text | Diagram showing the physics track as separate ontology, exact-GR benchmark, derivation burden, negative-result, and human-gate layers. |
| Caption | Static comprehension diagram: the physics track is a layered status model, not a single promoted claim. |
| Nearby prose requirement | State that the diagram is orientation only and cannot promote claims. |
| Review status | pending maintainer review |

## Equation walkthrough contract

No equation walkthrough required for this route. The page does not display or
derive equations.

## Safe summary

Safe summary: AEther Flow is a benchmark-disciplined physics research program
that preserves exact GR operationally while testing whether source-side
substrate structure can earn a derivation.

## Unsafe summary

Unsafe summary: AEther Flow has already derived GR, public explainers certify
benchmark recovery, or a scoped obstruction proves the whole ontology false.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/physics/`.
- Reason a new route is or is not justified: the physics landing page already
  owns this reader job.

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
`github-facing/aether-flow-physics-program-explainer.md` [Generated
noncanonical reader surface].
