# Research-Agent Workflow Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/ai-research-agent-system/workflow/`
- Reader job: Understand how a request becomes one inspectable transaction.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/research-agent-workflow-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/director-agentjob-lifecycle-explainer.md` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Request classification
2. Director decision
3. AgentJob allowlist
4. Validation evidence
5. Completion and handoff limits

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Director decision | Routing record selecting one path and boundary. | Not broad future permission. |
| Completion | Evidence record for outputs, checks, verdict, uncertainty, and next step. | Not claim promotion. |
| Handoff | Separate continuation recommendation. | Not a silent job extension. |

## Claim boundaries and forbidden implications

### Claim boundaries

- One request should not hide a second objective.
- PASS is bounded to the checked state.
- Human-gated decisions remain separate.

### Forbidden implications

- Workflow PASS proves a theorem.
- Handoff silently extends current authority.
- Memory can replace source inspection.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with reader context and source-boundary notice. |
| Plain summary | yes | Provided in the reusable comprehension block. |
| Mechanism steps | yes | Source-derived route mechanism. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Sources listed above and rendered as provenance. |
| Boundary block | yes | Claim boundaries and forbidden implications. |
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
| Alt text | Request through Director decision, AgentJob allowlist, execution, validators, completion, handoff, and bounded PASS limit. |
| Caption | Each workflow record narrows the current transaction instead of broadening authority. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Research-agent workflow makes one transaction inspectable through classification, a Director decision, one AgentJob, validation evidence, completion, and handoff when needed.

## Unsafe summary

Unsafe summary: A workflow page can expand scope, treat PASS as theorem proof, bypass human gates, or let memory and generated pages replace source inspection.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/ai-research-agent-system/workflow/`.
- Reason a new route is or is not justified: The existing route is the correct public surface for this content.

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

- AEther-Flow Project. (2026). `github-facing/research-agent-workflow-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/director-agentjob-lifecycle-explainer.md`.
