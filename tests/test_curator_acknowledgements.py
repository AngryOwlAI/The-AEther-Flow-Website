from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest
import run_curator
from test_curator_reports import sha256_text, write_fixture_repo


@pytest.fixture(autouse=True)
def clear_source_commit_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(run_curator.SOURCE_COMMIT_ENV_VAR, raising=False)


def init_source_git(source_root: Path) -> str:
    subprocess.run(["git", "init"], cwd=source_root, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "curator-test@example.com"],
        cwd=source_root,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Curator Test"],
        cwd=source_root,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=source_root, check=True)
    env = {
        **os.environ,
        "GIT_AUTHOR_DATE": "2026-06-26T00:00:00Z",
        "GIT_COMMITTER_DATE": "2026-06-26T00:00:00Z",
    }
    subprocess.run(
        ["git", "commit", "-m", "fixture"],
        cwd=source_root,
        check=True,
        env=env,
        capture_output=True,
    )
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def commit_source_changes(source_root: Path, message: str) -> str:
    subprocess.run(["git", "add", "."], cwd=source_root, check=True)
    env = {
        **os.environ,
        "GIT_AUTHOR_DATE": "2026-06-26T00:01:00Z",
        "GIT_COMMITTER_DATE": "2026-06-26T00:01:00Z",
    }
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=source_root,
        check=True,
        env=env,
        capture_output=True,
    )
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def write_ack(
    repo_root: Path,
    *,
    route_path: str = "/example/",
    source_path: str = "source.md",
    severity: str = "review_required",
    current_commit: str,
    current_sha256: str,
) -> Path:
    ack_dir = repo_root / "curator/acknowledgements"
    ack_dir.mkdir(parents=True, exist_ok=True)
    ack_path = ack_dir / "fixture.yaml"
    ack_path.write_text(
        "\n".join(
            [
                f'route_path: "{route_path}"',
                f'source_path: "{source_path}"',
                f'severity: "{severity}"',
                f'current_commit: "{current_commit}"',
                f'current_sha256: "{current_sha256}"',
                'acknowledged_by: "project owner"',
                'acknowledged_at: "2026-06-26T00:00:00Z"',
                'reason: "Reviewed as fixture drift."',
                "expires_at: null",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return ack_path


def write_reports(
    repo_root: Path,
    source_root: Path,
    *,
    source_commit: str | None = None,
) -> int:
    arguments = [
        "--repo-root",
        str(repo_root),
        "--source-root",
        str(source_root),
    ]
    if source_commit is not None:
        arguments.extend(["--source-commit", source_commit])
    arguments.append("--write")
    return run_curator.main(arguments)


def check_reports(
    repo_root: Path,
    source_root: Path,
    *,
    source_commit: str | None = None,
) -> int:
    arguments = [
        "--repo-root",
        str(repo_root),
        "--source-root",
        str(source_root),
    ]
    if source_commit is not None:
        arguments.extend(["--source-commit", source_commit])
    arguments.append("--check")
    return run_curator.main(arguments)


def test_critical_drift_fails_even_with_acknowledgement(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    init_source_git(source_root)
    (source_root / "snapshot.yaml").write_text("snapshot v2\n", encoding="utf-8")
    current_commit = commit_source_changes(source_root, "critical drift")

    assert write_reports(repo_root, source_root) == 0
    write_ack(
        repo_root,
        route_path=run_curator.CURRENT_STATE_ROUTE,
        source_path="snapshot.yaml",
        severity="critical",
        current_commit=current_commit,
        current_sha256=sha256_text("snapshot v2\n"),
    )

    assert check_reports(repo_root, source_root) == 1


def test_review_required_drift_fails_without_acknowledgement(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    init_source_git(source_root)
    (source_root / "source.md").write_text("source v2\n", encoding="utf-8")
    commit_source_changes(source_root, "review-required drift")

    assert write_reports(repo_root, source_root) == 0

    assert check_reports(repo_root, source_root) == 1


def test_review_required_drift_passes_with_exact_acknowledgement(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    init_source_git(source_root)
    (source_root / "source.md").write_text("source v2\n", encoding="utf-8")
    current_commit = commit_source_changes(source_root, "acknowledged drift")
    write_ack(
        repo_root,
        current_commit=current_commit,
        current_sha256=sha256_text("source v2\n"),
    )

    assert write_reports(repo_root, source_root) == 0
    assert check_reports(repo_root, source_root) == 0


def test_pinned_source_commit_is_stable_after_head_advances(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    init_source_git(source_root)
    (source_root / "source.md").write_text("source v2\n", encoding="utf-8")
    reviewed_commit = commit_source_changes(source_root, "reviewed drift")
    write_ack(
        repo_root,
        current_commit=reviewed_commit,
        current_sha256=sha256_text("source v2\n"),
    )

    assert write_reports(repo_root, source_root, source_commit=reviewed_commit) == 0
    report_path = repo_root / "curator/reports/latest.json"
    markdown_path = repo_root / "curator/reports/latest.md"
    report_before = report_path.read_bytes()
    markdown_before = markdown_path.read_bytes()

    (source_root / "source.md").write_text("source v3\n", encoding="utf-8")
    advanced_commit = commit_source_changes(source_root, "later unreviewed drift")

    assert advanced_commit != reviewed_commit
    assert check_reports(repo_root, source_root) == 1
    assert check_reports(repo_root, source_root, source_commit=reviewed_commit) == 0
    assert report_path.read_bytes() == report_before
    assert markdown_path.read_bytes() == markdown_before

    report = json.loads(report_before)
    assert report["current_commit"] == reviewed_commit
    assert report["current_commit_date"] == run_curator.git_output(
        source_root,
        "show",
        "-s",
        "--format=%cI",
        reviewed_commit,
    )
    assert report["acknowledgement_summary"]["matched_acknowledgement_count"] == 1


def test_explicit_source_commit_rejects_invalid_missing_and_noncommit_pins(
    tmp_path: Path,
) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    init_source_git(source_root)
    blob_commit = subprocess.run(
        ["git", "hash-object", "-w", "--stdin"],
        cwd=source_root,
        check=True,
        capture_output=True,
        input=b"not a commit\n",
    ).stdout.decode("utf-8").strip()

    for source_commit in ("not-a-commit", "f" * 40, blob_commit):
        result = run_curator.main(
            [
                "--repo-root",
                str(repo_root),
                "--source-root",
                str(source_root),
                "--source-commit",
                source_commit,
                "--check",
            ]
        )

        assert result == 1


def test_informational_drift_does_not_fail_validation(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    missing_source_root = source_root.parent / "missing-source"

    assert write_reports(repo_root, missing_source_root) == 0
    assert check_reports(repo_root, missing_source_root) == 0


def test_malformed_acknowledgement_fails_closed(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    (repo_root / "curator/acknowledgements").mkdir(parents=True)
    (repo_root / "curator/acknowledgements/bad.yaml").write_text(
        'route_path: "/example/"\n',
        encoding="utf-8",
    )

    assert write_reports(repo_root, source_root) == 1


def test_stale_acknowledgement_fails_closed(tmp_path: Path) -> None:
    repo_root, source_root = write_fixture_repo(tmp_path)
    init_source_git(source_root)
    (source_root / "source.md").write_text("source v2\n", encoding="utf-8")
    current_commit = commit_source_changes(source_root, "stale acknowledged drift")
    write_ack(
        repo_root,
        current_commit=current_commit,
        current_sha256=sha256_text("stale\n"),
    )

    assert write_reports(repo_root, source_root) == 1
