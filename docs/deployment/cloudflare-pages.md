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

## Git Integration Hardening Attempt

Status: blocked fail-closed on 2026-06-25.

The current project, `the-aether-flow-website`, is a Direct Upload project.
Cloudflare's current Pages documentation states that a Direct Upload project
cannot be switched later to Git integration. Preserving the existing
`the-aether-flow-website.pages.dev` hostname while changing to true Cloudflare
Git integration therefore requires a deliberate replacement operation:

1. Preserve current production evidence.
2. Delete the Direct Upload project.
3. Recreate `the-aether-flow-website` through Cloudflare Pages Git integration.
4. Connect `AngryOwlAI/The-AEther-Flow-Website`.
5. Deploy `main` and rerun production smoke/browser QA.

That replacement was not performed because it is destructive infrastructure
work and the current production site is healthy.

Non-destructive API attempts to create a separate Git-backed Pages project
failed with Cloudflare error `8000011`:

```text
There is an internal issue with your Cloudflare Pages Git installation.
If this issue persists after reinstalling your installation, contact support:
https://cfl.re/3WgEyrH.
```

Observed state:

- Existing Pages project: `the-aether-flow-website`.
- Existing production domain: `the-aether-flow-website.pages.dev`.
- Existing Git provider: `No`.
- Existing deployment trigger: `ad_hoc`.
- Existing production source shown by Wrangler: `0768944`.
- Attempted non-destructive Git-backed project names:
  `the-aether-flow-website-git`,
  `the-aether-flow-website-auto`.
- GitHub repository: `AngryOwlAI/The-AEther-Flow-Website`.
- GitHub token repository permission observed locally: `WRITE`, not
  `ADMIN` or `MAINTAIN`.
- GitHub Actions repository secrets observed locally: none.

Required authorization to continue true Cloudflare Git integration:

```text
Authorize or reinstall the Cloudflare Pages GitHub App for
AngryOwlAI/The-AEther-Flow-Website, then approve either:
1. creating a separate Git-integrated Pages project for verification, or
2. replacing the existing Direct Upload project to preserve the current
   the-aether-flow-website.pages.dev hostname.
```

Safe alternative if project replacement is not desired: keep the Direct Upload
project and use GitHub Actions with `cloudflare/wrangler-action` to deploy on
push. That achieves automatic deployment from GitHub, but it is not Cloudflare
Pages dashboard Git integration and the Wrangler project list will still show
`Git Provider: No`.

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

## References

Cloudflare. (2026a, April 21). *Direct Upload*. Cloudflare Pages Docs.
https://developers.cloudflare.com/pages/get-started/direct-upload/

Cloudflare. (2026b, April 21). *Git integration*. Cloudflare Pages Docs.
https://developers.cloudflare.com/pages/configuration/git-integration/

Cloudflare. (n.d.). *Create project*. Cloudflare API.
https://developers.cloudflare.com/api/resources/pages/subresources/projects/methods/create/
