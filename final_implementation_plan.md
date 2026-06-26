# Final Implementation Plan: Internal Explainer And Source Assets

Date: 2026-06-26

## Analysis

The PRD release has been implemented as a static, source-backed website
release. The implementation keeps the website as a reader-facing presentation
layer and keeps The AEther Flow source repository as the authority surface for
scientific, mathematical, governance, and research-workflow claims.

The release used the existing Astro/Python architecture rather than adding a
new runtime service. Public pages, assets, manifests, validators, and browser
QA now form the control layer for the release.

## Changes Made

1. Planning and agent instructions
   - Added `ImplementationPlans/internal_explainer_and_source_assets_implementation_plan.md`.
   - Added `ImplementationPlans/internal_explainer_and_source_assets_agent_tasks.md`.
   - Updated `AGENTS.md` with project commands, source-authority rules, and definition of done.
   - Added `.github/copilot-instructions.md`.

2. Route and provenance contract
   - Added `public/files/manifests/page_route_map.json`.
   - Added `public/files/manifests/page_provenance.schema.json`.
   - Added generated `public/files/manifests/page_provenance.json`.
   - Added `scripts/generate_page_provenance.py`.
   - Added `scripts/validate_page_provenance.py`.
   - Wired provenance validation into `npm run validate`.

3. Internal explainer coverage
   - Added `/project/operations/`.
   - Added six operations pages:
     - `/project/operations/director-agentjob-lifecycle/`
     - `/project/operations/role-routing/`
     - `/project/operations/validator-operator-workflow/`
     - `/project/operations/publication-process/`
     - `/project/operations/project-system-improvement/`
     - `/project/operations/technical-requirements/`
   - Added `/project/ai-research-agent-system/parent-child-synthesis/`.
   - Added shared internal explainer data and rendering through `src/lib/internalExplainers.ts` and `src/components/InternalExplainerPage.astro`.

4. Internal-first navigation and redirects
   - Updated primary navigation to Overview, Physics, AI System, Operations, Source Authority, and Resources.
   - Removed `/research/map/` from primary navigation while preserving the legacy `/research` redirect.
   - Added the known redirect from `/project/ai-research-agent-system/validator-operator-workflow/` to `/project/operations/validator-operator-workflow/`.
   - Added `scripts/validate_internal_first_links.py` to reject mapped GitHub explainer URLs in primary page/lib/component journey surfaces.

5. Canonical ontology assets
   - Added `scripts/import_ontology_assets.py`.
   - Imported eight ontology PDFs under `public/files/pdf/ontology/`.
   - Imported eight ontology TeX files under `public/files/tex/ontology/`.
   - Updated `source_manifest.json` and `asset_manifest.json`.
   - Deleted old public sample PDF/TeX fixture files.
   - Replaced `/resources/documents/` with an Ontology Documents library using direct PDF reads, PDF downloads, and TeX downloads.

6. Visible provenance and refresh model
   - Updated `SourceNotice` to render clickable current and pinned source links from `page_provenance.json`.
   - Updated visible source refresh dates to render from provenance data.
   - Kept source links visible in provenance sections while primary journey links remain internal-first.

## Review Control

An adversarial review sub-agent inspected the implementation against the PRD.
It found four gaps:

- visible provenance needed clickable links;
- visible refresh dates drifted from provenance dates;
- sample PDF/TeX files remained directly public;
- internal-first link validation scanned only page files.

All four findings were addressed before final validation.

## Verification

Commands run and final results:

- `.venv/bin/python -m pytest` -> 16 passed.
- `npm run validate` -> passed manifests, content, internal-first links, page provenance, Cloudflare config, and Astro build.
- `git diff --check` -> passed.
- `python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict` -> passed.
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4322/` -> passed for 44 routes.
- Playwright rendered QA -> passed for overview desktop, operations desktop, documents desktop/mobile, and validator workflow mobile.

Rendered QA checked:

- one `h1` per sampled page;
- no horizontal overflow on sampled desktop/mobile pages;
- correct active navigation;
- internal overview journey cards;
- operations route-family coverage;
- document actions for Read PDF, Download PDF, and Download TeX;
- visible TeX/PDF authority copy;
- visible provenance date `2026-06-26`;
- clickable source notice links.

Representative artifacts are under `output/playwright/`.

## Remaining Risk

- The page provenance hash currently records local route source files, not every imported component dependency. Component changes are still caught by build/browser QA, but not as page-hash drift.
- The release uses curated summaries for new operations pages. Further editorial review can improve depth without changing the source-authority model.
- Automatic source drift detection is documented as future work and is not implemented as live sync.
- Deployment was intentionally not performed.

## Future Sync Direction

The next sync design should compare recorded source commits, paths, and hashes
against current upstream source state. It should report stale pages/assets as
warnings, generate proposed updates for review, and avoid automatic update or
deletion of published material without explicit review.

## References

AEther-Flow Project. (2026). `github-facing/*.md` [Reviewed generated noncanonical public explainer set].

AEther-Flow Project. (2026). `ontology/README.md` [Ontology source and derivative authority boundary].

AEther-Flow Project. (2026). `ontology/tex/README.md` [Ontology TeX source authority and PDF derivative boundary].

AEther-Flow Project. (2026). `registries/TEX_SOURCE_REGISTRY.csv` [Registered TeX source metadata and claim status].

The AEther Flow Website. (2026). `PRDs/internal-explainer-and-source-assets-prd.md` [Release contract for internal explainers, canonical ontology assets, provenance, and validation].
