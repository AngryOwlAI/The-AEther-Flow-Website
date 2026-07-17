#!/usr/bin/env python3
"""Website-native adapter for the vendored governed-continuation runtime.

This module maps the website's existing ``implementation_control/`` records
into portable continue results and activation receipts. It never creates or
uses ``.agents/control`` and it never executes an implementation job itself.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
VENDOR_RUNTIME_SCRIPTS = (
    REPO_ROOT / ".agents" / "skills" / "agentjob-control" / "scripts"
)
for import_root in (SCRIPTS_ROOT, VENDOR_RUNTIME_SCRIPTS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from implementation_control.continue_implementation import (  # noqa: E402
    load_yaml,
    resolve_continue_context,
)

try:  # noqa: E402
    from agentjob_runtime.records.canonical import content_sha256
except ImportError:  # The integrity validator reports a clearer install failure.
    content_sha256 = None  # type: ignore[assignment]


CONTINUE_RESULT_SCHEMA = "sys4ai.continue-result.v1"
ACTIVATION_SCHEMA = "sys4ai.website-goal-activation.v1"
ADAPTER_EXTENSION = "website_implementation_control"
LOCAL_STATE_RELATIVE = Path(".local/sys4ai/continuation")
EXCLUDED_FINGERPRINT_PREFIXES = (
    ".local/sys4ai/continuation",
    ".local/sys4ai/install-transactions",
)
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,159}$")


class GoalRelayAdapterError(RuntimeError):
    """Raised when website evidence cannot be mapped without weakening policy."""


@dataclass(frozen=True)
class WebsiteSnapshot:
    """Canonical website control and Git evidence at one instant."""

    repo_root: Path
    resolver: dict[str, Any]
    resolver_exit_code: int
    git: dict[str, Any]
    record_paths: dict[str, str | None]
    record_hashes: dict[str, str]
    record_metadata: dict[str, dict[str, Any]]
    fingerprint: str
    source_authority: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "resolver": self.resolver,
            "resolver_exit_code": self.resolver_exit_code,
            "git": self.git,
            "record_paths": self.record_paths,
            "record_hashes": self.record_hashes,
            "record_metadata": self.record_metadata,
            "fingerprint": self.fingerprint,
            "source_authority": self.source_authority,
        }


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def stable_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    if content_sha256 is not None:
        return str(content_sha256(value))
    return hashlib.sha256(stable_json_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_git(repo_root: Path, *args: str, allow_failure: bool = False) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0 and not allow_failure:
        details = (completed.stderr or completed.stdout).strip()
        raise GoalRelayAdapterError(f"git {' '.join(args)} failed: {details}")
    return completed.stdout.strip()


def _status_path(raw_line: str) -> str:
    value = raw_line[3:] if len(raw_line) >= 4 else raw_line
    return value.rsplit(" -> ", 1)[-1]


def git_evidence(repo_root: Path) -> dict[str, Any]:
    root = repo_root.resolve()
    status_lines = _run_git(root, "status", "--porcelain=v1", "-uall").splitlines()
    retained_status = []
    for line in status_lines:
        path = _status_path(line)
        if any(
            path == prefix or path.startswith(f"{prefix}/")
            for prefix in EXCLUDED_FINGERPRINT_PREFIXES
        ):
            continue
        retained_status.append(line)
    branch = _run_git(root, "branch", "--show-current", allow_failure=True) or None
    common_dir_raw = _run_git(root, "rev-parse", "--git-common-dir")
    common_dir = Path(common_dir_raw)
    if not common_dir.is_absolute():
        common_dir = (root / common_dir).resolve()
    return {
        "project_root": str(root),
        "worktree": _run_git(root, "rev-parse", "--show-toplevel"),
        "git_common_dir": str(common_dir),
        "head": _run_git(root, "rev-parse", "HEAD"),
        "branch": branch,
        "status": sorted(retained_status),
    }


def _pointer_path(value: Any) -> str | None:
    if isinstance(value, str) and value:
        return value
    if isinstance(value, Mapping):
        for key in ("path", "yaml_path", "completion_path"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate:
                return candidate
    return None


def _safe_record_path(repo_root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise GoalRelayAdapterError(f"control pointer escapes repository: {value}")
    resolved = (repo_root / candidate).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as error:
        raise GoalRelayAdapterError(f"control pointer escapes repository: {value}") from error
    return resolved


def active_record_paths(
    repo_root: Path,
    resolver: Mapping[str, Any],
) -> dict[str, str | None]:
    program_relative = "implementation_control/program_state.yaml"
    program = load_yaml(repo_root / program_relative)
    task_relative = str(resolver.get("active_task", {}).get("path") or "") or None
    job_relative = str(resolver.get("current_job", {}).get("path") or "") or None
    handoff_relative = (
        str(resolver.get("latest_handoff", {}).get("yaml_path") or "") or None
    )
    handoff_markdown = (
        str(resolver.get("latest_handoff", {}).get("markdown_path") or "") or None
    )
    records: list[dict[str, Any]] = []
    for value in (job_relative, task_relative, handoff_relative):
        path = _safe_record_path(repo_root, value)
        if path and path.is_file():
            records.append(load_yaml(path))
    records.append(program)
    active_task_id = resolver.get("active_task", {}).get("task_id")
    active_job_id = resolver.get("current_job", {}).get("job_id")
    completion_relative = None
    for record in records:
        for key in ("latest_completion", "completion_record"):
            candidate = _pointer_path(record.get(key))
            candidate_path = _safe_record_path(repo_root, candidate)
            if candidate_path is None or not candidate_path.is_file():
                continue
            completion = load_yaml(candidate_path)
            if (
                active_task_id
                and completion.get("task_id") != active_task_id
            ) or (
                active_job_id
                and completion.get("job_id") != active_job_id
            ):
                continue
            completion_relative = candidate
            if completion_relative:
                break
        if completion_relative:
            break
    return {
        "program_state": program_relative,
        "task": task_relative,
        "job": job_relative,
        "handoff": handoff_relative,
        "handoff_markdown": handoff_markdown,
        "completion": completion_relative,
    }


def record_evidence(
    repo_root: Path,
    record_paths: Mapping[str, str | None],
) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    hashes: dict[str, str] = {}
    metadata: dict[str, dict[str, Any]] = {}
    id_fields = {
        "program_state": None,
        "task": "task_id",
        "job": "job_id",
        "handoff": "handoff_id",
        "completion": "completion_id",
    }
    for kind, id_field in id_fields.items():
        relative = record_paths.get(kind)
        path = _safe_record_path(repo_root, relative)
        if path is None or not path.is_file():
            continue
        hashes[kind] = file_sha256(path)
        record = load_yaml(path)
        metadata[kind] = {
            "path": str(relative),
            "record_id": (
                str(record.get(id_field)) if id_field and record.get(id_field) else None
            ),
            "record_type": record.get("record_type"),
            "status": record.get("status"),
        }
    markdown_relative = record_paths.get("handoff_markdown")
    markdown_path = _safe_record_path(repo_root, markdown_relative)
    if markdown_path and markdown_path.is_file():
        hashes["handoff_markdown"] = file_sha256(markdown_path)
        metadata["handoff_markdown"] = {
            "path": str(markdown_relative),
            "record_id": None,
            "record_type": "implementation_handoff_markdown",
            "status": None,
        }
    return hashes, metadata


def fingerprint_payload(
    *,
    git: Mapping[str, Any],
    resolver: Mapping[str, Any],
    record_paths: Mapping[str, str | None],
    record_hashes: Mapping[str, str],
) -> dict[str, Any]:
    """Return the relay-state-independent canonical project payload."""

    return {
        "schema_version": "sys4ai.website-project-fingerprint.v1",
        "git": dict(git),
        "control": {
            "record_paths": dict(record_paths),
            "record_hashes": dict(record_hashes),
            "status": resolver.get("status"),
            "active_task": resolver.get("active_task"),
            "current_job": resolver.get("current_job"),
            "latest_handoff": resolver.get("latest_handoff"),
            "allowed_paths": resolver.get("allowed_paths"),
            "approval_gates": resolver.get("approval_gates"),
            "boundary": resolver.get("boundary"),
            "checkpoint": resolver.get("checkpoint"),
            "required_validators": resolver.get("required_validators"),
            "stop_conditions": resolver.get("stop_conditions"),
            "next_recommended_action": resolver.get("next_recommended_action"),
        },
    }


def compute_canonical_fingerprint(
    repo_root: Path,
    *,
    resolver: Mapping[str, Any],
    record_paths: Mapping[str, str | None],
) -> tuple[str, dict[str, Any], dict[str, str]]:
    git = git_evidence(repo_root)
    hashes, _ = record_evidence(repo_root, record_paths)
    payload = fingerprint_payload(
        git=git,
        resolver=resolver,
        record_paths=record_paths,
        record_hashes=hashes,
    )
    return canonical_sha256(payload), git, hashes


def _source_authority(
    resolver: Mapping[str, Any],
    metadata: Mapping[str, Mapping[str, Any]],
    repo_root: Path,
) -> dict[str, Any]:
    task_path = metadata.get("task", {}).get("path")
    handoff_path = metadata.get("handoff", {}).get("path")
    task = load_yaml(repo_root / str(task_path)) if task_path else {}
    handoff = load_yaml(repo_root / str(handoff_path)) if handoff_path else {}
    return {
        "boundary": resolver.get("boundary", {}),
        "task_source_context": task.get("source_context", {}),
        "handoff_source_authority_boundary": handoff.get(
            "source_authority_boundary", {}
        ),
    }


def capture_snapshot(repo_root: Path = REPO_ROOT) -> WebsiteSnapshot:
    root = repo_root.resolve()
    resolver, exit_code = resolve_continue_context(root)
    paths = active_record_paths(root, resolver)
    fingerprint, git, hashes = compute_canonical_fingerprint(
        root,
        resolver=resolver,
        record_paths=paths,
    )
    _, metadata = record_evidence(root, paths)
    return WebsiteSnapshot(
        repo_root=root,
        resolver=dict(resolver),
        resolver_exit_code=exit_code,
        git=git,
        record_paths=paths,
        record_hashes=hashes,
        record_metadata=metadata,
        fingerprint=fingerprint,
        source_authority=_source_authority(resolver, metadata, root),
    )


def repository_binding(snapshot: WebsiteSnapshot) -> dict[str, Any]:
    return {
        "project_id": "The-AEther-Flow-Website",
        "root": str(snapshot.repo_root),
        "worktree": str(snapshot.repo_root),
        "branch": snapshot.git["branch"],
        "git_common_dir": snapshot.git["git_common_dir"],
        "starting_revision": snapshot.git["head"],
        "environment_mode": "local",
    }


def checkpoint_is_authorized(snapshot: WebsiteSnapshot) -> bool:
    checkpoint = snapshot.resolver.get("checkpoint")
    return bool(
        isinstance(checkpoint, Mapping)
        and checkpoint.get("staging_allowed_by_this_job") is True
    )


def pre_execution_block(snapshot: WebsiteSnapshot) -> tuple[str | None, str | None]:
    status = str(snapshot.resolver.get("status", "blocked"))
    if status == "approval_required":
        return "human_gate_required", "website.approval_required"
    if status == "ready" and not checkpoint_is_authorized(snapshot):
        return "human_gate_required", "website.checkpoint_authority_required"
    if status == "no_action":
        return "no_action", "website.no_action"
    if status != "ready" or snapshot.resolver_exit_code != 0:
        return "control_repair_required", "website.control_repair_required"
    return None, None


def activation_receipt_payload(
    snapshot: WebsiteSnapshot,
    *,
    goal_id: str,
    generation: int,
    envelope_sha256: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    if not SAFE_ID.fullmatch(goal_id):
        raise GoalRelayAdapterError("unsafe goal ID for activation receipt")
    return {
        "schema_version": ACTIVATION_SCHEMA,
        "activation_id": f"WGA-{goal_id}-{generation}",
        "goal_id": goal_id,
        "generation": generation,
        "envelope_sha256": envelope_sha256,
        "created_at": created_at or utc_now(),
        "canonical_fingerprint": snapshot.fingerprint,
        "git_binding": snapshot.git,
        "active_records": [
            {
                "kind": kind,
                **metadata,
                "sha256": snapshot.record_hashes.get(kind),
            }
            for kind, metadata in sorted(snapshot.record_metadata.items())
        ],
        "resolver_status": snapshot.resolver.get("status"),
        "checkpoint": snapshot.resolver.get("checkpoint"),
        "source_authority": snapshot.source_authority,
    }


def _require_regular_file(path: Path) -> None:
    if path.is_symlink():
        raise GoalRelayAdapterError(f"protected relay artifact is a symlink: {path}")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise GoalRelayAdapterError(f"protected relay artifact has an unsafe alias: {path}")


def write_protected_json(path: Path, value: Mapping[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise GoalRelayAdapterError(f"append-only relay artifact already exists: {path}")
    payload = json.dumps(value, indent=2, sort_keys=True) + "\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        if path.exists():
            path.unlink()
        raise
    return path


def read_protected_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise GoalRelayAdapterError(f"protected relay artifact is missing: {path}")
    _require_regular_file(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GoalRelayAdapterError(f"protected relay artifact must be an object: {path}")
    return value


def activation_receipt_path(
    repo_root: Path,
    *,
    goal_id: str,
    generation: int,
) -> Path:
    if not SAFE_ID.fullmatch(goal_id):
        raise GoalRelayAdapterError("unsafe goal ID for activation path")
    return (
        repo_root
        / LOCAL_STATE_RELATIVE
        / "activations"
        / goal_id
        / f"generation-{generation}.json"
    )


def write_activation_receipt(
    snapshot: WebsiteSnapshot,
    *,
    goal_id: str,
    generation: int,
    envelope_sha256: str,
) -> Path:
    path = activation_receipt_path(
        snapshot.repo_root,
        goal_id=goal_id,
        generation=generation,
    )
    return write_protected_json(
        path,
        activation_receipt_payload(
            snapshot,
            goal_id=goal_id,
            generation=generation,
            envelope_sha256=envelope_sha256,
        ),
    )


def verify_activation_receipt(
    snapshot: WebsiteSnapshot,
    receipt: Mapping[str, Any],
) -> None:
    expected = activation_receipt_payload(
        snapshot,
        goal_id=str(receipt.get("goal_id")),
        generation=int(receipt.get("generation", 0)),
        envelope_sha256=str(receipt.get("envelope_sha256")),
        created_at=str(receipt.get("created_at")),
    )
    if dict(receipt) != expected:
        raise GoalRelayAdapterError(
            "pre-execution Git or active control evidence differs from activation receipt"
        )


def _completion_record(snapshot: WebsiteSnapshot) -> dict[str, Any]:
    relative = snapshot.record_paths.get("completion")
    path = _safe_record_path(snapshot.repo_root, relative)
    return load_yaml(path) if path and path.is_file() else {}


def _validator_counts(
    snapshot: WebsiteSnapshot,
    completion: Mapping[str, Any],
) -> dict[str, int]:
    counts = {
        "required": len(snapshot.resolver.get("required_validators", [])),
        "passed": 0,
        "failed": 0,
        "warning": 0,
        "skipped": 0,
    }
    for item in completion.get("validator_results", []):
        if not isinstance(item, Mapping):
            continue
        status = str(item.get("status", "")).lower()
        if status in {"pass", "passed", "complete", "completed"}:
            counts["passed"] += 1
        elif status in {"fail", "failed", "error", "blocked"}:
            counts["failed"] += 1
        elif status in {"warning", "warn", "indeterminate"}:
            counts["warning"] += 1
        elif status in {"skip", "skipped", "not_run", "not-run"}:
            counts["skipped"] += 1
    return counts


def checkpoint_evidence(snapshot: WebsiteSnapshot) -> dict[str, Any]:
    completion_id = snapshot.record_metadata.get("completion", {}).get("record_id")
    job_id = snapshot.record_metadata.get("job", {}).get("record_id")
    completion_path = snapshot.record_paths.get("completion")
    if not completion_id or not job_id or not completion_path:
        return {
            "provider": "website-checkpoint",
            "status": "unknown",
            "revision": None,
            "evidence_ref": None,
        }
    message = _run_git(snapshot.repo_root, "show", "-s", "--format=%B", "HEAD")
    paths = set(
        _run_git(
            snapshot.repo_root,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ).splitlines()
    )
    passed = (
        f"Job: {job_id}" in message
        and f"Completion: {completion_id}" in message
        and completion_path in paths
    )
    return {
        "provider": "website-checkpoint",
        "status": "pass" if passed else "unknown",
        "revision": snapshot.git["head"] if passed else None,
        "evidence_ref": completion_path if passed else None,
    }


def _portable_extension(
    before: WebsiteSnapshot,
    after: WebsiteSnapshot,
    *,
    checkpoint: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        ADAPTER_EXTENSION: {
            "version": "0.1.0",
            "required": True,
            "data": {
                "implementation_authority": "implementation_control",
                "task_id": after.record_metadata.get("task", {}).get("record_id"),
                "job_id": after.record_metadata.get("job", {}).get("record_id"),
                "completion_id": after.record_metadata.get("completion", {}).get(
                    "record_id"
                ),
                "handoff_id": after.record_metadata.get("handoff", {}).get(
                    "record_id"
                ),
                "before_git": before.git,
                "after_git": after.git,
                "before_record_hashes": before.record_hashes,
                "after_record_hashes": after.record_hashes,
                "allowed_paths": before.resolver.get("allowed_paths"),
                "approval_gates": before.resolver.get("approval_gates"),
                "checkpoint": dict(checkpoint),
                "source_authority": after.source_authority,
            },
        }
    }


def execution_boundary_matches(
    before: WebsiteSnapshot,
    after: WebsiteSnapshot,
) -> bool:
    """Return whether final evidence still describes the one activated job."""

    repository_fields = ("project_root", "worktree", "git_common_dir", "branch")
    if any(before.git.get(key) != after.git.get(key) for key in repository_fields):
        return False
    for kind in ("task", "job"):
        before_id = before.record_metadata.get(kind, {}).get("record_id")
        after_id = after.record_metadata.get(kind, {}).get("record_id")
        if before_id != after_id:
            return False
    return True


def build_continue_result(
    before: WebsiteSnapshot,
    after: WebsiteSnapshot | None = None,
    *,
    execution_attempted: bool = False,
) -> dict[str, Any]:
    """Map direct website evidence into one portable continue result."""

    final = after or before
    completion = _completion_record(final)
    checkpoint = checkpoint_evidence(final)
    blocked_status, blocked_reason = pre_execution_block(before)
    task_id = final.record_metadata.get("task", {}).get("record_id")
    job_id = final.record_metadata.get("job", {}).get("record_id")
    completion_id = final.record_metadata.get("completion", {}).get("record_id")
    handoff_id = final.record_metadata.get("handoff", {}).get("record_id")

    if blocked_status:
        status = blocked_status
        boundary = (
            "human_gate_required"
            if blocked_status == "human_gate_required"
            else "no_action"
            if blocked_status == "no_action"
            else "control_repair_required"
        )
        jobs: int | str = 0
        progress = "blocked_evidence" if status != "no_action" else "none"
        performed = False
        reason = str(blocked_reason)
    elif not execution_attempted:
        status = "no_action"
        boundary = "existing_agent_job_ready"
        jobs = 0
        progress = "none"
        performed = False
        reason = "website.execution_not_attempted"
    elif not execution_boundary_matches(before, final):
        status = "unknown"
        boundary = "control_repair_required"
        jobs = "unknown"
        progress = "unknown"
        performed = True
        reason = "website.active_boundary_changed"
    elif completion_id and checkpoint["status"] == "pass":
        status = "completed"
        boundary = "existing_agent_job_ready"
        jobs = 1
        progress = "bounded_completion"
        performed = True
        reason = "website.job_completed_and_checkpointed"
    elif completion_id and not checkpoint_is_authorized(before):
        status = "human_gate_required"
        boundary = "human_gate_required"
        jobs = 1
        progress = "bounded_progress"
        performed = True
        reason = "website.checkpoint_authority_required"
    else:
        status = "unknown"
        boundary = "existing_agent_job_ready"
        jobs = "unknown"
        progress = "unknown"
        performed = True
        reason = "website.completion_contract_not_proven"

    next_action = final.resolver.get("next_recommended_action", {}).get("summary")
    return {
        "schema_version": CONTINUE_RESULT_SCHEMA,
        "status": status,
        "boundary_entered": boundary,
        "agent_jobs_executed": jobs,
        "task_id": task_id,
        "decision_id": None,
        "job_id": job_id,
        "completion_id": completion_id,
        "handoff_id": handoff_id,
        "progress_effect": progress,
        "global_goal_evaluation": "not_evaluated_here",
        "repository_fingerprint_before": before.fingerprint,
        "repository_fingerprint_after": final.fingerprint,
        "validators": _validator_counts(final, completion),
        "next_recommended_action": str(next_action) if next_action else None,
        "execution_performed": performed,
        "reason_code": reason,
        "extensions": _portable_extension(before, final, checkpoint=checkpoint),
    }


def _validator_class(validator_id: str) -> str:
    value = validator_id.lower()
    if "claim" in value or "source" in value or "provenance" in value:
        return "claim_validation"
    if "control" in value or "relay" in value:
        return "control_validation"
    if "path" in value or "diff" in value:
        return "path_validation"
    return "process_validation"


def build_direct_evidence(
    result: Mapping[str, Any],
    snapshot: WebsiteSnapshot,
    *,
    completion_contract_results: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    completion = _completion_record(snapshot)
    validator_results = []
    for item in completion.get("validator_results", []):
        if not isinstance(item, Mapping):
            continue
        validator_id = str(item.get("id") or "website-validator")
        raw_status = str(item.get("status", "")).lower()
        status = (
            "pass"
            if raw_status in {"pass", "passed", "complete", "completed"}
            else "fail"
            if raw_status in {"fail", "failed", "error", "blocked"}
            else "skipped"
            if raw_status in {"skip", "skipped", "not_run", "not-run"}
            else "warning"
        )
        notes = []
        evidence = item.get("evidence")
        if isinstance(evidence, str) and evidence:
            notes.append(evidence)
        validator_results.append(
            {
                "validator_id": validator_id,
                "validator_class": _validator_class(validator_id),
                "status": status,
                "reason_code": None,
                "evidence_ref": snapshot.record_paths.get("completion"),
                "notes": notes,
            }
        )
    extension = result.get("extensions", {}).get(ADAPTER_EXTENSION, {}).get("data", {})
    checkpoint = checkpoint_evidence(snapshot)
    human_gate = result.get("status") == "human_gate_required"
    return {
        "completion_contract_results": [
            dict(item) for item in completion_contract_results
        ],
        "checkpoint": checkpoint,
        "validator_results": validator_results,
        "revision_before": extension.get("before_git", {}).get("head"),
        "revision_after": snapshot.git["head"],
        "progress_summary": (
            str(completion.get("summary"))
            if completion.get("summary")
            else "The website continuation boundary was evaluated from direct evidence."
        ),
        "remaining_work": str(
            snapshot.resolver.get("next_recommended_action", {}).get("summary")
            or "Reevaluate the durable goal against canonical evidence."
        ),
        "human_gate_outstanding": human_gate,
        "extensions": {
            ADAPTER_EXTENSION: {
                "version": "0.1.0",
                "required": True,
                "data": {
                    "record_hashes": snapshot.record_hashes,
                    "source_authority": snapshot.source_authority,
                },
            }
        },
    }
