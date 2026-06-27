# GR Derivation Roadmap Content Dossier

Status: Task 9 physics dossier.
Human review status: pending maintainer review.

## Route and reader job

- Public route: `/project/physics/gr-derivation-roadmap/`
- Reader job: understand the roadmap as burden tracking rather than proof that
  burdens are discharged.
- Primary audience: readers evaluating derivation progress.
- Maintainer owner: website maintainer.
- Review status: implemented for mechanical audit; maintainer acceptance still
  required.

## Current page summary

The page already explains the burden chain and downstream blocks. The
remediation adds a static burden-ladder diagram and explicit safe/unsafe
summary blocks.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/gr-derivation-roadmap-explainer.md` | generated noncanonical reader surface | Milestone ladder, status terms, future AgentJob fields, freeze criteria, and safe/unsafe summary. |
| `research_control/design/gr_derivation_burden_map.md` | control note | Required milestone chain and future job contract. |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | registry | Persistent burden rows. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | registry | Forbidden derivation and promotion claims. |

## Source-derived topic outline

1. Roadmap as dependency map.
2. Burden rows and status terms.
3. Future physics job fields and payload rule.
4. Freeze criteria and validator limits.
5. Safe and unsafe summary.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Distance-to-GR ledger | Persistent control ledger for burden rows. | Not independent physics proof. |
| Frozen negative | Route should not be repeated without new payload or redesign. | Not global ontology rejection. |
| Mathematical payload | Source-side artifact named by completion. | Naming does not imply adoption. |

## Claim boundaries and forbidden implications

### Claim boundaries

- The roadmap names obligations and status.
- Each downstream burden needs its own source evidence and gate status.
- Validators cannot prove physics results.

### Forbidden implications

- Do not claim M_src or g_eff adoption from the roadmap.
- Do not infer matter coupling or Einstein equations.
- Do not claim benchmark promotion or completed derivation.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Roadmap as burden tracking. |
| Plain summary | Yes | Burdens are named, not discharged. |
| Mechanism steps | Yes | Locate row, check payload/gate, keep downstream blocked. |
| Term group | Yes | Ledger, frozen negative, payload. |
| Source basis | Optional | SourceNotice covers primary refs. |
| Boundary block | Yes | No g_eff adoption, no downstream GR. |
| Diagram | Yes | Static burden ladder. |
| Equation walkthrough | No | No equation walkthrough required for this route. |
| Safe/unsafe summary | Yes | High derivation-overclaim risk. |
| Related internal routes | Yes | Existing links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-gr-derivation-roadmap/diagrams/burden-ladder.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-roadmap-burden-ladder.png` |
| Manifest id | `comprehension_physics_roadmap_burden_ladder` |
| Alt text | Diagram showing the GR derivation roadmap as a burden ladder from source ontology through g_eff, matter coupling, Einstein equations, and benchmark promotion. |
| Caption | Static comprehension diagram: every derivation milestone needs its own evidence and boundary. |
| Nearby prose requirement | State that the roadmap is not evidentiary shortcut. |
| Review status | pending maintainer review |

## Equation walkthrough contract

No equation walkthrough required for this route. The route names objects and
statuses but does not display or derive equations.

## Safe summary

Safe summary: The GR derivation roadmap tracks separate source ontology,
localization, response, manifold, metric, matter-coupling, equation,
finite-toy, and benchmark-promotion burdens while preserving draft/control and
human-gated boundaries.

## Unsafe summary

Unsafe summary: AEther Flow has derived GR, M_src or g_eff is adopted,
validator passes are physics evidence, or a scoped freeze label proves the
whole ontology false.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead:
  `/project/physics/gr-derivation-roadmap/`.
- Reason a new route is or is not justified: existing route owns roadmap
  explanation.

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
`github-facing/gr-derivation-roadmap-explainer.md` [Generated noncanonical
reader surface].
