# Dual-Project Public Overview Follow-On Phase 0 Audit

Status: Phase 0 complete pending acceptance
Date: 2026-06-25
Plan: `ImplementationPlans/dual_project_public_overview_followon_implementation_plan.md`
Scope: evidence refresh and route audit only

## Analysis

Phase 0 was audit-only. The upstream source repository was available at
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`, and the project-explainer scanner
completed successfully. No implementation route, component, or style file was
changed in this phase.

The current website baseline supports the accepted public overview, research
map, resource scaffold pages, and math-rendering sample pages. It does not yet
contain the follow-on track landing pages or deeper public reading-path pages.

## Scanner Evidence

Command run:

```bash
python .codex/skills/project-explainer-frontend/scripts/scan_project_story.py \
  --repo . \
  --source-root /Volumes/P-SSD/AngryOwl/The-AEther-Flow \
  --out-dir scratch/project-explainer
```

Generated outputs:

- `scratch/project-explainer/project_story_brief.md`
- `scratch/project-explainer/project_story_brief.json`

Result:

- Source root available: `True`.
- Likely frontend stack: Astro static site, Astro MDX, TypeScript, CSS, and
  KaTeX rendering.
- Scanner guidance remains advisory. Public copy in later phases must inspect
  upstream source files directly before making source-backed claims.

## Current Website Routes

Current route files under `src/pages`:

| Route | File | Current role |
| --- | --- | --- |
| `/` | `src/pages/index.astro` | Home and publication-layer orientation scaffold. |
| `/project/overview/` | `src/pages/project/overview.astro` | Accepted dual-track public overview. |
| `/research/map/` | `src/pages/research/map.astro` | Website source-authority to static reader-surface map. |
| `/research/equations/` | `src/pages/research/equations.mdx` | KaTeX and equation rendering reference. |
| `/research/math-sample/` | `src/pages/research/math-sample.mdx` | Minimal MDX math rendering sample. |
| `/resources/` | `src/pages/resources/index.astro` | Manifest-backed resource scaffold; explicitly sample/source-index oriented. |
| `/resources/documents/` | `src/pages/resources/documents.astro` | PDF and TeX sample asset index. |
| `/resources/diagrams/` | `src/pages/resources/diagrams.astro` | Diagram orientation asset gallery. |

Relevant shared surfaces:

- `src/components/SourceNotice.astro`
- `src/layouts/BaseLayout.astro`
- `src/layouts/TechnicalPageLayout.astro`
- `src/lib/siteContent.ts`

## Missing Planned Routes

The planned reading path requires the following routes, none of which exists
yet in the website repository:

| Planned route | Planned phase | Status |
| --- | --- | --- |
| `/project/physics/` | Phase 2 | Missing. |
| `/project/ai-research-agent-system/` | Phase 2 | Missing. |
| `/project/source-authority/` | Phase 3 | Missing. |
| `/project/physics/ontology/` | Phase 4A | Missing. |
| `/project/physics/exact-gr-benchmark/` | Phase 4B | Missing. |
| `/project/physics/gr-derivation-roadmap/` | Phase 4C | Missing. |
| `/project/physics/claim-gates/` | Phase 4D | Missing. |
| `/project/ai-research-agent-system/workflow/` | Phase 5A | Missing. |
| `/project/ai-research-agent-system/roles-and-skills/` | Phase 5B | Missing. |
| `/project/ai-research-agent-system/memory-registries/` | Phase 5C | Missing. |
| `/project/ai-research-agent-system/validator-operator-workflow/` | Phase 5D | Missing. |

## Overview CTA Baseline

The accepted overview currently points:

- "Explore physics research" to `/resources/documents/`.
- "Explore the AI research system" to the external GitHub repository.

That is acceptable as the current baseline. Phase 2 should update those CTAs
only after the two first-class track landing pages exist.

## Upstream Source Evidence

Direct source inspection confirmed the upstream README supports the public
dual-track framing:

- Physics track: AEther / AEther-flow ontology, exact-GR benchmark boundary,
  open derivation burden, and negative-result preservation.
- AI research-agent track: human-scaffolded workflow, role-based routing,
  claim gates, review/refutation discipline, memory/wiki/registry surfaces,
  and separation between workflow state and physics proof.
- Human visual explainers are reviewed public reader surfaces but remain
  generated noncanonical derivatives.

The upstream publication registry confirms reviewed GitHub-facing and HTML
explainer surfaces for the planned page families. Those explainers are useful
orientation material, but their own source-authority footers state that they do
not become canonical authority.

## Sources To Inspect Before Phase 2 Copy

Before writing the Phase 2 physics track page, inspect:

- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/README.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/aether-flow-physics-program-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/aether-flow-ontology-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/exact-gr-benchmark-boundary-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/gr-derivation-roadmap-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/claim-gates-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/ontology/aether-and-aether-flow.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/gr_derivation_burden_map.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/TEX_SOURCE_REGISTRY.csv`

Before writing the Phase 2 AI research-agent track page, inspect:

- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/README.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/AGENTS.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/README.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/research-agent-workflow-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/roles-and-skills-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/memory-system-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/validator-operator-workflow-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/github-facing/source-authority-explainer.md`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/AGENT_ROLE_REGISTRY.csv`
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/PUBLICATION_BRIEF_REGISTRY.csv`

## Route Naming Concerns

The proposed Phase 2 routes are sound:

- `/project/physics/`
- `/project/ai-research-agent-system/`

Reasoning:

- Both routes live under the accepted `/project/` family.
- The physics route is concise and general enough to hold the first landing
  page without implying a completed derivation.
- The AI route uses the plan-approved phrase "AI research-agent system" and
  avoids implying an autonomous AI scientist.

No route rename is recommended for Phase 2. The only naming concern is link
discipline: do not point public CTAs to deeper planned routes until those
routes exist or are visibly marked as planned.

## Validation

Validation performed in Phase 0:

- Project-explainer scanner completed successfully.
- Current route inventory was inspected under `src/pages`.
- Upstream README and first-layer GitHub-facing explainers were inspected.
- `git status --short` was checked before writing this audit and showed no
  implementation page changes.

Build, browser, and strict frontend audit were not run because Phase 0 made no
public page implementation changes.

## Phase 0 Conclusion

Phase 0 is complete pending acceptance. The logical next step is Phase 1:
define shared route/content metadata and source-notice defaults without
creating new public route pages.

## References

AEther-Flow Project. (2026). `README.md` [Project front door, dual-track
research-program framing, exact-GR benchmark boundary, open derivation burden,
and AI research-agent system overview].

AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv`
[Reviewed public explainer registry and source-material bindings].

The AEther Flow Website. (2026).
`ImplementationPlans/dual_project_public_overview_followon_implementation_plan.md`
[Phased follow-on implementation plan].

The AEther Flow Website. (2026). `PRDs/dual-project-public-overview-prd.md`
[Accepted dual-project public overview PRD and release acceptance record].

The AEther Flow Website. (2026). `src/pages/project/overview.astro`
[Accepted public overview route].

The AEther Flow Website. (2026). `src/components/SourceNotice.astro`
[Website source-authority notice component].
