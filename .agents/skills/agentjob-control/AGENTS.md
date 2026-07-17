# AgentJob Control Maintenance Rules

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
- Add focused positive and negative tests for every protocol or state change.
- Preserve old-reader and rollback fixtures when changing compatibility.

## Validation

Run focused tests for the changed module, then the full package suite, manifest
validation, CLI help, and diff hygiene. Security- or state-machine changes also
require the fault, concurrency, path, command, and recovery suites.

## Target-Project Adaptation

Replace placeholders only in the adapted target copy. Declare project paths,
adapters, policy packs, validators, checkpoint behavior, human gates, and
protocol ranges explicitly. Record every local assumption and keep protected
actions human-gated.
