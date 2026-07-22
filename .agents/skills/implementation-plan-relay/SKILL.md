---
name: implementation-plan-relay
description: Launch one accepted implementation plan into a plan-native recursive discussion chain without executing a task.
---

# Implementation Plan Relay

## Purpose

Launch generation 1 of an accepted implementation plan under
`recursive_chain_v1`. This discussion is a launcher, not a coordinator. It
creates no native Codex Goal, no generic outer goal, and no AgentJob. It stops
after one generation-1 successor is recorded or after a protected dispatch
state is persisted.

## Required inputs

- exact accepted plan and a `sys4ai.plan-relay-acceptance.v1` object whose
  fields equal the latest read-only acceptance basis;
- repository binding/fingerprint and project-control fingerprint;
- launcher discussion identity;
- `recursive_chain_v1` profile/topology and accepted reasoning effort;
- provider capability report and explicit automatic or degraded-manual mode.

The acceptance object contains the basis fields plus exactly
`accepted=true` and a nonblank `acceptance_evidence_ref`. The basis binds the
plan/objective/revision/task graph, repository binding and fingerprint,
project-control fingerprint, launcher discussion, requested and effective
effort, authority manifest, protected-effect grants, profile, and topology.
Any missing, additional, or changed field is stale acceptance. It must fail
before the relay database is initialized or generation 1 is reserved.

## Protocol

1. Read and validate the complete plan, dependency graph, acceptance,
   repository, control, profile, and provider capability evidence.
2. Refuse legacy/mixed topology, stale acceptance, ambiguous repository
   identity, or a second active relay for the repository.
3. Run `prepare` read-only. Deterministically select only the first dependency-
   ready task; no-ready without positive completion proof is protected.
4. In one local transaction initialize `PlanRelayRun`, generation 1,
   `PlanTaskEnvelope v3`, one repository lease, and one
   `PlanDispatchIntent v3` with create budget one.
5. Call the provider at most once. If the result is concrete, record the exact
   child and response hash. If it is ambiguous, persist ambiguity and use
   `reconcile-dispatch`; never blindly retry.
6. Stop immediately. Do not execute, wait for, resume, or loop over the task.

The launcher cardinality is fixed: zero AgentJobs, zero task calls, one
generation-1 reservation, one provider-create budget, and at most one recorded
successor.

## Degraded manual mode

When automatic create/query capability is absent, emit the minimal redacted
handoff and report `degraded_manual`. Do not claim automatic continuity. Adopt
only one human-supplied child after exact project, checkout, effort,
idempotency, and current-thread evidence passes reconciliation.

## Protected stops

Stop without a child for missing authority/capability, integrity or identity
drift, multiple/uncertain children, explicit cancellation, or any state with no
single deterministic recovery. Provider state and prose cannot select or
complete the plan.

## Installation and provenance

Install through the dependency-resolved canonical bundle with
`agentjob-control` and `continue-implementation-plan-relay`. Mutable state
belongs in `<PROJECT_ROOT>/.local/sys4ai/implementation-plan-relay/`, never in
this package. Adapt target-project control and provider interfaces without
editing generated plugin copies.

## Required role posture

- **System Analyst:** establish the target-system plan, dependencies, evidence, and unresolved conditions.
- **System Engineer:** verify topology, identities, lease, provider capability, and safe dispatch boundary.
- **Software Engineer:** perform the one transactional launch and verify its canonical evidence.

## System-agnostic interpretation

The target system supplies its plan, repository, control, provider, and policy adapters. No project path, task taxonomy, branch, or domain claim is implicit.

## Domain emphasis

This skill validates orchestration and dispatch integrity, not the scientific, mathematical, legal, product, or operational truth of a task result.

## Authority boundaries

The launcher may create one plan-native run and generation-1 child. It cannot execute a task, infer protected authority, create a Goal, retry ambiguity, or authorize release effects.

## Completion receipt

Return run, generation, envelope, intent, provider, lease, revision, and journal evidence plus the next safe action. A launcher receipt never means plan completion.
