---
name: continue
description: Resolve authoritative project state and execute or close at most one activated AgentJob transaction.
---

# Continue

## Purpose

Use this skill to advance one configured project by at most one bounded,
activated AgentJob. It validates current authority, captures direct before and
after evidence, and returns one structured result. It does not recurse, spawn a
thread, infer missing permission, or treat process completion as domain truth.

## When to Use

Use `continue` when a user or a declared relay worker asks for the next lawful
bounded project transaction and the target project has a compatible
`agentjob-control` configuration.

Do not use it to bootstrap silently, perform multiple jobs, create successor
discussions, bypass human gates, or perform an external side effect absent
explicit authority.

## Inputs

Required:

- `<PROJECT_ROOT>`;
- a validated project control configuration;
- an optional explicit task ID when several tasks could be in scope.

Optional inputs include `normal`, `inspect`, or `recover-control` mode and a
bounded user objective. Goal metadata is context only; it never expands the
AgentJob.

## Outputs

Return one `sys4ai.continue-result.v3` object when invoked by a v4 goal worker.
It contains the boundary entered, zero or one executed AgentJob, canonical
record IDs, before and after fingerprints, validator counts, execution status,
a stable reason code, the accepted execution-authority hash, any exact
protected-action request, and the next recommended action. Standalone and
historical callers retain compatible v1/v2 results.

## Procedure

1. Resolve `<PROJECT_ROOT>` explicitly and load project configuration.
2. Run read-only preflight over capabilities, control records, activation,
   repository identity, gates, conflicts, and the canonical before snapshot.
3. Classify every non-executable boundary. Stop only for a genuine human gate,
   accepted finite policy limit, integrity incident, or cancellation. Route
   bootstrap, no-action, blocked machine state, validation/checkpoint failure,
   evidence gaps, and control repair through a declared bounded strategy.
4. Reuse one valid activated packet, or enter the System Director phase to
   create and activate exactly one decision/job/role packet.
5. Compile the AgentJob into path, command, environment, network, tool, and
   external-effect and repository-topology controls. A branch/worktree command
   requires the exact protected action and an unconsumed one-shot receipt.
6. Bind the activated execution role and execute exactly one AgentJob through
   approved interfaces.
7. Validate changed paths, outputs, command evidence, project rules,
   checkpoint evidence, and the inherited claim boundary.
8. Finalize one immutable completion when direct evidence permits it. Write a
   non-authoritative handoff only when a next route is known.
9. Regenerate indexes, capture the final fingerprint, return the structured
   result, and perform no second job.
10. In v4 goal context, bind the result to the envelope's exact execution
    authority. Report a protected action as a structured exact request; do not
    ask the user directly or infer broader permission.

## Invariants

- Maximum AgentJobs per invocation: one.
- Thread spawning: forbidden.
- Activated authority cannot expand during execution.
- Missing configuration returns `bootstrap_required` and executes nothing.
- Read-only and no-action paths create no completion, checkpoint commit, or
  synthetic work record.
- Process validation and checkpoint evidence cannot promote a domain claim.
- A v4 result cannot omit or change its accepted execution-authority hash.

## Validation

```text
python3 scripts/skills/validate_skill_manifest.py --manifest skills/continue/skill.yaml
python3 scripts/skills/validate_control_protocol.py --json
```

Report the highest verification level reached, the absence of canonical
AgentJob runtime regression coverage, and every unresolved gate.

## Failure Modes

- Missing configuration or capability: return `bootstrap_required`.
- Invalid, stale, or conflicting machine state: preserve evidence and route a
  bounded control repair or deterministic reconciliation.
- Human gate: record the protected boundary and execute zero jobs.
- Unsupported runtime constraint: run a declared doctor/fallback; require a
  human only if no lawful machine route remains.
- New authority requirement during execution: fail closed and preserve direct
  working evidence.
- Validation or checkpoint failure: do not record successful completion.

## Required role posture

- **System Analyst:** establish the target-system state, evidence, active task,
  assumptions, and unresolved conditions.
- **System Engineer:** select the earliest lawful boundary, required role,
  validators, and handoff.
- **Software Engineer:** execute at most one bounded AgentJob through the
  adapted control runtime and verify the resulting state.

## System-agnostic interpretation

Continue the target agentic system through project-supplied control and
repository adapters. No project path, provider, branch, task taxonomy, or
domain claim is implicit.

## Domain emphasis

The skill validates continuation process and bounded progress. Apply a selected
domain pack for the work product; a continuation receipt does not establish
scientific, mathematical, financial, biological, or product truth.

## Authority boundaries

Read project-authorized state and evidence. Write only records and outputs
within the active job authority. Do not execute more than one AgentJob, bypass
human gates, publish, create repository topology without exact authority, or
infer global goal completion from bounded progress.

## Completion receipt

Report the boundary entered, job and decision identifiers, fingerprints,
validators, changed paths, progress effect, remaining work, and next lawful
action.

## Provenance

Derived from a project-specific skill and generalized as a reusable template. Original project-specific names, paths, assumptions, and private operational details were removed or replaced with parameters.

## Adaptation Guide

When adapting this skill to a specific project:

- Replace placeholders with project-specific paths, commands, and authorities.
- Declare the project adapter, policy pack, checkpoint provider, and role catalog.
- Add domain validators without weakening the portable one-job or claim-boundary invariants.
- Preserve read-only preflight and structured direct evidence.
- Document every project-specific assumption introduced during adaptation.
