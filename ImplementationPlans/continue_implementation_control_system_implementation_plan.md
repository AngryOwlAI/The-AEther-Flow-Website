# Implementation Plan: Continue Implementation Control System

## Source PRD

- Source: `PRDs/continue-implementation-control-system-prd.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

The feature adds a website-local `continue implementation` system for The
AEther Flow Website. It mirrors the useful control invariants of the upstream
`continue research` workflow while staying strictly local to the website repo:
live state outranks stale plans, Codex executes at most one bounded packet per
invocation, high-risk work requires explicit approval, validation is part of the
normal repo health gate, and checkpointing creates a local Git commit only for
allowed packet files.

Success means future implementation sessions can run a deterministic resolver,
inspect the next packet, execute one bounded website task, validate the result,
record completion and handoff evidence, and commit the approved packet without
mutating the upstream research repo or unrelated user changes.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript components and data
  modules, Python repository tooling, Markdown documentation.
- Package manager and build system: `npm` scripts around Astro and Python
  validators.
- Existing related surfaces:
  - `AGENTS.md` defines project commands, source-authority boundary, and
    definition of done.
  - `CONTEXT.md` defines website vocabulary and Source Authority Boundary.
  - `ImplementationPlans/` and `PRDs/` already hold planning artifacts.
  - `scripts/` contains deterministic validators and manifest refresh tools.
  - `tests/` contains Python test coverage for validators and quality gates.
  - `docs/architecture/website-feature-and-functionality.md` records current
    architecture, validation gates, maintainer workflow, and revamp contract.
- Relevant repository instructions:
  - Upstream source project files remain authoritative for scientific,
    mathematical, governance, and research-workflow claims.
  - Website files may explain and organize reviewed material but must not
    silently strengthen source claims.
  - Relevant public manifests must be updated and validated after page, source,
    or asset changes.
  - Do not deploy unless explicitly authorized.
- Discovered validation commands:
  - `npm run validate`
  - `npm run quality`
  - `npm run validate:manifests`
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:layout`
  - `npm run validate:svg`
  - `npm run validate:provenance`
  - `npm run validate:curator`
  - `npm run validate:cloudflare`
  - `npm run build`
  - `python3 -m pytest`
  - `git diff --check`

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | Implementation-control records can use YAML parsed by Python standard-library-adjacent tooling already present in scripts or a small local parser pattern. | Existing website scripts are Python-based and the upstream resolver uses deterministic YAML records. | Coding |
| ASM-002 | Planning assumption | The initial bootstrap task may commit the PRD, implementation plan, scripts, tests, docs, package script updates, and implementation-control records as one bounded packet. | The user explicitly selected bootstrap as the first live authority. | Checkpoint |
| ASM-003 | Implementation detail | Commit-message format can be a deterministic concise website-local message unless the user later specifies a template. | Existing website repo has no implementation-control commit template. | Checkpoint implementation |
| ASM-004 | Planning assumption | The existing dirty untracked file outside this plan should not be touched by implementation-control bootstrap work unless the user later includes it. | Repository status showed unrelated untracked work; user required preservation of unrelated dirty files. | Coding and checkpoint |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Implementation detail | Should future implementation task IDs reserve a prefix beyond `WI-YYYYMMDD-NNN` for specialized work families? | Can be decided later without blocking bootstrap. |
| Q-002 | Implementation detail | Should checkpoint commits use `codex:` or another prefix? | Can be decided while implementing checkpoint script. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| REQ-001 | Upstream project remains read-only for website continuation. | Resolver, validator, checkpoint, docs, task schema. | TASK-01, TASK-02, TASK-03, TASK-04 | `python3 -m pytest`, `npm run validate:implementation-control` |
| REQ-002 | Live implementation state outranks plans and memory context. | `implementation_control/program_state.yaml`, resolver rules, docs. | TASK-01, TASK-02 | `python3 -m pytest` |
| REQ-003 | Lightweight task/job/completion/handoff control model exists. | `implementation_control/**`, validator tests. | TASK-01, TASK-03 | `npm run validate:implementation-control` |
| REQ-004 | Resolver emits deterministic JSON and supports summary output. | `scripts/implementation_control/continue_implementation.py`, package scripts, tests. | TASK-02 | `python3 -m pytest`, `npm run continue:implementation -- --summary` |
| REQ-005 | Continuation executes at most one bounded packet per invocation. | Resolver boundary model, task/job docs, validator. | TASK-01, TASK-02, TASK-03 | `python3 -m pytest` |
| REQ-006 | High-risk packets require explicit approval gates. | Task/job schema, validator, docs, tests. | TASK-01, TASK-03 | `npm run validate:implementation-control` |
| REQ-007 | Implementation-control validation is part of repo health. | `validate_implementation_control.py`, `package.json`, tests. | TASK-03 | `npm run validate:implementation-control`, `npm run validate` |
| REQ-008 | Checkpoint validates, stages allowed files, and commits locally. | `checkpoint_implementation_transaction.py`, tests, docs. | TASK-04 | `python3 -m pytest`, targeted checkpoint dry-run or fixture tests |
| REQ-009 | Bootstrap starts from explicit initial local task. | Initial `implementation_control/tasks/WI-*` records and handoff. | TASK-01, TASK-05 | `npm run validate:implementation-control` |
| REQ-010 | Source Authority Boundary is preserved. | Docs, approval gates, validator, checkpoint path checks. | TASK-01, TASK-03, TASK-04, TASK-05 | `npm run validate`, `git diff --check` |
| REQ-011 | Future sessions can use the system without guessing. | `scripts/implementation_control/README.md`, architecture docs, task packet. | TASK-05 | `git diff --check`, `npm run validate` |
| NFR-001 | No unnecessary dependencies are added. | Python scripts and existing npm commands. | TASK-02, TASK-03, TASK-04 | Code review, `npm install` not required |
| NFR-002 | Resolver and validator outputs are deterministic. | Script tests and stable JSON. | TASK-02, TASK-03 | `python3 -m pytest` |
| NFR-003 | Unrelated user work is preserved. | Checkpoint dirty-state logic and tests. | TASK-04 | `python3 -m pytest` |
| NFR-004 | No push, deploy, upstream refresh, or invented completion content. | Checkpoint restrictions, docs, tests. | TASK-04, TASK-05 | `python3 -m pytest`, code review |

## Proposed Technical Approach

Add a small `implementation_control/` authority layer and a narrow
`scripts/implementation_control/` tooling layer.

The control records should be simple YAML and Markdown files with explicit
fields for status, active task, latest handoff, approval gates, allowed read
paths, allowed write paths, required validators, stop conditions, completion
evidence, and next recommended action. This is intentionally smaller than the
upstream research-control schema. It keeps the invariant that live state comes
first without importing physics role routing.

The resolver should be read-only. It should parse implementation-control state,
resolve the latest handoff, inspect whether an active job exists, classify the
boundary, and print a deterministic JSON context packet. Summary mode should
render the same information for a human operator.

The validator should fail closed. It should catch missing records, mismatched
task/job/handoff IDs, invalid status transitions, missing approval disposition
for high-risk gates, unknown validators, absolute local-path leaks in public
records, invalid allowed-write patterns, and attempts to place upstream paths in
write allowlists.

The checkpoint script should be the only planned mutating command in the
control toolchain. It should verify the active job and completion record, run
the required validators, inspect Git status, stage only allowed paths, create a
local commit, and refuse ambiguous dirty-state conditions. It should not push,
deploy, refresh upstream, create completion evidence, or alter files outside
the job allowlist.

Package scripts should expose:

- `npm run continue:implementation`
- `npm run validate:implementation-control`

`npm run validate` should include `validate:implementation-control` after
existing website content/provenance checks and before `npm run build`.

No public UI, route, asset, or manifest change is required for the bootstrap
except package-script validation wiring. The system is primarily maintainer and
agent infrastructure.

## Implementation Phases

1. Control Records And Schema: create the bootstrap authority records, define
   the minimal schema in docs, and make the initial task explicit.
2. Resolver: implement read-only continuation resolution and package command.
3. Validator: implement fail-closed implementation-control validation and add
   it to normal validation.
4. Checkpoint: implement narrow validation, staging, and local commit behavior.
5. Documentation And Closeout: document operating procedure, validate the
   full system, and checkpoint the bootstrap packet.

## Codex Task Packets

See `ImplementationPlans/continue_implementation_control_system_task_packets.md`.

## Validation Plan

- Static checks:
  - `git diff --check`
- Unit tests:
  - `python3 -m pytest`
- Focused implementation-control validation:
  - `npm run validate:implementation-control`
- Resolver smoke checks:
  - `npm run continue:implementation`
  - `npm run continue:implementation -- --summary`
- Build and full repository validation:
  - `npm run validate`
- Manual QA:
  - Inspect generated resolver JSON and summary output for active task, latest
    handoff, boundary, allowed paths, validators, approval gates, and next
    action.
- Documentation or manifest validation:
  - No public manifest regeneration is expected unless implementation later
    changes public routes or assets.

## Security, Privacy, and Reliability Notes

- Data validation: YAML records must be parsed deterministically and validated
  fail-closed. Missing fields should block rather than infer authority.
- Permissions and access control: the system is local repository tooling. Its
  control boundary is allowed paths plus explicit approval gates, not external
  authentication.
- Abuse cases and rate limits: not applicable to runtime users because this is
  local maintainer tooling.
- Privacy or sensitive data concerns: records should avoid absolute local
  paths in public-facing contexts and should not include secrets.
- Failure modes and recovery: validation failure should leave files unstaged;
  checkpoint failure should not partially commit; ambiguous dirty state should
  block with named paths.
- Observability: resolver JSON, completion records, handoffs, validation output,
  and Git commit history provide audit evidence.

## Rollout and Rollback Plan

- Rollout:
  - Land the bootstrap control system in one local commit after validation.
  - Use the resolver for the next continuation packet only after the bootstrap
    commit exists.
- Migration/backfill:
  - Do not backfill old PRDs and plans as completed control tasks.
  - Future packets may reference older plans as route context.
- Feature flag or staged release:
  - Not required; this is maintainer tooling, not public runtime behavior.
- Rollback:
  - Revert the bootstrap commit if the system is rejected.
  - Since no public routes or upstream source files are changed, rollback risk
    is limited to local tooling and control records.
- Monitoring:
  - Normal `npm run validate` will catch broken control records after the
    validator is integrated.

## Out of Scope

- Upstream research-control mutation.
- Full physics role registry or DDR model.
- Cloudflare deployment.
- Remote push.
- Public page rewrites.
- Public route retirement or navigation changes.
- Public downloadable asset, TeX, PDF, or diagram publication changes.
- Retrospective migration of older implementation plans into historical
  completion records.

## Final Review Checklist

- [x] Every PRD requirement is mapped to a task or explicitly deferred.
- [x] Every task has acceptance criteria.
- [x] Every task has validation guidance.
- [x] Risky changes have review or rollback notes.
- [x] The plan avoids direct coding unless implementation is requested.
- [x] Commands were discovered from the repository or marked unknown.
- [x] Product questions are separated from implementation decisions.
