---
name: continue-implementing-goal
description: Hidden token-bound worker for one governed website goal generation. Use only from a recorded continue-goal activation or explicit recovery; consume one generation and call continue at most once.
---

# Continue Implementing One Website Goal Generation

## Invocation Boundary

Normal invocation requires the exact protected envelope, its SHA-256, expected
state revision, goal ID, generation, handoff token, and the recorded fresh
Codex task identity. Reject missing or mismatched identity before consuming the
generation.

Implicit invocation is disabled. Direct user invocation is recovery-only.

## Worker Procedure

1. Run the facade's `worker --phase prepare` with the exact activation values.
2. Before the generation is consumed, the facade writes an append-only
   activation receipt containing the exact Git binding and hashes of the active
   program state, task, job, completion, and handoff pointers.
3. Any Git, repository, task, job, handoff, completion, approval, checkpoint,
   or source-authority mismatch blocks before execution.
4. If preparation returns `continue_authorized`, invoke the project-local
   `continue` skill exactly once. Do not call it from any other path.
5. If the call boundary is ambiguous, run `worker --phase unknown` and enter
   recovery. Never retry the consumed generation.
6. After a definite return and completed website packet, supply exact
   completion-contract results and run `worker --phase finalize`.
7. The facade verifies portable result schema, direct validator/checkpoint
   evidence, fingerprints, and the immutable contract.
8. Terminalize, or reserve at most one fresh successor when the goal remains
   unmet and a lawful route exists.
9. If a successor is reserved, create one fresh Codex task using its
   non-executing reservation prompt, persist that identity with
   `worker --phase adopt-successor`, deliver the activation prompt once, and
   stop immediately.

## Invariants

- `continue` calls per generation: at most one.
- Website jobs per generation: zero or one.
- Successors per generation: at most one.
- A goal never supplies missing approval or checkpoint authority.
- A task creation or delivery ambiguity enters recovery without retry.
- Relay state is excluded from the website fingerprint.
- Push, deploy, source refresh, public-claim promotion, and upstream writes
  remain separately governed and unavailable by default.

## Recovery

Inspect first:

```bash
npm run continue:goal -- recover --action inspect --goal-id <goal-id>
```

Recovery may reconcile direct evidence or cancel with explicit authority. It
may not mutate immutable goal identity, erase receipts, reuse a consumed
generation, or assume a task was not created merely because its ID is missing.

