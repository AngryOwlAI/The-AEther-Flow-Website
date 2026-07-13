#!/usr/bin/env python3
"""Report advisory warning patterns in technical prose.

This proxy check flags generic marketing patterns and unsupported-benefit
wording. It cannot prove source coverage, factual correctness, originality, or
human authorship.
"""

from __future__ import annotations

import argparse
import glob
import re
import sys
from dataclasses import dataclass
from pathlib import Path

WARNING_PATTERNS = [
    "seamless",
    "robust",
    "cutting-edge",
    "transformative",
    "revolutionary",
    "unlock",
    "empower",
    "leverage",
    "at scale",
    "game-changing",
    "next-generation",
    "holistic",
    "dynamic",
    "comprehensive solution",
    "streamline",
]

UNSUPPORTED_BENEFIT_PATTERNS = [
    r"\bimproves? efficiency\b",
    r"\bincreases? trust\b",
    r"\bensures? security\b",
    r"\bmaximi[sz]es? performance\b",
    r"\bdrives? innovation\b",
    r"\bdelivers? insights?\b",
    r"\bboosts? productivity\b",
    r"\bharness(?:es|ing)? (?:the )?(?:power|potential|capabilities)\b",
]


@dataclass(frozen=True)
class Hit:
    path: Path
    line_number: int
    pattern: str
    line: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Files or glob patterns to check.")
    parser.add_argument("--report", help="Optional Markdown report path.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 1 when repair-level warning hits are found.",
    )
    return parser.parse_args()


def expand_paths(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        if not matches:
            matches = [pattern]
        for match in matches:
            path = Path(match)
            if path.is_dir():
                continue
            normalized = path.resolve()
            if normalized not in seen:
                paths.append(path)
                seen.add(normalized)
    return paths


def warning_regexes() -> list[tuple[str, re.Pattern[str]]]:
    phrase_patterns = [
        (pattern, re.compile(rf"\b{re.escape(pattern)}\b", re.IGNORECASE))
        for pattern in WARNING_PATTERNS
    ]
    benefit_patterns = [
        (pattern, re.compile(pattern, re.IGNORECASE))
        for pattern in UNSUPPORTED_BENEFIT_PATTERNS
    ]
    return phrase_patterns + benefit_patterns


def check_file(path: Path) -> tuple[list[Hit], str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [], "not valid UTF-8 text"
    except OSError as exc:
        return [], str(exc)

    hits: list[Hit] = []
    regexes = warning_regexes()
    for line_number, line in enumerate(text.splitlines(), 1):
        for label, regex in regexes:
            if regex.search(line):
                hits.append(
                    Hit(
                        path=path,
                        line_number=line_number,
                        pattern=label,
                        line=line.strip(),
                    )
                )
    return hits, None


def render_report(paths: list[Path], hits: list[Hit], errors: dict[Path, str]) -> str:
    if errors or not paths:
        gate = "block"
    elif hits:
        gate = "repair"
    else:
        gate = "pass"

    lines = [
        "# Technical Writing Quality Gate Report",
        "",
        f"Gate: `{gate}`",
        "",
        "## Scope",
        "",
        f"- Files checked: {len(paths)}",
        f"- Warning hits: {len(hits)}",
        f"- Read errors: {len(errors)}",
        "",
        "## Interpretation",
        "",
        "Warning matches are advisory review signals. This report does not prove ",
        "factual correctness, source coverage, originality, or human authorship.",
        "",
    ]

    if hits:
        lines.extend(["## Warning Hits", ""])
        for hit in hits:
            lines.append(
                f"- `{hit.path}:{hit.line_number}` matched `{hit.pattern}`: {hit.line}"
            )
        lines.append("")

    if errors:
        lines.extend(["## Read Errors", ""])
        for path, message in errors.items():
            lines.append(f"- `{path}`: {message}")
        lines.append("")

    if not hits and not errors and paths:
        lines.extend(["## Result", "", "No configured warning patterns were found.", ""])

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    paths = expand_paths(args.paths)
    if not paths:
        print("error: no files matched", file=sys.stderr)
        print(render_report([], [], {}))
        return 2

    all_hits: list[Hit] = []
    errors: dict[Path, str] = {}
    for path in paths:
        hits, error = check_file(path)
        all_hits.extend(hits)
        if error:
            errors[path] = error

    report = render_report(paths, all_hits, errors)
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        print(f"Wrote report: {report_path}")
    else:
        print(report)

    if errors:
        return 2
    if all_hits and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
