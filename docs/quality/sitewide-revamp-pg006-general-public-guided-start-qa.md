# PG-006 General-Public Guided Start QA

Date: 2026-06-28

## Scope

Implemented Task PG-006 from
`ImplementationPlans/sitewide_page_revamp_task_packets.md`.

Routes reviewed:

- `/resources/guided-starts/general-public/`
- `/resources/`
- `/`

## Changes Checked

- Added general-public guided-start route:
  `src/pages/resources/guided-starts/general-public/index.astro`.
- Added dossier and diagram source:
  - `docs/content-dossiers/guided-start-general-public/dossier.md`
  - `docs/content-dossiers/guided-start-general-public/diagrams/general-public-guided-start.mmd`
- Added public diagram:
  `/assets/diagrams/comprehension/general-public-guided-start.png`.
- Linked the route from homepage, resources, and library navigation.
- Updated route map, page provenance, source manifest, asset manifest,
  public-comprehension validator, page-provenance validator, and diagram
  renderer.

## Focused Validation

Passed:

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

Desktop and mobile checks passed:

- HTTP 200
- No console errors or warnings
- No horizontal overflow
- No `/Volumes/P-SSD` or `/Users/` local path leakage
- Guided-start route includes the three required reader questions:
  "what is this?", "what is currently claimed?", and "what should I not
  infer?"
- Guided-start route points to internal pages first.
- Homepage and resources landing link to the guided start.

Screenshots:

- `output/playwright/sitewide-revamp-pg006-general-public-guided-start-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg006-general-public-guided-start-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg006-resources-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg006-resources-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg006-home-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg006-home-static-mobile-2026-06-28.png`

## Known Full-Validate Blocker

The known release blocker remains ontology TeX/PDF critical source drift in
`npm run validate` through `validate:curator`. This packet did not repair or
reimport ontology assets.

## Conclusion

PG-006 acceptance criteria are satisfied:

- A public reader gets a clear first reading path.
- The route points to internal pages first.
- No new scientific claims are introduced.
