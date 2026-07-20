# Implementation Plan Goal

<!-- BEGIN GENERATED INSTALLATION BANNER -->
> **Dependency-resolved workflow:** Select this skill with the installer; do not copy the folder without its required closure.
>
> **Installation class:** `user_workflow` / `dependency_resolved`<br>
> **User-selectable:** yes<br>
> **Direct copy allowed:** no<br>
> **Required dependencies:** `agentjob-control`, `continue-implementing-plan-task`<br>
> **Recommended bundle:** `implementation-plan-goal`<br>
> **Recommended plugin:** none<br>
> **Mutable state required:** no<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill implementation-plan-goal --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

## Release status

This package remains an experimental `0.1.0` template. It supplies a strict
immutable v2 plan-definition contract, read compatibility for the initial v1
shape, a separate v1 plan-state and task-lifecycle contract, a separate
plan-task envelope contract, an immutable v1 PlanTaskReceipt and direct-evidence
contract with outcome fixtures, five append-only normalization/amendment/
supersession/provider-intent/selection-proof contracts, pure semantic
cross-record checks, deterministic read-only source classification and
least-transformative normalization, an exact normalization golden output,
offline profile/content-hash validation, state/receipt/amendment/supersession
validation, revision-bound advisory selection proofs, plan diff and task-hash
drift reporting, deterministic redaction, stable JSON reason codes, and
adaptation guidance. It also supplies combined goal/effort activation,
verified current-thread and successor profiles, additive SQLite schema 5,
automatic and manual provider dispatch, a profile-aware bounded worker,
protected recovery, topology enforcement, and per-generation completion
evidence. A deterministic PHASE-02 corpus supplies standalone
positive records for every declared state and outcome plus hash-indexed,
one-fault-per-file structural and semantic adversaries.

The runtime remains experimental and non-plugin. It does not imply production
support, release, deployment, or project-specific adaptation.

## Intended use

Adapt this package when an accepted implementation plan must advance serially,
with one immutable task assigned to each fresh discussion. Install it through
dependency resolution so `agentjob-control` and
`continue-implementing-plan-task` remain available as its required closure.

## Runtime and offline tooling

`scripts/planctl.py` classifies project-contained JSON or text sources into
the seven frozen source classes and normalizes explicitly accepted authority.
It preserves valid canonical plans, synthesizes only missing required
structure, emits stable IDs and traceable split recommendations, and blocks
authority or precedence conflicts. Its exact golden output demonstrates
determinism. The legacy v1 selection path deterministically selects the first
pending task whose dependencies are terminal. Immutable v2 plans still return
`state_required` when no separate state is supplied; `select-next --state`
validates exact plan bytes, state revision, repository and lease fingerprints,
receipt links, amendment chains, supersessions, provider intents, and supplied
proofs before emitting a deterministic advisory proof. `validate-record`
supports every declared record profile and verifies canonical content hashes
where the contract defines one. `validate-state`, `diff`, `redact`, and
`reason-codes` provide read-only cross-record validation, immutable-task drift
evidence, hash-preserving output redaction, and a stable machine-readable
catalog. The focused suite verifies exact enum-to-fixture coverage,
deterministic corpus regeneration, file hashes, all positive records, exact
single-path negative diffs, and expected fail-closed results in addition to
source normalization and legacy compatibility. The tool writes no state,
reserves no task, and performs no provider or external effect.

## Adaptation summary

Bind project authority, durable state, repository identity, ThreadProvider,
task execution, verification, and recovery in the target project. Preserve the
zero-AgentJob launcher boundary, separate record types, and one-task-per-
discussion rule. Inherit effort from the applicable envelope; never install a
worker-local static effort.
