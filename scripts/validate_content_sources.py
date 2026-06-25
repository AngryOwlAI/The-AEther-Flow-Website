#!/usr/bin/env python3
"""Validate website Markdown/MDX frontmatter claim-source discipline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ALLOWED_CLAIM_STATUSES = {
    "reviewed",
    "explanatory",
    "draft",
    "historical",
    "source-index-only",
}
SOURCE_REF_REQUIRED_STATUSES = {"reviewed", "draft", "historical", "source-index-only"}


def parse_frontmatter(path: Path) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing frontmatter block")

    end_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError("unterminated frontmatter block")

    metadata: dict[str, object] = {}
    current_key: str | None = None
    for raw_line in lines[1:end_index]:
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            value = line[4:].strip().strip('"')
            existing = metadata.setdefault(current_key, [])
            if isinstance(existing, list):
                existing.append(value)
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value:
            metadata[key] = value.strip('"')
        else:
            metadata[key] = []
    return metadata


def markdown_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for base in (root / "src/pages", root / "src/content"):
        if not base.exists():
            continue
        candidates.extend(path for path in base.rglob("*") if path.suffix in {".md", ".mdx"})
    return sorted(candidates)


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        frontmatter = parse_frontmatter(path)
    except ValueError as exc:
        return [f"{path}: {exc}"]

    claim_status = frontmatter.get("claim_status")
    if not isinstance(claim_status, str):
        errors.append(f"{path}: claim_status is required")
        return errors
    if claim_status not in ALLOWED_CLAIM_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_CLAIM_STATUSES))
        errors.append(f"{path}: unsupported claim_status {claim_status!r}; allowed: {allowed}")

    source_refs = frontmatter.get("source_refs")
    if claim_status in SOURCE_REF_REQUIRED_STATUSES:
        if not isinstance(source_refs, list) or not source_refs:
            errors.append(f"{path}: source_refs is required for claim_status {claim_status!r}")
    if isinstance(source_refs, list):
        for ref in source_refs:
            if not isinstance(ref, str) or not ref.startswith("source_manifest:"):
                errors.append(f"{path}: source_refs entries must use source_manifest:<id>")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Markdown and MDX claim-status frontmatter."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    files = markdown_files(root)
    for path in files:
        errors.extend(validate_file(path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Content source validation passed for {len(files)} Markdown/MDX file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
