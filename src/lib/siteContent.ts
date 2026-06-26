export type SiteNavigationLink = {
  title: string;
  href: string;
  matchPrefixes?: string[];
};

export const siteNavigationLinks: SiteNavigationLink[] = [
  {
    title: "Overview",
    href: "/project/overview/",
  },
  {
    title: "Physics",
    href: "/project/physics/",
    matchPrefixes: ["/project/physics/"],
  },
  {
    title: "AI system",
    href: "/project/ai-research-agent-system/",
    matchPrefixes: ["/project/ai-research-agent-system/"],
  },
  {
    title: "Operations",
    href: "/project/operations/",
    matchPrefixes: ["/project/operations/"],
  },
  {
    title: "Source authority",
    href: "/project/source-authority/",
  },
  {
    title: "Resources",
    href: "/resources/",
    matchPrefixes: ["/resources/"],
  },
];

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

export const researchMapNodes = [
  {
    title: "Source repository",
    status: "authoritative",
    body: "Research-control records, validators, source documents, and approved publication material remain upstream.",
  },
  {
    title: "Website manifest layer",
    status: "index",
    body: "The website records public asset paths, hashes, and source references before rendering reader surfaces.",
  },
  {
    title: "Reader-facing pages",
    status: "presentation",
    body: "Pages summarize, organize, and link reviewed material without extending the science.",
  },
  {
    title: "Deployment output",
    status: "static",
    body: "Astro builds static HTML and assets into dist/ for static hosting.",
  },
];

export const diagramGalleryItems = [
  {
    title: "Publication Layer Map sample",
    src: "/assets/diagrams/publication-layer-map.svg",
    alt: "Diagram showing source repository authority flowing into website manifests and static reader pages.",
    caption:
      "A sample, non-authoritative orientation diagram for the website publication layer.",
    provenance: "Website scaffold fixture; not a scientific source artifact.",
  },
];

export const resourceGroups = [
  {
    title: "Project overview",
    href: "/project/overview/",
    body: "Accepted public entry point for the dual physics-and-AI research program framing.",
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
    title: "Diagram sample gallery",
    href: "/resources/diagrams/",
    body: "Current visual orientation fixture with explicit caption, provenance, and manifest status.",
  },
  {
    title: "Equation sample",
    href: "/research/equations/",
    body: "A math-heavy static page used to verify KaTeX behavior and mobile equation wrapping.",
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
  overview: {
    claimStatus: "explanatory overview",
    updated: "2026-06-25",
    note: "This overview explains the accepted public project structure. Source authority remains with The-AEther-Flow.",
    sourceRefs: [
      "The AEther Flow Website. (2026). PRDs/dual-project-public-overview-prd.md",
      "The AEther Flow Website. (2026). src/pages/project/overview.astro",
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
    updated: "2026-06-25",
    note: "This page may explain how to read website and generated material, but it cannot replace registered source files or registries.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). AGENTS.md",
      "AEther-Flow Project. (2026). registries/PUBLICATION_BRIEF_REGISTRY.csv",
    ],
  },
  physicsOntology: {
    claimStatus: "ontology orientation",
    updated: "2026-06-25",
    note: "This page explains AEther / AEther-flow vocabulary as a current research ontology. It is not an accepted derivation of GR and cannot promote ontology beyond upstream source authority.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/aether-flow-ontology-explainer.md",
      "AEther-Flow Project. (2026). ontology/aether-and-aether-flow.md",
      "AEther-Flow Project. (2026). ontology/README.md",
      "AEther-Flow Project. (2026). registries/TEX_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
    ],
  },
  physicsExactGrBenchmark: {
    claimStatus: "benchmark boundary orientation",
    updated: "2026-06-25",
    note: "This page explains the exact-GR benchmark boundary in reader-facing language. It does not certify substrate derivation, benchmark promotion, empirical deviation, or Gate Chair approval.",
    sourceRefs: [
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). github-facing/exact-gr-benchmark-boundary-explainer.md",
      "AEther-Flow Project. (2026). github-facing/aether-flow-physics-program-explainer.md",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). registries/TEX_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
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
    updated: "2026-06-26",
    note: "This page presents a checked-in website snapshot of upstream physics control state. It is not source authority, does not auto-refresh during build, and cannot promote draft/control data into adopted physics claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0230.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0230.md",
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "The AEther Flow Website. (2026). src/data/physics_current_state_snapshot.json",
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
  aiResearchAgentWorkflow: {
    claimStatus: "workflow orientation",
    updated: "2026-06-25",
    note: "This page explains bounded research-agent workflow for readers. It does not change routing behavior, mutate control records, expand role authority, treat validator success as scientific proof, or replace human-gated decisions.",
    sourceRefs: [
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). AGENTS.md",
      "AEther-Flow Project. (2026). research_control/README.md",
      "AEther-Flow Project. (2026). github-facing/research-agent-workflow-explainer.md",
      "AEther-Flow Project. (2026). github-facing/director-agentjob-lifecycle-explainer.md",
      "AEther-Flow Project. (2026). github-facing/parent-child-synthesis-explainer.md",
      "AEther-Flow Project. (2026). .codex/skills/continue-research/SKILL.md",
      "AEther-Flow Project. (2026). .codex/skills/improve-project-system/SKILL.md",
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
  aiMemoryRegistries: {
    claimStatus: "memory-and-registry orientation",
    updated: "2026-06-25",
    note: "This page explains source-first memory, wiki surfaces, registries, semantic extracts, and retrieval limits for readers. It does not change memory behavior, registry schema, source authority, generated-output authority, or physics claim status.",
    sourceRefs: [
      "AEther-Flow Project. (2026). github-facing/memory-system-explainer.md",
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
      "AEther-Flow Project. (2026). .codex/skills/project-memory-system/SKILL.md",
      "AEther-Flow Project. (2026). research_control/README.md",
      "AEther-Flow Project. (2026). AGENTS.md",
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). registries/MARKDOWN_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/TEX_SOURCE_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/WIKI_ARTIFACT_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/OBSIDIAN_VAULT_REGISTRY.csv",
      "AEther-Flow Project. (2026). registries/CONTENT_SEMANTIC_REGISTRY.csv",
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
    title: "Claim gates and obstructions",
    href: "/project/physics/claim-gates/",
    phase: "Phase 4D",
    status: "implemented",
    description: "Explainer for no-go records, scoped obstructions, freeze discipline, and gates.",
  },
];

export const projectAiDeepDiveRoutes = [
  {
    title: "Roles and skills",
    href: "/project/ai-research-agent-system/roles-and-skills/",
    phase: "Phase 5B",
    status: "implemented",
    description: "Role and skill contract explainer with task-local authority and allowlist boundaries.",
  },
  {
    title: "Memory and registries",
    href: "/project/ai-research-agent-system/memory-registries/",
    phase: "Phase 5C",
    status: "implemented",
    description: "Source-first memory, wiki, registry, and retrieval-surface explainer.",
  },
  {
    title: "Parent-child synthesis",
    href: "/project/ai-research-agent-system/parent-child-synthesis/",
    phase: "Phase 5D",
    status: "implemented",
    description: "One-AgentJob perspective-synthesis explainer preserving a single outer authority frame.",
  },
  {
    title: "Validator and operator workflow",
    href: "/project/operations/validator-operator-workflow/",
    phase: "Operations",
    status: "implemented",
    description: "Operational guide that treats PASS results as bounded evidence, not authority expansion.",
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
    title: "Validator and operator workflow",
    href: "/project/operations/validator-operator-workflow/",
    phase: "Operations",
    status: "implemented",
    description: "Command selection, documentation-impact receipts, screenshots, tests, and PASS limits.",
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
    phase: "Operations",
    status: "implemented",
    description: "Classifier, resolver, signals, sidecars, one bounded AgentJob, and resolution evidence.",
  },
  {
    title: "Technical requirements",
    href: "/project/operations/technical-requirements/",
    phase: "Operations",
    status: "implemented",
    description: "Local tool tiers for reproducible operation without confusing tools with authorization.",
  },
];

export const projectReadingPathRoutes: ProjectRouteMetadata[] = [
  {
    title: "Project overview",
    href: "/project/overview/",
    phase: "Accepted overview",
    status: "accepted",
    description: "Accepted public overview introducing AEther Flow as a dual physics-and-AI research program.",
    sourceNotice: projectSourceNoticeDefaults.overview,
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
    phase: "Phase 3",
    status: "implemented",
    description: "Trust and source-boundary page explaining how readers should treat website and generated material.",
    sourceNotice: projectSourceNoticeDefaults.sourceAuthority,
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
      "Primary navigation now exposes the public project reading path: overview, physics, AI system, operations, source authority, and resources.",
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
