import type { ComprehensionContent } from "./comprehensionContent";
import { parentChildComprehension } from "./comprehensionContent";
import {
  directorAgentjobLifecycleComprehension,
  operationsComprehension,
  projectSystemImprovementComprehension,
  publicationProcessComprehension,
  roleRoutingComprehension,
  technicalRequirementsComprehension,
  validatorOperatorWorkflowComprehension,
} from "./operationsComprehensionContent";

export interface ExplainerCard {
  label: string;
  title: string;
  body: string;
}

export interface ExplainerSection {
  eyebrow: string;
  title: string;
  body: string;
  cards: ExplainerCard[];
}

export interface ExplainerLink {
  title: string;
  href: string;
  body: string;
}

export interface InternalExplainer {
  title: string;
  eyebrow: string;
  description: string;
  lead: string;
  actionHref: string;
  actionLabel: string;
  secondaryHref: string;
  secondaryLabel: string;
  visualTitle: string;
  visualCaption: string;
  boundaryLabel: string;
  boundaryTitle: string;
  boundaryBody: string;
  claimStatus: string;
  updated: string;
  sourceRefs: string[];
  sections: ExplainerSection[];
  relatedLinks: ExplainerLink[];
  sourceLinks: ExplainerLink[];
  comprehension?: ComprehensionContent;
}

const upstream = (path: string) =>
  `https://github.com/AngryOwlAI/The-AEther-Flow/blob/main/${path}`;

const upstreamRef = (path: string) => `AEther-Flow Project. (2026). ${path}`;

export const operationsLinks: ExplainerLink[] = [
  {
    title: "Director and AgentJob lifecycle",
    href: "/ai-research-system/agentjob-lifecycle/",
    body: "How tasks narrow into decisions, jobs, completions, handoffs, and registry evidence.",
  },
  {
    title: "Role routing",
    href: "/ai-research-system/roles-and-schemas/",
    body: "Why role names are templates, while execution records and AgentJobs control one transaction.",
  },
  {
    title: "Validator and operator workflow",
    href: "/ai-research-system/validators-and-handoffs/",
    body: "How checks, receipts, screenshots, and PASS results should be interpreted.",
  },
  {
    title: "Publication process",
    href: "/resources/publication-process/",
    body: "How public explainers move from brief to source spec, page, screenshots, and review.",
  },
  {
    title: "Project-system improvement",
    href: "/ai-research-system/project-system-improvement/",
    body: "How classifiers, signals, sidecars, receipts, and one bounded AgentJob structure repairs.",
  },
  {
    title: "Technical requirements",
    href: "/ai-research-system/runtime-requirements/",
    body: "Local tool tiers for reproducible operation without confusing tools with authorization.",
  },
];

const directorLifecycleSourceRefs = [
  upstreamRef("github-facing/director-agentjob-lifecycle-explainer.md"),
  upstreamRef("research_control/README.md"),
  upstreamRef("research_control/AGENTS.md"),
  upstreamRef(".agents/schemas/DIRECTOR_DECISION_SCHEMA.md"),
  upstreamRef(".agents/schemas/AGENT_JOB_SCHEMA.md"),
  upstreamRef(".agents/schemas/EXECUTION_ROLE_SCHEMA.md"),
  upstreamRef("registries/DIRECTOR_DECISION_REGISTRY.csv"),
  upstreamRef("registries/AGENT_JOB_REGISTRY.csv"),
  upstreamRef("registries/ROLE_EXECUTION_REGISTRY.csv"),
];

const roleRoutingSourceRefs = [
  upstreamRef("github-facing/role-routing-explainer.md"),
  upstreamRef("github-facing/roles-and-skills-explainer.md"),
  upstreamRef("research_control/README.md"),
  upstreamRef("registries/AGENT_ROLE_REGISTRY.csv"),
  upstreamRef("registries/ROLE_EXECUTION_REGISTRY.csv"),
  upstreamRef(".agents/schemas/ROLE_SCHEMA.md"),
  upstreamRef(".agents/schemas/EXECUTION_ROLE_SCHEMA.md"),
];

const publicationProcessSourceRefs = [
  upstreamRef("github-facing/documentation-curator-publication-process-explainer.md"),
  upstreamRef("research_control/design/documentation_curator_publication_process.md"),
  upstreamRef(".agents/roles/research_ops/documentation-curator.v2.0.0.md"),
  upstreamRef("markdown/publication-briefs/README.md"),
  upstreamRef("registries/PUBLICATION_BRIEF_REGISTRY.csv"),
  upstreamRef("scripts/validate_publication_process.py"),
  upstreamRef("research_control/tasks/RT-20260618-007/artifacts/publication_process_requirement_audit.md"),
  upstreamRef("research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md"),
];

const technicalRequirementsSourceRefs = [
  upstreamRef("github-facing/technical-requirements-explainer.md"),
  upstreamRef("README.md"),
  upstreamRef("AGENTS.md"),
  upstreamRef("research_control/README.md"),
  upstreamRef("requirements.txt"),
  upstreamRef("Makefile"),
  upstreamRef("scripts/README.md"),
  upstreamRef("tests/README.md"),
];

const operationsSourceRefs = [
  ...directorLifecycleSourceRefs,
  ...roleRoutingSourceRefs,
  upstreamRef("github-facing/validator-operator-workflow-explainer.md"),
  ...publicationProcessSourceRefs,
  upstreamRef("github-facing/project-system-improvement-explainer.md"),
  ...technicalRequirementsSourceRefs,
];

const operationsSourceLinks = [
  {
    title: "Director and AgentJob lifecycle source",
    href: upstream("github-facing/director-agentjob-lifecycle-explainer.md"),
    body: "Reviewed generated noncanonical source for the operational lifecycle page.",
  },
  {
    title: "Role routing source",
    href: upstream("github-facing/role-routing-explainer.md"),
    body: "Reviewed generated noncanonical source for the role-routing page.",
  },
  {
    title: "Validator workflow source",
    href: upstream("github-facing/validator-operator-workflow-explainer.md"),
    body: "Reviewed generated noncanonical source for the validator/operator page.",
  },
  {
    title: "Publication process source",
    href: upstream("github-facing/documentation-curator-publication-process-explainer.md"),
    body: "Reviewed generated noncanonical source for the publication-process page.",
  },
  {
    title: "Project-system improvement source",
    href: upstream("github-facing/project-system-improvement-explainer.md"),
    body: "Reviewed generated noncanonical source for the improvement-loop page.",
  },
  {
    title: "Technical requirements source",
    href: upstream("github-facing/technical-requirements-explainer.md"),
    body: "Reviewed generated noncanonical source for local operation requirements.",
  },
  {
    title: "Research-control guide",
    href: upstream("research_control/README.md"),
    body: "Committed control source for routing, validation, and operational evidence boundaries.",
  },
  {
    title: "Publication process standard",
    href: upstream("research_control/design/documentation_curator_publication_process.md"),
    body: "Committed source for brief-first publication and human review discipline.",
  },
  {
    title: "Project-control script guide",
    href: upstream("scripts/project_control/README.md"),
    body: "Committed tooling source for project-system classifier, resolver, sidecar, and receipt workflows.",
  },
];

export const internalExplainers: Record<string, InternalExplainer> = {
  operations: {
    title: "Operations",
    eyebrow: "Operational synthesis",
    description:
      "Operational explainer landing page for AEther Flow routing, roles, validation, publication, improvement, and technical requirements.",
    lead:
      "Operations are the control surfaces that make the project auditable: route one bounded task, bind authority to records, run the right checks, and preserve evidence without turning operational success into scientific proof.",
    actionHref: "#operations-map",
    actionLabel: "Read the operating model",
    secondaryHref: "/",
    secondaryLabel: "Back to Home",
    visualTitle: "Operations control map",
    visualCaption:
      "Visual orientation only: the operational family explains control evidence, not physics truth or claim promotion.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "Operations explain how work is controlled.",
    boundaryBody:
      "This landing page synthesizes reviewed operational explainers. It cannot change routing behavior, validators, role authority, publication requirements, project-system signals, or physics status.",
    claimStatus: "curated operational synthesis",
    updated: "2026-06-28",
    sourceRefs: operationsSourceRefs,
    comprehension: operationsComprehension,
    sections: [
      {
        eyebrow: "Operating model",
        title: "Authority narrows as evidence accumulates.",
        body:
          "The operational stack is conservative. Each record answers a smaller question than the previous one: what was requested, what was authorized, what was allowed, what was checked, and what remains open.",
        cards: [
          {
            label: "Route",
            title: "Director decision",
            body:
              "A Director decision selects one role path, records rejected alternatives, and preserves the claim boundary.",
          },
          {
            label: "Execute",
            title: "AgentJob allowlist",
            body:
              "The AgentJob controls allowed paths, outputs, validators, source classes, and stop conditions for one transaction.",
          },
          {
            label: "Check",
            title: "Validation evidence",
            body:
              "Validators and tests establish bounded acceptance for the checked state, not global correctness or source authority.",
          },
          {
            label: "Preserve",
            title: "Completion and handoff",
            body:
              "Completion records, handoffs, and registries keep the evidence trail inspectable without rewriting history.",
          },
        ],
      },
      {
        eyebrow: "Operational routes",
        title: "Use the operations pages as an inspection guide.",
        body:
          "These routes organize operational concepts inside the website. Source links remain available below as provenance.",
        cards: operationsLinks.map((link) => ({
          label: "Internal route",
          title: link.title,
          body: link.body,
        })),
      },
    ],
    relatedLinks: [
      ...operationsLinks,
      {
        title: "AI Research-Agent System",
        href: "/ai-research-system/",
        body: "Conceptual track landing page for the governed AI research-agent system.",
      },
      {
        title: "Source Authority",
        href: "/resources/source-authority/",
        body: "How to read website pages, generated derivatives, registries, and source records.",
      },
    ],
    sourceLinks: operationsSourceLinks,
  },
  parentChildSynthesis: {
    title: "Parent-Child Parallel Synthesis",
    eyebrow: "AI research-agent explainer",
    description:
      "Reader-facing explanation of parent-child parallel synthesis as an internal perspective structure inside one bounded physics AgentJob.",
    lead:
      "Parent-child synthesis lets one future physics AgentJob inspect a problem from multiple internal perspectives while preserving one outer decision, one allowlist, one completion, and one fused output.",
    actionHref: "#single-frame",
    actionLabel: "Read the one-job rule",
    secondaryHref: "/ai-research-system/",
    secondaryLabel: "Back to AI system",
    visualTitle: "Parent-child synthesis frame",
    visualCaption:
      "Visual orientation only: child perspectives remain inside one outer AgentJob and do not create independent authority.",
    boundaryLabel: "Authority boundary",
    boundaryTitle: "Parallel perspective does not create parallel authority.",
    boundaryBody:
      "This page explains a future physics AgentJob pattern. It cannot change the one-job rule, AgentJob schema, execution-role schema, validators, routing behavior, role authority, write permissions, or physics claim status.",
    claimStatus: "workflow orientation",
    updated: "2026-06-28",
    sourceRefs: [
      "The AEther Flow. (2026). github-facing/parent-child-synthesis-explainer.md",
      "The AEther Flow. (2026). research_control/README.md",
      "The AEther Flow. (2026). .agents/schemas/AGENT_JOB_SCHEMA.md",
      "The AEther Flow. (2026). .agents/schemas/EXECUTION_ROLE_SCHEMA.md",
      "The AEther Flow. (2026). registries/AGENT_JOB_REGISTRY.csv",
      "The AEther Flow Website. (2026). docs/system-analyses/parent-child-parallel-synthesis-walkthrough.md",
    ],
    comprehension: parentChildComprehension,
    sections: [
      {
        eyebrow: "Single outer frame",
        title: "The external control record remains singular.",
        body:
          "Child perspectives can improve review coverage, but they inherit the same claim boundary, source restrictions, write allowlist, validators, and stop conditions as the outer job.",
        cards: [
          {
            label: "Parent",
            title: "Review and fusion",
            body:
              "The parent enforces the shared boundary, reviews child outputs, preserves conflicts, and fuses the final artifact.",
          },
          {
            label: "Children",
            title: "Draft/control perspectives",
            body:
              "Child outputs surface analytical pressures but remain supporting `draft/control` artifacts without independent authority.",
          },
          {
            label: "Conflict",
            title: "Blocking disagreements must be resolved",
            body:
              "A declared blocking conflict must be reviewed and resolved, or the job cannot receive PASS completion.",
          },
          {
            label: "Output",
            title: "One fused artifact",
            body:
              "The final downstream reference remains one fused output tied to one completion record.",
          },
        ],
      },
      {
        eyebrow: "Inherited authority",
        title: "The child units cannot expand the job.",
        body:
          "If a task needs actual authority expansion, the project must route through ordinary execution-role paths and any protected human-gated approval.",
        cards: [
          {
            label: "No extra roles",
            title: "No child execution-role records",
            body:
              "Labels for child perspectives describe what to inspect; they do not become separate role contracts.",
          },
          {
            label: "No extra writes",
            title: "Same allowlist",
            body:
              "Child outputs, conflict notes, and fusion notes must stay inside the outer AgentJob write boundary.",
          },
          {
            label: "No promotion",
            title: "Same claim boundary",
            body:
              "Parent-child synthesis cannot promote ontology, certify a benchmark, or complete a derivation by structure alone.",
          },
        ],
      },
    ],
    relatedLinks: [
      {
        title: "AI Research-Agent System",
        href: "/ai-research-system/",
        body: "Return to the AI track landing page.",
      },
      {
        title: "Roles and skills",
        href: "/ai-research-system/roles-and-schemas/",
        body: "Inspect why labels and role templates are not permission by themselves.",
      },
      {
        title: "Director and AgentJob lifecycle",
        href: "/ai-research-system/agentjob-lifecycle/",
        body: "Read the operational record chain that parent-child synthesis must preserve.",
      },
    ],
    sourceLinks: [
      {
        title: "Parent-child synthesis source",
        href: upstream("github-facing/parent-child-synthesis-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this reader-facing adaptation.",
      },
    ],
  },
  directorAgentjobLifecycle: {
    title: "Director Decisions And AgentJob Lifecycle",
    eyebrow: "Operations explainer",
    description:
      "Reader-facing explanation of AEther Flow task routing, Director decisions, AgentJobs, completions, handoffs, and registry evidence.",
    lead:
      "The lifecycle makes controlled work inspectable. A task narrows into a Director decision, an AgentJob, role execution evidence, completion, and handoff or registry rows when needed.",
    actionHref: "#lifecycle-map",
    actionLabel: "Read the lifecycle",
    secondaryHref: "/ai-research-system/",
    secondaryLabel: "Back to operations",
    visualTitle: "Director and AgentJob lifecycle",
    visualCaption:
      "Visual orientation only: each state narrows authority for one bounded transaction.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "The record chain is evidence, not permission expansion.",
    boundaryBody:
      "This page cannot edit activated records, broaden an allowlist, change a role, issue a gate decision, promote ontology, or convert completion evidence into a broader scientific claim.",
    claimStatus: "operational orientation",
    updated: "2026-06-28",
    sourceRefs: directorLifecycleSourceRefs,
    comprehension: directorAgentjobLifecycleComprehension,
    sections: [
      {
        eyebrow: "Lifecycle map",
        title: "Each record narrows the next record.",
        body:
          "The durable chain answers what was authorized, what was allowed, what was checked, and what remains blocked or next.",
        cards: [
          {
            label: "Task",
            title: "Names the objective",
            body:
              "The task records status, parentage, current decision, current job, closure, and the next recommendation.",
          },
          {
            label: "Decision",
            title: "Selects the route",
            body:
              "The Director decision records role selection, rejected alternatives, claim boundary, and required checks.",
          },
          {
            label: "AgentJob",
            title: "Defines executable scope",
            body:
              "The job sets allowed reads and writes, generated outputs, forbidden paths, validators, and stop conditions.",
          },
          {
            label: "Completion",
            title: "Records evidence",
            body:
              "The completion captures outputs, command results, verdict, uncertainty, and next recommendation for one transaction.",
          },
        ],
      },
      {
        eyebrow: "Immutable evidence",
        title: "Correct by supersession, not silent mutation.",
        body:
          "A failed or obsolete record can be followed by a repair packet. The old record stays interpretable because history is not edited into a cleaner story.",
        cards: [
          {
            label: "Repair",
            title: "New packet",
            body:
              "A repair or changed route should produce a new bounded packet rather than rewriting activated authority.",
          },
          {
            label: "Stop",
            title: "Protected authority remains protected",
            body:
              "Gate Chair verdicts, benchmark promotion, ontology adoption, and source edits require their own authority paths.",
          },
          {
            label: "Limit",
            title: "Completion evidence stays transaction-local",
            body:
              "A completion can close or hand off one job, but it cannot make the checked operation a scientific result.",
          },
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Role routing",
        href: "/ai-research-system/roles-and-schemas/",
        body: "Read how role templates bind to one execution record.",
      },
      {
        title: "Validator and operator workflow",
        href: "/ai-research-system/validators-and-handoffs/",
        body: "Read how evidence is checked and interpreted.",
      },
      {
        title: "Parent-child synthesis",
        href: "/ai-research-system/workflow/",
        body: "Read how internal perspectives preserve one outer AgentJob.",
      },
    ],
    sourceLinks: [
      {
        title: "Director and AgentJob lifecycle source",
        href: upstream("github-facing/director-agentjob-lifecycle-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
      {
        title: "AgentJob schema",
        href: upstream(".agents/schemas/AGENT_JOB_SCHEMA.md"),
        body: "Committed schema source for allowed paths, outputs, validators, and stop conditions.",
      },
      {
        title: "Research-control scoped guidance",
        href: upstream("research_control/AGENTS.md"),
        body: "Committed guidance for immutable activated records and supersession.",
      },
    ],
  },
  roleRouting: {
    title: "Role Routing And Execution Contracts",
    eyebrow: "Operations explainer",
    description:
      "Reader-facing explanation of role templates, task overlays, provisional roles, execution-role records, and AgentJob allowlists.",
    lead:
      "A role name is not live permission. Role contracts describe normal capabilities, while the execution-role record and AgentJob allowlist decide what one transaction may do.",
    actionHref: "#contract-stack",
    actionLabel: "Read the contract stack",
    secondaryHref: "/ai-research-system/",
    secondaryLabel: "Back to operations",
    visualTitle: "Role routing contract stack",
    visualCaption:
      "Visual orientation only: role labels become current authority only through task-local records and allowlists.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "Role labels must not smuggle permissions.",
    boundaryBody:
      "This page cannot register roles, supersede roles, expand role authority, execute a Gate Chair path, change skill contracts, or authorize generated outputs as source authority.",
    claimStatus: "operational orientation",
    updated: "2026-06-28",
    sourceRefs: roleRoutingSourceRefs,
    comprehension: roleRoutingComprehension,
    sections: [
      {
        eyebrow: "Contract stack",
        title: "Inspect the current job, not only the role name.",
        body:
          "The safe inspection order is role registry, role contract, execution-role record, AgentJob, claim boundary, and completion evidence.",
        cards: [
          {
            label: "Registered role",
            title: "Stable template",
            body:
              "The registered role describes normal capability and constraints, but does not grant current write permission by itself.",
          },
          {
            label: "Task overlay",
            title: "One-job adaptation",
            body:
              "A task overlay can constrain a registered role locally. It must not become a reusable role version by habit.",
          },
          {
            label: "Provisional role",
            title: "Expires after one job",
            body:
              "A one-job provisional role is temporary unless later registered through a governed project-system path.",
          },
          {
            label: "AgentJob",
            title: "Actual boundary",
            body:
              "The allowlist decides allowed writes, outputs, source classes, validators, and stop conditions for the current transaction.",
          },
        ],
      },
      {
        eyebrow: "Overread prevention",
        title: "Operational labels are useful only when they remain bounded.",
        body:
          "The route family uses roles to make work reviewable. It does not turn labels, overlays, or provisional roles into durable permission grants.",
        cards: [
          {
            label: "Template",
            title: "A role is descriptive until routed",
            body:
              "The role registry and contract describe normal capability; the current task still needs an execution-role record and AgentJob.",
          },
          {
            label: "Gate",
            title: "Human-gated roles remain gated",
            body:
              "A role contract can describe gate authority without making a normal route able to execute that gate.",
          },
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Roles and skills",
        href: "/ai-research-system/roles-and-schemas/",
        body: "Reader-facing catalog for role and skill inspection.",
      },
      {
        title: "Director and AgentJob lifecycle",
        href: "/ai-research-system/agentjob-lifecycle/",
        body: "How a decision narrows into one executable job.",
      },
      {
        title: "Source Authority",
        href: "/resources/source-authority/",
        body: "How public summaries relate to registered sources.",
      },
    ],
    sourceLinks: [
      {
        title: "Role routing source",
        href: upstream("github-facing/role-routing-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
      {
        title: "Agent role registry",
        href: upstream("registries/AGENT_ROLE_REGISTRY.csv"),
        body: "Committed registry source for role status, defaults, and boundaries.",
      },
      {
        title: "Execution-role schema",
        href: upstream(".agents/schemas/EXECUTION_ROLE_SCHEMA.md"),
        body: "Committed schema source for task-local execution role records.",
      },
    ],
  },
  validatorOperatorWorkflow: {
    title: "Validator PASS Does Not Mean Physics Proof",
    eyebrow: "Operations explainer",
    description:
      "Reader-facing explanation of command selection, validation evidence, screenshots, receipts, and why PASS does not prove physics.",
    lead:
      "A PASS result says a named check accepted the checked state. It is useful operational evidence, but it is not theorem proof, ontology adoption, benchmark promotion, Gate Chair approval, or permission expansion.",
    actionHref: "#command-map",
    actionLabel: "Read the command map",
    secondaryHref: "/ai-research-system/",
    secondaryLabel: "Back to operations",
    visualTitle: "Validator evidence flow",
    visualCaption:
      "Visual orientation only: checks and receipts are bounded operational evidence.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "PASS is not a scientific verdict.",
    boundaryBody:
      "This page cannot change validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, checkpoint gates, sidecar adoption status, generated-output authority, Gate Chair status, or physics status.",
    claimStatus: "validator-pass boundary orientation",
    updated: "2026-06-28",
    sourceRefs: [
      upstreamRef("github-facing/validator-operator-workflow-explainer.md"),
      upstreamRef("github-facing/claim-gates-explainer.md"),
      upstreamRef("research_control/README.md"),
      upstreamRef("research_control/design/mathematical_decisiveness_completion_contract.md"),
      upstreamRef("scripts/research_control/README.md"),
      upstreamRef("scripts/project_control/README.md"),
      upstreamRef("tests/README.md"),
      "The AEther Flow Website. (2026). docs/system-analyses/validator-pass-does-not-mean-physics-proof.md",
    ],
    comprehension: validatorOperatorWorkflowComprehension,
    sections: [
      {
        eyebrow: "Command map",
        title: "Choose checks by changed authority surface.",
        body:
          "Memory refresh, publication pages, project-system state, source-bridged sidecars, tooling changes, and research-control records require different evidence.",
        cards: [
          {
            label: "Memory",
            title: "Bootstrap then validate",
            body:
              "Generated derivatives refresh through the approved path; source files remain the authority.",
          },
          {
            label: "Publication",
            title: "Pair checks with screenshots",
            body:
              "Public pages need deterministic checks plus rendered evidence because readability is user-facing.",
          },
          {
            label: "Project system",
            title: "Classify and receipt",
            body:
              "State-changing project-system work needs classifier, resolver, documentation-impact, research-control, and checkpoint evidence.",
          },
          {
            label: "Tooling",
            title: "Run focused tests",
            body:
              "Scripts, validators, schemas, roles, or memory tools require unit tests in addition to control validators.",
          },
        ],
      },
      {
        eyebrow: "PASS limits",
        title: "Deterministic acceptance has a bounded meaning.",
        body:
          "A green check does not promote claims, prove theorems, expand roles, adopt sidecars, issue Gate Chair approval, or make generated outputs authoritative.",
        cards: [
          {
            label: "Necessary",
            title: "Transaction evidence",
            body: "A PASS result can be necessary evidence for the current checked state.",
          },
          {
            label: "Insufficient",
            title: "No theorem proof",
            body: "It does not prove ontology, derive GR, promote a benchmark, or issue a Gate Chair verdict.",
          },
          {
            label: "Protected",
            title: "Human gates remain separate",
            body: "Ontology adoption, benchmark promotion, Gate Chair closure, and protected authority changes need their own source and approval path.",
          },
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Technical requirements",
        href: "/ai-research-system/runtime-requirements/",
        body: "Tool tiers needed to reproduce operations.",
      },
      {
        title: "Project-system improvement",
        href: "/ai-research-system/project-system-improvement/",
        body: "How signals and improvement packets are routed and closed.",
      },
      {
        title: "Gate Chair and human gates",
        href: "/ai-research-system/human-gated-promotion/",
        body: "Why protected decisions remain outside validator authority.",
      },
      {
        title: "Claim-boundary explorer",
        href: "/physics/claim-status/",
        body: "How allowed and forbidden claim forms are exposed for readers.",
      },
      {
        title: "Research-agent workflow",
        href: "/ai-research-system/workflow/",
        body: "Where validators fit in the bounded AgentJob record chain.",
      },
      {
        title: "Source Authority",
        href: "/resources/source-authority/",
        body: "The broader source and derivative boundary.",
      },
    ],
    sourceLinks: [
      {
        title: "Validator workflow source",
        href: upstream("github-facing/validator-operator-workflow-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
      {
        title: "Mathematical decisiveness contract",
        href: upstream("research_control/design/mathematical_decisiveness_completion_contract.md"),
        body: "Committed control source separating PASS from physics progress.",
      },
      {
        title: "Claim gates source",
        href: upstream("github-facing/claim-gates-explainer.md"),
        body: "Generated noncanonical source for claim-promotion and Gate Chair boundaries.",
      },
    ],
  },
  publicationProcess: {
    title: "Documentation Curator Publication Process",
    eyebrow: "Operations explainer",
    description:
      "Reader-facing explanation of how AEther Flow public explainers move from publication brief to source spec, page, screenshots, and review.",
    lead:
      "The publication process exists because a mechanically valid page can still be weak. It preserves source basis, authority boundary, readability, visual evidence, and review evidence.",
    actionHref: "#publication-lifecycle",
    actionLabel: "Read the lifecycle",
    secondaryHref: "/ai-research-system/",
    secondaryLabel: "Back to operations",
    visualTitle: "Publication lifecycle",
    visualCaption:
      "Visual orientation only: publication evidence improves readability without changing source authority.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "Publication quality is downstream from source authority.",
    boundaryBody:
      "This page cannot make generated reader surfaces authoritative, change publication validators, replace source specs, or alter scientific, mathematical, governance, or workflow source claims.",
    claimStatus: "publication-process orientation",
    updated: "2026-06-28",
    sourceRefs: publicationProcessSourceRefs,
    comprehension: publicationProcessComprehension,
    sections: [
      {
        eyebrow: "Publication lifecycle",
        title: "A page-specific brief controls the work.",
        body:
          "The brief defines reader, reader job, source basis, narrative shape, visual strategy, acceptance criteria, and forbidden patterns before public copy is produced.",
        cards: [
          {
            label: "Brief",
            title: "Define the reader job",
            body: "The brief names what the page must help readers understand and what it must not imply.",
          },
          {
            label: "Source spec",
            title: "Bind the source basis",
            body: "The source spec preserves source materials, authority boundary, and core claims.",
          },
          {
            label: "Page",
            title: "Adapt for readers",
            body: "The website may improve clarity and structure without changing the source claim status.",
          },
          {
            label: "Review",
            title: "Check rendered evidence",
            body: "Screenshots and before/after review capture public readability beyond command success.",
          },
        ],
      },
      {
        eyebrow: "Review boundary",
        title: "A readable page is not an authority upgrade.",
        body:
          "Publication work can improve the reader journey, expose provenance, and record screenshots. It still remains downstream from the source basis.",
        cards: [
          {
            label: "Human",
            title: "Review covers comprehension",
            body:
              "Screenshots and review notes capture public readability risks that deterministic checks cannot fully decide.",
          },
          {
            label: "Source",
            title: "Claims remain bound",
            body:
              "A source spec prevents the page from silently strengthening mathematical, scientific, governance, or workflow claims.",
          },
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Validator and operator workflow",
        href: "/ai-research-system/validators-and-handoffs/",
        body: "How publication checks and screenshot evidence are interpreted.",
      },
      {
        title: "Source Authority",
        href: "/resources/source-authority/",
        body: "Why generated surfaces remain downstream from sources.",
      },
    ],
    sourceLinks: [
      {
        title: "Publication process source",
        href: upstream("github-facing/documentation-curator-publication-process-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
      {
        title: "Publication process standard",
        href: upstream("research_control/design/documentation_curator_publication_process.md"),
        body: "Committed control source for brief-first publication discipline.",
      },
      {
        title: "Publication process validator",
        href: upstream("scripts/validate_publication_process.py"),
        body: "Committed script source for mechanical publication-process checks.",
      },
    ],
  },
  projectSystemImprovement: {
    title: "Project-System Improvement",
    eyebrow: "Operations explainer",
    description:
      "Reader-facing explanation of project-system signals, classification, resolver output, sidecars, receipts, and one bounded improvement AgentJob.",
    lead:
      "Project-system improvement starts from observed diff state, registered signals, source-bridged sidecars, or repeated workflow problems. It routes one bounded repair without smuggling physics continuation or broad system rewrites.",
    actionHref: "#improvement-loop",
    actionLabel: "Read the loop",
    secondaryHref: "/ai-research-system/",
    secondaryLabel: "Back to operations",
    visualTitle: "Project-system improvement loop",
    visualCaption:
      "Visual orientation only: improvement routing controls project machinery, not scientific claim status.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "A repair packet is one bounded project-system action.",
    boundaryBody:
      "This page cannot create or close signals, create sidecars, replace normal research handoffs, change routing or validator behavior, expand role authority, change checkpoint behavior, globally allowlist sidecars, or authorize physics claim promotion.",
    claimStatus: "project-system orientation",
    updated: "2026-06-28",
    sourceRefs: [
      upstreamRef("github-facing/project-system-improvement-explainer.md"),
      upstreamRef("research_control/README.md"),
      upstreamRef("scripts/project_control/README.md"),
      upstreamRef(".agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md"),
      upstreamRef("registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"),
      upstreamRef("registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"),
      "The AEther Flow Website. (2026). docs/system-analyses/project-system-improvement-loop.md",
    ],
    comprehension: projectSystemImprovementComprehension,
    sections: [
      {
        eyebrow: "Improvement loop",
        title: "Classify first, execute one bounded packet.",
        body:
          "The practical rule is to inspect live state, classify the boundary, resolve against open signals, execute one AgentJob, and close only with explicit evidence.",
        cards: [
          {
            label: "Observe",
            title: "Diff, signal, or repeated problem",
            body: "No action is authorized before source inspection and boundary classification.",
          },
          {
            label: "Route",
            title: "Classifier and resolver",
            body: "Classifier output and resolver ranking guide the next project-system packet.",
          },
          {
            label: "Bridge",
            title: "Sidecars stay separate",
            body: "Project-improvement sidecars are inputs, not replacement research handoffs or completed repairs.",
          },
          {
            label: "Close",
            title: "Receipt or rejection",
            body: "Signals close only with matching PASS completion evidence or a documented rejection decision.",
          },
          {
            label: "Boundary",
            title: "No physics promotion",
            body: "Maintenance packets do not adopt ontology, promote benchmarks, issue Gate Chair decisions, or continue derivation work.",
          },
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Director and AgentJob lifecycle",
        href: "/ai-research-system/agentjob-lifecycle/",
        body: "How one bounded job is authorized and closed.",
      },
      {
        title: "Validator and operator workflow",
        href: "/ai-research-system/validators-and-handoffs/",
        body: "How checks and receipts are interpreted.",
      },
      {
        title: "Memory preflight",
        href: "/ai-research-system/memory-preflight/",
        body: "How memory and retrieval drift remain source-finding support.",
      },
      {
        title: "Source Authority",
        href: "/resources/source-authority/",
        body: "Why generated surfaces and maintenance evidence remain below source authority.",
      },
      {
        title: "Technical requirements",
        href: "/ai-research-system/runtime-requirements/",
        body: "Tooling needed for reproducible operations.",
      },
    ],
    sourceLinks: [
      {
        title: "Project-system improvement source",
        href: upstream("github-facing/project-system-improvement-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
      {
        title: "Research control guide",
        href: upstream("research_control/README.md"),
        body: "Committed control source for signal routing, documentation impact, and resolver limits.",
      },
      {
        title: "Project-control script guide",
        href: upstream("scripts/project_control/README.md"),
        body: "Committed tooling source for classifier, resolver, sidecar, and validation boundaries.",
      },
    ],
  },
  technicalRequirements: {
    title: "Technical Requirements",
    eyebrow: "Operations explainer",
    description:
      "Reader-facing explanation of local tool tiers for reproducible AEther Flow operation and their authority limits.",
    lead:
      "Technical requirements define which tools are needed to perform an operation. They do not decide whether the operation is authorized.",
    actionHref: "#tool-tiers",
    actionLabel: "Read the tool tiers",
    secondaryHref: "/ai-research-system/",
    secondaryLabel: "Back to operations",
    visualTitle: "Technical requirement tiers",
    visualCaption:
      "Visual orientation only: working tools support reproducibility without creating source authority.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "A working tool is not authorization.",
    boundaryBody:
      "This page cannot change dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics status.",
    claimStatus: "technical-requirements orientation",
    updated: "2026-06-28",
    sourceRefs: technicalRequirementsSourceRefs,
    comprehension: technicalRequirementsComprehension,
    sections: [
      {
        eyebrow: "Tool tiers",
        title: "Use the tier that fits the operation.",
        body:
          "Read-only inspection, governed agent work, Python checks, memory refresh, HTML QA, and PDF derivative work have different tool requirements.",
        cards: [
          {
            label: "Inspect",
            title: "Browser, editor, shell, Git",
            body: "Read-only inspection has minimal requirements and does not authorize edits.",
          },
          {
            label: "Validate",
            title: "Python environment",
            body: "Repository-owned validators and tests provide deterministic evidence for changed surfaces.",
          },
          {
            label: "Render",
            title: "Astro and browser QA",
            body: "Public website work needs static build checks and rendered evidence where layouts changed.",
          },
          {
            label: "Derive",
            title: "Managed PDF lane",
            body: "PDF derivatives belong to registered TeX source workflows and remain human-readable derivatives.",
          },
        ],
      },
      {
        eyebrow: "Authority boundary",
        title: "Capability and authorization are separate questions.",
        body:
          "A complete local toolchain can make a check reproducible. It still cannot create permission, alter command policy, or promote a scientific claim.",
        cards: [
          {
            label: "Capability",
            title: "The tool can run",
            body:
              "Successful execution shows the local environment can perform the operation that was requested.",
          },
          {
            label: "Authority",
            title: "The source records decide scope",
            body:
              "Tasks, roles, AgentJobs, validators, and source registries still decide whether the operation is allowed.",
          },
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Validator and operator workflow",
        href: "/ai-research-system/validators-and-handoffs/",
        body: "Which checks fit each changed authority surface.",
      },
      {
        title: "Ontology Documents",
        href: "/resources/documents/",
        body: "Read PDF derivatives and download registered TeX source files.",
      },
      {
        title: "Source Authority",
        href: "/resources/source-authority/",
        body: "How tools, validators, generated pages, and source records differ.",
      },
    ],
    sourceLinks: [
      {
        title: "Technical requirements source",
        href: upstream("github-facing/technical-requirements-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
      {
        title: "Repository README",
        href: upstream("README.md"),
        body: "Committed source for local operating environment and command families.",
      },
      {
        title: "Tests guide",
        href: upstream("tests/README.md"),
        body: "Committed source for test areas and command evidence boundaries.",
      },
    ],
  },
};
