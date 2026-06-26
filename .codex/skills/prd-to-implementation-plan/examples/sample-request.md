# Sample Requests

Use these as examples of how a user or Codex prompt can invoke the skill.

## Codex App

```text
Use $prd-to-implementation-plan on PRDs/source-release-page.md.
Create docs/implementation-plans/source-release-page-implementation-plan.md
and docs/implementation-plans/source-release-page-task-packets.md.
Keep tasks small enough for separate draft PRs, use repository-discovered
validation commands, and preserve The AEther Flow Website source-authority
boundary.
```

## Codex IDE Extension

```text
Use $prd-to-implementation-plan on the selected PRD text.
Return the plan in chat only. Use @file references for likely implementation
areas where you can identify them, and include a follow-up prompt I can use to
review the local diff after the first implementation task.
```

## Codex CLI

```text
Use $prd-to-implementation-plan for docs/prds/profile-editing.md.
Write the implementation plan and task packets under
docs/implementation-plans/. First inspect AGENTS.md, package.json, existing
routes, and tests. Do not modify application code.
```
