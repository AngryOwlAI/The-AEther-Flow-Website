---
prd_id: "PRD-04"
title: "Role and Schema Components"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Role catalogue, authority inspector, schema reference map, claim-authority matrix, and human-gated promotion explainer"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-03-research-control-and-agent-workflow.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
  - "PRD-10-website-positioning-guidance.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
---

# PRD-04: Role and Schema Components

## 1. Summary

This PRD defines how The AEther Flow Website should explain project roles,
role authority, execution-role records, and schema contracts. It covers the
role catalogue, role authority inspector, schema reference map, "who can make
which claim?" matrix, and human-gated role explainer required by the website
PRD system.

The central product rule is that role pages may explain what roles can do,
cannot do, produce, and require for verification. They must not imply that a
role identity, schema, registry row, validator, or execution record creates
scientific proof or claim-promotion authority by itself.

## 2. Product Purpose

The AEther Flow Project uses named roles and schemas to keep research work
bounded, auditable, and hard to overread. Readers need a clear map of which
roles route work, construct draft/control artifacts, audit hidden imports,
repair project-control systems, or require explicit human approval.

The website should help readers understand:

- the difference between a registered base role and a task-local execution-role
  record;
- why some roles can create outputs but cannot promote claims;
- why the Gate Chair is human-gated and paused unless tracked approval exists;
- how schemas operate as control contracts rather than decorative reference
  pages;
- how registries establish provenance and validation metadata without becoming
  proof surfaces;
- where to verify role versions, execution records, and schema requirements in
  the upstream source project.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, routing, role, schema, workflow, or
claim-promotion authority.

Source basis for implementation should include:

- `.agents/roles/`;
- `.agents/schemas/ROLE_SCHEMA.md`;
- `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md`;
- `.agents/schemas/AGENT_JOB_SCHEMA.md`;
- `.agents/schemas/EXECUTION_ROLE_SCHEMA.md`;
- `.agents/schemas/DOCUMENTATION_IMPACT_SCHEMA.md`;
- `registries/AGENT_ROLE_REGISTRY.csv`;
- `registries/ROLE_EXECUTION_REGISTRY.csv`;
- `research_control/tasks/`;
- `research_control/handoffs/`;
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`.

The active role version for any reader-facing page should be resolved from
`AGENT_ROLE_REGISTRY.csv` at implementation time. Plan examples and older role
paths are source anchors, not automatic active-version truth.

Role contracts and schemas are upstream control authority. Website pages,
PRDs, generated explainers, memory extracts, wiki notes, local caches, and
semantic summaries are explanatory or retrieval layers unless a higher
authority tracked source says otherwise.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand that named roles are bounded responsibilities, not autonomous proof authorities. |
| Physicist or reviewer | Inspect which roles may construct, audit, refute, route, or human-gate scientific claims. |
| AI researcher | Understand how schemas constrain role use, execution records, AgentJobs, and Director decisions. |
| Contributor | Know which role or schema to inspect before proposing a task or continuing work. |
| Operator | Confirm whether a task needs a registered role, task overlay, provisional role, or human gate. |
| Site builder | Build role and schema pages without hard-coding stale versions or overstating authority. |

## 5. Scope

In scope:

- role catalogue requirements;
- role detail page requirements;
- role authority inspector requirements;
- schema reference map requirements;
- "who can make which claim?" matrix requirements;
- human-gated Gate Chair explainer requirements;
- registered-role versus execution-role boundary requirements;
- source and registry provenance requirements;
- acceptance criteria for role/schema pages.

Out of scope:

- changing upstream role contracts, schemas, registries, AgentJobs, tasks, or
  handoffs;
- implementing public routes in this packet;
- creating role records or execution-role records;
- registering new roles;
- promoting, closing, adopting, rejecting, or freezing scientific claims;
- editing public website copy, assets, manifests, generated derivatives, wiki
  layers, or `.local` retrieval layers;
- pushing or deploying.

## 6. Non-Goals

This PRD must not:

- claim that roles prove scientific results by identity;
- treat role contracts, schemas, registry rows, validator PASS, handoffs,
  commits, or execution-role records as scientific proof;
- imply that base roles silently acquire task-specific permissions;
- imply that task overlays or one-job provisional roles are reusable permanent
  roles;
- present the Gate Chair as executable without explicit tracked approval;
- present protected promotion, canonical ontology adoption, benchmark status,
  Gate Chair authority, or permanent role registration as automated outcomes;
- use generated derivatives, wiki notes, semantic extracts, or local memory as
  source authority for role or schema claims.

## 7. Website Surfaces

Required surfaces:

- Role catalogue;
- Role detail page template;
- Role authority inspector;
- Schema reference map;
- "Who can make which claim?" matrix;
- Human-gated role explainer;
- Registered-role versus execution-role explainer;
- Active-version provenance panel.

Supporting surfaces:

- role-family filter by physics, research operations, project control, and
  scientific gate;
- authority-level glossary;
- role output type guide;
- claim-boundary badges;
- schema-to-artifact map;
- registry provenance card;
- stale-version warning for superseded role contracts.

## 8. Functional Requirements

1. Provide a role catalogue that includes, at minimum, Director of Research,
   Candidate Constructor, Ontology Formalizer, Refuter, Smuggling Auditor, Gate
   Chair, Theoretical Continuation Selector, Documentation Curator,
   Memory-System Maintainer, Process Integrity Auditor, Project-Control
   Maintainer, Project-System Director, and Validator Engineer.
2. Provide a schema reference map that includes Role Schema, Director Decision
   Schema, AgentJob Schema, Execution Role Schema, and Documentation Impact
   Schema.
3. For every role page, include the same four reader questions: "can do,"
   "cannot do," "outputs," and "claim boundary."
4. Resolve active role versions from `AGENT_ROLE_REGISTRY.csv` and label
   superseded versions as historical when they are shown.
5. Explain that registered role contracts are stable templates, while
   execution-role records bind one AgentJob to exact task-local semantics.
6. Explain `registered_role`, `task_overlay`, and `one_job_provisional_role`
   as distinct execution-role modes.
7. Explain that a task overlay may narrow, constrain, or task-bind a role, but
   cannot silently grant protected authority.
8. Explain that one-job provisional roles expire after their owning AgentJob
   and are not reusable until registered.
9. Explain that schemas are control contracts with required fields,
   validators, and authority consequences.
10. Explain that AgentJobs are bounded executable contracts and immutable after
    creation.
11. Explain that Director Decision Records preserve routing reasoning and
    should be superseded rather than silently rewritten after activation.
12. Explain that documentation-impact records account for project-system
    changes and generated derivatives without making derivatives authority.
13. Explain that the Gate Chair is defined but paused; execution and any
    protected scientific promotion require explicit tracked approval.
14. Explain that physics roles may produce draft/control outputs, audits,
    stresses, candidate witnesses, or routing decisions, but cannot adopt
    ontology, promote benchmarks, derive GR, or create proof authority by role
    identity.
15. Explain that project-control roles can modify allowed control or tooling
    paths only inside an owning AgentJob allowlist.
16. Explain that registries support provenance, validation, and historical
    compatibility; they do not by themselves prove physics claims.
17. Provide a claim-authority matrix that separates routing authority,
    draft/control output authority, project-control modification authority,
    human-gated promotion authority, and no-proof status.
18. Provide links from role/schema pages to PRD-03 workflow concepts, PRD-05
    provenance concepts, and PRD-07 tooling and validation concepts.

## 9. Non-Functional Requirements

- Accuracy: Role and schema pages must be generated or reviewed against active
  upstream role contracts, schemas, and registries.
- Version awareness: The UI must distinguish active, superseded, historical,
  and paused/status-defined roles.
- Auditability: Every authority claim should map to a source role contract,
  schema, registry row, execution-role record, or claim-boundary record.
- Safety: Claim-boundary language must be adjacent to authority language.
- Maintainability: Pages should describe stable artifact classes and active
  registry resolution rules instead of hard-coding transient task examples.
- Comprehension: Readers should see the authority model before low-level
  frontmatter detail.
- Reversibility: Future role or schema changes should update the catalogue
  without changing the website's core authority model.

## 10. Claim Boundary

This PRD may specify website content that explains:

- roles as bounded project responsibilities;
- active role versions as registry-resolved source facts;
- schemas as control contracts;
- execution-role records as task-local authority bindings;
- registries as provenance and validation metadata;
- human gates as required protection for claim promotion.

This PRD must not authorize website content claiming:

- a role, registry, schema, validation result, or execution record proves a
  physics result;
- any non-Gate Chair role may promote protected scientific claims;
- Gate Chair promotion may occur without explicit tracked approval;
- task overlays or one-job provisional roles permanently expand role authority;
- project-control roles may change physics source status;
- generated derivatives, local memory, wiki notes, semantic extracts, or PRDs
  are source authority for scientific claims.

## 11. Content Requirements

The role catalogue must include a compact matrix like this:

| Role | Primary authority | Can do | Cannot do |
| --- | --- | --- | --- |
| Director of Research | Routing control | Select one bounded next step and create or reuse one AgentJob when no human gate is required. | Modify sources or promote claims. |
| Candidate Constructor | Science draft | Construct one bounded candidate, witness, finite model, or precise obstruction under the job boundary. | Adopt ontology, promote `M_src`, establish `g_eff`, derive Einstein equations, or claim completed derivation. |
| Ontology Formalizer | Science draft | Define draft/control source-side primitives, assumptions, maps, domains, and proof obligations. | Edit canonical ontology or adopt ontology changes. |
| Refuter | Science draft adversarial | Stress candidates and preserve local negative results. | Globally reject the theory or close a route without tracked authority. |
| Smuggling Auditor | Science draft adversarial | Audit hidden target imports and process-authority laundering. | Promote claims after a local audit pass. |
| Gate Chair | Human-gated scientific gate | Render protected promotion, closure, or suspension decisions only after explicit tracked approval. | Execute autonomously. |
| Theoretical Continuation Selector | Science draft routing | Select one bounded theoretical next packet when the route is underdetermined. | Create child jobs, promote ontology, or request Gate Chair review without the proper boundary. |
| Documentation Curator | Project documentation | Produce source-backed public documentation and documentation-impact records within allowlists. | Change physics claim status, control contracts, or generated derivatives as authority. |
| Memory-System Maintainer | Project control | Maintain source-first memory, registry, wiki, Obsidian, and retrieval tooling. | Make retrieval layers authoritative. |
| Process Integrity Auditor | Process control | Repair control-state defects when the correct state is uniquely determined. | Resolve ambiguous states without human input. |
| Project-Control Maintainer | Project control | Maintain role, schema, skill, control, and validator contracts inside an owning AgentJob. | Change physics claims or explanatory-only documentation without explicit scope. |
| Project-System Director | Project-control routing | Route one bounded project-system improvement job from tracked signals. | Execute the selected job or perform physics derivation. |
| Validator Engineer | Project-system validation | Improve deterministic validators, tests, and checkpoint gates. | Make human policy decisions or alter scientific verdicts. |

Every role detail page must include:

- source contract and registry row;
- active status and version;
- role kind and authority level;
- whether autonomous execution is allowed;
- whether output creation is allowed;
- whether source modification is allowed;
- whether claim promotion is allowed;
- whether a human gate is required;
- default validators;
- allowed and forbidden source classes;
- "can do" summary;
- "cannot do" summary;
- expected outputs;
- claim-boundary summary;
- links to execution examples only when examples are clearly labeled as
  examples and routed through freshness rules.

The schema reference map must explain:

| Schema | Controls | Reader explanation |
| --- | --- | --- |
| Role Schema | Registered role contracts | Defines immutable role-version identity, authority fields, validators, and human-gate status. |
| Director Decision Schema | Director Decision Records | Makes routing reasoning auditable and requires supersession instead of silent rewrite. |
| AgentJob Schema | AgentJobs | Defines bounded executable job contracts, allowlists, validators, memory preflight, and claim boundary. |
| Execution Role Schema | Execution-role records | Binds one AgentJob to registered role, task overlay, or one-job provisional semantics. |
| Documentation Impact Schema | Documentation-impact receipts | Records whether project-system changes required documentation updates and how generated derivatives were handled. |

The claim-authority matrix must separate:

- can route work;
- can create draft/control artifacts;
- can modify project-control files;
- can modify canonical science or benchmark sources;
- can promote protected scientific claims;
- requires human gate;
- creates proof authority.

The correct value for "creates proof authority" is always no. A role may
contribute evidence, routing, construction, audit, refutation, or human-gated
decision records, but proof authority still depends on source mathematics,
tracked approvals, and applicable source-governance records.

## 12. UX and Navigation Requirements

Role and schema navigation should:

- begin with the role authority matrix before individual role detail pages;
- group roles by physics construction, physics audit, routing, documentation,
  project-control, validation, memory, and human-gated authority;
- show active/superseded/status-defined status visibly without relying on color
  alone;
- include claim-boundary text near every authority-level label;
- link each role to its source contract, registry row, and relevant schema;
- link schema pages to artifact examples without making transient task IDs the
  primary reader journey;
- link workflow lifecycle concepts back to PRD-03;
- link provenance and registry concepts back to PRD-05;
- link validators and runtime checks forward to PRD-07;
- keep current task examples freshness-sensitive under PRD-09 rules;
- avoid making internal source paths the only way to understand the page.

Recommended reader path:

| Reader | First path |
| --- | --- |
| General reader | Role authority matrix to human-gated explainer to role catalogue. |
| Physicist | Physics roles to claim-boundary matrix to Gate Chair explainer. |
| AI researcher | Role Schema to Execution Role Schema to AgentJob Schema. |
| Contributor | Active role catalogue to execution-role mode explainer to source links. |
| Operator | Authority inspector to schema map to validator and approval gates. |
| Site builder | PRD-04 to PRD-03, PRD-05, and PRD-07 before route implementation. |

## 13. Data, Source, and Provenance Requirements

Future role and schema pages should declare:

- source artifacts used;
- active role version source and registry row;
- whether shown examples are stable contract data or freshness-sensitive
  current-state examples;
- whether the role is active, superseded, historical, paused, or
  status-defined;
- whether the role requires human gate;
- validators or checks used for implementation changes;
- last source-inspection date for any copied contract metadata.

The website should not duplicate registry data without a refresh strategy.
When role metadata is rendered as content, it should either be generated from
source registries or manually reviewed against the current registry row.

Role and schema pages must classify sources as:

- role contract;
- schema contract;
- execution-role record;
- registry metadata;
- claim-boundary registry;
- source authority explainer;
- example current-state record;
- explanatory derivative.

## 14. User Stories

1. As a general reader, I want role authority explained plainly, so that I do
   not mistake agent roles for proof machines.
2. As a physicist, I want to see which roles can construct, audit, refute, or
   human-gate claims, so that I can evaluate status without overreading local
   artifacts.
3. As an AI researcher, I want schemas presented as control contracts, so that
   I can understand the agent architecture's boundaries.
4. As a contributor, I want active role versions and source links, so that I
   can inspect the authoritative contract before proposing work.
5. As an operator, I want a role authority inspector, so that I can identify
   when a task needs a human gate or a project-system route.
6. As a site builder, I want acceptance criteria for role/schema pages, so that
   future implementation preserves source authority.

## 15. Acceptance Criteria

- The role catalogue includes all required roles from this PRD.
- Every role page includes "can do," "cannot do," "outputs," and "claim
  boundary."
- The Gate Chair page states that protected scientific promotion requires
  explicit tracked human authority.
- Schema pages explain schemas as control contracts, not decorative
  documentation.
- No role is presented as having authority beyond its registered contract and
  task-local execution record.
- Active role versions are resolved from `AGENT_ROLE_REGISTRY.csv` or clearly
  marked as manually reviewed against it.
- Superseded role versions are not presented as current defaults.
- The claim-authority matrix states that roles, registries, validators, and
  execution records do not create proof authority.
- Execution-role pages distinguish registered roles, task overlays, and
  one-job provisional roles.
- Current examples follow PRD-09 freshness and stale-data rules.

## 16. Dependencies

- PRD-00 defines the master source-authority model and information
  architecture.
- PRD-03 defines Director decisions, AgentJobs, execution roles, completions,
  handoffs, and validators as workflow concepts.
- PRD-05 defines source authority, registries, generated derivatives, memory,
  and provenance boundaries.
- PRD-09 defines current-state freshness and stale-data behavior for examples.
- PRD-10 defines safe public language and forbidden claim language.
- PRD-07 will define tooling, skills, validators, scripts, runtime, and cache
  details that support role/schema page implementation.
- PRD-08 and PRD-11 will orient future builders to repository topology and
  source maps.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Readers think a role identity grants proof authority. | Put the claim-authority matrix before detailed role pages. |
| Superseded role contracts are shown as active. | Resolve active versions from `AGENT_ROLE_REGISTRY.csv` and label historical versions. |
| Gate Chair appears executable without approval. | Require a dedicated human-gated role explainer and explicit tracked-approval language. |
| Schema pages become decorative. | Explain required fields, validators, and control consequences for each schema. |
| Execution-role overlays look like permanent role expansion. | State one-job expiration and non-reusability rules near overlay examples. |
| Registry metadata is mistaken for proof. | Classify registries as provenance and validation metadata, not physics proof. |
| Current examples become stale. | Route examples through PRD-09 snapshot and freshness rules. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Check every role page for "can do," "cannot do," "outputs," and "claim
   boundary" sections.
2. Confirm active role versions against `AGENT_ROLE_REGISTRY.csv`.
3. Confirm schema explanations mention required fields and contract behavior.
4. Search rendered copy for role-as-proof, validator-as-proof, and
   registry-as-proof language.
5. Confirm the Gate Chair page states explicit tracked human authority is
   required for protected promotion.
6. Confirm execution-role pages distinguish registered role, task overlay, and
   one-job provisional role.
7. Confirm examples are either stable contract examples or PRD-09 freshness
   snapshots.
8. Run applicable route, content, provenance, build, browser, and
   implementation-control validators for implementation packets.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: implementation support foundation.

This PRD should follow PRD-03 because role/schema pages depend on the
research-control lifecycle model. It should precede PRD-07 because tooling and
validator pages need the role and schema authority model to explain who owns
which checks and boundaries.

## 20. Open Questions

1. Should role metadata be rendered from registry data at build time or kept as
   reviewed Markdown with a source-inspection date?
2. Should the authority inspector be a standalone route, a reusable component,
   or both?
3. Should role detail pages include recent execution examples, or should
   examples live only in PRD-09-style current-state snapshots?
4. Should schema pages show full required-field tables or reader-first summaries
   with source links?

These questions do not block this PRD. They should be resolved during PRD-07,
PRD-08, PRD-11, or future route implementation planning.

## 21. Definition of Done

This PRD is complete when:

- it defines the role catalogue, authority inspector, schema map,
  claim-authority matrix, and human-gated explainer requirements;
- it lists all required roles and schemas;
- it requires every role page to include "can do," "cannot do," "outputs," and
  "claim boundary";
- it requires Gate Chair human-gate language;
- it explains schemas as control contracts;
- it preserves the distinction between registered roles and task-local
  execution-role records;
- it prevents role, registry, validator, and schema pages from implying proof
  authority.

## References

The AEther Flow Project. (2026). *Agent role registry* [Registry].

The AEther Flow Project. (2026). *AgentJob schema* [Schema contract].

The AEther Flow Project. (2026). *Director decision schema* [Schema contract].

The AEther Flow Project. (2026). *Documentation impact schema* [Schema
contract].

The AEther Flow Project. (2026). *Execution role schema* [Schema contract].

The AEther Flow Project. (2026). *Role execution registry* [Registry].

The AEther Flow Project. (2026). *Role schema* [Schema contract].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].

The AEther Flow Website. (2026). *Research-Control and Agent Workflow*
[Product requirements document].

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].
