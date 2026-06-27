# Public Comprehension And Diagram System Task Packets

Date: 2026-06-27

Source PRD: `PRDs/public-comprehension-and-diagram-system-prd.md`

Companion plan:
`ImplementationPlans/public_comprehension_and_diagram_system_implementation_plan.md`

## Shared Context For All Tasks

Repository: `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website`

This repository is the reader-facing website for
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`. Upstream source files, registries,
and governed task records remain authoritative for scientific, mathematical,
governance, validator, routing, memory, and workflow claims.

Global constraints:

- Keep this work source-derived. Do not invent scientific, mathematical,
  governance, or research-workflow claims in website code.
- Keep internal website routes as the primary reader journey; source and GitHub
  links are provenance or inspection links.
- Do not add Mermaid as a public browser runtime dependency.
- Do not deploy unless explicitly authorized.
- Create or update content dossiers before rewriting public pages.
- Regenerate page provenance after page-source changes.
- Regenerate asset manifests after public diagram asset changes.
- Preserve the command-interface visual language from the sibling PRD.
- Preserve animated SVG policy for SVG artwork: no visible embedded SVG text.
- Be aware the worktree may contain user changes. Do not revert unrelated work.

Common validation commands discovered from the repository:

```bash
npm run build
npm run validate
npm run quality
npm run validate:manifests
npm run validate:content
npm run validate:links
npm run validate:layout
npm run validate:svg
npm run validate:provenance
npm run validate:curator
npm run validate:cloudflare
python3 -m pytest
python3 scripts/generate_page_provenance.py --write
python3 scripts/build_asset_manifest.py --write
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

`npm run validate:comprehension` is proposed by this plan. Use it only after
the task that adds the command.

## Task 1: Add Dossier Template And Comprehension Review Contract

### Goal

Create the maintainer-facing content-dossier structure and review contract that
future page rewrites must use.

### Context

- PRD requirements: REQ-001, REQ-013, REQ-020, NFR-002, NFR-004
- Relevant files or directories:
  - `docs/content-dossiers/`
  - `docs/quality/`
  - `PRDs/public-comprehension-and-diagram-system-prd.md`
  - `docs/project-features-and-functionality.md`
- Existing patterns to follow:
  - Repository docs under `docs/` are maintainer-facing, not public
    navigation.
  - Existing QA notes live under `docs/quality/`.

### Constraints

- Do not change public routes in this task.
- Do not add diagram assets yet.
- Do not treat a dossier as source authority.
- Keep the template practical enough for repeated use.

### Implementation Notes

- Add `docs/content-dossiers/README.md` describing the dossier workflow.
- Add `docs/content-dossiers/_template.md` with required sections:
  - route and reader job,
  - current page summary,
  - upstream source basis,
  - source-derived topic outline,
  - glossary,
  - claim boundaries and forbidden implications,
  - required comprehension blocks,
  - diagram contract,
  - equation walkthrough contract,
  - safe/unsafe summaries,
  - new-page audit,
  - human review checklist.
- Add or update a quality note under `docs/quality/` explaining the public
  comprehension review standard.
- The template may include examples, but avoid page-specific claims unless
  clearly marked as examples.

### Acceptance Criteria

- [ ] `docs/content-dossiers/README.md` explains the workflow and source
      authority boundary.
- [ ] `docs/content-dossiers/_template.md` contains all required PRD dossier
      fields.
- [ ] Human review remains explicit and cannot be replaced by script PASS.
- [ ] No public route, public asset, or manifest is changed.

### Validation

```bash
npm run build
```

Optional structural check:

```bash
rg -n "Route and reader job|Claim boundaries|Safe summary|Unsafe summary|Human review" docs/content-dossiers
```

### Done When

The repository has a reusable content-dossier template and a documented
comprehension review contract ready for pilot dossiers.

## Task 2: Create Phase 1 Pilot Content Dossiers

### Goal

Create source-grounded dossiers for `/project/overview/` and
`/project/ai-research-agent-system/parent-child-synthesis/` before public page
rewrites.

### Context

- PRD requirements: REQ-001, REQ-003, REQ-004, REQ-007, REQ-016, REQ-020
- Relevant files or directories:
  - `docs/content-dossiers/_template.md`
  - `docs/content-dossiers/project-overview/dossier.md`
  - `docs/content-dossiers/parent-child-synthesis/dossier.md`
  - `src/pages/project/overview.astro`
  - `src/lib/internalExplainers.ts`
  - `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro`
  - `public/files/manifests/page_route_map.json`
- Existing patterns to follow:
  - `page_route_map.json` lists upstream sources for both pilot routes.
  - `SourceNotice` and source refs should keep source authority visible.

### Constraints

- Do not rewrite public pages in this task.
- Verify source paths before relying on them.
- Do not quote large source passages into dossiers; summarize and cite paths.
- Keep dossiers outside public navigation.

### Implementation Notes

- Copy the template for both pilot routes.
- For the overview dossier, map the PRD-required two-track framing:
  physics track, AI research-agent track, source authority, and reader route
  families.
- For the parent-child dossier, map:
  one Director decision, one outer AgentJob, one execution-role record, one
  completion record, one fused output, child `draft/control` status, inherited
  authority, blocking conflict behavior, and scope limits.
- Record Mermaid source paths and generated PNG paths planned for TASK-4.
- Include safe/unsafe summaries for both pilots, especially parent-child
  synthesis.
- Record human review criteria for each pilot route.

### Acceptance Criteria

- [ ] Both pilot dossiers exist and are complete enough to guide page edits.
- [ ] Each dossier identifies source basis, claim boundaries, glossary terms,
      diagram requirements, safe/unsafe summaries, and review checklist.
- [ ] Each dossier names the public route and reader job.
- [ ] No public page source is changed.

### Validation

```bash
npm run build
```

Optional structural check:

```bash
rg -n "one outer AgentJob|two-track|Safe summary|Unsafe summary|Mermaid source" docs/content-dossiers
```

### Done When

The two Phase 1 pilot pages have source-grounded dossiers that can be used as
the editorial contract for implementation.

## Task 3: Add Reusable Comprehension Content Model

### Goal

Add a small reusable content model and component support for richer
source-derived page explanations without hard-coding both pilot pages as
one-offs.

### Context

- PRD requirements: REQ-002, REQ-007, REQ-008, REQ-016, REQ-018, NFR-001,
  NFR-005
- Relevant files or directories:
  - `src/lib/internalExplainers.ts`
  - `src/lib/siteContent.ts`
  - `src/components/InternalExplainerPage.astro`
  - `src/components/CommandBand.astro`
  - `src/components/EvidenceRail.astro`
  - `src/components/StatusDossier.astro`
  - `src/components/Figure.astro`
  - `src/components/EquationBlock.astro`
  - optional new `src/lib/comprehensionContent.ts`
  - optional new `src/components/ComprehensionBlocks.astro`
- Existing patterns to follow:
  - Astro components are prop-driven and small.
  - Visual grammar already uses command bands, rails, and dossiers.
  - Current `InternalExplainer` data is too compressed for all PRD blocks.

### Constraints

- Do not add a broad content CMS or runtime data loader.
- Do not encode scientific claims in generic components.
- Do not break existing pages that use `InternalExplainerPage`.
- Keep the model flexible; not every route needs every block.

### Implementation Notes

- Add or extend TypeScript interfaces for:
  - context blocks,
  - plain summaries,
  - mechanism steps,
  - term groups,
  - source-basis entries,
  - boundary blocks,
  - diagram metadata,
  - equation walkthroughs,
  - safe/unsafe summaries,
  - related internal routes.
- Update `InternalExplainerPage.astro` or introduce a thin
  `ComprehensionBlocks.astro` component that renders only blocks present in the
  data.
- Extend `Figure.astro` only if needed for richer provenance or constrained
  diagram presentation.
- Extend `EquationBlock.astro` to support walkthrough text when actual public
  page equations are present.
- Preserve existing routes during the model introduction.

### Acceptance Criteria

- [ ] A reusable comprehension content shape exists.
- [ ] Existing pages still build.
- [ ] Components render optional blocks without empty shells.
- [ ] The model can represent overview and parent-child pilot needs.
- [ ] No public scientific or workflow claims are strengthened by component
      code.

### Validation

```bash
npm run build
npm run validate:layout
npm run validate:svg
```

If TypeScript or component tests are affected:

```bash
python3 -m pytest
```

### Done When

The codebase can represent the PRD's comprehension blocks in reusable Astro
and TypeScript surfaces without changing public copy yet.

## Task 4: Add Static Mermaid Diagram Pipeline And Phase 1 Diagrams

### Goal

Create the Phase 1 Mermaid sources, generate static PNG diagram assets, and
record them in manifests without adding public Mermaid runtime rendering.

### Context

- PRD requirements: REQ-005, REQ-006, REQ-015, REQ-017, NFR-001, NFR-003,
  NFR-005
- Relevant files or directories:
  - `docs/content-dossiers/project-overview/diagrams/`
  - `docs/content-dossiers/parent-child-synthesis/diagrams/`
  - `public/assets/diagrams/comprehension/`
  - `public/files/manifests/source_manifest.json`
  - `public/files/manifests/asset_manifest.json`
  - optional `scripts/render_mermaid_diagrams.py`
  - `src/components/Figure.astro`
- Existing patterns to follow:
  - `public/assets/diagrams/publication-layer-map.svg` is already manifest
    backed.
  - `scripts/build_asset_manifest.py --write` derives asset hashes from
    `source_manifest.json`.

### Constraints

- No public Mermaid runtime dependency.
- Default output is PNG.
- Do not satisfy this PRD with inline SVG containing visible text.
- Diagrams must have alt text, captions, and nearby explanatory prose when
  used on public pages.
- If adding a dev dependency, justify it as build-time only.

### Implementation Notes

- Add Mermaid source files:
  - `docs/content-dossiers/project-overview/diagrams/two-track-project-map.mmd`
  - `docs/content-dossiers/parent-child-synthesis/diagrams/single-outer-agentjob-frame.mmd`
- Add generated PNG targets:
  - `public/assets/diagrams/comprehension/project-overview-two-track-map.png`
  - `public/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png`
- Add or document the render command.
- Add source-manifest entries for both PNGs with `kind: "diagram"` and notes
  that they are explanatory public diagrams, not source authority.
- Run `python3 scripts/build_asset_manifest.py --write`.
- Check that public route code does not import or initialize Mermaid runtime.

### Acceptance Criteria

- [ ] Phase 1 Mermaid `.mmd` files are tracked in dossier directories.
- [ ] Phase 1 PNG diagram assets exist under
      `public/assets/diagrams/comprehension/`.
- [ ] `source_manifest.json` and `asset_manifest.json` include both diagrams.
- [ ] Diagram assets have source refs and valid hashes.
- [ ] No public page loads Mermaid runtime code.

### Validation

```bash
python3 scripts/build_asset_manifest.py --write
npm run validate:manifests
npm run build
```

After TASK-05:

```bash
npm run validate:comprehension
```

### Done When

The Phase 1 diagram pipeline is reproducible, static, manifest-backed, and
ready for public page use.

## Task 5: Add Public Comprehension Audit Command

### Goal

Add a conservative scripted audit for remediated public pages while keeping
human review as a required part of the gate.

### Context

- PRD requirements: REQ-006, REQ-007, REQ-008, REQ-013, REQ-014, REQ-016,
  REQ-020, NFR-002, NFR-003
- Relevant files or directories:
  - `scripts/validate_public_comprehension.py`
  - `package.json`
  - `docs/content-dossiers/**`
  - `docs/quality/**`
  - `public/files/manifests/source_manifest.json`
  - `public/files/manifests/asset_manifest.json`
  - `src/pages/**`
  - `src/lib/**`
- Existing patterns to follow:
  - Existing validators are Python scripts with package scripts.
  - `scripts/validate_layout_language.py` validates a specific migration
    contract.

### Constraints

- Do not make scripted PASS stand in for human comprehension review.
- Avoid brittle full-prose assertions.
- Start with mechanical, high-signal checks.
- Do not add this command to `npm run validate` until the user accepts the
  gate's stability.

### Implementation Notes

- Add `scripts/validate_public_comprehension.py`.
- Add `validate:comprehension` to `package.json`.
- Check remediated routes declared in a small allowlist or config:
  - dossier file exists,
  - required headings exist,
  - diagram references include `.mmd`, PNG, alt, caption, and manifest id,
  - no public Mermaid runtime markers,
  - high-risk pages include safe/unsafe summary markers,
  - equation references have walkthrough markers,
  - human review note exists or is explicitly pending.
- Add Python tests for helper functions if practical.
- Keep errors actionable and path-specific.

### Acceptance Criteria

- [ ] `npm run validate:comprehension` exists.
- [ ] The command fails when a remediated route lacks a dossier or required
      diagram metadata.
- [ ] The command checks for no public Mermaid runtime.
- [ ] The command requires or reports human review status.
- [ ] The command is separate from `npm run validate` unless explicitly
      approved.

### Validation

```bash
npm run validate:comprehension
python3 -m pytest
npm run build
```

### Done When

The repository has an executable comprehension audit that supports, but does
not replace, human public-comprehension review.

## Task 6: Remediate `/project/overview/`

### Goal

Rewrite `/project/overview/` as the Phase 1 public-comprehension proof, using
the overview dossier and two-track static diagram.

### Context

- PRD requirements: REQ-002, REQ-003, REQ-005, REQ-007, REQ-014, REQ-015,
  REQ-016, REQ-017, REQ-018, REQ-020, NFR-001, NFR-002, NFR-005
- Relevant files or directories:
  - `docs/content-dossiers/project-overview/dossier.md`
  - `src/pages/project/overview.astro`
  - `src/lib/siteContent.ts`
  - `src/lib/comprehensionContent.ts` if added
  - `src/components/Figure.astro`
  - `src/components/SourceNotice.astro`
  - `public/assets/diagrams/comprehension/project-overview-two-track-map.png`
  - `public/files/manifests/page_provenance.json`
- Existing patterns to follow:
  - `overview.astro` already uses `CommandBand`, `EvidenceRail`,
    `StatusDossier`, and `SourceNotice`.
  - Overview links should stay internal-first.

### Constraints

- Do not claim completed GR derivation.
- Do not claim autonomous AI research ownership.
- Do not make GitHub the primary route for general readers.
- Do not remove source authority notice.
- Do not introduce public Mermaid runtime.

### Implementation Notes

- Start from the overview dossier.
- Make the page teach AEther Flow before presenting route choices.
- Add or reference the static two-track project map diagram with alt text,
  caption, and nearby explanatory prose.
- Explain:
  - physics track,
  - AI research-agent track,
  - how the two tracks co-develop,
  - website versus source authority,
  - what the website does not claim.
- Add definitions for specialized terms used on the page.
- Add a safe/unsafe summary block if the dossier marks it required.
- Keep route links internal and reader-job oriented.
- Regenerate page provenance after editing.

### Acceptance Criteria

- [ ] Overview opens with general-public context, not metadata.
- [ ] Overview explains both project tracks and source-authority boundary.
- [ ] Overview includes the static two-track diagram with alt text and caption.
- [ ] Related routes explain why to click them.
- [ ] Source links remain provenance, not primary navigation.
- [ ] Page provenance is regenerated.
- [ ] The page passes the comprehension audit and standard validators.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
npm run validate:comprehension
npm run validate:content
npm run validate:links
npm run validate:provenance
npm run validate:manifests
npm run build
```

Browser QA:

```bash
npm run dev -- --host 127.0.0.1 --port 4321
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

Capture desktop and mobile screenshots of `/project/overview/`.

### Done When

The overview page is dossier-backed, diagram-backed, source-boundary-safe, and
validated as the front-door pilot.

## Task 7: Remediate Parent-Child Synthesis

### Goal

Rewrite `/project/ai-research-agent-system/parent-child-synthesis/` as the
deep-topic pilot centered on the one-outer-AgentJob invariant.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-005, REQ-007, REQ-014, REQ-015,
  REQ-016, REQ-017, REQ-018, REQ-020, NFR-001, NFR-002, NFR-005
- Relevant files or directories:
  - `docs/content-dossiers/parent-child-synthesis/dossier.md`
  - `src/lib/internalExplainers.ts`
  - `src/components/InternalExplainerPage.astro`
  - `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro`
  - `public/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png`
  - `public/files/manifests/page_provenance.json`
- Existing patterns to follow:
  - The route currently renders via `InternalExplainerPage` and
    `internalExplainers.parentChildSynthesis`.

### Constraints

- Do not imply child outputs are independent verdicts.
- Do not imply parent-child synthesis creates extra AgentJobs or authority.
- Do not broaden the mode beyond its scoped future physics AgentJob context.
- Do not claim validator PASS is valid while a declared blocking conflict is
  unresolved.
- Do not change upstream workflow authority.

### Implementation Notes

- Start from the parent-child dossier.
- Ensure the first substantive explanation is the one-outer-AgentJob invariant.
- Explain:
  - why internal child perspectives exist,
  - inherited authority,
  - child `draft/control` status,
  - parent review and fusion,
  - blocking conflict handling,
  - fused output,
  - scope limits.
- Add the static single-outer-AgentJob diagram with alt text, caption, and
  nearby explanatory prose.
- Add safe/unsafe summaries.
- Use the reusable comprehension model from TASK-03 where practical.
- Regenerate page provenance after editing.

### Acceptance Criteria

- [ ] The page opens with the one-job invariant.
- [ ] The page explains inherited authority, child draft/control status,
      conflict handling, fused output, and scope limits.
- [ ] The static diagram is present with alt text, caption, and nearby prose.
- [ ] Safe/unsafe summaries are present.
- [ ] Source basis and boundaries remain explicit.
- [ ] Page provenance is regenerated.
- [ ] The page passes the comprehension audit and standard validators.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
npm run validate:comprehension
npm run validate:content
npm run validate:links
npm run validate:provenance
npm run validate:manifests
npm run build
```

Browser QA:

```bash
npm run dev -- --host 127.0.0.1 --port 4321
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

Capture desktop and mobile screenshots of
`/project/ai-research-agent-system/parent-child-synthesis/`.

### Done When

The parent-child page is a validated deep-topic pilot and preserves the exact
one-outer-AgentJob authority boundary.

## Task 8: Complete Phase 1 Pilot QA And Human Review

### Goal

Close Phase 1 with validation evidence, screenshots, reduced-motion checks,
and human comprehension review notes.

### Context

- PRD requirements: REQ-006, REQ-014, REQ-015, REQ-017, REQ-019, REQ-020,
  NFR-001, NFR-004, NFR-005
- Relevant files or directories:
  - `docs/quality/`
  - `output/playwright/`
  - `src/pages/project/overview.astro`
  - `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro`
  - `public/files/manifests/**`
- Existing patterns to follow:
  - Existing QA notes summarize validation and screenshot evidence.
  - `output/playwright/` is appropriate for local screenshot artifacts.

### Constraints

- Do not deploy.
- Do not claim human review is complete unless it is actually recorded.
- If an unrelated validation blocker appears, name it precisely.
- Keep screenshot paths local unless the user asks to track them.

### Implementation Notes

- Run standard validation and comprehension audit.
- Run browser QA for desktop and mobile viewport sizes.
- Verify diagrams do not overflow, blur, or replace necessary prose.
- Verify longer text does not create nested cards, overlap, or button overflow.
- Verify reduced-motion behavior where motion-heavy surfaces are affected.
- Record a Phase 1 QA note under `docs/quality/`.
- Include:
  - commands run,
  - screenshots captured,
  - human review status,
  - remaining risks,
  - whether Phase 2 is ready.

### Acceptance Criteria

- [ ] Phase 1 QA note exists under `docs/quality/`.
- [ ] Commands run and results are recorded.
- [ ] Desktop and mobile screenshots exist locally.
- [ ] Human review status is recorded.
- [ ] Any skipped or failed check has a concrete reason.
- [ ] Phase 2 readiness is stated.

### Validation

```bash
npm run validate:comprehension
npm run validate
python3 -m pytest
```

Optional release-readiness gate:

```bash
npm run quality
```

Browser QA:

```bash
npm run dev -- --host 127.0.0.1 --port 4321
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

### Done When

Phase 1 has a reviewable validation record and no unreported uncertainty.

## Task 9: Remediate Physics Route Family

### Goal

Remediate the physics route family in overclaim-risk order, using dossiers,
diagrams, equation walkthroughs, and safe/unsafe summaries where needed.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-005, REQ-007, REQ-008, REQ-009,
  REQ-014, REQ-015, REQ-016, REQ-017, REQ-018, REQ-020, NFR-001, NFR-002,
  NFR-005
- Relevant files or directories:
  - `src/pages/project/physics/index.astro`
  - `src/pages/project/physics/ontology/index.astro`
  - `src/pages/project/physics/exact-gr-benchmark/index.astro`
  - `src/pages/project/physics/gr-derivation-roadmap/index.astro`
  - `src/pages/project/physics/claim-gates/index.astro`
  - `src/pages/project/physics/current-state/index.astro`
  - `src/lib/siteContent.ts`
  - `docs/content-dossiers/physics-*/`
  - `public/assets/diagrams/comprehension/`
  - manifests under `public/files/manifests/`
- Existing patterns to follow:
  - Physics pages already include `SourceNotice` defaults with strong
    source-boundary language.

### Constraints

- Do not claim GR has been derived from the AEther Flow ontology.
- Keep ontology, benchmark adoption, compatibility, derivation, and promotion
  separate.
- Preserve no-go, obstruction, and freeze labels as scoped route-control
  records.
- Do not convert validator PASS into theorem proof.

### Implementation Notes

- Create dossiers before each page rewrite.
- Prioritize:
  1. physics landing,
  2. ontology,
  3. exact-GR benchmark,
  4. GR derivation roadmap,
  5. claim gates,
  6. current state if not deferred.
- Add diagrams where they clarify:
  - benchmark boundary ladder,
  - derivation burden timeline,
  - claim gate/status matrix,
  - ontology-to-effective-model relationship map.
- Add equation walkthroughs when equations are displayed or substantively
  referenced.
- Add safe/unsafe summaries on high-risk pages.
- Regenerate page provenance and asset manifests as needed.

### Acceptance Criteria

- [ ] Each remediated physics page has a dossier.
- [ ] Each page separates ontology, benchmark, derivation burden, and claim
      promotion where relevant.
- [ ] Equation references have walkthroughs.
- [ ] High-risk pages have safe/unsafe summaries.
- [ ] Diagrams are explanatory, accessible, static, and manifest-backed.
- [ ] No physics page silently strengthens claim status.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
python3 scripts/build_asset_manifest.py --write
npm run validate:comprehension
npm run validate:content
npm run validate:links
npm run validate:manifests
npm run validate:provenance
npm run build
```

Capture desktop and mobile screenshots for representative physics routes.

### Done When

The physics route family has source-grounded comprehension depth and preserves
all physics claim boundaries.

## Task 10: Remediate AI-System And Operations Route Families

### Goal

Apply the Phase 1 model to the remaining AI research-agent pages and operations
pages, keeping operational evidence distinct from physics proof.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-005, REQ-007, REQ-010, REQ-011,
  REQ-014, REQ-015, REQ-016, REQ-017, REQ-018, REQ-020, NFR-001, NFR-002,
  NFR-005
- Relevant files or directories:
  - `src/pages/project/ai-research-agent-system/**`
  - `src/pages/project/operations/**`
  - `src/lib/internalExplainers.ts`
  - `src/lib/siteContent.ts`
  - `src/components/InternalExplainerPage.astro`
  - `docs/content-dossiers/ai-*/`
  - `docs/content-dossiers/operations-*/`
  - `public/assets/diagrams/comprehension/`
  - manifests under `public/files/manifests/`
- Existing patterns to follow:
  - Many operations pages render through `InternalExplainerPage`.
  - AI pages mix dedicated route code and source-notice defaults.

### Constraints

- Do not present AI methodology as physics evidence.
- Do not claim autonomous AI ownership of research decisions, authorship, or
  public release accountability.
- Keep AgentJobs, execution records, roles, validators, memory, registries, and
  generated wiki surfaces distinct.
- Keep PASS bounded to the checked state.

### Implementation Notes

- Create dossiers before each page rewrite.
- AI-system remediation should cover:
  - landing page,
  - workflow,
  - roles and skills,
  - memory and registries.
- Operations remediation should cover:
  - operations landing,
  - Director and AgentJob lifecycle,
  - role routing,
  - validator/operator workflow,
  - publication process,
  - project-system improvement,
  - technical requirements.
- Add diagrams where they clarify workflow lifecycle, authority narrowing,
  role/allowlist boundaries, memory hierarchy, record chains, validator
  evidence, publication flow, or improvement-loop routing.
- Add safe/unsafe summaries where a reader might confuse operational success
  with scientific proof.

### Acceptance Criteria

- [ ] Each remediated AI and operations page has a dossier.
- [ ] AI pages explain operational mechanics before metadata.
- [ ] Operations pages explain function rather than only control labels.
- [ ] Role, memory, validator, and AgentJob authority boundaries are clear.
- [ ] PASS evidence is consistently described as bounded.
- [ ] Diagrams are accessible, static, and manifest-backed where used.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
python3 scripts/build_asset_manifest.py --write
npm run validate:comprehension
npm run validate:content
npm run validate:links
npm run validate:manifests
npm run validate:provenance
npm run build
```

Capture desktop and mobile screenshots for representative AI and operations
routes.

### Done When

The AI-system and operations route families teach their mechanisms clearly
without overclaiming authority or physics significance.

## Task 11: Remediate Supporting Surfaces And Close Out Site-Wide QA

### Goal

Remediate resources, documents, diagram gallery, source authority, current
state, and secondary route decisions; then close the comprehension rollout with
site-wide QA and backlog notes.

### Context

- PRD requirements: REQ-001, REQ-002, REQ-005, REQ-007, REQ-008, REQ-012,
  REQ-013, REQ-014, REQ-015, REQ-017, REQ-018, REQ-019, REQ-020, NFR-001,
  NFR-002, NFR-004, NFR-005
- Relevant files or directories:
  - `src/pages/resources/index.astro`
  - `src/pages/resources/documents.astro`
  - `src/pages/resources/diagrams.astro`
  - `src/pages/project/source-authority/index.astro`
  - `src/pages/project/physics/current-state/index.astro`
  - `src/pages/research/**`
  - `src/lib/manifests.ts`
  - `src/lib/siteContent.ts`
  - `public/files/manifests/**`
  - `docs/content-dossiers/**`
  - `docs/quality/`
- Existing patterns to follow:
  - Resources and documents already use manifest-backed download surfaces.
  - Current-state page is a checked-in snapshot, not a live source authority
    surface.

### Constraints

- Keep TeX source authority and PDF derivative status explicit.
- Do not make diagrams authoritative.
- Do not imply current-state snapshots auto-refresh or promote draft/control
  data.
- Do not add new public pages without a content-gap audit.
- Do not deploy.

### Implementation Notes

- Create dossiers before each supporting-surface rewrite.
- Remediate:
  - resource index,
  - ontology documents page,
  - diagram gallery,
  - source-authority page,
  - current-state page if not already handled,
  - secondary research/support routes as decided by content-gap audit.
- Add source authority stack, document asset chain, diagram publication chain,
  or current-state dossier diagrams where they clarify reader trust.
- Update manifests and provenance as needed.
- Run site-wide validation and browser QA.
- Add a final comprehension closeout note under `docs/quality/` with:
  - routes remediated,
  - routes deferred,
  - validation results,
  - human review status,
  - remaining backlog,
  - deployment readiness if applicable.

### Acceptance Criteria

- [ ] Supporting surfaces reinforce internal-first reading and provenance
      boundaries.
- [ ] Document pages clearly distinguish TeX source authority from PDF
      derivatives.
- [ ] Diagram gallery explains what diagrams show and do not prove.
- [ ] Current-state copy explains snapshot status and drift limits.
- [ ] Secondary route decisions are recorded.
- [ ] Final QA note records validation, screenshots, human review, and backlog.

### Validation

```bash
python3 scripts/generate_page_provenance.py --write
python3 scripts/build_asset_manifest.py --write
npm run validate:comprehension
npm run validate
python3 -m pytest
```

Optional release-readiness gate:

```bash
npm run quality
```

Browser QA:

```bash
npm run dev -- --host 127.0.0.1 --port 4321
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

Capture desktop and mobile screenshots for representative supporting routes.

### Done When

The comprehension rollout has a site-wide QA record, deferred work is explicit,
and deployment readiness is known without performing deployment.

## Recommended First Implementation Prompt

Use this prompt to begin implementation in a new Codex session:

```text
Implement TASK-01 from ImplementationPlans/public_comprehension_and_diagram_system_task_packets.md. Keep the work planning/supporting-doc only: add the content-dossier template and comprehension review contract, do not change public routes, do not deploy, and run the listed validation.
```
