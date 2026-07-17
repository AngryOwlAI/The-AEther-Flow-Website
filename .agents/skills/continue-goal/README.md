# Continue Goal

## Release status

This package is an experimental `0.1.0` template with lifecycle status
`draft`. Relay use requires explicit finite guards, local state, and a declared
ThreadProvider; installation alone authorizes none of those operations.

`continue-goal` is the launcher for a durable fresh-discussion goal relay. It
persists exact goal identity and finite guards, dispatches one first-generation
worker, and stops. It executes zero AgentJobs and never substitutes same-thread
follow-up for a successor.

## Dependencies

Install `agentjob-control` and `continue-implementing-goal` with compatible
protocol versions. Configure a project-local SQLite or file-journal state root
and either an automatic ThreadProvider or the manual-handoff provider.

## Storage and secret boundary

Goal and completion-contract text are plaintext local records. Do not place
credentials, tokens, keys, or sensitive personal data in them. Mutable relay
state must remain outside installed skill or plugin directories.

## Adaptation summary

Bind repository identity, storage, provider, and guard values in the target
project. Do not change the zero-AgentJob launcher boundary or the one-successor
reservation rule.
