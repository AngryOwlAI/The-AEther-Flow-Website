# Codex Task Packets: Website Information-Space PRD Conversion

Source plan:
`ImplementationPlans/website-information-space/PRD-00-master-website-information-space-implementation-plan.md`

Source PRD:
`PRDs/website-information-space/PRD-00-master-website-information-space.md`

Execution rule: convert one PRD per implementation-control packet. Do not
implement public routes, public assets, public manifests, source refreshes,
generated derivatives, retrieval layers, upstream source writes, push, or
deployment from these planning packets.

Shared closeout requirement: every packet must report changed files,
requirements mapped, task packets created, validators run, skipped checks with
concrete reasons, remaining assumptions, and the next governed packet.

Shared validation profile:

- `git diff --check`
- `npm run validate:implementation-control`
- `.venv/bin/python -m pytest`
- Manual review of implementation-control YAML and Markdown records

## Task MIP-00: Convert PRD-00 To Master Implementation Plan

### Goal

Create the master website-information-space implementation plan, the master
conversion task-packet set, and the implementation-plan directory index.

### Context

- PRD requirements: PRD-00 sections 1 through 24.
- Relevant files:
  - `PRDs/website-information-space/PRD-00-master-website-information-space.md`
  - `PRDs/website-information-space/README.md`
  - `PRDs/website-information-space/PRD-FAMILY-VALIDATION-REVIEW.md`
  - `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
  - `ImplementationPlans/sitewide_greenfield_rebuild_task_packets.md`
- Existing patterns: implementation-control packets are the governing
  execution surface.

### Constraints

- Do not convert sub-PRDs in this packet.
- Do not implement public routes.
- Treat the sitewide greenfield rebuild plan as canonical.
- Record the display-spelling rule: `Æther` for reader-facing text; `aether`
  for links, slugs, and file naming.

### Implementation notes

- Create `ImplementationPlans/website-information-space/README.md`.
- Create the PRD-00 master implementation plan.
- Create this master conversion task-packet file.
- Complete `WI-20260630-015` only after validation evidence exists.

### Acceptance criteria

- [x] The directory index records conversion order and scope boundaries.
- [x] The master plan maps PRD-00 requirements to future implementation areas.
- [x] This task-packet file defines one packet per remaining sub-PRD.
- [x] Canonical greenfield constraints and the display-spelling rule are
      explicit.

### Validation

- `git diff --check`
- `npm run validate:implementation-control`
- `.venv/bin/python -m pytest`

### Done when

The master conversion outputs exist, control records are complete, validators
pass, and the next packet is limited to the first sub-PRD conversion.

## Task MIP-10: Convert PRD-10 Positioning Guidance

### Goal

Create the positioning and public-language sub implementation plan from
`PRD-10-website-positioning-guidance.md`.

### Context

- PRD requirements: approved phrasing, forbidden claims, homepage guidance,
  audience-specific pitch, SEO language, copy QA.
- Relevant future surfaces: Home, category introductions, physics pages, AI
  workflow pages, source-authority context copy.
- Existing patterns: source-authority boundary and greenfield intro paragraph
  rule.

### Constraints

- Do not write public copy in this packet.
- Do not claim completed GR derivation, solved matter coupling, benchmark
  promotion from first principles, or autonomous AI proof.
- Use `Æther` for reader-facing text and preserve existing machine identifiers.

### Implementation notes

- Map approved and forbidden language to reusable implementation guidance.
- Define copy-review checks future route packets must run before closeout.
- Identify which greenfield routes depend on PRD-10.

### Acceptance criteria

- [ ] A PRD-10 sub implementation plan exists.
- [ ] A PRD-10 task-packet set exists.
- [ ] Forbidden-claim QA terms are explicit and non-endorsing.
- [ ] Future Home and category packets can cite the positioning plan.

### Validation

- Shared validation profile.

### Done when

The positioning plan can govern future public-copy packets without changing any
public route in this packet.

## Task MIP-05: Convert PRD-05 Source Authority, Registry, Memory, And Retrieval

### Goal

Create the source-authority, registry, memory, retrieval, provenance, and
source/provenance footer sub implementation plan.

### Context

- PRD requirements: authority classes, canonical sources, registries,
  generated derivatives, memory, local retrieval layers, provenance behavior.
- Relevant future surfaces: `/resources/source-authority/`,
  `/resources/registries/`, `/resources/retrieval-layers/`, footer,
  source-bundle metadata.

### Constraints

- Do not treat memory, generated pages, registries, or validators as proof.
- Do not write public manifests.
- Do not add a dedicated `Source authority` section to library/resource pages
  where repository rules prohibit it.

### Implementation notes

- Define source-bundle fields required by future route packets.
- Map authority classifications to route metadata and provenance validation.
- Identify freshness-sensitive and non-authority layers.

### Acceptance criteria

- [ ] A PRD-05 sub implementation plan exists.
- [ ] A PRD-05 task-packet set exists.
- [ ] Source-authority classifications are mapped to future page contracts.
- [ ] Footer and provenance expectations are explicit.

### Validation

- Shared validation profile.

### Done when

Future route packets have source-bundle and provenance rules before public
claim-bearing copy is written.

## Task MIP-06: Convert PRD-06 Documentation, Publication, And Website Components

### Goal

Create the documentation, publication, library, generated-derivative, and
website-component sub implementation plan.

### Context

- PRD requirements: publication workflow, documentation layers, library
  surfaces, parity expectations, generated-derivative warnings, source-backed
  footer design.
- Relevant future surfaces: `/resources/generated-derivatives/`,
  `/resources/publication-process/`, `/resources/library/`,
  `/resources/diagrams/`.

### Constraints

- Do not refresh generated HTML, GitHub-facing Markdown, wiki, PDFs, diagrams,
  or local retrieval layers.
- Do not publish public assets or manifests.
- Preserve derivative-versus-authority distinctions.

### Implementation notes

- Map publication workflow to future route tasks.
- Define when diagram-gallery and library packets need manifest validation.
- Preserve the canonical greenfield Diagram Gallery reset rule.

### Acceptance criteria

- [ ] A PRD-06 sub implementation plan exists.
- [ ] A PRD-06 task-packet set exists.
- [ ] Generated derivative boundaries and library behavior are mapped.
- [ ] Diagram workflow expectations are linked to greenfield constraints.

### Validation

- Shared validation profile.

### Done when

Future publication and library packets have route, provenance, manifest, and
diagram-validation guidance.

## Task MIP-01: Convert PRD-01 High-Level Components

### Goal

Create the Home, project-overview, dual-track framing, trust-panel, and primary
reader-journey sub implementation plan.

### Context

- PRD requirements: first-visit understanding, homepage, project overview,
  dual physics-and-AI framing, internal-first reader journeys.
- Relevant future surfaces: `/`, `/resources/reading-paths/`, category
  overview pages.

### Constraints

- Do not implement the Home route in this packet.
- Align all public-language guidance with the PRD-10 sub plan.
- Align all provenance and source-boundary behavior with the PRD-05 sub plan.

### Implementation notes

- Map high-level reader journeys onto the greenfield route model.
- Define first-viewport, intro paragraph, trust signal, and related-route
  requirements.
- Identify which future tasks need browser QA.

### Acceptance criteria

- [ ] A PRD-01 sub implementation plan exists.
- [ ] A PRD-01 task-packet set exists.
- [ ] Home and overview implementation tasks are traceable to PRD-01.
- [ ] Internal-first route guidance is explicit.

### Validation

- Shared validation profile.

### Done when

The Home and high-level public story can be implemented under a later route
packet without revisiting master requirements.

## Task MIP-02: Convert PRD-02 Physics And Mathematical Components

### Goal

Create the physics and mathematics sub implementation plan for ontology,
exact-GR benchmark, derivation roadmap, flow geometry, claim status, and open
burdens.

### Context

- PRD requirements: ontology, exact-GR benchmark, adoption-versus-derivation
  boundary, derivation roadmap, flow geometry, mathematical caution,
  open-burden visibility.
- Relevant future surfaces: `/physics/`, `/physics/ontology/`,
  `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`,
  `/physics/flow-geometry/`, `/physics/claim-status/`,
  `/physics/open-burdens/`.

### Constraints

- Do not claim GR, matter coupling, Einstein equations, or benchmark promotion
  are derived from source-side substrate structure.
- Do not treat ontology vocabulary as equation-level proof.
- Do not write or refresh upstream physics sources.

### Implementation notes

- Map each physics page to source-bundle requirements and forbidden inferences.
- Define diagram, table, glossary, and matrix forms that serve explanation.
- Identify where current-frontier freshness from PRD-09 is required.

### Acceptance criteria

- [ ] A PRD-02 sub implementation plan exists.
- [ ] A PRD-02 task-packet set exists.
- [ ] Every physics route maps to claim boundaries and validation guidance.
- [ ] Open derivation burdens remain visible.

### Validation

- Shared validation profile.

### Done when

The physics route family is ready for future source-bundled implementation
packets.

## Task MIP-09: Convert PRD-09 Current Research Frontier

### Goal

Create the current-frontier, current-state, stale-data, source-precedence, and
blocked-claim sub implementation plan.

### Context

- PRD requirements: dated snapshots, source precedence, stale warnings,
  blocked claims, validation-status boundaries, refresh requirements.
- Relevant future surfaces: `/ai-research-system/current-state/`,
  `/physics/claim-status/`, `/physics/open-burdens/`.

### Constraints

- Do not refresh source snapshots in this packet.
- Do not hard-code active task, handoff, or current milestone IDs as permanent
  website truth.
- Do not frame validation as scientific proof.

### Implementation notes

- Define snapshot metadata, stale-data behavior, and fail-closed UI states.
- Map current-frontier requirements to future source-refresh approval gates.
- Specify manual review requirements for any current-state public copy.

### Acceptance criteria

- [ ] A PRD-09 sub implementation plan exists.
- [ ] A PRD-09 task-packet set exists.
- [ ] Freshness-sensitive route behavior is testable.
- [ ] Blocked-claim and stale-data behavior are explicit.

### Validation

- Shared validation profile.

### Done when

Future current-state packets can implement dated snapshots without silently
promoting stale or generated state.

## Task MIP-03: Convert PRD-03 Research-Control And Agent Workflow

### Goal

Create the research-control, AgentJob lifecycle, handoff, completion, validator,
parent-child synthesis, and Distance-to-GR workflow sub implementation plan.

### Context

- PRD requirements: Director decision, AgentJob, role execution, parent-child
  synthesis, completion, handoff, validators, operational proof boundary.
- Relevant future surfaces: `/ai-research-system/workflow/`,
  `/ai-research-system/agentjob-lifecycle/`,
  `/ai-research-system/validators-and-handoffs/`,
  `/ai-research-system/project-system-improvement/`.

### Constraints

- Preserve the one-job rule and live-state authority.
- Do not imply workflow validation proves physics claims.
- Do not expose raw YAML as the main reader path.

### Implementation notes

- Map workflow stages to diagrams, timelines, and source-bundle requirements.
- Define operational validation language and proof-boundary copy checks.
- Link current-state content to PRD-09 freshness rules.

### Acceptance criteria

- [ ] A PRD-03 sub implementation plan exists.
- [ ] A PRD-03 task-packet set exists.
- [ ] Agent workflow and validator semantics are mapped conservatively.
- [ ] Future AI workflow pages have validation guidance.

### Validation

- Shared validation profile.

### Done when

The AI workflow route family can be implemented without claiming operational
success is scientific closure.

## Task MIP-04: Convert PRD-04 Role And Schema Components

### Goal

Create the role catalogue, schema map, authority inspector, claim-authority
matrix, and human-gate sub implementation plan.

### Context

- PRD requirements: role and schema authority, human-gated promotion, authority
  classes, role limitations, schema-driven interpretation.
- Relevant future surfaces: `/ai-research-system/roles-and-schemas/`,
  `/ai-research-system/human-gated-promotion/`.

### Constraints

- Do not imply roles prove claims by identity.
- Do not present human gate authority as active without tracked approval.
- Do not mutate role or schema files.

### Implementation notes

- Map role/schema page content to matrices and authority inspectors.
- Define claim-authority display semantics.
- Tie human-gate language back to PRD-10 and PRD-05 boundaries.

### Acceptance criteria

- [ ] A PRD-04 sub implementation plan exists.
- [ ] A PRD-04 task-packet set exists.
- [ ] Role and schema authority boundaries are mapped.
- [ ] Future human-gate pages have conservative acceptance criteria.

### Validation

- Shared validation profile.

### Done when

Future role and schema route packets can explain authority without promoting
claims.

## Task MIP-07: Convert PRD-07 Tooling, Skills, Scripts, And Runtime

### Goal

Create the tooling, skills, scripts, validators, Makefile, runtime,
reproducibility, and local-cache boundary sub implementation plan.

### Context

- PRD requirements: technical tooling, skills, scripts, validators, runtime
  setup, reproducibility, local-cache limits.
- Relevant future surfaces: `/ai-research-system/runtime-requirements/`,
  `/ai-research-system/validators-and-handoffs/`,
  `/ai-research-system/project-system-improvement/`.

### Constraints

- Do not add dependencies or edit runtime scripts in this packet.
- Do not imply runtime setup grants source authority.
- Do not refresh caches.

### Implementation notes

- Map tooling pages to command-scope matrices and failure-mode notes.
- Identify validation commands future route packets should discover or run.
- Preserve cache and local-memory boundaries from PRD-05.

### Acceptance criteria

- [ ] A PRD-07 sub implementation plan exists.
- [ ] A PRD-07 task-packet set exists.
- [ ] Runtime and validator scope are mapped to future routes.
- [ ] No dependency or script mutation is included.

### Validation

- Shared validation profile.

### Done when

Future tooling and runtime pages can explain operations without bypassing
authority boundaries.

## Task MIP-08: Convert PRD-08 Folder And Repository Topology

### Goal

Create the repository topology, folder explorer, source-lane diagram, edit/read
guide, and generated-versus-canonical legend sub implementation plan.

### Context

- PRD requirements: folder families, canonical versus derivative status,
  generated/cache/read-only boundaries, source-lane orientation.
- Relevant future surfaces: `/resources/repository-map/`,
  `/resources/retrieval-layers/`, `/resources/site-builder-guide/`.

### Constraints

- Do not mutate upstream repository files.
- Do not treat topology convenience as source authority.
- Do not publish diagrams or manifests in this packet.

### Implementation notes

- Map folder families to future tables, diagrams, and source-bundle fields.
- Define how page builders should use topology without bypassing source review.
- Coordinate with PRD-11 for the concise site-builder map.

### Acceptance criteria

- [ ] A PRD-08 sub implementation plan exists.
- [ ] A PRD-08 task-packet set exists.
- [ ] Repository topology is mapped to reader-facing route requirements.
- [ ] Generated/cache/source distinctions remain explicit.

### Validation

- Shared validation profile.

### Done when

Future repository-map and site-builder pages can be implemented with clear
authority distinctions.

## Task MIP-11: Convert PRD-11 Quick Source Map For Site Builders

### Goal

Create the concise site-builder guide, source-bundle index, page-to-source map,
build-first checklist, contributor handoff, and staleness-handling sub
implementation plan.

### Context

- PRD requirements: page-to-source mapping table, future builder guide,
  source-bundle schema, build-first checklist, contributor handoff guide.
- Relevant future surfaces: `/resources/site-builder-guide/`,
  `/resources/reading-paths/`, route implementation packet prompts.

### Constraints

- Do not create public source bundles or manifests in this packet.
- Do not authorize implementation work beyond planning.
- Align route names and validation with the canonical greenfield plan.

### Implementation notes

- Map every greenfield route to controlling PRDs and source-bundle needs.
- Define contributor handoff requirements future route packets must satisfy.
- Identify where stale-data and source-refresh approval gates apply.

### Acceptance criteria

- [ ] A PRD-11 sub implementation plan exists.
- [ ] A PRD-11 task-packet set exists.
- [ ] The page-to-source map aligns with the greenfield route inventory.
- [ ] Future route packets have a concise source-bundle-first checklist.

### Validation

- Shared validation profile.

### Done when

The planning system has a complete source-map layer for future website
builders.

## Task MIP-99: Review Complete Sub-Plan Family

### Goal

After all sub-PRD implementation plans exist, review the complete planning set
against the master PRD, greenfield rebuild plan, and implementation-control
rules.

### Context

- Source requirements: all website-information-space PRDs and all generated
  sub implementation plans.
- Relevant outputs:
  - `ImplementationPlans/website-information-space/README.md`
  - all sub implementation plans and task-packet files
  - implementation-control handoff records

### Constraints

- Do not implement public routes.
- Do not consolidate by weakening source-authority boundaries.
- Do not open deployment or push authority.

### Implementation notes

- Confirm every sub-PRD has a plan and task-packet set.
- Check route dependencies against the canonical greenfield plan.
- Identify the first actual route implementation packet to open next.

### Acceptance criteria

- [ ] Every sub-PRD has a corresponding implementation plan.
- [ ] Every sub-PRD has task packets with validation guidance.
- [ ] The complete plan set preserves PRD-10 and PRD-05 constraints.
- [ ] The recommended first route packet is named with rationale.

### Validation

- Shared validation profile.

### Done when

The planning family is ready to transition from PRD conversion into governed
public route implementation.
