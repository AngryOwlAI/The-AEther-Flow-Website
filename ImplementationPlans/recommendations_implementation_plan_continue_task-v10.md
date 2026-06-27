<!-- authority: draft/control implementation plan -->

# Recommendations Implementation Plan for Continue Research, v8

**Filename:** `recommendations_implementation_plan_continue_task-v8.md`  
**Intended repo path:** `implementations_plans/recommendations_implementation_plan_continue_task-v8.md` unless the local repository has a different already-authorized implementation-plan directory.  
**Prepared for:** local AEther-Flow AI agents using the repository's governed Continue Research functionality.  
**Plan status:** draft/control implementation plan.  
**Physics authority:** none.  
**Project-control authority:** none until ingested by a bounded AgentJob and validated under the local research-control spine.  
**Primary implementation rule:** every phase and every task below must be implemented through exactly one bounded `/continue-research` invocation per task, unless the invocation stops under a tracked human gate, validation failure, or explicit Director no-role-fit decision.

---

## 0. Control Notice

This plan operationalizes the recommendations from the project review into repo-local tasks. It is intentionally written for the local AI agents, not for casual readers. The goal is to convert the review recommendations into a staged implementation sequence that preserves the AEther-Flow control discipline: Director routing, one bounded AgentJob per invocation, explicit claim boundaries, role contracts, completion receipts, Distance-to-GR hygiene, validators, generated-system synchronization, handoffs, and checkpoint discipline.

This plan does **not** claim that GR has been derived. It does **not** promote `M_src`, `g_eff`, matter coupling, Einstein equations, benchmark status, or any completed derivation. It does **not** authorize canonical ontology edits, source-law adoption, `MetricData(E)` adoption, `g_eff` scope expansion, coupling-law adoption, stress-energy semantics, matter-coupling derivation, Einstein equations, benchmark promotion, Gate Chair closure, future source-extension impossibility, or global theory rejection.

The plan is a router and implementation scaffold. It is not a proof surface.

### 0.1 Source Basis to Inspect Before Using This Plan

Every implementation task must begin with the normal Continue Research preflight, then inspect the canonical local versions of the following files when relevant:

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0264.yaml`
- `research_control/handoffs/handoff-0264.md`
- `research_control/tasks/RT-20260614-230/00_TASK.yaml`
- `research_control/tasks/RT-20260614-230/artifacts/259_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_COUPLING_LAW_CANDIDATE_OR_OBSTRUCTION.tex`
- `research_control/tasks/RT-20260614-231/00_TASK.yaml`
- `research_control/tasks/RT-20260614-231/jobs/completions/AJC-AJ-RT-20260614-231-001.yaml`
- `research_control/tasks/RT-20260614-231/artifacts/260_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_COUPLING_LAW_SMUGGLING_AUDIT.tex`
- `research_control/design/gr_derivation_burden_map.md`
- `research_control/design/mathematical_decisiveness_completion_contract.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `scripts/research_control/validate_research_control.py`
- `scripts/research_control/report_physics_progress_metrics.py`
- `research_control/current_frontier.md`

If any of these files are absent, moved, superseded, or contradicted by newer authoritative control state, the local Director must treat this plan as secondary and route a bounded state-resolution task before implementing downstream phases.

### 0.2 Current-State Assumption for This Plan

This plan assumes the latest authoritative research state is:

```yaml
active_task_id: "RT-20260614-231"
latest_handoff_id: "handoff-0264"
current_status: "post_matter_coupling_coupling_law_audited_pending_refuter_stress_no_adoption"
next_recommended_role: "refuter@0.2.0"
next_recommended_scope: "bounded Refuter stress of CouplingLaw_src^{GSC-cand}(E;G^beta,T_src(E))"
```

If `program_state.yaml` no longer matches that assumption, Phase 0 must first reconcile the plan with the newer state. Do not rewind the project to `RT-20260614-231`. Do not treat this plan's state assumption as authority over local tracked state.

### 0.3 Filename Version Boundary

The requested filename contains `v8`. The local repository may already contain references to other implementation-plan versions. The filename version here must **not** be interpreted as permission to downgrade the Continue Research skill, route contracts, mathematical decisiveness enforcement, validators, role versions, or any active v9 control state. Local agents must use the current tracked `Continue Research` skill and active repository contracts.

---

## 1. Universal Continue Research Implementation Protocol

Every task in every phase must use this protocol.

### 1.1 Operator Invocation Template

For each task, the human or supervising process should invoke Continue Research with a task-specific instruction of this form:

```text
Use /continue-research to implement exactly PLAN-<PHASE>-<TASK> from implementations_plans/recommendations_implementation_plan_continue_task-v8.md as one bounded AgentJob. Preserve all claim boundaries. Do not implement any later task in this invocation. If the task requires protected authority, stop with a tracked human-gate or no-role-fit result rather than expanding authority.
```

Examples:

```text
Use /continue-research to implement exactly PLAN-P1-T1 from implementations_plans/recommendations_implementation_plan_continue_task-v8.md as one bounded AgentJob. Preserve all claim boundaries. Do not implement P1-T2 or any later task in this invocation.
```

```text
Use /continue-research to implement exactly PLAN-P3-T1 from implementations_plans/recommendations_implementation_plan_continue_task-v8.md as one bounded Refuter AgentJob. Preserve no coupling-law adoption, no matter-coupling derivation, no stress-energy semantics, no Einstein equations, and no downstream GR promotion.
```

### 1.2 Mandatory Preflight for Each Task

Each invocation must perform the repository's normal Continue Research preflight:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup <object-id-or-path> --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "<targeted phrase>" --limit 10 --json
.venv/bin/python scripts/research_control/continue_research.py --json
```

Memory hits are retrieval hints only. Any hit that affects routing, claims, source selection, or implementation must be followed by inspection of the canonical source path or source-registry row.

### 1.3 One-Task Rule

Each task below is an upper bound. A single Continue Research invocation may implement **less** than the requested task if it reaches a lawful stop condition, but it may not implement more than one plan task.

Forbidden:

- bundling multiple phase tasks into one AgentJob;
- opportunistic validator repair outside the task boundary;
- mixing physics continuation with project-system repair unless the AgentJob explicitly authorizes both;
- using generated derivatives, registry status, memory status, validator status, file order, or commit status as mathematical premises;
- treating this plan as a source of physics authority.

### 1.4 Required Completion Receipt Shape

Every task completion must state:

```yaml
plan_task_id: "PLAN-Px-Ty"
plan_task_title: "..."
plan_task_status: "completed | blocked | human_gate_required | validation_failed | no_role_fit | superseded_by_current_state"
implemented_scope: "..."
not_implemented_scope:
  - "..."
claim_boundary_preserved: true
physics_promotion_authorized: false
```

Physics tasks governed by the mathematical decisiveness contract must additionally include:

```yaml
physics_progress_status:
  status: "..."
  target_derivation_milestone: "..."
  milestone_burden: "..."
  explanation: "..."
  physics_promotion_authorized: false
  promotion_authority_path: ""
distance_to_gr_delta:
  changed: true_or_false
  burden_id: "..."
  milestone: "..."
  old_status: "..."
  new_status: "..."
  ledger_row_updated: true_or_false
  ledger_path: "registries/DISTANCE_TO_GR_LEDGER.csv"
  downstream_unlocked:
    - "..."
  downstream_still_blocked:
    - "..."
  explanation: "..."
mathematical_payload_manifest:
  - payload_id: "PAYLOAD-001"
    payload_type: "definition | lemma | theorem | finite_model | countermodel | explicit_witness | obstruction | construction | dependency_map_update | packet_selection | source_extension_classification"
    object_name: "..."
    claim_status: "draft/control | proposal-only | accepted scoped source-extension | obstruction | frozen negative"
    source_path: "..."
    burden_effect: "..."
    summary: "..."
forbidden_conclusion_summary:
  physics_promotion_authorized: false
  authorized_scope: "..."
  forbidden_conclusions:
    - "canonical ontology edit"
    - "source-law adoption"
    - "MetricData(E) adoption"
    - "g_eff scope expansion"
    - "coupling-law adoption"
    - "matter-coupling derivation"
    - "stress-energy semantics"
    - "Einstein equations"
    - "benchmark promotion"
    - "completed derivation"
  summary: "..."
```

### 1.5 Standard Validators

Unless a task's AgentJob narrows this list, each implementation task must run the repository's normal validators after edits:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python scripts/project_control/classify_project_changes.py --json
.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py
git diff --check
```

If the task authorizes Python or unit-test changes, add targeted tests and run them explicitly.

### 1.6 Checkpoint Rule

After a successful state-changing task, use the repo checkpoint path rather than manual staging:

```zsh
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py
```

Do not push unless explicitly requested by the human operator.

---

## 2. Phase Overview

| Phase | Name | Primary purpose | Physics authority? | Typical role family |
|---|---|---|---:|---|
| P0 | Plan intake and route protection | Put this plan under control without changing science | No | Director / Documentation Curator / Project-Control Maintainer |
| P1 | Frontier synchronization | Remove stale frontier drift and add stale-state guards | No | Project-Control Maintainer / Validator Engineer |
| P2 | Plan-aware Continue Research routing | Make this plan consumable one task at a time | No | Director / Project-Control Maintainer |
| P3 | Coupling-law Refuter stress | Execute the immediate active physics next step | Draft/control only | Refuter |
| P4 | Positive emergence obligations | Add source-to-physics obligation map | Draft/control only | Ontology Formalizer / Theoretical Selector |
| P5 | Finite toy model v2 | Rebuild finite toy route with intrinsic invariants | Draft/control only | Selector / Candidate Constructor / Auditor / Refuter |
| P6 | Scoped metric nomenclature | Prevent `g_eff` overread | No physics promotion | Documentation Curator / Validator Engineer |
| P7 | Matter-coupling success criteria | Define positive coupling-law success, not only anti-smuggling | Draft/control only | Ontology Formalizer / Candidate Constructor |
| P8 | Formal finite checker and proof-kernel support | Add support-only finite verification tooling | Support only | Validator Engineer / Candidate Constructor |
| P9 | Gate authorization semantics | Clarify new gate vs consumed authorization | No | Project-Control Maintainer / Validator Engineer |
| P10 | Graph-continuity validation | Validate task, job, handoff, ledger, and approval links | No | Validator Engineer |
| P11 | Validation PASS vs physics PASS separation | Make control-validity visually distinct from science truth | No | Project-Control Maintainer / Documentation Curator |
| P12 | External review packet | Produce skeptical-reader source-backed review packet | Explanatory only | Documentation Curator / Theoretical Selector |
| P13 | Final integration and release gate | End-to-end validation, docs sync, handoff, checkpoint | No new physics | Director / Process Integrity Auditor |

---

# Phase P0: Plan Intake and Route Protection

## Phase Goal

Ingest this implementation plan into the repository as a non-authoritative draft/control implementation plan and ensure that later tasks can cite it without treating it as physics authority.

## Phase Claim Boundary

Allowed:

- add this Markdown implementation plan to the repo;
- register documentation impact if required;
- add a control note or index entry if the repo convention requires it;
- record that this plan is non-authoritative for physics claims.

Forbidden:

- changing `program_state.yaml` physics status except through normal task completion if local policy requires it;
- changing Distance-to-GR physics statuses;
- adopting source laws, `MetricData(E)`, `g_eff`, coupling law, matter coupling, Einstein equations, benchmark status, or completed derivation;
- using the filename `v8` to override active role or skill versions.

---

## PLAN-P0-T1: Ingest the Plan File

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P0-T1 from implementations_plans/recommendations_implementation_plan_continue_task-v8.md as one bounded non-physics plan-intake AgentJob. Add the implementation plan file only, preserve all physics claim boundaries, and do not implement downstream recommendations.
```

**Recommended role:** `documentation-curator@active` or `project-control-maintainer@active`, selected by Director according to current role registry.

**Task type:** `project_system_recommendations_plan_intake_v8`

**Allowed writes:**

- `implementations_plans/recommendations_implementation_plan_continue_task-v8.md`
- task-local records under the new `research_control/tasks/<task_id>/`
- registries required for the task transaction
- generated memory/wiki indexes authorized by the AgentJob

**Expected outputs:**

- the plan file in the repo;
- task `00_TASK.yaml`;
- DDR;
- AgentJob;
- completion receipt;
- handoff pair;
- documentation impact receipt if required.

**Acceptance criteria:**

- file exists at the selected repo path;
- completion explicitly says the plan has no physics authority;
- no scientific registry status changes except task metadata;
- validators pass.

---

## PLAN-P0-T2: Create a Plan Implementation Index

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P0-T2 from recommendations_implementation_plan_continue_task-v8.md as one bounded project-control task. Create a machine-readable implementation index for the plan if and only if local conventions allow it. Do not implement any phase task.
```

**Recommended role:** `project-control-maintainer@active`

**Objective:** Create an optional index that local agents can use to identify plan task IDs, phase dependencies, and completion state. If the repo already has an equivalent mechanism, record that no new index is needed.

**Candidate output path:**

- `research_control/implementation_plan_indexes/recommendations_implementation_plan_continue_task-v8.yaml`

If this directory does not exist and no convention supports it, stop with `no_role_fit` or `not_required` rather than inventing uncontrolled infrastructure.

**Index shape:**

```yaml
plan_id: "recommendations_implementation_plan_continue_task-v8"
plan_path: "implementations_plans/recommendations_implementation_plan_continue_task-v8.md"
claim_authority: "none"
implementation_mode: "one_continue_research_agentjob_per_plan_task"
phases:
  - phase_id: "P0"
    status: "in_progress"
    tasks:
      - plan_task_id: "PLAN-P0-T1"
        status: "completed | pending | blocked"
        completion_path: "..."
```

**Acceptance criteria:**

- index is explicitly non-authoritative;
- index does not replace `program_state.yaml`, handoffs, registries, or task records;
- validators pass.

---

## PLAN-P0-T3: Plan Boundary Audit

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P0-T3 from recommendations_implementation_plan_continue_task-v8.md as one bounded control-boundary audit. Audit the ingested plan for forbidden physics-promotion language, stale-state overread, and authority expansion. Do not repair downstream code unless the AgentJob authorizes only this audit's local artifacts.
```

**Recommended role:** `process-integrity-auditor@active` or `project-control-maintainer@active`

**Audit dimensions:**

- Does the plan claim GR is derived?
- Does the plan treat scoped `g_eff` as a physical metric?
- Does the plan treat source-purity audit as matter coupling?
- Does the plan treat validator success as theorem success?
- Does the plan ask local agents to bypass Continue Research?
- Does the plan require protected authority without human gate?
- Does the plan conflict with the active `Continue Research` skill?

**Expected output:**

- task-local audit artifact, e.g. `artifacts/recommendations_plan_v8_boundary_audit.md`.

**Acceptance criteria:**

- audit verdict is `pass`, `pass_with_local_limitations`, or `precise_boundary_failure`;
- any failure identifies the exact phrase and recommended local repair;
- no physics claims promoted.

---

# Phase P1: Frontier Synchronization and Stale-State Guard

## Phase Goal

Fix the mismatch risk where human-facing or agent-facing frontier summaries can lag behind authoritative state. The review found that `current_frontier.md` can become stale relative to `program_state.yaml`, handoffs, and the Distance-to-GR ledger.

## Phase Claim Boundary

Allowed:

- add stale-state checks;
- generate or update human-readable frontier summaries from authoritative control sources;
- document that frontier summaries are non-authoritative;
- add validation tests that detect mismatches.

Forbidden:

- changing physics statuses to match stale summaries;
- treating generated summaries as authority over `program_state.yaml`, handoffs, registries, or registered TeX sources;
- altering Distance-to-GR statuses except through a bounded physics completion.

---

## PLAN-P1-T1: Frontier Drift Detector Specification

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P1-T1 as one bounded project-system specification task. Specify a frontier drift detector comparing current_frontier.md, program_state.yaml, latest handoff, and DISTANCE_TO_GR_LEDGER.csv. Do not write the validator yet unless the Director selects implementation instead of specification.
```

**Recommended role:** `project-control-maintainer@active` or `validator-engineer@active`

**Objective:** Produce a design note for a deterministic stale-state detector.

**Required checks:**

1. `current_frontier.md` active task equals `research_control/program_state.yaml.active_task_id` or is explicitly marked stale.
2. `current_frontier.md` latest handoff equals `program_state.yaml.latest_handoff_id` or is explicitly marked stale.
3. The latest handoff `task_id` equals or descends from the active task.
4. Distance-to-GR rows referenced in `current_frontier.md` match ledger statuses or include an explicit snapshot date.
5. If the file is intentionally historical, it must contain a machine-readable `snapshot_after_task_id` and `not_current_authority: true` marker.

**Expected output path:**

- `research_control/design/frontier_drift_detector_spec.md`

**Acceptance criteria:**

- spec states source priority order;
- spec distinguishes stale warning from validation hard failure;
- spec includes examples of passing and failing states.

---

## PLAN-P1-T2: Implement Frontier Drift Detector

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P1-T2 as one bounded validator-engineering task. Implement the frontier drift detector specified in PLAN-P1-T1. Do not update physics frontier content except test fixtures or explicitly authorized non-authoritative generated summaries.
```

**Recommended role:** `validator-engineer@active`

**Candidate implementation:**

- Add function(s) to `scripts/research_control/validate_research_control.py`, or create a narrow helper under `scripts/research_control/validate_frontier_drift.py` and call it from the main validator.

**Required behavior:**

- hard fail if `current_frontier.md` claims to be current but disagrees with `program_state.yaml`;
- warning or pass if `current_frontier.md` is marked as a historical snapshot;
- report exact mismatched fields;
- do not parse scientific claims beyond explicit task IDs, handoff IDs, status strings, and ledger fields.

**Tests:**

- fixture where frontier matches program state;
- fixture where frontier is stale and unmarked;
- fixture where frontier is stale but explicitly marked historical;
- fixture where ledger row mismatches a claimed current status.

**Acceptance criteria:**

- `validate_research_control.py` reports drift deterministically;
- unit tests pass if the repo has a test harness;
- generated-memory bootstrap and research-control validation pass.

---

## PLAN-P1-T3: Generate or Refresh Current Frontier Summary

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P1-T3 as one bounded documentation/control task. Generate or refresh the current frontier summary from authoritative state. Do not change the underlying physics state.
```

**Recommended role:** `documentation-curator@active` or `project-control-maintainer@active`

**Objective:** Replace stale hand-authored frontier summaries with a generated or clearly synchronized non-authoritative surface.

**Expected behavior:**

- If `current_frontier.md` remains hand-maintained, update it to the latest authoritative state and add `snapshot_after_task_id`, `latest_handoff_id`, and `not_authority` markers.
- If generation is implemented, create a script such as `scripts/research_control/render_current_frontier.py` that reads:
  - `program_state.yaml`
  - latest handoff YAML
  - `DISTANCE_TO_GR_LEDGER.csv`
  - latest completion receipt
- The generated output must contain a prominent authority warning.

**Acceptance criteria:**

- human-readable frontier reflects the actual current active task and handoff;
- no physics status is invented by the renderer;
- drift detector passes.

---

## PLAN-P1-T4: Add Handoff-to-Frontier Synchronization Rule

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P1-T4 as one bounded project-control task. Add a rule requiring state-changing physics completions to either refresh current_frontier.md or mark it stale. Do not alter any physics artifact.
```

**Recommended role:** `project-control-maintainer@active`

**Candidate changes:**

- update `research_control/AGENTS.md` or a design note;
- update completion checklist documentation;
- optionally add validator support.

**Acceptance criteria:**

- future state-changing completions have a deterministic frontier-sync obligation;
- the obligation is control hygiene only, not physics authority.

---

# Phase P2: Plan-Aware Continue Research Routing

## Phase Goal

Make this plan consumable by local agents without inviting multi-task bundling or authority expansion.

## Phase Claim Boundary

Allowed:

- add a plan-task selection convention;
- add metadata or documentation so local agents can implement one plan task at a time;
- route plan tasks as project-system, documentation, or physics tasks depending on content.

Forbidden:

- changing the meaning of `/continue-research` globally without a bounded role and validators;
- giving the implementation plan authority over tracked research state;
- creating a parallel task system outside `research_control/tasks`.

---

## PLAN-P2-T1: Add Plan Task Invocation Guidance

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P2-T1 as one bounded documentation-control task. Add guidance for invoking individual plan tasks through Continue Research. Do not implement any plan task beyond the guidance itself.
```

**Recommended role:** `documentation-curator@active`

**Candidate output paths:**

- `research_control/design/continue_research_plan_task_invocation.md`
- or a narrow section in `.codex/skills/continue-research/SKILL.md` if the AgentJob authorizes skill documentation edits.

**Required content:**

- one AgentJob per plan task;
- task ID must be named in invocation;
- Director must respect current state over plan assumptions;
- protected authority stops at human gate;
- no empty commits for read-only or blocked tasks.

**Acceptance criteria:**

- local agents can identify plan task boundaries;
- no routing authority is expanded.

---

## PLAN-P2-T2: Add Plan Task Completion Marker Convention

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P2-T2 as one bounded project-control task. Add a convention for recording plan_task_id in task completions. Do not backfill old tasks unless explicitly authorized.
```

**Recommended role:** `project-control-maintainer@active`

**Required convention:**

```yaml
implementation_plan_receipt:
  plan_id: "recommendations_implementation_plan_continue_task-v8"
  plan_path: "implementations_plans/recommendations_implementation_plan_continue_task-v8.md"
  plan_task_id: "PLAN-Px-Ty"
  plan_phase_id: "Px"
  implemented_task_scope: "..."
  downstream_tasks_not_implemented:
    - "PLAN-Px-Ty+1"
```

**Acceptance criteria:**

- new completions can cite the plan task they implemented;
- validators do not require this field for unrelated tasks unless a separate rollout task authorizes enforcement.

---

## PLAN-P2-T3: Add Plan Dependency Guard

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P2-T3 as one bounded validator or control-spec task. Add a guard or documented checklist preventing later plan tasks from running before prerequisite tasks complete. Do not implement downstream phases.
```

**Recommended role:** `validator-engineer@active` for code, `project-control-maintainer@active` for spec.

**Minimal dependency rules:**

- P1 tasks should follow P0 intake.
- P3 may run immediately if current authoritative state still requires the Refuter stress, even if P1/P2 are incomplete.
- P4, P5, and P7 should incorporate the outcome of P3 if P3 has completed.
- P6, P9, P10, and P11 may run as project-system improvements independent of P3, but must not alter physics state.
- P12 external review packet should occur after P3 and after P6 nomenclature cleanup when possible.

**Acceptance criteria:**

- dependency guard is advisory unless explicitly validated by a new schema;
- guard reports skipped prerequisites in completion notes.

---

# Phase P3: Immediate Coupling-Law Refuter Stress

## Phase Goal

Execute the current recommended physics next step: a bounded Refuter stress test of the audited draft/control source-side coupling-law candidate `CouplingLaw_src^{GSC-cand}(E;G^beta,T_src(E))`.

## Phase Claim Boundary

Allowed:

- stress-test the audited draft/control candidate;
- classify stress survival, precise obstruction, or freeze need;
- sharpen proof obligations;
- update `matter_coupling` ledger only within the stress-test status boundary.

Forbidden:

- adopting a coupling law;
- deriving or adopting matter coupling;
- importing stress-energy semantics;
- adopting `MetricData(E)`;
- expanding scoped `g_eff`;
- deriving Einstein equations;
- promoting benchmark status;
- claiming completed derivation;
- claiming source-extension impossibility or rejecting the global theory unless a separate authorized no-go theorem exists.

---

## PLAN-P3-T1: Director Route Coupling-Law Refuter Packet

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P3-T1 as one bounded Director routing task for the next active physics step. If program_state.yaml still points to handoff-0264 and RT-20260614-231, create exactly one Refuter AgentJob for CouplingLaw_src^{GSC-cand}. If state has moved on, supersede this task with a current-state reconciliation result.
```

**Recommended role selected by Director:** `refuter@0.2.0`

**Target derivation milestone:** `matter_coupling`

**Milestone burden:** Stress the audited draft/control source-side coupling-law candidate before any adoption, matter-coupling derivation, Einstein-equation, benchmark, or completed-derivation route.

**Required read paths:**

- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0264.yaml`
- `research_control/handoffs/handoff-0264.md`
- `research_control/tasks/RT-20260614-230/artifacts/259_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_COUPLING_LAW_CANDIDATE_OR_OBSTRUCTION.tex`
- `research_control/tasks/RT-20260614-231/artifacts/260_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_COUPLING_LAW_SMUGGLING_AUDIT.tex`
- `research_control/design/gr_derivation_burden_map.md`
- `research_control/design/mathematical_decisiveness_completion_contract.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`

**Expected output:**

- DDR selecting Refuter;
- AgentJob with parent-child synthesis;
- role execution record or task overlay;
- no scientific result yet if this task is only route creation.

**Acceptance criteria:**

- exactly one Refuter AgentJob is created or reused;
- no stress result is fabricated in the routing record;
- claim boundary matches handoff-0264.

---

## PLAN-P3-T2: Execute Coupling-Law Refuter Stress

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P3-T2 as one bounded Refuter stress test of CouplingLaw_src^{GSC-cand}(E;G^beta,T_src(E)). Preserve no coupling-law adoption, no matter-coupling derivation, no stress-energy semantics, no Einstein equations, and no downstream promotion.
```

**Recommended role:** `refuter@0.2.0`

**Stress dimensions:**

1. **Source coupling-token update ambiguity**  
   Determine whether distinct source-token updates yield indistinguishable or conflicting admissibility outcomes without a hidden target criterion.

2. **Admissibility predicate nonuniqueness**  
   Test whether multiple incompatible predicates `A_E` satisfy all declared source-side constraints. If yes, classify whether this is harmless gauge freedom, underdetermination, or a fatal obstruction.

3. **Hidden stress-energy pressure**  
   Attempt to interpret `J_E`, `A_E`, or `K_E` as requiring stress-energy, matter action, conservation law, empirical matter sector, or field-equation semantics. If any is required, fail or bottom-route the candidate.

4. **Target import pressure**  
   Attempt to force target topology, target atlas, target metric, Lorentzian signature, proper time, detector semantics, or benchmark success into the candidate.

5. **Transition inverse behavior**  
   If `Theta_E` transports coupling-token relations, test whether inverse transitions are defined where required and whether failure is bottom-controlled.

6. **Transition cocycle behavior**  
   For composable source transitions `tau_1`, `tau_2`, test whether transport under `tau_2 tau_1` agrees with sequential transport up to declared source equivalence, or else returns bottom/obstruction.

7. **Bottom completeness**  
   Confirm absent, ambiguous, noncoherent, target-repaired, detector-repaired, benchmark-repaired, and process-repaired inputs all fail closed.

8. **Source-law adoption laundering**  
   Test whether scoped precondition evidence, scoped `g_eff`, or transition compatibility is being silently converted into source-law adoption.

9. **Coupling-law adoption laundering**  
   Test whether naming a candidate `CouplingLaw` is being used as if an adopted universal coupling law exists.

10. **Scoped `g_eff` overread**  
    Test whether compatibility with scoped source-extension `g_eff` is functioning as target metric import or scope expansion.

11. **`MetricData(E)` adoption laundering**  
    Test whether any argument assumes adopted `MetricData(E)` rather than scoped evidence.

12. **Einstein-equation pressure**  
    Test whether any derivation step assumes field equations, action variation, stress-energy conservation, or Bianchi identities.

13. **Benchmark-promotion pressure**  
    Test whether exact-GR benchmark success is being treated as evidence for the candidate.

14. **Nontriviality test**  
    Determine whether the candidate remains mathematically nontrivial after all forbidden semantics are removed. If it becomes vacuous, classify as a precise obstruction rather than a pass.

15. **Positive-support test**  
    Identify the minimal positive source-only data required for a non-bottom coupling-token update. If no such data exists, record the obstruction.

**Allowed result classes:**

```yaml
refuter_result_type: "stress_survived_pending_selector | precise_obstruction | route_frozen | invalid_under_claim_boundary"
```

**Required output artifact:**

- `research_control/tasks/<new-task>/artifacts/<N>_COUPLING_LAW_REFUTER_STRESS_TEST.tex`

**Completion must include:**

- `physics_progress_status`
- `distance_to_gr_delta`
- `mathematical_payload_manifest`
- `forbidden_conclusion_summary`
- `freeze_criteria_status` if obstruction or repeated burden is present
- `route_cycle_control`
- `parent_child_synthesis`

**Acceptance criteria:**

- stress result is decisive within its scope;
- if stress survives, the next lawful role is a Theoretical Continuation Selector or Gate Chair only if conditions support it;
- if obstruction is found, obstruction has a stable identifier, exact scope, failed object, exact failure, consequence, and forbidden overread;
- no adoption or downstream claim is made.

---

## PLAN-P3-T3: Post-Stress Theoretical Continuation Selector

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P3-T3 as one bounded Theoretical Continuation Selector task after the coupling-law Refuter stress result exists. Select one next lawful route: repair constructor, positive-obligation formalizer, Gate Chair precondition review, obstruction freeze, or current-state stop. Do not adopt a coupling law.
```

**Recommended role:** `theoretical-continuation-selector@0.1.0`

**Prerequisite:** PLAN-P3-T2 completion exists or current state has an equivalent stress result.

**Allowed next routes:**

- `candidate_constructor_repair`
- `ontology_formalizer_positive_success_criteria`
- `source_extension_gate_chair_precondition_review`
- `refuter_scoped_no_go`
- `route_frozen`
- `human_gated_authority_required`

**Selector must not choose:**

- direct coupling-law adoption;
- matter-coupling derivation;
- Einstein-equation derivation;
- benchmark promotion;
- generic pause if a bounded mathematical route exists.

**Acceptance criteria:**

- one next route selected;
- selector explains why other routes are deferred;
- no Distance-to-GR promotion unless the stress result and gate authority require it.

---

# Phase P4: Positive Emergence Obligations

## Phase Goal

Balance the project's strong anti-smuggling discipline with a positive map of what must actually emerge from source-side structure before GR recovery can be claimed.

## Phase Claim Boundary

Allowed:

- create draft/control obligation maps;
- define missing positive theorem obligations;
- add registry or ledger surfaces for obligation tracking;
- require future completions to reference positive obligations.

Forbidden:

- claiming obligations are discharged merely because they are listed;
- treating scoped source-extension objects as physical structures;
- promoting `g_eff`, matter coupling, stress-energy, Einstein equations, or benchmark status.

---

## PLAN-P4-T1: Positive Emergence Obligation Map Specification

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P4-T1 as one bounded Ontology Formalizer or Theoretical Continuation Selector task. Create a draft/control positive emergence obligation map specifying what source-side structures must positively produce before any GR-derivation claim. Do not claim any obligation is discharged.
```

**Recommended role:** `ontology-formalizer@0.2.0` or `theoretical-continuation-selector@0.1.0`

**Target derivation milestone:** `benchmark_promotion` or the active upstream milestone selected by Director.

**Candidate output path:**

- `research_control/design/positive_emergence_obligation_map.md`

**Required table columns:**

| Field | Meaning |
|---|---|
| `obligation_id` | Stable ID, e.g. `PEO-LORENTZIAN-SIGNATURE-001` |
| `target_physical_structure` | Physical/GR-side structure that must emerge |
| `source_side_candidate` | Current source-side object or missing placeholder |
| `current_status` | `missing`, `draft/control`, `scoped_source_extension`, `accepted_scoped`, `blocked`, `obstruction`, etc. |
| `positive_success_criterion` | What must be proven constructively |
| `forbidden_shortcut` | What cannot be imported |
| `minimum_finite_test` | Finite or local test that would give evidence |
| `blocking_burden` | Current blocker |
| `last_evidence_path` | Canonical path or empty |
| `downstream_claims_blocked` | List of claims still blocked |

**Minimum obligations to include:**

- `PEO-SOURCE-ONTOLOGY-PRIMITIVES`
- `PEO-EQSRC-EQUIVALENCE`
- `PEO-RETAINH`
- `PEO-GENH`
- `PEO-OBSERVER-LOCALIZATION`
- `PEO-RESPONSE-LOCALIZATION`
- `PEO-SOURCE-MANIFOLD`
- `PEO-METRICDATA`
- `PEO-EFFECTIVE-METRIC-FORM`
- `PEO-LORENTZIAN-SIGNATURE`
- `PEO-CAUSAL-CONES`
- `PEO-CLOCK-PROPER-TIME`
- `PEO-MATTER-TOKEN-SEMANTICS`
- `PEO-UNIVERSAL-COUPLING`
- `PEO-STRESS-ENERGY-EMERGENCE`
- `PEO-VARIATIONAL-DYNAMICS`
- `PEO-EINSTEIN-EQUATIONS`
- `PEO-EXACT-GR-BENCHMARK`

**Acceptance criteria:**

- every obligation has a positive success criterion and forbidden shortcut;
- map explicitly says it is not a proof;
- map is linked to existing Distance-to-GR burdens without replacing the ledger.

---

## PLAN-P4-T2: Positive Emergence Obligation Registry

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P4-T2 as one bounded project-control task. Add a positive-emergence obligation registry only if PLAN-P4-T1 shows a durable registry is needed. Do not change physics statuses.
```

**Recommended role:** `project-control-maintainer@active`

**Candidate path:**

- `registries/POSITIVE_EMERGENCE_OBLIGATION_REGISTRY.csv`

**Candidate columns:**

```csv
obligation_id,target_physical_structure,source_side_candidate,current_status,positive_success_criterion,forbidden_shortcut,minimum_finite_test,blocking_burden,last_evidence_path,updated_at,notes
```

**Acceptance criteria:**

- registry is clearly draft/control or planning authority only;
- no row uses `accepted` unless supported by an existing Gate Chair or canonical evidence path;
- `MetricData(E)`, stress-energy, matter coupling, Einstein equations, and benchmark rows remain blocked unless local state has changed lawfully.

---

## PLAN-P4-T3: Future Completion Obligation Reference Rule

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P4-T3 as one bounded control-contract task. Add a future-completion rule requiring relevant physics completions to state which positive emergence obligations they affect. Do not enforce as hard failure until a separate validator rollout task.
```

**Recommended role:** `project-control-maintainer@active`

**Required completion field:**

```yaml
positive_emergence_obligations:
  - obligation_id: "PEO-UNIVERSAL-COUPLING-001"
    effect: "unchanged | sharpened | candidate_constructed | audited | stressed | obstructed | discharged_scoped | discharged_full"
    evidence_path: "..."
    forbidden_shortcuts_preserved:
      - "stress-energy import"
      - "target metric import"
```

**Acceptance criteria:**

- rule is prospective;
- historical tasks are not invalidated;
- hard-fail enforcement deferred to a separate validator task.

---

# Phase P5: Finite Toy Model v2

## Phase Goal

Rebuild the finite toy model route after the earlier explicit-tag route froze negative. The new toy model must use intrinsic source-side invariants rather than tags that encode the desired response.

## Phase Claim Boundary

Allowed:

- define a finite source set;
- construct source-local readout syntax;
- propose intrinsic orientation/normalization/token candidates;
- define an induced response relation;
- construct a toy metric or distance-form analogue;
- run invariance, relabeling, and finite-variation checks;
- record countermodels or obstructions.

Forbidden:

- claiming full `g_eff` from a toy model;
- claiming physical proper time, stress-energy, or matter coupling;
- promoting benchmark status;
- treating a finite toy success as GR derivation.

---

## PLAN-P5-T1: Selector for Finite Toy Model v2 Route

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P5-T1 as one bounded Theoretical Continuation Selector task. Decide whether a finite toy model v2 route is lawful under current state, especially after any completed coupling-law Refuter stress. Do not construct the toy model in this task.
```

**Recommended role:** `theoretical-continuation-selector@0.1.0`

**Selector inputs:**

- old finite toy frozen negative route;
- current `Resp_lc`, `M_src`, scoped `g_eff`, and matter-coupling state;
- positive emergence obligation map if Phase P4 exists;
- latest coupling-law stress result if P3 completed.

**Allowed decisions:**

- `finite_toy_v2_candidate_constructor`
- `finite_toy_v2_not_lawful_yet`
- `finite_toy_v2_human_gate_required`
- `finite_toy_v2_rejected_due_to_current_obstruction`

**Acceptance criteria:**

- one route selected;
- selector states why old frozen route is not being reopened without distinction;
- no toy-model construction occurs in selector output.

---

## PLAN-P5-T2: Formalize Finite Toy Model v2 Requirements

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P5-T2 as one bounded Ontology Formalizer task. Formalize finite toy model v2 requirements with intrinsic source invariants and anti-tag constraints. Do not construct a candidate model yet.
```

**Recommended role:** `ontology-formalizer@0.2.0`

**Required artifact:**

- `research_control/tasks/<task>/artifacts/<N>_FINITE_TOY_MODEL_V2_REQUIREMENTS.tex`

**Definitions required:**

- finite source package `S_fin`;
- source-local readout syntax `R_src`;
- admissible intrinsic invariants `I_src`;
- forbidden explicit-target tags;
- candidate response relation `Rel_resp`;
- toy distance-form or metric analogue `d_toy` or `q_toy`;
- relabeling group/action;
- finite variation family;
- bottom/fail-closed cases;
- success/failure criteria.

**Acceptance criteria:**

- no target metric, Lorentzian signature, proper time, stress-energy, detector semantics, or benchmark success imported;
- requirements are strong enough that a Candidate Constructor can either build a model or return a precise obstruction.

---

## PLAN-P5-T3: Construct Finite Toy Model v2 Candidate or Obstruction

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P5-T3 as one bounded Candidate Constructor task. Construct one finite toy model v2 candidate satisfying the formal requirements from PLAN-P5-T2, or return one precise obstruction. Do not claim physical metric, matter coupling, or GR recovery.
```

**Recommended role:** `candidate-constructor@0.2.0`

**Required result types:**

```yaml
candidate_constructor_result.result_type: "constructed_candidate | minimal_countermodel | precise_obstruction | invalid_under_claim_boundary"
```

**If constructed, artifact must specify:**

- finite source set;
- readout syntax;
- intrinsic invariants;
- response relation;
- toy metric/distance-form analogue;
- relabeling checks;
- finite-variation checks;
- bottom cases;
- nontriviality witness;
- explicit limitations.

**If obstruction, artifact must specify:**

- obstruction ID;
- smallest failed component;
- minimal counterexample if available;
- why failure does not imply global theory rejection;
- next lawful route.

**Acceptance criteria:**

- no-fog Candidate Constructor result;
- source path named;
- next required role is Smuggling Auditor if candidate exists, Refuter or Selector if obstruction exists.

---

## PLAN-P5-T4: Smuggling Audit of Finite Toy Model v2

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P5-T4 as one bounded Smuggling Auditor task. Audit the finite toy model v2 candidate for hidden target imports, explicit tag encoding, detector semantics, metric import, benchmark import, and process-authority laundering. Do not stress the model yet.
```

**Recommended role:** `smuggling-auditor@0.2.0`

**Audit dimensions:**

- explicit answer-tag encoding;
- target topology/atlas/metric import;
- Lorentzian signature import;
- proper-time semantics;
- detector semantics;
- stress-energy or matter-action import;
- benchmark fit import;
- validator/registry/process authority;
- nontriviality preservation.

**Acceptance criteria:**

- audit pass only authorizes Refuter stress;
- audit failure gives exact failure and repair/freeze consequence.

---

## PLAN-P5-T5: Refuter Stress of Finite Toy Model v2

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P5-T5 as one bounded Refuter task. Stress the audited finite toy model v2 candidate under relabeling, finite variation, tag erasure, quotienting, nonuniqueness, and bottom behavior. Do not promote full GR claims.
```

**Recommended role:** `refuter@0.2.0`

**Stress dimensions:**

- tag erasure;
- relabeling invariance;
- finite variation stability;
- quotient collapse;
- nonunique response relation;
- degenerate metric/distance-form;
- bottom completeness;
- robustness under minimal perturbations;
- whether toy analogue is nontrivial without target imports.

**Acceptance criteria:**

- decisive scoped result;
- freeze criteria evaluated if repeated failure resembles old toy route;
- no full `g_eff` or matter-coupling claim.

---

## PLAN-P5-T6: Toy Model v2 Post-Stress Selector

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P5-T6 as one bounded Theoretical Continuation Selector task. Classify the post-stress finite toy model v2 route and choose one next lawful task. Do not promote the toy result.
```

**Allowed next routes:**

- `finite_toy_v2_gate_precondition_review`
- `finite_toy_v2_repair_constructor`
- `finite_toy_v2_obstruction_record`
- `positive_obligation_update`
- `route_frozen`
- `human_gate_required`

**Acceptance criteria:**

- downstream route tied to explicit stress result;
- no generic continuation fog.

---

# Phase P6: Scoped Metric Nomenclature and Overread Prevention

## Phase Goal

Prevent readers and agents from confusing accepted scoped source-extension `g_eff` with a derived physical effective metric or adopted `MetricData(E)`.

## Phase Claim Boundary

Allowed:

- add nomenclature policy;
- update explanatory text and generated summaries;
- add phrase scans or validators;
- clarify ledger notes.

Forbidden:

- changing the actual Gate Chair verdict;
- expanding scoped `g_eff`;
- adopting `MetricData(E)`;
- claiming a physical metric was derived.

---

## PLAN-P6-T1: Scoped Metric Nomenclature Policy

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P6-T1 as one bounded documentation/control task. Create a scoped metric nomenclature policy distinguishing scoped source-extension g_eff from physical metric or MetricData(E). Do not change physics status.
```

**Recommended role:** `documentation-curator@active` or `project-control-maintainer@active`

**Candidate output:**

- `research_control/design/scoped_metric_nomenclature_policy.md`

**Required distinctions:**

| Label | Meaning | Status |
|---|---|---|
| `g_eff^{GSC-cand}` | scoped source-extension candidate/object under declared source-side scope | accepted only if supported by Gate Chair status |
| `MetricData(E)` | stronger metric-data object requiring separate adoption | not adopted unless current state says otherwise |
| `g_phys` or `physical metric` | target/observable physical metric | not derived by scoped source-extension status |
| exact-GR metric | benchmark structure | not promoted |

**Acceptance criteria:**

- policy includes forbidden phrasing examples;
- policy includes allowed phrasing examples;
- no scientific status changes.

---

## PLAN-P6-T2: Update Human-Facing Summaries for Scoped Metric Language

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P6-T2 as one bounded documentation task. Update non-authoritative summaries so scoped g_eff cannot be read as physical metric derivation. Do not edit canonical physics artifacts except through authorized documentation paths.
```

**Recommended role:** `documentation-curator@active`

**Candidate paths:**

- `README.md`
- `research_control/current_frontier.md`
- relevant `markdown/` or publication-brief surfaces if authorized

**Required wording guard:**

Use:

```text
scoped source-extension g_eff object
```

Avoid unqualified:

```text
g_eff accepted
metric derived
effective metric constructed
```

unless immediately bounded by source-extension scope and forbidden downstream claims.

**Acceptance criteria:**

- no unqualified `accepted g_eff` in public summaries;
- docs say `MetricData(E)` and physical metric remain unadopted/underived unless current state changed.

---

## PLAN-P6-T3: Add Scoped Metric Phrase Scan

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P6-T3 as one bounded validator-engineering task. Add a phrase scan that warns or fails on unqualified scoped g_eff promotion language in noncanonical summaries. Do not scan mathematical formulas as false positives if avoidable.
```

**Recommended role:** `validator-engineer@active`

**Candidate checks:**

- flag `g_eff accepted` unless same paragraph contains `scoped source-extension`;
- flag `effective metric derived` unless same paragraph contains `not derived` or source-extension boundary;
- flag `MetricData(E) adopted` unless supported by an authorized evidence path;
- ignore registered TeX artifacts where exact claim boundary is local and citation is present, unless the artifact is explanatory.

**Acceptance criteria:**

- scan has tests for allowed and forbidden language;
- scan does not block legitimate mathematical notation;
- failure messages explain repair.

---

# Phase P7: Matter-Coupling Positive Success Criteria

## Phase Goal

Define what would count as positive progress toward universal matter coupling, rather than merely showing that a coupling-law candidate avoids forbidden imports.

## Phase Claim Boundary

Allowed:

- define positive success criteria;
- define proof obligations for source-side matter coupling;
- sharpen coupling-law candidate requirements;
- construct repair candidates after stress results.

Forbidden:

- adopting a coupling law;
- deriving matter coupling;
- importing stress-energy or matter action;
- claiming Einstein equations or benchmark recovery.

---

## PLAN-P7-T1: Formalize Matter-Coupling Positive Success Criteria

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P7-T1 as one bounded Ontology Formalizer task. Formalize positive success criteria for source-side matter coupling. This task defines obligations only and does not adopt a coupling law or derive matter coupling.
```

**Recommended role:** `ontology-formalizer@0.2.0`

**Required artifact:**

- `research_control/tasks/<task>/artifacts/<N>_MATTER_COUPLING_POSITIVE_SUCCESS_CRITERIA.tex`

**Minimum criteria to define:**

1. **Source-intrinsic token semantics**  
   Coupling tokens must have source-defined interpretation stronger than bare labels but weaker than imported stress-energy.

2. **Nontrivial admissibility**  
   `A_E` must admit and reject updates for source-intrinsic reasons.

3. **Transition coherence**  
   Coupling-token updates must commute with source transitions or fail closed.

4. **Universality analogue**  
   The same source-side coupling rule must apply across admissible matter-like source response sectors, not be hand-tailored per case.

5. **Metric compatibility boundary**  
   Compatibility with scoped `g_eff` must not import target metric semantics or expand `g_eff` scope.

6. **Conservation-like source obligation**  
   If conservation is needed, define a source-side conservation analogue without stress-energy tensors or Bianchi identities.

7. **Empirical-semantics separation**  
   Detector or matter-sector semantics must remain absent until separately derived or explicitly gated.

8. **Bottom and obstruction completeness**  
   Ambiguous, degenerate, target-repaired, detector-repaired, and benchmark-repaired cases fail closed.

**Acceptance criteria:**

- criteria are formal enough for Candidate Constructor or Refuter follow-up;
- artifact distinguishes `necessary`, `candidate sufficient`, and `future physical bridge` obligations;
- no adoption or derivation claim.

---

## PLAN-P7-T2: Coupling-Law Candidate Repair or Strengthening Packet

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P7-T2 as one bounded Candidate Constructor task only after PLAN-P3-T2 and PLAN-P7-T1 or equivalent current-state artifacts exist. Strengthen or repair the coupling-law candidate against positive success criteria, or return one precise obstruction. Do not adopt the repaired candidate.
```

**Recommended role:** `candidate-constructor@0.2.0`

**Prerequisites:**

- coupling-law Refuter stress result;
- positive success criteria artifact.

**Allowed result types:**

- `constructed_candidate`
- `precise_obstruction`
- `minimal_countermodel`
- `invalid_under_claim_boundary`

**Acceptance criteria:**

- repaired candidate states exactly which positive criteria it addresses;
- proof obligations listed;
- next role is Smuggling Auditor if a candidate exists.

---

## PLAN-P7-T3: Audit and Stress Strengthened Coupling Candidate

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P7-T3 as one bounded follow-up audit or stress task selected by the Director for the strengthened coupling candidate. Execute only the selected role: Smuggling Auditor or Refuter, not both.
```

**Recommended role:** Director chooses `smuggling-auditor@0.2.0` or `refuter@0.2.0` depending on current state.

**Acceptance criteria:**

- if candidate is new or materially changed, audit precedes stress;
- if only proof obligations are clarified and audit remains valid, Refuter may be selected if Director justifies it;
- all downstream claims remain blocked.

---

# Phase P8: Formal Finite Checker and Proof-Kernel Support

## Phase Goal

Add support-only executable checks for finite source structures, transition coherence, quotient invariance, bottom completeness, and counterexample generation. These tools support research artifacts but do not become proof authority unless separately and explicitly gated.

## Phase Claim Boundary

Allowed:

- add Python support checkers;
- add fixtures and tests;
- integrate support checks into task artifacts;
- document support-only status.

Forbidden:

- treating checker pass as theorem proof;
- giving generated reports proof authority;
- replacing TeX proof obligations with code output;
- adopting physics claims from executable checks alone.

---

## PLAN-P8-T1: Formal Checker Scope Specification

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P8-T1 as one bounded validator-engineering or candidate-constructor specification task. Specify support-only finite checker scope for source packages, transitions, quotient invariance, bottom completeness, and counterexamples. Do not implement the checker yet unless the Director explicitly selects implementation.
```

**Recommended role:** `validator-engineer@active` for tooling spec, `candidate-constructor@0.2.0` for mathematical finite-object spec.

**Required scope:**

- graph/source package data model;
- source transition data model;
- relation well-definedness check;
- cocycle check;
- inverse/partial inverse check;
- quotient invariance check;
- bottom completeness check;
- nontriviality check;
- counterexample search limits;
- report format;
- support-only authority banner.

**Acceptance criteria:**

- spec is implementable;
- no checker proof authority implied.

---

## PLAN-P8-T2: Implement Finite Checker Core

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P8-T2 as one bounded tooling task. Implement the support-only finite checker core according to PLAN-P8-T1. Do not wire checker PASS into physics promotion or Gate Chair authority.
```

**Recommended role:** `validator-engineer@active`

**Candidate paths:**

- `scripts/research_control/finite_source_checks.py`
- `tests/research_control/test_finite_source_checks.py`
- `research_control/design/finite_checker_support_only_policy.md`

**Required functions:**

```python
check_relation_well_defined(...)
check_transition_cocycle(...)
check_partial_inverse(...)
check_quotient_invariance(...)
check_bottom_completeness(...)
check_nontriviality(...)
search_minimal_counterexample(...)
```

**Acceptance criteria:**

- deterministic tests pass;
- checker reports include `support_only: true`;
- validators pass;
- no physics ledger status changes.

---

## PLAN-P8-T3: Integrate Checker Reports into Future Candidate Tasks

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P8-T3 as one bounded control-contract task. Add optional support-checker report fields to future finite Candidate Constructor and Refuter completions. Do not require reports for historical tasks.
```

**Recommended role:** `project-control-maintainer@active`

**Completion field:**

```yaml
support_checker_reports:
  - checker_name: "finite_source_checks"
    command: ".venv/bin/python scripts/research_control/finite_source_checks.py ..."
    report_path: "research_control/tasks/<task>/artifacts/support_checker_report.json"
    support_only: true
    proof_authority: false
```

**Acceptance criteria:**

- support reports are optional unless AgentJob requires them;
- all docs state checker output is scaffolding, not proof authority.

---

## PLAN-P8-T4: Long-Term Proof Assistant Feasibility Note

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P8-T4 as one bounded methodology task. Produce a feasibility note for migrating finite source definitions into Lean, Coq, Isabelle, or another proof assistant. Do not introduce a proof-assistant dependency yet.
```

**Recommended role:** `project-system-director@active` or `validator-engineer@active`

**Required analysis:**

- candidate proof assistant options;
- minimal formalization targets;
- dependency impact;
- local agent workflow impact;
- validation impact;
- reasons not to migrate yet;
- first proof-kernel milestone if migration is later approved.

**Acceptance criteria:**

- no new dependency added;
- note separates methodology from physics proof.

---

# Phase P9: Gate Authorization Semantics

## Phase Goal

Clarify the distinction between tasks that require a new human gate and tasks that consume a previously granted human authorization.

## Phase Claim Boundary

Allowed:

- add metadata fields;
- backfill metadata-only overlays if authorized;
- update validators and docs;
- improve Gate Chair task clarity.

Forbidden:

- changing Gate Chair verdicts;
- adding retroactive human authorization;
- promoting claims merely because metadata is clarified.

---

## PLAN-P9-T1: Gate Authorization Schema Specification

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P9-T1 as one bounded project-control specification task. Specify fields that distinguish new human-gate requirement from consumed prior authorization. Do not edit historical tasks yet.
```

**Recommended role:** `project-control-maintainer@active`

**Proposed fields:**

```yaml
human_gate_semantics:
  requires_new_human_gate: false
  consumes_prior_human_authorization: true
  human_authorization_id: "approval-YYYYMMDD-NNN"
  authorization_source_path: "research_control/approvals/..."
  authorized_scope: "..."
  gate_role: "gate-chair@0.1.0"
  protected_claims_authorized:
    - "scoped source-extension evidence-status review only"
  protected_claims_not_authorized:
    - "benchmark promotion"
    - "completed derivation"
```

**Acceptance criteria:**

- schema distinguishes current execution need from historical approval consumption;
- no claim status changes.

---

## PLAN-P9-T2: Implement Gate Authorization Validator Support

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P9-T2 as one bounded validator-engineering task. Add validator support for the gate authorization semantics specified in PLAN-P9-T1. Do not require fields for historical tasks until a backfill task authorizes it.
```

**Recommended role:** `validator-engineer@active`

**Validation rules:**

- if `consumes_prior_human_authorization: true`, `human_authorization_id` and `authorization_source_path` must be nonempty;
- if `requires_new_human_gate: true`, task must not execute protected role output until gate exists;
- Gate Chair role tasks must state authorized scope and blocked claims;
- `requires_human_gate: false` is allowed when prior authorization is consumed, but must be disambiguated.

**Acceptance criteria:**

- tests cover new gate, prior authorization, missing authorization, and non-gate tasks;
- no historical failures unless explicitly opted in.

---

## PLAN-P9-T3: Metadata-Only Backfill for Recent Gate Tasks

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P9-T3 as one bounded metadata-only backfill task for recent Gate Chair tasks. Add gate-authorization semantics without rewriting scientific artifacts or changing claim status.
```

**Recommended role:** `project-control-maintainer@active`

**Candidate task range:**

- recent Gate Chair tasks around scoped `g_eff` and matter-coupling precondition evidence, e.g. `RT-20260614-220`, `RT-20260614-222`, `RT-20260614-228`, if local state confirms them.

**Acceptance criteria:**

- metadata-only changes;
- no TeX scientific artifact rewritten unless explicit metadata sidecar is used;
- validators pass;
- completion states no physics claim status changed.

---

# Phase P10: Graph-Continuity Validation

## Phase Goal

Strengthen the research-control spine by validating links among tasks, jobs, completions, handoffs, ledger evidence paths, claim boundaries, and approvals.

## Phase Claim Boundary

Allowed:

- add deterministic validators;
- add tests and fixtures;
- report broken links;
- update metadata if uniquely determined and task authorizes repair.

Forbidden:

- inferring physics claims from graph continuity;
- treating linked evidence as proof unless the source and gate sequence support it;
- repairing ambiguous history without Process Integrity or human gate.

---

## PLAN-P10-T1: Graph-Continuity Validator Specification

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P10-T1 as one bounded validator specification task. Specify graph-continuity checks across tasks, jobs, completions, handoffs, ledger rows, claim boundaries, and approvals. Do not implement yet unless selected by Director.
```

**Recommended role:** `validator-engineer@active`

**Required checks:**

1. Every `parent_task_id` exists unless root or explicitly external.
2. Every `current_job_id` exists in job registry.
3. Every job `completion_path` exists if status is completed.
4. Every completion output path exists unless explicitly generated or external.
5. Every `program_state.latest_handoff_id` exists as YAML and Markdown pair.
6. Latest handoff points to existing task, job, and completion.
7. Every ledger `last_evidence_path` exists or is explicitly historical/external.
8. Every active claim boundary applies to an existing path.
9. Every Gate Chair task consuming approval links to an approval record.
10. Every registry row path is repo-relative and normalized.

**Acceptance criteria:**

- spec defines warning vs hard failure;
- spec identifies repair ownership.

---

## PLAN-P10-T2: Implement Graph-Continuity Validator

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P10-T2 as one bounded validator-engineering task. Implement graph-continuity checks from PLAN-P10-T1 and wire them into validate_research_control.py if appropriate.
```

**Recommended role:** `validator-engineer@active`

**Candidate implementation:**

- add helper module `scripts/research_control/validate_control_graph.py`;
- call helper from `validate_research_control.py`;
- add tests under `tests/research_control/` if a test harness exists.

**Acceptance criteria:**

- broken links are reported with exact field and path;
- valid current repo passes or known historical exceptions are explicitly grandfathered;
- no physics status changed.

---

## PLAN-P10-T3: Repair Any Detected Graph-Continuity Failures

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P10-T3 as one bounded Process Integrity repair task if graph-continuity validation reports failures. Repair only uniquely evidenced metadata. Stop for human gate or ambiguity.
```

**Recommended role:** `process-integrity-auditor@active`

**Allowed repairs:**

- typo in registry path when target file uniquely exists;
- missing registry row when task-local canonical file and all IDs are unique;
- missing handoff Markdown generated from matching YAML only if local convention supports it;
- stale metadata field where authoritative source is unambiguous.

**Forbidden repairs:**

- changing scientific artifact claims;
- inventing missing approvals;
- reparenting task history ambiguously;
- changing ledger physics status.

**Acceptance criteria:**

- every repair cites unique evidence;
- validators pass;
- unresolved failures are reported, not papered over.

---

# Phase P11: Validation PASS vs Physics PASS Separation

## Phase Goal

Make it impossible for readers, agents, or generated reports to confuse control-valid completion with scientific proof or physics promotion.

## Phase Claim Boundary

Allowed:

- add naming conventions, display changes, completion fields, and reporting changes;
- update docs and validators;
- clarify metrics.

Forbidden:

- changing actual physics statuses;
- demoting or promoting tasks based on wording alone;
- treating control validity as evidence of a theorem.

---

## PLAN-P11-T1: Control Validity vs Scientific Truth Field Specification

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P11-T1 as one bounded project-control specification task. Specify fields and display labels that separate validation PASS from physics progress or truth status. Do not implement code yet unless Director selects implementation.
```

**Recommended role:** `project-control-maintainer@active`

**Proposed fields:**

```yaml
control_validity_status: "PASS | FAIL | NOT_RUN"
physics_truth_status:
  claim_authority: "none | draft/control | scoped_source_extension | accepted_scoped | adopted | rejected | obstruction | frozen_negative"
  theorem_established: false
  source_law_adopted: false
  downstream_gr_promoted: false
  summary: "..."
```

**Required display vocabulary:**

Use:

- `control-valid`
- `validator-pass`
- `science-draft`
- `scoped evidence`
- `adopted only under declared scope`

Avoid:

- `proved` unless theorem and authority support it;
- `derived` unless derivation theorem and gate support it;
- `accepted` without scope.

**Acceptance criteria:**

- spec states prospective rollout;
- historical tasks remain valid.

---

## PLAN-P11-T2: Update Metrics Report Terminology

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P11-T2 as one bounded validator/reporting task. Update physics progress metrics terminology so validation PASS cannot be confused with physics proof. Preserve metric separation guard.
```

**Recommended role:** `validator-engineer@active`

**Candidate file:**

- `scripts/research_control/report_physics_progress_metrics.py`

**Changes:**

- rename or supplement `completion_validation_status_counts` with `control_validation_status_counts`;
- keep scientific metrics separate;
- add explanatory `status_legend` block;
- ensure no operational metric key enters `scientific_progress_metrics`.

**Acceptance criteria:**

- existing report still runs;
- metric separation guard passes;
- tests or snapshot checks updated if present.

---

## PLAN-P11-T3: Add Forbidden Summary Header to Generated Reports

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P11-T3 as one bounded documentation/reporting task. Add a visible nonclaim header to generated or human-facing reports that might otherwise overread validator success. Do not change scientific artifacts.
```

**Recommended role:** `documentation-curator@active` or `validator-engineer@active`

**Header template:**

```text
Control-validity notice: validator PASS means the transaction followed project-control rules. It does not prove a theorem, adopt a source law, derive g_eff, derive matter coupling, derive Einstein equations, promote benchmark status, or complete the derivation.
```

**Acceptance criteria:**

- visible in relevant generated summaries;
- does not pollute canonical TeX proof statements;
- validators pass.

---

# Phase P12: External Review Packet

## Phase Goal

Prepare a source-backed packet readable by skeptical external reviewers. The packet should state what is claimed, what is not claimed, what objects currently exist, what is blocked, and what the next decisive tests are.

## Phase Claim Boundary

Allowed:

- produce explanatory Markdown or PDF source packet;
- cite canonical repo artifacts;
- summarize current state;
- list open proof obligations and obstructions.

Forbidden:

- changing physics status;
- claiming external validation;
- representing internal scoped objects as accepted physical structures;
- publishing without local publication-process requirements if applicable.

---

## PLAN-P12-T1: External Review Packet Specification

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P12-T1 as one bounded documentation/specification task. Specify an external review packet for skeptical relativists, mathematicians, philosophers of physics, and AI-systems reviewers. Do not write the full packet yet unless Director selects that scope.
```

**Recommended role:** `documentation-curator@active` with possible theoretical selector input if local routing supports it.

**Required sections:**

1. Executive nonclaim boundary.
2. Current Distance-to-GR table.
3. Accepted scoped source-extension objects.
4. Current matter-coupling frontier.
5. What is not derived.
6. Obstructions and frozen routes.
7. Positive emergence obligations.
8. Finite toy model status.
9. AI-agent methodology and control system.
10. How to audit the claim path in the repo.
11. Questions for external reviewers.

**Acceptance criteria:**

- spec identifies canonical source paths;
- publication authority is separated from science authority.

---

## PLAN-P12-T2: Draft External Review Packet

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P12-T2 as one bounded Documentation Curator task. Draft the external review packet from canonical sources and current control state. Preserve all nonclaim boundaries.
```

**Recommended role:** `documentation-curator@active`

**Candidate path:**

- `markdown/review-packets/aether-flow_external_review_packet_current.md`

or another repo-approved documentation path.

**Style requirements:**

- concise enough for external review;
- source-backed;
- no promotional phrasing;
- explicit distinction between physics and AI-methodology claims;
- exact filenames and task IDs for audit trails.

**Acceptance criteria:**

- packet includes current active state;
- packet says GR is not derived;
- packet lists missing Einstein-equation and benchmark burdens;
- validators pass.

---

## PLAN-P12-T3: Skeptical Review Simulation

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P12-T3 as one bounded review-discipline task. Run an internal skeptical review simulation of the external review packet from physicist, mathematician, philosopher, and AI-system perspectives. Do not alter physics claims.
```

**Recommended role:** Director selects appropriate documentation or process-integrity role. If treated as physics review, use parent-child synthesis and preserve claim boundaries.

**Required review lenses:**

- relativist: target metric, matter coupling, Einstein equations, empirical semantics;
- mathematician: definitions, theorem statements, proof obligations, counterexamples;
- philosopher of physics: ontology/interpretation/empirical recovery boundaries;
- AI scientist/system engineer: workflow validity, agent authority, validation/science separation.

**Acceptance criteria:**

- review produces actionable edits or no-change verdict;
- packet claims are not expanded;
- unresolved concerns are preserved.

---

# Phase P13: Final Integration and Release Gate

## Phase Goal

Ensure all implemented recommendations remain coherent, validated, checkpointed, and non-promotional unless separately gated.

## Phase Claim Boundary

Allowed:

- run end-to-end validation;
- synchronize generated systems;
- update implementation index;
- create final handoff;
- prepare release notes.

Forbidden:

- using successful implementation as physics promotion;
- closing the GR derivation;
- promoting benchmark status.

---

## PLAN-P13-T1: End-to-End Plan Implementation Audit

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P13-T1 as one bounded Process Integrity audit. Audit all completed plan tasks for scope compliance, claim-boundary preservation, validator status, handoff continuity, and unresolved blockers. Do not repair issues unless the AgentJob explicitly authorizes unique-evidence metadata repair.
```

**Recommended role:** `process-integrity-auditor@active`

**Audit checklist:**

- each completed plan task has a completion receipt;
- each task used Continue Research;
- no task bundled multiple plan tasks;
- physics tasks include mathematical decisiveness fields;
- project-system tasks state no physics delta;
- handoffs exist;
- validators pass;
- `current_frontier.md` not stale or marked historical;
- scoped `g_eff` language guarded;
- coupling-law status not overread;
- external review packet nonclaims correct.

**Acceptance criteria:**

- audit produces pass, pass-with-limitations, or precise failure list;
- no claims promoted.

---

## PLAN-P13-T2: Final Generated-System Synchronization

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P13-T2 as one bounded generated-system synchronization task. Run memory/wiki/registry regeneration and validation for implemented plan changes. Do not create new science artifacts.
```

**Recommended role:** `memory-system-maintainer@active` or `project-control-maintainer@active`

**Required commands:**

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py
git diff --check
```

**Acceptance criteria:**

- generated surfaces synchronized;
- validation passes;
- generated derivatives remain non-authoritative.

---

## PLAN-P13-T3: Final Implementation Handoff

**Use Continue Research instruction:**

```text
Use /continue-research to implement exactly PLAN-P13-T3 as one bounded final handoff task. Create a final implementation handoff summarizing completed recommendations, blocked tasks, validators, and next research route. Do not claim physics completion.
```

**Recommended role:** `director-of-research@active` or `project-system-director@active`, depending on local state.

**Handoff must include:**

- completed plan tasks;
- incomplete or blocked plan tasks;
- current authoritative physics state;
- current Distance-to-GR statuses;
- next lawful Continue Research route;
- project-system sidecars if any;
- no-claim boundary.

**Acceptance criteria:**

- final handoff routes to exactly one next action;
- no downstream physics promotion.

---

# 3. Recommended Execution Order

The local agents should prefer this order unless current tracked state forces a different lawful route:

1. `PLAN-P0-T1` ingest plan.
2. `PLAN-P0-T3` boundary audit.
3. `PLAN-P3-T1` and `PLAN-P3-T2` immediate coupling-law Refuter stress if current state still requires it.
4. `PLAN-P3-T3` post-stress selector.
5. `PLAN-P1-T1` through `PLAN-P1-T4` frontier synchronization.
6. `PLAN-P6-T1` through `PLAN-P6-T3` scoped metric nomenclature guard.
7. `PLAN-P4-T1` through `PLAN-P4-T3` positive emergence obligations.
8. `PLAN-P7-T1` through `PLAN-P7-T3` matter-coupling positive criteria and candidate repair if justified.
9. `PLAN-P5-T1` through `PLAN-P5-T6` finite toy model v2 route if selected.
10. `PLAN-P8-T1` through `PLAN-P8-T4` support-only finite checker path.
11. `PLAN-P9-T1` through `PLAN-P9-T3` gate authorization semantics.
12. `PLAN-P10-T1` through `PLAN-P10-T3` graph-continuity validation.
13. `PLAN-P11-T1` through `PLAN-P11-T3` validation/science separation upgrades.
14. `PLAN-P12-T1` through `PLAN-P12-T3` external review packet.
15. `PLAN-P13-T1` through `PLAN-P13-T3` final integration audit and handoff.

Exception: If `program_state.yaml` still requires the immediate coupling-law Refuter stress, the Director may prioritize P3 before project-system cleanup because it is the active research frontier. If local validation or stale-state drift blocks safe continuation, run P1/P10 repair tasks first.

---

# 4. Global Stop Conditions

Stop the current task and record a lawful completion if any of the following occur:

- active tracked state supersedes the plan task;
- task would require protected authority not currently granted;
- human gate is required;
- validator fails and repair is outside the AgentJob boundary;
- source paths are missing or contradictory;
- role fit is absent;
- implementing the task would bundle multiple plan tasks;
- implementation would change physics claim status without a proper source, stress, gate, and registry sequence;
- implementation would require external literature or experiments not authorized by the AgentJob.

A stop is not a failure if it is precise, recorded, and routed.

---

# 5. Global Forbidden Conclusions

No task in this plan authorizes any of the following by itself:

- canonical ontology edit;
- source-law adoption;
- `MetricData(E)` adoption;
- `g_eff` scope expansion;
- physical effective metric derivation;
- coupling-law adoption;
- matter-coupling derivation;
- matter-coupling adoption;
- stress-energy semantics;
- matter action;
- empirical detector semantics;
- Einstein equations;
- exact-GR benchmark promotion;
- benchmark Gate Chair closure;
- completed derivation;
- future source-extension impossibility;
- global theory rejection.

If any local task appears to imply one of these conclusions, the correct action is to stop, record a boundary failure or human-gate requirement, and route through the appropriate Gate Chair or Process Integrity path.

---

# 6. Success Definition for This Implementation Plan

This plan is successfully implemented when:

1. Each completed plan task was executed through Continue Research as one bounded AgentJob.
2. The active physics frontier was not overclaimed.
3. The coupling-law Refuter stress either completed or was superseded by newer current state.
4. Stale frontier drift is detected or eliminated.
5. Scoped `g_eff` language is guarded.
6. Positive emergence obligations exist and are referenced by future physics tasks.
7. Matter-coupling success criteria are stated positively.
8. Finite toy model v2 has a lawful route, candidate, obstruction, or freeze decision.
9. Support-only checker tooling, if implemented, is clearly non-authoritative.
10. Gate authorization semantics distinguish new gate requirements from consumed prior approvals.
11. Graph-continuity validation exists or has a precise blocker.
12. Validator PASS and physics progress/truth are visibly separated.
13. External review packet exists or has a precise blocker.
14. Final implementation audit and handoff exist.
15. Validators pass or failures are precisely recorded with next repair route.

The implementation plan fails only if it causes authority expansion, claim laundering, bundled task execution, untracked modifications, or physics promotion without the required scientific and human-gated support.

---

# 7. Final Agent Reminder

The work here is not to make the project sound more complete. The work is to make the project harder to fool.

A clean obstruction is progress. A scoped no-go is progress. A finite countermodel is progress. A validator that prevents a beautiful false sentence from entering the claim path is progress. A successful coupling-law stress test is progress only inside its exact boundary. The local agents should prefer precise, bounded, falsifiable, and auditable outputs over grand synthesis.

Use Continue Research. One bounded task. One receipt. One handoff. No smuggled crowns.
