# PHASE-02 Fixture Corpus

This directory contains deterministic, project-neutral fixtures for the
complete Phase-02 implementation-plan contract and tooling gate.

`coverage-matrix.json` is the machine-readable authority for corpus coverage,
expected record profiles or reason codes, base-to-negative relationships, and
the SHA-256 of every generated data file. It covers:

- all seven source classes;
- all ten supported schema versions;
- all plan phases and task lifecycle statuses;
- all receipt dispositions and execution outcomes;
- all provider outcomes;
- all supersession terminal and reason paths;
- all amendment operations, normalization statuses, and selection outcomes;
- structural/content-hash and cross-record semantic adversaries.

Every file under `records/negative/` differs from its named positive base at
exactly one JSON path. One deliberate fault may produce several downstream
diagnostics, but no negative file combines independent mutations.

Generated JSON and text files are maintained by:

```text
python3 skills/implementation-plan-goal/scripts/build_phase02_fixture_corpus.py --write
```

Do not edit generated fixture data by hand. The normal read-only gate is:

```text
python3 skills/implementation-plan-goal/scripts/build_phase02_fixture_corpus.py --check
python3 -m unittest discover -s skills/implementation-plan-goal/tests -p "test_phase02_fixture_corpus.py" -v
```

The corpus is validation evidence only. It performs no plan-state mutation,
task reservation, provider call, recovery action, migration, or external
effect.
