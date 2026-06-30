# Sitewide Greenfield Review Ledger

Status: active implementation ledger.
Date: 2026-06-30.

## Purpose

This ledger tracks the greenfield rebuild route inventory, technical readiness,
source-bundle readiness, validation status, and human review status. It is a
maintainer-facing control surface, not public website copy and not source
authority.

Deployment remains blocked until the owner marks the rebuilt page set
`reviewed and accepted`.

## Status Vocabulary

| Field | Allowed values |
| --- | --- |
| Technical status | `not implemented`, `in progress`, `technically ready`, `blocked`, `retired` |
| Human review status | `not implemented`, `human review pending`, `reviewed with changes requested`, `reviewed and accepted` |
| Source-bundle status | `not started`, `drafted`, `verified`, `not required`, `blocked` |

## Route Inventory

| Order | Route | Page | Family | Task | Technical status | Human review status | Source-bundle status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `/` | Home | Home | GF-002 | technically ready | human review pending | verified | GF-002 rebuilt Home and primary navigation; linked category routes remain pending in later packets. |
| 2 | `/physics/` | Physics Overview | Physics Research | GF-003 | technically ready | human review pending | verified | GF-003 implemented the category landing page; linked remaining Physics child routes stay pending in later packets. |
| 3 | `/physics/ontology/` | Ontology | Physics Research | GF-003 | technically ready | human review pending | verified | GF-003 defines ontology terms near use and keeps proof-boundary language visible. |
| 4 | `/physics/exact-gr-benchmark/` | Exact-GR Benchmark | Physics Research | GF-004 | technically ready | human review pending | verified | GF-004 distinguishes benchmark adoption, compatibility, derivation, and promotion. |
| 5 | `/physics/derivation-roadmap/` | Derivation Roadmap | Physics Research | GF-004 | technically ready | human review pending | verified | GF-004 names open burdens without implying completed GR derivation. |
| 6 | `/physics/flow-geometry/` | Flow Geometry | Physics Research | GF-004 | technically ready | human review pending | verified | GF-004 implements a visual and tabular dictionary with assumptions and limits. |
| 7 | `/physics/claim-status/` | Physics Claim Status | Physics Research | GF-005 | not implemented | not implemented | not started | Must keep claim status and gate boundaries visible. |
| 8 | `/physics/open-burdens/` | Open Burdens | Physics Research | GF-005 | not implemented | not implemented | not started | Must preserve blocked and open-burden language. |
| 9 | `/ai-research-system/` | AI Research System Overview | AI Research System | GF-006 | not implemented | not implemented | not started | New category landing page. |
| 10 | `/ai-research-system/current-state/` | Current State | AI Research System | GF-006 | not implemented | not implemented | not started | Source freshness-sensitive; refresh requires authorization. |
| 11 | `/ai-research-system/workflow/` | Research-Agent Workflow | AI Research System | GF-007 | not implemented | not implemented | not started | Must keep AgentJob and authority boundaries explicit. |
| 12 | `/ai-research-system/agentjob-lifecycle/` | AgentJob Lifecycle | AI Research System | GF-007 | not implemented | not implemented | not started | Must explain lifecycle without expanding permissions. |
| 13 | `/ai-research-system/roles-and-schemas/` | Roles and Schemas | AI Research System | GF-008 | not implemented | not implemented | not started | Must distinguish role labels from live authority. |
| 14 | `/ai-research-system/human-gated-promotion/` | Human-Gated Promotion | AI Research System | GF-008 | not implemented | not implemented | not started | Must keep human-gate decisions protected. |
| 15 | `/ai-research-system/validators-and-handoffs/` | Validators and Handoffs | AI Research System | GF-008 | not implemented | not implemented | not started | Must state validator PASS is bounded. |
| 16 | `/ai-research-system/memory-preflight/` | Memory Preflight | AI Research System | GF-009 | not implemented | not implemented | not started | Memory and retrieval do not replace source inspection. |
| 17 | `/ai-research-system/project-system-improvement/` | Project-System Improvement | AI Research System | GF-009 | not implemented | not implemented | not started | Improvement loop must stay distinct from source authority. |
| 18 | `/ai-research-system/runtime-requirements/` | Runtime Requirements | AI Research System | GF-009 | not implemented | not implemented | not started | Must describe runtime evidence conservatively. |
| 19 | `/resources/` | Resources Overview | Resources | GF-010 | not implemented | not implemented | not started | Existing route is legacy evidence until GF-010 replaces it. |
| 20 | `/resources/source-authority/` | Source Authority | Resources | GF-010 | not implemented | not implemented | not started | Contextual authority page; resource pages must avoid banned dedicated section where applicable. |
| 21 | `/resources/registries/` | Registry Explorer | Resources | GF-010 | not implemented | not implemented | not started | Registries are evidence surfaces, not proof. |
| 22 | `/resources/generated-derivatives/` | Generated Derivatives | Resources | GF-011 | not implemented | not implemented | not started | Must distinguish derivative access from authority. |
| 23 | `/resources/retrieval-layers/` | Local Retrieval Layers | Resources | GF-011 | not implemented | not implemented | not started | Must preserve local retrieval boundary. |
| 24 | `/resources/publication-process/` | Publication Process | Resources | GF-011 | not implemented | not implemented | not started | Must preserve publication and provenance gates. |
| 25 | `/resources/library/` | Library | Resources | GF-011 | not implemented | not implemented | not started | Library/resource pages must not render a dedicated Source authority section. |
| 26 | `/resources/reading-paths/` | Reading Paths | Resources | GF-012 | not implemented | not implemented | not started | Internal-first routes must be primary. |
| 27 | `/resources/repository-map/` | Repository Map | Resources | GF-012 | not implemented | not implemented | not started | Must avoid exposing local-only paths as public authority. |
| 28 | `/resources/site-builder-guide/` | Site Builder Guide | Resources | GF-012 | not implemented | not implemented | not started | Must cite the source-bundle and page-contract rules. |
| 29 | `/resources/diagrams/` | Diagram Gallery | Resources | GF-012 | not implemented | not implemented | not started | Existing route is legacy evidence until GF-012 resets inventory. |

## Packet Ledger

| Packet | Scope | Status | Validation summary | Next action |
| --- | --- | --- | --- | --- |
| GF-000 | Open fresh greenfield control packet. | completed | `git diff --check`, `npm run validate:implementation-control`, and `.venv/bin/python -m pytest` passed in packet `WI-20260630-028`. | GF-001 foundation contract and review ledger. |
| GF-001 | Foundation contract and route review ledger. | completed | `git diff --check`, `npm run validate:implementation-control`, and `.venv/bin/python -m pytest` passed in packet `WI-20260630-029`. | GF-002 Home and primary navigation slice. |
| GF-002 | Home route and primary navigation slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:implementation-control`, `npm run build`, `.venv/bin/python -m pytest`, `npm run validate:svg`, and desktop/mobile browser QA passed in packet `WI-20260630-030`. | GF-003 Physics overview and ontology slice. |
| GF-003 | Physics overview and ontology slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-031`. | GF-004 Physics benchmark, roadmap, and flow geometry slice. |
| GF-004 | Physics benchmark, roadmap, and flow geometry slice. | completed | `git diff --check`, `npm run validate:content`, `npm run validate:links`, `npm run validate:layout`, `npm run validate:comprehension`, `npm run validate:provenance`, `npm run validate:manifests`, `npm run validate:svg`, `npm run build`, `npm run validate:implementation-control`, `.venv/bin/python -m pytest`, manual control-record inspection, and desktop/mobile browser QA passed in packet `WI-20260630-032`. | GF-005 Physics claim status and open burdens slice. |

## Review Rules

- Mark a route `technically ready` only after its packet passes the required
  validators and browser QA for the affected route.
- Mark a route `human review pending` only when it is technically ready for
  owner review.
- Mark a route `reviewed and accepted` only after owner review.
- Use `reviewed with changes requested` when owner review asks for changes.
- Keep deployment blocked until the rebuilt page set is accepted.
- Record skipped validators with concrete reasons in the packet closeout.

## References

The AEther Flow Website. (2026). *Sitewide Greenfield Rebuild* [Product
requirements document].

The AEther Flow Website. (2026). *Implementation Plan: Sitewide Greenfield
Rebuild* [Implementation plan].

The AEther Flow Website. (2026). *Public Comprehension Review Standard*
[Quality standard].
