# Implementation Plan: Sitewide Greenfield Rebuild

## Source PRD

- Source: `PRDs/sitewide-greenfield-rebuild-prd.md`
- Supporting requirements: `PRDs/website-information-space/`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions
- Recommended branch: `codex/sitewide-greenfield-rebuild`

## Product Summary

The rebuild replaces the current card-heavy route tree with a smaller public
information architecture:

- `/`
- `/physics/`
- `/ai-research-system/`
- `/resources/`

Home is a page. The other three are top-level categories with dropdown menus,
category landing pages, and focused child routes. Every substantive page must
begin with a hero/title/action/SVG area, then a substantial general-public
introductory paragraph, then topic-specific technical, scientific,
operational, professional, provenance, and navigation sections.

The old implementation is evidence, not the new implementation. It may be
inspected to preserve approved behavior and content boundaries: the current
footer, hero/title/action direction, animated SVG visual language, diagram
generation/display discipline, source-authority copy, provenance behavior, and
validation expectations. It must not be used as the new page grammar, route
model, card-grid structure, or default authoring model.

Deployment remains blocked until the project owner marks the rebuilt page set
as `reviewed and accepted`.

## Repository Context

- Frameworks and languages: Astro 7 static site, TypeScript content modules,
  Astro components, CSS, Python validation scripts.
- Package manager and build system: npm with `astro build`; local Python
  tooling through `.venv/bin/python` where available.
- Existing implementation evidence:
  - `src/layouts/BaseLayout.astro` contains the current footer and dropdown
    navigation mechanics.
  - `src/pages/index.astro` contains the current hero/action/SVG direction.
  - `src/pages/resources/diagrams.astro`,
    `src/components/DiagramGalleryList.astro`, and
    `scripts/render_mermaid_diagrams.py` contain the diagram-publication
    discipline.
  - `src/components/CommandBand.astro`, `EvidenceRail.astro`, and
    `StatusDossier.astro` show useful section forms, but the rebuild should
    create a new content contract rather than preserve old page structure.
  - `public/files/manifests/page_route_map.json`,
    `public/files/manifests/page_provenance.json`, and
    `public/files/manifests/asset_manifest.json` are public manifest surfaces
    that must be regenerated when routes or assets change.
- Repository instructions:
  - Upstream source files, registries, and governed task records remain
    authoritative for scientific, mathematical, governance, and
    research-workflow claims.
  - Website pages are explanatory derivatives.
  - Internal website routes are the primary reader journey; source and GitHub
    links are provenance or inspection links.
  - Library/resource pages under `/resources/` must not render a dedicated
    `Source authority` section.
  - Visual SVG figures must be animated and must not contain visible embedded
    text.
- Implementation-control context:
  - `implementation_control/program_state.yaml` treats PRDs and
    `ImplementationPlans/*.md` as context once live control records exist.
  - Route implementation, public manifest updates, public asset changes,
    upstream writes, source refreshes, push, and deploy require fresh live
    control authorization.
- Discovered validation commands:
  - `git diff --check`
  - `npm run validate:implementation-control`
  - `.venv/bin/python -m pytest`
  - `python3 -m pytest`
  - `npm run validate:manifests`
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:layout`
  - `npm run validate:svg`
  - `npm run validate:comprehension`
  - `npm run validate:provenance`
  - `npm run validate:curator`
  - `npm run validate:cloudflare`
  - `npm run build`
  - `npm run validate`
  - `npm run quality`
  - `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | The implementation-plan files belong under `ImplementationPlans/`. | Existing checked-in plans use this directory and previous repo-local PRD planning followed that convention. | Commit or workflow registration. |
| ASM-002 | Planning assumption | New routes should be built alongside the old route tree first. | The PRD authorizes greenfield replacement but not immediate deletion; bounded migration keeps rollback simple. | First route implementation packet. |
| ASM-003 | Planning assumption | Existing footer copy and badge behavior should be preserved semantically, not necessarily by keeping the exact old layout file. | The PRD preserves current footer content and behavior but rejects preserving the old implementation as the new architecture. | Shell implementation. |
| ASM-004 | Planning assumption | Existing animated SVG direction may be adapted into a new shell if it still passes SVG policy and browser QA. | The PRD preserves the hero SVG language, not every old SVG path or placement. | Shell and Home implementation. |
| ASM-005 | Planning assumption | Diagram Gallery should start with an empty or curated future-ready inventory unless a diagram is explicitly reapproved. | The PRD says preserve the gallery-format idea while removing the current inventory unless reapproved. | Diagram Gallery implementation. |
| ASM-006 | Planning assumption | Current-state pages should use existing snapshot scripts only after source freshness is authorized by a live packet. | PRD-09 and implementation-control state both require freshness-sensitive handling. | Current-state implementation. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Implementation detail | Should obsolete old routes redirect to nearest new routes with `301`, temporary `302`, or be removed after internal links are updated? | Affects `public/_redirects` and SEO semantics, not feasibility. |
| Q-002 | Implementation detail | Should the review ledger be Markdown-only under `docs/quality/`, or should a machine-readable JSON mirror be added for validators later? | Affects future automation, not first implementation. |
| Q-003 | Planning assumption | Which existing diagrams, if any, are explicitly reapproved for the new Diagram Gallery inventory? | Without approval, the gallery should preserve format and workflow but omit old inventory. |
| Q-004 | Implementation detail | Should the new content contract live in TypeScript data modules, Astro frontmatter, or a hybrid source-bundle registry? | The first foundation packet can decide after inspecting existing component boundaries. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| REQ-001 Greenfield IA | Top navigation has Home, Physics Research, AI Research System, and Resources. | `src/layouts/*`, `src/lib/*`, route files, CSS. | GF-001, GF-002, GF-013 | `npm run validate:links`, `npm run build`, browser QA. |
| REQ-002 Route inventory | All 29 planned pages exist at the new short routes. | `src/pages/physics/`, `src/pages/ai-research-system/`, `src/pages/resources/`, `src/pages/index.astro`. | GF-002 through GF-012 | Route smoke test, `npm run validate:provenance`, `npm run build`. |
| REQ-003 Old implementation reference only | New pages do not inherit the old route grammar or card-grid default. | New layout/content contract and page packets. | GF-001 through GF-014 | Plan review, browser QA, public-comprehension review. |
| REQ-004 Intro paragraph rule | Each substantive page has one substantial general-public introduction immediately after the hero. | Page layout, content source bundles, comprehension validator. | GF-002 through GF-012 | `npm run validate:comprehension`, human review. |
| REQ-005 Structured page grammar | Pages use narrative bands, evidence rails, dossiers, diagrams, matrices, tables, timelines, or glossaries where appropriate; cards are limited to true peer choices. | New components and route content. | GF-001 through GF-012 | Browser QA, layout review, `npm run validate:layout`. |
| REQ-006 Preserve hero/title/action direction | First viewport keeps a clear topic title, actions, and visual identity. | Shell, Home, category pages, CSS, SVG. | GF-001, GF-002 | `npm run validate:svg`, desktop/mobile QA. |
| REQ-007 Preserve animated SVG language | Hero or category visuals remain animated, textless, accessible SVGs. | SVG components, CSS animations. | GF-001 through GF-005 as needed | `npm run validate:svg`, browser QA. |
| REQ-008 Preserve footer | Footer keeps source-authority notice, copyright/license, project GitHub badge, creator identity, and profile badges. | New shell footer or adapted footer component. | GF-001 | `npm run build`, browser QA. |
| REQ-009 Physics category | Physics pages separate ontology, exact-GR benchmark, derivation burden, flow geometry, claim status, and open burdens. | `/physics/*`, source bundles from PRD-02 and PRD-09. | GF-003, GF-004, GF-005 | `npm run validate:comprehension`, source review, browser QA. |
| REQ-010 AI category | AI pages explain workflow, current state, AgentJobs, roles, validators, handoffs, memory, improvement loops, and runtime requirements. | `/ai-research-system/*`, PRD-03, PRD-04, PRD-07, PRD-09. | GF-006 through GF-009 | `npm run validate:comprehension`, source review, browser QA. |
| REQ-011 Resources category | Resources contains source authority, registries, derivatives, retrieval, publication, library, reading paths, repository map, site-builder guide, and diagrams. | `/resources/*`, PRD-05, PRD-06, PRD-08, PRD-11. | GF-010, GF-011, GF-012 | `npm run validate:content`, `npm run validate:links`, browser QA. |
| REQ-012 Diagram Gallery reset | Gallery remains under `/resources/diagrams/`, keeps gallery workflow, removes old inventory unless explicitly reapproved. | Diagram route, asset manifests, diagram source workflow. | GF-012 | `npm run validate:svg`, `npm run validate:manifests`, browser QA. |
| REQ-013 Source authority boundary | Pages label source anchors, claim status, internal-first role, and validation gates without strengthening claims. | Source bundles, page metadata, provenance manifests, footer. | All route tasks | `npm run validate:content`, `npm run validate:provenance`, human review. |
| REQ-014 Human review loop | Deployment is blocked until owner review accepts pages; feedback packets rerun validation. | `docs/quality/sitewide-greenfield-review-ledger.md`, task closeouts. | GF-001, GF-014 | Ledger review, validation summaries. |
| NFR-001 Static build | Affected routes build as static Astro pages. | Astro routes and layouts. | All code tasks | `npm run build`. |
| NFR-002 Accessibility and responsive quality | Dropdowns, SVGs, text, tables, diagrams, and footer work on desktop and mobile without overlap. | Layout, CSS, semantic HTML. | All code tasks | Desktop/mobile browser QA, `npm run validate:layout`. |
| NFR-003 No unsupported dependencies | The rebuild uses existing Astro/TypeScript/Python tooling unless a packet justifies a dependency. | `package.json`, implementation tasks. | All tasks | Diff review, `npm install` only if explicitly authorized. |
| NFR-004 Rollback safety | Old routes are removed only after replacements, redirects, manifests, and validation pass. | Route retirement packet. | GF-013 | `npm run validate`, redirect smoke test. |

## New Route And Source-Bundle Map

| Route | Page | Primary source requirements | Task |
| --- | --- | --- | --- |
| `/` | Home | PRD-01, PRD-10, source-authority boundary, preserved hero/footer evidence. | GF-002 |
| `/physics/` | Physics Overview | PRD-02, PRD-10, physics source bundle. | GF-003 |
| `/physics/ontology/` | Ontology | PRD-02, registered ontology TeX and ontology source anchors. | GF-003 |
| `/physics/exact-gr-benchmark/` | Exact-GR Benchmark | PRD-02, exact-closure TeX, adoption-versus-derivation table. | GF-004 |
| `/physics/derivation-roadmap/` | Derivation Roadmap | PRD-02, PRD-09, derivation burden map and Distance-to-GR evidence. | GF-004 |
| `/physics/flow-geometry/` | Flow Geometry | PRD-02, geometry TeX/source bundle. | GF-004 |
| `/physics/claim-status/` | Physics Claim Status | PRD-02, PRD-09, claim-boundary registry. | GF-005 |
| `/physics/open-burdens/` | Open Burdens | PRD-02, PRD-09, burden ledger and blocked-claim evidence. | GF-005 |
| `/ai-research-system/` | AI Research System Overview | PRD-03, PRD-10, workflow source bundle. | GF-006 |
| `/ai-research-system/current-state/` | Current State | PRD-09, implementation-control state, source freshness rules. | GF-006 |
| `/ai-research-system/workflow/` | Research-Agent Workflow | PRD-03, research-control workflow sources. | GF-007 |
| `/ai-research-system/agentjob-lifecycle/` | AgentJob Lifecycle | PRD-03, AgentJob schema and control record sources. | GF-007 |
| `/ai-research-system/roles-and-schemas/` | Roles and Schemas | PRD-04, role registry, schema sources. | GF-008 |
| `/ai-research-system/human-gated-promotion/` | Human-Gated Promotion | PRD-04, claim-boundary registry, human-gate sources. | GF-008 |
| `/ai-research-system/validators-and-handoffs/` | Validators and Handoffs | PRD-03, PRD-07, validator and handoff sources. | GF-008 |
| `/ai-research-system/memory-preflight/` | Memory Preflight | PRD-03, PRD-05, retrieval boundary sources. | GF-009 |
| `/ai-research-system/project-system-improvement/` | Project-System Improvement | PRD-03, PRD-07, improvement-loop sources. | GF-009 |
| `/ai-research-system/runtime-requirements/` | Runtime Requirements | PRD-07, scripts, tests, requirements, Makefile evidence. | GF-009 |
| `/resources/` | Resources Overview | PRD-05, PRD-06, PRD-11. | GF-010 |
| `/resources/source-authority/` | Source Authority | PRD-05, AGENTS, source-authority source bundle. | GF-010 |
| `/resources/registries/` | Registry Explorer | PRD-05, registry sources and manifest behavior. | GF-010 |
| `/resources/generated-derivatives/` | Generated Derivatives | PRD-05, PRD-06, derivative registries. | GF-011 |
| `/resources/retrieval-layers/` | Local Retrieval Layers | PRD-05, PRD-08, `.local` boundary. | GF-011 |
| `/resources/publication-process/` | Publication Process | PRD-06, publication briefs and source specs. | GF-011 |
| `/resources/library/` | Library | PRD-06, source-backed library surfaces. | GF-011 |
| `/resources/reading-paths/` | Reading Paths | PRD-01, PRD-06, PRD-11. | GF-012 |
| `/resources/repository-map/` | Repository Map | PRD-08, topology evidence. | GF-012 |
| `/resources/site-builder-guide/` | Site Builder Guide | PRD-11, source-bundle schema. | GF-012 |
| `/resources/diagrams/` | Diagram Gallery | Greenfield PRD, PRD-06, diagram workflow, reapproval rule. | GF-012 |

## Proposed Technical Approach

### 1. Fresh Control And Foundation

Before route coding, open a fresh implementation-control task for the
greenfield rebuild. The first code packet should establish:

- new navigation model;
- new content/page metadata contract;
- review ledger with `human review pending`, `reviewed with changes
  requested`, and `reviewed and accepted`;
- new shell or layout namespace for the rebuild;
- preserved footer behavior;
- hero/title/action/SVG acceptance checks;
- card-use rules and page-form vocabulary.

This foundation may inspect old files, but it should create the new
architecture in explicit greenfield files or clearly marked replacement
components.

### 2. Source-Bundle-First Page Work

Every page packet must inspect or create a source bundle before writing
claim-bearing public copy. Each bundle should name:

- primary authority sources;
- supporting sources;
- derivative seed material, if used;
- PRDs consulted;
- claim boundaries and forbidden inferences;
- freshness policy;
- validation commands;
- human review status.

Existing pages, generated explainers, Markdown derivatives, diagrams, and
registry tables can seed reader structure only after the bundle identifies the
actual authority source.

### 3. New Page Grammar

Use route-specific page forms instead of a universal card grid:

- narrative bands for explanation sequence;
- evidence rails for ordered source or claim-gate flows;
- status dossiers for current state or authority metadata;
- matrices and tables for comparison;
- timelines for workflow lifecycle;
- glossaries for terms;
- diagrams for relationship models;
- ordinary cards only for peer choices, catalogues, galleries, or inventories.

The implementation should make the page topic intelligible before metadata
dominates the screen.

### 4. Category Vertical Slices

Build in this dependency order:

1. Foundation shell and Home.
2. Physics overview and ontology, then benchmark/roadmap/flow, then
   claim-status/open-burden pages.
3. AI overview/current-state, then workflow/AgentJob lifecycle, then
   roles/human gates/validators, then memory/improvement/runtime.
4. Resources overview/source authority/registries, then
   derivatives/retrieval/publication/library, then reading paths/repository
   map/site-builder/diagrams.
5. Manifests, redirects, and old route retirement.
6. Human feedback packets and release gate.

### 5. Manifest, Provenance, And Redirect Discipline

Public route changes require route-map and provenance regeneration. Old routes
should stay available until replacement routes, internal links, redirects, and
manifests are valid. Route retirement should be one explicit packet, not a
side effect of page creation.

### 6. Human Review Gate

Automated validation can close implementation packets as technically ready,
but public acceptance requires owner review. Feedback must be handled as a
new packet that implements requested changes, reruns relevant checks, and
updates the ledger.

## Implementation Phases

1. Phase 0: Create fresh implementation-control records and confirm scope.
2. Phase 1: Build greenfield shell, content contract, review ledger, and Home.
3. Phase 2: Build Physics Research route family.
4. Phase 3: Build AI Research System route family.
5. Phase 4: Build Resources route family and reset Diagram Gallery.
6. Phase 5: Regenerate manifests, add redirects, retire obsolete old routes.
7. Phase 6: Owner review, feedback packets, final validation, and deploy
   readiness report. Deployment remains separate.

## Validation Plan

- Planning-only validation:
  - `git diff --check`
- Foundation/shared-shell packets:
  - `git diff --check`
  - `npm run validate`
  - `.venv/bin/python -m pytest`
  - desktop and mobile browser QA for `/`
- Page packets:
  - `git diff --check`
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:layout`
  - `npm run validate:comprehension`
  - `npm run validate:provenance`
  - `npm run build`
  - desktop and mobile browser QA for changed routes
- SVG or diagram packets:
  - page packet checks plus `npm run validate:svg`
  - `npm run validate:manifests`
- Manifest or route-retirement packet:
  - `npm run validate`
  - `.venv/bin/python -m pytest`
  - `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`
    against a local preview
- Release-candidate packet:
  - `npm run validate`
  - `npm run quality`
  - desktop and mobile smoke QA for representative routes
  - owner review ledger must show `reviewed and accepted`

If `npm run validate:curator` fails because of known pre-existing source drift
outside the packet, the closeout must name the concrete failing records and
show that changed greenfield routes passed their targeted checks.

## Security, Privacy, And Reliability Notes

- Data validation: source-bundle fields should be reviewed before route copy
  is written; current-state data must fail closed when stale or contradictory.
- Permissions and access control: no upstream source writes, source snapshot
  refreshes, push, or deploy without fresh authorization.
- Abuse cases: do not let public copy imply that validators, agents, roles,
  generated diagrams, memory, registries, or commits prove scientific claims.
- Privacy: preserve only intentional public creator/profile links from the
  current footer.
- Failure modes: broken route maps, stale provenance, unsupported claims,
  mobile layout overlap, and stale current-state data must block acceptance.
- Observability: every packet should report files changed, validators run,
  browser QA evidence, source bundle used, review status, and blockers.

## Rollout And Rollback Plan

- Rollout: create replacement routes alongside old routes; do not remove old
  implementation until replacement routes pass validation.
- Migration/backfill: update navigation and internal links to new routes, then
  regenerate route/provenance manifests.
- Feature flag or staged release: no runtime feature flag is needed for a
  static site; the staged release boundary is branch, route existence, and
  human review status.
- Rollback: before old route retirement, rollback is deleting new route files
  and restoring navigation. After retirement, rollback requires reverting the
  retirement commit and redirect changes.
- Monitoring: final QA should inspect route smoke tests, manifest validity,
  Cloudflare static config, and human review ledger.

## Out Of Scope

- Direct route implementation from this planning packet.
- Immediate deletion of current route files.
- Upstream source-project edits.
- Source snapshot refresh unless separately authorized.
- Diagram regeneration unless a diagram packet authorizes it.
- Scientific, mathematical, governance, or research-workflow claim promotion.
- Push or deployment.

## Final Review Checklist

- [x] Every PRD requirement is mapped to a task or deferred as an open
  question.
- [x] Every task packet has acceptance criteria.
- [x] Every task packet has validation guidance.
- [x] Risky changes have review or rollback notes.
- [x] The plan avoids direct coding.
- [x] Commands were discovered from the repository.
- [x] Product questions are separated from implementation decisions.
- [x] The old implementation is reference evidence only, not the rebuild
  architecture.

## References

The AEther Flow Website. (2026). *AGENTS.md instructions* [Repository
operating rules].

The AEther Flow Website. (2026). *Sitewide greenfield rebuild PRD* [Product
requirements document].

The AEther Flow Website. (2026). *Website information-space PRD index*
[Requirements index].

The AEther Flow Website. (2026). *PRD-00: AEther-Flow website information
space* [Master information architecture and requirements].

The AEther Flow Website. (2026). *Website information-space PRD family
validation review* [Requirements-readiness review].

The AEther Flow Website. (2026). *Public comprehension review standard*
[Maintainer-facing quality standard].
