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
    title: "Publication Layer Map",
    src: "/assets/diagrams/publication-layer-map.svg",
    alt: "Diagram showing source repository authority flowing into website manifests and static reader pages.",
    caption: "A non-authoritative orientation diagram for the website publication layer.",
    provenance: "Website scaffold fixture; not a scientific source artifact.",
  },
];

export const resourceGroups = [
  {
    title: "Source document library",
    href: "/resources/documents/",
    body: "PDF and TeX downloads rendered from the public asset manifest.",
  },
  {
    title: "Diagram gallery",
    href: "/resources/diagrams/",
    body: "Visual orientation assets with explicit captions and provenance.",
  },
  {
    title: "Equation sample",
    href: "/research/equations/",
    body: "A math-heavy static page used to verify KaTeX behavior and mobile equation wrapping.",
  },
];
