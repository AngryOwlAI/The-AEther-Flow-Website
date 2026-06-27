# Memory And Registries Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/ai-research-agent-system/memory-registries/`
- Reader job: Use memory and registry surfaces as source-finding support, not claim authority.
- Primary audience: public readers and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The current page is an implemented reader-facing route. This dossier records the public-comprehension contract used to add diagram-backed explanation, glossary terms, boundaries, safe/unsafe summaries, source basis, and internal-first related routes.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/memory-system-explainer.md` | upstream source | Source basis for this route. |
| `github-facing/source-authority-explainer.md` | upstream source | Source basis for this route. |
| `registries/MARKDOWN_SOURCE_REGISTRY.csv` | upstream source | Source basis for this route. |
| `registries/WIKI_ARTIFACT_REGISTRY.csv` | upstream source | Source basis for this route. |
| `registries/CONTENT_SEMANTIC_REGISTRY.csv` | upstream source | Source basis for this route. |

## Source-derived topic outline

1. Authority and retrieval layers
2. Query workflow
3. Freshness warnings
4. Source inspection requirement
5. Receipt evidence when memory affects work

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Registry | Tracked CSV source for project metadata. | Limited by schema and row state. |
| Wiki note | Generated retrieval surface. | Source wins on conflict. |
| Local cache | Convenience state for speed. | Never citation authority. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Memory hits are navigation only.
- Generated retrieval drift requires refresh or source inspection.
- Local caches are not committed evidence.

### Forbidden implications

- Memory overrides registered sources.
- Wiki notes promote generated derivatives.
- Local cache state can be cited as authority.

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
| Mermaid source | `docs/content-dossiers/ai-memory-registries/diagrams/source-first-memory-layers.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/ai-memory-source-first-layers.png` |
| Manifest id | `comprehension_ai_memory_source_first_layers` |
| Alt text | Canonical source files and registries upstream from memory, wiki, semantic extracts, inspection, receipts, and retrieval-is-not-authority boundary. |
| Caption | Retrieval layers point back to source authority rather than replacing it. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Memory and registries make source lookup faster; claim-affecting work still requires direct inspection of tracked files, registry rows, and current control records.

## Unsafe summary

Unsafe summary: A memory hit, wiki note, semantic extract, Obsidian mirror, SQLite index, or local cache overrides tracked source authority.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/ai-research-agent-system/memory-registries/`.
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

- AEther-Flow Project. (2026). `github-facing/memory-system-explainer.md`.
- AEther-Flow Project. (2026). `github-facing/source-authority-explainer.md`.
- AEther-Flow Project. (2026). `registries/MARKDOWN_SOURCE_REGISTRY.csv`.
- AEther-Flow Project. (2026). `registries/WIKI_ARTIFACT_REGISTRY.csv`.
- AEther-Flow Project. (2026). `registries/CONTENT_SEMANTIC_REGISTRY.csv`.
