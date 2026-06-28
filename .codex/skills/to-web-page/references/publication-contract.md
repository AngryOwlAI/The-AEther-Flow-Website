# To Web Page Publication Contract

Use this contract after reading `to-web-page/SKILL.md`.

## Intake

Required:

- one completed `docs/system-analyses/<topic-slug>.md` file, or topic-only
  mode that first runs `system-analysis`;
- one intended public route, inferred only when the parent track is clear;
- one page slug;
- the source-analysis path recorded in the dossier and QA note.

Block before public page creation when:

- the analysis file is missing;
- the analysis has a `block` quality-gate result;
- required analysis sections, evidence, references, or claim boundaries are
  absent;
- source authority is unclear;
- the target route already exists and the user did not explicitly authorize an
  update;
- the topic does not fit an existing parent route;
- the request would convert multiple analyses without a multi-page plan or PRD.

## Route Decision

Default route families:

- Physics: `/project/physics/<topic-slug>/`
- AI research-agent system: `/project/ai-research-agent-system/<topic-slug>/`
- Operations: `/project/operations/<topic-slug>/`
- Source authority: `/project/source-authority/<topic-slug>/` only when the
  topic is about provenance, source classes, authority boundaries, or release
  discipline.
- Resources: `/resources/<topic-slug>/` only when the topic is a reader
  resource collection rather than a project-system explanation.

Do not create a new top-level section by default.

## Dossier Fields

Create or update `docs/content-dossiers/<page-slug>/dossier.md` using the
existing dossier conventions. Include at minimum:

- public route and reader job;
- audience;
- review status;
- source-analysis path;
- upstream source basis from the analysis, with local paths kept maintainer-only;
- source-derived topic outline;
- glossary for required terms;
- claim boundaries and forbidden implications;
- required comprehension blocks;
- diagram contract or explicit no-diagram decision;
- equation walkthrough decision when equations are displayed or explained;
- safe and unsafe summaries;
- new-page or existing-page audit;
- compact page-publication brief with route, source analysis path, claim
  status, diagram decision, files changed, validation commands, and review
  status;
- APA 7-style references where formal references are listed.

## Public Copy Transformation

Transform the system-analysis artifact for a general public reader:

1. Plain-language summary first.
2. Mechanism or workflow explanation second.
3. Source and claim boundary third.
4. Internal website routes next.
5. Provenance/source links last.

Simplify structure and language, but preserve exact claim-status and hard
boundary terms where they carry authority. Do not expose local filesystem paths
in public page output. Keep detailed evidence paths in the maintainer dossier.

For speculative or blocked physics material, explain status, burden, and
boundary. Do not promote the material into a result, proof, or completed
physics claim.

## Page Implementation

Prefer the existing typed content-library model:

- add or update a content object in `src/lib/internalExplainers.ts` or the
  relevant sibling library;
- keep the Astro route thin;
- use `InternalExplainerPage`, `ComprehensionBlocks`, `Figure`,
  `EvidenceRail`, and `SourceNotice` when they fit;
- add discoverability inside the chosen parent track only when the page is
  intended as a public explainer route;
- avoid shared component edits unless local content cannot solve a real
  explanation, accessibility, or no-ai-slop problem.

For existing-route revisions:

- preserve existing route intent;
- compare current copy against the system-analysis artifact;
- repair no-ai-slop issues;
- update dossier, manifests, validators, and regression checks.

## Diagram Decision

Promote a diagram only when it reduces reader burden. If promoted:

- rewrite the analysis diagram as public-facing Mermaid under
  `docs/content-dossiers/<page-slug>/diagrams/*.mmd`;
- follow `mermaid-diagram-style` and its palette contract;
- render a static PNG under `public/assets/diagrams/comprehension/`;
- add alt text, caption, and nearby boundary prose;
- update `scripts/render_mermaid_diagrams.py`;
- update `source_manifest.json` and regenerate `asset_manifest.json` when the
  asset is tracked through the manifest pipeline.

Do not embed runtime Mermaid.

## Manifest And Validator Registration

For an integrated public route:

- add route-to-source mapping in `public/files/manifests/page_route_map.json`;
- add needed source/asset records in `public/files/manifests/source_manifest.json`;
- regenerate `public/files/manifests/page_provenance.json` after route/source
  changes;
- regenerate `public/files/manifests/asset_manifest.json` after asset changes;
- register the route in `scripts/validate_public_comprehension.py` with dossier
  path, optional diagram paths, and manifest id;
- register promoted diagrams in `scripts/render_mermaid_diagrams.py`.

If a source manifest entry is not needed, explain why in the QA note.

## Worker Prompt

Use a bounded worker prompt shaped like this:

```text
Use the repo-local to-web-page workflow to convert one completed system-analysis
artifact into one integrated AEther Flow Website page.

Analysis path: <docs/system-analyses/topic.md>
Target route: <route or "infer only if clear">
Write scope: <explicit files/directories>

Read the analysis file directly. Use the repo-local no-ai-slop,
project-explainer-frontend, mermaid-diagram-style if a diagram is promoted, and
system-analysis only if the analysis is incomplete. Preserve the
source-authority boundary. Do not push or deploy. Edit only the assigned
one-page scope. Return files changed, validation attempted, source checks, any
blockers, and review status.
```

The main agent must review the worker changes before finalizing.

## Validation Checklist

Minimum:

- `npm run validate:comprehension`
- `npm run validate:manifests`
- `npm run validate:content`
- `npm run build`
- focused browser or Playwright check on desktop and mobile

Release readiness:

- `npm run validate`

No-ai-slop gate:

- artifact type: public explainer page plus maintainer dossier;
- audience: general public, with maintainer traceability;
- purpose: explain one AEther Flow topic without authority drift;
- thesis: derived from the analysis and source evidence;
- result: `pass`, `repair` after direct fix, or `block`.

Default review status after automated validation passes:

- `technical validation passed`

Use `human review pending` only for high-risk, claim-heavy, experimental, or
user-requested human comprehension review cases.
