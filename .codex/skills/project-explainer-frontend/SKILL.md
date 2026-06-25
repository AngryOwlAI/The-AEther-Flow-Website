---
name: project-explainer-frontend
description: Build or redesign an informational frontend for The AEther Flow Website from repository evidence, while preserving the source-authority boundary.
disable-model-invocation: true
---

# Project Explainer Frontend

## Purpose

Create evidence-backed, accessible, reader-facing frontend plans and pages for
The AEther Flow Website.

This skill is adapted for this repository. The website is a public presentation
surface. It may explain reviewed material, organize resources, and improve
reader navigation. It must not silently create, strengthen, or reword
scientific, mathematical, governance, or research-workflow claims from the
upstream AEther Flow project.

## Use When

- The task asks for a project website, landing page, explainer page, visual
  frontend, documentation frontend, or GitHub-facing presentation surface.
- The task asks to adapt visual direction from reference images for a project
  explainer.
- The task asks to make AEther Flow material easier for readers to understand.

Do not use this skill for backend-only work, research derivation, validator
repair, or source-repository claim changes unless the deliverable is an
informational frontend.

## Source Authority Boundary

The upstream source project remains authoritative for scientific, mathematical,
governance, and research-workflow claims. If the upstream source root cannot be
inspected, fail closed: write only website-scaffold or explicitly explanatory
copy, and do not add new public claims.

Default source root:

```bash
/Volumes/P-SSD/AngryOwl/The-AEther-Flow
```

## Workflow

### 1. Scan website and source evidence

```bash
python .codex/skills/project-explainer-frontend/scripts/scan_project_story.py \
  --repo . \
  --source-root /Volumes/P-SSD/AngryOwl/The-AEther-Flow \
  --out-dir scratch/project-explainer
```

Read the generated files before making strong claims:

- `scratch/project-explainer/project_story_brief.json`
- `scratch/project-explainer/project_story_brief.md`

The scanner output is a map, not proof. Inspect relevant source files directly
before writing final copy.

### 2. Extract visual identity when reference images exist

```bash
python .codex/skills/project-explainer-frontend/scripts/extract_visual_identity.py \
  --image path/to/reference.png \
  --site-name "The AEther Flow" \
  --out-dir scratch/project-explainer
```

This step requires Pillow:

```bash
python -m pip install -r .codex/skills/project-explainer-frontend/requirements.txt
```

Exact font identification from raster images is unreliable. Treat this output
as design direction, not a certified font match.

### 3. Generate a site blueprint

```bash
python .codex/skills/project-explainer-frontend/scripts/generate_site_blueprint.py \
  --story scratch/project-explainer/project_story_brief.json \
  --out-dir scratch/project-explainer
```

If a visual identity was generated, also pass:

```bash
--identity scratch/project-explainer/visual_identity.json
```

Read:

- `scratch/project-explainer/site_blueprint.json`
- `scratch/project-explainer/site_blueprint.md`
- `scratch/project-explainer/design_tokens.css`

### 4. Implement with the existing Astro stack

Use this repository's current Astro conventions: pages under `src/pages`,
shared content under `src/lib`, layouts under `src/layouts`, components under
`src/components`, global styles under `src/styles`, and static public assets
under `public`.

Reader-facing pages should include source authority language, claim status, and
source references when they make reviewed, draft, historical, or source-index
claims. Follow the existing validators rather than inventing a new claim model.

### 5. Audit and browser-test

After building:

```bash
npm run build
python .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py \
  --site dist \
  --out-dir scratch/project-explainer \
  --strict
```

Use the Playwright CLI Skill and Playwright Interactive Skill for frontend QA.
Use `127.0.0.1`, not `file://`, and keep browser artifacts under
`output/playwright/`.

## Required Page Contract

An AEther Flow explainer page should answer:

- What is this page explaining?
- What source material supports it?
- What claim status does it have?
- What should a reader trust, and what remains upstream or gated?
- Where should the reader go next?

For research or governance pages, distinguish reviewed results, draft/control
material, proposal-only work, blocked claims, human-gated claims, limitations,
and next obligations.

## Non-Goals

- Do not build a runtime UI for the upstream project unless explicitly asked
  and supported by existing code.
- Do not invent simulations, dashboards, proof validation, metrics, or backend
  integration.
- Do not add production dependencies without approval.
- Do not use placeholder filler or generic marketing claims.
