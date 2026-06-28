# Publication And Provenance System

Status: PG-024 system analysis.
Quality gate: pass.
Date: 2026-06-28.

## Question

How should the website explain its publication/provenance system so public
readers understand why provenance exists and maintainers can identify which
manifest does what?

## Assumptions and constraints

- The website is a static Astro publication layer for the upstream research
  repository.
- Upstream source files, registries, and governed records remain authoritative
  for scientific, mathematical, governance, and workflow claims.
- Manifest presence does not make a claim true.
- Public copy must avoid local absolute paths.
- Source links are provenance links; internal website routes remain the primary
  reader journey when available.

## Source review

Reviewed website sources:

- `docs/architecture/website-feature-and-functionality.md`: defines route
  families, manifest and provenance model, validation gates, and deployment
  boundary.
- `public/files/manifests/page_route_map.json`: maps public routes to source
  basis, adaptation type, publication status, and boundary type.
- `public/files/manifests/page_provenance.json`: records route page hashes,
  upstream source hashes, source commit metadata, and GitHub provenance URLs.
- `public/files/manifests/source_manifest.json`: records public asset source
  paths, approval status, hashes, notes, and claim/status metadata.
- `public/files/manifests/asset_manifest.json`: records served asset paths,
  byte counts, hashes, titles, kinds, and source-manifest references.
- `scripts/generate_page_provenance.py`: builds page provenance from route map
  and upstream source state.
- `scripts/validate_page_provenance.py`: validates route coverage, page/source
  hashes, manifest shape, and local-path leak boundaries.
- `scripts/validate_manifest_paths.py`: validates public asset existence and
  hash integrity.
- `scripts/validate_internal_first_links.py`: enforces internal-first reader
  routing where mapped routes exist.

## Provenance model

The publication system has two related tracks:

1. Page provenance:
   - `page_route_map.json` declares a route's source basis and boundary.
   - `page_provenance.json` records the generated page hash and source hashes
     for that route.
   - Validation checks that route-map and provenance entries agree.

2. Asset provenance:
   - `source_manifest.json` declares source/status metadata for public files.
   - `asset_manifest.json` records the actual served file path, byte count, and
     hash.
   - Validation checks that files exist and hashes match.

The two tracks make static publication auditable. They do not adjudicate
scientific truth.

## Internal-first routing

Internal-first routing keeps the reading path on the website when a reviewed
route exists. GitHub links remain visible as provenance and source inspection
paths. This prevents the primary public journey from becoming a scattered list
of source links while still preserving auditability.

## Claim boundaries

Safe:

- The route can explain what each manifest records.
- The route can explain how page hashes and source hashes constrain
  publication.
- The route can explain why source links remain provenance links.

Unsafe:

- Manifest presence proves a scientific claim.
- A page hash proves a page is conceptually correct.
- A source hash promotes a claim or resolves a gate.
- Internal-first routing hides source authority.
- A public page supersedes upstream source files or registries.

## Implementation recommendation

Create `/project/source-authority/publication-and-provenance-system/` as a
source-authority child route:

- use page-local Astro content, consistent with the existing source-authority
  landing style;
- add a small static Mermaid diagram showing source basis, route map, page
  provenance, source manifest, asset manifest, static build, and internal-first
  reader routes;
- add the route to `projectSourceAuthorityRoutes`;
- add page route-map/provenance coverage;
- add a content dossier and public-comprehension registration;
- link back to source-authority landing and resources.

## Limitations

This analysis does not change manifest schema, validators, deployment, or
source authority. It only defines the reader-facing explanation for existing
publication and provenance surfaces.

## References

The AEther Flow Website. (2026). `docs/architecture/website-feature-and-functionality.md`.

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`.

The AEther Flow Website. (2026). `public/files/manifests/page_provenance.json`.

The AEther Flow Website. (2026). `public/files/manifests/source_manifest.json`.

The AEther Flow Website. (2026). `public/files/manifests/asset_manifest.json`.

The AEther Flow Website. (2026). `scripts/generate_page_provenance.py`.

The AEther Flow Website. (2026). `scripts/validate_page_provenance.py`.

The AEther Flow Website. (2026). `scripts/validate_manifest_paths.py`.

The AEther Flow Website. (2026). `scripts/validate_internal_first_links.py`.
