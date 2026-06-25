---
name: to-prd
description: Turn the current conversation and repository evidence into a local PRD for The AEther Flow Website without a fresh interview unless a blocking ambiguity remains.
disable-model-invocation: true
---

# To PRD

This skill synthesizes the current conversation and codebase understanding into
a product requirements document. Do not interview the user by default. Use what
has already been discussed, then ask only when a missing answer would make the
PRD materially wrong.

This local version is adapted for The AEther Flow Website. The default output is
a local Markdown file under `PRDs/`. Publish to an external issue tracker only
when that tracker and its label vocabulary are explicitly configured or the user
asks for it.

## Process

1. Explore the repo enough to understand current state. Use `CONTEXT.md`
   vocabulary, respect ADRs if present, and preserve the Source Authority
   Boundary.
2. Identify the highest useful implementation and testing seam. Prefer existing
   routes, layouts, components, scripts, manifest validators, or quality gates.
   Add new seams only when needed, and keep their count low.
3. If the seam is uncertain and the user is present, check it with one concise
   question before writing the PRD.
4. Write the PRD using the template below.
5. Save it as `PRDs/<short-slug>.md` unless the user provides another local
   path.
6. If an external issue tracker is configured, publish there too and apply the
   configured ready-for-agent triage label. If no tracker is configured, do not
   invent one.

## Website-specific constraints

- The website explains, describes, and promotes the upstream AEther Flow project.
- Authoritative scientific, mathematical, governance, and research-workflow
  claims remain in `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
- PRDs for website work should specify source provenance requirements when new
  public claims, downloadable artifacts, diagrams, or technical pages are in
  scope.
- PRDs should avoid embedding brittle file paths or code snippets unless a
  prototype produced a concise state model, schema, or reducer that captures a
  decision better than prose.

## PRD template

```md
# {Feature Name} PRD

## Problem Statement

The problem the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

1. As an <actor>, I want a <feature>, so that <benefit>.

Make this list extensive enough to cover the full feature surface.

## Implementation Decisions

- Modules, surfaces, or seams to build or modify.
- Interfaces or content boundaries that need to change.
- Technical clarifications from the conversation.
- Architectural decisions.
- Schema, manifest, route, or API contracts.
- Specific interactions.

Do not include specific file paths or code snippets by default; they can become
outdated quickly.

Exception: if a prototype produced a snippet that encodes a decision more
precisely than prose can, inline only the decision-rich part and note that it
came from a prototype.

## Testing Decisions

- What external behavior matters.
- Which routes, scripts, validators, or quality gates should be tested.
- Prior art for similar tests in the codebase.
- What should not be tested because it is implementation detail.

## Source Authority and Provenance

- Source project materials the feature depends on.
- Claim-status requirements.
- Reader-facing notices or provenance links required.

## Out of Scope

Things this PRD deliberately does not include.

## Further Notes

Additional useful context, risks, or follow-up questions.
```
