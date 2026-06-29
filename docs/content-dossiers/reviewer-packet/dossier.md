# External Reviewer Packet Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/resources/reviewer-packet/`
- Reader job: Inspect what is claimed, what is not claimed, and where source
  evidence lives before forming a review judgment.
- Primary audience: external reviewers, physicists, mathematicians, AI-system
  reviewers, and technically literate science readers.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: PG-026 browser QA recorded; maintainer
  and external review remain pending.
- Source analysis path: `docs/system-analyses/external-review-packet.md`.

## Current page summary

The reviewer packet is a concise inspection route. It starts with claim
boundaries, then points reviewers to current state, Distance-to-GR, ontology
documents, source authority, claim boundaries, specialist guided starts, and
publication provenance. It does not claim external validation or completed
scientific results.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `README.md` | upstream project source | Project-level source context. |
| `research_control/program_state.yaml` | upstream control state | Current active state and task context. |
| `research_control/handoffs/handoff-0323.yaml` | upstream handoff | Latest handoff state. |
| `research_control/handoffs/handoff-0323.md` | upstream handoff | Public-readable boundary summary. |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | upstream registry | Burden and blocker context. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | upstream registry | Claim-boundary and forbidden wording context. |
| `ontology/README.md` | upstream ontology source | Ontology document orientation. |
| `ontology/tex/README.md` | upstream ontology source | TeX source authority context. |
| `registries/TEX_SOURCE_REGISTRY.csv` | upstream registry | Registered TeX source context. |
| `github-facing/source-authority-explainer.md` | generated noncanonical explainer | Source-authority reading rule. |
| `github-facing/exact-gr-benchmark-boundary-explainer.md` | generated noncanonical explainer | Benchmark versus derivation boundary. |
| `github-facing/aether-flow-physics-program-explainer.md` | generated noncanonical explainer | Physics program route context. |
| `github-facing/research-agent-workflow-explainer.md` | generated noncanonical explainer | AI workflow process context. |

## Source-derived topic outline

1. Human review pending status
2. What is claimed for review
3. What is not claimed
4. Inspection order
5. Source and provenance surfaces
6. Reviewer questions
7. Safe and unsafe summaries

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Reviewer packet | Concise source-inspection route for external reviewers. | Not external validation. |
| Current-state snapshot | Website copy of checked source-control state at a recorded refresh date. | Not a live feed. |
| Distance-to-GR | Burden and blocker map for derivation work. | Not a proof score. |
| Human review pending | Review status for high-risk claim-heavy pages. | Not approval. |

## Claim boundaries and forbidden implications

### Claim boundaries

- The packet can route reviewers to existing sourced pages.
- The packet can report checked-in website snapshot boundaries.
- The packet can state human review pending.
- The packet can identify source/provenance surfaces for inspection.

### Forbidden implications

- External validation, peer review, or scientific viability has been achieved.
- `MetricData(E)` is adopted.
- `g_eff` is adopted or its scope changed.
- Matter coupling, stress-energy semantics, Einstein equations, benchmark
  promotion, downstream GR promotion, or completed derivation has occurred.
- Website publication, diagrams, validators, manifests, or reading order prove
  scientific claims.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Reviewer purpose and human review pending status. |
| Plain summary | yes | What is claimed and not claimed. |
| Mechanism steps | yes | Inspection order. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Source/provenance route links. |
| Boundary block | yes | Must appear before source links. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required. |
| Safe/unsafe summary | yes | High-risk reviewer overread prevention. |
| Related internal routes | yes | Current state, Distance-to-GR, ontology documents, source authority. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/reviewer-packet/diagrams/reviewer-inspection-order.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/reviewer-inspection-order.png` |
| Manifest id | `comprehension_reviewer_inspection_order` |
| Alt text | Diagram showing the reviewer packet moving from claim boundaries to current state, Distance-to-GR, ontology documents, source inspection, reviewer questions, human review pending, and no-completed-derivation boundary. |
| Caption | Reviewer inspection starts with claim boundaries before source inspection. |
| Nearby prose requirement | Explain that the diagram is a static reader aid, not external validation or source authority. |
| Review status | Human review status: PG-026 browser QA recorded; maintainer and external review remain pending. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The reviewer packet gives an external reviewer a source-first
inspection order and visible claim boundaries.

## Unsafe summary

Unsafe summary: The reviewer packet proves scientific viability, external
validation, completed GR derivation, `MetricData(E)`, `g_eff`, matter coupling,
Einstein equations, benchmark promotion, or downstream GR promotion.

## New-page audit

- Is a new public page proposed? Yes.
- New route: `/resources/reviewer-packet/`.
- Reason a new route is justified: PG-026 requires the reviewer packet after
  authority/orientation prerequisites exist.
- Existing prerequisite routes: `/project/physics/current-state/`,
  `/project/physics/distance-to-gr/`,
  `/project/source-authority/`,
  `/project/source-authority/claim-boundary-explorer/`,
  `/resources/documents/`, and `/resources/guided-starts/`.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible before source inspection paths.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [x] No-ai-slop refuter pass is recorded in the system analysis.
- [x] Mobile layout and desktop layout were reviewed for PG-026.
- [x] Human review note is recorded under `docs/quality/`.

## References

- The AEther Flow. (2026). `README.md`.
- The AEther Flow. (2026). `research_control/program_state.yaml`.
- The AEther Flow. (2026). `research_control/handoffs/handoff-0323.yaml`.
- The AEther Flow. (2026). `research_control/handoffs/handoff-0323.md`.
- The AEther Flow. (2026). `registries/DISTANCE_TO_GR_LEDGER.csv`.
- The AEther Flow. (2026). `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- The AEther Flow. (2026). `ontology/README.md`.
- The AEther Flow. (2026). `ontology/tex/README.md`.
- The AEther Flow. (2026). `registries/TEX_SOURCE_REGISTRY.csv`.
- The AEther Flow Website. (2026). `src/data/physics_current_state_snapshot.json`.
