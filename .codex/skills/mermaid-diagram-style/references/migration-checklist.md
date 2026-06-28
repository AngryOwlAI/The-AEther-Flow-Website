# Mermaid Migration Checklist

Use this checklist before committing Mermaid source or generated diagram assets.

## Source Edits

- Keep graph topology, node identifiers, and reader-facing labels stable unless
  the route dossier requires a content correction.
- Preserve intentional shape, border, arrow, edge-label, and group semantics.
  If a migration changes one of those meanings, document why.
- Add the canonical frontmatter config from `palette-contract.md`.
- Use semantic `classDef` entries from `palette-contract.md`, or
  diagram-specific `classDef` entries whose colors come from the same palette.
- Use `linkStyle default stroke:#d6c3b4,stroke-width:2.25px;`.
- Prefer class assignments over inline `style` statements.
- Use decision shapes for gates and choices unless the diagram defines a more
  precise visual grammar for that case.
- Use `risk` or `boundary` for blocked, forbidden, or non-authoritative states.
- Do not replace meaningful varied arrows or borders with defaults merely to
  simplify styling.
- Keep source-authority language exact; do not turn a reader aid into a claim.

## Render And Validate

Run these commands after changing comprehension Mermaid diagrams:

```bash
python3 scripts/render_mermaid_diagrams.py
python3 scripts/build_asset_manifest.py --write
npm run validate:comprehension
```

Run `npm run validate` before final delivery when the diagram packet is complete.

## Visual QA

Inspect `/resources/diagrams/` plus at least one physics route, one AI route,
and one operations route at desktop and mobile widths. Confirm:

- black diagram background,
- readable ivory text,
- visible cyan/orange semantic roles,
- arrows are thicker than the previous default,
- no clipped labels or diagram overflow,
- captions and nearby prose still state that diagrams are reader aids, not
  source authority.
