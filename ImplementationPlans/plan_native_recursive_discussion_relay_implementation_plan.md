# Plan-Native Recursive Discussion Relay Implementation Plan

## Document control

| Field | Value |
| --- | --- |
| Plan ID | `PLAN-SYS4AI-RECURSIVE-RELAY-001` |
| Status | Proposed; decision-ready; not accepted execution authority |
| Purpose | Replace the generic-goal-coupled, fixed-coordinator implementation-plan runtime with a plan-native, SQLite-backed recursive discussion relay |
| Primary implementation repository | `/Volumes/P-SSD/AngryOwl/skills-Sys4AI` |
| Adaptation repository | `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website` |
| Plan location | `ImplementationPlans/plan_native_recursive_discussion_relay_implementation_plan.md` |
| Source analysis | `/Users/alex.omegapy/.codex/attachments/ccedaa7d-f4ee-48c8-a2e2-ea8a096c17f4/pasted-text-1.txt` |
| Source SHA-256 | `33762f1a5e5f86e849be0a820a86026c53b518814157a278615339a9298a4e90` |
| Source size | 898 lines; 42,476 bytes |
| Website baseline inspected | `b5da31f3a4b25a4c0b3515f7d0d5eb71c917c81a` |
| Canonical skills baseline inspected | `7124baf2026f3ba392d9a81ce4feef55503f67d4` |
| Plan date | 2026-07-22 |
| Required sequence | Stabilize current terminalization, approve architecture decisions, implement canonical runtime, release canonical bundle, reinstall and adapt website, pilot, cut over |
| Validation posture | Focused and minimal; no repeated aggregate validation and no unrelated website tests |
| Recommendation coverage | Verified pass: 123 of 123 recommendations mapped to implementation tasks and acceptance paths |

### Implementation authorization boundary

This Markdown file is a planning artifact only. Creating or accepting it does
not authorize any of the following:

- modifying `/Volumes/P-SSD/AngryOwl/skills-Sys4AI`;
- changing the website runtime, installed skills, or `implementation_control/`;
- creating branches or worktrees;
- staging, committing, pushing, merging, tagging, releasing, or deploying;
- converting or deleting existing SQLite state;
- creating Codex discussions, native Codex Goals, or external provider effects;
- publishing new scientific, mathematical, operational, or authority claims.

Each implementation task must be selected and authorized through the live
control system applicable to its repository. In the website repository,
`implementation_control/` remains the execution authority. This plan supplies
scope and sequence; it does not supersede live tasks, jobs, handoffs, leases,
receipts, approval gates, or repository state.

## 1. Executive decision

The target is a **plan-native SQLite recursive discussion relay**:

```text
launcher -> generation 1 -> generation 2 -> ... -> terminal plan receipt
```

The target must replace this default topology:

```text
permanent coordinator -> worker 1 -> permanent coordinator -> worker 2
```

The redesign has five controlling decisions:

1. The accepted implementation plan and plan-native SQLite records are the
   orchestration authority. A generic outer goal is not created for new runs.
2. The launcher initializes and dispatches generation 1, then stops. Each
   relay frame owns exactly one generation and may schedule, but never execute,
   at most one distinct next-task successor.
3. The existing deterministic scheduler, compare-and-swap revisions, hashes,
   receipts, provider intents, repository binding, authority checks, protected
   effects, append-only evidence, and SQLite atomicity are preserved.
4. The canonical `skills-Sys4AI` package is redesigned and versioned before
   its generated or installed copies are updated in the website.
5. Validation is proportional: all material safety properties remain
   executable acceptance conditions, but they are implemented through a small
   focused suite, a table-driven recovery test, and one disposable relay pilot.

Updating the website to the current canonical `implementation-plan-goal`
version `0.2.0` is not the final solution. That version automates continuation
by resuming the same coordinator and therefore preserves the ownership model
this plan is intended to remove.

## 2. Source interpretation and evidence rules

### 2.1 Source hierarchy

1. Current tracked canonical source in `skills-Sys4AI` governs the reusable
   runtime and package as it exists at implementation time.
2. Current tracked website source and `implementation_control/` govern the
   website adaptation and its allowed effects.
3. The attached analysis is the recommendation source for this plan.
4. Historical databases, journals, receipts, and installer records are audit
   evidence. They must be preserved and must not be rewritten to fit the new
   model.
5. Memory, generated summaries, status prose, and worker prose are orientation
   or telemetry only until verified against tracked files and canonical state.

### 2.2 Baseline findings used by this plan

At the inspected baselines, current tracked code corroborates the source
analysis in the following material respects:

- the installed website adapter imports generic-goal activation and
  initialization code for new plan activation;
- the website session persists `coordinator_thread_id`;
- successor reservation is coordinator-only;
- the website CLI requires `--coordinator-thread-id` for `reserve-next` and
  recovery;
- the current completion-candidate branch does not expose a first-class
  tracked `finalize-plan` command;
- canonical `0.2.0` describes a continuously resumed coordinator and contains
  `wait_for_terminal`, `resume_thread`, coordinator wakeup, and `goal_reached`
  paths;
- the canonical plan store constructs a generic `SQLiteGoalStore` as part of
  plan authority.

The attached analysis also reports historical live-state observations and two
terminalization event names whose writer was not found. Those observations are
not assumed current. Phase 00 requires a new read-only audit before any runtime
mutation.

### 2.3 Later user constraint on test overhead

The source analysis proposed a broad acceptance suite. The later instruction
for this plan requires only necessary testing and validation. This plan
therefore preserves every recommended acceptance property while consolidating
execution as follows:

- one focused plan-store/state-machine suite;
- one focused provider and recovery suite, parameterized over all named crash
  boundaries;
- one focused website adapter suite;
- one three-task disposable end-to-end pilot;
- one final aggregate repository gate per affected repository, run once at the
  release boundary rather than after every task.

No new browser matrix, accessibility audit, route crawl, content validator,
claim validator, manifest regeneration, SVG validator, or repeated Astro build
is required unless an authorized implementation task actually changes the
surface governed by that check.

## 3. Goals, non-goals, and success definition

### 3.1 Goals

- Make recursive worker-owned discussion chaining the default topology for new
  implementation-plan runs.
- Remove mandatory generic outer-goal state from new plan writers.
- Retain SQLite as the durable atomic state and evidence store.
- Enforce at-most-once task invocation and provider creation across crashes.
- Provide deterministic recovery for every external-create and task-invocation
  uncertainty boundary.
- Add an explicit, CAS-bound plan terminalization path with an immutable
  completion report.
- Keep native Codex Goal integration optional and mirror-only.
- Keep website `implementation_control/` authoritative for actual website task
  execution and protected effects.
- Preserve legacy records byte-for-byte and keep them readable for audit.
- Provide compatibility shims for the old public skill names without retaining
  coordinator scheduling semantics in the new writer path.
- Make the new canonical package portable and then reinstall it through the
  normal dependency-resolved installer and provenance workflow.
- Provide passive status, chain inspection, and concise operator recovery
  commands without creating a hidden coordinator.

### 3.2 Non-goals

- Do not copy the upstream research relay's paired-file storage mechanism.
- Do not make Codex native Goal state the scheduler or completion authority.
- Do not synchronize a generic outer goal indefinitely with plan state.
- Do not patch `.agents/skills/`, `.codex/skills/`, or generated plugin files as
  the primary implementation.
- Do not convert an active plan from coordinator topology to recursive topology
  in place.
- Do not dual-write new runs into both coordinator and recursive state.
- Do not infer successful migration from a version number alone.
- Do not delete historical databases, journal entries, receipts, events,
  exports, locks, or installer records.
- Do not allow a relay frame to execute a second task.
- Do not create an automatic same-task successor.
- Do not treat a missing ready task as proof that the plan is complete.
- Do not add new public website routes or alter reader-facing scientific
  claims as part of this runtime redesign.
- Do not authorize stage, commit, push, deployment, publication, or upstream
  writes merely because a plan reaches terminal completion.

### 3.3 Definition of success

The redesign succeeds when a new disposable three-task plan produces this
auditable chain:

```text
launcher -> worker A -> worker B -> worker C -> terminal
```

and direct state evidence establishes all of the following:

- one launcher and three worker discussions exist;
- the launcher executed zero AgentJobs;
- exactly three task invocations and three immutable task receipts exist;
- generations 2 and 3 name the immediately preceding worker as predecessor;
- no worker wakes or resumes a permanent coordinator;
- the terminal worker creates no child;
- no generic outer-goal row was created for the run;
- no duplicate provider create, consume, receipt, or successor was accepted;
- the terminal plan receipt was created atomically with lease release;
- legacy records remain readable and unchanged;
- no unapproved repository or external effects occurred.

## 4. Decision register

All decisions below must be recorded in an accepted architecture decision
record before Phase 02 begins. “Recommended” means this plan supplies a default;
it does not bypass the named approval gate.

| ID | Decision | Recommended disposition | Gate |
| --- | --- | --- | --- |
| `DEC-001` | Default topology | `recursive_chain_v1`; no permanent coordinator | Architecture approval |
| `DEC-002` | Public skill name | `implementation-plan-relay`; retain `implementation-plan-goal` as a deprecated launcher shim | Architecture approval |
| `DEC-003` | Recursive frame name | `continue-implementation-plan-relay`; retain `continue-implementing-plan-task` as a deprecated frame shim | Architecture approval |
| `DEC-004` | New-run storage | New plan-native database at `.local/sys4ai/implementation-plan-relay/state.sqlite3` | Migration approval |
| `DEC-005` | Shared-database fallback | Additive migration `008_plan_native_discussion_relay.sql` only if one database is mandatory | Migration approval |
| `DEC-006` | Repository lease | One plan-native mutation owner per bound repository; expiry is diagnostic and never grants takeover | Architecture approval |
| `DEC-007` | Native Codex Goal | Optional UI mirror with `mirror_only` and `may_mark_complete=false` | Architecture approval |
| `DEC-008` | Provider contract | Fresh discussion in the same saved project and bound checkout; explicit effort; create/list/query support; no required resume | Capability approval |
| `DEC-009` | Human gate | Protected nonterminal or terminal disposition, no successor, explicit human reconciliation or cancellation | Safety approval |
| `DEC-010` | Unknown consumed work | Quarantine; never rerun automatically | Safety approval |
| `DEC-011` | Legacy compatibility duration | At least one released compatibility window; retire mutation commands only after audit confirms no required writers | Release approval |
| `DEC-012` | Python support | Prefer Python 3.11-compatible syntax; otherwise explicitly raise the declared minimum | Package approval |
| `DEC-013` | Validation | Focused suites during implementation; one final aggregate gate per repository | Plan acceptance |
| `DEC-014` | Existing canonical phased plan | Preserve as historical context; supersede explicitly rather than rewrite completed evidence | Architecture approval |

## 5. Target architecture and authority model

### 5.1 Control flow

```text
                    +--------------------------------------+
                    | Plan-native SQLite relay state       |
                    | revisions, hashes, tasks, receipts,  |
                    | leases, intents, journal, completion |
                    +--------------------------------------+
                         ^          ^            ^
                         |          |            |
launcher --create once--> G1 --create once--> G2 ... --> terminal
   stop                  stop                  stop

Optional Codex Goal mirror <--- read-only projection --- relay state
Website implementation_control <--- execution evidence --- task executor
```

The state helper performs local atomic mutations only. The skill or thread
provider performs the external discussion creation between a committed dispatch
intent and a second CAS transaction that records the returned successor.

### 5.2 Ownership and responsibility

| Component | Owns | Must not do |
| --- | --- | --- |
| Launcher discussion | Validate acceptance and identities; initialize run; select first task; reserve generation 1; persist one intent; create and record one successor; stop | Execute an AgentJob; wait for the plan; resume itself; create generation 2 |
| Relay frame N | Validate envelope; wait for predecessor record; claim; consume; invoke one bound task; verify; finalize; terminalize or create one N+1 successor; stop | Execute another task; create a same-task retry; create two successors; trust prose as evidence |
| Task executor / `continue` | Execute only the immutable task bound to the consumed generation | Select the next task; mutate orchestration state outside its receipt contract |
| Plan store | Plan revision; selection proof; generation state; receipts; leases; dispatch intents; journal; terminal report | Call Codex; infer external success; authorize website effects |
| Thread provider | Create, list, and query discussions; return exact identity and capability evidence | Decide task readiness, plan completion, retry authority, or lease ownership |
| Website `implementation_control/` | Website task scope, validators, checkpoints, protected effects, and execution authority | Delegate authority to plan prose or provider state |
| Status surface | Read-only summary and chain projection from any discussion | Schedule, claim, consume, dispatch, retry, or complete |
| Native Codex Goal mirror | Optional UI projection | Select, dispatch, retry, mutate, or mark the canonical plan complete |
| Human reviewer | Resolve genuine authority, ambiguous child, cancellation, and integrity gates | Retroactively rewrite evidence to make a failed transition appear valid |

### 5.3 Authority precedence

For a website-bound task, resolve conflicts in this order:

1. repository identity and current tracked files;
2. live `implementation_control/` task, job, handoff, completion, and approval
   records;
3. plan-native relay state and immutable plan/task binding;
4. verified provider and thread identity receipts;
5. task receipt and validator output;
6. passive status projection;
7. worker or coordinator prose.

Plan-native state proves orchestration history. It does not grant a stage,
commit, push, deployment, publication, upstream-write, branch, worktree, or
other protected effect that the website control plane has not authorized.

## 6. Mandatory invariants

### 6.1 Cardinality

| Invariant | Required value |
| --- | ---: |
| Launcher AgentJobs | exactly `0` |
| Tasks executed per relay frame | `0` or `1` |
| Direct `continue` calls per relay frame | `0` or `1` |
| AgentJobs per relay frame | `0` or `1` |
| Successors created per relay frame | `0` or `1` |
| Same-task automatic successors | exactly `0` |
| Active generations per plan | at most `1` |
| Provider create calls authorized per generation | at most `1` |
| Finalized receipts for a completed or protected execution frame | exactly `1` |

### 6.2 Identity and sequencing

- Generation `N+1` must record generation N's worker thread as predecessor.
- Only generation 1 may record the launcher as predecessor.
- A child that starts before `successor_created` is recorded waits read-only
  and cannot claim or consume.
- The current thread must equal the recorded successor before claim.
- Plan ID/hash, effective plan revision, task ID/hash, generation, topology,
  repository binding, website-control fingerprint, authority manifest,
  reasoning profile, predecessor, token hash, idempotency key, and receipt hash
  must match at every transition where they are relevant.
- A stale or mismatched identity fails before selection, claim, consumption,
  dispatch, or completion.

### 6.3 At-most-once execution

- A generation is consumed immediately before the task call.
- A consumed generation is never automatically rerun.
- Competing claims produce exactly one winner.
- Duplicate consume fails.
- Re-recording the same successor ID is idempotent.
- Re-recording a different successor ID fails.
- A second provider create is never authorized for the same generation.
- A worker cannot execute or reserve work for a second task within the same
  generation.

### 6.4 Authority and evidence

- Worker prose is telemetry, never completion evidence.
- Completion requires canonical repository, website-control, receipt,
  dependency, and validator evidence.
- “No ready task” is distinct from “all effective tasks terminal and complete.”
- A native Goal mirror cannot mutate plan state or establish completion.
- Lease expiration is diagnostic only and does not authorize lease theft.
- Terminal, human-gated, integrity-blocked, capability-blocked, ambiguous, and
  consumed-unknown frames create no successor.

## 7. Plan-native record model

Final schema identifiers and field names are frozen by `DEC-001` through
`DEC-012`. The following logical records and semantics are mandatory.

| Record | Purpose | Required content |
| --- | --- | --- |
| `PlanRelayRun v1` | Root state for one accepted plan execution | Relay ID; canonical plan ID/hash; accepted objective hash; effective plan revision; repository binding hash; authority hash; reasoning profile hash; topology; current generation; status; journal head; created/updated timestamps |
| `PlanRelayGeneration v1` | Permanent state for one discussion generation | Relay ID; generation; route kind; task ID/hash; predecessor thread; recorded worker thread; handoff token hash; idempotency key; claim/consume/invocation state; receipt hash; successor ID; expected revisions |
| `PlanTaskEnvelope v3` | Immutable worker input | Relay and plan identity; task identity; generation; repository and website-control binding; reasoning profile; selection proof; predecessor; topology contract; allowed effects; token-binding metadata |
| `PlanTaskReceipt v3` | Direct task evidence | Continue, AgentJob, provider, and successor counts; required validators; changed paths; before/after fingerprints; task disposition; checkpoint or protected-effect evidence; uncertainty; receipt hash |
| `PlanDispatchIntent v3` | Exactly-once external-create boundary | Relay/generation; provider; idempotency key; token hash; create budget; attempt count; expected predecessor and profile; outcome; returned thread ID; response hash; reconciliation state |
| `PlanRelayLease v1` | Plan-native repository mutation ownership | Repository fingerprint; relay/generation; holder kind; thread ID; token hash; transaction ID; diagnostic expiry; status; transfer history |
| `PlanCompletionReport v1` | Canonical terminal proof | Effective plan hash; every effective task's terminal receipt; required validators; dependency-completion proof; no open intent; no active lease; final repository/control fingerprints; journal head |
| `CodexGoalMirror v1` | Optional UI summary | Relay ID; generation; status; canonical state reference; `authority_effect=mirror_only`; `may_mark_complete=false` |

### 7.1 New-writer exclusions

The new recursive writer profile must not require or author:

- `outer_goal_id`;
- `expected_outer_revision`;
- `outer_holder_token`;
- `GoalMutation`;
- `SQLitePlanStore.goal_store` as plan authority;
- `goal_reached` as plan status or completion terminology;
- coordinator wakeup records;
- `coordinator_thread_id` as mutable owner;
- provider capabilities for `wait_for_terminal` or `resume_thread`.

The new writer path must not import `agentjob_runtime.goal.activation`,
`agentjob_runtime.goal.initialize`, or `GoalMutation`.

### 7.2 Neutral utilities retained

Move or expose the following through neutral namespaces before removing plan
runtime dependencies on generic-goal modules:

- canonical JSON serialization;
- SHA-256 content and identity helpers;
- UTC parsing and normalized timestamp helpers;
- SQLite migrations, backup, restore, and connection infrastructure;
- transaction and lock helpers;
- common error and reason-code types.

The extraction must preserve behavior and avoid duplicating security- or
integrity-sensitive logic.

## 8. Lifecycle and transaction contract

### 8.1 Launcher transaction

After exact combined acceptance, the launcher must:

1. verify the canonical plan, effective dependency graph, task hashes,
   repository binding, current discussion identity, requested/effective
   reasoning effort, authority manifest, topology, and protected-effect grants;
2. initialize one `PlanRelayRun` without a generic outer goal;
3. select the first dependency-ready task deterministically;
4. persist a selection proof bound to the expected plan revision;
5. reserve generation 1;
6. generate an opaque handoff token and persist only its hash in canonical
   state;
7. persist one `PlanDispatchIntent` with `create_budget=1` and `attempts=0`;
8. commit the reservation transaction;
9. call the authorized thread-create capability exactly once;
10. record the concrete successor ID, provider response hash, and lease
    transfer in a second CAS-bound transaction;
11. stop immediately, without waiting, resuming, or executing an AgentJob.

If the external create result is ambiguous, the launcher records ambiguity and
enters reconciliation. It does not retry blindly.

### 8.2 Relay-frame entry

Generation N must:

1. resolve the exact canonical relay-state location from the minimal handoff;
2. validate plan, task, generation, token, idempotency key, repository,
   website-control, authority, reasoning profile, predecessor, current thread,
   and topology identities;
3. confirm its current thread equals the recorded successor;
4. if the predecessor has not recorded `successor_created`, poll read-only for
   a bounded interval;
5. claim the generation once through CAS;
6. reject stale, duplicate, mismatched, consumed, or concurrently owned
   generations before any task effect.

### 8.3 Task execution

The claimed frame must:

1. reinspect live repository and website-control state;
2. compile the exact task-local `continue` invocation;
3. persist consumption immediately before the invocation;
4. invoke `continue` at most once for the bound task;
5. record `returned` when a direct return is observed;
6. record `unknown`, quarantine the generation, and create no successor when
   the call/return boundary is uncertain;
7. reinspect canonical files and control evidence rather than trusting returned
   prose;
8. run only the validators required by the bound task and affected surface;
9. construct one immutable `PlanTaskReceipt`.

### 8.4 Post-task decision

Prefer one atomic post-task transaction that:

1. finalizes the task receipt;
2. updates effective task and phase state;
3. revalidates the effective dependency graph and any accepted amendment or
   supersession chain;
4. selects the next dependency-ready task or proves canonical completion;
5. appends the selection, protected-stop, or completion proof;
6. performs exactly one of these dispositions:
   - terminalize the plan, release the lease, and append the completion receipt;
   - reserve generation N+1, transfer the lease to `successor_reserved`, and
     insert one dispatch intent;
   - record a protected nonterminal or terminal state without a successor.

The provider call occurs outside this transaction. If continuation is selected,
the frame performs the one authorized create, records the child, and stops.

### 8.5 Terminalization

`finalize-plan` must be a first-class CAS-bound operation. It must reject
terminalization unless the immutable `PlanCompletionReport` establishes:

- the effective plan hash and revision;
- terminal receipts for every effective task;
- satisfied dependencies and no unresolved replacement chain;
- required validator results;
- no open or ambiguous dispatch intent;
- no active task invocation;
- no active repository lease after the transaction;
- matching final repository and website-control fingerprints.

The transaction must append the terminal report/receipt, change the plan to its
terminal state, and release the lease atomically. Completion-proof logic from
canonical `0.2.0` may be reused after removing coordinator coupling and
`goal_reached` terminology.

### 8.6 Minimal successor prompt

Do not copy the full plan or mutable status prose into successor prompts. Use a
small continuation token whose routing facts are verified against SQLite:

```text
Use $continue-implementation-plan-relay.

This is one authorized frame of a user-requested implementation-plan relay.
relay_state: <exact absolute state reference>
relay_id: <relay id>
plan_id: <plan id>
expected_generation: <N>
handoff_token: <opaque token>
idempotency_key: <relay id>:<N>

Wait for the predecessor handoff to reach successor_created, then validate and
claim this exact generation. Execute at most one bound plan task and create at
most one generation N+1 successor.
```

The raw token must not be written to durable logs, status output, receipts, or
provider-response summaries. Durable records store the token hash.

## 9. Command surface

All mutating commands require expected plan revision, expected repository and
control fingerprints, current-thread evidence when applicable, and structured
reason codes. Commands print canonical structured output suitable for receipts.

| Command | Disposition | Required behavior |
| --- | --- | --- |
| `prepare` | Retain | Read-only classification, normalization, plan/binding inspection, and acceptance proposal |
| `launch` or `activate-relay` | Replace activation loop | Initialize plan-native state, reserve generation 1, persist intent; never run the plan loop |
| `record-successor` | Add | Idempotently record the returned child ID and response hash for an existing intent |
| `adopt-successor` | Add, degraded/manual only | Adopt exactly one proven matching unclaimed child after reconciliation policy authorizes it |
| `claim-generation` | Rename/replace `worker-prepare` | Verify the envelope and atomically claim one generation |
| `consume-generation` | Rename/replace `worker-consume` | Persist at-most-once consumption immediately before task invocation |
| `record-returned` | Add/split from finalize | Record direct return proof without deciding completion |
| `record-unknown` | Rename/retain semantics | Quarantine an uncertain consumed invocation; authorize no retry or child |
| `verify-and-decide` | Add | Reinspect canonical evidence, finalize receipt, and select terminal, successor, or protected stop |
| `reserve-successor` | Replace `reserve-next` | Bind generation N+1 to N's worker, receipt hash, expected revision, and one create budget |
| `finalize-plan` | Add | Validate completion report and atomically terminalize/release/receipt |
| `reconcile-dispatch` | Add | Query by idempotency key and classify zero, one, multiple, or uncertain child evidence |
| `abandon-unconsumed` | Add | Release or replace a generation only when non-consumption is directly proven |
| `reconcile-consumed` | Add | Record direct return proof or permanent unknown state; never rerun automatically |
| `summarize` | Add | Passive plan/chain/status/recovery projection; no mutation |
| `cancel` | Add | Record explicit cancellation, release allowed leases, and create no child |
| Legacy coordinator commands | Deprecate | Read-only or explicitly selected legacy mode during compatibility window; never default writer path |

Prefer small crash-auditable mutations. Do not hide a provider call and several
state changes behind a helper that cannot identify which boundary failed.

## 10. Exactly-once recovery matrix

| Failure boundary | Mandatory recovery |
| --- | --- |
| Before reservation commits | Retry only against the same expected revision |
| Reservation committed; create not attempted | Current proven owner may perform the one authorized create |
| Create returns a concrete ID; record fails | Retry `record-successor` only; never call create again |
| Create result ambiguous | Query child/task evidence by idempotency key; do not retry blindly |
| Exactly one matching unclaimed child | Adopt and record only after all identity checks pass |
| Zero children conclusively proven | Record definitive failure; replacement generation requires recovery policy |
| Multiple or uncertain matching children | Quarantine and require human reconciliation |
| Child begins before `successor_created` | Child waits read-only and cannot claim or consume |
| Crash after claim but before consume | Only the same proven thread or explicitly authorized adoption may resume |
| Crash after consume | Never rerun automatically; record `unknown` unless direct return proof exists |
| Receipt finalized before successor reservation | Resume orchestration decision only; never rerun task |
| Successor already recorded | Same ID is idempotent; different or second child fails deterministically |
| Repository or website-control identity changes | Stop before selection, claim, consume, dispatch, or completion |
| Requested/effective reasoning effort differs | Stop before claim; never silently downgrade |
| Lease expires | Diagnose; do not steal or reassign ownership automatically |
| Completion candidate | Build and validate immutable completion report; terminalize atomically; create no child |

Every state exposed by a crash must resolve to one deterministic command or an
explicit human-required disposition. Recovery never fabricates an external
effect, receipt, return, validator result, or completion proof.

## 11. Storage and migration strategy

### 11.1 Preferred new database

New recursive runs should use:

```text
.local/sys4ai/implementation-plan-relay/state.sqlite3
```

The existing goal-coupled database remains read-only for historical status,
export, and audit. This avoids rewriting `plans.outer_goal_id`, mixing two
writer semantics, or requiring cross-database atomicity with an outer goal that
no longer exists. It also supplies a clean rollback boundary and prevents new
runs from entering the old writer accidentally.

Neutral SQLite infrastructure must be shared rather than copied so locking,
backup, restore, canonical JSON, and hash behavior do not diverge.

### 11.2 Shared-database fallback

Use one physical database only if `DEC-005` records a concrete operational need.
The fallback must:

- add an additive migration such as
  `008_plan_native_discussion_relay.sql`;
- leave migrations 001 through 007 byte-identical;
- add an explicit orchestration-mode discriminator;
- make `outer_goal_id` optional only for the recursive writer profile;
- add plan-native relay-generation and repository-lease tables;
- preserve legacy rows and readers;
- prohibit simultaneous coordinator and recursive writes for one run.

The fallback has higher migration, foreign-key, and table-rebuild risk and is
not the default.

### 11.3 Prohibited migration actions

- no active-plan conversion mid-generation;
- no historical goal, plan, journal, receipt, event, lease, or intent rewrite;
- no placeholder outer goal for a new relay;
- no new-state dual write into generic-goal and relay tables;
- no completion inference from package or schema version alone;
- no deletion of old state after export;
- no topology change for an active legacy generation;
- no rollback that moves a consumed generation into another writer.

## 12. File and package impact map

### 12.1 Canonical `skills-Sys4AI`

| Surface | Planned change |
| --- | --- |
| `skills/implementation-plan-goal/` | Convert to compatibility launcher shim or supersede with `skills/implementation-plan-relay/`; update `SKILL.md`, `README.md`, `AGENTS.md`, `skill.yaml`, and agent metadata |
| `skills/continue-implementing-plan-task/` | Convert to compatibility frame shim or supersede with `skills/continue-implementation-plan-relay/`; remove coordinator return/wakeup semantics |
| `skills/agentjob-control/scripts/agentjob_runtime/plan/continuous.py` | Move coordinator implementation behind explicit legacy compatibility boundary |
| `skills/agentjob-control/scripts/agentjob_runtime/plan/relay.py` | Add plan-native launcher/frame orchestration and decision operations |
| `skills/agentjob-control/scripts/agentjob_runtime/plan/worker.py` | Remove coordinator wakeup; return canonical receipt; preserve consume-before-call and unknown quarantine |
| `skills/agentjob-control/scripts/agentjob_runtime/plan/sqlite_store.py` | Stop using generic goal store as new plan authority; add relay generations, leases, idempotent successor record, and atomic completion |
| `skills/agentjob-control/scripts/agentjob_runtime/plan/completion_report.py` | Generalize completion proof for plan terminology and plan-native fields |
| `skills/agentjob-control/scripts/agentjob_runtime/plan/recovery.py` | Add generation-bound typed recovery and dispatch reconciliation |
| `skills/agentjob-control/scripts/agentjob_runtime/adapters/` | Add or adapt fresh-discussion create/list/query provider; keep native Goal mirror-only |
| `skills/implementation-plan-relay/schemas/` or canonical equivalent | Add the eight versioned logical record contracts and semantic checks |
| `skills/agentjob-control/scripts/agentjob_runtime/goal/migrations/` | Do not modify historical bytes; add migration 008 only for the approved shared-database fallback |
| `scripts/skills/tests/` and focused skill tests | Add only the focused suites defined in Section 14 |
| registry, bundle, plugin, and generated catalog surfaces | Regenerate from canonical declarations after source validation; do not hand-edit derivatives |
| `implementation_plans/implementation-plan-goal-recommendations-phased-plan.md` | Preserve; add explicit supersession/context note if approved; do not rewrite historical task evidence |

The canonical package must remain reusable. It must use placeholders or
parameters rather than hard-coded AEther paths, private task IDs, local branch
names, or website-specific control records.

### 12.2 Website adaptation

| Surface | Planned change |
| --- | --- |
| `scripts/implementation_control/plan_goal_adapter.py` | Remove generic-goal activation/initialization from new relay activation; replace coordinator owner with launcher plus generation identities; add successor, finalization, and generation recovery operations |
| `scripts/implementation_control/continue_plan_goal.py` | Expose the new command surface; deprecate coordinator arguments; retain explicit legacy readers/mode |
| `.agents/implementation-plan-goal/adapter-config.json` or new relay config | Declare `recursive_chain_v1`, cardinalities, no persistent coordinator, provider mode, and degraded manual behavior |
| `.agents/skills/implementation-plan-goal/` | Replace only through normal installer with compatibility shim/new canonical package |
| `.agents/skills/continue-implementing-plan-task/` | Replace only through normal installer with compatibility shim/new canonical frame |
| `.agents/skills/agentjob-control/` | Replace only through dependency-resolved installation |
| plan-goal lock, registry, import provenance, and installer receipt | Regenerate/update from installed canonical release |
| `tests/test_plan_goal_adapter.py` and façade/installation tests | Adapt existing focused tests; do not create an unrelated broad suite |
| passive status output | Add chain/predecessor/successor/intent/lease/terminal report projection without scheduling authority |
| `implementation_control/` | Remain authoritative; change only through separately authorized website packet |

### 12.3 Required installed topology declaration

The approved installed config must express at least:

```json
{
  "relay_topology": "recursive_chain_v1",
  "launcher_successors": 1,
  "tasks_per_relay_frame": 1,
  "continue_invocations_per_relay_frame": 1,
  "agent_jobs_per_relay_frame": 1,
  "next_task_successors_per_relay_frame": 1,
  "same_task_successors": 0,
  "persistent_coordinator": false
}
```

If automatic Codex discussion creation is unavailable, the adapter must report
an explicitly selected degraded manual mode. It must not claim continuous
execution or synthesize provider evidence.

## 13. Phase dependency summary

| Phase | Purpose | Exit gate |
| --- | --- | --- |
| Phase 00 | Freeze new long-running use, audit history, and close current terminalization gap | Current state is understood; supported legacy terminalization exists or activation remains frozen |
| Phase 01 | Approve architecture, storage, provider, recovery, naming, and compatibility ADR | All `DEC-*` entries have an accepted disposition |
| Phase 02 | Define portable canonical skills, schemas, and compatibility boundaries | New package contracts and shims are review-complete |
| Phase 03 | Implement plan-native storage, migrations, CAS, leases, and legacy readers | State transitions are atomic and old records remain unchanged/readable |
| Phase 04 | Implement launcher, frame, receipt, terminalization, recovery, and CLI | One generation can execute safely without a coordinator |
| Phase 05 | Integrate fresh-discussion provider, exactly-once dispatch, minimal prompt, and status | External-create boundaries are recoverable and passive status is truthful |
| Phase 06 | Resolve Python runtime defect, run focused canonical checks, and create release candidate | Canonical release candidate is portable and internally consistent |
| Phase 07 | Install canonical bundle and adapt website façade/config/status | Website uses recursive writer by explicit mode while preserving control authority |
| Phase 08 | Run one disposable positive pilot and focused negative/rollback scenarios | Direct evidence proves topology, at-most-once behavior, and recovery |
| Phase 09 | Run one final gate, release/cut over, monitor, and retire legacy mutation after window | New writer is default; rollback and compatibility obligations are satisfied |

Phases are serial unless an accepted ADR explicitly proves two tasks cannot
touch the same state, schema, generated package, or compatibility surface.
No implementation task may silently perform a later phase's release effect.

## 14. Detailed phased implementation tasks

### Phase 00 — Control audit and terminalization stabilization

#### Phase objective

Prevent new work from depending on a known completion-path gap, preserve all
historical evidence, and establish a current baseline before architectural
changes begin.

#### Entry criteria

- Read-only access to current canonical, website, and state-store evidence.
- Authority to declare a temporary activation freeze or, if that authority is
  absent, to record the freeze as a required human gate.
- No assumption that the state observations in the source analysis are still
  current.

#### Phase exit gate

- Current plan, goal, receipt, intent, lease, and journal parity is recorded.
- Active, ambiguous, consumed-unknown, or unrecorded-child generations are
  named explicitly.
- The two historically observed terminalization events are preserved and their
  known provenance limitation is documented.
- A supported terminalization path exists for any future legacy run, or new
  long-running activation remains blocked.
- The redesign activation freeze remains in force through Phase 08; only the
  explicitly authorized disposable pilot may create a new relay before the
  Phase 09 cutover.

#### `RLY-00-01` — Freeze and capture the live control baseline

**Objective:** Prevent topology changes from overlapping an active or ambiguous
generation and capture the exact pre-redesign evidence set.

**Primary repository:** Website, read-only state inspection plus an authorized
control note if required.

**Dependencies:** None.

**Actions:**

1. Resolve the active website implementation-control task, job, handoff,
   completion, and approval state.
2. Resolve every stored implementation-plan run and project only: plan ID,
   mode/profile, plan revision, phase, generation, active task, outer goal if
   present, lease, unclosed provider intent, latest receipt, and journal head.
3. Identify any generation in reserved, child-ambiguous, claimed, consumed,
   invocation-unknown, receipt-pending, completion-candidate, or recovery state.
4. Compare SQLite records with adapter session state and provider records; do
   not repair during this task.
5. Record exact database paths, schema versions, file hashes, repository HEADs,
   and read-only backup hashes without copying secret token material.
6. Freeze new long-running activations through Phase 08. Permit only the
   explicitly authorized disposable pilot; do not resume production or legacy
   long-running activation merely because `RLY-00-03` closes. If the user or
   repository authority has not granted freeze authority, record an explicit
   human gate and stop.
7. Preserve unrelated dirty work and name it separately from relay evidence.

**Deliverables:**

- A dated baseline/audit record in the canonical implementation packet chosen
  for this task.
- A plan-run parity table and an ambiguity list.
- A recorded freeze disposition and its authority reference.

**Acceptance criteria:**

- No state mutation was performed during discovery.
- Every known run is classified as terminal, active, ambiguous, or corrupt with
  direct record references.
- No active or ambiguous generation is selected for topology conversion.
- Database and repository identities are sufficient to detect drift later.

**Minimal verification:** One read-only status/export command plus a manual
cross-check of record counts and hashes. Do not run runtime tests or aggregate
website validation.

**Protected stop:** Any active, consumed-unknown, or multiple-child generation
keeps the activation freeze in force and routes to an explicit recovery packet.

**Recommendation coverage:** `REC-015`, `REC-016`, `REC-096`.

#### `RLY-00-02` — Preserve and audit unexplained terminalization events

**Objective:** Document the missing writer provenance without rewriting the
events or inventing an explanation.

**Primary repository:** Website audit/control documentation; current database
remains unmodified unless an accepted packet authorizes an append-only note.

**Dependencies:** `RLY-00-01`.

**Actions:**

1. Locate every occurrence of the historically observed event names
   `plan_completion_candidate_confirmed` and
   `plan_terminal_completion_recorded` in live state, exports, backups, logs,
   and tracked history.
2. Record record IDs, plan IDs, generation, timestamps, journal predecessor and
   successor hashes, and surrounding event sequence.
3. Search current tracked code and reachable Git history for a writer using the
   exact event names and structurally equivalent terminalization mutations.
4. Distinguish: no tracked writer found, writer found but unversioned, writer
   found in generated/installed derivative only, or evidence insufficient.
5. Preserve the original bytes and append only a separate audit note. Do not
   rename, delete, normalize, or replay the events.
6. Record what the events can prove structurally and what they cannot prove
   about the missing writer or plan correctness.

**Deliverables:** Event-provenance audit note with hashes and an explicit
`known`, `unknown`, or `indeterminate` writer conclusion.

**Acceptance criteria:**

- Original event records and their journal ordering are unchanged.
- The note does not attribute authorship or authority without evidence.
- Any integrity break or hash mismatch is reported as a blocker rather than
  silently repaired.

**Minimal verification:** Hash comparison before and after the read-only audit;
no test suite.

**Protected stop:** Journal-chain mismatch, missing original bytes, or evidence
of concurrent mutation requires integrity review before `RLY-00-03`.

**Recommendation coverage:** `REC-015`, `REC-016`.

#### `RLY-00-03` — Add a supported legacy `finalize-plan` safety path

**Objective:** Close the current façade/provenance gap before another legacy
coordinator-mode plan depends on terminalization.

**Primary repository:** Website adapter, narrowly scoped. If canonical reusable
logic must change, split that work into a separately authorized canonical task.

**Dependencies:** `RLY-00-01`, `RLY-00-02`.

**Actions:**

1. Specify the immutable legacy completion report using the current plan
   schema, task receipts, validators, repository/control fingerprints, open
   intents, and lease state.
2. Add a first-class CLI/facade command named `finalize-plan` or a documented
   equivalent; do not synthesize the historical unexplained events.
3. Require expected plan revision, expected website-control hash, current
   holder identity, and the completion-report hash.
4. Reuse the current canonical completion-proof logic only where its inputs and
   semantics match the installed profile.
5. In one transaction, validate completion, append a new tracked event and
   immutable receipt, mark terminal, and release the lease.
6. Reject missing task receipts, unresolved dependencies, open/ambiguous
   provider intent, active invocation, validator failure, hash drift, or lease
   mismatch.
7. Document that this is a safety repair for legacy mode, not the recursive
   architecture implementation.

**Deliverables:** Supported command, minimal completion-report contract,
append-only event/receipt writer, and operator usage note.

**Acceptance criteria:**

- A completion candidate cannot become terminal through an untracked manual
  mutation.
- Terminalization and lease release are atomic.
- Repeating the same finalized request is idempotent or returns a deterministic
  already-terminal result.
- A mismatched report, revision, or control fingerprint fails closed.

**Minimal verification:** Add or adapt only the focused existing adapter tests
for successful finalization, incomplete proof rejection, and duplicate call.
Run `npm run test:plan-goal` once for this packet; do not run the full website
gate unless required by the live packet.

**Rollback:** Disable the new command without removing its append-only records.
Do not revert a successfully written terminal receipt independently of state.
The broader redesign activation freeze remains in force after this safety repair.

**Recommendation coverage:** `REC-017` through `REC-020`, `REC-080`.

### Phase 01 — Architecture, migration, and compatibility decisions

#### Phase objective

Approve one architecture decision record and one migration plan that freeze the
topology, names, state authority, provider contract, recovery rules, human
gates, storage choice, and compatibility window before runtime editing begins.

#### Entry criteria

- Phase 00 exit gate is satisfied.
- Current canonical and website code is re-read at implementation-time HEAD.
- Decision authority for both canonical reusable packages and website
  adaptation is identified.

#### Phase exit gate

- `DEC-001` through `DEC-014` are accepted, rejected with replacements, or
  explicitly human-gated.
- The accepted record defines exact version/profile identifiers and rollback
  boundaries.
- The existing canonical coordinator implementation and large historical
  phased plan have an explicit legacy/supersession disposition.

#### `RLY-01-01` — Approve topology, ownership, names, and authority ADR

**Objective:** Freeze the recursive-chain architecture and its separation of
orchestration, task execution, provider transport, website control, status, and
optional UI mirroring.

**Primary repository:** Canonical `skills-Sys4AI` documentation/ADR location.

**Dependencies:** Phase 00.

**Actions:**

1. Diagram and compare the current coordinator star, canonical `0.2.0`
   continuous coordinator, upstream research relay ownership, and proposed
   plan-native recursive chain.
2. Approve `recursive_chain_v1` as the new writer topology or record a concrete
   alternative that still meets every invariant in Section 6.
3. Define launcher, relay-frame, executor, plan-store, provider, website
   control, passive status, native mirror, and human-review responsibilities.
4. Freeze the rule that scheduling a successor is allowed but executing its
   task is not.
5. Approve the preferred public and internal skill names and the two deprecated
   compatibility shims.
6. State explicitly that new runs use no native Codex Goal and no generic outer
   goal as orchestration authority.
7. Freeze all cardinality, predecessor-chain, identity, evidence, and
   protected-stop invariants.
8. State that current `0.2.0` is legacy-compatible context, not the final target
   design.
9. Define how the pre-existing canonical phased plan is preserved and marked
   superseded without altering its historical task evidence.

**Deliverables:** Accepted ADR with decision, context, alternatives,
consequences, invariants, status terminology, and supersession references.

**Acceptance criteria:**

- No component has overlapping or implicit scheduling authority.
- Native Goal state and provider state are explicitly non-authoritative.
- One-task/one-successor semantics are unambiguous.
- Every rejected architecture in Section 17 has a recorded reason.

**Minimal verification:** Human review against Sections 5, 6, and the
recommendation ledger; no runtime tests.

**Recommendation coverage:** `REC-001` through `REC-014`, `REC-021` through
`REC-042`, `REC-097`, `REC-115` through `REC-122`.

#### `RLY-01-02` — Approve the state model and storage migration plan

**Objective:** Choose the new-database default or explicitly justify the
shared-database fallback and freeze the eight record contracts.

**Primary repository:** Canonical ADR/migration documentation.

**Dependencies:** `RLY-01-01`.

**Actions:**

1. Inventory current schema versions, migrations, foreign keys, backup/restore,
   locks, generic goal coupling, plan tables, and installed-state paths.
2. Approve the preferred new database and read-only legacy database behavior.
3. If the shared fallback is chosen, document migration 008, table rebuilds,
   nullability, mode discriminator, foreign-key checks, and why the extra risk
   is necessary.
4. Freeze logical schemas for `PlanRelayRun`, `PlanRelayGeneration`,
   `PlanTaskEnvelope v3`, `PlanTaskReceipt v3`, `PlanDispatchIntent v3`,
   `PlanRelayLease`, `PlanCompletionReport`, and `CodexGoalMirror`.
5. Define immutable fields, mutable state, CAS revision ownership, journal
   linking, canonical serialization, and hash rules.
6. Enumerate new-writer exclusions and neutral utility extraction boundaries.
7. Define legacy read/export behavior, exact backup restoration, and rollback
   without state conversion.
8. State all prohibited migration actions from Section 11.3.

**Deliverables:** Accepted migration plan, schema map, table/record ownership
map, rollback protocol, and legacy compatibility contract.

**Acceptance criteria:**

- There is exactly one writer model for a new run.
- Historical migration bytes and legacy rows remain immutable.
- No cross-database transaction with an outer goal is needed in the preferred
  design.
- Every active/consumed-state rollback case has a safe stop rather than a
  topology conversion.

**Minimal verification:** Read-only schema introspection and design review; no
migration execution.

**Recommendation coverage:** `REC-043` through `REC-056`, `REC-086`,
`REC-093` through `REC-095`.

#### `RLY-01-03` — Approve provider, lease, recovery, and human-gate contracts

**Objective:** Freeze the external effect boundary and deterministic recovery
rules before implementation.

**Primary repository:** Canonical ADR/provider contract and recovery matrix.

**Dependencies:** `RLY-01-01`, `RLY-01-02`.

**Actions:**

1. Specify provider capabilities for create, read, list/query by idempotency
   evidence, current-thread identity, same-project evidence, bound-checkout
   evidence, and requested/effective reasoning effort.
2. Explicitly remove `wait_for_terminal` and `resume_thread` as normal runtime
   requirements.
3. Define dispatch intent, create budget, attempt counter, response hash, and
   child-adoption semantics.
4. Freeze token generation, token-hash storage, raw-token redaction, and current
   thread proof.
5. Define one repository mutation lease, its transfers, diagnostic expiry, and
   prohibition on automatic takeover.
6. Walk every row of the recovery matrix and name the command, required proof,
   allowed mutation, and terminal/protected result.
7. Define human gates for multiple/uncertain child, missing capability,
   authority absence, integrity mismatch, explicit cancellation, and any state
   with no deterministic safe recovery.
8. Define degraded manual transport explicitly; it must not claim automatic
   continuity.

**Deliverables:** Provider protocol, lease protocol, recovery command matrix,
human-necessity rules, and capability/degraded-mode declaration.

**Acceptance criteria:**

- No ambiguous create path authorizes a blind retry.
- No consumed task path authorizes an automatic rerun.
- Provider and native Goal state cannot select or complete a plan.
- Every human gate names the missing authority/evidence and creates no child.

**Minimal verification:** Contract review with one worked trace for successful
create, ambiguous create, and crash-after-consume; no executable tests yet.

**Recommendation coverage:** `REC-057` through `REC-080`, `REC-099`.

#### `RLY-01-04` — Approve compatibility, release, and retirement policy

**Objective:** Define canonical-first delivery, installed-copy provenance,
legacy read/write limits, and coordinator retirement gates.

**Primary repository:** Canonical release/compatibility ADR with website
adaptation reference.

**Dependencies:** `RLY-01-01` through `RLY-01-03`.

**Actions:**

1. Approve the canonical-source-first sequence and prohibit primary fixes in
   installed copies or generated plugins.
2. Define compatibility shims, warning text, supported legacy readers, and
   explicit legacy-mode commands.
3. Define the compatibility window in versions or time plus evidence required
   before coordinator mutation commands are removed.
4. Freeze version/profile negotiation so new writers refuse legacy coordinator
   records and legacy writers refuse recursive records.
5. Define canonical package versioning, registry/bundle/plugin regeneration,
   website installer input, lock/import-provenance/receipt updates, and rollback.
6. State that release or plan completion does not authorize push, deployment,
   publication, or upstream mutation.
7. Preserve current `0.2.0` only as explicit legacy mode during the approved
   window; do not present it as the redesign.

**Deliverables:** Compatibility matrix, deprecation schedule, release sequence,
installed provenance checklist, and rollback ownership.

**Acceptance criteria:**

- A new writer cannot silently enter coordinator mode.
- Installed sources can be traced to one canonical release and installer
  receipt.
- Retirement is evidence-gated, not date-only.
- Legacy audit access survives retirement of mutation commands.

**Minimal verification:** Documentation consistency review; no package build.

**Recommendation coverage:** `REC-004`, `REC-005`, `REC-036`, `REC-037`,
`REC-074`, `REC-091`, `REC-092`, `REC-103`, `REC-116` through `REC-120`.

### Phase 02 — Canonical skills, contracts, and compatibility boundaries

#### Phase objective

Create portable canonical launcher/frame packages, versioned schemas, and thin
legacy shims without yet adapting the website's installed copies.

#### Entry criteria

- Phase 01 ADR and migration plan accepted.
- Canonical repository task authority identifies exact write paths.
- Package names and version/profile identifiers are frozen.

#### Phase exit gate

- Launcher and frame instructions express recursive ownership exactly.
- Eight record schemas and semantic cross-record rules exist.
- Compatibility shims route to the new implementation and disclaim native Goal
  and coordinator authority.
- Canonical source remains project-agnostic and generated derivatives have not
  been hand-edited.

#### `RLY-02-01` — Create the canonical launcher package

**Objective:** Implement `implementation-plan-relay` as a zero-AgentJob,
generation-1-only launcher.

**Target files:** New canonical skill folder with `SKILL.md`, `README.md`,
`AGENTS.md`, `skill.yaml`, agent metadata, and only necessary templates or
examples.

**Dependencies:** Phase 01.

**Actions:**

1. Define purpose, trigger conditions, inputs, outputs, exact acceptance gate,
   plan/repository/profile identities, and stop conditions.
2. State explicitly that the launcher creates no native Codex Goal and no
   generic outer goal.
3. Encode the launcher transaction from Section 8.1.
4. Limit the launcher to zero AgentJobs, one generation-1 reservation, one
   provider create budget, one recorded successor, and immediate stop.
5. Route ambiguity to `reconcile-dispatch`, not automatic create retry.
6. Use project placeholders and adapter contracts rather than AEther-specific
   paths or private identifiers.
7. Document degraded manual transport truthfully.
8. Add adaptation and provenance sections consistent with canonical repository
   policy.

**Deliverables:** Complete reusable launcher skill package.

**Acceptance criteria:**

- Instructions cannot be read as a persistent coordinator loop.
- No step authorizes the launcher to execute a task.
- Required identities and protected stops are explicit.
- Direct installation policy and dependency requirements are declared.

**Minimal verification:** Manifest/schema lint and manual builder/refuter review
of the skill text; no runtime suite.

**Recommendation coverage:** `REC-036`, `REC-081`, `REC-087`.

#### `RLY-02-02` — Create the canonical recursive frame package

**Objective:** Implement `continue-implementation-plan-relay` as the internal
one-generation worker/relay skill.

**Target files:** New canonical frame folder with `SKILL.md`, `README.md`,
`AGENTS.md`, `skill.yaml`, agent metadata, and minimal handoff template.

**Dependencies:** `RLY-02-01`.

**Actions:**

1. Encode immutable envelope validation, predecessor handoff wait, atomic
   claim, consume-before-call, one `continue`, and return/unknown recording.
2. Require live repository and project-control reinspection after the task.
3. Define the six allowed decisions: plan complete, safe next task, bounded
   repair/replan, genuine human gate, integrity/capability stop, or explicit
   cancellation.
4. Permit at most one distinct next-task successor and continue forbidding
   same-task automatic successors.
5. Separate task execution from post-receipt orchestration in wording and
   examples.
6. Require the frame to stop immediately after terminalization, protected
   stop, cancellation, or successor recording.
7. Use the minimal successor prompt and raw-token handling rules.
8. State that worker prose is telemetry and that receipts/canonical evidence
   establish completion.

**Deliverables:** Complete reusable recursive-frame skill package.

**Acceptance criteria:**

- One task per discussion is mechanically and linguistically unambiguous.
- The frame owns N-to-N+1 scheduling without waking a coordinator.
- Unknown consumed work creates no child and no retry.
- All decision branches end in one bounded state mutation sequence.

**Minimal verification:** Manifest/schema lint and manual instruction trace for
one success and one consumed-unknown case.

**Recommendation coverage:** `REC-037` through `REC-042`, `REC-082`,
`REC-087`.

#### `RLY-02-03` — Define schemas, templates, and semantic checks

**Objective:** Make every plan-native record independently validatable and
cross-record consistent.

**Target files:** Canonical schema, template, example, and semantic-validation
surfaces approved by the ADR.

**Dependencies:** `RLY-02-01`, `RLY-02-02`.

**Actions:**

1. Create versioned schemas for all eight logical records in Section 7.
2. Define canonical JSON, unknown-field, enum, identifier, hash, timestamp,
   token-hash, and reason-code rules.
3. Encode cardinality and topology fields in envelopes, receipts, run state,
   and generations rather than relying on prose alone.
4. Encode predecessor rules, current-thread equality, one active generation,
   one create budget, one receipt, and no same-task successor.
5. Cross-check plan/task/revision/repository/control/profile/topology/intent/
   receipt identities.
6. Encode terminal-report completeness and prohibition on treating no-ready-task
   as completion.
7. Add minimal positive examples for launch, one nonterminal frame, terminal
   completion, human gate, and invocation unknown.
8. Add only negative fixtures necessary to prove the high-risk cross-record
   invariants; consolidate related invalid cases in a table-driven fixture.

**Deliverables:** Versioned schemas, templates/examples, and one semantic
checker entry point.

**Acceptance criteria:**

- All mutable versus immutable fields are explicit.
- Token secrets are not allowed in durable record schemas.
- Each cross-record mismatch produces a stable reason code.
- New schemas do not modify legacy schema bytes.

**Minimal verification:** Focused schema/semantic fixture command only.

**Recommendation coverage:** `REC-021` through `REC-035`, `REC-045` through
`REC-052`, `REC-104` through `REC-106`.

#### `RLY-02-04` — Implement compatibility shims and remove default coordinator semantics

**Objective:** Preserve old entry names while making the recursive writer the
only new default path.

**Target files:** Existing canonical launcher/frame packages, manifests,
compatibility maps, and `plan/continuous.py` legacy boundary.

**Dependencies:** `RLY-02-01` through `RLY-02-03`.

**Actions:**

1. Convert `implementation-plan-goal` into a thin deprecated shim that invokes
   `implementation-plan-relay` and states that it does not create or depend on
   a native Codex Goal.
2. Convert `continue-implementing-plan-task` into a thin deprecated shim that
   invokes the new recursive frame.
3. Preserve coordinator implementation only in an explicit legacy module or
   profile; remove default-path calls to `run_to_goal`, `notify_coordinator`,
   and `answer_and_resume`.
4. Remove new-profile requirements for wait/resume provider capabilities.
5. Use plan-complete terminology instead of `goal_reached` in new profiles.
6. Make profile negotiation fail closed on cross-topology reads or writes.
7. Update human-facing README and deprecation guidance without editing
   generated plugin copies.

**Deliverables:** Two compatibility shims, explicit legacy boundary, updated
profile negotiation, and deprecation documentation.

**Acceptance criteria:**

- Old names reach the recursive implementation for new accepted runs.
- Coordinator mode requires an explicit legacy selector.
- No new writer imports generic-goal activation, initialization, or mutation.
- Legacy records remain readable under their original profile.

**Minimal verification:** Static import/profile check and one shim resolution
test; no end-to-end run.

**Recommendation coverage:** `REC-036`, `REC-037`, `REC-053` through
`REC-056`, `REC-083`, `REC-086`, `REC-091`.

### Phase 03 — Plan-native SQLite state, CAS, leases, and legacy readers

#### Phase objective

Implement durable plan-native state with atomic generation ownership and
completion, while preserving legacy auditability and avoiding copied storage
logic.

#### Entry criteria

- Phase 02 contracts are review-complete.
- `DEC-004` or `DEC-005` selects the physical database strategy.
- A backup/restore location and test fixture are authorized.

#### Phase exit gate

- New runs can initialize without generic goal state.
- One active generation and one repository mutation owner are enforced.
- All plan-native mutations are CAS-bound and journaled.
- Legacy records are readable and byte-preserved.
- Backup/restore returns the exact pre-migration state.

#### `RLY-03-01` — Extract neutral canonical state utilities

**Objective:** Remove the reason plan runtime must import generic-goal modules
for non-goal-specific infrastructure.

**Target files:** Neutral canonical JSON, hashing, time, SQLite, locking, backup,
and error namespaces selected by the ADR.

**Dependencies:** Phase 02.

**Actions:**

1. Inventory every plan import from `agentjob_runtime.goal.*` and classify it
   as goal-specific or reusable infrastructure.
2. Move or wrap only reusable logic in neutral namespaces.
3. Preserve canonical bytes, hash outputs, timestamp parsing, transaction
   isolation, busy handling, backup behavior, and error reason codes.
4. Update plan and generic-goal callers deliberately; do not create circular
   compatibility imports.
5. Leave goal-specific activation, initialization, goal lease, and mutation
   semantics in the goal namespace.

**Deliverables:** Neutral utility surface and import map.

**Acceptance criteria:**

- Plan-native code can use shared infrastructure without constructing or
  mutating a goal.
- Existing generic-goal behavior remains unchanged.
- No duplicate canonicalization or lock implementation is introduced.

**Minimal verification:** Existing focused utility tests plus hash parity on a
small fixture set.

**Recommendation coverage:** `REC-002`, `REC-055`, `REC-056`, `REC-087`.

#### `RLY-03-02` — Implement the selected database and additive schema

**Objective:** Create the physical persistence model for plan-native runs.

**Target files:** New database bootstrap/migrations or approved migration 008,
schema constants, backup/restore code, and schema documentation.

**Dependencies:** `RLY-03-01`.

**Actions:**

1. For the preferred design, create the new database path and initialize only
   relay-native tables, metadata, and journal structures.
2. For the fallback, add migration 008 without changing migrations 001–007 and
   implement the approved orchestration-mode discriminator.
3. Add uniqueness constraints for relay ID/generation, one active generation,
   idempotency key, successor identity, one repository mutation lease, and one
   completion report.
4. Store only token hashes; keep provider response content out of canonical
   state except the approved response hash and non-sensitive identity fields.
5. Add foreign keys and check constraints for plan/generation/intent/receipt/
   completion relationships.
6. Implement backup-before-migration and exact restore.
7. Prohibit opening a recursive database with a legacy writer and vice versa.

**Deliverables:** Physical schema, migration/bootstrap, schema versioning, and
backup/restore path.

**Acceptance criteria:**

- Fresh recursive state contains no generic outer-goal row.
- Database constraints enforce core uniqueness independent of application
  prose.
- Historical migration hashes remain unchanged.
- Interrupted migration restores exact prior bytes or a documented SQLite-
  equivalent state with matching exported canonical hashes.

**Minimal verification:** One fresh-database fixture, one migration/restore
fixture if fallback is chosen, and schema integrity check.

**Recommendation coverage:** `REC-043` through `REC-052`, `REC-086`,
`REC-093` through `REC-095`.

#### `RLY-03-03` — Implement store mutations, CAS, leases, and journal integrity

**Objective:** Provide small atomic operations for every authoritative local
transition.

**Target files:** Plan relay store/model/lifecycle and journal modules.

**Dependencies:** `RLY-03-02`.

**Actions:**

1. Implement initialize run, reserve generation, record successor, claim,
   consume, record returned, record unknown, finalize receipt, reserve next,
   record protected stop, cancel, and finalize plan.
2. Require expected plan revision and the applicable expected hashes for every
   mutation.
3. Implement the one-repository-owner lease and explicit transfers from
   launcher to reserved successor to claimed worker to successor-reserved or
   terminal release.
4. Make lease expiry diagnostic and require direct same-thread/adoption proof
   for recovery.
5. Append canonical journal events with previous-head linkage and mutation
   result hashes.
6. Make `record-successor` idempotent for the same child and conflicting for a
   different child.
7. Make terminalization, completion receipt, final journal entry, and lease
   release atomic.
8. Return structured reason codes and current canonical revision on conflicts.

**Deliverables:** Transactional store API with mutation contracts and journal
events.

**Acceptance criteria:**

- Competing claims and consumes have one winner.
- No mutation succeeds against stale plan/repository/control/profile/topology
  evidence.
- One active generation and one repository owner are enforced.
- Terminal or protected states cannot reserve a child.
- Journal replay detects missing, reordered, or altered entries.

**Minimal verification:** One focused parameterized state-transition suite;
do not run the entire canonical repository suite yet.

**Recommendation coverage:** `REC-002`, `REC-006`, `REC-021` through
`REC-035`, `REC-050`, `REC-053` through `REC-056`, `REC-105`.

#### `RLY-03-04` — Add legacy readers, export/import, and rollback projection

**Objective:** Preserve audit and compatibility without allowing new writers to
mutate legacy coordinator state.

**Target files:** Compatibility readers, export/import, status projection, and
rollback documentation.

**Dependencies:** `RLY-03-02`, `RLY-03-03`.

**Actions:**

1. Read legacy schema 3–7 records as applicable without normalizing or rewriting
   them.
2. Label each projected run with its writer profile and topology.
3. Refuse recursive mutations against legacy coordinator rows and legacy
   mutations against recursive rows.
4. Export canonical hashes, activation evidence, journal heads, intents,
   receipts, and completion state without exposing raw tokens.
5. Import only into a compatible empty/audit destination and verify all hashes
   before marking the import readable.
6. Demonstrate backup restore and rollback projection without converting an
   active or consumed generation.
7. Keep old state after successful export.

**Deliverables:** Read-only legacy projection, export/import contract, exact
restore evidence, and rollback guide.

**Acceptance criteria:**

- Legacy rows are byte-identical after every read/export operation.
- Export/import preserves canonical hashes and activation evidence.
- No active legacy generation can change topology in place.
- Rollback never deletes new or old evidence.

**Minimal verification:** One representative fixture per supported legacy
schema family plus one export/import hash comparison.

**Recommendation coverage:** `REC-094`, `REC-095`, `REC-108`.

### Phase 04 — Launcher, recursive frame, terminalization, recovery, and CLI

#### Phase objective

Implement one complete generation lifecycle over the plan-native store without
a coordinator, then expose each recovery-safe boundary through the command
surface.

#### Entry criteria

- Phase 03 store API and schemas are stable.
- Thread creation remains mocked or disabled until Phase 05.
- The deterministic scheduler and existing plan normalization rules have an
  explicit reuse decision.

#### Phase exit gate

- A launcher can reserve one first generation and stop.
- A frame can claim, consume, call one mock executor, finalize one receipt, and
  select a terminal/protected/successor outcome.
- `finalize-plan` produces an atomic terminal result.
- Typed recovery commands cover every local state boundary.
- No default call path imports goal activation or wakes a coordinator.

#### `RLY-04-01` — Implement the zero-AgentJob launcher

**Objective:** Convert accepted plan input into one committed generation-1
dispatch intent and no task execution.

**Target files:** Canonical plan launcher/relay module and launcher CLI handler.

**Dependencies:** Phase 03.

**Actions:**

1. Reuse current source classification, normalization, canonical-plan hashing,
   authority, profile, repository topology, and deterministic scheduler logic
   where it remains semantically valid.
2. Validate exact combined acceptance and invalidate it on goal/objective,
   plan, repository, current-thread, requested/effective effort, topology, or
   protected-effect change.
3. Initialize `PlanRelayRun` directly without goal activation or
   `initialize_goal()`.
4. Select the first dependency-ready task and persist a revision-bound
   selection proof.
5. Generate one opaque token, persist its hash, reserve generation 1, and
   insert a dispatch intent with create budget one.
6. Return an external-action instruction/receipt to the skill or provider
   boundary; do not call Codex inside the store helper.
7. Stop with exact counts: zero AgentJobs, zero task invocations, zero or one
   provider create after Phase 05, and zero or one successor.

**Deliverables:** Plan-native launcher function, structured launch result, and
CLI command.

**Acceptance criteria:**

- New launch creates no generic goal row or coordinator state.
- Deterministic selection is revision-bound and independently reproducible.
- A stale acceptance or identity fails before initialization/reservation.
- Launcher cannot execute a task or select generation 2.

**Minimal verification:** Focused launcher tests for success, stale acceptance,
no-ready-not-complete, and zero-AgentJob cardinality.

**Recommendation coverage:** `REC-013`, `REC-057` through `REC-060`,
`REC-069`, `REC-081`, `REC-104`.

#### `RLY-04-02` — Implement relay entry, claim, and consume

**Objective:** Prove the current discussion owns exactly one reserved
generation before any task effect.

**Target files:** Canonical relay/frame runtime and CLI handlers.

**Dependencies:** `RLY-04-01`.

**Actions:**

1. Resolve relay state from the minimal envelope and verify canonical state
   location.
2. Validate all plan/task/generation/token/idempotency/repository/control/
   profile/topology/predecessor/current-thread fields.
3. Read-only wait for the predecessor to record `successor_created`, bounded by
   the accepted envelope policy.
4. Claim via CAS and reject stale, duplicate, mismatched, already consumed, or
   concurrently owned generations.
5. Reinspect website control and repository identities immediately before
   consumption.
6. Compile the immutable task-local invocation without selecting another task.
7. Consume via CAS immediately before yielding the one call authorization.
8. Ensure no automatic adoption follows lease expiry.

**Deliverables:** `claim-generation` and `consume-generation` runtime/CLI
operations with structured receipts.

**Acceptance criteria:**

- Two claimants yield one winner and one deterministic conflict.
- A child cannot claim before its recorded predecessor handoff.
- Current-thread, profile, effort, and repository mismatch fail before consume.
- Duplicate consume and second-task compilation fail.

**Minimal verification:** Focused contention/identity tests in the plan-store
suite; no provider or website aggregate gate.

**Recommendation coverage:** `REC-038`, `REC-061`, `REC-070`, `REC-075`
through `REC-079`, `REC-104` through `REC-106`.

#### `RLY-04-03` — Implement one task call and immutable task receipt

**Objective:** Bind one consumed generation to at most one direct `continue`
call and one evidence-based receipt.

**Target files:** Canonical worker/executor integration, receipt builder, and
verification adapter.

**Dependencies:** `RLY-04-02`.

**Actions:**

1. Remove worker-to-coordinator wakeup and coordinator provider arguments from
   the new profile.
2. Accept the consumed invocation authorization and call `continue` at most
   once.
3. Record direct return proof as `returned`; do not treat an exception or lost
   boundary as a return.
4. Record uncertain call/return as `unknown`, quarantine, and create no child.
5. Reinspect actual repository, website control, task completion, validation,
   checkpoint, and protected-effect evidence.
6. Construct `PlanTaskReceipt v3` with exact continue, AgentJob, provider, and
   successor counts; changed paths; fingerprints; validators; disposition;
   uncertainty; and receipt hash.
7. Refuse a receipt that relies only on prose or omits required task validators.
8. Return the canonical receipt to the relay frame without scheduling inside
   the executor.

**Deliverables:** New-profile worker call boundary, returned/unknown operations,
and immutable receipt builder.

**Acceptance criteria:**

- A worker can execute no more than one task and one `continue` call.
- Unknown consumed work is permanent until direct reconciliation evidence
  exists and is never rerun automatically.
- Receipt counts and identity hashes are internally consistent.
- Coordinator wakeup and resumption do not occur in the new profile.

**Minimal verification:** Focused tests for direct return, unknown boundary,
duplicate call refusal, and prose-without-evidence rejection.

**Recommendation coverage:** `REC-039`, `REC-040`, `REC-062` through
`REC-064`, `REC-084`, `REC-106`.

#### `RLY-04-04` — Implement atomic post-task decision and plan finalization

**Objective:** Convert one verified receipt into exactly one terminal,
successor-reserved, or protected outcome.

**Target files:** Canonical relay decision, scheduler integration, completion
report, and store transaction.

**Dependencies:** `RLY-04-03`.

**Actions:**

1. Validate and finalize the immutable receipt in a CAS transaction.
2. Update effective task and phase status, including accepted amendment or
   task-supersession state.
3. Recompute the dependency graph and deterministically select the first ready
   task.
4. Distinguish selected task, safe bounded replan, human gate, integrity/
   capability stop, explicit cancellation, no-ready-blocked, and completion
   candidate.
5. For continuation, reserve N+1 with N's worker as predecessor, transfer the
   lease, and insert one dispatch intent.
6. For protected outcomes, append the disposition and release/retain the lease
   exactly as the accepted recovery policy specifies; create no child.
7. For completion, build `PlanCompletionReport`, prove every effective task
   terminal, prove no open intent, atomically write terminal receipt/state and
   release the lease.
8. Make a repeated identical finalization idempotent and a conflicting report
   deterministic failure.

**Deliverables:** `verify-and-decide`, `reserve-successor`, and `finalize-plan`
runtime operations.

**Acceptance criteria:**

- A finalized task is never rerun to resume orchestration.
- N+1 always names N's worker and one receipt hash.
- Terminal and protected frames create zero successors.
- Missing ready task alone cannot produce terminal completion.
- Terminal report, state, journal, and lease release are atomic.

**Minimal verification:** Focused decision-table tests for the six allowed
dispositions and terminal proof rejection.

**Recommendation coverage:** `REC-017` through `REC-020`, `REC-041`,
`REC-042`, `REC-065` through `REC-068`, `REC-080`, `REC-085`,
`REC-104` through `REC-106`.

#### `RLY-04-05` — Implement typed recovery and complete CLI surface

**Objective:** Expose every deterministic recovery without requiring direct
database edits or coordinator ownership.

**Target files:** Canonical recovery module, CLI parser/handlers, reason-code
catalog, and operator reference.

**Dependencies:** `RLY-04-01` through `RLY-04-04`.

**Actions:**

1. Implement all commands in Section 9 with explicit expected-revision and
   identity inputs.
2. Bind every recovery to one relay and generation; remove coordinator-only
   recovery from the new profile.
3. Implement `record-successor`, `reconcile-dispatch`,
   `abandon-unconsumed`, `reconcile-consumed`, `summarize`, and `cancel`.
4. Distinguish external create not attempted, concrete child returned,
   ambiguous, zero-child-proven, one-child-adoptable, and multi/uncertain-child
   results.
5. Require same-thread or explicit adoption proof after claim-before-consume
   crash.
6. Permit orchestration-decision resume after finalized receipt without task
   rerun.
7. Produce stable machine-readable status, reason code, execution count,
   provider count, next safe command, and human-gate fields.
8. Keep legacy commands read-only or behind the explicit legacy selector.

**Deliverables:** Complete crash-auditable CLI and recovery reference.

**Acceptance criteria:**

- Every recovery matrix row maps to exactly one command or explicit human gate.
- No command hides an unreported provider create.
- No command can steal an expired lease or rerun consumed work.
- `summarize` is strictly read-only.

**Minimal verification:** One parameterized CLI contract test over command
parsing, CAS mismatch, and recovery disposition; no full integration pilot yet.

**Recommendation coverage:** `REC-069` through `REC-080`, `REC-089`.

### Phase 05 — Fresh-discussion provider, dispatch reconciliation, and passive status

#### Phase objective

Integrate the external thread capability without giving it scheduling authority
and make its exactly-once uncertainty inspectable and recoverable.

#### Entry criteria

- Phase 04 works with a deterministic fake provider.
- The actual provider capability is identified and approved.
- Same-project, checkout binding, and reasoning-effort evidence can be obtained
  or the system is explicitly placed in degraded manual mode.

#### Phase exit gate

- One committed intent authorizes at most one create.
- Returned child identity and capability evidence are recorded separately from
  the intent transaction.
- Ambiguity can be queried by idempotency evidence without blind retry.
- Successor prompts are minimal and token-safe.
- Status and optional Goal mirror are passive projections.

#### `RLY-05-01` — Implement the provider capability contract

**Objective:** Create fresh discussions in the correct project/checkout with
explicit reasoning effort and verifiable identity.

**Target files:** Canonical thread provider protocol and Codex app/server or
automatic provider adapter.

**Dependencies:** Phase 04.

**Actions:**

1. Declare provider capabilities for create, get/read, list/query, current
   thread, project identity, checkout/repository binding, and requested/
   effective effort.
2. Require explicit requested effort and fail when effective effort differs.
3. Require the child to be created in the same saved project and bound checkout
   unless a separately authorized topology change says otherwise.
4. Accept an idempotency key and return concrete thread ID plus non-sensitive
   response evidence.
5. Support read-only query/list evidence sufficient to classify zero, one,
   multiple, or uncertain matching children.
6. Do not require or expose coordinator `wait_for_terminal` or `resume_thread`
   for the recursive profile.
7. Describe degraded manual capability separately and truthfully.

**Deliverables:** Provider protocol, concrete adapter, capability report, and
degraded-mode adapter or disposition.

**Acceptance criteria:**

- Provider cannot select a task, mutate plan state, authorize retry, or mark
  completion.
- Profile/project/checkout mismatches fail before claim.
- Missing query capability turns ambiguous create into a human gate, not retry.

**Minimal verification:** Contract test with a fake provider and one read-only
capability probe; do not create a production discussion.

**Recommendation coverage:** `REC-008`, `REC-057` through `REC-061`,
`REC-099`.

#### `RLY-05-02` — Implement intent/create/record and ambiguity reconciliation

**Objective:** Make the non-atomic external create safe under every returned,
failed, lost, or duplicate outcome.

**Target files:** Relay dispatch orchestrator, provider intent mutation, and
recovery integration.

**Dependencies:** `RLY-05-01`.

**Actions:**

1. Require a committed intent with create budget one before provider create.
2. Record the create attempt boundary without increasing authorization beyond
   one external call.
3. On concrete return, hash the response and call `record-successor`; if the
   record transaction fails, retain the concrete ID for record-only recovery.
4. On ambiguous result, mark the intent ambiguous and query by idempotency key.
5. Adopt exactly one matching unclaimed child only after identity, predecessor,
   profile, and checkout checks.
6. Record definitive zero-child failure before recovery policy creates any
   replacement generation.
7. Quarantine multiple or uncertain children for human reconciliation.
8. Reject a second provider create or a different child record for the same
   generation.

**Deliverables:** Exactly-once dispatch orchestrator and reconciliation path.

**Acceptance criteria:**

- Create-return/record-failure never produces a second create.
- Same child record is idempotent; different child conflicts.
- Every ambiguous outcome is visible in status with its next safe action.
- External provider evidence never overrides canonical state checks.

**Minimal verification:** Focused parameterized provider suite for returned,
failed-before-create, returned-record-failed, ambiguous-zero, ambiguous-one,
ambiguous-many, and duplicate invocation.

**Recommendation coverage:** `REC-049`, `REC-059`, `REC-067`, `REC-075`
through `REC-080`, `REC-107`.

#### `RLY-05-03` — Implement minimal successor prompt and secure token handling

**Objective:** Reduce prompt drift and keep routing authority in canonical
state.

**Target files:** Canonical prompt builder, envelope renderer, and redaction
helpers.

**Dependencies:** `RLY-05-02`.

**Actions:**

1. Render only the fields in Section 8.6 plus the selected canonical skill
   invocation.
2. Keep task instructions, mutable status, dependency graph, and completion
   claims out of the prompt; the frame loads them from verified state.
3. Include the raw opaque token only in the transport prompt and never in
   structured logs, status, receipts, exception output, or provider-response
   summaries.
4. Compare token hashes using the canonical security helper.
5. Redact absolute/local details from public or generated documentation while
   preserving exact local state references in the private runtime envelope.
6. Fail closed when prompt identity and stored intent differ.

**Deliverables:** Minimal prompt builder and redaction rules.

**Acceptance criteria:**

- Prompt is sufficient to locate and claim exactly one generation.
- Prompt prose cannot substitute for the SQLite task binding.
- Raw token does not appear in durable exported evidence.

**Minimal verification:** Golden prompt snapshot and secret-pattern scan on the
small fixture output.

**Recommendation coverage:** `REC-068`.

#### `RLY-05-04` — Add passive status, chain inspection, and optional Goal mirror

**Objective:** Make the relay understandable from any discussion without
creating another scheduler.

**Target files:** `summarize` projection, optional chain renderer, and native
Goal mirror adapter.

**Dependencies:** `RLY-05-02`, `RLY-05-03`.

**Actions:**

1. Project relay/plan identity, mode, revision, generation, task, predecessor,
   worker, claim/consume/return state, receipt, intent, lease, successor,
   terminal report, and next safe action.
2. Distinguish direct state from provider observation and inferred status.
3. Show ambiguity and human gates without providing a mutating button or hidden
   auto-retry.
4. Add a compact predecessor-successor chain view for operators.
5. If native Codex Goal mirroring is enabled, write only the approved
   `CodexGoalMirror` projection with `mirror_only` and
   `may_mark_complete=false`.
6. Make mirror failure advisory; it cannot fail, roll back, or alter canonical
   relay progress.

**Deliverables:** Read-only summary/chain output and optional mirror writer.

**Acceptance criteria:**

- Status commands execute no state mutation or provider create.
- Mirror state cannot select, dispatch, recover, cancel, or complete.
- Direct/inferred/unknown fields are visibly distinguished.

**Minimal verification:** Read-only snapshot test and mutation-counter assertion.

**Recommendation coverage:** `REC-009`, `REC-010`, `REC-052`, `REC-073`,
`REC-100`.

### Phase 06 — Python compatibility, focused canonical verification, and release candidate

#### Phase objective

Resolve the known interpreter inconsistency, prove the canonical runtime's
high-risk invariants with the smallest sufficient suite, and produce a
versioned canonical release candidate and generated metadata.

#### Entry criteria

- Phases 02–05 implementation is complete in canonical source.
- Package support range and release version are approved.
- No generated bundle or plugin has been hand-edited.

#### Phase exit gate

- Nested subprocesses use the resolved interpreter.
- Code parses on every declared supported Python version.
- Focused architecture, state, at-most-once, recovery, and compatibility tests
  pass.
- Canonical manifest, registry, bundle declaration, and generated metadata
  agree on the new package and dependencies.
- Release candidate is ready for website installation but is not pushed or
  published without separate authority.

#### `RLY-06-01` — Repair interpreter selection and support declaration

**Objective:** Make validation use one declared-compatible Python runtime from
parent to nested subprocess.

**Target files:** Canonical skill manifest, CLI launchers, nested subprocess
tests, runtime preflight, and syntax-incompatible generator line.

**Dependencies:** Phase 05.

**Actions:**

1. Replace hard-coded nested `python3` calls with `sys.executable` or an
   explicitly resolved approved interpreter.
2. Prefer rewriting 3.12-only syntax to remain compatible with the declared
   Python `>=3.11` floor; if that is not maintainable, raise the declared floor
   and document the compatibility consequence.
3. Add an early runtime-version preflight that fails before state mutation.
4. Propagate the same interpreter through all child validation and generation
   commands.
5. Configure release CI for every explicitly declared supported Python version;
   run the matrix once at the release-candidate gate, not after each task.

**Deliverables:** Interpreter resolver/preflight, compatible syntax, updated
manifest, and release CI matrix.

**Acceptance criteria:**

- Local unqualified `python3` cannot silently select Python 3.9 for this suite.
- Nested subprocess runtime equals the parent runtime.
- Manifest support range matches parsed syntax and CI.

**Minimal verification:** One runtime-preflight negative check and the release
CI matrix once.

**Recommendation coverage:** `REC-110` through `REC-114`.

#### `RLY-06-02` — Run the focused canonical acceptance suites

**Objective:** Establish executable evidence for all safety-critical acceptance
conditions without a broad or repetitive test program.

**Target files:** Existing implementation-plan tests, plus a minimal new relay
state/provider test module and static contract check.

**Dependencies:** `RLY-06-01`.

**Actions:**

1. Consolidate architecture/static checks into one scanner that rejects new
   goal activation imports, outer-goal fields in new records, coordinator owner
   state, worker-to-coordinator wakeups, resume requirements, and successor
   budgets above one.
2. Run one parameterized state suite over claims, consume, identities, leases,
   receipts, completion, no-ready semantics, and terminal/protected child bans.
3. Run one parameterized provider/recovery suite over the complete crash and
   ambiguity table in Section 16.4.
4. Run representative legacy-read, new-writer-refuses-legacy, backup/restore,
   export/import, and historical-migration-hash checks.
5. Do not duplicate these assertions in multiple skill and website suites;
   test canonical behavior once and adapt only façade-specific behavior later.

**Deliverables:** Focused test results and static contract report.

**Acceptance criteria:**

- Every condition in Sections 16.1–16.5 has an executable assertion.
- Tests do not require network or production discussion creation.
- Failure output identifies the violated invariant and state boundary.
- The suite remains small enough to run as one focused package gate.

**Minimal verification:** The focused suite itself plus `git diff --check` in
canonical source. Do not run unrelated skill or plugin suites at this task.

**Recommendation coverage:** `REC-104` through `REC-109`, `REC-123`.

#### `RLY-06-03` — Version canonical source and generate release metadata

**Objective:** Produce one dependency-resolved canonical release candidate from
source, not from installed derivatives.

**Target files:** Skill manifests, registry declarations, bundle/plugin source
declarations, catalog/README metadata, checksums, source maps, build receipts,
and release notes generated by canonical tooling.

**Dependencies:** `RLY-06-02`.

**Actions:**

1. Select the new version and writer/profile identifiers; retain explicit
   legacy compatibility identifiers.
2. Update canonical skill and dependency manifests.
3. Declare direct/dependency-resolved installation policies and plugin/bundle
   membership separately.
4. Generate registry, catalog, bundle, plugin, lock, source map, checksums, and
   build receipt using repository tools.
5. Verify generated sources point to the exact canonical commit/tree and that
   mutable state remains outside skill/generated trees.
6. Prepare release notes describing topology change, migration choice,
   compatibility shims, Python requirement, and rollback.
7. Do not push, tag, publish, or install into the website in this task unless
   separately authorized.

**Deliverables:** Canonical release candidate and deterministic generated
metadata.

**Acceptance criteria:**

- Installed package can be reproduced from declared canonical sources.
- No generated derivative contains an untracked hand edit.
- Old and new skill names resolve according to the accepted compatibility map.

**Minimal verification:** Canonical manifest/registry/bundle drift checks only;
the focused runtime suite is not rerun unless generation changes runtime bytes.

**Recommendation coverage:** `REC-004`, `REC-087`, `REC-091`, `REC-092`.

### Phase 07 — Canonical installation and website adaptation

#### Phase objective

Install the complete dependency-resolved canonical release candidate through
the normal installer, adapt the website façade to recursive ownership, and keep
website implementation control and release boundaries intact.

#### Entry criteria

- Phase 06 canonical release candidate is accepted for installation.
- Website live implementation-control packet authorizes exact installed,
  adapter, config, test, provenance, and documentation paths.
- Current website worktree, canonical source identity, lock, installer, and
  control state are revalidated.

#### Phase exit gate

- Website installed packages trace to the canonical release candidate.
- New website activation creates plan-native relay state and no generic outer
  goal.
- Worker-owned successor reservation and explicit terminalization are exposed.
- Adapter config declares recursive topology and accurate provider mode.
- Existing scope, validator, checkpoint, protected-effect, and release
  restrictions remain enforced.

#### `RLY-07-01` — Reinstall the dependency-resolved canonical bundle

**Objective:** Replace installed derivatives through the installer without
creating provenance drift.

**Primary repository:** Website installed-skill and installer metadata surfaces.

**Dependencies:** Phase 06.

**Actions:**

1. Record the exact canonical commit/version, bundle declaration, dependency
   graph, generated checksums, and installer command.
2. Confirm the website packet allowlist includes every installed dependency,
   shim, lock, registry, provenance, and receipt path the installer will touch.
3. Run the standard dependency-resolved installer once.
4. Reject partial direct copying or manual edits in `.agents/skills/`,
   `.codex/skills/`, or generated plugin trees.
5. Compare installed file hashes and versions with canonical bundle/source-map
   evidence.
6. Preserve unrelated installed skills and mutable local state.
7. Record installer output and exact changed-path manifest.

**Deliverables:** Complete installed bundle, changed-path manifest, and
installer evidence.

**Acceptance criteria:**

- Every installed relay dependency has a canonical source and checksum.
- No unexpected installed or generated path changed.
- Compatibility shims and new canonical entry points are both present as
  declared.
- Runtime state databases were not modified by installation.

**Minimal verification:** Installer integrity/checksum command and exact path
manifest comparison; do not run runtime or site gates yet.

**Rollback:** Reinstall the prior pinned bundle using its preserved lock and
receipt; do not delete new runtime state if any later task created it.

**Recommendation coverage:** `REC-004`, `REC-091`, `REC-092`.

#### `RLY-07-02` — Adapt the website state and lifecycle façade

**Objective:** Route new website plan runs to the plan-native relay and expose
generation-owned mutations.

**Target files:** `scripts/implementation_control/plan_goal_adapter.py` and
only its directly required support modules.

**Dependencies:** `RLY-07-01`.

**Actions:**

1. Add a recursive writer/profile selector that fails closed on legacy or
   mixed state.
2. Remove `goal.activation` and `initialize_goal` from recursive activation.
3. Replace mutable coordinator ownership with immutable
   `launcher_thread_id` plus per-generation predecessor and worker identities.
4. Route initialization, reservation, claim, consume, return/unknown, receipt,
   successor, recovery, and completion through plan-native operations.
5. Replace coordinator-only `reserve_next()` with worker-owned
   `reserve_successor()`.
6. Add adapter methods for `record_successor()`, `finalize_plan()`, typed
   generation recovery, reconciliation, summary, and cancellation.
7. Bind every mutation to expected plan revision and current website-control
   hash.
8. Keep `implementation_control/` task/job/handoff/completion and protected
   effects as the execution authority.
9. Preserve current scope, allowed-path, validator, checkpoint, branch,
   worktree, push, deploy, publication, and upstream-write restrictions.
10. Keep legacy coordinator handling read-only or explicitly selected legacy
    mode for the approved window.

**Deliverables:** Recursive website adapter path with explicit legacy boundary.

**Acceptance criteria:**

- Recursive activation creates no outer goal or coordinator session owner.
- Generation N's verified worker is the only normal owner allowed to reserve
  N+1.
- Completion candidate can be terminalized through the tracked command.
- Website-control drift stops before each mutating boundary.
- Plan completion grants no release or protected effect.

**Minimal verification:** Adapt the existing adapter tests only for recursive
activation, worker-owned successor, finalization, control-drift rejection, and
legacy-mode refusal.

**Recommendation coverage:** `REC-001`, `REC-006`, `REC-007`, `REC-017`
through `REC-020`, `REC-053` through `REC-056`, `REC-088`.

#### `RLY-07-03` — Update website CLI, config, and skill instructions

**Objective:** Make the recursive contract visible and executable from the
website's supported façade.

**Target files:** `scripts/implementation_control/continue_plan_goal.py`,
`.agents/implementation-plan-goal/adapter-config.json` or successor config,
installed skill docs produced by the installer, and focused façade tests.

**Dependencies:** `RLY-07-02`.

**Actions:**

1. Add/rename every command in Section 9 and its required CAS/identity
   arguments.
2. Deprecate `--coordinator-thread-id` for recursive commands and reject it when
   it would select a mixed topology.
3. Retain legacy commands only as read-only or explicit legacy mode.
4. Write the topology/cardinality declaration from Section 12.3.
5. Configure provider capability and explicit degraded manual mode.
6. Ensure installed launcher/frame instructions reflect the canonical source
   and stop after one successor.
7. Update help text with recovery-safe next commands and warning boundaries.
8. Keep old names as shims and show their deprecation/status without claiming
   native Goal behavior.

**Deliverables:** Website CLI, config, help, and installed skill surface.

**Acceptance criteria:**

- CLI exposes no required coordinator argument for recursive operation.
- Cardinality declarations match runtime constraints.
- Unsupported automatic create is reported as degraded manual mode.
- Help text never recommends blind retry or consumed-task rerun.

**Minimal verification:** Parser/help snapshot and focused façade tests; do not
run aggregate website validation yet.

**Recommendation coverage:** `REC-021` through `REC-042`, `REC-036` through
`REC-042`, `REC-069` through `REC-074`, `REC-089`, `REC-090`.

#### `RLY-07-04` — Add passive website status and control-boundary documentation

**Objective:** Expose truthful chain status while retaining the separation
between orchestration evidence and website execution/release authority.

**Target files:** Website summary/status renderer, implementation-control
operator documentation, and only necessary focused tests.

**Dependencies:** `RLY-07-02`, `RLY-07-03`.

**Actions:**

1. Project the passive status fields defined in `RLY-05-04` through the website
   façade.
2. Include website-control task/job/handoff identity and control hash beside
   relay status without merging the two authorities.
3. Explain that terminal plan state does not authorize stage, commit, push,
   deployment, publication, or upstream writes.
4. Document automatic and degraded-manual provider procedures.
5. Document recovery routes for ambiguity, consumed unknown, human gate,
   validation failure, no-ready blocked, cancellation, and identity drift.
6. Document the compatibility reader and retirement policy.
7. Keep status passive and ensure optional native Goal mirror failures are
   advisory only.

**Deliverables:** Website status output and operator guide.

**Acceptance criteria:**

- Operators can identify predecessor, worker, successor, intent, lease,
  receipt, terminal proof, and next safe action.
- Status cannot mutate plan or website control.
- Authority and release boundaries are explicit.

**Minimal verification:** Read-only snapshot and documentation review; no
browser or Astro build because no public route is added.

**Recommendation coverage:** `REC-007`, `REC-009`, `REC-010`, `REC-100`.

### Phase 08 — Disposable relay pilot and focused negative scenarios

#### Phase objective

Prove the new topology, at-most-once behavior, recovery, legacy readability,
and rollback with disposable state and no unapproved external effects.

#### Entry criteria

- Phase 07 passes its focused adapter checks.
- A disposable plan, project binding, database, and provider fixture or
  authorized non-production thread environment are available.
- The pilot has explicit authorization for exactly four discussions if a real
  provider is used.

#### Phase exit gate

- Positive three-task chain matches the exact expected topology and counts.
- All named negative/recovery boundaries resolve deterministically or to the
  expected human gate.
- Legacy records remain readable and unchanged.
- Rollback disables new writes without losing evidence.

#### `RLY-08-01` — Run the three-task recursive-chain pilot

**Objective:** Demonstrate the target architecture end to end with the smallest
useful dependency chain.

**Dependencies:** Phase 07.

**Pilot plan:** Three inert/disposable tasks with dependencies A -> B -> C and
no branch, commit, push, deploy, publication, or upstream effect.

**Actions:**

1. Launch once and record generation 1.
2. Let worker A claim, consume, execute task A once, finalize its receipt,
   reserve/create/record worker B, and stop.
3. Let worker B do the same for task B and worker C.
4. Let worker C execute task C, build the completion report, terminalize, release
   the lease, create no child, and stop.
5. Export the chain, receipts, intents, provider counts, revisions, journal,
   lease transfers, and final report.
6. Confirm no coordinator wakeup/resume and no generic outer-goal row.
7. Confirm no effect outside the disposable allowlist.

**Expected evidence:**

- four discussions total: one launcher and three workers;
- three task invocations and three immutable task receipts;
- one provider create per generation and zero duplicate creates;
- generation 2 predecessor equals worker A;
- generation 3 predecessor equals worker B;
- terminal worker creates zero children;
- one terminal completion report and no active lease or open intent.

**Acceptance criteria:** Every expected count and identity is established from
canonical state and provider receipts, not discussion prose.

**Minimal verification:** The pilot itself plus exported-state inspection. Do
not repeat canonical unit suites.

**Recommendation coverage:** `REC-101`, `REC-104` through `REC-106`.

#### `RLY-08-02` — Run table-driven negative and crash scenarios

**Objective:** Exercise all high-risk recovery boundaries in one consolidated
fixture-driven run.

**Dependencies:** `RLY-08-01`.

**Scenario table:**

| Group | Scenarios |
| --- | --- |
| Provider | ambiguous create; duplicate child; concrete return then record failure; zero child; multiple child |
| Invocation | crash after claim; crash after consume; unknown return boundary; task return before receipt |
| Identity | stale plan revision; repository drift; website-control drift; effort mismatch; current-thread mismatch |
| Decision | receipt before successor reservation; reservation before create; validation failure; human gate; cancellation |
| Completion | no-ready-task without completion; terminal proof before completion commit; open intent; active lease |

Implement the scenario set as one parameterized harness over injected boundary
markers, including failure immediately before and after every authoritative
state commit, before provider create, after create return, during successor
record, after claim, after consume, after task return, during receipt finalize,
after receipt/before successor reservation, after reservation/before create,
and after terminal proof/before completion commit.

**Deliverables:** A scenario-by-scenario result matrix containing the injected
boundary, resulting canonical state, permitted recovery command or human gate,
effect counts, invariant assertions, and retained evidence hash.

**Acceptance criteria:**

- Every resulting state has one deterministic recovery command or explicit
  human-required terminal/protected state.
- No scenario authorizes automatic rerun of consumed work.
- No scenario authorizes a second provider create for the same generation.
- Identity drift stops before the next effect.
- Validation failure and no-ready-blocked do not become completion.

**Minimal verification:** One execution of the parameterized harness. Do not
manually repeat every scenario in separate discussions.

**Recommendation coverage:** `REC-102`, `REC-107`.

#### `RLY-08-03` — Verify legacy compatibility, backup restore, and rollback

**Objective:** Prove the migration and rollback boundaries without converting
or deleting historical state.

**Dependencies:** `RLY-08-01`, `RLY-08-02`.

**Actions:**

1. Read representative legacy schema 3–7 records as applicable and compare
   pre/post hashes.
2. Prove new writers refuse legacy coordinator records and legacy writers
   refuse recursive records.
3. Export/import representative activation and hash evidence.
4. Restore the migration/new-database backup and compare canonical exports.
5. Disable the recursive writer and show that passive audit/status remains
   available.
6. Attempt no active-generation topology conversion; verify it is rejected.
7. Preserve both old and new state after the rehearsal.

**Deliverables:** Legacy read-compatibility report, migration-hash comparison,
backup/restore result, export/import hash result, and rollback rehearsal receipt.

**Acceptance criteria:**

- Legacy records and historical migration files remain byte-identical.
- Backup restores exactly or to canonical-hash equivalence documented by the
  ADR.
- Rollback requires no deletion or dual write.
- Active/consumed work remains in its original topology and stops safely.

**Minimal verification:** One compatibility/rollback fixture run and hash
comparison.

**Recommendation coverage:** `REC-095`, `REC-108`.

### Phase 09 — Final gate, release, cutover, monitoring, and retirement

#### Phase objective

Run the one permitted final aggregate gate per affected repository, release and
install only with explicit authority, switch new runs to recursive mode, and
retire legacy mutation commands only after the compatibility window and audit.

#### Entry criteria

- Phase 08 pilot and negative scenarios pass.
- No unresolved critical/high integrity, security, recovery, or migration
  finding remains.
- Release, install, and any Git/remote effects have separate explicit authority.

#### Phase exit gate

- Canonical release and website installed provenance agree.
- Recursive writer is the default for new runs.
- Legacy databases are read-only/auditable.
- Monitoring can identify ambiguity, unknown invocation, stuck intent, lease,
  and terminalization failure.
- Coordinator mutations retire only after their accepted compatibility gate.

#### `RLY-09-01` — Run one final proportional validation gate

**Objective:** Establish release-candidate consistency without repeating broad
checks throughout implementation.

**Dependencies:** Phase 08.

**Canonical repository checks:**

1. focused relay state/provider/recovery/compatibility suite;
2. declared Python-version release matrix;
3. canonical manifest/registry/bundle/plugin drift checks applicable to changed
   packages;
4. `git diff --check`.

**Website repository checks:**

1. `npm run validate:plan-goal`;
2. `npm run test:plan-goal`;
3. `npm run validate` once, because the website definition of done requires
   the aggregate gate or an explicit named skip reason;
4. `git diff --check`.

Do not add browser, accessibility, route, content, claim, manifest, SVG, or
build commands separately. The aggregate website command already runs its
configured checks once. If it fails because of verified unrelated drift,
record the exact blocker and keep the release unaccepted rather than repeatedly
rerunning or broadening this packet.

**Acceptance criteria:**

- Required commands pass on the final candidate, or a named external blocker
  prevents release without being misreported as implementation failure.
- One resolved compatible interpreter is used throughout each Python tree.
- No check was run repeatedly without a changed input that could affect it.

**Minimal verification:** The listed final commands are the verification. Do
not add a second manual or automated gate after they pass on unchanged bytes.

**Recommendation coverage:** `REC-109`, `REC-113`, `REC-114`, `REC-123`.

#### `RLY-09-02` — Release, reinstall final bytes, and cut over new writers

**Objective:** Activate the verified recursive profile for new runs while
preserving legacy state and release boundaries.

**Dependencies:** `RLY-09-01`.

**Actions:**

1. With explicit authority, commit/tag/publish the canonical release through
   repository release procedure.
2. Reinstall final released bytes into the website if they differ from the
   release candidate and regenerate lock, registry, import provenance, and
   installer receipt.
3. Verify installed hashes match the released canonical source map.
4. Change the website default new-run profile to `recursive_chain_v1`.
5. Keep legacy coordinator databases and readers available but prevent new
   runs from selecting them implicitly.
6. Record the activation time, versions, schema/profile identifiers, rollback
   command, and compatibility-window start.
7. Do not push or deploy the website unless separately authorized; local
   cutover and public deployment are different effects.

**Deliverables:** Canonical release receipt, final website installer receipt,
installed-hash comparison, cutover record, and rollback reference.

**Acceptance criteria:**

- New launch enters only the plan-native database/profile.
- No placeholder outer goal or dual write appears.
- Released, installed, locked, and receipted hashes agree.
- Rollback can disable new launch without deleting state.

**Minimal verification:** One post-install hash/profile inspection and one
read-only `summarize` call; do not rerun the full Phase 09 gate on unchanged
released bytes.

**Recommendation coverage:** `REC-092`, `REC-103`, `REC-115`.

#### `RLY-09-03` — Monitor the compatibility window and retire coordinator mutation

**Objective:** Retire the old mutation topology only after evidence shows it is
safe, while retaining historical inspection.

**Dependencies:** `RLY-09-02` plus the accepted compatibility window.

**Actions:**

1. Monitor new runs for ambiguous intents, multiple children, unknown consumed
   invocations, revision conflicts, lease anomalies, terminalization failures,
   mirror failures, and manual-mode use.
2. Keep monitoring passive; it may alert or summarize but cannot retry,
   reassign, or complete.
3. Audit whether any active or required workflow still needs legacy coordinator
   mutation commands.
4. Resolve or explicitly preserve every active legacy generation before
   retirement; never convert it in place.
5. Remove coordinator mutation commands and default wakeup/resume capability
   only after the ADR's evidence gate passes.
6. Retain read-only status/export and historical schema support for the approved
   retention period.
7. Update compatibility documentation and record the retirement receipt.

**Deliverables:** Compatibility-window observation summary, legacy-writer
usage audit, retirement decision/receipt, and updated compatibility matrix.

**Acceptance criteria:**

- No permanent coordinator is required for new operation.
- Retirement does not make historical state unreadable.
- No unresolved legacy writer is stranded or rewritten.
- Monitoring never becomes a hidden scheduler.

**Minimal verification:** Static absence check for default coordinator mutation
entry points plus read-only legacy export/status smoke check.

**Recommendation coverage:** `REC-103`, `REC-116` through `REC-120`.

## 15. Minimal validation and testing policy

### 15.1 Governing rule

Validation exists only to prove an affected contract or a release invariant.
Do not run a broad command merely because it exists. Do not repeat an aggregate
gate after every task. A task with documentation-only output uses review and
Markdown/diff hygiene; a task that changes one state transition uses the
focused transition suite; a task that changes generated packaging uses the
packaging drift check; and the final candidate receives one aggregate gate.

### 15.2 Required check families

| Check family | Purpose | When run | Maximum planned frequency |
| --- | --- | --- | ---: |
| Design/traceability review | Confirm ADR and plan cover topology, authority, migration, and recovery | Phase 01 and final plan audit | Twice |
| Schema/semantic fixtures | Confirm new records and cross-record identities | After Phase 02 schema stabilization | Once per materially changed schema batch |
| Focused state suite | Claims, consume, CAS, leases, receipt, decision, terminalization | Phase 03/04 stabilization and final candidate | Two runs unless relevant bytes change later |
| Focused provider/recovery suite | Exactly-once create and crash recovery | Phase 05/06 stabilization and final candidate | Two runs unless relevant bytes change later |
| Focused website façade suite | Adapter/config/CLI/legacy boundary | Phase 07 and final candidate | Two runs unless relevant bytes change later |
| Disposable three-task pilot | End-to-end recursive topology and counts | Phase 08 | Once |
| Parameterized negative pilot | Named failure boundaries | Phase 08 | Once |
| Python support matrix | Declared runtime compatibility | Phase 06 or final candidate | Once per release candidate |
| Aggregate canonical gate | Package/repository release consistency | Phase 09 | Once |
| Aggregate website `npm run validate` | Website definition of done | Phase 09 | Once |
| `git diff --check` | Formatting/whitespace defects | End of changed-repository packet and final | Lightweight; run when handing off a diff |

### 15.3 Explicitly omitted by default

Unless implementation changes the governed surface, do not add or separately
run:

- browser or multi-browser testing;
- visual or accessibility testing;
- route crawling;
- public content or claim review;
- manifest or provenance regeneration unrelated to installed skill provenance;
- SVG validation;
- Cloudflare validation or deployment;
- Astro page screenshots;
- performance or load testing;
- a second broad acceptance framework duplicating existing focused tests;
- repeated full `npm run validate` or repository-wide Python test discovery.

### 15.4 When a skipped check becomes required

A skipped check becomes required only if an authorized task changes the surface
the check governs. The task receipt must name the changed path/behavior and why
the additional check is necessary. “For completeness” is not a sufficient
reason.

## 16. Executable acceptance contract

The following conditions must be executable assertions before release. They
are consolidated into the focused suites described above rather than expanded
into a large independent test program.

### 16.1 Architecture assertions

- [ ] No new recursive plan run creates a generic outer-goal row.
- [ ] No default recursive runtime path imports goal activation,
  initialization, lease mutation, or coordinator state.
- [ ] Launcher creates exactly one generation-1 successor and zero AgentJobs.
- [ ] Every nonterminal relay frame creates at most one generation N+1
  successor.
- [ ] Every terminal or protected-stop frame creates zero successors.
- [ ] No generation after generation 1 points to the launcher.
- [ ] No `resume_thread(coordinator)` or worker-to-coordinator wakeup occurs.

### 16.2 State and authority assertions

- [ ] Every authoritative mutation is CAS-bound.
- [ ] Plan, task, repository, website control, thread, profile, topology,
  intent, and receipt identities match before claim and dispatch.
- [ ] SQLite uniqueness enforces one repository mutation owner.
- [ ] Plan state remains orchestration evidence, not website execution or
  release authority.
- [ ] Native Goal mirroring cannot mutate or complete plan state.
- [ ] Terminalization requires one complete immutable report.
- [ ] A missing ready task never proves completion.

### 16.3 At-most-once assertions

- [ ] Competing generation claims yield one winner.
- [ ] Duplicate consume fails.
- [ ] Duplicate provider create is not authorized.
- [ ] Re-recording the same successor ID is idempotent.
- [ ] Re-recording a different successor ID fails.
- [ ] Consumed unknown work is never rerun automatically.
- [ ] A worker cannot execute a second task.
- [ ] Same-task automatic successors remain forbidden.

### 16.4 Parameterized failure boundaries

Inject one failure marker at each boundary below in a single table-driven
harness:

- immediately before and after each authoritative state commit;
- before provider create;
- after provider create returns;
- during successor-record persistence;
- after claim;
- after consume;
- after task return;
- during receipt finalization;
- after receipt finalization but before successor reservation;
- after successor reservation but before provider create;
- after terminal proof construction but before completion commit.

Every resulting state must have a deterministic recovery command or an
explicit human-required terminal/protected disposition.

### 16.5 Compatibility and static assertions

- [ ] Legacy schema 3–7 records remain readable as applicable.
- [ ] New writers refuse legacy coordinator records.
- [ ] Legacy writers refuse recursive records.
- [ ] Migration backup restores exactly.
- [ ] Export/import preserves hashes and activation evidence.
- [ ] Historical migration files remain byte-identical.
- [ ] No active legacy generation can change topology in place.
- [ ] New authoritative plan imports do not use
  `agentjob_runtime.goal.*` activation/mutation paths.
- [ ] New relay records contain no required `outer_goal_id`.
- [ ] New writer state contains no mutable `coordinator_thread_id`.
- [ ] No worker-to-coordinator wakeup or resume capability is required.
- [ ] Every generation has exactly one successor create budget.

### 16.6 Final command gate

Run these website commands once on the final candidate:

```text
npm run validate:plan-goal
npm run test:plan-goal
npm run validate
git diff --check
```

Run canonical validation with one resolved declared-compatible Python
interpreter throughout the tree. Exact canonical commands must be taken from
the release candidate's current manifest rather than copied from stale plan
text.

## 17. Alternatives and disposition

| Alternative | Disposition | Reason |
| --- | --- | --- |
| Plan-native SQLite recursive relay | Recommended | Correct ownership topology, atomic state, no semantic outer-goal drift |
| Recursive relay with synchronized outer-goal shell | Temporary bridge only | Duplicates lifecycle state and creates synchronization risk; must have removal gate |
| Install canonical `0.2.0` persistent coordinator as final design | Rejected | Automates continuation but preserves permanent coordinator ownership and resume/wakeup dependence |
| Synchronize the current outer goal and keep manual coordinator | Rejected | Repairs lifecycle mismatch without changing the incorrect topology |
| Copy upstream file-backed helper exactly | Rejected | Paired-file transaction is weaker and adds avoidable crash-repair surface compared with SQLite |
| Native Codex Goal as authoritative scheduler | Rejected | UI/platform state cannot replace plan receipts, CAS, repository/control evidence, or protected-effect authority |

## 18. Security, privacy, reliability, and observability

### 18.1 Security and privacy

- Store only handoff token hashes; redact raw tokens from logs, receipts,
  exports, exceptions, status, and provider summaries.
- Reject state references outside the accepted repository/project binding.
- Preserve existing path-security and protected-effect controls.
- Do not write secrets, provider credentials, private URLs, or local personal
  data into canonical skill packages or public/generated documentation.
- Treat provider-returned text and worker prose as untrusted telemetry.
- Verify current thread, project, checkout, plan, task, profile, and effort
  before claim.
- Keep native Goal mirror permissions strictly below canonical relay authority.

### 18.2 Reliability

- Commit intent before the external create and record the returned child in a
  separate CAS transaction.
- Use SQLite uniqueness and transactions for one owner, one generation, one
  successor, one receipt, and one terminal report.
- Quarantine ambiguity and consumed unknowns rather than guessing.
- Preserve append-only evidence and journal links.
- Keep backup/restore and read-only legacy inspection available after cutover.
- Never use expiry alone to transfer a lease.

### 18.3 Observability

Passive status must expose:

- relay, plan, profile, topology, repository, and website-control identity;
- plan revision, generation, task, predecessor, and current worker;
- claim, consume, invocation, return/unknown, receipt, and validator state;
- dispatch intent, create budget/attempt, provider outcome, and successor;
- lease owner/status/diagnostic expiry;
- terminal report or protected-stop reason;
- direct versus inferred evidence;
- exactly one next safe command or a human gate.

Metrics or alerts may count ambiguity, unknown invocation, CAS conflict,
identity drift, lease anomaly, finalization failure, and degraded-manual use.
They remain passive and cannot schedule, retry, reassign, or complete.

## 19. Rollback rules

### 19.1 Before website cutover

- Revert or supersede canonical source through normal version control only when
  authorized.
- Reinstall the previous pinned bundle using preserved lock and installer
  receipt.
- Keep new disposable databases for audit until their retention decision.
- Do not rewrite the old coordinator database.

### 19.2 After website cutover but before a new run

- Disable recursive launch and restore the prior default profile only through
  an authorized configuration packet.
- Preserve installed and runtime evidence.
- Do not delete the plan-native database merely because no run is active.

### 19.3 After a recursive run starts

- Do not convert the active run to coordinator topology.
- Allow the current generation to reach a deterministic terminal/protected
  state or cancel it through the supported command.
- Disable only future recursive launches.
- Retain passive status/export and all receipts/intents/journal state.

### 19.4 Rollback acceptance

Rollback is successful only when repository and control identities are known,
no active mutation owner is orphaned, no consumed task is rerun, no evidence is
deleted, and the next safe operator action is explicit.

## 20. Recommendation coverage ledger

This ledger is the authoritative completeness checklist for the attached
analysis. Each recommendation has one stable ID, an implementation location,
and a source line range. A recommendation is “planned” only when its target task
and acceptance condition are both present; mere mention in this ledger is not
sufficient.

### 20.1 Architecture, authority, terminalization, and cardinality

| ID | Recommendation incorporated | Plan implementation | Source lines |
| --- | --- | --- | ---: |
| `REC-001` | Replace fixed coordinator and mandatory outer-goal wrapper with a plan-native recursive discussion relay | Sections 1, 5; `RLY-01-01`, `RLY-07-02` | 16–19 |
| `REC-002` | Preserve deterministic scheduler, CAS revisions, receipts, provider intents, validation boundaries, authority checks, and SQLite atomicity | Sections 1, 6–8; `RLY-03-01`, `RLY-03-03` | 16–19 |
| `REC-003` | Copy upstream relay ownership semantics, not its paired-file storage implementation | Sections 1, 3.2, 11; `RLY-01-01`, `RLY-01-02` | 16–19, 328–332 |
| `REC-004` | Redesign canonical `skills-Sys4AI` first, then install the redesigned bundle in the website | Sections 1, 12–14; `RLY-01-04`, `RLY-06-03`, `RLY-07-01` | 108–132, 591–605 |
| `REC-005` | Do not treat canonical `0.2.0` coordinator continuity as the final architecture | Sections 1, 4, 17; `RLY-01-01`, `RLY-01-04` | 108–132 |
| `REC-006` | Make the plan store the sole orchestration authority | Sections 5.2–5.3; `RLY-01-01`, `RLY-03-03`, `RLY-07-02` | 229–244 |
| `REC-007` | Keep website `implementation_control/` as actual execution/protected-effect authority | Sections 5.2–5.3, 12.2; `RLY-07-02`, `RLY-07-04` | 229–244, 555–564, 699–704 |
| `REC-008` | Keep the thread provider transport-only | Sections 5.2, 10; `RLY-05-01` | 229–244 |
| `REC-009` | Make status a passive inspection surface, not a scheduler | Sections 5.2, 18.3; `RLY-05-04`, `RLY-07-04` | 229–244, 699–704 |
| `REC-010` | Keep native Codex Goal optional, mirror-only, and unable to complete or mutate | Sections 4, 5.2, 7; `RLY-05-04`, `RLY-07-04` | 229–244, 336–345 |
| `REC-011` | Bind the task executor to only the current immutable task | Sections 5.2, 6.3; `RLY-02-02`, `RLY-04-03` | 229–244 |
| `REC-012` | Permit a frame to schedule one successor but never execute that successor's task | Sections 5.2, 6; `RLY-01-01`, `RLY-02-02` | 240–245 |
| `REC-013` | Limit launcher ownership to validate, initialize, reserve generation 1, create/record one successor, and stop | Sections 5.2, 8.1; `RLY-04-01` | 229–244, 372–388 |
| `REC-014` | Give relay frame N ownership of claim, one task invocation, verification, terminalization or one N+1 successor, then stop | Sections 5.2, 8.2–8.4; `RLY-02-02`, `RLY-04-02` through `RLY-04-04` | 229–244, 390–427 |
| `REC-015` | Preserve the unexplained historical terminalization events without rewrite or deletion | Phase 00; `RLY-00-01`, `RLY-00-02` | 134–172 |
| `REC-016` | Record an audit note for the missing terminalization-writer provenance | Phase 00; `RLY-00-02` | 134–172 |
| `REC-017` | Add a first-class CAS-bound `finalize-plan` operation | Sections 8.5, 9; `RLY-00-03`, `RLY-04-04`, `RLY-07-02` | 159–169, 451–472 |
| `REC-018` | Require an immutable completion report | Sections 7, 8.5; `RLY-00-03`, `RLY-04-04` | 159–169, 336–345 |
| `REC-019` | Terminalize, release lease, append completion receipt, and journal atomically | Sections 8.4–8.5; `RLY-00-03`, `RLY-03-03`, `RLY-04-04` | 159–169, 413–427 |
| `REC-020` | Reuse useful `0.2.0` completion-proof logic without coordinator coupling or `goal_reached` terminology | Sections 8.5, 12.1; `RLY-00-03`, `RLY-04-04` | 169–172, 518–539 |
| `REC-021` | Launcher AgentJobs equal zero | Section 6.1; `RLY-01-01`, `RLY-04-01`, `RLY-07-03` | 247–265 |
| `REC-022` | Tasks executed per relay discussion are zero or one | Section 6.1; `RLY-01-01`, `RLY-02-02`, `RLY-07-03` | 247–265 |
| `REC-023` | Direct `continue` calls per relay discussion are zero or one | Section 6.1; `RLY-01-01`, `RLY-04-03`, `RLY-07-03` | 247–265 |
| `REC-024` | AgentJobs per relay discussion are zero or one | Section 6.1; `RLY-01-01`, `RLY-04-03`, `RLY-07-03` | 247–265 |
| `REC-025` | Successors created per relay discussion are zero or one | Section 6.1; `RLY-01-01`, `RLY-04-04`, `RLY-07-03` | 247–265 |
| `REC-026` | Same-task automatic successor discussions equal zero | Sections 6.1, 6.3; `RLY-02-02`, `RLY-07-03` | 247–265 |
| `REC-027` | Active generations per plan are at most one | Sections 6.1–6.2; `RLY-03-02`, `RLY-03-03` | 247–265 |
| `REC-028` | Provider creates per generation are at most one | Sections 6.1, 10; `RLY-05-02` | 247–265 |
| `REC-029` | Completed/protected execution frames have exactly one finalized receipt | Sections 6.1, 8.3–8.4; `RLY-04-03`, `RLY-04-04` | 247–265 |
| `REC-030` | Consumed generations are never automatically rerun | Sections 6.3, 10; `RLY-04-03`, `RLY-04-05` | 247–265 |
| `REC-031` | Terminal or human-gated generations create no successor | Sections 6.4, 8.4; `RLY-04-04` | 247–265 |
| `REC-032` | Generation N+1 names generation N's worker as predecessor | Section 6.2; `RLY-04-04`, `RLY-08-01` | 247–265 |
| `REC-033` | Only generation 1 may name the launcher as predecessor | Section 6.2; `RLY-04-01`, `RLY-08-01` | 247–265 |
| `REC-034` | Lease expiry is diagnostic and never authorizes theft | Sections 6.4, 10; `RLY-01-03`, `RLY-03-03` | 247–265 |
| `REC-035` | Worker prose is telemetry, not completion evidence | Sections 5.3, 6.4, 8.3; `RLY-02-02`, `RLY-04-03` | 247–265 |
| `REC-036` | Prefer `implementation-plan-relay`; retain `implementation-plan-goal` as a thin no-native-Goal shim | Sections 4, 12.1; `RLY-02-01`, `RLY-02-04`, `RLY-07-03` | 267–285 |
| `REC-037` | Prefer `continue-implementation-plan-relay`; retain `continue-implementing-plan-task` as compatibility shim | Sections 4, 12.1; `RLY-02-02`, `RLY-02-04`, `RLY-07-03` | 287–300 |
| `REC-038` | Frame validates immutable envelope, waits for `successor_created`, and atomically claims | Sections 8.2, 14 Phase 04; `RLY-02-02`, `RLY-04-02` | 301–319, 390–399 |
| `REC-039` | Frame consumes immediately before and invokes `continue` at most once | Sections 8.3, 14 Phase 04; `RLY-02-02`, `RLY-04-03` | 301–319, 401–412 |
| `REC-040` | Frame records returned/unknown and reinspects canonical evidence | Sections 8.3, 14 Phase 04; `RLY-02-02`, `RLY-04-03` | 301–319, 401–412 |
| `REC-041` | Frame finalizes one receipt and decides complete, next task, bounded replan, human gate, integrity/capability stop, or cancellation | Sections 8.4, 14 Phase 04; `RLY-02-02`, `RLY-04-04` | 301–319, 413–427 |
| `REC-042` | Frame creates at most one authorized successor and stops after recording it | Sections 8.4, 14 Phase 04; `RLY-02-02`, `RLY-04-04` | 301–319, 413–427 |

### 20.2 State, lifecycle, commands, and recovery

| ID | Recommendation incorporated | Plan implementation | Source lines |
| --- | --- | --- | ---: |
| `REC-043` | Retain SQLite rather than copying the upstream paired-file state mechanism | Sections 1, 7, 11; `RLY-01-02`, `RLY-03-02` | 328–332 |
| `REC-044` | Prefer a new plan-native database and keep legacy goal-coupled state read-only | Section 11.1; `RLY-01-02`, `RLY-03-02`, `RLY-03-04` | 607–628 |
| `REC-045` | Add `PlanRelayRun v1` with root plan/repository/profile/revision/journal state | Section 7; `RLY-02-03`, `RLY-03-02` | 334–345 |
| `REC-046` | Add `PlanRelayGeneration v1` with permanent per-discussion ownership and invocation state | Section 7; `RLY-02-03`, `RLY-03-02` | 334–345 |
| `REC-047` | Add immutable `PlanTaskEnvelope v3` with relay/task/binding/profile/selection/topology identity | Section 7; `RLY-02-03` | 334–345 |
| `REC-048` | Add `PlanTaskReceipt v3` with direct counts, validators, paths, fingerprints, disposition, and uncertainty | Section 7; `RLY-02-03`, `RLY-04-03` | 334–345 |
| `REC-049` | Add `PlanDispatchIntent v3` with idempotency, token hash, create budget, attempt/outcome, returned ID, and response hash | Sections 7, 10; `RLY-02-03`, `RLY-05-02` | 334–345 |
| `REC-050` | Add `PlanRelayLease v1` with repository/generation/thread/token/transaction and diagnostic expiry | Sections 7, 10; `RLY-02-03`, `RLY-03-03` | 334–345 |
| `REC-051` | Add `PlanCompletionReport v1` with effective plan/receipts/validators/no-open-intent/no-lease/final fingerprints | Sections 7, 8.5; `RLY-02-03`, `RLY-04-04` | 334–345 |
| `REC-052` | Add optional `CodexGoalMirror v1` with mirror-only authority and no completion right | Sections 7, 14 Phase 05; `RLY-02-03`, `RLY-05-04` | 334–345 |
| `REC-053` | Remove required outer-goal IDs/revisions/tokens, `GoalMutation`, and goal store authority from new writers | Section 7.1; `RLY-02-04`, `RLY-03-03`, `RLY-07-02` | 347–357 |
| `REC-054` | Remove `goal_reached`, coordinator wakeups/owner state, and wait/resume provider requirements from new writers | Section 7.1; `RLY-02-04`, `RLY-07-02` | 347–357 |
| `REC-055` | Retain canonical JSON, SHA-256, UTC, SQLite migration/backup, locking, and common errors through neutral namespaces | Section 7.2; `RLY-03-01` | 359–366 |
| `REC-056` | New plan runtime must not import goal activation, initialization, or mutation | Sections 7.1, 16.5; `RLY-02-04`, `RLY-03-01`, `RLY-07-02` | 368–368 |
| `REC-057` | Launcher preflight verifies plan, graph, task hashes, repository, discussion, effort, authority, and protected grants | Section 8.1; `RLY-01-03`, `RLY-04-01` | 372–386 |
| `REC-058` | Launcher initializes, deterministically selects, writes revision proof, reserves generation 1, hashes token, and persists one intent | Section 8.1; `RLY-04-01` | 372–386 |
| `REC-059` | Launcher calls create exactly once, records child/response/lease in second CAS transaction, and stops | Sections 8.1, 10; `RLY-04-01`, `RLY-05-02` | 372–388 |
| `REC-060` | State helper must not call Codex; skill/provider performs the external effect between transactions | Sections 5.1, 8.1; `RLY-04-01` | 388–388 |
| `REC-061` | Successor validates all identities, confirms recorded thread, waits read-only, claims once, and rejects stale/duplicate ownership | Section 8.2; `RLY-04-02`, `RLY-05-01` | 390–399 |
| `REC-062` | Task path reinspects live state, compiles exact invocation, consumes, and calls once | Section 8.3; `RLY-04-03` | 401–412 |
| `REC-063` | Uncertain call/return records `unknown`, quarantines, and creates no successor | Sections 8.3, 10; `RLY-04-03`, `RLY-04-05` | 401–412 |
| `REC-064` | After return, recheck repository/control evidence, run required validators, and build one immutable receipt | Section 8.3; `RLY-04-03` | 401–412 |
| `REC-065` | Atomic post-task transaction finalizes receipt, updates task/phase, revalidates graph, selects/proves completion, and appends proof | Section 8.4; `RLY-04-04` | 413–425 |
| `REC-066` | Post-task outcome is terminal+release, one reserved successor+intent, or protected state with no successor | Section 8.4; `RLY-04-04` | 422–425 |
| `REC-067` | Provider create remains outside the post-task transaction | Sections 8.4, 10; `RLY-04-04`, `RLY-05-02` | 427–427 |
| `REC-068` | Use the minimal continuation-token prompt and keep routing authority in state | Section 8.6; `RLY-05-03` | 429–449 |
| `REC-069` | Retain `prepare`; replace activation loop with `launch`/`activate-relay` for generation 1 only | Section 9; `RLY-04-01`, `RLY-04-05` | 451–470 |
| `REC-070` | Provide claim, consume, returned/unknown, and verify/decide commands for generation frames | Section 9; `RLY-04-02` through `RLY-04-05` | 451–470 |
| `REC-071` | Provide worker-owned reserve successor, record successor, and finalize plan commands | Section 9; `RLY-04-04`, `RLY-04-05` | 451–470 |
| `REC-072` | Provide generation-bound reconcile, abandon-unconsumed, reconcile-consumed, and adopt-successor recovery commands | Section 9; `RLY-04-05` | 451–470 |
| `REC-073` | Provide passive `summarize` and explicit `cancel` commands | Section 9; `RLY-04-05`, `RLY-05-04` | 451–470 |
| `REC-074` | Use small crash-auditable mutations and deprecate coordinator arguments/commands | Section 9; `RLY-01-04`, `RLY-04-05`, `RLY-07-03` | 451–472 |
| `REC-075` | Retry pre-reservation only at same revision; after committed intent allow one create; after concrete return retry record only | Section 10; `RLY-04-05`, `RLY-05-02` | 474–493 |
| `REC-076` | Resolve ambiguous create by idempotency query: adopt exactly one, record proven zero, quarantine multiple/uncertain | Section 10; `RLY-01-03`, `RLY-05-02` | 474–493 |
| `REC-077` | Early child waits read-only; claim-before-consume recovery requires same proven thread or explicit adoption | Section 10; `RLY-04-02`, `RLY-04-05` | 474–493 |
| `REC-078` | Post-consume never reruns; post-receipt resumes only orchestration decision | Section 10; `RLY-04-03` through `RLY-04-05` | 474–493 |
| `REC-079` | Reject second successor, identity drift, and effort mismatch; diagnose rather than steal expired lease | Sections 6, 10; `RLY-03-03`, `RLY-04-05`, `RLY-05-02` | 474–493 |
| `REC-080` | Completion candidate builds immutable report, terminalizes atomically, and creates no child | Sections 8.5, 10; `RLY-00-03`, `RLY-04-04` | 474–493 |

### 20.3 File changes, migration, rollout, and installation

| ID | Recommendation incorporated | Plan implementation | Source lines |
| --- | --- | --- | ---: |
| `REC-081` | Recast canonical launcher as generation-1 bootstrap, no native Goal, no continuous coordinator, recursive worker ownership, preferred new name | Section 12.1; `RLY-02-01`, `RLY-04-01` | 497–509 |
| `REC-082` | Rename/recast canonical worker as recursive frame, replace wakeup with decision, allow one distinct successor, forbid same-task successor | Section 12.1; `RLY-02-02` | 510–516 |
| `REC-083` | Move `plan/continuous.py` coordinator path to legacy, add `plan/relay.py`, remove default run/wakeup/resume, use generation ownership and plan terminology | Section 12.1; `RLY-02-04` | 518–524 |
| `REC-084` | Stop worker coordinator wakeup, return canonical receipt, add post-receipt one-successor boundary, preserve consume/unknown safeguards | Section 12.1; `RLY-04-03` | 526–531 |
| `REC-085` | Stop constructing goal store as new plan authority; add plan leases/generations/idempotent successor/atomic completion while retaining CAS/evidence/intent integrity | Sections 7, 12.1; `RLY-03-03`, `RLY-04-04` | 533–539 |
| `REC-086` | If shared DB is used, add migration 008 and never edit historical migration bytes | Section 11.2; `RLY-01-02`, `RLY-03-02` | 541–551 |
| `REC-087` | Make the architectural change and reusable package in canonical `skills-Sys4AI` source before adaptation | Sections 12.1, 14 Phases 02–06; `RLY-02-01` through `RLY-06-03` | 495–551, 591–605 |
| `REC-088` | Remove goal activation from website adapter, replace coordinator identity, add worker reserve/record/finalize/generation recovery, preserve website controls | Section 12.2; `RLY-07-02` | 553–564 |
| `REC-089` | Introduce new website CLI commands, deprecate coordinator arguments, and keep legacy commands read-only/explicit | Sections 9, 12.2; `RLY-04-05`, `RLY-07-03` | 566–570 |
| `REC-090` | Replace adapter cardinality with explicit recursive topology and use truthful degraded manual mode if automatic create is unavailable | Section 12.3; `RLY-07-03` | 572–589 |
| `REC-091` | Do not patch installed `.agents/skills/` or `.codex/skills/` as the primary fix | Sections 3.2, 12; `RLY-01-04`, `RLY-07-01` | 591–605 |
| `REC-092` | Implement, validate, version, generate metadata, reinstall normally, update lock/registry/provenance/receipt, adapt façade, then validate website | Sections 12–14; `RLY-06-03`, `RLY-07-01`, `RLY-07-02`, `RLY-09-01`, `RLY-09-02` | 595–605 |
| `REC-093` | Prefer new relay DB, legacy read-only audit, clean rollback, byte-preserved old runs, and shared neutral SQLite infrastructure | Section 11.1; `RLY-01-02`, `RLY-03-01`, `RLY-03-02` | 607–628 |
| `REC-094` | If one DB is mandatory, add mode discriminator/nullable outer goal for new profile/relay and lease tables/legacy readers/no dual write | Section 11.2; `RLY-01-02`, `RLY-03-04` | 630–641 |
| `REC-095` | Never convert active plans, rewrite history, create placeholder goals, dual write, infer migration by version, or delete old state | Sections 11.3, 19; `RLY-01-02`, `RLY-03-04`, `RLY-08-03` | 643–650 |
| `REC-096` | Freeze long runs, record state parity, investigate event provenance, add supported terminalization, and confirm no active/ambiguous generations | Phase 00; `RLY-00-01` through `RLY-00-03` | 652–664 |
| `REC-097` | Approve ADR for topology, ownership, cardinality, authority, mirror, transport, lease, human gate/cancel, migration, and rollback | Phase 01; `RLY-01-01` through `RLY-01-04` | 666–678 |
| `REC-098` | Implement neutral utilities, native store/schemas/generations/completion/reconciliation/shims, keeping coordinator only explicit legacy | Phases 02–04; `RLY-02-04`, `RLY-03-01` through `RLY-04-05` | 680–688 |
| `REC-099` | Add fresh same-project/bound-checkout provider, explicit effort, intent-before-create, identity-after-create, ambiguity query, and no normal wait/resume | Phase 05; `RLY-01-03`, `RLY-05-01`, `RLY-05-02` | 690–697 |
| `REC-100` | Convert website commands/state, retain implementation-control authority, add passive chain view, and preserve release boundaries | Phase 07; `RLY-07-02` through `RLY-07-04` | 699–704 |
| `REC-101` | Run a three-task disposable chain with four discussions, three invocations/receipts, predecessor chaining, no coordinator, and terminal no-child | Phase 08; `RLY-08-01` | 706–722 |
| `REC-102` | Exercise ambiguous create, duplicate child, crash after consume, stale revision, repository drift, effort mismatch, human gate, validation failure, and no-ready-not-complete | Phase 08; `RLY-08-02` | 724–734 |
| `REC-103` | Release canonical version, reinstall full bundle, regenerate provenance metadata, run target validation, and retire coordinator mutation after compatibility window | Phase 09; `RLY-09-02`, `RLY-09-03` | 736–742 |

### 20.4 Acceptance, Python compatibility, alternatives, and first decisions

| ID | Recommendation incorporated | Plan implementation | Source lines |
| --- | --- | --- | ---: |
| `REC-104` | Enforce architecture acceptance: no outer goal/default goal imports, one first successor, at-most-one next, no terminal child, predecessor chain, no coordinator resume | Sections 6, 16.1; `RLY-06-02`, `RLY-08-01` | 744–756 |
| `REC-105` | Enforce CAS/identity/unique-owner/authority/mirror/completion-report/no-ready semantics | Sections 6, 16.2; `RLY-03-03`, `RLY-06-02` | 758–766 |
| `REC-106` | Enforce one claim winner, duplicate consume/create rejection, idempotent same child, conflicting child rejection, no unknown rerun/second task/same-task child | Sections 6, 16.3; `RLY-04-02`, `RLY-04-03`, `RLY-06-02` | 768–777 |
| `REC-107` | Inject all named failure boundaries and require deterministic recovery or human terminal | Sections 16.4, Phase 08; `RLY-06-02`, `RLY-08-02` | 779–795 |
| `REC-108` | Preserve schema 3–7 readability, writer separation, exact backup, hash-preserving export/import, migration bytes, and no in-place topology change; add static prohibitions | Sections 16.5, Phase 08; `RLY-03-04`, `RLY-06-02`, `RLY-08-03` | 797–817 |
| `REC-109` | Final minimum website commands include plan-goal validation/tests, aggregate validation, and diff check; canonical uses compatible interpreter | Sections 15, 16.6; `RLY-09-01` | 819–830 |
| `REC-110` | Use `sys.executable` for nested Python subprocesses | Phase 06; `RLY-06-01` | 832–847 |
| `REC-111` | Remove 3.12-only syntax or explicitly declare Python 3.12+ | Phase 06; `RLY-06-01` | 832–847 |
| `REC-112` | Add an early runtime-version preflight | Phase 06; `RLY-06-01` | 832–847 |
| `REC-113` | Run release CI on every declared supported Python version | Sections 15, Phase 06/09; `RLY-06-01`, `RLY-09-01` | 832–847 |
| `REC-114` | Use one resolved interpreter throughout the validation tree | Sections 15, 16.6; `RLY-06-01`, `RLY-09-01` | 832–847 |
| `REC-115` | Select plan-native SQLite recursive relay as the preferred architecture | Sections 1, 4, 17; `RLY-01-01`, `RLY-09-02` | 851–860 |
| `REC-116` | Allow synchronized outer-goal shell only as a short migration bridge | Sections 4, 17; `RLY-01-04`, `RLY-09-03` | 851–860 |
| `REC-117` | Reject canonical `0.2.0` persistent coordinator as the final design | Sections 1, 17; `RLY-01-01`, `RLY-01-04` | 851–860 |
| `REC-118` | Reject merely synchronizing current outer goal while retaining manual coordinator | Section 17; `RLY-01-01`, `RLY-09-03` | 851–860 |
| `REC-119` | Reject copying the upstream file-backed helper implementation | Sections 3.2, 11, 17; `RLY-01-02` | 851–860 |
| `REC-120` | Reject native Codex Goal as authoritative scheduler | Sections 4, 5, 17; `RLY-01-01`, `RLY-05-04` | 851–860 |
| `REC-121` | Make an accepted canonical ADR and migration plan the first architectural artifact, not a patch to installed website copies | Phase 01; `RLY-01-01` through `RLY-01-04` | 874–885 |
| `REC-122` | Settle final skill names, database choice, lease policy, human-gate recovery, provider contract, and compatibility duration before runtime/adaptation | Section 4, Phase 01; `RLY-01-01` through `RLY-01-04` | 874–885 |
| `REC-123` | Keep implementation testing and validation limited to required focused checks and one final aggregate gate | Sections 2.3, 15; `RLY-06-02`, `RLY-09-01` | Current user instruction |

## 21. Source-section coverage audit

| Source section | Recommendation IDs | Plan sections/tasks | Coverage disposition |
| --- | --- | --- | --- |
| Conclusion and findings 1.1–1.4 | `REC-001`–`REC-005`, `REC-115`–`REC-120` | Sections 1–5, 17; Phase 01 | Covered as architectural premise and alternatives |
| Finding 1.5 terminalization gap | `REC-015`–`REC-020` | Sections 8.5, 10; Phase 00 and `RLY-04-04` | Covered as pre-redesign safety repair and target terminalization |
| Target architecture 2.1 | `REC-006`–`REC-014` | Section 5; `RLY-01-01` | Covered by ownership and authority tables |
| Cardinality 2.2 | `REC-021`–`REC-035` | Section 6; schema/config/runtime tasks | Covered by data constraints and executable assertions |
| Two-skill design 3 | `REC-036`–`REC-042` | Sections 4, 12; Phase 02 | Covered by new packages and compatibility shims |
| Plan-native state model 4 | `REC-043`–`REC-056` | Sections 7, 11; Phases 02–03 | Covered by eight records, exclusions, and neutral utilities |
| Exact lifecycle 5 | `REC-057`–`REC-068` | Section 8; Phases 04–05 | Covered transaction by transaction |
| Command surface 6 | `REC-069`–`REC-074` | Section 9; `RLY-04-05`, `RLY-07-03` | Covered by supported CLI and legacy deprecation |
| Exactly-once recovery 7 | `REC-075`–`REC-080` | Section 10; Phases 04–05 and 08 | Covered by command matrix and parameterized faults |
| File-level recommendations 8 | `REC-081`–`REC-092` | Section 12; Phases 02, 06, 07 | Covered canonical-first through installed provenance |
| Storage migration 9 | `REC-093`–`REC-095` | Section 11; `RLY-01-02`, `RLY-03-02`, `RLY-03-04` | Covered preferred and fallback paths plus prohibitions |
| Rollout plan 10 | `REC-096`–`REC-103` | Phase summary and Phases 00–09 | Expanded into 37 bounded tasks |
| Acceptance suite 11 | `REC-104`–`REC-109` | Sections 15–16; Phases 06, 08, 09 | Covered with consolidated focused checks |
| Python defect 12 | `REC-110`–`REC-114` | `RLY-06-01`, `RLY-09-01` | Covered by interpreter preflight and one release matrix |
| Alternatives 13 | `REC-115`–`REC-120` | Section 17; Phase 01 | Covered with explicit dispositions |
| Logical next step | `REC-121`–`REC-122` | Section 4 and Phase 01 | Covered as mandatory gate before runtime edits |
| User validation constraint | `REC-123` | Sections 2.3, 15 | Covered by validation consolidation and skip policy |

## 22. Plan self-verification procedure

The plan is complete only when all checks below pass against this file.

### 22.1 Mechanical checks

1. Confirm source hash, line count, and byte count match Document control.
2. Confirm recommendation IDs form the uninterrupted sequence `REC-001`
   through `REC-123`.
3. Confirm every recommendation ID appears in the coverage ledger exactly once.
4. Confirm every ledger row names a non-empty implementation section/task and a
   non-empty source line range or the current user instruction.
5. Confirm all 37 task IDs are unique and each detailed task includes:
   objective, dependencies, actions, deliverables or expected evidence,
   acceptance criteria, minimal verification, and recommendation coverage.
6. Confirm source sections 1–14, Logical next step, and the current user's lean
   validation constraint have a coverage row.
7. Confirm the file is the only intended worktree change for this planning
   request.
8. Run `git diff --check`.

### 22.2 Builder pass

- Verify concrete actors, records, commands, files, transactions, dependencies,
  failure modes, phase gates, and rollback actions are named.
- Verify every task has a bounded outcome and does not silently perform later
  release effects.
- Verify the preferred architecture and acceptable fallback are distinguishable.
- Verify testing is proportional to changed behavior.

### 22.3 Refuter pass

- Search for any sentence that gives native Goal, provider, status, worker
  prose, plan prose, or validator output authority it does not possess.
- Search for any path that reruns consumed work, creates a second successor,
  steals an expired lease, or retries ambiguous create blindly.
- Search for any migration that edits history, dual-writes, converts an active
  run, or deletes old state.
- Search for any plan-complete statement that authorizes Git, deployment,
  publication, or upstream effects.
- Search for validation duplication, unrelated browser/site checks, or repeated
  aggregate gates.
- Search for any source recommendation without a task and acceptance path.

### 22.4 Gate result meanings

- `pass`: all 123 recommendations are mapped, the builder and refuter passes
  find no material omission, and mechanical checks pass.
- `repair`: the source and repository evidence are sufficient to correct a
  missing/ambiguous mapping directly.
- `block`: a recommendation requires an authority, decision, current-state
  fact, or implementation capability that cannot responsibly be inferred.

## 23. References

OpenAI Codex. (2026, July 22). *Implementation-plan relay architectural
analysis* [Unpublished technical analysis]. Local attachment
`/Users/alex.omegapy/.codex/attachments/ccedaa7d-f4ee-48c8-a2e2-ea8a096c17f4/pasted-text-1.txt`.

System for AI Skills. (2026). *Implementation plan goal* (Version 0.2.0)
[Software documentation].
`/Volumes/P-SSD/AngryOwl/skills-Sys4AI/skills/implementation-plan-goal/SKILL.md`.

The AEther Flow. (2026). *Continue research continue goal* [Software
documentation].
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.codex/skills/continue-research-continue-goal/SKILL.md`.

The AEther Flow. (2026). *Continue research goal* [Software documentation].
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.codex/skills/continue-research-goal/SKILL.md`.

The AEther Flow. (2026). *Continue-research goal record schema* [Technical
specification].
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.codex/skills/continue-research-goal/references/goal-file-schema.md`.

The AEther Flow Website. (2026). *Implementation plan goal* (Version 0.1.0)
[Software documentation].
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/.agents/skills/implementation-plan-goal/SKILL.md`.

The AEther Flow Website. (2026). *Plan-state SQLite design* [Technical
specification].
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/.agents/skills/agentjob-control/references/plan-state-sqlite-design.md`.

## 24. Completed plan-coverage verification

**Gate result:** `pass`.

**Mechanical result:**

- 123 recommendation ledger rows found;
- 123 unique recommendation IDs found;
- the uninterrupted range is `REC-001` through `REC-123`;
- no missing, extra, duplicate, or malformed ledger row found;
- 10 implementation phases found;
- 37 unique detailed task packets found;
- every task contains an objective, dependencies, bounded actions, deliverables
  or expected evidence, acceptance criteria, minimal verification, and
  recommendation coverage;
- all source recommendation sections and the later lean-validation instruction
  have explicit coverage rows;
- the source SHA-256 matches the Document control value;
- untracked-file diff whitespace check passed;
- only this intended plan file is new in the website worktree.

**Builder result:** The plan names concrete actors, authority boundaries,
records, fields, commands, state transitions, transaction boundaries, files,
dependencies, recovery paths, phase gates, evidence, rollback, and limited
validation. Every ledger recommendation maps to a section and at least one
bounded task/acceptance path.

**Refuter result:** The initial review found one sequencing defect: the
activation freeze ended after the legacy terminalization repair rather than
remaining in force for the full redesign. The plan was repaired so the freeze
continues through Phase 08, with only the explicitly authorized disposable
pilot excepted. The final review found no path that gives native Goal, provider,
status, plan prose, worker prose, or validator output excess authority; reruns
consumed work; blindly retries ambiguous creation; steals an expired lease;
dual-writes or rewrites migration history; or converts plan completion into
release authority.

**Writing-quality result:** The repository technical-writing warning gate
returned `pass` with zero warning hits after one imprecise phrase was replaced
with the exact term “generation N+1 successor.”

**Checks intentionally not run:** No npm tests, Astro build, route validation,
browser test, content/claim/manifest gate, or repository-wide validation was
run for this documentation-only planning change. Those checks cannot establish
recommendation coverage and would add the overhead the user explicitly asked
to avoid.
