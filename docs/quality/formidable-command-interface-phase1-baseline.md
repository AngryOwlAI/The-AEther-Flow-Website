# Formidable Command Interface Phase 1 Baseline

Date: 2026-06-27

## Scope

Route inspected: `/project/overview/`

This note records the pre-redesign rendered state for the Phase 1 command-interface proof. It reflects the worktree as served locally on 2026-06-27 before this redesign pass changed production route or component files. Existing uncommitted style edits were present before this note was written.

## Local Evidence

- Desktop screenshot: `output/playwright/formidable-phase1-baseline-overview-desktop-2026-06-27.png`
- Mobile screenshot: `output/playwright/formidable-phase1-baseline-overview-mobile-2026-06-27.png`
- Local URL: `http://127.0.0.1:4321/project/overview/`
- Desktop viewport: `1440x1200`
- Mobile viewport: `390x844`

The screenshot files are local QA artifacts under the ignored `output/playwright/` directory. They are referenced here for review but are not intended to be committed.

## Observations

- The hero already uses the cyan, orange, and graphite visual schema with an animated structural SVG.
- The two-track section renders as two peer `track-card` panels for physics and the AI research-agent system.
- The project capability section renders as a repeated `link-grid` of five equal card-like entries.
- The reader journey section renders as a second repeated `link-grid` of five equal card-like entries.
- The living-project section pairs copy with `SourceNotice`, but the section remains a bordered panel in the same visual rhythm as adjacent sections.
- Source-authority language is visible and should be preserved materially during redesign.

## Target Replacement Areas

- Replace the two-track `track-grid` rhythm with a rail or split command band that shows coordinated tracks without treating them as generic cards.
- Replace the capability `link-grid` with a journey/evidence rail that implies reader progression and internal-first movement.
- Replace the reader journey `link-grid` with a second rail or sequenced path that makes route purpose clearer.
- Convert the living-project/source-authority block into a status dossier paired with the existing source notice.

## Baseline Validation

- `npm run build` passed.
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321` passed for 45 routes.

## Baseline Judgment Boundary

This note distinguishes observable structure from design judgment. The baseline is functional and source-boundary aware, but it relies on repeated bordered card grids as the dominant page rhythm. Phase 1 should improve hierarchy and command-interface character without altering scientific, governance, or source-authority claims.
