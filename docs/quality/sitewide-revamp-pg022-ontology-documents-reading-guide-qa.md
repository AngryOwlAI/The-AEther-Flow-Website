# Sitewide Revamp PG-022 Ontology Documents Reading Guide QA

Date: 2026-06-28.

## Scope

Route reviewed:

- `/resources/documents/`

Implementation packet: PG-022, ontology document library with public reading
guide.

## Changes reviewed

- Added system analysis:
  `docs/system-analyses/ontology-document-library-reading-guide.md`.
- Revised `src/pages/resources/documents.astro` with:
  - "read this first" internal route path;
  - specialist reading order;
  - source-status guide;
  - status copy that distinguishes website copies from current upstream source
    review.
- Revised `src/components/DocumentActions.astro` so document cards expose
  reading order, PDF derivative role, TeX authority, claim status, research
  status, ontology promotion status, source commit, import date, and hashes.
- Revised `src/lib/supportComprehensionContent.ts` to include source-commit
  and source-drift boundaries.
- Updated the dossier:
  `docs/content-dossiers/resources-documents/dossier.md`.
- Added `registries/PDF_DERIVATIVE_REGISTRY.csv` to the page route map and
  regenerated `public/files/manifests/page_provenance.json`.

## Boundary review

Pass. The page now states:

- registered TeX is the source-inspection target for its registered version;
- PDFs are human-readable derivatives;
- website copies have source commits, hashes, and import dates;
- release readiness still depends on curator source-drift review;
- the reading order is a reader aid, not a new scientific dependency proof;
- the ontology package does not prove the broader first-principles GR
  derivation is solved.

## Command validation

Passed:

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
- `python3 scripts/run_curator.py --write`

Known release blocker:

- `npm run validate:curator` fails only on the known 16 critical ontology
  TeX/PDF source-drift records. This PG-022 page does not resolve that blocker;
  it makes source-commit/source-drift status visible to readers and maintainers.

## Browser QA

Tool: Playwright skill wrapper.

Automated browser checks:

- desktop viewport: `1440x1500`;
- mobile viewport: `390x1200`;
- screenshots captured as full-page PNGs;
- `scrollWidth === clientWidth` at both viewports;
- no horizontal overflow elements were reported;
- no unloaded images were reported;
- DOM check confirmed one `h1#documents-title` and eight document cards.

Screenshots:

- `output/playwright/sitewide-revamp-pg022-documents-reading-guide-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg022-documents-reading-guide-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg022-documents-reading-guide-mobile-bottom-2026-06-28.png`

Visual spot checks:

- desktop full-page screenshot;
- mobile full-page screenshot;
- mobile bottom viewport focused on the final document card, long hashes, and
  footer.

Result: acceptable. Long source hashes wrap inside document cards, status
labels are visible, and no overlap or blank diagram was observed.

## Remaining uncertainty

The page is now honest about source status, but the known ontology source-drift
blocker remains unresolved. Release readiness still requires re-importing or
reviewing the approved ontology TeX/PDF assets.

## Conclusion

PG-022 route implementation is complete subject to the global ontology
source-drift release blocker.
