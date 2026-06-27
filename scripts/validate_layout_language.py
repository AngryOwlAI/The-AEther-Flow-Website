#!/usr/bin/env python3
"""Validate the command-interface layout migration contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_PRIMITIVE_FILES = {
    "src/components/CommandBand.astro",
    "src/components/EvidenceRail.astro",
    "src/components/StatusDossier.astro",
}

MIGRATED_SURFACES = {
    "src/pages/project/overview.astro": {
        "required": ("CommandBand", "EvidenceRail", "StatusDossier"),
        "forbidden": (
            'class="track-grid"',
            'class="link-grid"',
            'class="track-card"',
            'class="link-card"',
        ),
    },
    "src/components/InternalExplainerPage.astro": {
        "required": ("EvidenceRail", "StatusDossier"),
        "forbidden": (),
    },
    "src/components/ProjectRouteGrid.astro": {
        "required": ("EvidenceRail",),
        "forbidden": (),
    },
    "src/components/DocumentActions.astro": {
        "required": ("StatusDossier",),
        "forbidden": (),
    },
    "src/pages/project/physics/current-state/index.astro": {
        "required": ("EvidenceRail", "StatusDossier"),
        "forbidden": (),
    },
    "src/pages/resources/index.astro": {
        "required": ("EvidenceRail", "StatusDossier"),
        "forbidden": (),
    },
    "src/pages/resources/documents.astro": {
        "required": ("EvidenceRail",),
        "forbidden": (),
    },
}

EXPLICIT_EXCEPTIONS = {
    "src/pages/resources/diagrams.astro": "diagram inspection remains framed by design",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_layout_language(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for relative in sorted(REQUIRED_PRIMITIVE_FILES):
        if not (root / relative).is_file():
            errors.append(f"{relative}: missing required command-interface primitive")

    for relative, contract in MIGRATED_SURFACES.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"{relative}: missing migrated surface")
            continue

        text = read_text(path)
        for token in contract["required"]:
            if token not in text:
                errors.append(f"{relative}: expected primitive token {token!r}")
        for token in contract["forbidden"]:
            if token in text:
                errors.append(f"{relative}: forbidden overview anti-pattern token {token!r}")

    for relative in EXPLICIT_EXCEPTIONS:
        if not (root / relative).is_file():
            errors.append(f"{relative}: missing explicit layout exception surface")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_layout_language(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Layout-language validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
