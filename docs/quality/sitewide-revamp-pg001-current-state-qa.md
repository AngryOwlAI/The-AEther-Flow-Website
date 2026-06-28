# Sitewide Revamp PG-001 Current State QA

Date: 2026-06-28

## Scope

Implemented PG-001 refresh for `/project/physics/current-state/`.

Files and surfaces added or updated:

- `docs/system-analyses/current-research-state-and-next-gate.md`
- `docs/content-dossiers/physics-current-state/dossier.md`
- `src/data/physics_current_state_snapshot.json`
- `src/pages/project/physics/current-state/index.astro`
- `src/lib/comprehensionContent.ts`
- `src/lib/siteContent.ts`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/page_provenance.json`
- `curator/reports/latest.json`
- `curator/reports/latest.md`

## Source-State Finding

The upstream source repository was clean at
`4d249ba24ead51445e496a74b2f6072149bc7609` when the final PG-001 snapshot was
refreshed. The checked-in snapshot now reflects `RT-20260614-247` and
`handoff-0280`.

The active Distance-to-GR burden remains `matter_coupling`. The current status
is `matter_coupling_recovery_bridge_selector_requires_narrow_gate_no_adoption`.
The page states that selector routing to a future narrow Gate Chair
evidence-status/precondition review is not coupling-law adoption,
matter-coupling derivation or adoption, `MetricData(E)` adoption, `g_eff`
scope change, Einstein-equation derivation, benchmark promotion, or completed
derivation.

## Browser QA Evidence

Captured against static build preview:
`http://127.0.0.1:4322/project/physics/current-state/`.

- `output/playwright/sitewide-revamp-pg001-current-state-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg001-current-state-static-mobile-2026-06-28.png`

Browser QA result:

- Desktop and mobile rendered the refreshed route from built `dist/` output.
- No console errors or warnings were observed.
- No horizontal overflow was detected.
- Page text included `handoff-0280`, `RT-20260614-247`, and gate-readiness
  language.
- Page text did not include stale `handoff-0279` or `handoff-0243`.
- The page exposed 13 pinned upstream links to
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

- `npm run validate:curator` now reports only critical ontology TeX/PDF source
  drift outside PG-001.
- `npm run validate` remains blocked at `validate:curator` for those ontology
  asset drift findings.

## No-AI-Slop Gate

PG-001 route: `pass`.

Reasoning: the page starts from public reader context, names current source
state and next action, preserves blocked claims, uses internal-first reading,
and keeps pinned source links as provenance rather than primary explanation.

Release gate: `block` until the known ontology TeX/PDF source-drift issue is
handled by a dedicated source asset or curator packet.

## Human Review Status

Human review status: technical validation passed; maintainer review recommended
before release because the route is claim-boundary-sensitive.
