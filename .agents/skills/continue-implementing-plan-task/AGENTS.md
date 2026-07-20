# Plan Task Worker Maintenance Rules

- Require exact plan, task, token, generation, thread, envelope, repository,
  and revision identity before consumption.
- Execute exactly one task ID per fresh discussion.
- Invoke `continue` at most once and execute at most one AgentJob.
- Never create a same-task successor or start the next plan task.
- Never automatically rerun consumed or unknown work.
- Use `task_requires_replan` and append-only replacement IDs for oversized
  tasks.
- Keep plan-task records distinct from generic goal records.
- Keep mutable state outside canonical, adapted, and plugin skill trees.
- Validate the manifest and focused plan-contract tests after every change.
