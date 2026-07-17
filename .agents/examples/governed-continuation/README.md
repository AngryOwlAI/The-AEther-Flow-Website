# Governed Continuation Portable Examples

These neutral fixtures exercise the portable protocol without private paths,
real tokens, network access, AEther terminology, or project-specific authority.
They are copied into temporary directories by the end-to-end tests; the source
fixtures remain reusable and non-authoritative.

| Fixture | Bounded behavior | Claim boundary |
| --- | --- | --- |
| `minimal-software-project` | Change one declared source value and run one approved local check. | Proves only the bounded value fixture. |
| `documentation-project` | Update one generated guide from one canonical source note. | Proves only the declared source-to-derivative match. |
| `research-note-project` | Update one traced note while domain evidence remains indeterminate. | Does not establish the research hypothesis. |

Additional examples cover:

- bootstrap-required and registered-profile setup under
  `skills/agentjob-control/examples/bootstrap-required.md`;
- existing-control conformance under
  `skills/agentjob-control/examples/existing-control-adapter.md`;
- one bounded execution under `skills/continue/examples/portable-example.md`;
- launch and manual handoff under `skills/continue-goal/examples/`;
- one generation worker under
  `skills/continue-implementing-goal/examples/portable-example.md`;
- crash reconciliation in
  `docs/skills/GOAL_RELAY_RECOVERY_RUNBOOK.md`.

Validate the fixtures and run their six end-to-end cases with:

```bash
python3 scripts/skills/validate_control_protocol.py --examples
```

Authority status: fixture files, generated control records in temporary tests,
test receipts, and this index are non-authoritative examples. In a target
project, only its activated control records, configuration, policy, and local
goal state can authorize work.
