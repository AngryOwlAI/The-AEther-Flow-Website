# RT-001 Prototype Route Retirement

Status: prototype routes retired from the public Astro route tree.
Date: 2026-06-28.

## Scope

Retired prototype routes:

- `/research/map/`
- `/research/equations/`
- `/research/math-sample/`

Replacement internal routes:

- `/research` and `/research/map/` redirect to
  `/project/source-authority/publication-and-provenance-system/`.
- `/equations`, `/research/equations/`, and `/research/math-sample/` redirect
  to `/resources/documents/`.

## Reasoning

The retired routes were prototype support surfaces:

- `/research/map/` duplicated the now first-class publication/provenance
  system route.
- `/research/equations/` and `/research/math-sample/` were KaTeX rendering
  fixtures, not inventory-backed public reader pages.

The public site should no longer expose sample/demo routes as finished
reader-facing pages.

## Files changed

- Removed `src/pages/research/map.astro`.
- Removed `src/pages/research/equations.mdx`.
- Removed `src/pages/research/math-sample.mdx`.
- Updated `public/_redirects`.
- Updated `scripts/quality_gate.py`.
- Updated `scripts/smoke_test_site.py`.
- Removed the now-unused `researchMapNodes` content from `src/lib/siteContent.ts`.

## Internal-link search

Search command:

- `rg -n "/research/(map|equations|math-sample)|research/map|research/equations|research/math-sample|Research Map|Math Sample|Equations" src public docs scripts -S`

Result:

- No ordinary reader-page internal links depended on the retired routes.
- Remaining references were quality, smoke, redirect, audit, and source-word
  occurrences; quality, smoke, and redirects were updated.

## Validation

Passed:

- `npm run validate:links`
- `npm run validate:provenance`
- `npm run validate:content`
- `git diff --check`
- `npm run build`
- `python3 scripts/quality_gate.py`
- `npm run validate:cloudflare`
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4322 --root .`
- `python3 scripts/run_curator.py --write`

Known non-RT-001 blocker:

- `npm run validate:curator` fails only on the previously known 16 ontology
  TeX/PDF critical source-drift records. No RT-001 curator error was observed.

## Browser QA

Replacement-route screenshots:

- `output/playwright/sitewide-revamp-rt001-replacement-publication-provenance-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-rt001-replacement-publication-provenance-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-rt001-replacement-documents-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-rt001-replacement-documents-static-mobile-2026-06-28.png`

Observed metrics:

- `/project/source-authority/publication-and-provenance-system/`: one H1,
  two loaded images, visible source notice, no horizontal overflow on desktop
  or mobile.
- `/resources/documents/`: one H1, two loaded images, visible source notice,
  no horizontal overflow on desktop or mobile.
- Retired route outputs are absent from `dist/research/`.

## References

The AEther Flow Website. (2026). `docs/architecture/website-feature-and-functionality.md`.

The AEther Flow Website. (2026). `ImplementationPlans/sitewide_page_revamp_task_packets.md`.
