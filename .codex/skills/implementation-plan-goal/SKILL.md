---
name: implementation-plan-goal
description: Prepare and coordinate one accepted canonical implementation plan through the website-local implementation-control adapter.
---

# Website Implementation Plan Goal

Use `npm run plan-goal -- <command>` as the only project-local façade.

Before activation, run `prepare` and present its exact combined acceptance.
That acceptance binds the goal, reasoning effort, canonical plan and binding
hashes, checkout identity, website control hash, and authorization to create
fresh local Codex tasks. Any bound value change requires a new preparation and
acceptance.

The canonical website records under `implementation_control/` remain sole
execution authority. The imported SQLite runtime schedules tasks and preserves
receipts, provider intent, at-most-once consumption, and recovery. Never invoke
the imported generic executor or create `.agents/control`.

The launcher reserves at most one task and creates no AgentJob. Task creation
is performed by the caller from the returned create request. Use
`adopt-worker` to bind the returned task ID and verified profile before sending
the returned token-bound prompt. Do not retry an ambiguous create result.

Checkpoint, commit, branch, worktree, push, deployment, public-claim, and
upstream-write rights come only from the selected website packet.
