# Technical Requirements Content Dossier

Status: evidence-reviewed draft dossier.

## Route and reader job

- Public route: `/project/operations/technical-requirements/`
- Reader job: Understand tools as reproducibility support, not authorization.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## PG-021 route-family evidence review

- Review artifact: `docs/system-analyses/remaining-operations-route-family.md`.
- Review decision: Preserve the existing technical-requirements route and
  expose the committed environment, dependency, script, and test sources behind
  the tool-tier explanation.
- Source state: Committed upstream source at
  `01efc4f180221caf9425fbb24683eb54927b553e`.
- Boundary: Tool availability supports reproducibility; it does not authorize
  work, change dependency policy, or promote scientific claims.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/technical-requirements-explainer.md` | upstream source | Source basis for this route. |
| `README.md` | upstream project source | Source basis for local environment and command-family guidance. |
| `AGENTS.md` | upstream project source | Source basis for authority hierarchy and generated-output boundaries. |
| `research_control/README.md` | upstream control source | Source basis for memory preflight, project-system, and research-control checks. |
| `requirements.txt` | upstream dependency ledger | Source basis for Python dependency requirements. |
| `Makefile` | upstream command source | Source basis for grouped command targets. |
| `scripts/README.md` | upstream script guide | Source basis for script groups and tooling authority boundary. |
| `tests/README.md` | upstream test guide | Source basis for unit-test areas and command shape. |

## Source-derived topic outline

1. Inspection tools
2. Validation tools
3. Astro and browser QA
4. TeX and PDF derivative tools
5. Tool authority boundary

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Tool tier | Class of local capability needed for an operation. | Not permission. |
| Derivative tooling | Tools used to generate human-readable outputs. | Registered source remains authority. |
| Command evidence | Recorded command result. | Bounded to what was run. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Successful tools do not grant scope.
- The page does not change dependency policy.
- Derivative tooling does not promote sources.

### Forbidden implications

- Installed tools authorize work.
- Commands change repository policy.
- PDF tooling creates scientific authority.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with reader context and source-boundary notice. |
| Plain summary | yes | Provided in the reusable comprehension block. |
| Mechanism steps | yes | Source-derived route mechanism. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Sources listed above and rendered as provenance. |
| Boundary block | yes | Claim boundaries and forbidden implications. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | no | No equation walkthrough required for this route. |
| Safe/unsafe summary | yes | High-risk overread prevention. |
| Related internal routes | yes | Internal-first reader journey before provenance links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/operations-technical-requirements/diagrams/technical-tool-authority-tiers.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/operations-technical-tool-tiers.png` |
| Manifest id | `comprehension_operations_technical_tool_tiers` |
| Alt text | Inspect tools, validation tools, Astro and browser QA, TeX and PDF derivative tools, and tool availability is not authorization. |
| Caption | Tools make operations reproducible without deciding whether an operation is allowed. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Technical requirements identify tools needed to inspect, validate, render, or derive artifacts, while authorization remains in task and source-control records.

## Unsafe summary

Unsafe summary: Installed tools, passing commands, or local capability authorize work, change dependencies, or promote scientific claims.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/operations/technical-requirements/`.
- Reason a new route is or is not justified: The existing route is the correct public surface for this content.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [x] Mobile layout and desktop layout were reviewed for PG-021.
- [x] Human review note is recorded under `docs/quality/sitewide-revamp-pg021-remaining-operations-family-qa.md`.

## References

- AEther-Flow Project. (2026). `github-facing/technical-requirements-explainer.md`.
- AEther-Flow Project. (2026). `README.md`.
- AEther-Flow Project. (2026). `AGENTS.md`.
- AEther-Flow Project. (2026). `research_control/README.md`.
- AEther-Flow Project. (2026). `requirements.txt`.
- AEther-Flow Project. (2026). `Makefile`.
- AEther-Flow Project. (2026). `scripts/README.md`.
- AEther-Flow Project. (2026). `tests/README.md`.
