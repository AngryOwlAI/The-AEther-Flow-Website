import type { ComprehensionContent } from "./comprehensionContent";

const sourceLabel = "Source basis";
const routeLabel = "Internal route";

export const sourceAuthorityComprehension: ComprehensionContent = {
  id: "source-authority-comprehension",
  eyebrow: "Trust-boundary comprehension",
  title: "Start from the source lane that owns the claim.",
  summary:
    "Source authority separates registered TeX and source files, registries, claim boundaries, generated derivatives, website pages, diagrams, and reader orientation.",
  diagram: {
    src: "/assets/diagrams/comprehension/source-authority-ladder.png",
    alt:
      "Diagram showing registered TeX and source files upstream from registries, generated derivatives, website pages, reader orientation, and source wins on conflict.",
    caption:
      "Static comprehension diagram: generated and website surfaces remain downstream from registered source authority.",
    provenance:
      "Mermaid source: docs/content-dossiers/source-authority/diagrams/source-authority-ladder.mmd. Manifest id: comprehension_source_authority_ladder.",
  },
  mechanismSteps: [
    {
      title: "Identify the owning lane",
      body:
        "Scientific, mathematical, governance, workflow, and publication claims can have different source owners.",
    },
    {
      title: "Inspect the registered source",
      body:
        "Use pages and generated explainers to locate the source, then verify against source files and registry rows.",
    },
    {
      title: "Resolve conflicts source-first",
      body:
        "When a derivative and source disagree, repair the derivative rather than upgrading the derivative into authority.",
    },
  ],
  terms: [
    {
      term: "Source authority",
      definition: "The upstream file, registry, or governed record that owns current claim status.",
      boundary: "Not replaced by public page clarity.",
    },
    {
      term: "Derivative",
      definition: "A generated or reader-facing surface derived from source material.",
      boundary: "Useful for orientation, not override.",
    },
    {
      term: "Claim boundary",
      definition: "A control statement describing what a result may and may not imply.",
      boundary: "Cannot be broadened by a website summary.",
    },
  ],
  boundaries: [
    {
      label: "No source replacement",
      title: "Website pages are maps",
      body: "The public site explains and links material without superseding source files or registries.",
    },
    {
      label: "No generated promotion",
      title: "Derivative quality is downstream",
      body: "Generated explainers, PDFs, diagrams, memory, and pages cannot promote claims by presentation quality.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Project overview",
      href: "/project/overview/",
      body: "Return to the public two-track entry point.",
    },
    {
      label: routeLabel,
      title: "Resources",
      href: "/resources/",
      body: "Inspect manifest-backed public assets with status labels.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Source authority explainer",
      body: "Generated noncanonical upstream explainer: github-facing/source-authority-explainer.md.",
    },
    {
      label: sourceLabel,
      title: "Publication brief registry",
      body: "Upstream registry: registries/PUBLICATION_BRIEF_REGISTRY.csv.",
    },
  ],
  safeUnsafe: {
    safe:
      "Use website and generated pages to find the right source lane, then rely on registered source files, registries, and governed records for claim status.",
    unsafe:
      "A generated explainer, public page, diagram, PDF, memory hit, or validator PASS replaces source authority or promotes a claim.",
  },
};

export const resourcesIndexComprehension: ComprehensionContent = {
  id: "resources-index-comprehension",
  eyebrow: "Resource comprehension",
  title: "Resources expose manifest-backed assets without creating authority.",
  summary:
    "The resource index is a website-local manifest surface. It links public pages, ontology documents, diagrams, and hashes while preserving source status labels.",
  diagram: {
    src: "/assets/diagrams/comprehension/resources-manifest-chain.png",
    alt:
      "Diagram showing source manifest, asset manifest, resources index, document downloads, diagram gallery, hashes, status labels, and index does not create authority.",
    caption:
      "Static comprehension diagram: resource pages organize committed assets and status labels downstream from source records.",
    provenance:
      "Mermaid source: docs/content-dossiers/resources-index/diagrams/resource-manifest-chain.mmd. Manifest id: comprehension_resources_manifest_chain.",
  },
  mechanismSteps: [
    {
      title: "Read status labels",
      body: "Approval status, kind, source reference, and hash come from the manifests.",
    },
    {
      title: "Choose the internal route",
      body: "Use project pages for explanation before downloading source or derivative files.",
    },
    {
      title: "Inspect manifests for files",
      body: "Asset paths and hashes support verification but do not create scientific authority.",
    },
  ],
  terms: [
    {
      term: "Source manifest",
      definition: "Website manifest describing public assets and their source references.",
      boundary: "Does not supersede upstream source registries.",
    },
    {
      term: "Asset manifest",
      definition: "Generated file list with paths, kinds, byte sizes, hashes, titles, and source refs.",
      boundary: "It indexes website files only.",
    },
  ],
  boundaries: [
    {
      label: "No asset promotion",
      title: "Downloads retain their source status",
      body: "A public resource link does not strengthen a file's claim status.",
    },
    {
      label: "No primary-source shortcut",
      title: "Reader pages explain first",
      body: "Resource pages support inspection after the internal route explains how to read the asset.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Ontology Documents",
      href: "/resources/documents/",
      body: "Inspect TeX sources and PDF derivatives.",
    },
    {
      label: routeLabel,
      title: "Diagram Gallery",
      href: "/resources/diagrams/",
      body: "Inspect diagram assets as visual orientation aids.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Ontology source README",
      body: "Upstream source: ontology/README.md.",
    },
    {
      label: sourceLabel,
      title: "TeX source registry",
      body: "Upstream registry: registries/TEX_SOURCE_REGISTRY.csv.",
    },
  ],
  safeUnsafe: {
    safe:
      "The resource index organizes manifest-backed website assets, hashes, and internal reader paths while preserving each asset's source status.",
    unsafe:
      "A downloadable file, manifest row, or resource card creates source authority, scientific proof, or claim promotion.",
  },
};

export const resourcesDocumentsComprehension: ComprehensionContent = {
  id: "resources-documents-comprehension",
  eyebrow: "Document comprehension",
  title: "Registered TeX carries source authority; PDFs are derivatives.",
  summary:
    "The ontology documents page serves website copies of canonical TeX sources and generated PDFs while keeping TeX registry status and derivative status explicit.",
  diagram: {
    src: "/assets/diagrams/comprehension/resources-tex-pdf-derivative-chain.png",
    alt:
      "Diagram showing registered TeX source, TeX registry row, generated PDF derivative, website TeX copy, human-readable PDF download, source inspection download, and PDF is derivative.",
    caption:
      "Static comprehension diagram: TeX source authority and PDF readability are different asset roles.",
    provenance:
      "Mermaid source: docs/content-dossiers/resources-documents/diagrams/tex-pdf-derivative-chain.mmd. Manifest id: comprehension_resources_tex_pdf_derivative_chain.",
  },
  mechanismSteps: [
    {
      title: "Use PDFs for reading",
      body: "PDFs are generated human-readable derivatives of registered TeX files.",
    },
    {
      title: "Use TeX for source inspection",
      body: "Registered TeX files carry scientific source authority according to upstream registry metadata.",
    },
    {
      title: "Preserve claim status",
      body: "Document availability does not prove a broader derivation or promote a benchmark.",
    },
  ],
  terms: [
    {
      term: "Registered TeX",
      definition: "A TeX source recorded in the upstream source registry.",
      boundary: "Claim status still depends on registry metadata and gates.",
    },
    {
      term: "PDF derivative",
      definition: "A generated human-readable rendering of TeX material.",
      boundary: "Not independent authority when TeX is available.",
    },
  ],
  boundaries: [
    {
      label: "No PDF authority",
      title: "Derivative does not supersede source",
      body: "Readers can use PDFs for accessibility and direct reading while source inspection targets TeX.",
    },
    {
      label: "No derivation promotion",
      title: "Canonical ontology is not full GR derivation",
      body: "The document package does not solve the broader first-principles derivation burden by being downloadable.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Physics Research",
      href: "/project/physics/",
      body: "Read the source-boundary-safe physics route family before inspecting documents.",
    },
    {
      label: routeLabel,
      title: "Source authority",
      href: "/project/source-authority/",
      body: "Read how documents, derivatives, and registries relate.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Ontology README",
      body: "Upstream source: ontology/README.md.",
    },
    {
      label: sourceLabel,
      title: "Ontology TeX README",
      body: "Upstream source: ontology/tex/README.md.",
    },
    {
      label: sourceLabel,
      title: "TeX source registry",
      body: "Upstream registry: registries/TEX_SOURCE_REGISTRY.csv.",
    },
  ],
  safeUnsafe: {
    safe:
      "The documents page makes canonical ontology TeX and generated PDF derivatives easier to inspect while preserving the TeX/PDF authority boundary.",
    unsafe:
      "A PDF download, document list, or website copy independently proves or promotes a scientific claim.",
  },
};

export const resourcesDiagramsComprehension: ComprehensionContent = {
  id: "resources-diagrams-comprehension",
  eyebrow: "Diagram comprehension",
  title: "Diagrams explain relationships; they do not own claims.",
  summary:
    "The diagram gallery presents visual orientation assets with source paths, manifest hashes, captions, provenance, and nearby prose.",
  diagram: {
    src: "/assets/diagrams/comprehension/resources-diagram-publication-boundary.png",
    alt:
      "Diagram showing Mermaid source, generated PNG, manifest entry, diagram gallery, nearby prose and caption, hash-backed asset status, and diagram is not source authority.",
    caption:
      "Static comprehension diagram: a diagram becomes public only as a manifest-backed reader aid.",
    provenance:
      "Mermaid source: docs/content-dossiers/resources-diagrams/diagrams/diagram-publication-boundary.mmd. Manifest id: comprehension_resources_diagram_publication_boundary.",
  },
  mechanismSteps: [
    {
      title: "Keep source editable",
      body: "Mermaid sources live in content dossiers so diagram intent remains reviewable.",
    },
    {
      title: "Serve static PNGs",
      body: "Public pages use committed PNG assets instead of a browser Mermaid runtime.",
    },
    {
      title: "Put claims in prose and sources",
      body: "Alt text, captions, nearby explanation, and source notices carry the interpretive boundary.",
    },
  ],
  terms: [
    {
      term: "Static diagram",
      definition: "A generated public image rendered from tracked diagram source.",
      boundary: "Not a source claim.",
    },
    {
      term: "Diagram provenance",
      definition: "The source path, manifest id, and generation path for the public image.",
      boundary: "Provenance supports audit, not promotion.",
    },
  ],
  boundaries: [
    {
      label: "No diagram authority",
      title: "Visual clarity is not evidence",
      body: "A diagram can reduce confusion but cannot replace sources, gates, or mathematical derivation.",
    },
    {
      label: "No runtime Mermaid",
      title: "Public pages use static images",
      body: "Mermaid remains maintainer/build tooling, not a public browser dependency.",
    },
  ],
  relatedRoutes: [
    {
      label: routeLabel,
      title: "Resources",
      href: "/resources/",
      body: "Return to the resource index and manifest status summary.",
    },
    {
      label: routeLabel,
      title: "Source authority",
      href: "/project/source-authority/",
      body: "Read the broader trust boundary for generated and visual material.",
    },
  ],
  sourceBasis: [
    {
      label: sourceLabel,
      title: "Content dossier workflow",
      body: "Website maintainer workflow: docs/content-dossiers/README.md.",
    },
    {
      label: sourceLabel,
      title: "Source manifest",
      body: "Website manifest: public/files/manifests/source_manifest.json.",
    },
  ],
  safeUnsafe: {
    safe:
      "The diagram gallery shows manifest-backed visual aids with editable sources, static PNG outputs, captions, provenance, and non-authority boundaries.",
    unsafe:
      "A diagram proves science, changes workflow authority, replaces source inspection, or needs Mermaid in the public browser runtime.",
  },
};
