---
name: implementation-plan-goal
description: Deprecated compatibility name for implementation-plan-relay.
---

# Implementation Plan Goal (Deprecated Shim)

This name is retained for one compatibility window. For every new accepted
run, invoke the canonical `implementation-plan-relay` skill and use
`recursive_chain_v1`.

The shim creates no native Codex Goal, no generic outer goal, and no persistent
coordinator. It executes no task. Coordinator-mode historical records are
read-only unless an operator explicitly selects the archived
`coordinator_v2_legacy` path for a named pre-existing run.

Warning: do not use `run_to_goal`, `notify_coordinator`, `answer_and_resume`,
wait/resume transport, or `goal_reached` terminology for a new run. Follow the
canonical launcher's one-intent/one-successor/stop contract.

## Required role posture

- **System Analyst:** identify whether the target-system request is new recursive work or legacy inspection.
- **System Engineer:** enforce the profile boundary and canonical redirect.
- **Software Engineer:** invoke only the supported target without adding shim logic.

## System-agnostic interpretation

The shim carries no project assumptions; all target-system behavior belongs to `implementation-plan-relay`.

## Domain emphasis

Compatibility routing proves neither task correctness nor domain truth.

## Authority boundaries

This shim has no independent mutation, task, Goal, coordinator, or release authority.

## Completion receipt

Report the deprecation warning, selected canonical target/profile, and redirect result.
