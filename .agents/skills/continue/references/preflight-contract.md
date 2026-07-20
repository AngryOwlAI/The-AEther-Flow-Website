# Continue Preflight Contract

Preflight is a read-only classification step. It must not create directories,
regenerate indexes, initialize a database, stage records, acquire execution
authority, run a project command, or execute an AgentJob.

## Required observations

- Explicit project and configuration identity.
- Required and optional capability status.
- Canonical control records, activation, supersession, task pointers, and
  derived-index parity.
- Repository provider, root, worktree, revision, branch, and normalized status.
- Active task, decision, job, role, and pending human gates.
- Direct source paths and hashes used to classify the continuation boundary.
- One timestamp-free canonical before fingerprint.

## Required outcomes

Return one of `bootstrap_required`, `existing_agent_job_ready`,
`director_decision_required`, `human_gate_required`, `no_action`, `blocked`, or
`control_repair_required` with a stable reason code and `execution_performed`
set to false.

Missing configuration or a required provider maps to `bootstrap_required`.
Invalid authority or conflicting canonical state maps to a protected stop; it
must not be repaired implicitly during preflight.
