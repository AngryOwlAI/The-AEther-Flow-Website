---
name: continue-research
description: Deprecated AEther compatibility name that routes one bounded invocation to the canonical continue skill.
---

# AEther compatibility shim: continue-research

This file is an activation template, not an active project integration.

Canonical skill: `continue`
Canonical template path: `skills/continue/SKILL.md`
Required adapter: `aether-research-control`
Required policy pack: `aether-research`

When this legacy name is invoked in an approved AEther adaptation:

1. Preserve the user's request and explicit project root.
2. Invoke the canonical `continue` skill with the AEther adapter and policy pack.
3. Permit zero or one AgentJob only.
4. Preserve the tracked `research_control/` authority, source validators,
   memory preflight, checkpoint provider, and scientific claim gates.
5. Return the canonical structured result under the legacy invocation name.
6. Preserve historical v1 records as reader-only evidence. For v3 relays,
   retain accepted effort and topology evidence and keep machine-fixable
   conditions nonterminal.
7. This shim cannot bypass combined goal/effort acceptance, protected
   branch/worktree authority, or human-only non-success terminal validation.

Do not copy the former workflow into this shim. Do not edit historical control
records or goal files. Direct edits to an activated shim must be replaced by a
new migration packet with renewed parity evidence.

Deprecation status: compatibility only. Remove only after the documented
support window and rollback test pass.
