#!/usr/bin/env python3
"""Scan website and optional upstream evidence for an AEther explainer brief."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

TEXT_EXTENSIONS = {
    ".astro",
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mdx",
    ".mjs",
    ".py",
    ".sh",
    ".tex",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}

LANGUAGE_BY_EXT = {
    ".astro": "Astro",
    ".css": "CSS",
    ".csv": "CSV",
    ".html": "HTML",
    ".js": "JavaScript",
    ".json": "JSON",
    ".md": "Markdown",
    ".mdx": "MDX",
    ".mjs": "JavaScript",
    ".py": "Python",
    ".sh": "Shell",
    ".tex": "TeX",
    ".toml": "TOML",
    ".ts": "TypeScript",
    ".yaml": "YAML",
    ".yml": "YAML",
}

EXCLUDE_DIRS = {
    ".astro",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "scratch",
}

HIGH_VALUE_NAMES = {
    "AGENTS.md",
    "CONTEXT.md",
    "Makefile",
    "README.md",
    "astro.config.mjs",
    "package.json",
    "pyproject.toml",
    "source_manifest.json",
    "source_manifest.schema.json",
    "tsconfig.json",
}

HIGH_VALUE_DIRS = {
    "docs",
    "html",
    "implementations_plans",
    "public",
    "research_control",
    "scripts",
    "src",
}

CLAIM_BOUNDARY_TERMS = [
    "adoption",
    "blocked",
    "candidate",
    "claim status",
    "draft/control",
    "fail-closed",
    "human-gated",
    "limitation",
    "not adopted",
    "proposal-only",
    "reviewed",
    "source authority",
    "source-only",
    "unverified",
]


@dataclass(frozen=True)
class FileEvidence:
    origin: str
    path: str
    kind: str
    language_or_type: str
    size_bytes: int
    headings: list[str]
    evidence_terms: list[str]
    opening_lines: list[str]


@dataclass(frozen=True)
class ProjectBrief:
    project_name: str
    website_root: str
    source_root: str | None
    source_root_available: bool
    source_authority_policy: str
    detected_languages: dict[str, int]
    likely_frontend_stack: list[str]
    validation_commands: list[str]
    high_value_files: list[FileEvidence]
    directory_map: dict[str, list[str]]
    project_summary_candidates: list[str]
    claim_boundary_terms_found: dict[str, list[str]]
    implementation_guidance: list[str]


def should_skip(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in EXCLUDE_DIRS for part in relative.parts)


def iter_files(root: Path, max_files: int) -> Iterable[Path]:
    count = 0
    for path in sorted(root.rglob("*")):
        if count >= max_files:
            break
        if path.is_dir() or should_skip(path, root):
            continue
        count += 1
        yield path


def safe_read(path: Path, max_chars: int = 24000) -> str:
    if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in HIGH_VALUE_NAMES:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError:
        return ""


def language_name(path: Path) -> str:
    return LANGUAGE_BY_EXT.get(path.suffix.lower(), path.suffix.lower().lstrip(".") or "file")


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                headings.append(heading[:160])
    return headings[:12]


def opening_lines(text: str, limit: int = 6) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()
        if not cleaned or cleaned.startswith(("---", "```", "<!--")):
            continue
        lines.append(cleaned[:220])
        if len(lines) >= limit:
            break
    return lines


def find_terms(text: str) -> list[str]:
    lower = text.lower()
    return [term for term in CLAIM_BOUNDARY_TERMS if term in lower]


def classify_file(path: Path, root: Path) -> str:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return "external"
    parts = set(relative.parts[:-1])
    if path.name in HIGH_VALUE_NAMES:
        return "project metadata"
    if parts & {"docs", "html"} or path.suffix.lower() in {".md", ".mdx", ".tex"}:
        return "documentation"
    if parts & {"research_control", "implementations_plans"}:
        return "source authority evidence"
    if path.suffix.lower() in {".astro", ".css", ".html", ".js", ".ts"}:
        return "frontend"
    if path.suffix.lower() in {".json", ".toml", ".yaml", ".yml"}:
        return "configuration"
    if path.suffix.lower() in {".py", ".sh"}:
        return "tooling"
    return "other"


def is_relevant(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    if path.name in HIGH_VALUE_NAMES:
        return True
    if relative.parts and relative.parts[0] in HIGH_VALUE_DIRS:
        return True
    return path.suffix.lower() in {".astro", ".css", ".md", ".mdx", ".tex"}


def summarize_readme(text: str) -> list[str]:
    candidates: list[str] = []
    paragraph: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            continue
        if not line:
            if paragraph:
                candidate = " ".join(paragraph)
                if len(candidate) > 40:
                    candidates.append(candidate[:700])
                paragraph = []
            if len(candidates) >= 4:
                break
            continue
        if line.startswith(("[!", "<", "|", "```")):
            continue
        paragraph.append(line)
        if len(" ".join(paragraph)) > 300:
            candidates.append(" ".join(paragraph)[:700])
            paragraph = []
        if len(candidates) >= 4:
            break
    if paragraph and len(candidates) < 4:
        candidates.append(" ".join(paragraph)[:700])
    return candidates


def detect_frontend_stack(files: list[Path], texts_by_path: dict[Path, str]) -> list[str]:
    names = {path.name for path in files}
    suffixes = {path.suffix.lower() for path in files}
    package_text = next(
        (text for path, text in texts_by_path.items() if path.name == "package.json"),
        "",
    ).lower()
    stack: list[str] = []
    if "astro" in package_text or "astro.config.mjs" in names:
        stack.append("Astro static site")
    if "@astrojs/mdx" in package_text or ".mdx" in suffixes:
        stack.append("Astro MDX")
    if "katex" in package_text:
        stack.append("KaTeX math rendering")
    if ".css" in suffixes:
        stack.append("CSS")
    if ".ts" in suffixes:
        stack.append("TypeScript")
    return sorted(set(stack))


def build_directory_map(
    roots_and_files: list[tuple[str, Path, list[Path]]],
) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = defaultdict(list)
    for origin, root, files in roots_and_files:
        for path in files:
            try:
                relative = path.relative_to(root)
            except ValueError:
                continue
            top = relative.parts[0] if len(relative.parts) > 1 else "."
            key = f"{origin}:{top}"
            if len(mapping[key]) < 12:
                mapping[key].append(relative.as_posix())
    return dict(sorted(mapping.items()))


def collect_evidence(
    origin: str,
    root: Path,
    files: list[Path],
    texts_by_path: dict[Path, str],
    max_evidence: int,
) -> tuple[list[FileEvidence], dict[str, list[str]]]:
    evidence: list[FileEvidence] = []
    claim_terms: dict[str, list[str]] = {}
    candidates = sorted(
        [path for path in files if is_relevant(path, root)],
        key=lambda path: (0 if path.name in HIGH_VALUE_NAMES else 1, path.as_posix()),
    )
    for path in candidates:
        text = texts_by_path.get(path, "")
        terms = find_terms(text)
        relative = path.relative_to(root).as_posix()
        evidence_key = f"{origin}:{relative}"
        if terms:
            claim_terms[evidence_key] = terms
        if len(evidence) >= max_evidence:
            continue
        if not text and path.suffix.lower() not in {".svg", ".png", ".jpg", ".webp"}:
            continue
        evidence.append(
            FileEvidence(
                origin=origin,
                path=relative,
                kind=classify_file(path, root),
                language_or_type=language_name(path),
                size_bytes=path.stat().st_size,
                headings=extract_headings(text),
                evidence_terms=terms,
                opening_lines=opening_lines(text),
            )
        )
    return evidence, claim_terms


def build_policy(source_root: Path | None, source_available: bool) -> str:
    if source_root is None:
        return (
            "No upstream source root was provided. Fail closed for new public "
            "scientific, mathematical, governance, or research-workflow claims."
        )
    if source_available:
        return (
            "Upstream source root was available for orientation. Treat scanner "
            "results as a map; inspect source files directly before final copy."
        )
    return (
        "Configured upstream source root was unavailable. Fail closed for new "
        "public scientific, mathematical, governance, or research-workflow claims."
    )


def create_brief(
    repo: Path,
    source_root: Path | None,
    max_files: int,
    max_evidence: int,
) -> ProjectBrief:
    website_files = list(iter_files(repo, max_files=max_files))
    website_texts = {path: safe_read(path) for path in website_files}
    source_available = bool(source_root and source_root.is_dir())
    source_files: list[Path] = []
    source_texts: dict[Path, str] = {}
    if source_root and source_available:
        source_files = list(iter_files(source_root, max_files=max(100, max_files // 2)))
        source_texts = {path: safe_read(path) for path in source_files}

    language_counts = Counter(
        language_name(path)
        for path in [*website_files, *source_files]
        if path.suffix or path.name in HIGH_VALUE_NAMES
    )
    website_evidence, website_terms = collect_evidence(
        "website",
        repo,
        website_files,
        website_texts,
        max_evidence=max_evidence,
    )
    source_evidence, source_terms = collect_evidence(
        "source",
        source_root,
        source_files,
        source_texts,
        max_evidence=max(10, max_evidence // 2),
    ) if source_root and source_available else ([], {})

    readme_text = next(
        (text for path, text in website_texts.items() if path.name.lower() == "readme.md"),
        "",
    )
    summaries = summarize_readme(readme_text)
    if not summaries:
        summaries = ["The AEther Flow Website is a static reader-facing site."]

    guidance = [
        "Use the existing Astro static-site stack.",
        "Keep website copy reader-facing and source-boundary aware.",
        "Do not add public research claims unless upstream source evidence is inspected.",
        "Use claim status and source references for reviewed or draft source-backed pages.",
        "Run repository validators plus browser QA before signoff.",
    ]
    if not source_available:
        guidance.append("Upstream source root unavailable; fail closed for new public claims.")

    roots_and_files = [("website", repo, website_files)]
    if source_root and source_available:
        roots_and_files.append(("source", source_root, source_files))

    return ProjectBrief(
        project_name="The AEther Flow",
        website_root=str(repo),
        source_root=str(source_root) if source_root else None,
        source_root_available=source_available,
        source_authority_policy=build_policy(source_root, source_available),
        detected_languages=dict(language_counts.most_common(18)),
        likely_frontend_stack=detect_frontend_stack(website_files, website_texts),
        validation_commands=[
            "make test",
            "make lint",
            "make validate",
            "npm run build",
        ],
        high_value_files=[*website_evidence, *source_evidence],
        directory_map=build_directory_map(roots_and_files),
        project_summary_candidates=summaries,
        claim_boundary_terms_found={**website_terms, **source_terms},
        implementation_guidance=guidance,
    )


def brief_to_markdown(brief: ProjectBrief) -> str:
    lines = [
        f"# Project Story Brief: {brief.project_name}",
        "",
        f"Website root: `{brief.website_root}`",
        f"Source root: `{brief.source_root or 'not provided'}`",
        f"Source root available: `{brief.source_root_available}`",
        "",
        "## Source authority policy",
        "",
        brief.source_authority_policy,
        "",
        "## Summary candidates",
        "",
    ]
    lines.extend(f"- {item}" for item in brief.project_summary_candidates)
    lines.extend(["", "## Likely frontend stack", ""])
    lines.extend(f"- {item}" for item in brief.likely_frontend_stack)
    lines.extend(["", "## Implementation guidance", ""])
    lines.extend(f"- {item}" for item in brief.implementation_guidance)
    lines.extend(["", "## High-value evidence", ""])
    for item in brief.high_value_files:
        lines.extend(
            [
                f"### `{item.origin}:{item.path}`",
                "",
                f"- Kind: {item.kind}",
                f"- Type: {item.language_or_type}",
                f"- Size: {item.size_bytes} bytes",
            ]
        )
        if item.headings:
            lines.append(f"- Headings: {', '.join(item.headings[:8])}")
        if item.evidence_terms:
            lines.append(f"- Claim-boundary terms: {', '.join(item.evidence_terms)}")
        if item.opening_lines:
            lines.append("- Opening evidence:")
            lines.extend(f"  - {line}" for line in item.opening_lines[:4])
        lines.append("")
    lines.extend(["## Directory map", ""])
    for key, entries in brief.directory_map.items():
        lines.append(f"### `{key}`")
        lines.extend(f"- `{entry}`" for entry in entries)
        lines.append("")
    if brief.claim_boundary_terms_found:
        lines.extend(["## Claim-boundary terms found", ""])
        for path, terms in brief.claim_boundary_terms_found.items():
            lines.append(f"- `{path}`: {', '.join(sorted(set(terms)))}")
    return "\n".join(lines).strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--source-root", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=Path("scratch/project-explainer"))
    parser.add_argument("--max-files", type=int, default=900)
    parser.add_argument("--max-evidence", type=int, default=80)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.expanduser().resolve()
    if not repo.is_dir():
        raise SystemExit(f"Repository root not found: {repo}")
    source_root = args.source_root.expanduser().resolve() if args.source_root else None
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    brief = create_brief(repo, source_root, args.max_files, args.max_evidence)
    data = asdict(brief)
    (out_dir / "project_story_brief.json").write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )
    (out_dir / "project_story_brief.md").write_text(brief_to_markdown(brief), encoding="utf-8")
    print(f"Wrote {out_dir / 'project_story_brief.json'}")
    print(f"Wrote {out_dir / 'project_story_brief.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
