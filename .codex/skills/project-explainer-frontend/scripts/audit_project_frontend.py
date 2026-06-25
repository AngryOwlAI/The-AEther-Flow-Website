#!/usr/bin/env python3
"""Audit AEther Flow explainer frontend output for common claim and UI risks."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path

HTML_EXTENSIONS = {".html", ".htm"}
CSS_EXTENSIONS = {".css", ".scss"}
FRONTEND_EXTENSIONS = {
    ".astro",
    ".css",
    ".htm",
    ".html",
    ".js",
    ".jsx",
    ".mdx",
    ".scss",
    ".ts",
    ".tsx",
}
EXCLUDE_DIRS = {
    ".astro",
    ".git",
    ".venv",
    "__pycache__",
    "coverage",
    "node_modules",
    "scratch",
}

LOCAL_PATH_SNIPPETS = {
    "/Volumes/P-SSD/AngryOwl/The-AEther-Flow",
    "/Users/alex.omegapy",
}
PLACEHOLDER_PATTERNS = {
    "coming soon",
    "lorem ipsum",
    "placeholder",
    "sample text",
    "todo:",
    "your project here",
}
RISKY_CLAIMS = {
    "fully automated research validation",
    "guaranteed derivation",
    "live simulation",
    "production-ready scientific proof",
    "proves general relativity",
    "runs the project",
    "validated proof",
}
CSS_VAR_RE = re.compile(r"--(?P<name>[a-zA-Z0-9_-]+)\s*:\s*(?P<value>#[0-9a-fA-F]{6})")


@dataclass(frozen=True)
class AuditIssue:
    severity: str
    path: str
    message: str
    evidence: str = ""


@dataclass(frozen=True)
class AuditReport:
    site: str
    files_checked: int
    html_files: int
    css_files: int
    issues: list[AuditIssue]
    passed: bool


class LinkAndImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.img_tags: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() == "img":
            self.img_tags.append(attr_map)
        if tag.lower() == "a":
            self.links.append(attr_map)


def should_skip(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in EXCLUDE_DIRS for part in relative.parts)


def iter_frontend_files(site: Path) -> Iterable[Path]:
    root = site if site.is_dir() else site.parent
    if site.is_file():
        if site.suffix.lower() in FRONTEND_EXTENSIONS:
            yield site
        return
    for path in sorted(site.rglob("*")):
        if path.is_file() and not should_skip(path, root):
            if path.suffix.lower() in FRONTEND_EXTENSIONS:
                yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def snippet(text: str, term: str, window: int = 90) -> str:
    index = text.lower().find(term.lower())
    if index < 0:
        return ""
    start = max(0, index - window)
    end = min(len(text), index + len(term) + window)
    return re.sub(r"\s+", " ", text[start:end]).strip()


def srgb_to_linear(channel: int) -> float:
    value = channel / 255
    if value <= 0.03928:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    clean = value.strip().lstrip("#")
    return tuple(int(clean[index : index + 2], 16) for index in (0, 2, 4))


def luminance(value: str) -> float:
    red, green, blue = (srgb_to_linear(channel) for channel in hex_to_rgb(value))
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: str, background: str) -> float:
    first = luminance(foreground)
    second = luminance(background)
    lighter = max(first, second)
    darker = min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def audit_claims(path: Path, root: Path, text: str) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    lower = text.lower()
    rpath = rel(path, root)
    for pattern in sorted(PLACEHOLDER_PATTERNS):
        if pattern in lower:
            issues.append(
                AuditIssue(
                    "warning",
                    rpath,
                    f"Placeholder-like text found: {pattern!r}.",
                    snippet(text, pattern),
                )
            )
    for pattern in sorted(RISKY_CLAIMS):
        if pattern in lower:
            issues.append(
                AuditIssue(
                    "error",
                    rpath,
                    f"Potentially unsupported runtime or scientific claim: {pattern!r}.",
                    snippet(text, pattern),
                )
            )
    for pattern in sorted(LOCAL_PATH_SNIPPETS):
        if pattern in text:
            issues.append(
                AuditIssue(
                    "error",
                    rpath,
                    f"Rendered local path leak: {pattern!r}.",
                    snippet(text, pattern),
                )
            )
    if "the aether flow" in lower and "source authority" not in lower:
        issues.append(
            AuditIssue(
                "warning",
                rpath,
                "AEther Flow page lacks visible source authority language.",
            )
        )
    return issues


def audit_html(path: Path, root: Path, text: str) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    lower = text.lower()
    rpath = rel(path, root)
    if "<main" not in lower:
        issues.append(AuditIssue("error", rpath, "No <main> landmark found."))
    h1_count = len(re.findall(r"<h1\b", lower))
    if h1_count == 0:
        issues.append(AuditIssue("error", rpath, "No <h1> found."))
    if h1_count > 1:
        issues.append(AuditIssue("warning", rpath, "More than one <h1> found."))
    if "name=\"viewport\"" not in lower and "name='viewport'" not in lower:
        issues.append(AuditIssue("error", rpath, "Missing viewport meta tag."))

    parser = LinkAndImageParser()
    parser.feed(text)
    for attrs in parser.img_tags:
        if "alt" not in attrs:
            issues.append(AuditIssue("error", rpath, "Image tag missing alt attribute."))
    for attrs in parser.links:
        href = attrs.get("href", "")
        if href in {"", "#", "javascript:void(0)"}:
            issues.append(AuditIssue("warning", rpath, "Anchor has placeholder href.", href))
        if attrs.get("target") == "_blank" and "noopener" not in attrs.get("rel", ""):
            issues.append(AuditIssue("warning", rpath, "target=_blank link lacks noopener."))
    return issues


def audit_css(path: Path, root: Path, text: str) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    lower = text.lower()
    rpath = rel(path, root)
    if ":focus-visible" not in lower and ":focus" not in lower:
        issues.append(AuditIssue("warning", rpath, "No visible focus style found."))
    uses_motion = re.search(r"animation\s*:|transition\s*:", lower)
    if uses_motion and "prefers-reduced-motion" not in lower:
        issues.append(AuditIssue("warning", rpath, "Motion lacks reduced-motion handling."))

    variables = {match.group("name"): match.group("value") for match in CSS_VAR_RE.finditer(text)}
    background = variables.get("color-bg") or variables.get("explainer-bg")
    text_color = variables.get("color-text") or variables.get("explainer-text")
    muted = variables.get("color-muted") or variables.get("explainer-muted")
    if background and text_color and contrast_ratio(text_color, background) < 4.5:
        issues.append(AuditIssue("error", rpath, "Text/background contrast appears low."))
    if background and muted and contrast_ratio(muted, background) < 3.0:
        issues.append(AuditIssue("warning", rpath, "Muted/background contrast appears low."))
    return issues


def audit_site(site: Path) -> AuditReport:
    root = site if site.is_dir() else site.parent
    files = list(iter_frontend_files(site))
    issues: list[AuditIssue] = []
    html_files = 0
    css_files = 0
    if not files:
        issues.append(AuditIssue("error", str(site), "No frontend files found."))
    if site.is_dir() and not any((site / name).exists() for name in ("index.html", "src")):
        issues.append(AuditIssue("warning", str(site), "No obvious homepage entry found."))
    for path in files:
        text = read_text(path)
        suffix = path.suffix.lower()
        issues.extend(audit_claims(path, root, text))
        if suffix in HTML_EXTENSIONS:
            html_files += 1
            issues.extend(audit_html(path, root, text))
        if suffix in CSS_EXTENSIONS:
            css_files += 1
            issues.extend(audit_css(path, root, text))
    return AuditReport(
        site=str(site),
        files_checked=len(files),
        html_files=html_files,
        css_files=css_files,
        issues=issues,
        passed=not any(issue.severity == "error" for issue in issues),
    )


def report_to_markdown(report: AuditReport) -> str:
    lines = [
        "# Project Frontend Audit",
        "",
        f"Site: `{report.site}`",
        f"Files checked: {report.files_checked}",
        f"HTML files: {report.html_files}",
        f"CSS files: {report.css_files}",
        f"Passed: {report.passed}",
        "",
        "## Issues",
        "",
    ]
    if not report.issues:
        lines.append("No issues found by this lightweight static audit.")
    else:
        lines.extend(["| Severity | Path | Message | Evidence |", "|---|---|---|---|"])
        for issue in report.issues:
            evidence = issue.evidence.replace("|", "\\|")[:220]
            lines.append(
                f"| {issue.severity} | `{issue.path}` | {issue.message} | {evidence} |"
            )
    lines.extend(
        [
            "",
            "## Note",
            "",
            "This audit is static. Use Playwright CLI and interactive QA for rendered checks.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("scratch/project-explainer"))
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    site = args.site.expanduser().resolve()
    if not site.exists():
        raise SystemExit(f"Site path does not exist: {site}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = audit_site(site)
    data = asdict(report)
    data["issues"] = [asdict(issue) for issue in report.issues]
    (args.out_dir / "frontend_audit.json").write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )
    (args.out_dir / "frontend_audit.md").write_text(
        report_to_markdown(report),
        encoding="utf-8",
    )
    print(f"Wrote {args.out_dir / 'frontend_audit.json'}")
    print(f"Wrote {args.out_dir / 'frontend_audit.md'}")
    if args.strict and report.issues:
        return 2
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
