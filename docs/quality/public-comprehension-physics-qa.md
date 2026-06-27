# Public Comprehension Physics QA

Date: 2026-06-27

## Scope

Physics route-family remediation covered:

- `/project/physics/`
- `/project/physics/ontology/`
- `/project/physics/exact-gr-benchmark/`
- `/project/physics/gr-derivation-roadmap/`
- `/project/physics/claim-gates/`
- `/project/physics/current-state/`

## Evidence

Representative screenshots were captured under:

- `output/playwright/public-comprehension-sitewide/physics-roadmap-desktop.png`
- `output/playwright/public-comprehension-sitewide/physics-roadmap-mobile.png`

The roadmap page was selected as the representative high-risk physics surface because it contains the densest claim-boundary language around source ontology, `g_eff`, matter coupling, Einstein equations, freeze labels, and benchmark promotion.

## Commands

- `npm run validate:comprehension` passed.
- `npm run quality` passed.
- `.venv/bin/python -m pytest` passed with 41 tests.
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321` passed for 68 routes.

## Human Review Status

Human review status: pending maintainer review.

Scripted validation confirms dossier, diagram, manifest, route-wiring, and source-boundary structure. It does not prove that public readers understand the physics route family.

## Remaining Risk

The primary residual risk is reader interpretation. The pages now visibly separate ontology, exact-GR benchmark boundary, derivation burden, claim gates, scoped obstruction/freeze records, and current-state snapshot limits, but a maintainer should still review the prose for overclaim drift before release signoff.
