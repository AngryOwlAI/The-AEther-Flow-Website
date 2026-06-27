# Role Routing And Execution Contracts Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/operations/role-routing/`
- Reader job: Understand why role labels become current only through task-local records and allowlists.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/role-routing-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/roles-and-skills-explainer.md` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Role template
2. Task overlay or provisional role
3. Execution-role record
4. AgentJob allowlist
5. Outputs and validators

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Role template | Reusable role definition. | Not current write permission. |
| Provisional role | Temporary one-job role. | Expires unless registered. |
| Allowlist | Current transaction permitted paths and outputs. | Cannot be expanded by page prose. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Labels do not grant writes.
- Public pages cannot register roles.
- Allowlists are job-local.

### Forbidden implications

- Role name is live permission.
- Task overlay becomes permanent by habit.
- Page copy expands allowlists.

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
| Mermaid source | `docs/content-dossiers/operations-role-routing/diagrams/role-routing-allowlist-stack.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/operations-role-routing-allowlist-stack.png` |
| Manifest id | `comprehension_operations_role_routing_allowlist_stack` |
| Alt text | Registered role, task overlay or provisional role, execution-role record, AgentJob allowlist, outputs, validators, and role name is not live permission. |
| Caption | Current authority lives in the job-specific allowlist, not in the label alone. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Role routing requires registry status, source contract, execution-role record, AgentJob allowlist, outputs, and validators to be read together.

## Unsafe summary

Unsafe summary: A role label, task overlay, provisional role, or public page grants authority outside the current AgentJob.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/operations/role-routing/`.
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

- AEther-Flow Project. (2026). `github-facing/role-routing-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/roles-and-skills-explainer.md`.
