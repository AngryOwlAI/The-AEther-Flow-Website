#!/usr/bin/env python3
"""Validate Cloudflare Pages static header and redirect files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

VALID_REDIRECT_CODES = {"200", "301", "302", "303", "307", "308"}


def meaningful_lines(path: Path) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        lines.append((number, line))
    return lines


def validate_headers(path: Path) -> list[str]:
    errors: list[str] = []
    current_rule: str | None = None
    for number, line in meaningful_lines(path):
        if line.startswith((" ", "\t")):
            if current_rule is None:
                errors.append(f"{path}:{number}: header appears before a path rule")
                continue
            stripped = line.strip()
            if ":" not in stripped:
                errors.append(f"{path}:{number}: header must use 'Name: value' syntax")
                continue
            name, value = stripped.split(":", 1)
            if not name.strip() or not value.strip():
                errors.append(f"{path}:{number}: header name and value are required")
            continue

        current_rule = line
        if not (current_rule.startswith("/") or current_rule.startswith("https://")):
            errors.append(f"{path}:{number}: header rule must start with '/' or 'https://'")

    if current_rule is None:
        errors.append(f"{path}: no header rules found")
    return errors


def validate_redirects(path: Path) -> list[str]:
    errors: list[str] = []
    for number, line in meaningful_lines(path):
        fields = line.split()
        if len(fields) not in {2, 3}:
            errors.append(f"{path}:{number}: redirect lines must have source destination [code]")
            continue
        source, destination = fields[0], fields[1]
        code = fields[2] if len(fields) == 3 else "302"
        if not source.startswith("/"):
            errors.append(f"{path}:{number}: redirect source must start with '/'")
        if not (destination.startswith("/") or destination.startswith("http://") or destination.startswith("https://")):
            errors.append(f"{path}:{number}: redirect destination must be a path or absolute URL")
        if code not in VALID_REDIRECT_CODES:
            errors.append(f"{path}:{number}: unsupported redirect status {code!r}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Cloudflare Pages config files.")
    parser.add_argument("--headers", type=Path, default=Path("public/_headers"))
    parser.add_argument("--redirects", type=Path, default=Path("public/_redirects"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    if not args.headers.is_file():
        errors.append(f"{args.headers}: missing _headers file")
    else:
        errors.extend(validate_headers(args.headers))
    if not args.redirects.is_file():
        errors.append(f"{args.redirects}: missing _redirects file")
    else:
        errors.extend(validate_redirects(args.redirects))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Cloudflare Pages config validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
