# PG-024 Publication And Provenance System QA

Status: browser QA recorded.
Human review status: PG-024 browser QA recorded; maintainer release review
remains pending.
Date: 2026-06-28.

## Scope

Route reviewed:
`/project/source-authority/publication-and-provenance-system/`.

PG-024 implemented the source-authority child route explaining route maps,
page provenance, source manifests, asset manifests, page and asset hashes,
and internal-first routing. The page preserves the boundary that publication
evidence is not source truth, claim proof, or release approval.

## Files and evidence

- Page source:
  `src/pages/project/source-authority/publication-and-provenance-system/index.astro`
- Dossier:
  `docs/content-dossiers/source-authority-publication-and-provenance-system/dossier.md`
- System analysis:
  `docs/system-analyses/publication-and-provenance-system.md`
- Diagram source:
  `docs/content-dossiers/source-authority-publication-and-provenance-system/diagrams/publication-provenance-system.mmd`
- Public diagram:
  `/assets/diagrams/comprehension/source-authority-publication-provenance-system.png`
- Manifest id:
  `comprehension_source_authority_publication_provenance_system`

## Validation

Passed:

- `python3 scripts/render_mermaid_diagrams.py`
- diagram source-manifest hash refresh
- `python3 scripts/build_asset_manifest.py --write`
- `python3 scripts/generate_page_provenance.py`
- `npm run validate:comprehension`
- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:provenance`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `git diff --check`
- `npm run build`
- `python3 scripts/quality_gate.py`
- `npm run validate:cloudflare`
- `python3 scripts/run_curator.py --write`

Known non-PG-024 blocker:

- `npm run validate:curator` fails only on the previously known 16 ontology
  TeX/PDF critical source-drift records. No PG-024 curator error was observed.

## Browser QA

Static server:
`http://127.0.0.1:4322/project/source-authority/publication-and-provenance-system/`.

Screenshots:

- Desktop:
  `output/playwright/sitewide-revamp-pg024-publication-provenance-system-static-desktop-2026-06-28.png`
- Mobile:
  `output/playwright/sitewide-revamp-pg024-publication-provenance-system-static-mobile-2026-06-28.png`

Observed metrics:

- Desktop viewport: 1440 x 1100.
- Mobile viewport: 390 x 1200.
- H1 count: 1.
- H1 accessible text: `Publication And Provenance System`.
- Images: 2 loaded, 0 unloaded.
- Horizontal overflow: none observed.
- Source notice: visible on desktop and mobile.

Visual result:

- Desktop layout reviewed. The repaired H1 breaks on complete words, the
  diagram is visible in the hero, and cards remain contained.
- Mobile layout reviewed. The route remains readable, source-reference links
  wrap inside their container, and no visual overlap was observed.

## References

The AEther Flow Website. (2026). `docs/architecture/website-feature-and-functionality.md`.

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`.

The AEther Flow Website. (2026). `public/files/manifests/page_provenance.json`.

The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`.

The AEther Flow Website. (2026). `public/files/manifests/asset_manifest.json`.
