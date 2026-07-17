# Governed Continuation Website Adapter

This tracked directory configures the experimental `0.1.0` governed
continuation bundle for The AEther Flow Website.

`implementation_control/` remains the sole implementation authority. The
vendored runtime under `.agents/skills/` supplies durable goal state,
at-most-once generation consumption, receipts, recovery, and handoff
machinery. It is not bootstrapped as a second `.agents/control/` system.

Mutable SQLite state, tokens, continuation envelopes, activation receipts,
manual handoffs, and provider receipts are written only below ignored
`.local/sys4ai/continuation/`. Installer rollback transactions remain below
ignored `.local/sys4ai/install-transactions/`.

## Maintenance

1. Keep `.agents/skill_registry/SKILL_LOCK.yaml` and
   `.agents/skill_registry/SKILL_REGISTRY.yaml` pinned to the recorded source
   commit.
2. Do not edit `.agents/skills/{agentjob-control,continue,continue-goal,continue-implementing-goal}`.
   Adapt the website through `.codex/skills/`, this configuration, or
   `scripts/implementation_control/goal_relay_adapter.py`.
3. Run `npm run validate:goal-relay` after any adapter, front-door,
   configuration, registry, or package change.
4. Run `npm run test:goal-relay-runtime` after any vendor refresh. A source
   update requires a new reviewed lock and attribution update. The complete
   suite also requires the exact read-only fixtures under
   `.agents/examples/governed-continuation/` and the integration contract at
   `.agents/docs/skills/CODEX_CONTINUATION_INTEGRATION.md`; their source-pinned
   hashes are recorded in `website-adapter.json`.
5. Never use `--bootstrap` for this repository. Any proposal to introduce a
   competing control root requires a separate architecture decision and
   implementation-control packet.

No validation command launches a real goal, creates a Codex task, pushes,
deploys, refreshes upstream sources, or promotes a public claim.
