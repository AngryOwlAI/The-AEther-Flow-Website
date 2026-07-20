"""Read-only adapter for AEther's tracked research-control protocol.

The adapter maps existing authority into inspectable portable interfaces.  It
does not create, activate, repair, checkpoint, or rewrite AEther records.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.adapters.protocols import (
    ADAPTER_CAPABILITY_VERSION,
    AdapterCapabilityReport,
    FeatureCapability,
    ValidationResult,
)
from agentjob_runtime.errors import IntegrityError, RecordNotFound, RecordValidationError
from agentjob_runtime.records.canonical import content_sha256, parse_yaml_subset


CORE_REGISTRIES = (
    "AGENT_ROLE_REGISTRY.csv",
    "ROLE_EXECUTION_REGISTRY.csv",
    "DIRECTOR_DECISION_REGISTRY.csv",
    "AGENT_JOB_REGISTRY.csv",
    "RESEARCH_TASK_REGISTRY.csv",
    "CLAIM_BOUNDARY_REGISTRY.csv",
)

SOURCE_BINDING_FILES = (
    ".codex/skills/continue-research/SKILL.md",
    ".codex/skills/continue-research-goal/SKILL.md",
    ".codex/skills/continue-research-continue-goal/SKILL.md",
    ".codex/skills/continue-research-goal/references/goal-file-schema.md",
    ".codex/skills/continue-research-goal/scripts/goal_state.py",
    "github-facing/director-agentjob-lifecycle-explainer.md",
    "research_control/AGENTS.md",
    "research_control/program_state.yaml",
    ".agents/schemas/AGENT_JOB_SCHEMA.md",
    ".agents/schemas/DIRECTOR_DECISION_SCHEMA.md",
    ".agents/schemas/EXECUTION_ROLE_SCHEMA.md",
    "scripts/research_control/continue_research.py",
    "scripts/research_control/continue_research_memory_preflight.py",
    "scripts/research_control/validate_research_control.py",
    "scripts/research_control/checkpoint_research_transaction.py",
)

REQUIRED_PATHS = SOURCE_BINDING_FILES + tuple(
    f"registries/{name}" for name in CORE_REGISTRIES
) + ("research_control/tasks", "research_control/handoffs", ".agents/roles")

AETHER_STOP_CONDITIONS = (
    "requires_human_gate=true",
    "validation fails",
    "no role fits",
    "selected role needs authority expansion",
    "job would touch paths outside its allowlist",
    "canonical ontology change or other protected authority requires human gate",
)

REQUIRED_ADAPTER_FEATURES = (
    "tracked-program-state",
    "task-records",
    "director-decisions",
    "agentjob-records",
    "execution-role-bindings",
    "completion-records",
    "handoffs",
    "registry-indexes",
    "legacy-boundary-resolver",
    "memory-context-provider",
    "checkpoint-provider",
)


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


class AetherProjectAdapter:
    """Map AEther authority without becoming an AEther mutation surface."""

    adapter_id = "aether-research-control"
    version = "1.0.0"

    def __init__(self, project_root: str | Path) -> None:
        self.project_root = Path(project_root).expanduser().resolve()

    def _path(self, relative: str, *, must_exist: bool = True) -> Path:
        supplied = Path(relative)
        if supplied.is_absolute() or ".." in supplied.parts:
            raise IntegrityError(
                f"AEther adapter path is not project-relative: {relative}",
                details={"reason_code": "aether.path_escape"},
            )
        candidate = self.project_root.joinpath(*supplied.parts)
        resolved = candidate.resolve(strict=False)
        if not resolved.is_relative_to(self.project_root):
            raise IntegrityError(
                f"AEther adapter path escapes the project root: {relative}",
                details={"reason_code": "aether.path_escape"},
            )
        if candidate.is_symlink():
            raise IntegrityError(
                f"AEther authority path may not be a symlink: {relative}",
                details={"reason_code": "aether.symlink_authority"},
            )
        if must_exist and not candidate.exists():
            raise RecordNotFound(
                f"AEther authority path is missing: {relative}",
                details={"reason_code": "aether.authority_missing", "path": relative},
            )
        return candidate

    def _read_bytes(self, relative: str) -> bytes:
        path = self._path(relative)
        if not path.is_file():
            raise RecordValidationError(f"AEther authority path is not a file: {relative}")
        before = path.read_bytes()
        if path.read_bytes() != before:
            raise IntegrityError(
                f"AEther authority changed during read: {relative}",
                details={"reason_code": "aether.concurrent_read_change"},
            )
        return before

    def _load_yaml(self, relative: str) -> dict[str, Any]:
        value = parse_yaml_subset(self._read_bytes(relative).decode("utf-8"), source=relative)
        if not isinstance(value, dict):
            raise RecordValidationError(f"AEther YAML authority must be a mapping: {relative}")
        return value

    def _load_frontmatter(self, relative: str) -> tuple[dict[str, Any], str]:
        text = self._read_bytes(relative).decode("utf-8")
        if not text.startswith("---\n"):
            raise RecordValidationError(f"AEther Markdown authority lacks frontmatter: {relative}")
        frontmatter, separator, body = text[4:].partition("\n---\n")
        if not separator:
            raise RecordValidationError(f"AEther Markdown authority has no frontmatter close: {relative}")
        value = parse_yaml_subset(frontmatter, source=f"{relative}:frontmatter")
        if not isinstance(value, dict):
            raise RecordValidationError(f"AEther frontmatter must be a mapping: {relative}")
        return value, body

    def _read_registry(self, name: str) -> list[dict[str, str]]:
        relative = f"registries/{name}"
        text = self._read_bytes(relative).decode("utf-8-sig")
        reader = csv.DictReader(text.splitlines())
        if not reader.fieldnames:
            raise RecordValidationError(f"AEther registry has no header: {relative}")
        return [dict(row) for row in reader]

    @staticmethod
    def _by_id(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, dict[str, str]]:
        return {str(row[key]): dict(row) for row in rows if row.get(key)}

    @staticmethod
    def _feature(feature_id: str, available: bool, reason: str | None = None) -> FeatureCapability:
        return FeatureCapability(
            feature_id,
            "1.0.0",
            True,
            available,
            "native" if available else "unsupported",
            reason,
        )

    def discover(self, project_root: Path) -> AdapterCapabilityReport:
        root = Path(project_root).expanduser().resolve()
        available = root == self.project_root
        reason = None if available else "aether.project_root_mismatch"
        if available:
            missing = [relative for relative in REQUIRED_PATHS if not self._path(relative, must_exist=False).exists()]
            available = not missing
            if missing:
                reason = "aether.required_authority_missing"
        features = tuple(self._feature(item, available, reason) for item in REQUIRED_ADAPTER_FEATURES)
        features += (
            FeatureCapability(
                "portable-activation-manifest",
                "1.0.0",
                False,
                False,
                "unsupported",
                "aether.legacy_activation_is_record_linkage",
            ),
            FeatureCapability(
                "legacy-goal-mutation",
                "1.0.0",
                False,
                False,
                "unsupported",
                "aether.legacy_goals_are_reader_only",
            ),
            FeatureCapability(
                "cross-platform-legacy-locking",
                "1.0.0",
                False,
                False,
                "unsupported",
                "aether.legacy_helper_uses_posix_fcntl",
            ),
            FeatureCapability(
                "domain-truth-promotion",
                "1.0.0",
                False,
                False,
                "unsupported",
                "aether.process_evidence_is_not_scientific_authority",
            ),
        )
        return AdapterCapabilityReport(
            self.adapter_id,
            self.version,
            ADAPTER_CAPABILITY_VERSION,
            features,
            ("research_control", ".agents/schemas", ".agents/roles", "registries"),
            (
                "portable-activation-manifest",
                "legacy-goal-mutation",
                "cross-platform-legacy-locking",
                "domain-truth-promotion",
            ),
            (
                "resolve_boundary",
                "conformance_claims",
                "validate_decision",
                "validate_job",
            ),
        )

    def source_hashes(self) -> dict[str, str]:
        return {
            relative: hashlib.sha256(self._read_bytes(relative)).hexdigest()
            for relative in SOURCE_BINDING_FILES
        }

    def _active_authority(self) -> dict[str, Any]:
        program_state = self._load_yaml("research_control/program_state.yaml")
        task_rows = self._read_registry("RESEARCH_TASK_REGISTRY.csv")
        decision_rows = self._read_registry("DIRECTOR_DECISION_REGISTRY.csv")
        job_rows = self._read_registry("AGENT_JOB_REGISTRY.csv")
        role_rows = self._read_registry("ROLE_EXECUTION_REGISTRY.csv")
        active_task_id = str(program_state.get("active_task_id", ""))
        task_row = self._by_id(task_rows, "task_id").get(active_task_id, {})
        decision_id = str(task_row.get("current_decision_id", ""))
        job_id = str(task_row.get("current_job_id", ""))
        decision_row = self._by_id(decision_rows, "decision_id").get(decision_id, {})
        job_row = self._by_id(job_rows, "job_id").get(job_id, {})
        role_row = next(
            (
                dict(row)
                for row in role_rows
                if row.get("task_id") == active_task_id and row.get("agent_job_id") == job_id
            ),
            {},
        )
        return {
            "program_state": program_state,
            "task_rows": task_rows,
            "decision_rows": decision_rows,
            "job_rows": job_rows,
            "role_rows": role_rows,
            "active_task_id": active_task_id,
            "task_row": task_row,
            "decision_id": decision_id,
            "decision_row": decision_row,
            "job_id": job_id,
            "job_row": job_row,
            "role_row": role_row,
        }

    @staticmethod
    def _record_path(row: Mapping[str, str], *keys: str) -> str | None:
        for key in keys:
            value = str(row.get(key, "")).strip()
            if value:
                return value
        return None

    def _optional_yaml(self, relative: str | None) -> dict[str, Any] | None:
        if not relative:
            return None
        path = self._path(relative, must_exist=False)
        return self._load_yaml(relative) if path.is_file() else None

    def _optional_frontmatter(self, relative: str | None) -> dict[str, Any] | None:
        if not relative:
            return None
        path = self._path(relative, must_exist=False)
        return self._load_frontmatter(relative)[0] if path.is_file() else None

    def _latest_handoff(self, program_state: Mapping[str, Any]) -> tuple[str, dict[str, Any] | None]:
        handoff_id = str(program_state.get("latest_handoff_id", ""))
        if not handoff_id:
            return "", None
        path = f"research_control/handoffs/{handoff_id}.yaml"
        return path, self._optional_yaml(path)

    def _required_authority_surfaces(
        self,
        authority: Mapping[str, Any],
        handoff_path: str,
    ) -> list[str]:
        active_task_id = str(authority["active_task_id"])
        values = [
            "AGENTS.md",
            "research_control/AGENTS.md",
            "research_control/program_state.yaml",
            "registries/AGENT_ROLE_REGISTRY.csv",
            "registries/ROLE_EXECUTION_REGISTRY.csv",
            "registries/DIRECTOR_DECISION_REGISTRY.csv",
            "registries/AGENT_JOB_REGISTRY.csv",
            "registries/RESEARCH_TASK_REGISTRY.csv",
        ]
        if handoff_path:
            values.extend([handoff_path, handoff_path.removesuffix(".yaml") + ".md"])
        if active_task_id:
            values.append(f"research_control/tasks/{active_task_id}/00_TASK.yaml")
        decision_path = self._record_path(authority["decision_row"], "decision_path")
        if decision_path:
            values.append(decision_path)
        job_path = self._record_path(authority["job_row"], "job_path")
        if job_path:
            values.append(job_path)
        return list(dict.fromkeys(values))

    def resolve_boundary(self) -> dict[str, Any]:
        """Mirror AEther's deterministic resolver over tracked records only."""

        authority = self._active_authority()
        program_state = authority["program_state"]
        task_row = authority["task_row"]
        decision_row = authority["decision_row"]
        job_id = str(authority["job_id"])
        pending_jobs = [
            {
                "job_id": row.get("job_id", ""),
                "task_id": row.get("task_id", ""),
                "decision_id": row.get("decision_id", ""),
                "role_id": row.get("role_id", ""),
                "role_version": row.get("role_version", ""),
                "job_path": row.get("job_path", ""),
                "requires_human_gate": row.get("requires_human_gate", ""),
                "status": row.get("status", ""),
            }
            for row in authority["job_rows"]
            if row.get("status") in {"pending", "active"}
        ]
        handoff_path, handoff = self._latest_handoff(program_state)
        next_action = str((handoff or {}).get("next_action", ""))
        boundary = "director_decision_required"
        if _bool(task_row.get("requires_human_gate")) or _bool(
            decision_row.get("requires_human_gate")
        ):
            boundary = "human_gate_required"
        elif pending_jobs:
            matching = [
                item
                for item in pending_jobs
                if item["task_id"] == authority["active_task_id"]
                and item["decision_id"] == authority["decision_id"]
                and (not job_id or item["job_id"] == job_id)
            ]
            boundary = "existing_agent_job_ready" if len(matching) == 1 else "blocked"
        elif not next_action and str(program_state.get("next_recommended_action", "")).upper() == "NONE":
            boundary = "no_action"

        role_rows = self._read_registry("AGENT_ROLE_REGISTRY.csv")
        roles = [
            {
                "role_id": row.get("role_id", ""),
                "version": row.get("version", ""),
                "role_kind": row.get("role_kind", ""),
                "authority_level": row.get("authority_level", ""),
                "requires_human_gate": row.get("requires_human_gate", ""),
                "contract_path": row.get("role_contract_path", ""),
            }
            for row in role_rows
            if row.get("status") == "active" or row.get("role_id") == "gate-chair"
        ]
        return {
            "status": "ready",
            "boundary": boundary,
            "active_task_id": authority["active_task_id"],
            "latest_handoff_id": str(program_state.get("latest_handoff_id", "")),
            "latest_handoff_path": handoff_path,
            "current_decision_id": authority["decision_id"],
            "current_job_id": authority["job_id"],
            "current_status": str(program_state.get("current_status", "")),
            "next_action": next_action,
            "next_recommended_action": str(
                program_state.get("next_recommended_action", next_action)
            ),
            "available_roles": roles,
            "pending_or_active_jobs": pending_jobs,
            "required_authority_surfaces": self._required_authority_surfaces(
                authority, handoff_path
            ),
            "stop_conditions": list(AETHER_STOP_CONDITIONS),
            "validation_errors": [],
            "validator_commands": [
                ".venv/bin/python scripts/research_control/validate_research_control.py --check-diff",
                ".venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only",
            ],
            "context_provider": {
                "provider_id": "aether-memory-preflight",
                "command": ".venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json",
                "canonical_source_inspection_required": True,
            },
            "checkpoint_provider": {
                "provider_id": "aether-research-checkpoint",
                "command_template": ".venv/bin/python scripts/research_control/checkpoint_research_transaction.py --job-id <JOB_ID>",
                "required_after_execution": boundary
                in {"director_decision_required", "existing_agent_job_ready"},
            },
            "execution_boundary": "one bounded AgentJob per invocation",
            "authority_model": "tracked research_control records are canonical; registries are indexes",
            "domain_truth": "not_evaluated",
            "execution_performed": False,
        }

    def _load_current_records(self, authority: Mapping[str, Any]) -> dict[str, Any]:
        task_path = self._record_path(authority["task_row"], "task_path") or (
            f"research_control/tasks/{authority['active_task_id']}/00_TASK.yaml"
            if authority["active_task_id"]
            else None
        )
        decision_path = self._record_path(authority["decision_row"], "decision_path") or (
            f"research_control/tasks/{authority['active_task_id']}/{authority['decision_id']}.md"
            if authority["active_task_id"] and authority["decision_id"]
            else None
        )
        job_path = self._record_path(authority["job_row"], "job_path")
        role_path = self._record_path(authority["role_row"], "record_path", "execution_role_path")
        task = self._optional_yaml(task_path)
        decision = self._optional_frontmatter(decision_path)
        job = self._optional_yaml(job_path)
        role = self._optional_yaml(role_path)
        completion = None
        completion_path = None
        if job_path and authority["job_id"]:
            completion_path = (
                str(Path(job_path).parent / "completions" / f"AJC-{authority['job_id']}.yaml")
            )
            completion = self._optional_yaml(completion_path)
        return {
            "task": {"path": task_path, "record": task},
            "director_decision": {"path": decision_path, "record": decision},
            "agent_job": {"path": job_path, "record": job},
            "execution_role": {"path": role_path, "record": role},
            "completion": {"path": completion_path, "record": completion},
        }

    def load_authoritative_state(self) -> Mapping[str, Any]:
        report = self.discover(self.project_root)
        report.require(REQUIRED_ADAPTER_FEATURES)
        authority = self._active_authority()
        handoff_path, handoff = self._latest_handoff(authority["program_state"])
        current_records = self._load_current_records(authority)
        current_records["handoff"] = {"path": handoff_path, "record": handoff}
        resolver = self.resolve_boundary()
        sidecar_jobs = [
            item
            for item in resolver["pending_or_active_jobs"]
            if item["task_id"] != resolver["active_task_id"]
        ]
        return {
            "adapter": report.as_dict(),
            "canonical_source_roots": list(report.canonical_source_roots),
            "canonical_source_hashes": self.source_hashes(),
            "program_state": copy.deepcopy(authority["program_state"]),
            "records": current_records,
            "registries": {
                "tasks": copy.deepcopy(authority["task_rows"]),
                "decisions": copy.deepcopy(authority["decision_rows"]),
                "jobs": copy.deepcopy(authority["job_rows"]),
                "execution_roles": copy.deepcopy(authority["role_rows"]),
            },
            "resolver": resolver,
            "sidecar_jobs": sidecar_jobs,
            "authority_note": (
                "The tracked program-state task remains the ordinary research authority. "
                "Pending jobs for other tasks are exposed as sidecars and may block routing "
                "without replacing that tracked route."
            ),
            "domain_truth": "not_evaluated",
            "execution_performed": False,
        }

    def list_roles(self, snapshot: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
        resolver = snapshot.get("resolver", {})
        roles = resolver.get("available_roles", []) if isinstance(resolver, Mapping) else []
        if not isinstance(roles, list):
            raise RecordValidationError("AEther adapter role snapshot must be a list")
        return tuple(copy.deepcopy(roles))

    def list_routes(self, snapshot: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
        resolver = snapshot.get("resolver", {})
        if not isinstance(resolver, Mapping):
            return ()
        route = str(resolver.get("next_recommended_action", "")).strip()
        if not route:
            return ()
        return (
            {
                "route_id": "aether-next-recommended-route",
                "status": "candidate",
                "description": route,
                "selection_authority": "director_required",
                "task_id": resolver.get("active_task_id"),
                "domain_truth": "not_evaluated",
            },
        )

    @staticmethod
    def _required(record: Mapping[str, Any], fields: Sequence[str], kind: str) -> ValidationResult:
        missing = tuple(field for field in fields if field not in record)
        if missing:
            return ValidationResult(
                "fail",
                f"aether.{kind}_fields_missing",
                tuple(f"missing field: {field}" for field in missing),
            )
        return ValidationResult("pass", evidence={"record_kind": kind})

    def validate_decision(self, decision: Mapping[str, Any]) -> ValidationResult:
        return self._required(
            decision,
            (
                "decision_id",
                "task_id",
                "director_version",
                "decision_type",
                "selected_role_id",
                "selected_role_version",
                "agent_job_id",
                "status",
                "supersedes_decision_id",
                "requires_human_gate",
                "role_fit_candidates",
            ),
            "director_decision",
        )

    def validate_job(self, job: Mapping[str, Any]) -> ValidationResult:
        result = self._required(
            job,
            (
                "job_id",
                "task_id",
                "decision_id",
                "role_id",
                "role_version",
                "status",
                "requires_human_gate",
                "allowed_read_paths",
                "allowed_write_paths",
                "allowed_generated_paths",
                "forbidden_paths",
                "allowed_source_classes",
                "forbidden_source_classes",
                "approved_commands",
                "required_validators",
                "expected_outputs",
                "claim_boundary",
            ),
            "agent_job",
        )
        if result.blocking:
            return result
        overlap = sorted(set(job["allowed_write_paths"]) & set(job["forbidden_paths"]))
        if overlap:
            return ValidationResult(
                "fail",
                "aether.path_authority_conflict",
                tuple(f"write path is also forbidden: {item}" for item in overlap),
            )
        return result

    def evaluate_completion(self, completion: Mapping[str, Any]) -> ValidationResult:
        result = self._required(
            completion,
            ("completion_id", "job_id", "task_id", "decision_id", "status", "validation_status"),
            "completion",
        )
        if result.blocking:
            return result
        if _bool(completion.get("physics_promotion_authorized")) and not completion.get(
            "promotion_authority_path"
        ):
            return ValidationResult(
                "fail",
                "aether.physics_promotion_authority_missing",
                ("A true physics promotion flag requires an explicit authority path.",),
            )
        return ValidationResult(
            "pass",
            evidence={"domain_truth": "not_evaluated", "record_kind": "completion"},
        )

    def compute_domain_fingerprint(self) -> Mapping[str, Any]:
        files: dict[str, str] = {}
        for root_name in ("research_control", ".agents/schemas", ".agents/roles", "registries"):
            root = self._path(root_name)
            for path in sorted(root.rglob("*")):
                if path.is_symlink():
                    raise IntegrityError(f"AEther canonical tree contains a symlink: {path}")
                if path.is_file():
                    relative = path.relative_to(self.project_root).as_posix()
                    files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        digest = content_sha256(files)
        return {
            "adapter_id": self.adapter_id,
            "adapter_version": self.version,
            "canonical_source_roots": [
                "research_control",
                ".agents/schemas",
                ".agents/roles",
                "registries",
            ],
            "file_count": len(files),
            "tree_sha256": digest,
            "domain_truth": "not_evaluated",
        }

    def conformance_claims(self) -> Mapping[str, Mapping[str, Any]]:
        claims = {
            "task": ("native", "research_control/tasks/<task-id>/00_TASK.yaml"),
            "director_decision": ("native", ".agents/schemas/DIRECTOR_DECISION_SCHEMA.md"),
            "agent_job": ("native", ".agents/schemas/AGENT_JOB_SCHEMA.md"),
            "execution_role": ("native", ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"),
            "completion": ("native", "research_control/tasks/<task-id>/jobs/completions/"),
            "handoff": ("native", "research_control/handoffs/"),
            "immutability": ("native", "research_control/AGENTS.md"),
            "supersession": ("native", ".agents/schemas/DIRECTOR_DECISION_SCHEMA.md"),
            "one_job_cardinality": ("native", ".codex/skills/continue-research/SKILL.md"),
            "claim_boundary": ("native", ".agents/schemas/AGENT_JOB_SCHEMA.md"),
            "path_boundary": ("native", ".agents/schemas/AGENT_JOB_SCHEMA.md"),
            "recovery_evidence": (
                "emulated",
                ".codex/skills/continue-research-goal/scripts/goal_state.py",
            ),
        }
        return {
            feature: {
                "mode": mode,
                "status": "pass",
                "evidence": [evidence],
                "reason_code": None,
            }
            for feature, (mode, evidence) in claims.items()
        }


def render_adapter_summary(adapter: AetherProjectAdapter) -> str:
    """Return deterministic JSON suitable for diagnostics and shadow reports."""

    return json.dumps(adapter.load_authoritative_state(), sort_keys=True, indent=2) + "\n"
