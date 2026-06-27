# Public Comprehension And Diagram System Task Packets

Date: 2026-06-27

Source PRD: `PRDs/public-comprehension-and-diagram-system-prd.md`

Companion plan:
`ImplementationPlans/public_comprehension_and_diagram_system_implementation_plan.md`

## Shared Context For All Tasks

Repository: `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website`

This repository is the reader-facing static website for
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`. The upstream source repository
remains authoritative for scientific, mathematical, governance, validator,
workflow, registry, TeX-source, and research-control claims.

Global constraints:

- Do not deploy unless explicitly authorized.
- Do not add public runtime Mermaid.
- Do not publish maintainer dossiers as public navigation pages.
- Do not silently strengthen physics, governance, workflow, role, validator, or
  AI-autonomy claims.
- Keep internal website routes as the primary reader journey.
- Keep GitHub and source links visible as provenance or inspection links.
- Regenerate page provenance after public page source changes.
- Update source and asset manifests after public diagram asset changes.
- Preserve SVG artwork policy: public SVG artwork must be animated and must not
  contain visible embedded text.
- Use PNG for generated Mermaid diagrams by default.
- Preserve user or unrelated worktree changes. Do not revert files outside the
  task scope.

Common validation commands discovered from the repository:

```bash
npm run build
npm run validate
npm run quality
npm run validate:manifests
npm run validate:content
npm run validate:links
npm run validate:svg
npm run validate:provenance
python3 -m pytest
python3 scripts/generate_page_provenance.py
python3 scripts/build_asset_manifest.py --write
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict
```

New commands expected to be added during this work:

- A Mermaid PNG render command in TASK-03.
- `npm run validate:comprehension` in TASK-04.

## Task 1: Create Content Dossier Template And Phase 1 Dossiers

### Goal

Create the maintainer evidence trail required before rewriting the two Phase 1
pilot pages.

### Context

- PRD requirements: REQ-001, REQ-006, REQ-013, REQ-016
- Relevant files or directories:
  - `docs/content-dossiers/`
  - `src/pages/project/overview.astro`
  - `src/lib/internalExplainers.ts`
  - `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro`
  - `public/files/manifests/page_route_map.json`
  - upstream source root: `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`
- Required upstream evidence for Phase 1:
  - `README.md`
  - `github-facing/project-overview-explainer.md`
  - `github-facing/parent-child-synthesis-explainer.md`
  - `markdown/html-explainer-specs/project-overview-explainer.md`
  - `markdown/html-explainer-specs/parent-child-synthesis-explainer.md`
  - `research_control/README.md`
  - `.agents/schemas/AGENT_JOB_SCHEMA.md`
  - `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
  - `registries/AGENT_JOB_REGISTRY.csv`

### Constraints

- Do not rewrite public pages in this task.
- Do not treat dossiers as public pages.
- Do not copy large upstream source text verbatim; summarize source basis and
  preserve exact claim qualifiers where needed.
- If a required upstream file is unavailable, record the missing source and stop
  before public copy changes.

### Implementation Notes

- Add `docs/content-dossiers/_template.md`.
- Add `docs/content-dossiers/project-overview.md`.
- Add `docs/content-dossiers/parent-child-synthesis.md`.
- Each dossier should include route, reader job, current website copy summary,
  mapped upstream sources, source-derived outline, glossary, claim boundaries,
  forbidden implications, required comprehension blocks, required diagrams,
  equation walkthrough needs, safe/unsafe summaries, related internal routes,
  manifest impact, and acceptance checklist.
- For parent-child synthesis, preserve the exact external invariant: one
  Director decision, one outer AgentJob, one execution-role record, one
  completion record, and one fused output.

### Acceptance Criteria

- [ ] A reusable content dossier template exists.
- [ ] The overview dossier maps current page copy to upstream source evidence.
- [ ] The parent-child dossier maps current page copy to upstream source
      evidence.
- [ ] Both dossiers identify glossary terms, claim boundaries, diagram needs,
      safe/unsafe summaries, manifest impact, and public-review checklist.
- [ ] No public route content changes in this task.

### Validation

```bash
git diff --check -- docs/content-dossiers
```

If public page files are accidentally touched, stop and review the diff before
continuing.

### Done When

The two Phase 1 page rewrites have a tracked source-derived editorial contract
ready for implementation.

## Task 2: Add Flexible Comprehension Blocks

### Goal

Introduce reusable content structures for context, summary, mechanism,
definitions, diagrams, equations, source basis, boundaries, safe/unsafe
summaries, and related reading.

### Context

- PRD requirements: REQ-001, REQ-003, REQ-005, REQ-016
- Relevant files or directories:
  - `src/lib/internalExplainers.ts`
  - `src/components/InternalExplainerPage.astro`
  - `src/components/Figure.astro`
  - `src/components/EquationBlock.astro`
  - `src/components/SourceNotice.astro`
  - `src/pages/project/overview.astro`
  - `src/styles/global.css`

### Constraints

- Do not force every page into the same visual template.
- Do not encode scientific claims inside generic components.
- Do not introduce unnecessary dependencies.
- Coordinate with the command-interface redesign if its primitives already
  exist; otherwise keep changes compatible with current route classes.

### Implementation Notes

- Add a small typed model, likely `src/lib/publicComprehension.ts`, with block
  kinds for context, plain summary, system logic, terms, source basis,
  boundary, diagram, equation walkthrough, safe/unsafe summary, and related
  path.
- Add or extend Astro components for the reusable block surfaces:
  `ComprehensionBlock.astro`, `DiagramFigure.astro`,
  `EquationWalkthrough.astro`, and `SafeUnsafeSummary.astro`.
- Extend `InternalExplainerPage.astro` to render optional rich blocks while
  preserving existing `sections` behavior for pages not yet remediated.
- Keep `Figure.astro` and `EquationBlock.astro` available for simple pages; do
  not break existing MDX math sample routes.

### Acceptance Criteria

- [ ] The content model can represent all PRD comprehension block types.
- [ ] Components support alt text, captions, source basis, and boundary copy.
- [ ] Equation walkthrough rendering supports symbols, assumptions, source
      status, valid regime, non-proof boundary, and a "read it as" sentence.
- [ ] Existing pages still build before pilot rewrites.
- [ ] No public claim language is changed by the component foundation alone.

### Validation

```bash
npm run build
npm run validate:content
```

If TypeScript or Python tests are affected:

```bash
python3 -m pytest
```

### Done When

The website has reusable comprehension block infrastructure ready for the
overview and parent-child pilots.

## Task 3: Add Mermaid Static Diagram Pipeline

### Goal

Create a reproducible maintainer pipeline for Mermaid source diagrams rendered
to committed static PNG assets.

### Context

- PRD requirements: REQ-004, REQ-014, NFR-001, NFR-002, NFR-003
- Relevant files or directories:
  - `docs/diagram-sources/`
  - `public/assets/diagrams/`
  - `public/files/manifests/source_manifest.json`
  - `public/files/manifests/asset_manifest.json`
  - `scripts/build_asset_manifest.py`
  - `scripts/validate_manifest_paths.py`
  - `package.json`
  - `tests/`

### Constraints

- Do not add Mermaid to public browser runtime.
- PNG is the default output format.
- SVG visible-text policy remains unchanged; do not use visible-text SVGs to
  satisfy this PRD.
- Keep any Mermaid dependency dev-only or script-local.

### Implementation Notes

- Choose and document the renderer path. Prefer a pinned dev-only Mermaid CLI
  workflow if it gives reproducible local rendering without runtime Mermaid.
- Add Mermaid source files:
  - `docs/diagram-sources/overview-two-track-project-map.mmd`
  - `docs/diagram-sources/parent-child-one-outer-agentjob.mmd`
- Add generated PNG files:
  - `public/assets/diagrams/overview-two-track-project-map.png`
  - `public/assets/diagrams/parent-child-one-outer-agentjob.png`
- Add or update a script/package command for rendering diagrams.
- Add source manifest rows for each public diagram and rebuild
  `asset_manifest.json`.
- Add a built-output or source check proving public pages do not include
  runtime Mermaid script usage.

### Acceptance Criteria

- [ ] Mermaid `.mmd` source files are tracked under `docs/diagram-sources/`.
- [ ] Generated PNG diagrams are committed under `public/assets/diagrams/`.
- [ ] Diagram assets are represented in `source_manifest.json` and
      `asset_manifest.json`.
- [ ] The public site references PNG assets, not Mermaid source.
- [ ] The repository has an explicit render command or script for regeneration.
- [ ] No public runtime Mermaid dependency is introduced.

### Validation

Run the new render command created by this task.

Then run:

```bash
npm run validate:manifests
npm run validate:svg
npm run build
```

After build, verify that generated public pages do not include Mermaid runtime
scripts. If no project command exists yet, document the exact check used in the
task summary.

### Done When

The Phase 1 diagrams are reproducible, static, manifest-backed PNG assets.

## Task 4: Add Public-Comprehension Audit Gate

### Goal

Add a focused quality gate that catches mechanical comprehension failures while
preserving human review as the final public-understanding check.

### Context

- PRD requirements: REQ-001, REQ-007, REQ-014, REQ-016
- Relevant files or directories:
  - `docs/quality/`
  - `docs/content-dossiers/`
  - `scripts/`
  - `tests/`
  - `package.json`
  - `src/pages/**`
  - `src/lib/**`

### Constraints

- Do not claim scripted checks prove public comprehension.
- Start as a separate gate, not automatically part of `npm run validate`, unless
  the reviewer explicitly approves hard integration.
- Keep checks observable and maintainable; avoid brittle prose-length quotas.

### Implementation Notes

- Add `docs/quality/public-comprehension-audit.md` with human review criteria.
- Add `scripts/validate_public_comprehension.py`.
- Add `npm run validate:comprehension`.
- Add tests covering success and failure fixtures.
- Mechanical checks should cover:
  - required dossier for remediated route;
  - plain-language summary marker;
  - source basis marker;
  - boundary marker;
  - term definitions for specialized terms;
  - diagram alt/caption/prose where a diagram is required;
  - equation walkthrough marker where equations are present;
  - safe/unsafe summary for high-risk claim-boundary topics;
  - internal-first route links;
  - no runtime Mermaid public dependency.
- Add a remediated-route allowlist so the audit can expand by phase.

### Acceptance Criteria

- [ ] Human audit checklist exists.
- [ ] `validate:comprehension` exists and runs the new validator.
- [ ] Tests cover at least one missing-dossier failure and one missing-boundary
      or missing-summary failure.
- [ ] The audit can target Phase 1 routes without requiring all future pages to
      pass before remediation.
- [ ] The task summary states what the script cannot prove.

### Validation

```bash
npm run validate:comprehension
python3 -m pytest
```

### Done When

The repository has a phase-expandable comprehension quality gate and a human
review contract.

## Task 5: Remediate The Project Overview Pilot

### Goal

Rewrite `/project/overview/` into a general-public front door that teaches the
dual project structure before presenting route choices.

### Context

- PRD requirements: REQ-002, REQ-004, REQ-006, REQ-008, REQ-014, REQ-016,
  NFR-002, NFR-003
- Relevant files or directories:
  - `docs/content-dossiers/project-overview.md`
  - `docs/diagram-sources/overview-two-track-project-map.mmd`
  - `public/assets/diagrams/overview-two-track-project-map.png`
  - `src/pages/project/overview.astro`
  - `src/lib/siteContent.ts`
  - `src/components/SourceNotice.astro`
  - `public/files/manifests/page_provenance.json`
  - `public/files/manifests/source_manifest.json`
  - `public/files/manifests/asset_manifest.json`

### Constraints

- Do not reopen visual color schema or command-interface decisions.
- Do not claim GR has been derived from the ontology.
- Do not claim the AI system autonomously owns research decisions or release
  accountability.
- Keep source links as provenance, not primary route choices.

### Implementation Notes

- Use the dossier as the source contract.
- Open with what AEther Flow is, not metadata or navigation.
- Explain the physics track, AI research-agent track, co-development, source
  authority boundary, reader route jobs, and website non-claims.
- Add the two-track project map PNG with alt text, caption, nearby prose, and a
  statement of what the diagram does not prove.
- Add glossary/terms for exact-GR benchmark, source authority, AgentJob, and
  derivation burden where first useful.
- Add safe/unsafe summary if the audit classifies the overview as high-risk.
- Regenerate page provenance after source changes.
- Capture desktop and mobile screenshots.

### Acceptance Criteria

- [ ] The page opens with clear general-public context.
- [ ] The page explains both project tracks and how they co-develop.
- [ ] The page explains upstream source authority and website limits.
- [ ] The two-track PNG diagram is visible, readable, accessible, and explained.
- [ ] Route links describe reader jobs and remain internal-first.
- [ ] The page includes source basis, boundary, glossary, related paths, and
      safe/unsafe summary where required by the audit.
- [ ] Page provenance is regenerated.

### Validation

```bash
python3 scripts/generate_page_provenance.py
npm run validate:manifests
npm run validate:provenance
npm run validate:links
npm run validate:comprehension
npm run build
```

For browser evidence, run a local server and capture desktop/mobile screenshots
of `/project/overview/`.

### Done When

The overview pilot passes repository checks, comprehension audit, human review,
and responsive browser QA.

## Task 6: Remediate The Parent-Child Synthesis Pilot

### Goal

Rewrite the parent-child synthesis page into a deep-topic explainer centered on
the one-outer-AgentJob invariant.

### Context

- PRD requirements: REQ-003, REQ-004, REQ-006, REQ-008, REQ-014, REQ-016,
  NFR-002, NFR-003
- Relevant files or directories:
  - `docs/content-dossiers/parent-child-synthesis.md`
  - `docs/diagram-sources/parent-child-one-outer-agentjob.mmd`
  - `public/assets/diagrams/parent-child-one-outer-agentjob.png`
  - `src/lib/internalExplainers.ts`
  - `src/components/InternalExplainerPage.astro`
  - `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro`
  - `public/files/manifests/page_provenance.json`
  - `public/files/manifests/source_manifest.json`
  - `public/files/manifests/asset_manifest.json`

### Constraints

- Preserve `draft/control` exactly where used for child artifacts.
- Do not imply child perspectives create separate jobs, roles, writes,
  validators, verdicts, or authority.
- Do not generalize parent-child synthesis to all project-system or
  documentation work.
- Keep unresolved blocking conflict behavior explicit.

### Implementation Notes

- Use the dossier as the source contract.
- Open with the one-outer-AgentJob invariant.
- Explain parent review, child perspectives, inherited authority, conflict
  handling, fused output, PASS limits, and scope limits.
- Add the one-outer-AgentJob PNG diagram with alt text, caption, nearby prose,
  and a diagram non-claim statement.
- Add glossary/terms for Director decision, AgentJob, execution-role record,
  completion record, fused output, `draft/control`, and blocking conflict.
- Add safe/unsafe summaries.
- Regenerate page provenance after source changes.
- Capture desktop and mobile screenshots.

### Acceptance Criteria

- [ ] The page opens with the one-job invariant.
- [ ] It explains inherited authority and child `draft/control` status.
- [ ] It explains unresolved blocking conflict behavior and PASS invalidity.
- [ ] It explains fused output and downstream reference behavior.
- [ ] It states scope limits.
- [ ] The PNG diagram is visible, readable, accessible, and explained.
- [ ] The page includes source basis, boundary, glossary, safe/unsafe summary,
      and related internal route guidance.
- [ ] Page provenance is regenerated.

### Validation

```bash
python3 scripts/generate_page_provenance.py
npm run validate:manifests
npm run validate:provenance
npm run validate:links
npm run validate:comprehension
npm run build
```

For browser evidence, run a local server and capture desktop/mobile screenshots
of `/project/ai-research-agent-system/parent-child-synthesis/`.

### Done When

The parent-child pilot passes repository checks, comprehension audit, human
review, and responsive browser QA.

## Task 7: Remediate Physics Route Family

### Goal

Remediate the physics pages in overclaim-risk order using dossiers, diagrams,
equation walkthroughs, and source-boundary-safe copy.

### Context

- PRD requirements: REQ-005, REQ-006, REQ-009, REQ-014, REQ-016
- Relevant files or directories:
  - `src/pages/project/physics/index.astro`
  - `src/pages/project/physics/ontology/index.astro`
  - `src/pages/project/physics/exact-gr-benchmark/index.astro`
  - `src/pages/project/physics/gr-derivation-roadmap/index.astro`
  - `src/pages/project/physics/claim-gates/index.astro`
  - `src/pages/project/physics/current-state/index.astro`
  - `src/lib/siteContent.ts`
  - `docs/content-dossiers/`
  - `docs/diagram-sources/`
  - `public/assets/diagrams/`
  - `public/files/manifests/**`

### Constraints

- Do not claim substrate derivation of GR.
- Keep ontology, mathematical model, empirical prediction, benchmark adoption,
  compatibility, derivation, and promotion separate.
- Explain no-go, obstruction, and freeze labels as scoped route-control records,
  not global rejection of the theory.
- Equation walkthroughs are required when equations are displayed or
  substantively referenced.

### Implementation Notes

- Create dossiers before each route rewrite.
- Recommended order: physics landing, ontology, exact-GR benchmark, GR
  derivation roadmap, claim gates, current-state if not deferred.
- Add diagrams only where they clarify structure: benchmark boundary ladder,
  derivation burden timeline, claim gate/status matrix,
  ontology-to-effective-model relationship map, or equation relationship map.
- Add equation walkthroughs for equation-bearing pages or pages discussing
  equation-level targets.
- Regenerate page provenance and asset manifests after changes.

### Acceptance Criteria

- [ ] Every remediated physics page has a dossier.
- [ ] Relevant pages separate ontology, benchmark adoption, compatibility,
      derivation, promotion, and empirical prediction.
- [ ] Equation references have walkthroughs.
- [ ] High-risk pages include safe/unsafe summaries.
- [ ] Diagrams explain boundaries or mechanisms and state what they do not
      prove.
- [ ] No page silently strengthens physics status.

### Validation

```bash
python3 scripts/generate_page_provenance.py
python3 scripts/build_asset_manifest.py --write
npm run validate
npm run validate:comprehension
npm run quality
```

Capture representative desktop/mobile screenshots for physics routes changed in
the task.

### Done When

The physics route family has source-derived public comprehension coverage and
passes validation and review for the changed routes.

## Task 8: Remediate AI Research-Agent Route Family

### Goal

Apply the parent-child pilot lessons to the remaining AI research-agent route
family.

### Context

- PRD requirements: REQ-006, REQ-010, REQ-014, REQ-016
- Relevant files or directories:
  - `src/pages/project/ai-research-agent-system/index.astro`
  - `src/pages/project/ai-research-agent-system/workflow/index.astro`
  - `src/pages/project/ai-research-agent-system/roles-and-skills/index.astro`
  - `src/pages/project/ai-research-agent-system/memory-registries/index.astro`
  - `src/lib/internalExplainers.ts`
  - `src/lib/siteContent.ts`
  - `docs/content-dossiers/`
  - `docs/diagram-sources/`
  - `public/assets/diagrams/`

### Constraints

- Separate AI-methodology claims from physics claims.
- Do not imply AI agents autonomously own research decisions, authorship, or
  public release accountability.
- Distinguish role names, registered roles, execution-role records, task
  overlays, AgentJob allowlists, validators, memory retrieval, and canonical
  source files.

### Implementation Notes

- Create dossiers before each route rewrite.
- Remediate AI landing, workflow, roles-and-skills, and memory-and-registries.
- Reuse parent-child block patterns for invariants, authority stacks, memory
  hierarchies, validator limits, and safe/unsafe summaries.
- Use diagrams selectively: workflow lifecycle, Director-to-AgentJob narrowing,
  role/allowlist authority stack, or memory/registry source hierarchy.

### Acceptance Criteria

- [ ] Every remediated AI-system page has a dossier.
- [ ] Pages explain operational mechanics before metadata.
- [ ] Role labels, execution records, AgentJobs, validators, and memory
      surfaces are distinguished.
- [ ] AI-methodology claims remain separate from physics claims.
- [ ] Diagrams clarify workflow, authority narrowing, memory surfaces, or role
      boundaries where useful.

### Validation

```bash
python3 scripts/generate_page_provenance.py
python3 scripts/build_asset_manifest.py --write
npm run validate
npm run validate:comprehension
```

Capture representative desktop/mobile screenshots for AI-system routes changed
in the task.

### Done When

The AI research-agent route family has source-derived public comprehension
coverage and passes validation and review for the changed routes.

## Task 9: Remediate Operations Route Family

### Goal

Remediate operational pages so they explain lifecycle, routing, validation,
publication, project-system improvement, and tools as bounded operational
evidence rather than physics progress.

### Context

- PRD requirements: REQ-006, REQ-011, REQ-014, REQ-016
- Relevant files or directories:
  - `src/pages/project/operations/index.astro`
  - `src/pages/project/operations/director-agentjob-lifecycle/index.astro`
  - `src/pages/project/operations/role-routing/index.astro`
  - `src/pages/project/operations/validator-operator-workflow/index.astro`
  - `src/pages/project/operations/publication-process/index.astro`
  - `src/pages/project/operations/project-system-improvement/index.astro`
  - `src/pages/project/operations/technical-requirements/index.astro`
  - `src/lib/internalExplainers.ts`
  - `docs/content-dossiers/`

### Constraints

- PASS evidence must remain bounded operational evidence.
- Publication quality must remain distinct from source authority.
- Project-system improvement must remain distinct from physics continuation or
  science progress.
- Do not mutate upstream routing, validator, role, or task authority.

### Implementation Notes

- Create dossiers before each route rewrite.
- Use diagrams selectively: record-chain lifecycle, validator evidence flow,
  publication process flow, improvement-loop routing map, or tool-tier
  dependency map.
- Preserve internal-first links and provenance sections.

### Acceptance Criteria

- [ ] Every remediated operations page has a dossier.
- [ ] Pages explain operational function, not only control labels.
- [ ] PASS evidence is consistently described as bounded.
- [ ] Publication quality is distinguished from source authority.
- [ ] Project-system improvement is distinguished from physics progress.
- [ ] Diagrams clarify record chains, validators, publication, improvement
      loops, or tool tiers where useful.

### Validation

```bash
python3 scripts/generate_page_provenance.py
python3 scripts/build_asset_manifest.py --write
npm run validate
npm run validate:comprehension
```

Capture representative desktop/mobile screenshots for operations routes changed
in the task.

### Done When

The operations route family has source-derived public comprehension coverage
and passes validation and review for the changed routes.

## Task 10: Remediate Supporting Surfaces And Audit Secondary Routes

### Goal

Remediate resources, documents, diagrams, source authority, current state, and
secondary/support routes so they reinforce trust, asset status, drift limits,
and internal-first reading.

### Context

- PRD requirements: REQ-006, REQ-008, REQ-012, REQ-013, REQ-014, REQ-016
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
  - `docs/content-dossiers/`

### Constraints

- TeX source authority versus PDF derivative status must remain explicit.
- The diagram gallery must explain diagram purpose and diagram limits.
- Current-state content must clarify snapshot status and drift risk.
- Do not add new public pages unless a content-gap audit proves necessity.

### Implementation Notes

- Create dossiers for supporting surfaces that are rewritten.
- Audit secondary research routes for remediation, de-emphasis, redirect, or
  retained support-route status.
- Update resource and diagram metadata so approved diagrams are distinguished
  from sample fixtures.
- Preserve manifest-backed asset display and source-provenance sections.

### Acceptance Criteria

- [ ] Resources and documents explain asset status and source authority.
- [ ] Diagram gallery explains what diagrams show and what they do not prove.
- [ ] Source-authority page distinguishes generated derivatives, source
      records, registries, validators, and website pages.
- [ ] Current-state page explains task state, handoff state, claim boundaries,
      drift risk, and next action in ordinary language.
- [ ] Secondary route treatment is documented through a content-gap audit.

### Validation

```bash
python3 scripts/generate_page_provenance.py
python3 scripts/build_asset_manifest.py --write
npm run validate
npm run validate:comprehension
npm run quality
```

Capture representative desktop/mobile screenshots for supporting routes changed
in the task.

### Done When

Supporting surfaces reinforce the improved core pages and no thin new page
masks weak explanations.

## Task 11: Run Site-Wide QA And Produce Handoff

### Goal

Close the remediation release with repository validation, public-comprehension
audit evidence, browser QA, and a remaining-backlog handoff.

### Context

- PRD requirements: REQ-007, REQ-014, REQ-015, REQ-016, all NFRs
- Relevant files or directories:
  - `docs/quality/`
  - `output/playwright/`
  - `scratch/project-explainer/`
  - `public/files/manifests/**`
  - `dist/`
  - all remediated route files

### Constraints

- Do not deploy.
- Do not treat validator PASS as human comprehension proof.
- Do not hide known unrelated validation blockers; name them concretely.

### Implementation Notes

- Run repository validators and record results.
- Run public-comprehension audit and human review checklist.
- Build the site and run the project explainer audit.
- Run local preview/dev server smoke tests.
- Capture representative desktop and mobile screenshots for remediated route
  families.
- Check reduced-motion behavior where animation changed.
- Verify Mermaid PNG assets, alt text, captions, nearby prose, and manifests.
- Verify page provenance after final page edits.
- Verify runtime Mermaid was not introduced.
- Write a QA/handoff note under `docs/quality/` with completed routes,
  deferred routes, residual risks, and recommended next packet.

### Acceptance Criteria

- [ ] `npm run validate` passes, or failures are named with concrete existing
      blockers.
- [ ] `npm run validate:comprehension` passes for the remediated route allowlist.
- [ ] `python3 -m pytest` passes, or failures are named with concrete existing
      blockers.
- [ ] Browser screenshots show no text overlap, diagram overflow, unreadable
      equations, button overflow, or inaccessible route sequencing.
- [ ] GitHub links remain provenance links, not primary reading links.
- [ ] Handoff identifies any routes not remediated and why.

### Validation

```bash
python3 -m pytest
npm run validate
npm run validate:comprehension
npm run quality
python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict
```

With a local server running:

```bash
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

### Done When

The remediated corpus has executable validation, human review evidence, browser
evidence, manifest/provenance integrity, and a clear remaining-backlog handoff.
