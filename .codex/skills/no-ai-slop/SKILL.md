---
name: no-ai-slop
description: Prevent low-quality AI-generated artifacts by applying a pass/repair/block quality gate and disciplined writing support. Use when the user asks to prevent AI slop, avoid low-quality generated writing, says No AI Slope or No AI Slop, or when creating or reviewing substantial or claim-bearing artifacts such as documentation, summaries, plans, tests, code explanations, UI copy, design rationale, handoffs, and public-facing content where evidence, audience fit, or source authority matters.
---

# No AI Slop

## Purpose

Apply a quality-control gate before finalizing substantial agent-created
artifacts. Optimize for useful, grounded, audience-fit output rather than
fluent volume.

Use this skill as a quality gate first and a writing aid second. Improve the
artifact silently when the repair is straightforward. Stop and report the
failure when the artifact lacks evidence, authority, intent, or enough context
to proceed honestly.

## Core Contract

Before publishing, committing, handing off, or finalizing a substantial or
claim-bearing artifact, classify it as:

- `pass`: specific, grounded, useful, and fit for handoff.
- `repair`: flawed but fixable without new evidence, authority, or user intent.
- `block`: missing evidence, authority, thesis, audience, constraints, or
  project context needed for a truthful artifact.

Do not use numeric slop scores. They imply false precision.

Surface the gate result only when it affects the outcome: a block, a material
repair, a user-requested audit, high-stakes work, public-facing work, scientific
or governance claims, legal/medical/financial risk, or source-authority
sensitivity.

## Required Workflow

1. Identify the artifact type, audience, purpose, and working thesis. Infer the
   thesis from the user request, source files, PRD, issue, or nearby repository
   context when possible. If no credible thesis can be inferred for substantial
   writing, return `block`.
2. Check the artifact against the quality gate. Read
   `references/quality-gate-checklist.md` for substantial, public-facing,
   research, governance, or claim-bearing work.
3. Repair ordinary weaknesses directly: generic phrasing, filler structure,
   unsupported polish, weak audience fit, vague claims, excessive length, or
   missing limitations that can be fixed from available evidence.
4. Block when repair would require inventing facts, strengthening claims,
   guessing authority, hiding uncertainty, or pretending evidence exists.
5. Produce the smallest artifact that fully satisfies the task. Length must be
   justified by complexity, traceability, user need, or review value.

## Builder And Refuter Pass

For serious, public-facing, scientific, governance, or claim-bearing work, use
two passes:

- Builder pass: improve clarity, structure, specificity, examples, and
  completeness.
- Refuter pass: look for hallucinations, unsupported claims, weak logic,
  audience mismatch, review burden, missing limitations, and authority drift.

For small routine tasks, use a compact single-pass gate.

## Evidence And Citations

Require traceable evidence for factual claims. Evidence can be repository
files, validated command output, source documents, official documentation,
tests, or user-provided material. Remove or mark uncertainty in claims that
cannot be verified.

Use APA 7 format when a formal document or public-facing explanatory artifact
cites documents or materials and the repository requires formal citations. Do
not force APA 7 into commit messages, short status updates, code comments, or
compact task packets unless the user or repository explicitly requires it.

## Warning Signs

Treat these as slop risk indicators, not rigid banned words:

- Generic transitions such as "In conclusion" that add no reasoning.
- Unsupported superlatives such as "robust", "seamless", "powerful", or
  "comprehensive".
- Corporate abstractions such as "unlock value" or "drive innovation" without
  concrete mechanism.
- Predictable bullet templates that do not reflect the task.
- Polished summaries with no sources, constraints, tradeoffs, or next action.
- Code, tests, or plans that increase review burden without clear necessity.

Repair by adding concrete evidence, constraints, decisions, limitations, or by
removing the sentence.

## Role-Specific Checks

- Coding agent: verify necessity, local fit, maintainability, tests, error
  handling, security implications, and whether comments or explanations make
  unsupported claims.
- System engineer: verify interfaces, failure modes, operational assumptions,
  observability, rollout, rollback, and long-term reliability.
- Analyst: verify evidence, denominators, methods, uncertainty, decision
  relevance, and whether the conclusion follows from the data.
- Designer: verify user task fit, accessibility, constraints, interaction
  states, content hierarchy, and whether design rationale is concrete rather
  than aesthetic filler.
- Writer or summarizer: verify thesis, audience, source discipline,
  specificity, exclusions, limitations, and minimum useful length.

This skill does not replace tests, type checks, security review, accessibility
checks, scientific validation, or repository-specific validators.

## AEther Flow Website Authority Boundary

For The AEther Flow Website, preserve the source-authority boundary. The
website may explain, organize, and link reviewed upstream material. It must not
create, strengthen, or silently alter scientific, mathematical, governance, or
research-workflow claims from `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.

Prefer exact claim-status language when it matters:

- `proposal-only`
- `draft/control`
- `source-extension`
- `fail-closed`
- `frozen negative`
- `no MetricData(E)`
- `no g_eff`
- `no downstream GR promotion`

When source authority is unclear, return `block` or write only explicitly
scaffold-level copy.

## Reference Files

- `references/quality-gate-checklist.md`: detailed pass/repair/block checklist.
- `examples/source-authority-repair.md`: compact AEther-style repair example.
