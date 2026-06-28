# Implementation Plan: Sitewide Page Revamp

## Source PRD

- Source: Grill-me session in this Codex thread, accepted decisions Q1-Q29.
- Canonical scope map: `docs/system-analyses/aether-flow-website-topic-inventory.md`.
- Generated for: Codex app, Codex IDE, and page-scoped `to-web-page` execution packets.
- Branch: `codex/revamp-all-pages`.
- Planning status: Ready with assumptions.

## Product Summary

The project needs a full reader-facing page revamp for The AEther Flow Website.
The accepted scope treats `aether-flow-website-topic-inventory.md` as the
canonical page map. Existing routes that overlap inventory topics should be
rewritten in place. Missing inventory topics should become new internal-first
routes. Existing utility, resource, index, and prototype-like pages should be
redesigned, consolidated, or retired when they do not serve an inventory-backed
reader job.

The primary reader is the general public. Each page must begin with a clear
plain-language explanation of the topic, why it matters, and what it does not
claim. Deeper sections may target physicists, mathematicians, system engineers,
software engineers, AI developers, engineers, scientists, reviewers, or
maintainers depending on the page topic.

The revamp should preserve animated SVG artwork where useful, preserve the
Astro static-site and manifest/provenance infrastructure, and replace weak
public-facing copy, layout hierarchy, navigation, and explanatory framing. The
site should read as a public science field guide, not a marketing page and not
a collection of generated summaries.

Deployment is explicitly out of scope. Implementation on this branch must not
deploy without a separate user approval.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content libraries,
  Markdown/MDX, Python validation scripts.
- Package manager and build system: npm with `astro build`.
- Existing route families: `/project/physics/`,
  `/project/ai-research-agent-system/`, `/project/operations/`,
  `/project/source-authority/`, and `/resources/`.
- Existing page infrastructure:
  - `src/pages/` for Astro routes.
  - `src/components/InternalExplainerPage.astro`,
    `ComprehensionBlocks.astro`, `Figure.astro`, `EvidenceRail.astro`,
    `SourceNotice.astro`, and `StatusDossier.astro` for reusable explainer
    surfaces.
  - `src/lib/internalExplainers.ts`, `src/lib/*ComprehensionContent.ts`, and
    `src/lib/siteContent.ts` for typed content.
  - `docs/content-dossiers/` for page dossiers and diagram sources.
  - `public/files/manifests/page_route_map.json`,
    `source_manifest.json`, `asset_manifest.json`, and
    `page_provenance.json` for route/source/asset provenance.
  - `scripts/validate_public_comprehension.py`,
    `scripts/render_mermaid_diagrams.py`, and
    `scripts/generate_page_provenance.py` for route registration and generated
    evidence.
- Repository rules:
  - Source authority remains upstream in `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
  - Website pages may explain, organize, and link reviewed material, but must
    not silently strengthen scientific, mathematical, governance, or
    research-workflow claims.
  - GitHub/source links are provenance. Internal website routes are the
    primary reader journey.
  - Visual SVG figures must remain animated and must not contain visible
    embedded text.
- Discovered validation commands:
  - `npm run validate:comprehension`
  - `npm run validate:manifests`
  - `npm run validate:content`
  - `npm run validate:provenance`
  - `npm run validate:svg`
  - `npm run validate:links`
  - `npm run validate`
  - `npm run quality`
  - `npm run build`
  - `python3 -m pytest`

## Accepted PRD Decisions

| ID | Decision |
| --- | --- |
| DEC-001 | Treat `docs/system-analyses/aether-flow-website-topic-inventory.md` as the canonical scope map. |
| DEC-002 | Build a shared foundation first, then execute page-by-page. |
| DEC-003 | Every claim-bearing topic page must receive or reuse a completed `docs/system-analyses/*.md` artifact before `to-web-page` creates or rewrites the route. |
| DEC-004 | Live-state pages must refresh from a clean, committed upstream state and record source commit or file hashes in manifests/provenance. |
| DEC-005 | Preserve animated SVG artwork, Astro, validators, manifests, provenance generation, content dossiers, and structurally useful components. Rewrite weak prose and page hierarchy. |
| DEC-006 | Keep and strengthen existing route families: physics, AI research-agent system, operations, source authority, and resources. |
| DEC-007 | Use one foundation packet, then one page-scoped `to-web-page` packet per page or route rewrite. |
| DEC-008 | Require a `no-ai-slop` builder/refuter gate with `pass`, `repair`, or `block`; page readiness requires `pass`. |
| DEC-009 | Use a layered page model: public layer, mechanism layer, evidence layer, specialist layer, and navigation layer. |
| DEC-010 | Use one common content contract with track-specific emphasis. |
| DEC-011 | Treat existing page prose as suspect by default; reuse only after evidence review and anti-slop pass. |
| DEC-012 | Plan every candidate item in the inventory; use the recommended build order only for the first wave. |
| DEC-013 | Include an explicit inventory-to-route matrix. |
| DEC-014 | Use a public science field-guide visual standard. |
| DEC-015 | Consolidate or retire prototype/sample routes that lack an inventory-backed reader job. |
| DEC-016 | Redesign bounded sitewide navigation before page implementation. |
| DEC-017 | Include guided-start routes or sections for the general public and specialist audiences. |
| DEC-018 | Stage the reviewer packet behind authority/orientation prerequisites. |
| DEC-019 | First implementation wave prioritizes current state, Distance-to-GR, source extension, Gate Chair/human gates, claim boundaries/source authority, and general-public guided start. |
| DEC-020 | Shared components may be updated in page packets only when local page changes cannot solve a reusable need; affected routes must then be verified. |
| DEC-021 | Desktop and mobile browser QA are mandatory for every page packet. |
| DEC-022 | Use tiered validation: page minimum, SVG/link additions, foundation/shared-component full validation, and release-candidate quality. |
| DEC-023 | Do not deploy from the revamp branch without explicit follow-up approval. |
| DEC-024 | Use milestones: foundation, first-wave authority/orientation, physics deepening, AI research-agent pages, operations/source-authority/resources, guided starts/reviewer packet/retirement/final QA. |
| DEC-025 | A page is not AI slop when a general-public reader can understand topic and claim boundary quickly, a specialist can find evidence and limits, factual claims are sourced or marked uncertain, and the structure is topic-specific. |
| DEC-026 | Write checked-in planning artifacts under `ImplementationPlans/`. |

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | Existing routes can be rewritten in place when they overlap inventory topics. | User explicitly accepted this scope. | Coding each route. |
| ASM-002 | Planning assumption | New inventory-backed routes can use current route families without a new top-level section. | Existing architecture and accepted route model support these families. | Creating route files. |
| ASM-003 | Planning assumption | Current live upstream state may drift after this plan. | The inventory itself notes stale current-state snapshot risk. | Implementing current-state, Distance-to-GR, Gate Chair, coupling-law, and reviewer-packet pages. |
| ASM-004 | Planning assumption | Existing animated SVGs are worth preserving unless a page-specific QA pass shows they no longer support comprehension. | User said the SVG animations are the only content definitely worth keeping. | Page rewrite QA. |
| ASM-005 | Implementation detail | Guided starts can be implemented either as `/resources/guided-starts/<audience>/` routes or a strong guided-start hub with audience sections. | The accepted decision requires first-class guided starts, but not a fixed URL shape. | Foundation packet. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Implementation detail | Should guided starts be separate child routes or one hub with anchored sections? | Affects URL count and navigation density, not the feasibility of the plan. |
| Q-002 | Implementation detail | Should route retirement use hard deletion, redirect pages, or navigation removal plus manifest deletion? | Affects implementation mechanics and link QA. |
| Q-003 | Implementation detail | Should high-risk pages use `human review pending` rather than `technical validation passed` after automated checks? | Affects review status, not task execution. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| REQ-001 Canonical scope | Every inventory item is mapped to a route action. | This plan, task packets, `src/pages`, `page_route_map.json`. | FND-001, QA-001 | Matrix review, `npm run validate:links`, `npm run validate:provenance`. |
| REQ-002 Foundation-first | Site navigation, content contract, and visual standard are defined before page rewrites. | `src/lib/siteContent.ts`, shared components, global styles, route landings. | FND-001, FND-002 | `npm run validate`, desktop/mobile QA. |
| REQ-003 Source analysis before pages | Claim-bearing pages start from completed `docs/system-analyses/*.md` artifacts. | `docs/system-analyses/`, `docs/content-dossiers/`, `to-web-page` workflow. | All PG-* tasks | `no-ai-slop` gate, page packet review. |
| REQ-004 Source refresh and pinning | Live-state pages do not publish stale or dirty upstream state. | Snapshot scripts, source manifests, page provenance. | PG-001, PG-002, PG-003, PG-004, PG-014, PG-026 | `npm run validate:manifests`, `npm run validate:provenance`, source clean-state check. |
| REQ-005 Preserve useful infrastructure | Astro, validators, manifests, provenance, dossiers, and animated SVGs remain in use. | Existing site stack and assets. | FND-001, all PG-* tasks | `npm run validate`, `npm run validate:svg`, browser QA. |
| REQ-006 Layered reader model | Pages begin public-first, then add mechanism, evidence, specialist detail, and navigation. | Page content contract, content libraries, dossiers. | FND-001, all PG-* tasks | `validate:comprehension`, no-ai-slop pass. |
| REQ-007 Anti-slop gate | Pages block or repair weak copy rather than shipping generic prose. | `no-ai-slop` workflow, dossiers, QA notes. | All PG-* tasks, QA-001 | No-ai-slop gate recorded in packet closeout. |
| REQ-008 Internal-first navigation | Readers move through website routes before source/provenance links. | Navigation, related links, source links, route cards. | FND-002, all PG-* tasks | `npm run validate:links`, browser QA. |
| REQ-009 Route retirement | Prototype/sample routes are consolidated or retired when not inventory-backed. | `/research/*`, route map, internal links. | RT-001 | `npm run validate:links`, `npm run validate:provenance`, `npm run build`. |
| REQ-010 Guided starts | General public and specialist readers get first-class reading paths. | `/resources/guided-starts/` or equivalent routes. | PG-006, PG-025 | `validate:content`, `validate:links`, browser QA. |
| REQ-011 Reviewer packet staging | Reviewer packet is planned but blocked until authority prerequisites exist. | `/resources/reviewer-packet/`, route map, dossiers. | PG-026 | Prerequisite review, no-ai-slop refuter pass, full validation. |
| REQ-012 Mandatory browser QA | Every page packet gets desktop and mobile browser inspection. | Dev server, Playwright artifacts under `output/playwright/`. | All implementation tasks | Screenshot or browser QA note. |
| REQ-013 No deploy | Revamp branch does not deploy automatically. | Release process. | QA-001 | Final release candidate report says deployment skipped. |

## Inventory-To-Route Matrix

| ID | Inventory item | Target route | Action | Required source analysis | Source refresh | Primary layer | Specialist layer | Risk | Packet |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INV-001 | Current Research State And Next Gate | `/project/physics/current-state/` | Rewrite existing | `docs/system-analyses/current-research-state-and-next-gate.md` | Required from clean upstream | General public | Physicist, reviewer | High | PG-001 |
| INV-002 | Distance To GR Dashboard | `/project/physics/distance-to-gr/` | Create | `docs/system-analyses/distance-to-gr-dashboard.md` | Required from clean upstream ledger | General public | Physicist, mathematician | High | PG-002 |
| INV-003 | Source Extension Pipeline | `/project/physics/source-extension-pipeline/` | Create | `docs/system-analyses/source-extension-pipeline.md` | Required for current gate language | General public | Physicist, system engineer | High | PG-003 |
| INV-004 | Gate Chair And Human-Gated Decisions | `/project/physics/gate-chair-and-human-gates/` | Create | `docs/system-analyses/gate-chair-and-human-gated-decisions.md` | Required for live handoff status | General public | Reviewer, governance reader | High | PG-004 |
| INV-005 | Claim Boundary Explorer | `/project/source-authority/claim-boundary-explorer/` | Create and link from existing claim-gates/source-authority routes | `docs/system-analyses/claim-boundary-explorer.md` | Required from registry snapshot | General public | Maintainer, reviewer | High | PG-005 |
| INV-006 | Ontology Document Library With Reading Guide | `/resources/documents/` | Rewrite/enhance existing | `docs/system-analyses/ontology-document-library-reading-guide.md` | Use committed ontology registry/assets | General public | Physicist, mathematician | Medium | PG-022 |
| INV-007 | Research-Agent Workflow Walkthrough | `/project/ai-research-agent-system/workflow/` | Rewrite existing | `docs/system-analyses/research-agent-workflow-walkthrough.md` | Use committed records or sanitized example | General public | AI developer, system engineer | Medium | PG-014 |
| INV-008 | Negative Results And Frozen Routes | `/project/physics/negative-results-and-frozen-routes/` | Create | `docs/system-analyses/negative-results-and-frozen-routes.md` | Required from ledger/control records | General public | Physicist, reviewer | High | PG-012 |
| INV-009 | AEther / AEther-Flow Ontology Vocabulary | `/project/physics/ontology/` | Rewrite existing | `docs/system-analyses/aether-flow-ontology-vocabulary.md` | Use committed ontology sources | General public | Physicist, mathematician | Medium | PG-007 |
| INV-010 | Exact-GR Benchmark Versus Derivation | `/project/physics/exact-gr-benchmark/` | Rewrite existing | `docs/system-analyses/exact-gr-benchmark-versus-derivation.md` | Use committed benchmark and burden sources | General public | Physicist | High | PG-008 |
| INV-011 | `Resp_lc`, `M_src`, `MetricData(E)`, `g_eff`, And Matter Coupling Ladder | `/project/physics/metric-response-ladder/` | Create | `docs/system-analyses/metric-response-ladder.md` | Required from current ledger/handoff state | General public | Physicist, mathematician | High | PG-009 |
| INV-012 | Finite Toy Models And Why One Route Froze | `/project/physics/finite-toy-models/` | Create | `docs/system-analyses/finite-toy-models-and-frozen-route.md` | Required from frozen-route records | General public | Physicist, mathematician | High | PG-010 |
| INV-013 | No-Target-Import Discipline | `/project/physics/no-target-import-discipline/` | Create | `docs/system-analyses/no-target-import-discipline.md` | Use committed guard-map sources | General public | Physicist, mathematician | High | PG-011 |
| INV-014 | Coupling-Law Candidate Status | `/project/physics/coupling-law-candidate-status/` | Create, staged | `docs/system-analyses/coupling-law-candidate-status.md` | Required from clean pinned handoff/task records | General public | Physicist, reviewer | Very high | PG-013 |
| INV-015 | One Bounded AgentJob In Practice | `/project/ai-research-agent-system/one-bounded-agentjob/` | Create | `docs/system-analyses/one-bounded-agentjob-in-practice.md` | Use committed or sanitized job records | General public | AI developer, system engineer | Medium | PG-015 |
| INV-016 | Parent-Child Parallel Synthesis Walkthrough | `/project/ai-research-agent-system/parent-child-synthesis/` | Rewrite existing | `docs/system-analyses/parent-child-parallel-synthesis-walkthrough.md` | Use committed workflow sources | General public | AI developer, system engineer | Medium | PG-016 |
| INV-017 | Role Authority Inspector | `/project/ai-research-agent-system/role-authority-inspector/` | Create | `docs/system-analyses/role-authority-inspector.md` | Use committed role registry snapshot | General public | AI developer, maintainer | Medium | PG-017 |
| INV-018 | Memory Preflight And Source-First Retrieval | `/project/ai-research-agent-system/memory-registries/` | Rewrite existing | `docs/system-analyses/memory-preflight-and-source-first-retrieval.md` | Use committed workflow/registry docs | General public | AI developer, system engineer | Medium | PG-018 |
| INV-019 | Validator PASS Does Not Mean Physics Proof | `/project/operations/validator-operator-workflow/` | Rewrite existing | `docs/system-analyses/validator-pass-does-not-mean-physics-proof.md` | Use committed validator/control sources | General public | AI developer, scientist | High | PG-019 |
| INV-020 | Project-System Improvement Loop | `/project/operations/project-system-improvement/` | Rewrite existing | `docs/system-analyses/project-system-improvement-loop.md` | Use committed project-system docs | General public | System engineer, maintainer | Medium | PG-020 |
| INV-021 | Guided Start Page For Physicists | `/resources/guided-starts/physicists/` | Create | `docs/system-analyses/guided-start-for-physicists.md` | Depends on authority/orientation pages | Physicist-oriented public | Physicist | High | PG-025 |
| INV-022 | Guided Start Page For AI/Agent Researchers | `/resources/guided-starts/ai-agent-researchers/` | Create | `docs/system-analyses/guided-start-for-ai-agent-researchers.md` | Depends on AI pages | AI-oriented public | AI developer, researcher | Medium | PG-025 |
| INV-023 | Publication And Provenance System | `/project/source-authority/publication-and-provenance-system/` | Create and strengthen source-authority landing | `docs/system-analyses/publication-and-provenance-system.md` | Use committed website manifests and docs | General public | Maintainer, system engineer | Medium | PG-024 |
| INV-024 | Visual Diagram Gallery By Concept | `/resources/diagrams/` | Rewrite/enhance existing | `docs/system-analyses/visual-diagram-gallery-by-concept.md` | Use committed diagram manifests/assets | General public | Visual reviewer, maintainer | Medium | PG-023 |
| INV-025 | External Review Packet | `/resources/reviewer-packet/` | Create, staged after prerequisites | `docs/system-analyses/external-review-packet.md` | Required after first-wave pages pass | Reviewer-oriented public | Physicist, mathematician, AI researcher | Very high | PG-026 |

## Additional Full-Site Route Work

| ID | Route or route family | Action | Reason | Packet |
| --- | --- | --- | --- | --- |
| SITE-001 | `/` and `/project/overview/` | Rewrite for public-first orientation and guided navigation | Homepage and overview shape the first impression and must set claim boundaries clearly. | FND-002 |
| SITE-002 | `/project/physics/` | Rewrite track landing | Must route readers to current state, Distance-to-GR, ontology, benchmark, and gates without overclaiming. | FND-002 |
| SITE-003 | `/project/ai-research-agent-system/` | Rewrite track landing | Must route readers to workflow, AgentJob, roles, memory, validators, and parent-child synthesis. | FND-002 |
| SITE-004 | `/project/operations/` and operational child routes not otherwise mapped | Rewrite/enhance | Existing operations pages need anti-slop consistency and stronger route relationships. | PG-021 |
| SITE-005 | `/project/source-authority/` | Rewrite landing | Must explain source authority before claim-boundary explorer and publication/provenance routes. | PG-005 |
| SITE-006 | `/resources/` | Rewrite resource landing | Must become a public reading hub, not a loose link collection. | FND-002 |
| SITE-007 | `/research/map/`, `/research/equations/`, `/research/math-sample/` | Consolidate or retire | Prototype/sample routes should not remain public unless they become inventory-backed routes. | RT-001 |

## Proposed Technical Approach

### 1. Foundation Contract

Create a shared revamp contract before page work:

- route family map and navigation hierarchy;
- layered page content contract;
- source-analysis requirement;
- no-ai-slop gate requirement;
- shared validation tiers;
- source refresh and pinning rules;
- browser QA artifact convention;
- SVG preservation rule;
- route retirement criteria.

Use existing components where they fit. Improve shared components only when the
foundation contract proves a reusable need.

### 2. Source Analysis Before Page Conversion

For every claim-bearing topic, create or verify a completed
`docs/system-analyses/*.md` artifact before route implementation. The analysis
must inspect upstream evidence, include source boundaries, and pass the
no-ai-slop gate. If source authority is unclear, the page task blocks.

### 3. Page-Scoped `to-web-page` Execution

Each page packet should run the repo-local `to-web-page` workflow against one
completed analysis file and one route. The task should update the dossier,
route/content library, discoverability, manifests, validator registration,
optional static diagram assets, provenance, QA note, and browser evidence.

Existing routes require explicit rewrite authorization, already provided by
this plan for inventory-overlapping routes. Existing prose remains suspect and
may be reused only after evidence review and no-ai-slop pass.

### 4. Track-Specific Emphasis

- Physics pages: claim boundaries, derivation status, assumptions, frozen or
  blocked routes, no downstream promotion.
- AI research-agent pages: workflow, authority, records, validator limits,
  memory boundaries, failure handling.
- Operations pages: interfaces, automation, manifests, validation,
  maintainability, release discipline.
- Resources pages: reading order, source authority, guided starts, reviewer
  utility.

### 5. Navigation And Guided Starts

Implement internal-first navigation around public and specialist reading paths:

- general public;
- physicists;
- mathematicians;
- AI/agent researchers;
- software/system engineers;
- external reviewers.

Guided starts assemble existing sourced pages. They must not introduce new
scientific claims.

### 6. Route Retirement

Prototype or sample routes should be consolidated, rewritten as true
inventory-backed pages, or retired. Each retirement must update route maps,
links, manifests, and provenance expectations.

## Implementation Phases

1. Milestone 0: Foundation contract and navigation shell.
   - Define shared page contract, navigation, visual standard, route retirement
     rules, and validation profiles.
   - Rewrite homepage/overview/track/resource landings only enough to create a
     coherent entry path.
2. Milestone 1: Authority and orientation first wave.
   - Refresh/rewrite current state.
   - Create Distance-to-GR, source-extension pipeline, Gate Chair/human gates,
     claim-boundary explorer, and general-public guided start.
3. Milestone 2: Physics deepening pages.
   - Rewrite ontology and benchmark pages.
   - Create metric-response ladder, finite toy models, no-target-import,
     negative-results, and staged coupling-law candidate pages.
4. Milestone 3: AI research-agent pages.
   - Rewrite workflow, parent-child, memory, and validator-limit pages.
   - Create one bounded AgentJob and role authority inspector pages.
5. Milestone 4: Operations, source authority, and resources.
   - Rewrite operations pages, source-authority landing, publication and
     provenance route, document library, and diagram gallery.
6. Milestone 5: Guided starts, reviewer packet, route retirement, and final QA.
   - Add specialist guided starts.
   - Add reviewer packet only after prerequisites pass.
   - Retire prototype routes.
   - Run release-candidate validation and browser QA.

## Codex Task Packets

The executable task packets are in
`ImplementationPlans/sitewide_page_revamp_task_packets.md`.

## Validation Plan

Page packet minimum:

```bash
npm run validate:comprehension
npm run validate:manifests
npm run validate:content
npm run validate:provenance
npm run build
```

SVG-affected packet:

```bash
npm run validate:svg
```

Navigation or link packet:

```bash
npm run validate:links
```

Foundation or shared-component packet:

```bash
npm run validate
```

Release candidate:

```bash
npm run validate
npm run quality
```

Every page packet also requires desktop and mobile browser QA against
`127.0.0.1`, with screenshots or a QA note under the repo's existing
`output/playwright/` or `docs/quality/` convention.

## Security, Privacy, And Reliability Notes

- Data validation: registry-derived pages must use structured parsers or
  snapshot generation where available, not ad hoc copy-paste.
- Permissions and access control: this is a static public site; do not expose
  private local paths in public pages.
- Privacy: sanitized examples are required for AgentJob or role records if
  records contain local or sensitive details.
- Reliability: current-state and ledger-backed pages must fail closed when the
  upstream source state is dirty, stale, or ambiguous.
- Observability: page provenance and manifest hashes are the audit layer.
- Rollback: page-scoped packets make route rollback possible by reverting a
  dossier, content entry, route file, manifest entries, and provenance changes.

## Rollout And Rollback Plan

- Rollout: implement on `codex/revamp-all-pages` in milestone order.
- Migration/backfill: update route maps, source manifests, asset manifests, and
  page provenance as routes are created, rewritten, or retired.
- Feature flag: not required for static routes, but staged route visibility can
  be simulated by withholding navigation links until validation passes.
- Rollback: revert the affected page packet or milestone commit. Do not deploy
  until explicit approval.
- Monitoring: use validation, browser QA, and final site smoke checks before
  any later deployment.

## Out Of Scope

- Deploying to Cloudflare Pages.
- Changing upstream scientific, mathematical, governance, or workflow claims.
- Creating runtime dashboards that imply live synchronization.
- Adding new dependencies unless a later task proves the need and receives
  explicit approval.
- Replacing the static-site stack.
- Treating PDFs as independent source authority when registered TeX sources
  carry authority.

## Final Review Checklist

- [x] Every PRD requirement is mapped to a task or explicitly staged.
- [x] Every inventory candidate is mapped to a target route and packet.
- [x] Every task packet has acceptance criteria and validation guidance.
- [x] Risky changes have review and rollback notes.
- [x] The plan avoids direct page implementation.
- [x] Commands are discovered from the repository.
- [x] Product decisions are separated from implementation details.
- [x] Source-authority boundaries are explicit.

## References

The AEther Flow Website. (n.d.-a). `AGENTS.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/AGENTS.md`.

The AEther Flow Website. (n.d.-b). `docs/system-analyses/aether-flow-website-topic-inventory.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/docs/system-analyses/aether-flow-website-topic-inventory.md`.

The AEther Flow Website. (n.d.-c). `docs/architecture/website-feature-and-functionality.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/docs/architecture/website-feature-and-functionality.md`.

The AEther Flow Website. (n.d.-d). `.codex/skills/prd-to-implementation-plan/SKILL.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/.codex/skills/prd-to-implementation-plan/SKILL.md`.

The AEther Flow Website. (n.d.-e). `.codex/skills/to-web-page/SKILL.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/.codex/skills/to-web-page/SKILL.md`.

The AEther Flow Website. (n.d.-f). `.codex/skills/no-ai-slop/SKILL.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/.codex/skills/no-ai-slop/SKILL.md`.

The AEther Flow Website. (n.d.-g). `public/files/manifests/page_route_map.json`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/public/files/manifests/page_route_map.json`.
