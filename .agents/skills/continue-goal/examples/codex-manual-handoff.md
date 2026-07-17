# Codex Manual Handoff Example

Use this mode on CLI, desktop, or IDE when no configured automatic thread
capability is available.

1. Configure `thread_provider: manual-handoff` and
   `thread_strategy: fresh_summary`.
2. Invoke `continue-goal` with exact goal text, a completion contract, finite
   guards, and an explicit project binding.
3. The launcher reserves generation 1 and writes:
   - `continuation-envelope.json`;
   - `new-thread-prompt.txt`;
   - `provider-receipt.json`.
4. The launcher stops with `manual_handoff_pending`. It executes zero
   AgentJobs and does not call `continue`.
5. Open a genuinely fresh Codex discussion and paste the exact generated
   prompt. Do not reuse the launcher discussion.
6. Adopt the fresh discussion using the reserved goal ID, generation,
   handoff-token value, envelope hash, and new thread identity.
7. The adopted worker validates its identity, consumes one invocation, calls
   `continue` at most once, and either terminalizes or reserves one successor.

Authority limitation: the generated prompt and envelope do not grant project
execution authority. The worker must still resolve and execute an activated
AgentJob through `continue`.

Evidence limitation: `manual_handoff_pending` proves only that durable
artifacts were written. It does not prove a new discussion exists until
explicit adoption records a distinct successor identity.

Privacy: never add credentials to the goal, contract, generated prompt, or
manual adoption evidence. Treat the handoff token as local protocol state and
retain manual artifacts according to project policy.

If adoption identity is ambiguous, enter recovery or cancel. Never create or
adopt a second successor blindly for the same generation.
