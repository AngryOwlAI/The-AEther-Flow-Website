# Implementation Plan Bindings

Files named `<plan-id>.yaml` in this directory are versioned, non-executable
maps from an accepted canonical `sys4ai.implementation-plan.v2` to exact
website `implementation_control/` packet projections.

The binding is not execution authority. Before combined acceptance, the
adapter verifies the canonical plan hash, every task ID and task hash, every
packet field, each per-task authority hash, the manifest hash, repository
topology, and the current website-control compare-and-swap hash. A selected
task is materialized only from its binding projection; plan prose cannot add
paths, gates, checkpoint rights, topology changes, or external effects.

Bindings conform to
`implementation_control/schemas/plan-binding-v1.schema.json`. Any plan,
binding, goal, reasoning profile, topology, authority hash, or website-control
hash change invalidates the prior combined acceptance.
