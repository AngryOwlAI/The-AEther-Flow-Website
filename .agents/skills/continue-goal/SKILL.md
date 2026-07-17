---
name: continue-goal
description: Initialize one durable governed goal relay and dispatch exactly one first-generation worker.
---

# Continue Goal

## Purpose

Use this launcher to bind exact goal text and a completion contract to durable
project-local state, reserve generation 1, and dispatch one generation worker.
The launcher performs no AgentJob, does not call `continue`, does not evaluate
the goal as complete, and stops after recording the first successor identity.

## When to Use

Use this skill only when the user explicitly requests recursive fresh-thread
continuation and supplies, or confirms, a sufficiently precise completion
contract. Use a normal bounded `continue` invocation when recursion was not
explicitly requested.

Do not launch when the target repository, project root, storage backend,
ThreadProvider, or completion contract is ambiguous. Do not silently replace a
missing automatic ThreadProvider with same-thread recursion.

## Inputs

Required:

- exact goal text;
- explicit `<PROJECT_ROOT>` and repository binding;
- an auditable completion contract with required evidence;
- finite pass, deadline, repeated-state, and handoff-timeout guards;
- explicit authorization for fresh recursive discussions;
- compatible `agentjob-control` and `continue-implementing-goal` installations.

Optional inputs include a selected state backend, ThreadProvider, manual
handoff preference, and non-secret project context.

The goal and contract are stored as plaintext local state. Reject apparent
credentials, private keys, access tokens, or other secrets rather than storing
them.

## Outputs

Return a launcher summary containing the goal ID, generation, envelope hash,
provider status, successor identity or manual handoff path, current revision,
and exact next action. The summary is not execution or completion evidence.

## Procedure

1. Validate capabilities, explicit repository identity, storage paths, and the
   completion contract without changing project work.
2. Initialize one immutable goal identity and fixed guard set.
3. Reserve generation 1 with a random handoff token and deterministic
   idempotency key.
4. Render and validate one continuation envelope and exact worker prompt.
5. Ask the selected ThreadProvider to create one fresh successor, or write one
   manual handoff artifact when automatic creation is unavailable.
6. Record the successor identity only after provider evidence is available.
7. Transfer the generation lease to the recorded successor.
8. Return the launcher summary and stop. Do not perform project work or wait for
   the worker to finish.

## Invariants

- AgentJobs executed by the launcher: zero.
- Worker discussions created or reserved: exactly one on successful dispatch.
- Provider create calls: at most one for the reserved generation.
- The original goal text and completion contract are immutable.
- Provider ambiguity enters recovery; it never authorizes a second dispatch.
- Manual handoff never reuses the launcher discussion as generation 1.

## Validation

```text
python3 scripts/skills/validate_skill_manifest.py --manifest skills/continue-goal/skill.yaml
python3 -m unittest discover -s skills/agentjob-control/tests -p 'test_goal_launcher.py' -v
```

## Failure Modes

- Missing capability or repository mismatch: create no goal and report the
  exact blocker.
- Ambiguous contract: obtain explicit user confirmation before initialization.
- Provider failure before external creation: preserve the reservation for
  bounded recovery or cancellation.
- Unknown provider outcome: quarantine the generation and reconcile identity;
  never call the provider again automatically.
- Manual handoff pending: return the exact prompt and adoption requirements.

## Required role posture

- **System Analyst:** define the durable goal, completion contract, evidence
  gaps, assumptions, and stop conditions.
- **System Engineer:** define relay guards, generation transitions, role
  boundaries, verification, recovery, and handoff.
- **Software Engineer:** operate the file-backed goal runtime, adapters, tests,
  and state revisions without weakening concurrency or idempotency controls.

## System-agnostic interpretation

Bind the durable goal to a target agentic system and repository through the
declared adapters. Do not assume a native goal API, provider, domain, branch,
or project control layout.

## Domain emphasis

The relay proves only governed continuation and completion-contract evidence.
Use a domain pack and independent validators for the content of the work and
for any claim promotion.

## Authority boundaries

Read only bound goal, repository, control, and verification evidence. Write
only declared goal state and receipts. Do not invent guard values, spawn an
unbounded relay, bypass confirmation, or equate worker prose with completion.

## Completion receipt

Report goal state and revision, generation, guard consumption, direct evidence,
fingerprints, validators, recovery state, terminal decision, and next action.

## Provenance

Derived from a project-specific skill and generalized as a reusable template. Original project-specific names, paths, assumptions, and private operational details were removed or replaced with parameters.

## Adaptation Guide

When adapting this skill to a specific project:

- bind a project-local state root outside installed skill directories;
- select a supported state backend and ThreadProvider;
- declare repository identity and finite guards;
- add domain evidence requirements only to the completion contract or policy;
- preserve launcher-only behavior and one-successor dispatch.
