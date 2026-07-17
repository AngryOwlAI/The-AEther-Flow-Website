# Continue

## Release status

This package is an experimental `0.1.0` template with lifecycle status
`draft`. Use it for governed validation and neutral pilots only after the target
project supplies explicit adapters, policy, and authority.

`continue` is the user-facing bounded transaction skill for a configured
AgentJob project. One invocation resolves current authority and executes zero
or one activated job. It never starts a successor discussion.

## Required dependency

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
