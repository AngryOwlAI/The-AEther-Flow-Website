# Public Comprehension And Diagram System Implementation Plan

Date: 2026-06-27

## Source PRD

- Source: `PRDs/public-comprehension-and-diagram-system-prd.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions
- Output companion: `ImplementationPlans/public_comprehension_and_diagram_system_task_packets.md`

## Product Summary

The PRD asks for a source-derived public comprehension system for The AEther
Flow Website. The problem is not only page structure or visual polish. The
problem is that current public pages can look organized while still failing to
teach unfamiliar readers what the project is, how its mechanisms work, what its
terms mean, which sources support each explanation, and what the website must
not claim.

The implementation should add four durable practices:

1. Tracked maintainer-facing content dossiers under `docs/content-dossiers/`.
2. A reusable comprehension content model for context, summaries, mechanisms,
   terms, diagrams, equations, source basis, boundaries, safe/unsafe summaries,
   and related internal routes.
3. Mermaid-authored, statically generated PNG diagrams committed under
   `public/assets/diagrams/comprehension/`, with Mermaid sources kept in the
   matching content dossier.
4. A public-comprehension audit gate that combines scripted checks with human
   review and does not treat ordinary validator PASS as sufficient evidence of
   reader understanding.

Phase 1 remediates two pilot routes: `/project/overview/` and
`/project/ai-research-agent-system/parent-child-synthesis/`. Later phases
remediate physics pages, AI research-agent pages, operations pages, and
supporting resource/source-authority/current-state surfaces.

## Repository Context

- Frameworks and languages: Astro 7 static site, Astro components, MDX, CSS,
  TypeScript data modules, Python validation scripts, KaTeX, and Playwright.
- Package manager and build system: npm with `package-lock.json`; Node engine
  is `22.x`; Astro builds static output to `dist/`.
- Current route surfaces:
  - `src/pages/project/overview.astro`
  - `src/pages/project/physics/**`
  - `src/pages/project/ai-research-agent-system/**`
  - `src/pages/project/operations/**`
  - `src/pages/project/source-authority/index.astro`
  - `src/pages/resources/**`
  - secondary research support routes under `src/pages/research/`
- Current reusable components:
  - `src/components/CommandBand.astro`
  - `src/components/EvidenceRail.astro`
  - `src/components/StatusDossier.astro`
  - `src/components/InternalExplainerPage.astro`
  - `src/components/ProjectRouteGrid.astro`
  - `src/components/Figure.astro`
  - `src/components/EquationBlock.astro`
  - `src/components/SourceNotice.astro`
- Current data modules:
  - `src/lib/siteContent.ts`
  - `src/lib/internalExplainers.ts`
  - `src/lib/manifests.ts`
  - `src/data/physics_current_state_snapshot.json`
- Current manifests:
  - `public/files/manifests/page_route_map.json`
  - `public/files/manifests/page_provenance.json`
  - `public/files/manifests/source_manifest.json`
  - `public/files/manifests/asset_manifest.json`
- Existing validation commands discovered from `package.json` and repository
  tooling:
  - `npm run build`
  - `npm run validate`
  - `npm run quality`
  - `npm run validate:manifests`
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:layout`
  - `npm run validate:svg`
  - `npm run validate:provenance`
  - `npm run validate:curator`
  - `npm run validate:cloudflare`
  - `python3 -m pytest`
  - `python3 scripts/generate_page_provenance.py --write`
  - `python3 scripts/build_asset_manifest.py --write`
  - `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`

## Relevant Repository Instructions

- This repository is the reader-facing website for
  `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
- Upstream source files, registries, and governed task records remain
  authoritative for scientific, mathematical, governance, and workflow claims.
- Website pages may explain, organize, promote, and link reviewed material, but
  must not silently strengthen or create source claims.
- GitHub links must remain available as provenance; primary reader journeys
  should prefer internal website routes.
- Registered TeX sources carry ontology authority; PDFs are generated
  human-readable derivatives.
- Visual SVG figures must be animated and must not contain visible embedded
  text.
- Page and asset hashes must be regenerated after page or public-asset changes.
- Deployment is explicitly out of scope unless separately authorized.

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | Planning artifacts belong in `ImplementationPlans/`. | Existing repo-local planning artifacts use `ImplementationPlans/`, and memory plus repository state confirm that convention. | Committing planning artifacts |
| ASM-002 | Planning assumption | Mermaid source files should live inside the matching dossier directory, for example `docs/content-dossiers/project-overview/diagrams/two-track-map.mmd`. | The PRD wants tracked maintainer artifacts outside public navigation; colocating diagram source with its dossier preserves editorial context. | Starting diagram implementation |
| ASM-003 | Planning assumption | Generated public diagram PNGs should live under `public/assets/diagrams/comprehension/`. | The repo already uses `public/assets/diagrams/` for public diagram assets; a `comprehension/` child keeps PRD-generated diagrams separate from existing fixtures. | Adding Phase 1 diagram assets |
| ASM-004 | Planning assumption | `npm run validate:comprehension` should be added as a separate command before being folded into `npm run validate`. | The PRD asks whether the audit should become hard validation; a separate focused command is safer until review rules stabilize. | Phase 1 release readiness |
| ASM-005 | Planning assumption | Build-time Mermaid rendering may use a dev-time tool, but no public Mermaid runtime script or client dependency should be added. | The PRD forbids runtime Mermaid, not build-time rendering. | Adding rendering tooling |
| ASM-006 | Planning assumption | The existing command-interface primitives should be reused for public comprehension layouts rather than replaced. | `CommandBand`, `EvidenceRail`, and `StatusDossier` already exist and satisfy the sibling command-interface PRD. | Building reusable comprehension components |
| ASM-007 | Planning assumption | Phase 1 can introduce a small new comprehension data contract before migrating every route family. | The PRD requires scalability but also asks for a two-page pilot first. | Coding Phase 1 |
| ASM-008 | Implementation detail | Human review evidence can start as tracked Markdown under `docs/quality/` with screenshot paths pointing to local artifacts under `output/playwright/`. | Existing QA notes use `docs/quality/`; screenshots are normally local artifacts. | Phase QA closeout |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Planning assumption | Who signs off the human public-comprehension audit? | Implementation can add the audit structure, but release readiness needs a named reviewer or accepted owner signoff. |
| Q-002 | Implementation detail | Should Mermaid rendering use a checked-in dev dependency, `npx --yes @mermaid-js/mermaid-cli`, or an externally documented local tool? | Does not block planning. It affects reproducibility, install cost, and CI behavior. |
| Q-003 | Implementation detail | Should `npm run validate:comprehension` later become part of `npm run validate` or stay under `npm run quality` only? | Phase 1 should keep it separate; later hardening can decide whether it is stable enough for the full gate. |
| Q-004 | Implementation detail | Which secondary research/support routes should be remediated, de-emphasized, redirected, or retained as support pages? | Phase 5 can decide this with a content-gap audit. |

No blocking question prevents a credible implementation plan.

## Requirement Traceability Matrix

| Requirement | PRD coverage | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- | --- |
| REQ-001: Dossier-first rewrites | Stories 32-34, 46 | Every rewritten page has a tracked maintainer dossier explaining evidence, source basis, glossary, boundaries, diagrams, equations, and acceptance criteria. | `docs/content-dossiers/**`, dossier template, source review workflow | TASK-01, TASK-02, TASK-09, TASK-10, TASK-11 | `npm run validate:comprehension`, human review |
| REQ-002: Flexible comprehension model | Stories 2-7, 35-37 | Pages can present context, summary, mechanisms, terms, source basis, boundaries, diagrams, equations, safe/unsafe summaries, and related paths without a rigid template. | `src/lib/comprehensionContent.ts`, `src/components/*`, `InternalExplainerPage.astro`, route files | TASK-03, TASK-06, TASK-07, TASK-09, TASK-10, TASK-11 | `npm run build`, browser QA |
| REQ-003: Overview pilot | Stories 1, 14-16, 64-65 | `/project/overview/` explains the dual physics and AI research project before route selection. | `src/pages/project/overview.astro`, overview dossier, overview diagram PNG | TASK-02, TASK-04, TASK-06, TASK-08 | screenshots, `npm run validate:links`, `npm run validate:provenance` |
| REQ-004: Parent-child pilot | Stories 10-13, 52 | Parent-child synthesis opens with the one-outer-AgentJob invariant and explains inherited authority, draft/control child artifacts, conflict handling, fused output, and scope limits. | `src/lib/internalExplainers.ts`, `InternalExplainerPage.astro`, parent-child route, dossier, diagram PNG | TASK-02, TASK-04, TASK-07, TASK-08 | screenshots, `npm run validate:content`, `npm run validate:comprehension` |
| REQ-005: Static diagram system | Stories 11, 14, 18, 38-43 | Diagrams are editable as Mermaid source, generated to committed PNG assets, and rendered with alt text, captions, and nearby explanations. | `docs/content-dossiers/**/diagrams/*.mmd`, `public/assets/diagrams/comprehension/*.png`, `Figure.astro`, manifests, render script | TASK-04, TASK-06, TASK-07, TASK-09, TASK-10, TASK-11 | `npm run validate:manifests`, `npm run validate:comprehension`, browser QA |
| REQ-006: No public Mermaid runtime | Story 40 and testing decisions | Public pages serve static images and do not load Mermaid in the browser. | route files, `package.json`, audit script | TASK-04, TASK-05, TASK-08 | `npm run validate:comprehension`, dependency diff review |
| REQ-007: Source authority and boundaries | Stories 7, 16, 20, 46, 63-64 | Pages state what each topic does not prove or authorize and keep source links as provenance. | `SourceNotice.astro`, page copy, manifests, dossiers | TASK-02, TASK-03, TASK-05 through TASK-11 | `npm run validate:content`, `npm run validate:links`, human review |
| REQ-008: Equation walkthroughs | Stories 5-6, 21, 23-25 | Equations include plain-language explanations, symbol meanings, assumptions, source status, and limits. | `EquationBlock.astro`, comprehension data model, physics pages, MDX support routes | TASK-03, TASK-05, TASK-09, TASK-11 | `npm run build`, `npm run validate:comprehension`, mobile QA |
| REQ-009: Physics route remediation | Stories 8, 21-26, 53 | Physics pages separate ontology, benchmark adoption, derivation burden, no-go/freeze records, and claim promotion. | `src/pages/project/physics/**`, `siteContent.ts`, physics dossiers, diagrams | TASK-09 | `npm run validate:content`, `npm run validate:provenance`, screenshots |
| REQ-010: AI research-agent remediation | Stories 9, 27-29, 54 | AI-system pages explain operational mechanics, roles, AgentJobs, validators, memory, registries, and authority limits. | `src/pages/project/ai-research-agent-system/**`, `internalExplainers.ts`, AI dossiers, diagrams | TASK-10 | `npm run validate:content`, `npm run validate:links`, screenshots |
| REQ-011: Operations remediation | Stories 30-31, 55 | Operations pages explain lifecycle, role routing, validation, publication, improvement, and tool tiers while keeping PASS bounded. | `src/pages/project/operations/**`, `internalExplainers.ts`, operations dossiers, diagrams | TASK-10 | `npm run validate:content`, screenshots |
| REQ-012: Supporting-surface remediation | Stories 17-20, 56 | Resources, documents, diagrams, source authority, and current-state pages explain trust boundaries, TeX/PDF status, diagram limits, and snapshot drift. | `src/pages/resources/**`, `src/pages/project/source-authority/**`, `src/pages/project/physics/current-state/**`, manifests | TASK-11 | `npm run validate:manifests`, `npm run validate:provenance`, screenshots |
| REQ-013: New page rule | Stories 44-45 | New public pages are added only after a content-gap audit. | dossier template, audit script, task packet guidance | TASK-01, TASK-05, TASK-11 | human review, `npm run validate:comprehension` |
| REQ-014: Before/after evidence | Stories 58-59 | Reviewers can compare baseline and remediated pages on desktop and mobile. | `docs/quality/**`, `output/playwright/**`, browser QA | TASK-08, TASK-09, TASK-10, TASK-11 | screenshots, QA notes |
| REQ-015: Accessibility and motion safety | Stories 60-62 | Diagrams have alt text, captions, nearby prose, keyboard-safe links, and reduced-motion-respecting surrounding visuals. | `Figure.astro`, CSS, route markup, Playwright QA | TASK-04, TASK-06, TASK-07, TASK-08 through TASK-11 | browser QA, `npm run validate:svg`, `npm run validate:comprehension` |
| REQ-016: Safe/unsafe summaries | Stories 7, 12-13, 22, 63 | High-risk pages include concise correct and incorrect summaries to reduce overclaim risk. | comprehension data model, page copy, dossiers | TASK-03, TASK-06, TASK-07, TASK-09, TASK-10, TASK-11 | `npm run validate:comprehension`, human review |
| REQ-017: Manifest and hash integrity | Stories 39, 47-48 | Page provenance and asset manifests are updated after page and diagram changes. | `page_provenance.json`, `source_manifest.json`, `asset_manifest.json`, scripts | TASK-04, TASK-06 through TASK-11 | `npm run validate:manifests`, `npm run validate:provenance` |
| REQ-018: Internal-first reader journeys | Stories 15-16, 64 | Route links explain reader jobs and keep the primary journey inside the website. | route copy, `ProjectRouteGrid.astro`, `EvidenceRail.astro`, link validator | TASK-03, TASK-06 through TASK-11 | `npm run validate:links`, browser QA |
| REQ-019: Phased sequence and handoff | Stories 52-57 | The rollout remediates pilot pages first, then physics, AI, operations, supporting surfaces, and final QA/backlog. | implementation task sequencing, closeout docs | TASK-08 through TASK-11 | phase QA notes, final checklist |
| REQ-020: Generic prose rejection | Problem statement, Story 65 | Public pages stop sounding generic by teaching specific AEther Flow mechanisms from source evidence. | dossiers, page copy, comprehension audit, human review | TASK-01 through TASK-11 | human review, `npm run validate:comprehension` |
| NFR-001: Static Astro compatibility | PRD testing decisions | All affected routes build as static Astro pages. | Astro routes and components | TASK-03 through TASK-11 | `npm run build` |
| NFR-002: No upstream authority changes | PRD assumptions and out of scope | Website implementation does not change source research authority or claim status. | all public copy and manifests | TASK-01 through TASK-11 | source-boundary review, `npm run validate:content` |
| NFR-003: No public runtime diagram dependency | Diagram rules and out of scope | Mermaid stays build-time or maintainer-side only. | `package.json`, route markup, scripts | TASK-04, TASK-05, TASK-08 | `npm run validate:comprehension`, dependency review |
| NFR-004: Reviewable incremental delivery | Phased delivery requirements | Each phase can be implemented, validated, and reviewed in bounded PR-sized packets. | task packets, QA notes, manifests | TASK-01 through TASK-11 | task-level validation summaries |
| NFR-005: Accessibility and responsive layout | Stories 59-62 | Longer explanations, diagrams, and equations do not overlap or become inaccessible on mobile. | CSS, components, browser QA | TASK-03 through TASK-11 | Playwright desktop/mobile screenshots |

## Proposed Technical Approach

### Architecture

Use the existing static Astro architecture. Do not introduce a backend, a
database, or a public client-side diagram renderer.

Add a small source-backed comprehension layer:

1. `docs/content-dossiers/<page-slug>/dossier.md` records the editorial source
   contract before each rewrite.
2. `docs/content-dossiers/<page-slug>/diagrams/*.mmd` stores editable Mermaid
   source for page-specific explanatory diagrams.
3. `public/assets/diagrams/comprehension/*.png` stores generated static public
   diagram assets.
4. `src/lib/comprehensionContent.ts` defines reusable content types for
   context, mechanism steps, term groups, diagram metadata, equation
   walkthroughs, source basis, boundaries, safe/unsafe summaries, and related
   internal routes.
5. Existing `CommandBand`, `EvidenceRail`, and `StatusDossier` components
   present comprehension blocks in the command-interface visual language.
6. `Figure.astro` and `EquationBlock.astro` are extended only as needed to
   support the PRD's accessibility and walkthrough contract.

### Content Dossiers

Each dossier should include:

- Route and reader job.
- Current website copy summary.
- Upstream source list and source-status notes.
- Source-derived topic outline.
- Glossary terms.
- Claim boundaries and forbidden implications.
- Required comprehension blocks.
- Required diagrams with Mermaid source path, PNG path, alt text, caption, and
  manifest impact.
- Required equation walkthroughs where applicable.
- Safe/unsafe summary pairs for high-risk pages.
- New-page audit result if a new page is proposed.
- Human comprehension review checklist.

Dossiers are maintainer artifacts. They must not be linked as public website
navigation.

### Diagram Pipeline

Recommended file layout:

```text
docs/content-dossiers/project-overview/dossier.md
docs/content-dossiers/project-overview/diagrams/two-track-project-map.mmd
docs/content-dossiers/parent-child-synthesis/dossier.md
docs/content-dossiers/parent-child-synthesis/diagrams/single-outer-agentjob-frame.mmd
public/assets/diagrams/comprehension/project-overview-two-track-map.png
public/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png
```

Add a script such as `scripts/render_mermaid_diagrams.py` that renders declared
Mermaid sources into PNG assets. The implementation should either:

- use `npx --yes @mermaid-js/mermaid-cli` and document the network/tooling
  expectation, or
- add `@mermaid-js/mermaid-cli` as a dev dependency only, with no public
  runtime bundle impact.

After generating PNGs, update `public/files/manifests/source_manifest.json` and
run `python3 scripts/build_asset_manifest.py --write`.

### Public Comprehension Audit

Add `scripts/validate_public_comprehension.py` and a package script:

```json
"validate:comprehension": "python3 scripts/validate_public_comprehension.py"
```

Initial scripted checks should be mechanical and conservative:

- Remediated routes have matching dossiers.
- Dossiers contain required headings.
- Diagram references have `.mmd` source, PNG output, alt text, caption, and
  manifest reference.
- Public pages do not include Mermaid runtime scripts.
- High-risk pages declare boundary and safe/unsafe summary blocks.
- Equation blocks or substantive equation references have walkthrough data.
- Internal related routes are present before source/provenance links.

The audit must also require a human review note for remediated pages, because
scripts cannot prove public comprehension.

### UI And Routing

- Phase 1 modifies `/project/overview/` and
  `/project/ai-research-agent-system/parent-child-synthesis/`.
- Existing routes remain stable unless a later content-gap audit justifies a
  new public page.
- Existing GitHub/source links remain available as provenance, not primary
  reader paths.
- The command-interface PRD remains the presentation layer. This PRD supplies
  source-derived explanatory content and page-specific diagram/equation
  contracts.

### Data, API, Schema, And State

- No backend API or database migration is needed.
- Content data can live in TypeScript modules and Markdown dossiers.
- Existing route map and provenance manifests remain the page-source contract.
- Public diagram assets require source and asset manifest updates.
- Page source edits require page provenance regeneration.

### Error Handling And Empty States

- Static pages do not need loading states.
- Comprehension components should fail at build time for missing required
  props rather than silently rendering empty explanation sections.
- Optional blocks may be omitted only when the dossier says why they are not
  needed.

### Security, Privacy, And Reliability

- No user data, authentication, permissions, or rate limiting are introduced.
- Avoid public leakage of local absolute paths in manifests, generated assets,
  and QA notes.
- Keep runtime static and Cloudflare-compatible.
- Treat build-time diagram tooling as a reproducibility concern; document the
  exact command and version approach.
- Preserve source-authority boundaries to reduce overclaim and downstream
  summarizer risk.

### Observability And QA Evidence

No runtime telemetry is required. Use repository evidence:

- validation command summaries,
- page provenance and asset hashes,
- human comprehension review notes,
- desktop/mobile screenshots,
- reduced-motion notes where affected,
- before/after comparison notes under `docs/quality/`.

## Implementation Phases

1. Phase 0: Dossier and audit foundation. Add the dossier template, audit
   criteria, and initial validation command surface.
2. Phase 1A: Pilot dossiers. Create source-grounded dossiers for overview and
   parent-child synthesis before public copy changes.
3. Phase 1B: Content model and rendering primitives. Extend the existing Astro
   content model and components to support the comprehension blocks.
4. Phase 1C: Static diagram pipeline. Add Mermaid source, render PNGs, update
   manifests, and confirm no public Mermaid runtime.
5. Phase 1D: Overview remediation. Rewrite the overview through the new
   dossier-backed model, with internal-first route guidance and a two-track
   diagram.
6. Phase 1E: Parent-child remediation. Rewrite parent-child synthesis through
   the one-outer-AgentJob invariant, scope limits, conflict behavior, and a
   static diagram.
7. Phase 1F: Pilot validation. Run standard validators, comprehension audit,
   browser QA, screenshots, reduced-motion checks, and human review.
8. Phase 2: Physics route remediation. Remediate physics pages in overclaim
   risk order.
9. Phase 3 and 4: AI-system and operations remediation. Apply lessons from the
   parent-child pilot to operational route families.
10. Phase 5: Supporting surfaces. Remediate resources, documents, diagrams,
    source authority, current-state, and secondary route decisions.
11. Phase 6: Site-wide QA and handoff. Run final validation, record remaining
    backlog, and prepare a follow-on closeout or implementation plan.

## Codex Task Packets

Task packets are in
`ImplementationPlans/public_comprehension_and_diagram_system_task_packets.md`.

## Validation Plan

- Static checks:
  - `npm run validate:manifests`
  - `npm run validate:content`
  - `npm run validate:links`
  - `npm run validate:layout`
  - `npm run validate:svg`
  - `npm run validate:provenance`
  - `npm run validate:cloudflare`
- New comprehension gate:
  - `npm run validate:comprehension` after TASK-05 adds it.
- Python tests:
  - `python3 -m pytest`
- Build:
  - `npm run build`
- Full repository gate:
  - `npm run validate`
  - `npm run quality` when route, asset, or rendered frontend behavior changes.
- Page provenance:
  - `python3 scripts/generate_page_provenance.py --write`
- Asset manifest:
  - `python3 scripts/build_asset_manifest.py --write`
- Browser QA:
  - Start the local server with `npm run dev -- --host 127.0.0.1 --port 4321`
    or preview a built site.
  - `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`
  - Capture desktop and mobile screenshots for remediated pages.
- Manual QA:
  - Human comprehension review against dossier acceptance criteria.
  - Confirm diagrams teach the topic and do not replace necessary prose.
  - Confirm equations have walkthroughs when displayed or substantively
    referenced.
  - Confirm GitHub/source links are provenance links.

## Security, Privacy, And Reliability Notes

- Data validation: manifest schemas and custom validators should reject missing
  public asset files, missing source references, stale hashes, missing alt
  text, missing captions, and absent dossiers.
- Permissions and access control: no permission system is introduced.
- Abuse cases and rate limits: not applicable for a static website.
- Privacy: avoid local absolute paths and private draft/control source content
  in public pages.
- Failure modes:
  - Diagram render command unavailable.
  - PNG generated but manifest not updated.
  - Page source changed but provenance hash stale.
  - Public page loads Mermaid runtime by accident.
  - Human review note absent.
  - Longer content creates mobile overlap.
- Recovery:
  - Revert the affected page or asset changes.
  - Regenerate manifests and provenance.
  - Keep dossiers and diagrams reviewable in their own small PRs.
- Observability:
  - QA notes and validation summaries are the durable evidence.

## Rollout And Rollback Plan

- Rollout:
  - Implement Phase 1 in small PR-sized packets.
  - Validate pilot routes before migrating route families.
  - Use screenshots and human review before declaring public comprehension
    improvements complete.
- Migration/backfill:
  - Backfill dossiers per route before rewriting the corresponding public page.
  - Add diagram assets only when the dossier says a diagram improves
    explanation.
- Feature flag or staged release:
  - No runtime flag is needed. Use branch/PR review and static deploy
    readiness.
- Rollback:
  - Revert specific route, manifest, and asset changes together.
  - Remove orphaned generated PNGs from manifests.
  - Regenerate page provenance after rollback.
- Monitoring:
  - Use local validation, quality gate, screenshots, and post-deploy smoke tests
    only if deployment is later authorized.

## Out Of Scope

- Direct implementation during this planning task.
- Deployment.
- Reopening the command-interface visual redesign PRD.
- Reopening the color schema or animation identity.
- Adding Mermaid as a public runtime dependency.
- Rendering full TeX documents into HTML.
- Building a custom PDF viewer.
- Publishing private or draft/control source material as authoritative public
  claims.
- Changing upstream scientific, mathematical, governance, validator, role,
  routing, memory, or research-control authority.
- Claiming that GR has been derived from the AEther Flow ontology.
- Claiming that AI agents own research decisions, authorship, or public release
  accountability.
- Adding new public pages without a content-gap audit.

## Final Review Checklist

- [x] The source PRD path is identified.
- [x] Planning status is `Ready with assumptions`.
- [x] Every PRD requirement is mapped to a task or route-family phase.
- [x] Functional and non-functional requirements are represented.
- [x] Explicit exclusions and constraints are preserved.
- [x] Open questions are classified by impact.
- [x] Repository architecture was inspected before planning.
- [x] Existing patterns are preferred over new abstractions.
- [x] New dependencies, migrations, or broad refactors are avoided or bounded.
- [x] Likely affected files and directories are named.
- [x] Data, UI, accessibility, error handling, reliability, rollout, and
      rollback are covered.
- [x] Task packets include acceptance criteria and validation guidance.
- [x] The plan avoids direct coding.
- [x] Upstream source authority is preserved.

## References

The AEther Flow Website. (2026). `AGENTS.md` [Repository operating rules].

The AEther Flow Website. (2026). `PRDs/public-comprehension-and-diagram-system-prd.md`
[Product requirements document].

The AEther Flow Website. (2026). `docs/project-features-and-functionality.md`
[Maintainer operating map].

The AEther Flow Website. (2026). `package.json` [Repository scripts and
dependencies].
