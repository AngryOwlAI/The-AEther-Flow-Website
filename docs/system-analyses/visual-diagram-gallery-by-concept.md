# Visual Diagram Gallery By Concept

Status: PG-023 system analysis.
Quality gate: pass.
Date: 2026-06-28.

## Question

How should `/resources/diagrams/` help readers find useful visual aids by
concept while preserving the rule that diagrams are analysis aids, not source
authority?

## Assumptions and constraints

- Public SVG artwork in `src/` and `public/assets/` must remain animated and
  textless when used as SVG.
- Public Mermaid diagrams must remain static PNGs generated from tracked
  Mermaid sources; no browser-side Mermaid runtime should be introduced.
- Diagrams need alt text, captions, nearby boundary prose, and provenance.
- The gallery should group diagrams by reader concept: physics, AI workflow,
  operations, and source authority.
- The page is a resource index. It should not create, promote, or verify
  scientific or workflow claims.

## Source review

Reviewed website sources:

- `src/pages/resources/diagrams.astro`: existing flat gallery and manifest
  download list.
- `src/lib/siteContent.ts`: existing `diagramGalleryItems` titles, image paths,
  alt text, captions, and provenance.
- `public/files/manifests/source_manifest.json`: approved public comprehension
  diagram records and hashes.
- `scripts/render_mermaid_diagrams.py`: renderer registration for static PNGs.
- `scripts/validate_svg_policy.py`: SVG text/animation policy validator.
- `scripts/validate_public_comprehension.py`: route/dossier/diagram
  comprehension validator.
- `docs/content-dossiers/resources-diagrams/dossier.md`: current gallery
  comprehension contract.

## Findings

1. The current page already uses static assets and explains non-authority
   status, but the main gallery is flat and does not match the requested
   concept grouping.

2. The source manifest already contains enough approved comprehension diagram
   assets to build the requested concept groups without generating new diagrams.

3. Adding group metadata to the existing `diagramGalleryItems` is the smallest
   maintainable change because it preserves alt text, captions, and provenance
   close to the gallery data.

4. The current page has a duplicated `description` prop on `DownloadList`.
   PG-023 should repair it while preserving the download list.

## Concept grouping

| Group | Reader job | Examples |
| --- | --- | --- |
| Physics | Understand claim boundaries, derivation burdens, frozen routes, and benchmark separation. | GR burden ladder, metric response ladder, finite toy models, no-target-import discipline, negative results. |
| AI workflow | Understand governed AgentJob, role, memory, and synthesis patterns. | AI workflow chain, one bounded AgentJob, parent-child synthesis, role authority inspector, memory preflight. |
| Operations | Understand operational evidence, validation, publication, improvement, and tooling boundaries. | Operations spine, validator PASS boundary, publication flow, project-system improvement, technical tool tiers. |
| Source authority | Understand how sources, manifests, routes, and visual assets remain downstream from authority. | Source authority ladder, claim-boundary explorer, resource manifest chain, TeX/PDF derivative chain, diagram publication boundary. |

## Claim boundaries

Safe:

- The gallery can help readers choose a visual aid by concept.
- Each diagram can have alt text, caption, provenance, and manifest status.
- The page can say a diagram is approved for public comprehension.

Unsafe:

- A diagram proves science, validates a workflow, changes an operation, or
  promotes a claim.
- A diagram replaces source inspection or the route that owns the explanation.
- A public page requires Mermaid runtime to interpret the diagram.

## Implementation recommendation

- Keep the existing route.
- Add concept group metadata to `diagramGalleryItems`.
- Add missing approved diagrams already present in the manifest for AI,
  operations, and source-authority concepts.
- Render gallery sections by group with boundary prose and figures.
- Keep the `DownloadList` as a manifest-backed audit surface, but fix the
  duplicate prop.
- Do not generate new diagram assets for PG-023.

## References

The AEther Flow Website. (2026). `src/pages/resources/diagrams.astro`.

The AEther Flow Website. (2026). `src/lib/siteContent.ts`.

The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`.

The AEther Flow Website. (2026). `scripts/render_mermaid_diagrams.py`.

The AEther Flow Website. (2026). `scripts/validate_svg_policy.py`.
