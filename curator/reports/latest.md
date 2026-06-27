# Curator Drift Report

This repo-internal report compares declared website source dependencies
against the current upstream source repository. It is not a public page
and does not rewrite website content.

## Summary

- Source commit: `61dd2ec11ca2fad09431b50d223559c02f05e634`
- Source commit date: `2026-06-26T20:49:38-06:00`
- Declared dependencies: 56
- Drift items: 5
- Critical drift: 3
- Review-required drift: 2
- Informational drift: 0
- Matched acknowledgements: 0

## Drift Items

### /project/physics/current-state/

- Source path: `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- Severity: `critical`
- Impact: `current_state_source`
- Old hash: `cdc4625d009801b57ef56f81c4f22bc9c9315b4174f2143166347a371b0f3711`
- New hash: `2f7e4b987a92d52c2cb8b5453a6d200568b552ab5d0f79feaa867b34930b1b00`
- Recommended action: Refresh the current-state snapshot and review the public page boundary.
- Acknowledgement: `not_allowed`

### /project/physics/current-state/

- Source path: `registries/DISTANCE_TO_GR_LEDGER.csv`
- Severity: `critical`
- Impact: `current_state_source`
- Old hash: `3f2636a03420ccd15ee75b234e5ed80535ef514d96a21e65e9af17d897366080`
- New hash: `ce18062e5e12f0c68b39d21cf5fd27a0268ab8c9b2ba49cd53aedd89a5bd4c01`
- Recommended action: Refresh the current-state snapshot and review the public page boundary.
- Acknowledgement: `not_allowed`

### /project/physics/current-state/

- Source path: `research_control/program_state.yaml`
- Severity: `critical`
- Impact: `current_state_source`
- Old hash: `e3de09d2298d9e4d7c65a1067457293668d3763650caf536d3281afa0d5bddf6`
- New hash: `a71f4d611eb68adb41a5dcaf6ab7ee28ff418149feaf40c5a5a86bd11be03b2d`
- Recommended action: Refresh the current-state snapshot and review the public page boundary.
- Acknowledgement: `not_allowed`

### /resources/

- Source path: `registries/TEX_SOURCE_REGISTRY.csv`
- Severity: `review_required`
- Impact: `mapped_route_source`
- Old hash: `8be681630cd1dc60af944aa8ec44c0cc3e741ad744e46a57912d86532b4fb66d`
- New hash: `9ad30eb6854529d6420a8523400b7dd23bbbad90965a25266a120388b62df3b0`
- Recommended action: Review the affected internal page against its upstream source dependency.
- Acknowledgement: `missing`

### /resources/documents/

- Source path: `registries/TEX_SOURCE_REGISTRY.csv`
- Severity: `review_required`
- Impact: `mapped_route_source`
- Old hash: `8be681630cd1dc60af944aa8ec44c0cc3e741ad744e46a57912d86532b4fb66d`
- New hash: `9ad30eb6854529d6420a8523400b7dd23bbbad90965a25266a120388b62df3b0`
- Recommended action: Review the affected internal page against its upstream source dependency.
- Acknowledgement: `missing`


## Diagnostics

- `source_summary_lag` (informational): current_frontier.md does not mention the latest program_state handoff handoff-0258. Source: `research_control/current_frontier.md`
- `source_summary_lag` (informational): current_frontier.md does not mention the active program_state task RT-20260614-225. Source: `research_control/current_frontier.md`
