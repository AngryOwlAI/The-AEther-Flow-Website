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
