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
3. Preserve unknown-outcome quarantine, recovery, optional finite limits, all
   non-budget guards, one-successor cardinality, and fresh-discussion
   requirements.
4. Never mutate or automatically rerun a historical
   `continue-research-goal.v1` generation.
5. Preserve v1/v2 records as reader-only bytes. New generations use the
   canonical v3 profile and bound-checkout contract.
6. This shim cannot bypass combined acceptance, accepted-effort propagation,
   one-shot topology authority, or Human Necessity Report validation.

Do not copy the former worker workflow into this shim. Direct edits require a
new migration packet, parity report, and rollback proof.

Deprecation status: compatibility only.
