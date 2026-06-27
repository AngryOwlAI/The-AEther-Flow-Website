# Site-Wide Formidable Command-Interface Redesign Implementation Plan

Date: 2026-06-27

## Source PRD

- Source: `PRDs/site-wide-formidable-command-interface-redesign-prd.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions
- Output companion: `ImplementationPlans/site_wide_formidable_command_interface_redesign_task_packets.md`

## Product Summary

The PRD calls for a phased, site-wide visual-language redesign. The goal is to
move the AEther Flow Website away from repeated bordered card grids and toward a
formidable, precise research-command interface while preserving the existing
Angry Owl cyan, orange, and graphite schema.

The redesign is presentation and UX work. It must not rewrite, strengthen, or
invent scientific, mathematical, governance, workflow, claim-status, route-map,
or source-authority claims. Phase 1 must define shared layout primitives and
apply them to `/project/overview/` as the proof. Later phases migrate shared
route-family structures before route-specific tuning.

## Repository Context

- Frameworks and languages: Astro 7 static output, Astro components, MDX, CSS,
  TypeScript data modules, Python validation scripts, Playwright dev dependency.
- Package manager and build system: npm with `package-lock.json`; Node engine is
  `22.x`; Astro builds static HTML into `dist/`.
- Current related routes: `src/pages/project/overview.astro`,
  `src/pages/project/physics/**`, `src/pages/project/ai-research-agent-system/**`,
  `src/pages/project/operations/**`, `src/pages/project/source-authority/**`,
  `src/pages/resources/**`.
- Current related components: `BaseLayout.astro`, `InternalExplainerPage.astro`,
  `ProjectRouteGrid.astro`, `SourceNotice.astro`, `DocumentActions.astro`,
  `DownloadList.astro`, `Figure.astro`.
- Current related data modules: `src/lib/siteContent.ts`,
  `src/lib/internalExplainers.ts`, `src/lib/manifests.ts`,
  `src/data/physics_current_state_snapshot.json`.
- Current visual surface: `src/styles/global.css` contains dark overview tokens,
  animated SVG styles, repeated grid/card primitives, reduced-motion handling,
  and route-family classes.
- Relevant manifests: `public/files/manifests/page_route_map.json`,
  `public/files/manifests/page_provenance.json`,
  `public/files/manifests/source_manifest.json`,
  `public/files/manifests/asset_manifest.json`.
- Existing validation commands discovered from `package.json`:
  - `npm run build`
  - `npm run validate`
  - `npm run quality`
  - `npm run validate:manifests`
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:svg`
  - `npm run validate:provenance`
  - `npm run validate:curator`
  - `npm run validate:cloudflare`
  - `python3 -m pytest`
- Existing utility commands:
  - `python3 scripts/generate_page_provenance.py --write`
  - `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`
  - `python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict`

## Relevant Repository Instructions

- The website is a reader-facing presentation layer for
  `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
- Upstream source files, registries, and governed task records remain
  authoritative.
- Website pages may explain, organize, promote, and link reviewed material, but
  must not silently strengthen or create source claims.
- GitHub links remain available as provenance; primary reader journeys should
  prefer internal routes.
- Registered TeX sources carry ontology document authority; PDFs are generated
  human-readable derivatives.
- Visual SVG figures must be animated and must not contain visible embedded text.
  Labels belong in HTML, ARIA labels, `<title>`, or `<desc>`.
- Definition of done includes static Astro build, relevant public manifest
  updates, regenerated page and asset hashes after file changes, `npm run
  validate` or named skipped checks, internal-first route cards, and SVG policy
  validation.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | Planning artifacts belong in `ImplementationPlans/` rather than `docs/implementation-plans/`. | The repository already stores PRD-derived plans and task packets in `ImplementationPlans/`. | Committing the plan |
| ASM-002 | Planning assumption | Phase 1 should work directly on `/project/overview/` after capturing baseline screenshots, not through a separate prototype route. | The PRD names `/project/overview/` as the flagship proof and requires comparison evidence. | Beginning Phase 1 coding |
| ASM-003 | Planning assumption | The layout-language audit should start as both a manual QA checklist and a small validator script once primitives exist. | The PRD asks to ban anti-patterns and make future drift reproducible. | Phase 4 hardening |
| ASM-004 | Planning assumption | No new production animation dependency should be introduced. | The PRD explicitly excludes new production animation dependencies; existing CSS/SVG animation is sufficient. | Any SVG or animation refactor |
| ASM-005 | Planning assumption | Existing text content and claim boundaries should be preserved unless a UI label must change to support the new structure. | The PRD scopes Phase 1 to presentation and forbids strengthened source claims. | Each route migration |
| ASM-006 | Implementation detail | Side-by-side screenshots can be local ignored artifacts under `output/playwright/`, with a tracked summary in `docs/quality/`. | `output/playwright/` is gitignored; `docs/quality/` already contains QA summaries. | Final Phase 1 review |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Planning assumption | Should the user-facing site include an explicit motion pause control in later phases, beyond `prefers-reduced-motion`? | Phase 1 can proceed with reduced-motion support; later route-wide motion prominence may require a control for stronger accessibility posture. |
| Q-002 | Implementation detail | Should the anti-pattern audit reject specific class names, measured page structure, or only manual review findings? | Does not block Phase 1; affects Phase 4 enforcement strength. |

No blocking questions prevent a credible implementation plan.

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| REQ-001: Formidable first impression | The site feels distinctive, precise, and less generic on first load. | `overview.astro`, shared command primitives, global CSS, screenshots | TASK-01, TASK-02, TASK-03, TASK-04 | Playwright desktop/mobile screenshots, `npm run build`, browser QA |
| REQ-002: Clear hierarchy | Readers can distinguish primary concepts, supporting evidence, and metadata. | Command bands, evidence rails, status dossiers | TASK-02, TASK-03, TASK-05, TASK-06 | Layout QA, no text overlap, screenshot review |
| REQ-003: Physics claim seriousness | Physics boundaries read as controlled claim states, not celebratory proof. | Physics landing/detail pages, current-state page, `SourceNotice` placement | TASK-05, TASK-06, TASK-07 | `npm run validate:content`, provenance review |
| REQ-004: AI workflow as command system | AI workflow pages communicate roles, validators, memory, and handoffs as operational control. | AI route family, `InternalExplainerPage.astro`, workflow rails | TASK-05, TASK-07 | Browser QA, `npm run validate` |
| REQ-005: Trust and provenance visible | Provenance is inspectable but not the dominant page rhythm. | `SourceNotice.astro`, status dossiers, provenance zones | TASK-02, TASK-03, TASK-05, TASK-06 | `npm run validate:links`, `npm run validate:provenance` |
| REQ-006: Routes as journeys or rails | Route lists show sequence, dependency, or reader progression instead of generic cards. | `ProjectRouteGrid.astro`, overview journey sections, route-family pages | TASK-02, TASK-03, TASK-05 | Internal-first link validation, browser QA |
| REQ-007: Current state as dossier | Returning readers see dense state metadata as scannable status dossiers. | `physics/current-state/index.astro`, dossier primitive | TASK-06, TASK-07 | `npm run build`, responsive screenshots |
| REQ-008: Document usability | PDF and TeX download surfaces remain clear and usable. | `resources/documents.astro`, `DocumentActions.astro` | TASK-06 | Browser QA, `npm run validate:manifests` |
| REQ-009: Mobile collapse | Headings, actions, rails, SVGs, and dossiers do not overlap on mobile. | Responsive CSS for primitives and migrated pages | TASK-03, TASK-04, TASK-05, TASK-06, TASK-07 | Mobile Playwright screenshots, manual overlap QA |
| REQ-010: Reduced motion | Animations respect motion-sensitive user settings. | CSS `prefers-reduced-motion`, SVG animation classes, QA script/checklist | TASK-02, TASK-04, TASK-08 | Reduced-motion browser QA, `npm run validate:svg` |
| REQ-011: Color schema locked | Cyan/orange/dark graphite schema remains intact. | CSS tokens in `global.css`; no palette rewrite | TASK-02 through TASK-08 | CSS review, screenshot review |
| REQ-012: SVG identity preserved | Existing animated SVG identity is elevated as structural scene/rail layers. | Overview SVG, route-family SVGs, primitive scene surfaces | TASK-02, TASK-03, TASK-05, TASK-07 | `npm run validate:svg`, screenshots |
| REQ-013: Generic card patterns banned | Equal-height repeated card grids stop being the default structural grammar. | Shared primitives, audit checklist/script, CSS refactor | TASK-02, TASK-03, TASK-05, TASK-08 | Layout-language audit |
| REQ-014: Shared primitives first | Command bands, evidence rails, and status dossiers exist before broad migration. | New/revised components and CSS utilities | TASK-02 | Component review, build |
| REQ-015: Phase validation | Each phase has repository gates and browser evidence. | Task-level validation, docs/quality summaries | TASK-04, TASK-08 | `npm run validate`, screenshots, QA summary |
| REQ-016: Phase 1 presentation-only | Phase 1 does not alter scientific or governance claims. | `overview.astro`, provenance regeneration | TASK-03, TASK-04 | Diff review, `npm run validate:content` |
| REQ-017: Visual comparison evidence | Old and new overview states can be compared side by side. | `output/playwright/`, `docs/quality/` | TASK-01, TASK-04 | Baseline/new screenshots and tracked summary |
| REQ-018: Contributor reproducibility | Anti-patterns and acceptance criteria remain visible to future implementers. | `docs/quality/`, optional validator, task checklists | TASK-08 | Audit script/tests, final checklist |
| NFR-001: Static Astro compatibility | Affected routes build as static Astro pages. | Route files, components, CSS | TASK-02 through TASK-08 | `npm run build` |
| NFR-002: Source-authority preservation | Website redesign cannot become source authority. | All content-bearing page migrations | TASK-03, TASK-05, TASK-06, TASK-07 | `npm run validate:content`, source notice review |
| NFR-003: Manifest and provenance integrity | Page hashes are regenerated after source edits. | `page_provenance.json`, provenance generator | TASK-03, TASK-05, TASK-06, TASK-07 | `python3 scripts/generate_page_provenance.py --write`, `npm run validate:provenance` |
| NFR-004: No unnecessary dependencies | The redesign uses Astro, CSS, SVG, and existing Playwright tooling. | `package.json` should not gain production animation libraries. | TASK-02 through TASK-08 | Dependency diff review |
| NFR-005: Accessibility and SVG policy | SVGs remain animated, accessible, textless, and reduced-motion safe. | SVG markup, CSS, validators | TASK-02, TASK-03, TASK-05, TASK-07, TASK-08 | `npm run validate:svg`, browser QA |

## Proposed Technical Approach

### Architecture

Use the existing Astro static architecture. Add or refine a small set of shared
presentation primitives instead of rewriting page content:

1. `CommandBand`: a full-width or constrained narrative section with strong
   hierarchy, optional structural scene slot, and explicit heading hierarchy.
2. `EvidenceRail`: a horizontal desktop and vertical mobile sequence for reader
   journeys, source flows, claim gates, workflow steps, or route progression.
3. `StatusDossier`: a dense metadata/status panel for source authority, current
   state, document metadata, download status, or claim-state information.

The primitive implementation can be Astro components, CSS classes, or both. The
preferred route is thin Astro components plus shared CSS because later route
families already repeat the same grid/card structures. Components should be
slot-based and content-agnostic; they must not encode scientific claims.

### UI And Routing

- Phase 1 targets `/project/overview/`.
- Preserve all current internal route destinations and source-authority
  boundaries.
- Replace overview `track-grid`, `link-grid`, and `live-state` card rhythm with
  rails, command bands, and dossiers.
- Keep `/resources/diagrams/` framed because the PRD identifies diagram
  inspection as an exception.
- Keep document/download actions explicit; visual drama must not obscure PDF or
  TeX actions.

### CSS And Motion

- Preserve existing color tokens in `src/styles/global.css`.
- Introduce reusable command-interface classes near the existing
  `project-overview-page` styles.
- Keep border radii at 8px or less unless preserving existing style.
- Ensure mobile collapse uses explicit grid constraints and stable dimensions.
- Keep SVG labels out of visible SVG text; use HTML, ARIA, `<title>`, and
  `<desc>`.
- Preserve `prefers-reduced-motion: reduce` and extend coverage for new
  animation hooks.

### Data, API, Schema, And State

- No backend, API, database, runtime service, or migration is needed.
- Data impact is limited to optional route metadata shape changes in
  `siteContent.ts` or `internalExplainers.ts` if rails need explicit labels,
  sequence numbers, status fields, or grouping.
- Manifest impact is page-provenance regeneration after source edits. Asset
  manifests change only if governed public assets change, which this PRD does
  not require.

### Error Handling And Empty States

- Static routes have no loading state.
- Component-level empty states should be conservative: do not render empty rails
  or dossiers; fail obvious during build if required props are missing.
- If an implementation introduces optional arrays, default to empty arrays only
  when the route can still communicate its boundary clearly.

### Security, Privacy, And Reliability

- No user data, authentication, permissions, or rate limits are introduced.
- Continue avoiding private absolute path leakage in public manifests.
- Preserve static hosting reliability by avoiding client-side dependencies.
- Treat browser QA artifacts under `output/playwright/` as local evidence unless
  summarized in tracked documentation.

### Observability

- No runtime telemetry is required.
- Phase evidence should be recorded through:
  - validation command summaries,
  - Playwright screenshots,
  - reduced-motion notes,
  - `docs/quality/` QA summaries,
  - provenance validator results.

## Implementation Phases

1. Phase 0: Baseline evidence and audit setup. Capture current overview
   screenshots and record the existing card-grid baseline before code changes.
   Risk is low; it creates evidence for later comparison.
2. Phase 1A: Primitive foundation. Add reusable command band, evidence rail, and
   status dossier primitives using Astro/CSS with no new production dependency.
   Risk is moderate because CSS can affect multiple pages if selectors are too
   broad.
3. Phase 1B: Overview proof. Apply the primitives to `/project/overview/`,
   preserve copy/claims, regenerate page provenance, and capture new screenshots.
   Risk is moderate because this route is the flagship entry point.
4. Phase 1C: Overview validation and comparison. Run repo gates, browser QA,
   reduced-motion QA, and produce side-by-side evidence. Risk is low but review
   quality matters because "formidable" is partly visual judgment.
5. Phase 2: Shared template migration. Refactor shared route-family templates
   and grid components before hand-tuning individual pages. Risk is moderate
   because shared components affect many routes.
6. Phase 3: Route-family refinement. Tune physics, AI-system, operations,
   resources, and current-state pages with route-specific command-interface
   structures. Risk is higher because source-boundary language must remain exact.
7. Phase 4: Visual QA and hardening. Add or finalize layout-language audit,
   verify major route families across viewport sizes, and document residual
   exceptions. Risk is low to moderate depending on validator strictness.

## Codex Task Packets

Task packets are in
`ImplementationPlans/site_wide_formidable_command_interface_redesign_task_packets.md`.

Recommended order:

1. TASK-01: Capture baseline and define Phase 1 evidence surface.
2. TASK-02: Add command-interface primitives.
3. TASK-03: Redesign `/project/overview/` as the Phase 1 proof.
4. TASK-04: Validate overview proof and create comparison evidence.
5. TASK-05: Migrate shared route-family templates.
6. TASK-06: Convert document and current-state surfaces to dossiers.
7. TASK-07: Refine route families.
8. TASK-08: Add layout-language audit and final hardening.

Parallelization:

- TASK-01 must precede TASK-03.
- TASK-02 must precede TASK-03, TASK-05, TASK-06, and TASK-07.
- TASK-04 depends on TASK-03.
- TASK-05 and TASK-06 can run after TASK-02 and can be parallel if they avoid
  the same CSS/component files.
- TASK-07 depends on TASK-05 and TASK-06.
- TASK-08 should close the sequence.

## Validation Plan

- Static checks:
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:svg`
  - `npm run validate:provenance`
- Unit and script tests:
  - `python3 -m pytest`
- Build:
  - `npm run build`
- Full repository gate:
  - `npm run validate`
- Quality gate when closing a phase:
  - `npm run quality`
- Provenance regeneration after page-source edits:
  - `python3 scripts/generate_page_provenance.py --write`
- Frontend audit after build:
  - `python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict`
- Smoke test with a local dev or preview server:
  - `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`
- Browser QA:
  - Desktop and mobile screenshots for `/project/overview/` in Phase 1.
  - Desktop, tablet, and mobile screenshots for representative route families in
    later phases.
  - Reduced-motion check for pages with continuous SVG/CSS animation.
  - Manual checks for no text overlap, no CTA overlap, no SVG obstruction, and
    working navigation menus.

## Rollout And Rollback Plan

- Rollout: implement in phases, with Phase 1 limited to primitives plus
  `/project/overview/` proof.
- Migration/backfill: regenerate `page_provenance.json` after every changed page
  source; update asset manifests only if governed public assets change.
- Feature flag: not needed for static phased implementation. Review boundaries
  are branch/PR boundaries.
- Rollback: revert the phase branch or PR. Keep primitive changes separate from
  route-family migrations so overview proof can be reverted without disturbing
  later content.
- Deployment: out of scope unless explicitly authorized. Current production
  workflow should be treated as Cloudflare Pages direct upload after a pushed
  commit, not assumed dashboard Git automation.

## Risks

- Visual overcorrection: a cinematic interface could become theatrical and
  weaken scientific restraint. Mitigation: keep claim-boundary copy, source
  notices, and dense dossiers visible.
- CSS blast radius: editing `global.css` can affect unrelated route families.
  Mitigation: use namespaced command-interface classes and review screenshots.
- Source-claim drift: UI label changes can subtly strengthen claims. Mitigation:
  keep source wording unchanged unless the label is purely structural, then run
  content validation and review diffs.
- Audit brittleness: a validator that counts class names may fail legitimate
  inspection surfaces. Mitigation: start warning/manual, then enforce only
  carefully scoped anti-patterns.
- Motion accessibility: elevating SVG scene layers increases motion exposure.
  Mitigation: extend reduced-motion coverage and consider a pause control in a
  later phase.

## Out Of Scope

- Reopening the color schema.
- Replacing the Angry Owl brand mark.
- Removing SVG animations.
- Adding new production animation dependencies.
- Rewriting scientific, mathematical, governance, workflow, source-authority, or
  claim-status claims.
- Changing the upstream source-authority model.
- Changing route-map semantics except when required by already approved route
  work.
- Building a backend, live dashboard, simulation, proof checker, or AI runtime.
- Redesigning `/resources/diagrams/` as an unframed cinematic scene.
- Automatic deployment.

## Final Review Checklist

- [x] Every PRD requirement is mapped to at least one task or explicitly
  deferred.
- [x] Functional and non-functional requirements are represented.
- [x] Explicit exclusions and constraints are preserved.
- [x] Open questions are classified by impact.
- [x] Repository architecture was inspected before planning.
- [x] Existing patterns are preferred over new dependencies.
- [x] Likely affected files and directories are named.
- [x] Data, UI, accessibility, error handling, security, reliability,
  observability, rollout, and rollback are covered where relevant.
- [x] Task packets are self-contained and validation-oriented.
- [x] Source-authority boundary is preserved.

## Evidence Cited

The AEther Flow Website. (2026). `AGENTS.md` [repository operating rules and
definition of done].

The AEther Flow Website. (2026).
`PRDs/site-wide-formidable-command-interface-redesign-prd.md`
[source product requirements document].

The AEther Flow Website. (2026). `package.json` [project scripts,
dependencies, and validation commands].

The AEther Flow Website. (2026). `src/pages/project/overview.astro` [current
overview implementation].

The AEther Flow Website. (2026). `src/styles/global.css` [current visual
tokens, layout primitives, SVG animation styles, and responsive rules].

The AEther Flow Website. (2026). `src/components/InternalExplainerPage.astro`
[shared internal explainer route renderer].

The AEther Flow Website. (2026). `src/components/ProjectRouteGrid.astro`
[current route-grid component].

The AEther Flow Website. (2026). `src/components/DocumentActions.astro`
[current ontology document action component].

The AEther Flow Website. (2026). `scripts/generate_page_provenance.py` and
`scripts/validate_page_provenance.py` [page provenance generation and
validation].

The AEther Flow Website. (2026).
`ImplementationPlans/internal_explainer_and_source_assets_implementation_plan.md`
[existing local implementation-plan convention].
