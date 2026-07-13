from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".codex/skills/technical-writing-quality-gate"
SCRIPT = SKILL_ROOT / "scripts/technical_writing_warning_gate.py"


def run_gate(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, SCRIPT.as_posix(), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_package_contract_and_project_boundary() -> None:
    required_files = [
        "SKILL.md",
        "README.md",
        "AGENTS.md",
        "agents/openai.yaml",
        "references/system-writing-quality.md",
        "examples/source-authority-repair.md",
        "scripts/technical_writing_warning_gate.py",
    ]
    for relative_path in required_files:
        assert (SKILL_ROOT / relative_path).is_file()

    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    metadata = (SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    assert skill.startswith("---\nname: technical-writing-quality-gate\n")
    assert "/Volumes/P-SSD/AngryOwl/The-AEther-Flow" in skill
    assert "pass`, `repair`, or `block" in skill
    assert "not proof" in skill
    assert "allow_implicit_invocation: true" in metadata
    assert not (ROOT / ".agents/skills/technical-writing-quality-gate").exists()
    assert not (SKILL_ROOT / "skill.yaml").exists()


def test_help_is_runnable() -> None:
    result = run_gate("--help")
    assert result.returncode == 0
    assert "Files or glob patterns to check" in result.stdout


def test_unicode_clean_input_passes(tmp_path: Path) -> None:
    source = tmp_path / "clean.md"
    source.write_text("The Æther source record defines the current boundary.\n", encoding="utf-8")

    result = run_gate(source.as_posix())

    assert result.returncode == 0
    assert "Gate: `pass`" in result.stdout
    assert "does not prove" in result.stdout


def test_warning_is_advisory_unless_strict(tmp_path: Path) -> None:
    source = tmp_path / "warning.md"
    source.write_text("This seamless platform drives innovation.\n", encoding="utf-8")

    advisory = run_gate(source.as_posix())
    strict = run_gate(source.as_posix(), "--strict")

    assert advisory.returncode == 0
    assert strict.returncode == 1
    assert "Gate: `repair`" in advisory.stdout
    assert "seamless" in advisory.stdout
    assert "drives? innovation" in advisory.stdout


def test_missing_and_invalid_utf8_inputs_block(tmp_path: Path) -> None:
    missing = run_gate((tmp_path / "missing.md").as_posix())
    invalid = tmp_path / "invalid.md"
    invalid.write_bytes(b"\xff\xfe")
    unreadable = run_gate(invalid.as_posix())

    assert missing.returncode == 2
    assert "Gate: `block`" in missing.stdout
    assert unreadable.returncode == 2
    assert "not valid UTF-8 text" in unreadable.stdout


def test_glob_expansion_and_report_generation(tmp_path: Path) -> None:
    (tmp_path / "first.md").write_text("Concrete system behavior.\n", encoding="utf-8")
    (tmp_path / "second.md").write_text("A robust solution.\n", encoding="utf-8")
    report = tmp_path / "reports/gate.md"

    result = run_gate((tmp_path / "*.md").as_posix(), "--report", report.as_posix())

    assert result.returncode == 0
    assert report.is_file()
    content = report.read_text(encoding="utf-8")
    assert "Files checked: 2" in content
    assert "Warning hits: 1" in content
    assert "Gate: `repair`" in content
    assert "does not prove" in content
