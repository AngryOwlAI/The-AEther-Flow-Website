# Project Explainer Frontend Skill

Project-local Codex skill for creating evidence-backed informational frontends
for The AEther Flow Website.

This skill is adapted from
`/Users/alex.omegapy/Downloads/project-explainer-frontend-skill` for this
repository's Astro static-site stack and Source Authority Boundary. The local
adaptation changes paths, output defaults, claim-boundary behavior, and
validation expectations.

## Install Notes

The skill itself is tracked inside:

```text
.codex/skills/project-explainer-frontend/
```

Image-based palette extraction is optional and requires Pillow:

```bash
python -m pip install -r .codex/skills/project-explainer-frontend/requirements.txt
```

## Typical Use

```text
Use $project-explainer-frontend to scan this project, inspect the upstream
source root, and generate a source-boundary-aware blueprint for a new Astro
explainer page.
```

## Script Pipeline

```bash
python .codex/skills/project-explainer-frontend/scripts/scan_project_story.py \
  --repo . \
  --source-root /Volumes/P-SSD/AngryOwl/The-AEther-Flow \
  --out-dir scratch/project-explainer

python .codex/skills/project-explainer-frontend/scripts/generate_site_blueprint.py \
  --story scratch/project-explainer/project_story_brief.json \
  --out-dir scratch/project-explainer

python .codex/skills/project-explainer-frontend/scripts/audit_project_frontend.py \
  --site dist \
  --out-dir scratch/project-explainer \
  --strict
```

Optional image identity extraction:

```bash
python .codex/skills/project-explainer-frontend/scripts/extract_visual_identity.py \
  --image reference.png \
  --site-name "The AEther Flow" \
  --out-dir scratch/project-explainer
```

## Outputs

- `scratch/project-explainer/project_story_brief.json`
- `scratch/project-explainer/project_story_brief.md`
- `scratch/project-explainer/visual_identity.json`
- `scratch/project-explainer/visual_identity.md`
- `scratch/project-explainer/site_blueprint.json`
- `scratch/project-explainer/site_blueprint.md`
- `scratch/project-explainer/design_tokens.css`
- `scratch/project-explainer/frontend_audit.json`
- `scratch/project-explainer/frontend_audit.md`

## Attribution

This project-local skill is adapted from a downloaded
`project-explainer-frontend-skill` bundle. No third-party license text was found
in that bundle during integration, so this README records provenance without
changing the repository's third-party notices.
