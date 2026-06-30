---
name: implementation-control
description: Trigger The AEther Flow Website's local implementation-control workflow. Use when the user asks to continue implementation, run implementation control, inspect the active implementation packet, execute one governed website implementation packet, or checkpoint a completed implementation-control packet.
---

# Implementation Control

## Purpose

Use the website-local implementation-control system before continuing governed
implementation work in The AEther Flow Website.

This skill is an operator trigger for the existing repository tooling. It does
not replace the live records under `implementation_control/`, create source
authority, push commits, deploy the site, or mutate the upstream source project
at `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.

## Use When

- The user says `continue implementation`, `/continue-implementation`,
  `implementation control`, or asks to run the governed implementation packet.
- The user asks what the active implementation-control packet is.
- The user asks to checkpoint a completed implementation-control packet.
- The user asks to resume website implementation and live control records should
  determine the lawful next step.

Do not use this skill for ordinary one-off edits unless the user asks for the
implementation-control workflow or the task clearly depends on live
implementation-control state.

## Authority Order

Use this order:

1. `AGENTS.md` and `CONTEXT.md`.
2. `implementation_control/program_state.yaml`.
3. Active task, job, completion, and handoff records under
   `implementation_control/`.
4. Current Git state and validator output.
5. PRDs and `ImplementationPlans/` only as route context.
6. Memory and conversation summaries only as navigation aids.

If live records and a plan disagree, live records win. If live records are
missing, malformed, blocked, or broader than the user's request, stop and report
the blocker instead of guessing.

## Required Workflow

### 1. Resolve The Live Boundary

From the repository root, run:

```bash
npm run continue:implementation -- --summary
```

For exact machine-readable fields, also run:

```bash
npm run continue:implementation
```

Inspect the resolved status, active task, current job, latest handoff, allowed
reads, allowed writes, approval gates, stop conditions, required validators,
source-authority boundary, and checkpoint expectations.

### 2. Decide The Execution Mode

- If the user asks only for status or inspection, report the resolved boundary
  and stop.
- If the resolver reports `blocked`, `approval_required`, or `no_action`, do not
  modify files. Report the exact condition and the logical next step.
- If the resolver reports `ready` and the user asked to continue or execute,
  perform at most one bounded packet inside the active allowed write scope.

### 3. Execute One Packet

Before editing, confirm the active job's allowed write paths. Do not widen
scope, do not touch unrelated dirty files, and do not write to the upstream
source repository.

If the work needs a path or approval gate that is not allowed by the active
task/job, stop and write or recommend a handoff instead of making the change.

Public scientific, mathematical, governance, workflow-claim, public-asset,
manifest-authority, navigation-retirement, shared-visual-system, push, deploy,
or upstream-write changes require the corresponding live approval gate.

### 4. Complete And Validate

After one packet's edits, write or update the required implementation-control
completion and handoff records if the active task expects them.

Run the validators required by the active job. At minimum, run:

```bash
npm run validate:implementation-control
```

Use `.venv/bin/python -m pytest` when Python tests are required and available.
If a documented validator is unavailable, report the exact missing command and
do not invent validation evidence.

### 5. Checkpoint Locally

When the active packet is complete and the completion record is valid, run:

```bash
npm run checkpoint:implementation
```

This creates a local commit only. It must not push, deploy, refresh upstream
state, broaden the packet, or fabricate completion evidence.

Use:

```bash
npm run checkpoint:implementation -- --dry-run
```

when the user asks for a preview or when checkpoint risk needs inspection before
mutation.

## Failure Handling

- Missing or malformed control records: stop and report the resolver or
  validator error.
- Approval required: name the gate and wait for explicit approval.
- Dirty worktree conflict: preserve unrelated user work; do not stage unrelated
  files.
- Validation failure: report the failing command and the smallest corrective
  next step.
- Request to push or deploy: require separate explicit instruction and use the
  appropriate website deployment workflow after a clean local checkpoint.

## Final Response Contract

Report:

- resolved active task and current job;
- whether work was status-only, executed, validated, or checkpointed;
- files changed, if any;
- validation commands and results;
- remaining blocker or uncertainty, if any;
- the logical next step.

If a local commit is created, emit the Codex app git commit directive in the
final response.
