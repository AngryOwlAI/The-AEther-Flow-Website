# Project Features And Functionality

Date: 2026-07-20

Status: maintainer operating map.

## Purpose And Authority Boundary

This repository builds the reader-facing static website for The AEther Flow
project. It presents, organizes, and publishes reviewed material from the
source research repository without silently changing scientific, mathematical,
governance, or workflow claims.

The upstream repository remains authoritative for source documents, registries,
research-control state, validators, and scientific claim status:

```text
/Volumes/P-SSD/AngryOwl/The-AEther-Flow
```

This document describes the website's features and operating surfaces. It is
not a source-authority record and does not promote any physics claim.

## Reader-Facing Route Map

| Route family | Reader function | Maintainer note |
| --- | --- | --- |
| `/` | Canonical Home entry point for the dual physics-and-AI research program. | Includes the reader capability map at `#project-capabilities`; `/project/overview/` redirects here. |
| `/project/physics/` | Physics track landing page for ontology, benchmark boundary, GR-derivation roadmap, current state, and claim gates. | Keep GR derivation, benchmark compatibility, and ontology status separate. |
| `/project/ai-research-agent-system/` | AI research-agent track for workflow, roles, skills, memory, registries, and parent-child synthesis. | Explain workflow evidence without treating it as physics proof. |
| `/project/operations/` | Operational synthesis for AgentJobs, role routing, validation, publication, project-system improvement, and technical requirements. | Operational success is bounded evidence, not scientific authority. |
| `/documents/` | Canonical Documentation Overview for categories, formats, status, authority roles, provenance, and reading paths. | The five-item Documents menu starts here; `/resources/` is redirect-only compatibility. |
| `/documents/anthology/` | Approved reader-facing anthology PDFs. | Planned or absent publications must not be presented as published. |
| `/documents/research/` | Research collection with direct PDF reading and registered TeX downloads. | Registered TeX carries source authority; PDFs are generated human-readable derivatives. |
| `/documents/governance/` | Front door for approved governance, control, registry, publication, and workflow material. | Public Markdown must remain allowlisted, status-labeled, and separated from internal control records. |
| `/documents/governance/source-authority/` | Trust-boundary page for source records, derivatives, generated surfaces, validators, and memory. | Use this route when public copy needs to clarify authority levels. |
| `/documents/governance/publication-process/` | Publication and provenance system for route maps, page provenance, source and asset manifests, and hash boundaries. | Publication records organize evidence but do not create source truth. |
| `/documents/diagrams/` | Manifest-backed diagram gallery grouped by concept. | Preserve captions, alt text, provenance, and non-authority framing. |
| `/documents/reading-paths/`, `/documents/reviewer-packet/`, `/documents/derivatives/` | Contextual reading, review, and generated-derivative destinations outside the five-item dropdown. | These assemble or explain existing evidence and must not strengthen its status. |

Primary navigation should remain concise: Home, Physics Research, AI Research
System, and Documents. Internal links use `/documents/.../`; retired
`/resources/.../` paths exist only as direct semantic redirects.

## Public Assets And Manifests

Public files live under `public/` and are copied into `dist/` by Astro.

Core manifests:

- `public/files/manifests/page_route_map.json`: route-to-source mapping
  contract.
- `public/files/manifests/page_provenance.json`: generated page hash and source
  provenance data.
- `public/files/manifests/source_manifest.json`: source and asset approval
  metadata.
- `public/files/manifests/asset_manifest.json`: public file paths, hashes,
  source references, and byte sizes.
- `public/files/manifests/document_catalog.json`: logical document records,
  categories, formats, source roles, publication status, and asset references.

Canonical ontology assets are committed under:

- `public/files/pdf/ontology/`
- `public/files/tex/ontology/`

Registered TeX carries source authority for this collection; PDFs are generated
human-readable derivatives. The document catalog and rendered Documents pages
index those roles and provenance without becoming scientific authority.

Use `scripts/import_ontology_assets.py` for intentional ontology refreshes and
`scripts/import_document_collection.py` for approved collection imports. These
tools update bounded catalog or manifest records; they must preserve unrelated
records and must not silently delete website files.

## Validation And Quality Gates

Repository validation entry points are defined in `package.json`.

Common commands:

```bash
npm run validate
npm run quality
python3 -m pytest
```

`npm run validate` currently checks manifest paths and the document catalog,
content sources, public claims, internal-first links, layout and SVG policy,
page provenance, curator state, Cloudflare static files, implementation-control
and plan-goal state, focused plan-goal tests, and the Astro build.

After editing a public page, update the relevant page provenance hash before
expecting `npm run validate:provenance` to pass. If route mappings, public
assets, or source bindings change, update the corresponding manifests and
rerun the relevant validators.

## Curator And Current-State Workflow

The current-state feature exposes a checked-in snapshot of upstream physics
control state at:

```text
/project/physics/current-state/
```

Important files:

- `src/data/physics_current_state_snapshot.json`
- `scripts/refresh_physics_current_state_snapshot.py`
- `scripts/run_curator.py`
- `curator/reports/latest.json`
- `curator/reports/latest.md`
- `curator/acknowledgements/`

The curator detects drift and participates in validation. It must not rewrite
public pages, public manifests, public assets, or public claims automatically.

## Deployment Model

The production site is deployed to Cloudflare Pages by Wrangler Direct Upload:

```text
https://the-aether-flow-website.pages.dev/
```

Use the deployment guide for current constraints and commands:

```text
docs/deployment/cloudflare-pages.md
```

Deployment is a separate explicit action. A documentation or implementation
packet should stop at deployment readiness unless deployment is requested.
Local validation does not imply staging, commit, push, deployment, or
production verification; record and authorize each applicable release action
separately.

## Repo-Local Codex Skills

Project-local skills live under:

```text
.codex/skills/
```

Current important skills:

- `implementation-control`: resolves live website-local packets, allowed
  scopes, validators, and local checkpoints.
- `system-analysis`: creates source-grounded analysis Markdown with native
  source-authority and pass/repair/block quality gates.
- `mermaid-diagram-style`: governs Mermaid diagram styling, static rendering,
  and diagram source-authority boundaries.
- `prototype`: local throwaway design exploration.
- `to-prd`: repository-local PRD synthesis.
- `prd-to-implementation-plan`: PRD-to-task planning.
- `push-and-deploy`: push, build, Direct Upload deploy, and production smoke
  test workflow.

These skills guide repository work. They do not replace source authority,
validation gates, or explicit deployment approval.

## Maintenance Checklist

- Inspect existing repository files before changing architecture, commands, or
  validation assumptions.
- Keep reader journeys internal-first; use GitHub/source links as provenance
  unless explicitly approved otherwise.
- Use canonical `/documents/.../` links. Keep `/resources/.../` references only
  where redirect compatibility itself is being documented or tested.
- Preserve claim boundaries when editing public copy.
- Preserve the registered-TeX/source and PDF/generated-derivative distinction;
  do not treat catalogs, manifests, pages, or validator passes as claim proof.
- Update manifests when public routes, public assets, source mappings, or page
  hashes change.
- Run `npm run validate` for normal release readiness.
- Run `npm run quality` when rendered frontend pages, public manifests, or
  assets change.
- Use preview and `scripts/smoke_test_site.py` before deployment when route
  behavior or public assets change.
- Record commit and push status independently, and do not deploy unless
  deployment is explicitly requested.

## References

The AEther Flow Website. (2026). `README.md` [Repository file].

The AEther Flow Website. (2026). `package.json` [Repository file].

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`
[Repository file].

The AEther Flow Website. (2026). `docs/deployment/cloudflare-pages.md`
[Repository file].

The AEther Flow Website. (2026).
`ImplementationPlans/aether-flow-documents-navigation-implementation-plan.canonical.json`
[Accepted implementation plan].

The AEther Flow Website. (2026). `public/files/manifests/document_catalog.json`
[Repository file].
