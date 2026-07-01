# Sitewide Greenfield Review Ledger

Status: active implementation ledger.
Date: 2026-06-30.

## Purpose

This ledger tracks the greenfield rebuild route inventory, technical readiness,
source-bundle readiness, validation status, and human review status. It is a
maintainer-facing control surface, not public website copy and not source
authority.

Deployment remains blocked until the owner marks the rebuilt page set
`reviewed and accepted`.

## Status Vocabulary

| Field | Allowed values |
| --- | --- |
| Technical status | `not implemented`, `in progress`, `technically ready`, `blocked`, `retired` |
| Human review status | `not implemented`, `human review pending`, `reviewed with changes requested`, `reviewed and accepted` |
| Source-bundle status | `not started`, `drafted`, `verified`, `not required`, `blocked` |

## Route Inventory

| Order | Route | Page | Family | Task | Technical status | Human review status | Source-bundle status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `/` | Home | Home | GF-002 | technically ready | human review pending | verified | GF-002 rebuilt Home and primary navigation; linked category routes remain pending in later packets. |
| 2 | `/physics/` | Physics Overview | Physics Research | GF-003 | technically ready | human review pending | verified | GF-003 implemented the category landing page; linked remaining Physics child routes stay pending in later packets. |
| 3 | `/physics/ontology/` | Ontology | Physics Research | GF-003 | technically ready | human review pending | verified | GF-003 defines ontology terms near use and keeps proof-boundary language visible. |
| 4 | `/physics/exact-gr-benchmark/` | Exact-GR Benchmark | Physics Research | GF-004 | technically ready | human review pending | verified | GF-004 distinguishes benchmark adoption, compatibility, derivation, and promotion. |
| 5 | `/physics/derivation-roadmap/` | Derivation Roadmap | Physics Research | GF-004 | technically ready | human review pending | verified | GF-004 names open burdens without implying completed GR derivation. |
| 6 | `/physics/flow-geometry/` | Flow Geometry | Physics Research | GF-004 | technically ready | human review pending | verified | GF-004 implements a visual and tabular dictionary with assumptions and limits. |
| 7 | `/physics/claim-status/` | Physics Claim Status | Physics Research | GF-005 | technically ready | human review pending | verified | GF-005 shows claimed, not claimed, blocked, and open states with visible freshness and source-basis metadata. |
| 8 | `/physics/open-burdens/` | Open Burdens | Physics Research | GF-005 | technically ready | human review pending | verified | GF-005 explains missing derivation steps without progress-bar proof or claim promotion. |
| 9 | `/ai-research-system/` | AI Research System Overview | AI Research System | GF-006 | technically ready | human review pending | verified | GF-006 explains the category as governed, source-first workflow before internal terms dominate. |
| 10 | `/ai-research-system/current-state/` | Current State | AI Research System | GF-006 | technically ready | human review pending | verified | GF-006 labels current implementation-control data as dated snapshot context with stale-data and proof-boundary warnings. |
| 11 | `/ai-research-system/workflow/` | Workflow | AI Research System | GF-007 | technically ready | human review pending | verified | GF-007 explains the state-to-handoff lifecycle with one-job, parent-child, validation, handoff, and source-authority limits visible. |
| 12 | `/ai-research-system/agentjob-lifecycle/` | AgentJob Lifecycle | AI Research System | GF-007 | technically ready | human review pending | verified | GF-007 explains one AgentJob as an auditable permission envelope without reusable permission or proof implications. |
| 13 | `/ai-research-system/roles-and-schemas/` | Roles and Schemas | AI Research System | GF-008 | technically ready | human review pending | verified | GF-008 distinguishes role labels, schema contracts, registry rows, execution-role records, and AgentJob allowlists from proof or live authority. |
| 14 | `/ai-research-system/human-gated-promotion/` | Human-Gated Promotion | AI Research System | GF-008 | technically ready | human review pending | verified | GF-008 separates protected promotion from automated outcomes and keeps Gate Chair authority inactive without explicit tracked approval. |
| 15 | `/ai-research-system/validators-and-handoffs/` | Validators and Handoffs | AI Research System | GF-008 | technically ready | human review pending | verified | GF-008 states validator PASS, registries, handoffs, screenshots, completions, and commits are operational evidence, not proof. |
| 16 | `/ai-research-system/memory-preflight/` | Memory Preflight | AI Research System | GF-009 | technically ready | human review pending | verified | GF-009 explains memory as navigation support, not source authority, and requires source inspection before retrieval hits affect claims or routing. |
| 17 | `/ai-research-system/project-system-improvement/` | Project-System Improvement | AI Research System | GF-009 | technically ready | human review pending | verified | GF-009 explains one bounded repair, documentation-impact evidence, and why project-system maintenance does not continue research or promote physics claims. |
| 18 | `/ai-research-system/runtime-requirements/` | Runtime Requirements | AI Research System | GF-009 | technically ready | human review pending | verified | GF-009 lists runtime and command scopes while stating that runtime setup, Python, Node.js, Playwright, and validator PASS do not grant authority or proof. |
| 19 | `/resources/` | Resources Overview | Resources | GF-010 | technically ready | human review pending | verified | GF-010 rebuilds Resources as an internal-first category landing page with planned child-route boundaries visible. |
| 20 | `/resources/source-authority/` | Source Authority | Resources | GF-010 | technically ready | human review pending | verified | GF-010 explains authority classes through contextual copy and provenance tables without rendering a dedicated source-authority component. |
| 21 | `/resources/registries/` | Registries | Resources | GF-010 | technically ready | human review pending | verified | GF-010 explains registries as provenance and status maps, not proof surfaces. |
| 22 | `/resources/generated-derivatives/` | Generated Derivatives | Resources | GF-011 | technically ready | human review pending | verified | GF-011 labels generated Markdown, HTML, PDF, wiki, and public assets as reader support below source authority. |
| 23 | `/resources/retrieval-layers/` | Local Retrieval Layers | Resources | GF-011 | technically ready | human review pending | verified | GF-011 explains memory, semantic extracts, mirrors, local indexes, and caches as navigation-only support. |
| 24 | `/resources/publication-process/` | Publication Process | Resources | GF-011 | technically ready | human review pending | verified | GF-011 separates source specs, briefs, validation, review, and publication quality from source authority. |
| 25 | `/resources/library/` | Library | Resources | GF-011 | technically ready | human review pending | verified | GF-011 organizes reader paths by reader job while preserving provenance and non-authority boundaries. |
| 26 | `/resources/reading-paths/` | Reading Paths | Resources | GF-012 | technically ready | human review pending | verified | GF-012 implements internal-first audience and question paths through new short routes before source archaeology. |
| 27 | `/resources/repository-map/` | Repository Map | Resources | GF-012 | technically ready | human review pending | verified | GF-012 classifies source, control, generated, local, tooling, archival, and reserved lanes with edit/read boundaries. |
| 28 | `/resources/site-builder-guide/` | Site Builder Guide | Resources | GF-012 | technically ready | human review pending | verified | GF-012 explains source-bundle-first implementation, build-first checks, handoff evidence, and stale-data boundaries. |
| 29 | `/resources/diagrams/` | Diagram Gallery | Resources | GF-012 | technically ready | human review pending | verified | GF-012 resets the visible diagram inventory, keeps static diagram workflow/provenance behavior, and requires explicit reapproval before restoring items. |

## Packet Ledger

| Packet | Scope | Status | Validation summary | Next action |
| --- | --- | --- | --- | --- |
| GF-000 | Open fresh greenfield control packet. | completed | `git diff --check`, `npm run validate:implementation-control`, and `.venv/bin/python -m pytest` passed in packet `WI-20260630-028`. | GF-001 foundation contract and review ledger. |
| GF-001 | Foundation contract and route review ledger. | completed | `git diff --check`, `npm run validate:implementation-control`, and `.venv/bin/python -m pytest` passed in packet `WI-20260630-029`. | GF-002 Home and primary navigation slice. |
| GF-002 | Home route and primary navigation slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:implementation-control`, `npm run build`, `.venv/bin/python -m pytest`, `npm run validate:svg`, and desktop/mobile browser QA passed in packet `WI-20260630-030`. | GF-003 Physics overview and ontology slice. |
| GF-003 | Physics overview and ontology slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-031`. | GF-004 Physics benchmark, roadmap, and flow geometry slice. |
| GF-004 | Physics benchmark, roadmap, and flow geometry slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-032`. | GF-005 Physics claim status and open burdens slice. |
| GF-005 | Physics claim status and open burdens slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-033`. | GF-006 AI overview and current state slice. |
| GF-006 | AI overview and current state slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-034`. | GF-007 AI workflow and AgentJob lifecycle slice. |
| GF-007 | AI workflow and AgentJob lifecycle slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-035`. | GF-008 AI roles, human gates, validators, and handoffs slice. |
| GF-008 | AI roles, human gates, validators, and handoffs slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-036`. | GF-009 AI memory, improvement, and runtime slice. |
| GF-009 | AI memory, improvement, and runtime slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-037`. | GF-010 Resources overview, source authority, and registries slice. |
| GF-010 | Resources overview, source authority, and registries slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-038`. | GF-011 Resources derivatives, retrieval, publication, and library slice. |
| GF-011 | Resources derivatives, retrieval, publication, and library slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-039`. | GF-012 Reading paths, repository map, site builder guide, and diagram gallery slice. |
| GF-012 | Reading paths, repository map, site builder guide, and diagram gallery slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-040`. | GF-013 manifests, redirects, and obsolete route retirement. |
| GF-013 | Manifest cleanup, redirects, and obsolete old route retirement. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and redirect/browser smoke checks passed in packet `WI-20260630-041`. | GF-014 owner review and release-candidate QA. |
| GF-014 | Owner review loop and release-candidate QA. | completed with blockers | Targeted manifest, content, links, layout, SVG, provenance, Cloudflare, implementation-control, build, Python tests, local smoke test, and desktop/mobile browser QA passed in packet `WI-20260630-042`; `npm run quality` was blocked by curator/source drift and `/resources/diagrams/` support-schema quality-gate mismatch. | Open bounded follow-up packets before owner acceptance or deployment. |
| GF-014A | Diagram Gallery quality-gate contract follow-up. | completed | `python3 scripts/quality_gate.py`, `.venv/bin/python -m pytest`, `npm run build`, `npm run validate:implementation-control`, and `git diff --check` passed in packet `WI-20260630-043`. | Curator/source-drift packet remains before owner acceptance or deployment. |
| GF-014B | Curator source-drift refresh. | completed | Regenerated page provenance, current-state snapshot, and curator reports from clean committed upstream source commit `2a934c29b58e84aa913a5088a8388bd259f6370b`; `npm run validate` and `npm run quality` passed with `AETHER_FLOW_SOURCE_ROOT` bound to that clean committed source view; `.venv/bin/python -m pytest`, `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`, `npm run validate:implementation-control`, and `git diff --check` passed in packet `WI-20260630-044`. | Owner review decision remains before acceptance or deployment. |
| GF-014C | Greenfield static diagram rollout. | completed | Added source-backed static diagram blocks to 28 greenfield routes; `git diff --check`, `npm run validate:comprehension`, `npm run validate:svg`, `npm run validate:manifests`, `npm run validate:provenance`, `npm run build`, `npm run validate`, `npm run quality`, `.venv/bin/python -m pytest`, route smoke checks, and desktop/mobile browser diagram QA passed in packet `WI-20260630-045` with curator validation bound to clean committed upstream source commit `2a934c29b58e84aa913a5088a8388bd259f6370b`. | Owner review decision remains before acceptance or deployment. |
| GF-014D | Greenfield diagram fit and expansion refinement. | completed | Refined the 28 greenfield route diagram blocks with full-width frames, viewport-contained sizing for oversized diagrams, in-page larger-view dialogs, and removal of the repeated visible post-diagram note; required validators, route smoke checks, and desktop/mobile dialog QA passed in packet `WI-20260630-045`. | Owner review decision remains before acceptance or deployment. |
| GF-014E | Greenfield diagram caption reform. | completed | Reworked visible diagram captions in the active greenfield/resource write scope into descriptive figure-note copy, removed visible Mermaid source paths from shared figure/gallery rendering, and recorded legacy project-route captions as out-of-scope follow-up for a future authorized packet. | Owner review decision remains before acceptance or deployment. |
| GF-014F | Greenfield diagram caption weight refinement. | completed | Changed shared diagram description captions, expanded-dialog captions, and gallery boundary note text to regular weight so descriptive figure notes do not read as bold labels. | Owner review decision remains before acceptance or deployment. |
| GF-014G | Diagram Gallery grouped inventory restoration. | completed | Restored `/resources/diagrams/` to render the approved manifest-backed diagram inventory grouped by physics, AI workflow, operations, and source authority concepts; HTML and Playwright image checks passed in packet `WI-20260630-045`. | Owner review decision remains before acceptance or deployment. |
| GF-014H | Comprehension diagram full-width and no-default-note rule. | completed | Changed shared comprehension diagrams to default to full route-column width, removed the automatic post-diagram note, and added `validate:comprehension` regression checks for the old width cap and repeated note; desktop/mobile browser QA passed on `/resources/diagrams/`. | Owner review decision remains before acceptance or deployment. |
| GF-014I | Mobile expanded diagram image-first dialog refinement. | completed | Reworked shared expanded diagram dialogs so mobile `Open larger` uses a compact close bar, scrollable image stage, wider-than-viewport diagram rendering, and below-image caption text; `npm run validate:comprehension` and Playwright mobile/desktop dialog geometry checks passed in packet `WI-20260630-045`. | Owner review decision remains before acceptance or deployment. |
| GF-014J | Animated SVG hero fact-caption rule. | completed | Rewrote greenfield animated SVG hero captions as conservative facts about each route topic and added a `validate:comprehension` guard against future visual-description captions such as `The diagram illustrates...`; page provenance was regenerated against clean committed upstream source commit `2a934c29b58e84aa913a5088a8388bd259f6370b`. | Owner review decision remains before acceptance or deployment. |
| GF-014K | Animated SVG caption label and capitalization rule. | completed | Removed the visible `Fact:` prefix from greenfield animated SVG hero fact sentences, capitalized each sentence start, and extended `validate:comprehension` so future inline animated SVG hero captions cannot use a visible `Fact:` label or lowercase sentence start. | Owner review decision remains before acceptance or deployment. |

## Review Rules

- Mark a route `technically ready` only after its packet passes the required
  validators and browser QA for the affected route.
- Mark a route `human review pending` only when it is technically ready for
  owner review.
- Mark a route `reviewed and accepted` only after owner review.
- Use `reviewed with changes requested` when owner review asks for changes.
- Keep deployment blocked until the rebuilt page set is accepted.
- Record skipped validators with concrete reasons in the packet closeout.

## References

The AEther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Product
requirements document].

The AEther Flow Website. (2026). *Implementation Plan: Sitewide Greenfield
Rebuild* [Implementation plan].

The AEther Flow Website. (2026). *Public Comprehension Review Standard*
[Quality standard].
