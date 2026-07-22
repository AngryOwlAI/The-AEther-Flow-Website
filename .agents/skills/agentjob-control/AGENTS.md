# AgentJob Control Maintenance Rules

- Treat ThreadExecutionProfileProvider evidence as runtime evidence; manifest
  defaults alone never prove current or successor effort.
- Preserve plan envelope/provider/receipt v1 read compatibility while new
  profile-aware plan writers emit v2.
- Keep plan activation history immutable and repository topology default-deny.

## Mission

Maintain a portable, default-deny control protocol for one bounded AgentJob
transaction and durable goal-relay state. Keep runtime mechanics separate from
project adapters and domain policy.

## Rules

- Preserve standard-library-only operation unless a separately approved
  manifest change justifies a dependency.
- Keep implicit invocation disabled.
- Treat activated records, completions, handoffs, receipts, approvals, and
  recovery events as immutable.
- Add fields through versioned schemas; put project/domain data below an owned
  extension namespace.
- Reject unknown required extensions, unsafe paths, duplicate keys, stale
  revisions, unapproved commands, and missing claim boundaries.
- Never let a resolver choose a role or invent authority.
- Never treat a generated index, plugin copy, snapshot, or log as canonical
  record authority.
- Keep mutable state outside the package and generated plugin.
- Validate every protocol or state change through the available static package,
  schema, documentation, example, and CLI checks.
- Preserve compatibility evidence and rollback requirements when changing
  compatibility.
- Preserve the v1 goal schema unchanged and keep v1 reader compatibility
  separate from v2 read/write capability.
- Keep canonical v2 null deadlines distinct from SQLite's reserved legacy
  projection marker.
- Keep v1-v3 goal records readable and unchanged. Advanced compatibility
  initialization may still emit v3; new uninterrupted launches use v4 only
  after complete question, response, authority, and activation bindings.
- No v3 non-success terminal is valid without a human-necessity report proving
  no lawful machine route remains.
- Require exact one-shot authority and before/after identity checks for
  branch/worktree/binding changes.
- Keep the v4 coordinator at zero AgentJobs, reject manual ThreadProviders,
  and require automatic create/profile/query/wait/resume capabilities at
  verified `max` before activation.
- Preserve SQLite migrations append-only through schema version 7.

## Validation

Run manifest and protocol-static validation, schema checks, CLI help or
read-only CLI validation as applicable, dependency and generated-artifact drift
checks, and diff hygiene. This package has no canonical runtime regression
suite; do not represent static validation as exercised runtime behavior.

## Target-Project Adaptation

Replace placeholders only in the adapted target copy. Declare project paths,
adapters, policy packs, validators, checkpoint behavior, human gates, and
protocol ranges explicitly. Record every local assumption and keep protected
actions human-gated.
