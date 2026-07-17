---
name: continue-research-continue-goal
description: Deprecated AEther compatibility name that routes one relay generation to continue-implementing-goal.
---

# AEther compatibility shim: continue-research-continue-goal

This file is an activation template, not an active project integration.

Canonical skill: `continue-implementing-goal`
Canonical template path: `skills/continue-implementing-goal/SKILL.md`
Historical reader: `agentjob_runtime.compat.aether_goal_v1`

When this legacy name is invoked in an approved AEther adaptation:

1. Pass the goal ID, generation, handoff token, expected revision, envelope
   hash, and successor identity unchanged to `continue-implementing-goal`.
2. Consume at most one generation and invoke canonical `continue` at most once.
3. Preserve unknown-outcome quarantine, recovery, finite guards, one-successor
   cardinality, and fresh-discussion requirements.
4. Never mutate or automatically rerun a historical
   `continue-research-goal.v1` generation.

Do not copy the former worker workflow into this shim. Direct edits require a
new migration packet, parity report, and rollback proof.

Deprecation status: compatibility only.
