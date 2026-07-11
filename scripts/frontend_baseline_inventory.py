#!/usr/bin/env python3
"""Generate deterministic static evidence for frontend baseline packet FE-G0-02."""

from __future__ import annotations

import argparse
import gzip
import json
import re
import statistics
import struct
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


WORD_RE = re.compile(r"[A-Za-z0-9Ææ][A-Za-z0-9Ææ'’_-]*")
MOTION_TOKEN_RE = re.compile(r"(?:motion|animate|orbit|pulse|spin|flow|drift|sweep|glow)", re.I)
CSS_BLOCK_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def route_for_html(path: Path, dist_root: Path) -> str:
    relative = path.relative_to(dist_root)
    if relative == Path("index.html"):
        return "/"
    parts = relative.parts[:-1]
    return "/" + "/".join(parts) + "/"


def route_for_source(path: Path, pages_root: Path) -> str:
    relative = path.relative_to(pages_root)
    parts = list(relative.parts)
    stem = Path(parts[-1]).stem
    parts[-1] = stem
    if stem == "index":
        parts.pop()
    return "/" + ("/".join(parts) + "/" if parts else "")


class PageInventoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.svg_depth = 0
        self.svg_records: list[dict[str, Any]] = []
        self.current_svg: dict[str, Any] | None = None
        self.words: list[str] = []
        self.tables = 0
        self.table_records: list[dict[str, Any]] = []
        self.current_table: dict[str, Any] | None = None
        self.in_thead = False
        self.in_table_header = False
        self.in_caption = False
        self.figcaptions = 0
        self.filters = 0
        self.filter_references = 0
        self.motion_hook_elements = 0
        self.images: list[dict[str, Any]] = []
        self.ids: list[str] = []
        self.nav_stack: list[dict[str, Any]] = []
        self.nav_records: list[dict[str, Any]] = []
        self.action_count = 0
        self.gallery_items = 0
        self.is_redirect = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        tag = tag.lower()

        if "id" in attrs_dict:
            self.ids.append(attrs_dict["id"])

        if tag == "meta" and attrs_dict.get("http-equiv", "").lower() == "refresh":
            self.is_redirect = True

        if tag in {"script", "style", "noscript", "template"}:
            self.skip_depth += 1

        if tag == "svg":
            self.svg_depth += 1
            record = {
                "role": attrs_dict.get("role", ""),
                "aria_hidden": attrs_dict.get("aria-hidden", ""),
                "aria_labelledby": attrs_dict.get("aria-labelledby", ""),
                "aria_label": attrs_dict.get("aria-label", ""),
                "title_count": 0,
                "description_count": 0,
                "filter_count": 0,
                "motion_hook_count": 0,
                "id_count": 1 if "id" in attrs_dict else 0,
            }
            self.svg_records.append(record)
            self.current_svg = record
        elif self.svg_depth:
            if "id" in attrs_dict and self.current_svg:
                self.current_svg["id_count"] += 1
            if tag == "title" and self.current_svg:
                self.current_svg["title_count"] += 1
            if tag == "desc" and self.current_svg:
                self.current_svg["description_count"] += 1
            if tag == "filter" and self.current_svg:
                self.current_svg["filter_count"] += 1
            if tag in {"animate", "animatemotion", "animatetransform", "set"} and self.current_svg:
                self.current_svg["motion_hook_count"] += 1

        if tag == "table":
            self.tables += 1
            self.current_table = {
                "class": attrs_dict.get("class", ""),
                "column_headers": [],
                "caption": "",
            }
            self.table_records.append(self.current_table)
        if tag == "thead" and self.current_table is not None:
            self.in_thead = True
        if tag == "th" and self.in_thead:
            self.in_table_header = True
        if tag == "caption" and self.current_table is not None:
            self.in_caption = True
        if tag == "figcaption":
            self.figcaptions += 1
        if tag == "filter":
            self.filters += 1
        if "filter" in attrs_dict:
            self.filter_references += 1

        class_tokens = attrs_dict.get("class", "")
        data_motion = any(key.startswith("data-motion") for key in attrs_dict)
        native_motion = tag in {"animate", "animatemotion", "animatetransform", "set"}
        if data_motion or native_motion or MOTION_TOKEN_RE.search(class_tokens):
            self.motion_hook_elements += 1
            if self.current_svg:
                self.current_svg["motion_hook_count"] += 1

        if tag == "img":
            source = attrs_dict.get("src", "")
            self.images.append(
                {
                    "src": source,
                    "remote": source.startswith(("http://", "https://")),
                    "alt_present": bool(attrs_dict.get("alt", "")),
                    "decorative_alt": attrs_dict.get("alt") == "",
                    "width": attrs_dict.get("width", ""),
                    "height": attrs_dict.get("height", ""),
                    "loading": attrs_dict.get("loading", "auto"),
                    "decoding": attrs_dict.get("decoding", "auto"),
                }
            )

        if tag == "nav":
            record = {
                "aria_label": attrs_dict.get("aria-label", ""),
                "anchor_count": 0,
                "button_count": 0,
            }
            self.nav_stack.append(record)
            self.nav_records.append(record)
        if self.nav_stack and tag == "a":
            self.nav_stack[-1]["anchor_count"] += 1
        if self.nav_stack and tag == "button":
            self.nav_stack[-1]["button_count"] += 1

        if tag in {"a", "button", "input", "select", "textarea"}:
            self.action_count += 1

        if tag == "article" and "diagram-gallery-item" in class_tokens.split():
            self.gallery_items += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "template"} and self.skip_depth:
            self.skip_depth -= 1
        if tag == "nav" and self.nav_stack:
            self.nav_stack.pop()
        if tag == "th":
            self.in_table_header = False
        if tag == "thead":
            self.in_thead = False
        if tag == "caption":
            self.in_caption = False
        if tag == "table":
            self.current_table = None
        if tag == "svg" and self.svg_depth:
            self.svg_depth -= 1
            if not self.svg_depth:
                self.current_svg = None

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and not self.svg_depth:
            self.words.extend(WORD_RE.findall(data))
        text = " ".join(data.split())
        if text and self.current_table is not None:
            if self.in_table_header:
                self.current_table["column_headers"].append(text)
            if self.in_caption:
                self.current_table["caption"] = (
                    f"{self.current_table['caption']} {text}".strip()
                )


def classify_svg(record: dict[str, Any]) -> str:
    if record["aria_hidden"] == "true" or record["role"] in {"none", "presentation"}:
        return "explicit_decorative"
    if record["role"] == "img" or record["aria_labelledby"] or record["aria_label"]:
        return "informational"
    return "unclassified"


def classify_table(record: dict[str, Any]) -> str:
    headers = [item.lower() for item in record["column_headers"]]
    first = headers[0] if headers else ""
    joined = " ".join(headers)
    if first == "term":
        return "public_vocabulary_or_definition"
    if any(token in joined for token in ("asset", "download", "file", "format", "bytes")):
        return "download_or_asset_metadata"
    if len(headers) <= 4 and any(
        token in joined for token in ("status", "state", "signal", "condition")
    ):
        return "small_status_matrix"
    if len(headers) >= 5:
        return "dense_specialist_data"
    return "true_comparison_table"


def image_dimensions(path: Path) -> tuple[int | None, int | None]:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in {b"GIF87a", b"GIF89a"} and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data.startswith(b"\xff\xd8"):
        offset = 2
        while offset + 9 < len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            marker = data[offset + 1]
            offset += 2
            if marker in {0xD8, 0xD9}:
                continue
            if offset + 2 > len(data):
                break
            length = int.from_bytes(data[offset : offset + 2], "big")
            if marker in range(0xC0, 0xC4) and offset + 7 < len(data):
                height = int.from_bytes(data[offset + 3 : offset + 5], "big")
                width = int.from_bytes(data[offset + 5 : offset + 7], "big")
                return width, height
            offset += max(length, 2)
    if path.suffix.lower() == ".svg":
        text = data.decode("utf-8", errors="ignore")
        viewbox = re.search(r"viewBox=[\"']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)", text)
        if viewbox:
            return round(float(viewbox.group(1))), round(float(viewbox.group(2)))
    return None, None


def css_inventory(repo_root: Path) -> dict[str, Any]:
    source_files = sorted((repo_root / "src").rglob("*.css"))
    built_files = sorted((repo_root / "dist" / "_astro").glob("*.css"))
    owner_counts: Counter[str] = Counter()
    selector_count = 0
    keyframes = 0
    animation_declarations = 0
    source_rows = []
    for path in source_files:
        text = path.read_text(encoding="utf-8")
        clean = CSS_COMMENT_RE.sub("", text)
        file_selectors = 0
        for selector_group, declarations in CSS_BLOCK_RE.findall(clean):
            if selector_group.lstrip().startswith("@"):
                continue
            selectors = [item.strip() for item in selector_group.split(",") if item.strip()]
            file_selectors += len(selectors)
            selector_count += len(selectors)
            for selector in selectors:
                class_match = re.search(r"\.([A-Za-z_][\w-]*)", selector)
                if class_match:
                    token = class_match.group(1)
                    owner = token.split("-")[0]
                elif selector.startswith(":root"):
                    owner = "tokens"
                else:
                    owner = "element_or_at_rule"
                owner_counts[owner] += 1
            animation_declarations += len(re.findall(r"(?:^|[;\s])animation(?:-name)?\s*:", declarations))
        keyframes += len(re.findall(r"@keyframes\s+[-\w]+", clean))
        source_rows.append(
            {
                "path": path.relative_to(repo_root).as_posix(),
                "lines": len(text.splitlines()),
                "bytes": path.stat().st_size,
                "selector_count": file_selectors,
            }
        )
    built_rows = []
    for path in built_files:
        data = path.read_bytes()
        built_rows.append(
            {
                "path": path.relative_to(repo_root).as_posix(),
                "lines": len(data.splitlines()),
                "bytes": len(data),
                "gzip_bytes": len(gzip.compress(data, compresslevel=9)),
            }
        )
    return {
        "source_files": source_rows,
        "source_file_count": len(source_rows),
        "source_lines": sum(row["lines"] for row in source_rows),
        "source_bytes": sum(row["bytes"] for row in source_rows),
        "selector_count": selector_count,
        "selector_owner_prefixes": dict(owner_counts.most_common()),
        "keyframe_count": keyframes,
        "animation_declaration_count": animation_declarations,
        "built_files": built_rows,
        "built_file_count": len(built_rows),
        "built_bytes": sum(row["bytes"] for row in built_rows),
        "built_gzip_bytes": sum(row["gzip_bytes"] for row in built_rows),
    }


def asset_inventory(repo_root: Path) -> list[dict[str, Any]]:
    assets_root = repo_root / "public" / "assets"
    rows = []
    for path in sorted(p for p in assets_root.rglob("*") if p.is_file()):
        width, height = image_dimensions(path)
        rows.append(
            {
                "path": path.relative_to(repo_root / "public").as_posix(),
                "extension": path.suffix.lower(),
                "bytes": path.stat().st_size,
                "width": width,
                "height": height,
            }
        )
    return rows


def quantile(values: list[int], fraction: float) -> float:
    if not values:
        return 0
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return round(ordered[lower] * (1 - weight) + ordered[upper] * weight, 2)


def build_inventory(repo_root: Path) -> dict[str, Any]:
    pages_root = repo_root / "src" / "pages"
    dist_root = repo_root / "dist"
    astro_files = sorted((repo_root / "src").rglob("*.astro"))
    source_files = sorted(
        path for path in pages_root.rglob("*") if path.suffix.lower() in {".astro", ".md", ".mdx"}
    )
    built_files = sorted(dist_root.rglob("index.html"))

    route_map = json.loads((repo_root / "public/files/manifests/page_route_map.json").read_text())
    provenance = json.loads((repo_root / "public/files/manifests/page_provenance.json").read_text())

    page_rows = []
    svg_classifications: Counter[str] = Counter()
    total_svg = total_titles = total_descriptions = total_captions = 0
    total_svg_ids = 0
    total_role_img = total_aria_labelledby = total_aria_label = 0
    total_missing_svg_pairs = 0
    total_filters = total_filter_references = total_motion_hooks = 0
    total_images = remote_images = images_missing_dimensions = 0
    loading_policies: Counter[str] = Counter()
    duplicate_id_pages: list[dict[str, Any]] = []
    table_routes: list[dict[str, Any]] = []
    table_classifications: Counter[str] = Counter()
    gallery_items = 0

    for path in built_files:
        parser = PageInventoryParser()
        parser.feed(path.read_text(encoding="utf-8"))
        route = route_for_html(path, dist_root)
        classifications = Counter(classify_svg(record) for record in parser.svg_records)
        svg_classifications.update(classifications)
        duplicates = sorted(key for key, count in Counter(parser.ids).items() if count > 1)
        if duplicates:
            duplicate_id_pages.append({"route": route, "ids": duplicates})
        if parser.tables:
            records = [
                {**record, "classification_candidate": classify_table(record)}
                for record in parser.table_records
            ]
            table_classifications.update(
                record["classification_candidate"] for record in records
            )
            table_routes.append(
                {"route": route, "table_count": parser.tables, "tables": records}
            )
        total_svg += len(parser.svg_records)
        total_titles += sum(record["title_count"] for record in parser.svg_records)
        total_descriptions += sum(record["description_count"] for record in parser.svg_records)
        total_svg_ids += sum(record["id_count"] for record in parser.svg_records)
        total_role_img += sum(1 for record in parser.svg_records if record["role"] == "img")
        total_aria_labelledby += sum(
            1 for record in parser.svg_records if record["aria_labelledby"]
        )
        total_aria_label += sum(1 for record in parser.svg_records if record["aria_label"])
        total_missing_svg_pairs += sum(
            1
            for record in parser.svg_records
            if not record["title_count"] or not record["description_count"]
        )
        total_captions += parser.figcaptions
        total_filters += parser.filters
        total_filter_references += parser.filter_references
        total_motion_hooks += parser.motion_hook_elements
        total_images += len(parser.images)
        remote_images += sum(1 for item in parser.images if item["remote"])
        images_missing_dimensions += sum(1 for item in parser.images if not item["width"] or not item["height"])
        loading_policies.update(item["loading"] for item in parser.images)
        gallery_items += parser.gallery_items
        page_rows.append(
            {
                "route": route,
                "redirect_document": parser.is_redirect,
                "word_count": len(parser.words),
                "table_count": parser.tables,
                "svg_count": len(parser.svg_records),
                "svg_classifications": dict(classifications),
                "figcaption_count": parser.figcaptions,
                "filter_count": parser.filters,
                "filter_reference_count": parser.filter_references,
                "motion_hook_element_count": parser.motion_hook_elements,
                "image_count": len(parser.images),
                "remote_image_count": sum(1 for item in parser.images if item["remote"]),
                "images_missing_dimensions": sum(
                    1 for item in parser.images if not item["width"] or not item["height"]
                ),
                "document_action_count": parser.action_count,
                "navigation": parser.nav_records,
                "duplicate_ids": duplicates,
            }
        )

    word_counts = [row["word_count"] for row in page_rows]
    assets = asset_inventory(repo_root)
    remote_hosts = Counter()
    for row in page_rows:
        page_path = dist_root / ("index.html" if row["route"] == "/" else row["route"].strip("/") + "/index.html")
        parser = PageInventoryParser()
        parser.feed(page_path.read_text(encoding="utf-8"))
        for image in parser.images:
            if image["remote"]:
                remote_hosts[urlparse(image["src"]).netloc] += 1

    return {
        "schema_version": "0.1",
        "packet_id": "FE-G0-02",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "method": {
            "source_routes": "Files under src/pages with Astro, Markdown, or MDX extensions.",
            "built_pages": "dist/**/index.html after npm run build.",
            "words": "Text tokens in built body markup excluding script, style, noscript, template, and inline SVG text.",
            "svg_classification": "Informational when role img or an accessible label is present; decorative when explicitly aria-hidden or presentation; otherwise unclassified.",
            "motion_hooks": "Elements with native SVG animation tags, data-motion attributes, or class tokens containing motion, animate, orbit, pulse, spin, flow, drift, sweep, or glow.",
            "selector_ownership": "First class-token prefix per selector; element-only selectors are grouped separately.",
            "browser_boundary": "Viewport-dependent and console evidence is recorded in the companion Markdown report, not inferred here.",
        },
        "routes": {
            "source_route_count": len(source_files),
            "source_routes": [route_for_source(path, pages_root) for path in source_files],
            "built_page_count": sum(1 for row in page_rows if not row["redirect_document"]),
            "built_html_document_count": len(built_files),
            "redirect_document_count": sum(1 for row in page_rows if row["redirect_document"]),
            "redirect_routes": [row["route"] for row in page_rows if row["redirect_document"]],
            "active_route_map_count": len(route_map["routes"]),
            "provenance_page_count": len(provenance["pages"]),
            "legacy_source_route_count": sum(
                1 for path in source_files if path.is_relative_to(pages_root / "project")
            ),
        },
        "words": {
            "total": sum(word_counts),
            "minimum": min(word_counts) if word_counts else 0,
            "p25": quantile(word_counts, 0.25),
            "median": statistics.median(word_counts) if word_counts else 0,
            "mean": round(statistics.mean(word_counts), 2) if word_counts else 0,
            "p75": quantile(word_counts, 0.75),
            "maximum": max(word_counts) if word_counts else 0,
        },
        "tables": {
            "total": sum(row["table_count"] for row in page_rows),
            "classification_candidate_counts": dict(table_classifications),
            "routes": table_routes,
        },
        "svg": {
            "inline_instance_count": total_svg,
            "source_inline_svg_artwork_count": sum(
                path.read_text(encoding="utf-8", errors="ignore").count("<svg")
                for path in astro_files
            ),
            "standalone_svg_file_count": len(
                list((repo_root / "src").rglob("*.svg"))
                + list((repo_root / "public").rglob("*.svg"))
            ),
            "source_svg_artwork_count": sum(
                path.read_text(encoding="utf-8", errors="ignore").count("<svg")
                for path in astro_files
            )
            + len(list((repo_root / "src").rglob("*.svg")))
            + len(list((repo_root / "public").rglob("*.svg"))),
            "astro_files_with_inline_svg": sum(
                1
                for path in astro_files
                if "<svg" in path.read_text(encoding="utf-8", errors="ignore")
            ),
            "classification_counts": dict(svg_classifications),
            "role_img_count": total_role_img,
            "aria_labelledby_count": total_aria_labelledby,
            "aria_label_count": total_aria_label,
            "title_count": total_titles,
            "description_count": total_descriptions,
            "missing_complete_title_description_pair_count": total_missing_svg_pairs,
            "figcaption_count": total_captions,
            "svg_id_attribute_count": total_svg_ids,
            "filter_definition_count": total_filters,
            "filter_reference_count": total_filter_references,
            "motion_hook_element_count": total_motion_hooks,
            "duplicate_id_pages": duplicate_id_pages,
        },
        "css": css_inventory(repo_root),
        "images": {
            "rendered_occurrence_count": total_images,
            "remote_occurrence_count": remote_images,
            "remote_hosts": dict(remote_hosts),
            "missing_intrinsic_dimension_occurrence_count": images_missing_dimensions,
            "loading_policy_counts": dict(loading_policies),
            "asset_file_count": len(assets),
            "asset_total_bytes": sum(row["bytes"] for row in assets),
            "assets": assets,
        },
        "gallery": {
            "rendered_item_count": gallery_items,
        },
        "pages": page_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    inventory = build_inventory(repo_root)
    rendered = json.dumps(inventory, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
