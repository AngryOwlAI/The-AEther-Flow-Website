#!/usr/bin/env python3
"""Smoke-test important routes on a running local preview server."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin


@dataclass(frozen=True)
class RouteCheck:
    path: str
    expected_status: int = 200


DEFAULT_ROUTES = [
    RouteCheck("/"),
    RouteCheck("/project/overview/"),
    RouteCheck("/project/ai-research-agent-system/workflow/"),
    RouteCheck("/project/source-authority/publication-and-provenance-system/"),
    RouteCheck("/resources/diagrams/"),
    RouteCheck("/resources/documents/"),
    RouteCheck("/robots.txt"),
]

SMOKE_TEST_USER_AGENT = "The-AEther-Flow-Website smoke-test/1.0"


def load_manifest_routes(root: Path) -> list[RouteCheck]:
    routes: list[RouteCheck] = []
    page_provenance_path = root / "public/files/manifests/page_provenance.json"
    asset_manifest_path = root / "public/files/manifests/asset_manifest.json"
    if page_provenance_path.is_file():
        with page_provenance_path.open("r", encoding="utf-8") as handle:
            page_provenance = json.load(handle)
        routes.extend(
            RouteCheck(page["route_path"])
            for page in page_provenance.get("pages", [])
            if isinstance(page, dict) and isinstance(page.get("route_path"), str)
        )
    if asset_manifest_path.is_file():
        with asset_manifest_path.open("r", encoding="utf-8") as handle:
            asset_manifest = json.load(handle)
        routes.extend(
            RouteCheck(asset["path"])
            for asset in asset_manifest.get("items", [])
            if isinstance(asset, dict) and isinstance(asset.get("path"), str)
        )
    return routes


def dedupe_routes(routes: list[RouteCheck]) -> list[RouteCheck]:
    seen: set[tuple[str, int]] = set()
    deduped: list[RouteCheck] = []
    for route in routes:
        key = (route.path, route.expected_status)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(route)
    return deduped


def check_route(base_url: str, route: RouteCheck, timeout: float) -> str | None:
    url = urljoin(base_url.rstrip("/") + "/", route.path.lstrip("/"))
    request = urllib.request.Request(
        url,
        headers={"User-Agent": SMOKE_TEST_USER_AGENT},
        method="HEAD",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        status = exc.code
    except urllib.error.URLError as exc:
        return f"{route.path}: request failed: {exc.reason}"

    if status != route.expected_status:
        return f"{route.path}: expected {route.expected_status}, got {status}"
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-test local static site routes.")
    parser.add_argument("--base-url", required=True, help="Base URL for local dev or preview.")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--timeout", type=float, default=5.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    routes = dedupe_routes(DEFAULT_ROUTES + load_manifest_routes(args.root.resolve()))
    errors = [
        error
        for route in routes
        if (error := check_route(args.base_url, route, args.timeout)) is not None
    ]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Smoke test passed for {len(routes)} route(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
