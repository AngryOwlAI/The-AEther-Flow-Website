# Cloudflare Pages Deployment

Status: configuration-ready; dashboard deployment still requires Cloudflare access.

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

## Dashboard Steps

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

Production and preview deployment verification cannot be completed from this
repository alone. It requires authenticated Cloudflare dashboard or API access
and a pushed Git branch.
