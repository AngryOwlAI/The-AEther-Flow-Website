# Generation Worker Maintenance Rules

- Require exact token, generation, thread, envelope, and revision identity in
  normal mode.
- Invoke the bounded continuation at most once per consumed generation.
- Never automatically rerun a consumed or unknown generation.
- Reserve and create at most one successor, then stop immediately.
- Keep recovery explicit, append-only, and evidence based.
- Do not treat worker prose, elapsed leases, or process success as global goal
  completion.
- Validate the manifest and focused worker tests after every change.
