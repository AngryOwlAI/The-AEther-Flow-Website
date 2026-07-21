from __future__ import annotations

from pathlib import Path

import validate_manifest_paths as validator

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = REPO_ROOT / "public"
SOURCE_MANIFEST = REPO_ROOT / "public/files/manifests/source_manifest.json"
ASSET_MANIFEST = REPO_ROOT / "public/files/manifests/asset_manifest.json"


def write_public_file(public_dir: Path, site_path: str) -> Path:
    path = public_dir / site_path.removeprefix("/")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Approved governance document\n", encoding="utf-8")
    return path


def markdown_source_item(**overrides: object) -> dict[str, object]:
    return {
        "id": "governance-document",
        "site_path": "/files/markdown/governance/document.md",
        "kind": "markdown",
        "title": "Governance document",
        "source_path": "governance/document.md",
        "approval_status": "approved",
        **overrides,
    }


def source_manifest_with(item: dict[str, object]) -> dict[str, object]:
    return {
        "version": 1,
        "generated_at": "2026-07-20T00:00:00Z",
        "source_repository": "repository",
        "items": [item],
    }


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


def test_approved_governance_markdown_source_and_asset_validate(
    tmp_path: Path,
) -> None:
    source_item = markdown_source_item()
    source_manifest = source_manifest_with(source_item)
    published = write_public_file(tmp_path, str(source_item["site_path"]))
    asset_manifest = {
        "version": 1,
        "generated_at": "2026-07-20T00:00:00Z",
        "items": [
            {
                "path": source_item["site_path"],
                "kind": "markdown",
                "bytes": published.stat().st_size,
                "sha256": validator.sha256_file(published),
                "title": source_item["title"],
                "source_ref": f"source_manifest:{source_item['id']}",
            }
        ],
    }

    assert validator.validate_source_manifest(source_manifest, tmp_path) == []
    assert (
        validator.validate_asset_manifest(asset_manifest, tmp_path, source_manifest)
        == []
    )


def test_invalid_markdown_source_records_fail_closed(tmp_path: Path) -> None:
    cases = [
        markdown_source_item(approval_status="draft"),
        markdown_source_item(site_path="/files/markdown/document.md"),
        markdown_source_item(source_path="/Users/example/private/document.md"),
        markdown_source_item(source_path="C:/Users/example/private/document.md"),
        markdown_source_item(source_path="../private/document.md"),
    ]

    for item in cases:
        write_public_file(tmp_path, str(item["site_path"]))
        errors = validator.validate_source_manifest(source_manifest_with(item), tmp_path)
        assert any("Markdown" in error for error in errors)
