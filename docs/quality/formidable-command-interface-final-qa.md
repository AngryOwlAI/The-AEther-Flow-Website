# Formidable Command Interface Final QA

Date: 2026-06-27

## Scope

This QA record covers the site-wide command-interface redesign implemented from `PRDs/site-wide-formidable-command-interface-redesign-prd.md` and `ImplementationPlans/site_wide_formidable_command_interface_redesign_task_packets.md`.

The redesign is presentation-only. It does not intentionally change scientific, mathematical, governance, workflow, source-authority, or claim-status claims.

## Migrated Surfaces

- `/project/overview/`: command-band hero, evidence rails, and living-project status dossier.
- Shared route renderer: `InternalExplainerPage.astro` now renders section metadata as status dossiers and related/source links as evidence rails.
- Shared route grid: `ProjectRouteGrid.astro` now renders implemented/planned routes as an evidence rail.
- `/project/physics/current-state/`: burden/status sections use evidence rails and status dossiers.
- `/resources/`: reader paths use an evidence rail; manifest state uses a status dossier.
- `/resources/documents/`: reading path uses an evidence rail; document metadata in `DocumentActions.astro` uses status dossiers.

## Explicit Exception

- `/resources/diagrams/` remains framed for diagram inspection. This is intentional because its primary reader task is artifact review rather than immersive command-interface reading.

## Screenshot Evidence

Baseline screenshots:

- `output/playwright/formidable-phase1-baseline-overview-desktop-2026-06-27.png`
- `output/playwright/formidable-phase1-baseline-overview-mobile-2026-06-27.png`

Production-preview screenshots:

- `output/playwright/formidable-preview-overview-desktop-2026-06-27.png`
- `output/playwright/formidable-preview-overview-tablet-2026-06-27.png`
- `output/playwright/formidable-preview-overview-mobile-2026-06-27.png`
- `output/playwright/formidable-preview-physics-desktop-2026-06-27.png`
- `output/playwright/formidable-preview-physics-mobile-2026-06-27.png`
- `output/playwright/formidable-preview-ai-system-desktop-2026-06-27.png`
- `output/playwright/formidable-preview-ai-system-mobile-2026-06-27.png`
- `output/playwright/formidable-preview-operations-desktop-2026-06-27.png`
- `output/playwright/formidable-preview-operations-mobile-2026-06-27.png`
- `output/playwright/formidable-preview-source-authority-desktop-2026-06-27.png`
- `output/playwright/formidable-preview-source-authority-mobile-2026-06-27.png`
- `output/playwright/formidable-preview-current-state-desktop-2026-06-27.png`
- `output/playwright/formidable-preview-current-state-mobile-2026-06-27.png`
- `output/playwright/formidable-preview-resources-desktop-2026-06-27.png`
- `output/playwright/formidable-preview-resources-mobile-2026-06-27.png`
- `output/playwright/formidable-preview-documents-desktop-2026-06-27.png`
- `output/playwright/formidable-preview-documents-mobile-2026-06-27.png`
- `output/playwright/formidable-preview-overview-reduced-motion-2026-06-27.png`

Browser QA report:

- `output/playwright/formidable-command-interface-preview-qa-2026-06-27.json`

The screenshot and JSON files are local QA artifacts under ignored `output/playwright/`.

## Browser QA Result

Production preview URL: `http://127.0.0.1:4322`

Checked routes:

- `/project/overview/`
- `/project/physics/`
- `/project/ai-research-agent-system/`
- `/project/operations/`
- `/project/source-authority/`
- `/project/physics/current-state/`
- `/resources/`
- `/resources/documents/`

Checked viewports:

- Desktop: `1440x1200`
- Tablet: `820x1180`
- Mobile: `390x844`

Automated browser checks found:

- No route-level horizontal overflow.
- No detected text clipping for links, buttons, headings, paragraphs, definition rows, list items, spans, small text, summaries, or figure captions.
- No browser console errors.
- Reduced-motion overview pass reported `0` running animations.

## Validation

Passed:

- `npm run build`
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`
- `python3 scripts/generate_page_provenance.py`
- `python3 scripts/run_curator.py --write`
- `npm run validate`
- `.venv/bin/python -m pytest`
- `python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict`
- `npm run quality`

Notes:

- The implementation plan listed `python3 scripts/generate_page_provenance.py --write`, but the current script has no `--write` flag. The valid repository command is `python3 scripts/generate_page_provenance.py`.
- The system `python3 -m pytest` environment did not have `pytest`; the repository virtualenv command `.venv/bin/python -m pytest` passed with 41 tests.

## Hardening Added

- Added `scripts/validate_layout_language.py`.
- Added `tests/test_validate_layout_language.py`.
- Added `npm run validate:layout`.
- Wired `validate:layout` into `npm run validate`.

The layout validator checks objective migration facts rather than visual taste: required command primitives must exist, migrated surfaces must use the relevant primitive tokens, and `/project/overview/` must not reintroduce primary `track-grid` or `link-grid` card-grid structure.
