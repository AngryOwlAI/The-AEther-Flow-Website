# Internal Explainer And Source Assets PRD

Date: 2026-06-26

## Problem Statement

The deployed website now has a strong public overview at `/project/overview/`,
but parts of the project reading path still send readers to GitHub as the
primary explanation surface. That behavior conflicts with the intended purpose
of The AEther Flow Website: the website should explain, describe, and promote
The AEther Flow Project inside the website itself, while GitHub remains
available for source inspection and provenance.

The public reader problem has three parts.

First, the upstream project already has reviewed public explainer material in
`github-facing/`, but the website has not yet internalized the full reviewed
set as curated reader-facing pages.

Second, the website currently exposes sample PDF and TeX fixtures rather than
the current canonical ontology PDF and TeX package from the source project. A
reader should be able to read PDFs and download PDF/TeX files directly from the
website without going to GitHub.

Third, the project is living. The website needs a provenance and refresh model
that records what upstream source state each public page or asset was adapted
from, while deferring automatic live synchronization until a later phase.

## Solution

Create the next public release of the website as an internal, source-backed
reading system.

The release will convert the 17 reviewed upstream `github-facing` explainers
into curated internal website pages. The pages should not be near-verbatim
mirrors. They should be reader-facing adaptations: clearer, more inviting, and
more promotional about the project's purpose, rigor, workflow, and openness,
without promoting unproven physics conclusions or silently changing scientific,
mathematical, governance, or research-workflow claims.

GitHub links remain available, but they move to visible source-provenance
sections and machine-readable provenance manifests. Primary navigation, route
cards, and "where to go next" areas should point to internal website routes for
mapped explainers.

The release will also import the current canonical ontology PDF/TeX package
from the source project into the website repository under stable public asset
paths. The files are committed to the website repo so Cloudflare Pages builds
remain self-contained. A small intentional import script should copy approved
assets, preserve upstream basenames, compute hashes, and update manifests. It
must report drift rather than delete website files automatically.

## User Stories

1. As a general reader, I want clicking through the website to open website
   pages, so that I can understand the project without using GitHub as the
   primary reading interface.
2. As a physics-interested reader, I want internal pages for the physics
   program, ontology, Exact-GR benchmark boundary, GR derivation roadmap, and
   claim gates, so that I can follow the research track in a coherent order.
3. As a reader interested in the AI research-agent system, I want internal
   pages for workflow, roles and skills, memory/registries, and parent-child
   synthesis, so that I can understand how the research process is structured.
4. As a reader interested in project operation, I want an operations landing
   page and operational explainers, so that publication, routing, validation,
   technical requirements, and project-system improvement are understandable
   without searching the repository.
5. As a reader evaluating credibility, I want every explainer page to show a
   boundary statement and source provenance, so that I can distinguish
   website explanation from upstream authority.
6. As a reader inspecting documents, I want to read ontology PDFs directly and
   download both PDF and TeX files from the website, so that GitHub is not
   required for basic document access.
7. As a reader comparing PDF and TeX files, I want the website to state that
   registered TeX files carry source authority while PDFs are generated
   human-readable derivatives, so that I do not mistake derivatives for
   independent authority.
8. As a returning reader, I want to see when a page was last refreshed from
   source, so that I know the website may lag behind the living project.
9. As the project owner, I want source commit hashes, source paths, GitHub
   links, page hashes, and asset hashes recorded, so that future sync and
   review tooling has a concrete baseline.
10. As a maintainer, I want validators to fail when provenance is missing,
    route mappings are incomplete, page hashes drift, assets are missing, or
    mapped GitHub links appear in primary journey cards, so that the website
    cannot regress to the current failure mode.
11. As a mobile or motion-sensitive reader, I want the new pages, diagrams,
    document actions, and progressive-disclosure controls to remain usable,
    readable, and reduced-motion compatible.
12. As an implementation agent, I want a phased release contract, so that the
    full 17-page and asset scope can be implemented in bounded, verifiable
    packets.

## Implementation Decisions

### Deliverable Classes

This release has three deliverable classes.

1. The 17 mapped curated explainer pages. Each is tied one-to-one to an
   upstream `github-facing` Markdown file.
2. The additional `/project/operations/` synthesis landing page. It is sourced
   from six operations explainers and marked as a curated synthesis, not a
   one-to-one adaptation.
3. The `/resources/documents/` ontology asset library. It is sourced from
   canonical `ontology/pdfs/*.pdf`, `ontology/tex/*.tex`, and the upstream
   TeX registry.

### Route Map

The required 17 one-to-one explainer mappings are:

| Website route | Upstream reviewed source |
| --- | --- |
| `/project/overview/` | `github-facing/project-overview-explainer.md` |
| `/project/physics/` | `github-facing/aether-flow-physics-program-explainer.md` |
| `/project/physics/ontology/` | `github-facing/aether-flow-ontology-explainer.md` |
| `/project/physics/exact-gr-benchmark/` | `github-facing/exact-gr-benchmark-boundary-explainer.md` |
| `/project/physics/gr-derivation-roadmap/` | `github-facing/gr-derivation-roadmap-explainer.md` |
| `/project/physics/claim-gates/` | `github-facing/claim-gates-explainer.md` |
| `/project/ai-research-agent-system/` | `github-facing/research-agent-workflow-explainer.md` |
| `/project/ai-research-agent-system/roles-and-skills/` | `github-facing/roles-and-skills-explainer.md` |
| `/project/ai-research-agent-system/memory-registries/` | `github-facing/memory-system-explainer.md` |
| `/project/ai-research-agent-system/parent-child-synthesis/` | `github-facing/parent-child-synthesis-explainer.md` |
| `/project/operations/director-agentjob-lifecycle/` | `github-facing/director-agentjob-lifecycle-explainer.md` |
| `/project/operations/role-routing/` | `github-facing/role-routing-explainer.md` |
| `/project/operations/validator-operator-workflow/` | `github-facing/validator-operator-workflow-explainer.md` |
| `/project/operations/publication-process/` | `github-facing/documentation-curator-publication-process-explainer.md` |
| `/project/operations/project-system-improvement/` | `github-facing/project-system-improvement-explainer.md` |
| `/project/operations/technical-requirements/` | `github-facing/technical-requirements-explainer.md` |
| `/project/source-authority/` | `github-facing/source-authority-explainer.md` |

Add `/project/operations/` as a required synthesis landing page. Its
provenance should cite:

- `github-facing/director-agentjob-lifecycle-explainer.md`
- `github-facing/role-routing-explainer.md`
- `github-facing/validator-operator-workflow-explainer.md`
- `github-facing/documentation-curator-publication-process-explainer.md`
- `github-facing/project-system-improvement-explainer.md`
- `github-facing/technical-requirements-explainer.md`

`/project/ai-research-agent-system/` remains a track landing page, even though
its primary source is the research-agent workflow explainer. It should route to
roles and skills, memory/registries, parent-child synthesis, and relevant
operations pages.

`/project/physics/` remains a track landing page, even though its primary
source is the physics program explainer. It should route to ontology, Exact-GR
benchmark, GR derivation roadmap, claim gates, and canonical ontology
documents.

### Information Architecture

Use three primary project route families:

- `/project/physics/...` for physics explainers.
- `/project/ai-research-agent-system/...` for AI research-agent conceptual
  explainers.
- `/project/operations/...` for publication process, technical requirements,
  validator/operator workflow, project-system improvement, role routing, and
  Director/AgentJob lifecycle.

Keep `/project/source-authority/` as a focused trust-boundary page for how to
read the whole site. Do not turn it into the container for every operational
concept.

Keep main navigation concise:

- Overview
- Physics
- AI System
- Operations
- Source Authority
- Resources

Remove `/research/map/` from main navigation. Preserve the existing `/research`
redirect as a secondary legacy shortcut for now.

### Redirects

Add permanent redirects only for currently existing or publicly deployed routes
that move. Do not add speculative aliases.

Known required redirect:

- `/project/ai-research-agent-system/validator-operator-workflow/` ->
  `/project/operations/validator-operator-workflow/`

### Internal-First Link Behavior

Primary navigation, internal route cards, related reading, and "where to go
next" areas must point to internal website pages for mapped explainers.

GitHub links are allowed in source-provenance zones. They should open in the
same tab by default. If a future design uses `target="_blank"`, it must include
`rel="noopener noreferrer"` and visible or assistive labeling.

### Asset Scope

First asset release includes only the current canonical ontology PDF and TeX
package:

- `ontology/pdfs/*.pdf`
- `ontology/tex/*.tex`

Do not publish `legacy_ontology` as primary material. Do not bulk-publish
research-control draft/control TeX artifacts. Legacy ontology snapshots may be
added later only as an explicitly labeled archive with `archival_noncanonical`
status.

Use exact upstream basenames under clean website folders:

- `/files/pdf/ontology/<upstream-basename>.pdf`
- `/files/tex/ontology/<upstream-basename>.tex`

Commit imported assets into the website repository. Cloudflare Pages builds
must not depend on local sibling paths or private build-time access to the
source project.

The reader-oriented document order is:

1. `aether_flow_foundations`
2. `aether_flow_dynamics`
3. `aether_flow_geometry`
4. `aether_flow_relativistic_recovery`
5. `aether_flow_consistency`
6. `aether_flow_exact_closure_note`
7. `aether_flow_exact_closure_sequence_overview`
8. `aether_flow_exact_closure_flagship_article`

Rename `/resources/documents/` from "Document Sample Library" to "Ontology
Documents" for this release. Remove sample PDF/TeX fixtures from public
manifests and public UI once canonical ontology documents are imported. Sample
files may be deleted if tests no longer require them, or moved into isolated
test fixtures.

Use direct static PDF URLs for "Read PDF." Provide explicit "Download PDF" and
"Download TeX" links. Do not build a custom PDF viewer. Do not render full TeX
documents into HTML in this release.

### Document Access Placement

Link canonical ontology documents from:

- `/project/physics/`
- `/project/physics/ontology/`
- `/project/physics/exact-gr-benchmark/`
- `/resources/documents/`

Other pages may link to the document library only when contextually relevant.
Do not scatter document-download CTAs everywhere.

### Provenance Model

Add a public `page_provenance.json` under `public/files/manifests/`, plus a
public JSON schema such as `page_provenance.schema.json`. The schema should be
publicly inspectable, while a Python validator enforces route/file/hash checks.

Use a checked-in JSON route/source mapping as the contract. It should enumerate
the 17 mapped explainers, `/project/operations/`, `/resources/documents/`, and
`/resources/` if that page is redesigned as a source-backed reader guide.

The generated `page_provenance.json` should include, at minimum:

- website route path;
- local page source path;
- SHA-256 hash of the local page source file;
- adaptation type, such as `one_to_one_adaptation`, `curated_synthesis`,
  `asset_index`, or `curated_index`;
- upstream source repository name;
- upstream source path or paths;
- upstream source commit hash recorded at import/adaptation time;
- upstream source commit date when available;
- import/adaptation date used for visible "Last refreshed from source";
- GitHub `main` URL for reader-facing current inspection;
- commit-pinned GitHub URL when available;
- upstream source SHA-256 when the source file is locally available;
- `upstream_authority_status`;
- `website_publication_status`;
- boundary type, such as `claim_boundary`, `authority_boundary`,
  `operational_boundary`, or `trust_boundary`;
- omission reason when an upstream source hash cannot be computed.

Separate upstream authority from website publication status.

Example upstream authority statuses:

- `canonical`
- `generated_noncanonical`
- `draft_control_artifact`
- `archival_noncanonical`

Example website publication statuses:

- `published`
- `approved_asset`
- `provenance_only`
- `planned`
- `excluded_first_release`

Visible source-provenance panels should show concise reader-friendly source
links. The current `main` link can be primary. A smaller "Pinned source
version" link may appear when space permits. The machine-readable manifest must
store both current and pinned references when available.

Visible "Last refreshed from source" dates should use import/adaptation date,
not build date. Source commit date should be stored separately when available.
Visible dates should not drift from provenance data. The preferred
implementation is rendering from provenance data; validator comparison is an
acceptable first implementation if render-time use is not yet clean.

### Import And Generation Scripts

Add a small intentional script for canonical ontology asset import. It should:

- copy `ontology/pdfs/*.pdf` and `ontology/tex/*.tex`;
- preserve basenames;
- write to the website public folders;
- compute SHA-256 hashes;
- update `source_manifest.json` and `asset_manifest.json`;
- record source path, source commit, approval status, and usage notes;
- report drift, missing upstream inputs, renamed files, or deleted upstream
  files;
- avoid automatic deletion of website files.

Add a page provenance generator. It should:

- read the checked-in JSON route/source mapping;
- compute local page hashes;
- compute upstream source hashes when the source project is locally available;
- record the source commit at generation time;
- write `page_provenance.json`;
- avoid local absolute paths and private machine details in the public output.

### Shared Components

Use a hybrid implementation model. Keep each page individually authored so
copy can be curated and reader-oriented, but extract shared page furniture:

- source provenance or source notice component;
- internal route-card/list component;
- document-actions component for PDF/TeX rows;
- related-reading component or pattern;
- status/boundary panels where repeated.

Existing `SourceNotice` may be extended or a new `SourceProvenance` component
may be introduced, whichever fits the codebase with the smallest correct
change.

### Boundary Statements

Every public explainer page should include a visible boundary statement. Labels
vary by page type:

- physics pages: "Claim boundary";
- AI research-agent pages: "Authority boundary";
- operations pages: "Operational boundary";
- source authority page: "Trust boundary".

Curated copy may be warmer and clearer than upstream Markdown, but exact
claim-status qualifiers must be preserved in boundary/provenance sections when
relevant. Examples include `generated_noncanonical`, `draft/control`,
`proposal-only`, `open derivation`, `archival_noncanonical`, and human-gated
authority qualifiers.

### Visual And Interaction Direction

Preserve the accepted dark Variant A identity from the existing overview PRD:
dark graphite/black backgrounds, warm amber/gold accents, ivory/smoke text,
restrained brass outlines, and SVG/CSS visual motifs. Do not reopen the hero
concept, variant selection, or overall visual schema.

Use animation intensity tiers:

- track landing pages may use richer animated SVG/CSS motifs;
- deep explainer pages should use restrained motion, diagrams, source-status
  panels, and progressive disclosure where useful;
- operations pages should feel precise and systems-oriented while belonging to
  the same visual system.

Require at least one meaningful visual orientation element per route family:
Physics, AI System, Operations, Source Authority, and Resources. Do not force
diagrams onto every page. Prefer site-authored SVG/CSS diagrams for reader
orientation, with "visual orientation only" language when needed. Import
upstream diagrams only when they are approved source-backed visual artifacts.

Use progressive disclosure only where density warrants it. Default content
should remain public-readable. Denser diagrams, technical statuses, and source
lists can appear behind "More detail" controls or lower-page sections.

### Reader Journey

Add reader-journey support to overview, resources, and track landing pages.
Useful journeys include:

- Start here;
- If you want physics;
- If you want the AI research-agent system;
- If you want operations;
- If you want source verification;
- If you want documents.

This supports non-specialist comprehension without replacing the accepted
dual-track information architecture.

### SEO And Indexability

Actual content pages should be indexable unless there is a specific reason not
to index them. The root redirect page can retain `noindex`.

Require simple metadata:

- unique page titles;
- unique descriptions;
- canonical paths;
- sensible Open Graph/Twitter metadata if the layout supports it or can add it
  cleanly.

Do not require sitemap generation in this release unless Astro support is
already present or trivial. A route manifest and route smoke tests are higher
priority.

### Release Definition Of Done

The release is done when:

- all 17 mapped explainers exist as internal curated pages;
- `/project/operations/` exists as a curated synthesis landing page;
- `/resources/documents/` is a production "Ontology Documents" library;
- primary journey cards link internally rather than to mapped GitHub sources;
- canonical ontology PDFs and TeX files are served from the website;
- public sample fixtures are removed from public manifests and public UI;
- provenance is visible and machine-readable;
- route/source mapping, `page_provenance.json`, and page provenance schema
  exist;
- redirects are in place for known deployed moved routes;
- validation, build, route smoke tests, asset checks, and representative
  browser QA pass;
- the release is locally deployment-ready, with actual deployment performed
  only by explicit later authorization.

## Phased Implementation Guidance

### Phase 1: Route And Provenance Contract

Create the route/source mapping JSON, page provenance schema, and page
provenance validator. Define required adaptation types, statuses, boundary
types, and route coverage. The validator should fail if required routes are
missing from the manifest, local page files are missing, or stored page hashes
do not match current file content.

### Phase 2: Internal Page Coverage

Implement or update the 17 curated internal explainer pages and the operations
synthesis page. Preserve the accepted overview identity while integrating the
new route map. Move operational canonical URLs under `/project/operations/...`
and keep AI/physics track pages as landing pages.

### Phase 3: Canonical Ontology Asset Import

Add and run the intentional import script for canonical ontology PDFs and TeX.
Update manifests, document-library UI, tests, and public resource copy. Remove
sample fixtures from public UI and public manifests.

### Phase 4: Navigation, Redirects, And Shared UI

Update primary navigation, internal route cards, source provenance components,
document action components, related reading, and known redirects. Remove
`/research/map/` from main navigation while preserving the existing `/research`
legacy shortcut.

### Phase 5: Validation And Browser QA

Run repository validation, manifest validation, page provenance validation,
build, route smoke tests, asset reachability checks, and representative browser
QA on desktop and mobile. Broaden screenshot coverage if page layouts diverge.

### Phase 6: Future Sync Design

Document the future automated sync direction: compare recorded source commits,
paths, and hashes against upstream current state; report stale pages/assets as
warnings; propose updates for review; do not auto-update or auto-delete
published material without an explicit review path.

## Testing Decisions

### Required Validators And Checks

The release should require:

- `npm run validate`;
- existing Cloudflare Pages config validation;
- source and asset manifest validation;
- new page provenance validation;
- static asset path checks;
- redirects verification;
- no build-time dependency on local sibling source paths;
- route smoke tests derived from the route/source mapping or generated page
  provenance manifest;
- a targeted content validation rule that rejects mapped-source GitHub URLs in
  primary journey zones while allowing them in provenance zones.

The page provenance validator is source-level only. It should not inspect built
HTML. Built-route existence belongs to build/preview smoke tests.

### Asset Validation

Asset validation should confirm that every manifest PDF/TeX path:

- exists in `public/`;
- builds into `dist/`;
- returns successfully under local preview;
- appears on `/resources/documents/`;
- has correct bytes and SHA-256 in the manifest.

At least one local browser or HTTP check should confirm a direct PDF URL is
reachable. TeX validation may be link/file existence and hash validation unless
content-integrity checks are expanded later.

### Route And Browser QA

Smoke coverage should include all required routes from the route/provenance
contract.

Screenshot review should cover every new or materially changed top-level
family page plus at least one representative detail page per family on desktop
and mobile. Full screenshot review of all 17 mapped explainers is optional
unless substantial unique layouts are used. If layouts diverge, broaden
screenshot coverage.

### Accessibility Acceptance

At minimum, verify:

- one `h1` per page;
- heading order sanity;
- keyboard-reachable links and controls;
- visible focus states;
- reduced-motion behavior;
- sufficient contrast;
- no incoherent text overlap on mobile or desktop;
- meaningful link text.

A full automated accessibility dependency is optional unless already available
or justified.

### What Not To Test As Implementation Detail

Do not test decorative animation internals as release criteria. Test observable
behavior: reduced-motion response, non-overlap, readability, route correctness,
document-link reachability, and provenance visibility.

## Source Authority And Provenance

The upstream source project remains authoritative for scientific,
mathematical, governance, and research-workflow claims. The website may
explain, organize, and promote reviewed source material, but it must not create
or strengthen claims beyond source support.

The source project currently contains the reviewed `github-facing` explainer
set, the canonical ontology TeX/PDF package, and registries that distinguish
canonical ontology sources from generated derivatives, archival snapshots, and
draft/control artifacts. The PRD's current planning evidence observed source
commit `5621442706f83f44187864ff44a5ad8a9cf6cfff`, but implementation must
compute and record the source commit live at import/adaptation time.

Registered TeX files carry source authority for ontology and benchmark
material. PDFs are generated human-readable derivatives. Website pages must
state this where ontology documents are presented or promoted.

APA 7-style references for this PRD:

- AEther-Flow Project. (2026). `README.md` [Project front door and dual-track
  research program summary].
- AEther-Flow Project. (2026). `github-facing/*.md` [Reviewed generated
  noncanonical public explainer set].
- AEther-Flow Project. (2026). `ontology/README.md` [Ontology source and
  derivative authority boundary].
- AEther-Flow Project. (2026). `ontology/tex/README.md` [Ontology TeX source
  authority and PDF derivative boundary].
- AEther-Flow Project. (2026). `registries/TEX_SOURCE_REGISTRY.csv`
  [Registered TeX source metadata and claim status].
- The AEther Flow Website. (2026). `CONTEXT.md` [Website vocabulary and Source
  Authority Boundary].
- The AEther Flow Website. (2026). `PRDs/dual-project-public-overview-prd.md`
  [Accepted public overview foundation].
- The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`
  [Current asset source manifest].
- The AEther Flow Website. (2026). `scripts/validate_manifest_paths.py`
  [Current manifest validation behavior].

## Risk Register

| Risk | Mitigation |
| --- | --- |
| Website copy overclaims physics status. | Require source-backed adaptation, visible boundary panels, exact qualifier preservation, and provenance validation. |
| GitHub remains the primary reader journey. | Require internal route cards and targeted validation against mapped-source GitHub links in primary zones. |
| Upstream content becomes stale. | Record source commits and hashes now; add future warning-level drift detection. |
| Asset or provenance data drifts from files. | Hash assets and page sources; fail validation on missing files or hash mismatch. |
| Readers confuse TeX authority and PDF derivatives. | State the TeX/PDF authority distinction in document library and relevant physics pages. |
| Redirects break known deployed links. | Add evidence-limited permanent redirects for currently deployed moved routes. |
| Animation harms comprehension or accessibility. | Use intensity tiers, reduced-motion support, and browser QA for non-overlap/readability. |
| Sample fixtures leak into production UI. | Remove sample fixtures from public manifests and UI; update tests accordingly. |
| Local source paths leak into public manifests. | Public manifests must use repository-relative paths and public URLs only. |
| Automatic deletion removes published assets. | First import script reports drift but does not delete website files. |

## Out Of Scope

- Automatic live sync from the source project.
- Backend services or dynamic server-side behavior.
- Full TeX-to-HTML rendering.
- Publishing `legacy_ontology` as current material.
- Bulk publishing research-control draft/control TeX artifacts.
- Treating website pages as scientific, mathematical, governance, or
  research-workflow authority.
- Adding speculative route aliases without deployed-link evidence.
- Reworking the accepted overview hero, variant selection, or visual direction.
- Building a custom PDF viewer.
- Requiring sitemap generation unless already trivial.
- Deploying the release without a separate explicit deployment request.

## Further Notes

The logical next step is to turn this PRD into a phased implementation plan.
That plan should begin with the route/source mapping and provenance validator
because they define the contract for the remaining pages, assets, smoke tests,
and future sync checks.

Deployment readiness should be defined by local validation and browser QA. The
actual Cloudflare Pages deployment should remain a separate owner-approved
action after implementation acceptance.
