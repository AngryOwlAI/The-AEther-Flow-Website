# FE-P0-01R Source Refresh And Manifest-Authority Repair

Date: 2026-07-12  
Packet: `FE-P0-01R`  
Task: `WI-20260712-001`  
Job: `WJ-20260712-001-A`  
Disposition: `source_refresh_and_manifest_authority_gate_cleared`

## 1. Scope and authority boundary

This packet repaired website-local publication metadata identified by the
`FE-P0-01` preflight. It did not open `FE-P0-02`, expand the Home or Physics
source bundles, alter source notices, change a public scientific statement,
grant physics review, write upstream, push, or deploy.

The upstream project remained read-only. Registered upstream TeX sources and
the TeX/PDF registries remain authoritative; this website record is only
implementation and verification evidence.

## 2. Pinned source state

| Field | Verified value | Result |
| --- | --- | --- |
| Upstream branch | `main` | Pass |
| Upstream commit | `a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0` | Pass |
| Remote parity | `origin/main` at the same commit | Pass |
| Worktree | Clean | Pass |
| Website checkpoint basis | `ed64e566292065dbb3ad537eebea348d99ae51dd` | Pass |

All eight published ontology TeX files and all eight PDF derivatives were
byte-identical to the corresponding upstream files before and after the
website-local refresh. Git therefore records no TeX or PDF asset-byte change.

## 3. Repair

### 3.1 Registry-specific importer authority

`scripts/import_ontology_assets.py` now reads:

- TeX authority and claim fields from `registries/TEX_SOURCE_REGISTRY.csv`;
- PDF authority from `registries/PDF_DERIVATIVE_REGISTRY.csv`.

The importer fails closed if a required registry or asset row is missing or if
`authority_status` is absent. A focused regression test proves that the same
package can retain canonical TeX authority while its PDF remains a generated,
noncanonical derivative.

### 3.2 Source and asset manifests

The existing 16-item ontology publication package was refreshed through the
repaired importer. The result is:

| Item class | Count | Authority status | Source commit |
| --- | ---: | --- | --- |
| Registered TeX | 8 | `canonical` | `a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0` |
| PDF derivative | 8 | `generated_noncanonical` | `a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0` |

The source manifest contains 54 total items and has SHA-256
`3e7cbceb7d380db596e60f77bea5b9a1532caff9801cbb373b7cc3a0cce3f0ab`.
The asset manifest also contains 54 items and has SHA-256
`d9ec52eabe097c97c2802c0707c87b4ac9e801541d1e3f6d6922c7e35933060f`.
Asset paths, byte counts, content hashes, titles, and source references are
unchanged; only the shared generation timestamp changed in the asset manifest.

### 3.3 Page provenance

`scripts/generate_page_provenance.py` regenerated all 34 route records from the
unchanged route map. The manifest now pins the clean upstream commit
`a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0` and has SHA-256
`9732d58da2c0ab4f1930a67cf476e9d7d860f6cfc3e5bfec323828ac3b67a993`.

The Physics route now records the current claim-boundary registry hash
`ce67a8f2060074c61d2bf4b613ef056c3891547c5f16ba230e6673a2acb30519`.
Home and Physics both remain `generated_noncanonical` curated syntheses. No
route classification, publication status, or boundary type changed.

## 4. Disposition of FE-P0-01 findings

| Finding | Disposition |
| --- | --- |
| PDF manifest incorrectly said `canonical` | Repaired to `generated_noncanonical` from the PDF registry |
| Ontology manifest pins were stale | Re-pinned to `a8c0b3f4…` |
| Page provenance pin and Physics claim-boundary hash were stale | Regenerated and current |
| Home and Physics omit exact-closure sources | Intentionally unchanged; remains `FE-P0-03` and `FE-P0-04` work |
| Home and Physics source notices omit exact-closure sources | Intentionally unchanged; remains `FE-P0-03` and `FE-P0-04` work |
| Independent physics reviewer and `AG-01` receipt are absent | Unchanged; public claim work remains blocked |

The website-local source-refresh and manifest-authority gate identified by
`FE-P0-01` is cleared. This conclusion does not clear the independent
Home/Physics source-bundle work or the physics-review gate.

## 5. Verification

| Check | Result |
| --- | --- |
| Focused importer regression | 2 passed |
| Full Python suite | 84 passed |
| Manifest validation | Passed |
| Page provenance validation | Passed for 34 routes |
| Static Astro build | 64 pages built |
| Implementation-control validation | Passed |
| `git diff --check` | Passed |
| TeX/PDF byte comparison | All 16 website files match upstream; no Git asset-byte diff |

Aggregate `npm run validate` passed manifest, content-source, internal-link,
layout-language, SVG-policy, and page-provenance checks, then stopped at the
pre-existing stale checked-in curator reports. The exact reported paths were
`curator/reports/latest.json` and `curator/reports/latest.md`. Curator report
regeneration was outside this packet's allowed writes.

## 6. Conclusion

`FE-P0-01R` repaired source freshness and manifest authority without changing
physics, source bytes, routes, runtime copy, or public claims. `FE-P0-02`
remained unopened throughout this packet. After a clean local checkpoint, it
may be separately authorized; it is not executed by this record.

No source-project write, physics promotion, physics delta, Git push, or
deployment occurred.

## References

The Æther Flow Project. (2026a). *PDF derivative registry* [CSV registry].
`registries/PDF_DERIVATIVE_REGISTRY.csv`.

The Æther Flow Project. (2026b). *TeX source registry* [CSV registry].
`registries/TEX_SOURCE_REGISTRY.csv`.

The Æther Flow Website. (2026a). *FE-P0-01 authoritative exact-closure source
preflight* [Quality record].
`docs/quality/frontend-exact-closure-source-preflight-2026-07-11.md`.

The Æther Flow Website. (2026b). *Frontend recommendations implementation
plan* [Implementation plan]. `ImplementationPlans/recomendation_frontend.md`.

The Æther Flow Website. (2026c). *Page provenance* [JSON manifest].
`public/files/manifests/page_provenance.json`.

The Æther Flow Website. (2026d). *Source manifest* [JSON manifest].
`public/files/manifests/source_manifest.json`.
