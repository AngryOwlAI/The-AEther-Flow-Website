# No AI Slop Quality Gate

Use this checklist for substantial, public-facing, research, governance, or
claim-bearing artifacts.

## Intake

- What is the artifact type?
- Who is the audience?
- What must the reader or maintainer understand afterward?
- What is the working thesis or purpose?
- What source evidence is available?
- What should be excluded?

If audience, purpose, or thesis cannot be inferred for substantial writing,
return `block`.

## Pass Criteria

An artifact can pass when:

- It says something specific and useful.
- Factual claims are traceable to evidence or explicitly marked uncertain.
- The level of detail matches the audience and task.
- The structure follows the material rather than a generic template.
- Limitations, assumptions, and exclusions are visible where they matter.
- The artifact reduces review burden rather than shifting hidden work to the
  user or maintainer.
- The final human-facing result is no longer than needed.

## Repair Criteria

Repair when the available context supports a truthful improvement:

- Replace generic claims with concrete facts, constraints, or examples.
- Remove filler introductions, padded conclusions, and repetitive bullets.
- Add missing caveats, assumptions, or scope boundaries from known context.
- Convert vague recommendations into testable next steps.
- Reorganize around audience tasks, not model-default sections.
- Tighten code comments, docs, plans, or UI copy so they explain actual
  behavior and decisions.

## Block Criteria

Block instead of polishing when:

- A factual claim lacks evidence and cannot be verified from available context.
- The artifact would need to invent sources, tests, user intent, or authority.
- Scientific, mathematical, governance, legal, medical, financial, or
  source-authority claims are unclear or unsupported.
- The requested volume would create many low-value artifacts.
- The artifact is mostly fluent restatement with no thesis, decision, or reader
  utility.
- The agent cannot distinguish what is proven, proposed, blocked, failed, or
  next.

## Serious-Work Refuter Pass

Ask:

- What claim would a knowledgeable reviewer challenge first?
- What sentence sounds polished but is not evidenced?
- What would be expensive for a human to verify later?
- What uncertainty is being hidden by confident language?
- What source, validator, test, or example would change the conclusion?
- Does the artifact preserve the project authority boundary?

Return `repair` when the answer is fixable now. Return `block` when it requires
new evidence, user intent, or source-authority inspection.
