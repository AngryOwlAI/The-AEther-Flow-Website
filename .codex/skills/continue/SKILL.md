---
name: continue
description: Resolve and execute at most one active website implementation-control packet, including a packet selected by implementation-plan-goal.
---

# Website Continue

Resolve the live packet with `npm run continue:implementation`. Treat
`implementation_control/` as sole authority. Execute at most one active or
pending website job, within its exact paths, gates, stop conditions, and
checkpoint rights.

When called by the plan relay, require the token-bound compiled invocation and
the active website packet to name the same plan task mapping. Do not use the
imported `.agents/control` executor. Return direct control and validator
evidence to `worker-finalize`, or use `worker-unknown` when the consumed result
cannot be established.
