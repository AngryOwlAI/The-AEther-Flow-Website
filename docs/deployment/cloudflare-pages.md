# Cloudflare Pages Deployment

Status: production deployed through Cloudflare Pages direct upload.

Production URL:

```text
https://the-aether-flow-website.pages.dev/
```

Production configuration:

```text
project: the-aether-flow-website
branch: main
git provider: No
```

Note: the project is deployed with Wrangler Pages direct upload. Cloudflare
dashboard Git integration remains optional future work.

Inspect the current production deployment id and source with:

```bash
npx --yes wrangler@latest pages deployment list \
  --project-name the-aether-flow-website \
  --environment production
```

## Build Settings

- Framework preset: Astro
- Build command: `npm run build`
- Build output directory: `dist`
- Root directory: `/`
- Node version: `22`
- Production branch: `main`

The repository pins Node with `.nvmrc` and `package.json` `engines.node`.

## Static Deployment Files

Cloudflare Pages reads the following files after Astro copies them from
`public/` into `dist/`:

- `public/_headers`
- `public/_redirects`

The header rules keep immutable caching on hashed Astro and diagram assets,
shorter caching on public files, a TeX content type for `.tex` downloads, and
basic security headers on all routes.

## Direct Upload Deployment

Use this path when Wrangler is authenticated and a local static build should be
published directly to Cloudflare Pages:

```bash
make quality
npx --yes wrangler@latest pages deploy dist \
  --project-name the-aether-flow-website \
  --branch main \
  --commit-hash "$(git rev-parse HEAD)" \
  --commit-message "$(git log -1 --pretty=%s)" \
  --commit-dirty=false
```

Verify the canonical production domain:

```bash
python scripts/smoke_test_site.py \
  --base-url https://the-aether-flow-website.pages.dev \
  --timeout 20
```

## Optional Dashboard Git Integration

1. Open Cloudflare Workers & Pages.
2. Create a Pages project connected to
   `git@github-omegapy:AngryOwlAI/The-AEther-Flow-Website.git`.
3. Use the build settings above.
4. Deploy the `main` branch.
5. Verify the production deployment.
6. Enable branch preview deployments.
7. Add a custom domain if available.
8. Verify HTTPS and direct access to:
   - `/`
   - `/resources/`
   - `/files/pdf/aether-flow-sample.pdf`
   - `/files/tex/aether-flow-sample.tex`
   - `/assets/diagrams/publication-layer-map.svg`

## Verification Commands

Before connecting or after a failed deployment, run:

```bash
make validate
make test
make lint
```

If a local preview is running:

```bash
.venv/bin/python scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

## External Constraints

Direct upload deployment requires an authenticated Wrangler session with Pages
write access. Dashboard Git integration requires Cloudflare dashboard access and
the Cloudflare GitHub app connection for this private repository.
