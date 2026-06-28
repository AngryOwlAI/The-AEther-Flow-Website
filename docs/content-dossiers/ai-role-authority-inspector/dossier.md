# Role Authority Inspector Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/ai-research-agent-system/role-authority-inspector/`
- Reader job: Inspect role authority without mistaking role labels or registry
  visibility for live permissions.
- Primary audience: general public, AI-system developers, system engineers,
  and maintainers reviewing role-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

PG-017 creates a new static inspector route for role authority. It explains the
inspection order from role registry through current AgentJob allowlist and
uses representative committed registry rows to show how active, superseded,
and human-gated roles should be read.

The route must not turn a registry display into permission grant and must not
expose private local operational details.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `registries/AGENT_ROLE_REGISTRY.csv` | committed registry | Representative role rows and field semantics. |
| `github-facing/roles-and-skills-explainer.md` | committed generated noncanonical reader source | Catalog visibility and role/skill boundary. |
| `github-facing/role-routing-explainer.md` | committed generated noncanonical reader source | Role routing stack and execution-role distinctions. |
| `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` | committed schema source | Execution-role kinds and one-job authority. |
| `.agents/schemas/AGENT_JOB_SCHEMA.md` | committed schema source | Allowlist, validators, outputs, and claim boundary. |
| `research_control/README.md` | committed control source | Authority model and one-job rule. |
| `docs/system-analyses/role-authority-inspector.md` | website analysis | PG-017 route-specific review. |

## Source-derived topic outline

1. Role label is not live permission.
2. Registry row gives identity, version, status, authority level, gate status,
   defaults, and notes.
3. Role contract supplies source text.
4. Execution-role record binds one job through `registered_role`,
   `task_overlay`, or `one_job_provisional_role`.
5. AgentJob allowlist controls actual reads, writes, outputs, validators, and
   claim boundary.
6. Completion evidence records what passed.
7. Human-gated authority remains protected.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Registered role | Versioned role template recorded in the role registry. | Not live permission by itself. |
| Active status | Registry status indicating the current base role version. | Still needs an execution-role record and AgentJob. |
| Superseded status | Historical row kept for old execution records. | Not current role authority. |
| Human-gated role | Role whose protected action requires explicit human approval. | Row visibility is not approval. |
| Task overlay | One-job adjustment of a registered role. | Not a reusable role version. |
| One-job provisional role | Temporary role identity for one AgentJob. | Expires unless registered through the proper path. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Registry rows are source evidence for role status.
- Public pages summarize; they do not register roles.
- Active role status is not current write permission.
- Execution-role records are task-local.
- AgentJob allowlists control actual transaction authority.
- Human-gated roles require explicit tracked approval.

### Forbidden implications

- A role name grants current writes.
- A public catalog entry activates a role.
- A superseded row is active because it is visible.
- A task overlay becomes reusable by habit.
- A provisional role persists after its owning AgentJob.
- Gate Chair row visibility authorizes claim promotion.
- Documentation pages can register roles or promote claims.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with role-label versus live-permission boundary. |
| Plain summary | yes | Provided in page lead and safe summary. |
| Mechanism steps | yes | Registry, contract, execution role, AgentJob, completion, human gate. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Sources listed above and rendered as provenance. |
| Boundary block | yes | Permission, supersession, gate, overlay, provisional-role, and catalog limits. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required for this route. |
| Safe/unsafe summary | yes | High-risk overread prevention. |
| Related internal routes | yes | Internal-first reader journey before provenance links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/ai-role-authority-inspector/diagrams/role-authority-inspection-stack.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/ai-role-authority-inspector-stack.png` |
| Manifest id | `comprehension_ai_role_authority_inspector_stack` |
| Alt text | Role authority inspection stack from role label to registry row, contract, execution-role record, AgentJob allowlist, completion evidence, and human gate boundary. |
| Caption | Role labels and registry rows support inspection; live authority comes from task-local execution records and AgentJob allowlists. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: role authority is inspectable only by reading the registry row,
role contract, execution-role record, current AgentJob allowlist, completion
evidence, and any required human gate.

## Unsafe summary

Unsafe summary: a role label, public catalog entry, active registry status, or
historical row grants current write permission or physics claim authority.

## New-page audit

- Is a new public page proposed? Yes.
- Existing route that should be used instead: none; PG-017 explicitly creates
  `/project/ai-research-agent-system/role-authority-inspector/`.
- Reason a new route is justified: the existing roles-and-skills page is a
  catalog overview; this route focuses on role authority inspection.

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

The AEther Flow. (2026a). *Agent role registry*
[`registries/AGENT_ROLE_REGISTRY.csv`].

The AEther Flow. (2026b). *Roles and skills catalog*
[`github-facing/roles-and-skills-explainer.md`].

The AEther Flow. (2026c). *Role routing and execution contracts*
[`github-facing/role-routing-explainer.md`].

The AEther Flow. (2026d). *Execution-role schema*
[`.agents/schemas/EXECUTION_ROLE_SCHEMA.md`].

The AEther Flow. (2026e). *AgentJob schema*
[`.agents/schemas/AGENT_JOB_SCHEMA.md`].
