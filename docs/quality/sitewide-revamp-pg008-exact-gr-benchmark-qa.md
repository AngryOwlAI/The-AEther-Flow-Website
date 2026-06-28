# PG-008 Exact-GR Benchmark QA

Date: 2026-06-28

## Scope

Implemented Task PG-008 from
`ImplementationPlans/sitewide_page_revamp_task_packets.md`.

Route reviewed:

- `/project/physics/exact-gr-benchmark/`

## Changes Checked

- Added required analysis:
  `docs/system-analyses/exact-gr-benchmark-versus-derivation.md`.
- Rewrote the route around the public contrast between:
  - matching or using the exact-GR benchmark;
  - deriving the benchmark from source ontology;
  - promoting the benchmark through protected authority.
- Added specialist source layer for the burden map, Distance-to-GR ledger,
  TeX registry, and claim-boundary registry.
- Added internal links to current state, Distance-to-GR, ontology, and the
  claim-boundary explorer.
- Updated dossier, shared comprehension data, source notice refs, route map,
  page provenance, and curator reports.

## Focused Validation

Passed:

- `python3 scripts/generate_page_provenance.py`
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

Desktop and mobile checks passed for `/project/physics/exact-gr-benchmark/`:

- HTTP 200
- No console errors or warnings
- No horizontal overflow
- No `/Volumes/P-SSD` or `/Users/` local path leakage
- Page includes the benchmark-versus-derivation contrast, specialist source
  layer, Distance-to-GR link, current-state link, claim-boundary explorer link,
  and explicit no-proof/no-promotion boundary language.

Screenshots:

- `output/playwright/sitewide-revamp-pg008-exact-gr-benchmark-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg008-exact-gr-benchmark-static-mobile-2026-06-28.png`

## Known Full-Validate Blocker

The known release blocker remains ontology TeX/PDF critical source drift in
`npm run validate` through `validate:curator`. This packet did not repair or
reimport ontology assets.

## Conclusion

PG-008 acceptance criteria are satisfied:

- The page prevents readers from confusing benchmark target with proven
  derivation.
- Specialist section identifies relevant source records and limitations.
- Related routes guide readers internally.
