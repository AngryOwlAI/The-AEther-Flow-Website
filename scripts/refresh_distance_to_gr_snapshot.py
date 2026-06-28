#!/usr/bin/env python3
"""Refresh the checked-in Distance-to-GR dashboard snapshot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
DEFAULT_OUT = Path("src/data/distance_to_gr_snapshot.json")
SOURCE_REPOSITORY = "AngryOwlAI/The-AEther-Flow"
GITHUB_BASE_URL = "https://github.com/AngryOwlAI/The-AEther-Flow"
UTC = timezone.utc  # noqa: UP017 - npm scripts may run on system Python 3.9.

LEDGER_FIELDS = [
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
]

GROUPS = [
    {
        "id": "source_foundation",
        "title": "Source foundation",
        "description": "Ontology, source equivalence, retention, generation, localization, and response rows.",
        "burden_ids": [
            "source_ontology_primitives",
            "source_equivalence_eqsrc",
            "retain_h",
            "gen_h",
            "obsloc_lc",
            "resp_lc",
        ],
    },
    {
        "id": "metric_bridge",
        "title": "Metric and bridge rows",
        "description": "Source manifold and effective metric rows that remain narrower than downstream GR promotion.",
        "burden_ids": ["m_src", "g_eff"],
    },
    {
        "id": "downstream_gr",
        "title": "Downstream GR burdens",
        "description": "Matter coupling, Einstein equations, benchmark promotion, and protected Gate Chair status.",
        "burden_ids": [
            "matter_coupling",
            "einstein_equations",
            "benchmark_promotion",
            "gate_chair_status",
        ],
    },
    {
        "id": "negative_and_control",
        "title": "Negative and control rows",
        "description": "Finite robustness and frozen toy-model rows that guide routing without proving global failure.",
        "burden_ids": ["finite_variation_robustness", "finite_toy_metric_response"],
    },
]


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


def dependency_entry(source_root: Path, relative_path: str, source_commit: str | None) -> dict[str, str | None]:
    path = source_root / relative_path
    if not path.is_file():
        raise SnapshotError(f"required source file is missing: {path}")
    github_main_url = f"{GITHUB_BASE_URL}/blob/main/{relative_path}"
    github_pinned_url = (
        f"{GITHUB_BASE_URL}/blob/{source_commit}/{relative_path}" if source_commit else None
    )
    return {
        "path": relative_path,
        "sha256": sha256_file(path),
        "github_main_url": github_main_url,
        "github_pinned_url": github_pinned_url,
    }


def load_text(source_root: Path, relative_path: str) -> str:
    path = source_root / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SnapshotError(f"required source file is missing: {path}") from exc


def parse_program_state(source_root: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in load_text(source_root, "research_control/program_state.yaml").splitlines():
        if not raw_line or raw_line.startswith((" ", "\t", "#")) or ":" not in raw_line:
            continue
        key, raw_value = raw_line.split(":", 1)
        value = raw_value.strip().strip("\"'")
        if key in {"active_task_id", "latest_handoff_id", "current_status", "next_recommended_action"}:
            values[key] = value
    missing = {"active_task_id", "latest_handoff_id", "current_status", "next_recommended_action"} - values.keys()
    if missing:
        raise SnapshotError(f"program_state.yaml missing required field(s): {', '.join(sorted(missing))}")
    return values


def load_ledger_rows(source_root: Path) -> list[dict[str, str]]:
    path = source_root / "registries/DISTANCE_TO_GR_LEDGER.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(LEDGER_FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise SnapshotError(f"{path}: missing required column(s): {', '.join(sorted(missing))}")
        return [{field: (row.get(field) or "").strip() for field in LEDGER_FIELDS} for row in reader]


def group_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    row_by_id = {row["burden_id"]: row for row in rows}
    groups: list[dict[str, Any]] = []
    seen: set[str] = set()
    for group in GROUPS:
        group_rows = [row_by_id[burden_id] for burden_id in group["burden_ids"] if burden_id in row_by_id]
        seen.update(row["burden_id"] for row in group_rows)
        groups.append({**group, "rows": group_rows})
    uncategorized = [row for row in rows if row["burden_id"] not in seen]
    if uncategorized:
        groups.append(
            {
                "id": "uncategorized",
                "title": "Uncategorized ledger rows",
                "description": "Rows present in the ledger but not yet assigned to a dashboard group.",
                "burden_ids": [row["burden_id"] for row in uncategorized],
                "rows": uncategorized,
            }
        )
    return groups


def validate_no_absolute_path_leak(data: dict[str, Any], source_root: Path) -> None:
    forbidden = str(source_root.resolve())

    def walk(value: Any) -> None:
        if isinstance(value, str) and forbidden in value:
            raise SnapshotError(f"snapshot data leaks absolute source root {forbidden!r}")
        if isinstance(value, dict):
            for child in value.values():
                walk(child)
        if isinstance(value, list):
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
        git_output(source_root, "show", "-s", "--format=%cI", "HEAD") if source_commit else None
    )
    today = datetime.now(tz=UTC).date().isoformat()
    program_state = parse_program_state(source_root)
    rows = load_ledger_rows(source_root)
    dependency_paths = [
        "registries/DISTANCE_TO_GR_LEDGER.csv",
        "research_control/design/gr_derivation_burden_map.md",
        "research_control/design/mathematical_decisiveness_completion_contract.md",
        "research_control/design/obstruction_and_freeze_control.md",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv",
        "research_control/program_state.yaml",
        f"research_control/handoffs/{program_state['latest_handoff_id']}.yaml",
        f"research_control/handoffs/{program_state['latest_handoff_id']}.md",
    ]
    dependencies = [
        dependency_entry(source_root, relative_path, source_commit)
        for relative_path in dependency_paths
    ]
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["current_status"]] = status_counts.get(row["current_status"], 0) + 1
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
        "status_counts": status_counts,
        "groups": group_rows(rows),
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
