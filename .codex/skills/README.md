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
- `agentjob-control/`: hidden website binding for the pinned portable schemas,
  durable goal state, activation receipts, fingerprints, and recovery runtime;
  it does not replace `implementation_control/`.
- `continue/`: explicitly resolve and execute zero or one existing website
  implementation-control job and emit a portable continuation result.
- `continue-goal/`: explicitly launch one finite durable goal across fresh
  Codex tasks without executing a website job in the launcher.
- `continue-implementing-goal/`: hidden token-bound worker that consumes one
  generation, invokes `continue` at most once, and terminalizes or reserves at
  most one successor.
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

The governed continuation family is experimental and explicit-invocation only.
Its exact vendor copies live under `.agents/skills/`; project adaptations live
under `.codex/skills/`, `.agents/continuation/`, and
`scripts/implementation_control/`. Mutable relay state belongs only under the
ignored `.local/sys4ai/continuation/` root. Validate installation hashes,
dependency edges, front doors, configuration, and adapter behavior with
`npm run validate:goal-relay`; run the complete portable runtime suite after
any vendor refresh.

See `THIRD_PARTY_NOTICES.md` for upstream attribution and license text.
