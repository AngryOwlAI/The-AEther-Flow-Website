from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BASE_LAYOUT = REPO_ROOT / "src/layouts/BaseLayout.astro"
GLOBAL_CSS = REPO_ROOT / "src/styles/global.css"


def test_mobile_menu_uses_one_controlled_disclosure() -> None:
    layout = BASE_LAYOUT.read_text(encoding="utf-8")

    assert layout.count("data-mobile-nav-trigger") == 2
    assert 'aria-controls="primary-navigation-links"' in layout
    assert 'aria-expanded="false"' in layout
    assert 'id="primary-navigation-links"' in layout
    assert "primaryNavigation.hidden = isCompact && !nextExpanded;" in layout
    assert 'mobileMenuTrigger.setAttribute("aria-expanded", String(nextExpanded));' in layout


def test_mobile_controller_preserves_close_and_resize_contracts() -> None:
    layout = BASE_LAYOUT.read_text(encoding="utf-8")

    assert 'event.key !== "Escape"' in layout
    assert "setMobileMenuExpanded(false, true);" in layout
    assert "!siteNavigation.contains(target)" in layout
    assert "closeMenus(menu);" in layout
    assert 'aria-current={isExactNavPath(child.href) ? "page" : undefined}' in layout
    assert 'compactNavigationQuery.addEventListener("change", syncCompactNavigation);' in layout
    assert "primaryNavigation.contains(document.activeElement)" in layout


def test_compact_navigation_is_viewport_safe_and_has_no_script_routes() -> None:
    layout = BASE_LAYOUT.read_text(encoding="utf-8")
    css = GLOBAL_CSS.read_text(encoding="utf-8")

    assert "<noscript>" in layout
    assert "data-no-script-navigation" in layout
    assert "siteNavigationLinks.filter((link)" in layout
    assert re.search(r"max-height:\s*calc\(100vh - [^)]+\);", css)
    assert re.search(r"max-height:\s*calc\(100dvh - [^)]+\);", css)
    assert "overflow-y: auto;" in css
    assert "overscroll-behavior: contain;" in css
    assert "scrollbar-gutter: stable;" in css
    assert "max-height: max(8rem, calc(100dvh - 10rem));" in css
    assert "(max-height: 480px) and (max-width: 900px)" in css
