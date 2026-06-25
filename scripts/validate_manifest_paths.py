#!/usr/bin/env python3
"""Validate website manifests against files published from public/."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ALLOWED_SOURCE_KINDS = {"pdf", "tex", "image", "diagram", "manifest", "other"}
ALLOWED_ASSET_KINDS = {"pdf", "tex", "image", "diagram", "other"}
ALLOWED_APPROVAL_STATUS = {
    "approved",
    "sample",
    "draft",
    "historical",
    "source-index-only",
}
REQUIRED_SOURCE_FIELDS = {
    "id",
    "site_path",
    "kind",
    "title",
    "source_path",
    "approval_status",
}
REQUIRED_ASSET_FIELDS = {"path", "kind", "bytes", "sha256", "title", "source_ref"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def public_path_to_file(public_dir: Path, site_path: str) -> Path:
    if not site_path.startswith("/"):
        raise ValueError(f"{site_path!r}: site paths must start with '/'")
    relative = Path(site_path.removeprefix("/"))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{site_path!r}: site paths must stay inside public/")
    return public_dir / relative


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_source_manifest(manifest: dict[str, Any], public_dir: Path) -> list[str]:
    errors: list[str] = []
    if manifest.get("version") != 1:
        errors.append("source_manifest: version must be 1")
    if not manifest.get("generated_at"):
        errors.append("source_manifest: generated_at is required")
    if not manifest.get("source_repository"):
        errors.append("source_manifest: source_repository is required")

    items = manifest.get("items")
    if not isinstance(items, list):
        return errors + ["source_manifest: items must be a list"]

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for index, item in enumerate(items):
        label = f"source_manifest.items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: item must be an object")
            continue

        missing = sorted(REQUIRED_SOURCE_FIELDS - item.keys())
        if missing:
            errors.append(f"{label}: missing required fields: {', '.join(missing)}")
            continue

        item_id = item["id"]
        site_path = item["site_path"]
        kind = item["kind"]
        approval_status = item["approval_status"]

        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{label}: id must be a nonempty string")
        elif item_id in seen_ids:
            errors.append(f"{label}: duplicate id {item_id!r}")
        else:
            seen_ids.add(item_id)

        if kind not in ALLOWED_SOURCE_KINDS:
            errors.append(f"{label}: unsupported kind {kind!r}")
        if approval_status not in ALLOWED_APPROVAL_STATUS:
            errors.append(f"{label}: unsupported approval_status {approval_status!r}")

        try:
            file_path = public_path_to_file(public_dir, site_path)
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue

        if site_path in seen_paths:
            errors.append(f"{label}: duplicate site_path {site_path!r}")
        else:
            seen_paths.add(site_path)

        if not file_path.is_file():
            errors.append(f"{label}: missing published file {file_path}")
            continue

        expected_hash = item.get("sha256")
        if expected_hash:
            actual_hash = sha256_file(file_path)
            if expected_hash != actual_hash:
                errors.append(
                    f"{label}: sha256 mismatch for {site_path}: "
                    f"expected {expected_hash}, got {actual_hash}"
                )

    return errors


def validate_asset_manifest(
    manifest: dict[str, Any],
    public_dir: Path,
    source_manifest: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if manifest.get("version") != 1:
        errors.append("asset_manifest: version must be 1")
    if not manifest.get("generated_at"):
        errors.append("asset_manifest: generated_at is required")

    source_ids = {
        item["id"]
        for item in source_manifest.get("items", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    items = manifest.get("items")
    if not isinstance(items, list):
        return errors + ["asset_manifest: items must be a list"]

    seen_paths: set[str] = set()
    for index, item in enumerate(items):
        label = f"asset_manifest.items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: item must be an object")
            continue

        missing = sorted(REQUIRED_ASSET_FIELDS - item.keys())
        if missing:
            errors.append(f"{label}: missing required fields: {', '.join(missing)}")
            continue

        site_path = item["path"]
        kind = item["kind"]
        source_ref = item["source_ref"]

        if kind not in ALLOWED_ASSET_KINDS:
            errors.append(f"{label}: unsupported kind {kind!r}")
        if site_path in seen_paths:
            errors.append(f"{label}: duplicate path {site_path!r}")
        else:
            seen_paths.add(site_path)

        if not isinstance(source_ref, str) or not source_ref.startswith("source_manifest:"):
            errors.append(f"{label}: source_ref must use source_manifest:<id>")
        else:
            source_id = source_ref.split(":", 1)[1]
            if source_id not in source_ids:
                errors.append(f"{label}: source_ref points to unknown source id {source_id!r}")

        try:
            file_path = public_path_to_file(public_dir, site_path)
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue

        if not file_path.is_file():
            errors.append(f"{label}: missing published file {file_path}")
            continue

        actual_bytes = file_path.stat().st_size
        if item.get("bytes") != actual_bytes:
            errors.append(
                f"{label}: bytes mismatch for {site_path}: "
                f"expected {item.get('bytes')}, got {actual_bytes}"
            )

        actual_hash = sha256_file(file_path)
        if item.get("sha256") != actual_hash:
            errors.append(
                f"{label}: sha256 mismatch for {site_path}: "
                f"expected {item.get('sha256')}, got {actual_hash}"
            )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate website source and asset manifest paths."
    )
    parser.add_argument(
        "--public-dir",
        type=Path,
        default=Path("public"),
        help="Directory that maps to the website public root.",
    )
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=Path("public/files/manifests/source_manifest.json"),
    )
    parser.add_argument(
        "--asset-manifest",
        type=Path,
        default=Path("public/files/manifests/asset_manifest.json"),
    )
    parser.add_argument(
        "--source-only",
        action="store_true",
        help="Validate only source_manifest.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    public_dir = args.public_dir.resolve()
    source_manifest = load_json(args.source_manifest)

    errors = validate_source_manifest(source_manifest, public_dir)
    if not args.source_only:
        asset_manifest = load_json(args.asset_manifest)
        errors.extend(validate_asset_manifest(asset_manifest, public_dir, source_manifest))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Manifest validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
