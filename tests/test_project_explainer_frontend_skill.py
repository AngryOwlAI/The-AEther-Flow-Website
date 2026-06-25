from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = ROOT / ".codex/skills/project-explainer-frontend/scripts"


def load_script(name: str) -> ModuleType:
    path = SKILL_SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_scan_records_missing_source_root_as_fail_closed(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text(
        "# The AEther Flow Website\n\nReader-facing publication layer.\n",
        encoding="utf-8",
    )
    (repo / "package.json").write_text(
        '{"dependencies":{"astro":"^7.0.0","katex":"^0.17.0"}}',
        encoding="utf-8",
    )
    (repo / "src").mkdir()
    (repo / "src/index.astro").write_text("<h1>The AEther Flow</h1>", encoding="utf-8")

    scan = load_script("scan_project_story")
    brief = scan.create_brief(
        repo,
        tmp_path / "missing-source",
        max_files=50,
        max_evidence=10,
    )

    assert brief.source_root_available is False
    assert "Fail closed" in brief.source_authority_policy
    assert "Astro static site" in brief.likely_frontend_stack


def test_blueprint_defaults_to_astro_and_source_boundary() -> None:
    blueprint_module = load_script("generate_site_blueprint")
    story = {
        "source_root_available": False,
        "source_authority_policy": "Configured upstream source root was unavailable.",
        "project_summary_candidates": ["A static reader-facing presentation layer."],
        "high_value_files": [{"origin": "website", "path": "README.md"}],
    }

    blueprint = blueprint_module.build_blueprint(story, blueprint_module.DEFAULT_IDENTITY)

    assert blueprint["recommended_implementation_target"] == "existing Astro static-site stack"
    assert blueprint["source_root_available"] is False
    assert any("source authority" in item.lower() for item in blueprint["implementation_contract"])


def test_audit_flags_local_path_and_risky_claim(tmp_path: Path) -> None:
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(
        """
        <!doctype html>
        <html>
          <head><meta name="viewport" content="width=device-width" /></head>
          <body>
            <main>
              <h1>The AEther Flow</h1>
              <p>Source authority remains upstream.</p>
              <p>This validated proof lives at /Volumes/P-SSD/AngryOwl/The-AEther-Flow.</p>
            </main>
          </body>
        </html>
        """,
        encoding="utf-8",
    )

    audit = load_script("audit_project_frontend")
    report = audit.audit_site(site)
    messages = [issue.message for issue in report.issues]

    assert report.passed is False
    assert any("Rendered local path leak" in message for message in messages)
    assert any("unsupported runtime or scientific claim" in message for message in messages)
