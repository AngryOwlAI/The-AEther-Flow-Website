# Plan-State SQLite Design

Status: Historical IPG-0301 design contract with current production mapping
Target profile: serial implementation-plan goal runtime v1
Target database baseline: generic goal-store schema version 2
Production implementation owner: IPG-0302 and later Phase-03 tasks

## Scope

This document records the normalized plan-state SQLite schema and migration
sequence designed for the serial implementation-plan profile. The design was
subsequently implemented by production migration
`scripts/agentjob_runtime/goal/migrations/003_plan_state_v1.sql` and the
production plan runtime. Where this document describes the original IPG-0301
boundary, that language is historical rather than a statement that production
implementation is absent.

This design preserves:

- existing generic goal tables and migration checksums;
- `sys4ai.continue-goal.v1` reader behavior and v2 read/write behavior;
- the generic continuation envelope, goal receipt, provider, lease, recovery,
  and CLI contracts;
- one accepted plan, one active task, one fresh worker, one direct
  continuation, zero or one AgentJob, and at most one provider intent per
  generation; and
- mutable state outside canonical, adapted, and generated skill trees.

## Storage decision

Plan state extends the existing goal-relay SQLite database through the same
global `schema_migrations` sequence. A separate plan database was rejected
because SQLite cannot provide one crash-atomic commit across two independent
database files for the outer goal revision, plan revision, task receipt,
journal entry, lease transfer, and successor intent under all supported
journal modes.

Plan records use separate `plan_*` tables. They do not add fields to generic
goal rows or reinterpret generic record bytes. `plans.outer_goal_id` binds one
plan record to one outer goal record, and plan leases bind to the matching
generic lease transaction.

## Migration versions

| Version | Name | Status | Contract |
| ---: | --- | --- | --- |
| 1 | `initial` | retained, immutable | Existing generic goal-relay tables, indexes, and triggers. |
| 2 | `nullable_effective_deadline` | retained, immutable | Existing v1 deadline projection and v2 unlimited-deadline support. |
| 3 | `plan_state_v1` | retained, immutable | Add all base plan tables, indexes, views, and immutability/CAS triggers as one atomic profile installation. |
| 4 | `goal_v3_profiles_and_reports` | retained, immutable | Add generic goal activation profiles, resolution records, and authoritative completion reports. |
| 5 | `plan_execution_profiles` | retained, immutable | Add accepted plan execution profiles, topology authority, and profile-aware provider/task evidence. |
| 6 | `plan_continuous_relay` | current additive writer | Add question batches and responses, execution authority, continuous state v2, coordinator wakeups, and canonical completion reports. |

The production version-3 file, if IPG-0302 accepts this design, belongs at
`scripts/agentjob_runtime/goal/migrations/003_plan_state_v1.sql`. Splitting
the initial plan profile across multiple applied versions is not permitted:
partial installation would allow a plan row without its receipt, intent,
lease, or journal constraints. Later compatible storage changes use version 4
or higher and never alter the applied version-3 bytes or checksum.

## Normalized table matrix

| Table | Canonical responsibility | Principal key and relation |
| --- | --- | --- |
| `plans` | Accepted immutable plan JSON, mutable canonical state JSON, outer-goal binding, repository binding, revision, phase, active task, evaluation, and journal head. | `plan_id`; unique `outer_goal_id`; `(plan_id, active_task_id)` points to `plan_tasks`. |
| `plan_phases` | Immutable phase definitions and canonical order. | `(plan_id, phase_id)`; unique canonical position per plan. |
| `plan_phase_dependencies` | Immutable ordered phase edges. | `(plan_id, phase_id, depends_on_phase_id)`; both ends reference the same plan. |
| `plan_tasks` | Immutable canonical and replacement task definitions, hashes, phase membership, and canonical order. | `(plan_id, task_id)`; unique task hash identity and canonical position. |
| `plan_task_dependencies` | Immutable ordered task edges. | `(plan_id, task_id, depends_on_task_id)`; both ends reference the same plan. |
| `plan_task_states` | Mutable task lifecycle projection, generation, cardinality counters, receipt link, fingerprints, and terminal reason. | One row per `(plan_id, task_id)`; unique non-null generation per plan. |
| `plan_receipts` | Immutable task, phase-gate, and plan-completion records with receipt hashes and scheduler-critical result projections. | Global `receipt_id`; partial unique indexes enforce one receipt per task, phase, generation, or plan as applicable. |
| `plan_amendments` | Finalized append-only effective-plan changes and prior/new hash chain. | `amendment_id`; unique sequence per plan. |
| `plan_supersessions` | Finalized original-task replacement authority and graph hash. | `supersession_id`; one finalized supersession per original task. |
| `plan_supersession_replacements` | Ordered replacement-task membership. | `(supersession_id, replacement_task_id)`. |
| `plan_supersession_acceptance` | Criterion-to-replacement coverage mapping. | `(supersession_id, criterion_id, replacement_task_id)`. |
| `plan_selection_proofs` | Immutable revision-bound scheduler proof and outcome. | `proof_id`; one deterministic proof per `(plan_id, plan_revision)`. |
| `plan_provider_intents` | One task/generation provider intent and its terminal outcome, with token and response hashes only. | `intent_id`; unique `(plan_id, generation)` and `(provider_id, idempotency_key)`. |
| `plan_fingerprints` | Ordered immutable repository fingerprints. | `(plan_id, sequence)`. |
| `plan_leases` | Plan projection of the active generic lease, using a holder-token hash. | `transaction_id`; unique active lease per plan and repository fingerprint; unique outer lease transaction. |
| `plan_events` | Append-only hash-linked plan journal. | `(plan_id, sequence)` and globally unique event hash. |
| `plan_recovery_actions` | Append-only authorized recovery evidence. | `recovery_action_id`; unique sequence and action hash. |
| `plan_question_batches` | Immutable deterministic activation and late-input batches. | `batch_id`; content hash and plan binding are immutable. |
| `plan_execution_authorities` | Immutable default-local and exact-exception authority manifest. | One accepted authority per continuous plan. |
| `plan_question_responses` | Immutable complete response to one question batch. | `response_id`; binds the exact batch hash. |
| `plan_continuous_states` | CAS-protected coordinator projection, nonterminal wait/safeguard state, and completion binding. | One row per plan with exact revision advancement. |
| `plan_coordinator_wakeups` | Idempotent worker-receipt notification and parent-resume evidence. | `wakeup_id`; unique generation and worker/receipt identity. |
| `plan_completion_reports` | Immutable canonical goal-completion proof. | One complete report per plan. |

The canonical JSON record remains authoritative for field meaning. Normalized
columns and child rows are searchable integrity projections, not a second
source of truth.

## Constraint matrix

| Invariant | SQLite enforcement | Store-level enforcement |
| --- | --- | --- |
| One active task per plan | Partial unique index on `plan_task_states(plan_id)` for `reserved`, `active`, or `verifying`. | `plans.active_task_id`, phase, lease, and lifecycle JSON must name the same task. |
| One task per generation | Partial unique index on `(plan_id, generation)`. | Envelope, provider intent, receipt, and journal must bind the same task/hash/generation. |
| One provider intent per generation | Unique `(plan_id, generation)`. | Intent content hash, task identity, expected revision, provider response, and outer provider evidence must agree. |
| One open provider intent per plan | Partial unique index for `status='intent' AND finalized=0`. | Unknown, ambiguous, timeout, or duplicate outcomes quarantine scheduling. |
| At most one provider call | `provider_create_budget=1`, `create_attempts` in `[0,1]`, and status-dependent checks. | Provider adapter call budget and direct receipt evidence remain authoritative. |
| No same-task successor | `same_task_successors=0` in task state. | Scheduler rejects the consumed task ID and requires a new replacement ID when replanning. |
| One finalized receipt | Partial unique receipt indexes for task, generation, phase, and plan. | Schema, content hash, journal link, acceptance, validator, checkpoint, and identity parity must pass. |
| One active lease | Partial unique indexes by plan and repository fingerprint; unique outer lease transaction. | Plan and generic lease transitions occur in the same transaction and use the same generation/repository binding. |
| Deterministic canonical order | Unique canonical positions and ordered dependency positions. | Scheduler orders by `(canonical_position, task_id)` only after effective graph validation. |
| Revision compare-and-swap | Trigger requires every plan-row update to increment by exactly one. | Update uses `WHERE plan_id=? AND state_revision=?` inside `BEGIN IMMEDIATE`. |
| Immutable definitions and evidence | Triggers reject updates/deletes of plan identity, phases, tasks, dependency edges, finalized receipts, amendments, supersessions, proofs, journal entries, fingerprints, and recovery actions. | Corrections append an amendment, supersession, recovery action, or new migration; original bytes remain. |
| Hash length and JSON shape | SHA-256 length checks and `json_valid` checks. | Strict schema dispatch, canonical-byte equality, content-hash recomputation, and semantic validation. |
| Dependency and supersession acyclicity | Self-edge and foreign-key checks. | Full phase, task, and replacement graph cycle detection before write and before selection. |

SQLite constraints intentionally do not claim to validate JSON Schema,
canonical SHA-256, graph acyclicity, receipt semantics, or cross-record
authority. Those require the versioned validators and canonical hashing
utilities already owned by `agentjob-control` and the implementation-plan
profile.

## Canonical JSON and normalized parity

Every canonical plan-profile record write must satisfy this sequence:

1. Parse with duplicate-key rejection and dispatch by exact schema version.
2. Validate the full JSON record and required cross-record semantics.
3. Serialize with `canonical_json_bytes`; the stored JSON text must equal the
   UTF-8 canonical bytes exactly.
4. Recompute the declared content hash using the schema-specific hash basis.
   Self-hash fields are omitted only where the schema explicitly says so.
5. Compare every normalized scalar projection with its canonical JSON field.
6. Compare every ordered phase, task, dependency, replacement, acceptance,
   receipt, fingerprint, and journal child row with the canonical arrays.
7. Verify receipt and provider identities against plan ID/hash, task ID/hash,
   generation, repository fingerprint, and journal head.
8. Verify `plans.active_task_id`, the sole active task-state row, plan phase,
   plan lease, and matching generic lease are identical projections.
9. Verify counters equal their task-state and receipt-derived totals.

Load fails closed on any byte, hash, projection, child-row, journal, lease, or
counter difference. A database `CHECK` pass alone is insufficient.

## Transaction boundary

Every state-changing plan operation uses one connection and one
`BEGIN IMMEDIATE` transaction:

1. Read `plans` by ID and compare the exact expected revision.
2. Validate current canonical/normalized parity and the active generic/plan
   lease pair.
3. Validate the proposed transition, schema, identities, hashes, authority,
   graph, counters, and journal predecessor.
4. Insert immutable child records and append the journal entry.
5. Synchronize task state, fingerprints, provider intent, receipt, amendment,
   supersession, proof, recovery, and lease projections.
6. Update `plans` with `state_revision = expected_revision + 1` and
   `WHERE state_revision = expected_revision`.
7. Re-read and validate the resulting projections and targeted foreign keys.
8. Commit. Any exception rolls back the full plan and outer-goal transition.

Provider creation remains outside the database transaction. The pre-effect
intent is committed first; the provider is called at most once; its returned,
definitive-failure, or uncertain outcome is then committed in a new
revision-checked transaction. Ambiguity is never hidden by holding a database
transaction across the external call.

Continuous coordinator waiting and parent resumption also remain outside the
transaction. Each wakeup intent is persisted before `resume_thread`; delivered
or ambiguous evidence is finalized exactly once. An ambiguous resume enters
`suspended_safeguard` and never authorizes a duplicate provider create or a
rerun of consumed work.

## Ready-task query

The design fixture defines:

- `plan_effective_task_leaves_v1`, a recursive view that resolves finalized
  supersession chains to effective leaf tasks; and
- `plan_ready_tasks_v1`, a view that returns pending, unsuperseded tasks only
  when there is no active task and every effective dependency leaf has one
  finalized `task_complete` receipt with passing acceptance/validators and a
  passing or not-required checkpoint.

After schema, parity, graph, receipt, journal, lease, and revision validation,
the only selection query is:

```sql
SELECT task_id, task_sha256, phase_id, canonical_position
FROM plan_ready_tasks_v1
WHERE plan_id = ?
ORDER BY canonical_position, task_id
LIMIT 1;
```

The query is read-only. Zero rows must be classified separately as
`active_task_present`, `blocked_no_runnable`, `completion_candidate`, or
`invalid`; zero rows never imply completion. A selected row is only a
candidate until a selection proof and the task reservation are committed by
compare-and-swap in one transaction.

## Migration and backup sequence

IPG-0302 must implement the version-3 migration using this sequence:

1. Acquire the existing process-level store lock and reject symlinked or
   out-of-root state paths.
2. Open the source database with foreign keys enabled, a bounded busy timeout,
   `synchronous=FULL`, and the existing WAL policy.
3. Verify current schema version 2, all applied names/checksums, quick/integrity
   status, foreign keys, and canonical generic-goal parity.
4. Create a same-snapshot SQLite online backup in the protected local state
   directory using a restrictive temporary file, then fsync and atomically
   rename it.
5. Create a deterministic JSON export and a backup manifest containing source
   database identity, from/to versions, migration checksum, backup SHA-256,
   export SHA-256, timestamp, permissions, and preflight results.
6. Recheck the source schema and state revision after backup; abort if either
   changed.
7. Execute `BEGIN IMMEDIATE`, apply the immutable version-3 SQL body, and
   insert its name/checksum into `schema_migrations`.
8. Run targeted table/index/trigger/view checks, `foreign_key_check`, and
   canonical projection parity before commit.
9. Commit, run the post-commit integrity and parity checks, fsync the database
   and containing directory where supported, and retain the backup manifest.
10. On failure, roll back the transaction and retain the verified version-2
    backup. Never insert a version-3 migration row after a partial failure.

The backup database, JSON export, and manifest remain project-local with mode
`0600` where supported. They may contain sensitive local state and must never
enter `skills/`, `.agents/skills/`, generated plugins, Git, logs, prompts, or
tracked receipts. Tracked evidence records only hashes and opaque local
references.

Rollback is restoration of the verified version-2 backup under explicit
authority, not a reverse migration and not deletion of newer audit evidence.
Old code must not open a version-3 database in write mode unless its reader
compatibility is directly proven.

## Compatibility and implementation boundary

Version 3 only adds prefixed tables, indexes, views, and triggers. It does not
rename, drop, reinterpret, or rewrite any generic goal table or record.
Existing goal readers that ignore unknown tables remain byte-compatible.
Existing migration checksums remain immutable.

At the IPG-0301 boundary, no production migration, `plan` model, store,
scheduler, CLI command, provider effect, recovery command, installer change,
generated copy, plugin, or mutable runtime state was added. IPG-0302 and later
Phase-03 work subsequently supplied the production migration, backup
implementation, checksums, canonical plan model, transactional store,
lifecycle mutations, and scheduler runtime. Later additive versions 4 through
6 preserve every applied migration byte and add profile, topology, and
continuous-coordinator records without silently upgrading an active v1 run.

## Design verification

Current repository validation checks immutable migration checksums, executed
3-to-4-to-5-to-6 paths, rollback and export behavior, uniqueness constraints,
ready-task views, coordinator CAS, provider ambiguity, worker wakeups, and a
multi-task continuous journey. Target-project adapters and a live provider
still require their own pilot because repository tests use controlled provider
transports.
