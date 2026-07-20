---
name: continue-implementing-plan-task
description: Internal-only worker lifecycle for one adopted implementation-plan task mapped to one website packet.
---

# Continue Implementing Plan Task

Internal component. Do not select this skill directly.

The adopted worker must verify its task identity, execution profile, envelope,
task hash, binding manifest, checkout topology, and website control hash before
claim. It claims once, consumes once immediately before invoking website
`continue`, and finalizes from direct website control and validation evidence.

It never selects or creates a successor. Unknown consumed execution is
quarantined and is not automatically retried.
