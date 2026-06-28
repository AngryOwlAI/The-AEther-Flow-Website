# Claim Boundary Explorer System Analysis

## Purpose

This analysis defines a public route for inspecting AEther Flow claim-boundary
behavior without replacing the upstream registry. It supports PG-005:
`/project/source-authority/claim-boundary-explorer/` may be implemented if it
shows allowed, forbidden, and gate-required language as registry-derived
orientation, not as certification or scientific promotion.

## Scope And Authority

This document is website-maintained explanatory analysis. It is not source
authority. It cannot create a claim boundary, edit the upstream registry,
authorize a Gate Chair verdict, promote ontology, adopt a source law, adopt
`MetricData(E)`, change `g_eff` scope, adopt a coupling law, derive matter
coupling, import stress-energy semantics, derive Einstein equations, promote a
benchmark, or complete a derivation.

The upstream source repository was inspected at commit
`4d249ba24ead51445e496a74b2f6072149bc7609`. The claim-boundary registry
contained 416 active rows. The current active task was `RT-20260614-247`, and
the latest handoff was `handoff-0280`.

## Evidence Reviewed

- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
  - Source registry for claim-boundary rows, including allowed claims,
    forbidden claims, gate requirements, scope, status, and authority-source
    paths.
- `research_control/program_state.yaml`
  - Current active task, current status, latest handoff, and next recommended
    action.
- `research_control/handoffs/handoff-0280.yaml`
  - Latest structured handoff state.
- `research_control/handoffs/handoff-0280.md`
  - Latest public-readable handoff summary and claim-boundary language.
- `research_control/README.md`
  - Research-control source authority and bounded packet rules.
- `github-facing/source-authority-explainer.md`
  - Generated noncanonical reader explanation of source authority.
- `github-facing/claim-gates-explainer.md`
  - Generated noncanonical reader explanation of claim gates and forbidden
    promotion.
- `ImplementationPlans/sitewide_page_revamp_task_packets.md`
  - PG-005 route goal, constraints, acceptance criteria, and validation plan.

## System Context

The claim-boundary registry is a control surface. It names what a task, packet,
or project surface may claim; what it must not imply; and what protected gate
would be required for stronger statements. It is especially important in this
project because many intermediate artifacts are useful without being adopted
physics. A selector result, stress test, validator pass, handoff, or public
summary can be meaningful while still being narrower than source-law adoption,
matter coupling, equations, benchmark promotion, or derivation closure.

The explorer route should therefore answer a reader question:

> "What wording is allowed, what wording is forbidden, and what kind of
> stronger statement would require a gate?"

It should not answer a different question:

> "Has the gate passed, or is the scientific claim now accepted?"

Insufficient data to conclude any protected scientific promotion from the
registry alone. The registry records boundaries; it does not discharge the
burdens it references.

## Functionality Or Topic Analysis

The explorer can use a checked-in JSON snapshot generated from upstream source
state. The generator should be deterministic, fail on dirty upstream state by
default, and reject local absolute path leakage. The route can then display:

1. Snapshot metadata: upstream commit, active task, latest handoff, registry
   row count, and status counts.
2. Allowed, forbidden, and gate-required examples from the current active task
   row.
3. Recurring forbidden phrases such as benchmark promotion, completed
   derivation claim, global theory rejection, `MetricData(E)` adoption, and
   `g_eff` adoption or scope change.
4. Representative recent rows, with their authority-source path shown as a
   repository-relative path.
5. Pinned source-provenance links, clearly separated from the primary internal
   reading path.

This creates a useful public model without pretending that the public page is
interactive source authority. The page should be described as a source-pinned
explorer, not a certification UI.

## Claim Boundaries

Allowed public wording:

- The registry records allowed, forbidden, and gate-required phrases for
  source-scoped work.
- The current active-task row permits only a narrow selector-to-Gate-Chair
  evidence-status/precondition review path.
- The registry repeatedly blocks overreads that would treat generated
  derivatives, validators, roles, handoffs, approvals, cache hits, file order,
  or commit status as proof.

Forbidden public wording:

- The explorer creates or edits claim boundaries.
- The registry itself proves physics claims.
- A boundary row is a Gate Chair verdict.
- Gate readiness is adoption.
- A validator or public page proves `MetricData(E)`, `g_eff`, matter coupling,
  Einstein equations, benchmark promotion, or completed derivation.
- A scoped obstruction is a global rejection of the theory.

## Page Contract

The page should:

- Use `/project/source-authority/claim-boundary-explorer/`.
- Link internally from `/project/source-authority/` and
  `/project/physics/claim-gates/`.
- Import `src/data/claim_boundary_snapshot.json`, not the upstream CSV at build
  time.
- Show the source snapshot date and upstream commit.
- Use internal website routes for the primary reader journey and pinned GitHub
  URLs as provenance.
- Avoid local absolute paths in public output.

The page should not:

- Display itself as legal review, scientific certification, approval, or
  Gate Chair execution.
- Claim that every registry row has been manually reviewed for public
  exposition beyond the checked source snapshot.
- Convert repeated forbidden phrases into a theorem that future work is
  impossible.

## Implementation Recommendation

The logical next step is to implement the route with a small static snapshot
generator and a bounded UI:

- A metadata dossier for source commit, row count, active task, and latest
  handoff.
- Three example cards for allowed, forbidden, and gate-required wording.
- Two phrase rails for recurring forbidden and gate-required language.
- A recent-row section showing representative active rows.
- A provenance section using pinned upstream links.

An improvement will be a later maintainer-facing filter UI backed by the same
snapshot. That should be deferred until the static route passes validation and
reader review.

## Limitations

- The page reflects a checked-in snapshot. It is not live source state.
- Phrase frequency is descriptive. A high count does not imply greater
  scientific importance.
- The route can help readers avoid overclaims, but it cannot decide whether a
  future Gate Chair packet is valid.

## References

The AEther Flow. (n.d.-a). *Claim boundary registry*
[`registries/CLAIM_BOUNDARY_REGISTRY.csv`].

The AEther Flow. (n.d.-b). *Program state*
[`research_control/program_state.yaml`].

The AEther Flow. (n.d.-c). *Handoff 0280 structured record*
[`research_control/handoffs/handoff-0280.yaml`].

The AEther Flow. (n.d.-d). *Handoff 0280 narrative record*
[`research_control/handoffs/handoff-0280.md`].

The AEther Flow. (n.d.-e). *Research control README*
[`research_control/README.md`].

The AEther Flow. (n.d.-f). *Source authority explainer*
[`github-facing/source-authority-explainer.md`].

The AEther Flow. (n.d.-g). *Claim gates explainer*
[`github-facing/claim-gates-explainer.md`].

The AEther Flow Website. (2026). *Sitewide page revamp task packets*
[`ImplementationPlans/sitewide_page_revamp_task_packets.md`].
