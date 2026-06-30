# Sitewide Greenfield Route Retirement

Status: GF-013 technical route-retirement note.
Date: 2026-06-30.

## Summary

GF-013 retires the old `/project/*` public route scheme through static
Cloudflare redirects and public manifest cleanup. The new internal-first public
journey is the short route model:

- `/`
- `/physics/*`
- `/ai-research-system/*`
- `/resources/*`

## Redirect Policy

Strong equivalents redirect directly to their replacement routes. Old detailed
routes without one-to-one replacements redirect to the nearest source-bounded
category or status route.

Examples:

- `/project/physics/ontology/` redirects to `/physics/ontology/`.
- `/project/physics/gr-derivation-roadmap/` redirects to
  `/physics/derivation-roadmap/`.
- `/project/physics/distance-to-gr/` redirects to `/physics/open-burdens/`.
- `/project/ai-research-agent-system/one-bounded-agentjob/` redirects to
  `/ai-research-system/agentjob-lifecycle/`.
- `/project/operations/publication-process/` redirects to
  `/resources/publication-process/`.
- `/project/source-authority/` redirects to `/resources/source-authority/`.

## Preservation Rationale

The old `src/pages/project/**` source files are intentionally preserved in this
packet. They are no longer primary public journey routes, and they have been
removed from `public/files/manifests/page_route_map.json`. They remain in the
source tree because `scripts/validate_public_comprehension.py` still validates
those files as legacy public-comprehension evidence. Deleting them safely would
require a validator migration and separate review of the affected content
dossiers.

This is a conservative retirement step:

- public requests use redirects;
- public manifests describe the new route inventory;
- internal route-card data points to the short route model;
- legacy source files remain available for validator continuity and rollback.

## Rollback

Rollback is simple and local:

1. Revert the GF-013 checkpoint commit.
2. Restore the previous `public/_redirects` entries.
3. Restore the previous route and provenance manifests.
4. Re-run the required validators before any deployment decision.

No upstream source files, public assets, generated diagrams, or deployment
state are changed by this packet.
