# FE-P0-01 Authoritative Exact-Closure Source Preflight

Date: 2026-07-11  
Packet: `FE-P0-01`  
Task: `WI-20260711-007`  
Job: `WJ-20260711-007-A`  
Disposition: `source_refresh_and_manifest_authority_repair_required`

## 1. Scope and authority boundary

This report pins and compares the exact-closure source set required by the
adopted frontend recommendations plan. It is website-local evidence, not
scientific authority. The upstream repository and its registered TeX sources
and registries remain authoritative.

The preflight was read-only toward
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`. It did not refresh a source, rebuild
a derivative, modify a registry or manifest, regenerate provenance, change a
public claim, appoint a physics reviewer, alter frontend runtime, push, or
deploy.

## 2. Pinned upstream state

| Field | Observed value | Result |
| --- | --- | --- |
| Repository | `/Volumes/P-SSD/AngryOwl/The-AEther-Flow` | Pinned |
| Branch | `main` | Pinned |
| Commit | `a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0` | Pinned |
| Commit date | `2026-07-09T10:35:40-06:00` | Pinned |
| Commit subject | `Research control: RT-20260709-008 validator-engineer@0.2.0--RT-20260709-008 completion` | Pinned |
| Remote parity | `origin/main` resolves to the same commit | Pass |
| Worktree | `## main...origin/main` with no changed paths | Clean and committed |

The current checkout satisfies the plan's clean-and-committed precondition.

## 3. Exact-closure source and derivative comparison

### 3.1 Registered TeX sources

| Source | Upstream SHA-256 | Website SHA-256 | Byte comparison | Upstream registry state |
| --- | --- | --- | --- | --- |
| `ontology/tex/aether_flow_exact_closure_sequence_overview.tex` | `356a5f65b0931914fdf9362ba544c2868bad7d33b828754b91c029bed96f86b1` | `356a5f65b0931914fdf9362ba544c2868bad7d33b828754b91c029bed96f86b1` | Match | `canonical`; `benchmark_claim`; `canonical_ontology`; `accepted`; validation `PASS` |
| `ontology/tex/aether_flow_exact_closure_note.tex` | `c4a4e956ad5a10e6b3f4e661351bdeda2145b01e6e85d9df849e765c765eca35` | `c4a4e956ad5a10e6b3f4e661351bdeda2145b01e6e85d9df849e765c765eca35` | Match | `canonical`; `benchmark_claim`; `canonical_ontology`; `accepted`; validation `PASS` |
| `ontology/tex/aether_flow_exact_closure_flagship_article.tex` | `900c799cb0c3d8f790c836196c136b3cec6944e46d41b89e511b85123fd30e40` | `900c799cb0c3d8f790c836196c136b3cec6944e46d41b89e511b85123fd30e40` | Match | `canonical`; `benchmark_claim`; `canonical_ontology`; `accepted`; validation `PASS` |

The exact TeX bytes are unchanged between the website manifest's older source
commit `c7369577a7e5f96c3f4c4c6c6982e723cd3cc751` and the current upstream pin.
The three applicable TeX registry rows are also unchanged from the route
provenance pin `2a934c29b58e84aa913a5088a8388bd259f6370b` and retain their current
registered states.

### 3.2 Registered PDF derivatives

| Derivative | Upstream SHA-256 | Website SHA-256 | Byte comparison | Upstream registry state |
| --- | --- | --- | --- | --- |
| `ontology/pdfs/aether_flow_exact_closure_sequence_overview.pdf` | `32f3a8fd6e902a892ae5c1126996d1fe6988e446c354647f677b9576201bc963` | `32f3a8fd6e902a892ae5c1126996d1fe6988e446c354647f677b9576201bc963` | Match | `pdf_derivative`; `generated_noncanonical`; validation `PASS`; build `built` |
| `ontology/pdfs/aether_flow_exact_closure_note.pdf` | `209c70ba169d98ba7a4324923ace3a48011c5341f63459c6549e30f511ba667b` | `209c70ba169d98ba7a4324923ace3a48011c5341f63459c6549e30f511ba667b` | Match | `pdf_derivative`; `generated_noncanonical`; validation `PASS`; build `built` |
| `ontology/pdfs/aether_flow_exact_closure_flagship_article.pdf` | `df25a63a39010fa521d373bf5bdb36fb9e25d81b6bfe308b726e25bd77af854b` | `df25a63a39010fa521d373bf5bdb36fb9e25d81b6bfe308b726e25bd77af854b` | Match | `pdf_derivative`; `generated_noncanonical`; validation `PASS`; build `built` |

The PDF bytes are current, but the website `source_manifest.json` marks each
PDF entry's `source_authority_status` as `canonical`. That conflicts with the
upstream PDF derivative registry and the repository rule that PDFs are
generated human-readable derivatives of registered TeX sources. The manifest
notes already describe the PDFs as derivatives, so the structured status and
human-readable note currently disagree.

## 4. Registry pins and claim boundary

| Registry | Current upstream SHA-256 | Relevant finding |
| --- | --- | --- |
| `registries/TEX_SOURCE_REGISTRY.csv` | `5b25759537db85573b8571127d7fa57a6a664dd09fc41a0cd6ea349511f9f3d2` | Exact-closure TeX rows remain canonical, accepted benchmark claims; they explicitly do not prove first-principles GR derivation. |
| `registries/PDF_DERIVATIVE_REGISTRY.csv` | `93f9510d9b5862128425be2045e1dcc0880d9692d2cdbbfa612f1a25fb16480b` | Exact-closure PDFs are generated, noncanonical human-reading derivatives. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | `ce67a8f2060074c61d2bf4b613ef056c3891547c5f16ba230e6673a2acb30519` | Active public-physics and ontology boundaries keep public surfaces generated and noncanonical and require gates for promotion, ontology edits, or completed-derivation language. |

The authoritative source language supports the bounded frontend framing:

1. The exact-closure package is complete at the effective-theory level.
2. Its observable gravitational content is operationally identical to
   ordinary general relativity.
3. The Æther / Æther-Flow ontology remains interpretive and conceptual within
   that effective package.
4. A first-principles recovery from substrate dynamics remains open.

This preflight does not approve website copy that expresses those points. It
only verifies that the adopted plan's framing is present in the pinned sources.

## 5. Website publication comparison

### 5.1 Source manifest

`public/files/manifests/source_manifest.json` has SHA-256
`800fc14d7b6c8836766f8ee7286b739ee9982a6c3f4a0e0da679fab89088c5c5`
and was generated on `2026-06-29T00:26:25.502165+00:00`.

- All six exact-closure TeX/PDF hashes match current upstream bytes.
- Each exact-closure item remains pinned to upstream commit
  `c7369577a7e5f96c3f4c4c6c6982e723cd3cc751`, not the current pinned commit.
- The three TeX authority and claim fields match the current upstream TeX
  registry.
- The three PDF `source_authority_status` values conflict with the current
  upstream PDF derivative registry: website `canonical` versus upstream
  `generated_noncanonical`.

Disposition: a separately authorized source-manifest authority repair and
repin is required. This report does not select or introduce a new enum.

### 5.2 Home and Physics route bundles

`public/files/manifests/page_route_map.json` has SHA-256
`8b7d8ea7a9c388fd7969e9d6bc2370c443665374fbdd7383138509f3f773fa8f`.

- `/` is a `curated_synthesis` with `generated_noncanonical` authority and a
  `trust_boundary`; it includes none of the overview, note, or flagship TeX
  sources.
- `/physics/` is a `curated_synthesis` with `generated_noncanonical` authority
  and a `claim_boundary`; it includes none of the overview, note, or flagship
  TeX sources.
- The existing `generated_noncanonical` route status remains logically correct
  for these reader-facing syntheses. Adding canonical inputs later would not
  make either route canonical.

Disposition: the omissions are confirmed inputs to `FE-P0-03` and `FE-P0-04`,
but those packets must not run until the source-refresh and manifest-authority
repair gate is cleared.

### 5.3 Page provenance

`public/files/manifests/page_provenance.json` has SHA-256
`0ef0d847f3f3f0b9a9cd13b475df91cf74db7de8b0720746fe41a24ff3c5a4f6`,
was generated on `2026-07-01T06:17:34.258417+00:00`, and pins upstream commit
`2a934c29b58e84aa913a5088a8388bd259f6370b`.

- Home and Physics provenance omit all three required exact-closure TeX
  sources because their route bundles omit them.
- Physics provenance records `registries/CLAIM_BOUNDARY_REGISTRY.csv` at
  `e85cf244f133531cba72d96f443731819869237639316bb7db64c5987befa75b`;
  the current registry hash is
  `ce67a8f2060074c61d2bf4b613ef056c3891547c5f16ba230e6673a2acb30519`.
- Both route records remain correctly classified as
  `generated_noncanonical`, but their source pins are not current.

Disposition: provenance is stale and must be regenerated only in a separately
authorized packet after route-bundle and manifest authority dispositions are
approved.

### 5.4 Source-notice defaults

`src/lib/siteContent.ts` has SHA-256
`1799a1ad94ea408e265a478f380b39678cef23ef12d702ab15e462a09b31c081`.

- Home source-notice defaults cite the local Home source plus project overview
  and source-authority material, but not the exact-closure overview, note, or
  flagship article.
- Physics source-notice defaults cite general physics, benchmark, and claim
  explainer material, but not the exact-closure overview, note, or flagship
  article.
- The existing notes preserve the upstream-authority boundary and do not
  themselves promote a claim.

Disposition: contextual source references and dates require later bounded
repair with `FE-P0-03` and `FE-P0-04`; no copy was changed here.

## 6. Physics-review and public-positioning ownership

No inspected governed record appoints an independent physics reviewer for the
frontend claim matrix or supplies the required checked-in receipt. The website
decision ledger explicitly records the physics reviewer as unassigned and
blocks `AG-01` and public claim work. The current upstream external-review
response template likewise states that it does not name a reviewer, authorize
outreach, publish reviewer identity, grant proof authority, or grant benchmark
authority.

Upstream documentation-curator and claim-boundary records permit bounded public
orientation while preserving generated-noncanonical status. They do not grant
physics-promotion or website-copy approval authority.

Disposition: `FE-P0-05`, `FE-P0-06`, and all source-strengthened public claim
publication remain blocked pending an independent named reviewer and receipt.

## 7. Drift disposition

| ID | Observation | Classification | Required action | Downstream effect |
| --- | --- | --- | --- | --- |
| P0-01-D01 | Upstream `main` is clean and equals `origin/main` at `a8c0b3f…` | Pass | Use this commit as the authoritative preflight pin | Satisfies clean-source precondition |
| P0-01-D02 | All three website TeX copies match current upstream hashes | No content drift | Preserve bytes; repin metadata later | Exact sources are usable after gate repair |
| P0-01-D03 | All three TeX registry rows remain canonical, benchmark, canonical-ontology, and accepted | No applicable status drift | Preserve registered states and limitations | No physics promotion granted |
| P0-01-D04 | All three website PDFs match current upstream hashes | No content drift | Preserve derivative bytes unless a later source rebuild is independently required | Derivatives are current by hash |
| P0-01-D05 | Website PDF manifest status is `canonical`; upstream status is `generated_noncanonical` | Manifest-authority mismatch | Separately authorize a source-manifest authority repair with schema/fixture review as applicable | Blocks downstream publication packets |
| P0-01-D06 | Exact-closure manifest items pin older commit `c736957…` | Freshness drift without byte drift | Repin through the approved source-manifest workflow | Blocks downstream publication packets |
| P0-01-D07 | Home and Physics route bundles omit overview, note, and flagship TeX | Known source-bundle gap | Repair in `FE-P0-03` and `FE-P0-04` after the preceding gate | Blocks narrative/provenance release |
| P0-01-D08 | Page provenance pins `2a934c2…`; Physics pins an obsolete claim-boundary hash | Critical provenance drift | Regenerate only after approved source/route changes | Blocks reliance on current provenance |
| P0-01-D09 | Home and Physics source notices omit the exact-closure sources | Contextual provenance gap | Repair dates and references in their bounded packets | Blocks source-corrected narrative release |
| P0-01-D10 | No independent physics reviewer or receipt exists | Approval gap | Appoint qualified reviewer and check in `AG-01` evidence | Blocks `FE-P0-05`, `FE-P0-06`, and public claim publication |

## 8. Conclusion

`FE-P0-01` has a complete read-only evidence result, but the disposition is not
`proceed_to_FE-P0-02`. The authoritative exact-closure source and derivative
bytes are clean and hash-identical, with no physics delta. The website's
publication metadata is not ready: PDF authority status conflicts with the
upstream registry, source pins are stale, route bundles omit the required
canonical TeX sources, and page provenance includes stale registry evidence.

The logical next step is a separately authorized, website-local
source-refresh and manifest-authority repair packet. It must resolve the PDF
authority status without strengthening source claims, repin current source
metadata, acknowledge or regenerate stale provenance in the correct order, and
preserve Home and Physics as generated, noncanonical syntheses. `FE-P0-02` must
remain unopened until that gate is cleared.

No upstream source, physics claim, physics status, physics promotion, or
physics delta changed in this packet.

## References

The Æther Flow Project. (2026a). *Æther Flow exact-closure flagship article*
[TeX source]. `ontology/tex/aether_flow_exact_closure_flagship_article.tex`.

The Æther Flow Project. (2026b). *Æther Flow exact-closure note* [TeX source].
`ontology/tex/aether_flow_exact_closure_note.tex`.

The Æther Flow Project. (2026c). *Æther Flow exact-closure sequence overview*
[TeX source].
`ontology/tex/aether_flow_exact_closure_sequence_overview.tex`.

The Æther Flow Project. (2026d). *Claim boundary registry* [CSV registry].
`registries/CLAIM_BOUNDARY_REGISTRY.csv`.

The Æther Flow Project. (2026e). *External review response intake template v1*
[Research-control template].
`research_control/design/external_review_response_intake_template_v1.md`.

The Æther Flow Project. (2026f). *PDF derivative registry* [CSV registry].
`registries/PDF_DERIVATIVE_REGISTRY.csv`.

The Æther Flow Project. (2026g). *TeX source registry* [CSV registry].
`registries/TEX_SOURCE_REGISTRY.csv`.

The Æther Flow Website. (2026a). *Frontend decision ledger, 2026-07-11*
[Quality record]. `docs/quality/frontend-decision-ledger-2026-07-11.md`.

The Æther Flow Website. (2026b). *Frontend recommendations implementation
plan* [Adopted planning context].
`ImplementationPlans/recomendation_frontend.md`.

The Æther Flow Website. (2026c). *Page provenance* [JSON manifest].
`public/files/manifests/page_provenance.json`.

The Æther Flow Website. (2026d). *Page route map* [JSON manifest].
`public/files/manifests/page_route_map.json`.

The Æther Flow Website. (2026e). *Source manifest* [JSON manifest].
`public/files/manifests/source_manifest.json`.
