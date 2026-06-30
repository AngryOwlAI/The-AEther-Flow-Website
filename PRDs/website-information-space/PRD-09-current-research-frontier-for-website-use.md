---
prd_id: "PRD-09"
title: "Current Research Frontier for Website Use"
status: "draft"
owner_role: "Documentation Curator"
project: "The-AEther-Flow"
website_area: "Current frontier dashboard, dated status snapshots, freshness warnings, blocked claims, and source precedence"
source_catalogue: "ImplementationPlans/aether_flow_project_components.md"
source_authority_class: "requirements-planning"
canonical_claim_authority: false
created: "2026-06-30"
last_reviewed: "2026-06-30"
depends_on:
  - "PRD-00-master-website-information-space.md"
  - "PRD-02-physics-and-mathematical-components.md"
  - "PRD-05-memory-registry-and-retrieval-components.md"
  - "PRD-10-website-positioning-guidance.md"
blocks_claim_promotion: true
requires_human_gate: false
claim_boundary_required: true
freshness_sensitive: true
requires_current_frontier_refresh: true
---

# PRD-09: Current Research Frontier for Website Use

## 1. Summary

This PRD defines how The AEther Flow Website should present current research
frontier status without converting a moving control snapshot into stale
permanent website truth.

The core product rule is: current frontier information must be displayed as a
dated, source-backed snapshot with visible source precedence, blocked claims,
and stale-data warnings. It may orient readers to active project state. It must
not become independent scientific, mathematical, governance, routing, or proof
authority.

## 2. Product Purpose

Readers need a concise way to understand what the project is working on now,
what remains blocked, and which source records govern that status. Without a
frontier layer, readers must inspect control files directly. With an unsafe
frontier layer, readers may overread a task, handoff, validation pass, or
generated summary as scientific proof.

The website should therefore provide a current-frontier surface that:

- explains the active task and latest handoff as a dated snapshot;
- identifies the current derivation milestone and burden family;
- shows Distance-to-GR status using layered anti-overread fields;
- displays exact blocked claims wherever progress is shown;
- separates validation health from physics proof;
- warns when source data is stale, missing, or contradictory;
- links readers to the authoritative source files.

## 3. Source Authority

This PRD is a requirements-planning artifact. It does not grant source,
scientific, mathematical, governance, routing, or research-workflow authority.

Current frontier implementation must refresh or verify from these upstream
sources:

- `research_control/program_state.yaml`;
- `research_control/current_frontier.md`;
- the latest relevant handoff under `research_control/handoffs/`;
- `registries/DISTANCE_TO_GR_LEDGER.csv`;
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`.

Source precedence for current-state data:

1. `research_control/program_state.yaml` is the compact live-state pointer.
2. The latest handoff named by `program_state.yaml` is immediate routing
   authority.
3. `registries/DISTANCE_TO_GR_LEDGER.csv` is the persistent burden-state
   ledger.
4. Task records, AgentJobs, completions, claim-boundary rows, role-execution
   rows, and approvals provide transaction provenance.
5. `research_control/current_frontier.md` is a generated synchronized
   reader-facing snapshot, not independent authority.
6. Website pages, PRDs, generated docs, memory, wiki notes, local caches, and
   semantic extracts are derivative or retrieval layers only.

If sources disagree, implementations must display the more authoritative
tracked source and label generated summaries as non-authoritative reader
surfaces.

## 4. Audience and Reader Jobs

| Audience | Reader job |
| --- | --- |
| General reader | Understand the current project direction without reading control YAML. |
| Physicist or reviewer | Inspect what is blocked before interpreting progress language. |
| AI researcher | Understand the active research-agent routing state and why validation is operational rather than proof. |
| Contributor | Find the current handoff, active task, and next recommended action before proposing work. |
| Operator | See whether displayed frontier data is fresh enough to trust as orientation. |
| Site builder | Build current-state pages that can be refreshed without rewriting stable physics pages. |

## 5. Scope

In scope:

- current research frontier dashboard requirements;
- current milestone and active task cards;
- latest handoff and next recommended action cards;
- Distance-to-GR status table requirements;
- blocked claims panel requirements;
- validation-status panel requirements;
- freshness, source-refresh, and stale-data behavior;
- source disagreement and precedence behavior;
- snapshot data-model requirements for future page implementation.

Out of scope:

- changing upstream research-control files;
- refreshing upstream source snapshots;
- editing ontology, TeX, PDF, generated HTML, GitHub-facing Markdown, wiki, or
  `.local` retrieval layers;
- implementing public routes in this packet;
- creating scientific claims or proof language;
- running the next research-control action;
- publishing, pushing, or deploying the website.

## 6. Non-Goals

This PRD must not:

- hard-code active task IDs, latest handoff IDs, milestone names, route labels,
  or next actions as permanent website copy;
- claim the current frontier is independent authority;
- treat validation PASS as scientific proof;
- treat generated summaries, memory, wiki notes, semantic extracts, local
  caches, registries, handoffs, approvals, roles, commits, or validators as
  physics proof;
- imply completed matter coupling, stress-energy semantics, Einstein-equation
  derivation, benchmark promotion, completed derivation, future
  source-extension impossibility, or global theory rejection unless tracked
  authority explicitly permits it;
- use current-status widgets to alter stable physics explanations.

## 7. Website Surfaces

Required surfaces:

- Current research frontier dashboard;
- Current milestone card;
- Active task and latest handoff card;
- Distance-to-GR status table;
- Blocked claims panel;
- Next recommended action card;
- Validation-status panel;
- Freshness and source-authority badge.

Supporting surfaces:

- source precedence note;
- source disagreement warning;
- stale-data warning;
- snapshot metadata panel;
- current frontier source links;
- "not proof" validation explainer;
- "what changed since last refresh" hook for future implementation.

## 8. Functional Requirements

1. Treat all current-state data as a dated snapshot.
2. Display `last_source_refresh` or an equivalent timestamp on every current
   frontier page or card.
3. Display source basis and source-authority class near the dashboard title.
4. Display the active task ID and latest handoff ID only as snapshot data.
5. Display the current milestone and current burden as snapshot data.
6. Display the next recommended action as routing context, not as website
   instruction or scientific result.
7. Show blocked claims prominently whenever progress status is shown.
8. Explain that validation PASS indicates operational consistency, not
   scientific proof.
9. Avoid permanent hard-coding of active task IDs, handoff IDs, route labels,
   and current milestone details in stable page copy.
10. Provide a stale-data warning if the dashboard has not been refreshed within
    the configured freshness window.
11. Provide a stronger warning if required source files are missing,
    unreadable, or contradictory.
12. Keep current frontier pages updateable without rewriting core physics,
    ontology, benchmark, or derivation-roadmap pages.
13. Preserve source links as provenance while keeping the reader journey
    internal-first.
14. Require snapshot regeneration or verification before any release that
    changes current frontier data.

## 9. Non-Functional Requirements

- Freshness: Current-state pages must make age and source basis visible.
- Stability: Stable physics pages must not depend on transient active task
  identifiers.
- Safety: Blocked-claim language must appear before or beside progress
  language.
- Maintainability: Frontier data should be supplied through a small data
  contract or manifest-like source, not duplicated across multiple pages.
- Auditability: Each visible current-state field should map back to a source
  field or source section.
- Reversibility: A stale or contradictory snapshot should fail closed into a
  warning state rather than hiding uncertainty.
- Accessibility: Snapshot tables and warning badges must use readable text,
  semantic table structure, and non-color-only status cues.

## 10. Claim Boundary

This PRD may specify website content that explains:

- current research status as a dated snapshot from tracked sources;
- the current milestone and burden family as source-derived routing context;
- blocked claims as trust-preserving anti-overread information;
- validation status as operational consistency information;
- next recommended action as a source-reported route, not as proof.

This PRD must not authorize website content claiming:

- the current frontier snapshot is independent authority;
- matter coupling has been solved or adopted;
- stress-energy semantics, stress-energy tensor, detector semantics, or matter
  action have been established from source-side structure;
- Einstein equations have been derived from AEther / AEther-flow substrate
  structure;
- the exact-GR benchmark has been promoted from first principles;
- `MetricData(E)` or unscoped `g_eff` adoption is authorized without tracked
  source authority;
- validation, registry, handoff, role, approval, generated output, memory,
  wiki, local cache, or commit status is scientific proof;
- a local obstruction or freeze is global theory rejection.

## 11. Content Requirements

The current frontier dashboard must include at least:

| Element | Required content | Boundary |
| --- | --- | --- |
| Snapshot metadata | Last source refresh, source files checked, source authority class. | Must not imply independent authority. |
| Active task | Task ID, title or objective, source path when available. | Snapshot only; not permanent copy. |
| Latest handoff | Handoff ID, summary, validation state when available. | Routing evidence, not proof. |
| Current milestone | Target derivation milestone and burden family. | Must include open-burden language. |
| Distance-to-GR table | Burden ID, milestone, control status, mathematical status, physical status, promotion status, overread guard. | Ledger governs if page summary drifts. |
| Blocked claims | Exact forbidden readings from current frontier and claim-boundary registry. | Must be visible near progress. |
| Next action | Source-reported next recommended action. | Must be labeled as tracked route context. |
| Validation status | Operational checks and pass/pending/fail state. | Must state not scientific proof. |

Required snapshot fields for a future implementation:

```text
frontier_snapshot:
  last_source_refresh
  source_paths_checked
  source_precedence
  active_task_id
  active_task_source_path
  latest_handoff_id
  latest_handoff_source_path
  current_status
  current_route_family
  target_derivation_milestone
  current_burden
  next_recommended_action
  blocked_claims
  distance_to_gr_rows
  validation_statuses
  retrieval_warning
  source_disagreement_warning
  stale_data_warning
```

Current source observation at PRD drafting time:

- `research_control/program_state.yaml` names active task `RT-20260630-007`
  and latest handoff `handoff-0359`.
- `research_control/current_frontier.md` states that it is a generated
  synchronized snapshot, not independent routing authority and not a physics
  proof surface.
- The current target derivation milestone is `matter_coupling`, but the
  current source state preserves no matter-coupling derivation or adoption.
- The current next route is a bounded future ontology-formalizer packet for a
  proposal-only `MatterCouplingPreconditionAssembly_v1(E)` target.
- The current blocked-claim family includes no canonical ontology edit, no
  source-law adoption, no `MetricData(E)` adoption, no `g_eff` scope change, no
  coupling-law adoption, no matter-coupling derivation or adoption, no
  stress-energy semantics, no stress-energy tensor, no detector semantics, no
  matter action, no Einstein equations, no benchmark promotion, and no
  completed derivation.

These observations are drafting evidence only. Future implementation must
refresh or verify them from source before publication.

Required copy fragments:

- "Current frontier status is a dated source-backed snapshot."
- "This page is not independent scientific authority."
- "Validation PASS means operational consistency, not physics proof."
- "Blocked claims are part of the status, not a footnote."
- "If the generated frontier summary contradicts tracked control files, the
  tracked control files govern."

## 12. UX and Navigation Requirements

Current frontier navigation should:

- enter from the master Current Frontier route family;
- provide a compact dashboard summary before detailed tables;
- place freshness and source-authority badges near the page heading;
- display blocked claims beside progress status;
- link to source authority and physics derivation-roadmap pages for context;
- avoid mixing stable educational physics copy with transient active-state
  widgets;
- provide clear empty, stale, contradictory, and unavailable states.

Recommended reader path:

| Reader | First path |
| --- | --- |
| General reader | Current status summary to blocked claims to "what remains open." |
| Physicist | Distance-to-GR table to ledger provenance to physics claim-status page. |
| AI researcher | Active task and handoff to validation status to research-control workflow. |
| Contributor | Latest handoff to next recommended action to source authority. |
| Operator | Freshness badge to source disagreement warning to validation panel. |
| Site builder | PRD-09 to PRD-05 to PRD-03 before implementing workflow pages. |

## 13. Data, Source, and Provenance Requirements

Current frontier data should be generated or verified from source before
publication. A future implementation should record:

- source paths checked;
- source file modified times or commit hashes when available;
- render or import timestamp;
- source precedence decision;
- stale threshold;
- disagreement or missing-source findings;
- whether generated summaries matched tracked authority.

Freshness behavior:

| Condition | Required website behavior |
| --- | --- |
| Fresh and source-consistent | Show normal status with source refresh timestamp. |
| Source age exceeds threshold | Show stale-data warning and avoid strong current-language phrasing. |
| Required source missing | Show unavailable state and source-basis warning. |
| Source disagreement detected | Show disagreement warning and prefer higher-authority source. |
| Validation pending or failed | Show operational validation state without treating it as scientific result. |

The dashboard should use a single snapshot data source for display. Duplicating
current status in unrelated static copy is prohibited unless that copy also
declares freshness and source basis.

## 14. User Stories

1. As a general reader, I want to see the current frontier as a dated snapshot,
   so that I do not mistake it for permanent project status.
2. As a physicist, I want blocked claims shown beside progress, so that I can
   evaluate claim strength accurately.
3. As an AI researcher, I want validation status separated from proof status,
   so that I can understand the research-control system honestly.
4. As a contributor, I want links to the active task and handoff, so that I can
   inspect current routing before proposing work.
5. As an operator, I want stale-data warnings, so that I can avoid publishing
   old frontier state as current.
6. As a site builder, I want a clear snapshot data contract, so that I can build
   a maintainable dashboard without scattering task IDs through stable copy.

## 15. Acceptance Criteria

- The status page includes `last_source_refresh` or an equivalent visible
  field.
- The status page says it is not independent source authority.
- The status system can be updated without rewriting core physics pages.
- Blocked claims are visible whenever progress status is shown.
- Validation status is described as operational consistency, not scientific
  proof.
- Active task ID, handoff ID, current milestone, and next route are rendered as
  snapshot data rather than hard-coded permanent copy.
- Stale, missing-source, and source-disagreement states have explicit warning
  behavior.
- Distance-to-GR rows expose control, mathematical, physical, promotion, and
  overread-guard fields.
- Implementation can fail closed when freshness or source precedence cannot be
  established.

## 16. Dependencies

- PRD-00 defines the master information architecture and source-authority
  policy.
- PRD-02 defines physics claim-status and derivation-roadmap boundaries.
- PRD-05 defines source authority, registry, memory, derivative, and provenance
  requirements.
- PRD-10 defines safe public language and forbidden claims.
- PRD-03 will define the research-control workflow, AgentJob, validation, and
  handoff lifecycle pages that current frontier pages link to.
- PRD-07 will define tooling, scripts, and runtime expectations for future
  snapshot generation.
- PRD-11 will define concise site-builder source maps.

## 17. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Current status becomes stale. | Require `last_source_refresh`, stale warnings, and refresh before release. |
| Readers infer proof from validation PASS. | Place "operational consistency, not proof" language in validation panels. |
| Readers infer progress from task IDs alone. | Show blocked claims and Distance-to-GR overread guards beside task status. |
| Generated frontier summary drifts from tracked authority. | Use source precedence and disagreement warnings; tracked authority governs. |
| Stable physics pages become coupled to transient status. | Use a separate snapshot data source and route family. |
| Future source state changes claim boundaries. | Treat all current-state fields as refreshable data, not static page copy. |

## 18. Validation Plan

Before implementing pages from this PRD:

1. Verify source precedence against `program_state.yaml`, latest handoff,
   Distance-to-GR ledger, claim-boundary registry, and current frontier
   snapshot.
2. Check that every progress display includes blocked claims or a direct link to
   blocked claims.
3. Check that validation status never uses proof language.
4. Check that stale, missing-source, and source-disagreement states render
   clearly.
5. Search rendered copy for hard-coded active task, handoff, milestone, or route
   identifiers outside the snapshot data model.
6. Run applicable build, content, provenance, implementation-control, and
   browser checks for any route implementation.

For this PRD packet, validation is limited to implementation-control structure,
git diff hygiene, and the Python test suite.

## 19. Launch Priority

Priority: MVP foundation.

This PRD completes the minimum PRD package for source-backed public
orientation. It should follow PRD-02 because current frontier pages depend on
physics claim-status discipline. It should precede PRD-03 because the current
frontier links readers into research-control workflow, AgentJob, handoff, and
validation lifecycle pages.

## 20. Open Questions

1. What freshness threshold should the first public implementation use:
   release-time refresh, daily freshness, or explicit manual refresh?
2. Should stale current-frontier widgets hide transient IDs or display them with
   a warning?
3. Should the first dashboard import from generated Markdown, a derived JSON
   snapshot, or a website-local manifest created from upstream control files?
4. Should source-disagreement failures block a build, block a release, or render
   an explicit warning page?

These questions do not block this PRD. They should be resolved in a future
implementation plan or PRD-07 tooling/runtime packet.

## 21. Definition of Done

This PRD is complete when:

- it defines dated current-frontier snapshot requirements;
- it defines source precedence and stale-data behavior;
- it requires visible blocked claims wherever current progress is shown;
- it separates validation status from scientific proof;
- it avoids hard-coding transient active-state details as permanent copy;
- it gives future current-frontier pages a testable requirements contract.

## References

The AEther Flow Website. (2026). *The AEther-Flow Research Project:
Functionality, Logic, Features, and Systems Catalogue* [Project catalogue].

The AEther Flow Website. (2026). *The AEther-Flow Website PRD System*
[Implementation handoff].

The AEther Flow Website. (2026). *AEther-Flow Website Information Space*
[Product requirements document].

The AEther Flow Website. (2026). *Physics and Mathematical Components*
[Product requirements document].

The AEther Flow Website. (2026). *Memory, Registry, and Retrieval Components*
[Product requirements document].

The AEther Flow Website. (2026). *Website Positioning Guidance* [Product
requirements document].

The AEther-Flow Research Project. (2026, June 30). *Current research frontier*
[Generated internal control snapshot].

The AEther-Flow Research Project. (2026, June 30). *Program state* [Internal
research-control state file].

The AEther-Flow Research Project. (2026, June 30). *Distance-to-GR ledger*
[Internal registry].

The AEther-Flow Research Project. (2026, June 30). *Claim boundary registry*
[Internal registry].
