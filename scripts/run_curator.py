#!/usr/bin/env python3
"""Generate and check internal curator reports for declared source drift."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/The-AEther-Flow")
SOURCE_ROOT_ENV_VAR = "AETHER_FLOW_SOURCE_ROOT"
SOURCE_COMMIT_ENV_VAR = "AETHER_FLOW_SOURCE_COMMIT"
DEFAULT_JSON_REPORT = Path("curator/reports/latest.json")
DEFAULT_MD_REPORT = Path("curator/reports/latest.md")
DEFAULT_ACKNOWLEDGEMENT_DIR = Path("curator/acknowledgements")
CURRENT_STATE_ROUTE = "/physics/claim-status/"
HEX_SHA256_LENGTH = 64
HEX_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
HEX_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REPORT_VERSION = 1
ALLOWED_SEVERITIES = {"critical", "review_required", "informational"}
ACK_REQUIRED_FIELDS = {
    "route_path",
    "source_path",
    "severity",
    "current_commit",
    "current_sha256",
    "acknowledged_by",
    "acknowledged_at",
    "reason",
    "expires_at",
}
UTC = timezone.utc  # noqa: UP017 - npm scripts may run on system Python 3.9.


def default_source_root() -> Path:
    return Path(os.environ.get(SOURCE_ROOT_ENV_VAR, DEFAULT_SOURCE_ROOT.as_posix()))


def default_source_commit() -> str | None:
    return os.environ.get(SOURCE_COMMIT_ENV_VAR)


class CuratorError(ValueError):
    """Raised when curator input files are malformed."""


@dataclass(frozen=True)
class Acknowledgement:
    route_path: str
    source_path: str
    severity: str
    current_commit: str
    current_sha256: str
    acknowledged_by: str
    acknowledged_at: str
    reason: str
    expires_at: str | None
    path: str


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


def resolve_source_commit(source_root: Path, requested_commit: str | None) -> str | None:
    if requested_commit is None:
        return git_output(source_root, "rev-parse", "HEAD") if source_root.exists() else None

    if re.fullmatch(r"[0-9A-Fa-f]{40}", requested_commit) is None:
        raise CuratorError("source commit pin must be a full 40-character hex commit")
    normalized_commit = requested_commit.lower()
    if not source_root.exists():
        raise CuratorError("source commit pin cannot be resolved because the source root is missing")

    object_type = git_output(source_root, "cat-file", "-t", normalized_commit)
    if object_type is None:
        raise CuratorError(f"source commit pin {normalized_commit} is missing")
    if object_type != "commit":
        raise CuratorError(
            f"source commit pin {normalized_commit} names a {object_type} object, not a commit"
        )
    resolved_commit = git_output(
        source_root,
        "rev-parse",
        "--verify",
        normalized_commit,
    )
    if resolved_commit != normalized_commit:
        raise CuratorError(f"source commit pin {normalized_commit} did not resolve exactly")
    return resolved_commit


def git_blob_bytes(repo: Path, ref: str, source_path: str) -> bytes | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "show", f"{ref}:{source_path}"],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout


def git_blob_text(repo: Path, ref: str, source_path: str) -> str | None:
    blob = git_blob_bytes(repo, ref, source_path)
    if blob is None:
        return None
    return blob.decode("utf-8")


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


def require_nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CuratorError(f"{label} must be a nonempty string")
    return value


def validate_source_path(source_path: object, label: str) -> str:
    if not isinstance(source_path, str) or not source_path or not is_safe_relative(source_path):
        raise CuratorError(f"{label}: source path must be a safe relative path")
    return source_path


def parse_ack_value(raw_value: str) -> str | None:
    value = raw_value.strip()
    if value == "null":
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_acknowledgement_file(path: Path, repo_root: Path) -> Acknowledgement:
    values: dict[str, str | None] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith((" ", "\t")) or ":" not in raw_line:
            raise CuratorError(
                f"{path}:{line_number}: acknowledgements support top-level scalars only"
            )
        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        if key not in ACK_REQUIRED_FIELDS:
            raise CuratorError(f"{path}:{line_number}: unsupported acknowledgement field {key!r}")
        values[key] = parse_ack_value(raw_value)

    missing = sorted(ACK_REQUIRED_FIELDS - values.keys())
    if missing:
        raise CuratorError(f"{path}: missing acknowledgement field(s): {', '.join(missing)}")

    route_path = values["route_path"]
    source_path = validate_source_path(values["source_path"], f"{path}: source_path")
    severity = values["severity"]
    current_commit = values["current_commit"]
    current_sha256 = values["current_sha256"]
    acknowledged_by = require_nonempty_string(
        values["acknowledged_by"],
        f"{path}: acknowledged_by",
    )
    acknowledged_at = require_nonempty_string(
        values["acknowledged_at"],
        f"{path}: acknowledged_at",
    )
    reason = require_nonempty_string(values["reason"], f"{path}: reason")
    expires_at = values["expires_at"]

    if (
        not isinstance(route_path, str)
        or not route_path.startswith("/")
        or not route_path.endswith("/")
    ):
        raise CuratorError(f"{path}: route_path must be a website route ending in '/'")
    if not isinstance(severity, str) or severity not in ALLOWED_SEVERITIES:
        raise CuratorError(f"{path}: unsupported severity {severity!r}")
    if severity == "critical":
        raise CuratorError(f"{path}: acknowledgements cannot target critical drift")
    if not isinstance(current_commit, str) or not HEX_COMMIT_RE.match(current_commit):
        raise CuratorError(f"{path}: current_commit must be a 40-character hex commit")
    if not isinstance(current_sha256, str) or not HEX_SHA256_RE.match(current_sha256):
        raise CuratorError(f"{path}: current_sha256 must be a 64-character hex sha256")
    if expires_at is not None:
        if not isinstance(expires_at, str) or not expires_at:
            raise CuratorError(f"{path}: expires_at must be null or a nonempty date string")
        try:
            expires_on = date.fromisoformat(expires_at[:10])
        except ValueError as exc:
            raise CuratorError(f"{path}: expires_at must start with YYYY-MM-DD") from exc
        if expires_on < datetime.now(tz=UTC).date():
            raise CuratorError(f"{path}: acknowledgement is expired")

    relative_path = path.resolve().relative_to(repo_root.resolve()).as_posix()
    return Acknowledgement(
        route_path=route_path,
        source_path=source_path,
        severity=severity,
        current_commit=current_commit,
        current_sha256=current_sha256,
        acknowledged_by=acknowledged_by,
        acknowledged_at=acknowledged_at,
        reason=reason,
        expires_at=expires_at,
        path=relative_path,
    )


def load_acknowledgements(repo_root: Path, acknowledgement_dir: Path) -> list[Acknowledgement]:
    path = (
        acknowledgement_dir
        if acknowledgement_dir.is_absolute()
        else repo_root / acknowledgement_dir
    )
    if not path.exists():
        return []
    acknowledgements = [
        parse_acknowledgement_file(candidate, repo_root)
        for candidate in sorted(path.glob("*.yaml"))
    ]
    seen: set[tuple[str, str, str, str, str]] = set()
    for acknowledgement in acknowledgements:
        key = acknowledgement_key(acknowledgement)
        if key in seen:
            raise CuratorError(f"{acknowledgement.path}: duplicate acknowledgement")
        seen.add(key)
    return acknowledgements


def acknowledgement_key(acknowledgement: Acknowledgement) -> tuple[str, str, str, str, str]:
    return (
        acknowledgement.route_path,
        acknowledgement.source_path,
        acknowledgement.severity,
        acknowledgement.current_commit,
        acknowledgement.current_sha256,
    )


def drift_ack_key(item: dict[str, Any]) -> tuple[str, str, str, str, str] | None:
    route_path = item.get("route_path")
    source_path = item.get("source_path")
    severity = item.get("severity")
    current_commit = item.get("current_commit")
    current_sha256 = item.get("new_sha256")
    if not isinstance(route_path, str):
        return None
    if not isinstance(source_path, str):
        return None
    if not isinstance(severity, str):
        return None
    if not isinstance(current_commit, str):
        return None
    if not isinstance(current_sha256, str):
        return None
    return (route_path, source_path, severity, current_commit, current_sha256)


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
            raise CuratorError(
                f"page_route_map.routes[{index}]: upstream_source_paths must be a list"
            )

        provenance_page = pages_by_route.get(route_path)
        provenance_sources = {
            source.get("path"): source
            for source in (provenance_page or {}).get("upstream_sources", [])
            if isinstance(source, dict) and isinstance(source.get("path"), str)
        }
        for source_path in source_paths:
            valid_source_path = validate_source_path(source_path, f"{route_path}")
            source = provenance_sources.get(valid_source_path, {})
            old_sha = source.get("sha256")
            if old_sha is not None and (
                not isinstance(old_sha, str) or len(old_sha) != HEX_SHA256_LENGTH
            ):
                raise CuratorError(
                    f"{route_path}: invalid recorded sha256 for {valid_source_path}"
                )
            merge_dependency(
                dependencies,
                Dependency(
                    source_path=valid_source_path,
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
        source_path = validate_source_path(
            item.get("source_path"),
            f"source_manifest.items[{index}]",
        )
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
        source_path = validate_source_path(
            item.get("path"),
            f"physics_current_state_snapshot.source_dependencies[{index}]",
        )
        old_sha = item.get("sha256")
        if old_sha is not None and (
            not isinstance(old_sha, str) or len(old_sha) != HEX_SHA256_LENGTH
        ):
            raise CuratorError(
                f"physics_current_state_snapshot.source_dependencies[{index}]: invalid sha256"
            )
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
    allow_worktree_fallback: bool = True,
) -> dict[str, Any]:
    source_file = source_root / dependency.source_path
    committed_blob = (
        git_blob_bytes(source_root, current_commit, dependency.source_path)
        if current_commit
        else None
    )
    source_missing = (
        not source_root.exists()
        or (
            committed_blob is None
            and (not allow_worktree_fallback or not source_file.is_file())
        )
    )
    new_sha: str | None
    if committed_blob is not None:
        new_sha = hashlib.sha256(committed_blob).hexdigest()
    else:
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


def build_diagnostics(
    source_root: Path,
    current_commit: str | None,
    *,
    allow_worktree_fallback: bool = True,
) -> list[dict[str, str | None]]:
    diagnostics: list[dict[str, str | None]] = []
    if not source_root.exists():
        return [
            {
                "diagnostic_type": "source_root_unavailable",
                "severity": "informational",
                "source_path": None,
                "message": (
                    "Upstream source root is unavailable; curator cannot compute "
                    "current hashes."
                ),
            }
        ]

    program_text = (
        git_blob_text(source_root, current_commit, "research_control/program_state.yaml")
        if current_commit
        else None
    )
    frontier_text = (
        git_blob_text(source_root, current_commit, "research_control/current_frontier.md")
        if current_commit
        else None
    )
    program_state = source_root / "research_control/program_state.yaml"
    current_frontier = source_root / "research_control/current_frontier.md"
    if allow_worktree_fallback:
        if program_text is None and program_state.is_file():
            program_text = program_state.read_text(encoding="utf-8")
        if frontier_text is None and current_frontier.is_file():
            frontier_text = current_frontier.read_text(encoding="utf-8")
    if program_text is not None and frontier_text is not None:
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


def validate_private_path_hygiene(
    data: dict[str, Any],
    *,
    repo_root: Path,
    source_root: Path,
) -> None:
    forbidden = [str(repo_root.resolve()), str(source_root.resolve())]
    for value in iter_strings(data):
        for snippet in forbidden:
            if snippet and snippet in value:
                raise CuratorError(f"curator report leaks private path {snippet!r}")


def build_report(
    *,
    repo_root: Path,
    source_root: Path,
    source_commit: str | None = None,
) -> dict[str, Any]:
    dependencies = collect_declared_dependencies(repo_root)
    current_commit = resolve_source_commit(source_root, source_commit)
    current_commit_date = (
        git_output(source_root, "show", "-s", "--format=%cI", current_commit)
        if current_commit
        else None
    )
    if source_commit is not None and current_commit_date is None:
        raise CuratorError(f"source commit pin {current_commit} has no readable commit date")
    allow_worktree_fallback = source_commit is None
    entries = [
        dependency_report_entry(
            dependency,
            source_root=source_root,
            current_commit=current_commit,
            allow_worktree_fallback=allow_worktree_fallback,
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
        "diagnostics": build_diagnostics(
            source_root,
            current_commit,
            allow_worktree_fallback=allow_worktree_fallback,
        ),
    }
    validate_private_path_hygiene(report, repo_root=repo_root, source_root=source_root)
    return report


def apply_acknowledgements(
    report: dict[str, Any],
    *,
    repo_root: Path,
    acknowledgement_dir: Path,
) -> None:
    acknowledgements = load_acknowledgements(repo_root, acknowledgement_dir)
    acknowledgement_index = {
        acknowledgement_key(acknowledgement): acknowledgement
        for acknowledgement in acknowledgements
    }
    matched_acknowledgements: set[tuple[str, str, str, str, str]] = set()

    for item in report["drift_items"]:
        severity = item["severity"]
        if severity == "critical":
            item["acknowledgement_state"] = "not_allowed"
            continue
        if severity == "informational":
            item["acknowledgement_state"] = "not_required"
            continue
        key = drift_ack_key(item)
        acknowledgement = acknowledgement_index.get(key) if key else None
        if acknowledgement is None:
            item["acknowledgement_state"] = "missing"
        else:
            item["acknowledgement_state"] = "acknowledged"
            item["acknowledgement_path"] = acknowledgement.path
            item["acknowledgement_reason"] = acknowledgement.reason
            matched_acknowledgements.add(acknowledgement_key(acknowledgement))

    for item in report["dependencies"]:
        if not item["drift_detected"]:
            item["acknowledgement_state"] = "not_required"

    unmatched = [
        acknowledgement
        for acknowledgement in acknowledgements
        if acknowledgement_key(acknowledgement) not in matched_acknowledgements
    ]
    if unmatched:
        names = ", ".join(acknowledgement.path for acknowledgement in unmatched)
        raise CuratorError(
            "stale acknowledgement(s) do not match current review-required drift: "
            f"{names}"
        )

    report["acknowledgement_summary"] = {
        "acknowledgement_count": len(acknowledgements),
        "matched_acknowledgement_count": len(matched_acknowledgements),
        "missing_review_required_count": sum(
            1
            for item in report["drift_items"]
            if item["severity"] == "review_required"
            and item["acknowledgement_state"] == "missing"
        ),
    }


def blocking_validation_errors(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for item in report["drift_items"]:
        route = item["route_path"] or item["source_manifest_id"] or "repo-internal dependency"
        source_path = item["source_path"]
        severity = item["severity"]
        acknowledgement_state = item["acknowledgement_state"]
        if severity == "critical":
            errors.append(
                f"{route}: critical source drift for {source_path}; {item['recommended_action']}"
            )
        elif severity == "review_required" and acknowledgement_state != "acknowledged":
            errors.append(
                f"{route}: review-required source drift for {source_path} "
                "lacks exact acknowledgement"
            )
    return errors


def markdown_report(report: dict[str, Any]) -> str:
    summary = report["dependency_summary"]
    acknowledgement_summary = report.get("acknowledgement_summary", {})
    matched_count = acknowledgement_summary.get("matched_acknowledgement_count", 0)
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
        f"- Matched acknowledgements: {matched_count}",
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
    parser.add_argument("--source-root", type=Path, default=default_source_root())
    parser.add_argument(
        "--source-commit",
        default=default_source_commit(),
        metavar="FULL_COMMIT_SHA",
        help=(
            f"Read the source repository at one exact commit "
            f"(default: ${SOURCE_COMMIT_ENV_VAR}, otherwise live HEAD)."
        ),
    )
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON_REPORT)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD_REPORT)
    parser.add_argument("--acknowledgement-dir", type=Path, default=DEFAULT_ACKNOWLEDGEMENT_DIR)
    parser.add_argument("--write", action="store_true", help="Write curator report files.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare fresh report to checked-in files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    json_report_path = (
        args.json_report
        if args.json_report.is_absolute()
        else repo_root / args.json_report
    )
    markdown_report_path = (
        args.markdown_report
        if args.markdown_report.is_absolute()
        else repo_root / args.markdown_report
    )
    try:
        report = build_report(
            repo_root=repo_root,
            source_root=args.source_root,
            source_commit=args.source_commit,
        )
        apply_acknowledgements(
            report,
            repo_root=repo_root,
            acknowledgement_dir=args.acknowledgement_dir,
        )
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
        errors.extend(blocking_validation_errors(report))
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
