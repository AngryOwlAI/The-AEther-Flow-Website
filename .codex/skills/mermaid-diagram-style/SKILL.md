---
name: mermaid-diagram-style
description: Create, review, or migrate Mermaid diagrams for The AEther Flow Website using the repo's Angry Owl black, cyan, orange, and ivory palette, Inter font stack, dark canvas, semantic class definitions, thicker arrows, static PNG rendering workflow, and source-authority boundary. Use when working on .mmd files, public comprehension diagrams, Mermaid styling, generated diagram PNGs, or diagram manifest validation in this repository.
---

# Mermaid Diagram Style

## Purpose

Style Mermaid diagrams for The AEther Flow Website as static, source-backed
reader aids. Use the website's live design tokens, preserve source-authority
boundaries, and avoid treating diagrams as scientific, mathematical, workflow,
or governance authority.

## Required Workflow

1. Inspect the diagram goal, route dossier, and nearby page copy before editing.
2. Read `references/palette-contract.md` before creating or restyling Mermaid.
3. Read `references/migration-checklist.md` before migrating existing diagrams
   or regenerating public PNG assets.
4. Use `scripts/apply_mermaid_style.py` for existing `.mmd` files when possible.
5. Render changed comprehension diagrams with `python3 scripts/render_mermaid_diagrams.py`.
6. Regenerate asset hashes with `python3 scripts/build_asset_manifest.py --write`
   when public diagram PNGs change.
7. Run the relevant validators. At minimum, run `npm run validate:comprehension`
   for comprehension diagrams.

## Diagram Contract

Every Mermaid comprehension diagram should use:

- Mermaid frontmatter `config`, not the deprecated init directive.
- `theme: base`, because custom theme variables are intended for the base theme.
- A black canvas, ivory text, Angry Owl cyan/orange semantic roles, and the
  repository font stack.
- Reusable `classDef` classes rather than repeated inline `style` statements.
- Shape plus color: decisions use Mermaid decision shapes, blockers use dashed
  borders, and authority boundaries are explicitly labeled.
- `linkStyle default stroke:#d6c3b4,stroke-width:2.25px;`.

Do not add runtime Mermaid rendering to public pages. This repository publishes
static PNG diagrams generated from tracked `.mmd` sources.

## Helper Script

Apply the canonical style contract to all public comprehension diagrams:

```bash
python3 .codex/skills/mermaid-diagram-style/scripts/apply_mermaid_style.py \
  --all-comprehension-diagrams
```

Apply it to selected files:

```bash
python3 .codex/skills/mermaid-diagram-style/scripts/apply_mermaid_style.py \
  docs/content-dossiers/resources-diagrams/diagrams/diagram-publication-boundary.mmd
```

The script is deliberately conservative. It preserves graph topology and node
labels, replaces known Mermaid styling surfaces, and fails closed for diagrams
without a `flowchart` or `graph` declaration or with unsupported style syntax.

## Source-Authority Boundary

Diagrams may orient readers, show routing, and clarify relationships. They must
not create, strengthen, or silently promote scientific, mathematical,
governance, or research-workflow claims. Keep labels close to source language,
and use boundary/risk classes for blocked, forbidden, or non-authoritative
states.
