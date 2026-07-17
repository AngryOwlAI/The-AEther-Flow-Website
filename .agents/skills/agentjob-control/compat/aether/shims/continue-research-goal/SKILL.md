---
name: continue-research-goal
description: Deprecated AEther compatibility name that routes goal launch to the canonical continue-goal skill.
---

# AEther compatibility shim: continue-research-goal

This file is an activation template, not an active project integration.

Canonical skill: `continue-goal`
Canonical template path: `skills/continue-goal/SKILL.md`
Historical reader: `agentjob_runtime.compat.aether_goal_v1`

When this legacy name is invoked in an approved AEther adaptation:

1. Preserve the exact user goal text, completion contract, finite guards, and
   explicit request for fresh recursive discussions.
2. Launch through canonical `continue-goal` with the configured AEther adapter,
   policy pack, state root, and ThreadProvider.
3. Create or reserve at most one first-generation successor and execute no
   AgentJob in the launcher.
4. Treat existing `continue-research-goal.v1` records as historical reader-only
   evidence. Preserve every legacy `crg-` ID, hash, journal entry, and byte.

Do not copy the former launcher or helper into this shim. Do not store mutable
relay state under an installed skill directory. Direct edits require renewed
parity and rollback evidence.

Deprecation status: compatibility only.
