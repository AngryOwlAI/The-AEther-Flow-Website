---
name: agentjob-control
description: Internal support boundary for the pinned plan scheduler, receipts, provider intent, and recovery runtime.
---

# AgentJob Control Support

Internal support provider. Do not select this skill directly.

The exact installed runtime under `.agents/skills/agentjob-control` supplies
the native SQLite plan revision, scheduling, lease, provider-intent,
PlanTaskReceipt v2, and recovery contracts. Website `implementation_control/`
records remain execution authority in declared `emulated` conformance mode.

The generic filesystem executor is disabled because it is bound to
`.agents/control`. Mutable state belongs only below
`.local/sys4ai/implementation-plan-goal/`.
