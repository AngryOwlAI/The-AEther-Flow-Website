import type { ComprehensionContent } from "./comprehensionContent";

const sourceLabel = "Source basis";
const routeLabel = "Internal route";

export const operationsComprehension: ComprehensionContent = {
  id: "operations-comprehension",
  eyebrow: "Operations comprehension",
  title: "Operations are the control spine, not scientific authority.",
  summary:
    "The operations family explains how requests become routed decisions, bounded AgentJobs, execution-role evidence, validators, completions, and handoffs.",
  diagram: {
    src: "/assets/diagrams/comprehension/operations-control-spine.png",
    alt:
      "Diagram showing request, Director decision, AgentJob, execution role, validators, completion, handoff, and an operational-evidence-is-not-physics-proof boundary.",
    caption:
      "Static comprehension diagram: operations keep work auditable while preserving source and claim boundaries.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations/diagrams/operations-control-spine.mmd. Manifest id: comprehension_operations_control_spine.",
  },
  mechanismSteps: [
    {
      title: "Route the task",
      body: "A Director decision selects the appropriate lane and records the boundary.",
    },
    {
      title: "Bind the job",
      body: "The AgentJob defines allowed reads, writes, generated outputs, validators, and stop conditions.",
    },
    {
      title: "Preserve evidence",
      body: "Completion, handoff, and registry evidence keep work inspectable without rewriting history.",
    },
  ],
  terms: [
    {
      term: "Operations",
      definition: "The project-control practices that route, execute, validate, publish, improve, and reproduce work.",
      boundary: "Not a scientific result.",
    },
    {
      term: "Completion evidence",
      definition: "A record of outputs, checks, verdict, uncertainty, and next step.",
      boundary: "Not claim promotion.",
    },
    {
      term: "Handoff",
      definition: "A bounded next-step record when work must continue separately.",
      boundary: "Not an extension of the current authority.",
    },
  ],
  boundaries: [
    {
      label: "No source edits",
      title: "Operations pages are explanatory",
      body: "They cannot change routing behavior, validators, roles, publication policy, or physics status.",
    },
    {
      label: "No proof by process",
      title: "Auditability is not theorem proof",
      body: "Strong operations can support trustworthy work without replacing mathematical or scientific source evidence.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Director and AgentJob lifecycle",
      href: "/ai-research-system/agentjob-lifecycle/",
      body: "Read the core record chain.",
    },
    {
      label: routeLabel,
      title: "Validator and operator workflow",
      href: "/ai-research-system/validators-and-handoffs/",
      body: "Read how PASS and command evidence are bounded.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Operations explainer set",
      body:
        "Generated noncanonical upstream explainers for lifecycle, role routing, validation, publication, improvement, and technical requirements.",
    },
  ],
  safeUnsafe: {
    safe:
      "Operations explain how bounded work is routed, executed, checked, recorded, published, and improved without changing source authority.",
    unsafe:
      "Operations pages authorize work, promote claims, prove physics, rewrite activated records, or make validator PASS broader than the checked state.",
  },
};

export const directorAgentjobLifecycleComprehension: ComprehensionContent = {
  id: "director-agentjob-lifecycle-comprehension",
  eyebrow: "Lifecycle comprehension",
  title: "The record chain narrows authority step by step.",
  summary:
    "A task row, Director decision, AgentJob, execution-role evidence, validation, completion, and handoff each answer a smaller operational question.",
  diagram: {
    src: "/assets/diagrams/comprehension/operations-director-agentjob-record-chain.png",
    alt:
      "Diagram showing task row, Director decision, AgentJob, execution-role evidence, command evidence, completion, handoff, and no silent authority expansion.",
    caption:
      "Static comprehension diagram: the lifecycle records why one transaction was authorized and how it closed.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-director-agentjob-lifecycle/diagrams/director-agentjob-record-chain.mmd. Manifest id: comprehension_operations_director_agentjob_record_chain.",
  },
  mechanismSteps: [
    {
      title: "Start with the task",
      body: "The task names the objective, current decision, current job, closure state, and next recommendation.",
    },
    {
      title: "Read the decision",
      body: "The Director decision records selected route, rejected alternatives, claim boundary, and checks.",
    },
    {
      title: "Inspect the AgentJob",
      body: "The job is the executable scope for one transaction.",
    },
  ],
  terms: [
    {
      term: "Task row",
      definition: "The tracked problem statement and state pointer for a piece of work.",
      boundary: "Not permission to act outside its current route.",
    },
    {
      term: "Execution-role evidence",
      definition: "The record binding role semantics to one job.",
      boundary: "Not a reusable authority grant.",
    },
  ],
  boundaries: [
    {
      label: "No mutation",
      title: "Correct by supersession",
      body: "Repair work should create a new bounded packet rather than silently rewriting activated history.",
    },
    {
      label: "No protected gate bypass",
      title: "Gates remain separate",
      body: "Ontology adoption, benchmark promotion, and Gate Chair decisions require their own authority path.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Role routing",
      href: "/ai-research-system/roles-and-schemas/",
      body: "Read how the role layer binds to one transaction.",
    },
    {
      label: routeLabel,
      title: "Parent-child synthesis",
      href: "/ai-research-system/workflow/",
      body: "Read how parallel internal perspectives preserve one outer AgentJob.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Director and AgentJob lifecycle explainer",
      body: "Generated noncanonical upstream explainer: github-facing/director-agentjob-lifecycle-explainer.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "The lifecycle page explains how one bounded task becomes a decision, an AgentJob, evidence, completion, and possibly a handoff.",
    unsafe:
      "A lifecycle diagram expands authority, rewrites activated records, bypasses protected gates, or changes physics status.",
  },
};

export const roleRoutingComprehension: ComprehensionContent = {
  id: "role-routing-comprehension",
  eyebrow: "Role-routing comprehension",
  title: "A role template becomes current only through task-local records.",
  summary:
    "Role routing separates registered role templates, task overlays, provisional roles, execution-role records, AgentJob allowlists, outputs, and validators.",
  diagram: {
    src: "/assets/diagrams/comprehension/operations-role-routing-allowlist-stack.png",
    alt:
      "Diagram showing registered role, task overlay or provisional role, execution-role record, AgentJob allowlist, outputs, validators, and role name is not live permission.",
    caption:
      "Static comprehension diagram: current authority lives in the job-specific allowlist, not in the label alone.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-role-routing/diagrams/role-routing-allowlist-stack.mmd. Manifest id: comprehension_operations_role_routing_allowlist_stack.",
  },
  mechanismSteps: [
    {
      title: "Check role status",
      body: "Use the registry and contract to determine what the role normally means.",
    },
    {
      title: "Check local adaptation",
      body: "Task overlays and provisional roles are bounded to one job unless later registered.",
    },
    {
      title: "Check the allowlist",
      body: "Allowed reads, writes, outputs, validators, and stop conditions control current action.",
    },
  ],
  terms: [
    {
      term: "Role template",
      definition: "A reusable role definition.",
      boundary: "Not current write permission.",
    },
    {
      term: "Provisional role",
      definition: "A temporary one-job role.",
      boundary: "Expires unless explicitly registered.",
    },
    {
      term: "Allowlist",
      definition: "The current transaction's permitted paths and outputs.",
      boundary: "Cannot be expanded by page prose.",
    },
  ],
  boundaries: [
    {
      label: "No permission smuggling",
      title: "Labels do not grant writes",
      body: "Only the current records can authorize a transaction's actual scope.",
    },
    {
      label: "No role registration",
      title: "Public pages cannot change roles",
      body: "The route explains role routing but cannot register, supersede, or expand roles.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Roles and skills",
      href: "/ai-research-system/roles-and-schemas/",
      body: "Reader-facing catalog for roles and governed skills.",
    },
    {
      label: routeLabel,
      title: "Director and AgentJob lifecycle",
      href: "/ai-research-system/agentjob-lifecycle/",
      body: "How one transaction receives its executable boundary.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Role routing explainer",
      body: "Generated noncanonical upstream explainer: github-facing/role-routing-explainer.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "Role routing requires registry status, source contract, execution-role record, AgentJob allowlist, outputs, and validators to be read together.",
    unsafe:
      "A role label, task overlay, provisional role, or public page grants authority outside the current AgentJob.",
  },
};

export const validatorOperatorWorkflowComprehension: ComprehensionContent = {
  id: "validator-operator-comprehension",
  eyebrow: "Validator PASS comprehension",
  title: "PASS is checked-state evidence, not physics proof.",
  summary:
    "The validator/operator route explains how operators choose focused checks, record command evidence, add screenshots for public UI, and avoid turning PASS into theorem proof or claim promotion.",
  diagram: {
    src: "/assets/diagrams/comprehension/operations-validator-pass-boundary.png",
    alt:
      "Diagram showing changed authority surface, focused checks, validator or test, command or screenshot receipt, PASS for checked state, claim-promotion decision, and no theorem, Gate Chair, role, or physics promotion.",
    caption:
      "Static comprehension diagram: PASS is operational checked-state evidence; claim promotion requires separate source and authority paths.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-validator-operator-workflow/diagrams/validator-pass-boundary.mmd. Manifest id: comprehension_operations_validator_pass_boundary.",
  },
  mechanismSteps: [
    {
      title: "Classify the changed surface",
      body: "Different authority surfaces need different validators, tests, documentation-impact receipts, or rendered screenshots.",
    },
    {
      title: "Record evidence",
      body: "Commands, outputs, screenshots, and receipts preserve what was checked and what was not checked.",
    },
    {
      title: "Read PASS narrowly",
      body: "PASS means a named check accepted a checked state, not a broader truth.",
    },
    {
      title: "Route promotion separately",
      body: "Theorem proof, ontology adoption, benchmark promotion, and Gate Chair closure require source evidence and protected authority paths.",
    },
  ],
  terms: [
    {
      term: "Validator",
      definition: "A deterministic repository check.",
      boundary: "Not a scientific judge.",
    },
    {
      term: "Receipt",
      definition: "A durable record of command evidence or review status.",
      boundary: "Not claim promotion by itself.",
    },
    {
      term: "Screenshot evidence",
      definition: "Rendered browser evidence for public UI changes.",
      boundary: "Still requires human comprehension review.",
    },
    {
      term: "Human gate",
      definition: "Explicit protected decision path for claim promotion or closure.",
      boundary: "Cannot be replaced by PASS.",
    },
  ],
  boundaries: [
    {
      label: "No theorem proof",
      title: "PASS does not prove physics",
      body: "Mathematical and scientific claims require source evidence, derivation, and any required gates.",
    },
    {
      label: "No authority expansion",
      title: "Validation does not grant writes",
      body: "A passing check cannot expand role authority or AgentJob scope.",
    },
    {
      label: "No gate shortcut",
      title: "Human-gated decisions stay separate",
      body: "Validators cannot issue Gate Chair approval, adopt ontology, or promote a benchmark.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Technical requirements",
      href: "/ai-research-system/runtime-requirements/",
      body: "Tool tiers needed to reproduce checks.",
    },
    {
      label: routeLabel,
      title: "Publication process",
      href: "/resources/publication-process/",
      body: "How screenshot and review evidence fit public pages.",
    },
    {
      label: routeLabel,
      title: "Gate Chair and human gates",
      href: "/ai-research-system/human-gated-promotion/",
      body: "Why protected scientific decisions remain separate from validation.",
    },
    {
      label: routeLabel,
      title: "Claim-boundary explorer",
      href: "/physics/claim-status/",
      body: "Inspect how allowed and forbidden claim forms are represented for readers.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Validator and operator workflow explainer",
      body: "Generated noncanonical upstream explainer: github-facing/validator-operator-workflow-explainer.md.",
    },
    {
      label: sourceLabel,
      title: "Mathematical decisiveness contract",
      body: "Committed control source: research_control/design/mathematical_decisiveness_completion_contract.md.",
    },
    {
      label: sourceLabel,
      title: "Research control guide",
      body: "Committed control source: research_control/README.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "Validators and tests provide bounded evidence for the surface they checked, with screenshots and receipts where needed; scientific promotion still requires source evidence and any required human gate.",
    unsafe:
      "PASS proves physics, promotes claims, changes roles, replaces human review, resolves unchecked surfaces, or issues Gate Chair approval.",
  },
};

export const publicationProcessComprehension: ComprehensionContent = {
  id: "publication-process-comprehension",
  eyebrow: "Publication comprehension",
  title: "Public readability is downstream from source binding.",
  summary:
    "The publication process begins with a brief and source spec, then produces a page, screenshots, review evidence, provenance, and manifest updates.",
  diagram: {
    src: "/assets/diagrams/comprehension/operations-publication-review-flow.png",
    alt:
      "Diagram showing publication brief, source spec, reader page, screenshots, human review, manifests, and readable page is downstream.",
    caption:
      "Static comprehension diagram: publication improves explanation without changing source authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-publication-process/diagrams/publication-source-review-flow.mmd. Manifest id: comprehension_operations_publication_review_flow.",
  },
  mechanismSteps: [
    {
      title: "Write the brief",
      body: "The brief names audience, reader job, source basis, acceptance criteria, and forbidden implications.",
    },
    {
      title: "Bind the source spec",
      body: "The source basis controls what public copy may explain.",
    },
    {
      title: "Review rendered evidence",
      body: "Screenshots and human review catch public-comprehension failures that commands cannot prove.",
    },
  ],
  terms: [
    {
      term: "Publication brief",
      definition: "A planning surface for reader job, source basis, and acceptance criteria.",
      boundary: "Not source authority by itself.",
    },
    {
      term: "Source spec",
      definition: "The source-boundary contract for a public page.",
      boundary: "Cannot strengthen source claims.",
    },
    {
      term: "Human review",
      definition: "A reviewer judgment that the page teaches the topic without overclaiming.",
      boundary: "Separate from scripted PASS.",
    },
  ],
  boundaries: [
    {
      label: "No generated authority",
      title: "Readable pages stay downstream",
      body: "A polished public page cannot supersede its source files or registries.",
    },
    {
      label: "No validator-only comprehension",
      title: "Human review remains required",
      body: "Scripts can catch missing structure, but not prove reader understanding.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Source authority",
      href: "/resources/source-authority/",
      body: "Trust boundary for source, generated, and website material.",
    },
    {
      label: routeLabel,
      title: "Validator and operator workflow",
      href: "/ai-research-system/validators-and-handoffs/",
      body: "How publication checks and screenshots are interpreted.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Documentation curator publication process explainer",
      body:
        "Generated noncanonical upstream explainer: github-facing/documentation-curator-publication-process-explainer.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "Publication work translates source-bound material into readable pages with screenshots, human review, manifests, and provenance.",
    unsafe:
      "A public page or screenshot changes source authority, proves comprehension by script alone, or promotes source claims.",
  },
};

export const projectSystemImprovementComprehension: ComprehensionContent = {
  id: "project-system-improvement-comprehension",
  eyebrow: "Improvement comprehension",
  title: "Project-system repair is maintenance, not physics continuation.",
  summary:
    "The improvement route starts from observed diff state, registered signals, sidecar input, or repeated workflow problems, then classifies, resolves, executes one bounded packet, receipts, and closes, defers, or rejects explicitly.",
  diagram: {
    src: "/assets/diagrams/comprehension/operations-project-system-improvement-loop.png",
    alt:
      "Diagram showing observed diff or registered signal, classifier, advisory resolver, source-bridged sidecar input, one project-system AgentJob, documentation-impact and PASS evidence, close defer or reject signal, and no hidden physics continuation or signal closure by prose.",
    caption:
      "Static comprehension diagram: project-system improvement repairs research machinery through one bounded packet and explicit evidence.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-project-system-improvement/diagrams/project-system-improvement-loop.mmd. Manifest id: comprehension_operations_project_system_improvement_loop.",
  },
  mechanismSteps: [
    {
      title: "Observe live state",
      body: "Start from a diff, registered signal, repeated failure, source-bridged sidecar, or documented project-system problem.",
    },
    {
      title: "Classify and resolve",
      body: "The classifier names impact and reason codes; the resolver ranks current diff state, open signals, and sidecar context as advisory routing evidence.",
    },
    {
      title: "Execute one packet",
      body: "The selected repair runs as one bounded project-system AgentJob with write-path and claim boundaries.",
    },
    {
      title: "Close with evidence",
      body: "Signals close only with matching PASS completion evidence or a documented rejection decision.",
    },
  ],
  terms: [
    {
      term: "Signal",
      definition: "A tracked project-system problem or improvement indicator.",
      boundary: "Not closed without matching evidence.",
    },
    {
      term: "Sidecar",
      definition: "A project-improvement support artifact generated from qualifying source-bridge evidence.",
      boundary: "Input to routing, not replacement research handoff.",
    },
    {
      term: "Resolver",
      definition: "A mechanism for ranking or choosing the next project-system packet.",
      boundary: "Advisory unless validators or concrete authority violations fail.",
    },
    {
      term: "Documentation impact",
      definition: "Receipt for source and generated-surface impact in state-changing project-system work.",
      boundary: "Operational evidence, not physics status.",
    },
  ],
  boundaries: [
    {
      label: "No hidden physics work",
      title: "Improvement packets stay project-system scoped",
      body: "A maintenance job cannot silently continue a physics derivation.",
    },
    {
      label: "No signal closure by assertion",
      title: "Receipts are required",
      body: "Signals need matching PASS evidence or a documented rejection/defer decision.",
    },
    {
      label: "No global sidecar allowlist",
      title: "Sidecar acceptance is exact-path scoped",
      body: "Conditional sidecar acceptance applies only to the YAML/Markdown pair named by source-bridge metadata.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Director and AgentJob lifecycle",
      href: "/ai-research-system/agentjob-lifecycle/",
      body: "How one bounded job is authorized and closed.",
    },
    {
      label: routeLabel,
      title: "Memory and registries",
      href: "/ai-research-system/memory-preflight/",
      body: "How retrieval drift and generated surfaces remain source-subordinate.",
    },
    {
      label: routeLabel,
      title: "Validator PASS limits",
      href: "/ai-research-system/validators-and-handoffs/",
      body: "Why signal closure evidence remains bounded operational evidence.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Project-system improvement explainer",
      body: "Generated noncanonical upstream explainer: github-facing/project-system-improvement-explainer.md.",
    },
    {
      label: sourceLabel,
      title: "Research control guide",
      body: "Committed control source: research_control/README.md.",
    },
    {
      label: sourceLabel,
      title: "Project-control scripts",
      body: "Committed tooling source: scripts/project_control/README.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "Project-system improvement classifies a live problem, routes one bounded project-system packet, records documentation-impact and PASS evidence, and closes, defers, or rejects signals explicitly.",
    unsafe:
      "A project-system repair silently changes physics route, closes signals without evidence, replaces handoffs, globally allowlists sidecars, or expands role authority.",
  },
};

export const technicalRequirementsComprehension: ComprehensionContent = {
  id: "technical-requirements-comprehension",
  eyebrow: "Tooling comprehension",
  title: "Tool availability supports reproducibility; it is not authorization.",
  summary:
    "Technical requirements explain inspection tools, validation tools, browser rendering, and TeX/PDF derivative tooling while keeping permission in source-control records.",
  diagram: {
    src: "/assets/diagrams/comprehension/operations-technical-tool-tiers.png",
    alt:
      "Diagram showing inspect tools, validation tools, Astro and browser QA, TeX and PDF derivative tools, and tool availability is not authorization.",
    caption:
      "Static comprehension diagram: tools make operations reproducible without deciding whether an operation is allowed.",
    provenance:
      "Mermaid source: docs/content-dossiers/operations-technical-requirements/diagrams/technical-tool-authority-tiers.mmd. Manifest id: comprehension_operations_technical_tool_tiers.",
  },
  mechanismSteps: [
    {
      title: "Match tools to the operation",
      body: "Read-only inspection, Python validation, Astro rendering, and PDF derivative work have different requirements.",
    },
    {
      title: "Run the relevant check",
      body: "Commands provide evidence for the changed surface when the job authorizes that surface.",
    },
    {
      title: "Keep authority separate",
      body: "A working command cannot authorize a write or claim that the job did not permit.",
    },
  ],
  terms: [
    {
      term: "Tool tier",
      definition: "A class of local capability needed for a kind of operation.",
      boundary: "Not permission.",
    },
    {
      term: "Derivative tooling",
      definition: "Tools used to generate human-readable outputs such as PDFs.",
      boundary: "The source file remains authority when registered.",
    },
  ],
  boundaries: [
    {
      label: "No command-as-authority",
      title: "Successful tools do not grant scope",
      body: "Authorization remains in the current records and gates.",
    },
    {
      label: "No dependency policy change",
      title: "The page is descriptive",
      body: "It cannot change repository dependencies, validators, or command semantics.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Validator and operator workflow",
      href: "/ai-research-system/validators-and-handoffs/",
      body: "How command evidence should be chosen and read.",
    },
    {
      label: routeLabel,
      title: "Ontology Documents",
      href: "/resources/documents/",
      body: "How TeX sources and PDF derivatives are exposed for readers.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Technical requirements explainer",
      body: "Generated noncanonical upstream explainer: github-facing/technical-requirements-explainer.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "Technical requirements identify tools needed to inspect, validate, render, or derive artifacts, while authorization remains in task and source-control records.",
    unsafe:
      "Installed tools, passing commands, or local capability authorize work, change dependencies, or promote scientific claims.",
  },
};
