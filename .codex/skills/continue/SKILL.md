---
name: continue
description: Resolve and execute zero or one existing The AEther Flow Website implementation-control job. Use only when explicitly asked to continue governed website implementation or when invoked once by the token-bound continue-implementing-goal worker.
---

# Continue One Website Job

## Purpose

Advance the website through zero or one job selected by the existing
`implementation_control/` system. This skill adapts the pinned portable
`continue` contract; it does not create an AgentJob, recurse, spawn a task, or
replace website control records.

## Authority Order

1. `AGENTS.md` and `CONTEXT.md`
2. `implementation_control/program_state.yaml`
3. Active website Task, Job, Completion, and Handoff records
4. Current Git and validator evidence
5. Goal context only as non-authoritative routing context

The durable goal never widens the resolved job.

## Procedure

1. Run `npm run continue:implementation` and inspect the exact resolved
   boundary.
2. Capture the canonical website snapshot through
   `scripts/implementation_control/goal_relay_adapter.py`.
3. Stop with a structured zero-job result for an approval gate, missing
   checkpoint authority, blocked control, no action, or repository mismatch.
4. If the resolver is ready and the invocation authorizes execution, follow
   `.codex/skills/implementation-control/SKILL.md` and execute at most one
   existing job.
5. Complete its required records and validators without crossing any allowed
   path or source-authority boundary.
6. Checkpoint only when the live job separately grants checkpoint authority.
7. Capture the final website snapshot and return one
   `sys4ai.continue-result.v1` record.
8. Stop. Do not inspect or execute a second job.

## Result Requirements

The result must identify the website task, job, completion, and handoff IDs;
before and after fingerprints; validator counts; checkpoint evidence; progress
effect; stable reason code; and next lawful action. If the bounded call's
outcome is ambiguous, return `unknown` and enter recovery. Never retry it.

## Invariants

- AgentJobs executed: zero or one.
- Codex tasks created: zero.
- Goal metadata grants no additional reads, writes, validators, approvals,
  checkpoint rights, claims, or external effects.
- Push, deployment, source refresh, public-claim promotion, and upstream writes
  remain unavailable unless separately authorized by live records and the
  user.

## Validation

```bash
npm run validate:goal-relay
npm run validate:implementation-control
```

