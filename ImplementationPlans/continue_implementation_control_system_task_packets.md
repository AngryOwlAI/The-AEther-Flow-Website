# Continue Implementation Control System Task Packets

Source PRD: `PRDs/continue-implementation-control-system-prd.md`

Companion plan:
`ImplementationPlans/continue_implementation_control_system_implementation_plan.md`

Repository:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website`

Branch scope recommendation: `codex/continue-implementation-control-system`

Global execution rules:

- Keep the system strictly website-local.
- Do not modify `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
- Do not deploy or push.
- Preserve unrelated dirty files.
- Execute at most one bounded task packet per invocation.
- Treat `PRDs/` and `ImplementationPlans/` as planning context, not live
  implementation authority.
- Preserve the Source Authority Boundary for all public claims.

## Task 1: Bootstrap Implementation-Control Records

### Goal

Create the first live website-local implementation-control authority records and
document the lightweight schema.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-003, REQ-005, REQ-006, REQ-009,
  REQ-010, REQ-011
- Relevant files or directories:
  - `implementation_control/`
  - `implementation_control/program_state.yaml`
  - `implementation_control/handoffs/`
  - `implementation_control/tasks/`
  - `AGENTS.md`
  - `CONTEXT.md`
  - `docs/architecture/website-feature-and-functionality.md`
  - `PRDs/continue-implementation-control-system-prd.md`
  - `ImplementationPlans/continue_implementation_control_system_implementation_plan.md`
- Existing patterns to follow:
  - Upstream `research_control` demonstrates live state plus handoff discipline,
    but do not copy physics-specific role machinery.
  - Website planning artifacts live under `PRDs/` and `ImplementationPlans/`.

### Constraints

- Do not create public routes, public assets, or public manifest records.
- Do not mutate upstream source project files.
- Do not mark old plans as completed implementation-control tasks.
- Keep the schema lightweight and explicit.

### Implementation notes

- Add `implementation_control/README.md` explaining authority order, record
  types, approval gates, one-packet execution, and upstream read-only status.
- Add `implementation_control/program_state.yaml` with the active bootstrap
  task, latest handoff, current status, and next recommended action.
- Add a first task directory such as
  `implementation_control/tasks/WI-20260629-001/`.
- Add `00_TASK.yaml`, one active job record under `jobs/`, and a matching
  initial handoff pair under `implementation_control/handoffs/`.
- Record allowed reads, allowed writes, required validators, stop conditions,
  approval gates, and checkpoint expectations.
- Keep status accurate. If the task is not complete yet, mark it active or
  pending rather than completed.

### Acceptance criteria

- [ ] `implementation_control/README.md` defines the lightweight control model.
- [ ] `program_state.yaml` names the active implementation task and latest
      handoff.
- [ ] The first task record has one bounded job with allowed reads, allowed
      writes, validators, stop conditions, and approval-gate fields.
- [ ] The latest handoff pair summarizes current state and next action.
- [ ] No upstream write path appears in allowed write paths.

### Validation

- `git diff --check`
- Until Task 3 exists, manually inspect the YAML and Markdown records for
  consistency.

### Done when

- The repository has an explicit prospective implementation-control authority
  surface ready for resolver and validator tooling.

## Task 2: Add Deterministic Continue-Implementation Resolver

### Goal

Add the read-only resolver command that reports the next bounded website
implementation packet.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-004, REQ-005, REQ-009, NFR-001,
  NFR-002
- Relevant files or directories:
  - `scripts/implementation_control/continue_implementation.py`
  - `scripts/implementation_control/README.md`
  - `package.json`
  - `tests/`
  - `implementation_control/`
- Existing patterns to follow:
  - `scripts/research_control/continue_research.py` in the upstream project for
    JSON-by-default and `--summary` ergonomics.
  - Existing website Python validators and tests.

### Constraints

- Resolver must be read-only.
- Do not checkpoint, commit, stage, push, deploy, or modify files from the
  resolver.
- Do not infer authority from PRD or plan text when live state exists.
- Do not add dependencies unless the existing environment already requires
  them.

### Implementation notes

- Implement `continue_implementation.py` with JSON default output and
  `--summary`.
- Resolve:
  - status;
  - boundary;
  - active task ID;
  - latest handoff ID and path;
  - current job ID;
  - next recommended action;
  - approval-gate status;
  - required validators;
  - allowed read/write summaries;
  - stop conditions;
  - checkpoint requirement.
- Add `npm run continue:implementation`.
- Add tests covering ready, missing-state blocked, approval-required, active-job
  ready, and no-action scenarios using temporary fixtures.

### Acceptance criteria

- [ ] `npm run continue:implementation` emits stable JSON.
- [ ] `npm run continue:implementation -- --summary` emits a concise human
      summary.
- [ ] Resolver fails closed when required state files are missing or malformed.
- [ ] Resolver output identifies one bounded active job or blocks clearly.
- [ ] Tests cover resolver boundary behavior.

### Validation

- `python3 -m pytest`
- `npm run continue:implementation`
- `npm run continue:implementation -- --summary`
- `git diff --check`

### Done when

- A future Codex session can start by running the resolver and reliably know
  the next implementation boundary without modifying files.

## Task 3: Add Implementation-Control Validator And Validation Gate

### Goal

Add fail-closed validation for implementation-control records and wire it into
the normal repository validation chain.

### Context

- PRD requirements: REQ-001, REQ-003, REQ-006, REQ-007, REQ-010, REQ-011,
  NFR-001, NFR-002
- Relevant files or directories:
  - `scripts/implementation_control/validate_implementation_control.py`
  - `scripts/implementation_control/README.md`
  - `package.json`
  - `tests/`
  - `implementation_control/`
- Existing patterns to follow:
  - `scripts/validate_*` commands in the website repo.
  - `tests/test_validate_*.py` style for focused validator tests.

### Constraints

- Validator must not modify files.
- Validator must not treat successful validation as source authority,
  deployment approval, or claim approval.
- Keep package-script ordering consistent with the PRD: after existing website
  content/provenance checks and before `npm run build`.

### Implementation notes

- Validate required directories and files.
- Validate program state, latest handoff, active task, active job, and
  completion references where present.
- Validate allowed write paths:
  - repo-relative;
  - no upstream source project paths;
  - no broad filesystem roots;
  - no unstated public manifest or asset authority expansion.
- Validate approval-gate fields for high-risk categories.
- Validate required validators against known package scripts or explicitly
  documented shell commands.
- Add `npm run validate:implementation-control`.
- Insert it into `npm run validate` before `npm run build`.
- Add Python tests for valid records and representative failures.

### Acceptance criteria

- [ ] `npm run validate:implementation-control` passes for the bootstrap
      records.
- [ ] Invalid control fixtures fail with specific error messages.
- [ ] `npm run validate` includes the implementation-control validator before
      the build step.
- [ ] Validator rejects upstream write paths and high-risk work without
      approval status.
- [ ] Tests cover success and failure cases.

### Validation

- `npm run validate:implementation-control`
- `python3 -m pytest`
- `npm run validate`
- `git diff --check`

### Done when

- Broken implementation-control state is visible through the standard website
  validation gate.

## Task 4: Add Narrow Checkpoint Transaction Command

### Goal

Add the mutating checkpoint command that validates, stages only allowed packet
files, and creates a local Git commit after successful packet completion.

### Context

- PRD requirements: REQ-001, REQ-005, REQ-006, REQ-008, REQ-010, NFR-003,
  NFR-004
- Relevant files or directories:
  - `scripts/implementation_control/checkpoint_implementation_transaction.py`
  - `scripts/implementation_control/validate_implementation_control.py`
  - `implementation_control/`
  - `package.json`
  - `tests/`
- Existing patterns to follow:
  - Upstream checkpoint discipline from `checkpoint_research_transaction.py`,
    but with a smaller website-specific scope.
  - Git safety rules in `AGENTS.md`.

### Constraints

- Do not push.
- Do not deploy.
- Do not mutate upstream source project files.
- Do not invent completion records or validation evidence.
- Do not stage unrelated dirty files.
- Block if dirty-state separation is ambiguous.

### Implementation notes

- Read the active job and completion record.
- Confirm completion exists before commit.
- Run the job's required validators.
- Inspect `git status --porcelain`.
- Stage only allowed write paths that belong to the active packet.
- If unrelated dirty files exist, leave them untouched when safely separable.
- If unrelated changes overlap allowed paths ambiguously, block with path
  evidence.
- Create a local commit with a deterministic message derived from the active
  task or completion summary.
- Print a concise receipt including staged paths, validators run, commit hash,
  and paths ignored as unrelated.
- Add tests using temporary Git repositories where feasible.

### Acceptance criteria

- [ ] Checkpoint refuses to run without a valid active completion.
- [ ] Checkpoint runs required validators before staging.
- [ ] Checkpoint stages only active packet allowed paths.
- [ ] Checkpoint preserves unrelated dirty files when separable.
- [ ] Checkpoint blocks ambiguous dirty-state overlap.
- [ ] Checkpoint creates a local commit and reports the commit hash.
- [ ] Checkpoint never pushes or deploys.

### Validation

- `python3 -m pytest`
- `npm run validate:implementation-control`
- `git diff --check`
- For manual smoke testing, use a temporary branch or fixture repository before
  using the command on the real bootstrap transaction.

### Done when

- Successful implementation packets can be validated and committed locally
  without broad staging or release-side effects.

## Task 5: Document Operating Procedure And Close Bootstrap

### Goal

Document how future sessions should use `continue implementation`, then close
the bootstrap task through completion and handoff records.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-005, REQ-008, REQ-009, REQ-010,
  REQ-011
- Relevant files or directories:
  - `implementation_control/README.md`
  - `scripts/implementation_control/README.md`
  - `docs/architecture/website-feature-and-functionality.md`
  - `implementation_control/tasks/WI-20260629-001/jobs/completions/`
  - `implementation_control/handoffs/`
  - `implementation_control/program_state.yaml`
- Existing patterns to follow:
  - Existing architecture document's maintainer workflow and validation gate
    descriptions.
  - Upstream handoff style: concise YAML metadata plus Markdown summary.

### Constraints

- Do not publish a public route for this system.
- Do not imply validation is source authority.
- Do not deploy or push.
- Do not rewrite unrelated architecture sections.

### Implementation notes

- Add or update docs describing the normal flow:
  1. run resolver;
  2. inspect boundary;
  3. execute one bounded packet;
  4. write completion and handoff records;
  5. run validation;
  6. checkpoint local commit;
  7. do not push or deploy without explicit instruction.
- Add completion evidence for the bootstrap task after Tasks 1 through 4 are
  implemented.
- Update `program_state.yaml` to the next recommended action.
- Create the next handoff pair.
- Run the full validation chain.
- Use the checkpoint command to create the local commit.

### Acceptance criteria

- [ ] Documentation explains resolver, validator, checkpoint, approval gates,
      and upstream read-only boundary.
- [ ] Bootstrap completion record lists files changed and validators run.
- [ ] Bootstrap handoff names the next recommended implementation packet.
- [ ] `program_state.yaml` reflects the closed bootstrap and next action.
- [ ] Full validation has been run or any failure is recorded with concrete
      command output and reason.
- [ ] The bootstrap transaction is locally committed by the checkpoint command.

### Validation

- `npm run continue:implementation`
- `npm run continue:implementation -- --summary`
- `npm run validate:implementation-control`
- `python3 -m pytest`
- `npm run validate`
- `git diff --check`

### Done when

- The bootstrap control system is documented, validated, closed with durable
  records, and committed locally as the first implementation-control
  transaction.
