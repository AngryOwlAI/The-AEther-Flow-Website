# The AEther Flow Website

This repository is the website-development workspace for
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.

The source research repository remains the authority for scientific claims,
research-control state, source documents, registries, validators, and generated
derivative rules. This website repository should present, organize, and publish
reader-facing material without silently changing the underlying research
claims.

## Purpose

- Build the public website for The AEther Flow research project.
- Keep website implementation separate from the source research-control repo.
- Preserve a clear boundary between public presentation and source authority.
- Track website code, assets, build configuration, and deployment notes here.

## Current Status

The repository contains the deployed Astro static site for the public AEther
Flow website. It includes MDX, KaTeX, manifest-backed downloads, Python/Bash
validation tooling, Docker development configuration, reader-facing project
overview pages, physics and AI research track pages, source-authority pages,
resource indexes, and Cloudflare Pages deployment documentation.

Production site:

```text
https://the-aether-flow-website.pages.dev/
```

Current deployment mode:

```text
Cloudflare Pages direct upload through Wrangler
```

Cloudflare dashboard Git integration is optional future work. The production
site is currently deployed from local static builds uploaded with authenticated
Wrangler access.

Project-local Codex skills live in:

```text
.codex/skills/
```

The current local skills include `project-explainer-frontend` for
source-boundary-aware website work, `prototype` for throwaway design
exploration, and `to-prd` for local PRD synthesis.

Build and validation entry points:

```bash
make install
make validate
make test
make lint
make quality
```

Cloudflare Pages settings are documented in:

```text
docs/deployment/cloudflare-pages.md
```

## Local Development

Install dependencies and run the local Astro development server:

```bash
make install
npm run dev
```

Build and preview the static site:

```bash
make quality
npm run preview -- --host 127.0.0.1 --port 4321
python scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

The smoke test checks the main public routes, resource downloads, diagram
asset, and `robots.txt`.

## Deployment

The canonical production domain is:

```text
https://the-aether-flow-website.pages.dev/
```

Publish a verified local build to Cloudflare Pages with:

```bash
make quality
npx --yes wrangler@latest pages deploy dist \
  --project-name the-aether-flow-website \
  --branch main \
  --commit-hash "$(git rev-parse HEAD)" \
  --commit-message "$(git log -1 --pretty=%s)" \
  --commit-dirty=false
```

Verify production after deployment:

```bash
python scripts/smoke_test_site.py \
  --base-url https://the-aether-flow-website.pages.dev \
  --timeout 20
```

Inspect the active Cloudflare Pages production deployment:

```bash
npx --yes wrangler@latest pages deployment list \
  --project-name the-aether-flow-website \
  --environment production
```

## Source Authority Boundary

Authoritative project state belongs in the source repository:

```text
/Volumes/P-SSD/AngryOwl/The-AEther-Flow
```

Website content should be derived from reviewed source material, publication
briefs, source specs, or other approved project surfaces. If a website page
needs to make or change a scientific, mathematical, governance, or research
workflow claim, update and validate the source repository first.

## Git Remote

This repository is connected to the AngryOwlAI GitHub repository using Alex's
Omegapy SSH identity:

```text
git@github-omegapy:AngryOwlAI/The-AEther-Flow-Website.git
```

This keeps the repository owned by `AngryOwlAI` while authenticating pushes
through Alex's GitHub collaborator account.
