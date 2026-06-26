from __future__ import annotations

from pathlib import Path

import validate_page_provenance as validator

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
ROUTE_MAP = REPO_ROOT / "public/files/manifests/page_route_map.json"
PAGE_PROVENANCE = REPO_ROOT / "public/files/manifests/page_provenance.json"


def test_current_page_provenance_validates() -> None:
    route_map = validator.load_json(ROUTE_MAP)
    provenance = validator.load_json(PAGE_PROVENANCE)

    errors = validator.validate_route_map(route_map)
    errors.extend(
        validator.validate_page_provenance(
            provenance,
            route_map,
            repo_root=REPO_ROOT,
            source_root=SOURCE_ROOT,
        )
    )

    assert errors == []


def test_page_hash_drift_fails_closed() -> None:
    route_map = validator.load_json(ROUTE_MAP)
    provenance = validator.load_json(PAGE_PROVENANCE)
    broken = {
        **provenance,
        "pages": [
            {
                **provenance["pages"][0],
                "local_page_sha256": "0" * 64,
            },
            *provenance["pages"][1:],
        ],
    }

    errors = validator.validate_page_provenance(
        broken,
        route_map,
        repo_root=REPO_ROOT,
        source_root=SOURCE_ROOT,
    )

    assert any("local page sha256 drift" in error for error in errors)
