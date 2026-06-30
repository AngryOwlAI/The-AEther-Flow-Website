# AEther Flow Source Project Functionality Inventory System Analysis

## Purpose

This analysis answers a repository-recovery question: whether a saved list
already exists that inventories all major functionality, features, components,
and systems implemented or used by
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.

The finding is precise. A single source-repository master inventory was not
found during this review. Closest existing artifacts are:

- `README.md`, which includes a project map, operating commands, and the two
  research tracks.
- `FOLDER_MAP.md`, which is a generated folder classification, not canonical
  authority and not a feature-level explanation.
- `registries/*.csv`, which are the machine-checkable source, task, role,
  claim-boundary, publication, wiki, and memory indexes.
- `docs/system-analyses/aether-flow-website-topic-inventory.md` in the website
  repository, which inventories website-topic candidates rather than every
  source-project function.

This document therefore provides a new source-grounded functionality inventory.
It is intended for maintainers who need a detailed mental model of what the
source project does and where each function lives.

## Scope And Authority

Scope is the tracked source project at
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`, plus limited website context where
needed to identify the pre-existing website-side topic inventory.

This document is website-maintained explanatory documentation. It is not source
authority for physics, mathematics, governance, routing, validators, role
permissions, publication status, or generated-output status. Upstream source
authority remains in registered TeX files, source registries, registered
Markdown, tracked research-control records, task artifacts, validators, and
human-gated decisions (The AEther Flow, n.d.-a; The AEther Flow, n.d.-c; The
AEther Flow, n.d.-d).

The inventory is comprehensive at the system/functionality level. It does not
line-by-line audit all 480 completed task records or all 4,379 file-object
registry rows. For exact object membership, use the named registries and task
folders.

When future maintainers reuse this inventory, preserve exact project status
fences when they are source-true: `proposal-only`, `draft/control`,
`source-extension`, `fail-closed`, `frozen negative`, `no MetricData(E)`,
`no g_eff`, and `no downstream GR promotion`.

## Evidence Reviewed

- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/AGENTS.md` - root operating
  rules, authority hierarchy, research-control continuation, project-system
  improvement, required checks, and generated-output boundaries.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/README.md` - front-door project
  definition, two-track research model, project map, requirements, memory/wiki
  commands, research-control workflow, and publication explainer list.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/FOLDER_MAP.md` - generated folder
  classification and registry counts by directory.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/README.md` - registry
  role descriptions and authority boundary.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/*.csv` - row counts,
  registry fields, role/status summaries, and source-object indexes.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/README.md` -
  tracked control spine, one-job rule, theoretical continuation gate,
  ontology-law packet route, Distance-to-GR ledger, mathematical-decisiveness
  contract, memory preflight, project-improvement signals, and validation.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/AGENTS.md` -
  scoped continuation, editing, source-extension, and human-gate rules for
  `research_control/`.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/program_state.yaml`
  - current source-control state at inspection time.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/handoffs/handoff-0344.yaml`
  and `.md` - latest tracked handoff at inspection time.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/README.md`
  - design-note subjects and authority boundary.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/gr_derivation_burden_map.md`
  - Distance-to-GR milestone chain and future AgentJob burden contract.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/no_target_import_guard_map.md`
  - no-target-import guard categories and validator boundaries.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/mathematical_decisiveness_completion_contract.md`
  - physics-completion field contract and operational-versus-scientific
  distinction.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/documentation_curator_publication_process.md`
  - active publication process for GitHub Markdown and HTML explainers.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/github_facing_explainer_contract.md`
  - GitHub-facing explainer source-authority contract.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/ontology/aether-and-aether-flow.md`
  - ontology-facing conceptual vocabulary and derivation caveats.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/ontology/tex/README.md` - live
  ontology TeX lane and derivative-PDF boundary.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/scripts/README.md` - script
  group responsibilities.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/scripts/research_control/README.md`
  - research-control script functions.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/scripts/project_control/README.md`
  - project-control script functions.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.agents/schemas/README.md` -
  schema contracts and relationship to templates.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/templates/README.md`
  - reusable control-record templates.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.codex/skills/*/SKILL.md` -
  repo-local skill entry points.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.codex/skills/project-memory-system/scripts/`
  - memory/wiki/registry/PDF/local-retrieval script set.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/Makefile` - validation command
  wrappers.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow/requirements.txt` - Python runtime
  dependency ledger.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/docs/system-analyses/aether-flow-website-topic-inventory.md`
  - prior website-topic inventory, used only to distinguish topic planning
  from source-project functionality inventory.
- `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/docs/project-features-and-functionality.md`
  - website feature map, used only as website context.

## System Context

The source project is a dual research program. One track is a physics program
around The AEther-Flow Interpretation of Relativity: an exact-GR benchmark is
kept as the public observable-scale boundary while first-principles substrate
derivation remains open unless future gates authorize stronger claims. The
second track is an AI research-agent system for theoretical physics work:
roles, tasks, validators, memory, registries, claim gates, publication
surfaces, and project-system maintenance (The AEther Flow, n.d.-b).

The project is not a conventional software application with one runtime entry
point. It is a governed research repository. Its implemented functionality is a
combination of source documents, research-control records, Python validators,
CSV registries, generated derivatives, local retrieval surfaces, role
contracts, Codex skills, publication explainers, and mathematical/physics
task artifacts.

At inspection time, `program_state.yaml` reported active task
`RT-20260629-049`, latest handoff `handoff-0344`, and status
`v12_p5_t01_selects_p5_t02_matter_sector_discriminator_target_no_promotion`.
The latest handoff states that P5-T01 selected P5-T02 matter-semantics target
formalization with no scientific claim promotion. The blocked claims include
canonical ontology edit, source-law adoption, `MetricData(E)` adoption,
`g_eff` adoption or scope expansion, matter-coupling derivation, Einstein
equations, benchmark promotion, completed derivation, future source-extension
impossibility, and global theory rejection (The AEther Flow, n.d.-g; The
AEther Flow, n.d.-h).

## Functionality Or Topic Analysis

### 1. Existing Inventory Finding

No single source-side file was found that functions as an exhaustive
"all project functionality/features/systems" inventory.

The source repo does contain partial and generated maps:

- `README.md` gives the human front door, project map, command surfaces,
  tracked publication explainers, memory/wiki description, and workflow
  overview.
- `FOLDER_MAP.md` classifies folders into `canonical source`, `archival
  source`, `control authority`, `generated derivative`, `local retrieval`,
  `tooling`, and `reserved lane`, but it explicitly says it is generated and
  not canonical authority.
- The CSV registries are the most complete machine-readable inventory. They
  record 480 completed research tasks, 480 AgentJobs, 480 Director decisions,
  481 active claim-boundary rows, 33 role rows, 169 Markdown source rows, 261
  TeX source rows, 16 PDF derivative rows, 17 HTML explainer rows, 463 wiki
  artifact rows, 463 content-semantic rows, and 4,379 file-object rows at the
  time of inspection.
- The website repo has `docs/system-analyses/aether-flow-website-topic-inventory.md`,
  but that file is a website planning inventory, not a complete source-project
  functionality list.

Conclusion: the list the user remembers may have survived indirectly as the
website-topic inventory and as distributed registry/folder-map evidence, but a
single source-project master functionality inventory did not appear in the
source repo during this inspection.

### 2. Top-Level Repository System Families

The source repo is organized into these major functional families:

| Family | Main paths | Functionality |
| --- | --- | --- |
| Project identity and instructions | `README.md`, `AGENTS.md`, `.agents/AGENTS.md`, `research_control/AGENTS.md` | Defines project mission, authority hierarchy, operating rules, research-control boundaries, and generated-output policy. |
| Physics ontology and exact-GR benchmark | `ontology/`, `ontology/tex/`, `ontology/pdfs/`, `legacy_ontology/`, `tex_shared/` | Maintains live ontology TeX sources, generated PDFs, archival ontology snapshots, and shared TeX inputs. |
| Research-control state machine | `research_control/`, `research_control/tasks/`, `research_control/handoffs/`, `research_control/templates/` | Tracks tasks, Director decisions, AgentJobs, execution roles, completions, handoffs, approvals, templates, and active program state. |
| Control design notes | `research_control/design/` | Defines Distance-to-GR burden map, mathematical-decisiveness contract, documentation process, no-target-import guards, graph schema, and related governance contracts. |
| Registries | `registries/` | Provides machine-checkable CSV authority for source objects, derivatives, tasks, jobs, roles, decisions, claim boundaries, signals, relationships, memory objects, and publication briefs. |
| Agent roles and schemas | `.agents/roles/`, `.agents/schemas/` | Defines reusable role contracts and schema documentation for research-control objects. |
| Repo-local skills and prompts | `.codex/skills/`, `.codex/prompts/`, `.codex/agents/` | Implements Codex operating skills for continuation, project improvement, memory, wiki generation, PDFs, publication explainers, and human-edited diff intake. |
| Project-control and research-control scripts | `scripts/`, `scripts/project_control/`, `scripts/research_control/` | Automates validators, resolvers, classifiers, memory preflight, checkpointing, graph/frontier rendering, and finite model checks. |
| Generated/publication explainers | `markdown/publication-briefs/`, `markdown/html-explainer-specs/`, `github-facing/`, `html/` | Maintains reviewed source-backed Markdown/HTML explainer publication pipeline. |
| Generated memory/wiki surfaces | `wiki/`, `.local/obsidian/`, `.local/content_semantics/`, `.local/memory_index/`, `output/` | Provides generated metadata notes, semantic extracts, Obsidian vault, local index, dependency graph outputs, and local retrieval support. |
| Tests and validation harness | `tests/`, `Makefile`, `requirements.txt` | Provides unit tests, validation command wrappers, and a minimal Python dependency ledger. |
| Planning/reserved/review lanes | `implementations_plans/`, `PRDs/`, `reviews/`, `manuscripts/`, `assets/`, `Step-by-step-Comments/` | Holds plans, future/reserved lanes, review assets, manuscript placeholders, images, and local notes. |

### 3. Physics And Ontology Functionality

The physics subsystem implements the project-specific source material and the
tracked derivation-burden framework.

- Live ontology TeX lane: `ontology/tex/` contains eight registered canonical
  TeX sources for foundations, geometry, dynamics, relativistic recovery,
  consistency, exact closure, sequence overview, and flagship article material.
  These files are the live scientific source lane when claim status allows it
  (The AEther Flow, n.d.-i).
- Live ontology PDF derivatives: `ontology/pdfs/` contains generated
  human-readable PDFs for the same ontology package. PDFs are generated
  derivatives and do not outrank registered TeX.
- Legacy ontology snapshot: `legacy_ontology/tex/` and `legacy_ontology/pdfs/`
  preserve a 2026-06-18 archival state for comparison. Registry rows mark this
  lane as archival noncanonical.
- Ontology-adjacent Markdown: `ontology/aether-and-aether-flow.md` states the
  conceptual vocabulary around `AEther`, `AEther-flow`, observed space,
  `S-time`, observed expansion, and gravity-as-reorganization framing while
  explicitly preserving the open derivation burden (The AEther Flow, n.d.-j).
- Exact-GR benchmark boundary: the README states that observable-scale physics
  remains ordinary GR with one operative Lorentzian metric, universal matter
  coupling, standard causal structure, and the same empirical content expected
  from ordinary GR; a first-principles derivation remains open (The AEther
  Flow, n.d.-b).
- Distance-to-GR milestone chain: `gr_derivation_burden_map.md` defines
  source ontology, `EqSrc`, `ObsLoc_lc`, `Resp_lc`, `M_src`, `g_eff`, matter
  coupling, Einstein equations, benchmark promotion, Gate Chair status, and
  finite toy response milestones. The ledger mirror is
  `registries/DISTANCE_TO_GR_LEDGER.csv`.
- Current source-state ledger: the ledger currently includes accepted or
  scoped source-extension statuses for some upstream objects, but the current
  handoff preserves no `MetricData(E)` adoption, no `g_eff` scope change in
  the current P5-T01 step, no matter-coupling derivation, no Einstein
  equations, and no benchmark promotion.
- Source-extension discipline: source extension is a controlled category,
  not an informal permission to import target-GR structures.
- No-target-import guards: `no_target_import_guard_map.md` names forbidden
  imports including target topology, target smooth atlas, target metric,
  empirical observer protocol, benchmark success, generated derivative
  authority, registry laundering, validator laundering, role laundering,
  handoff laundering, and file-order laundering (The AEther Flow, n.d.-k).
- Mathematical decisiveness contract: future opted-in physics completions
  must separate validator PASS from physics progress through explicit fields
  such as `physics_progress_status`, `distance_to_gr_delta`,
  `mathematical_payload_manifest`, and `forbidden_conclusion_summary` (The
  AEther Flow, n.d.-l).
- Negative-result preservation: obstruction and freeze criteria preserve
  stopped or repeated-burden routes without turning a scoped obstruction into
  global theory rejection.
- Finite/local model support: scripts and task artifacts include finite source
  cover and finite local candidate checkers, checker replay reports, finite
  graph witness checkers, and related property tests.
- Current P5 matter-semantics boundary: `handoff-0344` selects a P5-T02
  matter-semantics target formalization task only. It blocks interpreting that
  selection as stress-energy semantics, stress-energy tensor construction,
  detector semantics, matter action, coupling-law adoption, Einstein
  equations, or benchmark progress.

### 4. Research-Control Functionality

The research-control subsystem is the operational spine of the repo.

- Program state: `research_control/program_state.yaml` stores mode, active
  task, latest handoff, current status, claim-boundary summary, and next
  recommended action.
- Task folders: `research_control/tasks/RT-*` store task-local Director
  decisions, AgentJobs, execution-role records, artifacts, completions,
  parent/child records, validation evidence, and documentation-impact
  receipts.
- Director Decision Records: DDR files record routing decisions, selected
  role identity, decision type, and why other roles or routes were rejected.
- AgentJobs: job YAML files define allowed reads, allowed writes, output
  paths, validators, source restrictions, claim boundaries, and stop
  conditions.
- Execution-role records: role records under task folders bind a registered
  role, task overlay, or one-job provisional role to a specific job.
- Completion records: completion YAML files record what happened, validation
  status, command evidence, physics-progress fields, claim boundaries,
  signals, and handoff information.
- Handoffs: `research_control/handoffs/handoff-####.yaml` and `.md` preserve
  continuation state and next actions. The current tracked latest handoff
  inspected here is `handoff-0344`.
- One-job rule: `/continue-research` may set up or execute at most one
  bounded AgentJob per invocation.
- Parent-child parallel synthesis: physics AgentJobs after the activation date
  use one outer AgentJob with internal parent/child analytical synthesis. The
  children are not separate authority lanes or separate jobs.
- Theoretical continuation selector: when the next step is a theoretical
  choice, the project routes a bounded selector job rather than stopping at
  generic controlled pause.
- Ontology-law research packet route: `ontology-law-research-packet` is a
  named route for `derivation_critical_missing_source_law` and explicitly not
  for ordinary documentation gaps or workflow inconvenience.
- Human-gated authority: Gate Chair and protected human decisions control
  benchmark promotion, canonical ontology adoption, and other protected
  claim-promotion steps.
- Project-improvement bridge: research completions may emit
  `project_improvement_signals`. The normal research handoff remains
  continuation authority, while a separate sidecar can route through
  `/improve-project-system`.
- Missing-source-law inventory: `research_control/missing_laws/` stores the
  missing-law inventory YAML/Markdown pair for routing one derivation-critical
  law at a time through existing continuation machinery.
- Templates: `research_control/templates/` stores templates for tasks, DDRs,
  AgentJobs, execution roles, completions, approvals, handoffs,
  project-improvement handoffs, and parent-child conflict reviews.
- Approvals: `research_control/approvals/` stores human authorization records
  where needed.
- Formalization support: `research_control/formalization/` is a control
  support lane for formalization-related artifacts.
- Current frontier and graph renderers: `research_control/current_frontier.md`
  and `output/research_dependency_graph.*` are generated or rendered views
  supporting navigation, not independent authority.

### 5. Role, Agent, And Schema Functionality

The project implements a role-governed research-agent architecture.

- Active science roles include Director of Research, Ontology Formalizer,
  Candidate Constructor, Refuter, Smuggling Auditor, Theoretical Continuation
  Selector, and Gate Chair.
- Active project-system roles include Documentation Curator,
  Project-Control Maintainer, Project-System Director, Validator Engineer,
  Memory-System Maintainer, and Process Integrity Auditor.
- Role versions are tracked. Superseded versions remain in `.agents/roles/`
  and in the role registry for provenance.
- `AGENT_ROLE_REGISTRY.csv` records 33 role rows at inspection time, including
  active and superseded versions, role kinds, authority levels, autonomous
  execution flags, write-source flags, and validator defaults.
- The role system distinguishes registered roles, task overlays, and
  one-job provisional roles. The inspected registries show 313 task-overlay
  Director decisions, 164 existing-role decisions, and 3 provisional-role
  decisions.
- Schema files under `.agents/schemas/` define record shape and authority
  constraints for Director decisions, AgentJobs, execution roles, role
  contracts, documentation impact, project-improvement handoffs, and physics
  completion decisiveness.
- Schemas are project-control authority. Templates are scaffolding. Active
  authority comes from completed task-local records, registered rows, role
  contracts, validators, and human gates.

### 6. Registry Functionality

Registries are the source graph's machine-checkable memory and provenance
system. At inspection time, the key CSV registries contained:

| Registry | Rows | Implemented function |
| --- | ---: | --- |
| `RESEARCH_TASK_REGISTRY.csv` | 480 | Tracks tasks, task paths, type, status, current DDR/job, parent task, and dates. |
| `DIRECTOR_DECISION_REGISTRY.csv` | 480 | Tracks DDRs, decision types, selected role, selected job, status, and supersession links. |
| `AGENT_JOB_REGISTRY.csv` | 480 | Tracks jobs, task IDs, completion paths, allowed write paths, output paths, validators, and status. |
| `ROLE_EXECUTION_REGISTRY.csv` | 480 | Tracks concrete execution-role records, task overlays, registered-role uses, and provisional roles. |
| `CLAIM_BOUNDARY_REGISTRY.csv` | 481 | Tracks allowed claims, forbidden claims, gate requirements, authority source paths, and active claim boundaries. |
| `AGENT_ROLE_REGISTRY.csv` | 33 | Tracks role contracts, versions, role kinds, authority levels, statuses, permissions, and default validators. |
| `DISTANCE_TO_GR_LEDGER.csv` | 14 | Tracks GR-derivation milestones, required objects, current statuses, blockers, acceptance criteria, and last evidence. |
| `MARKDOWN_SOURCE_REGISTRY.csv` | 169 | Tracks Markdown source objects, role contracts, source specs, publication briefs, design notes, guidance, and generated Markdown derivatives. |
| `TEX_SOURCE_REGISTRY.csv` | 261 | Tracks ontology TeX, legacy TeX snapshots, and science draft/control TeX artifacts. |
| `PDF_DERIVATIVE_REGISTRY.csv` | 16 | Tracks ontology and legacy ontology PDF derivatives. |
| `HTML_EXPLAINER_REGISTRY.csv` | 17 | Tracks generated noncanonical HTML explainers. |
| `PUBLICATION_BRIEF_REGISTRY.csv` | 17 | Tracks reviewed publication briefs, source specs, GitHub Markdown outputs, HTML outputs, source materials, and review state. |
| `PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv` | 12 | Defines allowed improvement signal types and default routing roles/skills. |
| `PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv` | 6 | Tracks concrete project-improvement signals and resolution metadata. |
| `FILE_OBJECT_REGISTRY.csv` | 4,379 | Tracks file objects across source, generated, and retrieval surfaces. |
| `OBJECT_RELATIONSHIP_REGISTRY.csv` | 2,527 | Tracks object relationships used by generated memory/wiki surfaces. |
| `WIKI_ARTIFACT_REGISTRY.csv` | 463 | Tracks generated wiki Markdown notes. |
| `CONTENT_SEMANTIC_REGISTRY.csv` | 463 | Tracks content-semantic extracts. |
| `OBSIDIAN_VAULT_REGISTRY.csv` | 463 | Tracks generated local Obsidian vault notes. |

Registry functionality includes provenance tracking, source/derivative
separation, generated-output tracking, queryable memory, task state indexing,
publication-surface validation, and claim-boundary enforcement.

### 7. Memory, Wiki, And Retrieval Functionality

The project implements a source-first memory system.

- Bootstrap refresh: `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
  regenerates or validates registry/wiki/memory surfaces.
- PDF derivative build: `build_pdf_derivatives.py` builds managed PDFs from
  registered TeX into derivative lanes.
- Content semantics: `extract_content_semantics.py` produces generated
  semantic extracts for registered source objects.
- Obsidian vault generation: `init_obsidian_vault.py`,
  `sync_obsidian_vault.py`, and `lint_obsidian_vault.py` support a generated
  local vault under `.local/obsidian/aether-flow-wiki/`.
- Memory index: `build_memory_index.py` and `query_memory.py` provide local
  query/status/lookup/search functions.
- Local retrieval boundary: `.local/` caches, semantic extracts, Obsidian
  notes, and SQLite indexes are retrieval aids only and remain non-authority.
- Wiki generation: `wiki/markdown/`, `wiki/tex/`, `wiki/pdf/`, `wiki/html/`,
  and `wiki/indexes/` provide generated metadata notes and indexes.
- Folder mapping: `FOLDER_MAP.md` is generated from live tree plus registries
  and classifies folders for humans and agents.
- Relationship graph: `OBJECT_RELATIONSHIP_REGISTRY.csv` and
  `output/research_dependency_graph.*` expose generated graph-oriented
  navigation surfaces.
- Memory preflight: continuation workflows require memory status and at least
  one targeted lookup/search before routing decisions, with canonical source
  inspection after any useful memory hit.

### 8. Script And Validator Functionality

The script system is split into root-level scripts, project-control scripts,
and research-control scripts.

Root-level scripts:

- `scripts/enhance_html_explainers.py` supports generated HTML explainer
  enhancement.
- `scripts/spec_depth_lint.py` validates publication/source-spec depth.
- `scripts/validate_publication_process.py` validates public documentation
  source grounding, authority boundaries, no-network HTML, publication brief
  conformance, orphan outputs, duplicate skeletons, and known anti-patterns.

Project-control scripts:

- `classify_project_changes.py` classifies Git changes for documentation
  impact and project-system routing.
- `resolve_project_improvement.py` reports advisory project-improvement
  routing state.
- `collect_project_improvement_signals.py` validates emitted signals against
  the signal registries.
- `generate_project_improvement_handoff.py` creates deterministic
  project-improvement sidecar YAML/Markdown pairs.
- `validate_documentation_impact.py` checks documentation-impact receipts.
- `audit_documentation_surfaces.py` audits registered documentation surfaces,
  source hashes, derivatives, and local retrieval surfaces.
- `project_improvement_handoff_validation.py` supplies sidecar schema and
  parity checks.
- `project_signal_types.py` reads allowed signal-type vocabulary from the
  registry.

Research-control scripts:

- `continue_research.py` resolves the next bounded continuation packet.
- `continue_research_memory_preflight.py` runs the required memory preflight
  refresh/status path.
- `resolve_latest_handoff.py` resolves latest handoff state.
- `validate_research_control.py` validates task records, registries,
  handoffs, parent-child synthesis constraints, claim boundaries, and diff
  allowlists.
- `checkpoint_research_transaction.py` regenerates, validates, stages, and
  commits bounded transactions.
- `strict_yaml.py` provides deterministic YAML parsing for control records.
- `render_current_frontier.py` renders current-frontier views.
- `render_dependency_graph.py` renders dependency graph outputs.
- `report_physics_progress_metrics.py` reports separated operational and
  scientific-progress metrics.
- `finite_source_cover_model_checker.py` and
  `mechanized_checks/check_finite_local_candidate.py` support finite/local
  checker paths.
- `source_manifold_types.py` supports source-manifold data typing.

Validation wrappers:

- `make validate-memory` refreshes memory, syncs the Obsidian vault, lints the
  vault, runs tests, and smoke-tests memory queries.
- `make validate-project-control` runs project-control classification, signal
  validation, documentation impact validation, documentation-surface audit,
  bootstrap validation, spec-depth linting, research-control validation, diff
  validation, and tests.
- `make validate-html-explainers` runs bootstrap validation and publication
  depth checks.
- `make audit-documentation-surfaces` audits documentation surfaces.

Implementation risk found during this inventory: `Makefile` references
`scripts/validate_teaching_qa.py`, but that file was not present in the
inspected root `scripts/` listing. This should be treated as a command-surface
drift item until confirmed or repaired.

### 9. Publication And Explainer Functionality

The project implements a governed source-backed publication system for human
and GitHub-facing explainers.

- Publication briefs: `markdown/publication-briefs/` contains 17 reviewed
  publication briefs. The registry says all 17 are `reviewed`.
- Source specs: `markdown/html-explainer-specs/` contains matching Markdown
  source specs for tracked explainers.
- GitHub-facing Markdown: `github-facing/` contains 17 source-backed,
  noncanonical reader surfaces.
- HTML explainers: `html/` contains 17 generated noncanonical, human-only
  standalone HTML explainers.
- Publication brief registry: `PUBLICATION_BRIEF_REGISTRY.csv` is the active
  control surface for reviewed public GitHub Markdown and HTML publication
  pages.
- Documentation Curator process: the active publication process requires
  page-specific reader jobs, document type, narrative strategy, visual
  strategy, source basis, acceptance criteria, and forbidden patterns.
- Retired process boundary: the topic-registry/Visual Atlas/teaching-packet
  path is not the active creation path for public pages.
- GitHub-facing contract: GitHub pages may orient readers and cite source
  files, but they must not define physics claims, alter control behavior,
  replace registries, or become independent authority.
- No-network HTML requirement: tracked HTML must be standalone, mobile-safe,
  no-network, readable without JavaScript, and grounded in visible source
  paths.
- Reviewed explainer subjects include project overview, source authority,
  physics program, ontology, exact-GR benchmark boundary, GR derivation
  roadmap, claim gates, research-agent workflow, Director/AgentJob lifecycle,
  parent-child synthesis, role routing, documentation publication process,
  project-system improvement, memory system, roles and skills, validator
  workflow, and technical requirements.

### 10. Repo-Local Skill Functionality

The source repo includes repo-local Codex skills:

- `continue-research`: resolves tracked research-control state and sets up or
  executes one bounded AgentJob per invocation.
- `improve-project-system`: resolves project-system reliability/governance
  work without performing physics derivation or claim promotion.
- `user-modified-project`: integrates human-made local repository edits
  through classification, routing, registry/wiki refresh, and validation.
- `project-memory-system`: owns memory, registry, wiki, PDF derivative,
  cleanup, and validation scripts.
- `markdown-wiki`: front door for generated Markdown wiki metadata and
  indexes.
- `tex-wiki`: front door for TeX-source metadata notes and TeX registry
  validation.
- `obsidian-wiki`: front door for the generated local Obsidian vault,
  semantic extraction, relationship graph, and query surface.
- `pdf-derivative-build`: builds registered project PDFs from registered TeX
  sources into derivative lanes.
- `html-visual-explainer`: governs tracked standalone HTML publication
  explainers.
- `visual-explainer`: generates local visual explanation pages and vendored
  prompt templates; public deployment requires separate review.
- `ontology-promotion`: governs ontology-promotion packet boundaries.
- `grill-me` and `grill-with-docs`: structured planning/interview skills.

The skill system is tooling. It does not replace source authority, validators,
role contracts, or human gates.

### 11. Testing And QA Functionality

The `tests/` folder covers:

- memory-system smoke checks;
- Obsidian wiki behavior;
- publication-process validation;
- HTML explainer enhancement;
- spec-depth linting;
- documentation-surface audit;
- project-change classification;
- project-improvement bridge behavior;
- research-control validation;
- current-frontier rendering;
- dependency-graph rendering;
- finite source-cover model checking;
- finite local candidate checking and property tests;
- source-manifold types.

The tests are software/project-system evidence. They do not establish physics
truth, theorem validity, source-law adoption, or benchmark promotion.

### 12. Dependency And Runtime Functionality

The project uses a deliberately small runtime surface:

- Python virtual environment under `.venv/`.
- Python version noted in README as Python 3.12.13 in `.venv/`.
- `requirements.txt` currently lists PyMuPDF `>=1.27,<1.28` for direct PDF
  text extraction in the local semantic memory system.
- Codex app is the current governed AI-agent harness for continuation,
  project-system, skill, role, and memory workflows.
- Node.js/npm/Playwright Chromium are used by the vendored Mermaid/visual
  explainer tooling when diagram-backed HTML rendering is in scope.
- LaTeX/PDF tooling is used when TeX derivative builds are in scope.
- Git is required for repo state, checkpointing, diffs, commits, and source
  history inspection.

### 13. Generated, Derivative, And Local Surfaces

The repo deliberately tracks or generates several non-authority surfaces:

- `html/*.html`: generated human-only HTML explainers.
- `github-facing/*.md`: generated or derivative noncanonical GitHub reader
  surfaces backed by publication briefs/source specs.
- `wiki/*`: generated metadata notes and indexes.
- `ontology/pdfs/*.pdf` and `legacy_ontology/pdfs/*.pdf`: generated PDF
  derivatives from TeX.
- `output/research_dependency_graph.*`: generated dependency graph outputs.
- `.local/obsidian/aether-flow-wiki/`: generated local vault.
- `.local/content_semantics/`: generated semantic extracts.
- `.local/memory_index/`: local retrieval index.
- `.local/pdf_qa/`, `.local/render_qa/`, `.local/title_page_qa/`: local QA
  and scratch outputs.

These surfaces are useful, but they must not be treated as independent
scientific or governance authority.

### 14. Planning, Reserved, And Support Lanes

The repo includes support lanes whose authority varies:

- `implementations_plans/`: implementation plans and project-system plans.
- `PRDs/`: reserved lane for future project requirements material.
- `reviews/`: reserved review lane.
- `manuscripts/`: reserved or future manuscript lane.
- `assets/images/`: README and project images.
- `Step-by-step-Comments/`: local retrieval/reference lane, not tracked
  authority.
- `output/playwright/`: QA output lane.

Where these lanes are unregistered or marked reserved, they should not be
treated as active source authority without a registry row or task record.

## Mermaid Diagram

Visual grammar: cylinders are source or registry stores; rectangles are
implemented operational systems; diamonds are gates or authority decisions;
dashed arrows are generated, derivative, local retrieval, or provenance-only
relationships; solid arrows are primary governed flows. Cyan nodes are source
or canonical stores, orange nodes are control/governance systems, blue nodes
are operational/tooling bridges, green nodes are reader-facing or generated
outputs, and dashed orange nodes mark authority boundaries or risk controls.

```mermaid
---
config:
  theme: base
  themeVariables:
    darkMode: true
    background: "#000000"
    primaryColor: "#050403"
    primaryTextColor: "#fff8ef"
    primaryBorderColor: "#d6c3b4"
    lineColor: "#d6c3b4"
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "16px"
    clusterBkg: "#080401"
    clusterBorder: "#d6c3b4"
    edgeLabelBackground: "#000000"
---
flowchart TD
  root[(README / AGENTS / instructions)]
  ontology[(Ontology TeX sources)]
  registries[(CSV registries)]
  control[Research-control spine]
  roles[Role contracts and schemas]
  scripts[Validators and scripts]
  skills[Repo-local Codex skills]
  memory[Memory, wiki, vault, semantic index]
  publication[Publication briefs, specs, GitHub Markdown, HTML]
  gates{Claim gates and human authority}
  outputs([Generated reader and retrieval surfaces])
  boundary{"Source authority boundary"}
  current([Current state and handoffs])

  root --> control
  ontology --> registries
  control --> registries
  roles --> control
  skills --> control
  scripts --> control
  scripts --> registries
  registries --> memory
  registries --> publication
  control --> current
  control --> gates
  gates --> current
  memory -. retrieval only .-> boundary
  publication -. noncanonical reader surface .-> boundary
  outputs -. generated derivative .-> boundary
  boundary -. verify source .-> ontology
  boundary -. verify registry row .-> registries

  classDef default fill:#050403,stroke:#d6c3b4,color:#fff8ef,stroke-width:1.5px;
  classDef source fill:#0f364d,stroke:#48a0c0,color:#fff8ef,stroke-width:2px;
  classDef control fill:#270b01,stroke:#f87800,color:#fff8ef,stroke-width:2px;
  classDef bridge fill:#164964,stroke:#f4d6a1,color:#fff8ef,stroke-width:2px;
  classDef decision fill:#702000,stroke:#f87800,color:#fff8ef,stroke-width:2.25px;
  classDef target fill:#2d7ea0,stroke:#f4d6a1,color:#ffffff,stroke-width:2px;
  classDef risk fill:#702000,stroke:#f87800,color:#fff8ef,stroke-width:2px,stroke-dasharray: 5 5;
  classDef boundary fill:#000000,stroke:#f87800,color:#fff8ef,stroke-width:3px,stroke-dasharray: 5 5;

  class root,ontology,registries source;
  class control,roles,gates current control;
  class scripts,skills,memory bridge;
  class publication,outputs target;
  class boundary boundary;

  linkStyle default stroke:#d6c3b4,stroke-width:2.25px;
```

## Interfaces, Inputs, And Outputs

### Human Interfaces

- `README.md`: front-door project explanation, commands, route into
  publication explainers, and project map.
- `github-facing/*.md`: GitHub-native reader surfaces.
- `html/*.html`: standalone human-only generated visual explainers.
- `ontology/pdfs/*.pdf`: human-readable generated ontology PDFs.
- `wiki/indexes/*.md`: generated browse indexes.
- `.local/obsidian/aether-flow-wiki/`: local Obsidian reading/search surface.

### Agent Interfaces

- `AGENTS.md`, `.agents/AGENTS.md`, `research_control/AGENTS.md`: operating
  instructions.
- `.agents/roles/**/*.md`: role contracts.
- `.agents/schemas/*.md`: schema contracts.
- `.codex/skills/*/SKILL.md`: workflow skills.
- `research_control/program_state.yaml`: live routing state.
- `research_control/handoffs/handoff-####.yaml`: continuation handoffs.
- `registries/*.csv`: source graph and workflow indexes.

### Script Interfaces

- `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json`
- `.venv/bin/python scripts/research_control/continue_research.py`
- `.venv/bin/python scripts/research_control/validate_research_control.py`
- `.venv/bin/python scripts/research_control/validate_research_control.py --check-diff`
- `.venv/bin/python scripts/project_control/classify_project_changes.py --json`
- `.venv/bin/python scripts/project_control/resolve_project_improvement.py --json`
- `.venv/bin/python scripts/project_control/validate_documentation_impact.py`
- `.venv/bin/python scripts/project_control/audit_documentation_surfaces.py --skip-local`
- `.venv/bin/python scripts/validate_publication_process.py --root . --strict`
- `make validate-memory`
- `make validate-project-control`
- `make validate-html-explainers`

### Primary Inputs

- Registered TeX and Markdown source files.
- Human instructions or authorized task packets.
- Program state and latest handoff.
- Existing task artifacts and completions.
- Registry rows and source hashes.
- Git diff/status.
- Local generated memory surfaces, as navigation only.

### Primary Outputs

- New or updated task records.
- Director decisions.
- AgentJobs and execution-role records.
- TeX or Markdown task artifacts.
- Completion records.
- Handoffs.
- Registry updates.
- Generated wiki/semantic/vault surfaces.
- Generated PDFs, GitHub Markdown, and HTML explainers when authorized.
- Validation receipts and checkpoint commits.

## Risks, Failure Modes, And Claim Boundaries

- Inventory overclaim risk: folder presence does not prove active
  functionality. This inventory relies on registries, READMEs, scripts, and
  source-control records instead of directory names alone.
- Generated-derivative overclaim risk: PDFs, HTML, wiki notes, Obsidian notes,
  and semantic extracts are useful but non-authoritative.
- Validator laundering risk: validator PASS proves operational conformity, not
  theorem truth, source-law adoption, `M_src`, `g_eff`, matter coupling,
  Einstein equations, benchmark promotion, or completed derivation.
- Registry laundering risk: registry rows provide provenance and routing
  metadata, not proof by themselves.
- Handoff laundering risk: handoffs summarize state and next action; they do
  not independently prove physics claims.
- Role laundering risk: role identity and task routing do not grant physics
  truth or human-gated authority.
- Current-state drift risk: `program_state.yaml` and latest handoff are
  time-sensitive. This analysis inspected `handoff-0344` on 2026-06-29.
- Worktree risk: the source repo was on `main...origin/main [ahead 21]` with
  an untracked `research_control/tasks/RT-20260629-050/` directory during this
  inspection. This inventory therefore avoided writing into the source repo.
- Command drift risk: `Makefile` references `scripts/validate_teaching_qa.py`,
  but that file was not present in the inspected root `scripts/` directory.
- Exhaustiveness limitation: the inventory covers implemented system families
  and interfaces, but it does not individually summarize all 480 task artifacts
  or all 261 TeX registry rows. The registries remain the exact object index.

## Open Questions

- Was the remembered early project list originally created in a local,
  untracked, or external artifact outside both repos? This review cannot
  exclude that possibility.
- Should this new inventory be promoted into the source repo itself after the
  source repo's dirty state is intentionally handled?
- Should the dangling `scripts/validate_teaching_qa.py` Makefile reference be
  repaired, removed, or restored through a project-system AgentJob?
- Should a generated machine-readable inventory be added later, sourced from
  the registries, so this human inventory and the live object graph cannot
  drift?

## Logical Next Step

The logical next step is to decide whether this inventory should remain a
website-maintained system analysis or be promoted into the source repository as
a canonical or registered Markdown source. Promotion into the source repo should
not happen casually: it should use the source repo's controlled documentation
or project-system workflow, inspect the current dirty worktree, and update any
required registry/wiki surfaces through the approved bootstrap path.

An improvement will be to add a small script that produces a machine-readable
functionality index from `registries/*.csv`, `FOLDER_MAP.md`, role contracts,
skill contracts, and script READMEs, then links this human analysis to the
generated index.

## References

The AEther Flow. (n.d.-a). `AGENTS.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/AGENTS.md`.

The AEther Flow. (n.d.-b). `README.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/README.md`.

The AEther Flow. (n.d.-c). `registries/README.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/registries/README.md`.

The AEther Flow. (n.d.-d). `research_control/README.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/README.md`.

The AEther Flow. (n.d.-e). `FOLDER_MAP.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/FOLDER_MAP.md`.

The AEther Flow. (n.d.-f). `research_control/program_state.yaml`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/program_state.yaml`.

The AEther Flow. (n.d.-g). `research_control/handoffs/handoff-0344.yaml`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/handoffs/handoff-0344.yaml`.

The AEther Flow. (n.d.-h). `research_control/handoffs/handoff-0344.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/handoffs/handoff-0344.md`.

The AEther Flow. (n.d.-i). `ontology/tex/README.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/ontology/tex/README.md`.

The AEther Flow. (n.d.-j). `ontology/aether-and-aether-flow.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/ontology/aether-and-aether-flow.md`.

The AEther Flow. (n.d.-k). `research_control/design/no_target_import_guard_map.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/no_target_import_guard_map.md`.

The AEther Flow. (n.d.-l).
`research_control/design/mathematical_decisiveness_completion_contract.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/mathematical_decisiveness_completion_contract.md`.

The AEther Flow. (n.d.-m).
`research_control/design/gr_derivation_burden_map.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/gr_derivation_burden_map.md`.

The AEther Flow. (n.d.-n).
`research_control/design/documentation_curator_publication_process.md`.
Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/documentation_curator_publication_process.md`.

The AEther Flow. (n.d.-o).
`research_control/design/github_facing_explainer_contract.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/research_control/design/github_facing_explainer_contract.md`.

The AEther Flow. (n.d.-p). `scripts/README.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/scripts/README.md`.

The AEther Flow. (n.d.-q). `scripts/research_control/README.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/scripts/research_control/README.md`.

The AEther Flow. (n.d.-r). `scripts/project_control/README.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/scripts/project_control/README.md`.

The AEther Flow Website. (n.d.-a).
`docs/system-analyses/aether-flow-website-topic-inventory.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/docs/system-analyses/aether-flow-website-topic-inventory.md`.

The AEther Flow Website. (n.d.-b).
`docs/project-features-and-functionality.md`. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/docs/project-features-and-functionality.md`.
