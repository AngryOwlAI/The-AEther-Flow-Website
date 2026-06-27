import type { ComprehensionContent } from "./comprehensionContent";

const sourceLabel = "Source basis";
const routeLabel = "Internal route";

export const aiSystemComprehension: ComprehensionContent = {
  id: "ai-system-comprehension",
  eyebrow: "AI workflow comprehension",
  title: "Read the AI system as governed workflow, not autonomous research authority.",
  summary:
    "The AI research-agent system explains how requests narrow into bounded work, source inspection, role limits, memory support, validators, and human-accountable review.",
  diagram: {
    src: "/assets/diagrams/comprehension/ai-system-task-authority-map.png",
    alt:
      "Diagram showing an AI research-agent request narrowing through classification, one AgentJob, role limits, memory support, review, and a no-physics-proof boundary.",
    caption:
      "Static comprehension diagram: the AI system organizes auditable work without becoming independent physics evidence.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-research-agent-system/diagrams/task-authority-review-map.mmd. Manifest id: comprehension_ai_system_task_authority_map.",
  },
  mechanismSteps: [
    {
      title: "Classify the request",
      body:
        "Decide whether the work is research continuation, project-system repair, documentation, validation, or a stop condition.",
    },
    {
      title: "Bind one transaction",
      body:
        "A Director decision and AgentJob define the allowed reads, writes, outputs, validators, and claim boundary.",
    },
    {
      title: "Use memory as navigation",
      body:
        "Memory and registries can find likely evidence, but source files and registry rows must be inspected before relying on a claim.",
    },
    {
      title: "Preserve human accountability",
      body:
        "Protected publication, authorship, outreach, Gate Chair, and claim-promotion decisions remain explicit human-gated responsibilities.",
    },
  ],
  terms: [
    {
      term: "AI research-agent system",
      definition: "A governed workflow for planning, executing, validating, and preserving research work.",
      boundary: "Not autonomous ownership of scientific decisions.",
    },
    {
      term: "AgentJob",
      definition: "A bounded execution contract for one transaction.",
      boundary: "It cannot silently add objectives or authority.",
    },
    {
      term: "Human accountability",
      definition: "Protected decisions remain assigned to explicit human gates or maintainers.",
      boundary: "Generated output cannot substitute for those gates.",
    },
  ],
  boundaries: [
    {
      label: "No physics proof",
      title: "Workflow evidence is operational",
      body: "The workflow can make research auditable without deriving GR or promoting a benchmark.",
    },
    {
      label: "No role drift",
      title: "Roles stay task-local",
      body: "A role name or skill entry point does not grant write permission without the current AgentJob boundary.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Research-agent workflow",
      href: "/project/ai-research-agent-system/workflow/",
      body: "Read the request-to-AgentJob transaction chain.",
    },
    {
      label: routeLabel,
      title: "Roles and skills",
      href: "/project/ai-research-agent-system/roles-and-skills/",
      body: "Inspect why labels, role contracts, and skills do not grant current authority by themselves.",
    },
    {
      label: routeLabel,
      title: "Memory and registries",
      href: "/project/ai-research-agent-system/memory-registries/",
      body: "Read how retrieval support remains subordinate to tracked sources.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Research-agent workflow explainer",
      body: "Generated noncanonical upstream explainer: github-facing/research-agent-workflow-explainer.md.",
    },
    {
      label: sourceLabel,
      title: "Source authority route",
      href: "/project/source-authority/",
      body: "Internal route explaining how generated explainers, website pages, and source records relate.",
    },
  ],
  safeUnsafe: {
    safe:
      "The AI research-agent system is a governed workflow for bounded, source-inspected, validator-checked research work under human accountability.",
    unsafe:
      "The AI system autonomously owns research decisions, proves physics claims, grants role permissions, or replaces human-gated publication and claim authority.",
  },
};

export const aiWorkflowComprehension: ComprehensionContent = {
  id: "ai-workflow-comprehension",
  eyebrow: "Workflow comprehension",
  title: "A research request becomes one inspectable transaction.",
  summary:
    "The workflow page explains classification, Director decision, AgentJob allowlist, execution evidence, completion, and handoff as a record chain.",
  diagram: {
    src: "/assets/diagrams/comprehension/ai-workflow-bounded-agentjob-chain.png",
    alt:
      "Diagram showing a request flowing through Director decision, AgentJob allowlist, execution, validators, completion, handoff, and a bounded PASS limit.",
    caption:
      "Static comprehension diagram: each workflow record narrows the current transaction instead of broadening authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-workflow/diagrams/bounded-agentjob-chain.mmd. Manifest id: comprehension_ai_workflow_bounded_agentjob_chain.",
  },
  mechanismSteps: [
    {
      title: "Classify before executing",
      body:
        "The request must be sorted into the correct lane before any job can claim authority to read, write, or validate.",
    },
    {
      title: "Bind the allowlist",
      body:
        "The AgentJob names allowed paths, expected outputs, validators, stop conditions, and claim boundaries.",
    },
    {
      title: "Close with evidence",
      body:
        "Completion records command results, changed outputs, verdict, uncertainty, and next recommendation.",
    },
  ],
  terms: [
    {
      term: "Director decision",
      definition: "A routing record that selects one path and may preserve rejected alternatives.",
      boundary: "Not broad future permission.",
    },
    {
      term: "Completion",
      definition: "A record of outputs, checks, verdict, uncertainty, and continuation needs.",
      boundary: "Not claim promotion.",
    },
    {
      term: "Handoff",
      definition: "A separate continuation recommendation when another bounded step is needed.",
      boundary: "Not a silent extension of the current job.",
    },
  ],
  boundaries: [
    {
      label: "One job",
      title: "No hidden second objective",
      body: "A physics job cannot quietly become publication, schema repair, or benchmark promotion.",
    },
    {
      label: "PASS limit",
      title: "Command success is scoped",
      body: "Validator PASS accepts a checked state; it does not prove a theorem or issue a human-gated decision.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Director and AgentJob lifecycle",
      href: "/project/operations/director-agentjob-lifecycle/",
      body: "Operational record chain for decisions, jobs, completions, and handoffs.",
    },
    {
      label: routeLabel,
      title: "Validator and operator workflow",
      href: "/project/operations/validator-operator-workflow/",
      body: "How command evidence and PASS results should be interpreted.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Research-agent workflow explainer",
      body: "Generated noncanonical upstream explainer: github-facing/research-agent-workflow-explainer.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "Research-agent workflow makes one transaction inspectable through classification, a Director decision, one AgentJob, validation evidence, completion, and handoff when needed.",
    unsafe:
      "A workflow page can expand scope, treat PASS as theorem proof, bypass human gates, or let memory and generated pages replace source inspection.",
  },
};

export const aiRolesAndSkillsComprehension: ComprehensionContent = {
  id: "ai-roles-skills-comprehension",
  eyebrow: "Role comprehension",
  title: "Inspect role authority from registry status down to the current allowlist.",
  summary:
    "Roles and skills are useful only when their current status, source contract, execution record, and AgentJob allowlist are read together.",
  diagram: {
    src: "/assets/diagrams/comprehension/ai-roles-authority-stack.png",
    alt:
      "Diagram showing role registry status, contract text, execution-role record, AgentJob allowlist, completion evidence, and a public-catalog-is-not-permission boundary.",
    caption:
      "Static comprehension diagram: role authority is task-local and record-bound.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-roles-and-skills/diagrams/role-authority-stack.mmd. Manifest id: comprehension_ai_roles_authority_stack.",
  },
  mechanismSteps: [
    {
      title: "Start with status",
      body:
        "Check whether a role is active, superseded, provisional, or human-gated before reading it as current.",
    },
    {
      title: "Read the source contract",
      body:
        "The role or skill file defines normal behavior, constraints, outputs, and validation expectations.",
    },
    {
      title: "Apply the current AgentJob",
      body:
        "The live transaction boundary controls actual reads, writes, and outputs for the current job.",
    },
  ],
  terms: [
    {
      term: "Registered role",
      definition: "A versioned role contract recorded in the upstream role registry.",
      boundary: "Not live permission by itself.",
    },
    {
      term: "Task overlay",
      definition: "A one-job adaptation of a role.",
      boundary: "Not a reusable role version unless later registered.",
    },
    {
      term: "Skill",
      definition: "A governed procedure for a class of work.",
      boundary: "Still subordinate to source authority and the current allowlist.",
    },
  ],
  boundaries: [
    {
      label: "No catalog authority",
      title: "Visibility is not permission",
      body: "A public role catalog cannot register, supersede, or activate a role.",
    },
    {
      label: "No gate shortcut",
      title: "Human-gated roles remain protected",
      body: "Gate Chair or claim-promoting authority requires explicit tracked approval.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Role routing",
      href: "/project/operations/role-routing/",
      body: "Operational page for role templates, execution records, task overlays, and allowlists.",
    },
    {
      label: routeLabel,
      title: "Research-agent workflow",
      href: "/project/ai-research-agent-system/workflow/",
      body: "The transaction chain that binds role behavior to one job.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Roles and skills explainer",
      body: "Generated noncanonical upstream explainer: github-facing/roles-and-skills-explainer.md.",
    },
    {
      label: sourceLabel,
      title: "Role routing explainer",
      body: "Generated noncanonical upstream explainer: github-facing/role-routing-explainer.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "Roles and skills help classify and execute work only when registry status, source contract, execution-role record, and current AgentJob allowlist are all respected.",
    unsafe:
      "A role name, skill entry point, public catalog entry, or historical registry row grants current write authority or physics claim authority.",
  },
};

export const aiMemoryRegistriesComprehension: ComprehensionContent = {
  id: "ai-memory-registries-comprehension",
  eyebrow: "Memory comprehension",
  title: "Find with retrieval layers; rely on tracked sources.",
  summary:
    "Memory, registries, wiki notes, semantic extracts, local indexes, and caches accelerate lookup. They remain navigation surfaces unless checked against canonical source records.",
  diagram: {
    src: "/assets/diagrams/comprehension/ai-memory-source-first-layers.png",
    alt:
      "Diagram showing canonical source files and registries upstream from memory, wiki, semantic extracts, inspection, receipts, and a retrieval-is-not-authority boundary.",
    caption:
      "Static comprehension diagram: retrieval layers point back to source authority rather than replacing it.",
    provenance:
      "Mermaid source: docs/content-dossiers/ai-memory-registries/diagrams/source-first-memory-layers.mmd. Manifest id: comprehension_ai_memory_source_first_layers.",
  },
  mechanismSteps: [
    {
      title: "Check freshness",
      body:
        "Memory status and warnings identify retrieval drift; they do not change source authority.",
    },
    {
      title: "Search narrowly",
      body:
        "Use lookup to find likely object IDs, source paths, registry rows, or prior tasks.",
    },
    {
      title: "Inspect the source",
      body:
        "Any claim-affecting use of memory must be confirmed against tracked files or registry rows.",
    },
  ],
  terms: [
    {
      term: "Registry",
      definition: "A tracked CSV source for provenance, source objects, roles, generated outputs, or memory metadata.",
      boundary: "Its meaning is limited to its schema and current row state.",
    },
    {
      term: "Wiki note",
      definition: "A generated retrieval surface derived from source material.",
      boundary: "If it conflicts with a registered source, the source wins.",
    },
    {
      term: "Local cache",
      definition: "Uncommitted or convenience state used for speed.",
      boundary: "Never citation authority.",
    },
  ],
  boundaries: [
    {
      label: "No memory authority",
      title: "Retrieval is not source status",
      body: "Memory hits may guide inspection but cannot authorize routing, claims, or publication by themselves.",
    },
    {
      label: "No silent refresh",
      title: "Derivative drift must be explicit",
      body: "Stale wiki, semantic, Obsidian, or SQLite surfaces require refresh or direct source inspection.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Source authority",
      href: "/project/source-authority/",
      body: "Trust map for sources, derivatives, generated pages, and retrieval aids.",
    },
    {
      label: routeLabel,
      title: "Project-system improvement",
      href: "/project/operations/project-system-improvement/",
      body: "How drift, signals, sidecars, and receipts are routed.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Memory system explainer",
      body: "Generated noncanonical upstream explainer: github-facing/memory-system-explainer.md.",
    },
    {
      label: sourceLabel,
      title: "Source authority explainer",
      body: "Generated noncanonical upstream explainer: github-facing/source-authority-explainer.md.",
    },
  ],
  safeUnsafe: {
    safe:
      "Memory and registries make source lookup faster; claim-affecting work still requires direct inspection of tracked files, registry rows, and current control records.",
    unsafe:
      "A memory hit, wiki note, semantic extract, Obsidian mirror, SQLite index, or local cache overrides tracked source authority.",
  },
};
