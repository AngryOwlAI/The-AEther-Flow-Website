---
prd_id: "PRD-03"
title: "Research-Control and Agent Workflow"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Research-agent workflow, Director decisions, AgentJobs, execution roles, completions, handoffs, validators, and Distance-to-GR control flow"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
  - "PRD-09-current-research-frontier-for-website-use.md"
  - "PRD-10-website-positioning-guidance.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-03: Research-Control and Agent Workflow

## 1. Summary

This PRD defines how The AEther Flow Website should explain the governed AI
research-control workflow. It covers Director decisions, AgentJob contracts,
execution-role records, the one-job rule, memory preflight, parent-child
parallel synthesis, completion records, handoffs, validators, Distance-to-GR
status updates, and the boundary between operational validation and scientific
proof.

The central product rule is that the website may present the agent workflow as
auditable research infrastructure. It must not present agent execution,
validator PASS, generated artifacts, handoffs, roles, or commits as autonomous
scientific proof.

## 2. Product Purpose

The AEther Flow Project uses a controlled research-agent system because the
research program is speculative, mathematically delicate, and easy to overread.
The website should make that system understandable without exposing readers to
raw control files first.

Readers should understand:

- how a current frontier state becomes one bounded task;
- how the Director chooses or reuses one AgentJob;
- how role authority is bound to a task-local execution record;
- why memory and retrieval layers support navigation but do not create
  authority;
- how completions and handoffs preserve results, blockers, and next routes;
- how validators protect boundaries while remaining operational checks;
- how local failures, obstructions, and freezes become useful routing evidence
  rather than global theory rejection.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, routing, role, schema, or workflow
authority.

Source basis for implementation should include:

- `research_control/README.md`;
- `research_control/program_state.yaml`;
- `research_control/current_frontier.md`;
- `research_control/tasks/`;
- `research_control/handoffs/`;
- `research_control/templates/COMPLETION_TEMPLATE.yaml`;
- `research_control/design/gr_derivation_burden_map.md`;
- `research_control/design/mathematical_decisiveness_completion_contract.md`;
- `.codex/skills/continue-research/SKILL.md`;
- `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`;
- `.agents/schemas/AGENT_JOB_SCHEMA.md`;
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`;
- `registries/AGENT_JOB_REGISTRY.csv`;
- `registries/ROLE_EXECUTION_REGISTRY.csv`;
- `registries/DISTANCE_TO_GR_LEDGER.csv`;
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`.

Tracked research-control files are workflow authority. Website pages, PRDs,
generated summaries, wiki notes, local memory, semantic extracts, and `.local`
caches are explanatory or retrieval layers unless a higher-authority tracked
record says otherwise.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand that the AI system is governed and bounded rather than an autonomous proof machine. |
| Physicist or reviewer | Inspect how role outputs, obstructions, validations, and handoffs preserve claim boundaries. |
| AI researcher | Understand the architecture of Director decisions, AgentJobs, execution roles, validators, and memory preflight. |
| Contributor | Learn which workflow artifact to inspect before proposing or continuing research work. |
| Operator | Confirm the lifecycle and validation checkpoints needed before a transaction is checkpointed. |
| Site builder | Build workflow pages and diagrams that reflect the real control system without inventing authority. |

## 5. Scope

In scope:

- research-agent workflow page requirements;
- AgentJob lifecycle diagram requirements;
- Director Decision Record explainer requirements;
- AgentJob contract explainer requirements;
- execution-role record explainer requirements;
- memory-preflight and retrieval-boundary requirements;
- parent-child parallel synthesis explainer requirements;
- completion and handoff explainer requirements;
- Distance-to-GR workflow panel requirements;
- validator PASS limit explainer requirements;
- obstruction, freeze, and bounded theoretical continuation explanation
  requirements.

Out of scope:

- changing upstream research-control workflows;
- editing role contracts, schemas, registries, source files, tasks, handoffs, or
  validators;
- implementing public routes or diagrams in this packet;
- creating or executing research AgentJobs;
- changing current frontier state;
- promoting any scientific claim;
- pushing or deploying.

## 6. Non-Goals

This PRD must not:

- claim that AI agents independently prove physics results;
- describe language-model behavior as understanding;
- imply a role can exceed its registered contract or task-local execution-role
  record;
- treat validator PASS, registry entries, memory hits, generated derivatives,
  handoffs, approvals, or commits as scientific proof;
- present parent-child synthesis as multiple independent AgentJobs or expanded
  authority;
- present a local obstruction, failure, or freeze as global theory rejection;
- turn the website into a control console for mutating upstream research state.

## 7. Website Surfaces

Required surfaces:

- Research-agent workflow page;
- AgentJob lifecycle diagram;
- Director decision explainer;
- AgentJob contract explainer;
- Execution-role record explainer;
- Memory preflight and retrieval-boundary panel;
- Parent-child synthesis explainer;
- Completion and handoff explainer;
- Distance-to-GR workflow panel;
- Validator PASS limit explainer;
- Bounded theoretical continuation explainer.

Supporting surfaces:

- one-job rule card;
- source-authority and claim-boundary card;
- obstruction and local-freeze card;
- human-gated promotion card;
- project-improvement sidecar note;
- workflow glossary.

## 8. Functional Requirements

1. Explain the one-job rule: a continuation invocation may set up or execute at
   most one bounded AgentJob.
2. Explain Director Decision Records as auditable routing records with
   objective, authority surfaces read, role-fit matrix, selected role, claim
   boundary, and validation.
3. Explain AgentJob contracts as immutable executable YAML contracts for one
   bounded job.
4. Explain execution-role records as task-local authority contracts that bind an
   AgentJob to registered role, task overlay, or one-job provisional role
   semantics.
5. Explain memory preflight as navigation and source-inspection support, not as
   authority.
6. Explain parent-child parallel synthesis for physics jobs as internal
   perspective decomposition inside one outer AgentJob.
7. Explain completion records as receipts for outputs, validators, memory
   preflight, mathematical payloads, Distance-to-GR status, and forbidden
   conclusions.
8. Explain handoffs as durable state-transfer records that preserve result,
   next route, claim boundaries, and validation evidence.
9. Explain Distance-to-GR status matrix and delta as progress accounting for
   derivation burdens, not as proof or scalar percentage.
10. Explain that validator PASS means operational consistency, not scientific
    proof.
11. Explain local failures, obstructions, and freezes as preserved routing
    evidence, not global no-go claims.
12. Explain bounded theoretical continuation as the alternative to generic
    pause when a non-promotional theoretical route remains available.
13. Explain that protected promotion, benchmark closure, canonical ontology
    adoption, and Gate Chair authority require explicit tracked human gates.

## 9. Non-Functional Requirements

- Auditability: Every workflow explanation should map to a named control
  artifact or schema.
- Safety: Claim-boundary language must be adjacent to workflow power language.
- Maintainability: Pages should describe stable artifact classes rather than
  transient task IDs unless using PRD-09 snapshot rules.
- Comprehension: Diagrams should show lifecycle and authority flow before
  low-level schema detail.
- Security and integrity: Pages should avoid suggesting that users bypass
  validators, write allowlists, human gates, or checkpoint scripts.
- Reversibility: Future changes to roles or schemas should update workflow
  pages without changing the stable source-authority model.

## 10. Claim Boundary

This PRD may specify website content that explains:

- the research-control system as a governed, source-first, auditable workflow;
- Director decisions as routing decisions;
- AgentJobs as bounded executable contracts;
- execution roles as task-local authority bindings;
- memory preflight as retrieval support plus canonical source inspection;
- validation as operational receipt evidence;
- completions and handoffs as provenance and routing evidence;
- local obstructions and freezes as scoped results.

This PRD must not authorize website content claiming:

- AI agents, role outputs, or validators create scientific proof by themselves;
- parent-child synthesis expands authority beyond one outer AgentJob;
- operational validation proves theorem correctness, source-law adoption,
  `M_src`, `g_eff`, matter coupling, Einstein equations, benchmark promotion,
  or completed derivation;
- memory, wiki, semantic extracts, local caches, generated docs, registries,
  handoffs, approvals, commits, or role identities are proof surfaces;
- local failures or freezes are global theory rejection without tracked
  authority.

## 11. Content Requirements

The AgentJob lifecycle diagram must include at least:

```text
current tracked state
  -> memory preflight
  -> Director Decision Record
  -> execution-role record
  -> AgentJob contract
  -> one bounded execution
  -> completion record
  -> validation
  -> handoff
  -> program_state / current_frontier update
  -> local checkpoint
```

The workflow page must include a lifecycle table:

| Stage | Artifact | Reader explanation | Boundary |
| --- | --- | --- | --- |
| State pointer | `program_state.yaml` | Names active task, latest handoff, status, and next action. | Compact pointer, not a proof surface. |
| Frontier snapshot | `current_frontier.md` | Human-readable status summary. | Generated snapshot; tracked authority governs if drift occurs. |
| Director decision | DDR | Selects role and AgentJob using explicit authority surfaces. | Routing record, not scientific verdict. |
| Execution role | Role execution record | Binds the job to exact role semantics. | Task-local authority only. |
| AgentJob | YAML contract | Defines reads, writes, validators, outputs, and claim boundary. | One bounded job; immutable after creation. |
| Memory preflight | Receipt | Records memory status and canonical inspections. | Retrieval support only. |
| Parent-child synthesis | Internal artifacts | Adds two analytical perspectives plus parent fusion for physics jobs. | Still one outer job and one authority boundary. |
| Completion | YAML receipt | Records outputs, validator results, payloads, forbidden conclusions, and route consequence. | PASS is operational consistency. |
| Handoff | YAML and Markdown records | Transfers durable state and next route. | Routing authority below program state. |
| Checkpoint | Local commit | Seals allowed transaction paths. | Repository history, not proof. |

Required copy fragments:

- "One invocation, one bounded AgentJob."
- "The execution-role record is the task-local authority contract."
- "Memory preflight helps navigation; canonical sources remain authority."
- "Parent-child synthesis is internal analysis inside one outer AgentJob."
- "Validator PASS means operational consistency, not scientific proof."
- "A local obstruction sharpens routing; it is not global theory rejection."
- "Human-gated promotion requires explicit tracked authority."

The page should define these terms:

- Director of Research;
- Director Decision Record;
- AgentJob;
- execution-role record;
- registered role;
- task overlay;
- one-job provisional role;
- memory preflight;
- parent-child parallel synthesis;
- completion record;
- handoff;
- Distance-to-GR status matrix;
- Distance-to-GR delta;
- mathematical payload manifest;
- forbidden conclusion summary;
- obstruction record;
- freeze criteria status;
- route cycle control;
- theoretical continuation gate;
- ontology-law research packet;
- human-gated promotion.

## 12. UX and Navigation Requirements

Workflow navigation should:

- begin with a compact lifecycle diagram before schema detail;
- link current-state concepts to PRD-09 current frontier requirements;
- link role and schema details forward to PRD-04;
- link validator and tooling details forward to PRD-07;
- link memory, registry, and provenance concepts back to PRD-05;
- keep "not proof" language visible near validator and handoff explanations;
- expose "can do / cannot do / where to verify" for each workflow artifact;
- avoid making internal control jargon the first-reader entry point.

Recommended reader path:

| Reader | First path |
| --- | --- |
| General reader | Workflow overview to validator limit to human-gated promotion. |
| Physicist | Completion record to Distance-to-GR panel to forbidden conclusion summary. |
| AI researcher | Director decision to AgentJob contract to execution-role record. |
| Contributor | Current frontier to latest handoff to AgentJob allowlist and validators. |
| Operator | Memory preflight to validators to checkpoint boundary. |
| Site builder | PRD-03 to PRD-04 and PRD-07 before implementing role or tooling pages. |

## 13. Data, Source, and Provenance Requirements

Future workflow pages should declare:

- source artifacts used;
- whether each artifact is control authority, generated snapshot, registry
  metadata, retrieval support, or explanatory derivative;
- which fields are stable conceptual requirements and which are current-state
  snapshot data;
- whether human-gated authority is required for any claim promotion;
- which validators should cover implementation changes.

The website should not duplicate current AgentJob or handoff state in stable
copy. Current task and handoff IDs belong in PRD-09-style snapshots.

Workflow pages should prefer source-backed artifact-class explanations over
hard-coded examples. When examples are useful, they must be labeled as examples
and linked to source authority.

## 14. User Stories

1. As a general reader, I want a simple workflow diagram, so that I can see why
   the AI research system is controlled rather than free-running.
2. As a physicist, I want validator PASS separated from theorem proof, so that
   I do not overread operational checks.
3. As an AI researcher, I want to understand AgentJob contracts and role
   bindings, so that I can evaluate the agent architecture.
4. As a contributor, I want to know where handoffs and completions live, so
   that I can inspect the actual state before proposing work.
5. As an operator, I want the one-job rule and checkpoint boundary visible, so
   that implementation packets remain narrow and auditable.
6. As a site builder, I want workflow page requirements and acceptance
   criteria, so that future pages can explain control artifacts without
   granting them proof authority.

## 15. Acceptance Criteria

- The workflow page includes a lifecycle diagram from current state to handoff.
- The page states that validator PASS does not equal scientific proof.
- The page explains why local failures are preserved without becoming global
  no-go claims.
- The page explains how bounded theoretical continuation prevents generic
  pause.
- The page explains the one-job rule.
- The page explains Director Decision Records, AgentJobs, execution-role
  records, memory preflight, parent-child synthesis, completions, and handoffs.
- The page distinguishes workflow authority from physics claim authority.
- The page links current-state examples to PRD-09 freshness rules rather than
  treating transient state as stable copy.

## 16. Dependencies

- PRD-00 defines the master source-authority model and information
  architecture.
- PRD-05 defines memory, registry, retrieval, generated-derivative, and
  provenance boundaries.
- PRD-09 defines current-state freshness, stale-data, and source-precedence
  behavior.
- PRD-10 defines safe public language and forbidden claims.
- PRD-04 will define role and schema detail pages that extend this workflow
  explanation.
- PRD-07 will define tooling, scripts, validators, runtime, and checkpoint
  implementation details.
- PRD-08 and PRD-11 will orient future builders to repository topology and
  source maps.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Readers think agents prove physics autonomously. | Put role, validation, and human-gate boundaries beside every workflow claim. |
| Validators are mistaken for proof. | Require "operational consistency, not scientific proof" language on validation panels. |
| Role diagrams imply expanded authority. | Explain execution-role records and one-job boundaries before role catalog links. |
| Parent-child synthesis looks like multiple jobs. | State that child perspectives inherit one outer AgentJob boundary. |
| Current examples become stale. | Route transient task and handoff details through PRD-09 snapshot rules. |
| Local obstructions look like theory rejection. | Explain obstruction and freeze records as scoped routing evidence. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Check workflow copy for one-job rule, execution-role record, AgentJob
   contract, completion, handoff, and validation boundaries.
2. Search rendered copy for autonomous-proof language or validator-as-proof
   language.
3. Confirm lifecycle diagrams do not show child synthesis as separate
   independent AgentJobs.
4. Confirm current task or handoff examples follow PRD-09 freshness rules.
5. Confirm every workflow artifact links to source authority or a source
   authority explanation.
6. Run applicable route, content, provenance, build, browser, and
   implementation-control validators for implementation packets.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: implementation support foundation.

This PRD should follow PRD-09 because current-state status pages need a
workflow explainer to interpret active tasks, handoffs, validation states, and
next actions. It should precede PRD-04 and PRD-07 because role/schema and
tooling pages need the lifecycle model first.

## 20. Open Questions

1. Should the first public workflow page include a full AgentJob schema table or
   a simplified artifact-class overview with links?
2. Should parent-child synthesis be shown in the main lifecycle diagram or in a
   separate focused panel?
3. Should example control records be pulled from a dated snapshot bundle or
   linked directly as source provenance?
4. Should the validation panel group research-control, documentation-impact,
   memory, and build validators together or keep them by workflow phase?

These questions do not block this PRD. They should be resolved during PRD-04,
PRD-07, PRD-11, or future route implementation planning.

## 21. Definition of Done

This PRD is complete when:

- it defines research-agent workflow page requirements;
- it explains Director decisions, AgentJobs, execution-role records,
  completions, handoffs, memory preflight, parent-child synthesis, validators,
  and Distance-to-GR workflow requirements;
- it requires a lifecycle diagram from current state to handoff;
- it distinguishes operational validation from scientific proof;
- it preserves local obstruction and freeze boundaries;
- it gives future workflow pages a testable requirements contract.

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].

The AEther Flow Website. (2026). *Memory, Registry, and Retrieval Components*
[Product requirements document].

The AEther Flow Website. (2026). *Current Research Frontier for Website Use*
[Product requirements document].

The AEther Flow Website. (2026). *Website Positioning Guidance* [Product
requirements document].

The AEther-Flow Research Project. (2026, June 30). *Research control*
[Internal control documentation].

The AEther-Flow Research Project. (2026, June 30). *Continue research skill*
[Workflow contract].

The AEther-Flow Research Project. (2026, June 30). *AgentJob schema*
[Schema contract].

The AEther-Flow Research Project. (2026, June 30). *Director decision schema*
[Schema contract].

The AEther-Flow Research Project. (2026, June 30). *Execution role schema*
[Schema contract].

The AEther-Flow Research Project. (2026, June 30). *Mathematical decisiveness
completion contract* [Internal control note].
