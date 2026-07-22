# Implementation Plan Relay Maintenance Rules

- Keep the launcher at zero AgentJobs and generation 1 only.
- New runs use `recursive_chain_v1` and the independent relay database.
- Never import generic-goal activation, initialization, mutation, or completion.
- Commit one provider intent before the sole create attempt; ambiguity never
  authorizes a second create.
- Store token hashes only and keep status/export passive.
- Stop after one successor record or protected disposition.
- Generated plugin and installed copies are derivatives, not editing surfaces.

