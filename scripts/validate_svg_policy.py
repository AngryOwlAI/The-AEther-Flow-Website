#!/usr/bin/env python3
"""Validate project SVG artwork animation and text policy."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SVG_RE = re.compile(r"<svg\b[^>]*>.*?</svg>", re.IGNORECASE | re.DOTALL)
VISIBLE_TEXT_RE = re.compile(r"<text\b", re.IGNORECASE)
SVG_ANIMATION_ELEMENT_RE = re.compile(
    r"<(?:animate|animateMotion|animateTransform|set)\b",
    re.IGNORECASE,
)

ANIMATED_CLASS_HOOKS = {
    "agent-node-group",
    "agent-route",
    "charged-grain",
    "cosmic-dust",
    "detail-core",
    "detail-nodes",
    "field-ribbons",
    "flare-rays",
    "flare-system",
    "gold-field",
    "gold-filaments",
    "metric-grid",
    "plasma-filaments",
    "smoke-field",
    "smoke-filaments",
    "support-core",
    "support-dust",
    "support-flow-nodes",
    "support-flow-path",
    "support-line",
    "support-node-cores",
    "support-nodes",
    "support-rings",
    "track-figure-core",
    "track-figure-nodes",
    "track-figure-path",
}

SOURCE_SUFFIXES = {".astro", ".ts", ".tsx", ".js", ".jsx"}


def iter_svg_sources(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for base, suffixes in (
        (root / "src", SOURCE_SUFFIXES),
        (root / "public/assets", {".svg"}),
    ):
        if not base.exists():
            continue
        candidates.extend(
            path
            for path in base.rglob("*")
            if path.is_file() and path.suffix in suffixes
        )
    return sorted(candidates)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def has_animation_hook(svg_source: str) -> bool:
    if SVG_ANIMATION_ELEMENT_RE.search(svg_source):
        return True
    if "@keyframes" in svg_source and "animation:" in svg_source:
        return True
    return any(hook in svg_source for hook in ANIMATED_CLASS_HOOKS)


def validate_svg_policy(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    for path in iter_svg_sources(root):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)

        for match in VISIBLE_TEXT_RE.finditer(text):
            errors.append(
                f"{relative}:{line_number(text, match.start())}: "
                "visible SVG <text> is not allowed; use HTML copy, captions, "
                "ARIA labels, <title>, or <desc>"
            )

        for match in SVG_RE.finditer(text):
            svg_source = match.group(0)
            if not has_animation_hook(svg_source):
                errors.append(
                    f"{relative}:{line_number(text, match.start())}: "
                    "SVG must include an animation hook"
                )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_svg_policy(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("SVG policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
