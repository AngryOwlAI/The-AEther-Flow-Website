from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GLOBAL_CSS = REPO_ROOT / "src/styles/global.css"
BASE_LAYOUT = REPO_ROOT / "src/layouts/BaseLayout.astro"

EXPECTED_Z_INDEX_TOKENS = {
    "--z-content-raised": "1",
    "--z-overlay-control": "2",
    "--z-skip-link": "10",
    "--z-navigation-panel": "40",
    "--z-site-header": "50",
}

EXPECTED_Z_INDEX_USES = {
    ".skip-link": "--z-skip-link",
    ".site-header": "--z-site-header",
    ".nav-menu-panel": "--z-navigation-panel",
    ".figure-actions": "--z-overlay-control",
    ".figure-dialog-toolbar": "--z-overlay-control",
    ".overview-command-band .command-band-layout": "--z-content-raised",
}


def css_rule(css: str, selector: str) -> str:
    match = re.search(rf"{re.escape(selector)}\s*\{{(?P<body>.*?)\}}", css, re.DOTALL)
    assert match is not None, f"missing CSS rule for {selector}"
    return match.group("body")


def test_root_and_base_layout_advertise_native_dark_color_scheme() -> None:
    css = GLOBAL_CSS.read_text(encoding="utf-8")
    layout = BASE_LAYOUT.read_text(encoding="utf-8")

    assert "color-scheme: dark;" in css_rule(css, ":root")
    assert '<meta name="color-scheme" content="dark" />' in layout
    assert "color-scheme: light" not in css


def test_global_z_index_layers_are_named_and_preserve_existing_values() -> None:
    css = GLOBAL_CSS.read_text(encoding="utf-8")
    root = css_rule(css, ":root")

    for token, value in EXPECTED_Z_INDEX_TOKENS.items():
        assert f"{token}: {value};" in root

    z_index_declarations = re.findall(r"z-index:\s*([^;]+);", css)
    assert len(z_index_declarations) == len(EXPECTED_Z_INDEX_USES)
    assert all(value.startswith("var(--z-") for value in z_index_declarations)
    assert not re.search(r"z-index:\s*-?\d", css)


def test_each_existing_stacking_context_consumes_its_semantic_token() -> None:
    css = GLOBAL_CSS.read_text(encoding="utf-8")

    for selector, token in EXPECTED_Z_INDEX_USES.items():
        assert f"z-index: var({token});" in css_rule(css, selector)

    assert int(EXPECTED_Z_INDEX_TOKENS["--z-skip-link"]) < int(
        EXPECTED_Z_INDEX_TOKENS["--z-site-header"]
    )
