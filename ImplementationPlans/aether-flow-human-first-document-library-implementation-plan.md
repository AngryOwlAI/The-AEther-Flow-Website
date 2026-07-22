# Human-First Document Library and Ontology Access Implementation Plan

**Project:** The AEther Flow Website  
**Repository:** `AngryOwlAI/The-AEther-Flow-Website`  
**Production site:** `https://the-aether-flow-website.pages.dev/`  
**Plan status:** Proposed implementation plan  
**Plan date:** 2026-07-22  
**Prepared against:** The `main` branch as inspected on 2026-07-22  
**Suggested repository location:** `ImplementationPlans/aether-flow-human-first-document-library-implementation-plan.md`  
**Primary implementation area:** `/documents/`, especially `/documents/research/` and `/documents/anthology/`  
**Implementation authorization:** This document is a plan only. It does not authorize a commit, push, deployment, upstream-source mutation, scientific-claim change, or publication of previously unapproved material.

---

## 1. Executive Summary

The current Documents architecture has a strong technical foundation. It preserves canonical ontology ordering, stable PDF and TeX URLs, source-versus-derivative roles, status fields, provenance, source commits, hashes, and manifest-backed publication. Those capabilities should remain.

The central usability problem is presentation order. The current research collection asks a human reader to encounter repository and provenance concepts before the scientific subject has been explained. Terms such as exact closure, canonical front door, manifestation, authority scope, readable derivative, claim boundary, ontology promotion, SHA-256, source path, and import date receive substantial visible space. The result is technically precise but cognitively expensive.

This plan adds a human interpretation layer above the existing source and machine layers. The intended reading order becomes:

1. Explain what the collection is.
2. Explain what exact closure means.
3. State what is fixed, what is interpretive, and what remains open.
4. Show which paper to read first.
5. Explain what each paper answers.
6. Provide direct, descriptive PDF and TeX actions.
7. Offer individual HTML guide pages.
8. Move file verification and provenance into an optional technical disclosure.
9. Preserve structured metadata for agents through manifests, semantic HTML, JSON, and alternate-format links.

The implementation does not remove technical rigor. It changes the order in which rigor is presented.

The plan also makes TeX access truthful. The currently published root `.tex` files may reference shared inputs. A root file must not be described as a complete compilable package unless all required dependencies are included and compilation has been confirmed. The final experience should provide both direct root manuscript access and, where feasible, complete source archives.

Testing and validation are intentionally lean. This plan does not create a broad new test suite, a large browser matrix, recurring usability studies, or mandatory Playwright infrastructure. It uses existing build and manifest checks sparingly, adds low-cost build-time data assertions, performs one small manual comprehension check, and runs the repository aggregate validation only once before an authorized release.

---

## 2. Product Problem

### 2.1 Current reader problem

A first-time human reader must presently infer too much:

- What the ontology collection is.
- What exact closure means.
- Why the overview is the first paper.
- Whether exact closure means the deeper physics is fully derived.
- Whether the project is proposing new observer-level dynamics beyond general relativity.
- Why there are both an overview and a flagship article.
- Whether a PDF or TeX file is the appropriate format.
- Whether a TeX file can compile by itself.
- Why hashes, source paths, and commit identifiers are visible.
- Whether `approved` means published, internally reviewed, scientifically proven, or externally accepted.
- Which action opens a particular document when several buttons share generic wording.

The existing page gives machines and technical reviewers useful identifiers, but it makes human readers reconstruct the conceptual story from compact metadata.

### 2.2 Target outcome

A new reader should be able to answer the following without opening a raw source file:

- What is this collection?
- What does exact closure mean here?
- What does the project currently claim?
- What does it explicitly not claim?
- Which paper should I read first?
- What question does each paper answer?
- How do I read the PDF?
- How do I inspect or download the TeX?
- Is the TeX download a root source file or a complete package?
- Where are the technical provenance details if I need them?

A technical reviewer or agent should still be able to answer:

- What is the logical document ID?
- What is the canonical order?
- Which file is the registered source?
- Which file is the readable derivative?
- What are the asset paths, hashes, revisions, dates, and status values?
- What machine-readable endpoint describes the collection?
- Which page and asset records are authoritative for which type of statement?

---

## 3. Human-First and Agent-Friendly Design Contract

### 3.1 Human-first presentation

A human-first research website presents information in this order:

1. Subject and purpose.
2. Plain-language context.
3. Essential definitions.
4. Reader question.
5. Recommended next action.
6. Scientific scope and limits.
7. File formats and downloads.
8. Optional technical verification.

Human-facing copy should prefer:

- Familiar words before internal terminology.
- Short conceptual sections rather than dense metadata grids.
- Questions that match reader intent.
- Definitions near first use.
- Explanations of why an action matters.
- Narrative sequence rather than bare ordinal values.
- Humanized file sizes and dates.
- Explicit distinctions between publication state and scientific status.
- Progressive disclosure for specialist information.

### 3.2 Agent-friendly publication

Agent-friendly publication should provide:

- Stable document IDs.
- Stable routes and asset URLs.
- Canonical sequence numbers.
- Exact role and status values.
- Source and derivative relationships.
- Direct PDF and TeX paths.
- Hashes, commits, paths, and dates.
- Semantic headings and lists.
- Structured JSON.
- JSON-LD or equivalent structured metadata.
- Alternate-format links.
- Clear authority boundaries.

These capabilities belong in machine-readable surfaces and semantic markup. They do not require raw metadata to dominate the default visual experience.

### 3.3 Shared truth, separate presentation layers

The implementation shall preserve four layers:

| Layer | Primary users | Responsibility |
|---|---|---|
| Registered source layer | Researchers, maintainers, reviewers | Owns scientific source identity, scoped claims, and registered status |
| Machine publication layer | Agents, validators, technical reviewers | Exposes exact identifiers, paths, roles, hashes, relationships, and revisions |
| Human interpretation layer | General readers, students, researchers, reviewers | Explains concepts, sequence, purpose, limits, and actions |
| Raw asset layer | All users when needed | Provides direct PDF, TeX, source-package, image, and manifest access |

No layer may silently promote itself above the source authority recorded upstream.

### 3.4 No Human/AI mode toggle

The website shall not add a visible Human/AI toggle.

Reasons:

- It would create two interface states to maintain.
- Humans should not have to opt into understandable language.
- Agents can parse semantic HTML and structured endpoints without a special visual mode.
- One source of truth with progressive disclosure is easier to maintain than parallel sites.

---

## 4. Source-Authority and Claim Boundary

The following boundaries are mandatory:

- Registered TeX retains its existing scoped research-source role.
- PDF remains a readable fixed-layout derivative unless the upstream registry says otherwise.
- Human HTML guides are reader-facing explanations and do not become scientific source authority.
- Reader summaries must be traceable to registered source content.
- A website publication state such as `approved` must not be presented as proof, peer review, external acceptance, or empirical confirmation.
- Hashes establish artifact identity, not correctness.
- A successful build or validator pass establishes repository consistency, not scientific truth.
- The exact-closure explanation must preserve the distinction between adoption and first-principles derivation.
- The website must not claim a distinct verified low-energy gravitational sector beyond GR when the registered source does not.
- The website must not claim that the deeper substrate derivation has been completed when it remains open.
- Website copy may simplify terminology, but it must not remove material qualifications or strengthen claims.
- Existing stable ontology PDF and TeX asset URLs must remain available.

---

## 5. Goals

### 5.1 Primary goals

- [ ] Make all ontology PDFs directly and descriptively accessible to human readers.
- [ ] Make TeX access equally discoverable and truthful about package completeness.
- [ ] Define exact closure before asking readers to navigate by that term.
- [ ] Explain what is fixed, what is interpretive, and what remains open.
- [ ] Identify the Exact Closure Sequence Overview as the clear starting document.
- [ ] Replace generic artifact-role action labels with document-specific human labels.
- [ ] Present all eight ontology papers as one understandable reading journey.
- [ ] Add a human HTML guide page for every ontology paper.
- [ ] Move hashes, paths, commits, exact bytes, and import details behind progressive disclosure.
- [ ] Preserve all existing technical metadata and machine-readable access.
- [ ] Reframe the Documents overview around reader tasks rather than formats and manifests.
- [ ] Make the empty anthology state immediately honest and useful.
- [ ] Provide collection-level PDF and TeX downloads where source completeness permits.
- [ ] Keep implementation and validation overhead proportional.

### 5.2 Secondary goals

- [ ] Use consistent glossary definitions across the site.
- [ ] Distinguish website publication status from scientific claim status.
- [ ] Use humanized file sizes and dates in visible copy.
- [ ] Keep direct technical records available through secondary actions.
- [ ] Improve screen-reader link purpose and keyboard navigation.
- [ ] Improve mobile and zoom behavior by removing the persistent metadata side rail.
- [ ] Provide agents with a collection JSON endpoint and structured page metadata.
- [ ] Document source-package limitations instead of hiding them.
- [ ] Reuse the existing Astro architecture and avoid new runtime dependencies.

---

## 6. Non-Goals

The following work is outside this plan unless separately authorized:

- [ ] Do not rewrite upstream ontology manuscripts.
- [ ] Do not change scientific equations, mathematical derivations, citations, or registry status.
- [ ] Do not present website summaries as new research sources.
- [ ] Do not add a CMS, database, search service, personalization service, or external indexing dependency.
- [ ] Do not move existing PDF or TeX files solely to match new page routes.
- [ ] Do not remove technical manifests.
- [ ] Do not create a second AI-only visual interface.
- [ ] Do not require a complete redesign of unrelated physics, AI-system, governance, or diagram pages.
- [ ] Do not add a large automated test suite.
- [ ] Do not add a mandatory Playwright or Axe dependency as part of the initial implementation.
- [ ] Do not run `npm run quality` after every task.
- [ ] Do not run the full repository validation after every phase.
- [ ] Do not claim PDF/UA, WCAG conformance, or TeX reproducibility without evidence.
- [ ] Do not automatically deploy when implementation is complete.
- [ ] Do not delete compatibility routes or assets that remain in active use.
- [ ] Do not publish unapproved anthology content to avoid an empty state.

---

## 7. Current Repository Context

### 7.1 Framework and build

- Astro static site.
- TypeScript and Astro components.
- Static public assets under `public/`.
- Document records loaded from `public/files/manifests/document_catalog.json`.
- Asset and source metadata loaded from public manifests.
- Existing KaTeX support.
- Existing Playwright dependency, but no new browser suite is required by this plan.
- Existing build command: `npm run build`.
- Existing targeted manifest validation: `npm run validate:manifests`.
- Existing aggregate validation: `npm run validate`.

### 7.2 Relevant existing routes

```text
/documents/
/documents/anthology/
/documents/research/
/documents/governance/
/documents/diagrams/
/physics/ontology/
/physics/exact-gr-benchmark/
/physics/claim-status/
```

### 7.3 Relevant existing files

```text
src/pages/documents/index.astro
src/pages/documents/anthology/index.astro
src/pages/documents/research/index.astro
src/pages/physics/ontology/index.astro
src/components/documents/DocumentCollection.astro
src/components/documents/DocumentCard.astro
src/components/documents/DocumentActions.astro
src/components/documents/DocumentMetadata.astro
src/components/StatusDossier.astro
src/components/ComprehensionBlocks.astro
src/lib/documents.ts
src/lib/manifests.ts
src/lib/siteContent.ts
src/styles/global.css
public/files/manifests/document_catalog.json
public/files/manifests/source_manifest.json
public/files/manifests/asset_manifest.json
public/files/manifests/page_route_map.json
public/files/manifests/page_provenance.json
scripts/import_ontology_assets.py
scripts/validate_document_catalog.py
scripts/validate_manifest_paths.py
scripts/validate_page_provenance.py
scripts/quality_gate.py
package.json
```

### 7.4 Existing strengths to preserve

- Eight-document canonical order.
- Paired TeX and PDF records.
- Stable asset paths.
- Manifest-backed approval.
- Source-versus-derivative distinction.
- Internal-first reader routes.
- Semantic lists and definition lists.
- Skip link and keyboard-aware navigation.
- Clear separation between website presentation and source authority.
- Existing ontology comprehension content that can inform glossary wording.

### 7.5 Current problems to correct

- Research-page introduction describes publication mechanics before the physics subject.
- Exact closure is used before it is adequately defined.
- Reading guidance relies on internal terminology.
- PDF actions are generic and role-oriented.
- TeX action wording can imply more package completeness than exists.
- Technical metadata receives equal visual weight to the paper explanation.
- Hashes and exact bytes are visible before a reader asks for verification.
- Summaries are compact catalog descriptions rather than reader explanations.
- The first paper is not sufficiently distinguished from the remaining collection.
- The anthology route is mostly a policy explanation when no anthology items exist.
- The Documents overview prioritizes formats, authority, and manifest concepts over reader intentions.
- The existing comprehension capability is not applied to the document collection.
- The current TeX root files may reference shared inputs that are not included in individual downloads.

---

## 8. Adopted Product Decisions

### 8.1 Canonical routes remain unchanged

The canonical route family remains `/documents/`.

This avoids unnecessary redirect work and preserves existing links. Human-facing labels may change without changing the URL architecture.

### 8.2 Public navigation label

The recommended public top-level label is:

```text
Library
```

The canonical URL remains `/documents/`.

Recommended dropdown:

| Order | Public label | Route | Human purpose |
|---:|---|---|---|
| 1 | Start Here | `/documents/` | Choose a path based on what the reader wants to understand |
| 2 | Ontology Papers | `/documents/research/` | Access all eight ontology papers in PDF and TeX |
| 3 | Plain-Language Articles | `/documents/anthology/` | Read approved exposition and anthology publications |
| 4 | Diagrams | `/documents/diagrams/` | Browse visual explanations |
| 5 | Source & Governance | `/documents/governance/` | Inspect provenance, process, source authority, and operational records |

If project governance requires retaining `Documents` as the top-level label, keep the same dropdown labels and page changes. Route behavior and human-first page structure remain the same. The implementation task must record which label was adopted.

### 8.3 Research page public identity

Recommended visible identity:

```text
AEther Flow Ontology Papers
```

Recommended breadcrumb:

```text
Library / Ontology Papers
```

The route remains `/documents/research/`.

### 8.4 Anthology public identity

Recommended visible identity:

```text
Plain-Language Articles
```

The route remains `/documents/anthology/`.

While empty, it must say so immediately and route readers to the populated ontology collection.

### 8.5 Source and technical labels

Preferred human terms:

| Internal or technical term | Human-facing default |
|---|---|
| manifestation | format or file version |
| readable derivative | PDF reading copy generated from the TeX source |
| authoritative source | registered TeX manuscript |
| authority scope | source role or scientific scope |
| canonical front door | recommended starting paper |
| claim boundary | what the source supports and does not support |
| ontology promotion | ontology status |
| website import | website copy synchronized |
| bytes | humanized size, with exact bytes in technical details |
| SHA-256 | file verification code |
| source commit | source revision |
| collection slug | collection name |

### 8.6 Metadata disclosure

Visible by default:

- Paper number.
- Reader role.
- Human question.
- Formal title.
- Plain summary.
- What the reader will learn.
- PDF action.
- TeX or source-package action.
- Approximate humanized file size.
- A concise publication/source note where necessary.

Collapsed by default:

- Raw status vocabulary.
- Authority scope value.
- Exact bytes.
- Source path.
- Source commit.
- Import date.
- Full SHA-256.
- Role codes.
- Machine identifiers.
- Manifest links.

### 8.7 TeX truthfulness

Use the following labels:

- `View registered root TeX manuscript` when only the root file is published.
- `Download TeX source package` when dependencies are bundled but compilation has not been confirmed.
- `Download compilable TeX source package` only after a compile check has succeeded.
- `Download complete ontology TeX collection` only when the collection archive includes all declared shared dependencies and a README.

### 8.8 No primary JSON action

`Inspect catalog JSON` and similar actions remain available in a technical records area. They must not be the primary call to action on a human collection page.

### 8.9 One collection, multiple access levels

Every document should expose:

1. Human HTML guide.
2. PDF reading copy.
3. TeX root manuscript.
4. Complete source package when available.
5. Technical provenance.
6. Machine-readable record.

---

## 9. Target Page Architecture

### 9.1 `/documents/`

Recommended order:

1. Human hero.
2. Reader-intention cards.
3. Current available collections.
4. Brief format explanation.
5. Brief source and status explanation.
6. Reading paths.
7. Technical records.

### 9.2 `/documents/research/`

Recommended order:

1. Hero and direct start action.
2. Key information summary.
3. What exact closure means.
4. What is fixed, interpretive, and open.
5. Adoption versus derivation.
6. Featured start-here paper.
7. Collection downloads.
8. Narrative eight-paper reading path.
9. Full document cards.
10. Glossary and format help.
11. Technical records.

### 9.3 `/documents/research/[slug]/`

Recommended order:

1. Breadcrumb and sequence position.
2. Human display title and formal source title.
3. Plain summary.
4. Why read this paper.
5. What the reader will learn.
6. What the paper establishes.
7. What it does not establish.
8. Key terms.
9. Selected equations when useful.
10. Read/download actions.
11. Previous, collection, and next navigation.
12. Technical provenance disclosure.

### 9.4 `/documents/anthology/`

When empty:

1. Immediate empty-state truth.
2. Explanation of what will appear here.
3. Direct route to ontology papers.
4. Direct route to ontology orientation.
5. Optional collapsed publication-policy explanation.

When populated:

1. Plain-language collection introduction.
2. Audience and purpose.
3. Article cards.
4. Related research papers.
5. Optional technical provenance.

---

## 10. Presentation Data Architecture

### 10.1 Keep the document catalog technical and small

Do not overload `document_catalog.json` with long reader copy. It should continue to provide logical identity, formal title, category, collection, compact summary, status, authority scope, order, manifestations, and related routes.

### 10.2 Add a separate presentation model

Recommended files:

```text
src/lib/documentPresentation.ts
src/data/documentReaderProfiles.ts
src/data/documentGlossary.ts
src/data/documentCollectionPresentation.ts
```

This avoids a new content framework and uses the repository's existing TypeScript build for low-cost validation.

### 10.3 Reader profile type

```ts
export interface DocumentReaderProfile {
  documentId: string;
  displayTitle: string;
  shortTitle: string;
  formalTitle: string;
  readerQuestion: string;
  oneSentenceSummary: string;
  overview: readonly string[];
  whyRead: string;
  whatYouWillLearn: readonly string[];
  establishes: readonly string[];
  doesNotEstablish: readonly string[];
  audience: readonly ReaderAudience[];
  level: "orientation" | "intermediate" | "specialist";
  sequenceRole: string;
  startHere?: boolean;
  glossaryTerms: readonly string[];
  sourceBasis: readonly string[];
  actions: {
    pdfReadLabel: string;
    pdfDownloadLabel: string;
    texRootLabel: string;
    sourcePackageLabel?: string;
  };
  texPackaging: {
    mode: "root-only" | "source-package" | "compile-validated-package";
    explanation: string;
  };
  presentationReview: {
    status: "draft" | "reviewed";
    reviewedBy?: string;
    reviewedAt?: string;
  };
}
```

### 10.4 Build-time assertions

`documentPresentation.ts` should perform small synchronous assertions when imported during build:

- Every approved canonical ontology document has exactly one reader profile.
- No reader profile references an unknown document ID.
- Formal titles match the catalog.
- One and only one profile is marked `startHere`.
- The start-here profile is reading order 1.
- Required human fields are nonempty.
- Every referenced glossary term exists.
- TeX packaging mode and label agree.
- No profile claims a compile-validated package when no package path exists.
- No duplicate display slugs exist.

These assertions replace the need for a separate validator or test suite.

### 10.5 Glossary type

```ts
export interface DocumentGlossaryEntry {
  id: string;
  term: string;
  shortDefinition: string;
  expandedDefinition?: string;
  boundary?: string;
  relatedRoutes?: readonly string[];
  sourceBasis: readonly string[];
}
```

Required initial terms:

- ontology
- effective theory
- exact closure
- adoption
- derivation
- substrate
- benchmark
- claim boundary
- general relativity
- TeX
- PDF reading copy
- source package
- source revision
- SHA-256

---

## 11. Component Architecture

Recommended additions:

```text
src/components/documents/ReaderDocumentCard.astro
src/components/documents/DocumentFormatActions.astro
src/components/documents/TechnicalProvenanceDisclosure.astro
src/components/documents/DocumentSequence.astro
src/components/documents/ReaderSummaryBox.astro
src/components/documents/ClaimBoundaryList.astro
src/components/documents/CollectionDownloadPanel.astro
src/components/documents/DocumentGuideNavigation.astro
src/components/documents/DocumentStructuredData.astro
src/layouts/DocumentGuideLayout.astro
```

Recommended reuse:

- Keep `DocumentCollection.astro` where it remains useful, or make it a thin renderer over the new card.
- Reuse `DocumentMetadata.astro` logic inside the technical disclosure.
- Reuse `StatusDossier.astro` for exact technical metadata.
- Reuse existing button/link classes where visually appropriate.
- Reuse KaTeX and existing math styles.
- Reuse ontology terms and boundaries already established on the ontology page.

---

## 12. Requirement Traceability Matrix

| Requirement ID | Requirement | Main tasks |
|---|---|---|
| REQ-001 | Explain the collection before provenance mechanics | HFDOC-030, HFDOC-050 |
| REQ-002 | Define exact closure near first use | HFDOC-012, HFDOC-031 |
| REQ-003 | State what is fixed, interpretive, and open | HFDOC-012, HFDOC-031 |
| REQ-004 | Distinguish adoption from derivation | HFDOC-012, HFDOC-031 |
| REQ-005 | Make the overview the clear starting paper | HFDOC-032, HFDOC-041 |
| REQ-006 | Explain all eight papers as reader questions | HFDOC-013, HFDOC-033 |
| REQ-007 | Provide title-specific PDF actions | HFDOC-021, HFDOC-034 |
| REQ-008 | Make TeX access truthful and visible | HFDOC-021, HFDOC-060, HFDOC-062, HFDOC-063 |
| REQ-009 | Hide raw technical metadata by default | HFDOC-022, HFDOC-025 |
| REQ-010 | Explain SHA-256 and file verification | HFDOC-014, HFDOC-022 |
| REQ-011 | Humanize sizes and dates | HFDOC-022 |
| REQ-012 | Separate publication status from scientific scope | HFDOC-014, HFDOC-024 |
| REQ-013 | Add one HTML guide per paper | HFDOC-040 through HFDOC-045 |
| REQ-014 | Add previous and next collection navigation | HFDOC-045 |
| REQ-015 | Add selected equation explanations where useful | HFDOC-044 |
| REQ-016 | Reframe the library overview by reader intention | HFDOC-050 |
| REQ-017 | Reframe navigation labels for humans | HFDOC-002, HFDOC-051 |
| REQ-018 | Make empty anthology state honest and useful | HFDOC-052 |
| REQ-019 | Provide all-PDF collection download | HFDOC-061, HFDOC-065 |
| REQ-020 | Provide complete TeX source collection when feasible | HFDOC-060, HFDOC-062, HFDOC-064 |
| REQ-021 | Provide per-paper source packages when feasible | HFDOC-063 |
| REQ-022 | Preserve stable raw asset URLs | HFDOC-001, HFDOC-064 |
| REQ-023 | Preserve manifests and exact machine metadata | HFDOC-001, HFDOC-074 |
| REQ-024 | Add collection JSON | HFDOC-070 |
| REQ-025 | Add structured metadata and alternate formats | HFDOC-071 |
| REQ-026 | Use semantic HTML for agent and accessibility support | HFDOC-072, HFDOC-080 |
| REQ-027 | Add concise agent orientation without new authority | HFDOC-073 |
| REQ-028 | Avoid a Human/AI toggle | HFDOC-001, HFDOC-074 |
| REQ-029 | Preserve source-authority boundaries | All phases, especially HFDOC-001 and HFDOC-014 |
| REQ-030 | Improve link purpose for screen readers | HFDOC-021, HFDOC-080 |
| REQ-031 | Improve mobile, zoom, and reflow behavior | HFDOC-025, HFDOC-083 |
| REQ-032 | Keep definitions available without hover-only UI | HFDOC-011, HFDOC-081 |
| REQ-033 | Provide HTML orientation when PDFs are difficult | HFDOC-040 through HFDOC-045, HFDOC-082 |
| REQ-034 | Record PDF accessibility limitations without overclaiming | HFDOC-082 |
| REQ-035 | Keep validation light | HFDOC-003, HFDOC-090 through HFDOC-092 |
| REQ-036 | Perform one small human comprehension review | HFDOC-084 |
| REQ-037 | Avoid new runtime dependencies | HFDOC-001, HFDOC-010, HFDOC-070 |
| REQ-038 | Keep technical JSON actions secondary | HFDOC-036, HFDOC-050 |
| REQ-039 | Preserve article and collection status truth | HFDOC-014, HFDOC-052 |
| REQ-040 | Provide reversible rollout | HFDOC-093 |

---

## 13. Phase Sequence and Dependencies

```text
Phase 0  Contract and baseline
   ↓
Phase 1  Human presentation data
   ↓
Phase 2  Shared reader components
   ↓
Phase 3  Research collection page
   ↓
Phase 4  Individual paper guide pages
   ↓
Phase 5  Library overview, navigation, anthology
   ↓
Phase 6  PDF and TeX download packages
   ↓
Phase 7  Structured agent access
   ↓
Phase 8  Accessibility and human comprehension pass
   ↓
Phase 9  Minimal release verification and handoff
```

Phases 6 and 7 can begin after the presentation data model is stable, but should not be published before the human labels accurately describe package status.

---

# Phase 0: Establish the Human-First Implementation Contract

## Objective

Record the live starting state, freeze authority and product decisions, and prevent validation scope from expanding during implementation.

## Task HFDOC-000: Record the live baseline and implementation scope

**Goal**

Capture the exact repository state that will be modified and confirm that the work is limited to the human-first document-library program.

**Context**

The previous Documents navigation plan has already been implemented. This new plan changes presentation and reader access while preserving canonical routes and authority boundaries.

**Dependencies**

None.

**Likely files**

- `ImplementationPlans/aether-flow-human-first-document-library-implementation-plan.md`
- `implementation_control/ or the repository's current task-control records`
- `git status and current branch metadata`

**Implementation steps**

1. Record the current branch and full starting commit before editing.
2. Inspect the live versions of all files named in Section 7.3 because `main` may have advanced since this plan was written.
3. Record any unrelated uncommitted or plan-controlled changes.
4. Confirm whether implementation will use the existing main checkout, a branch, or another authorized workflow.
5. Confirm that no upstream research repository files will be edited as part of this website plan.
6. Record whether commit, push, and deployment are authorized separately. Default to not authorized.

**Constraints**

- Do not overwrite unrelated work.
- Do not treat this plan itself as permission to deploy.
- Do not assume the inspected July 22 state is still current.

**Acceptance criteria**

- [ ] The actual starting commit is recorded.
- [ ] Any divergence from the inspected state is summarized.
- [ ] Unrelated modified files are identified and protected.
- [ ] Release permissions are recorded separately.

**Required validation**

No test command. This is a read-only baseline task.

**Done when**

The implementation record names the exact starting state, working scope, and external-effect permissions.

## Task HFDOC-001: Adopt the human-first and source-authority contracts

**Goal**

Make the shared product rules explicit before code or copy changes begin.

**Context**

The human layer must become easier to understand without weakening the registered TeX, PDF derivative, manifest, or claim-status boundaries.

**Dependencies**

HFDOC-000.

**Likely files**

- `AGENTS.md`
- `SOUL.md`
- `ImplementationPlans/aether-flow-human-first-document-library-implementation-plan.md`
- `optional implementation task record`

**Implementation steps**

1. Record the four-layer model: registered source, machine publication, human interpretation, and raw assets.
2. Record that human explanations may simplify language but may not strengthen a scientific claim.
3. Record that registered TeX remains the source-inspection artifact and PDF remains the reading copy unless upstream metadata says otherwise.
4. Record that hashes and validation establish artifact identity or repository consistency, not scientific correctness.
5. Record that the project will use one semantic site with progressive disclosure, not a Human/AI toggle.
6. Record that existing PDF and TeX URLs remain stable.

**Constraints**

- No new source authority is created by this plan.
- No page, bundle, JSON endpoint, or HTML guide may be described as canonical scientific authority unless the upstream source says so.
- No asset is removed simply because the visible page changes.

**Acceptance criteria**

- [ ] The implementation record contains the human-first and authority contracts.
- [ ] Every later task can refer to one shared authority statement.
- [ ] The no-toggle decision is explicit.
- [ ] Stable asset URL preservation is explicit.

**Required validation**

No test command. Review the recorded contract against `AGENTS.md` and this plan.

**Done when**

The implementation team has one unambiguous authority and audience model.

## Task HFDOC-002: Freeze public naming and navigation decisions

**Goal**

Choose the final human-facing labels before building components and page copy.

**Context**

Canonical route paths can remain stable while visible labels become clearer. The recommended top-level label is Library, but project governance may choose to retain Documents.

**Dependencies**

HFDOC-001.

**Likely files**

- `src/lib/siteContent.ts`
- `src/pages/documents/index.astro`
- `src/pages/documents/research/index.astro`
- `src/pages/documents/anthology/index.astro`

**Implementation steps**

1. Adopt either `Library` or retain `Documents` as the top-level label. Record the decision once.
2. Adopt `Start Here`, `Ontology Papers`, `Plain-Language Articles`, `Diagrams`, and `Source & Governance` as dropdown labels unless a narrowly justified copy revision is recorded.
3. Adopt `AEther Flow Ontology Papers` as the research collection page title.
4. Adopt `Plain-Language Articles` as the anthology page title.
5. Adopt `Library / Ontology Papers` or the equivalent selected top-level label in breadcrumbs and eyebrows.
6. Keep `/documents/` canonical regardless of visible label.
7. Do not create redirects for label-only changes.

**Constraints**

- Do not change the route namespace.
- Do not use raw collection slugs as public labels.
- Do not use `manifestation` as ordinary reader language.

**Acceptance criteria**

- [ ] One naming set is recorded.
- [ ] Navigation, page titles, breadcrumbs, link labels, and ARIA labels use the same naming set.
- [ ] Canonical `/documents/.../` routes remain unchanged.

**Required validation**

No test command. Perform a copy-only review of the adopted naming table.

**Done when**

All later page and component work can use fixed public labels without reopening information architecture.

## Task HFDOC-003: Adopt the lean validation budget

**Goal**

Prevent the human-first implementation from accumulating unnecessary test and validation overhead.

**Context**

The repository already has broad validation commands. This plan needs only a small number of grouped checks.

**Dependencies**

HFDOC-000.

**Likely files**

- `package.json`
- `ImplementationPlans/aether-flow-human-first-document-library-implementation-plan.md`
- `implementation task record`

**Implementation steps**

1. Adopt four validation levels: V0 no command, V1 grouped build, V2 targeted manifest validation, and V3 one final aggregate repository validation.
2. Do not add a new unit-test suite for presentation data.
3. Use TypeScript/build-time assertions instead of a separate profile validator.
4. Do not add mandatory Playwright or Axe checks in the initial release.
5. Do not run `npm run quality` after every phase.
6. Schedule Checkpoint A after the core page and component work: one `npm run build`.
7. Schedule Checkpoint B after bundles and machine endpoints: one `npm run validate:manifests` followed by one `npm run build`.
8. Schedule one `npm run validate` only before an authorized release or when required by the repository definition of done.
9. Use one short manual route and comprehension review instead of a large usability study.

**Constraints**

- Validation may be increased only when an actual failure or risky change requires it.
- Do not claim any command passed until it was run.
- Skipped aggregate checks must be named in the handoff.

**Acceptance criteria**

- [ ] The implementation record contains the validation budget.
- [ ] Every task in this plan names either V0, a grouped checkpoint, or a narrowly necessary targeted check.
- [ ] No new recurring test infrastructure is required.

**Required validation**

No command. This task defines when later commands are allowed.

**Done when**

Validation scope is fixed and proportional before implementation begins.

# Phase 1: Create the Human Presentation Data Layer

## Objective

Add reviewed human explanations without bloating or weakening the technical document catalog.

## Task HFDOC-010: Create presentation types and document-profile joining logic

**Goal**

Create a small TypeScript layer that joins technical document records with human reader profiles.

**Context**

The existing document catalog should remain technical. Human summaries, questions, learning outcomes, and nonclaims belong in a separate presentation model.

**Dependencies**

HFDOC-001 through HFDOC-003.

**Likely files**

- `src/lib/documentPresentation.ts`
- `src/data/documentReaderProfiles.ts`
- `src/data/documentCollectionPresentation.ts`
- `src/lib/documents.ts`

**Implementation steps**

1. Define the `DocumentReaderProfile`, `ReaderAudience`, and collection-presentation types described in Section 10.
2. Create a lookup keyed by the existing document ID, not by a duplicated filename.
3. Implement a join function that returns the catalog document, approved asset information, sequence entry, and reader profile as one view model.
4. Implement build-time assertions for missing, duplicate, orphaned, or title-mismatched profiles.
5. Assert exactly one start-here record and confirm it is reading order 1.
6. Keep hashes, commits, and paths sourced from existing manifests rather than copying them into the reader-profile file.
7. Export stable helpers for the research index and detail routes.

**Constraints**

- No new runtime dependency.
- No new database or CMS.
- Do not modify document authority fields in the presentation layer.
- Do not silently fall back to generic copy for an approved ontology paper. Missing human content should fail the build.

**Acceptance criteria**

- [ ] All eight approved ontology records can be joined to a reader profile.
- [ ] Technical metadata remains sourced from existing records.
- [ ] Build-time assertions cover the required structural invariants.
- [ ] The presentation layer cannot create a new scientific status value.

**Required validation**

V0 during coding. The assertions will be exercised at grouped Checkpoint A through `npm run build`.

**Done when**

Pages can consume one typed human-and-technical view model without duplicating authority data.

## Task HFDOC-011: Create the shared glossary

**Goal**

Define unfamiliar project and document terms once, with plain definitions and boundaries.

**Context**

Human readers should not have to infer exact closure, adoption, derivation, substrate, benchmark, TeX, or SHA-256 from context.

**Dependencies**

HFDOC-010.

**Likely files**

- `src/data/documentGlossary.ts`
- `src/lib/documentPresentation.ts`
- `optional src/components/documents/TermDefinition.astro`
- `optional src/pages/glossary/index.astro`

**Implementation steps**

1. Create entries for all terms listed in Section 10.5.
2. Use the existing ontology-page vocabulary as the basis for ontology terms.
3. Give each term a short definition suitable for inline or card use.
4. Add an expanded definition only where it improves understanding.
5. Add a `boundary` field where readers may confuse a term with proof, empirical confirmation, or package completeness.
6. Add source-basis references using repository paths or document IDs.
7. Expose a helper that returns terms in a requested order.
8. Use visible text or keyboard-accessible links. Do not rely on hover-only tooltips.
9. Decide whether to add a full glossary route now or keep the first implementation embedded in relevant pages. The shared data model must support either.

**Constraints**

- Definitions must not strengthen claims.
- Definitions should use ordinary language before formal terminology.
- Do not define SHA-256 as a correctness test.

**Acceptance criteria**

- [ ] Every term referenced by a reader profile exists.
- [ ] Exact closure, adoption, and derivation have distinct definitions.
- [ ] TeX root file and source package are not conflated.
- [ ] Definitions can be rendered without JavaScript.

**Required validation**

V0. Content and type review only; build coverage occurs at Checkpoint A.

**Done when**

All required terms can be explained consistently near first use.

## Task HFDOC-012: Write the canonical human explanation of exact closure

**Goal**

Create one reviewed explanation that can be reused on the collection page and detail pages.

**Context**

The exact-closure manuscript already states the substantive distinction: observer-level dynamics are GR by adoption while deeper substrate derivation remains open.

**Dependencies**

HFDOC-011.

**Likely files**

- `src/data/documentCollectionPresentation.ts`
- `src/data/documentGlossary.ts`
- `source references to the registered overview manuscript`

**Implementation steps**

1. Add the exact-closure definition from Appendix A as the default plain-language explanation.
2. Add three short sections: `What is fixed`, `What is interpretive`, and `What remains open`.
3. Add separate definitions for adoption and derivation.
4. Add a concise statement that exact closure does not mean the ontology has been empirically confirmed.
5. Add a concise statement that the active package does not claim a distinct verified observer-level law beyond GR.
6. Add source-basis references to the overview manuscript sections that define exact closure, operational identity, adoption, derivation, and nonclaims.
7. Mark the presentation copy as reviewed before publication.

**Constraints**

- Do not describe exact closure as proof of substrate physics.
- Do not imply that the project has derived GR from first principles.
- Do not omit the distinction between effective theory and ontology.
- Do not use `theory is complete` without immediately stating the bounded effective scope.

**Acceptance criteria**

- [ ] The explanation answers what is closed, why it is called exact, and what remains open.
- [ ] The three-part fixed/interpretive/open structure is available to pages.
- [ ] Adoption and derivation are independently defined.
- [ ] Copy remains within the registered source boundary.

**Required validation**

V0. Source-to-summary review only.

**Done when**

The project has one reusable, reviewed human explanation of exact closure.

## Task HFDOC-013: Create reader profiles for all eight ontology papers

**Goal**

Write complete human-facing profiles for the full canonical collection.

**Context**

The current catalog summaries are compact indexing descriptions. Each paper needs a question, explanation, reader value, and nonclaim set.

**Dependencies**

HFDOC-010 through HFDOC-012.

**Likely files**

- `src/data/documentReaderProfiles.ts`
- `public/files/manifests/document_catalog.json`
- `src/lib/manifests.ts`
- `registered ontology TeX sources`

**Implementation steps**

1. Create one profile for each of the eight document IDs.
2. Use the paper questions and summaries in Appendix B as the starting copy.
3. Keep the formal catalog title unchanged in `formalTitle`.
4. Add a clearer display title only where it improves orientation.
5. Mark the Exact Closure Sequence Overview as `startHere`.
6. Describe the final flagship article as a synthesis after the core, not as a replacement for the overview.
7. Add `whyRead`, `whatYouWillLearn`, `establishes`, and `doesNotEstablish` fields.
8. Add audience and difficulty level.
9. Add glossary references.
10. Add title-specific PDF and TeX action labels.
11. Record current TeX packaging as `root-only` until package tasks complete.
12. Add source-basis paths or section references for every substantive summary.

**Constraints**

- Do not invent learning outcomes not supported by the paper.
- Do not flatten important differences between the overview, note, core modules, and flagship article.
- Do not use the same generic action text for all papers.
- Do not label root-only TeX as compilable.

**Acceptance criteria**

- [ ] Exactly eight reviewed profiles exist.
- [ ] Profile order matches the canonical reading order.
- [ ] Every profile contains a reader question and nonclaim section.
- [ ] Every profile has distinct PDF accessible labels.
- [ ] Every profile truthfully describes TeX packaging.

**Required validation**

V0. Source-to-profile review only; structural assertions run at Checkpoint A.

**Done when**

All ontology papers have complete human presentation data.

## Task HFDOC-014: Define publication, format, and verification explanations

**Goal**

Create reusable plain-language explanations for status, PDF, TeX, source packages, revisions, and hashes.

**Context**

Readers currently see internal values without enough explanation. The site must separate website publication state from scientific scope.

**Dependencies**

HFDOC-010 and HFDOC-011.

**Likely files**

- `src/data/documentCollectionPresentation.ts`
- `src/data/documentGlossary.ts`
- `src/lib/documentPresentation.ts`

**Implementation steps**

1. Add the PDF explanation from Appendix A.
2. Add the TeX root-file explanation from Appendix A.
3. Add source-package wording for unvalidated and compile-validated packages.
4. Add a plain explanation of website publication approval.
5. Add a separate explanation of scientific scope.
6. Add a humanized date helper and file-size helper.
7. Add the SHA-256 explanation from Appendix A.
8. Add labels for source revision and website synchronization date.
9. Define when exact bytes and raw status values appear in technical details.
10. Ensure all visible labels avoid raw underscore-separated values.

**Constraints**

- Do not say `approved research` when the actual meaning is approved for website publication.
- Do not say `published date` when the value is an import date.
- Do not imply that a hash verifies scientific correctness.
- Do not imply that a TeX root file contains all dependencies.

**Acceptance criteria**

- [ ] Reusable explanations exist for every file and status concept used on the page.
- [ ] Visible values use humanized formatting.
- [ ] Exact technical values remain available.
- [ ] Publication state and scientific scope are clearly separate.

**Required validation**

V0. Copy review only.

**Done when**

Components can explain technical records without exposing internal vocabulary as the primary interface.

# Phase 2: Build Shared Reader-Facing Document Components

## Objective

Replace the current metadata-first card pattern with reusable human-first components while preserving every technical field.

## Task HFDOC-020: Build the reader-first document card

**Goal**

Create a card that prioritizes the paper's purpose, reader question, summary, and actions.

**Context**

The current two-column card gives the metadata rail nearly equal weight. The new card should be a readable single-column experience with optional technical details below.

**Dependencies**

HFDOC-010 through HFDOC-014.

**Likely files**

- `src/components/documents/ReaderDocumentCard.astro`
- `src/components/documents/DocumentCard.astro`
- `src/components/documents/DocumentCollection.astro`

**Implementation steps**

1. Create `ReaderDocumentCard.astro` using the joined presentation view model.
2. Render sequence number, role, reader question, display title, formal title when different, summary, learning outcomes, and actions.
3. Use semantic `<article>` markup and a stable heading ID.
4. Keep the ordered list semantics supplied by the collection.
5. Allow a featured variant for the start-here paper.
6. Allow compact and full variants for collection index and related-paper contexts.
7. Keep the existing `DocumentCard` available temporarily for routes not yet migrated.
8. After all intended consumers migrate, either make `DocumentCard` a compatibility wrapper or remove it in a bounded cleanup task.

**Constraints**

- Do not render technical metadata in a side-by-side rail by default.
- Do not duplicate status or format role in multiple visible locations.
- Do not make the entire card a link because it contains multiple actions.

**Acceptance criteria**

- [ ] The card can render all eight papers.
- [ ] Human explanation appears before technical metadata.
- [ ] The start-here variant is visually and semantically distinct.
- [ ] Existing nonresearch consumers are not broken.

**Required validation**

V0 during task. Included in Checkpoint A build.

**Done when**

The research collection can render reader-first cards without losing technical access.

## Task HFDOC-021: Replace generic document actions with title-specific actions

**Goal**

Make every link identify the document, format, and behavior.

**Context**

Generic labels such as `Read PDF derivative` are artifact-role descriptions and produce ambiguous screen-reader link lists.

**Dependencies**

HFDOC-013 and HFDOC-020.

**Likely files**

- `src/components/documents/DocumentFormatActions.astro`
- `src/components/documents/DocumentActions.astro`
- `src/data/documentReaderProfiles.ts`

**Implementation steps**

1. Create `DocumentFormatActions.astro` or extend the existing action component to accept reader-profile labels.
2. Use labels such as `Read Exact Closure Overview (PDF)` and `Download Foundations (PDF)`.
3. Use `View registered root TeX manuscript` until a complete source package exists.
4. Add package actions only when the bundle record exists.
5. Ensure open-in-browser and download actions are visibly distinct.
6. Keep `aria-label` values document-specific even when visible labels are shortened in compact contexts.
7. Place PDF reading action first, PDF download second where both are offered, and TeX/source actions after PDF.
8. Keep technical provenance and machine-record actions outside the primary action row.

**Constraints**

- Do not use `derivative` in primary action text.
- Do not provide two actions with identical visible labels and different behavior.
- Do not add `target=_blank` unless the site has a consistent, communicated policy.

**Acceptance criteria**

- [ ] Every paper has a unique accessible PDF read link.
- [ ] Every download action identifies its format.
- [ ] TeX labels reflect actual packaging state.
- [ ] Primary actions are understandable without reading adjacent metadata.

**Required validation**

V0 during coding. Keyboard and link-purpose review occurs in HFDOC-080.

**Done when**

Document actions communicate destination and behavior clearly.

## Task HFDOC-022: Create technical provenance progressive disclosure

**Goal**

Preserve exact metadata while moving it behind an intentional technical-details control.

**Context**

Hashes, paths, commits, exact bytes, and role codes are valuable to reviewers and agents but should not dominate the default reading experience.

**Dependencies**

HFDOC-014 and HFDOC-020.

**Likely files**

- `src/components/documents/TechnicalProvenanceDisclosure.astro`
- `src/components/documents/DocumentMetadata.astro`
- `src/components/StatusDossier.astro`

**Implementation steps**

1. Create a native `<details>` disclosure with a `<summary>` such as `Technical provenance and file verification`.
2. Group registered-source details separately from PDF-reading-copy details.
3. Reuse existing metadata extraction logic.
4. Render human labels and preserve exact values.
5. Show approximate size outside the disclosure and exact bytes inside.
6. Explain SHA-256 before showing the value.
7. Add a copy-friendly code presentation for hashes and paths.
8. Optionally add a small `How to verify this file` subsection with standard commands, but keep it collapsed or secondary.
9. Ensure the disclosure works without client-side JavaScript.
10. Keep raw status values or role codes available only when useful to technical reviewers.

**Constraints**

- Do not remove any existing metadata field.
- Do not describe a source commit as a publication date.
- Do not use a tooltip as the only explanation.
- Do not expose private local paths.

**Acceptance criteria**

- [ ] All current technical metadata remains accessible.
- [ ] No full SHA-256 is visible before disclosure.
- [ ] Source and PDF data are visually grouped.
- [ ] The control is keyboard accessible and works without JavaScript.

**Required validation**

V0 during coding. Included in Checkpoint A build and HFDOC-080 manual check.

**Done when**

Technical reviewers retain exact data while human readers see a calm default card.

## Task HFDOC-023: Build the narrative document sequence

**Goal**

Represent the eight-paper collection as a guided argument rather than a list of registry positions.

**Context**

The sequence has meaningful roles: overview, short anchor, foundations, dynamics, consistency, recovery, geometry, and synthesis.

**Dependencies**

HFDOC-013.

**Likely files**

- `src/components/documents/DocumentSequence.astro`
- `src/data/documentReaderProfiles.ts`
- `src/lib/manifests.ts`

**Implementation steps**

1. Render an ordered list with paper number, human question, display title, and one-sentence purpose.
2. Mark the first item `Start here`.
3. Mark papers 2 through 7 as the coordinated core, using plain language rather than internal role codes.
4. Mark paper 8 as the public synthesis after the core.
5. Link sequence entries to HTML guide pages once those routes exist.
6. Provide a fallback link to the card anchor before detail routes are complete.
7. Use semantic ordered-list markup so sequence remains meaningful to agents and assistive technology.

**Constraints**

- Do not reorder the canonical source sequence.
- Do not imply that the flagship article replaces the overview.
- Do not expose role values such as `ordered_core` as visible copy.

**Acceptance criteria**

- [ ] All eight entries appear once and in canonical order.
- [ ] Each entry answers a human question.
- [ ] Start, core, and synthesis roles are clear.
- [ ] Sequence remains usable without visual styling.

**Required validation**

V0. Structural build assertion and final page build cover sequence integrity.

**Done when**

Readers can understand the logic of the collection before opening a paper.

## Task HFDOC-024: Build summary and claim-boundary blocks

**Goal**

Create reusable components for key information, fixed/interpretive/open structure, and nonclaims.

**Context**

Research pages need concise orientation without turning claim boundaries into a dense status dashboard.

**Dependencies**

HFDOC-012 and HFDOC-014.

**Likely files**

- `src/components/documents/ReaderSummaryBox.astro`
- `src/components/documents/ClaimBoundaryList.astro`
- `src/data/documentCollectionPresentation.ts`

**Implementation steps**

1. Create a semantic key-information summary block.
2. Create a three-column or stacked `Fixed`, `Interpretive`, and `Open` block.
3. Create a concise `What this does not claim` block.
4. Allow components to render as stacked cards on small screens.
5. Use headings and ordinary prose, not status codes.
6. Ensure colors are supplementary and labels carry the meaning.
7. Allow the same components to appear on collection and detail pages.

**Constraints**

- Do not use `safe` and `unsafe` as the primary public labels unless the surrounding page explains them.
- Do not present nonclaims as hidden fine print.
- Do not visually imply that open research is a failure state.

**Acceptance criteria**

- [ ] Key information can be scanned quickly.
- [ ] Claim limits remain visible and plain.
- [ ] Components reflow to one column.
- [ ] Content remains semantically ordered.

**Required validation**

V0. Included in Checkpoint A build.

**Done when**

The collection can explain scientific scope before presenting downloads.

## Task HFDOC-025: Implement reader-focused document styling and responsive behavior

**Goal**

Change visual hierarchy from dashboard-like metadata cards to readable research-library cards.

**Context**

The current document card uses a two-column layout and monospace metadata rail. The new default should prioritize prose and actions.

**Dependencies**

HFDOC-020 through HFDOC-024.

**Likely files**

- `src/styles/global.css`
- `optional route-specific stylesheet if the repository already uses one`
- `src/components/documents/*.astro`

**Implementation steps**

1. Use a primarily single-column card layout.
2. Limit long explanatory prose to a readable measure.
3. Place technical disclosure below the actions.
4. Give the start-here card stronger but restrained emphasis.
5. Use whitespace and heading scale to separate question, summary, learning outcomes, actions, and details.
6. Stack actions on narrow screens when necessary.
7. Ensure long hashes and paths wrap or scroll only inside the technical disclosure.
8. Remove any minimum side-rail width from the reader card.
9. Preserve visible focus styles.
10. Respect reduced-motion settings and avoid adding motion solely for decoration.
11. Keep technical monospace styling inside technical details, not in the primary summary.
12. Verify that the card remains usable at 320 CSS pixels and high zoom.

**Constraints**

- Do not redesign the global visual system.
- Do not introduce a new CSS framework.
- Do not rely on color alone.
- Do not reduce text size to fit metadata.

**Acceptance criteria**

- [ ] Main copy receives clear visual priority.
- [ ] Technical values no longer compete with the title and summary.
- [ ] Actions remain usable on narrow screens.
- [ ] Long technical values do not widen the page.

**Required validation**

V0 during coding. Visual spot check is grouped into HFDOC-083 and Checkpoint A.

**Done when**

The shared document components have a human reading hierarchy on desktop and mobile.

# Phase 3: Rebuild the Ontology Research Collection Page

## Objective

Turn `/documents/research/` into the obvious, explanatory, human-accessible home for all eight ontology papers while preserving direct source and machine access.

## Task HFDOC-030: Rewrite the research-page hero and introduction

**Goal**

Explain the collection's subject, purpose, and file access before discussing provenance.

**Context**

The current hero and introduction begin with source-oriented collection language. The new opening should answer what the papers are about and where to begin.

**Dependencies**

HFDOC-012 through HFDOC-014 and Phase 2 components.

**Likely files**

- `src/pages/documents/research/index.astro`
- `src/data/documentCollectionPresentation.ts`

**Implementation steps**

1. Change the visible page title to the adopted human-facing title.
2. Use the hero copy in Appendix A or an equally bounded reviewed revision.
3. Add a primary `Start with the overview` action.
4. Add a secondary `Browse all 8 papers` action.
5. Keep links to ontology orientation and claim status available as secondary context.
6. Move direct technical-record links out of the hero.
7. Replace `source-oriented document collection`, `manifestation`, and equivalent internal language in the opening copy.
8. State that PDFs are available for reading and TeX is available for technical inspection.

**Constraints**

- Do not hide the relationship to GR.
- Do not imply first-principles derivation is complete.
- Do not lead with catalog or manifest mechanics.

**Acceptance criteria**

- [ ] A first-time reader can describe the collection after reading the hero.
- [ ] The starting paper is one interaction away.
- [ ] The PDF and TeX availability is clear.
- [ ] Technical provenance is not the primary entry action.

**Required validation**

V0. Included in Checkpoint A build.

**Done when**

The first screen explains the subject and provides a direct human reading action.

## Task HFDOC-031: Add exact-closure, adoption, and derivation explanation

**Goal**

Place the core conceptual explanation before the paper list.

**Context**

Readers need to know what exact closure means before the site asks them to follow an exact-closure sequence.

**Dependencies**

HFDOC-012 and HFDOC-024.

**Likely files**

- `src/pages/documents/research/index.astro`
- `src/components/documents/ReaderSummaryBox.astro`
- `src/components/documents/ClaimBoundaryList.astro`

**Implementation steps**

1. Add the `Key information` summary from Appendix A.
2. Add a section titled `What exact closure means`.
3. Render the reviewed definition.
4. Render the `What is fixed`, `What is interpretive`, and `What remains open` structure.
5. Add a concise adoption-versus-derivation explanation.
6. Add a visible nonclaim statement that ontology alone is not empirical confirmation.
7. Link to the deeper ontology orientation and exact-GR boundary routes after the explanation.

**Constraints**

- Keep the explanation concise enough to scan.
- Do not put the central definition inside a collapsed disclosure.
- Do not substitute a diagram for the textual definition.

**Acceptance criteria**

- [ ] Exact closure is defined before the document sequence.
- [ ] Adoption and derivation are distinguishable in plain language.
- [ ] GR compatibility and open substrate derivation are both visible.
- [ ] Nonclaims are not hidden.

**Required validation**

V0. Source-boundary review and grouped build only.

**Done when**

The collection page supplies the conceptual context currently found only inside the manuscript.

## Task HFDOC-032: Create the featured start-here paper section

**Goal**

Give the Exact Closure Sequence Overview a distinct, explanatory entry point.

**Context**

The first paper is the canonical overview, but a normal list card does not make its role sufficiently clear to humans.

**Dependencies**

HFDOC-020, HFDOC-021, and HFDOC-013.

**Likely files**

- `src/pages/documents/research/index.astro`
- `src/components/documents/ReaderDocumentCard.astro`
- `src/data/documentReaderProfiles.ts`

**Implementation steps**

1. Render the overview as a featured card before the general sequence or as the first strongly distinguished item.
2. Show `Start here` and `Paper 1 of 8`.
3. Use the human display title `Exact Closure: Overview and Reading Guide` while retaining the formal title nearby.
4. Show the full plain summary.
5. Show the primary learning outcomes.
6. Provide direct PDF reading, PDF download, and truthful TeX actions.
7. Link to the HTML guide page when Phase 4 is complete.
8. Ensure the same document is not accidentally duplicated as a second full card. If it appears again in the full list, use a compact representation or clearly treat the list as an index.

**Constraints**

- Do not hide the formal source title.
- Do not present the flagship article as the start-here paper.
- Do not use `canonical front door` as the only explanation.

**Acceptance criteria**

- [ ] The overview is visibly the recommended first document.
- [ ] Its purpose and nonclaims are understandable before opening it.
- [ ] Actions name the document and format.
- [ ] No confusing duplicate full card appears.

**Required validation**

V0. Included in Checkpoint A build.

**Done when**

Readers have an unmistakable first document and can open it directly.

## Task HFDOC-033: Add the eight-paper narrative reading path

**Goal**

Explain how the collection forms one continuous argument.

**Context**

A bare sequence number is not enough for a human to infer the relation among papers.

**Dependencies**

HFDOC-023.

**Likely files**

- `src/pages/documents/research/index.astro`
- `src/components/documents/DocumentSequence.astro`

**Implementation steps**

1. Add a section such as `How to read the collection`.
2. Use the eight questions and roles from Appendix B.
3. Explain that papers 2 through 7 form the ordered scientific core after the overview.
4. Explain that paper 8 is a public synthesis after the core.
5. Link each sequence item to its detail route or card anchor.
6. Keep the sequence visually readable but semantically an ordered list.
7. Add one sentence that the order is a reading guide and claim-boundary aid, not an independent proof.

**Constraints**

- Do not change the canonical order.
- Do not make the sequence depend on JavaScript.
- Do not use internal role codes as visible labels.

**Acceptance criteria**

- [ ] All eight papers appear once in the reading path.
- [ ] Each item explains why it follows the previous one.
- [ ] Overview, core, and synthesis roles are clear.
- [ ] Sequence links work.

**Required validation**

V0. Build covers route links at Checkpoint A.

**Done when**

Readers can choose a paper based on the question they want answered.

## Task HFDOC-034: Render the complete paper collection with reader-first cards

**Goal**

Provide direct access to every PDF and TeX file without making readers parse technical dossiers.

**Context**

The page must remain the complete document collection, not only an overview narrative.

**Dependencies**

HFDOC-020 through HFDOC-025 and HFDOC-013.

**Likely files**

- `src/pages/documents/research/index.astro`
- `src/components/documents/DocumentCollection.astro`
- `src/components/documents/ReaderDocumentCard.astro`

**Implementation steps**

1. Replace or migrate the current card rendering to reader-first cards.
2. Keep canonical ordering enforced by existing sequence logic.
3. Show question, title, summary, and main actions.
4. Show concise humanized format availability.
5. Add the technical provenance disclosure to every card.
6. Keep related routes only when they add human explanation.
7. Remove duplicated format-role pills when the action and format help already communicate the distinction.
8. Ensure all eight PDF links and all eight TeX root links remain reachable.
9. Use detail pages as the preferred title link when Phase 4 is complete.

**Constraints**

- Do not remove direct raw file access.
- Do not hide TeX behind a technical-record JSON page.
- Do not show full hashes by default.
- Do not repeat identical explanatory paragraphs on every card.

**Acceptance criteria**

- [ ] All eight documents render in canonical order.
- [ ] Every document has direct PDF and TeX access.
- [ ] Visible card copy is human-oriented.
- [ ] All exact metadata remains available after disclosure.

**Required validation**

V0 during coding. Checkpoint A build and HFDOC-080 manual link review.

**Done when**

The collection remains complete while becoming understandable.

## Task HFDOC-035: Add format guidance and the shared glossary

**Goal**

Explain PDF, TeX, source packages, and key terms near the collection.

**Context**

Readers need enough format guidance to choose an action without understanding the publication system.

**Dependencies**

HFDOC-011 and HFDOC-014.

**Likely files**

- `src/pages/documents/research/index.astro`
- `src/data/documentGlossary.ts`
- `optional src/components/documents/TermDefinition.astro`

**Implementation steps**

1. Add a short `Choose a format` section.
2. Explain PDF as the reading, printing, and sharing format.
3. Explain root TeX as source inspection and formula/document structure.
4. Explain source packages separately.
5. Add or link glossary definitions for exact closure, ontology, effective theory, adoption, derivation, substrate, benchmark, TeX, and SHA-256.
6. Place SHA-256 explanation near technical records, not in the main reading path.
7. Ensure definitions are available through visible text or normal links.

**Constraints**

- Do not require hover.
- Do not show a long technical glossary before the paper list.
- Do not imply every TeX root file is self-contained.

**Acceptance criteria**

- [ ] A reader can choose PDF or TeX knowingly.
- [ ] Key scientific terms have plain definitions.
- [ ] Technical verification terms are available but secondary.

**Required validation**

V0. Included in Checkpoint A build.

**Done when**

Format and terminology no longer act as hidden prerequisites.

## Task HFDOC-036: Create collection downloads and technical-record sections

**Goal**

Separate collection-level human downloads from machine and provenance records.

**Context**

Humans need one place to download the collection. Agents and reviewers still need manifests.

**Dependencies**

HFDOC-024 and HFDOC-065 for final bundle activation.

**Likely files**

- `src/pages/documents/research/index.astro`
- `src/components/documents/CollectionDownloadPanel.astro`
- `src/data/documentCollectionPresentation.ts`

**Implementation steps**

1. Add a `Download the collection` section.
2. Before bundles exist, render only available actions and a truthful `Complete package not yet published` note.
3. After Phase 6, activate all-PDF and TeX-collection actions.
4. Add a separate `Technical records` disclosure or secondary section.
5. Move document-catalog JSON, source manifest, and asset manifest links into technical records.
6. Describe machine records as identity and provenance data, not scientific proof.
7. Ensure the primary button remains the overview PDF or guide, not JSON.

**Constraints**

- Do not render inactive download buttons.
- Do not fabricate bundle paths before files and manifest records exist.
- Do not remove existing JSON endpoints.

**Acceptance criteria**

- [ ] Collection downloads and technical records are visibly separate.
- [ ] Primary human actions precede machine records.
- [ ] Unavailable packages are not represented as published.
- [ ] Machine manifests remain discoverable.

**Required validation**

V0 until bundles are created. Bundle links are checked in Phase 6 and Checkpoint B.

**Done when**

Humans can find collection actions while reviewers retain direct machine access.

## Task HFDOC-037: Remove remaining machine-first language from the research page

**Goal**

Complete a focused copy pass so internal publication terminology no longer dominates visible page text.

**Context**

Even after component changes, old section headings and status copy can preserve the machine-first tone.

**Dependencies**

HFDOC-030 through HFDOC-036.

**Likely files**

- `src/pages/documents/research/index.astro`
- `src/components/documents/*.astro`
- `src/data/documentCollectionPresentation.ts`

**Implementation steps**

1. Search the rendered source copy for `manifestation`, `canonical front door`, `source-oriented`, `readable derivative`, `authority scope`, `website import`, and raw underscore status values.
2. Replace public occurrences with adopted human labels where the technical term is not necessary.
3. Keep precise terms inside technical disclosures when they add value.
4. Review headings for reader questions and actions rather than system state.
5. Review ARIA labels for meaningful human context.
6. Confirm `Read PDF derivative` no longer appears.

**Constraints**

- Do not remove necessary scientific terms such as ontology or derivation. Define them instead.
- Do not weaken source-role distinctions while simplifying labels.

**Acceptance criteria**

- [ ] Visible copy is understandable without repository knowledge.
- [ ] Technical terminology is defined or placed in technical details.
- [ ] No generic PDF-derivative action remains.

**Required validation**

V0. Manual source-copy search only; no new script.

**Done when**

The research page consistently follows the human-first language contract.

# Phase 4: Add Human HTML Guide Pages for Every Paper

## Objective

Create stable HTML orientation pages between the collection index and the raw PDF/TeX files.

## Task HFDOC-040: Create the static paper-guide route and layout

**Goal**

Generate one static guide page for every canonical ontology paper.

**Context**

HTML guide pages let humans understand purpose and limits before entering a long PDF, while giving agents a stable semantic route.

**Dependencies**

HFDOC-010 through HFDOC-025.

**Likely files**

- `src/pages/documents/research/[slug].astro`
- `src/layouts/DocumentGuideLayout.astro`
- `src/lib/documentPresentation.ts`
- `src/components/documents/DocumentGuideNavigation.astro`

**Implementation steps**

1. Create a static dynamic route using `getStaticPaths` over the joined approved ontology view models.
2. Use the existing document slug as the route slug unless a human alias is deliberately added.
3. Render a common guide layout with breadcrumb, sequence position, display title, formal title, summary, sections, actions, sequence navigation, and provenance disclosure.
4. Add page title and description metadata from the reader profile.
5. Use semantic `<article>` and heading hierarchy.
6. Keep the raw PDF and TeX URLs unchanged.
7. Return no route for an unapproved or unknown document.
8. Fail the build if a canonical approved document lacks a guide.

**Constraints**

- No new client-side framework.
- No duplicate scientific status fields.
- No generated guide may be treated as the registered manuscript.

**Acceptance criteria**

- [ ] Eight static guide routes are generated.
- [ ] Every route maps to one approved catalog record.
- [ ] Unknown slugs do not generate pages.
- [ ] Guide pages work without JavaScript.

**Required validation**

V0 during implementation. Checkpoint A build verifies static route generation.

**Done when**

Every ontology paper has a stable human HTML entry page.

## Task HFDOC-041: Build the Exact Closure Overview guide

**Goal**

Create the strongest and most complete guide page for the starting paper.

**Context**

The overview page is the main bridge between general orientation and the technical collection.

**Dependencies**

HFDOC-040 and HFDOC-012.

**Likely files**

- `src/data/documentReaderProfiles.ts`
- `src/pages/documents/research/[slug].astro`
- `optional paper-specific data in src/data/documentGuideDetails.ts`

**Implementation steps**

1. Use the Appendix A overview copy.
2. Explain why this paper exists.
3. Explain exact closure.
4. Explain adoption versus derivation.
5. List what the reader will learn.
6. List what the paper establishes.
7. List what it does not establish.
8. Explain the role of the remaining seven papers.
9. Provide PDF read/download and truthful TeX actions.
10. Link back to the collection and forward to the Exact Closure Note.
11. Include technical provenance collapsed by default.

**Constraints**

- Do not reproduce the entire manuscript.
- Do not replace source language with a stronger public claim.
- Do not omit the open substrate-derivation burden.

**Acceptance criteria**

- [ ] The guide answers the main conceptual questions without requiring the PDF.
- [ ] The overview remains clearly paper 1 of 8.
- [ ] Direct source and PDF access are preserved.
- [ ] Nonclaims are visible.

**Required validation**

V0. Source-to-guide review only; route build occurs at Checkpoint A.

**Done when**

The primary paper has a complete human orientation page.

## Task HFDOC-042: Build guide content for papers 2 through 7

**Goal**

Create clear, consistent guide pages for the exact-closure note and five core modules.

**Context**

Each core paper answers a different reader question and should not look like a generic duplicate.

**Dependencies**

HFDOC-040 and HFDOC-013.

**Likely files**

- `src/data/documentReaderProfiles.ts`
- `optional src/data/documentGuideDetails.ts`
- `registered ontology TeX sources`

**Implementation steps**

1. Complete the guide content for Exact Closure Note, Foundations, Dynamics, Consistency, Relativistic Recovery, and Flow Geometry.
2. For each guide, state the paper's role in the sequence.
3. Add why-read, learning, establishes, and does-not-establish sections.
4. Add paper-specific glossary terms.
5. Add related internal routes only when they explain the paper's topic.
6. Add direct PDF and TeX actions.
7. Add previous and next links.
8. Keep formal titles intact.
9. Review each guide against its registered manuscript rather than extrapolating from title alone.

**Constraints**

- Do not reuse the same nonclaim list mechanically if a paper has more specific boundaries.
- Do not describe consistency checks as independent derivation of the ontology.
- Do not describe relativistic recovery as evidence of a new observer-level deviation from GR.

**Acceptance criteria**

- [ ] Six distinct core guide profiles are complete.
- [ ] Each guide explains its own purpose and limits.
- [ ] Sequence navigation is correct.
- [ ] All source references remain direct.

**Required validation**

V0. Content review and grouped build only.

**Done when**

Papers 2 through 7 have complete human orientation pages.

## Task HFDOC-043: Build the flagship-article guide and preserve its secondary sequence role

**Goal**

Explain the public synthesis without allowing it to displace the overview or ordered core.

**Context**

The source states that the flagship article is release-facing synthesis after the core.

**Dependencies**

HFDOC-040 and HFDOC-013.

**Likely files**

- `src/data/documentReaderProfiles.ts`
- `src/pages/documents/research/[slug].astro`

**Implementation steps**

1. Describe the flagship article as a synthesis for readers who want the complete package in one public-facing treatment.
2. State that it should be read after the ordered core.
3. State that it does not replace the overview.
4. State that it does not alter the claim boundary.
5. Provide PDF and TeX actions.
6. Link back to Flow Geometry and the full collection.
7. Use a `Public synthesis` role label rather than `Start here`.

**Constraints**

- Do not make the flagship article the default hero action.
- Do not imply it has higher source authority than the overview or root papers.

**Acceptance criteria**

- [ ] The guide clearly identifies paper 8 of 8.
- [ ] Its synthesis role is plain.
- [ ] The overview remains the recommended starting paper.
- [ ] Technical source access remains available.

**Required validation**

V0. Source-to-guide review only.

**Done when**

The final paper has a human page that preserves its correct place in the collection.

## Task HFDOC-044: Add selected equation and symbol explanations where they improve orientation

**Goal**

Use existing KaTeX support to explain a small number of central equations without recreating the manuscripts.

**Context**

Some readers benefit from seeing the effective action, Einstein equation, null condition, or proper-time relation with ordinary-language explanation.

**Dependencies**

HFDOC-040 through HFDOC-043.

**Likely files**

- `src/data/documentReaderProfiles.ts or src/data/documentGuideDetails.ts`
- `src/components/documents/DocumentEquationGuide.astro`
- `src/styles/math.css`
- `existing KaTeX pipeline`

**Implementation steps**

1. Identify only the equations necessary for orientation on the overview, dynamics, or relativistic-recovery guides.
2. For each selected equation, provide expression, label, symbol meanings, assumptions, and limits.
3. State the source paper and section.
4. Explain in one or two sentences what the equation says in the context of the paper.
5. Do not add equations to a guide when they do not improve the reader's decision or understanding.
6. Use existing math rendering and avoid a new dependency.
7. Provide a plain-text explanation adjacent to rendered mathematics.

**Constraints**

- Do not present selected equations as a substitute for the full derivation.
- Do not introduce equations not present in the source.
- Do not overload every guide with math.

**Acceptance criteria**

- [ ] Only high-value equations are included.
- [ ] Symbols are explained.
- [ ] Assumptions and limits are visible.
- [ ] Math rendering reuses existing support.

**Required validation**

V0. Covered by grouped build. No equation-specific test suite.

**Done when**

Readers can understand the role of central formulas without entering the PDF immediately.

## Task HFDOC-045: Add sequence navigation, related context, and structured technical details

**Goal**

Complete each guide with predictable movement through the collection and optional provenance.

**Context**

Guide pages should help readers continue without returning to a raw file list.

**Dependencies**

HFDOC-040 through HFDOC-044.

**Likely files**

- `src/components/documents/DocumentGuideNavigation.astro`
- `src/components/documents/TechnicalProvenanceDisclosure.astro`
- `src/pages/documents/research/[slug].astro`

**Implementation steps**

1. Add previous, collection, and next navigation with document titles.
2. Use `nav` with an accessible label.
3. Add related ontology, benchmark, and claim-status routes only where relevant.
4. Add the technical provenance disclosure.
5. Add direct machine-record links inside technical details.
6. Add alternate-format hints to the page head in Phase 7.
7. Ensure first and last papers omit nonexistent previous or next links cleanly.

**Constraints**

- Do not expose raw route paths as visible labels.
- Do not make GitHub or manifest links the primary next action.
- Do not create circular next/previous links.

**Acceptance criteria**

- [ ] All eight guide pages have correct navigation.
- [ ] First and last edge cases are handled.
- [ ] Technical metadata is available but secondary.
- [ ] Internal explanatory routes precede external or raw provenance links.

**Required validation**

V0. Checkpoint A build and one manual sequence click-through.

**Done when**

Each guide is a complete, navigable human entry point.

# Phase 5: Reframe the Library Overview, Navigation, and Anthology

## Objective

Make the broader document system task-oriented and ensure the empty anthology does not distract from the populated ontology collection.

## Task HFDOC-050: Rewrite `/documents/` around reader intentions

**Goal**

Turn the document landing page into a human routing page before explaining formats and authority.

**Context**

The current overview begins with categories, formats, provenance, and status. Those remain useful but should follow reader goals.

**Dependencies**

HFDOC-002 and Phases 1 through 4.

**Likely files**

- `src/pages/documents/index.astro`
- `src/data/documentCollectionPresentation.ts`
- `existing card and rail components`

**Implementation steps**

1. Change the visible page title to `Research Library` or the adopted equivalent.
2. Use the task-based hero copy in Appendix A.
3. Add reader-intention cards for new reader, research papers, visual explanation, project review, and machine-readable records.
4. Place the populated ontology collection prominently.
5. Place format and authority explanations after the reader-intention section.
6. Move Manifest JSON to the technical-reader section rather than presenting it beside PDF and TeX as an equal first-step format.
7. Keep reading paths and reviewer routes.
8. Keep source authority context, but use a secondary placement.
9. Ensure the first recommended path for a new reader goes to ontology orientation or the ontology papers, not a manifest.

**Constraints**

- Do not remove governance or technical routes.
- Do not make repository layout the first reader task.
- Do not describe empty collections as published.

**Acceptance criteria**

- [ ] A new reader can choose a path without understanding file formats.
- [ ] Ontology papers are one clear action away.
- [ ] Technical records remain available in a dedicated area.
- [ ] Existing canonical routes remain internal-first.

**Required validation**

V0. Included in Checkpoint A build.

**Done when**

The library landing page routes humans by intent before explaining the publication system.

## Task HFDOC-051: Update navigation labels and descriptions

**Goal**

Expose the human-first library structure in the shared header without rewriting navigation behavior.

**Context**

The navigation is data-driven and already supports keyboard, mobile, no-script, and focus behavior.

**Dependencies**

HFDOC-002 and HFDOC-050.

**Likely files**

- `src/lib/siteContent.ts`
- `src/layouts/BaseLayout.astro only if a directly observed label issue requires it`

**Implementation steps**

1. Update the parent label to the adopted `Library` or retained `Documents` decision.
2. Update child labels and descriptions to the task-based set.
3. Describe Ontology Papers as all eight papers with PDF and TeX access.
4. Describe Plain-Language Articles truthfully when the collection is empty.
5. Keep `matchPrefixes` on `/documents/`.
6. Preserve existing interaction code.
7. Update ARIA labels or footer references only where the visible product label changed.
8. Do not change header behavior unless a real defect appears.

**Constraints**

- Do not rewrite the navigation component.
- Do not add dynamic client-side catalog counting to the header.
- Do not introduce an empty-state badge that cannot be understood by assistive technology.

**Acceptance criteria**

- [ ] Navigation labels match page identities.
- [ ] Ontology Papers is easy to discover.
- [ ] Keyboard and mobile behavior remain structurally unchanged.
- [ ] All child links use canonical routes.

**Required validation**

V0. One manual menu open/close check is included in HFDOC-083.

**Done when**

The global navigation points humans to the correct document destinations.

## Task HFDOC-052: Replace the anthology policy-first page with an honest empty or populated state

**Goal**

Make `/documents/anthology/` useful even when no anthology records exist.

**Context**

The catalog currently contains no anthology items. The page should not require readers to pass through publication-system explanations before learning that fact.

**Dependencies**

HFDOC-002 and HFDOC-050.

**Likely files**

- `src/pages/documents/anthology/index.astro`
- `src/lib/siteContent.ts`
- `src/data/documentCollectionPresentation.ts`

**Implementation steps**

1. Change the title to `Plain-Language Articles`.
2. If the collection is empty, render `No plain-language articles are currently published in this collection` near the top.
3. Explain briefly what will appear there.
4. Add direct actions to Ontology Papers, the Exact Closure Overview guide, and ontology orientation.
5. Move catalog-chain and publication-gate explanations into a collapsed `How publication works` section or a lower secondary block.
6. If anthology records later exist, render human article cards with audience, summary, read action, date when available, and related research papers.
7. Do not create sample or placeholder publications.
8. Keep publication approval and authority details available in technical disclosure.

**Constraints**

- Do not hide the empty state below a long introduction.
- Do not represent planned titles as published.
- Do not remove the route solely because it is empty.

**Acceptance criteria**

- [ ] The empty state is immediately visible.
- [ ] The page gives a useful next step.
- [ ] Publication mechanics remain available but secondary.
- [ ] The populated-state rendering is defined for future records.

**Required validation**

V0. Included in Checkpoint A build.

**Done when**

The anthology route is honest, calm, and useful in both empty and populated states.

## Task HFDOC-053: Align breadcrumbs, route labels, internal links, and page metadata

**Goal**

Make the human-first naming consistent across the site.

**Context**

Changing page identities without updating related links creates a fragmented mental model.

**Dependencies**

HFDOC-050 through HFDOC-052.

**Likely files**

- `src/pages/documents/**/*.astro`
- `src/lib/siteContent.ts`
- `src/lib/documentPresentation.ts`
- `relevant physics pages that link to research documents`

**Implementation steps**

1. Update breadcrumbs, eyebrows, page titles, descriptions, and related-route labels.
2. Replace `Research Articles` with `Ontology Papers` where the route specifically refers to the canonical ontology collection.
3. Replace `Anthology Articles` with `Plain-Language Articles` where adopted.
4. Keep formal source titles unchanged.
5. Update internal link text to describe the destination rather than expose raw routes.
6. Search for stale navigation product labels.
7. Keep canonical URLs unchanged.

**Constraints**

- Do not rewrite unrelated prose that uses `documents` generically.
- Do not change upstream source titles.
- Do not create redirects for copy changes.

**Acceptance criteria**

- [ ] Visible route naming is consistent.
- [ ] Internal links describe their destination.
- [ ] Page metadata reflects the human page purpose.
- [ ] No canonical route changes are introduced.

**Required validation**

V0. Source search and grouped build only.

**Done when**

The document system reads as one coherent human-facing product.

## Task HFDOC-054: Keep governance, diagrams, and technical records available as secondary paths

**Goal**

Ensure the human-first redesign does not erase specialist and agent access.

**Context**

The main emphasis changes, but governance and diagram routes remain important.

**Dependencies**

HFDOC-050 through HFDOC-053.

**Likely files**

- `src/pages/documents/index.astro`
- `src/pages/documents/research/index.astro`
- `src/lib/siteContent.ts`

**Implementation steps**

1. Keep prominent but secondary links to Diagrams and Source & Governance.
2. Add one-sentence explanations of when a reader should use each route.
3. Keep technical-record links in a dedicated machine/reviewer area.
4. Ensure source-authority guidance remains reachable from research pages.
5. Do not add a dedicated boilerplate Source Authority section to document collection pages if repository rules forbid it.
6. Use contextual copy and existing governance routes instead.

**Constraints**

- Do not remove agent or maintainer paths.
- Do not allow governance details to displace the primary human reading action.
- Do not violate the repository rule against dedicated boilerplate source-authority sections on collection pages.

**Acceptance criteria**

- [ ] Human paths are primary and specialist paths remain discoverable.
- [ ] Governance and technical access are not lost.
- [ ] Repository layout remains secondary.

**Required validation**

V0. Link presence is covered by grouped build.

**Done when**

The broader documentation ecosystem remains intact after the human-first reordering.

# Phase 6: Create Truthful PDF and TeX Download Packages

## Objective

Provide convenient collection downloads and source packages without implying that incomplete root files are self-contained.

## Task HFDOC-060: Audit TeX dependencies and define package completeness

**Goal**

Determine exactly what each root TeX manuscript needs in order to compile.

**Context**

Published root files contain shared `\input` references. Package wording must reflect actual dependency completeness.

**Dependencies**

HFDOC-001 and HFDOC-014.

**Likely files**

- `public/files/tex/ontology/*.tex`
- `upstream ontology/tex sources through the authorized import process`
- `scripts/import_ontology_assets.py`
- `new scripts/build_ontology_download_bundles.py`

**Implementation steps**

1. Scan each root TeX file for `\input`, `\include`, bibliography, graphics, style, and other file dependencies.
2. Resolve dependencies recursively within an explicit allowlist.
3. Record shared files required by one or more papers.
4. Identify any dependencies that are not currently published to the website.
5. Classify each current public TeX file as root-only.
6. Define the minimum complete package for each paper and the full collection.
7. Record whether a TeX engine and compilation command are available in the authorized source environment.
8. Do not copy arbitrary files outside approved source roots.

**Constraints**

- Prevent absolute paths and `..` path traversal.
- Do not publish private control files, credentials, temporary outputs, or unrelated repository material.
- Do not call a package compilable before evidence exists.

**Acceptance criteria**

- [ ] Every root paper has a dependency inventory.
- [ ] Missing dependencies are known.
- [ ] Package completeness criteria are documented.
- [ ] Current public labels can accurately say root-only.

**Required validation**

V0. This is a source inspection task. No compilation is required yet.

**Done when**

The implementation knows exactly what must be included in each source package.

## Task HFDOC-061: Build the ordered PDF collection archive

**Goal**

Provide one convenient download containing all eight PDFs in canonical reading order.

**Context**

Humans should not have to download eight files individually when they want the complete collection.

**Dependencies**

HFDOC-060 is not strictly required for PDFs, but the shared bundle script design should be coordinated.

**Likely files**

- `scripts/build_ontology_download_bundles.py`
- `public/files/bundles/ontology/aether-flow-ontology-papers-pdf.zip`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`

**Implementation steps**

1. Create a deterministic ZIP archive.
2. Use ordinal filenames from Appendix C.
3. Include `00-README.txt` or `README.md`.
4. Include all eight approved PDF assets.
5. Include `manifest.json` listing logical document ID, source asset path, archive filename, size, hash, order, and role.
6. Include the project license or a clear usage note when permitted.
7. Set deterministic ZIP entry timestamps and ordering so repeated generation is stable.
8. Fail bundle generation if an expected approved PDF is missing.
9. Do not move or rename the direct public PDF assets.

**Constraints**

- Do not include unapproved files.
- Do not claim the ZIP itself has source authority.
- Do not silently omit a paper.

**Acceptance criteria**

- [ ] The archive contains exactly eight ordered PDFs plus support files.
- [ ] The README explains the reading order and scientific scope.
- [ ] The archive is deterministic.
- [ ] Direct PDF URLs remain unchanged.

**Required validation**

V2 only after manifest records are added: run `npm run validate:manifests` once in Checkpoint B, not during every edit.

**Done when**

One complete human-readable ontology collection can be downloaded.

## Task HFDOC-062: Build the complete TeX collection archive

**Goal**

Provide the full source collection with shared dependencies and instructions.

**Context**

Root TeX files alone may not compile. The collection archive should preserve required directory structure.

**Dependencies**

HFDOC-060.

**Likely files**

- `scripts/build_ontology_download_bundles.py`
- `public/files/bundles/ontology/aether-flow-ontology-tex-source.zip`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`

**Implementation steps**

1. Create an archive containing all eight root manuscripts.
2. Include every allowlisted shared dependency discovered in HFDOC-060.
3. Preserve relative paths expected by `\input`, bibliography, and graphics references.
4. Include a README with prerequisites, working directory, engine, commands when known, source revision, package scope, and known limitations.
5. Include a machine-readable manifest.
6. Include license or usage information.
7. Use deterministic archive ordering and timestamps.
8. Fail if a declared required dependency is missing.
9. If no TeX engine is available, label the result `TeX source package`, not `compilable TeX source package`.
10. If a single manual batch compilation succeeds, record the command and permit the compile-validated label.

**Constraints**

- Do not include generated temporary files unless needed and intentionally documented.
- Do not import local absolute paths into the README.
- Do not include unrelated upstream files.

**Acceptance criteria**

- [ ] The archive contains all root manuscripts and declared dependencies.
- [ ] Directory structure supports the source references.
- [ ] README truthfully states validation status.
- [ ] Bundle manifest records source revision and contents.

**Required validation**

Required checks are internal to the generation script. A compilation command is conditional and one-time only if the site will use the word `compilable`.

**Done when**

The complete source collection is available without misleading packaging claims.

## Task HFDOC-063: Build per-paper TeX source packages

**Goal**

Offer convenient source packages for readers who need only one manuscript.

**Context**

A complete collection archive can be large or inconvenient. Per-paper packages should contain only the root and required dependencies.

**Dependencies**

HFDOC-060 and HFDOC-062.

**Likely files**

- `scripts/build_ontology_download_bundles.py`
- `public/files/bundles/ontology/papers/*.zip`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`

**Implementation steps**

1. Generate one deterministic archive per paper.
2. Include the root manuscript and its transitive allowlisted dependencies.
3. Include a small README and manifest.
4. Use human-readable archive names.
5. Record whether the package has been compile-validated.
6. Expose package paths through presentation data only after the files exist.
7. Keep the direct root `.tex` action for source inspection.
8. Fail a package build if a declared dependency is missing.

**Constraints**

- Do not duplicate source authority fields in reader profiles.
- Do not call an unvalidated package compilable.
- Do not create packages for unknown or unapproved records.

**Acceptance criteria**

- [ ] Eight per-paper packages exist or a documented blocked item explains why a package cannot be safely made.
- [ ] Each archive includes only necessary approved files.
- [ ] Labels match validation status.
- [ ] Root TeX access remains available.

**Required validation**

Generation-script checks only. No recurring CI compile suite is required.

**Done when**

Readers can download one paper's complete source context.

## Task HFDOC-064: Implement deterministic bundle generation and manifest integration

**Goal**

Make package generation repeatable, bounded, and consistent with existing asset/source records.

**Context**

Manual ZIP creation would drift. A small script should own bundle contents and metadata.

**Dependencies**

HFDOC-060 through HFDOC-063.

**Likely files**

- `scripts/build_ontology_download_bundles.py`
- `scripts/import_ontology_assets.py`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `optional src/data/documentCollectionBundles.ts`

**Implementation steps**

1. Create or extend a Python script that reads the canonical document sequence and approved assets.
2. Resolve dependencies through an allowlisted source root.
3. Generate PDF and TeX archives deterministically.
4. Calculate archive hashes and sizes.
5. Add bounded `other`-kind source and asset manifest records for bundles if supported by existing validators.
6. Preserve unrelated manifest records.
7. Generate a small website-side bundle registry or presentation data only if the existing manifests do not provide enough UI information.
8. Report missing assets or dependencies clearly and exit without partial publication.
9. Do not delete unexpected existing bundle files automatically unless the script owns them and deletion is explicit.
10. Document the invocation in a short maintainer note.

**Constraints**

- No new Python dependency unless unavoidable.
- Use the standard library where possible.
- Prevent path traversal.
- Preserve unrelated manifest rows.
- Keep bundle ownership explicit.

**Acceptance criteria**

- [ ] Bundle generation is deterministic and bounded.
- [ ] Manifest records resolve to real files.
- [ ] Unrelated records are preserved.
- [ ] Partial or unsafe bundles fail closed.

**Required validation**

Script self-checks plus one `npm run validate:manifests` at Checkpoint B.

**Done when**

Bundles can be regenerated safely from approved inputs.

## Task HFDOC-065: Activate collection and per-paper package actions

**Goal**

Connect the new bundle files to human-facing pages using truthful labels.

**Context**

Download buttons must not precede actual files or overstate compilation status.

**Dependencies**

HFDOC-061 through HFDOC-064 and HFDOC-036.

**Likely files**

- `src/data/documentCollectionPresentation.ts`
- `src/data/documentReaderProfiles.ts`
- `src/components/documents/CollectionDownloadPanel.astro`
- `src/components/documents/DocumentFormatActions.astro`
- `src/pages/documents/research/index.astro`
- `src/pages/documents/research/[slug].astro`

**Implementation steps**

1. Add the all-PDF archive to the collection download panel.
2. Add the full TeX collection archive.
3. Add per-paper source-package actions.
4. Derive label wording from package validation status.
5. Show archive size in humanized form.
6. Keep direct PDF and root TeX links.
7. Add a short explanation of what each archive contains.
8. Keep archive hashes in technical details.

**Constraints**

- Do not show an action for a missing bundle.
- Do not replace direct file links with ZIP-only access.
- Do not use `compilable` without recorded evidence.

**Acceptance criteria**

- [ ] All published bundles have working human actions.
- [ ] Labels accurately describe contents and status.
- [ ] Direct files remain available.
- [ ] Technical bundle metadata remains secondary.

**Required validation**

V0 for UI wiring. Checkpoint B runs targeted manifests and build once.

**Done when**

Humans can download the full collection or individual source packages confidently.

# Phase 7: Strengthen Structured Agent and Technical Access

## Objective

Move machine-oriented detail into better machine surfaces so the visible human page can remain calm without reducing agent capability.

## Task HFDOC-070: Add a static research collection JSON endpoint

**Goal**

Publish a joined, versioned machine-readable description of the ontology collection.

**Context**

Agents currently have multiple manifests but no single endpoint that combines sequence, human guide routes, and file access.

**Dependencies**

HFDOC-010 through HFDOC-014 and HFDOC-040.

**Likely files**

- `src/pages/documents/research/index.json.ts`
- `src/lib/documentPresentation.ts`
- `src/data/documentCollectionPresentation.ts`

**Implementation steps**

1. Create a prerendered Astro endpoint.
2. Include a schema version and collection ID.
3. Include the collection human title and bounded summary.
4. Include fixed/interpretive/open claim-boundary fields.
5. Include all eight documents in canonical order.
6. For each document, include document ID, formal title, display title, question, sequence position, HTML guide, PDF, root TeX, source package when available, role, and machine-record links.
7. Join hashes, revisions, and statuses from existing manifests rather than duplicating them in presentation data.
8. Include a clear `authority_note` that the endpoint is a publication index, not a source of scientific authority.
9. Set an appropriate JSON content type.

**Constraints**

- No network service.
- No runtime database.
- No duplicated uncontrolled status values.
- No new claim authority.

**Acceptance criteria**

- [ ] The endpoint is static and deterministic.
- [ ] All eight records are present in canonical order.
- [ ] Human and raw asset links resolve from one record.
- [ ] Authority note is explicit.

**Required validation**

V0 during coding. Checkpoint B build verifies endpoint generation.

**Done when**

Agents have one clear collection endpoint without requiring visible raw metadata.

## Task HFDOC-071: Add structured page metadata and alternate-format links

**Goal**

Expose document relationships and formats in page markup.

**Context**

Semantic head metadata improves agent and tool discovery without changing the visible page.

**Dependencies**

HFDOC-040 and HFDOC-070.

**Likely files**

- `src/components/documents/DocumentStructuredData.astro`
- `src/layouts/DocumentGuideLayout.astro`
- `src/pages/documents/research/[slug].astro`

**Implementation steps**

1. Add JSON-LD using `CreativeWork` or `ScholarlyArticle` only where the publication status supports that type.
2. Include name, alternate title, abstract, position, collection relation, keywords, URL, license when known, and encodings.
3. Do not claim peer review or external publication unless recorded.
4. Add `<link rel="alternate">` entries for PDF and TeX.
5. Add a machine-readable link to the collection JSON.
6. Ensure JSON serialization escapes content safely.
7. Use source revision as version information only when semantically appropriate.

**Constraints**

- Do not misrepresent website approval as scholarly acceptance.
- Do not expose private paths.
- Do not duplicate full manuscript text in structured data.

**Acceptance criteria**

- [ ] Every guide page exposes PDF and TeX alternates.
- [ ] Structured metadata uses bounded publication language.
- [ ] Collection position is represented.
- [ ] Markup is generated statically.

**Required validation**

V0. Build only at Checkpoint B.

**Done when**

Agents and tools can discover relationships without a special visible mode.

## Task HFDOC-072: Strengthen semantic HTML and stable identifiers

**Goal**

Make human page structure equally useful to assistive technology and agents.

**Context**

Semantic structure is the common layer that supports both audiences.

**Dependencies**

HFDOC-020 through HFDOC-045.

**Likely files**

- `src/components/documents/*.astro`
- `src/pages/documents/research/index.astro`
- `src/pages/documents/research/[slug].astro`

**Implementation steps**

1. Use ordered lists for reading order.
2. Use `<article>` for document guides and cards.
3. Use `<nav>` for sequence navigation.
4. Use `<details>` and `<summary>` for technical disclosure.
5. Use `<dl>` for metadata.
6. Use `<dfn>` where a term is formally defined.
7. Use stable IDs derived from document slugs.
8. Add `data-document-id`, `data-reading-order`, and `data-collection-id` only where useful and not visually exposed.
9. Keep heading levels logical.
10. Ensure title links and action links have clear programmatic context.

**Constraints**

- Do not add hidden keyword stuffing.
- Do not use ARIA where native HTML already supplies the behavior.
- Do not encode scientific authority in data attributes.

**Acceptance criteria**

- [ ] The sequence remains understandable without CSS.
- [ ] Metadata remains a definition list.
- [ ] Guide navigation has a clear accessible name.
- [ ] Stable document IDs are available to tools.

**Required validation**

V0. Manual DOM/source review only.

**Done when**

The same HTML structure serves humans, agents, and assistive technology.

## Task HFDOC-073: Add a concise `llms.txt` orientation file

**Goal**

Provide agents with a simple entry map and authority warning.

**Context**

An orientation file can reduce agent confusion while keeping machine detail out of the human page.

**Dependencies**

HFDOC-070 through HFDOC-072.

**Likely files**

- `public/llms.txt`

**Implementation steps**

1. Describe the website as a reader-facing presentation layer.
2. State that registered sources and governed records retain authority.
3. State that PDFs are reading copies and TeX carries the registered source role for the ontology collection.
4. State the effective-theory and open-derivation boundary in concise language.
5. List the collection HTML route, collection JSON endpoint, and manifest endpoints.
6. List the eight guide routes or point to the collection JSON.
7. State that website summaries and hashes do not strengthen scientific claims.

**Constraints**

- Do not present `llms.txt` as canonical scientific authority.
- Do not include secrets, local paths, or internal control records.
- Keep the file concise.

**Acceptance criteria**

- [ ] The file orients agents to the correct routes.
- [ ] Authority boundaries are explicit.
- [ ] Machine endpoints are discoverable.

**Required validation**

V0. Static text review only.

**Done when**

Agents have a low-friction map that does not burden human navigation.

## Task HFDOC-074: Preserve and reposition existing manifests and technical records

**Goal**

Ensure no machine capability is lost when visible metadata is collapsed.

**Context**

The redesign depends on better separation, not deletion.

**Dependencies**

HFDOC-022, HFDOC-036, and HFDOC-070.

**Likely files**

- `public/files/manifests/document_catalog.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `src/pages/documents/index.astro`
- `src/pages/documents/research/index.astro`

**Implementation steps**

1. Keep all existing manifest endpoints.
2. Keep direct manifest links in a technical records section.
3. Explain the purpose of each manifest in one sentence.
4. Keep hashes and source revisions in manifest data.
5. Confirm bundle records do not alter document-source authority.
6. Do not add a second human/AI interface.
7. Document that structured endpoints are publication aids, not authority promotion.

**Constraints**

- Do not delete or rename manifest paths.
- Do not move technical links so deeply that reviewers cannot find them.
- Do not show them as the primary page action.

**Acceptance criteria**

- [ ] All current machine records remain reachable.
- [ ] Human pages no longer depend on visible raw metadata.
- [ ] Authority language remains clear.

**Required validation**

V2 at Checkpoint B through existing manifest validation.

**Done when**

Agent and reviewer access is preserved while the default UI becomes human-first.

# Phase 8: Accessibility and Lightweight Human-Comprehension Review

## Objective

Ensure the human-first design is usable with keyboard, assistive technology, zoom, and ordinary reader expectations without creating a heavy compliance or test program.

## Task HFDOC-080: Review link purpose, keyboard behavior, and disclosure controls

**Goal**

Confirm that all essential interactions are understandable and keyboard accessible.

**Context**

Descriptive actions and native disclosure are central to the redesign.

**Dependencies**

Phases 2 through 5.

**Likely files**

- `src/components/documents/DocumentFormatActions.astro`
- `src/components/documents/TechnicalProvenanceDisclosure.astro`
- `src/components/documents/DocumentGuideNavigation.astro`
- `src/pages/documents/research/**/*.astro`

**Implementation steps**

1. Tab through the research index and one detail page.
2. Confirm visible focus remains clear.
3. Confirm every repeated action has a distinct accessible name.
4. Confirm the technical disclosure opens and closes with keyboard controls.
5. Confirm the sequence navigation order matches the visual order.
6. Confirm skip-to-content still works.
7. Confirm no essential definition is available only on hover.
8. Confirm download versus open behavior is named.

**Constraints**

- Use a short manual pass only.
- Do not add a large automated accessibility suite unless a real issue justifies it.

**Acceptance criteria**

- [ ] All primary actions are keyboard reachable.
- [ ] Screen-reader link-list labels are distinct by inspection.
- [ ] Native disclosure works.
- [ ] Essential definitions are visible or normally linked.

**Required validation**

V0 manual check. Record only failures and fixes; no formal report is required.

**Done when**

Core document interactions are accessible without new testing infrastructure.

## Task HFDOC-081: Review plain language and progressive disclosure

**Goal**

Confirm that human explanation precedes specialist detail and terminology is defined.

**Context**

The product goal is comprehension, not merely visual rearrangement.

**Dependencies**

HFDOC-030 through HFDOC-054.

**Likely files**

- `src/pages/documents/index.astro`
- `src/pages/documents/research/index.astro`
- `src/pages/documents/research/[slug].astro`
- `src/pages/documents/anthology/index.astro`
- `src/data/documentGlossary.ts`

**Implementation steps**

1. Read each page from top to bottom as a new reader.
2. Confirm exact closure is defined before the sequence.
3. Confirm adoption and derivation are not conflated.
4. Confirm publication approval and scientific scope are separate.
5. Confirm hashes, paths, and commits are collapsed.
6. Confirm glossary terms are available near first use.
7. Confirm the page does not require understanding `manifestation`, `authority scope`, or raw status values.
8. Confirm technical records remain discoverable.

**Constraints**

- No readability scoring tool is required.
- No automated jargon test is required.
- Do not simplify away scientific qualifications.

**Acceptance criteria**

- [ ] Core concepts are explained in ordinary language.
- [ ] Technical detail is progressively disclosed.
- [ ] No critical qualification is hidden.
- [ ] Specialist records remain available.

**Required validation**

V0 manual copy pass.

**Done when**

The page's information order matches the human-first contract.

## Task HFDOC-082: Provide an HTML accessibility fallback and record PDF limitations

**Goal**

Make essential orientation available in HTML and avoid overclaiming PDF accessibility.

**Context**

The website may not be authorized to rewrite upstream TeX or PDF generation. HTML guides provide a practical accessible route.

**Dependencies**

HFDOC-040 through HFDOC-045.

**Likely files**

- `src/pages/documents/research/[slug].astro`
- `optional docs/quality/ontology-pdf-accessibility-notes.md`
- `public PDF assets`

**Implementation steps**

1. Treat the HTML guide as the primary accessible orientation surface.
2. Perform a light manual inventory of each PDF: text selectable, title present if observable, obvious heading/bookmark behavior, obvious reading-order problems, and major figures.
3. Record only known limitations and remediation ownership.
4. Do not claim formal PDF accessibility conformance.
5. Where a PDF has a known problem, keep the HTML guide prominent and add a concise accessibility note.
6. Route source-level PDF remediation to the authorized upstream process rather than silently editing generated outputs.

**Constraints**

- No exhaustive PDF/UA audit is required in this plan.
- No repeated tool-based certification is required.
- Do not publish unsupported compliance claims.

**Acceptance criteria**

- [ ] Every paper has an HTML orientation alternative.
- [ ] Known major PDF limitations are documented if found.
- [ ] Accessibility wording is honest.
- [ ] Upstream remediation ownership is clear.

**Required validation**

V0 light manual inventory only.

**Done when**

Readers are not forced to rely on a raw PDF for basic orientation.

## Task HFDOC-083: Review responsive layout, zoom, and navigation labels

**Goal**

Confirm the new hierarchy survives narrow screens and enlarged text.

**Context**

The removal of the metadata side rail should improve reflow, but it needs a small visual check.

**Dependencies**

HFDOC-025 and HFDOC-051.

**Likely files**

- `src/styles/global.css`
- `src/components/documents/*.astro`
- `src/lib/siteContent.ts`

**Implementation steps**

1. Check the research index at a standard desktop width.
2. Check at approximately 320 CSS pixels.
3. Check at 200 percent browser zoom.
4. Open the global Library/Documents menu on desktop and compact navigation.
5. Confirm actions stack without clipping.
6. Confirm long technical values do not widen the page before or after disclosure.
7. Confirm page titles and navigation labels remain readable.
8. Confirm no horizontal page scroll is introduced by document cards.

**Constraints**

- Use one browser only unless a defect appears.
- Do not create a multi-browser matrix.
- Do not add screenshot regression tooling.

**Acceptance criteria**

- [ ] Cards reflow to one column.
- [ ] Actions remain usable.
- [ ] Technical values are contained.
- [ ] Navigation labels work in compact mode.

**Required validation**

V0 short manual visual check.

**Done when**

The reader experience remains usable at narrow width and zoom.

## Task HFDOC-084: Perform one lightweight human comprehension check

**Goal**

Verify that the redesign actually reduces conceptual confusion.

**Context**

Automated checks cannot determine whether a person understands exact closure or the reading order.

**Dependencies**

HFDOC-030 through HFDOC-083.

**Likely files**

- `optional docs/quality/document-library-human-review.md`
- `production-like local preview or built static output`

**Implementation steps**

1. Ask one to three people unfamiliar with the implementation, or one maintainer deliberately acting as a first-time reader, to complete five tasks.
2. Tasks: find the starting paper; explain exact closure; state whether GR has been derived from substrate physics; open the overview PDF; find the Foundations TeX or source package.
3. Record only blocking misunderstandings and concise observations.
4. Fix wording or hierarchy when multiple tasks fail for the same reason.
5. Do not turn this into a recurring research program.
6. Do not require statistical targets for the first release.

**Constraints**

- Keep the session short.
- Do not collect sensitive personal information.
- Do not claim population-level usability conclusions.

**Acceptance criteria**

- [ ] The starting paper can be found.
- [ ] The participant distinguishes effective GR adoption from open derivation.
- [ ] The participant can access PDF and TeX.
- [ ] Any blocking confusion is repaired or explicitly accepted.

**Required validation**

One short manual comprehension pass. No automated usability tooling.

**Done when**

The human-first goal has at least one direct reality check.

# Phase 9: Minimal Validation, Documentation, and Release Handoff

## Objective

Run only the checks required to establish that the static site and new assets are coherent, then hand off without automatic deployment.

## Task HFDOC-090: Run grouped Checkpoint A for pages and components

**Goal**

Verify that the human presentation data, shared components, collection page, detail pages, overview, navigation, and anthology build together.

**Context**

Running a build after every task would create unnecessary overhead. One grouped build is sufficient after Phases 1 through 5.

**Dependencies**

Phases 1 through 5 complete.

**Likely files**

- `package.json`
- `all changed src/ files`

**Implementation steps**

1. Run `npm run build` once.
2. Fix only build failures, missing static routes, broken imports, or invalid Astro markup.
3. Open the built research index, one detail page, the library overview, and the anthology route.
4. Confirm direct PDF and TeX links are present.
5. Record the command result.

**Constraints**

- Do not run the full quality gate at this checkpoint.
- Do not add tests to fix a simple build error.

**Acceptance criteria**

- [ ] The static build succeeds.
- [ ] Eight guide pages are generated.
- [ ] Core routes render.
- [ ] Direct document links are present.

**Required validation**

`npm run build` once.

**Done when**

The human-first site slice builds as static Astro output.

## Task HFDOC-091: Update route maps, page provenance, manifests, and maintainer notes

**Goal**

Bring repository records into alignment after routes, pages, and bundles are final.

**Context**

Page hashes and asset manifests must reflect the final implementation, but updates should occur once rather than after every edit.

**Dependencies**

HFDOC-064 through HFDOC-074 and HFDOC-090.

**Likely files**

- `public/files/manifests/page_route_map.json`
- `public/files/manifests/page_provenance.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `docs or README maintainer notes`
- `PROJECT_FEATURES_AND_FUNCTIONALITY.md if required by project practice`

**Implementation steps**

1. Add detail-page route mappings if the route map records generated routes.
2. Update page provenance hashes only after page copy is final.
3. Add bundle source and asset records.
4. Document the new reader-profile and bundle-generation files.
5. Document that canonical raw PDF and TeX paths remain unchanged.
6. Document the human-first versus machine-layer boundary.
7. Remove stale statements that say the Research Articles page is primarily source-oriented if no longer true.
8. Do not change upstream scientific records.

**Constraints**

- Do not churn unrelated manifest entries.
- Do not regenerate records repeatedly during content drafting.
- Do not treat provenance update as scientific approval.

**Acceptance criteria**

- [ ] New pages and bundles are represented where required.
- [ ] Hashes correspond to final page output.
- [ ] Maintainer documentation explains the new architecture.
- [ ] Unrelated records are preserved.

**Required validation**

V2 grouped Checkpoint B: run `npm run validate:manifests` once, followed by `npm run build` once.

**Done when**

Repository metadata and static output agree with the final human-first implementation.

## Task HFDOC-092: Run one final aggregate repository validation when release is authorized

**Goal**

Satisfy the repository definition of done without repeated full-suite execution.

**Context**

The project expects aggregate validation for release readiness. The user has requested minimal overhead, so this occurs only once.

**Dependencies**

HFDOC-091 and release authorization.

**Likely files**

- `package.json`
- `validation output record`

**Implementation steps**

1. Run `npm run validate` once before an authorized commit/push/deployment or when the repository task contract requires it.
2. Do not run `npm run quality` unless a real issue, repository rule, or explicit release instruction requires it.
3. Record any skipped check and the concrete reason.
4. Fix only failures caused by this implementation.
5. If the aggregate command exposes unrelated pre-existing failures, record them separately rather than expanding scope silently.

**Constraints**

- Do not claim pass without command evidence.
- Do not repeat the full command after nonfunctional copy changes unless necessary.
- Do not deploy automatically after a pass.

**Acceptance criteria**

- [ ] The aggregate validation passes or all remaining failures are accurately classified.
- [ ] Skipped checks are named.
- [ ] Release remains a separate decision.

**Required validation**

`npm run validate` once, only at final release readiness.

**Done when**

The implementation has one bounded aggregate verification record.

## Task HFDOC-093: Prepare rollout, rollback, and post-release spot check

**Goal**

Make the change reversible and ensure the production site exposes the intended human paths after a separately authorized release.

**Context**

The site is static and routes remain stable, so rollback can be straightforward.

**Dependencies**

HFDOC-092 and separate release authorization.

**Likely files**

- `release notes`
- `deployment record`
- `changed source files and manifests`

**Implementation steps**

1. Summarize visible changes, new routes, new bundle paths, and preserved raw asset paths.
2. Record that no upstream scientific source was changed.
3. Record rollback units: navigation labels, page/component commits, reader-profile data, bundle records, and static bundle files.
4. If deployment is authorized, perform a short production spot check on `/documents/`, `/documents/research/`, the overview guide, and `/documents/anthology/`.
5. Open one PDF and one TeX or source-package action.
6. Confirm the collection JSON endpoint if published.
7. Do not perform broad production crawling.

**Constraints**

- Deployment requires separate authorization.
- Rollback must remove matching manifest records when bundle files are removed.
- Do not leave visible links to removed assets.

**Acceptance criteria**

- [ ] Release notes explain the new human-first architecture.
- [ ] Rollback steps are concrete.
- [ ] Production spot check, if authorized, covers the primary human journey only.
- [ ] No external effect is implied by plan completion.

**Required validation**

Four-route and two-file production spot check only after deployment.

**Done when**

The implementation can be released or reverted without ambiguity.

---

# Appendix A: Approved Draft Copy Deck

The following copy is implementation-ready but still requires the normal project source-boundary review before publication.

## A.1 Research collection hero

**Eyebrow**

```text
Library / Ontology Papers
```

**Title**

```text
AEther Flow Ontology Papers
```

**Lead**

```text
Eight connected papers explain the project's ontology, its exact
GR-compatible effective theory, and the still-open question of whether
that theory can be derived from deeper substrate physics.
```

**Primary actions**

```text
Start with the overview
Browse all 8 papers
```

**Supporting sentence**

```text
Every paper is available as a PDF for reading. Registered TeX manuscripts
are available for technical inspection, and complete source packages are
provided where all required dependencies have been published.
```

## A.2 Key information summary

```text
Key information

• Begin with "Exact Closure: Overview and Reading Guide."
• The current observer-level theory uses the equations and predictions of
  general relativity.
• The AEther and AEther-flow vocabulary remains interpretive at the
  effective level.
• A first-principles derivation from deeper substrate dynamics remains open.
• All eight papers are available as PDFs and registered TeX manuscripts.
```

## A.3 Exact closure definition

```text
Exact closure, as used by this project, means that the observer-level
theory is explicitly fixed to general relativity within the stated scope.
The gravitational equations, matter coupling, light propagation, clocks,
redshift, and observable predictions remain those of GR. AEther and
AEther-flow are retained as an ontology or interpretation. Exact closure
does not mean that GR has already been derived from deeper substrate
physics, and it does not claim a new verified low-energy force, particle,
or gravitational law.
```

## A.4 Fixed, interpretive, and open

### What is fixed

```text
The effective observer-level theory uses general relativity.
```

### What is interpretive

```text
The AEther and AEther-flow vocabulary proposes a way to interpret what may
underlie observed spacetime and ordered motion.
```

### What remains open

```text
The project has not yet completed a first-principles derivation of GR from
explicit deeper substrate variables and laws.
```

## A.5 Adoption and derivation

```text
Adoption means using the established equations of general relativity as
the effective theory.

Derivation means recovering those equations from explicit deeper variables
and laws without assuming the target equations in advance.
```

## A.6 Featured overview card

```text
START HERE · PAPER 1 OF 8

Exact Closure: Overview and Reading Guide
Formal manuscript title: Exact Closure Sequence Overview

This overview explains how the eight ontology papers fit together. It
states the project's current effective-theory position, separates adopted
GR dynamics from the open substrate-derivation program, and tells you which
papers to read next.

What you will learn
• What "exact closure" means in this project.
• Why the observer-level theory currently matches GR.
• What remains open at the substrate level.
• How the other seven papers fit into the complete argument.

Read Exact Closure Overview (PDF)
Download Exact Closure Overview (PDF)
View registered root TeX manuscript
Download Exact Closure Overview source package
```

The source-package action appears only when the package exists.

## A.7 PDF explanation

```text
PDF is the best format for reading, printing, and sharing the fixed-layout
paper. The PDF is generated from the registered TeX manuscript and does not
replace the source role recorded for that manuscript.
```

## A.8 TeX root explanation

```text
The registered root TeX manuscript is published for source inspection. It
may reference shared TeX files that are not included in the individual
root-file download, so the root file may not compile by itself.
```

## A.9 Source package explanation

```text
A TeX source package includes the root manuscript and the published shared
files required by that manuscript. The page states whether compilation has
been confirmed.
```

## A.10 Website publication status

```text
Reviewed and approved for public access on this website.
```

## A.11 Scientific scope status

```text
Uses general relativity as the observer-level effective theory. A deeper
substrate derivation remains open.
```

## A.12 SHA-256 explanation

```text
A SHA-256 value is a file verification code. Most readers do not need it.
Technical reviewers can compare it with a downloaded file to confirm that
the file is byte-for-byte identical to the published copy. It does not
verify that the scientific claims are correct.
```

## A.13 Library overview hero

**Title**

```text
Research Library
```

**Lead**

```text
Choose a starting point based on what you want to understand. The library
includes plain-language explanations, the eight ontology papers, diagrams,
and technical source and governance records.
```

## A.14 Library reader-intention cards

### I am new to the project

```text
Begin with a plain explanation of the AEther-flow ontology and the
distinction between the project's current GR-compatible effective theory
and its open substrate-derivation research.
```

Action:

```text
Start with the ontology
```

### I want to read the research papers

```text
Browse the eight-paper ontology collection in its recommended order. Every
paper is available as a PDF, and source files are available for technical
inspection.
```

Action:

```text
Browse the ontology papers
```

### I want a visual explanation

```text
Explore diagrams that distinguish ontology, effective theory, derivation,
benchmark behavior, and claim boundaries.
```

Action:

```text
Browse diagrams
```

### I am reviewing the project

```text
Inspect claim status, source authority, research governance, publication
records, and technical provenance.
```

Action:

```text
Open the reviewer path
```

### I need machine-readable records

```text
Access document manifests, source records, file hashes, and structured
collection data.
```

Action:

```text
Open technical records
```

## A.15 Anthology empty state

**Title**

```text
Plain-Language Articles
```

**Empty message**

```text
No plain-language articles are currently published in this collection.
```

**Supporting copy**

```text
The ontology research library already contains eight papers in PDF and TeX
formats. Begin there to read the current scientific collection.
```

**Actions**

```text
Browse ontology papers
Start with the exact-closure overview
Explore the ontology explanation
```

**Secondary disclosure**

```text
How publication works
```

---

# Appendix B: Eight-Paper Human Reading Model

## B.1 Paper 1

**Formal title:** Exact Closure Sequence Overview  
**Display title:** Exact Closure: Overview and Reading Guide  
**Reader question:** What is the complete package, and what remains unfinished?  
**Role:** Start here.  
**Summary:** This overview explains how the eight ontology papers fit together. It states that the project currently uses the equations and observable predictions of general relativity while retaining AEther and AEther-flow as an interpretation of what may underlie them. It distinguishes this adopted effective theory from the still-open attempt to derive GR from deeper substrate physics.  

**What the reader learns:**

- The meaning of exact closure.
- The reading order.
- The distinction between adoption and derivation.
- The project-wide claim boundary.
- The role of the final flagship synthesis.

**Does not establish:**

- A completed first-principles substrate derivation.
- A unique underlying substrate action.
- A verified low-energy departure from GR.
- Empirical confirmation of the ontology.

## B.2 Paper 2

**Formal title:** Exact Closure Note  
**Display title:** Exact Closure: Short Statement  
**Reader question:** What is the shortest complete statement of the current physics position?  
**Role:** Compact anchor after the overview.  
**Summary:** This note gives the shortest standalone statement of the active exact-closure position. It identifies the adopted observer-level GR dynamics and the explicit nonclaims that keep the deeper substrate program separate.  

**What the reader learns:**

- The shortest current theory statement.
- Which claims are adopted at effective scope.
- Which stronger derivational claims remain unavailable.

**Does not establish:**

- New observer-level field equations.
- A completed substrate derivation.
- Independent empirical support for the ontology.

## B.3 Paper 3

**Formal title:** Foundations  
**Display title:** Foundations  
**Reader question:** What do AEther and AEther-flow mean in this framework?  
**Role:** Ontological foundation of the ordered core.  
**Summary:** This paper defines the project's ontological vocabulary, explains the original framework intent, and clarifies why exact closure is the current active stance.  

**What the reader learns:**

- The meaning of AEther.
- The meaning of AEther-flow.
- The relation among observed space, S-time, expansion language, and the deeper ontology.
- Why ontology and effective dynamics must be kept distinct.

**Does not establish:**

- The metric field equations from ontology alone.
- A direct experimental observation of the proposed substrate.
- A replacement for the dynamics paper.

## B.4 Paper 4

**Formal title:** Dynamics  
**Display title:** Dynamics  
**Reader question:** Which equations govern the effective theory?  
**Role:** Effective equations and matter coupling.  
**Summary:** This paper states the adopted effective action, Einstein field equations, universal matter coupling, weak-field structure, and benchmark role used by the exact-closure package.  

**What the reader learns:**

- The operative action.
- The observer-level field equations.
- How matter couples.
- Why the active benchmark remains GR.

**Does not establish:**

- That the Einstein action has been derived from substrate variables.
- A second operative metric.
- Additional verified low-energy gravitational modes.

## B.5 Paper 5

**Formal title:** Consistency  
**Display title:** Consistency  
**Reader question:** Does the adopted effective theory introduce extra modes or instabilities?  
**Role:** Effective health and constraint structure.  
**Summary:** This paper examines gauge structure, degrees of freedom, and effective health conditions inherited from the adopted GR sector.  

**What the reader learns:**

- The role of diffeomorphism gauge structure.
- The expected degree-of-freedom count.
- Why the adopted effective theory does not add a separate observer-level scalar or vector graviton sector.

**Does not establish:**

- The consistency of every possible future substrate model.
- A proof that all microscopic completions are healthy.
- A completed derivation of the adopted constraints from substrate dynamics.

## B.6 Paper 6

**Formal title:** Relativistic Recovery  
**Display title:** Relativistic Recovery  
**Reader question:** How does familiar relativistic behavior appear in the framework?  
**Role:** Relation to GR and local special relativity.  
**Summary:** This paper explains the exact observer-level relation to general relativity and the local relation to special relativity, including light propagation, redshift, clocks, and inertial structure.  

**What the reader learns:**

- How null propagation is treated.
- How proper time and clocks are treated.
- How redshift and local inertial behavior follow the operative metric.
- Why the observable sector remains the GR sector.

**Does not establish:**

- A new verified deviation in light propagation.
- A second clock law.
- A completed substrate derivation of relativistic behavior.

## B.7 Paper 7

**Formal title:** Flow Geometry  
**Display title:** Flow Geometry  
**Reader question:** How is the language of flow represented in relativistic geometry?  
**Role:** Formal geometric dictionary for the interpretation.  
**Summary:** This paper uses congruence-based relativistic geometry to give disciplined meaning to AEther-flow language without introducing a second low-energy gravitational law.  

**What the reader learns:**

- The role of congruences.
- How expansion, shear, acceleration, and related geometric quantities organize the flow interpretation.
- Why flow language is not a simple wind through space.

**Does not establish:**

- A new preferred-frame field with independent observer-level dynamics.
- A fluid medium inside ordinary three-dimensional space.
- A completed microscopic substrate law.

## B.8 Paper 8

**Formal title:** Exact Closure Flagship Article  
**Display title:** Exact Closure: Public Synthesis  
**Reader question:** How does the complete package read as one public-facing synthesis?  
**Role:** Final synthesis after the ordered core.  
**Summary:** This article presents the exact-closure package as a coherent public-facing argument after the overview and six-paper core. It summarizes the ontology, adopted dynamics, consistency, relativistic behavior, geometric interpretation, and remaining open derivation question.  

**What the reader learns:**

- How the complete package is communicated as one narrative.
- How the modules support the final synthesis.
- Why the active theory is operationally GR at observer scale.
- Why deeper derivation remains downstream.

**Does not establish:**

- Higher source authority than the overview or root papers.
- A changed reading order.
- A completed substrate derivation.
- A new observer-level departure from GR.

# Appendix C: Bundle Layouts

## C.1 PDF collection archive

```text
aether-flow-ontology-papers-pdf.zip
├── 00-README.md
├── 01-exact-closure-overview.pdf
├── 02-exact-closure-note.pdf
├── 03-foundations.pdf
├── 04-dynamics.pdf
├── 05-consistency.pdf
├── 06-relativistic-recovery.pdf
├── 07-flow-geometry.pdf
├── 08-exact-closure-flagship-article.pdf
├── manifest.json
└── LICENSE.txt
```

## C.2 Full TeX source archive

```text
aether-flow-ontology-tex-source.zip
├── README.md
├── LICENSE.txt
├── manifest.json
└── ontology
    └── tex
        ├── aether_flow_exact_closure_sequence_overview.tex
        ├── aether_flow_exact_closure_note.tex
        ├── aether_flow_foundations.tex
        ├── aether_flow_dynamics.tex
        ├── aether_flow_consistency.tex
        ├── aether_flow_relativistic_recovery.tex
        ├── aether_flow_geometry.tex
        ├── aether_flow_exact_closure_flagship_article.tex
        └── tex_shared
            └── [all declared approved shared dependencies]
```

## C.3 Bundle manifest example

```json
{
  "schema_version": 1,
  "bundle_id": "canonical-ontology-pdf-collection",
  "title": "AEther Flow Ontology Papers: PDF Collection",
  "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "source_revision": "<upstream revision>",
  "authority_note": "This archive is a publication bundle. Source roles remain recorded in the source manifest.",
  "items": [
    {
      "document_id": "research:aether-flow-exact-closure-sequence-overview",
      "reading_order": 1,
      "archive_path": "01-exact-closure-overview.pdf",
      "public_source_path": "/files/pdf/ontology/aether_flow_exact_closure_sequence_overview.pdf",
      "sha256": "<hash>",
      "bytes": 224206
    }
  ]
}
```

## C.4 Per-paper source package example

```text
exact-closure-overview-source.zip
├── README.md
├── manifest.json
├── aether_flow_exact_closure_sequence_overview.tex
└── tex_shared
    ├── aether_flow_apa_frontmatter.tex
    ├── aether_flow_what_this_package_is_not.tex
    ├── aether_flow_product_a_references_apa.tex
    └── [other transitive dependencies]
```

---

# Appendix D: Technical Provenance Disclosure Example

```html
<details class="technical-provenance">
  <summary>Technical provenance and file verification</summary>

  <section aria-labelledby="registered-source-title">
    <h4 id="registered-source-title">Registered source</h4>
    <dl>
      <div>
        <dt>Source role</dt>
        <dd>Registered TeX manuscript</dd>
      </div>
      <div>
        <dt>Source revision</dt>
        <dd><code>...</code></dd>
      </div>
      <div>
        <dt>Source path</dt>
        <dd><code>...</code></dd>
      </div>
    </dl>
  </section>

  <section aria-labelledby="pdf-copy-title">
    <h4 id="pdf-copy-title">PDF reading copy</h4>
    <p>
      The PDF is generated from the registered TeX manuscript. The
      verification code confirms file identity, not scientific correctness.
    </p>
    <dl>
      <div>
        <dt>Exact file size</dt>
        <dd>224,206 bytes</dd>
      </div>
      <div>
        <dt>Website copy synchronized</dt>
        <dd>July 12, 2026</dd>
      </div>
      <div>
        <dt>SHA-256 file verification code</dt>
        <dd><code>...</code></dd>
      </div>
    </dl>
  </section>
</details>
```

---

# Appendix E: Minimal Manual Review Script

This is the complete required manual review. It is intentionally small.

## E.1 Human journey

1. Open `/documents/`.
2. Find the ontology paper collection.
3. Open `/documents/research/`.
4. Identify the recommended first paper.
5. Explain exact closure in one sentence.
6. State whether the project claims a completed substrate derivation.
7. Open the overview PDF.
8. Find the Foundations TeX root or source package.
9. Open technical provenance for one paper.
10. Return to the collection using sequence navigation.

## E.2 Keyboard and responsive spot check

1. Use Tab and Shift+Tab through the primary actions.
2. Open and close one technical disclosure.
3. Open and close the global Library/Documents menu.
4. Check one page at approximately 320 CSS pixels.
5. Check one page at 200 percent zoom.
6. Confirm no page-wide horizontal scroll appears.

## E.3 Required outcome

- The start paper is obvious.
- Exact closure is understood as bounded effective GR closure, not completed substrate derivation.
- PDF and TeX are easy to find.
- TeX package status is truthful.
- Technical metadata is available but not visually dominant.

No formal usability report, statistical sample, accessibility certification, or recurring test suite is required.

---

# Appendix F: Lean Validation Policy

## F.1 Validation levels

### V0: No command

Use for:

- Copy drafting.
- Data-model drafting.
- Source-to-summary review.
- Semantic markup review.
- Manual keyboard and responsive checks.

### V1: Grouped static build

Run once after Phases 1 through 5:

```bash
npm run build
```

### V2: Targeted manifest and bundle check

Run once after Phases 6 and 7:

```bash
npm run validate:manifests
npm run build
```

### V3: Final aggregate release check

Run once only before an authorized release:

```bash
npm run validate
```

## F.2 Explicitly not required by this plan

- New unit tests.
- New Playwright suite.
- New Axe dependency.
- Screenshot regression tests.
- Multi-browser matrix.
- Full PDF/UA audit.
- Repeated TeX compilation in CI.
- `npm run quality` after every phase.
- Full validation after every task.
- Automated readability scoring.
- A new analytics or observability system.

## F.3 Conditional checks

- One manual TeX batch compilation is required only before using the word `compilable`.
- Additional browser or accessibility checks are required only when the short manual review reveals a concrete defect.
- `npm run quality` may be run if explicitly required by the release owner or if the aggregate validation indicates a visual or asset issue not covered elsewhere.

# Appendix G: Risk Register

| Risk | Consequence | Mitigation |
|---|---|---|
| Human summary strengthens a source claim | Scientific misrepresentation | Require source-basis references and review status in each profile |
| Exact closure remains ambiguous | Core usability goal fails | Use the fixed/interpretive/open model and explicit adoption/derivation definitions |
| TeX package is incomplete | Reader download fails to compile | Dependency audit, truthful labels, fail-closed bundle generation |
| Navigation label conflicts with prior plan | Governance or consistency issue | Record one label decision in HFDOC-002; keep routes unchanged |
| Metadata becomes too hidden | Reviewers lose access | Use native technical disclosure and dedicated technical-record sections |
| Metadata remains too prominent | Human-first goal fails | Keep hashes, paths, commits, and exact bytes collapsed by default |
| Detail pages drift from manuscripts | Misinformation | Source-basis references and build-time one-profile-per-document assertions |
| Bundle generation publishes unrelated files | Privacy or governance breach | Allowlisted dependency roots and path traversal prevention |
| Empty anthology looks abandoned | Reader confusion | Immediate honest empty state and direct next actions |
| HTML guide is mistaken for source authority | Authority confusion | Visible source-role note and structured authority note |
| Structured JSON becomes a second uncontrolled truth | Data drift | Generate from joined existing catalog, manifest, and reviewed presentation data |
| Page becomes excessively long | Reader fatigue | Featured start, narrative sequence, concise cards, and progressive disclosure |
| Validation expands uncontrollably | Implementation overhead | Fixed validation budget and grouped commands only |
| Full PDF accessibility cannot be proven | Overclaiming | Provide HTML alternatives and record only known limitations |
| Bundle files break old direct links | Access regression | Preserve all existing raw file URLs |
| New routes create provenance drift | Repository validation failure | Update route map and page provenance once after copy is final |
| Reader profiles become a shadow source | Authority and maintenance drift | Keep formal status and hashes out of profile data; join from manifests |
| `Library` label is rejected by governance | Minor IA rework | Retain `Documents` as allowed fallback while preserving all human-first child labels |
| Anthology remains empty for a long period | Navigation dead end | Keep explicit no-content description and direct routes to populated collections |
| Source package size grows | Slower downloads | Offer collection and per-paper packages; show humanized archive sizes |
| Agent orientation is overinterpreted | Incorrect authority inference | Put authority notes in JSON and `llms.txt`; link to source-authority route |

---

# Appendix H: Rollout and Rollback

## H.1 Rollout order

1. Merge presentation data and components.
2. Merge research index and guide pages.
3. Merge library overview, navigation labels, and anthology changes.
4. Merge bundle generation and published archives.
5. Merge collection JSON, structured metadata, and `llms.txt`.
6. Update manifests and provenance.
7. Run final release check once.
8. Deploy only with separate authorization.

## H.2 Rollback units

The implementation should remain separable into reversible units:

- Reader profile data.
- Reader card and disclosure components.
- Research index copy and layout.
- Detail guide routes.
- Library/navigation copy.
- Anthology empty-state copy.
- Bundle script and files.
- Bundle manifest records.
- JSON endpoint and structured metadata.
- Provenance updates.

If bundles are rolled back:

- Remove bundle links.
- Remove matching source and asset manifest rows.
- Remove bundle files.
- Preserve direct PDF and root TeX links.

If navigation labels are rolled back:

- Restore the previous visible labels.
- Keep canonical `/documents/` routes.
- Do not remove human guide pages solely because the top-level label changes.

If guide routes are rolled back:

- Restore collection-card titles to direct PDF or existing page anchors.
- Preserve raw PDF and TeX assets.
- Remove corresponding page-route and provenance records.
- Do not remove reader-profile data if another surface still uses it.

## H.3 Staged publication option

If the implementation owner wants the lowest-risk rollout, publish in two visible stages:

### Stage 1

- Human presentation data.
- Reader-first cards.
- Research index rewrite.
- Paper guide pages.
- Library and anthology rewrites.
- Direct existing PDF and root TeX access.

### Stage 2

- PDF collection archive.
- Complete TeX collection archive.
- Per-paper source packages.
- Collection JSON.
- Structured metadata and `llms.txt`.

Stage 1 already solves the primary human-comprehension problem. Stage 2 improves convenience and agent access without blocking the core redesign.

---

# Appendix I: Final Definition of Done

The human-first document-library program is complete when:

- [ ] `/documents/` routes readers by intent before explaining formats and manifests.
- [ ] `/documents/research/` clearly identifies the eight-paper ontology collection.
- [ ] Exact closure is defined before the reading sequence.
- [ ] Adoption and derivation are separately explained.
- [ ] The page states what is fixed, interpretive, and open.
- [ ] The Exact Closure Sequence Overview is clearly marked as the starting paper.
- [ ] All eight papers have human questions and summaries.
- [ ] All eight papers have distinct PDF read actions.
- [ ] All eight root TeX files remain directly accessible.
- [ ] TeX labels truthfully describe root-only or package status.
- [ ] Every paper has an HTML guide page.
- [ ] Every guide shows what the paper establishes and does not establish.
- [ ] Previous and next sequence navigation is correct.
- [ ] Raw hashes, paths, commits, and exact bytes are collapsed by default.
- [ ] Technical provenance remains available.
- [ ] Publication approval is not presented as scientific proof.
- [ ] File sizes and dates are humanized in visible copy.
- [ ] The anthology empty state is immediate and useful.
- [ ] The all-PDF bundle is available or explicitly deferred with no false action.
- [ ] The full TeX package includes declared dependencies or is explicitly blocked.
- [ ] Per-paper source packages are available where safely generated.
- [ ] Existing raw PDF and TeX URLs remain stable.
- [ ] The collection JSON endpoint represents all eight papers in order.
- [ ] Guide pages expose alternate PDF and TeX formats.
- [ ] Existing manifests remain available.
- [ ] `llms.txt` or equivalent agent orientation is bounded and nonauthoritative.
- [ ] Keyboard and narrow-screen spot checks pass.
- [ ] One lightweight human comprehension check is complete.
- [ ] Checkpoint A build has passed.
- [ ] Checkpoint B manifest validation and build have passed when bundles are included.
- [ ] One final aggregate validation has passed or skipped checks are recorded before release.
- [ ] Commit, push, and deployment remain separately authorized.

---

# Appendix J: Repository Evidence and References

The AEther Flow Website. (2026). `AGENTS.md` [Repository instructions].

The AEther Flow Website. (2026). `SOUL.md` [Repository instructions].

The AEther Flow Website. (2026). `ImplementationPlans/aether-flow-documents-navigation-implementation-plan.md` [Implementation plan].

The AEther Flow Website. (2026). `src/pages/documents/index.astro` [Website source].

The AEther Flow Website. (2026). `src/pages/documents/anthology/index.astro` [Website source].

The AEther Flow Website. (2026). `src/pages/documents/research/index.astro` [Website source].

The AEther Flow Website. (2026). `src/pages/physics/ontology/index.astro` [Website source].

The AEther Flow Website. (2026). `src/components/documents/DocumentCollection.astro` [Website component].

The AEther Flow Website. (2026). `src/components/documents/DocumentCard.astro` [Website component].

The AEther Flow Website. (2026). `src/components/documents/DocumentActions.astro` [Website component].

The AEther Flow Website. (2026). `src/components/documents/DocumentMetadata.astro` [Website component].

The AEther Flow Website. (2026). `src/components/StatusDossier.astro` [Website component].

The AEther Flow Website. (2026). `src/components/ComprehensionBlocks.astro` [Website component].

The AEther Flow Website. (2026). `src/lib/documents.ts` [Document model].

The AEther Flow Website. (2026). `src/lib/manifests.ts` [Manifest model and canonical ontology sequence].

The AEther Flow Website. (2026). `src/lib/siteContent.ts` [Navigation and public content data].

The AEther Flow Website. (2026). `src/styles/global.css` [Website stylesheet].

The AEther Flow Website. (2026). `public/files/manifests/document_catalog.json` [Public document catalog].

The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json` [Public source manifest].

The AEther Flow Website. (2026). `public/files/manifests/asset_manifest.json` [Public asset manifest].

The AEther Flow Website. (2026). `scripts/import_ontology_assets.py` [Ontology import script].

The AEther Flow Website. (2026). `scripts/validate_document_catalog.py` [Document catalog validator].

The AEther Flow Website. (2026). `scripts/quality_gate.py` [Static quality gate].

The AEther Flow Website. (2026). `package.json` [Build and validation commands].

The AEther Flow Project. (2026). `ontology/tex/aether_flow_exact_closure_sequence_overview.tex` [Registered ontology manuscript, published website copy].

---

## Plan Completion Record

**Planning status:** Ready with implementation assumptions.  
**Blocking product questions:** None.  
**Primary assumption:** Canonical routes remain `/documents/.../`; visible labels may be humanized.  
**Validation posture:** Deliberately lean.  
**Scientific-source mutation:** Not authorized.  
**Commit, push, deployment:** Not authorized by this plan.

