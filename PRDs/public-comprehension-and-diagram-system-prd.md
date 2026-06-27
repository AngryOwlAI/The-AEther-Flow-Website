# Public Comprehension And Diagram System PRD

Date: 2026-06-27

## Problem Statement

The AEther Flow Website has the correct strategic purpose: it is the
reader-facing website for the upstream AEther Flow research project, while the
source repository remains authoritative for scientific, mathematical,
governance, and research-workflow claims. The current website also has a
strong visual direction and an internal-first route map.

However, the current public content does not yet explain the project well
enough for general readers. Many pages compress rich upstream explanations into
short leads, generic cards, and authority notices. The result can look
organized while still failing at comprehension: readers see route labels,
status labels, and visual atmosphere, but do not get enough context about what
the topic is, why it matters, how the mechanism works, what equations do, or
what the project is not claiming.

The user described this failure as "AI slop": surface-level generated prose
that sounds plausible but does not teach the subject with enough context,
specificity, or human usability. That critique is accepted as the problem this
PRD exists to solve.

The issue is distinct from the site-wide visual redesign described in
`PRDs/site-wide-formidable-command-interface-redesign-prd.md`. That PRD owns
layout language, hierarchy, and the command-interface presentation model. This
PRD owns public comprehension: source-derived explanation depth, topic context,
feature and functionality coverage, diagram production, equation walkthroughs,
content dossiers, and page-by-page remediation.

## Solution

Create a source-derived public comprehension system for the website.

The system will replace shallow topic summaries with page-specific explanations
grounded in upstream source evidence. Each remediated page must teach its
topic before it describes the page. It must explain what the topic is, why it
exists in AEther Flow, how it functions, which source objects support it, what
terms mean, what diagrams show, what equations do, and what the topic does not
prove or authorize.

The release will introduce four durable practices:

1. **Tracked content dossiers**: maintainer-facing evidence packets under
   `docs/content-dossiers/` that collect current website copy, mapped upstream
   source material, relevant README/source context, claim boundaries,
   glossary terms, diagrams, equations, and safe/unsafe summaries before public
   copy is rewritten.
2. **Flexible comprehension blocks**: reusable page content structures for
   context, summary, mechanism walkthroughs, definitions, diagrams, equations,
   source basis, boundaries, safe/unsafe summaries, and related reading. These
   are required as coverage blocks, not as a rigid visual template.
3. **Mermaid-generated static diagrams**: reviewed Mermaid source diagrams
   rendered into committed PNG assets for public pages. The public site should
   not load Mermaid at runtime. Diagrams are explanatory artifacts, not
   decoration.
4. **Public comprehension audit**: a quality gate beyond structural
   validation. It checks whether a page actually explains the project,
   preserves source boundaries, defines its terms, uses diagrams and equations
   responsibly, and avoids generic generated prose.

Phase 1 will remediate two pilot pages:

1. `/project/overview/`, to prove the general-public front-door explanation
   model.
2. `/project/ai-research-agent-system/parent-child-synthesis/`, to prove the
   deep-topic model on a difficult AEther Flow workflow concept.

Later phases will remediate route families in risk order: physics pages first,
AI research-agent pages second, operations pages third, and resources/source
authority/current-state pages fourth, followed by site-wide QA and a follow-on
implementation plan handoff.

## User Stories

1. As a first-time general reader, I want the overview page to explain what
   AEther Flow is before showing me route choices, so that I can understand
   the project without prior repository knowledge.
2. As a first-time reader, I want a plain-language summary at the beginning of
   major pages, so that I can decide whether I am in the right place.
3. As a general reader, I want unfamiliar project terms defined near their
   first meaningful use, so that I am not forced to infer specialized
   vocabulary from context.
4. As a general reader, I want pages to explain mechanisms step by step, so
   that I can understand what a feature or workflow does.
5. As a reader with no physics background, I want equations to be accompanied
   by plain-language explanations, so that mathematical notation does not turn
   into opaque decoration.
6. As a reader with physics background, I want equations to preserve their
   assumptions, regimes, and source status, so that public explanation does
   not weaken scientific precision.
7. As a reader evaluating credibility, I want every major explanation to state
   what it does not prove, so that I do not mistake public prose for source
   authority.
8. As a reader evaluating the physics program, I want ontology, exact-GR
   benchmark adoption, derivation burden, and claim promotion to be separated,
   so that I can understand the current scientific status.
9. As a reader evaluating the AI research-agent system, I want role routing,
   AgentJobs, validators, memory, and handoffs explained as operational
   mechanics, so that I can understand the research system without treating it
   as physics evidence.
10. As a reader trying to understand parent-child synthesis, I want the
    one-outer-AgentJob invariant explained first, so that I do not think it
    creates extra jobs or extra authority.
11. As a reader trying to understand parent-child synthesis, I want a diagram
    of parent review, child perspectives, conflict handling, and fused output,
    so that the workflow is visually intelligible.
12. As a reader trying to understand parent-child synthesis, I want child
    outputs described as supporting `draft/control` artifacts, so that I do
    not mistake them for independent verdicts.
13. As a reader trying to understand parent-child synthesis, I want unresolved
    blocking conflict behavior explained, so that I understand why PASS cannot
    be valid while a declared blocking conflict remains unresolved.
14. As a reader trying to understand the project overview, I want a two-track
    diagram showing the physics track and AI research-agent track, so that the
    dual project structure is obvious.
15. As a reader trying to choose a route, I want route links to describe the
    reader job of each route, so that I understand why to click them.
16. As a reader trying to inspect sources, I want GitHub links to remain
    visible as provenance, so that source inspection is available without
    becoming the primary explanation path.
17. As a reader using the document library, I want ontology PDF and TeX assets
    explained in relation to source authority, so that I understand TeX versus
    PDF status.
18. As a reader using the diagrams page, I want each diagram to explain what
    it shows and what it does not prove, so that diagrams do not become visual
    overclaims.
19. As a reader of the current-state page, I want the status snapshot explained
    in ordinary language, so that task state, handoff state, claim boundaries,
    and next actions are understandable.
20. As a reader of the source-authority page, I want generated derivatives,
    source records, registries, validators, and website pages distinguished,
    so that I can assign trust correctly.
21. As a reader of physics pages, I want the site to explain why ordinary GR is
    kept at observable scale, so that benchmark compatibility is not confused
    with completed substrate derivation.
22. As a reader of physics pages, I want no-go, obstruction, and freeze labels
    explained as scoped route-control records, so that I do not infer a global
    rejection of the whole theory.
23. As a reader of the GR derivation roadmap, I want milestone burdens
    explained one by one, so that terms such as `M_src`, `g_eff`, matter
    coupling, Einstein equations, and benchmark promotion are not flattened
    into a generic progress list.
24. As a reader of the Exact-GR benchmark page, I want adoption,
    compatibility, derivation, and promotion separated, so that I understand
    which status is already present and which remains open.
25. As a reader of the ontology page, I want ontology separated from
    mathematical model and empirical prediction, so that speculative framing
    is not presented as proven physics.
26. As a reader of claim-gate content, I want accepted claims, stopped lines,
    no-go records, and freeze criteria separated, so that I can understand how
    research claims are controlled.
27. As a reader of roles-and-skills content, I want role names, registered
    roles, execution-role records, task overlays, and AgentJob allowlists
    distinguished, so that role labels do not look like live permission.
28. As a reader of memory and registries content, I want retrieval surfaces,
    generated wiki notes, CSV registries, and canonical source files
    distinguished, so that memory convenience is not mistaken for authority.
29. As a reader of validator workflow content, I want PASS results explained
    as bounded operational evidence, so that validation success is not
    mistaken for theorem proof.
30. As a reader of publication-process content, I want the brief, source spec,
    review evidence, public page, and provenance chain explained, so that
    public documentation quality is understandable.
31. As a reader of project-system improvement content, I want non-physics
    improvement work separated from physics continuation, so that tooling
    repairs do not look like science progress.
32. As a maintainer, I want a content dossier before each rewrite, so that
    public page changes are grounded in source material and claim boundaries.
33. As a maintainer, I want content dossiers to be tracked, so that future
    contributors can inspect why a public page says what it says.
34. As a maintainer, I want content dossiers outside public navigation, so that
    the website remains a clean reader surface.
35. As a maintainer, I want a reusable content model, so that Phase 1 does not
    create isolated one-off page structures that cannot scale.
36. As a maintainer, I want the current compressed `lead` plus `cards` model
    expanded, so that pages can carry actual explanation depth.
37. As a maintainer, I want page-specific structure to remain allowed, so that
    the cure for shallow prose is not a rigid generic template.
38. As a maintainer, I want every diagram to have Mermaid source and generated
    PNG output, so that diagram production is reproducible and static.
39. As a maintainer, I want diagram assets recorded in manifests, so that
    source provenance and asset hashes remain auditable.
40. As a maintainer, I want no public Mermaid runtime dependency, so that the
    static Cloudflare Pages model remains simple and stable.
41. As a maintainer, I want PNG to be the default generated diagram format, so
    that visible text in diagrams does not conflict with the existing SVG
    artwork policy.
42. As a maintainer, I want JPEG allowed only for photographic or texture-like
    assets, so that diagrams remain crisp and text-readable.
43. As a maintainer, I want diagrams to be required conditionally after Phase
    1, so that diagrams appear where they clarify structure rather than
    everywhere by formula.
44. As a maintainer, I want new public pages allowed only after a documented
    content-gap audit, so that the website can grow without becoming
    fragmented.
45. As a maintainer, I want existing pages improved first, so that thin new
    pages do not mask weak core explanations.
46. As a maintainer, I want page-route provenance preserved after rewrites, so
    that content quality work does not break source authority tracking.
47. As a maintainer, I want public page hashes regenerated after page changes,
    so that provenance validation remains meaningful.
48. As a maintainer, I want asset hashes regenerated after diagram assets
    change, so that public diagrams are tracked like other source-backed
    assets.
49. As a maintainer, I want comprehension audit criteria written down, so that
    "better writing" is not left as an untestable preference.
50. As a maintainer, I want scripts to catch obvious comprehension failures
    where practical, so that reviewers can focus on judgment rather than
    mechanical omissions.
51. As a maintainer, I want human review to remain part of the comprehension
    gate, so that validator PASS does not stand in for public understanding.
52. As an implementation agent, I want Phase 1 to include both overview and a
    deep topic, so that the model proves front-door and detail-page behavior.
53. As an implementation agent, I want physics pages remediated before most
    operational pages, so that highest overclaim risk is handled first.
54. As an implementation agent, I want AI-system pages remediated after the
    parent-child pilot, so that the pilot can inform route-family migration.
55. As an implementation agent, I want operations remediated after physics and
    AI-system pages, so that operational clarity improves without delaying
    physics risk reduction.
56. As an implementation agent, I want resources, documents, diagrams,
    source-authority, and current-state pages remediated together late in the
    sequence, so that supporting surfaces match the improved core pages.
57. As an implementation agent, I want a follow-on implementation plan before
    coding, so that exact files, commands, assets, screenshots, and validation
    packets are bounded.
58. As a reviewer, I want before/after evidence for remediated pages, so that I
    can compare actual comprehension improvement rather than only diff volume.
59. As a reviewer, I want mobile and desktop screenshots for remediated pages,
    so that longer explanations and diagrams do not create layout regressions.
60. As a motion-sensitive reader, I want any retained animation to respect
    reduced-motion behavior, so that diagram and visual improvements do not
    reduce accessibility.
61. As a screen-reader user, I want diagrams to have alt text, captions, and
    nearby prose, so that visual explanations are not the only access path.
62. As a keyboard-only user, I want expanded content and related links to
    remain navigable, so that deeper explanations do not create interaction
    traps.
63. As an external AI summarizer, I want safe/unsafe summaries and claim
    boundaries on high-risk pages, so that downstream summaries are less
    likely to overclaim.
64. As the project owner, I want the website to explain and promote the
    project inside the website itself, so that GitHub remains provenance
    rather than the main public reading experience.
65. As the project owner, I want the site to stop sounding generic, so that the
    public surface reflects the actual AEther Flow research system rather than
    a plausible but shallow AI-generated site.

## Assumptions

- The website repository remains a reader-facing presentation layer for the
  upstream AEther Flow source repository.
- The upstream source repository remains authoritative for scientific,
  mathematical, governance, and research-workflow claims.
- Existing internal-first route and provenance decisions from
  `PRDs/internal-explainer-and-source-assets-prd.md` remain binding.
- Existing visual language work from
  `PRDs/site-wide-formidable-command-interface-redesign-prd.md` remains
  binding for layout, hierarchy, command bands, evidence rails, and status
  dossiers.
- This PRD does not reopen the color schema, animation identity, deployment
  model, or primary route families.
- The current public page set is the first remediation target.
- New pages are allowed only when a content-gap audit proves that the existing
  route set cannot explain the concept cleanly.
- Phase 1 includes `/project/overview/` and
  `/project/ai-research-agent-system/parent-child-synthesis/`.
- Diagrams for Phase 1 must be Mermaid-generated static PNGs committed to the
  repository.
- Runtime Mermaid in public pages is out of scope.
- Content dossiers are maintainer artifacts and are not public navigation
  pages.
- The PRD should be comprehensive, but implementation still requires a
  follow-on implementation plan before coding.

## Implementation Decisions

### Relationship To The Command-Interface Redesign

- This PRD is a sibling to the command-interface PRD, not a replacement.
- The command-interface PRD owns layout primitives and anti-card visual
  direction.
- This PRD owns explanation depth, source-derived content, diagrams, equation
  walkthroughs, dossiers, and public comprehension quality gates.
- When both PRDs apply to the same page, use command-interface primitives to
  present the comprehension blocks, not to replace them.
- Command bands should carry major explanations, not decorative slogans.
- Evidence rails should show source chains, process steps, status ladders,
  workflow transitions, or route progression.
- Status dossiers should summarize claim state, source state, asset state, or
  operational status after the page has explained what those states mean.

### Required Content Dossiers

Before rewriting a public page, implementation must create a tracked content
dossier under `docs/content-dossiers/`.

Each dossier must include:

- Page route and reader job.
- Current website copy summary.
- Mapped upstream GitHub-facing explainer sources.
- Relevant upstream README sections.
- Relevant registered TeX, PDF, registry, schema, research-control, or design
  sources when the page explains equations, physics, operations, governance,
  validation, memory, or claim status.
- Source-derived topic outline.
- Plain-language glossary.
- Claim boundaries and forbidden implications.
- Required comprehension blocks for the page.
- Required diagrams, including Mermaid source, generated PNG path, alt text,
  caption, and manifest impact.
- Required equation walkthroughs, if applicable.
- Safe and unsafe summary pairs for high-risk topics.
- New-page audit result, if the dossier recommends splitting or adding a
  route.
- Acceptance checklist for public comprehension review.

The dossier is not itself the public page. It is the evidence trail and
editorial contract for the public page.

### Flexible Comprehension Blocks

The implementation must support a reusable content model that can express the
following blocks. A page should use the relevant subset, chosen by source
evidence and reader need:

- **Context block**: what the topic is, why it exists, and how it fits into
  AEther Flow.
- **Plain-language summary block**: the general-public takeaway.
- **System logic block**: how a mechanism, workflow, status model, or feature
  works step by step.
- **Terms and objects block**: definitions of specialized terms, source
  objects, records, variables, roles, or statuses.
- **Source basis block**: which upstream source surfaces support the
  explanation.
- **Boundary block**: what the page does not prove, authorize, promote, or
  change.
- **Diagram explanation block**: what each diagram shows and what it does not
  show.
- **Equation walkthrough block**: what an equation answers, what its symbols
  mean, when it applies, and what it does not prove.
- **Safe/unsafe summary block**: concise correct and incorrect summaries for
  overclaim-prone pages.
- **Related path block**: what to read next inside the website.

These blocks are coverage requirements, not a rigid public page template.
Different route families may sequence and present them differently.

### Reusable Content Model

The existing compressed explainer model should be extended or replaced with a
source-backed model that can represent richer public explanations.

The reusable model must support:

- Long-form context sections.
- Short public summaries.
- Mechanism walkthroughs with ordered steps.
- Glossary or term-definition groups.
- Diagram figures with generated asset metadata.
- Equation walkthroughs with labels and source references.
- Safe/unsafe summary pairs.
- Source-boundary notices.
- Related internal routes.
- Provenance/source links separated from primary navigation.

Phase 1 may keep the abstraction small, but it must not hard-code both pilot
pages as isolated one-off layouts that cannot inform later remediation.

### Diagram Production Rules

Public diagrams created under this PRD must follow these rules:

- Use Mermaid as the editable diagram source format.
- Render Mermaid to committed PNG assets for public pages.
- Do not load Mermaid in the public browser runtime.
- Record diagram assets in source and asset manifests when they become public.
- Keep Mermaid source tracked as a maintainer artifact.
- Use PNG by default.
- Use JPEG only for photographic, texture-like, or non-diagram imagery.
- Provide alt text, caption, and nearby explanatory prose.
- State what the diagram does not prove or authorize when the topic is
  claim-sensitive.
- Do not count decorative artwork as a required explanatory diagram.
- Preserve existing animated SVG identity, but do not use inline SVG with
  visible embedded text to satisfy this PRD's Mermaid-diagram requirement.

The implementation plan should choose exact Mermaid source locations. The
recommended default is a maintainer documentation path for `.mmd` files and
the existing public diagram assets path for generated PNGs.

### Equation Walkthrough Rules

Whenever a page displays or substantively references a mathematical equation,
it must include a plain-language equation walkthrough.

Each walkthrough must explain:

- What question the equation answers.
- What each symbol or major term means in ordinary language.
- Which assumptions, approximations, or valid regime apply.
- What source material the equation comes from.
- Whether the equation is adopted benchmark structure, a derived result,
  schematic notation, a definition, or an open research target.
- What the equation does not prove.
- A short "read it as" sentence for non-specialists.

Physics pages must repeat the adoption-versus-derivation boundary where needed.
Displaying Einstein-equation-level structure must not imply completed substrate
derivation.

### New Public Page Rule

Implementation may add new public pages only after a content-gap audit.

A new page is allowed when:

- The concept has a distinct reader job.
- The concept cannot be explained clearly as a section of an existing route.
- The concept has sufficient source evidence.
- The concept needs its own source dossier, diagram set, or provenance mapping.
- The route can be linked from the relevant route family without cluttering
  primary navigation.

A new page is not allowed merely because existing pages are too shallow. First
improve the existing mapped pages. Use progressive sections inside an existing
page when the concept is subordinate.

### Public Comprehension Quality Gate

The implementation must add a public-comprehension audit for remediated pages.
It may combine scripted checks and human review, but it must not rely on
`npm run validate` alone.

The audit must reject a remediated page when it:

- Opens with metadata instead of explaining the topic.
- Describes the page rather than the project functionality.
- Uses generic card grids without enough context.
- Lacks a plain-language summary.
- Lacks mechanism walkthroughs for operational or mathematical topics.
- Uses source-derived terms without definitions.
- Displays or references equations without walkthroughs.
- Uses diagrams as decoration rather than explanation.
- Fails to say what the topic does not prove or authorize.
- Routes readers to GitHub as the primary explanation surface.
- Silently strengthens scientific, mathematical, governance, or workflow
  claims.
- Omits source basis for important assertions.
- Provides no safe/unsafe summary for high-risk claim-boundary topics.

Human review must remain part of the audit because structural validation cannot
prove public comprehension quality.

### Feature And Functionality Coverage

The remediation must eventually cover the main AEther Flow functionality
domains.

#### Project Overview Domain

The overview must explain:

- AEther Flow as a dual physics-and-AI research project.
- The physics track as an exact-GR benchmark-disciplined research program with
  an open substrate derivation burden.
- The AI research-agent track as a governed, human-scaffolded research system.
- How the two tracks co-develop.
- How readers should move through the website.
- Why source authority remains upstream even though the website is the primary
  public reading surface.
- What the website does not claim.

Required Phase 1 diagram:

- A two-track project map showing physics track, AI research-agent track,
  source authority, and reader route families.

#### Parent-Child Parallel Synthesis Domain

The parent-child synthesis pilot must explain:

- The external invariant: one Director decision, one outer AgentJob, one
  execution-role record, one completion record, and one fused output.
- Why internal child perspectives exist.
- Why child outputs are supporting `draft/control` artifacts.
- What authority is inherited from the outer AgentJob.
- How parent review and fusion work.
- How blocking conflicts are handled.
- Why unresolved declared blocking conflicts prevent PASS completion.
- Why the mode is scoped to future physics research AgentJobs and is not a
  universal rule for all project-system or documentation tasks.
- Safe and unsafe summaries.

Required Phase 1 diagram:

- A single-outer-AgentJob frame containing parent review, child perspectives,
  conflict handling, and fused output.

#### Physics Domain

Physics page remediation must explain:

- AEther / AEther-flow ontology as a research ontology and explanatory frame.
- The exact-GR benchmark boundary.
- The difference between adoption, compatibility, derivation, and promotion.
- The current open burden of deriving effective Lorentzian geometry and GR
  behavior from source-defined substrate structure.
- Current-state status without turning it into claim promotion.
- Claim gates, no-go records, obstruction records, freeze criteria, and
  negative-result preservation.
- GR derivation roadmap milestone vocabulary.
- Source-extension and finite toy categories without treating them as GR
  shortcuts.
- Relevant equations and what they do.

Physics pages should use diagrams such as:

- Benchmark boundary ladder.
- Derivation burden timeline.
- Claim gate/status matrix.
- Ontology-to-effective-model relationship map.
- Equation relationship diagrams when useful.

#### AI Research-Agent Domain

AI research-agent page remediation must explain:

- Human-scaffolded research-agent workflow.
- Director decisions.
- AgentJobs.
- Role and skill boundaries.
- Memory, registries, wiki, and retrieval surfaces.
- Parent-child synthesis.
- Claim gates, review, and refutation discipline.
- Separation between AI-methodology claims and physics claims.
- Staged autonomy as an ambition, not a current autonomous-science claim.

AI pages should use diagrams such as:

- Research-agent workflow lifecycle.
- Director-to-AgentJob narrowing diagram.
- Role/allowlist authority stack.
- Memory and registry source hierarchy.
- Parent-child synthesis frame.

#### Operations Domain

Operations page remediation must explain:

- Director and AgentJob lifecycle.
- Role routing and execution contracts.
- Validator and operator workflow.
- Documentation Curator publication process.
- Project-system improvement loop.
- Technical requirements for reproducible operation.
- Why operational PASS evidence is bounded.
- Why operational success is not physics proof.

Operations pages should use diagrams such as:

- Record-chain lifecycle.
- Validator evidence flow.
- Publication process flow.
- Improvement-loop routing map.
- Tool-tier dependency map.

#### Resources, Documents, Diagrams, Source Authority, And Current-State Domain

Supporting pages must explain:

- Resource index purpose.
- Ontology document library status.
- Registered TeX source authority versus PDF derivative status.
- Diagram gallery status and diagram limits.
- Source authority hierarchy.
- Page provenance and route mapping.
- Current-state snapshot meaning and drift limits.
- GitHub/source links as provenance rather than primary reading path.

Supporting pages should use diagrams such as:

- Source authority stack.
- Document asset source chain.
- Diagram publication chain.
- Current-state status dossier map.

## Phased Delivery Requirements

### Phase 1: Two-Page Pilot

Scope:

- Remediate `/project/overview/`.
- Remediate `/project/ai-research-agent-system/parent-child-synthesis/`.
- Create tracked content dossiers for both pages.
- Create Mermaid source and generated PNG diagrams for both pages.
- Introduce the initial reusable comprehension content model.
- Cross-check visual presentation against the command-interface PRD.

Acceptance criteria:

- Overview opens with clear general-public context.
- Overview explains both project tracks and the website/source authority
  boundary.
- Overview includes a two-track project map diagram with accessible text.
- Parent-child page opens with the one-job invariant.
- Parent-child page explains inherited authority, child `draft/control`
  status, conflict handling, fused output, and scope limits.
- Parent-child page includes the one-outer-AgentJob diagram with accessible
  text.
- Both pages include source basis, boundary, glossary, safe/unsafe summary
  where needed, and related internal route guidance.
- Both pages pass public-comprehension audit.
- Existing page provenance is regenerated after page changes.
- Public diagram assets are manifest-backed after asset changes.

### Phase 2: Physics Route Remediation

Scope:

- Remediate physics landing page.
- Remediate ontology page.
- Remediate Exact-GR benchmark page.
- Remediate GR derivation roadmap page.
- Remediate claim-gates page.
- Remediate current physics state if not deferred to Phase 5 by the
  implementation plan.

Acceptance criteria:

- Every physics page separates ontology, benchmark adoption, derivation burden,
  and claim promotion where relevant.
- Equation references have walkthroughs.
- High-risk pages include safe/unsafe summaries.
- Diagrams explain benchmark boundaries, derivation burdens, claim gates, or
  current-state relationships.
- No page silently strengthens physics status.

### Phase 3: AI Research-Agent Route Remediation

Scope:

- Remediate AI research-agent landing page.
- Remediate workflow page.
- Remediate roles-and-skills page.
- Remediate memory-and-registries page.
- Carry lessons from the parent-child pilot into the rest of the AI-system
  route family.

Acceptance criteria:

- Pages explain operational mechanics before metadata.
- Role labels, execution records, AgentJobs, validators, and memory surfaces
  are distinguished.
- AI-methodology claims remain separate from physics claims.
- Diagrams clarify workflow, authority narrowing, memory surfaces, or role
  boundaries.

### Phase 4: Operations Route Remediation

Scope:

- Remediate operations landing page.
- Remediate Director and AgentJob lifecycle page.
- Remediate role-routing page.
- Remediate validator/operator workflow page.
- Remediate publication-process page.
- Remediate project-system improvement page.
- Remediate technical-requirements page.

Acceptance criteria:

- Pages explain operational function, not only control labels.
- PASS evidence is consistently described as bounded.
- Publication quality is distinguished from source authority.
- Project-system improvement is distinguished from physics progress.
- Diagrams clarify record chains, validators, publication, improvement loops,
  or tool tiers.

### Phase 5: Supporting Surfaces

Scope:

- Remediate resources index.
- Remediate ontology documents page.
- Remediate diagram gallery.
- Remediate source-authority page.
- Remediate current-state page if not completed in Phase 2.
- Audit secondary research/support routes for whether they need remediation,
  de-emphasis, redirects, or clearer status.

Acceptance criteria:

- Supporting surfaces reinforce internal-first reading and source-provenance
  boundaries.
- Document assets clearly distinguish TeX source authority from PDF
  derivatives.
- Diagram gallery explains diagram purpose and limits.
- Current-state explanations clarify snapshot status and drift risk.

### Phase 6: Site-Wide QA And Implementation-Plan Handoff

Scope:

- Run public-comprehension audit across remediated pages.
- Run repository validation.
- Run relevant Python tests.
- Run browser QA for desktop and mobile layouts.
- Verify generated diagram assets, alt text, captions, and manifests.
- Verify page provenance.
- Verify no Mermaid runtime dependency was added.
- Produce a follow-on implementation summary and remaining backlog.

Acceptance criteria:

- The remediated corpus passes standard validators or names concrete existing
  unrelated blockers.
- The remediated corpus passes public-comprehension audit.
- Screenshots show that longer text, diagrams, and equations fit on desktop
  and mobile.
- GitHub links remain provenance links, not primary reading links.
- Follow-on implementation plan or closeout notes identify any routes not yet
  remediated and why.

## Testing Decisions

- Tests should focus on observable public behavior, source-boundary
  preservation, route integrity, accessibility, and manifest/provenance
  correctness.
- Standard validation remains required: manifest validation, content-source
  validation, internal-first link validation, SVG policy validation, page
  provenance validation, curator validation, Cloudflare validation, and Astro
  build where applicable.
- Page-source changes require page provenance hash regeneration.
- Public diagram asset changes require asset manifest and source manifest
  updates.
- Mermaid-generated PNGs must be checked into the repository and served as
  static assets.
- Public pages must not include Mermaid runtime scripts or client-side Mermaid
  rendering requirements.
- Diagram accessibility must be tested by checking alt text, captions, and
  nearby explanatory prose.
- Equation walkthroughs must be checked on pages that display or substantively
  reference equations.
- The public-comprehension audit must include human review, because structural
  checks cannot prove that the page is understandable.
- Browser QA must include desktop and mobile screenshots for each phase's
  representative routes.
- QA must check that diagrams do not overflow, blur, become unreadable, or
  replace necessary text explanation.
- QA must check that longer explanations do not create card nesting, text
  overlap, button overflow, or inaccessible reading order.
- Reduced-motion behavior must be verified when existing animated SVGs or
  motion-heavy visual surfaces are affected.
- Tests should not assert internal component implementation details unless a
  new public content model exposes a stable data contract.

## Out of Scope

- Replacing the command-interface redesign PRD.
- Reopening the visual color schema.
- Removing existing animated SVG identity.
- Adding Mermaid as a public runtime dependency.
- Building a custom PDF viewer.
- Rendering full TeX documents into HTML.
- Publishing source-repository private or draft/control material as
  authoritative public claims.
- Changing scientific, mathematical, governance, validator, role, routing,
  memory, or research-control authority in the upstream source project.
- Claiming that GR has been derived from the AEther Flow ontology.
- Claiming that AI agents autonomously own research decisions, authorship, or
  public release accountability.
- Adding new public pages without a content-gap audit.
- Treating content dossiers as public navigation pages.
- Treating validator PASS as sufficient evidence of public comprehension.
- Deploying the site. Deployment remains a separate explicit action.

## Open Questions

- Which exact directory should store Mermaid `.mmd` sources: a dedicated
  diagram-source directory, the matching content dossier directory, or another
  maintainer path? The recommended default is a dedicated maintainer
  documentation path, with the final choice left to the follow-on
  implementation plan.
- Which human reviewer or review role will sign off the public-comprehension
  audit? The PRD requires human review but does not assign a person.
- Should the public-comprehension audit become a hard scripted validator in
  `npm run validate`, or a separate quality-gate command used during phased
  remediation? The recommended default is a separate focused quality command
  until the rules stabilize.
- Should secondary research routes be remediated, hidden from public journeys,
  redirected, or retained as developer/test support routes? This should be
  decided during Phase 5.

## Further Notes

The central implementation principle is source-derived explanation, not
copy-length inflation. Longer pages are acceptable when the subject requires
detail, but length alone does not solve the problem. A good remediated page
should make a reader more capable: it should define the topic, explain the
mechanism, show the diagram, walk through the equation when present, state the
source basis, and preserve the boundary.

This PRD also preserves the earlier internal-first website strategy. GitHub
and upstream source links remain essential, but they are provenance and
inspection surfaces. The primary public reading journey should live inside the
website.

The follow-on implementation plan should translate this PRD into bounded
packets with exact page lists, content-dossier files, Mermaid sources,
generated PNG assets, manifest updates, page-provenance updates, screenshots,
commands, and validation steps.

## References

AEther-Flow Project. (2026). `README.md` [Source repository front door].

AEther-Flow Project. (2026). `github-facing/parent-child-synthesis-explainer.md`
[Generated noncanonical reader explainer].

AEther-Flow Project. (2026). `markdown/html-explainer-specs/project-overview-explainer.md`
[Project overview source spec].

AEther-Flow Project. (2026). `markdown/html-explainer-specs/parent-child-synthesis-explainer.md`
[Parent-child synthesis source spec].

The AEther Flow Website. (2026). `AGENTS.md` [Website repository operating
rules].

The AEther Flow Website. (2026). `PRDs/internal-explainer-and-source-assets-prd.md`
[Internal explainer and source-assets release contract].

The AEther Flow Website. (2026). `PRDs/site-wide-formidable-command-interface-redesign-prd.md`
[Site-wide command-interface redesign PRD].

The AEther Flow Website. (2026). `docs/project-features-and-functionality.md`
[Website feature and functionality operating map].

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`
[Route-to-source mapping manifest].

Wikipedia contributors. (2026). *AI slop*. Wikipedia.
https://en.wikipedia.org/wiki/AI_slop
