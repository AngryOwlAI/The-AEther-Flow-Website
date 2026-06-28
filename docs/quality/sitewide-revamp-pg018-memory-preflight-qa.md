# PG-018 Memory Preflight And Source-First Retrieval QA

Human review status: pending maintainer review.

## Scope

- Route: `/project/ai-research-agent-system/memory-registries/`
- Page source: `src/pages/project/ai-research-agent-system/memory-registries/index.astro`
- System analysis: `docs/system-analyses/memory-preflight-and-source-first-retrieval.md`
- Dossier: `docs/content-dossiers/ai-memory-registries/dossier.md`
- Diagram source: `docs/content-dossiers/ai-memory-registries/diagrams/source-first-memory-layers.mmd`
- Diagram asset: `/assets/diagrams/comprehension/ai-memory-source-first-layers.png`

## Source-Authority Result

The route explains memory preflight, source-first retrieval, canonical
inspection, registry inspection, and receipt evidence from committed upstream
records. It does not expose private memory contents, change memory behavior,
change registry schemas, override tracked sources, promote generated
derivatives, prove claims, or bypass AgentJob and human-gate boundaries.

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
- `npm run build` - passed and generated the memory-preflight route.

## Browser QA

- Desktop screenshot:
  `output/playwright/sitewide-revamp-pg018-memory-preflight-static-desktop-2026-06-28.png`
- Mobile screenshot:
  `output/playwright/sitewide-revamp-pg018-memory-preflight-static-mobile-2026-06-28.png`
- Mobile diagram crop:
  `output/playwright/sitewide-revamp-pg018-memory-diagram-mobile-crop-2026-06-28.png`

Playwright checks confirmed:

- page title: `Memory Preflight And Source-First Retrieval | The AEther Flow`;
- `h1`: `Memory Preflight And Source-First Retrieval`;
- no horizontal overflow at `1440px` desktop width;
- no horizontal overflow at `390px` mobile width;
- source notice present;
- memory-preflight diagram loaded with nonzero natural dimensions;
- comprehension diagram image fallback is black, matching the dark diagram contract.

## Shared Component Note

During mobile QA, the comprehension diagram initially appeared as a blank light
rectangle in the screenshot path. The shared `ComprehensionBlocks` figure now
requests eager loading for comprehension diagrams, and the comprehension image
fallback is black rather than ivory.

## No-AI-Slop Gate

Status: pass.

Reasoning: the route is specific, source-bounded, and public-safe. It explains
the method without exposing private memory contents and directly names the
unsafe overread: retrieval hits and receipts do not override tracked source
authority or prove claims.

## Remaining Limitation

The upstream working tree is dirty, so this route deliberately avoids using
uncommitted later source-state material. The logical next step is maintainer
review after the sitewide packet batch is complete.
