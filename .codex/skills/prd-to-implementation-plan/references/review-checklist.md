# Final Plan Review Checklist

Use this checklist before presenting or writing the final implementation plan.

## Completeness

- [ ] The source PRD path, issue, pasted content, or selection is identified.
- [ ] Planning status is `Ready`, `Ready with assumptions`, or `Blocked`.
- [ ] Every PRD requirement is mapped to at least one task or explicitly
  deferred.
- [ ] Functional and non-functional requirements are both represented.
- [ ] Explicit exclusions and constraints are preserved.
- [ ] Open questions are classified by impact.

## Engineering Fit

- [ ] Repository architecture was inspected before planning.
- [ ] Existing patterns are preferred over new abstractions.
- [ ] New dependencies, migrations, or broad refactors are justified or avoided.
- [ ] Likely affected files and directories are named when known.
- [ ] Data, API, UI, accessibility, error handling, and state implications are
  covered when relevant.
- [ ] Security, privacy, reliability, observability, rollout, and rollback are
  considered.

## Task Packet Quality

- [ ] Every task has `Goal`, `Context`, `Constraints`, `Implementation notes`,
  `Acceptance criteria`, `Validation`, and `Done when`.
- [ ] Tasks are small enough for one branch or one draft PR where feasible.
- [ ] Tasks are ordered by dependency and mark parallelizable work.
- [ ] Each task references PRD requirement IDs.
- [ ] Validation guidance uses discovered commands or explicitly says to
  discover the command before coding.
- [ ] Risky tasks include review or rollback notes.

## Codex Surface Fit

- [ ] Codex app tasks are self-contained and do not depend on open editor state.
- [ ] Codex IDE tasks use `@file` references when specific files are known.
- [ ] Task prompts require validation summaries before completion.
- [ ] The plan does not perform direct coding unless the user asked to code.

## Source Authority

- [ ] For The AEther Flow Website, upstream authority is preserved for
  scientific, mathematical, governance, and research-workflow claims.
- [ ] GitHub or source links are treated as provenance when appropriate.
- [ ] Internal website routes remain the primary reader journey unless a link is
  explicitly a source or provenance link.
