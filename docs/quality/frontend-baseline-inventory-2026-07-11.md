# FE-G0-02 Frontend Baseline Inventory

Date: 2026-07-11  
Packet: `FE-G0-02`  
Task: `WI-20260711-003`  
Job: `WJ-20260711-003-A`  
Adopted roadmap SHA-256:
`55a4190b47dc0a1fbe4d13c38ab24f6cd588c233c9770bce57ff31399c825be5`

## Conclusion

The current static site remains buildable, but the fresh baseline confirms the
roadmap's main scale and maintainability concerns. The build produces 64 pages
and one additional redirect document. Thirty legacy source routes remain. The
site renders 88 tables, 62 informational inline SVG instances, 512 image
occurrences, 906 source selectors, and 37 diagram-gallery items. Aggregate
validation is not green because the pre-existing curator/source-drift gate
fails; this packet records that state and does not repair or acknowledge source
drift.

The machine-readable per-route and per-asset evidence is in
`docs/quality/frontend-baseline-inventory-2026-07-11.json` (The Æther Flow
Website, 2026a).

## Method

The deterministic inventory was generated after `npm run build` with
`scripts/frontend_baseline_inventory.py`. It parses checked-in route sources,
the two public route/provenance manifests, built HTML, source and built CSS, and
public image assets. Focused tests define word, route, SVG, table, and output
behavior.

Rendered-word counts include shared navigation and footer text because that is
reader-visible text. They exclude script, style, template, noscript, and inline
SVG text. SVG classification is structural: `role="img"` or an accessible label
is informational; explicit `aria-hidden`, `role="none"`, or
`role="presentation"` is decorative; other cases are unclassified. Table
treatment labels are deterministic candidates for later human review, not
approved redesign decisions.

Viewport-dependent evidence used local static preview output in headless Chrome
at 1440 by 900 CSS pixels with full motion. The representative routes were
Home, Physics, AI Research System, Resources, and Diagram Gallery, as required
by the adopted roadmap (The Æther Flow Website, 2026b).

## Route and content baseline

| Measurement | Exact result |
| --- | ---: |
| Astro source routes | 64 |
| Astro pages reported by the build | 64 |
| Built HTML documents | 65 |
| Additional redirect document | 1 at `/project/overview/` |
| Active route-map rows | 34 |
| Provenance page rows | 34 |
| Legacy `src/pages/project` routes | 30 |
| Rendered word tokens across built documents | 75,537 |
| Word minimum | 7 at `/project/overview/` redirect |
| Word 25th percentile | 980 |
| Word median | 1,095 |
| Word mean | 1,162.11 |
| Word 75th percentile | 1,307 |
| Word maximum | 2,153 at `/resources/diagrams/` |

The 64-page build count and 65-document filesystem count are not contradictory:
Astro reports 64 generated pages, while the configured `/project/overview/`
redirect adds one small HTML redirect document.

## Table baseline

There are 88 tables across 28 routes. The per-route table records, column
headers, CSS classes, and candidate treatments are preserved in the JSON
evidence.

| Candidate treatment | Count |
| --- | ---: |
| True comparison table | 72 |
| Small status matrix | 14 |
| Public vocabulary or definition | 2 |
| Dense specialist data | 0 |
| Download or asset metadata | 0 |

These are first-pass classification candidates. Table semantics and content
must be reviewed before later packets choose card, status-row, definition-list,
or overflow treatments.

## SVG and animation baseline

| Measurement | Exact result |
| --- | ---: |
| Built inline SVG instances | 62 |
| Informational | 62 |
| Explicit decorative | 0 |
| Unclassified | 0 |
| Source inline SVG artworks | 57 |
| Standalone SVG files | 1 |
| Total source SVG artworks | 58 |
| Astro files containing inline SVG | 54 |
| `role="img"` | 62 |
| `aria-labelledby` | 60 |
| `aria-label` | 2 |
| Title elements | 60 |
| Description elements | 47 |
| Missing a complete title/description pair | 15 |
| SVG-contained ID attributes | 205 |
| Pages with duplicate IDs | 0 |
| Filter definitions | 34 |
| Filter references | 40 |
| Static motion-hook elements | 62 |
| Document figcaptions | 125 |
| CSS keyframes | 23 |
| CSS animation declarations | 51 |

The 15 incomplete title/description pairs are a pre-existing accessibility
defect. Figcaption count is document-wide and is not asserted as a one-to-one
SVG caption mapping. The static motion-hook count is deliberately conservative;
the browser-observed first-view animation counts below are the viewport evidence.

## CSS baseline

| Surface | Lines | Bytes | Selectors |
| --- | ---: | ---: | ---: |
| `src/styles/global.css` | 4,382 | 99,297 | 905 |
| `src/styles/math.css` | 11 | 155 | 1 |
| Total source CSS | 4,393 | 99,452 | 906 |
| Built CSS bundle | 1 line | 113,828 | not re-parsed |
| Built CSS, gzip level 9 | — | 21,338 | — |

The largest first-class selector ownership prefixes are `project` 100,
`track` 61, element-only or at-rule-associated 60, `overview` 41, `ai` 40,
`physics` 36, `nav` 32, `source` 31, `evidence` 27, `operations` 25,
`authority` 25, and `resources` 23. Prefix ownership is a lexical maintenance
signal, not proof of component ownership.

## Image, loading, and gallery baseline

| Measurement | Exact result |
| --- | ---: |
| Public asset files under `public/assets` | 39 |
| Public asset bytes | 3,404,683 |
| Brand PNG dimensions | 1,254 by 1,254 |
| Brand PNG bytes | 1,147,309 |
| Rendered image occurrences | 512 |
| Remote image occurrences in built markup | 320 |
| Occurrences missing both intrinsic dimensions | 128 |
| Default or auto loading occurrences | 64 |
| Eager loading occurrences | 52 |
| Lazy loading occurrences | 396 |
| Diagram Gallery items | 37 |
| Diagram Gallery document height at 1440 by 900 | 14,130 px |

Every representative route placed only the 40 by 40 brand mark above the fold.
The route comprehension images were below the first viewport and lacked width
and height attributes. The JSON evidence records dimensions and byte size for
every local public asset and the loading/dimension state for every rendered
image occurrence.

Static markup contains five remote image occurrences per non-redirect page:
four Shields images and one GitHub-hosted creator image. A full Home-page scroll
caused 11 third-party visual request events: five YouTube embed stylesheet,
font, or image requests; four Shields image requests; the GitHub attachment
request; and its S3 image redirect. No request failed in the measured run.

## First-view browser baseline

| Route | HTTP | Height px | Visible actions | First-view running animated elements | All running animations | Gallery items |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `/` | 200 | 5,074 | 5 | 13 | 28 | 0 |
| `/physics/` | 200 | 4,241 | 8 | 6 | 9 | 0 |
| `/ai-research-system/` | 200 | 4,785 | 8 | 6 | 9 | 0 |
| `/resources/` | 200 | 5,008 | 8 | 7 | 11 | 0 |
| `/resources/diagrams/` | 200 | 14,130 | 9 | 7 | 11 | 37 |

The shared primary navigation contains 30 anchor descendants and three menu
buttons. Home adds a four-anchor homepage-action navigation. Each route also
contains a two-anchor footer project-links navigation. Hidden menu-panel links
are included in navigation child counts but excluded from visible first-view
action counts.

Physics, AI Research System, Resources, and Diagram Gallery produced no browser
console warning or error in the representative run. Home's embedded YouTube
surface produced an unrecognized `web-share` warning, one non-repeating
`compute-pressure` permissions-policy error, and a headless WebGL readback
performance warning. A full-scroll rerun reproduced the `web-share` and WebGL
warnings but not the permissions-policy error. These are recorded as
pre-existing third-party/browser observations, not corrected in this packet.

## Build and validator state

| Command or check | Result |
| --- | --- |
| `npm run build` | Passed; 64 pages built |
| Focused inventory tests | Passed; 3 tests |
| `.venv/bin/python -m pytest` | Passed; 79 tests |
| `git diff --check` | Passed |
| `npm run validate:implementation-control` | Passed before closeout |
| `npm run validate` | Failed at `validate:curator` after manifest, content, link, layout, SVG, and provenance checks passed |

The aggregate failure is pre-existing and outside this packet's write scope.
The checked-in curator JSON and Markdown reports are stale; many source-drift
rows lack exact acknowledgement; and `/physics/claim-status/` reports critical
drift for the claim-boundary registry, Distance-to-GR ledger, and upstream
program state. Making the aggregate gate green requires a separately governed
source-refresh/curator packet. This baseline does not write curator reports,
acknowledge drift, change manifests, promote physics claims, or mutate upstream.

## Pre-existing defect ledger

1. Fifteen informational SVGs lack a complete title/description pair.
2. One hundred twenty-eight rendered image occurrences lack both intrinsic
   dimensions.
3. The global stylesheet remains a 4,382-line, 905-selector monolith.
4. The first viewport runs 6 to 13 animated elements on representative routes;
   Home runs 28 animations across the document.
5. The shared primary navigation exposes 30 anchor descendants and three menu
   buttons before later mobile and information-architecture work.
6. The gallery is 14,130 pixels tall at the measured desktop viewport and
   renders all 37 approved items in one document.
7. Every non-redirect page contains five remote image URLs in shared markup;
   Home also initiates YouTube embed visual requests.
8. Thirty legacy source routes remain, plus the separately configured
   `/project/overview/` redirect document.
9. Aggregate validation is blocked by stale curator reports and unacknowledged
   upstream drift, including critical current-state drift.

## Boundary and next gate

This report is website-local implementation evidence. It changes no scientific,
mathematical, governance, or workflow claim; performs no source refresh; grants
no physics-owner acceptance; and changes no frontend runtime, public route,
asset, manifest, upstream repository, remote Git state, or deployment state.

After the local `FE-G0-02` checkpoint, `FE-G0-03` may be separately authorized
to measure current performance and propose provisional budgets. This packet does
not authorize it.

## References

The Æther Flow Website. (2026a, July 11). *FE-G0-02 frontend baseline inventory*
[JSON data set].

The Æther Flow Website. (2026b, July 11). *Frontend recommendation and
implementation roadmap* [Implementation plan].
