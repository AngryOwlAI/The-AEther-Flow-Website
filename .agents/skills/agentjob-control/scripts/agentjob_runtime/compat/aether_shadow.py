"""Read-only semantic comparison between AEther's legacy and portable resolvers."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.compat.aether_adapter import AetherProjectAdapter
from agentjob_runtime.errors import IntegrityError, RecordValidationError


def _run(
    argv: Sequence[str],
    *,
    cwd: Path,
    timeout_seconds: int,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(argv),
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def capture_git_status(project_root: Path) -> str | None:
    result = _run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=project_root,
        timeout_seconds=30,
    )
    return result.stdout if result.returncode == 0 else None


def capture_git_revision(project_root: Path) -> str | None:
    result = _run(["git", "rev-parse", "HEAD"], cwd=project_root, timeout_seconds=30)
    return result.stdout.strip() if result.returncode == 0 else None


def capture_legacy_resolver(
    project_root: Path,
    *,
    interpreter: Path | None = None,
    timeout_seconds: int = 120,
) -> dict[str, Any]:
    script = project_root / "scripts/research_control/continue_research.py"
    if not script.is_file() or script.is_symlink():
        raise RecordValidationError("AEther legacy resolver script is missing or unsafe")
    selected = interpreter
    if selected is None:
        local_python = project_root / ".venv/bin/python"
        selected = local_python if local_python.is_file() else Path(sys.executable)
    result = _run(
        [str(selected), str(script), "--json"],
        cwd=project_root,
        timeout_seconds=timeout_seconds,
    )
    if result.returncode != 0:
        raise RecordValidationError(
            "AEther legacy resolver failed",
            details={
                "reason_code": "aether.legacy_resolver_failed",
                "exit_code": result.returncode,
                "stderr": result.stderr[-4000:],
            },
        )
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RecordValidationError("AEther legacy resolver did not emit JSON") from error
    if not isinstance(value, dict):
        raise RecordValidationError("AEther legacy resolver output must be an object")
    return value


def _role_identities(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(
        f"{item.get('role_id', '')}@{item.get('version', '')}"
        for item in value
        if isinstance(item, Mapping)
    )


def _job_identities(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(
        f"{item.get('job_id', '')}|{item.get('task_id', '')}|{item.get('decision_id', '')}|{item.get('status', '')}"
        for item in value
        if isinstance(item, Mapping)
    )


def _sorted_strings(value: Any) -> list[str]:
    return sorted(str(item) for item in value) if isinstance(value, list) else []


def _check(
    category: str,
    field: str,
    legacy: Any,
    portable: Any,
    *,
    explanation: str,
) -> dict[str, Any]:
    matches = legacy == portable
    return {
        "category": category,
        "field": field,
        "status": "pass" if matches else "fail",
        "classification": "semantic_parity" if matches else "defect",
        "legacy": legacy,
        "portable": portable,
        "explanation": explanation if matches else "The portable adapter diverges from legacy authority.",
    }


def compare_resolvers(
    legacy: Mapping[str, Any], portable: Mapping[str, Any]
) -> list[dict[str, Any]]:
    legacy_validation_ready = legacy.get("status") == "ready" and not legacy.get(
        "validation_errors", []
    )
    portable_validation_ready = portable.get("status") == "ready" and not portable.get(
        "validation_errors", []
    )
    return [
        _check(
            "routing",
            "boundary",
            legacy.get("boundary"),
            portable.get("boundary"),
            explanation="Both resolvers select the same executable or blocking boundary.",
        ),
        _check(
            "task",
            "active_task_id",
            legacy.get("active_task_id"),
            portable.get("active_task_id"),
            explanation="The tracked program-state task remains the ordinary research authority.",
        ),
        _check(
            "decision",
            "current_decision_id",
            legacy.get("current_decision_id"),
            portable.get("current_decision_id"),
            explanation="The adapter follows the task registry's current decision reference.",
        ),
        _check(
            "job",
            "current_job_id",
            legacy.get("current_job_id"),
            portable.get("current_job_id"),
            explanation="The adapter preserves the current tracked AgentJob identity.",
        ),
        _check(
            "handoff",
            "latest_handoff_id",
            legacy.get("latest_handoff_id"),
            portable.get("latest_handoff_id"),
            explanation="The latest tracked handoff remains continuity evidence, not execution authority.",
        ),
        _check(
            "routing",
            "next_recommended_action",
            legacy.get("next_recommended_action"),
            portable.get("next_recommended_action"),
            explanation="The adapter preserves the tracked next action verbatim.",
        ),
        _check(
            "roles",
            "available_role_identities",
            _role_identities(legacy.get("available_roles")),
            _role_identities(portable.get("available_roles")),
            explanation="Role discovery remains registry-backed and does not grant task permission.",
        ),
        _check(
            "jobs",
            "pending_or_active_jobs",
            _job_identities(legacy.get("pending_or_active_jobs")),
            _job_identities(portable.get("pending_or_active_jobs")),
            explanation="Sidecar jobs remain visible and can block an unrelated canonical route.",
        ),
        _check(
            "paths",
            "required_authority_surfaces",
            _sorted_strings(legacy.get("required_authority_surfaces")),
            _sorted_strings(portable.get("required_authority_surfaces")),
            explanation="Both resolvers require the same tracked authority surfaces.",
        ),
        _check(
            "validators",
            "research_control_ready",
            legacy_validation_ready,
            portable_validation_ready,
            explanation="Both views require successful research-control validation before routing.",
        ),
        _check(
            "gates",
            "stop_conditions",
            _sorted_strings(legacy.get("stop_conditions")),
            _sorted_strings(portable.get("stop_conditions")),
            explanation="Protected authority, validation, role, and path stops are preserved.",
        ),
        _check(
            "checkpoint",
            "required_after_execution",
            legacy.get("checkpoint_required_after_execution"),
            portable.get("checkpoint_provider", {}).get("required_after_execution")
            if isinstance(portable.get("checkpoint_provider"), Mapping)
            else None,
            explanation="Checkpoint obligation is preserved for executable boundaries.",
        ),
        _check(
            "execution",
            "one_job_boundary",
            legacy.get("execution_boundary"),
            portable.get("execution_boundary"),
            explanation="Both runtimes permit at most one bounded AgentJob per invocation.",
        ),
    ]


def run_shadow_comparison(
    project_root: str | Path,
    *,
    legacy_output: Mapping[str, Any] | None = None,
    interpreter: Path | None = None,
    timeout_seconds: int = 120,
) -> dict[str, Any]:
    root = Path(project_root).expanduser().resolve()
    adapter = AetherProjectAdapter(root)
    before_fingerprint = adapter.compute_domain_fingerprint()
    before_status = capture_git_status(root)
    revision = capture_git_revision(root)
    legacy = dict(legacy_output) if legacy_output is not None else capture_legacy_resolver(
        root, interpreter=interpreter, timeout_seconds=timeout_seconds
    )
    portable = adapter.resolve_boundary()
    comparisons = compare_resolvers(legacy, portable)
    after_fingerprint = adapter.compute_domain_fingerprint()
    after_status = capture_git_status(root)
    source_unchanged = (
        before_fingerprint == after_fingerprint and before_status == after_status
    )
    if not source_unchanged:
        raise IntegrityError(
            "AEther source changed during the read-only shadow run",
            details={"reason_code": "aether.shadow_source_mutated"},
        )
    defects = [item for item in comparisons if item["status"] == "fail"]
    return {
        "schema_version": "sys4ai.aether-shadow-comparison.v1",
        "status": "pass" if not defects else "fail",
        "source_revision": revision,
        "source_dirty": bool(before_status),
        "source_unchanged": source_unchanged,
        "source_fingerprint": before_fingerprint,
        "legacy_resolver": {
            "status": legacy.get("status"),
            "boundary": legacy.get("boundary"),
            "execution_performed": False,
        },
        "portable_adapter": {
            "adapter_id": adapter.adapter_id,
            "adapter_version": adapter.version,
            "status": portable.get("status"),
            "boundary": portable.get("boundary"),
            "execution_performed": False,
        },
        "comparison_count": len(comparisons),
        "defect_count": len(defects),
        "comparisons": comparisons,
        "intended_adaptations": [
            {
                "field": "domain_truth",
                "classification": "intended_adaptation",
                "explanation": "The portable adapter states explicitly that process validation does not evaluate scientific truth.",
            },
            {
                "field": "legacy_goal_mutation",
                "classification": "intended_adaptation",
                "explanation": "Historical continue-research-goal.v1 records are reader-only and retain their original IDs and bytes.",
            },
            {
                "field": "activation_model",
                "classification": "intended_adaptation",
                "explanation": "Legacy linkage is mapped for inspection; no synthetic portable activation record is inserted into AEther.",
            },
        ],
        "authority_note": (
            "This report is read-only parity evidence. It does not activate portable skills, "
            "replace AEther validators, promote scientific claims, or authorize shim cutover."
        ),
        "execution_performed": False,
    }


def write_shadow_report(report: Mapping[str, Any], output: str | Path, *, source_root: Path) -> Path:
    path = Path(output).expanduser().resolve()
    if path.is_relative_to(source_root.resolve()):
        raise IntegrityError("shadow reports may not be written into the inspected AEther source")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path
