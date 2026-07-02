---
name: system-analysis
description: Analyze an AEther Flow system, functionality, subsystem, workflow, role, file family, or research topic from /Volumes/P-SSD/AngryOwl/The-AEther-Flow and write a grounded Markdown system analysis under docs/system-analyses/<topic-slug>.md. Use when the user asks for system analysis, functionality analysis, topic analysis, architecture explanation, subsystem explanation, or a visual Mermaid-backed explanation that preserves the website/source-authority boundary.
---

# System Analysis

## Purpose

Create website-maintained explanatory analyses for AEther Flow systems,
functionalities, workflows, roles, or topics. The output is a Markdown file in
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website/docs/system-analyses/` with an
embedded styled Mermaid diagram, source-grounded explanation, explicit
authority limits, APA-style references, and a native source-analysis quality
gate.

These analyses explain and organize upstream evidence. They do not create,
strengthen, or silently promote scientific, mathematical, governance, or
research-workflow claims.

## Required Inputs

- A topic, system, functionality, workflow, role, or file family to analyze.
- Optional target slug or output path. If omitted, derive a lowercase
  hyphen-case slug from the topic and write
  `docs/system-analyses/<topic-slug>.md`.

If the topic is too broad to analyze truthfully, narrow it to one bounded
system surface before writing. Ask one concise question only when repository
inspection cannot resolve the ambiguity.

## Required Workflow

1. Read the active repository instructions such as `AGENTS.md`.
2. Use the repo-local `mermaid-diagram-style` skill. At minimum, read its
   `SKILL.md` and `references/palette-contract.md` before writing the diagram.
3. Inspect upstream source evidence in
   `/Volumes/P-SSD/AngryOwl/The-AEther-Flow` before making source-dependent
   claims.
4. Attempt a Codex sub-agent for every non-trivial analysis when the current
   user request and available tools permit sub-agent delegation. Use a
   system-analyst role prompt. If no sub-agent tool is available or policy does
   not permit delegation, perform the same workflow in the main agent and state
   in the final response that no sub-agent was spawned.
5. Define the Mermaid diagram's visual grammar before drafting it. Decide what
   shapes, borders, arrows, edge labels, groups, and palette classes mean for
   this specific system, functionality, workflow, role, or topic.
6. Draft the analysis from repository evidence, not memory or generated
   summaries.
7. Read `references/analysis-template.md` from this skill and use its section
   order for the output file.
8. Write the Markdown file to `docs/system-analyses/<topic-slug>.md` unless the
   user provided a different path.
9. Run the native source-analysis pass/repair/block gate before finalizing.
   Repair ordinary weaknesses directly. Block instead of writing unsupported
   claims.

## Evidence Hierarchy

Use this authority order:

1. Upstream tracked source files, registries, research-control records,
   handoffs, tests, and scripts in `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
2. Website source files, manifests, dossiers, and docs in
   `/Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website`, only for website
   presentation, publication, and reader-journey context.
3. Generated wiki, HTML, Obsidian, or memory layers as orientation only. Verify
   every source-dependent claim against tracked repository files before writing.

When source authority is unclear, label the uncertainty, restrict the claim to
scaffold-level explanation, or block.

## Sub-Agent Contract

When delegation is available and allowed, spawn one Codex sub-agent with a
bounded analysis task. Do not ask the sub-agent to modify files. Ask for:

- source files inspected,
- summary of the system/functionality/topic,
- interfaces, inputs, outputs, and dependent components,
- risks, failure modes, and claim boundaries,
- Mermaid diagram concept with visual grammar,
- open questions and logical next step,
- APA-style reference candidates.

Use the sub-agent result as evidence to integrate, not as authority by itself.
The main agent remains responsible for verifying claims against source files,
writing the final Markdown, and applying the native source-analysis quality
gate.

Suggested prompt:

```text
Act as a system analyst for The AEther Flow project. Analyze <topic> using
tracked upstream evidence from /Volumes/P-SSD/AngryOwl/The-AEther-Flow. Do not
modify files. Return concise analysis notes with exact local paths reviewed,
system context, interfaces, risks, claim boundaries, a Mermaid diagram concept,
the diagram's proposed visual grammar, open questions, a logical next step, and
APA-style reference candidates. For the visual grammar, state what node shapes,
border styles, arrow styles, edge labels, groups, and palette classes should
mean in this analysis. Treat website docs and generated layers as orientation
only unless verified against tracked upstream files.
```

## Diagram Contract

Embed one Mermaid diagram directly in the analysis Markdown. Use the
`mermaid-diagram-style` palette contract: Mermaid frontmatter config,
`theme: base`, dark canvas, ivory text, Angry Owl cyan/orange semantic roles,
reusable `classDef` classes, shape plus color, and thicker arrows.

The diagram must be designed as analysis, not decoration. The system analyst
may use the Mermaid flowchart shapes, edge types, edge labels, subgraphs,
border styles, and class definitions that best encode the specific system
meaning, provided the colors stay inside the project palette. Do not force all
nodes into one shape, one border, or one arrow type when the evidence supports
meaningful distinctions.

Document non-obvious visual grammar in nearby prose, a compact legend, or
Mermaid comments. At minimum, make clear what colors/classes, shapes, dashed or
solid borders, and dashed, solid, bidirectional, or labeled arrows mean when
those distinctions carry analytical meaning. Color must never be the only
meaning carrier.

Do not create `.mmd`, PNG, or manifest files by default. If the user later asks
to promote the analysis into a public comprehension route or diagram gallery,
migrate the diagram into the existing `.mmd` plus render-manifest workflow.

## Citation Contract

Use inline parenthetical citations for source-dependent claims. Add APA
7-style entries under `## References`. For local repository files, use a
pragmatic APA-like form:

```text
The AEther Flow. (n.d.). File or document title/path. Local file:
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow/path/to/file`.
```

Also list exact inspected local paths under `## Evidence Reviewed` so
maintainers can verify the analysis quickly.

## Source-Analysis Quality Gate

Before finalizing, identify the artifact type, audience, purpose, working
thesis, evidence basis, and exclusions. Then run two checks for substantial,
public-facing, scientific, governance, or claim-bearing analyses:

- Builder pass: improve clarity, structure, specificity, examples, evidence
  traceability, limitations, and reader usefulness.
- Refuter pass: look for unsupported claims, authority drift, hidden
  uncertainty, generic prose, audience mismatch, excessive length, and review
  burden.

Classify the final artifact as:

- `pass`: specific, grounded, useful, and fit for handoff.
- `repair`: flawed but fixable from available evidence; repair before
  finalizing.
- `block`: missing source evidence, authority, thesis, or context needed for a
  truthful analysis.

Do not use numeric quality scores. Remove or mark uncertainty in claims that
cannot be verified. Block when repair would require inventing facts,
strengthening claims, guessing authority, hiding uncertainty, or pretending
evidence exists.

Surface the gate result in the final response when there was a material repair,
a block, public-facing sensitivity, scientific/governance claim sensitivity, or
source-authority risk.

## Public Page Boundary

This skill produces system-analysis Markdown only. Public page creation is no
longer routed through a separate repo-local publication skill. When an analysis
should become a public Astro route, open a fresh implementation-control packet
and use the repository's existing Astro, content-dossier, manifest, diagram,
browser-QA, and validator workflows inside that packet's allowed write scope.

## Reference Files

- `references/analysis-template.md`: required Markdown output skeleton and
  embedded Mermaid starter.
