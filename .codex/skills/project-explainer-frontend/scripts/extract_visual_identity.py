#!/usr/bin/env python3
"""Extract a small visual identity brief from reference images."""

from __future__ import annotations

import argparse
import colorsys
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ColorSample:
    hex: str
    count: int
    percentage: float
    luminance: float
    saturation: float
    hue_degrees: float
    role_hint: str


@dataclass(frozen=True)
class ContrastPair:
    foreground: str
    background: str
    ratio: float
    wcag_aa_body: bool
    wcag_aa_large: bool


FONT_STACKS = {
    "technical editorial": {
        "display": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "body": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "mono": "'SFMono-Regular', Consolas, 'Liberation Mono', monospace",
        "candidates": ["Inter", "Public Sans", "IBM Plex Mono"],
    },
    "archival humanist": {
        "display": "'IBM Plex Serif', Georgia, serif",
        "body": "'IBM Plex Sans', system-ui, sans-serif",
        "mono": "'IBM Plex Mono', Consolas, monospace",
        "candidates": ["IBM Plex Serif", "IBM Plex Sans", "IBM Plex Mono"],
    },
    "laboratory geometric": {
        "display": "'Space Grotesk', system-ui, sans-serif",
        "body": "'Inter', system-ui, sans-serif",
        "mono": "'JetBrains Mono', Consolas, monospace",
        "candidates": ["Space Grotesk", "Inter", "JetBrains Mono"],
    },
}


def srgb_to_linear(channel: int) -> float:
    value = channel / 255
    if value <= 0.03928:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    red, green, blue = (srgb_to_linear(channel) for channel in rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: tuple[int, int, int], background: tuple[int, int, int]) -> float:
    first = relative_luminance(foreground)
    second = relative_luminance(background)
    lighter = max(first, second)
    darker = min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    clean = value.strip().lstrip("#")
    return tuple(int(clean[index : index + 2], 16) for index in (0, 2, 4))


def saturation_and_hue(rgb: tuple[int, int, int]) -> tuple[float, float]:
    red, green, blue = [channel / 255 for channel in rgb]
    hue, _lightness, saturation = colorsys.rgb_to_hls(red, green, blue)
    return saturation, hue * 360


def role_hint(rgb: tuple[int, int, int]) -> str:
    saturation, _hue = saturation_and_hue(rgb)
    luminance = relative_luminance(rgb)
    if luminance < 0.18:
        return "dark background / ink"
    if luminance > 0.86 and saturation < 0.22:
        return "light background / paper"
    if saturation < 0.14:
        return "neutral / border / muted text"
    if saturation >= 0.34:
        return "accent / callout"
    return "supporting color"


def require_pillow() -> Any:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit(
            "Pillow is required. Install with: "
            "python -m pip install -r "
            ".codex/skills/project-explainer-frontend/requirements.txt"
        ) from exc
    return Image


def load_pixels(path: Path, max_side: int = 360) -> list[tuple[int, int, int]]:
    image_module = require_pillow()
    image = image_module.open(path).convert("RGB")
    image.thumbnail((max_side, max_side))
    pixels = list(image.getdata())
    stride = max(1, len(pixels) // 8000)
    return [tuple(pixel) for pixel in pixels[::stride]]


def bucket_rgb(rgb: tuple[int, int, int], step: int = 24) -> tuple[int, int, int]:
    return tuple(min(255, round(channel / step) * step) for channel in rgb)


def extract_palette(paths: list[Path], palette_size: int) -> list[ColorSample]:
    counter: Counter[tuple[int, int, int]] = Counter()
    for path in paths:
        for pixel in load_pixels(path):
            counter[bucket_rgb(pixel)] += 1
    total = sum(counter.values()) or 1
    samples: list[ColorSample] = []
    for rgb, count in counter.most_common(max(palette_size * 2, 12)):
        saturation, hue = saturation_and_hue(rgb)
        samples.append(
            ColorSample(
                hex=rgb_to_hex(rgb),
                count=count,
                percentage=round(count / total, 4),
                luminance=round(relative_luminance(rgb), 4),
                saturation=round(saturation, 4),
                hue_degrees=round(hue, 1),
                role_hint=role_hint(rgb),
            )
        )
    return samples[:palette_size]


def choose_roles(samples: list[ColorSample]) -> dict[str, str]:
    if not samples:
        return {
            "background": "#F7F4EA",
            "surface": "#FFFFFF",
            "text": "#1F2933",
            "muted": "#5B6770",
            "accent": "#5668A6",
            "accent_2": "#2E7D73",
            "border": "#D7D0BF",
        }
    darks = [sample for sample in samples if sample.luminance < 0.24]
    lights = [sample for sample in samples if sample.luminance > 0.78]
    neutrals = [sample for sample in samples if sample.saturation < 0.18]
    accents = [sample for sample in samples if sample.saturation >= 0.28]
    background = lights[0] if lights else (darks[0] if darks else samples[0])
    bg_rgb = hex_to_rgb(background.hex)
    white = (245, 247, 250)
    black = (31, 41, 51)
    text_rgb = white if contrast_ratio(white, bg_rgb) > contrast_ratio(black, bg_rgb) else black
    text = rgb_to_hex(text_rgb)
    surface = next((sample for sample in samples if sample.hex != background.hex), background)
    accent = accents[0] if accents else surface
    accent_2 = next(
        (sample for sample in accents[1:] if abs(sample.hue_degrees - accent.hue_degrees) > 24),
        accent,
    )
    muted = neutrals[0] if neutrals else surface
    border = next((sample for sample in neutrals if 0.2 <= sample.luminance <= 0.8), muted)
    return {
        "background": background.hex,
        "surface": surface.hex,
        "text": text,
        "muted": muted.hex,
        "accent": accent.hex,
        "accent_2": accent_2.hex,
        "border": border.hex,
    }


def typography_for_roles(roles: dict[str, str], font_note: str | None) -> dict[str, Any]:
    bg_luminance = relative_luminance(hex_to_rgb(roles["background"]))
    style = "technical editorial"
    rationale = ["Default AEther style favors precise technical editorial typography."]
    if bg_luminance < 0.35:
        style = "laboratory geometric"
        rationale.append("Dark background suggests a restrained laboratory-console direction.")
    elif roles["background"] == roles["surface"]:
        style = "archival humanist"
        rationale.append("Paper-like palette suggests an archival document direction.")
    if font_note:
        rationale.append(f"User font note supplied: {font_note}")
    stacks = FONT_STACKS[style]
    return {
        "style_direction": style,
        "confidence": "low-to-medium",
        "display_stack": stacks["display"],
        "body_stack": stacks["body"],
        "mono_stack": stacks["mono"],
        "external_font_candidates": stacks["candidates"],
        "rationale": rationale,
        "limitation": (
            "Exact font identification from raster images is not reliable. "
            "Treat this as style direction only."
        ),
    }


def contrast_pairs(roles: dict[str, str]) -> list[ContrastPair]:
    pairs = [
        ("text", "background"),
        ("text", "surface"),
        ("muted", "background"),
        ("background", "accent"),
    ]
    output: list[ContrastPair] = []
    for foreground_name, background_name in pairs:
        foreground = roles[foreground_name]
        background = roles[background_name]
        ratio = contrast_ratio(hex_to_rgb(foreground), hex_to_rgb(background))
        output.append(
            ContrastPair(
                foreground=f"{foreground_name}:{foreground}",
                background=f"{background_name}:{background}",
                ratio=round(ratio, 2),
                wcag_aa_body=ratio >= 4.5,
                wcag_aa_large=ratio >= 3.0,
            )
        )
    return output


def css_from_identity(roles: dict[str, str], typography: dict[str, Any]) -> str:
    return f"""/* AEther visual identity tokens generated from reference images. */
:root {{
  --explainer-bg: {roles["background"]};
  --explainer-surface: {roles["surface"]};
  --explainer-text: {roles["text"]};
  --explainer-muted: {roles["muted"]};
  --explainer-accent: {roles["accent"]};
  --explainer-accent-2: {roles["accent_2"]};
  --explainer-border: {roles["border"]};
  --explainer-font-display: {typography["display_stack"]};
  --explainer-font-body: {typography["body_stack"]};
  --explainer-font-mono: {typography["mono_stack"]};
}}

:focus-visible {{
  outline: 3px solid var(--explainer-accent-2);
  outline-offset: 3px;
}}

@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }}
}}
"""


def markdown_report(data: dict[str, Any]) -> str:
    lines = ["# Visual Identity Brief", "", "## Source images", ""]
    lines.extend(f"- `{image}`" for image in data["source_images"])
    lines.extend(["", "## Color roles", "", "| Role | Color |", "|---|---|"])
    lines.extend(f"| {role} | `{value}` |" for role, value in data["color_roles"].items())
    lines.extend(["", "## Typography", ""])
    typography = data["typography"]
    lines.append(f"- Style direction: {typography['style_direction']}")
    lines.append(f"- Confidence: {typography['confidence']}")
    lines.append(f"- Limitation: {typography['limitation']}")
    lines.extend(["", "## Contrast checks", ""])
    lines.extend(["| Foreground | Background | Ratio | AA body |", "|---|---|---:|---|"])
    for pair in data["contrast_pairs"]:
        lines.append(
            f"| {pair['foreground']} | {pair['background']} | "
            f"{pair['ratio']} | {pair['wcag_aa_body']} |"
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", action="append", required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("scratch/project-explainer"))
    parser.add_argument("--palette-size", type=int, default=8)
    parser.add_argument("--site-name", default="The AEther Flow")
    parser.add_argument("--font-note", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [Path(value).expanduser().resolve() for value in args.image]
    missing = [path.as_posix() for path in paths if not path.exists()]
    if missing:
        raise SystemExit(f"Missing image file(s): {', '.join(missing)}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    palette = extract_palette(paths, args.palette_size)
    roles = choose_roles(palette)
    typography = typography_for_roles(roles, args.font_note)
    data: dict[str, Any] = {
        "site_name": args.site_name,
        "source_images": [path.as_posix() for path in paths],
        "color_roles": roles,
        "palette_samples": [asdict(sample) for sample in palette],
        "typography": typography,
        "contrast_pairs": [asdict(pair) for pair in contrast_pairs(roles)],
        "usage_note": "Use these tokens as a starting design brief; verify visually.",
    }
    (args.out_dir / "visual_identity.json").write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )
    (args.out_dir / "visual_identity.md").write_text(markdown_report(data), encoding="utf-8")
    (args.out_dir / "design_tokens.css").write_text(
        css_from_identity(roles, typography),
        encoding="utf-8",
    )
    print(f"Wrote {args.out_dir / 'visual_identity.json'}")
    print(f"Wrote {args.out_dir / 'visual_identity.md'}")
    print(f"Wrote {args.out_dir / 'design_tokens.css'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
