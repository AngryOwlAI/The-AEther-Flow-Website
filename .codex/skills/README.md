# Project-Local Codex Skills

This directory contains Codex skills that are local to The AEther Flow Website
repository.

## Skills

- `system-analysis/`: analyze upstream AEther Flow systems, functionality,
  workflows, roles, or topics into source-grounded Markdown files under
  `docs/system-analyses/` with embedded Mermaid diagrams whose shapes, borders,
  arrows, colors, and labels carry explicit analytical meaning, plus explicit
  claim boundaries and a native source-analysis quality gate.
- `mermaid-diagram-style/`: create or migrate Mermaid diagrams with the
  website's Angry Owl palette, Inter font stack, dark canvas, semantic visual
  grammar, static PNG rendering workflow, and source-authority boundary.
- `push-and-deploy/`: push a clean accepted `main` commit and deploy the
  pushed commit to Cloudflare Pages using the current Direct Upload project.
- `implementation-control/`: resolve live website-local implementation-control
  records, execute at most one governed implementation packet, validate it, and
  checkpoint it locally without pushing, deploying, or mutating upstream.
- `implementation-plan-goal/`: user-facing serial plan launcher that binds a
  canonical v2 plan to exact website implementation packets and releases one
  adopted worker prompt at a time.
- `continue/`: relay-callable website continuation front door; it resolves and
  executes no more than one active website packet.
- `continue-implementing-plan-task/`: internal-only one-task worker lifecycle
  for claim, consumption, finalization, and unknown-result quarantine.
- `agentjob-control/`: internal-only support front door for the pinned SQLite
  scheduler, provider-intent, receipt, and recovery runtime.
- `technical-writing-quality-gate/`: draft, revise, or review source-grounded
  technical and public-facing prose with explicit pass, repair, or block
  outcomes plus an optional advisory standard-library warning matcher.
- `prd-to-implementation-plan/`: convert a PRD, product spec, or requirements
  document into a Codex-ready implementation plan and task packets.
- `prototype/`: build throwaway logic or UI prototypes to answer a specific
  design question before production implementation.
- `to-prd/`: synthesize the current conversation and repository evidence into a
  local product requirements document.

These skills are adapted for the website repository's source-authority boundary:
the website may explain and publish reviewed material, but it must not invent or
silently change scientific, mathematical, governance, or research-workflow
claims from the upstream source project.

Public page creation is governed through implementation-control packets and
the repository's Astro, content, manifest, diagram, and validation workflows.

See `THIRD_PARTY_NOTICES.md` for upstream attribution and license text.
