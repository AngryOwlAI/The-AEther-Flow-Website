# Sitewide Revamp PG-016 Parent-Child Synthesis QA

## Scope

Packet: PG-016, Rewrite Parent-Child Parallel Synthesis.

Route: `/project/ai-research-agent-system/parent-child-synthesis/`.

Primary files:

- `docs/system-analyses/parent-child-parallel-synthesis-walkthrough.md`
- `docs/content-dossiers/parent-child-synthesis/dossier.md`
- `src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro`
- `src/lib/internalExplainers.ts`
- `public/files/manifests/page_route_map.json`
- `public/files/manifests/page_provenance.json`

Reused diagram assets:

- `docs/content-dossiers/parent-child-synthesis/diagrams/single-outer-agentjob-frame.mmd`
- `public/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png`

## Source Review

Reviewed committed upstream source records through `git show HEAD:<path>`:

- `github-facing/parent-child-synthesis-explainer.md`
- `research_control/README.md`
- `.agents/schemas/AGENT_JOB_SCHEMA.md`
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`
- `registries/AGENT_JOB_REGISTRY.csv`

Reviewed website records:

- `docs/content-dossiers/parent-child-synthesis/dossier.md`
- `docs/content-dossiers/parent-child-synthesis/diagrams/single-outer-agentjob-frame.mmd`

Source conclusion: parent-child synthesis is an internal perspective structure
inside one future physics AgentJob. It preserves one Director decision, one
outer AgentJob, one execution-role record, one completion record, and one fused
output. Parallel perspectives do not create parallel authority.

## No-AI-Slop Gate

Status: pass.

Reasoning:

- The page now foregrounds the one-outer-AgentJob invariant.
- Parent, child, conflict review, and fused output are explained distinctly.
- Child outputs are described as supporting `draft/control` artifacts.
- The page states that child units do not create child AgentJobs, child
  execution-role records, independent verdicts, extra write authority, or
  human-gate bypass.
- Conflict review is explicit: PASS is invalid while a declared blocking
  parent-child conflict remains unresolved.

Subagent note: no subagent was spawned. The available multi-agent tool policy
requires explicit user request before spawning subagents.

## Validation

Passed:

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

Curator report note:

- `python3 scripts/run_curator.py --write` refreshed
  `curator/reports/latest.json` and `curator/reports/latest.md`.
- `npm run validate:curator` then failed only on the known 16 ontology
  TeX/PDF critical source-drift records listed below.

## Browser QA

Target:

- `http://127.0.0.1:4322/project/ai-research-agent-system/parent-child-synthesis/`

Desktop screenshot:

- `output/playwright/sitewide-revamp-pg016-parent-child-static-desktop-2026-06-28.png`

Mobile screenshot:

- `output/playwright/sitewide-revamp-pg016-parent-child-static-mobile-2026-06-28.png`

Automated browser checks passed:

- Required text present: `PARENT-CHILD PARALLEL SYNTHESIS`,
  `one outer AgentJob`, `Child outputs are supporting draft/control artifacts`,
  `Blocking conflicts must be resolved`, `one fused output`, `NO EXTRA JOBS`,
  `NO INDEPENDENT VERDICTS`, `NO CONFLICT BYPASS`, `INHERITED AUTHORITY`,
  `PASS is invalid`, `SAFE SUMMARY`, `UNSAFE SUMMARY`, and `Source authority`.
- No console errors.
- No page errors.
- No broken loaded images.
- No `/Volumes/` text leakage.
- Desktop document horizontal overflow: 0.
- Mobile document horizontal overflow: 0.

Visual review:

- Desktop layout is readable.
- Mobile layout is readable.
- The reused parent-child diagram is visible and not clipped.
- Long source refs wrap inside the source notice without creating page-level
  horizontal overflow.

## Known Blocker Outside PG-016

Full curator validation is expected to continue failing on known ontology
TeX/PDF critical source drift until those derivative/source pairs are
reconciled. PG-016 did not alter that blocker.

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

PG-016 is technically complete for local review. The logical next step is to
continue with PG-017.
