---
name: prototype
description: Build a throwaway prototype for The AEther Flow Website to answer one concrete logic, state, data-shape, or UI-design question before production implementation.
disable-model-invocation: true
---

# Prototype

A prototype is throwaway code that answers a question. The question decides the
shape.

This local version is adapted for The AEther Flow Website. Preserve the
Source Authority Boundary from `CONTEXT.md`: prototype copy, diagrams, and
technical claims must be derived from reviewed source material, fixtures, or
clearly marked placeholders. Do not use a prototype to invent or silently change
scientific, mathematical, governance, or research-workflow claims from the
upstream source project.

## Pick a branch

Identify which question is being answered from the user's prompt, surrounding
code, or by asking if the user is available:

- "Does this logic / state model feel right?" -> read `LOGIC.md`.
- "What should this look like?" -> read `UI.md`.

The two branches produce different artifacts. If the question is genuinely
ambiguous and the user is not reachable, default to whichever branch better
matches the surrounding code: a script, manifest, or validation concern usually
means logic; a page, layout, or component usually means UI. State the assumption
at the top of the prototype.

## Rules that apply to both

1. Mark the prototype as throwaway from day one.
2. Locate it close to the code or page being explored, using names that make its
   temporary status obvious.
3. Provide one command or URL to run it, using this repo's existing tooling.
4. Use in-memory state by default. If persistence is the subject being tested,
   use scratch files with clear prototype names.
5. Skip polish. Do not add production abstractions, broad error handling, or
   tests unless the prototype cannot run without a minimal check.
6. Surface the relevant state or variant after each action or switch.
7. Delete the prototype or absorb the validated decision once it has answered
   the question.

## Repository-specific guidance

- For website UI questions, prefer Astro pages, layouts, and components already
  in `src/`.
- For manifest, source-ingestion, validation, or quality-gate questions, prefer
  the existing Python and Bash tooling in `scripts/` and `tests/`.
- Do not leave prototype routes in production-bound output. Remove them before
  deployment or explicitly gate them with a project-approved development-only
  mechanism.
- If a prototype resolves durable terminology, update `CONTEXT.md`.
- If it resolves a hard-to-reverse, surprising, trade-off-driven architectural
  decision, propose an ADR in `docs/adr/`.

## When done

The answer is the only thing worth keeping from a prototype. Capture the
question and conclusion in the place with the lowest durable weight: a commit
message, issue, ADR, or `NOTES.md` next to the prototype. If the user is
available, ask them to confirm what the prototype taught before deleting or
absorbing it.
