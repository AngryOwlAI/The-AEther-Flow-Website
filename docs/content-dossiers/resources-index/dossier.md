# Resources Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/resources/`
- Reader job: Use manifest-backed assets and internal routes while preserving status labels.
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
| `public/files/manifests/source_manifest.json` | website maintainer source | Source basis for this route. |

## Source-derived topic outline

1. Manifest-backed asset status
2. Internal route selection
3. Document downloads
4. Diagram gallery
5. Hash and source-ref limits

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Source manifest | Website manifest describing public assets and source references. | Does not supersede upstream registries. |
| Asset manifest | Generated file list with paths, kinds, bytes, hashes, titles, and source refs. | Indexes website files only. |
| Download | Public copy or derivative served by the website. | Retains source status. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Downloads retain source status.
- Resource cards do not create authority.
- Internal reading path comes before source inspection.

### Forbidden implications

- Resource link promotes a claim.
- Manifest row replaces upstream source registry.
- Hash proves scientific correctness.

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
| Mermaid source | `docs/content-dossiers/resources-index/diagrams/resource-manifest-chain.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/resources-manifest-chain.png` |
| Manifest id | `comprehension_resources_manifest_chain` |
| Alt text | Source manifest, asset manifest, resources index, document downloads, diagram gallery, hashes, status labels, and index does not create authority. |
| Caption | Resource pages organize committed assets and status labels downstream from source records. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The resource index organizes manifest-backed website assets, hashes, and internal reader paths while preserving each asset source status.

## Unsafe summary

Unsafe summary: A downloadable file, manifest row, or resource card creates source authority, scientific proof, or claim promotion.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/resources/`.
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
- The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`.
