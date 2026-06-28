# Sitewide Revamp PG-011 No-Target-Import Discipline QA

## Scope

Packet: PG-011, Create No-Target-Import Discipline Page.

Route: `/project/physics/no-target-import-discipline/`.

Primary files:

- `docs/system-analyses/no-target-import-discipline.md`
- `docs/content-dossiers/physics-no-target-import-discipline/dossier.md`
- `docs/content-dossiers/physics-no-target-import-discipline/diagrams/no-target-import-discipline.mmd`
- `src/pages/project/physics/no-target-import-discipline/index.astro`
- `public/assets/diagrams/comprehension/physics-no-target-import-discipline.png`
- `src/lib/siteContent.ts`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `public/files/manifests/page_provenance.json`

## Source Review

Reviewed source records:

- `research_control/design/no_target_import_guard_map.md`
- `research_control/tasks/RT-20260614-105/DDR-20260614-105.md`
- `research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex`
- `research_control/tasks/RT-20260614-128/jobs/completions/AJC-AJ-RT-20260614-128-001.yaml`
- `research_control/tasks/RT-20260614-128/artifacts/parent_conflict_review_m_src_gsc_no_target_import_criterion.yaml`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `github-facing/claim-gates-explainer.md`
- `github-facing/gr-derivation-roadmap-explainer.md`

Source conclusion: no-target-import discipline is a reusable guardrail and
criterion for source-only factorization. Current criterion status is
`criterion_formalized_pending_audit`. It is not `M_src` adoption, not proof
that all future work is target-import-free, and not downstream GR promotion.

## No-AI-Slop Gate

Status: pass.

Reasoning:

- The page is source-bounded to inspected guard-map, criterion, completion,
  review, registry, and explainer records.
- The public explanation distinguishes forbidden target-context imports from
  acceptable source-side construction.
- The equation `C_src(E; T)=F_src(E)` is explained as an audit criterion, not
  proof of adoption.
- Unsafe summaries explicitly block all-future-clean, `M_src` adoption,
  benchmark-as-source-evidence, and process-authority-as-proof overreads.
- The page preserves no g_eff, no matter coupling, no Einstein equations, no
  benchmark promotion, no downstream GR promotion, and no completed derivation.

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

- `http://127.0.0.1:4322/project/physics/no-target-import-discipline/`

Desktop screenshot:

- `output/playwright/sitewide-revamp-pg011-no-target-import-static-desktop-2026-06-28.png`

Mobile screenshot:

- `output/playwright/sitewide-revamp-pg011-no-target-import-static-mobile-2026-06-28.png`

Automated browser checks passed:

- Required text present: `No-Target-Import Discipline`, `target metric`,
  `target topology`, `benchmark success`, `source-only factorization`,
  `C_src(E; T)=F_src(E)`, `criterion_formalized_pending_audit`,
  `OB-MSRC-TARGET-IMPORT`, `OB-MSRC-PROCESS-AUTHORITY-LAUNDERING`,
  `fail-closed`, `not proof that all future work is target-import-free`,
  `no g_eff`, and `no downstream GR promotion`.
- No console errors.
- No page errors.
- No broken loaded images.
- No `/Volumes/` text leakage.
- Desktop document horizontal overflow: 0.
- Mobile document horizontal overflow: 0.

Visual review:

- Desktop layout is readable.
- Mobile layout is readable.
- The mobile H1 wraps but remains contained.
- Long source paths in the source notice wrap without creating page-level
  horizontal overflow.

## Known Blocker Outside PG-011

Full curator validation is expected to continue failing on known ontology
TeX/PDF critical source drift until those derivative/source pairs are
reconciled. PG-011 did not alter that blocker.

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

PG-011 is technically complete for local review. The logical next step is to
continue with PG-012 after rerunning curator reporting for the updated site
state.
