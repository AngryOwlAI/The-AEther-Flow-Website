# Project Overview Content Dossier

Status: Phase 1 pilot dossier.
Human review status: pending maintainer review.

## Route and reader job

- Public route: `/project/overview/`
- Reader job: understand The AEther Flow as one source-first research program
  with two linked tracks, then choose the correct internal route family.
- Primary audience: public readers and technical readers entering the project
  without prior repository context.
- Maintainer owner: website maintainer.
- Review status: ready for implementation review; maintainer acceptance still
  required.

## Current page summary

The current overview already presents the dual physics-and-AI structure and
uses internal route links as primary actions. It is visually strong, but it
does not yet use a dossier-backed comprehension block model or a static
Mermaid-authored public diagram asset. The rewrite should keep the command
interface visual language while adding clearer term definitions, source basis,
safe/unsafe summary, and a manifest-backed diagram.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/project-overview-explainer.md` | generated noncanonical reader surface | Primary source-derived overview framing, page families, boundaries, and safe/unsafe summary. |
| `README.md` | upstream project front door | Supports two-track project identity and first-entry framing referenced by the generated explainer. |
| `AGENTS.md` | upstream operating instructions | Supports source-authority and generated-output boundary language referenced by the generated explainer. |
| `research_control/README.md` | upstream research-control guide | Supports bounded task, AgentJob, validation, memory, completion, and handoff concepts referenced by the generated explainer. |
| `research_control/design/documentation_curator_publication_process.md` | upstream publication process | Supports publication brief, source spec, review, screenshots, and validation process referenced by the generated explainer. |

## Source-derived topic outline

1. State the project identity: a source-first research project with a physics
   lane and a governed research-agent workflow lane.
2. Explain the physics lane conservatively: exact-GR benchmark at observable
   scale, with first-principles substrate derivation still open.
3. Explain the AI research-agent lane as governed workflow, not autonomous
   physics authority.
4. Explain the source-authority spine: website explanations route readers back
   to source files, registries, and reviewed records.
5. Give internal route families by reader question before provenance links.
6. State what the overview cannot do.
7. Provide safe and unsafe summaries.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Physics lane | The public route family for ontology, exact-GR benchmark, derivation burden, current state, and claim gates. | It does not assert a completed derivation. |
| AI research-agent lane | The workflow route family for bounded tasks, roles, AgentJobs, validation, memory, completions, and handoffs. | It organizes research work; it does not own scientific decisions. |
| Source-authority spine | The rule that source files, registries, and governed records own claims while the website explains them. | Website clarity does not promote source status. |
| Generated noncanonical reader surface | A reviewed explanatory derivative that helps readers navigate source material. | It remains downstream from source authority. |
| Validator PASS | A deterministic check accepted the checked state. | It is not a scientific verdict or proof of editorial comprehension. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Exact-GR benchmark compatibility is not the same as a completed substrate
  derivation.
- The overview is a route map and public explanation, not a scientific source
  document.
- AI workflow evidence is operational evidence, not physics proof.
- Generated pages, screenshots, and diagrams are reader aids downstream from
  upstream source authority.
- Memory, wiki notes, semantic extracts, mirrors, and local caches are
  retrieval support only.

### Forbidden implications

- Do not imply that the overview proves general relativity from the ontology.
- Do not imply that AI agents autonomously own research decisions, authorship,
  or release accountability.
- Do not imply that a role, skill, or tool expands current task-local
  authority.
- Do not imply that a public diagram is source authority.
- Do not make GitHub the primary general-reader path when an internal route
  exists.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Must open from public project identity and reader job. |
| Plain summary | Yes | Must state the two-track model in simple language. |
| Mechanism steps | Yes | Use a short "how to read this project" sequence. |
| Term group | Yes | Define lane, source authority, generated derivative, and PASS. |
| Source basis | Yes | Show source paths as provenance. |
| Boundary block | Yes | State no derivation, no role expansion, no generated authority. |
| Diagram | Yes | Static Mermaid-authored PNG two-track project map. |
| Equation walkthrough | No | No equation walkthrough required for this route. |
| Safe/unsafe summary | Yes | Required because this is the front-door overclaim-control page. |
| Related internal routes | Yes | Physics, AI system, operations, source authority, resources. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/project-overview/diagrams/two-track-project-map.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/project-overview-two-track-map.png` |
| Manifest id | `comprehension_project_overview_two_track_map` |
| Alt text | Diagram showing The AEther Flow overview as two linked tracks: physics research and AI research-agent workflow, both downstream from source authority. |
| Caption | Static comprehension diagram: the overview routes readers through the physics lane, AI research-agent lane, and source-authority spine without promoting claims. |
| Nearby prose requirement | Explain that the diagram is an orientation aid and that source files and registries remain authoritative. |
| Review status | pending maintainer review |

## Equation walkthrough contract

No equation walkthrough required for this route. The overview does not display
or substantively derive equations.

## Safe summary

Safe summary: The AEther Flow is a source-first research project with a physics
program and a governed research-agent workflow; the overview helps readers
choose the right internal route and source lane.

## Unsafe summary

Unsafe summary: The overview proves a substrate derivation, makes generated
website material authoritative, grants role or validator authority, or turns
the AI workflow into autonomous scientific ownership.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/overview/`.
- Reason a new route is or is not justified: The accepted overview route
  already carries the first-entry reader job. The Phase 1 work should deepen
  this existing route rather than add a parallel public entry point.

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

AEther-Flow Project. (2026). `github-facing/project-overview-explainer.md`
[Generated noncanonical reader surface].

The AEther Flow Website. (2026). `AGENTS.md` [Repository operating rules].

The AEther Flow Website. (2026).
`public/files/manifests/page_route_map.json` [Route-to-source mapping contract].
