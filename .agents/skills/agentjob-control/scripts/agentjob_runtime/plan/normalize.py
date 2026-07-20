"""Read-only runtime normalization through a planning-method adapter."""

from __future__ import annotations

import copy
import json
import re
import shlex
import tomllib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from agentjob_runtime.errors import RecordValidationError, SecurityError, StateConflict
from agentjob_runtime.plan.launcher import (
    PlanLauncherPreflight,
    PlanSourceRequest,
    secure_read_plan_source,
)
from agentjob_runtime.plan.model import require_implementation_plan
from agentjob_runtime.records.canonical import canonical_json_bytes, content_sha256
from agentjob_runtime.security import contains_secret
from agentjob_runtime.validation.schema import format_issues, validate_instance


PLANNING_ADAPTER_ID = "prd-to-implementation-plan"
SOURCE_CLASSES = frozenset(
    {
        "structured_plan",
        "partial_plan",
        "task_list",
        "phase_outline",
        "requirements",
        "prose",
        "mixed_source",
    }
)
MEMBER_SOURCE_CLASSES = SOURCE_CLASSES - {"mixed_source"}
NORMALIZATION_STATUSES = frozenset(
    {"candidate", "blocked", "human_gate_required"}
)
TASK_SIZING_RESULTS = frozenset(
    {"ready", "split_required", "blocked", "human_gate_required"}
)
TRANSFORMATIONS = frozenset(
    {"preserved", "canonicalized", "synthesized", "overridden", "deferred"}
)
UNKNOWN_COMMAND_GUIDANCE = (
    "Discover and document the correct command before coding"
)
DEFAULT_COMMAND_SOURCE_BYTES = 1024 * 1024
SAFE_COMMAND_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
MAKE_TARGET = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.-]*):(?:[^=]|$)")
JUST_RECIPE = re.compile(
    r"^([A-Za-z0-9][A-Za-z0-9_.-]*)(?:\s+[^:=]+)?\s*:(?!=)"
)


class NormalizerCallable(Protocol):
    """Established offline normalizer interface used by the runtime adapter."""

    def __call__(
        self,
        paths: list[str],
        *,
        source_root: Path,
        authorities: list[str] | None = None,
        precedences: list[int] | None = None,
    ) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class RepositoryCommand:
    """One repository-declared command with its direct evidence source."""

    argv: tuple[str, ...]
    source_path: str
    source_kind: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "argv": list(self.argv),
            "command": shlex.join(self.argv),
            "source_path": self.source_path,
            "source_kind": self.source_kind,
        }


@dataclass(frozen=True)
class RepositoryCommandDiscovery:
    """Read-only command evidence; discovered commands are not execution authority."""

    commands: tuple[RepositoryCommand, ...]
    sources_examined: tuple[str, ...]

    @property
    def status(self) -> str:
        return "discovered" if self.commands else "not_found"

    def as_dict(self) -> dict[str, Any]:
        result = {
            "status": self.status,
            "commands": [command.as_dict() for command in self.commands],
            "sources_examined": list(self.sources_examined),
        }
        if not self.commands:
            result["guidance"] = UNKNOWN_COMMAND_GUIDANCE
        return result


class PlanningAdapter(Protocol):
    """Portable planning-method boundary for one preflight result."""

    adapter_id: str
    available: bool
    supported_source_classes: frozenset[str]

    def normalize(self, preflight: PlanLauncherPreflight) -> Mapping[str, Any]: ...

    def discover_repository_commands(
        self,
        project_root: Path,
    ) -> RepositoryCommandDiscovery: ...


@dataclass(frozen=True)
class PrdToImplementationPlanAdapter:
    """Bind the accepted normalizer callable to the named planning method."""

    normalizer: NormalizerCallable = field(repr=False)
    command_discoverer: Callable[
        [Path], RepositoryCommandDiscovery
    ] | None = field(default=None, repr=False)
    available: bool = True
    adapter_id: str = PLANNING_ADAPTER_ID
    supported_source_classes: frozenset[str] = SOURCE_CLASSES

    def __post_init__(self) -> None:
        if self.command_discoverer is None:
            object.__setattr__(
                self,
                "command_discoverer",
                discover_repository_commands,
            )

    def normalize(self, preflight: PlanLauncherPreflight) -> Mapping[str, Any]:
        return self.normalizer(
            [source.relative_path for source in preflight.sources],
            source_root=Path(preflight.project_root),
            authorities=[source.authority for source in preflight.sources],
            precedences=[source.precedence for source in preflight.sources],
        )

    def discover_repository_commands(
        self,
        project_root: Path,
    ) -> RepositoryCommandDiscovery:
        if self.command_discoverer is None:  # Defensive; __post_init__ binds it.
            raise _error(
                "repository command discoverer is unavailable",
                reason_code="plan_task.capability_missing",
            )
        return self.command_discoverer(project_root)


@dataclass(frozen=True)
class PlanNormalizationResult:
    """Validated transient normalization output with no durable or provider effect."""

    status: str
    planning_adapter_id: str
    source_set_class: str
    candidate_plan: Mapping[str, Any] | None = field(repr=False)
    normalization_report: Mapping[str, Any] = field(repr=False)
    repository_commands: RepositoryCommandDiscovery
    state_writes: int = 0
    provider_create_calls: int = 0
    worker_discussions: int = 0
    agentjobs_executed: int = 0
    continue_invocations: int = 0
    task_reservations: int = 0
    branch_creations: int = 0
    worktree_creations: int = 0

    @property
    def ready_for_initialization(self) -> bool:
        return self.status == "candidate"

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "planning_adapter_id": self.planning_adapter_id,
            "source_set_class": self.source_set_class,
            "ready_for_initialization": self.ready_for_initialization,
            "candidate_plan": copy.deepcopy(self.candidate_plan),
            "normalization_report": copy.deepcopy(self.normalization_report),
            "repository_commands": self.repository_commands.as_dict(),
            "state_writes": self.state_writes,
            "provider_create_calls": self.provider_create_calls,
            "worker_discussions": self.worker_discussions,
            "agentjobs_executed": self.agentjobs_executed,
            "continue_invocations": self.continue_invocations,
            "task_reservations": self.task_reservations,
            "branch_creations": self.branch_creations,
            "worktree_creations": self.worktree_creations,
        }


def _error(
    message: str,
    *,
    reason_code: str = "plan.validation_failed",
    **details: Any,
) -> RecordValidationError:
    return RecordValidationError(
        message,
        details={"reason_code": reason_code, **details},
    )


def _read_command_source(
    project_root: Path,
    relative_path: str,
    *,
    max_bytes: int,
) -> str | None:
    path = project_root / relative_path
    if not path.exists():
        return None
    intake = secure_read_plan_source(
        project_root,
        PlanSourceRequest(relative_path, "advisory", 0),
        max_bytes=max_bytes,
    )
    return intake.text


def _deduplicate_commands(
    commands: Sequence[RepositoryCommand],
) -> tuple[RepositoryCommand, ...]:
    unique: dict[tuple[tuple[str, ...], str, str], RepositoryCommand] = {}
    for command in commands:
        if (
            not command.argv
            or any(not isinstance(item, str) or not item for item in command.argv)
            or not command.source_path
            or not command.source_kind
        ):
            raise _error("repository command evidence is malformed")
        key = (command.argv, command.source_path, command.source_kind)
        unique[key] = command
    return tuple(unique[key] for key in sorted(unique))


def discover_repository_commands(
    project_root: Path,
    *,
    max_source_bytes: int = DEFAULT_COMMAND_SOURCE_BYTES,
) -> RepositoryCommandDiscovery:
    """Discover commands explicitly declared by bounded repository surfaces."""

    try:
        root = Path(project_root).expanduser().resolve(strict=True)
    except (OSError, TypeError) as error:
        raise _error(
            "repository command discovery requires an existing project root",
            reason_code="plan.repository_mismatch",
        ) from error
    if (
        isinstance(max_source_bytes, bool)
        or not isinstance(max_source_bytes, int)
        or max_source_bytes <= 0
    ):
        raise _error("max_source_bytes must be a positive integer")

    commands: list[RepositoryCommand] = []
    examined: list[str] = []

    package_text = _read_command_source(
        root,
        "package.json",
        max_bytes=max_source_bytes,
    )
    if package_text is not None:
        examined.append("package.json")
        try:
            package = json.loads(package_text)
        except json.JSONDecodeError as error:
            raise _error(
                "package.json is not valid JSON",
                source_path="package.json",
            ) from error
        scripts = package.get("scripts") if isinstance(package, Mapping) else None
        if scripts is not None and not isinstance(scripts, Mapping):
            raise _error(
                "package.json scripts must be an object",
                source_path="package.json",
            )
        manager = (
            "pnpm"
            if (root / "pnpm-lock.yaml").is_file()
            else "yarn"
            if (root / "yarn.lock").is_file()
            else "npm"
        )
        for name in sorted(scripts or {}):
            value = scripts[name]
            if (
                not isinstance(name, str)
                or not SAFE_COMMAND_NAME.fullmatch(name)
                or not isinstance(value, str)
                or not value.strip()
            ):
                raise _error(
                    "package.json contains an invalid script declaration",
                    source_path="package.json",
                )
            commands.append(
                RepositoryCommand(
                    (manager, "run", name),
                    "package.json",
                    "package_script",
                )
            )

    for make_path in ("Makefile", "makefile"):
        make_text = _read_command_source(
            root,
            make_path,
            max_bytes=max_source_bytes,
        )
        if make_text is None:
            continue
        examined.append(make_path)
        for line in make_text.splitlines():
            match = MAKE_TARGET.match(line)
            if match and not match.group(1).startswith("."):
                commands.append(
                    RepositoryCommand(
                        ("make", match.group(1)),
                        make_path,
                        "make_target",
                    )
                )
        break

    for just_path in ("Justfile", "justfile"):
        just_text = _read_command_source(
            root,
            just_path,
            max_bytes=max_source_bytes,
        )
        if just_text is None:
            continue
        examined.append(just_path)
        for line in just_text.splitlines():
            match = JUST_RECIPE.match(line)
            if match and not match.group(1).startswith("_"):
                commands.append(
                    RepositoryCommand(
                        ("just", match.group(1)),
                        just_path,
                        "just_recipe",
                    )
                )
        break

    pyproject_text = _read_command_source(
        root,
        "pyproject.toml",
        max_bytes=max_source_bytes,
    )
    if pyproject_text is not None:
        examined.append("pyproject.toml")
        try:
            pyproject = tomllib.loads(pyproject_text)
        except tomllib.TOMLDecodeError as error:
            raise _error(
                "pyproject.toml is not valid TOML",
                source_path="pyproject.toml",
            ) from error
        project = pyproject.get("project")
        scripts = project.get("scripts") if isinstance(project, Mapping) else None
        if scripts is not None and not isinstance(scripts, Mapping):
            raise _error(
                "pyproject.toml project.scripts must be a table",
                source_path="pyproject.toml",
            )
        for name in sorted(scripts or {}):
            value = scripts[name]
            if (
                not isinstance(name, str)
                or not SAFE_COMMAND_NAME.fullmatch(name)
                or not isinstance(value, str)
                or not value.strip()
            ):
                raise _error(
                    "pyproject.toml contains an invalid project script",
                    source_path="pyproject.toml",
                )
            commands.append(
                RepositoryCommand(
                    (name,),
                    "pyproject.toml",
                    "project_script",
                )
            )

    return RepositoryCommandDiscovery(
        _deduplicate_commands(commands),
        tuple(examined),
    )


def _validate_preflight(preflight: PlanLauncherPreflight) -> None:
    if not isinstance(preflight, PlanLauncherPreflight):
        raise _error("normalization requires the canonical launcher preflight")
    if preflight.status != "ready" or not preflight.sources:
        raise _error("normalization requires a ready preflight with sources")
    effect_counts = {
        "state_writes": preflight.state_writes,
        "provider_create_calls": preflight.provider_create_calls,
        "agentjobs_executed": preflight.agentjobs_executed,
        "continue_invocations": preflight.continue_invocations,
    }
    if any(value != 0 for value in effect_counts.values()):
        raise _error(
            "normalization preflight contains an unexpected prior effect",
            effect_counts=effect_counts,
        )
    if not isinstance(preflight.repository_binding, Mapping) or not (
        preflight.repository_binding
    ):
        raise _error(
            "normalization preflight lacks repository binding evidence",
            reason_code="plan.repository_mismatch",
        )


def _validate_adapter(adapter: PlanningAdapter) -> None:
    if (
        getattr(adapter, "available", False) is not True
        or getattr(adapter, "adapter_id", None) != PLANNING_ADAPTER_ID
    ):
        raise _error(
            "required planning adapter is unavailable",
            reason_code="plan_task.capability_missing",
            missing=[PLANNING_ADAPTER_ID],
        )
    supported = getattr(adapter, "supported_source_classes", frozenset())
    missing_classes = sorted(SOURCE_CLASSES - set(supported))
    if missing_classes:
        raise _error(
            "planning adapter does not declare every required source route",
            reason_code="plan_task.capability_missing",
            missing=missing_classes,
        )


def _validate_source_parity(
    preflight: PlanLauncherPreflight,
    report: Mapping[str, Any],
    source_set_class: str,
) -> None:
    sources = report.get("sources")
    if not isinstance(sources, list) or len(sources) != len(preflight.sources):
        raise StateConflict(
            "normalizer source set differs from launcher intake",
            details={"reason_code": "plan.hash_mismatch"},
        )
    for intake, source in zip(preflight.sources, sources, strict=True):
        if not isinstance(source, Mapping):
            raise _error("normalization report source evidence is malformed")
        exact = (
            source.get("immutable_ref") == intake.relative_path
            and source.get("source_sha256") == intake.source_sha256
            and source.get("authority") == intake.authority
            and source.get("precedence") == intake.precedence
        )
        if not exact:
            raise StateConflict(
                "normalized source identity differs from launcher intake",
                details={
                    "reason_code": "plan.hash_mismatch",
                    "path": intake.relative_path,
                },
            )
        if source.get("source_class") not in MEMBER_SOURCE_CLASSES:
            raise _error(
                "normalization report contains an invalid member source class",
                source_class=source.get("source_class"),
            )
    expected_set_class = (
        "mixed_source" if len(sources) > 1 else sources[0]["source_class"]
    )
    if source_set_class != expected_set_class:
        raise _error("normalizer source-set classification is inconsistent")
    if report.get("source_set_sha256") != content_sha256(sources):
        raise StateConflict(
            "normalizer source-set hash is invalid",
            details={"reason_code": "plan.hash_mismatch"},
        )


def _validate_normalization_output(
    preflight: PlanLauncherPreflight,
    output: Mapping[str, Any],
    *,
    plan_schema_path: str | Path,
    normalization_report_schema_path: str | Path,
) -> tuple[str, str, Mapping[str, Any] | None, Mapping[str, Any]]:
    if not isinstance(output, Mapping):
        raise _error("planning adapter must return a mapping")
    source_set_class = output.get("source_set_class")
    if source_set_class not in SOURCE_CLASSES:
        raise _error(
            "planning adapter returned an invalid source-set class",
            source_set_class=source_set_class,
        )
    report = output.get("normalization_report")
    if not isinstance(report, Mapping):
        raise _error("planning adapter omitted the normalization report")
    report_issues = validate_instance(
        report,
        normalization_report_schema_path,
    )
    if report_issues:
        raise _error(
            "normalization report failed canonical validation",
            findings=format_issues(report_issues).splitlines(),
        )
    if report.get("schema_version") != "sys4ai.plan-normalization-report.v1":
        raise _error("planning adapter returned an unsupported report version")
    status = report.get("status")
    if status not in NORMALIZATION_STATUSES:
        raise _error("normalization report has an invalid status", status=status)
    if report.get("finalized") is not True:
        raise _error("normalization report must be finalized")
    supplied_report_hash = report.get("report_content_sha256")
    expected_report_hash = content_sha256(
        {
            key: value
            for key, value in report.items()
            if key != "report_content_sha256"
        }
    )
    if supplied_report_hash != expected_report_hash:
        raise StateConflict(
            "normalization report content hash is invalid",
            details={"reason_code": "plan.hash_mismatch"},
        )
    if contains_secret(canonical_json_bytes(report).decode("utf-8")):
        raise SecurityError(
            "normalization report appears to contain a secret; redact it first",
            details={"reason_code": "security.secret_detected"},
        )
    _validate_source_parity(preflight, report, str(source_set_class))

    findings = report.get("findings")
    if not isinstance(findings, list) or any(
        not isinstance(finding, Mapping) for finding in findings
    ):
        raise _error("normalization report findings are malformed")
    severities = {finding.get("severity") for finding in findings}
    if (
        status == "candidate"
        and severities.intersection({"blocking", "human_gate"})
    ) or (status == "blocked" and "blocking" not in severities) or (
        status == "human_gate_required" and "human_gate" not in severities
    ):
        raise _error("normalization report status and findings disagree")

    sizing = report.get("task_sizing")
    if not isinstance(sizing, list) or not sizing:
        raise _error("normalization report requires task-sizing evidence")
    if any(
        not isinstance(item, Mapping)
        or item.get("result") not in TASK_SIZING_RESULTS
        for item in sizing
    ):
        raise _error("normalization report task-sizing evidence is invalid")

    traces = report.get("traceability")
    if not isinstance(traces, list) or not traces:
        raise _error("normalization report requires transformation traceability")
    if any(
        not isinstance(item, Mapping)
        or item.get("transformation") not in TRANSFORMATIONS
        for item in traces
    ):
        raise _error("normalization report traceability is invalid")

    candidate = output.get("candidate_plan")
    if status == "candidate":
        if not isinstance(candidate, Mapping):
            raise _error("candidate normalization omitted the candidate plan")
        candidate = require_implementation_plan(
            candidate,
            schema_path=plan_schema_path,
        )
        if candidate.get("repository_binding") != preflight.repository_binding:
            raise StateConflict(
                "candidate repository binding differs from launcher preflight",
                details={"reason_code": "plan.repository_mismatch"},
            )
        if report.get("candidate_plan_sha256") != content_sha256(candidate):
            raise StateConflict(
                "candidate plan hash differs from normalization report",
                details={"reason_code": "plan.hash_mismatch"},
            )
    elif candidate is not None or report.get("candidate_plan_sha256") is not None:
        raise _error("protected normalization result must not expose a candidate")
    return str(status), str(source_set_class), candidate, report


def normalize_plan_preflight(
    preflight: PlanLauncherPreflight,
    *,
    planning_adapter: PlanningAdapter,
    plan_schema_path: str | Path,
    normalization_report_schema_path: str | Path,
) -> PlanNormalizationResult:
    """Normalize one ready intake without state, provider, or AgentJob effects."""

    _validate_preflight(preflight)
    _validate_adapter(planning_adapter)
    output = planning_adapter.normalize(preflight)
    status, source_set_class, candidate, report = _validate_normalization_output(
        preflight,
        output,
        plan_schema_path=plan_schema_path,
        normalization_report_schema_path=normalization_report_schema_path,
    )
    commands = planning_adapter.discover_repository_commands(
        Path(preflight.project_root)
    )
    if not isinstance(commands, RepositoryCommandDiscovery):
        raise _error("planning adapter returned invalid command-discovery evidence")
    commands = RepositoryCommandDiscovery(
        _deduplicate_commands(commands.commands),
        tuple(commands.sources_examined),
    )
    return PlanNormalizationResult(
        status=status,
        planning_adapter_id=planning_adapter.adapter_id,
        source_set_class=source_set_class,
        candidate_plan=copy.deepcopy(candidate),
        normalization_report=copy.deepcopy(report),
        repository_commands=commands,
    )
