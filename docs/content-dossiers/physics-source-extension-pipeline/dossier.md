# Source Extension Pipeline Content Dossier

Status: PG-003 implementation dossier.
Human review status: technical validation passed; maintainer review recommended before release.

## Route and reader job

- Public route: `/project/physics/source-extension-pipeline/`
- Reader job: understand how a source-extension candidate can move through
  proposal, audit, stress, selector, and human-gated precondition review
  without becoming adopted physics.
- Primary audience: general readers, technical readers, and maintainers
  interpreting source-extension status.
- Maintainer owner: website maintainer.
- Review status: technical validation passed; no deployment.
- Source-analysis path: `docs/system-analyses/source-extension-pipeline.md`

## Current page summary

This is a new page. It should start from plain-language workflow context, then
explain pipeline states, forbidden overreads, current internal reading paths,
and provenance. It must not present source-extension readiness as adoption.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `research_control/README.md` | control guide | Authority model, source-extension vocabulary, validator limits, and theoretical continuation context. |
| `github-facing/claim-gates-explainer.md` | generated noncanonical reader surface | Public-safe lifecycle language for proposal, audit, stress, completion, handoff, freeze, and human gate. |
| `research_control/design/gr_derivation_burden_map.md` | control note | Source-extension placement inside derivation burden and target-import boundary. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | registry | Forbidden implications and repeated claim-boundary patterns. |
| `registries/RESEARCH_TASK_REGISTRY.csv` | registry | Examples of selector, constructor, refuter, and Gate Chair packet statuses. |
| `docs/system-analyses/source-extension-pipeline.md` | website-maintained analysis | Maintainer analysis used to shape the public route. |

## Source-derived topic outline

1. Plain-language source-extension summary.
2. Candidate lifecycle: `proposal-only`, audit, `draft/control`, stress,
   selector, human gate.
3. Why readiness and routing do not equal adoption.
4. Static pipeline diagram.
5. Safe and unsafe summaries.
6. Internal reader path and provenance.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| `proposal-only` | A possible source-side idea has been named for bounded work. | Not accepted physics. |
| `draft/control` | Candidate material exists for controlled review. | Not adoption or downstream use. |
| `source-extension` | A controlled category for possible source-side additions or evidence. | Readiness is not adoption. |
| Smuggling audit | A check for hidden target-GR imports or hidden authority imports. | Audit success is not promotion. |
| Refuter stress | A pressure test for fragility, nonuniqueness, or missing primitives. | Stress survival is not proof. |
| Selector | A route-selection packet for the next bounded step. | Not a Gate Chair verdict. |
| Human gate | Protected authority for adoption or promotion decisions. | Cannot be replaced by validator PASS or public prose. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Source-extension work can be useful before adoption.
- A candidate may advance through audit, stress, and selector routing while
  remaining `proposal-only`, `draft/control`, or scoped `source-extension`
  evidence.
- The workflow is `fail-closed`: unclear authority narrows or blocks public
  claims.

### Forbidden implications

- Do not claim source-extension readiness is adoption.
- Do not claim validator PASS proves physics.
- Do not claim stress survival proves a theorem or completes a derivation.
- Do not claim selector output is a Gate Chair verdict.
- Do not claim `MetricData(E)`, `g_eff`, matter coupling, Einstein equations,
  benchmark promotion, or completed derivation unless upstream evidence
  explicitly authorizes it.
- Do not claim future source-extension work is impossible or that the global
  theory is rejected from one scoped failure.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Explain why source extension exists. |
| Plain summary | Yes | Candidate progress is narrower than adoption. |
| Mechanism steps | Yes | Proposal, audit, stress, selector, human gate. |
| Term group | Yes | Required status vocabulary. |
| Source basis | Yes | SourceNotice and provenance section. |
| Boundary block | Yes | No claim laundering. |
| Diagram | Yes | Static pipeline diagram. |
| Equation walkthrough | No | No equations displayed. |
| Safe/unsafe summary | Yes | High overclaim-risk route. |
| Related internal routes | Yes | Physics track, claim gates, current state, source authority. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-source-extension-pipeline/diagrams/source-extension-pipeline.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-source-extension-pipeline.png` |
| Manifest id | `comprehension_physics_source_extension_pipeline` |
| Alt text | Diagram showing proposal-only candidate, audit, stress, selector, human gate, scoped source-extension evidence, and blocked promotion paths. |
| Caption | Static comprehension diagram: source-extension candidates can advance through review without becoming adopted physics. |
| Nearby prose requirement | State that route selection, validation, and stress survival do not authorize adoption. |
| Review status | technical validation passed |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The source-extension pipeline lets AEther Flow test candidate
source-side additions through proposal, audit, stress, selector, and human-gated
review while preserving narrow claim status.

## Unsafe summary

Unsafe summary: A source-extension candidate that passed a validator, survived
stress, or reached selector review has been adopted as physics or unlocks
downstream GR claims.

## New-page audit

- Is a new public page proposed? Yes.
- Existing route that should be used instead: none. `/project/physics/claim-gates/`
  explains the broader claim-control model, but PG-003 needs a focused
  source-extension pipeline page.
- Reason a new route is justified: source-extension status recurs across the
  Distance-to-GR burden and is a distinct reader confusion risk.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [x] Mobile layout and desktop layout were reviewed.
- [x] Human review note is recorded under `docs/quality/`.

## References

The AEther Flow. (n.d.-a). `research_control/README.md` [Research-control guide].

The AEther Flow. (n.d.-b). `github-facing/claim-gates-explainer.md` [Generated noncanonical reader surface].

The AEther Flow. (n.d.-c). `research_control/design/gr_derivation_burden_map.md` [GR derivation burden map].

The AEther Flow. (n.d.-d). `registries/CLAIM_BOUNDARY_REGISTRY.csv` [Claim-boundary registry].

The AEther Flow. (n.d.-e). `registries/RESEARCH_TASK_REGISTRY.csv` [Research-task registry].

The AEther Flow Website. (n.d.). `docs/system-analyses/source-extension-pipeline.md` [Website-maintained system analysis].
