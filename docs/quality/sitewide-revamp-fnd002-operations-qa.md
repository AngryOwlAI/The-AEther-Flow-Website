# Sitewide Revamp FND-002 Operations QA

Date: 2026-06-27

## Scope

Advanced the FND-002 site-shell and route-landing work for
`/project/operations/`:

- Added an optional route-grid slot to `InternalExplainerPage`.
- Wired the operations landing to `projectOperationsRoutes` so lifecycle,
  routing, validation, publication, project-system improvement, and technical
  requirements are visible as first-class internal routes.
- Adjusted `track-section-dossier` styling to prevent empty grid-cell
  background artifacts on desktop.
- Regenerated `public/files/manifests/page_provenance.json` after the
  operations page source changed.

## Browser QA Evidence

Captured against `http://127.0.0.1:4321/project/operations/`:

- `output/playwright/sitewide-revamp-operations-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-operations-mobile-2026-06-27.png`

Captured for the FND-002 route set against `http://127.0.0.1:4321`:

- `output/playwright/sitewide-revamp-fnd002-home-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-home-mobile-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-overview-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-overview-mobile-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-physics-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-physics-mobile-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-ai-system-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-ai-system-mobile-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-operations-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-operations-mobile-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-source-authority-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-source-authority-mobile-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-resources-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-fnd002-resources-mobile-2026-06-27.png`

Visual review notes:

- Desktop and mobile render the updated operations route grid without visible
  text overflow or incoherent overlap.
- Six operations route cards are present in both viewports.
- The earlier empty grid-cell background artifact is removed.
- Source links remain in provenance sections; primary route movement remains
  internal-first.
- Automated route-set QA found no console errors, no page errors, and no
  horizontal overflow on `/`, `/project/overview/`, `/project/physics/`,
  `/project/ai-research-agent-system/`, `/project/operations/`,
  `/project/source-authority/`, or `/resources/`.

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

Partial:

- `npm run validate` passes through manifests, content, links, layout, SVG, and
  provenance, then stops at `validate:curator`.

Known curator blocker:

- `curator/reports/latest.json` and `curator/reports/latest.md` are stale.
- Approved ontology PDF and TeX assets report critical source drift.

No curator report rewrite, ontology re-import, push, or deployment was
performed in this packet.

## No-AI-Slop Gate

Operations landing update: `pass`.

Reasoning: the change improves route discoverability, keeps operations as
control evidence rather than science authority, preserves internal-first
navigation, and includes desktop/mobile browser QA.

Curator/source-drift release gate: `block` until handled by a dedicated source
asset/curator packet.
