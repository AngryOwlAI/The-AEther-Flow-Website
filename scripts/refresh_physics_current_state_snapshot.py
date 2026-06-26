#!/usr/bin/env python3
"""Refresh the checked-in physics current-state snapshot from upstream sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
DEFAULT_OUT = Path("src/data/physics_current_state_snapshot.json")
SOURCE_REPOSITORY = "AngryOwlAI/The-AEther-Flow"
GITHUB_BASE_URL = "https://github.com/AngryOwlAI/The-AEther-Flow"
REQUIRED_PROGRAM_FIELDS = {
    "active_task_id",
    "latest_handoff_id",
    "current_status",
    "claim_boundary_summary",
    "next_recommended_action",
}
DERIVATION_BURDEN_FIELDS = {
    "burden_id",
    "milestone",
    "required_object",
    "current_status",
    "blocking_burden",
    "accept_criteria",
    "failure_or_freeze_criteria",
    "last_evidence_path",
    "updated_at",
    "notes",
}
DOWNSTREAM_BURDEN_IDS = {
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
    "gate_chair_status",
}
SCALAR_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")
UTC = timezone.utc  # noqa: UP017 - npm scripts may run on system Python 3.9.


class SnapshotError(ValueError):
    """Raised when upstream source state is missing or unsupported."""


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SnapshotError(f"required source file is missing: {path}") from exc


def parse_scalar_value(raw: str) -> str | bool | None:
    value = raw.strip()
    if not value:
        return None
    if value in {"true", "false"}:
        return value == "true"
    if value == "null":
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_top_level_scalars(path: Path) -> dict[str, str | bool | None]:
    scalars: dict[str, str | bool | None] = {}
    for line_number, raw_line in enumerate(load_text(path).splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith((" ", "\t")):
            continue
        match = SCALAR_RE.match(raw_line)
        if not match:
            raise SnapshotError(f"{path}:{line_number}: unsupported top-level YAML line")
        key, raw_value = match.groups()
        scalars[key] = parse_scalar_value(raw_value)
    return scalars


def required_string(scalars: dict[str, Any], key: str, *, path: Path) -> str:
    value = scalars.get(key)
    if not isinstance(value, str) or not value:
        raise SnapshotError(f"{path}: missing required scalar field {key!r}")
    return value


def parse_top_level_string_list(path: Path, key: str) -> list[str]:
    lines = load_text(path).splitlines()
    start: int | None = None
    for index, raw_line in enumerate(lines):
        if raw_line == f"{key}:":
            start = index + 1
            break
    if start is None:
        raise SnapshotError(f"{path}: missing required top-level list {key!r}")

    values: list[str] = []
    for line_number, raw_line in enumerate(lines[start:], start=start + 1):
        if raw_line and not raw_line.startswith((" ", "\t")):
            break
        if not raw_line.strip():
            continue
        stripped = raw_line.strip()
        if not stripped.startswith("- "):
            raise SnapshotError(f"{path}:{line_number}: unsupported list item for {key!r}")
        value = parse_scalar_value(stripped[2:])
        if not isinstance(value, str) or not value:
            raise SnapshotError(f"{path}:{line_number}: {key!r} entries must be strings")
        values.append(value)
    if not values:
        raise SnapshotError(f"{path}: {key!r} must not be empty")
    return values


def parse_nested_scalars(path: Path, parent_key: str) -> dict[str, str | bool | None]:
    lines = load_text(path).splitlines()
    start: int | None = None
    for index, raw_line in enumerate(lines):
        if raw_line == f"{parent_key}:":
            start = index + 1
            break
    if start is None:
        raise SnapshotError(f"{path}: missing required object {parent_key!r}")

    scalars: dict[str, str | bool | None] = {}
    for line_number, raw_line in enumerate(lines[start:], start=start + 1):
        if raw_line and not raw_line.startswith((" ", "\t")):
            break
        if not raw_line.strip() or raw_line.startswith("    "):
            continue
        if not raw_line.startswith("  "):
            raise SnapshotError(f"{path}:{line_number}: unsupported indentation")
        match = SCALAR_RE.match(raw_line.strip())
        if not match:
            raise SnapshotError(f"{path}:{line_number}: unsupported nested YAML line")
        key, raw_value = match.groups()
        scalars[key] = parse_scalar_value(raw_value)
    return scalars


def parse_program_state(source_root: Path) -> dict[str, str]:
    path = source_root / "research_control/program_state.yaml"
    scalars = parse_top_level_scalars(path)
    return {key: required_string(scalars, key, path=path) for key in REQUIRED_PROGRAM_FIELDS}


def parse_handoff(source_root: Path, handoff_id: str) -> dict[str, Any]:
    handoff_yaml = source_root / f"research_control/handoffs/{handoff_id}.yaml"
    handoff_md = source_root / f"research_control/handoffs/{handoff_id}.md"
    if not handoff_yaml.is_file():
        raise SnapshotError(f"latest handoff YAML is missing: {handoff_yaml}")
    if not handoff_md.is_file():
        raise SnapshotError(f"latest handoff Markdown is missing: {handoff_md}")

    scalars = parse_top_level_scalars(handoff_yaml)
    distance_to_gr = parse_nested_scalars(handoff_yaml, "distance_to_gr")
    blocked_claims = parse_top_level_string_list(handoff_yaml, "blocked_claims")
    return {
        "handoff_id": required_string(scalars, "handoff_id", path=handoff_yaml),
        "created_at": required_string(scalars, "created_at", path=handoff_yaml),
        "task_id": required_string(scalars, "task_id", path=handoff_yaml),
        "status": required_string(scalars, "status", path=handoff_yaml),
        "summary": required_string(scalars, "summary", path=handoff_yaml),
        "next_action": required_string(scalars, "next_action", path=handoff_yaml),
        "distance_to_gr": {
            "milestone": required_string(distance_to_gr, "milestone", path=handoff_yaml),
            "burden_id": required_string(distance_to_gr, "burden_id", path=handoff_yaml),
            "status": required_string(distance_to_gr, "status", path=handoff_yaml),
        },
        "blocked_claims": blocked_claims,
    }


def load_distance_to_gr(source_root: Path, active_burden_id: str) -> dict[str, Any]:
    path = source_root / "registries/DISTANCE_TO_GR_LEDGER.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = DERIVATION_BURDEN_FIELDS - set(reader.fieldnames or [])
        if missing:
            raise SnapshotError(f"{path}: missing required column(s): {', '.join(sorted(missing))}")
        rows = [
            {key: row.get(key, "") for key in sorted(DERIVATION_BURDEN_FIELDS)}
            for row in reader
        ]

    active_row = next((row for row in rows if row["burden_id"] == active_burden_id), None)
    if active_row is None:
        raise SnapshotError(f"{path}: active burden {active_burden_id!r} not found")
    downstream_rows = [row for row in rows if row["burden_id"] in DOWNSTREAM_BURDEN_IDS]
    return {
        "active_burden_id": active_burden_id,
        "active_row": active_row,
        "downstream_rows": downstream_rows,
    }


def git_output(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dependency_entry(
    source_root: Path,
    relative_path: str,
    source_commit: str | None,
) -> dict[str, Any]:
    if Path(relative_path).is_absolute() or ".." in Path(relative_path).parts:
        raise SnapshotError(f"dependency path must be source-root-relative: {relative_path!r}")
    source_file = source_root / relative_path
    if not source_file.is_file():
        raise SnapshotError(f"required dependency is missing: {relative_path}")
    return {
        "path": relative_path,
        "sha256": sha256_file(source_file),
        "github_main_url": f"{GITHUB_BASE_URL}/blob/main/{relative_path}",
        "github_pinned_url": (
            f"{GITHUB_BASE_URL}/blob/{source_commit}/{relative_path}" if source_commit else None
        ),
    }


def iter_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            strings.extend(iter_strings(item))
        return strings
    if isinstance(value, dict):
        strings = []
        for item in value.values():
            strings.extend(iter_strings(item))
        return strings
    return []


def validate_no_absolute_path_leak(data: dict[str, Any], source_root: Path) -> None:
    forbidden = str(source_root.resolve())
    for value in iter_strings(data):
        if forbidden in value:
            raise SnapshotError(f"snapshot data leaks absolute source root {forbidden!r}")


def build_snapshot(
    *,
    source_root: Path,
    source_commit: str | None = None,
    source_commit_date: str | None = None,
    source_refresh_date: str | None = None,
    website_publication_date: str | None = None,
    allow_dirty_source: bool = False,
) -> dict[str, Any]:
    source_root = source_root.resolve()
    dirty_status = git_output(source_root, "status", "--porcelain")
    if dirty_status and not allow_dirty_source:
        raise SnapshotError(
            "source repository has uncommitted changes; commit upstream source "
            "state or rerun with --allow-dirty-source"
        )
    program_state = parse_program_state(source_root)
    handoff = parse_handoff(source_root, program_state["latest_handoff_id"])
    if handoff["handoff_id"] != program_state["latest_handoff_id"]:
        raise SnapshotError("latest handoff id differs between program_state and handoff YAML")

    source_commit = source_commit or git_output(source_root, "rev-parse", "HEAD")
    source_commit_date = source_commit_date or (
        git_output(source_root, "show", "-s", "--format=%cI", "HEAD") if source_commit else None
    )
    today = datetime.now(tz=UTC).date().isoformat()
    dependency_paths = [
        "research_control/program_state.yaml",
        f"research_control/handoffs/{handoff['handoff_id']}.yaml",
        f"research_control/handoffs/{handoff['handoff_id']}.md",
        "registries/DISTANCE_TO_GR_LEDGER.csv",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv",
    ]
    dependencies = [
        dependency_entry(source_root, relative_path, source_commit)
        for relative_path in dependency_paths
    ]
    snapshot = {
        "version": 1,
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": source_commit,
        "source_commit_date": source_commit_date,
        "source_refresh_date": source_refresh_date or today,
        "website_publication_date": website_publication_date or today,
        "active_task_id": program_state["active_task_id"],
        "latest_handoff_id": program_state["latest_handoff_id"],
        "latest_handoff_created_at": handoff["created_at"],
        "current_status": program_state["current_status"],
        "claim_boundary_summary": program_state["claim_boundary_summary"],
        "derivation_burden": load_distance_to_gr(
            source_root,
            handoff["distance_to_gr"]["burden_id"],
        ),
        "blocked_claims": handoff["blocked_claims"],
        "next_recommended_action": program_state["next_recommended_action"],
        "latest_handoff_summary": handoff["summary"],
        "latest_handoff_next_action": handoff["next_action"],
        "source_dependencies": dependencies,
        "source_provenance_links": [
            {
                "label": entry["path"],
                "href": entry["github_pinned_url"] or entry["github_main_url"],
            }
            for entry in dependencies
        ],
    }
    validate_no_absolute_path_leak(snapshot, source_root)
    return snapshot


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--write", action="store_true", help="Write the snapshot file.")
    parser.add_argument("--source-commit")
    parser.add_argument("--source-commit-date")
    parser.add_argument("--source-refresh-date")
    parser.add_argument("--website-publication-date")
    parser.add_argument(
        "--allow-dirty-source",
        action="store_true",
        help="Allow refreshing from a dirty upstream working tree.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        snapshot = build_snapshot(
            source_root=args.source_root,
            source_commit=args.source_commit,
            source_commit_date=args.source_commit_date,
            source_refresh_date=args.source_refresh_date,
            website_publication_date=args.website_publication_date,
            allow_dirty_source=args.allow_dirty_source,
        )
    except SnapshotError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.write:
        write_json(args.out, snapshot)
        print(f"Wrote {args.out}")
    else:
        print(json.dumps(snapshot, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
