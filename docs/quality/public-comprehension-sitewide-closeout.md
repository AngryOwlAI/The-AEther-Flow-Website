# Public Comprehension Sitewide Closeout

Date: 2026-06-27

## Routes Remediated

Pilot routes:

- `/project/overview/`
- `/project/ai-research-agent-system/parent-child-synthesis/`

Physics routes:

- `/project/physics/`
- `/project/physics/ontology/`
- `/project/physics/exact-gr-benchmark/`
- `/project/physics/gr-derivation-roadmap/`
- `/project/physics/claim-gates/`
- `/project/physics/current-state/`

AI research-agent routes:

- `/project/ai-research-agent-system/`
- `/project/ai-research-agent-system/workflow/`
- `/project/ai-research-agent-system/roles-and-skills/`
- `/project/ai-research-agent-system/memory-registries/`

Operations routes:

- `/project/operations/`
- `/project/operations/director-agentjob-lifecycle/`
- `/project/operations/role-routing/`
- `/project/operations/validator-operator-workflow/`
- `/project/operations/publication-process/`
- `/project/operations/project-system-improvement/`
- `/project/operations/technical-requirements/`

Supporting surfaces:

- `/project/source-authority/`
- `/resources/`
- `/resources/documents/`
- `/resources/diagrams/`

## Retired Prototype Routes

RT-001 retired the secondary research prototype routes from the public Astro
route tree:

- `/research/equations/`
- `/research/map/`
- `/research/math-sample/`

Replacement routes:

- `/research` and `/research/map/` redirect to
  `/project/source-authority/publication-and-provenance-system/`.
- `/equations`, `/research/equations/`, and `/research/math-sample/` redirect
  to `/resources/documents/`.

Decision: remove sample/demo routes from public exposure rather than promote
them into the primary reader journey.

## Evidence

Representative desktop and mobile screenshots were captured under:

- `output/playwright/public-comprehension-sitewide/project-overview-desktop.png`
- `output/playwright/public-comprehension-sitewide/project-overview-mobile.png`
- `output/playwright/public-comprehension-sitewide/physics-roadmap-desktop.png`
- `output/playwright/public-comprehension-sitewide/physics-roadmap-mobile.png`
- `output/playwright/public-comprehension-sitewide/ai-workflow-desktop.png`
- `output/playwright/public-comprehension-sitewide/ai-workflow-mobile.png`
- `output/playwright/public-comprehension-sitewide/operations-validator-desktop.png`
- `output/playwright/public-comprehension-sitewide/operations-validator-mobile.png`
- `output/playwright/public-comprehension-sitewide/source-authority-desktop.png`
- `output/playwright/public-comprehension-sitewide/source-authority-mobile.png`
- `output/playwright/public-comprehension-sitewide/resources-diagrams-desktop.png`
- `output/playwright/public-comprehension-sitewide/resources-diagrams-mobile.png`

Visual review notes:

- Static PNG comprehension diagrams rendered on desktop and mobile.
- The diagram gallery was adjusted so visible gallery examples use static PNG diagrams rather than the legacy SVG fixture.
- Gallery examples were set to eager loading so full-page browser QA captures nonblank images.
- No obvious overlap or button text overflow was observed in the inspected representative screenshots.

## Commands

- `python3 scripts/render_mermaid_diagrams.py` passed and rendered 23 static diagram targets.
- `python3 scripts/build_asset_manifest.py --write` regenerated `public/files/manifests/asset_manifest.json`.
- `python3 scripts/generate_page_provenance.py` regenerated `public/files/manifests/page_provenance.json`.
- `python3 scripts/run_curator.py --write` refreshed curator reports.
- `npm run validate:comprehension` passed.
- `npm run quality` passed.
- `.venv/bin/python -m pytest` passed with 41 tests.
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321` passed for 68 routes.

## Human Review Status

Human review status: pending maintainer review.

The scripted audit requires dossiers, diagrams, manifests, route wiring, no public Mermaid runtime markers, safe/unsafe summaries, and quality-note presence. It does not replace human public-comprehension review.

## Deployment Status

No deployment was performed. Deployment remains out of scope until separately authorized.

## Remaining Backlog

- Maintainer public-comprehension signoff for the remediated route set.
- Optional future audit for secondary `/research/**` routes if they become primary reader surfaces.
- Optional refinement of diagram visual styling if a future review prefers stronger brand consistency for Mermaid-generated PNGs.
