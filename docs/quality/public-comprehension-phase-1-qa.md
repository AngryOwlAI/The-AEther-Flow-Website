# Public Comprehension Phase 1 QA

Status: Phase 1 implementation QA complete; maintainer comprehension review pending.
Date: 2026-06-27

## Scope

Routes reviewed:

- `/project/overview/`
- `/project/ai-research-agent-system/parent-child-synthesis/`

Implemented Phase 1 surfaces:

- content dossier template and workflow notes,
- pilot dossiers for both routes,
- reusable comprehension content model and renderer,
- static Mermaid-to-PNG diagram assets,
- public comprehension audit command,
- page provenance and asset manifest refresh,
- desktop and mobile screenshot evidence.

## Commands run

```bash
python3 scripts/render_mermaid_diagrams.py
python3 scripts/build_asset_manifest.py --write
npm run build
python3 scripts/generate_page_provenance.py
npm run validate:comprehension
npm run validate:manifests
npm run validate:content
npm run validate:links
npm run validate:layout
npm run validate:svg
npm run validate:provenance
python3 scripts/run_curator.py --write
python3 scripts/run_curator.py --check
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
.venv/bin/python -m pytest
npm run validate
npm run quality
```

Known command adjustment:

- The implementation plan listed `python3 scripts/generate_page_provenance.py
  --write`, but the checked-in script writes by default and does not accept
  `--write`. The actual command used was `python3
  scripts/generate_page_provenance.py`.
- The system `python3 -m pytest` did not have `pytest` installed. The repo-local
  virtual environment was used instead: `.venv/bin/python -m pytest`.
- The first full `npm run validate` detected stale curator reports. The reports
  were refreshed with `python3 scripts/run_curator.py --write`, after which
  `npm run validate` and `npm run quality` passed.

## Screenshot evidence

Viewport screenshots from the Playwright CLI wrapper:

- `output/playwright/public-comprehension-phase-1/overview-desktop.png`
- `output/playwright/public-comprehension-phase-1/overview-mobile.png`
- `output/playwright/public-comprehension-phase-1/parent-child-desktop.png`
- `output/playwright/public-comprehension-phase-1/parent-child-mobile.png`

Full-page screenshots from Playwright's direct screenshot command:

- `output/playwright/public-comprehension-phase-1/overview-desktop-full.png`
- `output/playwright/public-comprehension-phase-1/overview-mobile-full.png`
- `output/playwright/public-comprehension-phase-1/parent-child-desktop-full.png`
- `output/playwright/public-comprehension-phase-1/parent-child-mobile-full.png`

The Playwright wrapper captured viewport screenshots and reported zero console
errors for the pilot routes. The wrapper's `run-code` command did not accept
top-level `await` in this local install, so full-page screenshots were captured
with `npx playwright screenshot --full-page`.

## Human review status

Human review status: pending maintainer review.

Automated checks and visual inspection show the pilot routes render, include
the new static diagrams, preserve source-boundary language, and avoid visible
mobile overlap in the captured screenshots. This QA note does not claim final
human comprehension acceptance.

## Remaining risks

- Mermaid PNG text is readable on desktop and supported by alt text, caption,
  and nearby prose on mobile; a later pass could add zoom/open-image behavior if
  maintainers want easier mobile diagram inspection.
- The comprehension audit is deliberately mechanical. It confirms dossiers,
  diagram metadata, manifests, source-boundary markers, and human-review
  status, but it cannot prove reader understanding.
- Phase 2 route-family remediation remains larger than the Phase 1 pilot and
  should continue dossier-first.

## Phase 2 readiness

Phase 2 is ready to begin only as a follow-on packet. The logical next step is
to remediate the physics route family in overclaim-risk order, beginning with a
physics landing-page dossier and preserving the open GR-derivation boundary.

## References

The AEther Flow Website. (2026). `AGENTS.md` [Repository operating rules].

The AEther Flow Website. (2026).
`ImplementationPlans/public_comprehension_and_diagram_system_task_packets.md`
[Implementation task packets].
