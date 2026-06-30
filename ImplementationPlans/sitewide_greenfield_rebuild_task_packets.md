# Codex Task Packets: Sitewide Greenfield Rebuild

Source plan: `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`

Source PRD: `PRDs/sitewide-greenfield-rebuild-prd.md`

Recommended branch: `codex/sitewide-greenfield-rebuild`

Execution rule: do not push and do not deploy. The old implementation is a
reference/source for preservation targets only. Do not use the old route tree,
card-heavy page grammar, or current component composition as the new
implementation architecture.

Shared closeout requirement: each implementation packet must report files
changed, source bundles inspected, validation attempted, browser QA evidence,
review ledger status, blockers, and any skipped checks with concrete reasons.

Shared validation profiles:

- Planning/control packet: `git diff --check`,
  `npm run validate:implementation-control`, and `.venv/bin/python -m pytest`
  when control records or tests are touched.
- Foundation/shared-shell packet: `git diff --check`, `npm run validate`,
  `.venv/bin/python -m pytest`, and desktop/mobile browser QA.
- Page packet: `git diff --check`, `npm run validate:content`,
  `npm run validate:links`, `npm run validate:layout`,
  `npm run validate:comprehension`, `npm run validate:provenance`,
  `npm run build`, and desktop/mobile browser QA for changed routes.
- SVG or diagram packet: page packet checks plus `npm run validate:svg` and
  `npm run validate:manifests`.
- Release packet: `npm run validate`, `npm run quality`, route smoke tests,
  and owner review ledger inspection.

## Task GF-000: Open Fresh Greenfield Control Packet

### Goal

Create or select fresh implementation-control records that authorize the first
bounded greenfield rebuild implementation packet.

### Context

- PRD requirements: REQ-001, REQ-003, REQ-014, NFR-004.
- Relevant files or directories:
  - `implementation_control/program_state.yaml`
  - `implementation_control/tasks/`
  - `implementation_control/handoffs/`
  - `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
  - `PRDs/sitewide-greenfield-rebuild-prd.md`
- Existing patterns to follow: `npm run continue:implementation -- --summary`
  resolves live state; implementation-control records are live authority for
  website-local packets.

### Constraints

- Do not implement public routes in this task.
- Do not delete or retire old route files.
- Do not push, deploy, refresh upstream sources, or mutate the upstream
  research repository.
- Treat this plan and the PRD as context until live control records authorize
  writes.

### Implementation notes

- Run the implementation-control resolver and inspect the active task/job.
- If needed, prepare the next control packet with a narrow write allowlist for
  GF-001 only.
- Record that the old implementation is preservation evidence only.

### Acceptance criteria

- [ ] A live control record authorizes the next bounded implementation packet.
- [ ] The authorized write scope is limited to GF-001 files.
- [ ] Deployment and upstream writes remain unauthorized.
- [ ] The closeout names validators and any blockers.

### Validation

- `npm run continue:implementation -- --summary`
- `git diff --check`
- `npm run validate:implementation-control`
- `.venv/bin/python -m pytest`

### Done when

The next coding packet can proceed under fresh live control records with a
clear write scope and no route implementation has occurred in this task.

## Task GF-001: Create Greenfield Shell Contract And Review Ledger

### Goal

Create the new rebuild foundation: navigation model, page/content metadata
contract, shell direction, preserved footer requirements, card-use rules,
review ledger, and validation expectations.

### Context

- PRD requirements: REQ-001, REQ-003, REQ-005, REQ-006, REQ-007, REQ-008,
  REQ-013, REQ-014, NFR-002, NFR-003.
- Relevant files or directories:
  - `src/layouts/BaseLayout.astro`
  - `src/pages/index.astro`
  - `src/lib/siteContent.ts`
  - `src/styles/global.css`
  - `docs/quality/public-comprehension-review-standard.md`
  - `docs/quality/`
  - `docs/architecture/`
- Existing patterns to inspect as reference only: footer content, dropdown
  behavior, hero/action/SVG language, source-authority boundary copy.

### Constraints

- Do not build the full route inventory in this task.
- Do not preserve the old route tree as the new architecture.
- Do not introduce dependencies.
- Library/resource pages under `/resources/` must not use a dedicated
  `Source authority` section.

### Implementation notes

- Add a concise architecture note or implementation contract for greenfield
  page packets.
- Add `docs/quality/sitewide-greenfield-review-ledger.md` with every planned
  route and initial status `human review pending` or `not implemented`.
- Define source-bundle fields required before writing claim-bearing copy.
- Define when cards are allowed and when narrative bands, evidence rails,
  dossiers, diagrams, tables, timelines, or glossaries are preferred.
- If code is included, create a new greenfield namespace rather than adapting
  old pages in place.

### Acceptance criteria

- [ ] The foundation contract states that old implementation is reference only.
- [ ] The route inventory and review statuses are recorded.
- [ ] The preserved footer, hero, SVG, and diagram rules are explicit.
- [ ] The content contract requires page family, source anchors, claim status,
  navigation role, validation gates, and intro paragraph.
- [ ] The validation profile for future packets is documented.

### Validation

- `git diff --check`
- `npm run validate:implementation-control` if control records changed
- `npm run validate` if runtime code, styles, routes, or manifests changed
- Documentation-only changes may stop after `git diff --check` and review.

### Done when

Future route packets can cite a checked-in foundation contract and review
ledger before building pages.

## Task GF-002: Build Home And Primary Navigation Slice

### Goal

Implement the new Home page and primary navigation slice at `/` with the new
top-level categories: Home, Physics Research, AI Research System, Resources.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-004, REQ-005, REQ-006, REQ-007,
  REQ-013, NFR-001, NFR-002.
- Relevant files or directories:
  - `src/pages/index.astro`
  - `src/layouts/`
  - `src/lib/`
  - `src/styles/global.css`
  - `public/files/manifests/`
  - `docs/quality/sitewide-greenfield-review-ledger.md`
- Source requirements: PRD-01, PRD-10, AGENTS source-authority boundary,
  existing footer evidence.

### Constraints

- Do not link primary navigation to old `/project/...` route families.
- Do not overclaim completed derivation or autonomous AI proof.
- Preserve footer content and behavior.
- Preserve animated SVG direction with textless accessible SVG.

### Implementation notes

- Build a new first-viewport sequence: hero/title/action/SVG, then substantial
  general-public introduction.
- Route category actions to the new category URLs.
- Update manifests/provenance only for changed public routes.
- Record Home as technically ready or human review pending in the ledger.

### Acceptance criteria

- [ ] `/` uses the new greenfield navigation model.
- [ ] The Home intro explains the project, why it matters, and how it connects
  physics, AI workflow, source authority, and resources.
- [ ] Footer content and badges remain available.
- [ ] The first viewport has no text overlap on desktop or mobile.
- [ ] Source/provenance links do not replace internal-first navigation.

### Validation

- Foundation/shared-shell validation profile.
- Desktop/mobile browser QA for `/`.

### Done when

The new Home page and navigation shell are technically valid and recorded as
ready for owner review.

## Task GF-003: Build Physics Overview And Ontology Slice

### Goal

Implement `/physics/` and `/physics/ontology/` as the first Physics Research
vertical slice.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-005, REQ-009, REQ-013, NFR-001,
  NFR-002.
- Relevant files or directories:
  - `src/pages/physics/`
  - `src/lib/`
  - `docs/content-dossiers/physics-track/`
  - `docs/content-dossiers/physics-ontology/`
  - `public/files/manifests/`
- Source requirements: PRD-02, PRD-10, ontology source anchors, registered TeX
  derivative boundary.

### Constraints

- Do not claim source-side GR derivation is complete.
- Do not present ontology vocabulary as equation-level proof.
- Do not use old `/project/physics/` page structure as the new structure.

### Implementation notes

- Create or inspect source bundles for both pages.
- Use narrative progression from general-public orientation to ontology terms,
  benchmark boundary, source authority, and related routes.
- Use glossary/matrix forms where clearer than cards.
- Update review ledger and manifests for the new routes.

### Acceptance criteria

- [ ] `/physics/` explains the category and routes readers to the six physics
  child pages.
- [ ] `/physics/ontology/` defines ontology terms near first use.
- [ ] Both pages have substantial intro paragraphs after the hero.
- [ ] Claim status and source basis are visible.
- [ ] Internal routes are primary; source links are provenance.

### Validation

- Page packet validation profile.
- Add `npm run validate:svg` if SVGs are added or modified.
- Desktop/mobile browser QA for `/physics/` and `/physics/ontology/`.

### Done when

Both pages are technically valid, source-bundled, provenance-covered, and
marked human review pending.

## Task GF-004: Build Physics Benchmark, Roadmap, And Flow Geometry Slice

### Goal

Implement `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, and
`/physics/flow-geometry/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-009, REQ-013, NFR-001, NFR-002.
- Relevant files or directories:
  - `src/pages/physics/exact-gr-benchmark/`
  - `src/pages/physics/derivation-roadmap/`
  - `src/pages/physics/flow-geometry/`
  - `docs/content-dossiers/physics-exact-gr-benchmark/`
  - `docs/content-dossiers/physics-gr-derivation-roadmap/`
  - `public/files/manifests/`
- Source requirements: PRD-02, PRD-09, exact-closure TeX, derivation burden
  map, flow-geometry source anchors.

### Constraints

- Separate exact-GR benchmark adoption from first-principles derivation.
- Do not claim matter coupling, Einstein equations, or benchmark promotion are
  derived from source-side substrate structure.
- Do not display equations without symbol/context explanation.

### Implementation notes

- Use an adoption-versus-derivation matrix for benchmark content.
- Use a burden-roadmap timeline or evidence rail for derivation roadmap.
- Use a visual dictionary/glossary for flow geometry.
- Source current-state statements only through authorized freshness-sensitive
  sources.

### Acceptance criteria

- [ ] Benchmark page states effective-level benchmark status without promotion.
- [ ] Roadmap page names open burdens rather than solving them.
- [ ] Flow geometry page defines its terms, assumptions, and limits.
- [ ] Each page has source basis, claim status, and related internal routes.
- [ ] No page defaults to a card grid.

### Validation

- Page packet validation profile.
- Add `npm run validate:svg` for visual changes.
- Desktop/mobile browser QA for the three routes.

### Done when

The three route pages are technically valid, source-bundled, and marked human
review pending.

## Task GF-005: Build Physics Claim Status And Open Burdens Slice

### Goal

Implement `/physics/claim-status/` and `/physics/open-burdens/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-009, REQ-013, NFR-001, NFR-002.
- Relevant files or directories:
  - `src/pages/physics/claim-status/`
  - `src/pages/physics/open-burdens/`
  - `src/data/`
  - `public/files/manifests/`
- Source requirements: PRD-02, PRD-09, claim-boundary registry,
  Distance-to-GR ledger, blocked-claim language.

### Constraints

- Current-state or ledger-derived content must include dated snapshot behavior.
- Do not hard-code active task or handoff IDs as permanent website truth.
- Validation PASS must be framed as operational consistency, not proof.

### Implementation notes

- Use status dossiers and tables for dense claim and burden metadata.
- Put blocked claims beside any progress or status language.
- Fail closed with a stale-data warning if source freshness cannot be verified.

### Acceptance criteria

- [ ] Claim status page shows what is claimed, not claimed, blocked, or open.
- [ ] Open burdens page explains missing derivation steps without progress-bar
  proof.
- [ ] Freshness/source-basis metadata is visible.
- [ ] Pages remain stable if current-state data cannot be refreshed.

### Validation

- Page packet validation profile.
- Run snapshot-specific tests if snapshot data is changed.
- Desktop/mobile browser QA for both routes.

### Done when

The pages are technically valid, conservative, and marked human review
pending.

## Task GF-006: Build AI Overview And Current State Slice

### Goal

Implement `/ai-research-system/` and `/ai-research-system/current-state/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-010, REQ-013, NFR-001, NFR-002.
- Relevant files or directories:
  - `src/pages/ai-research-system/`
  - `src/data/`
  - `implementation_control/program_state.yaml`
  - `public/files/manifests/`
- Source requirements: PRD-03, PRD-09, PRD-10, implementation-control current
  state, research-control current-state source precedence.

### Constraints

- Do not present AI agents as autonomous proof systems.
- Do not convert current implementation-control state into permanent website
  truth without dated snapshot behavior.
- Do not expose raw control metadata as the main reader experience.

### Implementation notes

- Explain the AI research system as governed, bounded, source-first workflow.
- Use a current-state dossier with snapshot date, source basis, stale behavior,
  and blocked overread warnings.
- Keep the category overview stable even when current-state snapshot data
  changes.

### Acceptance criteria

- [ ] AI overview page explains the category before internal terms dominate.
- [ ] Current-state page labels all live data as dated snapshot context.
- [ ] Validation and workflow status are not framed as proof.
- [ ] Pages route to workflow, AgentJob, roles, validators, memory, runtime,
  and improvement pages.

### Validation

- Page packet validation profile.
- Add snapshot tests if data contracts change.
- Desktop/mobile browser QA for both routes.

### Done when

Both pages are technically valid, source-bundled, and marked human review
pending.

## Task GF-007: Build AI Workflow And AgentJob Lifecycle Slice

### Goal

Implement `/ai-research-system/workflow/` and
`/ai-research-system/agentjob-lifecycle/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-010, REQ-013, NFR-001, NFR-002.
- Relevant files or directories:
  - `src/pages/ai-research-system/workflow/`
  - `src/pages/ai-research-system/agentjob-lifecycle/`
  - `docs/content-dossiers/ai-workflow/`
  - `docs/content-dossiers/ai-one-bounded-agentjob/`
- Source requirements: PRD-03, Director decisions, AgentJob schema,
  execution-role records, completions, handoffs.

### Constraints

- Preserve the one-job rule.
- Do not imply parent-child synthesis expands authority.
- Do not make raw YAML inspection the primary reader path.

### Implementation notes

- Use lifecycle timelines and artifact tables.
- Explain what each control record does and does not authorize.
- Include validator PASS limits near validation language.

### Acceptance criteria

- [ ] Workflow page explains the route from tracked state to handoff.
- [ ] AgentJob page explains one bounded executable contract.
- [ ] Both pages make authority and proof limits visible.
- [ ] Related routes stay internal-first.

### Validation

- Page packet validation profile.
- Desktop/mobile browser QA for both routes.

### Done when

The workflow and lifecycle pages are technically valid and marked human review
pending.

## Task GF-008: Build AI Roles, Human Gates, Validators, And Handoffs Slice

### Goal

Implement `/ai-research-system/roles-and-schemas/`,
`/ai-research-system/human-gated-promotion/`, and
`/ai-research-system/validators-and-handoffs/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-010, REQ-013, NFR-001, NFR-002.
- Relevant files or directories:
  - `src/pages/ai-research-system/roles-and-schemas/`
  - `src/pages/ai-research-system/human-gated-promotion/`
  - `src/pages/ai-research-system/validators-and-handoffs/`
  - `docs/content-dossiers/ai-roles-and-skills/`
  - `docs/content-dossiers/operations-validator-operator-workflow/`
- Source requirements: PRD-03, PRD-04, PRD-07, role registry, schema files,
  claim-boundary registry, handoff sources.

### Constraints

- Do not imply roles prove claims by identity.
- Do not present Gate Chair authority as active without tracked approval.
- Do not treat validators, registries, handoffs, or commits as proof.

### Implementation notes

- Use a claim-authority matrix for roles and schemas.
- Use human-gate explanation before promotion language.
- Use a validator/handoff table that names checked scope and non-scope.

### Acceptance criteria

- [ ] Role/schema page resolves active authority conservatively.
- [ ] Human-gated promotion page separates protected promotion from automated
  outcomes.
- [ ] Validators/handoffs page states operational validation limits.
- [ ] Each page has claim boundary and source basis near authority language.

### Validation

- Page packet validation profile.
- Desktop/mobile browser QA for all three routes.

### Done when

The three pages are technically valid, conservative, and marked human review
pending.

## Task GF-009: Build AI Memory, Improvement, And Runtime Slice

### Goal

Implement `/ai-research-system/memory-preflight/`,
`/ai-research-system/project-system-improvement/`, and
`/ai-research-system/runtime-requirements/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-010, REQ-013, NFR-001, NFR-002,
  NFR-003.
- Relevant files or directories:
  - `src/pages/ai-research-system/memory-preflight/`
  - `src/pages/ai-research-system/project-system-improvement/`
  - `src/pages/ai-research-system/runtime-requirements/`
  - `Makefile`
  - `package.json`
  - `scripts/`
  - `tests/`
- Source requirements: PRD-03, PRD-05, PRD-07, memory/retrieval boundary,
  project-system improvement sources, runtime evidence.

### Constraints

- Do not present memory lookup as authority.
- Do not imply runtime setup grants write permission or claim authority.
- Do not add dependencies.

### Implementation notes

- Use command-scope matrices for runtime and validators.
- Use retrieval-layer diagrams or tables for memory preflight.
- Explain project-system improvement as bounded maintenance, not source-claim
  mutation.

### Acceptance criteria

- [ ] Memory page explains navigation versus authority.
- [ ] Improvement page explains bounded repair loops and review evidence.
- [ ] Runtime page lists setup and validator scope without bypass language.
- [ ] All pages preserve source-authority and operational limits.

### Validation

- Page packet validation profile.
- Add `npm run validate:svg` if diagrams are added or modified.
- Desktop/mobile browser QA for all three routes.

### Done when

The three pages are technically valid, source-bundled, and marked human review
pending.

## Task GF-010: Build Resources Overview, Source Authority, And Registries Slice

### Goal

Implement `/resources/`, `/resources/source-authority/`, and
`/resources/registries/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-011, REQ-013, NFR-001, NFR-002.
- Relevant files or directories:
  - `src/pages/resources/index.astro`
  - `src/pages/resources/source-authority/`
  - `src/pages/resources/registries/`
  - `public/files/manifests/`
- Source requirements: PRD-05, PRD-06, PRD-10, registry sources, AGENTS
  `/resources/` source-authority-section constraint.

### Constraints

- Do not render a dedicated `Source authority` section on library/resource
  pages under `/resources/`.
- Do not make registry dashboards proof surfaces.
- Do not make GitHub/source links the primary route path.

### Implementation notes

- Use contextual copy and footer/provenance routes for authority boundaries.
- Use matrices or tables for source/registry classification.
- Keep Resources as a category landing page, not a loose link index.

### Acceptance criteria

- [ ] Resources overview orients readers to all Resources child pages.
- [ ] Source Authority page explains authority classes without violating the
  `/resources/` section rule.
- [ ] Registries page explains provenance/status use and proof limits.
- [ ] Internal links point to new short routes.

### Validation

- Page packet validation profile.
- Desktop/mobile browser QA for all three routes.

### Done when

The three resources pages are technically valid and marked human review
pending.

## Task GF-011: Build Resources Derivatives, Retrieval, Publication, And Library Slice

### Goal

Implement `/resources/generated-derivatives/`,
`/resources/retrieval-layers/`, `/resources/publication-process/`, and
`/resources/library/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-011, REQ-013, NFR-001, NFR-002.
- Relevant files or directories:
  - `src/pages/resources/generated-derivatives/`
  - `src/pages/resources/retrieval-layers/`
  - `src/pages/resources/publication-process/`
  - `src/pages/resources/library/`
  - `public/files/manifests/`
- Source requirements: PRD-05, PRD-06, PRD-08, derivative registries,
  publication briefs, source specs, local retrieval boundary.

### Constraints

- Do not treat generated HTML, PDFs, GitHub-facing Markdown, wiki, Obsidian,
  semantic extracts, or `.local` caches as canonical authority.
- Do not expose process metadata before reader topic comprehension.
- Do not add source authority sections prohibited under `/resources/`.

### Implementation notes

- Use source-versus-derivative-versus-retrieval matrices.
- Use publication-chain timelines.
- Use the library page as a reading surface, not repository archaeology.

### Acceptance criteria

- [ ] Generated derivatives page labels derivative status visibly.
- [ ] Retrieval layers page labels navigation-only behavior.
- [ ] Publication page distinguishes publication quality from source
  authority.
- [ ] Library page supports reader paths with provenance and internal routes.

### Validation

- Page packet validation profile.
- Desktop/mobile browser QA for all four routes.

### Done when

The four pages are technically valid, source-bundled, and marked human review
pending.

## Task GF-012: Build Reading Paths, Repository Map, Site Builder Guide, And Diagram Gallery

### Goal

Implement `/resources/reading-paths/`, `/resources/repository-map/`,
`/resources/site-builder-guide/`, and `/resources/diagrams/`.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-011, REQ-012, REQ-013, NFR-001,
  NFR-002.
- Relevant files or directories:
  - `src/pages/resources/reading-paths/`
  - `src/pages/resources/repository-map/`
  - `src/pages/resources/site-builder-guide/`
  - `src/pages/resources/diagrams/`
  - `src/components/DiagramGalleryList.astro`
  - `scripts/render_mermaid_diagrams.py`
  - `public/assets/diagrams/`
  - `public/files/manifests/asset_manifest.json`
- Source requirements: PRD-06, PRD-08, PRD-11, greenfield Diagram Gallery
  rule.

### Constraints

- Preserve Diagram Gallery format and static generated diagram discipline.
- Remove the current diagram inventory unless individual diagrams are
  explicitly reapproved.
- Do not regenerate or publish new diagrams unless this packet authorizes that
  work.
- Do not make topology or source-map convenience a substitute for source
  inspection.

### Implementation notes

- Reading paths should guide general and specialist readers through new
  internal routes.
- Repository map should classify folders by authority, derivative, retrieval,
  tooling, or cache status.
- Site-builder guide should expose the source-bundle schema.
- Diagram Gallery may launch with no approved diagrams, a future-ready empty
  state, or a small reapproved set if owner approval exists.

### Acceptance criteria

- [ ] Reading paths point to new short routes.
- [ ] Repository map explains edit/read boundaries.
- [ ] Site-builder guide explains source-bundle-first implementation.
- [ ] Diagram Gallery keeps format/provenance/non-authority behavior and
  removes old inventory unless reapproved.
- [ ] Empty or future-state diagram behavior is understandable and accessible.

### Validation

- SVG or diagram packet validation profile.
- Desktop/mobile browser QA for all four routes.

### Done when

The four resources pages are technically valid, diagram inventory status is
explicit, and pages are marked human review pending.

## Task GF-013: Regenerate Manifests, Redirects, And Retire Obsolete Old Routes

### Goal

After replacement routes validate, update public manifests, redirect mappings,
internal links, and remove or retire obsolete old route files.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-003, REQ-013, NFR-001, NFR-004.
- Relevant files or directories:
  - `src/pages/project/`
  - `src/pages/resources/`
  - `public/_redirects`
  - `public/files/manifests/page_route_map.json`
  - `public/files/manifests/page_provenance.json`
  - `public/files/manifests/asset_manifest.json`
  - `scripts/generate_page_provenance.py`
  - `scripts/run_curator.py`

### Constraints

- Do not retire old routes before all replacement routes exist and pass
  targeted validation.
- Do not delete preserved footer, hero direction, SVG language, or diagram
  workflow.
- Do not deploy.
- Use redirects only after internal links point to new routes.

### Implementation notes

- Build an old-to-new route mapping.
- Update all internal navigation and route cards to new routes.
- Add redirects for strong route equivalents; use category fallbacks only when
  justified.
- Regenerate page provenance and relevant manifests.
- Remove obsolete route files only under this packet's allowlist.

### Acceptance criteria

- [ ] No primary navigation or route card points to the old route scheme.
- [ ] Public manifests match the new route inventory.
- [ ] Old routes are redirected or intentionally removed with documented
  rationale.
- [ ] Build and validators pass, or unrelated baseline drift is named.
- [ ] Rollback path is clear.

### Validation

- Release packet validation profile except `npm run quality` may be reserved
  for GF-014 if owner review is still pending.
- Run redirect smoke checks against local preview.

### Done when

The old presentation architecture is retired safely and the new route model is
the internal-first public journey.

## Task GF-014: Run Owner Review Loop And Release-Candidate QA

### Goal

Complete owner review, feedback packets, final validation, and deploy
readiness reporting without deploying.

### Context

- PRD requirements: REQ-014, NFR-001, NFR-002, NFR-004.
- Relevant files or directories:
  - `docs/quality/sitewide-greenfield-review-ledger.md`
  - `docs/quality/`
  - `public/files/manifests/`
  - changed route files
  - `curator/reports/`
- Existing pattern: public-comprehension review records `pending maintainer
  review`, `reviewed with changes requested`, or `reviewed and accepted`.

### Constraints

- Do not mark deployment ready until owner review status is `reviewed and
  accepted`.
- Do not deploy in this packet unless a later explicit user request invokes
  the deploy workflow.
- Feedback changes must be implemented in bounded packets with validation
  rerun.

### Implementation notes

- Present route set to owner for review.
- For requested changes, open a follow-up feedback packet, implement changes,
  rerun relevant validators, and update ledger.
- Run final validation and quality checks after acceptance.
- Produce a release-candidate QA note that names any residual risk.

### Acceptance criteria

- [ ] Every rebuilt route has a ledger status.
- [ ] Requested changes are either implemented and revalidated or explicitly
  deferred by owner decision.
- [ ] Final validators and browser QA are recorded.
- [ ] Deployment is still separate and explicitly not performed.

### Validation

- `npm run validate`
- `npm run quality`
- `.venv/bin/python -m pytest`
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`
  against local preview
- Desktop/mobile browser QA for representative Home, Physics, AI, Resources,
  and Diagram Gallery routes.

### Done when

The greenfield rebuild is accepted or has a clear remaining feedback queue,
and a release-candidate report states whether deployment is authorized.
