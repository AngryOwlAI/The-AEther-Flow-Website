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

export const ontologyDocumentOrder = [
  "aether_flow_foundations",
  "aether_flow_dynamics",
  "aether_flow_geometry",
  "aether_flow_relativistic_recovery",
  "aether_flow_consistency",
  "aether_flow_exact_closure_note",
  "aether_flow_exact_closure_sequence_overview",
  "aether_flow_exact_closure_flagship_article",
];

const ontologyTitleFromSlug = (slug: string) =>
  slug
    .split("_")
    .map((word) => {
      if (word === "aether") return "AEther";
      if (word === "gr") return "GR";
      return `${word.charAt(0).toUpperCase()}${word.slice(1)}`;
    })
    .join(" ");

const ontologySlugFromDownload = (item: DownloadItem) => {
  const sourcePath = item.source?.source_path ?? item.path;
  const match = sourcePath.match(/ontology\/(?:pdfs|tex)\/(.+)\.(pdf|tex)$/);
  return match?.[1];
};

export const ontologyDocuments: OntologyDocument[] = ontologyDocumentOrder
  .map((slug) => {
    const documentDownloads = approvedDownloads.filter(
      (item) => ontologySlugFromDownload(item) === slug,
    );
    return {
      slug,
      title: ontologyTitleFromSlug(slug),
      pdf: documentDownloads.find((item) => item.kind === "pdf"),
      tex: documentDownloads.find((item) => item.kind === "tex"),
    };
  })
  .filter((document) => document.pdf || document.tex);
