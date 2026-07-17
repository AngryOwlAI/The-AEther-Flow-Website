---
name: continue-goal
description: Explicitly launch a finite governed website goal across fresh Codex tasks. Use only when the user expressly requests recursive fresh-task continuation and provides or confirms an auditable completion contract and finite guards.
---

# Continue Website Goal

## Purpose

Launch the experimental, durable, fresh-task continuation relay. The launcher
reserves one generation and dispatches one token-bound worker. It executes no
website job, invokes `continue` zero times, and never evaluates the goal as
complete.

Normal bounded implementation should use `implementation-control` or
`continue`. Do not infer permission to launch this relay from words such as
"finish" or "keep going"; fresh recursive tasks must be explicit.

## Required Inputs

- Exact goal text without secrets
- Auditable completion-contract JSON
- Finite guard JSON covering pass, deadline, repeated-state, and handoff limits
- Current predecessor Codex task ID
- Explicit authorization for fresh recursive tasks

Mutable goal state is plaintext under ignored `.local/sys4ai/continuation/`.
Reject credentials, tokens, private keys, or other secrets.

## Launch Procedure

1. Re-resolve website Git and implementation-control state.
2. Run:

   ```bash
   npm run continue:goal -- launch --phase reserve \
     --goal-file <goal-file> \
     --completion-contract <contract.json> \
     --guards <guards.json> \
     --predecessor-task-id <task-id>
   ```

3. The command reserves exactly one successor intent and writes protected
   manual handoff artifacts. It does not execute project work.
4. If the host's Codex task tools are available, create exactly one fresh task
   using the returned non-executing `reservation_prompt`.
5. Persist the returned task ID before activation:

   ```bash
   npm run continue:goal -- launch --phase adopt \
     --goal-id <goal-id> \
     --generation <generation> \
     --expected-revision <revision> \
     --envelope-sha256 <sha256> \
     --adopt-task-id <fresh-task-id>
   ```

6. Send the exact protected activation prompt to that recorded task once.
7. Stop the predecessor immediately. Do not wait, execute a job, or create
   another successor.

If automatic task tools are unavailable, return the protected manual handoff
paths for explicit adoption. If task creation or activation delivery is
ambiguous, record `recover --action delivery-unknown` and do not retry.

## Invariants

- Website jobs executed by launcher: zero.
- `continue` calls by launcher: zero.
- Successor creation attempts: at most one.
- Every goal has finite immutable guards and an immutable completion contract.
- The goal never widens website authority.
- Validation never launches a real goal or creates a Codex task.

## Recovery

Use `npm run continue:goal -- recover --action inspect --goal-id <goal-id>`
first. Recovery is explicit and evidence-driven; it cannot erase history,
rerun consumed work, or silently create a second task.

