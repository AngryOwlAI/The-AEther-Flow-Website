# Terminalization-event provenance audit

## Disposition

Writer provenance is **indeterminate; no tracked exact writer was found**.
The two original records are internally ordered, hash-linked terminalization
evidence for one historical plan. They do not establish which program or actor
authored them, whether that writer was reviewed, or whether the event names
belong to a supported released command. No event, database, backup, or journal
entry was rewritten during this audit.

## Authority and dependency

- Packet: `RLY-00-02` / `WI-20260722-050` / `WJ-20260722-050-A`.
- Authority: `codex-thread:019f8ad5-73d1-77f2-8d9d-521ccc9c98df:user-message:any-issue-authorization`.
- Dependency evidence: RLY-00-01 completion
  `implementation_control/tasks/WI-20260722-049/jobs/completions/WJC-20260722-049-A.yaml`,
  SHA-256 `687f75e8284f4e0eae5c1f9bc90f06a43ffbc3d7e87e824dee3e7aabf972d9f0`.
- Baseline audit SHA-256:
  `d7696de1df753f5f96698aa3b334a057f3fc5821f76bf395428c3e33e3c20d59`.

## Original live records

Both records occur in
`.local/sys4ai/implementation-plan-goal/state.sqlite3`, plan
`PLAN-AETHER-DOCUMENTS-NAV-RECOVERY-002`, generation 4. The records are the
last two entries in that plan's journal.

| Event ID / sequence | Event type | Raw payload bytes / SHA-256 | Prior hash | Event hash | Created |
| --- | --- | --- | --- | --- | --- |
| 675 / 61 | `plan_completion_candidate_confirmed` | 862 / `c66202f2518ddca64ebf8aea561cde9ecd75e8a3079352c764ddefce516b5733` | `0716c8c1f75dbdf423b56526867f605c70eb11127ce9b5eaac8c83ed616e2978` | `a04e2a185105a858cd9ee6c006c1b94f7ca9e47ed45d2442de484dbad3019938` | 2026-07-22T00:56:10Z |
| 676 / 62 | `plan_terminal_completion_recorded` | 3,442 / `a6a43e0bc30fea740a2bca26f4157c2816ac4514980cf45606c062db7dcdcb9e` | `a04e2a185105a858cd9ee6c006c1b94f7ca9e47ed45d2442de484dbad3019938` | `d89964b77f55cfb0a361b86d28a88b18615d4bb96dfb062dfa68ba856b9754d0` | 2026-07-22T00:56:10Z |

Sequence 60 is `plan_lease_released`, event hash
`0716c8c1f75dbdf423b56526867f605c70eb11127ce9b5eaac8c83ed616e2978`.
It is the exact predecessor named by sequence 61. Sequence 61 is the exact
predecessor named by sequence 62. There is no successor after sequence 62;
its event hash is the stored journal head. Current integrity, foreign-key, and
plan-parity checks pass.

Sequence 61 binds selection proof
`PSP-B518D0A5D136AA4767D2E18C`, proof SHA-256
`3e7d47c19c1c72709a235554fbf44d52950692990e02480ab5ac8003000e040a`,
completion-report SHA-256
`5137c5792f65804e6b18afe899db95a1b29762cabbb23f8322d4b1acf0bfd3af`,
the task-receipt hashes, and a hashed coordinator identity. Sequence 62 binds
source commit `c6aa66b9a7412f14c6573dd0467b82ea11310c20`, aggregate receipt
`PTR-b33588398239f93ead44122d70d88f73` / SHA-256
`42514584323a156ee5abe9634e3e576846b569c909fb738ad02a9b9f3a29ef6c`,
the completion record, release-effect flags, and the same hashed coordinator
identity.

These fields prove that the stored payloads claim specific terminal evidence
and are linked into the current valid journal. They do not identify the writer
binary, command, source revision, or human actor.

## Occurrence audit

An immutable read-only query found exactly two matching records in the live
database. No matching event name occurs in any of the four migration SQLite
snapshots:

| Snapshot | `plan_events` table | Matching events |
| --- | --- | ---: |
| pre-v2 | absent | 0 |
| pre-v3 | absent | 0 |
| pre-v4 | present | 0 |
| pre-v5 | present | 0 |

A binary-safe search of the ignored state tree found the names only in the
live database. The names are quoted in the RLY-00-01 baseline and this audit,
but no current website script, installed skill source, test, schema, control
record, or other tracked documentation defines an exact writer. Searches of
all website Git history likewise found no commit adding or removing either
exact event string.

The same exact-name searches found no writer in the canonical
`/Volumes/P-SSD/AngryOwl/skills-Sys4AI` checkout or its Git history at
`7124baf2026f3ba392d9a81ce4feef55503f67d4`.

## Structural comparison

Canonical implementation-plan-goal 0.2.0 does contain related reviewed logic:
`SQLitePlanStore.finalize_plan_completion` validates an immutable completion
report and, in one SQLite mutation, stores the report, sets the plan to
`terminal_complete`, and journals a `plan_completion_receipt`. Its continuous
runtime builds the report when deterministic selection returns
`completion_candidate`.

That is structurally equivalent terminalization logic, but it is not an exact
writer for these two records:

- the installed website profile is 0.1.0 and does not contain that method or
  continuous module;
- the canonical method journals `plan_completion_receipt`, not either audited
  `event_type`;
- the canonical payload shape differs from both original payloads; and
- neither Git history contains the exact audited names.

The canonical method therefore demonstrates that a supported completion-proof
design exists upstream; it does not establish authorship of event IDs 675 and
676.

## Before/after preservation evidence

The live database SHA-256 remained
`ad7aecf857bc9153fa50722cee03b5136b7ea5790889c6c4440f83d01ce4cf5b`
before and after every event, backup, source, and Git-history query. The
sequence-61 and sequence-62 raw-payload hashes, event hashes, and predecessor
links are unchanged from the RLY-00-01 baseline. No integrity break, concurrent
mutation, missing original byte sequence, or journal mismatch was found.

## Conclusion

The evidence supports the category **writer indeterminate, exact tracked
writer absent**. Authorship and execution authority remain unknown. The
original records must remain append-only historical evidence. RLY-00-03 should
add a separately named, first-class, CAS-bound legacy `finalize-plan` path and
must not synthesize, replay, or claim provenance for these two event names.

## References

The AEther Flow Website. (2026, July 22). *Plan-native recursive relay baseline
audit* [Control audit].

The AEther Flow Website. (2026, July 22). *Implementation-plan-goal SQLite
state, schema version 5* [Local control database].

Sys4AI. (2026, July 21). *Implementation-plan-goal 0.2.0 canonical source*
[Software source code].
