# Sitewide Revamp PG-012 Negative Results And Frozen Routes QA

## Scope

Packet: PG-012, Create Negative Results And Frozen Routes Page.

Route: `/project/physics/negative-results-and-frozen-routes/`.

Primary files:

- `docs/system-analyses/negative-results-and-frozen-routes.md`
- `docs/content-dossiers/physics-negative-results-and-frozen-routes/dossier.md`
- `docs/content-dossiers/physics-negative-results-and-frozen-routes/diagrams/negative-results-freeze-flow.mmd`
- `src/pages/project/physics/negative-results-and-frozen-routes/index.astro`
- `public/assets/diagrams/comprehension/physics-negative-results-and-frozen-routes.png`
- `src/lib/siteContent.ts`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `public/files/manifests/page_provenance.json`

## Source Review

Reviewed source records:

- `research_control/design/obstruction_and_freeze_control.md`
- `github-facing/claim-gates-explainer.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex`
- `research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex`
- `src/data/distance_to_gr_snapshot.json`
- `src/data/claim_boundary_snapshot.json`

Source conclusion: negative results and frozen routes are useful preserved
evidence only when failed object, scope, consequence, `forbidden_overread`, and
next route remain visible. A `frozen negative` route is not global theory
rejection, not future source-extension impossibility, and not downstream GR
promotion.

## No-AI-Slop Gate

Status: pass.

Reasoning:

- The page names limitations directly instead of hiding them behind positive
  framing.
- It distinguishes `scoped obstruction`, `route_frozen`, and `locally_frozen`
  from global no-go claims.
- It uses checked-in Distance-to-GR snapshot examples rather than live source
  reads during build.
- Safe and unsafe summaries block global rejection, future-impossibility,
  benchmark-promotion, validator-as-proof, and adoption overreads.

## Validation

Passed:

- `python3 scripts/render_mermaid_diagrams.py`
- `python3 scripts/build_asset_manifest.py --write`
- `python3 scripts/generate_page_provenance.py`
- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:provenance`
- `npm run validate:comprehension`
- `npm run validate:links`
- `npm run validate:svg`
- `npm run validate:layout`
- `npm run build`
- `git diff --check`

Manifest note: rerendering all registered Mermaid diagrams changed the
`physics-gate-chair-human-gates.png` hash again. Diagram SHA-256 values were
refreshed from generated public files, then the asset manifest was rebuilt.

## Browser QA

Target:

- `http://127.0.0.1:4322/project/physics/negative-results-and-frozen-routes/`

Desktop screenshot:

- `output/playwright/sitewide-revamp-pg012-negative-results-static-desktop-2026-06-28.png`

Mobile screenshot:

- `output/playwright/sitewide-revamp-pg012-negative-results-static-mobile-2026-06-28.png`

Automated browser checks passed:

- Required text present: `Negative Results And Frozen Routes`,
  `negative results`, `scoped obstruction`, `frozen negative`,
  `route_frozen`, `locally_frozen`, `forbidden_overread`,
  `not global theory rejection`, `not future source-extension impossibility`,
  `finite_toy_metric_response`, `Distance-to-GR`, `claim boundaries`, and
  `no downstream GR promotion`.
- No console errors.
- No page errors.
- No broken loaded images.
- No `/Volumes/` text leakage.
- Desktop document horizontal overflow: 0.
- Mobile document horizontal overflow: 0.

Visual review:

- Desktop layout is readable.
- Mobile layout is readable.
- Long source paths in the source notice wrap without creating page-level
  horizontal overflow.

## Known Blocker Outside PG-012

Full curator validation is expected to continue failing on known ontology
TeX/PDF critical source drift until those derivative/source pairs are
reconciled. PG-012 did not alter that blocker.

Checked command:

- `npm run validate:curator`

Observed result: failed only on the 16 known ontology critical source-drift
records:

- `ontology/pdfs/aether_flow_consistency.pdf`
- `ontology/pdfs/aether_flow_dynamics.pdf`
- `ontology/pdfs/aether_flow_exact_closure_flagship_article.pdf`
- `ontology/pdfs/aether_flow_exact_closure_note.pdf`
- `ontology/pdfs/aether_flow_exact_closure_sequence_overview.pdf`
- `ontology/pdfs/aether_flow_foundations.pdf`
- `ontology/pdfs/aether_flow_geometry.pdf`
- `ontology/pdfs/aether_flow_relativistic_recovery.pdf`
- `ontology/tex/aether_flow_consistency.tex`
- `ontology/tex/aether_flow_dynamics.tex`
- `ontology/tex/aether_flow_exact_closure_flagship_article.tex`
- `ontology/tex/aether_flow_exact_closure_note.tex`
- `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`
- `ontology/tex/aether_flow_foundations.tex`
- `ontology/tex/aether_flow_geometry.tex`
- `ontology/tex/aether_flow_relativistic_recovery.tex`

## Conclusion

PG-012 is technically complete for local review. The logical next step is to
continue with PG-013 after rerunning curator reporting for the updated site
state.
