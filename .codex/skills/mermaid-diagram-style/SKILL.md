---
name: mermaid-diagram-style
description: Create, review, or migrate Mermaid diagrams for The AEther Flow Website using the repo's Angry Owl black, cyan, orange, and ivory palette, Inter font stack, dark canvas, semantic visual grammar, thicker arrows, static PNG rendering workflow, and source-authority boundary. Use when working on .mmd files, public comprehension diagrams, Mermaid styling, generated diagram PNGs, or diagram manifest validation in this repository.
---

# Mermaid Diagram Style

## Purpose

Style Mermaid diagrams for The AEther Flow Website as static, source-backed
reader aids. Use the website's live design tokens, preserve source-authority
boundaries, and avoid treating diagrams as scientific, mathematical, workflow,
or governance authority.

This skill owns the project visual contract: palette, font, dark canvas,
rendering workflow, and source-authority discipline. It does not own every
diagram's semantic grammar. The diagram author or system analyst must choose
shapes, borders, arrows, labels, grouping, and edge styles because they explain
the specific system under analysis.

## Required Workflow

1. Inspect the diagram goal, route dossier, and nearby page copy before editing.
2. Read `references/palette-contract.md` before creating or restyling Mermaid.
3. Define the diagram's visual grammar before writing Mermaid. Record what
   shapes, borders, arrows, edge labels, groups, and color classes mean when
   the meaning is not obvious from the labels.
4. Read `references/migration-checklist.md` before migrating existing diagrams
   or regenerating public PNG assets.
5. Use `scripts/apply_mermaid_style.py` for existing `.mmd` files when possible
   and when it preserves the intended grammar.
6. Render changed comprehension diagrams with `python3 scripts/render_mermaid_diagrams.py`.
7. Regenerate asset hashes with `python3 scripts/build_asset_manifest.py --write`
   when public diagram PNGs change.
8. Run the relevant validators. At minimum, run `npm run validate:comprehension`
   for comprehension diagrams.

## Diagram Contract

Every Mermaid comprehension diagram should use:

- Mermaid frontmatter `config`, not the deprecated init directive.
- `theme: base`, because custom theme variables are intended for the base theme.
- A black canvas, ivory text, Angry Owl cyan/orange semantic roles, and the
  repository font stack.
- Reusable `classDef` classes rather than repeated inline `style` statements.
  Canonical classes from `palette-contract.md` are defaults, not the full
  expressive limit.
- A diagram-specific visual grammar. Shapes, borders, arrows, edge labels,
  clusters, and line styles must carry meaning or be omitted.
- Mermaid shapes chosen for the system being explained. Gates and choices
  usually use decision shapes, but artifacts, records, stores, external
  systems, transformations, loops, and terminal states may use different
  Mermaid shapes when that improves comprehension.
- Border and arrow variations only when they encode meaning. For example,
  dashed borders can mark unresolved or forbidden states; dashed arrows can
  mark optional, provisional, blocked, or provenance-only relationships; solid
  arrows can mark the primary flow; bidirectional arrows can mark mutual
  dependency.
- Project-palette colors. Custom diagram-specific `classDef` names are allowed
  when their fill, stroke, and text colors come from the palette contract and
  their meanings are documented near the diagram.
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

The script is deliberately conservative. It preserves graph topology, node
labels, and ordinary edge syntax, replaces known Mermaid styling surfaces, and
fails closed for diagrams without a `flowchart` or `graph` declaration or with
unsupported style syntax. Do not flatten an intentionally meaningful diagram to
fit the helper script. If a diagram needs custom palette-conformant classes,
subgraphs, special border meanings, or edge-specific semantics that the script
cannot preserve, style it manually and validate the rendered result.

## Source-Authority Boundary

Diagrams may orient readers, show routing, and clarify relationships. They must
not create, strengthen, or silently promote scientific, mathematical,
governance, or research-workflow claims. Keep labels close to source language,
and use boundary/risk classes for blocked, forbidden, or non-authoritative
states.
