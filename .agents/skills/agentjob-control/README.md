# AgentJob Control

## Release status

This package is an experimental `0.1.0` template with lifecycle status
`draft`. It is available for validation and neutral-project pilots, not as a
claim of production readiness. Installation does not activate project adapters,
legacy shims, external effects, or a target project's control authority.

`agentjob-control` is the shared, project-agnostic control capability for the
Governed Continuation family. It provides schemas, deterministic hashing,
record validation, activation, supersession, completion and handoff writers,
goal-relay state, recovery, adapters, policy-pack loading, and diagnostics.

It is an internal dependency. It does not execute work merely because it is
installed or invoked, and it grants no domain authority. A target project must
declare a compatible configuration and either adapt an existing control system
or bootstrap the portable registered profile.

## Package Contents

- `SKILL.md`: executable agent instructions and authority limits.
- `AGENTS.md`: maintenance and adaptation rules.
- `skill.yaml`: operating-layer manifest.
- `agents/openai.yaml`: invocation metadata with implicit invocation disabled.
- `schemas/`: portable JSON Schema protocol.
- `adapters/`: declarative existing-control adapter templates.
- `policy-packs/`: generic and target-domain policy packs kept outside core schemas.
- `compat/`: reader-only legacy support and inactive shim templates.
- `templates/`: human-maintained record templates.
- `scripts/agentjobctl.py`: stable CLI.
- `scripts/agentjob_runtime/`: standard-library Python implementation.
- `tests/`: neutral fixtures and protocol/runtime tests.

## What It Produces

The package may produce validated tracked control records under a target
project's configured control root and ignored mutable state under its local
state root. It also produces deterministic derived indexes and machine-readable
receipts. Generated indexes, plugins, and snapshots remain derivatives.

## Adaptation Summary

Adapt the template by selecting a control profile, project and repository
adapters, checkpoint provider, policy packs, role catalog, validators, human
gates, and local state root. Keep project- or domain-specific fields in owned
extension namespaces. Do not copy AEther paths, scientific roles, memory
commands, branch rules, or claim gates into the generic core.

## Validation Summary

The runtime uses the Python standard library. Run package tests, CLI help,
manifest validation, and target-project `doctor` before use. A project without
the mandatory capability receives `bootstrap_required`; no ungoverned fallback
exists.

## Provenance

Derived from a project-specific skill and generalized as a reusable template.
Original project-specific names, paths, assumptions, and private operational
details were removed or replaced with parameters.
