# Physics Current State And Curator Implementation Plan

Date: 2026-06-26

## Source PRD

- Source: `PRDs/physics-current-state-and-curator-prd.md`
- Citation: The AEther Flow Website. (2026). `PRDs/physics-current-state-and-curator-prd.md` [Product requirements document].
- Generated for: Codex app, Codex IDE extension, and Codex CLI
- Planning status: Ready with assumptions

## Product Summary

The PRD asks for two connected capabilities:

1. A static reader-facing page at `/project/physics/current-state/` that presents the latest reviewed physics derivation snapshot without making the website authoritative for physics claims.
2. A repo-internal documentation curator that detects drift between declared website dependencies and the live upstream AEther Flow source repository, produces JSON and Markdown reports, and participates in validation with severity and acknowledgement rules.

The page must expose the source refresh date, source commit, active task, latest handoff, current status, derivation burden, blocked claims, next recommended action, and concise source-provenance links. The curator must be advisory, fail-closed for critical drift, and must not rewrite public pages, manifests, assets, or claims automatically.

## Repository Context

- Frameworks and languages: Astro 7 static output, TypeScript, Astro components, Python 3.11 tooling, Playwright dev dependency.
- Package manager and build system: npm with `astro build`.
- Existing related routes:
  - `src/pages/project/physics/index.astro`
  - `src/pages/project/physics/gr-derivation-roadmap/index.astro`
  - `src/pages/project/physics/claim-gates/index.astro`
  - `src/components/SourceNotice.astro`
  - `src/lib/siteContent.ts`
- Existing provenance and manifest layer:
  - `public/files/manifests/page_route_map.json`
  - `public/files/manifests/page_provenance.json`
  - `public/files/manifests/page_provenance.schema.json`
  - `public/files/manifests/source_manifest.json`
  - `scripts/generate_page_provenance.py`
  - `scripts/validate_page_provenance.py`
  - `scripts/validate_manifest_paths.py`
- Existing tests:
  - `tests/test_validate_page_provenance.py`
  - `tests/test_validate_manifest_paths.py`
  - `tests/test_quality_gate.py`
- Relevant repository instructions:
  - The website is reader-facing only.
  - Upstream source files, registries, and governed task records remain authoritative.
  - Page and asset hashes must be regenerated after file changes.
  - Primary reader journeys should stay internal-first; GitHub links are provenance.
- Discovered validation commands:
  - `npm run build`
  - `npm run validate`
  - `npm run quality`
  - `python3 -m pytest`
  - `npm run validate:manifests`
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:provenance`
  - `npm run validate:cloudflare`

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | The implementation should discover the latest handoff from upstream `research_control/program_state.yaml`, not hard-code the PRD's inspected `handoff-0222`. | Live `program_state.yaml` currently reports `latest_handoff_id: handoff-0228`, so the PRD reference is already time-specific. | Coding the snapshot refresh script. |
| ASM-002 | Planning assumption | Python tooling should remain standard-library only unless implementation evidence proves a dependency is safer. | `requirements.txt` says runtime tooling uses the Python standard library only. | Writing YAML or report parsers. |
| ASM-003 | Planning assumption | Curator reports should be checked in under `curator/reports/latest.json` and `curator/reports/latest.md`, while validation computes a fresh report and fails if checked-in reports are stale. | The PRD names repo-internal report artifacts, and existing validation scripts are non-mutating. | Wiring `npm run validate:curator`. |
| ASM-004 | Planning assumption | Existing upstream drift checks in `validate_page_provenance.py` should be split so route/provenance shape stays there and upstream dependency drift moves into the curator. | The PRD introduces severity and acknowledgement semantics that cannot work if provenance validation hard-fails every upstream hash drift first. | Refactoring provenance validation. |
| ASM-005 | Implementation detail | The current-state page should import a checked-in snapshot file, likely `src/data/physics_current_state_snapshot.json`, rather than reading upstream files during Astro build. | Static builds should be reproducible and should not silently refresh public claims. | Implementing the page route. |
| ASM-006 | Implementation detail | Browser QA can use the existing Playwright dependency and project-explainer practice, with artifacts saved under `output/playwright/`. | Prior frontend work uses Playwright CLI and artifacts in that directory. | Final implementation signoff. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Planning assumption | Should the public page display an actual build timestamp, or should it display source refresh date, source commit date, website publication date, and provenance manifest generation date only? | Actual build-time values create deterministic-hash churn in static pages. The plan defaults to deterministic publication/provenance dates. |
| Q-002 | Implementation detail | Should curator acknowledgements include an expiry date as mandatory or optional? | Optional expiry is simpler for first release; mandatory expiry is stricter governance. |
| Q-003 | Implementation detail | Should the curator report include all declared route dependencies every run or only drift entries plus a dependency summary? | Drift-only reports are easier to review; full dependency reports are more audit-friendly. |

No blocking questions prevent implementation planning.

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| REQ-001: Current-state route | `/project/physics/current-state/` builds as a static Astro page. | `src/pages/project/physics/current-state/index.astro`, `src/lib/siteContent.ts`, styles as needed. | TASK-02 | `npm run build`, `npm run validate`, browser QA. |
| REQ-002: Snapshot metadata | Page shows last refreshed from source, upstream source commit, active task, latest handoff, current status, burden, blocked claims, next action, and provenance links. | `src/data/physics_current_state_snapshot.json`, page route, `SourceNotice`. | TASK-01, TASK-02 | Unit tests for snapshot shape, DOM checks, `npm run build`. |
| REQ-003: Source authority | Page uses upstream `program_state.yaml`, latest handoff YAML/Markdown, `DISTANCE_TO_GR_LEDGER.csv`, and claim-boundary data without strengthening claims. | Snapshot refresh script, page copy, source notice defaults. | TASK-01, TASK-02 | Parser tests, review checklist, browser QA. |
| REQ-004: Negative boundaries | Page preserves no `MetricData(E)` adoption, no `g_eff`, no matter coupling, no Einstein equations, no benchmark promotion, and no completed derivation unless upstream changes. | Snapshot data and page boundary panels. | TASK-01, TASK-02 | DOM/content assertions, manual source-authority review. |
| REQ-005: Navigation | Physics landing page and GR roadmap link to the current-state page where it clarifies status. | `src/pages/project/physics/index.astro`, `src/pages/project/physics/gr-derivation-roadmap/index.astro`, `src/lib/siteContent.ts`. | TASK-02 | `npm run validate:links`, browser QA. |
| REQ-006: Route and provenance mapping | Current-state route is present in route/source map and page provenance. | `page_route_map.json`, `page_provenance.json`, schema or validator required routes. | TASK-02 | `python3 scripts/generate_page_provenance.py`, `npm run validate:provenance`. |
| REQ-007: No automatic public rewrite | Curator detects drift and reports it, but does not modify public pages, manifests, assets, or public claims. | Curator script CLI modes and validation wiring. | TASK-03, TASK-04 | Curator tests verify no public writes in validation mode. |
| REQ-008: Declared dependency scope | Curator starts from website-declared dependencies in route map, page provenance, source manifest, and current-state snapshot dependencies. | `scripts/run_curator.py`, optional `curator/config.json`. | TASK-03 | Unit tests with temp fixtures. |
| REQ-009: JSON report | Curator writes deterministic `curator/reports/latest.json` with route, source path, old/new hashes, old/current commits, severity, impact, recommended action, and acknowledgement state. | `curator/reports/latest.json`, report generation code. | TASK-03, TASK-04 | `python3 -m pytest`, `npm run validate:curator`. |
| REQ-010: Markdown report | Curator writes human-readable `curator/reports/latest.md` explaining what changed, why it matters, and affected surfaces. | `curator/reports/latest.md`, report writer. | TASK-03 | Snapshot or text assertions, manual review. |
| REQ-011: Severity and acknowledgements | `critical` fails; `review_required` fails unless exact checked-in acknowledgement exists; `informational` reports without failing. | `curator/acknowledgements/*.yaml`, curator severity engine. | TASK-04 | Tests for critical, acknowledged review, unacknowledged review, informational. |
| REQ-012: Normal validation gate | Curator participates in `npm run validate` after existing manifest/provenance checks unless implementation proves a safer order. | `package.json`, scripts. | TASK-04 | `npm run validate`. |
| REQ-013: Private path hygiene | Curator reports and public route must not expose absolute local paths or private machine details. | Curator report serialization, page copy, quality gate. | TASK-02, TASK-03 | Curator tests, `npm run quality`. |
| NFR-001: Determinism | Unchanged dependencies produce stable JSON and Markdown reports. | Sorting, normalized timestamps, stable report schema. | TASK-03 | Determinism tests. |
| NFR-002: Maintainability | The implementation reuses existing manifest/provenance patterns and avoids a new database or backend. | Python scripts, JSON files, static Astro route. | TASK-01 to TASK-05 | Code review, existing validation commands. |

## Proposed Technical Approach

### 1. Static Current-State Snapshot

Add a checked-in data contract for the current-state page:

- `src/data/physics_current_state_snapshot.json`
- `scripts/refresh_physics_current_state_snapshot.py`
- `tests/test_physics_current_state_snapshot.py`

The refresh script should read upstream files only when explicitly run. It should write the snapshot only with `--write`; otherwise it should print or validate the computed snapshot. The page should import the checked-in snapshot so normal Astro builds do not silently update public scientific claims.

Minimum snapshot fields:

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

The script should use source-root-relative paths only. It should not place `/Volumes/...` paths into public data or curator reports.

Because runtime Python dependencies are currently standard-library only, first release parsing should be fail-closed and narrow:

- parse known top-level scalar fields from `program_state.yaml`;
- parse `blocked_claims` from the latest handoff YAML;
- parse derivation burden rows from `DISTANCE_TO_GR_LEDGER.csv` with `csv.DictReader`;
- treat unsupported YAML shape as an error rather than guessing.

### 2. Reader-Facing Page

Add `src/pages/project/physics/current-state/index.astro` following the existing physics route style:

- `BaseLayout`
- `SourceNotice`
- `track-page-hero`, `track-page-band`, `track-status-grid`, and `source-link-grid` patterns
- one `h1`
- visible source refresh metadata and source commit
- active task and handoff block
- current derivation burden block
- blocked claims list
- next recommended action block
- boundary notice stating that the page is a curated snapshot, not source authority

Update `src/lib/siteContent.ts` to add:

- `projectSourceNoticeDefaults.physicsCurrentState`
- a `projectPhysicsDeepDiveRoutes` entry
- route metadata for resource or reading-path use if needed

Update physics pages only where the route clarifies current status:

- `/project/physics/`
- `/project/physics/gr-derivation-roadmap/`

Keep source links in source/provenance zones, not primary journey cards except for internal website routes.

### 3. Route and Provenance Extension

Add `/project/physics/current-state/` to:

- `public/files/manifests/page_route_map.json`
- `scripts/validate_page_provenance.py` required route set
- `public/files/manifests/page_provenance.json` by running `python3 scripts/generate_page_provenance.py`

Recommended route-map source paths:

- `research_control/program_state.yaml`
- `research_control/handoffs/<latest_handoff_id>.yaml`
- `research_control/handoffs/<latest_handoff_id>.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`

The implementation should derive `<latest_handoff_id>` from the snapshot refresh step and update route map and provenance in the same reviewed edit.

### 4. Curator Drift Engine

Add repo-internal curator artifacts:

- `curator/reports/latest.json`
- `curator/reports/latest.md`
- `curator/acknowledgements/.gitkeep`
- optional `curator/config.json` if severity cannot be inferred cleanly from route metadata

Add scripts:

- `scripts/run_curator.py`
- optionally `scripts/validate_curator_reports.py` if separating generation from validation keeps the code clearer

The curator should compute declared dependencies from:

- `page_route_map.json`
- `page_provenance.json`
- `source_manifest.json`
- `physics_current_state_snapshot.json`

The JSON report should include, per drift item:

- `route_path`
- `source_path`
- `old_sha256`
- `new_sha256`
- `old_commit`
- `current_commit`
- `severity`
- `impact_class`
- `recommended_action`
- `acknowledgement_state`

Recommended severity policy:

- `critical`: current-state page sources changed, latest handoff changed, public claim/status source hash changed, or approved asset hash drift occurred. Always fails validation. Acknowledgements do not suppress it.
- `review_required`: non-current-state mapped route source drift or operational/source-authority source drift. Fails unless an exact acknowledgement exists.
- `informational`: declared dependency unavailable because source root is absent, optional source-summary lag, or non-public auxiliary drift. Reports but does not fail.

`current_frontier.md` should not feed public page authority. If it lags behind `program_state.yaml` or latest handoff, the curator should report `source_summary_lag` as a diagnostic only.

### 5. Acknowledgement Semantics

Acknowledgements should be checked in, route/source-specific, and exact to the observed drift. A minimal YAML shape:

```yaml
route_path: "/project/physics/gr-derivation-roadmap/"
source_path: "github-facing/gr-derivation-roadmap-explainer.md"
severity: "review_required"
current_commit: "<40-char-source-commit>"
current_sha256: "<64-char-source-sha>"
acknowledged_by: "project owner"
acknowledged_at: "2026-06-26T00:00:00Z"
reason: "Reviewed as non-critical for this release."
expires_at: null
```

Validation rules:

- reject acknowledgements with absolute paths;
- reject unknown severities;
- reject acknowledgements for `critical` drift;
- reject stale acknowledgements whose commit or sha does not match the current drift;
- optionally warn or fail on expired acknowledgements, depending on Q-002.

### 6. Validation Wiring

Add `validate:curator` to `package.json`:

```json
"validate:curator": "python3 scripts/run_curator.py --check"
```

Update `npm run validate` to include curator validation after manifest/content/link/provenance checks and before Cloudflare/build, unless implementation proves the provenance split requires a slightly different order.

Important refactor:

- keep `validate_page_provenance.py` fail-closed for route shape, missing route files, local page hash drift, safe relative paths, schema-level consistency, and private path leakage;
- move upstream source hash drift from hard provenance failure into the curator so severity and acknowledgement behavior can function.

This preserves fail-closed behavior for critical drift while allowing reviewed acknowledgement for non-critical drift.

## Implementation Phases

1. Snapshot contract and parser: create deterministic current-state data from upstream source files with no public auto-refresh.
2. Current-state page and navigation: add the static Astro route, source notice, route cards, and route/provenance entries.
3. Curator reports: add dependency collection, drift detection, deterministic JSON and Markdown output, and private-path guards.
4. Severity, acknowledgements, and validation: add acknowledgement parsing, severity failure rules, provenance drift split, and `npm run validate:curator`.
5. Final QA: run unit tests, full validation, build, and representative desktop/mobile browser QA.

## Validation Plan

- Static checks:
  - `npm run validate:links`
  - `npm run validate:provenance`
  - `npm run validate:curator`
- Unit tests:
  - `python3 -m pytest`
- Build:
  - `npm run build`
  - `npm run validate`
- Quality gate:
  - `npm run quality`
- Browser checks:
  - Run Astro dev or preview locally.
  - Use Playwright desktop and mobile checks for `/project/physics/current-state/`.
  - Confirm one `h1`, no overlapping metadata, internal links work, source notice is visible, and blocked claims are readable.
- Documentation or manifest validation:
  - `python3 scripts/generate_page_provenance.py`
  - `npm run validate:manifests`
  - `npm run validate:provenance`

Do not claim commands passed unless they are actually run during implementation.

## Security, Privacy, And Reliability Notes

- Data validation: current-state snapshot and curator reports must fail closed on missing required fields, malformed hashes, unknown severities, unsupported acknowledgement shape, or unsafe paths.
- Permissions and access control: no backend or user permissions are introduced.
- Abuse cases and rate limits: not applicable for a static site, but scripts must avoid following unsafe path traversal entries.
- Privacy concerns: public pages and reports must not include absolute local paths, home directories, machine names, or private runtime details.
- Failure modes:
  - source root absent: report informational or explicit source-root-unavailable diagnostic, not a false source claim;
  - latest handoff missing: critical for current-state refresh;
  - route source drift: severity-dependent validation outcome;
  - checked-in report stale: fail curator validation.
- Observability: `curator/reports/latest.md` is the human review surface; `latest.json` is the deterministic machine surface.

## Rollout And Rollback Plan

- Rollout:
  - Implement in one branch as several small vertical commits or one draft PR with task sections.
  - Run `npm run validate` and representative browser QA before merge.
- Migration/backfill:
  - Generate the initial current-state snapshot from live upstream state.
  - Add current-state route provenance and curator reports in the same reviewed edit.
- Feature flag or staged release:
  - Not needed for static route. If risk is high, first merge curator in report-only mode, then enable validation failure in a second task.
- Rollback:
  - Remove the current-state route from navigation and route map.
  - Remove `validate:curator` from `npm run validate`.
  - Keep curator reports and snapshot as review artifacts if useful, but do not serve them publicly.
- Monitoring:
  - Use `npm run validate:curator` in normal local and CI validation.
  - Review `curator/reports/latest.md` after upstream source changes.

## Out Of Scope

- Whole-repository upstream monitoring.
- Automatic rewriting of website copy, public manifests, source manifests, assets, or page text.
- Publishing curator reports as website routes or public assets.
- Treating website validation, curator acknowledgements, or successful builds as scientific authority.
- Completing the physics derivation, constructing `g_eff`, adopting `MetricData(E)`, deriving matter coupling, deriving Einstein equations, or promoting the exact-GR benchmark.
- Deployment.

## Can It Be Improved?

An improvement will be to treat curator output as a future internal dashboard after the report schema proves stable. A different perspective will be to generate a "source refresh packet" from curator reports: a small review bundle containing changed dependencies, suggested website files, and exact commands. That should remain deferred until acknowledgement semantics are reliable.

## Final Review Checklist

- [x] Every PRD requirement is mapped to a task or explicitly deferred.
- [x] Functional and non-functional requirements are represented.
- [x] Explicit exclusions and constraints are preserved.
- [x] Open questions are classified by impact.
- [x] Repository architecture was inspected before planning.
- [x] Existing patterns are preferred over new abstractions.
- [x] New dependencies, migrations, and broad refactors are avoided unless justified.
- [x] Likely affected files and directories are named.
- [x] Security, privacy, reliability, observability, rollout, and rollback are considered.
- [x] The plan avoids direct coding.
- [x] Commands were discovered from the repository.
- [x] Product questions are separated from implementation decisions.
