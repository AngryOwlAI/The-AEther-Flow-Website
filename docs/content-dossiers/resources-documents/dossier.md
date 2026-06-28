# Ontology Documents Content Dossier

Status: evidence-reviewed draft dossier.

## Route and reader job

- Public route: `/resources/documents/`
- Reader job: Distinguish registered TeX source authority from PDF derivative readability.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Technical validation passed; known ontology source-drift blocker remains.
- Source analysis path: `docs/system-analyses/ontology-document-library-reading-guide.md`.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, internal-first related routes, and the PG-022 reading guide.

## PG-022 evidence review

- Review artifact: `docs/system-analyses/ontology-document-library-reading-guide.md`.
- Review decision: Revise the existing route rather than create a new page.
- Source state: Committed upstream source at
  `01efc4f180221caf9425fbb24683eb54927b553e`.
- Boundary: The document library may expose website copies, source commits,
  hashes, and reading order. It cannot re-import assets, supersede upstream
  registered TeX, promote benchmark claims, or resolve curator source-drift
  review.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `ontology/README.md` | upstream source | Source basis for this route. |
| `ontology/tex/README.md` | upstream source | Source basis for this route. |
| `registries/TEX_SOURCE_REGISTRY.csv` | upstream source | Source basis for this route. |
| `registries/PDF_DERIVATIVE_REGISTRY.csv` | upstream source | Source basis for PDF derivative status. |
| `public/files/manifests/source_manifest.json` | website manifest | Source basis for website copy status, source commit, hashes, and import metadata. |

## Source-derived topic outline

1. Registered TeX source
2. TeX registry row
3. Generated PDF derivative
4. Website copies
5. Claim-status limits
6. Public read-this-first route path
7. Specialist reading order

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Registered TeX | TeX source recorded in upstream registry. | Claim status still depends on metadata and gates. |
| PDF derivative | Generated human-readable rendering. | Not independent authority when TeX is available. |
| Canonical ontology package | Current approved ontology asset set. | Not full first-principles GR derivation by availability alone. |
| Website copy | Public file served by this site with manifest hash and source commit. | Release readiness still depends on curator source-drift review. |
| Reading guide | Suggested reader sequence for interpretation. | Not a new scientific dependency claim. |

## Claim boundaries and forbidden implications

### Claim boundaries

- PDF does not supersede TeX.
- Download availability does not promote derivation.
- Registry metadata remains relevant.
- Source commit and import metadata remain visible.
- Reading order does not create source authority.

### Forbidden implications

- PDF download proves a scientific claim.
- Website copy supersedes upstream TeX.
- Canonical ontology package solves all downstream GR burdens.
- All files are equally current after upstream source changes.
- Reading order proves a dependency theorem.

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

Safe summary: The documents page makes ontology TeX and generated PDF derivatives easier to inspect while preserving TeX/PDF, source-commit, manifest, and source-drift boundaries.

## Unsafe summary

Unsafe summary: A PDF download, document list, reading order, or website copy independently proves a scientific claim, promotes a benchmark, or supersedes current upstream TeX.

## Reading guide contract

### Read this first

1. `/project/physics/ontology/` for vocabulary and derivation boundary.
2. `/project/physics/exact-gr-benchmark/` for benchmark status and burden.
3. `/project/source-authority/` for source, derivative, manifest, and website-copy boundaries.
4. `/project/physics/current-state/` for current research state and open derivation burdens.

### Specialist order

| Order | Document | Reason |
| --- | --- | --- |
| 1 | Foundations | Source vocabulary, core ontology terms, and baseline assumptions. |
| 2 | Dynamics | Evolution and response structure after foundations. |
| 3 | Geometry | Geometric interpretation layer. |
| 4 | Relativistic Recovery | Relativistic benchmark comparison. |
| 5 | Consistency | Internal compatibility checks. |
| 6 | Exact Closure Note | Compact closure-oriented note. |
| 7 | Exact Closure Sequence Overview | Guide to closure-sequence material. |
| 8 | Exact Closure Flagship Article | Broad synthesis after narrower source files. |

The specialist order is a reader aid derived from the website document order,
not a scientific dependency theorem.

## Compact page-publication brief

| Field | Value |
| --- | --- |
| Route | `/resources/documents/` |
| Source analysis path | `docs/system-analyses/ontology-document-library-reading-guide.md` |
| Claim status | approved ontology asset index with source-drift boundary visible |
| Diagram decision | Reuse existing TeX/PDF derivative-chain static PNG; no new diagram required. |
| Files changed | Route, component, support comprehension content, dossier, page route map, provenance, QA note. |
| Validation commands | `npm run validate:comprehension`, `npm run validate:manifests`, `npm run validate:content`, `npm run build`, browser QA. |
| Review status | Technical validation passed; known ontology source-drift blocker remains. |

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
- [x] Mobile layout and desktop layout were reviewed for PG-022.
- [x] Human review note is recorded under `docs/quality/sitewide-revamp-pg022-ontology-documents-reading-guide-qa.md`.

## References

- AEther-Flow Project. (2026). `ontology/README.md`.
- AEther-Flow Project. (2026). `ontology/tex/README.md`.
- AEther-Flow Project. (2026). `registries/TEX_SOURCE_REGISTRY.csv`.
- AEther-Flow Project. (2026). `registries/PDF_DERIVATIVE_REGISTRY.csv`.
- The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`.
