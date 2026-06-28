# Negative Results And Frozen Routes Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/physics/negative-results-and-frozen-routes/`
- Reader job: Understand how negative results, scoped obstructions, and frozen
  routes become preserved evidence without becoming global rejection or hidden
  success.
- Primary audience: general public readers, physicists, mathematicians, and
  readers inspecting claim discipline.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The page explains obstruction and freeze records as routing evidence. It pairs
plain-language examples with Distance-to-GR statuses and claim-boundary rules,
then separates safe and unsafe summaries.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `research_control/design/obstruction_and_freeze_control.md` | upstream control note | Obstruction scopes, consequences, freeze-control policy, and `forbidden_overread` requirement. |
| `github-facing/claim-gates-explainer.md` | generated noncanonical explainer | Public-safe lifecycle and negative-result wording. |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | upstream registry | Burden examples for frozen, blocked, and not-started rows. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | upstream registry | Forbidden global-rejection and downstream-promotion overreads. |
| `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex` | upstream task artifact | Concrete `frozen negative` finite toy example. |
| `research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex` | upstream task artifact | Fail-closed obstruction label example. |
| `src/data/distance_to_gr_snapshot.json` | website snapshot | Checked-in row data used by the route. |
| `src/data/claim_boundary_snapshot.json` | website snapshot | Checked-in claim-boundary context. |

## Source-derived topic outline

1. Negative results as source-backed records, not failure theater.
2. Obstruction record anatomy: failed object, scope, consequence, and
   `forbidden_overread`.
3. Freeze decisions: `route_frozen` and `locally_frozen` as local route-control
   statuses.
4. Examples from Distance-to-GR: finite toy frozen negative, missing primitives,
   not-started equations, blocked benchmark promotion.
5. Claim boundaries: not global theory rejection, not future source-extension
   impossibility, no downstream GR promotion.
6. Internal reading path.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| negative result | A source-backed record that a route did not meet its burden. | Not project failure. |
| scoped obstruction | A failure under stated assumptions and source tuple. | Not global no-go theorem. |
| `frozen negative` | A local route status preserving a failed tested path. | Not future impossibility. |
| `route_frozen` | Consequence meaning the named route should stop under current assumptions. | Does not reject the whole theory. |
| `locally_frozen` | Freeze decision for a named local route. | Does not authorize downstream promotion. |
| `forbidden_overread` | Required field stating what the obstruction must not be read to mean. | Prevents laundering local failure into global claim. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Negative results can be rigorous evidence.
- Freeze labels preserve scope and prevent repetition.
- Local freeze is route control, not global theory control.
- Claim-boundary registry language controls public summaries.

### Forbidden implications

- A scoped obstruction proves the whole theory false.
- A frozen route proves future source-extension impossibility.
- A failure authorizes benchmark promotion or suspension.
- Validator, registry, role, handoff, generated derivative, local cache, file
  order, commit status, or recency proves physics.
- Audit pass, stress survival, or selector choice is adoption.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Explain why negative evidence is useful and limited. |
| Plain summary | yes | Preserved evidence, not failure theater. |
| Mechanism steps | yes | Failed object, scope, consequence, forbidden overread, next route. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Freeze-control note, claim-gates explainer, ledgers, registries, examples. |
| Boundary block | yes | Not global rejection; not future impossibility; no downstream promotion. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required for this route. |
| Safe/unsafe summary | yes | High-risk overread prevention. |
| Related internal routes | yes | Finite toy models, Distance-to-GR, claim boundaries, no-target import. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-negative-results-and-frozen-routes/diagrams/negative-results-freeze-flow.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-negative-results-and-frozen-routes.png` |
| Manifest id | `comprehension_physics_negative_results_frozen_routes` |
| Alt text | Diagram showing a failed route becoming a scoped obstruction, obstruction receipt, local freeze or selector route, and preserved evidence while global rejection and downstream promotion remain blocked. |
| Caption | Static comprehension diagram: negative results become useful only when scope, consequence, and forbidden overread remain visible. |
| Nearby prose requirement | State that the diagram is a reader aid, not source authority or a global no-go theorem. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Negative results and frozen routes preserve rigorous evidence
when they name the failed object, scope, consequence, `forbidden_overread`, and
next route. A `frozen negative` result can prevent repeated work while
preserving no downstream GR promotion.

## Unsafe summary

Unsafe summary: A scoped obstruction proves global theory rejection, a frozen
route proves future source-extension impossibility, or negative evidence can
be hidden behind positive framing.

## New-page audit

- Is a new public page proposed? Yes.
- New route: `/project/physics/negative-results-and-frozen-routes/`.
- Reason a new route is justified: PG-012 requires a dedicated explanation of
  negative results as preserved evidence. Existing claim-gates and finite-toy
  pages cover parts of the idea but do not provide a full reader path through
  obstruction anatomy and freeze-control discipline.

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

- The AEther Flow. (2026a). `research_control/design/obstruction_and_freeze_control.md`.
- The AEther Flow. (2026b). `github-facing/claim-gates-explainer.md`.
- The AEther Flow. (2026c). `registries/DISTANCE_TO_GR_LEDGER.csv`.
- The AEther Flow. (2026d). `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- The AEther Flow. (2026e). `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex`.
- The AEther Flow. (2026f). `research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex`.
- The AEther Flow Website. (2026a). `src/data/distance_to_gr_snapshot.json`.
- The AEther Flow Website. (2026b). `src/data/claim_boundary_snapshot.json`.
- The AEther Flow Website. (2026c). `docs/system-analyses/negative-results-and-frozen-routes.md`.
