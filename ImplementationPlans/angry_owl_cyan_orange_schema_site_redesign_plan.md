# Angry Owl Cyan And Orange Schema Site Redesign Implementation Plan

Date: 2026-06-26

## 1. Objective

Integrate the cyan and orange color language from
`/Volumes/P-SSD/Documents-P/Logos/Angy Owl/main_angryowl_round.png` into the
The AEther Flow Website project schema, then restyle all public website pages
against that new schema.

The deliverable for this packet is this implementation plan only. It does not
apply the redesign.

## 2. Evidence Inspected

- Repository operating instructions: `AGENTS.md`.
- Project commands and validation gates: `package.json`.
- Current page structure: `src/pages/**`.
- Current shared layouts: `src/layouts/BaseLayout.astro`,
  `src/layouts/LandingLayout.astro`, and `src/layouts/TechnicalPageLayout.astro`.
- Current shared components: `src/components/**`.
- Current global style surface: `src/styles/global.css` and `src/styles/math.css`.
- Current route/source contract: `public/files/manifests/page_route_map.json`.
- Current source and asset manifest tooling:
  `scripts/generate_page_provenance.py` and `scripts/build_asset_manifest.py`.
- Repo-local frontend skill artifacts generated for orientation:
  `scratch/project-explainer/project_story_brief.md`,
  `scratch/project-explainer/visual_identity.md`,
  `scratch/project-explainer/site_blueprint.md`, and
  `scratch/project-explainer/design_tokens.css`.
- Reference logo image:
  `/Volumes/P-SSD/Documents-P/Logos/Angy Owl/main_angryowl_round.png`.

## 3. Current Architecture Summary

The site is an Astro static site with MDX support. Public routes live under
`src/pages`, layouts live under `src/layouts`, shared components live under
`src/components`, site metadata lives under `src/lib`, and global styling lives
mostly in `src/styles/global.css`.

The current visual system is not fully centralized. There is a compact global
token set at the top of `src/styles/global.css`, but the project overview and
several route-specific SVG/gradient treatments use additional hardcoded colors.
The redesign should therefore be treated as a token migration plus page-family
restyle, not as a single color replacement.

The site also has source-authority constraints. Style work must not rewrite or
strengthen scientific, mathematical, governance, or workflow claims. Any copy
edits should be limited to interface labels, captions, and accessibility text
needed by the visual redesign.

## 4. Extracted Color Findings

The automatic visual identity extractor detected the orange accent but gave too
much weight to the logo background and dark outline. A targeted saturated-pixel
analysis was therefore used for the requested cyan and orange families.

### 4.1 Image-Derived Cyan Family

| Role | Candidate | Evidence basis | Recommended use |
|---|---:|---|---|
| Cyan deep | `#0F364D` | Dominant dark blue-cyan feather/shadow bins | Dark panels, footer overlays, diagram backgrounds |
| Cyan ink | `#164964` | Mid/deep cyan family weighted sample | Link text on light backgrounds, nav active state |
| Cyan primary | `#2D7EA0` | Bright cyan top-bin weighted sample | Main cyan accent, badges, non-body text |
| Cyan bright | `#48A0C0` | Bright feather highlight bin | Highlights on dark backgrounds, SVG glow accents |

### 4.2 Image-Derived Orange Family

| Role | Candidate | Evidence basis | Recommended use |
|---|---:|---|---|
| Orange deep | `#702000` | Dark orange/brown branch and shadow bin | Text on light backgrounds when orange meaning is required |
| Orange ink | `#A73702` | Mid orange top-bin weighted sample | Accessible orange link/accent text on light backgrounds |
| Orange primary | `#E15C02` | Vivid orange weighted sample | Primary brand accent, buttons on dark backgrounds |
| Orange bright | `#F87800` | Dominant vivid logo orange bin | Decorative highlights, hero energy, dark-surface UI |
| Orange light | `#F4D6A1` | Light cream/orange highlight weighted sample | Warm surface tint, dark-surface readable text |

### 4.3 Supporting Neutrals

| Role | Candidate | Evidence basis | Recommended use |
|---|---:|---|---|
| Owl ink | `#270B01` | Logo outline weighted sample | High-contrast dark text and keyline on warm light UI |
| Owl black | `#180000` | Extractor dark accent | Deep background where brand drama is needed |
| Warm ivory | `#FFF8EF` | Derived from logo highlight family | Page background alternative to pure white |
| White | `#FFFFFF` | Existing site and image background | Surface and high-contrast neutral |

### 4.4 Contrast Notes

Contrast checks for candidate production pairings:

| Foreground | Background | Ratio | Use |
|---|---|---:|---|
| `#0F364D` | `#FFFFFF` | 12.69 | Body-capable cyan text |
| `#164964` | `#FFFFFF` | 9.67 | Links and active navigation |
| `#2D7EA0` | `#FFFFFF` | 4.56 | Large or carefully used accent text |
| `#48A0C0` | `#180000` | 6.80 | Highlight text on dark brand surfaces |
| `#702000` | `#FFFFFF` | 11.08 | Body-capable orange text |
| `#A73702` | `#FFFFFF` | 6.58 | Orange accent text on light surfaces |
| `#E15C02` | `#FFFFFF` | 3.66 | Not body text on white; use for graphics or dark UI |
| `#F87800` | `#180000` | 7.39 | Bright orange on dark brand surfaces |
| `#E15C02` | `#180000` | 5.52 | Primary orange on dark brand surfaces |
| `#F4D6A1` | `#180000` | 14.42 | Warm light text on dark brand surfaces |
| `#270B01` | `#FFF8EF` | 17.56 | Primary body text on warm light surfaces |
| `#A73702` | `#FFF8EF` | 6.25 | Orange link/accent text on warm light surfaces |

Conclusion: use deep cyan and deep orange for readable text on light surfaces.
Use vivid orange and bright cyan mainly on dark surfaces, in diagrams, or as
non-text accents.

## 5. Proposed Project Color Schema

### 5.1 Raw Brand Tokens

Add raw brand tokens first. Raw tokens should describe color origin, not UI use.

```css
:root {
  --owl-cyan-900: #0f364d;
  --owl-cyan-800: #164964;
  --owl-cyan-600: #2d7ea0;
  --owl-cyan-400: #48a0c0;

  --owl-orange-900: #702000;
  --owl-orange-800: #a73702;
  --owl-orange-600: #e15c02;
  --owl-orange-500: #f87800;
  --owl-orange-100: #f4d6a1;

  --owl-ink: #270b01;
  --owl-black: #180000;
  --owl-ivory: #fff8ef;
  --owl-white: #ffffff;
}
```

### 5.2 Semantic Tokens

Semantic tokens should be what components consume. This prevents every page from
knowing whether a color came from the cyan feather, orange body, or dark outline.

```css
:root {
  --color-page: var(--owl-ivory);
  --color-surface: var(--owl-white);
  --color-surface-warm: #fff1df;
  --color-surface-cool: #edf8fb;
  --color-ink: var(--owl-ink);
  --color-muted: #5f5049;
  --color-line: #ead6c5;

  --color-link: var(--owl-cyan-800);
  --color-link-hover: var(--owl-orange-800);
  --color-focus-ring: color-mix(in srgb, var(--owl-cyan-400), white 20%);

  --color-primary: var(--owl-cyan-800);
  --color-primary-hover: var(--owl-cyan-900);
  --color-accent: var(--owl-orange-800);
  --color-accent-vivid: var(--owl-orange-600);

  --color-dark-page: var(--owl-black);
  --color-dark-panel: #0f0805;
  --color-dark-text: #fff8ef;
  --color-dark-muted: #d6c3b4;
  --color-dark-line: rgba(244, 214, 161, 0.28);
  --color-dark-cyan: var(--owl-cyan-400);
  --color-dark-orange: var(--owl-orange-500);
}
```

### 5.3 Naming Rules

- Raw tokens use `--owl-*`.
- Site-wide semantic tokens use `--color-*`.
- Route-specific derived tokens use a route prefix only when the route needs a
  special atmosphere, for example `--overview-*`.
- Hardcoded hex values should be limited to the token declaration file and SVG
  assets that cannot consume CSS variables at render time.
- Any hardcoded SVG colors should still map back to an `--owl-*` or
  `--color-*` token in comments or plan notes.

## 6. Recommended Implementation Strategy

Recommendation: use a two-layer token architecture.

1. Create or expand a dedicated token section in `src/styles/global.css`.
2. Optionally split tokens into `src/styles/theme.css` if the file becomes too
   difficult to maintain. Import it before `global.css` from
   `src/layouts/BaseLayout.astro`.
3. Migrate global components and layouts to semantic tokens.
4. Migrate page-family color systems.
5. Migrate inline SVG gradients and public SVG artwork.
6. Regenerate page provenance and asset hashes after file changes.
7. Run full validation and browser QA.

This is the smallest maintainable path because the repository already uses
CSS variables and a single global stylesheet. A new design-token package,
Tailwind setup, Sass layer, or runtime theme system is unnecessary.

## 7. Files Likely Affected

### 7.1 Core Style Files

- `src/styles/global.css`: primary token definition, global UI restyle,
  route-family restyle, responsive refinements.
- `src/styles/math.css`: verify math block colors, equation surfaces, overflow
  shadows, and KaTeX contrast.

### 7.2 Layouts

- `src/layouts/BaseLayout.astro`: verify brand header, footer, skip link, focus
  states, favicon path, and global body class behavior.
- `src/layouts/LandingLayout.astro`: likely no structural change, but verify
  landing-page body-class styling after token migration.
- `src/layouts/TechnicalPageLayout.astro`: verify technical header, metadata
  list, source notice placement, and technical content surfaces.

### 7.3 Components

- `src/components/DocumentActions.astro`: restyle download/read actions with
  cyan/orange button hierarchy.
- `src/components/DownloadList.astro`: restyle list cards, link accents, and
  status labels.
- `src/components/EquationBlock.astro`: verify equation card/background colors.
- `src/components/Figure.astro`: restyle figure frame, caption, and provenance
  text.
- `src/components/InternalExplainerPage.astro`: major shared page-family
  restyle; this likely covers operations and AI explainer child routes.
- `src/components/ProjectRouteGrid.astro`: restyle route cards and states.
- `src/components/SourceNotice.astro`: restyle claim-status notice without
  weakening the authority boundary.

### 7.4 Data And Navigation

- `src/lib/siteContent.ts`: review whether route-card labels or color-category
  labels need metadata. Avoid copy changes unless required.
- `src/lib/internalExplainers.ts`: review whether visual captions reference old
  visual language. Do not change scientific or governance claims.
- `src/lib/manifests.ts`: likely no color change, but verify document card
  styling still receives the expected data.

### 7.5 Pages With Inline Visual Color

- `src/pages/project/overview.astro`: major migration. This page has its own
  dark visual system and inline SVG gradients.
- `src/pages/project/ai-research-agent-system/index.astro`: inline SVG gradient
  colors should be migrated to the new schema.
- `src/pages/resources/index.astro`: inline SVG gradient colors should be
  migrated to the new schema.

### 7.6 Public Assets

- `public/assets/brand/main_angryowl_round.png`: already available as the brand
  logo; no replacement required unless a separate optimized derivative is
  approved.
- `public/assets/diagrams/publication-layer-map.svg`: migrate colors while
  preserving the SVG policy: animated, no visible embedded text, labels in
  HTML/captions/ARIA/title/desc.
- `public/files/manifests/asset_manifest.json`: regenerate if public manifest
  assets change.
- `public/files/manifests/page_provenance.json`: regenerate after page source
  changes because page hashes will drift.

## 8. Route Coverage Matrix

Every public route should be checked after the redesign. The first pass should
avoid copy rewrites and focus on consistent theme application.

| Route | Source file | Redesign action |
|---|---|---|
| `/` | `src/pages/index.astro` | Verify redirect/landing behavior and any inherited header/footer styling |
| `/project/overview/` | `src/pages/project/overview.astro` | Full hero, dark-stage, SVG, card, CTA, and route-link migration |
| `/project/physics/` | `src/pages/project/physics/index.astro` | Shared page/card/source-notice migration |
| `/project/physics/ontology/` | `src/pages/project/physics/ontology/index.astro` | Shared explainer migration and ontology notice contrast |
| `/project/physics/exact-gr-benchmark/` | `src/pages/project/physics/exact-gr-benchmark/index.astro` | Shared explainer migration and warning/claim-boundary states |
| `/project/physics/gr-derivation-roadmap/` | `src/pages/project/physics/gr-derivation-roadmap/index.astro` | Shared explainer migration, roadmap card states |
| `/project/physics/current-state/` | `src/pages/project/physics/current-state/index.astro` | Current-state snapshot cards, statuses, and dense content contrast |
| `/project/physics/claim-gates/` | `src/pages/project/physics/claim-gates/index.astro` | Gate/status cards with accessible orange/cyan signal states |
| `/project/ai-research-agent-system/` | `src/pages/project/ai-research-agent-system/index.astro` | Landing visual gradient migration and shared card states |
| `/project/ai-research-agent-system/workflow/` | `src/pages/project/ai-research-agent-system/workflow/index.astro` | Shared internal explainer migration |
| `/project/ai-research-agent-system/roles-and-skills/` | `src/pages/project/ai-research-agent-system/roles-and-skills/index.astro` | Shared internal explainer migration |
| `/project/ai-research-agent-system/memory-registries/` | `src/pages/project/ai-research-agent-system/memory-registries/index.astro` | Shared internal explainer migration |
| `/project/ai-research-agent-system/parent-child-synthesis/` | `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro` | Shared internal explainer migration |
| `/project/operations/` | `src/pages/project/operations/index.astro` | Shared internal explainer landing migration |
| `/project/operations/director-agentjob-lifecycle/` | `src/pages/project/operations/director-agentjob-lifecycle/index.astro` | Shared internal explainer migration |
| `/project/operations/role-routing/` | `src/pages/project/operations/role-routing/index.astro` | Shared internal explainer migration |
| `/project/operations/validator-operator-workflow/` | `src/pages/project/operations/validator-operator-workflow/index.astro` | Shared internal explainer migration |
| `/project/operations/publication-process/` | `src/pages/project/operations/publication-process/index.astro` | Shared internal explainer migration |
| `/project/operations/project-system-improvement/` | `src/pages/project/operations/project-system-improvement/index.astro` | Shared internal explainer migration |
| `/project/operations/technical-requirements/` | `src/pages/project/operations/technical-requirements/index.astro` | Shared internal explainer migration |
| `/project/source-authority/` | `src/pages/project/source-authority/index.astro` | Trust-boundary page contrast and notice hierarchy |
| `/resources/` | `src/pages/resources/index.astro` | Resource landing gradient, cards, and document journey migration |
| `/resources/documents/` | `src/pages/resources/documents.astro` | Document actions and manifest-backed list contrast |
| `/resources/diagrams/` | `src/pages/resources/diagrams.astro` | Figure frame and SVG artwork migration |
| `/research/equations/` | `src/pages/research/equations.mdx` | MDX technical layout and math contrast |
| `/research/map/` | `src/pages/research/map.astro` | Research map node/card migration |
| `/research/math-sample/` | `src/pages/research/math-sample.mdx` | MDX math sample contrast and overflow behavior |

## 9. Phase Plan

### Phase 0: Redesign Scope Lock

Purpose: prevent uncontrolled page rewrites.

Tasks:

- Confirm this is a visual-schema migration, not a content rewrite.
- Freeze the initial token candidates from this plan.
- Decide whether to keep tokens in `src/styles/global.css` or split them into
  `src/styles/theme.css`.
- Decide whether the project overview remains a dark flagship page or shifts
  to the same warm-light scheme as the rest of the site.
- Identify whether any new logo derivative is needed. Default answer: no.

Acceptance criteria:

- One approved token table.
- One approved route treatment model: light system, dark system, or hybrid.
- No unresolved question about content rewriting.

### Phase 1: Token System Foundation

Purpose: make the color schema reusable before changing pages.

Tasks:

- Add raw `--owl-*` tokens.
- Add semantic `--color-*` tokens.
- Replace existing global tokens:
  `--color-teal`, `--color-teal-dark`, `--color-ruby`, and `--color-gold`.
- Keep backward-compatible aliases temporarily if this reduces migration risk.
  Example:

```css
--color-teal: var(--owl-cyan-800);
--color-teal-dark: var(--owl-cyan-900);
--color-ruby: var(--owl-orange-800);
--color-gold: var(--owl-orange-600);
```

- Add dark-surface tokens for overview and high-impact visual sections.
- Document token roles in comments near the token declarations.

Acceptance criteria:

- Existing pages still build after tokens are introduced.
- No component consumes raw image tokens when a semantic token is available.
- Contrast-sensitive foreground/background pairings are defined.

### Phase 2: Global Layout And Navigation Migration

Purpose: make the site shell coherent.

Tasks:

- Restyle `html`, `body`, and page background with warm ivory.
- Restyle links:
  - default links use deep cyan,
  - hover/focus uses accessible orange,
  - focus ring uses cyan and is visible on light and dark surfaces.
- Restyle the header:
  - brand mark remains visible,
  - nav active state uses deep cyan or orange underline,
  - dropdown panel uses warm surface and clear borders.
- Restyle the footer:
  - preserve source-authority text,
  - use dark or warm-neutral surface with sufficient contrast.
- Verify skip link contrast and focus visibility.

Acceptance criteria:

- Header, nav menu, dropdown, skip link, and footer are readable at 320 px and
  desktop widths.
- Active navigation remains visually distinct without relying only on color.
- Focus states pass visual inspection on all route families.

### Phase 3: Shared Component Migration

Purpose: restyle once where repeated UI is centralized.

Tasks:

- Migrate button styles:
  - primary action: deep cyan on light surfaces,
  - high-impact dark action: bright orange on dark surface,
  - secondary action: bordered cyan/orange treatment.
- Migrate cards:
  - route cards,
  - document cards,
  - explainer cards,
  - source notice cards,
  - metadata panels,
  - figure frames.
- Migrate status and boundary indicators:
  - cyan for routing, source structure, and trustworthy navigation,
  - orange for publication energy, warnings, and active reader action,
  - do not rely on color alone for claim status.
- Verify `SourceNotice` remains sober and explicit. It should look important
  without becoming an alarm banner.

Acceptance criteria:

- Repeated page cards no longer use old teal/ruby/gold meanings.
- Source notice, claim status, and provenance sections remain clearly legible.
- Button hierarchy is consistent across resources and project pages.

### Phase 4: Route-Family Restyle

Purpose: cover every page family with controlled design decisions.

Tasks:

- Project overview:
  - migrate `--overview-*` tokens to the owl schema,
  - preserve the dark flagship character if approved,
  - replace gold-only accents with cyan/orange interplay,
  - update inline SVG gradients,
  - ensure the logo colors are echoed without turning the page into a logo
    replica.
- Physics pages:
  - use calm warm-light surfaces,
  - use deep cyan for structure,
  - use deep orange for gates, warnings, and boundary labels,
  - avoid making unresolved scientific status look like completion.
- AI research-agent pages:
  - use cyan for workflow/system structure,
  - use orange for active routing/action emphasis,
  - preserve human-accountability and authority-boundary messaging.
- Operations pages:
  - make dense operational cards scannable,
  - use cyan/orange labels consistently by function,
  - preserve operational-boundary wording.
- Resources pages:
  - use orange for download/read actions only where accessible,
  - use cyan for internal navigation and provenance structure,
  - verify PDF/TeX action rows are clear.
- Research sample pages:
  - ensure MDX and KaTeX blocks match the new scheme,
  - do not over-invest in visual flourish if these remain samples.

Acceptance criteria:

- Each route family has a coherent visual role.
- No page still feels like the old teal/ruby/gold palette.
- No page becomes a single-hue orange or cyan theme.
- The website still reads as a research publication layer, not a generic brand
  landing page.

### Phase 5: SVG And Visual Asset Migration

Purpose: align visual artwork with the new schema while obeying the SVG policy.

Tasks:

- Update inline SVG gradients in:
  - `src/pages/project/overview.astro`,
  - `src/pages/project/ai-research-agent-system/index.astro`,
  - `src/pages/resources/index.astro`.
- Update `public/assets/diagrams/publication-layer-map.svg`.
- Preserve animation in SVG artwork.
- Keep visible text out of SVG artwork.
- Put labels in HTML, captions, `aria-label`, `<title>`, or `<desc>`.
- Re-run the SVG validator after edits.

Acceptance criteria:

- `npm run validate:svg` passes.
- SVGs use the new cyan/orange language.
- SVGs remain accessible and policy-compliant.

### Phase 6: Manifests, Hashes, And Provenance

Purpose: keep the repository's evidence model coherent after page changes.

Tasks:

- Regenerate page provenance after route source edits:

```bash
python3 scripts/generate_page_provenance.py
```

- Regenerate asset manifest if governed public assets change:

```bash
python3 scripts/build_asset_manifest.py --write
```

- If no governed public assets change, record that asset-manifest regeneration
  was not needed.
- Verify route map entries still match local source paths.
- Verify no private absolute path leaks into public manifests.

Acceptance criteria:

- `public/files/manifests/page_provenance.json` reflects new page hashes.
- `public/files/manifests/asset_manifest.json` is updated only when required.
- Manifest validators pass.

### Phase 7: Validation And Browser QA

Purpose: prove the redesign works beyond static build success.

Required commands:

```bash
npm run validate
python3 -m pytest
python .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict
```

If a local server is used:

```bash
npm run dev -- --host 127.0.0.1
python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

Browser QA targets:

- Desktop viewport: 1440 x 1000.
- Tablet-ish viewport: 900 x 1100.
- Mobile viewport: 390 x 844.
- At minimum inspect:
  - `/project/overview/`,
  - `/project/physics/current-state/`,
  - `/project/ai-research-agent-system/`,
  - `/project/operations/`,
  - `/project/source-authority/`,
  - `/resources/`,
  - `/resources/documents/`,
  - `/research/equations/`.

Acceptance criteria:

- Static build passes.
- All validators pass or skipped checks are named with concrete reasons.
- No obvious text overlap, low-contrast text, broken nav menu, or unreadable
  math block appears at tested widths.
- The brand image renders and does not distort.
- Route cards and navigation remain internal-first.

## 10. Quality Gate Checklist

Before implementation signoff:

- [ ] Raw and semantic tokens are present.
- [ ] Old teal/ruby/gold roles are removed or aliased intentionally.
- [ ] Hardcoded colors have been audited with:

```bash
rg -n "#[0-9A-Fa-f]{3,8}|rgb\\(|rgba\\(|hsl\\(|hsla\\(" src public
```

- [ ] Any remaining hardcoded color has a reason.
- [ ] Header, footer, nav menu, buttons, links, cards, notices, and figures use
  semantic tokens.
- [ ] Inline SVG gradients are migrated.
- [ ] `publication-layer-map.svg` is migrated and still passes SVG policy.
- [ ] Page provenance is regenerated.
- [ ] Asset manifest is regenerated if governed public assets changed.
- [ ] `npm run validate` passes.
- [ ] `python3 -m pytest` passes.
- [ ] Project frontend audit passes.
- [ ] Playwright or browser QA covers desktop and mobile.

## 11. Risks And Controls

| Risk | Impact | Control |
|---|---|---|
| Bright orange is used as body text on light backgrounds | Accessibility failure | Use `#A73702` or `#702000` for text, reserve `#E15C02` and `#F87800` for dark surfaces or graphics |
| Cyan becomes too dark and loses brand visibility | Visual system feels muted | Use `#2D7EA0` and `#48A0C0` for highlights, not body text |
| Redesign changes scientific meaning | Source-authority violation | Do not rewrite research claims; preserve source notices and claim status |
| Hardcoded overview palette remains | Site feels inconsistent | Audit `--overview-*` and inline SVG colors explicitly |
| SVG policy is accidentally violated | Validator failure | Keep visible text out of SVGs and preserve animation |
| Manifests drift after page edits | Provenance validator failure | Regenerate page provenance after all page/style edits |
| The site becomes a one-note orange/cyan theme | Reduced readability and professionalism | Keep warm neutral surfaces, dark outline tones, and restrained accent use |
| Browser-only visual regressions appear | Build passes but UI is poor | Require desktop and mobile screenshots before signoff |

## 12. Out Of Scope

- Scientific content rewrites.
- New physics, mathematics, AI, governance, or workflow claims.
- New runtime theme switching.
- New CSS framework, Tailwind, Sass, or design-system dependency.
- Cloudflare deployment.
- Logo redesign.
- Replacing the authoritative source repository or route provenance model.

## 13. Optional Improvements

An improvement will be to add a small style-audit script that fails on
unapproved hardcoded colors outside the token declaration and approved SVG
files. This should be a follow-up only after the first redesign lands, because
adding enforcement before migration will produce noise.

A different perspective will be to model the site as two stable modes:

- `publication-light`: warm ivory, deep cyan structure, deep orange action.
- `signal-dark`: owl-black panels, bright orange action, bright cyan signal.

This gives the project a stronger identity without forcing every page into the
same visual atmosphere.

An inventive and novel approach will be to use the owl logo as a measured
"spectral map" for route families:

- Cyan: structure, source authority, navigation, evidence paths.
- Orange: action, publication, warnings, active transitions.
- Dark outline: containment, boundary, authority limits.
- Ivory/cream: readable research surface.

This is practical because it maps brand color to information architecture
rather than decoration.

## 14. References

Angry Owl. (n.d.). *main_angryowl_round.png* [Logo image].
`/Volumes/P-SSD/Documents-P/Logos/Angy Owl/main_angryowl_round.png`

The AEther Flow Website. (2026). *AGENTS.md*. Local repository file.

The AEther Flow Website. (2026). *package.json*. Local repository file.

The AEther Flow Website. (2026). *page_route_map.json*. Local repository file.

The AEther Flow Website. (2026). *Project explainer frontend skill outputs*.
Local generated files under `scratch/project-explainer/`.
