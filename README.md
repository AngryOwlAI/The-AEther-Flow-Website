# The AEther Flow Website

This repository is the website-development workspace for
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.

The source research repository remains the authority for scientific claims,
research-control state, source documents, registries, validators, and generated
derivative rules. This website repository should present, organize, and publish
reader-facing material without silently changing the underlying research
claims.

## Your Soul

The SOUL.md file is mandatory for all agents to read and understand. It define core aspect of your personality,
the way you think, reason, and act.  It is the most important file in the repository and should be read first by any agent before doing any work in the project.

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
canonical Documents routes, catalog-backed downloads, and Cloudflare Pages
deployment documentation.

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

## Documentation

Maintainer-facing documentation starts at:

```text
docs/README.md
```

The project feature and functionality operating map is:

```text
docs/project-features-and-functionality.md
```

The accepted Documents architecture is indexed by the human-readable plan and
its hash-bound canonical relay artifact:

```text
ImplementationPlans/aether-flow-documents-navigation-implementation-plan.md
ImplementationPlans/aether-flow-documents-navigation-implementation-plan.canonical.json
```

Live records under `implementation_control/` remain the execution authority for
each bounded plan task and any permitted external effect.

These repository documents are for maintainers and implementation agents. They
are not exposed in the public website navigation.

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

The smoke test checks the main public routes, canonical Documents routes,
document downloads, a diagram asset, and `robots.txt`.

## Deployment

The canonical production domain is:

```text
https://the-aether-flow-website.pages.dev/
```

Publish a verified local build to Cloudflare Pages with:

Local implementation and validation do not create a commit, push a revision,
or deploy the site. Treat commit, push, and deployment as separate checkpoints;
run the following command only after deployment is explicitly authorized and
the release revision and push status have been recorded.

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

Within `/documents/`, registered TeX remains the source-authority format for
the ontology collection. PDFs are generated human-readable derivatives, and
rendered pages, catalog rows, manifests, provenance hashes, and validator
results organize or check publication state without becoming scientific claim
authority.

## Git Remote

This repository is connected to the AngryOwlAI GitHub repository using Alex's
Omegapy SSH identity:

```text
git@github-omegapy:AngryOwlAI/The-AEther-Flow-Website.git
```

This keeps the repository owned by `AngryOwlAI` while authenticating pushes
through Alex's GitHub collaborator account.
