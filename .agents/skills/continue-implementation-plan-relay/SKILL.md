---
name: continue-implementation-plan-relay
description: Claim, consume, execute, evidence, and relay exactly one plan generation in one discussion.
---

# Continue Implementation Plan Relay

## Purpose

Own one generation of `recursive_chain_v1`. This frame validates its immutable
envelope and predecessor handoff, consumes before the task call, invokes
`continue` at most once, records direct evidence, then terminalizes, protects,
or reserves and records at most one distinct next-task successor. It stops
after that decision; it never wakes or resumes a coordinator.

## Required sequence

1. Wait read-only until `successor_created` names this current discussion.
2. Re-read the live plan, repository, control fingerprint, profile, topology,
   requested/effective effort, generation, predecessor, envelope, intent, and
   lease evidence.
3. Atomically `claim-generation`; only the recorded current thread can win.
4. Atomically `consume-generation` immediately before the task boundary.
5. Invoke `continue` exactly once for the immutable task. Do not compile or
   execute another task.
6. Record direct return evidence with `record-returned`, or permanently
   quarantine uncertainty with `record-unknown`. Consumed work is never
   automatically rerun.
7. Reinspect repository and project control. Finalize one immutable receipt.
8. Choose exactly one disposition: `plan_complete`, `safe_next_task`, bounded
   `repair_or_replan`, `human_gate`, `integrity_or_capability_stop`, or
   `cancelled`.
9. For completion, validate the positive report and atomically terminalize,
   journal, and release the lease. For a safe next task, reserve N+1 with this
   worker and receipt as predecessor, perform the one intent/create/record
   protocol, and stop. Every protected branch creates no child.

Worker prose is telemetry. The receipt and canonical evidence establish
completion. Scheduling N+1 does not authorize this discussion to execute N+1.

## Cardinality

Exactly one task ID, at most one `continue` invocation, at most one AgentJob,
at most one distinct next-task successor, and zero same-task successors.

## Secret and recovery rules

Raw tokens are input-only and never enter durable records, exports, logs, or
mirrors. A create-return/record failure retries only `record-successor`.
Ambiguous create uses `reconcile-dispatch`. Claim-before-consume may be released
only with direct non-consumption proof. Consume uncertainty never reruns.

## Required role posture

- **System Analyst:** verify the target-system generation, predecessor, task, and direct evidence.
- **System Engineer:** enforce claim, consume, lease, recovery, and one-successor invariants.
- **Software Engineer:** execute the one bounded task call and persist its receipt and decision.

## System-agnostic interpretation

The target system supplies its task executor, repository, control, validators, and provider adapters. No project-specific path, policy, or domain authority is embedded.

## Domain emphasis

The frame establishes process integrity and evidence continuity. Its receipt does not promote a domain claim or replace target-system validation.

## Authority boundaries

The frame may mutate only its generation and one N+1 handoff. It cannot run a second task, steal a lease, retry consumed work, bypass a human gate, or grant release effects.

## Completion receipt

Return exactly one task receipt plus terminal/protected evidence or one successor record. Prose without canonical/direct evidence is not completion.
