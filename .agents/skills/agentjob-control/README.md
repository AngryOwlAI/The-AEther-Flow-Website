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
> **Mutable state required:** no<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill agentjob-control --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

## Plan execution-profile support

The shared runtime provides additive SQLite schema 5 plus plan activation,
execution-profile, task-envelope v2, provider-intent v2, task-receipt v2,
manual/recovery adoption, and repository-topology enforcement used by the
non-plugin `implementation-plan-goal` bundle. Thread providers must expose
creation with exact effort, effective-effort verification, and bound-checkout
reuse for profile-aware plan dispatch.

## Release status

This package is an experimental `0.3.0` template with lifecycle status
`draft`. It is available for validation and neutral-project pilots, not as a
claim of production readiness. Installation does not activate project adapters,
legacy shims, external effects, or a target project's control authority.

`agentjob-control` is the shared, project-agnostic control capability for the
Governed Continuation family. It provides schemas, deterministic hashing,
record validation, activation, supersession, completion and handoff writers,
goal-relay state, recovery, adapters, policy-pack loading, and diagnostics.

The goal-state runtime reads unchanged finite
`sys4ai.continue-goal.v1` records and reads/writes
`sys4ai.continue-goal.v3` records while retaining byte-preserving readers for
v1/v2. In v2, canonical null pass/deadline fields
mean unlimited passes and no wall-clock deadline.

It is an internal dependency. It does not execute work merely because it is
installed or invoked, and it grants no domain authority. A target project must
declare a compatible configuration and either adapt an existing control system
or bootstrap the portable registered profile.

## Package Contents

Version `0.3.0` adds combined activation receipts, ThreadProvider v2 execution
profiles, resolution and human-necessity records, one-shot repository topology
authority, goal-step receipt v2, authoritative completion reports, and
transactional SQLite schema version 4.

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

The runtime uses the Python standard library. Current assurance is limited to
static package, manifest, schema, documentation, example, and CLI verification;
the canonical package does not include a runtime regression suite. Run those
checks and target-project `doctor` before use. A project without the mandatory
capability receives `bootstrap_required`; no ungoverned fallback exists.

## Provenance

Derived from a project-specific skill and generalized as a reusable template.
Original project-specific names, paths, assumptions, and private operational
details were removed or replaced with parameters.
