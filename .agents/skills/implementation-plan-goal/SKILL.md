---
name: implementation-plan-goal
description: Initialize a governed serial implementation-plan relay that assigns exactly one immutable plan task to each fresh worker discussion.
---

# Implementation Plan Goal

## Purpose

Use this template to turn one accepted implementation plan into a serial,
dependency-aware relay. The launcher validates immutable plan and repository
identity, selects one dependency-ready task, reserves one fresh worker
discussion, and stops without executing an AgentJob.

This experimental `0.1.0` template provides contracts, validation, additive
SQLite persistence, activation gating, provider dispatch, worker enforcement,
protected recovery, and adaptation guidance. The
strict `sys4ai.implementation-plan.v2` definition keeps accepted immutable
plan content separate from `sys4ai.implementation-plan-state.v1` mutable
lifecycle state while retaining read compatibility for the initial v1 fixture
shape. The separate `sys4ai.plan-task-receipt.v1` contract binds immutable
task, relay, repository, cardinality, direct-evidence, disposition, recovery,
replanning, coordinator, and journal evidence without changing generic goal
receipts. Five additional append-only contracts define normalization reports,
authorized plan amendments, replacement-task supersessions, provider intents,
and revision-bound deterministic selection proofs. A pure semantic checker
validates their cross-record identity, hash, replacement-graph, provider, and
first-ready-selection relationships without performing state mutation. The
read-only `planctl classify` and `planctl normalize` commands apply the frozen
seven-class source policy, preserve valid canonical plans, and synthesize only
missing required plan, phase, task, stable-ID, and split-recommendation
structure while failing closed on ambiguous authority or conflicts. Read-only
offline commands validate every record profile and canonical content hash,
cross-check state, receipts, amendment chains, supersessions, provider intents,
and selection proofs, detect plan/task drift, generate revision-bound advisory
proofs, and redact output deterministically. A hash-indexed PHASE-02 corpus
provides standalone positive records for every declared state and outcome plus
one-fault-per-file structural and semantic adversaries. New profile-aware runs
use runtime-profile version 2, envelope/provider/receipt v2, and SQLite schema
5. Legacy v1 runtime rows remain readable but cannot silently enter the new
writer path.

## When to Use

Use this skill only when:

- the implementation plan is accepted as execution authority;
- every executable task has a stable ID, hash, dependencies, and acceptance
  boundary;
- serial one-task-per-discussion execution is required; and
- the target project will supply compatible plan state, repository, and thread
  adapters during adaptation.

Do not use it to infer authority from a generated plan, execute several tasks
in one discussion, or bypass a dependency, human gate, validation failure, or
protected external effect.

## Inputs

Required:

- `<PROJECT_ROOT>`;
- a plan conforming to `schemas/implementation-plan.schema.json`;
- immutable plan and repository identity;
- explicit fresh-discussion authorization;
- combined acceptance of the exact goal and selected reasoning effort; and
- target-project adapter and validation configuration.

## Outputs

Return a launcher receipt containing the validated plan identity, deterministic
selection result, reserved task identity, plan-task envelope hash, provider
receipt, and resulting revision. The launcher executes zero AgentJobs.

## Procedure

1. Propose the exact activation goal with `reasoning_effort: max` unless the
   user explicitly selects another provider-supported effort.
2. Configure or manually attest the current discussion, then render the exact
   goal and verified requested/effective effort together. Any goal or effort
   edit invalidates prior acceptance and repeats this step.
3. Obtain combined acceptance. Before it exists, create no plan row,
   activation receipt, reservation, provider intent, worker, AgentJob,
   continuation, branch, or worktree.
4. Classify each project-contained source from its observable structure and
   bind explicit authority and precedence.
5. Normalize only when required, preserve a valid canonical plan without
   synthesis, and stop for missing authority or equal-precedence conflicts.
6. Establish that the resulting plan is accepted authority and hash its
   canonical bytes.
7. Validate the immutable plan schema, exact required scope, phase/task
   membership, and semantic dependency graphs.
8. Reject duplicate IDs, unknown dependencies, self-dependencies, cycles, or
   inconsistent completed state.
9. Atomically persist the accepted activation, plan profile, normalization
   evidence, plan row, and initialization receipt.
10. Load separately versioned plan state and select the first dependency-ready
   pending task in canonical task order. Supply exact linked receipts,
   amendments, supersessions, provider intents, and prior proofs as applicable.
   Selection is revision-bound and advisory; it never reserves or activates a
   task.
11. Bind exactly one task ID and task hash to
   `sys4ai.plan-task-envelope.v2`, including the accepted profile, topology
   policy, activation hash, and repository-binding hash.
12. Persist provider intent v2, pass the profile to exactly one provider
   create, verify exact requested/effective effort and bound-checkout
   evidence, and quarantine uncertainty without retry.
13. Require the worker to compare envelope, canonical, provider,
   current-thread, binding, and topology evidence before claim. It may invoke
   `continue` once and must write immutable plan-task receipt v2.
14. Validate any normalization, amendment, task-supersession, provider-intent,
   and selection-proof records against their separate versioned contracts and
   semantic cross-record invariants.
15. Record the provider outcome and stop. Do not execute the selected task in
   the launcher discussion.

The bundled `scripts/planctl.py` provides read-only `classify`, `normalize`,
`validate`, `validate-envelope`, `validate-record`, `validate-state`,
`select-next`, `diff`, `redact`, and `reason-codes` commands. Classification
and normalization require project-relative contained inputs and explicit
accepted authority before producing a candidate plan. Multi-source
normalization also requires explicit precedence. `select-next` retains v1
fixture compatibility and returns `state_required` for an immutable v2 plan
unless `--state` is supplied. State-aware selection requires a prior journal
hash, validates the complete supplied control view, and returns a
compare-and-swap proof without mutation. The tool is not a durable store,
mutating scheduler, provider, or launcher runtime.

## Invariants

- One envelope names exactly one plan task.
- The launcher executes zero AgentJobs.
- A worker discussion may execute zero or one AgentJob for its bound task.
- A task ID never receives an automatic second discussion.
- Oversized work stops as `task_requires_replan` and requires new,
  append-only replacement task IDs.
- A finalized plan-task receipt records zero-job, one-job, or unknown
  execution separately from task or plan disposition.
- Generated plans are not self-authorizing.
- Existing generic goal and continuation record meanings remain unchanged.
- Every new worker inherits the profile applicable to its generation and
  verifies it before claim.
- A mismatch may repair only the same unclaimed worker; it never authorizes a
  second discussion.
- Branch, worktree, or binding changes require exact revision-bound one-shot
  user authority. The default reuses the bound checkout.

## Required role posture

- **System Analyst:** establish accepted plan authority, repository truth,
  dependency state, and the earliest lawful task.
- **System Engineer:** bind one plan task to one immutable envelope, fresh
  discussion, verification contract, and recovery boundary.
- **Software Engineer:** validate the plan package and implement only the
  selected task through the target-system's adapted runtime.

## System-agnostic interpretation

Coordinate an accepted implementation plan for a target system through
project-supplied state, repository, validation, and thread interfaces. No
project taxonomy, provider, branch policy, or deployment behavior is implicit.

## Domain emphasis

This skill governs task selection and dispatch integrity. Apply an appropriate
domain pack to validate the work product; relay correctness does not establish
scientific, mathematical, product, or software correctness.

## Authority boundaries

Read accepted plan and target-system evidence. Write only authorized plan
control records through adapted interfaces. Do not execute the task in the
launcher, infer plan acceptance, bypass a gate, or perform a protected external
effect.

## Completion receipt

Report plan and task identity, validation and selection evidence, zero
AgentJobs, provider cardinality, envelope hash, resulting revision, and any
protected stop or recovery requirement.

## Validation

```text
python3 scripts/skills/validate_skill_manifest.py --manifest skills/implementation-plan-goal/skill.yaml
python3 skills/implementation-plan-goal/scripts/build_phase02_fixture_corpus.py --check
python3 -m unittest discover -s skills/implementation-plan-goal/tests -p "test_*.py" -v
python3 -m unittest discover -s scripts/skills/tests -p "test_implementation_plan_*.py" -v
python3 skills/implementation-plan-goal/scripts/planctl.py classify skills/implementation-plan-goal/templates/canonical-plan-template.json --source-root . --authority accepted --json
python3 skills/implementation-plan-goal/scripts/planctl.py normalize skills/implementation-plan-goal/examples/normalization-partial-source.example.json --source-root . --authority accepted --json
python3 skills/implementation-plan-goal/scripts/planctl.py validate skills/implementation-plan-goal/templates/canonical-plan-template.json --json
python3 skills/implementation-plan-goal/scripts/planctl.py validate-record skills/implementation-plan-goal/examples/plan-task-envelope.example.json --json
python3 skills/implementation-plan-goal/scripts/planctl.py select-next skills/implementation-plan-goal/templates/canonical-plan-template.json --json
python3 skills/implementation-plan-goal/scripts/planctl.py diff skills/implementation-plan-goal/templates/canonical-plan-template.json skills/implementation-plan-goal/templates/canonical-plan-template.json --json
python3 skills/implementation-plan-goal/scripts/planctl.py reason-codes --json
```

## Failure Modes

- Plan authority is absent or ambiguous: stop before initialization.
- Equal-precedence accepted sources conflict: return a blocking finding.
- A source escapes the configured root or contains a secret: reject it.
- Schema or dependency validation fails: return deterministic findings.
- No task is dependency-ready: return `no_ready_task` without mutation.
- Provider result is unknown: preserve the intent and require recovery.
- Current or successor effort differs from the accepted profile: reject before
  claim; repair only the same unclaimed thread when supported.
- Repository topology differs from the bound checkout: reject before claim or
  quarantine an unapproved post-task change.
- A task exceeds one discussion or AgentJob: stop for append-only replanning.
- A protected action lacks authority: record the gate and do not infer consent.

## Adaptation Guide

When adapting this skill:

- replace placeholders with target-project paths, commands, and authorities;
- bind durable plan state, repository, checkpoint, ThreadProvider, and
  ThreadExecutionProfileProvider adapters;
- preserve the separate plan-task envelope and generic continuation contracts;
- add project-specific validators without weakening one-task cardinality;
- keep mutable state outside canonical, adapted, and plugin skill trees; and
- document every project-specific assumption.

## Provenance

Derived from repository-native governed-continuation and implementation-planning
patterns and generalized as a reusable template. Project-specific paths,
operational state, and private identifiers are not part of the package.
