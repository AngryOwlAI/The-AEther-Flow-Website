# Frontend Audit Recommendations: Comprehensive Implementation Plan

## 1. Document control

| Field | Value |
| --- | --- |
| Plan ID | FE-RECOMMENDATIONS-20260711 |
| Requested output | ImplementationPlans/recomendation_frontend.md |
| Planning date | 2026-07-11 |
| Planning status | Implementation-ready after the gates in this document are opened and satisfied |
| Audit basis | Frontend audit supplied by the project owner on 2026-07-11 |
| Website baseline inspected | main at 0be823a, aligned with origin/main |
| Upstream source baseline observed | /Volumes/P-SSD/AngryOwl/The-AEther-Flow at a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0, clean and aligned with origin/main at planning time |
| Framework | Astro 7 static site, TypeScript/Astro components, CSS, Python validators, Playwright development dependency |
| Primary audience | First-time public readers, followed by specialists, reviewers, contributors, and maintainers |
| Source authority | The tracked upstream research repository, registered TeX sources, registries, and governed records |
| Website authority | Reader-facing explanation, organization, promotion, and provenance only |
| Upstream writes | Forbidden by this plan |
| Deployment | Not authorized by this plan |
| Git push | Not authorized by this plan |
| Scientific promotion | Not authorized by this plan |
| Recommended execution model | One bounded implementation-control packet at a time, with validation and checkpoint evidence after every packet |

### 1.1 Planning-only boundary

This document is a detailed implementation roadmap. It does not itself open a
website implementation packet, authorize a public claim, authorize a source
refresh, approve a font or third-party service, approve route retirement,
authorize GitHub publication, or authorize Cloudflare deployment.

At the time of planning, the live implementation-control resolver reports an
unrelated active skill-retirement packet:

- Task: WI-20260702-001.
- Job: WJ-20260702-001-A.
- Handoff: WH-20260702-001.
- Boundary: website-local.
- Upstream source writes: forbidden.
- Deployment: not authorized.
- This plan path is not included in that packet's write allowlist.

Before any implementation work described here begins, the unrelated current
packet must be validated and checkpointed under its own existing authority.
That checkpoint is an external precondition, not a frontend-recommendations
task and not an action authorized by this plan. Only after the resolver exposes
a lawful transition point may the owner open a separately authorized
plan-adoption packet that explicitly allowlists this plan, the new frontend
control records, and no runtime frontend files. A later implementation packet
must then name its allowed reads,
allowed writes, outputs, validators, approvals, stop conditions, and checkpoint
behavior.

## 2. Executive implementation outcome

The implementation will preserve the existing black, ivory, cyan, and orange
identity while replacing the site's generic page silhouette, stale promotional
story, repetitive motion, excessive public navigation, and mobile/accessibility
defects with a source-grounded system that feels like a scientific instrument
observing a living field.

The outcome is not a color redesign. It is a coordinated correction across:

1. Scientific source and narrative integrity.
2. Product brand hierarchy.
3. Public information architecture.
4. Page archetypes and reading rhythm.
5. Typography, spacing, containers, z-index, and motion tokens.
6. Route-family-specific visual grammar.
7. Deterministic, accessible, lifecycle-aware motion.
8. Mobile navigation, tables, artwork, zoom, and assistive-technology behavior.
9. Diagram-gallery discovery and inspection.
10. Promotional, media, contribution, and discovery surfaces.
11. Image, CSS, animation, and route-build performance.
12. Manifest, provenance, source-notice, and validation rigor.

The redesigned first experience must communicate, without inflating source
authority, the registered effective-theory/open-foundation position stated by
the exact-closure sequence (The Æther Flow Project, 2026a, Abstract; Exact
Theory Statement):

- Exact closure is complete at the effective-theory level.
- Observable gravitational content is operationally identical to ordinary
  general relativity.
- The Æther / Æther-Flow ontology remains the interpretive and conceptual
  structure.
- First-principles recovery from deeper substrate dynamics remains open.
- No independent low-energy non-GR signature is claimed.
- The AI research system is governed infrastructure for pursuing and auditing
  the open foundational problem; it is not a proof authority.

## 3. Source, scientific, and governance constraints

### 3.1 Non-negotiable claim boundary

No public copy, visual, metadata, caption, alternative text, structured data,
video, social image, diagram, or interaction may imply any of the following:

1. General relativity has already been derived from Æther or Æther-Flow
   substrate microphysics.
2. The project has independent experimental or scientific validation beyond
   the source-authorized project position.
3. A validator PASS, registry row, hash, role, AgentJob, handoff, generated
   derivative, website page, or AI output proves a physics claim.
4. The AI research system crosses, completes, or replaces the open scientific
   derivation gate.
5. The exact-closure package introduces an established independent low-energy
   non-GR observable sector.
6. Website presentation has promoted an ontology, candidate, derivation, or
   scientific verdict.

### 3.2 Required authoritative source set

The P0 narrative correction must inspect and pin, at minimum:

- Upstream ontology/tex/aether_flow_exact_closure_sequence_overview.tex.
- Upstream ontology/tex/aether_flow_exact_closure_note.tex.
- Upstream ontology/tex/aether_flow_exact_closure_flagship_article.tex.
- Upstream registries/TEX_SOURCE_REGISTRY.csv.
- Upstream registries/PDF_DERIVATIVE_REGISTRY.csv.
- Upstream registries/CLAIM_BOUNDARY_REGISTRY.csv.
- Any current governed record that owns physics-owner review or public
  positioning approval.
- Website public/files/manifests/source_manifest.json.
- Website public/files/manifests/page_route_map.json.
- Website public/files/manifests/page_provenance.json.
- Website src/lib/siteContent.ts source-notice defaults.

The upstream checkout must be clean and committed before source bundles or
provenance are regenerated. Website-local copies must be compared by hash to
the pinned upstream commit. If source files or registry status differ from the
audit basis, implementation stops at the source-refresh gate.

### 3.3 Canonical document sequence

The public sequence must be represented consistently as follows (The Æther Flow
Project, 2026a, Flagship Package and Reading Order):

1. Exact-Closure Sequence Overview, the canonical front door.
2. Exact-Closure Note, the short standalone anchor.
3. Foundations.
4. Dynamics.
5. Consistency.
6. Relativistic Recovery.
7. Flow Geometry.
8. Flagship public article, presented as the release-facing synthesis built on
   the ordered core rather than as a replacement for the overview.

The sequence must be corrected in every place that owns or derives ordering,
including:

- src/pages/resources/documents.astro.
- src/lib/manifests.ts.
- src/components/DocumentActions.astro consumers.
- Any sequence data introduced for Home, Physics, Library, media, or structured
  metadata.
- Route copy, captions, and primary actions.
- Tests or validators added for sequence order.

### 3.4 Mixed-source route status

Adding canonical TeX sources to a curated website route does not automatically
make the website route canonical. Home and Physics remain reader-facing curated
syntheses. The implementation packet must decide whether:

- the existing upstream_authority_status value remains generated_noncanonical
  because the route itself is a derivative synthesis; or
- the page-provenance schema is intentionally extended with a reviewed mixed
  status.

No new enum may be introduced solely to make a route appear more authoritative.
Any schema change requires a dedicated manifest-authority review and fixture
tests.

### 3.5 Physics-owner acceptance gate

Before source-corrected positioning ships:

1. Produce a claim-copy-source matrix at statement granularity.
2. Map every promotional statement to an authoritative source path, pinned
   commit, relevant passage, registry status, and allowed public wording.
3. Record the exact statements that remain prohibited.
4. Obtain a named physics-owner review receipt.
5. Record accepted copy, required repairs, or blocked language.
6. Re-run content, manifest, provenance, and build gates after repairs.

The owner identity and receipt format are open decisions. Implementation may
prototype layout with clearly marked placeholder copy, but no source-strengthened
copy may be published before this gate passes.

## 4. Current-state evidence and architecture baseline

### 4.1 Audit snapshot to revalidate

The supplied audit observed the following baseline (Frontend audit conclusion,
2026):

| Measure | Audit value |
| --- | ---: |
| Built Astro pages | 64 |
| Main-content words | 53,456 |
| Median page length | Approximately 747 words |
| Pages at or above 800 words | 29 |
| Pages at or above 1,200 words | 8 |
| Rendered tables | 88 |
| Built inline SVG instances | 62 |
| Source SVG artworks | 58 |
| Astro files containing SVG artwork | 54 |
| Pages using physics-greenfield-svg | 27 |
| Diagram Gallery approved diagrams | 37 |
| Approximate gallery height | 14,000 rendered pixels |
| Global CSS lines | 4,382 |
| Global CSS source size | Approximately 99 KB |
| Brand PNG source | 1254 by 1254 pixels, approximately 1.1 MB |
| Home animated SVG elements in first viewport | Approximately 20 |
| Informational SVGs missing a complete title/description pair | 10 |

The audit's approximate contrast checks against black were:

- Ivory: 19.93:1.
- Muted ivory: 12.32:1.
- Orange: 7.68:1.
- Cyan: 7.07:1.

These values should be remeasured from the final computed tokens and states.
They are preservation baselines, not permission to use color as the only status
signal.

These are planning baselines, not perpetual facts. Packet FE-G0-02 must rerun
the inventory and store a dated baseline report before implementation.

### 4.2 Active public route architecture

The checked-in route map and provenance manifest each contain 34 active routes
(The Æther Flow Website, 2026b, 2026c).
The source tree contains 64 Astro pages because 30 legacy src/pages/project
routes still build even though production redirects send their URLs elsewhere.

Current primary route families:

- Home: /.
- Physics: /physics/ and six child routes.
- AI Research System: /ai-research-system/ and eight child routes.
- Resources: /resources/ and supporting library, trust, guide, and advanced
  routes.
- License: /license/.

### 4.3 Key implementation surfaces

| Concern | Current authority surface | Current issue |
| --- | --- | --- |
| Global shell | src/layouts/BaseLayout.astro | Brand hierarchy, metadata, remote assets, and mobile navigation |
| Navigation data | src/lib/siteContent.ts | Too many public children and no Advanced/Contributors layer |
| Home narrative | src/pages/index.astro | Stale positioning, late actions, generic two-track hero |
| Physics landing | src/pages/physics/index.astro | Defensive framing and generic orbital visual |
| AI landing | src/pages/ai-research-system/index.astro | Physics class reuse and generic orbit/core silhouette |
| Documents | src/pages/resources/documents.astro | Canonical sequence is incorrect |
| Manifest ordering | src/lib/manifests.ts | Duplicate source of incorrect document order |
| General-public guide | src/pages/resources/guided-starts/general-public/index.astro | Nineteen status/route items instead of three narrative acts |
| Diagram Gallery | src/pages/resources/diagrams.astro and src/components/DiagramGalleryList.astro | Equal weighting, repeated provenance, no search/filter hierarchy |
| Hero visual slot | src/components/CommandBand.astro | Strong reusable slot; preserve and extend |
| Linked cards | src/components/EvidenceRail.astro | Whole body and bullets form one verbose accessible link |
| Comprehension images | src/components/ComprehensionBlocks.astro | Forces eager loading |
| General figures | src/components/Figure.astro | No intrinsic dimensions or aspect-ratio contract |
| Generic deep renderer | src/components/InternalExplainerPage.astro | Repeats one page grammar; no breadcrumbs, TOC, sibling or next-step orientation |
| Design system | src/styles/global.css | Monolithic, alignment drift, long measures, excessive glow, generic motion |
| SVG policy | scripts/validate_svg_policy.py | Detects visible text and superficial motion hooks only |
| Layout contract | scripts/validate_layout_language.py | Hard-coded migrated surfaces and resource authority boundary |
| Quality gate | scripts/quality_gate.py | Hard-coded current gallery classes; no accessibility or motion-quality coverage |
| Route source bundles | public/files/manifests/page_route_map.json | Home and Physics omit core exact-closure TeX |
| Page hashes/provenance | public/files/manifests/page_provenance.json | Must regenerate after page or source-bundle changes |
| Published asset hashes | public/files/manifests/source_manifest.json and asset_manifest.json | Must decide governance for fonts, logos, social images, and media |
| Legacy routes | src/pages/project and public/_redirects | Thirty source routes build and then redirect |

### 4.4 Current strengths to preserve

1. Black, ivory, cyan, and orange identity.
2. Strong observed contrast relationships against black.
3. Static Astro output and low framework complexity.
4. Landmarks, headings, captions, current-page states, disclosure state, visible
   focus, and Escape-key behavior.
5. Informational SVG role usage.
6. No visible embedded SVG text.
7. Existing title and description coverage on most SVGs.
8. Operating-system reduced-motion support.
9. CommandBand visual-slot reuse.
10. Internal-first reader journeys with GitHub retained for provenance.
11. The /resources/source-authority/ trust route, together with the prohibition
    on embedding the reusable dedicated SourceAuthoritySection or SourceNotice
    section on any /resources/ page.
12. Manifest, provenance, hash, curator, build, and implementation-control
    infrastructure.

## 5. Target experience and design grammar

### 5.1 Product promise

The first viewport should say, in source-approved language:

- Eyebrow direction: Exact closure • Open foundation.
- Headline direction: A deeper ontology. Exactly Einsteinian gravity.
- Lead direction: The ontology is retained while ordinary GR is adopted as the
  exact effective gravitational law; first-principles substrate recovery remains
  open.

The audit's wording is a strong direction, not automatically approved final
copy. The P0 claim review owns the final text.

### 5.2 Primary first-viewport actions

No more than three:

1. Read the flagship theory.
2. Explore the open frontier.
3. See how the research is governed.

The exact internal destinations are resolved at the IA decision gate. At least
the flagship theory and current status must be reachable in one click.

### 5.3 Immediate status strip

Directly beneath the hero, render five compact states:

| State | Public value | Non-color semantics |
| --- | --- | --- |
| Exact closure | Completed effective statement | Solid frame and completion icon |
| Observable dynamics | Exactly GR | Solid cyan rule or shell plus explicit text |
| Ontology | Retained interpretive structure | Orange field marker plus explicit text |
| First-principles derivation | Open | Dashed bridge ending at aperture |
| New low-energy signature | Not claimed | Neutral stopped state plus explicit text |

The strip must not rely on color alone. Mobile may stack or horizontally group
the states, but no state may be clipped, hidden behind undiscoverable scrolling,
or removed.

### 5.4 Semantic palette

| Token meaning | Intended use | Prohibited implication |
| --- | --- | --- |
| Black | Substrate, depth, unknown state, unavailable transition | Failure by color alone |
| Ivory | Explanation, stable content, convergence | Independent validation |
| Cyan | Geometry, evidence, observation, validation, information transport | Proof merely because a surface is cyan |
| Orange | Source activity, active flow, primary action, unresolved transition | Adopted physics merely because a path is active |

### 5.5 Semantic shape and line grammar

| Form | Meaning |
| --- | --- |
| Solid line | Established, adopted, or currently operative relationship |
| Dashed line | Proposed, conditional, open, or not-yet-derived relationship |
| Aperture or gate | Human or scientific promotion boundary |
| Halo | Influence, context, or attention; never proof |
| Closed shell | Exact effective layer or adopted boundary |
| Stopped path | Explicitly open or unavailable transition |
| Return loop | Validation or operational feedback, not scientific truth |

### 5.6 Route-family silhouettes

Physics:

- Continuous fields.
- Curved and locally perturbed trajectories.
- Layered effective geometry.
- A solid exact-GR shell or layer.
- A dashed derivational bridge that visibly stops.
- Asymmetric rather than generic mirrored orbital networks.

AI Research System:

- Discrete request tokens.
- Bounded task or job envelope.
- Source-inspection checkpoint.
- Validator return loop.
- Completion and handoff branch.
- Explicit human gate and stop state.

Resources and provenance:

- One-way lineage from source to registry or manifest to approved derivative to
  reader.
- Visible versions and hashes.
- Archival, stable record treatment.
- No backward arrow or loop that implies derivatives modify authority.

Home:

- A narrative integration of ontology, exact effective closure, the open
  derivation gate, and the separate governed AI audit loop.
- It must be distinguishable from each family landing rather than becoming a
  fourth generic orbit.

## 6. Global goals and release outcomes

### 6.1 First-reader comprehension

Within 20 to 30 seconds, a first-time reader must be able to answer:

1. What does Æther Flow propose?
2. What is already complete?
3. What remains open?
4. How does the project relate to general relativity?
5. What role does the AI research system play?

The baseline proposal for the comprehension gate is at least five representative
first-time readers, at least 80 percent correct on each question, and zero
critical false inferences. The owner must approve the final sample, audience mix,
and pass threshold before testing.

### 6.2 Global release requirements

- No more than three primary first-viewport actions.
- Flagship theory and current status each reachable in one click.
- No more than five choices in any primary public menu group.
- Physics, AI, and Resources heroes identifiable with titles hidden in a still
  frame.
- Every promotional statement maps to a canonical source and claim status.
- Every animated figure provides Full, Reduced, and Still behavior.
- Offscreen and hidden-document motion pauses.
- No visible SVG text.
- Every informational SVG has a usable accessible name, title, description,
  caption, unique IDs, and meaningful static composition.
- Mobile art remains semantically clear without microscopic geometry.
- Technical table overflow is visible and keyboard-operable, or the table is
  replaced by an appropriate card presentation.
- SVG, layout, content, source, manifest, provenance, comprehension, build,
  implementation-control, and relevant accessibility gates pass after each
  packet.
- Skipped checks are named with a concrete reason and follow-up owner.

## 7. Approval gates and open decisions

### 7.1 Required approval gates

| Gate | Decision owner | Must pass before | Evidence |
| --- | --- | --- | --- |
| AG-01 Public claim changes | Physics owner and website owner | P0 copy publication and Home prototype acceptance | Claim-copy-source matrix and signed review receipt |
| AG-02 Source refresh uncertainty | Source owner | Importing or citing drifted upstream sources | Clean commit, source hashes, registry status |
| AG-03 Shared visual system | Website owner | Scaling Home prototype to route families | Still, Reduced, Full review and semantic checklist |
| AG-04 Broad navigation | Website owner | Public IA rollout | Route mapping and before/after journey review |
| AG-05 Route retirement | Website owner | Removing legacy source routes | Per-route redirect/canonical/link decision ledger |
| AG-06 Public downloadable assets | Website and source owners | Publishing new fonts, images, media, or kits | License, optimization, manifest and provenance review |
| AG-07 Public manifest authority records | Source or manifest owner | Schema/status changes | Schema diff, fixture tests, manual authority review |
| AG-08 Analytics or retention | Website owner and privacy owner | Adding tracking, subscriptions, or stored identifiers | Provider, consent, retention, access, deletion, and privacy decision |
| AG-09 External contribution channel | Project owner | Publishing challenge/reviewer submission action | Moderation, conduct, licensing, contact, response expectations |
| AG-10 Git push | Project owner | Publishing accepted commits to GitHub | Clean branch, scoped commit, validation evidence |
| AG-11 Cloudflare deployment | Project owner | Production release | Pushed accepted commit and explicit deploy authorization |

### 7.2 Open decision register

| ID | Decision | Default recommendation | Blocks |
| --- | --- | --- | --- |
| D-01 | Physics reviewer identity and receipt format | Named owner plus checked-in review record | P0 publication |
| D-02 | Final flagship article route | Reuse /resources/documents/ entry initially; approve a dedicated reader route only if it reduces friction | Hero CTA and structured data |
| D-03 | Production origin and canonical policy | Use one configured site origin; no hard-coded duplicates | Canonicals, sitemap, social metadata |
| D-04 | Final Home wording | Start from audit direction, then physics-owner edit | P0 copy |
| D-05 | Route-family ownership | Assign Home, Physics, AI, Resources maintainers | Bounded rollout |
| D-06 | Display font | Compare two or three licensed self-hostable geometric faces; choose one | Type implementation |
| D-07 | Mono font | Prefer self-hosted IBM Plex Mono or approved equivalent | Instrumentation type |
| D-08 | Canonical wide container | Normalize at an approved value, provisionally 1180px | Token and alignment work |
| D-09 | Page archetype hybrids | One primary archetype plus explicitly declared secondary behavior | Route mapping |
| D-10 | Motion control placement | Global header or utility control with per-site persisted preference | Motion foundation |
| D-11 | Preference precedence | Explicit user choice overrides OS until reset | Motion behavior |
| D-12 | Narrative replay | Run once per page load by default; provide replay only if user value is proven | Home prototype |
| D-13 | Observer threshold | Start near 35 percent visible with tested root margin | Motion lifecycle |
| D-14 | Performance budgets | Adopt provisional budgets in Section 18 after baseline measurement | Prototype acceptance |
| D-15 | Accessibility target | WCAG 2.2 AA is the recommended project target, subject to owner approval | QA program |
| D-16 | Mobile menu pattern | One top-level disclosure/drawer with nested on-demand groups | Navigation work |
| D-17 | Minimum supported viewport | Test 320px width and short landscape viewports | Responsive acceptance |
| D-18 | Table conversion inventory | Convert public vocabulary tables; wrap comparison/data tables | Table packets |
| D-19 | Gallery detail model | Accessible dialog for quick inspection plus stable asset link; dedicated pages only if editorial content warrants | Gallery rebuild |
| D-20 | Gallery feature owner | Website curator selects representative default subset | Gallery hierarchy |
| D-21 | Advanced indexing | Keep public and indexable unless it exposes internal-only material; remove from primary nav | IA rollout |
| D-22 | Legacy route policy | Retain redirects, remove duplicate source pages after link audit | Route retirement |
| D-23 | Update retention | Defer unless provider, privacy, ownership, and maintenance are approved | P6 retention |
| D-24 | Analytics | Defer unless a minimal event model and privacy decision are approved | P6 analytics |
| D-25 | Ninety-second media | Decide whether to replace or supplement the current video | Media packet |
| D-26 | Reviewer channel | Prefer GitHub issue/discussion template if the repository is ready; otherwise publish a read-only reviewer packet | Reviewer path |
| D-27 | Motion timing enforcement | Treat ranges as design tokens and warnings, not hard failures, until visual QA proves stable | Motion validator |
| D-28 | SVG classification | Require explicit informational or decorative classification in the new component contract | SVG validation |
| D-29 | Brand asset governance | Add optimized variants to manifests if treated as governed public assets | Brand packet |
| D-30 | Remote badge replacement | Replace with stable local icons and text, not locally forged live status badges | Footer packet |

## 8. Recommendation coverage registry

The registry below covers 73 distinct implementation units extracted from every
numbered recommendation, unnumbered promotional/discovery bullet,
accessibility/responsive bullet, performance/maintainability bullet, stated
acceptance criterion, and audit limitation.

### 8.1 Source and narrative integrity

| ID | Requirement | Primary targets | Delivery packet |
| --- | --- | --- | --- |
| S-01 | Gate visual redesign behind source and narrative correction | Control records, claim review, route bundles | FE-P0-01 through FE-P0-07 |
| S-02 | Correct the eight-item canonical document sequence | documents.astro, manifests.ts, sequence tests | FE-P0-02 |
| S-03 | Add overview, note, and flagship article to Home and Physics source bundles | page_route_map.json | FE-P0-03 and FE-P0-04 |
| S-04 | Regenerate route provenance and update contextual source notices | page_provenance.json, siteContent.ts | FE-P0-03 through FE-P0-06 |
| S-05 | Review every revised claim against registry and obtain physics-owner approval | Claim matrix and review record | FE-P0-05 |
| S-06 | Encode and reuse the six-rung claim ladder | New typed content module and route copy | FE-P0-05 and FE-P0-06 |
| S-07 | Prohibit derivation, independent-validation, and AI-crosses-gate implications | Copy/visual lint and manual review | All claim-bearing packets |
| S-08 | Reframe Home and Physics around exact closure and open foundation | Home, Physics, metadata | FE-P0-06 |
| S-09 | Add the five-state status strip with non-color semantics | New status component, Home | FE-P0-07 |
| S-10 | Lead positively and move detailed limits into accessible disclosure | Page archetypes, route copy | FE-P0-06 and FE-P3-07 |
| S-11 | Move the first mobile decision point earlier | Home hero and mobile nav | FE-P1-03 and FE-P2-06 |

### 8.2 Brand, type, layout, and visual grammar

| ID | Requirement | Primary targets | Delivery packet |
| --- | --- | --- | --- |
| B-01 | Make The Æther Flow primary and By Angry Owl secondary | BaseLayout, header, footer, media page | FE-P2-01 |
| B-02 | Preserve the palette and strong contrast | Token files and contrast QA | All visual packets |
| B-03 | Enforce semantic color usage | tokens.css, design grammar, component review | FE-P3-03 |
| B-04 | Enforce line, aperture, gate, and halo semantics | Motion config and figure specifications | FE-P2-02 and FE-P3-08 |
| B-05 | Create distinct Physics, AI, and Resources silhouettes | Family hero components and configs | FE-P5-PHY, FE-P5-AI, FE-P5-RES |
| B-06 | Introduce self-hosted body, display, and mono roles | Font assets and typography.css | FE-P3-01 and FE-P3-02 |
| B-07 | Formalize type, container, spacing, radius, z, motion, easing, and measure tokens | tokens.css and documentation | FE-P3-03 |
| B-08 | Reduce primary reading measure to approximately 62–68ch | layout.css and archetypes | FE-P3-05 |
| B-09 | Replace uniform panels with deliberate narrative rhythm | Story archetype and representative routes | FE-P3-06 and FE-P4-04 |
| B-10 | Reserve strong glow for semantically active states | figures.css, motion.css, visual audit | FE-P3-05 and route packets |

### 8.3 Motion and SVG architecture

| ID | Requirement | Primary targets | Delivery packet |
| --- | --- | --- | --- |
| M-01 | Build and approve one narrative Home hero before bulk migration | AetherFieldHero and Home | FE-P2-03 through FE-P2-07 |
| M-02 | Replace synchronized group motion with deterministic local variables | Motion primitives/config | FE-P2-03 and FE-P3-08 |
| M-03 | Use semantic timing bands | Motion tokens | FE-P3-03 and FE-P3-08 |
| M-04 | Use coherent trajectories, depth, occlusion, and asymmetry without calling art a simulation | Figure specs and captions | FE-P2-04 and family packets |
| M-05 | Visualize ontology adoption versus open derivation | Home and Physics visuals | FE-P2-04 and FE-P5-PHY |
| M-06 | Stop animating filter values | motion.css and SVG markup | FE-P1-09, FE-P2-04, family packets |
| M-07 | Pause offscreen and hidden-document motion | motion lifecycle module | FE-P1-09 |
| M-08 | Add Full, Reduced, and Still preference with local persistence | MotionPreferenceControl and controller | FE-P1-09 |
| M-09 | Build a separate mobile art profile | Motion configs and responsive figures | FE-P2-05 and family packets |
| M-10 | Build reusable motion primitives without an animation dependency | components/motion and scripts | FE-P2-03 and FE-P3-08 |
| M-11 | Strengthen SVG validation and fix incomplete title/description pairs | validate_svg_policy.py and tests | FE-P1-08 |
| M-12 | Retire cross-family physics-greenfield-svg usage | Route components, CSS, quality-gate fixtures | FE-P3-08 and family packets |

### 8.4 Information architecture and cognitive load

| ID | Requirement | Primary targets | Delivery packet |
| --- | --- | --- | --- |
| IA-01 | Establish Start Here, The Theory, Open Frontier, Research System, and Library | siteContent.ts and BaseLayout | FE-P4-01 through FE-P4-03 |
| IA-02 | Move registries, retrieval, repository, builder, publication, and low-level operations to Advanced/Contributors | Navigation data and routes | FE-P4-02 |
| IA-03 | Cap primary menu groups at five and remove duplicate-target labels | Navigation and journey audit | FE-P4-02 |
| IA-04 | Use one collapsed accessible mobile Menu control | BaseLayout/header component and JS | FE-P1-03 and FE-P4-03 |
| IA-05 | Give large menus viewport-safe height and scrolling | navigation.css and behavior tests | FE-P1-03 |
| IA-06 | Rebuild the general-public page as three acts and three actions | General-public route | FE-P4-04 |
| IA-07 | Define Story, Status, Process, Library, and Trust archetypes | New layouts/components and route registry | FE-P3-06 and FE-P3-09 |
| IA-08 | Add breadcrumbs, sibling nav, TOC, current status, one next step, and disclosure to long pages | Orientation components | FE-P3-07 and FE-P4-05 |
| IA-09 | Rebuild Diagram Gallery with categories, search, larger previews, details, and shared provenance | Gallery route/component/data | FE-P4-06 |
| IA-10 | Feature or group representative diagrams instead of equal initial weight | Gallery data and curator review | FE-P4-06 |

### 8.5 Promotion and discovery

| ID | Requirement | Primary targets | Delivery packet |
| --- | --- | --- | --- |
| P-01 | Produce a source-approved accessible 90-second visual explanation | Media asset, transcript, poster, route | FE-P6-01 |
| P-02 | Make the flagship public article a prominent one-click destination | Home, Library, Theory route | FE-P0-06 and FE-P6-02 |
| P-03 | Add a dated Current Frontier summary with stale-state behavior | New or existing status route/data | FE-P6-03 |
| P-04 | Add a canonical manuscript-sequence entry surface | Documents/Library | FE-P0-02 and FE-P6-02 |
| P-05 | Add reviewer or challenge-the-open-problem path | Reviewer packet and contribution policy | FE-P6-04 |
| P-06 | Add a clear GitHub follow/contribution action | Header/footer/media/reviewer surfaces | FE-P6-05 |
| P-07 | Add update retention only after infrastructure and privacy approval | Optional service integration | FE-P6-06 |
| P-08 | Add a compact media page with approved summary, creator info, diagrams, and citations | New media route | FE-P6-07 |
| P-09 | Emit one correct canonical URL for each indexable route | BaseLayout metadata contract | FE-P6-08 |
| P-10 | Add project-specific social images and Open Graph/social metadata | Metadata contract and assets | FE-P6-09 |
| P-11 | Generate a canonical-only sitemap | Astro config or static generation | FE-P6-10 |
| P-12 | Add structured data only after current-standard verification | BaseLayout and route metadata | FE-P6-11 |
| P-13 | Add minimal privacy-respecting analytics only after approval | Optional analytics module | FE-P6-12 |

### 8.6 Accessibility and responsive behavior

| ID | Requirement | Primary targets | Delivery packet |
| --- | --- | --- | --- |
| A-01 | Raise the skip link above the header | z tokens and global shell | FE-P1-02 |
| A-02 | Increase desktop navigation targets to approximately 40–44px | navigation.css | FE-P1-04 |
| A-03 | Give EvidenceRail links concise accessible names | EvidenceRail.astro | FE-P1-05 |
| A-04 | Add table scroll affordances or convert public tables to cards | Table components and ontology pilot | FE-P1-06 |
| A-05 | Set appropriate native dark color-scheme behavior | tokens/base styles and head metadata | FE-P1-01 |
| A-06 | Preserve focus, current state, disclosure, landmarks, headings, captions, and Escape handling | Regression tests | Every shared component packet |
| A-07 | Complete informational SVG title/description coverage | SVG sources and validator | FE-P1-08 |
| A-08 | Test keyboard, 200–400 percent zoom, VoiceOver, Safari, Firefox, Android, Reduced, and Still | QA matrix | FE-P7-02 through FE-P7-04 |
| A-09 | Establish a formal accessibility target and evidence policy | QA plan | FE-G0-04 |

### 8.7 Performance and maintainability

| ID | Requirement | Primary targets | Delivery packet |
| --- | --- | --- | --- |
| R-01 | Replace the 1.1 MB logo request with right-sized modern/fallback variants | public/assets/brand and BaseLayout | FE-P2-01 |
| R-02 | Split global.css by responsibility while preserving import order | src/styles modules | FE-P3-04 |
| R-03 | Lazy-load below-fold comprehension diagrams | ComprehensionBlocks and route overrides | FE-P1-07 |
| R-04 | Add intrinsic image dimensions or aspect ratios | Figure and gallery components | FE-P1-07 |
| R-05 | Replace remote Shields and creator images with local intentional links/assets | BaseLayout and local assets | FE-P2-01 |
| R-06 | Remove or truly retire the 30 legacy project source routes | src/pages/project and redirects | FE-P6-13 |
| R-07 | Migrate SVGs in bounded families | Route-family packet inventory | FE-P5 packets |
| R-08 | Define and enforce measured performance budgets | Baseline, prototype, final QA | FE-G0-03, FE-P2-07, FE-P7-05 |

## 9. Target technical architecture

### 9.1 Architecture principles

1. Preserve static Astro output.
2. Add no client framework.
3. Add no animation library.
4. Prefer typed data and reusable Astro primitives over duplicated page markup.
5. Keep JavaScript progressive, small, event-delegated where useful, and
   inactive when the related feature is absent.
6. Make meaning available in HTML and static composition before motion.
7. Keep every public claim downstream from a route source bundle.
8. Preserve /resources/source-authority/ as the public trust/reference route.
   On that route and every other /resources/ page, keep provenance and
   non-authority boundaries in contextual copy, manifests, footer, or links;
   do not render the forbidden reusable SourceAuthoritySection or direct
   SourceNotice section.
9. Introduce compatibility aliases before removing widely used CSS selectors.
10. Migrate route families separately and keep every packet reversible.

### 9.2 Proposed source tree

Exact filenames may be adjusted in the first architecture packet, but the
responsibility boundaries should remain:

    src/
      components/
        brand/
          ProjectBrand.astro
        navigation/
          SiteHeader.astro
          PrimaryNavigation.astro
          NavigationMenu.astro
          SourceAuthorityUtility.astro
          Breadcrumbs.astro
          SiblingNavigation.astro
          LocalTableOfContents.astro
          RecommendedNextStep.astro
        status/
          ProjectStatusStrip.astro
          ClaimBoundarySummary.astro
        data/
          ResponsiveDataTable.astro
          TermCardGrid.astro
          OverflowTable.astro
        disclosure/
          ProgressiveDisclosure.astro
        motion/
          AetherFieldHero.astro
          MotionDiagram.astro
          FlowPath.astro
          EvidenceParticle.astro
          AuthorityGate.astro
          NodeCluster.astro
          MotionPreferenceControl.astro
        archetypes/
          StoryPage.astro
          StatusDashboardPage.astro
          ProcessWalkthroughPage.astro
          LibraryPage.astro
          TrustReferencePage.astro
        media/
          ResponsiveImage.astro
          AccessibleVideo.astro
      data/
        publicClaimLadder.ts
        routeArchetypes.ts
        navigation.ts
        diagramCatalog.ts
        publicStatements.ts
      scripts/
        motion-controller.ts
        navigation-controller.ts
        gallery-controller.ts
      styles/
        global.css
        tokens.css
        fonts.css
        base.css
        typography.css
        layout.css
        navigation.css
        components.css
        cards.css
        figures.css
        motion.css
        responsive.css
        routes/
          home.css
          physics.css
          ai-system.css
          resources.css
      pages/
        media/
          index.astro

The initial migration should retain src/styles/global.css as the ordered entry
point imported by BaseLayout. It may import the new modules so route sources do
not all change at once. Remove migrated declarations from the old body only
after visual and selector-usage checks prove that the new module owns them.

### 9.3 Public claim data contract

Create one machine-readable, reviewed public-statement registry rather than
duplicating status sentences across Home, Physics, metadata, social cards, and
media copy. The runtime claim ladder references those statements by stable ID;
it does not own a second copy of the wording or source metadata.

Recommended shape:

    export type PublicClaimState =
      | "complete-effective"
      | "adopted-effective"
      | "interpretive"
      | "open-foundational"
      | "not-claimed"
      | "governed-method";

    export interface PublicClaimLadderItem {
      id: string;
      statementId: string;
      shortLabel: string;
      state: PublicClaimState;
      visualSemantic: "solid" | "dashed" | "field" | "stopped" | "loop";
      iconName: string;
    }

Requirements:

- Every item has one stable ID.
- Every item references exactly one reviewed statementId.
- The referenced statement owns exact wording, qualification, sources, source
  commit, registry status, review date, reviewer, and disposition.
- Components resolve wording from the reviewed registry; they do not invent or
  copy status sentences.
- Metadata and video scripts may summarize the ladder only through reviewed
  statement IDs or separately reviewed statement records.
- A unit test confirms all six required conceptual layers exist exactly once.
- A review fixture confirms no item equates adoption with derivation.
- Validation fails on orphaned statement IDs, duplicate IDs, non-accepted
  statements used at runtime, wording drift from generated review output, or a
  referenced source absent from the route's approved source bundle.

### 9.4 Public statement traceability

Create the authoritative reviewed registry as typed data such as
src/data/publicStatements.ts or a schema-validated JSON equivalent. Generate a
human-reviewable report under docs/quality or another owner-approved evidence
path from that single registry. Do not hand-maintain both copies. Each registry
record should contain:

| Field | Purpose |
| --- | --- |
| Statement ID | Stable reference used in review and tests |
| Exact public wording | The sentence or metadata claim being published |
| Surface | Home, Physics, media, social, video, caption, alternative text, or other |
| Source path | Canonical source that supports the wording |
| Source commit | Pinned upstream commit |
| Passage | Section or line-oriented locator |
| Registry status | Canonical, accepted, benchmark claim, or applicable state |
| Allowed qualification | Required boundary wording |
| Forbidden overread | Specific implication to prevent |
| Reviewer | Named physics or website owner |
| Review date | Date of accepted review |
| Disposition | Accepted, repair, blocked, or superseded |

The statement registry is publication evidence, not scientific authority. The
route source bundle and upstream records remain authoritative. Tests must
verify that the generated review report is current with the machine-readable
registry and that every runtime ladder statement is accepted for its actual
surface.

### 9.5 BaseLayout metadata contract

Extend BaseLayout without forcing each route to hand-author raw head tags.
Recommended properties:

    interface Props {
      title?: string;
      description?: string;
      bodyClass?: string;
      exactTitle?: boolean;
      canonicalPath?: string;
      socialImage?: {
        src: string;
        alt: string;
        width: number;
        height: number;
      };
      pageKind?: "website" | "article" | "technical" | "library" | "media";
      publishedTime?: string;
      modifiedTime?: string;
      robots?: "index,follow" | "noindex,follow";
      structuredData?: Record<string, unknown> | Record<string, unknown>[];
    }

Implementation rules:

- Configure the production site origin once through Astro configuration or a
  validated environment/public configuration value.
- Emit one absolute canonical for every indexable route.
- Do not emit a canonical for a URL that redirects elsewhere.
- Emit Open Graph and social metadata from the same route metadata object.
- Provide a project-level default social image and allow approved archetype or
  route overrides.
- Structured data must mirror visible content exactly.
- Escape serialized structured data safely.
- Do not mark a website synthesis as a canonical scientific publication.
- Add metadata fixture tests against representative Story, Status, Library,
  Trust, media, and noindex routes.

### 9.6 Header and navigation architecture

Extract header logic from BaseLayout into focused components while retaining a
single global navigation controller.

Desktop behavior:

- Primary brand lockup always identifies The Æther Flow.
- By Angry Owl appears as secondary attribution.
- Five primary public destinations maximum.
- Source Authority remains a visually persistent trust utility rather than a
  sixth equally weighted destination.
- Advanced/Contributors is visually subordinate.
- Every nav target provides a 44px goal and never less than the approved 40px
  exception.
- Current-page state uses aria-current and visible non-color styling.
- Dropdowns close on outside click and Escape.
- Focus returns to the trigger after Escape.

Mobile behavior:

- One Menu button is visible while the full navigation is collapsed.
- The button exposes an accessible name, aria-expanded, and aria-controls.
- Opening the menu moves focus to the first useful control or leaves focus on
  the trigger according to the approved disclosure pattern.
- Nested groups open on demand and do not render every child as a permanent
  stack.
- Menu height uses a dynamic-viewport-aware maximum with a safe fallback.
- All items remain reachable in short landscape viewports.
- Closing restores focus to the Menu button.
- Outside click or explicit Close may close the surface; Escape must close it.
- Page scrolling behavior is tested before any scroll lock is adopted.
- The no-JavaScript state keeps essential routes accessible.

Recommended navigation data shape:

    interface NavigationGroup {
      id: string;
      title: string;
      href: string;
      audience: "public" | "advanced";
      description: string;
      children?: NavigationItem[];
    }

Do not maintain separate unrelated desktop and mobile navigation datasets.

### 9.7 Recommended URL mapping for the five public destinations

This mapping minimizes new URLs and preserves existing route authority. It must
still pass AG-04.

| Public label | Recommended destination | Reason |
| --- | --- | --- |
| Start Here | /resources/guided-starts/general-public/ | Dedicated first-reader journey |
| The Theory | /physics/ | Existing primary reader-facing Physics landing can become the exact-closure front door |
| Open Frontier | /physics/open-burdens/ | Existing route explicitly owns unresolved work |
| Research System | /ai-research-system/ | Existing governed-method landing |
| Library | /resources/library/ | Existing reader-job library landing |
| Source Authority utility | /resources/source-authority/ | Persistent trust path |
| Advanced/Contributors | /resources/ or an approved anchored/child surface | Houses technical governance and builder paths |

The Home logo remains a direct link to /. Home does not need a sixth text link
if the brand link is clear and accessible.

### 9.8 Page archetype contract

Every active route receives one primary archetype. Hybrid behavior is explicit
and secondary.

#### Story

Required beats:

1. Immersive concept scene.
2. Narrow explanation.
3. Compact status/evidence band.
4. Expandable or interactive explanation.
5. Concise source closure.

Avoid:

- A disclaimer as the first substantive statement.
- A six-card route catalogue before the main idea.
- Multiple full-width source matrices in the primary narrative.

#### Status dashboard

Required beats:

1. Dated as-of state.
2. State source and freshness.
3. Complete, open, blocked, and not-claimed categories.
4. One clear next gate.
5. Expandable evidence details.
6. Stale-state failure behavior.

Avoid:

- Progress bars that imply proof percentage.
- A validator PASS presented as scientific completion.

#### Process walkthrough

Required beats:

1. Trigger or request.
2. Bounded envelope.
3. Source inspection.
4. Work and return loop.
5. Completion/handoff.
6. Human gate and stop condition.

Avoid:

- Cosmic field visuals.
- An unbounded autonomous-agent metaphor.

#### Library

Required beats:

1. Reader job or question.
2. Featured/recommended entry.
3. Search/filter/browse as needed.
4. Status and format distinctions.
5. Contextual provenance.

Avoid:

- Repository structure as the first task.
- Repeating the same provenance paragraph on every item.
- The reusable SourceAuthoritySection or direct SourceNotice section on any
  /resources/ page. Preserve /resources/source-authority/ as the trust route,
  implemented through contextual copy rather than the forbidden section
  component.

#### Trust/reference

Required beats:

1. Scope and purpose.
2. Stable reference data.
3. Version/date/hash context.
4. Allowed and prohibited inference.
5. Next inspection path.

Avoid:

- Strong bloom or transport motion on archival records.
- Treating metadata presence as proof.

### 9.9 Local orientation contract

Routes above an approved threshold, provisionally 900 words or six H2 sections,
must receive:

- Breadcrumbs derived from navigation/route metadata.
- A compact sibling navigation.
- A collapsible local table of contents generated from stable heading IDs.
- A visible You are here status.
- Exactly one recommended next step.
- Progressive disclosure for long matrices and source lists.

Implementation details:

- Breadcrumbs use a navigation landmark and ordered list.
- The current item is text or aria-current, not a redundant self-link.
- The table of contents remains usable without sticky behavior.
- Disclosure uses native details/summary where it satisfies the design.
- Collapsed source evidence remains accessible, searchable as intended, and
  deep-linkable when required.
- Heading IDs remain stable across copy revisions.

### 9.10 EvidenceRail semantic refactor

Do not wrap label, title, paragraph, bullet list, and action in a single anchor.
Recommended structure:

- Article is the card container.
- Label, title, body, and bullets remain normal text.
- Title link or explicit action link has the concise accessible name.
- A non-nested visual affordance may make the card feel actionable.
- If stretched-link behavior is retained, the accessible name still comes from
  one concise link element and no nested controls are present.

Acceptance:

- Accessibility tree exposes a short link name.
- Body and bullet content remains available as adjacent descriptive text.
- Focus indication is visible around the actionable element and card context.
- The click target meets the approved minimum without making the entire
  paragraph the accessible name.

### 9.11 Table decision system

Classify every current table:

| Table type | Mobile treatment |
| --- | --- |
| Public vocabulary or definition | Convert to stacked term cards |
| Small status matrix | Stack into labeled status rows |
| True comparison table | Keep table semantics inside explicit scroll wrapper |
| Dense specialist data | Scroll wrapper plus instructions, focus, and edge cues |
| Download/asset metadata | Responsive definition list or disclosure |

OverflowTable requirements:

- Visible instruction such as Scroll table horizontally when overflow exists.
- Focusable, labeled wrapper.
- Keyboard scrolling.
- Start/end edge shadow or equivalent non-color cue.
- No instruction when the table does not overflow, if this can be detected
  reliably without layout instability.
- Correct table semantics remain inside the wrapper.
- At 200–400 percent zoom, no content or operation is lost.

TermCardGrid requirements:

- One semantic list or set of articles.
- Each card repeats row/column labels so meaning does not depend on visual
  position.
- Do not render duplicate desktop and mobile content to assistive technology.
- The ontology route is the first conversion pilot.

### 9.12 Figure and responsive image contract

Extend Figure and any gallery image component with:

    interface ImageDimensions {
      width: number;
      height: number;
      aspectRatio?: string;
    }

Rules:

- Raster images require intrinsic width and height.
- SVG assets require a known aspect ratio or stable responsive container.
- Eager loading is explicit and limited to true first-view/LCP candidates.
- Lazy is the default for below-fold comprehension diagrams.
- Use decoding async unless a measured exception is documented.
- Art-directed desktop/mobile sources must reserve the correct aspect ratio
  before loading.
- Expandable dialog images preserve alternative text, caption, focus, Escape,
  and scroll usability.

ComprehensionBlocks must accept a loading or priority policy rather than force
eager loading.

### 9.13 Motion component contract

MotionDiagram configuration must define:

    interface MotionDiagramConfig {
      idPrefix: string;
      family: "home" | "physics" | "ai" | "resources";
      accessibleTitle: string;
      accessibleDescription: string;
      semanticStatus: string;
      geometry: unknown;
      motionProfile: unknown;
      fullState: unknown;
      reducedState: unknown;
      stillState: unknown;
      mobileProfile: unknown;
      pausePolicy: "viewport-and-visibility";
    }

Required invariants:

- idPrefix is unique per rendered instance.
- Informational art uses role img and an accessible title/description pair.
- Meaningful labels are outside SVG in HTML.
- No visible SVG text.
- Still is an authored final composition, not animation-play-state frozen at an
  arbitrary phase.
- Reduced removes continuous or large movement while preserving state changes.
- Full uses deterministic, configured variation.
- Runtime randomness is prohibited.
- Infinite motion declares and implements a pause policy.
- Animated filter values are prohibited.
- Static blur layers may exist beneath sharp semantic geometry.

### 9.14 Motion preference and lifecycle

Preference states:

- Full: complete narrative entrance and ambient motion.
- Reduced: brief opacity/state transitions, no continuous transport or large
  parallax.
- Still: authored static state with all meaning visible.

Precedence:

1. An explicit persisted user selection.
2. Otherwise the operating-system preference.
3. Otherwise Full.

Persistence:

- Store only the preference value locally.
- Do not send it to analytics.
- Provide a Reset to system option or equivalent behavior.
- Apply the state before visible animation begins to avoid a motion flash.
- Consider cross-tab storage events only if implementation remains small and
  robust.

Lifecycle:

- IntersectionObserver marks eligible scenes active.
- document.visibilityState pauses all scenes when hidden.
- Only visible active scenes resume.
- Two partially visible scenes follow a deterministic priority rule.
- Removed nodes unregister cleanly.
- The controller is safe when IntersectionObserver is unavailable: default to
  Still or Reduced rather than uncontrolled infinite motion.

### 9.15 Narrative Home motion

Full-mode entrance:

1. 0–400 ms: dim substrate field establishes depth.
2. 400–900 ms: central region condenses.
3. 900–1500 ms: two asymmetric flow families emerge.
4. 1500–2100 ms: solid exact-GR effective shell becomes visible.
5. 1800–2400 ms: dashed upstream derivation path approaches and stops at the
   open aperture.
6. After 2400 ms: settle into slow ambient field and transport movement.

The governed AI track appears as a discrete audit loop outside the scientific
gate. It may inspect, validate, return, and hand off. It may not cross the gate.

Motion timing tokens:

- Ambient field: 12–20 seconds.
- Transport: 4.5–8 seconds.
- Gate/validation event: 650–1100 milliseconds.
- Rare intensity event: 10–16 seconds.

These ranges are review guidance and semantic token boundaries. The validator
should warn about unexplained outliers, not reject artistically justified
values until stable evidence supports hard enforcement.

### 9.16 Mobile art profile

Default mobile requirements:

- Approximate height of 180–220px.
- Six to ten particles.
- Primary semantic paths only.
- Reduced bloom radius.
- Fewer depth planes.
- Responsive stroke widths.
- Short caption.
- No microscopic copy or geometry.
- No desktop scene merely scaled down to 82px or 96px.

Mobile art and early actions must be balanced: the project identity, primary
status, and at least one action should appear within or near the first viewport.

### 9.17 CSS module ownership

| Module | Owns |
| --- | --- |
| tokens.css | Raw palette aliases, semantic colors, type roles, spacing, radii, containers, z layers, motion durations, easing |
| fonts.css | Font-face declarations, font-display, fallbacks, supported weights/styles |
| base.css | Reset, root/body, native color scheme, global links, focus |
| typography.css | Display, headings, leads, body, captions, status/mono |
| layout.css | Reading/wide containers, page bands, grids, narrative rhythm |
| navigation.css | Header, desktop nav, mobile menu, breadcrumbs, local nav |
| components.css | Buttons, status strip, disclosure, utilities |
| cards.css | Evidence, status, library, archival records |
| figures.css | SVG/image frames, captions, route-family static grammar |
| motion.css | Keyframes, custom properties, preference and lifecycle selectors |
| responsive.css | Cross-cutting breakpoints and zoom-safe rules |
| routes/home.css | Home-only composition |
| routes/physics.css | Physics field/geometry silhouette |
| routes/ai-system.css | AI token/envelope/return-loop silhouette |
| routes/resources.css | Source-lineage/archive silhouette |

Migration requirements:

- Document import order.
- Preserve temporary aliases for legacy selectors.
- Run selector-usage and visual regression checks before deleting aliases.
- Do not use route body classes as a substitute for component semantics.
- Reconcile the 1120px header and 1180px content widths through named container
  tokens.
- Set primary reading measure within 62–68ch; wide data/figures use explicit
  wide containers.

### 9.18 Typography implementation

Body:

- Self-hosted Inter Variable.
- Subset to required character coverage, including Æ/æ.
- Use font-display swap or an approved measured alternative.

Display:

- Compare at least two restrained geometric faces.
- Evaluate uppercase/lowercase balance, Æ glyph quality, numerals, punctuation,
  long headings, mobile wrapping, licensing, and byte cost.
- Do not use oversized all-caps as the default dramatic device.

Status/instrumentation:

- Self-hosted IBM Plex Mono or approved equivalent.
- Use for dates, hashes, states, compact labels, and instrumentation only.
- Do not turn body paragraphs into terminal-style text.

Font acceptance:

- License files stored or referenced appropriately.
- No remote font requests.
- No missing glyphs.
- No material layout shift.
- Preload only measured critical font files.
- Total font budget satisfies Section 18.

### 9.19 Glow and archival-surface rules

Strong glow is permitted only for:

- Active transport.
- Current frontier.
- Convergence.
- Gate event.
- Selected or inspected state.

Static sources, hashes, version records, and manifest cards must be sharp,
quiet, and archival. Visual review should inventory every strong drop shadow,
blur, bloom, and filter and record its semantic reason.

### 9.20 Diagram Gallery architecture

Data:

- Retain diagramConceptGroups and diagramGalleryItems or migrate them to a
  dedicated typed diagram catalog.
- Add concept keywords, short caption, long description, category, featured
  rank, source/provenance reference, dimensions, and optional related routes.
- Continue filtering against approved asset-manifest entries.

Initial page:

- Show category controls for Physics, AI, Operations, and Authority.
- Provide concept search over title, keywords, and short caption.
- Present a curated featured/default subset or grouped representative entries.
- Show a live result count and clear-filter control.
- Lazy-load non-featured previews.

Cards:

- Larger readable preview.
- One-line caption in the default state.
- Expandable detail with longer description and route/source context.
- One shared provenance statement per group, not per card.
- Stable direct asset link remains available.

Interaction:

- Native dialog or accessible dialog pattern for larger inspection.
- Escape closes and focus returns.
- Search/filter changes are announced politely.
- Filter state may update URL query parameters only after canonical/indexing
  policy is defined.
- Filtered states do not create accidental duplicate indexable pages.

### 9.21 Promotional and media architecture

Ninety-second explanation:

- Script originates from reviewed public statement IDs.
- Storyboard uses the new semantic visual grammar.
- Captions and transcript are mandatory.
- Poster image and metadata are optimized.
- No autoplay with sound.
- Reduced-motion users receive equivalent controls and static/transcript access.

Current Frontier:

- Has an explicit as-of date and source commit.
- States the open foundational burden without exposing unnecessary internal
  governance.
- Fails visibly stale after an approved threshold.
- Links to one current-status route and one source/provenance path.

Reviewer path:

- States the exact open question.
- Defines acceptable evidence and scope.
- Provides source package and citation route.
- Defines conduct, license, privacy, moderation, and response expectations.
- Does not promise review capacity that has not been approved.

Media page:

- Source-safe project summary.
- Creator attribution.
- Approved logo and image kit.
- Selected diagrams with usage notes.
- Canonical APA 7 citations.
- Contact or contribution route.
- Last-reviewed date and source boundary.

### 9.22 Asset pipeline

Brand:

- Generate right-sized PNG fallback and WebP/AVIF variants for 1x and 2x header
  display.
- Create favicon and Apple-touch variants deliberately.
- Retain the full master only if needed for downstream production.
- Use picture/srcset or an approved equivalent.

Social:

- Produce project-specific 1200 by 630 class images with tested safe zones.
- Store source/export relationship and license/usage notes.
- Add image dimensions and alternative text metadata.

Remote assets:

- Replace remote Shields and creator avatar requests with local icons, local
  approved imagery, or styled text links.
- Do not copy third-party assets without usage review.
- Do not simulate live badge state with a static image.

Manifests:

- If assets are governed public artifacts, add source-manifest entries with
  source path, usage note, status, size, and hash.
- Run python3 scripts/build_asset_manifest.py --write after source-manifest
  updates.
- Validate manifest paths and hashes.

### 9.23 Validator architecture

Extend scripts/validate_svg_policy.py to classify and verify:

- Informational versus decorative SVG.
- role img where informational.
- Accessible name.
- Unique title and description IDs.
- Description for informational artwork.
- No visible SVG text.
- Real animation declaration rather than class-name false positive.
- Full/Reduced/Still contract markers.
- Meaningful static fallback.
- Animated-filter error or migration-period warning.
- Unique definitions and referenced IDs.
- Infinite animation pause policy.
- Unique instance prefix when components can repeat.

Add fixtures to tests/test_validate_svg_policy.py for each pass/fail state.

Enforcement is staged:

- P1 hard failures: visible SVG text; missing informational role/name/title or
  description; invalid accessible references; duplicate IDs within the
  inspected source; and an informational/decorative classification violation.
- P1 legacy warnings: missing authored Still/Reduced state, missing lifecycle
  pause contract, animated filters, false-positive motion hooks, missing
  instance-prefix contract, or caption/static-composition gaps on unmigrated
  legacy figures.
- Immediate hard failures for every new or migrated figure: the complete
  Full/Reduced/Still, static, caption, unique-prefix, no-animated-filter, and
  pause-policy contract.
- P7 converts every remaining legacy warning to a release-blocking failure.

This staging preserves the Home-first prototype boundary and prevents P1 from
becoming an implicit mass rewrite of all SVG families.

Extend layout/quality validation to cover:

- Five-item primary navigation cap.
- One mobile Menu trigger.
- Skip-link z-order token relationship.
- Resource-page prohibition on the reusable SourceAuthoritySection/direct
  SourceNotice section, while preserving /resources/source-authority/ as a
  contextual trust route.
- Route archetype registration.
- Required orientation on eligible long routes.
- Concise EvidenceRail link structure.
- Figure dimension/loading requirements.
- Gallery category/search structure.
- No stale physics-greenfield-svg requirement on AI or Resources.

Update tests/test_quality_gate.py before removing the gallery's current
ai-greenfield-page and physics-greenfield-svg classes.

Add npm run validate:comprehension to the aggregate validation chain only in a
dedicated validator packet, after confirming its runtime and failure behavior.

### 9.24 Provenance regeneration rules

When route source, route map, or source bundle changes:

1. Confirm the upstream source root and commit.
2. Update public/files/manifests/page_route_map.json.
3. Update route source notices and any page copy.
4. Run python3 scripts/generate_page_provenance.py.
5. Review the generated diff for source order, hashes, route count, statuses,
   pinned URLs, and local-path leakage.
6. Run python3 scripts/run_curator.py without a write flag to preview current
   declared drift.
7. Stop if the preview exposes unexpected upstream drift, unexplained severity,
   or source changes outside the packet.
8. If and only if the drift is expected and reviewed, run
   python3 scripts/run_curator.py --write.
9. Manually inspect curator/reports/latest.json and
   curator/reports/latest.md.
10. Run npm run validate:provenance and npm run validate:curator.

The generator always writes; it has no --write flag.
Any packet that performs this workflow must explicitly allowlist
public/files/manifests/page_provenance.json,
curator/reports/latest.json, and curator/reports/latest.md in addition to its
route-map, page, notice, or source-data writes. A missing allowlist entry is a
stop condition, not permission to omit regeneration.

When governed public assets change:

1. Update public files.
2. Update public/files/manifests/source_manifest.json.
3. Run python3 scripts/build_asset_manifest.py --write.
4. Run npm run validate:manifests.
5. Review sizes, hashes, kinds, source references, approval status, and usage
   notes.

## 10. Active-route archetype and migration matrix

| Route | Primary archetype | Public/advanced | Principal change | Target packet |
| --- | --- | --- | --- | --- |
| / | Story | Public | Exact-closure narrative, status strip, Home motion, three actions | FE-P2-06 |
| /physics/ | Story | Public | Theory front door and Physics-specific field silhouette | FE-P5-PHY-01 |
| /physics/ontology/ | Story with Trust support | Public | Stacked vocabulary cards and ontology/effective-law boundary | FE-P5-PHY-02 |
| /physics/exact-gr-benchmark/ | Story with Status support | Public | Adoption versus derivation explanation | FE-P5-PHY-03 |
| /physics/derivation-roadmap/ | Status dashboard | Public | Open bridge, burdens, next gate, no proof progress bar | FE-P5-PHY-04 |
| /physics/flow-geometry/ | Story | Public | Continuous geometry-specific visual | FE-P5-PHY-05 |
| /physics/claim-status/ | Status dashboard | Public | Allowed, forbidden, gate-required states | FE-P5-PHY-06 |
| /physics/open-burdens/ | Status dashboard | Public | Open Frontier landing and dated state | FE-P5-PHY-07 |
| /ai-research-system/ | Process walkthrough | Public | Discrete token/envelope/return-loop identity | FE-P5-AI-01 |
| /ai-research-system/current-state/ | Status dashboard | Public | Dated operational state and stale behavior | FE-P5-AI-02 |
| /ai-research-system/workflow/ | Process walkthrough | Public | Bounded request-to-handoff narrative | FE-P5-AI-03 |
| /ai-research-system/agentjob-lifecycle/ | Process walkthrough | Public | One job envelope and stop conditions | FE-P5-AI-04 |
| /ai-research-system/roles-and-schemas/ | Trust/reference with Process support | Public | Role labels versus actual authority | FE-P5-AI-05 |
| /ai-research-system/human-gated-promotion/ | Process walkthrough | Public | Human aperture/gate and protected decision | FE-P5-AI-06 |
| /ai-research-system/validators-and-handoffs/ | Process walkthrough | Public | Validator return loop and bounded PASS | FE-P5-AI-07 |
| /ai-research-system/memory-preflight/ | Trust/reference with Process support | Advanced-supported public | Retrieval points back to source inspection | FE-P5-AI-08 |
| /ai-research-system/project-system-improvement/ | Process walkthrough | Advanced-supported public | Maintenance loop separated from research continuation | FE-P5-AI-09 |
| /ai-research-system/runtime-requirements/ | Trust/reference | Advanced | Tool/environment evidence | FE-P5-AI-10 |
| /resources/guided-starts/general-public/ | Story | Public | Three acts and three actions | FE-P4-04 |
| /resources/guided-starts/ | Library | Public | Audience path selection | FE-P5-RES-02 |
| /resources/reviewer-packet/ | Trust/reference | Public specialist | Challenge/review path and evidence package | FE-P6-04 |
| /resources/documents/ | Library | Public | Correct sequence and flagship entry | FE-P0-02 |
| /resources/diagrams/ | Library | Public | Search/filter/featured/detail gallery | FE-P4-06 |
| /resources/ | Library | Advanced gateway | Public resource orientation plus Advanced grouping | FE-P5-RES-01 |
| /resources/source-authority/ | Trust/reference | Persistent public utility | Quiet archival authority explanation | FE-P5-RES-03 |
| /resources/registries/ | Trust/reference | Advanced | Registry scope without proof implication | FE-P5-RES-04 |
| /resources/generated-derivatives/ | Trust/reference | Advanced | One-way derivative lineage | FE-P5-RES-05 |
| /resources/retrieval-layers/ | Trust/reference | Advanced | Navigation aid versus authority | FE-P5-RES-06 |
| /resources/publication-process/ | Process walkthrough | Advanced | Source-to-review-to-reader path | FE-P5-RES-07 |
| /resources/library/ | Library | Public | Primary reader-job library | FE-P5-RES-08 |
| /resources/reading-paths/ | Library | Public | Audience-specific next steps | FE-P5-RES-09 |
| /resources/repository-map/ | Trust/reference | Advanced | Repository topology without raw archaeology first | FE-P5-RES-10 |
| /resources/site-builder-guide/ | Trust/reference | Advanced | Builder rules and validators | FE-P5-RES-11 |
| /license/ | Trust/reference | Footer utility | Quiet legal/license surface | FE-P5-RES-12 |

### 10.1 Planned and conditional route matrix

The baseline contains 34 active manifest routes. This plan introduces one
required planned route, /media/, bringing the default target to 35 active routes
after implementation. Other reader jobs should reuse existing routes unless
AG-04 approves a dedicated route. Every approved new route must add a route-map
row, generated provenance row, canonical/indexing decision, archetype, source
bundle, owner, navigation placement, tests, and sitemap disposition.

| Candidate route | Disposition | Archetype | Source bundle | Canonical/index policy | Navigation placement | Owner | Route-count effect |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| /media/ | Planned by FE-P6-07 | Trust/reference with media support | Accepted public statements; exact-closure overview/note/flagship; approved creator and asset records | Self-canonical and indexable after AG-01/AG-06 | Footer, contributor/reviewer, and approved media links; not a sixth primary item | Website/media owner | +1, default total 35 |
| /physics/current-frontier/ | Conditional; default is to enhance /physics/open-burdens/ | Status dashboard | Current-state source records, dated snapshot, claim boundaries | Only self-canonical/indexable if a distinct maintained reader job and freshness owner are approved | Open Frontier primary destination only if it replaces the existing target | Physics/status owner | +1 only if approved |
| /physics/flagship/ | Conditional; default is a prominent flagship entry on /physics/ and /resources/documents/ | Story/article | Canonical flagship TeX plus overview/note and claim registry | Only self-canonical/indexable if it adds a source-backed reader article rather than duplicating the document | The Theory journey, never duplicate primary labels | Physics/publication owner | +1 only if approved |
| /advanced/ | Conditional; default is an Advanced/Contributors group on /resources/ | Library/Trust | Existing advanced route metadata; no new scientific claims | Index policy decided by AG-04; avoid duplicate hub content | Subordinate Advanced/Contributors utility | Website owner | +1 only if approved |
| /theory/ | Not recommended by default; use the /physics/ label mapping | Story | Same as Physics landing if ever approved | A separate route requires unique content or must redirect to /physics/ | Primary label only after redirect/canonical decision | Physics/website owner | 0 as redirect or +1 with approved unique content |

Default source-route count after FE-P6-13:

- 64 current Astro source pages.
- Minus 30 retired duplicate src/pages/project routes.
- Plus 1 planned /media/ route.
- Expected default: 35 Astro source pages, matching 35 active route-map and
  provenance entries.

Any approved conditional route increments all three counts together. A count
disagreement blocks release until the route, redirect, manifest, or provenance
contract is repaired.

## 11. Legacy route retirement matrix

The following source routes currently build under src/pages/project while
public/_redirects sends their public URLs to active routes. FE-P6-13 must audit
and remove the source files only after every active target is accepted.

| Legacy source route | Redirect target | Retirement check |
| --- | --- | --- |
| /project/physics/ontology/ | /physics/ontology/ | Active target preserves required content and backlinks |
| /project/physics/exact-gr-benchmark/ | /physics/exact-gr-benchmark/ | Benchmark language and sources preserved |
| /project/physics/gr-derivation-roadmap/ | /physics/derivation-roadmap/ | Roadmap content and anchors mapped |
| /project/physics/current-state/ | /physics/claim-status/ | Current-state expectation intentionally consolidated |
| /project/physics/distance-to-gr/ | /physics/open-burdens/ | Ledger explanation intentionally consolidated |
| /project/physics/metric-response-ladder/ | /physics/open-burdens/ | Specialist content retained or deliberately retired |
| /project/physics/finite-toy-models/ | /physics/open-burdens/ | Negative/frozen route context retained |
| /project/physics/no-target-import-discipline/ | /physics/open-burdens/ | Discipline boundary preserved somewhere discoverable |
| /project/physics/negative-results-and-frozen-routes/ | /physics/open-burdens/ | Negative results remain traceable |
| /project/physics/claim-gates/ | /physics/claim-status/ | Claim-gate detail preserved |
| /project/physics/source-extension-pipeline/ | /physics/derivation-roadmap/ | Pipeline context preserved |
| /project/physics/gate-chair-and-human-gates/ | /ai-research-system/human-gated-promotion/ | Physics versus operational gate language remains correct |
| /project/physics/ | /physics/ | Landing parity accepted |
| /project/ai-research-agent-system/workflow/ | /ai-research-system/workflow/ | Workflow parity accepted |
| /project/ai-research-agent-system/one-bounded-agentjob/ | /ai-research-system/agentjob-lifecycle/ | One-job details preserved |
| /project/ai-research-agent-system/roles-and-skills/ | /ai-research-system/roles-and-schemas/ | Role/skill distinctions preserved |
| /project/ai-research-agent-system/role-authority-inspector/ | /ai-research-system/roles-and-schemas/ | Authority inspection retained |
| /project/ai-research-agent-system/memory-registries/ | /ai-research-system/memory-preflight/ | Registry/retrieval context retained |
| /project/ai-research-agent-system/parent-child-synthesis/ | /ai-research-system/workflow/ | Parent-child boundedness retained or explicitly archived |
| /project/ai-research-agent-system/ | /ai-research-system/ | Landing parity accepted |
| /project/operations/director-agentjob-lifecycle/ | /ai-research-system/agentjob-lifecycle/ | Director lifecycle content mapped |
| /project/operations/role-routing/ | /ai-research-system/roles-and-schemas/ | Routing/allowlist content mapped |
| /project/operations/validator-operator-workflow/ | /ai-research-system/validators-and-handoffs/ | Operator workflow mapped |
| /project/operations/publication-process/ | /resources/publication-process/ | Publication detail mapped |
| /project/operations/project-system-improvement/ | /ai-research-system/project-system-improvement/ | Improvement loop mapped |
| /project/operations/technical-requirements/ | /ai-research-system/runtime-requirements/ | Requirements mapped |
| /project/operations/ | /ai-research-system/ | Consolidation accepted |
| /project/source-authority/claim-boundary-explorer/ | /physics/claim-status/ | Registry explorer value intentionally retained or retired |
| /project/source-authority/publication-and-provenance-system/ | /resources/publication-process/ | Provenance system content mapped |
| /project/source-authority/ | /resources/source-authority/ | Authority landing parity accepted |

Related compatibility aliases must also remain aligned with canonical and
sitemap policy:

| Alias | Current target | Required review |
| --- | --- | --- |
| /project/overview/ | / | Keep Astro config and static redirect behavior consistent |
| /overview | / | Confirm slash/canonical behavior |
| /research | /resources/publication-process/ | Confirm temporary 302 versus permanent intent |
| /research/map/ | /resources/publication-process/ | Confirm destination still matches reader intent |
| /documents | /resources/documents/ | Retain canonical target |
| /diagrams | /resources/diagrams/ | Retain canonical target |
| /equations | /resources/documents/ | Confirm equations remain discoverable at target |
| /research/equations/ | /resources/documents/ | Confirm canonical consolidation |
| /research/math-sample/ | /resources/documents/ | Confirm sample retirement |
| /downloads | /resources/ | Confirm Library is not the more accurate target after IA approval |

Retirement packet requirements:

- Search source, tests, manifests, dossiers, docs, and built links for every
  legacy path.
- Record keep, redirect, archive, or gone decision per route.
- Preserve existing 301 status unless an explicit SEO/content decision changes
  it.
- Do not include redirect targets in the sitemap as duplicates.
- Remove obsolete route-source-specific tests only after replacement coverage.
- Re-run the full 64-to-target build count comparison and record the reduction.
- Smoke-test every redirect.
- Keep historical evidence in git; do not retain duplicate build surfaces for
  history alone.

## 12. Observability and implementation evidence

Each packet must leave evidence sufficient for a reviewer to answer:

1. What changed?
2. Why was it in scope?
3. Which audit recommendations did it satisfy?
4. Which source bundle and commit constrained the work?
5. Which routes and shared consumers changed?
6. Which visual/motion states were reviewed?
7. Which commands ran and what passed?
8. Which browser, viewport, zoom, and motion modes were inspected?
9. Which approvals were required and obtained?
10. What remains uncertain or deferred?
11. What is the rollback boundary?
12. What is the next lawful packet?

Recommended checked-in evidence under docs/quality/frontend-recommendations or
another approved quality path:

- Baseline inventory JSON/Markdown.
- Claim-copy-source matrix.
- Route-archetype registry.
- Navigation decision ledger.
- Table conversion inventory.
- SVG/motion inventory.
- Performance budget and measurements.
- Accessibility/browser matrix.
- Screenshot index with desktop/mobile/zoom/still/reduced/full variants.
- Per-packet closeout reports.
- Final release-readiness report.

Screenshots and generated profiling artifacts should be kept only when they are
part of the repository's approved evidence policy. Temporary browser output may
remain under output/ or /tmp during development and should not be committed by
default.

## 13. Governed implementation sequence

### 13.1 Phase order

| Phase | Scope | Entry gate | Exit gate |
| --- | --- | --- | --- |
| G0 | Adopt this plan under fresh control, rebaseline, decide budgets and approvals | External precondition completed and owner authorizes a frontend planning lane | Current evidence, decisions, and fresh packet set exist |
| P0 | Source bundles, canonical sequence, claim ladder, positioning | G0 source paths and reviewers resolved | Physics-owner claim review and provenance pass |
| P1 | Accessibility, responsive safety, image fundamentals, motion preference foundation | G0 baseline; source-safe copy unchanged where possible | Confirmed defects fixed and shared safety tests pass |
| P2 | Home-only narrative and motion prototype | P0 accepted; P1 foundations ready | Home prototype passes semantic, comprehension, accessibility, mobile, and performance review |
| P3 | Shared tokens, type, CSS modules, archetypes, orientation, complete motion architecture | P2 prototype accepted | Representative fixtures and shared-system validators pass |
| P4 | Public navigation, general-public journey, long-page orientation, gallery IA | P3 components ready; AG-04 approved | Public path and gallery usability review passes |
| P5 | Bounded Physics, AI, and Resources route-family migration | P4 routes stable; AG-03 approved | Every active route assigned and migrated or explicitly deferred |
| P6 | Promotion, media, discovery, assets, optional privacy features, legacy retirement | Stable active routes and approved services/assets | Promotional/discovery surfaces pass source and production gates |
| P7 | System-wide comprehension, accessibility, browser, motion, performance, and release QA | All intended packets closed | Release-readiness report accepted; deployment remains separate |

### 13.2 Dependency rules

1. P0 source correction precedes source-strengthened public copy.
2. P1 skip-link, navigation, table, EvidenceRail, and motion-preference fixes do
   not wait for full visual migration.
3. P2 implements only Home and the minimum reusable motion foundation.
4. No route-family SVG migration begins until P2 is explicitly accepted.
5. P3 shared CSS and component work must provide compatibility paths before P5.
6. P4 navigation approval precedes canonical/sitemap decisions that depend on
   route hierarchy.
7. P5 executes one bounded route or small related route group per packet.
8. P6 analytics and retention are independent optional packets and may remain
   permanently deferred.
9. Legacy route source deletion occurs after active replacements and redirects
   pass, not during early IA work.
10. Deployment is not part of P7; it requires AG-10 and AG-11 after acceptance.

### 13.3 Stop conditions

Stop the current packet immediately when:

- The upstream source checkout is dirty or unpinned.
- A canonical source or registry disagrees with planned public wording.
- A required reviewer or approval is unavailable.
- The packet needs a path outside its allowlist.
- A generated manifest or provenance diff widens beyond expected routes.
- A /resources/ page would require the forbidden reusable
  SourceAuthoritySection or direct SourceNotice section. The existing
  /resources/source-authority/ route remains in scope as contextual trust copy.
- A shared CSS change produces unexplained cross-route regressions.
- Still or Reduced mode loses information.
- An informational SVG cannot receive a stable accessible name or unique IDs.
- A route retirement breaks an inbound link without an approved mapping.
- A privacy feature lacks a service owner, consent model, retention, or removal
  path.
- A production action would be required without explicit authorization.

## 14. Implementation packet catalog

Every packet uses the packet template in Section 15. This catalog defines the
minimum bounded units; the live control workflow may split a packet further but
must not silently combine unrelated packets.

### 14.1 G0 governance and baseline packets

| Packet | Goal | Principal writes | Dependencies | Exit |
| --- | --- | --- | --- | --- |
| FE-G0-01 | Open a separately authorized frontend plan-adoption/control-transition packet after the unrelated packet is already checkpointed | This plan and new frontend control records only, exactly allowlisted | External precondition: current WI-20260702-001 checkpoint completed under its own authority | Resolver recognizes the adopted plan and exposes the first bounded baseline packet |
| FE-G0-02 | Re-run route, word, table, SVG, CSS, asset, animation, and gallery inventory | Baseline report and approved scripts/tests only | FE-G0-01 | Dated baseline records exact counts and pre-existing defects |
| FE-G0-03 | Measure current performance and set provisional budgets | Performance baseline report | FE-G0-02 | Home, Physics, AI, Resources, gallery baselines recorded |
| FE-G0-04 | Establish accessibility target, severity model, browser/AT/zoom matrix, and evidence policy | Accessibility plan | FE-G0-02 | Target and release blocker definitions approved |
| FE-G0-05 | Resolve D-01 through D-30 or record explicit deferrals | Decision ledger | FE-G0-02 through FE-G0-04 | Every later blocker has an owner and disposition |

FE-G0-02 minimum measurements:

- Astro source-route count and built-page count.
- Active route-map and provenance count.
- Legacy route count.
- Rendered words by route and summary distribution.
- Tables by route and classification candidate.
- Informational/decorative SVG count.
- role, title, description, caption, unique-ID, motion-hook, and filter usage.
- CSS line/source/built/compressed size and selector ownership.
- Image dimensions, bytes, loading policy, and above-fold status.
- Network requests to remote visual assets.
- First-view action count.
- Navigation child counts.
- Animated element count per first-view scene.
- Current build, console, and validator state.

### 14.2 P0 source and narrative packets

| Packet | Goal | Exact targets | Dependencies | Exit |
| --- | --- | --- | --- | --- |
| FE-P0-01 | Pin and verify the authoritative exact-closure source set | Upstream read evidence; source comparison report | FE-G0-05 | Clean commit, hashes, registry states, and drift disposition recorded |
| FE-P0-02 | Correct canonical document order and add order validation | src/pages/resources/documents.astro; src/lib/manifests.ts; DocumentActions consumers; tests | FE-P0-01 | Eight-item order is consistent and tested |
| FE-P0-03 | Expand Home source bundle and regenerate provenance/curator evidence | page_route_map.json; page_provenance.json; Home source notice; latest curator JSON/Markdown | FE-P0-01 | Overview, note, flagship are pinned and Home remains correctly classified |
| FE-P0-04 | Expand the Physics landing source bundle and regenerate provenance/curator evidence | The /physics/ route-map row; physicsTrack source notice; page provenance; latest curator JSON/Markdown | FE-P0-01 | The Physics landing includes the required canonical sources without widening unrelated child bundles |
| FE-P0-05 | Create shared claim ladder and claim-copy-source review matrix | publicClaimLadder module; quality review artifact; tests | FE-P0-02 through FE-P0-04 | Six states exist, unsafe inferences are explicit, physics review passes |
| FE-P0-06 | Rewrite Home and Physics positioning with positive structure | index.astro; physics/index.astro; route metadata; contextual closures | FE-P0-05 | Exact closure/open foundation is clear and source-safe |
| FE-P0-07 | Implement the immediate five-state status strip | ProjectStatusStrip; Home; tokens/styles; tests | FE-P0-05 | All five states render accessibly on desktop/mobile without color-only meaning |

FE-P0-02 implementation notes:

- Replace the current Foundations-first specialistReadingOrder.
- Correct the duplicate order in src/lib/manifests.ts.
- Keep the overview visually identified as canonical front door.
- Present the flagship article as synthesis on top of the core.
- Test labels, slugs, ordinal positions, and duplicate/missing items.
- Confirm TeX links remain source-inspection targets and PDF links remain
  derivatives.

FE-P0-03 and FE-P0-04 implementation notes:

- Preserve route adaptation_type as curated_synthesis unless schema review says
  otherwise.
- Do not change upstream_authority_status merely because canonical inputs are
  present.
- Keep source path order deterministic.
- Update src/lib/siteContent.ts sourceRefs and dates.
- Use python3 scripts/generate_page_provenance.py after route-map changes.
- Manually inspect generated pinned URLs, source hashes, route hashes, commit
  date, and omission_reason.
- FE-P0-04 defaults to /physics/ only. A child Physics route may add one of the
  exact-closure sources only after statement-level relevance review proves that
  the source directly supports that route's public wording and the packet
  explicitly allowlists the child route row and notice.

FE-P0-06 content order:

1. What the project is.
2. Why exact closure matters.
3. What exists now.
4. What remains open.
5. How the work is tested and governed.
6. Evidence and sources.

Keep one concise visible boundary. Move detailed matrices and large source lists
into accessible progressive disclosure only after P3 supplies that component.
Until then, keep evidence visible or use native details without hiding required
context.

### 14.3 P1 accessibility and responsive foundation packets

| Packet | Goal | Exact targets | Dependencies | Exit |
| --- | --- | --- | --- | --- |
| FE-P1-01 | Establish z-index tokens and native dark color scheme | tokens/base/global styles; BaseLayout head if needed | FE-G0-04 | Native controls and layering pass contrast/browser checks |
| FE-P1-02 | Fix skip-link visibility and main-focus behavior | global/base CSS; BaseLayout; focused test | FE-P1-01 | Skip link appears above header and activation reaches main |
| FE-P1-03 | Implement one compact accessible mobile Menu with safe height | BaseLayout or SiteHeader; navigation controller/CSS; tests | FE-G0-05 | Initial mobile nav is collapsed and fully operable |
| FE-P1-04 | Enlarge desktop nav targets and preserve current/Escape behavior | Navigation markup/CSS/JS | FE-P1-03 | Target sizes and interaction regression checks pass |
| FE-P1-05 | Refactor EvidenceRail accessible names | EvidenceRail.astro; styles; representative consumers; tests | FE-G0-04 | Concise link names and clear card action |
| FE-P1-06 | Build table treatments and convert ontology pilot | OverflowTable; TermCardGrid; ontology route; styles/tests | FE-G0-05 | No clipped undiscoverable ontology data |
| FE-P1-07 | Add image dimensions, aspect ratios, and loading policy | Figure; ComprehensionBlocks; gallery images; data metadata | FE-G0-03 | Below-fold diagrams lazy-load and no image layout shift appears |
| FE-P1-08 | Strengthen SVG validation, repair ten incomplete title/description pairs, and inventory legacy motion warnings | SVG validator/tests; affected accessibility metadata; warning inventory | FE-G0-04 | Hard accessibility/ID/text checks pass; unmigrated motion/static/caption gaps are bounded warnings; new/migrated figures use the full contract |
| FE-P1-09 | Implement motion preference and lifecycle foundation | MotionPreferenceControl; controller; motion CSS; tests | FE-G0-04 | Full/Reduced/Still and offscreen/hidden pause work |
| FE-P1-10 | Update quality/layout gates before class migrations | quality/layout validators and tests | FE-P1-03 through FE-P1-09 | Guards reflect intended contracts, not old visual class names |
| FE-P1-11 | Integrate comprehension validation into the aggregate path | package.json and CI/local documentation | FE-P1-10 | npm run validate includes comprehension or explicitly equivalent coverage |

FE-P1-02 manual cases:

- 320px and desktop width.
- Browser zoom at 200 and 400 percent.
- Header menu closed and open.
- First Tab reveals skip link.
- Link is visually above the header.
- Enter moves to main content.
- Focus is visible at the main target or the reading position is unambiguous.

FE-P1-03 interaction cases:

- Pointer open/close.
- Keyboard open/close.
- Escape close and trigger-focus return.
- Outside click.
- Nested group state.
- Current child route.
- Short viewport internal scroll.
- Orientation change.
- No-JavaScript fallback.
- VoiceOver announcement.
- Focus order at 200 and 400 percent zoom.

FE-P1-06 inventory output:

- Every one of the audited tables receives type, audience, route, mobile
  treatment, owner, and packet assignment.
- Public vocabulary rows are prioritized for cards.
- Specialist comparison tables retain table semantics and receive overflow
  affordance.
- Duplicate mobile/desktop markup is avoided or hidden correctly from assistive
  technology.

FE-P1-08 migration policy:

- Animated-filter findings may be warnings for legacy families during the
  migration window.
- New or migrated visuals fail on animated filters immediately.
- The final P7 gate converts remaining warnings to failures.
- Decorative SVGs require aria-hidden and no misleading title/description.
- Informational SVGs require role, title, description, caption, unique IDs,
  static state, motion modes, and pause policy.

### 14.4 P2 Home prototype packets

| Packet | Goal | Exact targets | Dependencies | Exit |
| --- | --- | --- | --- | --- |
| FE-P2-01 | Implement project-first brand and optimized local assets | BaseLayout/header/footer; brand assets; manifests if governed | P0 accepted; FE-P1-03 | The Æther Flow is primary and no remote visual requests remain |
| FE-P2-02 | Publish internal semantic visual/motion specification | Design grammar document and typed semantic states | FE-P0-05 | Color/line/gate/halo meanings are approved |
| FE-P2-03 | Build minimum reusable motion primitives | AetherFieldHero; MotionDiagram; FlowPath; particle/gate primitives | FE-P1-08 and FE-P1-09 | Home can render unique Full/Reduced/Still scenes |
| FE-P2-04 | Implement the narrative Home entrance and settled state | Home motion config, styles, captions | FE-P2-02 and FE-P2-03 | Six-step story and no-AI-crosses-gate semantics pass |
| FE-P2-05 | Implement the authored mobile Home composition | Mobile motion profile and responsive art | FE-P2-04 | 180–220px semantic art and early action pass |
| FE-P2-06 | Recompose Home as a Story archetype with status and three actions | index.astro and Home styles/components | FE-P0-07 and FE-P2-05 | First viewport and narrative sequence meet product goals |
| FE-P2-07 | Run the Home prototype acceptance gate | Review report, screenshots, profiles, comprehension test | FE-P2-06 | AG-03 accepts or returns repair; no bulk migration before PASS |

FE-P2-01 brand assets:

- Header 1x/2x variants.
- Modern format and PNG fallback.
- Favicon set.
- Apple-touch image.
- Local creator/project link graphics only if approved.
- Measured bytes and DPR quality.
- Manifest entries if AG-06/AG-07 require them.
- No remote Shields or remote GitHub avatar requests.

FE-P2-07 PASS requires:

- Physics-owner confirms the scene does not strengthen claims.
- First-time-reader comprehension meets the approved threshold.
- Still frame communicates all five project states.
- Reduced and Still modes preserve the same meaning.
- Offscreen and hidden-tab pause is demonstrated.
- Mobile art is comprehensible and primary action is timely.
- No animated filter values.
- No visible SVG text.
- No duplicate SVG IDs.
- No critical keyboard, zoom, or VoiceOver defect.
- Provisional performance budgets pass or receive a documented repair packet.
- Home source bundle/provenance remains valid.

### 14.5 P3 shared-system packets

| Packet | Goal | Exact targets | Dependencies | Exit |
| --- | --- | --- | --- | --- |
| FE-P3-01 | Run display/mono font comparison and licensing review | Font comparison artifact | FE-P2-07 | Selected fonts, fallbacks, weights, and budgets approved |
| FE-P3-02 | Self-host and integrate approved fonts | Font assets; fonts.css; typography tests | FE-P3-01 | No remote fonts, missing glyphs, or material shift |
| FE-P3-03 | Establish complete design-token system | tokens.css and token documentation | FE-P2-02 and FE-P3-02 | Named type/container/space/radius/z/motion/easing tokens exist |
| FE-P3-04 | Split global.css through a compatibility entry point | Style modules and global.css imports | FE-P3-03 | Import ownership documented; representative visual regression passes |
| FE-P3-05 | Normalize containers, reading measure, narrative rhythm, and glow | layout/typography/cards/figures CSS | FE-P3-04 | Alignment and 62–68ch reading targets pass |
| FE-P3-06 | Build five page-archetype wrappers/components | archetype components and fixtures | FE-P3-05 | Each archetype renders a representative accessible fixture |
| FE-P3-07 | Build breadcrumbs, sibling nav, TOC, next step, and disclosure | Navigation/orientation components and tests | FE-P3-06 | Long-page orientation contract passes |
| FE-P3-08 | Complete reusable motion architecture and retire cross-family class assumptions | motion components/styles/controller/validators | FE-P2-07 and FE-P3-04 | Home plus one family fixture render without physics class leakage |
| FE-P3-09 | Create route-archetype registry and migration inventory | routeArchetypes data and quality artifact | FE-P3-06 | All 34 active routes and 30 legacy sources have dispositions |

FE-P3-04 migration method:

1. Create modules and import them from global.css.
2. Move tokens first.
3. Move base and typography.
4. Move layout and navigation.
5. Move component/card/figure rules.
6. Move motion.
7. Move route-family rules.
8. Move responsive rules with their dependency notes.
9. Run visual regression after each move.
10. Remove duplicates only after computed-style comparison.

### 14.6 P4 public journey packets

| Packet | Goal | Exact targets | Dependencies | Exit |
| --- | --- | --- | --- | --- |
| FE-P4-01 | Approve final five-destination URL mapping and index policy | Navigation decision ledger | FE-P3-09 | AG-04 signs route labels, targets, Advanced policy |
| FE-P4-02 | Implement new navigation data and Advanced/Contributors grouping | siteContent/navigation data | FE-P4-01 | Five public choices and subordinate advanced routes |
| FE-P4-03 | Finalize desktop/mobile header against new IA | Header/nav components and CSS/JS | FE-P4-02 | All primary and nested navigation tests pass |
| FE-P4-04 | Rebuild general-public guide into three acts | General-public route, content/data, visuals | FE-P0-05 and FE-P3-06 | Idea/exists/open plus exactly three terminal actions |
| FE-P4-05 | Roll local orientation into eligible long routes | Route batches using P3 components | FE-P3-07 and FE-P3-09 | Eligible-route audit has no unexplained gaps |
| FE-P4-06 | Rebuild Diagram Gallery information architecture | Gallery route/component/data/controller/styles/tests | FE-P3-06 and FE-P4-03 | Categories/search/featured/details/shared provenance pass |

FE-P4-04 content:

Act 1, What is the idea?

- One visual.
- Three short sentences or equivalent compact editorial unit.
- Ontology stated positively without claiming proof.

Act 2, What exists now?

- Exact effective closure.
- Operational identity with GR.
- Retained ontology.
- Canonical manuscript package.

Act 3, What remains open?

- First-principles substrate recovery.
- Any independently distinct empirical extension.

Terminal actions only:

- Explore the theory.
- See current research status.
- Understand the research method.

### 14.7 P5 route-family rollout packets

Execution order:

1. Physics landing.
2. Physics ontology and exact-GR benchmark.
3. Remaining Physics routes one at a time.
4. AI landing.
5. AI workflow/lifecycle/human-gate pages.
6. AI status/reference pages.
7. Resources landing and Source Authority.
8. Documents/Library/Reading paths.
9. Remaining advanced resource routes.
10. License utility.

Every P5 route packet must:

- Name one route or no more than three tightly coupled routes.
- Assign the primary archetype.
- List the old SVG and CSS selectors being retired.
- Use one approved route-family configuration.
- Include Full/Reduced/Still and mobile profiles.
- Include unique IDs, title, description, caption, and static state.
- Remove animated filter values.
- Confirm lifecycle pause.
- Preserve or improve source closure.
- Update route hashes/provenance if page source changes.
- Run desktop/mobile/still/zoom screenshots.
- Run route-specific and shared-consumer validation.
- Retain a packet-local rollback boundary.

Physics packet exit specifics:

- Continuous-field/geometry identity.
- Solid exact-GR effective layer where relevant.
- Dashed bridge stops at open gate.
- No generic orbit network.
- No scene implies a completed substrate derivation.

AI packet exit specifics:

- Discrete request/token identity.
- Bounded envelope and stop state.
- Source checkpoint.
- Validator return loop.
- Completion/handoff branch.
- Human gate.
- No scene implies AI proof authority.

Resources packet exit specifics:

- One-way source lineage.
- Versions and hashes where relevant.
- Quiet archival surfaces.
- No derivative-to-authority backflow.
- Preserve /resources/source-authority/ as the trust route, but render no
  reusable SourceAuthoritySection or direct SourceNotice section on it or any
  other /resources/ page.

The exact route packet IDs are defined in Section 10. A family packet closes
only when its listed route is complete; a passing landing page does not close
the remaining family.

### 14.8 P6 promotion, discovery, and production packets

| Packet | Goal | Principal targets | Gate |
| --- | --- | --- | --- |
| FE-P6-01 | Produce accessible source-approved 90-second explanation | Video, poster, captions, transcript, media integration | AG-01 and AG-06 |
| FE-P6-02 | Make flagship article and canonical sequence prominent | Home/Theory/Library/Documents | AG-01 |
| FE-P6-03 | Add dated Current Frontier summary and stale behavior | Status data/route/card | AG-01 and source freshness |
| FE-P6-04 | Implement reviewer/challenge path | Reviewer route, contribution docs/channel | AG-09 |
| FE-P6-05 | Add intentional GitHub follow/contribution actions | Header/footer/media/reviewer | Internal-first review |
| FE-P6-06 | Optional project-update retention | Approved service and privacy surfaces | AG-08; otherwise defer |
| FE-P6-07 | Build compact media page | /media/, approved assets/citations | AG-01 and AG-06 |
| FE-P6-08 | Add canonical URL contract | BaseLayout, site origin, tests | AG-04 |
| FE-P6-09 | Add social metadata and project preview images | BaseLayout, assets, route metadata | AG-06 |
| FE-P6-10 | Generate canonical-only sitemap | Astro/static config, tests, robots decision | AG-04 |
| FE-P6-11 | Verify current standards and add accurate structured data | Metadata contract, JSON-LD, validation notes | Standards review |
| FE-P6-12 | Optional privacy-respecting analytics | Minimal events/provider/privacy docs | AG-08; otherwise defer |
| FE-P6-13 | Remove legacy route source files after content, parser, smoke-fixture, and Cloudflare-compatible redirect audit | src/pages/project; public/_redirects; astro redirect config; smoke script/tests; redirect-matrix tests/docs | AG-05 |

FE-P6-01 acceptance:

- Approximately 90 seconds.
- Every spoken or displayed claim maps to a statement ID.
- Captions and transcript are accurate.
- No autoplay with sound.
- Poster loads efficiently.
- Controls are keyboard and VoiceOver accessible.
- Static/transcript path preserves meaning.
- Video does not imply simulation or independent validation.

FE-P6-03 stale-state contract:

- The source commit and as-of date are visible.
- A staleness threshold is configured and documented.
- Stale state changes visible wording and blocks current-language overclaim.
- A missing or invalid source does not silently render the last state as fresh.
- One recommended next step is provided.

FE-P6-04 minimum content:

- Exact open question.
- Canonical background package.
- What evidence would be relevant.
- What claims are out of scope.
- How to submit or inspect.
- Contribution/license terms.
- Code of conduct or conduct expectations.
- Privacy and moderation implications.
- Response-time and review-capacity expectations.

FE-P6-08 through FE-P6-11 must agree on:

- Production site origin.
- Canonical active routes.
- Redirected/retired URLs.
- Advanced indexing policy.
- Media/article page types.
- Filter/query canonical behavior.
- Sitemap inclusion.
- Visible content and structured-data parity.

### 14.9 P7 validation and readiness packets

| Packet | Goal | Evidence | Exit |
| --- | --- | --- | --- |
| FE-P7-01 | Run source/narrative integrity audit across copy, metadata, visuals, captions, alt, media | Claim traceability and physics review | Zero unsafe implication |
| FE-P7-02 | Run first-reader comprehension study | Timed responses and rubric | Approved pass threshold |
| FE-P7-03 | Run keyboard, focus, zoom, and VoiceOver audit | Versioned route matrix and retests | Zero blocker/critical defect |
| FE-P7-04 | Run Chromium, Firefox, Safari/WebKit, and Android responsive audit | Browser/device matrix | Zero blocker/critical defect |
| FE-P7-05 | Run motion lifecycle and performance audit | Profiles, network traces, budgets, CWV lab/field notes | Budgets pass or owner accepts scoped exception |
| FE-P7-06 | Run full repo validation and write release-readiness report | Command logs, clean diff/status, unresolved risk list | Owner accepts or returns repairs |

P7 does not independently validate the project's physics. It validates website
source fidelity, comprehension, accessibility, behavior, performance, and
publication readiness.

## 15. Standard packet template

Every live implementation-control packet should contain:

### Goal

One outcome stated in reader, system, or validation terms.

### Audit trace

- Recommendation IDs.
- Acceptance outcome IDs.
- Preserve constraints.

### Context and evidence

- Baseline finding.
- Exact current files/symbols/routes.
- Source bundle and pinned commit.
- Screenshots or measurements where relevant.

### Allowed reads

- Exact repository paths or bounded directories.
- Upstream reads when required.

### Allowed writes

- Exact files.
- Generated derivatives explicitly named.
- Control records explicitly named.

### Forbidden actions

- Upstream source writes.
- Scientific promotion.
- Unlisted route-family changes.
- Unapproved dependencies/services.
- Git push.
- Deployment.

### Implementation steps

Numbered, smallest-correct-change sequence.

### Acceptance criteria

Objective checkbox list tied to this plan.

### Validation

Exact commands and manual/browser cases.

### Approval gate

Named gate, owner, receipt, and stop behavior.

### Rollback

Files/selectors/routes/data to restore and manifest/provenance regeneration
required after restoration.

### Completion evidence

- Changed files.
- Command results.
- Browser/visual evidence.
- Source and approval receipt.
- Remaining caveats.

### Done when

The packet outcome is achieved, required evidence exists, required validators
pass, the diff is scoped, and the next packet has not been silently started.

## 16. Validation profiles

### 16.1 Important aggregate-command limits

npm run validate currently covers:

- Manifest validation.
- Content-source validation.
- Internal-first links.
- Layout language.
- SVG policy.
- Page provenance.
- Curator check.
- Cloudflare configuration.
- Implementation-control structure.
- Astro build.

It currently omits:

- npm run validate:comprehension.
- Python tests.
- Ruff.
- mypy.

make quality covers its own narrower validation, tests, Ruff, mypy, and the
quality-gate script, but does not replace all npm validators. Do not claim that
one aggregate command covers every gate.

### 16.2 V0 planning/control profile

Use for planning, control, and decision artifacts:

    git diff --check
    npm run validate:implementation-control
    .venv/bin/python -m pytest

Add manual inspection of control YAML/Markdown and verify the active packet
allowlist.

### 16.3 V1 source/content/provenance profile

Use for claim, source bundle, reading order, notice, or route copy changes:

    git diff --check
    npm run validate:content
    npm run validate:manifests
    npm run validate:provenance
    npm run validate:links
    npm run validate:layout
    npm run validate:comprehension
    npm run validate:curator
    npm run validate:implementation-control
    npm run build
    .venv/bin/python -m pytest

Also run the curated statement review and inspect the generated provenance diff.
When this profile changes page provenance or source-bundle evidence, follow the
controlled curator preview, review, write, inspection, and check sequence in
Section 9.24. Do not run curator write mode merely to make a stale check green.

### 16.4 V2 shared component/style/script profile

Use for BaseLayout, header, navigation, EvidenceRail, Figure,
ComprehensionBlocks, archetypes, styles, or lifecycle scripts:

    git diff --check
    npm run validate:layout
    npm run validate:svg
    npm run validate:links
    npm run validate:comprehension
    npm run validate:provenance
    npm run validate:implementation-control
    npm run build
    .venv/bin/python -m pytest
    make lint

Then run representative Home, Physics, AI, Resources, Documents, Gallery, and
long technical route browser checks.

### 16.5 V3 route/visual profile

Use for one reader-facing route:

    git diff --check
    npm run validate:content
    npm run validate:layout
    npm run validate:svg
    npm run validate:links
    npm run validate:comprehension
    npm run validate:provenance
    npm run validate:implementation-control
    npm run build
    .venv/bin/python -m pytest

Manual route cases:

- Desktop Full.
- Desktop Reduced.
- Desktop Still.
- Mobile Full.
- Mobile Reduced.
- Mobile Still.
- Keyboard-only.
- 200 and 400 percent zoom.
- Hidden-tab pause.
- Offscreen pause.
- No console errors.
- Source/claim semantic review.

Because a route-source edit changes the local page hash in provenance, V3 must
also follow Section 9.24: regenerate provenance, preview curator output, stop on
unexpected drift, write the reviewed report, inspect both report files, and run
validate:curator.

### 16.6 V4 asset/media profile

Use for fonts, logos, social images, diagrams, or video:

    git diff --check
    python3 scripts/build_asset_manifest.py --write
    npm run validate:manifests
    npm run validate:content
    npm run validate:svg
    npm run validate:provenance
    npm run validate:curator
    npm run validate:implementation-control
    npm run build
    .venv/bin/python -m pytest

Only run the asset-manifest generator when governed source-manifest inputs or
published asset entries require it. Inspect byte size, dimensions, hashes,
source_ref, license/usage note, and loading behavior.

If an asset/media packet changes route provenance or source declarations seen by
the curator, follow the same preview-before-write sequence. Unexpected upstream
drift is a packet stop condition, not data to overwrite automatically.

### 16.7 V5 navigation/route-retirement profile

Use for IA, route changes, redirects, canonical policy, and legacy deletion:

    git diff --check
    npm run validate:links
    npm run validate:layout
    npm run validate:provenance
    npm run validate:cloudflare
    npm run validate:implementation-control
    npm run build
    .venv/bin/python -m pytest

Start local Astro preview to validate active 200-response routes and built
assets:

    npm run preview -- --host 127.0.0.1

Then:

    python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321

Astro preview does not apply Cloudflare public/_redirects behavior. It therefore
cannot prove legacy redirect status or Location headers. Before deleting legacy
source pages:

1. Update scripts/smoke_test_site.py and its tests so retired routes are not
   incorrectly expected to return 200.
2. Add a deterministic redirect-matrix parser/test for public/_redirects that
   checks source uniqueness, target existence, status, loops, chains, and the
   approved alias ledger.
3. Verify actual HTTP status and Location behavior in a Cloudflare-compatible
   local runtime using the repository-approved current Wrangler Pages command,
   or in a separately authorized preview environment.
4. Record the exact runtime/version and redirect results.
5. If no Cloudflare-compatible verification surface is available, mark redirect
   release verification blocked; do not substitute Astro preview as evidence.

### 16.8 V6 release-candidate profile

Run all explicit gates:

    git diff --check
    npm run validate:comprehension
    npm run validate
    .venv/bin/python -m pytest
    make lint
    npm run quality

Then run:

- Local preview smoke test.
- Source/claim review.
- First-reader comprehension.
- Accessibility/browser/AT/zoom matrix.
- Full/Reduced/Still matrix.
- Offscreen/hidden lifecycle checks.
- Performance budgets.
- Canonical/OG/social/sitemap/structured-data checks.
- Redirect matrix.
- Clean git status and scoped diff review.

If any command is skipped, the release report must identify:

- Command.
- Concrete reason.
- Risk.
- Owner.
- Follow-up packet.
- Whether release is blocked.

## 17. Browser, accessibility, responsive, and motion test matrix

### 17.1 Representative routes

The minimum shared-component matrix includes:

| Role | Route |
| --- | --- |
| Home Story | / |
| Physics Story | /physics/ |
| Public vocabulary | /physics/ontology/ |
| Physics Status | /physics/claim-status/ |
| Open Frontier | /physics/open-burdens/ |
| AI Process | /ai-research-system/workflow/ |
| AI Trust/reference | /ai-research-system/roles-and-schemas/ |
| General-public Story | /resources/guided-starts/general-public/ |
| Library | /resources/documents/ |
| Gallery | /resources/diagrams/ |
| Source trust | /resources/source-authority/ |
| Advanced long page | /resources/site-builder-guide/ |
| Footer/legal | /license/ |

Shared shell changes must inspect every row. Route-local changes inspect the
changed route plus Home and one representative shared consumer.

### 17.2 Viewport matrix

| Profile | Minimum case |
| --- | --- |
| Small phone | 320 by 568 |
| Current phone | 390 by 844 |
| Phone landscape/short height | 844 by 390 or equivalent |
| Tablet portrait | 768 by 1024 |
| Tablet/compact desktop | 1024 by 768 |
| Standard desktop | 1440 by 900 |
| Wide desktop | 1920 by 1080 |
| Browser zoom | 200 percent and 400 percent |
| Text-only enlargement | Browser text enlargement where supported |

Acceptance:

- No horizontal page scroll except intentional labeled data/figure containers.
- No content loss or overlap.
- Menu remains operable in short viewports.
- Focus is never clipped.
- First decision point remains timely.
- Mobile art remains meaningful.
- Table cues remain visible.
- Dialogs fit and scroll internally.

### 17.3 Browser and assistive-technology matrix

| Platform | Required behavior |
| --- | --- |
| Chromium desktop | Full interaction, metadata, motion, performance baseline |
| Firefox desktop | Layout, SVG, disclosure, dialog, focus, motion |
| Safari desktop | Fonts, color scheme, SVG, dialog, sticky/viewport behavior |
| WebKit automated where available | Regression support, not a substitute for Safari manual check |
| Android Chromium | Menu, tables, art, touch targets, orientation |
| macOS VoiceOver with Safari | Landmarks, headings, nav states, links, status strip, dialogs, tables |
| Keyboard-only | Logical focus, skip link, menu, filters, disclosures, dialog, next step |

Record:

- Operating system and version.
- Browser and version.
- Device or emulation.
- Route.
- Viewport/zoom.
- Motion setting.
- Test steps.
- Result.
- Evidence.
- Defect severity.
- Retest result.

### 17.4 Accessibility severity

Recommended severity model:

| Severity | Definition | Release effect |
| --- | --- | --- |
| Blocker | Prevents access to core content/action for keyboard, screen-reader, zoom, or motion-sensitive users | Blocks packet and release |
| Critical | Causes major loss, false state, trap, or unusable primary path | Blocks release |
| Major | Significant difficulty with a reasonable workaround | Requires repair or named owner-approved exception |
| Minor | Local friction without content/function loss | May defer with owner/date |

No compliance claim may be made solely from automated tools. Automated checks
support but do not replace manual keyboard, zoom, VoiceOver, and motion review.

### 17.5 Motion-mode matrix

For every animated figure:

| Test | Full | Reduced | Still |
| --- | --- | --- | --- |
| Meaning present | Required | Required | Required |
| Narrative entrance | Complete | Short opacity/state sequence or omitted | Omitted |
| Ambient transport | Allowed within budget | Removed or materially reduced | None |
| Gate/open state | Visible | Visible | Visible |
| Offscreen pause | Required | Required | No active motion |
| Hidden-document pause | Required | Required | No active motion |
| User preference persists | Required | Required | Required |
| OS default respected before override | Required | Required when OS requests | Required only by explicit choice |
| Static screenshot composed | Settled state | Reduced settled state | Deliberate final state |

### 17.6 Navigation test script

1. Load each representative route at mobile width.
2. Confirm only brand, Menu, and approved utility controls precede main content.
3. Tab to Menu and confirm visible focus.
4. Open with Enter and Space.
5. Confirm aria-expanded changes and controlled panel exists.
6. Navigate nested groups.
7. Confirm current page is announced and visible.
8. Reach every item in a short viewport.
9. Press Escape and confirm close/focus return.
10. Reopen, click outside, and confirm defined close behavior.
11. Rotate or resize while open.
12. Confirm no trapped focus or hidden active element.
13. Repeat with VoiceOver.
14. Repeat at 200 and 400 percent zoom.
15. Disable JavaScript and confirm essential destinations remain accessible.

### 17.7 Table test script

1. Inspect every table inventory row at 320px.
2. Confirm its assigned card or overflow treatment.
3. For overflow tables, confirm instruction and edge cue.
4. Tab to the wrapper and scroll with keyboard.
5. Confirm row/column headers are preserved.
6. Confirm focus outline is visible.
7. Confirm 200 and 400 percent zoom access.
8. For term cards, confirm every original cell value is present with its label.
9. Confirm only one semantic copy is exposed to assistive technology.
10. Confirm print or no-CSS reading remains intelligible where required.

### 17.8 Gallery test script

1. Load default featured/grouped view.
2. Confirm all approved diagrams remain discoverable.
3. Filter by Physics, AI, Operations, and Authority.
4. Search title, keyword, and caption terms.
5. Clear filters.
6. Confirm result count announcement.
7. Open detail with pointer and keyboard.
8. Confirm large preview, description, direct asset link, and contextual
   provenance.
9. Close with Escape and confirm focus return.
10. Confirm group provenance appears once rather than on every card.
11. Confirm below-fold previews lazy-load.
12. Confirm query/filter states follow canonical/index rules.
13. Test no-results state and reset action.
14. Test at mobile width and 400 percent zoom.

## 18. Provisional performance budgets

These are internal project targets, not claims about current external standards.
FE-G0-03 must measure the live baseline and verify current Core Web Vitals and
structured-data guidance against primary sources before the project adopts
final release thresholds.

### 18.1 User-centric budgets

| Metric | Provisional target | Scope |
| --- | ---: | --- |
| Largest Contentful Paint | At or below 2.5 seconds | Representative mobile lab profile and field data when available |
| Cumulative Layout Shift | At or below 0.10 | Entire page lifecycle |
| Interaction to Next Paint | At or below 200 ms | Field data when available; lab interaction proxy otherwise |
| Total Blocking Time | At or below 200 ms | Representative mobile lab run |
| Long tasks caused by site scripts | No unexplained task above 50 ms | Home, menu, gallery, motion control |

### 18.2 Asset and transfer budgets

| Asset class | Provisional target |
| --- | --- |
| Header logo 1x modern format | At or below 30 KB |
| Header logo 2x modern format | At or below 60 KB |
| Header PNG fallback | At or below 100 KB unless measured need justifies more |
| Critical font preload total | At or below 100 KB compressed |
| All initially required font files | At or below 180 KB compressed |
| Initial Home raster-image transfer | At or below 250 KB on the mobile profile |
| One social image | Not part of initial page transfer; optimized to platform need |
| Below-fold comprehension diagrams | Zero eager fetches unless route explicitly marks a first-view exception |
| Remote visual asset requests | Zero |

### 18.3 JavaScript budgets

| Script area | Provisional target |
| --- | --- |
| Global navigation plus motion preference/lifecycle | At or below 20 KB gzip combined |
| Gallery search/filter/detail behavior | At or below 15 KB gzip on Gallery only |
| Route without interactive feature | Does not load that feature's controller |
| Runtime animation dependency | None |
| Third-party analytics/retention script | Zero unless separately approved and budgeted |

### 18.4 CSS budgets

- Final compressed CSS should not exceed the measured baseline without an
  explicit owner-approved reason.
- A packet may not increase route CSS transfer by more than 10 percent without a
  budget review.
- CSS module splitting must improve ownership even if minification recombines
  output.
- Remove obsolete declarations only after selector and visual checks.
- Font and route-family additions must not duplicate core tokens.
- KaTeX/math CSS is measured separately from general UI CSS.

### 18.5 Motion budgets

| Measure | Desktop | Mobile |
| --- | ---: | ---: |
| Concurrent active animated elements in first-view hero | At most 24 provisionally | At most 12 provisionally |
| Mobile evidence particles | Not applicable | 6–10 |
| Animated filter values | 0 | 0 |
| Offscreen active animations | 0 | 0 |
| Hidden-document active animations | 0 | 0 |
| Simultaneously active narrative scenes | 1 preferred; 2 only with documented observer overlap | 1 |
| Target animation smoothness | Sustained near device refresh rate without repeated long frames | Same on approved reference phone |

Frame rate alone is insufficient. Record main-thread cost, paint/composite
behavior, battery/energy proxy where tooling allows, and observed device heat or
degradation during a sustained session.

### 18.6 Route-build budget

- Retiring legacy source routes should reduce built page count by the number of
  removed duplicate sources, adjusted only for approved new media/article
  routes.
- New routes require a reader job, archetype, source bundle, route-map entry,
  provenance entry, metadata, sitemap decision, and owner.
- No hidden redirect-only source page may remain without a documented reason.

## 19. Global acceptance matrix

| ID | Outcome | Pass condition | Evidence |
| --- | --- | --- | --- |
| AC-01 | First-reader comprehension | Approved participants answer five core questions within 20–30 seconds at approved accuracy with no critical false inference | Timed study rubric and notes |
| AC-02 | Focused first viewport | No more than three primary actions; identity/status/action appear promptly on desktop/mobile | Screenshot and action inventory |
| AC-03 | One-click priority content | Flagship theory and current status are each one click from Home | Link-path test |
| AC-04 | Bounded public navigation | Five or fewer choices in every primary public menu group | Data/DOM validation |
| AC-05 | Route-family identity | Physics, AI, Resources stills are correctly identifiable with titles hidden at approved rate | Blind still-frame study |
| AC-06 | Claim traceability | Every promotional statement has accepted source/status mapping | Statement registry and physics receipt |
| AC-07 | Motion modes | Every animated figure has meaningful Full, Reduced, and Still states | Mode screenshots and tests |
| AC-08 | Motion lifecycle | Offscreen/hidden scenes pause and only active scenes resume | Automated/manual lifecycle evidence |
| AC-09 | SVG text policy | No visible SVG text | Strengthened SVG validator |
| AC-10 | SVG accessibility | Every informational SVG has name, title, description, caption, unique IDs, and static state | Validator and accessibility review |
| AC-11 | Mobile art | Core relation is clear without clipping or microscopic geometry | Reference-device screenshots/study |
| AC-12 | Table discovery | No clipped public data lacks an explicit accessible affordance | Table inventory/test matrix |
| AC-13 | Navigation accessibility | Skip link, compact Menu, target size, concise links, focus, current state, Escape all pass | Keyboard/AT/zoom evidence |
| AC-14 | Browser/AT/zoom | Approved browser, Android, VoiceOver, keyboard, and 200–400 percent zoom matrix has no blocker/critical issue | Versioned QA report |
| AC-15 | Performance | Right-sized assets, lazy images, dimensions, no animated filters, pause behavior, and final budgets pass | Network/profile/CWV report |
| AC-16 | Gallery usability | All 37 approved diagrams categorized/searchable; previews/details/provenance accessible and deduplicated | Gallery functional/AT report |
| AC-17 | Long-page orientation | Eligible routes have correct breadcrumbs, TOC, siblings, state, one next step, and disclosure | Route-archetype audit |
| AC-18 | Discovery | Canonicals, social metadata/images, sitemap, and reviewed structured data are valid and aligned | Metadata/crawler/schema tests |
| AC-19 | Governance-safe promotion | No derivation, independent-validation, AI-proof, or source-authority overread | Cross-surface semantic audit |
| AC-20 | Packet quality | Required validators pass after every packet or a concrete blocked/deferred record exists | Packet closeout receipts |

### 19.1 Still-frame identity study

Recommended protocol:

1. Export settled Still states for Home, Physics, AI, and Resources at identical
   dimensions without visible titles.
2. Recruit at least five participants who did not build the visuals.
3. Ask participants to classify Physics, AI, and Resources and explain the cue.
4. Require at least 80 percent correct classification per family provisionally.
5. Treat classifications based only on color as a failure of semantic shape.
6. Record mistaken implications, especially AI crossing the physics gate or
   resources flowing backward into authority.
7. Repair the family grammar before broad rollout.

### 19.2 Claim-semantic visual review

For every source-bearing hero or diagram, reviewers answer:

- What is established/adopted?
- What is interpretive?
- What is open?
- What is not claimed?
- What is the gate?
- Does any arrow cross the gate incorrectly?
- Does any halo imply evidence?
- Does line style agree with status?
- Does caption use explanatory visualization rather than simulation?
- Does Still preserve the same answers?

## 20. Risk register

| Risk | Probability | Impact | Mitigation | Trigger/owner |
| --- | --- | --- | --- | --- |
| Public copy overstates exact closure as derivation | Medium | Critical | Statement registry, physics review, prohibited-inference checklist | Any unreviewed promotional sentence |
| Visual implies AI solves physics | Medium | Critical | Separate audit loop, semantic review, still study | Any AI path crossing aperture |
| Route status appears canonical because sources are canonical | Medium | High | Preserve derivative route classification; schema gate | Proposed status enum/label change |
| Upstream source drift invalidates copy | High over time | High | Clean pinned preflight, hash/provenance regeneration, stale behavior | Hash or registry mismatch |
| Global CSS split changes cascade | High | High | Compatibility entry, staged moves, computed/visual checks | Cross-route screenshot delta |
| Motion abstraction becomes overengineered | Medium | Medium | Home-first minimum API, no library, route fixtures | Primitive exists without two consumers |
| Motion causes nausea or battery cost | Medium | High | Reduced/Still, lifecycle pause, budgets, reference-device profiling | Long frames or user report |
| Still mode freezes an arbitrary phase | Medium | High | Authored static configuration | Missing stillState |
| Duplicate SVG IDs corrupt repeated figures | Medium | High | Required prefix and validator | Duplicate ID/reference finding |
| Mobile art delays actions | Medium | Medium | 180–220px bounded profile and first-viewport review | Action below approved threshold |
| Compact navigation hides advanced routes | Medium | Medium | Advanced/Contributors route, search/links, journey audit | Contributor cannot locate route |
| Mobile menu creates focus trap/double scroll | Medium | High | Native disclosure preference, short-height tests, no premature scroll lock | Keyboard/VoiceOver failure |
| Table cards lose comparisons | Medium | Medium | Type-based treatment and data parity tests | Missing cell or header relation |
| Gallery client filtering hurts indexing/accessibility | Medium | Medium | Static full catalog in HTML, progressive enhancement, canonical policy | No-JS or AT result loss |
| Local font assets increase payload or lack glyphs | Medium | Medium | Subset comparison, Æ glyph test, budgets, fallbacks | Font budget/glyph failure |
| Optimized logo looks soft on high DPR | Low | Medium | 1x/2x variants and zoom/DPR visual QA | Blur at reference display |
| Remote badge replacement loses useful live state | Low | Low | Replace with explicit text/action; do not promise live status | Stakeholder requests dynamic badge |
| Structured data misrepresents the project | Medium | High | Current official-standard review and visible-content parity | Validator or semantic discrepancy |
| Analytics/retention creates privacy burden | Medium | High | Default defer; AG-08; data minimization and removal | Provider or form proposed |
| Reviewer path creates unbounded support expectation | Medium | Medium | Scope, moderation, response policy, read-only fallback | No accountable review owner |
| Legacy route deletion breaks inbound links | Medium | High | Per-route ledger, retained redirects, smoke tests | 404 or lost anchor |
| New route count replaces removed duplication | Low | Medium | Reader-job and route-build budget | Route lacks source/archetype/owner |
| Aggregate validation hides omitted checks | High | Medium | Explicit V6 command list | Closeout cites only npm run validate |
| Curator drift blocks otherwise valid frontend packet | Medium | Medium | Inspect exact error, distinguish related/unrelated, record concrete blocker | validate:curator failure |
| Active unrelated implementation packet conflicts | High initially | High | Checkpoint it under its own authority as an external precondition, then open FE-G0-01 | Resolver does not expose frontend packet |
| Deployment occurs before acceptance | Low | Critical | Separate AG-10/AG-11 and push-and-deploy workflow | Any Wrangler/push action in packet |

## 21. Rollout and rollback strategy

### 21.1 Rollout

1. Work on a dedicated codex-prefixed branch or owner-approved branch after the
   live control transition.
2. Land validator/guard changes before broad selector or component migrations.
3. Correct source/narrative surfaces before visual promotion.
4. Release the Home prototype to local/review environments only.
5. Require explicit Home prototype PASS.
6. Migrate one route family in bounded packets.
7. Keep old CSS aliases until all family consumers move.
8. Complete IA and canonical metadata before sitemap/structured-data release.
9. Retire legacy source routes only after active replacements pass.
10. Run P7 full system QA.
11. Stop at the release gate. Push/deployment require separate approval.

### 21.2 Feature staging

This static site does not require a runtime flag service. Use:

- Branch boundary.
- Route/component adoption.
- Compatibility CSS aliases.
- Review-only local/preview builds.
- Manifest publication status.
- Owner review status.
- Deployment authorization.

Avoid introducing a feature-flag dependency solely for this redesign.

### 21.3 Packet rollback

Content/source packet:

- Restore route copy and route-map row.
- Regenerate page provenance.
- Re-run V1.
- Confirm no source notice or hash remains from the reverted state.

Shared component/CSS packet:

- Restore component and compatibility selectors together.
- Rebuild all representative routes.
- Re-run V2 and screenshots.

Asset packet:

- Restore markup and old local asset reference.
- Restore source/asset manifest rows and hashes.
- Rebuild asset manifest.
- Re-run V4.

Navigation/route packet:

- Restore navigation data, redirects, and canonical policy as one transaction.
- Rebuild.
- Re-run V5 and redirect matrix.

Motion packet:

- Restore component config, lifecycle hooks, and styles together.
- Ensure default behavior falls back to Still/Reduced rather than leaving an
  uncontrolled partial scene.
- Re-run motion matrix.

### 21.4 System rollback

If cross-family rollout reveals a fundamental problem:

1. Stop new route packets.
2. Keep accepted P0 source corrections unless they are independently wrong.
3. Keep confirmed P1 accessibility fixes unless the fix itself regressed.
4. Revert the shared visual system to the last accepted Home prototype or
   pre-prototype state.
5. Restore compatibility selectors.
6. Regenerate route hashes/provenance for restored page files.
7. Run full V6 before any public release.

## 22. Definition of done

### 22.1 Per-packet definition

- Scope matches one live packet.
- Allowed writes are exact.
- Source basis is pinned.
- Recommendation IDs are traced.
- Required approval exists.
- Implementation is smallest-correct and reversible.
- Relevant static routes build.
- Public manifests are updated when applicable.
- Page and asset hashes are regenerated when applicable.
- Internal-first navigation is preserved.
- /resources/source-authority/ remains the trust route, and no /resources/ page
  renders the forbidden reusable SourceAuthoritySection or direct SourceNotice
  section.
- No visible SVG text exists.
- Informational SVG accessibility and motion state pass.
- Desktop/mobile/zoom/motion checks are recorded.
- Required automated gates pass.
- Unrelated dirty files remain untouched.
- Checkpoint evidence is complete.
- No push or deployment occurs without authorization.

### 22.2 Final program checklist

Source and narrative:

- [ ] Canonical document order is correct everywhere.
- [ ] Home and Physics source bundles include overview, note, and flagship.
- [ ] Claim ladder has six source-reviewed states.
- [ ] Every promotional statement is traceable.
- [ ] Physics-owner acceptance exists.
- [ ] No derivation, validation, prediction, or AI-proof overread remains.

Brand and system:

- [ ] Header leads with The Æther Flow and retains By Angry Owl.
- [ ] Remote visual badges/assets are removed.
- [ ] Logo variants are right-sized.
- [ ] Fonts are self-hosted, licensed, and budgeted.
- [ ] Tokens cover type, containers, space, radius, z, motion, easing, measure.
- [ ] Main/header alignment is deliberate.
- [ ] Narrative reading measure is 62–68ch.
- [ ] Glow usage is semantically limited.
- [ ] global.css responsibilities are split with documented import order.

Accessibility and responsive:

- [ ] Skip link appears above header.
- [ ] One compact mobile Menu works.
- [ ] Menu height is viewport safe.
- [ ] Desktop targets meet the approved size.
- [ ] EvidenceRail link names are concise.
- [ ] Tables use cards or explicit accessible overflow.
- [ ] Native dark scheme is correct.
- [ ] Focus, current state, disclosure, landmarks, headings, captions, Escape are
      preserved.
- [ ] Keyboard, VoiceOver, Safari, Firefox, Android, and 200–400 percent zoom
      pass.

Motion and visuals:

- [ ] Home narrative prototype passed before scaling.
- [ ] Physics, AI, and Resources still frames are distinct.
- [ ] Motion uses deterministic local variation.
- [ ] Timing reflects semantic profiles.
- [ ] Coherent motion is described as explanatory visualization, not simulation.
- [ ] Adoption versus derivation is visually explicit.
- [ ] No animated filter values remain.
- [ ] Offscreen and hidden-document motion pauses.
- [ ] Full, Reduced, and Still are visible and persistent.
- [ ] Mobile art uses an authored reduced-density profile.
- [ ] Reusable primitives have unique IDs and typed configuration.
- [ ] SVG validator covers accessibility, states, IDs, filters, and pause policy.
- [ ] All informational SVGs have title/description/caption/static state.
- [ ] No AI or Resources route relies on physics-greenfield-svg.

Information architecture:

- [ ] Five public destinations are approved and implemented.
- [ ] Source Authority is a persistent trust utility.
- [ ] Advanced/Contributors owns low-level technical routes.
- [ ] Primary groups have five or fewer choices.
- [ ] General-public route has three acts and three terminal actions.
- [ ] All active routes have archetypes.
- [ ] Eligible long routes have local orientation.
- [ ] Diagram Gallery has categories, search, hierarchy, larger previews,
      accessible details, and deduplicated provenance.

Promotion/discovery:

- [ ] Source-approved 90-second explanation exists or is explicitly deferred.
- [ ] Flagship article is one click away.
- [ ] Dated Current Frontier exists with stale behavior.
- [ ] Canonical sequence entry is prominent.
- [ ] Reviewer/challenge path exists with accountable scope or is explicitly
      deferred.
- [ ] GitHub action is clear and external/provenance-labeled.
- [ ] Retention is implemented only if approved; otherwise no fake form exists.
- [ ] Media page has approved summary, creator, assets, citations, and boundary.
- [ ] Canonical URLs are correct.
- [ ] Social metadata/images are correct.
- [ ] Sitemap contains canonical indexable routes only.
- [ ] Structured data was verified against current official standards.
- [ ] Analytics is approved/minimal/privacy-safe or explicitly deferred.

Performance/maintenance:

- [ ] Below-fold diagrams are lazy.
- [ ] Images reserve dimensions/aspect ratios.
- [ ] No remote visual request remains.
- [ ] Legacy source routes are removed or explicitly retained with rationale.
- [ ] SVG migration occurred in bounded families.
- [ ] Final performance budgets pass.
- [ ] Full explicit validation chain passes.

## 23. Out of scope unless separately authorized

- Editing /Volumes/P-SSD/AngryOwl/The-AEther-Flow.
- Changing registered scientific, mathematical, ontology, or governance sources.
- Claim promotion, adoption, or protected physics verdicts.
- Independent scientific validation.
- New backend or database.
- User accounts.
- Unapproved newsletter, form, analytics, or tracking provider.
- Unapproved paid media production.
- Unapproved third-party animation or UI framework.
- Git push.
- Pull request creation.
- Cloudflare deployment.
- Production monitoring changes beyond an approved packet.

## 24. Logical first implementation packet

The logical next implementation action is not a CSS or Home edit.

1. External precondition: validate and checkpoint WI-20260702-001 under that
   packet's existing authority. Do not treat this as frontend work.
2. Execute FE-G0-01 as a separately authorized plan-adoption/control-transition
   packet that allowlists this plan and its new control records only.
3. Open the first bounded frontend-recommendations baseline packet.
4. Execute FE-G0-02 through FE-G0-05.
5. Begin FE-P0-01 source pinning.
6. Do not begin the visual prototype until P0 claim review passes.

The first user-visible change should be FE-P0-02 or FE-P1-02, depending on the
fresh control packet's dependency order:

- FE-P0-02 corrects a content-integrity defect.
- FE-P1-02 corrects a confirmed keyboard accessibility defect.

Both are small, testable, reversible, and do not require broad visual-system
approval.

## 25. Can the plan be improved?

Yes, through evidence rather than added scope:

1. Replace provisional performance targets with measured baseline-relative
   budgets.
2. Replace open font choices with a visual/licensing comparison.
3. Replace proposed IA mappings with an approved route decision ledger.
4. Replace provisional comprehension thresholds with an approved study design.
5. Replace inferred owner roles with named reviewers and receipt formats.
6. Add automated browser fixtures for navigation, motion lifecycle, gallery,
   metadata, and table affordance after component APIs stabilize.
7. Add a machine-readable recommendation-to-packet registry if implementation
   control will consume it directly.
8. Add a final packet index that links every completion receipt after execution.

These improvements should occur inside G0 and the relevant implementation
packets. They do not justify delaying the confirmed source-order, skip-link, or
navigation defects once governance is ready.

## 26. APA 7 references

*Frontend audit conclusion*. (2026, July 11). [Internal frontend audit supplied
by the project owner]. [Internal
attachment](/Users/alex.omegapy/.codex/attachments/98312d76-c284-4a39-ba6d-6758b9002932/pasted-text.txt)

The Æther Flow Project. (2026a). *The Æther Flow ontology: Exact-closure
sequence overview* [TeX manuscript]. [Local registered
copy](../public/files/tex/ontology/aether_flow_exact_closure_sequence_overview.tex)

The Æther Flow Project. (2026b). *The Æther Flow ontology: Exact-closure note*
[TeX manuscript]. [Local registered
copy](../public/files/tex/ontology/aether_flow_exact_closure_note.tex)

The Æther Flow Project. (2026c). *The Æther Flow ontology: Exact-closure
flagship article* [TeX manuscript]. [Local registered
copy](../public/files/tex/ontology/aether_flow_exact_closure_flagship_article.tex)

The Æther Flow Website. (2026a). *AGENTS.md instructions* [Repository operating
rules]. [Repository file](../AGENTS.md)

The Æther Flow Website. (2026b). *Page route map* [JSON manifest].
[Repository file](../public/files/manifests/page_route_map.json)

The Æther Flow Website. (2026c). *Page provenance* [JSON manifest].
[Repository file](../public/files/manifests/page_provenance.json)

The Æther Flow Website. (2026d). *Source manifest* [JSON manifest].
[Repository file](../public/files/manifests/source_manifest.json)

The Æther Flow Website. (2026e). *Website positioning guidance* [Draft product
requirements document; non-authoritative planning context]. [Repository
file](../PRDs/website-information-space/PRD-10-website-positioning-guidance.md)

The Æther Flow Website. (2026f). *High-level components* [Draft product
requirements document; non-authoritative planning context]. [Repository
file](../PRDs/website-information-space/PRD-01-high-level-components.md)

The Æther Flow Website. (2026g). *Sitewide page revamp* [Non-authoritative
implementation-planning context]. [Repository
file](sitewide_page_revamp_implementation_plan.md)

The Æther Flow Website. (2026h). *Master website information-space
implementation plan* [Non-authoritative implementation-planning context].
[Repository
file](website-information-space/PRD-00-master-website-information-space-implementation-plan.md)

## Appendix A. Coverage checksum

- Source/narrative implementation units: 11.
- Brand/layout implementation units: 10.
- Motion/SVG implementation units: 12.
- Information-architecture implementation units: 10.
- Promotion/discovery implementation units: 13.
- Accessibility/responsive implementation units: 9.
- Performance/maintainability implementation units: 8.
- Total distinct recommendation implementation units: 73.
- Sequenced delivery phases/gates: 9 implementation phases plus per-packet
  checkpoint discipline.
- Preserve/do-not-regress constraints: 12 recorded in Section 4.4.
- Global acceptance outcomes: 20.
- Active route dispositions: 34.
- Legacy source-route dispositions: 30.
- Open implementation decisions: 30.
- Required approval gates: 11.

All 27 numbered audit recommendations, all unnumbered promotional/discovery
recommendations, all accessibility/responsive recommendations, all
performance/maintainability recommendations, all audit phases, all stated
acceptance criteria, and all audit limitations are represented in this plan.

## Appendix B. Audit-to-plan crosswalk

### B.1 Numbered recommendations

| Audit recommendation | Plan coverage | Primary packets |
| --- | --- | --- |
| 1. Correct canonical document sequence | S-02; Sections 3.3 and 9.3 | FE-P0-02 |
| 2. Expand Home and Physics source bundles | S-03 through S-05; Sections 3.2–3.5 | FE-P0-01, FE-P0-03, FE-P0-04, FE-P0-05 |
| 3. Reframe around exact closure/open foundation | S-06 through S-08; Sections 5.1–5.2 | FE-P0-05, FE-P0-06 |
| 4. Add immediate status strip | S-09; Sections 5.3 and 9.3 | FE-P0-07 |
| 5. Lead positively, then state limits | S-10; Sections 9.8 and 14.2 | FE-P0-06, FE-P3-06, FE-P3-07 |
| 6. Make Æther Flow the visible product brand | B-01; Sections 9.6 and 14.4 | FE-P2-01 |
| 7. Preserve palette with stricter meaning | B-02 through B-04; Sections 5.4–5.5 | FE-P2-02, FE-P3-03 |
| 8. Create distinct route-family silhouettes | B-05; Section 5.6 | FE-P5-PHY, FE-P5-AI, FE-P5-RES route packets |
| 9. Introduce distinctive type system | B-06; Section 9.18 | FE-P3-01, FE-P3-02 |
| 10. Formalize non-color tokens | B-07; Sections 9.17 and 14.5 | FE-P3-03 |
| 11. Reduce width and add narrative pauses | B-08 and B-09; Sections 9.8 and 9.17 | FE-P3-05, FE-P3-06 |
| 12. Reserve glow for meaning | B-10; Section 9.19 | FE-P3-05 and route packets |
| 13. Build narrative Home animation | M-01; Section 9.15 | FE-P2-03 through FE-P2-07 |
| 14. Replace synchronized group motion | M-02 and M-03; Sections 9.13–9.15 | FE-P2-03, FE-P3-08 |
| 15. Make motion coherent without calling it simulation | M-04; Sections 9.13 and 19.2 | FE-P2-04 and family packets |
| 16. Represent adoption versus derivation visually | M-05; Sections 5.5–5.6 and 9.15 | FE-P2-04, FE-P5-PHY |
| 17. Stop animating filter values | M-06; Sections 9.13 and 18.5 | FE-P1-08, FE-P2-04, family packets |
| 18. Pause motion outside current scene | M-07; Section 9.14 | FE-P1-09 |
| 19. Add visible motion preference | M-08; Sections 9.14 and 17.5 | FE-P1-09 |
| 20. Design mobile artwork separately | M-09; Section 9.16 | FE-P2-05 and family packets |
| 21. Create reusable motion architecture | M-10; Sections 9.2 and 9.13 | FE-P2-03, FE-P3-08 |
| 22. Strengthen SVG validation | M-11 and M-12; Section 9.23 | FE-P1-08, FE-P1-10, FE-P3-08 |
| 23. Restructure public navigation | IA-01 through IA-05; Sections 9.6–9.7 | FE-P1-03, FE-P4-01 through FE-P4-03 |
| 24. Turn general-public page into three acts | IA-06; Section 14.6 | FE-P4-04 |
| 25. Define five page archetypes | IA-07; Section 9.8 | FE-P3-06, FE-P3-09 |
| 26. Add local orientation to long pages | IA-08; Section 9.9 | FE-P3-07, FE-P4-05 |
| 27. Rebuild Diagram Gallery | IA-09 and IA-10; Section 9.20 | FE-P4-06 |

### B.2 Promotional and discovery bullets

| Audit bullet | Plan coverage | Primary packet |
| --- | --- | --- |
| 90-second visual explanation | P-01; Section 9.21 | FE-P6-01 |
| Prominent flagship article | P-02 | FE-P6-02 |
| Dated current-frontier summary | P-03 | FE-P6-03 |
| Canonical manuscript-sequence entry | P-04 | FE-P0-02, FE-P6-02 |
| Reviewer/challenge path | P-05 | FE-P6-04 |
| GitHub follow/contribution action | P-06 | FE-P6-05 |
| Approved update/retention functionality | P-07 | FE-P6-06 or explicit defer |
| Compact media page | P-08 | FE-P6-07 |
| Canonical URLs | P-09 | FE-P6-08 |
| Project social images and metadata | P-10 | FE-P6-09 |
| Sitemap | P-11 | FE-P6-10 |
| Current-standard-reviewed structured data | P-12 | FE-P6-11 |
| Approved privacy-respecting analytics | P-13 | FE-P6-12 or explicit defer |

### B.3 Accessibility and responsive bullets

| Audit bullet | Plan coverage | Primary packet |
| --- | --- | --- |
| Raise skip link above header | A-01 | FE-P1-02 |
| One accessible mobile Menu | IA-04 | FE-P1-03 |
| Viewport-safe large menus | IA-05 | FE-P1-03 |
| 40–44px desktop nav targets | A-02 | FE-P1-04 |
| Concise EvidenceRail accessible links | A-03 | FE-P1-05 |
| Table wrappers/instructions or public cards | A-04 | FE-P1-06 |
| Native dark color-scheme behavior | A-05 | FE-P1-01 |
| Preserve focus and Escape behavior | A-06 | FE-P1-03, FE-P1-04 |
| Complete title/description coverage | A-07 | FE-P1-08 |
| Keyboard/zoom/VoiceOver/browser/Android/motion testing | A-08 and A-09 | FE-G0-04, FE-P7-03, FE-P7-04 |

### B.4 Performance and maintainability bullets

| Audit bullet | Plan coverage | Primary packet |
| --- | --- | --- |
| Right-size the 1.1 MB logo | R-01 | FE-P2-01 |
| Split 4,382-line global CSS | R-02 | FE-P3-04 |
| Lazy-load comprehension diagrams | R-03 | FE-P1-07 |
| Add intrinsic image dimensions/aspect ratios | R-04 | FE-P1-07 |
| Replace remote badges/creator assets | R-05 | FE-P2-01 |
| Retire duplicate legacy project routes | R-06 | FE-P6-13 |
| Migrate SVGs in bounded families | R-07 | P5 route packets |
| Define and measure performance budgets | R-08 | FE-G0-03, FE-P2-07, FE-P7-05 |

### B.5 Audit limitations converted to work

| Audit limitation | Plan response |
| --- | --- |
| Full accessibility compliance not established | FE-G0-04 establishes a target; FE-P7-03 runs evidence-based audit |
| Safari, Firefox, Android, and assistive-technology behavior not established | Section 17 matrix and FE-P7-03/04 |
| Reduced-motion behavior not dynamically established | FE-P1-09 plus Section 17.5 |
| Frame rate and battery cost not measured | FE-G0-03 and FE-P7-05 |
| Production Core Web Vitals not established | Section 18 and FE-P7-05 |
| Independent physics validation not established | Explicitly out of scope; source-fidelity review only |

## Appendix C. P5 route-packet actionability

### C.1 Shared interpretation

The table below turns every P5 route ID into an implementation-ready boundary.
The listed selector families are migration candidates, not permission for a
global search-and-replace. Each packet must confirm the live selectors used by
its route before writing.

Validation shorthand:

- V1 means the source/content/provenance profile in Section 16.3.
- V3 means the route/visual profile in Section 16.5.
- V4 means the governed asset profile in Section 16.6.
- RQ means the resource-specific layout/quality prohibition and contextual
  provenance review.

Every route-source change requires page-provenance regeneration and the
curator preview-before-write sequence. Every rollback restores the route source,
its route-family configuration, packet-local CSS, and any changed shared data
as one transaction, then regenerates provenance/curator reports and reruns the
listed validation.

### C.2 Physics route packets

| Packet | Route and exact primary write | Dependencies | Selector/component boundary | Validation | Rollback |
| --- | --- | --- | --- | --- | --- |
| FE-P5-PHY-01 | /physics/ — src/pages/physics/index.astro | P0 accepted; FE-P3-08; FE-P4-03 | Replace physics-greenfield-svg, physics-grid, physics-glow, track-figure-path/core/nodes with approved Physics MotionDiagram config | V1 + V3; blind still check | Restore landing, Physics config, packet CSS aliases, source notice, provenance/curator |
| FE-P5-PHY-02 | /physics/ontology/ — src/pages/physics/ontology/index.astro | FE-P1-06 ontology table pilot; FE-P5-PHY-01 | Use Story/Trust composition; replace generic figure hooks; retain TermCardGrid/OverflowTable decision | V1 + V3; table/zoom matrix | Restore route, term/table data, figure config, CSS, provenance/curator |
| FE-P5-PHY-03 | /physics/exact-gr-benchmark/ — src/pages/physics/exact-gr-benchmark/index.astro | FE-P0-05; FE-P5-PHY-01 | Exact-GR solid layer and open derivation bridge; retire generic orbit/path classes only on route | V1 + V3; claim-semantic review | Restore route/config/CSS and accepted statement IDs, then provenance/curator |
| FE-P5-PHY-04 | /physics/derivation-roadmap/ — src/pages/physics/derivation-roadmap/index.astro | FE-P5-PHY-03; Status archetype fixture | StatusDashboardPage, AuthorityGate, stopped dashed bridge; no proof/progress bar | V1 + V3; freshness/status test | Restore route/status data/config/CSS, provenance/curator |
| FE-P5-PHY-05 | /physics/flow-geometry/ — src/pages/physics/flow-geometry/index.astro | FE-P5-PHY-01; approved geometry grammar | Continuous field/curvature/perturbed trajectory config; remove generic orbital nodes | V1 + V3; motion/performance profile | Restore route/geometry config/CSS and provenance/curator |
| FE-P5-PHY-06 | /physics/claim-status/ — src/pages/physics/claim-status/index.astro | FE-P0-05; Status archetype fixture | Quiet status states, gate semantics, accessible matrices/disclosure | V1 + V3; claim registry parity | Restore route/status data/disclosure/CSS, provenance/curator |
| FE-P5-PHY-07 | /physics/open-burdens/ — src/pages/physics/open-burdens/index.astro | FE-P5-PHY-04 and FE-P5-PHY-06 | Open Frontier dashboard, one next gate, dated state; no completion percentage | V1 + V3; stale-state test | Restore route/status source/config/CSS, provenance/curator |

### C.3 AI Research System route packets

| Packet | Route and exact primary write | Dependencies | Selector/component boundary | Validation | Rollback |
| --- | --- | --- | --- | --- | --- |
| FE-P5-AI-01 | /ai-research-system/ — src/pages/ai-research-system/index.astro | FE-P3-08; FE-P4-03 | Remove physics-greenfield-svg; use discrete token/envelope/source/return/handoff/gate config | V3; no-AI-proof semantic review; blind still check | Restore landing, AI config, ai/track CSS aliases, provenance/curator |
| FE-P5-AI-02 | /ai-research-system/current-state/ — src/pages/ai-research-system/current-state/index.astro | Status archetype; FE-P5-AI-01 | Dated operational StatusDashboard; quiet records; no cosmic orbit | V1 + V3; stale-state test | Restore route/snapshot/config/CSS, provenance/curator |
| FE-P5-AI-03 | /ai-research-system/workflow/ — src/pages/ai-research-system/workflow/index.astro | Process archetype; FE-P5-AI-01 | Request token to source checkpoint to bounded job to return/handoff | V1 + V3; process order and stop-state check | Restore route/workflow config/CSS, provenance/curator |
| FE-P5-AI-04 | /ai-research-system/agentjob-lifecycle/ — src/pages/ai-research-system/agentjob-lifecycle/index.astro | FE-P5-AI-03 | Bounded envelope with allowlist, validator, completion, handoff; retire orbit/core hooks | V1 + V3; accessible sequence review | Restore route/config/CSS, provenance/curator |
| FE-P5-AI-05 | /ai-research-system/roles-and-schemas/ — src/pages/ai-research-system/roles-and-schemas/index.astro | Trust archetype; FE-P5-AI-01 | Quiet authority stack; role labels never become authority through glow | V1 + V3; authority-language audit | Restore route/data/config/CSS, provenance/curator |
| FE-P5-AI-06 | /ai-research-system/human-gated-promotion/ — src/pages/ai-research-system/human-gated-promotion/index.astro | FE-P5-AI-03; approved gate grammar | Explicit human aperture, stopped state, protected decision | V1 + V3; gate/Escape/motion review | Restore route/gate config/CSS, provenance/curator |
| FE-P5-AI-07 | /ai-research-system/validators-and-handoffs/ — src/pages/ai-research-system/validators-and-handoffs/index.astro | FE-P5-AI-03 | Validator return loop and bounded PASS; no proof halo | V1 + V3; false-inference audit | Restore route/config/CSS, provenance/curator |
| FE-P5-AI-08 | /ai-research-system/memory-preflight/ — src/pages/ai-research-system/memory-preflight/index.astro | Trust/Process archetype | Retrieval token points to canonical inspection; no reverse authority | V1 + V3; source-first path review | Restore route/config/CSS, provenance/curator |
| FE-P5-AI-09 | /ai-research-system/project-system-improvement/ — src/pages/ai-research-system/project-system-improvement/index.astro | FE-P5-AI-03 | Maintenance return loop with bounded stop/defer/reject outcomes | V1 + V3; maintenance/research boundary | Restore route/config/CSS, provenance/curator |
| FE-P5-AI-10 | /ai-research-system/runtime-requirements/ — src/pages/ai-research-system/runtime-requirements/index.astro | Trust archetype; FE-P5-AI-01 | Quiet tool/environment evidence; move to Advanced navigation | V1 + V3; advanced-path discovery | Restore route/navigation/config/CSS, provenance/curator |

### C.4 Resources and trust route packets

| Packet | Route and exact primary write | Dependencies | Selector/component boundary | Validation | Rollback |
| --- | --- | --- | --- | --- | --- |
| FE-P5-RES-01 | /resources/ — src/pages/resources/index.astro | FE-P4-02/03; Library archetype | Remove physics-greenfield-svg/ai-greenfield-page leakage; establish one-way lineage and Advanced entry | V1 + V3 + RQ | Restore landing/nav/config/CSS, provenance/curator |
| FE-P5-RES-02 | /resources/guided-starts/ — src/pages/resources/guided-starts/index.astro | FE-P4-04; Library archetype | Audience path selection; no repeated authority boilerplate | V1 + V3 + RQ | Restore route/data/config/CSS, provenance/curator |
| FE-P5-RES-03 | /resources/source-authority/ — src/pages/resources/source-authority/index.astro | Trust archetype; FE-P5-RES-01 | Preserve trust route through contextual copy; do not add forbidden SourceAuthoritySection/SourceNotice component; quiet lineage visual | V1 + V3 + RQ | Restore route/config/CSS, provenance/curator |
| FE-P5-RES-04 | /resources/registries/ — src/pages/resources/registries/index.astro | FE-P4-02 Advanced grouping | Quiet registry reference; hashes/status do not glow as proof | V1 + V3 + RQ | Restore route/navigation/config/CSS, provenance/curator |
| FE-P5-RES-05 | /resources/generated-derivatives/ — src/pages/resources/generated-derivatives/index.astro | FE-P5-RES-03 | One-way source-to-derivative-to-reader chain; no backflow | V1 + V3 + RQ | Restore route/config/CSS, provenance/curator |
| FE-P5-RES-06 | /resources/retrieval-layers/ — src/pages/resources/retrieval-layers/index.astro | FE-P4-02 Advanced grouping | Retrieval as navigation aid pointing to source inspection | V1 + V3 + RQ | Restore route/navigation/config/CSS, provenance/curator |
| FE-P5-RES-07 | /resources/publication-process/ — src/pages/resources/publication-process/index.astro | Process archetype; FE-P5-RES-03 | Source to brief/review/manifest/reader one-way workflow | V1 + V3 + RQ | Restore route/config/CSS, provenance/curator |
| FE-P5-RES-08 | /resources/library/ — src/pages/resources/library/index.astro | FE-P0-02; Library archetype | Featured reader jobs, canonical sequence entry, accessible data treatment | V1 + V3 + RQ | Restore route/library data/config/CSS, provenance/curator |
| FE-P5-RES-09 | /resources/reading-paths/ — src/pages/resources/reading-paths/index.astro | FE-P4-04; FE-P5-RES-08 | Compact public/specialist paths and one recommended next step | V1 + V3 + RQ | Restore route/path data/config/CSS, provenance/curator |
| FE-P5-RES-10 | /resources/repository-map/ — src/pages/resources/repository-map/index.astro | FE-P4-02 Advanced grouping | Public-safe one-way topology; no repository archaeology first | V1 + V3 + RQ | Restore route/navigation/config/CSS, provenance/curator |
| FE-P5-RES-11 | /resources/site-builder-guide/ — src/pages/resources/site-builder-guide/index.astro | FE-P3-07; FE-P4-02 | Long-page orientation, builder rules, quiet technical visual | V1 + V3 + RQ | Restore route/navigation/orientation/config/CSS, provenance/curator |
| FE-P5-RES-12 | /license/ — src/pages/license/index.astro | Brand/footer packet FE-P2-01 | Quiet Trust/reference utility; verify footer path and creator attribution | V1 + V3 | Restore route/footer/CSS, provenance/curator |

## Appendix D. P6 packet actionability

| Packet | Exact default writes | Dependencies/approval | Validation | Rollback boundary |
| --- | --- | --- | --- | --- |
| FE-P6-01 | public/assets/media approved exports; transcript/caption/poster files; src/components/media/AccessibleVideo.astro; approved Home/media integration; source/asset manifests | FE-P0-05; FE-P2-07; AG-01; AG-06; D-25 | V1 + V3 + V4; caption/transcript; reduced/static; media network budget | Remove integration; restore media component/assets and manifest rows together; regenerate asset/page evidence |
| FE-P6-02 | src/pages/index.astro; src/pages/physics/index.astro; src/pages/resources/documents.astro; src/pages/resources/library/index.astro; shared sequence/statement data | FE-P0-02/05; AG-01; default reuses existing routes | V1 + affected-route V3; one-click path | Restore CTA/sequence entries and statement IDs; regenerate provenance/curator |
| FE-P6-03 | Default: src/pages/physics/open-burdens/index.astro plus dated source data/statement IDs; conditional new route only through Section 10.1 | Freshness owner; AG-01; source preflight | V1 + V3; stale/missing/invalid-state fixtures | Restore prior status data/route; remove conditional route row if created; regenerate provenance/curator |
| FE-P6-04 | src/pages/resources/reviewer-packet/index.astro; contribution/conduct/contact metadata; optional issue/discussion templates only if approved | FE-P5-PHY-07; AG-09; D-26 | V1 + V3 + RQ; channel/moderation/privacy review | Restore read-only packet; remove unapproved submission mechanism and related metadata |
| FE-P6-05 | src/layouts/BaseLayout.astro or extracted footer/header components; local icon assets; contribution link data | FE-P2-01; approved repository/action meaning | V2 + V4 if assets; external-link and internal-first audit | Restore prior local links/assets; never restore remote visual requests without approval |
| FE-P6-06 | No default writes; provider-specific allowlist, privacy copy, form/service config, and tests defined only after AG-08 | AG-08; owner/provider/consent/retention/delete decisions | Provider-specific security/privacy/accessibility/performance plus V2/V3 | Remove form/script/provider config and published data endpoint; preserve no fake form |
| FE-P6-07 | src/pages/media/index.astro; route map; generated provenance/curator; route metadata; approved assets; navigation/footer link data | FE-P0-05; FE-P2-01; AG-01; AG-06 | V1 + V3 + V4 + canonical/sitemap tests | Remove route/link/route-map row/assets as one transaction; regenerate provenance/curator/sitemap |
| FE-P6-08 | astro.config.mjs or validated site-origin config; BaseLayout metadata props; route metadata data/tests | FE-P4-01; production origin D-03; AG-04 | V2 + V5; one canonical per active route; redirects excluded | Restore metadata contract/config together; remove incorrect canonicals before release |
| FE-P6-09 | BaseLayout social props; approved social images under public/assets; route metadata; source/asset manifests | FE-P6-08; AG-06 | V2 + V4; metadata/image dimension/crop tests | Restore default metadata and remove image/manifest rows together |
| FE-P6-10 | astro.config.mjs or approved sitemap generator/config; public/robots.txt if policy requires; sitemap tests | FE-P6-08; AG-04; final active-route ledger | V5; canonical 200-only sitemap audit | Remove generator/config and robots reference together; restore prior robots file |
| FE-P6-11 | BaseLayout safe JSON-LD serializer; route structured-data objects; standards decision record/tests | FE-P6-08; current primary-source standards review | V2 + schema/visible-content parity; no claim inflation | Remove invalid JSON-LD objects/serializer output without affecting visible content |
| FE-P6-12 | No default writes; minimal provider/module/event taxonomy/privacy docs/tests only after AG-08 | AG-08; D-24; performance budget | Provider/privacy/security/performance and event-payload audit | Remove script/provider/event hooks and stored identifiers; verify zero residual requests |
| FE-P6-13 | src/pages/project subtree; public/_redirects; astro.config.mjs redirect parity; scripts/smoke_test_site.py; focused smoke/redirect tests; route docs | All active targets accepted; AG-05 | V5 plus Cloudflare-compatible status/Location matrix and target build-count check | Restore deleted route files and old smoke expectations only as one reviewed rollback; retain redirects; rebuild/provenance check |
