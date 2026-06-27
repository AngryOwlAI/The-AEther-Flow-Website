# Site-Wide Formidable Command-Interface Redesign Task Packets

Date: 2026-06-27

Source PRD: `PRDs/site-wide-formidable-command-interface-redesign-prd.md`

Companion plan:
`ImplementationPlans/site_wide_formidable_command_interface_redesign_implementation_plan.md`

## Shared Context For All Tasks

Repository: `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website`

This is the reader-facing website for
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`. Upstream source files, registries,
and governed task records remain authoritative. The redesign is presentation
work unless a task explicitly says otherwise.

Global constraints:

- Preserve the existing Angry Owl cyan, orange, and dark graphite color schema.
- Do not add new production animation dependencies.
- Do not rewrite or strengthen scientific, mathematical, governance,
  research-workflow, source-authority, or claim-status claims.
- Keep internal website routes as primary reader journeys; keep GitHub/source
  links as provenance or inspection links.
- Keep animated SVGs textless and accessible through HTML, ARIA labels,
  `<title>`, and `<desc>`.
- Regenerate page provenance after page-source changes.
- Do not deploy unless explicitly authorized.
- Be aware the worktree may already contain user changes. Do not revert them.

Common validation commands discovered from the repository:

```bash
npm run build
npm run validate
npm run quality
npm run validate:content
npm run validate:links
npm run validate:svg
npm run validate:provenance
python3 -m pytest
python3 scripts/generate_page_provenance.py --write
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict
```

## Task 1: Capture Phase 1 Baseline Evidence

### Goal

Capture the pre-redesign `/project/overview/` visual baseline and record the
specific card-grid/layout issues Phase 1 is meant to replace.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-013, REQ-015, REQ-017, REQ-018
- Relevant files or directories:
  - `src/pages/project/overview.astro`
  - `src/styles/global.css`
  - `docs/quality/`
  - `output/playwright/`
- Existing patterns to follow:
  - `docs/quality/` holds tracked QA summaries.
  - `output/playwright/` holds local screenshot artifacts and is gitignored.

### Constraints

- Do not change production code in this task.
- Do not claim the new design is better yet; this task records the baseline.
- Do not deploy.

### Implementation Notes

- Start the local dev server or preview server on `127.0.0.1`.
- Capture desktop and mobile screenshots of `/project/overview/`.
- Optionally capture a tablet viewport if it reveals layout pressure.
- Record baseline observations in a new tracked QA note such as
  `docs/quality/formidable-command-interface-phase1-baseline.md`.
- Identify the exact sections that currently read as repeated card grids:
  two-track section, project capabilities, reader journeys, and living-project
  source-authority section.
- Record screenshot paths rather than committing ignored screenshot files.

### Acceptance Criteria

- [ ] Baseline desktop and mobile overview screenshots exist locally.
- [ ] A tracked QA note describes the pre-redesign card-grid rhythm and target
      replacement areas.
- [ ] The note distinguishes observation from judgment.
- [ ] No production source files are modified.

### Validation

```bash
npm run build
```

If a server is used:

```bash
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

### Done When

The baseline evidence is captured, the QA note is ready for review, and the
next task can redesign against a known visual baseline.

## Task 2: Add Command-Interface Primitives

### Goal

Add reusable command band, evidence rail, and status dossier primitives that can
support Phase 1 and later route-family migrations without broad one-off CSS.

### Context

- PRD requirements: REQ-002, REQ-005, REQ-006, REQ-010, REQ-011, REQ-012,
  REQ-013, REQ-014, REQ-018, NFR-001, NFR-004, NFR-005
- Relevant files or directories:
  - `src/components/`
  - `src/styles/global.css`
  - `src/pages/project/overview.astro`
  - `src/components/InternalExplainerPage.astro`
  - `src/components/ProjectRouteGrid.astro`
- Existing patterns to follow:
  - Astro components are small and prop-driven.
  - Visual styling is centralized in `src/styles/global.css`.
  - Current dark route-family classes are namespaced under
    `project-overview-page` and `project-track-page`.

### Constraints

- Do not add production dependencies.
- Do not encode scientific claims inside generic components.
- Do not remove existing SVG animations.
- Do not create nested cards or a renamed card grid.
- Keep mobile constraints explicit so content cannot overlap.

### Implementation Notes

- Prefer thin Astro components plus shared CSS:
  - `src/components/CommandBand.astro`
  - `src/components/EvidenceRail.astro`
  - `src/components/StatusDossier.astro`
- If a component would be too abstract, use shared classes first, but document
  the primitive contract in code comments or QA notes.
- Components should accept ordinary heading/body/link slots or simple arrays.
- Evidence rails should support horizontal desktop and vertical mobile layout.
- Status dossiers should be dense but legible and should not become the default
  replacement for every section.
- Extend `prefers-reduced-motion` coverage for new animation hooks.
- Keep SVG policy intact: no visible SVG text; accessible names via
  `<title>`, `<desc>`, ARIA, captions, or nearby HTML.

### Acceptance Criteria

- [ ] Command band, evidence rail, and status dossier primitives exist as
      reusable implementation surfaces.
- [ ] The primitives preserve existing color tokens.
- [ ] The primitives have responsive behavior for mobile viewports.
- [ ] The primitives have reduced-motion coverage where they animate.
- [ ] No scientific or source-authority copy changes are introduced merely by
      creating primitives.

### Validation

```bash
npm run build
npm run validate:svg
```

If Python tests are affected:

```bash
python3 -m pytest
```

### Done When

The primitive foundation builds, passes SVG policy validation, and is ready for
use on `/project/overview/`.

## Task 3: Redesign `/project/overview/` As The Phase 1 Proof

### Goal

Apply the command-interface primitives to `/project/overview/` as the flagship
proof while preserving source-boundary copy and route destinations.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-005, REQ-006, REQ-009, REQ-011,
  REQ-012, REQ-013, REQ-014, REQ-016, REQ-017, NFR-001, NFR-002, NFR-003,
  NFR-005
- Relevant files or directories:
  - `src/pages/project/overview.astro`
  - `src/styles/global.css`
  - `src/components/CommandBand.astro`
  - `src/components/EvidenceRail.astro`
  - `src/components/StatusDossier.astro`
  - `src/components/SourceNotice.astro`
  - `public/files/manifests/page_provenance.json`
- Existing patterns to follow:
  - Current overview already uses animated structural SVGs.
  - Current overview already routes readers internally.
  - `SourceNotice` preserves source-authority boundaries.

### Constraints

- Phase 1 is presentation-only.
- Do not rewrite or strengthen physics, AI-system, governance, or
  source-authority claims.
- Do not reopen color schema decisions.
- Do not change route-map semantics.
- Do not redesign `/resources/diagrams/`.

### Implementation Notes

- Convert the overview hero into a command band with the existing field SVG as
  a structural scene layer rather than a framed preview.
- Convert the two-track section into an evidence rail or split command band
  showing physics and AI as first-class coordinated tracks.
- Convert project capabilities and reader journeys away from equal card grids
  into journey rails with clear progression and internal route emphasis.
- Convert living-project/source-authority content into a status dossier paired
  with `SourceNotice`.
- Keep current route destinations unless the PRD already authorizes a label
  refinement.
- Regenerate page provenance after editing `overview.astro`.

### Acceptance Criteria

- [ ] `/project/overview/` no longer relies on repeated equal-card grids as its
      primary structure.
- [ ] Command bands, evidence rails, and status dossiers are visibly used.
- [ ] Existing internal route links still work.
- [ ] Source-authority and claim-boundary language remains materially
      unchanged.
- [ ] The page builds as static Astro output.
- [ ] `page_provenance.json` is regenerated after source edits.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
npm run validate:content
npm run validate:links
npm run validate:svg
npm run validate:provenance
npm run build
```

### Done When

The overview proof is implemented, provenance is current, route behavior is
unchanged, and the page is ready for browser evidence.

## Task 4: Validate Overview Proof And Create Comparison Evidence

### Goal

Validate Phase 1 with repository gates, browser screenshots, reduced-motion
checks, and side-by-side comparison evidence.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-009, REQ-010, REQ-013, REQ-015,
  REQ-016, REQ-017, NFR-001, NFR-002, NFR-003, NFR-005
- Relevant files or directories:
  - `src/pages/project/overview.astro`
  - `src/styles/global.css`
  - `docs/quality/`
  - `output/playwright/`
  - `scratch/project-explainer/`
- Existing patterns to follow:
  - Browser QA artifacts go under `output/playwright/`.
  - Tracked summaries can live under `docs/quality/`.

### Constraints

- Do not deploy.
- Do not hide validation failures.
- If a validation command is skipped, name the concrete reason.
- Keep the comparison focused on visual hierarchy, overlap, motion, source
  boundaries, and internal navigation.

### Implementation Notes

- Capture post-redesign desktop and mobile screenshots of `/project/overview/`.
- Create a side-by-side comparison artifact or tracked QA note referencing the
  baseline and post-redesign screenshots.
- Verify hover/focus states for primary actions and navigation menu behavior.
- Verify reduced-motion mode manually or through Playwright emulation.
- Run full validation if feasible.
- Run the project frontend audit against `dist/` after `npm run build`.

### Acceptance Criteria

- [ ] Desktop and mobile post-redesign screenshots exist locally.
- [ ] A tracked QA summary compares baseline and redesigned overview.
- [ ] No text, CTA, SVG, heading, or navigation overlap is observed in the
      tested viewports.
- [ ] Reduced-motion behavior is checked and summarized.
- [ ] Validation results are summarized with exact commands.

### Validation

```bash
npm run validate
python3 -m pytest
python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict
```

If a local server is used:

```bash
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

### Done When

Phase 1 has repo-gate evidence, browser evidence, reduced-motion notes, and a
reviewable comparison summary.

## Task 5: Migrate Shared Route-Family Templates

### Goal

Move shared route-family structures from card grids toward command bands,
evidence rails, and status dossiers before individual route hand-tuning.

### Context

- PRD requirements: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-009,
  REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, NFR-001, NFR-002, NFR-003,
  NFR-005
- Relevant files or directories:
  - `src/components/InternalExplainerPage.astro`
  - `src/components/ProjectRouteGrid.astro`
  - `src/lib/internalExplainers.ts`
  - `src/lib/siteContent.ts`
  - `src/pages/project/physics/index.astro`
  - `src/pages/project/ai-research-agent-system/index.astro`
  - `src/pages/project/operations/index.astro`
  - `src/pages/project/source-authority/index.astro`
  - `src/styles/global.css`
  - `public/files/manifests/page_provenance.json`
- Existing patterns to follow:
  - Internal explainer pages already share `InternalExplainerPage.astro`.
  - Route cards are centralized through `ProjectRouteGrid.astro`.

### Constraints

- Preserve route copy and claim qualifiers.
- Keep source links in provenance/source zones.
- Avoid one-off CSS solving the same layout problem differently across pages.
- Do not change document asset manifests unless public assets change.

### Implementation Notes

- Refactor `InternalExplainerPage.astro` sections so `section.cards` can render
  as evidence rails or status dossiers depending on section purpose.
- Refactor `ProjectRouteGrid.astro` into a journey/evidence rail while
  preserving implemented/planned route status.
- Apply shared primitives to physics, AI-system, operations, and
  source-authority landing pages where they currently use route grids or status
  grids.
- Keep `/resources/diagrams/` framed for inspection.
- Regenerate page provenance for changed page sources.

### Acceptance Criteria

- [ ] Shared route-family pages use common command-interface primitives.
- [ ] Route lists present progression or inspection purpose rather than generic
      peer cards.
- [ ] Source-authority notes remain visible and accurate.
- [ ] Internal-first link validation passes.
- [ ] Page provenance is regenerated for changed routes.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
npm run validate:content
npm run validate:links
npm run validate:svg
npm run validate:provenance
npm run build
```

### Done When

The shared route-family renderer and route grids use the new layout language
without content-authority drift.

## Task 6: Convert Document And Current-State Surfaces To Dossiers

### Goal

Apply status dossier and evidence rail patterns to document/download and
current-state surfaces while preserving document usability and physics-status
precision.

### Context

- PRD requirements: REQ-003, REQ-005, REQ-007, REQ-008, REQ-009, REQ-011,
  REQ-012, REQ-015, NFR-001, NFR-002, NFR-003, NFR-005
- Relevant files or directories:
  - `src/pages/resources/documents.astro`
  - `src/components/DocumentActions.astro`
  - `src/lib/manifests.ts`
  - `src/pages/project/physics/current-state/index.astro`
  - `src/data/physics_current_state_snapshot.json`
  - `src/styles/global.css`
  - `public/files/manifests/page_provenance.json`
- Existing patterns to follow:
  - `DocumentActions.astro` already separates PDF reading, PDF download, and
    TeX download.
  - Current-state page already distinguishes snapshot metadata, burden state,
    blocked claims, and next action.

### Constraints

- Do not reduce PDF/TeX action clarity.
- Do not imply PDFs carry authority over registered TeX sources.
- Do not alter checked-in physics snapshot facts.
- Do not auto-refresh upstream source state during build.

### Implementation Notes

- Convert document metadata to status dossier rows without hiding action links.
- Keep `Read PDF`, `Download PDF`, and `Download TeX` labels clear.
- Convert current-state metadata and burden sections into dense dossiers and
  burden/status rails.
- Preserve negative and blocked claim language exactly unless a purely visual
  label needs shortening.
- Regenerate page provenance for changed page sources.

### Acceptance Criteria

- [ ] Document actions remain visible, keyboard reachable, and plainly labeled.
- [ ] Current-state metadata is easier to scan as dossiers.
- [ ] Physics status language is not strengthened.
- [ ] Mobile screenshots show no overlap in document and current-state pages.
- [ ] Manifest validation still passes.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
npm run validate:manifests
npm run validate:content
npm run validate:svg
npm run validate:provenance
npm run build
```

### Done When

Document and current-state pages align with the new command-interface language
while preserving source-authority and download usability.

## Task 7: Refine Major Route Families

### Goal

Tune the physics, AI-system, operations, resources, and current-state route
families after shared primitives are stable.

### Context

- PRD requirements: REQ-001 through REQ-015, NFR-001 through NFR-005
- Relevant files or directories:
  - `src/pages/project/physics/**`
  - `src/pages/project/ai-research-agent-system/**`
  - `src/pages/project/operations/**`
  - `src/pages/resources/**`
  - `src/pages/project/source-authority/index.astro`
  - `src/components/**`
  - `src/lib/**`
  - `src/styles/global.css`
  - `public/files/manifests/page_provenance.json`
- Existing patterns to follow:
  - Physics pages use claim-boundary language and source notices.
  - AI and operations pages use internal explainers and source provenance.
  - Resources pages prioritize document and asset inspection.

### Constraints

- Work route family by route family; keep PR/branch scope reviewable.
- Do not change scientific or operational claims.
- Keep `/resources/diagrams/` framed when the reader task is diagram
  inspection.
- Keep GitHub/source links in provenance zones unless clearly labeled source
  inspection.

### Implementation Notes

- Physics pages: emphasize source-boundary command bands and claim-gate rails.
- AI-system pages: emphasize workflow rails, role/status dossiers, validator and
  memory boundaries.
- Operations pages: emphasize control-map command bands and execution evidence
  rails.
- Resources pages: emphasize document-library dossiers and asset-status rails.
- Current-state page: emphasize compact source-state dossiers and burden/status
  rails.
- Capture representative screenshots for each migrated route family.

### Acceptance Criteria

- [ ] Major route families share the command-interface visual language.
- [ ] Route-family differences are intentional and tied to reader jobs.
- [ ] Primary reader journeys remain internal-first.
- [ ] Source and provenance zones remain inspectable.
- [ ] Representative desktop, tablet, and mobile screenshots show no overlap.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
npm run validate
python3 -m pytest
python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict
```

If a local server is used:

```bash
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

### Done When

The major route families have been migrated, validated, and visually checked
without source-claim drift.

## Task 8: Add Layout-Language Audit And Final Hardening

### Goal

Make the anti-card-grid direction reproducible with a final QA checklist and,
where feasible, a scoped validator for forbidden or excessive layout patterns.

### Context

- PRD requirements: REQ-010, REQ-013, REQ-015, REQ-017, REQ-018, NFR-001,
  NFR-002, NFR-004, NFR-005
- Relevant files or directories:
  - `scripts/`
  - `tests/`
  - `docs/quality/`
  - `src/styles/global.css`
  - `src/pages/**`
  - `package.json`
- Existing patterns to follow:
  - Repository validators are Python scripts under `scripts/`.
  - Tests for validators live under `tests/`.
  - `npm run validate` is the full configured gate.

### Constraints

- Do not create a brittle validator that rejects legitimate diagram inspection
  or dense metadata use.
- Do not fail pages merely because a card-like component exists; fail only when
  banned patterns are primary structural rhythm or when a scoped anti-pattern is
  unambiguous.
- Keep exceptions explicit, especially `/resources/diagrams/`.

### Implementation Notes

- Start with a tracked final QA checklist in `docs/quality/` if enforcement
  scope is not yet clear.
- Add a Python validator only for precise checks, such as:
  - no nested card/panel class combinations in project pages,
  - no new primary sections using `link-grid` or `track-status-grid` on migrated
    routes,
  - required presence of at least one command-interface primitive on migrated
    route families,
  - explicit exception list for diagram inspection pages.
- Add tests for pass/fail cases if a validator is introduced.
- Wire the validator into `package.json` only after false-positive risk is low.
- Record final browser QA and residual exceptions.

### Acceptance Criteria

- [ ] The final QA record states which routes are migrated, deferred, or
      intentionally exempt.
- [ ] Anti-patterns from the PRD are represented as checklist items or scoped
      validation checks.
- [ ] Any new validator has tests.
- [ ] Full validation either passes or skipped checks are named with concrete
      reasons.
- [ ] The final review confirms no route regressed to generic card-grid
      structure as its primary model.

### Validation

If no validator is added:

```bash
npm run validate
```

If a validator is added and wired into npm scripts:

```bash
python3 -m pytest
npm run validate
npm run quality
```

### Done When

The redesign has a durable acceptance surface: QA notes, optional validator
coverage, full gate results, and explicit residual exceptions.

## Recommended First Codex Prompt

```text
Use ImplementationPlans/site_wide_formidable_command_interface_redesign_task_packets.md.
Execute Task 1 only: capture Phase 1 baseline evidence for /project/overview/.
Do not modify production code. Save local screenshots under output/playwright/
and write the tracked QA summary under docs/quality/. Report exact commands run,
artifact paths, and any blockers.
```
