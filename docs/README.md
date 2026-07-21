# Documentation Index

Status: maintainer-facing repository documentation.

This directory contains operating notes for maintaining The AEther Flow Website.
It is separate from the public reader-facing website navigation.

## Core Documents

- [Project Features And Functionality](project-features-and-functionality.md):
  concise operating map for routes, manifests, validators, assets, deployment,
  repo-local skills, and maintenance checks.
- [Cloudflare Pages Deployment](deployment/cloudflare-pages.md): production
  deployment model, Direct Upload constraints, and Wrangler commands.
- [Documents Navigation Implementation Plan](../ImplementationPlans/aether-flow-documents-navigation-implementation-plan.md):
  human-readable architecture, migration, validation, and release-boundary plan.
- [Accepted Documents Plan (canonical JSON)](../ImplementationPlans/aether-flow-documents-navigation-implementation-plan.canonical.json):
  hash-bound plan and task identities used by the governed relay.
- [Phase 7 Quality Gate](quality/phase7-quality-gate.md): local and runtime
  quality-gate expectations.
- [Physics Current State And Curator Final QA](quality/physics-current-state-curator-final-qa.md):
  final QA note for the current-state page and curator workflow.
- [Dual Project Public Overview Phase 0 Audit](quality/dual-project-public-overview-phase0-audit.md):
  earlier audit evidence for the public overview route.

## Operating Rule

Public website routes explain the project to readers. Repository docs explain
how maintainers keep that website accurate, source-boundary-safe, and
deployable. `/documents/` is the canonical documentation hub; `/resources/.../`
exists only for semantic compatibility redirects. Plan acceptance or local
validation does not authorize commit, push, or deployment, which remain
separate recorded actions under live implementation control.
