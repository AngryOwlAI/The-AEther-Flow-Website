# Project-System Improvement Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/operations/project-system-improvement/`
- Reader job: Understand how project-system signals, sidecars, classifiers, resolvers, one bounded AgentJob, and receipts repair the research machinery without changing physics status.
- Primary audience: general public, system engineers, software engineers, AI-system maintainers, and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

PG-020 rewrites the existing project-system improvement route around
observable signals, current diffs, classifiers, advisory resolver output,
source-bridged sidecars, one bounded project-system AgentJob, documentation
impact, PASS completion evidence, and signal close/defer/reject rules.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/project-system-improvement-explainer.md` | committed generated noncanonical reader source | Improvement loop, sidecar flow, resolver boundary, and reader scope. |
| `research_control/README.md` | committed control source | Documentation-impact, signal routing, resolver limits, and signal resolution evidence rules. |
| `scripts/project_control/README.md` | committed tooling source | Classifier, resolver, signal collection, sidecar generation, validation, and sidecar allowlist boundaries. |
| `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md` | committed schema source | Project-improvement sidecar field contract and source-bridge metadata. |
| `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv` | committed registry | Controlled signal vocabulary and default recommended skill/role routing. |
| `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv` | committed registry | Concrete signal instances, severity, status, evidence, and resolution fields. |
| `docs/system-analyses/project-system-improvement-loop.md` | website analysis | PG-020 route-specific review. |

## Source-derived topic outline

1. Observed diff, registered signal, repeated workflow problem, or source-bridged sidecar creates a maintenance input.
2. Classifier identifies documentation-impact and project-system reason codes.
3. Resolver ranks current diff state, open signals, and sidecar context but remains advisory.
4. One bounded project-system AgentJob executes the selected repair.
5. Documentation-impact and PASS completion evidence close, defer, or reject signals explicitly.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Signal | Tracked project-system problem or improvement indicator. | Not closed without matching evidence. |
| Signal type | Registered category such as documentation drift, validator gap, or routing ambiguity. | Type does not determine urgency alone. |
| Sidecar | Project-improvement support artifact generated from qualifying source-bridge evidence. | Input, not replacement research handoff. |
| Resolver | Advisory mechanism for ranking or choosing next project-system packet. | Not a hard checkpoint gate or physics selector. |
| Documentation impact | Receipt for state-changing project-system changes. | Operational evidence, not physics status. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Improvement packets stay project-system scoped.
- Receipts are required for signal closure.
- Sidecars are support inputs.
- Resolver output is advisory unless validators or concrete authority violations fail.
- Conditional sidecar acceptance is exact-path scoped.

### Forbidden implications

- Maintenance silently continues physics.
- Signals close by assertion.
- Resolver output alone blocks checkpointing.
- Sidecars replace normal research handoffs.
- Conditional sidecar acceptance becomes a global directory allowlist.
- Project-system packets promote physics claims or Gate Chair decisions.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with project-system maintenance versus physics-continuation boundary. |
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
| Alt text | Observed diff or registered signal, classifier, advisory resolver, source-bridged sidecar input, one project-system AgentJob, documentation-impact and PASS evidence, close defer or reject decision, and no hidden physics continuation or signal closure by prose. |
| Caption | Project-system improvement repairs research machinery through one bounded packet and explicit evidence; it does not become physics continuation. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Project-system improvement classifies a live problem, routes one bounded project-system packet, records documentation-impact and PASS evidence, and closes, defers, or rejects signals explicitly.

## Unsafe summary

Unsafe summary: A project-system repair silently changes physics route, closes signals without evidence, replaces handoffs, globally allowlists sidecars, or expands role authority.

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
- [x] Mobile layout and desktop layout were reviewed.
- [x] Human review note is recorded under `docs/quality/`.

## References

The AEther Flow. (2026a). *Project-system improvement loop*
[`github-facing/project-system-improvement-explainer.md`].

The AEther Flow. (2026b). *Research control*
[`research_control/README.md`].

The AEther Flow. (2026c). *Project-control scripts*
[`scripts/project_control/README.md`].

The AEther Flow. (2026d). *Project improvement handoff schema*
[`.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`].

The AEther Flow. (2026e). *Project improvement signal type registry*
[`registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`].

The AEther Flow. (2026f). *Project improvement signal registry*
[`registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`].
