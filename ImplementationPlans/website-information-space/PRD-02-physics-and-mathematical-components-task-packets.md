# Codex Task Packets: PRD-02 Physics and Mathematical Components

Source plan:
`ImplementationPlans/website-information-space/PRD-02-physics-and-mathematical-components-implementation-plan.md`

Source PRD:
`PRDs/website-information-space/PRD-02-physics-and-mathematical-components.md`

Execution rule: these are future implementation packets. Do not implement them
inside the planning conversion packet that creates this file.

Shared constraints:

- Treat the sitewide greenfield rebuild plan as canonical.
- Preserve the Source Authority Boundary.
- Use `Æther` in reader-facing text and `aether` only for links, slugs, file
  naming, package names, repository paths, and machine-facing identifiers.
- Keep internal routes primary and source links available as provenance.
- Do not push, deploy, mutate upstream sources, or refresh generated materials
  without fresh authorization.

## Task PRD-02-TASK-01: Prepare Source Bundle And Page Contract

### Goal

Prepare source-bundle and page-contract guidance for physics, mathematics, exact-gr benchmark, and open burdens.

### Context

- PRD requirements: `PRD-02` traceability rows in the source implementation plan.
- Relevant future routes: `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`.
- Existing patterns: canonical greenfield route model, substantial intro paragraph
  rule, source-bundle-first public copy, and owner review.

### Constraints

- Do not write public route copy until source basis is inspected.
- Do not treat generated derivatives, memory, validators, or registries as
  scientific proof.
- Do not change public manifests or assets in this task unless separately
  authorized.

### Implementation notes

- Identify primary authority sources, supporting sources, derivative seed
  material, freshness policy, forbidden inferences, and validation gates.
- Record the source bundle in the future route packet or approved source-bundle
  location.
- Confirm whether current-state or source-refresh approval is required.

### Acceptance criteria

- [ ] Every future route has named source-bundle requirements.
- [ ] Claim boundaries and forbidden inferences are explicit.
- [ ] Validation and owner-review expectations are named.

### Validation

- `git diff --check`
- `npm run validate:implementation-control`
- Add source-specific validators only when source bundles or public routes are
  actually changed.

### Done when

Future route implementation can proceed without guessing source authority or
claim boundaries.

## Task PRD-02-TASK-02: Implement Greenfield Route Slice

### Goal

Implement the affected greenfield route surface for physics, mathematics, exact-gr benchmark, and open burdens.

### Context

- PRD requirements: `PRD-02` functional requirements.
- Relevant future routes: `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`.
- Existing patterns: greenfield page grammar, hero/title/action/SVG opening,
  substantial general-public introduction, and internal-first navigation.

### Constraints

- Do not revive the old card-grid page grammar as the default structure.
- Do not strengthen public scientific, mathematical, governance, or workflow
  claims beyond source authority.
- Do not retire old routes in the same packet unless the live control record
  explicitly authorizes route retirement.

### Implementation notes

- Build one vertical route slice at a time.
- Prefer narrative bands, evidence rails, dossiers, matrices, tables, timelines,
  glossaries, and diagrams when they fit the information type.
- Use ordinary cards only for true peer choices, catalogues, inventories, or
  galleries.

### Acceptance criteria

- [ ] The route slice satisfies the mapped `PRD-02` requirements.
- [ ] The first viewport and intro paragraph are understandable without source
  archaeology.
- [ ] Claim status, source basis, and related internal routes are visible.
- [ ] Desktop and mobile layouts have no incoherent overlap.

### Validation

- `git diff --check`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:provenance`
- `npm run validate:comprehension`
- `npm run build`
- Desktop and mobile browser QA for changed routes

### Done when

The route slice is technically valid, source-bundled, and marked for owner review.

## Task PRD-02-TASK-03: Validate, Review, And Prepare Handoff

### Goal

Close the implementation work for physics, mathematics, exact-gr benchmark, and open burdens with validation evidence, owner-review status, and a clear next packet.

### Context

- PRD requirements: `PRD-02` acceptance criteria and validation plan.
- Relevant future routes: `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/`.
- Existing patterns: implementation-control completion record and handoff closeout.

### Constraints

- Do not mark owner acceptance unless the owner has reviewed and accepted the route set.
- Do not deploy or push from this task.
- Do not hide skipped validators. Name skipped checks with concrete reasons.

### Implementation notes

- Run the validators required by the active packet.
- Run route-specific validators and browser QA when public routes changed.
- Update review ledger or handoff evidence as authorized by the live packet.
- Name residual risk and the logical next packet.

### Acceptance criteria

- [ ] Validation results are recorded.
- [ ] Browser QA evidence is recorded when routes changed.
- [ ] Owner-review status is recorded where relevant.
- [ ] The next implementation-control packet is explicit.

### Validation

- Use the active packet validators.
- For public route work, also use the future route validation profile from this task-packet file.

### Done when

The packet can be checkpointed locally without push, deploy, or source-refresh side effects.
