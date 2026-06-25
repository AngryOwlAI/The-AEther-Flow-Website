#!/usr/bin/env python3
"""Smoke-test important routes on a running local preview server."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import urljoin


@dataclass(frozen=True)
class RouteCheck:
    path: str
    expected_status: int = 200


DEFAULT_ROUTES = [
    RouteCheck("/"),
    RouteCheck("/project/overview/"),
    RouteCheck("/research/map/"),
    RouteCheck("/research/equations/"),
    RouteCheck("/resources/"),
    RouteCheck("/resources/documents/"),
    RouteCheck("/resources/diagrams/"),
    RouteCheck("/research/math-sample/"),
    RouteCheck("/files/pdf/aether-flow-sample.pdf"),
    RouteCheck("/files/tex/aether-flow-sample.tex"),
    RouteCheck("/assets/diagrams/publication-layer-map.svg"),
    RouteCheck("/robots.txt"),
]


def check_route(base_url: str, route: RouteCheck, timeout: float) -> str | None:
    url = urljoin(base_url.rstrip("/") + "/", route.path.lstrip("/"))
    request = urllib.request.Request(url, method="HEAD")
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
    parser.add_argument("--timeout", type=float, default=5.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = [
        error
        for route in DEFAULT_ROUTES
        if (error := check_route(args.base_url, route, args.timeout)) is not None
    ]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Smoke test passed for {len(DEFAULT_ROUTES)} route(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
