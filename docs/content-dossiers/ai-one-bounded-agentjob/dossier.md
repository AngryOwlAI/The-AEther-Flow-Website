# One Bounded AgentJob In Practice Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/ai-research-agent-system/one-bounded-agentjob/`
- Reader job: Understand one AgentJob as a bounded permission envelope for one
  auditable transaction.
- Primary audience: general public, AI-system developers, system engineers,
  and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

PG-015 creates a new route that uses committed AgentJob
`AJ-RT-20260614-249-001` as a concrete example. The page explains inputs,
allowed reads, allowed writes, forbidden paths/classes, validators, expected
outputs, completion, and handoff.

The route must avoid private local details and must not imply that one
AgentJob can settle broad project truth or promote physics claims.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/research-agent-workflow-explainer.md` | committed generated noncanonical reader source | One bounded AgentJob invariant and safe/unsafe workflow summary. |
| `github-facing/director-agentjob-lifecycle-explainer.md` | committed generated noncanonical reader source | AgentJob lifecycle context. |
| `research_control/README.md` | committed control source | Authority model, one-job rule, validators, memory preflight, and PASS limits. |
| `research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml` | committed control record | Concrete AgentJob example. |
| `research_control/tasks/RT-20260614-249/00_TASK.yaml` | committed control record | Task objective and closure context. |
| `research_control/tasks/RT-20260614-249/DDR-20260614-249.md` | committed control record | Route-selection context. |
| `research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml` | committed control record | Completion evidence and verdict. |
| `research_control/handoffs/handoff-0282.yaml` | committed control record | Separate next-action boundary. |
| `registries/AGENT_JOB_REGISTRY.csv` | committed registry | Discovery row linking AgentJob and completion. |

## Source-derived topic outline

1. One AgentJob is one transaction.
2. The task and Director decision authorize the job.
3. Allowed reads define the evidence surface.
4. Allowed writes define the change surface.
5. Forbidden paths and source classes define stop conditions.
6. Expected outputs define completion obligations.
7. Validators produce bounded operational evidence.
8. Completion records verdict and uncertainty.
9. Handoff names a separate next packet.
10. Registry rows support discovery and validation.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| AgentJob | A bounded execution contract for one transaction. | Not reusable permission. |
| Allowed read path | A source or record the job may inspect. | Reading a source does not adopt its strongest possible claim. |
| Allowed write path | A path the job may change. | Anything outside the allowlist is out of scope. |
| Forbidden source class | A category the job must not rely on or promote. | Requires stop, new route, or gate. |
| Expected output | A file or record the job must account for. | Output existence is not claim adoption. |
| Completion | The closeout record for outputs, checks, verdict, and next recommendation. | Not broad truth. |

## Claim boundaries and forbidden implications

### Claim boundaries

- One AgentJob is one auditable transaction.
- The AgentJob allowlist is task-local.
- Allowed reads are evidence inputs, not claim promotions.
- Allowed writes are not general project permission.
- Validators check operational state.
- Completion evidence is scoped to the job.
- Handoff is a next-packet recommendation.

### Forbidden implications

- A historical AgentJob grants current permission.
- One AgentJob settles broad project truth.
- Validator PASS proves a theorem or promotes a benchmark.
- Expected outputs automatically become adopted source claims.
- Handoff extends the current job.
- The RT-249 example adopts a coupling law, derives matter coupling, adopts
  `MetricData(E)`, changes `g_eff`, derives Einstein equations, promotes a
  benchmark, or claims completed derivation.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with one-transaction model and source-boundary notice. |
| Plain summary | yes | Provided in page lead and safe summary. |
| Mechanism steps | yes | Inputs, allowed reads/writes, forbidden classes, validators, outputs, completion, handoff. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Sources listed above and rendered as provenance. |
| Boundary block | yes | Broad-truth, PASS, permission, handoff, and physics-claim limits. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required for this route. |
| Safe/unsafe summary | yes | High-risk overread prevention. |
| Related internal routes | yes | Internal-first reader journey before provenance links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/ai-one-bounded-agentjob/diagrams/one-agentjob-envelope.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/ai-one-bounded-agentjob-envelope.png` |
| Manifest id | `comprehension_ai_one_bounded_agentjob_envelope` |
| Alt text | One AgentJob envelope showing inputs, allowed reads, allowed writes, forbidden classes, validators, expected outputs, completion, handoff, and bounded PASS. |
| Caption | One AgentJob is an auditable permission envelope, not reusable authority or scientific proof. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: one bounded AgentJob makes one transaction auditable by naming
its objective, inputs, allowed paths, forbidden paths/classes, validators,
expected outputs, completion record, and handoff boundary.

## Unsafe summary

Unsafe summary: one AgentJob can settle broad project truth, grant reusable
permission, prove physics through PASS, or turn expected outputs into adopted
source claims.

## New-page audit

- Is a new public page proposed? Yes.
- Existing route that should be used instead: none; PG-015 explicitly creates
  `/project/ai-research-agent-system/one-bounded-agentjob/`.
- Reason a new route is justified: the workflow page explains the whole
  record chain; this route focuses on the AgentJob contract itself.

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

The AEther Flow. (2026d). *AgentJob AJ-RT-20260614-249-001*
[`research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml`].

The AEther Flow. (2026e). *Completion AJC-AJ-RT-20260614-249-001*
[`research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml`].

The AEther Flow. (2026f). *Handoff 0282*
[`research_control/handoffs/handoff-0282.yaml`].
