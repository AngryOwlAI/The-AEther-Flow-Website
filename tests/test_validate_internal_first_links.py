from __future__ import annotations

from pathlib import Path

import validate_internal_first_links as validator

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_current_pages_do_not_use_mapped_github_links_as_primary_journey() -> None:
    assert validator.validate_internal_first_links(REPO_ROOT) == []


def test_mapped_github_link_fails_outside_allowed_source_page(tmp_path: Path) -> None:
    page = tmp_path / "src/pages/example.astro"
    page.parent.mkdir(parents=True)
    page.write_text(
        '---\n---\n<a href="https://github.com/AngryOwlAI/The-AEther-Flow/blob/main/'
        'github-facing/project-overview-explainer.md">source</a>\n',
        encoding="utf-8",
    )

    errors = validator.validate_internal_first_links(tmp_path)

    assert any("mapped GitHub explainer URL" in error for error in errors)


def test_mapped_github_link_fails_in_lib_data(tmp_path: Path) -> None:
    data = tmp_path / "src/lib/routes.ts"
    data.parent.mkdir(parents=True)
    data.write_text(
        "export const routes = [{ href: "
        "'https://github.com/AngryOwlAI/The-AEther-Flow/blob/main/"
        "github-facing/claim-gates-explainer.md' }];\n",
        encoding="utf-8",
    )

    errors = validator.validate_internal_first_links(tmp_path)

    assert any("src/lib/routes.ts" in error for error in errors)
