# Plan-Native Recursive Relay Cutover and Retirement

Date: 2026-07-22  
Authority:
`codex-thread:019f8ad5-73d1-77f2-8d9d-521ccc9c98df:user-message:any-issue-authorization`

## Cutover decision

New website implementation-plan runs now select `recursive_chain_v1` and
`.local/sys4ai/implementation-plan-relay/state.sqlite3`. The persistent
coordinator and generic outer Goal are disabled for new runs. The plan store
owns scheduling evidence only; `implementation_control/` remains the website
execution and protected-effect authority, and plan completion grants no
release effect.

Canonical source was committed and published as
`implementation-plan-relay-v0.3.0` at
`e9fd6cb5d836bd6b1ee19edef2f025a6ab9178e3`. The final source lock SHA-256 is
`72bbb35580e9b5678c8a126b7ae45c6ee2167983e4c75d0218a91a3dcbfe1fd2`.
The clean-source installer transaction
`620f37c82966485f86d7a02cf57dc6da` observed all six packages unchanged and
verified their installed hashes. Its receipt is
`.agents/skill_registry/INSTALL_RECEIPTS/bundle-implementation-plan-relay-620f37c82966485f86d7a02cf57dc6da.json`.

The installed source hashes are:

| Package | Version | SHA-256 |
| --- | ---: | --- |
| `agentjob-control` | 0.4.1 | `7700ecba131698b03cf0b8f81cd9507b2c8b8364fa9e109b50640ec9f063e53c` |
| `continue` | 0.4.0 | `f7b2ebb1df26ea31ba526458263a3745a1a23254e769c4bd72419c9eda9f8bad` |
| `continue-implementation-plan-relay` | 0.3.0 | `c98a4c1a2b19c1a3af5e4a555d189288cb558ae6ac4bbe1aeaba32ebf0718e17` |
| `continue-implementing-plan-task` | 0.3.0 | `ecea5223950c1a3ef250b9b8815021a415f84a63005627add552d34d18f318ee` |
| `implementation-plan-goal` | 0.3.0 | `38dad3a248185701a48c9320827723f0234beb04f92c5d4e907eff0bbeae2b7a` |
| `implementation-plan-relay` | 0.3.0 | `c0a2e0a70a0c92b350f6b736846d3482506177b6fc923bfdd988ad0a730b361c` |

The detailed machine-readable record is
`.agents/implementation-plan-relay/cutover-receipt.json`.

## State and rollback

Installation did not initialize recursive runtime state. It also left the
legacy database byte-identical at SHA-256
`ad7aecf857bc9153fa50722cee03b5136b7ea5790889c6c4440f83d01ce4cf5b`.
No dual write, active-run conversion, bootstrap, Python-package installation,
website push, or deployment occurred.

Rollback first sets `recursive_writer_enabled` to false and refuses new
launches. Installer rollback may use
`.local/sys4ai/install-transactions/620f37c82966485f86d7a02cf57dc6da/rollback.json`.
Both state trees must remain preserved. A claimed, consumed, or ambiguous run
stays in its native topology and is never converted.

## Compatibility-window observation

The window is grounded in one published recursive version plus the passing
three-task pilot, 25-case fault matrix, schema-3-through-7 read checks,
backup/import equivalence, installed-hash inspection, and website adapter
tests. Passive observation found no live recursive run and therefore no live
ambiguous intent, duplicate child, unknown invocation, lease anomaly,
terminalization failure, mirror failure, or automatic retry.

The legacy database contains three terminal plans: one `terminal_complete`
and two `terminal_validation_failed`. All 47 legacy provider intents are
finalized; no plan or goal lease remains active. Two pending task rows remain
inside the two terminal-validation-failed plans and are preserved as
historical evidence, not converted or reactivated.

## Retirement boundary

Coordinator mutation is retired from the default surface. New commands import
only the recursive adapter. Legacy mutation requires the explicit
`coordinator_v2_legacy` selector and is limited to a named historical run; it
cannot be selected implicitly. Default worker-to-coordinator wakeup and
`resume_thread(coordinator)` capability are absent.

Read-only legacy status/export and schema-3-through-7 support remain retained.
This is a compatibility archive, not a second new-run writer. The
machine-readable decision is
`.agents/implementation-plan-relay/retirement-receipt.json`.
