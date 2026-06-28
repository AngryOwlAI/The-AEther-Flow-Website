# Research-Agent Workflow Walkthrough System Analysis

## Purpose

This analysis supports PG-014: rewriting
`/project/ai-research-agent-system/workflow/` as a concrete record-chain
walkthrough.

The public page should let a general reader understand how one request becomes
one bounded transaction, while preserving the specialist distinction between
workflow evidence and scientific proof.

## Scope And Authority

This document is website-maintained explanatory analysis. It is not source
authority and does not change routing behavior, role authority, validator
semantics, write permissions, claim boundaries, or physics status.

The route may explain committed workflow records. It cannot authorize an
AgentJob, mutate a Director decision, change an allowlist, treat PASS as proof,
or promote a physics claim.

## Evidence Reviewed

Committed upstream sources were inspected via `git show HEAD:<path>` to avoid
using dirty working-tree material.

- `github-facing/research-agent-workflow-explainer.md`
  - Defines the request-to-one-AgentJob narrowing sequence, memory as
    navigation, source inspection, two operating lanes, role gates, outputs,
    and stop conditions.
- `github-facing/director-agentjob-lifecycle-explainer.md`
  - Defines the record chain: task, Director Decision Record, AgentJob,
    execution-role record, completion, handoff, and registry rows.
- `research_control/README.md`
  - Defines the authority model, one-job rule, memory preflight, validators,
    documentation impact, and PASS-result limits.
- `github-facing/validator-operator-workflow-explainer.md`
  - Defines validation as bounded operational evidence and warns against
    reading PASS as scientific truth.
- `research_control/tasks/RT-20260614-249/00_TASK.yaml`
  - Provides a committed task example with objective, decision, job,
    completion, parent task, human-gate flag, claim boundary, and closure.
- `research_control/tasks/RT-20260614-249/DDR-20260614-249.md`
  - Provides a Director Decision Record selecting one route and preserving
    rejected alternatives.
- `research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml`
  - Provides an AgentJob example with allowed reads, allowed writes, forbidden
    paths/classes, validators, expected outputs, and claim boundary.
- `research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml`
  - Provides completion evidence: output paths, command results, validation
    status, verdict, distance-to-GR status, next recommendation, and forbidden
    conclusion summary.
- `research_control/handoffs/handoff-0282.yaml`
  - Provides the continuation record created after completion.
- `registries/RESEARCH_TASK_REGISTRY.csv`,
  `registries/DIRECTOR_DECISION_REGISTRY.csv`, and
  `registries/AGENT_JOB_REGISTRY.csv`
  - Show that registry rows make the task, decision, and AgentJob discoverable.

## Source-State Note

The upstream working tree is currently dirty because later candidate-era files
exist outside the committed source state. PG-014 therefore uses committed HEAD
records only. It does not rely on uncommitted `RT-20260614-250` files or
dirty working-tree registry state.

## System Context

The workflow is a control system for bounded work. Its central invariant is
that a request narrows rather than widens:

1. identify the kind of work;
2. run memory preflight when relevant;
3. verify memory hits against canonical sources or registry rows;
4. select one route through a Director Decision Record;
5. bind authority through one AgentJob;
6. execute within allowed reads, writes, outputs, validators, and claim
   boundary;
7. record completion evidence; and
8. hand off a separate next packet only when continuation is needed.

The process is useful because it records what was authorized, what was checked,
what changed, and what remains blocked. It is not useful as independent
physics evidence.

## Concrete Walkthrough: RT-20260614-249

The route can use `RT-20260614-249` as a committed example.

| Record | Concrete file | What it shows | Boundary |
| --- | --- | --- | --- |
| Task | `research_control/tasks/RT-20260614-249/00_TASK.yaml` | One objective, parent task, decision id, job id, completion id, claim boundary, and closure status. | The task does not authorize adjacent future packets. |
| Director Decision Record | `research_control/tasks/RT-20260614-249/DDR-20260614-249.md` | Selected Theoretical Continuation Selector route and rejected broader routes. | The decision authorizes selector-only classification. |
| AgentJob | `research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml` | Allowed reads, writes, generated paths, forbidden paths/classes, validators, outputs, and claim boundary. | The allowlist is not reusable permission. |
| Completion | `research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml` | Output paths, command evidence, PASS status, verdict, and next recommendation. | PASS is operational evidence for the bounded transaction. |
| Handoff | `research_control/handoffs/handoff-0282.yaml` | Separate next action and preserved blocked claims. | Handoff is not silent extension of the closed job. |
| Registries | `registries/*.csv` rows | Discovery and validator-checkable references. | Registry presence is not theorem proof. |

Public-safe summary of the example:

`RT-20260614-249` selected one future criteria-formalization route after scoped
evidence acceptance. It did not adopt a coupling law, derive or adopt matter
coupling, adopt `MetricData(E)`, change `g_eff`, import stress-energy
semantics, derive Einstein equations, promote a benchmark, or claim completed
derivation.

## Functionality Or Topic Analysis

### Reader model

A reader should understand the workflow as a ledger of bounded authority:
each record narrows the next record and leaves a trace for review.

### Specialist model

A specialist should see where authority lives:

- task objective and closure status;
- Director route selection;
- execution-role binding;
- AgentJob allowlist;
- validators and command evidence;
- completion verdict and uncertainty;
- handoff boundary; and
- registry discoverability.

### AI and language-model boundary

The page should avoid anthropomorphizing model behavior. The agent is not
presented as independently understanding, owning, or proving the research. The
workflow records human-governed, source-inspected, validator-checked tool use.

## Interfaces, Inputs, Outputs

| Interface | Input | Output | Boundary |
| --- | --- | --- | --- |
| Request classification | User request and tracked state | Lane or stop condition | No write authority yet. |
| Memory preflight | Memory index and retrieval layers | Navigation hints and receipts | Memory is not source authority. |
| Canonical source inspection | Registered source files and CSV rows | Verified evidence basis | Source record scope controls claim scope. |
| Director Decision Record | Objective, source state, roles | One selected route | Not future broad permission. |
| AgentJob | Selected route | Allowed reads, writes, validators, outputs | One transaction only. |
| Completion | Outputs and command results | Verdict, uncertainty, next recommendation | PASS is bounded evidence. |
| Handoff | Completion state | Separate next packet | Not an extension of the closed job. |
| Registry rows | Canonical record paths | Discoverability | Not proof of science. |

## Risks, Failure Modes, Claim Boundaries

Primary risks:

- presenting workflow as autonomous reasoning or scientific authority;
- treating validator PASS as theorem proof;
- implying a handoff extends the current job;
- using memory, wiki, generated pages, or registry metadata instead of source
  inspection;
- implying a role template grants live authority without task-local binding;
- making the RT-249 example sound like physics promotion.

Hard boundaries:

- AI workflow is not physics proof.
- PASS is bounded operational evidence.
- Memory is navigation, not authority.
- Generated pages are reader surfaces, not source authority.
- A role template is not current write permission.
- Handoff is not silent extension.
- No coupling-law adoption.
- No matter-coupling derivation or adoption.
- No `MetricData(E)`.
- No `g_eff` scope change.
- No Einstein equations.
- No benchmark promotion.
- No completed derivation.

## Page Recommendations

The rewritten route should:

- open with the one-transaction model;
- name a concrete committed record chain near the top;
- show task, Director decision, AgentJob, completion, handoff, and registry
  chain as distinct records;
- keep memory/source inspection before execution;
- explain validators as bounded evidence;
- link internally to source authority, memory/registries, roles/skills,
  Director and AgentJob lifecycle, and validator/operator workflow;
- keep provenance links available but secondary to internal reader paths; and
- keep unsafe interpretations visible.

## No-AI-Slop Gate

Status: pass with required edits.

Required edits:

- replace generic workflow prose with concrete record-chain explanation;
- add the RT-249 example as a bounded public-safe walkthrough;
- avoid model-anthropomorphic language;
- preserve PASS and human-gate limits; and
- update dossier, diagram, and route QA after implementation.

## Logical Next Step

Rewrite the route, update the content dossier and comprehension diagram, render
the diagram, regenerate manifests and page provenance, run the page validation
profile, and perform desktop/mobile browser QA.

## References

The AEther Flow. (2026a). *Research-agent workflow*
[`github-facing/research-agent-workflow-explainer.md`].

The AEther Flow. (2026b). *Director decisions and AgentJob lifecycle*
[`github-facing/director-agentjob-lifecycle-explainer.md`].

The AEther Flow. (2026c). *Research control*
[`research_control/README.md`].

The AEther Flow. (2026d). *Validator and operator workflow*
[`github-facing/validator-operator-workflow-explainer.md`].

The AEther Flow. (2026e). *Task RT-20260614-249*
[`research_control/tasks/RT-20260614-249/00_TASK.yaml`].

The AEther Flow. (2026f). *Director Decision Record DDR-20260614-249*
[`research_control/tasks/RT-20260614-249/DDR-20260614-249.md`].

The AEther Flow. (2026g). *AgentJob AJ-RT-20260614-249-001*
[`research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml`].

The AEther Flow. (2026h). *Completion AJC-AJ-RT-20260614-249-001*
[`research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml`].

The AEther Flow. (2026i). *Handoff 0282*
[`research_control/handoffs/handoff-0282.yaml`].
