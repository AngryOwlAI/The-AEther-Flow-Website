# Ontology Document Library Reading Guide

Status: PG-022 system analysis.
Quality gate: pass.
Date: 2026-06-28.

## Question

How should `/resources/documents/` guide public and specialist readers through
the ontology TeX/PDF asset library without weakening the registered TeX source
authority boundary or implying that all downloads are equally current?

## Assumptions and constraints

- The page is a resource library, not a physics-result page.
- Registered TeX sources carry authority for ontology and benchmark material
  when supported by registry metadata and gates.
- PDFs are generated human-readable derivatives.
- Website copies are manifest-backed assets and can drift from the current
  upstream source state until re-imported or reviewed.
- The library must guide readers toward internal explanatory routes before raw
  downloads.

## Source review

Reviewed source families:

- `ontology/README.md`: separates live `ontology/` sources, generated PDFs,
  explanatory Markdown, and legacy snapshots.
- `ontology/tex/README.md`: defines the live registered TeX lane and states
  that PDF derivatives are not independent authority.
- `registries/TEX_SOURCE_REGISTRY.csv`: records the eight live ontology TeX
  rows as `ontology_source`, `canonical`, `benchmark_claim`,
  `canonical_ontology`, and `accepted`, with the explicit note that the current
  canonical ontology package does not prove the broader first-principles GR
  derivation is solved.
- `registries/PDF_DERIVATIVE_REGISTRY.csv`: records PDFs as generated
  human-reading derivatives from registered TeX sources.
- `public/files/manifests/source_manifest.json`: records approved website
  copies of TeX/PDF assets, their hashes, source paths, source commits, claim
  status fields, and generation metadata.

## Reader model

General readers need orientation before downloads:

1. Read the ontology vocabulary page to understand terms and claim boundaries.
2. Read the exact-GR benchmark boundary page to understand benchmark status.
3. Read source authority to understand TeX/PDF and website-source boundaries.
4. Use the document library for direct PDF reading and TeX inspection.

Specialist readers need a document order:

1. Foundations.
2. Dynamics.
3. Geometry.
4. Relativistic Recovery.
5. Consistency.
6. Exact Closure Note.
7. Exact Closure Sequence Overview.
8. Exact Closure Flagship Article.

This order follows the website's existing ontology document order and should be
presented as a reading guide, not as a proof dependency theorem.

## Claim boundaries

Safe:

- The page can say the library exposes approved website copies of ontology TeX
  and PDF assets.
- The page can say registered TeX is the source-inspection target and PDFs are
  reading derivatives.
- The page can surface claim status, research status, promotion status, source
  commit, hashes, and import metadata from manifests.

Unsafe:

- A PDF download proves or promotes a scientific claim.
- A website copy supersedes current upstream registered TeX.
- All files are equally current after upstream ontology changes.
- The canonical ontology package solves the broader first-principles GR
  derivation burden.
- The reading order is a new scientific dependency claim.

## Implementation recommendation

Revise the existing route rather than create a new page:

- add a "read this first" section with internal routes to ontology vocabulary,
  exact-GR benchmark boundary, source authority, and current physics state;
- add a specialist reading-order section using the existing ontology document
  order;
- surface source status on each document card, including TeX authority, claim
  status, research status, ontology promotion status, source commit, import
  timestamp, and PDF derivative role;
- keep the existing TeX/PDF derivative-chain diagram and manifest-backed asset
  list;
- update the page route map to include `registries/PDF_DERIVATIVE_REGISTRY.csv`;
- record browser QA and the known curator source-drift blocker separately.

## Limitations

This analysis does not re-import ontology assets and does not adjudicate the
scientific content of the TeX package. It only defines the public reading guide
and source-status boundary for the website resource page.

## References

The AEther Flow. (2026). `ontology/README.md`.

The AEther Flow. (2026). `ontology/tex/README.md`.

The AEther Flow. (2026). `registries/TEX_SOURCE_REGISTRY.csv`.

The AEther Flow. (2026). `registries/PDF_DERIVATIVE_REGISTRY.csv`.

The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`.
