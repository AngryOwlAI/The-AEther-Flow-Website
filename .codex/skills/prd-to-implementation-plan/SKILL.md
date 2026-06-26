---
name: prd-to-implementation-plan
description: Convert a PRD, product spec, feature brief, issue, or requirements document into a Codex-ready implementation plan for the Codex app, Codex IDE extension, or Codex CLI. Use when the user asks for planning before coding, task breakdowns, vertical slices, acceptance criteria, validation commands, or PR-ready work packets from a PRD. Do not use for direct implementation unless the user explicitly asks to code after the plan.
---

# PRD to Implementation Plan

## Overview

Transform a product requirements document into an actionable engineering
implementation plan that Codex can execute in small, reviewable, validated
tasks. Produce a plan, not code, unless the user explicitly asks to implement
after planning.

This skill bridges product intent and engineering execution. Do not merely
summarize the PRD; map requirements to code areas, implementation phases, test
strategy, risks, and Codex-ready task packets.

## Operating Principles

- Prefer repository evidence over guesses. Inspect relevant files, docs,
  package manifests, test commands, existing patterns, and `AGENTS.md` when
  present.
- Keep tasks small enough for one branch or one draft PR.
- Prefer vertical slices over horizontal layers when feasible.
- Preserve traceability from each PRD requirement to tasks, acceptance criteria,
  and validation.
- Mark assumptions, blockers, deferred work, and out-of-scope items clearly.
- Use Codex-friendly task packets with `Goal`, `Context`, `Constraints`, and
  `Done when`.
- Make validation executable whenever possible. Use discovered project commands
  rather than invented commands.
- Avoid broad rewrites, new dependencies, migrations, or architecture changes
  unless the PRD or existing architecture justifies them.

## Activation and Input Discovery

Use this skill when the task is to convert a PRD or feature specification into
an implementation plan.

Locate the PRD from one or more inputs:

- A user-provided path such as `@docs/PRD.md` or
  `docs/prds/profile-editing.md`.
- The open editor file or selected text in the Codex IDE extension.
- A pasted PRD, issue body, ticket description, README section, or design
  document.
- A repository search for names such as `prd`, `requirements`, `spec`,
  `proposal`, `rfc`, or `feature`.

If no PRD or equivalent input is available, ask for the PRD path or content. If
the PRD is partial but usable, proceed and record missing details under `Open
Questions`.

Honor optional user inputs such as target output path, milestone, areas to
avoid, required test levels, deployment constraints, migration constraints,
compliance constraints, accessibility constraints, security constraints, and
whether the user wants only a plan, only task packets, or both.

## Required Workflow

### 1. Intake the PRD

Read the PRD and extract product goal, users, jobs to be done, functional
requirements, non-functional requirements, acceptance criteria, user stories,
primary flows, edge cases, error states, analytics, observability, rollout,
migration needs, explicit exclusions, and constraints.

Normalize vague requirements into testable statements when possible. Do not
silently invent product behavior. Record inferred behavior as an assumption.
Read `references/prd-intake-checklist.md` when the PRD is long, vague, or
multi-stakeholder.

### 2. Scan Repository Context

Before planning implementation, inspect the repository with read-only intent.
Look for:

- `AGENTS.md` or `AGENTS.override.md` repository rules.
- Existing implementation patterns related to the feature.
- Frameworks, languages, package managers, build systems, and test tools.
- API routes, service boundaries, UI routes, components, stores, models,
  database schemas, migrations, fixtures, and test directories.
- Existing validation commands in package manifests, Makefiles, CI configs,
  README files, or docs.
- Prior features with similar shape.

Do not modify code during the scan. Prefer safe read-only commands such as file
listing, manifest reads, symbol search, and test discovery commands that do not
change state.

For The AEther Flow Website, preserve the source-authority boundary: upstream
source files, registries, and governed task records remain authoritative for
scientific, mathematical, governance, and research-workflow claims.

### 3. Build a Requirement Map

Create a traceability map from PRD requirements to engineering work. For each
requirement, identify:

- Requirement ID or short label.
- User-visible behavior.
- Likely code areas.
- Data or API impact.
- UI impact.
- Test coverage needed.
- Dependencies on other tasks.
- Open questions or assumptions.

Use stable IDs such as `REQ-001`, `REQ-002`, and `NFR-001` if the PRD lacks
IDs.

### 4. Identify Blockers and Assumptions

Ask clarification questions only for blockers that prevent a credible plan.
Limit questions to the smallest useful set. If progress is possible, proceed
with reasonable assumptions and record them under `Assumptions`.

Classify uncertainty as:

- `Blocking`: must be answered before implementation.
- `Planning assumption`: enough to plan, must be confirmed before coding.
- `Implementation detail`: can be decided during a task.

### 5. Design the Implementation Plan

Produce a plan that includes:

- Proposed architecture and approach.
- Files and directories likely affected.
- New files likely needed.
- Data model, schema, migration, or fixture changes.
- API or contract changes.
- UI, state management, routing, copy, and accessibility changes.
- Error handling and empty/loading states.
- Security, privacy, permissions, rate limits, abuse cases, and data
  validation.
- Observability, logging, analytics, or feature flag needs.
- Rollout, migration, and rollback considerations.
- Test strategy with executable commands when known.
- Risks, dependencies, and out-of-scope items.

Prefer an incremental path that can be reviewed in vertical slices. If a
prerequisite refactor is needed, make it explicit and justify it.

Read `references/implementation-plan-template.md` before writing a file or a
long-form chat plan.

### 6. Create Codex-Ready Task Packets

Break the plan into task packets. Each task should be suitable for one Codex
app, IDE, or CLI session and should include:

- `Goal`
- `Context`
- `Constraints`
- `Implementation notes`
- `Acceptance criteria`
- `Validation`
- `Done when`

Order tasks so each one has minimum dependency on future work. Mark tasks that
can run in parallel. Read `references/codex-task-packet-template.md` before
writing task packets.

### 7. Optimize for Codex App and Codex IDE

For the Codex app:

- Make each task self-contained because it may run in a cloud or delegated
  environment.
- Include setup assumptions, validation commands, and repository paths.
- Avoid relying on open editor state.
- Include expected output, branch or PR scope, and review checklist.

For the Codex IDE extension:

- Use `@file` references in task prompts when specific files are known.
- Mention open files, selections, or nearby examples that will improve context.
- Keep each task small enough to review diffs in the editor.
- Include a short follow-up prompt for reviewing the local diff.

For both surfaces, require validation summaries before considering a task
complete.

### 8. Validate the Plan Before Finalizing

Before presenting or writing the final plan, read
`references/review-checklist.md` and check that every PRD requirement is mapped
to at least one task or explicitly deferred, every task has acceptance
criteria, every task has validation guidance, risky changes have review or
rollback notes, the plan avoids direct coding unless requested, the plan does
not invent repository commands, and product questions are separated from
implementation decisions.

## Default Output

If the user asks for files, create this structure unless they specify
otherwise:

```text
<repo>/docs/implementation-plans/<feature-slug>-implementation-plan.md
<repo>/docs/implementation-plans/<feature-slug>-task-packets.md
```

If the user asks for a chat response only, present the same content in the
response.

## Reference Files

Read these files from this skill folder when useful:

- `references/implementation-plan-template.md`: full implementation plan
  template.
- `references/codex-task-packet-template.md`: reusable task packet template.
- `references/prd-intake-checklist.md`: PRD analysis checklist.
- `references/review-checklist.md`: final plan quality checklist.
- `examples/sample-request.md`: example prompts for the Codex app and IDE.

## Completion Behavior

When the work is complete, report:

- Files created or updated.
- Planning status.
- Number of requirements mapped.
- Number of task packets created.
- Key assumptions and blockers.
- Recommended next Codex prompt to begin implementation.

Do not claim validation commands passed unless they were actually run.
