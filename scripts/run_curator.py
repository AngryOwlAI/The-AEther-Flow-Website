#!/usr/bin/env python3
"""Generate and check internal curator reports for declared source drift."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
DEFAULT_JSON_REPORT = Path("curator/reports/latest.json")
DEFAULT_MD_REPORT = Path("curator/reports/latest.md")
CURRENT_STATE_ROUTE = "/project/physics/current-state/"
HEX_SHA256_LENGTH = 64
REPORT_VERSION = 1


class CuratorError(ValueError):
    """Raised when curator input files are malformed."""


@dataclass
class Dependency:
    source_path: str
    route_path: str | None
    old_sha256: str | None
    old_commit: str | None
    dependency_type: str
    declared_in: set[str] = field(default_factory=set)
    title: str | None = None
    source_manifest_id: str | None = None
    approval_status: str | None = None


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise CuratorError(f"{path}: top-level JSON value must be an object")
    return data


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8")


def stable_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def is_safe_relative(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


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
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def dependency_key(dependency: Dependency) -> tuple[str, str | None]:
    return (dependency.source_path, dependency.route_path)


def merge_dependency(
    dependencies: dict[tuple[str, str | None], Dependency],
    candidate: Dependency,
) -> None:
    key = dependency_key(candidate)
    existing = dependencies.get(key)
    if existing is None:
        dependencies[key] = candidate
        return

    existing.declared_in.update(candidate.declared_in)
    if existing.old_sha256 is None and candidate.old_sha256 is not None:
        existing.old_sha256 = candidate.old_sha256
    if existing.old_commit is None and candidate.old_commit is not None:
        existing.old_commit = candidate.old_commit
    if existing.title is None:
        existing.title = candidate.title
    if existing.source_manifest_id is None:
        existing.source_manifest_id = candidate.source_manifest_id
    if existing.approval_status is None:
        existing.approval_status = candidate.approval_status


def validate_source_path(source_path: str, label: str) -> None:
    if not isinstance(source_path, str) or not source_path or not is_safe_relative(source_path):
        raise CuratorError(f"{label}: source path must be a safe relative path")


def collect_page_dependencies(
    route_map: dict[str, Any],
    provenance: dict[str, Any],
) -> dict[tuple[str, str | None], Dependency]:
    dependencies: dict[tuple[str, str | None], Dependency] = {}
    pages_by_route = {
        page.get("route_path"): page
        for page in provenance.get("pages", [])
        if isinstance(page, dict) and isinstance(page.get("route_path"), str)
    }

    for index, route in enumerate(route_map.get("routes", [])):
        if not isinstance(route, dict):
            raise CuratorError(f"page_route_map.routes[{index}]: route must be an object")
        route_path = route.get("route_path")
        source_paths = route.get("upstream_source_paths")
        if not isinstance(route_path, str) or not route_path.startswith("/"):
            raise CuratorError(f"page_route_map.routes[{index}]: invalid route_path")
        if not isinstance(source_paths, list):
            raise CuratorError(f"page_route_map.routes[{index}]: upstream_source_paths must be a list")

        provenance_page = pages_by_route.get(route_path)
        provenance_sources = {
            source.get("path"): source
            for source in (provenance_page or {}).get("upstream_sources", [])
            if isinstance(source, dict) and isinstance(source.get("path"), str)
        }
        for source_path in source_paths:
            validate_source_path(source_path, f"{route_path}")
            source = provenance_sources.get(source_path, {})
            old_sha = source.get("sha256")
            if old_sha is not None and (
                not isinstance(old_sha, str) or len(old_sha) != HEX_SHA256_LENGTH
            ):
                raise CuratorError(f"{route_path}: invalid recorded sha256 for {source_path}")
            merge_dependency(
                dependencies,
                Dependency(
                    source_path=source_path,
                    route_path=route_path,
                    old_sha256=old_sha,
                    old_commit=(
                        provenance_page.get("upstream_source_commit")
                        if isinstance(provenance_page, dict)
                        else None
                    ),
                    dependency_type="page_route_source",
                    declared_in={"page_route_map", "page_provenance"},
                    title=route.get("title") if isinstance(route.get("title"), str) else None,
                ),
            )
    return dependencies


def collect_source_manifest_dependencies(
    source_manifest: dict[str, Any],
) -> dict[tuple[str, str | None], Dependency]:
    dependencies: dict[tuple[str, str | None], Dependency] = {}
    for index, item in enumerate(source_manifest.get("items", [])):
        if not isinstance(item, dict):
            raise CuratorError(f"source_manifest.items[{index}]: item must be an object")
        approval_status = item.get("approval_status")
        source_commit = item.get("source_commit")
        if approval_status != "approved" or not isinstance(source_commit, str):
            continue
        source_path = item.get("source_path")
        validate_source_path(source_path, f"source_manifest.items[{index}]")
        old_sha = item.get("sha256")
        if old_sha is not None and (
            not isinstance(old_sha, str) or len(old_sha) != HEX_SHA256_LENGTH
        ):
            raise CuratorError(f"source_manifest.items[{index}]: invalid sha256")
        source_id = item.get("id")
        merge_dependency(
            dependencies,
            Dependency(
                source_path=source_path,
                route_path=None,
                old_sha256=old_sha,
                old_commit=source_commit,
                dependency_type="source_manifest_asset",
                declared_in={"source_manifest"},
                title=item.get("title") if isinstance(item.get("title"), str) else None,
                source_manifest_id=source_id if isinstance(source_id, str) else None,
                approval_status=approval_status,
            ),
        )
    return dependencies


def collect_snapshot_dependencies(
    snapshot: dict[str, Any],
) -> dict[tuple[str, str | None], Dependency]:
    dependencies: dict[tuple[str, str | None], Dependency] = {}
    source_commit = snapshot.get("source_commit")
    for index, item in enumerate(snapshot.get("source_dependencies", [])):
        if not isinstance(item, dict):
            raise CuratorError(f"physics_current_state_snapshot.source_dependencies[{index}]")
        source_path = item.get("path")
        validate_source_path(source_path, f"physics_current_state_snapshot.source_dependencies[{index}]")
        old_sha = item.get("sha256")
        if old_sha is not None and (
            not isinstance(old_sha, str) or len(old_sha) != HEX_SHA256_LENGTH
        ):
            raise CuratorError(f"physics_current_state_snapshot.source_dependencies[{index}]: invalid sha256")
        merge_dependency(
            dependencies,
            Dependency(
                source_path=source_path,
                route_path=CURRENT_STATE_ROUTE,
                old_sha256=old_sha,
                old_commit=source_commit if isinstance(source_commit, str) else None,
                dependency_type="current_state_snapshot_source",
                declared_in={"physics_current_state_snapshot"},
                title="Current Physics State",
            ),
        )
    return dependencies


def collect_declared_dependencies(repo_root: Path) -> list[Dependency]:
    route_map = load_json(repo_root / "public/files/manifests/page_route_map.json")
    provenance = load_json(repo_root / "public/files/manifests/page_provenance.json")
    source_manifest = load_json(repo_root / "public/files/manifests/source_manifest.json")
    snapshot = load_json(repo_root / "src/data/physics_current_state_snapshot.json")

    dependencies: dict[tuple[str, str | None], Dependency] = {}
    for collection in (
        collect_page_dependencies(route_map, provenance),
        collect_source_manifest_dependencies(source_manifest),
        collect_snapshot_dependencies(snapshot),
    ):
        for dependency in collection.values():
            merge_dependency(dependencies, dependency)

    return sorted(
        dependencies.values(),
        key=lambda dependency: (
            dependency.route_path or "",
            dependency.source_path,
            dependency.dependency_type,
        ),
    )


def classify_severity(dependency: Dependency, *, source_missing: bool) -> tuple[str, str, str]:
    if source_missing:
        return (
            "informational",
            "source_unavailable",
            "Verify source availability before reviewing website copy.",
        )
    if dependency.route_path == CURRENT_STATE_ROUTE:
        return (
            "critical",
            "current_state_source",
            "Refresh the current-state snapshot and review the public page boundary.",
        )
    if dependency.dependency_type == "source_manifest_asset":
        return (
            "critical",
            "approved_asset_source",
            "Re-import or review the approved published asset before release.",
        )
    return (
        "review_required",
        "mapped_route_source",
        "Review the affected internal page against its upstream source dependency.",
    )


def dependency_report_entry(
    dependency: Dependency,
    *,
    source_root: Path,
    current_commit: str | None,
) -> dict[str, Any]:
    source_file = source_root / dependency.source_path
    source_missing = not source_root.exists() or not source_file.is_file()
    new_sha = None if source_missing else sha256_file(source_file)
    drift_detected = dependency.old_sha256 != new_sha
    severity, impact_class, recommended_action = classify_severity(
        dependency,
        source_missing=source_missing,
    )
    status = "source_missing" if source_missing else "drift" if drift_detected else "in_sync"
    return {
        "acknowledgement_state": "not_evaluated",
        "approval_status": dependency.approval_status,
        "current_commit": current_commit,
        "declared_in": sorted(dependency.declared_in),
        "dependency_type": dependency.dependency_type,
        "drift_detected": drift_detected,
        "impact_class": impact_class,
        "old_commit": dependency.old_commit,
        "old_sha256": dependency.old_sha256,
        "new_sha256": new_sha,
        "recommended_action": recommended_action,
        "route_path": dependency.route_path,
        "severity": severity,
        "source_manifest_id": dependency.source_manifest_id,
        "source_path": dependency.source_path,
        "status": status,
        "title": dependency.title,
    }


def build_diagnostics(source_root: Path) -> list[dict[str, str | None]]:
    diagnostics: list[dict[str, str | None]] = []
    if not source_root.exists():
        return [
            {
                "diagnostic_type": "source_root_unavailable",
                "severity": "informational",
                "source_path": None,
                "message": "Upstream source root is unavailable; curator cannot compute current hashes.",
            }
        ]

    program_state = source_root / "research_control/program_state.yaml"
    current_frontier = source_root / "research_control/current_frontier.md"
    if program_state.is_file() and current_frontier.is_file():
        program_text = program_state.read_text(encoding="utf-8")
        frontier_text = current_frontier.read_text(encoding="utf-8")
        latest_handoff = None
        active_task = None
        for raw_line in program_text.splitlines():
            if raw_line.startswith("latest_handoff_id:"):
                latest_handoff = raw_line.split(":", 1)[1].strip().strip('"')
            if raw_line.startswith("active_task_id:"):
                active_task = raw_line.split(":", 1)[1].strip().strip('"')
        if latest_handoff and latest_handoff not in frontier_text:
            diagnostics.append(
                {
                    "diagnostic_type": "source_summary_lag",
                    "severity": "informational",
                    "source_path": "research_control/current_frontier.md",
                    "message": (
                        "current_frontier.md does not mention the latest "
                        f"program_state handoff {latest_handoff}."
                    ),
                }
            )
        if active_task and active_task not in frontier_text:
            diagnostics.append(
                {
                    "diagnostic_type": "source_summary_lag",
                    "severity": "informational",
                    "source_path": "research_control/current_frontier.md",
                    "message": (
                        "current_frontier.md does not mention the active "
                        f"program_state task {active_task}."
                    ),
                }
            )
    return diagnostics


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


def validate_private_path_hygiene(data: dict[str, Any], *, repo_root: Path, source_root: Path) -> None:
    forbidden = [str(repo_root.resolve()), str(source_root.resolve())]
    for value in iter_strings(data):
        for snippet in forbidden:
            if snippet and snippet in value:
                raise CuratorError(f"curator report leaks private path {snippet!r}")


def build_report(*, repo_root: Path, source_root: Path) -> dict[str, Any]:
    dependencies = collect_declared_dependencies(repo_root)
    current_commit = git_output(source_root, "rev-parse", "HEAD") if source_root.exists() else None
    current_commit_date = (
        git_output(source_root, "show", "-s", "--format=%cI", "HEAD")
        if current_commit
        else None
    )
    entries = [
        dependency_report_entry(
            dependency,
            source_root=source_root,
            current_commit=current_commit,
        )
        for dependency in dependencies
    ]
    drift_items = [entry for entry in entries if entry["drift_detected"]]
    report = {
        "version": REPORT_VERSION,
        "generated_at": current_commit_date,
        "source_repository": "AngryOwlAI/The-AEther-Flow",
        "current_commit": current_commit,
        "current_commit_date": current_commit_date,
        "dependency_summary": {
            "declared_dependency_count": len(entries),
            "drift_count": len(drift_items),
            "critical_count": sum(1 for item in drift_items if item["severity"] == "critical"),
            "review_required_count": sum(
                1 for item in drift_items if item["severity"] == "review_required"
            ),
            "informational_count": sum(
                1 for item in drift_items if item["severity"] == "informational"
            ),
        },
        "dependencies": entries,
        "drift_items": drift_items,
        "diagnostics": build_diagnostics(source_root),
    }
    validate_private_path_hygiene(report, repo_root=repo_root, source_root=source_root)
    return report


def markdown_report(report: dict[str, Any]) -> str:
    summary = report["dependency_summary"]
    lines = [
        "# Curator Drift Report",
        "",
        "This repo-internal report compares declared website source dependencies",
        "against the current upstream source repository. It is not a public page",
        "and does not rewrite website content.",
        "",
        "## Summary",
        "",
        f"- Source commit: `{report.get('current_commit') or 'unavailable'}`",
        f"- Source commit date: `{report.get('current_commit_date') or 'unavailable'}`",
        f"- Declared dependencies: {summary['declared_dependency_count']}",
        f"- Drift items: {summary['drift_count']}",
        f"- Critical drift: {summary['critical_count']}",
        f"- Review-required drift: {summary['review_required_count']}",
        f"- Informational drift: {summary['informational_count']}",
        "",
        "## Drift Items",
        "",
    ]
    if not report["drift_items"]:
        lines.append("No declared source dependency drift detected.")
    else:
        for item in report["drift_items"]:
            route = item["route_path"] or item["source_manifest_id"] or "repo-internal dependency"
            lines.extend(
                [
                    f"### {route}",
                    "",
                    f"- Source path: `{item['source_path']}`",
                    f"- Severity: `{item['severity']}`",
                    f"- Impact: `{item['impact_class']}`",
                    f"- Old hash: `{item['old_sha256'] or 'unavailable'}`",
                    f"- New hash: `{item['new_sha256'] or 'unavailable'}`",
                    f"- Recommended action: {item['recommended_action']}",
                    f"- Acknowledgement: `{item['acknowledgement_state']}`",
                    "",
                ]
            )

    lines.extend(["", "## Diagnostics", ""])
    if not report["diagnostics"]:
        lines.append("No diagnostics.")
    else:
        for diagnostic in report["diagnostics"]:
            source_path = diagnostic.get("source_path") or "not applicable"
            lines.append(
                f"- `{diagnostic['diagnostic_type']}` ({diagnostic['severity']}): "
                f"{diagnostic['message']} Source: `{source_path}`"
            )
    lines.append("")
    return "\n".join(lines)


def compare_report_file(path: Path, expected: str) -> list[str]:
    if not path.is_file():
        return [f"{path}: report file is missing"]
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        return [f"{path}: checked-in report is stale; run scripts/run_curator.py --write"]
    return []


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON_REPORT)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD_REPORT)
    parser.add_argument("--write", action="store_true", help="Write curator report files.")
    parser.add_argument("--check", action="store_true", help="Compare fresh report to checked-in files.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    json_report_path = args.json_report if args.json_report.is_absolute() else repo_root / args.json_report
    markdown_report_path = (
        args.markdown_report if args.markdown_report.is_absolute() else repo_root / args.markdown_report
    )
    try:
        report = build_report(repo_root=repo_root, source_root=args.source_root)
        json_text = stable_json(report)
        md_text = markdown_report(report)
    except CuratorError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.write:
        write_json(json_report_path, report)
        write_text(markdown_report_path, md_text)
        print(f"Wrote {json_report_path}")
        print(f"Wrote {markdown_report_path}")
        return 0

    if args.check:
        errors = []
        errors.extend(compare_report_file(json_report_path, json_text))
        errors.extend(compare_report_file(markdown_report_path, md_text))
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("Curator report validation passed.")
        return 0

    print(json_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
