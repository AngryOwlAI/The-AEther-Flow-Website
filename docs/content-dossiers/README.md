# Public Comprehension Content Dossiers

Status: maintainer-facing editorial workflow.

This directory records the source-derived preparation work for public page
rewrites. A dossier is not source authority. It is an editorial contract that
connects one public route to the upstream source files, claim boundaries,
glossary, diagrams, equation walkthroughs, and human review checks needed before
the route is rewritten.

The upstream source repository remains authoritative for scientific,
mathematical, governance, workflow, validator, routing, memory, and registry
claims:

```text
/Volumes/P-SSD/AngryOwl/The-AEther-Flow
```

## Workflow

1. Start from `_template.md`.
2. Identify the public route and reader job.
3. Inspect the route's upstream source paths from
   `public/files/manifests/page_route_map.json`.
4. Summarize source material without large quotations.
5. Record claim boundaries and forbidden implications before public copy is
   edited.
6. Record diagram source and generated public image paths when a diagram is
   needed.
7. Record equation walkthrough requirements when equations are displayed or
   substantively referenced.
8. Record safe and unsafe summaries for high-risk routes.
9. Run `npm run validate:comprehension` after the audit command exists.
10. Record human review status under `docs/quality/`; a script PASS cannot
    replace human comprehension review.

## Directory Convention

Use one directory per route-oriented dossier:

```text
docs/content-dossiers/project-overview/dossier.md
docs/content-dossiers/project-overview/diagrams/two-track-project-map.mmd
```

Generated public diagram images belong under:

```text
public/assets/diagrams/comprehension/
```

Mermaid source stays here with the dossier so maintainers can edit the diagram
in the same context as the source basis and claim boundaries.

## Authority Boundary

Website pages may explain, organize, and link reviewed material. They must not
silently strengthen source claims, convert generated derivatives into canonical
sources, turn validator PASS into scientific proof, grant role authority, or
claim a completed GR derivation where the upstream source keeps the derivation
burden open.

## Validation

Use the focused audit as a support gate:

```bash
npm run validate:comprehension
```

Use full repository validation before release readiness:

```bash
npm run validate
```

The comprehension audit is intentionally conservative. It checks that required
editorial evidence exists; it does not prove that an unfamiliar reader now
understands the page. Human review remains required.

## References

The AEther Flow Website. (2026). `AGENTS.md` [Repository operating rules].

The AEther Flow Website. (2026).
`PRDs/public-comprehension-and-diagram-system-prd.md` [Product requirements
document].

The AEther Flow Website. (2026).
`public/files/manifests/page_route_map.json` [Route-to-source mapping contract].
