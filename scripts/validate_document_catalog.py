#!/usr/bin/env python3
"""Validate logical document grouping against asset and source manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DOCUMENT_CATEGORIES = {"anthology", "research", "governance", "diagram"}
DOCUMENT_FORMATS = {"pdf", "tex", "markdown", "png", "svg", "mermaid"}
AUTHORITY_ROLES = {
    "authoritative_source",
    "registered_source",
    "readable_derivative",
    "governance_source",
    "operational_record",
    "explanatory_derivative",
    "public_comprehension_asset",
    "provenance_record",
}
DOCUMENT_FIELDS = {
    "id",
    "slug",
    "title",
    "category",
    "collection",
    "summary",
    "status",
    "authority_scope",
    "reading_order",
    "tags",
    "manifestations",
    "related_routes",
}
REQUIRED_DOCUMENT_FIELDS = {
    "id",
    "slug",
    "title",
    "category",
    "summary",
    "status",
    "authority_scope",
    "manifestations",
}
MANIFESTATION_FIELDS = {"kind", "site_path", "role", "title"}
REQUIRED_MANIFESTATION_FIELDS = {"kind", "site_path", "role"}
ASSET_KINDS_BY_FORMAT = {
    "pdf": {"pdf"},
    "tex": {"tex"},
    "markdown": {"markdown"},
    "png": {"image", "diagram"},
    "svg": {"image", "diagram"},
    "mermaid": {"diagram"},
}
GOVERNANCE_MARKDOWN_PREFIX = "/files/markdown/governance/"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return value


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label}: must be a list")
        return
    if any(not _nonempty_string(item) for item in value):
        errors.append(f"{label}: values must be nonempty strings")
    elif len(value) != len(set(value)):
        errors.append(f"{label}: values must be unique")


def validate_document_catalog(
    catalog: dict[str, Any],
    asset_manifest: dict[str, Any],
    source_manifest: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if catalog.get("version") != 1 or isinstance(catalog.get("version"), bool):
        errors.append("document_catalog: version must be 1")
    if not _nonempty_string(catalog.get("generated_at")):
        errors.append("document_catalog: generated_at is required")
    unknown_top_level = sorted(set(catalog) - {"version", "generated_at", "documents"})
    if unknown_top_level:
        errors.append(
            "document_catalog: unsupported fields: " + ", ".join(unknown_top_level)
        )

    documents = catalog.get("documents")
    if not isinstance(documents, list):
        return errors + ["document_catalog: documents must be a list"]

    assets_by_path = {
        item["path"]: item
        for item in asset_manifest.get("items", [])
        if isinstance(item, dict) and _nonempty_string(item.get("path"))
    }
    sources_by_id = {
        item["id"]: item
        for item in source_manifest.get("items", [])
        if isinstance(item, dict) and _nonempty_string(item.get("id"))
    }
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()
    seen_paths: set[str] = set()
    seen_order: set[tuple[str, str, int]] = set()

    for index, document in enumerate(documents):
        label = f"document_catalog.documents[{index}]"
        if not isinstance(document, dict):
            errors.append(f"{label}: document must be an object")
            continue

        missing = sorted(REQUIRED_DOCUMENT_FIELDS - document.keys())
        unknown = sorted(set(document) - DOCUMENT_FIELDS)
        if missing:
            errors.append(f"{label}: missing required fields: {', '.join(missing)}")
        if unknown:
            errors.append(f"{label}: unsupported fields: {', '.join(unknown)}")

        document_id = document.get("id")
        slug = document.get("slug")
        for field in ("id", "slug", "title", "summary", "status", "authority_scope"):
            if not _nonempty_string(document.get(field)):
                errors.append(f"{label}.{field}: must be a nonempty string")
        if isinstance(document_id, str):
            if document_id in seen_ids:
                errors.append(f"{label}.id: duplicate value {document_id!r}")
            seen_ids.add(document_id)
        if isinstance(slug, str):
            if slug in seen_slugs:
                errors.append(f"{label}.slug: duplicate value {slug!r}")
            seen_slugs.add(slug)

        category = document.get("category")
        if category not in DOCUMENT_CATEGORIES:
            errors.append(f"{label}.category: unsupported value {category!r}")
        collection = document.get("collection")
        if collection is not None and not _nonempty_string(collection):
            errors.append(f"{label}.collection: must be a nonempty string")

        reading_order = document.get("reading_order")
        if reading_order is not None:
            if (
                isinstance(reading_order, bool)
                or not isinstance(reading_order, int)
                or reading_order < 1
            ):
                errors.append(f"{label}.reading_order: must be a positive integer")
            elif isinstance(category, str):
                order_key = (category, str(collection or ""), reading_order)
                if order_key in seen_order:
                    errors.append(f"{label}.reading_order: duplicate collection position")
                seen_order.add(order_key)

        for field in ("tags", "related_routes"):
            if field in document:
                _validate_string_list(document[field], f"{label}.{field}", errors)

        manifestations = document.get("manifestations")
        if not isinstance(manifestations, list) or not manifestations:
            errors.append(f"{label}.manifestations: must be a nonempty list")
            continue

        for manifestation_index, manifestation in enumerate(manifestations):
            manifestation_label = f"{label}.manifestations[{manifestation_index}]"
            if not isinstance(manifestation, dict):
                errors.append(f"{manifestation_label}: manifestation must be an object")
                continue

            missing = sorted(REQUIRED_MANIFESTATION_FIELDS - manifestation.keys())
            unknown = sorted(set(manifestation) - MANIFESTATION_FIELDS)
            if missing:
                errors.append(
                    f"{manifestation_label}: missing required fields: {', '.join(missing)}"
                )
            if unknown:
                errors.append(
                    f"{manifestation_label}: duplicates manifest authority fields: "
                    + ", ".join(unknown)
                )

            kind = manifestation.get("kind")
            role = manifestation.get("role")
            site_path = manifestation.get("site_path")
            if kind not in DOCUMENT_FORMATS:
                errors.append(f"{manifestation_label}.kind: unsupported value {kind!r}")
            if role not in AUTHORITY_ROLES:
                errors.append(f"{manifestation_label}.role: unsupported value {role!r}")
            if not _nonempty_string(site_path) or not str(site_path).startswith("/files/"):
                errors.append(f"{manifestation_label}.site_path: must start with /files/")
                continue
            if site_path in seen_paths:
                errors.append(f"{manifestation_label}.site_path: duplicate value {site_path!r}")
            seen_paths.add(str(site_path))

            asset = assets_by_path.get(site_path)
            if asset is None:
                errors.append(f"{manifestation_label}.site_path: missing asset record {site_path!r}")
                continue
            expected_asset_kinds = ASSET_KINDS_BY_FORMAT.get(str(kind), set())
            if asset.get("kind") not in expected_asset_kinds:
                errors.append(
                    f"{manifestation_label}.kind: {kind!r} conflicts with asset kind "
                    f"{asset.get('kind')!r}"
                )

            source_ref = asset.get("source_ref")
            if not isinstance(source_ref, str) or not source_ref.startswith(
                "source_manifest:"
            ):
                errors.append(f"{manifestation_label}.site_path: asset source_ref is invalid")
                continue
            source = sources_by_id.get(source_ref.split(":", 1)[1])
            if source is None:
                errors.append(f"{manifestation_label}.site_path: asset source is unknown")
                continue

            if kind == "markdown":
                if category != "governance":
                    errors.append(
                        f"{manifestation_label}.kind: public Markdown requires "
                        "governance category"
                    )
                if document.get("status") != "approved":
                    errors.append(
                        f"{label}.status: governance Markdown must be approved"
                    )
                if role != "governance_source":
                    errors.append(
                        f"{manifestation_label}.role: governance Markdown must use "
                        "governance_source"
                    )
                if not (
                    isinstance(site_path, str)
                    and site_path.startswith(GOVERNANCE_MARKDOWN_PREFIX)
                    and site_path.lower().endswith(".md")
                ):
                    errors.append(
                        f"{manifestation_label}.site_path: governance Markdown must be "
                        f"under {GOVERNANCE_MARKDOWN_PREFIX}"
                    )
                if source.get("site_path") != site_path or source.get("kind") != "markdown":
                    errors.append(
                        f"{manifestation_label}.site_path: linked source is not the same "
                        "Markdown publication"
                    )
                if source.get("approval_status") != "approved":
                    errors.append(
                        f"{manifestation_label}.site_path: linked governance source is "
                        "not approved"
                    )
                for field in ("reviewed_by", "license_or_usage_note"):
                    if not _nonempty_string(source.get(field)):
                        errors.append(
                            f"{manifestation_label}.site_path: linked governance source "
                            f"requires {field}"
                        )
            elif isinstance(site_path, str) and site_path.startswith(
                GOVERNANCE_MARKDOWN_PREFIX
            ):
                errors.append(
                    f"{manifestation_label}.site_path: governance Markdown path requires "
                    "Markdown kind"
                )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path("public/files/manifests/document_catalog.json"),
    )
    parser.add_argument(
        "--asset-manifest",
        type=Path,
        default=Path("public/files/manifests/asset_manifest.json"),
    )
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=Path("public/files/manifests/source_manifest.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_document_catalog(
        load_json(args.catalog),
        load_json(args.asset_manifest),
        load_json(args.source_manifest),
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Document catalog validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
