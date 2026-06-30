# The Æther-Flow Research Project: Functionality, Logic, Features, and Systems Catalogue

**Prepared for:** an informational website describing, explaining, and promoting `AngryOwlAI/The-AEther-Flow`.
**Repository examined:** `https://github.com/AngryOwlAI/The-AEther-Flow` on the `main` branch.
**Snapshot basis:** repository README, root agent guidance, ontology sources, research-control documentation, role contracts, schemas, skills, registries, folder map, Makefile, and current frontier files inspected on 2026-06-29.

## Executive Description

The Æther-Flow project is a dual physics-and-AI research program. Its physics track develops **The Æther-Flow Interpretation of Relativity**, where the current public benchmark keeps the observable-scale theory exactly aligned with ordinary general relativity while treating first-principles derivation from an `Æther` / `Æther-flow` ontology as open work.

Its AI track develops a governed, human-scaffolded theoretical-physics research-agent system. That system uses roles, Director decisions, AgentJobs, validation scripts, registries, claim gates, memory tools, handoffs, and generated reader surfaces to make speculative theoretical work auditable instead of foggy.

The website should present the project as a disciplined research program with a strong interpretive physics statement, a clear exact-GR benchmark, and an unusually explicit AI research-control architecture. It should not state that GR has already been derived from the ontology, that the benchmark has been promoted from first principles, or that generated docs, validators, or agent workflow status constitute physics proof.

## Authority and Claim Boundary Summary

- **Canonical physics authority:** registered `.tex` sources under `ontology/tex/` and related source registries.
- **Canonical project-control authority:** `AGENTS.md`, `research_control/`, `.agents/`, `.codex/skills/`, schemas, and registries.
- **Generated reader surfaces:** PDFs, HTML explainers, GitHub-facing Markdown, wiki notes, semantic extracts, Obsidian notes, and `.local/` caches are useful reading or retrieval layers, not independent authority.
- **Core promotional phrasing:** “exact-GR benchmark adoption plus an open first-principles derivation program,” not “completed derivation of GR.”

---

# 1. High-Level Components

## H01. Dual Physics-and-AI Research Program
- **What it is:** A two-track research project combining theoretical physics with AI research-agent methodology.
- **How it works:** The physics track supplies a hard research problem; the AI track supplies auditable workflow for exploring, refuting, repairing, and preserving results.
- **How it connects:** Both tracks meet at the GR derivation burden, where candidate mathematical work is routed through controlled agent roles and claim gates.
- **Source anchors:** `README.md`; `AGENTS.md`; `research_control/README.md`.

## H02. Physics Track
- **What it is:** The physics program studies whether ordinary GR can be interpreted, and eventually derived, from a deeper four-dimensional Æther / Æther-flow ontology.
- **How it works:** Current observable physics remains exactly GR through one operative metric, universal matter coupling, standard causal structure, and Einsteinian dynamics.
- **How it connects:** It gives the agent system a real frontier: construct source-side objects, audit hidden imports, preserve negative results, and avoid premature promotion.
- **Source anchors:** `ontology/`; `ontology/tex/`; `research_control/design/gr_derivation_burden_map.md`.

## H03. AI Research-Agent Track
- **What it is:** A human-scaffolded research-agent system for theoretical physics investigation.
- **How it works:** It routes bounded work through Director decisions, AgentJobs, execution-role records, validators, completions, handoffs, and registries.
- **How it connects:** It turns speculative theory-building into auditable transactions, while reserving scientific promotion for protected gates.
- **Source anchors:** `.agents/`; `.codex/skills/`; `research_control/`.

## H04. Exact-GR Benchmark Package
- **What it is:** The active public physics benchmark where the effective gravitational theory is exactly general relativity.
- **How it works:** It adopts the Einstein-Hilbert action, Einstein equations, one metric, universal matter coupling, null propagation, proper time, and standard GR/SR recovery.
- **How it connects:** It is the benchmark every future extension or derivation must answer to; it is not itself a completed substrate derivation.
- **Source anchors:** `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`; `ontology/tex/aether_flow_exact_closure_note.tex`.

## H05. Æther / Æther-Flow Ontology
- **What it is:** The conceptual foundation: `Æther` as a deeper four-dimensional substrate and `Æther-flow` as its intrinsic ordered motion.
- **How it works:** Observed three-dimensional space, S-time, expansion, and gravity are interpreted as observer-accessible appearances or reorganizations of deeper order.
- **How it connects:** The ontology frames the research goal, but it must be translated into source-side mathematical laws before it can count as derivation.
- **Source anchors:** `ontology/aether-and-aether-flow.md`; `ontology/tex/aether_flow_foundations.tex`.

## H06. Open GR-Derivation Program
- **What it is:** The unresolved research program to recover ordinary GR or the exact-GR benchmark from explicit source-side substrate structure.
- **How it works:** The project decomposes the derivation into milestones: source ontology, source equivalence, localization, response, source manifold, effective metric, matter coupling, Einstein equations, and benchmark promotion.
- **How it connects:** Every future physics AgentJob must name the milestone and burden it advances, preventing vague “progress” from masquerading as proof.
- **Source anchors:** `research_control/design/gr_derivation_burden_map.md`; `registries/DISTANCE_TO_GR_LEDGER.csv`.

## H07. Research-Control Spine
- **What it is:** The tracked operating system for Director-led research continuation.
- **How it works:** It stores tasks, Director Decision Records, AgentJobs, role executions, completions, handoffs, active state, and validation receipts.
- **How it connects:** It is the governance layer between scientific sources, agent roles, generated artifacts, validators, and current frontier state.
- **Source anchors:** `research_control/README.md`; `research_control/program_state.yaml`; `research_control/current_frontier.md`.

## H08. Role-Based Agent Architecture
- **What it is:** A catalog of versioned role contracts for physics work and research-operations work.
- **How it works:** Roles define authority, allowed source classes, validators, output formats, stop conditions, and whether human gates are required.
- **How it connects:** Director decisions bind one AgentJob to a role through an execution-role record, so authority is explicit and task-local.
- **Source anchors:** `.agents/roles/`; `.agents/schemas/ROLE_SCHEMA.md`; `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`.

## H09. Claim Gates and Human-Gated Promotion
- **What it is:** The discipline that separates drafts, candidates, accepted source-side evidence, benchmark promotion, and scientific closure.
- **How it works:** Non-human roles can construct, stress, audit, and recommend, but protected claims require explicit human-gated authority.
- **How it connects:** This protects the project from overclaiming when validators pass, local witnesses exist, or generated documents look polished.
- **Source anchors:** `.agents/roles/physics/gate-chair.v0.1.0.md`; `registries/CLAIM_BOUNDARY_REGISTRY.csv`.

## H10. Source-First Memory System
- **What it is:** A registry-backed memory and retrieval system for project knowledge.
- **How it works:** It indexes registered sources, generated wiki notes, semantic extracts, Obsidian vault notes, PDFs, and relationship records while preserving canonical source precedence.
- **How it connects:** Agents may use memory hits for navigation, but must inspect canonical sources or registry rows before using those hits for routing or claims.
- **Source anchors:** `.codex/skills/project-memory-system/SKILL.md`; `wiki/`; `.local/content_semantics/`; `.local/obsidian/`.

## H11. Registry System
- **What it is:** A CSV-based state and provenance layer for source objects, roles, tasks, decisions, jobs, generated derivatives, and project-improvement signals.
- **How it works:** Registries track object IDs, file paths, authority class, hashes, statuses, relationships, and validation-facing metadata.
- **How it connects:** They make the repository machine-checkable and connect scientific source files to generated derivatives and workflow records.
- **Source anchors:** `registries/`; `FOLDER_MAP.md`; `.codex/skills/project-memory-system/SKILL.md`.

## H12. Generated Reader Surfaces
- **What it is:** Human-facing Markdown, HTML, PDFs, and wiki pages that explain or package authoritative sources.
- **How it works:** Generated outputs must derive from registered source specs, publication briefs, TeX files, or registry rows, and may not be hand-edited as authority.
- **How it connects:** They make the research understandable to readers and external agents while remaining subordinate to source and control layers.
- **Source anchors:** `github-facing/`; `html/`; `ontology/pdfs/`; `wiki/`; `markdown/html-explainer-specs/`.

## H13. Public Documentation and Website-Explainer Layer
- **What it is:** A curated documentation surface for explaining the project to readers, contributors, and external AI systems.
- **How it works:** Publication briefs, Markdown source specs, GitHub-facing Markdown, and no-network HTML explainers define reader jobs and visual strategies.
- **How it connects:** It is the natural foundation for your website, but it should inherit the repo’s source-authority and claim-boundary language.
- **Source anchors:** `markdown/publication-briefs/`; `registries/PUBLICATION_BRIEF_REGISTRY.csv`; `html/`.

## H14. Validation and Checkpoint System
- **What it is:** A deterministic script layer that validates memory, documentation impact, research-control records, generated surfaces, tests, and bounded commits.
- **How it works:** The Makefile and workflow skills call validators before transactions are checkpointed; failures are treated as repair evidence, not as obstacles to bypass.
- **How it connects:** Validation protects role boundaries, registry consistency, generated output freshness, and project-system discipline.
- **Source anchors:** `Makefile`; `scripts/research_control/`; `scripts/project_control/`; `tests/`.

## H15. Project-System Improvement Loop
- **What it is:** A separate maintenance workflow for repairing the research system itself.
- **How it works:** Project-improvement signals, classifiers, resolvers, project-system roles, documentation-impact receipts, and validators process reliability issues one bounded AgentJob at a time.
- **How it connects:** It prevents physics continuation from quietly rewriting tools, roles, schemas, docs, or validators outside its authority.
- **Source anchors:** `.codex/skills/improve-project-system/SKILL.md`; `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`.

## H16. Current Frontier Snapshot
- **What it is:** A generated reader-facing summary of the active research state after the latest tracked handoff.
- **How it works:** It reports active task, handoff, milestone, burden, blocked claims, Distance-to-GR rows, and next recommended action from tracked authority.
- **How it connects:** It helps the website explain current status, but authority remains with `program_state.yaml`, the latest handoff, and the Distance-to-GR ledger.
- **Source anchors:** `research_control/current_frontier.md`; `research_control/program_state.yaml`; `registries/DISTANCE_TO_GR_LEDGER.csv`.

---

# 2. Low-Level Physics and Mathematical Components

## P01. Ontological Core Vocabulary
- **What it is:** The basic conceptual dictionary: Æther, Æther-flow, observed three-dimensional space, S-time, and observed expansion.
- **How it works:** The vocabulary disciplines the project’s ontology by rejecting naive three-dimensional medium or vector-wind interpretations.
- **How it connects:** Later mathematical work must translate this vocabulary into explicit source-side laws before derivational claims can be made.
- **Source anchors:** `ontology/aether-and-aether-flow.md`; `ontology/tex/aether_flow_foundations.tex`.

## P02. Four-Dimensional Substrate Claim
- **What it is:** The claim that the deepest proposed reality layer is a four-dimensional substrate, not ordinary observed three-space.
- **How it works:** The substrate is represented minimally as a differentiable arena with ordered motion, while avoiding premature claims about full dynamics.
- **How it connects:** It supplies the starting object for future derivation attempts such as observer readout, source manifold construction, and effective metric generation.
- **Source anchors:** `ontology/tex/aether_flow_foundations.tex`.

## P03. Æther-Flow as Ordered Motion
- **What it is:** The intrinsic ordered motion of the Æther, treated as ontological structure rather than an observed wind.
- **How it works:** Flow language may be modeled by congruence-like or kinematic proxies, but those are disciplined dictionaries rather than extra low-energy fields.
- **How it connects:** The flow interpretation later maps into expansion, acceleration, vorticity, and shear in exact GR geometry.
- **Source anchors:** `ontology/tex/aether_flow_foundations.tex`; `ontology/tex/aether_flow_geometry.tex`.

## P04. Observed Space as Local Experiential Slice
- **What it is:** The idea that observed three-dimensional spatial relations are local observer-accessible slices of deeper substrate structure.
- **How it works:** The foundations paper sketches induced or experienced spatial geometry without claiming a finished emergent-geometry theorem.
- **How it connects:** This motivates the observer-normal/readout burden and prevents the ontology from collapsing into ordinary spatial ether language.
- **Source anchors:** `ontology/aether-and-aether-flow.md`; `ontology/tex/aether_flow_foundations.tex`.

## P05. S-Time
- **What it is:** S-time is the experienced order of change arising from matter, light, and Æther-flow.
- **How it works:** It is not treated as a second spatial corridor or hidden container, but as an observer-level ordering relation.
- **How it connects:** Any successful derivation must eventually explain clock behavior and Einsteinian closure without smuggling target metric structure.
- **Source anchors:** `ontology/aether-and-aether-flow.md`; `ontology/tex/aether_flow_foundations.tex`.

## P06. Observed Expansion Interpretation
- **What it is:** The project interprets observed cosmic expansion as three-dimensional appearance of deeper ordered motion.
- **How it works:** In the exact-GR benchmark, cosmological behavior remains standard GR, with expansion represented through relativistic geometry rather than external-container imagery.
- **How it connects:** Flow geometry later identifies expansion with congruence expansion, especially the FLRW relation `theta = 3H`.
- **Source anchors:** `ontology/aether-and-aether-flow.md`; `ontology/tex/aether_flow_geometry.tex`.

## P07. Gravity as Mass-Shaped Reorganization
- **What it is:** A heuristic ontology-level picture where matter reorganizes nearby Æther-flow and gravity is the observer-level effect.
- **How it works:** The repo treats this as interpretive and underselective, not as a completed equation-level derivation.
- **How it connects:** It motivates the missing response-soldering and equivalence-locking laws required by future derivational work.
- **Source anchors:** `ontology/aether-and-aether-flow.md`.

## P08. Exact-Closure Theory Definition
- **What it is:** The active theory statement where effective gravitational dynamics are exactly those of GR with ordinary matter coupling.
- **How it works:** The exact effective action uses Einstein-Hilbert gravity plus `S_matter[g, psi]`, producing the usual Einstein equations.
- **How it connects:** This exact-closure theory is the operational floor and reversion target for future extensions.
- **Source anchors:** `ontology/tex/aether_flow_exact_closure_note.tex`; `ontology/tex/aether_flow_dynamics.tex`.

## P09. Einstein-Hilbert Effective Action
- **What it is:** The mathematical action used by the exact benchmark: gravitational Einstein-Hilbert term plus universally coupled matter action.
- **How it works:** Variation with respect to the effective metric yields the standard Einstein field equations and stress tensor definition.
- **How it connects:** It fixes all low-energy predictions and prevents new ontology language from adding untested gravitational sectors.
- **Source anchors:** `ontology/tex/aether_flow_dynamics.tex`; `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`.

## P10. One Operative Metric
- **What it is:** The project’s exact benchmark uses one operational Lorentzian metric for geometry, matter, null propagation, and proper time.
- **How it works:** Matter couples to the same metric, and observed causal and clock structure are inherited from standard GR.
- **How it connects:** This blocks bimetric, preferred-frame, or extra-vector interpretations at the active benchmark level.
- **Source anchors:** `ontology/tex/aether_flow_exact_closure_note.tex`; `ontology/tex/aether_flow_relativistic_recovery.tex`.

## P11. Universal Matter Coupling
- **What it is:** The exact benchmark couples ordinary matter universally to the effective metric.
- **How it works:** This preserves standard GR matter behavior and the equivalence structure needed for tested relativistic physics.
- **How it connects:** Deriving universal matter coupling from source-side ontology remains an open milestone, not an already closed result.
- **Source anchors:** `ontology/tex/aether_flow_dynamics.tex`; `research_control/design/gr_derivation_burden_map.md`.

## P12. No Independent Low-Energy Non-GR Signature
- **What it is:** The active package makes no independent low-energy prediction beyond ordinary GR.
- **How it works:** Novelty is interpretive and architectural: exact closure, ontology discipline, congruence dictionary, and governed derivation workflow.
- **How it connects:** This is central for website accuracy, because the project promotes a deeper interpretation without claiming experimentally distinct low-energy gravity.
- **Source anchors:** `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`; `ontology/tex/aether_flow_exact_closure_note.tex`.

## P13. Dark-Energy Completion Inside Exact Closure
- **What it is:** The exact benchmark can include a cosmological constant or GR-compatible dark-energy stress tensor within the same one-metric theory.
- **How it works:** Dark energy stays on the adopted GR side and does not derive the Einstein sector from ontology.
- **How it connects:** It makes the cosmological benchmark complete without altering the adoption-versus-derivation boundary.
- **Source anchors:** `ontology/tex/aether_flow_exact_closure_note.tex`; `ontology/tex/aether_flow_dynamics.tex`.

## P14. Weak-Field and PPN Recovery
- **What it is:** The benchmark reproduces the standard weak-field line element and GR post-Newtonian content.
- **How it works:** The Newtonian limit emerges in the ordinary way, with `gamma_PPN = 1` and the standard Poisson equation in the slow-motion regime.
- **How it connects:** It demonstrates that the observer-facing weak-field sector is inherited from exact GR, not from a new ether force law.
- **Source anchors:** `ontology/tex/aether_flow_relativistic_recovery.tex`; `ontology/tex/aether_flow_exact_closure_note.tex`.

## P15. Relativistic Recovery
- **What it is:** The module explaining exact recovery of GR/SR phenomena at the observer-facing level.
- **How it works:** Null propagation, proper time, redshift, clock behavior, local inertial structure, and weak-field behavior are all inherited from the same metric.
- **How it connects:** It bridges the ontology to tested physics while keeping the deeper substrate derivation explicitly unfinished.
- **Source anchors:** `ontology/tex/aether_flow_relativistic_recovery.tex`.

## P16. Effective Consistency Analysis
- **What it is:** The consistency module showing that the adopted exact-closure sector has ordinary GR gauge and mode structure.
- **How it works:** Around admissible backgrounds, it uses diffeomorphism gauge redundancy and standard perturbative analysis to preserve the two tensor modes of GR.
- **How it connects:** It supports the benchmark’s role as a healthy effective theory while not claiming a completed substrate degree-of-freedom analysis.
- **Source anchors:** `ontology/tex/aether_flow_consistency.tex`.

## P17. No Extra Scalar, Vector, Ghost, or Tachyon Sector
- **What it is:** A negative boundary of the exact benchmark: the active theory does not add new low-energy gravitational modes.
- **How it works:** Because the effective law is GR, the benchmark inherits GR’s ordinary constraint and gauge structure under standard matter-health assumptions.
- **How it connects:** This separates Æther-flow from Einstein-aether theory, Hořava gravity, or preferred-structure alternatives at observable scale.
- **Source anchors:** `ontology/tex/aether_flow_consistency.tex`; `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`.

## P18. Flow-Geometry Pair `(g, u)`
- **What it is:** The disciplined geometric dictionary for reading Æther-flow inside exact relativistic geometry.
- **How it works:** It uses the exact GR metric `g_{\mu\nu}` plus a future-directed unit timelike congruence `u^\mu` as an observer field.
- **How it connects:** The congruence adds interpretation, not a second field equation or independent low-energy dynamics.
- **Source anchors:** `ontology/tex/aether_flow_geometry.tex`.

## P19. Observer Rest-Space Projector
- **What it is:** The projector `h_{\mu\nu} = g_{\mu\nu} + u_\mu u_\nu / c^2` defining local spatial geometry for an observer congruence.
- **How it works:** It decomposes relativistic quantities into temporal and spatial parts relative to the chosen observer family.
- **How it connects:** It gives the flow interpretation a local SR-compatible structure instead of a preferred-frame ontology.
- **Source anchors:** `ontology/tex/aether_flow_geometry.tex`.

## P20. Congruence Kinematic Decomposition
- **What it is:** The decomposition of `nabla_mu u_nu` into expansion, shear, vorticity, and acceleration.
- **How it works:** `theta` measures local volume expansion, `a_mu` proper acceleration, `omega` swirl or frame dragging, and `sigma` tidal or wave strain.
- **How it connects:** It turns flow language into a rigorous GR dictionary and avoids collapsing gravity into one metaphor.
- **Source anchors:** `ontology/tex/aether_flow_geometry.tex`.

## P21. Raychaudhuri Control
- **What it is:** The use of the Raychaudhuri equation to control congruence focusing and defocusing.
- **How it works:** It relates expansion evolution to shear, vorticity, acceleration divergence, and curvature along the observer flow.
- **How it connects:** It keeps the flow interpretation mathematically grounded rather than merely illustrative.
- **Source anchors:** `ontology/tex/aether_flow_geometry.tex`.

## P22. Frobenius and Vorticity Criterion
- **What it is:** The criterion that a congruence is hypersurface-orthogonal exactly when vorticity vanishes.
- **How it works:** It gives swirl and frame-dragging language a sharp geometric meaning through failure of hypersurface orthogonality.
- **How it connects:** It supports the website’s explanation of rotation, frame dragging, and flow without implying an extra physical fluid.
- **Source anchors:** `ontology/tex/aether_flow_geometry.tex`.

## P23. Observer Normal / Readout Orbit Target
- **What it is:** A sharpened first derivational burden: source-side data should construct an observer normal/readout orbit `([n]_U, Phi_U)`.
- **How it works:** The proposed map runs from local Æther response data to observer readout structure without importing a target metric by hand.
- **How it connects:** This is a key bridge between ontology and effective Lorentzian geometry, and it remains not yet derived.
- **Source anchors:** `ontology/aether-and-aether-flow.md`; `research_control/design/gr_derivation_burden_map.md`.

## P24. Source Ontology Milestone
- **What it is:** The first Distance-to-GR milestone concerning primitive substrate data.
- **How it works:** It requires source-only definitions with explicit claim boundaries and canonical adoption rules.
- **How it connects:** It is the base from which later EqSrc, localization, response, manifold, metric, and matter-coupling burdens depend.
- **Source anchors:** `research_control/design/gr_derivation_burden_map.md`; `registries/DISTANCE_TO_GR_LEDGER.csv`.

## P25. EqSrc and Source Equivalence
- **What it is:** A milestone for establishing source-side equivalence under relevant variations.
- **How it works:** It requires theorem-level control and stress passing, not just notation or analogy.
- **How it connects:** EqSrc sits upstream of localization, response, and source-manifold construction in the derivation chain.
- **Source anchors:** `research_control/design/gr_derivation_burden_map.md`; `research_control/current_frontier.md`.

## P26. ObsLoc_lc Localization
- **What it is:** A source-localization milestone represented in the ledger as a constructive witness line.
- **How it works:** It concerns local exact-branch behavior and robustness under source-side constraints.
- **How it connects:** It supports later response-localization work but does not by itself establish matter coupling or benchmark recovery.
- **Source anchors:** `research_control/current_frontier.md`; `registries/DISTANCE_TO_GR_LEDGER.csv`.

## P27. Resp_lc Response Localization
- **What it is:** A response-localization line involving selector data and source-side response semantics.
- **How it works:** The project treats selector underdetermination as a possible local freeze label rather than global theory rejection.
- **How it connects:** It pressures the path toward `M_src`, `g_eff`, and matter coupling while preserving source-extension possibilities.
- **Source anchors:** `research_control/design/gr_derivation_burden_map.md`; `research_control/current_frontier.md`.

## P28. Source Manifold `M_src`
- **What it is:** A milestone for constructing a source-side manifold-like object.
- **How it works:** Its ledger state is scoped source-only object status, with strong guards against reading it as target manifold, metric, or GR derivation.
- **How it connects:** It is upstream of effective metric construction and downstream of localization and response bridge work.
- **Source anchors:** `research_control/current_frontier.md`; `registries/DISTANCE_TO_GR_LEDGER.csv`.

## P29. Effective Metric `g_eff`
- **What it is:** A milestone for producing a source-to-metric map or effective metric candidate.
- **How it works:** Existing ledger status is guarded as scoped source-extension object evidence, not unscoped Lorentzian metric adoption.
- **How it connects:** It is necessary before matter coupling, Einstein equations, and benchmark promotion can be credibly pursued.
- **Source anchors:** `research_control/current_frontier.md`; `research_control/design/gr_derivation_burden_map.md`.

## P30. Matter-Coupling Milestone
- **What it is:** The active derivation milestone in the current frontier snapshot.
- **How it works:** Current status is scoped precondition evidence, explicitly not matter-coupling adoption, stress-energy semantics, matter action, or detector semantics.
- **How it connects:** The next recommended route formalizes a source-side matter-sector discriminator obstruction target before coupling-law or Einstein-equation work.
- **Source anchors:** `research_control/current_frontier.md`; `research_control/program_state.yaml`.

## P31. Einstein-Equations Milestone
- **What it is:** The downstream burden to derive field equations from source-side dynamics, action, or variation.
- **How it works:** It is marked not started because dynamics/action/variation remain missing in the derivation chain.
- **How it connects:** It cannot be promoted until upstream metric and matter-coupling burdens are discharged under protected gates.
- **Source anchors:** `research_control/current_frontier.md`; `research_control/design/gr_derivation_burden_map.md`.

## P32. Benchmark Promotion Milestone
- **What it is:** The final controlled promotion from source-side derivation work to exact-GR benchmark status.
- **How it works:** It is blocked and human-gated, requiring all prior objects and Gate Chair approval.
- **How it connects:** It is the line that prevents exact-GR compatibility from being advertised as completed derivation.
- **Source anchors:** `research_control/design/gr_derivation_burden_map.md`; `.agents/roles/physics/gate-chair.v0.1.0.md`.

## P33. Finite Toy Metric-Response Model
- **What it is:** A controlled finite source-to-response toy target before attempting a full source-to-GR construction.
- **How it works:** It must specify source set, readout syntax, response relation, metric analogue, and invariance checks.
- **How it connects:** It can sharpen theory development but cannot establish `g_eff`, matter coupling, Einstein equations, or benchmark recovery.
- **Source anchors:** `research_control/design/gr_derivation_burden_map.md`; `research_control/current_frontier.md`.

## P34. Negative Result Preservation
- **What it is:** A system for preserving local failed routes, obstructions, and frozen negative results without overgeneralizing.
- **How it works:** Refuter outputs, obstruction records, freeze labels, and ledger rows store scoped failures and their allowed implications.
- **How it connects:** It lets the project learn from failed derivation attempts while avoiding global no-go claims without theorem-level support.
- **Source anchors:** `.agents/roles/physics/refuter.v0.2.0.md`; `research_control/design/mathematical_decisiveness_completion_contract.md`.

## P35. Adoption vs Derivation Boundary
- **What it is:** A core philosophical and scientific distinction in the project.
- **How it works:** Adoption means using established GR dynamics exactly at the effective level; derivation means recovering those dynamics from explicit substrate variables.
- **How it connects:** This boundary is the most important website language rule for presenting the project accurately.
- **Source anchors:** `README.md`; `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`; `AGENTS.md`.

---

# 3. Low-Level Research-Control and Agent Workflow Components

## R01. `program_state.yaml`
- **What it is:** The compact live pointer to the active research-control state.
- **How it works:** It records mode, active task, latest handoff, current status, claim boundary summary, and next recommended action.
- **How it connects:** Other reader snapshots defer to it when they drift, making it the immediate state beacon for continuation.
- **Source anchors:** `research_control/program_state.yaml`.

## R02. `current_frontier.md`
- **What it is:** A generated snapshot explaining the current frontier to humans and agents.
- **How it works:** It summarizes active task, latest handoff, current milestone, blocked claims, Distance-to-GR table, and validation status.
- **How it connects:** It is useful for the website as status context, but the tracked authority files govern if there is conflict.
- **Source anchors:** `research_control/current_frontier.md`.

## R03. Research Task Directories
- **What it is:** `research_control/tasks/RT-*` directories that hold bounded research transactions.
- **How it works:** Each task may contain task YAML, decisions, AgentJobs, roles, artifacts, completion records, documentation-impact receipts, and evidence.
- **How it connects:** They are the durable history of how physics and project-system work moved through the governance machine.
- **Source anchors:** `research_control/tasks/`; `registries/RESEARCH_TASK_REGISTRY.csv`.

## R04. Director Decision Records
- **What it is:** Strict-frontmatter Markdown records where the Director selects the next role and AgentJob.
- **How it works:** Required sections include objective, authority surfaces read, role-fit matrix, selected role, claim boundary, and validation.
- **How it connects:** A new DDR supersedes old decisions; activated decisions are not silently rewritten.
- **Source anchors:** `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`; `registries/DIRECTOR_DECISION_REGISTRY.csv`.

## R05. AgentJob Contracts
- **What it is:** Immutable YAML executable contracts for a single bounded job.
- **How it works:** They define read/write/generated paths, forbidden paths, commands, validators, expected outputs, source classes, memory preflight, and claim boundaries.
- **How it connects:** AgentJobs are the central unit that keeps research or maintenance work bounded and auditable.
- **Source anchors:** `.agents/schemas/AGENT_JOB_SCHEMA.md`; `registries/AGENT_JOB_REGISTRY.csv`.

## R06. Execution-Role Records
- **What it is:** Task-local authority contracts binding one AgentJob to exact role semantics.
- **How it works:** They support direct registered roles, task overlays, and one-job provisional roles without silently expanding authority.
- **How it connects:** They allow flexible routing while preserving role boundaries, write allowlists, and human-gate rules.
- **Source anchors:** `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`; `registries/ROLE_EXECUTION_REGISTRY.csv`.

## R07. One-Job Rule
- **What it is:** The rule that a continuation invocation may create or execute at most one bounded AgentJob.
- **How it works:** Even complex internal analysis must resolve into one outer job, one execution-role record, one completion, and one fused output.
- **How it connects:** It prevents research-control work from becoming an unbounded swarm of untracked actions.
- **Source anchors:** `research_control/README.md`; `.codex/skills/continue-research/SKILL.md`.

## R08. Parent-Child Parallel Synthesis
- **What it is:** An internal physics-job decomposition mode required for new physics AgentJobs after the policy timestamp.
- **How it works:** A parent plus two child perspectives produce supporting outputs, conflict review, and one fused final result under the same outer AgentJob.
- **How it connects:** It adds multidisciplinary analysis without creating child jobs, child roles, new write paths, or authority expansion.
- **Source anchors:** `research_control/README.md`; `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`; `.codex/skills/continue-research/SKILL.md`.

## R09. Memory Preflight Receipt
- **What it is:** A mandatory recorded memory-status and source-inspection receipt for later AgentJobs and completions.
- **How it works:** Agents run memory status and targeted lookup/search, then inspect canonical source files or registry rows for any influential hit.
- **How it connects:** It makes research memory useful while keeping retrieval layers from becoming authority.
- **Source anchors:** `.agents/schemas/AGENT_JOB_SCHEMA.md`; `.codex/skills/continue-research/SKILL.md`.

## R10. Theoretical Continuation Gate
- **What it is:** A rule preventing generic pause when theoretical work can continue.
- **How it works:** Missing local data, witnesses, or primitives route to bounded theoretical selection, construction, no-go, or calculation packets unless protected authority is required.
- **How it connects:** It keeps the physics program moving without pretending missing repo-local data is a terminal result.
- **Source anchors:** `research_control/README.md`; `.agents/roles/physics/theoretical-continuation-selector.v0.1.0.md`.

## R11. Ontology-Law Research Packet Route
- **What it is:** A named route for derivation-critical missing source-side laws or selectors.
- **How it works:** It is allowed only when the current ontology does not derive a required law, discriminator, transition rule, robustness rule, or equivalent primitive.
- **How it connects:** It preserves same-milestone continuation while blocking ontology adoption, benchmark promotion, and global impossibility claims.
- **Source anchors:** `AGENTS.md`; `research_control/README.md`; `.agents/schemas/AGENT_JOB_SCHEMA.md`.

## R12. Distance-to-GR Status Matrix
- **What it is:** A completion-level matrix tracking local result status across derivation burdens.
- **How it works:** It separates local packet success from observer readout, effective metric, matter coupling, Einstein equations, benchmark promotion, and route freeze status.
- **How it connects:** It gives the website a clean way to explain “where the project is” without overclaiming.
- **Source anchors:** `research_control/design/gr_derivation_burden_map.md`; `research_control/templates/COMPLETION_TEMPLATE.yaml`.

## R13. Distance-to-GR Delta
- **What it is:** A mathematical-decisiveness field stating whether a completion changed the persistent ledger.
- **How it works:** It names burden ID, old and new status, ledger update state, downstream unlocked items, downstream blocked items, and explanation.
- **How it connects:** It prevents validator success from being conflated with physics progress.
- **Source anchors:** `research_control/design/mathematical_decisiveness_completion_contract.md`; `research_control/templates/COMPLETION_TEMPLATE.yaml`.

## R14. Mathematical Payload Manifest
- **What it is:** A completion field requiring concrete mathematical or control payload items.
- **How it works:** Payloads may be definitions, lemmas, theorems, finite models, countermodels, witnesses, obstructions, constructions, dependency updates, selections, or source-extension classifications.
- **How it connects:** It makes completions auditable and discourages vague “more work required” endings.
- **Source anchors:** `research_control/design/mathematical_decisiveness_completion_contract.md`.

## R15. Forbidden Conclusion Summary
- **What it is:** A required completion field listing claims the task does not authorize.
- **How it works:** It blocks conclusions such as ontology edit, `M_src` adoption, `g_eff` claim, matter coupling, Einstein equations, benchmark promotion, Gate Chair verdict, completed derivation, or global rejection.
- **How it connects:** It is the anti-overread fuse for both agents and website copy.
- **Source anchors:** `research_control/design/mathematical_decisiveness_completion_contract.md`; `research_control/templates/COMPLETION_TEMPLATE.yaml`.

## R16. Candidate Constructor Result
- **What it is:** A decisive result block for Candidate Constructor physics tasks.
- **How it works:** It must end with constructed candidate, minimal countermodel, precise obstruction, or invalid-under-claim-boundary, plus a no-fog explanation.
- **How it connects:** It forces constructive roles to leave the research state sharper than they found it.
- **Source anchors:** `.agents/roles/physics/candidate-constructor.v0.2.0.md`; `research_control/design/mathematical_decisiveness_completion_contract.md`.

## R17. Obstruction Record
- **What it is:** A structured record for precise obstructions or route freezes.
- **How it works:** It stores obstruction ID, scope, failed object, exact failure, ontology implication, source-extension implication, consequence, and forbidden overread.
- **How it connects:** It preserves negative results as routing evidence rather than burying them in prose.
- **Source anchors:** `research_control/design/mathematical_decisiveness_completion_contract.md`.

## R18. Freeze Criteria Status
- **What it is:** A mechanism to prevent repeated-burden orbit.
- **How it works:** It records prior attempts, freeze conditions, do-not-freeze conditions, freeze decision, and next allowed route.
- **How it connects:** It lets the project locally freeze an unproductive route without rejecting the whole theory.
- **Source anchors:** `research_control/design/gr_derivation_burden_map.md`; `research_control/design/mathematical_decisiveness_completion_contract.md`.

## R19. Route Cycle Control
- **What it is:** A completion block exposing repeated selector, constructor, audit, or stress cycles.
- **How it works:** It records cycle family, current step, related tasks, cycle risk, orbit-avoidance reason, and next role consequence.
- **How it connects:** It helps future agents distinguish genuine narrowing from repetitive motion.
- **Source anchors:** `research_control/design/mathematical_decisiveness_completion_contract.md`.

## R20. Completion Records
- **What it is:** YAML records documenting AgentJob output, command results, validators, payloads, claim boundaries, and next consequences.
- **How it works:** The template includes validation status, output paths, memory preflight, Distance-to-GR status, mathematical-decisiveness fields, and project-improvement signals.
- **How it connects:** They are the receipt layer that joins role work to registries, handoffs, and current state.
- **Source anchors:** `research_control/templates/COMPLETION_TEMPLATE.yaml`; `research_control/tasks/`.

## R21. Handoff Records
- **What it is:** Durable state-transfer records created after completions.
- **How it works:** Handoffs preserve the result, next recommended route, claim boundaries, validation evidence, and any project-improvement sidecar signals.
- **How it connects:** The latest handoff is immediate routing authority below `program_state.yaml`.
- **Source anchors:** `research_control/handoffs/`; `research_control/current_frontier.md`.

## R22. Claim Boundary Registry
- **What it is:** The registry of explicit claim blocks and controlled claim statuses.
- **How it works:** It defines what cannot be inferred from local results, role outputs, validators, generated derivatives, or registry metadata.
- **How it connects:** It is the guardrail that keeps the website, agents, and generated docs from overreading internal progress.
- **Source anchors:** `registries/CLAIM_BOUNDARY_REGISTRY.csv`; `AGENTS.md`.

## R23. Novel Datum Acquisition Rule
- **What it is:** A rule that local absence of data or witnesses is not automatically terminal.
- **How it works:** The Director may route one bounded job to primary literature search, source-acquisition design, bounded calculation, mathematical construction, or experiment design.
- **How it connects:** It keeps theoretical work active while labeling new material as draft/control until audit and gates occur.
- **Source anchors:** `research_control/README.md`; `.codex/skills/continue-research/SKILL.md`.

## R24. Checkpoint Transaction System
- **What it is:** The final commit discipline for valid state-changing transactions.
- **How it works:** It regenerates systems, validates, stages only allowed paths, checks dirty state, classifies impact, and commits with deterministic boundaries.
- **How it connects:** It turns research-control and project-system work into reproducible repository history.
- **Source anchors:** `scripts/research_control/checkpoint_research_transaction.py`; `.codex/skills/continue-research/SKILL.md`.

---

# 4. Role and Schema Components

## A01. Director of Research
- **What it is:** The routing-control role that resolves the next bounded research step.
- **How it works:** It reads tracked authority surfaces, writes or reuses a DDR, selects a role fit, and creates one AgentJob when no human gate is required.
- **How it connects:** It is the switchyard between current state, physics roles, schemas, claim gates, and validation.
- **Source anchors:** `.agents/roles/research_ops/director-of-research.v0.2.0.md`; `.codex/skills/continue-research/SKILL.md`.

## A02. Candidate Constructor
- **What it is:** A physics role that builds one bounded candidate derivation step or witness.
- **How it works:** It attempts bridge maps, finite witnesses, source-extension data, or precise failures while preserving all downstream promotion blocks.
- **How it connects:** Its output usually feeds Smuggling Auditor, Refuter, or human-gated review depending on result status.
- **Source anchors:** `.agents/roles/physics/candidate-constructor.v0.2.0.md`.

## A03. Ontology Formalizer
- **What it is:** A physics role that defines source-side primitives, assumptions, forbidden imports, and Gate 0 burdens.
- **How it works:** It produces draft/control formalizations with explicit domains, maps, proof obligations, and no-target-import boundaries.
- **How it connects:** It prepares candidate-law or source-side objects for construction, audit, stress, or human-gated consideration.
- **Source anchors:** `.agents/roles/physics/ontology-formalizer.v0.2.0.md`.

## A04. Refuter
- **What it is:** A physics adversarial role that attacks candidates and mechanisms.
- **How it works:** It stress-tests collapse, nonuniqueness, inverse defects, cocycle defects, variation fragility, and repeated burdens.
- **How it connects:** It preserves local negative results and can trigger freeze review without globally rejecting the theory.
- **Source anchors:** `.agents/roles/physics/refuter.v0.2.0.md`.

## A05. Smuggling Auditor
- **What it is:** A physics adversarial role that detects hidden target imports.
- **How it works:** It audits whether a candidate silently uses target atlas, target metric, benchmark success, generated derivatives, registry authority, role authority, or validation authority as source premises.
- **How it connects:** It can block or flag promotion, but it cannot promote claims itself.
- **Source anchors:** `.agents/roles/physics/smuggling-auditor.v0.2.0.md`.

## A06. Gate Chair
- **What it is:** A human-gated scientific role for promotion, closure, or suspension decisions.
- **How it works:** It is defined but paused; execution and any promotion require explicit tracked approval.
- **How it connects:** It is the protected authority for benchmark promotion, closure, or other high-risk scientific status changes.
- **Source anchors:** `.agents/roles/physics/gate-chair.v0.1.0.md`.

## A07. Theoretical Continuation Selector
- **What it is:** A physics routing role for choosing the next theoretical packet when no single execution role is obvious.
- **How it works:** It selects from packet types such as source-side selector primitive, irrelevance theorem, concrete witness, finite toy model, source extension, or human gate requirement.
- **How it connects:** It prevents generic controlled pause when bounded theoretical continuation remains possible.
- **Source anchors:** `.agents/roles/physics/theoretical-continuation-selector.v0.1.0.md`.

## A08. Documentation Curator
- **What it is:** A research-operations role for human-facing explanatory documentation and source-backed visual explainers.
- **How it works:** It may update explanatory Markdown, source specs, publication registries, tracked HTML explainers, and documentation-impact receipts within allowlists.
- **How it connects:** It is the main role behind website-style materials, while forbidden from changing physics claims or project-control contracts.
- **Source anchors:** `.agents/roles/research_ops/documentation-curator.v0.7.0.md`.

## A09. Memory-System Maintainer
- **What it is:** A project-control role maintaining memory, wiki, registry, Obsidian, and derivative metadata tooling.
- **How it works:** It edits scripts and tooling that generate or validate retrieval layers while preserving source-first authority.
- **How it connects:** It keeps agents able to navigate the repository without letting local retrieval become scientific authority.
- **Source anchors:** `.agents/roles/research_ops/memory-system-maintainer.v0.2.0.md`.

## A10. Process Integrity Auditor
- **What it is:** A process-control role for diagnosing and repairing control-state defects.
- **How it works:** It may edit control files, state boards, registry links, and handoff metadata when the correct state is uniquely determined from evidence.
- **How it connects:** If more than one plausible state remains, it stops with a conflict report and requires human resolution.
- **Source anchors:** `.agents/roles/research_ops/process-integrity-auditor.v0.1.0.md`.

## A11. Project-Control Maintainer
- **What it is:** A project-control role for skill contracts, role contracts, schemas, control registries, and validator hooks.
- **How it works:** It changes workflow behavior only inside an owning AgentJob and must run research-control and documentation-impact validation.
- **How it connects:** It is distinct from Documentation Curator because it changes how the system operates, not just how it is explained.
- **Source anchors:** `.agents/roles/research_ops/project-control-maintainer.v0.1.0.md`.

## A12. Project-System Director
- **What it is:** A project-control routing role for one bounded project-system improvement step.
- **How it works:** It uses tracked signals, change classification, guidance, and validation state to create one project-system DDR and AgentJob.
- **How it connects:** It routes non-physics repairs to documentation, validator, memory, or control-maintenance roles.
- **Source anchors:** `.agents/roles/research_ops/project-system-director.v0.1.0.md`.

## A13. Validator Engineer
- **What it is:** A project-control role for deterministic validators, tests, and checkpoint gates.
- **How it works:** It edits validation scripts, tests, validator contracts, and related registry rows, preferring deterministic checks over model judgment.
- **How it connects:** It strengthens the system’s machine-checkable boundaries without changing scientific verdicts.
- **Source anchors:** `.agents/roles/research_ops/validator-engineer.v0.1.0.md`.

## A14. Role Schema
- **What it is:** The schema defining required frontmatter for versioned role contracts.
- **How it works:** It requires fields for role identity, authority, permissions, validators, source classes, and human-gate status.
- **How it connects:** It keeps roles stable over time while execution-role records handle task-specific adaptation.
- **Source anchors:** `.agents/schemas/ROLE_SCHEMA.md`.

## A15. Director Decision Schema
- **What it is:** The schema for machine-checkable Director Decision Records.
- **How it works:** Frontmatter carries decision metadata, while required body sections record objective, authority surfaces, role fit, selected role, claim boundary, and validation.
- **How it connects:** It makes routing reasoning auditable and prevents activated decisions from being silently rewritten.
- **Source anchors:** `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`.

## A16. AgentJob Schema
- **What it is:** The executable-contract schema for bounded AgentJobs.
- **How it works:** It requires fields for job identity, role, status, gates, paths, commands, validators, outputs, claim boundary, memory preflight, and derivation milestones.
- **How it connects:** It is the main low-level contract that turns agent work into controlled state changes.
- **Source anchors:** `.agents/schemas/AGENT_JOB_SCHEMA.md`.

## A17. Execution Role Schema
- **What it is:** The schema for binding one AgentJob to one role execution context.
- **How it works:** It distinguishes registered roles, task overlays, and one-job provisional roles, while preserving expiration and authority-delta summaries.
- **How it connects:** It gives the Director flexibility without letting route labels become new roles or hidden permission expansions.
- **Source anchors:** `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`.

## A18. Documentation Impact Schema
- **What it is:** The schema for documentation-impact receipts after project-system changes.
- **How it works:** It records changed paths, whether documentation updates were required, inspected surfaces, updated docs, registries, generated derivatives, validators, and status.
- **How it connects:** It ensures changes to how the system operates are reflected in source documentation or explicitly justified as no-op.
- **Source anchors:** `.agents/schemas/DOCUMENTATION_IMPACT_SCHEMA.md`.

---

# 5. Memory, Registry, and Retrieval Components

## M01. `TEX_SOURCE_REGISTRY.csv`
- **What it is:** The registry of canonical TeX scientific sources.
- **How it works:** It links physics source files to object IDs, hashes, status, and generated derivatives.
- **How it connects:** It is the strongest source lane for physics and derivational claims.
- **Source anchors:** `registries/TEX_SOURCE_REGISTRY.csv`; `ontology/tex/`.

## M02. `MARKDOWN_SOURCE_REGISTRY.csv`
- **What it is:** The registry of authored Markdown sources.
- **How it works:** It covers front-door docs, agent guidance, role contracts, schema contracts, skill contracts, control notes, publication briefs, and source specs.
- **How it connects:** It gives non-TeX documentation a canonical source lane while preserving physics authority boundaries.
- **Source anchors:** `registries/MARKDOWN_SOURCE_REGISTRY.csv`; `markdown/`; `.agents/`; `.codex/skills/`.

## M03. `PDF_DERIVATIVE_REGISTRY.csv`
- **What it is:** The registry for generated PDF derivatives.
- **How it works:** PDFs are built from registered TeX sources and tracked as human-reading outputs.
- **How it connects:** PDFs are useful for readers, but they do not override TeX source authority.
- **Source anchors:** `registries/PDF_DERIVATIVE_REGISTRY.csv`; `ontology/pdfs/`.

## M04. `HTML_EXPLAINER_REGISTRY.csv`
- **What it is:** The registry for tracked HTML explainer derivatives.
- **How it works:** HTML pages must correspond to registered Markdown source specs and publication briefs.
- **How it connects:** It is the control layer that keeps website-style pages source-backed and noncanonical.
- **Source anchors:** `registries/HTML_EXPLAINER_REGISTRY.csv`; `html/`; `markdown/html-explainer-specs/`.

## M05. `PUBLICATION_BRIEF_REGISTRY.csv`
- **What it is:** The registry of reviewed public explainer briefs and their output paths.
- **How it works:** It maps page title, document type, brief path, source spec, GitHub Markdown path, HTML path, source materials, visual strategy, and review status.
- **How it connects:** It is the active control surface for public HTML and GitHub-facing Markdown publication pages.
- **Source anchors:** `registries/PUBLICATION_BRIEF_REGISTRY.csv`; `markdown/publication-briefs/`.

## M06. `WIKI_ARTIFACT_REGISTRY.csv`
- **What it is:** The registry of generated wiki notes and indexes.
- **How it works:** Wiki pages point back to sources and make objects easier to browse.
- **How it connects:** Wiki notes are generated derivatives and should be regenerated from source rather than hand-edited.
- **Source anchors:** `registries/WIKI_ARTIFACT_REGISTRY.csv`; `wiki/`.

## M07. `CONTENT_SEMANTIC_REGISTRY.csv`
- **What it is:** The registry of semantic extracts for local retrieval.
- **How it works:** It supports search across Markdown, TeX, PDF, HTML, and related content through local extract layers.
- **How it connects:** It improves agent navigation while remaining non-authoritative retrieval evidence.
- **Source anchors:** `registries/CONTENT_SEMANTIC_REGISTRY.csv`; `.local/content_semantics/`.

## M08. `OBSIDIAN_VAULT_REGISTRY.csv`
- **What it is:** The registry for generated Obsidian vault notes.
- **How it works:** The vault mirrors registered objects into a local reader and navigation environment.
- **How it connects:** It is useful for research navigation, but `.local/obsidian` remains ignored local retrieval state.
- **Source anchors:** `registries/OBSIDIAN_VAULT_REGISTRY.csv`; `.local/obsidian/aether-flow-wiki/`.

## M09. `FILE_OBJECT_REGISTRY.csv`
- **What it is:** A broad generated registry of tracked file objects.
- **How it works:** It helps classify files by category, object relationship, and generation status.
- **How it connects:** It supports memory, wiki, folder mapping, and validation, but generated registry metadata is not physics authority.
- **Source anchors:** `registries/FILE_OBJECT_REGISTRY.csv`; `FOLDER_MAP.md`.

## M10. `OBJECT_RELATIONSHIP_REGISTRY.csv`
- **What it is:** A relationship registry linking source objects and derivatives.
- **How it works:** It records how sources, generated artifacts, and related objects point to one another.
- **How it connects:** It makes the repository navigable as a graph rather than a loose pile of files.
- **Source anchors:** `registries/OBJECT_RELATIONSHIP_REGISTRY.csv`; `.codex/skills/project-memory-system/SKILL.md`.

## M11. `AGENT_ROLE_REGISTRY.csv`
- **What it is:** The registry of versioned agent roles.
- **How it works:** It records role identity, status, authority class, and contract location.
- **How it connects:** Role contracts and execution-role records rely on it for validation and historical compatibility.
- **Source anchors:** `registries/AGENT_ROLE_REGISTRY.csv`; `.agents/roles/`.

## M12. `AGENT_JOB_REGISTRY.csv`
- **What it is:** The registry of AgentJobs and their canonical paths.
- **How it works:** It connects jobs to tasks, decisions, roles, completions, and status evidence.
- **How it connects:** It is the index for bounded work and the resolution evidence for some project-improvement signals.
- **Source anchors:** `registries/AGENT_JOB_REGISTRY.csv`; `research_control/tasks/`.

## M13. `DIRECTOR_DECISION_REGISTRY.csv`
- **What it is:** The registry of Director Decision Records.
- **How it works:** It maps decision IDs to paths, tasks, jobs, and state.
- **How it connects:** It allows validators and agents to trace why a role and job were selected.
- **Source anchors:** `registries/DIRECTOR_DECISION_REGISTRY.csv`; `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`.

## M14. `ROLE_EXECUTION_REGISTRY.csv`
- **What it is:** The registry of execution-role records.
- **How it works:** It tracks the one-job role semantics used by AgentJobs, including overlays and provisional roles.
- **How it connects:** It prevents base role contracts from being silently mutated for one task.
- **Source anchors:** `registries/ROLE_EXECUTION_REGISTRY.csv`; `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`.

## M15. `RESEARCH_TASK_REGISTRY.csv`
- **What it is:** The registry of research tasks.
- **How it works:** It indexes task directories, statuses, active boundaries, and relationships to jobs and handoffs.
- **How it connects:** It is the task-level map for the research-control state machine.
- **Source anchors:** `registries/RESEARCH_TASK_REGISTRY.csv`; `research_control/tasks/`.

## M16. `DISTANCE_TO_GR_LEDGER.csv`
- **What it is:** The persistent ledger for derivation burdens and Distance-to-GR status.
- **How it works:** It tracks layered control, mathematical, physical, promotion, and overread-guard fields for each burden.
- **How it connects:** It is the main source for explaining current derivation progress without overpromotion.
- **Source anchors:** `registries/DISTANCE_TO_GR_LEDGER.csv`; `research_control/current_frontier.md`.

## M17. Project-Improvement Signal Registries
- **What it is:** The type and instance registries for project-system improvement signals.
- **How it works:** Signal types define allowed categories and routing metadata; signal instances carry severity, status, and resolution evidence.
- **How it connects:** They route documentation drift, validator issues, memory tooling problems, and control-system repairs outside physics continuation.
- **Source anchors:** `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`; `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`.

## M18. Generated Markdown Wiki
- **What it is:** A generated browsing layer under `wiki/markdown`, `wiki/tex`, `wiki/pdf`, `wiki/html`, and indexes.
- **How it works:** Notes point back to registered sources and provide source metadata for humans and agents.
- **How it connects:** It is a navigation layer, not a place to make canonical edits.
- **Source anchors:** `wiki/`; `FOLDER_MAP.md`.

## M19. Local Semantic Extracts
- **What it is:** A local retrieval layer generated under `.local/content_semantics`.
- **How it works:** It extracts searchable text or semantic summaries from registered content formats.
- **How it connects:** Agents can search it for navigation, but must verify influential hits against canonical sources.
- **Source anchors:** `.local/content_semantics/`; `research_control/README.md`.

## M20. Local Obsidian Vault
- **What it is:** A regenerated local vault for reading and linking project objects in Obsidian.
- **How it works:** It mirrors source-backed notes and indexes while staying ignored and local.
- **How it connects:** It supports human and agent navigation but remains outside committed authority.
- **Source anchors:** `.local/obsidian/aether-flow-wiki/`; `Makefile`.

## M21. SQLite / Memory Index Concept
- **What it is:** A local memory index referenced by memory preflight and query tools.
- **How it works:** It supports `query_memory.py status`, `lookup`, and `search` workflows for registered project objects.
- **How it connects:** It is a retrieval accelerator, not a substitute for source inspection.
- **Source anchors:** `.codex/skills/project-memory-system/SKILL.md`; `.codex/skills/continue-research/SKILL.md`.

## M22. Folder Map
- **What it is:** A generated classification map of repository folders.
- **How it works:** It labels each folder as canonical source, archival source, control authority, generated derivative, local retrieval, tooling, or reserved lane.
- **How it connects:** It is a website-friendly orientation map for explaining the project’s source and authority topology.
- **Source anchors:** `FOLDER_MAP.md`.

---

# 6. Documentation, Publication, and Website Components

## D01. README Front Door
- **What it is:** The main public entry point explaining the project’s two tracks, current benchmark, ontology lane, research-agent system, explainers, and requirements.
- **How it works:** It summarizes canonical state for humans while pointing readers toward source authority and generated explainers.
- **How it connects:** The website can use it as a narrative foundation but should preserve its claim-boundary language.
- **Source anchors:** `README.md`.

## D02. Context Glossary
- **What it is:** A small glossary defining project-specific documentation language.
- **How it works:** It clarifies terms such as GitHub-facing Markdown System, GitHub-facing Explainer, Advisory Formatting Guidance, and Subject Summary.
- **How it connects:** It helps future website copy use the project’s documentation terminology consistently.
- **Source anchors:** `CONTEXT.md`.

## D03. Markdown Source Specs
- **What it is:** Source specifications under `markdown/html-explainer-specs/` for generated public explainers.
- **How it works:** Specs declare title, purpose, audience, output paths, renderer skill, source materials, claim boundary, controls, and layout intent.
- **How it connects:** They are the canonical source lane for tracked HTML and GitHub-facing explainer pages.
- **Source anchors:** `markdown/html-explainer-specs/`; `.agents/roles/research_ops/documentation-curator.v0.7.0.md`.

## D04. Publication Briefs
- **What it is:** Page-specific briefs that define reader job, document type, visual strategy, acceptance criteria, and forbidden patterns.
- **How it works:** They guide design and content for each reviewed public explainer page.
- **How it connects:** They are highly relevant to your website because they already encode public-facing explanatory strategy.
- **Source anchors:** `markdown/publication-briefs/`; `registries/PUBLICATION_BRIEF_REGISTRY.csv`.

## D05. GitHub-Facing Markdown Explainers
- **What it is:** Generated source-backed Markdown pages under `github-facing/` for repository browsers and external AI agents.
- **How it works:** They orient readers while remaining noncanonical for physics, routing, validators, schemas, or registries.
- **How it connects:** They can be adapted into website sections if source authority and noncanonical status are preserved.
- **Source anchors:** `github-facing/`; `CONTEXT.md`; `README.md`.

## D06. Tracked HTML Explainers
- **What it is:** Reviewed, no-network, standalone HTML reader pages under `html/`.
- **How it works:** They must be generated from registered Markdown source specs and publication briefs, with visible source grounding.
- **How it connects:** They are the closest existing artifact to the website surface you are building.
- **Source anchors:** `html/`; `.codex/skills/html-visual-explainer/SKILL.md`.

## D07. Project Overview Explainer
- **What it is:** A front-door reader page for the two project missions and first reading path.
- **How it works:** It orients readers to the ontology, GR-derivation goal, AI research-agent harness, and source-authority discipline.
- **How it connects:** It can become the website homepage model, provided it keeps current proof boundaries visible.
- **Source anchors:** `github-facing/project-overview-explainer.md`; `html/project-overview-explainer.html`.

## D08. Source Authority Explainer
- **What it is:** A public page explaining canonical sources, generated derivatives, registries, and local retrieval layers.
- **How it works:** It shows how readers should treat TeX, Markdown, PDFs, HTML, wiki, and `.local` layers differently.
- **How it connects:** It should be prominent on the website to protect readers from mistaking generated presentation for source authority.
- **Source anchors:** `github-facing/source-authority-explainer.md`; `html/source-authority-explainer.html`.

## D09. Physics Program Explainer
- **What it is:** A public overview of the physics mission, exact-GR benchmark boundary, and open derivation burden.
- **How it works:** It translates exact closure, ontology, and derivation roadmap into a reader-facing physics narrative.
- **How it connects:** It is the core website page for technically accurate promotion of the physics track.
- **Source anchors:** `github-facing/aether-flow-physics-program-explainer.md`; `html/aether-flow-physics-program-explainer.html`.

## D10. Ontology Explainer
- **What it is:** A concept explainer for the proposed Æther / Æther-flow substrate ontology.
- **How it works:** It explains the substrate, flow, observed space, S-time, expansion, and claim limits without claiming completed derivation.
- **How it connects:** It is a natural website “conceptual foundation” page.
- **Source anchors:** `github-facing/aether-flow-ontology-explainer.md`; `html/aether-flow-ontology-explainer.html`.

## D11. Exact-GR Benchmark Boundary Explainer
- **What it is:** A comparison or boundary map separating benchmark compatibility from derivation.
- **How it works:** It explains why exact GR adoption is a real theory statement but not a first-principles source recovery.
- **How it connects:** It should sit near any promotional claim about GR consistency.
- **Source anchors:** `github-facing/exact-gr-benchmark-boundary-explainer.md`; `html/exact-gr-benchmark-boundary-explainer.html`.

## D12. GR Derivation Roadmap Explainer
- **What it is:** A public decision guide for the staged burden from ontology to effective Lorentzian geometry and GR.
- **How it works:** It translates the burden map and ledger into reader-facing milestones, gates, and blocked claims.
- **How it connects:** It helps the website show progress without implying the endpoint has been reached.
- **Source anchors:** `github-facing/gr-derivation-roadmap-explainer.md`; `html/gr-derivation-roadmap-explainer.html`.

## D13. Claim Gates Explainer
- **What it is:** A public boundary map for accepted claims, stopped lines, no-go records, and freeze criteria.
- **How it works:** It explains why negative results are preserved, why local failures do not imply global rejection, and why promotion is gated.
- **How it connects:** It is a credibility feature for the website because it shows the project’s anti-overclaim machinery.
- **Source anchors:** `github-facing/claim-gates-explainer.md`; `html/claim-gates-explainer.html`.

## D14. Research-Agent Workflow Explainer
- **What it is:** A workflow guide for Director routing, AgentJobs, roles, completions, and handoffs.
- **How it works:** It explains the AI track as a governed research-agent workflow, not an autonomous proof machine.
- **How it connects:** It supports the website’s AI-system story and shows how theoretical work becomes auditable.
- **Source anchors:** `github-facing/research-agent-workflow-explainer.md`; `html/research-agent-workflow-explainer.html`.

## D15. Roles and Skills Catalog
- **What it is:** A reference catalog for active role contracts and repo-local skills.
- **How it works:** It pairs the `.agents/roles/` contracts with `.codex/skills/` workflows and describes their boundaries.
- **How it connects:** It can inform a website page about the project’s agent architecture.
- **Source anchors:** `github-facing/roles-and-skills-explainer.md`; `html/roles-and-skills-explainer.html`.

## D16. Memory System Explainer
- **What it is:** A reference catalog for CSV registries, wiki notes, Obsidian, semantic extracts, and retrieval limits.
- **How it works:** It explains source-first memory as navigation plus verification rather than authority substitution.
- **How it connects:** It is useful for explaining why the project is searchable and auditable at scale.
- **Source anchors:** `github-facing/memory-system-explainer.md`; `html/memory-system-explainer.html`.

## D17. Validator and Operator Workflow Explainer
- **What it is:** An operator guide for deterministic checks, documentation impact, and checkpoint gates.
- **How it works:** It lays out how contributors validate memory, project control, HTML explainers, and research-control transactions.
- **How it connects:** It helps technical readers trust that the repo’s operational state is actively checked.
- **Source anchors:** `github-facing/validator-operator-workflow-explainer.md`; `html/validator-operator-workflow-explainer.html`.

## D18. Technical Requirements Explainer
- **What it is:** A contributor/operator guide for local Python, Codex, memory, validation, rendering, and PDF requirements.
- **How it works:** It explains the runtime stack, dependency tiers, PyMuPDF, Mermaid/Playwright, Obsidian, and LaTeX/PDF paths.
- **How it connects:** It can support the website’s contributor documentation section.
- **Source anchors:** `github-facing/technical-requirements-explainer.md`; `html/technical-requirements-explainer.html`; `README.md`.

## D19. Subject Summary Contract
- **What it is:** A documentation standard requiring each explainer to open with a source-backed functional summary.
- **How it works:** The summary states what the subject is, what role it has, why it matters, and which sources ground it.
- **How it connects:** This is an excellent pattern for website sections because it forces each page to be useful before diving into detail.
- **Source anchors:** `CONTEXT.md`; `.agents/roles/research_ops/documentation-curator.v0.7.0.md`.

## D20. No-Network HTML Publication Rule
- **What it is:** A publication constraint for tracked HTML pages.
- **How it works:** HTML must be single-file, no-network, readable without JavaScript, mobile-safe, source-grounded, and explicit about noncanonical status.
- **How it connects:** It is directly relevant if the website reuses generated HTML or wants reproducible static pages.
- **Source anchors:** `.codex/skills/html-visual-explainer/SKILL.md`.

---

# 7. Tooling, Skills, Scripts, and Runtime Components

## T01. Codex App Harness
- **What it is:** The current AI-agent execution harness assumed by repo-local skills, prompts, agent configuration, and continuation workflows.
- **How it works:** Read-only inspection and Python validators can run outside Codex, but governed workflow reproduction currently assumes Codex app access.
- **How it connects:** It is the present operational environment for the AI research-agent track.
- **Source anchors:** `README.md`; `.codex/`.

## T02. `continue-research` Skill
- **What it is:** The main skill for research-control continuation.
- **How it works:** It runs memory preflight, resolves tracked state, selects or reuses one AgentJob, enforces roles and gates, writes completions and handoffs, regenerates memory, validates, and checkpoints.
- **How it connects:** It is the operating procedure for physics continuation and controlled research progress.
- **Source anchors:** `.codex/skills/continue-research/SKILL.md`.

## T03. `improve-project-system` Skill
- **What it is:** The workflow for improving roles, schemas, validators, control Markdown, memory tooling, generated-document pipelines, and reliability.
- **How it works:** It classifies changes, resolves project-improvement signals, routes one bounded project-system AgentJob, writes documentation-impact receipts, regenerates, validates, and checkpoints.
- **How it connects:** It keeps operational repair separate from physics derivation and claim promotion.
- **Source anchors:** `.codex/skills/improve-project-system/SKILL.md`.

## T04. `project-memory-system` Skill
- **What it is:** The skill owning memory, registry, wiki, PDF-derivative, cleanup, and validation scripts.
- **How it works:** It runs bootstrap generation, validate-only checks, docs-only checks, strict docs validation, and local noise cleanup.
- **How it connects:** It synchronizes generated surfaces and registries that other workflows rely on.
- **Source anchors:** `.codex/skills/project-memory-system/SKILL.md`.

## T05. `html-visual-explainer` Skill
- **What it is:** The front door for governed, standalone HTML publication explainers.
- **How it works:** It requires publication briefs, source specs, no-network HTML, source grounding, GitHub Markdown pairing, validation, and screenshot QA for pilot pages.
- **How it connects:** It is the strongest existing process for building website-ready explanatory surfaces.
- **Source anchors:** `.codex/skills/html-visual-explainer/SKILL.md`.

## T06. `visual-explainer` Skill
- **What it is:** A local visual-documentation skill for diagrams, architecture overviews, recaps, plans, and project explainers.
- **How it works:** It can generate local self-contained HTML in `.local/html_wikis/`, while tracked publication requires the governed HTML explainer path.
- **How it connects:** It provides design capability but does not make generated pages authoritative.
- **Source anchors:** `.codex/skills/visual-explainer/SKILL.md`.

## T07. `user-modified-project` Skill
- **What it is:** An integration router for human-made repository edits.
- **How it works:** It recovers intent, inspects Git state, classifies changed paths, routes to physics or project-system workflows, refreshes generated systems, validates, and checkpoints.
- **How it connects:** It lets human edits enter the governed system without bypassing authority rules.
- **Source anchors:** `.codex/skills/user-modified-project/SKILL.md`.

## T08. Markdown, Obsidian, TeX, PDF, and Ontology Skills
- **What it is:** A set of repo-local skills for generated wiki, Obsidian vault, TeX wiki, PDF derivative builds, and ontology-promotion workflows.
- **How it works:** They support format-specific generation and controlled source workflows under the project-memory and authority hierarchy.
- **How it connects:** They maintain reader and derivative layers while keeping canonical edits in the proper source lanes.
- **Source anchors:** `.codex/skills/markdown-wiki/`; `.codex/skills/obsidian-wiki/`; `.codex/skills/tex-wiki/`; `.codex/skills/pdf-derivative-build/`; `.codex/skills/ontology-promotion/`.

## T09. Research-Control Scripts
- **What it is:** Python scripts that operate the tracked research-control state machine.
- **How it works:** Main tools include `continue_research.py`, `resolve_latest_handoff.py`, `validate_research_control.py`, `report_physics_progress_metrics.py`, `checkpoint_research_transaction.py`, and `strict_yaml.py`.
- **How it connects:** They enforce tracked state but do not replace Director decisions, AgentJob allowlists, role contracts, or human gates.
- **Source anchors:** `scripts/research_control/README.md`; `scripts/research_control/`.

## T10. Project-Control Scripts
- **What it is:** Python scripts for change classification, signal collection, signal type handling, project-improvement resolution, documentation-surface audit, and documentation-impact validation.
- **How it works:** Key files include `classify_project_changes.py`, `resolve_project_improvement.py`, `collect_project_improvement_signals.py`, `project_signal_types.py`, `validate_documentation_impact.py`, and `audit_documentation_surfaces.py`.
- **How it connects:** They support the project-system improvement loop and checkpoint gates outside physics continuation.
- **Source anchors:** `scripts/project_control/`; `.codex/skills/improve-project-system/SKILL.md`.

## T11. Bootstrap Memory Script
- **What it is:** The generator and validator for memory, wiki, registry, and derivative metadata systems.
- **How it works:** It refreshes generated outputs normally and can run `--validate-only`, docs-only, docs-validate-only, and strict-docs modes.
- **How it connects:** It is the main sync operation after changing sources or registries.
- **Source anchors:** `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`; `Makefile`.

## T12. Query Memory Script
- **What it is:** A command-line retrieval interface for memory status, lookup, and search.
- **How it works:** Workflows use it for preflight status and targeted queries, then verify influential results against canonical source rows.
- **How it connects:** It is the agent navigation tool for source-first memory.
- **Source anchors:** `.codex/skills/project-memory-system/scripts/query_memory.py`; `.codex/skills/continue-research/SKILL.md`.

## T13. Documentation Impact Validator
- **What it is:** A validator that checks documentation-impact receipts against live project-system changes.
- **How it works:** It verifies changed paths, reason codes, source docs, registries, generated derivatives, and required validators.
- **How it connects:** It makes sure operational changes are reflected in documentation or justified with a valid no-op rationale.
- **Source anchors:** `scripts/project_control/validate_documentation_impact.py`; `.agents/schemas/DOCUMENTATION_IMPACT_SCHEMA.md`.

## T14. Research-Control Validator
- **What it is:** The validator for task records, registries, handoffs, parent-child synthesis constraints, and diff allowlists.
- **How it works:** It can run normally or with `--check-diff` to verify the transaction’s changed paths against authority boundaries.
- **How it connects:** It is one of the primary checkpoint gates for both research and project-system work.
- **Source anchors:** `scripts/research_control/validate_research_control.py`; `scripts/research_control/README.md`.

## T15. Physics Progress Metrics Reporter
- **What it is:** A script that reports operational validation metrics and scientific progress metrics from tracked completions and registries.
- **How it works:** Operational counts summarize workflow health; scientific counts summarize tracked result fields and still require source artifact inspection.
- **How it connects:** It helps evaluate AI-system behavior without turning counts into scientific promotion.
- **Source anchors:** `scripts/research_control/report_physics_progress_metrics.py`; `research_control/README.md`.

## T16. Current Frontier Renderer
- **What it is:** A script-rendered snapshot system for `research_control/current_frontier.md`.
- **How it works:** It reads tracked control sources and can write, check, or emit JSON for the active frontier snapshot.
- **How it connects:** It keeps the reader-facing frontier synchronized while preserving `program_state.yaml`, handoff, and ledger authority.
- **Source anchors:** `scripts/research_control/render_current_frontier.py`; `research_control/current_frontier.md`.

## T17. Makefile Targets
- **What it is:** A top-level command surface for common validation tasks.
- **How it works:** Targets include `validate-memory`, `validate-project-control`, `validate-html-explainers`, and `audit-documentation-surfaces`.
- **How it connects:** It gives operators a compact way to run memory sync, Obsidian checks, unit tests, project-control validation, spec-depth lint, teaching QA, and research-control validators.
- **Source anchors:** `Makefile`.

## T18. Python Runtime and PyMuPDF
- **What it is:** The Python environment requirement for local repository scripts.
- **How it works:** The README specifies Python 3.12.13 in `.venv/`, and `requirements.txt` currently includes PyMuPDF for PDF text extraction.
- **How it connects:** It powers memory, validation, rendering, and PDF-derived retrieval functions.
- **Source anchors:** `README.md`; `requirements.txt`.

## T19. Unit Tests
- **What it is:** The test layer for memory-system and project-control behavior.
- **How it works:** Workflows call `python -m unittest discover -s tests` after changing memory-system scripts or validators.
- **How it connects:** Tests are part of the deterministic reliability net around the agent-control system.
- **Source anchors:** `tests/`; `Makefile`; `AGENTS.md`.

## T20. Spec Depth Lint
- **What it is:** A documentation-quality lint for source specs and explainer content depth.
- **How it works:** It flags shallow content blocks and directive-stub language that reads like instructions rather than finished documentation.
- **How it connects:** It helps keep public explainers website-worthy while remaining advisory rather than canonical content law.
- **Source anchors:** `scripts/spec_depth_lint.py`; `.agents/roles/research_ops/documentation-curator.v0.7.0.md`.

## T21. Publication Process Validator
- **What it is:** A validator for public explainer publication workflow.
- **How it works:** It checks source grounding, authority boundaries, no-network HTML, publication brief conformance, orphan explainers, and anti-template failures.
- **How it connects:** It is the quality-control bridge between repo docs and public website-grade pages.
- **Source anchors:** `scripts/validate_publication_process.py`; `.codex/skills/html-visual-explainer/SKILL.md`.

## T22. Mermaid and Playwright Rendering Stack
- **What it is:** The rendering stack for diagram-backed HTML and visual explainers.
- **How it works:** Governed tracked HTML requires build-time rendered diagrams rather than browser-side Mermaid execution, with screenshot QA for pilot pages.
- **How it connects:** It enables polished visual education without depending on external runtime services.
- **Source anchors:** `.codex/skills/visual-explainer/`; `.codex/skills/html-visual-explainer/SKILL.md`; `README.md`.

## T23. LaTeX and PDF Build Path
- **What it is:** The TeX-to-PDF derivative path for scientific manuscripts.
- **How it works:** Registered TeX files can require PDF derivatives, which are built and then registered or validated through memory bootstrap.
- **How it connects:** It provides reader-friendly scientific PDFs while keeping TeX as source authority.
- **Source anchors:** `ontology/tex/`; `ontology/pdfs/`; `.codex/skills/pdf-derivative-build/`.

## T24. Local Cache Boundary
- **What it is:** The rule that `.local/` stores retrieval caches, previews, semantic extracts, and experiments, not authority.
- **How it works:** `.local/` is ignored state and may be refreshed or cleaned, but it cannot be used as committed transaction evidence or source authority.
- **How it connects:** It gives the system fast local retrieval without poisoning canonical project state.
- **Source anchors:** `AGENTS.md`; `research_control/README.md`; `FOLDER_MAP.md`.

---

# 8. Folder and Repository Topology Components

## F01. `.agents/`
- **What it is:** The control-authority folder for agent roles and schemas.
- **How it works:** It defines permitted agent behavior, role contracts, authority levels, and execution schemas.
- **How it connects:** It is the formal contract layer for the AI research-agent system.
- **Source anchors:** `.agents/roles/`; `.agents/schemas/`; `FOLDER_MAP.md`.

## F02. `.codex/`
- **What it is:** The tooling folder for Codex skills, prompts, and agent configuration.
- **How it works:** It contains workflow procedures for continuation, memory, project improvement, visual explainers, user edit integration, wiki generation, and PDF derivatives.
- **How it connects:** It operationalizes the role and schema system inside the current Codex app harness.
- **Source anchors:** `.codex/skills/`; `README.md`; `FOLDER_MAP.md`.

## F03. `ontology/`
- **What it is:** The canonical source folder for ontology and exact-GR benchmark manuscripts.
- **How it works:** It contains Markdown ontology notes, registered TeX sources, and generated PDF derivatives.
- **How it connects:** It is the scientific source spine for the physics track.
- **Source anchors:** `ontology/`; `ontology/tex/`; `ontology/pdfs/`.

## F04. `legacy_ontology/`
- **What it is:** An archival source lane preserving an earlier ontology snapshot.
- **How it works:** It stores legacy TeX and PDF materials for comparison while live ontology remains elsewhere.
- **How it connects:** It helps preserve history without making old snapshots the active authority lane.
- **Source anchors:** `legacy_ontology/`; `FOLDER_MAP.md`.

## F05. `research_control/`
- **What it is:** The tracked control spine for research continuation.
- **How it works:** It holds approvals, design notes, handoffs, tasks, templates, missing-law records, current frontier, and active program state.
- **How it connects:** It is the command center connecting roles, registries, validators, and current physics status.
- **Source anchors:** `research_control/`; `research_control/README.md`.

## F06. `registries/`
- **What it is:** The CSV authority and generated metadata directory.
- **How it works:** It stores registries for files, sources, derivatives, roles, tasks, jobs, decisions, relationships, claims, memory layers, and improvement signals.
- **How it connects:** It is the machine-checkable ledger layer underneath the project.
- **Source anchors:** `registries/`; `FOLDER_MAP.md`.

## F07. `markdown/`
- **What it is:** A canonical Markdown source lane.
- **How it works:** It contains publication briefs and HTML explainer specs, among other source-backed project documentation.
- **How it connects:** It is the source layer from which GitHub-facing and HTML reader surfaces are generated.
- **Source anchors:** `markdown/`; `markdown/publication-briefs/`; `markdown/html-explainer-specs/`.

## F08. `github-facing/`
- **What it is:** A generated source-backed Markdown documentation layer for repository browsing.
- **How it works:** Pages are derived from Markdown source specs and are clearer reader surfaces, not canonical authority.
- **How it connects:** They are prime seed content for a website information architecture.
- **Source anchors:** `github-facing/`; `CONTEXT.md`.

## F09. `html/`
- **What it is:** The tracked generated HTML explainer folder.
- **How it works:** It contains standalone, no-network human-only pages generated from registered source specs and governed by publication briefs.
- **How it connects:** It is the closest existing analogue to the intended public website.
- **Source anchors:** `html/`; `.codex/skills/html-visual-explainer/SKILL.md`.

## F10. `wiki/`
- **What it is:** The generated wiki folder for object notes and indexes.
- **How it works:** It mirrors registered Markdown, TeX, PDF, and HTML objects into browseable notes.
- **How it connects:** It supports navigation and memory, but edits must happen in source files and registries.
- **Source anchors:** `wiki/`; `FOLDER_MAP.md`.

## F11. `scripts/`
- **What it is:** The Python tooling folder for project-control and research-control workflows.
- **How it works:** It contains classifiers, validators, renderers, checkpoint scripts, metrics reporters, and publication/documentation audits.
- **How it connects:** It is the deterministic enforcement layer beneath roles and skills.
- **Source anchors:** `scripts/`; `scripts/project_control/`; `scripts/research_control/`.

## F12. `tests/`
- **What it is:** The repository test suite and fixtures.
- **How it works:** It supports validator and memory-tooling changes through focused unit tests.
- **How it connects:** It is part of the reliability loop for project-system engineering.
- **Source anchors:** `tests/`; `Makefile`.

## F13. `tex_shared/`
- **What it is:** A shared source-support lane for TeX manuscript frontmatter or common includes.
- **How it works:** Scientific TeX documents import shared formatting and frontmatter components from this folder.
- **How it connects:** It supports manuscript consistency without carrying separate physics claims.
- **Source anchors:** `tex_shared/`; `ontology/tex/`.

## F14. `.local/`
- **What it is:** Ignored repository-local cache, retrieval, vault, preview, and semantic extraction state.
- **How it works:** It may store content semantics, Obsidian notes, memory indexes, render QA, PDF QA, and local HTML wikis.
- **How it connects:** It accelerates search and review while remaining non-authoritative and untracked.
- **Source anchors:** `.local/`; `AGENTS.md`; `FOLDER_MAP.md`.

---

# 9. Current Research Frontier for Website Use

## C01. Active Task and Handoff
- **What it is:** The active snapshot names `RT-20260629-049` and latest handoff `handoff-0344`.
- **How it works:** These identifiers point to the current routed research state and the latest transition evidence.
- **How it connects:** A website status badge may reference this as a dated snapshot, but should not treat it as independent authority.
- **Source anchors:** `research_control/current_frontier.md`; `research_control/program_state.yaml`.

## C02. Current Milestone: Matter Coupling
- **What it is:** The current burden family is `matter_coupling`, with strong anti-overread guards.
- **How it works:** The ledger records scoped evidence/precondition status, not matter-coupling adoption or derivation.
- **How it connects:** This is the safest public way to describe the live frontier: matter-sector formalization before coupling-law or Einstein-equation work.
- **Source anchors:** `research_control/current_frontier.md`; `registries/DISTANCE_TO_GR_LEDGER.csv`.

## C03. Next Recommended Action
- **What it is:** Run P5-T02 as one bounded `ontology-formalizer@0.2.0` transaction.
- **How it works:** The next task formalizes a source-side matter-sector discriminator obstruction target and no-target-import obligations.
- **How it connects:** It shows that the project is currently sharpening preconditions, not claiming downstream GR completion.
- **Source anchors:** `research_control/program_state.yaml`; `research_control/current_frontier.md`.

## C04. Exact Blocked Claims
- **What it is:** The current frontier explicitly blocks ontology edit, source-law adoption, `MetricData(E)` adoption, `g_eff` scope expansion, matter coupling, Einstein equations, benchmark promotion, completed derivation, and global rejection.
- **How it works:** These blocked claims are listed to prevent readers from inferring too much from accepted scoped evidence.
- **How it connects:** A website should make these boundaries visible anywhere it presents current progress.
- **Source anchors:** `research_control/current_frontier.md`.

## C05. Validation Status Snapshot
- **What it is:** The current frontier records recent PASS status for memory bootstrap, validate-only, graph freshness, documentation impact, and research-control validation.
- **How it works:** These passes show operational consistency of tracked state at the snapshot point.
- **How it connects:** They indicate process health but are not scientific proof.
- **Source anchors:** `research_control/current_frontier.md`.

---

# 10. Website Positioning Guidance

## W01. Safe One-Sentence Project Pitch
- **What it is:** “The Æther-Flow project is a dual physics and AI research program that presents an exact-GR-compatible interpretation of relativity while building a governed AI research-agent system for pursuing the still-open derivation from deeper substrate structure.”
- **How it works:** It highlights the physics idea, exact-GR discipline, open derivation, and AI research infrastructure in one sentence.
- **How it connects:** It avoids claiming a completed derivation while still sounding confident and promotional.
- **Source anchors:** `README.md`; `AGENTS.md`.

## W02. Claims to Use
- **What it is:** Use “exact-GR benchmark,” “GR-consistent interpretation,” “open first-principles derivation burden,” “source-backed research-control system,” and “human-scaffolded AI research-agent workflow.”
- **How it works:** These terms match the project’s authority hierarchy and current scientific status.
- **How it connects:** They let the site promote the project without overstating proof status.
- **Source anchors:** `README.md`; `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`.

## W03. Claims to Avoid
- **What it is:** Avoid “GR has been derived,” “new tested gravity prediction,” “autonomous proof system,” “benchmark promoted,” “matter coupling solved,” or “Einstein equations derived from Æther.”
- **How it works:** Those claims are blocked by current frontier state, exact-closure boundaries, and human-gated promotion rules.
- **How it connects:** This protects public trust and aligns the website with the repository’s own control records.
- **Source anchors:** `research_control/current_frontier.md`; `research_control/design/gr_derivation_burden_map.md`.

## W04. Suggested Website Navigation
- **What it is:** A site map can begin with Overview, Ontology, Exact-GR Benchmark, Derivation Roadmap, Research-Agent System, Claim Gates, Memory and Registries, Publications, and Contributor Requirements.
- **How it works:** This mirrors the repo’s own reviewed explainers and separates physics content from workflow content.
- **How it connects:** It gives readers both a conceptual journey and a technical audit trail.
- **Source anchors:** `README.md`; `registries/PUBLICATION_BRIEF_REGISTRY.csv`; `github-facing/`.

## W05. Homepage Hero Structure
- **What it is:** A homepage hero should state the dual mission, exact-GR status, and open derivation burden immediately.
- **How it works:** Follow with three cards: “The Ontology,” “The Exact Benchmark,” and “The Research-Agent System.”
- **How it connects:** This gives readers the project’s whole logic before they encounter dense physics or governance details.
- **Source anchors:** `README.md`; `html/project-overview-explainer.html`.

## W06. Trust and Transparency Section
- **What it is:** A dedicated section explaining what the project claims, what it does not claim, and how claims are gated.
- **How it works:** Use the Distance-to-GR and blocked-claims language as public transparency instead of burying caveats.
- **How it connects:** It turns caution into a strength: the project is ambitious, but not sloppy.
- **Source anchors:** `research_control/current_frontier.md`; `github-facing/claim-gates-explainer.md`.

## W07. AI-System Promotion Angle
- **What it is:** Present the AI system as a research-governance and staged-autonomy experiment, not an oracle.
- **How it works:** Emphasize bounded AgentJobs, role contracts, validators, source-first memory, negative-result preservation, and human-gated promotion.
- **How it connects:** This makes the AI track valuable even while the physics derivation remains open.
- **Source anchors:** `research_control/README.md`; `.codex/skills/continue-research/SKILL.md`.

## W08. Physics Promotion Angle
- **What it is:** Present the physics as an exact-GR-compatible ontology and benchmark with a rigorous future derivation program.
- **How it works:** Explain that the effective theory inherits GR’s predictions while the ontology proposes a deeper account of what that geometry may be about.
- **How it connects:** This preserves scientific caution while making the philosophical and mathematical ambition legible.
- **Source anchors:** `ontology/tex/aether_flow_exact_closure_note.tex`; `ontology/aether-and-aether-flow.md`.

---

# 11. Quick Source Map for Site Builders

## S01. Best Starting Sources
- **What it is:** The fastest orientation path through the repository.
- **How it works:** Read `README.md`, `AGENTS.md`, `ontology/aether-and-aether-flow.md`, `research_control/README.md`, `research_control/current_frontier.md`, and the reviewed GitHub-facing explainers.
- **How it connects:** This sequence gives both narrative and authority boundaries before low-level file archaeology.
- **Source anchors:** `README.md`; `AGENTS.md`; `research_control/current_frontier.md`.

## S02. Best Physics Sources
- **What it is:** The canonical physics source family.
- **How it works:** Begin with exact-closure sequence overview, exact-closure note, foundations, dynamics, consistency, relativistic recovery, and flow geometry.
- **How it connects:** These sources define the exact-GR benchmark and the ontology’s mathematical interpretation.
- **Source anchors:** `ontology/tex/*.tex`; `registries/TEX_SOURCE_REGISTRY.csv`.

## S03. Best AI-System Sources
- **What it is:** The core sources for explaining the agent workflow.
- **How it works:** Read research-control README, continue-research skill, improve-project-system skill, role contracts, schemas, and registries.
- **How it connects:** These sources describe the system’s actual operating logic rather than just its aspiration.
- **Source anchors:** `research_control/README.md`; `.codex/skills/`; `.agents/roles/`; `.agents/schemas/`.

## S04. Best Website Source Materials
- **What it is:** The existing public documentation and publication layer.
- **How it works:** Use `github-facing/`, `html/`, `markdown/publication-briefs/`, `markdown/html-explainer-specs/`, and `PUBLICATION_BRIEF_REGISTRY.csv` as the website seed corpus.
- **How it connects:** These are already organized for readers and grounded in source-authority constraints.
- **Source anchors:** `github-facing/`; `html/`; `markdown/`; `registries/PUBLICATION_BRIEF_REGISTRY.csv`.

## S05. Best Operator Sources
- **What it is:** The implementation and reproducibility layer for contributors.
- **How it works:** Use `README.md` requirements, `Makefile`, `requirements.txt`, project-control scripts, research-control scripts, and tests.
- **How it connects:** These sources explain how to run validation, refresh memory, audit docs, and keep the repo coherent.
- **Source anchors:** `Makefile`; `requirements.txt`; `scripts/`; `tests/`.

---

# 12. Final Website Framing

The public story should feel ambitious but disciplined: a modern ontology-first interpretation of relativity, constrained by exact GR, paired with a serious AI research-control system for attacking the open derivation problem. The project is valuable today because it has a stable exact-GR benchmark, a coherent ontology vocabulary, a formal derivation roadmap, and a governance system that preserves both progress and failure.

The website should make the project’s caution part of its identity. The strongest message is not “we already solved GR,” but “we built a source-backed physics and AI research system that knows exactly what has been adopted, what remains open, how future derivation attempts are routed, and which claims cannot yet be made.”
