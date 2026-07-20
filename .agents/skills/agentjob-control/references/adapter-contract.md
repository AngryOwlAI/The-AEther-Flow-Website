# Adapter Contract

Portable adapters expose authority and capability facts; they do not execute
project work during discovery.

Every adapter reports:

- an adapter ID and semantic version;
- capability contract version `1.0.0`;
- feature availability, requirement status, implementation mode, and stable
  reason codes;
- canonical source roots;
- unsupported features;
- named conformance hooks.

Required capability mismatches are blocking and machine-readable. Optional
features may be reported as unsupported without weakening core invariants.

Authority-affecting extensions must use a declared namespace and the standard
`version`, `required`, and `data` envelope. An adapter may add evidence or make
policy stricter. It may not weaken one-AgentJob cardinality, record
immutability, supersession, at-most-once consumption, path boundaries, claim
boundaries, or recovery requirements.

Repository, checkpoint, context, thread, and native-goal providers are separate
interfaces. This separation prevents a cache, UI mirror, checkpoint receipt,
or repository observation from silently becoming execution authority.

Conformance is an evidence-backed claim. Adapters should expose native,
emulated, and unsupported status for each mapped authority surface and provide
stable hooks that the conformance suite can inspect without running a task.
