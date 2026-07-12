from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/import_ontology_assets.py"
SPEC = importlib.util.spec_from_file_location("import_ontology_assets", SCRIPT)
assert SPEC and SPEC.loader
IMPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORTER)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def write_registry(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


def test_importer_uses_kind_specific_authority_registry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "website"
    source_root = tmp_path / "upstream"
    slug = "aether_flow_exact_closure_note"
    tex_path = f"ontology/tex/{slug}.tex"
    pdf_path = f"ontology/pdfs/{slug}.pdf"

    (source_root / tex_path).parent.mkdir(parents=True)
    (source_root / tex_path).write_text("registered TeX source", encoding="utf-8")
    (source_root / pdf_path).parent.mkdir(parents=True)
    (source_root / pdf_path).write_bytes(b"generated PDF derivative")

    write_registry(
        source_root / "registries/TEX_SOURCE_REGISTRY.csv",
        {
            "path": tex_path,
            "authority_status": "canonical",
            "claim_status": "benchmark_claim",
            "research_status": "canonical_ontology",
            "ontology_promotion_status": "accepted",
        },
    )
    write_registry(
        source_root / "registries/PDF_DERIVATIVE_REGISTRY.csv",
        {
            "path": pdf_path,
            "authority_status": "generated_noncanonical",
            "claim_status": "",
            "research_status": "",
            "ontology_promotion_status": "",
        },
    )

    source_manifest_path = repo_root / "public/files/manifests/source_manifest.json"
    asset_manifest_path = repo_root / "public/files/manifests/asset_manifest.json"
    write_json(source_manifest_path, {"version": 1, "items": []})
    write_json(asset_manifest_path, {"version": 1, "items": []})

    monkeypatch.setattr(IMPORTER, "DOCUMENT_ORDER", [slug])
    monkeypatch.setattr(
        IMPORTER,
        "git_output",
        lambda _repo, *args: "a" * 40 if args == ("rev-parse", "HEAD") else None,
    )

    source_manifest, _, messages = IMPORTER.import_assets(
        repo_root=repo_root,
        source_root=source_root,
        source_manifest_path=source_manifest_path,
        asset_manifest_path=asset_manifest_path,
    )

    items = {item["kind"]: item for item in source_manifest["items"]}
    assert items["tex"]["source_authority_status"] == "canonical"
    assert items["tex"]["claim_status"] == "benchmark_claim"
    assert items["pdf"]["source_authority_status"] == "generated_noncanonical"
    assert messages == []


def test_importer_fails_closed_when_registry_row_is_missing() -> None:
    with pytest.raises(
        ValueError,
        match="PDF_DERIVATIVE_REGISTRY.csv: missing registry row",
    ):
        IMPORTER.require_registry_row(
            {},
            "ontology/pdfs/missing.pdf",
            "PDF_DERIVATIVE_REGISTRY.csv",
        )
