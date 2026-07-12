#!/usr/bin/env python3
"""Refresh the checked-in claim-boundary explorer snapshot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
DEFAULT_OUT = Path("src/data/claim_boundary_snapshot.json")
SOURCE_REPOSITORY = "AngryOwlAI/The-AEther-Flow"
GITHUB_BASE_URL = "https://github.com/AngryOwlAI/The-AEther-Flow"
UTC = timezone.utc  # noqa: UP017 - npm scripts may run on system Python 3.9.

REGISTRY_FIELDS = [
    "claim_boundary_id",
    "scope",
    "applies_to_path",
    "allowed_claims",
    "forbidden_claims",
    "requires_gate_for",
    "authority_source_path",
    "status",
    "created_at",
    "updated_at",
    "notes",
]

PROGRAM_STATE_FIELDS = {
    "active_task_id",
    "latest_handoff_id",
    "current_status",
    "next_recommended_action",
}


class SnapshotError(ValueError):
    """Raised when source evidence cannot produce a safe public snapshot."""


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


def load_text(source_root: Path, relative_path: str) -> str:
    path = source_root / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SnapshotError(f"required source file is missing: {relative_path}") from exc


def dependency_entry(
    source_root: Path,
    relative_path: str,
    source_commit: str | None,
) -> dict[str, str | None]:
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts:
        raise SnapshotError(f"dependency path must be source-root-relative: {relative_path!r}")
    source_file = source_root / relative_path
    if not source_file.is_file():
        raise SnapshotError(f"required source file is missing: {relative_path}")
    return {
        "path": relative_path,
        "sha256": sha256_file(source_file),
        "github_main_url": f"{GITHUB_BASE_URL}/blob/main/{relative_path}",
        "github_pinned_url": (
            f"{GITHUB_BASE_URL}/blob/{source_commit}/{relative_path}"
            if source_commit
            else None
        ),
    }


def parse_program_state(source_root: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in load_text(source_root, "research_control/program_state.yaml").splitlines():
        if not raw_line or raw_line.startswith((" ", "\t", "#")) or ":" not in raw_line:
            continue
        key, raw_value = raw_line.split(":", 1)
        value = raw_value.strip().strip("\"'")
        if key in PROGRAM_STATE_FIELDS:
            values[key] = value
    missing = PROGRAM_STATE_FIELDS - values.keys()
    if missing:
        raise SnapshotError(
            "program_state.yaml missing required field(s): "
            + ", ".join(sorted(missing))
        )
    return values


def load_registry_rows(source_root: Path) -> list[dict[str, str]]:
    path = source_root / "registries/CLAIM_BOUNDARY_REGISTRY.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(REGISTRY_FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise SnapshotError(
                f"{path}: missing required column(s): {', '.join(sorted(missing))}"
            )
        return [
            {field: (row.get(field) or "").strip() for field in REGISTRY_FIELDS}
            for row in reader
        ]


def split_phrases(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def summarize_counter(counter: Counter[str], limit: int) -> list[dict[str, str | int]]:
    return [
        {"phrase": phrase, "count": count}
        for phrase, count in counter.most_common(limit)
    ]


def row_summary(row: dict[str, str]) -> dict[str, Any]:
    allowed_phrases = split_phrases(row["allowed_claims"])
    forbidden_phrases = split_phrases(row["forbidden_claims"])
    gate_phrases = split_phrases(row["requires_gate_for"])
    return {
        "claim_boundary_id": row["claim_boundary_id"],
        "scope": row["scope"],
        "applies_to_path": row["applies_to_path"],
        "authority_source_path": row["authority_source_path"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "notes": row["notes"],
        "allowed_summary": allowed_phrases[:3],
        "forbidden_summary": forbidden_phrases[:8],
        "requires_gate_summary": gate_phrases[:8],
        "allowed_claims": row["allowed_claims"],
        "forbidden_claims": row["forbidden_claims"],
        "requires_gate_for": row["requires_gate_for"],
    }


def path_prefix(relative_path: str) -> str:
    parts = Path(relative_path).parts
    if not parts:
        return "unspecified"
    if parts[0] == "research_control" and len(parts) > 1:
        return "/".join(parts[:2])
    return parts[0]


def applies_to_active_task(applies_to_path: str, active_task_id: str) -> bool:
    for candidate in applies_to_path.split(";"):
        normalized = candidate.strip().removesuffix("/**").rstrip("/")
        if normalized == active_task_id or normalized.endswith(f"/{active_task_id}"):
            return True
    return False


def build_language_examples(current_row: dict[str, str] | None) -> list[dict[str, str]]:
    if current_row is None:
        return []
    allowed = split_phrases(current_row["allowed_claims"])
    forbidden = split_phrases(current_row["forbidden_claims"])
    gate = split_phrases(current_row["requires_gate_for"])
    return [
        {
            "label": "Allowed explanation",
            "title": "Describe the bounded action",
            "body": (
                allowed[0]
                if allowed
                else "No allowed wording was available in the current row."
            ),
        },
        {
            "label": "Forbidden promotion",
            "title": "Do not strengthen it into adoption",
            "body": "; ".join(forbidden[:4])
            if forbidden
            else "No forbidden wording was available in the current row.",
        },
        {
            "label": "Gate required",
            "title": "Protected changes remain gated",
            "body": "; ".join(gate[:4])
            if gate
            else "No gate-required wording was available in the current row.",
        },
    ]


def validate_no_absolute_path_leak(data: dict[str, Any], source_root: Path) -> None:
    forbidden = str(source_root.resolve())

    def walk(value: Any) -> None:
        if isinstance(value, str) and forbidden in value:
            raise SnapshotError(f"snapshot data leaks absolute source root {forbidden!r}")
        if isinstance(value, dict):
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)


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
    source_commit = source_commit or git_output(source_root, "rev-parse", "HEAD")
    source_commit_date = source_commit_date or (
        git_output(source_root, "show", "-s", "--format=%cI", "HEAD")
        if source_commit
        else None
    )
    today = datetime.now(tz=UTC).date().isoformat()
    program_state = parse_program_state(source_root)
    rows = load_registry_rows(source_root)
    current_rows = [
        row
        for row in rows
        if applies_to_active_task(
            row["applies_to_path"],
            program_state["active_task_id"],
        )
    ]
    latest_rows = sorted(rows, key=lambda row: row["updated_at"], reverse=True)[:12]
    current_row = current_rows[0] if current_rows else (latest_rows[0] if latest_rows else None)

    forbidden_counter: Counter[str] = Counter()
    gate_counter: Counter[str] = Counter()
    scope_counter: Counter[str] = Counter()
    status_counter: Counter[str] = Counter()
    authority_prefix_counter: Counter[str] = Counter()
    for row in rows:
        scope_counter[row["scope"]] += 1
        status_counter[row["status"]] += 1
        authority_prefix_counter[path_prefix(row["authority_source_path"])] += 1
        forbidden_counter.update(split_phrases(row["forbidden_claims"]))
        gate_counter.update(split_phrases(row["requires_gate_for"]))

    dependency_paths = [
        "registries/CLAIM_BOUNDARY_REGISTRY.csv",
        "research_control/program_state.yaml",
        f"research_control/handoffs/{program_state['latest_handoff_id']}.yaml",
        f"research_control/handoffs/{program_state['latest_handoff_id']}.md",
        "research_control/README.md",
        "github-facing/source-authority-explainer.md",
        "github-facing/claim-gates-explainer.md",
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
        "current_status": program_state["current_status"],
        "next_recommended_action": program_state["next_recommended_action"],
        "row_count": len(rows),
        "scope_counts": dict(sorted(scope_counter.items())),
        "status_counts": dict(sorted(status_counter.items())),
        "authority_source_prefix_counts": dict(sorted(authority_prefix_counter.items())),
        "current_task_rows": [row_summary(row) for row in current_rows],
        "latest_rows": [row_summary(row) for row in latest_rows],
        "recurring_forbidden_claims": summarize_counter(forbidden_counter, 16),
        "recurring_gate_requirements": summarize_counter(gate_counter, 12),
        "language_examples": build_language_examples(current_row),
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
        help="Permit snapshot generation from an upstream worktree with uncommitted changes.",
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
        print(f"ERROR: {exc}", flush=True)
        return 1

    if args.write:
        write_json(args.out, snapshot)
        print(f"Wrote {args.out}")
    else:
        print(json.dumps(snapshot, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
