# Specialist Guided Starts

Status: PG-025 system analysis.
Quality gate: pass.
Date: 2026-06-28.

## Question

How should the website provide first-class specialist guided starts for
physicists, mathematicians, AI/agent researchers, software/system engineers,
and external reviewers without creating new scientific or workflow claims?

## Assumptions and constraints

- Guided starts assemble existing sourced website routes.
- They may recommend reading order and state audience-specific caution.
- They must not duplicate or strengthen high-risk claim copy.
- The external reviewer path must remain a prerequisite path until PG-026
  creates the dedicated reviewer packet.
- Source links remain provenance; internal routes remain the primary reader
  journey.

## Source review

Reviewed website and source-bound route families:

- `/`: public two-track Home orientation.
- `/project/physics/`: physics route family for ontology, exact-GR benchmark,
  current state, Distance-to-GR, source extension, frozen routes, and claim
  gates.
- `/project/ai-research-agent-system/`: AI workflow route family for AgentJobs,
  roles, memory, parent-child synthesis, and validation limits.
- `/project/operations/`: operational route family for lifecycle, role routing,
  validator limits, publication, improvement, and tool requirements.
- `/project/source-authority/`: trust boundary, claim-boundary explorer, and
  publication/provenance system.
- `/resources/documents/`: ontology document reading guide.
- `/resources/diagrams/`: visual aids by concept.
- `public/files/manifests/page_route_map.json`: route inventory and publication
  status.

## Route model

The foundation contract permits guided starts as either child routes or a
strong hub with audience sections. PG-025 should use one hub route:
`/resources/guided-starts/`.

Reasoning:

1. The specialist audiences share the same source-authority boundary.
2. The route is a navigation layer, not a new claim-bearing topic page.
3. Anchored sections avoid duplicating high-risk claim summaries.
4. The future reviewer packet can become a separate route in PG-026 after this
   prerequisite path exists.

## Audience paths

### Physicists

Reader job: inspect current physics status, ontology, exact-GR benchmark
boundary, open derivation burden, and claim gates.

Do not infer: exact-GR benchmark compatibility is a completed first-principles
derivation, or that `g_eff`, matter coupling, Einstein equations, benchmark
promotion, or downstream GR promotion are complete.

### Mathematicians

Reader job: inspect definitions, route burdens, obstruction structure, finite
toy model limits, and no-target-import discipline.

Do not infer: local route freeze is global impossibility, or that a diagram or
reading path supplies missing existence, uniqueness, regularity, or
construction proof.

### AI/agent researchers

Reader job: inspect bounded AgentJobs, role authority, memory retrieval,
parent-child synthesis, validation limits, and handoff discipline.

Do not infer: AI workflow owns scientific decisions, validator PASS is proof,
or role labels grant live authority without task-local records.

### Software/system engineers

Reader job: inspect system operation, validator boundaries, publication
provenance, technical requirements, and project-system repair loops.

Do not infer: tool capability is authorization, build success is scientific
truth, or publication manifests replace source review.

### External reviewers

Reader job: read prerequisites before PG-026 reviewer packet: current state,
Distance-to-GR, source authority, claim boundaries, ontology documents, and
specialist path matching the reviewer's discipline.

Do not infer: this prerequisite path is the reviewer packet or a review
invitation with completed scientific claims.

## Claim boundaries

Safe:

- A guided-start hub can route each audience to existing internal pages.
- It can warn against overreads already blocked by sourced pages.
- It can stage reviewers toward prerequisites before PG-026.

Unsafe:

- The hub creates new scientific, mathematical, AI, operational, or reviewer
  claims.
- The hub updates current source state.
- The hub converts public explanation, diagrams, validators, manifests, or
  reading order into proof or release approval.

## Implementation recommendation

Create `/resources/guided-starts/` with:

- one public summary of what guided starts do;
- five anchored audience sections;
- explicit "read first", "then inspect", and "do not infer" language;
- internal-first cards only;
- one static Mermaid-derived PNG showing the hub as a routing layer;
- route-map, provenance, source-manifest, asset-manifest, and
  public-comprehension validator coverage.

## Limitations

This analysis does not create the PG-026 external reviewer packet and does not
change the status of any scientific or operational source. It only defines
safe reading order for specialist audiences.

## References

The AEther Flow Website. (2026). `/`.

The AEther Flow Website. (2026). `/project/physics/`.

The AEther Flow Website. (2026). `/project/ai-research-agent-system/`.

The AEther Flow Website. (2026). `/project/operations/`.

The AEther Flow Website. (2026). `/project/source-authority/`.

The AEther Flow Website. (2026). `/resources/documents/`.

The AEther Flow Website. (2026). `/resources/diagrams/`.

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`.
