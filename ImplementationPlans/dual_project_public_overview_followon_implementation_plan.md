# Dual-Project Public Overview Follow-On Implementation Plan

Status: draft phased implementation plan
Date: 2026-06-25
Repository: The-AEther-Flow-Website
Source PRD: `PRDs/dual-project-public-overview-prd.md`
Primary skill: `project-explainer-frontend`

## 1. Analysis

The accepted public overview establishes the website's core public framing:
AEther Flow is a dual physics-and-AI research program. The productionized
overview already introduces the two first-class tracks, preserves source
authority language, uses the dark amber/graphite visual direction, and has a
final acceptance record.

The next problem is not to rebuild the overview. The next problem is to turn
the overview into a coherent public reading path. A reader who selects
"Explore physics research" or "Explore the AI research system" should land on
clear, source-boundary-safe pages that explain the selected track, identify
what is trusted, identify what remains open or upstream, and point to deeper
resources without inventing claims.

Conclusion: implementation should proceed as a sequence of bounded phases. Each
phase should be executable, reviewable, and independently verifiable. No phase
should silently pull in later pages, synchronization architecture, backend
services, or stronger scientific claims.

## 2. Guiding Principles

1. Preserve the accepted overview.
   The existing `/project/overview/` route is accepted. Do not reopen Variant
   B/C, query-parameter prototypes, or subjective hero art direction unless a
   later PRD explicitly authorizes that work.

2. Source authority remains upstream.
   Website pages may explain, organize, and link to reviewed source material.
   They must not create, strengthen, or reword scientific, mathematical,
   governance, or research-workflow claims beyond source support.

3. Work one phase at a time.
   Each phase has a stop condition. Do not start the next phase until the
   current phase passes its validation and is accepted.

4. Start broad, then deepen.
   First build the two track landing pages. Then build deeper pages by page
   family. This keeps the public reading path coherent while limiting claim
   risk.

5. Prefer existing Astro conventions.
   Use `src/pages`, `src/components`, `src/layouts`, `src/lib`, `src/styles`,
   and `public` as the repository already does. Do not add dependencies unless
   explicitly approved.

6. Treat visuals as presentation, not evidence.
   SVG/CSS diagrams can orient readers, but they do not establish scientific or
   workflow authority.

7. Verify by observable behavior.
   Test rendering, headings, links, responsive layout, source notices,
   reduced-motion behavior, and absence of overlap. Do not test animation
   internals as a release criterion.

## 3. Current Baseline

Current source pages:

- `src/pages/index.astro`
- `src/pages/project/overview.astro`
- `src/pages/research/map.astro`
- `src/pages/research/equations.mdx`
- `src/pages/research/math-sample.mdx`
- `src/pages/resources/index.astro`
- `src/pages/resources/documents.astro`
- `src/pages/resources/diagrams.astro`

Accepted production route:

- `/project/overview/`

Relevant shared implementation surfaces:

- `src/components/SourceNotice.astro`
- `src/layouts/BaseLayout.astro`
- `src/layouts/TechnicalPageLayout.astro`
- `src/styles/global.css`
- `src/styles/math.css`
- `src/lib/siteContent.ts`

Existing verification commands:

- `make quality`
- `npm run build`
- `python .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict`
- `python scripts/smoke_test_site.py --base-url http://127.0.0.1:<port>`

## 4. Target Public Reading Path

The finished follow-on path should support this sequence:

1. General reader enters `/project/overview/`.
2. Reader chooses a first-class track:
   - Physics Research
   - AI Research-Agent System
3. Reader lands on a track page that explains:
   - what the track is,
   - what source material supports it,
   - what claim status applies,
   - what is open, gated, or upstream,
   - where to go next.
4. Reader can continue into deeper source-backed pages only when those pages
   have their own provenance and validation.

Recommended route map:

| Route | Purpose | Initial status |
| --- | --- | --- |
| `/project/overview/` | Accepted dual-track overview | Done |
| `/project/physics/` | Physics track landing page | Planned Phase 2 |
| `/project/ai-research-agent-system/` | AI research-agent track landing page | Planned Phase 2 |
| `/project/source-authority/` | Public trust and source-boundary page | Planned Phase 3 |
| `/project/physics/ontology/` | AEther / AEther-flow ontology explainer | Planned Phase 4A |
| `/project/physics/exact-gr-benchmark/` | Exact-GR benchmark boundary explainer | Planned Phase 4B |
| `/project/physics/gr-derivation-roadmap/` | Open GR-derivation roadmap | Planned Phase 4C |
| `/project/physics/claim-gates/` | Claim gates, no-go records, and obstruction discipline | Planned Phase 4D |
| `/project/ai-research-agent-system/workflow/` | Research-agent workflow explainer | Planned Phase 5A |
| `/project/ai-research-agent-system/roles-and-skills/` | Role contracts and governed skills | Planned Phase 5B |
| `/project/ai-research-agent-system/memory-registries/` | Source-first memory, wiki, and registries | Planned Phase 5C |
| `/project/ai-research-agent-system/validator-operator-workflow/` | Validation and operator workflow | Planned Phase 5D |

## 5. Cross-Phase Acceptance Rules

Every implementation phase that edits website code must satisfy:

1. Page contract:
   - one clear `h1`;
   - accessible section headings;
   - meaningful internal and external links;
   - visible source authority or claim-status language;
   - no fake routes unless visibly marked as planned;
   - no overclaiming of GR derivation, ontology status, AI autonomy, or
     workflow authority.

2. Visual contract:
   - no text overlap on desktop or mobile;
   - readable typography;
   - no blue/cyan-dominant return for the overview family;
   - reduced-motion behavior preserved for animated elements.

3. Source contract:
   - inspect relevant upstream files before writing public claims;
   - cite source materials in APA 7 style inside PRDs/plans when cited;
   - preserve qualifiers such as `open`, `source authority`, `explanatory`,
     `generated noncanonical`, `reviewed`, `draft/control`, `proposal-only`,
     and `human-gated` where applicable.

4. Verification contract:
   - run the repository checks appropriate to the phase;
   - run strict project-explainer audit for built public pages;
   - capture Playwright desktop/mobile screenshots for new or materially
     changed public routes;
   - keep browser artifacts under `output/playwright/`.

5. Stop condition:
   - after a phase passes validation, stop and report results;
   - do not begin the next phase without explicit authorization.

## 6. Phase Plan

### Phase 0 - Evidence Refresh and Scope Audit

Purpose:
Establish the current source and website baseline before adding new pages.
This phase is audit-only.

Inputs:

- `PRDs/dual-project-public-overview-prd.md`
- `src/pages/project/overview.astro`
- `src/components/SourceNotice.astro`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/README.md`
- Relevant upstream GitHub-facing explainers listed by the source README.

Actions:

1. Run the project-explainer scanner:

   ```bash
   python .codex/skills/project-explainer-frontend/scripts/scan_project_story.py \
     --repo . \
     --source-root /Volumes/P-SSD/AngryOwl/The-AEther-Flow \
     --out-dir scratch/project-explainer
   ```

2. Read:
   - `scratch/project-explainer/project_story_brief.md`
   - `scratch/project-explainer/project_story_brief.json`

3. Inspect current routes under `src/pages`.

4. Inspect the upstream source README sections for:
   - two-track project framing;
   - physics benchmark and open derivation boundary;
   - AI research-agent system wording;
   - public explainer inventory.

5. Produce an audit note identifying:
   - existing routes;
   - missing routes required by the PRD reading path;
   - source files that must be inspected before Phase 2 copy;
   - any route naming concerns.

Files likely touched:

- Prefer no tracked code changes.
- Optional tracked audit if desired: `docs/quality/dual-project-public-overview-phase0-audit.md`.

Validation:

- `git status --short`
- No page implementation changes.

Stop condition:

- Phase 0 audit accepted.
- Explicit authorization received for Phase 1.

### Phase 1 - Information Architecture and Shared Content Contract

Purpose:
Define reusable route metadata, page content boundaries, and shared components
before building new routes.

Inputs:

- Phase 0 audit.
- Accepted overview PRD.
- Existing `src/lib/siteContent.ts`.
- Existing `SourceNotice` component.

Actions:

1. Decide the exact public routes for the first page family:
   - `/project/physics/`
   - `/project/ai-research-agent-system/`
   - `/project/source-authority/`

2. Create or extend shared route/content data in `src/lib` so page labels,
   descriptions, planned child pages, and source notices are not duplicated
   unnecessarily.

3. Define page-level source notice defaults:
   - `claimStatus`;
   - `updated`;
   - short source-boundary note;
   - optional source references.

4. Decide whether the current global navigation should add a `Project` or
   `Tracks` grouping now, or defer navigation changes until Phase 7.

5. Identify any small reusable components needed for:
   - track cards;
   - planned route chips;
   - source-boundary panels;
   - page-family next-step lists.

Files likely touched:

- `src/lib/siteContent.ts`
- `src/components/*.astro` if a reusable component is justified.
- No route pages unless needed for type/build validation.

Validation:

- `npm run build`
- `make quality` if TypeScript/Python validation surfaces are affected.

Stop condition:

- Shared content contract is accepted.
- No public page is created yet unless the change is required for safe
  validation.

### Phase 2 - Two First-Class Track Landing Pages

Purpose:
Build the two primary pages that the overview promises:
Physics Research and AI Research-Agent System.

Routes:

- `/project/physics/`
- `/project/ai-research-agent-system/`

Physics page required content:

1. Plain-language definition of the physics track.
2. Clear statement that the GR derivation remains open.
3. Distinction between:
   - AEther / AEther-flow ontology;
   - Exact-GR benchmark boundary;
   - open derivation burden;
   - no-go / obstruction records.
4. Links to current real resources, or visibly planned links where a route is
   not built yet.
5. Source authority notice with claim status.

AI research-agent page required content:

1. Plain-language definition of the AI research-agent system.
2. Distinction between AI-methodology claims and physics proof.
3. Explanation of:
   - bounded tasks;
   - role contracts;
   - claim gates;
   - review/refutation discipline;
   - source-first memory, wiki, and registries.
4. Link to the upstream source repository.
5. Source authority notice with claim status.

Overview updates:

- Update the overview CTAs so:
  - "Explore physics research" points to `/project/physics/`.
  - "Explore the AI research system" points to `/project/ai-research-agent-system/`.
- Keep an external GitHub link available from the AI page rather than making
  the overview jump directly out of the site.

Files likely touched:

- `src/pages/project/physics/index.astro`
- `src/pages/project/ai-research-agent-system/index.astro`
- `src/pages/project/overview.astro`
- `src/lib/siteContent.ts`
- `src/styles/global.css`

Validation:

- `npm run build`
- `python .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict`
- `make quality`
- Local preview:

  ```bash
  npm run preview -- --host 127.0.0.1 --port 4327
  python scripts/smoke_test_site.py --base-url http://127.0.0.1:4327
  ```

- Playwright desktop/mobile screenshots for:
  - `/project/overview/`
  - `/project/physics/`
  - `/project/ai-research-agent-system/`

Stop condition:

- Track landing pages pass validation and visual review.
- Do not implement deeper physics or AI pages in this phase.

### Phase 3 - Public Source Authority Page

Purpose:
Add a public trust page explaining how readers should treat source authority,
generated derivatives, website pages, and upstream source records.

Route:

- `/project/source-authority/`

Required content:

1. Define the Source Authority Boundary for public readers.
2. Explain what website pages can and cannot establish.
3. Explain how to read generated/public material without treating it as
   canonical science or workflow authority.
4. Link back to:
   - overview;
   - physics track;
   - AI research-agent track;
   - resources.
5. Include visible claim status and source notice.

Files likely touched:

- `src/pages/project/source-authority/index.astro`
- `src/lib/siteContent.ts`
- `src/pages/project/overview.astro` only if adding a source-authority link.
- `src/styles/global.css`

Validation:

- `npm run build`
- strict project-explainer audit
- `make quality`
- desktop/mobile screenshots for `/project/source-authority/`

Stop condition:

- Source authority page accepted.
- No synchronization workflow is implemented in this phase.

### Phase 4 - Physics Deep-Dive Page Family

Purpose:
Build the physics reader path one page at a time. Each subphase is separately
authorized and independently verified.

Shared physics constraints:

- Do not claim GR has been derived.
- Do not present the ontology as established physics.
- Preserve the distinction between benchmark compatibility and derivation.
- Use source-backed language and visible source notices.

#### Phase 4A - Ontology Page

Route:

- `/project/physics/ontology/`

Required content:

- Explain AEther / AEther-flow as the current research ontology.
- State that it is an explanatory frame and research ontology, not an accepted
  derivation of GR.
- Link back to the physics track page.

Validation:

- Build, audit, quality gate.
- Desktop/mobile screenshots for the new page.

Stop condition:

- Ontology page accepted.

#### Phase 4B - Exact-GR Benchmark Boundary Page

Route:

- `/project/physics/exact-gr-benchmark/`

Required content:

- Explain the benchmark boundary in plain language.
- State that observable-scale behavior remains ordinary GR under the current
  benchmark framing.
- State that benchmark compatibility is not first-principles derivation.

Validation:

- Build, audit, quality gate.
- Desktop/mobile screenshots for the new page.

Stop condition:

- Exact-GR benchmark page accepted.

#### Phase 4C - GR Derivation Roadmap Page

Route:

- `/project/physics/gr-derivation-roadmap/`

Required content:

- Explain the open derivation burden.
- Identify the effective Lorentzian metric generation milestone only if
  supported by inspected source material.
- Present roadmap status as explanatory, not as proof.

Validation:

- Build, audit, quality gate.
- Desktop/mobile screenshots for the new page.

Stop condition:

- GR derivation roadmap page accepted.

#### Phase 4D - Claim Gates and Obstructions Page

Route:

- `/project/physics/claim-gates/`

Required content:

- Explain claim gates, negative results, no-go records, obstruction records,
  and freeze criteria at a public-reader level.
- Preserve stopped or blocked status without reinterpreting it as success.
- Link to source authority and AI research-agent workflow where relevant.

Validation:

- Build, audit, quality gate.
- Desktop/mobile screenshots for the new page.

Stop condition:

- Physics page family accepted as a coherent first version.

### Phase 5 - AI Research-Agent Deep-Dive Page Family

Purpose:
Build the AI research-agent reader path one page at a time. Each subphase is
separately authorized and independently verified.

Shared AI constraints:

- Do not present the AI system as autonomous beyond source support.
- Distinguish workflow/methodology claims from physics proof.
- Keep operational metrics and validator passes separate from scientific truth.
- Preserve human accountability for public release and authorship.

#### Phase 5A - Research-Agent Workflow Page

Route:

- `/project/ai-research-agent-system/workflow/`

Required content:

- Explain how bounded tasks, Director decisions, AgentJobs, completions, and
  handoffs work at a public-reader level.
- Avoid internal-only routing detail unless needed for comprehension.

Validation:

- Build, audit, quality gate.
- Desktop/mobile screenshots for the new page.

Stop condition:

- Workflow page accepted.

#### Phase 5B - Roles and Skills Page

Route:

- `/project/ai-research-agent-system/roles-and-skills/`

Required content:

- Explain role contracts and governed skills.
- State that role/skill existence does not expand current authority or
  task-local allowlists.
- Link to source authority.

Validation:

- Build, audit, quality gate.
- Desktop/mobile screenshots for the new page.

Stop condition:

- Roles and skills page accepted.

#### Phase 5C - Memory and Registries Page

Route:

- `/project/ai-research-agent-system/memory-registries/`

Required content:

- Explain source-first memory, wiki surfaces, registries, and retrieval limits.
- State that memory/wiki/semantic extracts support retrieval and orientation;
  they do not override tracked source authority.

Validation:

- Build, audit, quality gate.
- Desktop/mobile screenshots for the new page.

Stop condition:

- Memory and registries page accepted.

#### Phase 5D - Validator and Operator Workflow Page

Route:

- `/project/ai-research-agent-system/validator-operator-workflow/`

Required content:

- Explain validation, deterministic checks, documentation impact, and operator
  workflow at a public-reader level.
- State that validator success is not a scientific verdict.

Validation:

- Build, audit, quality gate.
- Desktop/mobile screenshots for the new page.

Stop condition:

- AI research-agent page family accepted as a coherent first version.

### Phase 6 - Resources and Manifest Alignment

Purpose:
Make resource pages support the new public reading path without pretending
sample fixtures are real scientific sources.

Actions:

1. Audit `public/files/manifests/source_manifest.json`.
2. Identify which current assets are scaffold fixtures and which are real
   source-backed public assets.
3. Update `/resources/`, `/resources/documents/`, and `/resources/diagrams/`
   so they point readers toward relevant public pages and clearly label sample
   or planned resources.
4. Add real downloadable assets only if source provenance and approval status
   are available.

Files likely touched:

- `public/files/manifests/source_manifest.json`
- `public/files/manifests/source_manifest.schema.json` only if schema changes
  are required and approved.
- `src/pages/resources/index.astro`
- `src/pages/resources/documents.astro`
- `src/pages/resources/diagrams.astro`
- `src/lib/manifests.ts`

Validation:

- `npm run validate:manifests`
- `npm run build`
- strict project-explainer audit
- `make quality`
- screenshots for changed resources pages.

Stop condition:

- Resource pages accurately distinguish real, sample, and planned material.
- No source-to-website automation is implemented in this phase.

### Phase 7 - Navigation, Cross-Linking, and Reader Flow

Purpose:
Connect the overview, track pages, deep-dive pages, and resources into a
coherent navigational system.

Actions:

1. Review global navigation.
2. Decide whether to add:
   - a `Project` section;
   - track subnavigation;
   - breadcrumbs;
   - related-page cards;
   - "Where to go next" sections.
3. Update links so no public CTA points to a fake or unmarked future route.
4. Ensure external GitHub links are clearly distinguishable from internal site
   pages.

Files likely touched:

- `src/layouts/BaseLayout.astro`
- `src/components/*.astro`
- `src/lib/siteContent.ts`
- page files that need related links.
- `src/styles/global.css`

Validation:

- `npm run build`
- `python scripts/smoke_test_site.py --base-url http://127.0.0.1:<port>`
- strict project-explainer audit
- `make quality`
- desktop/mobile screenshots for representative pages.

Stop condition:

- Reader can move from overview to either track, to deeper pages, to source
  authority, and back without dead ends.

### Phase 8 - Visual System and Accessibility Hardening

Purpose:
Polish the public page family after the core information architecture exists.

Actions:

1. Review typography scale across overview, track pages, and deep pages.
2. Confirm mobile spacing and no-overlap behavior.
3. Confirm focus states and keyboard navigation for links/details controls.
4. Confirm reduced-motion behavior across animated SVG/CSS elements.
5. Keep visuals aligned with the dark amber/graphite overview direction without
   making every page visually identical.
6. Avoid adding new dependencies.

Files likely touched:

- `src/styles/global.css`
- page-local SVG/CSS structures if needed.

Validation:

- `npm run build`
- strict project-explainer audit
- `make quality`
- Playwright screenshots across:
  - desktop;
  - mobile;
  - selected scrolled states;
  - reduced-motion checks.

Stop condition:

- Objective visual and accessibility release standard passes.
- Taste-level refinements are documented as follow-on work, not blockers.

### Phase 9 - Full Release QA and Acceptance Record

Purpose:
Close the public page family as a release packet.

Actions:

1. Run full repository quality:

   ```bash
   make quality
   ```

2. Run strict project-explainer audit:

   ```bash
   python .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py \
     --site dist \
     --out-dir scratch/project-explainer \
     --strict
   ```

3. Run local preview and route smoke test:

   ```bash
   npm run preview -- --host 127.0.0.1 --port 4327
   python scripts/smoke_test_site.py --base-url http://127.0.0.1:4327
   ```

4. Capture desktop/mobile screenshots for all new and materially changed
   public routes.

5. Verify:
   - one `h1` per page;
   - meaningful links;
   - no fake unmarked routes;
   - source notices;
   - reduced motion;
   - no mobile overlap;
   - no overclaims.

6. Add a dated acceptance section either to this implementation plan or a
   follow-on release record.

Files likely touched:

- `ImplementationPlans/dual_project_public_overview_followon_implementation_plan.md`
- Maybe `PRDs/dual-project-public-overview-prd.md` only if the accepted PRD is
  explicitly being used as the release record for this new packet.

Validation:

- `make quality`
- strict audit
- smoke test
- screenshot review
- `git diff --check`

Stop condition:

- Release packet accepted and ready to commit.

Acceptance record - 2026-06-25:

- Scope: 19 rendered HTML routes and 23 smoke-tested routes covering the home
  page, project overview, physics track, physics deep pages, AI
  research-agent track, AI deep pages, source authority, research support pages,
  resources, document samples, and diagram assets.
- Repository quality passed with `make quality`, including manifest validation,
  content source validation, Astro build, Python tests, Ruff, and mypy.
- Strict project-explainer audit passed with:

  ```bash
  python .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py \
    --site dist \
    --out-dir scratch/project-explainer \
    --strict
  ```

- Local preview and route smoke test passed with:

  ```bash
  npm run preview -- --host 127.0.0.1 --port 4327
  python scripts/smoke_test_site.py --base-url http://127.0.0.1:4327
  ```

- Browser release QA passed across 19 routes at desktop `1440x1100` and mobile
  `390x900`, with 40 screenshots written under
  `output/playwright/release-phase9-*-2026-06-25.png`.
- Browser QA verified one `h1` per page, meaningful link text or labels, no
  `/planned`, `/todo`, or `/coming-soon` route placeholders, source-authority
  and claim-status notices where required, reduced-motion compliance for
  project pages, no horizontal mobile overflow, complete image loads, and no
  positive overclaim patterns.
- Representative screenshot review covered desktop overview, mobile overview,
  source-authority scrolled view, and mobile resources. No layout overlap or
  source-boundary defect was observed.
- Result: Phase 9 release packet is locally accepted and ready to commit.
- Boundary: Phase 10 deployment was not started.

### Phase 10 - Push, Deploy, and Post-Deploy Verification

Purpose:
Publish the accepted page family only after local release QA passes.

Actions:

1. Push the accepted commit.
2. Confirm Cloudflare Pages or the selected deployment target builds the site.
3. Smoke-test deployed routes.
4. Compare deployed desktop/mobile appearance against local screenshots.
5. Record deployment URL and any deployment-specific issues.

Validation:

- Deployment build succeeds.
- Public routes return expected status.
- Source authority language is visible on deployed pages.

Stop condition:

- Deployment verified.
- Any deployment defect becomes a new bounded fix phase.

## 7. Phase Ordering Rule

The phases must be executed in order unless a later explicit decision revises
the plan:

1. Phase 0 - Evidence Refresh and Scope Audit
2. Phase 1 - Information Architecture and Shared Content Contract
3. Phase 2 - Two First-Class Track Landing Pages
4. Phase 3 - Public Source Authority Page
5. Phase 4A - Ontology Page
6. Phase 4B - Exact-GR Benchmark Boundary Page
7. Phase 4C - GR Derivation Roadmap Page
8. Phase 4D - Claim Gates and Obstructions Page
9. Phase 5A - Research-Agent Workflow Page
10. Phase 5B - Roles and Skills Page
11. Phase 5C - Memory and Registries Page
12. Phase 5D - Validator and Operator Workflow Page
13. Phase 6 - Resources and Manifest Alignment
14. Phase 7 - Navigation, Cross-Linking, and Reader Flow
15. Phase 8 - Visual System and Accessibility Hardening
16. Phase 9 - Full Release QA and Acceptance Record
17. Phase 10 - Push, Deploy, and Post-Deploy Verification

Do not collapse multiple page-family phases into one broad implementation run.
If a phase reveals missing source support, stop and either narrow the page copy
or create a source/provenance follow-up before proceeding.

## 8. Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Website copy overstates physics status | Scientific authority drift | Inspect upstream source files; preserve open-derivation boundary; use source notices. |
| AI system page implies autonomous capability beyond source support | Methodology overclaim | Use "AI research-agent system" and human-accountability language; separate workflow from proof. |
| Too many pages built at once | Review and QA failure | Execute one bounded phase or subphase at a time. |
| Public CTAs point to fake routes | Reader trust failure | Mark planned routes visibly or defer links until routes exist. |
| Visual system becomes inconsistent | Brand and usability drift | Reuse overview tokens and components; QA desktop/mobile screenshots. |
| Resource pages list scaffold samples as real research material | Provenance confusion | Audit manifests; label sample/planned/real assets clearly. |
| Validators pass but page quality is weak | Release quality gap | Add browser screenshots and manual objective release review. |
| Deployment differs from local preview | Production defect | Post-deploy smoke test and screenshot comparison. |

## 9. Definition of Done for the Full Plan

The full plan is done when:

1. The accepted overview remains stable.
2. The two track landing pages exist and are source-boundary safe.
3. The source-authority page exists or an explicit decision defers it.
4. Physics deep-dive pages exist in the planned route family, each with source
   notices and no derivation overclaim.
5. AI research-agent deep-dive pages exist in the planned route family, each
   separating workflow claims from physics proof.
6. Resource pages accurately label real, sample, and planned materials.
7. Navigation lets public readers move through the site without dead ends.
8. Desktop and mobile QA evidence exists for all new or materially changed
   public routes.
9. Reduced-motion behavior is verified.
10. `make quality` and strict project-explainer audit pass.
11. A final acceptance record lists commands, results, and screenshot paths.
12. The accepted release is committed, pushed if authorized, and deployment is
    verified if deployment is in scope.

## 10. References

AEther-Flow Project. (2026). `README.md` [Project front door, dual-track
research-program framing, source authority, physics benchmark boundary, open
derivation burden, and AI research-agent system overview].

The AEther Flow Website. (2026). `PRDs/dual-project-public-overview-prd.md`
[Accepted dual-project public overview PRD and release acceptance record].

The AEther Flow Website. (2026). `src/pages/project/overview.astro`
[Productionized public overview route].

The AEther Flow Website. (2026). `src/components/SourceNotice.astro`
[Website source-authority notice component].

The AEther Flow Website. (2026).
`.codex/skills/project-explainer-frontend/SKILL.md`
[Project explainer frontend workflow and source-authority boundary].
