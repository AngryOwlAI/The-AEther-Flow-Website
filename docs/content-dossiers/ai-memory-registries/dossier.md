# Memory Preflight And Source-First Retrieval Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/ai-research-agent-system/memory-registries/`
- Reader job: Understand memory preflight as a source-finding step whose hits must be verified against tracked source files and registry rows.
- Primary audience: general public, AI-system developers, system engineers, and maintainers reviewing source-boundary language.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

PG-018 rewrites the existing memory route around source-first retrieval. The
page explains memory status, targeted lookup/search, canonical source
inspection, registry-row inspection, receipt evidence, and the boundary that
retrieval layers remain navigation only.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/memory-system-explainer.md` | committed generated noncanonical reader source | Memory as source-finding support and retrieval-layer boundaries. |
| `github-facing/source-authority-explainer.md` | committed generated noncanonical reader source | Authority ladder and source-first checklist. |
| `research_control/README.md` | committed control source | Memory preflight command, receipt requirement, and source-inspection rule. |
| `.agents/schemas/AGENT_JOB_SCHEMA.md` | committed schema source | `memory_preflight` receipt fields and canonical inspection requirements. |
| `registries/MARKDOWN_SOURCE_REGISTRY.csv` | committed source registry | Representative registered Markdown source lane. |
| `registries/TEX_SOURCE_REGISTRY.csv` | committed source registry | Representative registered TeX source lane. |
| `registries/WIKI_ARTIFACT_REGISTRY.csv` | committed generated derivative registry | Wiki retrieval-layer boundary. |
| `registries/CONTENT_SEMANTIC_REGISTRY.csv` | committed generated derivative registry | Semantic retrieval-layer boundary. |
| `docs/system-analyses/memory-preflight-and-source-first-retrieval.md` | website analysis | PG-018 route-specific review. |

## Source-derived topic outline

1. Memory status reports retrieval-layer freshness.
2. Targeted lookup or search finds likely source objects, paths, rows, or prior tasks.
3. Canonical source files and registry rows must be inspected before a hit can affect routing, claim language, source selection, or project-control work.
4. AgentJobs and completions that use memory preflight record status, query commands, returned IDs, canonical inspections, registries, paths, and hashes.
5. Generated wiki notes, semantic extracts, Obsidian mirrors, SQLite indexes, and `.local` caches remain retrieval layers only.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Memory preflight | Bounded status and lookup step before controlled routing or AgentJob creation. | Navigation and receipt evidence only. |
| Canonical inspection | Direct check of a tracked source file and relevant registry row. | Required before retrieval hits affect claims or routing. |
| Registry row | Tracked CSV metadata for a source, derivative, task, role, or generated output. | Does not replace reading the source it describes. |
| Retrieval layer | Wiki note, semantic extract, Obsidian mirror, SQLite index, or `.local` cache. | Never citation or claim authority. |
| Receipt | Recorded status, query, source inspection, registry, path, and hash evidence. | Operational audit record, not physics proof. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Memory hits are navigation only.
- Memory preflight does not expose or publish private memory contents.
- Generated retrieval drift requires refresh or source inspection.
- Local caches are not committed evidence.
- Source-first retrieval does not change research status or claim authority.

### Forbidden implications

- Memory overrides registered sources.
- Wiki notes promote generated derivatives.
- Local cache state can be cited as authority.
- A retrieval hit can route, summarize, or cite without canonical inspection.
- A receipt can prove a theorem, promote a claim, or bypass an AgentJob boundary.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Route opens with memory-preflight and source-first retrieval context. |
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
| Alt text | Memory status, targeted lookup, likely source object, canonical source file, source registry row, preflight receipt, retrieval layers, and retrieval-is-not-authority boundary. |
| Caption | Memory preflight can find evidence; source inspection decides whether it may be relied on. |
| Nearby prose requirement | Explain that the diagram is a static reader aid and not source authority. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Memory preflight accelerates source lookup; claim-affecting work still requires direct inspection of tracked files, registry rows, current control records, and receipt evidence.

## Unsafe summary

Unsafe summary: A memory hit, wiki note, semantic extract, Obsidian mirror, SQLite index, local cache, or receipt overrides tracked source authority or proves a claim.

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
- [x] Mobile layout and desktop layout were reviewed.
- [x] Human review note is recorded under `docs/quality/`.

## References

The AEther Flow. (2026a). *Memory, registries, wiki, and retrieval surfaces*
[`github-facing/memory-system-explainer.md`].

The AEther Flow. (2026b). *Source authority and generated derivatives*
[`github-facing/source-authority-explainer.md`].

The AEther Flow. (2026c). *Research control*
[`research_control/README.md`].

The AEther Flow. (2026d). *AgentJob schema*
[`.agents/schemas/AGENT_JOB_SCHEMA.md`].

The AEther Flow. (2026e). *Markdown source registry*
[`registries/MARKDOWN_SOURCE_REGISTRY.csv`].

The AEther Flow. (2026f). *TeX source registry*
[`registries/TEX_SOURCE_REGISTRY.csv`].

The AEther Flow. (2026g). *Wiki artifact registry*
[`registries/WIKI_ARTIFACT_REGISTRY.csv`].

The AEther Flow. (2026h). *Content semantic registry*
[`registries/CONTENT_SEMANTIC_REGISTRY.csv`].
