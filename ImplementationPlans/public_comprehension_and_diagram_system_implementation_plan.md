# Public Comprehension And Diagram System Implementation Plan

Date: 2026-06-27

## Source PRD

- Source: `PRDs/public-comprehension-and-diagram-system-prd.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions
- Output companion: `ImplementationPlans/public_comprehension_and_diagram_system_task_packets.md`

## Product Summary

The PRD converts the website from a route map with short explanatory copy into
a source-derived public comprehension system. The target reader is a general
public reader who should understand what AEther Flow is, how each project
mechanism works, what the important terms mean, what diagrams and equations are
showing, and what the website is not authorized to claim.

The release starts with two Phase 1 pilots:

- `/project/overview/`, proving the general-public front-door model.
- `/project/ai-research-agent-system/parent-child-synthesis/`, proving the
  deep-topic workflow model.

The implementation must preserve the source-authority boundary: upstream
source files, registries, TeX sources, governed task records, and validators
remain authoritative. Website pages may teach, organize, promote, and link
reviewed material, but must not silently strengthen scientific, mathematical,
governance, or workflow claims.

## Repository Context

- Frameworks and languages: Astro 7 static pages, Astro components, MDX,
  TypeScript data modules, CSS, Python validation scripts, Playwright dev
  dependency, KaTeX/remark math support.
- Package manager and build system: npm with `package-lock.json`; Node engine
  is `22.x`; Astro builds static output into `dist/`.
- Existing related routes:
  - `src/pages/project/overview.astro`
  - `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro`
  - `src/pages/project/physics/**`
  - `src/pages/project/ai-research-agent-system/**`
  - `src/pages/project/operations/**`
  - `src/pages/project/source-authority/index.astro`
  - `src/pages/resources/**`
- Existing related components:
  - `src/components/InternalExplainerPage.astro`
  - `src/components/Figure.astro`
  - `src/components/EquationBlock.astro`
  - `src/components/SourceNotice.astro`
  - `src/components/ProjectRouteGrid.astro`
  - `src/components/DownloadList.astro`
- Existing related data:
  - `src/lib/internalExplainers.ts`
  - `src/lib/siteContent.ts`
  - `src/lib/manifests.ts`
  - `src/data/physics_current_state_snapshot.json`
- Existing manifest and provenance contracts:
  - `public/files/manifests/page_route_map.json`
  - `public/files/manifests/page_provenance.json`
  - `public/files/manifests/source_manifest.json`
  - `public/files/manifests/asset_manifest.json`
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
  - `python3 scripts/generate_page_provenance.py`
  - `python3 scripts/build_asset_manifest.py --write`
  - `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`
  - `python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict`

## Relevant Repository Instructions

- This repository is the reader-facing website for
  `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
- Upstream source files, registries, and governed task records remain
  authoritative for scientific, mathematical, governance, and workflow claims.
- Keep GitHub links available as provenance, but prefer internal website routes
  for primary reader journeys.
- For ontology documents, registered TeX sources carry source authority and
  PDFs are generated human-readable derivatives.
- Visual SVG artwork in `src/` and `public/assets/` must be animated and must
  not contain visible embedded text.
- Affected routes must build as static Astro pages.
- Relevant manifests and page/asset hashes must be updated after page or asset
  changes.
- Deployment is out of scope unless explicitly requested.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | Planning artifacts should be written under `ImplementationPlans/`. | Existing PRD-derived implementation plans and task packets live there. | Committing this plan |
| ASM-002 | Planning assumption | Phase 1 dossiers can seed from the local upstream source checkout at `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`, but implementation must fail closed if required source files are missing. | The current repo already generates page provenance from that source root. | Phase 1 content rewrite |
| ASM-003 | Planning assumption | Mermaid source files should live under `docs/diagram-sources/`, and generated public PNGs should live under `public/assets/diagrams/`. | The PRD asks for a maintainer documentation path for `.mmd` sources and the existing public diagram asset path already exists. | Diagram pipeline implementation |
| ASM-004 | Planning assumption | A dev-only Mermaid rendering dependency or scripted `mmdc` workflow is acceptable if it does not ship Mermaid to public browser runtime. | The PRD requires Mermaid-generated static PNGs and explicitly excludes runtime Mermaid. | Package change review |
| ASM-005 | Planning assumption | The public-comprehension audit should start as a separate command such as `npm run validate:comprehension`, not part of `npm run validate` until the rules stabilize. | The PRD open question recommends a focused quality command, and human review remains required. | Release hardening |
| ASM-006 | Planning assumption | If command-interface primitives land first, use them; otherwise implement the comprehension work inside the current Astro/CSS route structure without reopening the visual redesign. | The PRD is a sibling to the command-interface PRD, not a replacement. | Pilot page implementation |
| ASM-007 | Implementation detail | The reusable content model should support block coverage without forcing every page into the same visual sequence. | The PRD requires flexible comprehension blocks, not a rigid template. | Component design |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Planning assumption | Which human reviewer or role signs off the public-comprehension audit? | Implementation can create the checklist and mark reviewer as pending; release signoff still needs an assigned reviewer. |
| Q-002 | Planning assumption | Should the comprehension audit be added to `npm run validate` after Phase 1 or remain a separate quality gate through all phases? | Does not block Phase 1; affects how hard the gate becomes for future unrelated changes. |
| Q-003 | Implementation detail | Should secondary research routes be remediated, hidden, redirected, or retained as support routes? | Decided during the supporting-surfaces phase after a content-gap audit. |
| Q-004 | Implementation detail | Should the Mermaid renderer be a pinned dev dependency or an explicit one-off tool invocation documented in a script? | Does not change public runtime behavior; affects reproducibility and install footprint. |

No blocking question prevents a credible implementation plan.

## Requirement Traceability Matrix

| Requirement | PRD coverage | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- | --- |
| REQ-001: Source-derived comprehension model | Stories 1-7, 32-37, 49-51, 63-65 | Pages teach the subject before describing the page and avoid generic public prose. | `docs/content-dossiers/`, typed content model, shared comprehension components, audit docs | TASK-01, TASK-02, TASK-04, TASK-11 | `npm run build`, `npm run validate:comprehension` after added, human review |
| REQ-002: Overview pilot | Stories 1-4, 7, 14-16, 52, 58-59, 64-65 | `/project/overview/` explains the dual physics and AI tracks, source boundary, route jobs, and reader path. | `src/pages/project/overview.astro`, overview dossier, overview diagram, page provenance | TASK-01, TASK-03, TASK-05, TASK-11 | `npm run validate`, desktop/mobile screenshots |
| REQ-003: Parent-child pilot | Stories 3-4, 7, 9-13, 52, 58-59, 63, 65 | The parent-child page explains the one-outer-AgentJob invariant, child `draft/control` status, conflict handling, fused output, and scope limits. | `src/lib/internalExplainers.ts`, `InternalExplainerPage.astro`, parent-child route, dossier, diagram | TASK-01, TASK-02, TASK-03, TASK-06, TASK-11 | `npm run validate`, desktop/mobile screenshots |
| REQ-004: Diagram production system | Stories 11, 14, 18, 38-43, 48, 60-61 | Explanatory diagrams have Mermaid source, committed PNG output, alt text, captions, nearby prose, and manifest records. | `docs/diagram-sources/`, `public/assets/diagrams/`, manifests, render script, figure component | TASK-03, TASK-05, TASK-06, TASK-07, TASK-08, TASK-09, TASK-10 | `npm run validate:manifests`, `npm run build`, no runtime Mermaid check |
| REQ-005: Equation walkthrough model | Stories 5-6, 8, 21, 23-25 | Equations are explained in plain language with symbols, assumptions, source status, regimes, and non-proof boundaries. | `EquationBlock.astro` extension or new `EquationWalkthrough.astro`, physics dossiers/pages | TASK-02, TASK-07, TASK-11 | `npm run build`, `npm run quality`, human physics review |
| REQ-006: Dossier evidence trail | Stories 32-34, 39, 46-48, 58 | Each rewrite has tracked evidence, source basis, glossary, boundaries, diagrams, and acceptance checklist before public copy changes. | `docs/content-dossiers/`, dossier template, phase dossiers | TASK-01, TASK-05, TASK-06, TASK-07, TASK-08, TASK-09, TASK-10 | dossier review, `git diff --check` |
| REQ-007: Public-comprehension audit | Stories 49-51, 58-63 | A remediated page must pass mechanical checks plus human comprehension review. | `docs/quality/public-comprehension-audit.md`, validator script, package script, tests | TASK-04, TASK-11 | `npm run validate:comprehension`, `python3 -m pytest`, human review record |
| REQ-008: Internal-first provenance | Stories 15-17, 20, 30, 44-46, 64 | Primary reader routes stay inside the website; GitHub/source links remain visible as provenance. | route cards, related links, source links, `page_route_map.json`, `page_provenance.json` | TASK-05, TASK-06, TASK-07, TASK-08, TASK-09, TASK-10 | `npm run validate:links`, `npm run validate:provenance` |
| REQ-009: Physics route remediation | Stories 8, 21-26, 53 | Physics pages separate ontology, benchmark adoption, derivation burden, claim gates, freeze labels, and promotion status. | `src/pages/project/physics/**`, physics dossiers, diagrams, equation walkthroughs | TASK-07, TASK-11 | `npm run validate`, browser QA, physics boundary review |
| REQ-010: AI research-agent remediation | Stories 9, 27-29, 54 | AI-system pages explain workflow, roles, AgentJobs, validators, memory surfaces, and AI/physics separation. | `src/pages/project/ai-research-agent-system/**`, `internalExplainers.ts`, AI dossiers | TASK-08, TASK-11 | `npm run validate`, browser QA |
| REQ-011: Operations remediation | Stories 30-31, 55 | Operations pages explain lifecycle, role routing, validation, publication, improvement, and tools without implying physics progress. | `src/pages/project/operations/**`, operations dossiers and diagrams | TASK-09, TASK-11 | `npm run validate`, browser QA |
| REQ-012: Supporting surfaces remediation | Stories 17-20, 28, 30, 56 | Resources, documents, diagrams, source authority, and current state reinforce trust levels, drift limits, and asset status. | `src/pages/resources/**`, `src/pages/project/source-authority/**`, current-state route | TASK-10, TASK-11 | `npm run validate`, `npm run quality`, browser QA |
| REQ-013: New public page rule | Stories 44-45 | New pages are allowed only after a content-gap audit proves an existing route cannot carry the concept. | dossier template, supporting-surface audit, task checklists | TASK-01, TASK-10 | dossier review |
| REQ-014: Review evidence and accessibility | Stories 58-62 | Reviewers get before/after evidence, desktop/mobile screenshots, reduced-motion checks, and nonvisual diagram access. | `docs/quality/`, `output/playwright/`, diagram components, QA checklist | TASK-05, TASK-06, TASK-11 | screenshots, reduced-motion QA, `npm run validate:svg` |
| REQ-015: Phase sequence and handoff | Stories 52-57 | Phase 1 proves both pilot models; later families remediate in risk order and close with a remaining-backlog handoff. | task sequencing and final summary | TASK-05 through TASK-11 | final QA summary |
| REQ-016: Source authority and no-overclaim discipline | Stories 7-8, 16, 20-31, 63, out-of-scope items | Public pages teach without creating source authority, GR derivation claims, autonomous-agent claims, or validator overclaims. | all content-bearing tasks | TASK-01 through TASK-11 | source-boundary review, `npm run validate:content`, `npm run validate:provenance` |
| NFR-001: Static Astro and no runtime Mermaid | Diagram rules and testing decisions | The public browser loads static pages and committed PNGs, not Mermaid runtime rendering. | render pipeline, page components, package review | TASK-03, TASK-11 | `npm run build`, built-output runtime check |
| NFR-002: Accessibility and reduced motion | Stories 60-62 | Longer text, diagrams, equations, and retained animations remain accessible on desktop and mobile. | CSS, figures, alt text, captions, reduced-motion QA | TASK-03, TASK-05, TASK-06, TASK-11 | screenshots, reduced-motion QA |
| NFR-003: Manifest and provenance integrity | Stories 39, 46-48 | Page and asset hashes are regenerated after source or asset changes. | manifests and generators | TASK-03, TASK-05, TASK-06, TASK-11 | `npm run validate:manifests`, `npm run validate:provenance` |
| NFR-004: Safety, privacy, and reliability | Repository rules and out-of-scope items | No backend, user data, deployment, private source leakage, or authority mutation is introduced. | all tasks | TASK-01 through TASK-11 | diff review, existing validators |

## Proposed Technical Approach

### Content Dossier Layer

Add tracked maintainer dossiers under `docs/content-dossiers/`. The first task
should create a reusable template and two pilot dossiers:

- `docs/content-dossiers/_template.md`
- `docs/content-dossiers/project-overview.md`
- `docs/content-dossiers/parent-child-synthesis.md`

Each dossier should record route, reader job, current website copy summary,
mapped upstream source material, source-derived outline, glossary, claim
boundaries, required comprehension blocks, diagrams, equation walkthroughs
where applicable, safe/unsafe summaries, and a public-comprehension acceptance
checklist.

Dossiers are maintainer artifacts. They must not be added to public navigation.

### Flexible Comprehension Model

Add a small content model that can represent the PRD's required block coverage
without forcing every page into the same visual template. The likely location is
`src/lib/publicComprehension.ts`, with block types such as:

- `context`
- `plainSummary`
- `systemLogic`
- `terms`
- `sourceBasis`
- `boundary`
- `diagram`
- `equationWalkthrough`
- `safeUnsafe`
- `relatedPath`

Use thin Astro components to render reusable pieces:

- `src/components/ComprehensionBlock.astro`
- `src/components/DiagramFigure.astro`
- `src/components/EquationWalkthrough.astro`
- `src/components/SafeUnsafeSummary.astro`

The existing `InternalExplainerPage.astro` can be extended to render optional
rich comprehension blocks for data-driven pages. The overview may stay as a
custom Astro route while using the same block components for diagrams, safe
summaries, and source-boundary sections.

### Diagram Production

Use Mermaid only as a maintainer/source format. Do not load Mermaid in public
browser runtime.

Recommended locations:

- Mermaid sources: `docs/diagram-sources/*.mmd`
- Public PNG output: `public/assets/diagrams/*.png`

Phase 1 diagrams:

- `docs/diagram-sources/overview-two-track-project-map.mmd`
- `public/assets/diagrams/overview-two-track-project-map.png`
- `docs/diagram-sources/parent-child-one-outer-agentjob.mmd`
- `public/assets/diagrams/parent-child-one-outer-agentjob.png`

Implementation should add an explicit rendering command or script, for example
a package script backed by a pinned dev-only Mermaid CLI workflow. The exact
renderer choice should be documented in the task. Public assets must be
committed and added to `source_manifest.json` and `asset_manifest.json`.

### Public-Comprehension Audit

Add a human-readable audit contract and a focused scripted validator:

- `docs/quality/public-comprehension-audit.md`
- `scripts/validate_public_comprehension.py`
- tests under `tests/`
- package script such as `validate:comprehension`

The script should check mechanical requirements for remediated routes: dossier
existence, required block markers, diagram metadata, safe/unsafe summaries for
high-risk pages, equation walkthrough markers where equations are present,
internal-first route links, and absence of public Mermaid runtime wiring.

The script must not claim that comprehension has been proven. Each phase should
also record a human review note under `docs/quality/`, with reviewer identity
or pending-review status.

### Pilot Page Implementation

Remediate `/project/overview/` first after creating its dossier and diagram.
The page should explain:

- AEther Flow as a dual physics-and-AI research project.
- The physics track as exact-GR benchmark disciplined with an open substrate
  derivation burden.
- The AI track as a governed, human-scaffolded research system.
- How the two tracks co-develop.
- How readers should move through the website.
- Why source authority remains upstream.
- What the website does not claim.

Remediate `/project/ai-research-agent-system/parent-child-synthesis/` after the
overview. The page should explain:

- one Director decision, one outer AgentJob, one execution-role record, one
  completion record, and one fused output;
- why internal child perspectives exist;
- why child outputs are supporting `draft/control` artifacts;
- inherited authority;
- parent review, conflict handling, and fusion;
- unresolved blocking conflict behavior;
- scope limits and safe/unsafe summaries.

### Later Route Families

Proceed in PRD risk order:

1. Physics pages.
2. AI research-agent pages.
3. Operations pages.
4. Resources, documents, diagrams, source authority, current-state, and
   secondary/support route audit.
5. Site-wide QA and handoff.

Each family should start with dossiers, then source-derived content, diagrams
or equation walkthroughs only where useful, manifest/provenance updates, audit
results, and browser evidence.

## Implementation Phases

1. Foundation dossiers and audit contract: create dossier template, Phase 1
   dossiers, source mapping, and audit checklist. Low implementation risk; high
   value for source discipline.
2. Reusable content and diagram primitives: add content block types, diagram
   rendering pathway, and audit script. Moderate risk from package/script
   changes; keep runtime static.
3. Overview pilot: remediate `/project/overview/`, add two-track PNG diagram,
   regenerate provenance, and capture desktop/mobile evidence.
4. Parent-child pilot: remediate the parent-child page, add one-outer-AgentJob
   PNG diagram, regenerate provenance, and capture desktop/mobile evidence.
5. Physics family: remediate physics pages in highest overclaim-risk order,
   including equation walkthroughs where equations are present or substantively
   referenced.
6. AI research-agent family: remediate workflow, roles and skills, and memory
   and registries using lessons from the parent-child pilot.
7. Operations family: remediate operational lifecycle, role routing,
   validators, publication process, project-system improvement, and technical
   requirements.
8. Supporting surfaces: remediate resources, documents, diagrams, source
   authority, current-state, and decide secondary route treatment through a
   content-gap audit.
9. Site-wide QA and handoff: run validators, browser QA, reduced-motion checks,
   diagram/manifest checks, human audit, and produce a remaining backlog.

## Codex Task Packets

See `ImplementationPlans/public_comprehension_and_diagram_system_task_packets.md`.

## Validation Plan

Use current repository commands where they already exist:

- Static checks: `npm run validate:content`, `npm run validate:links`,
  `npm run validate:svg`, `npm run validate:provenance`
- Manifest checks: `npm run validate:manifests`
- Unit tests: `python3 -m pytest`
- Build: `npm run build`
- Full gate: `npm run validate`
- Quality gate: `npm run quality`
- Browser smoke test on a running server:
  `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`
- Project explainer audit after build:
  `python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict`

Add these commands during implementation, then run them where relevant:

- Mermaid PNG rendering command, exact name to be created by TASK-03.
- `npm run validate:comprehension`, created by TASK-04.

Manual QA required for each remediated phase:

- Desktop screenshot of representative remediated routes.
- Mobile screenshot of representative remediated routes.
- Reduced-motion behavior check when animated SVGs or motion-heavy surfaces are
  affected.
- Diagram readability and overflow check.
- Human public-comprehension checklist.

## Security, Privacy, And Reliability Notes

- Data validation: new scripts should validate public paths, safe relative
  paths, dossier references, diagram metadata, and source manifest IDs.
- Permissions and access control: no authentication or user permissions are
  introduced.
- Abuse cases and rate limits: not applicable to the static site.
- Privacy: do not expose local absolute paths, private source paths, or local
  machine state in public manifests, page copy, diagrams, or screenshots.
- Reliability: keep the public site static; no runtime Mermaid, no backend, no
  live source-repository dependency during Cloudflare page serving.
- Observability: use checked-in QA notes, validation output summaries, page
  provenance, asset manifests, and screenshots as release evidence.

## Rollout And Rollback Plan

- Rollout: implement in vertical slices by route or route family, beginning
  with the two Phase 1 pilots.
- Migration/backfill: no database migration. Public page changes require page
  provenance regeneration. Public diagram assets require source and asset
  manifest updates.
- Feature flag or staged release: not needed for static pages. Use reviewable
  draft PRs or branches per task packet.
- Rollback: revert a route-specific page, dossier, diagram, and manifest
  update together. Regenerate page provenance after rollback. If a Mermaid
  pipeline change is unstable, keep committed PNGs and revert only the tooling.
- Monitoring: use local validation, browser QA, and post-deploy smoke tests
  only if deployment is later explicitly authorized.

## Out Of Scope

- Deploying the site.
- Replacing the command-interface redesign PRD.
- Reopening the color schema, animation identity, deployment model, or primary
  route families.
- Adding runtime Mermaid to public pages.
- Building a custom PDF viewer.
- Rendering full TeX documents into HTML.
- Publishing private, draft/control, or unreviewed upstream material as
  authoritative public claims.
- Changing upstream scientific, mathematical, governance, validator, role,
  memory, routing, or research-control authority.
- Claiming that GR has been derived from the AEther Flow ontology.
- Claiming that AI agents autonomously own research decisions, authorship, or
  public release accountability.
- Adding new public pages without a content-gap audit.

## Final Review Checklist

- [ ] Every PRD requirement is mapped to a task or explicitly deferred.
- [ ] Every task has acceptance criteria.
- [ ] Every task has validation guidance.
- [ ] Risky changes have review or rollback notes.
- [ ] The plan avoids direct coding beyond planning artifacts.
- [ ] Commands were discovered from the repository or marked as commands that a
      task must create.
- [ ] Product questions are separated from implementation decisions.
- [ ] Source-authority boundaries are preserved.
- [ ] Internal website routes remain the primary reader journey.
- [ ] Human comprehension review remains separate from scripted validation.

## References

AEther-Flow Project. (2026). *Parent-child parallel synthesis* [Generated
noncanonical reader surface]. `github-facing/parent-child-synthesis-explainer.md`.

AEther-Flow Project. (2026). *Project overview* [Generated noncanonical reader
surface]. `github-facing/project-overview-explainer.md`.

AEther-Flow Project. (2026). *The Æther-Flow interpretation of relativity
research project* [Source repository front door]. `README.md`.

The AEther Flow Website. (2026). *AGENTS.md instructions* [Repository operating
rules]. `AGENTS.md`.

The AEther Flow Website. (2026). *Internal explainer and source assets PRD*
[Product requirements document]. `PRDs/internal-explainer-and-source-assets-prd.md`.

The AEther Flow Website. (2026). *Project features and functionality*
[Maintainer operating map]. `docs/project-features-and-functionality.md`.

The AEther Flow Website. (2026). *Public comprehension and diagram system PRD*
[Product requirements document]. `PRDs/public-comprehension-and-diagram-system-prd.md`.

The AEther Flow Website. (2026). *Site-wide formidable command-interface
redesign PRD* [Product requirements document].
`PRDs/site-wide-formidable-command-interface-redesign-prd.md`.
