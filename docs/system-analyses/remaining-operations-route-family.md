# Remaining Operations Route Family

Status: PG-021 route-family audit.
Date: 2026-06-28.

## Question

Do the remaining operations routes read as one coherent, source-bound system,
without implying that operational success is scientific proof or live
authorization?

Routes in scope:

- `/project/operations/`
- `/project/operations/director-agentjob-lifecycle/`
- `/project/operations/role-routing/`
- `/project/operations/publication-process/`
- `/project/operations/technical-requirements/`

## Assumptions and constraints

- The routes explain operations. They do not change execution contracts,
  validators, roles, source registries, publication requirements, or physics
  status.
- Source claims are bound to the committed upstream repository state at
  `01efc4f180221caf9425fbb24683eb54927b553e`.
- Generated upstream explainers are useful reader surfaces, but their source
  material lists must be treated as provenance back to committed control files,
  schemas, registries, scripts, and tests.
- Website diagrams are static reader aids and not authority.

## Source review

The five routes were reviewed against the following committed upstream source
families:

- lifecycle source: generated lifecycle explainer, research-control guidance,
  Director/AgentJob/execution-role schemas, and related registries;
- role-routing source: generated role-routing explainer, role registry,
  execution-role registry, role schema, and execution-role schema;
- publication-process source: generated publication explainer, active
  Documentation Curator publication standard, role contract, publication brief
  registry, validator script, and pilot review evidence;
- technical-requirements source: generated technical-requirements explainer,
  project README, root AGENTS guidance, requirements ledger, Makefile, scripts
  guide, and tests guide;
- operations landing source: the synthesis of the route family above, plus
  research-control, publication, project-control, and test evidence.

## Findings

1. The routes already use the shared layered `InternalExplainerPage` model.
   The main gap was not page structure; it was source-basis visibility.

2. The strongest operational claims depend on committed control sources, not
   only on generated GitHub-facing explainers. The route map therefore needs
   expanded upstream paths so the rendered source notice exposes the audit
   trail.

3. The family has a single invariant: operational evidence narrows and records
   work, but does not promote scientific claims. This invariant appears in the
   lifecycle, role-routing, publication, technical-requirements, validator, and
   project-system pages and should remain visible in each route.

4. Full new system analyses are not necessary for each low-risk operational
   child route in PG-021. A route-family audit is sufficient because the pages
   are existing explanations and no execution contract is changed.

## Page-specific conclusions

| Route | Main correction | Boundary to preserve |
| --- | --- | --- |
| `/project/operations/` | Expose synthesis sources beyond the six generated explainers. | Operations are a control spine, not scientific authority. |
| `/project/operations/director-agentjob-lifecycle/` | Bind lifecycle prose to schemas, registries, and immutable-record guidance. | Completion evidence remains transaction-local. |
| `/project/operations/role-routing/` | Bind role prose to role and execution-role registries/schemas. | Role labels do not grant live permission. |
| `/project/operations/publication-process/` | Bind publication prose to the active publication standard and validator evidence. | Readable public pages remain downstream from source authority. |
| `/project/operations/technical-requirements/` | Bind tooling prose to environment, dependency, script, and test sources. | Tool availability is reproducibility support, not authorization. |

## Implementation decision

Use one route-family audit plus metadata/content tightening:

- update source references and source links for the five route-family pages;
- update `page_route_map.json` so generated page provenance lists committed
  upstream control sources;
- keep all pages on the layered explainer model;
- add anti-overread copy where a reader might confuse completion, role label,
  publication quality, or tool capability with authority.

No runtime behavior, validator behavior, role contract, schema, registry, or
publication requirement is changed.

## Limitations

This audit does not validate scientific claims and does not inspect every
historical operation record. It verifies the reader-facing route family against
the current committed source basis and checks that the pages do not overstate
operational evidence.

## Recommendation

Treat PG-021 as complete when route provenance is regenerated, page validation
passes, the known curator drift is the only remaining global validation
failure, and desktop/mobile screenshots show the operations family with no
obvious layout overflow.

## References

The AEther Flow. (2026). `github-facing/director-agentjob-lifecycle-explainer.md`.

The AEther Flow. (2026). `github-facing/role-routing-explainer.md`.

The AEther Flow. (2026). `github-facing/documentation-curator-publication-process-explainer.md`.

The AEther Flow. (2026). `github-facing/technical-requirements-explainer.md`.

The AEther Flow. (2026). `research_control/README.md`.

The AEther Flow. (2026). `research_control/design/documentation_curator_publication_process.md`.

The AEther Flow. (2026). `.agents/schemas/AGENT_JOB_SCHEMA.md`.

The AEther Flow. (2026). `registries/AGENT_ROLE_REGISTRY.csv`.
