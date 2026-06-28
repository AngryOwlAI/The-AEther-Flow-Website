# Home Overview Fusion QA

Date: 2026-06-28.

## Scope

Fused the former Start and Overview surfaces into canonical Home at `/`.
`/project/overview/` is retired as a duplicate content route and redirects to
`/`.

## Changes Reviewed

- Home H1 is `The Æther Flow Project`.
- Home uses the former Overview animated SVG hero.
- The first post-hero section is `Two first-class tracks`.
- The visible `Public comprehension` block is not rendered on Home.
- Primary navigation has one `Home` item and no separate `Overview` item.
- Page route/provenance manifests publish 37 content routes.
- The former overview public-comprehension dossier and diagram contract are
  owned by `/`.

## Verification

Passed:

- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run validate:provenance`
- `npm run validate:cloudflare`
- `npm run validate:comprehension`
- `npm run build`
- `python3 scripts/quality_gate.py`
- `.venv/bin/python -m pytest` (`46 passed`)
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4322 --root .`

Browser QA passed on local preview at `http://127.0.0.1:4322/`:

- Desktop screenshot: `output/playwright/home-fusion-desktop-2026-06-28.png`.
- Mobile screenshot: `output/playwright/home-fusion-mobile-2026-06-28.png`.
- Desktop and mobile HTML title and H1 rendered as
  `The Æther Flow Project`.
- First post-hero eyebrow rendered as `TWO FIRST-CLASS TRACKS`.
- `Public comprehension` visible-text count was `0`.
- Hero SVG was visible at desktop and mobile widths.
- Mobile horizontal overflow was `0px`.
- `/project/overview/` local Astro meta redirect reached `/`; Cloudflare
  `_redirects` records `/project/overview/ / 301`.

Known blocker:

- `npm run validate` and `npm run quality` still fail only at
  `validate:curator` because of the known 16 ontology TeX/PDF source-drift
  records.

## References

The AEther Flow Website. (2026). `src/pages/index.astro`.

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`.

The AEther Flow Website. (2026). `public/_redirects`.
