# Sitewide Revamp PG-023 Diagram Gallery By Concept QA

Date: 2026-06-28.

## Scope

Route reviewed:

- `/resources/diagrams/`

Implementation packet: PG-023, visual diagram gallery grouped by concept.

## Changes reviewed

- Added system analysis:
  `docs/system-analyses/visual-diagram-gallery-by-concept.md`.
- Added concept group metadata and additional approved manifest-backed diagram
  entries in `src/lib/siteContent.ts`.
- Revised `src/pages/resources/diagrams.astro` so figures render under:
  - physics concepts;
  - AI workflow concepts;
  - operations concepts;
  - source authority concepts.
- Revised `src/lib/supportComprehensionContent.ts` so the comprehension block
  describes concept grouping and diagram non-authority.
- Updated `docs/content-dossiers/resources-diagrams/dossier.md`.
- Repaired the duplicated `description` prop on the route's `DownloadList`.

## Boundary review

Pass. The page now states and preserves:

- diagrams are public comprehension aids, not source authority;
- concept groups organize navigation and do not change claim status;
- public figures are static PNGs generated from tracked Mermaid sources;
- no browser-side Mermaid runtime is introduced;
- each grouped figure carries alt text, caption, and provenance.

## Command validation

Passed:

- `python3 scripts/generate_page_provenance.py`
- `npm run validate:comprehension`
- `npm run validate:manifests`
- `npm run validate:provenance`
- `npm run validate:svg`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `git diff --check`
- `npm run build`
- `python3 scripts/run_curator.py --write`

Known release blocker:

- `npm run validate:curator` fails only on the known 16 critical ontology
  TeX/PDF source-drift records. No PG-023 diagram-gallery issue was reported.

## Browser QA

Tool: Playwright skill wrapper.

Automated browser checks:

- desktop viewport: `1440x1500`;
- mobile viewport: `390x1200`;
- screenshots captured as full-page PNGs;
- `scrollWidth === clientWidth` at both viewports;
- 36 figures and 36 images were present;
- all four concept groups were present in the DOM;
- no horizontal overflow elements were reported;
- no unloaded images were reported.

Screenshots:

- `output/playwright/sitewide-revamp-pg023-diagram-gallery-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg023-diagram-gallery-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg023-diagram-gallery-mobile-operations-crop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg023-diagram-gallery-mobile-source-authority-crop-2026-06-28.png`

Visual spot checks:

- desktop full-page screenshot;
- mobile full-page screenshot;
- mobile operations group crop;
- mobile source-authority group crop.

Result: acceptable. Long provenance text wraps inside figure cards, grouped
headings are visible, images load, and the page reads as a concept gallery
rather than a raw asset list.

## Remaining uncertainty

This QA does not resolve the known ontology TeX/PDF source-drift blocker. It
also does not create or regenerate diagram assets; PG-023 intentionally reuses
existing manifest-backed static PNGs.

## Conclusion

PG-023 route implementation is complete subject to the global ontology
source-drift release blocker.
