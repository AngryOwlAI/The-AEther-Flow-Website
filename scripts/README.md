# Website Tooling

These scripts support the static website repository. They must not modify the
source research repository at `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.

## Commands

- `python scripts/validate_assets.py`: validates source and asset manifests,
  file existence, byte counts, hashes, and source references.
- `python scripts/validate_content_sources.py`: validates MDX/Markdown
  frontmatter claim status and source-reference discipline.
- `python scripts/build_asset_manifest.py`: computes an asset manifest from the
  source manifest. It prints JSON by default and writes only with `--write`.
- `python scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`:
  checks key routes on a running local server.

Shell wrappers live in `scripts/shell/` and resolve the repository root from
their own location.
