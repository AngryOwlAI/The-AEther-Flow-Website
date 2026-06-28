# Distance To GR Dashboard Content Dossier

Status: PG-002 implementation dossier.
Human review status: technical validation passed; maintainer review recommended before release.

## Route and reader job

- Public route: `/project/physics/distance-to-gr/`
- Reader job: understand the derivation-burden ledger without treating it as a
  proof surface, progress bar, or live source authority.
- Primary audience: general readers, physicists, mathematicians, reviewers,
  and maintainers.
- Maintainer owner: website maintainer.
- Review status: technical validation passed; no deployment.
- Source-analysis path: `docs/system-analyses/distance-to-gr-dashboard.md`

## Current page summary

This is a new dashboard page. It should explain the checked-in
Distance-to-GR snapshot, group the ledger rows into reader-legible regions,
and keep all downstream GR promotions blocked unless upstream source authority
explicitly changes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | registry | Primary burden rows. |
| `research_control/design/gr_derivation_burden_map.md` | control note | Milestone order and burden semantics. |
| `research_control/design/mathematical_decisiveness_completion_contract.md` | control note | Separates validation from proof. |
| `research_control/design/obstruction_and_freeze_control.md` | control note | Freeze and obstruction interpretation. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | registry | Forbidden claim overreads. |
| `research_control/program_state.yaml` | control state | Current task and handoff context. |
| `research_control/handoffs/handoff-0280.yaml` | control handoff | Latest no-adoption, gate-ready state. |
| `research_control/handoffs/handoff-0280.md` | control handoff | Public-readable handoff summary. |
| `src/data/distance_to_gr_snapshot.json` | website snapshot | Checked-in data used by this route. |

## Source-derived topic outline

1. Explain that the dashboard is a burden map, not a percentage.
2. Show snapshot metadata and status counts.
3. Group ledger rows by source foundation, metric bridge, downstream GR, and
   negative/control rows.
4. State blocked downstream implications.
5. Provide pinned provenance links without making them the primary journey.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Distance-to-GR ledger | Persistent source-side record of derivation-burden rows. | Not proof or live public synchronization. |
| Burden row | One tracked obligation or routing state in the derivation chain. | Earlier row status does not unlock later rows. |
| Gate readiness | Evidence may be ready for a future protected review. | Not a Gate Chair verdict. |
| `frozen negative` | A scoped route is frozen after a negative result. | Not global theory rejection. |
| `source-extension` | Scoped source-side extension data accepted or considered under guarded rules. | Not downstream GR promotion. |

## Claim boundaries and forbidden implications

### Claim boundaries

- The page reports a checked-in dashboard snapshot.
- The ledger is a control surface, not an automatic proof surface.
- Rows remain scoped to their burden and source authority.
- Downstream matter-coupling, Einstein-equation, benchmark, and Gate Chair
  claims remain blocked unless source authority explicitly changes.

### Forbidden implications

- Do not present a completion percentage.
- Do not infer `MetricData(E)` adoption, `g_eff` scope change,
  matter-coupling adoption, Einstein equations, benchmark promotion, or
  completed derivation.
- Do not read gate-ready status as a Gate Chair verdict.
- Do not read `frozen negative` as global rejection.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Why the dashboard exists. |
| Plain summary | Yes | Burden map, not proof. |
| Mechanism steps | Yes | Snapshot, grouping, blocked downstream claims. |
| Term group | Yes | Ledger, burden row, gate readiness, frozen negative. |
| Source basis | Yes | SourceNotice and provenance links. |
| Boundary block | Yes | No progress-bar proof or downstream promotion. |
| Diagram | Yes | Static dashboard flow diagram. |
| Equation walkthrough | No | No equation derivation is displayed. |
| Safe/unsafe summary | Yes | High overclaim risk. |
| Related internal routes | Yes | Current state, roadmap, source extension, Gate Chair, claim gates. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-distance-to-gr/diagrams/distance-dashboard-boundary.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-distance-to-gr-dashboard.png` |
| Manifest id | `comprehension_physics_distance_to_gr_dashboard` |
| Alt text | Diagram showing the Distance-to-GR ledger, burden map, claim boundaries, checked-in snapshot, dashboard groups, and forbidden overreads. |
| Caption | Static comprehension diagram: the dashboard groups ledger rows while preserving the no-promotion boundary. |
| Nearby prose requirement | State that dashboard status is not percentage completion or proof. |
| Review status | technical validation passed |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The Distance-to-GR dashboard is a checked-in, source-pinned map
of derivation burdens and blocked downstream promotions.

## Unsafe summary

Unsafe summary: The dashboard proves GR is nearly derived, computes a
percentage completion score, adopts `MetricData(E)`, changes `g_eff` scope,
derives matter coupling or Einstein equations, promotes the benchmark, or
records a Gate Chair verdict.

## New-page audit

- Is a new public page proposed? Yes.
- Existing route that should be used instead: none. The existing
  `/project/physics/gr-derivation-roadmap/` page explains the conceptual
  burden ladder, but PG-002 requires a ledger-backed dashboard.
- Reason a new route is justified: the first-wave authority/orientation path
  needs a direct internal target for ledger-backed burden state.

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

The AEther Flow. (n.d.-a). `registries/DISTANCE_TO_GR_LEDGER.csv` [Distance-to-GR ledger].

The AEther Flow. (n.d.-b). `research_control/design/gr_derivation_burden_map.md` [GR derivation burden map].

The AEther Flow. (n.d.-c). `research_control/design/mathematical_decisiveness_completion_contract.md` [Completion contract].

The AEther Flow. (n.d.-d). `research_control/design/obstruction_and_freeze_control.md` [Obstruction and freeze control].

The AEther Flow. (n.d.-e). `registries/CLAIM_BOUNDARY_REGISTRY.csv` [Claim-boundary registry].

The AEther Flow. (n.d.-f). `research_control/handoffs/handoff-0280.yaml` [Latest handoff YAML].

The AEther Flow Website. (n.d.). `src/data/distance_to_gr_snapshot.json` [Checked-in dashboard snapshot].
