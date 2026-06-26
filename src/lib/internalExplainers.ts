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
}

const upstream = (path: string) =>
  `https://github.com/AngryOwlAI/The-AEther-Flow/blob/main/${path}`;

const upstreamRef = (path: string) => `AEther-Flow Project. (2026). ${path}`;

export const operationsLinks: ExplainerLink[] = [
  {
    title: "Director and AgentJob lifecycle",
    href: "/project/operations/director-agentjob-lifecycle/",
    body: "How tasks narrow into decisions, jobs, completions, handoffs, and registry evidence.",
  },
  {
    title: "Role routing",
    href: "/project/operations/role-routing/",
    body: "Why role names are templates, while execution records and AgentJobs control one transaction.",
  },
  {
    title: "Validator and operator workflow",
    href: "/project/operations/validator-operator-workflow/",
    body: "How checks, receipts, screenshots, and PASS results should be interpreted.",
  },
  {
    title: "Publication process",
    href: "/project/operations/publication-process/",
    body: "How public explainers move from brief to source spec, page, screenshots, and review.",
  },
  {
    title: "Project-system improvement",
    href: "/project/operations/project-system-improvement/",
    body: "How classifiers, signals, sidecars, receipts, and one bounded AgentJob structure repairs.",
  },
  {
    title: "Technical requirements",
    href: "/project/operations/technical-requirements/",
    body: "Local tool tiers for reproducible operation without confusing tools with authorization.",
  },
];

const operationsSourceRefs = [
  upstreamRef("github-facing/director-agentjob-lifecycle-explainer.md"),
  upstreamRef("github-facing/role-routing-explainer.md"),
  upstreamRef("github-facing/validator-operator-workflow-explainer.md"),
  upstreamRef("github-facing/documentation-curator-publication-process-explainer.md"),
  upstreamRef("github-facing/project-system-improvement-explainer.md"),
  upstreamRef("github-facing/technical-requirements-explainer.md"),
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
    secondaryHref: "/project/overview/",
    secondaryLabel: "Back to overview",
    visualTitle: "Operations control map",
    visualCaption:
      "Visual orientation only: the operational family explains control evidence, not physics truth or claim promotion.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "Operations explain how work is controlled.",
    boundaryBody:
      "This landing page synthesizes reviewed operational explainers. It cannot change routing behavior, validators, role authority, publication requirements, project-system signals, or physics status.",
    claimStatus: "curated operational synthesis",
    updated: "2026-06-26",
    sourceRefs: operationsSourceRefs,
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
        href: "/project/ai-research-agent-system/",
        body: "Conceptual track landing page for the governed AI research-agent system.",
      },
      {
        title: "Source Authority",
        href: "/project/source-authority/",
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
    secondaryHref: "/project/ai-research-agent-system/",
    secondaryLabel: "Back to AI system",
    visualTitle: "Parent-child synthesis frame",
    visualCaption:
      "Visual orientation only: child perspectives remain inside one outer AgentJob and do not create independent authority.",
    boundaryLabel: "Authority boundary",
    boundaryTitle: "Parallel perspective does not create parallel authority.",
    boundaryBody:
      "This page explains a future physics AgentJob pattern. It cannot change the one-job rule, AgentJob schema, execution-role schema, validators, routing behavior, role authority, write permissions, or physics claim status.",
    claimStatus: "workflow orientation",
    updated: "2026-06-26",
    sourceRefs: [upstreamRef("github-facing/parent-child-synthesis-explainer.md")],
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
        href: "/project/ai-research-agent-system/",
        body: "Return to the AI track landing page.",
      },
      {
        title: "Roles and skills",
        href: "/project/ai-research-agent-system/roles-and-skills/",
        body: "Inspect why labels and role templates are not permission by themselves.",
      },
      {
        title: "Director and AgentJob lifecycle",
        href: "/project/operations/director-agentjob-lifecycle/",
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
    secondaryHref: "/project/operations/",
    secondaryLabel: "Back to operations",
    visualTitle: "Director and AgentJob lifecycle",
    visualCaption:
      "Visual orientation only: each state narrows authority for one bounded transaction.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "The record chain is evidence, not permission expansion.",
    boundaryBody:
      "This page cannot edit activated records, broaden an allowlist, change a role, issue a gate decision, promote ontology, or convert completion evidence into a broader scientific claim.",
    claimStatus: "operational orientation",
    updated: "2026-06-26",
    sourceRefs: [upstreamRef("github-facing/director-agentjob-lifecycle-explainer.md")],
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
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Role routing",
        href: "/project/operations/role-routing/",
        body: "Read how role templates bind to one execution record.",
      },
      {
        title: "Validator and operator workflow",
        href: "/project/operations/validator-operator-workflow/",
        body: "Read how evidence is checked and interpreted.",
      },
      {
        title: "Parent-child synthesis",
        href: "/project/ai-research-agent-system/parent-child-synthesis/",
        body: "Read how internal perspectives preserve one outer AgentJob.",
      },
    ],
    sourceLinks: [
      {
        title: "Director and AgentJob lifecycle source",
        href: upstream("github-facing/director-agentjob-lifecycle-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
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
    secondaryHref: "/project/operations/",
    secondaryLabel: "Back to operations",
    visualTitle: "Role routing contract stack",
    visualCaption:
      "Visual orientation only: role labels become current authority only through task-local records and allowlists.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "Role labels must not smuggle permissions.",
    boundaryBody:
      "This page cannot register roles, supersede roles, expand role authority, execute a Gate Chair path, change skill contracts, or authorize generated outputs as source authority.",
    claimStatus: "operational orientation",
    updated: "2026-06-26",
    sourceRefs: [upstreamRef("github-facing/role-routing-explainer.md")],
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
    ],
    relatedLinks: [
      {
        title: "Roles and skills",
        href: "/project/ai-research-agent-system/roles-and-skills/",
        body: "Reader-facing catalog for role and skill inspection.",
      },
      {
        title: "Director and AgentJob lifecycle",
        href: "/project/operations/director-agentjob-lifecycle/",
        body: "How a decision narrows into one executable job.",
      },
      {
        title: "Source Authority",
        href: "/project/source-authority/",
        body: "How public summaries relate to registered sources.",
      },
    ],
    sourceLinks: [
      {
        title: "Role routing source",
        href: upstream("github-facing/role-routing-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
    ],
  },
  validatorOperatorWorkflow: {
    title: "Validator And Operator Workflow",
    eyebrow: "Operations explainer",
    description:
      "Reader-facing explanation of command selection, validation evidence, screenshots, receipts, and PASS-result limits.",
    lead:
      "The operator question is which evidence chain fits the changed authority surface. A PASS result is bounded acceptance for a named check, not scientific truth or permission expansion.",
    actionHref: "#command-map",
    actionLabel: "Read the command map",
    secondaryHref: "/project/operations/",
    secondaryLabel: "Back to operations",
    visualTitle: "Validator evidence flow",
    visualCaption:
      "Visual orientation only: checks and receipts are bounded operational evidence.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "PASS is not a scientific verdict.",
    boundaryBody:
      "This page cannot change validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, checkpoint gates, sidecar adoption status, generated-output authority, or physics status.",
    claimStatus: "validator-operator orientation",
    updated: "2026-06-26",
    sourceRefs: [upstreamRef("github-facing/validator-operator-workflow-explainer.md")],
    sections: [
      {
        eyebrow: "Command map",
        title: "Choose checks by changed surface.",
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
          "A green check does not promote claims, expand roles, adopt sidecars, or make generated outputs authoritative.",
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
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Technical requirements",
        href: "/project/operations/technical-requirements/",
        body: "Tool tiers needed to reproduce operations.",
      },
      {
        title: "Project-system improvement",
        href: "/project/operations/project-system-improvement/",
        body: "How signals and improvement packets are routed and closed.",
      },
      {
        title: "Source Authority",
        href: "/project/source-authority/",
        body: "The broader source and derivative boundary.",
      },
    ],
    sourceLinks: [
      {
        title: "Validator workflow source",
        href: upstream("github-facing/validator-operator-workflow-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
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
    secondaryHref: "/project/operations/",
    secondaryLabel: "Back to operations",
    visualTitle: "Publication lifecycle",
    visualCaption:
      "Visual orientation only: publication evidence improves readability without changing source authority.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "Publication quality is downstream from source authority.",
    boundaryBody:
      "This page cannot make generated reader surfaces authoritative, change publication validators, replace source specs, or alter scientific, mathematical, governance, or workflow source claims.",
    claimStatus: "publication-process orientation",
    updated: "2026-06-26",
    sourceRefs: [upstreamRef("github-facing/documentation-curator-publication-process-explainer.md")],
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
    ],
    relatedLinks: [
      {
        title: "Validator and operator workflow",
        href: "/project/operations/validator-operator-workflow/",
        body: "How publication checks and screenshot evidence are interpreted.",
      },
      {
        title: "Source Authority",
        href: "/project/source-authority/",
        body: "Why generated surfaces remain downstream from sources.",
      },
    ],
    sourceLinks: [
      {
        title: "Publication process source",
        href: upstream("github-facing/documentation-curator-publication-process-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
    ],
  },
  projectSystemImprovement: {
    title: "Project-System Improvement",
    eyebrow: "Operations explainer",
    description:
      "Reader-facing explanation of project-system signals, classification, resolver output, sidecars, receipts, and one bounded improvement AgentJob.",
    lead:
      "Project-system improvement starts from observed diff state, registered signals, or repeated workflow problems. It routes one bounded repair without smuggling physics continuation or broad system rewrites.",
    actionHref: "#improvement-loop",
    actionLabel: "Read the loop",
    secondaryHref: "/project/operations/",
    secondaryLabel: "Back to operations",
    visualTitle: "Project-system improvement loop",
    visualCaption:
      "Visual orientation only: improvement routing controls project machinery, not scientific claim status.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "A repair packet is one bounded project-system action.",
    boundaryBody:
      "This page cannot create or close signals, create sidecars, replace normal research handoffs, change routing or validator behavior, expand role authority, change checkpoint behavior, or authorize physics claim promotion.",
    claimStatus: "project-system orientation",
    updated: "2026-06-26",
    sourceRefs: [upstreamRef("github-facing/project-system-improvement-explainer.md")],
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
        ],
      },
    ],
    relatedLinks: [
      {
        title: "Director and AgentJob lifecycle",
        href: "/project/operations/director-agentjob-lifecycle/",
        body: "How one bounded job is authorized and closed.",
      },
      {
        title: "Validator and operator workflow",
        href: "/project/operations/validator-operator-workflow/",
        body: "How checks and receipts are interpreted.",
      },
      {
        title: "Technical requirements",
        href: "/project/operations/technical-requirements/",
        body: "Tooling needed for reproducible operations.",
      },
    ],
    sourceLinks: [
      {
        title: "Project-system improvement source",
        href: upstream("github-facing/project-system-improvement-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
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
    secondaryHref: "/project/operations/",
    secondaryLabel: "Back to operations",
    visualTitle: "Technical requirement tiers",
    visualCaption:
      "Visual orientation only: working tools support reproducibility without creating source authority.",
    boundaryLabel: "Operational boundary",
    boundaryTitle: "A working tool is not authorization.",
    boundaryBody:
      "This page cannot change dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics status.",
    claimStatus: "technical-requirements orientation",
    updated: "2026-06-26",
    sourceRefs: [upstreamRef("github-facing/technical-requirements-explainer.md")],
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
    ],
    relatedLinks: [
      {
        title: "Validator and operator workflow",
        href: "/project/operations/validator-operator-workflow/",
        body: "Which checks fit each changed authority surface.",
      },
      {
        title: "Ontology Documents",
        href: "/resources/documents/",
        body: "Read PDF derivatives and download registered TeX source files.",
      },
      {
        title: "Source Authority",
        href: "/project/source-authority/",
        body: "How tools, validators, generated pages, and source records differ.",
      },
    ],
    sourceLinks: [
      {
        title: "Technical requirements source",
        href: upstream("github-facing/technical-requirements-explainer.md"),
        body: "Reviewed generated noncanonical upstream source for this page.",
      },
    ],
  },
};
