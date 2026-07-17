# Portable launcher example

Input:

```yaml
project_root: <PROJECT_ROOT>
goal_text: Complete the bounded fixture under its declared validation contract.
completion_contract:
  interpretation: The fixture is complete only when its required checks pass.
  required_evidence:
    - The configured required checks pass.
fresh_recursive_threads_explicitly_requested: true
guards:
  max_continue_passes: 6
  deadline_at: <UTC_DEADLINE>
  handoff_ready_timeout_seconds: 120
```

Expected launcher effect: one immutable goal identity, one reserved generation,
and one recorded automatic successor or manual-handoff artifact. It performs no
project transaction.

Authority status: the envelope, generated prompt, and provider receipt are
non-authoritative continuity evidence. They cannot grant project execution
authority or prove that the goal is complete.
