# Sitewide Revamp PG-021 Remaining Operations Family QA

Date: 2026-06-28.

## Scope

Routes reviewed:

- `/project/operations/`
- `/project/operations/director-agentjob-lifecycle/`
- `/project/operations/role-routing/`
- `/project/operations/publication-process/`
- `/project/operations/technical-requirements/`

Implementation packet: PG-021, remaining operations route family.

## Changes reviewed

- Added route-family audit:
  `docs/system-analyses/remaining-operations-route-family.md`.
- Expanded committed upstream source basis in
  `public/files/manifests/page_route_map.json` for the operations landing and
  four remaining operation child routes.
- Regenerated `public/files/manifests/page_provenance.json`.
- Updated operation page content in `src/lib/internalExplainers.ts` with
  refreshed source references, provenance links, and anti-overread cards.
- Updated the five route dossiers with PG-021 evidence-review notes and
  route-specific source bases.

## Boundary review

Pass. The route family remains explanatory only:

- no operation page changes execution contracts;
- no operation page changes validators, roles, schemas, registries, or command
  semantics;
- no operation page implies operational success is scientific proof;
- no completion, role label, publication review, or working tool is presented
  as live authorization or claim promotion.

## Command validation

Passed:

- `python3 scripts/generate_page_provenance.py`
- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:provenance`
- `npm run validate:comprehension`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `git diff --check`
- `npm run build`
- `python3 scripts/run_curator.py --write`

Known release blocker:

- `npm run validate:curator` fails only on the pre-existing 16 critical
  ontology TeX/PDF source-drift records. No PG-021 operations-family issue was
  reported by the curator check.

## Browser QA

Tool: Playwright skill wrapper.

Automated browser checks:

- desktop viewport: `1440x1400`;
- mobile viewport: `390x1200`;
- all five routes captured as full-page screenshots;
- all five routes reported `scrollWidth === clientWidth`;
- no horizontal overflow elements were reported;
- no unloaded images were reported.

Screenshots:

- `output/playwright/sitewide-revamp-pg021-operations-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-operations-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-director-agentjob-lifecycle-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-director-agentjob-lifecycle-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-role-routing-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-role-routing-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-publication-process-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-publication-process-static-mobile-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-technical-requirements-static-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-pg021-technical-requirements-static-mobile-2026-06-28.png`

Visual spot checks:

- operations landing desktop and mobile;
- publication-process mobile;
- technical-requirements mobile.

Result: acceptable. Long source-provenance lists wrap within the source notice,
comprehension diagrams load, and the route family reads as one coherent
operations system.

## Remaining uncertainty

This QA does not resolve the known ontology TeX/PDF source drift. It also does
not inspect every historical operation record. It verifies the PG-021
reader-facing route family against the current committed source basis and
rendered static build.

## Conclusion

PG-021 route-family implementation is complete subject to the global
pre-existing ontology source-drift release blocker.
