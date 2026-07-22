from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

from scripts.implementation_control.plan_goal_adapter import (
    EXPECTED_LOCK_SHA256,
    EXPECTED_SKILLS,
    LOCK_RELATIVE,
    directory_sha256,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path("/Volumes/P-SSD/AngryOwl/skills-Sys4AI")


def run_installer(
    source: Path,
    target: Path,
    *mode: str,
) -> dict:
    completed = subprocess.run(
        [
            str(REPO_ROOT / ".venv/bin/python"),
            str(source / "scripts/skills/install_skills.py"),
            "--root",
            str(source),
            "--bundle",
            "implementation-plan-relay",
            "--target-project",
            str(target),
            "--lock",
            str(source / LOCK_RELATIVE),
            *mode,
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return json.loads(completed.stdout)


def test_exact_release_candidate_install_is_deterministic_and_plugin_free(
    tmp_path: Path,
):
    source = SOURCE_ROOT
    target = tmp_path / "target"
    target.mkdir()
    lock = source / LOCK_RELATIVE
    assert hashlib.sha256(lock.read_bytes()).hexdigest() == EXPECTED_LOCK_SHA256

    dry_run = run_installer(source, target, "--dry-run")
    assert dry_run["status"] == "ready"
    assert len(dry_run["actions"]) == 6
    assert {item["action"] for item in dry_run["actions"]} == {"install"}
    assert dry_run["conflicts"] == []
    assert dry_run["bootstrap_requested"] is False
    assert dry_run["python_install_requested"] is False
    assert dry_run["recommended_plugins"] == []

    applied = run_installer(source, target, "--apply")
    assert applied["status"] == "installed"
    assert applied["validation"]["status"] == "pass"
    assert applied["authority_granted"] is False
    assert applied["bootstrap_requested"] is False
    assert applied["python_install_requested"] is False

    unchanged = run_installer(source, target, "--dry-run")
    assert len(unchanged["actions"]) == 6
    assert {item["action"] for item in unchanged["actions"]} == {
        "unchanged"
    }
    assert unchanged["conflicts"] == []

    for skill_id, (_, expected_hash) in EXPECTED_SKILLS.items():
        skill_root = target / ".agents" / "skills" / skill_id
        assert directory_sha256(skill_root) == expected_hash
        forbidden = [
            item
            for item in skill_root.rglob("*")
            if (
                item.name in {"__pycache__", ".pytest_cache", ".local"}
                or item.suffix in {".pyc", ".pyo"}
            )
        ]
        assert forbidden == []
    assert not (target / ".agents/control").exists()
    assert not any(
        path.name.startswith("plugin")
        for path in (target / ".agents").rglob("*")
    )


def test_tracked_install_matches_exact_package_hashes_and_has_no_cache():
    assert hashlib.sha256(
        (REPO_ROOT / LOCK_RELATIVE).read_bytes()
    ).hexdigest() == EXPECTED_LOCK_SHA256
    for skill_id, (_, expected_hash) in EXPECTED_SKILLS.items():
        root = REPO_ROOT / ".agents" / "skills" / skill_id
        assert directory_sha256(root) == expected_hash
        assert not any(
            item.name in {"__pycache__", ".pytest_cache", ".local"}
            or item.suffix in {".pyc", ".pyo"}
            for item in root.rglob("*")
        )
