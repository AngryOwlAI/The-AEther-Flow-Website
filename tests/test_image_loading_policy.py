from __future__ import annotations

import re
import struct
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IMAGE_METADATA = REPO_ROOT / "src/lib/imageMetadata.ts"
FIGURE = REPO_ROOT / "src/components/Figure.astro"
COMPREHENSION_BLOCKS = REPO_ROOT / "src/components/ComprehensionBlocks.astro"
DIAGRAM_GALLERY = REPO_ROOT / "src/components/DiagramGalleryList.astro"
SITE_CONTENT = REPO_ROOT / "src/lib/siteContent.ts"
COMPREHENSION_ASSETS = REPO_ROOT / "public/assets/diagrams/comprehension"

METADATA_ENTRY = re.compile(
    r'"(?P<path>/assets/diagrams/comprehension/[^\"]+\.png)":\s*'
    r'\{\s*width:\s*(?P<width>\d+),\s*height:\s*(?P<height>\d+)\s*\}',
)


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", data[16:24])


def test_comprehension_png_metadata_matches_every_asset() -> None:
    source = IMAGE_METADATA.read_text(encoding="utf-8")
    entries = {
        match.group("path"): (int(match.group("width")), int(match.group("height")))
        for match in METADATA_ENTRY.finditer(source)
    }
    assets = {
        f"/assets/diagrams/comprehension/{path.name}": png_dimensions(path)
        for path in COMPREHENSION_ASSETS.glob("*.png")
    }

    assert entries == assets
    assert "export interface ImageDimensions" in source
    assert "aspectRatio?: string;" in source
    assert "aspectRatio: dimensions.aspectRatio ?? `${dimensions.width} / ${dimensions.height}`" in source


def test_figure_reserves_geometry_for_primary_and_dialog_images() -> None:
    source = FIGURE.read_text(encoding="utf-8")

    assert 'import { getImageDimensions } from "../lib/imageMetadata";' in source
    assert 'loading = "lazy"' in source
    assert source.count("width={imageDimensions.width}") == 2
    assert source.count("height={imageDimensions.height}") == 2
    assert source.count("aspect-ratio: ${imageDimensions.aspectRatio}") == 2
    assert source.count('decoding="async"') == 2


def test_comprehension_and_gallery_loading_policies_are_explicit() -> None:
    comprehension = COMPREHENSION_BLOCKS.read_text(encoding="utf-8")
    gallery = DIAGRAM_GALLERY.read_text(encoding="utf-8")
    site_content = SITE_CONTENT.read_text(encoding="utf-8")

    assert 'loading?: "lazy" | "eager";' in comprehension
    assert 'const { content, className = "", loading = "lazy" } = Astro.props;' in comprehension
    assert "loading={loading}" in comprehension
    assert 'loading="eager"' not in comprehension

    assert "width: number;" in gallery
    assert "height: number;" in gallery
    assert "aspectRatio: string;" in gallery
    assert "width={item.width}" in gallery
    assert "height={item.height}" in gallery
    assert "aspect-ratio: ${item.aspectRatio}" in gallery
    assert "--diagram-aspect-ratio: ${item.aspectRatio}" in gallery
    assert "aspect-ratio: var(--diagram-aspect-ratio);" in gallery
    assert "max-height: 22rem;" in gallery
    assert "max-height: 18rem;" in gallery
    assert 'loading="lazy"' in gallery
    assert 'decoding="async"' in gallery

    image_link_rule = re.search(
        r"\.diagram-gallery-image-link \{(?P<body>.*?)\n  \}",
        gallery,
        re.DOTALL,
    )
    assert image_link_rule is not None
    assert "width: 100%;" in image_link_rule.group("body")
    assert "max-width: 100%;" in image_link_rule.group("body")
    assert "justify-self: stretch;" in image_link_rule.group("body")
    assert "grid-template-columns: minmax(0, 1fr);" in image_link_rule.group("body")
    assert "grid-template-rows: minmax(0, 1fr);" in image_link_rule.group("body")

    image_rule = re.search(
        r"\.diagram-gallery-image-link img \{(?P<body>.*?)\n  \}",
        gallery,
        re.DOTALL,
    )
    assert image_rule is not None
    assert "width: 100%;" in image_rule.group("body")
    assert "max-width: 100%;" in image_rule.group("body")
    assert "height: 100%;" in image_rule.group("body")
    assert "max-height: 100%;" in image_rule.group("body")
    assert "min-width: 0;" in image_rule.group("body")
    assert "min-height: 0;" in image_rule.group("body")
    assert "object-fit: contain;" in image_rule.group("body")
    assert "object-position: center;" in image_rule.group("body")

    assert 'import { withImageDimensions } from "./imageMetadata";' in site_content
    assert "diagramGallerySourceItems.map(withImageDimensions)" in site_content
