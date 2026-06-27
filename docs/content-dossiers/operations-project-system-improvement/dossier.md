# Project-System Improvement Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/operations/project-system-improvement/`
- Reader job: Understand project-system repair as one bounded improvement packet.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/project-system-improvement-explainer.md` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Observed diff or signal
2. Classifier
3. Resolver
4. One project-system AgentJob
5. Receipt and close/defer decision

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Signal | Tracked project-system problem or improvement indicator. | Not closed without matching evidence. |
| Sidecar | Project-improvement support artifact. | Input, not replacement handoff. |
| Resolver | Mechanism for ranking or choosing next packet. | Not a physics selector. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Improvement packets stay project-system scoped.
- Receipts are required for closure.
- Sidecars are support inputs.

### Forbidden implications

- Maintenance silently continues physics.
- Signals close by assertion.
- Resolver overrides normal handoff authority.

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
| Mermaid source | `docs/content-dossiers/operations-project-system-improvement/diagrams/project-system-improvement-loop.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/operations-project-system-improvement-loop.png` |
| Manifest id | `comprehension_operations_project_system_improvement_loop` |
| Alt text | Diff or signal, classifier, resolver, one project-system AgentJob, receipt evidence, close or defer signal, and no hidden physics continuation. |
| Caption | Project-system improvement repairs machinery without becoming physics continuation. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Project-system improvement classifies a live problem, routes one bounded project-system packet, records evidence, and closes or defers explicitly.

## Unsafe summary

Unsafe summary: A project-system repair silently changes physics route, closes signals without evidence, replaces handoffs, or expands role authority.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/operations/project-system-improvement/`.
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

- AEther-Flow Project. (2026). `github-facing/project-system-improvement-explainer.md`.
