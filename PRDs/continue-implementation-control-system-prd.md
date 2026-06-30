# Continue Implementation Control System PRD

## Problem Statement

The AEther Flow Website has PRDs, implementation plans, task-packet documents,
route manifests, provenance manifests, validators, and quality gates, but it
does not yet have a live implementation-continuation control system equivalent
to the upstream project's `continue research` workflow.

The current risk is that future website implementation work can be routed from
old plans, stale task-packet text, or conversational memory rather than live
tracked state. That creates avoidable drift: an agent can batch too much work,
change public claims without approval, skip manifest/provenance duties, commit
unrelated files, or confuse website implementation authority with upstream
research authority.

The user needs a website-local `continue implementation` system that preserves
the useful invariants of the upstream `continue research` system while avoiding
its physics-specific role and registry complexity.

## Solution

Create a lightweight, website-local implementation-control system. The system
will resolve the next bounded website implementation packet from live local
state, then let Codex execute exactly one authorized packet per invocation.
After successful execution, a narrow checkpoint path will validate the packet,
stage only the packet's allowed write paths, create a local Git commit, and
leave push or deployment to explicit user instruction.

The upstream AEther Flow project remains read-only from this system. Website
implementation may inspect upstream `program_state.yaml`, handoffs, registries,
and source files for provenance and source-authority checks, but it must not
mutate upstream control state.

## Requirements

- REQ-001: The system must be strictly website-local. It may inspect upstream
  source project files for provenance, but must not modify the upstream project.
- REQ-002: Live website implementation state must outrank PRDs,
  implementation plans, task packets, and memory-derived context.
- REQ-003: Add a lightweight control model with program state, handoff records,
  task records, job records, and completion records.
- REQ-004: Add a deterministic resolver command that reports the next bounded
  packet in JSON by default and supports a human-readable summary.
- REQ-005: Execute at most one bounded website implementation packet per
  invocation when the resolver reports a ready boundary.
- REQ-006: Require explicit approval before packets that affect public claims,
  source-refresh uncertainty, broad navigation, route retirement, shared visual
  systems, public downloadable assets, manifest authority records, deployment,
  push, or other high-blast-radius changes.
- REQ-007: Add implementation-control validation and include it in the standard
  repository validation chain before the Astro build.
- REQ-008: Add a narrow checkpoint command that validates the active job,
  stages only allowed packet files, creates a local Git commit, and refuses
  ambiguous dirty-state conditions.
- REQ-009: Bootstrap from an explicit initial local task rather than
  retroactively promoting older plans into live authority.
- REQ-010: Preserve the Source Authority Boundary for all public scientific,
  mathematical, governance, and research-workflow claims.
- REQ-011: Provide documentation and tests sufficient for future Codex sessions
  to use the control system without guessing command semantics.
- NFR-001: Keep the implementation dependency-light and consistent with the
  existing Astro plus Python tooling.
- NFR-002: Make resolver and validator behavior deterministic and suitable for
  automated tests.
- NFR-003: Keep checkpointing non-destructive toward unrelated user work.
- NFR-004: Do not push, deploy, refresh upstream, or invent completion evidence
  from checkpointing.

## User Stories

1. As a website maintainer, I want a live implementation state file, so that
   future work starts from current tracked state rather than stale plans.
2. As a website maintainer, I want the resolver to name the next bounded
   implementation packet, so that continuation work is narrow and auditable.
3. As a website maintainer, I want PRDs and implementation plans treated as
   route context, so that useful planning remains available without becoming
   stale authority.
4. As a website maintainer, I want explicit approval gates for claim-bearing
   and high-blast-radius changes, so that automation cannot silently strengthen
   source claims or reshape public reader journeys.
5. As a website maintainer, I want upstream source inspection to remain
   read-only, so that the website preserves the source-authority boundary.
6. As an implementation agent, I want a JSON resolver command, so that I can
   start a continuation turn deterministically.
7. As an implementation agent, I want a summary mode, so that I can inspect the
   next boundary quickly in human-readable form.
8. As an implementation agent, I want task and job records with allowed read
   paths, allowed write paths, validators, and stop conditions, so that I can
   execute one packet without widening scope.
9. As an implementation agent, I want a validator in `npm run validate`, so
   that broken implementation-control state is caught by normal repo health
   checks.
10. As an implementation agent, I want checkpointing to stage only allowed
    packet files, so that unrelated user work is preserved.
11. As an implementation agent, I want checkpointing to create a local commit
    only after validation, so that successful continuation packets have durable
    Git evidence.
12. As a reviewer, I want completion and handoff records, so that I can inspect
    what changed, what was verified, what remains blocked, and what the logical
    next packet is.
13. As a reviewer, I want no push or deployment without explicit instruction,
    so that publication and release remain deliberate operations.

## Implementation Decisions

- Add a new website-local `implementation_control/` directory as the live
  authority for website implementation continuation.
- Use a lightweight record model rather than the upstream research repo's full
  AgentJob, DDR, role registry, and physics-routing schema.
- Use these durable record families:
  - `implementation_control/program_state.yaml`;
  - `implementation_control/handoffs/handoff-0001.yaml` and matching Markdown
    summaries;
  - `implementation_control/tasks/WI-YYYYMMDD-NNN/00_TASK.yaml`;
  - `implementation_control/tasks/.../jobs/WJ-...yaml`;
  - `implementation_control/tasks/.../jobs/completions/WJC-...yaml`.
- Treat existing `PRDs/` and `ImplementationPlans/` files as planning inputs
  and route context, not live-state authority.
- Add `scripts/implementation_control/continue_implementation.py` as the
  deterministic resolver. It should emit JSON by default and support
  `--summary`.
- Expose the resolver as `npm run continue:implementation`.
- Keep the resolver read-only. It resolves and reports the next packet; Codex
  performs the implementation work.
- Add `scripts/implementation_control/validate_implementation_control.py` and
  expose it as `npm run validate:implementation-control`.
- Include `validate:implementation-control` in `npm run validate` after
  existing website content/provenance checks and before `npm run build`.
- Add `scripts/implementation_control/checkpoint_implementation_transaction.py`
  as the narrow mutating endpoint for validation, allowed-path staging, and
  local commit creation.
- The checkpoint command must not push, deploy, refresh upstream, mutate
  upstream source files, or invent completion content.
- The first live task should bootstrap the control system itself. It should
  become live authority prospectively; older PRDs and implementation plans
  remain historical context.
- Approval gates should be data fields in task or job records, not only prose.
- Required validators should be explicit per job and verified by the
  implementation-control validator and checkpoint command.

## Testing Decisions

- Test the resolver's default JSON output and `--summary` output.
- Test resolver behavior for ready, blocked, human approval required, existing
  active job, and no-action boundaries.
- Test validation failures for missing program state, handoff mismatch, missing
  task/job/completion records, invalid allowed write paths, unknown validators,
  and high-risk packets without explicit approval status.
- Test checkpoint behavior for clean allowed changes, unrelated separable dirty
  files, ambiguous dirty files, missing completion records, failed validators,
  and attempts to stage outside allowed write paths.
- Keep tests in the existing Python test suite and run them with
  `python3 -m pytest`.
- Run `npm run validate:implementation-control` as a focused check.
- Run `npm run validate` for final integration because implementation-control
  validation becomes part of standard repo health.
- Do not test internal YAML parsing details beyond observable validation
  behavior and stable output contracts.

## Source Authority and Provenance

- The system depends on repository-local website instructions, especially the
  Source Authority Boundary defined by `AGENTS.md` and `CONTEXT.md`.
- The upstream AEther Flow project remains authoritative for scientific,
  mathematical, governance, and research-workflow claims.
- Website implementation-control records may cite upstream source project
  materials as read-only provenance, including program state, handoffs,
  registries, and source files.
- If a future implementation packet affects public claims or source-derived
  status, the packet must require explicit approval unless the work has already
  been pre-approved and the job records precise source/provenance duties.
- Implementation-control validation or checkpoint success must not be presented
  as scientific proof, source authority, or deployment approval.

## Out of Scope

- Copying the upstream research repo's full physics role ontology, role
  registry, DDR system, parent-child synthesis policy, or GR-routing machinery.
- Mutating `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
- Deploying to Cloudflare Pages.
- Pushing to a remote repository.
- Rewriting public pages, global navigation, shared design primitives, or
  source-derived claim content as part of the control-system bootstrap unless a
  later task explicitly authorizes that work.
- Retrofitting all older PRDs and implementation plans into completed control
  records.

## Further Notes

- The upstream `continue research` pattern supplies the control invariants:
  live state first, one bounded packet, explicit boundaries, validation, and a
  durable handoff.
- The website version should be intentionally smaller. Its core job is
  implementation continuity and safety, not scientific route selection.
- A useful future improvement will be a compact implementation dashboard page
  or report, but that is not needed for the bootstrap.
