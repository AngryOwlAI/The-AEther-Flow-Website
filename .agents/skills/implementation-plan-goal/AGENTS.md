# Implementation Plan Goal Maintenance Rules

- Keep the canonical package project-agnostic and standard-library-only.
- Keep the launcher boundary at zero AgentJobs and at most one provider create.
- Preserve one immutable task ID and task hash per fresh worker discussion.
- Never extend the generic continuation envelope with plan-specific fields.
- Keep `planctl.py` offline and read-only. Durable mutation belongs only to the
  shared `agentjob_runtime.plan` SQLite runtime; offline validation or
  selection must not repair, reserve, activate, dispatch, or call a provider.
- Require combined acceptance of the exact goal and selected effort before
  initialization. Metadata defaults are not runtime verification.
- Require envelope, canonical, provider, current-thread, binding, and topology
  parity before a profile-aware worker claim.
- Preserve bound-checkout reuse and exact one-shot user authority for branch,
  worktree, or binding changes.
- Reject duplicate task IDs, unknown dependencies, self-dependencies, cycles,
  and inconsistent terminal state.
- Require append-only replacement task IDs for work that exceeds one worker
  discussion.
- Keep mutable plan state outside canonical, adapted, and plugin skill trees.
- Keep the PHASE-02 corpus deterministic, project-neutral, hash-indexed, and
  one-fault-per-negative-file. Regenerate it only through the declared builder.
- Validate the manifest, corpus drift, focused tests, fixtures, registry, and
  bundle after every change.
