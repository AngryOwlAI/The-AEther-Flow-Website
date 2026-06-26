#!/usr/bin/env python3
"""Import the canonical ontology PDF and TeX package into public assets."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DEFAULT_SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
DOCUMENT_ORDER = [
    "aether_flow_foundations",
    "aether_flow_dynamics",
    "aether_flow_geometry",
    "aether_flow_relativistic_recovery",
    "aether_flow_consistency",
    "aether_flow_exact_closure_note",
    "aether_flow_exact_closure_sequence_overview",
    "aether_flow_exact_closure_flagship_article",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_output(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return result.stdout.strip() or None


def title_from_slug(slug: str) -> str:
    special = {"gr": "GR", "aether": "AEther"}
    words = []
    for word in slug.split("_"):
        words.append(special.get(word, word.capitalize()))
    return " ".join(words)


def load_tex_registry(source_root: Path) -> dict[str, dict[str, str]]:
    registry_path = source_root / "registries/TEX_SOURCE_REGISTRY.csv"
    if not registry_path.is_file():
        return {}
    rows: dict[str, dict[str, str]] = {}
    with registry_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            path = row.get("path")
            if path:
                rows[path] = row
    return rows


def keep_non_document_item(item: dict[str, Any]) -> bool:
    return item.get("kind") not in {"pdf", "tex"}


def import_assets(
    *,
    repo_root: Path,
    source_root: Path,
    source_manifest_path: Path,
    asset_manifest_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    source_manifest = load_json(source_manifest_path)
    asset_manifest = load_json(asset_manifest_path)
    generated_at = datetime.now(tz=UTC).isoformat()
    source_commit = git_output(source_root, "rev-parse", "HEAD")
    registry_rows = load_tex_registry(source_root)

    public_dir = repo_root / "public"
    pdf_dest_dir = public_dir / "files/pdf/ontology"
    tex_dest_dir = public_dir / "files/tex/ontology"
    pdf_dest_dir.mkdir(parents=True, exist_ok=True)
    tex_dest_dir.mkdir(parents=True, exist_ok=True)

    new_source_items = [
        item
        for item in source_manifest.get("items", [])
        if isinstance(item, dict) and keep_non_document_item(item)
    ]
    new_asset_items = [
        item
        for item in asset_manifest.get("items", [])
        if isinstance(item, dict) and keep_non_document_item(item)
    ]

    expected_destinations: set[Path] = set()
    messages: list[str] = []
    for slug in DOCUMENT_ORDER:
        title = title_from_slug(slug)
        for kind, source_dir, dest_dir, extension in (
            ("pdf", source_root / "ontology/pdfs", pdf_dest_dir, ".pdf"),
            ("tex", source_root / "ontology/tex", tex_dest_dir, ".tex"),
        ):
            source_file = source_dir / f"{slug}{extension}"
            if not source_file.is_file():
                raise FileNotFoundError(f"missing upstream ontology asset: {source_file}")
            dest_file = dest_dir / source_file.name
            shutil.copy2(source_file, dest_file)
            expected_destinations.add(dest_file)

            source_relative = f"ontology/{'pdfs' if kind == 'pdf' else 'tex'}/{source_file.name}"
            site_path = f"/files/{kind}/ontology/{source_file.name}"
            file_hash = sha256_file(dest_file)
            source_id = f"ontology_{kind}_{slug}"
            registry_row = registry_rows.get(source_relative, {})
            if kind == "tex":
                notes = (
                    "Registered TeX source for the canonical ontology package. "
                    "Claim status remains governed by upstream registry metadata."
                )
            else:
                notes = (
                    "Generated human-readable PDF derivative of the canonical ontology "
                    "TeX source; do not treat as independent source authority."
                )

            new_source_items.append(
                {
                    "id": source_id,
                    "site_path": site_path,
                    "kind": kind,
                    "title": f"{title} {'PDF' if kind == 'pdf' else 'TeX'}",
                    "source_path": source_relative,
                    "source_commit": source_commit,
                    "approval_status": "approved",
                    "sha256": file_hash,
                    "generated_by": "scripts/import_ontology_assets.py",
                    "generated_at": generated_at,
                    "license_or_usage_note": "Website publication of canonical ontology package assets.",
                    "notes": notes,
                    "source_authority_status": registry_row.get("authority_status", "canonical"),
                    "claim_status": registry_row.get("claim_status"),
                    "research_status": registry_row.get("research_status"),
                    "ontology_promotion_status": registry_row.get("ontology_promotion_status"),
                }
            )
            new_asset_items.append(
                {
                    "path": site_path,
                    "kind": kind,
                    "bytes": dest_file.stat().st_size,
                    "sha256": file_hash,
                    "title": f"{title} {'PDF' if kind == 'pdf' else 'TeX'}",
                    "source_ref": f"source_manifest:{source_id}",
                }
            )

    for dest_dir in (pdf_dest_dir, tex_dest_dir):
        for published in dest_dir.iterdir():
            if published.is_file() and published not in expected_destinations:
                messages.append(f"DRIFT: unexpected published ontology asset retained: {published}")

    source_manifest = {
        **source_manifest,
        "version": 1,
        "generated_at": generated_at,
        "source_repository": "AngryOwlAI/The-AEther-Flow",
        "items": new_source_items,
    }
    asset_manifest = {
        **asset_manifest,
        "version": 1,
        "generated_at": generated_at,
        "items": new_asset_items,
    }
    return source_manifest, asset_manifest, messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    source_manifest_path = (
        args.source_manifest if args.source_manifest.is_absolute() else repo_root / args.source_manifest
    )
    asset_manifest_path = (
        args.asset_manifest if args.asset_manifest.is_absolute() else repo_root / args.asset_manifest
    )
    source_manifest, asset_manifest, messages = import_assets(
        repo_root=repo_root,
        source_root=args.source_root,
        source_manifest_path=source_manifest_path,
        asset_manifest_path=asset_manifest_path,
    )
    write_json(source_manifest_path, source_manifest)
    write_json(asset_manifest_path, asset_manifest)
    for message in messages:
        print(message)
    print("Imported canonical ontology PDF/TeX assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
