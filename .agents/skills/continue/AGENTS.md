# Continue Maintenance Rules

## Scope

Maintain a portable one-AgentJob continuation template. Project-specific
routes, role names, paths, branch policies, and domain truth criteria do not
belong in this package.

## Invariants

- Preflight remains read-only.
- One invocation executes no more than one AgentJob.
- This skill never creates or forks a discussion.
- Runtime controls cannot exceed activated AgentJob authority.
- A missing capability stops the current execution attempt but remains a
  machine-repair route while a declared doctor or fallback is lawful.
- Validation and checkpoint evidence cannot broaden a claim.
- Read-only and no-action results create no fake completion.
- Preserve failed validation/checkpoint evidence and create a separate repair
  route; never edit a failure into a pass.
- Reject branch/worktree creation without exact one-shot protected-action
  authority and before/after topology validation.

## Required validation

Run the manifest validator, governed-continuation protocol-static validator,
relevant CLI checks, generated-artifact drift checks, and `git diff --check`.
Inspect examples and scripts for hard-coded project assumptions before
finalizing a template change. AgentJob control has no canonical runtime
regression suite; report that limitation explicitly.
