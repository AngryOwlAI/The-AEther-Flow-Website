# Sitewide Revamp PG-015 One Bounded AgentJob QA

## Scope

Packet: PG-015, Create One Bounded AgentJob Page.

Route: `/project/ai-research-agent-system/one-bounded-agentjob/`.

Primary files:

- `docs/system-analyses/one-bounded-agentjob-in-practice.md`
- `docs/content-dossiers/ai-one-bounded-agentjob/dossier.md`
- `docs/content-dossiers/ai-one-bounded-agentjob/diagrams/one-agentjob-envelope.mmd`
- `src/pages/project/ai-research-agent-system/one-bounded-agentjob/index.astro`
- `src/lib/siteContent.ts`
- `scripts/render_mermaid_diagrams.py`
- `scripts/validate_public_comprehension.py`
- `public/assets/diagrams/comprehension/ai-one-bounded-agentjob-envelope.png`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/source_manifest.json`
- `public/files/manifests/asset_manifest.json`
- `public/files/manifests/page_provenance.json`

## Source Review

Reviewed committed upstream source records through `git show HEAD:<path>`:

- `github-facing/research-agent-workflow-explainer.md`
- `github-facing/director-agentjob-lifecycle-explainer.md`
- `research_control/README.md`
- `research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml`
- `research_control/tasks/RT-20260614-249/00_TASK.yaml`
- `research_control/tasks/RT-20260614-249/DDR-20260614-249.md`
- `research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml`
- `research_control/handoffs/handoff-0282.yaml`
- `registries/AGENT_JOB_REGISTRY.csv`

Source conclusion: `AJ-RT-20260614-249-001` is a suitable committed example
for one bounded AgentJob if the page treats it as a permission-envelope
walkthrough. The page must not expose private local details or imply one
AgentJob can settle broad project truth.

## No-AI-Slop Gate

Status: pass.

Reasoning:

- The page explains objective, allowed reads, allowed writes, forbidden
  classes, validators, expected outputs, completion, and handoff.
- It distinguishes public mental model from specialist transaction surfaces.
- It treats PASS as operational evidence only.
- It states that the historical AgentJob is not reusable current permission.
- It avoids private local absolute paths and uses repo-relative committed
  source paths.
- It preserves no coupling-law adoption, no matter-coupling derivation or
  adoption, no `MetricData(E)`, no `g_eff`, no Einstein equations, no
  benchmark promotion, and no completed derivation.

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

Diagram QA note: the first PG-015 diagram render used a horizontal Mermaid
layout that clipped on mobile. The diagram was changed to a vertical flow and
the route figure was given the shared `content-figure` responsive class. The
second browser pass verified the corrected asset.

Curator report note:

- `python3 scripts/run_curator.py --write` refreshed
  `curator/reports/latest.json` and `curator/reports/latest.md`.
- `npm run validate:curator` then failed only on the known 16 ontology
  TeX/PDF critical source-drift records listed below.

## Browser QA

Target:

- `http://127.0.0.1:4322/project/ai-research-agent-system/one-bounded-agentjob/`

Desktop screenshot:

- `output/playwright/sitewide-revamp-pg015-one-agentjob-static-desktop-2026-06-28.png`

Mobile screenshot:

- `output/playwright/sitewide-revamp-pg015-one-agentjob-static-mobile-2026-06-28.png`

Automated browser checks passed:

- Required text present: `ONE BOUNDED AGENTJOB IN PRACTICE`,
  `AJ-RT-20260614-249-001`, `ALLOWED READS`, `ALLOWED WRITES`,
  `FORBIDDEN CLASSES`, `VALIDATORS`, `EXPECTED OUTPUTS`, `Completion`,
  `Handoff`, `Safe summary`, `UNSAFE SUMMARY`, `not reusable authority`,
  `not broad project truth`, `PASS is operational evidence`,
  `no coupling-law adoption`, `no matter-coupling derivation or adoption`,
  `no MetricData(E)`, `no g_eff`, and `Source authority`.
- No console errors.
- No page errors.
- No broken loaded images.
- No `/Volumes/` text leakage.
- Desktop document horizontal overflow: 0.
- Mobile document horizontal overflow: 0.

Visual review:

- Desktop layout is readable.
- Mobile layout is readable.
- The corrected vertical diagram scales inside its container.
- Long source refs wrap inside the source notice without creating page-level
  horizontal overflow.

## Known Blocker Outside PG-015

Full curator validation is expected to continue failing on known ontology
TeX/PDF critical source drift until those derivative/source pairs are
reconciled. PG-015 did not alter that blocker.

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

PG-015 is technically complete for local review. The logical next step is to
continue with PG-016.
