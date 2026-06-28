# Publication And Provenance System Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/source-authority/publication-and-provenance-system/`
- Reader job: Understand how route maps, page provenance, source manifests,
  asset manifests, and internal-first routing make static publication
  auditable.
- Primary audience: public readers and maintainers reviewing provenance and
  source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: PG-024 browser QA recorded; maintainer
  release review remains pending.
- Source analysis path: `docs/system-analyses/publication-and-provenance-system.md`.

## Current page summary

This is a new source-authority child route. It explains the publication and
provenance system used by the website while preserving the upstream
source-authority boundary.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `docs/architecture/website-feature-and-functionality.md` | website maintainer source | Source basis for architecture and manifest model. |
| `public/files/manifests/page_route_map.json` | website public manifest | Source basis for route-to-source mapping. |
| `public/files/manifests/page_provenance.json` | website public manifest | Source basis for page/source hash provenance. |
| `public/files/manifests/source_manifest.json` | website public manifest | Source basis for public asset source/status records. |
| `public/files/manifests/asset_manifest.json` | website public manifest | Source basis for served asset file hashes and sizes. |
| `scripts/generate_page_provenance.py` | website maintainer source | Source basis for provenance generation. |
| `scripts/validate_page_provenance.py` | website maintainer source | Source basis for provenance validation. |
| `scripts/validate_manifest_paths.py` | website maintainer source | Source basis for asset manifest validation. |
| `scripts/validate_internal_first_links.py` | website maintainer source | Source basis for internal-first routing checks. |

## Source-derived topic outline

1. Source basis
2. Page route map
3. Page provenance
4. Source manifest
5. Asset manifest
6. Static build
7. Internal-first reader routes
8. Provenance links
9. Publication is not source truth

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Page route map | Manifest that declares which sources a public route adapts and which boundary type applies. | Declaration, not source truth by itself. |
| Page provenance | Generated manifest with page hash, source hashes, commit metadata, and source URLs. | Audit evidence, not conceptual correctness proof. |
| Source manifest | Manifest that records public asset source paths, approval status, hashes, and notes. | Does not promote asset claims. |
| Asset manifest | Generated manifest that records served file path, kind, byte count, hash, title, and source reference. | Indexes website files only. |
| Internal-first routing | Rule that primary reader journeys use internal routes when they exist. | Does not hide source links; source links remain provenance. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Manifest presence is not source truth.
- Page hashes constrain publication but do not prove comprehension.
- Source hashes support audit but do not promote claims.
- Internal routes are reader paths; source links remain provenance.

### Forbidden implications

- A route-map entry proves a scientific claim.
- A page-provenance hash proves the page is conceptually correct.
- Asset-manifest approval promotes source authority.
- Internal-first routing hides source authority.
- The website page supersedes upstream sources or registries.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with reader context and source-boundary notice. |
| Plain summary | yes | Page lead and diagram-backed system summary. |
| Mechanism steps | yes | Route map, page provenance, source manifest, asset manifest, validation. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Sources listed above and rendered as provenance. |
| Boundary block | yes | Claim boundaries and forbidden implications. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required for this route. |
| Safe/unsafe summary | yes | High-risk overread prevention. |
| Related internal routes | yes | Internal-first route links before source links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/source-authority-publication-and-provenance-system/diagrams/publication-provenance-system.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/source-authority-publication-provenance-system.png` |
| Manifest id | `comprehension_source_authority_publication_provenance_system` |
| Alt text | Source basis feeding page route map, page provenance, source manifest, asset manifest, static build, internal reader routes, provenance links, and publication-is-not-source-truth boundary. |
| Caption | Publication manifests make routes and assets auditable without making publication source truth. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Publication provenance records which sources and assets a public
route depends on, which hashes were checked, and where source inspection lives.

## Unsafe summary

Unsafe summary: A manifest row, page hash, asset hash, or internal-first route
proves a scientific claim, promotes a source, or replaces upstream authority.

## New-page audit

- Is a new public page proposed? Yes.
- New child route:
  `/project/source-authority/publication-and-provenance-system/`.
- Reason a new route is justified: Source authority now needs a focused
  maintainer/public explainer for page provenance, route maps, source manifests,
  asset manifests, and internal-first routing. The existing source-authority
  landing explains the general trust boundary but not the website publication
  machinery.

## Compact page-publication brief

| Field | Value |
| --- | --- |
| Route | `/project/source-authority/publication-and-provenance-system/` |
| Source analysis path | `docs/system-analyses/publication-and-provenance-system.md` |
| Claim status | publication/provenance orientation |
| Diagram decision | Add one static Mermaid-derived PNG for the provenance system. |
| Files changed | New route, dossier, diagram, render registration, source manifest, asset manifest, route map, site content navigation, public-comprehension validator, QA note. |
| Validation commands | `npm run validate:comprehension`, `npm run validate:manifests`, `npm run validate:links`, `npm run build`, browser QA. |
| Review status | PG-024 browser QA recorded; maintainer release review remains pending. |

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [x] Mobile layout and desktop layout were reviewed for PG-024.
- [x] Human review note is recorded under `docs/quality/`.

## References

- The AEther Flow Website. (2026). `docs/architecture/website-feature-and-functionality.md`.
- The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`.
- The AEther Flow Website. (2026). `public/files/manifests/page_provenance.json`.
- The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`.
- The AEther Flow Website. (2026). `public/files/manifests/asset_manifest.json`.
- The AEther Flow Website. (2026). `scripts/generate_page_provenance.py`.
- The AEther Flow Website. (2026). `scripts/validate_page_provenance.py`.
- The AEther Flow Website. (2026). `scripts/validate_manifest_paths.py`.
- The AEther Flow Website. (2026). `scripts/validate_internal_first_links.py`.
