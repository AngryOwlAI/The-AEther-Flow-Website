# Current Physics State Content Dossier

Status: Task 9 and supporting-surface dossier.
Human review status: pending maintainer review.

## Route and reader job

- Public route: `/project/physics/current-state/`
- Reader job: read a checked-in source-state snapshot without treating it as a
  live authority surface or claim promotion.
- Primary audience: readers checking current physics burden state.
- Maintainer owner: website maintainer.
- Review status: implemented for mechanical audit; maintainer acceptance still
  required.

## Current page summary

The page already states snapshot metadata, active burden, blocked claims,
source provenance, and no-promotion boundaries. The remediation adds a static
snapshot-boundary diagram and explicit safe/unsafe summary block.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `research_control/program_state.yaml` | draft/control state | Active source control state. |
| `research_control/handoffs/handoff-0250.yaml` | draft/control handoff | Latest handoff state in snapshot. |
| `research_control/handoffs/handoff-0250.md` | draft/control handoff | Human-readable handoff summary. |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | registry | Burden rows. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | registry | Blocked and forbidden claims. |
| `src/data/physics_current_state_snapshot.json` | website snapshot | Checked-in data used by this route. |

## Source-derived topic outline

1. Snapshot status and refresh date.
2. Active burden and downstream blocked rows.
3. Blocked claims list.
4. Pinned provenance links.
5. Safe and unsafe summary.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Checked-in snapshot | Website JSON copy of selected upstream state. | Not live source authority. |
| Blocked claim | Claim explicitly not authorized. | Must not be softened into progress. |
| Local source-purity audit | Bounded audit result for a candidate as written. | Not g_eff or downstream GR adoption. |

## Claim boundaries and forbidden implications

### Claim boundaries

- The page reports checked-in state.
- Drift must be handled by curator/refresh workflow.
- Blocked claims remain visible.

### Forbidden implications

- Do not imply the snapshot auto-refreshes.
- Do not adopt MetricData(E), g_eff, matter coupling, Einstein equations, or
  benchmark status.
- Do not promote draft/control records.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Snapshot route. |
| Plain summary | Yes | Source-state snapshot, not authority. |
| Mechanism steps | Yes | Read date, preserve blocked claims, use provenance. |
| Term group | Yes | Snapshot, blocked claim, audit. |
| Source basis | Optional | Page already has pinned source provenance. |
| Boundary block | Yes | No auto-refresh, no promotion. |
| Diagram | Yes | Static snapshot boundary map. |
| Equation walkthrough | No | No equation walkthrough required for this route. |
| Safe/unsafe summary | Yes | Current-state overclaim risk. |
| Related internal routes | Yes | Existing physics route links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-current-state/diagrams/snapshot-boundary.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-current-state-snapshot-boundary.png` |
| Manifest id | `comprehension_physics_current_state_snapshot_boundary` |
| Alt text | Diagram showing upstream control state flowing into a checked-in website snapshot with blocked downstream claims preserved. |
| Caption | Static comprehension diagram: current-state pages report a bounded snapshot and preserve blocked downstream claims. |
| Nearby prose requirement | State that the snapshot does not auto-refresh or promote claims. |
| Review status | pending maintainer review |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The current-state page is a checked-in website snapshot of
upstream physics control state with blocked downstream claims preserved.

## Unsafe summary

Unsafe summary: The website snapshot auto-refreshes, adopts draft/control data,
constructs g_eff, derives matter coupling or Einstein equations, or promotes
the benchmark.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead:
  `/project/physics/current-state/`.
- Reason a new route is or is not justified: existing route owns current-state
  snapshot explanation.

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

The AEther Flow Website. (2026).
`src/data/physics_current_state_snapshot.json` [Checked-in website snapshot].

AEther-Flow Project. (2026). `registries/DISTANCE_TO_GR_LEDGER.csv`
[Distance-to-GR ledger].
