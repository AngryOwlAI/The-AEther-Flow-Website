# Sitewide Revamp PG-002 Distance-To-GR QA

Date: 2026-06-28

## Scope

Implemented PG-002:
`/project/physics/distance-to-gr/`.

Files and surfaces added or updated:

- `docs/system-analyses/distance-to-gr-dashboard.md`
- `docs/content-dossiers/physics-distance-to-gr/dossier.md`
- `docs/content-dossiers/physics-distance-to-gr/diagrams/distance-dashboard-boundary.mmd`
- `public/assets/diagrams/comprehension/physics-distance-to-gr-dashboard.png`
- `scripts/refresh_distance_to_gr_snapshot.py`
- `src/data/distance_to_gr_snapshot.json`
- `src/pages/project/physics/distance-to-gr/index.astro`
- `src/lib/siteContent.ts`
- `src/pages/index.astro`
- `src/pages/project/physics/index.astro`
- `scripts/render_mermaid_diagrams.py`
- `scripts/validate_public_comprehension.py`
- `scripts/validate_page_provenance.py`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `public/files/manifests/page_provenance.json`

## Source-State Finding

The upstream source repository was clean at
`4d249ba24ead51445e496a74b2f6072149bc7609` when the dashboard snapshot was
generated. The snapshot includes 14 Distance-to-GR ledger rows and current
control state `RT-20260614-247` / `handoff-0280`.

The dashboard states that it is a burden map, not proof, live source authority,
or percentage progress. It preserves no `MetricData(E)` adoption, no `g_eff`
scope change, no coupling-law adoption, no matter-coupling derivation or
adoption, no stress-energy semantics, no Einstein equations, no benchmark
promotion, no Gate Chair verdict, and no completed derivation.

## Browser QA Evidence

Captured against static build preview:
`http://127.0.0.1:4322/project/physics/distance-to-gr/`.

- `output/playwright/sitewide-revamp-pg002-distance-to-gr-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg002-distance-to-gr-static-mobile-2026-06-28.png`

Browser QA result:

- Desktop and mobile rendered the new route from built `dist/` output.
- No console errors or warnings were observed.
- No horizontal overflow was detected after wrapping long evidence paths.
- No absolute local filesystem paths were visible in page text.
- The page included `handoff-0280`, the 14-row snapshot count, `matter_coupling`
  burden text, and non-proof language.
- The page exposed 16 pinned upstream links to
  `4d249ba24ead51445e496a74b2f6072149bc7609`.

## Validation

Passed:

- `git diff --check`
- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run validate:provenance`
- `npm run validate:comprehension`
- `npm run build`

Aggregate status:

- `npm run validate:curator` reports only critical ontology TeX/PDF source
  drift outside PG-002.
- `npm run validate` remains blocked at `validate:curator` for those ontology
  asset drift findings.

## No-AI-Slop Gate

PG-002 route: `pass`.

Reasoning: the dashboard starts from the reader problem, uses a checked-in
source-pinned snapshot, rejects progress-bar proof, groups all ledger rows
without promoting downstream claims, and keeps source links as provenance.

Release gate: `block` until the known ontology TeX/PDF source-drift issue is
handled by a dedicated source asset or curator packet.

## Human Review Status

Human review status: technical validation passed; maintainer review recommended
before release because the route is claim-boundary-sensitive.
