# Sitewide Greenfield Rebuild PRD

Date: 2026-06-30

## Problem Statement

The current AEther Flow Website has accumulated too many routes, cards, and
page-body patterns. The result is difficult to read as one coherent public
information space. The title and hero often identify the topic, but many pages
do not give enough immediate context for a general reader before moving into
technical or governance detail.

The project owner wants a clean rebuild rather than a light redesign. The old
implementation, route structure, and card-heavy default authoring model should
be retired. The rebuild must still preserve the visual and trust elements that
are working: the hero/title/action-button direction, the animated SVG hero
language, the current footer, and the diagram generation/display discipline.

## Solution

Rebuild the website around a smaller, clearer information architecture:

- Home
- Physics Research
- AI Research System
- Resources

Home is a page. The other three are top-level navigation categories with
dropdown menus and category landing pages. The body layouts should be rebuilt
from the website-information-space PRD family rather than copied from the old
route tree.

The new design should explain, describe, and promote the AEther Flow Project
with a stronger comprehension sequence:

1. Hero/title/action/SVG area.
2. A substantial one-paragraph general-public introduction to the page topic.
3. Technical, scientific, operational, or professional sections.
4. Source boundary, provenance, related routes, and footer.

Cards are not banned, but they must stop being the default page grammar. Use
ordinary cards only when the items are true peer choices with no strong
sequence, dependency, or authority relation. Prefer narrative bands, evidence
rails, status dossiers, diagrams, matrices, tables, timelines, and structured
explanatory sections when those forms better match the information.

## User Stories

1. As a general reader, I want every page to explain its topic in one
   substantial introductory paragraph, so that I understand what I am reading
   before the page becomes technical.
2. As a general reader, I want the top navigation to have only a few clear
   categories, so that I am not forced to understand the old project route
   structure.
3. As a physics-interested reader, I want the Physics Research category to
   separate ontology, exact-GR compatibility, derivation burden, flow geometry,
   claim status, and open burdens.
4. As an AI researcher, I want the AI Research System category to explain the
   governed research workflow, current state, AgentJobs, roles, validators,
   handoffs, memory, improvement loops, and runtime requirements.
5. As a reviewer, I want Resources to contain source authority, registries,
   generated derivatives, retrieval layers, publication process, library,
   reading paths, repository map, site-builder guidance, and diagrams.
6. As the project owner, I want the old card-heavy implementation removed or
   retired, so that the rebuild does not preserve the structure I objected to.
7. As the project owner, I want the current hero/title/action-button direction
   preserved, so that the rebuild keeps the successful first-viewport identity.
8. As the project owner, I want the existing animated SVG hero language
   preserved, so that the site keeps its living technical identity.
9. As the project owner, I want the current footer preserved, so that source
   authority, project identity, creator attribution, license, and profile links
   remain intact.
10. As the project owner, I want the Diagram Gallery to remain under Resources
    and keep its gallery-format idea, while removing the current diagram
    inventory and preparing for future diagrams.
11. As a maintainer, I want human review to block deployment, so that technically
    valid pages are not treated as accepted before the project owner reviews
    them.
12. As an implementation agent, I want feedback packets to implement requested
    review changes and rerun validation, so that review is an iterative gate
    rather than a one-time comment.

## Implementation Decisions

### Rebuild Scope

This PRD authorizes a greenfield website rebuild plan, not an immediate file
deletion. Implementation should replace the old presentation architecture in
bounded packets, then remove obsolete routes, components, CSS tokens, and
content models once replacement pages exist and validation passes.

The old `/project/...` route scheme does not need to be preserved. The new
route model should be short and category-based.

### Preserved Elements

Preserve these elements through the rebuild:

- hero/title/action-button structure;
- animated SVG hero direction and existing successful hero visual language;
- current footer content and behavior, including source-authority notice,
  copyright/license, project GitHub badge, creator identity, and profile badges;
- static diagram generation and display discipline;
- Diagram Gallery as a Resources page, with its gallery-format idea retained.

The preserved elements may be integrated into the new layout system, but they
must not be removed, demoted, or replaced by unrelated design patterns.

### Top Navigation

Use this top-level navigation:

| Navigation item | Type | Role |
| --- | --- | --- |
| Home | Page | Public first surface for project identity, dual-track thesis, hero, and first orientation. |
| Physics Research | Dropdown category | Physics and mathematics explanation surfaces. |
| AI Research System | Dropdown category | Governed AI research workflow, current state, operations, roles, validation, and runtime surfaces. |
| Resources | Dropdown category | Source authority, registries, library, publication, repository, site-builder, and diagram surfaces. |

### Route Scheme

Use this route scheme unless a later implementation plan identifies a concrete
reason to adjust a slug:

```text
/
/physics/
/physics/ontology/
/physics/exact-gr-benchmark/
/physics/derivation-roadmap/
/physics/flow-geometry/
/physics/claim-status/
/physics/open-burdens/

/ai-research-system/
/ai-research-system/current-state/
/ai-research-system/workflow/
/ai-research-system/agentjob-lifecycle/
/ai-research-system/roles-and-schemas/
/ai-research-system/human-gated-promotion/
/ai-research-system/validators-and-handoffs/
/ai-research-system/memory-preflight/
/ai-research-system/project-system-improvement/
/ai-research-system/runtime-requirements/

/resources/
/resources/source-authority/
/resources/registries/
/resources/generated-derivatives/
/resources/retrieval-layers/
/resources/publication-process/
/resources/library/
/resources/reading-paths/
/resources/repository-map/
/resources/site-builder-guide/
/resources/diagrams/
```

### Page Inventory

The rebuild should create these pages:

| Category | Pages |
| --- | --- |
| Home | Home |
| Physics Research | Physics Overview, Ontology, Exact-GR Benchmark, Derivation Roadmap, Flow Geometry, Physics Claim Status, Open Burdens |
| AI Research System | AI Research System Overview, Current State, Research-Agent Workflow, AgentJob Lifecycle, Roles and Schemas, Human-Gated Promotion, Validators and Handoffs, Memory Preflight, Project-System Improvement, Runtime Requirements |
| Resources | Resources Overview, Source Authority, Registry Explorer, Generated Derivatives, Local Retrieval Layers, Publication Process, Library, Reading Paths, Repository Map, Site Builder Guide, Diagram Gallery |

### Page Format Rule

Every page should identify its page family, source anchors, claim status,
internal-first navigation role, and validation gates. The visual structure
should follow the information type:

- use command-band or narrative-band sections for major topic transitions;
- use evidence rails for sequences, reader journeys, provenance, source flows,
  and claim gates;
- use status dossiers for dense metadata, current state, claim status, source
  status, and downloads;
- use diagrams for relationships that are easier to understand visually;
- use matrices, tables, and glossaries when comparison or definition is the
  reader job;
- use ordinary cards only when items are genuine peer choices.

Default card-grid authoring is explicitly rejected. A page may use two to four
ordinary cards when that is the clearest form. More cards are allowed only when
the section is inherently a gallery, catalogue, inventory, or peer-choice list
and the implementation explains why the card form is appropriate.

### Introduction Paragraph Rule

Directly below the hero/title/action/SVG area, every substantive page must have
one substantial introductory paragraph aimed at a general-public audience. This
paragraph must explain:

- what the topic is;
- why it matters to the AEther Flow Project;
- how it connects to the physics track, AI research system, source authority,
  or resources;
- what the page will help the reader understand.

The sections after this paragraph may become more technical, scientific,
operational, or professional.

### Diagram Gallery Rule

The Diagram Gallery remains a Resources page. It should keep the existing
gallery-format idea, static generated diagram display, captions, provenance,
and non-authority boundary. The current diagram inventory should be removed
during the rebuild unless a diagram is explicitly reapproved for the new
information architecture. Future diagrams should be added through the existing
Mermaid-source-to-static-public-asset workflow, with manifest and provenance
coverage where applicable.

### Human Review Loop

Deployment is blocked until the project owner accepts the reviewed pages.
Implementation packets may close as `human review pending` only when the page
is technically valid and ready for owner review.

If the owner requests changes, the next work should open a follow-up feedback
packet. That packet must implement the feedback, rerun relevant automated
validation and browser QA, and return the page to owner review. A page is not
accepted until the owner review status is `reviewed and accepted`.

## Testing Decisions

Future implementation packets should use validation appropriate to the changed
surface:

- build affected Astro routes as static pages;
- run content, link, layout, SVG, provenance, manifest, and build validators
  when those surfaces change;
- run public-comprehension validation for claim-bearing pages;
- regenerate page and asset provenance or hashes after route or asset changes;
- perform desktop and mobile browser QA for changed pages;
- verify the first viewport, intro paragraph, navigation dropdowns, footer,
  diagrams, text wrapping, and absence of layout overlap;
- record review status as `human review pending`, `reviewed with changes
  requested`, or `reviewed and accepted`;
- block deployment unless the owner has accepted the reviewed page set.

The PRD itself is a planning artifact. It does not require route, manifest, or
asset validation until implementation begins.

## Source Authority and Provenance

The rebuild must preserve the Source Authority Boundary:

- authoritative scientific, mathematical, governance, and research-workflow
  claims remain in the upstream AEther Flow Project;
- website pages are explanatory derivatives;
- source links remain available as provenance;
- internal website routes remain the primary reader journey;
- the PRD family supplies requirements, not canonical claim authority;
- current-state content remains freshness-sensitive and must use dated source
  basis and stale-data behavior.

The primary planning source for the rebuild is the website-information-space
PRD family. Page implementation must inspect the relevant source bundles before
writing or publishing claim-bearing copy.

## Out of Scope

This PRD does not itself:

- delete the current implementation;
- implement the new route tree;
- change source claims;
- mutate upstream source-project files;
- refresh current-state source snapshots;
- regenerate diagrams;
- publish new public assets;
- push or deploy;
- approve pages for production release.

## Further Notes

The logical next step is to convert this PRD into a bounded implementation plan
with phased packets. The first implementation packet should create the new
site shell, navigation model, preserved footer, and one representative page
without deleting old routes. Later packets should migrate each category and
only then remove obsolete implementation surfaces.

An improvement will be to add a small review ledger for rebuild pages that
tracks page route, technical validation status, owner review status, requested
changes, revalidation commands, and acceptance date.

## References

The AEther Flow Website. (2026). *AGENTS.md instructions* [Repository
operating rules].

The AEther Flow Website. (2026). *PRD-00: AEther-Flow Website information
space* [Master website information architecture and requirements].

The AEther Flow Website. (2026). *PRD-01: High-level components* [Homepage,
overview, dual-track framing, and reader-journey requirements].

The AEther Flow Website. (2026). *PRD-02: Physics and mathematical components*
[Physics page-family requirements].

The AEther Flow Website. (2026). *PRD-03: Research-control and agent workflow*
[AI research-agent workflow requirements].

The AEther Flow Website. (2026). *PRD-05: Memory, registry, and retrieval
components* [Source authority, registry, derivative, and retrieval boundary
requirements].

The AEther Flow Website. (2026). *PRD-06: Documentation, publication, and
website components* [Library, publication, and page-template requirements].

The AEther Flow Website. (2026). *PRD-09: Current research frontier for
website use* [Current-state freshness and source-precedence requirements].

The AEther Flow Website. (2026). *PRD-10: Website positioning guidance*
[Approved positioning, forbidden claims, and copy QA requirements].

The AEther Flow Website. (2026). *Public comprehension review standard*
[Human review status and comprehension-review expectations].
