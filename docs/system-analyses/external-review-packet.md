# External Reviewer Packet

Status: PG-026 system analysis.
Quality gate: pass with human review pending.
Date: 2026-06-28.

## Question

How should `/resources/reviewer-packet/` orient an external reviewer to what
is claimed, what is not claimed, and where to inspect sources without
presenting the website as scientific authority or external validation?

## Assumptions and constraints

- PG-001 current state, PG-002 Distance-to-GR, PG-005 claim
  boundary/source authority, PG-022 ontology document reading guide, and
  PG-025 specialist guided starts exist and passed their local browser QA.
- The reviewer packet is reviewer-oriented public material with
  `human review pending` status.
- The packet must state claim boundaries before source inspection paths.
- The packet must not add scientific viability claims, peer-review claims,
  external validation claims, or completed-derivation claims.
- Source links remain provenance; internal website routes are the primary
  reading path.

## Source review

Reviewed website surfaces:

- `/project/source-authority/`: source authority and generated-derivative
  boundary.
- `/project/source-authority/claim-boundary-explorer/`: allowed, forbidden,
  and gate-required wording.
- `/project/physics/current-state/`: checked-in current-state snapshot.
- `/project/physics/distance-to-gr/`: burden ledger dashboard.
- `/resources/documents/`: ontology document reading guide and TeX/PDF
  authority boundary.
- `/resources/guided-starts/`: specialist prerequisite paths.
- `/project/physics/exact-gr-benchmark/`: benchmark versus derivation
  boundary.
- `/project/physics/gr-derivation-roadmap/`: open derivation burden structure.
- `/project/operations/validator-operator-workflow/`: validator PASS limits.
- `/project/source-authority/publication-and-provenance-system/`: publication
  provenance and hash boundaries.

Reviewed source-backed data:

- `src/data/physics_current_state_snapshot.json` reports active task
  `RT-20260614-248`, latest handoff `handoff-0281`, and the current website
  snapshot status
  `recovery_bridge_candidate_accepted_scoped_source_extension_evidence_only_no_adoption`.
- The same snapshot explicitly blocks canonical ontology edit, source-law
  adoption, `MetricData(E)` adoption, `g_eff` scope change, coupling-law
  adoption, stress-energy semantics, matter-coupling derivation or adoption,
  Einstein equations, benchmark promotion, benchmark Gate Chair closure,
  completed derivation, future source-extension impossibility, and global
  theory rejection.

## Reviewer route model

The reviewer packet should be a concise inspection route:

1. Claim boundaries first.
2. Current source-state snapshot second.
3. Ontology and derivation-burden evidence third.
4. Source/provenance inspection fourth.
5. Reviewer questions last.

This avoids a marketing structure and prevents the page from reading like a
paper abstract.

## Claim boundaries

Safe:

- The packet can say the website snapshot reports scoped source-extension
  recovery-bridge-candidate evidence/precondition acceptance.
- The packet can say that this is evidence only, with no adoption of coupling
  law or matter coupling.
- The packet can route reviewers to source authority, current state,
  Distance-to-GR, ontology documents, claim boundaries, and specialist starts.
- The packet can state human review pending.

Unsafe:

- The packet proves a substrate derivation of GR.
- The packet claims accepted external review, peer review, empirical
  validation, or scientific viability.
- The packet claims `MetricData(E)` adoption, `g_eff` adoption/scope change,
  matter-coupling derivation, stress-energy semantics, Einstein equations,
  benchmark promotion, or completed derivation.
- The packet converts website publication, diagrams, manifests, or validators
  into scientific proof.

## Refuter pass

No-ai-slop refuter questions:

- Could a skeptical physicist read this as completed GR recovery? Answer: no,
  because the route must place the no-completed-derivation boundary before the
  inspection order.
- Could a mathematician read a diagram or guided route as a proof object?
  Answer: no, because the packet labels diagrams and guided starts as reader
  aids only.
- Could an AI reviewer read validator PASS or AgentJob evidence as scientific
  ownership? Answer: no, because the packet routes validator limits and AI
  workflow as process evidence only.
- Could a reviewer treat the page as external validation? Answer: no, because
  the packet status is human review pending and explicitly denies external
  validation.

Result: pass for publication as a reviewer-oriented website packet with
human review pending.

## Implementation recommendation

Create `/resources/reviewer-packet/` with:

- human review pending source notice;
- visible "what is claimed" and "what is not claimed" cards before source
  links;
- route-first inspection order through source authority, current state,
  Distance-to-GR, ontology documents, exact-GR benchmark boundary, derivation
  roadmap, and specialist guided starts;
- one static Mermaid-derived PNG showing claim boundaries before source
  inspection;
- route-map, page-provenance, source-manifest, asset-manifest, and
  public-comprehension validator coverage;
- desktop/mobile browser QA and explicit known curator blocker note.

## Limitations

This page does not request review, publish review results, or make scientific
claims stronger than the existing source-bound routes. It is a staged,
human-review-pending inspection guide.

## References

The AEther Flow Website. (2026). `/project/source-authority/`.

The AEther Flow Website. (2026). `/project/source-authority/claim-boundary-explorer/`.

The AEther Flow Website. (2026). `/project/physics/current-state/`.

The AEther Flow Website. (2026). `/project/physics/distance-to-gr/`.

The AEther Flow Website. (2026). `/resources/documents/`.

The AEther Flow Website. (2026). `/resources/guided-starts/`.

The AEther Flow Website. (2026). `src/data/physics_current_state_snapshot.json`.
