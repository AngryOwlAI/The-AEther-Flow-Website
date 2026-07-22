# implementation-plan-relay

<!-- BEGIN GENERATED INSTALLATION BANNER -->
> **Dependency-resolved workflow:** Select this skill with the installer; do not copy the folder without its required closure.
>
> **Installation class:** `user_workflow` / `dependency_resolved`<br>
> **User-selectable:** yes<br>
> **Direct copy allowed:** no<br>
> **Required dependencies:** `agentjob-control`, `continue-implementation-plan-relay`<br>
> **Recommended bundle:** `implementation-plan-relay`<br>
> **Recommended plugin:** none<br>
> **Mutable state required:** yes — `{project_root}/.local/sys4ai/implementation-plan-relay`; keep it outside installed skill/plugin trees and preserve it on uninstall<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill implementation-plan-relay --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

The public zero-AgentJob launcher for `recursive_chain_v1`. It validates one
accepted plan, commits generation 1 and one dispatch intent, records at most one
fresh worker discussion, and stops. It has no coordinator loop and no native or
generic Goal authority.

Runtime entry point: `scripts/relayctl.py`. Canonical state operations live in
`agentjob_runtime.plan.relay`; the eight versioned schemas in `schemas/`
describe the durable logical contracts. `templates/` contains safe token-hash-
only record starters, while `examples/` covers launch, nonterminal receipt,
terminal completion, human gate, and invocation-unknown states.

`relayctl.py validate-record` validates one logical record. `project-chain`
creates a read-only cross-record projection, and `validate-chain` checks exact
run/generation/envelope/intent/receipt/lease/completion identity and
cardinality with stable reason codes.

Launch accepts only `sys4ai.plan-relay-acceptance.v1`: copy the complete
read-only acceptance basis, add `accepted: true` and one nonblank
`acceptance_evidence_ref`, and change no bound value. Plan, task graph,
repository, control, launcher discussion, effort, authority, grant, profile,
or topology drift invalidates the acceptance before state initialization.

Install through a resolved bundle. Direct copying is unsupported because the
launcher requires the shared transactional runtime and recursive frame.
