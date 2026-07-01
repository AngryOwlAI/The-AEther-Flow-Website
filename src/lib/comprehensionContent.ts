export interface ComprehensionCard {
  label: string;
  title: string;
  body: string;
}

export interface ComprehensionStep {
  title: string;
  body: string;
}

export interface ComprehensionTerm {
  term: string;
  definition: string;
  boundary?: string;
}

export interface ComprehensionDiagram {
  src: string;
  alt: string;
  caption: string;
  provenance: string;
}

export type ComprehensionDiagramFit = "full-width" | "viewport-contained";

export interface ComprehensionLink {
  title: string;
  href?: string;
  body: string;
  label?: string;
}

export interface SafeUnsafeSummary {
  safe: string;
  unsafe: string;
}

export interface ComprehensionEquation {
  expression: string;
  label: string;
  sourceStatus: string;
  assumptions?: string[];
  limits?: string[];
  symbols?: { symbol: string; meaning: string }[];
}

export interface ComprehensionContent {
  id: string;
  eyebrow: string;
  title: string;
  summary: string;
  diagram?: ComprehensionDiagram;
  diagramFit?: ComprehensionDiagramFit;
  diagramExpandable?: boolean;
  diagramNote?: string;
  mechanismSteps?: ComprehensionStep[];
  terms?: ComprehensionTerm[];
  boundaries?: ComprehensionCard[];
  sourceBasis?: ComprehensionLink[];
  relatedRoutes?: ComprehensionLink[];
  equations?: ComprehensionEquation[];
  safeUnsafe?: SafeUnsafeSummary;
}

const sourceLabel = "Source basis";

export const overviewComprehension: ComprehensionContent = {
  id: "project-overview-comprehension",
  eyebrow: "Public comprehension",
  title: "Read the project as two linked tracks under one source-authority spine.",
  summary:
    "Home is the front door. It separates the physics research lane from the governed AI research-agent workflow, then routes readers to source-authority context before any claim is treated as evidence.",
  diagram: {
    src: "/assets/diagrams/comprehension/project-overview-two-track-map.png",
    alt:
      "Diagram showing The AEther Flow Home page as two linked tracks: physics research and AI research-agent workflow, both downstream from source authority.",
    caption:
      "The diagram illustrates Home as two linked tracks, with the physics lane and AI research-agent lane both downstream from the source-authority spine.",
    provenance:
      "Mermaid source: docs/content-dossiers/project-overview/diagrams/two-track-project-map.mmd. Manifest id: comprehension_project_overview_two_track_map.",
  },
  mechanismSteps: [
    {
      title: "Choose the lane",
      body:
        "Use Home to decide whether the question is about physics status, AI research workflow, operations, source authority, or public resources.",
    },
    {
      title: "Read internally first",
      body:
        "Follow the internal route family that explains the reader job before leaving the site for source inspection.",
    },
    {
      title: "Inspect source authority",
      body:
        "Treat GitHub and source links as provenance. Registered sources, registries, and governed records own claim status.",
    },
    {
      title: "Preserve the boundary",
      body:
        "Do not convert overview clarity, a generated page, a diagram, or validator PASS into a stronger scientific or workflow claim.",
    },
  ],
  terms: [
    {
      term: "Physics lane",
      definition:
        "The route family for ontology, exact-GR benchmark boundary, open derivation burden, current state, and claim gates.",
      boundary: "It does not assert that a first-principles GR derivation is complete.",
    },
    {
      term: "AI research-agent lane",
      definition:
        "The governed workflow for tasks, roles, AgentJobs, validation, memory, completions, and handoffs.",
      boundary: "It organizes research work; it does not own scientific decisions.",
    },
    {
      term: "Source-authority spine",
      definition:
        "The rule that source files, registries, and governed records own claims while the website explains them.",
      boundary: "Website clarity does not promote source status.",
    },
    {
      term: "Validator PASS",
      definition: "A deterministic check accepted the checked state.",
      boundary: "It is not a scientific verdict or proof of public comprehension.",
    },
  ],
  boundaries: [
    {
      label: "Physics",
      title: "Benchmark is not derivation",
      body:
        "Exact-GR benchmark compatibility and first-principles substrate derivation remain separate claims.",
    },
    {
      label: "Workflow",
      title: "AI workflow is not physics proof",
      body:
        "Tasks, roles, AgentJobs, validators, and memory make work auditable without replacing scientific sources.",
    },
    {
      label: "Publication",
      title: "Generated surfaces stay downstream",
      body:
        "Website pages, diagrams, screenshots, and generated explainers orient readers but do not become canonical authority.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Project Home explainer",
      body:
        "Generated noncanonical upstream explainer: github-facing/project-overview-explainer.md.",
    },
    {
      label: sourceLabel,
      title: "Source authority page",
      href: "/resources/source-authority/",
      body: "Internal trust-boundary route for source records, generated surfaces, and derivatives.",
    },
  ],
  safeUnsafe: {
    safe:
      "The AEther Flow is a source-first research project with a physics program and a governed research-agent workflow; Home helps readers choose the right internal route and source lane.",
    unsafe:
      "Home proves a substrate derivation, makes generated website material authoritative, grants role or validator authority, or turns the AI workflow into autonomous scientific ownership.",
  },
};

export const parentChildComprehension: ComprehensionContent = {
  id: "parent-child-comprehension",
  eyebrow: "One outer AgentJob",
  title: "Parent-child synthesis adds internal perspectives, not extra authority.",
  summary:
    "The pattern keeps one Director decision, one outer AgentJob, one execution-role record, one completion record, and one fused output. Child outputs are supporting draft/control artifacts inside that frame.",
  diagram: {
    src: "/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png",
    alt:
      "Diagram showing one outer AgentJob containing parent review, child draft/control perspectives, conflict review, and one fused output.",
    caption:
      "The diagram illustrates parent-child synthesis inside one outer AgentJob, including parent review, child draft/control perspectives, conflict review, and one fused output.",
    provenance:
      "Mermaid source: docs/content-dossiers/parent-child-synthesis/diagrams/single-outer-agentjob-frame.mmd. Manifest id: comprehension_parent_child_single_outer_agentjob.",
  },
  mechanismSteps: [
    {
      title: "Authorize one outer frame",
      body:
        "A single Director decision and outer AgentJob own the read paths, write paths, validators, expected outputs, and stop conditions.",
    },
    {
      title: "Use child perspectives as draft/control support",
      body:
        "Child units inspect the problem from bounded angles. Their outputs do not become independent role records or verdicts.",
    },
    {
      title: "Review conflicts before PASS",
      body:
        "A declared blocking conflict must be reviewed and resolved within the policy, or the job remains blocked.",
    },
    {
      title: "Fuse one downstream output",
      body:
        "The parent fuses shared consensus, unique contributions, and remaining limits into one final artifact for completion and handoff.",
    },
  ],
  terms: [
    {
      term: "Outer AgentJob",
      definition:
        "The single executable contract that owns the current transaction's reads, writes, validators, expected outputs, and stop conditions.",
      boundary: "Child perspectives cannot add a second job.",
    },
    {
      term: "Child unit",
      definition: "An analytical perspective used to inspect one problem from a specific angle.",
      boundary: "Its output is supporting draft/control, not an independent verdict.",
    },
    {
      term: "Fused output",
      definition:
        "The one final artifact used for completion, handoff, and downstream reference.",
      boundary: "Supporting drafts do not replace it.",
    },
    {
      term: "Blocking conflict",
      definition:
        "A declared disagreement that must be reviewed and resolved or leave the job blocked.",
      boundary: "PASS is invalid while it remains unresolved.",
    },
  ],
  boundaries: [
    {
      label: "No extra jobs",
      title: "The external control record stays singular",
      body:
        "The mode preserves one Director decision, one outer AgentJob, one execution-role record, one completion record, and one fused output.",
    },
    {
      label: "No independent verdicts",
      title: "Children inherit authority",
      body:
        "Child perspectives inherit the same claim boundary, source restrictions, allowlist, validators, human-gate status, and stop conditions.",
    },
    {
      label: "No conflict bypass",
      title: "Blocking conflicts must be resolved",
      body:
        "A parent cannot select a convenient child and ignore a declared blocking disagreement while still claiming PASS.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Parent-child synthesis explainer",
      body:
        "Generated noncanonical upstream explainer: github-facing/parent-child-synthesis-explainer.md.",
    },
    {
      label: sourceLabel,
      title: "Director and AgentJob lifecycle",
      href: "/ai-research-system/agentjob-lifecycle/",
      body: "Internal route explaining the operational record chain this mode must preserve.",
    },
  ],
  safeUnsafe: {
    safe:
      "Parent-child synthesis is an internal perspective structure inside one physics AgentJob; child outputs support parent review, and only the fused output enters completion and downstream references.",
    unsafe:
      "Parent-child synthesis creates extra jobs, extra role records, extra write authority, independent child verdicts, a path around conflict review, or a mandatory mode for all non-physics work.",
  },
};

export const physicsTrackComprehension: ComprehensionContent = {
  id: "physics-track-comprehension",
  eyebrow: "Physics comprehension",
  title: "Keep ontology, benchmark, derivation burden, and claim gates separate.",
  summary:
    "The physics track is intentionally conservative. It explains an AEther-flow ontology and exact-GR benchmark discipline while keeping first-principles derivation, downstream burdens, negative results, and protected gates distinct.",
  diagram: {
    src: "/assets/diagrams/comprehension/physics-track-status-map.png",
    alt:
      "Diagram showing the physics track as separate ontology, exact-GR benchmark, derivation burden, negative-result, and human-gate layers.",
    caption:
      "The diagram illustrates the physics track as separate ontology, exact-GR benchmark, derivation burden, negative-result, and human-gate layers.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-track/diagrams/status-layer-map.mmd. Manifest id: comprehension_physics_track_status_map.",
  },
  mechanismSteps: [
    {
      title: "Name the layer",
      body:
        "Ask whether the sentence is about ontology vocabulary, benchmark behavior, source-side derivation, a negative result, or a protected gate.",
    },
    {
      title: "Check the source status",
      body:
        "Use registered sources, burden maps, ledgers, and claim-boundary records before treating a summary as evidence.",
    },
    {
      title: "Preserve open burdens",
      body:
        "Metric construction, matter coupling, Einstein equations, and benchmark promotion remain separate downstream obligations.",
    },
  ],
  terms: [
    {
      term: "Exact-GR benchmark",
      definition: "The conservative observable-scale reference behavior remains ordinary GR.",
      boundary: "Benchmark discipline is not a first-principles derivation.",
    },
    {
      term: "Derivation burden",
      definition:
        "The source-side obligation to recover metric behavior, matter coupling, equations, and promotion without target import.",
      boundary: "Open burdens stay open until source authority and gates close them.",
    },
    {
      term: "Scoped obstruction",
      definition: "A specific route failed under stated assumptions or source data.",
      boundary: "It is not global theory rejection.",
    },
  ],
  boundaries: [
    {
      label: "No derivation claim",
      title: "GR is not derived by this route",
      body:
        "The physics landing page orients readers but cannot complete the source-to-GR bridge.",
    },
    {
      label: "No validator proof",
      title: "Checks are not physics evidence",
      body:
        "Validator success can support bounded repository state, not metric, coupling, equation, or benchmark claims.",
    },
  ],
  safeUnsafe: {
    safe:
      "AEther Flow is a benchmark-disciplined physics research program that preserves exact GR operationally while testing whether source-side substrate structure can earn a derivation.",
    unsafe:
      "AEther Flow has already derived GR, public explainers certify benchmark recovery, or a scoped obstruction proves the whole ontology false.",
  },
};

export const physicsOntologyComprehension: ComprehensionContent = {
  id: "physics-ontology-comprehension",
  eyebrow: "Ontology comprehension",
  title: "Ontology names the model vocabulary; mathematics and prediction remain separate.",
  summary:
    "AEther-flow ontology supplies vocabulary for a proposed deeper substrate, ordered motion, observed space, time-language, and expansion-language. It does not by itself force the exact-GR benchmark.",
  diagram: {
    src: "/assets/diagrams/comprehension/physics-ontology-boundary-map.png",
    alt:
      "Diagram separating AEther-flow ontology vocabulary from mathematical bridge work, exact-GR benchmark status, and empirical prediction.",
    caption:
      "The diagram illustrates AEther-flow ontology vocabulary, mathematical bridge work, exact-GR benchmark status, and empirical prediction as separate layers.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-ontology/diagrams/ontology-boundary-map.mmd. Manifest id: comprehension_physics_ontology_boundary_map.",
  },
  mechanismSteps: [
    {
      title: "Use the terms carefully",
      body:
        "AEther and AEther-flow refer to the project's deeper-substrate vocabulary, not to an ordinary fluid moving through observed space.",
    },
    {
      title: "Ask for the bridge",
      body:
        "A stronger claim needs source-side mathematics that recovers observer structure, metric behavior, matter coupling, and closure.",
    },
    {
      title: "Keep prediction downstream",
      body:
        "Empirical prediction requires a completed mathematical model and source authority, not generated public documentation.",
    },
  ],
  terms: [
    {
      term: "AEther",
      definition: "A proposed deeper four-dimensional substrate in this ontology.",
      boundary: "Not an ordinary three-dimensional medium in observed space.",
    },
    {
      term: "AEther-flow",
      definition: "Intrinsic ordered motion of that proposed substrate.",
      boundary: "Not a directly observed wind, river, or current.",
    },
    {
      term: "Observed space",
      definition: "The observer-accessible local appearance of the deeper substrate.",
      boundary: "Not the full underlying ontology.",
    },
    {
      term: "S-time",
      definition: "Experienced order of change involving matter, light, and AEther-flow.",
      boundary: "Not a second place-like corridor or mathematical closure by itself.",
    },
    {
      term: "Observed expansion",
      definition: "Three-dimensional appearance of deeper four-dimensional ordered motion.",
      boundary: "Not a claim that measured expansion is unreal.",
    },
  ],
  boundaries: [
    {
      label: "No ontology promotion",
      title: "Vocabulary is not adoption",
      body:
        "The page can explain the ontology lane without promoting it beyond upstream source authority.",
    },
    {
      label: "No GR forcing",
      title: "Conceptual fit is not derivation",
      body:
        "The ontology still needs source-side mathematics before benchmark recovery can be claimed.",
    },
  ],
  safeUnsafe: {
    safe:
      "AEther-flow ontology names a deeper four-dimensional substrate and ordered motion, while the project still requires source-side mathematics and gates before claiming a first-principles derivation of GR.",
    unsafe:
      "AEther-flow ontology has already forced GR, generated pages certify ontology promotion, or AEther-flow is an ordinary fluid moving through observed three-dimensional space.",
  },
};

export const physicsBenchmarkComprehension: ComprehensionContent = {
  id: "physics-benchmark-comprehension",
  eyebrow: "Benchmark comprehension",
  title: "Adoption, compatibility, derivation, and promotion are different claim states.",
  summary:
    "The exact-GR benchmark keeps public observable-scale behavior ordinary while the substrate derivation remains open. Matching a benchmark is weaker than deriving it from source ontology, and public pages must not collapse either state into promotion.",
  diagram: {
    src: "/assets/diagrams/comprehension/physics-benchmark-boundary-ladder.png",
    alt:
      "Diagram showing benchmark adoption, ontology compatibility, source-side derivation, and human-gated benchmark promotion as separate claim states.",
    caption:
      "The diagram illustrates benchmark adoption, ontology compatibility, source-side derivation, and human-gated benchmark promotion as separate claim states.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-exact-gr-benchmark/diagrams/benchmark-boundary-ladder.mmd. Manifest id: comprehension_physics_benchmark_boundary_ladder.",
  },
  mechanismSteps: [
    {
      title: "Read the conservative answer",
      body:
        "At observable scale, the public benchmark keeps one operative Lorentzian metric, universal matter coupling, and ordinary causal structure.",
    },
    {
      title: "Do not infer source derivation",
      body:
        "A benchmark can be adopted operationally before a source-side substrate derivation is completed.",
    },
    {
      title: "Reserve promotion for gates",
      body:
        "Benchmark promotion depends on upstream authority and protected gate decisions, not reader-facing prose.",
    },
  ],
  terms: [
    {
      term: "Adoption",
      definition: "Taking ordinary GR behavior over as the observable-scale benchmark.",
      boundary: "Not benchmark promotion from a completed source derivation.",
    },
    {
      term: "Compatibility",
      definition: "Holding ontology language beside the benchmark without contradiction.",
      boundary: "Weaker than derivation.",
    },
    {
      term: "Derivation",
      definition: "Source-side mathematics that recovers metric behavior, matter coupling, equations, and closure.",
      boundary: "Not established by benchmark matching or public explanation.",
    },
    {
      term: "Promotion",
      definition: "A protected source-authority change after burdens and gates are satisfied.",
      boundary: "Generated website prose cannot issue it.",
    },
  ],
  boundaries: [
    {
      label: "No empirical deviation",
      title: "The benchmark remains ordinary GR",
      body:
        "The page does not announce an observable deviation from general relativity.",
    },
    {
      label: "No source-to-metric claim",
      title: "g_eff remains upstream",
      body:
        "This boundary page does not construct g_eff, matter coupling, or field equations.",
    },
  ],
  safeUnsafe: {
    safe:
      "AEther Flow keeps ordinary GR as an exact operational benchmark while the substrate derivation remains open and claim-gated.",
    unsafe:
      "The public page, ontology note, or a generated derivative proves GR from AEther-flow.",
  },
};

export const physicsRoadmapComprehension: ComprehensionContent = {
  id: "physics-roadmap-comprehension",
  eyebrow: "Roadmap comprehension",
  title: "The roadmap names burdens; it does not discharge them.",
  summary:
    "The GR derivation roadmap tracks separate source ontology, localization, response, manifold, metric, matter-coupling, equation, finite-toy, and benchmark-promotion burdens.",
  diagram: {
    src: "/assets/diagrams/comprehension/physics-roadmap-burden-ladder.png",
    alt:
      "Diagram showing the GR derivation roadmap as a burden ladder from source ontology through g_eff, matter coupling, Einstein equations, and benchmark promotion.",
    caption:
      "The diagram illustrates the GR derivation roadmap as a burden ladder from source ontology through g_eff, matter coupling, Einstein equations, and benchmark promotion.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-gr-derivation-roadmap/diagrams/burden-ladder.mmd. Manifest id: comprehension_physics_roadmap_burden_ladder.",
  },
  mechanismSteps: [
    {
      title: "Locate the burden row",
      body:
        "A roadmap row names a required object, status category, evidence path, and accept or freeze criterion.",
    },
    {
      title: "Check payload and gate",
      body:
        "A future physics job must name its target milestone and mathematical payload; protected decisions remain human-gated.",
    },
    {
      title: "Keep downstream blocked",
      body:
        "g_eff, matter coupling, Einstein equations, and benchmark promotion cannot be inferred from earlier rows.",
    },
  ],
  terms: [
    {
      term: "Distance-to-GR ledger",
      definition: "Persistent control ledger for derivation burdens and statuses.",
      boundary: "Not independent physics proof outside its cited evidence.",
    },
    {
      term: "Frozen negative",
      definition: "A route should not be repeated without new payload, redesign, or gate action.",
      boundary: "Not global ontology rejection.",
    },
    {
      term: "Mathematical payload",
      definition: "A definition, lemma, theorem, model, witness, obstruction, or other source-side artifact named by a physics completion.",
      boundary: "Payload naming does not make the payload accepted.",
    },
  ],
  boundaries: [
    {
      label: "No g_eff adoption",
      title: "Metric construction remains controlled",
      body:
        "The roadmap names the metric milestone but does not adopt g_eff or MetricData(E).",
    },
    {
      label: "No downstream GR",
      title: "Later burdens remain independent",
      body:
        "Matter coupling, Einstein equations, and benchmark promotion require their own source-side evidence.",
    },
  ],
  safeUnsafe: {
    safe:
      "The GR derivation roadmap tracks separate source ontology, localization, response, manifold, metric, matter-coupling, equation, finite-toy, and benchmark-promotion burdens while preserving draft/control and human-gated boundaries.",
    unsafe:
      "AEther Flow has derived GR, M_src or g_eff is adopted, validator passes are physics evidence, or a scoped freeze label proves the whole ontology false.",
  },
};

export const physicsClaimGatesComprehension: ComprehensionContent = {
  id: "physics-claim-gates-comprehension",
  eyebrow: "Claim-gate comprehension",
  title: "Claim gates make each result narrower, not broader.",
  summary:
    "Proposals, audits, stress tests, completions, handoffs, freeze labels, and human gates each authorize narrower language than a tempting public summary usually wants to use.",
  diagram: {
    src: "/assets/diagrams/comprehension/physics-claim-gates-lifecycle.png",
    alt:
      "Diagram showing proposal, audit, stress test, completion, handoff, freeze, and human gate states with separate allowed claim scopes.",
    caption:
      "The diagram illustrates claim control across proposal, audit, stress test, completion, handoff, freeze, and human gate states.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-claim-gates/diagrams/claim-gates-lifecycle.mmd. Manifest id: comprehension_physics_claim_gates_lifecycle.",
  },
  mechanismSteps: [
    {
      title: "Classify the state",
      body:
        "Decide whether a result is proposal, audit, refutation, completion, handoff, freeze, or protected gate.",
    },
    {
      title: "Read the allowed claim",
      body:
        "Use the claim-boundary registry pattern to keep transaction statements narrower than public overclaims.",
    },
    {
      title: "Preserve negative value",
      body:
        "A failed or frozen route can be useful evidence without becoming global no-go or hidden success.",
    },
  ],
  terms: [
    {
      term: "Human gate",
      definition: "A protected decision path for adoption, promotion, or Gate Chair approval.",
      boundary: "Validators and generated pages cannot auto-promote it.",
    },
    {
      term: "Scoped obstruction",
      definition: "A route-local failure under stated assumptions.",
      boundary: "Not a global no-go theorem.",
    },
    {
      term: "Validator pass",
      definition: "A repository control check accepted a bounded state.",
      boundary: "Not physics proof.",
    },
  ],
  boundaries: [
    {
      label: "No Gate Chair shortcut",
      title: "Protected verdicts require explicit authority",
      body:
        "Generated documentation, role labels, and validators cannot issue Gate Chair approval.",
    },
    {
      label: "No global inflation",
      title: "Negative results remain scoped",
      body:
        "Freeze labels and stress failures do not reject the entire ontology or prove future work impossible.",
    },
  ],
  safeUnsafe: {
    safe:
      "AEther Flow preserves proposals, audits, refutations, stress tests, completions, handoffs, freeze labels, and human gates so each claim stays scoped to its source evidence and authority boundary.",
    unsafe:
      "A frozen route proves the whole theory false, validators prove physics, generated documentation can promote claims, or Gate Chair approval occurred without an explicit human-gated record.",
  },
};

export const physicsCurrentStateComprehension: ComprehensionContent = {
  id: "physics-current-state-comprehension",
  eyebrow: "Current-state comprehension",
  title: "A snapshot reports source state; it does not refresh or promote claims.",
  summary:
    "The current-state page presents checked-in upstream control data for readers. It must preserve snapshot date, drift limits, blocked claims, and the distinction between scoped evidence/precondition acceptance and downstream GR promotion.",
  diagram: {
    src: "/assets/diagrams/comprehension/physics-current-state-snapshot-boundary.png",
    alt:
      "Diagram showing upstream control state flowing into a checked-in website snapshot with blocked downstream claims preserved.",
    caption:
      "The diagram illustrates upstream control state flowing into a checked-in website snapshot, with blocked downstream claim paths shown alongside it.",
    provenance:
      "Mermaid source: docs/content-dossiers/physics-current-state/diagrams/snapshot-boundary.mmd. Manifest id: comprehension_physics_current_state_snapshot_boundary.",
  },
  mechanismSteps: [
    {
      title: "Read the refresh date",
      body:
        "The page imports a checked-in JSON snapshot; normal Astro builds do not silently read the upstream source repo.",
    },
    {
      title: "Preserve blocked claims",
      body:
        "No source-law adoption, MetricData(E) adoption, g_eff scope change, matter-coupling adoption, Einstein equations, or benchmark promotion follows from the snapshot.",
    },
    {
      title: "Use pinned provenance",
      body:
        "Pinned source links support inspection while the website page remains downstream presentation.",
    },
  ],
  terms: [
    {
      term: "Checked-in snapshot",
      definition: "A JSON copy of selected upstream control state committed to the website repo.",
      boundary: "Not a live source authority surface.",
    },
    {
      term: "Blocked claim",
      definition: "A claim explicitly not authorized by the current source state.",
      boundary: "It must not be softened into implied progress.",
    },
    {
      term: "Gate readiness",
      definition: "A selector or source record may route evidence to a future protected review.",
      boundary: "Not a Gate Chair verdict, coupling-law adoption, matter-coupling adoption, or downstream GR promotion.",
    },
  ],
  boundaries: [
    {
      label: "No auto-refresh",
      title: "Builds do not update source state",
      body:
        "Snapshot drift must be handled by the curator workflow and explicit refresh, not assumed away.",
    },
    {
      label: "No promotion",
      title: "Draft/control stays draft/control",
      body:
        "The snapshot cannot promote MetricData(E), g_eff scope change, matter coupling, equations, or benchmark status.",
    },
  ],
  safeUnsafe: {
    safe:
      "The current-state page is a checked-in website snapshot of upstream physics control state with blocked downstream claims preserved.",
    unsafe:
      "The website snapshot auto-refreshes, adopts draft/control data, adopts a coupling law, adopts matter coupling, derives Einstein equations, or promotes the benchmark.",
  },
};
