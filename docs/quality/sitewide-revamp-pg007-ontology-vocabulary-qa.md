# PG-007 Ontology Vocabulary QA

Date: 2026-06-28

## Scope

Implemented Task PG-007 from
`ImplementationPlans/sitewide_page_revamp_task_packets.md`.

Route reviewed:

- `/project/physics/ontology/`

## Changes Checked

- Added required analysis:
  `docs/system-analyses/aether-flow-ontology-vocabulary.md`.
- Rewrote the ontology route as a public-first vocabulary page:
  - AEther
  - AEther-flow
  - observed space
  - S-time
  - observed expansion
  - gravity-as-reorganization language
- Added a specialist source-status layer:
  - registered TeX
  - PDF derivatives
  - Markdown ontology notes
  - generated explainers
  - claim boundaries
  - open derivation burdens
- Updated the route dossier, shared comprehension terms, source notice refs,
  route map, page provenance, and curator reports.

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

Desktop and mobile checks passed for `/project/physics/ontology/`:

- HTTP 200
- No console errors or warnings
- No horizontal overflow
- No `/Volumes/P-SSD` or `/Users/` local path leakage
- Page includes public vocabulary terms, observed expansion, gravity-language
  boundary, specialist source status, registered TeX, PDF derivatives,
  Distance-to-GR, claim-boundary links, and explicit no-accepted-GR-derivation
  language.

Screenshots:

- `output/playwright/sitewide-revamp-pg007-ontology-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg007-ontology-static-mobile-2026-06-28.png`

## Known Full-Validate Blocker

The known release blocker remains ontology TeX/PDF critical source drift in
`npm run validate` through `validate:curator`. This packet did not repair or
reimport ontology assets.

## Conclusion

PG-007 acceptance criteria are satisfied:

- Public layer defines vocabulary without overclaiming.
- Specialist layer names the relevant ontology source basis.
- Dossier identifies safe and unsafe summaries.
