# Sitewide Revamp PG-004 Gate Chair QA

Date: 2026-06-28

## Scope

Implemented PG-004:
`/project/physics/gate-chair-and-human-gates/`.

Files and surfaces added or updated:

- `docs/system-analyses/gate-chair-and-human-gated-decisions.md`
- `docs/content-dossiers/physics-gate-chair-and-human-gates/dossier.md`
- `docs/content-dossiers/physics-gate-chair-and-human-gates/diagrams/human-gate-authority.mmd`
- `public/assets/diagrams/comprehension/physics-gate-chair-human-gates.png`
- `src/pages/project/physics/gate-chair-and-human-gates/index.astro`
- `src/lib/siteContent.ts`
- `scripts/render_mermaid_diagrams.py`
- `scripts/validate_public_comprehension.py`
- `scripts/validate_page_provenance.py`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `public/files/manifests/page_provenance.json`

## Source-State Finding

The upstream source repository was clean at
`4d249ba24ead51445e496a74b2f6072149bc7609` when PG-004 evidence was refreshed.
The page explains Gate Chair and human-gated authority only. It now uses
`handoff-0280` as the current example: a selector routed the draft/control
recovery-bridge candidate to a future narrow Gate Chair
evidence-status/precondition review. It does not issue a Gate Chair verdict,
execute a gate, promote validator PASS as scientific proof, adopt source law,
adopt `MetricData(E)`, change `g_eff` scope, derive matter coupling, derive
Einstein equations, promote a benchmark, or authorize downstream GR claims.

## Browser QA Evidence

Captured against static build preview:
`http://127.0.0.1:4322/project/physics/gate-chair-and-human-gates/`.

- `output/playwright/sitewide-revamp-pg004-gate-chair-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg004-gate-chair-static-mobile-2026-06-28.png`

Browser QA result:

- Desktop and mobile rendered the new route from built `dist/` output.
- No console errors or warnings were observed.
- No horizontal overflow was detected.
- The static comprehension diagram loaded at natural size `1568x464`.
- The SourceNotice showed the June 28 source refresh date after rebuilding.
- The page included future narrow Gate Chair review language and did not
  include stale pending-selector language.
- The page exposed 9 pinned upstream links to
  `4d249ba24ead51445e496a74b2f6072149bc7609`.
- Internal reader-path links were present for source extension, claim gates,
  current state, and source authority.

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

- `npm run validate` passed through manifests, content, links, layout, SVG,
  and provenance, then stopped at `validate:curator`.
- PG-004 does not appear in the final curator errors after repinning to
  `4d249ba24ead51445e496a74b2f6072149bc7609`.
- The known aggregate blocker is critical ontology PDF/TeX source drift.

## No-AI-Slop Gate

PG-004 route: `pass`.

Reasoning: the public copy starts from reader context, distinguishes protected
human-gated authority from readiness signals, preserves internal-first
navigation, and explicitly blocks validator, handoff, role-row, and website
overreads.

Release gate: `block` until the known curator/source-drift issue is handled by
a dedicated source asset or curator packet.

## Human Review Status

Human review status: technical validation passed; maintainer review recommended
before release because the route is claim-boundary-sensitive.
