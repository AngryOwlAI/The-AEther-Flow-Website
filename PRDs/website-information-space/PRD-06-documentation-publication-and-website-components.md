---
prd_id: "PRD-06"
title: "Documentation, Publication, and Website Components"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Documentation, publication workflow, page templates, and library surfaces"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-10-website-positioning-guidance.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-06: Documentation, Publication, and Website Components

## 1. Summary

This PRD defines the website requirements for the documentation and
publication system behind The AEther Flow Website. It covers publication
workflow, source specs, publication briefs, generated GitHub-facing Markdown,
tracked HTML explainers, page-type templates, library surfaces, parity checks,
visual strategy, and source-backed page footer design.

The central product rule is that publication quality and source authority are
separate. The website may reuse polished reader-facing explainers as seed
material, but those surfaces remain generated or derivative unless a higher
authority source record says otherwise.

## 2. Product Purpose

The website needs a repeatable publication system because the project already
contains multiple reader-facing output layers: Markdown source specs,
publication briefs, GitHub-facing Markdown explainers, tracked HTML explainers,
PDF derivatives, registry rows, and source-authority pages.

This PRD gives future page builders the requirements for turning that corpus
into coherent website pages without weakening the upstream source hierarchy.
It should make the site feel like an integrated reading surface rather than a
thin index of repository files.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, or research-workflow authority.

Source basis for implementation should include:

- `README.md`;
- `CONTEXT.md`;
- `markdown/publication-briefs/`;
- `markdown/html-explainer-specs/`;
- `github-facing/`;
- `html/`;
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`;
- `registries/HTML_EXPLAINER_REGISTRY.csv`;
- `.codex/skills/html-visual-explainer/SKILL.md`;
- `.agents/roles/research_ops/documentation-curator.v0.7.0.md`;
- the website master, positioning, and source-authority PRDs.

Implementation must treat Markdown source specs and publication briefs as the
publication planning lane, GitHub-facing Markdown and tracked HTML as generated
reader derivatives, and upstream canonical sources or registries as the
authority lane for public claims.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Find a clear reading path through overview, concept, boundary, and library material without learning the repository first. |
| Physicist or reviewer | Distinguish published explainers from canonical physics sources before evaluating technical claims. |
| AI researcher | Understand the publication process as governed documentation work, not model-generated authority. |
| Contributor | Learn what must exist before proposing a new source-backed website page. |
| Operator | Know which source spec, publication brief, registry row, derivative output, and validator evidence belong to a publication packet. |
| Site builder | Reuse existing explainers, visual strategies, and source bundles while preserving parity and claim boundaries. |

## 5. Scope

In scope:

- publication process explainer requirements;
- page-type template library requirements;
- source-spec and publication-brief template requirements;
- GitHub Markdown and website parity guide requirements;
- visual strategy catalogue requirements;
- source-backed page footer design requirements;
- library and reading-path surface requirements;
- publication validation and acceptance criteria.

Out of scope:

- implementing public routes or library pages;
- regenerating HTML, Markdown, PDFs, wiki pages, or `.local/` retrieval layers;
- changing upstream source-project files;
- changing public manifests;
- promoting scientific claims;
- replacing the existing publication process with an ungoverned website-only
  authoring workflow.

## 6. Non-Goals

This PRD must not:

- treat tracked HTML as canonical source authority;
- treat GitHub-facing Markdown as stronger than the source spec, publication
  brief, registry row, or upstream source basis;
- make generic template compliance a substitute for publication quality;
- require every page to follow a single universal section skeleton;
- expose internal publication metadata as the main reader experience;
- require a route implementation before the PRD family is complete.

## 7. Website Surfaces

Required surfaces:

- Publication process explainer;
- Page-type template library;
- Source-spec template;
- Publication-brief template;
- GitHub Markdown and website parity guide;
- Visual strategy catalogue;
- Source-backed page footer design.

Supporting surfaces:

- library overview;
- reading-path pages;
- explainer catalogue;
- reviewer packet index;
- page-to-source bundle cards;
- documentation-quality checklist;
- publication validation checklist.

## 8. Functional Requirements

1. Define page-type requirements for project overview pages, concept
   explainers, boundary explainers, status dashboards, role catalogues,
   registry/source maps, operator guides, site-builder guides, and library or
   reading-path pages.
2. Require every major planned page to declare audience, reader job, source
   basis, claim boundary, visual strategy, acceptance criteria, and freshness
   rule if applicable.
3. Require a source-spec model for pages derived from `markdown/html-explainer-specs/`.
4. Require a publication-brief model for reader job, document type, narrative
   structure, visual strategy, acceptance criteria, and forbidden patterns.
5. Require GitHub-facing Markdown, tracked HTML, and website pages derived from
   the same source bundle to preserve source basis, authority boundary, and
   core claims.
6. Require tracked HTML explainers to remain generated noncanonical reader
   surfaces unless an upstream authority record says otherwise.
7. Require website page templates to foreground subject matter before process
   metadata.
8. Require visual strategies to be page-specific and source-backed rather than
   generic decoration.
9. Require a source-backed footer or equivalent provenance note on every major
   publication-derived website page.
10. Require publication validation to distinguish structural compliance from
    editorial quality.

## 9. Non-Functional Requirements

- Accuracy: Publication pages must preserve source hierarchy and claim
  boundaries.
- Editorial quality: Pages should explain the project, not merely describe the
  file or process that generated the page.
- Maintainability: Templates should reduce repeated decisions without forcing a
  brittle universal section structure.
- Auditability: Each published page should point to its source spec,
  publication brief, registry row, and upstream source basis where applicable.
- Portability: The publication process should support static website pages and
  generated no-network explainers without requiring external services.
- Reversibility: A page can be revised by updating the source spec and brief,
  regenerating derivatives, and validating parity.

## 10. Claim Boundary

This PRD may specify website content that explains:

- the AEther / AEther-flow ontology as a research ontology;
- the exact-GR benchmark as the current observable-scale benchmark;
- the GR derivation burden as open;
- the AI research-agent workflow as governed, source-first, bounded, and
  human-scaffolded;
- current status only as a dated snapshot from tracked project sources.

This PRD must not authorize website content claiming:

- GR has been derived from AEther / AEther-flow;
- matter coupling has been solved;
- Einstein equations have been derived from source-side substrate structure;
- the benchmark has been promoted from first principles;
- validators, generated docs, registries, or handoffs are physics proof;
- local negative results are global theory rejection without tracked authority.

Additional publication boundary:

Publication workflow, page templates, visual strategies, validation results,
and generated derivatives may improve reader comprehension. They do not
independently authorize source claims.

## 11. Content Requirements

The publication process explainer must define this source-to-publication chain:

| Layer | Function | Website use |
| --- | --- | --- |
| Canonical source or registry | Source basis for claim-bearing material | Verify public claims and authority class. |
| Markdown source spec | Publication source lane for an explainer | Define purpose, audience, outputs, source materials, and claim boundary. |
| Publication brief | Reader-experience and quality contract | Define reader job, document type, visual strategy, acceptance criteria, and forbidden patterns. |
| GitHub-facing Markdown | Repository-browser and AI-reader derivative | Reuse as seed copy when source hierarchy is preserved. |
| Tracked HTML explainer | No-network human reader derivative | Reuse as design/content prior, not as independent authority. |
| Website page | Integrated public reading surface | Present subject-first content with provenance and internal navigation. |

Required page-type library entries:

- overview article;
- concept explainer;
- comparison or boundary map;
- workflow guide;
- decision or lifecycle guide;
- reference catalogue;
- troubleshooting or operator guide;
- contributor/operator guide;
- visual brief;
- reading path.

Required copy fragments:

- "Publication pages are reader surfaces, not source authority."
- "A generated explainer can guide reading, but public claims still require
  source-basis verification."
- "Parity means shared source basis, authority boundary, and core claims; it
  does not require identical section order."
- "Validation proves process conformance; it does not prove physics claims."

## 12. UX and Navigation Requirements

The publication UX should:

- keep internal website routes primary for reader journeys;
- link source and GitHub artifacts as provenance rather than as the first
  reading step;
- organize library material by reader job, not only by file type;
- provide badges or short labels for source-backed, generated derivative,
  current snapshot, and requirements-planning status;
- expose source-spec and publication-brief links where they help reviewers and
  contributors;
- avoid leading general readers into registry tables before explaining what
  the material means.

The page-type template UX should:

- start with the subject being explained;
- move authority, source, freshness, and provenance details into visible but
  secondary boundary sections;
- support diagrams, matrices, timelines, decision trees, source maps, and
  annotated tables only when they teach a page-specific idea.

## 13. Data, Source, and Provenance Requirements

Every publication-derived website page should declare:

- page type;
- audience;
- reader job;
- source basis;
- source authority class;
- derivative status;
- claim boundary;
- freshness rule, if current status is used;
- visual strategy;
- publication brief, where applicable;
- source spec, where applicable;
- registry row or manifest reference, where applicable;
- acceptance criteria.

Parity requirements:

- GitHub-facing Markdown and tracked HTML should preserve the same source
  basis, authority boundary, and core claims.
- Website adaptations should preserve those same constraints while improving
  navigation, structure, and reader experience.
- Website copy may reorganize the generated derivative when doing so improves
  comprehension and does not alter claim status.

## 14. User Stories

1. As a first-time reader, I want a library page organized around what I am
   trying to understand, so that I do not need to know the repository layout.
2. As a physicist, I want publication pages to reveal source basis and claim
   status, so that I can separate explanation from authority.
3. As an AI researcher, I want generated explainers labeled as derivatives, so
   that I do not mistake a model-assisted publication layer for source truth.
4. As a contributor, I want source-spec and publication-brief templates, so
   that new page proposals start from the correct evidence.
5. As an operator, I want a validation checklist for parity and source
   grounding, so that publication packets can be reviewed repeatably.
6. As a site builder, I want a page-type library and visual strategy catalogue,
   so that future routes can be built consistently without generic page
   skeletons.

## 15. Acceptance Criteria

- Every planned publication page has a source basis and claim boundary.
- The publication process distinguishes reader surfaces from canonical
  authority.
- No tracked HTML, GitHub-facing Markdown, generated wiki, or publication page
  is treated as independent scientific authority.
- The website system can reuse existing explainer content while preserving
  source hierarchy.
- Every major planned page declares audience, reader job, source basis, claim
  boundary, visual strategy, acceptance criteria, and freshness rule if
  applicable.
- Page templates prioritize subject-first explanation over self-referential
  process description.
- Publication validators are described as process and parity checks, not proof
  mechanisms.

## 16. Dependencies

- PRD-00 defines the master website information architecture.
- PRD-10 defines approved public messaging and forbidden claims.
- PRD-05 defines source authority, derivative, retrieval, and provenance
  boundaries.
- PRD-11 will define the quick source map for future site builders.
- PRD-01, PRD-02, and PRD-09 depend on this PRD when their pages reuse
  publication-derived explainers or library surfaces.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Generated explainers become treated as canonical source pages. | Require derivative labels, source/provenance footers, and canonical source checks. |
| Templates produce generic pages that describe themselves instead of the project. | Require subject-first openings and page-specific reader jobs. |
| HTML, GitHub Markdown, and website pages drift in authority boundary. | Validate parity on source basis, authority boundary, and core claims. |
| Visual strategy becomes decorative or repetitive. | Require each major visual to have a page-specific purpose and source basis. |
| Library pages overwhelm readers with repository structure. | Organize by reading path and reader job before exposing file-type catalogues. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Check that every planned publication page declares source basis and claim
   boundary.
2. Check that source specs, publication briefs, derivative outputs, and website
   adaptations preserve source hierarchy.
3. Check GitHub-facing Markdown, tracked HTML, and website pages for shared
   source basis, authority boundary, and core claims.
4. Check that publication validators are described as operational/process
   checks rather than scientific proof.
5. Check page openings for subject-first explanation rather than
   self-referential page metadata.
6. Run applicable publication-process, content, provenance, build, and browser
   QA validators for implementation packets.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: MVP foundation.

This PRD should follow PRD-05 and PRD-10 because publication pages need source
authority and safe messaging rules before they can become public website
requirements.

## 20. Open Questions

1. Should the first implementation expose a full publication workflow page, or
   fold publication guidance into the site-builder guide until the route family
   is larger?
2. Should source-spec and publication-brief templates be rendered as public
   pages, maintainer-only docs, or both?
3. Should the library organize first by reader journey, source type, topic, or
   claim status?
4. What minimum browser QA evidence should be required when a publication page
   includes a complex visual strategy?

These questions do not block this PRD. They should be resolved in PRD-01,
PRD-02, PRD-09, PRD-11, or follow-on implementation plans.

## 21. Definition of Done

This PRD is complete when:

- it defines the documentation and publication workflow for website use;
- it specifies source-spec, publication-brief, GitHub Markdown, tracked HTML,
  and website parity requirements;
- it defines page-type template, library, reading-path, visual-strategy, and
  footer requirements;
- it preserves the boundary that generated reader surfaces are not source
  authority;
- it gives future publication and library pages a testable requirements
  contract.

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].

The AEther Flow Website. (2026). *Website Positioning Guidance* [Product
requirements document].

The AEther Flow Website. (2026). *Memory, Registry, and Retrieval Components*
[Product requirements document].
