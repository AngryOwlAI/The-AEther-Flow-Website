# Implementation Plan: Website Information-Space Master Plan

## Source PRD

- Source: `PRDs/website-information-space/PRD-00-master-website-information-space.md`
- Supporting index: `PRDs/website-information-space/README.md`
- Supporting review:
  `PRDs/website-information-space/PRD-FAMILY-VALIDATION-REVIEW.md`
- Canonical rebuild plan:
  `ImplementationPlans/sitewide_greenfield_rebuild_implementation_plan.md`
- Canonical rebuild task packets:
  `ImplementationPlans/sitewide_greenfield_rebuild_task_packets.md`
- Generated for: Codex app and Codex IDE
- Planning status: Ready with assumptions

## Product Summary

The website information-space plan turns the reviewed PRD family into a
governed implementation-planning system for the public website rebuild. Its
purpose is not to implement routes directly. Its purpose is to define the master
planning layer, the conversion order for all sub-PRDs, the traceability model
from requirements to implementation packets, and the constraints that future
route work must preserve.

The canonical implementation direction is the sitewide greenfield rebuild:
Home, Physics Research, AI Research System, and Resources form the public route
model. Pages must use a hero/title/action/SVG opening, a substantial
general-public introductory paragraph, then topic-appropriate narrative,
technical, operational, provenance, and navigation sections. Cards are allowed
only when they fit the information type; card grids are not the default page
grammar.

## Repository Context

- Frameworks and languages: Astro static site, TypeScript content modules,
  Astro components, CSS, Python validation scripts.
- Package manager and build system: npm scripts with `astro build`; local
  Python tests through `.venv/bin/python` when available.
- Implementation-control boundary: live records under
  `implementation_control/` are authoritative for what may be edited in a
  packet. This plan is route context until a future live packet authorizes
  implementation work.
- Relevant repository instructions:
  - Website pages are explanatory derivatives.
  - Upstream source files, registries, and governed task records remain
    authoritative for scientific, mathematical, governance, and
    research-workflow claims.
  - Internal website routes are the primary reader journey; GitHub and source
    links remain available as provenance.
  - Visual SVG figures must be animated and must not contain visible embedded
    text.
  - Library/resource pages under `/resources/` must not render a dedicated
    `Source authority` section.
- Discovered validation commands:
  - `git diff --check`
  - `npm run validate:implementation-control`
  - `.venv/bin/python -m pytest`
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

## Assumptions

| ID | Type | Assumption | Why it is reasonable | Must confirm before |
| --- | --- | --- | --- | --- |
| ASM-001 | Planning assumption | `ImplementationPlans/website-information-space/` is the correct output directory for PRD-family implementation plans. | The active implementation-control packet explicitly allows this directory. | Local checkpoint. |
| ASM-002 | Planning assumption | The sitewide greenfield rebuild plan is canonical for route model, page grammar, validation, and owner-review loop. | The active task and job require treating it as canonical. | Any route implementation packet. |
| ASM-003 | Planning assumption | Sub-PRD implementation plans should be produced in the PRD dependency order, not numerical order. | The PRD index and PRD-system plan both define dependency order. | Opening the first sub-PRD packet. |
| ASM-004 | Planning assumption | Route implementation should start only after sub implementation plans exist for positioning and source authority. | Public copy and source-boundary requirements constrain every later route. | First public route packet. |
| ASM-005 | Planning assumption | Existing source identifiers and file paths keep their current spelling even when reader-facing text uses `Æther`. | The spelling rule distinguishes display copy from machine-facing identifiers. | Public copy, source maps, and route slugs. |

## Open Questions

| ID | Classification | Question | Impact if unanswered |
| --- | --- | --- | --- |
| Q-001 | Implementation detail | Should the sub implementation plans each include one sub-PRD-specific task-packet file, or should each plan include embedded task packets? | Affects file layout, not feasibility. The recommended default is one plan file plus one task-packet file per sub-PRD. |
| Q-002 | Planning assumption | Should the first actual route implementation packet begin with Home or with Resources/Source Authority? | The greenfield plan begins with shell and Home, while the PRD family emphasizes source authority first. This can be resolved after sub-plan conversion. |
| Q-003 | Implementation detail | Should a machine-readable conversion ledger be added after all sub plans exist? | Useful for validators later, but out of scope for this packet. |

## Requirement Traceability Matrix

| Requirement | User-visible behavior | Implementation area | Task IDs | Validation |
| --- | --- | --- | --- | --- |
| REQ-001 Master public narrative | Readers receive a coherent first-visit explanation of the dual physics and AI research program. | Home, project overview, positioning, page introductions, route IA. | MIP-00, MIP-10, MIP-01 | `npm run validate:comprehension`, browser QA in future route packets. |
| REQ-002 Exact-GR and open derivation boundary | Physics pages separate exact-GR benchmark adoption from unresolved first-principles derivation. | Physics routes, claim-status surfaces, source-bundle requirements. | MIP-02, MIP-09, MIP-10 | `npm run validate:content`, `npm run validate:comprehension`, source review. |
| REQ-003 AI research-agent explanation | AI pages explain governed, bounded, source-first workflow without implying autonomous proof. | AI route family, roles, validators, handoffs, memory, runtime. | MIP-03, MIP-04, MIP-07, MIP-09 | `npm run validate:content`, `npm run validate:provenance`. |
| REQ-004 Source authority as trust architecture | Pages expose source basis, claim status, claim boundary, provenance, and freshness constraints. | Source authority, registries, library, publication, page metadata. | MIP-05, MIP-06, MIP-11 | `npm run validate:content`, `npm run validate:provenance`. |
| REQ-005 Internal-first information architecture | Primary reader paths use website routes before provenance links. | Navigation model, route cards, reading paths, source maps. | MIP-00, MIP-01, MIP-11 | `npm run validate:links`, route smoke tests. |
| REQ-006 Greenfield rebuild constraint | Future route work follows the canonical short route model and rejects old card-grid grammar as default. | All future route implementation packets. | MIP-00 and all sub-plan packets | Plan review, `npm run validate:layout`, browser QA. |
| REQ-007 Current-frontier freshness | Active status pages show dated source basis, stale behavior, blocked claims, and source precedence. | Current Frontier, AI current state, physics claim status, source bundles. | MIP-09, MIP-02, MIP-03 | Snapshot-specific checks, `npm run validate:content`. |
| REQ-008 Accessibility and SVG discipline | Pages use semantic structure, readable tables, non-color-only status, accessible animated textless SVGs. | Layout, page components, SVG assets, diagrams. | MIP-01, MIP-02, MIP-03, MIP-06, MIP-11 | `npm run validate:svg`, `npm run validate:layout`, browser QA. |
| REQ-009 Governed implementation | Work proceeds one bounded packet at a time under live implementation-control records. | `implementation_control/`, task packets, checkpoint workflow. | MIP-00 and every later conversion packet | `npm run validate:implementation-control`, `.venv/bin/python -m pytest`. |
| NFR-001 Static build | Public route work remains compatible with static Astro builds. | Route files, content modules, manifests. | Future route packets derived from sub plans | `npm run build`, `npm run validate`. |
| NFR-002 Auditability | Maintainers can trace every public claim to sources, PRDs, and validation gates. | Source bundles, provenance manifests, route metadata. | MIP-05, MIP-06, MIP-11 | `npm run validate:provenance`, manual review. |
| NFR-003 Conservative failure | Stale current-state or missing source evidence blocks claim strengthening. | Current-state data contracts and page copy. | MIP-09 | Current-state validation and manual source review. |

## Proposed Technical Approach

### 1. Convert Requirements Before Coding

The master PRD creates the governing plan. Each sub-PRD should then produce a
sub implementation plan and task-packet set before public route code is
changed. This keeps public implementation packets small, traceable, and
reviewable.

### 2. Treat Greenfield Rebuild As Canonical

The sitewide greenfield rebuild plan controls the route model, page grammar,
human-review loop, and old-route retirement sequence. Sub implementation plans
should map their requirements onto the greenfield route families instead of
reviving the older route tree.

### 3. Preserve Source Authority Boundary

Implementation plans may describe source basis, claim status, provenance, and
validation expectations. They must not silently strengthen scientific,
mathematical, governance, or research-workflow claims. Public copy changes
require later live authorization.

### 4. Apply Display-Spelling Rule

Future reader-facing text should use `Æther`. Links, slugs, file names,
package names, repository paths, and existing machine-facing identifiers should
use or preserve `aether`/`AEther` as appropriate to the existing identifier.

### 5. Produce Sub Plans In Dependency Order

The recommended conversion order is:

1. PRD-10: positioning and public language.
2. PRD-05: source authority, registries, memory, retrieval, provenance.
3. PRD-06: documentation, publication, library, website components.
4. PRD-01: Home, overview, high-level components, primary journeys.
5. PRD-02: physics and mathematics.
6. PRD-09: current frontier and stale-data behavior.
7. PRD-03: research-control and AgentJob workflow.
8. PRD-04: roles, schemas, authority classes, human gates.
9. PRD-07: tooling, skills, scripts, validators, runtime.
10. PRD-08: folder and repository topology.
11. PRD-11: quick source map for site builders.

## Implementation Phases

1. Master conversion: create this master plan, master task-packet set, and
   directory index.
2. Messaging and authority foundation: convert PRD-10 and PRD-05 so every
   future page packet has safe language and authority rules.
3. Publication and public journey foundation: convert PRD-06 and PRD-01.
4. Physics and freshness planning: convert PRD-02 and PRD-09.
5. AI workflow and role planning: convert PRD-03 and PRD-04.
6. Tooling, topology, and builder support: convert PRD-07, PRD-08, and PRD-11.
7. Consolidation: review all sub plans against the greenfield route map before
   opening public route implementation packets.

## Codex Task Packets

Task packets for this conversion system are in:

`ImplementationPlans/website-information-space/PRD-00-master-website-information-space-task-packets.md`

The task-packet file defines one current master-conversion packet and one
future packet for each remaining sub-PRD conversion.

## Validation Plan

- Planning/control packet validation:
  - `git diff --check`
  - `npm run validate:implementation-control`
  - `.venv/bin/python -m pytest`
- Sub implementation-plan conversion packets:
  - `git diff --check`
  - `npm run validate:implementation-control`
  - `.venv/bin/python -m pytest`
  - manual review that every sub-PRD requirement maps to route, source-bundle,
    manifest, validation, or explicit deferral guidance.
- Future public route packets:
  - Use the validation profile in the canonical greenfield rebuild plan.
  - Add source-specific checks when source bundles, current-state snapshots,
    diagrams, SVGs, manifests, or public assets change.
- Deployment:
  - Out of scope until the owner review ledger reaches `reviewed and accepted`
    and a fresh deploy workflow authorizes publication.

## Security, Privacy, And Reliability Notes

- Data validation: current-state and source-derived public content must use
  dated source basis and fail closed on stale evidence.
- Permissions and access control: no upstream source writes, push, deployment,
  source refresh, generated publication refresh, or retrieval-layer refresh is
  authorized by this plan.
- Abuse cases: do not let validators, agents, registries, generated documents,
  memory, or handoffs appear to prove scientific claims.
- Privacy: preserve only intentionally public profile and attribution links
  when route implementation later touches the footer.
- Failure modes: unsupported public claim, stale current-state data, broken
  provenance, route-map drift, mobile overlap, SVG policy failure, and old-route
  retirement before replacement validation.

## Rollout And Rollback Plan

- Rollout: complete sub implementation-plan conversion first; then open public
  route packets under live implementation-control records.
- Migration/backfill: future route work should build replacement routes before
  old route retirement, then regenerate manifests and redirects in a dedicated
  packet.
- Feature flag or staged release: use branch, route existence, owner review
  status, and deployment authorization as the stage boundary.
- Rollback: planning changes can be reverted by removing the relevant plan
  files and restoring implementation-control state before checkpoint. Future
  public route rollback must follow the greenfield rebuild plan.
- Monitoring: each packet should report changed files, source bundles inspected,
  validation attempted, browser QA evidence where relevant, owner-review status,
  and blockers.

## Out Of Scope

- Direct public route implementation.
- Public copy changes.
- Public manifest or asset changes.
- Source snapshot refreshes.
- Source bundle dataset changes.
- Generated HTML, Markdown, wiki, PDF, or retrieval-layer refreshes.
- Upstream source-project writes.
- Git push.
- Cloudflare deployment.
- Scientific, mathematical, governance, or research-workflow claim promotion.

## Final Review Checklist

- [x] Source PRD and supporting planning files are identified.
- [x] Planning status is recorded.
- [x] Master PRD requirements are mapped to conversion tasks or future route
      implementation areas.
- [x] Canonical greenfield rebuild constraints are integrated.
- [x] Display-spelling rule is recorded.
- [x] Source authority boundary is preserved.
- [x] Validation commands are discovered from the repository.
- [x] Product questions are separated from implementation decisions.
- [x] The plan avoids direct coding.

## References

The Æther Flow Website. (2026). *AGENTS.md instructions* [Repository operating
rules].

The Æther Flow Website. (2026). *PRD-00: Æther-Flow Website Information Space*
[Product requirements document].

The Æther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Implementation
plan].

The Æther Flow Website. (2026). *Website Information-Space PRD Family
Validation Review* [Requirements-readiness review].
