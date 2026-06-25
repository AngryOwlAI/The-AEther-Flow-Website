# Phase 7 Quality Gate

Status: local quality gate implemented; external Docker and Cloudflare runtime
verification still require the relevant services.

## Local Gate

Run:

```bash
make quality
```

This expands to:

- Python asset and source-manifest validation.
- Markdown/MDX claim-status validation.
- Cloudflare `_headers` and `_redirects` syntax validation.
- Astro static build.
- Python tests.
- Ruff and mypy.
- Artifact-level quality checks on `dist/`.

The artifact-level gate checks:

- Internal links in built HTML.
- Manifest-backed asset existence.
- Source authority notices on technical and resource pages.
- KaTeX markup on math-heavy pages.
- Absence of rendered source-repository local path leaks.

## Runtime Gate

With preview running, run:

```bash
.venv/bin/python scripts/smoke_test_site.py --base-url http://127.0.0.1:4321
```

## External Gates

The following cannot be completed from this repository without external state:

- Docker build and Docker Compose runtime verification, because Docker is not
  installed in the current environment.
- Cloudflare Pages production deployment from `main`.
- Cloudflare Pages branch preview deployment.
- Cloudflare-applied response header verification, including the `.tex` content
  type from `public/_headers`.
