# Internal Explainer And Source Assets Implementation Plan

Date: 2026-06-26

## 1. Files Likely Affected

- `src/pages/project/**`: add missing internal explainer routes and update route family landing pages.
- `src/pages/resources/**`: convert the document library from sample fixtures to ontology documents.
- `src/components/**`: add or adapt shared page, provenance, route-list, and document-action components.
- `src/lib/**`: add route/document metadata and update navigation/resource lists.
- `public/files/manifests/**`: add route/source provenance and update source and asset manifests.
- `public/files/pdf/ontology/**` and `public/files/tex/ontology/**`: import canonical ontology PDF/TeX assets.
- `scripts/**`: add ontology import, page provenance generation, and page provenance validation.
- `tests/**`: cover new validators and manifest behavior.
- `public/_redirects`: add the known operational route redirect.
- `AGENTS.md` and `.github/copilot-instructions.md`: add operational agent guidance.

## 2. Existing Patterns To Follow

- Astro pages live under `src/pages`; shared layout is in `src/layouts/BaseLayout.astro`.
- Current reader pages use `SourceNotice`, `track-page-*`, `content-band`, and manifest-backed resource components.
- Existing validation is Python-first and wired through `npm run validate`.
- Public static assets are committed under `public/`; manifests record site paths, source references, hashes, and status.
- The website remains a presentation layer. The upstream source project remains authoritative.

## 3. Proposed Architecture Changes

- Add a checked-in `page_route_map.json` as the route/source contract.
- Add `page_provenance.schema.json` and generated `page_provenance.json`.
- Add a source-level page provenance validator that fails on missing routes, missing files, hash drift, invalid statuses, or private absolute path leakage.
- Add an intentional ontology import script that copies only `ontology/pdfs/*.pdf` and `ontology/tex/*.tex`, preserves basenames, hashes files, updates manifests, and reports drift without deleting.
- Add a shared internal explainer renderer for the new operations and parent-child pages while keeping one route file per public page.

## 4. Data Model / API / UI Changes

- `page_route_map.json` entries define route path, local page file, upstream source path(s), adaptation type, authority status, publication status, and boundary type.
- `page_provenance.json` records route path, page hash, upstream source hashes, source commit, source commit date, adaptation date, and current plus commit-pinned GitHub URLs.
- `source_manifest.json` and `asset_manifest.json` move document rows from sample fixtures to approved ontology PDF/TeX assets.
- `/resources/documents/` becomes "Ontology Documents" with paired "Read PDF", "Download PDF", and "Download TeX" actions.
- Main navigation becomes Overview, Physics, AI System, Operations, Source Authority, and Resources.

## 5. Risks And Unknowns

- Existing pages contain hand-authored copy. Broad rewriting risks accidental scientific or workflow overclaiming.
- Page hashes must be regenerated after any source edit; otherwise provenance validation should fail.
- Cloudflare redirect behavior should be checked after removing the legacy primary route from navigation.
- Upstream source state is live. Import and provenance scripts must record the live commit at execution time rather than assuming the PRD-observed commit.

## 6. Test Plan

- Run `python3 -m pytest`.
- Run `npm run validate`, which should include manifest, content, provenance, Cloudflare config, and Astro build checks.
- Run the project explainer audit against `dist/`.
- Run preview smoke tests against a local server.
- Run representative browser QA for desktop and mobile if the dev/preview server is available.

## 7. Phased Task Breakdown

1. Route and provenance contract: add route map, schema, generator, validator, and tests.
2. Internal page coverage: add missing operations pages, parent-child page, operations landing, and update internal route cards.
3. Canonical ontology asset import: add import script, run it, update manifests, and replace sample document UI.
4. Navigation, redirects, and shared UI: update primary nav, known redirect, document actions, and resource journey cards.
5. Validation and browser QA: run tests, build, smoke checks, project audit, and representative browser checks.
6. Future sync design: document warning-level drift reporting and review-first sync as follow-up.

## 8. Out Of Scope

- Automatic live synchronization from the source project.
- Backend services or dynamic server-side rendering.
- Full TeX-to-HTML rendering.
- Custom PDF viewer.
- Publishing `legacy_ontology` or research-control draft/control TeX artifacts as current public material.
- Reopening the accepted overview visual direction.
- Deployment; release remains local unless explicitly authorized.
