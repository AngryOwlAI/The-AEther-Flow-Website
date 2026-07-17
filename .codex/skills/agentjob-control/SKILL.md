---
name: agentjob-control
description: Internal website adapter for the pinned Sys4AI AgentJob schemas, durable goal state, receipts, fingerprints, and recovery runtime. Use only when a declared continuation skill needs these controls or when explicitly auditing the governed continuation installation.
---

# Website AgentJob Control

## Purpose

Provide the hidden control runtime used by the website's governed continuation
skills. The exact portable package is vendored at
`.agents/skills/agentjob-control/`; this front door binds it to this
repository's authority hierarchy.

`implementation_control/` remains the sole implementation authority. Never
bootstrap or operate `.agents/control/` in this repository.

## Invocation Boundary

- Implicit user invocation is disabled.
- Normal use is internal to `continue`, `continue-goal`, and
  `continue-implementing-goal`.
- An explicit audit may inspect schemas, the installed lock, receipts,
  fingerprints, and recovery state, but performs no implementation job.

## Website Binding

- Portable runtime: `.agents/skills/agentjob-control/`
- Source lock: `.agents/skill_registry/SKILL_LOCK.yaml`
- Adapter configuration: `.agents/continuation/website-adapter.json`
- Website adapter: `scripts/implementation_control/goal_relay_adapter.py`
- Mutable state: ignored `.local/sys4ai/continuation/`
- Implementation authority: `implementation_control/`

The adapter maps website Task, Job, Completion, Handoff, approval-gate,
checkpoint, validator, Git, and source-authority evidence into portable
records. Relay state is excluded from the canonical repository fingerprint.

## Invariants

- Do not create a competing control root.
- Do not edit vendored files in place.
- Do not infer an approval, checkpoint right, read, write, validator, or claim
  boundary from a durable goal.
- Do not use a relay receipt as scientific or publication authority.
- Do not push, deploy, refresh sources, promote public claims, or write
  upstream without separate live authority and explicit user authorization.

## Validation

Run:

```bash
npm run validate:goal-relay
npm run test:goal-relay-runtime
npm run test:goal-relay
```

These checks must not launch a goal or create a Codex task.

