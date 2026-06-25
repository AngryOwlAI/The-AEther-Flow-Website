from __future__ import annotations

from pathlib import Path

import validate_manifest_paths as validator

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = REPO_ROOT / "public"
SOURCE_MANIFEST = REPO_ROOT / "public/files/manifests/source_manifest.json"
ASSET_MANIFEST = REPO_ROOT / "public/files/manifests/asset_manifest.json"


def test_current_manifests_validate() -> None:
    source_manifest = validator.load_json(SOURCE_MANIFEST)
    asset_manifest = validator.load_json(ASSET_MANIFEST)

    source_errors = validator.validate_source_manifest(source_manifest, PUBLIC_DIR)
    asset_errors = validator.validate_asset_manifest(asset_manifest, PUBLIC_DIR, source_manifest)

    assert source_errors == []
    assert asset_errors == []


def test_missing_source_manifest_file_fails_closed() -> None:
    source_manifest = validator.load_json(SOURCE_MANIFEST)
    broken_manifest = {
        **source_manifest,
        "items": [
            {
                **source_manifest["items"][0],
                "site_path": "/files/pdf/does-not-exist.pdf",
            }
        ],
    }

    errors = validator.validate_source_manifest(broken_manifest, PUBLIC_DIR)

    assert any("missing published file" in error for error in errors)
