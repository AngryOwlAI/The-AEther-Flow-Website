# PG-020 Project-System Improvement QA

Human review status: pending maintainer review.

## Scope

- Route: `/project/operations/project-system-improvement/`
- Page source: `src/pages/project/operations/project-system-improvement/index.astro`
- System analysis: `docs/system-analyses/project-system-improvement-loop.md`
- Dossier: `docs/content-dossiers/operations-project-system-improvement/dossier.md`
- Diagram source: `docs/content-dossiers/operations-project-system-improvement/diagrams/project-system-improvement-loop.mmd`
- Diagram asset: `/assets/diagrams/comprehension/operations-project-system-improvement-loop.png`

## Source-Authority Result

The route explains project-system signals, signal types, sidecars, classifiers,
advisory resolver output, one bounded project-system AgentJob, documentation
impact, PASS completion evidence, and explicit close/defer/reject rules. It
does not create or close signals, create sidecars, replace research handoffs,
change routing behavior, change validator behavior, globally allowlist
sidecars, expand role authority, change checkpoint behavior, or authorize
physics claim promotion.

Committed upstream sources were used because the upstream working tree contains
later dirty source-state material outside this packet's public-claim basis.

## Validation

- `python3 scripts/render_mermaid_diagrams.py` - passed.
- `python3 scripts/build_asset_manifest.py --write` - passed.
- `python3 scripts/generate_page_provenance.py` - passed.
- `npm run validate:manifests` - passed.
- `npm run validate:content` - passed.
- `npm run validate:provenance` - passed.
- `npm run validate:comprehension` - passed.
- `npm run validate:links` - passed.
- `npm run validate:layout` - passed.
- `npm run validate:svg` - passed.
- `npm run build` - passed and generated the project-system improvement route.

## Browser QA

- Desktop screenshot:
  `output/playwright/sitewide-revamp-pg020-project-system-improvement-static-desktop-2026-06-28.png`
- Mobile screenshot:
  `output/playwright/sitewide-revamp-pg020-project-system-improvement-static-mobile-2026-06-28.png`
- Mobile diagram crop:
  `output/playwright/sitewide-revamp-pg020-project-system-improvement-diagram-mobile-crop-2026-06-28.png`

Playwright checks confirmed:

- page title: `Project-System Improvement | The AEther Flow`;
- `h1`: `Project-System Improvement`;
- no horizontal overflow at `1440px` desktop width;
- no horizontal overflow at `390px` mobile width after caption wrapping fix;
- source notice present;
- project-system improvement diagram loaded with nonzero natural dimensions;
- comprehension diagram image fallback is black, matching the dark diagram contract.

## Shared Style Note

Mobile QA exposed long diagram provenance paths overflowing figure captions.
The shared content-figure caption styles now allow long caption/provenance
strings to wrap safely.

## No-AI-Slop Gate

Status: pass.

Reasoning: the route is specific, source-bounded, and useful for both public
readers and maintainers. It names the unsafe overreads directly: maintenance is
not physics continuation, sidecars are not replacement handoffs, resolver
output is advisory, and signals require explicit closure evidence.

## Remaining Limitation

The upstream working tree is dirty, so this route deliberately avoids using
uncommitted later source-state material. The logical next step is maintainer
review after the sitewide packet batch is complete.
