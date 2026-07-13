---
name: technical-writing-quality-gate
description: Draft, revise, and evaluate source-grounded technical, scientific, system, governance, or public-facing prose for The AEther Flow Website with an explicit pass, repair, or block gate. Use when claim-bearing writing must be checked against upstream authority, website presentation evidence, audience needs, APA 7 citation requirements, or generic unsupported language.
---

# Technical Writing Quality Gate

## Purpose

Produce or review technical prose that is specific, audience-fit, and
proportional to the available evidence. Apply an explicit `pass`, `repair`, or
`block` decision before substantial claim-bearing writing is accepted or
published.

This skill is a writing and claim-discipline aid. It does not establish
scientific truth, prove source coverage, replace expert review, or grant
publication authority.

## When To Use

- Drafting or revising technical, scientific, architecture, governance,
  operational, release, or public website prose.
- Reviewing text that sounds generic, inflated, vague, or unsupported.
- Checking whether a document explains the system, mechanism, evidence,
  constraints, and remaining uncertainty clearly.
- Producing a `pass`, `repair`, or `block` decision before handoff or
  publication.

Do not use this skill as a substitute for physics review, mathematical
verification, security review, legal review, accessibility review, or the
repository's content, claim, provenance, curator, manifest, and build gates.

## Required Inputs

- Draft text, outline, prompt, or writing objective.
- Intended audience, purpose, and publication surface.
- Relevant source authority and current repository evidence.
- Required terminology, constraints, and citation standard.
- Optional target path and optional report path.

If the audience, purpose, or authority cannot be established from the request
and repository evidence, return `block` rather than inventing them.

## Evidence Hierarchy

Use this order:

1. Tracked sources, registries, governed records, and accepted review evidence
   in `/Volumes/P-SSD/AngryOwl/The-AEther-Flow` for scientific, mathematical,
   governance, and research-workflow claims.
2. Tracked website source, data, manifests, dossiers, tests, and validator
   output for reader-facing organization, presentation, and route behavior.
3. Generated reports, summaries, caches, and memory only as orientation until
   verified against tracked authority.

Website prose may explain, organize, promote, and link reviewed material. It
must not create, strengthen, or silently alter upstream claims.

## Outputs

- Revised or newly drafted prose when evidence is sufficient.
- Gate result of `pass`, `repair`, or `block`.
- Concise source-grounding notes and unsupported-claim findings.
- Validation performed, skipped checks, and remaining limitations.
- Optional advisory warning-pattern report.

## Required Workflow

1. Read the applicable repository instructions and identify the artifact,
   audience, purpose, publication surface, and working thesis.
2. Establish the source authority before drafting. Inspect tracked evidence
   rather than relying on memory or generated summaries.
3. Extract concrete facts such as actors, inputs, outputs, interfaces,
   mechanisms, workflows, constraints, failure modes, dependencies, and known
   uncertainty.
4. Rank defining facts before background. Preserve exact names, status terms,
   qualifications, and scope limits when they affect meaning.
5. Draft or revise with specific nouns, active verbs, visible mechanics, and
   causal sequence. Prefer evidence and mechanism over praise.
6. Check each material claim against the evidence. Keep supported claims,
   label necessary inference, repair overextension, and block claims that
   cannot be evaluated responsibly.
7. Apply the gate:
   - `pass` means the text is concrete, source-grounded, audience-fit, and
     proportional to the evidence.
   - `repair` means available evidence supports a direct correction to vague,
     inflated, poorly sequenced, or overextended prose.
   - `block` means required source facts, authority, audience, intent, or
     review evidence are missing.
8. For substantial or public-facing prose, read
   `references/system-writing-quality.md` and perform both a builder pass and a
   refuter pass.
9. Use APA 7 for citations to documents or materials. For local repository
   evidence, also list exact paths and line references when practical.
10. If a public Astro route or public claim-bearing source would change, stop
    until a live implementation-control packet authorizes the exact writes and
    approval gates.
11. Run the advisory warning matcher when useful, then run the repository
    validators appropriate to the affected surface.
12. Report the gate result, sources used, material repairs, validation, skipped
    checks, and unresolved risk.

## AEther Flow Claim Boundaries

Do not imply that:

- general relativity has been derived from explicit Æther or Æther-Flow
  substrate variables;
- exact effective closure proves the proposed ontology;
- the project has independent scientific or empirical validation beyond the
  accepted source position;
- a registry entry, validator pass, review receipt, generated artifact, AI
  output, or website page proves a physics claim;
- the governed AI research system is a scientific or mathematical proof
  authority;
- the effective package establishes a new independent low-energy non-GR
  observable sector.

When claim wording is publication-sensitive, inspect the current accepted
statement registry and public claim review evidence. Do not copy an older
qualification from memory.

## Advisory Warning Matcher

Run the standard-library helper against the files changed by the active task:

```bash
python3 .codex/skills/technical-writing-quality-gate/scripts/technical_writing_warning_gate.py \
  <TARGET_FILES>
```

Write a disposable report only when useful:

```bash
python3 .codex/skills/technical-writing-quality-gate/scripts/technical_writing_warning_gate.py \
  <TARGET_FILES> --report .tmp/technical-writing-quality-gate.md
```

Use `--strict` only when the active task explicitly requires warning hits to
return failure. This repository does not wire the matcher into `npm run
quality`.

Exit codes:

- `0` for readable inputs, including advisory warning hits without `--strict`;
- `1` for warning hits when `--strict` is supplied;
- `2` when no files match or a file cannot be read as UTF-8 text.

A clean report is not proof of factual correctness, source coverage,
originality, or human authorship. Every hit requires contextual review; the
configured words are warning signs, not banned terms.

## Validation Routing

Select the smallest relevant repository checks:

- Public claims or reviewed wording: `npm run validate:claims` and the active
  implementation packet's claim-review requirements.
- Source bundles or public content: `npm run validate:content`.
- Manifests or provenance: `npm run validate:manifests` and
  `npm run validate:provenance`.
- Source currency: `npm run validate:curator`.
- Public route output: `npm run build` and any packet-specific browser or
  accessibility review.
- Broad accepted changes: `npm run validate`.

Validator success establishes only the check it performs. State any scientific,
legal, security, or expert-review limitation separately.

## Failure Modes

- Rewriting vague prose into smoother vague prose.
- Treating style or warning matches as evidence of truth or authorship.
- Adding capabilities, outcomes, certainty, or authority absent from sources.
- Dropping exact qualifications that define the accepted claim boundary.
- Treating website presentation records as upstream scientific authority.
- Using generated summaries or memory without checking tracked evidence.
- Adding a strict repository-wide writing gate without explicit approval and
  false-positive evidence.

## Reference Files

- `references/system-writing-quality.md`: builder and refuter checklist.
- `examples/source-authority-repair.md`: website-specific repair example.

## Provenance

Adapted for The AEther Flow Website from the Sys4AI-dev technical-writing
quality-gate package at commit
`ef93cc008f1d3d91129e86bb4ce48b1435c17f6d`. The source package and script
hashes are recorded in implementation-control task `WI-20260713-002`.
