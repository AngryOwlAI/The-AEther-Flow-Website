from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "frontend_baseline_inventory.py"


def load_inventory_module():
    spec = importlib.util.spec_from_file_location("frontend_baseline_inventory", SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_page_parser_excludes_svg_text_and_records_accessibility_fields() -> None:
    module = load_inventory_module()
    parser = module.PageInventoryParser()
    parser.feed(
        """
        <html><body><main><p>Visible words remain.</p>
        <figure><svg role="img" aria-labelledby="t d"><title id="t">Hidden title</title>
        <desc id="d">Hidden description</desc><filter id="f"></filter>
        <circle class="flow-pulse" filter="url(#f)" /></svg><figcaption>Figure caption.</figcaption></figure>
        <img src="/asset.png" alt="Example" loading="lazy" />
        </main></body></html>
        """
    )

    assert parser.words == ["Visible", "words", "remain", "Figure", "caption"]
    assert len(parser.svg_records) == 1
    assert module.classify_svg(parser.svg_records[0]) == "informational"
    assert parser.svg_records[0]["title_count"] == 1
    assert parser.svg_records[0]["description_count"] == 1
    assert parser.filters == 1
    assert parser.filter_references == 1
    assert parser.figcaptions == 1
    assert parser.images[0]["loading"] == "lazy"


def test_route_mapping_handles_home_and_nested_index() -> None:
    module = load_inventory_module()
    dist = Path("/tmp/dist")
    pages = Path("/tmp/src/pages")

    assert module.route_for_html(dist / "index.html", dist) == "/"
    assert module.route_for_html(dist / "physics/ontology/index.html", dist) == "/physics/ontology/"
    assert module.route_for_source(pages / "index.astro", pages) == "/"
    assert module.route_for_source(pages / "physics/ontology/index.astro", pages) == "/physics/ontology/"


def test_live_inventory_covers_required_static_surfaces() -> None:
    module = load_inventory_module()
    inventory = module.build_inventory(REPO_ROOT)

    assert inventory["packet_id"] == "FE-G0-02"
    assert inventory["routes"]["source_route_count"] == inventory["routes"]["built_page_count"]
    assert inventory["routes"]["built_html_document_count"] >= inventory["routes"]["built_page_count"]
    assert inventory["routes"]["active_route_map_count"] == inventory["routes"]["provenance_page_count"]
    assert inventory["words"]["total"] > 0
    assert inventory["svg"]["inline_instance_count"] > 0
    assert inventory["css"]["source_bytes"] > 0
    assert inventory["images"]["asset_file_count"] > 0
    assert len(inventory["pages"]) == inventory["routes"]["built_html_document_count"]
