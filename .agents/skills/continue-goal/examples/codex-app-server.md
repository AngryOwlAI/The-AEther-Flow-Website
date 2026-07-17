# Codex App Server Example

Use this mode only when an external controller is configured and reports the
documented thread lifecycle operations required by the selected strategy.

Conceptual configuration:

```yaml
goal_relay:
  thread_provider: codex-app-server
  thread_strategy: fresh_summary
```

The integration performs this sequence:

1. Query the external controller's capability report.
2. Initialize the canonical goal and reserve one successor intent.
3. Submit exactly one `fresh_summary` start request containing the validated
   worker prompt and continuation envelope.
4. Record only redacted request hashes, operation, strategy, request ID, and
   minimal response status as provider evidence.
5. Persist the returned successor ID in canonical goal state.
6. Stop the predecessor immediately after persistence.

For `fork_history`, the adapter submits one configured fork request with the
predecessor identity. Forked history remains non-authoritative context; the
worker revalidates the canonical envelope and project state before claiming.

Authority limitation: the external controller may create or inspect threads,
but it does not own generation numbering, handoff tokens, leases, at-most-once
consumption, AgentJob authority, or completion decisions.

Evidence limitation: an external request ID is not a protocol receipt and an
external idempotency feature is not assumed to provide the relay's exactly-one
successor semantics.

Privacy: configure the transport so credentials remain outside prompts and
provider receipts. Do not persist full thread history or raw response payloads
unless a separate approved retention policy requires it.

Timeout or ambiguous response: issue no second create call. Enter recovery,
inspect the controller for a uniquely matching live successor, and then adopt
or cancel through the canonical state machine.
