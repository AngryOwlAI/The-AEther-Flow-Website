export type SiteNavigationChild = {
  title: string;
  href: string;
  description: string;
};

export type SiteNavigationLink = {
  title: string;
  href: string;
  matchPrefixes?: string[];
  children?: SiteNavigationChild[];
};

export const overviewPillars = [
  {
    title: "Public explanation",
    body: "The website explains the project in reader-facing language while keeping scientific authority upstream.",
  },
  {
    title: "Technical resources",
    body: "Equations, diagrams, PDFs, and TeX files can be published as static assets with explicit provenance.",
  },
  {
    title: "Governed publication",
    body: "Claim status and source references make the boundary between presentation and authority visible to readers.",
  },
];

export type DiagramGalleryGroupId =
  | "physics"
  | "ai-workflow"
  | "operations"
  | "source-authority";

export const diagramConceptGroups: Array<{
  id: DiagramGalleryGroupId;
  title: string;
  body: string;
}> = [
  {
    id: "physics",
    title: "Physics concepts",
    body:
      "Visual aids for ontology, benchmark status, derivation burdens, route freezes, and claim gates.",
  },
  {
    id: "ai-workflow",
    title: "AI workflow concepts",
    body:
      "Visual aids for bounded AgentJobs, roles, memory, parent-child synthesis, and task authority.",
  },
  {
    id: "operations",
    title: "Operations concepts",
    body:
      "Visual aids for routing, validation, publication, project-system improvement, and tool boundaries.",
  },
  {
    id: "source-authority",
    title: "Source authority concepts",
    body:
      "Visual aids for source boundaries, manifests, reader routes, and diagram-publication status.",
  },
];

export const diagramGalleryItems = [
  {
    group: "source-authority",
    title: "Home two-track map",
    src: "/assets/diagrams/comprehension/project-overview-two-track-map.png",
    alt: "Diagram showing The AEther Flow Home page as physics research and AI research-agent workflow downstream from source authority.",
    caption:
      "Public comprehension diagram for the Home route; it orients readers without promoting scientific claims.",
    provenance:
      "Mermaid source: docs/content-dossiers/project-overview/diagrams/two-track-project-map.mmd.",
  },
  {
    group: "physics",
    title: "Physics track status map",
    src: "/assets/diagrams/comprehension/physics-track-status-map.png",
    alt:
      "Diagram showing physics research status layers as ontology, benchmark, derivation burden, claim gates, and source authority boundaries.",
    caption:
      "Public comprehension diagram for the physics track; it separates status layers without promoting claims.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-track/diagrams/status-layer-map.mmd.",
  },
  {
    group: "physics",
    title: "Ontology boundary map",
    src: "/assets/diagrams/comprehension/physics-ontology-boundary-map.png",
    alt:
      "Diagram showing ontology vocabulary, mathematical bridge work, exact-GR benchmark status, and empirical prediction as separate zones.",
    caption:
      "Public comprehension diagram for the ontology route; vocabulary orientation is not a completed derivation.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-ontology/diagrams/ontology-boundary-map.mmd.",
  },
  {
    group: "physics",
    title: "Exact-GR benchmark boundary ladder",
    src: "/assets/diagrams/comprehension/physics-benchmark-boundary-ladder.png",
    alt:
      "Diagram showing exact-GR benchmark compatibility below first-principles derivation and downstream promotion burdens.",
    caption:
      "Public comprehension diagram for the exact-GR benchmark route; benchmark compatibility remains below derivation proof.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-exact-gr-benchmark/diagrams/benchmark-boundary-ladder.mmd.",
  },
  {
    group: "physics",
    title: "Physics derivation burden ladder",
    src: "/assets/diagrams/comprehension/physics-roadmap-burden-ladder.png",
    alt: "Diagram showing the GR derivation roadmap as separate source, metric, matter-coupling, equation, and promotion burdens.",
    caption:
      "Public comprehension diagram for the GR derivation roadmap; it names burdens rather than discharging them.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-gr-derivation-roadmap/diagrams/burden-ladder.mmd.",
  },
  {
    group: "physics",
    title: "Claim gates lifecycle",
    src: "/assets/diagrams/comprehension/physics-claim-gates-lifecycle.png",
    alt:
      "Diagram showing claim gates, obstructions, freeze discipline, and gate boundaries as a lifecycle.",
    caption:
      "Public comprehension diagram for claim gates; gate structure does not itself approve a claim.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-claim-gates/diagrams/claim-gates-lifecycle.mmd.",
  },
  {
    group: "physics",
    title: "Source extension pipeline",
    src: "/assets/diagrams/comprehension/physics-source-extension-pipeline.png",
    alt:
      "Diagram showing proposal-only source extension through audit, stress, selector, and human-gated adoption boundaries.",
    caption:
      "Public comprehension diagram for source extension; proposal and audit stages do not become adoption.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-source-extension-pipeline/diagrams/source-extension-pipeline.mmd.",
  },
  {
    group: "physics",
    title: "Gate Chair and human gates",
    src: "/assets/diagrams/comprehension/physics-gate-chair-human-gates.png",
    alt:
      "Diagram showing Gate Chair status, human-gated decisions, protected approvals, and validator limits.",
    caption:
      "Public comprehension diagram for human gates; protected decisions remain outside validator authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-gate-chair-and-human-gates/diagrams/human-gate-authority.mmd.",
  },
  {
    group: "physics",
    title: "Current-state snapshot boundary",
    src: "/assets/diagrams/comprehension/physics-current-state-snapshot-boundary.png",
    alt:
      "Diagram showing current physics state as a snapshot with active task, handoff, open burden, blocked claims, and next action.",
    caption:
      "Public comprehension diagram for current state; a snapshot reports status without closing the burden.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-current-state/diagrams/snapshot-boundary.mmd.",
  },
  {
    group: "physics",
    title: "Distance-to-GR dashboard boundary",
    src: "/assets/diagrams/comprehension/physics-distance-to-gr-dashboard.png",
    alt:
      "Diagram showing a distance-to-GR dashboard with ledger inputs, burden labels, blockers, and no progress-bar proof.",
    caption:
      "Public comprehension diagram for the distance-to-GR dashboard; burden visualization is not derivation progress.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-distance-to-gr/diagrams/distance-dashboard-boundary.mmd.",
  },
  {
    group: "ai-workflow",
    title: "AI system task authority map",
    src: "/assets/diagrams/comprehension/ai-system-task-authority-map.png",
    alt:
      "Diagram showing request classification, source authority, task records, AgentJobs, validators, and bounded outputs.",
    caption:
      "Public comprehension diagram for the AI system; task authority remains record-bound.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-research-agent-system/diagrams/task-authority-review-map.mmd.",
  },
  {
    group: "ai-workflow",
    title: "AI workflow bounded AgentJob chain",
    src: "/assets/diagrams/comprehension/ai-workflow-bounded-agentjob-chain.png",
    alt: "Diagram showing a request flowing through Director decision, AgentJob allowlist, execution, validators, completion, handoff, and bounded PASS.",
    caption:
      "Public comprehension diagram for the workflow route; PASS remains bounded to the checked state.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-workflow/diagrams/bounded-agentjob-chain.mmd.",
  },
  {
    group: "ai-workflow",
    title: "One bounded AgentJob envelope",
    src: "/assets/diagrams/comprehension/ai-one-bounded-agentjob-envelope.png",
    alt:
      "Diagram showing one AgentJob envelope containing allowed reads, writes, outputs, validators, forbidden paths, and stop conditions.",
    caption:
      "Public comprehension diagram for one bounded AgentJob; the envelope does not authorize adjacent work.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-one-bounded-agentjob/diagrams/one-agentjob-envelope.mmd.",
  },
  {
    group: "ai-workflow",
    title: "AI roles authority stack",
    src: "/assets/diagrams/comprehension/ai-roles-authority-stack.png",
    alt:
      "Diagram showing role labels below registry status, execution records, AgentJob allowlists, and validators.",
    caption:
      "Public comprehension diagram for roles and skills; role labels are not live permission.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-roles-and-skills/diagrams/role-authority-stack.mmd.",
  },
  {
    group: "ai-workflow",
    title: "Role authority inspector",
    src: "/assets/diagrams/comprehension/ai-role-authority-inspector-stack.png",
    alt:
      "Diagram showing role name, registry row, role contract, execution-role record, AgentJob, validators, and current authority boundary.",
    caption:
      "Public comprehension diagram for role authority inspection; current authority requires task-local records.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-role-authority-inspector/diagrams/role-authority-inspection-stack.mmd.",
  },
  {
    group: "ai-workflow",
    title: "Memory source-first layers",
    src: "/assets/diagrams/comprehension/ai-memory-source-first-layers.png",
    alt:
      "Diagram showing canonical sources above registries, handoffs, generated memory layers, retrieval, and source-first verification.",
    caption:
      "Public comprehension diagram for memory preflight; retrieval helps locate sources without replacing them.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-memory-registries/diagrams/source-first-memory-layers.mmd.",
  },
  {
    group: "ai-workflow",
    title: "Parent-child synthesis frame",
    src: "/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png",
    alt:
      "Diagram showing parent-child synthesis inside one outer AgentJob with one allowlist, one completion, and one fused output.",
    caption:
      "Public comprehension diagram for parent-child synthesis; parallel perspectives do not create parallel authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/parent-child-synthesis/diagrams/single-outer-agentjob-frame.mmd.",
  },
  {
    group: "operations",
    title: "Operations control spine",
    src: "/assets/diagrams/comprehension/operations-control-spine.png",
    alt:
      "Diagram showing request, Director decision, AgentJob, execution role, validators, completion, handoff, and no physics proof boundary.",
    caption:
      "Public comprehension diagram for operations; operational evidence is not scientific proof.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations/diagrams/operations-control-spine.mmd.",
  },
  {
    group: "operations",
    title: "Director and AgentJob record chain",
    src: "/assets/diagrams/comprehension/operations-director-agentjob-record-chain.png",
    alt:
      "Diagram showing task row, Director decision, AgentJob, execution-role evidence, command evidence, completion, and handoff.",
    caption:
      "Public comprehension diagram for the lifecycle route; each record narrows one transaction.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-director-agentjob-lifecycle/diagrams/director-agentjob-record-chain.mmd.",
  },
  {
    group: "operations",
    title: "Role routing allowlist stack",
    src: "/assets/diagrams/comprehension/operations-role-routing-allowlist-stack.png",
    alt:
      "Diagram showing registered role, task overlay or provisional role, execution-role record, AgentJob allowlist, outputs, and validators.",
    caption:
      "Public comprehension diagram for role routing; current authority lives in the job-specific allowlist.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-role-routing/diagrams/role-routing-allowlist-stack.mmd.",
  },
  {
    group: "operations",
    title: "Validator PASS boundary",
    src: "/assets/diagrams/comprehension/operations-validator-pass-boundary.png",
    alt:
      "Diagram showing changed surface, focused check, command or screenshot receipt, PASS for checked state, and no claim promotion.",
    caption:
      "Public comprehension diagram for validator PASS; passing checks remain checked-state evidence.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-validator-operator-workflow/diagrams/validator-pass-boundary.mmd.",
  },
  {
    group: "operations",
    title: "Publication review flow",
    src: "/assets/diagrams/comprehension/operations-publication-review-flow.png",
    alt:
      "Diagram showing publication brief, source spec, reader page, screenshots, human review, and manifests.",
    caption:
      "Public comprehension diagram for publication; readability remains downstream from source authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-publication-process/diagrams/publication-source-review-flow.mmd.",
  },
  {
    group: "operations",
    title: "Project-system improvement loop",
    src: "/assets/diagrams/comprehension/operations-project-system-improvement-loop.png",
    alt:
      "Diagram showing observed issue, classifier, resolver, sidecar input, one AgentJob, receipts, and close/defer/reject outcome.",
    caption:
      "Public comprehension diagram for project-system improvement; repairs stay one bounded maintenance packet.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-project-system-improvement/diagrams/project-system-improvement-loop.mmd.",
  },
  {
    group: "operations",
    title: "Technical tool authority tiers",
    src: "/assets/diagrams/comprehension/operations-technical-tool-tiers.png",
    alt:
      "Diagram showing inspection tools, validation tools, Astro browser QA, TeX/PDF tools, and tool availability boundary.",
    caption:
      "Public comprehension diagram for technical requirements; tool capability is not authorization.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-technical-requirements/diagrams/technical-tool-authority-tiers.mmd.",
  },
  {
    group: "source-authority",
    title: "Source authority ladder",
    src: "/assets/diagrams/comprehension/source-authority-ladder.png",
    alt: "Diagram showing source files and registries upstream from generated derivatives, website pages, and reader orientation.",
    caption:
      "Public comprehension diagram for the source-authority route; if derivatives and sources conflict, source records win.",
    provenance:
      "Mermaid source: docs/content-dossiers/source-authority/diagrams/source-authority-ladder.mmd.",
  },
  {
    group: "source-authority",
    title: "Claim boundary explorer",
    src: "/assets/diagrams/comprehension/source-authority-claim-boundary-explorer.png",
    alt: "Diagram showing the claim-boundary registry feeding a checked-in snapshot and public explorer while forbidden overreads remain blocked.",
    caption:
      "Public comprehension diagram for the claim-boundary explorer route; registry language remains upstream authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/source-authority-claim-boundary-explorer/diagrams/claim-boundary-explorer.mmd.",
  },
  {
    group: "source-authority",
    title: "Publication provenance system",
    src: "/assets/diagrams/comprehension/source-authority-publication-provenance-system.png",
    alt:
      "Diagram showing source basis feeding page route map, page provenance, source manifest, asset manifest, static build, internal reader routes, provenance links, and a publication-is-not-source-truth boundary.",
    caption:
      "Public comprehension diagram for the publication provenance system; manifest evidence makes publication auditable without creating source truth.",
    provenance:
      "Mermaid source: docs/content-dossiers/source-authority-publication-and-provenance-system/diagrams/publication-provenance-system.mmd.",
  },
  {
    group: "source-authority",
    title: "General-public guided start",
    src: "/assets/diagrams/comprehension/general-public-guided-start.png",
    alt: "Diagram showing a general-public reader moving through Home, current state, source authority, claim boundaries, and provenance without creating new claims.",
    caption:
      "Public comprehension diagram for the general-public guided start; it assembles existing sourced pages without adding claims.",
    provenance:
      "Mermaid source: docs/content-dossiers/guided-start-general-public/diagrams/general-public-guided-start.mmd.",
  },
  {
    group: "source-authority",
    title: "Specialist guided starts",
    src: "/assets/diagrams/comprehension/specialist-guided-starts.png",
    alt:
      "Diagram showing a specialist guided-start hub routing physicists, mathematicians, AI and agent researchers, software and system engineers, and external reviewers to internal prerequisite pages while preserving the no-new-claims boundary.",
    caption:
      "Public comprehension diagram for specialist guided starts; audience paths route readers without creating source authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/guided-start-specialists/diagrams/specialist-guided-starts.mmd.",
  },
  {
    group: "source-authority",
    title: "Reviewer inspection order",
    src: "/assets/diagrams/comprehension/reviewer-inspection-order.png",
    alt:
      "Diagram showing the reviewer packet moving from claim boundaries to current state, Distance-to-GR, ontology documents, source inspection, reviewer questions, human review pending, and no-completed-derivation boundary.",
    caption:
      "Public comprehension diagram for the reviewer packet; claim boundaries come before source inspection.",
    provenance:
      "Mermaid source: docs/content-dossiers/reviewer-packet/diagrams/reviewer-inspection-order.mmd.",
  },
  {
    group: "physics",
    title: "Metric response ladder",
    src: "/assets/diagrams/comprehension/physics-metric-response-ladder.png",
    alt: "Diagram showing Resp_lc, M_src, MetricData(E), scoped g_eff, matter coupling, Einstein equations, and benchmark promotion as separate ladder objects with blocked overreads.",
    caption:
      "Public comprehension diagram for the metric-response ladder route; it separates object status from downstream GR promotion.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-metric-response-ladder/diagrams/metric-response-ladder.mmd.",
  },
  {
    group: "physics",
    title: "Finite toy route freeze",
    src: "/assets/diagrams/comprehension/physics-finite-toy-models.png",
    alt: "Diagram showing a finite toy route moving through selector, draft/control construction, conditional audit, tag-removal stress, frozen negative local route status, and source-extension continuation while blocked overreads remain separate.",
    caption:
      "Public comprehension diagram for the finite toy models route; it explains a local frozen negative result without global theory rejection.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-finite-toy-models/diagrams/finite-toy-freeze.mmd.",
  },
  {
    group: "physics",
    title: "No-target-import discipline",
    src: "/assets/diagrams/comprehension/physics-no-target-import-discipline.png",
    alt: "Diagram showing source data entering a source-only factorization check while target topology, target atlas, target metric, benchmark success, and process authority are blocked into fail-closed obstruction labels.",
    caption:
      "Public comprehension diagram for the no-target-import discipline route; it explains a guardrail without proving candidate adoption.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-no-target-import-discipline/diagrams/no-target-import-discipline.mmd.",
  },
  {
    group: "physics",
    title: "Negative results and frozen routes",
    src: "/assets/diagrams/comprehension/physics-negative-results-and-frozen-routes.png",
    alt: "Diagram showing a failed route becoming a scoped obstruction, obstruction receipt, local freeze or selector route, and preserved evidence while global rejection and downstream promotion remain blocked.",
    caption:
      "Public comprehension diagram for the negative results route; it preserves obstruction scope without global rejection.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-negative-results-and-frozen-routes/diagrams/negative-results-freeze-flow.mmd.",
  },
  {
    group: "source-authority",
    title: "Resources manifest chain",
    src: "/assets/diagrams/comprehension/resources-manifest-chain.png",
    alt:
      "Diagram showing source manifest, asset manifest, resource index, downloads, hashes, status labels, and no authority creation.",
    caption:
      "Public comprehension diagram for resources; manifest rows organize assets without promoting them.",
    provenance:
      "Mermaid source: docs/content-dossiers/resources-index/diagrams/resource-manifest-chain.mmd.",
  },
  {
    group: "source-authority",
    title: "TeX/PDF derivative chain",
    src: "/assets/diagrams/comprehension/resources-tex-pdf-derivative-chain.png",
    alt:
      "Diagram showing registered TeX source, TeX registry row, generated PDF derivative, website copy, and source inspection download.",
    caption:
      "Public comprehension diagram for ontology documents; PDFs are derivatives of registered TeX.",
    provenance:
      "Mermaid source: docs/content-dossiers/resources-documents/diagrams/tex-pdf-derivative-chain.mmd.",
  },
  {
    group: "source-authority",
    title: "Diagram publication boundary",
    src: "/assets/diagrams/comprehension/resources-diagram-publication-boundary.png",
    alt:
      "Diagram showing Mermaid source, generated PNG, manifest entry, gallery, nearby prose, and diagram non-authority boundary.",
    caption:
      "Public comprehension diagram for this gallery; diagram publication creates a reader aid, not authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/resources-diagrams/diagrams/diagram-publication-boundary.mmd.",
  },
] satisfies Array<{
  group: DiagramGalleryGroupId;
  title: string;
  src: string;
  alt: string;
  caption: string;
  provenance: string;
}>;

export const resourceGroups = [
  {
    title: "External reviewer packet",
    href: "/resources/reviewer-packet/",
    body: "Human-review-pending inspection packet with claim boundaries before source inspection paths.",
  },
  {
    title: "Specialist guided starts",
    href: "/resources/guided-starts/",
    body: "Audience-specific reading paths for physicists, mathematicians, AI/agent researchers, software/system engineers, and reviewers.",
  },
  {
    title: "General-public guided start",
    href: "/resources/guided-starts/general-public/",
    body: "A first reading path that answers what this is, what is currently claimed, and what not to infer.",
  },
  {
    title: "Home",
    href: "/",
    body: "Canonical public entry point for the dual physics-and-AI research program framing.",
  },
  {
    title: "Physics Research",
    href: "/project/physics/",
    body: "Source-boundary-safe reader path for ontology, benchmark, derivation, and claim-gate pages.",
  },
  {
    title: "AI Research-Agent System",
    href: "/project/ai-research-agent-system/",
    body: "Reader path for workflow, roles, memory, registries, and validator/operator pages.",
  },
  {
    title: "Source authority",
    href: "/project/source-authority/",
    body: "Trust boundary for website pages, generated derivatives, manifests, and upstream records.",
  },
  {
    title: "Ontology Documents",
    href: "/resources/documents/",
    body: "Canonical ontology PDF derivatives and registered TeX source files served from the website.",
  },
  {
    title: "Operations",
    href: "/project/operations/",
    body: "Operational guides for routing, roles, validation, publication, improvement, and tool requirements.",
  },
  {
    title: "Diagram gallery",
    href: "/resources/diagrams/",
    body: "Current visual orientation fixture with explicit caption, provenance, and manifest status.",
  },
];

export type ProjectRouteStatus = "accepted" | "implemented" | "planned";

export interface ProjectSourceNoticeDefaults {
  claimStatus: string;
  updated: string;
  note: string;
  sourceRefs?: string[];
}

export interface ProjectRouteMetadata {
  title: string;
  href: string;
  phase: string;
  status: ProjectRouteStatus;
  description: string;
  sourceNotice: ProjectSourceNoticeDefaults;
  plannedChildren?: Array<{
    title: string;
    href: string;
    phase: string;
    status: Extract<ProjectRouteStatus, "implemented" | "planned">;
    description: string;
  }>;
}

export const projectSourceNoticeDefaults = {
  home: {
    claimStatus: "public orientation",
    updated: "2026-06-28",
    note: "The Home page is a reader-entry surface derived from the public overview and source-authority contract. It does not add scientific, mathematical, governance, or workflow authority.",
    sourceRefs: [
      "The AEther Flow Website. (2026). src/pages/index.astro",
      "The AEther Flow Website. (2026). docs/architecture/website-feature-and-functionality.md",
      "AEther-Flow Project. (2026). github-facing/project-overview-explainer.md",
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
    ],
  },
  physicsTrack: {
    claimStatus: "explanatory track landing",
    updated: "2026-06-25",
    note: "This page may orient readers to the physics track, but it must preserve the open GR-derivation boundary and defer scientific authority upstream.",
    sourceRefs: [
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). github-facing/aether-flow-physics-program-explainer.md",
      "AEther-Flow Project. (2026). github-facing/exact-gr-benchmark-boundary-explainer.md",
      "AEther-Flow Project. (2026). github-facing/claim-gates-explainer.md",
    ],
  },
  aiResearchAgentTrack: {
    claimStatus: "explanatory track landing",
    updated: "2026-06-25",
    note: "This page may explain the research-agent workflow, but it must separate AI-methodology claims from physics proof and preserve human accountability.",
    sourceRefs: [
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). github-facing/research-agent-workflow-explainer.md",
      "AEther-Flow Project. (2026). github-facing/roles-and-skills-explainer.md",
      "AEther-Flow Project. (2026). github-facing/memory-system-explainer.md",
    ],
  },
  operationsTrack: {
    claimStatus: "operational synthesis",
    updated: "2026-06-26",
    note: "This page family explains project operations. It cannot change routing behavior, validators, role authority, publication requirements, project-system signals, or physics status.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/director-agentjob-lifecycle-explainer.md",
      "AEther-Flow Project. (2026). github-facing/role-routing-explainer.md",
      "AEther-Flow Project. (2026). github-facing/validator-operator-workflow-explainer.md",
      "AEther-Flow Project. (2026). github-facing/documentation-curator-publication-process-explainer.md",
      "AEther-Flow Project. (2026). github-facing/project-system-improvement-explainer.md",
      "AEther-Flow Project. (2026). github-facing/technical-requirements-explainer.md",
    ],
  },
  sourceAuthority: {
    claimStatus: "source-authority orientation",
    updated: "2026-06-28",
    note: "This page may explain how to read website, generated material, and claim-boundary snapshots, but it cannot replace registered source files or registries.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). AGENTS.md",
      "AEther-Flow Project. (2026). registries/PUBLICATION_BRIEF_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
    ],
  },
  sourceAuthorityClaimBoundaryExplorer: {
    claimStatus: "claim-boundary registry orientation",
    updated: "2026-06-28",
    note: "This page presents a checked-in registry snapshot for reader orientation. It cannot create boundaries, certify claims, execute gates, or promote scientific results.",
    sourceRefs: [
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.md",
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
      "AEther-Flow Project. (2026). github-facing/claim-gates-explainer.md",
      "The AEther Flow Website. (2026). src/data/claim_boundary_snapshot.json",
      "The AEther Flow Website. (2026). docs/system-analyses/claim-boundary-explorer.md",
    ],
  },
  sourceAuthorityPublicationProvenance: {
    claimStatus: "publication/provenance orientation",
    updated: "2026-06-28",
    note: "This page explains website publication evidence. It cannot turn manifest presence, page hashes, source hashes, or internal-first routing into source truth.",
    sourceRefs: [
      "The AEther Flow Website. (2026). docs/architecture/website-feature-and-functionality.md",
      "The AEther Flow Website. (2026). public/files/manifests/page_route_map.json",
      "The AEther Flow Website. (2026). public/files/manifests/page_provenance.json",
      "The AEther Flow Website. (2026). public/files/manifests/source_manifest.json",
      "The AEther Flow Website. (2026). public/files/manifests/asset_manifest.json",
      "The AEther Flow Website. (2026). scripts/generate_page_provenance.py",
      "The AEther Flow Website. (2026). scripts/validate_page_provenance.py",
      "The AEther Flow Website. (2026). scripts/validate_manifest_paths.py",
      "The AEther Flow Website. (2026). scripts/validate_internal_first_links.py",
      "The AEther Flow Website. (2026). docs/system-analyses/publication-and-provenance-system.md",
    ],
  },
  physicsOntology: {
    claimStatus: "ontology orientation",
    updated: "2026-06-28",
    note: "This page explains AEther / AEther-flow vocabulary as a current research ontology. It is not an accepted derivation of GR and cannot promote ontology beyond upstream source authority.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/aether-flow-ontology-explainer.md",
      "AEther-Flow Project. (2026). ontology/aether-and-aether-flow.md",
      "AEther-Flow Project. (2026). ontology/README.md",
      "AEther-Flow Project. (2026). registries/TEX_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "The AEther Flow Website. (2026). docs/system-analyses/aether-flow-ontology-vocabulary.md",
    ],
  },
  physicsExactGrBenchmark: {
    claimStatus: "benchmark boundary orientation",
    updated: "2026-06-28",
    note: "This page explains the exact-GR benchmark boundary in reader-facing language. It does not certify substrate derivation, benchmark promotion, empirical deviation, or Gate Chair approval.",
    sourceRefs: [
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). github-facing/exact-gr-benchmark-boundary-explainer.md",
      "AEther-Flow Project. (2026). github-facing/aether-flow-physics-program-explainer.md",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/TEX_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "The AEther Flow Website. (2026). docs/system-analyses/exact-gr-benchmark-versus-derivation.md",
    ],
  },
  physicsGrDerivationRoadmap: {
    claimStatus: "roadmap orientation",
    updated: "2026-06-25",
    note: "This page explains the open GR-derivation roadmap. It is not proof of a milestone, source-object adoption beyond tracked scope, g_eff construction, matter coupling, Einstein equations, or benchmark promotion.",
    sourceRefs: [
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). github-facing/gr-derivation-roadmap-explainer.md",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/README.md",
    ],
  },
  physicsCurrentState: {
    claimStatus: "curated current-state snapshot",
    updated: "2026-06-28",
    note: "This page presents a checked-in website snapshot of upstream physics control state. It is not source authority, does not auto-refresh during build, and cannot promote draft/control data into adopted physics claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.md",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). research_control/design/mathematical_decisiveness_completion_contract.md",
      "AEther-Flow Project. (2026). research_control/design/obstruction_and_freeze_control.md",
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "The AEther Flow Website. (2026). src/data/physics_current_state_snapshot.json",
    ],
  },
  physicsDistanceToGr: {
    claimStatus: "ledger-backed burden dashboard",
    updated: "2026-06-28",
    note: "This page organizes a checked-in Distance-to-GR ledger snapshot. It is not a proof surface, progress percentage, live source authority, Gate Chair verdict, or downstream GR promotion.",
    sourceRefs: [
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). research_control/design/mathematical_decisiveness_completion_contract.md",
      "AEther-Flow Project. (2026). research_control/design/obstruction_and_freeze_control.md",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.yaml",
      "The AEther Flow Website. (2026). src/data/distance_to_gr_snapshot.json",
      "The AEther Flow Website. (2026). docs/system-analyses/distance-to-gr-dashboard.md",
    ],
  },
  physicsMetricResponseLadder: {
    claimStatus: "metric-response ladder orientation",
    updated: "2026-06-28",
    note: "This page explains checked-in metric-response ladder status. It cannot adopt MetricData(E), expand scoped g_eff, adopt a coupling law, derive matter coupling, derive Einstein equations, promote the benchmark, or complete GR derivation.",
    sourceRefs: [
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.md",
      "The AEther Flow Website. (2026). src/data/distance_to_gr_snapshot.json",
      "The AEther Flow Website. (2026). src/data/physics_current_state_snapshot.json",
      "The AEther Flow Website. (2026). src/data/claim_boundary_snapshot.json",
      "The AEther Flow Website. (2026). docs/system-analyses/metric-response-ladder.md",
    ],
  },
  physicsFiniteToyModels: {
    claimStatus: "finite toy frozen-route orientation",
    updated: "2026-06-28",
    note: "This page explains the explicit-tag-only finite toy route as a local frozen negative result. It cannot adopt toy tags as ontology, derive a physical metric, claim global theory rejection, or promote downstream GR claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/RESEARCH_TASK_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/ROLE_EXECUTION_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-053/artifacts/94_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL.tex",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-054/artifacts/95_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_SMUGGLING_AUDIT.tex",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0097.yaml",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-056/artifacts/97_RESP_LC_THEORETICAL_CONTINUATION_SELECTOR_SOURCE_EXTENSION_DECISION.yaml",
      "The AEther Flow Website. (2026). docs/system-analyses/finite-toy-models-and-frozen-route.md",
    ],
  },
  physicsNoTargetImportDiscipline: {
    claimStatus: "no-target-import methodology orientation",
    updated: "2026-06-28",
    note: "This page explains no-target-import discipline as a methodology guardrail. It cannot prove that all future work is target-import-free, adopt M_src, define g_eff, derive matter coupling, or promote downstream GR claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). research_control/design/no_target_import_guard_map.md",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-105/DDR-20260614-105.md",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-128/jobs/completions/AJC-AJ-RT-20260614-128-001.yaml",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-128/artifacts/parent_conflict_review_m_src_gsc_no_target_import_criterion.yaml",
      "AEther-Flow Project. (2026). registries/RESEARCH_TASK_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). github-facing/claim-gates-explainer.md",
      "AEther-Flow Project. (2026). github-facing/gr-derivation-roadmap-explainer.md",
      "The AEther Flow Website. (2026). docs/system-analyses/no-target-import-discipline.md",
    ],
  },
  physicsNegativeResultsFrozenRoutes: {
    claimStatus: "negative-result and freeze-control orientation",
    updated: "2026-06-28",
    note: "This page explains negative results and frozen routes as scoped evidence. It cannot issue a freeze, prove global theory rejection, prove future source-extension impossibility, or promote downstream GR claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). research_control/design/obstruction_and_freeze_control.md",
      "AEther-Flow Project. (2026). github-facing/claim-gates-explainer.md",
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex",
      "AEther-Flow Project. (2026). research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex",
      "The AEther Flow Website. (2026). src/data/distance_to_gr_snapshot.json",
      "The AEther Flow Website. (2026). src/data/claim_boundary_snapshot.json",
      "The AEther Flow Website. (2026). docs/system-analyses/negative-results-and-frozen-routes.md",
    ],
  },
  physicsClaimGates: {
    claimStatus: "claim-control orientation",
    updated: "2026-06-25",
    note: "This page explains claim gates, negative results, scoped obstructions, and freeze criteria for readers. It does not create claim boundaries, issue a Gate Chair verdict, promote a benchmark, or reinterpret blocked states as success.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/claim-gates-explainer.md",
      "AEther-Flow Project. (2026). research_control/README.md",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/AGENT_ROLE_REGISTRY.csv",
      "AEther-Flow Project. (2026). github-facing/research-agent-workflow-explainer.md",
    ],
  },
  physicsSourceExtensionPipeline: {
    claimStatus: "source-extension workflow orientation",
    updated: "2026-06-27",
    note: "This page explains the source-extension workflow for readers. It cannot turn proposal-only, draft/control, audit, stress, selector, validator, or precondition status into adoption or downstream GR promotion.",
    sourceRefs: [
      "AEther-Flow Project. (2026). research_control/README.md",
      "AEther-Flow Project. (2026). github-facing/claim-gates-explainer.md",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "The AEther Flow Website. (2026). docs/system-analyses/source-extension-pipeline.md",
    ],
  },
  physicsGateChairAndHumanGates: {
    claimStatus: "human-gated authority orientation",
    updated: "2026-06-28",
    note: "This page explains Gate Chair and human-gated decision authority for readers. It cannot execute a gate, issue a Gate Chair verdict, treat validators as scientific proof, or promote source-law, MetricData(E), g_eff, matter-coupling, Einstein-equation, benchmark, or downstream GR claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.yaml",
      "AEther-Flow Project. (2026). registries/AGENT_ROLE_REGISTRY.csv",
      "AEther-Flow Project. (2026). .agents/roles/physics/gate-chair.v0.1.0.md",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "The AEther Flow Website. (2026). docs/system-analyses/gate-chair-and-human-gated-decisions.md",
    ],
  },
  aiResearchAgentWorkflow: {
    claimStatus: "workflow orientation",
    updated: "2026-06-28",
    note: "This page explains a committed bounded research-agent workflow record chain for readers. It does not change routing behavior, mutate control records, expand role authority, treat validator success as scientific proof, anthropomorphize model behavior, or replace human-gated decisions.",
    sourceRefs: [
      "The AEther Flow. (2026). github-facing/research-agent-workflow-explainer.md",
      "The AEther Flow. (2026). github-facing/director-agentjob-lifecycle-explainer.md",
      "The AEther Flow. (2026). research_control/README.md",
      "The AEther Flow. (2026). github-facing/validator-operator-workflow-explainer.md",
      "The AEther Flow. (2026). research_control/tasks/RT-20260614-249/00_TASK.yaml",
      "The AEther Flow. (2026). research_control/tasks/RT-20260614-249/DDR-20260614-249.md",
      "The AEther Flow. (2026). research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml",
      "The AEther Flow. (2026). research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml",
      "The AEther Flow. (2026). research_control/handoffs/handoff-0282.yaml",
      "The AEther Flow Website. (2026). docs/system-analyses/research-agent-workflow-walkthrough.md",
    ],
  },
  aiOneBoundedAgentJob: {
    claimStatus: "one-agentjob orientation",
    updated: "2026-06-28",
    note: "This page explains one committed AgentJob as a bounded permission envelope. It cannot authorize a new job, reuse a past allowlist as current permission, mutate completion evidence, treat validator success as scientific proof, or promote physics claims.",
    sourceRefs: [
      "The AEther Flow. (2026). github-facing/research-agent-workflow-explainer.md",
      "The AEther Flow. (2026). github-facing/director-agentjob-lifecycle-explainer.md",
      "The AEther Flow. (2026). research_control/README.md",
      "The AEther Flow. (2026). research_control/tasks/RT-20260614-249/jobs/AJ-RT-20260614-249-001.yaml",
      "The AEther Flow. (2026). research_control/tasks/RT-20260614-249/00_TASK.yaml",
      "The AEther Flow. (2026). research_control/tasks/RT-20260614-249/DDR-20260614-249.md",
      "The AEther Flow. (2026). research_control/tasks/RT-20260614-249/jobs/completions/AJC-AJ-RT-20260614-249-001.yaml",
      "The AEther Flow. (2026). research_control/handoffs/handoff-0282.yaml",
      "The AEther Flow. (2026). registries/AGENT_JOB_REGISTRY.csv",
      "The AEther Flow Website. (2026). docs/system-analyses/one-bounded-agentjob-in-practice.md",
    ],
  },
  aiRolesAndSkills: {
    claimStatus: "role-and-skill orientation",
    updated: "2026-06-25",
    note: "This page explains role contracts, governed skills, and authority inspection order for readers. It does not register roles, supersede roles, expand role authority, change skill contracts, change allowlists, or promote physics claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/roles-and-skills-explainer.md",
      "AEther-Flow Project. (2026). github-facing/role-routing-explainer.md",
      "AEther-Flow Project. (2026). research_control/README.md",
      "AEther-Flow Project. (2026). AGENTS.md",
      "AEther-Flow Project. (2026). registries/AGENT_ROLE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/ROLE_EXECUTION_REGISTRY.csv",
      "AEther-Flow Project. (2026). .codex/skills/continue-research/SKILL.md",
      "AEther-Flow Project. (2026). .codex/skills/improve-project-system/SKILL.md",
      "AEther-Flow Project. (2026). .codex/skills/project-memory-system/SKILL.md",
      "AEther-Flow Project. (2026). .codex/skills/html-visual-explainer/SKILL.md",
      "AEther-Flow Project. (2026). .codex/skills/visual-explainer/SKILL.md",
    ],
  },
  aiRoleAuthorityInspector: {
    claimStatus: "role-authority inspection orientation",
    updated: "2026-06-28",
    note: "This page explains how to inspect role authority from committed source records. It cannot register roles, activate roles, supersede roles, change schemas, change AgentJob allowlists, bypass human gates, or promote claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). registries/AGENT_ROLE_REGISTRY.csv",
      "AEther-Flow Project. (2026). github-facing/roles-and-skills-explainer.md",
      "AEther-Flow Project. (2026). github-facing/role-routing-explainer.md",
      "AEther-Flow Project. (2026). .agents/schemas/EXECUTION_ROLE_SCHEMA.md",
      "AEther-Flow Project. (2026). .agents/schemas/AGENT_JOB_SCHEMA.md",
      "AEther-Flow Project. (2026). research_control/README.md",
      "The AEther Flow Website. (2026). docs/system-analyses/role-authority-inspector.md",
    ],
  },
  aiMemoryRegistries: {
    claimStatus: "memory-preflight orientation",
    updated: "2026-06-28",
    note: "This page explains memory preflight, source-first retrieval, registry inspection, and retrieval-layer limits for readers. It does not expose private memory contents, change memory behavior, change registry schema, override source authority, or promote claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/memory-system-explainer.md",
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
      "AEther-Flow Project. (2026). research_control/README.md",
      "AEther-Flow Project. (2026). .agents/schemas/AGENT_JOB_SCHEMA.md",
      "AEther-Flow Project. (2026). .codex/skills/project-memory-system/SKILL.md",
      "AEther-Flow Project. (2026). AGENTS.md",
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). registries/MARKDOWN_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/TEX_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/WIKI_ARTIFACT_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/OBSIDIAN_VAULT_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/CONTENT_SEMANTIC_REGISTRY.csv",
      "The AEther Flow Website. (2026). docs/system-analyses/memory-preflight-and-source-first-retrieval.md",
    ],
  },
  aiValidatorOperatorWorkflow: {
    claimStatus: "validator-operator orientation",
    updated: "2026-06-25",
    note: "This page explains validation, deterministic checks, documentation impact, checkpoint gates, screenshots, tests, and PASS-result limits for readers. It does not change validator behavior, command semantics, routing behavior, checkpoint gates, sidecar adoption status, generated-output authority, or physics claim status.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/validator-operator-workflow-explainer.md",
      "AEther-Flow Project. (2026). github-facing/project-system-improvement-explainer.md",
      "AEther-Flow Project. (2026). research_control/README.md",
      "AEther-Flow Project. (2026). AGENTS.md",
      "AEther-Flow Project. (2026). .codex/skills/improve-project-system/SKILL.md",
      "AEther-Flow Project. (2026). .codex/skills/project-memory-system/SKILL.md",
      "AEther-Flow Project. (2026). scripts/README.md",
      "AEther-Flow Project. (2026). scripts/project_control/README.md",
      "AEther-Flow Project. (2026). scripts/research_control/README.md",
      "AEther-Flow Project. (2026). tests/README.md",
    ],
  },
  generalPublicGuidedStart: {
    claimStatus: "guided reading path",
    updated: "2026-06-28",
    note: "This route assembles existing sourced pages for general-public orientation. It cannot update source state, create claims, or convert public explanation into proof.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/project-overview-explainer.md",
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.yaml",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "The AEther Flow Website. (2026). public/files/manifests/page_route_map.json",
      "The AEther Flow Website. (2026). docs/content-dossiers/guided-start-general-public/dossier.md",
    ],
  },
  specialistGuidedStarts: {
    claimStatus: "specialist guided reading path",
    updated: "2026-06-28",
    note: "This route assembles existing sourced pages by specialist audience. It cannot create claims, update source state, grant role authority, or replace the future reviewer packet.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/project-overview-explainer.md",
      "AEther-Flow Project. (2026). github-facing/aether-flow-physics-program-explainer.md",
      "AEther-Flow Project. (2026). github-facing/exact-gr-benchmark-boundary-explainer.md",
      "AEther-Flow Project. (2026). github-facing/claim-gates-explainer.md",
      "AEther-Flow Project. (2026). github-facing/research-agent-workflow-explainer.md",
      "AEther-Flow Project. (2026). github-facing/roles-and-skills-explainer.md",
      "AEther-Flow Project. (2026). github-facing/memory-system-explainer.md",
      "AEther-Flow Project. (2026). github-facing/validator-operator-workflow-explainer.md",
      "AEther-Flow Project. (2026). github-facing/documentation-curator-publication-process-explainer.md",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "The AEther Flow Website. (2026). public/files/manifests/page_route_map.json",
      "The AEther Flow Website. (2026). docs/content-dossiers/guided-start-specialists/dossier.md",
      "The AEther Flow Website. (2026). docs/system-analyses/specialist-guided-starts.md",
    ],
  },
  reviewerPacket: {
    claimStatus: "human review pending reviewer packet",
    updated: "2026-06-28",
    note: "This route is an external-review inspection guide. It cannot claim peer review, external validation, scientific viability, completed derivation, or source authority.",
    sourceRefs: [
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0281.md",
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). ontology/README.md",
      "AEther-Flow Project. (2026). ontology/tex/README.md",
      "AEther-Flow Project. (2026). registries/TEX_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
      "AEther-Flow Project. (2026). github-facing/exact-gr-benchmark-boundary-explainer.md",
      "AEther-Flow Project. (2026). github-facing/aether-flow-physics-program-explainer.md",
      "AEther-Flow Project. (2026). github-facing/research-agent-workflow-explainer.md",
      "The AEther Flow Website. (2026). src/data/physics_current_state_snapshot.json",
      "The AEther Flow Website. (2026). docs/system-analyses/external-review-packet.md",
      "The AEther Flow Website. (2026). docs/content-dossiers/reviewer-packet/dossier.md",
    ],
  },
} satisfies Record<string, ProjectSourceNoticeDefaults>;

export const projectPhysicsDeepDiveRoutes = [
  {
    title: "Current physics state",
    href: "/project/physics/current-state/",
    phase: "Current snapshot",
    status: "implemented",
    description: "Reviewed source-state snapshot for active task, latest handoff, open burden, blocked claims, and next action.",
  },
  {
    title: "Distance-to-GR dashboard",
    href: "/project/physics/distance-to-gr/",
    phase: "PG-002",
    status: "implemented",
    description: "Ledger-backed burden dashboard that rejects progress-bar proof and downstream claim promotion.",
  },
  {
    title: "Metric response ladder",
    href: "/project/physics/metric-response-ladder/",
    phase: "PG-009",
    status: "implemented",
    description: "Glossary-first ladder for Resp_lc, M_src, MetricData(E), scoped g_eff, matter coupling, equations, and blocked promotions.",
  },
  {
    title: "Finite toy models",
    href: "/project/physics/finite-toy-models/",
    phase: "PG-010",
    status: "implemented",
    description: "Controlled finite-model explainer for the explicit-tag frozen negative route and its non-global scope.",
  },
  {
    title: "No-target-import discipline",
    href: "/project/physics/no-target-import-discipline/",
    phase: "PG-011",
    status: "implemented",
    description: "Methodology guardrail for blocking target-context and process-authority imports without claiming completed proof.",
  },
  {
    title: "Negative results and frozen routes",
    href: "/project/physics/negative-results-and-frozen-routes/",
    phase: "PG-012",
    status: "implemented",
    description: "Evidence-preservation explainer for scoped obstructions, frozen negative routes, and local freeze boundaries.",
  },
  {
    title: "AEther / AEther-flow ontology",
    href: "/project/physics/ontology/",
    phase: "Phase 4A",
    status: "implemented",
    description: "Ontology explainer that keeps vocabulary orientation separate from GR derivation.",
  },
  {
    title: "Exact-GR benchmark boundary",
    href: "/project/physics/exact-gr-benchmark/",
    phase: "Phase 4B",
    status: "implemented",
    description: "Boundary explainer separating benchmark compatibility from first-principles derivation.",
  },
  {
    title: "GR derivation roadmap",
    href: "/project/physics/gr-derivation-roadmap/",
    phase: "Phase 4C",
    status: "implemented",
    description: "Roadmap explainer for the open derivation burden and its guarded milestones.",
  },
  {
    title: "Source extension pipeline",
    href: "/project/physics/source-extension-pipeline/",
    phase: "PG-003",
    status: "implemented",
    description: "Workflow explainer for proposal-only, audit, stress, selector, and human-gated source-extension preconditions.",
  },
  {
    title: "Gate Chair and human gates",
    href: "/project/physics/gate-chair-and-human-gates/",
    phase: "PG-004",
    status: "implemented",
    description: "Authority explainer for protected human-gated decisions, Gate Chair status, validator limits, and verdict boundaries.",
  },
  {
    title: "Claim gates and obstructions",
    href: "/project/physics/claim-gates/",
    phase: "Phase 4D",
    status: "implemented",
    description: "Explainer for no-go records, scoped obstructions, freeze discipline, and gates.",
  },
];

export const projectAiDeepDiveRoutes = [
  {
    title: "Research-agent workflow",
    href: "/project/ai-research-agent-system/workflow/",
    phase: "Phase 5A",
    status: "implemented",
    description: "Request classification, Director decisions, one bounded AgentJob, completion evidence, handoffs, and authority limits.",
  },
  {
    title: "One bounded AgentJob",
    href: "/project/ai-research-agent-system/one-bounded-agentjob/",
    phase: "PG-015",
    status: "implemented",
    description: "Concrete permission-envelope walkthrough for one auditable AgentJob transaction.",
  },
  {
    title: "Roles and skills",
    href: "/project/ai-research-agent-system/roles-and-skills/",
    phase: "Phase 5B",
    status: "implemented",
    description: "Role and skill contract explainer with task-local authority and allowlist boundaries.",
  },
  {
    title: "Role authority inspector",
    href: "/project/ai-research-agent-system/role-authority-inspector/",
    phase: "PG-017",
    status: "implemented",
    description: "Static inspection stack separating role labels, registry status, execution records, and AgentJob authority.",
  },
  {
    title: "Memory preflight",
    href: "/project/ai-research-agent-system/memory-registries/",
    phase: "PG-018",
    status: "implemented",
    description: "Source-first retrieval, memory preflight receipts, registry inspection, and retrieval-layer boundaries.",
  },
  {
    title: "Parent-child synthesis",
    href: "/project/ai-research-agent-system/parent-child-synthesis/",
    phase: "Phase 5D",
    status: "implemented",
    description: "One-AgentJob perspective-synthesis explainer preserving a single outer authority frame.",
  },
];

export const projectOperationsRoutes = [
  {
    title: "Director and AgentJob lifecycle",
    href: "/project/operations/director-agentjob-lifecycle/",
    phase: "Operations",
    status: "implemented",
    description: "Task, decision, AgentJob, completion, handoff, and registry evidence chain.",
  },
  {
    title: "Role routing",
    href: "/project/operations/role-routing/",
    phase: "Operations",
    status: "implemented",
    description: "Role templates, execution-role records, task overlays, provisional roles, and allowlists.",
  },
  {
    title: "Validator PASS limits",
    href: "/project/operations/validator-operator-workflow/",
    phase: "PG-019",
    status: "implemented",
    description: "Why command PASS is checked-state evidence, not theorem proof, claim promotion, role authority, or Gate Chair approval.",
  },
  {
    title: "Publication process",
    href: "/project/operations/publication-process/",
    phase: "Operations",
    status: "implemented",
    description: "Brief, source spec, public page, screenshot evidence, and review discipline.",
  },
  {
    title: "Project-system improvement",
    href: "/project/operations/project-system-improvement/",
    phase: "PG-020",
    status: "implemented",
    description: "Signals, sidecars, classifiers, advisory resolver output, one bounded maintenance packet, and explicit closure evidence.",
  },
  {
    title: "Technical requirements",
    href: "/project/operations/technical-requirements/",
    phase: "Operations",
    status: "implemented",
    description: "Local tool tiers for reproducible operation without confusing tools with authorization.",
  },
];

export const projectSourceAuthorityRoutes = [
  {
    title: "Claim Boundary Explorer",
    href: "/project/source-authority/claim-boundary-explorer/",
    phase: "PG-005",
    status: "implemented",
    description: "Source-pinned registry snapshot showing allowed, forbidden, and gate-required wording without certifying claims.",
  },
  {
    title: "Publication And Provenance System",
    href: "/project/source-authority/publication-and-provenance-system/",
    phase: "PG-024",
    status: "implemented",
    description: "Route maps, page provenance, source manifests, asset manifests, hashes, and internal-first routing without creating source truth.",
  },
];

const toNavigationChild = (route: {
  title: string;
  href: string;
  description: string;
}): SiteNavigationChild => ({
  title: route.title,
  href: route.href,
  description: route.description,
});

export const siteNavigationLinks: SiteNavigationLink[] = [
  {
    title: "Home",
    href: "/",
  },
  {
    title: "Physics Research",
    href: "/project/physics/",
    matchPrefixes: ["/project/physics/"],
    children: [
      {
        title: "Physics Research",
        href: "/project/physics/",
        description: "Track landing for ontology, benchmark, derivation roadmap, and claim-gate context.",
      },
      ...projectPhysicsDeepDiveRoutes.map(toNavigationChild),
    ],
  },
  {
    title: "AI Research System",
    href: "/project/ai-research-agent-system/",
    matchPrefixes: ["/project/ai-research-agent-system/"],
    children: [
      {
        title: "AI Research System",
        href: "/project/ai-research-agent-system/",
        description: "Track landing for bounded research-agent workflow, roles, memory, and synthesis.",
      },
      ...projectAiDeepDiveRoutes.map(toNavigationChild),
    ],
  },
  {
    title: "Research Ops",
    href: "/project/operations/",
    matchPrefixes: ["/project/operations/"],
    children: [
      {
        title: "Research Ops",
        href: "/project/operations/",
        description: "Operational landing for lifecycle, routing, validation, publication, improvement, and tools.",
      },
      ...projectOperationsRoutes.map(toNavigationChild),
    ],
  },
  {
    title: "Source Authority",
    href: "/project/source-authority/",
    matchPrefixes: ["/project/source-authority/"],
    children: [
      {
        title: "Source Authority",
        href: "/project/source-authority/",
        description: "Trust boundary for website pages, generated derivatives, manifests, and upstream records.",
      },
      ...projectSourceAuthorityRoutes.map(toNavigationChild),
    ],
  },
  {
    title: "Library",
    href: "/resources/",
    matchPrefixes: ["/resources/"],
    children: [
      {
        title: "Library",
        href: "/resources/",
        description: "Manifest-backed resource index for public pages and approved ontology documents.",
      },
      {
        title: "External Reviewer Packet",
        href: "/resources/reviewer-packet/",
        description: "Human-review-pending inspection packet with claim boundaries before source inspection.",
      },
      {
        title: "Specialist Guided Starts",
        href: "/resources/guided-starts/",
        description: "Audience-specific internal-first paths for specialist readers and staged reviewer prerequisites.",
      },
      {
        title: "General-Public Guided Start",
        href: "/resources/guided-starts/general-public/",
        description: "First reading path through the site for general-public readers.",
      },
      {
        title: "Ontology Documents",
        href: "/resources/documents/",
        description: "Canonical ontology PDF derivatives and registered TeX source files served from the website.",
      },
      {
        title: "Diagram Gallery",
        href: "/resources/diagrams/",
        description: "Website-local visual orientation fixtures with explicit provenance and non-authority status.",
      },
    ],
  },
];

export const projectReadingPathRoutes: ProjectRouteMetadata[] = [
  {
    title: "Home",
    href: "/",
    phase: "Canonical Home",
    status: "accepted",
    description: "Canonical public Home introducing AEther Flow as a dual physics-and-AI research program.",
    sourceNotice: projectSourceNoticeDefaults.home,
  },
  {
    title: "Physics Research",
    href: "/project/physics/",
    phase: "Phase 2",
    status: "implemented",
    description: "First-class track landing page for ontology, benchmark, open derivation, and obstruction boundaries.",
    sourceNotice: projectSourceNoticeDefaults.physicsTrack,
    plannedChildren: projectPhysicsDeepDiveRoutes,
  },
  {
    title: "AI Research-Agent System",
    href: "/project/ai-research-agent-system/",
    phase: "Phase 2",
    status: "implemented",
    description: "First-class track landing page for the governed AI-assisted research workflow.",
    sourceNotice: projectSourceNoticeDefaults.aiResearchAgentTrack,
    plannedChildren: projectAiDeepDiveRoutes,
  },
  {
    title: "Operations",
    href: "/project/operations/",
    phase: "PRD release",
    status: "implemented",
    description: "Operational route family for lifecycle, role routing, validation, publication, project-system repair, and tool requirements.",
    sourceNotice: projectSourceNoticeDefaults.operationsTrack,
    plannedChildren: projectOperationsRoutes,
  },
  {
    title: "Source Authority",
    href: "/project/source-authority/",
    phase: "Phase 3 / PG-005",
    status: "implemented",
    description: "Trust and source-boundary page explaining how readers should treat website material, generated derivatives, and claim-boundary snapshots.",
    sourceNotice: projectSourceNoticeDefaults.sourceAuthority,
    plannedChildren: projectSourceAuthorityRoutes,
  },
];

export const projectInformationArchitectureDecision = {
  firstFamilyRoutes: [
    "/project/physics/",
    "/project/ai-research-agent-system/",
    "/project/operations/",
    "/project/source-authority/",
  ],
  navigationChange: {
    status: "implemented",
    phase: "Phase 7",
    rationale:
      "Primary navigation now exposes the public project reading path: Home, physics, AI system, operations, source authority, and resources.",
  },
  internalFirstLinkDecision: {
    status: "implemented",
    phase: "Internal explainer/source asset release",
    rationale:
      "Mapped explainer source links are kept in provenance sections while primary journey cards point to internal website routes.",
  },
  reusableComponentDecision: {
    status: "defer",
    rationale:
      "Phase 1 only defines data. Track cards, route chips, source-boundary panels, and next-step lists should be extracted after Phase 2 proves the repeated markup shape.",
  },
};
