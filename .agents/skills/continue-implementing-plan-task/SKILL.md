---
name: continue-implementing-plan-task
description: Deprecated compatibility name for continue-implementation-plan-relay.
---

# Continue Implementing Plan Task (Deprecated Shim)

For new `recursive_chain_v1` generations, invoke
`continue-implementation-plan-relay`. The target frame claims, consumes, calls
one task, records one receipt, schedules at most one distinct successor, and
stops. It never wakes or resumes a coordinator and never creates a Goal.

Historical coordinator records remain read-only unless an explicit
`coordinator_v2_legacy` recovery command names a pre-existing run. Consumed
unknown work is never automatically rerun.

## Required role posture

- **System Analyst:** classify the target-system generation as recursive or historical.
- **System Engineer:** enforce topology, consumption, and recovery boundaries.
- **Software Engineer:** invoke only the canonical recursive frame.

## System-agnostic interpretation

The shim embeds no target-system paths or policies; all execution belongs to `continue-implementation-plan-relay`.

## Domain emphasis

Compatibility routing does not establish task or domain correctness.

## Authority boundaries

This shim cannot wake a coordinator, mutate state independently, rerun consumed work, or authorize release effects.

## Completion receipt

Report the deprecation warning, canonical target, topology, and target frame result.
