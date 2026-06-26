from __future__ import annotations

from pathlib import Path

import validate_svg_policy as validator

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_current_svg_sources_follow_textless_animation_policy() -> None:
    assert validator.validate_svg_policy(REPO_ROOT) == []


def test_visible_svg_text_fails(tmp_path: Path) -> None:
    page = tmp_path / "src/pages/example.astro"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<svg viewBox="0 0 100 100"><path class="track-figure-path" d="M0 0h50" />'
        "<text x=\"10\" y=\"10\">label</text></svg>",
        encoding="utf-8",
    )

    errors = validator.validate_svg_policy(tmp_path)

    assert any("visible SVG <text>" in error for error in errors)


def test_svg_without_animation_hook_fails(tmp_path: Path) -> None:
    page = tmp_path / "src/pages/example.astro"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="10" /></svg>',
        encoding="utf-8",
    )

    errors = validator.validate_svg_policy(tmp_path)

    assert any("animation hook" in error for error in errors)


def test_textless_accessible_animated_svg_passes(tmp_path: Path) -> None:
    page = tmp_path / "src/pages/example.astro"
    page.parent.mkdir(parents=True)
    page.write_text(
        '<svg viewBox="0 0 100 100" role="img" aria-labelledby="title desc">'
        '<title id="title">Accessible name</title>'
        '<desc id="desc">Accessible description.</desc>'
        '<path class="track-figure-path" d="M0 50h100" />'
        "</svg>",
        encoding="utf-8",
    )

    assert validator.validate_svg_policy(tmp_path) == []
