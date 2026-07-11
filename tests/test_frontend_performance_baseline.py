from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "frontend_performance_baseline.py"
SPEC = importlib.util.spec_from_file_location("frontend_performance_baseline", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_summarize_values_uses_median_and_extrema() -> None:
    assert MODULE.summarize_values([7052.8, 1504.2, 1577.3]) == {
        "min": 1504.2,
        "median": 1577.3,
        "max": 7052.8,
    }


def test_checked_in_baseline_has_required_routes_and_runs() -> None:
    baseline = json.loads(
        (ROOT / "docs/quality/frontend-performance-baseline-2026-07-11.json").read_text(
            encoding="utf-8"
        )
    )
    assert baseline["packet_id"] == "FE-G0-03"
    assert set(baseline["routes"]) == set(MODULE.ROUTES)
    assert all(len(route["runs"]) == 3 for route in baseline["routes"].values())
    assert all(
        route["structured_data"]["malformed_blocks"] == 0
        for route in baseline["routes"].values()
    )


def test_budget_evidence_preserves_field_and_lab_boundary() -> None:
    baseline = json.loads(
        (ROOT / "docs/quality/frontend-performance-baseline-2026-07-11.json").read_text(
            encoding="utf-8"
        )
    )
    assert "not field data" in baseline["guidance"]["core_web_vitals"]["qualification"]
    assert baseline["budget_policy"]["status"] == "provisional_baseline_relative"
    assert baseline["cross_route_findings"]["all_routes_zero_tbt"] is True
    assert baseline["cross_route_findings"]["routes_with_lcp_stability_failure"]
