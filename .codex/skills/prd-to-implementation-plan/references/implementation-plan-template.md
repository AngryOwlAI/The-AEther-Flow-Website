# Implementation Plan Template

Use this template when writing the final implementation plan as a file or a
long-form chat response.

```markdown
# Implementation Plan: <Feature Name>

## Source PRD
- Source: <path, issue, selection, or pasted content>
- Generated for: Codex app and Codex IDE
- Planning status: <Ready | Ready with assumptions | Blocked>

## Product Summary

<Summarize the goal, users, jobs to be done, primary flows, and success
criteria. Preserve uncertainty and do not invent product behavior.>

## Repository Context

- Frameworks and languages:
- Package manager and build system:
- Existing related routes, components, services, models, tests, scripts, or
  docs:
- Relevant repository instructions:
- Discovered validation commands:

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | <text> | <evidence> | <coding/release/etc.> |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Blocking | <question> | <impact> |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| REQ-001 | <behavior> | <files, routes, APIs, data, docs> | TASK-01 | <commands/checks> |

## Proposed Technical Approach

<Describe the smallest maintainable architecture that satisfies the PRD. Include
data model, API or contract changes, UI and routing changes, state management,
accessibility, error handling, loading and empty states, security/privacy,
observability, rollout, and rollback where relevant.>

## Implementation Phases

1. <Phase title>: <goal, scope, dependencies, risk>
2. <Phase title>: <goal, scope, dependencies, risk>

## Codex Task Packets

<Paste or link task packets. Each task must have Goal, Context, Constraints,
Implementation notes, Acceptance criteria, Validation, and Done when.>

## Validation Plan

- Static checks:
- Unit tests:
- Integration tests:
- E2E or browser checks:
- Build:
- Manual QA:
- Documentation or manifest validation:

Use only discovered commands. If a command is unknown, write `Discover and
document the correct command before coding`.

## Security, Privacy, and Reliability Notes

- Data validation:
- Permissions and access control:
- Abuse cases and rate limits:
- Privacy or sensitive data concerns:
- Failure modes and recovery:
- Observability:

## Rollout and Rollback Plan

- Rollout:
- Migration/backfill:
- Feature flag or staged release:
- Rollback:
- Monitoring:

## Out of Scope

- <Explicit exclusions or deferred work.>

## Final Review Checklist

- [ ] Every PRD requirement is mapped to a task or explicitly deferred.
- [ ] Every task has acceptance criteria.
- [ ] Every task has validation guidance.
- [ ] Risky changes have review or rollback notes.
- [ ] The plan avoids direct coding unless implementation was requested.
- [ ] Commands were discovered from the repository or marked unknown.
- [ ] Product questions are separated from implementation decisions.
```
