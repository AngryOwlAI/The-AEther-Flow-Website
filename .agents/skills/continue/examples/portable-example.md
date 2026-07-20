# Portable Example: One Software Repair Transaction

## Scenario

A small project has one active task to correct a formatting defect in
`src/report.py`. Its activated AgentJob permits reading that file and its
focused test, writing only `src/report.py`, and running one structured test
command. Network and external effects are denied.

## Invocation

```text
Use $continue with project_root=<PROJECT_ROOT> and task_id=TASK-001.
```

## Expected transaction

1. Read-only preflight validates configuration, activation, repository
   identity, and the before fingerprint.
2. The existing job and execution-role binding are reused.
3. Runtime authority is compiled without widening paths or commands.
4. Exactly one repair operation writes `src/report.py` and runs the approved
   focused test.
5. Post-execution validation checks the changed-path allowlist, expected
   output, command evidence, claim boundary, and checkpoint receipt.
6. One completion is finalized and the structured result reports one executed
   AgentJob.

## Protected alternatives

- If configuration is absent, return `bootstrap_required` with no writes.
- If another path changes, report validation failure and do not claim success.
- If publication is requested but not authorized, stop at the human gate.
- If the task is already complete, return `no_action` without a fake
  completion or empty commit.

## Adaptation notes

Replace the example paths, task ID, command, role, validators, and checkpoint
provider with target-project values. Preserve the one-job and no-thread rules.

## Authority status

This example and any generated fixture records are non-authoritative. In a
target project, the activated AgentJob, policy, human gates, and project-local
records decide what may execute.
