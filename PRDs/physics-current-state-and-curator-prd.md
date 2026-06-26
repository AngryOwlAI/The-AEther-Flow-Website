# Physics Current State And Curator PRD

## Problem Statement

The website explains the AEther Flow Project, but it does not yet provide a
clear reader-facing snapshot of the current state of the physics derivation.
Readers can see roadmap and boundary pages, but they cannot easily answer:
what is the current derivation burden, what is blocked, what changed upstream,
and when was the website last refreshed from source?

The website also needs a disciplined way to notice when the upstream AEther
Flow Project changes in ways that affect published website pages, assets, or
promotional descriptions. Without that, website copy can silently become stale
or overstate current research status. The required system must preserve the
Source Authority Boundary: it should detect and report drift, but it should not
rewrite public website pages automatically.

## Solution

Add a curated snapshot page at `/project/physics/current-state/` that presents
the current state of the physics derivation as of the last reviewed website
refresh. The page should be sourced from upstream `program_state.yaml`, the
latest handoff YAML/Markdown, and relevant derivation ledgers. It should show
last refreshed from source, source commit, active task and handoff, current
derivation burden, blocked claims, and next recommended action.

Add a repo-internal documentation curator system that checks declared website
source dependencies against the current upstream AEther Flow Project state. The
curator should be advisory and fail-closed. It should produce both a
machine-readable JSON report and a human-readable Markdown review report. It
should be part of the normal validation gate with severity control, but it
must not auto-update public pages, public manifests, or public claims.

## User Stories

1. As a general reader, I want a current-state physics page, so that I can
   understand where the derivation work currently stands without reading raw
   control files.
2. As a physics-interested reader, I want the page to identify the active
   derivation burden, so that I do not mistake a roadmap for a completed
   derivation.
3. As a reader evaluating credibility, I want visible blocked claims, so that I
   can see what the project explicitly does not claim.
4. As a returning reader, I want to see "last refreshed from source" and the
   source commit, so that I know whether the website may lag behind the living
   project.
5. As the project owner, I want the website to reflect upstream changes to
   physics and project-system descriptions, so that public explanation remains
   aligned with source state.
6. As a maintainer, I want drift detection against declared source
   dependencies, so that I receive actionable stale-page reports instead of
   noisy whole-repository alerts.
7. As a maintainer, I want a JSON curator report, so that validators and future
   automation can reason about drift deterministically.
8. As a maintainer or implementation agent, I want a Markdown curator report,
   so that I can review what changed, why it matters, and which website
   surfaces need attention.
9. As a release operator, I want curator drift to participate in normal
   validation, so that stale critical public claims cannot pass silently.
10. As a release operator, I want severity levels and acknowledgements, so that
    non-critical drift can be reviewed without permanently blocking unrelated
    work.
11. As a reader, I want only curated public results exposed on the website, so
    that internal stale-state diagnostics and draft/control paths do not become
    public content.

## Implementation Decisions

- Add a new public route at `/project/physics/current-state/`.
- Link the route from the physics landing page, GR derivation roadmap page, and
  other physics routes only where it clarifies current status.
- Treat the page as a curated snapshot, not an evergreen conceptual explainer.
- The page must not auto-update when upstream files change. Public changes
  require a reviewed website edit, regenerated provenance, and validation.
- Primary public fields should include:
  - last refreshed from source;
  - upstream source commit;
  - active task ID;
  - latest handoff ID;
  - current status;
  - current derivation milestone or burden;
  - current blocked claims;
  - next recommended action;
  - concise source-provenance links.
- Primary upstream authority for the current-state page should be
  `program_state.yaml` plus the latest handoff YAML/Markdown.
- Relevant derivation ledgers should include `DISTANCE_TO_GR_LEDGER.csv` and,
  where useful for claim-boundary display, `CLAIM_BOUNDARY_REGISTRY.csv` or the
  active handoff's blocked-claim list.
- `current_frontier.md` should not be primary authority when it disagrees with
  `program_state.yaml` or the latest handoff. In that case, the curator should
  report `source_summary_lag`.
- Extend the route/source map and page provenance model to include
  `/project/physics/current-state/`.
- Add the current-state source dependencies to the curator input set:
  `program_state.yaml`, latest handoff YAML/Markdown, selected derivation
  ledgers, and any other explicitly declared dependencies used by the page.
- The curator scope starts with website-declared source dependencies only:
  `page_route_map.json`, `page_provenance.json`, `source_manifest.json`, and
  the new current-state dependencies.
- Do not monitor the entire upstream repository in the first release.
- Add repo-internal curator artifacts:
  - `curator/reports/latest.json`;
  - `curator/reports/latest.md`;
  - `curator/acknowledgements/*.yaml`.
- Curator reports are maintenance artifacts and should not be served as public
  website pages or assets.
- The JSON report should record route, source path, old hash, new hash, old
  commit, current commit, severity, impact class, recommended action, and any
  acknowledgement state.
- The Markdown report should explain stale surfaces in review language:
  what changed, why it matters, and which website surfaces need attention.
- Add severity classes:
  - `critical`: validation fails. Examples: current-state page sources changed,
    latest handoff changed, public claim/status source hash changed, or
    approved asset hash drift occurred.
  - `review_required`: validation fails unless explicitly acknowledged in a
    checked-in curator acknowledgement file.
  - `informational`: appears in reports but does not fail validation.
- Acknowledgements should be explicit, checked in, route/source-specific, and
  reviewable. They should not suppress `critical` drift.
- Add the curator check to `npm run validate` after existing provenance and
  manifest checks, unless implementation evidence shows a safer ordering.
- The curator must report drift rather than modify website files, public
  manifests, source manifests, assets, or page copy.

## Testing Decisions

- Test that `/project/physics/current-state/` builds as a static Astro route.
- Test that the page includes one `h1`, visible source refresh metadata,
  active task/handoff, derivation burden, blocked claims, and next action.
- Test that the route is included in page provenance and route/source mapping.
- Test that curator JSON is deterministic for unchanged dependencies.
- Test that changed hashes in declared dependencies create drift entries.
- Test that `critical` drift fails validation.
- Test that `review_required` drift fails without acknowledgement and passes
  with a valid acknowledgement.
- Test that `informational` drift is reported without failing validation.
- Test that curator reports do not contain absolute local paths or private
  machine details.
- Test that `current_frontier.md` lag relative to `program_state.yaml` produces
  a diagnostic rather than public current-state authority.
- Run `npm run validate` before signoff.
- For frontend implementation, run representative browser QA for desktop and
  mobile non-overlap on the new page.

## Source Authority and Provenance

- Authoritative scientific, mathematical, governance, and workflow claims
  remain in the upstream AEther Flow Project.
- The current-state page is a reader-facing adaptation of upstream control
  state, not a source authority surface.
- The page must preserve explicit negative boundaries such as no
  `MetricData(E)` construction or adoption, no `g_eff`, no matter coupling, no
  Einstein equations, no benchmark promotion, and no completed derivation
  unless upstream source state explicitly changes.
- Source status should distinguish source commit date, source refresh date,
  website publication date, and build date.
- Curator reports may cite draft/control paths internally, but public pages
  should expose only curated source notices and provenance links.

References:

- AEther-Flow Project. (2026). `research_control/program_state.yaml` [Current
  research-control state].
- AEther-Flow Project. (2026). `research_control/handoffs/handoff-0222.yaml`
  [Latest inspected handoff metadata].
- AEther-Flow Project. (2026). `research_control/handoffs/handoff-0222.md`
  [Latest inspected handoff summary].
- AEther-Flow Project. (2026). `registries/DISTANCE_TO_GR_LEDGER.csv`
  [Derivation burden ledger].
- The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`
  [Website route/source mapping].
- The AEther Flow Website. (2026). `public/files/manifests/page_provenance.json`
  [Website page provenance manifest].
- The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`
  [Website source and asset provenance manifest].

## Out of Scope

- Whole-repository upstream monitoring in the first release.
- Automatic rewriting of website copy, public manifests, source manifests, or
  assets.
- Public exposure of curator JSON or Markdown reports.
- Treating website validation, curator acknowledgements, or successful builds
  as scientific authority.
- Completing the physics derivation, constructing `g_eff`, adopting
  `MetricData(E)`, deriving matter coupling, deriving Einstein equations, or
  promoting the exact-GR benchmark.
- Deployment. Deployment should remain a separate explicit action.

## Further Notes

- The logical implementation seam is the existing page provenance and manifest
  validation layer. Extending that layer is lower risk than inventing a
  separate publication database.
- A different perspective will be to treat the curator as a future dashboard.
  That should wait until the repo-internal reports and fail-closed validator
  behavior are proven useful.
- An improvement will be to generate a concise "source refresh packet" from
  curator reports, but only after acknowledgement semantics and severity
  classes are stable.
