# Research-Agent Workflow Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/ai-research-agent-system/workflow/`
- Reader job: Understand how one research request becomes one bounded,
  inspectable record chain.
- Primary audience: general public, AI-system developers, system engineers,
  and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The route is an implemented reader-facing page. PG-014 rewrites it from a
general workflow overview into a concrete record-chain walkthrough using the
committed `RT-20260614-249` task family as the public-safe example.

The route must explain task, Director decision, AgentJob, execution-role
binding, completion, handoff, and registry discovery without presenting AI
workflow as physics proof.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/research-agent-workflow-explainer.md` | committed generated noncanonical reader source | General workflow model and safe/unsafe operating summary. |
| `github-facing/director-agentjob-lifecycle-explainer.md` | committed generated noncanonical reader source | Record-chain lifecycle and immutable-evidence boundary. |
| `research_control/README.md` | committed control source | Authority model, one-job rule, memory preflight, validation, and PASS limits. |
| `github-facing/validator-operator-workflow-explainer.md` | committed generated noncanonical reader source | Validator and PASS interpretation. |
| `research_control/tasks/RT-20260614-249/00_TASK.yaml` | committed control record | Concrete task example. |
| `research_control/tasks/RT-20260614-249/DDR-20260614-249.md` | committed control record | Concrete Director decision example. |
| `research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml` | committed control record | Concrete AgentJob allowlist and validator example. |
| `research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml` | committed control record | Concrete completion and PASS evidence example. |
| `research_control/handoffs/handoff-0282.yaml` | committed control record | Concrete handoff example. |
| `registries/RESEARCH_TASK_REGISTRY.csv` | committed registry | Discovery row for task. |
| `registries/DIRECTOR_DECISION_REGISTRY.csv` | committed registry | Discovery row for decision. |
| `registries/AGENT_JOB_REGISTRY.csv` | committed registry | Discovery row for AgentJob and completion. |

## Source-derived topic outline

1. Request classification and stop conditions.
2. Memory preflight and source inspection.
3. Director Decision Record selects one route.
4. AgentJob binds one allowed transaction.
5. Execution stays inside reads, writes, outputs, validators, and claim
   boundary.
6. Completion records command evidence, verdict, uncertainty, and next
   recommendation.
7. Handoff names a separate next packet.
8. Registry rows make the record chain discoverable.
9. PASS, memory, role labels, handoffs, and generated outputs remain bounded.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Director Decision Record | A routing record selecting one path and recording why other paths were not selected. | Not broad future permission. |
| AgentJob | A bounded execution contract with allowed reads, allowed writes, outputs, validators, and claim boundary. | Not reusable write authority. |
| Completion | Evidence record for outputs, command results, verdict, uncertainty, and next recommendation. | Not claim promotion or theorem proof. |
| Handoff | A separate continuation recommendation after a bounded transaction closes. | Not silent extension of the current job. |
| Registry row | Discoverability and validation metadata for a tracked record. | Not source proof by itself. |
| Memory preflight | Retrieval support for finding likely sources and prior decisions. | Navigation only; verify source files. |

## Claim boundaries and forbidden implications

### Claim Boundaries

- One request becomes one bounded transaction.
- Memory is navigation, not authority.
- Source files and registry rows must be inspected before relying on memory.
- A role template becomes current authority only through an execution-role
  record and AgentJob allowlist.
- Validator PASS is operational evidence for the checked state.
- A handoff is a future packet recommendation, not current authority.
- Generated pages remain reader surfaces.

### Forbidden Implications

- The workflow proves physics.
- The AI system independently owns scientific judgment.
- A validator PASS proves a theorem, promotes a benchmark, or adopts ontology.
- A handoff silently extends a closed job.
- Registry metadata, generated derivatives, wiki notes, or memory hits replace
  source inspection.
- A role label grants permission outside the current AgentJob.
- The RT-249 example authorizes coupling-law adoption, matter coupling,
  `MetricData(E)`, `g_eff`, Einstein equations, benchmark promotion, or
  completed derivation.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with reader context and source-boundary notice. |
| Plain summary | yes | Provided in reusable comprehension block and page lead. |
| Mechanism steps | yes | Request, memory/source, Director decision, AgentJob, completion, handoff. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Sources listed above and rendered as provenance. |
| Boundary block | yes | PASS, memory, role, handoff, and physics-claim limits. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required for this route. |
| Safe/unsafe summary | yes | High-risk overread prevention. |
| Related internal routes | yes | Internal-first reader journey before provenance links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/ai-workflow/diagrams/bounded-agentjob-chain.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/ai-workflow-bounded-agentjob-chain.png` |
| Manifest id | `comprehension_ai_workflow_bounded_agentjob_chain` |
| Alt text | Request narrows through memory/source checks, Director decision, one AgentJob, completion, handoff, registry rows, and a PASS boundary. |
| Caption | Each workflow record narrows the current transaction; PASS remains bounded to the checked state. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: research-agent workflow makes one transaction inspectable through
classification, memory/source checks, a Director decision, one AgentJob,
completion evidence, handoff when needed, and registry discovery.

## Unsafe summary

Unsafe summary: a workflow page can expand scope, treat PASS as theorem proof,
bypass human gates, anthropomorphize model behavior, or let memory and
generated pages replace source inspection.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead:
  `/project/ai-research-agent-system/workflow/`.
- Reason a new route is or is not justified: The existing route is the correct
  public surface for this content.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [ ] Mobile layout and desktop layout were reviewed.
- [ ] Human review note is recorded under `docs/quality/`.

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
