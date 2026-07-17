# Continue Implementing Goal

## Release status

This package is an experimental `0.1.0` internal template with lifecycle status
`draft`. It is not a general autonomous loop and cannot be entered without the
exact token-bound continuation envelope and revision.

`continue-implementing-goal` is the internal generation worker for a durable
goal relay. Each invocation consumes one token-bound generation, calls the
bounded `continue` skill at most once, verifies direct evidence, and then stops
at a terminal state or after recording one fresh successor.

Normal entry without a valid envelope, token, generation, expected revision,
and matching discussion identity is rejected. Recovery is an explicit mode;
it never grants permission to rerun consumed or unknown work.

## Adaptation summary

Bind the target project's state backend, repository adapter, ThreadProvider,
and `continue` installation. Preserve at-most-once consumption, one-successor
creation, immutable goal identity, and fresh-discussion recursion.
