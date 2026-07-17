---
name: continue-implementing-goal
description: Consume one token-bound goal generation, invoke one bounded continuation, verify it, and terminalize or dispatch one successor.
---

# Continue Implementing Goal

## Purpose

Use this internal worker only for one reserved generation of a durable goal
relay. It validates its continuation envelope, irreversibly consumes one
generation, invokes `continue` exactly once, verifies canonical evidence, and
then either terminalizes or records one fresh successor before stopping.

## Invocation Boundary

Normal mode requires all of the following:

- goal ID;
- generation number;
- random handoff token;
- expected state revision;
- continuation-envelope hash;
- successor thread identity matching the reserved provider receipt.

Reject normal invocation when any identity field is absent or mismatched.
Recovery mode is explicit, performs no automatic rerun of a consumed
generation, and requires the recovery authority described by the canonical
goal record.

Implicit invocation is disabled. A user should normally enter through
`continue-goal`; a recorded predecessor or an operator may invoke recovery.

## Inputs

Required normal-mode inputs are the token-bound identity above, an explicit
`<PROJECT_ROOT>`, compatible relay state, and access to `agentjob-control` and
`continue`. Goal and generation context never broadens the AgentJob selected by
the bounded continuation.

## Outputs

Return one worker summary containing the generation receipt, canonical before
and after fingerprints, direct invocation count, goal evaluation, terminal
state or successor receipt, current revision, and recovery status.

## Procedure

1. Validate the envelope schema, hash, repository binding, predecessor
   readiness, token, generation, successor identity, and expected revision.
2. Claim the generation lease and run all pre-execution guards.
3. Irreversibly consume the generation immediately before the bounded call.
4. Invoke `continue` exactly once and record the direct structured return. If
   the call boundary is uncertain, record `unknown` and enter recovery.
5. Verify canonical control records, fingerprints, validator results,
   checkpoint evidence, and the completion contract.
6. Evaluate the global goal as `met`, `unmet`, or `indeterminate` from direct
   canonical evidence only.
7. Terminalize for completion or a protected stop. When unmet and legally
   continuable, reserve and create exactly one fresh successor generation.
8. Record the successor identity, transfer its lease, and stop immediately.

## Invariants

- `continue` invocations per worker generation: at most one.
- AgentJobs per worker generation: zero or one, solely through that call.
- Successor reservations and provider creates per worker: at most one.
- A consumed or unknown generation is never automatically rerun.
- The worker never follows up on itself or reuses its discussion as a successor.
- Goal completion requires the immutable completion contract and canonical
  evidence; worker prose is non-authoritative.

## Recovery Mode

Recovery may classify and reconcile an interrupted generation, adopt one
uniquely proven successor, finalize an unknown result, amend only allowed guard
or contract fields through append-only authority, or cancel. It may not erase
history, mutate original goal identity, steal a lease merely because time
elapsed, or rerun consumed work.

## Validation

```text
python3 scripts/skills/validate_skill_manifest.py --manifest skills/continue-implementing-goal/skill.yaml
python3 -m unittest discover -s skills/agentjob-control/tests -p 'test_goal_worker.py' -v
```

## Failure Modes

- Invalid token, generation, thread, or revision: reject before consumption.
- Guard stop: finalize a zero-job receipt where legal and terminalize.
- Unknown bounded-call outcome: quarantine leases and require recovery.
- Validation, checkpoint, human-gate, capability, deadline, repeated-state, or
  no-progress stop: map to the declared terminal state.
- Ambiguous provider outcome: do not reserve or create another successor.

## Required role posture

- **System Analyst:** re-evaluate goal evidence, current state, assumptions, and
  the earliest incomplete dependency-ready work.
- **System Engineer:** bind one generation to one bounded continuation,
  verification contract, recovery path, and successor decision.
- **Software Engineer:** claim, consume, execute, verify, and journal the
  generation through the adapted runtime.

## System-agnostic interpretation

Act as the relay worker for a target agentic system through project-defined
repository, control, and thread providers. No project workflow or domain
semantics are implicit.

## Domain emphasis

This worker governs one continuation generation. It must invoke independent
domain or claim validation for the work product and must not treat relay
success as domain correctness.

## Authority boundaries

Read the bound goal, generation, claim, and repository evidence. Write only
authorized goal state, receipts, and bounded work outputs. Never reuse a claim,
execute multiple continuation passes, or spawn a successor before verification.

## Completion receipt

Report claim and generation identifiers, invocation result, fingerprints,
direct evidence, validator outcomes, pending or final receipt, and successor or
terminal disposition.

## Provenance

Derived from a project-specific skill and generalized as a reusable template. Original project-specific names, paths, assumptions, and private operational details were removed or replaced with parameters.

## Adaptation Guide

When adapting this skill to a specific project:

- bind the installed `continue` skill and goal-state backend;
- configure the ThreadProvider and repository adapter;
- preserve token, revision, at-most-once, lease, and fresh-discussion rules;
- add project validators without weakening terminal guard mappings;
- keep recovery explicit and evidence driven.
