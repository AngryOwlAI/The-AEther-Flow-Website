# Website Information-Space Implementation Plans

## Purpose

This directory contains the implementation-plan layer generated from the
reviewed website information-space PRD family.

The plans are planning and control artifacts. They do not create scientific,
mathematical, governance, public-claim, deployment, source-refresh, or upstream
source authority. Public website implementation still requires fresh
implementation-control records for each bounded route or route-family packet.

## Governing Sources

- Master PRD:
  `PRDs/website-information-space/PRD-00-master-website-information-space.md`
- PRD family index:
  `PRDs/website-information-space/README.md`
- Requirements-readiness review:
  `PRDs/website-information-space/PRD-FAMILY-VALIDATION-REVIEW.md`
- Canonical greenfield rebuild plan:
  `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Canonical greenfield rebuild task packets:
  `ImplementationPlans/sitewide_greenfield_rebuild_task_packets.md`

When this directory and the sitewide greenfield rebuild plan disagree, the
sitewide greenfield rebuild plan is canonical for route model, page grammar,
validation profile, owner-review loop, and old-route retirement sequencing.

## Display-Spelling Rule

Use `Æther` in reader-facing text.

Use `aether` only for links, slugs, file naming, package names, repository
paths, or existing machine-facing identifiers.

Existing source paths such as `The-AEther-Flow` remain unchanged because they
are repository identifiers, not display copy.

## Conversion Order

`PRD-00` produces the master implementation plan and master task-packet set.
Every other PRD produces a sub implementation plan in a later governed packet,
one packet at a time.

| Order | Source PRD | Planned output | Status |
| --- | --- | --- | --- |
| 1 | `PRD-00-master-website-information-space.md` | Master implementation plan and master conversion task packets | complete |
| 2 | `PRD-10-website-positioning-guidance.md` | `PRD-10-website-positioning-guidance-implementation-plan.md` and `PRD-10-website-positioning-guidance-task-packets.md` | complete |
| 3 | `PRD-05-memory-registry-and-retrieval-components.md` | `PRD-05-memory-registry-and-retrieval-components-implementation-plan.md` and `PRD-05-memory-registry-and-retrieval-components-task-packets.md` | complete |
| 4 | `PRD-06-documentation-publication-and-website-components.md` | `PRD-06-documentation-publication-and-website-components-implementation-plan.md` and `PRD-06-documentation-publication-and-website-components-task-packets.md` | complete |
| 5 | `PRD-01-high-level-components.md` | `PRD-01-high-level-components-implementation-plan.md` and `PRD-01-high-level-components-task-packets.md` | complete |
| 6 | `PRD-02-physics-and-mathematical-components.md` | `PRD-02-physics-and-mathematical-components-implementation-plan.md` and `PRD-02-physics-and-mathematical-components-task-packets.md` | complete |
| 7 | `PRD-09-current-research-frontier-for-website-use.md` | `PRD-09-current-research-frontier-for-website-use-implementation-plan.md` and `PRD-09-current-research-frontier-for-website-use-task-packets.md` | complete |
| 8 | `PRD-03-research-control-and-agent-workflow.md` | `PRD-03-research-control-and-agent-workflow-implementation-plan.md` and `PRD-03-research-control-and-agent-workflow-task-packets.md` | complete |
| 9 | `PRD-04-role-and-schema-components.md` | `PRD-04-role-and-schema-components-implementation-plan.md` and `PRD-04-role-and-schema-components-task-packets.md` | complete |
| 10 | `PRD-07-tooling-skills-scripts-and-runtime-components.md` | `PRD-07-tooling-skills-scripts-and-runtime-components-implementation-plan.md` and `PRD-07-tooling-skills-scripts-and-runtime-components-task-packets.md` | complete |
| 11 | `PRD-08-folder-and-repository-topology-components.md` | `PRD-08-folder-and-repository-topology-components-implementation-plan.md` and `PRD-08-folder-and-repository-topology-components-task-packets.md` | complete |
| 12 | `PRD-11-quick-source-map-for-site-builders.md` | `PRD-11-quick-source-map-for-site-builders-implementation-plan.md` and `PRD-11-quick-source-map-for-site-builders-task-packets.md` | complete |

## Current Outputs

- `PRD-00-master-website-information-space-implementation-plan.md`
- `PRD-00-master-website-information-space-task-packets.md`
- `PRD-10-website-positioning-guidance-implementation-plan.md`
- `PRD-10-website-positioning-guidance-task-packets.md`
- `PRD-05-memory-registry-and-retrieval-components-implementation-plan.md`
- `PRD-05-memory-registry-and-retrieval-components-task-packets.md`
- `PRD-06-documentation-publication-and-website-components-implementation-plan.md`
- `PRD-06-documentation-publication-and-website-components-task-packets.md`
- `PRD-01-high-level-components-implementation-plan.md`
- `PRD-01-high-level-components-task-packets.md`
- `PRD-02-physics-and-mathematical-components-implementation-plan.md`
- `PRD-02-physics-and-mathematical-components-task-packets.md`
- `PRD-09-current-research-frontier-for-website-use-implementation-plan.md`
- `PRD-09-current-research-frontier-for-website-use-task-packets.md`
- `PRD-03-research-control-and-agent-workflow-implementation-plan.md`
- `PRD-03-research-control-and-agent-workflow-task-packets.md`
- `PRD-04-role-and-schema-components-implementation-plan.md`
- `PRD-04-role-and-schema-components-task-packets.md`
- `PRD-07-tooling-skills-scripts-and-runtime-components-implementation-plan.md`
- `PRD-07-tooling-skills-scripts-and-runtime-components-task-packets.md`
- `PRD-08-folder-and-repository-topology-components-implementation-plan.md`
- `PRD-08-folder-and-repository-topology-components-task-packets.md`
- `PRD-11-quick-source-map-for-site-builders-implementation-plan.md`
- `PRD-11-quick-source-map-for-site-builders-task-packets.md`

- `PRD-IMPLEMENTATION-PLAN-FAMILY-VALIDATION-REVIEW.md`

## Validation Profile

Planning/control packets for this directory should run:

- `git diff --check`
- `npm run validate:implementation-control`
- `.venv/bin/python -m pytest`

Route, manifest, asset, SVG, public-copy, source-refresh, deployment, or
upstream-source work is outside this directory's current authority and requires
fresh implementation-control authorization.

## References

The Æther Flow Website. (2026). *PRD-00: Æther-Flow Website Information Space*
[Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation
plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family
Validation Review* [Requirements-readiness review].
