from __future__ import annotations

import refresh_claim_boundary_snapshot as snapshot


def test_active_task_matching_supports_current_recursive_registry_paths() -> None:
    active_task_id = "RT-20260709-006"

    assert snapshot.applies_to_active_task(
        "research_control/tasks/RT-20260709-006/**",
        active_task_id,
    )
    assert snapshot.applies_to_active_task(
        "other/path;research_control/tasks/RT-20260709-006/**;another/path",
        active_task_id,
    )
    assert snapshot.applies_to_active_task(
        "research_control/tasks/RT-20260709-006",
        active_task_id,
    )
    assert not snapshot.applies_to_active_task(
        "research_control/tasks/PREFIX-RT-20260709-006-SUFFIX/**",
        active_task_id,
    )
