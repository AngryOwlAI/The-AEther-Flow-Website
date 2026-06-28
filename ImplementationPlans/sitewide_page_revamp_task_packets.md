# Codex Task Packets: Sitewide Page Revamp

Source plan: `ImplementationPlans/sitewide_page_revamp_implementation_plan.md`

Branch scope: `codex/revamp-all-pages`

Execution rule: do not push and do not deploy. Each implementation task should
return files changed, validation attempted, browser QA evidence, source checks,
blockers, and no-ai-slop status.

Shared source rule: for every claim-bearing page, verify or create the required
`docs/system-analyses/*.md` file before invoking `to-web-page`. If source
authority is unclear, stop with `block` instead of creating public copy.

Shared page rule: use the repo-local `to-web-page` workflow for one analysis
file and one public page per task. Existing-route rewrites are authorized by
the implementation plan, but existing prose remains suspect until it passes
evidence review and the no-ai-slop gate.

Shared validation profiles:

- Page minimum: `npm run validate:comprehension`,
  `npm run validate:manifests`, `npm run validate:content`,
  `npm run validate:provenance`, `npm run build`, plus desktop/mobile browser
  QA.
- SVG affected: add `npm run validate:svg`.
- Navigation affected: add `npm run validate:links`.
- Shared-component or foundation affected: run `npm run validate`.
- Release candidate: run `npm run validate` and `npm run quality`.

## Task FND-001: Define The Revamp Foundation Contract

### Goal

Create the shared implementation contract that future page packets must follow:
page layers, source-analysis rule, anti-slop gate, route families, navigation
model, SVG preservation, validation tiers, and route retirement rules.

### Context

- PRD requirements: REQ-001 through REQ-013.
- Relevant files or directories:
  - `ImplementationPlans/sitewide_page_revamp_implementation_plan.md`
  - `AGENTS.md`
  - `docs/architecture/website-feature-and-functionality.md`
  - `src/lib/siteContent.ts`
  - `src/components/InternalExplainerPage.astro`
  - `docs/content-dossiers/_template.md`
- Existing patterns to follow: internal-first routes, content dossiers,
  manifest/provenance registration, source-authority notices.

### Constraints

- Do not implement individual topic pages in this packet.
- Do not add dependencies.
- Do not deploy.
- Preserve exact hard-boundary phrases where they are source-true:
  `proposal-only`, `draft/control`, `source-extension`, `fail-closed`,
  `frozen negative`, `no MetricData(E)`, `no g_eff`,
  `no downstream GR promotion`.

### Implementation Notes

- Write a concise foundation note under `docs/architecture/` or extend the
  existing architecture document with a clearly labeled revamp contract section.
- Define the layered page model: public, mechanism, evidence, specialist, and
  navigation.
- Define when `technical validation passed`, `human review pending`, `repair`,
  and `block` apply.
- Define the browser QA artifact convention for future page packets.

### Acceptance Criteria

- [ ] The foundation contract names route families and page layers.
- [ ] The contract requires source analysis before public page conversion.
- [ ] The contract defines anti-slop pass/repair/block handling.
- [ ] The contract preserves SVG animation and textless SVG policy.
- [ ] The contract records the no-deploy boundary.

### Validation

- `git diff --check`
- `npm run validate` if shared code, styles, or route metadata changed.
- Documentation-only changes may use `git diff --check` and a plan review
  note if no runtime file changed.

### Done When

The foundation contract is checked in locally, future packets can cite it, and
the diff is reviewable without requiring page implementation.

## Task FND-002: Redesign Site Shell And Route Landings

### Goal

Revamp the homepage, project overview, route-family landings, and resource
landing so the site has a coherent public-first learning path before topic
pages are rewritten.

### Context

- PRD requirements: REQ-002, REQ-006, REQ-008, REQ-010, REQ-012.
- Relevant routes:
  - `/`
  - `/project/overview/`
  - `/project/physics/`
  - `/project/ai-research-agent-system/`
  - `/project/operations/`
  - `/project/source-authority/`
  - `/resources/`
- Relevant files:
  - `src/pages/index.astro`
  - `src/pages/project/overview.astro`
  - `src/pages/project/physics/index.astro`
  - `src/pages/project/ai-research-agent-system/index.astro`
  - `src/pages/project/operations/index.astro`
  - `src/pages/project/source-authority/index.astro`
  - `src/pages/resources/index.astro`
  - `src/lib/siteContent.ts`
  - `src/styles/global.css`

### Constraints

- Do not create unsupported scientific claims.
- Keep source links as provenance, not primary navigation.
- Preserve animated SVGs where they still improve comprehension.
- Shared component edits require full-site validation.

### Implementation Notes

- Reframe the first screen for the general public.
- Add clear track cards and guided-start entry points.
- Make current state, Distance-to-GR, source authority, and documents easy to
  find.
- Remove generic marketing language and replace it with concrete reader jobs.

### Acceptance Criteria

- [ ] A general-public reader can identify what the project is and where to
  start.
- [ ] Specialist paths are visible without overwhelming the first screen.
- [ ] Source-authority boundary is visible early.
- [ ] Internal routes are favored over GitHub/source links.
- [ ] Existing animated SVGs remain visible or are intentionally retired with a
  reason.

### Validation

- `npm run validate`
- Desktop and mobile browser QA for `/`, `/project/overview/`, and each track
  landing.

### Done When

The site shell and landings provide a stable navigation foundation for page
packets and pass full validation or have concrete, documented blockers.

## Task PG-001: Rewrite Current Research State And Next Gate

### Goal

Refresh and rewrite `/project/physics/current-state/` as the first authority
and orientation page.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-006, REQ-007, REQ-012.
- Inventory item: INV-001.
- Required analysis:
  `docs/system-analyses/current-research-state-and-next-gate.md`.
- Relevant files:
  - `src/pages/project/physics/current-state/index.astro`
  - `src/data/physics_current_state_snapshot.json`
  - `scripts/refresh_physics_current_state_snapshot.py`
  - `docs/content-dossiers/physics-current-state/dossier.md`
  - `public/files/manifests/page_route_map.json`
  - `public/files/manifests/page_provenance.json`

### Constraints

- Require clean, committed upstream source state before refresh.
- Do not promote current state into completed derivation or Gate Chair verdict.
- Preserve exact blocked-claim language from upstream.

### Implementation Notes

- Inspect upstream `program_state.yaml`, latest handoff, relevant ledgers, and
  claim-boundary registry.
- Refresh the checked-in snapshot only if upstream is clean and source state is
  clear.
- Use `to-web-page` after the system analysis exists and passes no-ai-slop.
- Put plain-language status first and technical/provenance detail later.

### Acceptance Criteria

- [ ] Page states what is current, what is next, and what is not claimed.
- [ ] Snapshot/provenance reflects clean pinned upstream evidence.
- [ ] Dossier records source analysis and claim boundaries.
- [ ] Browser QA confirms desktop and mobile readability.

### Validation

- Page minimum validation profile.
- Add `npm run validate:links` if navigation changes.
- Desktop/mobile browser QA for `/project/physics/current-state/`.

### Done When

The route is refreshed, source-pinned, no-ai-slop passes, and the current-state
page can serve as the authority reference for later physics pages.

## Task PG-002: Create Distance To GR Dashboard

### Goal

Create `/project/physics/distance-to-gr/` as a ledger-backed dashboard that
explains derivation burden without implying progress-bar proof.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-006, REQ-007, REQ-012.
- Inventory item: INV-002.
- Required analysis: `docs/system-analyses/distance-to-gr-dashboard.md`.
- Relevant sources: `registries/DISTANCE_TO_GR_LEDGER.csv`,
  `research_control/design/gr_derivation_burden_map.md`,
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`.

### Constraints

- Do not imply real-time synchronization unless a checked-in snapshot exists.
- Do not present the ledger as proof.
- Do not claim `g_eff`, matter coupling, Einstein equations, benchmark
  promotion, or completed derivation unless upstream evidence explicitly
  permits it.

### Implementation Notes

- Prefer a checked-in derived JSON snapshot if the implementation needs
  structured rendering.
- Use status badges or burden cards instead of a misleading percentage bar.
- Link internally to current state, exact-GR benchmark, claim gates, and source
  authority.

### Acceptance Criteria

- [ ] Route explains each burden step in public language.
- [ ] Specialist section identifies source objects and blocked downstream
  promotions.
- [ ] Source manifest/provenance covers the ledger or derived snapshot.
- [ ] No local filesystem paths appear in public output.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Desktop/mobile browser QA for `/project/physics/distance-to-gr/`.

### Done When

The page gives a source-backed, non-overclaiming map of the Distance-to-GR
burden and passes validation.

## Task PG-003: Create Source Extension Pipeline Page

### Goal

Create `/project/physics/source-extension-pipeline/` explaining proposal,
audit, stress, selector, and Gate Chair preconditions.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-006, REQ-007.
- Inventory item: INV-003.
- Required analysis: `docs/system-analyses/source-extension-pipeline.md`.
- Relevant sources: `research_control/README.md`,
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`,
  `registries/RESEARCH_TASK_REGISTRY.csv` if present.

### Constraints

- Preserve `proposal-only`, `draft/control`, `source-extension`, and
  `fail-closed` meanings.
- Do not turn source-extension readiness into adoption.

### Implementation Notes

- Build a narrative flow with a diagram only if it reduces reader burden.
- Emphasize why claim laundering is blocked.
- Link to Gate Chair/human gates and claim-boundary explorer.

### Acceptance Criteria

- [ ] Page explains how a candidate can proceed without claim promotion.
- [ ] Page distinguishes validator success, stress survival, selector status,
  and human-gated decision.
- [ ] Dossier records forbidden implications.

### Validation

- Page minimum validation profile.
- Add `npm run validate:svg` if a new or changed SVG/static diagram is used.
- Desktop/mobile browser QA.

### Done When

The route is a clear public explanation of source-extension workflow and passes
the anti-slop gate.

## Task PG-004: Create Gate Chair And Human-Gated Decisions Page

### Goal

Create `/project/physics/gate-chair-and-human-gates/` explaining protected
decision authority and exact authorization.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-006, REQ-007.
- Inventory item: INV-004.
- Required analysis:
  `docs/system-analyses/gate-chair-and-human-gated-decisions.md`.
- Relevant sources: latest handoff YAML/Markdown,
  `registries/AGENT_ROLE_REGISTRY.csv`, `registries/CLAIM_BOUNDARY_REGISTRY.csv`.

### Constraints

- Gate readiness is not a Gate Chair verdict.
- Validators cannot promote claims.
- Do not disclose sensitive local workflow details beyond public-safe evidence.

### Implementation Notes

- Use public layer to explain why human gates exist.
- Use specialist layer to explain authorization, role authority, and validator
  limits.
- Cross-link to source-extension pipeline and current state.

### Acceptance Criteria

- [ ] Page makes human-gated authority understandable to non-specialists.
- [ ] Page states what validators cannot decide.
- [ ] Source evidence is pinned or explicitly scoped.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The page can be cited by later high-risk pages whenever human-gated status
must be understood.

## Task PG-005: Create Claim Boundary Explorer And Strengthen Source Authority

### Goal

Create `/project/source-authority/claim-boundary-explorer/` and strengthen the
source-authority landing so allowed and forbidden claim forms are visible.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007, REQ-008.
- Inventory item: INV-005.
- Related route: `/project/source-authority/`.
- Required analysis: `docs/system-analyses/claim-boundary-explorer.md`.
- Relevant source: `registries/CLAIM_BOUNDARY_REGISTRY.csv`.

### Constraints

- Avoid leaking local absolute paths in public output.
- Do not make the explorer look like a legal or scientific certification UI.
- Keep GitHub/source links as provenance.

### Implementation Notes

- Use a static, source-pinned table or cards.
- Include plain-language examples of allowed versus forbidden wording.
- Link from physics claim-gates and source-authority pages.

### Acceptance Criteria

- [ ] Readers can distinguish allowed explanation from forbidden promotion.
- [ ] Registry-derived data has manifest/provenance coverage.
- [ ] Source-authority landing links to the explorer internally.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Desktop/mobile browser QA for source-authority routes.

### Done When

Claim-boundary behavior is inspectable through the website without replacing
upstream authority.

## Task PG-006: Create General-Public Guided Start

### Goal

Create the first guided-start path for general-public readers.

### Context

- PRD requirements: REQ-006, REQ-008, REQ-010, REQ-012.
- Accepted decision: primary reader is the general public.
- Suggested route: `/resources/guided-starts/general-public/` or a route
  chosen by the foundation packet.

### Constraints

- Guided starts assemble existing sourced pages; they do not create new claims.
- This packet depends on FND-002 and should prefer already implemented
  authority/orientation routes.

### Implementation Notes

- Explain what to read first, what each page answers, and when to inspect
  provenance.
- Include short paths for "what is this?", "what is currently claimed?", and
  "what should I not infer?".

### Acceptance Criteria

- [ ] A public reader gets a clear first reading path.
- [ ] The route points to internal pages first.
- [ ] No new scientific claims are introduced.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Desktop/mobile browser QA.

### Done When

The site has a public-first guided route that can anchor broader navigation.

## Task PG-007: Rewrite AEther Ontology Vocabulary Page

### Goal

Rewrite `/project/physics/ontology/` as a public-first ontology vocabulary and
source-boundary page.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-009.
- Required analysis:
  `docs/system-analyses/aether-flow-ontology-vocabulary.md`.

### Constraints

- Ontology vocabulary is not a completed GR derivation.
- Registered TeX sources carry authority where applicable; PDFs are
  human-readable derivatives.

### Implementation Notes

- Start with AEther, AEther-flow, observed space, S-time, and expansion in
  plain language.
- Put source status and technical vocabulary after the public layer.
- Cross-link to documents, exact-GR benchmark, and Distance-to-GR.

### Acceptance Criteria

- [ ] Public layer defines vocabulary without overclaiming.
- [ ] Specialist layer names the relevant ontology source basis.
- [ ] Dossier identifies safe and unsafe summaries.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The ontology route is readable by non-specialists and disciplined enough for
specialist inspection.

## Task PG-008: Rewrite Exact-GR Benchmark Versus Derivation

### Goal

Rewrite `/project/physics/exact-gr-benchmark/` to distinguish benchmark
compatibility, derivation, and promotion.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-010.
- Required analysis:
  `docs/system-analyses/exact-gr-benchmark-versus-derivation.md`.

### Constraints

- No completed first-principles GR derivation claim.
- No benchmark promotion unless upstream evidence permits it.

### Implementation Notes

- Use a public-first contrast: "matching a benchmark" versus "deriving it from
  source ontology".
- Cross-link to Distance-to-GR, current state, ontology, and claim boundaries.

### Acceptance Criteria

- [ ] The page prevents readers from confusing benchmark target with proven
  derivation.
- [ ] Specialist section identifies relevant source records and limitations.
- [ ] Related routes guide readers internally.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The benchmark route can carry readers through the central physics boundary
without strengthening the claim.

## Task PG-009: Create Metric Response Ladder Page

### Goal

Create `/project/physics/metric-response-ladder/` explaining `Resp_lc`,
`M_src`, `MetricData(E)`, `g_eff`, and matter-coupling ladder status.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-006, REQ-007.
- Inventory item: INV-011.
- Required analysis: `docs/system-analyses/metric-response-ladder.md`.

### Constraints

- Preserve `no MetricData(E)` and `no g_eff` where source-true.
- Do not imply downstream unlocks unless the ledger and human-gated evidence
  support them.

### Implementation Notes

- Use a careful glossary and ladder diagram if it reduces reader burden.
- Explain object names without requiring mathematical background in the first
  section.
- Put technical detail in the specialist layer.

### Acceptance Criteria

- [ ] Public layer explains why the ladder matters.
- [ ] Specialist layer names object status and blocked promotions.
- [ ] Hard-boundary phrases are preserved exactly where needed.

### Validation

- Page minimum validation profile.
- Add `npm run validate:svg` if diagram assets change.
- Desktop/mobile browser QA.

### Done When

The page explains the derivation-object ladder without creating downstream GR
claims.

## Task PG-010: Create Finite Toy Models Page

### Goal

Create `/project/physics/finite-toy-models/` explaining finite toy models and
why one route froze.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-006, REQ-007.
- Inventory item: INV-012.
- Required analysis:
  `docs/system-analyses/finite-toy-models-and-frozen-route.md`.

### Constraints

- A `frozen negative` route is a scoped negative result, not global theory
  rejection.
- Do not overread toy models as physical derivations.

### Implementation Notes

- Explain why toy models are useful, what they can test, and what they cannot
  prove.
- Link to negative results and Distance-to-GR.

### Acceptance Criteria

- [ ] Page explains the frozen route without fatalism or overclaiming.
- [ ] Source references identify the scoped obstruction.
- [ ] Public and specialist layers are clearly separated.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

Finite toy model status is understandable and source-bounded.

## Task PG-011: Create No-Target-Import Discipline Page

### Goal

Create `/project/physics/no-target-import-discipline/` explaining why hidden
target-metric, target-topology, and benchmark-success imports are blocked.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-013.
- Required analysis: `docs/system-analyses/no-target-import-discipline.md`.

### Constraints

- This page explains methodology and guardrails, not proof of a candidate.
- Do not imply all target imports have been eliminated from all future work.

### Implementation Notes

- Use examples of what counts as target import versus acceptable source-side
  construction.
- Cross-link to source-extension pipeline and claim-boundary explorer.

### Acceptance Criteria

- [ ] Readers understand why the guardrail exists.
- [ ] Specialist readers can inspect the source basis.
- [ ] Unsafe summaries are recorded in the dossier.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The route explains methodological discipline without presenting it as completed
physics proof.

## Task PG-012: Create Negative Results And Frozen Routes Page

### Goal

Create `/project/physics/negative-results-and-frozen-routes/` showing how
failed or blocked routes become useful preserved evidence.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-006, REQ-007.
- Inventory item: INV-008.
- Required analysis:
  `docs/system-analyses/negative-results-and-frozen-routes.md`.

### Constraints

- Scoped obstruction is not global theory rejection.
- Do not hide limitations behind positive framing.

### Implementation Notes

- Pair plain-language examples with source-backed status.
- Link to finite toy models, Distance-to-GR, and claim boundaries.

### Acceptance Criteria

- [ ] Page presents negative results as rigorous evidence, not failure theater.
- [ ] Claim boundaries prevent global overread.
- [ ] Source records are inspectable through provenance.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The page improves trust by making preserved negative evidence intelligible.

## Task PG-013: Create Coupling-Law Candidate Status Page

### Goal

Create `/project/physics/coupling-law-candidate-status/` only after source
evidence is clean, pinned, and safe to present.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-007, REQ-011.
- Inventory item: INV-014.
- Required analysis:
  `docs/system-analyses/coupling-law-candidate-status.md`.
- Depends on PG-001, PG-003, PG-004, and PG-005.

### Constraints

- Very high claim risk.
- No coupling-law adoption.
- No matter-coupling derivation or adoption.
- No Einstein equations.
- No benchmark promotion.
- No completed derivation.
- Use `human review pending` if automated checks pass but claim risk remains.

### Implementation Notes

- If evidence is not frozen to a known commit, stop as blocked.
- Treat the page as status and precondition explanation, not a result page.
- Keep hard boundaries visible near the top.

### Acceptance Criteria

- [ ] Page states candidate status without adopting the candidate.
- [ ] Prerequisite pages exist and are linked.
- [ ] No-ai-slop refuter pass explicitly checks overclaiming.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Desktop/mobile browser QA.
- Manual source-boundary review before marking beyond `human review pending`.

### Done When

The page exists only if the source evidence supports safe publication; otherwise
the packet closes as blocked with reasons.

## Task PG-014: Rewrite Research-Agent Workflow Walkthrough

### Goal

Rewrite `/project/ai-research-agent-system/workflow/` as a concrete record-chain
walkthrough.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-007.
- Required analysis:
  `docs/system-analyses/research-agent-workflow-walkthrough.md`.

### Constraints

- Do not present AI-agent workflow as physics proof.
- Sanitized examples only if records expose local-sensitive information.

### Implementation Notes

- Show task, Director decision, AgentJob, completion, handoff, and registry
  chain.
- Use source-first explanation and internal route links.

### Acceptance Criteria

- [ ] General public can understand the workflow purpose.
- [ ] Specialist layer names control records and validation limits.
- [ ] Dossier records source basis and unsafe interpretations.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The workflow route explains one governed work chain without anthropomorphizing
or overclaiming model behavior.

## Task PG-015: Create One Bounded AgentJob Page

### Goal

Create `/project/ai-research-agent-system/one-bounded-agentjob/` as a concrete
example of one auditable transaction.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-015.
- Required analysis:
  `docs/system-analyses/one-bounded-agentjob-in-practice.md`.

### Constraints

- Do not expose private local details.
- Do not imply one AgentJob can settle broad project truth.

### Implementation Notes

- Use a sanitized or source-approved example.
- Explain inputs, allowed paths, outputs, validators, completion, and handoff.

### Acceptance Criteria

- [ ] Page demonstrates auditability at one-transaction scale.
- [ ] Public and specialist layers are distinct.
- [ ] Source links are provenance only.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The route gives readers a concrete mental model for bounded execution.

## Task PG-016: Rewrite Parent-Child Parallel Synthesis

### Goal

Rewrite `/project/ai-research-agent-system/parent-child-synthesis/` with a
clear lifecycle diagram and one-outer-job boundary.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-016.
- Required analysis:
  `docs/system-analyses/parent-child-parallel-synthesis-walkthrough.md`.

### Constraints

- Parallel perspectives do not create parallel authority.
- Preserve one outer AgentJob framing.

### Implementation Notes

- Reuse existing SVG/diagram only if it passes visual and anti-slop review.
- Make conflict handling and parent fusion clear.

### Acceptance Criteria

- [ ] Page explains parent-child synthesis to a general reader.
- [ ] Specialist layer covers authority and conflict boundaries.
- [ ] Diagram, if present, is accessible and source-bounded.

### Validation

- Page minimum validation profile.
- Add `npm run validate:svg` if SVG/diagram assets change.
- Desktop/mobile browser QA.

### Done When

The page explains parallel synthesis without implying independent child-agent
authority.

## Task PG-017: Create Role Authority Inspector

### Goal

Create `/project/ai-research-agent-system/role-authority-inspector/` explaining
why role labels do not grant live permissions.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-017.
- Required analysis: `docs/system-analyses/role-authority-inspector.md`.
- Relevant source: `registries/AGENT_ROLE_REGISTRY.csv`.

### Constraints

- Do not turn registry display into permission grant.
- Avoid leaking local operational details not intended for public pages.

### Implementation Notes

- Use a static filterable-looking table only if static rendering remains clear.
- Link to roles-and-skills, role routing, and source authority.

### Acceptance Criteria

- [ ] Readers understand role authority versus execution authority.
- [ ] Registry status is represented without overstatement.
- [ ] Dossier defines safe and unsafe summaries.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Desktop/mobile browser QA.

### Done When

The route makes role authority inspectable without creating new authority.

## Task PG-018: Rewrite Memory Preflight And Source-First Retrieval

### Goal

Rewrite `/project/ai-research-agent-system/memory-registries/` around memory
preflight, source-first retrieval, and registry authority.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-018.
- Required analysis:
  `docs/system-analyses/memory-preflight-and-source-first-retrieval.md`.

### Constraints

- Memory accelerates lookup; it is not source authority.
- Do not expose private memory contents.

### Implementation Notes

- Use public language for why memory exists.
- Specialist layer should explain authority order and verification.

### Acceptance Criteria

- [ ] Page separates memory, retrieval, registry, and source authority.
- [ ] Page links to workflow and source-authority routes.
- [ ] No sensitive memory details are included.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The memory route teaches source-first retrieval without elevating memory to
authority.

## Task PG-019: Rewrite Validator PASS Does Not Mean Physics Proof

### Goal

Rewrite `/project/operations/validator-operator-workflow/` so validator PASS
limits are explicit and understandable.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-019.
- Required analysis:
  `docs/system-analyses/validator-pass-does-not-mean-physics-proof.md`.

### Constraints

- PASS is bounded to checked state.
- Validator success cannot promote scientific claims.

### Implementation Notes

- Use examples to separate operational validation from physics proof.
- Link to Gate Chair/human gates, claim-boundary explorer, and workflow.

### Acceptance Criteria

- [ ] Public reader understands what PASS can and cannot mean.
- [ ] Specialist layer identifies validators and boundaries.
- [ ] Dossier records unsafe PASS interpretations.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The validator route becomes a reusable anti-overclaiming reference.

## Task PG-020: Rewrite Project-System Improvement Loop

### Goal

Rewrite `/project/operations/project-system-improvement/` as a public and
maintainer-readable explanation of improvement signals, sidecars, and bounded
maintenance packets.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007.
- Inventory item: INV-020.
- Required analysis:
  `docs/system-analyses/project-system-improvement-loop.md`.

### Constraints

- Do not imply maintenance signals change physics status.
- Keep process claims source-backed.

### Implementation Notes

- Explain drift, signal classification, sidecars, and repair loops.
- Link to operations, validator workflow, and source authority.

### Acceptance Criteria

- [ ] Public layer explains why improvement control matters.
- [ ] Specialist layer names operational interfaces and failure modes.
- [ ] Page reduces maintainer review burden.

### Validation

- Page minimum validation profile.
- Desktop/mobile browser QA.

### Done When

The improvement-loop route is clear, grounded, and useful to both public and
maintainer readers.

## Task PG-021: Revamp Remaining Operations Route Family

### Goal

Revamp operations pages not otherwise covered by inventory-specific tasks:
Director/AgentJob lifecycle, role routing, publication process, technical
requirements, and operations landing consistency.

### Context

- PRD requirements: REQ-006, REQ-007, REQ-008.
- Relevant routes:
  - `/project/operations/`
  - `/project/operations/director-agentjob-lifecycle/`
  - `/project/operations/role-routing/`
  - `/project/operations/publication-process/`
  - `/project/operations/technical-requirements/`

### Constraints

- These pages explain operations; they do not change execution contracts.
- Existing prose is suspect and must pass evidence review.

### Implementation Notes

- Use lightweight route-audit notes if full system analyses are not needed for
  low-risk operational cleanup.
- For claim-bearing operation claims, create or verify system analyses.
- Normalize navigation and source notices.

### Acceptance Criteria

- [ ] Operations pages share the layered page model.
- [ ] Route family links are coherent.
- [ ] No page implies operational success is scientific proof.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Desktop/mobile browser QA for the operations family.

### Done When

Operations pages read as one coherent system rather than disconnected summaries.

## Task PG-022: Rewrite Ontology Document Library With Reading Guide

### Goal

Rewrite `/resources/documents/` as an ontology document library with a public
reading guide.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007, REQ-008.
- Inventory item: INV-006.
- Required analysis:
  `docs/system-analyses/ontology-document-library-reading-guide.md`.

### Constraints

- Registered TeX sources carry authority; PDFs are human-readable derivatives.
- Do not imply all documents are equally current or authoritative.

### Implementation Notes

- Add "read this first" and specialist reading order.
- Make source status visible.
- Link to ontology vocabulary and source authority.

### Acceptance Criteria

- [ ] Readers know which documents to start with and why.
- [ ] TeX/PDF authority distinction is explicit.
- [ ] Manifest-backed assets remain valid.

### Validation

- Page minimum validation profile.
- `npm run validate:manifests`
- Desktop/mobile browser QA.

### Done When

The document library becomes a guided resource rather than a file shelf.

## Task PG-023: Rewrite Visual Diagram Gallery By Concept

### Goal

Rewrite `/resources/diagrams/` as a diagram gallery grouped by physics, AI
workflow, operations, and source authority.

### Context

- PRD requirements: REQ-006, REQ-007, REQ-008.
- Inventory item: INV-024.
- Required analysis:
  `docs/system-analyses/visual-diagram-gallery-by-concept.md`.

### Constraints

- Diagrams are analysis aids, not authority.
- Public SVG artwork must remain animated and textless when used as SVG.
- Static Mermaid PNGs must remain registered through the existing renderer and
  manifests.

### Implementation Notes

- Preserve useful existing diagram assets.
- Add concept grouping and captions that explain boundaries.
- Do not embed runtime Mermaid in public pages.

### Acceptance Criteria

- [ ] Gallery is organized by reader concept, not raw asset order.
- [ ] Each diagram has alt text, caption, and provenance.
- [ ] SVG/diagram policy validation passes.

### Validation

- Page minimum validation profile.
- `npm run validate:svg`
- Desktop/mobile browser QA.

### Done When

The diagram gallery helps readers navigate concepts without elevating diagrams
to source authority.

## Task PG-024: Create Publication And Provenance System Page

### Goal

Create `/project/source-authority/publication-and-provenance-system/` explaining
page provenance, source manifests, asset manifests, route maps, and
internal-first routing.

### Context

- PRD requirements: REQ-003, REQ-006, REQ-007, REQ-008.
- Inventory item: INV-023.
- Required analysis:
  `docs/system-analyses/publication-and-provenance-system.md`.

### Constraints

- Mostly operational; do not turn manifest presence into source truth.
- Keep local paths out of public copy.

### Implementation Notes

- Use the website architecture doc and public manifests as evidence.
- Explain how page hashes and source hashes constrain publication.
- Link to source-authority landing and resources.

### Acceptance Criteria

- [ ] Public reader understands why provenance exists.
- [ ] Maintainer reader can identify which manifest does what.
- [ ] Source links remain provenance.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Desktop/mobile browser QA.

### Done When

The site has a clear explainer for its own publication and provenance system.

## Task PG-025: Create Specialist Guided Starts

### Goal

Create or complete first-class guided-start paths for physicists,
mathematicians, AI/agent researchers, software/system engineers, and external
reviewers.

### Context

- PRD requirements: REQ-006, REQ-008, REQ-010.
- Inventory items: INV-021 and INV-022.
- Accepted audience decision also adds mathematicians, software/system
  engineers, engineers, scientists, and reviewers.

### Constraints

- Guided starts assemble sourced pages; they must not create new claims.
- Reviewer path should not become the reviewer packet until PG-026 prerequisites
  pass.

### Implementation Notes

- Use the route model chosen in FND-001.
- Create separate routes or anchored sections depending on foundation decision.
- Each audience path should state what to read first and what not to infer.

### Acceptance Criteria

- [ ] Each specialist audience has a clear internal-first path.
- [ ] Routes avoid duplicating high-risk claim copy.
- [ ] Reviewer path points to prerequisites before reviewer packet.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Desktop/mobile browser QA for guided-start routes.

### Done When

Specialist readers have practical reading routes without weakening the
general-public first-page model.

## Task PG-026: Create External Reviewer Packet

### Goal

Create `/resources/reviewer-packet/` only after authority/orientation
prerequisites are complete.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-007, REQ-011.
- Inventory item: INV-025.
- Required analysis: `docs/system-analyses/external-review-packet.md`.
- Prerequisites:
  - PG-001 current state.
  - PG-002 Distance-to-GR.
  - PG-005 claim boundary/source authority.
  - PG-022 document reading guide.
  - Relevant guided starts.

### Constraints

- Highest risk for accidental overclaiming.
- Must state what is claimed, not claimed, and where to inspect sources.
- Use `human review pending` unless the user approves a stronger status.

### Implementation Notes

- Build a concise route for reviewers, not a marketing packet.
- Include source-first inspection order and exact boundaries.
- Run a no-ai-slop refuter pass with special attention to scientific claims.

### Acceptance Criteria

- [ ] Prerequisite pages exist and pass.
- [ ] Page states claim boundaries before source inspection paths.
- [ ] External reviewer can find ontology, current state, Distance-to-GR, and
  source authority routes.
- [ ] No unsupported scientific viability claim is added.

### Validation

- Page minimum validation profile.
- `npm run validate:links`
- Full `npm run validate` recommended because this route aggregates many
  sources.
- Desktop/mobile browser QA.

### Done When

The reviewer packet is safe, source-backed, and explicitly staged for human
review.

## Task RT-001: Consolidate Or Retire Prototype Research Routes

### Goal

Consolidate or retire `/research/map/`, `/research/equations/`, and
`/research/math-sample/` unless each becomes an inventory-backed route with a
clear reader job.

### Context

- PRD requirements: REQ-009, REQ-012.
- Relevant files:
  - `src/pages/research/map.astro`
  - `src/pages/research/equations.mdx`
  - `src/pages/research/math-sample.mdx`
  - `src/lib/siteContent.ts`
  - `public/files/manifests/page_route_map.json`

### Constraints

- Do not break internal links silently.
- If deleting a route, provide a replacement internal route or clear route-map
  update.
- Do not deploy until route retirement is reviewed.

### Implementation Notes

- Search all internal references before changing routes.
- Fold useful equation or map material into relevant physics/resources pages.
- Update route maps, navigation, and provenance expectations.

### Acceptance Criteria

- [ ] Prototype routes are removed from primary navigation or converted into
  true sourced pages.
- [ ] Internal links do not point to retired routes.
- [ ] Route maps and provenance are consistent.

### Validation

- `npm run validate:links`
- `npm run validate:provenance`
- `npm run build`
- Browser QA for replacement routes.

### Done When

The public site no longer exposes sample/demo routes as if they were finished
reader-facing pages.

## Task QA-001: Run Final Sitewide Revamp QA

### Goal

Run release-candidate validation, browser QA, anti-slop review, and final route
coverage audit for the revamp branch.

### Context

- PRD requirements: all requirements.
- Depends on all selected milestone tasks.
- Relevant commands:
  - `npm run validate`
  - `npm run quality`
  - `python3 -m pytest`

### Constraints

- Do not deploy.
- Do not mark blocked/high-risk pages as final without human review if the
  packet requires it.
- Do not paper over validation failures from source drift; name them.

### Implementation Notes

- Review every route in `src/pages/` against the inventory-to-route matrix.
- Check page provenance, route maps, source manifests, and asset manifests.
- Run desktop and mobile browser QA for representative pages in every route
  family.
- Prepare a concise release-readiness note with pass/fail status and remaining
  risk.

### Acceptance Criteria

- [ ] Every inventory item is implemented, explicitly staged, or blocked with a
  source-authority reason.
- [ ] Every public route is either revamped, intentionally retained, or retired.
- [ ] Full validation and quality gates are run or skipped with concrete
  reasons.
- [ ] Browser QA covers mobile and desktop.
- [ ] No deployment occurs.

### Validation

- `npm run validate`
- `npm run quality`
- `python3 -m pytest`
- Browser QA across homepage, track landings, first-wave pages, resource pages,
  guided starts, and any newly created high-risk pages.

### Done When

The branch is ready for human review and a separate deployment decision.
