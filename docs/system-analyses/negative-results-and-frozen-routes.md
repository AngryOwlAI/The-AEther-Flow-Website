# Negative Results And Frozen Routes System Analysis

## Purpose

This analysis supports PG-012: creating
`/project/physics/negative-results-and-frozen-routes/` to explain how failed,
blocked, obstructed, or frozen research routes become preserved evidence.

The route should help readers understand negative results without fatalism or
positive spin. A scoped obstruction is not a global theory rejection, and a
frozen route is not hidden success.

## Scope And Authority

This document is website-maintained explanatory analysis. It is not source
authority and does not change research state. The authoritative records remain
the upstream control notes, registries, task artifacts, and human-gated
decisions.

The route may explain obstruction and freeze control as a publication topic. It
cannot issue a freeze, reopen a route, promote a benchmark, reject the global
theory, prove future source-extension impossibility, or convert a negative
result into adoption.

## Evidence Reviewed

- `research_control/design/obstruction_and_freeze_control.md`
  - Defines obstruction records, freeze-control policy, local freeze
    consequences, required `forbidden_overread`, and the distinction between
    local freeze and global rejection.
- `github-facing/claim-gates-explainer.md`
  - Provides public-safe lifecycle language for proposals, audits, stress
    tests, completions, handoffs, freeze labels, and human gates.
- `registries/DISTANCE_TO_GR_LEDGER.csv`
  - Provides current burden statuses, including `finite_toy_metric_response`
    as `frozen negative`, `retain_h` and `gen_h` as blocked by missing
    primitive, `einstein_equations` as not started, and `benchmark_promotion`
    as blocked by missing primitive.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
  - Provides allowed, forbidden, and gate-required wording for scoped
    obstruction, future source-extension impossibility, global theory
    rejection, downstream GR promotion, and process-authority overreads.
- `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex`
  - Concrete finite toy example of a `frozen negative` local route.
- `research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex`
  - Example of fail-closed target-import obstruction labels.
- `src/data/distance_to_gr_snapshot.json`
  - Checked-in website snapshot used by the public route rather than live
    upstream reads during Astro build.
- `src/data/claim_boundary_snapshot.json`
  - Checked-in website snapshot of registry row count and public boundary
    context.

## System Context

AEther Flow treats negative results as routing evidence. A failed construction,
smuggling failure, stress-test obstruction, missing primitive, or local freeze
can prevent repeated work and sharpen future tasks. That is useful only if the
source record names four things:

1. the exact failed object or route;
2. the scope and assumptions;
3. the consequence, such as repair allowed, selector required, route frozen, or
   human gate required; and
4. the forbidden overread.

The `forbidden_overread` field is essential. Without it, a local obstruction
can be inflated into global rejection, or a stress survival can be laundered
into adoption.

## Functionality Or Topic Analysis

### Negative evidence types

- Missing primitive: the current source assumptions lack a named object or
  theorem.
- Scoped obstruction: a specific route failed under stated assumptions.
- Smuggling failure: a construction depends on target context or process
  authority.
- Stress result: a Refuter test identifies fragility, nonuniqueness, or
  underdetermination.
- Local freeze: a named route should not continue under the same burden and
  assumptions without new payload, redesign, freeze review, or human gate.

### Useful because specific

Negative results become useful when they tell a future Director or researcher
what not to repeat. They can justify a selector route, repair candidate,
human-gated decision, or local freeze. They cannot justify broad claims unless
a separate authorized theorem or gate supplies that stronger conclusion.

### Concrete examples

- `finite_toy_metric_response` is `frozen negative`: the explicit-tag-only
  finite toy route failed tag-removal stress and froze locally.
- The old `Resp_lc` selector obstruction remains part of the record even though
  later source-extension data changed the continuation path.
- `retain_h` and `gen_h` are blocked by missing primitive in the checked-in
  Distance-to-GR snapshot.
- `benchmark_promotion` remains blocked by missing primitive.

## Interfaces, Inputs, Outputs

| Interface | Input | Output | Boundary |
| --- | --- | --- | --- |
| Obstruction control note | scopes, consequences, freeze decisions | rule for recording negative evidence | control note is not physics proof. |
| Distance-to-GR ledger | burden rows | public examples of blocked/frozen status | not a progress bar. |
| Claim-boundary registry | forbidden and gate-required claims | overread guardrails | registry rows are not theorem proofs. |
| Task artifacts | construction, audit, stress, completion | concrete examples | artifact scope controls public claim. |
| Public route | source-reviewed explanation | reader understanding | cannot issue verdicts. |

## Risks, Failure Modes, Claim Boundaries

Primary risk: making negative results sound either fatal or decorative. The
route must do neither.

Safe claims:

- Negative results can be rigorous evidence.
- A frozen route can preserve work and prevent unproductive repetition.
- A scoped obstruction can guide the next route.
- Local freeze is not global rejection.
- Fail-closed branches protect downstream claims.

Forbidden implications:

- A scoped obstruction proves the whole theory false.
- A frozen route proves future source-extension impossibility.
- A failed packet authorizes benchmark suspension or promotion.
- Validator, registry, role, handoff, generated derivative, local cache, file
  order, or commit status proves physics.
- Stress survival, audit pass, or selector choice is adoption.

Hard public phrases:

- `scoped obstruction`
- `frozen negative`
- `route_frozen`
- `locally_frozen`
- `forbidden_overread`
- not global theory rejection
- not future source-extension impossibility
- no downstream GR promotion

## Open Questions

- Whether a later dashboard should expose a sanitized table of obstruction
  records after the upstream schema has enough consistent opt-in completions.
- Whether PG-012 should eventually merge with or cross-filter a claim-boundary
  search UI once route count grows.

## Logical Next Step

Create the public route, dossier, static diagram, manifest registrations, and
browser QA for `/project/physics/negative-results-and-frozen-routes/`. The
route should link internally to finite toy models, Distance-to-GR, no-target
import discipline, and claim-boundary explorer.

## References

The AEther Flow. (2026a). *Obstruction and freeze control*
[`research_control/design/obstruction_and_freeze_control.md`].

The AEther Flow. (2026b). *Claim gates explainer*
[`github-facing/claim-gates-explainer.md`].

The AEther Flow. (2026c). *Distance-to-GR ledger*
[`registries/DISTANCE_TO_GR_LEDGER.csv`].

The AEther Flow. (2026d). *Claim boundary registry*
[`registries/CLAIM_BOUNDARY_REGISTRY.csv`].

The AEther Flow. (2026e). *Finite toy metric-response model Refuter stress test*
[`research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex`].

The AEther Flow. (2026f). *No-target-import criterion*
[`research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex`].

The AEther Flow Website. (2026a). *Distance-to-GR snapshot*
[`src/data/distance_to_gr_snapshot.json`].

The AEther Flow Website. (2026b). *Claim-boundary snapshot*
[`src/data/claim_boundary_snapshot.json`].
