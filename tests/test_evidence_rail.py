from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPONENT = REPO_ROOT / "src/components/EvidenceRail.astro"


def test_linked_cards_use_one_concise_action_link() -> None:
    source = COMPONENT.read_text(encoding="utf-8")

    assert '<article class={`evidence-rail-item ${linkClass}`.trim()}>' in source
    assert '<a class="evidence-rail-item evidence-rail-link"' not in source
    assert source.count('<a class="evidence-rail-action"') == 1
    assert "aria-label={accessibleActionLabel}" in source
    assert 'const accessibleActionLabel = `${actionLabel}: ${item.title}`;' in source


def test_descriptive_content_remains_outside_the_link() -> None:
    source = COMPONENT.read_text(encoding="utf-8")

    heading_position = source.index("<h3>{item.title}</h3>")
    body_position = source.index("<p>{item.body}</p>")
    points_position = source.index("{item.points && item.points.length > 0 && (")
    action_position = source.index('<a class="evidence-rail-action"')

    assert heading_position < body_position < points_position < action_position
    assert source.index("</a>", action_position) < source.index("</article>", action_position)


def test_stretched_action_preserves_visible_focus_context_and_target_size() -> None:
    source = COMPONENT.read_text(encoding="utf-8")

    assert ".evidence-rail-link:focus-within {" in source
    assert "outline: 3px solid var(--color-focus-ring);" in source
    assert ".evidence-rail-action::after {" in source
    assert "inset: 0;" in source
    assert "min-height: 2.75rem;" in source
    assert ".evidence-rail-link-external {" in source
    assert "@media (prefers-reduced-motion: reduce)" in source
