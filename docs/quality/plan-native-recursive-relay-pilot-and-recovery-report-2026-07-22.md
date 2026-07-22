# Plan-Native Recursive Relay Pilot and Recovery Report

Date: 2026-07-22  
Plan: `PLAN-SYS4AI-RECURSIVE-RELAY-001`  
Canonical release: `implementation-plan-relay-v0.3.0` at
`e9fd6cb5d836bd6b1ee19edef2f025a6ab9178e3`

## Conclusion

The disposable three-task recursive chain, the consolidated failure/recovery
matrix, legacy compatibility, backup/import equivalence, and website façade
checks passed. No production discussion, native Codex Goal, generic outer
goal, website content mutation, push, or deployment was used by the pilot.

The canonical acceptance receipt is
`/Volumes/P-SSD/AngryOwl/skills-Sys4AI/docs/skills/VALIDATION_RECEIPTS/2026-07-22-plan-native-relay-acceptance.json`,
SHA-256
`022ddd16f0e85e338046c8f880dca90f65612fefd5f93f4b41c31f717ac44b54`.

## Positive pilot

The pilot created one launcher discussion plus workers A, B, and C. It
observed exactly three generations, three provider creates, three task
invocations, three immutable receipts, and one completion report. Generation
2 named worker A as predecessor; generation 3 named worker B. The terminal
frame created no child, all intents were closed, the repository lease was
released, the journal verified, and the state contained zero outer-goal rows
and zero coordinator wakeups.

The final run revision was 22. The acceptance receipt records both expected
and observed counts and marks the pilot `pass`.

## Acceptance and launch preflight

`sys4ai.plan-relay-acceptance.v1` now binds the complete plan/objective/
revision/task graph, repository binding and fingerprint, website-control
fingerprint, launcher discussion, requested/effective effort, authority
manifest, protected-effect grants, profile, and topology. The focused test
`test_stale_acceptance_fails_before_database_initialization` changes one bound
identity and proves `relay.acceptance_stale` is returned while the SQLite file
does not exist. This closes the launch-before-acceptance failure boundary.

## Negative and crash matrix

All 25 table-driven scenarios passed. They cover:

- provider failure proven before create, ambiguous create, duplicate child,
  returned-child record failure, and zero/multiple-child reconciliation;
- crash after claim, crash after consume, unknown return, return before
  receipt, and receipt-finalization CAS failure;
- stale revision, repository/control drift, effort mismatch, and current-
  thread mismatch;
- receipt-before-decision, successor-reservation-before-create, validation
  failure, human gate, and explicit cancellation; and
- no-ready-but-incomplete, proof-before-completion-commit, open intent, and
  active-lease atomic terminalization.

Every scenario retains a deterministic recovery route or an explicit human
gate. No scenario exceeds one invocation or one provider attempt per
generation, authorizes lease theft, creates a same-task successor, or reruns
consumed unknown work.

## Compatibility and rollback

Read-only legacy fixtures for schemas 3, 4, 5, 6, and 7 retained identical
database hashes. Historical migrations 001 through 007 retained identical
SHA-256 values. Recursive writers refused legacy state and legacy writers
refused recursive state. Backup and import exports reproduced the source
canonical export hash exactly. The rollback rehearsal disabled the recursive
writer without deleting state, dual writing, or converting an active run.

## Interpreter and focused tests

The same 24-test focused canonical suite passed under Python 3.11.14 and
Python 3.12.13. The Python 3.11 requirements check reported a standard-library-
only compatible closure. The website-specific relay adapter suite passed
seven tests after installing the final source hashes, including stale
acceptance, control drift, terminalization, passive status, protected stop,
redaction, and no-outer-goal assertions.

Evidence classification is explicit: SQLite identities, generations,
intents, receipts, hashes, and counts are direct; lease-expiry and next-safe-
action labels are inferred; an absent worker ID is unknown. No conversational
prose or provider state was treated as completion evidence.
