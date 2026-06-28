# Operations Content Dossier

Status: evidence-reviewed draft dossier.

## Route and reader job

- Public route: `/project/operations/`
- Reader job: Understand operations as the source-first control spine for bounded work.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## PG-021 route-family evidence review

- Review artifact: `docs/system-analyses/remaining-operations-route-family.md`.
- Review decision: Use the existing layered page model and tighten source
  basis/provenance instead of creating a new route or changing operational
  contracts.
- Source state: Committed upstream source at
  `01efc4f180221caf9425fbb24683eb54927b553e`.
- Boundary: This route synthesizes the operations family and cannot authorize
  work, change validators, change roles, close signals, or promote physics
  claims.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/director-agentjob-lifecycle-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/role-routing-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/validator-operator-workflow-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/documentation-curator-publication-process-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/project-system-improvement-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/technical-requirements-explainer.md` | upstream source | Source basis for this route. |
| `research_control/README.md` | upstream control source | Source basis for routing, validation, and evidence boundaries. |
| `research_control/design/documentation_curator_publication_process.md` | upstream control source | Source basis for publication discipline. |
| `scripts/project_control/README.md` | upstream tooling source | Source basis for project-system classifier, resolver, sidecar, and receipt workflows. |
| `tests/README.md` | upstream tooling source | Source basis for test evidence boundaries. |

## Source-derived topic outline

1. Director routing
2. AgentJob allowlist
3. Execution-role evidence
4. Validators and completion
5. Handoff and registry evidence

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Operations | Project-control practices that route, execute, validate, publish, improve, and reproduce work. | Not a scientific result. |
| Completion evidence | Record of outputs, checks, verdict, uncertainty, and next step. | Not claim promotion. |
| Handoff | Bounded next-step record. | Not current authority extension. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Operations pages are explanatory.
- Auditability is not theorem proof.
- Generated pages cannot change validators or roles.

### Forbidden implications

- Operations pages authorize work.
- Process evidence proves physics.
- Validator PASS becomes source authority.

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
| Mermaid source | `docs/content-dossiers/operations/diagrams/operations-control-spine.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/operations-control-spine.png` |
| Manifest id | `comprehension_operations_control_spine` |
| Alt text | Request, Director decision, AgentJob, execution role, validators, completion, handoff, and operational-evidence-is-not-physics-proof boundary. |
| Caption | Operations keep work auditable while preserving source and claim boundaries. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Operations explain how bounded work is routed, executed, checked, recorded, published, and improved without changing source authority.

## Unsafe summary

Unsafe summary: Operations pages authorize work, promote claims, prove physics, rewrite activated records, or make validator PASS broader than the checked state.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/operations/`.
- Reason a new route is or is not justified: The existing route is the correct public surface for this content.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [x] Mobile layout and desktop layout were reviewed for PG-021.
- [x] Human review note is recorded under `docs/quality/sitewide-revamp-pg021-remaining-operations-family-qa.md`.

## References

- AEther-Flow Project. (2026). `github-facing/director-agentjob-lifecycle-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/role-routing-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/validator-operator-workflow-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/documentation-curator-publication-process-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/project-system-improvement-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/technical-requirements-explainer.md`.
- AEther-Flow Project. (2026). `research_control/README.md`.
- AEther-Flow Project. (2026). `research_control/design/documentation_curator_publication_process.md`.
- AEther-Flow Project. (2026). `scripts/project_control/README.md`.
- AEther-Flow Project. (2026). `tests/README.md`.
