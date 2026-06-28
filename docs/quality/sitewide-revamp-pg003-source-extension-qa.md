# Sitewide Revamp PG-003 Source Extension QA

Date: 2026-06-27

## Scope

Implemented PG-003:
`/project/physics/source-extension-pipeline/`.

Files and surfaces added or updated:

- `docs/system-analyses/source-extension-pipeline.md`
- `docs/content-dossiers/physics-source-extension-pipeline/dossier.md`
- `docs/content-dossiers/physics-source-extension-pipeline/diagrams/source-extension-pipeline.mmd`
- `public/assets/diagrams/comprehension/physics-source-extension-pipeline.png`
- `src/pages/project/physics/source-extension-pipeline/index.astro`
- `src/lib/siteContent.ts`
- `scripts/render_mermaid_diagrams.py`
- `scripts/validate_public_comprehension.py`
- `scripts/validate_page_provenance.py`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `public/files/manifests/page_provenance.json`

## Source-State Finding

The page explains source-extension workflow, not current adoption state. Dirty
upstream current-state records were not used as public authority for source-law
adoption, `MetricData(E)`, `g_eff`, matter coupling, Einstein equations,
benchmark promotion, or completed derivation.

## Browser QA Evidence

Captured against
`http://127.0.0.1:4321/project/physics/source-extension-pipeline/`:

- `output/playwright/sitewide-revamp-pg003-source-extension-desktop-2026-06-27.png`
- `output/playwright/sitewide-revamp-pg003-source-extension-mobile-2026-06-27.png`

Browser QA result:

- Desktop and mobile rendered the new route.
- No console errors or page errors were observed.
- No horizontal overflow was detected.
- Four internal reader-path links were present.
- The static comprehension diagram rendered.

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

- `npm run validate` passes through manifests, content, links, layout, SVG, and
  provenance, then stops at `validate:curator`.
- The remaining aggregate blocker is the pre-existing stale curator report and
  critical ontology PDF/TeX source drift.

## No-AI-Slop Gate

PG-003 route: `pass`.

Reasoning: the public copy starts from reader context, distinguishes
`proposal-only`, `draft/control`, `source-extension`, stress, selector, and
human-gated states, preserves internal-first navigation, and explicitly blocks
adoption/downstream-GR overreads.

Release gate: `block` until the known curator/source-drift issue is handled by
a dedicated source asset or curator packet.

## Human Review Status

Human review status: technical validation passed; maintainer review recommended
before release because the route is claim-boundary-sensitive.
