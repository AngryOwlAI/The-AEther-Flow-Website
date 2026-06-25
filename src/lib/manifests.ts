import assetManifest from "../../public/files/manifests/asset_manifest.json";
import sourceManifest from "../../public/files/manifests/source_manifest.json";

export type SourceManifestItem = {
  id: string;
  site_path: string;
  kind: string;
  title: string;
  source_path: string;
  source_commit?: string;
  approval_status: string;
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
