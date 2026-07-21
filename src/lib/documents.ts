import catalogManifest from "../../public/files/manifests/document_catalog.json";

export type DocumentCategory =
  | "anthology"
  | "research"
  | "governance"
  | "diagram";

export type DocumentFormat =
  | "pdf"
  | "tex"
  | "markdown"
  | "png"
  | "svg"
  | "mermaid";

export type DocumentAuthorityRole =
  | "authoritative_source"
  | "registered_source"
  | "readable_derivative"
  | "governance_source"
  | "operational_record"
  | "explanatory_derivative"
  | "public_comprehension_asset"
  | "provenance_record";

// Source-specific status vocabularies remain authoritative in their manifests.
export type DocumentStatus = string;

export type DocumentManifestation = {
  kind: DocumentFormat;
  sitePath: string;
  role: DocumentAuthorityRole;
  title?: string;
  bytes?: number;
  sha256?: string;
  sourceId?: string;
  sourcePath?: string;
  sourceCommit?: string;
  generatedAt?: string;
};

export type DocumentRecord = {
  id: string;
  slug: string;
  title: string;
  category: DocumentCategory;
  collection?: string;
  summary: string;
  status: DocumentStatus;
  authorityScope: string;
  readingOrder?: number;
  tags?: string[];
  manifestations: DocumentManifestation[];
  relatedRoutes?: string[];
};

type CatalogManifestation = {
  kind: DocumentFormat;
  site_path: string;
  role: DocumentAuthorityRole;
  title?: string;
};

type CatalogDocumentRecord = {
  id: string;
  slug: string;
  title: string;
  category: DocumentCategory;
  collection?: string;
  summary: string;
  status: DocumentStatus;
  authority_scope: string;
  reading_order?: number;
  tags?: string[];
  manifestations: CatalogManifestation[];
  related_routes?: string[];
};

export type DocumentCatalogManifest = {
  version: 1;
  generated_at: string;
  documents: CatalogDocumentRecord[];
};

export const documentCatalog =
  catalogManifest as unknown as DocumentCatalogManifest;

export const documents: readonly DocumentRecord[] = documentCatalog.documents.map(
  (record) => ({
    id: record.id,
    slug: record.slug,
    title: record.title,
    category: record.category,
    collection: record.collection,
    summary: record.summary,
    status: record.status,
    authorityScope: record.authority_scope,
    readingOrder: record.reading_order,
    tags: record.tags,
    manifestations: record.manifestations.map((manifestation) => ({
      kind: manifestation.kind,
      sitePath: manifestation.site_path,
      role: manifestation.role,
      title: manifestation.title,
    })),
    relatedRoutes: record.related_routes,
  }),
);

export const documentsById = new Map(
  documents.map((document) => [document.id, document]),
);
