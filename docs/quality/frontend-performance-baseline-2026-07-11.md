# FE-G0-03 Frontend Performance Baseline — 2026-07-11

## Analysis

This report is a read-only local lab baseline for the five routes required by
`FE-G0-03`. It does not claim production or field performance. Three pinned
Lighthouse mobile-simulation runs were collected per route against the static
Astro preview. No frontend runtime, public claim, source, asset, manifest,
remote Git, or deployment state changed.

## Method

- Lighthouse 13.4.0; 3 cold-navigation runs per route.
- Form factor: mobile; throttling: simulate; viewport: 412 × 823 CSS px.
- CPU slowdown: 4×; RTT: 150 ms; throughput: 1638.4 Kbps.
- Measurement window: 2026-07-11T17:20:49.484Z through 2026-07-11T17:24:05.467Z.
- Aggregates use median for the central observation and maximum for stability/no-regression guards.

## Route results

| Route | Score median | LCP median / max | CLS max | TBT max | Transfer | Requests | Budget result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `/` | 100 | 1.58 s / 7.05 s | 0.00 | 0 ms | 1214.9 KiB | 5 | fail: lcp_stability_guard, long_task_guard, below_fold_eager_image_target |
| `/physics/` | 77 | 7.05 s / 7.05 s | 0.00 | 0 ms | 1209.7 KiB | 5 | fail: lcp_median_target, lcp_stability_guard, long_task_guard, below_fold_eager_image_target |
| `/ai-research-system/` | 100 | 1.28 s / 6.90 s | 0.00 | 0 ms | 1177.3 KiB | 5 | fail: lcp_stability_guard, long_task_guard, below_fold_eager_image_target |
| `/resources/` | 77 | 7.05 s / 7.05 s | 0.00 | 0 ms | 1196.2 KiB | 5 | fail: lcp_median_target, lcp_stability_guard, long_task_guard, below_fold_eager_image_target |
| `/resources/diagrams/` | 100 | 1.58 s / 1.58 s | 0.00 | 0 ms | 1293.0 KiB | 7 | fail: long_task_guard, below_fold_eager_image_target |

### Per-run LCP and score evidence

| Route | Run | Score | FCP | LCP | CLS | TBT | Longest task |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `/` | 1 | 100 | 0.90 s | 1.50 s | 0.00 | 0 ms | 50 ms |
| `/` | 2 | 77 | 0.90 s | 7.05 s | 0.00 | 0 ms | 51 ms |
| `/` | 3 | 100 | 0.90 s | 1.58 s | 0.00 | 0 ms | 0 ms |
| `/physics/` | 1 | 100 | 0.90 s | 1.50 s | 0.00 | 0 ms | 51 ms |
| `/physics/` | 2 | 77 | 0.90 s | 7.05 s | 0.00 | 0 ms | 52 ms |
| `/physics/` | 3 | 77 | 0.90 s | 7.05 s | 0.00 | 0 ms | 0 ms |
| `/ai-research-system/` | 1 | 77 | 0.90 s | 6.90 s | 0.00 | 0 ms | 54 ms |
| `/ai-research-system/` | 2 | 100 | 0.90 s | 1.28 s | 0.00 | 0 ms | 51 ms |
| `/ai-research-system/` | 3 | 100 | 0.90 s | 1.28 s | 0.00 | 0 ms | 51 ms |
| `/resources/` | 1 | 77 | 0.90 s | 7.05 s | 0.00 | 0 ms | 0 ms |
| `/resources/` | 2 | 77 | 0.90 s | 7.05 s | 0.00 | 0 ms | 52 ms |
| `/resources/` | 3 | 100 | 0.90 s | 1.43 s | 0.00 | 0 ms | 51 ms |
| `/resources/diagrams/` | 1 | 100 | 0.90 s | 1.58 s | 0.00 | 0 ms | 50 ms |
| `/resources/diagrams/` | 2 | 100 | 0.90 s | 1.50 s | 0.00 | 0 ms | 52 ms |
| `/resources/diagrams/` | 3 | 100 | 0.90 s | 1.58 s | 0.00 | 0 ms | 51 ms |

## Findings

1. The shared 1,147,309-byte header PNG dominates every route. Total initial transfer is 1177.3 KiB–1293.0 KiB; Lighthouse estimates most header-image bytes are avoidable.
2. CLS and TBT were zero in all 15 runs. No external JavaScript transfer was observed; any inline script remains part of the HTML response. Lighthouse still recorded unattributable long tasks up to 54 ms, slightly above the 50 ms guard.
3. LCP was unstable above the 4-second guard on: home, physics, ai, resources. The repeated approximately 7.05-second samples make LCP stability a baseline defect even where a route median passes 2.5 seconds.
4. The lab observed no remote requests. This does not negate the separate FE-G0-02 browser observation that Home can initiate third-party YouTube requests during broader interaction/full-scroll behavior.
5. Below-fold images were fetched during initial navigation on: home, physics, ai, resources, gallery. This fails the provisional zero-eager-fetch target where the images are comprehension diagrams below the mobile viewport.
6. INP is unavailable because no field dataset or controlled interaction series was supplied. TBT is retained only as a lab responsiveness proxy.

## Measured provisional budgets

- User-centric lab gates: route median LCP ≤ 2.5 s, maximum-run LCP stability guard ≤ 4.0 s, maximum CLS ≤ 0.10, maximum TBT ≤ 200 ms, and no unexplained long task above 50 ms.
- Transfer and request ceilings: each route may not exceed its measured maximum without review. These are no-regression ceilings, not acceptable end-state targets.
- CSS review threshold: route CSS transfer above 110% of the measured baseline requires explicit budget review.
- External JavaScript and remote visual-request ceilings remain zero unless separately approved.
- Below-fold comprehension-diagram eager fetches remain zero; the current baseline does not meet this target.
- Remediation targets remain 30 KB for a 1× modern header logo, 60 KB for 2×, 100 KB for PNG fallback, and 250 KB for initial Home raster transfer. The current Home raster transfer is 1184.6 KiB.

## Structured-data observation

| Route | JSON-LD blocks | Types | Malformed |
| --- | ---: | --- | ---: |
| `/` | 0 | none | 0 |
| `/physics/` | 0 | none | 0 |
| `/ai-research-system/` | 0 | none | 0 |
| `/resources/` | 0 | none | 0 |
| `/resources/diagrams/` | 0 | none | 0 |

Presence and JSON parsing do not establish rich-result eligibility. Google’s
guidance requires accurate, relevant markup that represents visible page content.

## Limitations

- Local static preview removes production CDN, TLS, geographic latency, cache, and server variability.
- Three simulated mobile lab runs are diagnostic and do not substitute for 75th-percentile field Core Web Vitals.
- No representative user interactions were executed, so INP is unavailable; TBT is the recorded lab proxy.
- Performance-only Lighthouse runs do not validate structured-data eligibility; checked-in JSON-LD is inventoried separately.

## Conclusion

The current frontend is main-thread-light but image-heavy. CLS and TBT satisfy
the provisional gates, while LCP stability does not. The logical repair order is
to right-size the shared header logo, add the planned image loading/dimension
policy, and rerun the identical baseline before enforcing budgets in CI.

## References

Chrome for Developers. (n.d.). *Total Blocking Time*. Retrieved July 11, 2026, from https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time

Google Search Central. (2026, January 6). *General structured data guidelines*. https://developers.google.com/search/docs/appearance/structured-data/sd-policies

web.dev. (2025, May 7). *How the Core Web Vitals metrics thresholds were defined*. https://web.dev/articles/defining-core-web-vitals-thresholds
