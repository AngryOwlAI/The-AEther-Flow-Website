from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import run_curator


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_fixture_repo(tmp_path: Path) -> tuple[Path, Path]:
    repo_root = tmp_path / "site"
    source_root = tmp_path / "source"
    (repo_root / "public/files/manifests").mkdir(parents=True)
    (repo_root / "src/data").mkdir(parents=True)
    source_root.mkdir()

    source_text = "source v1\n"
    snapshot_text = "snapshot v1\n"
    asset_text = "asset v1\n"
    (source_root / "source.md").write_text(source_text, encoding="utf-8")
    (source_root / "snapshot.yaml").write_text(snapshot_text, encoding="utf-8")
    (source_root / "asset.tex").write_text(asset_text, encoding="utf-8")

    write_json(
        repo_root / "public/files/manifests/page_route_map.json",
        {
            "version": 1,
            "routes": [
                {
                    "route_path": "/example/",
                    "title": "Example",
                    "upstream_source_paths": ["source.md"],
                }
            ],
        },
    )
    write_json(
        repo_root / "public/files/manifests/page_provenance.json",
        {
            "version": 1,
            "pages": [
                {
                    "route_path": "/example/",
                    "upstream_source_commit": "a" * 40,
                    "upstream_sources": [
                        {
                            "path": "source.md",
                            "sha256": sha256_text(source_text),
                        }
                    ],
                }
            ],
        },
    )
    write_json(
        repo_root / "public/files/manifests/source_manifest.json",
        {
            "version": 1,
            "items": [
                {
                    "id": "asset",
                    "title": "Asset",
                    "source_path": "asset.tex",
                    "source_commit": "a" * 40,
                    "approval_status": "approved",
                    "sha256": sha256_text(asset_text),
                },
                {
                    "id": "sample",
                    "title": "Sample",
                    "source_path": "sample.svg",
                    "approval_status": "sample",
                    "sha256": "0" * 64,
                },
            ],
        },
    )
    write_json(
        repo_root / "src/data/physics_current_state_snapshot.json",
        {
            "source_commit": "a" * 40,
            "source_dependencies": [
                {
                    "path": "snapshot.yaml",
                    "sha256": sha256_text(snapshot_text),
                }
            ],
        },
    )
    return repo_root, source_root


def test_report_generation_is_deterministic_for_unchanged_dependencies(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)

    first = run_curator.build_report(repo_root=repo_root, source_root=source_root)
    second = run_curator.build_report(repo_root=repo_root, source_root=source_root)

    assert run_curator.stable_json(first) == run_curator.stable_json(second)
    assert first["dependency_summary"]["drift_count"] == 0
    assert first["dependency_summary"]["declared_dependency_count"] == 3
    snapshot_dependency = next(
        item
        for item in first["dependencies"]
        if item["dependency_type"] == "current_state_snapshot_source"
    )
    assert snapshot_dependency["route_path"] == "/physics/claim-status/"


def test_parse_args_uses_source_root_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(run_curator.SOURCE_ROOT_ENV_VAR, str(tmp_path))

    args = run_curator.parse_args(["--check"])

    assert args.source_root == tmp_path


def test_parse_args_uses_source_commit_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_commit = "a" * 40
    monkeypatch.setenv(run_curator.SOURCE_COMMIT_ENV_VAR, source_commit)

    args = run_curator.parse_args(["--check"])

    assert args.source_commit == source_commit


def test_explicit_source_commit_argument_overrides_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(run_curator.SOURCE_COMMIT_ENV_VAR, "a" * 40)

    args = run_curator.parse_args(["--source-commit", "b" * 40, "--check"])

    assert args.source_commit == "b" * 40


def test_empty_source_commit_environment_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    monkeypatch.setenv(run_curator.SOURCE_COMMIT_ENV_VAR, "")

    result = run_curator.main(
        [
            "--repo-root",
            str(repo_root),
            "--source-root",
            str(source_root),
            "--check",
        ]
    )

    assert result == 1


def test_changed_declared_dependency_creates_drift_item(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    (source_root / "source.md").write_text("source v2\n", encoding="utf-8")

    report = run_curator.build_report(repo_root=repo_root, source_root=source_root)

    assert report["dependency_summary"]["drift_count"] == 1
    drift = report["drift_items"][0]
    assert drift["route_path"] == "/example/"
    assert drift["source_path"] == "source.md"
    assert drift["old_sha256"] == sha256_text("source v1\n")
    assert drift["new_sha256"] == sha256_text("source v2\n")
    assert drift["severity"] == "review_required"


def test_reports_contain_no_absolute_private_paths(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)

    report = run_curator.build_report(repo_root=repo_root, source_root=source_root)
    rendered = run_curator.stable_json(report) + run_curator.markdown_report(report)

    assert str(repo_root.resolve()) not in rendered
    assert str(source_root.resolve()) not in rendered


def test_check_mode_does_not_write_report_files(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)

    result = run_curator.main(
        [
            "--repo-root",
            str(repo_root),
            "--source-root",
            str(source_root),
            "--check",
        ]
    )

    assert result == 1
    assert not (repo_root / "curator/reports/latest.json").exists()
    assert not (repo_root / "curator/reports/latest.md").exists()


def test_write_mode_updates_only_curator_report_artifacts(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)

    result = run_curator.main(
        [
            "--repo-root",
            str(repo_root),
            "--source-root",
            str(source_root),
            "--write",
        ]
    )

    assert result == 0
    assert (repo_root / "curator/reports/latest.json").is_file()
    assert (repo_root / "curator/reports/latest.md").is_file()
    assert not (repo_root / "public/curator").exists()
