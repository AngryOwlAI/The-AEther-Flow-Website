# Sitewide Revamp PG-014 Research-Agent Workflow QA

## Scope

Packet: PG-014, Rewrite Research-Agent Workflow Walkthrough.

Route: `/project/ai-research-agent-system/workflow/`.

Primary files:

- `docs/system-analyses/research-agent-workflow-walkthrough.md`
- `docs/content-dossiers/ai-workflow/dossier.md`
- `docs/content-dossiers/ai-workflow/diagrams/bounded-agentjob-chain.mmd`
- `src/pages/project/ai-research-agent-system/workflow/index.astro`
- `src/lib/aiComprehensionContent.ts`
- `src/lib/siteContent.ts`
- `public/assets/diagrams/comprehension/ai-workflow-bounded-agentjob-chain.png`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `public/files/manifests/page_provenance.json`

## Source Review

Reviewed committed upstream source records through `git show HEAD:<path>`:

- `github-facing/research-agent-workflow-explainer.md`
- `github-facing/director-agentjob-lifecycle-explainer.md`
- `research_control/README.md`
- `github-facing/validator-operator-workflow-explainer.md`
- `research_control/tasks/RT-20260614-249/00_TASK.yaml`
- `research_control/tasks/RT-20260614-249/DDR-20260614-249.md`
- `research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml`
- `research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml`
- `research_control/handoffs/handoff-0282.yaml`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`

Source conclusion: the workflow route can safely use `RT-20260614-249` as a
committed concrete record-chain example if it remains an operations
walkthrough, not a physics-proof page. The route must state that PASS, memory,
role labels, registry rows, generated pages, and handoffs are bounded evidence
only.

## No-AI-Slop Gate

Status: pass.

Reasoning:

- The page now walks a concrete task, Director decision, AgentJob, completion,
  handoff, and registry chain.
- Memory is described as navigation, not authority.
- Validator PASS is described as operational evidence only.
- Handoff is described as a separate next packet, not silent extension.
- The page avoids treating model behavior as independent scientific
  understanding or authority.
- The `RT-20260614-249` example preserves no coupling-law adoption, no
  matter-coupling derivation or adoption, no `MetricData(E)`, no `g_eff`, no
  Einstein equations, no benchmark promotion, and no completed derivation.

Subagent note: no subagent was spawned. The available multi-agent tool policy
requires explicit user request before spawning subagents.

## Validation

Passed:

- `python3 scripts/render_mermaid_diagrams.py`
- mechanical source-manifest diagram hash refresh from generated PNG files
- `python3 scripts/build_asset_manifest.py --write`
- `python3 scripts/generate_page_provenance.py`
- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:provenance`
- `npm run validate:comprehension`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run build`
- `git diff --check`

Manifest note: rerendering all registered Mermaid diagrams refreshed diagram
SHA-256 values in `source_manifest.json`, then the asset manifest was rebuilt.

Curator report note:

- `python3 scripts/run_curator.py --write` refreshed
  `curator/reports/latest.json` and `curator/reports/latest.md`.
- `npm run validate:curator` then failed only on the known 16 ontology
  TeX/PDF critical source-drift records listed below.

## Browser QA

Target:

- `http://127.0.0.1:4322/project/ai-research-agent-system/workflow/`

Desktop screenshot:

- `output/playwright/sitewide-revamp-pg014-workflow-static-desktop-2026-06-28.png`

Mobile screenshot:

- `output/playwright/sitewide-revamp-pg014-workflow-static-mobile-2026-06-28.png`

Automated browser checks passed:

- Required text present: `RESEARCH-AGENT WORKFLOW`,
  `RT-20260614-249`, `Director decision`, `AgentJob`, `Completion`,
  `Handoff`, `Memory preflight`, `PASS is operational evidence`,
  `No autonomous proof claim`, `no coupling-law adoption`,
  `no matter-coupling derivation or adoption`, `no MetricData(E)`,
  `no g_eff`, `not silent extension`, and `Source authority`.
- No console errors.
- No page errors.
- No broken loaded images.
- No `/Volumes/` text leakage.
- Desktop document horizontal overflow: 0.
- Mobile document horizontal overflow: 0.

Visual review:

- Desktop layout is readable.
- Mobile layout is readable.
- Long record paths and source refs wrap inside their containers without
  creating page-level horizontal overflow.

## Known Blocker Outside PG-014

Full curator validation is expected to continue failing on known ontology
TeX/PDF critical source drift until those derivative/source pairs are
reconciled. PG-014 did not alter that blocker.

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

PG-014 is technically complete for local review. The logical next step is to
continue with PG-015.
