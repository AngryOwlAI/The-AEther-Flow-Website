from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".codex/skills/mermaid-diagram-style/scripts/apply_mermaid_style.py"


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("apply_mermaid_style", SCRIPT)
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["apply_mermaid_style"] = module
    spec.loader.exec_module(module)
    return module


def test_inserts_frontmatter_and_link_style() -> None:
    style = load_script()
    output = style.format_diagram(
        """flowchart LR
  A["Source file"] --> B["Reader route"]
"""
    )

    assert output.startswith("---\nconfig:\n  theme: base")
    assert 'background: "#000000"' in output
    assert 'fontFamily: "Inter, ui-sans-serif, system-ui' in output
    assert "linkStyle default stroke:#d6c3b4,stroke-width:2.25px;" in output


def test_replaces_legacy_classdefs() -> None:
    style = load_script()
    output = style.format_diagram(
        """flowchart LR
  source["Source"] --> boundary["Forbidden"]

  classDef source fill:#0f172a,stroke:#38bdf8,color:#e0f2fe,stroke-width:2px;
  classDef control fill:#1f2937,stroke:#f59e0b,color:#fff7ed,stroke-width:2px;
  classDef boundary fill:#111827,stroke:#f97316,color:#ffedd5,stroke-width:3px;
  class source source;
  class boundary boundary;
"""
    )

    assert "fill:#0f172a" not in output
    assert "classDef source fill:#0f364d,stroke:#48a0c0" in output
    assert "class source source;" in output
    assert "class boundary boundary;" in output


def test_preserves_node_and_edge_lines() -> None:
    style = load_script()
    source = """flowchart TD
  Alpha["Ontology source laws"] --> Beta{"Gate review"}
  Beta --> Gamma["Candidate bridge"]
"""
    output = style.format_diagram(source)

    assert 'Alpha["Ontology source laws"] --> Beta{"Gate review"}' in output
    assert 'Beta --> Gamma["Candidate bridge"]' in output


def test_adds_semantic_classes_to_unclassified_nodes() -> None:
    style = load_script()
    output = style.format_diagram(
        """flowchart LR
  Source["Source manifest"] --> Review{"Gate review"}
  Review --> Boundary["Forbidden: source authority replaced"]
"""
    )

    assert "class Source source;" in output
    assert "class Review decision;" in output
    assert "class Boundary boundary;" in output


def test_fails_closed_for_unsupported_input() -> None:
    style = load_script()

    try:
        style.format_diagram("sequenceDiagram\n  Alice->>Bob: Hello\n")
    except ValueError as exc:
        assert "missing supported flowchart or graph declaration" in str(exc)
    else:
        raise AssertionError("unsupported Mermaid input should fail closed")
