# Exact-GR Benchmark Versus Derivation System Analysis

## Purpose

This analysis supports PG-008: rewriting
`/project/physics/exact-gr-benchmark/` so public readers can distinguish
benchmark compatibility, first-principles derivation, and benchmark promotion.

The decision it supports is narrow: the website may explain the exact-GR
benchmark boundary if it does not claim a completed source-side derivation or
protected benchmark promotion.

## Scope And Authority

This document is website-maintained explanatory analysis. It is not source
authority and cannot derive GR, construct `g_eff`, adopt matter coupling,
derive Einstein equations, promote a benchmark, issue a Gate Chair verdict, or
turn generated explainers into physics evidence.

The upstream source basis was inspected at commit
`4d249ba24ead51445e496a74b2f6072149bc7609`.

## Evidence Reviewed

- `github-facing/exact-gr-benchmark-boundary-explainer.md`
  - Generated noncanonical reader explainer for the benchmark boundary.
- `research_control/design/gr_derivation_burden_map.md`
  - Control note separating source ontology, localization, response, `M_src`,
    `g_eff`, matter coupling, Einstein equations, and benchmark promotion.
- `registries/DISTANCE_TO_GR_LEDGER.csv`
  - Current burden ledger for source-to-GR status.
- `registries/TEX_SOURCE_REGISTRY.csv`
  - Registered TeX source status for ontology and benchmark materials.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
  - Forbidden benchmark-promotion and completed-derivation overreads.
- `research_control/program_state.yaml`
  - Current active task and latest handoff context.
- `research_control/handoffs/handoff-0280.yaml`
  - Latest current-state handoff showing downstream GR boundaries remain
    blocked.
- `ImplementationPlans/sitewide_page_revamp_task_packets.md`
  - PG-008 implementation and validation requirements.

## System Context

The exact-GR benchmark is a conservative target and operating boundary. It
says observable-scale behavior is read against ordinary GR: one operative
Lorentzian metric, universal matter coupling, ordinary causal structure, and
no public empirical-deviation claim at the benchmark boundary.

That is different from deriving the benchmark from AEther / AEther-flow source
ontology. Derivation would require source-side construction across the burden
chain: source ontology, source equivalence, localization, response,
`M_src`, `g_eff`, matter coupling, Einstein equations, and benchmark
promotion. Those burden labels are not interchangeable.

## Claim-State Distinctions

Use these distinctions on the public page:

- Matching or using a benchmark means the project keeps ordinary GR as the
  public observable-scale reference.
- Compatibility means ontology language can sit beside the benchmark without
  contradiction.
- Derivation means source-side mathematics forces the benchmark without
  importing the target result by hand.
- Promotion means a protected source-authority change has accepted the result
  through the required gate.

The current public page may explain the first two and describe the last two as
open or protected. It may not imply the last two are complete.

## Specialist Source Layer

The specialist layer should identify:

- `research_control/design/gr_derivation_burden_map.md` as the burden map.
- `registries/DISTANCE_TO_GR_LEDGER.csv` as the current burden ledger.
- `registries/TEX_SOURCE_REGISTRY.csv` as registered TeX source status.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv` as overread and promotion control.
- Current-state handoff and program state as routing context.

## Forbidden Overreads

The route must not imply:

- completed first-principles GR derivation;
- derived `g_eff`;
- universal matter coupling derivation;
- Einstein equations derivation;
- benchmark promotion;
- Gate Chair approval;
- empirical deviation from ordinary GR at the benchmark boundary; or
- generated pages, PDFs, wiki notes, validators, handoffs, or registry
  metadata as scientific proof.

## Recommendation

The logical next step is to rewrite the page as a public-first contrast:

1. "Matching the benchmark" means ordinary GR remains the observable-scale
   reference.
2. "Deriving the benchmark" means future source mathematics must discharge the
   burden chain.
3. "Promoting the benchmark" means protected upstream approval, not public
   prose.

An improvement will be a later matrix that links each burden row to the
Distance-to-GR dashboard, but the first rewrite should stay readable and
source-boundary safe.

## References

The AEther Flow. (n.d.-a). *Exact-GR benchmark boundary explainer*
[`github-facing/exact-gr-benchmark-boundary-explainer.md`].

The AEther Flow. (n.d.-b). *GR derivation burden map*
[`research_control/design/gr_derivation_burden_map.md`].

The AEther Flow. (n.d.-c). *Distance-to-GR ledger*
[`registries/DISTANCE_TO_GR_LEDGER.csv`].

The AEther Flow. (n.d.-d). *TeX source registry*
[`registries/TEX_SOURCE_REGISTRY.csv`].

The AEther Flow. (n.d.-e). *Claim boundary registry*
[`registries/CLAIM_BOUNDARY_REGISTRY.csv`].

The AEther Flow. (n.d.-f). *Program state*
[`research_control/program_state.yaml`].

The AEther Flow. (n.d.-g). *Handoff 0280 structured record*
[`research_control/handoffs/handoff-0280.yaml`].

The AEther Flow Website. (2026). *Sitewide page revamp task packets*
[`ImplementationPlans/sitewide_page_revamp_task_packets.md`].
