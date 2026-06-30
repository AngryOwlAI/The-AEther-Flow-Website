---
prd_id: "PRD-07"
title: "Tooling, Skills, Scripts, and Runtime Components"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Technical requirements, skills catalogue, script catalogue, validator/operator workflow, Makefile reference, runtime environment, reproducibility, and local-cache boundaries"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-03-research-control-and-agent-workflow.md"
  - "PRD-04-role-and-schema-components.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
  - "PRD-10-website-positioning-guidance.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-07: Tooling, Skills, Scripts, and Runtime Components

## 1. Summary

This PRD defines how The AEther Flow Website should explain the tooling,
skills, scripts, validators, runtime requirements, reproducibility workflow,
and local-cache boundary used by The AEther Flow Project. It covers technical
requirements pages, skills catalogues, script catalogues, validator/operator
workflow pages, Makefile command references, runtime environment pages, and
reproducibility guides.

The central product rule is that tooling pages must show what each command,
skill, script, validator, or runtime dependency does and what it does not do.
Operational tools can validate structure, state, provenance, and reproducible
workflow behavior. They must not be presented as proof engines, scientific
promotion mechanisms, or substitutes for tracked source authority.

## 2. Product Purpose

The AEther Flow Project is unusually tooling-rich because it is both a physics
research project and an AI research-agent system. Readers need a clear,
bounded explanation of how operators reproduce the project state, run
validators, inspect source-backed memory, understand repo-local skills, and
avoid overclaiming from green checks.

The website should help readers understand:

- why the Codex app is the current governed AI-agent harness;
- which repo-local skills are entry points for continuation, project-system
  repair, memory, visual explainers, and human edit integration;
- which scripts operate research-control state versus project-control state;
- what Makefile targets group into repeatable operator workflows;
- which runtime requirements are necessary for Python, memory, PDF, diagram,
  Playwright, and LaTeX/PDF work;
- where validation evidence, documentation-impact evidence, completion
  evidence, screenshots, and checkpoints are recorded;
- why `.local/`, Obsidian notes, semantic extracts, generated wiki notes, and
  local caches remain retrieval support rather than authority.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, routing, tooling, runtime, validator, or
claim-promotion authority.

Source basis for implementation should include:

- `.codex/skills/`;
- `.codex/skills/continue-research/SKILL.md`;
- `.codex/skills/improve-project-system/SKILL.md`;
- `.codex/skills/project-memory-system/SKILL.md`;
- `.codex/skills/html-visual-explainer/SKILL.md`;
- `.codex/skills/visual-explainer/SKILL.md`;
- `.codex/skills/user-modified-project/SKILL.md`;
- `.codex/skills/markdown-wiki/SKILL.md`;
- `.codex/skills/obsidian-wiki/SKILL.md`;
- `.codex/skills/tex-wiki/SKILL.md`;
- `.codex/skills/pdf-derivative-build/SKILL.md`;
- `.codex/skills/ontology-promotion/SKILL.md`;
- `scripts/research_control/README.md`;
- `scripts/research_control/`;
- `scripts/project_control/README.md`;
- `scripts/project_control/`;
- `Makefile`;
- `requirements.txt`;
- `tests/README.md`;
- `tests/`;
- `README.md`;
- `FOLDER_MAP.md` when topology and local-cache boundaries are in scope.

Tracked skills, scripts, Makefile targets, requirements, test READMEs, and
control documentation are source basis for tooling explanations. Website
pages, PRDs, generated explainers, local memory, wiki notes, Obsidian notes,
semantic extracts, screenshots, and `.local/` caches remain explanatory,
retrieval, or QA evidence unless a higher-authority tracked source says
otherwise.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand that validators and tooling make the workflow auditable but do not prove physics. |
| Contributor | Learn the minimum setup, common validation commands, and where evidence is recorded before proposing work. |
| Operator | Reproduce validation, memory, publication, and checkpoint workflows without bypassing authority boundaries. |
| AI researcher | Inspect how skills, scripts, validators, memory preflight, and checkpoint gates shape the research-agent system. |
| Site builder | Build technical pages that explain command behavior without turning implementation details into public claims. |
| Reviewer | Trace what a tool checked, what it did not check, and which source artifact remains authoritative. |

## 5. Scope

In scope:

- technical requirements page requirements;
- skills catalogue requirements;
- script catalogue requirements;
- validator/operator workflow page requirements;
- Makefile command reference requirements;
- runtime environment page requirements;
- reproducibility guide requirements;
- local-cache boundary requirements;
- command scope and non-scope language requirements;
- evidence-location and checkpoint-expectation requirements.

Out of scope:

- changing upstream skills, scripts, validators, Makefile targets, runtime
  dependencies, tests, caches, or control workflows;
- implementing public routes in this packet;
- refreshing source snapshots, memory, wiki, Obsidian, semantic extracts, PDF
  derivatives, or HTML explainers;
- adding dependencies;
- changing validation behavior;
- promoting or weakening any scientific, mathematical, governance, or
  research-workflow claim;
- pushing or deploying.

## 6. Non-Goals

This PRD must not:

- claim that validators prove theorem correctness, derivation success, source
  ontology adoption, benchmark promotion, or scientific truth;
- present tests as substitutes for source inspection, human gates, or tracked
  approvals;
- imply that the Codex app harness is permanent or irreplaceable;
- present generated HTML, GitHub-facing Markdown, wiki notes, PDFs, Obsidian
  notes, semantic extracts, or `.local/` caches as source authority;
- turn command references into instructions to bypass AgentJob allowlists,
  documentation-impact receipts, human gates, or checkpoint scripts;
- imply that local runtime setup grants write permission to upstream source
  files.

## 7. Website Surfaces

Required surfaces:

- Technical requirements page;
- Skills catalogue;
- Script catalogue;
- Validator/operator workflow page;
- Makefile command reference;
- Runtime environment page;
- Reproducibility guide;
- Local cache boundary explainer.

Supporting surfaces:

- command scope matrix;
- "what this validates / what this does not validate" cards;
- minimum setup checklist;
- evidence-location map;
- validator versus proof warning component;
- skill-to-role and skill-to-script relationship map;
- runtime dependency tier table;
- generated versus source artifact warning panel.

## 8. Functional Requirements

1. Explain the Codex app harness as the current governed AI-agent execution
   environment while stating that read-only inspection, normal Git use, and
   Python validators can run outside Codex.
2. Explain that future harness replacement would need to preserve tracked
   state, authority hierarchy, role boundaries, allowlists, validator gates,
   checkpoint discipline, and generated-derivative boundaries.
3. Explain the `continue-research` skill as the research-control continuation
   workflow for memory preflight, tracked-state resolution, Director decisions,
   one bounded AgentJob, validation, completion, handoff, regeneration, and
   checkpointing.
4. Explain the `improve-project-system` skill as the project-system repair
   workflow for roles, schemas, validators, control Markdown, memory tooling,
   generated-document pipelines, and reliability.
5. Explain the `project-memory-system` skill as the owner of memory, registry,
   wiki, Obsidian, PDF-derivative, cleanup, and validation scripts.
6. Explain the `html-visual-explainer` workflow as the governed tracked-HTML
   publication path based on publication briefs and Markdown source specs.
7. Explain the `visual-explainer` skill as local visual documentation support,
   with tracked publication delegated to the governed HTML explainer path.
8. Explain the `user-modified-project` skill as the router for human-made
   local edits into the proper controlled workflow.
9. Explain Markdown, Obsidian, TeX, PDF, and ontology-support skills as
   format-specific support workflows that do not bypass source authority.
10. Explain research-control scripts, including continuation, latest-handoff
    resolution, validation, checkpointing, current-frontier rendering, physics
    progress metrics, dependency graph rendering, strict YAML parsing, and
    finite-source checks.
11. Explain project-control scripts, including change classification,
    project-improvement resolution, signal collection, handoff generation,
    sidecar validation, documentation-impact validation, documentation-surface
    audit, and signal-type reading.
12. Explain memory bootstrap and query tools, including bootstrap refresh,
    validate-only mode, Obsidian sync, vault lint, memory status, lookup, and
    search.
13. Explain validators and tests as deterministic reliability checks, not
    proof or claim-promotion mechanisms.
14. Explain Makefile targets as operator convenience wrappers around existing
    validation and memory workflows.
15. Explain the Python runtime requirement, including `.venv`, Python 3.12.13
    as the documented local runtime, `requirements.txt`, and PyMuPDF for PDF
    text extraction in local semantic memory.
16. Explain diagram and screenshot tooling requirements only where governed
    visual publication or browser QA is in scope.
17. Explain `.local/` as ignored local retrieval, vault, preview, semantic,
    and experiment state that may be refreshed or cleaned but is not source
    authority.
18. For every command page, state what the command validates or changes and
    what it does not validate or change.
19. For contributor paths, show minimum setup, common validation commands, and
    where evidence is recorded.
20. For operator paths, identify which workflows require a completion record,
    documentation-impact record, handoff, screenshot QA, registry row,
    checkpoint, or explicit human gate.

## 9. Non-Functional Requirements

- Accuracy: Tooling pages must be reviewed against current source skills,
  script READMEs, Makefile targets, requirements, and test documentation.
- Safety: Validator and test pages must place non-proof language next to
  positive validation descriptions.
- Reproducibility: Command pages should include preconditions, expected
  evidence outputs, and common failure interpretation.
- Maintainability: Pages should describe command families and source locations
  rather than copying long script internals.
- Boundary clarity: Source, derivative, retrieval, QA, and cache artifacts
  must be visually distinct.
- Security and integrity: Pages must not encourage manual edits to generated
  artifacts, bypassing allowlists, or treating local caches as committed
  evidence.
- Portability: Runtime pages should distinguish documented current setup from
  future possible harnesses or runtimes.

## 10. Claim Boundary

This PRD may specify website content that explains:

- the Codex app as the current governed execution harness;
- repo-local skills as workflow procedures;
- scripts as deterministic tooling;
- validators and tests as operational checks;
- Makefile targets as convenience wrappers;
- Python, PyMuPDF, Node, Mermaid, Playwright, Obsidian, and LaTeX/PDF tooling
  as runtime requirements when relevant;
- `.local/` as retrieval/cache support.

This PRD must not authorize website content claiming:

- tooling, validators, tests, generated outputs, screenshots, local caches, or
  successful checkpoints prove physics claims;
- command execution promotes source laws, benchmark status, `M_src`, `g_eff`,
  matter coupling, Einstein equations, or completed derivation;
- a skill can override role contracts, AgentJob allowlists, human gates, or
  source authority;
- local runtime setup creates write authority;
- generated or cached artifacts are independent authority.

## 11. Content Requirements

The skills catalogue must include at least:

| Skill | Reader explanation | Boundary |
| --- | --- | --- |
| `continue-research` | Continues tracked research-control through memory preflight, Director routing, one AgentJob, validators, completions, handoffs, and checkpointing. | Does not bypass roles, gates, allowlists, or source authority. |
| `improve-project-system` | Routes one bounded repair or clarification to project-system roles for validators, schemas, control Markdown, memory tooling, or generated-document pipelines. | Does not perform physics derivation or promote claims. |
| `project-memory-system` | Builds, validates, queries, syncs, lints, and cleans memory, registry, wiki, Obsidian, and derivative metadata systems. | Retrieval layers and generated artifacts remain non-authoritative. |
| `html-visual-explainer` | Governs tracked standalone HTML publication from publication briefs and Markdown source specs. | Direct HTML-only edits are blocked for normal publication work. |
| `visual-explainer` | Creates local visual explanation artifacts and supports governed visual strategy. | Local `.local/` outputs are explanatory scratch artifacts unless separately governed. |
| `user-modified-project` | Integrates human-made edits through classification, routing, validation, refresh, and checkpoint discipline. | Does not bypass `continue-research`, `improve-project-system`, generated-surface rules, or AgentJob allowlists. |
| Markdown, Obsidian, TeX, PDF, ontology skills | Maintain format-specific generated surfaces or controlled source workflows. | Generated derivatives do not become source authority. |

The script catalogue must include at least:

| Script family | Includes | Boundary |
| --- | --- | --- |
| Research-control scripts | `continue_research.py`, `resolve_latest_handoff.py`, `validate_research_control.py`, `checkpoint_research_transaction.py`, `report_physics_progress_metrics.py`, `render_current_frontier.py`, `render_dependency_graph.py`, `strict_yaml.py`, finite-source checks. | Enforce tracked state but do not replace Director decisions, AgentJob allowlists, role contracts, or human gates. |
| Project-control scripts | `classify_project_changes.py`, `resolve_project_improvement.py`, `collect_project_improvement_signals.py`, `generate_project_improvement_handoff.py`, `project_improvement_handoff_validation.py`, `validate_documentation_impact.py`, `audit_documentation_surfaces.py`, `project_signal_types.py`. | Classifier and resolver output is routing evidence; checkpoint validity is decided by validators, receipts, allowlists, and checkpoint gates. |
| Memory scripts | `bootstrap_memory_system.py`, `query_memory.py`, `sync_obsidian_vault.py`, `lint_obsidian_vault.py`, `clean_local_noise.py`, and related builders. | Generated memory and retrieval outputs support navigation and verification, not claim promotion. |
| Tests | Python unit tests under `tests/`. | Passing tests are behavior evidence, not scientific authority. |

Every command reference must use this structure:

```text
Command:
Purpose:
Inputs:
Writes, if any:
Evidence produced:
Validates:
Does not validate:
Authority boundary:
Common failure interpretation:
```

The Makefile reference must cover:

- `validate-memory`;
- `validate-project-control`;
- `validate-html-explainers`;
- `audit-documentation-surfaces`.

The runtime page must include:

- read/inspect tier: browser, text editor, and Git;
- governed workflow tier: Codex app plus repo-local skills, prompts, and
  agent configuration;
- validator and memory tier: Python `.venv`, `requirements.txt`, and PyMuPDF;
- memory/wiki/registry refresh tier: bootstrap and `make validate-memory`;
- diagram-backed HTML tier: Node.js, npm, Mermaid dependencies, and Playwright
  Chromium when visual publication work is in scope;
- optional local retrieval tier: Obsidian reader plus `.local/obsidian/`;
- LaTeX/PDF tier when TeX derivatives are in scope.

The local-cache boundary page must state:

- `.local/` is ignored repository-local state;
- `.local/` may contain content semantics, Obsidian notes, memory indexes,
  render QA, PDF QA, and local HTML wikis;
- local cache data can guide inspection but cannot be cited as source
  authority;
- authoritative claims require tracked source files, registries, approvals,
  role contracts, schemas, tasks, completions, handoffs, or publication briefs
  as applicable.

## 12. UX and Navigation Requirements

Tooling navigation should:

- begin with a non-proof warning before command details;
- group skills, scripts, validators, Make targets, runtime dependencies, and
  cache boundaries into distinct families;
- use command cards for individual commands only when each card includes
  "validates" and "does not validate";
- link research-control tooling back to PRD-03 workflow concepts;
- link role ownership and authority back to PRD-04;
- link generated derivative and memory boundaries back to PRD-05;
- link source paths and repository location details forward to PRD-08 and
  PRD-11;
- keep GitHub/source links available as provenance but make internal website
  routes the primary reader path;
- avoid encouraging readers to run broad mutating commands without first
  checking task authority and write allowlists.

Recommended reader path:

| Reader | First path |
| --- | --- |
| General reader | Validator versus proof warning to skills overview. |
| Contributor | Minimum setup to common validation to evidence-location map. |
| Operator | Workflow selector to command reference to checkpoint evidence. |
| AI researcher | Skills catalogue to script catalogue to memory preflight model. |
| Site builder | PRD-07 to PRD-03, PRD-04, PRD-05, PRD-08, and PRD-11. |

## 13. Data, Source, and Provenance Requirements

Future tooling pages should declare:

- source artifacts used;
- command or skill source path;
- whether the artifact is source, generated derivative, local cache, QA
  evidence, or explanatory derivative;
- whether a command writes files or only validates;
- required runtime preconditions;
- evidence output location;
- whether the command belongs to research-control, project-control, memory,
  publication, test, runtime, or local-cache families;
- whether an AgentJob, documentation-impact record, human gate, or checkpoint
  is required before or after the command.

Tooling pages should avoid copying full scripts or long command internals.
They should link to source files and explain stable behavior, inputs, outputs,
and boundaries.

## 14. User Stories

1. As a contributor, I want a minimum setup and validation guide, so that I can
   inspect and validate work without guessing which runtime is required.
2. As an operator, I want command pages that say what a command validates and
   what it does not validate, so that I can interpret failures and passes
   correctly.
3. As an AI researcher, I want a skills-to-scripts map, so that I can evaluate
   the research-agent architecture as a controlled system.
4. As a site builder, I want tooling requirements tied to source authority, so
   that future pages do not overstate validator evidence.
5. As a reviewer, I want local caches and generated derivatives classified, so
   that I can tell retrieval support from source authority.
6. As a general reader, I want tooling explained without developer-only
   assumptions, so that I understand why the project is auditable but still
   scientifically cautious.

## 15. Acceptance Criteria

- The technical requirements page explains Codex app, Python `.venv`,
  `requirements.txt`, PyMuPDF, diagram tooling, optional Obsidian, and LaTeX/PDF
  tiers when relevant.
- The skills catalogue includes the required skills and states each skill's
  boundary.
- The script catalogue distinguishes research-control, project-control, memory,
  and test scripts.
- Every command page says what the command validates and what it does not
  validate.
- Validator pages never imply proof, derivation, source-law adoption, benchmark
  promotion, or claim promotion.
- Contributor paths show minimum setup, common validation, and where evidence
  is recorded.
- The Makefile reference describes each target as a wrapper over source
  commands rather than a separate authority layer.
- The runtime page distinguishes current documented setup from future possible
  harness replacement.
- The local-cache page states that `.local/`, Obsidian, semantic extracts, and
  local memory are retrieval support, not authority.
- Tooling pages link to PRD-03, PRD-04, PRD-05, PRD-08, and PRD-11 where their
  concepts depend on workflow, role, provenance, topology, or source-map
  context.

## 16. Dependencies

- PRD-00 defines the master source-authority model and information
  architecture.
- PRD-03 defines Director decisions, AgentJobs, validators, completions,
  handoffs, and checkpoint concepts.
- PRD-04 defines roles, schema contracts, and authority boundaries.
- PRD-05 defines memory, registry, generated derivative, retrieval, and
  provenance boundaries.
- PRD-09 defines freshness-sensitive examples for current-state command
  references.
- PRD-10 defines safe public language and forbidden claims.
- PRD-08 will define repository topology and folder-family orientation.
- PRD-11 will define a concise source map for future page builders.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Validator PASS is mistaken for scientific proof. | Require adjacent "does not validate" and non-proof language on every command page. |
| Command references become unsafe operating instructions. | Include preconditions, write behavior, evidence outputs, and authority boundaries. |
| Local caches are treated as committed evidence. | Require a local-cache boundary page and classify `.local/` as ignored retrieval support. |
| Tooling pages drift from actual source commands. | Review against skill files, script READMEs, Makefile, requirements, and tests before implementation. |
| Runtime setup appears to grant write authority. | State that runtime capability and AgentJob authority are separate. |
| Makefile targets are treated as independent gates. | Describe them as wrappers around existing validators and memory scripts. |
| Generated HTML or visual explainer output is treated as source. | Link back to publication briefs, source specs, and PRD-05 derivative boundaries. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Check every command page for "validates" and "does not validate" fields.
2. Confirm all skill names and script names against current source files.
3. Confirm Makefile targets against the current `Makefile`.
4. Confirm runtime dependency descriptions against `README.md` and
   `requirements.txt`.
5. Search rendered copy for validator-as-proof, test-as-proof, cache-as-proof,
   and generated-derivative-as-authority language.
6. Confirm mutating commands identify required AgentJob, allowlist,
   documentation-impact, checkpoint, or human-gate context where applicable.
7. Confirm local-cache pages classify `.local/` and Obsidian/semantic outputs
   as retrieval support.
8. Run applicable route, content, provenance, build, browser, and
   implementation-control validators for implementation packets.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: implementation support foundation.

This PRD should follow PRD-03 and PRD-04 because tooling explanations need the
workflow lifecycle and role/schema authority model first. It should precede
PRD-08 and PRD-11 because topology and source-map pages should link tool and
runtime concepts to where they live in the repository.

## 20. Open Questions

1. Should command references be generated from source command metadata or kept
   as manually reviewed Markdown with a source-inspection date?
2. Should the contributor path include a single "safe read-only" command set
   before any mutating workflow is shown?
3. Should validator pages include recent example failures, or should examples
   be kept in PRD-09-style freshness snapshots?
4. Should runtime pages distinguish website repo requirements from upstream
   source-project requirements when both are shown in one public information
   architecture?

These questions do not block this PRD. They should be resolved during PRD-08,
PRD-11, or future route implementation planning.

## 21. Definition of Done

This PRD is complete when:

- it defines technical requirements, skills catalogue, script catalogue,
  validator/operator workflow, Makefile reference, runtime environment,
  reproducibility, and local-cache boundary requirements;
- it covers all required tooling and runtime components from the PRD-system
  plan;
- it requires every command page to say what the command validates and does not
  validate;
- it prevents validators, tests, generated derivatives, screenshots,
  checkpoints, and caches from being presented as scientific proof;
- it gives future contributor/operator pages testable requirements for setup,
  common validation, and evidence recording.

## References

The AEther Flow Project. (2026). *Continue research skill* [Skill contract].

The AEther Flow Project. (2026). *HTML visual explainer skill* [Skill
contract].

The AEther Flow Project. (2026). *Improve project system skill* [Skill
contract].

The AEther Flow Project. (2026). *Makefile* [Operator command surface].

The AEther Flow Project. (2026). *Project-control scripts README* [Technical
documentation].

The AEther Flow Project. (2026). *Project memory system skill* [Skill
contract].

The AEther Flow Project. (2026). *README* [Project documentation].

The AEther Flow Project. (2026). *Research-control scripts README* [Technical
documentation].

The AEther Flow Project. (2026). *Requirements* [Runtime dependency ledger].

The AEther Flow Project. (2026). *Tests README* [Technical documentation].

The AEther Flow Project. (2026). *User-modified project skill* [Skill
contract].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].

The AEther Flow Website. (2026). *Role and Schema Components* [Product
requirements document].

The AEther Flow Website. (2026). *Research-Control and Agent Workflow*
[Product requirements document].

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].
