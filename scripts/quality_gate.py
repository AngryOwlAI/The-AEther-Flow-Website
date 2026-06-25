#!/usr/bin/env python3
"""Run artifact-level quality checks for the static website build."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

HTML_ROUTES_REQUIRING_SOURCE_NOTICE = {
    "/project/overview/",
    "/research/map/",
    "/research/equations/",
    "/research/math-sample/",
    "/resources/",
    "/resources/documents/",
    "/resources/diagrams/",
}
ROUTES_REQUIRING_KATEX = {
    "/research/equations/",
    "/research/math-sample/",
}
FORBIDDEN_RENDERED_SNIPPETS = {
    "/Volumes/P-SSD/AngryOwl/The-AEther-Flow",
}


@dataclass(frozen=True)
class LinkRef:
    source: Path
    attribute: str
    value: str


class LinkCollector(HTMLParser):
    def __init__(self, source: Path) -> None:
        super().__init__()
        self.source = source
        self.links: list[LinkRef] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            if name in {"href", "src"}:
                self.links.append(LinkRef(self.source, name, value))


def route_for_html(dist_dir: Path, html_path: Path) -> str:
    relative = html_path.relative_to(dist_dir)
    if relative.name != "index.html":
        return "/" + relative.as_posix()
    parent = relative.parent.as_posix()
    if parent == ".":
        return "/"
    return "/" + parent.rstrip("/") + "/"


def url_path_to_dist_path(dist_dir: Path, url_path: str) -> Path:
    path = unquote(url_path.split("#", 1)[0].split("?", 1)[0])
    if path == "/":
        return dist_dir / "index.html"
    relative = path.removeprefix("/")
    candidate = dist_dir / relative
    if path.endswith("/"):
        return candidate / "index.html"
    if candidate.exists():
        return candidate
    return candidate / "index.html"


def collect_html_links(dist_dir: Path) -> list[LinkRef]:
    links: list[LinkRef] = []
    for html_path in sorted(dist_dir.rglob("*.html")):
        parser = LinkCollector(html_path)
        parser.feed(html_path.read_text(encoding="utf-8"))
        links.extend(parser.links)
    return links


def validate_internal_links(dist_dir: Path) -> list[str]:
    errors: list[str] = []
    for ref in collect_html_links(dist_dir):
        parsed = urlparse(ref.value)
        if parsed.scheme or parsed.netloc or ref.value.startswith(("mailto:", "tel:", "#")):
            continue
        if parsed.path == "":
            continue
        target = url_path_to_dist_path(dist_dir, parsed.path)
        if not target.exists():
            errors.append(f"{ref.source}: broken {ref.attribute}={ref.value!r}")
    return errors


def load_manifest(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected object")
    return data


def validate_manifest_assets(dist_dir: Path) -> list[str]:
    errors: list[str] = []
    asset_manifest = load_manifest(dist_dir / "files/manifests/asset_manifest.json")
    items = asset_manifest.get("items")
    if not isinstance(items, list):
        return ["dist asset manifest items must be a list"]
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"asset_manifest.items[{index}]: expected object")
            continue
        path = item.get("path")
        source_ref = item.get("source_ref")
        if not isinstance(path, str) or not isinstance(source_ref, str):
            errors.append(f"asset_manifest.items[{index}]: path and source_ref are required")
            continue
        target = url_path_to_dist_path(dist_dir, path)
        if not target.exists():
            errors.append(f"asset_manifest.items[{index}]: missing built asset {path}")
        if not source_ref.startswith("source_manifest:"):
            errors.append(f"asset_manifest.items[{index}]: invalid source_ref {source_ref!r}")
    return errors


def validate_source_notices(dist_dir: Path) -> list[str]:
    errors: list[str] = []
    for route in sorted(HTML_ROUTES_REQUIRING_SOURCE_NOTICE):
        html_path = url_path_to_dist_path(dist_dir, route)
        text = html_path.read_text(encoding="utf-8")
        if "Source authority" not in text or "Claim status" not in text:
            errors.append(f"{route}: missing visible source authority notice or claim status")
    return errors


def validate_equation_rendering(dist_dir: Path) -> list[str]:
    errors: list[str] = []
    for route in sorted(ROUTES_REQUIRING_KATEX):
        html_path = url_path_to_dist_path(dist_dir, route)
        text = html_path.read_text(encoding="utf-8")
        katex_count = len(re.findall(r'class="[^"]*katex', text))
        if katex_count == 0:
            errors.append(f"{route}: expected rendered KaTeX markup")
    return errors


def validate_no_local_path_leaks(dist_dir: Path) -> list[str]:
    errors: list[str] = []
    for html_path in sorted(dist_dir.rglob("*.html")):
        text = html_path.read_text(encoding="utf-8")
        for snippet in FORBIDDEN_RENDERED_SNIPPETS:
            if snippet in text:
                errors.append(f"{html_path}: rendered local source path leak {snippet!r}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local static-site quality gate checks.")
    parser.add_argument("--dist-dir", type=Path, default=Path("dist"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dist_dir = args.dist_dir.resolve()
    if not dist_dir.is_dir():
        print(f"ERROR: {dist_dir}: dist directory does not exist", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors.extend(validate_internal_links(dist_dir))
    errors.extend(validate_manifest_assets(dist_dir))
    errors.extend(validate_source_notices(dist_dir))
    errors.extend(validate_equation_rendering(dist_dir))
    errors.extend(validate_no_local_path_leaks(dist_dir))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Quality gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
