# Plan-Native Recursive Relay Operator Guide

## Default topology

New runs use `recursive_chain_v1` and
`.local/sys4ai/implementation-plan-relay/state.sqlite3`. The launcher creates
generation 1 and stops. Worker N claims, consumes, executes one task, records
one receipt, and either terminalizes or records one distinct worker N+1 before
stopping. There is no persistent coordinator, native Codex Goal authority, or
generic outer goal.

The installed provider mode is currently `degraded_manual`. It emits and
adopts one externally created discussion only after exact project, checkout,
effort, idempotency, and current-thread evidence. It does not claim automatic
continuity. If an automatic provider is configured later, it must support
create/read/query-by-idempotency plus project, checkout, thread, and effective-
effort evidence.

## Safe command progression

1. `relay-prepare --launcher-thread-id <THREAD> --reasoning-effort <EFFORT>`
   is read-only and returns the plan, repository, current website-control
   fingerprints, and the exact acceptance basis.
2. Copy the complete `sys4ai.plan-relay-acceptance.v1` basis, add only
   `accepted: true` and a nonblank `acceptance_evidence_ref`, then pass that
   object to `launch`. Any plan/objective/revision/task-graph, repository,
   control, thread, effort, authority, grant, profile, or topology drift fails
   before the relay database or generation 1 exists. A successful `launch`
   commits generation 1 and one intent and runs zero AgentJobs.
3. `prepare-dispatch` consumes the sole provider-create budget immediately
   before external creation.
4. `record-successor` records the one returned child; a create uncertainty
   instead uses `reconcile-dispatch` and never a blind retry.
5. The child uses `claim-generation`, then `consume-generation` immediately
   before one task call.
6. Use `record-returned` for direct evidence or `record-unknown` for an
   uncertain consumed boundary. Unknown work is quarantined and never rerun
   automatically.
7. `finalize-receipt` and `verify-and-decide` recheck canonical and website
   control evidence. The result is completion, one successor candidate, or a
   protected stop.
8. `reserve-successor` binds N+1 to worker N and N's receipt. The worker then
   performs the same one-create/record protocol and stops.
9. `finalize-plan` validates positive plan-wide proof and atomically writes the
   report, terminal state, journal, and lease release.
10. `summarize` is passive. It never mutates state or contacts a provider.

## Status evidence

`summarize` reports the launcher, generation number, task, predecessor thread
and receipt, worker, intent and status, invocation count, receipt, successor,
lease holder/expiry/release, completion report, journal count, current website
task/job/handoff resolver state, and next safe action. Fields are identified as
direct canonical evidence; provider or conversational inference cannot replace
them.

## Recovery routes

| State | Safe route |
| --- | --- |
| Create returned but record failed | Retry `record-successor` with the same child/response; never create again. |
| Create ambiguous | `reconcile-dispatch`; one exact child may be adopted, zero/multiple/uncertain is a human gate. |
| Claim committed, consume absent | `abandon-unconsumed` only with direct non-consumption proof. |
| Consume committed, result unknown | `reconcile-consumed` with direct return evidence or permanent `record-unknown`; never rerun. |
| Receipt finalized, decision absent | `verify-and-decide`; do not rerun the task. |
| Validation failure | Protected repair/replan; no child and no completion. |
| No ready task but incomplete plan | Protected `no_ready_blocked`; no child and no completion. |
| Human gate | Name the absent authority/evidence/capability; create no child. |
| Identity/control drift | Stop before the next mutation/effect and inspect current evidence. |
| Cancellation | `cancel` with explicit authority reference; release the lease and create no child. |

Lease expiry is diagnostic and never permits automatic takeover.

## Authority boundary

The relay owns scheduling and evidence only. `implementation_control/` remains
the authority for website task/job paths, validators, checkpoints, and
protected effects. Plan completion does not authorize staging, commit, push,
deployment, publication, or upstream-source writes.

Legacy coordinator schema 3–7 remains available for read-only status/export
during the compatibility window. New recursive commands refuse it; legacy
mutation requires the explicit `coordinator_v2_legacy` selector and is not a
default path. Retirement is evidence-gated and retains historical readers.
