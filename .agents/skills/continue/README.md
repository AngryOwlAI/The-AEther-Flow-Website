# Continue

<!-- BEGIN GENERATED INSTALLATION BANNER -->
> **Dependency-resolved workflow:** Select this skill with the installer; do not copy the folder without its required closure.
>
> **Installation class:** `user_workflow` / `dependency_resolved`<br>
> **User-selectable:** yes<br>
> **Direct copy allowed:** no<br>
> **Required dependencies:** `agentjob-control`<br>
> **Recommended bundle:** `governed-continuation`<br>
> **Recommended plugin:** `sys4ai-governed-continuation`<br>
> **Mutable state required:** no<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill continue --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

## Release status

This package is an experimental `0.3.0` template with lifecycle status
`draft`. Use it for governed validation and neutral pilots only after the target
project supplies explicit adapters, policy, and authority.

`continue` is the user-facing bounded transaction skill for a configured
AgentJob project. One invocation resolves current authority and executes zero
or one activated job. It never starts a successor discussion.

## Required dependency

Version `0.3.0` returns `sys4ai.continue-result.v2`, classifies machine repair
separately from human intervention, preserves failed validator/checkpoint
evidence, and requires repository-topology enforcement for command-capable
AgentJobs.

The skill requires the `agentjob-control` template and a target-project
configuration that supplies control, repository, policy, validation, and
checkpoint capabilities. Without them it returns `bootstrap_required` and
performs no work.

## Inputs and output

Supply an explicit `<PROJECT_ROOT>` and, when needed, a task ID. The output is a
validated `sys4ai.continue-result.v1` object with canonical IDs, fingerprints,
validator counts, and a stable next-action reason.

## Portability boundary

The template contains no fixed repository name, branch rule, role catalog,
domain claim rule, checkpoint command, or deployment permission. Those belong
in project adapters and policy packs.

## Adaptation summary

Install the template in the target project, bind `agentjob-control`, configure
providers, and add only the domain extensions the project actually requires.
Do not widen the one-job maximum or enable thread creation.
