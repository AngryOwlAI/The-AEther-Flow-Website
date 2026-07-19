# Implementation Plan: Fluid Page System and `web-page` Curator

## Source PRD

- Source: the design-research response immediately preceding this planning
  request, promoted by the user to the governing PRD for this plan.
- Supplemental user requirements: create a repository-local skill named
  `web-page`; give it UI/UX design, system-analysis, and system-engineering
  responsibilities; create flexible guidance templates for the home page,
  overview pages, general resource pages, the Library, and the Diagram Gallery;
  account for all remaining page families; inspect upstream AEther Flow
  freshness before claim-bearing work.
- Repository: `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website`.
- Generated for: Codex app, Codex IDE, and repository-local
  implementation-control execution.
- Date: 2026-07-17.
- Planning status: **Ready with assumptions**. Implementation remains gated by
  the active homepage packet and the source-freshness decision described below.
- Companion task packets:
  `ImplementationPlans/fluid_page_system_and_web_page_curator_task_packets.md`.

## Executive Decision

The website should not be rebuilt as a collection of equally bounded cards, nor
should all content be allowed to stretch without limit. The implementation
should introduce a **fluid outer canvas with deliberate inner measures**:

1. Page sections and background bands may span the viewport.
2. Responsive gutters preserve usable edge space.
3. A shared grid aligns content across sections without imposing one universal
   fixed-width box.
4. Prose retains a readable line length.
5. Diagrams, videos, code, tables, galleries, and true modular records may
   retain visible containers.
6. Borders are used to communicate an actual object boundary, status, grouping,
   or interaction—not merely to prove that a section exists.

The implementation should preserve `BaseLayout.astro` as the site shell and add
page-template components beneath it. This is smaller, safer, and more consistent
with the live Astro architecture than replacing the shell or reviving the
unused `LandingLayout.astro` and `TechnicalPageLayout.astro`.

The requested `web-page` skill should be created as the governed curator for
this system. Its Markdown templates are **guidance contracts**, not canonical
page compositions. A page designer may vary hierarchy, rhythm, module order,
and visual treatment when the reader job justifies the variation, while the
skill enforces source authority, accessibility, responsive behavior, internal-
first navigation, validation, and one-bounded-packet execution.

## Product Summary

### Product goal

Modernize the complete reader-facing website so it feels spatially open,
responsive, intentional, and contemporary without weakening the Angry Owl
identity or The AEther Flow project's scientific and governance boundaries.
Turn the design intent into a reusable page system and a repository-local
curation workflow rather than a one-time CSS patch.

### Primary users

| User | Primary job |
| --- | --- |
| General reader | Understand what The AEther Flow is, why its two tracks matter, and where to start. |
| Physics reader | Distinguish ontology, exact-GR benchmark status, open derivation burdens, and evidence without mistaking orientation for proof. |
| AI/governance reader | Understand the governed research-agent system, roles, bounded AgentJobs, validators, and current state. |
| Reviewer or specialist | Inspect dense status, registries, documents, diagrams, claim boundaries, and provenance efficiently. |
| Website maintainer | Create or revise one page through a repeatable, source-bound, visually flexible workflow. |
| Codex agent | Select the correct page family, use the appropriate guidance template, implement one bounded packet, and leave reproducible validation evidence. |

### Jobs to be done

1. When the viewport becomes wider, use the available space for stronger
   composition and media scale instead of leaving the complete page in a
   narrow, bordered column.
2. When reading prose, keep the line length comfortable even though the outer
   section is fluid.
3. When inspecting a diagram, table, video, code sample, document record, or
   gallery item, preserve a clear object boundary and useful controls.
4. When moving between page families, encounter a coherent system without
   making every page visually identical.
5. When a maintainer asks Codex to create or revise a page, apply a governed
   design and source-curation workflow rather than ad hoc markup.
6. When upstream sources change, identify the affected routes and claim risk
   before presentation work silently republishes stale or stronger claims.

### Success criteria

- General page sections no longer depend on `1120px` or `1180px` as a global
  outer-page ceiling.
- At wide desktop sizes, the section canvas and grid grow with the viewport
  while gutters remain deliberate.
- Prose is normally constrained to approximately `60ch`–`72ch`; tables and
  media may use broader grid spans.
- A four-sided panel is exceptional and semantically justified.
- The home, overview, general resource, Library, Diagram Gallery, document
  library, general explainer, and utility families have explicit contracts.
- The `web-page` skill can classify a route, require a clean source basis,
  select a guidance template, enforce the quality gate, and stop after one
  governed packet.
- All 64 current Astro routes are inventoried and assigned a template,
  disposition decision, or redirect-review state.
- Relevant static builds, validators, browser checks, accessibility checks,
  manifest/provenance regeneration, and quality gates pass before release.
- No source claim is created or strengthened by the template migration.

## Repository Context

### Framework and build system

- Astro `7.0.3`, TypeScript/JavaScript, HTML, CSS, and Python validators.
- Static output configured in `astro.config.mjs`.
- Node.js `22.x`.
- npm scripts are the repository's command authority.
- Playwright is available as a development dependency for browser QA.
- No new production dependency is required by this plan.

### Current architecture

| Area | Observed state | Planning consequence |
| --- | --- | --- |
| Shared shell | `src/layouts/BaseLayout.astro` owns metadata, navigation, main landmark, footer, and navigation behavior. | Keep it; modernize its width behavior through a bounded shell packet. |
| Other layouts | `LandingLayout.astro` and `TechnicalPageLayout.astro` have no active consumers. | Do not build the new system on dead abstractions; review and delete only after dependency proof. |
| Shared page primitives | `CommandBand`, `EvidenceRail`, `StatusDossier`, `ProjectIntroduction`, `ComprehensionBlocks`, `SourceAuthoritySection`, `Figure`, and `OverflowTable` are already used. | Recompose and extend them rather than replacing the component vocabulary wholesale. |
| Shared explainer | `InternalExplainerPage.astro` renders several operations routes but owns a large fixed page composition and embedded visuals. | Migrate it behind the general explainer contract, then reduce duplicated layout ownership. |
| Specialized resources | `DiagramGalleryList.astro` and `DocumentActions.astro` already express specialized reader jobs. | Preserve their domain behavior within dedicated resource templates. |
| Content data | `src/lib/siteContent.ts`, `src/lib/internalExplainers.ts`, and `src/lib/manifests.ts` centralize navigation, route content, explainers, and published assets. | Templates accept typed data and slots; they do not become claim stores. |
| Global CSS | `src/styles/global.css` contains the design tokens and several generations of route styles. It uses `--max-width: 1120px` and multiple `width: min(100% - 2rem, 1180px)` rules. | Introduce semantic width tokens and compatibility aliases first; delete legacy selectors only after consumers migrate. |
| Route surface | 64 Astro route files are currently present. | The final migration ledger must account for every route, including the legacy `/project/*` subtree and `/license/`. |
| Provenance surface | `public/files/manifests/page_route_map.json` and generated `page_provenance.json` cover the governed public route set. | Route or claim-bearing page changes must update/regenerate the appropriate records. |
| Quality system | Validators cover manifests, content sources, public claims, internal-first links, layout language, SVG policy, comprehension, provenance, curator state, Cloudflare configuration, implementation control, build, and a broader quality gate. | Extend existing validators; do not create a parallel QA system. |

### Existing plans and contracts

This plan consolidates rather than discards useful prior work:

- `ImplementationPlans/recomendation_frontend.md` contains the broader frontend
  architecture, page archetypes, accessibility matrix, performance baselines,
  and release-validation ideas.
- `ImplementationPlans/sitewide_page_revamp_implementation_plan.md` defines the
  public-first, source-analysis-first route workflow.
- `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md` and
  `docs/architecture/sitewide-greenfield-foundation-contract.md` define the
  current navigation, page metadata, source-bundle, page-grammar, SVG, and
  review-ledger contracts.
- `docs/content-dossiers/_template.md` is the content/source template and should
  remain separate from the new visual page templates.
- The old plans refer to a procedural `to-web-page` skill, but no such skill is
  currently installed in `.codex/skills/`. The new requested name is
  `web-page`. References to `to-web-page` are historical planning context and
  must not be treated as a live skill.

Precedence for implementation is:

1. `AGENTS.md`, safety, source authority, and live repository evidence.
2. Live implementation-control task/job/handoff records.
3. This PRD-derived plan.
4. Existing implementation plans and contracts as supporting context.
5. Existing page markup as evidence, not mandatory architecture.

### Current implementation-control state

At planning time, the repository has an active ready-for-checkpoint packet:
`WI-20260717-001`, **Align Homepage Primary Actions**. Its live handoff forbids
opening another packet, staging, committing, pushing, deploying, or refreshing
sources. Therefore:

- This planning work does not alter runtime code or control records.
- `GATE-00` must resolve that packet through the authorized checkpoint workflow
  before the implementation program opens its first packet.
- Existing dirty changes, especially `src/styles/global.css` and
  `tests/test_public_positioning.py`, must be preserved and classified before
  any layout work begins.

### Upstream source state

Read-only inspection produced the following planning evidence:

- Website accepted source pin:
  `57438af555214bc0785dcb390ee6254f580b8a62`.
- Clean upstream `origin/main`:
  `fd802dee85da59d29c71842f9dcfa882a0927c29`.
- Upstream local working branch:
  `codex/v19-remaining-relay` at
  `eaa300adc942150b87441bb33d27c2e85aa9fc7b`, with unrelated uncommitted work.
- The accepted pin is an ancestor of clean upstream `main`.
- Eight declared page dependencies changed between the accepted pin and clean
  upstream `main`.
- Running the curator against a temporary clean checkout of `fd802dee` found
  41 drift items: 1 critical and 40 `review_required`.
- The critical item affects `/physics/claim-status/` through
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`.

Consequences:

- Never bind source-refresh work to the dirty upstream working tree.
- `SRC-01` must use a clean immutable checkout.
- Claim-sensitive route migrations must wait for source-drift classification.
- Claim-neutral skill contracts, inventories, and layout primitives may proceed
  after `GATE-00`, provided they do not regenerate source-derived content.

## Design Diagnosis

### Observed problem

The screenshot and CSS agree with the user's diagnosis. Several page families
use a fixed centered outer width, repeated four-sided borders, near-identical
dark panels, and card-like section containment. At larger viewport widths, the
page does not meaningfully expand. The result is visually coherent but overly
boxy, horizontally timid, and insufficiently differentiated by reader job.

### Important distinction

The defect is not “all maximum widths are old-fashioned.” Readable prose,
intrinsic media, and complex data still need bounds. The defect is using one
fixed container and one framed-panel language for nearly every level of the
page.

### Modern design principles adopted by this plan

1. **Fluid by default, bounded by purpose.** HTML and modern grid/flex layouts
   are naturally responsive; fixed page widths create excess empty space on
   wide screens and overflow pressure on narrow screens (MDN Web Docs, 2025).
2. **Use a grid for alignment, not imprisonment.** A responsive grid and
   gutters create consistent relationships while individual sections choose
   their appropriate spans (U.S. Web Design System, n.d.-a; Carbon Design
   System, n.d.).
3. **Keep readable measures inside fluid canvases.** Relative widths and
   controlled line length support reflow and reading comfort (World Wide Web
   Consortium, 2026a, 2026b).
4. **Use cards only for actual discrete objects.** Cards are appropriate for
   concise, self-contained, peer-level content—not as a default wrapper around
   continuous narrative (U.S. Web Design System, n.d.-b).
5. **Let reusable components respond to their container.** Container queries
   are appropriate for reusable rails, gallery records, and media modules that
   may occupy different grid spans (MDN Web Docs, 2026).
6. **Create hierarchy with rhythm.** Spacing, full-bleed tonal bands,
   typography, alignment, and selective rules should do most section
   separation; four-sided borders should signal a genuine boundary.

## Scope

### In scope

- Repository-local `web-page` skill, agent manifest, guidance references,
  templates, validation, and skill registration.
- Fluid page-layout tokens and reusable Astro primitives.
- Explicit page-template contracts and components.
- Page-family inventory for all 64 current routes.
- Migration of the governed modern route families.
- Source-drift classification before claim-sensitive page work.
- Conditional disposition of legacy `/project/*` routes.
- Accessibility, responsive, performance, provenance, manifest, browser, and
  release validation.
- Removal of demonstrably unused layouts/selectors after migration.

### Out of scope

- Changing upstream physics, mathematics, AI-governance, or research claims.
- Treating website copy, plans, memory, or generated diagrams as upstream
  authority.
- Writing to the upstream AEther Flow repository.
- A new frontend framework, component runtime, CMS, database, analytics
  platform, or production dependency.
- Automatic deployment. Deployment remains a separate explicit user action
  through the existing `push-and-deploy` workflow.
- Rebranding Angry Owl or replacing the cyan/orange/ivory visual identity.
- Making every route unique for novelty's sake.
- Resolving the legacy route information-architecture decision before
  `LEGACY-01` produces current evidence.

## Assumptions

| ID | Type | Assumption | Evidence | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | The preceding design response is the PRD even though it is not a checked-in PRD file. | The user explicitly promoted it to PRD status. | Plan adoption. |
| ASM-002 | Planning assumption | The new skill is named `web-page`, not `to-web-page`. | The user explicitly chose the name; the old skill is absent. | Skill creation. |
| ASM-003 | Planning assumption | Templates are design guidance with mandatory invariants and optional modules, not rigid canonical markup. | Explicit user requirement. | Skill/template implementation. |
| ASM-004 | Planning assumption | `BaseLayout.astro` remains the shell. | It is the active shared layout for the current static site. | Foundation coding. |
| ASM-005 | Planning assumption | Page templates live under `src/components/page-templates/`, not `src/layouts/`. | The project already uses one real shell layout and component composition; two other layouts are unused. | Architecture packet. |
| ASM-006 | Planning assumption | A document-library template is warranted in addition to the user's minimum list. | `/resources/documents/` has a specialized document/download reader job and `DocumentActions.astro`. | Template contract review. |
| ASM-007 | Planning assumption | General explainers and utility/legal pages need explicit fallback contracts. | Thirty `/project/*` routes and `/license/` do not fit the five minimum templates. | Route classification. |
| ASM-008 | Planning assumption | The initial visual pilot is `/physics/`. | It is the route selected in the original browser comment and exposes the fixed-width problem clearly. | Pilot packet. |
| ASM-009 | Planning assumption | One route is migrated per governed route packet after shared foundations exist. | Repository memory, prior plans, and implementation-control discipline favor bounded packets. | Route rollout. |
| ASM-010 | Planning assumption | Existing page copy remains unchanged unless a source-bound page packet explicitly authorizes copy changes. | The PRD is primarily a design-system request and source authority remains upstream. | Every route packet. |
| ASM-011 | Planning assumption | Clean upstream `main` is the comparison source, but not automatically the new accepted website pin. | Curator drift requires review and explicit source-refresh authority. | `SRC-01` closeout. |
| ASM-012 | Implementation detail | Container queries will be used only where a component is reused in materially different widths. | This avoids unnecessary complexity while supporting flexible templates. | Component implementation. |
| ASM-013 | Implementation detail | The first implementation keeps CSS in the existing global pipeline, with a dedicated page-layout section or imported stylesheet selected by the packet. | Avoids a speculative CSS architecture rewrite. | `FOUND-01`. |
| ASM-014 | Planning assumption | Human visual acceptance remains required before release even after automated checks pass. | Existing review ledgers and QA artifacts distinguish technical validity from owner acceptance. | `QA-01`. |

## Open Questions

None prevents a credible plan. The following decisions are deliberately
deferred to evidence-producing packets:

| ID | Classification | Question | Resolution point | Impact if unanswered |
| --- | --- | --- | --- | --- |
| Q-001 | Planning assumption | Should clean upstream `main` become the new accepted website source pin? | `SRC-01` after reviewing 41 drift items. | Claim-sensitive migrations remain blocked. |
| Q-002 | Implementation detail | Should page-template primitives be placed in one `page-layout.css` file or a bounded section of `global.css` first? | `FOUND-01` after selector-dependency inspection. | No product impact; affects maintainability and diff size. |
| Q-003 | Implementation detail | Which current panels remain semantically boxed? | Each route's before/after containment audit. | Visual quality degrades if decided globally without content context. |
| Q-004 | Product decision | Which `/project/*` routes remain canonical, become redirects, or remain specialist-only? | `LEGACY-01`. | Legacy migration/deletion packets cannot be opened safely. |
| Q-005 | Product decision | Does the owner want optional search/filter behavior in Library and Diagram Gallery now or only a layout contract ready for it? | `RES-02` and `RES-03` baseline inventory. | Determines progressive enhancement scope; static browsing remains required. |
| Q-006 | Implementation detail | Which wide-screen ceiling, if any, is appropriate for data-heavy media beyond approximately 1800–2000 CSS pixels? | Pilot browser QA. | Affects ultra-wide polish, not baseline responsiveness. |

## Requirement Traceability Matrix

### Functional requirements

| Requirement | User-visible or maintainer-visible behavior | Implementation area | Task packets | Validation |
| --- | --- | --- | --- | --- |
| REQ-001 Fluid outer canvas | General sections expand with the viewport instead of stopping at one global fixed width. | Layout tokens, `PageSection`, page templates, shell. | `FOUND-01`, `SHELL-01`, all page packets | Computed-style audit; wide screenshots; `npm run validate:layout`. |
| REQ-002 Responsive gutters | Side margins remain present and scale by viewport. | `--page-gutter-*`, grid primitives. | `FOUND-01`, all page packets | 320, 768, 1280, 1536, 1920 CSS-pixel checks. |
| REQ-003 Shared alignment grid | Sections align through a responsive 12-column model on wide screens and collapse deliberately. | `PageGrid`/`PageSection` primitives. | `FOUND-01`, page-template packets | Overlay/manual alignment review; browser screenshots. |
| REQ-004 Readable prose | Long prose normally stays around 60–72 characters per line. | `prose` width mode; heading/body slots. | `FOUND-01`, all page packets | Computed width and representative line-length review. |
| REQ-005 Wide media/data | Diagrams, video, code, tables, and galleries may occupy broader spans than prose. | `media` and `data` modes; `MediaFrame`; `OverflowTable`. | `FOUND-01`, `RES-03`, `RES-04`, route packets | Overflow and wide-screen QA. |
| REQ-006 Selective containment | Only semantic objects retain full containers; continuous narrative is unboxed. | Template guidance, CSS migration. | `SKILL-01`, `PAGE-01` onward | Per-section containment audit in QA receipt. |
| REQ-007 Rhythmic section separation | Spacing, tonal bands, alignment, and selective rules establish hierarchy. | Design tokens and template contracts. | `FOUND-01`, page packets | Before/after visual review. |
| REQ-008 Home template | Home has a unique, public-first composition. | `HomePageTemplate.astro` and guidance template. | `SKILL-01`, `PAGE-02` | Home desktop/mobile/ultra-wide QA; content/link validators. |
| REQ-009 Overview template | Physics, AI, and Resources category landings use a flexible overview contract. | `OverviewPageTemplate.astro`. | `SKILL-01`, `PAGE-01`, `PAGE-03`, `PAGE-04` | Three-route comparison matrix; no forced identical composition. |
| REQ-010 General resource template | Ordinary resource routes use a reader-job and contextual-provenance grammar. | `ResourcePageTemplate.astro`. | `SKILL-01`, `RES-01`, `RRES-*` | Resource source-authority prohibition; content/link/browser checks. |
| REQ-011 Library template | Library browsing, status, metadata, and empty/no-result states have a dedicated contract. | `LibraryPageTemplate.astro`, library data. | `SKILL-01`, `RES-02` | Keyboard, no-results, 320px, wide-data checks. |
| REQ-012 Diagram Gallery template | Gallery browsing and inspection use a dedicated, manifest-backed contract. | `DiagramGalleryPageTemplate.astro`, `DiagramGalleryList.astro`. | `SKILL-01`, `RES-03` | SVG/manifest/keyboard/dialog or expansion checks. |
| REQ-013 Document Library template | Document roles, TeX/PDF authority, metadata, and download actions are explicit. | `DocumentLibraryPageTemplate.astro`, `DocumentActions.astro`. | `SKILL-01`, `RES-04` | Manifest, download, format-role, mobile table checks. |
| REQ-014 General explainer template | Claim-bearing child pages get a flexible explanatory grammar. | `ExplainerPageTemplate.astro`, `InternalExplainerPage.astro`. | `SKILL-01`, `EXP-01`, `RPHY-*`, `RAI-*` | Dossier/comprehension/provenance checks. |
| REQ-015 Utility template | Legal/support routes avoid accidental use of claim-bearing templates. | `UtilityPageTemplate.astro` or documented exception. | `SKILL-01`, `UTIL-01` | `/license/` semantic and responsive QA. |
| REQ-016 Flexible guidance | Templates define required invariants and optional modules without fixing every order or appearance. | Skill references and Markdown templates. | `SKILL-01`, `SKILL-02` | Validator checks required fields, not one canonical sequence. |
| REQ-017 `web-page` skill | Maintainers can invoke one repository-local page-curation skill. | `.codex/skills/web-page/`. | `SKILL-01`, `SKILL-02` | Skill structure/test; README registration. |
| REQ-018 Multidisciplinary role | Skill acts as UI/UX designer, system analyst, system engineer, and source curator. | `SKILL.md` role and decision protocol. | `SKILL-01` | Review against role responsibilities and failure modes. |
| REQ-019 Route-family classifier | Skill assigns the route to the correct template or justified exception. | Page-family registry and routing reference. | `ARCH-01`, `SKILL-01` | All 64 routes accounted for. |
| REQ-020 Source preflight | Claim-bearing work verifies source bundle, freshness, and authority first. | Skill source protocol; curator; manifests. | `SRC-01`, `SKILL-01`, route packets | `npm run validate:curator`, provenance checks, receipt. |
| REQ-021 One bounded packet | Each invocation implements at most one route or one shared foundation concern. | Skill stopping rules and implementation control. | All packets | `npm run validate:implementation-control`; handoff review. |
| REQ-022 Preserve claims | Layout work does not silently change or strengthen scientific/governance claims. | All pages/data/manifests. | All page packets | Content, claims, provenance, diff review. |
| REQ-023 Internal-first navigation | Primary journeys remain on website routes; GitHub/source links remain inspection paths. | Navigation, actions, evidence rails. | `SHELL-01`, page packets | `npm run validate:links`. |
| REQ-024 Resource authority rule | `/resources/*` does not render a dedicated Source authority section. | Resource templates and validator. | `RES-01`–`RES-04`, `RRES-*`, `CLEAN-01` | `npm run validate:layout`. |
| REQ-025 Preserve brand | Angry Owl palette, typography direction, accessible animated visuals, and editorial tone remain recognizable. | Tokens, SVGs, templates. | `FOUND-01`, all visual packets | Visual review; `npm run validate:svg`. |
| REQ-026 Fluid shell | Header and footer participate in the fluid system without losing behavior/content. | `BaseLayout.astro`, shell CSS. | `SHELL-01` | Keyboard navigation; compact menu; footer link review. |
| REQ-027 Current source drift | Clean upstream changes are reviewed before claim-sensitive migration. | Curator/provenance/source pin. | `SRC-01` | Zero unresolved critical drift before affected page release. |
| REQ-028 Route inventory | Every current Astro route has a family, canonical status, and migration state. | Page-family registry/review ledger. | `ARCH-01`, `LEGACY-01`, `QA-01` | Inventory count equals current route count; no orphan rows. |
| REQ-029 Safe cleanup | Dead layouts, aliases, and fixed-width selectors are removed only after consumer proof. | Layouts, CSS, tests. | `CLEAN-01` | `rg` consumer proof, diff review, full validation. |
| REQ-030 Reproducible QA receipt | Each page packet records visual decisions, containment exceptions, commands, and artifacts. | `web-page` receipt template; `docs/quality/`. | `SKILL-01`, all page packets | Receipt completeness validator/manual review. |

### Non-functional requirements

| Requirement | Quality target | Implementation area | Task packets | Validation |
| --- | --- | --- | --- | --- |
| NFR-001 Static compatibility | Every affected route remains a static Astro page. | Astro templates/routes. | All runtime packets | `npm run build`. |
| NFR-002 Reflow | No page-level horizontal scrolling at 320 CSS pixels or equivalent 400% zoom; bounded data regions expose accessible overflow. | CSS/templates/tables/media. | `FOUND-01`, all page packets, `QA-01` | 320px and 400% browser checks; W3C reflow review. |
| NFR-003 Zoom and text resize | Layout and controls remain usable at 200% and 400% zoom. | Responsive CSS and navigation. | `SHELL-01`, page packets | Browser matrix. |
| NFR-004 Keyboard and focus | All interactive controls work by keyboard with visible focus and logical order. | Shell, gallery/library controls, links. | `SHELL-01`, `RES-02`, `RES-03`, all page packets | Keyboard walkthrough. |
| NFR-005 Reduced motion | Essential meaning does not depend on animation; reduced-motion behavior is preserved. | SVG/CSS motion rules. | Visual packets | Reduced-motion screenshot and behavior check. |
| NFR-006 Contrast and semantics | Text, controls, landmarks, headings, captions, tables, and ARIA remain accessible. | Templates/components/tokens. | All runtime packets | Existing validators plus manual semantic review. |
| NFR-007 Performance | The migration does not add a client runtime or materially regress the accepted frontend baseline without justification. | Astro/CSS/assets. | `FOUND-01`, specialized pages, `QA-01` | `scripts/frontend_performance_baseline.py`; asset/network review. |
| NFR-008 Maintainability | Width behavior is expressed through semantic tokens/modes instead of route-specific pixel copies. | Page primitives and CSS. | `FOUND-01`, `CLEAN-01` | Selector audit and focused tests. |
| NFR-009 Reliability | Source, manifest, provenance, build, and quality gates fail closed. | Validators/control/curator. | `SRC-01`, `SKILL-02`, `CLEAN-01`, `QA-01` | `npm run validate`; `npm run quality`. |
| NFR-010 No new dependency | Use Astro, CSS Grid/Flexbox, and existing scripts. | Entire program. | All packets | `package.json` diff review. |
| NFR-011 Reversibility | Each packet has a bounded rollback and does not combine source refresh, layout migration, and deployment. | Implementation-control records. | All packets | Handoff/rollback review. |
| NFR-012 Data/privacy neutrality | No personal data, authentication, tracking, or new external data flow is introduced. | Site architecture. | All packets | Diff/network review. |

## Proposed Technical Approach

### 1. Authority and execution layers

The implementation must keep five layers distinct:

| Layer | Purpose | Authority |
| --- | --- | --- |
| Upstream AEther Flow | Physics, mathematics, AI-governance, registries, and research state. | Canonical source authority. |
| Content dossier/source bundle | Route-specific source reading, reader job, safe/unsafe implications, diagrams, and freshness. | Implementation input, not new source authority. |
| `web-page` skill | Select template, analyze system/page, implement one packet, validate, and record evidence. | Procedural execution contract. |
| Page-template components | Provide semantic composition, width modes, slots, and accessibility defaults. | Presentation contract only. |
| Route page and public manifests | Bind reviewed content to the public URL and generated provenance. | Reader-facing derivative. |

The skill must never infer that a visual template authorizes new claims.

### 2. `web-page` skill design

#### Proposed file structure

```text
.codex/skills/web-page/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── page-authority-contract.md
│   ├── page-family-routing.md
│   ├── source-freshness-protocol.md
│   ├── ui-ux-quality-gate.md
│   └── browser-qa-matrix.md
├── templates/
│   ├── page-implementation-brief.md
│   ├── page-review-receipt.md
│   ├── home-page-template.md
│   ├── overview-page-template.md
│   ├── resource-page-template.md
│   ├── library-page-template.md
│   ├── diagram-gallery-page-template.md
│   ├── document-library-page-template.md
│   ├── explainer-page-template.md
│   └── utility-page-template.md
└── scripts/
    └── validate_web_page_skill.py
```

Also update:

- `.codex/skills/README.md`
- `package.json` only if a repository validation command is deliberately added
- focused tests under `tests/`

#### Required skill roles

The skill should act through four coordinated lenses:

1. **UI/UX designer:** reader job, information hierarchy, visual rhythm,
   responsive composition, interaction, cognitive load, accessibility, and
   page-family fit.
2. **System analyst:** route purpose, upstream source basis, dependency
   boundaries, content state, claim risk, existing components, and related
   routes.
3. **System engineer:** implementation-control authority, component contracts,
   failure modes, maintainability, validation, rollback, and release evidence.
4. **Page curator:** freshness, provenance, internal-first paths, template
   selection, visual consistency, and human review handoff.

#### Required invocation flow

1. Resolve live implementation-control state.
2. Stop if another packet forbids opening work.
3. Identify whether the request is new-page, redesign, content-only, asset-only,
   or review-only.
4. Inventory the route and nearest consumers.
5. Select a page family or record a justified exception.
6. Read the relevant guidance template completely.
7. Inspect the route's dossier/source bundle and accepted source binding.
8. Run curator/source-freshness checks appropriate to claim risk.
9. State the reader job, content hierarchy, visual intent, containment
   decisions, and smallest change boundary.
10. Implement one route or one shared foundation concern.
11. Run narrow validation, then required broader checks.
12. Perform desktop, mobile, wide, zoom, keyboard, and reduced-motion QA as
    applicable.
13. Write a page review receipt with commands, artifacts, exceptions, and
    remaining human-review status.
14. Stop at checkpoint/handoff. Do not push or deploy unless a separate
    authorized workflow is invoked.

#### Flexible-template rule

Every guidance template should distinguish:

- **Mandatory invariants:** authority boundary, reader job, page title,
  accessible landmarks/headings, responsive width behavior, internal next
  steps, provenance treatment, validation, and review state.
- **Recommended modules:** hero, public introduction, mechanism, evidence,
  status, diagram, glossary, related routes, and source context.
- **Conditional modules:** equations, filters, tables, downloads, timelines,
  code, video, comparisons, reviewer actions, and no-results states.
- **Forbidden defaults:** wrapping every section in a bordered panel, using
  cards for continuous prose, embedding visible text in SVGs, turning source
  links into the primary journey, or changing claims because a template has an
  empty slot.

The skill should allow reordering and visual variation when documented in the
page brief. It should validate invariants and rationale, not a single DOM
sequence.

### 3. Runtime page-template architecture

Use component templates beneath `BaseLayout`:

```text
src/components/page-templates/
├── PageSection.astro
├── PageGrid.astro
├── MediaFrame.astro
├── SectionHeader.astro
├── HomePageTemplate.astro
├── OverviewPageTemplate.astro
├── ResourcePageTemplate.astro
├── LibraryPageTemplate.astro
├── DiagramGalleryPageTemplate.astro
├── DocumentLibraryPageTemplate.astro
├── ExplainerPageTemplate.astro
└── UtilityPageTemplate.astro
```

The final exact file count should be selected during `FOUND-01` and the first
template packets. A smaller composition is acceptable if it preserves the
contracts. Do not create a component merely to mirror every Markdown template.

#### Primitive responsibilities

| Primitive | Responsibility | Must not own |
| --- | --- | --- |
| `PageSection` | Full-bleed band, section spacing, semantic element/label, tone, and inner width mode. | Claims, route-specific headings, or arbitrary card styling. |
| `PageGrid` | Responsive alignment columns and named spans. | Fixed route content order. |
| `SectionHeader` | Eyebrow/title/lead relationships and heading level. | Page-level source authority. |
| `MediaFrame` | Semantic containment for diagram/video/image/code with caption and optional controls. | Visible SVG labels or unreviewed assets. |
| Page-family templates | Arrange required and optional slots and apply family metadata/classes. | Canonical scientific copy or one immutable visual composition. |

#### Width taxonomy

The system should expose semantic width modes:

| Mode | Intended use | Behavior |
| --- | --- | --- |
| `full` | Background, separator, or special full-bleed visual. | Spans viewport; content may still use safe gutters. |
| `grid` | Normal section composition. | Uses responsive page gutters and the full shared grid. |
| `prose` | Narrative paragraphs and explanatory headings. | Grid-aligned with approximately 60–72ch reading measure. |
| `media` | Diagrams, video, large illustrations, comparison figures. | Broader grid span; intrinsic-size and aspect-ratio safeguards. |
| `data` | Tables, registries, document lists, dense status. | Broad span; local overflow when irreducible. |

Suggested tokens to validate in the pilot rather than blindly freeze:

```text
--page-gutter-inline: clamp(1rem, 3vw, 4.5rem)
--page-grid-gap: clamp(1rem, 2vw, 2rem)
--page-section-space: clamp(3.5rem, 7vw, 8rem)
--page-reading-measure: 68ch
--page-wide-measure: 96rem (optional safety ceiling for extreme displays)
```

`--page-wide-measure` is not a replacement global box. If retained, it is an
ultra-wide readability/composition guard applied selectively to grid content,
while section backgrounds remain fluid.

#### CSS migration strategy

1. Add semantic tokens and primitives without deleting existing selectors.
2. Add compatibility mappings for `overview-shell`, `overview-panel`,
   `track-page-hero`, `track-page-band`, `content-band`, header, and footer.
3. Migrate the `/physics/` pilot and measure the result.
4. Migrate template families one route per packet.
5. Record remaining consumer counts after every phase.
6. Remove `1120px`/`1180px` outer-page behavior and legacy aliases only after
   no active route depends on them.
7. Keep legitimate `max-width` rules for prose, controls, dialogs, and intrinsic
   media.

### 4. Page-template contracts

#### Home page

Required:

- public identity and two-track thesis;
- clear primary action and bounded secondary actions;
- substantial public introduction;
- physics and AI track orientation;
- current project/status context;
- guided reading paths;
- internal-first next steps;
- source-boundary context;
- responsive hero/visual area.

Flexible:

- asymmetrical hero;
- full-bleed atmospheric band;
- alternating editorial sections;
- status rail or dossier;
- one or more media moments.

Avoid:

- turning every track paragraph into a card;
- placing the entire home page inside one centered panel;
- making source links the main call to action.

#### Category overview page

Applies to `/physics/`, `/ai-research-system/`, and `/resources/`.

Required:

- category identity and reader promise;
- public introduction;
- conceptual/status map;
- child-route orientation;
- current status or scope boundary where relevant;
- recommended next step;
- source/provenance treatment appropriate to the family.

Flexible:

- editorial split hero;
- route rail, staged path, matrix, or true peer cards;
- a large visual or status summary;
- category-specific section order.

#### General resource page

Required:

- resource reader job;
- what the resource contains and does not prove;
- internal routes/assets/data needed for the job;
- contextual provenance and limits;
- no dedicated `SourceAuthoritySection`.

Flexible:

- table, inventory, timeline, route rail, glossary, or ordinary prose;
- object containers where the resource itself is a discrete artifact.

#### Library

Required:

- browsing purpose and audience;
- featured or recommended entry points;
- clear distinctions among source, derivative, document type, and status;
- scalable result/shelf layout;
- keyboard-operable controls if filtering is added;
- no-results/empty state;
- contextual provenance without a dedicated source-authority section.

The page must work as static HTML without JavaScript. Client enhancement may
improve filtering but cannot hide the complete library from no-script users.

#### Diagram Gallery

Required:

- manifest-backed diagram catalog;
- concept/category context;
- result count or inventory context;
- accessible preview, caption, description, and inspection path;
- mobile-safe media;
- no-results state if filtering is present;
- explicit statement that a diagram is a reader aid, not source proof;
- no dedicated source-authority section.

If a dialog/lightbox is introduced, it must handle focus entry, focus return,
Escape, accessible naming, scroll locking, and no-script fallback. A simpler
expanded-page link is preferred if those requirements would expand the packet
unreasonably.

#### Document Library

Required:

- reading order and audience;
- document status;
- TeX source versus generated PDF role;
- manifest-backed file metadata and actions;
- mobile-safe data presentation;
- contextual provenance and format limits.

#### General explainer

Required:

- reader context;
- plain-language summary;
- mechanism or conceptual sequence;
- evidence/status;
- terminology near use;
- boundaries and unsafe implications;
- related internal routes;
- source provenance;
- dedicated source-authority section only outside `/resources/*`.

#### Utility/legal

Required:

- task-specific title and content;
- simple readable measure;
- correct legal/support semantics;
- internal return path;
- no claim-bearing modules unless independently justified.

### 5. Route-family inventory

#### Governed modern route set

| Family | Routes | Planned template |
| --- | --- | --- |
| Home | `/` | Home |
| Physics overview | `/physics/` | Overview |
| Physics explainers/status | `/physics/claim-status/`, `/physics/derivation-roadmap/`, `/physics/exact-gr-benchmark/`, `/physics/flow-geometry/`, `/physics/ontology/`, `/physics/open-burdens/` | Explainer, with `data`/status variants where needed |
| AI overview | `/ai-research-system/` | Overview |
| AI explainers/status | `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/current-state/`, `/ai-research-system/human-gated-promotion/`, `/ai-research-system/memory-preflight/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/roles-and-schemas/`, `/ai-research-system/runtime-requirements/`, `/ai-research-system/validators-and-handoffs/`, `/ai-research-system/workflow/` | Explainer |
| Resources overview | `/resources/` | Overview |
| General resources | `/resources/generated-derivatives/`, `/resources/guided-starts/`, `/resources/guided-starts/general-public/`, `/resources/publication-process/`, `/resources/reading-paths/`, `/resources/registries/`, `/resources/repository-map/`, `/resources/retrieval-layers/`, `/resources/reviewer-packet/`, `/resources/site-builder-guide/`, `/resources/source-authority/` | General resource, with reviewer/guided-start variants |
| Resource Library | `/resources/library/` | Library |
| Diagram Gallery | `/resources/diagrams/` | Diagram Gallery |
| Document Library | `/resources/documents/` | Document Library |
| Utility | `/license/` | Utility |

#### Legacy/specialist route set requiring disposition

`LEGACY-01` must classify the following 30 routes as `canonical`,
`specialist-only`, `redirect candidate`, or `retire candidate` before code
deletion or migration:

- `/project/ai-research-agent-system/`
- `/project/ai-research-agent-system/memory-registries/`
- `/project/ai-research-agent-system/one-bounded-agentjob/`
- `/project/ai-research-agent-system/parent-child-synthesis/`
- `/project/ai-research-agent-system/role-authority-inspector/`
- `/project/ai-research-agent-system/roles-and-skills/`
- `/project/ai-research-agent-system/workflow/`
- `/project/operations/`
- `/project/operations/director-agentjob-lifecycle/`
- `/project/operations/project-system-improvement/`
- `/project/operations/publication-process/`
- `/project/operations/role-routing/`
- `/project/operations/technical-requirements/`
- `/project/operations/validator-operator-workflow/`
- `/project/physics/`
- `/project/physics/claim-gates/`
- `/project/physics/current-state/`
- `/project/physics/distance-to-gr/`
- `/project/physics/exact-gr-benchmark/`
- `/project/physics/finite-toy-models/`
- `/project/physics/gate-chair-and-human-gates/`
- `/project/physics/gr-derivation-roadmap/`
- `/project/physics/metric-response-ladder/`
- `/project/physics/negative-results-and-frozen-routes/`
- `/project/physics/no-target-import-discipline/`
- `/project/physics/ontology/`
- `/project/physics/source-extension-pipeline/`
- `/project/source-authority/`
- `/project/source-authority/claim-boundary-explorer/`
- `/project/source-authority/publication-and-provenance-system/`

Likely duplicates must not be redirected solely because their titles resemble
modern routes. The disposition must compare reader job, source dossier,
navigation role, inbound internal links, route-map/provenance coverage, and
unique specialist content.

### 6. State, data, and API impact

- No server API, database, authentication, or persistent user state is needed.
- Existing typed data modules should remain claim/content stores.
- A small page-family registry may be added under `src/lib/` or
  `docs/architecture/`; `ARCH-01` decides whether runtime typing adds value.
- Gallery/library filtering, if added, is progressive enhancement over complete
  static HTML.
- Loading states are unnecessary for static content. If media is lazy-loaded,
  intrinsic dimensions and stable placeholders must prevent layout shifts.
- Empty/no-result states are required only for user-controlled filtering or a
  truly empty manifest group.
- Errors in source binding, route classification, manifests, or template
  invariants must fail validation rather than render a misleading fallback.

### 7. Accessibility and responsive acceptance

Every runtime page packet should cover the relevant subset of:

| Profile | Required observation |
| --- | --- |
| 320 × 568 | No page-level horizontal scroll; readable hierarchy; controls fit or wrap. |
| 390 × 844 | Representative modern mobile layout. |
| 768 × 1024 | Tablet/intermediate composition, not an enlarged mobile stack by accident. |
| 1280 × 800 | Standard desktop composition. |
| 1536 × 1285 | Compare directly with the original physics screenshot context. |
| 1920 × 1080 | Verify the page uses width intentionally and does not look trapped. |
| Short landscape | Navigation and overlays remain usable. |
| 200% zoom | Navigation, headings, controls, and data remain operable. |
| 400% zoom / 320 equivalent | WCAG reflow behavior. |
| Keyboard only | Logical order, visible focus, menus/filters/dialogs operable. |
| Reduced motion | Animated visuals stop or reduce without losing meaning. |

The site must not claim WCAG conformance from these checks alone. They are
acceptance evidence for the affected behaviors.

### 8. Validation and observability

This static site does not need production logging for the layout system.
Observability consists of:

- implementation-control state and handoffs;
- source-curator reports;
- generated manifests and provenance;
- focused validator output;
- per-page QA receipts;
- Playwright screenshots under `output/playwright/`;
- final performance-baseline comparison;
- owner review status in the appropriate review ledger.

## Files and Directories Likely Affected

### New

- `.codex/skills/web-page/**`
- `src/components/page-templates/**` (exact set determined incrementally)
- focused tests for the skill, template contracts, and layout language
- page-family registry or architecture record
- per-packet QA receipts under `docs/quality/`

### Modified

- `.codex/skills/README.md`
- `src/styles/global.css` and possibly one imported page-layout stylesheet
- `src/layouts/BaseLayout.astro`
- selected existing primitives
- one route per page packet
- `src/lib/siteContent.ts`, `src/lib/internalExplainers.ts`, or
  `src/lib/manifests.ts` only when a route packet requires it
- `scripts/validate_layout_language.py`
- `scripts/validate_public_comprehension.py` only when its current contract
  needs a compatible update
- `public/files/manifests/page_route_map.json`,
  `page_provenance.json`, source/asset manifests only when route/source/asset
  changes require them
- implementation-control records for each authorized packet

### Candidate deletions after proof

- `src/layouts/LandingLayout.astro`
- `src/layouts/TechnicalPageLayout.astro`
- unused `DownloadList.astro`
- obsolete fixed-width aliases and selectors
- obsolete route files only after `LEGACY-01`, redirects, provenance updates,
  smoke checks, and owner approval

No deletion is authorized by this plan alone.

## Implementation Phases

1. **Control and source gates.** Resolve the active homepage packet, then
   classify clean upstream drift. No layout work begins inside the existing
   dirty packet.
2. **Curator contract.** Create and validate the `web-page` skill, flexible
   guidance templates, and page-review receipt.
3. **Inventory and baseline.** Account for all routes, capture representative
   screenshots/computed widths, and freeze the template assignment ledger.
4. **Fluid foundation.** Add semantic width modes and shared primitives without
   deleting compatibility styles.
5. **Pilot.** Migrate `/physics/`, compare against the original problem, and
   adjust tokens/contracts based on evidence.
6. **Primary page families.** Migrate home, AI overview, Resources overview,
   general resource, Library, Diagram Gallery, documents, explainer, and
   utility surfaces in separate packets.
7. **Governed route queue.** Apply the accepted templates to the remaining 24
   modern child routes, one route per packet.
8. **Legacy disposition.** Decide the `/project/*` route future and create
   separate follow-on packets for any retained migration or redirect.
9. **Cleanup and enforcement.** Remove proven-dead layout language and strengthen
   validators only after migration.
10. **Sitewide QA and release readiness.** Validate all routes, compare
    performance, record human review status, and stop before push/deploy.

## Codex Task Packets

The companion file defines:

- 20 fully specified core packets;
- 24 instantiated one-route migration packets using a common full contract;
- 44 total planned packets before any conditional legacy-route implementation
  packets created by `LEGACY-01`.

Task packets are ordered by dependency and are intentionally smaller than the
complete redesign program. Several documentation-only packets may run in
parallel only when live implementation control explicitly allows it; default
execution remains one packet at a time.

## Validation Plan

### Planning-artifact validation

- Inspect both plan files for required sections and stable requirement IDs.
- Confirm every requirement maps to at least one task.
- Confirm every core task has Goal, Context, Constraints, Implementation notes,
  Acceptance criteria, Validation, and Done when.
- Run `git diff --check`.
- Do not run runtime quality gates merely to validate Markdown planning files.

### Skill packets

- Focused Python tests for skill structure and guidance-template invariants.
- `.codex/skills/README.md` registration review.
- `git diff --check`.
- `npm run validate:implementation-control` when control records change.
- Broader `python3 -m pytest` using the repository's available environment.

### Page packets

Run the narrowest relevant checks first:

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
```

Use `npm run validate:manifests` when assets/manifests change. Regenerate with
the actual repository commands only when required:

```text
python3 scripts/build_asset_manifest.py --write
python3 scripts/generate_page_provenance.py
```

Run targeted Python tests first, then:

```text
python3 -m pytest
```

Use the project environment form recorded by the live packet if it differs.

### Browser and release checks

- Start/confirm the local static preview on an available port.
- Perform the viewport, zoom, keyboard, and reduced-motion matrix.
- Store screenshots/receipts using the existing `output/playwright/` and
  `docs/quality/` conventions.
- Run:

```text
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:<port>
npm run validate
npm run quality
```

- Run `python3 scripts/frontend_performance_baseline.py` according to its
  discovered CLI before and after shared-foundation/final packets.
- Review final diff statistics, whitespace, route count, consumer counts,
  manifests, curator status, and implementation-control handoff.

No packet may claim a command passed unless its output was observed in that
packet.

## Security, Privacy, and Reliability Notes

- The work adds no authentication, permissions, user accounts, forms,
  analytics, or personal-data collection.
- External project links must retain safe `target`/`rel` behavior.
- Interactive gallery/library enhancements must not inject untrusted HTML.
- Route/source metadata must be validated as repository-controlled data.
- Source drift and manifest mismatch fail closed.
- No skill may write to upstream or deploy by implication.
- The most likely reliability failure is partial migration: new and old width
  systems coexisting indefinitely. The route ledger, consumer counts, cleanup
  gate, and final QA packet address this explicitly.
- The most likely design failure is replacing fixed boxes with unbounded long
  lines. The width taxonomy separates fluid outer layout from readable inner
  measures.

## Risks and Mitigations

| Risk | Likelihood/impact | Mitigation |
| --- | --- | --- |
| Current dirty packet is overwritten | Medium / high | `GATE-00`; no runtime edits before authorized checkpoint; preserve unrelated changes. |
| Upstream drift changes claim meaning | High / high for affected routes | `SRC-01` clean checkout; resolve critical claim-status drift first. |
| Template system becomes rigid | Medium / high | Mandatory/recommended/conditional distinction; rationale-based validator; slot composition. |
| Template system becomes too abstract | Medium / medium | Build primitives only when the pilot or second consumer proves reuse; use scope alarms. |
| Fluid layout produces unreadable text | Medium / high | Explicit `prose` measure and browser line-length review. |
| Ultra-wide layout becomes sparse or theatrical | Medium / medium | Grid spans, optional selective wide ceiling, and 1920px pilot review. |
| Removing borders destroys hierarchy | Medium / medium | Replace with spacing, bands, alignment, rules, and real object containers; compare screenshots. |
| Resource pages violate source-authority rule | Medium / high | Resource template contract plus existing layout validator. |
| Legacy routes are accidentally deleted | Medium / high | `LEGACY-01` evidence gate, redirects, inbound-link and provenance checks, owner decision. |
| CSS migration regresses unrelated routes | High / medium | Compatibility phase, one-route packets, representative matrix, final consumer audit. |
| Gallery enhancement harms no-script/accessibility | Low–medium / high | Static-first baseline; simplest interaction; keyboard/focus/escape/fallback criteria. |
| Visual work expands into content rewriting | Medium / high | Preserve-copy constraint; source bundle and diff review; separate content packet when needed. |
| Quality gate is bypassed because local page looks correct | Medium / high | Final `npm run validate` and `npm run quality`; report blockers without bypass. |

## Rollout and Rollback Plan

### Rollout

- No big-bang rewrite.
- One shared concern or one route per governed packet.
- Pilot first, then primary page families, then the remaining route queue.
- Human review status remains distinct from technical completion.
- Release readiness does not imply push or deployment.

### Migration

- Add new primitives alongside old classes.
- Migrate a route, validate, capture QA, and checkpoint.
- Update route-family ledger and consumer counts.
- Retain compatibility selectors until all consumers are proven migrated.
- Regenerate provenance/manifests only when relevant inputs change.

### Rollback

- Each packet reverts only its own template/route/control-record changes.
- Shared-token rollback restores the prior compatibility values without
  reverting already accepted unrelated work.
- A source-refresh rollback restores the prior accepted pin and generated
  artifacts as one coherent set; never mix hashes from two source commits.
- Route retirement rollback restores the page and removes its redirect only as
  a reviewed unit.
- Deployment rollback is outside this plan.

## Definition of Done

The program is complete only when:

- the `web-page` skill and its flexible templates are installed and validated;
- all 64 current routes have a recorded family/disposition;
- the governed modern route set uses the accepted fluid page system;
- each retained legacy route is either migrated by a follow-on packet or
  explicitly accepted as a justified exception;
- no general page shell depends on the legacy global fixed-width behavior;
- prose, media, data, and object containers use their intended width modes;
- source drift has no unresolved critical item for released routes;
- manifests/provenance/hashes are consistent;
- `npm run validate`, relevant Python tests, smoke tests, browser QA, and
  `npm run quality` pass against the accepted clean source binding;
- owner review status is recorded;
- no push or deployment has occurred without separate authorization.

## Final Review Checklist

- [x] Every PRD requirement is mapped to a task or a gated decision.
- [x] Every core task has acceptance criteria.
- [x] Every core task has validation guidance.
- [x] Risky source, layout, interaction, cleanup, and route changes have
  rollback notes.
- [x] This plan does not implement runtime code or the skill.
- [x] Commands are discovered from the repository.
- [x] Product questions are separated from implementation decisions.
- [x] Upstream source authority and website derivative status are explicit.
- [x] The current dirty implementation packet is preserved.
- [x] The templates are flexible guidance rather than canonical page markup.
- [x] All 64 current Astro routes are represented in the inventory or legacy
  disposition set.

## References

Carbon Design System. (n.d.). *2x grid overview*.
https://carbondesignsystem.com/elements/2x-grid/overview/

MDN Web Docs. (2025). *Responsive web design*.
https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design

MDN Web Docs. (2026). *CSS container queries*.
https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries

The AEther Flow Website. (2026a). `AGENTS.md` [Repository operating rules].

The AEther Flow Website. (2026b). *Sitewide greenfield foundation contract*
[Architecture contract].

The AEther Flow Website. (2026c). *Frontend recommendation* [Implementation
plan].

U.S. Web Design System. (n.d.-a). *Layout grid*.
https://designsystem.digital.gov/utilities/layout-grid/

U.S. Web Design System. (n.d.-b). *Card*.
https://designsystem.digital.gov/components/card/

World Wide Web Consortium. (2026a). *Understanding Success Criterion 1.4.10:
Reflow*. https://www.w3.org/WAI/WCAG22/Understanding/reflow.html

World Wide Web Consortium. (2026b). *C20: Using relative measurements to set
column widths so that lines can average 80 characters or less when the browser
is resized*. https://www.w3.org/WAI/WCAG22/Techniques/css/C20
