# Recursive Frame Maintenance Rules

- One discussion owns one immutable generation and one task.
- Consume before the executor call; never rerun consumed unknown work.
- Only worker N may reserve N+1 and only after N's receipt.
- Terminal and protected dispositions create zero children.
- Provider ambiguity never authorizes a blind retry.
- Stop immediately after terminalization, protection, cancellation, or one
  successor record. Never wake/resume a coordinator.

