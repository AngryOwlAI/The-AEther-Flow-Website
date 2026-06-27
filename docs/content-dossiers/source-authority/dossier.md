# Source Authority Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/source-authority/`
- Reader job: Understand which source lane owns which claim and how generated derivatives relate.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/source-authority-explainer.md` | upstream source | Source basis for this route. |
| `registries/PUBLICATION_BRIEF_REGISTRY.csv` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Authority ladder
2. Source-to-derivative boundary
3. Source-first checklist
4. Failure modes
5. Safe and unsafe source reading

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Source authority | Upstream file, registry, or governed record that owns claim status. | Not replaced by page clarity. |
| Derivative | Generated or reader-facing surface derived from source material. | Useful for orientation, not override. |
| Claim boundary | Control statement limiting what a result may imply. | Cannot be broadened by summary. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Website pages are maps.
- Derivative quality is downstream.
- Source wins on conflict.

### Forbidden implications

- Generated explainers promote claims.
- Website pages replace registries.
- Validator PASS becomes source authority.

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
| Mermaid source | `docs/content-dossiers/source-authority/diagrams/source-authority-ladder.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/source-authority-ladder.png` |
| Manifest id | `comprehension_source_authority_ladder` |
| Alt text | Registered TeX and source files upstream from registries, generated derivatives, website pages, reader orientation, and source wins on conflict. |
| Caption | Generated and website surfaces remain downstream from registered source authority. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Use website and generated pages to find the right source lane, then rely on registered source files, registries, and governed records for claim status.

## Unsafe summary

Unsafe summary: A generated explainer, public page, diagram, PDF, memory hit, or validator PASS replaces source authority or promotes a claim.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/source-authority/`.
- Reason a new route is or is not justified: The existing route is the correct public surface for this content.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [ ] Mobile layout and desktop layout were reviewed.
- [ ] Human review note is recorded under `docs/quality/`.

## References

- AEther-Flow Project. (2026). `github-facing/source-authority-explainer.md`.
- AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv`.
