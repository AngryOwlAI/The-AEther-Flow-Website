# PG-025 Specialist Guided Starts QA

Status: browser QA recorded.
Human review status: PG-025 browser QA recorded; maintainer release review
remains pending.
Date: 2026-06-28.

## Scope

Route reviewed: `/resources/guided-starts/`.

PG-025 implemented a specialist guided-start hub with anchored reading paths
for physicists, mathematicians, AI/agent researchers, software/system
engineers, and external reviewers. The reviewer section is explicitly
prerequisite-only and does not replace the PG-026 reviewer packet.

## Files and evidence

- Page source: `src/pages/resources/guided-starts/index.astro`
- Dossier: `docs/content-dossiers/guided-start-specialists/dossier.md`
- System analysis: `docs/system-analyses/specialist-guided-starts.md`
- Diagram source:
  `docs/content-dossiers/guided-start-specialists/diagrams/specialist-guided-starts.mmd`
- Public diagram: `/assets/diagrams/comprehension/specialist-guided-starts.png`
- Manifest id: `comprehension_specialist_guided_starts`

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

Known non-PG-025 blocker:

- `npm run validate:curator` fails only on the previously known 16 ontology
  TeX/PDF critical source-drift records. No PG-025 curator error was observed.

## Browser QA

Static server: `http://127.0.0.1:4322/resources/guided-starts/`.

Screenshots:

- Desktop:
  `output/playwright/sitewide-revamp-pg025-specialist-guided-starts-static-desktop-2026-06-28.png`
- Mobile:
  `output/playwright/sitewide-revamp-pg025-specialist-guided-starts-static-mobile-2026-06-28.png`

Observed metrics:

- Desktop viewport: 1440 x 1100.
- Mobile viewport: 390 x 1200.
- H1 count: 1.
- H1 text: `Specialist Guided Starts`.
- Audience sections: 5.
- Images: 2 loaded, 0 unloaded.
- Horizontal overflow: none observed.
- Source notice: visible on desktop and mobile.

Visual result:

- Desktop layout reviewed. The hero, source notice, diagram, five audience
  sections, safe/unsafe summary, and related-route cards are contained.
- Mobile layout reviewed. Source-reference links wrap inside the notice,
  audience sections stack cleanly, and no visual overlap was observed.

## References

The AEther Flow Website. (2026). `docs/system-analyses/specialist-guided-starts.md`.

The AEther Flow Website. (2026). `docs/content-dossiers/guided-start-specialists/dossier.md`.

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`.
