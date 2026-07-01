# Sitewide Greenfield Release-Candidate QA Report

Status: release-candidate QA green, owner review pending.
Date: 2026-06-30.
Packet: GF-014, `WI-20260630-042`.

## Conclusion

The rebuilt greenfield route set is technically present, browser-smoke
healthy, and validation-green. Deployment is not authorized until owner review
accepts the rebuilt route set and a separate deployment request is made.

Owner review remains pending for all rebuilt routes.

## Owner Review State

Owner acceptance: not granted.
Deployment readiness: technically green but not owner-accepted and not
deployment-authorized.
Feedback queue: no owner-requested changes yet. The Diagram Gallery
quality-gate contract blocker was resolved in packet `WI-20260630-043`.
Curator/source drift was resolved in packet `WI-20260630-044` by refreshing
website-side generated artifacts from clean committed upstream source commit
`2a934c29b58e84aa913a5088a8388bd259f6370b` and validating with
`AETHER_FLOW_SOURCE_ROOT` bound to that clean source view.
Owner-requested static diagram wiring was resolved in packet
`WI-20260630-045` by adding source-backed diagram blocks to 28 greenfield
routes. The optional `/license/` split-license decision map remains out of the
core release-candidate route set because no existing source-backed static
diagram asset matches that lower-priority concept.
Owner-requested diagram fit feedback was resolved in the same packet by
expanding the diagram frames to the route content width, containing oversized
vertical diagrams, adding an in-page larger-view dialog, and removing the
repeated visible post-diagram note.
Owner-requested diagram caption feedback was resolved in the same packet by
rewriting allowed greenfield/resource figure captions as descriptive figure
notes and removing visible Mermaid source paths from shared figure/gallery
rendering. Legacy `/project/*` caption wording remains a follow-up item because
those files are outside the active packet's write scope.
Owner-requested diagram caption weight feedback was resolved by rendering
diagram description captions and expanded-dialog captions as regular note text
rather than bold label text.

## Route Set For Review

All 29 rebuilt routes are `technically ready` and `human review pending` in
`docs/quality/sitewide-greenfield-review-ledger.md`.

| Family | Routes |
| --- | --- |
| Home | `/` |
| Physics Research | `/physics/`, `/physics/ontology/`, `/physics/exact-gr-benchmark/`, `/physics/derivation-roadmap/`, `/physics/flow-geometry/`, `/physics/claim-status/`, `/physics/open-burdens/` |
| AI Research System | `/ai-research-system/`, `/ai-research-system/current-state/`, `/ai-research-system/workflow/`, `/ai-research-system/agentjob-lifecycle/`, `/ai-research-system/roles-and-schemas/`, `/ai-research-system/human-gated-promotion/`, `/ai-research-system/validators-and-handoffs/`, `/ai-research-system/memory-preflight/`, `/ai-research-system/project-system-improvement/`, `/ai-research-system/runtime-requirements/` |
| Resources | `/resources/`, `/resources/source-authority/`, `/resources/registries/`, `/resources/generated-derivatives/`, `/resources/retrieval-layers/`, `/resources/publication-process/`, `/resources/library/`, `/resources/reading-paths/`, `/resources/repository-map/`, `/resources/site-builder-guide/`, `/resources/diagrams/` |

## Validation Evidence

Passed:

- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run validate:provenance`
- `npm run validate:cloudflare`
- `npm run validate:implementation-control`
- `npm run build`: 64 static pages built.
- `.venv/bin/python -m pytest`: 79 passed.
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`: 92 routes passed.
- Browser QA: Home, Physics, AI Research System, Resources, and Diagram Gallery returned HTTP 200 on desktop and mobile, exposed expected `h1` text, and showed no document-level horizontal overflow.
- `python3 scripts/quality_gate.py`: passed after `WI-20260630-043` updated the quality gate to validate `/resources/diagrams/` against the greenfield Diagram Gallery contract while keeping `/resources/documents/` on the support-page schema.
- `npm run validate`: passed after `WI-20260630-044` with
  `AETHER_FLOW_SOURCE_ROOT` bound to clean committed upstream source commit
  `2a934c29b58e84aa913a5088a8388bd259f6370b`.
- `npm run quality`: passed after `WI-20260630-044` with
  `AETHER_FLOW_SOURCE_ROOT` bound to the same clean committed source view.
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4321`: 92 routes passed after the source-derived refresh.
- `WI-20260630-045` diagram rollout: 28 changed routes rendered a
  `ComprehensionBlocks` static diagram block with manifest-backed PNG paths,
  captions, provenance, and non-authority note.
- Browser diagram QA after `WI-20260630-045`: 28 changed routes passed desktop
  and mobile checks for nonzero loaded diagram dimensions and no document-level
  horizontal overflow.
- `WI-20260630-045` diagram fit refinement: all 28 greenfield diagram routes
  passed desktop/mobile checks for full-width figure frames, contained oversized
  diagrams, absent repeated note text, no horizontal overflow, and working
  larger-view dialogs.
- `WI-20260630-045` caption reform: allowed greenfield/resource captions use
  descriptive figure-note language, shared figure/gallery rendering no longer
  displays Mermaid source paths, and remaining old warning-style phrase hits are
  limited to legacy `/project/*` surfaces outside this packet's write scope.
- `WI-20260630-045` caption weight refinement: shared diagram descriptions,
  gallery boundary notes, and expanded-dialog captions render as regular note
  text rather than bold label text.

Failed or blocked:

- Owner review has not accepted the rebuilt route set.
- Deployment has not been requested or performed.

## Browser QA Artifacts

Screenshots were captured under ignored local QA output:

- `output/playwright/gf014-home-desktop-2026-06-30.png`
- `output/playwright/gf014-physics-desktop-2026-06-30.png`
- `output/playwright/gf014-ai-research-system-desktop-2026-06-30.png`
- `output/playwright/gf014-resources-desktop-2026-06-30.png`
- `output/playwright/gf014-diagrams-desktop-2026-06-30.png`
- `output/playwright/gf014-home-mobile-2026-06-30.png`
- `output/playwright/gf014-physics-mobile-2026-06-30.png`
- `output/playwright/gf014-ai-research-system-mobile-2026-06-30.png`
- `output/playwright/gf014-resources-mobile-2026-06-30.png`
- `output/playwright/gf014-diagrams-mobile-2026-06-30.png`

## Residual Risk

- Owner review has not accepted the rebuilt route set.
- Old `/project/*` source files remain in the build for validator continuity even though the public route/provenance manifests now expose the short-route inventory.
- Some legacy `/project/*` diagram captions still use old warning-style wording;
  they were not changed because the active packet authorizes the greenfield and
  resources route scope, not legacy project-route caption rewrites.
- The default curator source root currently points at the upstream working tree;
  when that tree is dirty, validation must bind `AETHER_FLOW_SOURCE_ROOT` to a
  clean committed source view to avoid treating uncommitted upstream edits as
  release-candidate evidence.

## Recommendation

Do not deploy. Do not mark the rebuild owner-accepted.

The logical next step is owner review. The owner must either accept the rebuilt
route set or request bounded feedback packets. Deployment remains a separate
explicit request after acceptance.

## References

The AEther Flow Website. (2026). *Implementation Plan: Sitewide Greenfield
Rebuild* [Implementation plan].

The AEther Flow Website. (2026). *Sitewide Greenfield Review Ledger* [Quality
ledger].

The AEther Flow Website. (2026). *Sitewide Greenfield Rebuild Task Packets*
[Implementation task packets].
