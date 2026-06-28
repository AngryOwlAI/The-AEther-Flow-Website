# Claim Boundary Explorer Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/source-authority/claim-boundary-explorer/`
- Reader job: Understand how allowed, forbidden, and gate-required claim
  language is recorded without treating the explorer as source authority.
- Primary audience: public readers, maintainers, and reviewers checking claim
  language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The page presents a checked-in snapshot of
`registries/CLAIM_BOUNDARY_REGISTRY.csv`. It shows row counts, current active
task wording, recurring forbidden phrases, recurring gate-required phrases,
recent representative rows, and pinned provenance links. It does not create,
edit, certify, or promote claim boundaries.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | upstream registry | Source basis for allowed, forbidden, and gate-required language. |
| `research_control/program_state.yaml` | upstream control state | Active task, latest handoff, current status, and next action. |
| `research_control/handoffs/handoff-0280.yaml` | upstream handoff | Structured current handoff context. |
| `research_control/handoffs/handoff-0280.md` | upstream handoff | Public-readable handoff and current boundary language. |
| `research_control/README.md` | upstream guidance | Bounded packet and source-control rules. |
| `github-facing/source-authority-explainer.md` | generated noncanonical explainer | Reader-facing source-authority orientation. |
| `github-facing/claim-gates-explainer.md` | generated noncanonical explainer | Reader-facing claim-gate orientation. |
| `src/data/claim_boundary_snapshot.json` | website snapshot | Checked-in public data generated from upstream sources. |

## Source-derived topic outline

1. Source-pinned snapshot metadata
2. Allowed claim wording
3. Forbidden promotion wording
4. Gate-required wording
5. Representative rows and authority-source paths
6. Pinned source provenance

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Claim boundary | A source-scoped record of what may and may not be implied. | It is not the same as claim adoption. |
| Allowed claim | Wording permitted inside the row's scope. | It does not authorize stronger wording. |
| Forbidden claim | Wording or implication explicitly blocked for that scope. | It is not a proof of global impossibility. |
| Gate-required claim | A stronger statement that would require protected approval. | The explorer cannot execute that gate. |
| Authority source path | Repository-relative source path that owns the row's basis. | It is provenance, not the website page's own authority. |

## Claim boundaries and forbidden implications

### Claim boundaries

- The explorer is a checked-in snapshot.
- Registry rows are shown as upstream source evidence.
- Phrase counts are descriptive, not proof scores.
- Current active-task wording remains narrower than adoption or derivation.

### Forbidden implications

- The explorer creates claim boundaries.
- Registry metadata proves physics claims.
- Gate readiness is a verdict.
- A validator, role, handoff, approval, generated derivative, cache, file
  order, or commit status is scientific proof.
- The page promotes `MetricData(E)`, `g_eff`, matter coupling, Einstein
  equations, benchmark success, or completed derivation.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Explain source-pinned snapshot status. |
| Plain summary | yes | Explain allowed versus forbidden wording. |
| Mechanism steps | yes | Registry row to snapshot to public route. |
| Term group | yes | Use glossary above. |
| Source basis | yes | Include registry, program state, handoff, source-authority, and claim-gates sources. |
| Boundary block | yes | State non-certification and no-promotion limits. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required. |
| Safe/unsafe summary | yes | High-risk overread prevention. |
| Related internal routes | yes | Source authority, claim gates, current state, Gate Chair. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/source-authority-claim-boundary-explorer/diagrams/claim-boundary-explorer.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/source-authority-claim-boundary-explorer.png` |
| Manifest id | `comprehension_source_authority_claim_boundary_explorer` |
| Alt text | Diagram showing the claim-boundary registry feeding a checked-in snapshot and public explorer while forbidden overreads remain blocked. |
| Caption | Static comprehension diagram: the explorer makes registry language readable without replacing source authority. |
| Nearby prose requirement | Explain that the diagram and page are reader aids, not gate decisions or registry edits. |
| Review status | Human review status: pending maintainer review. |

## Safe summary

Safe summary: The claim-boundary explorer helps readers see which wording is
allowed, forbidden, or gate-required in a source-pinned registry snapshot.

## Equation walkthrough contract

No equation walkthrough required for this route.

## Unsafe summary

Unsafe summary: The explorer certifies claims, executes gates, changes source
authority, or promotes scientific results.

## New-page audit

- Is a new public page proposed? Yes.
- New route: `/project/source-authority/claim-boundary-explorer/`
- Reason a new route is justified: The existing source-authority page explains
  authority layers, but PG-005 requires a dedicated reader surface for the
  claim-boundary registry's allowed and forbidden language.
- Existing related routes: `/project/source-authority/`,
  `/project/physics/claim-gates/`,
  `/project/physics/gate-chair-and-human-gates/`, and
  `/project/physics/current-state/`.

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

- The AEther Flow. (n.d.-a). `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- The AEther Flow. (n.d.-b). `research_control/program_state.yaml`.
- The AEther Flow. (n.d.-c). `research_control/handoffs/handoff-0280.yaml`.
- The AEther Flow. (n.d.-d). `research_control/handoffs/handoff-0280.md`.
- The AEther Flow. (n.d.-e). `research_control/README.md`.
- The AEther Flow. (n.d.-f). `github-facing/source-authority-explainer.md`.
- The AEther Flow. (n.d.-g). `github-facing/claim-gates-explainer.md`.
- The AEther Flow Website. (2026). `docs/system-analyses/claim-boundary-explorer.md`.
