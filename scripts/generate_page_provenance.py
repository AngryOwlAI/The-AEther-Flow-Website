#!/usr/bin/env python3
"""Generate page provenance from the checked-in route/source map."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
UTC = timezone.utc  # noqa: UP017 - npm scripts may run on system Python 3.9.


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_output(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return result.stdout.strip() or None


def git_blob_bytes(repo: Path, ref: str, source_path: str) -> bytes | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "show", f"{ref}:{source_path}"],
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return result.stdout


def public_github_url(base_url: str, ref: str, source_path: str) -> str:
    return f"{base_url.rstrip('/')}/blob/{ref}/{source_path}"


def validate_relative_path(value: str, label: str) -> None:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must be a repository-relative path: {value!r}")


def build_source_entries(
    source_paths: list[str],
    *,
    source_root: Path,
    github_base_url: str,
    source_commit: str | None,
) -> list[dict[str, str | None]]:
    entries: list[dict[str, str | None]] = []
    for source_path in source_paths:
        validate_relative_path(source_path, "upstream source path")
        source_file = source_root / source_path
        sha256: str | None = None
        omission_reason: str | None = None
        committed_blob = (
            git_blob_bytes(source_root, source_commit, source_path)
            if source_commit
            else None
        )
        if committed_blob is not None:
            sha256 = hashlib.sha256(committed_blob).hexdigest()
        elif source_file.is_file():
            sha256 = sha256_file(source_file)
        elif source_root.exists():
            omission_reason = "source_file_missing"
        else:
            omission_reason = "source_root_unavailable"

        pinned_url = (
            public_github_url(github_base_url, source_commit, source_path)
            if source_commit
            else None
        )
        entries.append(
            {
                "path": source_path,
                "sha256": sha256,
                "github_main_url": public_github_url(github_base_url, "main", source_path),
                "github_pinned_url": pinned_url,
                "omission_reason": omission_reason,
            }
        )
    return entries


def generate_provenance(
    *,
    repo_root: Path,
    source_root: Path,
    route_map_path: Path,
) -> dict[str, Any]:
    route_map = load_json(route_map_path)
    if route_map.get("version") != 1:
        raise ValueError("page route map version must be 1")

    source_repository = route_map.get("source_repository")
    github_base_url = route_map.get("github_base_url")
    adapted_at = route_map.get("adapted_at")
    routes = route_map.get("routes")
    if not isinstance(source_repository, str) or not source_repository:
        raise ValueError("page route map source_repository is required")
    if not isinstance(github_base_url, str) or not github_base_url:
        raise ValueError("page route map github_base_url is required")
    if not isinstance(adapted_at, str) or not adapted_at:
        raise ValueError("page route map adapted_at is required")
    if not isinstance(routes, list):
        raise ValueError("page route map routes must be a list")

    source_commit = git_output(source_root, "rev-parse", "HEAD") if source_root.exists() else None
    source_commit_date = (
        git_output(source_root, "show", "-s", "--format=%cI", "HEAD")
        if source_commit
        else None
    )

    pages: list[dict[str, Any]] = []
    for index, route in enumerate(routes):
        if not isinstance(route, dict):
            raise ValueError(f"routes[{index}] must be an object")
        route_path = route.get("route_path")
        local_page_source = route.get("local_page_source")
        source_paths = route.get("upstream_source_paths")
        if not isinstance(route_path, str) or not route_path.startswith("/"):
            raise ValueError(f"routes[{index}].route_path must start with '/'")
        if not isinstance(local_page_source, str):
            raise ValueError(f"routes[{index}].local_page_source is required")
        validate_relative_path(local_page_source, "local page source")
        if not isinstance(source_paths, list) or not all(
            isinstance(path, str) for path in source_paths
        ):
            raise ValueError(f"routes[{index}].upstream_source_paths must be a string list")

        page_file = repo_root / local_page_source
        if not page_file.is_file():
            raise FileNotFoundError(
                f"missing local page source for {route_path}: {local_page_source}"
            )

        upstream_sources = build_source_entries(
            source_paths,
            source_root=source_root,
            github_base_url=github_base_url,
            source_commit=source_commit,
        )
        pages.append(
            {
                "route_path": route_path,
                "local_page_source": local_page_source,
                "local_page_sha256": sha256_file(page_file),
                "title": route.get("title"),
                "adaptation_type": route.get("adaptation_type"),
                "upstream_source_repository": source_repository,
                "upstream_sources": upstream_sources,
                "upstream_source_commit": source_commit,
                "upstream_source_commit_date": source_commit_date,
                "adapted_from_source_date": adapted_at,
                "github_main_urls": [entry["github_main_url"] for entry in upstream_sources],
                "github_pinned_urls": [
                    entry["github_pinned_url"]
                    for entry in upstream_sources
                    if entry["github_pinned_url"]
                ],
                "upstream_authority_status": route.get("upstream_authority_status"),
                "website_publication_status": route.get("website_publication_status"),
                "boundary_type": route.get("boundary_type"),
            }
        )

    return {
        "version": 1,
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "source_repository": source_repository,
        "source_commit": source_commit,
        "source_commit_date": source_commit_date,
        "pages": pages,
    }


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
        "--out",
        type=Path,
        default=Path("public/files/manifests/page_provenance.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    route_map_path = args.route_map if args.route_map.is_absolute() else repo_root / args.route_map
    out_path = args.out if args.out.is_absolute() else repo_root / args.out
    data = generate_provenance(
        repo_root=repo_root,
        source_root=args.source_root,
        route_map_path=route_map_path,
    )
    write_json(out_path, data)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
