#!/usr/bin/env python3
"""Reject mapped upstream explainer URLs in primary website page code."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAPPED_SOURCE_URL = re.compile(
    r"https://github\.com/AngryOwlAI/The-AEther-Flow/blob/main/github-facing/[^\"')\s]+"
)

ALLOWED_DIRECT_SOURCE_LINK_FILES = {
    Path("src/pages/project/source-authority/index.astro"),
}


def validate_internal_first_links(root: Path) -> list[str]:
    errors: list[str] = []
    candidates: list[Path] = []
    for base in (root / "src/pages", root / "src/lib", root / "src/components"):
        if not base.exists():
            continue
        candidates.extend(
            path
            for path in base.rglob("*")
            if path.suffix in {".astro", ".ts", ".tsx"}
        )
    for path in sorted(candidates):
        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        if relative in ALLOWED_DIRECT_SOURCE_LINK_FILES:
            continue
        for match in MAPPED_SOURCE_URL.finditer(text):
            line_number = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"{relative}:{line_number}: mapped GitHub explainer URL belongs in "
                "source provenance, not primary page journey data"
            )
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_internal_first_links(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Internal-first link validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
