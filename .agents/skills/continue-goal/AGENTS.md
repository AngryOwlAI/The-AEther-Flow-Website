# Continue Goal Maintenance Rules

- Keep this package launcher-only: zero AgentJobs and no bounded project-work
  invocation.
- Preserve exact goal-text hashing, completion-contract hashing, finite guards,
  and repository binding.
- Dispatch at most one first-generation successor and stop after recording it.
- Treat unknown provider outcomes as recovery state, not permission to retry.
- Keep secrets out of examples, envelopes, logs, and launcher summaries.
- Validate the manifest and focused launcher tests after every change.
