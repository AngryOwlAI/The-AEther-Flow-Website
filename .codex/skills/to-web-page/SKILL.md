---
name: to-web-page
description: Turn a completed docs/system-analyses/*.md system-analysis artifact, or a topic that first needs system-analysis, into one integrated AEther Flow Website public explainer route. Use when the user says to web page, make this analysis a page, publish this system analysis, create an explainer route from this analysis, or asks to convert an AEther Flow topic/system/feature/functionality/workflow/role analysis into a website page with dossier, route, manifests, optional static diagram, validation, and no-ai-slop gates.
---

# To Web Page

## Purpose

Create one integrated public explainer page from one AEther Flow system-analysis
Markdown artifact. The page must fit this website's Astro, content-dossier,
manifest, static-diagram, validation, and source-authority workflows.

This skill is an orchestrator. It does not replace `system-analysis`,
`project-explainer-frontend`, `mermaid-diagram-style`, or `no-ai-slop`.

## Required Inputs

- Preferred: a completed `docs/system-analyses/<topic-slug>.md` file.
- Topic-only fallback: a bounded topic, system, feature, functionality,
  workflow, or role. In topic-only mode, run `system-analysis` first and stop
  after the analysis if source authority is unclear.

Handle one analysis file and one public page per invocation by default. Batch
conversion requires an explicit multi-page plan or PRD.

## Required Skill Use

1. Read the active repository instructions such as `AGENTS.md`.
2. Use `no-ai-slop`; read its quality checklist for public-facing,
   claim-bearing work.
3. Use `project-explainer-frontend`; follow its Astro implementation,
   source-boundary, audit, and Playwright QA expectations.
4. Use `system-analysis` only in topic-only mode or when the supplied analysis
   is missing required evidence or authority sections.
5. Use `mermaid-diagram-style` only when promoting a Mermaid diagram into a
   public static PNG.
6. Use `prototype` only when the information architecture or visual treatment
   is genuinely unresolved.

Read `references/publication-contract.md` before editing files.

## Publication Boundary

The completed system-analysis artifact is an input, not source authority.
Before public page creation:

- verify required analysis sections exist;
- confirm the analysis has no `block` quality-gate result;
- re-check key upstream source paths and high-risk claims without redoing the
  entire analysis;
- stop if source authority is unclear, unresolved, or marked blocked.

Public pages may explain status, burden, boundaries, and source-backed
relationships. They must not silently promote scientific, mathematical,
governance, or research-workflow claims.

Preserve exact hard-boundary phrases when they carry authority:

- `proposal-only`
- `draft/control`
- `source-extension`
- `fail-closed`
- `frozen negative`
- `no MetricData(E)`
- `no g_eff`
- `no downstream GR promotion`

## Route And Page Defaults

Default to `/project/<track>/<topic-slug>/` only when the topic clearly belongs
under an existing track such as:

- `/project/physics/`
- `/project/ai-research-agent-system/`
- `/project/operations/`
- `/project/source-authority/`
- `/resources/`

If the topic does not fit an existing track, block and ask for the intended
parent route. If the target route already exists, block and ask for explicit
update authorization unless the user supplied that route.

Reuse existing page and content patterns by default:

- `InternalExplainerPage`
- `ComprehensionBlocks`
- `Figure`
- `EvidenceRail`
- `SourceNotice`
- typed content-library entries such as `src/lib/internalExplainers.ts`

Use page-local content only for a genuine one-off route. Change shared
components only when a concrete no-ai-slop, accessibility, or explanation
problem cannot be solved locally; name the shared change in the QA note and
verify affected routes.

## Sub-Agent Contract

When the user explicitly invokes this skill and multi-agent tools are
available, attempt one bounded Codex worker sub-agent by default. Give the
worker the system-analysis file path and require it to read the file directly.
Do not pass only a summary.

The worker may edit only the assigned one-page scope:

- `docs/content-dossiers/<page-slug>/dossier.md`
- optional `docs/content-dossiers/<page-slug>/diagrams/*.mmd`
- optional generated `public/assets/diagrams/comprehension/*.png`
- the Astro route and content-library entries for the one page
- relevant manifest and validator registrations
- one focused QA note under `docs/quality/` when appropriate

The main agent remains responsible for review, integration, source spot-checks,
validation, browser QA, and the final no-ai-slop gate. If sub-agents are
unavailable or not permitted, perform the same workflow in the main agent and
state that no sub-agent was spawned.

## Diagram Rule

Promote the system-analysis Mermaid diagram only when it materially improves
public understanding. A promoted diagram must become a public-facing `.mmd`
dossier diagram, render to a static PNG under
`public/assets/diagrams/comprehension/`, include alt text, caption, nearby
boundary prose, manifest coverage, and standard renderer registration.

Do not embed runtime Mermaid in public pages.

## Required Output Surfaces

For an integrated public route, create or update:

- `docs/content-dossiers/<page-slug>/dossier.md`
- optional `.mmd` diagram source and static PNG
- Astro route and typed content entry
- parent track discoverability when the page is intended as a public explainer
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/source_manifest.json` when new source/asset records
  are needed
- regenerated `public/files/manifests/asset_manifest.json` when assets change
- regenerated `public/files/manifests/page_provenance.json`
- `scripts/validate_public_comprehension.py` registration for integrated
  public routes
- `scripts/render_mermaid_diagrams.py` registration for promoted diagrams
- a short QA note when appropriate

Do not push or deploy. Release remains an explicit follow-up through
`push-and-deploy`.

## Verification

Minimum local verification for one integrated public page:

```bash
npm run validate:comprehension
npm run validate:manifests
npm run validate:content
npm run build
```

Run a focused browser or Playwright check of the new route on desktop and
mobile. For release readiness, run:

```bash
npm run validate
```

Record skipped checks with concrete reasons.

## Review Status

After automated validation passes, use `technical validation passed` as the
default review status. Use `human review pending` only when the page is
high-risk, claim-heavy, explicitly experimental, or the user asks for human
comprehension review.
