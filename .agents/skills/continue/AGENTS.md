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
- A missing capability stops execution.
- Validation and checkpoint evidence cannot broaden a claim.
- Read-only and no-action results create no fake completion.

## Required validation

Run the manifest validator, focused `continue` tests, the complete
`agentjob-control` suite, and `git diff --check`. Inspect examples and scripts
for hard-coded project assumptions before finalizing a template change.
