# Internal Explainer And Source Assets Agent-Ready Tasks

Date: 2026-06-26

## Task: Add route/source provenance contract

### Goal
Create the machine-readable route/source contract and fail-closed page provenance validation.

### Context
PRD section: Provenance Model and Phase 1. Relevant files:
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/page_provenance.schema.json`
- `scripts/generate_page_provenance.py`
- `scripts/validate_page_provenance.py`
- `package.json`
- `tests/`

### Requirements
- Cover all 17 mapped explainer routes, `/project/operations/`, `/resources/documents/`, and `/resources/`.
- Record page hashes, upstream source hashes when available, source commit, source commit date, and GitHub URLs.
- Reject missing routes, missing page files, invalid statuses, hash drift, or absolute local path leakage.

### Constraints
- Do not add runtime dependencies.
- Do not treat website pages as upstream authority.

### Acceptance Criteria
- `python3 scripts/validate_page_provenance.py` passes after generation.
- `npm run validate` includes provenance validation.
- Tests cover current manifest success and a hash-drift or missing-file failure.

### Validation Commands
```bash
python3 -m pytest
npm run validate
```

## Task: Add internal operations and parent-child explainer pages

### Goal
Complete internal page coverage for the PRD route map.

### Context
PRD section: Route Map and Phase 2. Relevant files:
- `src/pages/project/operations/**`
- `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro`
- `src/components/InternalExplainerPage.astro`
- `src/lib/internalExplainers.ts`
- `src/lib/siteContent.ts`

### Requirements
- Add `/project/operations/` synthesis page.
- Add six operations detail pages.
- Add `/project/ai-research-agent-system/parent-child-synthesis/`.
- Preserve qualifiers such as `draft/control`, `proposal-only`, human-gated authority, and generated noncanonical status when relevant.

### Constraints
- Use upstream `github-facing` explainers as source support.
- Keep GitHub links in provenance/source zones, not primary journey cards.

### Acceptance Criteria
- All route files exist.
- Page content has visible boundary statements.
- Internal route cards point to website routes.

### Validation Commands
```bash
npm run build
python3 scripts/validate_page_provenance.py
```

## Task: Import canonical ontology PDF and TeX assets

### Goal
Replace public document samples with canonical ontology PDF/TeX assets.

### Context
PRD section: Asset Scope and Phase 3. Relevant files:
- `scripts/import_ontology_assets.py`
- `public/files/pdf/ontology/**`
- `public/files/tex/ontology/**`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `src/pages/resources/documents.astro`
- `src/lib/manifests.ts`

### Requirements
- Copy only `ontology/pdfs/*.pdf` and `ontology/tex/*.tex`.
- Preserve basenames and compute SHA-256 hashes.
- Remove sample PDF/TeX entries from public manifests and public UI.
- State that TeX files carry source authority and PDFs are generated human-readable derivatives.

### Constraints
- Do not publish `legacy_ontology`.
- Do not delete website files automatically from the import script.

### Acceptance Criteria
- Eight PDF and eight TeX ontology files are present under stable public paths.
- The document library shows paired PDF/TeX actions.
- Manifest validation passes.

### Validation Commands
```bash
python3 scripts/import_ontology_assets.py
npm run validate:manifests
npm run build
```

## Task: Update navigation, redirects, and resource journeys

### Goal
Make the website internal-first while preserving known deployed shortcuts.

### Context
PRD section: Information Architecture, Redirects, and Internal-First Link Behavior. Relevant files:
- `src/lib/siteContent.ts`
- `src/pages/project/physics/index.astro`
- `src/pages/project/ai-research-agent-system/index.astro`
- `src/pages/resources/index.astro`
- `public/_redirects`

### Requirements
- Primary navigation includes Overview, Physics, AI System, Operations, Source Authority, Resources.
- Remove `/research/map/` from primary navigation.
- Add `/project/ai-research-agent-system/validator-operator-workflow/` to `/project/operations/validator-operator-workflow/` redirect.
- Primary journey cards for mapped explainers use internal routes.

### Constraints
- Preserve `/research` as a legacy shortcut.
- Do not add speculative route aliases.

### Acceptance Criteria
- Navigation renders the new primary route families.
- Known redirect is present.
- Content validation finds no mapped-source GitHub links in primary journey zones.

### Validation Commands
```bash
npm run validate
```

## Task: Run release validation and adversarial review

### Goal
Close the PRD implementation with executable checks and a review-controlled final implementation plan.

### Context
PRD section: Release Definition Of Done and Testing Decisions. Relevant files:
- `final_implementation_plan.md`
- `scratch/project-explainer/**`
- `output/playwright/**`

### Requirements
- Run unit tests, validation, build, project frontend audit, preview smoke tests, and representative browser QA where possible.
- Perform an adversarial review against the PRD.
- Record residual risks and follow-up tasks.

### Constraints
- Do not deploy without explicit authorization.
- Do not modify code during the adversarial review step.

### Acceptance Criteria
- Validation results are summarized.
- Review findings are addressed or explicitly deferred.
- `final_implementation_plan.md` reflects implementation, validation, review, risks, and future sync design.

### Validation Commands
```bash
python3 -m pytest
npm run validate
python3 .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py --site dist --out-dir scratch/project-explainer --strict
```
