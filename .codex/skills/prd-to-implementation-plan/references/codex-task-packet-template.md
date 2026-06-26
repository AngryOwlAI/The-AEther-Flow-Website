# Codex Task Packet Template

Use this template for each implementation task. Keep every task scoped to one
branch or one draft PR where feasible.

```markdown
## Task N: <short action-oriented title>

### Goal
<One specific outcome.>

### Context
- PRD requirements: <REQ IDs>
- Relevant files or directories: <paths or @file references when known>
- Existing patterns to follow: <brief notes>

### Constraints
- <What not to change>
- <Architecture, dependency, style, or safety constraints>

### Implementation notes
- <Suggested steps, not overly prescriptive>

### Acceptance criteria
- [ ] <Observable criterion>
- [ ] <Observable criterion>

### Validation
- <Exact lint, typecheck, unit, integration, e2e, build, or manual commands when discovered>
- If a command is unknown, write `Discover and document the correct command before coding`.

### Done when
- <Tests pass, behavior works, docs updated, PR ready>
```

## Packet Quality Rules

- Make the task self-contained for the Codex app, IDE extension, or CLI.
- Include setup assumptions and repository paths when known.
- Prefer vertical slices that can be reviewed independently.
- Include source PRD requirement IDs and validation commands.
- State any dependency on earlier tasks.
- Mark tasks that can run in parallel.
- Include the expected output, branch or PR scope, and review checklist when
  useful.
- For Codex IDE, include `@file` references when specific files are known.
- Include a short follow-up prompt for reviewing the local diff when helpful.
