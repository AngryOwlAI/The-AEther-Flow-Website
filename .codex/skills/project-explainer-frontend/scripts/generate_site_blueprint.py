#!/usr/bin/env python3
"""Generate an Astro-ready AEther explainer blueprint from a story brief."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_IDENTITY: dict[str, Any] = {
    "color_roles": {
        "background": "#F7F4EA",
        "surface": "#FFFFFF",
        "text": "#1F2933",
        "muted": "#5B6770",
        "accent": "#5668A6",
        "accent_2": "#2E7D73",
        "border": "#D7D0BF",
    },
    "typography": {
        "style_direction": "technical editorial",
        "confidence": "fallback",
        "display_stack": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "body_stack": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "mono_stack": "'SFMono-Regular', Consolas, 'Liberation Mono', monospace",
        "limitation": "Fallback identity; no reference image was supplied.",
    },
}


def load_json(path: Path | None, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if path is None:
        return fallback or {}
    if not path.exists():
        if fallback is not None:
            return fallback
        raise SystemExit(f"Missing JSON file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"Expected object JSON: {path}")
    return data


def clean_text(text: str, max_len: int = 300) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    if len(cleaned) > max_len:
        return cleaned[: max_len - 1].rstrip() + "..."
    return cleaned


def first_summary(story: dict[str, Any]) -> str:
    for candidate in story.get("project_summary_candidates", []):
        if isinstance(candidate, str) and candidate.strip():
            return clean_text(candidate)
    return (
        "The AEther Flow Website is a static reader-facing presentation layer "
        "for reviewed AEther Flow material."
    )


def source_policy(story: dict[str, Any]) -> str:
    policy = story.get("source_authority_policy")
    if isinstance(policy, str) and policy:
        return policy
    return (
        "Fail closed for scientific, mathematical, governance, and "
        "research-workflow claims unless upstream source evidence is inspected."
    )


def evidence_paths(story: dict[str, Any], limit: int = 14) -> list[str]:
    output: list[str] = []
    for item in story.get("high_value_files", []):
        if not isinstance(item, dict):
            continue
        origin = item.get("origin")
        path = item.get("path")
        if isinstance(origin, str) and isinstance(path, str):
            value = f"{origin}:{path}"
            if value not in output:
                output.append(value)
        if len(output) >= limit:
            break
    return output


def claim_boundary_notes(story: dict[str, Any]) -> list[str]:
    notes = [source_policy(story)]
    terms = story.get("claim_boundary_terms_found")
    if isinstance(terms, dict) and terms:
        for path, found in list(terms.items())[:8]:
            if isinstance(found, list):
                notes.append(f"{path}: {', '.join(sorted(set(map(str, found))))}")
    else:
        notes.append(
            "No scanner-detected claim-boundary terms. Still use source notices "
            "for source-backed content."
        )
    return notes


def sections(source_available: bool) -> list[dict[str, str]]:
    authority_guidance = (
        "Use inspected upstream evidence for claim status and source references."
        if source_available
        else "Do not introduce new public research claims; explain only website state."
    )
    return [
        {
            "id": "hero",
            "title": "Hero",
            "purpose": "State the page subject and one reader action.",
            "content_guidance": "Use precise, non-marketing language.",
        },
        {
            "id": "what-it-is",
            "title": "What it is",
            "purpose": "Explain the subject in reader-facing language.",
            "content_guidance": "Separate website presentation from source authority.",
        },
        {
            "id": "why-it-exists",
            "title": "Why it exists",
            "purpose": "Explain the reader need or publication problem.",
            "content_guidance": "Ground motivation in README, CONTEXT, or source evidence.",
        },
        {
            "id": "how-it-works",
            "title": "How it works",
            "purpose": "Show the publication or research-control relationship.",
            "content_guidance": "Prefer source-boundary diagrams and reading-path structures.",
        },
        {
            "id": "evidence-state",
            "title": "Evidence and state",
            "purpose": "Expose claim status, source refs, and limitations.",
            "content_guidance": authority_guidance,
        },
        {
            "id": "reading-path",
            "title": "Reading path",
            "purpose": "Guide readers to resources, source-backed pages, and downloads.",
            "content_guidance": "Use existing routes and manifest-backed resources.",
        },
    ]


def design_thesis(identity: dict[str, Any]) -> dict[str, Any]:
    roles = identity.get("color_roles", DEFAULT_IDENTITY["color_roles"])
    typography = identity.get("typography", DEFAULT_IDENTITY["typography"])
    return {
        "summary": (
            "Use a restrained evidence-led atlas: source-boundary notices, "
            "publication-map structure, and clear claim-state panels."
        ),
        "visual_signature": "source-boundary evidence atlas",
        "palette_strategy": {
            "background": roles.get("background"),
            "surface": roles.get("surface"),
            "text": roles.get("text"),
            "muted": roles.get("muted"),
            "accent": roles.get("accent"),
            "accent_2": roles.get("accent_2"),
            "border": roles.get("border"),
        },
        "typography_strategy": {
            "style_direction": typography.get("style_direction"),
            "display_stack": typography.get("display_stack"),
            "body_stack": typography.get("body_stack"),
            "mono_stack": typography.get("mono_stack"),
            "note": typography.get("limitation"),
        },
    }


def css_tokens(identity: dict[str, Any]) -> str:
    roles = identity.get("color_roles", DEFAULT_IDENTITY["color_roles"])
    typography = identity.get("typography", DEFAULT_IDENTITY["typography"])
    display_stack = typography.get("display_stack", DEFAULT_IDENTITY["typography"]["display_stack"])
    body_stack = typography.get("body_stack", DEFAULT_IDENTITY["typography"]["body_stack"])
    mono_stack = typography.get("mono_stack", DEFAULT_IDENTITY["typography"]["mono_stack"])
    return f"""/* AEther explainer tokens. Review before production use. */
:root {{
  --explainer-bg: {roles.get("background", "#F7F4EA")};
  --explainer-surface: {roles.get("surface", "#FFFFFF")};
  --explainer-text: {roles.get("text", "#1F2933")};
  --explainer-muted: {roles.get("muted", "#5B6770")};
  --explainer-accent: {roles.get("accent", "#5668A6")};
  --explainer-accent-2: {roles.get("accent_2", "#2E7D73")};
  --explainer-border: {roles.get("border", "#D7D0BF")};
  --explainer-font-display: {display_stack};
  --explainer-font-body: {body_stack};
  --explainer-font-mono: {mono_stack};
  --explainer-measure: 72ch;
  --explainer-section-space: clamp(3.5rem, 7vw, 7rem);
}}
"""


def build_blueprint(story: dict[str, Any], identity: dict[str, Any]) -> dict[str, Any]:
    source_available = bool(story.get("source_root_available"))
    return {
        "project_name": "The AEther Flow",
        "site_purpose": (
            "Create an informational Astro frontend surface that explains "
            "AEther Flow material without changing source authority."
        ),
        "project_summary_candidate": first_summary(story),
        "recommended_implementation_target": "existing Astro static-site stack",
        "source_root_available": source_available,
        "source_authority_policy": source_policy(story),
        "design_thesis": design_thesis(identity),
        "sections": sections(source_available),
        "evidence_files_to_inspect": evidence_paths(story),
        "claim_boundary_notes": claim_boundary_notes(story),
        "implementation_contract": [
            "Use src/pages, src/layouts, src/components, src/lib, and src/styles.",
            "Include source authority language on source-backed reader pages.",
            "Use claim_status and source_refs frontmatter for MDX claim surfaces.",
            "Do not add runtime UI behavior unless explicitly requested.",
            "Do not add production dependencies without approval.",
            "Run existing validators, this skill audit, and Playwright QA.",
        ],
    }


def blueprint_to_markdown(blueprint: dict[str, Any]) -> str:
    lines = [
        f"# Site Blueprint: {blueprint['project_name']}",
        "",
        "## Purpose",
        "",
        blueprint["site_purpose"],
        "",
        "## Source Authority",
        "",
        blueprint["source_authority_policy"],
        "",
        "## Design Thesis",
        "",
        blueprint["design_thesis"]["summary"],
        "",
        f"- Visual signature: {blueprint['design_thesis']['visual_signature']}",
        f"- Implementation target: {blueprint['recommended_implementation_target']}",
        "",
        "## Sections",
        "",
    ]
    for section in blueprint["sections"]:
        lines.extend(
            [
                f"### {section['title']}",
                "",
                f"- Purpose: {section['purpose']}",
                f"- Guidance: {section['content_guidance']}",
                "",
            ]
        )
    lines.extend(["## Evidence to Inspect", ""])
    lines.extend(f"- `{path}`" for path in blueprint["evidence_files_to_inspect"])
    lines.extend(["", "## Claim Boundary Notes", ""])
    lines.extend(f"- {note}" for note in blueprint["claim_boundary_notes"])
    lines.extend(["", "## Implementation Contract", ""])
    lines.extend(f"- {item}" for item in blueprint["implementation_contract"])
    return "\n".join(lines).strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", type=Path, required=True)
    parser.add_argument("--identity", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=Path("scratch/project-explainer"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    story = load_json(args.story)
    identity = load_json(args.identity, fallback=DEFAULT_IDENTITY)
    blueprint = build_blueprint(story, identity)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "site_blueprint.json").write_text(
        json.dumps(blueprint, indent=2),
        encoding="utf-8",
    )
    (args.out_dir / "site_blueprint.md").write_text(
        blueprint_to_markdown(blueprint),
        encoding="utf-8",
    )
    (args.out_dir / "design_tokens.css").write_text(css_tokens(identity), encoding="utf-8")
    print(f"Wrote {args.out_dir / 'site_blueprint.json'}")
    print(f"Wrote {args.out_dir / 'site_blueprint.md'}")
    print(f"Wrote {args.out_dir / 'design_tokens.css'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
