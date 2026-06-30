# Implementation Control

This directory is the live website-local control surface for continuing
implementation work in The AEther Flow Website.

It is intentionally smaller than the upstream research-control system. Its job
is to preserve bounded execution, source-authority discipline, and durable
handoffs for website implementation packets. It does not route physics claims,
grant scientific authority, push commits, deploy the site, or mutate the
upstream research project.

## Authority Order

Use this order when deciding what a future implementation session may do:

1. Repository instructions in `AGENTS.md` and vocabulary boundaries in
   `CONTEXT.md`.
2. Live implementation-control records in this directory, especially
   `program_state.yaml`.
3. Active task, job, completion, and handoff records under
   `implementation_control/`.
4. Current Git state and validator output.
5. PRDs and `ImplementationPlans/` files as route context only.
6. Memory or conversation summaries as navigation aids only.

The upstream project at `/Volumes/P-SSD/AngryOwl/The-AEther-Flow` remains
read-only for this system. Website implementation may inspect upstream source
material for provenance and source-authority checks only when a task allows
that read. It must not write there.

## Record Types

`program_state.yaml`
: Current implementation-control pointer. It names the active task, current
job, latest handoff, repository boundary, required validators, and next
recommended action.

`tasks/WI-YYYYMMDD-NNN/00_TASK.yaml`
: One bounded implementation task. It records scope, requirements, allowed
reads, allowed writes, required validators, approval gates, stop conditions,
and checkpoint expectations.

`tasks/WI-YYYYMMDD-NNN/jobs/WJ-*.yaml`
: One executable job inside a task. A future resolver should report at most one
active job per invocation.

`tasks/WI-YYYYMMDD-NNN/jobs/completions/WJC-*.yaml`
: Completion records. They summarize completed work, validator results,
changed files, remaining risk, and checkpoint readiness after a job has enough
evidence to be committed.

`handoffs/WH-*.yaml` and `handoffs/WH-*.md`
: Machine-readable and human-readable handoff pair for the same state
transition. The YAML file is the structured record; the Markdown file is the
operator summary.

## Lightweight Schema

All YAML records use a small explicit schema:

- `schema_version`
- `record_type`
- stable record identifier, such as `task_id`, `job_id`, or `handoff_id`
- `status`
- timestamps in UTC
- repository boundary and source-authority boundary fields
- allowed read paths
- allowed write paths
- approval gates
- required validators
- stop conditions
- checkpoint expectations
- next recommended action

Paths in allowed write lists must be repo-relative unless a future validator
defines a narrower safe exception. Absolute upstream write paths are forbidden.
Public routes, public assets, public manifests, source-derived claim content,
pushes, and deployments require explicit task approval before they can appear
in an allowed write list.

## Approval Gates

A task or job must declare gate status for high-risk categories:

- public scientific, mathematical, governance, or workflow claim changes
- source-refresh uncertainty
- broad navigation or route retirement
- shared visual systems
- public downloadable assets
- public manifest authority records
- Git push
- Cloudflare or production deployment
- upstream source-project writes

Allowed gate status values are:

- `not_required`
- `required`
- `approved`
- `blocked`

If a gate is `required` and not `approved`, execution must stop before the
risky change.

## One-Packet Execution

Future continuation work must execute at most one bounded task packet per
invocation. If live state and a plan disagree, live state wins. If a task needs
broader work than its allowed paths or approvals permit, stop and write a
handoff instead of widening scope.

## Normal Operating Sequence

Use this sequence for future website implementation packets:

1. Run `npm run continue:implementation` or
   `npm run continue:implementation -- --summary`.
2. Inspect the active task, active job, approval gates, allowed writes,
   validators, stop conditions, and source-authority boundary.
3. Execute exactly one bounded packet inside the active allowed write scope.
4. Write or update the completion record and handoff pair.
5. Run the focused validators named by the job and any broader validation
   required by the task.
6. Run `npm run checkpoint:implementation` to create one local commit.
7. Push or deploy only after separate explicit instruction.

## Validation And Checkpoint Expectations

`validate:implementation-control` checks the structural integrity of the live
control records and is wired into `npm run validate` before the build step. It
does not grant source authority, public claim approval, Git push approval,
deployment approval, or upstream write permission.

`checkpoint:implementation` is the narrow local commit endpoint. It validates
the implementation-control records, requires an active completion record, runs
the active job's required validators, stages only completion-listed files that
also fit the active task/job allowed write paths, and creates one local Git
commit. It fails closed when unrelated staged files would enter the commit or
when dirty files overlap the active allowed write scope without being listed in
the completion record.

The checkpoint command does not push, deploy, refresh upstream state, mutate
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`, or invent completion evidence.
