# Sitewide Revamp PG-002 Analysis QA

Date: 2026-06-27

## Scope

Prepared the prerequisite system analysis for PG-002, the future
`/project/physics/distance-to-gr/` dashboard:

- Added `docs/system-analyses/distance-to-gr-dashboard.md`.
- Reviewed the committed upstream Distance-to-GR baseline at
  `6d011d527ec39178fefbcf5e614ab9a901a57a74`.
- Reviewed the local dirty upstream state only as gated evidence, not as a
  publication-authoritative source.
- Preserved the public route as blocked until the upstream source state is
  clean, committed, or explicitly accepted for website use.

## Source-State Finding

PG-002 route implementation is not yet publication-safe. The upstream
repository has uncommitted changes in Distance-to-GR-relevant records,
including `registries/DISTANCE_TO_GR_LEDGER.csv`,
`research_control/program_state.yaml`, `research_control/handoffs/handoff-0277.*`,
and `research_control/tasks/RT-20260614-244/`.

The analysis records the boundary but does not create route copy, a dashboard
snapshot, source manifest entries, or public provenance entries.

## No-AI-Slop Gate

Analysis artifact: `pass`.

Public route conversion: `block`.

Reasoning: the artifact is source-bounded, distinguishes committed baseline
from dirty working state, and refuses progress-bar or proof-like framing. The
route should remain blocked until the dashboard can cite a clean pinned source
state and avoid implying real-time synchronization.

## Validation

Planned validation for this documentation-only packet:

- `git diff --check`
- `npm run validate:content`

Full page-minimum validation, links, browser QA, route-map updates, and
provenance regeneration remain deferred until the actual
`/project/physics/distance-to-gr/` route is implemented from a pinned snapshot.

## Logical Next Step

Once upstream Distance-to-GR evidence is clean or explicitly accepted, generate
a checked-in dashboard data snapshot from the ledger, then implement the public
route using the PG-002 page-minimum validation profile.
