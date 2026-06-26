# Physics Current State And Curator Codex Task Packets

Date: 2026-06-26

Source PRD: The AEther Flow Website. (2026). `PRDs/physics-current-state-and-curator-prd.md` [Product requirements document].

These packets are ordered for one Codex session or one draft PR each. Tasks 03 and 04 depend on the route/provenance decisions from Task 02. Task 05 is the release verification pass.

## Task 01: Add Current-State Snapshot Contract

### Goal

Create a deterministic, checked-in current-state snapshot data contract sourced from upstream control files without automatically changing public website content during normal builds.

### Context

- PRD requirements: REQ-002, REQ-003, REQ-004, REQ-007, NFR-001, NFR-002
- Relevant files or directories:
  - `PRDs/physics-current-state-and-curator-prd.md`
  - `src/data/physics_current_state_snapshot.json`
  - `scripts/refresh_physics_current_state_snapshot.py`
  - `tests/test_physics_current_state_snapshot.py`
  - `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/program_state.yaml`
  - `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/handoffs/`
  - `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/DISTANCE_TO_GR_LEDGER.csv`
  - `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/CLAIM_BOUNDARY_REGISTRY.csv`
- Existing patterns to follow:
  - Python standard-library scripts in `scripts/`
  - deterministic JSON writing from `scripts/generate_page_provenance.py`
  - tests in `tests/`

### Constraints

- Do not add runtime Python dependencies unless implementation evidence proves standard-library parsing is unsafe.
- Do not read upstream files during Astro page rendering.
- Do not write public pages, public manifests, public assets, or page copy from the snapshot script except through an explicit reviewed `--write` mode for the snapshot file.
- Do not expose absolute local source paths in snapshot data.
- Preserve negative claim boundaries exactly: no `MetricData(E)` adoption, no `g_eff`, no matter coupling, no Einstein equations, no benchmark promotion, and no completed derivation unless upstream source state explicitly changes.

### Implementation Notes

- Add `src/data/physics_current_state_snapshot.json` with reviewed fields:
  - `source_repository`
  - `source_commit`
  - `source_commit_date`
  - `source_refresh_date`
  - `website_publication_date`
  - `active_task_id`
  - `latest_handoff_id`
  - `current_status`
  - `claim_boundary_summary`
  - `derivation_burden`
  - `blocked_claims`
  - `next_recommended_action`
  - `source_dependencies`
  - `source_provenance_links`
- Add a script that reads upstream source root and derives the latest handoff from `program_state.yaml`.
- Use `csv.DictReader` for `DISTANCE_TO_GR_LEDGER.csv`.
- Parse only the needed YAML fields in a strict, fail-closed way. Unsupported shape should error rather than guess.
- Add tests with temporary fixture files for:
  - normal snapshot generation;
  - missing latest handoff;
  - missing required program state field;
  - no absolute path leakage;
  - preservation of blocked claim strings.

### Acceptance Criteria

- [ ] `src/data/physics_current_state_snapshot.json` exists and contains source-root-relative dependencies only.
- [ ] The refresh script can compute the snapshot from a fixture source root.
- [ ] The refresh script writes only when explicitly invoked with `--write`.
- [ ] Snapshot generation derives the latest handoff from `program_state.yaml`.
- [ ] Tests cover malformed or missing source data as fail-closed errors.
- [ ] No public page, public manifest, asset file, or public claim is modified by this task except the new snapshot artifact.

### Validation

```bash
python3 -m pytest tests/test_physics_current_state_snapshot.py
python3 -m pytest
```

### Done When

The repository has a reviewed current-state snapshot contract and tested refresh script, with no public route added yet and no automatic public claim updates.

## Task 02: Build The Static Current-State Page And Provenance Entries

### Goal

Add `/project/physics/current-state/` as a static Astro page with internal-first navigation, source-authority notices, and route/provenance coverage.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-013
- Relevant files or directories:
  - `src/pages/project/physics/current-state/index.astro`
  - `src/pages/project/physics/index.astro`
  - `src/pages/project/physics/gr-derivation-roadmap/index.astro`
  - `src/lib/siteContent.ts`
  - `src/components/SourceNotice.astro`
  - `src/data/physics_current_state_snapshot.json`
  - `public/files/manifests/page_route_map.json`
  - `public/files/manifests/page_provenance.json`
  - `scripts/generate_page_provenance.py`
  - `scripts/validate_page_provenance.py`
  - `scripts/quality_gate.py`
- Existing patterns to follow:
  - Physics pages use `BaseLayout`, `SourceNotice`, `track-page-*` classes, `track-status-grid`, and source-boundary sections.
  - Route/source provenance lives in `page_route_map.json` and generated `page_provenance.json`.

### Constraints

- Keep the page a curated snapshot, not an evergreen conceptual explainer.
- Do not auto-refresh public content from upstream during build.
- Do not add external dependencies.
- Keep GitHub/source links in provenance/source zones.
- Do not publish curator diagnostics or draft/control paths as primary public content.
- Avoid visible absolute local paths.

### Implementation Notes

- Add `projectSourceNoticeDefaults.physicsCurrentState` in `src/lib/siteContent.ts`.
- Add a `projectPhysicsDeepDiveRoutes` entry for "Current physics state".
- Update `/project/physics/` and `/project/physics/gr-derivation-roadmap/` with internal links to the current-state page where they clarify status.
- Add the new route to `page_route_map.json` with upstream source paths from the snapshot dependencies.
- Update `scripts/validate_page_provenance.py` required routes.
- Regenerate `page_provenance.json` after page and route map changes.
- Consider adding the route to `scripts/quality_gate.py` source-notice checks.
- The page should include one `h1`, source refresh metadata, active task/handoff, derivation burden, blocked claims, next recommended action, and concise source-provenance links.

### Acceptance Criteria

- [ ] `/project/physics/current-state/` builds as a static Astro route.
- [ ] The page has exactly one `h1`.
- [ ] The page visibly shows source refresh metadata and source commit.
- [ ] The page visibly shows active task, latest handoff, current status, derivation burden, blocked claims, and next recommended action.
- [ ] The page states that it is a reader-facing curated snapshot and not source authority.
- [ ] The physics landing page and GR roadmap link to the new internal route.
- [ ] The route exists in `page_route_map.json` and `page_provenance.json`.
- [ ] No rendered page contains an absolute local path.

### Validation

```bash
python3 scripts/generate_page_provenance.py
npm run validate:provenance
npm run build
npm run validate
```

For browser QA, run a local server and inspect desktop and mobile viewports:

```bash
npm run dev -- --host 127.0.0.1
```

Then use Playwright to check `/project/physics/current-state/` for non-overlap, visible source notice, and working internal links.

### Done When

The current-state route is visible, static, internally linked, provenance-covered, and source-boundary safe.

## Task 03: Add Curator Dependency Collection And Drift Reports

### Goal

Create the repo-internal curator engine that compares declared website source dependencies against current upstream source state and writes deterministic JSON and Markdown reports.

### Context

- PRD requirements: REQ-007, REQ-008, REQ-009, REQ-010, REQ-013, NFR-001, NFR-002
- Relevant files or directories:
  - `scripts/run_curator.py`
  - `curator/reports/latest.json`
  - `curator/reports/latest.md`
  - `public/files/manifests/page_route_map.json`
  - `public/files/manifests/page_provenance.json`
  - `public/files/manifests/source_manifest.json`
  - `src/data/physics_current_state_snapshot.json`
  - `tests/test_curator_reports.py`
- Existing patterns to follow:
  - `scripts/validate_page_provenance.py` hash helpers and safe-relative-path checks.
  - `scripts/import_ontology_assets.py` source-root and git command patterns.

### Constraints

- Do not modify public pages, public manifests, public assets, or page copy.
- Do not serve curator reports under `public/`.
- Do not include absolute local paths in reports.
- Do not monitor the whole upstream repository in first release.
- Keep output deterministic for unchanged dependencies.

### Implementation Notes

- Build dependency entries from:
  - route map upstream source paths;
  - page provenance upstream source hashes and commits;
  - source manifest approved assets;
  - current-state snapshot dependencies.
- Compute current source commit and current source hashes.
- Generate `latest.json` with stable key ordering and sorted entries.
- Generate `latest.md` with review language:
  - what changed;
  - why it matters;
  - affected website surfaces;
  - recommended action.
- Add a check mode that computes a fresh report and compares it to checked-in `curator/reports/latest.*` without mutating files.
- Add a write mode that updates report artifacts only when explicitly requested.
- Add a `source_summary_lag` diagnostic when `current_frontier.md` lags behind `program_state.yaml` or the latest handoff. Keep it diagnostic, not public authority.

### Acceptance Criteria

- [ ] Curator report generation is deterministic for unchanged fixture dependencies.
- [ ] `curator/reports/latest.json` contains route, source path, old hash, new hash, old commit, current commit, severity, impact class, recommended action, and acknowledgement state.
- [ ] `curator/reports/latest.md` explains changed surfaces in human review language.
- [ ] Reports contain no absolute local paths or private machine details.
- [ ] Validation mode does not write public files or curator report files.
- [ ] Write mode updates only `curator/reports/latest.json` and `curator/reports/latest.md`.

### Validation

```bash
python3 -m pytest tests/test_curator_reports.py
python3 -m pytest
```

### Done When

The curator can produce and validate deterministic internal reports from declared dependencies, without acknowledgement or package-script gating yet.

## Task 04: Add Severity, Acknowledgements, And Validation Gate

### Goal

Wire curator severity and acknowledgement semantics into normal validation without weakening fail-closed behavior for critical drift.

### Context

- PRD requirements: REQ-008, REQ-009, REQ-011, REQ-012, REQ-013
- Relevant files or directories:
  - `scripts/run_curator.py`
  - `scripts/validate_page_provenance.py`
  - `curator/acknowledgements/*.yaml`
  - `package.json`
  - `tests/test_curator_acknowledgements.py`
  - `tests/test_validate_page_provenance.py`
- Existing patterns to follow:
  - package scripts use `python3 scripts/...`
  - validator tests create broken fixtures and assert fail-closed errors.

### Constraints

- Acknowledgements must not suppress `critical` drift.
- Acknowledgements must be checked in, exact to route/source/commit/hash, and reviewable.
- Keep provenance validation fail-closed for route structure, local page hash drift, safe paths, and private path leakage.
- Move upstream source drift comparison into the curator only if needed for severity and acknowledgement behavior.
- Do not add a database or runtime service.

### Implementation Notes

- Add `curator/acknowledgements/.gitkeep`.
- Define a strict acknowledgement YAML shape:
  - `route_path`
  - `source_path`
  - `severity`
  - `current_commit`
  - `current_sha256`
  - `acknowledged_by`
  - `acknowledged_at`
  - `reason`
  - `expires_at`
- Use a narrow standard-library parser for this shape, or choose JSON if YAML parsing proves too fragile and document the deviation. The PRD names YAML, so YAML is preferred.
- Add severity outcomes:
  - `critical`: validation fails always.
  - `review_required`: validation fails without exact valid acknowledgement.
  - `informational`: reported without failing.
- Add `validate:curator` to `package.json`.
- Update `npm run validate` to include curator after existing manifest/content/link/provenance checks and before Cloudflare/build unless tests prove another ordering is safer.
- If `validate_page_provenance.py` still hard-fails upstream source drift, refactor it so that drift is emitted by the curator instead.

### Acceptance Criteria

- [ ] `npm run validate:curator` exists.
- [ ] `npm run validate` invokes curator validation.
- [ ] Critical drift fails even with an acknowledgement.
- [ ] Review-required drift fails without acknowledgement.
- [ ] Review-required drift passes with an exact valid acknowledgement.
- [ ] Informational drift appears in reports without failing validation.
- [ ] Stale or malformed acknowledgements fail closed.
- [ ] Existing provenance tests still cover local page hash drift and route map integrity.

### Validation

```bash
python3 -m pytest tests/test_curator_acknowledgements.py
python3 -m pytest tests/test_validate_page_provenance.py
python3 -m pytest
npm run validate:curator
npm run validate
```

### Done When

Curator severity and acknowledgement rules are part of normal validation, with critical drift fail-closed and non-critical drift reviewable through checked-in acknowledgement files.

## Task 05: Final QA, Browser Verification, And Review Notes

### Goal

Verify the page, curator, manifests, and validation wiring end to end, then record residual risks and follow-up recommendations.

### Context

- PRD requirements: REQ-001 through REQ-013, NFR-001, NFR-002
- Relevant files or directories:
  - `src/pages/project/physics/current-state/index.astro`
  - `curator/reports/latest.json`
  - `curator/reports/latest.md`
  - `public/files/manifests/page_route_map.json`
  - `public/files/manifests/page_provenance.json`
  - `output/playwright/`
  - `ImplementationPlans/physics_current_state_and_curator_implementation_plan.md`
  - `ImplementationPlans/physics_current_state_and_curator_task_packets.md`
- Existing patterns to follow:
  - Use `npm run validate` for the configured gate.
  - Use Playwright desktop and mobile checks for frontend signoff when relevant.

### Constraints

- Do not deploy. Deployment is explicitly out of scope.
- Do not claim scientific authority from validator success.
- Do not leave a dev server running when the task finishes.
- Do not skip failed checks without recording concrete reasons.

### Implementation Notes

- Run the full Python test suite.
- Run the full npm validation gate.
- Run `npm run quality` if the implementation touched rendered frontend pages or public manifests.
- Use Playwright against a local dev or preview server for:
  - desktop viewport;
  - mobile viewport;
  - one `h1`;
  - visible source metadata;
  - visible blocked claims;
  - no overlapping text;
  - source notice present;
  - internal links work.
- Save browser artifacts under `output/playwright/` if useful.
- Review the final diff against the PRD before signoff.

### Acceptance Criteria

- [ ] `python3 -m pytest` passes.
- [ ] `npm run validate` passes.
- [ ] `npm run quality` passes or any skip is justified with a concrete reason.
- [ ] Browser QA confirms the page renders correctly on desktop and mobile.
- [ ] Curator reports are internal and not under `public/`.
- [ ] No public page or report leaks absolute local paths.
- [ ] Final response names validation results and remaining uncertainty.

### Validation

```bash
python3 -m pytest
npm run validate
npm run quality
npm run dev -- --host 127.0.0.1
```

Use Playwright for browser QA after the dev server starts.

### Done When

The PRD implementation is verified end to end, residual risks are documented, and the work is ready for review or a draft PR. Deployment remains a separate explicit action.

## Recommended First Implementation Prompt

Use this prompt to begin coding with Codex:

```text
Implement Task 01 from ImplementationPlans/physics_current_state_and_curator_task_packets.md. Read PRDs/physics-current-state-and-curator-prd.md and AGENTS.md first. Add only the current-state snapshot contract, refresh script, and focused tests. Do not add the public route yet. Preserve the website source-authority boundary and do not add runtime dependencies unless the repository evidence proves they are required. Run python3 -m pytest for the affected tests and summarize results.
```
