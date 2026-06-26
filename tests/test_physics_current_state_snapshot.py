from __future__ import annotations

from pathlib import Path

import refresh_physics_current_state_snapshot as snapshot


def write_fixture_source(root: Path) -> None:
    (root / "research_control/handoffs").mkdir(parents=True)
    (root / "registries").mkdir()
    (root / "research_control/program_state.yaml").write_text(
        "\n".join(
            [
                'mode: "director_led_research_control"',
                'active_task_id: "RT-TEST"',
                'latest_handoff_id: "handoff-0001"',
                'current_status: "draft_control_candidate_pending_selector_no_geff"',
                (
                    'claim_boundary_summary: "No MetricData(E) adoption, no g_eff, '
                    'no matter coupling, no Einstein equations, no benchmark promotion."'
                ),
                'next_recommended_action: "Run one bounded selector packet."',
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "research_control/handoffs/handoff-0001.yaml").write_text(
        "\n".join(
            [
                'handoff_id: "handoff-0001"',
                'created_at: "2026-06-26T00:00:00Z"',
                'task_id: "RT-TEST"',
                'status: "completed"',
                'summary: "Fixture summary."',
                'next_action: "Fixture next action."',
                "distance_to_gr:",
                '  milestone: "effective_metric_g_eff"',
                '  burden_id: "g_eff"',
                '  status: "No MetricData(E) adoption and no g_eff construction"',
                "blocked_claims:",
                '  - "MetricData(E) adoption"',
                '  - "g_eff construction"',
                '  - "matter coupling"',
                '  - "Einstein equations"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "research_control/handoffs/handoff-0001.md").write_text(
        "# Handoff 0001\n\nFixture handoff.\n",
        encoding="utf-8",
    )
    (root / "registries/DISTANCE_TO_GR_LEDGER.csv").write_text(
        "\n".join(
            [
                (
                    "burden_id,milestone,required_object,current_status,blocking_burden,"
                    "accept_criteria,failure_or_freeze_criteria,last_evidence_path,"
                    "updated_at,notes"
                ),
                (
                    "g_eff,effective_metric_g_eff,g_eff,blocked,no MetricData(E),"
                    "metric construction,freeze route,research_control/program_state.yaml,"
                    "2026-06-26T00:00:00Z,no g_eff"
                ),
                (
                    "matter_coupling,matter_coupling,universal coupling,not started,"
                    "response semantics,coupling derivation,freeze route,"
                    "research_control/program_state.yaml,2026-06-26T00:00:00Z,"
                    "no matter coupling"
                ),
                (
                    "einstein_equations,einstein_equations,field equations,not started,"
                    "dynamics,derivation theorem,freeze route,"
                    "research_control/program_state.yaml,2026-06-26T00:00:00Z,"
                    "no Einstein equations"
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "registries/CLAIM_BOUNDARY_REGISTRY.csv").write_text(
        "claim_boundary_id,scope,applies_to_path,allowed_claims,forbidden_claims\n",
        encoding="utf-8",
    )


def walk_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            strings.extend(walk_strings(item))
        return strings
    if isinstance(value, dict):
        strings = []
        for item in value.values():
            strings.extend(walk_strings(item))
        return strings
    return []


def test_snapshot_generation_from_fixture_source(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    write_fixture_source(source_root)

    data = snapshot.build_snapshot(
        source_root=source_root,
        source_commit="a" * 40,
        source_commit_date="2026-06-26T00:00:00Z",
        source_refresh_date="2026-06-26",
        website_publication_date="2026-06-26",
    )

    assert data["active_task_id"] == "RT-TEST"
    assert data["latest_handoff_id"] == "handoff-0001"
    assert data["derivation_burden"]["active_burden_id"] == "g_eff"
    assert {entry["path"] for entry in data["source_dependencies"]} == {
        "research_control/program_state.yaml",
        "research_control/handoffs/handoff-0001.yaml",
        "research_control/handoffs/handoff-0001.md",
        "registries/DISTANCE_TO_GR_LEDGER.csv",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv",
    }


def test_missing_latest_handoff_fails_closed(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    write_fixture_source(source_root)
    (source_root / "research_control/handoffs/handoff-0001.yaml").unlink()

    try:
        snapshot.build_snapshot(source_root=source_root)
    except snapshot.SnapshotError as exc:
        assert "latest handoff YAML is missing" in str(exc)
    else:
        raise AssertionError("missing latest handoff did not fail closed")


def test_missing_required_program_state_field_fails_closed(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    write_fixture_source(source_root)
    program_state = source_root / "research_control/program_state.yaml"
    program_state.write_text(
        program_state.read_text(encoding="utf-8").replace(
            'active_task_id: "RT-TEST"\n',
            "",
        ),
        encoding="utf-8",
    )

    try:
        snapshot.build_snapshot(source_root=source_root)
    except snapshot.SnapshotError as exc:
        assert "active_task_id" in str(exc)
    else:
        raise AssertionError("missing active task did not fail closed")


def test_snapshot_contains_no_absolute_source_paths(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    write_fixture_source(source_root)

    data = snapshot.build_snapshot(
        source_root=source_root,
        source_commit="b" * 40,
        source_commit_date="2026-06-26T00:00:00Z",
    )

    assert str(source_root.resolve()) not in "\n".join(walk_strings(data))


def test_blocked_claim_strings_are_preserved(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    write_fixture_source(source_root)

    data = snapshot.build_snapshot(source_root=source_root)

    assert data["blocked_claims"] == [
        "MetricData(E) adoption",
        "g_eff construction",
        "matter coupling",
        "Einstein equations",
    ]


def test_cli_writes_only_with_explicit_write(tmp_path: Path, capsys) -> None:
    source_root = tmp_path / "source"
    out_path = tmp_path / "snapshot.json"
    write_fixture_source(source_root)

    result = snapshot.main(
        [
            "--source-root",
            str(source_root),
            "--out",
            str(out_path),
            "--source-commit",
            "c" * 40,
        ]
    )

    assert result == 0
    assert not out_path.exists()
    assert '"active_task_id": "RT-TEST"' in capsys.readouterr().out

    result = snapshot.main(
        [
            "--source-root",
            str(source_root),
            "--out",
            str(out_path),
            "--source-commit",
            "c" * 40,
            "--write",
        ]
    )

    assert result == 0
    assert out_path.is_file()
