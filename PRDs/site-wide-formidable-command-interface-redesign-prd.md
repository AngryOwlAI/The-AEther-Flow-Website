# Site-Wide Formidable Command-Interface Redesign PRD

Date: 2026-06-27

## Problem Statement

The current AEther Flow Website has a strong dark cyan/orange visual schema and
animated SVG identity, but its page structure still depends too heavily on
repeated bordered card grids. The result can read as a softened Brutalist card
layout: common in AI-generated websites, visually predictable, and weaker than
the project's intended character.

The user wants the website to feel formidable, precise, and impressive while
remaining scientifically restrained. The site should look like a disciplined
research-command interface rather than a sequence of generic feature cards.

This is a presentation and UX problem, not a color problem. The Angry Owl
cyan/orange/dark graphite color schema is locked. Existing SVG animations should
be preserved and elevated. Scientific, mathematical, governance, and
source-authority claims must not be rewritten or strengthened by the redesign.

## Solution

Create a phased, site-wide layout-language redesign that replaces the default
card-grid rhythm with a cinematic research-command interface.

The new design language will use three reusable primitives:

1. **Command bands**: full-width narrative sections with strong hierarchy for
   major concepts and primary reader movement.
2. **Evidence rails**: horizontal or vertical source, provenance, journey, or
   status tracks that replace isolated equal cards where sequence and authority
   matter.
3. **Status dossiers**: compact dense panels for claim state, current state,
   document metadata, downloads, and provenance, used sparingly rather than as
   the dominant page rhythm.

Animated SVGs should become structural scene layers: background fields, rails,
orbital traces, gate lines, source-flow diagrams, and status currents. They
should not usually sit inside bordered preview boxes when their purpose is to
shape the page atmosphere and information hierarchy. The exception is
inspection-oriented diagram surfaces, especially `/resources/diagrams/`, where a
framed artifact remains appropriate.

Phase 1 will define the shared primitives and apply them to `/project/overview/`
as the flagship proof. Later phases will migrate shared route-family templates
before hand-tuning individual pages.

## Research And Evidence Notes

Direct public UX complaint data for this specific website is weak. No strong
public source set was found that reports user pain for the AEther Flow Website.
The primary evidence is therefore repository-local: current route code,
existing PRDs, page screenshots, Playwright artifacts, route manifests, and the
user's design judgment.

The local evidence shows the problematic pattern clearly: the overview, physics,
AI-system, operations, resources, and current-state routes rely on repeated
rectangular cards and bordered panels. This makes the site feel less singular
than the research program it represents.

General UX evidence supports the direction. Nielsen Norman Group describes
visual hierarchy as the mechanism that guides attention using contrast, scale,
grouping, and related visual signals. The redesign should therefore create
larger structural hierarchy instead of presenting most content as equal boxes.
W3C accessibility guidance for motion requires that moving or animated content
respect user needs for reduced motion, pause, stop, or hide behavior where
applicable.

## User Stories

1. As a first-time reader, I want the site to feel distinctive and formidable,
   so that the project makes a strong first impression.
2. As a first-time reader, I want a clear page hierarchy, so that I can tell
   which ideas are primary, supporting, or evidentiary.
3. As a physics-interested reader, I want claim-boundary sections to feel
   serious and controlled, so that unresolved physics status is not mistaken
   for completed proof.
4. As a systems-interested reader, I want the AI research-agent workflow to feel
   like an operational command system, so that roles, validators, memory, and
   handoffs are easier to understand.
5. As a reader evaluating trust, I want source authority and provenance to be
   visible without dominating the entire page, so that I can inspect credibility
   when needed.
6. As a reader choosing a path, I want routes presented as journeys or rails
   rather than generic cards, so that navigation feels intentional.
7. As a returning reader, I want current-state information to read as a status
   dossier, so that dense source metadata is scannable and authoritative.
8. As a document reader, I want PDF and TeX download surfaces to remain clear,
   so that visual drama does not reduce document usability.
9. As a mobile reader, I want the command-interface layout to collapse cleanly,
   so that no heading, action, rail, SVG, or dossier overlaps.
10. As a motion-sensitive reader, I want SVG and CSS animations to respect
    reduced-motion behavior, so that presentation does not block access.
11. As the project owner, I want the Angry Owl cyan/orange/dark graphite schema
    preserved, so that the redesign does not reopen palette decisions.
12. As the project owner, I want SVG animations preserved, so that the site keeps
    its living technical identity.
13. As the project owner, I want generic AI-looking card layouts explicitly
    banned, so that future implementation does not drift back under deadline
    pressure.
14. As a maintainer, I want shared primitives implemented before broad route
    migration, so that the redesign is maintainable rather than hand-built page
    by page.
15. As a maintainer, I want each phase validated with repository gates and
    browser evidence, so that visual improvement does not introduce regressions.
16. As an implementation agent, I want Phase 1 scoped to presentation only, so
    that no scientific or governance claims change during visual work.
17. As an implementation agent, I want side-by-side visual comparison artifacts,
    so that "formidable" can be judged against the old card-grid baseline.
18. As a future contributor, I want the PRD to define anti-patterns and
    acceptance criteria, so that the design direction remains reproducible.

## Assumptions

- The current Angry Owl cyan/orange/dark graphite color schema remains
  authoritative for this redesign.
- The existing `ImplementationPlans/angry_owl_cyan_orange_schema_site_redesign_plan.md`
  remains a historical and valid source for palette and token decisions.
- The redesign is site-wide but phased.
- Phase 1 should prove the new language on `/project/overview/` before migrating
  the rest of the site.
- Phase 1 is presentation-only. It may alter layout, visual hierarchy, SVG
  placement, responsive behavior, and UI labels needed by the new structure.
- Phase 1 must not rewrite or strengthen scientific, mathematical, governance,
  research-workflow, claim-status, route-map, or provenance claims.
- Page provenance hashes must be regenerated after source edits.
- Direct public UX feedback for the website is currently insufficient to rank
  external user complaints with high confidence.

## Implementation Decisions

### Design Direction

- Adopt "cinematic research-command interface" as the site-wide visual model.
- Preserve the existing dark cyan/orange/graphite schema.
- Preserve SVG animation as a first-class identity element.
- Move away from equal card grids as the default structural language.
- Use strong hierarchy, larger narrative bands, source-aware rails, and compact
  dossiers to make the site feel formidable without becoming theatrical or
  scientifically unserious.

### Required Layout Primitives

- **Command band**:
  - used for major concepts, route-family transitions, and flagship sections;
  - may contain unframed or lightly bounded SVG motion;
  - must create clear primary/secondary hierarchy;
  - should not contain nested card grids as its main structure.
- **Evidence rail**:
  - used for journeys, source flows, claim gates, route sequences, and status
    relationships;
  - can be horizontal on desktop and vertical on mobile;
  - should show sequence, dependency, authority, or reader progression;
  - should replace generic groups of equal cards where relationships matter.
- **Status dossier**:
  - used for source authority, current-state metadata, claim status, asset
    metadata, download status, and provenance;
  - should be dense but legible;
  - should be used sparingly to avoid becoming the new default card.

### Anti-Patterns To Ban

- Equal-height repeated card grids as the default page structure.
- Nested cards or panels inside panels.
- Light cards dropped onto dark pages as the main rhythm.
- Generic "feature card" sections with three or five equal boxes unless the
  content truly has equal peer status and no sequence.
- Decorative SVGs trapped in bordered preview frames when they should structure
  the page.
- Multiple route-family pages solving the same layout problem with unrelated
  one-off CSS.
- Visual drama that weakens source-authority, claim-status, or provenance
  clarity.

### SVG Placement Rules

- Animated SVGs should become structural scene layers on overview, track, and
  operations pages.
- Use SVG motion for fields, rails, orbital traces, gate lines, source-flow
  diagrams, status currents, and authority boundaries.
- Keep SVG policy intact: animated SVG figures must not contain visible embedded
  text; labels belong in HTML headings, captions, body copy, ARIA labels,
  `<title>`, or `<desc>`.
- Preserve reduced-motion support.
- Framed SVG inspection remains acceptable for `/resources/diagrams/` and any
  future page whose primary task is artifact review.

### Phase Plan

#### Phase 1: Foundation Plus Overview Proof

- Define shared layout primitives for command bands, evidence rails, and status
  dossiers.
- Apply them to `/project/overview/` as the reference implementation.
- Preserve the current color schema and existing SVG animation identity.
- Convert the hero, two-track section, reader journey, and living-project /
  source-authority section away from stacked card grids.
- Create side-by-side visual comparison evidence showing the current overview
  versus the command-interface proof.
- Regenerate page provenance after page-source changes.

#### Phase 2: Shared Template Migration

- Migrate shared structures before individual route hand-tuning.
- Target internal explainer pages, route grids, source notices, document and
  download lists, status grids, and current-state data blocks.
- Improve physics, AI system, operations, resources, and current-state pages by
  changing common primitives first.
- Preserve route content, source references, and claim-status language.

#### Phase 3: Route-Family Refinement

- Tune each major route family after shared primitives are stable:
  - physics pages use source-boundary command bands and claim-gate rails;
  - AI-system pages use workflow rails and role/status dossiers;
  - operations pages use control-map bands and execution evidence rails;
  - resources pages use document-library dossiers and asset-status rails;
  - current-state page uses compact source-state dossiers and burden/status
    rails.
- Keep GitHub/source links in provenance zones unless explicitly marked as
  source inspection.

#### Phase 4: Visual QA And Hardening

- Compare pre-redesign and post-redesign screenshots for major route families.
- Verify desktop, tablet, and mobile layouts.
- Audit animation behavior, reduced-motion behavior, and SVG policy.
- Confirm no public page regresses to generic card-grid structure as its primary
  layout model.

## Testing Decisions

- Each implementation phase must run `npm run validate` unless a skipped check
  is named with a concrete reason.
- Relevant Python tests must run for changed validators, scripts, or manifest
  behavior.
- `npm run validate:svg` must pass after SVG or SVG-related style changes.
- Page provenance must be regenerated after page-source changes.
- Asset manifests must be regenerated only if governed public assets change.
- Phase 1 must produce desktop and mobile Playwright screenshots for
  `/project/overview/`.
- Frontend-signoff phases must include side-by-side visual comparison against
  the prior page state.
- Browser QA should verify no text overlap, no CTA overlap, no SVG obstruction
  of readable content, and no broken navigation menus.
- Reduced-motion behavior must be verified for routes with animation changes.
- Tests should focus on observable behavior, accessibility, responsive layout,
  route integrity, and source-boundary preservation, not animation internals.
- A layout-language audit should confirm that repeated equal cards are
  secondary, not structural, on the redesigned overview.

## Out of Scope

- Reopening the color schema.
- Replacing the Angry Owl brand mark.
- Removing SVG animations.
- Adding new production animation dependencies.
- Rewriting scientific, mathematical, governance, research-workflow, or
  source-authority claims.
- Changing the upstream source-authority model.
- Changing route-map semantics except when required by already approved route
  work.
- Building a backend, live dashboard, simulation, proof checker, or AI runtime.
- Redesigning `/resources/diagrams/` as an unframed cinematic scene when the user
  goal is diagram inspection.
- Deploying the redesign automatically; deployment remains a separate explicit
  action.

## Open Questions

No blocking scope questions remain for the PRD.

Non-blocking implementation questions:

- Should Phase 1 introduce a small coded prototype route before replacing the
  production overview, or should it work directly on the production overview
  with screenshots as the review artifact?
- Should the layout-language audit be implemented as a manual QA checklist, a
  script that counts repeated card primitives, or both?
- Should future phases include a user-facing motion pause control in addition
  to `prefers-reduced-motion`, especially if continuous decorative animation
  remains prominent?

## Further Notes

### Public UX Research Scan Summary

Product: The AEther Flow Website.

Audience: public readers, physics-interested readers, systems/software readers,
and maintainers.

Time horizon: current redesign planning for the next phased website work.

Research scope: public UX signal for the specific website plus general design
and accessibility principles relevant to the proposed redesign.

Observed evidence:

- Direct public complaint evidence for this specific site is weak.
- Local repository evidence and screenshots show the card-grid pattern across
  several route families.
- General UX guidance supports improving visual hierarchy through scale,
  grouping, contrast, and placement rather than treating most content as equal.
- Accessibility guidance supports preserving reduced-motion behavior and
  considering pause, stop, or hide mechanisms for long-running motion.

Inference:

- The highest-leverage UX problem is not missing content but weak structural
  hierarchy. The site has strong content and a distinctive palette, but the
  repeated card grammar makes the interface feel more generic than the project.

Opportunity map:

- Fix this week: Phase 1 overview proof, primitive definitions, side-by-side
  visual comparison.
- Fix this quarter: shared template migration and route-family refinement.
- Needs deeper research: reader testing for whether the new rails and dossiers
  improve comprehension of physics status, source authority, and AI-system
  workflow.

### References

- Gordon, K. (2021, January 17). *Visual hierarchy in UX: Definition*. Nielsen
  Norman Group. https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- The AEther Flow Website. (2026). `AGENTS.md` [repository operating rules and
  response discipline].
- The AEther Flow Website. (2026).
  `ImplementationPlans/angry_owl_cyan_orange_schema_site_redesign_plan.md`
  [color-schema and token-plan evidence].
- The AEther Flow Website. (2026). `PRDs/dual-project-public-overview-prd.md`
  [accepted overview direction and source-authority constraints].
- The AEther Flow Website. (2026).
  `PRDs/internal-explainer-and-source-assets-prd.md` [internal-first route and
  provenance model].
- The AEther Flow Website. (2026). `src/pages/project/overview.astro`
  [current overview implementation].
- The AEther Flow Website. (2026). `src/styles/global.css` [current style and
  layout primitives].
- World Wide Web Consortium. (n.d.). *Understanding Success Criterion 2.2.2:
  Pause, Stop, Hide*. Web Accessibility Initiative.
  https://www.w3.org/WAI/WCAG21/Understanding/pause-stop-hide.html
- World Wide Web Consortium. (n.d.). *Understanding Success Criterion 2.3.3:
  Animation from Interactions*. Web Accessibility Initiative.
  https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html
