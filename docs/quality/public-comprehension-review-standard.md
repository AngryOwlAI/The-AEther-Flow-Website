# Public Comprehension Review Standard

Status: maintainer-facing quality standard.
Date: 2026-06-27

## Purpose

The public comprehension review checks whether an unfamiliar reader can
understand what a route explains, what source material supports it, what the
website must not claim, and where to go next. It supplements deterministic
validation; it does not replace source authority or human review.

## Review Inputs

- Route dossier under `docs/content-dossiers/`.
- Upstream source paths from `public/files/manifests/page_route_map.json`.
- Rendered page at desktop and mobile viewports.
- Diagram source and generated public diagram image, when applicable.
- Page provenance and asset manifests after changes.
- `npm run validate:comprehension` output.

## Required Checks

1. The page opens with reader context before internal labels dominate.
2. Specialized terms are defined near use.
3. Source authority and claim limits are visible.
4. Internal website routes are the primary next steps.
5. Source and GitHub links are provenance or inspection links.
6. Diagrams have editable source, static public image output, alt text,
   caption, and nearby explanatory prose.
7. Equations have symbol meanings, assumptions, and limits when displayed or
   substantively referenced.
8. Safe and unsafe summaries exist for routes with overclaim risk.
9. The page does not imply completed GR derivation, autonomous AI research
   ownership, role-permission expansion, or validator PASS beyond the checked
   state.
10. Desktop and mobile rendering show no overlap, clipped controls, or diagram
    overflow.

## Human Review Status

Human review must be recorded as one of:

- `pending maintainer review`
- `reviewed with changes requested`
- `reviewed and accepted`

The first implementation pass may record `pending maintainer review`, but it
must not describe Phase 1 as publicly accepted until a maintainer accepts the
review.

## References

The AEther Flow Website. (2026). `AGENTS.md` [Repository operating rules].

The AEther Flow Website. (2026).
`PRDs/public-comprehension-and-diagram-system-prd.md` [Product requirements
document].
