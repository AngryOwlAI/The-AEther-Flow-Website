# AgentJob Control

<!-- BEGIN GENERATED INSTALLATION BANNER -->
> **Support provider:** This package supplies shared capability. Prefer dependency resolution or the recommended bundle/plugin.
>
> **Installation class:** `support_provider` / `advanced_or_dependency`<br>
> **User-selectable:** advanced use only — normally dependency-resolved<br>
> **Direct copy allowed:** no<br>
> **Required dependencies:** none<br>
> **Recommended bundle:** `governed-continuation`, `research-control`<br>
> **Recommended plugin:** `sys4ai-governed-continuation`<br>
> **Mutable state required:** yes — `{project_root}/.local/sys4ai/continuation`; keep it outside installed skill/plugin trees and preserve it on uninstall<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill agentjob-control --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

## Plan execution-profile support

The shared runtime provides additive SQLite schema 6 plus plan activation v2,
question/authority records, continuous state v2, task-envelope v2,
provider-intent v2, task-receipt v2, coordinator wakeups, canonical completion
reports, recovery adoption, and repository-topology enforcement used by the
non-plugin `implementation-plan-goal` bundle. Continuous ThreadProviders must
expose creation with exact effort, effective-effort verification,
bound-checkout reuse, terminal waiting, and same-coordinator resumption.

## Release status

This package is an experimental `0.4.0` template with lifecycle status
`draft`. It is available for validation and neutral-project pilots, not as a
claim of production readiness. Installation does not activate project adapters,
legacy shims, external effects, or a target project's control authority.

`agentjob-control` is the shared, project-agnostic control capability for the
Governed Continuation family. It provides schemas, deterministic hashing,
record validation, activation, supersession, completion and handoff writers,
goal-relay state, recovery, adapters, policy-pack loading, and diagnostics.

The goal-state runtime reads unchanged finite
`sys4ai.continue-goal.v1` records and reads/writes
`sys4ai.continue-goal.v4` records through the continuous entry while retaining
byte-preserving readers for v1-v3 and the advanced v3 compatibility writer. In
v2, canonical null pass/deadline fields
mean unlimited passes and no wall-clock deadline.

It is an internal dependency. It does not execute work merely because it is
installed or invoked, and it grants no domain authority. A target project must
declare a compatible configuration and either adapt an existing control system
or bootstrap the portable registered profile.

## Package Contents

Version `0.4.0` supplies both the continuous implementation-plan substrate and
generic one-confirmation goals: question batches, complete responses, exact
execution authority, activation receipt v2, authority-bound envelope/result/
receipt v3, durable coordinator wakeups, provider waiting/resumption, one-shot
grant consumption, and SQLite schema version 7. It retains the continuous
implementation-plan 0.2.0
substrate: combined activation receipts v2, consolidated question and exact
authority records, ThreadProvider terminal waiting and parent resumption,
idempotent `advance_once`, nonterminal input/safeguard states, authoritative
plan completion reports, and transactional SQLite schema version 6.

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

The runtime uses the Python standard library. The shared regression suite
exercises migrations, activation, provider identity, topology, task workers,
continuous multi-task advancement, late input, bounded repair, ambiguity, and
completion. Run those checks and target-project `doctor` before use. A project
without the mandatory capability receives `bootstrap_required`; no ungoverned
continuous fallback exists.

## Provenance

Derived from a project-specific skill and generalized as a reusable template.
Original project-specific names, paths, assumptions, and private operational
details were removed or replaced with parameters.
