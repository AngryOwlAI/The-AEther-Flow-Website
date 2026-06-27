# Ontology Documents Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/resources/documents/`
- Reader job: Distinguish registered TeX source authority from PDF derivative readability.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `ontology/README.md` | upstream source | Source basis for this route. |
| `ontology/tex/README.md` | upstream source | Source basis for this route. |
| `registries/TEX_SOURCE_REGISTRY.csv` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Registered TeX source
2. TeX registry row
3. Generated PDF derivative
4. Website copies
5. Claim-status limits

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Registered TeX | TeX source recorded in upstream registry. | Claim status still depends on metadata and gates. |
| PDF derivative | Generated human-readable rendering. | Not independent authority when TeX is available. |
| Canonical ontology package | Current approved ontology asset set. | Not full first-principles GR derivation by availability alone. |

## Claim boundaries and forbidden implications

### Claim boundaries

- PDF does not supersede TeX.
- Download availability does not promote derivation.
- Registry metadata remains relevant.

### Forbidden implications

- PDF download proves a scientific claim.
- Website copy supersedes upstream TeX.
- Canonical ontology package solves all downstream GR burdens.

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
| Mermaid source | `docs/content-dossiers/resources-documents/diagrams/tex-pdf-derivative-chain.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/resources-tex-pdf-derivative-chain.png` |
| Manifest id | `comprehension_resources_tex_pdf_derivative_chain` |
| Alt text | Registered TeX source, TeX registry row, generated PDF derivative, website TeX copy, human-readable PDF download, source inspection download, and PDF is derivative. |
| Caption | TeX source authority and PDF readability are different asset roles. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The documents page makes canonical ontology TeX and generated PDF derivatives easier to inspect while preserving the TeX/PDF authority boundary.

## Unsafe summary

Unsafe summary: A PDF download, document list, or website copy independently proves or promotes a scientific claim.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/resources/documents/`.
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

- AEther-Flow Project. (2026). `ontology/README.md`.
- AEther-Flow Project. (2026). `ontology/tex/README.md`.
- AEther-Flow Project. (2026). `registries/TEX_SOURCE_REGISTRY.csv`.
