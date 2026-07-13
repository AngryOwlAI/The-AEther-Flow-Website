# Technical Writing Quality Gate

Project-local workflow for drafting, revising, and reviewing source-grounded
technical prose with an explicit `pass`, `repair`, or `block` result.

## Canonical Surface

The canonical website package is:

```text
.codex/skills/technical-writing-quality-gate/
```

There is no `.agents` compatibility shim and no website-local `skill.yaml`.

## Project Fit

The skill preserves The AEther Flow Website's authority boundary:

1. Upstream tracked sources and governed records own scientific,
   mathematical, governance, and research-workflow claims.
2. Website files own reader-facing presentation and route behavior.
3. Generated reports and memory are orientation until verified.

The bundled Python script flags generic marketing and unsupported-benefit
patterns. It is advisory by default, standard-library-only, and intentionally
outside `npm run quality`.

## Package Contents

- `SKILL.md`: executable workflow and authority contract.
- `AGENTS.md`: maintenance rules.
- `agents/openai.yaml`: Codex discovery metadata.
- `references/system-writing-quality.md`: detailed review checklist.
- `examples/source-authority-repair.md`: project-specific repair example.
- `scripts/technical_writing_warning_gate.py`: optional proxy checker.

## Quick Check

```bash
python3 .codex/skills/technical-writing-quality-gate/scripts/technical_writing_warning_gate.py \
  docs/example.md
```

Add `--strict` only when the active task explicitly authorizes warning hits to
fail. A clean result does not prove correctness, coverage, originality, or
human authorship.
