---
name: agentjob-control
description: Provide portable schemas, activation, supersession, state, validation, recovery, adapters, and diagnostics for bounded AgentJob execution.
---

# AgentJob Control

## Purpose

Use this internal dependency to validate and operate a portable AgentJob
control system. It supplies protocol machinery; it does not select domain
truth, grant execution authority by itself, or replace a target project's
policy and human gates.

Implicit invocation is disabled. User-facing continuation skills may call this
capability only after a project configuration declares a compatible control
profile and required adapters.

## When to Use

Use this skill when a declared parent skill or operator needs to:

- validate task, decision, AgentJob, execution-role, completion, handoff,
  activation, supersession, goal, receipt, adapter, policy, or configuration
  records;
- resolve whether a project must bootstrap, reuse a job, create a Director
  decision, stop for a gate, repair control state, or report no action;
- stage and atomically activate one bounded decision/job/role packet;
- close one AgentJob and optionally create one non-authoritative handoff;
- inspect or recover governed continuation state;
- generate deterministic indexes and fingerprints.

Do not use it as a general-purpose task runner, background controller, domain
decision-maker, deployment tool, or permission bypass.

## Inputs

Required for project operations:

- `<PROJECT_ROOT>` resolved explicitly or supplied by the parent skill;
- a validated `.agents/control/config.yaml` or compatible adapter declaration;
- the exact expected control revision for every write;
- canonical records and any policy-pack or human-gate evidence required by the
  requested operation.

Optional inputs include a task ID, packet directory, output mode, adapter
configuration, or recovery evidence. Secrets must be referenced indirectly and
must not be copied into control or goal records.

## Outputs

Depending on the operation, produce:

- structured validation findings with stable reason codes;
- a capability or `bootstrap_required` report;
- an activation, supersession, completion, handoff, index, status, doctor, or
  fingerprint receipt;
- project-local tracked control records below the configured control root;
- project-local ignored state below the configured local state root.

Every output states its evidence class and must remain within the upstream
AgentJob and claim boundary.

## Procedure

1. Resolve `<PROJECT_ROOT>` without relying on an implicit current directory.
2. Load and schema-validate configuration in strict mode.
3. Discover control, repository, state, checkpoint, policy, and optional thread
   capabilities. Stop with `bootstrap_required` when mandatory capabilities are
   absent.
4. Validate canonical record schemas, hashes, activation manifests,
   supersession chains, task pointers, extensions, and repository binding.
5. For a write, require the exact expected revision and an operation-specific
   AgentJob authority boundary.
6. Stage records outside the authoritative tree and validate cross-record
   semantics.
7. Activate immutable records by writing the activation manifest last, then
   update the task pointer through compare-and-swap.
8. Execute no domain work. Parent skills compile and execute the separately
   activated AgentJob.
9. Validate completion evidence against the exact job, write one immutable
   completion, update the task, and create a handoff only when work remains.
10. Regenerate derived indexes from canonical records and report hashes,
    validators, warnings, failures, and unresolved gates.

## Invariants

- A draft packet has no execution authority.
- One `continue` invocation may execute zero or one AgentJob.
- Activated records and finalized receipts are immutable.
- Corrections use supersession or append-only recovery evidence.
- Missing permissions, paths, commands, network access, or external effects
  mean denied.
- A handoff recommends a next route but never activates it.
- Process validation does not prove domain truth.
- Mutable state never lives inside a skill or plugin installation directory.

## Validation

Use the narrowest relevant checks first:

```text
python3 scripts/skills/validate_skill_manifest.py --manifest skills/agentjob-control/skill.yaml
python3 scripts/skills/validate_control_protocol.py --json
python3 <AGENTJOB_CONTROL_PATH>/scripts/agentjobctl.py --help
python3 <AGENTJOB_CONTROL_PATH>/scripts/agentjobctl.py validate --project-root <PROJECT_ROOT> --json
```

The canonical package has static, schema, documentation, example, and CLI
verification only. It does not include a runtime regression suite. Validation
proves only the class it reports: a static or schema PASS does not establish
runtime correctness, and process or control PASS does not establish domain
truth.

## Failure Modes

- Missing or invalid configuration: return `bootstrap_required` or a stable
  configuration error; execute nothing.
- Revision conflict: preserve existing bytes and return a compare-and-swap
  conflict.
- Partial staging: retain or quarantine non-authoritative staged evidence;
  write no activation manifest.
- Hash, path, symlink, hard-link, or extension mismatch: block the operation.
- Ambiguous external call boundary: mark the result `unknown`; never retry the
  consumed authorization automatically.
- Missing human authority: stop before the protected action.

## Required role posture

- **System Analyst:** establish the target-system boundary, controlled state,
  stakeholders, assumptions, risks, and open issues.
- **System Engineer:** define control contracts, role and job boundaries,
  interfaces, verification evidence, lifecycle transitions, and handoff.
- **Software Engineer:** inspect or change runtime code, schemas, stores,
  adapters, static validators, and commands while preserving compatibility.

## System-agnostic interpretation

Apply the control protocol to the target agentic system through project-supplied
adapters. Do not assume a repository layout, provider, domain, or mutable state
location beyond the declared interfaces and placeholders.

## Domain emphasis

The base skill governs execution rather than domain truth. Apply a selected
domain pack for software, AI/ML, physics, mathematics, finance, biology, or
another field, and keep its claim validators independent from control checks.

## Authority boundaries

Read only project-authorized control, repository, adapter, and policy evidence.
Write only the declared control records and local state through approved
interfaces. Do not expand job authority, bypass a gate, publish, or infer
domain truth from schema or process conformance.

## Completion receipt

Report records read or changed, state revisions, adapter and dependency use,
commands and validators, skipped checks, unresolved risks, and the next lawful
control transition.

## Provenance

Derived from a project-specific skill and generalized as a reusable template. Original project-specific names, paths, assumptions, and private operational details were removed or replaced with parameters.

## Adaptation Guide

When adapting this skill to a specific project:

- Replace placeholders with project-specific paths, commands, and authorities.
- Add project-specific validation commands.
- Add domain-specific constraints only when they are required.
- Preserve the reusable procedure unless local evidence shows a better structure.
- Document any project-specific assumptions introduced during adaptation.
