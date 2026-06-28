# QA-001 Final Sitewide Revamp QA

Status: ready for human review; not ready for release until named blockers are
resolved.
Date: 2026-06-28.

## Scope

QA-001 covers the sitewide revamp branch after FND-001, FND-002, PG-001
through PG-026, RT-001, and the final representative browser sweep.

No deployment was performed.

## Route Coverage

Route coverage audit:

- Built static routes in `dist/`: 38.
- `page_route_map.json` route entries: 38.
- `page_provenance.json` page entries: 38.
- Missing route-map entries from `dist/`: none.
- Extra built routes outside route map: none.
- Route-map/provenance symmetric difference: none.

Retired prototype routes:

- `/research/map/`
- `/research/equations/`
- `/research/math-sample/`

Replacement routes:

- `/project/source-authority/publication-and-provenance-system/`
- `/resources/documents/`

## Validation

Passed directly:

- `npm run validate:manifests`
- `npm run validate:content`
- `npm run validate:links`
- `npm run validate:layout`
- `npm run validate:svg`
- `npm run validate:provenance`
- `npm run validate:cloudflare`
- `npm run build`
- `python3 scripts/quality_gate.py`
- `python3 scripts/smoke_test_site.py --base-url http://127.0.0.1:4322 --root .`
- `python3 scripts/run_curator.py --write`
- `/tmp/aether-flow-website-pytest-venv/bin/python -m pytest`

Python test result:

- 46 tests passed.
- A temporary venv outside the repository was used because system Python did
  not have `pytest` installed.

Aggregate command behavior:

- `npm run validate` fails at `npm run validate:curator` after all earlier
  validation steps pass.
- `npm run quality` fails for the same reason before it can invoke
  `python3 scripts/quality_gate.py`.
- Standalone `python3 scripts/quality_gate.py` passes after the build.

Known curator blocker:

- `npm run validate:curator` fails only on the known 16 ontology TeX/PDF
  critical source-drift records:
  - `ontology/pdfs/aether_flow_consistency.pdf`
  - `ontology/pdfs/aether_flow_dynamics.pdf`
  - `ontology/pdfs/aether_flow_exact_closure_flagship_article.pdf`
  - `ontology/pdfs/aether_flow_exact_closure_note.pdf`
  - `ontology/pdfs/aether_flow_exact_closure_sequence_overview.pdf`
  - `ontology/pdfs/aether_flow_foundations.pdf`
  - `ontology/pdfs/aether_flow_geometry.pdf`
  - `ontology/pdfs/aether_flow_relativistic_recovery.pdf`
  - `ontology/tex/aether_flow_consistency.tex`
  - `ontology/tex/aether_flow_dynamics.tex`
  - `ontology/tex/aether_flow_exact_closure_flagship_article.tex`
  - `ontology/tex/aether_flow_exact_closure_note.tex`
  - `ontology/tex/aether_flow_exact_closure_sequence_overview.tex`
  - `ontology/tex/aether_flow_foundations.tex`
  - `ontology/tex/aether_flow_geometry.tex`
  - `ontology/tex/aether_flow_relativistic_recovery.tex`

## Browser QA

Representative routes checked on desktop and mobile:

- `/`
- `/project/overview/`
- `/project/physics/`
- `/project/physics/current-state/`
- `/project/physics/distance-to-gr/`
- `/project/ai-research-agent-system/`
- `/project/operations/`
- `/project/source-authority/`
- `/resources/`
- `/resources/documents/`
- `/resources/guided-starts/`
- `/resources/reviewer-packet/`

Representative screenshot pattern:

- `output/playwright/sitewide-revamp-qa001-<route-slug>-desktop-2026-06-28.png`
- `output/playwright/sitewide-revamp-qa001-<route-slug>-mobile-2026-06-28.png`

Browser metrics:

- Every checked route had exactly one H1.
- Every checked route loaded all images.
- Every checked route showed a source notice.
- Every checked route had `body.scrollWidth` equal to viewport width.
- `/project/overview/` mobile reported SVG child geometry outside the viewport,
  but page body width matched viewport width; this was treated as SVG-internal
  geometry rather than page horizontal overflow.

## Human Review Status

Human review remains pending for high-risk pages where required, especially:

- current physics state;
- Distance-to-GR;
- claim-boundary explorer;
- specialist guided starts;
- external reviewer packet;
- ontology document source-drift decisions.

The branch is ready for human review and a separate deployment decision after
the ontology source-drift blocker is resolved or explicitly accepted by the
maintainer.

## No-Deploy Boundary

No push or deployment was performed in QA-001.

## References

The AEther Flow Website. (2026). `ImplementationPlans/sitewide_page_revamp_task_packets.md`.

The AEther Flow Website. (2026). `docs/architecture/website-feature-and-functionality.md`.

The AEther Flow Website. (2026). `public/files/manifests/page_route_map.json`.

The AEther Flow Website. (2026). `public/files/manifests/page_provenance.json`.

The AEther Flow Website. (2026). `curator/reports/latest.md`.
