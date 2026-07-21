#!/usr/bin/env python3
"""Import one explicitly registered PDF, TeX, or Markdown collection."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

UTC = timezone.utc  # noqa: UP017 - npm scripts may run on system Python 3.9.
SCRIPT_ID = "scripts/import_document_collection.py"
SCHEMA_VERSION = "website.document-collection-import.v1"
FORMATS = {"pdf", "tex", "markdown"}
CATEGORIES = {"anthology", "research", "governance"}
ROLES = {
    "authoritative_source",
    "registered_source",
    "readable_derivative",
    "governance_source",
    "operational_record",
    "explanatory_derivative",
    "provenance_record",
}
DOCUMENT_FIELDS = {
    "id",
    "slug",
    "title",
    "category",
    "summary",
    "status",
    "authority_scope",
    "reading_order",
    "tags",
    "related_routes",
    "manifestations",
}
ITEM_FIELDS = {
    "kind",
    "role",
    "source_id",
    "source_path",
    "site_path",
    "title",
    "approval_status",
    "source_authority_status",
    "reviewed_by",
    "license_or_usage_note",
    "notes",
}
GOVERNANCE_ALLOWLIST_FIELDS = {
    "source_path",
    "site_path",
    "reviewed_by",
    "current_state_reviewed",
}
GOVERNANCE_MARKDOWN_PREFIX = "/files/markdown/governance/"
GOVERNANCE_MARKDOWN_DENY_PATTERNS = (
    (
        "credential material",
        re.compile(
            r"(?i)\b(?:api[_ -]?key|access[_ -]?token|auth[_ -]?token|"
            r"client[_ -]?secret|password|secret)\b\s*(?:[:=]|\bis\b)\s*"
            r"[`\"']?[A-Za-z0-9_./+=-]{8,}"
        ),
    ),
    (
        "private key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "private email address",
        re.compile(
            r"(?i)\b[A-Z0-9._%+-]+@(?!(?:example\.com|example\.org|"
            r"example\.net)\b)[A-Z0-9.-]+\.[A-Z]{2,}\b"
        ),
    ),
    (
        "local or temporary filesystem path",
        re.compile(
            r"(?i)(?:/Users/|/Volumes/|/home/|/private/var/|/tmp/|"
            r"/var/tmp/|file://|[A-Z]:\\Users\\)"
        ),
    ),
    (
        "internal control record",
        re.compile(
            r"(?i)(?:implementation_control/|\.local/sys4ai/|"
            r"\.agents/control/|<codex_delegation\b|\b(?:handoff_token|"
            r"claim_token|codex_task_id)\b)"
        ),
    ),
    (
        "confidential or non-public marker",
        re.compile(
            r"(?i)\b(?:confidential|internal[- ]only|non[- ]public|"
            r"do not distribute)\b"
        ),
    ),
    (
        "raw upstream content URL",
        re.compile(r"(?i)https?://raw\.githubusercontent\.com/"),
    ),
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: must be a nonempty string")
    return value


def require_keys(
    value: object,
    required: set[str],
    allowed: set[str],
    label: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: must be an object")
    missing = sorted(required - value.keys())
    unknown = sorted(set(value) - allowed)
    if missing:
        raise ValueError(f"{label}: missing required fields: {', '.join(missing)}")
    if unknown:
        raise ValueError(f"{label}: unsupported fields: {', '.join(unknown)}")
    return value


def governance_markdown_allowlist(
    value: object,
) -> dict[tuple[str, str], dict[str, Any]]:
    """Validate the explicit human-reviewed governance Markdown allowlist."""

    if value is None:
        return {}
    if not isinstance(value, list):
        raise ValueError("governance_markdown_allowlist: must be a list")
    entries: dict[tuple[str, str], dict[str, Any]] = {}
    for index, raw_entry in enumerate(value):
        label = f"governance_markdown_allowlist[{index}]"
        entry = require_keys(
            raw_entry,
            GOVERNANCE_ALLOWLIST_FIELDS,
            GOVERNANCE_ALLOWLIST_FIELDS,
            label,
        )
        source_path = require_string(entry["source_path"], f"{label}.source_path")
        site_path = require_string(entry["site_path"], f"{label}.site_path")
        require_string(entry["reviewed_by"], f"{label}.reviewed_by")
        if entry["current_state_reviewed"] is not True:
            raise ValueError(f"{label}.current_state_reviewed: must be true")
        if (
            Path(source_path).is_absolute()
            or ".." in Path(source_path).parts
            or "\\" in source_path
            or source_path.startswith("~")
            or "://" in source_path
            or ":" in source_path.split("/", 1)[0]
            or not source_path.lower().endswith(".md")
        ):
            raise ValueError(f"{label}.source_path: must be safe repository-relative Markdown")
        if not (
            site_path.startswith(GOVERNANCE_MARKDOWN_PREFIX)
            and site_path.lower().endswith(".md")
            and ".." not in PurePosixPath(site_path).parts
        ):
            raise ValueError(
                f"{label}.site_path: must name one Markdown file under "
                f"{GOVERNANCE_MARKDOWN_PREFIX}"
            )
        key = (source_path, site_path)
        if key in entries:
            raise ValueError(f"{label}: duplicate governance Markdown allowlist entry")
        entries[key] = entry
    return entries


def validate_governance_markdown_source(
    *,
    document: dict[str, Any],
    item: dict[str, Any],
    source_file: Path,
    allowlist: dict[tuple[str, str], dict[str, Any]],
    label: str,
) -> tuple[str, str]:
    """Fail closed before one governance Markdown source can be staged."""

    if document.get("status") != "approved":
        raise ValueError(f"{label}: governance Markdown document must be approved")
    if item.get("role") != "governance_source":
        raise ValueError(f"{label}.role: governance Markdown must use governance_source")
    key = (str(item["source_path"]), str(item["site_path"]))
    entry = allowlist.get(key)
    if entry is None:
        raise ValueError(f"{label}: missing explicit governance Markdown allowlist entry")
    if entry["reviewed_by"] != item.get("reviewed_by"):
        raise ValueError(f"{label}.reviewed_by: differs from governance allowlist review")
    try:
        content = source_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{label}: governance Markdown must be valid UTF-8") from error
    for reason, pattern in GOVERNANCE_MARKDOWN_DENY_PATTERNS:
        if pattern.search(content):
            raise ValueError(f"{label}: governance Markdown contains denied {reason}")
    return key


def matches_prefix(site_path: object, prefixes: Iterable[str]) -> bool:
    return isinstance(site_path, str) and any(
        site_path.startswith(prefix) for prefix in prefixes
    )


def safe_source_file(source_root: Path, relative_path: str) -> Path:
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts or "\\" in relative_path:
        raise ValueError(f"{relative_path!r}: unsafe source_path")
    root = source_root.resolve(strict=True)
    candidate = root / relative
    if candidate.is_symlink() or not candidate.is_file():
        raise FileNotFoundError(f"missing registered source file: {candidate}")
    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ValueError(f"{relative_path!r}: source_path escapes source root") from error
    return resolved


def safe_public_file(public_dir: Path, site_path: str) -> Path:
    parts = PurePosixPath(site_path).parts
    if not site_path.startswith("/files/") or ".." in parts or site_path.endswith("/"):
        raise ValueError(f"{site_path!r}: unsafe public site_path")
    root = public_dir.resolve()
    candidate = root.joinpath(*parts[1:])
    try:
        candidate.parent.resolve().relative_to(root)
    except ValueError as error:
        raise ValueError(f"{site_path!r}: site_path escapes public root") from error
    if candidate.is_symlink():
        raise ValueError(f"{site_path!r}: destination cannot be a symlink")
    return candidate


def unique(records: Iterable[dict[str, Any]], field: str, label: str) -> None:
    seen: set[str] = set()
    for record in records:
        value = require_string(record.get(field), f"{label}.{field}")
        if value in seen:
            raise ValueError(f"{label}: duplicate {field} {value!r}")
        seen.add(value)


def partition_sources(
    records: object, source_prefix: str, path_prefixes: list[str]
) -> tuple[list[dict[str, Any]], set[str]]:
    if not isinstance(records, list):
        raise ValueError("source_manifest.items: must be a list")
    foreign: list[dict[str, Any]] = []
    owned_ids: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"source_manifest.items[{index}]: must be an object")
        signals = (
            isinstance(record.get("id"), str)
            and record["id"].startswith(source_prefix),
            matches_prefix(record.get("site_path"), path_prefixes),
            record.get("generated_by") == SCRIPT_ID,
        )
        if any(signals) and not all(signals):
            raise ValueError(
                f"source_manifest.items[{index}]: ambiguous collection ownership"
            )
        if all(signals):
            owned_ids.add(record["id"])
        else:
            foreign.append(record)
    return foreign, owned_ids


def partition_assets(
    records: object,
    source_prefix: str,
    path_prefixes: list[str],
    owned_source_ids: set[str],
) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError("asset_manifest.items: must be a list")
    foreign: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"asset_manifest.items[{index}]: must be an object")
        source_ref = record.get("source_ref")
        source_id = (
            source_ref.split(":", 1)[1]
            if isinstance(source_ref, str)
            and source_ref.startswith("source_manifest:")
            else None
        )
        signals = (
            matches_prefix(record.get("path"), path_prefixes),
            isinstance(source_id, str) and source_id.startswith(source_prefix),
            source_id in owned_source_ids,
        )
        if any(signals) and not all(signals):
            raise ValueError(
                f"asset_manifest.items[{index}]: ambiguous collection ownership"
            )
        if not all(signals):
            foreign.append(record)
    return foreign


def partition_documents(
    records: object,
    collection: str,
    document_prefix: str,
    path_prefixes: list[str],
) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError("document_catalog.documents: must be a list")
    foreign: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"document_catalog.documents[{index}]: must be an object")
        manifestations = record.get("manifestations")
        paths_owned = (
            isinstance(manifestations, list)
            and bool(manifestations)
            and all(
                isinstance(item, dict)
                and matches_prefix(item.get("site_path"), path_prefixes)
                for item in manifestations
            )
        )
        signals = (
            record.get("collection") == collection,
            isinstance(record.get("id"), str)
            and record["id"].startswith(document_prefix),
            paths_owned,
        )
        if any(signals) and not all(signals):
            raise ValueError(
                f"document_catalog.documents[{index}]: ambiguous collection ownership"
            )
        if not all(signals):
            foreign.append(record)
    return foreign


def build_import(
    *,
    config: dict[str, Any],
    repo_root: Path,
    source_root: Path,
    source_manifest: dict[str, Any],
    asset_manifest: dict[str, Any],
    document_catalog: dict[str, Any],
    generated_at: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[tuple], list[str]]:
    """Build and fully preflight an import without publishing anything."""

    require_keys(
        config,
        {"schema_version", "collection", "source_repository", "ownership", "documents"},
        {
            "schema_version",
            "collection",
            "source_repository",
            "source_commit",
            "ownership",
            "documents",
            "governance_markdown_allowlist",
        },
        "collection",
    )
    if config["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"collection.schema_version: expected {SCHEMA_VERSION!r}")
    collection = require_string(config["collection"], "collection.collection")
    source_repository = require_string(
        config["source_repository"], "collection.source_repository"
    )
    source_commit = config.get("source_commit")
    if source_commit is not None:
        source_commit = require_string(source_commit, "collection.source_commit")
    governance_allowlist = governance_markdown_allowlist(
        config.get("governance_markdown_allowlist")
    )
    used_governance_allowlist: set[tuple[str, str]] = set()
    ownership = require_keys(
        config["ownership"],
        {"document_id_prefix", "source_id_prefix", "site_path_prefixes"},
        {"document_id_prefix", "source_id_prefix", "site_path_prefixes"},
        "collection.ownership",
    )
    document_prefix = require_string(
        ownership["document_id_prefix"], "ownership.document_id_prefix"
    )
    source_prefix = require_string(
        ownership["source_id_prefix"], "ownership.source_id_prefix"
    )
    path_prefixes = ownership["site_path_prefixes"]
    if (
        not document_prefix.endswith(":")
        or not source_prefix.endswith("_")
        or not isinstance(path_prefixes, list)
        or not path_prefixes
        or len(path_prefixes) != len(set(path_prefixes))
    ):
        raise ValueError("collection.ownership: invalid or non-unique prefixes")
    for prefix in path_prefixes:
        if (
            not isinstance(prefix, str)
            or not prefix.startswith("/files/")
            or not prefix.endswith("/")
            or len(PurePosixPath(prefix).parts) < 4
        ):
            raise ValueError("site_path_prefixes must name collection-specific directories")
    if source_manifest.get("source_repository") != source_repository:
        raise ValueError("collection source_repository differs from source_manifest")
    if any(
        value.get("version") != 1
        for value in (source_manifest, asset_manifest, document_catalog)
    ):
        raise ValueError("source, asset, and document manifests must use version 1")

    foreign_sources, owned_source_ids = partition_sources(
        source_manifest.get("items"), source_prefix, path_prefixes
    )
    foreign_assets = partition_assets(
        asset_manifest.get("items"),
        source_prefix,
        path_prefixes,
        owned_source_ids,
    )
    foreign_documents = partition_documents(
        document_catalog.get("documents"),
        collection,
        document_prefix,
        path_prefixes,
    )
    raw_documents = config["documents"]
    if not isinstance(raw_documents, list) or not raw_documents:
        raise ValueError("collection.documents: must be a nonempty list")

    new_sources: list[dict[str, Any]] = []
    new_assets: list[dict[str, Any]] = []
    new_documents: list[dict[str, Any]] = []
    copies: list[tuple[Path, Path, str, int]] = []
    expected_paths: set[str] = set()
    seen_document_ids: set[str] = set()
    seen_slugs: set[str] = set()
    seen_source_ids: set[str] = set()
    seen_site_paths: set[str] = set()
    public_dir = repo_root / "public"
    for document_index, raw_document in enumerate(raw_documents):
        label = f"collection.documents[{document_index}]"
        document = require_keys(
            raw_document,
            {
                "id",
                "slug",
                "title",
                "category",
                "summary",
                "status",
                "authority_scope",
                "manifestations",
            },
            DOCUMENT_FIELDS,
            label,
        )
        document_id = require_string(document["id"], f"{label}.id")
        if not document_id.startswith(document_prefix):
            raise ValueError(f"{label}.id: outside declared ownership")
        slug = require_string(document["slug"], f"{label}.slug")
        if document_id in seen_document_ids:
            raise ValueError(f"document_catalog.documents: duplicate id {document_id!r}")
        if slug in seen_slugs:
            raise ValueError(f"document_catalog.documents: duplicate slug {slug!r}")
        seen_document_ids.add(document_id)
        seen_slugs.add(slug)
        for field in ("title", "summary", "status", "authority_scope"):
            require_string(document[field], f"{label}.{field}")
        if document["category"] not in CATEGORIES:
            raise ValueError(f"{label}.category: unsupported value")
        raw_items = document["manifestations"]
        if not isinstance(raw_items, list) or not raw_items:
            raise ValueError(f"{label}.manifestations: must be a nonempty list")
        catalog_items: list[dict[str, Any]] = []
        for item_index, raw_item in enumerate(raw_items):
            item_label = f"{label}.manifestations[{item_index}]"
            item = require_keys(
                raw_item,
                {
                    "kind",
                    "role",
                    "source_id",
                    "source_path",
                    "site_path",
                    "title",
                    "approval_status",
                    "source_authority_status",
                    "reviewed_by",
                    "license_or_usage_note",
                },
                ITEM_FIELDS,
                item_label,
            )
            kind = require_string(item["kind"], f"{item_label}.kind")
            role = require_string(item["role"], f"{item_label}.role")
            source_id = require_string(item["source_id"], f"{item_label}.source_id")
            source_path = require_string(
                item["source_path"], f"{item_label}.source_path"
            )
            site_path = require_string(item["site_path"], f"{item_label}.site_path")
            title = require_string(item["title"], f"{item_label}.title")
            authority_status = require_string(
                item["source_authority_status"],
                f"{item_label}.source_authority_status",
            )
            reviewed_by = require_string(item["reviewed_by"], f"{item_label}.reviewed_by")
            usage_note = require_string(
                item["license_or_usage_note"],
                f"{item_label}.license_or_usage_note",
            )
            if kind not in FORMATS or role not in ROLES:
                raise ValueError(f"{item_label}: unsupported kind or format role")
            if item["approval_status"] != "approved":
                raise ValueError(f"{item_label}.approval_status: must be 'approved'")
            if not source_id.startswith(source_prefix) or not matches_prefix(
                site_path, path_prefixes
            ):
                raise ValueError(f"{item_label}: outside declared ownership")
            if site_path in seen_site_paths:
                raise ValueError(f"source_manifest.items: duplicate site_path {site_path!r}")
            if source_id in seen_source_ids:
                raise ValueError(f"source_manifest.items: duplicate id {source_id!r}")
            seen_site_paths.add(site_path)
            seen_source_ids.add(source_id)
            source_file = safe_source_file(source_root, source_path)
            destination = safe_public_file(public_dir, site_path)
            if kind == "markdown":
                if document["category"] != "governance":
                    raise ValueError(
                        f"{item_label}: public Markdown requires governance category"
                    )
                used_governance_allowlist.add(
                    validate_governance_markdown_source(
                        document=document,
                        item=item,
                        source_file=source_file,
                        allowlist=governance_allowlist,
                        label=item_label,
                    )
                )
            elif site_path.startswith(GOVERNANCE_MARKDOWN_PREFIX):
                raise ValueError(
                    f"{item_label}: governance Markdown path requires governance category"
                )
            digest = sha256_file(source_file)
            size = source_file.stat().st_size
            expected_paths.add(site_path)
            copies.append((source_file, destination, digest, size))
            source_record = {
                "id": source_id,
                "site_path": site_path,
                "kind": kind,
                "title": title,
                "source_path": source_path,
                "approval_status": "approved",
                "sha256": digest,
                "generated_by": SCRIPT_ID,
                "generated_at": generated_at,
                "reviewed_by": reviewed_by,
                "license_or_usage_note": usage_note,
                "notes": item.get("notes", "Registered collection source."),
                "source_authority_status": authority_status,
            }
            if source_commit is not None:
                source_record["source_commit"] = source_commit
            new_sources.append(source_record)
            new_assets.append(
                {
                    "path": site_path,
                    "kind": kind,
                    "bytes": size,
                    "sha256": digest,
                    "title": title,
                    "source_ref": f"source_manifest:{source_id}",
                }
            )
            catalog_items.append(
                {"kind": kind, "site_path": site_path, "role": role, "title": title}
            )
        catalog_record = {
            key: document[key]
            for key in DOCUMENT_FIELDS - {"manifestations"}
            if key in document
        }
        catalog_record.update(
            {"collection": collection, "manifestations": catalog_items}
        )
        new_documents.append(catalog_record)

    unused_allowlist = sorted(set(governance_allowlist) - used_governance_allowlist)
    if unused_allowlist:
        source_path, site_path = unused_allowlist[0]
        raise ValueError(
            "governance_markdown_allowlist: unused entry for "
            f"{source_path!r} -> {site_path!r}"
        )

    merged_sources = foreign_sources + sorted(
        new_sources, key=lambda item: (item["site_path"], item["id"])
    )
    merged_assets = foreign_assets + sorted(new_assets, key=lambda item: item["path"])
    merged_documents = foreign_documents + new_documents
    unique(merged_sources, "id", "source_manifest.items")
    unique(merged_sources, "site_path", "source_manifest.items")
    unique(merged_assets, "path", "asset_manifest.items")
    unique(merged_documents, "id", "document_catalog.documents")
    unique(merged_documents, "slug", "document_catalog.documents")
    unique(
        [item for document in merged_documents for item in document["manifestations"]],
        "site_path",
        "document_catalog.manifestations",
    )
    messages = unexpected_files(public_dir, path_prefixes, expected_paths)
    return (
        {**source_manifest, "generated_at": generated_at, "items": merged_sources},
        {**asset_manifest, "generated_at": generated_at, "items": merged_assets},
        {**document_catalog, "generated_at": generated_at, "documents": merged_documents},
        copies,
        messages,
    )


def unexpected_files(
    public_dir: Path, prefixes: list[str], expected_paths: set[str]
) -> list[str]:
    messages: list[str] = []
    for prefix in prefixes:
        directory = public_dir.joinpath(*PurePosixPath(prefix).parts[1:])
        if directory.is_dir():
            for path in sorted(item for item in directory.rglob("*") if item.is_file()):
                site_path = "/" + path.relative_to(public_dir).as_posix()
                if site_path not in expected_paths:
                    messages.append(
                        f"DRIFT: unexpected collection asset retained: {site_path}"
                    )
    return messages


def stage_json(directory: Path, name: str, value: dict[str, Any]) -> Path:
    path = directory / name
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return path


def import_collection(
    *,
    config_path: Path,
    repo_root: Path,
    source_root: Path,
    source_manifest_path: Path,
    asset_manifest_path: Path,
    document_catalog_path: Path,
    generated_at: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    timestamp = generated_at or datetime.now(tz=UTC).isoformat()
    source_manifest, asset_manifest, catalog, copies, messages = build_import(
        config=load_json(config_path),
        repo_root=repo_root,
        source_root=source_root,
        source_manifest=load_json(source_manifest_path),
        asset_manifest=load_json(asset_manifest_path),
        document_catalog=load_json(document_catalog_path),
        generated_at=timestamp,
    )
    with tempfile.TemporaryDirectory(prefix="document-collection-") as temporary:
        staging = Path(temporary)
        staged_files: list[tuple[Path, Path]] = []
        for index, (source, destination, digest, size) in enumerate(copies):
            staged = staging / f"asset-{index}"
            shutil.copyfile(source, staged)
            if staged.stat().st_size != size or sha256_file(staged) != digest:
                raise RuntimeError(f"staged copy verification failed for {source}")
            staged_files.append((staged, destination))
        staged_manifests = (
            (stage_json(staging, "source.json", source_manifest), source_manifest_path),
            (stage_json(staging, "asset.json", asset_manifest), asset_manifest_path),
            (stage_json(staging, "catalog.json", catalog), document_catalog_path),
        )
        for staged, destination in staged_files + list(staged_manifests):
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged, destination)
    return source_manifest, asset_manifest, catalog, messages


def resolve(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else repo_root / path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=Path("public/files/manifests/source_manifest.json"),
    )
    parser.add_argument(
        "--asset-manifest",
        type=Path,
        default=Path("public/files/manifests/asset_manifest.json"),
    )
    parser.add_argument(
        "--document-catalog",
        type=Path,
        default=Path("public/files/manifests/document_catalog.json"),
    )
    parser.add_argument("--generated-at")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve(strict=True)
    try:
        _, _, _, messages = import_collection(
            config_path=resolve(repo_root, args.config),
            repo_root=repo_root,
            source_root=args.source_root.resolve(strict=True),
            source_manifest_path=resolve(repo_root, args.source_manifest),
            asset_manifest_path=resolve(repo_root, args.asset_manifest),
            document_catalog_path=resolve(repo_root, args.document_catalog),
            generated_at=args.generated_at,
        )
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for message in messages:
        print(message)
    print("Imported one registered document collection.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
