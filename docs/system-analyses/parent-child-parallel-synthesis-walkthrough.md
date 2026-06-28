# Parent-Child Parallel Synthesis Walkthrough System Analysis

## Purpose

This analysis supports PG-016: rewriting
`/project/ai-research-agent-system/parent-child-synthesis/` with a clear
lifecycle explanation and one-outer-AgentJob boundary.

The route should explain why parent-child synthesis exists, how it improves
review coverage, and why parallel perspectives do not create parallel
authority.

## Scope And Authority

This document is website-maintained explanatory analysis. It is not source
authority and does not change the one-job rule, AgentJob schema,
execution-role schema, validators, routing behavior, role authority, write
permissions, or physics claim status.

The page may explain the mode. It cannot authorize a parent-child packet, add
child AgentJobs, create child execution-role records, bypass conflict review,
or promote physics claims.

## Evidence Reviewed

Committed upstream sources were inspected via `git show HEAD:<path>` to avoid
using dirty working-tree material.

- `github-facing/parent-child-synthesis-explainer.md`
  - Defines the one outer AgentJob invariant, internal parent and child units,
    inherited authority, conflict handling, fused output, reader scope, and
    safe/unsafe summaries.
- `research_control/README.md`
  - Defines the one-job rule and states that physics research AgentJobs after
    the relevant date must declare `parent_child_parallel_synthesis` without
    relaxing the one-job boundary.
- `.agents/schemas/AGENT_JOB_SCHEMA.md`
  - Provides the AgentJob contract surface that owns reads, writes, validators,
    expected outputs, and role decomposition fields.
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
  - Provides the execution-role boundary: one task-local role contract
    constrains the job.
- `registries/AGENT_JOB_REGISTRY.csv`
  - Provides registry context for AgentJob discoverability and completion
    paths.
- `docs/content-dossiers/parent-child-synthesis/dossier.md`
  - Provides the existing page-comprehension contract.
- `docs/content-dossiers/parent-child-synthesis/diagrams/single-outer-agentjob-frame.mmd`
  - Provides the existing source-bounded Mermaid diagram.

## Source-State Note

The upstream working tree is currently dirty because later candidate-era files
exist outside the committed source state. PG-016 therefore uses committed HEAD
sources only and does not rely on uncommitted `RT-20260614-250` material.

## System Context

Parent-child synthesis is an internal structure inside one physics AgentJob.
It exists to improve analytical coverage when a difficult packet benefits from
multiple perspectives, such as mathematical and philosophical pressure tests.

The external control surface remains singular:

1. one Director decision;
2. one outer AgentJob;
3. one execution-role record;
4. one completion record;
5. one fused output; and
6. one downstream reference path.

The internal units do not create new authority. Child outputs inherit the
outer job's claim boundary, source restrictions, write allowlist, validators,
human-gate status, and stop conditions.

## Lifecycle Walkthrough

| Stage | Function | Boundary |
| --- | --- | --- |
| Director decision | Selects one outer job route. | Does not select child jobs. |
| Outer AgentJob | Owns reads, writes, validators, outputs, and stop conditions. | Child units cannot expand the allowlist. |
| Parent unit | Reviews children, preserves conflicts, and fuses the final artifact. | Cannot ignore blocking conflict. |
| Child units | Produce supporting `draft/control` perspective outputs. | No independent verdict or role record. |
| Conflict review | Inspects declared disagreements. | PASS is blocked while a blocking conflict remains unresolved. |
| Fused output | Carries the final artifact for completion and handoff. | Supporting drafts do not replace it. |
| Completion and handoff | Close the one job and name any next packet. | No hidden second job. |

## Functionality Or Topic Analysis

### Public layer

For a general reader, parent-child synthesis means "more than one internal
perspective inside one bounded job." It does not mean multiple independent
agents each have their own authority.

### Specialist layer

For maintainers and AI-system developers, the critical details are:

- role decomposition remains inside the outer AgentJob;
- child outputs are supporting `draft/control` artifacts;
- parent fusion produces the downstream artifact;
- conflict policy is mandatory;
- declared blocking conflict prevents PASS completion if unresolved; and
- all paths stay inside the outer AgentJob allowlist.

### Diagram review

The existing `single-outer-agentjob-frame.mmd` diagram is source-bounded and
already matches the route contract: Director decision, outer AgentJob, parent,
children, conflict review, fused output, completion, and no-extra-authority
boundary. It can be reused if browser QA confirms the generated PNG remains
readable on desktop and mobile.

## Interfaces, Inputs, Outputs

| Interface | Input | Output | Boundary |
| --- | --- | --- | --- |
| Director decision | Source state and route need | One outer AgentJob | Not multiple child jobs. |
| Outer AgentJob | Role decomposition and allowlist | Parent/child work surface | Same boundary for all units. |
| Child unit | Assigned perspective | Supporting draft/control output | Not an independent verdict. |
| Parent unit | Child outputs and conflict policy | Fused artifact | Cannot hide blocking conflict. |
| Conflict review | Declared disagreement | Resolved, revised, or blocked state | PASS blocked if unresolved. |
| Completion | Fused output and validator receipts | One verdict and next recommendation | Scoped to one job. |

## Risks, Failure Modes, Claim Boundaries

Primary risks:

- implying child units are separate AgentJobs;
- implying child units have separate role records or write authority;
- implying parallel perspectives bypass human gates;
- treating a child output as an independent verdict;
- allowing the parent to ignore a declared blocking conflict;
- presenting parent-child synthesis as mandatory for all project-system or
  documentation work.

Hard boundaries:

- one Director decision;
- one outer AgentJob;
- one execution-role record;
- one completion record;
- one fused output;
- child outputs are supporting `draft/control`;
- no child AgentJobs;
- no child execution-role records;
- no extra write authority;
- no independent child verdicts;
- no conflict bypass;
- no human-gate bypass;
- no physics claim promotion.

## Page Recommendations

The rewritten route should:

- open with the one-outer-AgentJob invariant;
- define parent, child, conflict review, and fused output;
- explain inherited authority before describing child perspectives;
- make conflict handling and PASS blocking visible;
- show safe and unsafe summaries;
- link to workflow, one bounded AgentJob, roles, Director/AgentJob lifecycle,
  validator workflow, and source authority;
- use internal routes as the primary reader path; and
- keep source links/provenance secondary.

## No-AI-Slop Gate

Status: pass with required edits.

Required edits:

- replace the generic internal explainer wrapper with a direct route;
- foreground one outer AgentJob;
- make conflict review and parent fusion explicit;
- preserve child `draft/control` status; and
- run desktop/mobile browser QA.

## Logical Next Step

Rewrite the public route, update source/provenance metadata, regenerate page
provenance, run the page validation profile, and perform desktop/mobile browser
QA for `/project/ai-research-agent-system/parent-child-synthesis/`.

## References

The AEther Flow. (2026a). *Parent-child parallel synthesis*
[`github-facing/parent-child-synthesis-explainer.md`].

The AEther Flow. (2026b). *Research control*
[`research_control/README.md`].

The AEther Flow. (2026c). *AgentJob schema*
[`.agents/schemas/AGENT_JOB_SCHEMA.md`].

The AEther Flow. (2026d). *Execution-role schema*
[`.agents/schemas/EXECUTION_ROLE_SCHEMA.md`].

The AEther Flow. (2026e). *AgentJob registry*
[`registries/AGENT_JOB_REGISTRY.csv`].

The AEther Flow Website. (2026a). *Parent-child synthesis content dossier*
[`docs/content-dossiers/parent-child-synthesis/dossier.md`].
