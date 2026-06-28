# One Bounded AgentJob In Practice System Analysis

## Purpose

This analysis supports PG-015: creating
`/project/ai-research-agent-system/one-bounded-agentjob/` as a concrete
example of one auditable transaction.

The route should give readers a practical mental model for bounded execution:
what goes into an AgentJob, what it may touch, what it must produce, what
validators check, and how completion and handoff close the transaction.

## Scope And Authority

This document is website-maintained explanatory analysis. It is not source
authority and does not change routing behavior, role authority, validator
semantics, write permissions, claim boundaries, or physics status.

The route may explain a committed AgentJob record. It cannot authorize a new
AgentJob, reuse a past allowlist as current permission, mutate a completion,
or imply one AgentJob can settle broad project truth.

## Evidence Reviewed

Committed upstream sources were inspected via `git show HEAD:<path>` to avoid
using dirty working-tree material.

- `github-facing/research-agent-workflow-explainer.md`
  - Defines the one bounded AgentJob invariant, source inspection, memory
    boundary, roles, gates, outputs, and stop conditions.
- `github-facing/director-agentjob-lifecycle-explainer.md`
  - Defines how AgentJob records fit between Director decisions, execution
    roles, completions, handoffs, and registries.
- `research_control/README.md`
  - Defines the authority model, one-job rule, memory preflight, validators,
    documentation impact, and PASS limits.
- `research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml`
  - Provides the source-approved AgentJob example for inputs, paths, outputs,
    validators, and boundaries.
- `research_control/tasks/RT-20260614-249/00_TASK.yaml`
  - Provides the task frame, objective, parent task, decision id, completion
    id, and closure status.
- `research_control/tasks/RT-20260614-249/DDR-20260614-249.md`
  - Provides the route-selection context that authorized the AgentJob.
- `research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml`
  - Provides output paths, command evidence, validation status, verdict,
    next recommendation, and forbidden conclusion summary.
- `research_control/handoffs/handoff-0282.yaml`
  - Provides the post-completion next-action boundary.
- `registries/AGENT_JOB_REGISTRY.csv`
  - Provides the registry row linking AgentJob and completion.

## Source-State Note

The upstream working tree is currently dirty because later candidate-era files
exist outside the committed source state. PG-015 therefore uses committed HEAD
records only. It does not rely on uncommitted `RT-20260614-250` material.

## System Context

An AgentJob is the executable boundary for one transaction. It is narrower
than the research topic and narrower than the role template. In practice, it
answers five questions:

1. What objective is this job allowed to pursue?
2. Which sources may it inspect?
3. Which paths may it write?
4. Which paths, source classes, and conclusions are forbidden?
5. Which outputs and validators must the completion account for?

The job is not reusable permission. A later task needs its own decision and
AgentJob, even when it follows directly from a handoff.

## Concrete Walkthrough: AJ-RT-20260614-249-001

The route can use `AJ-RT-20260614-249-001` as a committed example.

| AgentJob field family | What it does | Public explanation | Boundary |
| --- | --- | --- | --- |
| Objective | States the one transaction. | Classify the next route after scoped evidence acceptance. | Not adoption, derivation, or benchmark promotion. |
| Allowed reads | Names source files, prior tasks, roles, schemas, and registries. | Shows what evidence may be inspected. | Read access does not make every source a conclusion. |
| Allowed writes | Names control files, task directory, handoff files, and registries. | Shows where changes may land. | Anything outside the allowlist is out of scope. |
| Forbidden paths/classes | Names ontology, manuscripts, target imports, generated authority, role authority, validator authority, and physics-promotion classes. | Shows what the job must not claim or edit. | A forbidden class requires a new route or gate. |
| Required validators | Names memory, project-control, research-control, and diff checks. | Shows the operational evidence required at closeout. | PASS is not theorem proof. |
| Expected outputs | Names child outputs, fused artifact, completion, and handoff. | Shows what completion must account for. | Missing output blocks clean closure. |
| Completion id | Links to command evidence and verdict. | Shows what actually passed and what remains blocked. | Completion evidence is scoped to this job. |

Public-safe summary of the example:

`AJ-RT-20260614-249-001` selected a future criteria-formalization packet and
recorded bounded operational evidence. It did not adopt a coupling law, derive
or adopt matter coupling, adopt `MetricData(E)`, change `g_eff`, import
stress-energy semantics, derive Einstein equations, promote a benchmark, or
claim completed derivation.

## Functionality Or Topic Analysis

### Public layer

For a general reader, the AgentJob is a permission envelope. It keeps one
piece of work small enough to audit.

### Specialist layer

For maintainers and AI-system developers, the AgentJob is a schema-backed
contract linking:

- task and Director decision;
- execution role;
- allowed reads and writes;
- forbidden paths and source classes;
- expected outputs;
- approved commands;
- required validators;
- completion id; and
- claim boundary.

### Security and privacy boundary

The public page should avoid exposing private local runtime details. It may
show repository-relative source paths from committed records. It should not
publish local absolute paths, hidden credentials, terminal state, or private
machine context.

## Interfaces, Inputs, Outputs

| Interface | Input | Output | Boundary |
| --- | --- | --- | --- |
| Task | Objective and parent state | AgentJob id and completion id | Not full-topic truth. |
| Director decision | Route selection | Selected role and job | Not broad future permission. |
| AgentJob | Reads, writes, outputs, validators, boundary | Executable contract | Not reusable authority. |
| Validators | Current file state | PASS or failure evidence | Not physics proof. |
| Completion | Outputs and command results | Verdict and next recommendation | Scoped to one job. |
| Handoff | Completion status | Future packet recommendation | Not current job extension. |
| Registry row | Canonical record paths | Discovery and checkability | Not theorem proof. |

## Risks, Failure Modes, Claim Boundaries

Primary risks:

- implying a historical AgentJob grants current permission;
- treating allowed reads as endorsement of all read content;
- presenting PASS as scientific proof;
- publishing private local paths or runtime details;
- implying one job can settle broad project truth;
- losing the distinction between output existence and claim adoption.

Hard boundaries:

- one AgentJob is one transaction;
- no reusable permission;
- no private local details;
- PASS is bounded operational evidence;
- completion is not claim promotion;
- handoff is not current-job extension;
- no coupling-law adoption;
- no matter-coupling derivation or adoption;
- no `MetricData(E)`;
- no `g_eff`;
- no Einstein equations;
- no benchmark promotion;
- no completed derivation.

## Page Recommendations

The public page should:

- show the AgentJob as a permission envelope;
- list the concrete RT-249 AgentJob identifiers;
- explain inputs, allowed reads, allowed writes, forbidden paths/classes,
  validators, expected outputs, completion, and handoff;
- keep public and specialist layers distinct;
- link internally to workflow, roles, memory, validator, lifecycle, and source
  authority routes;
- make provenance links secondary; and
- include safe and unsafe readings.

## No-AI-Slop Gate

Status: pass with required edits.

Required edits:

- create the route from committed AgentJob evidence;
- add a dossier and diagram;
- avoid private local details;
- keep broad-truth and physics-promotion boundaries visible; and
- run desktop/mobile browser QA.

## Logical Next Step

Create the public route, dossier, static diagram, manifest registrations, and
browser QA for `/project/ai-research-agent-system/one-bounded-agentjob/`.

## References

The AEther Flow. (2026a). *Research-agent workflow*
[`github-facing/research-agent-workflow-explainer.md`].

The AEther Flow. (2026b). *Director decisions and AgentJob lifecycle*
[`github-facing/director-agentjob-lifecycle-explainer.md`].

The AEther Flow. (2026c). *Research control*
[`research_control/README.md`].

The AEther Flow. (2026d). *AgentJob AJ-RT-20260614-249-001*
[`research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml`].

The AEther Flow. (2026e). *Task RT-20260614-249*
[`research_control/tasks/RT-20260614-249/00_TASK.yaml`].

The AEther Flow. (2026f). *Director Decision Record DDR-20260614-249*
[`research_control/tasks/RT-20260614-249/DDR-20260614-249.md`].

The AEther Flow. (2026g). *Completion AJC-AJ-RT-20260614-249-001*
[`research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml`].

The AEther Flow. (2026h). *Handoff 0282*
[`research_control/handoffs/handoff-0282.yaml`].
