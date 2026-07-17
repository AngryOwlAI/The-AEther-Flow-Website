# Codex Governed Continuation Integration

## Authority Model

Codex surfaces host the portable protocol; they do not replace it. Canonical
authority remains in project-local Task, Director Decision, AgentJob,
ExecutionRole, Completion, Handoff, and durable goal records. A thread ID,
native Goal mirror, generated prompt, provider response, or UI status is
supporting evidence only.

Runtime permissions are defense in depth. The AgentJob compiler, one-job
budget, at-most-once goal state, post-execution changed-path validation, and
claim-boundary validation remain mandatory even when a surface offers a
sandbox or approval controls.

## Capability Detection

Provider selection uses an explicit configured provider or the ordered set of
capabilities supplied by the host integration. The portable core does not
guess private tool names.

| Surface | Safe default | Authority limitation | Evidence limitation |
| --- | --- | --- | --- |
| CLI | Manual new-thread handoff | The CLI cannot treat the current discussion as a successor generation. | A written prompt and envelope prove an intent, not a created thread. |
| Desktop | Configured automated provider, otherwise manual | UI task creation does not grant AgentJob authority. | Returned thread identity is useful only after durable successor persistence. |
| IDE | Configured provider when its capability is explicit, otherwise manual | Editor state and open files do not widen read or write paths. | IDE notifications are not completion receipts. |
| App Server | External-controller adapter | The server does not own generation, token, lease, or receipt semantics. | Server idempotency is not assumed to be protocol idempotency. |
| Native Goal | Optional mirror | The mirror cannot initialize, amend, complete, cancel, or recover a canonical goal. | A stale or missing mirror never overrides SQLite or file-journal state. |

If a required automatic capability is absent, stop with a capability blocker.
If automatic recursion is optional, select the manual provider and retain the
same one-successor reservation.

## Thread Strategies

`fresh_summary` starts a new discussion from the validated continuation
envelope and a compact prompt. It is the portable default because it makes
context transfer deliberate and auditable.

`fork_history` asks a configured external controller to fork the predecessor
history. The envelope still supplies the canonical generation and authority
identity. Forked history is context, not authority, and may contain stale
assumptions that must be rechecked.

`manual_new_thread` writes the envelope, prompt, and provider receipt under the
project-local relay state root. A user opens a genuinely fresh discussion and
performs explicit adoption using the reserved goal, generation, token, and
envelope hash.

No strategy permits same-thread recursion.

## App Server Mode

The App Server adapter uses only operations declared by a configured external
transport. It can start, read, resume, or fork a thread when those documented
capabilities are reported. The adapter sends one request for one reserved
intent, records a redacted request hash and minimal response evidence, and
returns one of:

- `returned` with a thread ID;
- `definitive_failure`;
- `timeout`;
- `ambiguous`;
- `duplicate`.

Timeout and ambiguous outcomes are not automatically retried. Recovery must
determine whether a matching successor exists before adoption, cancellation,
or another legal transition.

## Native Goal Mirror

An enabled mirror contains only a concise summary, goal ID and hash, current
generation, current canonical phase, canonical revision, and pointer to local
state. It contains no handoff token or credential and declares
`authority_effect: mirror_only` and `may_mark_complete: false`.

Mirror update failure is non-corrupting. A read is stale when its goal identity,
revision, generation, or phase differs from canonical state. Disable the mirror
without changing the relay whenever the UI capability is unavailable.

## Runtime Permission Mapping

Compile the activated AgentJob into the narrowest supported Codex controls:

- exact project working directory;
- exact writable source and generated roots;
- network enabled or disabled exactly as authorized;
- deny-unlisted approval posture;
- generic read, write, and local-command tool categories;
- required skill mentions;
- one-AgentJob and bounded command budgets.

When a surface cannot enforce a fine-grained exclusion, retain the local
executor and post-execution validator. If project policy marks that runtime
restriction mandatory, stop rather than broadening the sandbox.

## Privacy and Retention

Goal text and completion contracts are plaintext project-local state. Reject
credentials before initialization. Do not copy access tokens, private keys,
authorization headers, full private thread history, or provider payloads into
prompts, mirror records, or receipts.

Provider evidence should retain hashes, operation names, strategy, request ID,
minimal status, and stable diagnostics. Apply the target project's retention
policy to manual envelopes, prompts, rendered snapshots, and external thread
history. Deleting a derivative does not delete canonical protocol evidence.

## Recovery Rule

After any uncertain create boundary, do not issue another create request for
the same successor intent. Inspect provider state, prove zero or one matching
successor, and use the authorized recovery operations. The durable goal state
machine—not the Codex surface—decides whether adoption, cancellation, or a
terminal result is legal.
