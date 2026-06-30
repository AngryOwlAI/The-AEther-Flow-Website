# Implementation-Control Scripts

These scripts support website-local continuation control. They are maintainer
tools, not public website runtime code.

## Commands

- `python3 scripts/implementation_control/continue_implementation.py`: read
  `implementation_control/program_state.yaml` and referenced task, job, and
  handoff records, then print deterministic JSON describing the next bounded
  implementation boundary.
- `python3 scripts/implementation_control/continue_implementation.py --summary`:
  print the same resolved state as a concise human-readable summary.
- `python3 scripts/implementation_control/validate_implementation_control.py`:
  validate implementation-control records fail-closed, including live record
  references, approval gates, allowed write paths, required validators, and
  validation-chain package wiring.
- `python3 scripts/implementation_control/checkpoint_implementation_transaction.py`:
  validate the active completed packet, run required validators, stage only
  completion-listed files inside active allowed write paths, and create one
  local Git commit.
- `python3 scripts/implementation_control/checkpoint_implementation_transaction.py --dry-run`:
  report the same checkpoint boundary without staging or committing.

`continue_implementation.py` is read-only. It does not stage, commit, push,
deploy, refresh source snapshots, or modify the upstream source repository at
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.

The resolver treats live `implementation_control/` records as authority. PRDs
and files under `ImplementationPlans/` remain route context only.

## Operating Procedure

For future website implementation packets, run the resolver first, inspect the
boundary, execute one bounded job, write completion and handoff records, run
the required validators, and checkpoint with `npm run checkpoint:implementation`.
The checkpoint command creates a local commit only; it does not push, deploy,
refresh upstream state, or broaden the active job.

`validate_implementation_control.py` is also read-only. A passing result means
the website-local control records are structurally coherent. It does not grant
scientific source authority, public claim approval, Git push approval,
Cloudflare deployment approval, or permission to mutate the upstream source
repository.

`checkpoint_implementation_transaction.py` is the only mutating script in this
directory. It refuses to push or deploy, and it refuses to commit before a valid
active completion record exists. Unrelated unstaged dirty files outside the
active packet are preserved. Unrelated staged files, or dirty files inside the
active allowed write scope but missing from the completion record, block the
transaction.
