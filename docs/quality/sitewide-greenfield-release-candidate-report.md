# Sitewide Greenfield Release-Candidate QA Report

Status: release-candidate QA completed with remaining blockers.
Date: 2026-06-30.
Packet: GF-014, `WI-20260630-042`.

## Conclusion

The rebuilt greenfield route set is technically present and browser-smoke
healthy, but it is not release-ready. Deployment is not authorized.

Owner review remains pending for all rebuilt routes. Full `npm run quality`
does not pass under the current source-drift and quality-gate state.

## Owner Review State

Owner acceptance: not granted.
Deployment readiness: not granted.
Feedback queue: no owner-requested changes yet. The Diagram Gallery
quality-gate contract blocker was resolved in packet `WI-20260630-043`;
curator/source drift remains open.

## Route Set For Review

All 29 rebuilt routes are `technically ready` and `human review pending` in
`docs/quality/sitewide-greenfield-review-ledger.md`.

| Family | Routes |
| --- | --- |
| Home | `/` |
| Physics Research | `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/` |
| AI Research System | `/ai-research-system/`, `/ai-research-system/current-state/`, `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`, `/ai-research-system/validators-and-handoffs/`, `/ai-research-system/memory-preflight/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/runtime-requirements/` |
| Resources | `/resources/`, `/resources/source-authority/`, `/resources/registries/`, `/resources/generated-derivatives/`, `/resources/retrieval-layers/`, `/resources/publication-process/`, `/resources/library/`, `/resources/reading-paths/`, `/resources/repository-map/`, `/resources/site-builder-guide/`, `/resources/diagrams/` |

## Validation Evidence

Passed:

- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run validate:provenance`
- `npm run validate:cloudflare`
- `npm run validate:implementation-control`
- `npm run build`: 64 static pages built.
- `.venv/bin/python -m pytest`: 75 passed.
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`: 92 routes passed.
- Browser QA: Home, Physics, AI Research System, Resources, and Diagram Gallery returned HTTP 200 on desktop and mobile, exposed expected `h1` text, and showed no document-level horizontal overflow.
- `python3 scripts/quality_gate.py`: passed after `WI-20260630-043` updated the quality gate to validate `/resources/diagrams/` against the greenfield Diagram Gallery contract while keeping `/resources/documents/` on the support-page schema.

Failed or blocked:

- `npm run quality` failed because `npm run validate` fails at `npm run validate:curator`.
- `npm run validate:curator` reports stale checked-in curator reports and source-drift acknowledgement failures. Concrete records include `curator/reports/latest.json`, `curator/reports/latest.md`, review-required drift for `registries/CLAIM_BOUNDARY_REGISTRY.csv` across multiple greenfield routes, and critical drift on `/project/physics/current-state/` for `registries/CLAIM_BOUNDARY_REGISTRY.csv`, `registries/DISTANCE_TO_GR_LEDGER.csv`, and `research_control/program_state.yaml`.

## Browser QA Artifacts

Screenshots were captured under ignored local QA output:

- `output/playwright/gf014-home-desktop-2026-06-30.png`
- `output/playwright/gf014-physics-desktop-2026-06-30.png`
- `output/playwright/gf014-ai-research-system-desktop-2026-06-30.png`
- `output/playwright/gf014-resources-desktop-2026-06-30.png`
- `output/playwright/gf014-diagrams-desktop-2026-06-30.png`
- `output/playwright/gf014-home-mobile-2026-06-30.png`
- `output/playwright/gf014-physics-mobile-2026-06-30.png`
- `output/playwright/gf014-ai-research-system-mobile-2026-06-30.png`
- `output/playwright/gf014-resources-mobile-2026-06-30.png`
- `output/playwright/gf014-diagrams-mobile-2026-06-30.png`

## Residual Risk

- Owner review has not accepted the rebuilt route set.
- Curator/source-drift policy prevents a green full validate or quality result.
- Old `/project/*` source files remain in the build for validator continuity even though the public route/provenance manifests now expose the short-route inventory.

## Recommendation

Do not deploy. Do not mark the rebuild accepted.

The logical next step is a bounded packet for curator/source-drift
acknowledgement and stale curator reports. After that blocker is resolved,
rerun `npm run validate`, `npm run quality`, Python tests, smoke testing, and
owner review. Deployment remains a separate explicit request.

## References

The AEther Flow Website. (2026). *Implementation Plan: Sitewide Greenfield
Rebuild* [Implementation plan].

The AEther Flow Website. (2026). *Sitewide Greenfield Review Ledger* [Quality
ledger].

The AEther Flow Website. (2026). *Sitewide Greenfield Rebuild Task Packets*
[Implementation task packets].
