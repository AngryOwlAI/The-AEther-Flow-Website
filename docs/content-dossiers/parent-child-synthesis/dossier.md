# Parent-Child Synthesis Content Dossier

Status: Phase 1 pilot dossier.
Human review status: pending maintainer review.

## Route and reader job

- Public route: `/project/ai-research-agent-system/parent-child-synthesis/`
- Reader job: understand parent-child synthesis as an internal perspective
  structure inside one future physics AgentJob, not as extra jobs or extra
  authority.
- Primary audience: readers inspecting AI research-agent workflow mechanics and
  authority boundaries.
- Maintainer owner: website maintainer.
- Review status: ready for implementation review; maintainer acceptance still
  required.

## Current page summary

The current route renders through `InternalExplainerPage` and already explains
the one-job frame, inherited authority, child `draft/control` status, blocking
conflicts, and fused output. The rewrite should make the one-outer-AgentJob
invariant the first substantive comprehension block, add a static
Mermaid-authored diagram, add term definitions, and keep safe/unsafe summaries
visible.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/parent-child-synthesis-explainer.md` | generated noncanonical reader surface | Primary source-derived explanation of the one outer AgentJob invariant, internal units, inherited authority, conflicts, and safe/unsafe summary. |
| `README.md` | upstream project front door | Supports project-level context. |
| `AGENTS.md` | upstream operating instructions | Supports source hierarchy and authority-boundary framing referenced by the generated explainer. |
| `research_control/README.md` | upstream research-control guide | Supports AgentJob lifecycle, validation, and completion concepts referenced by the generated explainer. |
| `research_control/AGENTS.md` | upstream scoped guidance | Supports research-control operating constraints referenced by the generated explainer. |
| `.agents/schemas/AGENT_JOB_SCHEMA.md` | upstream schema | Supports AgentJob contract, conflict policy, and bounded write concepts referenced by the generated explainer. |
| `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` | upstream schema | Supports execution-role singularity and role-boundary concepts referenced by the generated explainer. |
| `registries/AGENT_JOB_REGISTRY.csv` | upstream registry | Supports AgentJob registry evidence path referenced by the generated explainer. |

## Source-derived topic outline

1. Open with the invariant: one Director decision, one outer AgentJob, one
   execution-role record, one completion record, and one fused output.
2. Explain why internal child perspectives exist: broader analytical coverage
   for difficult physics packets.
3. Explain inherited authority: same claim boundary, source restrictions,
   write allowlist, validators, human-gate status, and stop conditions.
4. Explain child output status: supporting `draft/control` artifacts without
   independent authority.
5. Explain blocking conflict behavior: unresolved blocking conflict prevents a
   valid PASS completion.
6. Explain fused output: one final downstream artifact tied to one completion
   and handoff path.
7. State scope limits: future physics AgentJobs, not mandatory for all
   project-system or documentation work.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Outer AgentJob | The single executable job that owns reads, writes, validators, expected outputs, and stop conditions. | Child perspectives cannot add a second job. |
| Parent unit | The review-and-fusion unit that enforces the shared boundary and produces the final artifact. | It cannot ignore declared blocking conflicts. |
| Child unit | An analytical perspective used to inspect one problem from a specific angle. | Its output is supporting `draft/control`, not an independent verdict. |
| Fused output | The one final artifact used for completion, handoff, and downstream reference. | It is the only downstream output of the parent-child packet. |
| Blocking conflict | A declared disagreement that must be reviewed and resolved or leave the job blocked. | PASS is invalid while it remains unresolved. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Parent-child synthesis is scoped to a future physics AgentJob pattern.
- It preserves one Director decision, one outer AgentJob, one execution-role
  record, one completion record, and one fused output.
- Child outputs inherit the outer job's authority, claim boundary, source
  restrictions, write allowlist, validators, human-gate status, and stop
  conditions.
- Child outputs are supporting `draft/control` artifacts.
- A declared blocking conflict must be reviewed and resolved, or the job
  remains blocked.

### Forbidden implications

- Do not imply child outputs are independent verdicts.
- Do not imply child units create extra AgentJobs, role records, validators, or
  write authority.
- Do not imply parent-child synthesis is a way around human gates or source
  restrictions.
- Do not imply a parent can select a convenient child and ignore a declared
  blocking conflict.
- Do not imply the mode is mandatory for all non-physics work.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Must identify the page as workflow orientation. |
| Plain summary | Yes | Must state the one-outer-AgentJob invariant. |
| Mechanism steps | Yes | Parent review, child drafts, conflict review, fusion, completion. |
| Term group | Yes | Define parent, child, outer AgentJob, fused output, blocking conflict. |
| Source basis | Yes | Show source paths as provenance. |
| Boundary block | Yes | No extra authority, no extra jobs, no claim promotion. |
| Diagram | Yes | Static Mermaid-authored PNG single-outer-AgentJob frame. |
| Equation walkthrough | No | No equation walkthrough required for this route. |
| Safe/unsafe summary | Yes | Required because authority confusion risk is high. |
| Related internal routes | Yes | AI system, roles and skills, Director/AgentJob lifecycle. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/parent-child-synthesis/diagrams/single-outer-agentjob-frame.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png` |
| Manifest id | `comprehension_parent_child_single_outer_agentjob` |
| Alt text | Diagram showing one outer AgentJob containing parent review, child draft/control perspectives, conflict review, and one fused output. |
| Caption | Static comprehension diagram: parent-child synthesis adds internal perspectives inside one bounded AgentJob, not extra jobs or independent authority. |
| Nearby prose requirement | Explain that every internal unit inherits the outer job's claim boundary, allowlist, validators, and stop conditions. |
| Review status | pending maintainer review |

## Equation walkthrough contract

No equation walkthrough required for this route. The page explains workflow
mechanics rather than displaying or deriving equations.

## Safe summary

Safe summary: Parent-child synthesis is an internal perspective structure
inside one physics AgentJob; child outputs support parent review, and only the
fused output enters completion and downstream references.

## Unsafe summary

Unsafe summary: Parent-child synthesis creates extra jobs, extra role records,
extra write authority, independent child verdicts, a path around conflict
review, or a mandatory mode for all non-physics work.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead:
  `/project/ai-research-agent-system/parent-child-synthesis/`.
- Reason a new route is or is not justified: The existing route already maps to
  the upstream parent-child explainer and should be remediated in place.

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

AEther-Flow Project. (2026).
`github-facing/parent-child-synthesis-explainer.md` [Generated noncanonical
reader surface].

The AEther Flow Website. (2026). `AGENTS.md` [Repository operating rules].

The AEther Flow Website. (2026).
`public/files/manifests/page_route_map.json` [Route-to-source mapping contract].
