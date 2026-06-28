# Project-Local Codex Skills

This directory contains Codex skills that are local to The AEther Flow Website
repository.

## Skills

- `project-explainer-frontend/`: build AEther-aware informational frontend
  plans and audits from website and upstream source evidence while preserving
  the source-authority boundary.
- `system-analysis/`: analyze upstream AEther Flow systems, functionality,
  workflows, roles, or topics into source-grounded Markdown files under
  `docs/system-analyses/` with embedded Mermaid diagrams whose shapes, borders,
  arrows, colors, and labels carry explicit analytical meaning, plus explicit
  claim boundaries.
- `to-web-page/`: turn one completed system-analysis artifact into one
  integrated public explainer route with dossier, manifests, optional static
  diagram, validation, and no-ai-slop gates.
- `mermaid-diagram-style/`: create or migrate Mermaid diagrams with the
  website's Angry Owl palette, Inter font stack, dark canvas, semantic visual
  grammar, static PNG rendering workflow, and source-authority boundary.
- `no-ai-slop/`: apply a pass/repair/block quality gate so substantial
  AI-assisted artifacts stay specific, evidenced, audience-fit, and useful.
- `push-and-deploy/`: push a clean accepted `main` commit and deploy the
  pushed commit to Cloudflare Pages using the current Direct Upload project.
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

See `THIRD_PARTY_NOTICES.md` for upstream attribution and license text.
