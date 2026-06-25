# AEther Flow Website Implementation Plan

Status: draft implementation plan
Date: 2026-06-25
Repository: The-AEther-Flow-Website
Primary recommendation: Astro static site deployed to Cloudflare Pages, with Python and Bash tooling for source ingestion, asset validation, and agent-skill support. Docker is included as an optional reproducible development and build environment, not as the primary production runtime.

## 1. Analysis

The current website repository is intentionally separate from the source research repository. The repository README states that the source research repository remains authoritative for scientific claims, research-control state, source documents, registries, validators, and derivative rules. Therefore, the website should publish reviewed, reader-facing material without becoming an alternate source of truth.

The site requirements are content-oriented:

- Explain and promote The AEther Flow project.
- Render mathematical and physics equations clearly in web pages.
- Publish images, diagrams, and selected project visuals.
- Provide direct website access to `.pdf` and `.tex` files without routing readers through GitHub.
- Avoid a complex backend unless a future feature justifies one.
- Support local Python and Bash scripts for automation, agent skills, content ingestion, validation, and build helpers.
- Allow Docker where it improves reproducibility, especially around Node, Python, TeX-adjacent tooling, or cross-machine consistency.

Conclusion: this project should start as a static content-first website. A backend is not justified by the present requirements. Docker is useful for development parity and reproducible builds, but production deployment should serve the generated static files.

## 2. Goals

1. Build a public, content-rich explanatory website for The AEther Flow.
2. Preserve the source-authority boundary between website presentation and the research-control repository.
3. Provide first-class support for equations, technical writing, diagrams, PDFs, and `.tex` files.
4. Use a small, maintainable frontend stack.
5. Support Python and Bash tooling without mixing tool state into the published site.
6. Make local development reproducible on macOS and portable to other machines.
7. Deploy static output through a platform suited to public static assets.
8. Keep future expansion possible without prematurely adding a backend.

## 3. Non-Goals

1. Do not build a database-backed application in the first implementation phase.
2. Do not create a private CMS before the content model is proven.
3. Do not make the website repository authoritative for scientific claims.
4. Do not silently rewrite source-repo claims during website content generation.
5. Do not require Docker for ordinary content edits unless a contributor chooses that path.
6. Do not ignore or hide future Codex skill directories in Git.
7. Do not store large generated caches or local virtual environments in the repository.

## 4. Recommended Architecture

### 4.1 Frontend Framework

Use Astro.

Reasoning:

- Astro is designed for content-heavy sites.
- It can generate static HTML by default.
- It supports Markdown and MDX for structured technical pages.
- It ships little or no client-side JavaScript unless interactive components require it.
- It can organize technical content using content collections.
- It can publish static assets directly from `public/`.

### 4.2 Deployment Target

Use Cloudflare Pages as the first production deployment target.

Reasoning:

- The site is primarily static.
- Cloudflare Pages supports continuous deployment from Git.
- Cloudflare's static asset model fits PDFs, `.tex` files, images, diagrams, CSS, and generated HTML.
- Cloudflare Pages currently advertises unlimited static requests and bandwidth on its public product page.
- Cloudflare gives a simple path to custom domains, caching, redirects, headers, and future edge functions if needed.

Secondary options:

- Vercel: strong developer experience and also suitable for Astro static output.
- Netlify: also suitable, especially if future form handling or Netlify-specific workflows become useful.
- GitHub Pages: acceptable for a prototype or mirror, but less preferred for this site because it has stricter documented size, bandwidth, and build constraints.

### 4.3 Runtime Model

Production should serve static output from `dist/`.

No always-on Node server, Python server, or Docker container is required for the public site at launch.

Use Docker for:

- Local reproducible development.
- CI-like build verification.
- Running Python tooling in a stable environment.
- Avoiding host-machine dependency drift.

Do not deploy Docker as the public runtime unless a future backend feature requires server-side execution.

## 5. Proposed Repository Structure

```text
The-AEther-Flow-Website/
  .gitignore
  README.md
  package.json
  package-lock.json
  astro.config.mjs
  tsconfig.json
  Dockerfile
  docker-compose.yml
  .dockerignore
  requirements.txt
  requirements-dev.txt
  Makefile
  ImplementationPlans/
    aether_flow_website_static_astro_cloudflare_docker_plan.md
  src/
    content/
      pages/
      research/
      references/
      releases/
    components/
      EquationBlock.astro
      DownloadList.astro
      SourceNotice.astro
      Figure.astro
      Diagram.astro
    layouts/
      BaseLayout.astro
      TechnicalPageLayout.astro
      LandingLayout.astro
    pages/
      index.astro
      research/
      resources/
      files/
    styles/
      global.css
      math.css
    lib/
      content.ts
      sources.ts
  public/
    assets/
      images/
      diagrams/
      generated/
    files/
      pdf/
      tex/
      manifests/
    favicon.svg
    robots.txt
  scripts/
    README.md
    sync_sources.py
    build_asset_manifest.py
    validate_assets.py
    validate_content_sources.py
    generate_diagram_index.py
    smoke_test_site.py
    shell/
      dev.sh
      build.sh
      validate.sh
      docker-build.sh
  tests/
    fixtures/
    test_asset_manifest.py
    test_content_sources.py
```

This structure separates:

- Website source code: `src/`
- Public downloadable assets: `public/`
- Automation tooling: `scripts/`
- Python tests: `tests/`
- Planning artifacts: `ImplementationPlans/`
- Local generated state: ignored by `.gitignore`

## 6. Source Authority Model

### 6.1 Authority Rule

The source research repository remains authoritative.

The website repository may contain:

- Reader-facing summaries.
- Approved publication briefs.
- Copied or exported PDFs.
- Copied or exported `.tex` files.
- Diagrams derived from reviewed source material.
- A website-local manifest describing where each public asset came from.

The website repository must not become the place where scientific claims are invented or altered.

### 6.2 Source Manifest

Create a manifest at:

```text
public/files/manifests/source_manifest.json
```

Recommended schema:

```json
{
  "version": 1,
  "generated_at": "2026-06-25T00:00:00-06:00",
  "source_repository": "/Volumes/P-SSD/AngryOwl/The-AEther-Flow",
  "items": [
    {
      "site_path": "/files/pdf/example.pdf",
      "kind": "pdf",
      "title": "Example PDF",
      "source_path": "relative/path/in/source/repo/example.pdf",
      "source_commit": "commit-hash-if-known",
      "approval_status": "approved",
      "notes": "Reader-facing public asset."
    }
  ]
}
```

Minimum required fields:

- `site_path`
- `kind`
- `title`
- `source_path`
- `approval_status`

Recommended optional fields:

- `source_commit`
- `sha256`
- `generated_by`
- `generated_at`
- `reviewed_by`
- `license_or_usage_note`

### 6.3 Claim Discipline

Every technical page should include one of these statuses in frontmatter:

```yaml
claim_status: reviewed
claim_status: explanatory
claim_status: draft
claim_status: historical
claim_status: source-index-only
```

Rules:

- `reviewed`: derived from approved source material.
- `explanatory`: high-level website explanation that does not extend the science.
- `draft`: visible only if intentionally published with a draft notice.
- `historical`: preserves a prior state or archived explanation.
- `source-index-only`: lists files or resources without asserting new scientific claims.

## 7. Astro Implementation Plan

### Phase 1: Scaffold Astro

Commands:

```bash
npm create astro@latest .
npm install
```

Recommended selections:

- Template: minimal or empty.
- TypeScript: yes.
- Install dependencies: yes.
- Initialize Git: no, because the repository already exists.

Expected files:

- `package.json`
- `package-lock.json`
- `astro.config.mjs`
- `tsconfig.json`
- `src/`
- `public/`

Acceptance criteria:

- `npm run dev` starts the local site.
- `npm run build` generates `dist/`.
- `npm run preview` serves the built site.
- No source-repo claims are added during scaffolding.

### Phase 2: Configure Core Site Shell

Create:

- `src/layouts/BaseLayout.astro`
- `src/layouts/LandingLayout.astro`
- `src/layouts/TechnicalPageLayout.astro`
- `src/styles/global.css`
- `src/pages/index.astro`
- `src/pages/resources/index.astro`

Core layout responsibilities:

- Page metadata.
- Canonical URL placeholders.
- Site navigation.
- Footer with source-authority notice.
- Responsive layout.
- Math stylesheet import.
- Accessible color contrast.
- Clean typography for equations and technical prose.

Acceptance criteria:

- Home page loads.
- Resources page loads.
- Navigation works without client-side routing.
- Layout is usable on desktop and mobile.

### Phase 3: Configure MDX and Content Collections

Install:

```bash
npm install @astrojs/mdx
```

Add MDX integration:

```bash
npx astro add mdx
```

Create content collections:

```text
src/content/research/
src/content/references/
src/content/releases/
```

Recommended content frontmatter:

```yaml
title: "Page Title"
description: "Short reader-facing description."
claim_status: explanatory
source_refs:
  - "source_manifest:item-id"
updated: 2026-06-25
```

Acceptance criteria:

- Content entries validate at build time.
- Pages can render from collection data.
- Missing required metadata fails the build.

## 8. Equation Rendering Plan

### 8.1 Primary Math Renderer

Use KaTeX first.

Reasoning:

- Fast rendering.
- Good static-site fit.
- Strong support for common TeX math syntax.
- Works well through Markdown/MDX build-time processing with `remark-math` and `rehype-katex`.

Install:

```bash
npm install remark-math rehype-katex katex
```

Configure `astro.config.mjs`:

```js
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  integrations: [mdx()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
});
```

Import KaTeX CSS globally:

```css
@import "katex/dist/katex.min.css";
```

Supported authoring pattern:

```md
Inline math: $E = mc^2$

Display math:

$$
G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}
$$
```

### 8.2 MathJax Fallback

Add MathJax only if the project uses TeX features unsupported by KaTeX.

Trigger conditions:

- KaTeX cannot render required source equations.
- Accessibility needs require MathJax features such as advanced expression exploration.
- The site needs dynamic equation rendering after client-side interaction.

Implementation rule:

- Do not ship both KaTeX and MathJax globally by default.
- Prefer one renderer per page class.
- Document any MathJax-only pages in the implementation notes.

### 8.3 Equation Quality Checks

Create `scripts/validate_math_content.py` later if needed.

Checks:

- Detect unmatched `$`, `$$`, `\(`, `\)`, `\[`, `\]`.
- Identify unsupported macros.
- Render sample pages in CI.
- Run Playwright or Astro preview smoke tests for math-heavy pages.

Acceptance criteria:

- Representative equations render in local dev.
- Production build does not fail on math syntax.
- Math pages remain readable with CSS disabled.
- Equation overflow is handled on mobile.

## 9. PDFs, `.tex`, Images, and Diagrams

### 9.1 Public Asset Paths

Use:

```text
public/files/pdf/
public/files/tex/
public/assets/images/
public/assets/diagrams/
```

Example public URLs:

```text
/files/pdf/example.pdf
/files/tex/example.tex
/assets/images/example.png
/assets/diagrams/example.svg
```

### 9.2 File Access Policy

Readers should access project files directly from the website.

Rules:

- Do not link primarily to GitHub for core reader-facing PDFs and `.tex` files.
- Do include source provenance in the page or manifest.
- Do not modify `.tex` files in the website repository unless the source-authority process permits it.
- Track published `.pdf` and `.tex` files in Git unless they become too large for ordinary repository use.

### 9.3 Asset Manifest

Generate an asset manifest:

```text
public/files/manifests/asset_manifest.json
```

Recommended fields:

```json
{
  "path": "/files/pdf/example.pdf",
  "kind": "pdf",
  "bytes": 123456,
  "sha256": "hash",
  "title": "Example",
  "source_ref": "source_manifest:item-id"
}
```

### 9.4 Diagrams

Use a layered approach:

1. Static SVG or PNG for stable conceptual diagrams.
2. Mermaid for diagrams that should remain text-editable.
3. Generated images only when visual polish or narrative clarity requires it.
4. Avoid making diagrams authoritative unless they are derived from reviewed source artifacts.

Recommended locations:

```text
src/content/references/diagrams/
public/assets/diagrams/
scripts/generate_diagram_index.py
```

Acceptance criteria:

- PDFs and `.tex` files open from website URLs.
- Asset lists are generated from the manifest, not manually duplicated everywhere.
- Large images are compressed.
- Alt text exists for meaningful images and diagrams.

## 10. Python Tooling Plan

### 10.1 Virtual Environment

Use a local `.venv`.

Commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

The `.venv/` directory must be ignored by Git.

### 10.2 Dependency Files

Create:

```text
requirements.txt
requirements-dev.txt
```

Initial `requirements.txt` candidates:

```text
pyyaml
python-frontmatter
rich
```

Initial `requirements-dev.txt` candidates:

```text
-r requirements.txt
pytest
ruff
mypy
types-PyYAML
```

Add PDF or image dependencies only when a script requires them:

- `pymupdf` for PDF inspection.
- `pillow` for image checks.
- `beautifulsoup4` for HTML validation helpers.

### 10.3 Script Responsibilities

Recommended scripts:

```text
scripts/sync_sources.py
```

Copies approved assets from the source repository into website public folders. It should use explicit allowlists or manifest entries, not broad recursive copying.

```text
scripts/build_asset_manifest.py
```

Computes file size, hash, kind, title, and public path for published files.

```text
scripts/validate_assets.py
```

Checks that every listed asset exists, is below size thresholds, and has source provenance.

```text
scripts/validate_content_sources.py
```

Checks MDX frontmatter for source references and claim status.

```text
scripts/generate_diagram_index.py
```

Builds a diagram index page or data file from diagram metadata.

```text
scripts/smoke_test_site.py
```

Fetches local preview pages and confirms important URLs return expected status codes.

### 10.4 Python Quality Standards

Use:

```bash
python -m pytest
python -m ruff check .
python -m mypy scripts tests
```

Initial rules:

- Scripts should be deterministic.
- Scripts should default to dry-run where they copy or overwrite assets.
- Scripts should fail closed when source provenance is missing.
- Scripts should produce clear logs and nonzero exit codes on validation failure.
- Scripts should not modify the source research repository.

## 11. Bash and Makefile Plan

Use Bash wrappers for common operations and a `Makefile` as the command index.

Recommended `Makefile` targets:

```makefile
.PHONY: install dev build preview test lint validate clean docker-build docker-dev

install:
	npm install
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	. .venv/bin/activate && python -m pip install -r requirements-dev.txt

dev:
	npm run dev

build:
	npm run build

preview:
	npm run preview

test:
	. .venv/bin/activate && python -m pytest

lint:
	npm run astro check
	. .venv/bin/activate && python -m ruff check .

validate:
	. .venv/bin/activate && python scripts/validate_assets.py
	. .venv/bin/activate && python scripts/validate_content_sources.py
	npm run build

clean:
	rm -rf dist .astro .pytest_cache .mypy_cache .ruff_cache htmlcov

docker-build:
	docker build -t aether-flow-website:local .

docker-dev:
	docker compose up --build
```

Bash scripts should live under:

```text
scripts/shell/
```

Rules:

- Use `set -euo pipefail`.
- Resolve repository root from script location.
- Print the command purpose before running destructive or expensive steps.
- Do not hide validation failures.

## 12. Docker Plan

### 12.1 Docker Role

Docker is included for reproducible development and build verification.

It is not the primary production runtime unless future requirements change.

### 12.2 Dockerfile Strategy

Use a multi-stage Dockerfile:

1. `base`: Node plus Python.
2. `deps`: install Node dependencies and Python dependencies.
3. `build`: run validation and `npm run build`.
4. `runtime`: serve `dist/` using a small static server image for local testing only.

Example shape:

```Dockerfile
# syntax=docker/dockerfile:1

FROM node:22-bookworm-slim AS base
WORKDIR /app
RUN apt-get update \
  && apt-get install -y --no-install-recommends python3 python3-venv python3-pip \
  && rm -rf /var/lib/apt/lists/*

FROM base AS deps
COPY package*.json ./
RUN npm ci
COPY requirements*.txt ./
RUN python3 -m venv .venv \
  && . .venv/bin/activate \
  && python -m pip install --upgrade pip \
  && python -m pip install -r requirements-dev.txt

FROM deps AS build
COPY . .
RUN . .venv/bin/activate && python -m pytest || true
RUN npm run build

FROM nginx:alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
```

Important: remove `|| true` once tests exist and should be enforced. It is shown only for a very early scaffold where tests may not exist yet.

### 12.3 docker-compose.yml

Use Compose for local development:

```yaml
services:
  web:
    build:
      context: .
      target: base
    working_dir: /app
    command: sh -c "npm install && npm run dev -- --host 0.0.0.0"
    ports:
      - "4321:4321"
    volumes:
      - .:/app
      - node_modules:/app/node_modules

volumes:
  node_modules:
```

Add Python tooling only after requirements files exist.

### 12.4 .dockerignore

Create `.dockerignore` to avoid copying local-only state into Docker builds:

```text
.git
.venv
node_modules
dist
.astro
.pytest_cache
.mypy_cache
.ruff_cache
.DS_Store
```

Do not ignore source files needed for build.

### 12.5 Docker Acceptance Criteria

- `docker build -t aether-flow-website:local .` succeeds.
- `docker compose up --build` serves the dev site on port `4321`.
- Docker build does not copy `.venv`, `node_modules`, `.git`, or macOS metadata.
- Production deployment still uses static hosting, not a long-running app container.

## 13. Deployment Plan

### 13.1 Cloudflare Pages Setup

Deployment settings:

```text
Framework preset: Astro
Build command: npm run build
Build output directory: dist
Root directory: /
Node version: pin through package manager or Cloudflare setting
```

Recommended environment variables:

```text
NODE_VERSION=22
```

Only add secrets if a future build step needs authenticated source access.

### 13.2 Branch Model

Recommended:

- `main`: production.
- Feature branches: preview deployments.
- Pull request previews: enabled.

### 13.3 Headers and Redirects

Use Cloudflare Pages conventions:

```text
public/_headers
public/_redirects
```

Recommended headers:

```text
/assets/*
  Cache-Control: public, max-age=31536000, immutable

/files/*
  Cache-Control: public, max-age=86400

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

Be careful with long immutable caching for PDFs and `.tex` files. If file contents may change under the same path, use shorter caching or versioned filenames.

### 13.4 Custom Domain

Steps:

1. Add the site to Cloudflare Pages.
2. Connect GitHub repository.
3. Confirm build settings.
4. Deploy preview.
5. Add custom domain.
6. Verify HTTPS.
7. Add canonical URL in Astro config.

### 13.5 Rollback

Rollback approach:

- Use Cloudflare Pages deployment history for immediate rollback.
- Use Git tags for stable release points.
- Version published PDFs or `.tex` files if content changes materially.

## 14. Testing and Verification

### 14.1 Local Checks

Run:

```bash
npm run build
npm run preview
python -m pytest
python scripts/validate_assets.py
python scripts/validate_content_sources.py
```

### 14.2 Static Site Checks

Verify:

- Home page returns 200.
- Resource index returns 200.
- PDF URLs return 200.
- `.tex` URLs return 200.
- Math-heavy pages render equations.
- Mobile viewport does not overflow horizontally.
- Large images are compressed and sized appropriately.

### 14.3 Content Checks

Verify:

- Every technical page has `claim_status`.
- Every source-derived page has `source_refs`.
- Every public PDF and `.tex` file appears in the asset manifest.
- Every manifest item has source provenance.
- No website page claims research conclusions beyond approved source material.

### 14.4 Security Checks

Verify:

- No `.env` files are committed.
- No source-repo private notes are copied into `public/`.
- No build cache is published.
- No generated local path leaks into rendered pages.
- File downloads have expected MIME behavior.
- External links use clear labels.

## 15. Accessibility and Reader Experience

Requirements:

- Use semantic HTML.
- Maintain sufficient contrast.
- Give diagrams useful alt text or captions.
- Ensure keyboard navigation works.
- Avoid hiding core content behind JavaScript.
- Ensure equations do not break mobile layout.
- Provide readable captions for technical figures.
- Provide direct download links for PDFs and `.tex` files.

Recommended components:

- `SourceNotice.astro`: explains source authority and last-reviewed date.
- `DownloadList.astro`: renders PDF and `.tex` downloads from manifest data.
- `EquationBlock.astro`: wraps display equations with overflow handling.
- `Figure.astro`: standardizes images, captions, and provenance.

## 16. Performance Plan

Performance practices:

- Prefer static HTML.
- Use optimized images.
- Avoid global JavaScript unless required.
- Use Astro islands only for genuinely interactive components.
- Use versioned asset paths for long-cache assets.
- Keep PDF files compressed where feasible.
- Avoid loading MathJax globally unless required.

Targets:

- Good Lighthouse score for static pages.
- No avoidable layout shift.
- No unnecessary JavaScript on purely textual pages.
- Math pages remain responsive.

## 17. Content Roadmap

Initial pages:

1. Home
2. Project overview
3. Research map
4. Mathematical foundations
5. Physics context
6. Source documents
7. Diagrams
8. Publications or drafts
9. FAQ
10. Contact or project links

Initial resource pages:

1. PDF library
2. TeX source library
3. Diagram gallery
4. Glossary
5. Source authority note

## 18. Implementation Phases

### Phase 0: Repository Hygiene

Tasks:

- Add `.gitignore`.
- Add this implementation plan.
- Confirm `README.md` source-authority boundary.
- Confirm remote and branch state.

Acceptance criteria:

- `ImplementationPlans/` is tracked.
- `.gitignore` does not ignore Codex skill directories.
- Working tree only contains intentional changes.

### Phase 1: Astro Scaffold

Tasks:

- Scaffold Astro.
- Install dependencies.
- Add MDX integration.
- Add KaTeX integration.
- Add base layouts.
- Add global styles.

Acceptance criteria:

- `npm run build` succeeds.
- Home page renders.
- Sample math page renders.

### Phase 2: Asset and Source Manifests

Tasks:

- Create public asset directories.
- Define source manifest schema.
- Add sample manifest.
- Add Python script to validate manifest paths.
- Add DownloadList component.

Acceptance criteria:

- PDF and `.tex` sample files can be linked from the site.
- Manifest validation fails if files are missing.
- Resource page renders from manifest data.

### Phase 3: Python and Bash Tooling

Tasks:

- Add `.venv` workflow.
- Add requirements files.
- Add validation scripts.
- Add shell wrappers.
- Add Makefile.

Acceptance criteria:

- `make install` prepares Node and Python dependencies.
- `make validate` runs Python checks and Astro build.
- Scripts do not modify source research repo.

### Phase 4: Docker Development Environment

Tasks:

- Add Dockerfile.
- Add docker-compose.yml.
- Add `.dockerignore`.
- Add Docker Makefile targets.

Acceptance criteria:

- Docker build succeeds.
- Docker Compose serves local dev site.
- Docker context excludes local caches.

### Phase 5: Content Buildout

Tasks:

- Add project overview page.
- Add research map page.
- Add source document library.
- Add diagram gallery.
- Add equation-heavy technical sample page.
- Add source-authority notices.

Acceptance criteria:

- Pages render from structured content where practical.
- Technical pages include claim status.
- Download pages use manifest data.

### Phase 6: Cloudflare Pages Deployment

Tasks:

- Connect GitHub repository to Cloudflare Pages.
- Configure build command and output directory.
- Add custom domain if available.
- Add `_headers` and `_redirects`.
- Verify production and preview deploys.

Acceptance criteria:

- Production site deploys from `main`.
- Preview deploys work for branches.
- Public PDFs and `.tex` files are accessible from site URLs.
- Build logs are clean.

### Phase 7: Quality Gate

Tasks:

- Run local build.
- Run Docker build.
- Run Python validation.
- Check key pages on desktop and mobile.
- Check download links.
- Check source manifest.

Acceptance criteria:

- No broken internal links.
- No missing asset manifest entries.
- No known equation rendering failures.
- No source-authority violations.

## 19. Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Website text drifts from source research authority | High | Require source refs and claim status for technical pages |
| KaTeX cannot render all equations | Medium | Keep MathJax fallback available for specific pages |
| PDFs grow too large for Git | Medium | Compress PDFs, version large assets, consider release assets or object storage later |
| Docker adds complexity | Medium | Make Docker optional for development, not mandatory for routine edits |
| Asset copying leaks private or draft source files | High | Use explicit allowlists and fail-closed validation |
| Cloudflare build environment differs from local macOS | Medium | Pin Node version and provide Docker build path |
| Equations overflow on mobile | Medium | Add math overflow CSS and viewport checks |
| Future backend need appears | Low to Medium | Astro can add server/edge rendering later without changing initial content model |

## 20. Decision Points

### 20.1 KaTeX or MathJax

Default decision: KaTeX.

Switch or supplement with MathJax only if required by equation coverage or accessibility needs.

### 20.2 Track PDFs in Git or External Storage

Default decision: track PDFs in Git while the set is small.

Reassess if:

- Repository size approaches platform limits.
- Individual files become very large.
- Update frequency becomes high.
- Public traffic to large PDFs becomes substantial.

### 20.3 Docker in Production

Default decision: no production Docker runtime.

Reassess if:

- A backend is added.
- Server-side rendering becomes necessary.
- Authentication, search indexing, dynamic forms, or API routes become required.

### 20.4 CMS

Default decision: no CMS.

Reassess if:

- Non-technical editors need browser-based publishing.
- Content volume becomes too large for MDX.
- Approval workflow needs structured review UI.

## 21. Acceptance Criteria for the Overall Recommendation

The recommendation is implemented when:

1. Astro site builds static output into `dist/`.
2. Equations render correctly in representative pages.
3. PDFs and `.tex` files are accessible through website URLs.
4. Public assets have manifest entries and source provenance.
5. Python scripts run inside `.venv`.
6. Bash or Makefile commands cover install, build, validate, and preview.
7. Docker can reproduce a build or local dev environment.
8. Cloudflare Pages deploys from Git.
9. The website contains source-authority notices for technical material.
10. `.gitignore` excludes local/generated artifacts without hiding source assets or Codex skills.

## 22. Logical Next Step

The logical next step is Phase 1: scaffold Astro, install MDX and KaTeX support, and create one minimal technical page that renders both inline and display equations.

After that, implement Phase 2 so public PDFs and `.tex` files are handled through a manifest rather than ad hoc links.

## 23. Can It Be Improved?

Yes. A stronger version of this plan would add a source-provenance gate that compares the website manifest against validated source-repo publication records before deployment. That would make the public website not merely static and fast, but also structurally aligned with the research-control system.

A different perspective is to treat the website as a controlled publication layer rather than a marketing site. That model keeps promotion, explanation, and technical rigor compatible: every public-facing simplification can remain connected to an approved source object.

## References

Astro. (n.d.). Content collections. Astro Docs. Retrieved June 25, 2026, from https://docs.astro.build/en/guides/content-collections/

Astro. (n.d.). Deploy your Astro site. Astro Docs. Retrieved June 25, 2026, from https://docs.astro.build/en/guides/deploy/

Cloudflare. (2026). Cloudflare Pages. https://pages.cloudflare.com/

Docker. (n.d.). Building best practices. Docker Docs. Retrieved June 25, 2026, from https://docs.docker.com/build/building/best-practices/

Docker. (n.d.). Multi-stage builds. Docker Docs. Retrieved June 25, 2026, from https://docs.docker.com/build/building/multi-stage/

GitHub. (2026). GitHub Pages limits. GitHub Docs. https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

KaTeX. (n.d.). Auto-render extension. Retrieved June 25, 2026, from https://katex.org/docs/autorender.html

MathJax. (n.d.). MathJax documentation. Retrieved June 25, 2026, from https://docs.mathjax.org/

Python Software Foundation. (2026). Virtual environments and packages. Python 3.14.6 documentation. https://docs.python.org/3/tutorial/venv.html

The AEther Flow Website. (2026). README.md [Repository file].
