# Documentation Curator Publication Process Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/operations/publication-process/`
- Reader job: Understand how public pages move from brief and source spec to screenshots and review.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/documentation-curator-publication-process-explainer.md` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Publication brief
2. Source spec
3. Reader page
4. Screenshots
5. Human review and manifest updates

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Publication brief | Planning surface for reader job and source basis. | Not source authority alone. |
| Source spec | Source-boundary contract for a public page. | Cannot strengthen source claims. |
| Human review | Judgment that the page teaches without overclaiming. | Separate from scripted PASS. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Readable pages stay downstream.
- Human comprehension review remains required.
- Publication cannot promote claims.

### Forbidden implications

- Public page changes source authority.
- Screenshots prove comprehension alone.
- Source spec broadens source claims.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with reader context and source-boundary notice. |
| Plain summary | yes | Provided in the reusable comprehension block. |
| Mechanism steps | yes | Source-derived route mechanism. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Sources listed above and rendered as provenance. |
| Boundary block | yes | Claim boundaries and forbidden implications. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required for this route. |
| Safe/unsafe summary | yes | High-risk overread prevention. |
| Related internal routes | yes | Internal-first reader journey before provenance links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/operations-publication-process/diagrams/publication-source-review-flow.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/operations-publication-review-flow.png` |
| Manifest id | `comprehension_operations_publication_review_flow` |
| Alt text | Publication brief, source spec, reader page, screenshots, human review, manifests, and readable page is downstream. |
| Caption | Publication improves explanation without changing source authority. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Publication work translates source-bound material into readable pages with screenshots, human review, manifests, and provenance.

## Unsafe summary

Unsafe summary: A public page or screenshot changes source authority, proves comprehension by script alone, or promotes source claims.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/operations/publication-process/`.
- Reason a new route is or is not justified: The existing route is the correct public surface for this content.

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

- AEther-Flow Project. (2026). `github-facing/documentation-curator-publication-process-explainer.md`.
