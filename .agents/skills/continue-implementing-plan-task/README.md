# Continue Implementing Plan Task

<!-- BEGIN GENERATED INSTALLATION BANNER -->
> **Internal component:** Do not install this folder as a root. Use its owning bundle or plugin.
>
> **Installation class:** `internal_component` / `internal_only`<br>
> **User-selectable:** no — not a user-selected install root<br>
> **Direct copy allowed:** no<br>
> **Required dependencies:** `agentjob-control`, `continue`<br>
> **Recommended bundle:** `implementation-plan-goal`<br>
> **Recommended plugin:** none<br>
> **Mutable state required:** no<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill continue-implementing-plan-task --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

## Release status

This package is an experimental `0.1.0` internal template. It provides the
profile-aware one-task worker, durable at-most-once invocation consumption,
PlanTaskReceipt v2 evidence, and protected recovery integration.

## Intended use

Install only as a dependency of `implementation-plan-goal`. A target-project
adaptation must bind canonical plan state, `continue`, repository and
checkpoint providers, validators, current-thread profile observation, and
explicit recovery.

## Adaptation summary

Preserve exact plan/task identity, at-most-once consumption, at most one
`continue` call, zero or one AgentJob, and the prohibition on starting a second
task in the same discussion. Inherit effort from envelope v2; never install a
worker-local static `max`.
