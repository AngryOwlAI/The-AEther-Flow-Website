# Project Features And Functionality

Date: 2026-06-26

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
| `/project/source-authority/` | Trust-boundary page for source records, derivatives, generated surfaces, validators, and memory. | Use this route when public copy needs to clarify authority levels. |
| `/resources/` | Manifest-backed resource index. | Keep resource cards internal-first and status-labeled. |
| `/resources/documents/` | Ontology document library with direct PDF reading and TeX downloads. | Registered TeX carries source authority; PDFs are generated human-readable derivatives. |
| `/project/source-authority/publication-and-provenance-system/` | Publication/provenance route replacing the old research-map prototype. | Use this when readers need route-map, page-provenance, source-manifest, asset-manifest, and hash-boundary context. |
| `/resources/guided-starts/`, `/resources/reviewer-packet/` | Specialist guided starts and human-review-pending reviewer packet. | These assemble existing sourced pages and must not create new claims. |

Primary navigation should remain concise: Home, Physics, AI system,
Operations, Source authority, and Resources.

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

Canonical ontology assets are committed under:

- `public/files/pdf/ontology/`
- `public/files/tex/ontology/`

Use `scripts/import_ontology_assets.py` for intentional ontology asset import.
It should copy approved assets and update manifests; it should not silently
delete website files.

## Validation And Quality Gates

Repository validation entry points are defined in `package.json`.

Common commands:

```bash
npm run validate
npm run quality
python3 -m pytest
```

`npm run validate` currently checks manifests, content sources, internal-first
links, page provenance, curator state, Cloudflare static files, and the Astro
build.

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

## Repo-Local Codex Skills

Project-local skills live under:

```text
.codex/skills/
```

Current important skills:

- `project-explainer-frontend`: source-boundary-aware frontend implementation
  and QA workflow.
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
- Preserve claim boundaries when editing public copy.
- Update manifests when public routes, public assets, source mappings, or page
  hashes change.
- Run `npm run validate` for normal release readiness.
- Run `npm run quality` when rendered frontend pages, public manifests, or
  assets change.
- Use preview and `scripts/smoke_test_site.py` before deployment when route
  behavior or public assets change.
- Do not deploy unless deployment is explicitly requested.

## References

The AEther Flow Website. (2026). `README.md` [Repository file].

The AEther Flow Website. (2026). `package.json` [Repository file].

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`
[Repository file].

The AEther Flow Website. (2026). `docs/deployment/cloudflare-pages.md`
[Repository file].
