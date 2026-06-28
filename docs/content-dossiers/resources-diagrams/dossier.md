# Diagram Gallery Content Dossier

Status: evidence-reviewed draft dossier.

## Route and reader job

- Public route: `/resources/diagrams/`
- Reader job: Read diagrams as visual orientation aids with tracked sources and non-authority status.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Technical validation passed; known ontology source-drift blocker remains.
- Source analysis path: `docs/system-analyses/visual-diagram-gallery-by-concept.md`.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, internal-first related routes, and PG-023 concept grouping.

## PG-023 evidence review

- Review artifact: `docs/system-analyses/visual-diagram-gallery-by-concept.md`.
- Review decision: Revise the existing route rather than create a new page or
  generate new diagram assets.
- Boundary: Concept groups organize reader navigation. They do not make
  diagrams authoritative, prove claims, change workflow authority, or replace
  source inspection.
- Implementation note: The route preserves existing static PNG assets and
  repairs the duplicate `description` prop on the manifest-backed
  `DownloadList`.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `docs/content-dossiers/README.md` | website maintainer source | Source basis for this route. |
| `public/files/manifests/source_manifest.json` | website maintainer source | Source basis for this route. |
| `scripts/render_mermaid_diagrams.py` | website maintainer source | Source basis for this route. |

## Source-derived topic outline

1. Editable Mermaid source
2. Generated static PNG
3. Manifest entry
4. Caption and nearby prose
5. No diagram authority
6. Concept group navigation

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Static diagram | Generated public image rendered from tracked diagram source. | Not a source claim. |
| Diagram provenance | Source path, manifest id, and generation path. | Supports audit, not promotion. |
| Runtime Mermaid | Browser rendering dependency. | Out of scope for public pages. |
| Concept group | Reader-facing group such as physics, AI workflow, operations, or source authority. | Organizes diagrams without changing claim status. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Visual clarity is not evidence.
- Public pages use static PNGs.
- Claims remain in source and prose.
- Concept grouping is navigation, not authority.

### Forbidden implications

- Diagram proves science.
- Diagram replaces source inspection.
- Mermaid runtime is needed in the public browser.
- Concept group proves a claim or workflow.

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
| Mermaid source | `docs/content-dossiers/resources-diagrams/diagrams/diagram-publication-boundary.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/resources-diagram-publication-boundary.png` |
| Manifest id | `comprehension_resources_diagram_publication_boundary` |
| Alt text | Mermaid source, generated PNG, manifest entry, diagram gallery, nearby prose and caption, hash-backed asset status, and diagram is not source authority. |
| Caption | A diagram becomes public only as a manifest-backed reader aid. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The diagram gallery shows manifest-backed visual aids grouped by concept, with editable sources, static PNG outputs, captions, provenance, and non-authority boundaries.

## Unsafe summary

Unsafe summary: A diagram or concept group proves science, changes workflow authority, replaces source inspection, or needs Mermaid in the public browser runtime.

## Concept group contract

| Group | Reader job |
| --- | --- |
| Physics concepts | Understand ontology, benchmark status, derivation burdens, frozen routes, and claim gates. |
| AI workflow concepts | Understand bounded AgentJobs, role authority, memory, task authority, and parent-child synthesis. |
| Operations concepts | Understand routing, validation, publication, project-system improvement, and tool boundaries. |
| Source authority concepts | Understand source boundaries, manifests, reader routes, TeX/PDF derivatives, and diagram-publication status. |

Each rendered figure must retain alt text, caption, and provenance.

## Compact page-publication brief

| Field | Value |
| --- | --- |
| Route | `/resources/diagrams/` |
| Source analysis path | `docs/system-analyses/visual-diagram-gallery-by-concept.md` |
| Claim status | source-index-only diagram gallery |
| Diagram decision | Reuse existing static PNG assets; no new diagram generated for PG-023. |
| Files changed | Route, site content diagram metadata, support comprehension content, dossier, QA note. |
| Validation commands | `npm run validate:comprehension`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, browser QA. |
| Review status | Technical validation passed; known ontology source-drift blocker remains. |

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/resources/diagrams/`.
- Reason a new route is or is not justified: The existing route is the correct public surface for this content.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [x] Mobile layout and desktop layout were reviewed for PG-023.
- [x] Human review note is recorded under `docs/quality/sitewide-revamp-pg023-diagram-gallery-by-concept-qa.md`.

## References

- The AEther Flow Website. (2026). `docs/content-dossiers/README.md`.
- The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`.
- The AEther Flow Website. (2026). `scripts/render_mermaid_diagrams.py`.
- The AEther Flow Website. (2026). `docs/system-analyses/visual-diagram-gallery-by-concept.md`.
