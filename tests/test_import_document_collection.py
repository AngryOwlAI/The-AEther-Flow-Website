from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/import_document_collection.py"
SPEC = importlib.util.spec_from_file_location("import_document_collection", SCRIPT)
assert SPEC and SPEC.loader
IMPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORTER)

MANIFEST_SPEC = importlib.util.spec_from_file_location(
    "validate_manifest_paths",
    SCRIPT.with_name("validate_manifest_paths.py"),
)
CATALOG_SPEC = importlib.util.spec_from_file_location(
    "validate_document_catalog",
    SCRIPT.with_name("validate_document_catalog.py"),
)
assert MANIFEST_SPEC and MANIFEST_SPEC.loader and CATALOG_SPEC and CATALOG_SPEC.loader
MANIFEST_VALIDATOR = importlib.util.module_from_spec(MANIFEST_SPEC)
CATALOG_VALIDATOR = importlib.util.module_from_spec(CATALOG_SPEC)
MANIFEST_SPEC.loader.exec_module(MANIFEST_VALIDATOR)
CATALOG_SPEC.loader.exec_module(CATALOG_VALIDATOR)

GENERATED_AT = "2026-07-20T21:00:00+00:00"


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def make_fixture(tmp_path: Path) -> dict[str, object]:
    repo_root = tmp_path / "website"
    source_root = tmp_path / "source"
    public = repo_root / "public"
    foreign_path = public / "files/pdf/ontology/keep.pdf"
    foreign_path.parent.mkdir(parents=True)
    foreign_path.write_bytes(b"foreign ontology bytes")
    stale_path = public / "files/pdf/anthology/stale.pdf"
    stale_path.parent.mkdir(parents=True)
    stale_path.write_bytes(b"stale but retained")

    source_manifest = {
        "version": 1,
        "generated_at": "before",
        "source_repository": "AngryOwlAI/The-AEther-Flow",
        "items": [
            {
                "id": "ontology_pdf_keep",
                "site_path": "/files/pdf/ontology/keep.pdf",
                "kind": "pdf",
                "title": "Keep",
                "source_path": "ontology/keep.pdf",
                "approval_status": "approved",
                "sha256": hashlib.sha256(b"foreign ontology bytes").hexdigest(),
                "generated_by": "scripts/import_ontology_assets.py",
            },
            {
                "id": "anthology_stale",
                "site_path": "/files/pdf/anthology/stale.pdf",
                "kind": "pdf",
                "title": "Stale",
                "source_path": "anthology/stale.pdf",
                "approval_status": "approved",
                "sha256": hashlib.sha256(b"stale but retained").hexdigest(),
                "generated_by": IMPORTER.SCRIPT_ID,
            },
        ],
    }
    asset_manifest = {
        "version": 1,
        "generated_at": "before",
        "items": [
            {
                "path": "/files/pdf/ontology/keep.pdf",
                "kind": "pdf",
                "bytes": len(b"foreign ontology bytes"),
                "sha256": hashlib.sha256(b"foreign ontology bytes").hexdigest(),
                "title": "Keep",
                "source_ref": "source_manifest:ontology_pdf_keep",
            },
            {
                "path": "/files/pdf/anthology/stale.pdf",
                "kind": "pdf",
                "bytes": len(b"stale but retained"),
                "sha256": hashlib.sha256(b"stale but retained").hexdigest(),
                "title": "Stale",
                "source_ref": "source_manifest:anthology_stale",
            },
        ],
    }
    document_catalog = {
        "version": 1,
        "generated_at": "before",
        "documents": [
            {
                "id": "research:keep",
                "slug": "keep",
                "title": "Keep",
                "category": "research",
                "collection": "canonical-ontology",
                "summary": "Foreign document.",
                "status": "approved",
                "authority_scope": "registered_research_source",
                "manifestations": [
                    {
                        "kind": "pdf",
                        "site_path": "/files/pdf/ontology/keep.pdf",
                        "role": "readable_derivative",
                    }
                ],
            },
            {
                "id": "anthology:stale",
                "slug": "stale",
                "title": "Stale",
                "category": "anthology",
                "collection": "anthology",
                "summary": "Stale owned document.",
                "status": "approved",
                "authority_scope": "readable_derivative",
                "manifestations": [
                    {
                        "kind": "pdf",
                        "site_path": "/files/pdf/anthology/stale.pdf",
                        "role": "readable_derivative",
                    }
                ],
            },
        ],
    }
    source_manifest_path = public / "files/manifests/source_manifest.json"
    asset_manifest_path = public / "files/manifests/asset_manifest.json"
    document_catalog_path = public / "files/manifests/document_catalog.json"
    write_json(source_manifest_path, source_manifest)
    write_json(asset_manifest_path, asset_manifest)
    write_json(document_catalog_path, document_catalog)

    source_file = source_root / "anthology/volume-one.pdf"
    source_file.parent.mkdir(parents=True)
    source_file.write_bytes(b"registered anthology bytes")
    config = {
        "schema_version": IMPORTER.SCHEMA_VERSION,
        "collection": "anthology",
        "source_repository": "AngryOwlAI/The-AEther-Flow",
        "source_commit": "a" * 40,
        "ownership": {
            "document_id_prefix": "anthology:",
            "source_id_prefix": "anthology_",
            "site_path_prefixes": ["/files/pdf/anthology/"],
        },
        "documents": [
            {
                "id": "anthology:volume-one",
                "slug": "volume-one",
                "title": "Anthology Volume One",
                "category": "anthology",
                "summary": "A reviewed anthology volume.",
                "status": "approved",
                "authority_scope": "registered_source",
                "reading_order": 1,
                "manifestations": [
                    {
                        "kind": "pdf",
                        "role": "readable_derivative",
                        "source_id": "anthology_pdf_volume_one",
                        "source_path": "anthology/volume-one.pdf",
                        "site_path": "/files/pdf/anthology/volume-one.pdf",
                        "title": "Anthology Volume One PDF",
                        "approval_status": "approved",
                        "source_authority_status": "generated_noncanonical",
                        "reviewed_by": "website-publication-review",
                        "license_or_usage_note": "Approved for website publication.",
                    }
                ],
            }
        ],
    }
    config_path = repo_root / "collection.json"
    write_json(config_path, config)
    return {
        "repo_root": repo_root,
        "source_root": source_root,
        "source_manifest_path": source_manifest_path,
        "asset_manifest_path": asset_manifest_path,
        "document_catalog_path": document_catalog_path,
        "config_path": config_path,
        "config": config,
        "foreign_source": source_manifest["items"][0],
        "foreign_asset": asset_manifest["items"][0],
        "foreign_document": document_catalog["documents"][0],
    }


def run_import(fixture: dict[str, object]):
    return IMPORTER.import_collection(
        config_path=fixture["config_path"],
        repo_root=fixture["repo_root"],
        source_root=fixture["source_root"],
        source_manifest_path=fixture["source_manifest_path"],
        asset_manifest_path=fixture["asset_manifest_path"],
        document_catalog_path=fixture["document_catalog_path"],
        generated_at=GENERATED_AT,
    )


def test_import_preserves_foreign_rows_and_binds_public_identity(tmp_path: Path) -> None:
    fixture = make_fixture(tmp_path)
    source_manifest, asset_manifest, catalog, messages = run_import(fixture)

    assert source_manifest["items"][0] == fixture["foreign_source"]
    assert asset_manifest["items"][0] == fixture["foreign_asset"]
    assert catalog["documents"][0] == fixture["foreign_document"]
    assert {item["id"] for item in source_manifest["items"]} == {
        "ontology_pdf_keep",
        "anthology_pdf_volume_one",
    }
    imported_source = source_manifest["items"][1]
    imported_asset = asset_manifest["items"][1]
    imported_document = catalog["documents"][1]
    expected_bytes = b"registered anthology bytes"
    expected_hash = hashlib.sha256(expected_bytes).hexdigest()
    assert imported_source["sha256"] == expected_hash
    assert imported_source["generated_by"] == IMPORTER.SCRIPT_ID
    assert imported_asset["bytes"] == len(expected_bytes)
    assert imported_asset["sha256"] == expected_hash
    assert imported_asset["source_ref"] == (
        "source_manifest:anthology_pdf_volume_one"
    )
    assert imported_document["id"] == "anthology:volume-one"
    assert imported_document["collection"] == "anthology"
    assert imported_document["manifestations"] == [
        {
            "kind": "pdf",
            "site_path": "/files/pdf/anthology/volume-one.pdf",
            "role": "readable_derivative",
            "title": "Anthology Volume One PDF",
        }
    ]
    assert (
        fixture["repo_root"] / "public/files/pdf/anthology/volume-one.pdf"
    ).read_bytes() == expected_bytes
    assert messages == [
        "DRIFT: unexpected collection asset retained: "
        "/files/pdf/anthology/stale.pdf"
    ]
    public_dir = fixture["repo_root"] / "public"
    assert MANIFEST_VALIDATOR.validate_source_manifest(source_manifest, public_dir) == []
    assert (
        MANIFEST_VALIDATOR.validate_asset_manifest(
            asset_manifest, public_dir, source_manifest
        )
        == []
    )
    assert (
        CATALOG_VALIDATOR.validate_document_catalog(
            catalog, asset_manifest, source_manifest
        )
        == []
    )


def test_rerun_is_deterministic_for_fixed_inputs(tmp_path: Path) -> None:
    fixture = make_fixture(tmp_path)
    first = run_import(fixture)
    first_bytes = [
        fixture[name].read_bytes()
        for name in (
            "source_manifest_path",
            "asset_manifest_path",
            "document_catalog_path",
        )
    ]

    second = run_import(fixture)
    second_bytes = [
        fixture[name].read_bytes()
        for name in (
            "source_manifest_path",
            "asset_manifest_path",
            "document_catalog_path",
        )
    ]

    assert first[:3] == second[:3]
    assert first_bytes == second_bytes


@pytest.mark.parametrize(
    ("mutation", "match"),
    [
        (
            lambda config: config["documents"].append(
                copy.deepcopy(config["documents"][0])
            ),
            "duplicate id 'anthology:volume-one'",
        ),
        (
            lambda config: config["documents"][0]["manifestations"].append(
                copy.deepcopy(config["documents"][0]["manifestations"][0])
            ),
            "duplicate site_path '/files/pdf/anthology/volume-one.pdf'",
        ),
    ],
)
def test_duplicate_identity_fails_before_publication(
    tmp_path: Path, mutation, match: str
) -> None:
    fixture = make_fixture(tmp_path)
    config = fixture["config"]
    mutation(config)
    write_json(fixture["config_path"], config)

    with pytest.raises(ValueError, match=match):
        run_import(fixture)

    assert not (
        fixture["repo_root"] / "public/files/pdf/anthology/volume-one.pdf"
    ).exists()


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("approval_status", "draft", "approval_status: must be 'approved'"),
        ("source_authority_status", "", "source_authority_status"),
    ],
)
def test_unapproved_or_ambiguous_source_status_fails_closed(
    tmp_path: Path, field: str, value: str, match: str
) -> None:
    fixture = make_fixture(tmp_path)
    fixture["config"]["documents"][0]["manifestations"][0][field] = value
    write_json(fixture["config_path"], fixture["config"])

    with pytest.raises(ValueError, match=match):
        run_import(fixture)

    assert not (
        fixture["repo_root"] / "public/files/pdf/anthology/volume-one.pdf"
    ).exists()


def test_ambiguous_existing_ownership_fails_closed(tmp_path: Path) -> None:
    fixture = make_fixture(tmp_path)
    source_manifest = json.loads(fixture["source_manifest_path"].read_text())
    source_manifest["items"][1]["generated_by"] = "another_importer.py"
    write_json(fixture["source_manifest_path"], source_manifest)

    with pytest.raises(ValueError, match="ambiguous collection ownership"):
        run_import(fixture)

    assert not (
        fixture["repo_root"] / "public/files/pdf/anthology/volume-one.pdf"
    ).exists()


def test_missing_registered_source_fails_before_publication(tmp_path: Path) -> None:
    fixture = make_fixture(tmp_path)
    (fixture["source_root"] / "anthology/volume-one.pdf").unlink()

    with pytest.raises(FileNotFoundError, match="missing registered source file"):
        run_import(fixture)

    assert not (
        fixture["repo_root"] / "public/files/pdf/anthology/volume-one.pdf"
    ).exists()
