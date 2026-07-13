from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "src/components/InternalExplainerPage.astro"
OPERATIONS_ROOT = ROOT / "src/pages/project/operations"
PARENT_CHILD_ROUTE = (
    ROOT
    / "src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro"
)


def operations_route_files() -> list[Path]:
    return sorted(
        [OPERATIONS_ROOT / "index.astro", *OPERATIONS_ROOT.glob("*/index.astro")]
    )


def test_exactly_seven_operations_routes_opt_in_to_description_contract() -> None:
    route_files = operations_route_files()

    assert len(route_files) == 7
    for route_file in route_files:
        source = route_file.read_text(encoding="utf-8")
        assert source.count("showDescription") == 1, route_file.relative_to(ROOT)

    assert "showDescription" not in PARENT_CHILD_ROUTE.read_text(encoding="utf-8")


def test_description_follows_complete_hero_and_source_authority_is_terminal() -> None:
    source = COMPONENT.read_text(encoding="utf-8")

    assert "showDescription?: boolean;" in source
    assert re.search(
        r"</section>\s*\{showDescription && \(\s*"
        r'<section[^>]+data-page-section="description"',
        source,
    )

    description = source.index('data-page-section="description"')
    comprehension = source.index("{page.comprehension", description)
    source_authority = source.rindex("<SourceAuthoritySection")
    layout_close = source.rindex("</BaseLayout>")

    assert '<h2 id="internal-explainer-description-title">Description</h2>' in source
    assert "<p>{page.description}</p>" in source
    assert description < comprehension < source_authority < layout_close
    assert "<section" not in source[source_authority:layout_close]
