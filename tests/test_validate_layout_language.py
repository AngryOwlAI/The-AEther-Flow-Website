from __future__ import annotations

from pathlib import Path

import validate_layout_language as validator

REPO_ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_minimal_layout_contract(root: Path, *, overview: str | None = None) -> None:
    for relative in validator.REQUIRED_PRIMITIVE_FILES:
        write(root / relative, "---\n---\n")

    for relative, contract in validator.MIGRATED_SURFACES.items():
        if relative == "src/pages/project/overview.astro" and overview is not None:
            write(root / relative, overview)
            continue
        write(root / relative, " ".join(contract["required"]))

    for relative in validator.EXPLICIT_EXCEPTIONS:
        write(root / relative, "diagram exception")


def test_current_layout_language_contract_passes() -> None:
    assert validator.validate_layout_language(REPO_ROOT) == []


def test_missing_primitive_fails(tmp_path: Path) -> None:
    write_minimal_layout_contract(tmp_path)
    (tmp_path / "src/components/EvidenceRail.astro").unlink()

    errors = validator.validate_layout_language(tmp_path)

    assert any("EvidenceRail.astro: missing" in error for error in errors)


def test_overview_card_grid_antipattern_fails(tmp_path: Path) -> None:
    write_minimal_layout_contract(
        tmp_path,
        overview='CommandBand EvidenceRail StatusDossier <div class="link-grid">',
    )

    errors = validator.validate_layout_language(tmp_path)

    assert any("forbidden overview anti-pattern" in error for error in errors)
