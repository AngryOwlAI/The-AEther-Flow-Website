---
name: continue-implementing-plan-task
description: Consume one immutable plan-task envelope, execute at most one bounded continuation for that task, verify it, and stop.
---

# Continue Implementing Plan Task

## Purpose

Use this internal template for one reserved task of an accepted implementation
plan. A future adapted runtime validates exact plan, task, thread, repository,
generation, token, and revision identity; consumes the invocation at most once;
calls `continue` at most once; verifies direct evidence; and stops after one
task receipt or protected stop.

This experimental `0.1.0` template includes the durable profile-aware worker,
PlanTaskReceipt v2 persistence, and protected recovery boundary.

## Invocation Boundary

Normal entry for a new run requires a valid
`sys4ai.plan-task-envelope.v2` record and a fresh
discussion whose identity matches the recorded provider receipt. Reject
missing, stale, reused, or mismatched identities before consumption.
Legacy v1 envelopes remain readable but cannot enter the v2 writer silently.

## Inputs

- Explicit `<PROJECT_ROOT>`;
- plan ID and hash;
- exactly one task ID and task hash;
- generation, handoff token, idempotency key, and expected revision;
- repository binding and matching successor discussion identity;
- inherited execution profile, verified provider/current-thread evidence, and
  observed pre-task topology; and
- target-project validators and authority.

## Outputs

Return one bounded result identifying the task, direct invocation count,
AgentJob count, validators, fingerprints, completion or protected-stop
disposition, and exact next action. Do not start another task in the same
discussion.

## Procedure

1. Validate exact plan-task envelope and canonical reservation identity.
2. Before mutation, compare envelope, canonical, provider, current-thread,
   repository-binding, and topology evidence.
3. Claim the generation and run pre-execution guards.
4. Consume the single task invocation immediately before calling `continue`.
5. Invoke `continue` exactly once for the bound task and no other task.
6. Verify changed paths, task acceptance evidence, validators, checkpoint, and
   repository fingerprint.
7. Verify post-task topology and finalize one PlanTaskReceipt v2 or protected
   stop with profile/topology evidence.
8. If the task cannot fit, record `task_requires_replan`; do not create a
   second discussion for the same task ID.
9. Return control to the plan coordinator. Do not select or start the next
   task from this worker discussion.

## Invariants

- Plan tasks per worker discussion: exactly one.
- Direct `continue` invocations: at most one.
- AgentJobs: zero or one.
- Automatic rerun after consumption or unknown outcome: forbidden.
- Same-task successor discussions: forbidden.
- Static worker effort: forbidden; inherit the applicable envelope profile.
- Profile or topology mismatch before claim consumes no invocation or AgentJob.
- Plan-task records never change generic goal-record meaning.

## Required role posture

- **System Analyst:** re-evaluate the target-system evidence, bound task,
  assumptions, dependencies, and acceptance conditions.
- **System Engineer:** preserve exact task identity, one-invocation controls,
  verification, recovery, and replanning boundaries.
- **Software Engineer:** execute and validate at most one bounded AgentJob for
  the bound task through the adapted runtime.

## System-agnostic interpretation

Advance exactly one task for a target system through project-defined plan,
repository, control, validation, and checkpoint providers. No project workflow
or domain semantics are implicit.

## Domain emphasis

This worker governs one-task process integrity. Apply a selected domain pack
to the task product; a valid task receipt does not by itself prove domain
correctness.

## Authority boundaries

Read only the bound plan task and target-system evidence. Write one authorized
task lifecycle and receipt through adapted interfaces. Never widen the task,
start a second task, infer protected authority, or rerun consumed work.

## Completion receipt

Report exact plan/task identity, direct invocation and AgentJob counts,
fingerprints, validators, checkpoint evidence, task disposition, recovery
status, and the coordinator's next lawful action.

## Validation

```text
python3 scripts/skills/validate_skill_manifest.py --manifest skills/continue-implementing-plan-task/skill.yaml
python3 -m unittest discover -s skills/implementation-plan-goal/tests -p "test_*.py" -v
python3 -m unittest discover -s scripts/skills/tests -p "test_implementation_plan_*.py" -v
```

## Failure Modes

- Invalid plan, task, token, thread, envelope, or revision: reject before
  consumption.
- Unknown invocation outcome: quarantine and require explicit recovery.
- Validation, checkpoint, human, capability, or repository stop: preserve the
  protected boundary.
- Oversized task: record `task_requires_replan` with proposed replacement IDs.
- Attempted second task: stop without execution.

## Adaptation Guide

Bind the durable plan store, `continue` capability, repository and checkpoint
providers, task receipt, recovery, and target-project validators. Preserve
at-most-once consumption, one-task cardinality, separate record semantics, and
append-only supersession.

## Provenance

Derived from a generic token-bound goal worker and generalized for one task of
an accepted implementation plan. Project-specific identifiers, paths, and
operational state were removed.
