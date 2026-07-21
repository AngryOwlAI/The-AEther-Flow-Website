import type { ComprehensionContent } from "./comprehensionContent";
import { withImageDimensions } from "./imageMetadata";

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

export const publicComprehensionSummaryLabels = {
  safe: "Safe summary",
  unsafe: "Unsafe summary",
} as const;

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

const diagramGallerySourceItems = [
  {
    group: "source-authority",
    title: "Home two-track map",
    src: "/assets/diagrams/comprehension/project-overview-two-track-map.png",
    alt: "Diagram showing The AEther Flow Home page as physics research and AI research-agent workflow downstream from source authority.",
    caption:
      "The diagram illustrates how the Home route branches into the physics research lane, the AI research-agent workflow, and the shared source-authority spine.",
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
      "The diagram illustrates the physics track as layered status areas: ontology, benchmark behavior, derivation burdens, claim gates, and source authority.",
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
      "The diagram illustrates how ontology vocabulary, mathematical bridge work, benchmark status, and empirical prediction occupy separate zones.",
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
      "The diagram illustrates the benchmark ladder from operational exact-GR compatibility through source derivation and downstream promotion burdens.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-exact-gr-benchmark/diagrams/benchmark-boundary-ladder.mmd.",
  },
  {
    group: "physics",
    title: "Physics derivation burden ladder",
    src: "/assets/diagrams/comprehension/physics-roadmap-burden-ladder.png",
    alt: "Diagram showing the GR derivation roadmap as separate source, metric, matter-coupling, equation, and promotion burdens.",
    caption:
      "The diagram illustrates the GR derivation roadmap as a sequence of source, metric, matter-coupling, equation, and promotion burdens.",
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
      "The diagram illustrates the claim-gate lifecycle across proposal states, obstructions, freeze discipline, and protected gate boundaries.",
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
      "The diagram illustrates the source-extension path from proposal-only work through audit, stress testing, selector review, and human-gated adoption boundaries.",
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
      "The diagram illustrates how Gate Chair status, human-gated decisions, protected approvals, and validator limits relate to one another.",
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
      "The diagram illustrates the current-state snapshot as a dated view of active task context, handoff context, open burden, blocked claims, and next action.",
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
      "The diagram illustrates how Distance-to-GR ledger inputs, burden labels, blockers, and dashboard grouping feed a public status view.",
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
      "The diagram illustrates the AI system as a chain from request classification through source authority, task records, AgentJobs, validators, and bounded outputs.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-research-agent-system/diagrams/task-authority-review-map.mmd.",
  },
  {
    group: "ai-workflow",
    title: "AI workflow bounded AgentJob chain",
    src: "/assets/diagrams/comprehension/ai-workflow-bounded-agentjob-chain.png",
    alt: "Diagram showing a request flowing through Director decision, AgentJob allowlist, execution, validators, completion, handoff, and bounded PASS.",
    caption:
      "The diagram illustrates how a request moves through Director decision, AgentJob allowlist, execution, validators, completion, handoff, and checked output.",
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
      "The diagram illustrates one AgentJob envelope containing allowed reads, writes, expected outputs, validators, forbidden paths, and stop conditions.",
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
      "The diagram illustrates the role-authority stack from role labels through registry status, execution records, AgentJob allowlists, and validators.",
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
      "The diagram illustrates role authority inspection across the role name, registry row, role contract, execution-role record, AgentJob, validators, and current boundary.",
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
      "The diagram illustrates source-first memory layers from canonical sources through registries, handoffs, generated memory layers, retrieval, and source inspection.",
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
      "The diagram illustrates parent-child synthesis inside one outer AgentJob with one allowlist, one completion record, and one fused output.",
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
      "The diagram illustrates the operations control spine from request intake through Director decision, AgentJob, execution role, validators, completion, and handoff.",
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
      "The diagram illustrates the lifecycle record chain from task row and Director decision through AgentJob evidence, command receipts, completion, and handoff.",
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
      "The diagram illustrates role routing across registered roles, task overlays, execution-role records, AgentJob allowlists, outputs, and validators.",
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
      "The diagram illustrates validator PASS as a flow from changed surface through focused check, receipt evidence, checked state, and handoff context.",
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
      "The diagram illustrates publication review flow from brief and source specification through reader page, screenshots, human review, and manifests.",
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
      "The diagram illustrates project-system improvement as a loop from observed issue through classification, sidecar input, one AgentJob, receipts, and close/defer/reject outcome.",
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
      "The diagram illustrates technical tool tiers across inspection tools, validation tools, browser QA, TeX/PDF tooling, and tool-availability boundaries.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-technical-requirements/diagrams/technical-tool-authority-tiers.mmd.",
  },
  {
    group: "source-authority",
    title: "Source authority ladder",
    src: "/assets/diagrams/comprehension/source-authority-ladder.png",
    alt: "Diagram showing source files and registries upstream from generated derivatives, website pages, and reader orientation.",
    caption:
      "The diagram illustrates the source-authority ladder from source files and registries through generated derivatives, website pages, and reader orientation.",
    provenance:
      "Mermaid source: docs/content-dossiers/source-authority/diagrams/source-authority-ladder.mmd.",
  },
  {
    group: "source-authority",
    title: "Claim boundary explorer",
    src: "/assets/diagrams/comprehension/source-authority-claim-boundary-explorer.png",
    alt: "Diagram showing the claim-boundary registry feeding a checked-in snapshot and public explorer while forbidden overreads remain blocked.",
    caption:
      "The diagram illustrates how claim-boundary registry rows feed checked snapshots and public explorer views while blocked overread paths stay separated.",
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
      "The diagram illustrates the publication provenance system across source basis, route maps, page provenance, source manifests, asset manifests, static build output, and reader routes.",
    provenance:
      "Mermaid source: docs/content-dossiers/source-authority-publication-and-provenance-system/diagrams/publication-provenance-system.mmd.",
  },
  {
    group: "source-authority",
    title: "General-public reading path",
    src: "/assets/diagrams/comprehension/general-public-guided-start.png",
    alt: "Diagram showing a general-public reader moving through Home, current state, source authority, claim boundaries, and provenance without creating new claims.",
    caption:
      "The diagram illustrates a general-public reading path through Home, current state, source authority, claim boundaries, and provenance context.",
    provenance:
      "Mermaid source: docs/content-dossiers/guided-start-general-public/diagrams/general-public-guided-start.mmd.",
  },
  {
    group: "source-authority",
    title: "Audience reading paths",
    src: "/assets/diagrams/comprehension/specialist-guided-starts.png",
    alt:
      "Diagram showing one reading-path hub routing physicists, mathematicians, AI and agent researchers, software and system engineers, and external reviewers to internal prerequisite pages while preserving the no-new-claims boundary.",
    caption:
      "The diagram illustrates audience reading paths for physicists, mathematicians, AI and agent researchers, software and system engineers, and external reviewers.",
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
      "The diagram illustrates the reviewer inspection order from claim boundaries through current state, Distance-to-GR, ontology documents, source inspection, questions, and human review.",
    provenance:
      "Mermaid source: docs/content-dossiers/reviewer-packet/diagrams/reviewer-inspection-order.mmd.",
  },
  {
    group: "physics",
    title: "Metric response ladder",
    src: "/assets/diagrams/comprehension/physics-metric-response-ladder.png",
    alt: "Diagram showing Resp_lc, M_src, MetricData(E), scoped g_eff, matter coupling, Einstein equations, and benchmark promotion as separate ladder objects with blocked overreads.",
    caption:
      "The diagram illustrates the metric-response ladder across response objects, MetricData(E), scoped g_eff, matter coupling, Einstein equations, and benchmark promotion.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-metric-response-ladder/diagrams/metric-response-ladder.mmd.",
  },
  {
    group: "physics",
    title: "Finite toy route freeze",
    src: "/assets/diagrams/comprehension/physics-finite-toy-models.png",
    alt: "Diagram showing a finite toy route moving through selector, draft/control construction, conditional audit, tag-removal stress, frozen negative local route status, and source-extension continuation while blocked overreads remain separate.",
    caption:
      "The diagram illustrates a finite-toy route moving through selector, draft/control construction, conditional audit, tag-removal stress, frozen local status, and source-extension continuation.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-finite-toy-models/diagrams/finite-toy-freeze.mmd.",
  },
  {
    group: "physics",
    title: "No-target-import discipline",
    src: "/assets/diagrams/comprehension/physics-no-target-import-discipline.png",
    alt: "Diagram showing source data entering a source-only factorization check while target topology, target atlas, target metric, benchmark success, and process authority are blocked into fail-closed obstruction labels.",
    caption:
      "The diagram illustrates no-target-import discipline as source data entering factorization checks while target-context imports route to fail-closed obstruction labels.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-no-target-import-discipline/diagrams/no-target-import-discipline.mmd.",
  },
  {
    group: "physics",
    title: "Negative results and frozen routes",
    src: "/assets/diagrams/comprehension/physics-negative-results-and-frozen-routes.png",
    alt: "Diagram showing a failed route becoming a scoped obstruction, obstruction receipt, local freeze or selector route, and preserved evidence while global rejection and downstream promotion remain blocked.",
    caption:
      "The diagram illustrates how a failed route becomes scoped obstruction evidence, an obstruction receipt, a local freeze or selector route, and preserved review context.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-negative-results-and-frozen-routes/diagrams/negative-results-freeze-flow.mmd.",
  },
  {
    group: "source-authority",
    title: "Document manifest chain",
    src: "/assets/diagrams/comprehension/resources-manifest-chain.png",
    alt:
      "Diagram showing source manifest, asset manifest, document index, downloads, hashes, status labels, and no authority creation.",
    caption:
      "The diagram illustrates how source manifests, asset manifests, document routes, downloads, hashes, and status labels organize public documents.",
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
      "The diagram illustrates the TeX/PDF derivative chain from registered TeX source through registry row, generated PDF derivative, website copy, and source inspection download.",
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
      "The diagram illustrates the diagram-publication workflow from Mermaid source through generated PNG, manifest entry, gallery placement, and nearby explanatory prose.",
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

export const diagramGalleryItems = diagramGallerySourceItems.map(withImageDimensions);

type DiagramGalleryItem = (typeof diagramGalleryItems)[number];

const diagramGalleryByTitle = Object.fromEntries(
  diagramGalleryItems.map((item) => [item.title, item]),
) as Record<string, DiagramGalleryItem>;

const requireDiagram = (title: string): DiagramGalleryItem => {
  const diagram = diagramGalleryByTitle[title];
  if (!diagram) {
    throw new Error(`Missing public comprehension diagram: ${title}`);
  }
  return diagram;
};

const withGreenfieldDiagramDefaults = <T extends Record<string, ComprehensionContent>>(
  blocks: T,
): { [K in keyof T]: ComprehensionContent } =>
  Object.fromEntries(
    Object.entries(blocks).map(([key, block]) => [
      key,
      {
        diagramExpandable: true,
        ...block,
      },
    ]),
  ) as { [K in keyof T]: ComprehensionContent };

export const greenfieldRouteDiagramBlocks = withGreenfieldDiagramDefaults({
  home: {
    id: "home-static-diagram",
    eyebrow: "Static diagram",
    title: "Read Home as two tracks under one source-authority boundary.",
    summary:
      "The diagram keeps the physics research lane, AI research-agent workflow, and source-authority spine visible before readers choose a deeper route.",
    diagram: requireDiagram("Home two-track map"),
  },
  physicsTrack: {
    id: "physics-track-static-diagram",
    eyebrow: "Static diagram",
    title: "Read the physics track as status layers, not one promoted claim.",
    summary:
      "The diagram separates ontology, exact-GR benchmark status, derivation burdens, claim gates, and source authority so the route does not collapse orientation into proof.",
    diagram: requireDiagram("Physics track status map"),
  },
  physicsOntology: {
    id: "physics-ontology-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep vocabulary, source authority, and derivation boundaries distinct.",
    summary:
      "The ontology map shows where vocabulary orientation ends and where registered mathematics, benchmark status, and downstream prediction burdens begin.",
    diagram: requireDiagram("Ontology boundary map"),
  },
  physicsExactGrBenchmark: {
    id: "physics-benchmark-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep benchmark compatibility below derivation proof.",
    summary:
      "The benchmark ladder shows exact-GR compatibility, source derivation, and promotion as separate levels with separate evidence burdens.",
    diagram: requireDiagram("Exact-GR benchmark boundary ladder"),
  },
  physicsDerivationRoadmap: {
    id: "physics-roadmap-static-diagram",
    eyebrow: "Static diagram",
    title: "Read the derivation roadmap as a burden ladder.",
    diagramFit: "viewport-contained",
    summary:
      "The ladder names the open sequence from ontology primitives through metric behavior, matter coupling, equations, and benchmark promotion without discharging those burdens.",
    diagram: requireDiagram("Physics derivation burden ladder"),
  },
  physicsOpenBurdens: {
    id: "physics-open-burdens-static-diagram",
    eyebrow: "Static diagram",
    title: "Read open burdens as ledger states, not progress percentages.",
    summary:
      "The dashboard boundary diagram keeps Distance-to-GR ledger rows, blockers, and burden labels visible while preventing a progress-bar interpretation.",
    diagram: requireDiagram("Distance-to-GR dashboard boundary"),
  },
  physicsFlowGeometry: {
    id: "physics-flow-geometry-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep flow-geometry vocabulary below metric promotion.",
    summary:
      "The metric-response ladder is reused here because it illustrates the same protected boundary: geometry terms and response objects do not jump directly to matter coupling, Einstein equations, or GR promotion.",
    diagram: requireDiagram("Metric response ladder"),
  },
  physicsClaimStatus: {
    id: "physics-claim-status-static-diagram",
    eyebrow: "Static diagram",
    title: "Read claim status as a controlled lifecycle.",
    summary:
      "The claim-gates diagram keeps allowed language, blocked overreads, frozen results, open burdens, and human-gated states separated from one another.",
    diagram: requireDiagram("Claim gates lifecycle"),
  },
  aiSystem: {
    id: "ai-system-static-diagram",
    eyebrow: "Static diagram",
    title: "Read the AI research system as task authority, not autonomous proof.",
    summary:
      "The authority map shows request classification, source authority, task records, AgentJobs, validators, and bounded outputs in one controlled chain.",
    diagram: requireDiagram("AI system task authority map"),
  },
  aiWorkflow: {
    id: "ai-workflow-static-diagram",
    eyebrow: "Static diagram",
    title: "Follow one request through one bounded AgentJob chain.",
    summary:
      "The workflow diagram shows the request, Director decision, allowlist, execution, validators, completion, handoff, and bounded PASS scope.",
    diagram: requireDiagram("AI workflow bounded AgentJob chain"),
  },
  aiAgentjobLifecycle: {
    id: "ai-agentjob-lifecycle-static-diagram",
    eyebrow: "Static diagram",
    title: "Read AgentJob lifecycle records as a narrowing chain.",
    summary:
      "The record-chain diagram shows how Director decisions, execution-role evidence, command receipts, completions, and handoffs close one transaction.",
    diagram: requireDiagram("Director and AgentJob record chain"),
  },
  aiRolesAndSchemas: {
    id: "ai-roles-schemas-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep role labels below schema and job authority.",
    diagramFit: "viewport-contained",
    summary:
      "The role stack shows that labels, schemas, execution-role records, AgentJob allowlists, and validators occupy distinct authority layers.",
    diagram: requireDiagram("AI roles authority stack"),
  },
  aiHumanGatedPromotion: {
    id: "ai-human-gated-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep human-gated promotion outside validator authority.",
    summary:
      "The human-gate map shows Gate Chair decisions, protected approvals, claim promotion, automation limits, and validator limits as separate boundaries.",
    diagram: requireDiagram("Gate Chair and human gates"),
  },
  aiValidatorsAndHandoffs: {
    id: "ai-validators-handoffs-static-diagram",
    eyebrow: "Static diagram",
    title: "Read PASS as scoped checked-state evidence.",
    diagramFit: "viewport-contained",
    summary:
      "The validator boundary diagram shows the changed surface, focused check, receipt, PASS scope, handoff, and the no-claim-promotion boundary.",
    diagram: requireDiagram("Validator PASS boundary"),
  },
  aiMemoryPreflight: {
    id: "ai-memory-preflight-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep retrieval below source inspection.",
    diagramFit: "viewport-contained",
    summary:
      "The source-first layers diagram shows memory, generated retrieval layers, registries, handoffs, and source inspection without allowing retrieval to become authority.",
    diagram: requireDiagram("Memory source-first layers"),
  },
  aiProjectSystemImprovement: {
    id: "ai-project-improvement-static-diagram",
    eyebrow: "Static diagram",
    title: "Read project-system improvement as a bounded repair loop.",
    diagramFit: "viewport-contained",
    summary:
      "The improvement diagram shows signal, classification, sidecar input, one AgentJob, evidence receipts, and close/defer/reject outcomes.",
    diagram: requireDiagram("Project-system improvement loop"),
  },
  aiCurrentState: {
    id: "ai-current-state-static-diagram",
    eyebrow: "Static diagram",
    title: "Read current state through task authority and freshness boundaries.",
    summary:
      "The AI authority map is reused here to keep dated snapshots, handoffs, source context, validators, and bounded outputs tied to tracked records.",
    diagram: requireDiagram("AI system task authority map"),
  },
  aiRuntimeRequirements: {
    id: "ai-runtime-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep tool capability separate from authorization.",
    diagramFit: "viewport-contained",
    summary:
      "The technical tiers diagram shows Node, Python, validators, browser checks, build tools, and the boundary that tool availability does not grant permission.",
    diagram: requireDiagram("Technical tool authority tiers"),
  },
  documentsSourceAuthority: {
    id: "documents-source-authority-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep website pages downstream from source authority.",
    diagramFit: "viewport-contained",
    summary:
      "The source-authority ladder shows source files and registries above generated derivatives, public pages, diagrams, and reader orientation.",
    diagram: requireDiagram("Source authority ladder"),
  },
  documentsRegistries: {
    id: "documents-registries-static-diagram",
    eyebrow: "Static diagram",
    title: "Read registries as typed control records.",
    summary:
      "The claim-boundary explorer diagram is reused to show how registry rows feed checked snapshots and public readers while forbidden overreads remain blocked.",
    diagram: requireDiagram("Claim boundary explorer"),
  },
  documentsGeneratedDerivatives: {
    id: "documents-derivatives-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep generated derivatives downstream from source and manifests.",
    summary:
      "The publication-provenance diagram shows source basis, route maps, page provenance, source manifests, asset manifests, static build output, and conflict paths back to source.",
    diagram: requireDiagram("Publication provenance system"),
  },
  documentsRetrievalLayers: {
    id: "documents-retrieval-static-diagram",
    eyebrow: "Static diagram",
    title: "Keep retrieval layers below canonical source inspection.",
    diagramFit: "viewport-contained",
    summary:
      "The source-first memory diagram shows memory, semantic extracts, mirrors, caches, registries, handoffs, and the final source-inspection boundary.",
    diagram: requireDiagram("Memory source-first layers"),
  },
  documentsPublicationProcess: {
    id: "documents-publication-static-diagram",
    eyebrow: "Static diagram",
    title: "Read publication as review flow, not authority promotion.",
    summary:
      "The publication flow diagram shows brief, source spec, reader page, screenshots, human review, manifests, and provenance in one auditable chain.",
    diagram: requireDiagram("Publication review flow"),
  },
  documentsRepositoryMap: {
    id: "documents-repository-map-static-diagram",
    eyebrow: "Static diagram",
    title: "Read repository topology through manifest and source boundaries.",
    summary:
      "The manifest chain is reused here to keep canonical source, public assets, generated derivatives, document routes, and no-authority boundaries visible while reading folder lanes.",
    diagram: requireDiagram("Document manifest chain"),
  },
  documentsSiteBuilderGuide: {
    id: "documents-site-builder-static-diagram",
    eyebrow: "Static diagram",
    title: "Build pages from source bundles through provenance.",
    summary:
      "The publication-provenance diagram shows the source-bundle-first workflow: inspect source, build the route, update manifests, validate, and hand off without strengthening claims.",
    diagram: requireDiagram("Publication provenance system"),
  },
} satisfies Record<string, ComprehensionContent>);

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
    updated: "2026-07-12",
    note: "The Home page is a reader-entry curated synthesis grounded in the public overview, source-authority contract, exact-closure overview, note, and flagship article. Canonical inputs do not make this website route canonical, and the page does not add scientific, mathematical, governance, or workflow authority.",
    sourceRefs: [
      "The AEther Flow Website. (2026). src/pages/index.astro",
      "The AEther Flow Website. (2026). docs/architecture/website-feature-and-functionality.md",
      "AEther-Flow Project. (2026). github-facing/project-overview-explainer.md",
      "AEther-Flow Project. (2026). github-facing/source-authority-explainer.md",
      "AEther-Flow Project. (2026). github-facing/aether-flow-ontology-explainer.md",
      "AEther-Flow Project. (2026). ontology/tex/aether_flow_exact_closure_sequence_overview.tex",
      "AEther-Flow Project. (2026). ontology/tex/aether_flow_exact_closure_note.tex",
      "AEther-Flow Project. (2026). ontology/tex/aether_flow_exact_closure_flagship_article.tex",
      "AEther-Flow Project. (2026). github-facing/gr-derivation-roadmap-explainer.md",
    ],
  },
  physicsTrack: {
    claimStatus: "explanatory track landing",
    updated: "2026-07-12",
    note: "This page is a curated synthesis grounded in the physics-program materials and the exact-closure overview, note, and flagship article. Those canonical inputs do not make the website route canonical; it preserves the open GR-derivation boundary and defers scientific authority upstream.",
    sourceRefs: [
      "AEther-Flow Project. (2026). README.md",
      "AEther-Flow Project. (2026). github-facing/aether-flow-physics-program-explainer.md",
      "AEther-Flow Project. (2026). ontology/tex/aether_flow_exact_closure_sequence_overview.tex",
      "AEther-Flow Project. (2026). ontology/tex/aether_flow_exact_closure_note.tex",
      "AEther-Flow Project. (2026). ontology/tex/aether_flow_exact_closure_flagship_article.tex",
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
    updated: "2026-06-29",
    note: "This page presents a checked-in registry snapshot for reader orientation. It cannot create boundaries, certify claims, execute gates, or promote scientific results.",
    sourceRefs: [
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0323.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0323.md",
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
    note: "This page explains Æther / Æther-flow vocabulary as a current research ontology. It is not an accepted derivation of GR and cannot promote ontology beyond upstream source authority.",
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
    updated: "2026-06-29",
    note: "This page presents a checked-in website snapshot of upstream physics control state. It is not source authority, does not auto-refresh during build, and cannot promote draft/control data into adopted physics claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0323.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0323.md",
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
    updated: "2026-06-29",
    note: "This page organizes a checked-in Distance-to-GR ledger snapshot. It is not a proof surface, progress percentage, live source authority, Gate Chair verdict, or downstream GR promotion.",
    sourceRefs: [
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). research_control/design/mathematical_decisiveness_completion_contract.md",
      "AEther-Flow Project. (2026). research_control/design/obstruction_and_freeze_control.md",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0323.yaml",
      "The AEther Flow Website. (2026). src/data/distance_to_gr_snapshot.json",
      "The AEther Flow Website. (2026). docs/system-analyses/distance-to-gr-dashboard.md",
    ],
  },
  physicsMetricResponseLadder: {
    claimStatus: "metric-response ladder orientation",
    updated: "2026-06-29",
    note: "This page explains checked-in metric-response ladder status. It cannot adopt MetricData(E), expand scoped g_eff, adopt a coupling law, derive matter coupling, derive Einstein equations, promote the benchmark, or complete GR derivation.",
    sourceRefs: [
      "AEther-Flow Project. (2026). registries/DISTANCE_TO_GR_LEDGER.csv",
      "AEther-Flow Project. (2026). registries/CLAIM_BOUNDARY_REGISTRY.csv",
      "AEther-Flow Project. (2026). research_control/design/gr_derivation_burden_map.md",
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0323.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0323.md",
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
    updated: "2026-06-29",
    note: "This page explains Gate Chair and human-gated decision authority for readers. It cannot execute a gate, issue a Gate Chair verdict, treat validators as scientific proof, or promote source-law, MetricData(E), g_eff, matter-coupling, Einstein-equation, benchmark, or downstream GR claims.",
    sourceRefs: [
      "AEther-Flow Project. (2026). research_control/program_state.yaml",
      "AEther-Flow Project. (2026). research_control/handoffs/handoff-0323.yaml",
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
} satisfies Record<string, ProjectSourceNoticeDefaults>;

export const projectPhysicsDeepDiveRoutes = [
  {
    title: "Current physics state",
    href: "/physics/claim-status/",
    phase: "Current snapshot",
    status: "implemented",
    description: "Reviewed source-state snapshot for active task, latest handoff, open burden, blocked claims, and next action.",
  },
  {
    title: "Distance-to-GR dashboard",
    href: "/physics/open-burdens/",
    phase: "PG-002",
    status: "implemented",
    description: "Ledger-backed burden dashboard that rejects progress-bar proof and downstream claim promotion.",
  },
  {
    title: "Metric response ladder",
    href: "/physics/open-burdens/",
    phase: "PG-009",
    status: "implemented",
    description: "Glossary-first ladder for Resp_lc, M_src, MetricData(E), scoped g_eff, matter coupling, equations, and blocked promotions.",
  },
  {
    title: "Finite toy models",
    href: "/physics/open-burdens/",
    phase: "PG-010",
    status: "implemented",
    description: "Controlled finite-model explainer for the explicit-tag frozen negative route and its non-global scope.",
  },
  {
    title: "No-target-import discipline",
    href: "/physics/open-burdens/",
    phase: "PG-011",
    status: "implemented",
    description: "Methodology guardrail for blocking target-context and process-authority imports without claiming completed proof.",
  },
  {
    title: "Negative results and frozen routes",
    href: "/physics/open-burdens/",
    phase: "PG-012",
    status: "implemented",
    description: "Evidence-preservation explainer for scoped obstructions, frozen negative routes, and local freeze boundaries.",
  },
  {
    title: "AEther / AEther-flow ontology",
    href: "/physics/ontology/",
    phase: "Phase 4A",
    status: "implemented",
    description: "Ontology explainer that keeps vocabulary orientation separate from GR derivation.",
  },
  {
    title: "Exact-GR benchmark boundary",
    href: "/physics/exact-gr-benchmark/",
    phase: "Phase 4B",
    status: "implemented",
    description: "Boundary explainer separating benchmark compatibility from first-principles derivation.",
  },
  {
    title: "GR derivation roadmap",
    href: "/physics/derivation-roadmap/",
    phase: "Phase 4C",
    status: "implemented",
    description: "Roadmap explainer for the open derivation burden and its guarded milestones.",
  },
  {
    title: "Source extension pipeline",
    href: "/physics/derivation-roadmap/",
    phase: "PG-003",
    status: "implemented",
    description: "Workflow explainer for proposal-only, audit, stress, selector, and human-gated source-extension preconditions.",
  },
  {
    title: "Gate Chair and human gates",
    href: "/ai-research-system/human-gated-promotion/",
    phase: "PG-004",
    status: "implemented",
    description: "Authority explainer for protected human-gated decisions, Gate Chair status, validator limits, and verdict boundaries.",
  },
  {
    title: "Claim gates and obstructions",
    href: "/physics/claim-status/",
    phase: "Phase 4D",
    status: "implemented",
    description: "Explainer for no-go records, scoped obstructions, freeze discipline, and gates.",
  },
];

export const projectAiDeepDiveRoutes = [
  {
    title: "Research-agent workflow",
    href: "/ai-research-system/workflow/",
    phase: "Phase 5A",
    status: "implemented",
    description: "Request classification, Director decisions, one bounded AgentJob, completion evidence, handoffs, and authority limits.",
  },
  {
    title: "One bounded AgentJob",
    href: "/ai-research-system/agentjob-lifecycle/",
    phase: "PG-015",
    status: "implemented",
    description: "Concrete permission-envelope walkthrough for one auditable AgentJob transaction.",
  },
  {
    title: "Roles and skills",
    href: "/ai-research-system/roles-and-schemas/",
    phase: "Phase 5B",
    status: "implemented",
    description: "Role and skill contract explainer with task-local authority and allowlist boundaries.",
  },
  {
    title: "Role authority inspector",
    href: "/ai-research-system/roles-and-schemas/",
    phase: "PG-017",
    status: "implemented",
    description: "Static inspection stack separating role labels, registry status, execution records, and AgentJob authority.",
  },
  {
    title: "Memory preflight",
    href: "/ai-research-system/memory-preflight/",
    phase: "PG-018",
    status: "implemented",
    description: "Source-first retrieval, memory preflight receipts, registry inspection, and retrieval-layer boundaries.",
  },
  {
    title: "Parent-child synthesis",
    href: "/ai-research-system/workflow/",
    phase: "Phase 5D",
    status: "implemented",
    description: "One-AgentJob perspective-synthesis explainer preserving a single outer authority frame.",
  },
];

export const projectOperationsRoutes = [
  {
    title: "Director and AgentJob lifecycle",
    href: "/ai-research-system/agentjob-lifecycle/",
    phase: "Operations",
    status: "implemented",
    description: "Task, decision, AgentJob, completion, handoff, and registry evidence chain.",
  },
  {
    title: "Role routing",
    href: "/ai-research-system/roles-and-schemas/",
    phase: "Operations",
    status: "implemented",
    description: "Role templates, execution-role records, task overlays, provisional roles, and allowlists.",
  },
  {
    title: "Validator PASS limits",
    href: "/ai-research-system/validators-and-handoffs/",
    phase: "PG-019",
    status: "implemented",
    description: "Why command PASS is checked-state evidence, not theorem proof, claim promotion, role authority, or Gate Chair approval.",
  },
  {
    title: "Publication process",
    href: "/documents/governance/publication-process/",
    phase: "Operations",
    status: "implemented",
    description: "Brief, source spec, public page, screenshot evidence, and review discipline.",
  },
  {
    title: "Project-system improvement",
    href: "/ai-research-system/project-system-improvement/",
    phase: "PG-020",
    status: "implemented",
    description: "Signals, sidecars, classifiers, advisory resolver output, one bounded maintenance packet, and explicit closure evidence.",
  },
  {
    title: "Technical requirements",
    href: "/ai-research-system/runtime-requirements/",
    phase: "Operations",
    status: "implemented",
    description: "Local tool tiers for reproducible operation without confusing tools with authorization.",
  },
];

export const projectSourceAuthorityRoutes = [
  {
    title: "Claim Boundary Explorer",
    href: "/physics/claim-status/",
    phase: "PG-005",
    status: "implemented",
    description: "Source-pinned registry snapshot showing allowed, forbidden, and gate-required wording without certifying claims.",
  },
  {
    title: "Publication And Provenance System",
    href: "/documents/governance/publication-process/",
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
    href: "/physics/",
    matchPrefixes: ["/physics/"],
    children: [
      {
        title: "Physics Overview",
        href: "/physics/",
        description: "Category landing for ontology, benchmark boundaries, derivation roadmap, and open burdens.",
      },
      {
        title: "Ontology",
        href: "/physics/ontology/",
        description: "Plain vocabulary for Æther, Æther-flow, observed space, S-time, expansion, and gravity language.",
      },
      {
        title: "Exact-GR Benchmark",
        href: "/physics/exact-gr-benchmark/",
        description: "Benchmark compatibility boundaries without treating compatibility as derivation.",
      },
      {
        title: "Derivation Roadmap",
        href: "/physics/derivation-roadmap/",
        description: "Open burden map for effective geometry, matter coupling, equations, and benchmark promotion.",
      },
      {
        title: "Flow Geometry",
        href: "/physics/flow-geometry/",
        description: "Geometry-facing explanation constrained by source-bundle evidence.",
      },
      {
        title: "Claim Status",
        href: "/physics/claim-status/",
        description: "Claim gates, obstruction status, frozen routes, and blocked overreads.",
      },
      {
        title: "Open Burdens",
        href: "/physics/open-burdens/",
        description: "Remaining proof, model, and evidence burdens before stronger claims are available.",
      },
    ],
  },
  {
    title: "AI Research System",
    href: "/ai-research-system/",
    matchPrefixes: ["/ai-research-system/"],
    children: [
      {
        title: "System Overview",
        href: "/ai-research-system/",
        description: "Category landing for the governed research workflow and its authority boundaries.",
      },
      {
        title: "Current State",
        href: "/ai-research-system/current-state/",
        description: "Freshness-sensitive research-control status and source-boundary framing.",
      },
      {
        title: "Workflow",
        href: "/ai-research-system/workflow/",
        description: "Request routing, bounded AgentJobs, review discipline, and source-first execution.",
      },
      {
        title: "AgentJob Lifecycle",
        href: "/ai-research-system/agentjob-lifecycle/",
        description: "One job envelope from allowlist through validators, completion, and handoff.",
      },
      {
        title: "Roles and Schemas",
        href: "/ai-research-system/roles-and-schemas/",
        description: "Role labels, schemas, registry records, and job-local authority boundaries.",
      },
      {
        title: "Human-Gated Promotion",
        href: "/ai-research-system/human-gated-promotion/",
        description: "Human review gates for promotion, adoption, and protected decisions.",
      },
      {
        title: "Validators and Handoffs",
        href: "/ai-research-system/validators-and-handoffs/",
        description: "Validator PASS boundaries, completion evidence, and handoff constraints.",
      },
      {
        title: "Memory Preflight",
        href: "/ai-research-system/memory-preflight/",
        description: "Source-first memory and retrieval support without replacing source inspection.",
      },
      {
        title: "Project-System Improvement",
        href: "/ai-research-system/project-system-improvement/",
        description: "Bounded maintenance loops for workflow and tooling improvements.",
      },
      {
        title: "Runtime Requirements",
        href: "/ai-research-system/runtime-requirements/",
        description: "Tool, validator, and environment requirements stated as operational evidence.",
      },
    ],
  },
  {
    title: "Documents",
    href: "/documents/",
    matchPrefixes: ["/documents/"],
    children: [
      {
        title: "Documentation Overview",
        href: "/documents/",
        description: "Document categories, formats, status, authority, provenance, and reading paths.",
      },
      {
        title: "Anthology Articles",
        href: "/documents/anthology/",
        description: "Reader-facing anthology articles published as approved PDF documents.",
      },
      {
        title: "Research Articles",
        href: "/documents/research/",
        description: "Research documents with distinct source and readable derivative roles.",
      },
      {
        title: "Governance & Control",
        href: "/documents/governance/",
        description: "Approved governance and control documents with explicit status and scope.",
      },
      {
        title: "Diagram Gallery",
        href: "/documents/diagrams/",
        description: "Website-local visual aids with explicit provenance and non-authority status.",
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
    href: "/physics/",
    phase: "Phase 2",
    status: "implemented",
    description: "First-class track landing page for ontology, benchmark, open derivation, and obstruction boundaries.",
    sourceNotice: projectSourceNoticeDefaults.physicsTrack,
    plannedChildren: projectPhysicsDeepDiveRoutes,
  },
  {
    title: "AI Research-Agent System",
    href: "/ai-research-system/",
    phase: "Phase 2",
    status: "implemented",
    description: "First-class track landing page for the governed AI-assisted research workflow.",
    sourceNotice: projectSourceNoticeDefaults.aiResearchAgentTrack,
    plannedChildren: projectAiDeepDiveRoutes,
  },
  {
    title: "Operations",
    href: "/ai-research-system/",
    phase: "PRD release",
    status: "implemented",
    description: "Operational route family for lifecycle, role routing, validation, publication, project-system repair, and tool requirements.",
    sourceNotice: projectSourceNoticeDefaults.operationsTrack,
    plannedChildren: projectOperationsRoutes,
  },
  {
    title: "Source Authority",
    href: "/documents/governance/source-authority/",
    phase: "Phase 3 / PG-005",
    status: "implemented",
    description: "Trust and source-boundary page explaining how readers should treat website material, generated derivatives, and claim-boundary snapshots.",
    sourceNotice: projectSourceNoticeDefaults.sourceAuthority,
    plannedChildren: projectSourceAuthorityRoutes,
  },
];

export const projectInformationArchitectureDecision = {
  firstFamilyRoutes: [
    "/physics/",
    "/ai-research-system/",
    "/ai-research-system/",
    "/documents/governance/source-authority/",
  ],
  navigationChange: {
    status: "implemented",
    phase: "Phase 7",
    rationale:
      "Primary navigation now exposes the public project reading path: Home, physics, AI system, operations, source authority, and documents.",
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
