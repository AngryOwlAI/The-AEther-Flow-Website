# Documents Navigation and Documentation Architecture Implementation Plan

**Project:** The AEther Flow Website\
**Repository:** `AngryOwlAI/The-AEther-Flow-Website`\
**Production site:** `https://the-aether-flow-website.pages.dev/`\
**Plan status:** Proposed implementation plan\
**Baseline inspected:** `main` at commit `3a2c8560f8f98d918a388677242b901c8e36a6f9`\
**Suggested repository location:** `docs/implementation-plans/documents-navigation-and-documentation-architecture.md`\
**Plan date:** 2026-07-16\
**Implementation authorization:** This document is a plan only. It does not authorize a commit, push, deployment, upstream-source mutation, or publication of new scientific claims.

---

## 1. Executive Summary

This implementation replaces the current top-level **Resources** navigation dropdown with a focused top-level **Documents** dropdown and reorganizes the website's public documentation into a coherent, category-based information architecture.

The intended final navigation is:

```text
Documents
├── Documentation Overview
├── Anthology Articles
├── Research Articles
├── Governance & Control
└── Diagram Gallery
```

The current `/resources/library/` page will be renamed and substantially rewritten as **Documentation Overview**. It will become the canonical `/documents/` landing page and explain the site's document categories, formats, authority roles, provenance conventions, status labels, and reading paths.

The current `/resources/documents/` page is not a general documents overview. It is an ontology-focused TeX/PDF collection. It will become the initial **Research Articles** collection at `/documents/research/`.

The current `/resources/diagrams/` page will move to `/documents/diagrams/` while preserving its manifest filtering, conceptual groups, captions, alt text, provenance, and non-authority framing.

Every other former Resources menu option will be removed from the primary navigation. Its associated page will be one of the following:

1. Moved beneath the Documents namespace.
2. Consolidated into a more appropriate Documents page.
3. Retained only as a redirect if its content is redundant.
4. Retired after all internal links and provenance records point to the replacement.

The migration will preserve the project's source-authority boundary:

- Registered TeX can carry scoped research-source authority.
- PDF commonly serves as a human-readable derivative.
- Approved Markdown can carry governance or operational authority within its stated scope.
- Diagrams remain explanatory visual aids.
- Website pages remain reader-facing adaptations.
- Manifests and hashes establish artifact identity and provenance, not scientific correctness.

The implementation should be thorough in architecture and content, but deliberately light in testing. During implementation, run only targeted checks relevant to the files changed. Before an authorized deployment, run one aggregate repository validation because the repository's existing release discipline requires it. Do not add a broad new test suite, perform exhaustive multi-browser testing, or repeatedly run the full quality gate during each phase.

---

## 2. Goals

### 2.1 Primary goals

- [ ] Replace the top-level **Resources** dropdown with **Documents**.
- [ ] Remove every former Resources child from the primary navigation.
- [ ] Add a concise Documents dropdown with exactly five category-level entries.
- [ ] Rename **Library** to **Documentation Overview**.
- [ ] Make `/documents/` the canonical documentation landing page.
- [ ] Reclassify the current ontology TeX/PDF page as **Research Articles**.
- [ ] Move the Diagram Gallery beneath Documents.
- [ ] Provide category pages for anthology PDFs, TeX/PDF research articles, approved governance/control Markdown, and diagrams.
- [ ] Preserve the project's source, derivative, governance, and provenance boundaries.
- [ ] Retire the `/resources/` namespace through explicit semantic redirects.
- [ ] Update route manifests and page provenance only after canonical page locations are final.
- [ ] Keep validation proportional and minimal.

### 2.2 Secondary goals

- [ ] Make document discovery understandable without exposing repository layout as the first reader task.
- [ ] Group multiple formats of one logical document into a single reader-facing record.
- [ ] Prevent the existing ontology importer from deleting unrelated future PDF and TeX records.
- [ ] Add first-class support for approved Markdown document assets.
- [ ] Preserve stable existing ontology asset URLs during the navigation migration.
- [ ] Keep the header's current keyboard, mobile, no-script, active-state, and disclosure behavior.
- [ ] Reduce menu density and make the documentation taxonomy scalable.

---

## 3. Non-Goals and Scope Boundaries

The following work is explicitly outside this implementation unless separately authorized:

- [ ] Do not alter scientific, mathematical, governance, or research-workflow claims in upstream source files.
- [ ] Do not promote a draft or generated document to canonical status.
- [ ] Do not publish every Markdown file from the upstream research repository.
- [ ] Do not recursively expose internal control records, temporary task files, private paths, or unreviewed current-state material.
- [ ] Do not redesign the global header component unless a defect is discovered during the navigation change.
- [ ] Do not add a search service, database, content-management system, or external indexing dependency.
- [ ] Do not move existing ontology files merely to make their URLs match the new page namespace.
- [ ] Do not create a blanket `/resources/* -> /documents/` redirect.
- [ ] Do not deploy as an automatic consequence of completing the code changes.
- [ ] Do not run the complete test, lint, browser, and quality suite after every task.
- [ ] Do not treat hashes, manifests, validator output, screenshots, or diagrams as proof of scientific correctness.
- [ ] Do not convert the public Documents section into maintainer-only repository documentation.
- [ ] Do not remove historical redirect compatibility until the explicit replacement route is live.

---

## 4. Current-State Findings That Drive the Plan

### 4.1 Navigation is data-driven

The shared header reads `siteNavigationLinks` from `src/lib/siteContent.ts`. `BaseLayout.astro` renders direct links and disclosure menus from that data. The current component already supports:

- Parent active state through `matchPrefixes`.
- Exact child active state.
- Mobile menu disclosure.
- Dropdown disclosure.
- Escape-key closing.
- Outside-click closing.
- Focus return.
- No-script fallback navigation.
- Responsive dropdown containment.

**Implementation consequence:** update the navigation data first. Do not rewrite the header logic unless the new menu reveals a real defect.

### 4.2 The current Resources menu is too broad

The current Resources dropdown mixes:

- Resources Overview.
- Source Authority.
- Registries.
- Generated Derivatives.
- Retrieval Layers.
- Publication Process.
- Library.
- Reading Paths.
- Repository Map.
- Site Builder Guide.
- Diagram Gallery.

This is not one coherent reader category. It combines document collections, governance explanations, provenance systems, reading utilities, and maintainer guidance.

**Implementation consequence:** the replacement menu must contain category-level document destinations only.

### 4.3 The current Library page is a reader-routing page

`src/pages/resources/library/index.astro` is organized around reader jobs, library shelves, internal-first links, publication, retrieval, provenance, and general Resources navigation.

**Implementation consequence:** reuse its strongest principles, but rewrite its identity, hero, section labels, route links, content data names, ARIA identifiers, captions, and page metadata. A superficial title replacement is insufficient.

### 4.4 The current Documents page is ontology-specific

`src/pages/resources/documents.astro` publishes a canonical ontology package with paired TeX and PDF assets and a specialist reading order.

**Implementation consequence:** move it into the Research Articles category. Do not use it as the general Documentation Overview.

### 4.5 The Diagram Gallery already has the correct content boundary

`src/pages/resources/diagrams.astro` filters approved diagram manifest entries, removes duplicates, groups by concept, and uses `DiagramGalleryList.astro`.

**Implementation consequence:** relocate and recopy the page, but preserve the gallery component and its data contract.

### 4.6 Routes are coupled to provenance

The project tracks canonical routes in:

```text
public/files/manifests/page_route_map.json
public/files/manifests/page_provenance.json
scripts/validate_page_provenance.py
```

**Implementation consequence:** route moves require coordinated route-map and provenance updates. Perform those updates after page paths are final, not during early scaffolding.

### 4.7 Current redirects point in the wrong direction for the new architecture

The current Cloudflare redirect configuration includes routes such as:

```text
/documents -> /resources/documents/
/diagrams -> /resources/diagrams/
/downloads -> /resources/
```

**Implementation consequence:** replace these mappings before `/documents/` becomes canonical. Otherwise the new architecture can create redirect loops or contradictory canonical destinations.

### 4.8 The ontology importer is unsafe for future document collections

`scripts/import_ontology_assets.py` currently removes all PDF and TeX manifest rows before re-adding the ontology package.

**Implementation consequence:** fix importer ownership before adding anthology PDFs or non-ontology research TeX/PDF assets.

---

## 5. Adopted Information Architecture

### 5.1 Primary navigation

The final primary navigation will contain:

```text
Home
Physics Research
AI Research System
Documents
```

No top-level **Resources** item will remain.

No former Resources child will remain as a direct top-level navigation item.

### 5.2 Documents dropdown

The Documents dropdown will contain exactly these entries, in this order:

| Order | Label | Canonical route | Purpose |
|---:|---|---|---|
| 1 | Documentation Overview | `/documents/` | Explain categories, formats, status, authority, provenance, and reading paths |
| 2 | Anthology Articles | `/documents/anthology/` | Reader-facing anthology PDF publications |
| 3 | Research Articles | `/documents/research/` | TeX sources and corresponding readable PDFs |
| 4 | Governance & Control | `/documents/governance/` | Approved governance, control, registry, publication, and workflow Markdown |
| 5 | Diagram Gallery | `/documents/diagrams/` | Approved manifest-backed public diagrams |

### 5.3 Contextual routes that should not clutter the dropdown

The following routes may exist beneath Documents without becoming dropdown entries:

```text
/documents/research/ontology/
/documents/governance/source-authority/
/documents/governance/registries/
/documents/governance/publication-process/
/documents/governance/retrieval-layers/
/documents/governance/repository-map/
/documents/governance/site-builder-guide/
/documents/reading-paths/
/documents/reading-paths/general-public/
/documents/reviewer-packet/
/documents/derivatives/
```

These pages are secondary reader destinations. They should be reached through category pages, related-route cards, or contextual links.

### 5.4 Canonical route policy

- `/documents/` is the canonical documentation landing page.
- `/documents/research/` is the canonical research document index.
- `/documents/diagrams/` is the canonical gallery.
- The old `/resources/.../` routes become redirect-only compatibility paths.
- Existing physical asset paths remain stable unless a later asset migration is separately approved.

---

## 6. Adopted Migration Strategy

Use a staged migration inside one implementation program.

### Stage A: establish the new canonical system

1. Fix importer ownership.
2. Add document data types and category definitions.
3. Add the new `/documents/.../` routes.
4. Rewrite Documentation Overview.
5. Move Research Articles and Diagram Gallery.
6. Add Governance & Control and Anthology category pages.
7. Switch primary navigation.
8. Update primary internal links.
9. Add redirects for the highest-value old routes.

### Stage B: retire the remaining Resources system

1. Move or consolidate all remaining Resources pages.
2. Update every inbound internal link.
3. Add explicit semantic redirects.
4. Remove old Resources page sources.
5. Update route maps, required routes, and provenance.
6. Remove stale Resources product-language from public pages.
7. Perform one final lightweight release check.

This staged approach keeps each change understandable while ensuring the final state fully removes the Resources navigation and namespace.

---

# Phase 0: Establish the Implementation Contract

## Objective

Freeze the naming, route, authority, and scope decisions before code movement begins.

## Task 0.1: Record the baseline

**Required**

Record:

```text
Repository: AngryOwlAI/The-AEther-Flow-Website
Branch: main
Baseline commit: 3a2c8560f8f98d918a388677242b901c8e36a6f9
```

Implementation must re-check the live branch before starting. If `main` has advanced, inspect navigation, Resources pages, redirect configuration, and manifest code again before applying this plan.

**Acceptance criteria**

- [ ] The implementation task records the actual starting commit.
- [ ] Any divergence from the inspected baseline is noted.
- [ ] No file from an unrelated active task is silently overwritten.

## Task 0.2: Adopt the naming contract

**Required**

Use these exact public labels unless later copy review changes capitalization:

```text
Documents
Documentation Overview
Anthology Articles
Research Articles
Governance & Control
Diagram Gallery
```

Avoid these as page identities:

```text
Resources
Resources Overview
Library
Resources / Library
Resources / Diagram Gallery
Ontology Documents
```

The phrase “document library” may remain in ordinary prose when it describes a collection, but **Library** must not remain the product name or primary page title.

**Acceptance criteria**

- [ ] All developers use one naming set.
- [ ] Navigation, page titles, hero headings, breadcrumbs, and ARIA labels agree.

## Task 0.3: Adopt the authority contract

**Required**

The following public meanings must remain consistent:

| Surface | Role |
|---|---|
| Registered TeX | Research source-inspection artifact within its registered status |
| PDF paired with TeX | Human-readable derivative unless metadata explicitly says otherwise |
| Approved Markdown | Governance or operational source within its stated scope |
| Website page | Reader-facing explanation or index |
| Diagram | Explanatory visual aid |
| Manifest | File identity and relationship record |
| Hash | Artifact identity evidence |
| Validator PASS | Bounded process evidence |
| Current-state page | Dated snapshot with freshness limits |

**Acceptance criteria**

- [ ] New copy does not flatten these roles into one “approved document” label.
- [ ] Research, governance, and diagram pages expose role-specific explanations.

## Task 0.4: Confirm the final route map

**Required**

Approve the canonical routes listed in Phase 1 and the redirect mapping listed in Phase 7 before removing old page files.

**Acceptance criteria**

- [ ] Every old Resources route has one explicit replacement.
- [ ] No route is assigned two conflicting destinations.
- [ ] No canonical route redirects to a retired Resources route.

## Task 0.5: Define the implementation boundary

**Required**

This implementation includes website-local navigation, pages, manifests, import tooling, redirects, provenance, and maintainer documentation.

It does not include upstream research-source edits unless a missing approved document record blocks publication. In that case, stop and open a separate upstream-source task.

**Acceptance criteria**

- [ ] Website code does not invent missing registry status.
- [ ] Missing source metadata causes a blocked item, not a guessed label.

---

# Phase 1: Create the Document Domain Model

## Objective

Replace ontology-only document assumptions with a reusable but small document model.

## Task 1.1: Add generic document categories

**Required**

In `src/lib/manifests.ts`, or a new focused module such as `src/lib/documentCatalog.ts`, define:

```ts
export type DocumentCategory =
  | "anthology"
  | "research"
  | "governance"
  | "diagram";

export type DocumentFormat =
  | "pdf"
  | "tex"
  | "markdown"
  | "png"
  | "svg"
  | "mermaid";

export type DocumentAuthorityRole =
  | "authoritative_source"
  | "registered_source"
  | "readable_derivative"
  | "governance_source"
  | "operational_record"
  | "explanatory_derivative"
  | "public_comprehension_asset"
  | "provenance_record";
```

Do not force every project status into one enum if existing manifests already contain more specific values. The generic role is for reader-facing grouping; source-specific statuses remain attached as metadata.

**Acceptance criteria**

- [ ] Category and format values are explicit.
- [ ] Existing ontology records can be represented without losing metadata.
- [ ] Diagram records remain distinct from research documents.

## Task 1.2: Add a logical document record

**Required**

Add a logical document type:

```ts
export type DocumentManifestation = {
  kind: DocumentFormat;
  sitePath: string;
  role: DocumentAuthorityRole;
  title?: string;
  bytes?: number;
  sha256?: string;
  sourceId?: string;
  sourcePath?: string;
  sourceCommit?: string;
  generatedAt?: string;
};

export type DocumentRecord = {
  id: string;
  slug: string;
  title: string;
  category: DocumentCategory;
  collection?: string;
  summary: string;
  status: string;
  authorityScope: string;
  readingOrder?: number;
  tags?: string[];
  manifestations: DocumentManifestation[];
  relatedRoutes?: string[];
};
```

The record represents one logical reader object. A TeX file and its corresponding PDF are manifestations of one research article, not two unrelated cards.

**Acceptance criteria**

- [ ] One research article renders once.
- [ ] All available formats are actions on that record.
- [ ] PDF-only anthology documents remain valid.
- [ ] Markdown-only governance documents remain valid.
- [ ] Diagram records can point to image and source manifestations.

## Task 1.3: Add a document catalog manifest

**Recommended and part of the preferred architecture**

Create:

```text
public/files/manifests/document_catalog.json
```

Suggested shape:

```json
{
  "version": 1,
  "generated_at": "2026-07-16T00:00:00Z",
  "documents": [
    {
      "id": "research:aether-flow-exact-closure-overview",
      "slug": "aether-flow-exact-closure-overview",
      "title": "Exact Closure Sequence Overview",
      "category": "research",
      "collection": "canonical-ontology",
      "summary": "Canonical front door for the exact-closure sequence.",
      "status": "approved",
      "authority_scope": "registered_research_source",
      "reading_order": 1,
      "tags": [
        "physics",
        "ontology",
        "exact-closure"
      ],
      "manifestations": [
        {
          "kind": "tex",
          "site_path": "/files/tex/ontology/aether_flow_exact_closure_sequence_overview.tex",
          "role": "authoritative_source"
        },
        {
          "kind": "pdf",
          "site_path": "/files/pdf/ontology/aether_flow_exact_closure_sequence_overview.pdf",
          "role": "readable_derivative"
        }
      ],
      "related_routes": [
        "/physics/ontology/",
        "/physics/exact-gr-benchmark/"
      ]
    }
  ]
}
```

The document catalog complements, rather than replaces:

```text
source_manifest.json
asset_manifest.json
```

Use:

- `source_manifest.json` for source-level status and provenance.
- `asset_manifest.json` for public file paths, bytes, hashes, and source references.
- `document_catalog.json` for logical grouping, collections, reader summaries, and format pairing.

**Acceptance criteria**

- [ ] Every catalog manifestation resolves to an asset-manifest path.
- [ ] Every asset-manifest path still resolves to a source-manifest item.
- [ ] The catalog does not duplicate file bytes or hashes as a separate authority source.
- [ ] Logical IDs remain stable even if physical paths later change.

## Task 1.4: Preserve ontology sequence behavior

**Required**

Keep `ontologyDocumentSequence` or migrate it into the research collection model.

The sequence remains:

1. Exact Closure Sequence Overview.
2. Exact Closure Note.
3. Foundations.
4. Dynamics.
5. Consistency.
6. Relativistic Recovery.
7. Flow Geometry.
8. Exact Closure Flagship Article.

The current reading-order guidance remains useful and should not be discarded.

**Acceptance criteria**

- [ ] Existing ontology reading order is preserved.
- [ ] Existing source and derivative labels remain visible.
- [ ] The ontology collection becomes one Research Articles collection, not the entire document system.

## Task 1.5: Keep the model small

**Required**

Do not add:

- A database.
- A search index.
- A server API.
- A schema library dependency.
- A client-side state framework.
- A generalized content platform.

Use static JSON, TypeScript, and Astro rendering.

**Acceptance criteria**

- [ ] The site remains a static Astro build.
- [ ] The change adds no runtime service dependency.
- [ ] Data remains inspectable in the repository.

---

# Phase 2: Make Document Import Safe

## Objective

Prevent collection-specific importers from deleting or corrupting unrelated document records.

## Task 2.1: Restrict ontology importer ownership

**Required before importing any new PDF or TeX collection**

Current behavior removes every PDF and TeX item before rebuilding ontology entries. Replace broad kind-based removal with path- or collection-based ownership.

Recommended helper:

```python
def is_ontology_manifest_item(item: dict[str, Any]) -> bool:
    site_path = item.get("site_path") or item.get("path")
    if not isinstance(site_path, str):
        return False

    return (
        site_path.startswith("/files/pdf/ontology/")
        or site_path.startswith("/files/tex/ontology/")
    )
```

Use:

```python
new_source_items = [
    item
    for item in source_manifest.get("items", [])
    if isinstance(item, dict) and not is_ontology_manifest_item(item)
]

new_asset_items = [
    item
    for item in asset_manifest.get("items", [])
    if isinstance(item, dict) and not is_ontology_manifest_item(item)
]
```

Do not remove items only because their kind is `pdf` or `tex`.

**Acceptance criteria**

- [ ] Rerunning the ontology importer preserves anthology PDF rows.
- [ ] Rerunning the ontology importer preserves non-ontology research rows.
- [ ] Rerunning the ontology importer preserves governance Markdown rows.
- [ ] Rerunning the ontology importer preserves diagrams.
- [ ] Unexpected ontology files are reported, not silently deleted.

## Task 2.2: Add first-class Markdown manifest support

**Required for governance document downloads**

Update `scripts/validate_manifest_paths.py`:

```python
ALLOWED_SOURCE_KINDS = {
    "pdf",
    "tex",
    "markdown",
    "image",
    "diagram",
    "manifest",
    "other",
}

ALLOWED_ASSET_KINDS = {
    "pdf",
    "tex",
    "markdown",
    "image",
    "diagram",
    "other",
}
```

Do not classify governance Markdown as `other`.

**Acceptance criteria**

- [ ] Markdown records validate as a known kind.
- [ ] Markdown assets have explicit source-manifest references.
- [ ] Existing kinds continue to validate.

## Task 2.3: Add a collection-oriented importer

**Recommended**

Create a small generic importer:

```text
scripts/import_document_collection.py
```

It should accept a collection configuration or explicit arguments and perform:

1. Load source and asset manifests.
2. Load the selected collection definition.
3. Verify every source file exists.
4. Verify every item has an approved public registry row.
5. Copy only approved files.
6. Compute bytes and SHA-256.
7. Preserve unrelated manifest rows.
8. Update only rows owned by the target collection.
9. Update or regenerate document-catalog records.
10. Report unexpected files.
11. Fail closed on missing authority or approval metadata.

A collection definition can be static JSON or Python data. Avoid introducing YAML parsing if the repository does not already need it here.

**Acceptance criteria**

- [ ] Importing one collection does not mutate another.
- [ ] Duplicate document IDs fail clearly.
- [ ] Duplicate public paths fail clearly.
- [ ] Missing approval status blocks publication.
- [ ] Missing source file blocks publication.
- [ ] No unregistered Markdown file is copied.

## Task 2.4: Define governance Markdown publication safety

**Required**

Governance files must use an explicit allowlist or approved registry source.

Before public copy, check for:

- Secrets.
- API keys.
- Tokens.
- Private email addresses.
- Absolute local filesystem paths.
- Temporary filesystem paths.
- Internal-only repository URLs.
- Non-public task instructions.
- Unreviewed current-state claims.
- Confidential operational details.
- Personal data not intended for publication.
- Links that replace a public internal route with an upstream raw source.

Do not implement a complicated scanner. Use a short deterministic deny-pattern list and explicit human review.

**Acceptance criteria**

- [ ] No recursive Markdown directory import exists.
- [ ] Every public Markdown asset has an explicit allowlist entry.
- [ ] Every public Markdown asset has source and approval metadata.
- [ ] Files containing forbidden private path patterns fail import.

## Task 2.5: Preserve existing physical ontology URLs

**Required**

Retain:

```text
/files/pdf/ontology/
/files/tex/ontology/
```

The page route can move without moving asset paths.

New collections may use:

```text
/files/pdf/anthology/
/files/pdf/research/<collection>/
/files/tex/research/<collection>/
/files/markdown/governance/
```

**Acceptance criteria**

- [ ] Existing document URLs continue to work.
- [ ] Existing external citations do not break.
- [ ] Asset manifests do not churn solely because page routes changed.

## Task 2.6: Add Markdown response headers

**Required if raw Markdown downloads are published**

Update `public/_headers`:

```text
/files/markdown/*
  Content-Type: text/markdown; charset=utf-8
  Cache-Control: public, max-age=3600
```

Keep:

- Immutable caching for hashed static assets.
- Existing PDF caching.
- Existing TeX MIME behavior.
- Existing manifest JSON behavior.
- Existing security headers.

**Acceptance criteria**

- [ ] Markdown downloads return a Markdown content type.
- [ ] `nosniff` does not cause unusable Markdown responses.
- [ ] No existing header rule is weakened.

---

# Phase 3: Create the Canonical Documents Route Family

## Objective

Create the final routes before changing redirects or deleting old pages.

## Task 3.1: Create the route directory

**Required**

Create:

```text
src/pages/documents/
```

Initial canonical pages:

```text
src/pages/documents/index.astro
src/pages/documents/anthology/index.astro
src/pages/documents/research/index.astro
src/pages/documents/governance/index.astro
src/pages/documents/diagrams/index.astro
```

**Acceptance criteria**

- [ ] Every canonical dropdown route has a page.
- [ ] Every page builds statically.
- [ ] Every page has a unique title and description.

## Task 3.2: Create secondary route directories

**Required when the corresponding old Resources content is retained**

Create as needed:

```text
src/pages/documents/governance/source-authority/index.astro
src/pages/documents/governance/registries/index.astro
src/pages/documents/governance/publication-process/index.astro
src/pages/documents/governance/retrieval-layers/index.astro
src/pages/documents/governance/repository-map/index.astro
src/pages/documents/governance/site-builder-guide/index.astro
src/pages/documents/reading-paths/index.astro
src/pages/documents/reading-paths/general-public/index.astro
src/pages/documents/reviewer-packet/index.astro
src/pages/documents/derivatives/index.astro
```

Do not create empty placeholder pages only to satisfy a route table. Each retained route must have a real reader purpose.

**Acceptance criteria**

- [ ] Every redirect destination exists before the redirect is added.
- [ ] Redundant pages are consolidated instead of copied verbatim.
- [ ] Secondary pages are linked from a category page.

## Task 3.3: Keep page layout conventions

**Required**

Reuse established components:

```text
BaseLayout
CommandBand
EvidenceRail
ProjectIntroduction
ComprehensionBlocks
StatusDossier
DiagramGalleryList
```

Use a new component only when repeated document markup is proven across at least two categories.

**Acceptance criteria**

- [ ] New pages match the site design system.
- [ ] No new framework or styling dependency is introduced.
- [ ] Global styles are changed only if a shared document pattern requires them.

## Task 3.4: Define Documents-specific body classes

**Recommended**

Use body classes such as:

```text
documents-page
documents-overview-page
documents-category-page
documents-research-page
documents-governance-page
documents-diagram-page
```

Avoid retaining `resources-greenfield-page` on canonical Documents pages unless it is temporarily required for styling compatibility. If compatibility classes remain during migration, remove them in the cleanup phase.

**Acceptance criteria**

- [ ] Canonical pages do not depend permanently on misleading Resources class names.
- [ ] Styling migration is controlled and does not trigger a site-wide redesign.

---

# Phase 4: Rewrite Library as Documentation Overview

## Objective

Transform the former Library concept into a true documentation-system overview.

## Task 4.1: Create canonical page metadata

**Required**

Use:

```astro
<BaseLayout
  title="Documentation Overview"
  description="Overview of The AEther Flow documentation, including anthology articles, research TeX and PDF publications, governance Markdown, diagrams, provenance, and document status."
  bodyClass="project-overview-page project-track-page documents-overview-page"
>
```

**Acceptance criteria**

- [ ] Browser title identifies Documentation Overview.
- [ ] Meta description names the principal categories and formats.
- [ ] No page metadata uses Library as the page identity.

## Task 4.2: Replace the hero

**Required**

Recommended hero contract:

```text
Eyebrow: Documents / Overview
H1: Documentation Overview
Lead: Explore the project's public documentation by category, format, authority role, and reader purpose. Each document retains its source, derivative, status, and provenance boundaries.
```

Recommended actions:

```text
Browse research articles
Browse governance and control
Open Diagram Gallery
Understand formats and authority
```

**Acceptance criteria**

- [ ] Hero actions point to canonical `/documents/.../` routes.
- [ ] No hero action points to `/resources/`.
- [ ] The lead explains the documentation system rather than repository layout.

## Task 4.3: Rename Library-specific code identifiers

**Required**

Rename identifiers such as:

```text
resourcesLibraryProjectIntroduction
readerPathRows
libraryRows
policyRows
librarySvg
resources-library-title
resources-library-desc
resources-library-caption
library-policy-title
related library routes
Library page actions
```

Suggested replacements:

```text
documentationOverviewIntroduction
documentationReaderPathRows
documentationCategoryRows
documentationPolicyRows
documentationOverviewSvg
documentation-overview-title
documentation-overview-desc
documentation-overview-caption
documentation-policy-title
related documentation routes
Documentation Overview actions
```

**Acceptance criteria**

- [ ] Source names match public page meaning.
- [ ] ARIA IDs remain unique.
- [ ] No stale Library-specific label survives accidentally.

## Task 4.4: Add a Documentation Categories section

**Required**

Display four category cards:

### Anthology Articles

Explain:

- Curated reader-facing publication.
- Usually PDF-first.
- May combine synthesis, exposition, or editorial context.
- Authority status comes from its source record, not from visual polish.

### Research Articles

Explain:

- TeX source and corresponding PDF.
- Source and derivative roles.
- Claim and research status.
- Reading order where applicable.

### Governance & Control

Explain:

- Approved Markdown.
- Policy, schema, procedure, registry guidance, publication process, or operational record.
- Scope and freshness boundaries.

### Diagram Gallery

Explain:

- Approved static visual aids.
- Captions and provenance.
- Non-authority status.
- Concept-based grouping.

Each card should include:

- Category title.
- One-sentence purpose.
- Typical formats.
- Authority note.
- Canonical link.

**Acceptance criteria**

- [ ] All four dropdown categories are represented.
- [ ] Cards do not imply equal authority across formats.
- [ ] Category actions use canonical routes.

## Task 4.5: Add a Format and Authority Guide

**Required**

Use a compact table:

| Format | Typical role | Reader action | Boundary |
|---|---|---|---|
| TeX | Registered research source | Inspect source text | Authority remains scoped to registry status |
| PDF | Human-readable publication | Read or download | May be a derivative of TeX |
| Markdown | Governance or control source | Read rendered page or raw file | Authority applies within stated operational scope |
| PNG/SVG | Explanatory diagram | Inspect visual and caption | Does not independently prove a claim |
| Manifest JSON | Identity and provenance record | Audit hashes and relationships | Hashes establish identity, not correctness |

**Acceptance criteria**

- [ ] The distinction between TeX and PDF is explicit.
- [ ] Markdown is not described as scientific source authority by default.
- [ ] Diagram status is explicit.
- [ ] Hash limitations are explicit.

## Task 4.6: Preserve and rewrite reader paths

**Required**

Retain the reader-job concept, rewritten around documentation.

Recommended rows:

| Reader | Recommended route sequence |
|---|---|
| New reader | Documentation Overview, then Anthology or a project overview page |
| Physics specialist | Physics status pages, Research Articles, source provenance |
| AI workflow reviewer | AI system pages, Governance & Control, relevant records |
| Governance reviewer | Governance & Control, Source Authority, Registries, Publication Process |
| External reviewer | Reviewer Packet, Research Articles, Claim Status, Governance |
| Website maintainer | Documentation Overview, Publication Process, Repository Map, Site Builder Guide |

Each route sequence must start with an internal explanatory page when one exists.

**Acceptance criteria**

- [ ] File downloads do not become the first step for general readers.
- [ ] Specialist readers can reach direct sources quickly.
- [ ] The page remains useful without exposing raw repository paths first.

## Task 4.7: Add a status and freshness guide

**Required**

Explain:

```text
Approved
Draft
Historical
Current snapshot
Generated derivative
Source-index-only
Retrieval support
```

For freshness-sensitive records, show:

- Source date.
- Source commit.
- Website import date.
- Review date when available.
- Current or superseded state.
- A warning when freshness cannot be confirmed.

**Acceptance criteria**

- [ ] Current-state material is not presented as timeless.
- [ ] Generated derivatives are visibly identified.
- [ ] Historical materials remain distinguishable.

## Task 4.8: Add a collections overview

**Required**

List logical collections such as:

```text
Canonical Ontology and Exact Closure
Anthology Volume I
Research Notes
Governance and Research Control
Publication and Provenance
Public Diagram Collection
Reviewer Materials
```

Only display a collection as live when it contains at least one published item.

**Acceptance criteria**

- [ ] Empty planned collections are labeled planned or omitted.
- [ ] Collections group reader meaning, not only file extensions.
- [ ] Collection links lead to category or detail pages.

## Task 4.9: Rewrite related routes

**Required**

Replace Resources-related cards with canonical documentation routes.

Recommended related destinations:

```text
Research Articles
Governance & Control
Diagram Gallery
Reading Paths
Reviewer Packet
Source Authority
```

**Acceptance criteria**

- [ ] No related card points to a retired Resources route.
- [ ] Card labels match the destination.

---

# Phase 5: Implement the Category Pages

## Objective

Provide useful category-level pages that can scale beyond the initial assets.

## Task 5.1: Implement Anthology Articles

**Required as a category page, even if the initial inventory is small**

Canonical route:

```text
/documents/anthology/
```

### Page responsibilities

- Explain what the anthology is.
- Identify whether it is one volume or several collections.
- List available articles.
- Show PDF status and provenance.
- Provide direct reading and download actions.
- Connect each article to relevant internal project pages.
- Distinguish anthology synthesis from research-source authority.

### Recommended card fields

```text
Title
Collection or volume
Author or editorial attribution
Short abstract
Publication status
Publication date
Revision date
PDF bytes
SHA-256
License or usage note
Related internal routes
Read PDF
Download PDF
```

### Initial-state handling

If no approved anthology PDF exists:

- Render the category page.
- Explain the category.
- Show a clearly labeled “No approved public anthology articles are currently listed.”
- Do not invent sample content.
- Do not add an empty download card.
- Keep the navigation entry because the category is part of the approved architecture only if the owner wants the category visible before content exists.
- Otherwise, add the entry when the first approved article is available.

The preferred plan assumes at least one approved anthology PDF will be provided or already exists upstream.

**Acceptance criteria**

- [ ] The page does not falsely imply that planned files are published.
- [ ] Every visible article has a valid public asset path.
- [ ] PDF status is explicit.
- [ ] Anthology content does not replace underlying research sources.

## Task 5.2: Implement Research Articles

**Required**

Canonical route:

```text
/documents/research/
```

### Move current functionality

Move the current Ontology Documents behavior from:

```text
src/pages/resources/documents.astro
```

to:

```text
src/pages/documents/research/index.astro
```

### Rename public identity

Replace:

```text
Ontology Documents
Ontology documents
This library serves...
```

with a category page identity such as:

```text
Research Articles
Canonical ontology and exact-closure collection
This section presents registered research TeX sources and corresponding readable PDFs.
```

### Preserve

- Existing document order.
- Existing TeX/PDF pairing.
- Existing metadata.
- Existing reading guidance.
- Existing source commit.
- Existing import date.
- Existing hash display.
- Existing claim and research status.
- Existing source-authority explanation.

### Add category structure

The page should be able to show multiple collections:

```text
Canonical Ontology and Exact Closure
Research Notes
Technical Appendices
Future approved research collections
```

The initial implementation can render only the canonical ontology collection.

### Recommended article actions

```text
Read PDF
Download PDF
View TeX
Download TeX
Open related explanation
Inspect provenance
```

A raw TeX browser view is optional. A download action is sufficient if the current public server behavior is appropriate.

**Acceptance criteria**

- [ ] Each logical article renders once.
- [ ] TeX and PDF actions are attached to one card.
- [ ] TeX is identified as the source-inspection artifact.
- [ ] PDF is identified as a human-readable derivative.
- [ ] The page title is not Ontology Documents.
- [ ] Existing ontology files remain reachable at their current URLs.

## Task 5.3: Generalize DocumentActions

**Required**

Current `DocumentActions.astro` is ontology-specific. Replace or refactor it into generic document components.

Recommended structure:

```text
src/components/documents/DocumentCollection.astro
src/components/documents/DocumentCard.astro
src/components/documents/DocumentActions.astro
src/components/documents/DocumentMetadata.astro
```

### `DocumentCollection.astro`

Inputs:

```ts
{
  title: string;
  description?: string;
  documents: DocumentRecord[];
  emptyMessage?: string;
}
```

Responsibilities:

- Collection heading.
- Collection description.
- Ordered or unordered document rendering.
- Empty state.

### `DocumentCard.astro`

Inputs:

```ts
{
  document: DocumentRecord;
  showCollection?: boolean;
  showSummary?: boolean;
}
```

Responsibilities:

- Title.
- Summary.
- Status.
- Collection.
- Format badges.
- Actions.
- Metadata.

### `DocumentActions.astro`

Render only available actions.

Rules:

- PDF primary action: `Read PDF`.
- PDF secondary action: `Download PDF`.
- TeX action: `Download TeX` or `View TeX`.
- Markdown primary action: `Read document`.
- Markdown secondary action: `Download Markdown`.
- Diagram primary action: `Open diagram`.
- Provenance action: `Inspect provenance`.

### `DocumentMetadata.astro`

Render:

- Status.
- Authority scope.
- Reading order.
- Source commit.
- Import date.
- Bytes.
- SHA-256.
- Collection.
- Revision.
- Format role.

**Acceptance criteria**

- [ ] No component hard-codes “Ontology document” for every category.
- [ ] Missing formats do not render empty controls.
- [ ] Action labels include file format.
- [ ] Long hashes wrap without horizontal overflow.

## Task 5.4: Implement Governance & Control

**Required**

Canonical route:

```text
/documents/governance/
```

### Category groups

Use groups such as:

```text
Source Authority
Research Control
Roles and Schemas
Publication and Provenance
Registries and Status
Validation and Handoffs
Website Maintenance
Historical Governance Records
```

### Governance document types

Each item should identify one type:

```text
Policy
Schema
Procedure
Registry guide
Current-state record
Maintainer guide
Historical record
```

### Recommended metadata

```text
Title
Document type
Operational scope
Status
Freshness
Source commit
Source date
Website import date
Rendered internal route
Raw Markdown download
Related project route
Superseded-by relationship
```

### Public rendering policy

Primary reader action should open a rendered internal page.

Raw Markdown should be secondary and available only for approved public files.

### Current-state policy

For current-state or program-state records:

- Show the snapshot date.
- State that the record may become stale.
- Do not present it as live unless the site has a verified current refresh process.
- Show superseded status when known.

**Acceptance criteria**

- [ ] Governance documents are explicitly scoped.
- [ ] Raw Markdown is not the only reader surface.
- [ ] Internal-only files are excluded.
- [ ] Freshness-sensitive records carry dates.
- [ ] Scientific authority is not inferred from operational authority.

## Task 5.5: Relocate Source Authority

**Required if the current page remains public**

Move:

```text
/resources/source-authority/
```

to:

```text
/documents/governance/source-authority/
```

Update:

- Page metadata.
- Eyebrow.
- Related routes.
- Internal links.
- Route map.
- Provenance.
- Redirects.

Do not change its core trust-boundary meaning.

**Acceptance criteria**

- [ ] Old URL redirects directly to the new URL.
- [ ] Source Authority remains reachable from Governance & Control.
- [ ] It is not restored as an unrelated top-level Resources item.

## Task 5.6: Relocate Registries

**Required if retained**

Move:

```text
/resources/registries/
```

to:

```text
/documents/governance/registries/
```

Position it as an explanation of registry evidence, status, and provenance.

**Acceptance criteria**

- [ ] Registry rows are not described as proof.
- [ ] Registry pages link back to Governance & Control.
- [ ] Old URL redirects directly.

## Task 5.7: Relocate Publication Process

**Required if retained**

Move:

```text
/resources/publication-process/
```

to:

```text
/documents/governance/publication-process/
```

Update legacy project redirects to point directly to the new route.

**Acceptance criteria**

- [ ] No redirect chain passes through `/resources/publication-process/`.
- [ ] The page remains a publication governance explanation.
- [ ] Route cards use the new URL.

## Task 5.8: Relocate Retrieval Layers

**Required if retained**

Move:

```text
/resources/retrieval-layers/
```

to:

```text
/documents/governance/retrieval-layers/
```

Keep the distinction between retrieval support and source authority.

**Acceptance criteria**

- [ ] Retrieval is described as navigation support.
- [ ] It is not a primary Documents dropdown entry.
- [ ] Old route redirects directly.

## Task 5.9: Relocate Repository Map and Site Builder Guide

**Required if retained**

Move:

```text
/resources/repository-map/
-> /documents/governance/repository-map/

/resources/site-builder-guide/
-> /documents/governance/site-builder-guide/
```

These are maintainer or system documentation, so they belong under Governance & Control, not in the primary dropdown.

**Acceptance criteria**

- [ ] Both routes are linked from Governance & Control.
- [ ] Both old URLs redirect directly.
- [ ] Public-safe boundaries are preserved.

## Task 5.10: Consolidate Reading Paths and Guided Starts

**Required**

Preferred canonical route:

```text
/documents/reading-paths/
```

Map:

```text
/resources/reading-paths/
-> /documents/reading-paths/

/resources/guided-starts/
-> /documents/reading-paths/

/resources/guided-starts/general-public/
-> /documents/reading-paths/general-public/
```

Where content overlaps, merge rather than duplicate.

**Acceptance criteria**

- [ ] One canonical reading-path system exists.
- [ ] Audience-specific content remains available.
- [ ] Old routes do not form redirect chains.

## Task 5.11: Relocate Reviewer Packet

**Required if retained**

Move:

```text
/resources/reviewer-packet/
```

to:

```text
/documents/reviewer-packet/
```

Link it from Documentation Overview and appropriate research/governance pages, but not necessarily from the top dropdown.

**Acceptance criteria**

- [ ] Reviewer Packet remains a specialist route.
- [ ] It does not clutter the dropdown.
- [ ] Old URL redirects directly.

## Task 5.12: Relocate Generated Derivatives

**Required if retained**

Move:

```text
/resources/generated-derivatives/
```

to:

```text
/documents/derivatives/
```

This page explains derivative classes and should not be a primary category unless it becomes a substantial collection.

**Acceptance criteria**

- [ ] Derivative status remains explicit.
- [ ] The page links to research PDFs and diagrams contextually.
- [ ] Old URL redirects directly.

## Task 5.13: Move Diagram Gallery

**Required**

Move:

```text
src/pages/resources/diagrams.astro
```

to:

```text
src/pages/documents/diagrams/index.astro
```

### Preserve

- `DiagramGalleryList.astro`.
- Approved manifest filtering.
- Duplicate-path suppression.
- Concept groups.
- Alt text.
- Captions.
- Original asset links.
- Provenance.
- Responsive image containment.
- Non-authority language.

### Change

- Page route.
- Relative imports.
- Page title metadata only as needed.
- Eyebrow from `Resources / Diagram Gallery` to `Documents / Diagram Gallery`.
- Links to Resources.
- Related route cards.
- Comprehension-content key names containing Resources.
- ARIA labels containing Resources.
- Route map and provenance.

### Recommended hero actions

```text
Browse gallery
Read diagram status
Open Documentation Overview
Read publication governance
```

**Acceptance criteria**

- [ ] Gallery inventory remains unchanged unless manifest content changed separately.
- [ ] Every approved diagram still appears once.
- [ ] Group counts remain stable.
- [ ] No diagram is promoted to source authority.
- [ ] Old route redirects directly to `/documents/diagrams/`.

---

# Phase 6: Replace the Navigation

## Objective

Switch the primary navigation only after all five canonical destinations exist.

## Task 6.1: Replace the Resources object

**Required**

In `src/lib/siteContent.ts`, replace the current Resources navigation object with:

```ts
{
  title: "Documents",
  href: "/documents/",
  matchPrefixes: ["/documents/"],
  children: [
    {
      title: "Documentation Overview",
      href: "/documents/",
      description:
        "Overview of document categories, formats, authority levels, status labels, and recommended reading paths.",
    },
    {
      title: "Anthology Articles",
      href: "/documents/anthology/",
      description:
        "Curated anthology articles and reader-facing PDF publications.",
    },
    {
      title: "Research Articles",
      href: "/documents/research/",
      description:
        "Research papers with registered TeX sources and corresponding readable PDFs.",
    },
    {
      title: "Governance & Control",
      href: "/documents/governance/",
      description:
        "Approved Markdown documents for governance, control, registries, publication, and workflow.",
    },
    {
      title: "Diagram Gallery",
      href: "/documents/diagrams/",
      description:
        "Manifest-backed explanatory diagrams with captions, provenance, and authority boundaries.",
    },
  ],
}
```

**Acceptance criteria**

- [ ] One Documents trigger exists.
- [ ] No Resources trigger exists.
- [ ] The five children appear in the approved order.
- [ ] Every child has a nonempty description.
- [ ] All hrefs are canonical.

## Task 6.2: Preserve BaseLayout behavior

**Required**

Do not modify `BaseLayout.astro` unless necessary.

The existing behavior should continue to provide:

- Active dropdown state for `/documents/.../`.
- Exact active child state.
- Mobile menu.
- No-script fallback.
- Escape and outside-click closing.
- Focus return.

**Acceptance criteria**

- [ ] `/documents/` marks Documentation Overview active.
- [ ] `/documents/research/` marks Documents active and Research Articles current.
- [ ] `/documents/governance/source-authority/` marks Documents active.
- [ ] No-script navigation links Documents to `/documents/`.

## Task 6.3: Update information-architecture metadata

**Required**

Update `projectInformationArchitectureDecision` in `src/lib/siteContent.ts`.

Replace rationale that names Resources with a statement such as:

```text
Primary navigation exposes the public project reading path through Home, Physics Research, AI Research System, and Documents. Documents groups public documentation by category while source authority and provenance remain attached to each item.
```

**Acceptance criteria**

- [ ] Maintainer-facing metadata matches the live header.
- [ ] No stale Resources claim remains in current IA documentation.

## Task 6.4: Remove all former Resources children from navigation data

**Required**

Do not leave hidden or duplicated copies of:

```text
Resources Overview
Source Authority
Registries
Generated Derivatives
Retrieval Layers
Publication Process
Library
Reading Paths
Repository Map
Site Builder Guide
Diagram Gallery under Resources
```

These routes may remain reachable contextually, but not as Resources children.

**Acceptance criteria**

- [ ] Primary navigation contains no former Resources menu.
- [ ] Diagram Gallery appears only beneath Documents.
- [ ] Documentation Overview replaces Library.

## Task 6.5: Check dropdown density manually

**Lightweight required review**

Open the header at one desktop width and one compact width.

Confirm:

- All five entries fit.
- Descriptions wrap normally.
- No horizontal overflow occurs.
- The panel remains keyboard reachable.
- Mobile scrolling remains available when needed.

Do not run a full responsive matrix unless a defect appears.

**Acceptance criteria**

- [ ] Desktop dropdown is usable.
- [ ] Compact menu is usable.
- [ ] No layout fix beyond the menu is required.

---

# Phase 7: Migrate Routes and Redirects

## Objective

Retire the Resources namespace without breaking existing links or creating redirect loops.

## Task 7.1: Add canonical slash redirect

**Required**

Add:

```text
/documents /documents/ 301
```

Use one canonical trailing-slash form.

**Acceptance criteria**

- [ ] `/documents` resolves to `/documents/`.
- [ ] `/documents/` returns the page directly.

## Task 7.2: Replace current reverse redirects

**Required**

Replace:

```text
/documents /resources/documents/ 301
/diagrams /resources/diagrams/ 301
/equations /resources/documents/ 301
/research/equations/ /resources/documents/ 301
/research/math-sample/ /resources/documents/ 301
/downloads /resources/ 301
```

with:

```text
/documents /documents/ 301
/diagrams /documents/diagrams/ 301
/equations /documents/research/ 301
/research/equations/ /documents/research/ 301
/research/math-sample/ /documents/research/ 301
/downloads /documents/ 301
```

**Acceptance criteria**

- [ ] No redirect destination begins with retired `/resources/` for these aliases.
- [ ] No redirect loop exists.

## Task 7.3: Add explicit Resources redirects

**Required**

Use:

```text
/resources/ /documents/ 301
/resources/library/ /documents/ 301
/resources/documents/ /documents/research/ 301
/resources/diagrams/ /documents/diagrams/ 301
/resources/source-authority/ /documents/governance/source-authority/ 301
/resources/registries/ /documents/governance/registries/ 301
/resources/generated-derivatives/ /documents/derivatives/ 301
/resources/retrieval-layers/ /documents/governance/retrieval-layers/ 301
/resources/publication-process/ /documents/governance/publication-process/ 301
/resources/reading-paths/ /documents/reading-paths/ 301
/resources/repository-map/ /documents/governance/repository-map/ 301
/resources/site-builder-guide/ /documents/governance/site-builder-guide/ 301
/resources/guided-starts/ /documents/reading-paths/ 301
/resources/guided-starts/general-public/ /documents/reading-paths/general-public/ 301
/resources/reviewer-packet/ /documents/reviewer-packet/ 301
```

Only add a line when its destination exists.

**Acceptance criteria**

- [ ] Every retired canonical route has a permanent redirect.
- [ ] Every redirect has one semantic destination.
- [ ] No blanket wildcard redirect is used.

## Task 7.4: Repoint older project redirects directly

**Required**

Update destinations such as:

```text
/project/operations/publication-process/
/project/source-authority/publication-and-provenance-system/
/project/source-authority/
/research
/research/map/
```

Map each directly to the final Documents route.

Example:

```text
/project/operations/publication-process/ /documents/governance/publication-process/ 301
/project/source-authority/publication-and-provenance-system/ /documents/governance/publication-process/ 301
/project/source-authority/ /documents/governance/source-authority/ 301
/research /documents/governance/publication-process/ 302
/research/map/ /documents/governance/publication-process/ 301
```

Retain `302` only when the existing temporary intent remains deliberate. Otherwise use `301`.

**Acceptance criteria**

- [ ] Old project routes do not redirect through `/resources/`.
- [ ] Avoidable redirect chains are removed.

## Task 7.5: Choose one redirect source of truth

**Recommended**

The project currently has redirects in `public/_redirects` and at least one Astro redirect in `astro.config.mjs`.

Preferred approach:

1. Create a small route configuration module or JSON file.
2. Generate or consume the same mappings in both Astro and Cloudflare configurations.
3. Keep `public/_redirects` as the production output.

Lower-overhead acceptable approach:

- Keep `_redirects` authoritative.
- Mirror only critical local-preview redirects in `astro.config.mjs`.
- Add a short maintainer note that Cloudflare is the production source of truth.

Do not build a complicated redirect-generation system solely for this migration.

**Acceptance criteria**

- [ ] No conflicting mapping exists between Astro and Cloudflare.
- [ ] Production redirects are documented.

## Task 7.6: Remove old page source files

**Required after replacements and redirects exist**

Remove:

```text
src/pages/resources/index.astro
src/pages/resources/library/index.astro
src/pages/resources/documents.astro
src/pages/resources/diagrams.astro
```

Remove or relocate all remaining Resources page source files after their replacements are complete.

Do not leave duplicate canonical content at old paths.

**Acceptance criteria**

- [ ] Old Resources paths are redirect-only.
- [ ] Search engines see one canonical content URL.
- [ ] Repository source no longer contains a public Resources route family.

---

# Phase 8: Update Internal Links and Public Language

## Objective

Remove stale Resources routing and product language from current public pages.

## Task 8.1: Inventory references

**Required**

Run:

```bash
rg -n \
  'Resources|Library|/resources/|/documents|/diagrams|/downloads' \
  src public docs scripts tests
```

Classify each result:

- Navigation.
- Page title.
- Hero eyebrow.
- Page description.
- Action link.
- Related-route card.
- ARIA label.
- SVG ID or caption.
- Manifest route.
- Redirect.
- Test assertion.
- Maintainer documentation.
- Historical record that should remain unchanged.

**Acceptance criteria**

- [ ] Every current reader-facing `/resources/` link is migrated.
- [ ] Historical records are not rewritten blindly.

## Task 8.2: Replace primary internal links

**Required**

Update all page journey links to canonical Documents routes.

Examples:

```text
/resources/library/ -> /documents/
/resources/documents/ -> /documents/research/
/resources/diagrams/ -> /documents/diagrams/
/resources/publication-process/ -> /documents/governance/publication-process/
```

**Acceptance criteria**

- [ ] Public pages do not rely on redirects for their own internal links.
- [ ] Direct file links remain secondary actions.

## Task 8.3: Replace stale labels

**Required**

Remove current public labels such as:

```text
Resources / Library
Resources Overview
Return to Resources
Library page actions
Related library routes
Resources route map
Live resource paths
```

Replace with context-specific Documents wording.

**Acceptance criteria**

- [ ] Public navigation and page copy present one coherent system.
- [ ] No page tells the reader to return to a removed Resources page.

## Task 8.4: Retain legitimate generic uses

**Required**

Do not ban the words “resource” or “library” globally.

Legitimate examples:

```text
document library
research resource
source library
resource constraint
```

Only remove obsolete product identities and canonical-route references.

**Acceptance criteria**

- [ ] Copy remains natural.
- [ ] Historical documentation remains accurate.

---

# Phase 9: Update Route Maps, Provenance, and Maintainer Documentation

## Objective

Align project control records with the final canonical route system.

## Task 9.1: Update required route paths

**Required**

In `scripts/validate_page_provenance.py`, remove required canonical page entries for retired Resources routes.

Add:

```python
"/documents/",
"/documents/anthology/",
"/documents/research/",
"/documents/governance/",
"/documents/diagrams/",
```

Add secondary routes only when they exist as canonical pages.

Do not add redirect-only legacy routes.

**Acceptance criteria**

- [ ] Required routes describe canonical pages.
- [ ] Redirect-only paths are excluded.

## Task 9.2: Update page_route_map.json

**Required**

Add canonical route entries for all Documents pages.

For each route, specify:

```text
route_path
local_page_source
title
adaptation_type
upstream_source_paths
upstream_authority_status
website_publication_status
boundary_type
```

Remove old Resources page entries after their source files are removed.

Recommended route titles:

```text
Documentation Overview
Anthology Articles
Research Articles
Governance & Control
Diagram Gallery
```

**Acceptance criteria**

- [ ] Every canonical page has one route-map entry.
- [ ] Local page paths match actual files.
- [ ] Upstream source paths remain ordered and intentional.
- [ ] No route map entry points to a deleted Resources file.

## Task 9.3: Regenerate page provenance

**Required**

After all page content and paths are final:

1. Regenerate local page SHA-256 values.
2. Update route paths.
3. Update local page source paths.
4. Preserve upstream source commit pinning.
5. Preserve source order.
6. Preserve omission reasons.
7. Verify no private local paths appear.

Do not copy old hashes to new page paths.

**Acceptance criteria**

- [ ] Every local hash matches its page.
- [ ] Every canonical route appears once.
- [ ] No retired Resources route remains as a canonical page.

## Task 9.4: Update source and asset manifests only when assets change

**Required**

A route-only migration does not require moving existing ontology or diagram assets.

Update `source_manifest.json` and `asset_manifest.json` only when:

- New anthology files are added.
- New research files are added.
- Governance Markdown downloads are added.
- Asset paths change.
- Existing asset metadata changes.

**Acceptance criteria**

- [ ] Route migration does not create unnecessary asset-manifest churn.
- [ ] New files receive valid source references, bytes, and hashes.

## Task 9.5: Update README.md

**Required**

Update:

- Public route overview.
- Documentation route examples.
- Smoke-test descriptions.
- Any statement that treats Resources as a primary navigation destination.
- Any example that points to old document or diagram routes.

**Acceptance criteria**

- [ ] README route examples match production intent.
- [ ] Source-authority boundary remains explicit.

## Task 9.6: Update AGENTS.md

**Required**

Replace the rule referring to “Library/resource pages under `/resources/`” with a Documents rule.

Suggested wording:

```text
Documents pages under `/documents/` must preserve source, derivative, governance, and diagram authority roles in contextual copy. Do not add a generic authority badge that flattens these distinctions. Use internal explanatory routes as the primary reader journey and direct source or asset links as inspection actions.
```

Update Definition of Done references if they name old routes.

**Acceptance criteria**

- [ ] Repository instructions match the new namespace.
- [ ] Maintainers are warned against authority flattening.

## Task 9.7: Update docs/project-features-and-functionality.md

**Required**

Update:

- Reader-facing route map.
- Primary navigation description.
- Document route descriptions.
- Public assets and manifests section.
- Smoke-test route notes.
- Maintenance checklist.

**Acceptance criteria**

- [ ] Operating map describes Documents rather than Resources.
- [ ] Ontology documents are described as a Research Articles collection.
- [ ] Diagram Gallery uses its canonical route.

## Task 9.8: Update deployment documentation

**Required only where route examples exist**

Update `docs/deployment/cloudflare-pages.md`:

- Replace old Resources route examples.
- Replace sample document/diagram verification paths.
- Keep Direct Upload deployment instructions unchanged.
- Keep deployment as a separately authorized action.

**Acceptance criteria**

- [ ] Deployment checks use canonical routes.
- [ ] Deployment model is not accidentally changed.

## Task 9.9: Update docs/README.md

**Recommended**

Add this implementation plan to the maintainer documentation index after it is committed.

Suggested entry:

```text
- Documents Navigation and Documentation Architecture Implementation Plan:
  phased migration from Resources to Documents, document-category model,
  redirects, manifests, provenance, and lightweight verification.
```

**Acceptance criteria**

- [ ] Maintainers can discover the plan.
- [ ] The plan remains separate from public navigation.

---

# Phase 10: Accessibility, Interaction, and Content Quality

## Objective

Preserve the existing interaction quality without adding a large accessibility program.

## Task 10.1: Preserve navigation semantics

**Required**

Keep:

- `aria-expanded`.
- `aria-controls`.
- `aria-current`.
- Keyboard focus.
- Escape behavior.
- Outside-click close.
- No-script route.
- Touch target sizing.

**Acceptance criteria**

- [ ] Documents trigger is a button.
- [ ] Child destinations are links.
- [ ] Active child uses `aria-current="page"`.

## Task 10.2: Use explicit action labels

**Required**

Use:

```text
Read PDF
Download PDF
Download TeX
Read document
Download Markdown
Open diagram
Inspect provenance
```

Avoid:

```text
Open
View
Download
More
```

when the format or destination would be ambiguous.

**Acceptance criteria**

- [ ] Action meaning is understandable out of context.
- [ ] Screen-reader users hear the format.

## Task 10.3: Preserve heading hierarchy

**Required**

Each page should use:

- One H1.
- H2 for category sections.
- H3 for individual document cards or collection subsections.
- No heading level chosen only for visual size.

**Acceptance criteria**

- [ ] Heading outline is logical.
- [ ] Collection and document labels are distinguishable.

## Task 10.4: Preserve diagram accessibility

**Required**

Keep:

- Descriptive alt text.
- Prose captions.
- Source provenance.
- Original asset link where currently available.
- Static image rendering rather than browser Mermaid dependency.

**Acceptance criteria**

- [ ] Moving the page does not reduce accessible description.
- [ ] Diagram meaning is not embedded only as visible image text.

## Task 10.5: Prevent metadata overflow

**Required**

Ensure long values such as SHA-256, source paths, and commits wrap.

Preferred CSS properties:

```css
overflow-wrap: anywhere;
word-break: break-word;
min-width: 0;
```

Apply them to metadata values, not globally.

**Acceptance criteria**

- [ ] Document cards have no horizontal overflow at compact width.
- [ ] Hashes remain selectable and readable.

## Task 10.6: Keep tables genuinely tabular

**Required**

Use tables for:

- Format-role matrices.
- Status comparison.
- Route mapping.
- Structured metadata comparisons.

Use cards or lists for:

- Document collections.
- Article summaries.
- Reader actions.
- Related routes.

**Acceptance criteria**

- [ ] Mobile layouts remain usable.
- [ ] Tables are not used as general page layout.

---

# Phase 11: Lightweight Validation and Release Readiness

## Objective

Use only the checks necessary for this migration. Avoid repetitive full-suite overhead.

## Validation principle

During implementation, run targeted checks by change type. Run the aggregate release validation once, immediately before an authorized deployment or release checkpoint.

Do not run `npm run quality` after every phase.

Do not add a large new test suite solely for this navigation migration.

## Task 11.1: Build check

**Required once after canonical pages and navigation are complete**

Run:

```bash
npm run build
```

This confirms:

- Astro page imports resolve.
- New routes compile.
- Moved files have correct relative imports.
- Static output is generated.

**Failure response**

Fix build errors before proceeding. Do not continue to provenance generation with a broken build.

## Task 11.2: Targeted navigation review

**Required, manual, minimal**

Open:

```text
/
/documents/
/documents/research/
/documents/diagrams/
```

At:

- One normal desktop viewport.
- One compact/mobile viewport.

Check only:

- Documents is visible.
- Resources is absent.
- Dropdown opens and closes.
- All five links work.
- Active state works.
- No obvious overflow exists.

No broad viewport matrix is required unless a defect appears.

## Task 11.3: Targeted redirect check

**Required**

After redirects are configured, check a representative set without following redirects automatically:

```bash
curl -I https://<preview-or-production>/resources/
curl -I https://<preview-or-production>/resources/library/
curl -I https://<preview-or-production>/resources/documents/
curl -I https://<preview-or-production>/resources/diagrams/
```

Confirm:

```text
301 status
correct Location header
one-hop destination
```

Check additional old routes only when their mappings were modified in this implementation.

## Task 11.4: Manifest validation by change type

**Required only if source, asset, or document catalog manifests change**

Run:

```bash
npm run validate:manifests
```

If the new document catalog has a lightweight structural check, include it in this command or run:

```bash
python3 scripts/validate_document_catalog.py
```

The validator should perform structural checks only. It should not become a network crawler or expensive integration suite.

## Task 11.5: Provenance validation

**Required because canonical route files and route maps change**

After final provenance regeneration, run:

```bash
npm run validate:provenance
```

Run it once after final page edits, not repeatedly during copy drafting.

## Task 11.6: Cloudflare configuration validation

**Required because redirects and headers change**

Run:

```bash
npm run validate:cloudflare
```

This is a small syntax check and is directly relevant.

## Task 11.7: Targeted existing tests only

**Conditional**

Run existing focused tests only if the related code changed:

```bash
python3 -m pytest tests/test_mobile_navigation.py -q
```

Run gallery-focused tests only if `DiagramGalleryList.astro` or gallery rendering logic changed. A route move alone does not require retesting all image policy behavior.

Do not add a separate comprehensive navigation test suite unless implementation reveals regression risk that current tests do not cover.

A single small navigation assertion may be added to the existing mobile-navigation test file:

```text
Documents exists
Resources does not exist
approved five child labels exist
```

## Task 11.8: Final aggregate validation

**Required once before deployment because repository release policy expects it**

Run:

```bash
npm run validate
```

Do not automatically run:

```bash
npm run quality
python3 -m pytest
make lint
```

unless:

- `npm run validate` requires them.
- Related Python logic changed and targeted tests were insufficient.
- A release owner explicitly requests the full quality gate.
- A failure indicates broader verification is necessary.

## Task 11.9: Deployment remains separate

**Required process boundary**

Do not deploy as part of implementation completion.

After separate deployment authorization:

1. Build the final commit.
2. Deploy through the existing Wrangler Direct Upload process.
3. Check the five canonical Documents routes.
4. Check the four representative redirects.
5. Confirm the production header has Documents and not Resources.

No exhaustive post-deployment browser campaign is required unless a defect appears.

---

# Phase 12: Cleanup and Completion

## Objective

Remove migration residue and leave one coherent architecture.

## Task 12.1: Remove compatibility names from source

**Required**

Remove temporary identifiers such as:

```text
resourcesLibrary
resourcesDocuments
resourcesDiagrams
resources-greenfield-page
```

where they no longer describe the canonical page.

Do not rename unrelated historical implementation-control records.

**Acceptance criteria**

- [ ] Current source names match Documents architecture.
- [ ] No styling dependency silently requires a Resources class.

## Task 12.2: Remove dead route data

**Required**

Remove obsolete Resources entries from:

```text
siteNavigationLinks
route-card arrays
reading-path arrays
related-route arrays
comprehension content
route map
provenance
smoke-test defaults
maintainer docs
```

**Acceptance criteria**

- [ ] No dead canonical Resources data remains.
- [ ] Redirect configuration is the only intentional current use of retired URLs.

## Task 12.3: Confirm asset integrity

**Required only for changed or newly imported assets**

Confirm:

- File exists.
- Manifest path matches.
- Bytes match.
- SHA-256 matches.
- Source reference exists.
- Approval status is explicit.

Do not recompute or touch unchanged assets solely because page routes moved.

## Task 12.4: Record migration completion

**Required**

The completion record should state:

- Baseline commit.
- Final canonical route map.
- Old route redirects.
- Navigation labels.
- Pages moved.
- Pages consolidated.
- Importer safety correction.
- Manifest changes.
- Provenance regeneration.
- Minimal checks run.
- Checks intentionally not run.
- Deployment status.

**Acceptance criteria**

- [ ] A future maintainer can reconstruct what changed.
- [ ] Skipped broad checks are recorded without implying they passed.

---

## 13. Exact Route Migration Matrix

| Old route | Final route | Content action | Redirect |
|---|---|---|---|
| `/resources/` | `/documents/` | Merge useful overview content into Documentation Overview | 301 |
| `/resources/library/` | `/documents/` | Rewrite and rename as Documentation Overview | 301 |
| `/resources/documents/` | `/documents/research/` | Move ontology TeX/PDF collection | 301 |
| `/resources/diagrams/` | `/documents/diagrams/` | Move gallery intact | 301 |
| `/resources/source-authority/` | `/documents/governance/source-authority/` | Reclassify under governance | 301 |
| `/resources/registries/` | `/documents/governance/registries/` | Reclassify under governance | 301 |
| `/resources/generated-derivatives/` | `/documents/derivatives/` | Reclassify as derivative guidance | 301 |
| `/resources/retrieval-layers/` | `/documents/governance/retrieval-layers/` | Reclassify under governance | 301 |
| `/resources/publication-process/` | `/documents/governance/publication-process/` | Reclassify under governance | 301 |
| `/resources/reading-paths/` | `/documents/reading-paths/` | Move | 301 |
| `/resources/repository-map/` | `/documents/governance/repository-map/` | Reclassify under governance | 301 |
| `/resources/site-builder-guide/` | `/documents/governance/site-builder-guide/` | Reclassify under governance | 301 |
| `/resources/guided-starts/` | `/documents/reading-paths/` | Consolidate | 301 |
| `/resources/guided-starts/general-public/` | `/documents/reading-paths/general-public/` | Move or merge | 301 |
| `/resources/reviewer-packet/` | `/documents/reviewer-packet/` | Move | 301 |
| `/documents` | `/documents/` | Canonical slash normalization | 301 |
| `/diagrams` | `/documents/diagrams/` | Update alias | 301 |
| `/equations` | `/documents/research/` | Update alias | 301 |
| `/downloads` | `/documents/` | Update alias | 301 |

---

## 14. File-by-File Change Map

### 14.1 Navigation and layout

#### `src/lib/siteContent.ts`

- Replace Resources navigation object.
- Add Documents dropdown.
- Update IA rationale.
- Update route-card labels and links.
- Rename Resources/Library data identifiers.
- Keep diagram concept data unless route-specific naming requires change.

#### `src/layouts/BaseLayout.astro`

- Prefer no logic change.
- Update only if a discovered defect prevents Documents behavior.
- Preserve accessibility and mobile disclosure.

### 14.2 Pages

#### Create

```text
src/pages/documents/index.astro
src/pages/documents/anthology/index.astro
src/pages/documents/research/index.astro
src/pages/documents/governance/index.astro
src/pages/documents/diagrams/index.astro
```

#### Create when retained

```text
src/pages/documents/governance/source-authority/index.astro
src/pages/documents/governance/registries/index.astro
src/pages/documents/governance/publication-process/index.astro
src/pages/documents/governance/retrieval-layers/index.astro
src/pages/documents/governance/repository-map/index.astro
src/pages/documents/governance/site-builder-guide/index.astro
src/pages/documents/reading-paths/index.astro
src/pages/documents/reading-paths/general-public/index.astro
src/pages/documents/reviewer-packet/index.astro
src/pages/documents/derivatives/index.astro
```

#### Remove after migration

```text
src/pages/resources/index.astro
src/pages/resources/library/index.astro
src/pages/resources/documents.astro
src/pages/resources/diagrams.astro
src/pages/resources/source-authority/index.astro
src/pages/resources/registries/index.astro
src/pages/resources/generated-derivatives/index.astro
src/pages/resources/retrieval-layers/index.astro
src/pages/resources/publication-process/index.astro
src/pages/resources/reading-paths/index.astro
src/pages/resources/repository-map/index.astro
src/pages/resources/site-builder-guide/index.astro
src/pages/resources/guided-starts/index.astro
src/pages/resources/guided-starts/general-public/index.astro
src/pages/resources/reviewer-packet/index.astro
```

Confirm exact existing paths before removal.

### 14.3 Components

#### Refactor

```text
src/components/DocumentActions.astro
```

#### Recommended additions

```text
src/components/documents/DocumentCollection.astro
src/components/documents/DocumentCard.astro
src/components/documents/DocumentActions.astro
src/components/documents/DocumentMetadata.astro
```

#### Preserve

```text
src/components/DiagramGalleryList.astro
```

### 14.4 Data and manifests

#### Update

```text
src/lib/manifests.ts
public/files/manifests/source_manifest.json
public/files/manifests/asset_manifest.json
public/files/manifests/page_route_map.json
public/files/manifests/page_provenance.json
```

#### Add

```text
public/files/manifests/document_catalog.json
```

### 14.5 Scripts

#### Update

```text
scripts/import_ontology_assets.py
scripts/validate_manifest_paths.py
scripts/validate_page_provenance.py
scripts/smoke_test_site.py
scripts/validate_cloudflare_pages_config.py
```

The Cloudflare validator may need no code change if existing syntax validation already accepts the new lines.

#### Recommended additions

```text
scripts/import_document_collection.py
scripts/validate_document_catalog.py
```

Keep both scripts small and deterministic.

### 14.6 Cloudflare and Astro

#### Update

```text
public/_redirects
public/_headers
astro.config.mjs
```

### 14.7 Styles

#### Review and change only when necessary

```text
src/styles/global.css
```

Potential additions:

- Documents body-class mappings.
- Document card layout.
- Metadata wrapping.
- Format badges.
- Category grid.

Avoid broad global style changes.

### 14.8 Tests

#### Update minimally

```text
tests/test_mobile_navigation.py
```

Add only simple Documents/Resources assertions if useful.

#### Conditional

```text
tests/test_image_loading_policy.py
```

No change required for a route-only gallery move unless source path assumptions are hard-coded.

### 14.9 Maintainer documentation

```text
README.md
AGENTS.md
docs/README.md
docs/project-features-and-functionality.md
docs/deployment/cloudflare-pages.md
```

---

## 15. Minimal Validation Matrix

| Change type | Minimum required check | Avoid unless needed |
|---|---|---|
| Markdown plan file only | None beyond opening the file | Full build, tests, provenance |
| Navigation data and Astro page moves | `npm run build` plus one desktop and one compact manual check | Full browser matrix |
| Redirect changes | Cloudflare config validator plus representative `curl -I` checks | Crawling every historical URL |
| Source/asset manifest changes | `npm run validate:manifests` | Full quality gate during each edit |
| Page route map/provenance changes | `npm run validate:provenance` once after final edits | Repeated hash regeneration |
| Ontology importer change | One targeted importer preservation check | Full Python suite unless failure suggests it |
| Gallery component logic change | Existing focused gallery test | Retesting every site page |
| Final pre-deployment state | One `npm run validate` | `npm run quality`, full pytest, lint unless required |

---

## 16. Implementation Checkpoint Strategy

Use a small number of logical checkpoints rather than one commit per micro-task.

### Checkpoint A: document foundation

Includes:

- Generic document types.
- Importer ownership fix.
- Markdown manifest kind.
- Document catalog.
- No navigation switch yet.

### Checkpoint B: canonical Documents pages

Includes:

- Documentation Overview.
- Anthology.
- Research.
- Governance.
- Diagram Gallery.
- Secondary retained routes.

### Checkpoint C: navigation and route migration

Includes:

- Documents dropdown.
- Internal-link changes.
- Redirects.
- Removal of Resources pages.

### Checkpoint D: manifests, provenance, and documentation

Includes:

- Route map.
- Page provenance.
- Maintainer docs.
- Final cleanup.

Each checkpoint should remain local until separately authorized for push. Deployment remains a later explicit action.

---

## 17. Rollback Plan

### 17.1 Navigation rollback

If the new Documents pages are incomplete:

- Restore the previous navigation object.
- Do not keep Documents links pointing to unfinished pages.
- Leave canonical Documents page work on the branch for repair.

### 17.2 Redirect rollback

If a redirect loop or wrong destination appears:

- Revert only the affected `_redirects` lines.
- Keep new pages available directly.
- Do not restore reverse `/documents -> /resources/documents/` unless the entire migration is rolled back.

### 17.3 Manifest rollback

If new document imports corrupt manifest relationships:

- Restore source and asset manifests from the last known valid commit.
- Restore imported files and catalog together.
- Do not manually delete only one side of a source/asset relationship.

### 17.4 Provenance rollback

If page provenance fails:

- Keep canonical page files.
- Regenerate provenance from the final page state.
- Do not restore stale hashes.

### 17.5 Content rollback

If category copy overstates authority:

- Remove or soften the affected claim immediately.
- Preserve document availability only when its source status remains valid.
- Escalate source-status uncertainty to a separate upstream review.

---

## 18. Risks and Mitigations

### Risk 1: Treating the work as a menu rename

**Failure:** stale routes, page titles, redirects, manifests, and provenance remain.

**Mitigation:** execute all phases through route cleanup.

### Risk 2: Deleting old routes too early

**Failure:** broken internal links and provenance failures.

**Mitigation:** create canonical destinations and redirects before deletion.

### Risk 3: Making Ontology Documents the entire Documents system

**Failure:** anthology, governance, and diagram categories cannot scale cleanly.

**Mitigation:** treat ontology as a Research Articles collection.

### Risk 4: Losing future PDF or TeX manifest rows

**Failure:** ontology importer removes unrelated collections.

**Mitigation:** fix collection ownership first.

### Risk 5: Publishing internal Markdown

**Failure:** private paths or unreviewed control material become public.

**Mitigation:** explicit allowlist, minimal deny-pattern scan, human review.

### Risk 6: Redirect loop

**Failure:** `/documents` points to Resources while Resources points to Documents.

**Mitigation:** replace reverse redirects before canonical switch.

### Risk 7: Redirect chains

**Failure:** old project route redirects to Resources, then Documents.

**Mitigation:** repoint legacy routes directly.

### Risk 8: Duplicate canonical content

**Failure:** old and new pages both return 200.

**Mitigation:** remove old page files after redirects exist.

### Risk 9: Authority flattening

**Failure:** all approved documents look equally authoritative.

**Mitigation:** role-specific labels and format guide.

### Risk 10: Excessive implementation overhead

**Failure:** migration stalls under unnecessary tests and abstractions.

**Mitigation:** static data model, targeted checks, one final aggregate validation.

### Risk 11: Empty Anthology category

**Failure:** navigation points to a page with no useful material.

**Mitigation:** publish at least one approved item or clearly label the category state. Delay the nav entry only if the owner chooses content-first exposure.

### Risk 12: Production does not match Git

**Failure:** code is merged but Direct Upload production is unchanged.

**Mitigation:** treat deployment and post-deployment check as a separately authorized phase.

---

## 19. Definition of Done

### Navigation

- [ ] Resources is absent from the primary navigation.
- [ ] Documents is present.
- [ ] Documents contains exactly five approved entries.
- [ ] Documentation Overview is first.
- [ ] Diagram Gallery is beneath Documents.
- [ ] Mobile and no-script navigation use the same canonical routes.
- [ ] Active state works on nested Documents routes.

### Documentation Overview

- [ ] `/documents/` is canonical.
- [ ] Library is no longer the page identity.
- [ ] Categories, formats, authority, provenance, status, and reading paths are explained.
- [ ] All hero and related links are canonical.

### Anthology

- [ ] `/documents/anthology/` exists.
- [ ] Every visible article has an approved PDF.
- [ ] Planned content is not presented as published.
- [ ] PDF role and provenance are explicit.

### Research

- [ ] `/documents/research/` exists.
- [ ] Existing ontology articles remain available.
- [ ] TeX/PDF pairs render as one logical document.
- [ ] Reading order is preserved.
- [ ] TeX and PDF roles remain distinct.

### Governance

- [ ] `/documents/governance/` exists.
- [ ] Approved public Markdown is allowlisted.
- [ ] Governance type, scope, status, and freshness are visible.
- [ ] Internal-only material is excluded.

### Diagrams

- [ ] `/documents/diagrams/` exists.
- [ ] Gallery inventory is preserved.
- [ ] Alt text, captions, provenance, and non-authority labels remain.
- [ ] Old gallery URL redirects directly.

### Routes

- [ ] Every old Resources route has a semantic 301 destination.
- [ ] No redirect loop exists.
- [ ] No avoidable redirect chain exists.
- [ ] Old Resources pages do not return duplicate canonical content.
- [ ] Internal links do not depend on redirects.

### Data

- [ ] Ontology importer preserves unrelated document records.
- [ ] Markdown is a first-class manifest kind.
- [ ] Logical documents can group multiple formats.
- [ ] Existing asset URLs are preserved unless deliberately changed.
- [ ] New files have valid source references, bytes, and hashes.

### Provenance

- [ ] Route map contains canonical Documents routes.
- [ ] Page provenance hashes match final page files.
- [ ] Retired Resources routes are not canonical provenance pages.
- [ ] No private local path is exposed.

### Documentation

- [ ] README is current.
- [ ] AGENTS.md is current.
- [ ] Project feature map is current.
- [ ] Deployment examples use canonical routes.
- [ ] This plan is indexed in maintainer docs.

### Minimal verification

- [ ] `npm run build` passes.
- [ ] Representative desktop and compact navigation checks pass.
- [ ] Representative old routes return correct 301 locations.
- [ ] Manifest validation passes if manifests changed.
- [ ] Provenance validation passes.
- [ ] Cloudflare configuration validation passes.
- [ ] One final `npm run validate` passes before authorized deployment.
- [ ] Any intentionally skipped broad checks are named.

### Release boundary

- [ ] Commit and push status are recorded.
- [ ] Deployment status is recorded.
- [ ] No deployment is implied unless explicitly performed.
- [ ] Production verification is performed only after deployment authorization.

---

## 20. Recommended Final Public Structure

```text
/
├── physics/
├── ai-research-system/
└── documents/
    ├── index.astro                         Documentation Overview
    ├── anthology/
    │   └── index.astro                     Anthology Articles
    ├── research/
    │   ├── index.astro                     Research Articles
    │   └── ontology/                       Optional collection detail
    ├── governance/
    │   ├── index.astro                     Governance & Control
    │   ├── source-authority/
    │   ├── registries/
    │   ├── publication-process/
    │   ├── retrieval-layers/
    │   ├── repository-map/
    │   └── site-builder-guide/
    ├── diagrams/
    │   └── index.astro                     Diagram Gallery
    ├── reading-paths/
    │   ├── index.astro
    │   └── general-public/
    ├── reviewer-packet/
    └── derivatives/
```

Public assets remain separately organized:

```text
/files/pdf/ontology/
/files/tex/ontology/
/files/pdf/anthology/
/files/pdf/research/<collection>/
/files/tex/research/<collection>/
/files/markdown/governance/
/assets/diagrams/
```

Public manifests remain:

```text
/files/manifests/source_manifest.json
/files/manifests/asset_manifest.json
/files/manifests/document_catalog.json
/files/manifests/page_route_map.json
/files/manifests/page_provenance.json
```

---

## 21. Final Implementation Order

Execute in this exact order:

1. [ ] Re-check current `main`.
2. [ ] Freeze route and naming decisions.
3. [ ] Fix ontology importer ownership.
4. [ ] Add Markdown manifest kind.
5. [ ] Add generic document types and logical catalog.
6. [ ] Build Documentation Overview.
7. [ ] Build Anthology Articles.
8. [ ] Move Ontology Documents to Research Articles.
9. [ ] Build Governance & Control.
10. [ ] Move and preserve Diagram Gallery.
11. [ ] Move or consolidate secondary Resources pages.
12. [ ] Replace Resources navigation with Documents.
13. [ ] Update internal links and public labels.
14. [ ] Replace reverse redirects.
15. [ ] Add explicit Resources redirects.
16. [ ] Repoint older project redirects directly.
17. [ ] Remove old Resources page sources.
18. [ ] Update required routes.
19. [ ] Update page route map.
20. [ ] Regenerate page provenance.
21. [ ] Update README, AGENTS, project map, and deployment docs.
22. [ ] Run one build.
23. [ ] Perform one desktop and one compact navigation check.
24. [ ] Perform representative redirect checks.
25. [ ] Run only relevant manifest, provenance, and Cloudflare validators.
26. [ ] Run one final `npm run validate` before authorized release.
27. [ ] Record completion and skipped broad checks.
28. [ ] Stop before push or deployment unless separately authorized.

---

## 22. Final Architectural Decision

The final system is a **Documents architecture**, not a renamed Resources menu.

The core design decisions are:

1. **Documentation Overview** is the documentation front door.
2. **Anthology Articles** is a PDF-oriented reader publication category.
3. **Research Articles** groups TeX and PDF manifestations of logical research documents.
4. **Governance & Control** exposes approved Markdown within explicit scope and freshness boundaries.
5. **Diagram Gallery** remains a manifest-backed explanatory visual collection.
6. Former Resources pages become contextual Documents pages, consolidated pages, or redirects.
7. Existing document assets retain stable URLs during the route migration.
8. Source authority remains upstream and format-specific.
9. Route manifests and provenance are updated only after canonical files are final.
10. Verification remains intentionally lean and directly related to changed surfaces.

This produces a cleaner reader journey, a scalable document model, safer import behavior, and a smaller navigation surface without weakening the project's provenance or source-authority discipline.
