from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

import validate_document_catalog as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_ROOT = REPO_ROOT / "public/files/manifests"
CATALOG = MANIFEST_ROOT / "document_catalog.json"
ASSET_MANIFEST = MANIFEST_ROOT / "asset_manifest.json"
SOURCE_MANIFEST = MANIFEST_ROOT / "source_manifest.json"
IMPORTER_PATH = REPO_ROOT / "scripts/import_document_collection.py"
IMPORTER_SPEC = importlib.util.spec_from_file_location(
    "import_document_collection_for_catalog_tests", IMPORTER_PATH
)
assert IMPORTER_SPEC and IMPORTER_SPEC.loader
IMPORTER = importlib.util.module_from_spec(IMPORTER_SPEC)
IMPORTER_SPEC.loader.exec_module(IMPORTER)


def load_current_manifests() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    return (
        validator.load_json(CATALOG),
        validator.load_json(ASSET_MANIFEST),
        validator.load_json(SOURCE_MANIFEST),
    )


def load_typescript_documents() -> list[dict[str, object]]:
    script = r"""
import { createServer } from "vite";

const server = await createServer({
  root: process.cwd(),
  server: { middlewareMode: true },
  appType: "custom",
  logLevel: "silent",
});

try {
  const module = await server.ssrLoadModule("/src/lib/documents.ts");
  process.stdout.write(JSON.stringify(module.documents));
} finally {
  await server.close();
}
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_current_catalog_groups_formats_without_flattening_roles() -> None:
    catalog, asset_manifest, source_manifest = load_current_manifests()

    assert (
        validator.validate_document_catalog(catalog, asset_manifest, source_manifest)
        == []
    )
    documents = catalog["documents"]
    assert isinstance(documents, list)
    overview = next(
        document
        for document in documents
        if document["id"] == "research:aether-flow-exact-closure-sequence-overview"
    )
    assert {
        (manifestation["kind"], manifestation["role"])
        for manifestation in overview["manifestations"]
    } == {
        ("tex", "authoritative_source"),
        ("pdf", "readable_derivative"),
    }
    assert all(
        not ({"bytes", "sha256", "source_id", "source_path"} & manifestation.keys())
        for document in documents
        for manifestation in document["manifestations"]
    )


def test_typescript_domain_module_exposes_logical_documents() -> None:
    documents = load_typescript_documents()

    assert len(documents) == 8
    assert len({document["id"] for document in documents}) == 8
    assert all(document["category"] == "research" for document in documents)
    assert all(len(document["manifestations"]) == 2 for document in documents)


def test_catalog_rejects_unknown_assets_and_duplicate_logical_ids() -> None:
    catalog, asset_manifest, source_manifest = load_current_manifests()
    broken = copy.deepcopy(catalog)
    broken["documents"][0]["manifestations"][0]["site_path"] = (
        "/files/tex/ontology/not-published.tex"
    )
    broken["documents"].append(copy.deepcopy(broken["documents"][0]))

    errors = validator.validate_document_catalog(
        broken, asset_manifest, source_manifest
    )

    assert any("missing asset record" in error for error in errors)
    assert any("duplicate value 'research:" in error for error in errors)


def test_catalog_rejects_duplicated_authority_data_and_unknown_sources() -> None:
    catalog, asset_manifest, source_manifest = load_current_manifests()
    broken_catalog = copy.deepcopy(catalog)
    broken_catalog["documents"][0]["manifestations"][0]["sha256"] = "0" * 64
    broken_assets = copy.deepcopy(asset_manifest)
    target_path = broken_catalog["documents"][0]["manifestations"][0]["site_path"]
    target_asset = next(
        asset for asset in broken_assets["items"] if asset["path"] == target_path
    )
    target_asset["source_ref"] = "source_manifest:not-present"

    errors = validator.validate_document_catalog(
        broken_catalog, broken_assets, source_manifest
    )

    assert any("duplicates manifest authority fields: sha256" in error for error in errors)
    assert any("asset source is unknown" in error for error in errors)


def governance_records() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    site_path = "/files/markdown/governance/publication-policy.md"
    catalog = {
        "version": 1,
        "generated_at": "2026-07-20T00:00:00Z",
        "documents": [
            {
                "id": "governance:publication-policy",
                "slug": "publication-policy",
                "title": "Publication Policy",
                "category": "governance",
                "summary": "Reviewed public governance policy.",
                "status": "approved",
                "authority_scope": "governance_source",
                "manifestations": [
                    {
                        "kind": "markdown",
                        "site_path": site_path,
                        "role": "governance_source",
                    }
                ],
            }
        ],
    }
    assets = {
        "items": [
            {
                "path": site_path,
                "kind": "markdown",
                "source_ref": "source_manifest:governance_publication_policy",
            }
        ]
    }
    sources = {
        "items": [
            {
                "id": "governance_publication_policy",
                "site_path": site_path,
                "kind": "markdown",
                "approval_status": "approved",
                "reviewed_by": "website-publication-review",
                "license_or_usage_note": "Approved for public website distribution.",
            }
        ]
    }
    return catalog, assets, sources


def test_governance_markdown_catalog_requires_approved_reviewed_source() -> None:
    catalog, assets, sources = governance_records()
    assert validator.validate_document_catalog(catalog, assets, sources) == []

    sources["items"][0]["approval_status"] = "draft"
    sources["items"][0]["reviewed_by"] = ""
    errors = validator.validate_document_catalog(catalog, assets, sources)

    assert any("linked governance source is not approved" in error for error in errors)
    assert any("requires reviewed_by" in error for error in errors)

    catalog["documents"][0]["category"] = "research"
    errors = validator.validate_document_catalog(catalog, assets, sources)
    assert any("public Markdown requires governance category" in error for error in errors)


def test_governance_markdown_import_requires_exact_reviewed_allowlist(
    tmp_path: Path,
) -> None:
    source = tmp_path / "publication-policy.md"
    source.write_text("# Public publication policy\n", encoding="utf-8")
    document = {"status": "approved"}
    item = {
        "kind": "markdown",
        "role": "governance_source",
        "source_path": "governance/publication-policy.md",
        "site_path": "/files/markdown/governance/publication-policy.md",
        "reviewed_by": "website-publication-review",
    }
    allowlist = IMPORTER.governance_markdown_allowlist(
        [
            {
                "source_path": item["source_path"],
                "site_path": item["site_path"],
                "reviewed_by": item["reviewed_by"],
                "current_state_reviewed": True,
            }
        ]
    )

    assert IMPORTER.validate_governance_markdown_source(
        document=document,
        item=item,
        source_file=source,
        allowlist=allowlist,
        label="manifestation",
    ) == (item["source_path"], item["site_path"])

    with pytest.raises(ValueError, match="missing explicit governance Markdown allowlist"):
        IMPORTER.validate_governance_markdown_source(
            document=document,
            item=item,
            source_file=source,
            allowlist={},
            label="manifestation",
        )


@pytest.mark.parametrize(
    "content",
    [
        "API_KEY = abcdefghijklmnop",
        "Maintainer: private.person@company.test",
        "Local checkout: /Users/operator/private-project",
        "Read implementation_control/program_state.yaml",
        "Status: internal-only",
        "Raw source: https://raw.githubusercontent.com/org/repo/main/private.md",
    ],
)
def test_governance_markdown_import_denies_private_or_operational_content(
    tmp_path: Path, content: str
) -> None:
    source = tmp_path / "publication-policy.md"
    source.write_text(content, encoding="utf-8")
    item = {
        "role": "governance_source",
        "source_path": "governance/publication-policy.md",
        "site_path": "/files/markdown/governance/publication-policy.md",
        "reviewed_by": "website-publication-review",
    }
    allowlist = {
        (item["source_path"], item["site_path"]): {
            "reviewed_by": item["reviewed_by"]
        }
    }

    with pytest.raises(ValueError, match="governance Markdown contains denied"):
        IMPORTER.validate_governance_markdown_source(
            document={"status": "approved"},
            item=item,
            source_file=source,
            allowlist=allowlist,
            label="manifestation",
        )


def test_governance_markdown_headers_preserve_security_policy() -> None:
    headers = (REPO_ROOT / "public/_headers").read_text(encoding="utf-8")
    rule = headers.split("/files/markdown/governance/*", 1)[1].split(
        "/files/manifests/*", 1
    )[0]

    assert "Content-Type: text/markdown; charset=utf-8" in rule
    assert "X-Content-Type-Options: nosniff" in rule
    assert "Referrer-Policy: strict-origin-when-cross-origin" in rule
    assert "X-Frame-Options: SAMEORIGIN" in rule
    assert "Permissions-Policy: camera=(), microphone=(), geolocation=()" in rule
