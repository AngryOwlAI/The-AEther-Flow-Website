# Mermaid Palette Contract

Use this contract for The AEther Flow Website Mermaid diagrams. Values are
derived from the live `src/styles/global.css` tokens and written as literal hex
colors because Mermaid theme variables are not CSS variable aware.

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
