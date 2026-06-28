# General-Public Guided Start Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/resources/guided-starts/general-public/`
- Reader job: Follow a short, internal-first path through the website without
  mistaking explanation for source authority.
- Primary audience: general public readers.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The page assembles existing sourced pages into a guided public reading path. It
answers three reader questions: what is this project, what is currently
claimed, and what should not be inferred. It introduces no scientific claim of
its own.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/project-overview-explainer.md` | generated noncanonical explainer | Home route source basis. |
| `github-facing/source-authority-explainer.md` | generated noncanonical explainer | Source-authority reading rule. |
| `research_control/program_state.yaml` | upstream control state | Current-state route context. |
| `research_control/handoffs/handoff-0280.yaml` | upstream handoff | Current handoff context. |
| `research_control/handoffs/handoff-0280.md` | upstream handoff | Public-readable current boundary. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | upstream registry | Claim-boundary and forbidden-overread context. |
| `public/files/manifests/page_route_map.json` | website maintainer source | Internal route assembly and publication status. |

## Source-derived topic outline

1. What is this project?
2. What is currently claimed?
3. What should I not infer?
4. When should I inspect provenance?
5. What should I read next?

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Guided start | Curated reading path through already sourced pages. | Does not create claims. |
| Internal-first route | Website route used before external source inspection. | Source links remain provenance. |
| Current state | Checked-in source-state snapshot page. | Not a live authority feed. |
| Forbidden inference | Stronger claim blocked by claim-boundary sources. | Not proof of global impossibility. |

## Claim boundaries and forbidden implications

### Claim boundaries

- The route assembles existing pages.
- It can recommend a reading order.
- It can state when to inspect provenance.
- It can warn against overreads already blocked by sourced pages.

### Forbidden implications

- The guided start creates new scientific claims.
- The guided start updates current source state.
- A simplified reading path proves `MetricData(E)`, `g_eff`, matter coupling,
  Einstein equations, benchmark promotion, or completed derivation.
- A public-friendly explanation replaces upstream source authority.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Explain who the guided start is for. |
| Plain summary | yes | Three-question route structure. |
| Mechanism steps | yes | Internal route sequence. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Existing sourced pages and route map. |
| Boundary block | yes | No new claims and no live source update. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required. |
| Safe/unsafe summary | yes | General-public overread prevention. |
| Related internal routes | yes | Home, current state, source authority, claim boundaries, documents. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/guided-start-general-public/diagrams/general-public-guided-start.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/general-public-guided-start.png` |
| Manifest id | `comprehension_general_public_guided_start` |
| Alt text | Diagram showing a general-public reader moving through Home, current state, source authority, claim boundaries, and provenance without creating new claims. |
| Caption | Static comprehension diagram: the guided start assembles existing internal pages and preserves source authority. |
| Nearby prose requirement | Explain that the diagram is a reader aid, not a source-state update or scientific proof. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The guided start tells general readers which existing sourced
pages to read first and when to inspect provenance.

## Unsafe summary

Unsafe summary: The guided start itself states new physics results, updates
current source state, or converts public explanation into proof.

## New-page audit

- Is a new public page proposed? Yes.
- New route: `/resources/guided-starts/general-public/`.
- Reason a new route is justified: PG-006 requires the first guided-start path
  for the accepted primary audience, and the resources area is the established
  reader-support location.
- Existing related routes: `/`,
  `/project/physics/current-state/`, `/project/source-authority/`,
  `/project/source-authority/claim-boundary-explorer/`, and `/resources/`.

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

- The AEther Flow. (n.d.-a). `github-facing/project-overview-explainer.md`.
- The AEther Flow. (n.d.-b). `github-facing/source-authority-explainer.md`.
- The AEther Flow. (n.d.-c). `research_control/program_state.yaml`.
- The AEther Flow. (n.d.-d). `research_control/handoffs/handoff-0280.yaml`.
- The AEther Flow. (n.d.-e). `research_control/handoffs/handoff-0280.md`.
- The AEther Flow. (n.d.-f). `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`.
