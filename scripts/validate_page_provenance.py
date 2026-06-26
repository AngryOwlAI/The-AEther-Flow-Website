#!/usr/bin/env python3
"""Validate page provenance, route coverage, and source/page hash integrity."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
HEX_COMMIT = re.compile(r"^[0-9a-f]{40}$")

REQUIRED_ROUTE_PATHS = {
    "/project/overview/",
    "/project/physics/",
    "/project/physics/ontology/",
    "/project/physics/exact-gr-benchmark/",
    "/project/physics/gr-derivation-roadmap/",
    "/project/physics/claim-gates/",
    "/project/ai-research-agent-system/",
    "/project/ai-research-agent-system/roles-and-skills/",
    "/project/ai-research-agent-system/memory-registries/",
    "/project/ai-research-agent-system/parent-child-synthesis/",
    "/project/operations/",
    "/project/operations/director-agentjob-lifecycle/",
    "/project/operations/role-routing/",
    "/project/operations/validator-operator-workflow/",
    "/project/operations/publication-process/",
    "/project/operations/project-system-improvement/",
    "/project/operations/technical-requirements/",
    "/project/source-authority/",
    "/resources/documents/",
    "/resources/",
}

ALLOWED_ADAPTATION_TYPES = {
    "one_to_one_adaptation",
    "curated_synthesis",
    "asset_index",
    "curated_index",
}
ALLOWED_UPSTREAM_AUTHORITY_STATUS = {
    "canonical",
    "generated_noncanonical",
    "draft_control_artifact",
    "archival_noncanonical",
}
ALLOWED_WEBSITE_PUBLICATION_STATUS = {
    "published",
    "approved_asset",
    "provenance_only",
    "planned",
    "excluded_first_release",
}
ALLOWED_BOUNDARY_TYPES = {
    "claim_boundary",
    "authority_boundary",
    "operational_boundary",
    "trust_boundary",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_safe_relative(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def iter_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, dict):
        for child in value.values():
            strings.extend(iter_strings(child))
    elif isinstance(value, list):
        for child in value:
            strings.extend(iter_strings(child))
    return strings


def validate_route_map(route_map: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if route_map.get("version") != 1:
        errors.append("page_route_map: version must be 1")
    if not isinstance(route_map.get("source_repository"), str):
        errors.append("page_route_map: source_repository is required")
    if not isinstance(route_map.get("github_base_url"), str):
        errors.append("page_route_map: github_base_url is required")
    routes = route_map.get("routes")
    if not isinstance(routes, list):
        return errors + ["page_route_map: routes must be a list"]

    seen: set[str] = set()
    for index, route in enumerate(routes):
        label = f"page_route_map.routes[{index}]"
        if not isinstance(route, dict):
            errors.append(f"{label}: route must be an object")
            continue
        route_path = route.get("route_path")
        local_page_source = route.get("local_page_source")
        source_paths = route.get("upstream_source_paths")
        if (
            not isinstance(route_path, str)
            or not route_path.startswith("/")
            or not route_path.endswith("/")
        ):
            errors.append(f"{label}: route_path must start and end with '/'")
        elif route_path in seen:
            errors.append(f"{label}: duplicate route_path {route_path!r}")
        else:
            seen.add(route_path)
        if not isinstance(local_page_source, str) or not is_safe_relative(local_page_source):
            errors.append(f"{label}: local_page_source must be a safe relative path")
        if not isinstance(source_paths, list) or not source_paths:
            errors.append(f"{label}: upstream_source_paths must be a nonempty list")
        elif not all(isinstance(path, str) and is_safe_relative(path) for path in source_paths):
            errors.append(f"{label}: upstream_source_paths must be safe relative paths")
        if route.get("adaptation_type") not in ALLOWED_ADAPTATION_TYPES:
            errors.append(f"{label}: unsupported adaptation_type {route.get('adaptation_type')!r}")
        if route.get("upstream_authority_status") not in ALLOWED_UPSTREAM_AUTHORITY_STATUS:
            errors.append(
                f"{label}: unsupported upstream_authority_status "
                f"{route.get('upstream_authority_status')!r}"
            )
        if route.get("website_publication_status") not in ALLOWED_WEBSITE_PUBLICATION_STATUS:
            errors.append(
                f"{label}: unsupported website_publication_status "
                f"{route.get('website_publication_status')!r}"
            )
        if route.get("boundary_type") not in ALLOWED_BOUNDARY_TYPES:
            errors.append(f"{label}: unsupported boundary_type {route.get('boundary_type')!r}")

    missing = sorted(REQUIRED_ROUTE_PATHS - seen)
    if missing:
        errors.append(f"page_route_map: missing required route(s): {', '.join(missing)}")
    return errors


def validate_public_strings(
    data: dict[str, Any],
    *,
    forbidden_substrings: list[str],
    label: str,
) -> list[str]:
    errors: list[str] = []
    for value in iter_strings(data):
        for forbidden in forbidden_substrings:
            if forbidden and forbidden in value:
                errors.append(f"{label}: public data leaks private path substring {forbidden!r}")
    return errors


def validate_page_provenance(
    provenance: dict[str, Any],
    route_map: dict[str, Any],
    *,
    repo_root: Path,
    source_root: Path,
) -> list[str]:
    errors: list[str] = []
    if provenance.get("version") != 1:
        errors.append("page_provenance: version must be 1")
    if not provenance.get("generated_at"):
        errors.append("page_provenance: generated_at is required")
    source_commit = provenance.get("source_commit")
    if source_commit is not None and (
        not isinstance(source_commit, str) or not HEX_COMMIT.match(source_commit)
    ):
        errors.append("page_provenance: source_commit must be a 40-character hex commit or null")

    pages = provenance.get("pages")
    if not isinstance(pages, list):
        return errors + ["page_provenance: pages must be a list"]

    route_map_entries = {
        route["route_path"]: route
        for route in route_map.get("routes", [])
        if isinstance(route, dict) and isinstance(route.get("route_path"), str)
    }
    seen: set[str] = set()
    for index, page in enumerate(pages):
        label = f"page_provenance.pages[{index}]"
        if not isinstance(page, dict):
            errors.append(f"{label}: page must be an object")
            continue
        route_path = page.get("route_path")
        local_page_source = page.get("local_page_source")
        local_page_sha256 = page.get("local_page_sha256")
        if not isinstance(route_path, str):
            errors.append(f"{label}: route_path is required")
            continue
        if route_path in seen:
            errors.append(f"{label}: duplicate route_path {route_path!r}")
        seen.add(route_path)
        route_entry = route_map_entries.get(route_path)
        if route_entry is None:
            errors.append(f"{label}: route is not present in page_route_map")
            continue
        if local_page_source != route_entry.get("local_page_source"):
            errors.append(f"{label}: local_page_source differs from page_route_map")
        if not isinstance(local_page_source, str) or not is_safe_relative(local_page_source):
            errors.append(f"{label}: local_page_source must be a safe relative path")
            continue
        page_file = repo_root / local_page_source
        if not page_file.is_file():
            errors.append(f"{label}: missing local page source {local_page_source}")
        elif not isinstance(local_page_sha256, str) or sha256_file(page_file) != local_page_sha256:
            errors.append(f"{label}: local page sha256 drift for {local_page_source}")
        if not isinstance(local_page_sha256, str) or not HEX_SHA256.match(local_page_sha256):
            errors.append(f"{label}: local_page_sha256 must be 64 hex characters")
        if page.get("adaptation_type") != route_entry.get("adaptation_type"):
            errors.append(f"{label}: adaptation_type differs from page_route_map")
        if page.get("upstream_authority_status") != route_entry.get("upstream_authority_status"):
            errors.append(f"{label}: upstream_authority_status differs from page_route_map")
        if page.get("website_publication_status") != route_entry.get("website_publication_status"):
            errors.append(f"{label}: website_publication_status differs from page_route_map")
        if page.get("boundary_type") != route_entry.get("boundary_type"):
            errors.append(f"{label}: boundary_type differs from page_route_map")

        upstream_sources = page.get("upstream_sources")
        if not isinstance(upstream_sources, list) or not upstream_sources:
            errors.append(f"{label}: upstream_sources must be a nonempty list")
            continue
        expected_sources = route_entry.get("upstream_source_paths")
        actual_sources = [
            source.get("path")
            for source in upstream_sources
            if isinstance(source, dict) and isinstance(source.get("path"), str)
        ]
        if actual_sources != expected_sources:
            errors.append(f"{label}: upstream source path order differs from page_route_map")
        for source_index, source in enumerate(upstream_sources):
            source_label = f"{label}.upstream_sources[{source_index}]"
            if not isinstance(source, dict):
                errors.append(f"{source_label}: source must be an object")
                continue
            source_path = source.get("path")
            if not isinstance(source_path, str) or not is_safe_relative(source_path):
                errors.append(f"{source_label}: path must be a safe relative path")
                continue
            source_file = source_root / source_path
            source_sha = source.get("sha256")
            if source_file.is_file():
                if not isinstance(source_sha, str) or sha256_file(source_file) != source_sha:
                    errors.append(f"{source_label}: upstream sha256 drift for {source_path}")
            elif source.get("omission_reason") is None:
                errors.append(f"{source_label}: missing omission_reason for unavailable source")

    missing = sorted(set(route_map_entries) - seen)
    extra = sorted(seen - set(route_map_entries))
    if missing:
        errors.append(f"page_provenance: missing route(s): {', '.join(missing)}")
    if extra:
        errors.append(f"page_provenance: extra route(s): {', '.join(extra)}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument(
        "--route-map",
        type=Path,
        default=Path("public/files/manifests/page_route_map.json"),
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=Path("public/files/manifests/page_provenance.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    route_map_path = (
        args.route_map if args.route_map.is_absolute() else repo_root / args.route_map
    )
    provenance_path = (
        args.provenance if args.provenance.is_absolute() else repo_root / args.provenance
    )
    route_map = load_json(route_map_path)
    provenance = load_json(provenance_path)
    forbidden_substrings = [str(repo_root), str(args.source_root)]
    errors = []
    errors.extend(validate_route_map(route_map))
    errors.extend(
        validate_public_strings(
            route_map,
            forbidden_substrings=forbidden_substrings,
            label="page_route_map",
        )
    )
    errors.extend(
        validate_public_strings(
            provenance,
            forbidden_substrings=forbidden_substrings,
            label="page_provenance",
        )
    )
    errors.extend(
        validate_page_provenance(
            provenance,
            route_map,
            repo_root=repo_root,
            source_root=args.source_root,
        )
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Page provenance validation passed for {len(provenance['pages'])} route(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
