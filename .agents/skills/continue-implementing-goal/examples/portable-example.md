# Portable Example: One Goal Generation

## Input state

A fresh successor Codex task receives a validated continuation envelope for
goal `<GOAL_ID>`, generation `2`, together with a protected handoff-token file,
the expected envelope hash, idempotency key, and its own successor task ID.
Durable state shows the generation is reserved, unclaimed, and unconsumed.

## Expected sequence

1. Resolve the explicit project root and read current goal revision.
2. Verify goal ID, generation, exact goal hash, repository binding, successor
   identity, envelope hash, idempotency key, and handoff token.
3. Claim generation 2 through compare-and-swap and receive a protected claim
   token.
4. Record invocation consumption before calling `continue`.
5. Invoke `continue` exactly once. It executes zero or one AgentJob.
6. Record the direct structured return, or record `unknown` if the return
   boundary is uncertain.
7. Verify canonical repository fingerprint and completion-contract evidence.
8. Finalize exactly one generation receipt.
9. If the goal is unmet and guards permit a materially new route, reserve and
   dispatch at most one successor. Otherwise enter the evidence-backed
   terminal state.

## Example bounded return

```json
{
  "status": "completed",
  "agent_jobs_executed": 1,
  "task_id": "TASK-002",
  "agent_job_id": "AJ-TASK-002-001",
  "repository_fingerprint_after": "<SHA256>",
  "global_goal_evaluation": "unmet",
  "execution_performed": true
}
```

This return may justify one continuation decision; it does not itself create a
successor or prove the entire goal complete.

## Crash branch

If invocation consumption is durable but the `continue` return is uncertain,
record `unknown`, stop automatic recursion, and use the recovery runbook. Do
not invoke `continue` again with generation 2.

Authority status: the envelope, prompt, provider receipt, and this example are
non-authoritative continuity material. The activated target-project AgentJob
remains the only executable authority for project work.
