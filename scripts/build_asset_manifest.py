#!/usr/bin/env python3
"""Build asset_manifest.json data from source_manifest.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from validate_manifest_paths import load_json, public_path_to_file, sha256_file


def infer_asset_kind(kind: str) -> str:
    if kind in {"pdf", "tex", "image", "diagram"}:
        return kind
    return "other"


def build_asset_manifest(source_manifest: dict[str, Any], public_dir: Path) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for source_item in source_manifest.get("items", []):
        if not isinstance(source_item, dict):
            continue
        site_path = source_item["site_path"]
        file_path = public_path_to_file(public_dir, site_path)
        items.append(
            {
                "path": site_path,
                "kind": infer_asset_kind(str(source_item["kind"])),
                "bytes": file_path.stat().st_size,
                "sha256": sha256_file(file_path),
                "title": source_item["title"],
                "source_ref": f"source_manifest:{source_item['id']}",
            }
        )

    return {
        "version": 1,
        "generated_at": source_manifest.get("generated_at"),
        "items": items,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the website asset manifest.")
    parser.add_argument("--public-dir", type=Path, default=Path("public"))
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=Path("public/files/manifests/source_manifest.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("public/files/manifests/asset_manifest.json"),
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the generated manifest to --output. Default prints JSON only.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    public_dir = args.public_dir.resolve()
    source_manifest = load_json(args.source_manifest)
    generated = build_asset_manifest(source_manifest, public_dir)
    payload = json.dumps(generated, indent=2) + "\n"

    if args.write:
        args.output.write_text(payload, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
