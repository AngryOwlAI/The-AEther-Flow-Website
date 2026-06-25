from __future__ import annotations

from pathlib import Path

import quality_gate


def test_route_for_root_index() -> None:
    dist = Path("/tmp/site/dist")
    assert quality_gate.route_for_html(dist, dist / "index.html") == "/"


def test_url_path_to_dist_path_for_directory_route() -> None:
    dist = Path("/tmp/site/dist")
    assert quality_gate.url_path_to_dist_path(dist, "/resources/") == dist / "resources/index.html"


def test_internal_link_validator_reports_missing_target(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text('<a href="/missing/">Missing</a>', encoding="utf-8")

    errors = quality_gate.validate_internal_links(dist)

    assert any("broken href" in error for error in errors)
