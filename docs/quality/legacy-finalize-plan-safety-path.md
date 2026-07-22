# Legacy `finalize-plan` safety path

## Purpose

The website façade now provides a supported terminalization boundary for
installed implementation-plan-goal 0.1.0 runs. It replaces untracked SQLite
mutation with a canonical completion proof, a hash-bound operator report, and
one revision-checked SQLite mutation. It is a Phase 00 safety repair; it is not
the recursive relay implementation and does not lift the Phase 08 activation
freeze.

The command never emits or reuses the unexplained historical event names
`plan_completion_candidate_confirmed` or
`plan_terminal_completion_recorded`. Successful finalization appends one
`plan_completion_receipt` journal entry with receipt schema
`website.legacy-plan-completion-receipt.v1`.

## Preconditions

`prepare-finalize-plan` fails unless all of the following are true:

- the requested plan revision and website-control SHA-256 are current;
- the caller is the coordinator recorded by the accepted adapter session;
- the last task invocation is finalized and the deterministic scheduler returns
  `completion_candidate`;
- the installed canonical completion-report builder returns `complete`;
- task receipts, dependency completion, profile evidence, repository topology,
  and normalized validator evidence are internally consistent;
- every provider intent is `returned`;
- there is no active task, plan lease, or outer-goal lease; and
- repository binding and topology still match the accepted session.

The legacy lifecycle releases the final task's plan and outer-goal leases in
the task-receipt transaction before a coordinator can observe a completion
candidate. `finalize-plan` therefore does not steal, expire, or synthesize a
lease. Its `BEGIN IMMEDIATE` transaction rechecks that both leases remain
absent and makes `terminal_complete` impossible while a lease or active task
exists. This is the installed profile's atomic lease-closure boundary.

## Prepare the immutable report

First obtain the exact plan revision and website-control hash from the read-only
status command. Then run:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  scripts/implementation_control/continue_plan_goal.py \
  prepare-finalize-plan \
  --plan-id PLAN-ID \
  --expected-plan-revision REVISION \
  --expected-control-sha256 CONTROL-SHA256 \
  --current-holder-thread-id COORDINATOR-THREAD-ID
```

The canonical JSON response contains `completion_report` and
`completion_report_sha256`. Store only the nested `completion_report` as a
repository-relative JSON file, normally below the ignored
`.local/sys4ai/implementation-plan-goal/` tree. Preserve its reported SHA-256.
Preparing the report is read-only.

## Finalize

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  scripts/implementation_control/continue_plan_goal.py \
  finalize-plan \
  --plan-id PLAN-ID \
  --expected-plan-revision REVISION \
  --expected-control-sha256 CONTROL-SHA256 \
  --current-holder-thread-id COORDINATOR-THREAD-ID \
  --completion-report .local/sys4ai/implementation-plan-goal/reports/REPORT.json \
  --completion-report-sha256 REPORT-SHA256
```

The command reconstructs the report from current canonical state and requires
byte-equivalent canonical content before mutation. In one SQLite transaction it
sets `phase=terminal_complete`, sets `evaluation=met`, records the terminal
reason, and appends the full immutable report and its hash to a new
`plan_completion_receipt` journal entry. The adapter session is then projected
to `terminal_complete`; the SQLite journal remains canonical if that secondary
projection needs reconciliation.

Repeating the exact request with the original report and original expected
revision returns `already_terminal` without another write. A different report,
revision, control hash, holder, repository identity, open or ambiguous intent,
active invocation, failed completion proof, or lease fails closed.

## Authority boundary

Terminal completion grants no stage, commit, branch, worktree, push, deploy,
publication, upstream-write, external-provider, or scientific-claim authority.
Historical plan, goal, receipt, intent, lease, event, and backup bytes remain
append-only evidence.

## References

The AEther Flow Website. (2026, July 22). *Plan-native recursive discussion
relay implementation plan* [Implementation plan].

The AEther Flow Website. (2026, July 22). *Terminalization-event provenance
audit* [Control audit].
