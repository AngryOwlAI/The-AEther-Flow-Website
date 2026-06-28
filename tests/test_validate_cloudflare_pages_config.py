from __future__ import annotations

from pathlib import Path

import validate_cloudflare_pages_config as validator

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_current_cloudflare_pages_config_validates() -> None:
    header_errors = validator.validate_headers(REPO_ROOT / "public/_headers")
    redirect_errors = validator.validate_redirects(REPO_ROOT / "public/_redirects")

    assert header_errors == []
    assert redirect_errors == []


def test_project_overview_redirects_to_home() -> None:
    redirects = [line for _, line in validator.meaningful_lines(REPO_ROOT / "public/_redirects")]

    assert "/project/overview/ / 301" in redirects
    assert "/overview / 301" in redirects


def test_redirect_validator_rejects_invalid_status(tmp_path: Path) -> None:
    redirects = tmp_path / "_redirects"
    redirects.write_text("/old /new 999\n", encoding="utf-8")

    errors = validator.validate_redirects(redirects)

    assert any("unsupported redirect status" in error for error in errors)
