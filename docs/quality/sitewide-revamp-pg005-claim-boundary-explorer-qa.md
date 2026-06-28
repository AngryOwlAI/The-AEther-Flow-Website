# PG-005 Claim Boundary Explorer QA

Date: 2026-06-28

## Scope

Implemented Task PG-005 from
`ImplementationPlans/sitewide_page_revamp_task_packets.md`.

Routes reviewed:

- `/project/source-authority/claim-boundary-explorer/`
- `/project/source-authority/`

## Source State

- Upstream source repository:
  `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`
- Upstream commit:
  `4d249ba24ead51445e496a74b2f6072149bc7609`
- Active task: `RT-20260614-247`
- Latest handoff: `handoff-0280`
- Claim-boundary registry rows in snapshot: 416
- Snapshot file: `src/data/claim_boundary_snapshot.json`

## Changes Checked

- Added source-pinned claim-boundary snapshot generator:
  `scripts/refresh_claim_boundary_snapshot.py`.
- Added checked-in snapshot:
  `src/data/claim_boundary_snapshot.json`.
- Added route:
  `src/pages/project/source-authority/claim-boundary-explorer/index.astro`.
- Strengthened source-authority landing with an internal link to the explorer.
- Added source-analysis and content dossier:
  - `docs/system-analyses/claim-boundary-explorer.md`
  - `docs/content-dossiers/source-authority-claim-boundary-explorer/dossier.md`
- Added static comprehension diagram:
  - `docs/content-dossiers/source-authority-claim-boundary-explorer/diagrams/claim-boundary-explorer.mmd`
  - `/assets/diagrams/comprehension/source-authority-claim-boundary-explorer.png`
- Updated route map, source manifest, asset manifest, page provenance,
  public-comprehension validator, page-provenance validator, and diagram
  renderer.

## Focused Validation

Passed:

- `python3 scripts/refresh_claim_boundary_snapshot.py --write`
- `python3 scripts/render_mermaid_diagrams.py`
- `python3 scripts/generate_page_provenance.py`
- `python3 scripts/build_asset_manifest.py --write`
- `python3 scripts/run_curator.py --write`
- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run validate:provenance`
- `npm run validate:comprehension`
- `npm run build`
- `git diff --check`

## Browser QA

Static server: `http://127.0.0.1:4322`

Desktop and mobile checks passed for both routes:

- HTTP 200
- No console errors or warnings
- No horizontal overflow
- No `/Volumes/P-SSD` or `/Users/` local path leakage
- New explorer route includes `RT-20260614-247`, `handoff-0280`, 416 registry
  rows, allowed/forbidden language, and internal route links
- New explorer route includes 14 pinned upstream source links
- Source-authority landing links internally to the explorer

Screenshots:

- `output/playwright/sitewide-revamp-pg005-claim-boundary-explorer-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg005-claim-boundary-explorer-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg005-source-authority-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg005-source-authority-static-mobile-2026-06-28.png`

## Known Full-Validate Blocker

The known release blocker remains ontology TeX/PDF critical source drift in
`npm run validate` through `validate:curator`. This packet did not repair or
reimport ontology assets.

## Conclusion

PG-005 acceptance criteria are satisfied:

- Readers can distinguish allowed explanation from forbidden promotion.
- Registry-derived data has manifest and provenance coverage.
- Source-authority landing links to the explorer internally.
