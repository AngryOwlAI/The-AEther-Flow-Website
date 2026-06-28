# PG-026 External Reviewer Packet QA

Status: browser QA recorded.
Human review status: PG-026 browser QA recorded; maintainer and external review
remain pending.
Date: 2026-06-28.

## Scope

Route reviewed: `/resources/reviewer-packet/`.

PG-026 implemented the external reviewer packet after prerequisite authority
and orientation pages existed. The route places claim boundaries before source
inspection paths and keeps the status at human review pending.

## Files and evidence

- Page source: `src/pages/resources/reviewer-packet/index.astro`
- Dossier: `docs/content-dossiers/reviewer-packet/dossier.md`
- System analysis: `docs/system-analyses/external-review-packet.md`
- Diagram source:
  `docs/content-dossiers/reviewer-packet/diagrams/reviewer-inspection-order.mmd`
- Public diagram: `/assets/diagrams/comprehension/reviewer-inspection-order.png`
- Manifest id: `comprehension_reviewer_inspection_order`

## Validation

Passed:

- `python3 scripts/render_mermaid_diagrams.py`
- diagram source-manifest hash refresh
- `python3 scripts/build_asset_manifest.py --write`
- `python3 scripts/generate_page_provenance.py`
- `npm run validate:comprehension`
- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:provenance`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `git diff --check`
- `npm run build`
- `python3 scripts/quality_gate.py`
- `npm run validate:cloudflare`
- `python3 scripts/run_curator.py --write`

Known non-PG-026 blocker:

- `npm run validate:curator` fails only on the previously known 16 ontology
  TeX/PDF critical source-drift records. No PG-026 curator error was observed.

## No-AI-Slop Refuter Check

Refuter result: pass with human review pending.

- A reader should not be able to infer completed GR derivation: the route names
  no completed derivation before the source inspection links.
- A reader should not be able to infer external validation: the route states
  human review pending and denies peer review, external validation, and
  scientific viability claims.
- A reader should not be able to infer `MetricData(E)`, `g_eff`, matter
  coupling, Einstein equations, benchmark promotion, or downstream GR
  promotion: those blocked claims are stated in the claim-boundary section.
- A reader should not be able to treat diagrams, validators, manifests, or
  reading order as proof: the route separates publication and validation
  evidence from scientific authority.

## Browser QA

Static server: `http://127.0.0.1:4322/resources/reviewer-packet/`.

Screenshots:

- Desktop:
  `output/playwright/sitewide-revamp-pg026-reviewer-packet-static-desktop-2026-06-28.png`
- Mobile:
  `output/playwright/sitewide-revamp-pg026-reviewer-packet-static-mobile-2026-06-28.png`

Observed metrics:

- Desktop viewport: 1440 x 1100.
- Mobile viewport: 390 x 1200.
- H1 count: 1.
- H1 text: `External Reviewer Packet`.
- Claim-boundary heading: `Review the narrow claim, not an inflated one.`
- Images: 2 loaded, 0 unloaded.
- Horizontal overflow: none observed.
- Source notice: visible on desktop and mobile.

Visual result:

- Desktop layout reviewed. Claim boundaries appear before source-inspection
  paths, and route cards remain contained.
- Mobile layout reviewed. Long source references wrap inside the notice,
  sections stack cleanly, and no visual overlap was observed.

## References

The AEther Flow Website. (2026). `docs/system-analyses/external-review-packet.md`.

The AEther Flow Website. (2026). `docs/content-dossiers/reviewer-packet/dossier.md`.

The AEther Flow Website. (2026). `src/data/physics_current_state_snapshot.json`.
