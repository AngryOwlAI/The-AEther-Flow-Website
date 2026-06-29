from __future__ import annotations

from pathlib import Path

import validate_layout_language as validator

REPO_ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_minimal_layout_contract(root: Path, *, home: str | None = None) -> None:
    for relative in validator.REQUIRED_PRIMITIVE_FILES:
        write(root / relative, "---\n---\n")

    for relative, contract in validator.MIGRATED_SURFACES.items():
        if relative == "src/pages/index.astro" and home is not None:
            write(root / relative, home)
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


def test_home_card_grid_antipattern_fails(tmp_path: Path) -> None:
    write_minimal_layout_contract(
        tmp_path,
        home='CommandBand EvidenceRail StatusDossier <div class="link-grid">',
    )

    errors = validator.validate_layout_language(tmp_path)

    assert any("forbidden overview anti-pattern" in error for error in errors)


def test_resource_source_authority_section_fails(tmp_path: Path) -> None:
    write_minimal_layout_contract(tmp_path)
    write(
        tmp_path / "src/pages/resources/reviewer-packet/index.astro",
        "\n".join(
            [
                "---",
                "import SourceAuthoritySection from "
                '"../../../components/SourceAuthoritySection.astro";',
                "---",
                "<SourceAuthoritySection />",
            ]
        ),
    )

    errors = validator.validate_layout_language(tmp_path)

    assert any(
        "Library resource pages must not render dedicated Source authority sections" in error
        and "SourceAuthoritySection component" in error
        for error in errors
    )


def test_nested_resource_direct_source_notice_fails(tmp_path: Path) -> None:
    write_minimal_layout_contract(tmp_path)
    write(
        tmp_path / "src/pages/resources/guided-starts/general-public/index.astro",
        "\n".join(
            [
                "---",
                'import SourceNotice from "../../../../components/SourceNotice.astro";',
                "---",
                "<SourceNotice />",
            ]
        ),
    )

    errors = validator.validate_layout_language(tmp_path)

    assert any(
        "Library resource pages must not render dedicated Source authority sections" in error
        and "direct SourceNotice component" in error
        for error in errors
    )


def test_resource_source_authority_prose_is_allowed(tmp_path: Path) -> None:
    write_minimal_layout_contract(tmp_path)
    write(
        tmp_path / "src/pages/resources/guided-starts/general-public/index.astro",
        "EvidenceRail StatusDossier source authority remains a contextual prose boundary.",
    )

    errors = validator.validate_layout_language(tmp_path)

    assert errors == []
