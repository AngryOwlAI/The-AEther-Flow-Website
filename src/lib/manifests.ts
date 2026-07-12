import assetManifest from "../../public/files/manifests/asset_manifest.json";
import sourceManifest from "../../public/files/manifests/source_manifest.json";

export type SourceApprovalStatus =
  | "approved"
  | "sample"
  | "draft"
  | "historical"
  | "source-index-only";

export type SourceManifestItem = {
  id: string;
  site_path: string;
  kind: string;
  title: string;
  source_path: string;
  source_commit?: string;
  approval_status: SourceApprovalStatus;
  sha256?: string;
  generated_by?: string;
  generated_at?: string;
  reviewed_by?: string;
  license_or_usage_note?: string;
  notes?: string;
  source_authority_status?: string;
  claim_status?: string;
  research_status?: string;
  ontology_promotion_status?: string;
};

export type AssetManifestItem = {
  path: string;
  kind: string;
  bytes: number;
  sha256: string;
  title: string;
  source_ref: string;
};

export type DownloadItem = AssetManifestItem & {
  source?: SourceManifestItem;
};

export type OntologyDocument = {
  slug: string;
  title: string;
  pdf?: DownloadItem;
  tex?: DownloadItem;
};

export type OntologyDocumentSequenceEntry = {
  slug: string;
  ordinal: number;
  title: string;
  role: "canonical_front_door" | "ordered_core" | "release_synthesis";
  guidance: string;
};

const sourceItems = (sourceManifest.items as SourceManifestItem[]) ?? [];
const assets = (assetManifest.items as AssetManifestItem[]) ?? [];
const sourceById = new Map(sourceItems.map((item) => [item.id, item]));

export const downloads: DownloadItem[] = assets.map((asset) => {
  const sourceId = asset.source_ref.replace(/^source_manifest:/, "");
  return {
    ...asset,
    source: sourceById.get(sourceId),
  };
});

export const approvedDownloads = downloads.filter(
  (item) => item.source?.approval_status === "approved",
);

export const sampleDownloads = downloads.filter(
  (item) => item.source?.approval_status === "sample",
);

export const downloadStatusCounts = downloads.reduce<Record<string, number>>((counts, item) => {
  const status = item.source?.approval_status ?? "unknown";
  counts[status] = (counts[status] ?? 0) + 1;
  return counts;
}, {});

export const ontologyDocumentSequence: readonly OntologyDocumentSequenceEntry[] = [
  {
    slug: "aether_flow_exact_closure_sequence_overview",
    ordinal: 1,
    title: "Exact Closure Sequence Overview",
    role: "canonical_front_door",
    guidance:
      "Start here. This overview is the canonical scientific front door and fixes the package reading order and claim boundary.",
  },
  {
    slug: "aether_flow_exact_closure_note",
    ordinal: 2,
    title: "Exact Closure Note",
    role: "ordered_core",
    guidance:
      "Read the shortest standalone anchor for the active exact-closure position and its explicit nonclaims.",
  },
  {
    slug: "aether_flow_foundations",
    ordinal: 3,
    title: "Foundations",
    role: "ordered_core",
    guidance:
      "Continue with the ontological vocabulary, original framework intent, and the reason exact closure is the active stance.",
  },
  {
    slug: "aether_flow_dynamics",
    ordinal: 4,
    title: "Dynamics",
    role: "ordered_core",
    guidance:
      "Inspect the adopted effective action, field equations, matter coupling, weak-field structure, and benchmark role.",
  },
  {
    slug: "aether_flow_consistency",
    ordinal: 5,
    title: "Consistency",
    role: "ordered_core",
    guidance:
      "Check the gauge structure, degree-of-freedom count, and effective health conditions inherited from GR.",
  },
  {
    slug: "aether_flow_relativistic_recovery",
    ordinal: 6,
    title: "Relativistic Recovery",
    role: "ordered_core",
    guidance:
      "Read the exact relation to GR and the local relation to SR, including propagation, redshift, clocks, and inertial structure.",
  },
  {
    slug: "aether_flow_geometry",
    ordinal: 7,
    title: "Flow Geometry",
    role: "ordered_core",
    guidance:
      "Complete the core with the congruence-based geometric dictionary for the AEther-flow interpretation.",
  },
  {
    slug: "aether_flow_exact_closure_flagship_article",
    ordinal: 8,
    title: "Exact Closure Flagship Article",
    role: "release_synthesis",
    guidance:
      "Read this release-facing synthesis after the ordered scientific core; it does not replace the canonical overview.",
  },
];

export const ontologyDocumentOrder = ontologyDocumentSequence.map(
  (entry) => entry.slug,
);

const ontologySlugFromDownload = (item: DownloadItem) => {
  const sourcePath = item.source?.source_path ?? item.path;
  const match = sourcePath.match(/ontology\/(?:pdfs|tex)\/(.+)\.(pdf|tex)$/);
  return match?.[1];
};

const duplicateValues = (values: readonly string[]) =>
  [...new Set(values.filter((value, index) => values.indexOf(value) !== index))];

export const validateOntologyDocumentSequence = (
  sequence: readonly OntologyDocumentSequenceEntry[],
  availableSlugs: readonly string[],
) => {
  const expectedSlugs = sequence.map((entry) => entry.slug);
  const duplicateExpected = duplicateValues(expectedSlugs);
  const duplicateAvailable = duplicateValues(availableSlugs);
  const expectedSet = new Set(expectedSlugs);
  const availableSet = new Set(availableSlugs);
  const missing = expectedSlugs.filter((slug) => !availableSet.has(slug));
  const unexpected = availableSlugs.filter((slug) => !expectedSet.has(slug));
  const invalidOrdinals = sequence
    .filter((entry, index) => entry.ordinal !== index + 1)
    .map((entry) => `${entry.slug}=${entry.ordinal}`);
  const errors = [
    duplicateExpected.length && `duplicate sequence slugs: ${duplicateExpected.join(", ")}`,
    duplicateAvailable.length && `duplicate available slugs: ${duplicateAvailable.join(", ")}`,
    missing.length && `missing ontology documents: ${missing.join(", ")}`,
    unexpected.length && `unexpected ontology documents: ${unexpected.join(", ")}`,
    invalidOrdinals.length && `invalid sequence ordinals: ${invalidOrdinals.join(", ")}`,
  ].filter(Boolean);

  if (errors.length) {
    throw new Error(
      `Canonical ontology document sequence is invalid: ${errors.join("; ")}`,
    );
  }
};

const documentDownloadsBySlug = new Map<string, DownloadItem[]>();
for (const item of approvedDownloads) {
  const slug = ontologySlugFromDownload(item);
  if (!slug) continue;
  const documentDownloads = documentDownloadsBySlug.get(slug) ?? [];
  documentDownloads.push(item);
  documentDownloadsBySlug.set(slug, documentDownloads);
}

validateOntologyDocumentSequence(
  ontologyDocumentSequence,
  [...documentDownloadsBySlug.keys()],
);

export const ontologyDocuments: OntologyDocument[] = ontologyDocumentSequence
  .map((entry) => {
    const documentDownloads = documentDownloadsBySlug.get(entry.slug) ?? [];
    return {
      slug: entry.slug,
      title: entry.title,
      pdf: documentDownloads.find((item) => item.kind === "pdf"),
      tex: documentDownloads.find((item) => item.kind === "tex"),
    };
  })
  .filter((document) => document.pdf || document.tex);
