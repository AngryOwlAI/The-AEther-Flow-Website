# AI Research-Agent System Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/ai-research-agent-system/`
- Reader job: Understand the governed AI workflow as bounded support for research, not autonomous scientific authority.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/research-agent-workflow-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/roles-and-skills-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/memory-system-explainer.md` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Governed workflow and human accountability
2. Task classification and one bounded AgentJob
3. Role and skill limits
4. Memory as source navigation
5. Safe and unsafe interpretations

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| AI research-agent system | Governed workflow for planning, checking, preserving, and reviewing work. | Not autonomous research ownership. |
| AgentJob | Bounded execution contract for one transaction. | Cannot silently add objectives. |
| Human accountability | Protected publication and claim decisions remain explicit. | Generated output cannot replace those gates. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Workflow evidence is operational, not physics proof.
- Role and skill labels do not grant current write permission.
- Memory is navigation and must be checked against sources.

### Forbidden implications

- The AI system autonomously owns research decisions.
- Workflow validation proves physics claims.
- Generated output replaces human-gated responsibility.

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
| Mermaid source | `docs/content-dossiers/ai-research-agent-system/diagrams/task-authority-review-map.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/ai-system-task-authority-map.png` |
| Manifest id | `comprehension_ai_system_task_authority_map` |
| Alt text | AI workflow request narrowing through classification, one AgentJob, role limits, memory support, review, and a no-physics-proof boundary. |
| Caption | The AI system organizes auditable work without becoming independent physics evidence. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The AI research-agent system is a governed workflow for bounded, source-inspected, validator-checked research work under human accountability.

## Unsafe summary

Unsafe summary: The AI system autonomously owns research decisions, proves physics claims, grants role permissions, or replaces human-gated publication and claim authority.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/ai-research-agent-system/`.
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
- AEther-Flow Project. (2026). `github-facing/roles-and-skills-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/memory-system-explainer.md`.
