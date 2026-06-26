# Curator Drift Report

This repo-internal report compares declared website source dependencies
against the current upstream source repository. It is not a public page
and does not rewrite website content.

## Summary

- Source commit: `76196604fe93300a3086e38102a20e81e1b0cd28`
- Source commit date: `2026-06-26T14:52:34-06:00`
- Declared dependencies: 50
- Drift items: 3
- Critical drift: 3
- Review-required drift: 0
- Informational drift: 0

## Drift Items

### /project/physics/current-state/

- Source path: `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- Severity: `critical`
- Impact: `current_state_source`
- Old hash: `7e5864f1c5920de351ea7a982648a6d5562e9725dcf6c99be76f6cb8cd4b0209`
- New hash: `b04a4ccd85eaafa0fb90e93df61d4566d5de97790b7a9e1c64801f559d54fcde`
- Recommended action: Refresh the current-state snapshot and review the public page boundary.
- Acknowledgement: `not_evaluated`

### /project/physics/current-state/

- Source path: `registries/DISTANCE_TO_GR_LEDGER.csv`
- Severity: `critical`
- Impact: `current_state_source`
- Old hash: `a3441822c0634adcf12aaa9310d22e83ed00392f97c47042b74d8e59d081bc40`
- New hash: `a6b6bc9be980559919f407477f44225d1c0cd7c25b34a289d8d76633b6131c69`
- Recommended action: Refresh the current-state snapshot and review the public page boundary.
- Acknowledgement: `not_evaluated`

### /project/physics/current-state/

- Source path: `research_control/program_state.yaml`
- Severity: `critical`
- Impact: `current_state_source`
- Old hash: `56e06f0c8bd4963105008b6b388aaf52ebd231dc8909b1b593cbace6d54c396c`
- New hash: `d62c27b33c50e2b49e519f30e49e41b9285a2cd24799224fe5d30eec087b468c`
- Recommended action: Refresh the current-state snapshot and review the public page boundary.
- Acknowledgement: `not_evaluated`


## Diagnostics

- `source_summary_lag` (informational): current_frontier.md does not mention the latest program_state handoff handoff-0230. Source: `research_control/current_frontier.md`
- `source_summary_lag` (informational): current_frontier.md does not mention the active program_state task RT-20260614-197. Source: `research_control/current_frontier.md`
