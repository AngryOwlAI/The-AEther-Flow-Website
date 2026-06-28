# Director Decisions And AgentJob Lifecycle Content Dossier

Status: evidence-reviewed draft dossier.

## Route and reader job

- Public route: `/project/operations/director-agentjob-lifecycle/`
- Reader job: Understand how task, decision, AgentJob, evidence, completion, and handoff narrow authority.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## PG-021 route-family evidence review

- Review artifact: `docs/system-analyses/remaining-operations-route-family.md`.
- Review decision: Preserve the existing lifecycle route and bind its claims to
  committed schemas, registries, and immutable-record guidance.
- Source state: Committed upstream source at
  `01efc4f180221caf9425fbb24683eb54927b553e`.
- Boundary: Lifecycle records narrow and evidence one transaction; completion
  evidence does not promote scientific claims or expand authority.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/director-agentjob-lifecycle-explainer.md` | upstream source | Source basis for this route. |
| `research_control/README.md` | upstream control source | Source basis for research-control operating model. |
| `research_control/AGENTS.md` | upstream scoped guidance | Source basis for immutable activated-record and supersession rules. |
| `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md` | upstream schema | Source basis for Director decision fields. |
| `.agents/schemas/AGENT_JOB_SCHEMA.md` | upstream schema | Source basis for AgentJob allowlist and stop conditions. |
| `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` | upstream schema | Source basis for execution-role records. |
| `registries/DIRECTOR_DECISION_REGISTRY.csv` | upstream registry | Source basis for Director decision discovery. |
| `registries/AGENT_JOB_REGISTRY.csv` | upstream registry | Source basis for AgentJob discovery. |
| `registries/ROLE_EXECUTION_REGISTRY.csv` | upstream registry | Source basis for execution-role discovery. |

## Source-derived topic outline

1. Task row
2. Director decision
3. AgentJob
4. Execution-role and validation evidence
5. Completion and handoff

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Task row | Tracked problem statement and state pointer. | Not permission outside current route. |
| Execution-role evidence | Record binding role semantics to one job. | Not reusable authority. |
| Supersession | Repair through a new bounded packet. | Not silent mutation. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Correct by supersession, not silent mutation.
- Gates remain separate.
- One job remains one transaction.

### Forbidden implications

- Lifecycle records expand authority.
- Activated records can be quietly rewritten.
- Completion promotes source claims.

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
| Mermaid source | `docs/content-dossiers/operations-director-agentjob-lifecycle/diagrams/director-agentjob-record-chain.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/operations-director-agentjob-record-chain.png` |
| Manifest id | `comprehension_operations_director_agentjob_record_chain` |
| Alt text | Task row, Director decision, AgentJob, execution-role evidence, command evidence, completion, handoff, and no silent authority expansion. |
| Caption | The lifecycle records why one transaction was authorized and how it closed. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: The lifecycle page explains how one bounded task becomes a decision, an AgentJob, evidence, completion, and possibly a handoff.

## Unsafe summary

Unsafe summary: A lifecycle diagram expands authority, rewrites activated records, bypasses protected gates, or changes physics status.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/operations/director-agentjob-lifecycle/`.
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
- AEther-Flow Project. (2026). `research_control/README.md`.
- AEther-Flow Project. (2026). `research_control/AGENTS.md`.
- AEther-Flow Project. (2026). `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`.
- AEther-Flow Project. (2026). `.agents/schemas/AGENT_JOB_SCHEMA.md`.
- AEther-Flow Project. (2026). `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`.
- AEther-Flow Project. (2026). `registries/DIRECTOR_DECISION_REGISTRY.csv`.
- AEther-Flow Project. (2026). `registries/AGENT_JOB_REGISTRY.csv`.
- AEther-Flow Project. (2026). `registries/ROLE_EXECUTION_REGISTRY.csv`.
