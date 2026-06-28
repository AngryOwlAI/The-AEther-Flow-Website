# Mermaid Palette Contract

Use this contract for The AEther Flow Website Mermaid diagrams. Values are
derived from the live `src/styles/global.css` tokens and written as literal hex
colors because Mermaid theme variables are not CSS variable aware.

The palette contract constrains color, typography, canvas, and baseline
readability. It does not constrain the analyst to one node shape, one border
meaning, or one arrow type. Shapes, borders, arrows, edge labels, and groups
are part of each diagram's semantic grammar and should be selected from the
Mermaid syntax that best explains the system.

## Palette Boundary

Use only the project palette for fills, strokes, text, edge lines, and edge
labels:

- black canvas: `#000000`
- near-black node fill: `#050403`
- elevated near-black fill: `#080401`
- ivory text: `#fff8ef`
- muted ivory stroke: `#d6c3b4`
- cyan fill and stroke family: `#0f364d`, `#164964`, `#2d7ea0`, `#48a0c0`
- orange fill and stroke family: `#270b01`, `#702000`, `#f87800`
- warm highlight stroke: `#f4d6a1`
- white target text when needed for contrast: `#ffffff`

New colors require an explicit design-token update outside this skill.

## Theme Frontmatter

```mermaid
---
config:
  theme: base
  themeVariables:
    darkMode: true
    background: "#000000"
    primaryColor: "#050403"
    primaryTextColor: "#fff8ef"
    primaryBorderColor: "#d6c3b4"
    lineColor: "#d6c3b4"
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "16px"
    clusterBkg: "#080401"
    clusterBorder: "#d6c3b4"
    edgeLabelBackground: "#000000"
---
```

## Semantic Classes

```mermaid
classDef default fill:#050403,stroke:#d6c3b4,color:#fff8ef,stroke-width:1.5px;
classDef source fill:#0f364d,stroke:#48a0c0,color:#fff8ef,stroke-width:2px;
classDef control fill:#270b01,stroke:#f87800,color:#fff8ef,stroke-width:2px;
classDef bridge fill:#164964,stroke:#f4d6a1,color:#fff8ef,stroke-width:2px;
classDef decision fill:#702000,stroke:#f87800,color:#fff8ef,stroke-width:2.25px;
classDef target fill:#2d7ea0,stroke:#f4d6a1,color:#ffffff,stroke-width:2px;
classDef success fill:#164964,stroke:#48a0c0,color:#fff8ef,stroke-width:2px;
classDef risk fill:#702000,stroke:#f87800,color:#fff8ef,stroke-width:2px,stroke-dasharray: 5 5;
classDef boundary fill:#000000,stroke:#f87800,color:#fff8ef,stroke-width:3px,stroke-dasharray: 5 5;
classDef external fill:#080401,stroke:#f4d6a1,color:#fff8ef,stroke-width:2px;

linkStyle default stroke:#d6c3b4,stroke-width:2.25px;
```

These classes are a reusable starter library, not an exhaustive ontology. A
diagram may define additional semantic classes when the class names and visual
treatments are specific to that diagram and all colors come from the palette
boundary above.

## Role Meanings

- `source`: source documents, registries, manifests, and authoritative inputs.
- `control`: ordinary process, operation, route, validation, or publication nodes.
- `bridge`: translation, adaptation, candidate, or transformation nodes.
- `decision`: gates, reviews, choices, and branch points.
- `target`: final reader-facing output or goal state.
- `success`: accepted, approved, complete, or PASS states.
- `risk`: blockers, proof debt, no-go records, and unresolved negative states.
- `boundary`: forbidden implications, non-authority warnings, and hard claim limits.
- `external`: external systems or provenance links outside the primary website journey.

Color is never the only meaning carrier. Use shape, label wording, dashed
boundaries, and nearby prose to preserve accessibility and source discipline.

## Visual Grammar

Define the visual grammar before writing or reviewing the Mermaid:

- shapes should encode node type, such as source artifact, process, review
  gate, data store, output, external system, loop, or terminal state;
- borders should encode status, such as normal, emphasized, blocked,
  unresolved, forbidden, or authority-limited;
- arrows should encode relationship type, such as primary flow, dependency,
  optional path, feedback loop, provenance-only link, failure path, or
  candidate/provisional route;
- edge labels should name relationships when direction alone is ambiguous;
- groups or subgraphs should encode scope only when the group boundary is part
  of the explanation.

Do not use shape, border, arrow, or color variation as decoration. Every visual
distinction should either be self-evident from the labels or explained in
nearby prose, a caption, a Mermaid comment, or a compact legend.
