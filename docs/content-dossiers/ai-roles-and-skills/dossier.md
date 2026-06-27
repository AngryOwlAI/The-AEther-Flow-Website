# Roles And Skills Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/ai-research-agent-system/roles-and-skills/`
- Reader job: Inspect role authority from registry status through current AgentJob allowlist.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/roles-and-skills-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/role-routing-explainer.md` | upstream source | Source basis for this route. |
| `registries/AGENT_ROLE_REGISTRY.csv` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Authority inspection order
2. Role and skill contracts
3. Execution-role record
4. AgentJob allowlist
5. Catalog overread prevention

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Registered role | Versioned role contract recorded upstream. | Not live permission by itself. |
| Task overlay | One-job adaptation of a role. | Not a reusable role version. |
| Skill | Governed procedure for a class of work. | Still subordinate to source authority and allowlist. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Public catalog visibility is not role activation.
- Human-gated roles remain protected.
- Task overlays stay local unless registered.

### Forbidden implications

- A role name grants current writes.
- A skill entry point grants blanket permission.
- Historical rows are active by visibility alone.

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
| Mermaid source | `docs/content-dossiers/ai-roles-and-skills/diagrams/role-authority-stack.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/ai-roles-authority-stack.png` |
| Manifest id | `comprehension_ai_roles_authority_stack` |
| Alt text | Role registry status, contract text, execution-role record, AgentJob allowlist, completion evidence, and public-catalog-is-not-permission boundary. |
| Caption | Role authority is task-local and record-bound. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Roles and skills help classify and execute work only when registry status, source contract, execution-role record, and current AgentJob allowlist are all respected.

## Unsafe summary

Unsafe summary: A role name, skill entry point, public catalog entry, or historical registry row grants current write authority or physics claim authority.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/ai-research-agent-system/roles-and-skills/`.
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

- AEther-Flow Project. (2026). `github-facing/roles-and-skills-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/role-routing-explainer.md`.
- AEther-Flow Project. (2026). `registries/AGENT_ROLE_REGISTRY.csv`.
