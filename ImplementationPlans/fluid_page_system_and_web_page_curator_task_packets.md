# Codex Task Packets: Fluid Page System and `web-page` Curator

## Packet Set

- Source plan:
  `ImplementationPlans/fluid_page_system_and_web_page_curator_implementation_plan.md`
- Repository:
  `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website`
- Planning status: ready with assumptions; implementation remains gated by
  `GATE-00` and source-sensitive work by `SRC-01`.
- Core packets: 20.
- Instantiated route-migration packets: 24.
- Total planned packets: 44.
- Conditional legacy implementation packets: created only after `LEGACY-01`
  supplies an evidence-backed disposition.

## Shared Execution Contract

Every packet in this file inherits these rules:

1. Resolve and obey the live implementation-control task, job, completion, and
   handoff. This plan is routing context, not write authority.
2. Work on at most one shared foundation concern or one public route.
3. Preserve unrelated dirty and untracked files.
4. Do not write to `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
5. For source-derived claims, use a clean immutable upstream source view at the
   accepted pin selected by the live packet.
6. Do not strengthen scientific, mathematical, governance, current-state, or
   research-workflow claims.
7. Keep internal website routes primary and source/GitHub links contextual.
8. `/resources/*` routes must not render a dedicated Source authority section.
9. Website SVG artwork remains animated, accessible, and free of visible
   embedded text.
10. Do not add a production dependency without a separately justified
    architecture decision.
11. Record commands actually run, their outcomes, browser artifacts, remaining
    uncertainty, and rollback boundary in the handoff or QA receipt.
12. Stop before checkpoint, push, or deployment unless the live handoff and a
    separate user authorization permit the action.

The expected branch/PR scope for every packet is the packet itself. Do not
combine adjacent tasks because they appear mechanically similar.

### Explicit coverage for requirements otherwise referenced by ranges

- `REQ-002` responsive gutters maps to `FOUND-01` and every runtime page packet.
- `REQ-004` readable prose maps to `FOUND-01`, `PAGE-01`, `RES-01`, and
  `EXP-01`.
- `REQ-005` wide media/data maps to `FOUND-01`, `RES-03`, `RES-04`, and all
  data/media route instances.
- `REQ-017` the installed `web-page` skill maps to `SKILL-01` and `SKILL-02`.
- `NFR-003` zoom/text-resize behavior maps to `SHELL-01`, every runtime page
  packet, and `QA-01`.
- `NFR-004` keyboard/focus behavior maps to `SHELL-01`, `RES-02`, `RES-03`,
  every interactive route packet, and `QA-01`.
- `NFR-005` reduced-motion behavior maps to `FOUND-01`, every animated route
  packet, and `QA-01`.
- `NFR-007` performance maps to `FOUND-01`, specialized media/library packets,
  and `QA-01`.
- `NFR-010` no new production dependency maps to every packet and receives an
  explicit `package.json` diff review in `QA-01`.

---

## Core Packet GATE-00: Resolve the Existing Homepage Packet

### Goal

Reach a lawful implementation-control state in which the completed
`WI-20260717-001` homepage-action packet is either checkpointed through an
explicitly authorized workflow or remains visibly blocked without opening new
implementation work.

### Context

- PRD requirements: execution prerequisite for all requirements.
- Relevant files:
  `@implementation_control/handoffs/WH-20260717-001.yaml`,
  `@implementation_control/program_state.yaml`, and the completion referenced
  by the live handoff.
- Current observed state: `ready_for_checkpoint`; checkpoint, staging, commit,
  push, deployment, source refresh, and a new packet are not authorized.
- The current packet reports a 12-path dry-run scope and excludes an unrelated
  untracked implementation plan.

### Constraints

- This task does not itself authorize a checkpoint.
- Do not infer authorization from the existence of this plan.
- Do not stage or modify the two new fluid-page planning files as part of the
  homepage packet.
- Preserve all unrelated dirty work.

### Implementation notes

1. Run `npm run continue:implementation -- --summary`.
2. Read the current handoff and completion; do not rely on the 2026-07-17
   snapshot if live state has changed.
3. If the user separately authorizes checkpointing, use the exact command and
   arguments produced by the implementation-control workflow and inspect its
   dry run before mutation.
4. If authorization is absent, stop and report the precise blocker.
5. After a successful checkpoint, rerun the summary and confirm no stale active
   packet prevents `SRC-01`, `SKILL-01`, or `ARCH-01`.

### Acceptance criteria

- [ ] Live implementation-control status is recorded.
- [ ] No unauthorized Git mutation occurs.
- [ ] Any checkpoint includes only the live packet's authorized paths.
- [ ] Unrelated planning files and pre-existing changes remain untouched.
- [ ] The post-action summary identifies the lawful next packet state.

### Validation

- `npm run continue:implementation -- --summary`
- `npm run validate:implementation-control`
- `git status --short --branch`
- Checkpoint dry run and post-checkpoint validation only when explicitly
  authorized by the live workflow and user.

### Done when

The existing packet no longer creates an ambiguous write boundary, or the task
has stopped with the missing checkpoint authorization stated exactly.

---

## Core Packet SRC-01: Classify Upstream Source Drift

### Goal

Determine whether clean upstream `main` should replace the website's accepted
source pin, resolve the critical `/physics/claim-status/` drift decision, and
produce a route-level freshness decision without reading claim authority from
the dirty upstream worktree.

### Context

- PRD requirements: `REQ-020`, `REQ-022`, `REQ-027`, `NFR-009`, `NFR-011`.
- Relevant files:
  `@scripts/run_curator.py`,
  `@public/files/manifests/page_route_map.json`,
  `@public/files/manifests/page_provenance.json`,
  curator reports under `docs/quality/`, and source-refresh scripts.
- Planning snapshot:
  accepted pin `57438af555214bc0785dcb390ee6254f580b8a62`;
  clean upstream `main` `fd802dee85da59d29c71842f9dcfa882a0927c29`;
  41 curator items, including one critical claim-boundary change.

### Constraints

- Depend on `GATE-00`.
- Fetch/read operations may update remote-tracking metadata only if the live
  packet permits them; no upstream writes.
- Never use the upstream dirty branch as a publication source.
- Do not combine source refresh with page-template or CSS changes.
- A newer upstream commit observed during execution supersedes this planning
  snapshot and must be recorded.

### Implementation notes

1. Resolve the current accepted source pin from control/provenance records.
2. Resolve current upstream `origin/main`.
3. Create a temporary clean detached source view at the candidate commit.
4. Run the curator against that exact source root.
5. Review every critical item and group review-required items by route and
   dependency.
6. For `/physics/claim-status/`, inspect the changed claim-boundary registry and
   the page's current-state snapshot contract; do not infer a public copy
   change from a hash change alone.
7. Produce one decision:
   - retain the existing pin;
   - adopt the candidate pin with required generated updates;
   - or block adoption pending upstream/owner review.
8. If adoption is authorized, regenerate source-derived artifacts as one
   coherent set and rerun all source/provenance/quality gates.

### Acceptance criteria

- [ ] The comparison uses clean immutable source roots.
- [ ] Candidate and accepted commits are recorded as 40-character hashes.
- [ ] All critical drift is resolved or explicitly blocking.
- [ ] Every review-required item has `refresh`, `acknowledge`, or `defer with
  reason` status.
- [ ] No upstream file is modified.
- [ ] Claim-sensitive page packets receive an explicit go/no-go gate.
- [ ] Generated records never mix two source commits.

### Validation

- `npm run validate:content`
- `npm run validate:provenance`
- `npm run validate:curator`
- `npm run validate:claims`
- `npm run validate:manifests` when source/asset manifests change
- `npm run validate`
- `npm run quality`
- `git diff --check`
- Focused Python tests for any refresh script changed, followed by
  `python3 -m pytest`.

### Done when

The accepted source binding and affected-route decisions are reproducible, the
critical drift is resolved or a precise blocker is recorded, and no page design
work is mixed into the packet.

---

## Core Packet SKILL-01: Create the `web-page` Curator Skill

### Goal

Create the repository-local `web-page` skill and its flexible page-guidance
templates so a Codex agent can design, analyze, engineer, implement, validate,
and hand off one page or one shared page-system concern.

### Context

- PRD requirements: `REQ-006`, `REQ-008`–`REQ-018`, `REQ-020`–`REQ-025`,
  `REQ-030`, `NFR-001`–`NFR-012`.
- New directory: `@.codex/skills/web-page/`.
- Existing examples:
  `@.codex/skills/implementation-control/SKILL.md`,
  `@.codex/skills/system-analysis/SKILL.md`,
  `@.codex/skills/technical-writing-quality-gate/SKILL.md`, and their agent
  manifests.
- Existing content template:
  `@docs/content-dossiers/_template.md`.

### Constraints

- Depend on `GATE-00`.
- This packet creates procedural documentation and templates, not runtime page
  code.
- The skill must not replace implementation-control, system-analysis,
  technical-writing, Mermaid, or deployment skills.
- Templates are guidance; do not enforce one section order or one visual
  composition.
- The skill may not authorize upstream writes, Git checkpoint, push, or deploy.

### Implementation notes

1. Create `SKILL.md` with explicit trigger rules, role lenses, preflight,
   page-family classification, source gate, design brief, bounded
   implementation, QA, receipt, and stop conditions.
2. Create `agents/openai.yaml` following the installed manifest shape.
3. Add references for authority, family routing, freshness, UI/UX quality, and
   browser QA.
4. Add guidance templates for:
   - page implementation brief;
   - page review receipt;
   - home;
   - overview;
   - general resource;
   - Library;
   - Diagram Gallery;
   - document library;
   - explainer;
   - utility/legal.
5. Mark each template's invariants, recommended modules, conditional modules,
   forbidden defaults, validation profile, and allowed design flexibility.
6. Require the skill to name the reader job, layout rationale, containment
   decisions, source basis, and smallest change boundary before editing.
7. Require one route or one shared foundation concern per invocation.
8. Register the skill in `.codex/skills/README.md`.

### Acceptance criteria

- [ ] The skill is named exactly `web-page`.
- [ ] UI/UX designer, system analyst, system engineer, and page-curator roles
  are explicit and operational.
- [ ] All requested templates exist, plus evidence-supported document,
  explainer, and utility guidance.
- [ ] Template flexibility is explicit and testable.
- [ ] Source authority, resource-page rule, SVG policy, internal-first links,
  accessibility, and implementation-control boundaries are explicit.
- [ ] The skill stops after one bounded packet and requires a validation
  summary.
- [ ] The skill README entry is accurate.

### Validation

- `git diff --check`
- Manual comparison with existing local skill structures.
- `npm run validate:implementation-control` when control records change.
- Run focused Markdown/skill tests introduced by `SKILL-02`; until then, record
  manual contract review.

### Done when

The skill package is complete enough to invoke without relying on this plan or
open-editor state, but no runtime route has been modified.

---

## Core Packet SKILL-02: Validate the Skill and Template Contracts

### Goal

Add focused, maintainable validation that detects missing `web-page` skill
files and mandatory guidance invariants without turning flexible templates into
a rigid DOM or prose schema.

### Context

- PRD requirements: `REQ-016`–`REQ-021`, `REQ-024`, `REQ-030`,
  `NFR-008`–`NFR-011`.
- Relevant files:
  `@.codex/skills/web-page/`,
  `@tests/`,
  `@scripts/`,
  `@package.json`.

### Constraints

- Depend on `SKILL-01`.
- Validate presence and safety contracts, not exact wording or template order.
- Prefer one focused Python validator/test module.
- Do not add a production dependency.
- Do not add an npm script unless it materially improves the existing
  `validate` chain and the packet justifies the maintenance cost.

### Implementation notes

1. Validate the skill header/name/description and required agent manifest keys.
2. Validate the required references and templates exist.
3. Check that every page template includes:
   reader job, invariants, flexible/optional modules, source boundary,
   accessibility, validation, and review state.
4. Check resource templates explicitly prohibit a dedicated source-authority
   section.
5. Check Diagram Gallery guidance includes manifest, accessibility, fallback,
   and no-source-proof boundaries.
6. Check skill workflow contains live control preflight, clean source
   requirement, one-bounded-packet rule, validation receipt, and stop before
   push/deploy.
7. Add negative fixtures or temporary test inputs only when they clarify a real
   failure mode.

### Acceptance criteria

- [ ] Removing a required template causes a focused failure.
- [ ] Removing a safety invariant causes a focused failure.
- [ ] Reordering optional modules does not fail.
- [ ] Adding page-specific creative guidance does not fail.
- [ ] Failure messages name the missing contract and file.
- [ ] The validator is documented and runs in the repository test environment.

### Validation

- Focused test command for the new test module.
- `python3 -m pytest`
- `git diff --check`
- `npm run validate:implementation-control`
- `npm run validate` only if `package.json` or the aggregate validation chain
  changes.

### Done when

The skill's non-negotiable safety and completeness contract is executable while
its design guidance remains flexible.

---

## Core Packet ARCH-01: Inventory Routes and Assign Page Families

### Goal

Create a live route-family and migration ledger that accounts for all current
Astro routes, maps governed modern routes to a page template, and sends
ambiguous `/project/*` routes to `LEGACY-01`.

### Context

- PRD requirements: `REQ-019`, `REQ-028`, `REQ-029`, `NFR-008`, `NFR-011`.
- Relevant files:
  `@src/pages/`,
  `@public/files/manifests/page_route_map.json`,
  `@public/files/manifests/page_provenance.json`,
  `@docs/architecture/sitewide-greenfield-foundation-contract.md`,
  `@docs/quality/sitewide-greenfield-review-ledger.md`.
- Planning inventory: 64 Astro routes, 34 governed route-map records, and 30
  `/project/*` routes requiring disposition.

### Constraints

- Depend on `GATE-00`; may be performed before `SRC-01` closes because it does
  not change claims.
- This is an inventory/architecture packet, not a route migration.
- Do not mark a route obsolete merely because it is absent from the current
  route map.
- Do not create runtime data unless a real runtime consumer is justified.

### Implementation notes

1. Regenerate the route inventory from the filesystem.
2. Record route, source file, page family, navigation role, current shared
   components, route-map/provenance status, source dossier, planned template,
   source sensitivity, migration status, and human review state.
3. Mark the home, overview, modern child, resource-specialized, utility, and
   legacy groups.
4. Assign the 24 repeatable route packets defined later in this file.
5. Add a count/integrity test or script if it can cheaply detect orphan routes.
6. Record baseline fixed-width selectors and component consumers by family.

### Acceptance criteria

- [ ] Every current `.astro` route appears exactly once.
- [ ] Counts are generated or cross-checked, not manually assumed.
- [ ] Every governed modern route has a template and packet ID.
- [ ] Every `/project/*` route is explicitly pending `LEGACY-01`.
- [ ] `/license/` is classified as utility/legal.
- [ ] The ledger distinguishes route existence from canonical navigation.
- [ ] No public route or claim changes.

### Validation

- `git diff --check`
- Route inventory/count command recorded in the packet.
- Focused test for ledger coverage if added.
- `python3 -m pytest` when tests/scripts change.
- `npm run validate:implementation-control`.

### Done when

The migration can be tracked without relying on memory, and every present route
has one unambiguous planning state.

---

## Core Packet FOUND-01: Build the Fluid Layout Foundation

### Goal

Introduce the semantic width modes, responsive grid, gutters, section rhythm,
and smallest reusable Astro primitives needed for the new page system while
preserving all current routes through compatibility styles.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-025`, `NFR-001`–`NFR-012`.
- Relevant files:
  `@src/styles/global.css`,
  `@src/layouts/BaseLayout.astro`,
  `@src/components/CommandBand.astro`,
  proposed `@src/components/page-templates/`.
- Current fixed-width evidence includes `--max-width: 1120px` and multiple
  `1180px` outer wrappers.

### Constraints

- Depend on `ARCH-01`; preserve any uncheckpointed homepage CSS unless live
  control proves it belongs to a completed checkpoint.
- Shared foundation only: do not redesign a public route in this packet.
- Do not delete compatibility selectors.
- Do not turn all sections into full-width text.
- Scope alarm: if more than three runtime source files or approximately 100
  non-generated lines beyond focused tests are needed, reassess and split.

### Implementation notes

1. Capture the current computed widths for representative home, physics,
   resource, and specialist routes.
2. Add semantic tokens for page gutters, grid gap, section space, prose
   measure, and optional wide safety measure.
3. Add the smallest primitives proven necessary—normally `PageSection` and
   `PageGrid`; defer `MediaFrame`/`SectionHeader` if the pilot can reuse current
   components.
4. Implement width modes `full`, `grid`, `prose`, `media`, and `data`.
5. Provide responsive collapse and safe overflow behavior.
6. Add focused validator/tests for the primitives and forbidden new hard-coded
   outer widths.
7. Preserve current visuals until `PAGE-01` consumes the primitives.
8. Capture performance/build baselines for comparison.

### Acceptance criteria

- [ ] Semantic width modes exist and are documented.
- [ ] Gutters scale without disappearing.
- [ ] Prose and media can use different spans in the same section.
- [ ] Existing routes render without a deliberate redesign.
- [ ] No new client runtime or production dependency.
- [ ] Compatibility behavior is explicit and temporary.
- [ ] Baseline artifacts and rollback boundary are recorded.

### Validation

- Focused component/layout tests.
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run build`
- `python3 -m pytest`
- `git diff --check`
- Run `python3 scripts/frontend_performance_baseline.py` with discovered required
  `--input-dir`, `--json-output`, and `--markdown-output` paths.
- Representative desktop/mobile smoke screenshots.

### Done when

The foundation is usable by the physics pilot, preserves current behavior, and
can be rolled back independently of any route migration.

---

## Core Packet SHELL-01: Make Header and Footer Fluid

### Goal

Migrate the shared navigation and footer from the legacy global width ceiling to
the new gutter/grid system without changing navigation behavior, source notice,
copyright, project links, creator identity, or compact-menu accessibility.

### Context

- PRD requirements: `REQ-001`–`REQ-003`, `REQ-023`, `REQ-025`, `REQ-026`,
  `NFR-002`–`NFR-006`, `NFR-008`.
- Relevant files:
  `@src/layouts/BaseLayout.astro`,
  `@src/styles/global.css`,
  `@src/lib/siteContent.ts`.

### Constraints

- Depend on `FOUND-01`.
- Do not change navigation information architecture or link targets.
- Preserve no-script navigation and footer semantics.
- Do not combine with a page-body migration.

### Implementation notes

1. Replace shell dependence on `var(--max-width)` with the accepted fluid grid
   and gutters.
2. Preserve readable sub-columns in the footer; full width does not mean one
   unbounded text line.
3. Test menu open/close, Escape, focus return, click outside, resize, short
   landscape, and no-script fallback.
4. Verify external links retain safe attributes and accessible labels.
5. Update focused shell/layout tests without encoding incidental pixel values.

### Acceptance criteria

- [ ] Header/footer align with page grid at all target widths.
- [ ] Wide screens use space without stretching footer prose excessively.
- [ ] Mobile and short-landscape menus remain usable.
- [ ] Keyboard focus is visible and logical.
- [ ] No navigation, footer content, or link target is lost.
- [ ] No page-level horizontal overflow is introduced.

### Validation

- `npm run validate:links`
- `npm run validate:layout`
- `npm run build`
- Focused shell/navigation tests and `python3 -m pytest`
- Keyboard/no-script/manual browser matrix
- `git diff --check`

### Done when

The shared shell is fluid and accessible, with unchanged information and
behavior.

---

## Core Packet PAGE-01: Migrate the Physics Overview Pilot

### Goal

Use `/physics/` to prove that the fluid page system fixes the original
fixed-width, over-boxed design problem while preserving copy, actions, visual,
claim boundaries, and reader paths.

### Context

- PRD requirements: `REQ-001`–`REQ-009`, `REQ-020`–`REQ-026`, `REQ-030`,
  `NFR-001`–`NFR-011`.
- Relevant files:
  `@src/pages/physics/index.astro`,
  `@src/components/CommandBand.astro`,
  `@src/components/ProjectIntroduction.astro`,
  `@src/styles/global.css`,
  physics dossier and provenance records.
- Reference viewport: 1533 × 1285 CSS pixels from the user comment.

### Constraints

- Depend on `FOUND-01`; `SRC-01` must be resolved if any copy, source-derived
  status, provenance, or snapshot changes.
- Preserve public copy by default.
- Do not migrate sibling physics routes.
- Retain a visible frame for the hero SVG if the visual-object audit justifies
  it; unbox the page-level narrative by default.

### Implementation notes

1. Create or adopt the smallest `OverviewPageTemplate` contract needed for the
   route.
2. Write the page brief: reader job, hierarchy, grid spans, containment audit,
   and expected wide-screen behavior.
3. Make hero and sections use fluid canvas/grid/prose/media modes.
4. Replace four-sided section panels with spacing, tonal bands, alignment, or
   selective rules where no object boundary exists.
5. Preserve the animated textless SVG, actions, intro, status-layer diagram,
   claim boundary, and internal routes.
6. Compare 1280, 1533, and 1920 screenshots to verify the page actually grows.
7. Record every retained box and its semantic reason.

### Acceptance criteria

- [ ] The main section canvas grows beyond the prior 1180px outer ceiling.
- [ ] Prose remains readable and does not span the full viewport.
- [ ] The hero visual uses a wider media span without distortion.
- [ ] Narrative sections are not uniformly boxed.
- [ ] Actions and internal routes are unchanged unless separately authorized.
- [ ] No page-level overflow at 320px or 400% zoom.
- [ ] Source/claim boundaries remain accurate.
- [ ] A page review receipt and before/after artifacts exist.

### Validation

- `npm run validate:content`
- `npm run validate:claims`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run validate:comprehension`
- `npm run validate:provenance`
- `npm run validate:curator`
- `npm run build`
- Focused tests, then `python3 -m pytest`
- Full viewport/zoom/keyboard/reduced-motion browser QA
- `git diff --check`

### Done when

The owner can compare the pilot directly with the reported problem, all
technical checks pass, and the accepted token/template adjustments are recorded
for later packets.

---

## Core Packet PAGE-02: Migrate the Home Page

### Goal

Implement the unique Home template using the accepted fluid system while
preserving the completed homepage primary-action alignment and public-first
two-track orientation.

### Context

- PRD requirements: `REQ-001`–`REQ-008`, `REQ-016`, `REQ-021`–`REQ-026`,
  `REQ-030`, `NFR-001`–`NFR-011`.
- Relevant files:
  `@src/pages/index.astro`,
  `@src/components/CommandBand.astro`,
  `@src/components/ProjectIntroduction.astro`,
  `@src/styles/global.css`,
  home dossier/provenance.

### Constraints

- Depend on `PAGE-01` and the accepted pilot decisions.
- Verify `WI-20260717-001` is checkpointed; do not regress its row alignment.
- The Home template is unique and must not become a generic overview copy.
- Preserve primary/secondary action labels, destinations, order, and grouping
  unless a separate content packet authorizes change.

### Implementation notes

1. Create/adopt `HomePageTemplate` with flexible slots for hero, introduction,
   two tracks, status, guided starts, and source context.
2. Use full-bleed or tonal bands selectively to create an editorial sequence.
3. Keep continuous two-track explanation unboxed unless a discrete route/action
   object needs containment.
4. Allow the home visual and track orientation to use broader spans.
5. Add a regression assertion for the accepted action alignment if current
   tests do not already cover the migrated markup.
6. Capture wide, mobile, and action-geometry evidence.

### Acceptance criteria

- [ ] Home is recognizably unique.
- [ ] The two-track thesis remains clear and public-first.
- [ ] The completed primary-action alignment holds across its accepted widths.
- [ ] The page uses wide space intentionally without unbounded prose.
- [ ] Internal starts remain primary.
- [ ] Source context remains downstream and accurate.

### Validation

- Home-focused positioning tests
- `npm run validate:content`
- `npm run validate:claims`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:comprehension`
- `npm run validate:provenance`
- `npm run build`
- `python3 -m pytest`
- Full browser matrix and `git diff --check`

### Done when

The Home template is proven by the live route, the prior action fix is
preserved, and no sibling route is migrated.

---

## Core Packet PAGE-03: Migrate the AI Research System Overview

### Goal

Apply the flexible Overview template to `/ai-research-system/` while preserving
the governed research-system explanation, current status, animated visual,
internal child routes, and human-gate boundaries.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-009`, `REQ-016`, `REQ-020`–`REQ-026`,
  `REQ-030`, `NFR-001`–`NFR-011`.
- Relevant files:
  `@src/pages/ai-research-system/index.astro`,
  shared overview components/styles, dossier, route map, provenance.

### Constraints

- Depend on `PAGE-01`; depend on `SRC-01` for any claim/status change.
- Preserve AI governance boundaries and do not anthropomorphize agents.
- Do not copy the Physics composition mechanically; use the same contract but
  a reader-job-specific hierarchy.

### Implementation notes

1. Write the route page brief and containment audit.
2. Reuse Overview slots/primitives while allowing AI-specific status,
   lifecycle, and human-gate emphasis.
3. Convert continuous explanations to open narrative bands.
4. Preserve object frames for diagrams/status records when semantically useful.
5. Review wide layout, long headings, status density, and internal route
   scanning.

### Acceptance criteria

- [ ] The route uses the Overview contract without becoming a Physics clone.
- [ ] The governed, human-accountable nature of the system remains explicit.
- [ ] Long titles and status content reflow cleanly.
- [ ] Primary internal route choices remain discoverable.
- [ ] Claim/source links remain secondary inspection paths.

### Validation

- Standard page validation profile from `PAGE-01`
- AI-specific content/claim diff review
- Browser matrix with long-title and reduced-motion checks
- `git diff --check`

### Done when

The AI overview is fluid, differentiated, source-safe, and technically valid.

---

## Core Packet PAGE-04: Migrate the Resources Overview

### Goal

Apply the Overview template to `/resources/` while creating a clear route into
source authority, registries, library, documents, diagrams, reading paths, and
builder/reviewer resources without a dedicated Source authority section.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-009`, `REQ-016`, `REQ-023`–`REQ-026`,
  `REQ-030`, `NFR-001`–`NFR-011`.
- Relevant files:
  `@src/pages/resources/index.astro`,
  `@src/lib/siteContent.ts`,
  `@scripts/validate_layout_language.py`,
  resources dossier/provenance.

### Constraints

- Depend on `PAGE-01`.
- Resource-page source-authority prohibition is absolute.
- Do not turn all resource destinations into identical cards; use routes,
  staged paths, rails, or matrices according to reader job.
- Do not migrate child resources.

### Implementation notes

1. Write the resource-overview page brief.
2. Use overview composition with contextual provenance and explicit limits.
3. Distinguish orientation, inspection, publication, reading, and gallery jobs.
4. Use true peer cards only where destinations are concise peer choices.
5. Verify navigation labels and route targets against `siteContent.ts`.

### Acceptance criteria

- [ ] All principal resource jobs are discoverable.
- [ ] The page is fluid and not a single bounded resource panel.
- [ ] No dedicated Source authority section is rendered.
- [ ] Internal destinations are primary.
- [ ] Dense resource choices remain usable at 320px and wide desktop.

### Validation

- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:comprehension`
- `npm run validate:provenance`
- `npm run build`
- `python3 -m pytest`
- Browser matrix and `git diff --check`

### Done when

The Resources overview is a clear, fluid directory into specialized resource
jobs without violating the repository's provenance rule.

---

## Core Packet RES-01: Prove the General Resource Template on Registries

### Goal

Create and prove the general Resource template on `/resources/registries/`,
using broad data presentation where needed and open narrative elsewhere.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-010`, `REQ-016`, `REQ-020`–`REQ-025`,
  `REQ-030`, `NFR-001`–`NFR-011`.
- Relevant files:
  `@src/pages/resources/registries/index.astro`,
  relevant content data, route map, provenance, and resource validators.

### Constraints

- Depend on `PAGE-04`; depend on `SRC-01` if registry descriptions or status
  change.
- No dedicated source-authority section.
- Registry data may be boxed/table-like; its surrounding narrative should not
  be boxed by default.

### Implementation notes

1. Implement/adopt `ResourcePageTemplate`.
2. Use `prose` for explanation and `data` for registry inventory.
3. Preserve direct source links as inspection paths and internal routes as
   primary orientation.
4. Define local overflow behavior for irreducible tables.
5. Record why each retained bordered object is a registry/data object.

### Acceptance criteria

- [ ] General resource invariants are reusable by later `RRES-*` packets.
- [ ] Registry data uses wide space without page-level overflow.
- [ ] Prose remains readable.
- [ ] No dedicated Source authority section.
- [ ] Source and status descriptions remain accurate.

### Validation

- Resource page validation profile
- 320px/400% table overflow and keyboard review
- `npm run validate:curator` against accepted clean source
- `git diff --check`

### Done when

The general Resource template is proven on a data-heavy route and documented
for reuse.

---

## Core Packet RES-02: Build the Library Template

### Goal

Migrate `/resources/library/` to a dedicated Library template that supports
fast browsing, meaningful status/type distinctions, and optional progressive
filtering without losing the complete static library.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-011`, `REQ-016`, `REQ-020`–`REQ-025`,
  `REQ-030`, `NFR-001`–`NFR-012`.
- Relevant files:
  `@src/pages/resources/library/index.astro`,
  `@src/lib/manifests.ts`,
  resource manifests and validators.

### Constraints

- Depend on `RES-01`.
- No dedicated source-authority section.
- Static HTML must remain complete and usable without JavaScript.
- Add filtering only if the inventory size and packet scope justify it.
- Do not create a client framework or remote search service.

### Implementation notes

1. Audit current library items, metadata, grouping, and reader paths.
2. Implement/adopt `LibraryPageTemplate`.
3. Separate featured/recommended orientation from complete inventory.
4. Express status, kind, source/derivative role, and primary action clearly.
5. If filtering is included, use native controls or minimal script, announce
   result count accessibly, support reset, and render a useful no-results state.
6. Use broad data/grid spans but readable item descriptions.
7. Test long titles, missing optional metadata, and zero matching results.

### Acceptance criteria

- [ ] The library is scannable on mobile and wide desktop.
- [ ] Static/no-script users see the complete inventory.
- [ ] Any controls are keyboard-operable and visibly focused.
- [ ] Empty/no-results behavior is useful.
- [ ] Format/status/source roles are not conflated.
- [ ] No dedicated Source authority section.

### Validation

- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:provenance`
- `npm run build`
- Focused control tests if script is added; `python3 -m pytest`
- No-script, keyboard, 320px, 1920px browser QA
- `git diff --check`

### Done when

The Library has a dedicated, reusable contract and works fully without a client
runtime.

---

## Core Packet RES-03: Build the Diagram Gallery Template

### Goal

Migrate `/resources/diagrams/` to a dedicated Diagram Gallery template that
uses the viewport for visual inspection while preserving manifest authority,
accessible descriptions, static fallback, and the reader-aid boundary.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-012`, `REQ-016`, `REQ-020`–`REQ-025`,
  `REQ-030`, `NFR-001`–`NFR-012`.
- Relevant files:
  `@src/pages/resources/diagrams.astro`,
  `@src/components/DiagramGalleryList.astro`,
  `@src/lib/siteContent.ts`,
  diagram manifests/assets and SVG/comprehension validators.

### Constraints

- Depend on `PAGE-04` and accepted gallery-related work already checkpointed.
- No dedicated source-authority section.
- Preserve the rule that visual SVG art is animated and has no visible
  embedded text.
- A lightbox/dialog is optional; do not expand into a complex overlay system
  without evidence.
- Static page and direct asset/page links must remain usable without script.

### Implementation notes

1. Audit gallery item count, metadata, categories, current containment, and
   image sizes.
2. Implement/adopt `DiagramGalleryPageTemplate`.
3. Give previews a media-width grid and reserve cards/frames for the diagram
   objects themselves.
4. Keep captions and explanatory labels in HTML.
5. If filters are justified, implement accessible result counts, reset, and
   no-results state.
6. If enlarged inspection is justified, prefer the simplest accessible model;
   verify focus management, Escape, return focus, and no-script alternative.
7. Preserve or improve lazy loading without blank full-page QA captures or
   layout shift.

### Acceptance criteria

- [ ] Diagrams are materially larger/easier to inspect on wide screens.
- [ ] Gallery objects remain clearly framed, while surrounding sections are not
  uniformly boxed.
- [ ] Captions/descriptions are accessible and external to SVG artwork.
- [ ] Manifest and source references are valid.
- [ ] Keyboard/no-script/reduced-motion behavior is complete.
- [ ] No dedicated Source authority section.

### Validation

- `npm run validate:manifests`
- `npm run validate:svg`
- `npm run validate:comprehension`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:provenance`
- `npm run build`
- Focused tests and `python3 -m pytest`
- Gallery-specific viewport, crop, keyboard, no-script, and reduced-motion QA
- `git diff --check`

### Done when

The gallery uses wide space for its actual visual objects, all inspection paths
are accessible, and the manifest/non-authority boundary remains explicit.

---

## Core Packet RES-04: Build the Document Library Template

### Goal

Migrate `/resources/documents/` to a dedicated document-library template that
clarifies reading order, status, TeX source authority, PDF derivative role,
metadata, and download actions.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-013`, `REQ-016`, `REQ-020`–`REQ-025`,
  `REQ-030`, `NFR-001`–`NFR-011`.
- Relevant files:
  `@src/pages/resources/documents.astro`,
  `@src/components/DocumentActions.astro`,
  `@src/lib/manifests.ts`,
  source/asset manifests.

### Constraints

- Depend on `RES-01`.
- No dedicated source-authority section.
- Do not imply PDF authority where registered TeX is authoritative.
- Preserve manifest-backed links and hashes.

### Implementation notes

1. Audit current document groups, metadata, actions, and reading sequence.
2. Implement/adopt `DocumentLibraryPageTemplate`.
3. Use narrative/prose for orientation and data/object containers for document
   records.
4. Make source versus derivative roles visible without turning provenance into
   primary navigation.
5. Ensure long filenames, metadata, and actions reflow or locally overflow.
6. Retain a no-script static experience.

### Acceptance criteria

- [ ] Document roles and status are unambiguous.
- [ ] Reading order is clear.
- [ ] Download/source actions are accessible and valid.
- [ ] Dense metadata is usable at 320px and 400% zoom.
- [ ] No dedicated Source authority section.
- [ ] Manifests and hashes remain consistent.

### Validation

- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:provenance`
- `npm run build`
- Focused tests and `python3 -m pytest`
- Mobile/wide/keyboard/no-script browser QA
- `git diff --check`

### Done when

The documents route has its own reusable page contract and preserves the
project's source/derivative distinction.

---

## Core Packet EXP-01: Prove the General Explainer on Physics Ontology

### Goal

Create and prove the general Explainer template on `/physics/ontology/`,
preserving ontology/model/evidence boundaries while opening the narrative
layout and retaining appropriate table/media containment.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-014`, `REQ-016`, `REQ-020`–`REQ-025`,
  `REQ-030`, `NFR-001`–`NFR-011`.
- Relevant files:
  `@src/pages/physics/ontology/index.astro`,
  `@src/components/ComprehensionBlocks.astro`,
  `@src/components/OverflowTable.astro`,
  `@src/components/TermCardGrid.astro`,
  ontology dossier/manifests/provenance.

### Constraints

- Depend on `PAGE-01` and `SRC-01`.
- Do not alter ontology terminology or claim status without direct source
  authority and a separately stated content need.
- Tables, term records, and diagrams may remain contained; surrounding
  explanation should use open bands.
- Do not migrate another physics child route.

### Implementation notes

1. Implement/adopt `ExplainerPageTemplate`.
2. Map context, plain summary, mechanism, terms, evidence/status, boundaries,
   related routes, provenance, and source authority into flexible slots.
3. Use `prose`, `media`, and `data` spans deliberately.
4. Review whether `TermCardGrid` contains true peer terms or should use a less
   card-like glossary presentation.
5. Preserve equation/diagram walkthrough obligations from the dossier.
6. Record safe and unsafe summary parity.

### Acceptance criteria

- [ ] The route is easier to read without flattening ontology distinctions.
- [ ] Prose, diagram, glossary, and table use appropriate width modes.
- [ ] Source authority remains visible and accurate.
- [ ] No new physical claim or derivation is implied.
- [ ] The template can support later physics/AI explainers.
- [ ] Mobile data overflow is localized and accessible.

### Validation

- Full standard page profile, including claims, comprehension, provenance,
  curator, manifests/SVG when affected, build, Python tests, and browser matrix
- Dossier safe/unsafe summary review
- `git diff --check`

### Done when

The explainer contract is proven on a high-risk scientific page and is safe for
the repeated route queue.

---

## Core Packet UTIL-01: Migrate the License Utility Page

### Goal

Apply a restrained utility/legal contract to `/license/` so it participates in
the fluid system without acquiring irrelevant claim, gallery, or overview
modules.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-015`, `REQ-016`, `REQ-025`,
  `REQ-026`, `REQ-028`, `NFR-001`–`NFR-006`, `NFR-008`–`NFR-012`.
- Relevant files:
  `@src/pages/license/index.astro`,
  `@src/layouts/BaseLayout.astro`,
  utility styles.

### Constraints

- Depend on `FOUND-01`; may follow `SHELL-01`.
- Do not change license meaning or legal text in a design packet.
- Do not add source-authority or comprehension modules without a legal/content
  requirement.

### Implementation notes

1. Implement/adopt the smallest Utility template or a documented template
   exception.
2. Use a readable measure, clear heading structure, and internal return path.
3. Preserve exact legal content.
4. Test long unbroken text/URLs and print behavior if currently supported.

### Acceptance criteria

- [ ] Legal content is unchanged.
- [ ] The route uses fluid gutters and readable measure.
- [ ] Heading and landmark semantics are correct.
- [ ] No irrelevant page-family module appears.
- [ ] Mobile/zoom behavior is usable.

### Validation

- Exact text/diff review
- `npm run validate:links`
- `npm run validate:layout`
- `npm run build`
- Focused tests and `python3 -m pytest`
- Mobile/desktop/zoom browser QA
- `git diff --check`

### Done when

The utility route is visually coherent with the system without being forced
into a content template it does not need.

---

## Core Packet LEGACY-01: Decide the `/project/*` Route Disposition

### Goal

Produce an evidence-backed decision for all 30 `/project/*` routes:
`canonical`, `specialist-only`, `redirect candidate`, or `retire candidate`,
then generate bounded follow-on packet definitions without changing routes in
this packet.

### Context

- PRD requirements: `REQ-014`, `REQ-015`, `REQ-019`, `REQ-022`, `REQ-023`,
  `REQ-028`, `REQ-029`, `NFR-001`, `NFR-008`–`NFR-012`.
- Relevant files:
  `@src/pages/project/`,
  `@src/components/InternalExplainerPage.astro`,
  `@src/lib/internalExplainers.ts`,
  dossiers, internal links, smoke tests, route maps, provenance, existing
  redirects, and architecture plans.

### Constraints

- Depend on `ARCH-01`, `EXP-01`, and `SRC-01`.
- Planning/disposition only; no route deletion, redirect, or page migration.
- Absence from navigation or route map is not sufficient evidence to delete.
- Preserve unique specialist content and incoming internal links.
- Owner decision is required before irreversible route retirement.

### Implementation notes

For each route:

1. Compare reader job and unique content with modern `/physics/*`,
   `/ai-research-system/*`, and `/resources/*` routes.
2. Inspect source dossier, current component/data ownership, inbound internal
   links, manifest/provenance status, and search/smoke expectations.
3. Record the recommended canonical target if redirecting.
4. Identify whether a retained page uses Overview, Explainer, Resource, or a
   justified specialist variant.
5. Define one follow-on packet per retained migration or redirect group that is
   still small enough for independent review.
6. Require redirect status/location, internal-link replacement, route-map,
   provenance, smoke, and rollback checks for retirement.

### Acceptance criteria

- [ ] All 30 routes have one disposition and evidence.
- [ ] Unique content and inbound links are recorded.
- [ ] Every redirect candidate has one canonical target and parity rationale.
- [ ] Every retained route has a template and source gate.
- [ ] Ambiguous routes remain blocked rather than guessed.
- [ ] Follow-on packets and owner-decision points are explicit.
- [ ] No route changes in this packet.

### Validation

- Filesystem route count and ledger comparison
- Internal-link search
- Route-map/provenance comparison
- `git diff --check`
- Focused ledger tests if added
- `python3 -m pytest` when tests/scripts change
- `npm run validate:implementation-control`

### Done when

The legacy subtree has a complete decision record and safe follow-on queue,
with no deletion or redirect performed prematurely.

---

## Core Packet CLEAN-01: Remove Legacy Width Language and Enforce Contracts

### Goal

After all accepted route migrations and legacy decisions, remove proven-dead
layouts, compatibility aliases, fixed outer-width selectors, and obsolete
component code; strengthen validators so the old global boxed-page pattern
cannot silently return.

### Context

- PRD requirements: `REQ-001`–`REQ-007`, `REQ-019`, `REQ-024`, `REQ-028`,
  `REQ-029`, `NFR-001`–`NFR-011`.
- Relevant files:
  `@src/styles/global.css`,
  `@src/layouts/`,
  `@src/components/`,
  `@scripts/validate_layout_language.py`,
  tests and route ledger.

### Constraints

- Depend on all governed modern route packets and the accepted output of
  `LEGACY-01`.
- Delete only with zero-consumer proof.
- Keep legitimate max widths for prose, controls, dialogs, and intrinsic media.
- Do not combine legacy route retirement here; those use their own follow-on
  packets.

### Implementation notes

1. Search for consumers of every candidate layout/component/class/token.
2. Compare route ledger migration states with the filesystem.
3. Remove compatibility aliases in the smallest coherent groups.
4. Remove dead `LandingLayout`, `TechnicalPageLayout`, `DownloadList`, or other
   candidates only if consumer and dynamic-reference checks are clean.
5. Update `validate_layout_language.py` to reject newly introduced global
   fixed-width page shells while allowing semantic prose/media limits.
6. Add focused positive/negative tests.
7. Run the entire static route suite and representative visual matrix.

### Acceptance criteria

- [ ] Every deletion has recorded zero-consumer evidence.
- [ ] No active general page shell uses `1120px`/`1180px` as its universal
  outer ceiling.
- [ ] Legitimate readable/object constraints remain.
- [ ] Validator messages distinguish forbidden outer shells from valid local
  widths.
- [ ] All current routes build and render.
- [ ] Rollback can restore each cleanup group without reverting route content.

### Validation

- `rg` consumer audit recorded in the handoff
- Focused layout-validator tests
- `npm run validate:layout`
- `npm run validate`
- `python3 -m pytest`
- Representative browser matrix
- `git diff --check`

### Done when

The compatibility layer is gone only where proven unnecessary and the
repository actively guards the new layout contract.

---

## Core Packet QA-01: Run Sitewide Release-Readiness Review

### Goal

Verify the complete accepted page system across all retained routes, source and
manifest authority, accessibility profiles, performance, smoke tests, and
human-review records, then report release readiness without pushing or
deploying.

### Context

- PRD requirements: all `REQ-*` and `NFR-*`.
- Relevant files: all changed runtime files, route-family ledger, manifests,
  provenance, curator reports, quality receipts, implementation-control
  records, and final build output.

### Constraints

- Depend on `CLEAN-01`, all accepted modern route packets, and any legacy
  follow-ons required for the chosen release.
- No new feature or visual repair unless a separate bounded packet is opened.
- Do not bypass a failing curator, provenance, accessibility, smoke, or quality
  gate.
- No push or deployment.

### Implementation notes

1. Recompute route inventory and compare with the ledger.
2. Confirm every released route has source/template/migration/human-review
   status.
3. Regenerate only required manifests/provenance against the accepted clean
   source root.
4. Run full validation and quality.
5. Start an Astro preview and smoke all routes.
6. Run the representative page-family browser matrix at 320, 390, 768, 1280,
   1536, and 1920 widths; test 200%/400% zoom, keyboard, short landscape,
   reduced motion, no-script where interactions exist, and local table
   overflow.
7. Compare performance with the pre-foundation baseline using the exact
   `frontend_performance_baseline.py` CLI.
8. Record remaining human-review items and release blockers.

### Acceptance criteria

- [ ] Route ledger count equals the retained static route surface.
- [ ] No unresolved critical source drift for released routes.
- [ ] Manifests/provenance/hashes are coherent.
- [ ] `npm run validate` passes.
- [ ] `npm run quality` passes.
- [ ] Python tests and route smoke tests pass.
- [ ] Browser matrix shows no page-level horizontal overflow and no broken
  interaction.
- [ ] Performance has no unexplained material regression.
- [ ] Human acceptance and technical completion are reported separately.
- [ ] No push or deployment occurs.

### Validation

```text
git diff --check
npm run validate
npm run quality
python3 -m pytest
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:<port> --root .
python3 scripts/frontend_performance_baseline.py --input-dir <accepted-input> --dist-root dist --json-output <path> --markdown-output <path>
```

Also inspect Git status/diff statistics, browser console output, screenshots,
route ledger, curator report, and review ledger.

### Done when

A reproducible release-readiness report says either `ready for owner
acceptance` or names the exact blockers. The packet stops before Git
publication or deployment.

---

# Repeatable Governed Route-Migration Packet Contract

Each `RPHY-*`, `RAI-*`, and `RRES-*` record below is an independent task packet
and inherits this complete contract plus its route-specific record.

## Goal

Migrate exactly the named route to its accepted page-family template and fluid
width system while preserving its reader job, reviewed copy, claim boundary,
internal links, visual/assets, and source/provenance contract.

## Context

- PRD requirements:
  `REQ-001`–`REQ-007`, the applicable family requirement from `REQ-010` or
  `REQ-014`, `REQ-016`, `REQ-019`–`REQ-025`, `REQ-028`, `REQ-030`,
  `NFR-001`–`NFR-012`.
- Relevant route, dossier, data/component, and special acceptance notes are in
  the instance table.
- Existing patterns:
  accepted `PAGE-01`, `RES-01`, or `EXP-01` implementation and the live
  `web-page` skill.

## Constraints

- One route only.
- Depend on `GATE-00`, `FOUND-01`, `SKILL-01`, `SKILL-02`, `ARCH-01`, and the
  named family pilot.
- Claim-sensitive instances also depend on `SRC-01`.
- Preserve copy by default; if source freshness requires copy changes, record
  and validate them explicitly in this same one-route packet only when live
  scope permits.
- Do not migrate sibling routes or delete shared compatibility styles.
- Resource instances may not render a dedicated Source authority section.

## Implementation notes

1. Invoke `web-page` and read the correct guidance template.
2. Resolve live control and accepted clean source binding.
3. Inspect the route, dossier/source bundle, provenance, current components,
   and before-state at all representative widths.
4. Write a page implementation brief:
   reader job, hierarchy, width modes, containment decisions, source risk,
   behavior to preserve, and smallest change boundary.
5. Use the accepted page-template component and existing content data.
6. Unbox continuous narrative; retain frames for actual media, data, code,
   downloads, controls, or modular records.
7. Avoid route-specific pixel widths when a semantic mode exists.
8. Regenerate route provenance/manifests only when inputs require it.
9. Run narrow validation first, then the full route profile.
10. Create a QA receipt and stop at the live handoff boundary.

## Acceptance criteria

- [ ] Exactly one route is migrated.
- [ ] Route-specific acceptance notes are satisfied.
- [ ] The outer section/grid is fluid and the prose measure remains readable.
- [ ] Every retained four-sided container has a recorded semantic reason.
- [ ] No page-level overflow at 320px or equivalent 400% zoom.
- [ ] Keyboard/focus/reduced-motion behavior is preserved.
- [ ] Copy, claim, and source status remain reviewed and accurate.
- [ ] Internal routes remain primary.
- [ ] Relevant manifests/provenance are coherent.
- [ ] A page brief, validation summary, browser artifacts, and review receipt
  exist.

## Validation

Run the relevant subset, recording every result:

```text
git diff --check
npm run validate:content
npm run validate:claims
npm run validate:links
npm run validate:layout
npm run validate:svg
npm run validate:comprehension
npm run validate:provenance
npm run validate:curator
npm run validate:implementation-control
npm run build
python3 -m pytest
```

Add `npm run validate:manifests` when assets/manifests change. Browser QA must
include 320, 768, 1280, and 1920 CSS-pixel widths plus keyboard, 200%/400% zoom,
and reduced motion where animated visuals exist.

## Done when

The named route satisfies the template and source contracts, all required
checks pass or an exact pre-existing blocker is reported, the QA receipt is
complete, and no adjacent route, checkpoint, push, or deployment has been
performed.

## Instantiated Physics Route Packets

| Packet | Route and source context | Template/pilot dependency | Behavior that must remain | Route-specific acceptance |
| --- | --- | --- | --- | --- |
| `RPHY-01` | `/physics/claim-status/`; route file, claim-status dossier/snapshot, claim-boundary registry, provenance. | Explainer/status; `EXP-01`; hard dependency on `SRC-01` critical-drift resolution. | Adopted benchmark, remaining burdens, claim qualification, updated/source status. | Critical curator item is resolved; status/data use `data` width; no implication of a verified new gravity law. |
| `RPHY-02` | `/physics/derivation-roadmap/`; roadmap dossier, diagram, provenance. | Explainer; `EXP-01`. | Open derivation burdens, staged roadmap, non-proof boundary. | Roadmap sequence is visually clear; continuous explanation is open; diagram remains a framed reader aid. |
| `RPHY-03` | `/physics/exact-gr-benchmark/`; benchmark dossier, equations/diagram, provenance. | Explainer; `EXP-01`. | Exact effective package status and distinction from microscopic derivation. | Equations retain walkthrough/assumptions; benchmark data can use wide spans; no derivation overclaim. |
| `RPHY-04` | `/physics/flow-geometry/`; flow-geometry dossier/assets/provenance. | Explainer; `EXP-01`. | Ontology-to-geometry explanatory boundary and visual. | Media is materially wider; terminology and captions remain accessible; no visible SVG text. |
| `RPHY-05` | `/physics/open-burdens/`; burden/status dossier and provenance. | Explainer/status; `EXP-01`. | Remaining open work, negative results, and status qualifications. | Dense burdens scan well without a wall of cards; unresolved items are not visually promoted as completed results. |

## Instantiated AI Research System Route Packets

| Packet | Route and source context | Template/pilot dependency | Behavior that must remain | Route-specific acceptance |
| --- | --- | --- | --- | --- |
| `RAI-01` | `/ai-research-system/agentjob-lifecycle/`; lifecycle dossier/diagram/provenance. | Explainer; `EXP-01` and `PAGE-03`. | One bounded AgentJob, completion, handoff, and authority chain. | Lifecycle order is clear; agent behavior is not anthropomorphized; diagram remains accessible. |
| `RAI-02` | `/ai-research-system/current-state/`; current-state source bundle/provenance. | Explainer/status; `PAGE-03`; `SRC-01`. | Snapshot date, implemented versus planned state, and limits. | Snapshot-sensitive content is fresh or explicitly dated; status uses broad data layout without overstating runtime completion. |
| `RAI-03` | `/ai-research-system/human-gated-promotion/`; human-gate dossier/provenance. | Explainer; `PAGE-03`. | Human authority, gate decisions, and non-autonomous promotion. | Human decision points are more prominent than decorative system flow. |
| `RAI-04` | `/ai-research-system/memory-preflight/`; memory dossier/diagram/provenance. | Explainer; `PAGE-03`. | Source-first memory preflight and non-authority of summaries. | Layer relationships use media/data spans; memory is not presented as canonical source. |
| `RAI-05` | `/ai-research-system/project-system-improvement/`; improvement-loop dossier/provenance. | Explainer; `PAGE-03`. | Governed improvement loop, review, and stopping boundaries. | Cyclic process is understandable without repeated boxed steps; status remains bounded. |
| `RAI-06` | `/ai-research-system/roles-and-schemas/`; roles/schema sources/provenance. | Explainer/data; `PAGE-03`. | Role authority and schema distinctions. | Dense role/schema comparison uses `data` width and local overflow; prose remains narrow. |
| `RAI-07` | `/ai-research-system/runtime-requirements/`; technical requirements dossier/provenance. | Explainer/data; `PAGE-03`. | Runtime prerequisites versus aspirational architecture. | Requirements are scannable and status-qualified; no plan is presented as implemented runtime. |
| `RAI-08` | `/ai-research-system/validators-and-handoffs/`; validator/handoff sources/provenance. | Explainer/process; `PAGE-03`. | Validator pass boundary, evidence, and handoff role. | Process order and failure boundary are visible; cards used only for discrete records. |
| `RAI-09` | `/ai-research-system/workflow/`; workflow dossier/diagram/provenance. | Explainer/process; `PAGE-03`. | Governed workflow, one bounded packet, checks, and stop conditions. | Sequence is clear across widths; sources remain inspection paths; no implied autonomous authority. |

## Instantiated General Resource Route Packets

| Packet | Route and source context | Template/pilot dependency | Behavior that must remain | Route-specific acceptance |
| --- | --- | --- | --- | --- |
| `RRES-01` | `/resources/generated-derivatives/`; derivative records/manifests/provenance. | General Resource; `RES-01`. | Distinction between generated derivative and source authority. | Asset records use object/data containers; surrounding explanation stays open; no dedicated authority section. |
| `RRES-02` | `/resources/guided-starts/`; guided-start data/provenance. | General Resource/path variant; `RES-01`. | Audience route choices and internal-first navigation. | Paths read as staged journeys, not a generic card wall; no dedicated authority section. |
| `RRES-03` | `/resources/guided-starts/general-public/`; public-start dossier/provenance. | General Resource/path variant; `RES-01`. | General-public reading sequence and plain-language orientation. | Sequence remains obvious at mobile and wide widths; source links do not displace internal steps. |
| `RRES-04` | `/resources/publication-process/`; publication dossier/diagram/provenance. | General Resource/process variant; `RES-01`. | Source-to-review-to-publication boundary. | Process uses an open sequence plus framed diagram; no site copy becomes source authority. |
| `RRES-05` | `/resources/reading-paths/`; path data/provenance. | General Resource/path variant; `RES-01`. | Audience-specific routes and order. | Multiple paths are distinguishable without identical nested boxes; keyboard link order is logical. |
| `RRES-06` | `/resources/repository-map/`; repository-map sources/provenance. | General Resource/data variant; `RES-01`. | Repository areas and authority roles. | Map/table uses `data` width with local overflow; no misleading claim that file location alone grants authority. |
| `RRES-07` | `/resources/retrieval-layers/`; retrieval sources/provenance. | General Resource/explainer variant; `RES-01`. | Canonical versus derivative retrieval layers. | Layer visualization is wide and accessible; hierarchy is not flattened into peer cards. |
| `RRES-08` | `/resources/reviewer-packet/`; reviewer dossier/downloads/provenance. | General Resource/reviewer variant; `RES-01`. | Reviewer order, evidence, downloads, and limits. | Actions and records are discrete objects; instructions remain readable; no dedicated authority section. |
| `RRES-09` | `/resources/site-builder-guide/`; source-bundle and builder guidance/provenance. | General Resource/guide variant; `RES-01`. | Page-family, source-bundle, freshness, validation, and handoff sequence. | Builder steps are clear without asserting this page is implementation authority; code/data blocks overflow locally. |
| `RRES-10` | `/resources/source-authority/`; source-authority dossier/provenance. | General Resource/explainer variant; `RES-01`; `SRC-01`. | Explanation of authority hierarchy and inspection paths. | It explains source authority contextually but does not render the forbidden dedicated Source authority component/section. |

## Route-Packet Ordering

After the pilots:

1. `RPHY-01` first because upstream drift marks it critical.
2. `RPHY-02`–`RPHY-05` in any dependency-safe order, one at a time.
3. `RAI-02` before other snapshot-sensitive AI routes; the remaining AI packets
   may follow reader-journey order.
4. `RRES-01` and `RRES-10` early because they establish derivative/authority
   boundaries; remaining resource packets may follow navigation order.
5. Do not run packets concurrently if they share `global.css`, the same
   template component, manifests, provenance, or implementation-control
   records. Apparent route independence does not override the one-packet
   default.

## Per-Packet Review Prompt

After any implementation packet, use this follow-up review prompt:

> Review the current packet diff against its requirement IDs, route brief,
> accepted source binding, template invariants, containment audit, accessibility
> matrix, validation output, and rollback boundary. Identify unrelated changes,
> silent claim strengthening, fixed-width regressions, unjustified boxes,
> missing browser evidence, or incomplete control records. Do not modify files
> unless a separate repair packet is authorized.
