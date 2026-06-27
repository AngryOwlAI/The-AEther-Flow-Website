#!/usr/bin/env python3
"""Apply the AEther Flow Mermaid style contract to diagram sources."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
DIAGRAM_ROOT = REPO_ROOT / "docs/content-dossiers"

THEME_FRONTMATTER = """---
config:
  theme: base
  themeVariables:
    darkMode: true
    background: "#000000"
    primaryColor: "#050403"
    primaryTextColor: "#fff8ef"
    primaryBorderColor: "#d6c3b4"
    lineColor: "#d6c3b4"
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "16px"
    clusterBkg: "#080401"
    clusterBorder: "#d6c3b4"
    edgeLabelBackground: "#000000"
---
"""

CLASS_DEFS = [
    "  classDef default fill:#050403,stroke:#d6c3b4,color:#fff8ef,stroke-width:1.5px;",
    "  classDef source fill:#0f364d,stroke:#48a0c0,color:#fff8ef,stroke-width:2px;",
    "  classDef control fill:#270b01,stroke:#f87800,color:#fff8ef,stroke-width:2px;",
    "  classDef bridge fill:#164964,stroke:#f4d6a1,color:#fff8ef,stroke-width:2px;",
    "  classDef decision fill:#702000,stroke:#f87800,color:#fff8ef,stroke-width:2.25px;",
    "  classDef target fill:#2d7ea0,stroke:#f4d6a1,color:#ffffff,stroke-width:2px;",
    "  classDef success fill:#164964,stroke:#48a0c0,color:#fff8ef,stroke-width:2px;",
    "  classDef risk fill:#702000,stroke:#f87800,color:#fff8ef,stroke-width:2px,stroke-dasharray: 5 5;",
    "  classDef boundary fill:#000000,stroke:#f87800,color:#fff8ef,stroke-width:3px,stroke-dasharray: 5 5;",
    "  classDef external fill:#080401,stroke:#f4d6a1,color:#fff8ef,stroke-width:2px;",
]
LINK_STYLE = "  linkStyle default stroke:#d6c3b4,stroke-width:2.25px;"

ALLOWED_CLASSES = {
    "default",
    "source",
    "control",
    "bridge",
    "decision",
    "target",
    "success",
    "risk",
    "boundary",
    "external",
}
LEGACY_CLASSES = {
    "source": "source",
    "control": "control",
    "boundary": "boundary",
}

GRAPH_RE = re.compile(r"^\s*(flowchart|graph)\s+(?:TB|TD|BT|LR|RL)\b")
CLASS_DEF_RE = re.compile(r"^\s*classDef\s+([A-Za-z0-9_-]+)\s+")
CLASS_ASSIGN_RE = re.compile(r"^\s*class\s+(.+?)\s+([A-Za-z0-9_-]+)\s*;\s*$")
LINK_STYLE_RE = re.compile(r"^\s*linkStyle\s+(.+?)\s+")
NODE_RE = re.compile(r"(?<![A-Za-z0-9_-])([A-Za-z][A-Za-z0-9_-]*)\s*(\[\[|\[|\{\{|\{|\(\(|\()")
LABEL_RE = re.compile(r'["\[]([^"\]]+)["\]]')


@dataclass(frozen=True)
class ParsedDiagram:
    body_lines: list[str]
    class_assignments: dict[str, str]


def diagram_paths() -> list[Path]:
    return sorted(DIAGRAM_ROOT.glob("**/diagrams/*.mmd"))


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[index + 1 :]).lstrip("\n")
    raise ValueError("frontmatter opens with --- but does not close")


def extract_label(line: str) -> str:
    match = LABEL_RE.search(line)
    return match.group(1) if match else ""


def iter_node_segments(line: str) -> list[tuple[str, str]]:
    matches = list(NODE_RE.finditer(line))
    segments: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(line)
        segments.append((match.group(1), line[match.start() : next_start]))
    return segments


def infer_class(node_id: str, label: str, *, shape_line: str) -> str:
    text = f"{node_id} {label}".lower()
    if "forbidden" in text or "not source authority" in text or "claim boundary" in text:
        return "boundary"
    if "boundary" in text or "no derivation" in text or "no role expansion" in text:
        return "boundary"
    if any(term in text for term in ["blocked", "blocker", "proof debt", "no-go", "negative"]):
        return "risk"
    if any(term in text for term in ["approved", "accepted", "complete", "pass", "success"]):
        return "success"
    if "{" in shape_line or any(term in text for term in ["gate", "review", "decision", "choose", "classify"]):
        return "decision"
    if any(term in text for term in ["bridge", "candidate", "adapt", "generated", "derivative"]):
        return "bridge"
    if any(term in text for term in ["goal", "output", "target", "reader-facing"]):
        return "target"
    if any(term in text for term in ["github", "external", "provenance link"]):
        return "external"
    if any(
        term in text
        for term in [
            "source",
            "manifest",
            "registry",
            "registries",
            "ontology",
            "tex",
            "mermaid",
            "memory",
            "receipt",
            "handoff",
        ]
    ):
        return "source"
    return "control"


def parse_diagram(text: str) -> ParsedDiagram:
    body = strip_frontmatter(text).rstrip()
    if "%%{init" in body:
        raise ValueError("deprecated Mermaid init directive is unsupported")

    body_lines: list[str] = []
    class_assignments: dict[str, str] = {}
    saw_graph = False

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            body_lines.append("")
            continue
        if GRAPH_RE.match(line):
            saw_graph = True
            body_lines.append(line)
            continue
        if stripped.startswith(("style ", "click ", "subgraph ")):
            raise ValueError(f"unsupported Mermaid syntax for conservative restyle: {stripped}")
        class_def_match = CLASS_DEF_RE.match(line)
        if class_def_match:
            class_name = class_def_match.group(1)
            if class_name not in ALLOWED_CLASSES and class_name not in LEGACY_CLASSES:
                raise ValueError(f"unsupported classDef {class_name!r}")
            continue
        class_match = CLASS_ASSIGN_RE.match(line)
        if class_match:
            node_ids = [node.strip() for node in class_match.group(1).split(",") if node.strip()]
            class_name = LEGACY_CLASSES.get(class_match.group(2), class_match.group(2))
            if class_name not in ALLOWED_CLASSES:
                raise ValueError(f"unsupported class assignment {class_name!r}")
            for node_id in node_ids:
                class_assignments[node_id] = class_name
            continue
        link_match = LINK_STYLE_RE.match(line)
        if link_match:
            if link_match.group(1).strip() != "default":
                raise ValueError("only linkStyle default is supported")
            continue
        body_lines.append(line)

    if not saw_graph:
        raise ValueError("missing supported flowchart or graph declaration")

    for line in body_lines:
        for node_id, segment in iter_node_segments(line):
            class_assignments.setdefault(
                node_id,
                infer_class(node_id, extract_label(segment), shape_line=segment),
            )

    return ParsedDiagram(body_lines=trim_blank_edges(body_lines), class_assignments=class_assignments)


def trim_blank_edges(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def class_lines(assignments: dict[str, str]) -> list[str]:
    grouped: dict[str, list[str]] = {}
    for node_id, class_name in sorted(assignments.items()):
        grouped.setdefault(class_name, []).append(node_id)
    return [f"  class {','.join(nodes)} {class_name};" for class_name, nodes in sorted(grouped.items())]


def format_diagram(text: str) -> str:
    parsed = parse_diagram(text)
    sections = [
        THEME_FRONTMATTER.rstrip(),
        "\n".join(parsed.body_lines).rstrip(),
        "\n".join(CLASS_DEFS),
        "\n".join(class_lines(parsed.class_assignments)),
        LINK_STYLE,
    ]
    return "\n\n".join(section for section in sections if section.strip()) + "\n"


def resolve_input_path(path_text: str) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def apply_file(path: Path, *, check: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = format_diagram(original)
    changed = updated != original
    if changed and not check:
        path.write_text(updated, encoding="utf-8")
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Mermaid .mmd files to update.")
    parser.add_argument(
        "--all-comprehension-diagrams",
        action="store_true",
        help="Update every docs/content-dossiers/**/diagrams/*.mmd file.",
    )
    parser.add_argument("--check", action="store_true", help="Report files that would change.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.all_comprehension_diagrams:
        paths = diagram_paths()
    else:
        paths = [resolve_input_path(path) for path in args.paths]

    if not paths:
        print("ERROR: provide paths or --all-comprehension-diagrams", file=sys.stderr)
        return 2

    failures: list[str] = []
    changed: list[Path] = []
    for path in paths:
        try:
            if apply_file(path, check=args.check):
                changed.append(path)
        except (OSError, ValueError) as exc:
            failures.append(f"{path}: {exc}")

    for path in changed:
        status = "would update" if args.check else "updated"
        print(f"{status}: {path.relative_to(REPO_ROOT)}")
    for failure in failures:
        print(f"ERROR: {failure}", file=sys.stderr)

    if failures:
        return 1
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
