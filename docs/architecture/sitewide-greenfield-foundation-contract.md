# Sitewide Greenfield Foundation Contract

Status: implementation contract.
Date: 2026-06-30.

## Purpose

This contract governs greenfield website packets that rebuild The AEther Flow
Website from the website information-space PRDs and the sitewide greenfield
rebuild plan. It is not public website copy and does not create scientific,
mathematical, governance, deployment, or upstream source authority.

The contract exists so later route packets can cite a stable foundation before
editing pages, components, navigation, manifests, or assets.

## Authority Boundary

The upstream source project remains authoritative for scientific,
mathematical, governance, and research-workflow claims. The website may
explain, organize, promote, and link reviewed reader-facing material, but it
must not silently strengthen source claims.

Implementation-control records remain the live authority for each packet.
PRDs, implementation plans, this contract, and the review ledger are route
context until a live task and job authorize writes.

## Old Implementation Rule

The old implementation is evidence, not architecture.

It may be inspected to preserve:

- footer content and behavior;
- hero, title, action-button, and animated SVG direction;
- dropdown interaction expectations;
- source-authority notice behavior;
- diagram generation and display discipline;
- provenance and validation expectations.

It must not be copied as the new:

- route tree;
- page grammar;
- default card-grid model;
- component composition;
- navigation hierarchy;
- claim-authoring surface.

When a later packet adapts an old component or pattern, its closeout must name
the preserved behavior and explain why the adaptation does not preserve the old
architecture.

## Navigation Model

The greenfield public navigation model is:

| Navigation item | Type | Route role |
| --- | --- | --- |
| Home | Page | Public first surface for project identity, dual-track thesis, hero, and first orientation. |
| Physics Research | Dropdown category | Physics and mathematics explanation surfaces. |
| AI Research System | Dropdown category | Governed AI research workflow, current state, operations, roles, validators, and runtime surfaces. |
| Resources | Dropdown category | Source authority, registries, generated derivatives, retrieval layers, publication, library, reading paths, repository map, site-builder guidance, and diagrams. |

Primary reader journeys must prefer internal website routes. Source and GitHub
links are provenance or inspection paths unless a live packet records a
different, narrow reason.

## Page And Content Metadata Contract

Every substantive greenfield page packet must define or update a page metadata
record before writing claim-bearing public copy. The record may begin in a
source bundle, Astro frontmatter, TypeScript data module, or another governed
format chosen by the packet, but it must cover these fields:

| Field | Required meaning |
| --- | --- |
| `route` | Public route path, including trailing slash policy. |
| `page_title` | Reader-facing page title. |
| `page_family` | One of Home, Physics Research, AI Research System, Resources, or utility route. |
| `navigation_role` | Home page, category landing page, child explanation page, resource page, or utility page. |
| `source_anchors` | Primary upstream or repository authority sources inspected for claims. |
| `supporting_sources` | PRDs, implementation plans, prior dossiers, generated derivatives, or manifests used as support only. |
| `claim_status` | Claim class such as explanatory derivative, source-boundary overview, current-state snapshot, generated derivative, or utility page. |
| `forbidden_inferences` | Claims the page must not imply. |
| `freshness_policy` | Whether source freshness is static, packet-local, snapshot-sensitive, or blocked until refresh authorization. |
| `intro_paragraph` | Substantial general-public paragraph immediately after the hero. |
| `internal_next_steps` | Primary internal routes for reader continuation. |
| `provenance_links` | Source or GitHub links for inspection, not primary journey substitution. |
| `validation_gates` | Commands and manual checks required by the packet. |
| `human_review_status` | `not implemented`, `human review pending`, `reviewed with changes requested`, or `reviewed and accepted`. |

The page packet must also state whether manifests, SVG policy checks, browser
QA, source refreshes, or owner review are required before closeout.

## Source-Bundle Requirement

Before claim-bearing copy is written or materially changed, the packet must
inspect or create a source bundle. A source bundle must identify:

- route and page family;
- implementation packet id;
- primary authority sources;
- supporting sources and their non-authority role;
- derivative seed material, if any;
- PRDs consulted;
- claim boundaries;
- forbidden inferences;
- freshness policy;
- validation commands;
- human review status;
- manifest or provenance implications.

Generated explainers, memory, prior summaries, diagrams, registries, and
website pages may help locate material, but they do not replace direct source
inspection for claims.

## Page Grammar

Greenfield pages must choose structure by reader job:

| Form | Use when |
| --- | --- |
| Narrative band | The reader needs staged explanation in a deliberate sequence. |
| Evidence rail | The reader needs source flow, claim gates, provenance, or process order. |
| Status dossier | The reader needs dense current-state, claim-status, metadata, or download information. |
| Matrix or table | The reader needs comparison, classification, or checklist evidence. |
| Timeline | The reader needs lifecycle or workflow progression. |
| Glossary | Terms need definitions near use. |
| Diagram | Relationships are clearer visually and can satisfy SVG or diagram policy. |
| Ordinary cards | Items are true peer choices, galleries, catalogues, inventories, or small unordered route choices. |

Default card-grid authoring is rejected. If a later packet uses more than four
ordinary cards in one section, its closeout must justify why the section is a
gallery, catalogue, inventory, or peer-choice list.

## Preserved Footer Requirements

The greenfield shell must preserve the current footer semantics:

- source-authority notice that the website is a publication and presentation
  layer;
- copyright and license path;
- project GitHub badge or equivalent project repository link;
- creator identity;
- creator profile badges or equivalent profile links;
- accessible labels and link targets.

The visual layout may change, but the information and behavior must remain
available.

## Hero, SVG, And Diagram Rules

Every substantive page must begin with a hero, title, action, and visual area
appropriate to the route. Directly after that area, the page must include a
substantial general-public introductory paragraph.

SVG artwork must remain animated, accessible, and textless. Visible labels
belong in HTML headings, captions, prose, ARIA labels, `<title>`, or `<desc>`,
not inside the SVG artwork itself.

Diagram packets must preserve the static source-to-public-artifact discipline:
editable source, generated public image where applicable, alt text, caption,
nearby explanatory prose, manifest or provenance coverage when required, and a
clear non-authority boundary.

## Validation Profiles

Use the narrowest validation profile that covers the packet:

| Packet type | Required validation |
| --- | --- |
| Control or documentation packet | `git diff --check`, `npm run validate:implementation-control` when control records change, `.venv/bin/python -m pytest` when control records or tests are touched, and manual control-record inspection. |
| Foundation or shared-shell packet | `git diff --check`, `npm run validate`, `.venv/bin/python -m pytest`, and desktop/mobile browser QA when runtime code, routes, styles, or manifests change. |
| Page packet | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run build`, and desktop/mobile browser QA for changed routes. |
| SVG or diagram packet | Page-packet checks plus `npm run validate:svg` and `npm run validate:manifests` when assets or manifests change. |
| Release packet | `npm run validate`, `npm run quality`, route smoke tests, and owner review ledger inspection. |

If a validator is skipped, the packet closeout must name the concrete reason.
Deployment remains blocked until owner review marks the rebuilt page set
`reviewed and accepted`.

## Review Ledger Requirement

Every route packet must update
`docs/quality/sitewide-greenfield-review-ledger.md` with:

- route;
- page family;
- implementation packet;
- technical status;
- human review status;
- source-bundle status;
- validation summary;
- remaining blocker or next review action.

Initial route status is `not implemented` unless a packet has produced a
technically valid route ready for owner review. A technically valid route may
be marked `human review pending`; it must not be marked accepted without owner
review.

## References

The AEther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Product
requirements document].

The AEther Flow Website. (2026). *Implementation Plan: Sitewide Greenfield
Rebuild* [Implementation plan].

The AEther Flow Website. (2026). *Public Comprehension Review Standard*
[Quality standard].

The AEther Flow Website. (2026). `AGENTS.md` [Repository operating rules].
